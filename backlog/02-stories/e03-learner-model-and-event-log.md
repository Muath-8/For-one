# E03 · Learner model and event log

*Architecture domain 04. Rule: live roles never write; only after-session roles write, from an append-only event log; every life fact carries the learner's exact words.*

### E03-S01 · Append-only events with idempotent append
**As an** engineer, **I want** an `events` table partitioned by month with RLS, a typed payload registry and `events.append` with idempotency keys and clock-skew handling, **so that** the whole learner model can be rebuilt from the log.
- **Given** the same event sent twice with one idempotency key, **when** appended, **then** exactly one row exists.
- **Given** a client timestamp 3 hours in the future, **when** appended, **then** the server time is stored and the skew recorded.
- Size: M · Priority: P0 · Week: W1 · Domain: 04 Learner model · Depends on: E01-S02

### E03-S02 · Word bank with spaced scheduling
**As a** teacher role, **I want** a per-word bank with known-word probability, priors from frequency and the word check, and an FSRS-style scheduler per word, structure and corrected form, **so that** the language comes back when it is about to be forgotten.
- **Given** a word with predicted recall below 0.85 by the next drop time, **when** `due_list` runs, **then** the word is due.
- **Given** the pilot learner files' hand-kept "next due" column, **when** `due_list` is compared, **then** 80% of items agree.
- Size: L · Priority: P0 · Week: W1 · Domain: 04 Learner model · Depends on: E03-S01, E02-S06

### E03-S03 · Structure map and error profile
**As a** teacher role, **I want** a structure map with 14-day accuracy windows and an error profile where an error (not a slip) needs 3 observations across 2 sessions, **so that** the hosts bring back the right forms of real mistakes, not one-off slips.
- **Given** two observations of the same error in one session, **when** the updater runs, **then** it is still a slip; a third in a later session makes it an error with a `working_on` candidate.
- Size: M · Priority: P0 · Week: W2 · Domain: 04 Learner model · Depends on: E03-S01, E02-S06

### E03-S04 · Life facts with the learner's exact words
**As a** learner, **I want** every fact the show knows about me stored with the sentence I said, a confidence, a sensitivity class and an expiry, **so that** the show only uses what I told it.
- **Given** a proposed fact without a verbatim quote found in the transcript, **when** `verify_quote` runs, **then** the fact stays `heard_once` and never reaches a brief.
- **Given** a fact in a sensitive class (health, money, relationships, religion, politics), **when** the learner did not raise it themselves, **then** it is never stored.
- **Given** the confirmed facts in the pilot learner files, **when** replayed against the imported transcripts, **then** 100% pass the quote check.
- Size: M · Priority: P0 · Week: W2 · Domain: 04 Learner model · Depends on: E03-S01

### E03-S05 · Interests, goals, show canon and the series bible
**As a** writer role, **I want** interests with decay, the season goal in the learner's words, show canon (side characters capped at 3 to 5, places, running jokes) and a series bible excerpt, **so that** the show stays one show.
- **Given** a sixth side character proposed, **when** the canon write runs, **then** it is refused and the writer is told to reuse one.
- Size: M · Priority: P0 · Week: W2 · Domain: 04 Learner model · Depends on: E03-S01

### E03-S06 · Compiled briefs per role
**As a** role, **I want** `briefs.compile(role)` for teacher, writer, host, Salma, chat and proof returning only what that role needs, with confirmed facts only, **so that** no role ever sees the whole file.
- **Given** a host brief, **when** compiled, **then** it holds the call plan, the recall gaps, the due words, the forms to echo, and at most 2 confirmed life facts, and fits the cached prompt budget.
- **Given** an unconfirmed fact, **when** any brief is compiled, **then** it is absent.
- Size: L · Priority: P0 · Week: W2 to W4 · Domain: 04 Learner model · Depends on: E03-S02, E03-S04, E03-S05

### E03-S07 · Onboarding writes and word-check scoring
**As a** learner, **I want** my intake cards, word-check answers and consents to seed my model, **so that** my first episode is pitched at my level.
- **Given** 48 word-check answers (36 real, 12 pseudowords), **when** scored, **then** the band estimate matches the pilot kit's method and pseudoword hits lower the confidence.
- **Given** the 15 pilot word checks, **when** rescored, **then** every estimate reproduces the kit's number.
- Size: M · Priority: P0 · Week: W3 · Domain: 04 Learner model · Depends on: E03-S02, E06-S04

### E03-S08 · Player, article, chat and call event ingestion
**As a** teacher role, **I want** play, huh, tap, keep, article scroll, followed-answer, chat and call-turn events ingested end to end from the web app and the worker, **so that** the model sees what the learner actually did.
- **Given** a learner taps a word twice, **when** events arrive, **then** the word becomes a recall candidate.
- **Given** an api outage of 5 minutes, **when** the client queue retries, **then** no event is lost or duplicated.
- Size: M · Priority: P0 · Week: W3 to W4 · Domain: 04 Learner model, 06 Client · Depends on: E03-S01, E07-S04

### E03-S09 · Apply the after-session result
**As a** teacher role, **I want** `apply_after_pass` to update words, structures, errors, skills, interests, facts, canon, the scheduler and the notebook counts in one transaction, **so that** the next plan reads a consistent model.
- **Given** one pilot learner's 14 imported sessions, **when** the full after-pass replays, **then** the word bank's owned words and the pattern errors agree with Muath's hand-kept file on 80% of items.
- Size: L · Priority: P0 · Week: W5 · Domain: 04 Learner model · Depends on: E03-S06, E09-S06

### E03-S10 · Learner edits: veto, add, fix a memory
**As a** learner, **I want** to veto or add a "working on" item, correct or delete a fact, and flag a wrong memory, **so that** I steer the teacher and a wrong memory is fixed at once.
- **Given** a veto, **when** saved, **then** the teacher is re-triggered the same day and the next plan no longer targets the item.
- **Given** a fact deleted, **when** any later brief compiles, **then** the fact is absent and a `facts.invalidated` event exists.
- **Given** a `wrong_memory_flag`, **when** raised, **then** it counts toward the wrong-memory metric (target under 1 in 100 callbacks).
- Size: M · Priority: P0 · Week: W5 · Domain: 04 Learner model · Depends on: E03-S04, E10-S02

### E03-S11 · Export, purge order and rebuild
**As a** learner, **I want** an export of everything about me and a deletion that purges in a known order, **so that** the data is mine.
- **Given** an export request, **when** the job runs, **then** every JSON opens, transcripts are included, and the link is emailed within 1 hour.
- **Given** a deletion, **when** the purge runs, **then** the `deletion_ledger` lists every store in order and `privacy/verify` passes.
- **Given** a code-version bump, **when** `learner/rebuild` replays the log, **then** the diff is reported as a count.
- Size: L · Priority: P0 (rebuild P1) · Week: W5 · Domain: 04 Learner model, 07 Security · Depends on: E03-S01, E13-S06
