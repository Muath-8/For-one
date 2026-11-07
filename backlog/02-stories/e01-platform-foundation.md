# E01 · Platform foundation

*Stories for the shared infrastructure. Architecture domain 01 (system topology) and 09 (operations). Weeks are beta build weeks: W1 = 18 to 24 Nov, W2 = 25 Nov to 1 Dec, W3 = 2 to 8 Dec, W4 = 9 to 15 Dec, W5 = 16 to 22 Dec, Beta = 23 Dec to 26 Jan.*

### E01-S01 · Monorepo with CI and local compose
**As an** operator, **I want** one repository with `api`, `web`, `call-worker` and `tools` packages, CI on every push and a docker compose for local work, **so that** every engineer starts from the same checkout on day one.
- **Given** a fresh clone, **when** `docker compose up` runs, **then** Postgres, the api and the web shell start and the health route answers 200.
- **Given** a push to any branch, **when** CI runs, **then** lint, type checks and unit tests run for Python and TypeScript and a failure blocks merge.
- Size: M · Priority: P0 · Week: W1 · Domain: 01 System topology · Depends on: none

### E01-S02 · Core settings, database and migrations
**As an** engineer, **I want** `forone.core` with typed settings, a Postgres connection, Alembic migrations and the three database roles (`forone_app`, `forone_workflows`, `forone_purge`), **so that** every service reads configuration and the schema the same way.
- **Given** an empty database, **when** `alembic upgrade head` runs, **then** every table in the architecture's data design exists with row-level security enabled on learner-keyed tables.
- **Given** the `forone_app` role, **when** it tries to delete from `events`, **then** the database refuses.
- Size: M · Priority: P0 · Week: W1 · Domain: 01 System topology · Depends on: E01-S01

### E01-S03 · API skeleton with OpenAPI codegen
**As an** engineer, **I want** a FastAPI `api` service with versioned routes under `/v1`, request ids, and an OpenAPI schema the web client generates types from, **so that** client and server never disagree on a payload.
- **Given** a route is added to `api`, **when** CI runs, **then** the generated TypeScript client is regenerated and a stale client fails the build.
- Size: S · Priority: P0 · Week: W1 · Domain: 01 System topology · Depends on: E01-S02

### E01-S04 · Durable workflows on Inngest
**As an** engineer, **I want** Inngest wired with a hello function, event-driven triggers and retries, **so that** every multi-step job (produce an episode, after-session pass, deletion) is durable and resumable.
- **Given** a function step throws, **when** Inngest retries, **then** completed steps are not re-run and the failure is visible in the Inngest dashboard with the learner id tokenized.
- Size: S · Priority: P0 · Week: W1 · Domain: 01 System topology · Depends on: E01-S02

### E01-S05 · Staging infrastructure as code
**As an** operator, **I want** Terraform for staging (VPC with NAT and endpoints, RDS Postgres 16 Multi-AZ-ready with pgvector, S3 with KMS, ECR, ECS Fargate, ALB with WAF, Secrets Manager) written as a module production reuses, **so that** production is the same code applied twice.
- **Given** `terraform apply` on staging, **when** it completes, **then** the api answers on the staging hostname over TLS and the call-worker task definition exists.
- **Given** the home region is not yet confirmed by counsel, **when** staging is created, **then** the region is a single variable and nothing else in the module names it.
- Size: L · Priority: P0 · Week: W1 · Domain: 01 System topology · Depends on: E01-S01; legal view on region (blocking item B4) for production only

### E01-S06 · Error tracking and tracing wired
**As an** operator, **I want** Sentry in every service and Langfuse wired for model calls under the agreed retention, **so that** a failure is seen with context and no learner text leaks into a third party unscrubbed.
- **Given** an exception in `api`, `web` or `call-worker`, **when** it is raised, **then** it appears in Sentry with the learner id tokenized and no transcript text.
- **Given** a test user in Langfuse, **when** per-user deletion is called, **then** every trace for that user is gone within the documented window (verified once in W1).
- Size: S · Priority: P0 · Week: W1 · Domain: 01 System topology · Depends on: E01-S03

### E01-S07 · Staging deploy pipeline and canary episode
**As an** operator, **I want** a merge to `main` to deploy to staging and run a canary episode for a synthetic learner, **so that** a broken build is known within minutes.
- **Given** a merge to `main`, **when** the pipeline finishes, **then** staging runs the new build and the canary produces one episode end to end or pages.
- Size: M · Priority: P0 · Week: W2 · Domain: 01 System topology · Depends on: E01-S05, E04-S03

### E01-S08 · Media storage, per-learner keys and the media route
**As a** learner, **I want** my audio stored under a key that is mine alone and served only to me, **so that** nobody else can read my episodes or my voice.
- **Given** an episode is published, **when** its segments are written to S3, **then** each object is encrypted with a per-learner data key (SSE-C) derived under KMS and the bucket policy denies unencrypted writes.
- **Given** a signed media request from another learner's session, **when** it hits the media route, **then** it is refused with 403 and audited.
- **Given** the drop minute for 50 learners, **when** a load test runs, **then** p95 first byte for a segment is under 500 ms.
- Size: L · Priority: P0 · Week: W2 · Domain: 01 System topology, 07 Security · Depends on: E01-S05, E13-S01

### E01-S09 · Production stood up and restored once
**As an** operator, **I want** production applied from the same Terraform in Multi-AZ, with a documented restore drill from backup, **so that** the beta runs on an environment we have already brought back from the dead.
- **Given** production exists, **when** the restore drill runs on a copy, **then** a point-in-time restore completes and the privacy checks pass on the restored copy.
- **Given** the freeze on 19 December 12:00, **when** anything is deployed after it, **then** it is a hotfix with a named approver in the release manifest.
- Size: M · Priority: P0 · Week: W5 · Domain: 01 System topology · Depends on: E01-S05, E15-S05
