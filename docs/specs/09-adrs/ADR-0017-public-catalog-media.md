# ADR-0017 — Authored catalog media is public and immutable; signed URLs are for user-owned objects

**Status:** Accepted

## Context

00-decisions §3 originally said "signed URLs only" for Supabase Storage without qualification. The `catalog` bucket holds authored, non-personal media — dialect samples and voice samples — identical for every user and fetched in bulk on the two highest-fan-out onboarding screens (dialect choice, cast-creation voice picker). Serving those through per-object signed URLs adds a mint round-trip per sample and defeats long-lived CDN caching, for objects that contain no user data.

## Decision

Narrow the rule: **signed URLs are mandatory for every user-owned or user-derived object** (episode audio, call recordings, proof audio, exports). The `catalog` bucket is public-read with `Cache-Control: max-age=31536000, immutable`; objects are content-addressed (hash in key) so replacement is a new key, never an overwrite. No object derived from any user may ever be written to `catalog`.

## Alternatives considered

1. **Keep signed URLs everywhere.** Rejected: measurable onboarding latency and URL-mint fan-out purchased zero privacy, because the objects are authored content.
2. **Proxy catalog media through the API.** Rejected: adds server load and latency to remove a CDN benefit.

## Consequences

- 06 §9 marks `catalog` public-immutable; EP-02/EP-03 return plain CDN URLs instead of minting.
- The security review in 08 verifies mechanically that `catalog` contains only seeded content-addressed objects and that no write path from user flows targets it.
- 00-decisions §3 storage row updated to reference this ADR.
