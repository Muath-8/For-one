# For one — implementation-ready documentation handoff

**Updated:** 2026-08-09 09:31 Asia/Riyadh  
**Transfer target:** a fresh Claude Code session on another computer, with no access to the Codex conversation that produced this file  
**Workspace at handoff:** `C:\Users\muath_vib1xo6\Documents\Visual Studio code\For one`  
**Project phase:** Phase 3 — adversarial review and closure  
**Completion status:** **NOT COMPLETE**  
**Repository status:** this folder is **not currently a Git repository**; the files on disk are the only reliable state

---

## 0. Start the new session this way

Give the new Claude Code session this instruction:

> Continue and complete the “For one” implementation-ready documentation project in this workspace. Read `AGENTS.md`, then read `docs/HANDOFF.md` completely, then read `docs/specs/00-decisions.md` completely. Treat the current disk as authoritative; do not rely on old review findings until revalidated. Resume at HANDOFF §9, close the remaining Live/Hidden defects by owner, run fresh independent reviews of all six implementation traces, and create `docs/specs/README.md` only after every trace is BUILDABLE with zero defects and the final mechanical checks pass. Do not wait for me between ordinary engineering decisions.

The new session must follow this order before editing:

1. `AGENTS.md`
2. this file
3. `docs/specs/00-decisions.md`
4. the owning spec for each fact being changed, using `00-decisions.md` §12
5. any directly affected companion specs and tests

Do not begin by rewriting the project. The current documents contain many settled decisions and several rounds of high-value fixes. Resume from the exact open register in §9.

---

## 1. Mission and definition of done

The original mandate came from Claude Code session:

`82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c`

The objective is a complete, internally consistent, implementation-ready product and engineering specification set for **For one**. A junior engineer with no prior context must be able to implement every path without inventing product-visible behavior, state transitions, validation, failure handling, storage rules, AI contracts, or architecture.

The required workflow is:

1. Discovery and canonical decisions.
2. Specialist authoring.
3. Independent adversarial review, author fixes, and repeated re-review until zero defects.
4. Final assembly and `docs/specs/README.md` only after Phase 3 passes.

The project is done only when all of the following are true:

- every required deliverable exists;
- every user-visible path has exact states, copy, validation, failure, offline, concurrency, and permission behavior;
- every endpoint and entity is complete and internally consistent;
- every AI stage has prompt, model, schema, persistence, fallback, latency, cost, and evaluation coverage;
- every FR/NFR maps to executable tests;
- all ID references resolve;
- design copy and tokens preserve the adopted authority;
- fresh independent reviewers report **zero defects**;
- all six end-to-end traces are **BUILDABLE**;
- `docs/specs/README.md` is created last;
- a final lead pass confirms the claims directly from disk.

The six implementation traces are:

1. Onboarding
2. Daily loop
3. Live Call-in
4. Hidden learning layer
5. Weekly Proof
6. Trust surface

---

## 2. Authority and ownership

Precedence is binding:

1. `docs/specs/00-decisions.md`
2. Other files in `docs/specs/`, according to the ownership map in `00-decisions.md` §12
3. Historical/source material under `docs/`

Exception: `docs/For_one_Design_System_and_UI_Specification.md` is the adopted design authority, subject only to `00-decisions.md` §9.3 and ADR-0016.

Owner map:

| File | Sole owner |
|---|---|
| `00-decisions.md` | cross-cutting decisions, conventions, ID schemes, stack, product laws, budget envelopes |
| `01-prd.md` | F-## features, personas, user stories, metrics, scope |
| `02-ux-spec.md` | SCR screens/states, IA, exact user-facing copy, banned UI lexicon |
| `03-design-system.md` | tokens and DS component behavior |
| `04-srs.md` | FR/NFR requirements, exact limits, validation, behavior and state machines |
| `05-tdd.md` | architecture, modules, jobs, security, reliability, deployment, observability |
| `06-data-api-spec.md` | schema, constraints, state machines, storage, endpoints, errors, rate limits, queries |
| `07-ai-spec.md` | models, prompts, schemas, context assembly, memory behavior, AI fallback and budgets |
| `08-eval-testing-plan.md` | tests, matrices, evals and release gates |
| `09-adrs/` | significant decisions, rationale and consequences |

Rules that matter during closure:

- `00-decisions.md` is binding. A contradiction with it is a defect.
- Preserve one source of truth per fact. Change the owner and make companions cite it.
- Do not silently choose between contradictory documents.
- A significant cross-cutting choice requires an ADR and, when it changes canon, an update to `00-decisions.md`.
- Preserve every ID family and the F → FR → TC chain.
- Normative prose uses RFC 2119. The banned normative words named in `00` must not appear outside quoted copy or the rule that names them.
- Engineering prose in 01–06, 08 and 09 says **user**. “Listener” is restricted to 07 prompt voice, quoted copy and 01 user-story narrative.
- Use `rg` first for searches and `apply_patch` for edits.
- There is no Git history to recover from. Inspect every edit directly and avoid destructive rewrites.

---

## 3. Current artifact inventory

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
- `docs/specs/09-adrs/ADR-0001` through `ADR-0023`
- `docs/review-artifacts/` containing non-normative recovered review reports
- the adopted design authority and original source documents under `docs/`

Absent intentionally:

- `docs/specs/README.md`

Do not create the README until fresh independent review returns zero defects for all six traces.

No subagent was still writing when this handoff was generated. The last two specialist turns ended with transport errors, and their intended unfinished work is recorded below. The disk is therefore frozen at this handoff point.

---

## 4. Current owner censuses and mechanical baseline

The current test owner assertion is `TC-1082` in `08-eval-testing-plan.md`. At this handoff it declares:

| Family | Current owner count |
|---|---:|
| Features | 55 |
| Defined FRs | 248 |
| Defined NFRs | 33 |
| Entities | 29 |
| Live API endpoints | 57, plus 2 webhook receivers |
| Retired endpoint IDs | EP-13, EP-23, EP-50 |
| Error codes | 28 |
| Rate-limit classes | 19 |
| Query IDs | 88 |
| Background jobs | 36 |
| Prompts | 21 |
| Model roles | 6 |
| AI failure rows | 19 |
| Screens | 27 |
| Screen states | 307 total, including two retired states |
| Active COPY rows | 301 |
| Reserved COPY IDs | COPY-069, COPY-122, COPY-156 |
| Components | 52 |
| ADRs | 23 |
| Logical tests | 570 |

Additional mechanical observations taken immediately before this handoff:

- `06-data-api-spec.md` has 57 live `EP-*` headings across EP-01…EP-60 excluding the three retired IDs.
- `06` has 88 distinct `Q-*` identifiers and currently claims the registry closes.
- `05` has 36 distinct `JOB-*` identifiers and 36 distinct `INV-*` identifiers.
- `07` has 21 distinct versioned prompts, 6 model roles and 19 AIF rows.
- `02` declares **27 screens / 307 states** and has 301 catalog rows beginning with `COPY-*`.
- `08` still declares **570 logical tests**. A raw regex finds additional compound/secondary TC mentions, so use the owner’s logical-test parser rather than raw unique-ID count.
- `docs/specs/README.md` does not exist.

These counts are a baseline, not proof of semantic closure. If the remaining follow-up lifecycle is implemented as a new job, the job count will likely change from 36 to 37 and every owner/inventory/test assertion must be updated atomically.

---

## 5. Major work already completed

The documentation has received many review/fix waves. Do not redo these areas from scratch.

### 5.1 Canon and product behavior

`00-decisions.md` now records, among other settled decisions:

- export and full account deletion in v1;
- all-language package pipeline;
- exactly three steady-state planner triggers;
- Weekly Proof assessment-week W and delivery-week W+1 identity via ADR-0023;
- zero v1 feature flags;
- automatic primary regeneration, generated-fallback regeneration and reviewed terminal-folio recovery;
- the `support_required` terminal-publication exception;
- unsafe-topic refusal before writes;
- one-way live degradation;
- package starter-set behavior on terminal planner failure;
- distinct honest cost-guard copy;
- authored-duo attribution for terminal fallback via ADR-0022;
- manifest-epoch replacement for post-publication duration failure;
- the `content_terminal_at` forward-stage gate.

### 5.2 Onboarding and Daily loop

Large closure work is already on disk for:

- provisional Clerk profile/age flow and exact under-age behavior;
- asynchronous coalesced intake generation and EP-59 recovery;
- one-pitch onboarding variants 1/2 plus deterministic variant 3;
- pitch-owned pre-generation attachment and EP-16 branch matrix;
- exact server-owned local date/session cap;
- remix/scratch pitch-only then EP-16 choreography;
- safe-topic refusal;
- Today pending-first-set projection;
- strict >20-hour staleness and 4.5-second join inside the 5-second SLA;
- package starter-set assembly and acceptance prediction formula;
- cost parking for generation jobs;
- reviewed terminal folio and forward-stage content-terminal freeze;
- progressive manifest/epoch behavior and transcript timing states.

The latest recorded independent lead status before the final Live/Hidden wave was **Onboarding BUILDABLE — 0 defects** and **Daily loop BUILDABLE — 0 defects**. Because later shared-doc edits touched 02–08, both traces must still be rerun before completion.

### 5.3 Weekly Proof and Trust

Major fixes on disk include:

- canonical ProofInput and 90–150-second script contract;
- zero-win flat-week branch;
- durable proof evidence, transcript, delivery window and playback checkpoint;
- ADR-0023 schedule/cutoff behavior;
- text and voice knowledge correction through EP-43;
- consent-history read contract;
- closed export serializer, replacement/retry/expiry behavior;
- deletion propagation, provider completion and transactional email outbox.

These traces received author/QA fixes, but no final independent zero-defect verdict is recorded after the latest changes. They need fresh re-review.

### 5.4 Live Call-in

Already implemented on disk:

- EP-24 entry CAS and exact room/agent tuple;
- EP-60 authenticated/idempotent live-End intent, targeted agent RPC and reconciliation;
- closed durable degradation causes;
- offline-at-entry and microphone-denial voice-note authorization;
- signed direct upload, durable host reply audio and one-way voice-note continuation;
- finalization receipts, participant-left grace and hard cut;
- exact immediate local cutoff/conditional confirmation behavior;
- same-document memory-only unsent voice-note policy, warning and Discard action.

### 5.5 Hidden learning layer

Already implemented on disk:

- exact target selection/lifecycle and recheck outcomes;
- stable recast identity and deterministic uptake window algorithm;
- productive-vocabulary evidence tuples and generated frontier column design;
- expected-structure package catalog and avoidance projection/evidence shape;
- lazy salience/dormancy and explicit unpin;
- frozen session effective coordinate/energy modifier;
- post-session atomic application identity and evidence cutoff;
- What-works five-metric projection;
- exact CAF paired-window persistence and movement selection.

Several final owner contradictions in this area remain open in §9.

---

## 6. Changes that landed immediately before this handoff

These edits are current disk state and may not appear in older review artifacts.

### 6.1 `05-tdd.md`

- §4.6 now orders healthy live entry as:
  1. allocate stable room;
  2. create exactly one dispatch;
  3. receive stable agent identity;
  4. sign token;
  5. lock/CAS and atomically persist `(live_room_name, live_agent_identity, live_entry_nonce, live_room_issued_at)`;
  6. cancel dispatch/delete empty room on any pre-commit failure;
  7. return the token after commit.
- §5.4.4 now states that first End activation cuts local microphone and remote playout immediately. If SCR-12/S12 confirmation is required during an active utterance, EP-60 is deferred until confirmation; Cancel may restore audio only after a fresh eligible owner-state check. Once EP-60 is sent, no branch restores live audio.

These changes close two findings from the latest Live reviewer, but need independent re-review and test comparison.

### 6.2 `02-ux-spec.md`, `03-design-system.md`, `04-srs.md`, `08-eval-testing-plan.md`

The last QA turn landed before disconnect:

- COPY-154 now includes the exact same-document loss warning and **Discard recording** action.
- SCR-12/S19 and SCR-13 voice-note states implement the memory-only Blob lifecycle.
- SCR-12/S20 transitions at exactly 7:00 even if sign-off is missing/unusable/incomplete.
- SCR-12/S12 and DS-CallInStage implement immediate local cutoff, conditional confirmation, guarded Cancel and EP-60 submission.
- FR and TC coverage was updated for these behaviors.

Current UX counts remain 27 screens / 307 states / 301 active COPY rows / 52 components.

### 6.3 `07-ai-spec.md`

The lead began the final Hidden repair wave and landed only these parts before switching to this handoff:

- a shared closed `errorCategorySchema` is now used by error extraction and CAF;
- CAF metrics now have explicit non-negative/upper bounds;
- `heaviestCategories` uses the closed taxonomy;
- vocabulary counts have consistency checks;
- CAF delta magnitude/evidence are non-empty, and evidence is capped at 280;
- `PRM-uptake` now returns required stable evidence `{ sourceTurnId, quote, startUtf16, endUtf16 }` for every 0–2 rating;
- uptake has an exact owner/session/cutoff/substring deterministic gate;
- skipped Notes or no user production is a deterministic absent result and does not call the prompt.

Companion persistence/tests for the new uptake tuple have **not** been completed. The other planned 07 fixes in §9 remain open.

### 6.4 Interrupted specialist turns

Two specialist turns ended with `stream disconnected before completion`:

- data owner intended to patch `06-data-api-spec.md` for the remaining Hidden storage/query contracts;
- QA owner intended to finish companion requirements/tests.

Do not assume their intended patches landed. The timestamp audit showed `06-data-api-spec.md` was last written before that final Hidden task began. Revalidate every intended change directly.

---

## 7. Latest independent trace verdicts

The most recent independent read-only reviewer focused on Live and Hidden after the previous broad fix waves.

### Live Call-in

Initial verdict: **BLOCKED — 5 defects**.

Four were subsequently addressed on disk:

1. EP-24 allocation/dispatch/agent/CAS order — fixed in `05` §4.6.
2. Missing memory-only pre-record warning and Discard action — fixed in `02`/`03`/`04`/`08` using COPY-154.
3. Hard cut depending on sign-off completion — fixed in SCR-12/S20 and companions.
4. End “one action” versus active-utterance confirmation — fixed across `02`/`03`/`04`/`05`/`08`.

One known Live defect remains open:

5. `07` AIF-11’s claimed closed degradation set is incomplete.

### Hidden layer

Latest verdict: **BLOCKED — 12 defects**.

Two have partial AI-owner fixes on disk:

- CAF output bounds/closed categories — patched in `07`, needs test/review confirmation.
- uptake evidence identity/gate — patched in `07`, but `06` persistence and `08` tests still need alignment.

The remaining register is in §9.

### Onboarding and Daily loop

Latest recorded status before this final shared wave: both were independently reported BUILDABLE with zero defects. Rerun both after all Live/Hidden changes because shared owners changed.

### Weekly Proof and Trust

Author and QA repairs landed after their last blocking review, but no fresh final independent zero-defect report is recorded. Rerun both.

---

## 8. Current known-good mechanical checks

Before the unfinished Hidden repair wave, the project had repeatedly passed these scoped checks:

- 248/248 defined FRs and 33/33 defined NFRs;
- F → FR inverse closure for 55 features;
- 570 logical tests with matrices preserved;
- endpoint/error/rate/query/job/prompt/screen/copy/component census synchronization at the values in §4;
- 23 ADR files and register closure;
- banned normative vocabulary scans;
- person-vocabulary scans;
- no `docs/specs/README.md` before Phase 4.

Run them again after the remaining edits. The current `07` patch has not yet received the complete global mechanical pass.

---

## 9. Exact open defect register and recommended owner routing

Every item below was revalidated against current disk immediately before this handoff unless marked “partial fix.” Line numbers are anchors for the current files and will drift after edits; search by identifiers/text.

### 9.1 Live — AIF-11 closed cause set

**Severity:** High  
**Owner:** `07-ai-spec.md`  
**Current anchor:** AIF-11 near line 3506

Current AIF-11 names connection, agent-worker and TTS exhaustion, plus entry LiveKit/microphone paths, then says “no other cause exists.” It omits current 06-owned causes:

- `offline_at_entry`
- `stt_recovery_exhausted`
- `llm_recovery_exhausted`

The exact current closed set in `06` is:

1. `offline_at_entry`
2. `livekit_unavailable`
3. `microphone_denied`
4. `connection_recovery_exhausted`
5. `agent_worker_recovery_exhausted`
6. `stt_recovery_exhausted`
7. `llm_recovery_exhausted`
8. `tts_recovery_exhausted`

**Required correction:** make AIF-11 cite the 06-owned closed set and map each writer/detector without restating an incomplete subset. Preserve the rule that recoverable failures and latency never authorize degradation. Recheck AIF-09 and AIF-13 for the STT/LLM writers. Add/verify exact 08 coverage across all eight causes.

### 9.2 Hidden — avoidance projection deadlock

**Severity:** High  
**Owners:** `07` context assembly; `06` query/projection; `08` tests

Current `07` episode context row near lines 2815–2818 says `{receptive_structures}` contains only zero to two **ready** flags. But every new weekly flag begins `awaiting_exposure` and can become ready only after generation/playout exposure. Selecting ready-only makes first exposure impossible.

`07` §7.7.1 already describes generation of unresolved flags and EP-19 playout evidence more accurately. `06` currently stores unresolved states and orders them, but Q-AVOIDANCE-PROJECTION still ends with language suggesting generation selects unresolved ready rows.

**Required correction:** one owner rule must select at most two unresolved flags from `awaiting_exposure|receptive|ready`, excluding `resolved`, in a deterministic total order. Freeze IDs/package keys/receptive forms into the generation manifest. EP-19’s first actual `playing` event remains the sole exposure writer. Add first-exposure, repeated-exposure, readiness-boundary, replay and empty-projection tests.

### 9.3 Hidden — due recheck omitted from prompt target context

**Severity:** High  
**Owner:** `07`

`07` §7.7 correctly selects at most one overdue `recheck` before ordinary `active|taking` targets and freezes the assignment. But the episode context table still re-queries only `active|taking` targets by score.

**Required correction:** `{targets}` must consume the session’s frozen assignment list, in frozen order, including the optional due recheck. Generation must not re-query current target lifecycle. Add a due-recheck fixture proving the same target reaches script/article/call brief and survives lifecycle changes after the cutoff.

### 9.4 Hidden — avoidance threshold contradiction

**Severity:** High  
**Owner:** `07`

`07` §7.1 still says an avoidance flag is written only after the structure is absent across at least two weeks. `07` §7.7.1 and FR-425 create flags from each qualifying weekly assessment and then use one-/two-week exposure windows for readiness.

**Required correction:** §7.1 must say a qualifying weekly absence creates `awaiting_exposure`; the one-/two-week timing classifies readiness after actual delivery, not flag creation. Do not retain the old two-week creation threshold.

### 9.5 Hidden — follow-up lifecycle has no executable scheduler/writer

**Severity:** High  
**Owners:** `05` job architecture and `06` schema/query; `08` tests

FR-011 owns:

- `due` when the date is within 48 hours of the current instant;
- `expired` when the date is more than 7 days in the past and unused;
- closed states `pending|due|used|expired`.

Current `06` has `follow_ups.due_on`, `state`, `idx_followups_scan` and Q-FOLLOWUP-HOOK-SCAN, but no exact scheduled transition fields/CAS contract. Current `05` has no registered task that actually performs `pending→due`, fires the follow-up planner reason, or applies `pending|due→expired`.

**Recommended production-grade correction:**

- In `06`, freeze server-computed due/expiry instants from `due_on` and the timezone used at capture; add exact state/timestamp tuple constraints and an identifier-only scanner projection.
- In `05`, add one `JOB-follow-up-lifecycle` with discriminated scanner/subject modes or another equally explicit single mechanism. Post-commit delayed runs should use stable keys; a bounded scanner must repair insert-to-enqueue crashes.
- At due, lock the row and CAS `pending→due`; only the winner enqueues `JOB-planner-run` with reason `follow_up`.
- At expiry, CAS unused `pending|due→expired`; `used` wins every race and is terminal for this scheduler.
- Define exact cadence, retries, idempotency, stale-run no-op rules and timezone behavior.
- Add boundary tests at 49h/48h/47h before and exactly 7 days/just over 7 days after, plus due/use and due/expiry races.

If a new job ID is added, update the 36-job census everywhere, the job/failure registers and `TC-1082`.

### 9.6 Hidden — frontier vocabulary owner/order drift

**Severity:** High  
**Owners:** `06` query and `07` context

FR-128 and the 06 `PitchBrief` freeze `frontierLemmaIds`, but `07`’s episode context table re-queries `vocab_items` for three emerging/receptive items. Q-FRONTIER-VOCAB currently says only “one user; 07-owned k” and has no total order.

**Required correction:** Q-FRONTIER-VOCAB must define a deterministic owner-scoped selection order and return stable IDs. Planner freezes those IDs into PitchBrief. Episode/article generation resolves exactly the frozen IDs in that order and never substitutes a newer frontier member. Missing/invalid frozen IDs fail the stage or produce the owner-defined empty block; they must not silently re-rank.

### 9.7 Hidden — ADR-0015 names obsolete recast evidence

**Severity:** Medium/High canon drift  
**Owner:** `docs/specs/09-adrs/ADR-0015-recast-enforcement.md`

The consequence near line 40 says recast uptake joins delivered recasts against later `error_observations`. Current canonical behavior uses immutable `sessions.target_outcomes` plus stable `evidenceTurnIds` and the deterministic post-recast window in `07` §7.7.

**Required correction:** amend the ADR consequence to describe the current evidence identity/algorithm. Do not change the accepted decision or invent a second uptake path.

### 9.8 Hidden — character-memory runtime permissions contradict required mutation

**Severity:** High  
**Owner:** `06`

`06` §1.2 classifies `character_memories` as append-only with only salience mutation. Elsewhere, character memories require:

- `status='superseded'` from validated memory supersession;
- `last_touched_at` maintenance with salience touch.

The declared runtime grants cannot perform the required writer.

**Required correction:** define narrow column-level grants for the exact mutable interpretation fields, preserve immutable provenance/content, and make §1.2, §5.6, export semantics and tests agree. Do not make the whole table generally mutable.

### 9.9 Hidden — follow-up evidence quote can be empty

**Severity:** High  
**Owner:** `07`

`PRM-memory-extraction.followUps[].quote` currently uses `.max(280)` without `.min(1)`, and the deterministic gate checks only the date. An ungrounded follow-up can pass schema and persist.

**Required correction:** require `.min(1).max(280)` and validate the quote as an exact substring of a stable user-authored source turn in the frozen session. Apply the same ownership/span rules as other persisted memory evidence. Reject invalid follow-ups without truncation.

### 9.10 Hidden — character-memory character ID is not ownership/cast gated

**Severity:** High  
**Owners:** `07` gate, `06` repository/constraint, `08` security tests

`PRM-memory-extraction.characterMemory[].characterId` is an arbitrary UUID. Current schema has a foreign key but no `(user,character)` partition constraint, and the deterministic gate does not require membership in the session’s actual effective cast.

**Required correction:** validate every proposed character ID against the owner-scoped character repository and the session’s frozen effective delivered cast (delivered override when present, otherwise selected cast). A cross-user or non-participating ID must reject the complete memory-extraction application before any domain write, because the post-session bundle is atomic. Add cross-partition and retired/non-cast tests.

### 9.11 Hidden — CAF structured-output validation

**Status:** AI-owner patch landed; needs companion verification  
**Owner:** `07`; tests in `08`

The lead added a closed error-category schema, metric bounds, vocabulary consistency checks and non-empty 280-character delta evidence. Revalidate:

- every metric’s units and upper bounds against 06 persistence and fixtures;
- unique `heaviestCategories` if required by the intended contract;
- Zod 4 syntax in the documented schema;
- 08 boundary tests for negative, out-of-range and foreign enum values;
- the CAF current-revision writer remains unchanged.

### 9.12 Hidden — uptake evidence persistence is only partially aligned

**Severity:** High until complete  
**Owners:** `06` persistence and `08` tests; `07` patch already landed

`07` now requires `{ sourceTurnId, quote, startUtf16, endUtf16 }` for every rating and defines an exact gate. Current `06` still stores only `sessions.uptake_evidence text` capped at 300, with no stable turn/span identity.

**Required correction:** change the owner persistence shape to retain the exact stable evidence tuple (without adding an entity), constrain it with the rating/evaluation tuple, and make post-session replay/rebuild validate the same user/session/cutoff substring. Update export privacy if the hidden tuple must remain excluded. Add 0/1/2 rating fixtures, empty/foreign/interim/out-of-range failures and deterministic absent cases.

### 9.13 Hidden — memory session summary lacks episode context

**Severity:** High  
**Owner:** `07`

`PRM-memory-extraction` requires a non-empty session summary covering what the episode was about and the user’s position. Its current context supplies existing memory plus call/chat only. A skipped or silent session can have no user transcript, and the model has no authoritative episode/topic/article facts from which to write a grounded summary.

**Recommended correction:** add a bounded trusted `{session_facts}` block to the prompt and context budget containing exact session/topic/format, episode/article title or compact validated descriptors, terminal/skipped stages and selected/delivered cast IDs. Keep total context at 4,200 tokens by using the currently unused 300-token headroom. Instruct the prompt to derive summary content only from session facts plus supplied user evidence. Empty evidence must yield empty memory arrays and a grounded summary/no-op rather than invention. Add silent/skipped/no-call/no-chat tests.

### 9.14 Hidden — target context and follow-up fixes must preserve atomic post-session behavior

This is a cross-check rather than a separate reviewer count. `05` §5.5 currently owns one frozen post-session manifest and one atomic domain commit. Any fixes above must not reintroduce independent substage commits, current-state re-queries after the cutoff, or partial writes. Failed validation of character identity or uptake evidence must leave the complete attempt unapplied and retry the same frozen input under the job bound.

---

## 10. Suggested next implementation wave

Use owner-separated edits to avoid new contradictions.

### Wave A — AI and ADR owner

Edit only `07-ai-spec.md` and ADR-0015:

1. Fix AIF-11’s eight-cause mapping.
2. Make episode `{targets}` consume frozen assignments including recheck.
3. Make `{frontier_vocab}` consume frozen PitchBrief IDs.
4. Make `{receptive_structures}` select unresolved avoidance states, not ready-only.
5. Correct the avoidance creation threshold.
6. Require and gate follow-up quotes.
7. Add character owner/effective-cast validation.
8. Add grounded `{session_facts}` context.
9. Amend ADR-0015’s recast evidence consequence.
10. Recheck the already-landed CAF/uptake schema patch and code fences.

### Wave B — data/API owner

Edit only `06-data-api-spec.md`:

1. Add exact follow-up lifecycle persistence/CAS/scanner support.
2. Define Q-FRONTIER-VOCAB’s total order and frozen-ID contract.
3. Align Q-AVOIDANCE-PROJECTION with unresolved flag generation.
4. Align character-memory grants/mutability.
5. Add character owner/effective-cast validation at the repository boundary.
6. Replace plain uptake text with the stable evidence tuple.
7. Preserve the 29-entity census unless an ADR intentionally changes it.
8. Recompute Q/error/RL/EP counts only if actual identifiers change.

### Wave C — architecture owner

Edit `05-tdd.md`:

1. Add the exact follow-up lifecycle execution mechanism and job registration.
2. Cite the 06 owner fields/query instead of duplicating them.
3. Add failure/retry/reconciliation rows and observability.
4. Preserve the three-value planner trigger register; the scheduler produces the existing `follow_up` reason rather than a fourth trigger.

### Wave D — requirements/QA companions

Edit `04-srs.md` only if an owner contract exposes a missing required rule; otherwise cite existing FRs. Edit `08-eval-testing-plan.md` to add exact boundary, race, security and rebuild assertions without creating unnecessary new TC IDs. Update all censuses if the job/query inventory changes.

### Wave E — independent review

Use fresh read-only reviewers who did not author the fixes:

- Reviewer 1: Onboarding + Daily loop
- Reviewer 2: Live + Hidden
- Reviewer 3: Weekly Proof + Trust
- Reviewer 4: canon/design/copy/ID/mechanical delta

Require separate verdicts in the exact format:

`<Trace>: BUILDABLE — 0 defects`

Any nonzero verdict must include severity, owner, exact citations and required correction. Repeat author/fresh-review waves until every trace is zero.

---

## 11. Final mechanical closure checklist

After semantic review is zero, run all of these against current disk:

1. F register = 55 and F → FR inverse is exact.
2. Defined FR blocks = 248; defined NFR blocks = 33.
3. Every FR/NFR has a primary TC and the inverse matrices match.
4. Logical test total remains 570 unless a deliberate owner change updates the catalog and matrices coherently.
5. Parse and compare endpoint headings, retired IDs and receiver count.
6. Parse and compare error, rate-limit, query, job, invariant, prompt, model, AIF, screen, state, copy, component and ADR registers.
7. Verify all references resolve exactly once and retired/reserved IDs are not rendered or reused.
8. Verify 29 entity sections unless an ADR changes the census.
9. Verify banned normative vocabulary.
10. Verify engineering person vocabulary.
11. Verify no replacement characters, broken UTF-8, trailing whitespace or unbalanced code fences.
12. Verify copy byte fidelity and `[source]` provenance under `00` §9.3.
13. Verify no duplicate owner values or stale census prose.
14. Verify every storage/object path has retention/deletion/export treatment.
15. Verify every async job has trigger, stable key, timeout, retry bound, terminal result, lost-enqueue repair and test.
16. Verify every AI prompt has role, schema, context, deterministic gate, persistence, fallback, cost and eval coverage.
17. Rerun all six end-to-end implementation traces from a blank junior-engineer perspective.

Only after all checks and independent trace verdicts are zero should Phase 4 begin.

---

## 12. Phase 4 README requirements

Create `docs/specs/README.md` last. It should contain:

- status and scope;
- reading order;
- authority/precedence rules;
- ownership map;
- document relationships;
- implementation entry points by product flow;
- ID/traceability map;
- architecture/data/API/AI/test navigation;
- ADR index;
- how to verify the owner censuses and test matrices;
- a statement that source documents outside `docs/specs/` are historical except for the adopted design authority.

Do not copy whole enumerations into the README. Cite the owner sections so the README cannot become another source of truth.

---

## 13. Recovery map to the original Claude work

Original main transcript on the old computer:

`C:\Users\muath_vib1xo6\.claude\projects\C--Users-muath-vib1xo6-Documents-Visual-Studio-code-For-one\82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c.jsonl`

Original subagent directory:

`C:\Users\muath_vib1xo6\.claude\projects\C--Users-muath-vib1xo6-Documents-Visual-Studio-code-For-one\82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c\subagents`

Notable original subagent transcripts:

- onboarding trace: `agent-a8fb3d488d901a471.jsonl`
- daily-loop trace: `agent-a42d3ccb9394f2492.jsonl`
- live-call trace: `agent-ae6643ba08c3d3352.jsonl`
- hidden-layer trace: `agent-a5de8d605bef0e05d.jsonl`
- Reviewer C parent: `agent-areviewer-c-d2e638242f1aaeec.jsonl`
- Reviewer B2 parent: `agent-areviewer-b2-fa7d75a0f706a395.jsonl`
- design-fidelity child: `agent-a3b3105357ac5a87c.jsonl`
- new-08 canon child: `agent-a215813f1c3ae239c.jsonl`
- Reviewer A2: `agent-areviewer-a2-d49c991dd24eaec1.jsonl`
- data fixer at cutoff: `agent-afix-data-212e21deb09d3aaa.jsonl`
- TDD fixer at cutoff: `agent-afix-architect-07a18a4038db8271.jsonl`
- QA fixer at cutoff: `agent-afix-qa-d6f13cf6c6c095fc.jsonl`

Durable copies of the important recovered reports are under `docs/review-artifacts/`. They are non-normative leads only. Current specs and fresh review win.

---

## 14. Moving/pushing the workspace safely

Because this folder has no Git repository, make sure the transfer includes the entire project folder, especially:

- `AGENTS.md`
- `docs/HANDOFF.md`
- all `docs/specs/`
- all `docs/specs/09-adrs/`
- `docs/For_one_Design_System_and_UI_Specification.md`
- `docs/review-artifacts/`
- the remaining source documents under `docs/`

Preserve UTF-8 bytes. Several documents contain curly punctuation, arrows, mathematical symbols and non-ASCII names; an editor or copy process that rewrites them can create design-copy defects.

If initializing Git for the transfer, do it only after copying the complete folder and confirming file counts. Make the current disk one baseline commit before any new Claude edits, because there is no earlier repository history. Do not treat that commit as a claim that Phase 3 passed.

---

## 15. Final state statement

The project is substantially advanced and mechanically coherent, but it is **not implementation-ready yet** under its own zero-defect bar. The remaining known work is concentrated in one Live AI-fallback row and the Hidden-layer lifecycle/evidence contracts in §9, followed by fresh review of all six traces and final assembly.

Do not declare completion from file presence or counts. Completion requires fresh independent zero-defect verdicts, all six BUILDABLE traces, the full mechanical pass, and then the Phase 4 README.
