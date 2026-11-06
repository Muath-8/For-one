# 04. CI and CD

Part of the For one engineering handbook. Written 2026-11-06 against architecture 01 §4.8 and 09 §4.3 and D9. The starter workflow is `engineering/starter-files/ci.yml`.

## 1. Principles

1. **Green on day one.** CI exists before the first feature. An empty repo with a passing pipeline is the first commit of week 1.
2. **Every check is reproducible on a laptop.** `make lint`, `make test`, `make test-int`, `make eval SUITE=x` run the same commands CI runs. CI has no magic.
3. **Prompts are code.** A change to anything a model reads goes through the same pipeline as a code change, plus the eval gate.
4. **Fast by default, expensive by diff.** The cheap jobs run on every PR in under eight minutes. The jobs that cost money (eval suites, staging calls) run only when the diff touches what they test, and print their cost in the job summary.
5. **Nothing deploys to prod without a human name on it.** One approval, in the release window, on a tag.

## 2. Pipelines

| Workflow | Trigger | Jobs | Time |
|---|---|---|---|
| `ci.yml` | every PR, every push to `main` | `python`, `web`, `package`, `secrets`, `infra-plan` (if `infra/` changed), `eval-gate` (if versioned paths changed), `image` (main only) | 6 to 10 min; eval-gate adds 2 to 15 |
| `deploy-staging.yml` | push to `main`, after `ci.yml` is green | migrate, roll services, drain-replace worker, smoke test, Slack | 8 to 12 min |
| `deploy-prod.yml` | tag `v*` | manifest check, **approval**, migrate, roll, drain-replace (window-checked), canary, Slack; auto-rollback on canary failure | 15 to 25 min |
| `nightly.yml` | 02:00 Riyadh, Sunday to Thursday | staging up, full eval smoke (`writer`, `editor`, `host` replay half, `analyst`, `notes`, `memory`, `recognizers`), `calls_50` weekly on Wednesday, Terraform drift check, dependency audit, staging down | 40 to 60 min |

## 3. Checks on every PR

**`python`**

- `uv sync --frozen` (the lockfile is the truth; an unlocked dependency fails).
- `ruff check` and `ruff format --check`, including the custom rules: `banned-api` for `resend` and `pywebpush` outside `forone.core.messaging`, for `os.environ` outside `forone.core.settings`, for `boto3` outside `forone.core.media` and `forone.core.keys`, and for any `hume` import.
- `pyright` strict on `packages/core`, `adapters`, `learner`, `assess`; standard elsewhere until week 4.
- `import-linter` contracts for the package layering (handbook 01 §3).
- `pytest` unit with `FORONE_FAKE_VENDORS=1`: every package, under 90 seconds, coverage reported but not gated (a coverage gate on a five-week build produces tests of the wrong things).
- `pytest -m integration` against services started with docker compose in the runner: the RLS policy walk (every learner-scoped table, every role, a cross-learner read must return zero rows), migrations up and down on a fresh database, the Inngest payload test (no event model has a field named `text`, `quote`, `transcript`, `audio`), the messaging enum test (exactly eight kinds, three senders), the PII scrub corpus (zero leaks over `eval/fixtures/pii_corpus.jsonl`), the language-literal grep (handbook 01 §4).

**`web`**

- `pnpm install --frozen-lockfile`, `tsc --noEmit`, `eslint` including the law-furniture rule (no component may render a streak, points, level or "next episode" control; the rule matches a list of banned prop and class names and is reviewed by Muath when extended), `next build`, Playwright smoke on the built app against a mocked API (ten flows: open, Salma, word check, Today, play, call screen, after, notebook, controls, plans).

**`package`**

- Validates every language package: bibles present, every character has a voice for both wired vendors, crisis resources and keywords present, consent texts present in every `ui_strings` file with matching version ids, `ban_list.yaml` schema, every prompt file's frontmatter declares every slot its body uses, `versions.yaml` lists every file under `prompts/` and `rules/`.
- Validates `vendors.yaml` against its schema (no `hume`; writer and editor never resolve to the same vendor without a `note`; every `pinned_until` role has an empty fallback) and `prices.yaml` (every role's model has a dated price row; a row older than 120 days warns).
- Reads `docs/ropa.md` and fails if `vendors.yaml` names a vendor whose register row is not `dpa: signed` or `dpa: clickwrap-accepted`.

**`secrets`**

- `gitleaks` over the diff and, weekly, the whole history. A hit fails the job and posts to `#forone-ops`; rotation the same day is a rule (handbook 03 §4).

**`infra-plan`** (only when `infra/` changed)

- `terraform fmt -check`, `terraform validate`, `terraform plan` for staging and prod through the OIDC role (read-only plan permissions), plan posted as a PR comment, `tfsec` or `checkov` for the obvious mistakes (public bucket, open security group, unencrypted anything).

**`eval-gate`** (only when a versioned path changed; a required check on `main`)

The path-to-suite map lives in `eval/suites.yaml` under `ci_triggers` and mirrors architecture 09 §4.3. The job:

1. Computes which suites the diff requires; prints the estimated cost and minutes to the job summary before running.
2. Refuses outright if `versions.yaml` bumps `rater` while `pinned_until` is in the future, or if a prompt file changed without its version bump (and the reverse).
3. Runs the suites with `tools/eval run --suite <name> --baseline eval/baselines/<name>.json`. Suites marked `staging` (`host`, `calls_50`) claim the staging lock, start staging if stopped, and release it after.
4. Compares every metric with `thresholds.yaml`: a floor or ceiling breach fails; a regression beyond `max_regression` against the baseline fails; everything else is reported as a table in the PR comment with the deltas.
5. On pass, the run's id is attached to the PR as a check output so `tools/release cut` can record it in the manifest. The baseline is updated only by merging (a post-merge step copies the run to `eval/baselines/` on `main`).

Cost ceiling: a single PR's eval-gate may not exceed $25 without the label `eval-expensive` and a reviewer's approval of the cost in the PR. The nightly covers the rest.

**`image`** (`main` only)

- Builds `forone-python` once with BuildKit cache, bakes ffmpeg, the spaCy model and the turn-detector and Silero weights (fetched from the fixtures bucket, not from the internet at build time, so builds are reproducible), scans with Trivy (critical CVEs fail), pushes to ECR tagged with the SHA, and records the digest.

## 4. Preview deploys

`web` gets a Vercel preview per PR automatically, pointed at **staging** `api`. The preview URL is posted on the PR. Previews use the staging staff accounts; a preview is never pointed at prod and the `NEXT_PUBLIC_API_URL` for previews is fixed in the Vercel project, not per PR.

The backend has no preview environments (architecture 01 D14). A PR that needs a running backend to be judged is deployed to staging by its author with `tools/release staging deploy <sha>` after claiming the staging lock; the lock is released when the review is done and `main` is redeployed. This happens rarely if the fakes and the suites are good; if it happens daily, the fakes are the thing to improve.

## 5. Branch protection on `main`

- Pull request required; no direct pushes, including by Muath.
- Required checks: `python`, `web`, `package`, `secrets`, and `eval-gate` and `infra-plan` when they ran.
- One approving review from someone other than the author. With one engineer, Muath is the reviewer for prompt and infra changes and the engineer self-merges pure code changes after CI, with the PR left open for an hour for a second look. That exception ends the day a second engineer starts.
- Linear history (squash merge). The squash commit message is the PR title plus the PR body's "Why" section.
- `CODEOWNERS` (starter file) routes prompt, rule, consent, infra and data-handling paths to the named reviewers.

## 6. Nightly

The nightly exists because the eval-gate runs only what the diff touched, and drift arrives from the vendors' side: a model update, a voice change, a quota change. The nightly runs the cheap suites in full, `calls_50` once a week, the Terraform drift check, `pip-audit` and `pnpm audit`, the vendor health probes with their current quotas, and the cassette staleness check (cassettes older than the prompt version they were recorded under are listed). Results go to `#forone-ops` as one message with a link to the run. A nightly failure is a Tuesday item, not a page, unless it is `calls_50` failing a latency gate two weeks running.

## 7. Release process, step by step

1. **Decide the release.** On a release day the on-call engineer looks at `main` since the last tag, the open P1 and P2 alerts, and the window. If any P1 is firing, no release.
2. **Cut.** `tools/release cut` creates the tag, writes `release_manifest`, posts the diff (code, prompt versions, flags, migrations, eval runs) to Slack.
3. **Approve.** The approver reads the manifest, checks that every prompt version change in it has an eval run id, and approves in the GitHub environment. The approver is never the person who cut the tag when there are two people.
4. **Deploy.** The workflow runs the steps in handbook 03 §5. The engineer watches `#forone-ops` and `/admin/alerts` for 30 minutes after the canary passes.
5. **Record.** The manifest row gets `deployed_at`, `approved_by`, `canary_passed`. A rollback writes `rolled_back_at` and a note.
6. **Tell nobody outside the team.** There is no learner-facing changelog; the product's only on-air announcement is the voice-change line (PRD 7.1).

## 8. What CI never does

- Call a real vendor on a PR that did not change a versioned path.
- Touch prod data, read a prod secret, or run against prod from any job but `deploy-prod.yml`.
- Skip, disable or quarantine a failing test to get green. A test that is wrong is fixed or deleted in a PR that says so.
- Push an empty commit or re-run a job to make a flaky test pass. A flaky test is a bug with its own ticket; three flakes in a week and it is fixed or deleted.
