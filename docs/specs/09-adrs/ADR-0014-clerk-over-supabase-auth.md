# ADR-0014 — Clerk over Supabase Auth

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §3, `05-tdd.md` §4

## Context

Requirements from PRD 1.3 and 2.1: email and password plus Google and Apple OAuth; a self-declared birth date age gate at account creation; **email verification required before session 2, not before session 1** — nothing blocks the first episode; and account deletion in v1 (ADR-0001).

Supabase Auth is the default companion to Supabase Postgres and is free with the database. Its natural pattern, however, is to be the authorization boundary for direct browser-to-database access through RLS — a pattern ADR-0012 rejects outright. That removes most of the integration advantage before the comparison starts.

Two requirements then do the discriminating work. The verification rule is unusual: the first session must proceed with an unverified email, and the second must not. That means verification state has to be a *readable attribute* the application gates on at one specific point, not a precondition for having a session at all. And the age gate has a rejection path that must leave no account behind, which means account deletion has to be callable from our own code at signup time.

The team is small, and every hour spent on password reset flows, OAuth callback edge cases, session revocation, and Apple's Sign in with Apple requirements is an hour not spent on the product.

## Decision

**Clerk is the identity provider.** `@clerk/nextjs` 6.x, with `clerkMiddleware()` on every non-static path and `auth()` inside the route-handler wrapper. Postgres stores no credentials; `users.clerk_user_id` is the external key and `users.id` is ours.

Three integration points are specified precisely:

1. **Verification gates and delivery.** A custom session-token claim `evf` carries the primary email's verification status as a boolean. `POST /api/v1/sessions` enforces the session-two rule: one or more prior sessions plus `evf !== true` returns the status and `EMAIL_VERIFICATION_REQUIRED` mapping owned by 06. The export endpoint separately enforces the adopted verified-email export interaction in 02; that gate does not change session-one eligibility. Reading the claim from the JWT means no Clerk API round trip on either gated request path. EP-58 is the sole resend mutation: it resolves the primary email from the verified Clerk subject and asks Clerk to send its provider-owned single-use link, valid for exactly 24 hours, to the fixed allowlisted `/verify-email` redirect under the 06-owned rate limit. The product accepts no address, redirect, or token, stores no verification secret, and never redeems a link itself. Clerk's verification page consumes the token, rejects expired or cross-subject attempts without disclosing an address, treats a used link as already verified, and refreshes the session claim before a blocked product action is retried.
2. **Age gate.** Birth date and the two language choices are collected by us after Clerk sign-up and posted to canonical `EP-05`, `POST /api/v1/onboarding/profile`. A provisional `users` row may already exist from identity synchronization, so its profile fields are nullable until EP-05 completes. EP-05 authenticates the verified Clerk subject even when no product row exists and performs an idempotent scoped upsert. Under 18 returns the exact 06-owned `UNDER_AGE` mapping, commits no birth date or profile tuple, removes any provisional product row, and writes the 06-owned deletion receipt before asynchronous Clerk deletion. That durable receipt blocks middleware and identity sync from recreating or admitting the subject until provider absence is confirmed; over 18 atomically completes the profile fields. Replay, recovery, and same-attempt lockout behavior are owned by EP-05 and the existing account-deletion job.
3. **Sync.** `POST /api/webhooks/clerk` is svix-verified against `CLERK_WEBHOOK_SIGNING_SECRET`, deduplicated through the 06-owned `wh:clerk:{svix-id}` record for seven days, and enqueues `JOB-identity-sync`. The handler performs no database work inline and returns within 200 ms. The job and EP-05 use the same idempotent provisional-row upsert, so webhook/profile arrival order cannot create two users or overwrite a completed profile.

## Alternatives considered

**Supabase Auth.** The obvious default, and it lost on three points. Its principal advantage — being the RLS authorization boundary for direct browser database access — is worth nothing under ADR-0012. Its verification model is oriented toward blocking sign-in until confirmed, whereas we need session 1 to proceed and session 2 to be gated, which means building the readable-attribute gate ourselves. And its OAuth, session management, and account-recovery surface would need meaningfully more of our own code for Google and Apple than Clerk's managed flows.

**Auth.js (NextAuth).** Lost on operational load. It is a library, not a service: we would own the user table, password hashing, email verification tokens, reset flows, session rotation, and every OAuth provider's edge cases. That is a permanent maintenance and security obligation, and it is the single most attacked surface in any product.

**Clerk with Supabase third-party JWT integration for browser RLS.** Lost with ADR-0012, which removes the reason to mint Supabase-compatible tokens at all. Not doing it removes an entire class of token-lifetime and key-rotation bugs.

**Rolling our own auth.** Not seriously considered. It is the highest-risk, lowest-differentiation work available.

## Consequences

- Credentials, password reset, OAuth callbacks, and session revocation are outside our threat model and outside our codebase. `05-tdd.md` §11.1 lists spoofing controls that all reduce to "the verified session is the only source of `userId`".
- Two identity records exist — Clerk's and ours — so they can drift. The webhook plus `JOB-identity-sync` is the reconciler, and `JOB-reconcile` retries a failed sync daily. `identity:clerk:{clerkUserId}` is cached in Redis for 3600 s and invalidated by the sync job.
- Deletion has two entry points, both landing on `JOB-delete-account` with idempotency key `del-{userId}`: the user deleting from "Your show", and Clerk's `user.deleted` webhook. The job is idempotent, so both firing is harmless.
- A Clerk outage prevents sign-in. Already-signed-in users keep working until their JWT expires, because verification is read from the token rather than from an API call. There is no fallback authentication path, and adding one would be a larger risk than the outage.
- Clerk is a paid dependency where Supabase Auth was included. Accepted as cheaper than the engineering time it replaces, and the business model is deferred (`00` §1) so no pricing surface depends on it.
- The `evf` claim must be configured in the Clerk dashboard for the gate to work. That is out-of-repo configuration, so `08-eval-testing-plan` MUST cover the session-2 gate as an end-to-end test that fails loudly if the claim is missing.
