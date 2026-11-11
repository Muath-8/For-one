# E12 · Plans, trial and payments

*Architecture domains 07 and 01. Three plans differ only in new episodes a day. Paddle is the merchant of record (ADR-24.4; Stripe with Stripe Tax only if Paddle declines the account, register A6); the prices are $19.99 / $29.99 / $44.99 with the founding lock for the first 100 payers (ADR-24.5).*

### E12-S01 · Plan catalogue and the recommended plan
**As a** learner, **I want** three plans shown plainly (1 a day $19.99, 2 a day $29.99 marked Recommended, 3 a day $44.99), with "about $1 a day" and the tutor comparison, **so that** the choice is honest and easy.
- **Given** the plans page, **when** rendered, **then** no countdown, scarcity, pre-ticked upgrade or guilt copy exists (law lint corpus) and the per-episode price is shown.
- Size: S · Priority: P0 · Week: Phase 5 · Due: Day-1 · Domain: 06 Client · Depends on: E07-S01
- Requirements: FR-005, FR-1202, FR-1230, FR-1231

### E12-S02 · Allowance enforced on the server
**As an** operator, **I want** new episodes per active day and one swap enforced in `day/next`, with listening, the article, the chat and round two unlimited, **so that** no plan loses money at full use and no client can bypass it.
- **Given** a 1-a-day learner, **when** a second new episode is requested by any route, **then** it is refused; replays and round two are allowed.
- **Given** a 2 or 3 a day learner, **when** the day's other ideas are chosen, **then** they are made on demand the same day.
- Size: M · Priority: P0 · Week: Phase 3 · Due: Day-1 · Domain: 01 Topology · Depends on: E08-S02
- Requirements: FR-006, FR-206, FR-209

### E12-S03 · Trial ledger
**As a** learner, **I want** a 7-day trial on 2 a day with no card, **so that** I try the real thing before paying.
- **Given** the account is created, **when** the trial starts, **then** the ledger records the plan and end date; a second trial for the same email or device is refused.
- Size: S · Priority: P0 · Week: Phase 3 · Due: Day-1 · Domain: 07 Security · Depends on: E06-S08
- Requirements: FR-007, FR-1201

### E12-S04 · Checkout and subscriptions
**As a** learner, **I want** to pay through Paddle's hosted checkout with a card, Apple Pay, Google Pay or PayPal (ADR-24.B4), prices shown in my currency where Paddle supports it and tax handled for me, **so that** I keep the full product after the trial.
- **Given** a checkout, **when** Paddle confirms, **then** `subscriptions` holds the plan and `payment_events` the verified webhook; a replayed webhook changes nothing.
- **Given** a country Paddle cannot sell into, **when** checkout opens, **then** it is refused with a plain message (ADR-24.9).
- Size: L · Priority: P0 · Week: Phase 5 · Due: Day-1 · Domain: 07 Security, 06 Client · Depends on: E12-S01; the Paddle account under the legal entity by 2026-12-02 (A6)
- Requirements: FR-1202, FR-1204

### E12-S05 · Day-7 and trial-ended states
**As a** learner, **I want** a clear day-7 choice and, if I do not pay, my archive, notebook, export and delete kept for 90 days, **so that** nothing is held hostage.
- **Given** day 6 of the trial, **when** it starts, **then** one plain email says the trial ends tomorrow; payment is asked for once, on day 7.
- **Given** the trial ends unpaid, **when** Today opens, **then** the archive and notebook remain readable, no new episode is made, and after 90 days one email precedes deletion.
- Size: M · Priority: P0 · Week: Phase 5 · Due: Day-1 · Domain: 06 Client · Depends on: E12-S04
- Requirements: FR-240, FR-1048, FR-1201

### E12-S06 · Founding members keep their price
**As a** founding member, **I want** my plan's price locked for as long as I stay subscribed, **so that** the promise is real.
- **Given** one of the first 100 paying learners, **when** prices change, **then** their subscription keeps the original price.
- Until it ships: the founding order is the order of first payments in Paddle, kept in `payment_events`; the lock only matters when a price changes (ADR-24.5).
- Size: S · Priority: P0 · Week: Beta · Due: beta day 28 (2027-04-13) · Domain: 07 Security · Depends on: E12-S04
- Requirements: FR-1203

### E12-S07 · One-tap cancel
**As a** learner, **I want** to cancel in one tap from controls with no retention flow, **so that** "never manipulate" holds at the exit.
- **Given** cancel, **when** tapped, **then** billing stops at period end, access continues to then, and no message other than a receipt is sent.
- **Given** a refund request within 14 days of the first payment, **when** made, **then** it is refunded in full; after that there are no refunds for part-months (ADR-24.B16).
- Until it ships: every Paddle receipt carries Paddle's own cancel link, and "cancel" in Controls sends a request the on-call completes in Paddle the same working day (runbook line in E15-S06).
- Size: S · Priority: P0 · Week: Beta · Due: beta day 21 (2027-04-06) · Domain: 06 Client, 07 Security · Depends on: E12-S04
- Requirements: FR-1022, FR-1233

### E12-S08 · Billing reconcile
**As an** operator, **I want** a job that reconciles subscriptions with the processor's records and flags mismatches, **so that** nobody is charged for what they do not have.
- **Given** a mismatch, **when** found, **then** it is listed on the admin page with the learner id tokenized.
- Size: M · Priority: P1 · Week: Beta · Domain: 07 Security · Depends on: E12-S04
- Requirements: FR-1204

### E12-S09 · Regional prices
**As an** operator, **I want** country-level prices once there is data on where learners come from, **so that** the product is affordable where incomes are lower.
- **Given** a region list, **when** prices are set, **then** the price shown and charged match per country.
- Size: M · Priority: LATER · Week: After beta · Domain: 07 Security · Depends on: E12-S04
- Requirements: FR-1206

### E12-S10 · Plan changes
**As a** paying learner, **I want** to move between 1, 2 and 3 a day from Controls, told plainly when it takes effect, **so that** the plan follows my life.
- **Given** an upgrade, **when** confirmed, **then** the new allowance starts at the next drop and Paddle prorates the charge; **given** a downgrade, **then** it takes effect at the next billing date with no proration (ADR-24.B3); the sheet says which in one sentence, and unused allowance is never refunded or carried.
- **Given** a learner who reached the day's limit on 3 or more days in a week, **when** that week's proof is made, **then** it ends with one plain line naming the next plan and its price, once; a learner who used less than half the allowance for 4 weeks hears once that a smaller plan exists; no other upgrade prompt exists anywhere (law lint corpus).
- Until it ships: "change plan" in Controls sends a request the on-call completes in Paddle within one working day, stating when it takes effect (runbook line in E15-S06).
- Size: M · Priority: P0 · Week: Beta · Due: beta day 28 (2027-04-13) · Domain: 06 Client, 07 Security · Depends on: E12-S04, E11-S03
- Requirements: FR-209, FR-1205, FR-1231

### E12-S11 · Failed payments and the grace week
**As a** paying learner, **I want** one plain email if a payment fails and a 7-day grace in which the show continues, **so that** a card problem never costs me my show overnight.
- **Given** Paddle reports a failed renewal, **when** the webhook is verified, **then** one plain email is sent and the show continues for 7 days; after that new episodes stop and the account behaves as a trial that ended unpaid (archive, notebook, export and delete for 90 days).
- **Given** a successful payment, **when** it settles, **then** Paddle's receipt is the only email sent.
- Until it ships: Paddle's own failed-payment emails and retries run; the on-call applies the 7-day grace by hand (runbook line in E15-S06).
- Size: S · Priority: P0 · Week: Beta · Due: beta day 37 (2027-04-22) · Domain: 07 Security · Depends on: E12-S04, E12-S05
- Requirements: FR-240, FR-1048, FR-1232
