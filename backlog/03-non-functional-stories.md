# For one: non-functional stories

*The requirements that cut across every epic: latency, cost, privacy, deletion, evaluation, reliability, accessibility. Each is a story with acceptance criteria and the epic that owns the implementation. These are P0 unless marked.*

## Latency

### NF-01 · The host answers within about a second
**As a** learner, **I want** the host to reply within about a second of my turn ending, **so that** the call feels like a conversation.
- **Given** the 50 scripted calls, **when** measured, **then** reply latency median is under 1.5 s and p95 under 2.5 s, and connect is under 3 s.
- **Given** production, **when** a day's calls are measured, **then** `host_reply_p50` over 1.5 s for an hour pages.
- Owner: E05, E02-S04, E15-S04 · Size: cross-cutting · Due: Day-1
- Requirements: NFR-107

### NF-02 · First sound in under 60 seconds, first sentence in under 5 minutes
- **Given** a first open on a 4G phone, **when** measured on the pilot learners' re-onboarding, **then** Salma's voice plays under 60 s, the pilot plays under 45 s after intake, and the learner's first spoken sentence is under 5 minutes.
- Owner: E06 · Alert: `first_sound_slow` · Due: Day-1
- Requirements: FR-120, NFR-101, NFR-102, NFR-104

### NF-03 · The dropped episode starts in under 2 seconds; on-demand kinds in under 30 seconds
- **Given** a dropped episode, **when** Play is tapped, **then** sound starts under 2 s; **given** a swap, return or sample, **then** streaming starts under 30 s.
- Owner: E07-S03, E04-S08 · Alerts: `dropped_start_slow`, `on_demand_slow` · Due: Day-1
- Requirements: NFR-103, NFR-105, NFR-106

### NF-04 · The word sheet opens in under 300 ms; the word button answers in under 2 s
- Owner: E07-S06, E05-S07 · Alerts: `word_sheet_slow`, `talkback_p50` · Due: Day-1
- Requirements: NFR-108, NFR-110

### NF-05 · The after-session pass finishes within 10 minutes and tomorrow's episode is ready before the drop
- **Given** a session end, **when** the pass runs, **then** `session.after_pass.completed` under 10 minutes p99; **given** the drop time, **then** 95% of episodes were ready before it, and the batch falls back to on-demand at drop minus 90 minutes.
- Owner: E09-S06, E04-S07, E08-S02 · Alert: `episode_not_ready_before_drop` · Due: Day-1
- Requirements: NFR-112, NFR-113

## Cost

### NF-06 · Cost per session under $0.60 in the beta, with a costed path to $0.35
**As an** operator, **I want** every session's cost measured against the $0.60 budget and the $0.64 estimate, **so that** the stop line ($1.00 with no plan) is never crossed unseen.
- **Given** the pilot learners' production week, **when** rolled up, **then** the measured cost per session is in the exit document beside the estimate, with the levers to $0.35 each carrying a measured first column.
- **Given** a session over $1.00, **when** rolled up, **then** it pages with the role breakdown; **given** p50 over $0.80 for 7 days, **then** it pages.
- **Given** no plan may lose money at full use at $0.35, **when** prices are confirmed, **then** the 2 and 3 a day plans break even at $0.42 or below.
- Owner: E14, E16-S08 · Due: Day-1
- Requirements: FR-011, NFR-401, NFR-402, NFR-403, NFR-404, NFR-405

### NF-07 · The sample episode costs under $0.05 and a trial under $8
- Owner: E06-S01, E14-S05 · Due: Day-1
- Requirements: NFR-406

### NF-08 · Daily spend is capped and a runaway halts
- **Given** the daily cap, **when** reached, **then** non-live vendor calls halt and the on-call is paged; live calls finish.
- Owner: E14-S04 · Due: Day-1
- Requirements: NFR-403, NFR-404

## Privacy and deletion

### NF-09 · Told, not inferred
- **Given** any brief, **when** compiled, **then** only confirmed, quote-backed facts appear; sensitive classes never appear unless the learner raised them; no enrichment or external lookup about a person exists in the codebase (a dependency allow-list test).
- Owner: E03-S04, E03-S06, E13-S09 · Due: Day-1
- Requirements: FR-620, FR-621, FR-622

### NF-10 · Deletion and export on the clock
- Voice storage off: call audio deleted within 15 minutes of call end. Revoke: all audio within 24 hours. Export: within 72 hours while fulfilled by hand, 1 hour once automated (ADR-24.B7). Account deletion: access ends at once with no grace (ADR-24.B1), live purge within 24 hours, backups within 30 days. Trial ended unpaid: 90 days of archive access, then one email, then deletion.
- **Given** each window, **when** `privacy/verify` runs daily, **then** a missed window pages.
- Owner: E13-S05, E13-S06, E13-S11, E12-S05 · Due: Day-1 (audio windows automatic; deletion by runbook in 24 hours; export by hand in 72 hours); beta day 35 (2027-04-20) for the automated export and purge
- Requirements: FR-1046, FR-1047, FR-1048, NFR-304

### NF-11 · No personal data in logs, traces or third parties beyond the register
- **Given** the scrub corpus, **when** tests run, **then** zero leaks; Langfuse retention is 30 days with per-user deletion; every vendor in `vendors.yaml` has a DPA or terms and a training opt-out recorded.
- Owner: E15-S01, E13-S02 · Due: Day-1
- Requirements: NFR-306

### NF-12 · Every learner's audio under their own key
- Owner: E13-S01, E01-S08 · Due: Day-1
- Requirements: NFR-302

### NF-13 · AI disclosure and the crisis protocol in every live role
- **Given** "are you real?", **when** asked of any character in any language, **then** a plain answer; **given** a crisis keyword, **then** step-out, quarantine and the resources card.
- Owner: E05-S11, E13-S08 · Due: Day-1
- Requirements: FR-560, FR-571

## The laws, enforced by the build

### NF-14 · No game furniture can be built
- **Given** a component for a streak, points, level, percentage, chart, leaderboard or confetti, **when** lint runs, **then** the build fails; counts are plain text and monotonic.
- Owner: E07-S01, E10-S05 · Due: Day-1
- Requirements: FR-224, FR-1001, FR-1017

### NF-15 · Nothing reads as a correction
- **Given** any generated surface (episode, call, chat, proof, feed note), **when** the law scan runs, **then** no string from the corpus ("wrong", "the correct answer", "you should have said", homework phrasing) appears; the host's per-call budgets hold (1 recast per turn, 3 clarifications, 1 nudge).
- Owner: E04-S04, E05-S02, E15-S03 · Due: Day-1
- Requirements: FR-333, FR-420, FR-837

### NF-16 · No claim without proof
- **Given** any progress sentence template, **when** CI greps, **then** it resolves to a `claims` row; the first false-claim audit on 1 January shows under 5%.
- Owner: E11-S01, E11-S10 · Due: Day-1
- Requirements: FR-840, NFR-502

### NF-17 · Exactly three kinds of outbound message
- **Given** the codebase, **when** the messaging test runs, **then** only the drop notification, the one opt-in gap note and transactional email (sign-in code, receipts, the day-6 trial email, payment failed, export ready, account deleted) can be sent; the weekly proof sends nothing of its own; no re-engagement job exists.
- Owner: E08 · Due: Day-1
- Requirements: FR-008, FR-240

## Evaluation and quality

### NF-18 · A prompt change cannot ship without its suite
- **Given** a change to a prompt, bible or rule, **when** CI runs, **then** `eval-gate` runs the mapped suites and a regression beyond threshold fails the build; the release manifest records every version.
- Owner: E15-S03, E15-S05 · Due: Day-1
- Requirements: NFR-206, NFR-501

### NF-19 · Calibration against a person
- Classifier precision at least 0.8 on claim-feeding tags; rater agreement about 0.7 quadratic weighted kappa; 150 to 200 double-tagged samples by the end of the beta; a human reads 10 random episodes per learner per month.
- Owner: E09-S08, E15-S08 · Due: beta day 28 (2027-04-13)
- Requirements: FR-860, NFR-503

### NF-20 · Coverage and variety measured on every episode
- About 95% known words for audio and 98% for text (dial per learner); no format three times in a row; cosine similarity against the last 20 under the threshold set from the pilot's "too alike" pairs.
- Owner: E04-S03, E04-S11 · Due: beta day 8 (2027-03-24)
- Requirements: FR-432, FR-433, FR-730

## Reliability and operations

### NF-21 · No session is lost to a voice failure
- **Given** a live voice failure, **when** detected, **then** the call falls back to voice notes with the same host; **given** a voice vendor outage, **then** the secondary carries the same day's production.
- Owner: E05-S10, E14-S07 · Due: Day-1
- Requirements: NFR-202, NFR-203

### NF-22 · A missed drop pages within 5 minutes and has a runbook
- Owner: E15-S04, E15-S06 · Due: Day-1
- Requirements: NFR-201

### NF-23 · Production restored from backup once before the beta
- Owner: E01-S09 · Due: Day-1
- Requirements: NFR-207

### NF-24 · Capacity for 50 concurrent learners at the morning peak
- **Given** the drop minute for 250 learners, **when** load-tested, **then** media p95 first byte under 500 ms; **given** 15 concurrent calls, **then** no degradation in reply latency.
- Owner: E01-S08, E05 (load test in W5) · Due: Day-1
- Requirements: NFR-105, NFR-107

## Accessibility and languages

### NF-25 · Works in the learner's own language, including right-to-left
- **Given** Arabic, Hebrew, Persian or Urdu as the learner's language, **when** any screen renders, **then** the bidi snapshot suite passes and logical properties are used throughout (lint).
- Owner: E07-S01 · Due: Day-1
- Requirements: FR-010, NFR-601

### NF-26 · Usable with a screen reader and on a mid-range Android
- Lighthouse performance above 85; every control labelled; captions on the call.
- Owner: E07-S12 · Due: Day-1
- Requirements: NFR-603, NFR-604

### NF-27 · A language opens only through the gate
- **Given** a language package, **when** marked shippable, **then** all five checks passed in the harness and the result page is linked from the release manifest.
- Owner: E02-S06 (English, through the Milestone 0 gate run), E02-S08 (P1, the harness for other languages) · Due: Day-1
- Requirements: FR-1101, NFR-605
