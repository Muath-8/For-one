# ADR-0006 — Drizzle ORM over Prisma and supabase-js

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §3, `05-tdd.md` §2, §12.2

## Context

The data layer has to satisfy four requirements that jointly narrow the field:

1. **Postgres-native features are load-bearing.** pgvector similarity search with a `user_id` pre-filter, row-level security on every user-owned table, partial and expression indexes, `CONCURRENTLY`-built indexes, and append-only tables with database-level constraints. The data layer must not stand between us and Postgres.
2. **Three runtimes, two connection models.** Vercel functions and Trigger.dev tasks are short-lived and must use the Supavisor transaction pooler; the voice agent is a long-lived process. Both need small, predictable connection footprints and a cold start measured in milliseconds.
3. **Table ownership is architectural.** ADR-0004 puts each table's definition inside its owning module. The schema must be expressible as ordinary TypeScript files distributed across the tree, not as one central artifact.
4. **Migrations must be forward-only and reviewable.** `00` §11 requires expand-and-contract with a CI check that blocks destructive statements outside labelled contract migrations, which means migrations must be plain SQL files we can grep.

## Decision

**Drizzle ORM with drizzle-kit SQL migrations.** Table definitions live in `src/modules/<module>/schema.ts` and are re-exported from `src/platform/db/schema.ts` for drizzle-kit. The driver is postgres.js with `prepare: false` against the Supavisor transaction pooler for the app and tasks, and a session-mode pool capped at 5 for the agent. `DIRECT_DATABASE_URL` on port 5432 is used only by drizzle-kit.

Raw SQL through `sql\`\`` is a first-class, expected tool for pgvector queries and anything the query builder expresses awkwardly. Repository functions in `repo.ts` are the only place either appears.

## Alternatives considered

**Prisma.** Lost on three concrete points, not on taste. Its schema lives in one `schema.prisma` file, which directly contradicts per-module table ownership and would make the boundary rule unenforceable for the most important artifact in the system. pgvector support requires preview features and raw queries anyway, so the abstraction leaks exactly where we need it most. And the generated query engine adds cold-start weight and a binary to every serverless invocation, in a system where the app is deployed as functions.

**supabase-js as the primary data layer.** Lost on scope mismatch. It is a PostgREST client: excellent for RLS-scoped browser access, which ADR-0012 forbids, and weak for the server-side work we actually do — multi-statement transactions, complex joins for retrieval and assessment, and typed migrations. It is retained for exactly what it is good at: Storage operations and signed-URL minting in `src/platform/storage`.

**Kysely.** Genuinely close. It has the same "thin over SQL" philosophy and better-typed joins. It lost because drizzle-kit's migration generation and drift detection are integral, whereas Kysely delegates migrations to a separate tool. Given that migration discipline is a named CI gate, having schema, migration generation, and drift check in one tool is worth more than marginally better join typing.

**Raw SQL with no query layer.** Lost because repository-layer `userId` scoping is a security control (`00` §4). A typed schema makes "every user-owned table read is scoped" mechanically checkable; hand-written SQL strings make it a review promise.

## Consequences

- Table ownership is physical. Moving a table between modules is a file move that the boundary lint rule immediately reasons about.
- Migrations are plain SQL in `drizzle/`, so `scripts/check-migrations.ts` can grep for `DROP COLUMN`, `DROP TABLE`, type alterations, and `NOT NULL` additions without a default, and fail CI outside labelled contract migrations.
- `prepare: false` is mandatory under transaction-mode pooling. Forgetting it produces intermittent prepared-statement errors under load rather than an immediate failure, so it is set once in `src/platform/db/client.ts` and never per-call.
- Less runtime safety than Prisma's generated client: Drizzle will let a badly shaped raw query through. Mitigated by keeping raw SQL confined to `repo.ts` files and covering every repository function with integration tests against a real Postgres 16 container.
- RLS policies are written by hand in migrations rather than derived from the schema. `05-tdd.md` §11.2 and 08's per-resource "A cannot read B" tests are the check that they are correct.
- pgvector, HNSW indexes, partial indexes, and `CREATE INDEX CONCURRENTLY` are all directly available, because nothing is translating our intent.
