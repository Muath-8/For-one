# Fix round 2 — consolidated dispatch plan (post quota-reset, after 6:20 AM Riyadh)

Inputs: review-A-traceability.md (29 defects) + review-B-canon.md (18 defects), both in this folder.
Already fixed by the lead (do NOT re-dispatch): RA-01 (06 §7.2/§17.1 + ADR-0018 alt 3), RA-03 (01 §6 metric), RA-04 (05 §9.4 metric), RA-22 (FR-611 citation), RA-23 (00 §2 registers EP/COPY/INV/Q/RL + US note), RA-25 (07 pointer), RA-26 ruling (user vs listener — rule added to 00 §1), RA-27 (00 §1 stage names), RB-04 (00 §3 Testing row), RB-09/RB-12 ratified (00 §9.3), RB-01 ruling recorded as ADR-0020, RB-05 as ADR-0021; 00 §13 register updated.

## srs-agent → 04
- RB-03/ADR-0020: rewrite FR-110 transport-neutral (5 s freshness bound stays; cite 06's state endpoint EP-## once data-agent assigns it; drop poll verbs + [decided here] interval).
- RA-05: fix 12 FR trace lines naming nonexistent prompts → real IDs: PRM-intake-producer, PRM-level-estimate, PRM-realtime-host, PRM-chat-opener/PRM-chat-turns, PRM-error-extraction, PRM-uptake.
- RA-07: replace all 63 "(SCR mapping: 02)" placeholders with real SCR-## IDs from 02; delete the stale §1.3 premise sentence and the §6.4 obligation row.
- RA-09: fix job names to 05 §7 catalog: JOB-export→JOB-export-user-data, JOB-generate-session→JOB-generate-episode, JOB-planner→JOB-planner-run, JOB-session-sweep→JOB-abandon-stale-sessions, JOB-voice-purge→JOB-purge-voice-audio; JOB-intake-finalize has NO counterpart — either cite the real intake completion mechanism from 05 or ask architect to add the job (flag to lead if added).
- RA-11/RA-12/RA-13: regenerate §6.1 strictly as the inverse of FR trace lines (fix 8 over-reports + 61 under-reports); give FR-711 a feature home (trace to F-01 or add explicit "platform-wide, traces to all F via 00 law" — pick: trace it to F-55 telemetry? No: FR-711 is ownership semantics → assign to F-29 learner file? srs decides and records) so no orphan remains.
- RA-15 coordination: nothing in 04 (01 changes).
- RA-28: label NFR-34–40 range as reserved in §1.2.
- RA-26: FR-517/FR-408 "listener" → "user" per new 00 §1 person-vocabulary rule.

## data-agent → 06
- ADR-0020: delete EP-23 (SSE, RL-SSE, pub/sub publisher contract); add the state endpoint as a new EP-## per ADR-0020 (path, schemas, ETag/304, cadence guidance, rate limit sized to 1 s tier; payload = generation readiness + pending after-show reply + pending voice-note reply); renumber/cross-check citations of EP-23.
- RA-02: characters CHECK cardinality(traits) BETWEEN 2 AND 4 contradicts FR-304 (1-trait completion allowed) → change CHECK to BETWEEN 1 AND 4.
- RA-10: quirk/backstory single text columns can't hold FR-304's "at most 3 each" → change to text[] with cardinality <= 3 CHECKs (keep length caps per element or total; decide and state).
- RA-16: retarget ~48 constraint rationale citations from "PRD Part x.y" (historical) to the owning FR-### (140-char → FR-101; 48 h → FR-206; 180–480 s → FR-210; ≤2 refs → FR-216; word bands → FR-217; sweep the rest).
- RA-17: §5.12 personal-reference CHECK cites FR-216.
- RA-09: JOB-purge-call-audio → JOB-purge-voice-audio.

## architect-agent → 05
- ADR-0020: §6.4 cites the new 06 EP-## (no path definition in 05); keep cadence tiers, cite ADR-0020.
- RA-06: add the missing §8.1 publish-failure row (or fold TC-1012's target into an existing row and tell qa-agent which; coordinate) so 05 §8 rows = 08's asserted counts; verify total row count against 08 §14.6 after edit.
- RA-16: sweep 05's ~23 historical-PRD citations → owning FR IDs.
- RA-20: §9.4 metric rows cite 01 §6 for targets (keep measurement expressions).
- RA-09: confirm whether an intake-finalize job exists under another name; if genuinely missing and needed, add JOB row + tell lead; else tell srs-agent the right mechanism to cite.

## ux-agent → 02 + 03
- RB-07: restore typographic punctuation in all [source] strings (≈14: COPY-034, 070, 077, 083, 157, 165, 170, 327, host-boundary lines 1937–39) to match the authority byte-for-byte (00 §9.3 now states punctuation is part of verbatim).
- RB-08: COPY-078 adopts the {title} form: Starting this episode will end "{title}" early. (authority line 1862; destructive labels name the result); note the authority self-inconsistency resolution in Appendix A.
- RB-10: add "personalised experience" to Appendix B.2.
- RB-11: keep "verification link"; add one reconciliation note in Appendix A (authority self-inconsistent 824 vs 1833; clearer form adopted).
- RB-13: restore "token examples" to the mono-usage rule; RB-14: restore "follow media semantics documented in help" clause; RB-15: restore "completion celebration" wording; RB-16: restore "rail" in the responsive table.
- RB-17: add Appendix A note that authority line 1838 pitch is illustrative, not a shipped string.
- RB-18: add mapping note: authority "Paused and resumed sessions" → SCR-06 S6/S9 + COPY-070…082.
- RA-19: 03 DS-ProgrammePitch title-cap lines cite FR-101 (drop bare literals or mark "(FR-101)").
- RA-21: 02/03's four 48-hour mentions cite FR-206.

## ai-agent → 07
- RA-14: renumber §11 failure rows F-01…F-18 → AIF-01…AIF-18 (update §14 table + tell qa-agent for 08's §10.2/§14.6 citations).
- RA-24: §4.6 gate word-band literals → cite FR-217 (keep numbers only inside actual prompt text if the prompt needs them).

## product-agent → 01
- RA-15: F-30 pointers → 07 §7.3–7.4 (thresholds/decay) and 06 §5.7/07 §7.2 (three-valued confidence); remove "confidence value" numeric register + weekly-decay mechanism restatement.
- RA-29: resolved by lead in 00 §2 (US = narrative aids) — add one line in §5 preamble noting it.
- RA-03 already fixed by lead — verify surrounding prose consistent.

## qa-agent → 08
- ADR-0020: add TCs for the state endpoint (correctness, ETag/304, cadence budget under load); remove/replace any TC referencing EP-23.
- RA-06: align §14.6 with 05 §8 after architect's row addition; fix TC-1012's target reference.
- RA-08: add INV-JOB-4 row + TC; fix TC-1188 completeness claim.
- RA-14: update 07 §11 citations to AIF-## once renumbered.
- RA-18: TC-1186 "all 30 jobs" → cite 05 §7 without a count (or the current count after architect's edits).
- D-16/RA-04: confirm TC-1090 language consistent with the fixed 01/05 metric definitions; mark D-16 resolved in §16.2.

## Then: relaunch reviewer C (implementability, original brief) + a delta re-review by A and B scopes (verify fixes only).
