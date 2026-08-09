# ADR-0001 — Data export and account deletion restored to v1

**Status:** Accepted (user-ratified 2026-08-08)

## Context

The Product Concept's Trust Contract promises: "The data is theirs — see it, export it, delete it. Instantly, completely, no friction." Source PRD v2.0 Part 12.8 quietly removed export and full deletion from v1 ("reduced to verification-only after removal of export/deletion"), and the adopted design document consequently declined to design those surfaces, flagging the omission as "a known gap against the Product Concept's broader trust promise." The contradiction had to be resolved before any spec could be final: a product that asks for voice recordings, insecurities, and life details cannot ship with a trust story its own concept document calls incomplete — and GDPR/CCPA-class regimes make access, portability, and erasure legal obligations, not features.

## Decision

Full data export and full account deletion are v1 features:

- **Export:** user-initiated from "Your show → Account essentials"; asynchronous job produces a ZIP (structured JSON + stored media the user is entitled to); delivered via signed URL with 7-day expiry; in-app banner plus one transactional email on readiness.
- **Deletion:** type-to-confirm; immediate sign-out and Clerk user deletion; all rows, storage objects, embeddings, and PostHog data purged ≤ 24 h; backups age out ≤ 30 days under a deletion-on-restore policy; one confirmation email.
- Transactional email scope widens accordingly: verification, password reset, export-ready, deletion confirmation. Re-engagement email remains banned forever.

## Alternatives considered

1. **Keep PRD v2.0 as written (no export/deletion).** Rejected: violates the Trust Contract, is legally untenable in target markets, and the concept document itself treats the trust promises as load-bearing differentiation.
2. **Deletion only, export deferred.** Rejected: portability is the cheaper half to build (a job that serializes rows the schema already isolates per user) and the halves reinforce each other's credibility.

## Consequences

- 02-ux-spec designs SCR-25/26/27 (Account essentials, export, deletion) and supersedes the design doc's "Unsupported data actions" text.
- 06-data-api-spec carries `export_jobs` and `deletion_jobs` entities and endpoints; every table's ON DELETE behavior must support complete cascade.
- 05-tdd designs JOB-export-user-data and JOB-delete-account including third-party propagation (Clerk, PostHog, Supabase Storage).
- Deletion completeness becomes a release-gate test in 08 (traced end-to-end, verified empty).
