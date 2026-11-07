# E13 · Privacy, security and compliance

*Architecture domain 07. The data is theirs. Counsel's answers (region, transfer basis, consent copy, crisis lines, California SB 243, refunds) are the blocking item B4 and must be loaded before the first paying learner on 23 December.*

### E13-S01 · Per-learner keys and audit log
**As a** learner, **I want** my audio and transcripts encrypted under a key that is mine, with every staff access logged, **so that** my data cannot be read in bulk.
- **Given** `forone.core.keys`, **when** a learner is created, **then** a data key is minted under KMS and the audit log records every decrypt purpose.
- **Given** the RLS CI test, **when** run, **then** no learner-keyed table is readable across learners by the app role.
- Size: L · Priority: P0 · Week: W1 · Domain: 07 Security · Depends on: E01-S05

### E13-S02 · Processor register and counsel requests sent
**As an** operator, **I want** `docs/ropa.md` listing every vendor with its DPA status and training opt-out, and the six decision requests sent to counsel in week 1, **so that** nothing is built on a vendor we cannot use.
- **Given** the register, **when** a vendor's row is `blocked`, **then** the adapters refuse it.
- **Given** 22 December, **when** checked, **then** every vendor in `vendors.yaml` has a DPA or clickwrap terms recorded and the training opt-out screenshotted.
- Size: S · Priority: P0 · Week: W1 · Domain: 07 Security · Depends on: none

### E13-S03 · Consent texts with versions and the A9 flow
**As a** learner, **I want** consent asked in one plain sentence, right after I heard myself, with the exact text version recorded, and switches in controls, **so that** my consent is informed and reversible.
- **Given** a consent change, **when** saved, **then** `consent_change` carries `text_shown_version` and the Milestone 0 wording is never weakened.
- Size: M · Priority: P0 · Week: W3 · Domain: 07 Security · Depends on: E13-S02; counsel's copy (B4)

### E13-S04 · Age gate and pre-account sweep
**As an** operator, **I want** under-18s refused at A1 with a plain message and any pre-account data swept, **so that** the product is adults-only in fact.
- **Given** an under-18 flag, **when** any api call follows, **then** it returns `403 under_18` and the pre-account sweep deletes the data within the hour.
- Size: S · Priority: P0 · Week: W3 · Domain: 07 Security · Depends on: E06-S03

### E13-S05 · Voice storage off: delete within 15 minutes
**As a** learner, **I want** my call audio analysed and deleted within 15 minutes when I decline storage, and all audio gone within 24 hours when I revoke, **so that** the promise at consent is kept.
- **Given** storage off, **when** `audio/expire` runs on `media.object_created`, **then** the object is gone within 15 minutes of call end and `privacy/verify` confirms it.
- Size: M · Priority: P0 · Week: W4 · Domain: 07 Security · Depends on: E05-S03, E13-S01

### E13-S06 · Export and account deletion on the clock
**As a** learner, **I want** an export link within an hour and deletion that ends access at once, purges live data in 24 hours and backups in 30 days, **so that** the data is mine to take or destroy.
- **Given** a deletion, **when** requested, **then** access ends immediately, the purge order runs, processor deletions (Langfuse, vendors with retention) are called, and `privacy/verify` passes at 24 hours.
- Size: L · Priority: P0 · Week: W5 · Domain: 07 Security, 04 Learner model · Depends on: E03-S11, E13-S01

### E13-S07 · Research opt-in, anonymize and revoke
**As a** learner, **I want** my anonymized transcripts used to improve the teacher only if I opt in, off by default, never audio, with revoke honoured, **so that** data use is my choice.
- **Given** opt-in, **when** `research/anonymize` runs, **then** names from `life_facts.people` are replaced and the output is audited; **given** revoke, **then** the learner's rows are removed from the research set.
- Size: M · Priority: P0 (switch), P1 (model-assisted names) · Week: W5 · Domain: 07 Security · Depends on: E13-S03

### E13-S08 · Crisis protocol
**As a** learner, **I want** the host or Salma to step out of character and give real help if I say something that suggests I am in danger, **so that** the product is safe.
- **Given** a keyword-list hit, **when** detected in a call or chat, **then** the crisis path activates, the audio is quarantined, the resources card shows once on Today, and the keyword list's false-positive rate on about 200 pilot calls is recorded.
- Size: M · Priority: P0 · Week: W4 · Domain: 07 Security · Depends on: E05-S11; counsel's crisis lines (B4)

### E13-S09 · Output guard and the listener-text sanitizer
**As an** operator, **I want** every prompt that includes learner text to carry the operator rule, a sanitizer on listener text and names, and an output guard that enforces AI disclosure and told-not-inferred, **so that** an injection in a call cannot steer the host.
- **Given** the 10 injection transcripts, **when** replayed, **then** zero disclosures of the brief and zero rule changes; the 30-case set runs in the offline suite (P1).
- Size: M · Priority: P0 · Week: W2 to W4 · Domain: 07 Security · Depends on: E05-S02, E04-S02

### E13-S10 · Staff accounts, roles and the review access rules
**As an** operator, **I want** staff sign-in with owner, engineer and reviewer roles, and reviewers seeing episodes with names tokenized, **so that** reading episodes for quality does not expose who the learner is.
- **Given** a reviewer, **when** opening an episode, **then** learner names are tokens and the access is audited.
- Size: M · Priority: P0 · Week: W3 · Domain: 07 Security · Depends on: E13-S01

### E13-S11 · Privacy verify and the admin privacy page
**As an** operator, **I want** a job that checks every privacy promise (deletion windows, export times, consent versions, audio expiry) and a page that shows it, **so that** a missed promise pages before a learner notices.
- **Given** a missed window, **when** `privacy/verify` runs, **then** `privacy_promise_missed` pages.
- Size: M · Priority: P0 · Week: W5 · Domain: 07 Security · Depends on: E13-S05, E13-S06

### E13-S12 · Incident runbook and tabletop
**As an** operator, **I want** a security incident runbook and a 60-minute tabletop run once before the beta, **so that** the first incident is not the first rehearsal.
- **Given** the tabletop, **when** done, **then** the runbook lists the steps, the contacts, the learner-notice template and the processor list, and the gaps found are fixed or ticketed.
- Size: S · Priority: P0 · Week: W5 · Domain: 07 Security, 09 Operations · Depends on: E15-S06
