# E11 · Weekly proof, claim gate, recordings and seasons

*Architecture domains 05 and 02. Law 12: no claim without proof. The claim gate in code is the only route from the learner model to any progress statement.*

### E11-S01 · The claim gate
**As an** operator, **I want** a code module that passes a claim only if it is like for like, beyond about twice the metric's standard error, from at least 2 data points, from clean evidence, and openable, **so that** the product is believed on good weeks because it admits flat ones.
- **Given** a claim with one data point, **when** gated, **then** it fails with the reason stored.
- **Given** any progress sentence template in the codebase, **when** CI greps, **then** each resolves to a `claims` row or the build fails.
- Size: M · Priority: P0 · Week: W1 · Domain: 05 Assessment · Depends on: E09-S03

### E11-S02 · Claims storage and "how we know"
**As a** learner, **I want** to open the evidence behind any claim, **so that** nothing about my progress is asserted without proof.
- **Given** a shown claim, **when** "how we know" is tapped, **then** the clips, dates and measure appear and `mark_claim_shown` is recorded.
- Size: S · Priority: P0 · Week: W5 · Domain: 05 Assessment, 06 Client · Depends on: E11-S01

### E11-S03 · The proof producer
**As a** learner, **I want** a 2-minute episode from Salma every week with one headline piece of evidence and what comes next, shorter in a slow week, honest in a flat week, **so that** I hear what I can now do.
- **Given** a week with no passed claim, **when** the proof is made, **then** it says the week was flat and names the one thing the teacher is changing.
- **Given** fewer than 2 sessions, **when** the proof is made, **then** it is about 45 s and about what has built up over time.
- **Given** the proof script, **when** scanned, **then** it contains no list of mistakes and no string from the law corpus.
- Size: L · Priority: P0 (simple) · Week: W5 · Domain: 05 Assessment, 02 Pipeline · Depends on: E11-S01, E04-S05

### E11-S04 · Proof screen and the worth-it question
**As a** learner, **I want** the proof on my chosen day with "how we know" and one question, "was this week worth your time?", **so that** the product measures what matters.
- **Given** the proof day, **when** it arrives, **then** it is one of the three allowed messages and the worth-it answer is stored as a measure.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E11-S03, E08-S03

### E11-S05 · Then-and-now recording
**As a** learner, **I want** to record about 3 minutes (a retell, an opinion, 8 repeat sentences) after session 2 and every 4 weeks, skippable, with nothing scored on screen, **so that** I can hear my own voice then and now.
- **Given** the recording screen, **when** completed, **then** `recording.completed` is appended, the audio is under the learner's key, and no number is shown.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client, 03 Live call · Depends on: E05-S12

### E11-S06 · Test-retest pairs and metric unlock
**As an** operator, **I want** each metric to make claims only once 12 test-retest pairs exist for it, **so that** early claims are cautious, especially in a new language.
- **Given** the gates page, **when** opened, **then** it shows per metric and per language how many pairs exist and the date claims unlock.
- Size: M · Priority: P1 · Week: Beta · Domain: 05 Assessment · Depends on: E09-S09, E11-S01

### E11-S07 · Seasons and the goal in the learner's words
**As a** learner, **I want** a 4-week season with one real goal in my own words, set with Salma, **so that** there is a near goal without a level.
- **Given** a season starts, **when** the goal is set, **then** it appears in the teacher brief and in "why this episode" reasons.
- Size: M · Priority: P0 · Week: W4 · Domain: 02 Pipeline, 04 Learner model · Depends on: E04-S12

### E11-S08 · Mid-season rehearsal
**As a** learner, **I want** a real-life rehearsal of my actual scene mid-season, **so that** the show is the gym and life is the game.
- **Given** a rehearsal episode, **when** produced, **then** the call brief carries the scene and the host plays the other side.
- Size: M · Priority: P0 · Week: W5 · Domain: 02 Pipeline · Depends on: E11-S07, E04-S02

### E11-S09 · The season finale
**As a** learner, **I want** a finale with both recordings side by side, at most two measured differences in plain words, my real-world attempt, and next season's goal set inside it, **so that** finishing never becomes a reason to stop.
- **Given** the first session on or after day 28, **when** it runs, **then** the finale kind is produced and the next goal is asked for before the goodbye.
- Size: L · Priority: P1 · Week: Beta (from 20 January) · Domain: 02 Pipeline, 05 Assessment · Depends on: E11-S05, E11-S06, E11-S07

### E11-S10 · False-claim audit
**As an** operator, **I want** a monthly sample of shown claims checked by a person against the evidence, **so that** the false-claim rate is known (target under 5%).
- **Given** the audit page, **when** a reviewer marks a claim false, **then** it is retracted from the notebook and the metric updates.
- Size: S · Priority: P1 · Week: Beta (first on 1 January) · Domain: 09 Operations · Depends on: E11-S02, E15-S08
