# E09 · After-session assessment

*Architecture domain 05. Nothing in assessment runs in the live path. Salma's after-call notes, the margin note and the polish card are dropped (decision 3); what remains feeds the next episodes and the claim gate.*

### E09-S01 · Verbatim recognizer and the confidence threshold
**As an** analyst role, **I want** a `VerbatimRecognizer` on the chosen vendor with disfluencies kept and a per-language confidence threshold from the 30-clip test, **so that** the learner's errors survive transcription.
- **Given** the 30 pilot clips, **when** run, **then** `low_confidence_reason` is set correctly against the package threshold and the error-survival rate is recorded as the baseline.
- Size: M · Priority: P0 · Week: Phase 4 · Due: Day-1 · Domain: 05 Assessment · Depends on: E02-S02
- Requirements: FR-801, FR-804, FR-862

### E09-S02 · Structure rules and the edit classifier
**As an** analyst role, **I want** `structure_rules.yaml` and an `edit_classifier` that turns minimal edits into structure-inventory tags by rules (errant plus spaCy), **so that** errors are classified the same way every time.
- **Given** Muath's pilot tags, **when** the classifier runs on the same calls, **then** precision is at least 0.8 on the claim-feeding tags, or those tags are marked not claim-eligible.
- Until it ships: as E03-S03: edits kept unclassified, classified by a rebuild on landing.
- Size: L · Priority: P0 · Week: Beta · Due: beta day 14 (2027-03-30) · Domain: 05 Assessment · Depends on: E02-S06
- Requirements: FR-803, FR-815, FR-1320

### E09-S03 · Measures from timings
**As an** analyst role, **I want** fluency measures (speech rate, pause length, mean length of run, words used and understood) computed from verbatim word timings, **so that** claims have numbers with known noise.
- **Given** the pilot week-0 and week-3 recordings, **when** measures run, **then** the standard error per metric is computed from the test-retest pairs.
- Until it ships: only event claims ship (first-ever, words owned), which need no fluency measure.
- Size: M · Priority: P0 · Week: Beta · Due: beta day 21 (2027-04-06) · Domain: 05 Assessment · Depends on: E09-S01
- Requirements: FR-613, FR-805, FR-810, FR-811, FR-812

### E09-S04 · The analyst with a fixed schema
**As a** teacher role, **I want** an analyst that reads the verbatim call and the session events and outputs a fixed schema (errors, words produced, recall gaps hit, retell measures, talk share), validated by code, **so that** the model is updated from checked data.
- **Given** output that fails the schema, **when** validated, **then** the pass retries once and then marks the session degraded, never writing partial data.
- **Given** the edit classifier has not shipped (it is due later), **when** the analyst's minimal edits are stored, **then** they are kept unclassified in the log and classified by a rebuild when E09-S02 lands.
- Size: L · Priority: P0 · Week: Phase 4 · Due: Day-1 · Domain: 05 Assessment · Depends on: E09-S01
- Requirements: FR-602, FR-802, FR-1310

### E09-S05 · The memory keeper
**As a** learner, **I want** life facts proposed only with my exact quote, a confidence ladder (heard once, repeated, confirmed) and a shelf life, **so that** a wrong memory is rare and fixable.
- **Given** the pilot intakes and calls replayed, **when** compared with the hand-confirmed facts, **then** fact precision is above 0.9 and the false-fact rate below 1 in 100.
- Size: M · Priority: P0 · Week: Phase 4 · Due: Day-1 · Domain: 05 Assessment, 04 Learner model · Depends on: E03-S04, E09-S04
- Requirements: FR-620, FR-621, FR-623, FR-806, FR-1311

### E09-S06 · The after-session pass end to end
**As a** teacher role, **I want** `session/after-pass` to run verbatim, analyst, memory keeper, updater, session summary and the teacher trigger within 10 minutes of a session, **so that** tomorrow's plan uses today's call.
- **Given** a session ends, **when** the pass runs, **then** `session.after_pass.completed` fires under 10 minutes p99 and the teacher is triggered once (triggers coalesce).
- **Given** each pilot learner's 14 days replayed, **when** compared with the learner files' structures tables, **then** the structure map agrees on 80% of items.
- Size: L · Priority: P0 · Week: Phase 4 · Due: Day-1 · Domain: 05 Assessment · Depends on: E09-S04, E09-S05, E03-S09
- Requirements: FR-351, FR-701, FR-807, NFR-112

### E09-S07 · Skills with ranges and "where do I stand"
**As a** learner, **I want** separate listening, speaking, reading and writing estimates with ranges, said honestly only when I ask and only for calibrated skills, **so that** I get a real answer and never a number pushed at me.
- **Given** an uncalibrated skill, **when** asked, **then** Salma says it is too early to say, with what would make it possible.
- Until it ships: Salma's prompt says plainly she cannot say reliably yet, for every skill (FR-846's uncalibrated case).
- Size: M · Priority: P0 · Week: Beta · Due: beta day 21 (2027-04-06) · Domain: 05 Assessment · Depends on: E09-S06, E09-S08
- Requirements: FR-613, FR-619, FR-845, FR-846, FR-1019

### E09-S08 · Calibration samples and `calibration/run`
**As an** operator, **I want** Muath's pilot tags imported as calibration samples and a CI job that reports classifier precision and rater agreement (quadratic weighted kappa about 0.7), **so that** the internal measure is checked against a person.
- **Given** a prompt or rule change, **when** CI runs, **then** calibration numbers are compared with the baseline and a drop beyond the threshold fails the build.
- **Given** no second tagger yet (recruited from the native-reader pool by build week 5, ADR-24.14), **when** claims are gated, **then** only event claims ship and metric claims stay off.
- Until it ships: only event claims ship (ADR-24.14).
- Size: M · Priority: P0 · Week: Beta · Due: beta day 28 (2027-04-13) · Domain: 05 Assessment, 09 Operations · Depends on: E09-S02, E15-S02
- Requirements: FR-860, NFR-206

### E09-S09 · The recording rater
**As an** operator, **I want** then-and-now recordings rated by code metrics plus a calibrated model, per language, **so that** the 4-weekly comparison is like for like.
- **Given** a recording pair, **when** rated, **then** accuracy, fluency and complexity measures and a rater judgment are stored with the metric's standard error.
- Until it ships: the week-4 recordings are stored and rated when this ships; nothing is shown before the finale (P1).
- Size: M · Priority: P0 (rating), P1 (comparison) · Week: Beta · Due: beta day 28 (2027-04-13) · Domain: 05 Assessment · Depends on: E09-S03, E09-S08
- Requirements: FR-851, FR-1313

### E09-S10 · Wrong-memory correction path
**As a** learner, **I want** a wrong fact fixed at once from the notebook and never used again, **so that** a wrong memory is treated as a bug.
- **Given** `memory/correct`, **when** called, **then** `facts.invalidated` is appended, the brief cache for the learner is cleared and the metric increments.
- Size: S · Priority: P0 · Week: Phase 4 · Due: Day-1 · Domain: 05 Assessment · Depends on: E09-S05, E03-S10
- Requirements: FR-626

### E09-S11 · The weekly avoidance flag
**As a** teacher role, **I want** structures expected at the learner's estimate that they have never attempted to be flagged once a week, **so that** avoided forms get input flood first and then an avoidance treatment.
- **Given** the weekly run, **when** a structure expected at the learner's speaking estimate has obligatory contexts but no attempt in the learner-local rolling 7 days (ADR-24.B21), **then** its avoidance flag is set in the structure map and the teacher's next plan treats it by the treatment rules; nothing is shown to the learner.
- Until it ships: avoided structures get no special treatment; nothing is shown either way.
- Size: S · Priority: P0 · Week: Beta · Due: beta day 21 (2027-04-06) · Domain: 05 Assessment · Depends on: E09-S02, E03-S03
- Requirements: FR-611, FR-823
