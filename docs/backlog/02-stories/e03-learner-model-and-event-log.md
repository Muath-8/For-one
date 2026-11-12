# E03 · Learner model and event log

*Architecture domain 04. Rule: live roles never write; only after-session roles write, from an append-only event log; every life fact carries the learner's exact words.*

### E03-S01 · Append-only events with idempotent append
**As the** coding agent, **I want** an `events` table partitioned by month with RLS, a typed payload registry and `events.append` with idempotency keys and clock-skew handling, **so that** the whole learner model can be rebuilt from the log.
- **Given** the same event sent twice with one idempotency key, **when** appended, **then** exactly one row exists.
- **Given** a client timestamp 3 hours in the future, **when** appended, **then** the server time is stored and the skew recorded.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 04 Learner model · Depends on: E01-S02
- Requirements: FR-601, FR-602, FR-603

### E03-S02 · Word bank with spaced scheduling
**As a** teacher role, **I want** a per-word bank with known-word probability, priors from frequency and the word check, and an FSRS-style scheduler per word, structure and corrected form, **so that** the language comes back when it is about to be forgotten.
- **Given** a word with predicted recall below 0.85 by the next drop time, **when** `due_list` runs, **then** the word is due.
- **Given** synthetic learners with planted review histories and the expected due dates, **when** `due_list` is compared, **then** 80% of items agree.
- Size: L · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S01, E02-S06
- Requirements: FR-610, FR-619, FR-720, FR-1320

### E03-S03 · Structure map and error profile
**As a** teacher role, **I want** a structure map with 14-day accuracy windows and an error profile where an error (not a slip) needs 3 observations across 2 sessions, **so that** the hosts bring back the right forms of real mistakes, not one-off slips.
- **Given** two observations of the same error in one session, **when** the updater runs, **then** it is still a slip; a third in a later session makes it an error with a `working_on` candidate.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S01, E02-S06
- Requirements: FR-611, FR-612, FR-704, FR-820

### E03-S04 · Life facts with the learner's exact words
**As a** learner, **I want** every fact the show knows about me stored with the sentence I said, a confidence, a sensitivity class and an expiry, **so that** the show only uses what I told it.
- **Given** a proposed fact without a verbatim quote found in the transcript, **when** `verify_quote` runs, **then** the fact stays `heard_once` and never reaches a brief.
- **Given** a fact in a sensitive class (health, money, relationships, religion, politics, sexuality) that the learner raised, **when** it is proposed, **then** it is usable in the same session only, and is kept for later sessions only after the learner taps the one-tap confirmation card in the notebook (E10-S04); a spoken "yes" is not enough (ADR-24.10). A sensitive fact the learner did not raise is never stored.
- **Given** the facts planted in the synthetic transcripts, **when** replayed, **then** 100% of the real ones pass the quote check and every planted paraphrase fails it.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S01
- Requirements: FR-615, FR-620, FR-621, FR-622, FR-623

### E03-S05 · Interests, goals, show canon and the series bible
**As a** writer role, **I want** interests with decay, the season goal in the learner's words, show canon (side characters capped at 3 to 5, places, running jokes) and a series bible excerpt, **so that** the show stays one show.
- **Given** a sixth side character proposed, **when** the canon write runs, **then** it is refused and the writer is told to reuse one.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S01
- Requirements: FR-505, FR-540, FR-614, FR-616, FR-618, FR-624

### E03-S06 · Compiled briefs per role
**As a** role, **I want** `briefs.compile(role)` for teacher, writer, host, Salma, chat and proof returning only what that role needs, with confirmed facts only, **so that** no role ever sees the whole file.
- **Given** a host brief, **when** compiled, **then** it holds the call plan, the recall gaps, the due words, the forms to echo, and at most 2 confirmed life facts, and fits the cached prompt budget.
- **Given** an unconfirmed fact, **when** any brief is compiled, **then** it is absent.
- Size: L · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S02, E03-S04, E03-S05
- Requirements: FR-640, FR-641, FR-642, FR-643, FR-644, FR-645

### E03-S07 · Onboarding writes and word-check scoring
**As a** learner, **I want** my intake cards, word-check answers and consents to seed my model, **so that** my first episode is pitched at my level.
- **Given** 48 word-check answers (36 real, 12 pseudowords), **when** scored, **then** the band estimate follows the package's scoring method and pseudoword hits lower the confidence.
- **Given** 15 fixture word checks with expected bands, **when** rescored, **then** every estimate reproduces the expected band.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S02, E06-S04
- Requirements: FR-121, FR-845, FR-850

### E03-S08 · Player, article, chat and call event ingestion
**As a** teacher role, **I want** play, huh, tap, keep, article scroll, followed-answer, chat and call-turn events ingested end to end from the web app and the worker, **so that** the model sees what the learner actually did.
- **Given** a learner taps a word twice, **when** events arrive, **then** the word becomes a recall candidate.
- **Given** an api outage of 5 minutes, **when** the client queue retries, **then** no event is lost or duplicated.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 04 Learner model, 06 Client · Depends on: E03-S01, E07-S04
- Requirements: FR-316, FR-372, FR-603, FR-617, FR-723

### E03-S09 · Apply the after-session result
**As a** teacher role, **I want** `apply_after_pass` to update words, structures, errors, skills, interests, facts, canon, the scheduler and the notebook counts in one transaction, **so that** the next plan reads a consistent model.
- **Given** a synthetic learner's 14 scripted sessions with planted words and error patterns, **when** the full after-pass replays, **then** the word bank's owned words and the pattern errors agree with the planted truth on 80% of items.
- **Given** a structure or word, **when** the updater runs, **then** its lifecycle moves only by the rules (heard, attempting, active target, taking, stable), and "owned" or "learned" is set only for correct, unprompted use in two different sessions at least a day apart.
- Size: L · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S06, E09-S06
- Requirements: FR-602, FR-805, FR-821, FR-822, FR-1321

### E03-S10 · Learner edits: veto, add, fix a memory
**As a** learner, **I want** to veto or add a "working on" item, correct or delete a fact, and flag a wrong memory, **so that** I steer the teacher and a wrong memory is fixed at once.
- **Given** a veto, **when** saved, **then** the teacher is re-triggered the same day and the next plan no longer targets the item.
- **Given** a fact deleted, **when** any later brief compiles, **then** the fact is absent and a `facts.invalidated` event exists.
- **Given** a `wrong_memory_flag`, **when** raised, **then** it counts toward the wrong-memory metric (target under 1 in 100 callbacks).
- Size: M · Priority: P0 · Phase: Phase 5 · Release: v1 · Domain: 04 Learner model · Depends on: E03-S04, E10-S02
- Requirements: FR-626, FR-706, FR-1011

### E03-S11 · Export, purge order and rebuild
**As a** learner, **I want** an export of everything about me and a deletion that purges in a known order, **so that** the data is mine.
- **Given** an export request, **when** the job runs, **then** every JSON opens, transcripts are included, and the link is emailed within 1 hour (ADR-24.B7).
- **Given** a deletion, **when** the purge runs, **then** the `deletion_ledger` lists every store in order and `privacy/verify` passes.
- **Given** a code-version bump, **when** `learner/rebuild` is run as a script over the log (the automated runner waits, per architecture 04's cut), **then** the diff is reported as a count and no claim already shown is retracted silently.
- Size: L · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 04 Learner model, 07 Security · Depends on: E03-S01, E13-S06
- Requirements: FR-630, FR-1046, FR-1047
