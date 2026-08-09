# For one — Codex handoff

Updated: 2026-08-08, Asia/Riyadh

## 1. Provenance and mission

This project is being transferred from Claude Code session:

`82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c`

The user's original mandate was to create a complete, implementation-ready product and engineering specification set for **For one**. A junior engineer with no prior context must be able to implement the product without inventing product-visible or architectural behavior. The user explicitly required a phased team workflow:

1. Discovery and canonical decisions.
2. Specialist authoring.
3. Independent adversarial review, author fixes, and repeated review until **zero defects**.
4. Final assembly and `docs/specs/README.md` only after review passes.

The user also supplied a production-grade engineering standard covering scalability, latency, cost, reliability, resilience, security, privacy, accessibility, internationalization, AI quality, data integrity, observability, operability, and testing. The governing instruction is to choose the simplest architecture that satisfies the real requirements while preserving deliberate evolution paths.

## 2. Product in one paragraph

For one is a responsive-web, personalized AI language-learning product presented as the user's own podcast. The daily experience is Episode → Notes → Call-in → After-show. Personalization, difficulty, correction, learning state, and progression remain hidden. The user controls topic, format, and cast. The system uses recasts rather than lesson-like correction, stores long-term learner and character memory, supports generated scripts/audio and live voice interaction, produces an honest Weekly Proof, and provides export, deletion, and voice-consent controls.

Do not rely on this paragraph for implementation facts. The owning specifications are authoritative.

## 3. Authority and ownership

Precedence:

1. `docs/specs/00-decisions.md`.
2. Other files in `docs/specs/`, according to the ownership map in `00-decisions.md` §12.
3. Historical source material in `docs/`.

Exception: `docs/For_one_Design_System_and_UI_Specification.md` is the adopted design authority for UX/UI, subject only to `00-decisions.md` §9.3 and ADR-0016.

Important owners:

- `01-prd.md`: features, personas, user stories, metrics, scope.
- `02-ux-spec.md`: screens, states, exact copy, IA, banned UI lexicon.
- `03-design-system.md`: tokens and component behavior.
- `04-srs.md`: functional and non-functional requirements.
- `05-tdd.md`: architecture, modules, jobs, deployment, security, reliability, observability.
- `06-data-api-spec.md`: schema, state machines, storage, endpoints, errors, rate limits, queries.
- `07-ai-spec.md`: models, prompts, structured outputs, context, memory behavior, AI fallback and budgets.
- `08-eval-testing-plan.md`: test cases, matrices, evaluation, and release gates.
- `09-adrs/`: rationale and consequences of significant decisions.

Read `00-decisions.md` rather than restating its stack, product laws, budgets, or ID schemes here.

## 4. Artifact state at transfer

Present:

- `docs/specs/00-decisions.md`
- `docs/specs/01-prd.md`
- `docs/specs/02-ux-spec.md`
- `docs/specs/03-design-system.md`
- `docs/specs/04-srs.md`
- `docs/specs/05-tdd.md`
- `docs/specs/06-data-api-spec.md`
- `docs/specs/07-ai-spec.md`
- `docs/specs/08-eval-testing-plan.md`
- `docs/specs/09-adrs/ADR-0001` through `ADR-0021`

Absent intentionally:

- `docs/specs/README.md` — Phase 4 has not begun because Phase 3 did not reach zero defects.

The folder is not a Git repository. There is no commit history or reliable diff baseline.

## 5. Work completed before the cutoff

Phase 1 and the first authoring pass were completed. All eight specialist documents and 21 ADRs were written.

The first QA and review rounds found substantial cross-document defects. Authors applied two large fix waves. Confirmed clean checks from the last completed traceability delta review include:

- `04-srs.md` §6.1 was mechanically correct in both traceability directions at that checkpoint.
- All 570 test cases were banded with empty diffs.
- EP-23/SSE retirement was airtight and ADR-0020 polling semantics were in place.
- Cross-document ID families checked by Reviewer A2 resolved.
- The review found zero forbidden normative vocabulary at that checkpoint.
- `01`, `02`, `03`, `04`, `05`, `06`, `07`, and `08` had all received the planned fix-round-2 edits before re-review began.

These are checkpoint results, not a final release verdict. Later implementability review found many unresolved behavioral contradictions.

## 6. Exact cutoff state

Claude Code hit its session limit at approximately 21:30–21:34 Asia/Riyadh on 2026-08-08.

At the cutoff:

- Reviewer A2 had finished its delta review. The lead triaged and applied most of its findings.
- The QA-side A2 follow-ups were complete.
- The TDD-side A2 fixes were substantially complete. The current `05-tdd.md` already defers the 48-hour abandonment retry count to the job catalog instead of duplicating a literal count.
- Two data-spec follow-ups were requested but **did not land** before quota exhaustion:
  1. Give authored immutable duo-intro, host-sign-off, and fallback-episode audio a canonical storage home in the public `catalog` bucket, including key patterns and backing columns/contracts.
  2. Replace prose uses of “part(s)” with “segment(s)” for the ADR-0021 playback unit while preserving schema/key identifiers such as `partsReady` and `part-{nn}.mp3`.
- Reviewer B2, the canon-delta reviewer, did not deliver a final report.
- Reviewer C, the implementability reviewer, did not aggregate a final report. Four of six trace workers did finish and each reported BLOCKED paths.
- Reviewer C never completed the Trust Surface and Weekly Proof traces.
- Phase 4 did not start.

## 7. Recovered review findings that remain actionable

All findings below must be revalidated against the current files before editing. They were produced after fix round 2, so they are high-value leads, but concurrent edits occurred during review.

### 7.1 Reviewer C — onboarding trace

Verdict: **BLOCKED** with 11 High, 8 Medium, and 3 Low findings.

High-level blockers:

- Intake completion and first-session creation have incompatible mechanisms; the SRS path lacks an endpoint.
- `ai_disclosure` gates handoff but no screen/FR/copy collects it.
- Email-verification gating counts sessions inconsistently.
- Age-gate endpoint, status, and error code disagree.
- Conservative one-band offset is unconditional in some owners and confidence-conditional in 07.
- `PRM-level-estimate` has no legal execution point.
- First-episode on-selection gating has incompatible definitions.
- 05 introduces an undefined `cold_open` generation stage.
- Three SCR-05 critical actions have no endpoint.
- FR-110's 90-second delay surface has no screen state, component, or copy.
- Show-name limit is 60 in 04/08 and 64 in 06.

The Medium findings cover the closed error catalog, idempotency semantics, missing timezone-refresh endpoint, Clerk webhook inconsistencies, null `level_step`, missing duo-introduction skip affordance, unbound first-episode length, and `intake_transcript` overflow behavior.

### 7.2 Reviewer C — daily loop trace

Verdict: **BLOCKED** with 6 High, 7 Medium, and 1 Low findings.

Blockers:

- Pre-generated episode content has no storage home before a session exists.
- The client cannot obtain the cold-open URL that underpins the under-2-second path.
- Tap-to-define has two incompatible architectures.
- Planner failure yields incompatible programme behavior.
- In-flight duplicate `Idempotency-Key` behavior is undefined by the owner and contradicted by 05.
- Silent After-show behavior conflicts: one host message versus three, and completion semantics differ.

The Medium findings cover staleness handler/flag naming, 4.5 s versus 5 s rendezvous, lock-key drift, session-create payload shape, conflicting rate limits, “Ready now” semantics, and an invalid `reason='skip'` value.

### 7.3 Reviewer C — live call-in trace

Verdict: **BLOCKED** with 11 High, 9 Medium, and 3 Low findings.

Blockers:

- Latency-triggered voice-note degradation is both mandated and forbidden.
- FR-225's five-second turn-taking gate conflicts with the 300 ms latency allocation.
- Call-in host brief and article armament have no persisted schema home.
- The mandatory `chat_opener` generation stage is undefined.
- `room_finished` incorrectly enqueues post-session analysis before After-show evidence exists.
- Voice-note exchange has no termination rule or speaking→chatting writer.
- 05's voice-note upload path contradicts the signed-upload API and binding “audio never transits our API” rule.
- Hard-cut timing/mechanism conflicts.
- STT dropout has three recovery ladders.
- Live consent revocation is required but cannot reach the agent under the zero-reads-per-turn design.
- LiveKit token TTL is 900 seconds in 06 but 120 seconds in 05/08.

The Medium findings cover the unstable-line trigger, missing prompt context assembly, recast identity persistence, armament enum drift, nonexistent `call_turns.state`, closer semantics, abandonment wording, missing/misaligned LiveKit webhook architecture, model-swap triggers, and VAD values.

### 7.4 Reviewer C — hidden-layer trace

Verdict: **BLOCKED** with 9 High, 7 Medium, and 1 Low finding.

Blockers:

- `error_observations` has required fields no producer emits.
- Uptake has no storage field.
- Learner-fact and memory-extractor enums are disjoint.
- Vocabulary ring promotion/demotion is undefined.
- Target selection lacks formula, tie-break, and 1-versus-2 rule.
- Re-check pass/fail and surfacing are undefined.
- Post-calibration level movement and band/step wrap are undefined.
- One-band-down offset has contradictory conditions.
- Unpinning a dormant fact has no defined effect.

The Medium findings cover post-session prompt membership, character-memory enum drift, nonexistent confidence column, energy range/thresholds, supersession fields, and an invisible fact type.

### 7.5 Reviewer B2 child — design fidelity

Two concrete residual defects:

- `02-ux-spec.md` contained an ASCII apostrophe in the shipped SCR-26 export body (`hosts'` instead of typographic `hosts’`).
- COPY-064 (`{Weekday}, {day} {Month}`) was tagged `[source]` despite no authority counterpart; it needs `[new]` plus an Appendix A.1 composition note.

The reviewer also flagged 14 other `[source]` rows whose brace abstraction or joined-fragment construction is not literally byte-exact. Resolve this by a narrow, explicit convention if justified or retag them consistently. Do not leave the current rule internally inconsistent.

### 7.6 Reviewer B2 child — newly added 08 text

Actionable findings:

- `08` §2.3 restates the testing-tool list without citing `00` §3.
- Its claim that the suite “restates none” of EP-52/EP-53 is false; tests lawfully restate cited expected values.
- EP-53 ETag coverage is re-listed without `durationExact`.
- The foreground/no-determinate-wait polling tier is not tested.
- The 10-second polling tier conflicts with hidden-tab suspension and is silently narrowed.
- `Q-EPISODE-MANIFEST`'s 40 ms budget has no test.

Reviewer B2 itself had already found additional issues before quota exhaustion but never produced a final report. Re-run the complete Reviewer B canon-delta scope; do not assume the six child findings are exhaustive.

### 7.7 Unfinished data-spec fixes

Current-file verification performed during transfer showed:

- The authored duo-intro / host-sign-off / fallback-episode storage addition is absent from `06-data-api-spec.md`.
- Prose still calls ADR-0021 units “parts” in several locations. Preserve identifiers but standardize engineering prose to “segments.”

## 8. Recovery map to the original work

Main Claude transcript:

`C:\Users\muath_vib1xo6\.claude\projects\C--Users-muath-vib1xo6-Documents-Visual-Studio-code-For-one\82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c.jsonl`

Subagent directory:

`C:\Users\muath_vib1xo6\.claude\projects\C--Users-muath-vib1xo6-Documents-Visual-Studio-code-For-one\82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c\subagents`

Most relevant subagent transcripts:

- Onboarding trace: `agent-a8fb3d488d901a471.jsonl`
- Daily-loop trace: `agent-a42d3ccb9394f2492.jsonl`
- Live-call trace: `agent-ae6643ba08c3d3352.jsonl`
- Hidden-layer trace: `agent-a5de8d605bef0e05d.jsonl`
- Reviewer C parent: `agent-areviewer-c-d2e638242f1aaeec.jsonl`
- Reviewer B2 parent: `agent-areviewer-b2-fa7d75a0f706a395.jsonl`
- Design-fidelity child: `agent-a3b3105357ac5a87c.jsonl`
- New-08 canon child: `agent-a215813f1c3ae239c.jsonl`
- Reviewer A2: `agent-areviewer-a2-d49c991dd24eaec1.jsonl`
- Data fixer at cutoff: `agent-afix-data-212e21deb09d3aaa.jsonl`
- TDD fixer at cutoff: `agent-afix-architect-07a18a4038db8271.jsonl`
- QA fixer at cutoff: `agent-afix-qa-d6f13cf6c6c095fc.jsonl`

Claude scratchpad reports, if the temporary directory still exists:

`C:\Users\MUATH_~1\AppData\Local\Temp\claude\C--Users-muath-vib1xo6-Documents-Visual-Studio-code-For-one\82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c\scratchpad`

Important files there:

- `review-A-traceability.md`
- `review-B-canon.md`
- `review-A2-delta.md`
- `fix-round-2-dispatch.md`

Durable copies of those four reports are stored in `docs/review-artifacts/`. The folder is explicitly non-normative and does not participate in the specification authority chain.

## 9. Resume sequence

1. Re-read `00-decisions.md` and verify the current files before accepting any recovered finding.
2. Apply and verify the two unfinished `06` fixes from §7.7.
3. Re-run the full Reviewer B2 canon-delta review, including its original 18-defect scope and everything added in fix round 2.
4. Complete Reviewer C across all six traces. Revalidate the four recovered trace reports; perform the missing Trust Surface and Weekly Proof traces.
5. Triage findings according to the ownership map. Make ordinary engineering decisions; write or amend ADRs for significant or cross-cutting decisions.
6. After each fix wave, independently re-run:
   - cross-document ID closure;
   - F→FR→TC traceability and inverse matrices;
   - endpoint, error, rate-limit, query, job, prompt, screen, copy, component, invariant, and ADR registers;
   - banned normative vocabulary;
   - person vocabulary;
   - design-copy byte fidelity;
   - duplicate-owned-value checks;
   - all six implementation traces.
7. Continue until independent reviewers return zero defects and all six traces are BUILDABLE.
8. Only then create `docs/specs/README.md` with reading order, authority/ownership map, document relationships, implementation entry points, and traceability map.
9. Perform the lead's final personal pass and report completion with evidence, not merely file presence.

## 10. Definition of done

The work is complete only when:

- every required deliverable exists;
- every user-visible path has exact states, copy, validation, failure, offline, concurrency, and permission behavior;
- every endpoint and entity is complete and internally consistent;
- every AI stage has prompt, model, schema, persistence, fallback, latency, cost, and evaluation coverage;
- every FR/NFR maps to executable tests;
- all ID references resolve;
- design copy and tokens preserve the adopted authority;
- independent reviewers report zero defects;
- all six end-to-end traces are BUILDABLE;
- `docs/specs/README.md` is assembled last.
