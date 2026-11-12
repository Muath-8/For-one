# Record of processing activities

> **Self-reviewed against legal/00; not reviewed by a lawyer; see the triggers** ([00-self-review-checklist.md](00-self-review-checklist.md) §25). The GDPR Art. 30(1) record for For one, kept by Muath from the ICO and CNIL record templates (legal/00 §17), from 07 §4.4, §4.9, §4.12 to §4.14, 04 §4.1.5, §4.12 and §4.14, 01's `model_io` and `retention/daily`, ADR-24.17 and ADR-25. Keep this file and the machine-readable processor register that CI reads (07 §4.9, handbook 09 §9) identical; when one changes, the other changes in the same pull request.

This file is the source record; the code repository's `docs/` links to it (ADR-24.B11).

## 1. Controller

| | |
|---|---|
| Controller | `[Company legal name]`, `[Address]`, `[Company number]` |
| Contact | `[privacy email]`; Muath is the privacy contact |
| Representatives | EU and UK: `[name, address]`, appointed if the company is outside the EU and UK (GDPR Art. 27; register A7). Saudi Arabia: `[if SDAIA's rules require it, legal/00 §6]` |
| DPO | None at launch; reassessed at 1,000 learners (legal/00 §5) |
| Home region | AWS `eu-central-1` (Frankfurt) (ADR-24.8) |

## 2. Processing activities

Data subjects are learners unless the row says otherwise. "People mentioned" means people the learner talks about, stored only as a first name or role the learner used (FR-505). Security measures are summarized in §5; the letters in the last column point there. The lawful bases are those fixed in legal/00 §7.

| # | Activity and purpose | Data categories | Lawful basis | Recipients | Transfers | Retention | Security |
|---|---|---|---|---|---|---|---|
| 1 | **Onboarding and account**: the first session (Salma's intake, the first episode, the first call), account by email one-time code, age check, country, plan | Identity (name used by hosts, email, birth date, residence country, native and target language, time zone), intake answers, name clip | Contract; steps before a contract for the pre-account minutes; explicit consent for special-category content (`special_category`) | AWS, Anthropic, recognizers, voice vendor, LiveKit, Resend | US (vendors) | Life of account; pre-account learners deleted after 24 h if no account; under-18 refusals deleted at once | a, b, c, f |
| 2 | **Episode production**: planning, writing, fitting, editing, voicing the learner's episodes, articles and chat | Usable life facts and quotes, interests, goals, learner-model briefs, first name in scripts | Contract | AWS, Anthropic, Google (editor, embeddings of scripts only), voice vendors, Inngest (ids) | US | Episodes and scripts: life of account. Prompts and completions (`model_io`): 90 days | a, b, d |
| 3 | **Live calls and voice processing**: streaming recognition, host replies, verbatim re-transcription, pronunciation scoring | Learner voice (in transit and briefly at rest), transcripts, word timings, pause profile, internal pronunciation scores; no voiceprints | Contract | LiveKit, streaming and verbatim recognizers, pronunciation scorer, Anthropic, voice vendor, AWS | US (call-worker may run in the US) | Voice with storage off: within 15 min of the call ending (S3 lifecycle backstop 1 day). Transcripts: life of account | a, b, e |
| 4 | **Keeping recordings** (opt-in) | Full call recordings, voice notes, then-and-now recordings, "say it once", shadowing, name clip | Consent | AWS | None at rest | Until the learner deletes them or the account; within 24 h of revoking; noncurrent versions 7 days | a, b, e |
| 5 | **Learner model and life facts**: the nine stores, the notebook, follow-ups | Word bank, structures, errors, skills, interests, life facts with quotes, goals, taste, show canon; people mentioned | Contract | AWS; Anthropic (memory keeper, analyst) | US | Life of account; facts expire by shelf life but stay in history | a, b |
| 6 | **Sensitive facts** (health, money, relationships, religion, politics, sexuality) | Special-category and other sensitive content the learner volunteered | Explicit consent by one-tap card (ADR-24.10) | AWS; Anthropic (chat host and Salma, same session only) | US | Unconfirmed: never stored as a fact (stays in the transcript). Confirmed: life of account or until deleted | a, b |
| 7 | **Delivery**: drop notifications, the private podcast feed, the three email kinds | Push subscription, feed token, email address, first name in episode audio | Contract; gap note by consent | AWS, Resend, Vercel, the learner's browser push service and podcast app | US | Life of account; feed token until reset | a, g |
| 8 | **Progress evidence**: claims, weekly proof, finale, "where do I stand" | Claims and evidence, the learner's own clips if kept | Contract | AWS, Anthropic, voice vendor | US | Life of account; failed claims 90 days | a |
| 9 | **Crisis protocol**: detection, fixed response, resources card, log, yearly count | No content: date, residence country, resource shown, whether the call ended, `host_confirmed`, `learner_declined` (ADR-24.B15, B20); the triggering turn stays in the event log, quarantined | Explicit consent at account creation; vital interests when the learner cannot act | AWS; the helpline directory (link only, nothing sent); Muath sees weekly counts only (ADR-24.15) | None at rest | Life of account; on deletion de-identified (learner id dropped) and kept 3 years for annual reporting, then deleted | a, b, h |
| 10 | **Billing** through Paddle (merchant of record, separate controller) | Plan, subscription state, customer and subscription refs, amounts, tax amounts, invoice link | Contract; legal obligation (Paddle, tax) | Paddle | Paddle's regions | Until account deletion (cost aggregates de-identified first); raw webhook bodies only when debugging is on, 30 days | a, i |
| 11 | **Security, audit and abuse prevention**: sign-in, rate limits, trial limit, WAF, audit log, pgaudit | Hashed IPs and identities, OTP codes, owner and service access records, normalized identity HMAC | Legitimate interests | AWS, Vercel | None at rest | Audit log 24 months, learner id nulled 12 months after deletion; pgaudit logs 400 days; rate-limit rows 2 days; trial ledger 180 days; deletion ledger email HMAC 60 days after deletion | a, c |
| 12 | **Quality review**: an AI review pass reads sampled episodes against the laws and ban lists; Muath reads some (ADR-25.7) | Scripts and articles with names tokenized | Contract (quality of the service) | Anthropic (the review model); Muath | US | Review findings: life of account, de-identified on deletion | c, f |
| 13 | **Improving the teacher** (opt-in) and, after launch, the calibration set | Pseudonymized, de-identified transcripts (people's names, places and employers replaced, ADR-24.B9); calibration samples with audio only if both consents hold | Consent | Muath; Anthropic (automated checks); Langfuse (de-identified text) | US | Until revoked (24 h) or account deletion | c, f |
| 14 | **Observability**: tracing, error tracking, cost per learner | Ids, versions, timings, costs, research pseudonym; scrubbed errors | Legitimate interests | Langfuse (EU), Sentry (EU), Better Stack, Slack (ids only) | None by default | Langfuse 30 days; Sentry 90 days; Inngest run history 30 days; spool files 2 days | d |
| 15 | **Rights requests**: see, export, correct, delete | Everything above | Legal obligation | AWS, Resend | | Export ready within 72 h (1 h once automated), zip kept 7 days; deletion: no grace, live purge 24 h, backups 30 days (ADR-24.B1, B7) | a, e |
| 16 | **Sample episodes** before signup | First name or nickname, the visitor's answers, sample audio | Legitimate interests (sample limits); steps at the visitor's request | AWS, Anthropic, voice vendor | US | 30 days | a, c |
| 17 | **Vendor tests with volunteer clips** (data subjects: about 30 volunteers; ADR-25.6) | Clips of the volunteer reading and speaking; name, native language, consent date | Consent (`volunteer.recording`) | Candidate recognizers and voice vendors; AWS (private bucket) | US | Until the tests no longer need them, at most 12 months, or on request | c |

## 3. Recipients: processors and other controllers (ADR-24.17)

All processors are used under their standard, self-serve DPA (legal/00 §3). The transfer safeguard for every US processor is the SCCs in that DPA with a transfer impact assessment, or the EU-US DPF where the vendor is certified (ADR-24.B13).

| Recipient | Role | Data | Audio | Region | Transfer safeguard | Retention at the vendor | Training | DPA |
|---|---|---|---|---|---|---|---|---|
| Amazon Web Services | Hosting, storage, keys | Everything, encrypted | Yes, at rest encrypted | EU (Frankfurt) | n/a (EU) | Ours to set | n/a | AWS standard |
| Anthropic | Teacher, writer, fitter, hosts, Salma text, chat host, analyst, memory keeper, proof producer, rater, editor fallback, review pass | Briefs with usable facts and quotes, transcripts, scripts | No | US | SCCs + TIA, or DPF | Commercial terms; **zero retention requested** (A1) | Not used for training (API default) | Standard |
| Google (Gemini API, paid) | Editor, embeddings (scripts only), TTS candidate | Scripts and checked facts | No | US | SCCs + TIA, or DPF | Abuse-logging retention as stated in its terms | Paid tier, not used | Google Cloud terms |
| `[Episode and call voice vendor and runner-up]` | Episode, call and Salma voices; alignment | Script text, host lines, first name | Produced audio only | `[US/EU]` | SCCs + TIA, or DPF | Workspace retention off | Switched off | Standard |
| `[Streaming recognizer]` | Live speech-to-text, talkback | Live learner speech | Yes, in transit | `[US/EU]` | SCCs + TIA, or DPF | No retention setting on | Off | Standard |
| `[Verbatim recognizer]` | Verbatim transcript after the call | Every learner turn, voice notes, recordings | Yes, held for the job | `[US/EU]` | SCCs + TIA, or DPF | Delete after transcription | Off | Standard |
| `[Pronunciation scorer]` | Pronunciation on known sentences | 15 to 20 s clips | Yes, in transit | `[US/EU]` | SCCs + TIA, or DPF | Minimum offered | Off where offered | Standard |
| LiveKit Cloud | Media relay | Call media, room metadata | Yes, in transit | Nearest edge | SCCs + TIA, or DPF | No recording (Egress disabled) | n/a | Standard |
| Inngest Cloud (EU) | Workflow state | Ids, dates, enums | No | EU | n/a | Run history 30 days | n/a | Standard |
| Langfuse Cloud (EU) | Tracing | Metadata and pseudonym; de-identified text only for opted-in learners | No | EU | n/a | 30 days | n/a | Standard |
| Resend | Email, including sign-in codes | Email address, message | No | `[US/EU]` | SCCs + TIA, or DPF | Minimum log retention; tracking off | n/a | Standard |
| Sentry (EU) | Errors | Scrubbed traces, no learner ids | No | EU | n/a | 90 days | n/a | Standard |
| Vercel | Web hosting | Request logs with IPs (public pages, app shell) | No | Edge; logs US | SCCs + TIA, or DPF | Short; configured | n/a | Standard |
| Better Stack | Uptime and alerts to Muath | Ids only | No | `[region]` | SCCs + TIA, or DPF | As configured | n/a | Standard |
| **Paddle** (separate controller, merchant of record) | Checkout, payment, tax, invoices, refunds | Name, email, country, payment details | No | Paddle's | Paddle's own | Paddle's own (tax law) | n/a | Seller agreement |
| The learner's podcast app (chosen by the learner) | Fetches the private feed | Episode audio and titles (first name, personal topics) | Produced audio | Varies | n/a (learner's choice) | Theirs | Theirs | None; disclosed |

## 4. Retention schedule (one table)

| Data | Period | Enforced by | Source |
|---|---|---|---|
| Learner voice, storage off | 15 min after call end; lifecycle backstop 1 day | `audio/expire`, `call/verbatim-turn`, S3 rule; checked hourly by `privacy/verify` | FR-343, 07 §4.4 |
| Learner voice after revoke or "delete all" | 24 h | `learner/purge-audio` | FR-1042, 07 §4.4 |
| Kept recordings | Until the learner deletes or the account ends; noncurrent versions 7 days | Purge deletes all versions | FR-1040, 04 §4.11 |
| Transcripts, events, learner model, notebook | Life of account | `learner/delete` | FR-1043, 04 §4.1.5 |
| Prompts and completions (`model_io`) | 90 days | `retention/daily` drops partitions | 01 `retention/daily` |
| Langfuse traces | 30 days | Project setting, asserted weekly | ADR-09 |
| Inngest run history | 30 days | Configured | 07 §4.9 |
| Sentry events | 90 days | Configured | 07 §4.9 |
| Research set | Until revoke (24 h) or deletion | `research/revoke`, `learner/delete` | 04 D18 |
| Exports | Ready within 72 h (1 h once automated); zip kept 7 days after ready | `retention/daily` | ADR-24.B7, 04 D16, FR-1046 |
| Trial ended unpaid | 90 days, warning at day 83 | `retention/daily` | FR-1048, 04 §4.12.3 |
| Failed payment | 7-day grace with the processor's retries inside it, then as trial ended | Subscription state | ADR-24.B2, FR-1232 |
| Pre-account learners | 24 h | `pre_account_sweep` | 07 D8 |
| Account deletion | No grace: access ends at once, live purge within 24 h, backups expire within 30 days | `learner/delete`; RDS backup retention 30 days | ADR-24.B1, FR-1047 |
| Audit log | 24 months; learner id nulled 12 months after deletion | `retention/daily` | 07 §4.12 |
| pgaudit logs (human SQL) | 400 days | CloudWatch | 07 §4.2 |
| Rate-limit rows | 2 days | `retention/daily` | 07 §4.11 |
| Trial ledger | 180 days per identity | Ledger rule | 07 §4.11 |
| Deletion ledger | Email HMAC removed 60 days after deletion (30 days after the backups expire); counts kept | `retention/daily` | 04 D17; legal/00 §14 |
| Crisis log (no content) | Life of account; on deletion de-identified and kept 3 years, then deleted | `learner/delete`, `retention/daily` | ADR-24.B15 |
| Raw payment webhook bodies (debug only, off by default) | 30 days | `retention/daily` | 07 §4.14 |
| Spool files | 2 days | S3 rule | 07 §4.4 |
| Sample episodes | 30 days | `retention/daily` | 07 §4.4 |
| Volunteer clips | Until the tests no longer need them, at most 12 months, or on request | Manual (Muath) | ADR-25.6 |
| The owner's staff account | While active; deleted 12 months after it ends | Manual | 07 §4.13 |

## 5. Security measures (Art. 32), by letter

- **a. Encryption and isolation.** TLS 1.2+ everywhere; RDS and S3 encrypted with KMS; learner voice SSE-C under a per-learner key, show audio SSE-KMS served by 10-minute presigned URLs; row-level security on every learner table with a CI check (07 §4.1, §4.2).
- **b. Key and access control.** Per-learner key unwrapped only by three service roles with a logged purpose; 60-second cache, never for export or break-glass; key destroyed last on deletion (07 D2, ADR-18).
- **c. People.** Only the owner (Muath) can read content, through break-glass with MFA and a reason; every content read logged and shown to the learner. The AI coding agent has no production credentials and works only with synthetic learners (legal/00 §15; ADR-25.2).
- **d. Minimum data to vendors.** Compiled briefs, metadata-only tracing, ids-only workflow events, logging redaction of vendor error bodies (07 §4.9, §4.12; ADR-09).
- **e. Verified deletion.** Every window has a doer that writes evidence and an independent hourly checker (07 D5).
- **f. Pseudonymization.** Names tokenized for the review pass; research pseudonym as a stored random value deleted with the learner (07 D6).
- **g. Feed protection.** Unguessable tokens, excluded from directories, resettable, many-IP warning (06; 07 §4.11).
- **h. Crisis quarantine.** The triggering turn never becomes a fact, callback, claim or proof (07 §4.8).
- **i. Payments.** Hosted checkout only (SAQ-A); signed webhooks with replay protection; no raw bodies kept (07 §4.14).
- **Incidents.** Four severities, a runbook rehearsed before launch, alerts to Muath, a 72-hour regulator clock, and a lawyer engaged for any notifiable breach (07 §4.15; legal/00 §16, §25).
