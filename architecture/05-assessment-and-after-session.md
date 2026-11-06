# Assessment engine, after-session pass and the claim gate

*For one technical architecture, domain 5 of 9. Written 2026-10-17 against PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the assessment, language-acquisition and learning-science lenses, and the Milestone 0 kit (04-production.md, 05-prompts.md, 06-then-and-now.md). Names in this document align with 01-system-topology.md, 02-generation-pipeline.md and 03-live-call-and-voice.md where those documents already named something; where they do not, the names here are canonical.*

Scope: everything that runs after a session and everything that makes a claim about progress. PRD-v2 Parts 10 and 11, 9.1 to 9.3 as the consumer of this output, 5.5 (Salma's notes), 5.6 rule 6 (the margin note), 8.5 (rebuilds), 14.1 after-session roles. Not in scope: the live call (03), episode generation and the teacher's own reasoning (02), the event log's physical schema and the nine stores' storage (data domain), the notebook's screens (client domain).

---

## 1. Summary and the decisions in one table

The after-session pass is one Inngest function, `session/after-pass`, with a 90-second first stage that produces Salma's notes and a second stage that finishes everything else inside 10 minutes and hands the teacher a new learner-model version. Models judge only what needs judgment (what the learner meant, the smallest fix, whether a moment shows a skill, which sentence to polish); code does everything that must be consistent (classification, counting, measures, lifecycles, probabilities, the claim gate). The claim gate is a Python module with one entry point and one output table, `claims`, and that table is the only input of the weekly proof, the finale, the return episode's "real win", the "New for you" card and "where do I stand".

| # | Decision | Chosen | Reason | Rejected |
|---|---|---|---|---|
| D1 | Shape of the pass | One Inngest function `session/after-pass` with a stage-1 step (notes, 60 s budget) and six more steps; per-turn verbatim transcription runs during the call in `call/verbatim-turn` [DECISION, PRD-v2 10.2, 5.5] | The 90 s notes budget is impossible if transcription starts at call end; per-turn transcription means only the last turn is waited for | A whole-call re-transcription after `call.ended` (60 to 120 s of STT before anything else can start) |
| D2 | Analyst model and shape | Claude Haiku 5.5 (`claude-haiku-5-5`), structured output against the `AnalystOutput` Pydantic schema, effort `low`, standard pricing; one call per session on learner turns only, plus a shorter `analyst_fast` call in stage 1 [DECISION, PRD-v2 14.1] | Cheapest model that handles minimal-edit correction and quote-exact extraction; structured outputs remove the parsing failure mode; 10 min does not allow Batch | Sonnet for the analyst (5 to 20x cost for a job the calibration set will show Haiku does); Batch pricing (24 h worst case) |
| D3 | Error classification | Code: ERRANT-style alignment and typing in Python (`errant` library with spaCy `en_core_web_sm`, the pipeline's lemmatizer), then a package rule table `structure_rules.yaml` maps ERRANT types plus token patterns to inventory structure ids and the 12 categories [DECISION, PRD-v2 10.2 step 3, 10.4] | "Models propose, code decides"; the same edit always gets the same tag, which calibration needs; ERRANT is the published standard for English | Asking the model for the structure id (labels drift, precision cannot be measured per tag) |
| D4 | Obligatory-context counting | Analyst marks `needed_structures` per turn from a closed list (the session's targets plus the structures the host's necessity moves invite); code counts contexts and correctness from the classifier's output; a context the analyst invents without a detector pattern is dropped [DECISION, PRD-v2 10.3] | Obligatory contexts need judgment ("was the past needed here?") but the count must be auditable | Pure rule detectors (miss most contexts), pure model counts (unauditable) |
| D5 | Confidence filter | An edit is "clean" when every verbatim word in its span, plus one word on each side, has confidence at or above `asr.confidence_threshold` (package config, set by the 10.14 test; placeholder 0.70) and the turn was not `verbatim_failed`, not dial-in, not a voice note on a weak link; unclean edits are stored with `clean=false`, feed planning at half weight, and never feed a claim [DECISION, PRD-v2 10.2 step 4] | The PRD makes the threshold empirical; the neighbourhood rule catches boundary misrecognitions | Dropping unclean edits entirely (planning loses signal) |
| D6 | Measures and segments | Fluency and complexity only on `comparable_segments` (retell turn, round two, recording tasks), minimum 40 pruned words or 30 s; accuracy on every clean turn and chat message; all formulas in 4.4 [DECISION, PRD-v2 10.3] | The assessment lens: task moves the numbers more than growth; the PRD limits fluency to retell, round two and recordings | Whole-call fluency (confounded by topic and by the host's questions) |
| D7 | Word knowledge | Three Beta distributions per lemma (heard, read, produced), prior from frequency rank and the vocabulary-size estimate, fixed evidence weights (4.5.1); "owned" is a count rule on clean unprompted uses, not a probability threshold [DECISION, PRD-v2 8.3, 10.6] | Every estimate carries a range for free; the fitter can read the mean; the owned rule must be explainable in one sentence to the learner | Single probability with ad hoc bumps; rings (confident/emerging/unseen) |
| D8 | Skill estimates | Four scalar estimates on an internal 0 to 100 scale anchored to CEFR bands, each a Gaussian (mean, variance) updated by a scalar Kalman step from per-session observations with fixed observation noise; the 4-weekly recording re-anchors with lower noise [DECISION, PRD-v2 10.8] | Slow, bounded, carries a range, explainable; one formula for all four skills | IRT or a learned model (no data until months in; a small team cannot maintain it) |
| D9 | Error versus slip | Pattern key `(structure_id, error_type)`; needs 3 clean, non-self-corrected observations across 2 or more sessions; slips are stored and visible to the teacher as slips, never targetable [DECISION, PRD-v2 10.5, 9.2.6] | PRD rule, made precise: self-corrections are monitoring evidence, not errors | Counting any edit |
| D10 | Claim gate placement | A pure module `forone.assessment.claims` producing rows in `claims`; the proof producer, the teacher's `claims_passed`, the finale, the "New for you" card and Salma's "where do I stand" read only `claims` with `status in (passed, shown)`; nothing else in the codebase can write a progress sentence [DECISION, PRD-v2 10.10, law 12] | Fabricated wins impossible by construction; a monthly audit can read one table | Letting the proof producer prompt see the learner model |
| D11 | Standard errors | `metric_calibration` rows per `(metric, task_type)` with `sem` from test-retest pairs; a metric is claimable only when `n_pairs >= 12`; until then only `did_it`, `first_ever` and `word_owned` claims exist [DECISION, PRD-v2 10.10] | PRD rule; 12 pairs is the smallest number at which an SD is not noise (judgment) | Hard-coded thresholds per metric |
| D12 | Rater pinning | `vendors.yaml roles.rater.pinned_until` plus a `rater_versions` row per 4-week window; `assessment_version` (analyst prompt, classifier rules, measures code) is one semver string stamped on every store row and claim; a change triggers `assessment/rebuild` [DECISION, PRD-v2 10.11, 8.5] | An upgrade must never look like progress; a rebuild must be one command | Silent upgrades with "it is probably better" |
| D13 | Salma's notes selection | Code picks the three cards from stage-1 output by fixed priorities (4.7); Claude Sonnet 5.5 writes the Arabic text from a fixed slot structure; a code law scan rejects numbers, grades and banned words before anything is shown [DECISION, PRD-v2 5.5, 10.12] | The hard part is choosing the right sentence, which is a rule; the model only needs to write warm Arabic | Letting the model pick the cards (it picks the most interesting error, not the one on an active target) |
| D14 | Then-and-now rating | Code metrics (fluency, complexity, repeat-task scoring by alignment) plus one pinned Sonnet 5.5 call for holistic band and retell content points, with package anchor transcripts in the prompt; four parallel forms A to D, rotated per season [DECISION, PRD-v2 10.9.2, 14.1] | Most of the comparison is arithmetic on verbatim transcripts; the model is needed only for "meaning kept" and band | A model-only rating (unstable), a second human rater in production (cost) |
| D15 | Weekly proof production | `proof/make` builds a `ProofPlan` in code from `claims`, the schedule and the last plan; Sonnet 5.5 writes Salma's script from the plan with the claim sentences quoted verbatim; `voice-studio.render` voices it; clips are byte ranges of kept audio [DECISION, PRD-v2 11.1] | The simple P0 proof and the full P1 proof differ only in which claim kinds exist in `claims` | A separate proof pipeline per version |
| D16 | Correction propagation | A `wrong_memory_flag` event runs `memory/correct`: the fact is fixed in the Life store at once, dependents (canon, follow-ups, briefs in flight) are invalidated by `facts.invalidated`, and any claim whose evidence the learner disputes is retracted with a notice in the next proof [DECISION, PRD-v2 8.4 rule 7, 8.5, trust promise 7] | A wrong memory is a bug and must not survive in any cache | Fixing the fact and hoping briefs are recompiled |

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
| Notes within 90 s; three cards; rules for every layer | 5.5, 10.12, 15 | stage 1 (4.7) |
| Margin note, at most one per chat, on an active target | 5.6.6, 10.12 | `chat/margin-note` (4.7.5) |
| Pass plus teacher update within 10 min | 9.1.1, 15 | timeline in 3.4; `session.after_pass.completed` by minute 3 |
| Error vs slip: 3 observations across 2 sessions | 10.5, 9.2.6 | 4.5.4 |
| Lifecycle: taking, stable, re-checks; words owned | 10.6 | 4.5.3 |
| Avoidance, weekly | 10.7, 9.3 | 4.5.5 |
| Skill estimates with ranges; "where do I stand" only when calibrated | 10.8, 0.1 row 3 | 4.5.6, `skill_calibration` |
| Word check scoring into a vocabulary-size estimate | 10.9.1 | `word_check.score()` (4.5.1) |
| Then-and-now: tasks, framing, first "then" in week 1, storage-off rule, never dial-in | 10.9.2, 12.5.2 | 4.10 |
| The five gate rules; SE rule; honest fallback sentences; impossibility of fabricated wins | 10.10, law 12, trust 1 and 4 | 4.8 |
| Calibration set, bars, pinned rater, re-run on model change | 10.11 | 4.9 |
| Correction layers table and its rules | 10.12 | 4.7, 4.11 |
| External test | 10.13 | 4.12 |
| Recognizer test feeds the threshold | 10.14 | 4.1, 7 |
| Weekly proof (simple P0, full P1), slow/flat/worse weeks, the "more" section, worth-it question | 11.1 | 4.11 |
| Season finale with at most two measured differences | 11.2 | 4.11.4 |
| Rebuild on version change; shown claims never silently retracted | 8.5 | 4.14 |
| Wrong memory fixed at once and counted | 8.4.7, 16.1 | 4.14 |
| Laws 1, 5, 7, 12; trust promises 1, 4, 6, 7 | 1.2, 1.3 | Law scan on notes and proof text; AI signature; no inference of sensitive classes; claims only through the gate |
| Cost: re-transcription and pronunciation $0.03, analyst and memory keeper $0.04, notes $0.04 (shared with chat), proof share $0.03 | 14.5 | Section 6 |
| Crisis detection in after-session analysis | 7.9.3 | `AnalystOutput.flags.crisis` leads to `crisis.detected_after_session` |

---

## 3. Architecture

### 3.1 Components (canonical names)

All Python, inside the `workflows` service of the topology (01 decision 3), package `forone.assessment`. Nothing here runs in `api` or `call-worker`.

| Component | Kind | Job |
|---|---|---|
| `call/verbatim-turn` | Inngest function (shell: topology; body: here) | One learner turn: verbatim STT, confidence annotation, `clean_spans`, write back to the `call_turn` event, delete the turn audio when storage is off |
| `session/after-pass` | Inngest function (shell: topology; body: here) | Stage 1 (notes) and stages 2 to 7; emits `notes.ready`, `session.after_pass.completed` |
| `chat/margin-note` | Inngest function | One margin note per chat at most, on the learner's message |
| `analyst` | Module, one Haiku 5.5 call (two variants: `fast`, `full`) | `AnalystOutput` per session |
| `edit_classifier` | Module, code (spaCy + errant + `structure_rules.yaml`) | Edits to structure ids and categories; obligatory-context tallies |
| `measures` | Module, code | Fluency, complexity, accuracy, comprehension, talkback, pronunciation roll-ups |
| `updater` | Module, code | Word bank, structure map, error profile, skills, taste rows; scheduler grades |
| `memory_keeper` | Module, one Haiku 5.5 call plus rules | Fact candidates with quotes, interests, goals, canon; quote verification |
| `claims` (`forone.assessment.claims`) | Module, code | Candidate generation and the five-rule gate; writes `claims` |
| `notes` | Module, code plus one Sonnet 5.5 call | Card selection, Salma's Arabic text, law scan, polish-line TTS |
| `recording/rate` | Inngest function | Verbatim per task, code metrics, pinned rater, comparison through the gate |
| `proof/make` | Inngest function (shell: topology; body: here) | Weekly proof; finale differences for the pipeline's finale episode |
| `assessment/rebuild` | Inngest function | Replay the log under a new `assessment_version` into shadow rows; diff shown claims; swap |
| `memory/correct` | Inngest function | `wrong_memory_flag` handling and `facts.invalidated` fan-out |
| `calibration/run` | Inngest function (manual or on version bump) | Run analyst, classifier and rater over `calibration_samples`; write `calibration_runs`; block deploys that miss the bars |
| `word_check` | Module, code | Scores the 48-item check into a vocabulary-size estimate with a range |
| `external_tests` | Table plus admin import | Week-0 and week-8 scores; correlation report |

### 3.2 Diagrams, described

**Diagram A: the after-session pass (draw as a swimlane with four lanes: call-worker, Inngest functions, Postgres/S3, model vendors; time runs left to right with two vertical dashed lines at 90 s and 10 min).**

1. During the call, each learner turn ends: `call-worker` uploads `turn-{n}.ogg` and emits `call.turn_audio_ready`. `call/verbatim-turn` (concurrency 20) calls the `VerbatimRecognizer`, writes `verbatim_text`, `verbatim_words`, `clean_spans`, `verbatim_status=done` into the turn's `call_turn` event, emits `verbatim.turn_completed`, deletes the audio if `voice_storage=false`.
2. `call.ended` arrives. `session/after-pass` starts (concurrency 1 per learner). Step `wait_last_turn`: `waitForEvent verbatim.turn_completed` matching the last `turn_n`, timeout 20 s; on timeout the last turn uses its streaming text at `clean=false`.
3. Step `stage1_notes` (60 s budget): `analyst.fast` (Haiku, learner turns only, no chat, no canon), `notes.select_cards` (code), `notes.write` (Sonnet), `notes.law_scan` (code), polish-line TTS through `voice-studio.render_line`, write `notes` row, emit `notes.ready`. The vertical line at 90 s is drawn after this step.
4. Steps `analyst_full`, `classify_and_measure`, `update_stores`, `memory_keeper`, `claims_candidates`, `finish`. `finish` bumps `learner_model_version`, writes `session_summaries`, emits `session.after_pass.completed`. The 10-minute line is drawn after `finish`; the teacher's step in `episode/produce` (02) is shown starting at it.
5. A side arrow from every model call to the tracing lane (`vendor_calls`, Langfuse), per the cost domain's middleware.

**Diagram B: the claim path (draw as a funnel).** Inputs at the top: `structure_map`, `word_bank`, `comparable_segments`, `recording_ratings`, `analyst can-do moments`. Middle: `claims.generate_candidates()` produces `claims` rows with `status=candidate`. The gate box has five sub-boxes in order: like-for-like, beyond-the-noise, repeated, clean evidence, openable; each either passes the row to the next or stamps `status=failed` with `failed_rule`. Outputs at the bottom, each reading only `status in (passed, shown)`: `proof/make`, `briefs.compile('teacher').claims_passed` (data domain), the finale (pipeline), `notes` ("New for you" uses `did_it` and `first_ever` only), Salma live ("where do I stand" reads `skill_calibration`, not claims). An arrow from the "shown" surfaces back to `claims.status=shown` via the `claim_shown` event.

### 3.3 Interfaces

**Events consumed.** `call.turn_audio_ready`, `recording.turn_audio_ready` (03 4.10, same shape with `surface`), `call.ended {learner_id, call_id, session_id, kind, end_reason, voice_storage}`, `chat.closed {learner_id, session_id, chat_id}` [ASSUMPTION: emitted by the chat service at message 5 or the learner's last message], `chat.learner_message {learner_id, chat_id, message_id, session_id}` [ASSUMPTION], `voicenote.received`, `recording.completed {learner_id, recording_id, season_number, form}` [ASSUMPTION: emitted by `api` when all three task uploads are in], `pronunciation.scored {learner_id, event_id}` (03), `proof.requested {learner_id, week_start}` (topology cron), `season.boundary {learner_id, season_number}`, `wrong_memory_flag` as an Inngest event `memory.flagged {learner_id, event_id}` [ASSUMPTION: `api` mirrors the log event], `working_on.changed`, `learner.consent_changed`.

**Events emitted.** `verbatim.turn_completed {learner_id, call_id, turn_n, event_id, status}`, `notes.ready {learner_id, session_id, notes_id, cards: int}`, `session.after_pass.completed {learner_id, session_id, learner_model_version, evidence_quality: "full"|"partial"|"text_only"}`, `claims.updated {learner_id, passed: int}`, `proof.ready {learner_id, episode_id}`, `recording.rated {learner_id, recording_id}`, `facts.invalidated {learner_id, fact_ids[]}`, `claims.retracted {learner_id, claim_ids[]}`, `crisis.detected_after_session {learner_id, session_id, event_id}`, `assessment.rebuild_completed {scope, assessment_version}`, `calibration.completed {component, passed}`.

**APIs provided (Python, in-process; other domains import them).**

```python
# forone/assessment/api.py
def claims_passed(learner_id: UUID, *, since: date | None = None) -> list[Claim]          # TeacherInput.claims_passed, finale, return episode
def finale_differences(learner_id: UUID, season_number: int) -> list[Claim]                # at most 2, kind in (fluency_change, complexity_change, accuracy_change, mistake_gone)
def skill_answer(learner_id: UUID) -> dict[str, SkillAnswer | None]                        # for Salma's "where do I stand": None when not calibrated
def session_summary(session_id: UUID) -> SessionSummary                                    # last_14_days rows for the teacher
def grade_word_check(answers: list[WordCheckAnswer]) -> VocabEstimate                      # onboarding A4
def margin_note_for(message_id: UUID) -> MarginNote | None
```

**Tables this domain owns** (DDL in 4.16): `session_summaries`, `comparable_segments`, `claims`, `claim_evidence`, `metric_calibration`, `calibration_samples`, `calibration_runs`, `rater_versions`, `recordings`, `recording_ratings`, `notes`, `margin_notes`, `proofs`, `external_tests`, `skill_calibration`. **Stores it writes but does not own** (data domain's nine stores): word bank, structure map, error profile, skills, interests, life, goals (the can-do and season-goal rows only), taste (the per-session rows), show canon.

### 3.4 The two budgets as timelines

Stage 1, 90 seconds from `call.ended` (PRD-v2 5.5.1, 15):

| t (s) | Step | Typical | Worst allowed |
|---|---|---|---|
| 0 | `call.ended` received; `after-pass` starts | 1 | 3 |
| 1 | `wait_last_turn` (only the last turn's verbatim is outstanding; earlier turns were transcribed during the call) | 5 to 12 | 20, then streaming text |
| 13 | `analyst.fast`: Haiku 5.5, learner turns only, ~4k input tokens, ~800 output tokens, effort `low` | 6 to 12 | 25 |
| 25 | `notes.select_cards` and `notes.header` (code) | <1 | 1 |
| 26 | `notes.write`: Sonnet 5.5, ~3k input (cached Salma persona prefix), ~400 output | 6 to 12 | 25 |
| 38 | `notes.law_scan` (code); one retry of `notes.write` on failure | <1 (+12) | 13 |
| 39 | Polish line and natural version TTS (host voice, one line each) through `voice-studio.render_line`; skipped when no polish card | 3 to 6 | 10 |
| 45 | Write `notes`, emit `notes.ready` | <1 | 1 |
| **46** | **Typical end** | | **88 worst** |

The step has a 60 s Inngest timeout on the model calls; past it, the degraded path in section 5 ships a notes card set without the Sonnet text (header plus the reached-for word only) so the learner never waits past 90 s.

Stages 2 to 7, 10 minutes (PRD-v2 9.1.1, 15):

| t | Step | Typical |
|---|---|---|
| 0:46 | `analyst.full`: Haiku 5.5 on all learner turns plus chat so far, ~9k input, ~2.5k output, effort `low` | 15 to 40 s |
| 1:30 | `classify_and_measure`: spaCy parse, errant alignment, rules, measures | 2 to 6 s |
| 1:36 | `update_stores`: word bank, structure map, error profile, skills, taste, scheduler grades (one transaction) | 1 to 3 s |
| 1:40 | `memory_keeper`: Haiku 5.5, ~6k input, ~1k output; quote check in code | 10 to 25 s |
| 2:05 | `claims_candidates` and the gate | <2 s |
| 2:07 | `finish`: `session_summaries`, bump `learner_model_version`, `session.after_pass.completed` | <1 s |
| **~2:10** | **Teacher starts (02 4.3); it has about 7 min 50 s** | |

The pipeline waits at most 15 min for `session.after_pass.completed` (02 4.2 `wait_after_pass`) and then plans from the model as it stands; this domain's own hard limit is 6 minutes, after which `finish` runs with whatever stages completed and `evidence_quality="partial"`.

---

## 4. Detailed design

### 4.1 Verbatim turns and the confidence filter

`call/verbatim-turn` body (the shell, concurrency 20, retries 2 with the secondary vendor on the second retry, is in 01 4.3):

```python
async def verbatim_turn(evt: CallTurnAudioReady):
    audio = await s3.get(evt.media_id, dek=keys.dek(evt.learner_id))          # SSE-C, memory only
    res = await adapters.for_role("verbatim_stt").transcribe(
        audio=audio, content_type="audio/ogg", language=evt.language,          # "en"; "ar" only for talkback clips, which never come here
        meta=CallMeta(learner_id=evt.learner_id, role="verbatim_stt", call_id=evt.call_id, ...))
    thr = package.asr.confidence_threshold                                      # 0.70 placeholder [ASSUMPTION]; set by 10.14
    words = [{**w, "clean": w["confidence"] >= thr} for w in res.words]
    clean_spans = merge_runs(words, key="clean")                                # [(start_idx, end_idx)] of consecutive clean words
    await events.update_call_turn(evt.event_id, {
        "verbatim_text": res.text, "verbatim_words": words, "verbatim_vendor": res.vendor,
        "verbatim_status": "done", "clean_spans": clean_spans, "clean_share": clean_words/len(words),
        "assessment_version": ASSESSMENT_VERSION})
    if not evt.voice_storage: await media.delete(evt.media_id)
    await inngest.send("verbatim.turn_completed", {...})
```

Rules the rest of the domain depends on:

- An **edit span is clean** when all verbatim words in `[span.start - 1, span.end + 1]` are clean. A turn with `verbatim_status in (failed, pending)` has no clean spans; its streaming text is used for planning at `clean=false`.
- `calls.kind = dial_in` [P1] and `mode = voice_notes` turns are marked `low_confidence_source=true`; they have no clean spans regardless of the recognizer (PRD-v2 5.4.12; voice notes on a weak link, 03 assumption 4).
- A session's `evidence_quality` is `full` when at least 80% of learner words are clean, `partial` when 40 to 80%, `text_only` below 40% or when every call turn failed; `text_only` sessions still produce chat evidence (clean by definition) and planning signals.
- The `events` write is the one allowed late-binding update per `call_turn` event (03 assumption 3); if the data domain chooses a second event `call_turn_verbatim` instead, this function emits it and the readers in this domain join on `(call_id, turn_n)`.

### 4.2 The analyst

Two variants of one prompt and one schema. `analyst.fast` (stage 1) receives the learner's call turns and the call brief; `analyst.full` (stage 2) receives everything below. Both: `claude-haiku-5-5`, `output_config={"format": AnalystOutput JSON schema, "effort": "low"}`, `max_tokens` 6000, temperature default, the stable prefix cached.

Input (`AnalystInput`, compiled by code; the whole learner model is never sent, PRD-v2 8.1 rule 4):

```python
class AnalystInput(BaseModel):
    session_id: UUID; call_id: UUID | None; kind: Literal["first","main","round_two","small_door","chat_only","recording"]
    brief: {grammar_target: {structure_id, label, examples: list[str]}, contrast_pair: ... | None,
            words: [{lemma, sense_key}], recall_gaps: [{id, expected}], necessity_moves: [str], retell_prompt: str | None}
    active_targets: [{structure_id, label}]                     # the "working on" items plus current targets, for polish priority
    invited_structures: [{structure_id, label, detector_hint}]  # closed list the analyst may mark as "needed": targets + structures the host moves invite + the package's B1 core set (about 40)
    turns: [{turn_n, speaker: "learner"|"host", text: str, verbatim: bool, clean_spans: [[int,int]], words: [{w, s, e, c}] | None,
             host_moves: {recast: str | None, clarify: bool, recall_gap_id: str | None, retell: bool, talkback_word: str | None}}]
    chat: [{message_id, from: "learner"|"host"|"salma", text}]
    known_patterns: [{structure_id, error_type, count, sessions}]  # the error profile's current patterns, so "repeat" is marked consistently
    produced_before: set[str]                                   # lemmas the learner has produced (for "new for you")
    learner_name: str; native_lang: "ar"
```

Output schema (fixed; code validates every quote against the input text before anything is used):

```python
class Edit(BaseModel):
    turn_n: int | None; message_id: UUID | None
    original: str                      # exact substring of the learner's verbatim text (or chat text), minimal span
    corrected: str                     # smallest change that makes it acceptable spoken English; "" for a deletion
    blurred_meaning: bool
    self_corrected: bool               # the learner produced the correct form later in the same turn
    recast_uptake: Literal["repeated","ignored","n/a"]   # when the host recast this form in the previous host turn
    note: str | None                   # at most 12 words, for the human reviewer only

class NeededStructure(BaseModel):      # obligatory context proposal
    turn_n: int; structure_id: str; span: str; realized: bool

class CanDoMoment(BaseModel):
    turn_n: int; quote: str; can_do_id: str   # from the package's can-do list (about 30 ids, e.g. "disagree_with_reason", "narrate_past_event")

class ReachedFor(BaseModel):
    turn_n: int; paraphrase_quote: str; target_word: str; confidence: Literal["high","medium"]

class TargetUse(BaseModel):
    lemma: str; turn_n: int; quote: str; prompted: Literal["unprompted","host_prompted","recall_gap","talkback","after_polish"]; correct: bool

class AnalystOutput(BaseModel):
    edits: list[Edit]
    needed: list[NeededStructure]
    target_uses: list[TargetUse]
    uptake: Literal[0,1,2]             # did the call reflect the episode and the article
    uptake_evidence: str               # one quote
    retell: {turn_n: int, done: bool} | None
    recall_gaps: [{id, completed: bool, turn_n}]
    can_do: list[CanDoMoment]          # at most 3
    reached_for: list[ReachedFor]
    new_lemmas_produced: list[str]     # lemmas used that are not in produced_before, with quotes
    flags: {crisis: bool, crisis_quote: str | None, complaint: bool, feels_tested: bool, anxiety_signs: bool, recognition_doubt: bool}
    skipped_spans: [{turn_n, text, reason: "garbled"|"arabic"|"unclear"}]
```

Prompt skeleton (the cached prefix is everything before the breakpoint; the Milestone 0 prompt A's analyst rules are carried over nearly verbatim so the calibration set tagged against them stays valid):

```text
[SYSTEM, cached]
You are the analyst of "For one", an English show made for one Arabic-speaking adult at about B1. You read what the learner said today and record exactly what it shows, nothing more. Another program checks every quote you give against the transcript; a quote that is not exact is thrown away.
Rules:
- Only the learner's words count. Quote them exactly as given, including fillers.
- Record an error only when you are confident it is the learner's and not a recognition error. Skip garbled or unclear passages and list them under skipped_spans.
- For each error give the smallest change that makes it acceptable spoken English. Nothing stylistic. Never "improve" a correct sentence. One edit per error; split unrelated errors in one sentence into separate edits.
- Mark blurred_meaning when a listener could misunderstand what happened, who, or when.
- Mark self_corrected when the learner says the right form later in the same turn.
- recast_uptake: if the host's previous turn recast this form, say whether the learner repeated the corrected form in this turn.
- needed: for each structure in INVITED_STRUCTURES, list every learner span where that structure was needed (an obligatory context), and whether it was realized correctly. Do not list structures that are not in the list.
- target_uses: every use of a target word, and whether it was prompted (the host said the word in the two turns before, a recall gap asked for it, talkback gave it, or a polish card showed it this session).
- can_do: at most 3 moments that match a can-do id, with the exact quote. Prefer moments on hard things (disagreeing with a reason, narrating in sequence, hedging).
- reached_for: words the learner searched for, asked for, or talked around; give the English word they needed and quote the paraphrase.
- Common patterns in Arabic speakers' English to watch for, never to assume: missing "be", articles, present perfect vs past simple, prepositions, resumptive pronouns, questions without inversion, uncountable plurals, p/b confusion that made a word unclear.
- flags: crisis is any statement of self-harm intent or serious distress, in either language; quote it.
- You never write to the learner. You never praise, grade or summarize.
INVITED_STRUCTURES and CAN_DO ids: {package lists}
<<cache breakpoint>>
[USER]
{AnalystInput as compact JSON}
```

Code checks after the call (`analyst.validate`), each dropping the offending item and counting a `analyst_validation_drop` metric:

1. `original`, `quote`, `span`, `paraphrase_quote`, `uptake_evidence`, `crisis_quote` must be exact substrings (after whitespace normalization) of the named turn's verbatim text or chat message.
2. `corrected` must differ from `original` by at most 4 token edits (errant alignment); larger rewrites are dropped as stylistic.
3. `structure_id`, `can_do_id`, target lemmas must exist in the package lists sent.
4. At most 3 `can_do`, at most 40 edits per session (above that the output is suspicious and the session is marked `analyst_overflow` for review).
5. An edit whose `original` lies in a non-clean span is kept with `clean=false`.
6. `flags.crisis=true` emits `crisis.detected_after_session` immediately, before any other step (PRD-v2 7.9.3); the rest of the pass continues.

### 4.3 The edit classifier and obligatory contexts

Alignment and typing: for each edit, `errant` aligns `original` to `corrected` (both tokenized with spaCy `en_core_web_sm`, the pipeline's lemmatizer, 02 D19) and yields one or more `(operation, errant_type)` pairs such as `(R:VERB:TENSE)`, `(M:DET)`, `(U:PREP)`, `(R:VERB:SVA)`, `(R:NOUN:NUM)`, `(R:WO)`. The package then maps to the inventory:

```yaml
# packages/language/ar-en/structure_rules.yaml (excerpt)
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
  # ... a few hundred rows seeded from the English Grammar Profile A2 to B2 (OPEN Part 18 #8); each has match, category, expected_band, and optionally detector
fallback:
  by_errant_prefix: {VERB:TENSE: tense_aspect, VERB:SVA: sva, DET: articles, PREP: prepositions, WO: word_order, NOUN:NUM: plurals, PRON: pronouns, ADJ:FORM: comparatives, OTHER: word_choice}
```

Classification returns `(structure_id | None, category, error_type)` where `error_type` is the errant type string; an edit that matches no rule keeps its category from the fallback and `structure_id=None` (it still counts for the category's errors per 100 words, never for a structure). Ambiguity is resolved by rule order (most specific first); a rule can declare `requires_target: true` to match only when that structure is a current target.

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
| `pronunciation` | `say_it_once` and `shadow` event payloads from `call/pronunciation-score` (03 4.10), rolled up as a per-session mean sentence score; internal only | Skills store (`pronunciation_internal`) |

A **comparable segment** row is created for: the retell turn (the learner turn following the host's `retell` move, plus continuation turns until the next host question; `task_type=retell`), round two's first answer turn (`task_type=round_two`), each recording task (`task_type in (rec_retell, rec_opinion, rec_repeat)`). Minimum size 40 pruned words or 30 s, else `measurable=false`. Each row stores every measure above, `clean_share`, `source_quality` (`live`, `voice_note`, `dial_in`), `assessment_version`.

Repeat task scoring (recording part 3), code only: for each of the 8 sentences, word error rate of the verbatim pruned transcript against the reference after lowercasing and contraction normalization; `score = 4 if wer == 0 else 3 if wer <= 0.15 else 2 if wer <= 0.40 else 1 if wer <= 0.75 else 0` [ASSUMPTION, maps the Milestone 0 rubric to WER bands; checked against Muath's hand scores in week 1]; `ei_total` 0 to 32.

### 4.5 The updater (code)

#### 4.5.1 Word bank

Each lemma (and chunk from the package's formulaic list) has three Beta distributions: `heard ~ Beta(a_h, b_h)`, `read ~ Beta(a_r, b_r)`, `produced ~ Beta(a_p, b_p)`. The mean is the probability the fitter reads (02 assumption 3, `word_bank.p_understood`); the range shown to the teacher is the 10th to 90th percentile.

Prior from the vocabulary-size estimate `V` (word check, else the band prior: B1 = 3,000 families, range 2,000 to 4,500 [ASSUMPTION]):

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
| Production after talkback or polish card, same session | | | +0.3 |
| Edit on the word (word choice or form) | | | −2 |
| `reached_for` (talked around it) | −0.5 | | −2 |
| `talkback` ask for the word | | | −1.5 |
| `keep` | (no probability change; sets `kept=true`, scheduled like a target) | | |

Word check scoring (PRD-v2 10.9.1), `word_check.score()`: per band `b` of six, `hits_b` on 6 real items and `fa` false alarms on 12 pseudowords overall; corrected score `s_b = hits_b/6 − fa/12`; vocabulary size `V = sum over bands of clamp(s_b, 0, 1) × band_width` (bands 1,000 to 2,000, 2,000 to 3,000, 3,000 to 4,000, 4,000 to 6,000, 6,000 to 8,000, 8,000 to 10,000, plus the first 1,000 assumed known) with a range of ±(1 − items_answered/48) × 1,500 ± 600 [ASSUMPTION, widened when the check stopped early]. Partial answers count; a learner who skips gets the band prior.

Scheduler grades handed to the data domain's FSRS-style scheduler per item encountered this session: `again` (edit, tap, reached_for, talkback), `hard` (prompted correct), `good` (heard or read without tap, uptake ≥ 1), `easy` (unprompted correct). One grade per item per session, the worst wins.

**Words owned** (PRD-v2 10.6): `owned_at` is set when the word has ≥ 2 clean unprompted correct productions in different sessions whose `occurred_at` differ by ≥ 20 hours [DECISION: "a day apart" as 20 h so an evening session and the next morning's count], and no edit on the word in the later of the two. The learner's own sentences for the notebook are the two quotes. A later edit on an owned word does not un-own it (counts only grow, law 1) but is logged.

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
def update_patterns(error_profile, edits_this_session, session_id):
    for e in edits_this_session:
        if not e.clean or e.self_corrected or e.structure_id is None: 
            error_profile.record_slip(e)            # stored, shown to the teacher as slips, never targetable
            continue
        key = (e.structure_id, e.error_type)
        row = error_profile.get_or_create(key)
        row.observations.append({session_id, e.quote, e.corrected, e.blurred_meaning})
        row.sessions = {o.session_id for o in row.observations}
        row.pattern = len(row.observations) >= 3 and len(row.sessions) >= 2        # PRD-v2 10.5
        row.blurred_share = mean(o.blurred_meaning for o in row.observations)
        row.examples = last_3_clean(row.observations)
```

The teacher's `error_profile` input (02 4.3) receives rows with `pattern=true` as targetable and rows with `pattern=false` tagged `slip`; its prompt rule "an error pattern qualifies only after 3 observations across 2 sessions" is therefore satisfied by data, not by the model's counting. Chat edits are clean by definition and count. A pattern that the learner vetoed in "working on" keeps counting but carries `vetoed=true`; it returns to targeting only if `blurred_share > 0.5` (PRD-v2 9.2.5 "unless it breaks meaning").

#### 4.5.5 Avoidance (weekly)

Runs inside the first `after-pass` of each ISO week per learner (`finish` checks `last_avoidance_check < start_of_week`), never in the live path:

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

Per-session observation `z` per skill, with observation variance `R` (fixed per source):

| Skill | Observation (linear scoring table in `skill_scoring.yaml`, each feature mapped to 0 to 100 by band anchors, averaged with weights) | R |
|---|---|---|
| speaking | `errors_per_100` (w .3, clean turns only), `mlr` (.25), `speech_rate` (.2), `subordination_ratio` (.15), `beyond_2000_share` (.1); only when ≥ 80 clean pruned words in the session | 100 (sd 10); 64 from a recording's rater band |
| listening | `uptake` (.4), `huh_per_min` relative to predicted coverage (.3), `taps_per_100` in the transcript (.2), `transcript_opened` on first play (.1) | 144 |
| reading | article `taps_per_100` (.4), read time per 100 words vs band norms (.3), `uptake` when the call reflected the article (.3) | 144 |
| writing | chat `errors_per_100` (.5), `mlc` (.3), `beyond_2000_share` (.2); only when ≥ 60 learner words in the chat | 100 |

Update: `K = var / (var + R); mu += K·(z − mu); var = (1 − K)·var + Q` with process noise `Q = 2` per session (lets the estimate move slowly) and `var` capped at 225. Prior at onboarding: `mu` from the band prior (B1 = 47), `var = 225`; the word check moves listening and reading priors by `(V − 3000)/200` points; the first call gives the first speaking observation with `R = 196`. A recording re-anchors speaking with `R = 64` using the pinned rater's band and the code measures.

`skill_answer()` returns a band range and its real-situation sentence from the package descriptors only when `skill_calibration[skill].calibrated = true` (4.9); otherwise `None`, and Salma says she cannot say reliably yet (PRD-v2 10.8.3).

### 4.6 The memory keeper

One Haiku 5.5 call with structured output, then rules. Input: the learner's verbatim turns and chat, the onboarding fact cards (session 1 only), current facts (text, status, fact_type, expires_at), interests (topic, salience), goals, canon (last 30 entries), the sensitive-class list.

```python
class FactCandidate(BaseModel):
    text: str                          # the fact in third person, Arabic or English as said
    quote: str                         # exact substring of a learner turn or chat message
    turn_n: int | None; message_id: UUID | None
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
2. **Ladder:** new fact → `said_once` (never spoken; notebook "I think..."). An existing `said_once` fact matched by text similarity (embedding cosine ≥ 0.85 [ASSUMPTION] on the same `fact_type`) in a different session → `usable`. A `fact_card_edit` or `notebook_edit` event → `ground_truth`. A notebook card viewed and left unedited for 48 h → `usable` (the client emits `notebook_viewed {fact_ids}` [ASSUMPTION]).
3. **Sensitivity:** `fact_type in (health, money, relationship, religion, politics)` → `sensitive=true`; stored only if the learner confirms (ladder step 2 by chat or notebook; a second spontaneous mention does not count), never `usable` for a brief outside the session week it was raised; the teacher's `facts_usable` filter (02) excludes them after that week.
4. **Shelf life** by `fact_type` from the package (`job` 180 d, `city` 365 d, `people` 365 d, `event_dated` until `event_date + 14 d`, `health` 7 d, `preference` 120 d, `interest` handled by salience); expired → `dormant`, never spoken, kept.
5. **Supersede:** `supersedes_fact_id` sets the old fact `superseded` and links history.
6. **Follow-ups:** one row per `event_dated` fact, `due_at = event_date + 1 d`, state `pending → used → history`; the teacher consumes `follow_ups_due`.
7. **Interests:** salience `+0.3` on `mentioned`, `+0.6` on `enthusiastic`, `−0.5` on `dismissed`, decays `×0.93` per week without engagement; below 0.2 → `dormant`; a mention wakes it.
8. **Canon** rows are appended with the session id; the pipeline's series bible reads them (02 D14).
9. **Corrections** go straight to `memory/correct` (4.14) with the quote as evidence.

The memory keeper never infers: a candidate whose `quote` does not itself state the fact (the model "concluded" it) fails the quote check by construction, because the check is on the quote, and a second rule rejects facts whose text contains tokens absent from the quote beyond a stop-list and inflections (`text_overlap >= 0.6`).

### 4.7 Salma's notes (stage 1)

#### 4.7.1 Card selection (code)

Input: `analyst.fast` output (validated), the call's `calls.metrics`, the structure map and error profile as of before this session, `produced_before`, `voice_storage`.

```python
def select_cards(a: AnalystOutput, ctx) -> list[Card]:
    cards = []
    # 1. New for you: a did_it / first_ever candidate that passes the gate's clean+openable rules
    nf = claims.candidates_new_for_you(a, ctx)          # kinds: first_ever (structure first correct unprompted, word first unprompted) or did_it (can_do on a hard thing)
    nf = [c for c in nf if claims.gate(c).passed]
    if nf: cards.append(Card("new_for_you", claim=rank_new_for_you(nf)[0]))   # rank: structure first_ever > can_do hard > word first unprompted
    # 2. Polish: one sentence, errors on active targets first
    pool = [e for e in a.edits if e.clean and not e.self_corrected and e.structure_id]
    def polish_score(e):
        on_target = e.structure_id in ctx.active_target_ids
        pattern = ctx.error_profile.is_pattern(e.structure_id, e.error_type)
        fluent = ctx.no_pause_over_500ms_in(e)           # said fluently = confident error (learning-science lens)
        return (on_target*4 + pattern*3 + e.blurred_meaning*2 + fluent*1 + (e.recast_uptake=="ignored")*1)
    if pool: cards.append(Card("polish", edit=max(pool, key=polish_score)))
    # 3. A word you reached for
    rf = [r for r in a.reached_for if r.confidence == "high" and r.target_word not in ctx.produced_before]
    if rf: cards.append(Card("reached_for", item=rf[0]))
    # Notes preference: "only when it matters" shows the set only if a polish card on an active target exists
    if ctx.notes_pref == "when_it_matters" and not any(c.kind=="polish" and c.edit.structure_id in ctx.active_target_ids for c in cards): return []
    if ctx.notes_pref == "never": return []
    return cards[:3]
```

Anxiety mode (`calls.metrics.anxiety_mode` not null) does not remove the polish card; PRD-v2 5.4.7 moves correction *to* the notes. The first call (`kind=first`, A8) uses the same selector with `max_cards=2` and the polish card optional (PRD-v2 2.2 A8).

Header (code, never the model): `"{call_mm:ss} مكالمة · تكلمت {speech_mm:ss}"` from `calls.metrics.learner_speech_ms`. Information, not a target; no comparison with yesterday.

#### 4.7.2 Writing the text (Sonnet 5.5)

`claude-sonnet-5-5`, standard pricing, `output_config={"format": NotesText schema}`, `max_tokens` 1500, cached prefix = Salma's bible plus the rules below; the per-call part is the three selected cards with their quotes and, for the polish card, the corrected sentence from the analyst (the model may rephrase the *natural version* for spoken English but the learner's sentence is pasted by code, never re-typed by the model).

```text
[SYSTEM, cached] You are Salma, the producer of "For one" (bible: {salma_bible}). You write short notes in friendly, plain Saudi Arabic with the learner's English quoted exactly as given. Season English share: {english_share}.
Rules: at most three cards in the given order, each only from the material given. Card "new_for_you": one line in Arabic on why that moment matters, the learner's exact English words go in {quote} unchanged. Card "polish": the learner's sentence first (unchanged), then "قبل ما تنزل، كيف تصلّحها؟", then the better version (one change, spoken English), then "قلها مرة وحدة بصوت عالي". Card "reached_for": the word, its Arabic meaning for this sense, one short English example. Never a number, a grade, a level, a percentage, a score, a streak. Never praise the person; name the thing. Never mention progress or improvement. Never a lesson word (lesson, test, exercise, level, homework). End with "سلمى، منتجة البرنامج (ذكاء اصطناعي)".
<<cache breakpoint>>
[USER] {cards as JSON}
```

#### 4.7.3 Law scan (code, before anything is stored)

Rejects and retries once, then falls to the degraded card set: any digit outside the header and the quote; any of the package's banned lesson words in Arabic or English (`درس`, `اختبار`, `مستوى`, `واجب`, `نسبة`, `درجة`, `lesson`, `test`, `level`, `homework`, `score`, `percent`); any progress verb list (`تحسنت`, `تقدمت`, `improved`, `better than`); the learner's quoted sentence altered (string equality against the analyst's `original`); a card not in the selected set; a missing signature.

#### 4.7.4 Audio and storage

Polish card: the learner's own sentence is played by byte range from `call_full` (voice storage on) using the turn's `t_start_ms`/`t_end_ms` and the word timings of the span; with storage off, text only (PRD-v2 5.5.2). The natural version is rendered once in the throwing host's voice (`voice-studio.render_line`), stored as a `media_objects` row of kind `clip`, and the "New for you" ▶ uses the same byte-range mechanism. `notes` row: `{id, learner_id, session_id, call_id, cards jsonb, header, text_ar, audio_refs, model_versions, assessment_version, shown_at}`; a `note_shown` event when opened; `say_it_once` upload → `pronunciation.requested` (03) and `after_polish` provenance on any later use of that form this session.

#### 4.7.5 The margin note (chat)

`chat/margin-note` on `chat.learner_message`, debounced 5 s per chat, concurrency 1 per chat: if `margin_notes` already has a row for this chat, stop. Run the classifier on the message (text is clean): `edits = classify(analyst.fast_text(message))` (a Haiku call on one message, ~1 s). Candidate edits on an active target, pattern first; if none, stop (a margin note on a non-target error is not allowed, PRD-v2 5.6.6). Write the note (Sonnet, the polish-card slot without the "say it once" line, ≤ 25 Arabic words plus the two English sentences), law scan, store `margin_notes {chat_id, message_id, edit, text_ar}`, emit `margin_note.ready`; the chat service renders the collapsed "✎ 1 note" chip (client domain). The host never sees it.

### 4.8 The claim gate (code)

#### 4.8.1 Claim kinds

| kind | Statement shape | Minimum history | P |
|---|---|---|---|
| `did_it` | "You disagreed with Karim and gave a reason" (a can-do moment on a structure or can-do at or above the learner's band) | none (A8 onward) | P0 |
| `first_ever` | "First time you used *should have* on your own" (structure: first clean correct unprompted context; word: first clean unprompted use) | the structure or word had ≥ 1 prior session of exposure with no correct unprompted use | P0 |
| `word_owned` | "*Negotiate* is yours now: Tuesday you said ..., today you said ..." | the owned rule (4.5.1) | P0 |
| `mistake_gone` | "*I go yesterday* has not come back since 2026-12-14" | structure `confirmed` (stable and held in the next recording) and the pattern had ≥ 3 observations | P1 |
| `fluency_change` | "You spoke for 40 seconds before your first long pause; in week 1 it was 12" / `mlr`, `speech_rate`, `mid_clause_pause_rate` | `metric_calibration` row usable; ≥ 2 comparable segments each side | P1 |
| `complexity_change` | `subordination_ratio`, `mlc`, `beyond_2000_share` | same | P1 |
| `accuracy_change` | `oc_accuracy` for one structure, or `errors_per_100` on a category, always with the attempted count beside it | same; ≥ 5 contexts each window | P1 |
| `accuracy_fell_while_trying` | "More mistakes this week because you tried the past perfect eleven times; in October you never tried it" | a worse `accuracy_change` whose attempts rose ≥ 2× | P1 |
| `talkback_falling` | "Four talkback asks this week; in week 1, fifteen" | ≥ 3 weeks of calls, change beyond noise | P1 |
| `then_and_now` | the finale's measured differences (a `fluency_change`, `complexity_change` or `accuracy_change` whose two data points are two recordings) | two recordings | P1 |

Every claim row carries `evidence` (4.16): the event ids, quotes, media byte ranges, segment ids and the numbers, so "how we know" is a render of the row.

#### 4.8.2 The gate

```python
NOISE_K = config("claims.noise_multiplier", 2.0)          # PRD-v2 10.10 rule 2
MIN_PAIRS = config("claims.min_test_retest_pairs", 12)     # D11
LIKE_FOR_LIKE = {                                          # rule 1: which task types may be compared
    "retell": {"retell"}, "round_two": {"round_two"}, "rec_retell": {"rec_retell"}, "rec_opinion": {"rec_opinion"}, "rec_repeat": {"rec_repeat"},
}

def gate(c: ClaimCandidate) -> GateResult:
    # Rule 4 first because it is cheapest and most often fails: clean evidence
    if c.kind in GRAMMAR_KINDS and not all(ev.clean for ev in c.evidence):            return fail(c, "clean_evidence")
    if any(ev.source_quality in ("dial_in", "voice_note") for ev in c.evidence):       return fail(c, "clean_evidence")   # PRD-v2 5.4.12
    if any(ev.verbatim_status != "done" for ev in c.evidence if ev.is_speech):         return fail(c, "clean_evidence")
    # Rule 5: openable
    if not all(ev.openable() for ev in c.evidence):                                    return fail(c, "openable")        # quote exists in the log; audio range exists or text fallback is allowed for this kind
    if c.kind in ("did_it", "first_ever", "word_owned"):                               # rule 3 exempts first-ever events; rule 1 and 2 do not apply to events
        return passed(c)
    # Rule 1: like for like
    if c.kind in METRIC_KINDS:
        if not c.before.task_type in LIKE_FOR_LIKE[c.after.task_type]:                 return fail(c, "like_for_like")
        if c.kind == "then_and_now" and c.before.form == c.after.form:                 return fail(c, "like_for_like")   # same stimulus would be memory, not growth
        if c.before.assessment_version != c.after.assessment_version:                  return fail(c, "like_for_like")   # D12: never across a version change
    if c.kind in ("accuracy_change", "accuracy_fell_while_trying") and (c.before.contexts < 5 or c.after.contexts < 5):
                                                                                        return fail(c, "like_for_like")
    # Rule 2: beyond the noise
    cal = metric_calibration.get(c.metric, c.after.task_type)
    if cal is None or cal.n_pairs < MIN_PAIRS:                                         return fail(c, "no_standard_error")  # PRD-v2 10.10: until SE exists, only events
    threshold = NOISE_K * cal.sem
    if abs(c.after.value - c.before.value) < threshold:                                return fail(c, "beyond_noise")
    # Rule 3: repeated: at least two data points point the same way
    recent = c.after_points                                                             # the two most recent comparable segments (or the single recording, for then_and_now, where "repeated" is met by rule: two recordings are two points)
    if c.kind != "then_and_now":
        if len(recent) < 2 or len(c.before_points) < 2:                                return fail(c, "repeated")
        sign = math.copysign(1, c.after.value - c.before.value)
        if not all(math.copysign(1, p.value - c.before.value) == sign and abs(p.value - c.before.value) >= threshold for p in recent):
                                                                                        return fail(c, "repeated")
    return passed(c)
```

Candidate construction, per metric kind: `before` = mean over the two earliest measurable comparable segments of the same `task_type` in the comparison window (weekly proof: the previous 2 weeks against this week; finale: the previous recording), `after` = mean over the two most recent; `before_points`, `after_points` are those segments. A window with fewer than two measurable segments on either side produces no candidate. `sem` for a metric is `sd(x2 − x1) / √2` over the test-retest pairs in `metric_calibration` (same learner, same task type, 2 to 7 days apart), recomputed nightly as pairs accumulate; `n_pairs`, `sem`, `computed_at` are stored and every claim records the `sem` it was judged against.

Direction: a candidate is generated for both improvement and decline. Declines pass the same gate and are stored as `direction=worse`; the proof producer must phrase them with the supported reason (`accuracy_fell_while_trying` when attempts rose, `harder_task` when the segment's difficulty tag is higher, `long_gap` when `days_since_session >= 5` preceded the window, else `unknown` → the proof says "a worse week on X, and I cannot say why yet"). The honest fallbacks when nothing passes are chosen in `proof/make`, not here (4.11.2).

#### 4.8.3 Status lifecycle

`candidate → passed | failed(failed_rule)`; `passed → shown` when any surface emits `claim_shown {claim_id, surface}`; `passed | shown → retracted(reason)` only by `assessment/rebuild` or `memory/correct`; a `shown` claim that is retracted sets `notice_pending=true` and the next proof carries one honest line (PRD-v2 8.5). A claim is never deleted. A `failed` candidate is kept 90 days for the audit, then purged.

#### 4.8.4 Thresholds in one place

| Key | Default | Source |
|---|---|---|
| `claims.noise_multiplier` | 2.0 | PRD-v2 10.10 |
| `claims.min_test_retest_pairs` | 12 | D11 [ASSUMPTION] |
| `claims.min_contexts_accuracy` | 5 | PRD-v2 10.6 |
| `claims.owned.min_sessions` / `owned.min_hours_apart` | 2 / 20 | PRD-v2 10.6 |
| `claims.first_ever.min_prior_sessions` | 1 | D |
| `claims.did_it.min_band_offset` | 0 (at or above the learner's `band_low`) | PRD-v2 2.2 A8 "not easy" |
| `claims.stable.window_days` / `stable.min_contexts` / `stable.min_accuracy` | 14 / 5 / 0.8 | PRD-v2 10.6 |
| `claims.recheck_days` | [14, 28, 56] | PRD-v2 10.6 |
| `claims.finale.max_differences` | 2 | PRD-v2 11.2 |
| `claims.failed_retention_days` | 90 | audit |
| `asr.confidence_threshold` | 0.70 placeholder | 10.14 (package) |
| `measures.pause_ms` / `measures.long_pause_ms` | 250 / 2000 | research norm [ASSUMPTION] |
| `measures.min_segment_words` / `min_segment_s` | 40 / 30 | D6 |

### 4.9 Calibration before claims

Tables: `calibration_samples {id, source: m0|beta|synthetic, surface: call|chat|recording, learner_ref (opaque), text, audio_ref|null, consent_data_use bool, tags_a jsonb, tags_b jsonb, adjudicated jsonb, band_a, band_b, band_adjudicated}`; `calibration_runs {id, component: analyst_classifier|rater, model, prompt_version, assessment_version, ran_at, n, qwk_band, precision_by_tag jsonb, recall_by_tag jsonb, precision_claim_tags, passed, notes}`; `skill_calibration {skill, calibrated bool, qwk, n, as_of}`; `rater_versions {window_start, window_end, model, prompt_version, calibration_run_id}`.

Process (PRD-v2 10.11):

1. **Set.** Milestone 0's hand-tagged calls and chats (Muath's tags in the learner files, exported by `tools/import_m0_tags.py` into `calibration_samples` as `tags_a`) plus a second tagger (OPEN for Muath, section 10) give the first 100 to 150 samples; beta learners with `data_use=true` add the rest to reach 150 to 200. Audio stays only where voice storage consent exists; the analyst needs text and `clean_spans`, which are always kept.
2. **Bars.** `qwk_band ≥ 0.7` for the rater against adjudicated bands; `precision ≥ 0.8` for every `(structure_id)` tag that feeds a claim (the claim-feeding set = structures that are or were targets plus every structure with `pattern=true` for any learner); recall is reported, not gated. Tags below the bar are marked `claim_eligible=false` in `structure_rules.yaml` and claims on them fail with `tag_not_calibrated` until the rule is fixed.
3. **Pinning.** `vendors.yaml roles.rater.pinned_until` names the window; `rater_versions` records the run; `recording/rate` refuses to run with a model or prompt not in the current window row. Mid-window vendor loss is a degraded mode (section 5), never a silent swap.
4. **Re-run on change.** `calibration/run` runs in CI on any change to the analyst prompt, `structure_rules.yaml`, measures code or the rater prompt; a failing run blocks the deploy of that version. A passing run bumps `assessment_version` and schedules `assessment/rebuild`.
5. **"Where do I stand".** `skill_calibration.calibrated` is set per skill when the rater's band QWK on that skill's samples meets the bar *and* the external test correlation (4.12) exists for that skill with `r ≥ 0.5` on ≥ 20 learners [DECISION, judgment: internal agreement alone does not prove the scale means what CEFR means]. Expected: speaking first (recordings and the DET conversation subscore), the others after the beta.

### 4.10 The then-and-now recording

Task bank in the language package: forms A to D (A and B from the Milestone 0 kit; C and D written in build week 2 to the same template: a 165-word story with the eight-point shape, an opinion question on a familiar topic, eight repeat sentences matched by structure). Form rotation per learner: season 1 "then" = A or B by `learner_id` parity, "now" = the other; season 2 uses C and D; season 3 returns to A/B (eight weeks after the first use) [DECISION].

Flow (the client records; the recorder, upload and `recording.turn_audio_ready` are the call domain's, 03 4.10):

1. Offer: Salma's notes after session 2 carry the "opening tape of your season" card; offered again once in sessions 3 to 5 (the `notes` builder reads `recordings` to decide). Framing text from the package (the Milestone 0 Arabic message, adapted).
2. `api` creates `recordings {id, learner_id, season_number, kind: then|now, form, tasks: {retell: media_id, opinion: media_id, repeat: [media_id x 8]}, started_at, completed_at, kept: bool}` and emits `recording.completed` when all uploads are in; a partial recording (one task skipped) completes with nulls.
3. `recording/rate`: each task through `call/verbatim-turn` (surface `recording`); `comparable_segments` rows for `rec_retell`, `rec_opinion`; `rec_repeat` scored by alignment (4.4); then one pinned rater call.
4. Rater prompt (Sonnet 5.5, pinned, `output_config` structured, no thinking display needed): input is the two task transcripts (never both recordings of a pair, so it cannot know which is first), the band descriptors A2 to B2+ from the package, six anchor transcripts per band with their adjudicated bands, and the story's eight content points. Output: `{band: int 0..100, band_low, band_high, retell_points_present: [bool x 8], meaning_kept_repeat: [bool x 8] (for sentences with wer in 0.15..0.40 only), notes}`. The rater never produces a progress statement and never sees the learner's name.
5. `recording_ratings {recording_id, task, band, band_low, band_high, measures jsonb, repeat_scores int[], content_points bool[], rater_version_id, assessment_version}`; speaking re-anchored (4.5.6); structures in `stable` checked for confirmation (4.5.3); `recording.rated`.
6. Comparison [P1]: when a `now` recording is rated and a `then` exists for the previous season (or week 0), `claims.generate_then_and_now()` builds candidates per metric and task type with `before` = the earlier recording's value and `after` = this one's, through the gate; `finale_differences()` returns at most two passed claims ranked: `fluency_change(first_long_pause_s or mlr)` > `accuracy_change` > `complexity_change`, preferring claims whose evidence has audio.
7. Storage-off rule (PRD-v2 12.5.2): the recording's media is `ephemeral=true` unless the learner tapped "keep this recording"; the comparison then uses transcripts and measures only, and the finale says so in one line.
8. The season gate (PRD-v2 16.1 "the 4-weekly recording improves for most") is computed by the evaluation domain from `recording_ratings` and `claims`, never shown to learners.

### 4.11 Weekly proof and season finale

#### 4.11.1 `proof/make` (shell in 01; body here)

```python
async def proof_make(evt: ProofRequested):
    L = learner(evt.learner_id); week = evt.week_start
    sessions = sessions_in(L, week, week + 7)
    plan = ProofPlan(learner=L, week=week)
    plan.mode = "slow" if len(sessions) <= 1 else "normal"                                    # PRD-v2 11.1.4
    cands = claims.generate_weekly(L, window=(week - 14, week + 7))                             # metric kinds [P1] + events accrued this week
    passed = [c for c in cands if gate(c).passed] + claims.unshown_passed(L)                    # unshown event claims (owned words, first-evers) from the week
    plan.headline = rank_headline(passed)                                                       # then_and_now > mistake_gone > fluency/complexity/accuracy change > first_ever (structure) > word_owned > did_it
    plan.more = [c for c in passed if c is not plan.headline][:4]
    plan.worse = [c for c in passed if c.direction == "worse"]
    plan.retraction_notice = claims.notices_pending(L)                                          # PRD-v2 8.5
    plan.rhythm_line = rhythm_met_sentence(L, week) if rhythm_met(L, week) else None            # PRD-v2 3.9.3: nothing when not met
    plan.next_focus = last_plan(L).targets.grammar.label_ar                                     # from the teacher's current plan (02 EpisodePlan)
    plan.working_on = working_on_items(L)                                                       # at most 3, with one learner sentence each
    plan.cumulative = {"hours_heard": hours_heard(L), "minutes_spoken": minutes_spoken(L), "words_owned": owned_count(L)}   # monotonic counts only
    plan.flat = plan.headline is None and plan.mode == "normal"
    plan.flat_change = flat_change_sentence(last_plan(L)) if plan.flat else None                 # "the one thing I'm changing": the teacher's step_reason or next target
    plan.question = "worth_it"                                                                   # yes / mostly / no + optional why
    script = await proof_producer.write(plan)                                                    # Sonnet 5.5; claim sentences pasted verbatim by code into {slots}
    law_scan(script)                                                                             # same scanner as notes, plus: no claim sentence outside plan.headline/more/worse
    audio = await voice_studio.render(RenderJob(kind="proof", lines=script.lines, clips=plan.clip_refs(), voice=salma))
    episode_id = publish_proof_episode(L, script, audio)                                        # episodes.kind = proof; above Today; feed item
    mark_shown(plan.headline, plan.more, plan.worse, surface="proof")                            # claim_shown events
    await inngest.send("proof.ready", {...})
```

#### 4.11.2 The honest sentences

| Situation | Rule | Sentence slot (Arabic, from the package; the model fills names and the quoted evidence only) |
|---|---|---|
| Slow week (0 or 1 session) | about 45 s, about what has built up since the start, never about the week | cumulative counts, one owned word with its sentence if any, next focus |
| Flat week (normal mode, nothing passed) | say so plainly, name the one change | "أسبوع ثابت. الشي الوحيد اللي بغيّره: {flat_change}" |
| Worse (a passed decline) | the most likely supported reason, then the change | `accuracy_fell_while_trying`: "أخطاء أكثر هالأسبوع لأنك جرّبت {structure} {n} مرات؛ في {month} ما جرّبته ولا مرة"; `harder_task`, `long_gap`, `unknown` variants |
| Too early (metric has no SE yet) | not mentioned at all; the proof does not promise what it cannot measure | nothing |
| Retraction notice | one line, once | "صحّحت شي قلته قبل: {old claim} ما كان دقيق، وهذي الأدلة اللي عندي الحين" |

The simple P0 proof (PRD-v2 11.1.8) is this function with the metric kinds absent from `claims` because no `metric_calibration` row has `n_pairs ≥ 12`; nothing else differs.

#### 4.11.3 The proof producer prompt (Sonnet 5.5, batch pricing when the proof day is ≥ 6 h away, else standard)

```text
[SYSTEM, cached] You are Salma, producer of "For one". You script the weekly proof: about 2 minutes of audio you present, with the learner's own clips. You receive a PLAN. Every sentence about the learner's progress is already written in the plan under headline, more and worse; paste them where the slots are and do not add, soften, strengthen or paraphrase them. Everything else you write is linking text, the next focus, the working-on list and the question. Never a number except the ones in the plan's claim sentences and the cumulative counts. No praise of the person. No "keep it up", no "don't stop". {salma_bible} {english_share}
<<cache breakpoint>>
[USER] PLAN: {ProofPlan as JSON, claim sentences pre-rendered in Arabic by code from claim templates}
```

#### 4.11.4 Season finale [P1]

`season.boundary` is consumed by the pipeline to make the finale episode (02); the pipeline's writer receives `claims_passed` restricted by `finale_differences(learner_id, season)` (at most two, PRD-v2 11.2) plus the recap counts and the "out in the world" rows; this domain supplies the then-and-now clips through `recording_ratings` and the kept media, and the proof producer's narration for the comparison (the same slots as 4.11.2, "then and now" variant). When the learner skipped the "now" recording, `finale_differences()` returns only non-recording claims and a `no_recording=true` flag so the finale says so (PRD-v2 11.2.3).

### 4.12 External test hook [P1]

`external_tests {id, learner_id, provider: det|other, sitting: week0|week8, taken_at, overall, subscores jsonb (literacy, comprehension, conversation, production for DET), certificate_ref, consent_marketing bool default false, imported_by}`; imported by an admin CSV page (no API integration in the beta). A monthly job `calibration/external-report` computes, per skill, Pearson r between the internal `mu` at the sitting date and the mapped subscore (speaking ↔ conversation+production, listening ↔ comprehension, reading ↔ literacy, writing ↔ production), n, and the band-edge refit (an isotonic fit of internal scale to DET bands, written to `skill_scoring.yaml` as a proposal, applied by hand). Results feed `skill_calibration` (4.9 step 5) and the evaluation domain's gate report. Never shown to any learner; never in marketing without `consent_marketing`.

### 4.13 The teacher as consumer

What this domain writes that `briefs.compile('teacher')` (data domain) reads into `TeacherInput` (02 4.3):

| TeacherInput field | Written by | Rule honoured |
|---|---|---|
| `skills.*` with `{value, low, high}`, `huh_rate_2w_median`, `reading_speed_wpm` | 4.5.6, 4.4 | ranges on every estimate |
| `structure_map[]` with `state, acc_14d{correct, contexts}, avoidance, consecutive_targeted, examples[]` | 4.5.2 to 4.5.5 | clean contexts only in `acc_14d`; `consecutive_targeted` maintained here from `plan.targets` echoes |
| `error_profile[]` with `pattern` / `slip` and `blurred_meaning` share | 4.5.4 | 3-across-2 |
| `word_bank_summary.size_est, owned_count, recall_candidates, kept` | 4.5.1 (`recall_candidates` = lemmas with ≥ 2 taps across sessions) | PRD-v2 9.5.3 |
| `due_list` | the data domain's scheduler, fed by this domain's grades | PRD-v2 9.4 |
| `facts_usable`, `follow_ups_due`, `interests` | 4.6 | ladder, sensitivity, shelf life |
| `last_14_days[]` (`session_summaries`) | `finish` | uptake, energy signals (`short_turns`, `skipped_call`, `error_spike` = `errors_per_100` > 1.5× the 14-day median, `huh_spike`), talk share, abandoned |
| `claims_passed` | `claims_passed()` | only `status in (passed, shown)` |
| `energy.anxiety_flag` | from `calls.metrics.anxiety_mode` in the last 2 sessions | PRD-v2 5.4.7 |

Triggers (PRD-v2 9.1): `session.after_pass.completed` is the "after each session" trigger, consumed by `episode/produce`'s `wait_after_pass` (02); the nightly, follow-up-due and gap triggers are the pipeline's and the scheduler's. `working_on.changed` is consumed here too: a veto sets `vetoed=true` on the structure's patterns (4.5.4) and an addition is mapped by one Haiku call (`working_on.map`) from the learner's words to inventory structure ids and lemmas with a quote, written to `working_on_items` with `source=learner`, before the pipeline's same-day re-plan reads it.

### 4.14 Rebuilds and the propagation of a wrong memory

**`memory/correct`** (on `memory.flagged`, which `api` emits with the `wrong_memory_flag` event; and on the memory keeper's `corrections`):

1. Resolve the fact: by `fact_id` when the notebook flagged it; otherwise by matching the quote against facts mentioned in the last call's `callback` (the host brief's `callback.fact_id` is in the call bundle) and, failing that, by embedding similarity ≥ 0.85 on the disputed text; no match → `status=unresolved` and a review-queue item (human reads it within a day).
2. Fix at once: `status=deleted` (learner says it is false) or `superseded` with the learner's correction as `ground_truth` (they gave the right version); `dont_bring_up=true` when they say so. Dependents: `follow_ups` for the fact cancelled; `show_canon` rows citing the fact marked `invalid`; `interests` unaffected.
3. Fan out `facts.invalidated {learner_id, fact_ids}`: the pipeline drops the fact from any plan not yet voiced and re-runs editor check 4 on a voiced-but-unpublished episode (02's responsibility; assumption in section 9); the call bundle is recompiled at the next `POST /v1/calls` (03 4.2 already filters by current status).
4. Claims: a wrong memory is about a fact, and claims never cite facts; but when the learner's flag disputes a *quote* ("I never said that"), every claim whose evidence contains that quote is `retracted(reason="learner_disputed")` with `notice_pending=true`, and the event's `verbatim_status` is set to `disputed` so it can never be evidence again.
5. Count: `wrong_memory_flags / callbacks_shown` over 30 days, where `callbacks_shown` = host brief callbacks actually spoken (03 `moves`) plus Today's one-line memory; reported to the evaluation domain (PRD-v2 16.1 under 1 in 100).
6. The live apology ("My mistake, noted.") is the live role's line (03), triggered by the same flag.

**`assessment/rebuild`** (on `assessment_version` change, or by hand with a learner scope):

1. Create shadow copies of the affected stores for the scope (`word_bank_shadow`, `structure_map_shadow`, `error_profile_shadow`, `skills_shadow`, `comparable_segments_shadow`, `claims_shadow`).
2. Replay sessions in `occurred_at` order: re-run `analyst.full` (Haiku; the memory keeper is **not** re-run, so learner-confirmed facts and deletions survive [DECISION]), classifier, measures, updater, claim candidates; rate limit 5 learners in parallel.
3. Diff: every claim with `status=shown` in the live table that does not pass in the shadow becomes `retracted(reason="rebuild:{version}")` with `notice_pending=true`; passed claims that were never shown are simply replaced; new passes are ordinary candidates.
4. Swap in one transaction per learner, bump `learner_model_version`, emit `assessment.rebuild_completed`. The teacher's next run sees the new model; nothing is shown to the learner until the next proof carries the notice.
5. Cost ceiling per rebuild is computed first (sessions × $0.004) and the run refuses above `rebuild.max_cost_usd` (default $50) without a flag.

### 4.15 Configuration keys

| Key | Default | Note |
|---|---|---|
| `assessment.version` | `1.0.0` | stamped on every row; bump triggers calibration and rebuild |
| `asr.confidence_threshold` (package) | 0.70 | 10.14 |
| `analyst.model` / `analyst.effort` / `analyst.max_edits` | `claude-haiku-5-5` / `low` / 40 | |
| `analyst.fast.timeout_s` / `analyst.full.timeout_s` | 25 / 90 | |
| `notes.model` / `notes.timeout_s` / `notes.max_cards` | `claude-sonnet-5-5` / 25 / 3 | |
| `notes.stage1_budget_s` | 60 | hard step timeout; degraded path after |
| `memory.model` / `memory.similarity_threshold` / `memory.view_confirm_hours` | `claude-haiku-5-5` / 0.85 / 48 | |
| `memory.shelf_life_days.{job,city,people,event_dated,health,preference}` | 180/365/365/14/7/120 | package |
| `measures.*`, `claims.*` | section 4.8.4 | |
| `skills.R.{speaking,listening,reading,writing}` / `skills.Q` / `skills.var_cap` / `skills.R_recording` | 100/144/144/100 / 2 / 225 / 64 | 4.5.6 |
| `wordbank.prior.k` / `prior.n0` / `prior.produced_factor` | 1500 / 4 / 0.6 | 4.5.1 |
| `avoidance.window_days` / `min_sessions` / `min_opportunities` | 21 / 5 / 3 | 4.5.5 |
| `rater.model` / `rater.pinned_until` (vendors.yaml) | `claude-sonnet-5-5` / 2026-12-31 | window 1 |
| `recording.forms` / `recording.max_task_s` | [A,B,C,D] / 90 | package |
| `proof.default_day` / `proof.slow_week_max_sessions` / `proof.max_more` | 7 / 1 / 4 | 11.1 |
| `rebuild.max_cost_usd` / `rebuild.parallel_learners` | 50 / 5 | |
| `calibration.qwk_min` / `calibration.precision_min` / `calibration.min_samples` | 0.7 / 0.8 / 150 | 10.11 |
| `prompts.analyst/notes/memory/proof/rater.version` | semver | recorded on every artifact |

### 4.16 Schemas this domain owns

```sql
create table session_summaries (
  session_id uuid primary key references sessions(id),
  learner_id uuid not null, local_date date not null, episode_kind text, format text,
  evidence_quality text not null check (evidence_quality in ('full','partial','text_only')),
  learner_speech_ms int, talk_share numeric(4,3), turns_learner int, words_clean int, words_total int,
  uptake smallint, huh_per_min numeric(6,3), taps_per_100 numeric(6,3), transcript_opened boolean,
  errors_per_100 numeric(6,3), errors_by_category jsonb, targets jsonb,      -- {grammar:{structure_id, contexts, correct}, words:[{lemma, use}]}
  recall_gaps jsonb, retell_done boolean, talkback_asks int, energy_signals text[], anxiety_mode text, abandoned boolean,
  pronunciation_internal numeric(5,2), analyst_run_id text, assessment_version text not null, created_at timestamptz default now()
);
create index on session_summaries (learner_id, local_date desc);

create table comparable_segments (
  id uuid primary key default gen_random_uuid(), learner_id uuid not null, session_id uuid, call_id uuid, recording_id uuid,
  task_type text not null check (task_type in ('retell','round_two','rec_retell','rec_opinion','rec_repeat')),
  form text, difficulty_tag text, source_quality text not null default 'live', measurable boolean not null,
  t_start_ms int, t_end_ms int, event_ids uuid[] not null, pruned_words int, clean_share numeric(4,3),
  speech_rate numeric(6,2), articulation_rate numeric(6,3), mlr numeric(6,2), mid_clause_pause_rate numeric(6,2), first_long_pause_s numeric(6,2),
  fillers_per_100 numeric(6,2), repairs_per_100 numeric(6,2), mlc numeric(6,2), subordination_ratio numeric(4,3), mtld numeric(7,2), beyond_2000_share numeric(4,3),
  errors_per_100 numeric(6,2), ei_total smallint, assessment_version text not null, occurred_at timestamptz not null
);
create index on comparable_segments (learner_id, task_type, occurred_at desc);

create table claims (
  id uuid primary key default gen_random_uuid(), learner_id uuid not null,
  kind text not null check (kind in ('did_it','first_ever','word_owned','mistake_gone','fluency_change','complexity_change','accuracy_change','accuracy_fell_while_trying','talkback_falling','then_and_now')),
  metric text, task_type text, direction text check (direction in ('better','worse','event')),
  subject jsonb not null,                   -- {structure_id} | {lemma} | {can_do_id} | {category}
  before_value numeric, after_value numeric, before_points jsonb, after_points jsonb, sem_used numeric, threshold_used numeric,
  before_window daterange, after_window daterange, attempts_before int, attempts_after int, reason text,   -- for worse: trying|harder_task|long_gap|unknown
  text_ar text not null,                    -- rendered from the kind's template by code; the only sentence any surface may speak
  status text not null default 'candidate' check (status in ('candidate','passed','failed','shown','retracted')),
  failed_rule text, retracted_reason text, notice_pending boolean not null default false,
  shown_at timestamptz, shown_surface text, created_at timestamptz not null default now(),
  assessment_version text not null, rater_version_id uuid
);
create index on claims (learner_id, status, created_at desc);

create table claim_evidence (
  claim_id uuid references claims(id) on delete cascade, ord smallint,
  event_id uuid, segment_id uuid, recording_id uuid, quote text, corrected text,
  media_object_id uuid, t_start_ms int, t_end_ms int, clean boolean not null, source_quality text not null,
  label_ar text,                            -- "then" / "now" / "Tuesday"
  primary key (claim_id, ord)
);

create table metric_calibration (
  metric text not null, task_type text not null, n_pairs int not null, sem numeric not null, sd_diff numeric, mean_abs_diff numeric,
  computed_at timestamptz not null, assessment_version text not null, primary key (metric, task_type, assessment_version)
);
create table test_retest_pairs (learner_ref text, metric text, task_type text, x1 numeric, x2 numeric, days_apart numeric, source text, assessment_version text);

create table recordings (
  id uuid primary key default gen_random_uuid(), learner_id uuid not null, season_number int not null, kind text not null check (kind in ('then','now')),
  form text not null, tasks jsonb not null, offered_at timestamptz, started_at timestamptz, completed_at timestamptz, kept boolean not null default false, skipped boolean not null default false,
  unique (learner_id, season_number, kind)
);
create table recording_ratings (
  recording_id uuid references recordings(id), task text not null, band smallint, band_low smallint, band_high smallint,
  measures jsonb, repeat_scores smallint[], content_points boolean[], rater_version_id uuid, assessment_version text, rated_at timestamptz, primary key (recording_id, task)
);
create table rater_versions (id uuid primary key, window_start date, window_end date, model text, prompt_version text, calibration_run_id uuid);
create table calibration_samples (id uuid primary key, source text, surface text, learner_ref text, text text, audio_ref text, consent_data_use boolean, tags_a jsonb, tags_b jsonb, adjudicated jsonb, band_a smallint, band_b smallint, band_adjudicated smallint, created_at timestamptz);
create table calibration_runs (id uuid primary key, component text, model text, prompt_version text, assessment_version text, ran_at timestamptz, n int, qwk_band numeric, precision_by_tag jsonb, recall_by_tag jsonb, precision_claim_tags numeric, passed boolean, notes text);
create table skill_calibration (skill text primary key, calibrated boolean not null default false, qwk numeric, external_r numeric, n int, as_of timestamptz);

create table notes (id uuid primary key, learner_id uuid, session_id uuid, call_id uuid, cards jsonb not null, header text, text_ar text, audio_refs jsonb, degraded boolean default false, model_versions jsonb, assessment_version text, created_at timestamptz, shown_at timestamptz);
create table margin_notes (id uuid primary key, learner_id uuid, chat_id uuid, message_id uuid, edit jsonb, text_ar text, created_at timestamptz, unique (chat_id));
create table proofs (id uuid primary key, learner_id uuid, week_start date, mode text, plan jsonb, episode_id uuid, headline_claim_id uuid, more_claim_ids uuid[], worse_claim_ids uuid[], worth_it_answer text, worth_it_why text, created_at timestamptz, unique (learner_id, week_start));
create table external_tests (id uuid primary key, learner_id uuid, provider text, sitting text, taken_at date, overall numeric, subscores jsonb, certificate_ref text, consent_marketing boolean default false, imported_by text, imported_at timestamptz);
create table working_on_items (id uuid primary key, learner_id uuid, structure_id text, lemma text, label_ar text, example_quote text, source text check (source in ('teacher','learner')), vetoed boolean default false, created_at timestamptz, retired_at timestamptz);
```

The event payload update for `call_turn` (data domain's table) adds `verbatim_status`, `verbatim_words`, `clean_spans`, `clean_share`, `low_confidence_source`, `disputed` as described in 4.1.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detection | Fallback | Learner sees | Claims |
|---|---|---|---|---|
| Last turn's verbatim not back in 20 s | `wait_last_turn` timeout | Stage 1 uses the streaming text for that turn at `clean=false`; stage 2 waits for it up to 3 min, else `verbatim_failed` | Notes on time; the polish card never quotes that turn | None from that turn |
| Verbatim vendor down | adapter errors ≥ 5 in 10 min (`vendor/health`) | Secondary vendor (ElevenLabs Scribe) via `vendor_config`; both down: turns marked `verbatim_failed`, audio retained until success only if storage is on, else deleted at 15 min and the session is `text_only` | Notes from streaming text: header and reached-for card only, no polish card (PRD-v2 5.4.11: low confidence, no claims) | None from speech that session |
| Haiku structured output fails validation (schema error, quotes not found) | `analyst.validate` drop count > 50% of items, or SDK parse error | One retry with the failure list appended; then stage 1 ships header plus reached-for from the host's `talkback` events only (degraded notes); stage 2 marks `analyst_failed` and the session summary carries counts only | A short notes set | None |
| Sonnet notes text fails the law scan twice, or times out | scanner, 25 s timeout | Degraded card set: header, the "New for you" card rendered from the claim template (code), the reached-for word with its gloss from the gloss cache; no polish card | Still under 90 s | Unchanged |
| Stage 1 step exceeds 60 s | Inngest step timeout | Degraded card set as above; `notes.degraded=true`; a Sentry event | Under 90 s | |
| Stages 2 to 7 exceed 6 min | step deadline | `finish` runs with `evidence_quality=partial`; missing stores keep yesterday's rows; the teacher plans with `evidence_lag` (02) | Nothing | Candidates are generated only from completed stages |
| Memory keeper fails | error or timeout | Facts from this session are not stored; the session is queued for a nightly `memory/retry` (facts can wait a day; they are never spoken until usable anyway) | Nothing | n/a |
| `metric_calibration` has fewer than 12 pairs | nightly recompute | Metric claims fail with `no_standard_error`; the proof shows events only | A simpler proof | Only events |
| Rater model unavailable inside a pinned window | adapter error | The recording is rated by code measures only; `recording_ratings.band=null`; the comparison still works for code metrics; the band re-anchor is skipped; an ops page | The finale still plays the clips; measured differences only from code metrics | `then_and_now` claims on code metrics only |
| Vendor forces a rater model change mid-window | `pinned_until` violated by `vendor_config` | `recording/rate` refuses and pages; the window is closed early, `calibration/run` runs on the new model, a new `rater_versions` row starts, and no comparison crosses the boundary (rule 1) | A finale without the then-and-now sentence that month if the run has not passed | None across versions |
| Analyst overflow (≥ 40 edits) or `recognition_doubt` flag | validator, flag | Session marked for human review; its edits count at half weight for patterns (0.5 observation) and never for claims | Nothing | None |
| Crisis flag from the analyst | `flags.crisis` | `crisis.detected_after_session` at once; Salma's resources card at next open (client); logged for SB 243; the rest of the pass continues without a polish card that quotes the distress turn | The resources card once | None from that session |
| Learner disputes a quote | `wrong_memory_flag` on a claim's "how we know" | Claim retracted with notice; event `disputed` | One honest line next proof | Retracted |
| Rebuild changes a shown claim | diff in `assessment/rebuild` | Retracted with notice | One honest line next proof | Retracted |
| Spend alert ($1.00 per session) | cost middleware | Analyst and memory keeper fall to `analyst.fast` only for the day's remaining sessions; notes unchanged | Nothing | Candidates from the available evidence |
| Storage-off learner, pass slower than 15 min | `audio/expire` fires first | Audio gone; verbatim turns already done are kept; turns not yet transcribed are `verbatim_failed` | Nothing | None from those turns |

Too much for the team, and the cut: the full P1 metric claims depend on test-retest pairs that may not exist by 2027-01-10 for every metric. The cut is already in the design: each metric unlocks independently as its row reaches 12 pairs, and the proof's P0 form needs nothing unlocked. If build week 5 slips, the order to drop is: the margin note (4.7.5), avoidance (4.5.5), the external-test import page (4.12), then `assessment/rebuild` automation (run it by hand from a script).

---

## 6. Cost and performance against the budgets

Prices from the model table dated 2026-10-06 (Haiku 5.5 $0.10 / $0.50 per MTok; Sonnet 5.5 $2 / $10, cache reads $0.20; Batch at half) and [ASSUMPTION] vendor rates for STT and TTS, to be replaced by the cost domain's `prices.yaml`.

| Piece | Unit assumption | Per session | PRD-v2 14.5 line |
|---|---|---|---|
| Verbatim STT, 7 min of learner audio across call and round two at $0.004/min [ASSUMPTION AssemblyAI-class batch-verbatim rate] | $0.028 | $0.028 | Re-transcription and pronunciation $0.03 |
| Pronunciation, 1 to 3 known sentences at $0.002 each [ASSUMPTION] | $0.004 | $0.004 | (same line) |
| `analyst.fast` Haiku: 4k in (2.5k cached), 0.8k out | $0.0005 | | Analyst and memory keeper $0.04 |
| `analyst.full` Haiku: 9k in (3k cached), 2.5k out | $0.0019 | | |
| Memory keeper Haiku: 6k in, 1k out | $0.0011 | | |
| Margin note Haiku + Sonnet short: | $0.004 | $0.008 total for the four | |
| Salma's notes Sonnet: 3k in (2k cached), 0.4k out | $0.006 | | Notes and chat $0.04 (chat is 03's) |
| Polish-line TTS, 2 lines at about 120 characters at $0.00003/char [ASSUMPTION] | $0.007 | $0.013 | |
| Weekly proof: Sonnet batch script ($0.01) + 2 min Salma TTS ($0.05 [ASSUMPTION]) + clips (byte ranges, $0) ÷ 4 sessions | | $0.015 | Proof share and hosting $0.03 |
| Recording rater (Sonnet, 6k in, 0.5k out) once per 4 weeks ÷ 20 sessions | | $0.001 | |
| **Total this domain** | | **about $0.07** | **$0.14 allowed across the four lines** |

Headroom is real; the risk is not this domain's model cost but STT minutes if learners talk more (which is the goal): at 12 min of audio a session the STT line doubles to $0.05 and the total is still under the lines. Scale levers for the $0.35 target: Batch for `analyst.full` and the memory keeper when the drop is more than 6 h away (saves 50% of $0.003, not worth code in the beta), a single analyst call instead of fast plus full once notes latency is proven (saves $0.0005), and running the rater on Haiku once its calibration passes.

Performance: section 3.4 timelines. Postgres load per session: about 30 row writes and 6 reads; the stores are per-learner rows under RLS; nothing here scans across learners except the nightly `metric_calibration` recompute (reads `test_retest_pairs`, a few thousand rows) and `proof/fanout`.

---

## 7. Build plan for 2026-11-02 to 2026-12-06

| Week | Ships | P0 / P1 | What the pilot data lets us test |
|---|---|---|---|
| 1 (2026-11-02) | `structure_rules.yaml` v1 (about 120 structures, A2 to B2 core; the full few hundred by week 3), errant plus spaCy in the worker image, `edit_classifier` with unit tests on the Milestone 0 tags; `tools/import_m0_tags.py` into `calibration_samples`; `measures` on verbatim word timings; the 10.14 recognizer test run through `VerbatimRecognizer` on the 30 clips, which sets `asr.confidence_threshold`; `claims` and the gate module with the event kinds; schema migrations for every table in 4.16 | P0 | Classifier precision against Muath's tags on M0 calls (the first calibration number); which recognizer keeps learner errors; confidence distributions on real Saudi speech |
| 2 (2026-11-09) | `analyst` (both variants) with validation; `updater` (word bank, structure map, error profile, skills); `word_check.score`; `session/after-pass` stages 2 to 7 end to end on M0 transcripts replayed as synthetic sessions; `session_summaries` feeding the teacher (02 builds in the same week); forms C and D of the task bank | P0 | Replay all 14 days of each M0 learner and compare the structure map with the learner files' Structures tables; the teacher's targets against what Muath chose by hand |
| 3 (2026-11-16) | `memory_keeper` with the ladder and quote check (replay M0 intake and calls, compare with the hand-confirmed Life facts); `metric_calibration` recompute from M0 week-0 and week-3 recordings plus any extra test-retest pairs (section 10); `recording/rate` with code metrics and the rater prompt; `calibration/run` in CI | P0 (rating), P1 (comparison) | Fact precision against the hand-confirmed facts; false-fact rate; the first SEM numbers and how many metrics clear 12 pairs |
| 4 (2026-11-23) | `call/verbatim-turn` body wired to the live call (03 builds the call this week); stage 1 notes with the 90 s path, law scan, degraded path; `chat/margin-note`; `memory/correct` and `facts.invalidated` | P0 | Notes latency on the 50 scripted test calls; card selection on M0 transcripts judged by Muath against the notes he actually sent |
| 5 (2026-11-30) | `proof/make` simple version; the first "then" recording offer in notes; `assessment/rebuild` (script-run); the external-test import page; the end-to-end run with M0 learners; audit page listing `claims` with evidence | P0 (proof simple, first then), P1 (rebuild automation, external test) | A first weekly proof for each returning M0 learner built only from events; the monthly false-claim audit dry run on those proofs |
| Beta (2026-12-07 to 2027-01-10) | Metric claims unlock per metric as pairs reach 12; avoidance weekly job; finale differences at the first season boundaries (2027-01-03 onward for 2026-12-07 starters); DET week-0 sittings and the import; `calibration/run` on the first beta-tagged samples | P1 | False-claim audit under 5%; targets that hold in the next recording; recognizer error by first language |

Exit on 2026-12-07 for this domain: notes under 90 s on the 50 scripted calls (p95), `session.after_pass.completed` under 10 min (p99), classifier precision ≥ 0.8 on the claim-feeding tags of the M0 set (or those tags marked not claim-eligible), zero progress sentences anywhere that do not resolve to a `claims` row (a grep-level test over every Arabic string template plus the law scan in CI).

---

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Transcribe the whole call once after `call.ended` | 60 to 120 s of STT before the analyst can start; the 90 s notes budget becomes impossible; per-turn transcription also deletes storage-off audio sooner |
| Let the analyst (or Sonnet) assign structure ids and categories | Labels drift between runs and models; per-tag precision cannot be measured or pinned; ERRANT plus a rule table gives the same tag every time and a diff when the rules change |
| One Sonnet analyst call for everything (edits, facts, notes) | Three jobs with three standards: the analyst must be stingy, the memory keeper must quote, Salma must be warm; mixing them in one prompt produced the Milestone 0 pattern of notes quoting sentences that were not exactly said |
| Skip the fast analyst and reuse the full one for notes | The full pass needs the chat and the whole session; waiting for it would push notes past 90 s on long calls; the fast variant costs $0.0005 |
| A learned memory model (half-life regression) in the beta | No data to train on until months in; the FSRS-style scheduler (data domain) with this domain's grades gives most of the benefit with no training; revisit after 10,000 sessions |
| IRT or a per-item response model for skills | Same data problem; a Kalman scalar with fixed noise is explainable to Muath and to the learner ("a range that narrows slowly") |
| Claim thresholds as fixed constants per metric | A constant is a fabricated standard error; the PRD requires test-retest estimates, and the gate's `no_standard_error` failure is the honest state until they exist |
| Letting the proof producer prompt read the learner model | It would write progress sentences the gate never saw; the `ProofPlan` with pre-rendered claim sentences makes a fabricated win a code bug, not a prompt failure |
| A second human rater per recording in production | Cost and latency; humans stay in the calibration set and the monthly audit, which is where their judgment calibrates the machine |
| Re-running the memory keeper in rebuilds | Would resurrect facts the learner deleted and re-ask confirmed ones; facts are learner-governed, not model-governed |
| Marking a word "owned" by a probability threshold | Not explainable in one sentence; the two-sessions-a-day-apart rule is, and it is what the notebook shows |
| Counting fillers and repairs in fluency | r = −.20 with perceived fluency (assessment lens); logged for research, never weighted |
| Whole-call fluency | Confounded by the host's questions and the topic; comparable segments only |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check.

1. **System topology (01).** `session/after-pass`, `call/verbatim-turn`, `proof/make`, `audio/expire` shells exist with the triggers and concurrency in 01 4.3; this domain adds `chat/margin-note`, `recording/rate`, `assessment/rebuild`, `memory/correct`, `calibration/run` and `memory/retry` as functions in `workflows`; the worker image carries spaCy `en_core_web_sm`, `errant`, `wordfreq` and the CMU dictionary; `media_objects` byte-range reads are available in-region for clips; the proof is an `episodes` row of kind `proof` published above Today by the delivery path.
2. **Episode generation pipeline (02).** `episode/produce` waits on `session.after_pass.completed` (15 min) and reads `TeacherInput` through the data domain; `claims_passed` is quoted verbatim by the writer and nowhere else; the finale episode takes `finale_differences()`; `voice-studio.render` and `render_line` exist for the proof and the polish line in the throwing host's voice; the pipeline handles `facts.invalidated` by dropping the fact from unvoiced plans and re-running editor check 4 before publish; the fitter's realized target spans are available so `heard` state can be set from exposure; `plan.targets` is echoed back so `consecutive_targeted` can be maintained here.
3. **Live call and voice stack (03).** Per-turn upload and `call.turn_audio_ready` with `is_last` and `event_id`; `calls.metrics` with `learner_speech_ms`, `anxiety_mode`, `moves`; host `call_turn` events carry `moves.recast`, `recall_gap_id`, `retell`, `talkback_word` so prompted use can be computed; `recording.turn_audio_ready` with `surface` and the reference text for repeat sentences; `pronunciation.scored` or an equivalent signal when `call/pronunciation-score` writes the payload; the "my mistake, noted" line is triggered live from the same flag; the call bundle is compiled at `POST /v1/calls` so invalidated facts never reach a host.
4. **Learner model, event log and data platform.** `events` accepts the late-binding verbatim update per `call_turn` (or the second-event alternative); the nine stores expose write APIs for the fields in 4.5 and 4.6 and the FSRS-style scheduler accepts `scheduler.review(item, grade, at)`; `briefs.compile('teacher')` reads `claims_passed()` and `session_summaries` from this domain; `learner_model_version` is bumped by `finish` and by `assessment/rebuild`; a `notebook_viewed {fact_ids}` event exists for the "left unedited after viewing" rung; `working_on_edit` events are mirrored as `working_on.changed`.
5. **Client app, podcast feed and delivery.** The notes door renders `notes.cards` with ▶ by byte range and the "say it once" recorder; the chat renders `margin_notes` as the collapsed chip; the notebook's "working on", "words you own", "the tape" and "how we know" read `working_on_items`, the word bank's owned rows, `recordings` plus `recording_ratings`, and `claim_evidence`; the client emits `claim_shown {claim_id, surface}` and `note_shown`; the recording screen enforces 90 s per task and offers "keep this recording"; `chat.closed`, `chat.learner_message`, `recording.completed` and `memory.flagged` are emitted by `api`.
6. **Security, privacy, consent and compliance.** Verbatim vendors are approved processors for audio in transit; `calibration_samples` holds text only unless `consent_data_use` and voice storage both hold; anonymization of `learner_ref` is defined there; the SB 243 crisis log consumes `crisis.detected_after_session`; `external_tests` rows are learner-scoped PII under the same RLS.
7. **Cost model, vendor strategy and tracing.** `prices.yaml` carries verbatim STT per-minute, pronunciation per-utterance and Salma TTS per-character rates; every model call here passes through the adapter middleware with `role in (analyst, memory_keeper, salma_text, proof_producer, rater, verbatim_stt, pronunciation)`; `vendors.yaml roles.rater.pinned_until` is honoured by `vendor_config` (a runtime override of the rater is refused while pinned).
8. **Evaluation, observability and operations.** The monthly false-claim audit samples `claims` with `status=shown` and their `claim_evidence`; "targets that hold in the next recording", "delayed recall", "talkback use over weeks", "recognizer error by first language" and "wrong memories per 100 callbacks" are computed from `structure_map`, `word_bank`, `session_summaries`, the 10.14 report and the counter in 4.14; `analyst_validation_drop`, `notes.degraded`, `evidence_quality` and gate failure counts by rule are dashboard series; the offline suite (6.7) calls `analyst` and `edit_classifier` on planted-error transcripts and reports tag precision.

---

## 10. Open for Muath

1. **[OPEN for Muath] Test-retest pairs before 2026-12-07.** The claim gate's metric rules cannot open until a metric has 12 pairs of recordings 2 to 7 days apart (D11). Milestone 0 gives week-0 and week-3 pairs (two weeks apart, which measure growth plus noise, not noise). Ask 8 to 10 Milestone 0 learners to record the week-0 form once more 3 to 5 days later (about 3 minutes each, framed as "a second take so I can hear the difference between a day and a month"), or accept that fluency and accuracy claims open only in January.
2. **[OPEN for Muath] The second tagger for calibration.** PRD-v2 10.11 needs double-tagged samples. Budget: one English teacher for about 15 hours (150 samples at 6 minutes) by build week 3, paid; or Muath tags twice with a week between, which is weaker but free. The precision bar cannot be reported without a second set of tags.
3. **[OPEN for Muath] English Grammar Profile permission (Part 18 #8).** `structure_rules.yaml` is seeded from it in week 1. If permission is refused by 2026-11-09, the inventory is rewritten from the CEFR Companion Volume descriptors and public learner-corpus lists, which costs about three days and loses the per-band evidence.
4. **[OPEN for Muath] External test (Part 18 #9).** Default DET at week 0 and week 8 for 20 to 30 learners; roughly $70 a sitting (estimate, not a quote), about $4,000 total, paid by For one. The week-0 sitting must happen in the learner's first 7 days, so the invitation and payment flow needs to exist by 2026-12-07 even though the import page is P1.
5. **[OPEN for Muath] Notes when voice storage is off.** The polish card then shows the learner's sentence as text with the natural version in the host's voice. The assessment lens suggests saying at consent time that this loses the most motivating part; the exact sentence is brand voice and consent wording (legal review).
6. **[OPEN for Muath] Whether a worse week with an unknown reason is said.** This design says it ("a worse week on X, and I cannot say why yet") because the trust contract prefers honesty to silence; the alternative is to say nothing when no supported reason exists. Product call.
7. **[OPEN for Muath] The rater's first window.** Pinned to Sonnet 5.5 until 2026-12-31 in `vendors.yaml`. The first beta learners' finales fall on or after 2027-01-03, so the first comparison crosses a window boundary unless the window is extended to 2027-01-31. Recommendation: windows aligned to beta cohorts (2026-12-07 to 2027-01-31), which this document assumes.
8. **[OPEN for Muath] Forms C and D of the then-and-now task bank.** Someone writes them to the Milestone 0 template in build week 2; this is content, not code. If nobody does, season 2 reuses A and B eight weeks after first use, which the design tolerates.
9. **[OPEN for Muath] Data-use consent wording for calibration samples.** Transcripts of consenting beta learners enter `calibration_samples` and are read by a paid tagger. The Controls switch text must say a person may read anonymized transcripts; counsel's wording.
