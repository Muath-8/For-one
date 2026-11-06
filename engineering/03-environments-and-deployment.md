# 03. Environments and deployment

Part of the For one engineering handbook. Written 2026-11-06 against architecture 01 D8, D9, D13, D14, §4.7, §4.8; 07 D7, §4.9, §4.13; 09 D9.

## 1. Three environments

| | `dev` | `staging` | `prod` |
|---|---|---|---|
| Where | a laptop, docker compose | AWS account `forone`, same region as prod, own VPC | AWS account `forone`, home region |
| Purpose | build and test for free | the 50 scripted calls, the Milestone 0 end-to-end run, every release before prod, vendor failover drills | learners |
| Data | synthetic only | synthetic learners plus consented Milestone 0 fixtures; never a copy of prod | real |
| Vendors | fakes by default | real keys, staging workspace per vendor where the vendor supports it | real keys, prod workspace |
| Postgres | compose | RDS `db.t4g.medium`, single AZ, 7-day backups, **stopped outside test windows** | RDS `db.t4g.large` Multi-AZ, 30-day backups, PITR |
| S3 | MinIO | `forone-{media,voice,exports}-staging` | `forone-{media,voice,exports}-prod`, versioning off, lifecycle rules |
| Inngest | dev server | Inngest Cloud env `staging` (EU) | Inngest Cloud env `prod` (EU) |
| LiveKit | dev server | LiveKit Cloud project `forone-staging` | LiveKit Cloud project `forone-prod` |
| `web` | `next dev` | Vercel preview per PR, `staging.<domain>` on `main` | `app.<domain>` from the release tag |
| Email | Mailpit | Resend test domain, delivery only to `@<domain>` addresses | Resend `<domain>` |
| Spend cap | $20/day per engineer key | $50/day | alerts at $50/day and $1.00/session; recomputed `max(50, learners × 1.50)` from launch |
| Who can deploy | anyone, to their laptop | CI, on merge to `main` | CI, from a tag, after one named approval |

There is no fourth environment. Preview environments for the backend were rejected (architecture 01 D14) for cost and time; a PR that needs a running backend to test is tested on staging, serially, by whoever holds the staging lock in Slack (`/staging claim`, a one-line bot or just a message).

**Staging is stopped when idle.** `tools/release staging up` and `staging down` start and stop RDS and scale the ECS services to zero. The nightly job (handbook 04 §6) starts it, runs, and stops it. Leaving staging up costs about $200 a month; the first engineer to notice it running on a weekend turns it off.

## 2. Region

`HOME_REGION` is one configuration key read by Terraform, the S3 and KMS clients and the task placement. The default is `me-central-1` (UAE). Counsel's answer on whether learner voice may rest in the UAE or the EU is due before Terraform is first applied (architecture 01 §10 #1); the fallback is `eu-central-1` and the move between the two is a one-day job as long as nothing has been written to prod. The call worker may run in `eu-central-1` for vendor latency regardless, because it holds nothing at rest.

If counsel requires data at rest inside Saudi Arabia, the GCP Dammam option is five to eight engineer-days and is a different Terraform tree. The handbook does not plan for it until counsel says so; if that answer arrives after week 1, the week-3 web work slips by the same amount.

Every managed vendor is pinned to its EU region where one exists: Inngest EU, Langfuse EU, Sentry EU, Vercel `dxb1` for the edge. Anthropic, Google and the voice and recognition vendors process in the US or EU regardless of our region; the processor register (`docs/ropa.md`, from architecture 07 §4.9) carries that disclosure.

## 3. Infrastructure as code: Terraform

Terraform is the choice, over CDK and Pulumi, for one reason: the team is Python-first but the infrastructure is small and standard (VPC, RDS, S3, KMS, ECS, ALB, WAF, IAM, Secrets Manager), and Terraform's AWS modules for exactly those pieces are the most widely read code on the internet. A second engineer or a contractor will know it on day one.

Layout:

```
infra/terraform/
├── modules/
│   ├── network/        VPC, two private and two public subnets, one NAT gateway, VPC endpoints for S3, ECR, Secrets Manager, CloudWatch
│   ├── rds/            Postgres 16, pgvector, parameter group with pgaudit, Multi-AZ as a variable
│   ├── storage/        three S3 buckets, lifecycle rules, bucket policies (deny unencrypted puts, deny non-SSE-C on learner prefixes)
│   ├── kms/            one CMK per environment plus the media service key; key policy limited to the three task roles and break-glass
│   ├── ecs/            cluster, three services, task definitions with secrets from Secrets Manager, autoscaling for call-worker with scale-in protection
│   ├── alb/            one ALB, listeners, WAF web ACL (rate rules, managed common set), /internal/* restricted to the VPC
│   ├── iam/            task roles (api, workflows, call-worker), the GitHub OIDC deploy role, the break-glass role (MFA condition)
│   ├── secrets/        the secret *names* and their IAM; never values
│   └── observability/  CloudWatch log groups (30 days), EMF metrics, the four dashboards
└── envs/
    ├── staging/        main.tf wires modules with staging sizes; backend config
    └── prod/
```

Rules:

- State lives in an S3 bucket `forone-tfstate` with DynamoDB locking, in the home region, encrypted, versioned, in the same account. Not Terraform Cloud: one fewer processor to register, and the state holds resource ids only.
- `terraform plan` runs in CI on every PR touching `infra/` and posts the plan as a PR comment. `terraform apply` runs only from `main` for staging and only from the release job for prod, both through the GitHub OIDC role; nobody applies from a laptop except during an incident, and then with the break-glass role and a Slack note.
- Terraform owns everything in AWS. A resource created in the console is a bug; the weekly drift check (`terraform plan -detailed-exitcode` in `nightly.yml`) posts any drift to Slack.
- Vendor-side configuration that has a Terraform provider (Vercel project, Sentry project, Better Stack monitors, Cloudflare DNS) is also in Terraform under `modules/vendors/`. Vendor settings without a provider (Inngest, LiveKit, Langfuse, the voice vendors' retention switches) are listed in `infra/MANUAL.md` with the setting, the value, who set it and the date, and the privacy verify job checks the ones it can read through an API.

## 4. Secrets

Secrets are in **AWS Secrets Manager**, one secret per environment per service (`forone/prod/api`, `forone/prod/workflows`, `forone/prod/call-worker`), injected into ECS task definitions by ARN. Vercel holds only the `NEXT_PUBLIC_*` values, which are not secrets. GitHub Actions holds no vendor key at all; it assumes the deploy role through OIDC and the tasks fetch their own secrets at start.

- No secret is ever in the repo, an image, a Terraform variable file, a Slack message, a PR comment or a `.env` outside `dev`. `gitleaks` runs in CI and as a pre-commit hook; a hit blocks the merge and the key is rotated the same day whether or not it reached `main`.
- Rotation: vendor keys quarterly and on any suspected exposure, by creating the new key in the vendor console, updating the secret, and restarting the service (`tools/release restart <service>`); `INTERNAL_JWT_SIGNING_KEY` and `SESSION_SECRET` support two active values for a 24-hour overlap. `RESEARCH_PSEUDONYM_SECRET` is never rotated (rotation would re-identify nobody but would break the research set's joins).
- Each engineer has their **own** vendor keys for laptop work, created under the shared vendor org with a spend cap (handbook 07) and named `dev-<name>`. The prod keys are read by nobody; they are created by Muath or the infra engineer in the vendor console and pasted once into Secrets Manager.
- Access to Secrets Manager values in prod: the task roles, and the break-glass role (MFA, CloudTrail, Slack alert). Reading a prod secret is an audited act and needs a reason in Slack, like reading learner audio.

## 5. Deploying

**Staging** deploys on every merge to `main` (`deploy-staging.yml`): build the image once, push to ECR tagged with the git SHA, run `alembic upgrade head` as a one-off ECS task, roll `api` and `workflows` (minimum healthy 100%), drain-then-replace `call-worker` (section 7), deploy `web` through Vercel's Git integration from the same commit, then run the smoke test: one `POST /v1/sample`, one scripted call through `tools/call-bench --n 1`. A failed smoke test marks the deploy red in Slack and leaves staging as is; the fix is a new merge.

**Prod** deploys from a tag (`deploy-prod.yml`):

1. `tools/release cut` on `main` creates `vYYYY.MM.DD-N`, writes the `release_manifest` row (image digest, versions snapshot from `versions.yaml`, flags snapshot, the `eval_runs` ids that covered the diff since the last tag) and posts the manifest diff to Slack.
2. The workflow pauses on a GitHub environment approval. One named approver (Muath or the other engineer, never the person who cut the tag when there are two engineers) approves inside the release window.
3. Migrations, rolling deploy of `api` and `workflows`, drain-then-replace of `call-worker` (refused automatically inside any learner's call window; override with a reason).
4. `ops/canary`: one `episode/produce` and one scripted call for the synthetic prod learner through the primary voice vendor. A failed canary rolls back automatically to the previous task definition revision and pages P2.
5. The deploy is announced in `#forone-ops` with the manifest diff and the canary result.

**Release window:** Sunday to Thursday, 10:00 to 16:00 Riyadh. Never while a P1 is firing. Never within 30 minutes before any learner's drop when the diff touches `episode/produce` or `day/next`. **Freezes:** 2026-12-05 12:00 to 2026-12-08 12:00 Riyadh (launch) and 2026-12-31 to 2027-01-02 (the Gemini price change and the first finales). A hotfix during a freeze needs Muath's explicit yes in Slack and ships as a tag like any other.

**Rollback** is `tools/release rollback`: redeploy the previous tag's image. The database only rolls forward (section 6), and a prompt version rolls back by reverting its PR and cutting a new tag, because versions are files.

## 6. Migrations

Alembic, one revision per PR at most, **expand then contract**: a column or table is added in one release, written to in the same or a later one, and an old column is dropped at least one release after nothing reads it. `make migrate-check` fails a revision that drops or renames anything unless the PR carries the label `contract-migration` and a link to the expand PR. Every revision has a working `downgrade`, exercised in CI on a fresh database, even though prod never runs it; it is the proof the author understood the change.

Row-level security policies are part of migrations and the RLS walk test (handbook 05 §3) runs on every PR.

## 7. The call worker is special

A deploy must never cut a call. `tools/release drain-replace call-worker` sets the running tasks to drain (the worker stops accepting dispatches, finishes its calls, exits), starts the new tasks, waits for the old ones to reach zero calls or 15 minutes, then stops them. The job is refused between 05:00 and 08:30 Riyadh and inside any learner's chosen call slot unless `--force` is passed with a reason, which goes to the audit log.

Autoscaling: CPU-based with scale-in protection while a task has an active call; the image is about 1.6 GB and pulls from ECR in the same region in 20 to 40 seconds, inside the cold-start allowance.

## 8. Domains and DNS

The brand domain is still open (architecture 01 §10 #13); the handbook writes `<domain>`. When it is chosen: `app.<domain>` (web), `api.<domain>` (ALB), `staging.<domain>`, `s.<domain>` (sample share links). DNS is in Cloudflare (Terraform-managed), which also provides Turnstile; Cloudflare's proxy is **off** for `api.` so the WAF on the ALB sees real client addresses and so no second processor sits in front of learner audio. The cookie domain, the VAPID subject and the email sender all derive from the one Terraform variable.

## 9. Access to environments

| Who | Staging | Prod |
|---|---|---|
| Engineer | AWS console (MFA), `forone_readonly` SQL through SSM port forwarding, ECS exec, staff account `engineer` | AWS console read-only (MFA), ECS exec **off**, `forone_readonly` SQL under pgaudit through SSM with a Slack note, staff account `engineer`, break-glass role for incidents only |
| Muath | everything | everything, as `owner`, every content read logged and visible to the learner in their export |
| Reviewer, tagger | `/admin/review` or `/admin/research` on staging for training | the same pages on prod, nothing else |
| CI | OIDC deploy role scoped to ECR push, ECS update, the migration task, Terraform apply | the same, plus the environment approval gate |

No long-lived AWS access keys exist for humans or CI. If one is created for a vendor integration that cannot use a role, it is listed in `infra/MANUAL.md` with its purpose and rotated quarterly.

## 10. Monthly fixed cost to expect

From architecture 01 §10 #4: about $800 to $1,100 a month with staging, $700 to $850 for prod alone, before vendor minimums (voice winner's paid tier, LiveKit Ship, Vercel Pro, Langfuse Core, Better Stack). Multi-AZ RDS is about $120 of that. The cost dashboard (handbook 06) shows fixed cost as its own line so the per-session number is never flattered by it.
