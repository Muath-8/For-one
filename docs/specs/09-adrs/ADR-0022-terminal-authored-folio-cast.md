# ADR-0022 — Terminal authored-folio cast attribution

**Status:** Accepted

## Context

FR-213 normally requires the episode to use exactly the cast the user selected. FR-417 also requires a reviewed terminal fallback that remains shippable after generated fallback exhaustion, and NFR-03 requires the first episode to begin within three minutes. A created host or arbitrary selected pairing cannot have immutable fallback audio authored before that user and pairing exist. Runtime synthesis cannot be the terminal guarantee when synthesis, orchestration, or the quality path is what failed.

The specifications therefore need one explicit answer for the otherwise impossible intersection of cast fidelity, immutable terminal media, and the first-frame deadline. Silent substitution would violate the trust contract.

## Decision

The selected cast remains immutable requested metadata for the session. Normal generation and the generated fallback MUST use it. Only when the terminal reviewed-folio claim wins—after FR-417's generated path is exhausted, after an eligible generation stage exhausts its 05-owned provider/orchestrator bound and claims `fallback_reason='orchestrator_exhausted'`, at the first-episode deadline, or when an already-readable generated epoch cannot close inside its applicable FR-027/FR-210 duration band and claims `fallback_reason='postpublication_duration_failure'`—MAY delivery use the language package's authored duo.

The claim atomically records a delivered-cast override with reason `terminal_authored_folio`. Episode attribution, transcript speakers, Notes attribution, call brief, and After-show opener all resolve the delivered authored duo from that override. The interface states the actual duo with the exact 02-owned template and MUST NOT imply that the selected cast spoke. The override is not available to planners, cost controls, ordinary retries, or pedagogy.

The post-publication duration claim is the sole path that replaces a readable manifest. It lets the buffered old segment end at its authored boundary, atomically publishes the complete reviewed folio as manifest epoch 2, retires epoch 1, resets playback to zero, and renders the exact simpler-episode and delivered-cast copy before a new Play. It MUST NOT splice the authored duo into generated audio, merge epochs, resume the old position, or withdraw audio mid-word.

Until the active epoch is content-terminal, Episode playback MAY use its ready range but Notes, Call-in, and After-show MUST remain unreachable. The terminal writer and the epoch-2 replacement writer atomically freeze Episode, Notes, definitions, call brief, and chat opener before exposing the monotonic content-terminal projection. This forward-surface gate prevents a user from entering Notes or Call-in against a folio that the sole replacement path could still supersede; it does not require listening to finish or waiting for asynchronous master concatenation.

If publication of that reviewed folio itself exhausts its infrastructure retry bound, the losing transaction publishes none of its artifacts or cast override. The job and episode commit the 06-owned terminal failed tuple; EP-52 maps only that tuple to `support_required`; and 02 renders COPY-341 with one configured human-support link and no Retry. This is the sole terminal-infrastructure exception to the delivery guarantee in FR-027 and FR-418. It does not permit a generated or ungated substitute, and it does not make Today or earlier completed work empty.

## Alternatives considered

1. **Synthesize the terminal fallback in the selected cast.** Rejected because it makes the terminal path depend on the same runtime provider and generation path it must survive, and cannot guarantee NFR-03.
2. **Pre-author terminal media for every cast.** Rejected because user-created hosts and arbitrary pairings do not exist at package-authoring time; the combination count is unbounded.
3. **Substitute the authored duo silently.** Rejected because it lies about who is speaking and violates the trust contract.
4. **Fail the cycle when ordinary or generated authoring fails.** Rejected because FR-418 requires automatic generated and reviewed fallbacks and FR-027 requires the first cycle to continue. A terminal publication failure after the reviewed immutable folio itself exhausts is distinguished from content-path failure and uses the closed support result above.

## Consequences

- FR-213 gains one narrow, visible terminal exception; all ordinary cast fidelity remains unchanged.
- 06 preserves selected-cast identifiers and stores the delivered override separately, so audit/export can distinguish request from delivery.
- The full reviewed folio uses one coherent delivered cast across Episode, Notes, Call-in, and After-show.
- EP-52 and EP-53 expose one monotonic content-terminal projection; the UI and transition endpoint withhold every downstream folio consumer until it is true, while master concatenation may finish later.
- A terminal publication failure exposes no partial folio or delivered-cast override and has one persistent support mapping; it cannot be mistaken for another generation mode.
- 02 owns one exact runtime-name template; 08 tests solo, created-host, mixed-pair, and authored-duo sessions plus every forbidden attempt to set the override outside the terminal claim.
- Removing or widening this exception requires a new ADR and a canon update.
