# 09. Data handling

Part of the For one engineering handbook. Written 2026-11-06 against architecture 07 (D1 to D6, D13, D14, §4.3, §4.4, §4.6, §4.9, §4.12, §4.13), 04 D16 to D18, 01 D7 and D15, 09 §4.5.4 and §4.9, and PRD 1.3, 12.4 to 12.7; revised 2026-11-12 for ADR-25 (the coding agent and Muath are the only actors; no reviewers, no Milestone 0 data, no counsel). This page is the rulebook for the coding agent; the architecture holds the mechanisms.

## 1. What we hold, and how sensitive each class is

| Class | Examples | Where it lives | Who may see it |
|---|---|---|---|
| **Voice** (the most sensitive) | call turns, the mixed call recording when storage is on, say-it-once and voice-note clips, the name clip, the then-and-now recordings | S3 `forone-voice`, SSE-C under the learner's own data key | the learner; code; Muath only through break-glass with a reason |
| **Life facts and quotes** | the notebook, `life_facts`, the learner's own words quoted in briefs and proofs | Postgres, learner-scoped rows under RLS | the learner; code; Muath as `owner` with every read logged and shown in the learner's export |
| **Transcripts and chat** | streaming and verbatim transcripts, chat with the host, talkback | Postgres under RLS; text to Langfuse only with the data-use opt-in, names tokenized | the learner; code; `owner` logged |
| **Identity and contact** | display name, email, phone, birth date (stored as a date, never shown, exported with identity; architecture 07 §4.7, ADR-24.B8), sign-in identities, feed tokens | Postgres under RLS | `owner`; never in logs, traces, Inngest or Sentry |
| **Produced show content** | scripts, articles, episodes, hosts' lines, Salma's answers when asked | Postgres and S3 `forone-media`, SSE-KMS under the environment's service key (ADR-12, ADR-24.B8) | the learner; the AI review pass for sampled items with names tokenized; `owner` |
| **Behaviour and state** | events (plays, opens, choices), sessions, schedule, allowance, billing state | Postgres | the agent, as ids and enums; `owner` |
| **Operational facts** | `vendor_calls`, `pipeline_steps`, measures, alerts, audit log | Postgres | the agent; `owner` |

Classification lives in code: `forone.learner.pii` names every column and field by class, the log scrubber and the Sentry scrubber read it, the export job reads it, and a new column without a class fails a unit test.

## 2. The promises the code keeps (and the agent must not break)

From PRD 1.3 and 12.5, made verifiable in architecture 07 D5:

| Promise | Window | Job | Verified by |
|---|---|---|---|
| Audio deleted when voice storage is off | within 15 minutes of the call ending, for every learner-voice object (ADR-24.B8) | `audio/expire` on every ephemeral `media_objects` insert; `call/verbatim-turn` per-turn deletion | `privacy/verify` hourly, sampling S3 prefixes |
| All audio deleted on revocation | within 24 hours | `learner/purge-audio` | same |
| Export | a link emailed within 72 hours of the request until export is automated, then within 1 hour (PRD FR-1046); zip with no passphrase; the download is minted on click and valid 15 minutes; the file is kept 7 days (ADR-24.B7) | `learner/export` (everything, including the staff-access log) | same |
| Account deletion | live data within 24 hours; backups within 30 days; processors called (Langfuse deletion API, Resend, the voice vendors' history if any) | `learner/delete`, eight steps | same, plus `rds_assert(BackupRetentionPeriod == 30, manual_snapshots == 0)` |
| Unpaid trial data | deleted after 90 days with one warning email (`trial_deleting_soon`, ADR-24.B21) at day 83 | `retention/daily` | same |
| The one kept then-and-now recording | kept while the account exists, `kept_explicitly = true` | | the verify job ignores it by flag |
| Staff access visible to the learner | every content read by a human is an `audit_log` row included in the export | `forone.core.audit` | the RLS walk and a test that every admin content route writes a row |

The agent must not: take a manual RDS snapshot (it breaks the 30-day promise; the verify job fails on any manual snapshot), change the S3 versioning settings (versioning is on for `forone-voice` and `forone-media` with noncurrent versions expiring after 7 days on `learners/`, and never on `ephemeral/`, so a deletion bug cannot erase a kept recording and ephemeral voice still dies in 15 minutes; architecture 04, ADR-24.B8), add a cache or a queue that holds learner text outside Postgres, or add a learner-voice object kind without wiring it into the three deletion jobs and the verify job in the same PR.

## 3. What the agent may and may not look at

The role matrix from architecture 07 §4.13, as rules of conduct. There are two actors: the coding agent and Muath, the only staff account (`owner`).

**The agent may, without asking:** work with the synthetic learners and the eval fixtures freely; read every id, enum, timestamp, count, cost, version and status that an alert, a log line, a Sentry event, Langfuse trace metadata or an Inngest run carries, as Muath passes them to it or as `ops.yml` returns them; query `forone_readonly` for operational tables on staging.

**Only Muath may, with a reason row:** read a learner's prompt and completion text by span id (`/admin/trace/{span_id}`, which writes an `audit_log` row with the reason and appears in the learner's export); read a transcript for a specific call under investigation (same path); assume the break-glass IAM role to read an audio object or a secret (MFA, CloudTrail, a Slack note in `#forone-ops` before, the audit row written by the tool). The reason is a sentence a learner could read in their export without alarm: "investigating why your episode was late on 12 December". When the agent needs what such a read shows, Muath summarises it in words that contain no learner content. The weekly review lists the week's reason rows.

**The agent may not, ever:** read learner content of any kind (transcripts, chat, facts, quotes, the notebook, audio, names, emails); hold a prod credential; copy learner data into a prompt, a fixture, a cassette, a PR, an issue, a spreadsheet or a screenshot; run any query that joins learners together except the measures code; use a real learner as a test learner; send a message to a learner by any channel (there are three message kinds and none is manual).

**Muath as `owner`** can see everything, and every content read is logged and visible to the learner as "owner". The product's trust promise is that this is rare and reasoned.

**The AI review pass** that checks episode samples after launch (ADR-25.7) sees sampled scripts with names tokenized, never transcripts, chat, the notebook or identity, and runs only through the adapters under the register. There are no hired reviewers or taggers at launch.

Infrastructure access follows: AWS console for Muath only, with MFA; no access keys; CloudTrail on; ECS exec off in prod; the break-glass role alerting Slack on every assumption.

## 4. Where learner data may and may not go

| Destination | Allowed | Rule |
|---|---|---|
| Postgres (home region) | all classes | under RLS, learner-scoped |
| S3 (home region) | audio, produced media, exports | learner voice SSE-C with the learner's DEK; show audio SSE-KMS (ADR-12); exports downloaded through a presigned URL minted on click, valid 15 minutes, the file kept 7 days (ADR-24.B7) |
| Inngest Cloud (EU) | ids, dates, enums, short strings | no `text`, `quote`, `transcript`, `audio` field on any event model; CI test |
| Langfuse Cloud (EU) | metadata for everyone; prompt and completion text only for `data_use = true`, names tokenized; never audio | 30-day retention; deletion called by `learner/delete` |
| Sentry (EU) | scrubbed context, ids; browser errors | `beforeSend` scrub plus server-side scrub |
| CloudWatch | the log schema in handbook 06 | scrubber at the logger; PII corpus test |
| Better Stack, Slack | ids only | the poster uses the scrubber |
| Model, voice and recognition vendors | what the role needs, in transit, under the register's retention terms | only through `forone.adapters`; only vendors in `legal/05-ropa.md` with a DPA; the register row names what each sees |
| Resend | email address and the message body of one of the three kinds | no tracking; minimum log retention |
| The agent's working session, a local machine | nothing from prod, ever | synthetic learners and the eval fixtures only |
| Staging | synthetic learners and the consented volunteer clips | never a copy of prod |
| A third-party analytics tool | nothing | there is none, and none is added without Muath and a new self-review (ADR-25.3) |

Embeddings are computed on model-written scripts only, never on learner turns, so the embeddings vendor sees no learner text.

## 5. Consent

Six consent kinds (architecture 07 D4), each a versioned text in the native package (`packages/native/<lang>/`, ADR-02), each change a `consent_change` event carrying the version shown, mirrored into `consents`. Nothing is inferred from behaviour. Code reads consent before every act that needs it: `POST /v1/calls` (voice storage), `audio/expire`, the tracing middleware (data use), the research anonymizer, the proof producer (the kept recording).

The agent: never adds a consent flag without a text version; never defaults a consent to true; never changes a consent text, which is built from `legal/03-consent-texts.md`, checked against the self-review checklist and approved by Muath (ADR-25.3); and treats a learner's "no" as a data fact the verify job will check.

## 6. Development data and fixtures

- **Synthetic learners** are the default for everything: dev seeds, staging, cassettes, the e2e run, the canary, load tests. They are generated by `tools/eval synth` (the Milestone 0 kit's learner-file layout is the template) with invented names, invented facts and planted errors.
- **Recognizer clips** (ADR-25.6): utterances from the open speechocean762 corpus (Apache-2.0, cited in the fixture's README) and about 30 clips recorded by volunteers, each with a one-line consent naming the use (testing speech recognizers, sent to the recognizer vendors under test). The volunteer clips and their consents live in the `forone-fixtures` bucket, fetched by `make fixtures`; they are deleted if a volunteer asks. No real learner's data is ever a fixture.
- **Cassettes** are recorded only with synthetic learners. A cassette whose prompt contains a real person's text is deleted on sight.
- **Production data in a bug report:** ids, timestamps, the trace id and the span id. Never the text. If the text is truly needed, Muath reads it through the audited path and gives the agent what matters in words that contain no learner content.

## 7. Research use of transcripts

PRD 12.5.5: pseudonymized and de-identified transcripts (never "anonymized", which overclaims; ADR-24.B9) may be used "for checking and improving the teacher" only with the learner's opt-in. The anonymizer (architecture 07 D6) runs inside the after-pass: the research pseudonym (a random value stored in `research_pseudonyms`, deleted with the learner; no HMAC and no secret, architecture 10 §4 and ADR-09), people's names, place names, employers, emails, phones, URLs and digit runs replaced by typed tokens (architecture 04 §4.12.4, ADR-24.B9), rows removed on revoke or deletion. The research set is read only on `/admin/research` by Muath, one row at a time, never bulk-exported; the calibration set for metric claims is built from it after launch (ADR-25.6). An eval built from it copies the pseudonymized rows into fixtures through `tools/eval import-research`, which re-checks the opt-in per row at copy time and records the fixture's provenance; a learner's later revoke removes the fixture rows on the next `retention/daily` run, and the baseline is recomputed.

## 8. Incidents

Architecture 07 §4.15: four severities, one runbook, a `security_incidents` row with `regulator_deadline_at = detected_at + 72 h`, a tabletop before launch. A personal-data breach that must be notified is one of the triggers for engaging a lawyer (ADR-25.3). When the agent suspects exposure (a key in a log, a cross-learner read, a scrubber miss, a vendor breach notice) opens the incident first and investigates second: `tools/incident open "<one line>"` creates the row and the Slack thread. and tells Muath at once. Saying it early and being wrong costs nothing; saying it late costs the 72-hour clock.

## 9. The processor register

`legal/05-ropa.md` (from architecture 07 §4.9; the DPIA is `legal/04-dpia.md`; both completed by Muath from the official templates, ADR-25.3) is the record of processing activities: every vendor, the role it serves, what it sees, whether audio, region, retention, training opt-out, DPA status. It is rendered into `/admin/privacy` and into the privacy notice so the notice and the system cannot drift. CI refuses a vendor in `vendors.yaml` that has no register row with a signed or accepted DPA. Adding a vendor is therefore: Muath opens the account and accepts the vendor's standard DPA with SCCs, the agent fills the row and documents the retention switch, the self-review checklist is re-checked, Muath approves the PR, and only then does code call it.
