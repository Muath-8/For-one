# E16 · Founding beta and season one

*All domains. 23 December 2026 to 26 January 2027, English only, about 50 learners a week into 7-day trials. The gate review is on 26 January; the first season after the beta runs 27 January to 23 February.*

### E16-S01 · Cohort 1 invited on 23 December
**As an** operator, **I want** the first batch of about 50 invites sent from the waitlist on 23 December, with the pilot learners first, **so that** the beta starts on the day.
- **Given** the batch, **when** sent, **then** redemptions, first sound and first spoken sentence are on the measures page the same day.
- Size: S · Priority: P0 · Week: Beta · Domain: 09 Operations · Depends on: E06-S02, every P0 story in E01 to E15

### E16-S02 · Weekly cohorts and the 08:30 checklist
**As an** operator, **I want** a new batch each week and a daily checklist (drops, fallbacks, cost, pages, review queue), **so that** the beta runs on a rhythm.
- **Given** a week, **when** it ends, **then** the digest shows the cohort's trial-to-paid, sessions, speech minutes and cost.
- Size: S · Priority: P0 · Week: Beta · Domain: 09 Operations · Depends on: E15-S06, E15-S11

### E16-S03 · External test at week 0 and week 8
**As an** operator, **I want** 20 to 30 learners to take a recognized test at week 0 and week 8 with the results imported, **so that** the internal measure is checked against the world.
- **Given** the import page, **when** results are loaded, **then** correlation with the internal skill estimates is shown per skill.
- Size: M · Priority: P1 · Week: Beta · Domain: 05 Assessment · Depends on: E09-S07; test choice (open)

### E16-S04 · P1 features shipped during the beta
**As a** learner, **I want** round two, the finale, the tape, shadowing, Apple and Google sign-in and the dial-in experiment to arrive during the beta, **so that** the product grows while I use it.
- **Given** each P1 story, **when** shipped, **then** it goes out behind a flag with its suite passing and is noted in the digest.
- Size: L · Priority: P1 · Week: Beta · Domain: all · Depends on: E05-S13, E11-S09, E10-S09, E06-S10

### E16-S05 · First false-claim audit and wrong-memory count
**As an** operator, **I want** the first false-claim audit on 1 January and the wrong-memory rate read weekly, **so that** the trust gates are read from real data.
- **Given** the audit, **when** done, **then** the rate is on the gates page (target under 5%) with the retractions made.
- Size: S · Priority: P1 · Week: Beta · Domain: 09 Operations · Depends on: E11-S10

### E16-S06 · First season finales from 20 January
**As a** learner who started on 23 December, **I want** my finale on my first session on or after day 28, with the next goal set inside it, **so that** season one ends with something to hear.
- **Given** the first finales, **when** produced, **then** each has at most two measured differences or an honest "too early to say", and the next goal is stored.
- Size: M · Priority: P1 · Week: Beta · Domain: 02 Pipeline, 05 Assessment · Depends on: E11-S09

### E16-S07 · Per-language quality and the close rule
**As an** operator, **I want** worth-it and false-claim rates per language, and a rule that closes a language that falls well behind English until fixed, **so that** opening many languages never means shipping a bad one.
- **Given** a second language open, **when** its worth-it rate is more than 15 points below English for two weeks, **then** it closes to new learners.
- Size: S · Priority: P1 · Week: Beta · Domain: 09 Operations · Depends on: E15-S09, E02-S08

### E16-S08 · Cost path executed: batch voices and the January prices
**As an** operator, **I want** batch text-to-speech and the January voice plan executed during the beta, **so that** cost moves toward $0.35 while the beta runs.
- **Given** the week of 28 December, **when** the next-week-prices report runs, **then** the January rises are in it and the measured cost per session is below $0.60.
- Size: M · Priority: P1 · Week: Beta · Domain: 08 Cost · Depends on: E14-S08

### E16-S09 · Gate review on 26 January
**As an** operator, **I want** a one-page reading of every gate against its pass and stop lines, with the failed claim named if any, **so that** the decision is made on the day.
- **Given** the gates page, **when** snapshotted on 26 January, **then** each gate is pass, fail or not readable, and the document names the one change each failure implies.
- Size: S · Priority: P0 · Week: Beta · Domain: 09 Operations · Depends on: E15-S09

### E16-S10 · Season two plan (27 January to 23 February)
**As an** operator, **I want** the first post-beta season planned from the gate review: public prices confirmed, the floor stack migrated piece by piece behind blind tests, the observer tested behind a flag, and the second language opened if it passed, **so that** the beta's lessons become the launch.
- **Given** the review, **when** the plan is written, **then** each item has a gate it depends on and a date.
- Size: M · Priority: LATER · Week: After beta · Domain: all · Depends on: E16-S09
