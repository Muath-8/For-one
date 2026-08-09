# ADR-0019 — STT pin updated to Scribe v2 identifiers

**Status:** Accepted

## Context

00-decisions §3 pinned ElevenLabs STT as `scribe_v1` (batch + streaming). During 07's provider verification (2026-08-08), ElevenLabs was found to have delisted `scribe_v1` in favour of `scribe_v2` (batch) and `scribe_v2_realtime` (streaming). Pinning a delisted identifier would fail at implementation. The language-catalog rule (ADR-0002) is defined as the intersection of flash-v2.5 TTS support and Scribe STT support; Scribe v2's language coverage is a superset of the flash v2.5 32-language set, so the catalog is unaffected.

## Decision

Amend the STT pins everywhere: batch transcription uses `scribe_v2`; live call-in streaming uses `scribe_v2_realtime`. Cost modelling in 07 §10 already uses currently published Scribe rates. The catalog rule's wording becomes "supported by both `eleven_flash_v2_5` and `scribe_v2`"; the seeded 32-language set is unchanged.

## Alternatives considered

1. **Keep `scribe_v1` until forced.** Rejected: the identifier is already delisted; there is nothing to keep.
2. **Switch live STT to a non-ElevenLabs streaming provider.** Rejected: the stack decision (single STT provider, one billing/ops surface) stands; no evidence against Scribe v2's latency yet — 08's call-in latency tests will verify the 300 ms STT-final allocation in 07 §9.1.

## Consequences

- 00 §1/§3, ADR-0002, ADR-0008, 05 §3.2, 06 §5.2/§15.1, and 07 §2.3 reference the v2 identifiers.
- If Scribe v2 streaming misses the latency allocation in eval, that is a new decision with its own ADR — not a silent swap.
