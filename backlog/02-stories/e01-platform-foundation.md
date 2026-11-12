# E01 · Platform foundation and the agent's workflow

*Stories for the shared infrastructure. Architecture domain 01 (system topology) and 09 (operations). In every story file, `Phase` is the release-plan phase a v1 story is built in (phases follow dependency order; there are no dates, ADR-25.1), and `Release` is v1 (needed at launch) or v1.1 (after launch). Sizes S, M and L are relative complexity only (ADR-25.2).*

### E01-S01 · Monorepo with CI and local compose
**As an** operator, **I want** one repository with `api`, `web`, `call-worker` and `tools` packages, CI on every push and a docker compose for local work, **so that** the coding agent, CI and Muath all work from the same checkout.
- **Given** a fresh clone, **when** `docker compose up` runs, **then** Postgres, the api and the web shell start and the health route answers 200.
- **Given** a push to any branch, **when** CI runs, **then** lint, type checks and unit tests run for Python and TypeScript and a failure blocks merge.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology · Depends on: none
- Requirements: enabling (no FR)

### E01-S02 · Core settings, database and migrations
**As the** coding agent, **I want** `forone.core` with typed settings, a Postgres connection, Alembic migrations and the three database roles (`forone_app`, `forone_workflows`, `forone_purge`), **so that** every service reads configuration and the schema the same way.
- **Given** an empty database, **when** `alembic upgrade head` runs, **then** every table in the architecture's data design exists with row-level security enabled on learner-keyed tables.
- **Given** the `forone_app` role, **when** it tries to delete from `events`, **then** the database refuses.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology · Depends on: E01-S01
- Requirements: FR-601, FR-1321, NFR-303

### E01-S03 · API skeleton with OpenAPI codegen
**As the** coding agent, **I want** a FastAPI `api` service with versioned routes under `/v1`, request ids, and an OpenAPI schema the web client generates types from, **so that** client and server never disagree on a payload.
- **Given** a route is added to `api`, **when** CI runs, **then** the generated TypeScript client is regenerated and a stale client fails the build.
- Size: S · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology · Depends on: E01-S02
- Requirements: enabling (no FR)

### E01-S04 · Durable workflows on Inngest
**As the** coding agent, **I want** Inngest wired with a hello function, event-driven triggers and retries, **so that** every multi-step job (produce an episode, after-session pass, deletion) is durable and resumable.
- **Given** a function step throws, **when** Inngest retries, **then** completed steps are not re-run and the failure is visible in the Inngest dashboard with the learner id tokenized.
- Size: S · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology · Depends on: E01-S02
- Requirements: FR-1325, NFR-204

### E01-S05 · Staging infrastructure as code
**As an** operator, **I want** Terraform for staging in `eu-central-1` (VPC with NAT and endpoints, RDS Postgres 16 Multi-AZ-ready with pgvector, S3 with KMS, ECR, ECS Fargate, ALB with WAF, Secrets Manager) written as a module production reuses, **so that** production is the same code applied twice. Terraform stays (ADR-24.B19); a console setup with a written runbook is only the fallback if Terraform is not applying by the end of build week 1.
- **Given** `terraform apply` on staging, **when** it completes, **then** the api answers on the staging hostname over TLS and the call-worker task definition exists.
- **Given** the home region (`eu-central-1`, final for v1 by ADR-24.8 and ADR-25.3), **when** the module is written, **then** the region is a single variable and nothing else in the module names it, so any later move is one variable.
- Size: L · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology · Depends on: E01-S01
- Requirements: NFR-301, NFR-307

### E01-S06 · Error tracking and tracing wired
**As an** operator, **I want** Sentry in every service and Langfuse wired for model calls under the agreed retention, **so that** a failure is seen with context and no learner text leaks into a third party unscrubbed.
- **Given** an exception in `api`, `web` or `call-worker`, **when** it is raised, **then** it appears in Sentry with the learner id tokenized and no transcript text.
- **Given** a test user in Langfuse, **when** per-user deletion is called, **then** every trace for that user is gone within the documented window (verified once in Phase 1).
- Size: S · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology · Depends on: E01-S03
- Requirements: NFR-306

### E01-S07 · Staging deploy pipeline and canary episode
**As an** operator, **I want** a merge to `main` to deploy to staging and run a canary episode for a synthetic learner, **so that** a broken build is known within minutes.
- **Given** a merge to `main`, **when** the pipeline finishes, **then** staging runs the new build and the canary produces one episode end to end or pages.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 01 System topology · Depends on: E01-S05, E04-S03
- Requirements: enabling (no FR)

### E01-S08 · Media storage, per-learner keys and the media route
**As a** learner, **I want** my audio stored under a key that is mine alone and served only to me, **so that** nobody else can read my episodes or my voice.
- **Given** an episode is published, **when** its segments are written to S3, **then** each object is encrypted with a per-learner data key (SSE-C) derived under KMS and the bucket policy denies unencrypted writes.
- **Given** a signed media request from another learner's session, **when** it hits the media route, **then** it is refused with 403 and audited.
- **Given** the drop minute for 50 learners, **when** a load test runs, **then** p95 first byte for a segment is under 500 ms.
- Size: L · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 01 System topology, 07 Security · Depends on: E01-S05, E13-S01
- Requirements: FR-1050, NFR-105, NFR-301, NFR-302

### E01-S09 · Production stood up and restored once
**As an** operator, **I want** production applied from the same Terraform in Multi-AZ, with a documented restore drill from backup, **so that** launch runs on an environment we have already brought back from the dead.
- **Given** production exists, **when** the restore drill runs before the open, **then** a full point-in-time restore into staging completes within 4 hours and the privacy checks pass on the restored copy; the drill repeats once a quarter.
- **Given** the database, **when** backups are configured, **then** they are automated, kept 30 days with point-in-time recovery at a recovery point of 5 minutes or better, and never scrubbed: deletion relies on their 30-day expiry (NFR-207, FR-1047).
- **Given** the pre-launch freeze (the two working days before launch), **when** anything is deployed inside it, **then** it is a hotfix Muath approves, recorded in the release manifest.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 01 System topology · Depends on: E01-S05, E15-S05
- Requirements: NFR-207, NFR-307

### E01-S10 · How the coding agent builds and Muath approves
**As** Muath, **I want** the repository to carry the agent's working rules, every story's acceptance criteria written as failing tests before the code, an independent AI review of every change in CI, and my approval on the changes that matter, **so that** an AI coding agent can build For one safely under one person (ADR-25.2).
- **Given** the repository, **when** the agent starts a session, **then** it reads one instructions file (`AGENTS.md`) that states the twelve laws, the story format, the tests-first rule, the approval gates, and what it must never do (call a vendor SDK outside an adapter, read production learner data, commit a secret, deploy to production, edit a migration that has run).
- **Given** a story, **when** the agent works on it, **then** a first commit adds the acceptance criteria as tests that fail, a later commit makes them pass, and CI checks that the order holds; a story whose tests were written after its code is sent back.
- **Given** a pull request, **when** CI runs, **then** lint, types, tests, the mapped eval suites, dependency scanning and secret scanning pass, and a second AI reviewer that did not write the change (a separate session with only the diff, the story and the laws) posts findings; a blocking finding fails the check. A change that touches auth, keys, media URLs, the feed or deletion also gets an AI security review (the `/security-review` pass), and its blocking findings fail the check too (ADR-25.11).
- **Given** a merge to `main`, a database migration, a prompt or bible change, or a production deploy, **when** it is ready, **then** it waits for Muath's approval (protected branch, required reviewer, a deploy environment with an approver); the agent cannot approve its own change.
- **Given** an alert, **when** Muath asks, **then** the agent runs the matching runbook as a script that logs every step it took; no runbook runs on its own except the automated fallbacks.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 01 System topology, 09 Operations · Depends on: E01-S01
- Requirements: NFR-501
