# ADR-0021 — Segment-manifest progressive playback for produced audio

**Status:** Accepted (ratifies the decision recorded in 05 §5.3.3)

## Context

Episode audio is synthesized segment-by-segment in script order and must be playable when the first chunk exists (< 30 s on-selection budget; < 2 s pre-generated start via the cold open). The delivery mechanism determines the player contract, storage layout, retry granularity, and the archive/export story. 05 chose a mechanism inline with two rejected alternatives and no ADR; Phase-3 review (RB-05) flagged the missing record.

## Decision

**Segment-manifest progressive playback, then a concatenated master.** Synthesis uploads fixed-order MP3 segments to Storage as they complete; a JSON manifest (segment keys, durations, running offsets, word-timing spans) is updated atomically per segment; the player fetches the manifest, plays segments gaplessly via scheduled buffer swaps, and displays truthful available-range vs total-duration. When the last segment lands, `JOB-episode-audio-master` concatenates a single master file; archive, export, and Media Session surfaces use that master. EP-53 and its manifest API path remain the sole episode-media read contract and mint `masterUrl`; only segment-by-segment playback is retired for that episode once the master is readable.

## Alternatives considered

1. **HLS packaging.** Rejected: brings a packager, playlist lifecycle, and player library for capabilities (adaptive bitrate, live windows) a fixed-quality private audio stream never uses.
2. **Media Source Extensions streaming.** Rejected: MSE codec/container support is uneven precisely on the primary target (mobile Safari), and debugging MSE edge cases is expensive; plain `<audio>` elements over segment URLs behave identically for this workload.

## Consequences

- The player contract is the EP-53 manifest document: signed segment URLs during progressive playback, `masterUrl` when complete, and ADR-0022's explicit epoch increase for the sole post-readability terminal replacement. EP-21 embeds that same document rather than returning a separate manifest URL.
- Retry granularity is one segment; a failed segment re-synthesizes alone (05 §8.1).
- Export and archive always reference the master, so long-term storage is one object per episode.
- If a future need (adaptive bitrate, DRM, live co-listening) appears, that is a new ADR — not a silent upgrade.
