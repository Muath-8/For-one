# E13 · Privacy, security and compliance

*Architecture domain 07. The data is theirs. There is no lawyer: compliance comes from conservative design and a written self-review (ADR-25.3). GDPR-grade rights for everyone, hosting in `eu-central-1`, vendors under their standard DPAs with SCCs, Paddle as merchant of record for payment law, 18+, no voiceprints, voice storage off by default with deletion in 15 minutes, data use opt-in, the sensitive-fact card, AI disclosed. Muath completes the self-review checklist and approves the texts in `legal/` before launch (register A4).*

### E13-S01 · Per-learner keys and audit log
**As a** learner, **I want** my audio and transcripts encrypted under a key that is mine, with every staff access logged, **so that** my data cannot be read in bulk.
- **Given** `forone.core.keys`, **when** a learner is created, **then** a data key is minted under KMS and the audit log records every decrypt purpose.
- **Given** the RLS CI test, **when** run, **then** no learner-keyed table is readable across learners by the app role.
- Size: L · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 07 Security · Depends on: E01-S05
- Requirements: FR-1050, NFR-301, NFR-302, NFR-303

### E13-S02 · Processor register, DPIA and the self-review checklist
**As an** operator, **I want** `legal/05-ropa.md` (linked from the code repository's `docs/`, ADR-24.B11) listing every vendor with its standard DPA, SCCs and training opt-out, the DPIA from the official template, and `legal/00-self-review-checklist.md` with a final position and its source for every question, **so that** nothing is built on a vendor we cannot use and every legal text has a written basis (ADR-25.3).
- **Given** the register, **when** a vendor's row is `blocked`, **then** the adapters refuse it.
- **Given** the launch checklist, **when** checked, **then** every vendor in `vendors.yaml` has its DPA accepted and the training opt-out recorded (register A1), and every legal text has passed an AI review pass against the self-review checklist and Muath's approval (A4).
- Size: S · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 07 Security · Depends on: none
- Requirements: FR-1051, NFR-307

### E13-S03 · Consent texts with versions and the A9 flow
**As a** learner, **I want** consent asked in one plain sentence, right after I heard myself, with the exact text version recorded, and switches in controls, **so that** my consent is informed and reversible.
- **Given** account creation, **when** the learner agrees to the processing of conversation content, **then** a `special_category` consent with its text version is stored, and without it no account exists (ADR-25.9); it never stands in for the one-tap card that keeps a sensitive fact.
- **Given** a consent change, **when** saved, **then** `consent_change` carries `text_shown_version` and the wording approved in the self-review is never weakened without a new version.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 07 Security · Depends on: E13-S02; the self-review and Muath's approval of the texts (A4)
- Requirements: FR-118, FR-1043, FR-1049, FR-1051

### E13-S04 · Age gate and pre-account sweep
**As an** operator, **I want** under-18s refused at A1 with a plain message and any pre-account data swept, **so that** the product is adults-only in fact.
- **Given** an under-18 flag, **when** any api call follows, **then** it returns `403 under_18` and the pre-account sweep deletes the data within the hour.
- Size: S · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 07 Security · Depends on: E06-S03
- Requirements: FR-001, FR-003

### E13-S05 · Voice storage off: delete within 15 minutes
**As a** learner, **I want** my call audio analysed and deleted within 15 minutes when I decline storage, and all audio gone within 24 hours when I revoke, **so that** the promise at consent is kept.
- **Given** storage off, **when** `audio/expire` runs on `media.object_created`, **then** the object is gone within 15 minutes of call end and `privacy/verify` confirms it.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 07 Security · Depends on: E05-S03, E13-S01
- Requirements: FR-343, FR-1040, FR-1041, FR-1042, NFR-304

### E13-S06 · Export and account deletion on the clock
**As a** learner, **I want** an export link within an hour and deletion that ends access at once, purges live data in 24 hours and backups in 30 days, done by jobs from launch with no grace period (ADR-24.B1), **so that** the data is mine to take or destroy.
- **Given** an export request, **when** the job runs, **then** the zip has no passphrase, the emailed link opens the notebook, the download is a presigned URL minted on click and valid 15 minutes, the file is kept 7 days, and the whole takes under 1 hour (ADR-24.B7).
- **Given** a deletion, **when** requested, **then** access ends immediately, the purge order runs, processor deletions (Langfuse, vendors with retention) are called, and `privacy/verify` passes at 24 hours.
- Size: L · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 07 Security, 04 Learner model · Depends on: E03-S11, E13-S01
- Requirements: FR-1022, FR-1046, FR-1047, NFR-304

### E13-S07 · Research opt-in, de-identify and revoke
**As a** learner, **I want** my pseudonymized and de-identified transcripts (ADR-24.B9) used to improve the teacher only if I opt in, off by default, never audio, with revoke honoured, **so that** data use is my choice.
- **Given** opt-in, **when** `research/anonymize` runs, **then** people's names, place names and employers are replaced (04 §4.12.4) and the output is audited; **given** revoke, **then** the learner's rows are removed from the research set.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 07 Security · Depends on: E13-S03
- Requirements: FR-1044, NFR-303

### E13-S08 · Crisis protocol
**As a** learner, **I want** the host or Salma to step out of character and give real help if I say something that suggests I am in danger, **so that** the product is safe.
- **Given** a keyword-list hit, **when** the host or Salma confirms within 2 s, or no confirmation arrives within 2 s (fail safe: a missed crisis costs more than a false alarm, ADR-24.B12), **then** the crisis path activates for every learner wherever they live (SB 243 duties for all, ADR-24.9), the audio is quarantined, the resources card for the learner's ISO country, taken from a maintained international helpline directory (ADR-25.3), shows once on Today, and the keyword list's false-positive rate on the synthetic and scripted calls is recorded.
- **Given** an activation, **when** logged for the SB 243 annual report, **then** `crisis_log` holds no content (date, residence country, resource shown, whether the call ended, `host_confirmed`, `learner_declined`); on account deletion its rows are de-identified and kept 3 years, then deleted (ADR-24.B15, 24.B20); Muath sees the weekly count only and nobody writes to the learner personally (ADR-24.15).
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 07 Security · Depends on: E05-S11; the crisis wording in `legal/` approved in the self-review (A4)
- Requirements: FR-570, FR-571, FR-572, FR-1104

### E13-S09 · Output guard and the listener-text sanitizer
**As an** operator, **I want** every prompt that includes learner text to carry the operator rule, a sanitizer on listener text and names, and an output guard that enforces AI disclosure and told-not-inferred, **so that** an injection in a call cannot steer the host.
- **Given** the 10 injection transcripts, **when** replayed, **then** zero disclosures of the brief and zero rule changes; the 30-case set runs in the offline suite (P1).
- **Given** any host, Salma or chat line, **when** the correction guard reads it, **then** a line that says or implies "wrong", "mistake" or "the correct way is", or sets the learner's sentence beside a corrected one, is blocked and regenerated (ADR-06); "my mistake" is on the allow-list only when the host or Salma says it about their own memory (ADR-24.B25).
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 07 Security · Depends on: E05-S02, E04-S02
- Requirements: FR-333, FR-522, FR-560, FR-561, FR-837

### E13-S10 · Staff accounts, roles and the review access rules
**As an** operator, **I want** staff sign-in with owner and reviewer roles (the coding agent has no access to production learner data), and reviewers seeing episodes with names tokenized, **so that** reading episodes for quality does not expose who the learner is.
- **Given** a reviewer, **when** opening an episode, **then** learner names are tokens and the access is audited.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 07 Security · Depends on: E13-S01
- Requirements: FR-436, FR-1050

### E13-S11 · Privacy verify and the admin privacy page
**As an** operator, **I want** a job that checks every privacy promise (deletion windows, export times, consent versions, audio expiry) and a page that shows it, **so that** a missed promise pages before a learner notices.
- **Given** a missed window, **when** `privacy/verify` runs, **then** `privacy_promise_missed` pages.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 07 Security · Depends on: E13-S05, E13-S06
- Requirements: FR-1046, FR-1047, NFR-304

### E13-S12 · Incident runbook and tabletop
**As an** operator, **I want** a security incident runbook and a 60-minute tabletop run once before launch, **so that** the first incident is not the first rehearsal.
- **Given** the tabletop, **when** done, **then** the runbook lists the steps, the contacts, the learner-notice template, the processor list, and when a lawyer becomes necessary (a notifiable breach, a regulator contact, ADR-25.3), and the gaps found are fixed or ticketed.
- **Given** staging before launch, **when** an OWASP ZAP baseline scan runs, **then** no high finding is open; a paid penetration test is not run at launch and becomes necessary at 1,000 paying learners, before any B2B contract, or after any security incident (ADR-25.11).
- Size: S · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 07 Security, 09 Operations · Depends on: E15-S06
- Requirements: enabling (no FR)

