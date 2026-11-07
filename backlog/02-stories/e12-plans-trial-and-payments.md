# E12 · Plans, trial and payments

*Architecture domains 07 and 01. Three plans differ only in new episodes a day. The merchant of record and the exact prices are open (blocking items B5 and B6); the stories assume Stripe test mode until decided and $19.99 / $29.99 / $44.99.*

### E12-S01 · Plan catalogue and the recommended plan
**As a** learner, **I want** three plans shown plainly (1 a day $19.99, 2 a day $29.99 marked Recommended, 3 a day $44.99), with "about $1 a day" and the tutor comparison, **so that** the choice is honest and easy.
- **Given** the plans page, **when** rendered, **then** no countdown, scarcity, pre-ticked upgrade or guilt copy exists (law lint corpus) and the per-episode price is shown.
- Size: S · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E07-S01; prices confirmed (B6)

### E12-S02 · Allowance enforced on the server
**As an** operator, **I want** new episodes per active day and one swap enforced in `day/next`, with listening, the article, the chat and round two unlimited, **so that** no plan loses money at full use and no client can bypass it.
- **Given** a 1-a-day learner, **when** a second new episode is requested by any route, **then** it is refused; replays and round two are allowed.
- **Given** a 2 or 3 a day learner, **when** the day's other ideas are chosen, **then** they are made on demand the same day.
- Size: M · Priority: P0 · Week: W3 · Domain: 01 Topology · Depends on: E08-S02

### E12-S03 · Trial ledger
**As a** learner, **I want** a 7-day trial on 2 a day with no card, **so that** I try the real thing before paying.
- **Given** the account is created, **when** the trial starts, **then** the ledger records the plan and end date; a second trial for the same email or device is refused.
- Size: S · Priority: P0 · Week: W3 · Domain: 07 Security · Depends on: E06-S08

### E12-S04 · Checkout and subscriptions
**As a** learner, **I want** to pay by card or Apple Pay through a web checkout, **so that** I keep the full product after the trial.
- **Given** a checkout, **when** the processor confirms, **then** `subscriptions` holds the plan and `payment_events` the verified webhook; a replayed webhook changes nothing.
- Size: L · Priority: P0 · Week: W3 to W5 · Domain: 07 Security, 06 Client · Depends on: E12-S01; merchant of record (B5)

### E12-S05 · Day-7 and trial-ended states
**As a** learner, **I want** a clear day-7 choice and, if I do not pay, my archive, notebook, export and delete kept for 90 days, **so that** nothing is held hostage.
- **Given** the trial ends unpaid, **when** Today opens, **then** the archive and notebook remain readable, no new episode is made, and after 90 days one email precedes deletion.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E12-S04

### E12-S06 · Founding members keep their price
**As a** founding member, **I want** my plan's price locked for as long as I stay subscribed, **so that** the promise is real.
- **Given** one of the first 100 paying learners, **when** prices change, **then** their subscription keeps the original price.
- Size: S · Priority: P0 · Week: W5 · Domain: 07 Security · Depends on: E12-S04

### E12-S07 · One-tap cancel
**As a** learner, **I want** to cancel in one tap from controls with no retention flow, **so that** "never manipulate" holds at the exit.
- **Given** cancel, **when** tapped, **then** billing stops at period end, access continues to then, and no message other than a receipt is sent.
- Size: S · Priority: P0 · Week: W5 · Domain: 06 Client, 07 Security · Depends on: E12-S04

### E12-S08 · Billing reconcile
**As an** operator, **I want** a job that reconciles subscriptions with the processor's records and flags mismatches, **so that** nobody is charged for what they do not have.
- **Given** a mismatch, **when** found, **then** it is listed on the admin page with the learner id tokenized.
- Size: M · Priority: P1 · Week: Beta · Domain: 07 Security · Depends on: E12-S04

### E12-S09 · Regional prices
**As an** operator, **I want** country-level prices once there is data on where learners come from, **so that** the product is affordable where incomes are lower.
- **Given** a region list, **when** prices are set, **then** the price shown and charged match per country.
- Size: M · Priority: LATER · Week: After beta · Domain: 07 Security · Depends on: E12-S04
