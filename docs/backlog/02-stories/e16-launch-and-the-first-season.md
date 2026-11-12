# E16 · Launch and the first season

*All domains. Version 1 launches once, publicly, with open signup, when every v1 story passes and the launch checklist in `00-release-plan.md` is green (ADR-25.1, 25.5). English is the only target language unless another passes the gate. The beta gates are now launch health measures, read 4 and 8 weeks after launch with the same targets and stop lines.*

### E16-S01 · Launch: signup opens
**As an** operator, **I want** signup opened to everyone once the launch checklist is green, **so that** version 1 starts on a product that is ready rather than on a date.
- **Given** the launch checklist, **when** every line is green and Muath approves the production deploy, **then** the landing page goes live and the first signups' first sound, first-episode time and first spoken sentence are on the measures page the same day.
- Size: S · Priority: P0 · Phase: Launch · Release: v1 · Domain: 09 Operations · Depends on: E06-S02, every v1 story in E01 to E15
- Requirements: FR-004

### E16-S02 · The daily rhythm after launch
**As an** operator, **I want** a morning checklist the agent runs and reports to Muath (drops, fallbacks, cost, alerts, review queue) and a weekly digest, **so that** one person can run the product.
- **Given** a week, **when** it ends, **then** the digest shows the signup week's trial-to-paid, sessions, speech minutes and cost.
- Size: S · Priority: P0 · Phase: Launch · Release: v1 · Domain: 09 Operations · Depends on: E15-S06, E15-S11
- Requirements: enabling (no FR)

### E16-S04 · v1.1 features shipped after launch
**As a** learner, **I want** round two, the finale, the tape, shadowing and the dial-in experiment to arrive after launch, **so that** the product grows while I use it.
- **Given** each v1.1 story, **when** shipped, **then** it goes out behind a flag with its suite passing and is noted in the digest.
- Size: L · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: all · Depends on: E05-S13, E11-S09, E10-S09
- Requirements: FR-118, FR-318, FR-345, FR-346, FR-920, FR-1013

### E16-S05 · First false-claim audit and wrong-memory count
**As an** operator, **I want** the first monthly false-claim audit a month after launch and the wrong-memory rate read weekly, **so that** the trust measures are read from real data.
- **Given** the audit, **when** Muath completes it, **then** the rate is on the launch health page (target under 5%) with the retractions made.
- Size: S · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 09 Operations · Depends on: E11-S10
- Requirements: NFR-502

### E16-S06 · First season finales
**As a** learner, **I want** my finale at my first session on or after day 28 of my season, with the next goal set inside it, **so that** season one ends with something to hear.
- **Given** the first finales, **when** produced, **then** each has at most two measured differences or an honest "too early to say", and the next goal is stored.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 02 Pipeline, 05 Assessment · Depends on: E11-S09
- Requirements: FR-920

### E16-S07 · Per-language quality and the close rule
**As an** operator, **I want** worth-it, false-claim and recognizer-error rates per target language and per learner first language, and a rule that closes a language that falls well behind until fixed, **so that** opening many languages never means shipping a bad one.
- **Given** a language open (a target, or a first language whose speakers learn English), **when** its worth-it rate is more than 15 points below the English-target average for two weeks, or its recognizer error is well behind, **then** it closes to new learners and the digest says why.
- Size: S · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 09 Operations · Depends on: E15-S09, E02-S08
- Requirements: FR-1107, NFR-504

### E16-S08 · Cost path executed: batch voices and the negotiated rate
**As an** operator, **I want** batch text-to-speech and the negotiated voice rate (register A9) in production after launch, **so that** cost moves toward $0.35.
- **Given** the weekly cost report, **when** both are live, **then** the measured cost per session is below $0.60 and each lever's saving is a measured line.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 08 Cost · Depends on: E14-S08
- Requirements: FR-1326, NFR-403, NFR-404

### E16-S09 · Launch health reviews at 4 and 8 weeks
**As an** operator, **I want** a one-page reading of every launch health measure against its target and stop line, 4 and 8 weeks after launch, with the failed claim named if any, **so that** each decision is made on the reading.
- **Given** the launch health page, **when** snapshotted at 4 and at 8 weeks, **then** each measure is pass, fail or not readable, and the document names the one change each failure implies.
- Size: S · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 09 Operations · Depends on: E15-S09
- Requirements: enabling (no FR)

### E16-S10 · The plan after the 8-week review
**As an** operator, **I want** the next season planned from the 8-week review: prices confirmed (ADR-24.5), the floor stack migrated piece by piece behind blind tests, the observer tested behind a flag, a second language opened if it passed, **so that** the first weeks' lessons shape what follows.
- **Given** the review, **when** the plan is written, **then** each item names the measure it depends on.
- Size: M · Priority: LATER · Phase: Later · Release: later · Domain: all · Depends on: E16-S09
- Requirements: FR-557, FR-1309
