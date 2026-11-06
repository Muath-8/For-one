# 09. Data handling

Part of the For one engineering handbook. Written 2026-11-06 against architecture 07 (D1 to D6, D13, D14, §4.3, §4.4, §4.6, §4.9, §4.12, §4.13), 04 D16 to D18, 01 D7 and D15, 09 §4.5.4 and §4.9, and PRD-v2 1.3, 12.4 to 12.7. This page is the rulebook for engineers; the architecture holds the mechanisms.

## 1. What we hold, and how sensitive each class is

| Class | Examples | Where it lives | Who may see it |
|---|---|---|---|
| **Voice** (the most sensitive) | call turns, the mixed call recording when storage is on, say-it-once and voice-note clips, the name clip, the then-and-now recordings | S3 `forone-voice`, SSE-C under the learner's own data key | the learner; code; a human only through break-glass with a reason |
| **Life facts and quotes** | the notebook, `life_facts`, the learner's own words quoted in briefs, notes and proofs | Postgres, learner-scoped rows under RLS | the learner; code; Muath as `owner` with every read logged and shown in the learner's export |
| **Transcripts and chat** | streaming and verbatim transcripts, chat with the host, talkback | Postgres under RLS; text to Langfuse only with the data-use opt-in, names tokenized | the learner; code; `owner` logged; a tagger only as pseudonymized research rows |
| **Identity and contact** | display name, email, phone, birth date (validated, not stored beyond the attestation), sign-in identities, feed tokens | Postgres under RLS | `owner`, `ops` for billing state; never in logs, traces, Inngest or Sentry |
| **Produced show content** | scripts, articles, episodes, hosts' lines, Salma's notes | Postgres and S3 `forone-media`, SSE-C in the beta | the learner; the reviewer for sampled items with names tokenized |
| **Behaviour and state** | events (plays, opens, choices), sessions, schedule, allowance, billing state | Postgres | engineers, as ids and enums |
| **Operational facts** | `vendor_calls`, `pipeline_steps`, measures, alerts, audit log | Postgres | engineers |

Classification lives in code: `forone.learner.pii` names every column and field by class, the log scrubber and the Sentry scrubber read it, the export job reads it, and a new column without a class fails a unit test.

## 2. The promises the code keeps (and engineers must not break)

From PRD-v2 1.3 and 12.5, made verifiable in architecture 07 D5:

| Promise | Window | Job | Verified by |
|---|---|---|---|
| Audio deleted when voice storage is off | within 15 minutes of the turn or clip, for every learner-voice object | `audio/expire` on every ephemeral `media_objects` insert; `call/verbatim-turn` per-turn deletion | `privacy/verify` daily, sampling S3 prefixes |
| All audio deleted on revocation | within 24 hours | `learner/purge-audio` | same |
| Export | within 1 hour of the request | `learner/export` (everything, including the staff-access log) | same |
| Account deletion | live data within 24 hours; backups within 30 days; processors called (Langfuse deletion API, Resend, the voice vendors' history if any) | `learner/delete`, eight steps | same, plus `rds_assert(BackupRetentionPeriod == 30, manual_snapshots == 0)` |
| Unpaid trial data | deleted after 90 days with one warning email at day 83 | `retention/daily` | same |
| The one kept then-and-now recording | kept while the account exists, `kept_explicitly = true` | | the verify job ignores it by flag |
| Staff access visible to the learner | every content read by a human is an `audit_log` row included in the export | `forone.core.audit` | the RLS walk and a test that every admin content route writes a row |

Engineers must not: take a manual RDS snapshot (it breaks the 30-day promise; the verify job fails on any manual snapshot), turn on S3 versioning (deletion must be real), add a cache or a queue that holds learner text outside Postgres, or add a learner-voice object kind without wiring it into the three deletion jobs and the verify job in the same PR.

## 3. What engineers may and may not look at

The role matrix from architecture 07 §4.13, as rules of conduct:

**An engineer may, without asking:** read every id, enum, timestamp, count, cost, version and status; open any Inngest run, Langfuse trace metadata, CloudWatch log, Sentry event; read `/admin/learners` state, `/admin/pipeline`, `/admin/vendors`, `/admin/privacy`, `/admin/costs`, `/admin/alerts`, `/admin/crisis` (ids only); query `forone_readonly` for operational tables; read the de-identified eval fixtures; work with the synthetic learners freely.

**An engineer may, with a reason row:** read a learner's prompt and completion text by span id (`/admin/trace/{span_id}`, which writes an `audit_log` row with the reason and appears in the learner's export); read a transcript for a specific call under investigation (same path); assume the break-glass IAM role to read an audio object or a secret (MFA, CloudTrail, a Slack note in `#forone-ops` before, the audit row written by the tool). The reason is a sentence a learner could read in their export without alarm: "investigating why your notes were late on 12 December". The on-call reviews the week's reason rows on Tuesday.

**An engineer may not, ever:** read the notebook or `life_facts` page (there is none for the engineer role, and SQL against those tables is under pgaudit with a Tuesday review); listen to learner audio for curiosity, for training a model, or to "check quality" (that is the reviewer's role, with transcripts); copy learner data to a laptop, a spreadsheet, a chat with an AI assistant, a ticket, or a screenshot; run any query that joins learners together except the measures code; use a real learner as a test learner; send a message to a learner by any channel (there are three message kinds and none is manual); read a prod secret without the break-glass path.

**Muath as `owner`** can see everything, and every content read is logged and visible to the learner as "owner". The product's trust promise is that this is rare and reasoned; the Tuesday review shows the owner's reads too.

**The reviewer** (a paid native reader) sees sampled scripts with names tokenized, never transcripts, chat, the notebook or identity; signs a confidentiality agreement before the first login; has no bulk route. **The tagger** sees pseudonymized calibration rows one at a time. **`ops`** sees billing and delivery state, never content.

Infrastructure access follows: AWS console with MFA only, no access keys, CloudTrail on, ECS exec off in prod, the break-glass role alerting Slack on every assumption.

## 4. Where learner data may and may not go

| Destination | Allowed | Rule |
|---|---|---|
| Postgres (home region) | all classes | under RLS, learner-scoped |
| S3 (home region) | audio, produced media, exports | SSE-C with the learner's DEK; exports under a 1-hour signed link |
| Inngest Cloud (EU) | ids, dates, enums, short strings | no `text`, `quote`, `transcript`, `audio` field on any event model; CI test |
| Langfuse Cloud (EU) | metadata for everyone; prompt and completion text only for `data_use = true`, names tokenized; never audio | 30-day retention; deletion called by `learner/delete` |
| Sentry (EU) | scrubbed context, ids; browser errors | `beforeSend` scrub plus server-side scrub |
| CloudWatch | the log schema in handbook 06 | scrubber at the logger; PII corpus test |
| Better Stack, Slack | ids only | the poster uses the scrubber |
| Model, voice and recognition vendors | what the role needs, in transit, under the register's retention terms | only through `forone.adapters`; only vendors in `docs/ropa.md` with a DPA; the register row names what each sees |
| Resend | email address and the message body of one of the three kinds | no tracking; minimum log retention |
| A laptop | nothing from prod, ever | synthetic learners and consented fixtures only |
| Staging | synthetic learners and consented Milestone 0 fixtures | never a copy of prod |
| A third-party analytics tool | nothing | there is none, and none is added without Muath and counsel |

Embeddings are computed on model-written scripts only, never on learner turns, so the embeddings vendor sees no learner text.

## 5. Consent

Six consent kinds (architecture 07 D4), each a versioned text in `ui_strings/<language>.yaml`, each change a `consent_change` event carrying the version shown, mirrored into `consents`. Nothing is inferred from behaviour. Code reads consent before every act that needs it: `POST /v1/calls` (voice storage), `audio/expire`, the tracing middleware (data use), the research anonymizer, the proof producer (the kept recording).

Engineers: never add a consent flag without a text version; never default a consent to true; never change a consent text, which belongs to counsel; and treat a learner's "no" as a data fact the verify job will check.

## 6. Development data and fixtures

- **Synthetic learners** are the default for everything: dev seeds, staging, cassettes, the e2e run, the canary, load tests. They are generated by `tools/eval synth` from the Milestone 0 template with invented names, invented facts and planted errors.
- **Milestone 0 fixtures** (15 learner files, scripts, tags, 30 consented clips, recordings, facts, notes) are real pilot learners' data, de-identified (display name tokenized, learner id replaced by `m0-Lnn`, people's names in facts tokenized) and used as eval golden sets **only under the pilot consent**. Whether that consent covers indefinite use as test fixtures is open for Muath and counsel (architecture 09 §10 #8; 01 §10 #11); until confirmed, the fixtures that are not the 30 clips stay out of the public repository and in the `forone-fixtures` bucket, fetched by `make fixtures` with staging credentials. The repository is public today, so this is not optional.
- **Cassettes** are recorded only with synthetic learners. A cassette whose prompt contains a real learner's text is deleted and the author re-reads this page.
- **Production data in a bug report:** ids, timestamps, the trace id and the span id. Never the text. The engineer who needs the text reads it through the audited path and summarises what matters in words that contain no learner content.

## 7. Research use of transcripts

PRD 12.5.5: anonymized transcripts may be used "for checking and improving the teacher" only with the learner's opt-in. The anonymizer (architecture 07 D6) runs inside the after-pass: pseudonym by HMAC with a never-rotated secret, names, emails, phones, URLs and digit runs replaced by typed tokens, place names kept, rows removed on revoke or deletion. The research set is read only on `/admin/research` by the `tagger` role, one row at a time, never bulk-exported. An engineer building an eval from it copies the pseudonymized rows into fixtures through `tools/eval import-research`, which re-checks the opt-in per row at copy time and records the fixture's provenance; a learner's later revoke removes the fixture rows on the next `retention/daily` run, and the baseline is recomputed.

## 8. Incidents

Architecture 07 §4.15: four severities, one runbook, a `security_incidents` row with `regulator_deadline_at = detected_at + 72 h`, a tabletop in build week 5. An engineer who suspects exposure (a key in a log, a cross-learner read, a scrubber miss, a vendor breach notice) opens the incident first and investigates second: `tools/incident open "<one line>"` creates the row and the Slack thread. Saying it early and being wrong costs nothing; saying it late costs the 72-hour clock.

## 9. The processor register

`docs/ropa.md` (from architecture 07 §4.9) is the record of processing activities: every vendor, the role it serves, what it sees, whether audio, region, retention, training opt-out, DPA status. It is rendered into `/admin/privacy` and into the privacy notice so the notice and the system cannot drift. CI refuses a vendor in `vendors.yaml` that has no register row with a signed or accepted DPA. Adding a vendor is therefore: Muath opens the account and accepts the terms, the engineer fills the row and sets the retention switch, counsel confirms the transfer basis, and only then does code call it.
