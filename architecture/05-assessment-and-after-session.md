# Assessment engine, after-session pass and the claim gate

*For one technical architecture, domain 5 of 9. Written 2026-10-16, revised 2026-10-17 after design review, and revised again 2026-11-06 against the 2026-10-23 decisions (decisions.md), the second review pass (the conformance and skeptic reviews in `_review-findings.md`, which had not been applied before) and 10-decision-records.md. Written against PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the assessment, language-acquisition and learning-science lenses, and the Milestone 0 kit (04-production.md, 05-prompts.md, 06-then-and-now.md). "PRD x.y" means PRD-v2 part x.y; where decisions.md or 10-decision-records changed a part, the decision is cited instead (ADR-01). Tags: [DECISION] decided here; [ASSUMPTION] assumed because the sources are silent; [OPEN for Muath] only the owner can settle. Names in this document align with 01-system-topology.md, 02-generation-pipeline.md, 03-live-call-and-voice.md and 04-learner-model-and-data.md where those documents already named something, and with 10-decision-records section 4 everywhere; where none of them names a thing, the names here are canonical.*

*What changed in this revision, in one paragraph.* Teaching is invisible (ADR-06): Salma's after-call notes, the polish card, the chat margin note, the 90-second stage 1 and everything that served them (`notes`, `margin_notes`, `notes.ready`, `note_shown`, `notes_mode`, the polish-line TTS, the notes cost line) are gone; the after-session pass is one Inngest function with the 10-minute budget, and corrections reach the learner only as recasts inside the conversation, planned by the teacher's echo plan from the recast evidence this pass extracts. The pass now builds one `AfterPassResult` and hands it to the data domain's `stores.apply_after_pass` in a single transaction, runs once per evidence event with an idempotency key and an evidence watermark, appends `call_turn_verbatim` instead of updating an event, persists the validated analyst output as an `analyst_result` event so `learner/rebuild` replays without vendor calls, and writes `word_uses` (ADR-19). The `claims` table is the data domain's (04 D13) and the gate writes it through `record_claim`; the kinds are the finer ones here, plus `skill_range` for "where do I stand". Accuracy and talkback claims get an analytic standard error, then-and-now claims lose their rule-3 waiver, the multiple-comparisons policy is stated, and the ten native-language claim templates are given. Evidence is per target language and the first-language transfer list is driven by `native_language` (ADR-02); the build plan is re-dated to 2026-11-18 to 12-22 and re-sequenced to the team as it is (ADR-07); operations are round the clock (ADR-16). Section 11 lists every finding and ruling applied.

Scope: everything that runs after a session and everything that makes a claim about progress. PRD-v2 Parts 10 and 11, 9.1 to 9.3 as the consumer of this output, 8.5 (rebuilds), 14.1 after-session roles, and decisions.md §3 and §4 (invisible teaching; evidence instead of tests). Not in scope: the live call (03), episode generation and the teacher's own reasoning (02), the event log's physical schema and the nine stores' storage (data domain), the notebook's screens (client domain), the correction guard's code (07, with the per-language phrase list) and the `explicit_corrections_per_100_turns` measure itself (09; this domain supplies one of its two detectors).

---

## 1. Summary and the decisions in one table

The after-session pass is one Inngest function, `session/after-pass`, that finishes inside 10 minutes of the call ending and hands the teacher a new learner-model version through one `AfterPassResult` applied in one transaction by the data domain (ADR-06: there is no notes stage and nothing from this pass is shown to the learner after a call). Models judge only what needs judgment (what the learner meant, the smallest fix, whether a moment shows a skill, which facts were stated); code does everything that must be consistent (classification, counting, measures, lifecycles, probabilities, the claim gate, prompted-ness). The claim gate is a Python module with one entry point writing one table, the data domain's `claims`, through `record_claim`, and that table is the only input of the weekly proof, the finale, the return episode's "real win", the "New for you" card and "where do I stand". Corrections reach the learner only inside the conversation: this pass records which recasts the host made and whether the learner took them up, and the teacher's echo plan (02, 03 `recasts`) decides which right forms the next call and episodes carry.

| # | Decision | Chosen | Reason | Rejected |
|---|---|---|---|---|
| D1 | Shape of the pass | One Inngest function `session/after-pass` with the 10-minute budget and six steps (wait for the last verbatim turn, analyst, classify and measure, memory keeper, claim candidates, apply); it runs once per evidence event (a full run on `call.ended`, a text-only run on `chat.closed` and `voicenote.received`) with the idempotency key `{session_id}:{trigger_type}:{trigger_event_id}` and processes only events after the learner's `high_water_seq`; per-turn verbatim transcription runs during the call in `call/verbatim-turn` [DECISION, ADR-06, PRD-v2 10.2] | Invisible teaching removes the 90 s stage; per-turn transcription still keeps the storage-off deletion window at 15 min and lets the pass start at once; chat and round two are the PRD's cleanest grammar and fluency evidence and must reach the analyst | A 90 s notes stage (removed by decisions.md §3); a whole-call re-transcription after `call.ended`; one run per session that ignores chat and round two |
| D2 | Analyst model and shape | Claude Haiku 5.5 (`claude-haiku-5-5`), structured output against the `AnalystOutput` Pydantic schema, `effort: low` set explicitly, standard pricing, `retries=0` with an `asyncio.wait_for` of 90 s; one prompt and one call per run, incremental on later runs of the same session (new events only); the validated output is appended as an `analyst_result` event so rebuilds replay it without a vendor call [DECISION, PRD-v2 14.1, 04 D14] | Cheapest model that handles minimal-edit correction and quote-exact extraction; structured outputs remove the parsing failure mode; one prompt is what the calibration set certifies; 10 min does not allow Batch | Sonnet for the analyst (5 to 20x cost for a job the calibration set will show Haiku does); a `fast` and a `full` variant (two prompts, two outputs for the same turns, nothing to calibrate against); Batch pricing (24 h worst case) |
| D3 | Error classification | Code: ERRANT-style alignment and typing in Python (`errant` with the target package's spaCy model, `en_core_web_sm` for English, the pipeline's lemmatizer) on normalized text (fillers and repetitions stripped, punctuation restored), then the target package's rule table `packages/languages/<target>/structure_rules.yaml` maps ERRANT types plus named feature predicates to inventory structure ids and the 12 categories; v1 carries the claim-feeding set (about 30 to 40 structures) plus the category fallback [DECISION, PRD-v2 10.2 step 3, 10.4, ADR-02] | "Models propose, code decides"; the same edit always gets the same tag, which calibration needs; ERRANT is the published standard for English and the per-language rule table is what makes a second target language a package, not a rewrite | Asking the model for the structure id (labels drift, precision cannot be measured per tag); a few-hundred-row table in week 1 |
| D4 | Obligatory-context counting | Analyst marks `needed_structures` per turn from a closed list (the session's targets plus the structures the host's necessity moves invite); code counts contexts and correctness from the classifier's output; a context the analyst invents without a detector pattern is dropped [DECISION, PRD-v2 10.3] | Obligatory contexts need judgment ("was the past needed here?") but the count must be auditable | Pure rule detectors (miss most contexts), pure model counts (unauditable) |
| D5 | Confidence filter | An edit is "clean" when every verbatim word in its span, plus one word on each side, has confidence at or above `asr.confidence_threshold[vendor]` (per recognizer, in `packages/languages/<target>/recognizer.yaml`, set by the language gate's 30-clip check; placeholder 0.70 for the primary [ASSUMPTION]) and the turn was not `verbatim_failed`, not dial-in, not a voice note recorded under the weak-link fallback; a turn transcribed by a vendor without a calibrated threshold is never clean; unclean edits are stored with `clean=false`, feed planning at half weight, and never feed a claim [DECISION, PRD-v2 10.2 step 4, ADR-03] | The PRD makes the threshold empirical and vendor scores are not comparable across vendors; the neighbourhood rule catches boundary misrecognitions | One threshold for two vendors; dropping unclean edits entirely (planning loses signal) |
| D6 | Measures and segments | Fluency and complexity only on `comparable_segments` (retell turn, round two, recording tasks), minimum 40 pruned words or 30 s; accuracy on every clean turn and chat message; all formulas in 4.4 [DECISION, PRD-v2 10.3] | The assessment lens: task moves the numbers more than growth; the PRD limits fluency to retell, round two and recordings | Whole-call fluency (confounded by topic and by the host's questions) |
| D7 | Word knowledge | Three Beta distributions per lemma (heard, read, produced), prior from frequency rank and the vocabulary-size estimate, fixed evidence weights (4.5.1); every production is one `word_uses` row (04's table, written here, ADR-19); "owned" is a count rule on clean unprompted `word_uses` rows, not a probability threshold; an owned word that is edited twice afterwards gets `shaky_since` and is shown with its later sentence [DECISION, PRD-v2 8.3, 10.6] | Every estimate carries a range for free; the fitter can read the mean; the owned rule must be explainable in one sentence to the learner and openable to the two uses | Single probability with ad hoc bumps; rings (confident/emerging/unseen); un-owning a word silently |
| D8 | Skill estimates | Four scalar estimates on an internal 0 to 100 scale anchored to CEFR bands, each a Gaussian (mean, variance) updated by a scalar Kalman step with fixed observation noise; in the beta the observations are the band prior, the word check (listening, reading), the two A3 English moments, and for speaking `errors_per_100` and `mlr` against a published anchor table plus the rater's band once calibrated; the full feature tables are P1 after the first external-test correlations [DECISION, PRD-v2 10.8] | Slow, bounded, carries a range, explainable; one formula for all four skills; the beta needs the planning signal, not a scoring system nobody has data to fit | IRT or a learned model (no data until months in); four feature tables with unpublished anchors in the beta |
| D9 | Error versus slip | Pattern key `(structure_id, error_type)`; needs 3 clean, non-self-corrected observations across 2 or more sessions; slips are stored and visible to the teacher as slips, never targetable [DECISION, PRD-v2 10.5, 9.2.6] | PRD rule, made precise: self-corrections are monitoring evidence, not errors | Counting any edit |
| D10 | Claim gate placement | A pure module `forone.assessment.claims` whose only write is `stores.record_claim` into the data domain's `claims` table (04 D13; the kind enum is this document's: `did_it`, `first_ever`, `word_owned`, `mistake_gone`, `fluency_change`, `complexity_change`, `accuracy_change`, `accuracy_fell_while_trying`, `talkback_falling`, `then_and_now`, `skill_range`); the proof producer, the teacher's `claims_passed`, the finale, the "New for you" card and Salma's "where do I stand" (`salma_explain`) read only `claims` rows with `gate.passed=true`; nothing else in the codebase can write a progress sentence [DECISION, PRD-v2 10.10, law 12] | Fabricated wins impossible by construction; a monthly audit can read one table; two owners of one table would mean two schemas | Letting the proof producer prompt see the learner model; a second `claims` DDL in this domain |
| D11 | Standard errors | `metric_calibration` rows per `(metric, task_type)`: for fluency and complexity metrics `sem` from test-retest pairs written by `calibration/pairs-daily` (claimable when `n_pairs >= 20`, provisional from 12), carried across `assessment_version` bumps that do not touch the measures module; for accuracy and talkback kinds an analytic standard error (binomial on correct/contexts, Poisson on asks per call) with `source='analytic'`; until a row exists only `did_it`, `first_ever`, `word_owned` and `skill_range` claims exist [DECISION, PRD-v2 10.10, 11.1.8] | PRD rule; an SD from 12 pairs has about ±21% relative error, so 20 is the honest bar; accuracy has no test-retest pairs and a count-based SE is the standard answer | Hard-coded thresholds per metric; accuracy claims failing with `no_standard_error` forever |
| D12 | Rater pinning and versions | `vendors.yaml roles.rater.pinned_until` plus a `rater_versions` row per window (the first window runs from the first cohort to 2027-02-16 so no first finale crosses a boundary, 4.15); `assessment_version` is one semver string stamped on every row this domain writes and recorded in `learner_model_versions.code_versions` with its parts (`analyst`, `classifier`, `measures`, `memory_keeper`, `rater_pin`); a change triggers the data domain's `learner/rebuild`, which replays stored `analyst_result` events and re-runs the model only when `code_versions.analyst` changed [DECISION, PRD-v2 10.11, 8.5, 04 D14] | An upgrade must never look like progress; a rebuild must be one command, deterministic and free of vendor calls; a two-engineer team cannot afford two rebuild mechanisms | Silent upgrades; a second rebuild function `assessment/rebuild` with shadow tables of its own and a Haiku re-run per session |
| D13 | Corrections after the call | None are shown (ADR-06, decisions.md §3). The pass records every host recast and its uptake, every self-correction and every pattern observation, and hands the teacher an `echo_plan_input` (recurring errors with the right form and the last recast outcome); the teacher's echo plan (02) and the host brief's `recasts` (03) are the only correction channel; the analyst also flags any host line that reads as an explicit correction, which feeds 09's `explicit_corrections_per_100_turns` (ceiling 0) beside the correction guard (07) [DECISION, ADR-06, concept-v2 law 7] | Muath's call; law 7 must be enforced by code the way law 12 is, and the teacher needs the recast evidence to plan the next echo | Salma's notes, the polish card and the margin note (decisions.md §3); notes behind a flag (a flag never changes a law) |
| D14 | Then-and-now rating | Code metrics (fluency, complexity, repeat-task scoring by alignment) plus one pinned Sonnet 5.5 call for holistic band and retell content points, with package anchor transcripts in the prompt; one recording per sitting (`sitting_n`), forms cycling A, B, C, D, A so consecutive sittings never share a form, the comparison is sitting n against n−1 (and n−3 for the 3-month window) [DECISION, PRD-v2 10.9.2, 11.3, 14.1] | Most of the comparison is arithmetic on verbatim transcripts; the model is needed only for "meaning kept" and band; the PRD has one recording in week 1 and one per finale, not two per season | A model-only rating (unstable); a second human rater in production (cost); a 'then' and a 'now' recording per season (doubles the one performance moment) |
| D15 | Weekly proof production | `proof/make` builds a `ProofPlan` in code from `claims`, the schedule and the last plan; Sonnet 5.5 writes Salma's script from the plan with the claim sentences quoted verbatim; `voice-studio.render` voices it; clips are byte ranges of kept audio [DECISION, PRD-v2 11.1] | The simple P0 proof and the full P1 proof differ only in which claim kinds exist in `claims` | A separate proof pipeline per version |
| D16 | Correction propagation | A `wrong_memory_flag` event is applied synchronously by the data domain's `apply_learner_edit` (fact fixed at once, version bumped, every cached brief invalid by construction); `memory/correct` then resolves unmatched flags (facts used in the last call go `on_hold` until resolved), fans out `facts.invalidated`, and for a disputed quote appends a `quote_disputed {event_id, claim_id}` event and invalidates every claim whose evidence carries that quote with a notice in the next proof [DECISION, PRD-v2 8.4 rule 7, 8.5, trust promise 7, 04 D1] | A wrong memory is a bug and must not survive in any cache; nothing ever updates an event | Fixing the fact and hoping briefs are recompiled; setting a status on the original event |
| D17 | Store writes | Stages 2 to 5 are pure functions over `call_turns_v`, `chat_message` events and the stores as they stood; they build one `AfterPassResult` (04 §4.3.0) and the last step calls `stores.apply_after_pass(result)` once, which writes the nine stores, `word_uses`, `structure_observations`, the scheduler and the version in one transaction; on the 6-minute deadline the partial result is applied once with `evidence_quality=partial` or nothing is applied; every observation carries a deterministic id so a replay or a retry writes nothing twice [DECISION, 04 §B, D4] | A memory-keeper failure must not leave stores updated under the old version; Inngest retries steps, so writes must be idempotent | Writing stores in step 4, facts in step 5 and the version in step 7 (half-applied sessions) |

---

## 2. Requirements this domain implements

| Requirement | PRD-v2 | What it binds here |
|---|---|---|
| Nothing in assessment runs in the live path; the pass may influence tomorrow's plan, never a claim | 10.1 | `session/after-pass` is the only writer; the claim gate runs on stored evidence only |
| Verbatim re-transcription of every learner audio turn with fillers, timings, confidences | 10.2.1, 5.4.11 | `call/verbatim-turn` (shell in 01, step body here); `VerbatimRecognizer` adapter |
| Analyst: smallest correction, uptake 0 to 2, can-do moments, words reached for, recast uptake, self-corrections | 10.2.2 | `AnalystOutput` schema (4.2) |
| Edit classifier into inventory and 12 categories; obligatory-context use | 10.2.3, 10.4 | `edit_classifier` module, `structure_rules.yaml` (4.3) |
| Confidence filter from the 30-clip test | 10.2.4, 10.14 | `asr.confidence_threshold`, `clean` flag (4.1) |
| Measures per 10.3 | 10.2.5, 10.3 | `measures` module (4.4) |
| Bayesian updates with ranges; review states; lifecycles | 10.2.6, 10.6, 9.4 | `updater` module (4.5) |
| Memory keeper with quote check and the confidence ladder | 10.2.7, 8.4 | `memory_keeper` module (4.6) |
| Teaching is invisible: no notes, polish card or margin note; corrections only as recasts inside the conversation; `explicit_corrections_per_100_turns` ceiling 0 | decisions.md §3, concept-v2 law 7, ADR-06 (replaces PRD-v2 5.5, 5.6.6, 10.12 correction layers) | 4.7: recast evidence, the echo plan input, the analyst's explicit-correction flag; no learner-facing output from the pass |
| Pass plus teacher update within 10 min | 9.1.1, 15 | timeline in 3.4; `session.after_pass.completed` by minute 3 typical, 6 min hard |
| Evidence instead of tests: the notebook, "where do I stand" with a range when asked, the then-and-now tape, the weekly proof | decisions.md §4 | `skill_range` claims (4.8), `claims_passed`, 4.10, 4.11 |
| Several episodes a day feed one evidence store; the proof counts sessions, not days | ADR-04, ADR-05 | every run keys on `session_id`; `proofs.sessions_in_week` is computed from `session_summaries` (4.11.1) |
| Error vs slip: 3 observations across 2 sessions | 10.5, 9.2.6 | 4.5.4 |
| Lifecycle: taking, stable, re-checks; words owned | 10.6 | 4.5.3 |
| Avoidance, weekly | 10.7, 9.3 | 4.5.5 |
| Skill estimates with ranges; "where do I stand" only when calibrated, as a claim | 10.8, 10.10, decisions.md §4 f | 4.5.6, `skill_calibration`, claim kind `skill_range` (4.8.1) |
| Word check scoring into a vocabulary-size estimate | 10.9.1 | `word_check.score()` (4.5.1) |
| Then-and-now: tasks, framing, first "then" in week 1, storage-off rule, never dial-in | 10.9.2, 12.5.2 | 4.10 |
| The five gate rules; SE rule; honest fallback sentences; impossibility of fabricated wins | 10.10, law 12, trust 1 and 4 | 4.8 |
| Calibration set, bars, pinned rater, re-run on model change | 10.11 | 4.9 |
| Correction layers: only the live recast remains; the layers after the call are removed | 10.12 as amended by ADR-06 | 4.7 |
| External test | 10.13 | 4.12 |
| Recognizer test feeds the threshold | 10.14 | 4.1, 7 |
| Weekly proof (simple P0, full P1), slow/flat/worse weeks, the "more" section, worth-it question | 11.1 | 4.11 |
| Season finale with at most two measured differences | 11.2 | 4.11.4 |
| Rebuild on version change; shown claims never silently retracted | 8.5 | 4.14 (the data domain's `learner/rebuild` with this domain's pure stages and stored `analyst_result` events) |
| Wrong memory fixed at once and counted | 8.4.7, 16.1 | 4.14 |
| Laws 1, 5, 7, 12; trust promises 1, 4, 6, 7 | 1.2, 1.3 | Law scan on the proof, the finale narration and Salma's explanations; AI signature; no inference of sensitive classes; claims only through the gate; the correction guard (07) on every host and Salma line |
| Cost: re-transcription and pronunciation $0.03, analyst and memory keeper $0.04, proof share $0.03; the former notes line is now "Salma (when asked) and chat" and is 03's and 08's | 14.5 as amended by ADR-06 | Section 6 |
| Consent: voice recordings for the learner's own progress only; anonymized transcripts (no audio) for calibration with `data_use`; purge within 24 h; data use revocable | 12.5.3, 12.5.5, 12.5.8, trust promise 8 | 4.9 (text-only calibration samples keyed by `learner_id`), `consent/apply` (4.14) |
| Crisis detection in after-session analysis | 7.9.3 | `AnalystOutput.flags.crisis` leads to `crisis.detected_after_session` |

---

## 3. Architecture

### 3.1 Components (canonical names)

All Python, inside the `workflows` service of the topology (01 decision 3), package `forone.assessment`. Nothing here runs in `api` or `call-worker`.

| Component | Kind | Job |
|---|---|---|
| `call/verbatim-turn` | Inngest function (shell: topology; body: here) | One learner turn: verbatim STT, per-vendor confidence annotation, `clean_spans`, append `call_turn_verbatim` through `events.append()`, delete the turn audio when storage is off |
| `session/after-pass` | Inngest function (shell: topology; body: here) | One run per evidence event: wait for the last verbatim turn, analyst, classify and measure, memory keeper, claim candidates, `apply_after_pass`; emits `session.after_pass.completed` |
| `analyst` | Module, one Haiku 5.5 call, one prompt | `AnalystOutput` per run (incremental on later runs of a session); validated output appended as an `analyst_result` event |
| `edit_classifier` | Module, code (spaCy + errant + `structure_rules.yaml`) | Edits to structure ids and categories; obligatory-context tallies |
| `measures` | Module, code | Fluency, complexity, accuracy, comprehension, talkback, pronunciation roll-ups |
| `updater` | Module, code | Word bank, structure map, error profile, skills, taste rows; scheduler grades |
| `memory_keeper` | Module, one Haiku 5.5 call plus rules | Fact candidates with quotes, interests, goals, canon; quote verification |
| `claims` (`forone.assessment.claims`) | Module, code | Candidate generation, dedupe, the five-rule gate and the template renderer; writes the data domain's `claims` through `record_claim` |
| `echo_plan_input` | Module, code | Recast outcomes, self-corrections and recurring errors with their right forms for the teacher's echo plan (02); the only correction channel (ADR-06) |
| `law_scan` | Module, code | Digits (Western and Eastern Arabic), number words, grades, levels, lesson and progress words outside the allowed slots; runs on the proof script, the finale narration, Salma's explanations and, in CI, on the rendered template set |
| `recording/rate` | Inngest function | Verbatim per task, code metrics, pinned rater, comparison through the gate |
| `proof/make` | Inngest function (shell: topology; body: here) | Weekly proof; finale differences for the pipeline's finale episode |
| `memory/correct` | Inngest function | Unresolved `wrong_memory_flag` handling after `apply_learner_edit`, `on_hold` facts, `quote_disputed`, `facts.invalidated` fan-out |
| `consent/apply` | Step inside the data domain's `learner.consent_changed` handling (body here) | What voice revocation, data-use off and deletion do to `claim_evidence`, `calibration_samples`, `test_retest_pairs` |
| `calibration/run` | Inngest function (manual or on version bump) | Run analyst, classifier and rater over `calibration_samples`; write `calibration_runs`; block deploys that miss the bars |
| `calibration/pairs-daily` | Inngest cron, 03:00 UTC (fixed UTC, not learner-relative, ADR-16) | Build `test_retest_pairs` per task type by the pairing rules in 4.8.2 and recompute `metric_calibration` |
| rebuild (the data domain's `learner/rebuild`, 04 D14) | Pure functions from this domain called by 04 | `analyst.replay(analyst_result)`, `classify`, `measure`, `update`, `claims.generate` over stored events; no vendor call unless `code_versions.analyst` changed |
| `word_check` | Module, code | Scores the 48-item check into a vocabulary-size estimate with a range |
| `external_tests` | Table plus admin import | Week-0 and week-8 scores; correlation report |

### 3.2 Diagrams, described

**Diagram A: the after-session pass (draw as a swimlane with four lanes: call-worker, Inngest functions, Postgres/S3, model vendors; time runs left to right with one vertical dashed line at 10 min and a thinner one at 6 min, the domain's own deadline).**

1. During the call, each learner turn ends: `call-worker` uploads `turn-{n}.ogg` and emits `call.turn_audio_ready`. `call/verbatim-turn` (concurrency 20) calls the `VerbatimRecognizer`, appends a `call_turn_verbatim` event (`call_id, turn_index, text, words[], vendor, disfluencies_kept, low_confidence_reason`) through `events.append()`, emits `verbatim.turn_completed`, deletes the audio if `voice_storage=false`. Nothing updates the `call_turn` event; readers use `call_turns_v` (04).
2. `call.ended` arrives. `session/after-pass` starts (concurrency 1 per learner, idempotency key `{session_id}:call.ended:{event_id}`). Step `wait_last_turn`: `waitForEvent verbatim.turn_completed` matching the last `turn_index`, timeout 20 s; on timeout the last turn uses its streaming text at `clean=false` and the run waits for the verbatim event up to 3 min before classifying.
3. Steps `analyst` (one Haiku call on the learner turns and chat messages after the learner's `high_water_seq`, `retries=0`), `classify_and_measure` (code), `memory_keeper` (one Haiku call plus the quote check), `claims_candidates` (code). Each is a pure function; together they fill one `AfterPassResult` plus the claim candidates. The validated analyst output is appended as an `analyst_result` event in the same step that produced it.
4. Step `apply`: `stores.apply_after_pass(result)` (04) in one transaction writes the nine stores, `word_uses`, `structure_observations`, the scheduler grades, `session_summaries`, bumps `learner_model_version` with cause `after_pass` and the `high_water_seq`, then `record_claim` for every passed candidate, then `session.after_pass.completed`. The 10-minute line is drawn after it; the teacher's step in `episode/produce` (02) is shown starting at it.
5. The same function runs again on `chat.closed` and `voicenote.received` for the session (text-only run: analyst on the new messages only, classifier, updater, memory keeper, claim candidates, `apply`), each run bumping the version once. `recording.completed` is handled by `recording/rate`, not by this function.
6. A side arrow from every model call to the tracing lane (`vendor_calls` written in their own transaction, Langfuse metadata only; ADR-09, ADR-13).

**Diagram B: the claim path (draw as a funnel).** Inputs at the top: `structure_map`, `word_bank`, `comparable_segments`, `recording_ratings`, `analyst can-do moments`. Middle: `claims.generate_candidates()` produces `claims` rows with `status=candidate`. The gate box has five sub-boxes in order: like-for-like, beyond-the-noise, repeated, clean evidence, openable; each either passes the row to the next or stamps `status=failed` with `failed_rule`. Outputs at the bottom, each reading only rows with `gate.passed=true` and `invalidated_at is null`: `proof/make`, `briefs.compile('teacher').claims_passed` (data domain), the finale (pipeline), the "New for you" card on Today and in the notebook (`did_it` and `first_ever` only, client domain), and `salma_explain` ("where do I stand" reads the `skill_range` claim, so the answer has a `claim_evidence` set and a "how we know"). An arrow from the shown surfaces back to `claims.shown_at` via the `claim_shown` event (04's `mark_claim_shown`, idempotent).

### 3.3 Interfaces

**Events consumed.** `call.turn_audio_ready`, `recording.turn_audio_ready` (03 4.10, same shape with `surface`), `call.ended {learner_id, call_id, session_id, kind, end_reason, voice_storage}` (a full run; `kind` carries `main`, `round_two`, `first`), `chat.closed {learner_id, session_id, chat_id}` (a text-only run; `chat_id` is the per-session exchange from opener to closer inside the host's long thread [ASSUMPTION: emitted by `api` at the closer or the learner's last message]), `voicenote.received {learner_id, session_id, event_id}` (a text-only run on the small-door note's verbatim text), `recording.completed {learner_id, recording_id, sitting_n, form}` [ASSUMPTION: emitted by `api` when all three task uploads are in], `pronunciation.scored {learner_id, event_id}` (03), `proof.requested {learner_id, week_start, proof_day}` (`proof/fanout`, 01), `season.boundary {learner_id, season_number}`, `memory.flagged {learner_id, event_id, fact_id|null, claim_id|null, disputed_text}` (`api` mirrors the `wrong_memory_flag` log event after `apply_learner_edit` ran [ASSUMPTION]), `working_on.changed`, `learner.consent_changed {learner_id, voice_storage, data_use}`, `learner.rebuild_requested` (handled by 04; this domain's functions are called). `chat.learner_message` is no longer consumed (the margin note is removed, ADR-06).

**Events emitted.** `verbatim.turn_completed {learner_id, call_id, turn_index, event_id, status}`, `session.after_pass.completed {learner_id, session_id, learner_model_version, trigger, evidence_quality: "full"|"partial"|"text_only"}`, `claims.updated {learner_id, passed: int}`, `proof.ready {learner_id, episode_id}`, `recording.rated {learner_id, recording_id}`, `facts.invalidated {learner_id, fact_ids[]}`, `claims.retracted {learner_id, claim_ids[]}` (the data domain writes the `claim_invalidations` rows), `crisis.detected_after_session {learner_id, session_id, event_id}`, `calibration.completed {component, passed}`. **Log events appended** (through `events.append()`, types registered in 04's registry [ASSUMPTION]): `call_turn_verbatim`, `small_door_voice_verbatim`, `analyst_result {session_id, run_id, trigger_event_id, output: AnalystOutput, prompt_version}` (about 3 KB), `quote_disputed {event_id, claim_id, disputed_text}`.

**APIs provided (Python, in-process; other domains import them).**

```python
# forone/assessment/api.py
def claims_passed(learner_id: UUID, *, since: date | None = None) -> list[Claim]          # TeacherInput.claims_passed, finale, return episode
def finale_differences(learner_id: UUID, season_number: int) -> list[Claim]                # at most 2, kind in (fluency_change, complexity_change, accuracy_change, mistake_gone)
def skill_answer(learner_id: UUID) -> dict[str, Claim | None]                              # for salma_explain's "where do I stand": the passed skill_range claim per skill, None when not calibrated
def session_summary(session_id: UUID) -> SessionSummary                                    # last_14_days rows for the teacher
def grade_word_check(answers: list[WordCheckAnswer]) -> VocabEstimate                      # onboarding A4
def produced_before(learner_id: UUID) -> set[str]                                          # lemmas with a word_uses row; for the live talkback role's word-or-hint (03, PRD-v2 5.4.5.4)
def active_targets_with_evidence(learner_id: UUID) -> list[TargetWithEvidence]           # structure, lifecycle, acc_14d, three clean quotes; for the host brief's recasts and salma_explain
def echo_plan_input(learner_id: UUID) -> EchoPlanInput                                    # recurring errors, right forms, last recast outcomes; for the teacher (02), ADR-06
def law_scan(text: str, *, allowed_slots: list[str], native_language: str) -> ScanResult   # shared scanner (4.7.3)
```

**Tables this domain owns** (DDL in 4.16): `session_summaries`, `comparable_segments`, `claim_evidence`, `metric_calibration`, `test_retest_pairs`, `calibration_samples`, `calibration_runs`, `rater_versions`, `recordings`, `recording_ratings`, `proofs`, `external_tests`, `skill_calibration`, `working_on_items`. **Tables it writes but does not own**: `claims` (04 D13, through `record_claim`; the `claim_invalidations` rows are 04's), `word_uses` and `structure_observations` (04, through `AfterPassResult`, ADR-19), the data domain's nine stores (word bank, structure map, error profile, skills, interests, life, goals (the can-do and season-goal rows only), taste (the per-session rows), show canon) and `out_in_world`, all through `stores.apply_after_pass`. `notes` and `margin_notes` no longer exist (ADR-06).

### 3.4 The one budget as a timeline, and the run rules

There is one budget: `session.after_pass.completed` within 10 minutes of `call.ended` (PRD-v2 9.1.1, 15), with this domain's own hard deadline at 6 minutes. The 90-second notes budget is gone with the notes (ADR-06; PRD-v2 15's "Salma's notes after a call: under 90 s" is removed). The clock is the `call.ended` timestamp in the payload, not the event's arrival.

| t | Step | Typical | Worst allowed |
|---|---|---|---|
| 0:00 | `call.ended` received; `after-pass` starts | 1 to 3 s | 5 s |
| 0:03 | `wait_last_turn`: only the last turn's verbatim is outstanding (earlier turns were transcribed during the call) | 5 to 12 s | 20 s, then streaming text at `clean=false`; the run keeps waiting for the verbatim event up to 3:00 |
| 0:15 | `analyst`: Haiku 5.5 on the learner turns and chat so far, about 9k input (3k cached), about 2.5k output, `effort: low` explicit, `asyncio.wait_for(90)`, `retries=0` | 15 to 40 s | 90 s, then `analyst_failed` |
| 0:55 | `classify_and_measure`: normalization, spaCy parse, errant alignment, rules, measures, `word_uses` and `structure_observations` rows built | 2 to 6 s | 15 s |
| 1:01 | `memory_keeper`: Haiku 5.5, about 6k input, about 1k output, `effort: low`; quote check in code | 10 to 25 s | 60 s, then facts queued for `memory/retry` |
| 1:26 | `claims_candidates`, dedupe and the gate; templates rendered | under 2 s | 5 s |
| 1:28 | `apply`: `stores.apply_after_pass(result)` in one transaction, `record_claim` per passed candidate, `session.after_pass.completed` | 1 to 3 s | 10 s |
| **about 1:30** | **Teacher starts (02 4.3); it has more than 8 minutes** | | **6:00 hard: `apply` runs with what completed, `evidence_quality=partial`** |

The pipeline waits at most 15 min for `session.after_pass.completed` (02 4.2 `wait_after_pass`) and then plans from the model as it stands. After the 6-minute deadline, `apply` is called once with the partial result (stages that did not finish contribute nothing; `evidence_quality=partial`) or, if `classify_and_measure` itself did not finish, with nothing at all except `session_summaries`; the stores are never half-applied (D17).

**Run rules.**

- **Triggers.** A full run on `call.ended` (`kind` in `first`, `main`, `round_two`); a text-only run on `chat.closed` (the chat opens within 30 s of the call ending and can run for minutes, PRD-v2 5.6.2) and on `voicenote.received` (the small-door note, PRD-v2 3.7). Each run has its own cost line (section 6: about $0.003 for a text-only run) and bumps `learner_model_version` once. `recording.completed` starts `recording/rate`. The teacher's next run, nightly or on demand, picks up the chat evidence through the usual brief.
- **Idempotency key** `{session_id}:{trigger_type}:{trigger_event_id}`. Inngest step retries are off on the two model steps (`retries=0` with the in-step timeout); code steps may retry because they are pure.
- **Evidence watermark.** A run processes only `events.seq` greater than the learner's `high_water_seq` in the last `learner_model_versions` row (04 D4), so the chat-close run never re-extracts the call's edits, pseudo-counts are added once, `contexts_14d` is a query over `structure_observations`, and the Kalman step for a skill runs once per observation (the chat run contributes only the writing observation).
- **Observation identity.** `structure_observations.id = uuid5(session_id, event_id, structure_id, span)` (04 §4.3.2) and `word_uses` is unique on `(learner_id, unit_id, event_id)` [ASSUMPTION: 04 adds the constraint], so a replay or a retry writes nothing twice.
- **Analyst incrementality.** On a later run of the same session the analyst receives the stored `analyst_result` of the earlier runs (edits already found, `skipped_spans`) plus the new events only; dedupe of claim candidates is by `(kind, subject, source_event_id)`.

---

## 4. Detailed design

### 4.1 Verbatim turns and the confidence filter

`call/verbatim-turn` body (the shell, concurrency 20, `is_last` priority, retries 2 with the secondary vendor when the queue age exceeds 30 s, is in 01 4.3). It appends a second event; it never updates one (04 D1, D2; ADR-19):

```python
async def verbatim_turn(evt: CallTurnAudioReady):
    L = learner(evt.learner_id)                                                 # target_language, native_language, tz
    audio = await s3.get(evt.media_id, dek=keys.dek(evt.learner_id))          # SSE-C, memory only
    res = await adapters.for_role("verbatim_stt", target=L.target_language).transcribe(
        audio=audio, content_type="audio/ogg", language=L.target_language,     # talkback clips in the native language never come here
        meta=CallMeta(learner_id=evt.learner_id, role="verbatim_stt", call_id=evt.call_id, ...))
    thr = package(L.target_language).asr.confidence_threshold.get(res.vendor)  # per vendor, set by the language gate's 30-clip check (ADR-03); None = uncalibrated
    words = [{**w, "clean": thr is not None and w["confidence"] >= thr} for w in res.words]
    clean_spans = merge_runs(words, key="clean")                                # [(start_idx, end_idx)] of consecutive clean words
    low_conf = None if thr is not None else "vendor_uncalibrated"
    if evt.source_mode == "voice_notes_fallback": low_conf = "weak_link_fallback"   # PRD-v2 5.4.10 only
    await events.append([Event(type="call_turn_verbatim", learner_id=evt.learner_id, call_id=evt.call_id,
        event_id=uuid5(NS, f"{evt.event_id}:verbatim"),                          # deterministic: a retry appends nothing new (04 4.1.3)
        payload={"call_id": evt.call_id, "turn_index": evt.turn_index, "text": res.text, "words": words,
                 "vendor": res.vendor, "disfluencies_kept": True, "low_confidence_reason": low_conf,
                 "clean_spans": clean_spans, "clean_share": clean_words / len(words), "assessment_version": ASSESSMENT_VERSION})])
    if not evt.voice_storage: await media.delete(evt.media_id)
    await inngest.send("verbatim.turn_completed", {...})
```

The recording tasks and the small-door voice note go through the same body with `surface=recording` or `surface=small_door`; the small-door note's event type is `small_door_voice_verbatim` (04's `QUOTE_SOURCES`). Readers in this domain use `call_turns_v` (04 4.1.2), which joins `call_turn` and `call_turn_verbatim` on `(call_id, turn_index)`; a turn whose verbatim event is missing has `text_verbatim is null` and no clean spans.

Rules the rest of the domain depends on:

- An **edit span is clean** when all verbatim words in `[span.start - 1, span.end + 1]` are clean. A turn without a verbatim event, or with `low_confidence_reason` set, has no clean spans; its streaming text is used for planning at `clean=false`.
- **Per-vendor thresholds** [DECISION, skeptic review]: `asr.confidence_threshold` is a map by vendor in `packages/languages/<target>/recognizer.yaml`, each value set by the gate's 30-clip check for that recognizer; `clean=true` therefore means the same thing across turns of one session whichever vendor transcribed them. The vendor is stored on the event and copied to every evidence row and comparable segment; the gate's rule 4 fails evidence from an uncalibrated vendor (`clean_evidence`).
- `low_confidence_source=true` (no clean spans regardless of the recognizer) applies only to `calls.kind = dial_in` [P1] turns (PRD-v2 5.4.12) and to turns produced under the 5.4.10 weak-link voice-note fallback (03's `mode = voice_notes` on a failed live call). The small-door voice note and "say it once" uploads are deliberate recordings on a normal link and follow the normal confidence filter (PRD-v2 3.7, 10.2.1) [DECISION, conformance review].
- A session's `evidence_quality` is `full` when at least 80% of learner words are clean, `partial` when 40 to 80%, `text_only` below 40% or when every call turn failed [ASSUMPTION; revised by the week-2 replay of the Milestone 0 transcripts: the cut points move if more than 15% of sessions with a clean analyst output land in `partial`]; `text_only` sessions still produce chat evidence (clean by definition) and planning signals.
- The target language decides the recognizer, the threshold map and the spaCy model; the native language decides nothing here except which clips are talkback (ADR-02).

### 4.2 The analyst

One prompt, one schema, one call per run (D2; the `fast` variant of the first draft went with the notes, ADR-06). `claude-haiku-5-5`, `output_config={"format": AnalystOutput JSON schema, "effort": "low"}` (effort set explicitly so thinking tokens stay small and are counted; the cost middleware logs `usage.output_tokens` including thinking into `vendor_calls`), `max_tokens` 6000, temperature default, the stable prefix cached, `asyncio.wait_for(90)`, Inngest `retries=0`. On the first run of a session the input is the call; on a later run (`chat.closed`, `voicenote.received`) the input is the new events plus the stored `analyst_result` of the earlier runs, and the prompt says "these edits and spans are already recorded; analyze only the NEW section". The validated output is appended as an `analyst_result` event (about 3 KB) so `learner/rebuild` replays it without a vendor call (04 D14) and the calibration set certifies exactly this prompt on exactly these inputs.

Input (`AnalystInput`, compiled by code; the whole learner model is never sent, PRD-v2 8.1 rule 4):

```python
class AnalystInput(BaseModel):
    session_id: UUID; call_id: UUID | None; kind: Literal["first","main","round_two","small_door","chat_only","recording"]
    brief: {grammar_target: {structure_id, label, examples: list[str]}, contrast_pair: ... | None,
            words: [{lemma, sense_key}], recall_gaps: [{id, expected}], necessity_moves: [str], retell_prompt: str | None}
    active_targets: [{structure_id, label}]                     # the "working on" items plus current targets, for recast-uptake priority and the echo plan
    invited_structures: [{structure_id, label, detector_hint}]  # closed list the analyst may mark as "needed": targets + structures the host moves invite + the target package's B1 core set (about 40)
    turns: [{turn_index, speaker: "learner"|"host", text: str, verbatim: bool, clean_spans: [[int,int]], words: [{w, s, e, c}] | None,
             host_moves: {recast: str | None, clarify: bool, recall_gap_id: str | None, retell: bool, talkback_word: str | None}}]
    chat: [{message_id, from: "learner"|"host"|"salma", text}]
    known_patterns: [{structure_id, error_type, count, sessions}]  # the error profile's current patterns, so "repeat" is marked consistently
    produced_before: set[str]                                   # lemmas with a word_uses row (for "new for you")
    prior_results: list[AnalystOutput]                          # earlier runs of this session (empty on the first run); the new section is marked
    learner_name: str; native_language: str; target_language: str   # ADR-02: the pair is a learner fact
```

Output schema (fixed; code validates every quote against the input text before anything is used):

```python
class Edit(BaseModel):
    turn_index: int | None; message_id: UUID | None
    original: str                      # exact substring of the learner's verbatim text (or chat text), minimal span
    corrected: str                     # smallest change that makes it acceptable spoken English; "" for a deletion
    blurred_meaning: bool
    self_corrected: bool               # the learner produced the correct form later in the same turn
    recast_uptake: Literal["repeated","ignored","n/a"]   # when the host recast this form in the previous host turn
    note: str | None                   # at most 12 words, for the human reviewer only

class NeededStructure(BaseModel):      # obligatory context proposal
    turn_index: int; structure_id: str; span: str; realized: bool

class CanDoMoment(BaseModel):
    turn_index: int; quote: str; can_do_id: str   # from the package's can-do list (about 30 ids, e.g. "disagree_with_reason", "narrate_past_event")

class ReachedFor(BaseModel):
    turn_index: int; paraphrase_quote: str; target_word: str; confidence: Literal["high","medium"]

class TargetUse(BaseModel):
    lemma: str; turn_index: int | None; message_id: UUID | None; quote: str; correct: bool   # prompted-ness is NOT the model's: code sets it (4.2 check 7)

class AnalystOutput(BaseModel):
    edits: list[Edit]
    needed: list[NeededStructure]
    target_uses: list[TargetUse]
    uptake: Literal[0,1,2]             # did the call reflect the episode and the article
    uptake_evidence: str               # one quote
    retell: {turn_index: int, done: bool} | None
    recall_gaps: [{id, completed: bool, turn_index}]
    can_do: list[CanDoMoment]          # at most 3
    reached_for: list[ReachedFor]
    new_lemmas_produced: list[str]     # lemmas used that are not in produced_before, with quotes
    flags: {crisis: bool, crisis_quote: str | None, complaint: bool, feels_tested: bool, anxiety_signs: bool, recognition_doubt: bool,
            host_explicit_correction: bool, host_explicit_correction_quote: str | None}   # a host or Salma line that reads as "the correct form is": feeds 09's explicit_corrections_per_100_turns (ADR-06)
    skipped_spans: [{turn_index, text, reason: "garbled"|"native_language"|"unclear"}]
```

Prompt skeleton (the cached prefix is everything before the breakpoint; the Milestone 0 prompt A's analyst rules are carried over nearly verbatim so the calibration set tagged against them stays valid):

```text
[SYSTEM, cached]
You are the analyst of "For one", a {target_language_name} show made for one adult at about B1 whose first language is {native_language_name}. You read what the learner said today and record exactly what it shows, nothing more. Another program checks every quote you give against the transcript; a quote that is not exact is thrown away.
Rules:
- Only the learner's words count. Quote them exactly as given, including fillers.
- Record an error only when you are confident it is the learner's and not a recognition error. Skip garbled or unclear passages and list them under skipped_spans.
- For each error give the smallest change that makes it acceptable spoken English. Nothing stylistic. Never "improve" a correct sentence. One edit per error; split unrelated errors in one sentence into separate edits.
- Mark blurred_meaning when a listener could misunderstand what happened, who, or when.
- Mark self_corrected when the learner says the right form later in the same turn.
- recast_uptake: if the host's previous turn recast this form, say whether the learner repeated the corrected form in this turn.
- needed: for each structure in INVITED_STRUCTURES, list every learner span where that structure was needed (an obligatory context), and whether it was realized correctly. Do not list structures that are not in the list.
- target_uses: every use of a target word with its exact quote and whether it was correct. Do not judge whether it was prompted; the program knows what the host said.
- can_do: at most 3 moments that match a can-do id, with the exact quote. Prefer moments on hard things (disagreeing with a reason, narrating in sequence, hedging).
- reached_for: words the learner searched for, asked for, or talked around; give the English word they needed and quote the paraphrase.
- Patterns to watch for, never to assume, in {native_language_name} speakers' {target_language_name}: {l1_transfer_list}
- flags: crisis is any statement of self-harm intent or serious distress, in either language; quote it. host_explicit_correction: a host or producer line that tells the learner they were wrong or states "the correct form is"; quote it (a recast inside a reply is not one).
- You never write to the learner. You never praise, grade or summarize.
INVITED_STRUCTURES and CAN_DO ids: {target package lists}
<<cache breakpoint>>
[USER]
{AnalystInput as compact JSON}
```

The `{l1_transfer_list}` comes from `packages/native/<native_language>/l1_transfer/<target_language>.yaml` (for `native/ar` and target `en`: missing "be", articles, present perfect against past simple, prepositions, resumptive pronouns, questions without inversion, uncountable plurals, p/b confusion); a native package without a file for the target sends an empty list and the analyst works from the target inventory alone. Nothing in the prompt, the classifier or the stores assumes a first language (ADR-02).

Code checks after the call (`analyst.validate`), each dropping the offending item and counting a `analyst_validation_drop` metric:

1. `original`, `quote`, `span`, `paraphrase_quote`, `uptake_evidence`, `crisis_quote` must be exact substrings (after whitespace normalization) of the named turn's verbatim text or chat message.
2. `corrected` must differ from `original` by at most 4 token edits (errant alignment); larger rewrites are dropped as stylistic.
3. `structure_id`, `can_do_id`, target lemmas must exist in the package lists sent.
4. At most 3 `can_do`, at most 40 edits per session (above that the output is suspicious and the session is marked `analyst_overflow` for review).
5. An edit whose `original` lies in a non-clean span is kept with `clean=false`.
6. `flags.crisis=true` emits `crisis.detected_after_session` immediately, before any other step (PRD-v2 7.9.3); the rest of the pass continues.
7. **Prompted-ness is computed by code** (models propose, code decides; skeptic review): a `TargetUse` or a structure context is `host_prompted` when the lemma or form appears in the two preceding host turns (`call_turns_v`, speaker host), `recall_gap` when the host turn carried `recall_gap_id` for it, `talkback` when a `talkback` event for the lemma precedes it in the session, `say_it_once` inside that exchange, else `unprompted`. The analyst's output carries no `prompted` field.
8. Items already present in `prior_results` (same `source_event_id` and span) are dropped as duplicates before anything else runs.
9. The validated output is appended as `analyst_result {session_id, run_id, trigger_event_id, output, prompt_version}` in the same step; `session_summaries.analyst_run_id` and every claim candidate carry `run_id`.

### 4.3 The edit classifier and obligatory contexts

Normalization first (skeptic review: ERRANT is built for written, punctuated, cased text): both `original` and `corrected` are passed through `normalize()`, which strips the target package's filler list and immediate repetitions (the same pruning as 4.4), restores punctuation and casing with a small restorer model in the worker image (`punctuate` from the target package's tooling list; the verbatim vendor's `format_text` option is requested too, and the raw text stays on the event), and ignores `U:` edits whose only tokens are fillers. Then `errant` aligns `original` to `corrected` (both tokenized with the target package's spaCy model, `en_core_web_sm` for English, the pipeline's lemmatizer, 02 D19) and yields one or more `(operation, errant_type)` pairs such as `(R:VERB:TENSE)`, `(M:DET)`, `(U:PREP)`, `(R:VERB:SVA)`, `(R:NOUN:NUM)`, `(R:WO)`. The target package then maps to the inventory. Every match feature in the table (`corrected_irregular`, `head_noun_countable`, `pron_object`, `sentence_is_question`, ...) is a named Python predicate in `forone.assessment.features` with a unit test; a rule naming an unknown predicate fails CI.

```yaml
# packages/languages/en/structure_rules.yaml (excerpt; ADR-02: one file per target language)
version: 1
categories: [tense_aspect, sva, articles, prepositions, word_order, word_choice, plurals, pronouns, comparatives, conditionals, questions, register]
rules:
  - id: past_simple_irregular_narrative
    label_ar: "الماضي البسيط: الأفعال الشاذة"
    category: tense_aspect
    expected_band: A2
    match:
      errant: [R:VERB:TENSE, R:VERB:FORM]
      corrected_pos: VERB
      corrected_tag: VBD
      corrected_irregular: true           # lemma not in the regular -ed list
      context_any: [yesterday, last, ago, when I, "then"]   # optional booster; not required
    detector:                              # obligatory-context detector, runs on the learner text (not on edits)
      spacy_pattern: [{"TAG": {"IN": ["VBD","VBN"]}}]       # realized contexts
      time_cues: [yesterday, last week, last year, ago, when I was]   # needed contexts the analyst may propose
  - id: present_perfect_vs_past_simple
    category: tense_aspect
    expected_band: B1
    match: {errant: [R:VERB:TENSE], original_tag_any: [VBD, VBP], corrected_contains_any: [have, has, "'ve", "'s"]}
  - id: article_singular_countable
    category: articles
    expected_band: A2
    match: {errant: [M:DET, U:DET, R:DET], head_noun_number: singular, head_noun_countable: true}
  - id: resumptive_pronoun_relative
    category: pronouns
    expected_band: B1
    match: {errant: [U:PRON], original_prev_dep_any: [relcl], pron_object: true}
  - id: question_inversion
    category: questions
    expected_band: A2
    match: {errant: [R:WO, M:AUX], sentence_is_question: true}
  - id: uncountable_plural
    category: plurals
    expected_band: A2
    match: {errant: [R:NOUN:NUM], lemma_in: uncountable_list}
  # v1 (build week 1): the claim-feeding set only, about 30 to 40 B1 core structures (the `invited_structures` list); everything else classifies to a category by the fallback.
  # Growth: from calibration misses and from structures that become targets, not from the Grammar Profile wholesale; the few-hundred-row inventory is a beta-period task (section 7). Seeded from the English Grammar Profile A2 to B2 where permission allows (section 10 #3).
fallback:
  by_errant_prefix: {VERB:TENSE: tense_aspect, VERB:SVA: sva, DET: articles, PREP: prepositions, WO: word_order, NOUN:NUM: plurals, PRON: pronouns, ADJ:FORM: comparatives, OTHER: word_choice}
item_key:                                   # item-based patterns when no structure rule matches (PRD-v2 9.3 "attempting, item-based")
  R:OTHER: {category: word_choice, key: head_lemma}
  R:PREP:  {category: prepositions, key: governing_verb_lemma}   # "depend of" -> (prepositions, depend, R:PREP)
  R:VERB:  {category: word_choice, key: corrected_lemma}
```

Classification returns `(structure_id | None, item_key | None, category, error_type)` where `error_type` is the errant type string. An edit that matches no structure rule keeps its category from the fallback; when the edit's head lemma is identifiable under `item_key` (word choice, collocation, preposition with its verb) it gets an `item_key = (category, lemma_or_chunk, error_type)` so it can become an item-based pattern (4.5.4) and later a `mistake_gone` claim; only true unclassifiables have neither and are slips. Ambiguity is resolved by rule order (most specific first); a rule can declare `requires_target: true` to match only when that structure is a current target.

Obligatory contexts, per structure and session:

```python
def obligatory_contexts(structure, turns, analyst_needed, edits):
    realized = detector_matches(structure, turns)                                   # code: spans where the form appears
    proposed = [n for n in analyst_needed if n.structure_id == structure.id]        # analyst: spans where it was needed
    contexts = dedupe_by_span(realized + [p for p in proposed if structure.detector and cue_present(structure, p.span)])
    # a proposed context survives only if the rule has a detector and one of its cues is in the span: the analyst cannot invent contexts
    for c in contexts:
        c.correct = not any(e.structure_id == structure.id and overlaps(e, c) for e in edits)
        c.clean = span_is_clean(c)
    return contexts
```

The structure map row accumulates `contexts_14d` and `correct_14d` over clean contexts only; unclean contexts are kept in a separate pair for the teacher's view.

### 4.4 Measures (code)

Definitions, computed from `verbatim_words` (`s`, `e` in ms, `c` confidence) with fillers from the package list (`um, uh, er, ah, mm, like (filler), you know`) and repetitions (an identical token repeated within 2 positions) removed to make the pruned token list.

| Measure | Formula | Where |
|---|---|---|
| `speech_rate` | pruned words / total segment seconds × 60 (total time includes pauses) | comparable segments |
| `articulation_rate` | syllables (CMU dictionary lookup, vowel-group fallback) / phonation seconds (total minus pauses ≥ 250 ms) | comparable segments |
| `mlr` (mean length of run) | mean pruned words between silent pauses ≥ 250 ms | comparable segments |
| `mid_clause_pause_rate` | pauses ≥ 250 ms whose position is inside a clause (spaCy: not immediately before a clause-initial token, a coordinating conjunction, or sentence start) per 100 pruned words | comparable segments |
| `first_long_pause_s` | seconds from segment start to the first pause ≥ 2000 ms; used only for the then-and-now sentence "you spoke for 40 s before your first long pause" | recordings, retell |
| `fillers_per_100`, `repairs_per_100` | logged, never weighted (PRD-v2 10.3) | comparable segments |
| `mlc` (mean length of clause) | pruned words / clauses (clause = finite verb heads from the dependency parse: ROOT, ccomp, advcl, relcl, conj with its own finite verb) | comparable segments, chat |
| `subordination_ratio` | subordinate clauses (advcl, relcl, ccomp, xcomp with a subject) / clauses | same |
| `mtld` | McCarthy & Jarvis 2010, factor threshold 0.72, forward and backward averaged, on lemmas; requires ≥ 50 tokens else null | same |
| `beyond_2000_share` | lemmas with frequency rank > 2000 in the package list / content lemmas | same |
| `errors_per_100` (by category and total) | clean edits / clean pruned words × 100 | all clean call turns, chat |
| `oc_accuracy[structure]` | correct clean contexts / clean contexts, 14-day window | structure map |
| `learner_speech_s`, `talk_share` | from `calls.metrics` (03) | session summary |
| `huh_per_min`, `taps_per_100`, `transcript_opened` | from `huh`, `tap`, `transcript_toggle` events over the episode's duration and running words | session summary (the teacher's `huh_rate_2w_median`, 02 assumption 4) |
| `uptake` | analyst 0 to 2 | session summary |
| `talkback_asks` | count of `talkback` events, by lemma | session summary, Skills store |
| `followed_answer` | the one-tap "how much did you follow?" answer after an episode (client event `followed {value 0..3}`), stored as given and compared with the fitter's predicted coverage by 09 (PRD-v2 10.3 comprehension row, 16.2) | session summary |
| `pronunciation` | `say_it_once` and `shadow` event payloads from `call/pronunciation-score` (03 4.10), rolled up as a per-session mean sentence score; internal only | Skills store (`pronunciation_internal`) |

A **comparable segment** row is created for: the retell turn (the learner turn following the host's `retell` move, plus continuation turns until the next host question; `task_type=retell`), round two's first answer turn (`task_type=round_two`), each recording task (`task_type in (rec_retell, rec_opinion, rec_repeat)`). `measurable = (pruned_words >= 40 or seconds >= 30) and clean_share >= asr.segment_clean_min` (placeholder 0.8 [ASSUMPTION], in the target package; a recognizer that hallucinates near long pauses moves speech rate and MLR directly, PRD-v2 10.14), with `unmeasurable_reason` recorded (`too_short`, `low_clean_share`, `uncalibrated_vendor`). Each row stores every measure above, `clean_share`, `verbatim_vendor`, `source_quality` (`live`, `voice_note`, `dial_in`), `difficulty_tag` (from the brief's retell story or the recording form), `assessment_version`.

Repeat task scoring (recording part 3), code only: for each of the 8 sentences, word error rate of the verbatim pruned transcript against the reference after lowercasing and contraction normalization; `score = 4 if wer == 0 else 3 if wer <= 0.15 else 2 if wer <= 0.40 else 1 if wer <= 0.75 else 0` [ASSUMPTION, maps the Milestone 0 rubric to WER bands; checked against Muath's hand scores in week 1]; `ei_total` 0 to 32.

### 4.5 The updater (code)

#### 4.5.1 Word bank

Each lemma (and chunk from the package's formulaic list) has three Beta distributions: `heard ~ Beta(a_h, b_h)`, `read ~ Beta(a_r, b_r)`, `produced ~ Beta(a_p, b_p)`. The mean is the probability the fitter reads (02 assumption 3, `word_bank.p_understood`); the range shown to the teacher is the 10th to 90th percentile.

Prior from the vocabulary-size estimate `V` (word check, else the band prior: B1 = 3,000 families, range 2,000 to 4,500 [ASSUMPTION]). The constants below (`k`, `n0`, the produced factor, the evidence weights) are assumptions, listed in 4.15 with the check that revises each: the week-2 replay of the Milestone 0 learners against Muath's hand-kept word lists (agreement on 80% of `owned` items, 04 §7).

```python
def prior(rank, V, surface):
    k = 1500                                   # softness of the knowledge frontier [ASSUMPTION]
    p = 1 / (1 + math.exp(-(V - rank) / k))
    if surface == "produced": p *= 0.6         # productive lags receptive
    n0 = 4                                     # prior strength in pseudo-observations
    return Beta(a=p * n0 + 0.5, b=(1 - p) * n0 + 0.5)
```

Evidence weights (pseudo-observations added to `a` for positive, `b` for negative):

| Evidence | heard | read | produced |
|---|---|---|---|
| `tap` on the word (transcript or article) | +0 / −3 (transcript) | +0 / −3 (article) | |
| `huh` on a sentence: each of the sentence's two hardest words (lowest prior) | −1 | | |
| Heard in an episode without a tap, with `uptake >= 1` | +0.3 (cap +1.5 per session) | | |
| Read in the article without a tap, `article_scroll` reached it | | +0.3 (cap +1.5) | |
| Word check hit (real word) | +2 | +2 | |
| Word check miss on a real word | −2 | −2 | |
| Unprompted correct production (clean) | +1 | +0.5 | +3 |
| Prompted correct production (host prompt, recall gap) | +0.5 | | +1 |
| Production after talkback or "say it once", same session | | | +0.3 |
| Edit on the word (word choice or form) | | | −2 |
| `reached_for` (talked around it) | −0.5 | | −2 |
| `talkback` ask for the word | | | −1.5 |
| `keep` | (no probability change; sets `kept=true`, scheduled like a target) | | |

Word check scoring (PRD-v2 10.9.1), `word_check.score()`: per band `b` of six, `hits_b` on 6 real items and `fa` false alarms on 12 pseudowords overall; corrected score `s_b = hits_b/6 − fa/12`; vocabulary size `V = sum over bands of clamp(s_b, 0, 1) × band_width` (bands 1,000 to 2,000, 2,000 to 3,000, 3,000 to 4,000, 4,000 to 6,000, 6,000 to 8,000, 8,000 to 10,000, plus the first 1,000 assumed known) with a range of ±(1 − items_answered/48) × 1,500 ± 600 [ASSUMPTION, widened when the check stopped early]. Partial answers count; a learner who skips gets the band prior.

Scheduler grades handed to the data domain's FSRS-style scheduler per item encountered this session: `again` (edit, tap, reached_for, talkback), `hard` (prompted correct), `good` (heard or read without tap, uptake ≥ 1), `easy` (unprompted correct). One grade per item per session, the worst wins.

**Every production is a row** in `word_uses(learner_id, unit_id, event_id, occurred_at, clean, correct, prompted, quote)`, the data domain's table written by this pass through `AfterPassResult.word_evidence` (ADR-19; the twin of `structure_observations`); `produced_before()` and the owned rule are queries over it, so the notebook's "words you own" opens to the exact turns. With two or three sessions a day (ADR-04) the rows simply accumulate per session; the 20-hour rule below is what keeps "a day apart" meaningful.

**Words owned** (PRD-v2 10.6): `owned_at` is set when the word has ≥ 2 `word_uses` rows with `clean and correct and prompted = false` in different sessions whose `occurred_at` differ by ≥ 20 hours [DECISION: "a day apart" as 20 h so an evening session and the next morning's count], and no edit on the word in the later of the two. The learner's own sentences for the notebook are the two quotes. `owned_at` is never cleared (the two sentences were real), but when ≥ 2 clean edits on the word occur after ownership the row gets `shaky_since` and the notebook shows the word with its later sentence rather than silently keeping the old claim; law 1 bans game furniture, it does not say evidence may never be revised, and a standing untrue "words you own" line would break trust promise 1 [DECISION, skeptic review; the visual treatment is 06's and the wording is OPEN for Muath, section 10 #5].

#### 4.5.2 Structure map

Per structure: `state`, `contexts_14d`, `correct_14d`, `contexts_total`, `first_attempt_at`, `avoidance_flag`, `targeted_sessions[]`, `consecutive_targeted`, `examples[3]` (clean quotes), `lifecycle` (`none`, `active`, `taking`, `stable`, `recheck_2w`, `recheck_4w`, `recheck_8w`, `confirmed`), `stable_since`, `confirmed_by_recording_id`.

#### 4.5.3 The state machine

```text
not_seen ──heard in an episode or article (fitter's realized spans)──► heard
heard ──any clean context (correct or not)──► attempting
attempting ──teacher picks it (plan.targets.grammar)──► active   (lifecycle=active; the state stays attempting)
active ──TAKING rule──► taking
taking ──STABLE rule──► stable (lifecycle=stable, stable_since=now)
stable ──next recording: oc_accuracy on the recording's contexts >= 0.8 with >= 2 contexts──► confirmed
stable/confirmed ──re-check at stable_since + 14d, 28d, 56d: window accuracy < 0.8 or a new pattern on it──► active (lifecycle back to active, teacher told)
any ──no context in 60 days──► unchanged (nothing decays; counts only grow)

TAKING: >= 2 clean correct unprompted contexts in 2 different sessions, and at least one of them >= 20 h after the last session in which the structure was targeted.
STABLE: over a window >= 14 days ending now: contexts_clean >= 5 and correct/contexts >= 0.8 and no new pattern on this structure in the window.
```

"Unprompted" for a structure: the context is not within the two turns after a host recast of the same structure, not inside a nudge exchange, and not the "say it once" repetition.

#### 4.5.4 Error versus slip

```python
def update_patterns(error_profile, edits_this_run, session_id) -> list[ErrorObs]:     # pure: returns observations for AfterPassResult
    out = []
    for e in edits_this_run:
        if not e.clean or e.self_corrected:
            out.append(ErrorObs(kind="slip", edit=e)); continue                   # stored, shown to the teacher as slips, never targetable
        if e.structure_id is not None:   key = ("structure", e.structure_id, e.error_type)
        elif e.item_key is not None:     key = ("item",) + e.item_key              # (category, lemma_or_chunk, error_type), 4.3
        else:                            out.append(ErrorObs(kind="slip", edit=e)); continue
        out.append(ErrorObs(kind="pattern_obs", key=key, id=uuid5(NS, f"{session_id}:{e.source_event_id}:{e.span}:{key}"),
                            session_id=session_id, quote=e.original, corrected=e.corrected, blurred=e.blurred_meaning,
                            recast_uptake=e.recast_uptake))
    return out
# applied by stores.apply_after_pass: row.pattern = count_clean >= 3 and sessions >= 2 (PRD-v2 10.5), blurred_share, examples = last 3 clean,
# last_recast_outcome = the most recent recast_uptake on the key; the observation id makes a replay idempotent (04 §4.3.2)
```

Item-based keys (`item_patterns`) follow the same 3-across-2 rule and reach the teacher beside `error_profile` so the PRD's item-based treatment (recast, then the item returns on schedule, PRD-v2 9.3) has input; a resolved item pattern can become a `mistake_gone` claim like a structure. The teacher's `error_profile` input (02 4.3) receives rows with `pattern=true` as targetable and rows with `pattern=false` tagged `slip`; its prompt rule "an error pattern qualifies only after 3 observations across 2 sessions" is therefore satisfied by data, not by the model's counting. Chat edits are clean by definition and count. A pattern that the learner vetoed in "working on" keeps counting but carries `vetoed=true`; it returns to targeting only if `blurred_share > 0.5` (PRD-v2 9.2.5 "unless it breaks meaning").

#### 4.5.5 Avoidance (weekly)

Runs inside the first `after-pass` after the start of the learner's local week (Monday 00:00 in `learners.tz`; the `apply` step checks `last_avoidance_check < start_of_local_week`), never in the live path and never on a timezone fixed for everyone (ADR-16). It stays P0 and ships in build week 5 (conformance review: PRD-v2 10.7 is untagged, so it is P0, and it is about 20 lines once the structure map exists):

```python
expected = [s for s in inventory if band_index(s.expected_band) <= band_index(skills.speaking.band_low)]
window = sessions_with_speech(last_21_days)
for s in expected:
    if len(window) < 5: break
    opportunities = count(analyst_needed(s) in window) + count(necessity_moves_for(s) in window briefs)
    attempts = structure_map[s].contexts_total_in(window)
    structure_map[s].avoidance_flag = opportunities >= 3 and attempts == 0
```

A flagged structure enters the teacher's input with `avoidance=true`; treatment is the teacher's (PRD-v2 9.3 "avoided" row). The flag clears on the first attempt.

#### 4.5.6 Skill estimates

Internal scale 0 to 100 with CEFR bands A1 10 to 25, A2 25 to 40, B1 40 to 55, B2 55 to 70, C1 70 to 85, C2 85 to 100 [ASSUMPTION, GSE-like grain; the external test (4.12) re-fits the band edges]. Each skill is `N(mu, var)`; the range shown is `mu ± 1.64·sd` (90%).

**Beta scope** [DECISION, skeptic review: the four feature tables delivered nothing learner-facing in the beta and their anchors were unpublished]. One scalar per skill, moved by the observations below with fixed `R`; the full feature tables (`huh_per_min` relative to predicted coverage, read time against band norms, `subordination_ratio`, `beyond_2000_share`, chat `mlc`) are P1 after the first external-test correlations exist (4.12) and are listed in section 7 under the beta period.

| Skill | Beta observation `z` | R |
|---|---|---|
| speaking | mean of two anchored features over the session's clean call turns when ≥ 80 clean pruned words: `errors_per_100` and `mlr`, mapped by the anchor table below | 100 (sd 10); 64 from a recording's rater band only while `calibration_runs.passed = true` for the rater, else the recording's code measures at 100 and the band is stored as advisory |
| listening | the word check (`(V − 3000)/200` points on the prior) and the A3 comprehension line (`heard_it` 0 or 1 → 40 or 55) | 196 (A3), word check moves the prior directly |
| reading | the word check only | n/a (prior move) |
| writing | chat `errors_per_100` through the same anchor row as speaking, when ≥ 60 learner words in the chat | 100 |

Anchor table (`packages/languages/<target>/skill_anchors.yaml`, linear interpolation between anchors; [ASSUMPTION, refit by the external test's isotonic fit, 4.12]) for English:

| Feature | 30 (A2 low) | 40 (A2/B1) | 50 (B1) | 60 (B2 low) | 70 (B2/C1) |
|---|---|---|---|---|---|
| `errors_per_100` (clean edits per 100 clean pruned words) | 12 | 8 | 5 | 3 | 1.5 |
| `mlr` (pruned words between pauses ≥ 250 ms) | 3.0 | 4.0 | 5.5 | 7.0 | 9.0 |

Update: `K = var / (var + R); mu += K·(z − mu); var = (1 − K)·var + Q` with process noise `Q = 2` per observation (lets the estimate move slowly) and `var` capped at 225. Prior at onboarding: `mu` from the band prior (B1 = 47), `var = 225`; the two English moments in A3 give the first listening observation (above) and the first speaking observation (the production line's `errors_per_100` and `mlr` at `R = 196`, PRD-v2 2.2); the first call gives the next speaking observation with `R = 196`. Each observation is applied once (the run rules in 3.4: the chat run contributes only the writing observation).

`skill_answer()` returns, per skill, the passed `skill_range` claim (4.8.1) or `None`. A `skill_range` candidate is generated after every run for each skill with `skill_calibration[skill].calibrated = true` (rater QWK ≥ 0.7 per skill, 4.9 step 5); it carries the band range `mu ± 1.64·sd` mapped to the two nearest band labels and the package's real-situation descriptor, and it goes through the gate like every other claim (rules 1 to 3 n/a by kind; rule 4: the sessions behind the estimate are clean; rule 5: openable to the words owned, the tape and the two most recent comparable segments). `salma_explain` (Salma's on-demand role, ADR-06) speaks only that sentence and can open "how we know"; when there is no passed claim Salma says she cannot say reliably yet (PRD-v2 10.8.3). [DECISION, conformance review: the first draft bypassed `claims` here, against law 12 and PRD-v2 10.10.]

### 4.6 The memory keeper

One Haiku 5.5 call with structured output (`effort: low`, `retries=0`), then rules. Input: the learner's verbatim turns and chat after the watermark, the onboarding fact cards (first run only), current facts (text, status, fact_type, expires_at), interests (topic, salience), goals, canon (last 30 entries), the sensitive-class list. Output is a list of candidates in `AfterPassResult.fact_candidates`, `interest_signals`, `goal_signals`, `canon`, `out_in_world` (04 §4.3.0); the data domain's validator and ladder apply them. `out_in_the_world` rows live in 04's `out_in_world` store and reach the proof and the finale through `briefs.compile('proof')` (PRD-v2 11.2.2, 12.3).

```python
class FactCandidate(BaseModel):
    text: str                          # the fact in third person, Arabic or English as said
    quote: str                         # exact substring of a learner turn or chat message
    turn_index: int | None; message_id: UUID | None
    fact_type: Literal["job","city","people","event_dated","interest","preference","health","money","relationship","religion","politics","other"]
    event_date: date | None            # for event_dated: becomes a follow-up
    supersedes_fact_id: UUID | None
    dont_bring_up: bool                # learner said so
class MemoryOutput(BaseModel):
    facts: list[FactCandidate]
    interests: [{topic, signal: "mentioned"|"enthusiastic"|"dismissed", quote}]
    goals: [{can_do_text, quote}]      # only when the learner states a real situation
    canon: [{kind: "position"|"story"|"joke"|"side_character", text, quote}]
    out_in_the_world: [{text, quote, date_hint}]
    corrections: [{fact_id | None, quote, what_is_wrong}]   # "that's not right" moments
```

Rules in code (PRD-v2 8.4):

1. **Quote check:** `quote` must appear word for word in the named verbatim turn or chat message; else the candidate is dropped and counted. Life facts from unclean speech spans are stored at `confidence=said_once` but can only climb the ladder through a chat, a notebook view, or a second clean mention.
2. **Ladder:** new fact → `said_once` (never spoken; notebook "I think..."). An existing `said_once` fact matched by text similarity (embedding cosine ≥ 0.85 [ASSUMPTION], Google's embedding model under ADR-10, on the same `fact_type`) in a different session → `usable`. A `fact_card_edit` or `notebook_edit` event → `ground_truth`. A notebook card viewed and left unedited for 48 h → `usable` (the client emits `fact_card_viewed {fact_ids}`, 04 §4.3.6). **Onboarding** [DECISION, conformance review; PRD-v2 2.3, 3.4, 8.4.2]: an A3 fact card shown to the learner and not removed before A9 counts as "viewed and left unedited" (the card is the notebook view) and enters at `usable` at account creation; a card edited with ✎ enters at `ground_truth`; a card removed with ✕ is never stored. This is what makes the day-2 verbatim callback and Today's first host line possible. Sensitive-class cards still need the explicit confirmation of rule 3.
3. **Sensitivity:** `fact_type in (health, money, relationship, religion, politics)` → `sensitive=true`. A sensitive candidate is held in `pending_confirmation`, which is not shown as "I think...", is never in a brief, and expires after 7 days unconfirmed; it becomes `usable` only when the learner confirms by chat, by the notebook card or by the in-session verbatim "yes" (section 10 of 10-decision-records, item 1, asks counsel whether that is explicit consent); a second spontaneous mention does not count. A confirmed sensitive fact is usable for a brief only inside the local week in which it was raised [DECISION, PRD-v2 5.1 "that week" over 8.4.3 "that session"]; the teacher's `facts_usable` filter (02) excludes it after that week.
4. **Shelf life** by `fact_type` from the native package's defaults (`job` 180 d, `city` 365 d, `people` 365 d, `event_dated` until `event_date + 14 d`, `health` 7 d, `preference` 120 d, `relationship` 365 d, `money` 90 d, `religion` and `politics` the raising week only (rule 3, no shelf life beyond it), `other` 120 d [ASSUMPTION for the five the PRD does not list], `interest` handled by salience); expired → `dormant`, never spoken, kept.
5. **Supersede:** `supersedes_fact_id` sets the old fact `superseded` and links history.
6. **Follow-ups:** one row per `event_dated` fact, `due_at = event_date + 1 d`, state `pending → used → history`; the teacher consumes `follow_ups_due`.
7. **Interests:** salience `+0.3` on `mentioned`, `+0.6` on `enthusiastic`, `−0.5` on `dismissed`, decays `×0.93` per week without engagement; below 0.2 → `dormant`; a mention wakes it.
8. **Canon** rows are appended with the session id; the pipeline's series bible reads them (02 D14).
9. **Corrections** go straight to `memory/correct` (4.14) with the quote as evidence.

The memory keeper never infers: a candidate whose `quote` does not itself state the fact (the model "concluded" it) fails the quote check by construction, because the check is on the quote, and a second rule rejects facts whose text contains tokens absent from the quote beyond a stop-list and inflections (`text_overlap >= 0.6`).

### 4.7 Corrections after the call: nothing is shown, and what the pass extracts instead (ADR-06)

#### 4.7.1 What was removed

decisions.md §3 (2026-10-23) made teaching invisible: the hosts correct inside the conversation with a recast ("oh, you went there yesterday?") and never with "the correct answer is"; Salma, the producer, explains when asked and never corrects. The first draft of this section built Salma's three-card notes within 90 s, the polish card with its "say it once" line, and the chat margin note. All of it is removed: the `notes` and `margin_notes` tables, `chat/margin-note`, the `fast` analyst, `notes.ready`, `note_shown`, `notes_mode`, the polish-line TTS, the notes door and the margin chip (06), the notes budget (15), the notes cost line (08) and the `notes_late` alert (09). A flag was not kept (10-decision-records §8: a flag never changes a law). What stays of PRD-v2 5.5 and 10.12 is the evidence underneath: the pass still extracts every word use, structure observation, can-do moment, reached-for word and recast outcome, for the teacher's plan and for the weekly proof.

#### 4.7.2 Recast evidence and the echo plan input (code)

The only correction channel is the conversation. The teacher's echo plan (02) decides which of the learner's recurring errors the host should recast in the next call and which right forms the next episodes carry; the host brief's `recasts` field (03) carries it live. This pass supplies the evidence:

```python
class EchoPlanInput(BaseModel):                      # echo_plan_input(learner_id); compiled into TeacherInput by briefs.compile('teacher') (04)
    recurring: list[{key: PatternKey, right_form: str, examples: list[str], blurred_share: float,
                     last_recast_at: datetime | None, last_recast_uptake: Literal["repeated","ignored","n/a"],
                     recasts_last_14d: int, uptake_rate_14d: float | None, vetoed: bool, in_working_on: bool}]
    self_corrections_14d: int                        # monitoring evidence, PRD-v2 10.2.2
    forms_to_carry: list[{structure_id | lemma, right_form, example_quote}]   # right forms the episodes should model, from patterns and reached_for
```

`recast_uptake` comes from the analyst per edit (4.2) and is checked by code against the preceding host turn's `recast` payload in `call_turns_v`; a recast the host did not make (per the event) cannot have an uptake. Vetoed patterns stay in the list with `vetoed=true` and the teacher may recast them only when `blurred_share > 0.5` (PRD-v2 9.2.5). Nothing here reaches the learner.

#### 4.7.3 Law scan (code)

One scanner, `law_scan(text, allowed_slots, native_language)`, used on every learner-facing sentence this domain produces or feeds: the proof script (4.11.1), the finale narration (4.11.4), `salma_explain`'s answers (4.7.4), and in CI on the rendered claim-template set (4.8.5). It rejects: any digit, Western or Eastern Arabic (`[0-9٠-٩]`), and any number word from the native package's list (`packages/native/<lang>/law/number_words.yaml`) outside the allowed slots; any banned lesson word from the native and target packages (for `native/ar` and `lang en`: `درس`, `اختبار`, `مستوى`, `واجب`, `نسبة`, `درجة`, `lesson`, `test`, `level`, `homework`, `score`, `percent`); any progress verb outside a claim sentence (`تحسنت`, `تقدمت`, `improved`, `better than`); a claim sentence altered (string equality against `claims.text_ar`); a missing AI signature where the surface requires one. Allowed slots are declared by the caller: for the proof, the pasted claim sentences and the three cumulative-count slots; for `salma_explain`, the `skill_range` sentence (whose band labels are the one place a level word is permitted, decisions.md §4 f) and claim sentences; for the finale, the claim sentences and the recap counts. Unit tests cover Eastern digits and number words.

#### 4.7.4 "New for you" and `salma_explain`

"New for you" is a card on Today and in the notebook (06), not a note after the call: it renders the most recent passed `did_it` or `first_ever` claim (`rank: structure first_ever > can_do hard > word first unprompted`) with its exact quote and, when voice storage is on, ▶ by byte range from the turn's `call_turn` media; with storage off, text only. It appears when the pass completes (minutes after the call, not within 90 s) and is marked shown through `claim_shown`. Because the claim passed the full gate after the classifier ran, a structure `first_ever` is never a model's judgment alone (the first draft's stage-1 card was; conformance review).

`salma_explain` is Salma's on-demand role (Sonnet 5.5, 03 and 06 own the surface and the prompt; 08 prices it under "Salma (when asked) and chat"). This domain feeds it `skill_answer()`, `claims_passed()`, `active_targets_with_evidence()` and the notebook's rows, and every answer passes the correction guard (07) and the law scan before it is spoken. Salma explains what a claim rests on, what "working on" means, and where the learner stands when asked; she never corrects a sentence and never introduces a progress statement that is not a claim row.

#### 4.7.5 The measure

`explicit_corrections_per_100_turns` (09; ceiling 0) counts host and Salma turns that read as an explicit correction per 100 host turns. It has two detectors: the correction guard in `guard.check_output` (07, with the per-language phrase list `guard/correction_words.yaml`), counted in `moves.violations` live, and this pass's `flags.host_explicit_correction` with its quote (4.2), which catches what the phrase list missed. This domain writes `session_summaries.explicit_corrections` (count, with the quotes in `energy_signals`-style detail for review) and 09 computes the measure from it and from `moves`. Any non-zero reading opens a review item with the quote, the prompt version and the brief.

### 4.8 The claim gate (code)

#### 4.8.1 Claim kinds

| kind | Statement shape | Minimum history | P |
|---|---|---|---|
| `did_it` | "You disagreed with Karim and gave a reason" (a can-do moment on a structure or can-do at or above the learner's band) | none (A8 onward), but once per `can_do_id` per learner: no passed or shown `did_it` with the same `can_do_id` may exist, so it is a first-ever event by construction and rule 3's exemption is honest (`claims.did_it.once_per_can_do = true`) [DECISION, conformance review, PRD-v2 5.5.2.1 "had not done before"] | P0 |
| `first_ever` | "First time you used *should have* on your own" (structure: first clean correct unprompted context; word: first clean unprompted use) | the structure or word had ≥ 1 prior session of exposure with no correct unprompted use | P0 |
| `word_owned` | "*Negotiate* is yours now: Tuesday you said ..., today you said ..." | the owned rule (4.5.1) | P0 |
| `mistake_gone` | "*I go yesterday* has not come back since 2026-12-14" | structure `confirmed` (stable and held in the next recording) and the pattern had ≥ 3 observations | P1 |
| `fluency_change` | "You spoke for 40 seconds before your first long pause; in week 1 it was 12" / `mlr`, `speech_rate`, `mid_clause_pause_rate` | `metric_calibration` row usable; ≥ 2 comparable segments each side | P1 |
| `complexity_change` | `subordination_ratio`, `mlc`, `beyond_2000_share` | same | P1 |
| `accuracy_change` | `oc_accuracy` for one structure, or `errors_per_100` on a category, always with the attempted count beside it | same; ≥ 5 contexts each window | P1 |
| `accuracy_fell_while_trying` | "More mistakes this week because you tried the past perfect eleven times; in October you never tried it" | a worse `accuracy_change` whose attempts rose ≥ 2× | P1 |
| `talkback_falling` | "Four talkback asks this week; in week 1, fifteen" | ≥ 3 weeks of calls, change beyond noise | P1 |
| `then_and_now` | the finale's measured differences (a `fluency_change`, `complexity_change` or `accuracy_change` whose two data points are consecutive recording sittings) | two sittings; rule 3 is **not** waived: the difference must hold beyond threshold on both recording tasks (`rec_retell` and `rec_opinion`), or on one task plus the weekly retell segments of the same window, and the pinned rater's band must not move the other way [DECISION, PRD-v2 10.10 rule 3 exempts only first-ever events; Milestone 0 kit 06 gate rule 2] | P1 |
| `skill_range` | "Listening around B1; speaking just below" with the real-situation descriptor, the answer to "where do I stand" (decisions.md §4 f) | `skill_calibration[skill].calibrated` (rater QWK ≥ 0.7 per skill); rules 1 to 3 n/a by kind; one live row per skill, superseded by the next | P0 |

Every claim row carries `evidence` (04's `claims.evidence` plus this domain's `claim_evidence` rows, 4.16): the event ids, quotes, media byte ranges, segment ids and the numbers, so "how we know" is a render of the row.

#### 4.8.2 The gate

```python
NOISE_K = config("claims.noise_multiplier", 2.0)          # PRD-v2 10.10 rule 2, for the top-ranked candidate of a proof or finale
NOISE_K_REST = config("claims.noise_multiplier_rest", 2.8) # every further metric candidate in the same proof or finale (multiple comparisons)
MIN_PAIRS = config("claims.min_test_retest_pairs", 20)     # D11: 20 is the bar; 12 to 19 is provisional (sem carries ±21% relative error at 12)
LIKE_FOR_LIKE = {                                          # rule 1: which task types may be compared
    "retell": {"retell"}, "round_two": {"round_two"}, "rec_retell": {"rec_retell"}, "rec_opinion": {"rec_opinion"}, "rec_repeat": {"rec_repeat"},
    "call_turns": {"call_turns"}, "chat": {"chat"},        # accuracy and talkback kinds: counts over the window, analytic SE
}
EVENT_KINDS = ("did_it", "first_ever", "word_owned", "skill_range")

def gate(c: ClaimCandidate, *, rank_in_family: int = 0) -> GateResult:
    # Rule 4 first because it is cheapest and most often fails: clean evidence
    if c.kind in GRAMMAR_KINDS and not all(ev.clean for ev in c.evidence):            return fail(c, "clean_evidence")
    if any(ev.source_quality in ("dial_in", "voice_note_fallback") for ev in c.evidence): return fail(c, "clean_evidence")   # PRD-v2 5.4.12, 5.4.10
    if any(ev.is_speech and (ev.verbatim_event_id is None or ev.vendor_threshold is None) for ev in c.evidence):
                                                                                        return fail(c, "clean_evidence")   # no verbatim event, or an uncalibrated vendor (4.1)
    if any(ev.disputed for ev in c.evidence):                                          return fail(c, "clean_evidence")   # a quote_disputed event names it (4.14)
    # Rule 5: openable
    if not all(ev.openable() for ev in c.evidence):                                    return fail(c, "openable")        # quote exists in the log; audio range exists, or the kind allows text (OPENABLE_TEXT_OK)
    if c.kind == "did_it" and claims_exist(c.learner_id, kind="did_it", can_do_id=c.subject.can_do_id, passed=True):
                                                                                        return fail(c, "repeated_can_do") # once per can_do (4.8.1)
    if c.kind in EVENT_KINDS:                                                           # rule 3 exempts first-ever events; rules 1 and 2 do not apply to events
        return passed(c, rules={"like_for_like": None, "beyond_noise": None, "repeated": None, "clean": True, "openable": True})
    # Rule 1: like for like
    if not c.before.task_type in LIKE_FOR_LIKE[c.after.task_type]:                     return fail(c, "like_for_like")
    if c.kind == "then_and_now" and c.before.form == c.after.form:                     return fail(c, "like_for_like")   # same stimulus would be memory, not growth
    if c.before.measures_version != c.after.measures_version:                          return fail(c, "like_for_like")   # D12: never across a change of the measures code
    if c.before.difficulty_tag != c.after.difficulty_tag and c.kind != "then_and_now": return fail(c, "like_for_like")   # pseudo test-retest only within one difficulty tag
    if c.kind in ("accuracy_change", "accuracy_fell_while_trying") and (c.before.contexts < 5 or c.after.contexts < 5):
                                                                                        return fail(c, "like_for_like")
    # Rule 2: beyond the noise
    cal = metric_calibration.get(c.metric, c.after.task_type)                           # source = 'test_retest' (fluency, complexity) or 'analytic' (accuracy, talkback)
    if cal is None or (cal.source == "test_retest" and cal.n_pairs < MIN_PAIRS):        return fail(c, "no_standard_error")  # PRD-v2 10.10: until SE exists, only events
    sem = cal.sem if cal.source == "test_retest" else analytic_sem(c)                   # binomial on correct/contexts; Poisson on asks per call; see below
    k = NOISE_K if rank_in_family == 0 else NOISE_K_REST
    threshold = k * sem
    if abs(c.after.value - c.before.value) < threshold:                                return fail(c, "beyond_noise")
    # Rule 3: repeated: at least two data points point the same way (no kind is waived)
    sign = math.copysign(1, c.after.value - c.before.value)
    if c.kind == "then_and_now":
        if not (c.other_task_point and math.copysign(1, c.other_task_point.diff) == sign and abs(c.other_task_point.diff) >= threshold) \
           and not corroborated_by_weekly_retells(c, sign, threshold):                   return fail(c, "repeated")
        if c.rater_band_diff is not None and math.copysign(1, c.rater_band_diff) == -sign: return fail(c, "repeated")     # the pinned rater moved the other way
    else:
        recent = c.after_points                                                         # the two most recent comparable segments or the two most recent weekly counts
        if len(recent) < 2 or len(c.before_points) < 2:                                return fail(c, "repeated")
        if not all(math.copysign(1, p.value - c.before.value) == sign and abs(p.value - c.before.value) >= threshold for p in recent):
                                                                                        return fail(c, "repeated")
    return passed(c, rules={"like_for_like": True, "beyond_noise": True, "repeated": True, "clean": True, "openable": True, "se_used": sem, "k_used": k})
```

**Analytic standard errors** [DECISION, conformance review; PRD-v2 10.10 rule 2 names test-retest pairs for the metrics that have them and is silent on counts]: `accuracy_change` compares two proportions `correct/contexts`; `analytic_sem = sqrt(p1(1−p1)/n1 + p2(1−p2)/n2)`; `talkback_falling` compares two rates of asks per call, `analytic_sem = sqrt(r1/c1 + r2/c2)` (Poisson). The rows `metric_calibration(metric, task_type in ('call_turns','chat'), source='analytic', sem=null)` exist so the audit can see which rule applied, and every claim records the `sem` and `k` it was judged against in `gate.se_used`, `gate.k_used`.

**Multiple comparisons** [DECISION, skeptic review]: a weekly proof or a finale is one family of candidates. `generate_weekly` and `generate_then_and_now` rank the metric candidates (by effect size over `sem`), and the gate admits the top-ranked one at `K = 2.0` and every further one at `K = 2.8` (`rank_in_family`). With 3 to 5 metrics × 2 tasks per finale and rule 3 no longer waived, the expected false-pass rate per finale falls from about 25 to 40% to under 5%, which is the 16.1 audit target. Expected false-pass rates per kind are recorded in 4.8.4 so the audit has a target per kind.

Candidate construction, per metric kind: `before` = mean over the two earliest measurable comparable segments of the same `task_type` and `difficulty_tag` in the comparison window (weekly proof: the previous 2 weeks against this week; finale: the previous sitting), `after` = mean over the two most recent; `before_points`, `after_points` are those segments. A window with fewer than two measurable segments on either side produces no candidate. Candidates are deduped by `(kind, subject, source_event_id)` across runs of the same session and across the chat and call runs.

**`test_retest_pairs` and `sem`** (the writer the first draft lacked; skeptic review): `calibration/pairs-daily` (03:00 UTC, ADR-16) builds pairs per task type under explicit rules and recomputes `metric_calibration`. Recordings (`rec_retell`, `rec_opinion`): two sittings of the same learner 3 to 5 days apart on **different** forms (repeating a form measures practice, not noise), `source='beta_retest'`, plus the Milestone 0 week-0 re-takes (`source='m0'`, with `long_opinion=true` where the task was the kit's 2-minute version, section 10 #1). Retell and round two: consecutive sessions 2 to 7 days apart with the same `difficulty_tag`, stated as **pseudo test-retest** (`source='pseudo'`; differences include topic variance, so `sem` is conservative, which is the safe direction). `sem = sd(x2 − x1) / √2` over the pairs; `n_pairs`, `sem`, `computed_at`, `measures_version` are stored. The row's key is `(metric, task_type, measures_version)`, not the full `assessment_version`, so a bump of the analyst prompt or the rule table does not close metric claims again (the measures module is versioned separately, `code_versions.measures`). A metric is claimable at 20 pairs (`MIN_PAIRS`); from 12 to 19 the row is `provisional=true` and the gate still fails `no_standard_error`, while `/admin/gates` (09) shows how close each metric is.

Direction: a candidate is generated for both improvement and decline. Declines pass the same gate and are stored as `direction=worse`; the proof producer must phrase them with the supported reason (`accuracy_fell_while_trying` when attempts rose, `harder_task` when the segment's difficulty tag is higher, `long_gap` when `days_since_session >= 5` preceded the window, else `unknown` → the proof says "a worse week on X, and I cannot say why yet"). The honest fallbacks when nothing passes are chosen in `proof/make`, not here (4.11.2).

#### 4.8.3 Status lifecycle, on the data domain's table

The `claims` table is 04's (D13; its DDL in 04 §4.10) and this document no longer carries one [DECISION, skeptic blocker]. Mapping of the first draft's statuses onto 04's columns: a candidate that passes is written by `stores.record_claim(ClaimIn)` with `gate = {like_for_like, beyond_noise, repeated, clean, openable, se_used, k_used}` (nulls where a rule is n/a by kind), `kind` from this document's enum (04 adopts it; the first draft's `words_owned`, `structure_learned`, `fluency`, `accuracy`, `complexity`, `can_do`, `flat`, `worse` map to `word_owned`, `mistake_gone`, `fluency_change`, `accuracy_change`, `complexity_change`, `did_it`, and `flat` and `worse` are not kinds but proof situations and a `direction`), `text_ar` rendered by code from the template (4.8.5), `learner_model_version` and `gate_version` (`assessment_version`). `shown_at`, `shown_surface`, `shown_event_id` are set once by 04's `mark_claim_shown` on `claim_shown {claim_id, surface}`. A retraction is a `claim_invalidations` row (`reason`: `rebuild:{version}` or `learner_disputed`) written by 04's `learner/rebuild` or by `memory/correct` through `stores.invalidate_claim`; `invalidated_at` is set, the row is never deleted, and `told_at` is set when the next proof carried the one honest line (PRD-v2 8.5; `invalidated_untold` in the proof brief). A candidate that fails is not a claim: it goes to this domain's `claim_candidates` table with `failed_rule`, kept 90 days for the audit, then purged. `direction` (`better`, `worse`, `event`) and the worse-week `reason` live in `claim_evidence`'s header row (4.16) so 04's DDL needs no column for them [ASSUMPTION: 04 keeps `claims` as in its §4.10 and accepts the enum].

#### 4.8.4 Thresholds in one place

| Key | Default | Source |
|---|---|---|
| `claims.noise_multiplier` / `claims.noise_multiplier_rest` | 2.0 / 2.8 | PRD-v2 10.10; the family correction (4.8.2) [DECISION] |
| `claims.min_test_retest_pairs` / `claims.provisional_from` | 20 / 12 | D11 [ASSUMPTION; revised when `calibration_runs` show the sd of `sem` across bootstrap samples under 10%] |
| `claims.did_it.once_per_can_do` | true | 4.8.1 |
| `claims.expected_false_pass` per kind | event kinds about 0 (rules 4 and 5 only); single metric top-ranked 0.046 two-sided per candidate, further ones 0.005; finale family under 0.05 | binomial arithmetic on the gate's thresholds; the 16.1 audit target |
| `claims.min_contexts_accuracy` | 5 | PRD-v2 10.6 |
| `claims.owned.min_sessions` / `owned.min_hours_apart` | 2 / 20 | PRD-v2 10.6 |
| `claims.first_ever.min_prior_sessions` | 1 | D |
| `claims.did_it.min_band_offset` | 0 (at or above the learner's `band_low`) | PRD-v2 2.2 A8 "not easy" |
| `claims.stable.window_days` / `stable.min_contexts` / `stable.min_accuracy` | 14 / 5 / 0.8 | PRD-v2 10.6 |
| `claims.recheck_days` | [14, 28, 56] | PRD-v2 10.6 |
| `claims.finale.max_differences` | 2 | PRD-v2 11.2 |
| `claims.failed_retention_days` | 90 | audit |
| `asr.confidence_threshold[vendor]` | 0.70 placeholder for the primary; none for an uncalibrated vendor | the language gate's 30-clip check per recognizer (ADR-03), `packages/languages/<target>/recognizer.yaml` |
| `asr.segment_clean_min` | 0.8 [ASSUMPTION] | 4.4 |
| `measures.pause_ms` / `measures.long_pause_ms` | 250 / 2000 | research norm [ASSUMPTION] |
| `measures.min_segment_words` / `min_segment_s` | 40 / 30 | D6 |

#### 4.8.5 The claim templates: the only progress sentences any surface may speak

Templates live in the native-language package, `packages/native/<lang>/claims/templates.yaml` (ADR-02), one per kind and direction, with named slots that code fills from the claim row; the model never writes or rephrases them, and the proof producer, the finale writer and `salma_explain` paste `text_ar` by string equality. The law scan runs on the rendered set in CI with every slot filled by a fixture (the "zero progress sentences outside `claims`" exit criterion, section 7). The pilot set for `native/ar` (Gulf colloquial, Salma's register; the Milestone 0 prompt F sentence "في التسجيل الأول وقفت ٦ مرات وسط الجملة، هالمرة مرتين" is the model). The column is 04's `text_ar`; this document recommends it be renamed `text_native` with `native_language` beside it when 04 revises (section 9 #4).

| Kind, direction | Slots | Template (`native/ar`) |
|---|---|---|
| `did_it` | `can_do_ar` (package descriptor in the past tense), `quote` | «{can_do_ar}: قلت "{quote}"» e.g. «خالفت كريم وعطيته سبب: قلت "I don't think so, because..."» |
| `first_ever`, structure | `form`, `quote` | «أول مرة تستخدم "{form}" من نفسك: "{quote}"» |
| `first_ever`, word | `lemma`, `quote` | «أول مرة تقول "{lemma}" بدون ما أحد يذكّرك: "{quote}"» |
| `word_owned` | `lemma`, `day_1`, `quote_1`, `quote_2` | «"{lemma}" صارت لك: {day_1} قلت "{quote_1}"، واليوم قلت "{quote_2}"» |
| `mistake_gone` | `wrong_form`, `date_ar` | «"{wrong_form}" ما رجعت من {date_ar}» |
| `fluency_change`, better or worse, `mid_clause_pause_rate` or `first_long_pause_s` | `label_before`, `n_before`, `label_after`, `n_after` | «في {label_before} وقفت {n_before} مرات وسط الجملة، {label_after} {n_after}» / «في {label_before} أول وقفة طويلة جات بعد {n_before} ثانية، {label_after} بعد {n_after}» |
| `fluency_change`, `mlr` or `speech_rate` | same | «كلامك بين الوقفات صار أطول: {n_before} كلمات في {label_before}، {n_after} {label_after}» / «... أقصر ...» for `worse` |
| `complexity_change` | same, on `subordination_ratio` as "out of ten" | «جُملك فيها ربط أكثر: {n_before} من كل عشر جمل في {label_before}، {n_after} {label_after}» |
| `accuracy_change` (always with the attempted count beside it, PRD-v2 10.3) | `structure_ar`, `correct_after`, `contexts_after`, `label_before`, `correct_before`, `contexts_before` | «{structure_ar}: {correct_after} صح من {contexts_after} محاولات {label_after}؛ في {label_before} {correct_before} من {contexts_before}» |
| `accuracy_fell_while_trying` | `structure_ar`, `n`, `month` | «أخطاء أكثر هالأسبوع لأنك جرّبت {structure_ar} {n} مرات؛ في {month} ما جرّبته ولا مرة» |
| `talkback_falling` | `n_after`, `label_before`, `n_before` | «طلبت الكلمة من سلمى {n_after} مرات هالأسبوع؛ في {label_before} {n_before}» |
| `then_and_now` | the fluency, complexity or accuracy template with `label_before` = «التسجيل الأول» or «تسجيل {month}» and `label_after` = «هالمرة» | as above |
| `skill_range` | `skill_ar`, `band_low_ar`, `band_high_ar`, `descriptor_ar` | «{skill_ar} تقريباً بين {band_low_ar} و{band_high_ar}: {descriptor_ar}» (the one template in which a band label is permitted, decisions.md §4 f) |

Number slots are rendered as digits in the learner's numeral system (`packages/native/<lang>/numerals`), which the law scan whitelists only inside these slots; `label_*` slots are package phrases («الثلاثاء», «قبل أسبوعين», «في بداية الموسم»), never free text. A second native language adds a file, not code.

### 4.9 Calibration before claims

Tables: `calibration_samples {id, learner_id (for purge and consent, RLS-exempt role for the calibration job), source: m0|beta|synthetic, surface: call|chat|recording, target_language, native_language, text (pseudonymized by 07's `research/anonymize` before any human reads it), clean_spans, word_timings, consent_event_id, tags_a jsonb, tags_b jsonb, adjudicated jsonb, band_a, band_b, band_adjudicated, split: anchor|test}`; `calibration_runs {id, component: analyst_classifier|rater, model, prompt_version, assessment_version, ran_at, n, qwk_band, qwk_ci_low, qwk_ci_high, precision_by_category jsonb, precision_by_tag jsonb, recall_by_tag jsonb, passed, provisional bool, notes}` (aggregates only, no learner data); `skill_calibration {skill, calibrated bool, qwk, external_r, n, as_of}`; `rater_versions {window_start, window_end, model, prompt_version, calibration_run_id}`. There is no `audio_ref`: calibration is text, `clean_spans` and word timings only; PRD-v2 12.5.5 allows "anonymized transcripts (no audio)" and neither consent covers a paid tagger hearing a learner's voice (conformance review). An audio set for the recognizer check (10.14) comes from the Milestone 0 clips under their own addendum, stored separately (10-decision-records §10 #13).

Process (PRD-v2 10.11):

1. **Set.** Milestone 0's hand-tagged calls and chats (Muath's tags in the learner files, exported by `tools/import_m0_tags.py` into `calibration_samples` as `tags_a`) plus a second tagger (OPEN for Muath, section 10) give the first 100 to 150 samples; beta learners with `data_use=true` add the rest to reach 150 to 200. Text, `clean_spans` and word timings only (above). The rater's anchors (`split=anchor`) come from the Milestone 0 week-0 recordings, the test set (`split=test`) from the week-3 recordings, so anchors and evaluation never overlap (skeptic review).
2. **Bars.** `qwk_band ≥ 0.7` for the rater against adjudicated bands on the test split, with the confidence interval stored (`qwk_ci_low`, `qwk_ci_high`; on about 30 items it is wide, so the run is `provisional=true` until beta samples reach about 100 and the bar is read on the lower bound after that). For the classifier, precision is measured at the 12-category level (`precision_by_category ≥ 0.8` for every category) and at the structure level only for tags with ≥ 10 adjudicated instances: those get `claim_eligible=true` in `structure_rules.yaml` when their precision is ≥ 0.8 (expected: 10 to 20 structures in the beta, which covers the active targets); every other structure is `claim_eligible=false` and a claim on it fails with `tag_not_calibrated` until the instances and the precision exist. Recall is reported, not gated. [DECISION, skeptic review: per-tag precision over a few hundred tags with 150 samples is undefined for almost all tags.]
3. **Pinning.** `vendors.yaml roles.rater.pinned_until` names the window; `rater_versions` records the run; `recording/rate` refuses to run with a model or prompt not in the current window row. Mid-window vendor loss is a degraded mode (section 5), never a silent swap.
4. **Re-run on change.** `calibration/run` runs in CI on any change to the analyst prompt, `structure_rules.yaml`, measures code or the rater prompt; a failing run blocks the deploy of that version. A passing run bumps `assessment_version` and schedules the data domain's `learner/rebuild` (4.14).
5. **"Where do I stand".** `skill_calibration.calibrated` is set per skill when the rater's band QWK on that skill's samples meets the bar (PRD-v2 10.11, 10.8.3: the only precondition the PRD states); the `skill_range` claim (4.8.1) then exists for that skill. The first draft also required the external-test correlation `r ≥ 0.5` on ≥ 20 learners, which cannot exist before the week-8 sittings (February 2027) and would silently remove a P0 feature from the beta; it is now [OPEN for Muath] as an additional bar (section 10 #4), and until he decides the PRD's bar applies. Expected: speaking first (recordings), listening when the rater's listening samples exist; the others after the beta.

### 4.10 The then-and-now recording

Task bank in the target package (`packages/languages/<target>/then_and_now/`): forms A to D (A and B from the Milestone 0 kit; C and D written in build week 2 to the same shape, with the PRD-v2 lengths: a 165-word story retold in 60 to 90 s, an opinion question on a familiar topic answered in 60 to 90 s (PRD-v2 10.9.2.1, shorter than the kit's 2-minute task), eight repeat sentences matched by structure). One recording per sitting, not a 'then' and a 'now' per season (PRD-v2 10.9.2.3: the first 'then' after session 2, then one at every finale, each finale's recording being the next comparison's 'then'; conformance and skeptic reviews). `recordings` has one row per sitting with `sitting_n` (the Milestone 0 baseline is sitting 0 with its form recorded), the form cycles A, B, C, D, A by `sitting_n` offset by `learner_id` parity so consecutive sittings never share a form [DECISION]; the comparison is sitting n against n−1, and from sitting 3 also against n−3 for PRD-v2 11.3's 3-month window.

Flow (the client records; the recorder, upload and `recording.turn_audio_ready` are the call domain's, 03 4.10):

1. Offer: Salma offers "the opening tape of your season" on Today after session 2 (a Salma line and a card, 06; the notes are gone, ADR-06); offered again once in sessions 3 to 5 (`api` reads `recordings` to decide); then once at every season finale (`season.boundary`). Framing text from the native package (the Milestone 0 message, adapted).
2. `api` creates `recordings {id, learner_id, sitting_n, season_number, form, tasks: {retell: media_id, opinion: media_id, repeat: [media_id x 8]}, started_at, completed_at, kept: bool}` and emits `recording.completed` when all uploads are in; a partial recording (one task skipped) completes with nulls.
3. `recording/rate`: each task through `call/verbatim-turn` (surface `recording`); `comparable_segments` rows for `rec_retell`, `rec_opinion`; `rec_repeat` scored by alignment (4.4); then one pinned rater call.
4. Rater prompt (Sonnet 5.5, pinned, `output_config` structured, no thinking display needed): input is the two task transcripts (never both recordings of a pair, so it cannot know which is first), the band descriptors A2 to B2+ from the package, six anchor transcripts per band with their adjudicated bands, and the story's eight content points. Output: `{band: int 0..100, band_low, band_high, retell_points_present: [bool x 8], meaning_kept_repeat: [bool x 8] (for sentences with wer in 0.15..0.40 only), notes}`. The rater never produces a progress statement and never sees the learner's name.
5. `recording_ratings {recording_id, task, band, band_low, band_high, measures jsonb, repeat_scores int[], content_points bool[], rater_version_id, assessment_version}`; speaking re-anchored (4.5.6); structures in `stable` checked for confirmation (4.5.3); `recording.rated`.
6. Comparison [P1]: when sitting n is rated and sitting n−1 exists, `claims.generate_then_and_now()` builds candidates per metric and task type with `before` = sitting n−1's value and `after` = sitting n's, ranks them as one family (4.8.2) and runs the gate (rule 3 by corroboration across the two tasks, 4.8.1); `finale_differences()` returns at most two passed claims ranked: `fluency_change(first_long_pause_s or mlr)` > `accuracy_change` > `complexity_change`, preferring claims whose evidence has audio. The Milestone 0 learners' week-0 recordings are sitting 0 where they consented (01 §7 week 5).
7. Storage-off rule (PRD-v2 12.5.2): the recording's media is `ephemeral=true` unless the learner tapped "keep this recording"; the comparison then uses transcripts and measures only, and the finale says so in one line.
8. The season gate (PRD-v2 16.1 "the 4-weekly recording improves for most") is computed by the evaluation domain from `recording_ratings` and `claims`, never shown to learners.

### 4.11 Weekly proof and season finale

#### 4.11.1 `proof/make` (shell in 01; body here)

```python
async def proof_make(evt: ProofRequested):
    L = learner(evt.learner_id); week = evt.week_start                                         # week_start and proof_day in the learner's tz (ADR-16)
    sessions = sessions_in(L, week, week + 7)                                                   # from session_summaries: sessions, not days (ADR-04/05: a learner on two_a_day may have 10 in a week)
    plan = ProofPlan(learner=L, week=week, sessions_in_week=len(sessions))                     # proofs.sessions_in_week is computed here, never stored (ADR-19)
    plan.mode = "slow" if len(sessions) <= 1 else "normal"                                    # PRD-v2 11.1.4
    cands = claims.generate_weekly(L, window=(week - 14, week + 7))                             # metric kinds [P1] + events accrued this week, ranked as one family (4.8.2)
    passed = [c for i, c in enumerate(cands) if gate(c, rank_in_family=i).passed] + claims.unshown_passed(L)   # unshown event claims (owned words, first-evers) from the week
    plan.headline = rank_headline(passed)                                                       # then_and_now > mistake_gone > fluency/complexity/accuracy change > first_ever (structure) > word_owned > did_it
    plan.more = [c for c in passed if c is not plan.headline][:4]
    plan.worse = [c for c in passed if c.direction == "worse"]
    plan.retraction_notice = claims.invalidated_untold(L)                                       # PRD-v2 8.5; 04's claim_invalidations with told_at null
    plan.rhythm_line = rhythm_met_sentence(L, week) if rhythm_met(L, week) else None            # PRD-v2 3.9.3: nothing when not met
    plan.next_focus = last_plan(L).targets.grammar.label_ar                                     # from the teacher's current plan (02 EpisodePlan)
    plan.working_on = working_on_items(L)                                                       # at most 3, with one learner sentence each
    plan.cumulative = {"hours_heard": hours_heard(L), "minutes_spoken": minutes_spoken(L), "words_owned": owned_count(L)}   # monotonic counts only
    plan.flat = plan.headline is None and plan.mode == "normal"
    plan.flat_change = flat_change_sentence(last_plan(L)) if plan.flat else None                 # "the one thing I'm changing": the teacher's step_reason or next target
    plan.question = "worth_it"                                                                   # yes / mostly / no + optional why
    pricing = "batch" if hours_until(evt.proof_day_at) > 24 else "standard"                     # Batch turnaround is up to 24 h (02's cut-line rule); effort set explicitly either way
    script = await proof_producer.write(plan, pricing=pricing)                                   # Sonnet 5.5; claim sentences pasted verbatim by code into {slots}
    law_scan(script, allowed_slots=[c.text_ar for c in plan.claims()] + plan.cumulative_slots(), native_language=L.native_language)
    # whitelist: digits only inside pasted claim sentences (string equality with claims.text_ar) and inside the three cumulative-count slots; any other digit, Eastern or Western, or number word fails (4.7.3); no claim sentence outside plan.headline/more/worse
    audio = await voice_studio.render(RenderJob(kind="proof", lines=script.lines, clips=plan.clip_refs(), voice=salma))
    episode_id = publish_proof_episode(L, script, audio)                                        # episodes.kind = proof; above Today; feed item
    mark_shown(plan.headline, plan.more, plan.worse, surface="proof")                            # claim_shown events -> 04's mark_claim_shown, idempotent
    await inngest.send("proof.ready", {...})
```

The proof day: `proof/fanout` (01) computes it per learner as the weekday with the most sessions in the learner's first 7 local days, else day 7, stores it as `learner_schedule.proof_weekday` [ASSUMPTION: a column the data domain adds; PRD-v2 11.1.1] and sends `proof.requested {learner_id, week_start, proof_day}` at the learner's local proof time, never at a fixed clock time for everyone (ADR-16).

#### 4.11.2 The honest sentences

| Situation | Rule | Sentence slot (from `packages/native/<lang>/`, the pilot's shown in Arabic; the model fills names and the quoted evidence only) |
|---|---|---|
| Slow week (0 or 1 session) | about 45 s, about what has built up since the start, never about the week | cumulative counts, one owned word with its sentence if any, next focus |
| Flat week (normal mode, nothing passed) | say so plainly, name the one change | "أسبوع ثابت. الشي الوحيد اللي بغيّره: {flat_change}" |
| Worse (a passed decline) | the most likely supported reason, then the change | `accuracy_fell_while_trying`: "أخطاء أكثر هالأسبوع لأنك جرّبت {structure} {n} مرات؛ في {month} ما جرّبته ولا مرة"; `harder_task`, `long_gap`, `unknown` variants |
| Too early (metric has no SE yet) | not mentioned at all; the proof does not promise what it cannot measure | nothing |
| Retraction notice | one line, once | "صحّحت شي قلته قبل: {old claim} ما كان دقيق، وهذي الأدلة اللي عندي الحين" |

The simple P0 proof (PRD-v2 11.1.8) is this function with the metric kinds absent from `claims` because no `metric_calibration` row has `n_pairs ≥ 12`; nothing else differs.

#### 4.11.3 The proof producer prompt (Sonnet 5.5, batch pricing when the proof day is more than 24 h away, else standard; `effort` set explicitly and thinking tokens logged)

```text
[SYSTEM, cached] You are Salma, producer of "For one". You script the weekly proof: about 2 minutes of audio you present, with the learner's own clips. You receive a PLAN. Every sentence about the learner's progress is already written in the plan under headline, more and worse; paste them where the slots are and do not add, soften, strengthen or paraphrase them. Everything else you write is linking text, the next focus, the working-on list and the question. Never a number except the ones in the plan's claim sentences and the cumulative counts. No praise of the person. No "keep it up", no "don't stop". {salma_bible} {english_share}
<<cache breakpoint>>
[USER] PLAN: {ProofPlan as JSON, claim sentences pre-rendered by code from the native package's claim templates}
```

#### 4.11.4 Season finale [P1]

`season.boundary` is consumed by the pipeline to make the finale episode (02); the pipeline's writer receives `claims_passed` restricted by `finale_differences(learner_id, season)` (at most two, PRD-v2 11.2) plus the recap counts and the "out in the world" rows; this domain supplies the then-and-now clips through `recording_ratings` and the kept media, and the proof producer's narration for the comparison (the same slots as 4.11.2, "then and now" variant). When the learner skipped the sitting, `finale_differences()` returns only non-recording claims and a `no_recording=true` flag so the finale says so (PRD-v2 11.2.3). When both sittings exist but no difference passes the gate, it returns `nothing_passed=true` and the finale uses the package sentence «هذا خط البداية؛ بدري نقول إن شي تغيّر» (the pilot's "this is your starting line"), never a softened difference (PRD-v2 10.10 "the honest thing is said instead"). "The moment Salma liked most" (PRD-v2 11.2.2) is a sentence about the learner and is drawn from claims: the highest-ranked passed `did_it` or `first_ever` claim of the season, with its quote and clip; when none exists the slot is omitted.

### 4.12 External test hook [P1]

`external_tests {id, learner_id, provider: det|other, sitting: week0|week8, taken_at, overall, subscores jsonb (literacy, comprehension, conversation, production for DET), certificate_ref, consent_event_id, consent_marketing bool default false, imported_by}`; imported by an admin CSV page (no API integration in the beta). Consent (trust promise 6, "only what the learner told the show"): a result enters only when the learner shared the certificate themselves (the Controls "share my test result" action writes a `consent_change {external_test_share: true}` event whose id is `consent_event_id`); For one paying for the sitting does not give it the result. A monthly job `calibration/external-report` computes, per skill, Pearson r between the internal `mu` at the sitting date and the mapped subscore (speaking ↔ conversation+production, listening ↔ comprehension, reading ↔ literacy, writing ↔ production), n, and the band-edge refit (an isotonic fit of internal scale to DET bands, written to `skill_scoring.yaml` as a proposal, applied by hand). Results feed `skill_calibration` (4.9 step 5) and the evaluation domain's gate report. Never shown to any learner; never in marketing without `consent_marketing`.

### 4.13 The teacher as consumer

What this domain writes that `briefs.compile('teacher')` (data domain) reads into `TeacherInput` (02 4.3):

| TeacherInput field | Written by | Rule honoured |
|---|---|---|
| `skills.*` with `{value, low, high}`, `huh_rate_2w_median`, `reading_speed_wpm` | 4.5.6, 4.4 | ranges on every estimate |
| `structure_map[]` with `state, acc_14d{correct, contexts}, avoidance, consecutive_targeted, examples[]` | 4.5.2 to 4.5.5 | clean contexts only in `acc_14d`; `consecutive_targeted` maintained here from `plan.targets` echoes |
| `error_profile[]` with `pattern` / `slip` and `blurred_meaning` share, plus `item_patterns[]` on `(category, lemma_or_chunk, error_type)` | 4.5.4 | 3-across-2 |
| `echo_plan_input` (recurring errors, right forms, last recast outcomes, forms to carry) | 4.7.2 | ADR-06: the teacher's echo plan is the only correction channel |
| `word_bank_summary.size_est, owned_count, recall_candidates, kept` | 4.5.1 (`recall_candidates` = lemmas with ≥ 2 taps across sessions) | PRD-v2 9.5.3 |
| `due_list` | the data domain's scheduler, fed by this domain's grades | PRD-v2 9.4 |
| `facts_usable`, `follow_ups_due`, `interests` | 4.6 | ladder, sensitivity, shelf life |
| `last_14_days[]` (`session_summaries`) | `finish` | uptake, energy signals (`short_turns`, `skipped_call`, `error_spike` = `errors_per_100` > 1.5× the 14-day median, `huh_spike`), talk share, abandoned |
| `claims_passed` | `claims_passed()` | only `status in (passed, shown)` |
| `energy.anxiety_flag` | from `calls.metrics.anxiety_mode` in the last 2 sessions | PRD-v2 5.4.7 |

Triggers (PRD-v2 9.1): `session.after_pass.completed` is the "after each session" trigger, consumed by `episode/produce`'s `wait_after_pass` (02); the nightly, follow-up-due and gap triggers are the pipeline's and the scheduler's. `working_on.changed` is consumed here too: a veto sets `vetoed=true` on the structure's patterns (4.5.4) and an addition is mapped by one Haiku call (`working_on.map`, `effort: low`) from the learner's words (04's `working_on_additions` row) to inventory structure ids and lemmas with a quote, written to `working_on_items` with `source=learner`, before the pipeline's same-day re-plan reads it. With two or three episodes a day (ADR-05) the teacher's one nightly plan covers all of the day's episodes, so this domain's outputs are read once a night and after each session's pass, not per episode.

### 4.14 Rebuilds and the propagation of a wrong memory

**A wrong memory** (PRD-v2 8.4.7, trust promise 7; 04 §C): the learner's `wrong_memory_flag` event is applied synchronously by the data domain's `apply_learner_edit` in `api`, which fixes the named fact at once (`deleted` or `ground_truth` with the correction), bumps `learner_model_version` with cause `learner_edit` so every cached brief is invalid by construction (04 D12), and relays `memory.flagged {learner_id, event_id, fact_id|null, claim_id|null, disputed_text}`. **`memory/correct`** then does what needs more than one row (and also runs on the memory keeper's `corrections` from a call):

1. Resolve, when `fact_id` is null: by matching `disputed_text` against the facts in the last call's `callback` (the host brief's `callback.fact_id` is in the call bundle) and Today's memory line, then by embedding similarity ≥ 0.85 on `disputed_text`. No match → every fact used in the last call's callbacks and in Today's memory line goes `on_hold` (never spoken, not in any brief) until a human resolves the review-queue item within a day; "fixed at once" is honoured because nothing suspect can be spoken meanwhile [DECISION, skeptic review]. A resolved match is applied through `apply_learner_edit` again so the version bumps.
2. Dependents: `follow_ups` for the fact cancelled; `show_canon` rows citing the fact marked `invalid`; `interests` unaffected; `dont_bring_up=true` when the learner said so.
3. Fan out `facts.invalidated {learner_id, fact_ids}`: the pipeline drops the fact from any plan not yet voiced and re-runs editor check 4 on a voiced-but-unpublished episode (02; assumption in section 9); the call bundle is recompiled at the next `POST /v1/calls` (03 4.2 filters by current status).
4. Claims: claims never cite facts, but when the flag disputes a *quote* ("I never said that"), `memory/correct` appends a `quote_disputed {event_id, claim_id, disputed_text}` event through `events.append()` (nothing updates an event, 04 D1), and `stores.invalidate_claim(claim_id, reason="learner_disputed")` writes a `claim_invalidations` row for every claim whose evidence carries that quote; `openable()` and the candidate generator exclude any evidence event with a dispute row from then on.
5. Count: `wrong_memory_flags / callbacks_shown` over 30 days, where `callbacks_shown` = host brief callbacks actually spoken (03 `moves`) plus Today's one-line memory; `learners.wrong_memory_n` is 04's counter; reported to the evaluation domain (PRD-v2 16.1 under 1 in 100).
6. The live apology ("My mistake, noted.") is the live role's line (03), triggered by the same flag.

**Rebuilds** are the data domain's `learner/rebuild` (04 D14; triggered by `learner.rebuild_requested {learner_id, reason}` from `/admin` when `code_versions` change, or in bulk by a script). This domain has no rebuild function of its own [DECISION, skeptic blocker: two owners of one job]. What it contributes:

1. Pure stage functions callable over stored events: `analyst.replay(analyst_result)` (returns the stored validated output), `classify(output, turns)`, `measure(turns, segments)`, `update(...)`, `claims.generate(...)`; 04 replays sessions in order into its `stores_shadow` schema and applies each result with the shadow writers.
2. The analyst is re-run (Haiku, about $0.002 a session) only when `code_versions.analyst` (prompt or model) changed; otherwise the stored `analyst_result` event is replayed, so a classifier, measures or rule-table bump is free and deterministic. A re-run computes its cost first (`sessions × $0.002`) and refuses above `rebuild.max_cost_usd` (default $50) without a flag; the memory keeper is **never** re-run (facts are learner-governed: deletions and confirmations survive) [DECISION, kept from the first draft].
3. The diff is 04's: every claim with `shown_at` set that the new stores no longer support gets a `claim_invalidations` row with `reason="rebuild:{version}"`; passed claims never shown are replaced; new passes are ordinary candidates. `metric_calibration` rows keyed by `measures_version` survive a rebuild that did not change the measures module (4.8.2).
4. `assessment_version` and its parts are recorded in `learner_model_versions.code_versions`; the swap bumps the version with cause `rebuild`; `rebuild_runs` is 04's table. The admin action `rerun-after-pass` (09) is a one-session rebuild through the same path.

**`consent/apply`** (this domain's part of `learner.consent_changed`, 04 §C; PRD-v2 12.5.3, 12.5.5, 12.5.8):

- Voice storage revoked: within 24 h all stored audio is gone (07, 04). `claim_evidence` rows keep `quote`, `t_start_ms`, `t_end_ms` with `media_object_id=null`; "how we know" and "New for you" render text only; no claim is invalidated by this (rule 5 allows the text fallback for every kind except `then_and_now` clips, which the finale then describes in words). `recordings.kept` stays the learner's choice and is honoured by the same rule.
- Data use switched off, or account deletion: `calibration_samples`, `test_retest_pairs` and `claim_candidates` rows for that `learner_id` are deleted (10-decision-records §10 #15: research rows after deletion are deleted, not kept anonymized) and the three tables are in 04's `learner/delete` purge order [ASSUMPTION: 04 adds them]; `calibration_runs` hold aggregates only and are untouched; the pseudonym row (`research_pseudonyms`, ADR-09) goes with the learner.

### 4.15 Configuration keys

| Key | Default | Note |
|---|---|---|
| `assessment.version` and its parts `code_versions.{analyst,classifier,measures,memory_keeper,rater_pin}` | `1.0.0` | stamped on every row and recorded in `learner_model_versions.code_versions` (04 D4); a bump triggers calibration and `learner/rebuild`; `metric_calibration` keys on `measures` only |
| `asr.confidence_threshold[vendor]` (target package `recognizer.yaml`) | 0.70 primary [ASSUMPTION]; revised by the language gate's 30-clip check per recognizer by 2026-11-10 | ADR-03 |
| `asr.segment_clean_min` | 0.8 [ASSUMPTION]; revised by the week-2 replay (share of segments lost) | 4.4 |
| `evidence_quality.full_min` / `partial_min` | 0.80 / 0.40 [ASSUMPTION]; revised by the week-2 replay | 4.1 |
| `analyst.model` / `analyst.effort` / `analyst.max_edits` / `analyst.timeout_s` / `analyst.retries` | `claude-haiku-5-5` / `low` / 40 / 90 / 0 | one prompt (D2) |
| `after_pass.hard_deadline_s` / `after_pass.wait_last_turn_s` | 360 / 20 | 3.4 |
| `after_pass.triggers` | `call.ended` (full), `chat.closed`, `voicenote.received` (text-only) | 3.4 run rules |
| `memory.model` / `memory.effort` / `memory.similarity_threshold` / `memory.view_confirm_hours` / `memory.pending_confirmation_days` | `claude-haiku-5-5` / `low` / 0.85 / 48 / 7 | |
| `memory.shelf_life_days.{job,city,people,event_dated,health,preference,relationship,money,other}` | 180/365/365/14/7/120/365/90/120 | native package defaults; `religion`, `politics`: the raising week only (4.6) |
| `measures.*`, `claims.*` | section 4.8.4 | |
| `skills.R.{speaking,writing}` / `skills.R_a3` / `skills.Q` / `skills.var_cap` / `skills.R_recording` | 100/100 / 196 / 2 / 225 / 64 (only while the rater's `calibration_runs.passed`) | 4.5.6 [ASSUMPTION]; revised by the external-test correlation report |
| `skills.anchors` (target package `skill_anchors.yaml`) | the two-feature table in 4.5.6 [ASSUMPTION] | revised by the isotonic refit, 4.12 |
| `wordbank.prior.k` / `prior.n0` / `prior.produced_factor` | 1500 / 4 / 0.6 [ASSUMPTION] | revised by the week-2 replay against the hand-kept word lists (04 §7: 80% agreement on `owned`) |
| `wordbank.shaky_after_edits` | 2 | 4.5.1 |
| `avoidance.window_days` / `min_sessions` / `min_opportunities` | 21 / 5 / 3 | 4.5.5 |
| `rater.model` / `rater.pinned_until` (vendors.yaml) | `claude-sonnet-5-5` / 2027-02-16 | window 1 runs from the first cohort (2026-12-23) to 2027-02-16 so no beta cohort's first finale (2027-01-19 onward, weekly cohorts) crosses a boundary [DECISION; 01 and 08 adopt the value; cohort-aligned windows thereafter are section 10 #6] |
| `recording.forms` / `recording.max_task_s` / `recording.form_cycle` | [A,B,C,D] / 90 / by `sitting_n` | target package |
| `proof.slow_week_max_sessions` / `proof.max_more` / `proof.batch_if_hours_away` | 1 / 4 / 24 | 11.1; `proof_weekday` is per learner (4.11.1) |
| `rebuild.max_cost_usd` | 50 | only when `code_versions.analyst` changed (4.14); `parallel_learners` is 04's |
| `calibration.qwk_min` / `calibration.precision_min` / `calibration.min_samples` / `calibration.min_instances_per_tag` | 0.7 / 0.8 / 150 / 10 | 10.11, 4.9 |
| `calibration.pairs_daily_at` | 03:00 UTC | ADR-16: a fixed UTC job, not learner-relative |
| `prompts.analyst/memory/proof/rater.version` | semver | recorded on every artifact; `notes` is gone |

### 4.16 Schemas this domain owns

```sql
create table session_summaries (
  session_id uuid primary key references sessions(id),
  learner_id uuid not null, local_date date not null, episode_kind text, format text,
  evidence_quality text not null check (evidence_quality in ('full','partial','text_only')),
  learner_speech_ms int, talk_share numeric(4,3), turns_learner int, words_clean int, words_total int,
  uptake smallint, huh_per_min numeric(6,3), taps_per_100 numeric(6,3), transcript_opened boolean,
  errors_per_100 numeric(6,3), errors_by_category jsonb, targets jsonb,      -- {grammar:{structure_id, contexts, correct}, words:[{lemma, use}]}
  recall_gaps jsonb, retell_done boolean, talkback_asks int, followed_answer smallint, energy_signals text[], anxiety_mode text, abandoned boolean,
  explicit_corrections smallint not null default 0, explicit_correction_quotes jsonb,   -- the analyst's host_explicit_correction flags (4.7.5); 09 reads them
  runs jsonb not null default '[]',          -- [{trigger, trigger_event_id, run_id, completed_at, evidence_quality}] one entry per run of the pass (3.4)
  pronunciation_internal numeric(5,2), analyst_run_id text, assessment_version text not null, created_at timestamptz default now()
);
create index on session_summaries (learner_id, local_date desc);

create table comparable_segments (
  id uuid primary key default gen_random_uuid(), learner_id uuid not null, session_id uuid, call_id uuid, recording_id uuid,
  task_type text not null check (task_type in ('retell','round_two','rec_retell','rec_opinion','rec_repeat')),
  form text, difficulty_tag text, source_quality text not null default 'live', verbatim_vendor text, measurable boolean not null, unmeasurable_reason text,
  t_start_ms int, t_end_ms int, event_ids uuid[] not null, pruned_words int, clean_share numeric(4,3),
  speech_rate numeric(6,2), articulation_rate numeric(6,3), mlr numeric(6,2), mid_clause_pause_rate numeric(6,2), first_long_pause_s numeric(6,2),
  fillers_per_100 numeric(6,2), repairs_per_100 numeric(6,2), mlc numeric(6,2), subordination_ratio numeric(4,3), mtld numeric(7,2), beyond_2000_share numeric(4,3),
  errors_per_100 numeric(6,2), ei_total smallint, measures_version text not null, assessment_version text not null, occurred_at timestamptz not null
);
create index on comparable_segments (learner_id, task_type, occurred_at desc);

-- claims: the data domain's table (04 §4.10, D13), written only through stores.record_claim; kind enum per 4.8.1 (04 adopts it).
-- This domain adds the per-claim evidence detail and the failed-candidate record:

create table claim_candidates (                -- every candidate the gate judged; passed ones also become a claims row (claim_id set)
  id uuid primary key, learner_id uuid not null, claim_id uuid, kind text not null, subject jsonb not null, metric text, task_type text,
  direction text check (direction in ('better','worse','event')), reason text,          -- for worse: trying|harder_task|long_gap|unknown
  before_value numeric, after_value numeric, before_points jsonb, after_points jsonb, sem_used numeric, k_used numeric, threshold_used numeric,
  before_window daterange, after_window daterange, attempts_before int, attempts_after int,
  passed boolean not null, failed_rule text, rank_in_family smallint, family_id uuid,    -- the proof or finale this candidate competed in (4.8.2)
  source_event_ids uuid[] not null, analyst_run_id text, assessment_version text not null, rater_version_id uuid, created_at timestamptz not null default now(),
  unique (learner_id, kind, subject, source_event_ids)                                   -- dedupe across runs (3.4)
);
create index on claim_candidates (learner_id, passed, created_at desc);   -- failed rows purged after claims.failed_retention_days (90)

create table claim_evidence (
  claim_id uuid references claims(claim_id) on delete cascade, ord smallint,
  event_id uuid, verbatim_event_id uuid, segment_id uuid, recording_id uuid, quote text, corrected text,
  media_object_id uuid, t_start_ms int, t_end_ms int, clean boolean not null, source_quality text not null, verbatim_vendor text,
  label_native text,                        -- "then" / "now" / "Tuesday" in the learner's native language (ADR-02)
  primary key (claim_id, ord)
);
-- media_object_id becomes null when voice storage is revoked (consent/apply, 4.14); quote and timings stay; an event named by a quote_disputed event is excluded by openable()

create table metric_calibration (
  metric text not null, task_type text not null, source text not null check (source in ('test_retest','pseudo','analytic')),
  n_pairs int not null default 0, sem numeric, sd_diff numeric, mean_abs_diff numeric, provisional boolean not null default true,
  computed_at timestamptz not null, measures_version text not null, primary key (metric, task_type, measures_version)   -- survives analyst and rule-table bumps (4.8.2)
);
create table test_retest_pairs (
  id uuid primary key, learner_id uuid not null,        -- for purge and data-use revocation (consent/apply); RLS-exempt role for calibration/pairs-daily only
  metric text not null, task_type text not null, x1 numeric not null, x2 numeric not null, days_apart numeric not null,
  form_1 text, form_2 text, difficulty_tag text, long_opinion boolean not null default false,
  source text not null check (source in ('m0','beta_retest','pseudo')), measures_version text not null, created_at timestamptz not null default now()
);

create table recordings (
  id uuid primary key default gen_random_uuid(), learner_id uuid not null, sitting_n int not null,   -- 0 = the Milestone 0 baseline where consented; 1 = the first 'then' after session 2; then one per finale
  season_number int, form text not null, tasks jsonb not null, offered_at timestamptz, started_at timestamptz, completed_at timestamptz,
  kept boolean not null default false, skipped boolean not null default false,
  unique (learner_id, sitting_n)
);
create table recording_ratings (
  recording_id uuid references recordings(id), task text not null, band smallint, band_low smallint, band_high smallint,
  measures jsonb, repeat_scores smallint[], content_points boolean[], rater_version_id uuid, assessment_version text, rated_at timestamptz, primary key (recording_id, task)
);
create table rater_versions (id uuid primary key, window_start date, window_end date, model text, prompt_version text, calibration_run_id uuid);
create table calibration_samples (id uuid primary key, learner_id uuid not null, source text, surface text, target_language text not null, native_language text not null, text text not null, clean_spans jsonb, word_timings jsonb, consent_event_id uuid not null, split text check (split in ('anchor','test')), tags_a jsonb, tags_b jsonb, adjudicated jsonb, band_a smallint, band_b smallint, band_adjudicated smallint, created_at timestamptz);
  -- text only, pseudonymized by research/anonymize (07) before a tagger reads it; no audio_ref (PRD-v2 12.5.5); rows deleted on data-use off or deletion (consent/apply)
create table calibration_runs (id uuid primary key, component text, model text, prompt_version text, assessment_version text, ran_at timestamptz, n int, qwk_band numeric, qwk_ci_low numeric, qwk_ci_high numeric, precision_by_category jsonb, precision_by_tag jsonb, recall_by_tag jsonb, passed boolean, provisional boolean not null default true, notes text);   -- aggregates only
create table skill_calibration (skill text primary key, calibrated boolean not null default false, qwk numeric, external_r numeric, n int, as_of timestamptz);

-- notes and margin_notes: removed (ADR-06, decisions.md §3). Nothing after a call is shown to the learner by this domain.
create table proofs (id uuid primary key, learner_id uuid, week_start date, mode text, plan jsonb, episode_id uuid, headline_claim_id uuid, more_claim_ids uuid[], worse_claim_ids uuid[], worth_it_answer text, worth_it_why text, created_at timestamptz, unique (learner_id, week_start));
  -- sessions_in_week is computed in proof/make from session_summaries, never stored (ADR-19)
create table external_tests (id uuid primary key, learner_id uuid, provider text, sitting text, taken_at date, overall numeric, subscores jsonb, certificate_ref text, consent_event_id uuid not null, consent_marketing boolean default false, imported_by text, imported_at timestamptz);
create table working_on_items (id uuid primary key, learner_id uuid, structure_id text, lemma text, label_ar text, example_quote text, source text check (source in ('teacher','learner')), vetoed boolean default false, created_at timestamptz, retired_at timestamptz);
```

Log events this domain appends (04's registry; nothing updates an event): `call_turn_verbatim {call_id, turn_index, text, words[] {t,s,e,c,clean}, vendor, disfluencies_kept, low_confidence_reason|null, clean_spans, clean_share, assessment_version}` (04 D2), `small_door_voice_verbatim` (same payload with `event_id` of the note), `analyst_result {session_id, run_id, trigger_event_id, output, prompt_version}`, `quote_disputed {event_id, claim_id, disputed_text}`. Tables written through 04's contracts: `claims` (`record_claim`), `word_uses(learner_id, unit_id, event_id, occurred_at, clean, correct, prompted, quote)` and `structure_observations` (through `AfterPassResult`; ADR-19).

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detection | Fallback | Learner sees | Claims |
|---|---|---|---|---|
| Last turn's verbatim not back in 20 s | `wait_last_turn` timeout | The run uses the streaming text for that turn at `clean=false` and keeps waiting for the verbatim event up to 3 min before classifying; past that the turn has no verbatim event (`text_verbatim is null`) | Nothing (there are no notes, ADR-06) | None from that turn |
| Verbatim vendor down | adapter errors ≥ 5 in 10 min (`vendor/health`) | Secondary vendor via `vendor_config` with its own calibrated threshold; both down: turns have no verbatim event, audio retained until success only if storage is on, else deleted at 15 min and the session is `text_only` (PRD-v2 5.4.11: low confidence, no claims) | Nothing | None from speech that session |
| Secondary vendor has no calibrated threshold yet | `low_confidence_reason = vendor_uncalibrated` | Turns transcribed by it are planning evidence only | Nothing | None from those turns until the gate's 30-clip check sets the threshold |
| Haiku structured output fails validation (schema error, quotes not found) | `analyst.validate` drop count > 50% of items, or SDK parse error | One in-step retry with the failure list appended (`retries=0` at the Inngest level); then the run marks `analyst_failed`, the session summary carries counts only, and the stored `analyst_result` is absent so a later `rerun-after-pass` re-runs the model | Nothing | None |
| The pass exceeds 6 min | step deadline | `apply` runs once with the partial result and `evidence_quality=partial`, or with nothing but `session_summaries` if classification did not finish; stores are never half-applied (D17); the teacher plans with `evidence_lag` (02) | Nothing | Candidates are generated only from completed stages |
| The pass runs twice for one trigger (Inngest redelivery) or a code step retries | idempotency key, deterministic observation ids | The second run is a no-op (`events.append` duplicates ignored, `structure_observations.id` and `word_uses` unique keys, `claim_candidates` unique) | Nothing | Unchanged |
| A chat-close run arrives before the call run finished | concurrency 1 per learner | It queues; the watermark makes it process only the chat events | Nothing | Unchanged |
| Memory keeper fails | error or timeout | Facts from this session are not stored; the session is queued for `memory/retry`, which runs hourly (facts can wait; they are never spoken until usable anyway) | Nothing | n/a |
| `metric_calibration` has fewer than 20 pairs for a metric | `calibration/pairs-daily` | Metric claims on it fail with `no_standard_error`; the proof shows events (and accuracy claims under the analytic SE) only | A simpler proof | Only events and analytic kinds |
| A host or Salma line read as an explicit correction | `flags.host_explicit_correction`, the correction guard (07) | Counted in `session_summaries.explicit_corrections` and 09's measure (ceiling 0); a review item with the quote and the prompt version | Nothing further (the line was already spoken or blocked by the guard) | Unchanged |
| Rater model unavailable inside a pinned window | adapter error | The recording is rated by code measures only; `recording_ratings.band=null`; the comparison still works for code metrics; the band re-anchor is skipped; an ops page | The finale still plays the clips; measured differences only from code metrics | `then_and_now` claims on code metrics only |
| Vendor forces a rater model change mid-window | `pinned_until` violated by `vendor_config` | `recording/rate` refuses and pages; the window is closed early, `calibration/run` runs on the new model, a new `rater_versions` row starts, and no comparison crosses the boundary (rule 1) | A finale without the then-and-now sentence that month if the run has not passed | None across versions |
| Analyst overflow (≥ 40 edits) or `recognition_doubt` flag | validator, flag | Session marked for human review; its edits count at half weight for patterns (0.5 observation) and never for claims | Nothing | None |
| Crisis flag from the analyst | `flags.crisis` | `crisis.detected_after_session` at once; Salma's resources card at next open (client, resources per `residence_country`, ADR-20); logged for the crisis record (07); the rest of the pass continues and no claim quotes the distress turn | The resources card once | None from that session |
| Learner disputes a quote | `wrong_memory_flag` on a claim's "how we know" | `quote_disputed` event appended; `claim_invalidations` row with notice; the event is excluded from evidence from then on | One honest line next proof | Invalidated |
| Rebuild changes a shown claim | diff in 04's `learner/rebuild` | `claim_invalidations` row with notice | One honest line next proof | Invalidated |
| Voice storage revoked | `learner.consent_changed` | `consent/apply`: `claim_evidence.media_object_id` nulled, text kept | "How we know" in text | Unchanged |
| Spend alert (per-plan guard, ADR-15) | cost middleware | The memory keeper is deferred to `memory/retry` for the day's remaining sessions; the analyst never falls back to a shorter variant (there is none) | Nothing | Candidates from the available evidence |
| Storage-off learner, pass slower than 15 min | `audio/expire` fires first | Audio gone; verbatim turns already done are kept; turns not yet transcribed have no verbatim event | Nothing | None from those turns |

Too much for the team, and the cut: the full P1 metric claims depend on test-retest pairs that may not exist by 2027-01-26 for every metric. The cut is already in the design: each metric unlocks independently as its row reaches 20 pairs, and the proof's P0 form needs nothing unlocked. If build week 5 slips, the order to drop is, starting with what PRD-v2 already tags P1: the external-test import page (4.12), the forms C and D (season 1 needs only A and B), the recording rater (code metrics still rate), the SEM machinery (`calibration/pairs-daily`), then the full four-skill scoring (already P1). Avoidance (4.5.5) is P0 (PRD-v2 10.7 untagged) and stays in week 5; cutting it would be the owner's call (section 10 #7). The margin note is no longer a cut because it no longer exists (ADR-06). **If there is one engineer** splitting time with the call and pipeline domains, the beta ships: `call/verbatim-turn`, the analyst with validation and `analyst_result`, the classifier with the 12 categories and about 30 structures, the updater as counts into `AfterPassResult`, event claims (`did_it`, `first_ever`, `word_owned`) with their templates, the memory keeper, and the simple proof; everything else in this document waits for the beta period.

---

## 6. Cost and performance against the budgets

Prices from the model table dated 2026-10-06 (Haiku 5.5 $0.10 / $0.50 per MTok; Sonnet 5.5 $2 / $10, cache reads $0.20; Batch at half) and [ASSUMPTION] vendor rates for STT and TTS, to be replaced by the cost domain's `prices.yaml`.

| Piece | Unit assumption | Per session | PRD-v2 14.5 line |
|---|---|---|---|
| Verbatim STT, 7 min of learner audio across call and round two at $0.004/min [ASSUMPTION AssemblyAI-class batch-verbatim rate] | $0.028 | $0.028 | Re-transcription and pronunciation $0.03 |
| Pronunciation, 1 to 3 known sentences at $0.002 each [ASSUMPTION] | $0.004 | $0.004 | (same line) |
| `analyst` Haiku, call run: 9k in (3k cached), 2.5k out including thinking at `effort: low` | $0.0019 | | Analyst and memory keeper $0.04 |
| `analyst` Haiku, text-only run (chat close or small-door note): 4k in (3k cached), 0.8k out | $0.0006 | | |
| Memory keeper Haiku: 6k in, 1k out, `effort: low`; a second short run on the chat | $0.0011 + $0.0005 | $0.004 total for the model calls of a session's two runs | |
| Salma's notes, polish-line TTS, margin note | removed (ADR-06); Salma's on-demand explanations are 03's and 08's line "Salma (when asked) and chat" | $0 here | (that line is 08's) |
| Weekly proof: Sonnet script ($0.01 batch, $0.02 standard when the proof day is under 24 h away) + 2 min Salma TTS ($0.05 [ASSUMPTION]) + clips (byte ranges, $0) ÷ 4 sessions | | $0.015 to $0.018 | Proof share and hosting $0.03 |
| Recording rater (Sonnet, 6k in, 0.5k out) once per 4 weeks ÷ 20 sessions | | $0.001 | |
| `working_on.map` Haiku, rare | | under $0.001 | |
| **Total this domain** | | **about $0.05** | **$0.10 allowed across the three remaining lines** |

Thinking tokens: every call sets `effort` explicitly (`low` for Haiku; `low` for the proof producer and the rater, whose jobs are pasting and banding, not reasoning) and the adapter middleware logs `usage.output_tokens` including thinking into `vendor_calls` (ADR-13: written in its own transaction), so the table above is checked against measured rows from build week 2. Headroom is real; the risk is not this domain's model cost but STT minutes if learners talk more (which is the goal) and more sessions a day (ADR-04: a `three_a_day` learner has three passes a day, each with its own STT line): at 12 min of audio a session the STT line doubles to $0.05 and the total is still under the lines. Rebuilds cost nothing unless the analyst prompt changed (4.14). Scale levers for the $0.35 target: Batch for the memory keeper when the drop is more than 24 h away (saves 50% of $0.0011, not worth code in the beta) and running the rater on Haiku once its calibration passes.

Performance: section 3.4 timeline. Postgres load per run: about 30 row writes in one transaction and 6 reads; the stores are per-learner rows under RLS; nothing here scans across learners except `calibration/pairs-daily` (reads `test_retest_pairs`, a few thousand rows, under the RLS-exempt calibration role) and `proof/fanout` (01).

---

## 7. Build plan for 2026-11-18 to 2026-12-22

Re-dated by 16 days (ADR-07) and re-sequenced to the team as it is (skeptic review: the first draft assumed a dedicated engineer from week 1 while 01, 02 and 03 schedule the same one or two engineers on the event log, the pipeline and the call; 04 lands `apply_after_pass` in week 5). Milestone 0 runs 2026-10-24 to 11-18 in parallel; the language gate for English (ADR-03) sets the recognizer thresholds by 2026-11-10, so this domain does not run the 30-clip test itself. The beta minimum is stated per week; the few-hundred-row inventory, the rater's full calibration and the metric claims are beta-period work.

| Week | Ships | P0 / P1 | What the pilot data lets us test |
|---|---|---|---|
| 1 (2026-11-18 to 11-24) | `call/verbatim-turn` body appending `call_turn_verbatim` with the per-vendor thresholds from the gate's `recognizer.yaml` (ADR-03, ADR-19); `normalize()` and errant plus the target package's spaCy model in the worker image; `packages/languages/en/structure_rules.yaml` v1 with the claim-feeding set (about 30 to 40 B1 core structures) and the 12-category fallback with named predicates and unit tests on the Milestone 0 tags; `tools/import_m0_tags.py` into `calibration_samples` (text only, `learner_id`, anchor/test split); `word_uses` DDL agreed with 04 (ADR-19); migrations for the tables in 4.16 | P0 | Classifier precision by category against Muath's tags on the M0 calls (the first calibration number); confidence distributions per recognizer on the pilot's clips |
| 2 (2026-11-25 to 12-01) | `analyst` (one prompt) with validation, prompted-ness in code and the `analyst_result` event; `measures` limited to `speech_rate`, `mlr`, `mid_clause_pause_rate`, `first_long_pause_s`, `errors_per_100` on verbatim word timings; the updater as pure functions building `AfterPassResult` (words with `word_uses` rows, structures with `structure_observations`, error and item patterns, the beta skill scalars); `word_check.score`; the pass's stages replayed end to end on the M0 transcripts as synthetic sessions against 04's shadow writers; forms C and D of the task bank at the PRD lengths | P0 | Replay all 14 days of each M0 learner and compare the structure map and `owned` words with the learner files (04 §7: 80% agreement); the constants in 4.15 revised |
| 3 (2026-12-02 to 12-08) | `claims` module: candidates, dedupe, the gate with the family correction and the analytic SE, the templates in `packages/native/ar/claims/templates.yaml`, `record_claim` against 04's table, `claim_candidates`; `law_scan` with the CI run over the rendered templates; `memory_keeper` with the ladder, the A3 entry rule and the quote check (replay the M0 intake and calls, compare with the hand-confirmed Life facts); `calibration/pairs-daily` and `metric_calibration` from the M0 week-0 and week-3 recordings plus any re-takes (section 10 #1); `calibration/run` in CI with the category-level bars | P0 (events, templates, memory), P1 (pairs) | Fact precision and false-fact rate against the hand-confirmed facts; the first `sem` numbers and how many metrics are provisional; zero law-scan failures on the template set |
| 4 (2026-12-09 to 12-15) | `session/after-pass` wired to the live call on staging (03 builds the call this week) with the run rules of 3.4: triggers, idempotency key, watermark, the 6-minute deadline, `apply_after_pass` as the single write; `echo_plan_input` into `briefs.compile('teacher')`; `memory/correct` with `on_hold`, `quote_disputed` and `facts.invalidated`; `consent/apply`; `recording/rate` with code metrics and the pinned rater prompt (anchors from the M0 week-0 split); the host-explicit-correction flag feeding 09's `explicit_corrections_per_100_turns` beside the correction guard that 07 and 03 land this week (ADR-06) | P0 | After-pass timings on the 50 `call-bench` calls (p50 and p99 against 10 min); the second run on `chat.closed` adds no duplicate observations; `explicit_corrections_per_100_turns` reads 0 on the scripted calls |
| 5 (2026-12-16 to 12-22) | `session/after-pass` as one function in production (10-decision-records §7 week 5); `proof/make` simple version with the per-learner proof day; the first "then" recording offer on Today after session 2 (sitting 1); avoidance (4.5.5); `salma_explain` fed with `skill_answer()` and `claims_passed` (surface 03/06); the audit page listing `claims` with `claim_evidence`; the end-to-end run with the Milestone 0 learners under a consent that covers it (10-decision-records §10 #13); the exit document's measured cost per session for this domain | P0 (proof simple, first then, avoidance), P1 (rater comparison) | A first weekly proof for each returning M0 learner built only from events and analytic accuracy claims; the monthly false-claim audit dry run on those proofs |
| Beta (2026-12-23 to 2027-01-26) | Metric claims unlock per metric as pairs reach 20; finale differences at the first season boundaries (2027-01-19 onward for the 2026-12-23 cohort, weekly cohorts after); the inventory grown from calibration misses and new targets toward the few hundred rows; the rater's provisional bar re-read at about 100 beta samples; the full four-skill feature tables after the first DET week-8 sittings (P1); the external-test import page and the DET week-0 invitations in the learner's first 7 days; `calibration/run` on the first beta-tagged samples | P1 | False-claim audit under 5% per kind; targets that hold in the next recording; recognizer error by `native_language`; `explicit_corrections_per_100_turns` at 0 across the cohort |

Freeze 2026-12-21 12:00 to 12-24 12:00 UTC and 2026-12-31 to 2027-01-02 (ADR-07); the rater's first window and `calibration/run` must have passed before the first cohort's sitting 1 on about 2026-12-25.

Exit on 2026-12-22 for this domain: `session.after_pass.completed` under 10 min (p99) and under 3 min (p50) on the 50 `call-bench` calls and the end-to-end run; a second run per session on `chat.closed` adds zero duplicate `structure_observations` or `word_uses` rows (a CI replay test); classifier precision ≥ 0.8 by category on the M0 set and `claim_eligible=true` only for structures with ≥ 10 instances above the bar; zero progress sentences anywhere that do not resolve to a `claims` row (a grep-level test over every native-language string template plus the law scan in CI); `explicit_corrections_per_100_turns` = 0 on the end-to-end run; the inventory's few-hundred-row target is stated as beta work, not an exit criterion.

---

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Transcribe the whole call once after `call.ended` | 60 to 120 s of STT before the analyst can start; per-turn transcription deletes storage-off audio sooner and lets the pass begin at once |
| Salma's notes, the polish card and the margin note behind a feature flag | decisions.md §3 removed them and 10-decision-records §8 says a flag never changes a law; the correction guard would need a hole for them |
| A `claims` DDL and a rebuild function in this domain beside 04's | Two owners of one table and one job; the proof brief, `mark_claim_shown`, the purge order and the export are written against 04's shape; a two-person team cannot afford two rebuild mechanisms |
| Re-running the analyst in every rebuild | Vendor cost and non-determinism; the stored `analyst_result` event makes a classifier or measures bump free and reproducible |
| Writing stores stage by stage inside the pass | A memory-keeper failure or the 6-minute deadline would leave stores updated under the old version; one `AfterPassResult` in one transaction is 04's contract |
| Letting the analyst decide prompted-ness | The host's turns and the events are in the log; a model deciding `unprompted` would decide `first_ever` and `owned` claims |
| Let the analyst (or Sonnet) assign structure ids and categories | Labels drift between runs and models; per-tag precision cannot be measured or pinned; ERRANT plus a rule table gives the same tag every time and a diff when the rules change |
| One Sonnet call for the analyst and the memory keeper | Two jobs with two standards: the analyst must be stingy, the memory keeper must quote; mixing them in one prompt produced the Milestone 0 pattern of quoting sentences that were not exactly said |
| A `fast` analyst variant for a 90-second stage | Nothing needs the output within 90 s once the notes are gone (ADR-06); two prompts would mean two outputs for the same turns and nothing to calibrate against |
| Waiving rule 3 for then-and-now | PRD-v2 10.10 exempts only first-ever events; with 3 to 5 metrics × 2 tasks per finale the false-pass rate per finale would have been 25 to 40% |
| A learned memory model (half-life regression) in the beta | No data to train on until months in; the FSRS-style scheduler (data domain) with this domain's grades gives most of the benefit with no training; revisit after 10,000 sessions |
| IRT or a per-item response model for skills | Same data problem; a Kalman scalar with fixed noise is explainable to Muath and to the learner ("a range that narrows slowly") |
| Claim thresholds as fixed constants per metric | A constant is a fabricated standard error; the PRD requires test-retest estimates, and the gate's `no_standard_error` failure is the honest state until they exist |
| Letting the proof producer prompt read the learner model | It would write progress sentences the gate never saw; the `ProofPlan` with pre-rendered claim sentences makes a fabricated win a code bug, not a prompt failure |
| A second human rater per recording in production | Cost and latency; humans stay in the calibration set and the monthly audit, which is where their judgment calibrates the machine |
| Re-running the memory keeper in rebuilds | Would resurrect facts the learner deleted and re-ask confirmed ones; facts are learner-governed, not model-governed |
| Marking a word "owned" by a probability threshold | Not explainable in one sentence; the two-sessions-a-day-apart rule is, and it is what the notebook shows |
| Un-owning a word when it is edited later | The two sentences were real; `shaky_since` and the later sentence are honest without erasing evidence |
| Audio in the calibration set | Neither consent covers a tagger hearing the learner's voice (PRD-v2 12.5.5); the analyst and the rater work on text |
| Counting fillers and repairs in fluency | r = −.20 with perceived fluency (assessment lens); logged for research, never weighted |
| Whole-call fluency | Confounded by the host's questions and the topic; comparable segments only |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check; names follow 10-decision-records §4.

1. **System topology (01).** `session/after-pass` (triggers `call.ended`, `chat.closed`, `voicenote.received`; concurrency 1 per learner; no stage-1 step budget any more), `call/verbatim-turn` (append `call_turn_verbatim`, `is_last` priority), `proof/make`, `proof/fanout` (computes the per-learner proof day and sends `proof.requested` at the learner's local time), `audio/expire` shells exist as in 01 4.3; this domain adds `recording/rate`, `memory/correct`, `calibration/run`, `calibration/pairs-daily` and `memory/retry` as functions in `workflows`; `recording.completed` starts `recording/rate`, not the pass; the worker image carries the target package's spaCy model, `errant`, a punctuation restorer, `wordfreq` and the CMU dictionary; `media_objects` byte-range reads are available in-region for clips (learner-voice kinds stay SSE-C behind `api`, ADR-12); the proof is an `episodes` row of kind `proof` with `episodes.state` published above Today by the delivery path; `HOME_REGION` defaults to `eu-central-1` (ADR-08) and nothing here depends on the region; the rater's `pinned_until: 2027-02-16` replaces 01's `2027-01-03`.
2. **Episode generation pipeline (02).** `episode/produce` waits on `session.after_pass.completed` (15 min) and reads `TeacherInput` through the data domain, including `echo_plan_input` and `item_patterns`; the teacher's one nightly plan covers all of the day's 1 to 3 episodes (ADR-05) and its echo plan is the only correction channel (ADR-06); `claims_passed` is quoted verbatim by the writer and nowhere else; the finale episode takes `finale_differences()` with its `nothing_passed` and `no_recording` flags and "the moment Salma liked most" from claims; `voice-studio.render` exists for the proof (no `render_line` is needed by this domain any more); the pipeline handles `facts.invalidated` by dropping the fact from unvoiced plans and re-running editor check 4 before publish; the editor's check 10 "nothing reads as a correction or a lesson" runs on every script (ADR-06); the fitter's realized target spans are available so `heard` state can be set from exposure; `plan.targets` is echoed back so `consecutive_targeted` can be maintained here.
3. **Live call and voice stack (03).** Per-turn upload and `call.turn_audio_ready` with `is_last`, `event_id`, `turn_index` and `source_mode` (so the 5.4.10 weak-link fallback can be told from a small-door note); `calls.metrics` with `learner_speech_ms`, `anxiety_mode`, `moves` (including `recasts` and `violations` from the correction guard); host `call_turn` events carry `recast`, `recall_gap_id`, `retell`, `talkback_word` so prompted-ness and recast uptake are computed in code; the host brief's `recasts` field is filled from the teacher's echo plan; `recording.turn_audio_ready` with `surface` and the reference text for repeat sentences; `pronunciation.scored` when `call/pronunciation-score` writes the payload; the "my mistake, noted" line is triggered live from the same flag; the call bundle is compiled at `POST /v1/calls` so invalidated and `on_hold` facts never reach a host; `salma_explain` (Sonnet, on demand) is 03's role and reads `skill_answer()`, `claims_passed()` and `active_targets_with_evidence()`; the live talkback role reads `produced_before()` for word-or-hint; `talkback_stt.languages = [native_language, target_language]` per call (ADR-02).
4. **Learner model, event log and data platform (04).** `events` is append-only and registers `call_turn_verbatim` (D2), `small_door_voice_verbatim`, `analyst_result` and `quote_disputed`; `call_turns_v` is the read view; `stores.apply_after_pass(AfterPassResult)` applies everything in one transaction, writes `word_uses` and `structure_observations` with the deterministic ids, bumps the version with `high_water_seq`, and accepts the field names in this document at integration (04 §9 #4); `word_uses` gets a unique key on `(learner_id, unit_id, event_id)`; `claims` keeps 04's DDL with this document's kind enum (and, when 04 revises, `text_native` with `native_language` in place of `text_ar`), `record_claim`, `mark_claim_shown`, `invalidate_claim` and `claim_invalidations`; `learner/rebuild` calls this domain's pure functions and replays `analyst_result`; `apply_learner_edit` handles `wrong_memory_flag`, `fact_card_edit`, `fact_card_viewed`, `working_on_edit` and `consent_change` and relays `memory.flagged` with the extended payload and `learner.consent_changed`; the A3 cards enter the ladder at `usable` at account creation; `out_in_world` and `working_on_additions` exist; `learner_schedule.proof_weekday` is added; `calibration_samples`, `test_retest_pairs` and `claim_candidates` join the `learner/delete` purge order; `learners.{native_language, target_language, residence_country, tz, plan}` exist (ADR-02, ADR-04); the FSRS-style scheduler accepts the grades in 4.5.1.
5. **Client app, podcast feed and delivery (06).** There is no notes door and no margin chip (ADR-06); "New for you" is a card on Today and in the notebook reading passed `did_it` and `first_ever` claims with ▶ by byte range when storage is on; the notebook's "working on", "words you own" (with `shaky_since` shown through the later sentence), "the tape" and "how we know" read `working_on_items`, `word_uses` and the word bank's owned rows, `recordings` plus `recording_ratings`, and `claim_evidence`; the client emits `claim_shown {claim_id, surface}`, `followed {value}` and `fact_card_viewed`; the recording screen enforces 90 s per task (PRD-v2 lengths) and offers "keep this recording"; `chat.closed`, `recording.completed`, `memory.flagged` and the "share my test result" consent action are emitted by `api`; the interface language and numerals come from `packages/native/<lang>/` and the claim templates render in them.
6. **Security, privacy, consent and compliance (07).** Verbatim vendors are approved processors for audio in transit under the regime table (ADR-20); `calibration_samples` holds text only, pseudonymized by `research/anonymize` before a tagger reads it, keyed by `learner_id` for purge; the correction guard with `guard/correction_words.yaml` per language is `guard.check_output` item 6 and counts into `moves.violations` (ADR-06); the crisis record consumes `crisis.detected_after_session` and resources are per `residence_country`; `external_tests` rows are learner-scoped PII under the same RLS; Langfuse carries metadata only unless `data_use` (ADR-09); the in-session verbatim "yes" as explicit consent for sensitive-class facts is counsel's question (10-decision-records §10 #1).
7. **Cost model, vendor strategy and tracing (08).** `prices.yaml` carries verbatim STT per-minute, pronunciation per-utterance and Salma TTS per-character rates, and the Google embedding model (ADR-10); every model call here passes through the adapter middleware with `role in (analyst, memory_keeper, proof_producer, rater, verbatim_stt, pronunciation, working_on_map)` and `vendor_calls` rows are written in their own transaction with thinking tokens counted (ADR-13); `vendors.yaml roles.rater.pinned_until = 2027-02-16` is honoured by `vendor_config`; the per-plan guard (ADR-15) is what trips the spend row in section 5; `salma_explain` is priced under "Salma (when asked) and chat".
8. **Evaluation, observability and operations (09).** The monthly false-claim audit samples `claims` with `shown_at` set and their `claim_evidence`, with the expected false-pass rate per kind from 4.8.4 as the target; `explicit_corrections_per_100_turns` (ceiling 0) is computed from `moves.violations` and `session_summaries.explicit_corrections`; "targets that hold in the next recording", "delayed recall", "talkback use over weeks", "recognizer error by `native_language`", "how much did you follow" against predicted coverage and "wrong memories per 100 callbacks" are computed from `structure_map`, `word_uses`, `session_summaries`, the gate's report and the counter in 4.14; `analyst_validation_drop`, `evidence_quality`, runs per session and gate failure counts by rule are dashboard series; `after_pass_late` is the one latency alert for this domain (`notes_late` is gone); `measures/hourly` replaces the nightly job and `claims/audit-sample` runs at a fixed UTC time (ADR-16); the property tests over the gate assert the invariants in 4.8 against 04's columns (`gate.passed`, `claim_invalidations`), and `eval-gate` runs `calibration/run` on assessment paths.

---

## 10. Open for Muath

Shared items are in 10-decision-records §10 and are not repeated here. Items this domain settled by an ADR or a review fix are removed and listed in section 11.

1. **[OPEN for Muath] Test-retest pairs before the beta.** The claim gate's metric rules cannot open until a metric has 20 pairs (provisional from 12) of same-task recordings on different forms 3 to 5 days apart (D11). Milestone 0 gives week-0 and week-3 pairs (two weeks apart, which measure growth plus noise, not noise; and the kit's opinion task is the 2-minute version, flagged `long_opinion`). Ask 8 to 10 Milestone 0 learners to record the other form once more 3 to 5 days after their week-3 sitting (about 3 minutes each, framed as "a second take so I can hear the difference between a day and a month"), or accept that fluency and complexity claims open only from late January and that the first finales (2027-01-19) carry accuracy claims under the analytic standard error and the honest "starting line" sentence otherwise.
2. **[OPEN for Muath] The second tagger for calibration.** PRD-v2 10.11 needs double-tagged samples. Budget: one teacher of the target language for about 15 hours (150 samples at 6 minutes) by build week 3, paid, under the tagger confidentiality agreement (10-decision-records §10 #2); or Muath tags twice with a week between, which is weaker but free. The category-level precision bar cannot be reported without a second set of tags. The paid native reader of 10-decision-records §10 #11 could be the same person.
3. **[OPEN for Muath] English Grammar Profile permission (PRD-v2 Part 18 #8).** `packages/languages/en/structure_rules.yaml` v1 (about 30 to 40 structures) can be written from the CEFR Companion Volume and public learner-corpus lists without it; the few-hundred-row inventory in the beta period is what the Profile would seed. If permission is refused by 2026-11-25, the beta-period inventory is written from public sources, which costs about three days and loses the per-band evidence.
4. **[OPEN for Muath] Should "where do I stand" wait for the external test?** The PRD's bar is the rater's QWK ≥ 0.7 per skill; the first draft added an external-test correlation `r ≥ 0.5` on ≥ 20 learners, which cannot exist before February 2027 and would remove the `skill_range` answer from the beta. Default in this document: the PRD's bar, with the correlation reported to Muath and used to refit the band edges. Also the DET itself (PRD-v2 Part 18 #9): week 0 and week 8 for 20 to 30 learners, roughly $70 a sitting (an estimate, not a quote), about $4,000, paid by For one; the week-0 sitting must happen in the learner's first 7 days, so the invitation flow must exist by 2026-12-23 even though the import page is P1; the result enters only when the learner shares it (4.12).
5. **[OPEN for Muath] How a shaky owned word is shown.** `owned_at` is never cleared, but a word edited twice after ownership gets `shaky_since` and the notebook shows it with the later sentence (4.5.1). Whether that is a quiet change of the sentence or a line from Salma ("this one slipped on Tuesday") is wording and brand voice.
6. **[OPEN for Muath] Rater windows aligned to cohorts.** The first window is pinned to Sonnet 5.5 from 2026-12-23 to 2027-02-16 so no beta cohort's first finale crosses a boundary (4.15). After it, windows of 4 weeks aligned to the first cohort (2027-02-16, 03-16, ...) mean later cohorts' finales may cross a boundary and lose the then-and-now sentence that month; windows per cohort mean several pinned raters at once. Recommendation: cohort-aligned to the first cohort, accept the occasional missing sentence, which the finale says honestly.
7. **[OPEN for Muath] Whether a worse week with an unknown reason is said, and the week-5 cut.** This design says it ("a worse week on X, and I cannot say why yet") because the trust contract prefers honesty to silence; the alternative is to say nothing when no supported reason exists. In the same breath: avoidance (4.5.5) is P0 and in week 5; if week 5 slips it is the one P0 item in this domain that could be cut (about half a day), and that is the owner's call.
8. **[OPEN for Muath] Forms C and D of the then-and-now task bank.** Someone writes them to the shape in 4.10 at the PRD lengths in build week 2; this is content, not code. If nobody does, the cycle runs A, B, A, B, which the design tolerates until the third sitting (eight weeks after first use).
9. **[OPEN for Muath] Data-use consent wording for calibration samples.** Pseudonymized transcripts (no audio) of consenting learners enter `calibration_samples` and are read by a paid tagger. The Controls switch text per native language must say a person may read anonymized transcripts; counsel's wording (10-decision-records §10 #2).

---

## 11. Revision log (2026-11-06)

Findings from `_review-findings.md` (review:conformance and review:skeptic for this document, neither applied before today) and the rulings in 10-decision-records applied in this revision. Where an ADR overruled a review's fix, the bullet says so.

- conformance major "'where do I stand' bypasses claims" → `skill_range` claim kind written by the gate with rules 1 to 3 n/a and rules 4 and 5 applied (4.5.6, 4.8.1, 4.8.2); `skill_answer()` returns the claim (3.3); calibration precondition is the PRD's QWK bar only, the external-test bar is §10 #4.
- conformance major "stage-1 first_ever rests on the model" → stage 1 no longer exists (ADR-06); "New for you" renders claims that passed after the classifier ran (4.7.4).
- conformance major "did_it has no not-done-before check" → once per `can_do_id` by construction, `claims.did_it.once_per_can_do` (4.8.1, 4.8.2, 4.8.4).
- conformance major "polish card may be an error on any structure" → the polish card is removed (ADR-06); the fix is moot and recorded here.
- conformance major "chat, round two and small-door evidence never reach the pass" → runs per evidence event: full on `call.ended`, text-only on `chat.closed` and `voicenote.received`, each with its cost line and a version bump (3.4, 5, 6).
- conformance major "accuracy and talkback kinds fail no_standard_error forever" → analytic standard errors (binomial, Poisson) with `source='analytic'` rows and `task_type in ('call_turns','chat')` (4.8.2, 4.8.4, 4.16).
- conformance major "avoidance and the margin note cut without the owner" → avoidance kept in week 5 as P0 with the cut as §10 #7; the margin note is removed by ADR-06 rather than cut; the drop order starts with PRD P1 items (5, 7).
- conformance major "stage-1 worst case sums to 98 s" → the 90 s budget is gone with the notes (ADR-06 overrules the fix); one 10-minute timeline with worst-allowed values from the `call.ended` timestamp (3.4).
- conformance major "audio in calibration_samples" → `audio_ref` dropped; text, `clean_spans` and timings only (4.9, 4.16).
- conformance major "A3 facts enter at said_once" → cards shown and not removed enter at `usable`, edited cards at `ground_truth` (4.6 rule 2).
- conformance major "word-choice errors are slips forever" → `item_key` patterns on `(category, lemma_or_chunk, error_type)` with the 3-across-2 rule, `item_patterns` to the teacher (4.3, 4.5.4, 4.13).
- conformance major "week 1 is two to three engineer-weeks" → beta minimum stated: v1 rule table with the claim-feeding set, measures limited, the inventory as beta work (4.3, 7).
- conformance major "the Arabic claim templates are missing" → the template table per kind and direction in the native package, law scan on the rendered set in CI (4.8.5).
- conformance minor "two recordings per season" → one row per sitting, forms cycling, comparison n against n−1 (4.10, 4.16, D14).
- conformance minor "rule 3 reinterpreted for then_and_now" → rule 3 by corroboration across the two tasks and the rater's band, tagged [DECISION] (4.8.1, 4.8.2).
- conformance minor "proof scanner would reject every proof" → whitelist: pasted claim sentences by string equality and the three cumulative slots (4.7.3, 4.11.1).
- conformance minor "margin_notes unique (chat_id)" → table removed (ADR-06); `chat_id` defined as the per-session exchange for the `chat.closed` trigger (3.3).
- conformance minor "consent_changed has no handler" → `consent/apply` (4.14): media refs nulled on voice revocation; calibration and pair rows deleted on data-use off or deletion.
- conformance minor "uncalibrated rater re-anchors speaking at R=64" → R=64 only while `calibration_runs.passed`, else code measures at R=100 and the band advisory (4.5.6).
- conformance minor "sensitive facts: week versus session, stored before confirmation" → `pending_confirmation` state, 7-day expiry, the week reading tagged [DECISION, 5.1 over 8.4.3] (4.6 rule 3).
- conformance minor "measurable is size-based only" → `clean_share >= asr.segment_clean_min` with `unmeasurable_reason` (4.4).
- conformance minor "pinned_until contradicts the open item" → one value, 2027-02-16, computed from ADR-07's cohort dates; 01 and 08 adopt it (4.15, §9 #1 and #7, §10 #6).
- conformance minor "try-first line untagged" → removed with the notes (ADR-06).
- conformance minor "every voice note is low confidence" → `low_confidence_source` only for dial-in and the 5.4.10 weak-link fallback; small-door and say-it-once follow the normal filter (4.1).
- conformance minor "followed_answer missing" → `session_summaries.followed_answer` and the comprehension row (4.4, 4.16).
- conformance minor "no API for produced_before and active targets" → `produced_before()`, `active_targets_with_evidence()`, `echo_plan_input()` in `api.py` (3.3).
- conformance minor "forms C and D to the kit's 2-minute template" → PRD lengths stated; M0 pairs flagged `long_opinion` (4.10, 4.16).
- conformance minor "finale's nothing-passed and 'moment Salma liked most' unspecified" → `nothing_passed` flag with the package sentence; the moment is the top passed `did_it` or `first_ever` (4.11.4).
- conformance "Missing" items → templates (4.8.5); per-event runs (3.4); SE source (4.8.2); consent handling (4.14); beta minimum (7); A3 path (4.6); the two A3 English moments as first observations (4.5.6); `out_in_the_world` storage (4.6); shelf lives for the five missing types (4.6 rule 4); the proof day and `proof.requested {proof_day}` (4.11.1); DET consent (4.12).
- skeptic blocker "two owners of claims and two rebuilds" → this domain's `claims` DDL and `assessment/rebuild` deleted; 04's table through `record_claim` with this document's kind enum; pure stages contributed to `learner/rebuild`; `analyst_result` event so rebuilds are free unless the analyst changed (3.1, 4.8.3, 4.14, 4.16, D10, D12).
- skeptic blocker "the design mutates event rows" → `call/verbatim-turn` appends `call_turn_verbatim`; readers use `call_turns_v`; disputes are `quote_disputed` events (4.1, 4.14, 4.16).
- skeptic blocker "store writes contradict 04" → stages 2 to 5 pure, one `AfterPassResult`, one `apply_after_pass` call, partial-or-nothing on the deadline, `retries=0` on model steps (3.2, 3.4, D17).
- skeptic blocker "no idempotency or evidence watermark" → idempotency key, `high_water_seq`, deterministic observation ids, `word_uses` unique key, candidate dedupe (3.4, 4.5.4, 4.16, 5).
- skeptic major "stage-1 arithmetic and thinking tokens" → the stage is gone (ADR-06); `effort` explicit on every call, thinking tokens logged, `retries=0` and in-step timeouts (3.4, 4.2, 6).
- skeptic major "multiple comparisons" → rule 3 not waived for then_and_now; family ranking with K=2.0 for the top candidate and 2.8 for the rest; expected false-pass rates per kind recorded (4.8.2, 4.8.4).
- skeptic major "nobody writes test_retest_pairs" → `calibration/pairs-daily` with pairing rules per task type, pseudo pairs stated, `measures_version` key, 20 as the bar (3.1, 4.8.2, 4.16, D11).
- skeptic major "calibration bars cannot be computed" → category-level precision plus structures with ≥ 10 instances; anchors split from the test set; QWK confidence interval stored; provisional until about 100 samples (4.9).
- skeptic major "ERRANT on spoken ASR text" → `normalize()` before alignment, punctuation restored, filler `U:` edits ignored, named feature predicates with tests, v1 capped at the claim-feeding set (4.3).
- skeptic major "one threshold for two vendors" → `asr.confidence_threshold[vendor]`, vendor on every evidence row, gate fails uncalibrated vendors (4.1, 4.8.2, D5).
- skeptic major "opaque learner_ref cannot be purged" → `learner_id` on `calibration_samples` and `test_retest_pairs`, purge and revocation in `consent/apply`, runs hold aggregates, text pseudonymized by 07 (4.9, 4.14, 4.16).
- skeptic major "four-skill Kalman delivers nothing in the beta" → beta scope: one scalar per skill from the band prior, the word check, the A3 moments and two anchored speaking features; anchor table published; full tables P1 (4.5.6, 7).
- skeptic major "fast and full analyst disagree" → one prompt; incremental later runs on new events with `prior_results`; `analyst_run_id` on claims; dedupe by `(kind, subject, source_event_id)` (4.2, 4.16, D2).
- skeptic major "build plan assumes a dedicated engineer" → re-sequenced to 01/04 with the one-engineer version stated (5, 7).
- skeptic major "memory/correct leaves a wrong fact live for a day" → the fix goes through `apply_learner_edit` (version bump); unresolved flags put the last call's facts `on_hold`; `memory.flagged` extended with `fact_id`, `claim_id`, `disputed_text` (3.3, 4.14, D16).
- skeptic minor "schema implies two recordings per season" → as the conformance minor above (4.10, 4.16).
- skeptic minor "a later edit never un-owns" → `shaky_since` with the later sentence shown; wording OPEN (4.5.1, §10 #5).
- skeptic minor "law scan misses Eastern digits" → `[0-9٠-٩]` and the native package's number words, unit-tested (4.7.3).
- skeptic minor "prompted-ness decided by the model" → computed by code from host turns and events; the analyst has no `prompted` field (4.2 check 7).
- skeptic minor "three dates for the rater window" → one value, 2027-02-16 (4.15).
- skeptic minor "thinking tokens and batch turnaround" → `effort` explicit, tokens logged; the proof uses Batch only when the proof day is more than 24 h away (4.11.1, 4.11.3, 6).
- skeptic minor "untagged constants" → tagged [ASSUMPTION] with the check that revises each (4.1, 4.5.1, 4.15).
- skeptic "Missing" items → `AfterPassResult` pointer and the single write (3.2, D17); idempotency and dedupe (3.4); pairs writer (4.8.2); multiple-comparisons policy (4.8.2); anchor values and the deferral (4.5.6); per-vendor thresholds (4.1); purge handling (4.14); normalization and predicates (4.3); `openable()` text fallback and "New for you" without audio (4.14, 4.7.4); `analyst_result` persistence (4.2); the one-engineer plan (5).
- ADR-01 → front matter cites decisions.md over PRD-v2 where they differ; PRD part numbers kept elsewhere.
- ADR-02 → `packages/languages/<target>/` for the rule table, recognizer thresholds, anchors and the task bank; `packages/native/<lang>/` for the claim templates, number words, L1-transfer list and shelf-life defaults; the analyst prompt and the L1 patterns driven by `native_language` and `target_language` from the learner row; `label_native`; nothing country- or first-language-specific remains except the pilot's `native/ar` instances.
- ADR-03 → the recognizer thresholds come from the language gate per recognizer; this domain no longer runs the 30-clip test (4.1, 7).
- ADR-04 and ADR-05 → several sessions a day feed the same stores by `session_id`; `proofs.sessions_in_week` computed from `session_summaries`; the teacher's one nightly plan covers the day's episodes; the per-plan guard in section 5; STT cost scales with passes a day (2, 4.5.1, 4.11.1, 4.13, 5, 6).
- ADR-06 → removed: notes, polish card, margin note, `chat/margin-note`, the `fast` analyst, stage 1, `notes.ready`, `note_shown`, `notes_mode`, the notes door, the polish TTS, the notes cost line, `notes_late`; kept as evidence: the notebook, the proof, "New for you", "where do I stand" as `skill_range`, say-it-once and shadowing as pronunciation; added: `echo_plan_input`, the `host_explicit_correction` flag feeding `explicit_corrections_per_100_turns`, `salma_explain` as the consumer of `skill_answer()`; the pass is one function with the 10-minute budget (1, 2, 3, 4.7, 5, 6, 7, 8).
- ADR-07 → build plan 2026-11-18 to 12-22 with the week contents re-sequenced; beta 2026-12-23 to 2027-01-26; first finales from 2027-01-19; freezes; rater window to 2027-02-16 (4.15, 7, §10).
- ADR-08 → nothing here depends on the region; stated in §9 #1.
- ADR-09, ADR-13 → Langfuse metadata only; `vendor_calls` in its own transaction with thinking tokens (3.2, 6, §9 #7).
- ADR-10 → the memory keeper's similarity match uses the Google embedding model (4.6 rule 2).
- ADR-12 → learner-voice clips stay SSE-C behind `api`; byte-range reads for "how we know" and "New for you" (§9 #1).
- ADR-15 → the spend row in section 5 trips on the per-plan guard.
- ADR-16 → no timezone fixed for everyone anywhere: avoidance on the learner's local week, the proof day at the learner's local time, `calibration/pairs-daily` at a fixed UTC time, `measures/hourly` in §9 #8.
- ADR-19 → `word_uses` written by this domain (4.5.1, 4.16); `call_turn_verbatim` as the read event; `episodes.state`; `proofs.sessions_in_week` computed; `cohort_key = invite_date` for the beta cohorts in section 7.
- ADR-20 → crisis resources per `residence_country` in section 5.
- ADR-22 → §10 keeps only this domain's items; the shared ones point to 10-decision-records §10 (#1 region and the verbatim "yes", #2 tagger confidentiality, #11 reviewers, #13 Milestone 0 consents).
- Removed from §10 as settled: "notes when voice storage is off" (notes removed, ADR-06); the old item 7's date (settled by ADR-07 and 4.15); the "forms C and D" item is kept but re-dated.
- **Not applied, and why:** the skeptic's fix to move avoidance into the beta period as P1 was not applied because PRD-v2 10.7 is untagged (P0) and the conformance review's fix to keep it in week 5 wins, with the cut left to Muath (§10 #7). The skeptic's fix to make the memory keeper's rebuild "replay a stored result" was applied for the analyst but the memory keeper is still never re-run in a rebuild (facts are learner-governed), as the first draft decided. The conformance fix to run the structure detector "in stage 1 before a first_ever card" was not applied because stage 1 no longer exists (ADR-06). The conformance review's exact `text_ar` wording for templates was kept as a column name because 04 owns the table; the rename to `text_native` is recommended in §9 #4 rather than made here.
