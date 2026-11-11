# Record of processing activities

> **Draft for counsel. Not legal advice.** The GDPR Art. 30(1) record for For one, drafted 2026-11-12 from 07 §4.4, §4.9, §4.12 to §4.14, 04 §4.1.5, §4.12 and §4.14, 01's `model_io` and `retention/daily`, and ADR-24.17. **Counsel must confirm:** the lawful basis column (pack A-5), the transfer safeguards (A-2), and every retention period marked "not set" (B-5). Keep this file and the machine-readable processor register that CI reads (07 §4.9, handbook 09 §9) identical; when one changes, the other changes in the same pull request.

This file is the source record; the code repository's `docs/` links to it (per ADR-24.B11).

## 1. Controller

| | |
|---|---|
| Controller | `[Company legal name]`, `[Address]`, `[Company number]` |
| Contact | `[privacy email]` |
| Representatives | EU: `[name, address, if required]`. UK: `[name, address, if required]`. Saudi Arabia: `[if required]` |
| DPO | `[If required, pack A-4]` |
| Home region | AWS `eu-central-1` (Frankfurt), final for the beta (ADR-24.8) |

## 2. Processing activities

Data subjects are learners unless the row says otherwise. "People mentioned" means people the learner talks about, stored only as a first name or role the learner used (FR-505). Security measures are summarized in §5; the letters in the last column point there.

| # | Activity and purpose | Data categories | Lawful basis (working) | Recipients | Transfers | Retention | Security |
|---|---|---|---|---|---|---|---|
| 1 | **Onboarding and account**: the first session (Salma's intake, the pilot episode, the first call), account, age check, country, plan | Identity (name used by hosts, email or Apple/Google id, birth date, residence country, native and target language, time zone), intake answers, name clip | Contract; steps before a contract for the pre-account minutes | AWS, Anthropic, recognizers, voice vendor, LiveKit, Apple, Google, Resend | US (vendors) | Life of account; pre-account learners deleted after 24 h if no account; under-18 refusals deleted at once | a, b, c, f |
| 2 | **Episode production**: planning, writing, fitting, editing, voicing the learner's episodes, articles and chat | Usable life facts and quotes, interests, goals, learner-model briefs, first name in scripts | Contract | AWS, Anthropic, Google (editor, embeddings of scripts only), voice vendors, Inngest (ids) | US | Episodes and scripts: life of account. Prompts and completions (`model_io`): 90 days | a, b, d |
| 3 | **Live calls and voice processing**: streaming recognition, host replies, verbatim re-transcription, pronunciation scoring | Learner voice (in transit and briefly at rest), transcripts, word timings, pause profile, internal pronunciation scores | Contract | LiveKit, streaming and verbatim recognizers, pronunciation scorer, Anthropic, voice vendor, AWS | US (call-worker may run in the US) | Voice with storage off: within 15 min of the call ending (S3 lifecycle backstop 1 day). Transcripts: life of account | a, b, e |
| 4 | **Keeping recordings** (opt-in) | Full call recordings, voice notes, then-and-now recordings, "say it once", shadowing, name clip | Consent | AWS | None at rest | Until the learner deletes them or the account; within 24 h of revoking; noncurrent versions 7 days | a, b, e |
| 5 | **Learner model and life facts**: the nine stores, the notebook, follow-ups | Word bank, structures, errors, skills, interests, life facts with quotes, goals, taste, show canon; people mentioned | Contract | AWS; Anthropic (memory keeper, analyst) | US | Life of account; facts expire by shelf life but stay in history | a, b |
| 6 | **Sensitive facts** (health, money, relationships, religion, politics, sexuality) | Special-category and other sensitive content the learner volunteered | Explicit consent by one-tap card (ADR-24.10) | AWS; Anthropic (chat host and Salma, same session only) | US | Unconfirmed: never stored as a fact (stays in the transcript). Confirmed: life of account or until deleted | a, b |
| 7 | **Delivery**: drop notifications, the private podcast feed, the three email kinds | Push subscription, feed token, email address, first name in episode audio | Contract; gap note by consent | AWS, Resend, Vercel, the learner's browser push service and podcast app | US | Life of account; feed token until reset | a, g |
| 8 | **Progress evidence**: claims, weekly proof, finale, "where do I stand" | Claims and evidence, the learner's own clips if kept | Contract | AWS, Anthropic, voice vendor | US | Life of account; failed claims 90 days | a |
| 9 | **Crisis protocol**: detection, fixed response, resources card, log, yearly count | No content: date, residence country, resource shown, whether the call ended, `host_confirmed`, `learner_declined` (ADR-24.B15, B20); no reviewer field; the triggering turn stays in the event log, quarantined | `[Counsel, pack B-4]` | AWS; ops page with ids only; founder sees weekly counts only (ADR-24.15) | None at rest | Life of account; on deletion de-identified (learner id dropped) and kept 3 years for annual reporting, then deleted (ADR-24.B15) | a, b, h |
| 10 | **Billing** through Paddle (merchant of record, separate controller) | Plan, subscription state, customer and subscription refs, amounts, tax amounts, invoice link | Contract; legal obligation (Paddle, tax) | Paddle | Paddle's regions | Until account deletion (cost aggregates de-identified first); raw webhook bodies only when debugging is on, 30 days | a, i |
| 11 | **Security, audit and abuse prevention**: sign-in, rate limits, trial limit, WAF, audit log, pgaudit | Hashed IPs and identities, OTP codes, staff and service access records, normalized identity HMAC | Legitimate interests | AWS, Vercel | None at rest | Audit log 24 months, learner id nulled 12 months after deletion; pgaudit logs 400 days; rate-limit rows 2 days; trial ledger 180 days; deletion ledger (email HMAC) **retention not set** | a, c |
| 12 | **Quality review**: a paid native reader reads 10 random episodes per learner per month | Scripts and articles with names tokenized | Contract (quality of the service); `[counsel]` | The reviewer (staff, under agreement) | Reviewer's country `[may be outside the EU]` | Review findings: life of account, de-identified on deletion | c, f |
| 13 | **Improving the teacher** (opt-in; writes nothing until P1) and calibration tagging | Pseudonymized, de-identified transcripts (people's names, places and employers replaced, ADR-24.B9); calibration samples with audio only if both consents hold | Consent | Taggers (staff, under agreement); Langfuse (de-identified text) | Tagger's country | Until revoked (24 h) or account deletion | c, f |
| 14 | **Observability**: tracing, error tracking, cost per learner | Ids, versions, timings, costs, research pseudonym; scrubbed errors | Legitimate interests | Langfuse (EU), Sentry (EU), Better Stack, Slack (ids only) | None by default | Langfuse 30 days; Sentry 90 days; Inngest run history 30 days; spool files 2 days | d |
| 15 | **Rights requests**: see, export, correct, delete | Everything above | Legal obligation | AWS, Resend | | Export ready within 72 h in the beta (1 h once automated), zip kept 7 days; deletion: no grace, live purge 24 h, backups 30 days (ADR-24.B1, B7) | a, e |
| 16 | **Waitlist and sample episodes** | Name, WhatsApp number or email, native language, reason, self-rating, country; sample answers and audio | Consent (waitlist); legitimate interests (sample limits) | AWS, Anthropic, voice vendor, Resend | US | Waitlist rows not invited: 12 months; samples 30 days | a, c |
| 17 | **Staff administration** (data subjects: staff, reviewers, taggers) | Email, role, languages, agreement date, sessions | Contract | AWS | | While active; `[then: not set]` | c |
| 18 | **Milestone 0 data** (data subjects: 15 pilot learners): vendor tests, the bridge (hand-made episodes for pre-payers until 2027-03-17), de-identified fixtures, the end-to-end run | Clips, scripts, tags, facts, recordings, de-identified (`m0-Lnn`) | Consent (pilot consent; the addendum) | Candidate recognizers and pronunciation vendors; AWS (`forone-fixtures`, private) | US | Pilot data by 2026-12-31 unless kept; fixtures per the addendum | c, f |

## 3. Recipients: processors and other controllers (ADR-24.17)

| Recipient | Role | Data | Audio | Region | Transfer safeguard (working) | Retention at the vendor | Training | DPA |
|---|---|---|---|---|---|---|---|---|
| Amazon Web Services | Hosting, storage, keys | Everything, encrypted | Yes, at rest encrypted | EU (Frankfurt) | AWS DPA | Ours to set | n/a | AWS standard |
| Anthropic | Teacher, writer, fitter, hosts, Salma text, chat host, analyst, memory keeper, proof producer, rater, editor fallback | Briefs with usable facts and quotes, transcripts, scripts | No | US | SCCs + TIA, or DPF if certified (ADR-24.B13; counsel confirms, pack A-2) | Commercial terms; **zero retention requested** (A7) | Not used for training (API default) | Sign |
| Google (Gemini API, paid) | Editor, embeddings (scripts only), TTS candidate | Scripts and checked facts | No | US | `[as above]` | Abuse-logging retention to confirm | Paid tier, not used | Google Cloud terms |
| `[Episode and call voice vendor and runner-up]` (ElevenLabs or Inworld) | Episode, call and Salma voices; alignment | Script text, host lines, first name | Produced audio only | `[US/EU]` | `[as above]` | Workspace retention off | Switched off | Sign |
| `[Streaming recognizer]` (Soniox; Deepgram secondary) | Live speech-to-text, talkback | Live learner speech | Yes, in transit | `[US/EU]` | `[as above]` | "No retention" confirmed in writing | Off | Sign |
| `[Verbatim recognizer]` (AssemblyAI or ElevenLabs Scribe) | Verbatim transcript after the call | Every learner turn, voice notes, recordings | Yes, held for the job | `[US/EU]` | `[as above]` | Minimum; negotiate hardest | Off | Sign |
| `[Pronunciation scorer]` (Speechace or Microsoft) | Pronunciation on known sentences | 15 to 20 s clips | Yes, in transit | `[US/EU]` | `[as above]` | To confirm | To confirm | Sign |
| LiveKit Cloud | Media relay | Call media, room metadata | Yes, in transit | Nearest edge | `[as above]` | No recording (Egress disabled) | n/a | Sign |
| Inngest Cloud (EU) | Workflow state | Ids, dates, enums | No | EU | n/a | Run history 30 days | n/a | Sign |
| Langfuse Cloud (EU) | Tracing | Metadata and pseudonym; pseudonymized, de-identified text only for opted-in learners | No | EU | n/a | 30 days | n/a | Sign |
| Resend | Email | Email address, message | No | `[US/EU]` | `[as above]` | Minimum log retention; tracking off | n/a | Sign |
| Sentry (EU) | Errors | Scrubbed traces, no learner ids | No | EU | n/a | 90 days | n/a | Sign |
| Vercel | Web hosting | Request logs with IPs (public pages, app shell) | No | Edge; logs US | `[as above]` | Short; configure | n/a | Standard |
| Better Stack | Uptime and paging | Ids only | No | `[region]` | `[as above]` | `[to confirm]` | n/a | Standard |
| **Paddle** (separate controller, merchant of record) | Checkout, payment, tax, invoices | Name, email, country, payment details | No | `[Paddle]` | Paddle's own | Paddle's own (tax law) | n/a | Seller agreement |
| Apple, Google (separate controllers) | Sign-in | Sign-in identity, relay email | No | US | Their own | Their own | n/a | Developer terms |
| The learner's podcast app (chosen by the learner) | Fetches the private feed | Episode audio and titles (first name, personal topics) | Produced audio | Varies | n/a (learner's choice) | Theirs | Theirs | None; disclosed |

Milestone 0 services (Google Drive, Google Forms, WhatsApp, ElevenLabs Agents, claude.ai Projects) do not carry into the beta (07 §4.9).

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
| Research set (P1) | Until revoke (24 h) or deletion | `research/revoke`, `learner/delete` | 04 D18 |
| Exports | Ready within 72 h in the beta (1 h once automated); zip kept 7 days after ready | `retention/daily` | ADR-24.B7, 04 D16, FR-1046 |
| Trial ended unpaid | 90 days, warning at day 83 | `retention/daily` | FR-1048, 04 §4.12.3 |
| Failed payment | 7-day grace with the processor's retries inside it, then as trial ended | Subscription state | ADR-24.B2, FR-1232 |
| Pre-account learners | 24 h | `pre_account_sweep` | 07 D8 |
| Account deletion | No grace: access ends at once, live purge within 24 h, backups expire within 30 days | `learner/delete`; RDS backup retention 30 days | ADR-24.B1, FR-1047 |
| Audit log | 24 months; learner id nulled 12 months after deletion | `retention/daily` | 07 §4.12 |
| pgaudit logs (human SQL) | 400 days | CloudWatch | 07 §4.2 |
| Rate-limit rows | 2 days | `retention/daily` | 07 §4.11 |
| Trial ledger | 180 days per identity | Ledger rule | 07 §4.11 |
| Deletion ledger (email HMAC, counts) | **Not set** (needed for the 30-day re-signup audit) | | 04 D17 |
| Crisis log (no content) | Life of account; on deletion de-identified and kept 3 years, then deleted | `learner/delete`, `retention/daily` | ADR-24.B15 |
| Raw payment webhook bodies (debug only, off by default) | 30 days | `retention/daily` | 07 §4.14 |
| Spool files | 2 days | S3 rule | 07 §4.4 |
| Sample episodes | 30 days | `retention/daily` | 07 §4.4 |
| Waitlist, not invited | 12 months | `[job not yet named]` | 07 §10 #11, ADR-24.23 |
| Staff accounts and agreements | **Not set** after an account ends | | 07 §4.13 |
| Milestone 0 data | By 2026-12-31 unless kept, or unless the learner signed Part 2 by 2026-12-15 (bridge until 2027-03-17; import; fixtures until `[2027-12-31]`) (ADR-24.B28) | Manual (Muath) | milestone-0/02 |

## 5. Security measures (Art. 32), by letter

- **a. Encryption and isolation.** TLS 1.2+ everywhere; RDS and S3 encrypted with KMS; learner voice SSE-C under a per-learner key, show audio SSE-KMS served by 10-minute presigned URLs; row-level security on every learner table with a CI check (07 §4.1, §4.2).
- **b. Key and access control.** Per-learner key unwrapped only by three service roles with a logged purpose; 60-second cache, never for export or break-glass; key destroyed last on deletion (07 D2, ADR-18).
- **c. People.** Named staff accounts with roles and an IP allowlist; break-glass with MFA and a reason; every content read logged and shown to the learner; reviewers and taggers sign [08](08-reviewer-confidentiality.md) first (07 §4.13).
- **d. Minimum data to vendors.** Compiled briefs, metadata-only tracing, ids-only workflow events, logging redaction of vendor error bodies (07 §4.9, §4.12; ADR-09).
- **e. Verified deletion.** Every window has a doer that writes evidence and an independent hourly checker (07 D5).
- **f. Pseudonymization.** Names tokenized for reviewers; research pseudonym as a stored random value deleted with the learner (07 D6).
- **g. Feed protection.** Unguessable tokens, excluded from directories, resettable, many-IP warning (06; 07 §4.11).
- **h. Crisis quarantine.** The triggering turn never becomes a fact, callback, claim or proof (07 §4.8).
- **i. Payments.** Hosted checkout only (SAQ-A); signed webhooks with replay protection; no raw bodies kept (07 §4.14).
- **Incidents.** Four severities, a runbook rehearsed in the last build week, a 72-hour regulator clock per affected regime (07 §4.15).
