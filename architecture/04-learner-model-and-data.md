# Learner model, event log and data platform

*Architecture domain 4 of 9 for For one. Written 2026-10-16, revised 2026-10-17 after design review, and revised again 2026-11-06 against the 2026-10-23 decisions (decisions.md), the second review pass (the conformance and skeptic reviews in `_review-findings.md`, which had not been applied before) and `10-decision-records.md`. Sources: PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the personalization, assessment-progress and AI-architecture lenses, and the Milestone 0 kit (04-production.md, 05-prompts.md, learner-file-template.md). It builds on `01-system-topology.md` (Python 3.12, FastAPI, Inngest, Postgres 16 on RDS in one home region, three S3 buckets) and `02-generation-pipeline.md` (the `TeacherInput` contract, `episode_artifacts`, `gloss_cache`, the fiction side of the series bible). Where this document and those two disagree, section 9 says so for the integrator. "PRD x.y" means PRD-v2 part x.y; where decisions.md or an ADR changed that part, the decision is cited instead (ADR-01).*

*Scope: PRD-v2 Part 8 (8.1 to 8.6), 9.4, 10.4 to 10.7, 12.3 (the notebook's data), 12.5 (export, deletion, retention). Tags: [DECISION] decided here; [ASSUMPTION] the spec is silent; [OPEN for Muath] only the owner can settle.*

*What changed in this revision, in one paragraph: the event log gained a real idempotency key (`event_ids`), a sequence instead of an identity column (Postgres 16), a 24-hour skew rule with no header, `received_at`/`effective_at` instead of a rewritten `occurred_at`, a `schema_version`, producer binding per type, an October partition and the `after_pass_result` event that makes a code-only rebuild possible; the rebuild runner moved to the assessment domain's `assessment/rebuild` with this domain's shadow-schema library under it, and learner-governed stores are carried over, never regenerated; the `claims` table is the assessment domain's status-lifecycle DDL and `claim_invalidations` is gone; the `briefs` cache table is gone (compile on read); the scheduler uses py-fsrs's own retrievability, pinned, with the assessment domain's grade mapping and no fractional weights; the word prior is the pipeline's saturating curve; the 14-day window is a function with an `as_of`; sensitive facts are usable only in the session they were raised; dated facts stay active until their follow-up; the intake card yields `usable`; the S3 layout puts `ephemeral/` first, uses `learners/{lid}` and the pipeline's file names, with encryption by kind (ADR-12) and versioning on kept prefixes; export is an authenticated link, not an AES zip; deletion is driven from `information_schema` with row counts in the ledger; the research set is pseudonymous (`research_pseudonyms`, ADR-09) and P1; `conversation_chunks` is P1 with Google embeddings (ADR-10); every note, margin-note and `notes_mode` artifact is removed (ADR-06); the learner carries `native_language`, `target_language`, `residence_country`, `tz` and `plan`, every Arabic-only column became a native-package lookup (ADR-02), `word_uses` is defined here (ADR-19), and the build plan is re-dated to 2026-11-18 to 12-22 (ADR-07) with export and deletion in week 3. Section 11 is the log.*

---

## 1. Summary and the decisions in one table

The learner model is one append-only table of events and nine derived tables that any engineer can drop and rebuild from the events: a code-version rebuild replays the stored, validated after-pass results (the `after_pass_result` event) through the new code with no vendor calls, in about 2 s per session; a model-version rebuild re-runs the analyst and is the assessment domain's `assessment/rebuild`, costed per learner. Nothing a model says is written directly: the after-session pass hands this domain a fixed-schema result, code validates it (every life fact's quote must exist word for word in a verbatim transcript or chat message), appends it to the log, applies it in one transaction under a per-learner lock, and bumps a per-learner integer `learner_model_version`. Every brief a role reads, every model call and every claim shown carries that integer, so a bad episode can be traced to exactly the model state that produced it. The scheduler is the open FSRS algorithm (py-fsrs, pinned) with a 0.85 recall threshold at the next drop time; word knowledge is a Beta distribution per word and surface, so every number has a range for free. The learner's pair is a row fact (`native_language`, `target_language`, ADR-02): the lexicon and inventory come from `packages/languages/<target>/`, labels and consent copy from `packages/native/<lang>/`. Audio lives in S3 under per-learner prefixes with encryption by kind (ADR-12); text lives in Postgres 16 with row-level security; export is a plain zip behind an authenticated link; deletion is a purge driven from the catalogue plus key destruction, with the 30-day backup window stated as a fact of RDS retention, not a promise we have to engineer.

| # | Decision | Chosen | Why | Rejected |
|---|---|---|---|---|
| D1 | Event store | One `events` table, append-only (no UPDATE/DELETE grant, trigger guard), range-partitioned by month on `occurred_at` (never rewritten), `seq` from an explicit sequence (Postgres 16), `schema_version` on every row, per-learner ordering by `(coalesce(effective_at, occurred_at), seq)` [DECISION, PRD-v2 8.1, 8.2] | One table is what a two-person team can operate; month partitions give retention and backup granularity the topology already asked for | Kafka or a stream (nothing consumes in real time except the after-pass, which Inngest already triggers); hash partitions by learner (no query gains over the btree at under 100M rows) |
| D2 | Verbatim enrichment of call turns | Two event types, `call_turn` (streaming, from the worker) and `call_turn_verbatim` (batch, from `call/verbatim-turn`), joined by `(call_id, turn_index)` in a view [DECISION] | Keeps the table append-only; the topology's "update the call_turn event" becomes an append | Updating the `call_turn` row (breaks D1); one event written only after verbatim (notes would wait for the whole call) |
| D3 | Idempotency | Producer-minted UUIDv7 `event_id` (the wire field `client_event_id` of the topology's contract); uniqueness enforced by the small unpartitioned `event_ids (learner_id, event_id)` table written in the same statement, because a partitioned table cannot carry that unique key; duplicates are ignored, not errors [DECISION] | The PWA replays a 24 h offline queue; the worker retries; Inngest retries steps | Server-assigned ids (replay would double-count); relying on the partitioned PK (it includes `occurred_at`, so a corrected timestamp would insert twice) |
| D4 | Learner-model version | Integer per learner, bumped by one in every store-writing transaction, recorded in `learner_model_versions` with the cause, the event high-water mark and the code versions that wrote it; serialized as `lm_v_{n}` in events and traces [DECISION] | The topology's `CallMeta` carries an int; the pipeline carries a string; both map to this | A global version (cannot tell which learner changed); a hash of the stores (not comparable, not ordered) |
| D5 | Who may write stores | `workflows` (after-session pass, rebuilds, retention) and, for learner-authored edits only, `api` synchronously inside the event append transaction; every store write takes the `learners` row lock as its first statement and `session/after-pass` runs with an Inngest concurrency key per learner [DECISION, PRD-v2 8.4.7 "fixed at once"] | A learner's correction must be true before the next screen renders; it is still an event, so a rebuild reproduces it | Learner edits through Inngest (a visible delay on "my mistake, noted"); models writing anything (PRD-v2 8.1 forbids) |
| D6 | Word knowledge | `word_bank` row per (learner, unit) with Beta(α, β) per surface (ear, eye, produced); prior from frequency rank and the word-check size estimate; ranges are the Beta 10 to 90% interval [DECISION, PRD-v2 8.3] | Gives p(understood) for the fitter and a range for every number in one representation | Point probabilities with a separate "confidence" column; logistic regression (needs data we do not have yet) |
| D7 | Review scheduler | py-fsrs (open FSRS, MIT), version pinned in `code_versions.scheduler`, library defaults, the library's own `get_retrievability`; the evidence-to-grade mapping (again, hard, good, easy) is the assessment domain's (05) and is the only one; no fractional weights in the beta; due = R(next drop) < 0.85 and `reps >= 1`; grammar structures capped at 3-day intervals for their first three reviews [DECISION, PRD-v2 9.4] | The best-evidenced scheduler available, zero research cost; a hand-written curve would diverge from the pinned library; the caps implement "every 1 to 3 days early" | Half-life regression (needs training data); a hand-made Leitner (worse by the published benchmarks); a second rating mapping with weights in this document (two owners for one number) |
| D8 | Structure and word evidence | `structure_observations` rows (one per obligatory context) and their twin `word_uses` (one per word use, ADR-19), both written by the assessment domain, plus a `structure_map` summary; the 14-day accuracy is the function `structure_acc(learner_id, structure_id, as_of, days)`, never a stored counter or a `now()`-anchored view [DECISION, PRD-v2 8.3, 10.6] | Claims need evidence links to the exact turn; windows must be recomputable at a replayed point in time after a rebuild | Counters in the map only (no evidence to open); a view on `now()` (not replayable) |
| D9 | Life facts | `life_facts` with `quote_event_id`, deterministic `fact_id` (uuid5), a three-rung ladder (`heard_once`, `usable`, `ground_truth`), sensitivity class, `valid_from`/`expires_at`, supersession chain, `entities`; sensitive candidates are never stored unconfirmed and a stored sensitive fact is usable only in the session that raised it [DECISION, PRD-v2 8.4.3] | The quote check is a database lookup, not a prompt; the editor's check 4 becomes a join | Free-text memory summaries (the lens evidence: drift, overwrite, hallucination) |
| D10 | Fact confirmation by viewing | A `fact_card_viewed` event for the one expanded card, with dwell ≥ 4 s, and no edit within the same notebook visit promotes `heard_once` to `usable`; `api` applies it when the batch carrying the visit's end marker arrives [DECISION, PRD-v2 8.4.2] | The PRD rule needs a measurable "viewed"; 4 s is long enough to read a card; a visible-in-list dwell would promote every card on screen | Promotion on any render (the learner may never have looked); a timer in `api` or "the next after-pass" (no trigger) |
| D11 | Show canon and callbacks | `show_canon` rows written by the analyst; beta callbacks are served from `show_canon` plus a `pg_trgm` search over `call_turns_v` and `chat_message`; `conversation_chunks` with a pgvector column (no typmod) embedded by Google's model (ADR-10) and exact per-learner search is P1 [DECISION, PRD-v2 14.3] | A learner has under 2,000 chunks in year one; the first season's callbacks are to things the analyst already wrote to canon; one fewer processor and extension in the beta | HNSW over all learners (filtered ANN recall problems, operational noise for nothing); an OpenAI embedding (not on the processor register) |
| D12 | Compiled briefs | `briefs.compile(role, learner_id, scope, as_of)` computes on read (300 to 500 ms); no `briefs` table: the consumer stores the compiled body with the artifact it fed (the pipeline's `brief_ref`, the call bundle, the proof row), which is where the audit trail belongs; the stable part of every brief is ordered first for prompt caching [DECISION, PRD-v2 8.6] | The version bumps after every pass and every edit, so a version-keyed cache would hit a handful of times a week; date-dependent tails (expiry, follow-ups, the due list) would be served stale from a cache | A `briefs` cache table with a GC rule (build time for nothing, and stale tails); a materialized view (cannot be role-shaped) |
| D13 | Claims store | One `claims` table with the assessment domain's DDL and status lifecycle (`candidate → passed | failed → shown → retracted`, `failed_rule`, `retracted_reason`, `notice_pending`), written only by the claim gate, `assessment/rebuild` and `memory/correct`; this domain owns the table's home, RLS and the trigger that a row with `shown_at` may change only to `retracted` and is never deleted [DECISION, PRD-v2 8.5, 10.10] | The proof producer must read exactly one table; two domains must not ship two tables named `claims`; the "never retract silently" rule is a status with a notice flag | Claims recomputed on read (a shown claim would vanish after a rebuild); a separate `claim_invalidations` table keyed by rebuild run (cannot represent `retracted(learner_disputed)`) |
| D14 | Rebuild | One runner, the assessment domain's `assessment/rebuild`, calling this domain's `forone.learner.rebuild` library: shadow copies of the derived tables, replay in log order, diff, swap in one transaction with cause `rebuild`. Two kinds: a code-version rebuild replays stored `after_pass_result` events through the new classifier, measures, scheduler and updater code (no vendor calls, about 2 s a session); a model-version rebuild re-calls the analyst (05 4.14: about $0.004 a session, $50 ceiling, 5 learners in parallel, about 20 s a session). Learner-governed stores (`life_facts`, `goals`, `out_in_world`, `show_canon`, `claims` with `shown_at`, `interests` with learner flags) are carried over, never regenerated; learner edits are replayed against carried rows [DECISION, PRD-v2 8.5] | Stores are disposable by design; the shadow schema makes a rebuild safe while the learner is using the app; a regenerated fact gets a new id and every replayed edit would miss | In-place rewrite (a learner mid-session reads half-rebuilt stores); a second runner `learner/rebuild` beside 05's (two semantics for one word); "no vendor calls" for a model-version change (false) |
| D15 | Object storage keys | This document owns the key layout (4.11): `learners/{lid}/...` on every kept learner object in all three buckets, the pipeline's file names for show audio; every learner-voice kind has an ephemeral variant under the bucket-root prefix `ephemeral/learners/{lid}/...` so one lifecycle rule on the literal prefix `ephemeral/` is the backstop; `media_objects.encryption in ('sse_c_learner','sse_kms_env')` by kind (ADR-12); versioning on for kept prefixes with a 7-day noncurrent expiry, off for `ephemeral/` [DECISION, PRD-v2 12.5, 12.6] | S3 lifecycle filters by literal prefix or tag, never by a mid-key segment; per-learner listing still works with two prefixes; a deletion bug must not erase a paid-for recording irreversibly | Content-addressed keys (deletion needs the index anyway); `{lid}/ephemeral/...` (one rule per learner, 1,000-rule limit); versioning off everywhere (zero recovery window for consented audio) |
| D16 | Export | Plain zip with `manifest.json`, `learner_model.json` (the nine stores), `events.ndjson`, `transcripts/`, `notebook.json`, `audio/` (kept audio only), built by `learner/export` within 1 h; the email carries a link to `GET /v1/exports/{id}`, which requires the learner's session and re-signs the object for 15 minutes on click; no passphrase, no AES zip; available for 14 days and while `status = 'trial_ended'` [DECISION, PRD-v2 12.5.7] | A forwarded email leaks nothing without the session; a 7-day presigned URL cannot exist under a Fargate task role (it dies with the temporary credentials); Python's `zipfile` cannot write AES and phones cannot open it | A 7-day presigned URL (expires with the task credentials, silently); an AES-256 zip with a passphrase shown in the app (needs `pyzipper`, does not open in iOS Files or Archive Utility) |
| D17 | Deletion | Access revoked synchronously and the "we started" email sent from `api` at once; the purge is driven from `information_schema` (every table with a `learner_id` column, in FK order computed at run time) under `forone_purge` with `bypassrls`, with an allow-list of tables that keep a de-identified row, per-table row counts asserted and written to `deletion_ledger`, all S3 object versions deleted, show kinds by prefix, the DEK destroyed last; the ledger holds `email_hmac` (HMAC with a server key, so a re-signup inside the 30-day window can be audited); RDS automated backup retention set to 30 days so "purged from backups within 30 days" is true by configuration [DECISION, PRD-v2 12.5.8] | A hand-written table list already missed `model_io`, `crisis_log`, `audit_log` and the payment tables; without a policy the purge role deletes zero rows and reports success; matches the promise with no custom backup scrubbing | A hand-listed purge order; a salted hash (cannot be looked up later); rewriting backups (not possible with RDS snapshots); 7-day retention (breaks PITR for an incident) |
| D18 | Research set | `research_transcripts` is P1; when built it is populated only while `data_use` consent is on, from text only, under the pseudonym in `research_pseudonyms(learner_id, pseudonym)` (ADR-09, the same id Langfuse carries), after a redaction pass over the analyst's entity list; it is called pseudonymized, never anonymized; revoking consent or deleting the account removes the learner's rows [DECISION, PRD-v2 12.5.5] | "Never sold" and "theirs" read naturally as revocable; an HMAC of a never-rotated secret is pseudonymization under another name and cannot rotate | Keeping rows after deletion (10-decision-records §10 #15 records the answer: deleted); calling name replacement "anonymization" (a legal claim the mechanism does not support) |
| D19 | Structure inventory source | `structures` table per target language, loaded from `packages/languages/<target>/structures.yaml`; for English seeded from the English Grammar Profile ids with our own labels; if permission (PRD-v2 Part 18 #8) is refused, the same table is filled from the kit's hand-written list and Cambridge's public CEFR descriptors; native-language labels come from `packages/native/<lang>/` [DECISION, PRD-v2 10.4, ADR-02] | The table shape does not depend on the source or the pair | Blocking week 1 on the license; `label_ar` columns (one native language baked into the schema) |
| D20 | Learner edits apply synchronously in `api` | See D5 | | |
| D21 | The after-pass result is an event | `stores.apply_after_pass` first appends the validated `AfterPassResult` as an `after_pass_result` event (with `analyst`, `classifier`, `memory_keeper` and `measures` versions), then applies it; the log alone, without a model, can replay every store [DECISION, PRD-v2 8.1, 8.5] | PRD 8.1 says models only propose and the log is the source of truth; the proposals are therefore part of the record, or a code-only rebuild is impossible | Keeping model output only in the stores (a classifier fix would cost a Haiku pass over every session) |
| D22 | Producer binding | The type registry carries `allowed_sources` per type; `api` sets `events.source` from the authenticated principal (session cookie = `web`, call JWT = `worker`, Inngest signature = `wf`, the import tool = `import`), never from the body; a type/source mismatch is a 422 [DECISION, PRD-v2 10.10 rule 4] | A browser must not be able to post a `call_turn_verbatim`, a `claim_shown` or an `after_pass_result`; the evidence chain is only as clean as this check | Trusting `source` from the request (the first draft) |

---

## 2. Requirements this domain implements

| PRD-v2 part | Requirement | How it is met here |
|---|---|---|
| 1.2 law 1 | No game furniture; only monotonic plain counts | The stores hold no percentage or level intended for display; `notebook_counts` (words owned, hours heard, hours spoken) are the only learner-visible numbers; they never decrease except to correct a bug, and then Salma says so once (4.3.9) |
| decisions.md §3, ADR-06 | Teaching is invisible: no notes, polish card or margin note | No `notes` store, no `note_shown` or `margin_note` event, no `notes_mode` consent; the only correction channel is the host's recast inside the conversation (`call_turn.recast`) planned by the teacher; the notebook, the proof, "why this episode" and the claims stay as evidence (4.1.1, 4.9, 4.10) |
| decisions.md §1, ADR-02 | No launch country or pair | `learners.native_language`, `target_language`, `residence_country`, `tz`; lexicon and inventory per target language from `packages/languages/<target>/`; labels, consent copy and the quote normalizer per native language from `packages/native/<lang>/` (4.4, 4.7.1) |
| decisions.md §2, ADR-04, ADR-05 | Plans of 1, 2 or 3 new episodes a day | `learners.plan` (topology); the teacher brief carries `plan.episodes_per_day` and the day's `episodes_today`; `episode_next_requested` events feed the pre-write rule; the due list is sized per day, not per episode (4.9, 4.5.3) |
| 1.2 law 3 | Vetoes and additions re-target the same day | `working_on_edit` applied synchronously, version bump, `working_on.changed` emitted (4.7.7) |
| 1.2 law 10 | Text used once, language comes back | FSRS due list per word, chunk and structure (4.5) |
| 1.2 law 12, 1.3 #1 | No claim without proof; no memory stated unless confirmed | `claims` only via the gate (4.10); briefs expose only `usable` or `ground_truth` facts (4.9) |
| 1.3 #5 | See, export, delete | 4.12 |
| 1.3 #6 | Told, not inferred; sensitive classes never inferred | Validator rejects any fact without a quote; sensitive class requires `confirmed_in_session` (4.7.3) |
| 1.3 #7 | Wrong memory is a bug | `wrong_memory_flag` fixes the fact at once and feeds the 16.1 metric (4.7.7) |
| 1.3 #8 | Data use opt-in | `research_transcripts` [P1] gated by `consents.data_use` under `research_pseudonyms` (4.12.4); Langfuse receives text only for `data_use` learners after `anonymize()` (ADR-09, 4.14) |
| 2.2 A3, A4, A9 | Intake facts with cards; word check seeds priors; consent at A9 | `onboarding_answer`, `word_check_answer`, `consent_change` events; prior seeding (4.5.1) |
| 2.3 | Day-2 callback sourced verbatim | `facts.verify_quote` and `show_canon` (4.7, 4.8) |
| 3.6 | Active day definition | Derived from `playback_intervals(session_id)` (merged, deduplicated `play`/`pause`/`seek` intervals ≥ 50% of duration), `call_turn` (any) or `small_door`; computed by `api` after each append for the session, stored once on `sessions.active_day_marked_at` (topology table); `learner_schedule.expects_drop` is set from it for the next local day (ADR-19) |
| 4 | Door states persist indefinitely | `doors.position` (topology) holds position; the events hold history |
| 5.1, 5.3, 5.4.5, 5.4.11, 5.5, 5.6, 5.7 | Everything logged | Event taxonomy 4.1.1 |
| 5.4.4 | Pause profile adapts within 1.0 to 2.5 s | `skills.pause_profile` (4.3.4) |
| 5.4.5 | Word or hint from produced-word history | `briefs.compile('salma_talkback')` returns the produced-word dict (4.9) |
| 5.4.11, 12.5.2 | Audio deleted within 15 min when storage is off; evidence kept at low confidence | `media_objects.ephemeral`, every learner-voice kind under the `ephemeral/` prefix with one lifecycle rule, `call_turn_verbatim.low_confidence_reason` (4.1, 4.11) |
| 6.3 check 4 | Every fact used is confirmed, unexpired, not "don't bring up", quote exists | One SQL predicate, the `facts_usable(learner_id, as_of, role)` function (4.7.5) |
| 7.5 | Series bible stored with the learner model | Fiction side in the pipeline domain's tables; `show_canon` here; `SeriesBibleExcerpt` compiled here (4.8) |
| 8.1 | Event log is the source of truth; models propose, code decides; live roles never write; compiled briefs | D1, D5, 4.3, 4.9 |
| 8.2 | Event fields: learner, session, door, type, time, payload, model and prompt versions, cost | `events` DDL (4.1.2) |
| 8.3 | Nine stores, writers, ranges on every estimate | 4.3 |
| 8.4 | Life-fact rules | 4.7 |
| 8.5 | Rebuilds; shown claims never retracted silently | `after_pass_result` events (D21), the rebuild library under `assessment/rebuild` (D14), `claims.status = 'retracted'` with `notice_pending` (4.10) |
| 8.6 | Compiled briefs per role | 4.9 |
| 9.4 | FSRS-style scheduler; due below 0.85 at next drop; grammar 1 to 3 days early | 4.5 (py-fsrs pinned; grades from 05) |
| 10.3 | Say-it-once and shadow lines scored internally, never shown | `AfterPassResult.pronunciation` rows stored in `skills.pronunciation` (internal, never in a brief or the notebook) (4.3.4) |
| 9.5 | Tapped twice or more becomes a recall candidate; kept words scheduled like targets | `word_bank.tapped_n`, `kept` (4.3.1) |
| 10.4 | Inventory of a few hundred structures; 12 categories; frequency list and lemmatizer | 4.4 |
| 10.5, 10.6, 10.7 | Error vs slip; lifecycle; avoidance | 4.6 |
| 10.8 | Skills on a fine scale with ranges, CEFR words never shown unprompted | `skills` (4.3.4) |
| 10.11 | Rating model pinned per 4-week window | `learner_model_versions.code_versions.rater_pin` records it per write; `apply_after_pass` refuses a result whose `rater_pin` differs from `vendors.yaml roles.rater.pinned_until`'s pin for the window the session falls in, so a rebuild cannot mix rater versions inside a window; the pin itself is `vendors.yaml` (topology) |
| 12.3 | Notebook sections | Each maps to a store or view (4.3.9) |
| 12.4, 12.5 | "See all my data", "delete all recordings"; data rules 1 to 9 | "See" is the notebook plus the export (no separate in-app view of the nine stores in the beta [DECISION]); "delete all recordings" is `learner/purge-audio` over every learner-voice kind including `kept_explicitly` (4.12.2); 4.11, 4.12 |
| 12.6 | Row-level isolation; per-learner keys; no cross-learner paths except gloss cache and opt-in transcripts | RLS on every learner table (4.13); only `gloss_cache` (pipeline) and `research_transcripts` lack `learner_id`; learner-voice objects SSE-C under the learner DEK, show audio SSE-KMS (ADR-12) |
| 14.3 | Postgres; vector index only for past-conversation callbacks | D11 |
| 14.5, 16.1 | Cost traced per role, vendor, learner | `events.cost_usd` for events that cost money; `learner_model_version` on every adapter call via `CallMeta` |
| 15 | Teacher update within 10 min; export within 1 h; audio 15 min / 24 h; deletion 24 h / 30 days (the 90 s notes budget is removed, ADR-06) | 4.12, section 6 |
| 19.2 week 1 (re-dated by ADR-07) | Event log and learner-model schema; lexicon and scheduler | Section 7 |

Budgets that bind this domain: none of the per-session AI cost is spent here (no model calls in the beta; the P1 embedding call is the pipeline's line); the domain's own cost is storage and database time, reported as fixed per month and variable per session (section 6). Latency: `briefs.compile('teacher')` under 5 s (pipeline's assumption; target 500 ms), `word_bank.p_understood` for a 1,500-unit script under 100 ms, learner edits applied before the response returns (under 200 ms, including the wait for a running after-pass's row lock, up to 3 s at p99).

---

## 3. Architecture

### 3.1 Components

Everything in this domain is one Python package, `forone.learner`, imported by `api` (append and learner edits) and `workflows` (everything else). No service of its own.

| Module | Job | Called by |
|---|---|---|
| `forone.learner.events` | `append(batch, principal)`: validate against the type schema and `schema_version`, bind `source` to the principal and check `allowed_sources`, de-duplicate through `event_ids`, assign `seq`, insert; `read(learner_id, since_seq)`; the type registry, payload schemas and one upgrader per `(type, schema_version)` | `api` (`POST /v1/events`, `POST /internal/events`), `workflows` |
| `forone.learner.versions` | `lock(learner_id)` (the `learners` row lock, first statement of every store write); `bump(learner_id, cause, code_versions) -> int` inside a caller's transaction; `current(learner_id)` | every store writer |
| `forone.learner.stores` | `apply_after_pass(AfterPassResult)` (appends `after_pass_result`, locks, applies); `apply_learner_edit(event)`; the nine store writers | `workflows` (after-pass), `api` (learner edits) |
| `forone.learner.rebuild` | Library, no function of its own: `shadow(learner_id)`, `replay(learner_id, kind: code|model, results: Iterable[AfterPassResult])`, `diff`, `swap`; the carry-over list for learner-governed stores | the assessment domain's `assessment/rebuild` (05 4.14) |
| `forone.learner.lexicon_db` | The `lexicon_lemmas`, `lexicon_chunks`, `structures`, `reporting_categories` tables per target language; loaders from `packages/languages/<target>/`; native labels from `packages/native/<lang>/` | pipeline's `lexicon`, assessment's classifier |
| `forone.learner.word_bank` | `p_understood(unit, surface)`, `p_understood_many(units, surface)`, priors (the pipeline's saturating curve), Beta updates, owned-word rule, `word_uses` reads | fitter, analyst updater, notebook |
| `forone.learner.scheduler` | py-fsrs wrapper: `review(card, grade, at, is_structure)`, `retrievability(card, at)` (the library's), `due_list(learner_id, at_drop)` | teacher brief, updater |
| `forone.learner.facts` | `verify_quote(fact_id)` and `verify_quote_text(learner_id, quote, quote_event_id)`, `propose(candidates)`, ladder transitions, shelf life, supersession, follow-ups, interests salience on read, the per-native-language normalizer | memory keeper validator, editor check 4, notebook |
| `forone.learner.canon` | `show_canon` writes; `search_callbacks` over canon and `pg_trgm`; `series_bible_excerpt(learner_id)`; `conversation_chunks` embed and vector search [P1] | analyst, writer brief |
| `forone.learner.briefs` | `compile(role, learner_id, scope, as_of)` on read, no cache; the field-to-table map per role (4.9) | pipeline (teacher, writer, host), call-worker via `api`, after-pass (chat), Salma when asked, proof |
| `forone.learner.claims` | Home of the `claims` table (05's DDL): RLS, the shown-row trigger, `mark_shown`, `passed_for_proof(learner_id, week)`; the gate, `retract` and candidate writes are the assessment domain's module | claim gate (writes), proof producer, return episode, finale |
| `forone.learner.export` | Build the zip; `GET /v1/exports/{id}` re-signing | `learner/export` step bodies, `api` |
| `forone.learner.deletion` | Catalogue-driven purge, row counts, ledger | `learner/delete` step bodies |
| `forone.learner.retention` | Trial-ended queries, orphan audits, partition creation, ephemeral overdue checks | `retention/daily` (per learner-local midnight, ADR-16) step bodies |
| `forone.learner.pii` | The column classification as code (used by export, Langfuse scrubbing and tests; a CI test fails when a `learner_id` table is unclassified) | export, tracing middleware, `learner/delete` |

### 3.2 Diagram, in text

Draw three lanes left to right: **Producers**, **The log**, **Derived**.

- Producers (left): `web` (player, article, chat, notebook, controls), `call-worker` (call turns, talkback, floor, silence), `workflows` (after-pass outputs, verbatim turns, claims shown, consent jobs). All three arrows enter one box in `api` labelled `POST /v1/events` or `POST /internal/events`, which calls `events.append`.
- The log (middle): one tall box `events` (monthly partitions drawn as shelves; one shelf labelled `after_pass_result`). Three side boxes attached to it: `event_ids` (the idempotency key), `learner_model_versions` (a counter with a pointer into the log: "high-water seq") and `media_objects` (topology; an arrow to S3 drawn as three buckets `media`, `voice`, `exports`, each with a `learners/{lid}/` folder icon and the voice bucket with a second `ephemeral/` folder).
- Derived (right): nine boxes in a 3×3 grid: `word_bank` (+ `word_uses` beneath it), `structure_map` (+ `structure_observations` beneath it), `error_profile`, `skills`, `interests`, `life_facts` (+ `follow_ups`), `goals`, `taste`, `show_canon` (+ `conversation_chunks`, dashed, P1). Above the grid: `claims`. Below the grid: `briefs.compile` (a function, no table) with outgoing arrows labelled teacher, writer, host, talkback, explain, chat, proof.
- Arrows: a thick arrow from `events` to a box `stores.apply_after_pass` (in `workflows`) that fans into the nine boxes; a thin arrow from `api` labelled `apply_learner_edit` into `life_facts`, `interests`, `goals`, `word_bank(kept)` and `claims(shown)`; a dashed loop from the nine boxes back to `events` labelled "rebuild: shadow, replay, swap" with `assessment/rebuild (05) → forone.learner.rebuild` on it. Every arrow into a store passes through a small lock icon labelled `versions.lock` and then a gate icon labelled `versions.bump`.
- A lock icon on every box on the right and on `events`: RLS by `learner_id`.

### 3.3 The four flows

**A. A session's events (write path, live).** `web` buffers events for up to 2 s and posts batches of up to 50 to `POST /v1/events` with the session cookie; the server sets `forone.learner_id` for RLS, sets `source` from the principal (D22), validates each payload against its type schema and `schema_version`, checks the type's `allowed_sources`, inserts the ids into `event_ids` with `on conflict do nothing returning`, inserts the rows that came back into `events` in the same statement (a CTE), and returns `{accepted, duplicates, rejected[]}`. The same call runs `playback_intervals(session_id)` over the deduplicated rows and computes whether the day just became active (PRD-v2 3.6): if so, it sets `sessions.active_day_marked_at` once, sets `learner_schedule.expects_drop` for the next local day (ADR-19) and sends `day.became_active` (topology). The worker posts through `POST /internal/events` with the call JWT; the payload is identical. A request from a session revoked by deletion (step 1 of 4.12.2) returns 410 and appends nothing. No store is touched on this path.

**B. The after-session pass (write path, within 10 min).** The assessment domain's `session/after-pass` (one function since ADR-06; no notes stage) produces one `AfterPassResult` (4.3.0) and calls `stores.apply_after_pass(result)`, which: appends the result as an `after_pass_result` event (D21; `event_id = uuid5(run_id, "after_pass_result")` so a retried step appends nothing new); then in one transaction takes the `learners` row lock as its first statement (`versions.lock`), checks `rater_pin` against the window, validates every life-fact candidate against the log, applies word, structure (including the `word_uses` and `structure_observations` rows), error, skill, interest, goal, taste and canon updates, runs the scheduler for every unit touched, bumps the version with cause `after_pass`, writes a `learner_model_versions` row with the high-water `seq` and the code versions (`analyst`, `classifier`, `measures`, `memory_keeper`, `scheduler`, `rater_pin`), and returns the new version. `session/after-pass` runs with Inngest `concurrency: {key: event.data.learner_id, limit: 1}` so two passes for one learner (the main call and round two minutes apart, or a retried step racing its predecessor) never read the same snapshot. The caller then sends `session.after_pass.completed {learner_id, session_id, learner_model_version}` (topology event).

**C. A learner edit (write path, synchronous).** `web` posts a `fact_card_edit`, `notebook_edit`, `working_on_edit`, `wrong_memory_flag` or `consent_change` event. `api` appends it and, in the same transaction, calls `stores.apply_learner_edit(event)`, which takes the `learners` row lock first (waiting out a running pass, 1 to 3 s at worst), changes the one store row the edit names, bumps the version with cause `learner_edit`, and returns. For `working_on_edit` it then sends `working_on.changed`; for `consent_change` it sends `learner.consent_changed`. The response carries the new `learnerModelVersion` (the topology's cache key). This is the only store write outside `workflows`.

**D. A rebuild.** The runner is the assessment domain's `assessment/rebuild` (05 4.14), started by a passing `calibration/run` on an `assessment_version` change or by hand with a learner scope; this domain supplies the library it calls (`forone.learner.rebuild`) and the two kinds it distinguishes. (a) **Code-version rebuild** (classifier, measures, scheduler, updater, or a store-DDL change): `shadow(learner_id)` creates shadow copies of the regenerated tables (`stores_shadow` schema, same DDL); `replay` walks the log in `(coalesce(effective_at, occurred_at), seq)` order, feeding each stored `after_pass_result` event through the new code with the replay cursor as `as_of` (so `structure_acc` and the scheduler see the historical window), and replaying learner edits at their positions; no vendor call; about 2 s a session, a 100-session learner in under 4 minutes. (b) **Model-version rebuild** (analyst prompt or model, `rater_pin`): 05 re-runs `analyst.full` over `call_turns_v` and `chat_message` per session, validates, appends a new `after_pass_result` with the new versions, and feeds it to the same `replay`; about 20 s and $0.004 a session, $50 ceiling per run, 5 learners in parallel (05's numbers); the memory keeper is not re-run. In both kinds the learner-governed stores are carried over, never regenerated: `life_facts`, `follow_ups`, `goals`, `out_in_world`, `show_canon`, `interests` rows with `hard_dislike`, `no_go` or `source = 'told'`, and every `claims` row; their ids are stable and the replayed edits land. `diff` compares the claims the new stores support with the `passed` and `shown` rows; `swap` replaces the regenerated rows in one transaction with cause `rebuild`, and 05's module marks a shown claim the new stores no longer support `retracted(reason='rebuild')` with `notice_pending = true` (4.10). A test in build week 2 replays a learner with three edits (a removal, a "don't bring up", a ground-truth correction) and asserts all three hold afterwards.

### 3.4 Interfaces to other domains

Functions provided (Python, in-process):

```python
# forone/learner/api.py  (the public surface of the package; everything else is internal)
def append_events(learner_id: UUID, batch: list[EventIn], source: Source) -> AppendResult: ...
def current_version(learner_id: UUID) -> int: ...
def apply_after_pass(result: AfterPassResult) -> int: ...                 # appends after_pass_result, locks, applies; returns new learner_model_version
def apply_learner_edit(event: Event) -> int: ...
def compile_brief(role: Role, learner_id: UUID, scope: BriefScope | None = None, as_of: datetime | None = None) -> Brief: ...
def p_understood(learner_id: UUID, unit_id: str, surface: Literal["ear","eye"]) -> float: ...   # the prior, in memory, for a unit with no row
def p_understood_many(learner_id: UUID, unit_ids: list[str], surface) -> dict[str, float]: ...
def due_list(learner_id: UUID, at: datetime) -> DueList: ...               # .due (<= 60), .kept, .active_targets
def playback_intervals(session_id: UUID) -> list[tuple[int, int]]: ...     # merged play intervals in ms, capped at duration
def verify_quote(fact_id: UUID) -> QuoteCheck: ...                         # the editor's check 4 form
def verify_quote_text(learner_id: UUID, quote: str, quote_event_id: UUID) -> QuoteCheck: ...   # the validator's form
def facts_usable(learner_id: UUID, as_of: date, role: Role, session_id: UUID | None = None) -> list[Fact]: ...
def search_callbacks(learner_id: UUID, query: str, k: int = 5) -> list[Callback]: ...   # canon + trigram in the beta; chunks P1
def mark_claim_shown(claim_id: UUID, surface: str, event_id: UUID) -> None: ...   # idempotent; the gate, retract and candidates are 05's module
def passed_claims(learner_id: UUID, since: date | None) -> list[Claim]: ...  # status in ('passed','shown')
def build_export(learner_id: UUID, export_id: UUID) -> ExportManifest: ...
def purge_learner(learner_id: UUID) -> PurgeReport: ...                     # per-table row counts, object versions deleted
# rebuild library (called by 05's assessment/rebuild)
def rebuild_shadow(learner_id: UUID) -> ShadowHandle: ...
def rebuild_replay(h: ShadowHandle, results: Iterable[AfterPassResult], kind: Literal["code","model"]) -> None: ...
def rebuild_diff_and_swap(h: ShadowHandle) -> RebuildReport: ...
```

Inngest events consumed (names from the topology's catalogue unless marked new): `call.ended`, `learner.consent_changed`, `learner.export_requested`, `learner.deletion_requested`, `claim.shown` [new, sent by the surface that showed a claim: `{learner_id, claim_id, surface, event_id}`]. `assessment.rebuild_requested` and its completion are the assessment domain's (05); the `/admin` button sends 05's event, not one of mine.

Inngest events emitted: `working_on.changed`, `learner.consent_changed` (relayed from the event), `learner.model_updated` [new: `{learner_id, learner_model_version, cause}`; the pipeline may use it to recompile a brief], `export.ready {learner_id, export_id}` [new], `learner.purged {learner_id}` [new].

Functions I own the step bodies of: `learner/export`, `learner/delete` (purge), the data parts of `retention/daily` (trial-ended queries, partition creation, orphan audits, ephemeral overdue checks), and `learner/purge-audio`'s object step (07 owns the function). I own no rebuild function (D14).

---

## 4. Detailed design

### 4.1 The event log

#### 4.1.1 Taxonomy

Every type from PRD-v2 8.2 that survives ADR-06 (no `note_shown`, no `margin_note`; the notes door is gone) plus the twelve this design needs (marked +). Payload fields are the Pydantic schema names; every payload carries `schema_version smallint` (4.1.2); `door` is one of `listen, shadow, read, call, chat, round_two, small_door, onboarding, notebook, controls, proof, today, feed`. "Who" is the producer and is enforced (D22): `web`, `worker` (call-worker), `wf` (workflows), `import` (the Milestone 0 tool); `api` is the gate that binds the source, not a producer, and mints no type of its own.

| type | Who | door | Payload (required fields) | Consumed by |
|---|---|---|---|---|
| `play` | web | listen, read, proof | `episode_id, media_kind (episode|read_aloud|recap|proof), position_ms, speed, surface (app|feed)` | active-day rule, taste, hours heard |
| `pause` | web | listen | `episode_id, position_ms` | taste |
| `seek` | web | listen | `episode_id, from_ms, to_ms` | taste |
| `speed` | web | listen | `episode_id, speed (0.75|0.85|1.0)` | skills (listening support) |
| `replay_line` | web | listen, read, call | `episode_id, line_id, source (button|media_session)` | word bank (weak), skills |
| `huh` | web | listen | `episode_id, line_id, sentence_text, unit_ids[]` | word bank, huh rate, dials |
| `transcript_toggle` | web | listen | `episode_id, open: bool, on_first_play: bool` | skills (transcript default) |
| `tap` | web | listen, read | `episode_id, surface (transcript|huh|article), unit_id, lemma, sense_key, line_id|sent_id, chunk: bool` | word bank (strong), recall candidates |
| `keep` | web | listen, read | `episode_id, unit_id, sense_key, sentence_text` | word bank.kept, notebook |
| `mark` | web | listen | `episode_id, line_id, position_ms, sentence_text, clip_media_object_id` | notebook |
| `article_scroll` | web | read | `episode_id, depth (0..1), ms_on_page, section_times[]` | reading speed, taste |
| `read_aloud` | web | read | `episode_id, on: bool, position_ms` | skills |
| `call_turn` | worker | call, round_two, onboarding | `call_id, turn_index, speaker (learner|host|salma), text_stream, started_ms, ended_ms, words_stream[] {t,s,e,c}, recast: {target_lemma|structure_id}|null, clarification: bool, nudge: bool, recall_gap_id|null, mode (live|voice_note)` | everything after |
| `call_turn_verbatim` + | wf | call, round_two, onboarding, small_door | `call_id, turn_index, text, words[] {t,s,e,c}, vendor, disfluencies_kept, low_confidence_reason|null, mode (live|voice_note)`; a small-door voice note is a `call_turn_verbatim` with `mode='voice_note'` and the note's `call_id` | analyst, classifier, measures, quote check |
| `talkback` | worker | call | `call_id, turn_index, asked_native (the learner's words in `native_language`), lemma_asked|null, gave (word|hint), hint_kind|null, latency_ms` | word bank, talkback metric |
| `hold_floor` | worker | call | `call_id, turn_index, held_ms` | pause profile |
| `silence` | worker | call | `call_id, turn_index, silence_ms, host_action (backchannel|smaller_question|offer_wrap|none)` | anxiety mode, pause profile |
| `say_it_once` | web | shadow | `episode_id, line_id, media_object_id, reference_text` (pronunciation only, ADR-06; scored internally, never shown) | pronunciation (internal) |
| `shadow` | web | shadow | `episode_id, line_id, media_object_id, reference_text` | pronunciation, elicited imitation |
| `chat_message` | web, wf | chat | `thread_id, message_index, speaker (learner|host), text, in_reply_to|null` | analyst, canon, quote check |
| `idea_shown` | wf | chat, today | `plan_id, ideas[] {idea_id, rank, is_wildcard, from_life, arc_id}` | taste, "tomorrow chosen" metric |
| `idea_chosen` | web | chat, today | `plan_id, idea_id, source (pick|tell_salma|remix|cutoff), remix: {topic|format|cast}|null, salma_text|null` | taste, pipeline |
| `swap` | web | today | `episode_id, replaced_by_episode_id` | taste, `swap_count_30d` |
| `episode_next_requested` + | web | today | `plan_id, episode_index (2|3), previous_episode_id` (the "next one" action, ADR-05; `episodes_per_day` is checked in `api`) | taste, the `prewrite_extra` rule (02), allowance measures |
| `small_door` | web | small_door | `episode_id, recap_played_ms, voice_note_media_object_id|null, duration_ms` | active day, after-pass |
| `fact_card_edit` | web | notebook, onboarding | `fact_id, action (edit|remove|dont_bring_up|confirm), new_text|null` | life facts (sync) |
| `fact_card_viewed` + | web | notebook | `fact_id, dwell_ms, visit_id` (one per expanded card per visit; dwell counted only while the card is expanded and in the centre band, 06) | ladder promotion (4.7.2) |
| `notebook_visit_ended` + | web | notebook | `visit_id, cards_viewed: int` (the end marker; its batch triggers rule (c) in `api`) | ladder promotion (4.7.2) |
| `notebook_edit` | web | notebook | `section (about_you|out_in_world|kept|goals), action (add|edit|remove), item_id|null, text|null, date|null` | goals, out-in-world (sync) |
| `working_on_edit` | web | notebook, proof | `action (veto|add|unhide|hide), item_id|null, text|null, voice_media_object_id|null` | targeting (sync), `working_on.changed` |
| `claim_shown` | wf, web | proof, today, finale, notebook | `claim_id, surface (proof|new_for_you|finale|where_do_i_stand|return), text_shown` | claims.status = shown |
| `consent_change` | web | onboarding, controls | `kind (voice_storage|data_use|drop_notification|captions|gap_note), value, text_shown_version` | retention jobs (sync relay) |
| `worth_it_answer` | web | proof | `proof_id, answer (yes|mostly|no), why_text|null` | 16.2 |
| `wrong_memory_flag` | web, wf | call, chat, notebook | `fact_id|null, canon_id|null, said_by (host|salma), quote_of_show, learner_correction|null` | facts (sync), 16.1 metric |
| `onboarding_answer` + | worker, web | onboarding | `step (A1..A10), question_key, answer_text, answer_mode (voice|text), skipped: bool, target_language_line: bool`; A9 carries `residence_country` (ISO 3166-1, asked, never inferred, ADR-20) and the pair (`native_language`, `target_language`) | intake facts, first estimate, `learners` row fields |
| `word_check_answer` + | web | onboarding | `item_id, lemma|pseudoword, band, answered_known: bool, ms` | priors (4.5.1) |
| `recording` + | web | proof, finale, notebook | `recording_id, task (retell|opinion|repeat), media_object_id, reference_text|null, kept_explicitly: bool` (offered by the proof and the finale, ADR-06) | then-and-now rater |
| `followed_answer` + | web | listen | `episode_id, answer (most|about_half|little)` | 16.2 against `why.predicted` |
| `host_turn_text` + | wf | chat | reserved; host chat text is `chat_message{speaker:host}`; this type exists for the small-door host reply: `episode_id, text` | canon |
| `crisis_flag` + | worker, wf | call, chat, after_pass | `source (host|salma|analyst), language, resources_shown: bool, continued: bool` | SB 243 log (security domain reads) |
| `session_closed` + | wf | any | `session_id, reason (next_published|learner_started_next|deleted)` | rebuild ordering |
| `after_pass_result` + | wf | any | the validated `AfterPassResult` (4.3.0) as the payload, plus `versions {analyst, classifier, measures, memory_keeper, rater_pin}`, `rejected_facts: int`; `event_id = uuid5(run_id, 'after_pass_result')`; `model_versions` and `cost_usd` carry the analyst and memory keeper calls | code-version rebuilds (D21, D14); the audit |

Rules: a type not in the registry is rejected with 422 and logged; each registry entry carries `allowed_sources` and `api` rejects a type whose bound `source` is not in the list with 422 (D22; `call_turn_verbatim`, `claim_shown{wf}`, `after_pass_result`, `crisis_flag{wf}`, `session_closed`, `idea_shown`, `host_turn_text` are `wf`-only; `call_turn`, `talkback`, `hold_floor`, `silence` are `worker`-only; a browser can never post them); every payload carries `schema_version` and `forone.learner.events` keeps one upgrader per `(type, version)` so a two-year replay reads old rows through the current schema; payload fields beyond the schema are kept (forward compatibility) but never read by the stores; `model_versions`, `prompt_version` and `cost_usd` are set only on events produced by a model (`call_turn{speaker:host|salma}`, `chat_message{speaker:host}`, `idea_shown`, `call_turn_verbatim`, `after_pass_result`) and are null otherwise; the id age check (4.1.3) applies to `source in ('web','worker')` only.

#### 4.1.2 DDL

```sql
-- forone/learner/sql/001_events.sql
create extension if not exists pgcrypto;

-- Postgres 16 (01 §1 row 6: RDS for PostgreSQL 16; compose pins pgvector/pgvector:pg16). Identity columns on a
-- partitioned table need Postgres 17, so seq comes from an explicit sequence.
create sequence events_seq as bigint;

-- The idempotency key. A range-partitioned table cannot carry unique (learner_id, event_id) because every unique
-- index must include the partition key, so the key lives in this small unpartitioned table, written in the same
-- statement as the events row (D3): insert into event_ids ... on conflict do nothing returning drives which rows go on.
create table event_ids (
  learner_id        uuid not null,
  event_id          uuid not null,                             -- the wire field client_event_id (01 §4 contract)
  occurred_at       timestamptz not null,                      -- so a duplicate's partition can be found without a scan
  primary key (learner_id, event_id)
);

create table events (
  seq               bigint not null default nextval('events_seq'),  -- server order; monotonic per database
  event_id          uuid not null,                             -- UUIDv7, minted by the producer; = event_ids.event_id
  learner_id        uuid not null references learners(id),
  session_id        uuid,                                      -- null for onboarding before the first session, controls, feed fetches
  episode_id        uuid,
  call_id           uuid,
  door              text not null,
  type              text not null,
  schema_version    smallint not null default 1,               -- the payload schema version of the registry entry that validated it
  occurred_at       timestamptz not null,                      -- producer clock, NEVER rewritten (it is the partition key)
  received_at       timestamptz not null default now(),        -- server clock at receipt (01's name)
  effective_at      timestamptz,                               -- server-corrected time when the skew rule fired (4.1.4); null otherwise
  source            text not null check (source in ('web','worker','wf','import')),   -- bound to the principal (D22)
  payload           jsonb not null,
  model_versions    jsonb,                                     -- {"host":"anthropic/claude-sonnet-5.5@2026-11-20"} on model-produced events
  prompt_version    text,
  learner_model_version integer,                               -- the version a model-produced event READ
  cost_usd          numeric(8,5),
  vendor_call_id    uuid,                                      -- cost domain's vendor_calls.id (written in its own transaction, ADR-13)
  inngest_run_id    text,
  primary key (learner_id, event_id, occurred_at),             -- partition key must be in the PK; uniqueness is event_ids
  check (jsonb_typeof(payload) = 'object')
) partition by range (occurred_at);

-- Partitions are created three months ahead by retention/daily (topology). Naming: events_2026_11.
-- events_2026_10 exists for the Milestone 0 import (2026-10-24 to 11-18); events_default catches anything else
-- rather than failing an insert.
create table events_2026_10 partition of events for values from ('2026-10-01') to ('2026-11-01');
create table events_2026_11 partition of events for values from ('2026-11-01') to ('2026-12-01');
create table events_2026_12 partition of events for values from ('2026-12-01') to ('2027-01-01');
create table events_2027_01 partition of events for values from ('2027-01-01') to ('2027-02-01');
create table events_default partition of events default;

create index events_learner_time on events (learner_id, coalesce(effective_at, occurred_at), seq);
create index events_learner_seq  on events (learner_id, seq);                      -- versions.bump's max(seq) per learner
create index events_learner_type on events (learner_id, type, occurred_at);
create index events_session on events (session_id, occurred_at) where session_id is not null;
create index events_call on events (call_id, ((payload->>'turn_index')::int)) where call_id is not null;   -- same expression as call_turns_v
create index events_seq on events (seq);

-- Append-only: the application roles cannot update or delete; a trigger guards even the owner.
revoke update, delete, truncate on events from forone_app, forone_workflows, forone_admin, forone_readonly, forone_human;
create or replace function events_immutable() returns trigger language plpgsql as $$
begin
  if current_setting('forone.purge_mode', true) is distinct from 'on' then
    raise exception 'events is append-only (set forone.purge_mode=on only inside learner/delete)';
  end if;
  return old;
end $$;
create trigger events_no_update before update or delete on events
  for each row execute function events_immutable();

-- Row-level security: every learner-facing query sees one learner. nullif() makes an empty GUC yield zero rows
-- instead of a cast error. forone_purge bypasses RLS (alter role forone_purge bypassrls) so learner/delete deletes
-- real rows; forone_admin has aggregate-only views (ADR-17), not a policy here.
alter table events enable row level security;
create policy events_by_learner on events
  using (learner_id = nullif(current_setting('forone.learner_id', true), '')::uuid);
create policy events_service on events to forone_workflows using (true);
alter table event_ids enable row level security;
create policy event_ids_by_learner on event_ids using (learner_id = nullif(current_setting('forone.learner_id', true), '')::uuid);
create policy event_ids_service on event_ids to forone_workflows using (true);
```

The view that gives the assessment domain a call's turns with both texts:

```sql
create view call_turns_v as
select s.learner_id, s.call_id, (s.payload->>'turn_index')::int as turn_index,
       s.payload->>'speaker' as speaker,
       s.payload->>'text_stream' as text_stream,
       v.payload->>'text' as text_verbatim,
       v.payload->'words' as words_verbatim,
       (v.payload->>'low_confidence_reason') as low_confidence_reason,
       (s.payload->>'started_ms')::int as started_ms, (s.payload->>'ended_ms')::int as ended_ms,
       s.payload->'recast' as recast, s.event_id as stream_event_id, v.event_id as verbatim_event_id
from events s
left join events v on v.learner_id = s.learner_id and v.call_id = s.call_id
   and v.type = 'call_turn_verbatim' and (v.payload->>'turn_index')::int = (s.payload->>'turn_index')::int
where s.type = 'call_turn';
```

#### 4.1.3 Idempotency

- `event_id` is a UUIDv7 minted by the producer at the moment the event happens (the PWA, the worker, or the workflow step). On the wire it is the topology's `client_event_id`; the column is `event_id` because workflow-produced events have no client. The time prefix makes it sortable and lets the server reject ids more than 7 days old or in the future for `source in ('web','worker')`; `import` ids are `uuid5(file_path, row)` minted by `tools/m0_import.py` with `occurred_at` from the kit and are exempt.
- Uniqueness is `(learner_id, event_id)` and is enforced by `event_ids` (D3): one CTE inserts the batch into `event_ids ... on conflict do nothing returning event_id` and inserts into `events` only the ids that came back. A duplicate is reported in `AppendResult.duplicates`; it is never an error, because the offline queue and worker retries will send duplicates by design. The partitioned PK `(learner_id, event_id, occurred_at)` is not the dedupe key and `occurred_at` is never rewritten, so a replay with the original timestamp meets the same key.
- For events the workflow produces inside a retried step, the step derives `event_id` deterministically: `uuid5(namespace, f"{run_id}:{step}:{key}")`, so a retry appends nothing new.
- Batches are atomic per request: either every non-duplicate row is inserted or none.

#### 4.1.4 Ordering

- `occurred_at` is the producer's clock and is stored as sent. `api` compares it to `received_at`: if `occurred_at` is more than `events.client_clock_skew_max_h` (24 h, the length of the PWA's offline queue; one rule for 01, 04 and 06, no header) in the past or more than 5 minutes in the future, `effective_at = received_at` is set and the event is flagged `payload._clock_corrected=true`; `occurred_at` itself is never rewritten (it is the partition key and part of the PK). A client-settable header cannot bypass the rule because there is none.
- Within one learner, replay order is `(coalesce(effective_at, occurred_at), seq)`. `seq` breaks ties and preserves arrival order for events with equal timestamps (the worker emits `call_turn` and `silence` at the same millisecond).
- Cross-learner order does not matter anywhere.
- The after-session pass is triggered by `call.ended`/`chat.closed` and reads whatever events have arrived by the time its stage runs; an event that arrives after the pass (an offline replay a day later) is folded in by the next pass or by a rebuild. That is why stores are rebuildable rather than exactly-once.

#### 4.1.5 Retention

Events are kept for the life of the account (they are the learner's data and the only source of rebuilds). On deletion, the learner's rows are removed from every partition (4.12). Nothing is detached from Postgres in the beta [DECISION]: the topology's "cold partitions older than 90 days compacted to Parquet" line (01 §6 capacity table) is superseded by this rule, because export and rebuild read `events` only and a detached partition would need a second reader. After the beta, partitions older than 24 months may be compacted to Parquet under `forone-exports/archive/{yyyy_mm}/` with a reader in `forone.learner.events` that export and rebuild use transparently; that reader is written before the first detach, not after. [ASSUMPTION] At 10,000 learners, about 300 events per session and 20 sessions a month, the table grows by about 60M rows (about 60 GB with payloads) a month; that is ordinary for RDS with monthly partitions and is addressed in section 6.

#### 4.1.6 Example rows

```json
{ "event_id": "0192f3c1-4b1e-7a63-8d2c-2b5d1e7f0a11", "learner_id": "7d0b...", "session_id": "c4e9...", "episode_id": "a1f2...",
  "door": "listen", "type": "huh", "schema_version": 1, "occurred_at": "2026-12-28T07:52:14.310+03:00", "received_at": "2026-12-28T04:52:15.002Z", "source": "web",
  "payload": { "episode_id": "a1f2...", "line_id": "s2-l07", "sentence_text": "The referee robbed us, and not for the first time.",
               "unit_ids": ["referee", "rob", "not_for_the_first_time"] } }

{ "event_id": "0192f3c4-9a02-7b11-9f0e-7c1d2a3b4c5d", "learner_id": "7d0b...", "session_id": "c4e9...", "call_id": "e77a...",
  "door": "call", "type": "call_turn", "schema_version": 1, "occurred_at": "2026-12-28T08:03:41.120+03:00", "source": "worker",
  "payload": { "call_id": "e77a...", "turn_index": 6, "speaker": "learner", "text_stream": "I went to the match with my cousin and we was late",
               "started_ms": 61230, "ended_ms": 66010, "words_stream": [{"t":"I","s":61230,"e":61300,"c":0.98}, "..."], "recast": null,
               "clarification": false, "nudge": false, "recall_gap_id": null, "mode": "live" } }

{ "event_id": "0192f3c6-1c40-7c22-a1b2-3c4d5e6f7a8b", "learner_id": "7d0b...", "session_id": "c4e9...", "call_id": "e77a...",
  "door": "call", "type": "call_turn_verbatim", "schema_version": 1, "occurred_at": "2026-12-28T08:03:52.004+03:00", "source": "wf",
  "model_versions": {"verbatim_stt": "assemblyai/universal-3.6@2026-11-10"}, "cost_usd": 0.00061, "vendor_call_id": "5f3e...",
  "payload": { "call_id": "e77a...", "turn_index": 6, "text": "I went to the- I go, I went to the match with my cousin and, uh, we was late",
               "words": [{"t":"I","s":61230,"e":61298,"c":0.97}, {"t":"went","s":61310,"e":61520,"c":0.91}, "..."],
               "vendor": "assemblyai", "disfluencies_kept": true, "low_confidence_reason": null, "mode": "live" } }

{ "event_id": "0192f3d0-7e01-5a9b-8c3d-4e5f6a7b8c9d", "learner_id": "7d0b...", "session_id": "c4e9...", "door": "call", "type": "after_pass_result",
  "schema_version": 1, "occurred_at": "2026-12-28T08:14:02.771Z", "source": "wf", "inngest_run_id": "01JF...", "learner_model_version": 60,
  "model_versions": {"analyst": "anthropic/claude-haiku-5.5@2026-12-01", "memory_keeper": "anthropic/claude-haiku-5.5@2026-12-01"}, "cost_usd": 0.0041,
  "payload": { "versions": {"analyst": "1.3.0", "classifier": "1.1.2", "measures": "1.0.4", "memory_keeper": "1.2.0", "rater_pin": "claude-sonnet-5.5@2026-12-01"},
               "rejected_facts": 1, "result": { "word_uses": ["..."], "structure_observations": ["..."], "fact_candidates": ["..."], "measures": {"...": "..."} } } }
```

The learner's timestamps carry the learner's own offset (`learners.tz`); nothing here assumes a timezone (ADR-16).

### 4.2 Learner-model versioning

```sql
create table learner_model_versions (
  learner_id        uuid not null references learners(id) on delete cascade,
  version           integer not null,
  cause             text not null check (cause in ('onboarding','after_pass','learner_edit','consent','rebuild','retention','import','admin')),
  session_id        uuid,
  high_water_seq    bigint not null,                 -- last events.seq folded into the stores by this write
  code_versions     jsonb not null,                  -- {"analyst":"1.3.0","classifier":"1.1.2","measures":"1.0.4","memory_keeper":"1.2.0","scheduler":"py-fsrs==5.1.0/default","rater_pin":"claude-sonnet-5.5@2026-12-01","package":"languages/en@2026.11.1"}
  stores_touched    text[] not null,
  created_at        timestamptz not null default now(),
  primary key (learner_id, version)
);
-- the current version is max(version); cached on learners.lm_version for cheap reads
alter table learners add column lm_version integer not null default 0;
```

```python
# forone/learner/versions.py
def lock(conn, learner_id) -> int:
    """FIRST statement of apply_after_pass, apply_learner_edit and rebuild.swap: serializes every store writer for
    one learner before any store is read, so two writers never compute on the same unlocked snapshot."""
    return conn.execute(text("select lm_version from learners where id=:l for update"), {"l": learner_id}).scalar()

def bump(conn, learner_id, cause, *, session_id=None, stores_touched, code_versions) -> int:
    """Must run inside the caller's transaction, after lock(). Does not take the lock itself."""
    new = conn.execute(text("select lm_version from learners where id=:l"), {"l": learner_id}).scalar() + 1
    hw = conn.execute(text("select coalesce(max(seq),0) from events where learner_id=:l"), {"l": learner_id}).scalar()  # events_learner_seq
    conn.execute(text("""insert into learner_model_versions(learner_id, version, cause, session_id, high_water_seq, code_versions, stores_touched)
                         values (:l,:v,:c,:s,:hw,:cv,:st)"""), dict(l=learner_id, v=new, c=cause, s=session_id, hw=hw,
                         cv=json.dumps(code_versions), st=stores_touched))
    conn.execute(text("update learners set lm_version=:v where id=:l"), {"v": new, "l": learner_id})
    return new
```

`learner_model_versions` is not mirrored into `events` (the first draft's `lm_write` event is cut for the beta): the log plus `after_pass_result` replays every store without it, and the table is exported with the stores. `code_versions.scheduler` names the installed py-fsrs release (`pyproject.toml` pins it in build week 1), so a rebuild cannot silently run a different curve.

Where the version is recorded: `briefs.learner_model_version`; `CallMeta.learner_model_version` on every adapter call (topology 4.5), so `vendor_calls` and Langfuse carry it; `events.learner_model_version` on model-produced events; `claims.learner_model_version`; `episodes.model_versions` already exists, and the pipeline's `EpisodePlan.learner_model_version` is the string form `lm_v_{n}`. The string form is only for serialization; comparisons use the integer.

### 4.3 The nine stores

Every store table has `learner_id`, `lm_version` (the version of the write that last touched the row), `updated_at`, RLS as in 4.1.2, and an index starting with `learner_id`. Every estimate is stored as parameters from which a range follows (Beta for probabilities, mean and standard deviation for scales), never as a bare point. Row ids in the learner-governed stores (`life_facts`, `goals`, `out_in_world`, `show_canon`, `working_on_additions`) are deterministic: `uuid5(learner_id, store, quote_event_id or event_id, normalized key)`, so the same proposal yields the same id on any replay and a learner edit that names the id resolves after a rebuild (D14). Text columns that hold the learner's own words are in whatever language the learner used; text the system renders for the learner (`text` in facts and goals, labels) is in `learners.native_language` and the column is named `text_native` where a second language could appear (ADR-02).

#### 4.3.0 The write contract from the after-session pass

```python
# forone/learner/contracts.py (consumed from the assessment domain; this is the only way stores change after a session)
class AfterPassResult(BaseModel):
    learner_id: UUID; session_id: UUID; call_ids: list[UUID]; chat_thread_ids: list[UUID]
    code_versions: dict[str, str]                      # analyst, classifier, measures, memory_keeper, rater_pin (checked against vendors.yaml's window)
    word_uses: list[WordUse]                           # {unit_id, event_id, occurred_at, clean: bool, correct: bool, prompted: bool, quote}  -> word_uses rows (ADR-19)
    word_evidence: list[WordEvidence]                  # non-production evidence the analyst adds: {unit_id, surface: ear|eye, kind: EvidenceKind, event_id, confidence}
    structure_observations: list[StructureObs]        # {structure_id, obligatory: bool, correct: bool, prompted: bool, event_id, quote, confidence, blurred_meaning: bool, category}
    pronunciation: list[dict]                          # {event_id (say_it_once|shadow|recording), score_0_100, vendor}; internal only (PRD-v2 10.3)
    fsrs_grades: list[dict]                            # {unit_id|structure_id, grade: again|hard|good|easy, event_id}; the assessment domain's one mapping (05)
    uptake: dict                                       # {content_uptake_0_2: int, recast_uptake: [{structure_id|lemma, repeated: bool}], self_corrections: int}
    measures: Measures                                 # per task type: speech_rate_wpm, mlr_words, mid_clause_pause_rate, articulation_rate, mtld, beyond_2000_share, clause_len, subordination; pause_profile_obs: {eot_silences_ms: [...]}; talk_share
    reached_for: list[dict]                            # {paraphrase, lemma_given, event_id}
    can_do_moments: list[dict]                         # {can_do_id, quote, event_id}
    fact_candidates: list[FactCandidate]               # {text, fact_type, quote, quote_event_id, sensitivity: str|None, confirmed_in_session: bool, dated_event: date|None, supersedes_hint: str|None}
    interest_signals: list[dict]                       # {topic_key, kind: mentioned|talked_long|chose|skipped|dislike|no_go, strength: float, event_id}
    goal_signals: list[dict]                           # {kind: can_do|season_goal, text, quote, event_id}
    canon: list[CanonIn]                               # {kind, who, text, episode_id|None, event_id}
    out_in_world: list[dict]                           # {text, quote, event_id, date}
    anxiety_flag: bool; low_energy_signals: list[str]
```

`stores.apply_after_pass` first appends the result as an `after_pass_result` event (D21), then opens the transaction with `versions.lock`, refuses the result if `code_versions.rater_pin` is not the pin `vendors.yaml roles.rater` names for the session's 4-week window (PRD-v2 10.11), and applies the sections in the order: facts (validator first, because a rejected candidate must not reach canon), words and `word_uses`, structures and `structure_observations`, errors, skills (including `pronunciation`), interests, goals, taste, canon, scheduler (from `fsrs_grades`), counts; then `versions.bump`. The function is pure over `(result, stores, as_of)`: a replay with `as_of` set to the result's `occurred_at` reproduces the live write.

#### 4.3.1 Word bank (written by code from the log and the analyst)

```sql
create table word_bank (
  learner_id        uuid not null references learners(id) on delete cascade,
  unit_id           text not null,                 -- lemma ("referee") or chunk id ("c:not_for_the_first_time")
  unit_kind         text not null check (unit_kind in ('lemma','chunk')),
  sense_key         text,                          -- dominant sense seen; per-occurrence sense lives in events
  ear_a real not null, ear_b real not null,        -- Beta params: p(understood by ear)
  eye_a real not null, eye_b real not null,        -- p(understood in reading)
  prod_a real not null, prod_b real not null,      -- p(produced correctly)
  prior_p           real not null,                 -- the frequency prior used (for rebuild audits)
  status            text not null default 'unseen' check (status in ('unseen','planned','heard','read','attempting','owned')),
  heard_n int not null default 0, read_n int not null default 0, tapped_n int not null default 0, huh_n int not null default 0,
  produced_prompted_n int not null default 0, produced_unprompted_n int not null default 0,
  produced_sessions uuid[] not null default '{}',  -- distinct sessions with correct unprompted production (owned rule)
  talkback_n        int not null default 0,
  kept              boolean not null default false, kept_at timestamptz,
  first_seen_at timestamptz, last_seen_at timestamptz, owned_at timestamptz,
  own_sentences     jsonb not null default '[]',   -- up to 3: [{text, session_id, event_id, at}]
  fsrs              jsonb not null,                -- py-fsrs Card.to_dict(): {card_id, state, step, stability, difficulty, due, last_review}; reps and lapses kept beside it
  reps int not null default 0, lapses int not null default 0,
  lm_version        integer not null, updated_at timestamptz not null default now(),
  primary key (learner_id, unit_id)
);
create index word_bank_due on word_bank (learner_id, ((fsrs->>'due')::timestamptz));
create index word_bank_status on word_bank (learner_id, status);

-- Per-use word evidence (ADR-19): the twin of structure_observations, written by the assessment domain's updater from
-- AfterPassResult.word_uses; one row per learner production of a unit; owned here, read by word_bank, claims and the notebook.
create table word_uses (
  learner_id   uuid not null references learners(id) on delete cascade,
  unit_id      text not null,
  event_id     uuid not null,                       -- the call_turn_verbatim, chat_message or recording event
  occurred_at  timestamptz not null,
  clean        boolean not null,                    -- confidence >= package threshold or source is chat (claim gate rule 4)
  correct      boolean not null,
  prompted     boolean not null,                    -- Salma gave the word, or a recall gap asked for it
  quote        text not null,                       -- the learner's sentence, verbatim
  session_id   uuid, surface text not null check (surface in ('call','round_two','chat','small_door','recording')),
  lm_version   integer not null,
  primary key (learner_id, unit_id, event_id)
);
create index word_uses_learner_time on word_uses (learner_id, unit_id, occurred_at desc);
```

Sizing rule (a contract the fitter can test): a `word_bank` row is created on the first evidence of any kind (a `play` completion that contained the unit, a `tap`, a `huh`, a `keep`, a `word_use`), never on planning alone; `p_understood_many` returns the prior computed in memory (4.5.1) for every unit without a row, so the fitter's coverage query costs one indexed read for the rows that exist and no writes. About 5,000 rows per learner after a year.

Example rows:

```json
{ "learner_id": "7d0b...", "unit_id": "referee", "unit_kind": "lemma", "sense_key": "referee#n#match official",
  "ear_a": 5.6, "ear_b": 1.1, "eye_a": 6.1, "eye_b": 0.9, "prod_a": 3.4, "prod_b": 1.6, "prior_p": 0.78,
  "status": "owned", "heard_n": 9, "read_n": 4, "tapped_n": 1, "huh_n": 1, "produced_prompted_n": 1, "produced_unprompted_n": 2,
  "produced_sessions": ["c4e9...", "d10a..."], "kept": false, "first_seen_at": "2026-12-08T07:41:00+03:00", "owned_at": "2026-12-12T08:05:11+03:00",
  "own_sentences": [{"text": "the referee gave him a yellow card for nothing", "session_id": "d10a...", "event_id": "0192...", "at": "2026-12-12T08:05:11+03:00"}],
  "fsrs": {"state": "review", "stability": 11.2, "difficulty": 4.9, "due": "2026-12-23T04:40:00Z", "last_review": "2026-12-12T05:05:11Z", "reps": 5, "lapses": 1},
  "lm_version": 61 }

{ "learner_id": "7d0b...", "unit_id": "c:not_for_the_first_time", "unit_kind": "chunk", "ear_a": 1.4, "ear_b": 3.2, "eye_a": 1.6, "eye_b": 2.4,
  "prod_a": 0.8, "prod_b": 3.2, "prior_p": 0.30, "status": "heard", "heard_n": 1, "tapped_n": 1, "huh_n": 1,
  "fsrs": {"state": "learning", "stability": 0.9, "difficulty": 6.8, "due": "2026-12-10T04:40:00Z", "reps": 1, "lapses": 0}, "lm_version": 58 }
```

Rebuild: delete the learner's `word_bank` and `word_uses` rows; for every `tap`, `huh`, `keep`, `play` completion, `talkback`, and every `word_uses`, `word_evidence` and `fsrs_grades` entry in the stored `after_pass_result` events, re-apply 4.5.2 in log order with `as_of` = the event's time. Deterministic given the same `scheduler` pin; `kept` and `kept_at` are replayed from `keep` events, so the learner's choice survives.

#### 4.3.2 Structure map and observations (analyst proposes, code checks and writes)

```sql
create table structure_observations (
  id                uuid primary key,              -- uuid5(session_id, event_id, structure_id, span) so a replay is idempotent
  learner_id        uuid not null references learners(id) on delete cascade,
  session_id        uuid not null, event_id uuid not null,
  structure_id      text not null references structures(structure_id),
  category          text not null,                 -- one of the 12, denormalized for reporting
  obligatory        boolean not null, correct boolean not null, prompted boolean not null,
  blurred_meaning   boolean not null default false,
  confidence        real not null,                 -- min recognizer confidence over the span; chat = 1.0
  clean             boolean not null,              -- confidence >= package threshold OR source is chat (claim gate rule 4)
  quote             text not null, corrected text,
  surface           text not null check (surface in ('call','round_two','chat','small_door','recording','shadow','say_it_once')),
  observed_at       timestamptz not null,
  classifier_version text not null
);
create index so_learner_struct_time on structure_observations (learner_id, structure_id, observed_at desc);

create table structure_map (
  learner_id        uuid not null references learners(id) on delete cascade,
  structure_id      text not null references structures(structure_id),
  state             text not null default 'not_seen' check (state in ('not_seen','heard','attempting','taking','stable')),
  target_lifecycle  text not null default 'none' check (target_lifecycle in ('none','active','taking','stable','recheck','dropped_by_learner')),
  avoidance         boolean not null default false, avoidance_flagged_at timestamptz,
  heard_n           int not null default 0,        -- input occurrences in shipped episodes (from the fitter's realized counts, via publish)
  consecutive_targeted smallint not null default 0, last_targeted_session_id uuid, targeted_sessions uuid[] not null default '{}',
  taking_at timestamptz, stable_at timestamptz, stable_confirmed_at timestamptz,
  recheck_due_at    timestamptz,                   -- next of the 2, 4, 8 week re-checks
  examples          jsonb not null default '[]',   -- up to 3 of the learner's own correct sentences {text, session_id, event_id}
  fsrs              jsonb not null,
  lm_version        integer not null, updated_at timestamptz not null default now(),
  primary key (learner_id, structure_id)
);

-- the 14-day accuracy window is a function with an as_of, never a stored counter and never a view on now(), so a
-- rebuild replaying a session in January sees January's window (PRD-v2 8.3, 10.6, D8)
create function structure_acc(p_learner uuid, p_structure text, p_as_of timestamptz, p_days int default 14)
returns table (contexts int, correct int, sessions int, clean_contexts int, first_at timestamptz, last_at timestamptz)
language sql stable as $$
  select count(*) filter (where obligatory)::int,
         count(*) filter (where obligatory and correct)::int,
         count(distinct session_id) filter (where obligatory)::int,
         count(*) filter (where obligatory and clean)::int,
         min(observed_at) filter (where obligatory), max(observed_at) filter (where obligatory)
  from structure_observations
  where learner_id = p_learner and structure_id = p_structure
    and observed_at > p_as_of - make_interval(days => p_days) and observed_at <= p_as_of
$$;
-- convenience for the live path and the admin pages only
create view structure_acc_14d as
select m.learner_id, m.structure_id, a.* from structure_map m, lateral structure_acc(m.learner_id, m.structure_id, now()) a;
```

Example `structure_map` row:

```json
{ "learner_id": "7d0b...", "structure_id": "egp:past_simple_irregular_narrative", "state": "attempting", "target_lifecycle": "active",
  "avoidance": false, "heard_n": 47, "consecutive_targeted": 2, "targeted_sessions": ["c4e9...", "d10a..."],
  "examples": [{"text": "I went to the match with my cousin", "session_id": "c4e9...", "event_id": "0192f3c6..."}],
  "fsrs": {"state": "learning", "stability": 2.1, "difficulty": 6.2, "due": "2026-12-11T04:40:00Z", "reps": 2, "lapses": 1}, "lm_version": 61 }
```

Rebuild: delete observations and map rows; re-insert observations from the stored `after_pass_result` events (ids are deterministic); recompute the map by running `structures.step(map_row, observations, as_of)` over observations in time order with `as_of` advancing with the replay cursor, so `taking → stable` fires on the same day it fired live.

#### 4.3.3 Error profile (analyst)

```sql
create table error_profile (
  learner_id   uuid not null references learners(id) on delete cascade,
  structure_id text not null references structures(structure_id),
  category     text not null,
  count_total  int not null default 0, count_clean int not null default 0, blurred_n int not null default 0,
  sessions     uuid[] not null default '{}',       -- distinct sessions with at least one observation
  status       text not null default 'observed' check (status in ('observed','pattern','targeting','dropped_by_learner','resolved')),
  examples     jsonb not null default '[]',        -- 2 or 3 verbatim {quote, corrected, session_id, event_id}
  first_at timestamptz, last_at timestamptz,
  lm_version integer not null, updated_at timestamptz not null default now(),
  primary key (learner_id, structure_id)
);
```

`status` becomes `pattern` when `count_clean >= 3 and cardinality(sessions) >= 2` (PRD-v2 10.5); `targeting` when the teacher picks it; `dropped_by_learner` on a veto (unless `blurred_n > 0`, which the teacher may still target "if it breaks meaning"); `resolved` when the structure reaches `stable_confirmed_at`. Rebuild: derived entirely from `structure_observations` with `correct = false`.

#### 4.3.4 Skills (code)

```sql
create table skills (
  learner_id        uuid primary key references learners(id) on delete cascade,
  listening         jsonb not null, reading jsonb not null, speaking jsonb not null, writing jsonb not null,
      -- each {mean: 48.0, sd: 6.5, n_obs: 7, calibrated: false, anchored_at: timestamptz|null}; internal scale 10..90 anchored to CEFR (4.3.4 table)
  fluency           jsonb not null default '{}',   -- per task type: {"retell": {"speech_rate_wpm": {mean, sd, n}, "mlr_words": {...}, "mid_clause_pause_rate": {...}, "articulation_rate": {...}}, "round_two": {...}, "recording": {...}}
  complexity        jsonb not null default '{}',   -- same shape: clause_len, subordination, mtld, beyond_2000_share
  comprehension     jsonb not null default '{}',   -- {uptake_mean_4w, huh_per_min_2w_median, taps_per_100_2w, followed_vs_predicted: [...]}
  pause_profile     jsonb not null default '{"eot_silence_ms": 1500, "n": 0}',   -- adapted within 1000..2500 (PRD-v2 5.4.4)
  reading_speed_wpm real,
  transcript_default text not null default 'folded' check (transcript_default in ('folded','open')),
  talkback_per_call_4w real,
  pronunciation     jsonb not null default '{}',   -- {say_it_once: {mean, sd, n}, shadow: {...}, recording: {...}} from AfterPassResult.pronunciation; INTERNAL: never in a brief, a claim or the notebook (PRD-v2 10.3)
  lm_version integer not null, updated_at timestamptz not null default now()
);
create table skill_snapshots (                      -- [P1] weekly and at every recording; the then-and-now and re-anchoring read these
  learner_id uuid not null references learners(id) on delete cascade,
  taken_at timestamptz not null, reason text not null check (reason in ('weekly','recording','rebuild','onboarding')),
  snapshot jsonb not null, lm_version integer not null,
  primary key (learner_id, taken_at)
);
```

Scale anchors [ASSUMPTION, GSE-like]: A2 30 to 42, B1 43 to 58, B2 59 to 75, C1 76 to 84. Only Salma's "where do I stand" (PRD-v2 10.8) translates to words, and only when `calibrated = true` (set by the assessment domain's calibration job). Update rule in the updater: Gaussian conjugate update with observation variance from the measure's test-retest standard error once estimated; until then a fixed `sd_obs = 8` so one session moves the mean by at most about a point. The pause profile: `eot_silence_ms = clamp(1000, 2500, median(last 30 learner end-of-turn silences) + 300)`, recomputed after each call. Rebuild: recompute from replayed `measures` in order.

#### 4.3.5 Interests (memory keeper and behavior)

```sql
create table interests (
  learner_id   uuid not null references learners(id) on delete cascade,
  topic_key    text not null,                      -- normalized ("football:al_hilal"), from the memory keeper's normalizer
  topic_label  text not null, topic_label_native text,   -- label in target_language; label in native_language when it differs
  entities     jsonb not null default '[]',        -- the memory keeper's normalized entity list for the topic (02's TeacherInput interests[].entities)
  salience_base real not null,                     -- 0..1 at last_engaged_at; the current salience is computed on read (4.7.6), never written back
  depth        text not null default 'curious' check (depth in ('curious','fan','expert')),
  source       text not null check (source in ('told','behavior','intake','waitlist')),
  last_engaged_at timestamptz not null,            -- dormant is a predicate: salience(now) < interests.dormant_below
  hard_dislike boolean not null default false, no_go boolean not null default false,  -- no_go = "never bring up" (topic form)
  quote text, quote_event_id uuid,
  lm_version integer not null, updated_at timestamptz not null default now(),
  primary key (learner_id, topic_key)
);
```

#### 4.3.6 Life facts and follow-ups (memory keeper; learner edits)

```sql
create table life_facts (
  fact_id           uuid primary key,              -- uuid5(learner_id, 'life_facts', quote_event_id, fact_type || ':' || normalized text): stable across rebuilds
  learner_id        uuid not null references learners(id) on delete cascade,
  fact_type         text not null references fact_shelf_life(fact_type),
  text_native       text not null,                 -- the fact in Salma's words, in the learner's native_language
  quote             text not null,                 -- the learner's exact words, in whatever language they used
  quote_event_id    uuid not null,                 -- the call_turn_verbatim, chat_message or typed onboarding_answer event (4.7.1)
  session_id        uuid, said_at timestamptz not null,
  entities          jsonb not null default '[]',   -- the memory keeper's normalized entities (02's facts_usable[].entities)
  confidence        text not null check (confidence in ('heard_once','usable','ground_truth')),
  confirmed_by      text check (confirmed_by in ('repeated','asked','viewed_unedited','edited','intake_card')),
  confirmed_at      timestamptz, repeat_event_id uuid,
  sensitivity       text check (sensitivity in ('health','money','relationships','religion','politics')),
  status            text not null default 'active' check (status in ('active','dormant','superseded','deleted')),
  valid_from        date not null, expires_at date,
  dont_bring_up     boolean not null default false,
  supersedes_fact_id uuid references life_facts(fact_id), superseded_by_fact_id uuid,
  dated_event_on    date,                          -- for follow-ups; a dated fact stays active until its follow-up is used or expired (4.7.4)
  times_used        int not null default 0, last_used_episode_id uuid,
  people            jsonb,                         -- {"name_used": "my manager", "relation": "manager"} for side characters based on real people
  lm_version integer not null, updated_at timestamptz not null default now()
);
create index facts_learner_status on life_facts (learner_id, status, confidence);

create table follow_ups (
  follow_up_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  fact_id uuid not null references life_facts(fact_id) on delete cascade,
  due_on date not null, state text not null default 'pending' check (state in ('pending','used','expired','cancelled')),
  used_in_episode_id uuid, used_at timestamptz,
  lm_version integer not null
);
create unique index one_follow_up_per_fact on follow_ups (fact_id);          -- one follow-up per dated event (PRD-v2 8.4.5)

create table fact_shelf_life (                     -- product configuration, loaded at deploy; the notebook's label per fact_type comes from
  fact_type text primary key, shelf_days int, sensitive_default boolean not null default false   -- packages/native/<lang>/strings/fact_types.yaml (ADR-02)
);
insert into fact_shelf_life values
 ('job', 270, false), ('study', 270, false), ('city', 365, false), ('person', 365, false),
 ('plan_dated', null, false), ('trip', 60, false), ('this_week', 7, false),
 ('possession', 180, false), ('preference', 120, false), ('routine', 120, false),
 ('health', 14, true), ('money', 60, true), ('relationship', 90, true), ('religion', 365, true), ('politics', 30, true);
```

Example rows:

```json
{ "fact_id": "f-8821", "learner_id": "7d0b...", "fact_type": "plan_dated", "text_native": "مقابلة عمل لمنصب إقليمي", "quote": "I have an interview in six weeks for a regional role",
  "quote_event_id": "0192f2a0-...", "session_id": null, "said_at": "2026-12-23T19:12:40+03:00", "confidence": "usable", "confirmed_by": "intake_card",
  "confirmed_at": "2026-12-23T19:13:05+03:00", "entities": ["regional role", "interview"], "sensitivity": null, "status": "active", "valid_from": "2026-12-23", "expires_at": null,
  "dont_bring_up": false, "dated_event_on": "2027-02-03", "times_used": 3, "lm_version": 3 }

{ "fact_id": "f-9102", "learner_id": "7d0b...", "fact_type": "person", "text_native": "مديره الجديد صارم", "quote": "my new manager is strict, like really strict",
  "quote_event_id": "0192f3c9-...", "session_id": "c4e9...", "said_at": "2026-12-28T08:05:30+03:00", "confidence": "heard_once", "confirmed_by": null,
  "entities": ["manager"], "sensitivity": null, "status": "active", "valid_from": "2026-12-28", "expires_at": "2027-12-28", "people": {"name_used": "my manager", "relation": "manager"}, "lm_version": 61 }

{ "follow_up_id": "fu-31", "learner_id": "7d0b...", "fact_id": "f-8821", "due_on": "2027-02-04", "state": "pending", "lm_version": 3 }
```

The first row is an intake card the learner left standing: `usable`, not `ground_truth` (PRD-v2 8.4.2 gives ground truth only to a fact the learner edited; a card edited with ✎ at A3 is `ground_truth` with `confirmed_by='edited'`). The native-language text is the learner's `native_language` (Arabic for this learner); nothing in the schema assumes it.

#### 4.3.7 Goals (Salma's after-session pass; the learner)

```sql
create table goals (
  goal_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  kind text not null check (kind in ('can_do','season_goal','why_this_language')),   -- why_this_language: the A2 answer, per target_language (ADR-02)
  text text not null, text_native text, quote text, quote_event_id uuid,            -- goal_id = uuid5(learner_id, 'goals', quote_event_id or event_id, kind || ':' || normalized text)
  season_id uuid,                                  -- for season_goal (pipeline's seasons table)
  status text not null default 'active' check (status in ('active','met','dropped')),
  evidence jsonb not null default '[]',            -- can_do moments: [{quote, event_id, session_id}]
  set_by text not null check (set_by in ('learner','salma','intake')),
  lm_version integer not null, updated_at timestamptz not null default now()
);
```

The anchor and rhythm live in `learner_schedule` (topology); `goals` does not duplicate them. Rebuild: from `onboarding_answer`, `notebook_edit{section:goals}` and replayed `goal_signals`.

#### 4.3.8 Taste (code)

```sql
create table taste (
  learner_id uuid primary key references learners(id) on delete cascade,
  format_completion jsonb not null default '{}',   -- {"debate": {"started": 6, "completed": 5}, ...}
  host_completion   jsonb not null default '{}',
  words_per_min     jsonb not null default '{}',   -- {"by_format": {"debate": 112}, "by_topic": {"football:al_hilal": 128}}
  length_pref_min   real, time_of_day_hist jsonb not null default '{}',  -- 24 buckets of session starts, local
  swap_n int not null default 0, skip_patterns jsonb not null default '{}',   -- {"read": 4, "call": 1}
  lm_version integer not null, updated_at timestamptz not null default now()
);
```

Preference only; nothing here is read as a learning style (PRD-v2 8.3). Rebuild: pure aggregation over `play`, `idea_chosen`, `swap`, `call_turn`, door states.

#### 4.3.9 Show canon (analyst), the notebook counts and the notebook views

```sql
create table show_canon (
  canon_id uuid primary key,                       -- uuid5(learner_id, 'show_canon', event_id or episode_id, kind || ':' || normalized text)
  learner_id uuid not null references learners(id) on delete cascade,
  kind text not null check (kind in ('position_learner','position_host','thing_said','joke_used','callback_made','retold')),
  who text not null check (who in ('learner','karim','mona','salma')),
  text text not null, quote text, event_id uuid, episode_id uuid, session_id uuid,
  topic_key text, at timestamptz not null,
  lm_version integer not null
);
create index canon_learner_topic on show_canon (learner_id, topic_key, at desc);
create index canon_learner_text_trgm on show_canon using gin (text gin_trgm_ops);   -- the beta's callback search (4.8)

-- learner-visible counts: the only numbers the notebook shows; they only grow in normal operation, and a correction is said, not hidden (4.3.9 text)
create table notebook_counts (
  learner_id uuid primary key references learners(id) on delete cascade,
  words_owned int not null default 0, hours_heard_s bigint not null default 0, hours_spoken_s bigint not null default 0,
  lm_version integer not null, updated_at timestamptz not null default now()
);
```

Hours heard (PRD-v2 12.3): the sum of `playback_intervals(session_id)` over every session (the merged union of `play`/`pause`/`seek` intervals from the deduplicated rows, capped at the episode's duration, recomputed after each append for the session so out-of-order offline batches converge), plus each feed episode's full duration once when a `call_turn`, `chat_message` or `small_door` for that episode exists and no app `play` reached 50%. Hours spoken: learner `call_turn` durations plus `say_it_once`, `shadow`, `small_door` voice notes and recordings. A rebuild recomputes both. If a rebuild lowers a count (it cannot, except after a bug), the count is corrected, not frozen: trust promise 1 forbids showing a number the system knows is wrong, and PRD-v2 12.3's "never reset" is about not punishing the learner, not about preserving a wrong figure. The correction is handled like a retracted claim: a `claims` row of kind `count_corrected` with `notice_pending = true` so Salma says so once in the next proof (4.10).

Notebook sections as reads (the notebook is evidence and stays, decisions.md §4, ADR-06): *What I'm working on* = `working_on` items (held in the pipeline's current `EpisodePlan.targets` filtered by `error_profile.status <> 'dropped_by_learner'`, with one `examples[0]` sentence each; the `working_on_items` view joins them); *About you* = `life_facts` (all statuses but `deleted`, with `confidence` rendered as "I think..." for `heard_once`), `interests`, `goals`; *Words you own* = `word_bank where status='owned'` with `own_sentences[0]` and the clip from the sentence's `event_id` when the `media_objects` row is alive (after "delete all recordings" or with voice storage off, the sentence is shown as text with no clip); *The tape* = `recording` events [P1]; *Out in the world* = `out_in_world` rows (below); *Kept words and marked moments* = `word_bank.kept` and `mark` events; *Hours* = `notebook_counts`; *Why this episode* = the pipeline's `episode_artifacts(kind='why')`; *How we know* = `claims` with `status in ('passed','shown')` and their `claim_evidence`. "See all my data" (PRD-v2 12.4) is the notebook plus the export; the beta has no separate in-app view of the nine stores [DECISION].

```sql
create table out_in_world (
  item_id uuid primary key,                        -- uuid5(learner_id, 'out_in_world', event_id, on_date || ':' || normalized text)
  learner_id uuid not null references learners(id) on delete cascade,
  text text not null, quote text, event_id uuid, on_date date not null, added_by text not null check (added_by in ('learner','salma')),
  lm_version integer not null
);
```

### 4.4 Lexicon and inventory tables (target-language package, loaded into Postgres)

Every table here is keyed by `lang` = the target language and is loaded from `packages/languages/<target>/` (ADR-02); the pilot loads `en`. Labels in the learner's native language are not columns: they live in `packages/native/<lang>/strings/` (`structures.yaml`, `categories.yaml`, `fact_types.yaml`) and the notebook resolves them at render time by `learners.native_language`, with `native/en` as the fallback. The target-language label (`label`) is the one column, because it is the same for every learner of that target.

```sql
create table lexicon_lemmas (
  lang text not null, lemma text not null, pos text, rank int not null, zipf real not null,
  is_function boolean not null default false, source text not null,   -- 'wordfreq-<lang>-3.x' in the beta; a subtitle list later
  primary key (lang, lemma)
);
create index lexicon_rank on lexicon_lemmas (lang, rank);

create table lexicon_chunks (
  lang text not null, chunk_id text not null, lemma_seq text[] not null, surface_example text not null, rank int,
  primary key (lang, chunk_id)
);

create table structures (
  structure_id text primary key,                   -- 'en:egp:past_simple_irregular_narrative' (prefixed by target language)
  lang text not null, label text not null,         -- label in the target language; native labels from packages/native/<lang>/strings/structures.yaml
  category text not null references reporting_categories(category),
  cefr_band text not null check (cefr_band in ('A1','A2','B1','B2','C1')),
  expected_from_scale real not null,               -- internal scale value from which the structure is "expected" (avoidance check)
  learnability text not null check (learnability in ('rule','item')),
  contrast_group text,                             -- 'past_vs_present_perfect'
  source_ref text, package_version text not null
);
create table reporting_categories (lang text not null, category text not null, label text not null, sort int not null, primary key (lang, category));
insert into reporting_categories values
 ('en','tense_aspect','verb tense and aspect',1), ('en','sv_agreement','subject-verb agreement',2), ('en','articles','articles',3),
 ('en','prepositions','prepositions',4), ('en','word_order','word order',5), ('en','word_choice','word choice',6),
 ('en','plurals','plurals',7), ('en','pronouns','pronouns',8), ('en','comparatives','comparatives',9),
 ('en','conditionals','conditionals',10), ('en','questions','question formation',11), ('en','register','register',12);
```

Loaders: `python -m forone.learner.lexicon_db load --lang en --version 2026.11.1` reads `packages/languages/en/lexicon/wordfreq.tsv`, `chunks.tsv`, `structures.yaml`, `categories.yaml` and upserts; the package version is recorded in `learner_model_versions.code_versions.package` as `languages/en@2026.11.1`. The structure inventory is the language gate's fifth check (ADR-03): a target opens only when its `structures.yaml` has passed. Size for English: about 60,000 lemmas, 300 to 400 chunks, 250 to 350 structures (PRD-v2 10.4 "a few hundred"). The word-check items (36 lemmas in six bands plus 12 pseudowords) and the then-and-now bank are package files, not tables.

### 4.5 Word probabilities and the review scheduler (code)

#### 4.5.1 Priors

For an unseen unit the prior is the pipeline's saturating curve (02-generation-pipeline.md 4.5), adopted here verbatim and owned here from now on: `p0 = prior.known_fraction + (1 - prior.known_fraction) * (1 - rank / size_est)` is not it; the shape is

```
p0 = clip(sigmoid((prior.center * size_est - rank) / (prior.width * size_est)), 0.02, 0.98)      # center 1.25, width 0.10
```

so a learner with `size_est = 3,000` sits at about 0.92 for rank 3,000 and 0.5 at rank 3,750, and a top-3,000 script clears the 95% audio floor the fitter checks. The first draft's `(size_est - rank) / (0.35 * size_est)` is gone: it gave 0.5 at rank 3,000 and about 0.73 at rank 2,000, which would have made the fitter reject every script the kit's coverage checker passes. The three keys `prior.known_fraction`, `prior.center`, `prior.width` (02 §9 item 3) are in 4.15; `known_fraction` is the floor the fitter uses for units below rank 500. The acceptance test is the week-1 one: `p_understood_many` over 10 kit scripts reproduces the kit's coverage checker within 0.5 points. `size_est` comes from the word check: `hits - false_alarms` per band maps to a families estimate by the package's band table; no word check or fewer than 12 answers gives the B1 default `prior.size_default = 3000` with `size_sd = 1200`. Chunks use the rank of their rarest content lemma plus 2,000. Stored as a Beta with concentration `prior.k = 4`: `a = p0 * 4`, `b = (1 - p0) * 4`, so two taps outweigh the prior and ten uneventful hearings are needed to move it far. The eye prior equals the ear prior plus `prior.eye_bonus` (0.05; reading is easier for the pilot's profile, PRD-v2 1.4, and the package may set it per target); the produced prior is `p0 * prior.prod_factor` (0.6).

#### 4.5.2 Evidence to Beta updates

This table is the Beta update, owned here. The FSRS grade per evidence kind is the assessment domain's mapping (05 4.5) and arrives as `AfterPassResult.fsrs_grades`; the last column shows it for reference only, so one document owns that number. Weak evidence (a hearing with no tap, an article scrolled past) is not a review at all in the beta: it moves the Beta and leaves the FSRS card alone, which is what the first draft's fractional weights approximated.

| Evidence (event or after-pass kind) | ear (Δa, Δb) | eye (Δa, Δb) | prod (Δa, Δb) | FSRS grade (05's mapping) |
|---|---|---|---|---|
| `tap` on transcript or Huh? sheet | (0, +2) | (0, +1) | | again |
| `tap` on article | (0, +1) | (0, +2) | | again |
| `huh` on a sentence containing the unit (per unit, diluted by units in sentence) | (0, +0.5) | | | hard |
| Heard in a completed episode (≥ 90% played), no tap | (+0.15, 0) | | | no review |
| Read in an article scrolled to the end, no tap | | (+0.15, 0) | | no review |
| Content uptake 2 on a call that reused the unit | (+0.5, 0) | | | no review |
| `word_uses` row: correct, prompted (recall gap completed, Salma gave it) | (+1, 0) | | (+1, 0) | good |
| `word_uses` row: correct, unprompted | (+2, 0) | (+1, 0) | (+2, 0) | easy |
| `word_uses` row: incorrect (word choice error on this unit) | | | (0, +1.5) | again |
| `talkback` asked for this unit | (0, +0.5) | | (0, +1) | again |
| `keep` | none | none | none | no review; `kept=true` and the unit is listed to the teacher in its own list (4.5.3) |

Ranges: `p_low, p_high` are the Beta 10% and 90% quantiles. Time: when `last_seen_at` is older than `scheduler.stale_days` (30), `p_understood` returns `mean * max(R(now), scheduler.stale_floor)` with R from the library, so a word unused for months is treated as shaky again (the personalization lens's rule) without a separate decay model.

#### 4.5.3 The scheduler

```python
# forone/learner/scheduler.py
from fsrs import Scheduler, Card, Rating, State       # py-fsrs, pinned in pyproject.toml (code_versions.scheduler = "py-fsrs==<pin>/default");
_s = Scheduler(desired_retention=0.85)               # library default parameters (FSRS-6) until we fit our own; PRD-v2 9.4: due below 0.85
GRADES = {"again": Rating.Again, "hard": Rating.Hard, "good": Rating.Good, "easy": Rating.Easy}   # 05's names

STRUCTURE_EARLY_CAP_DAYS = (1, 3)                    # grammar targets spaced tightly early (PRD-v2 9.4.3)

def review(card: Card, grade: str, at: datetime, is_structure: bool, reps: int) -> tuple[Card, int]:
    """One full review per grade the assessment domain sends; no fractional weights (D7)."""
    new, _log = _s.review_card(card, GRADES[grade], review_datetime=at)
    if is_structure and reps + 1 <= 3:
        lo, hi = STRUCTURE_EARLY_CAP_DAYS
        new.due = at + timedelta(days=min(max((new.due - at).days, lo), hi))
    return new, reps + 1

def retrievability(card: Card, at: datetime) -> float | None:
    """The library's own curve for the pinned release; None for a card never reviewed (not 0.0: a new card is not 'due')."""
    if card.last_review is None: return None
    return card.get_retrievability(at)

def due_list(conn, learner_id, at_drop: datetime) -> DueList:
    """due: reviewed cards (reps >= 1) whose predicted recall at the next drop is below 0.85, lowest first, at most 60.
    kept: every kept word (PRD-v2 9.5.4 'scheduled like targets'), never capped. active_targets: structure_map rows with
    target_lifecycle='active'. Heard-but-never-reviewed structures reach the teacher through structure_map.state and the
    avoidance flag, not through this list."""
    rows = conn.execute(text("""
      select 'word' as kind, unit_id as id, fsrs, reps, kept, status as st, false as active from word_bank where learner_id=:l and (reps >= 1 or kept)
      union all
      select 'structure', structure_id, fsrs, reps, false, state, target_lifecycle = 'active' from structure_map where learner_id=:l and (reps >= 1 or target_lifecycle = 'active')"""), {"l": learner_id})
    due, kept, active = [], [], []
    for r in rows:
        card = Card.from_dict(r.fsrs); R = retrievability(card, at_drop)
        item = DueItem(kind=r.kind, id=r.id, p_recall_at_drop=R, stability=card.stability, last_seen=card.last_review, kept=r.kept)
        if r.kept: kept.append(item)
        if r.active: active.append(item)
        if r.reps >= 1 and R is not None and R < _s.desired_retention: due.append(item)
    return DueList(due=sorted(due, key=lambda d: d.p_recall_at_drop)[:60], kept=kept, active_targets=active)
```

`Scheduler.next_interval` is not a public py-fsrs API and is not used; `Card.get_retrievability` and `Scheduler.review_card` are the whole surface this wrapper touches, so a library upgrade is a pin change plus a rebuild, not a curve rewrite. The due list is computed at brief-compile time, not by a cron: it depends on the next drop time, which `learner_schedule` knows, and on the day's plan: with `plan.episodes_per_day > 1` the teacher distributes the one list over the day's episodes (ADR-05), the list is not recomputed per episode. Own parameters: once 2,000 reviews per cohort (`cohort_key`, ADR-19) exist (about month 3), fit them on `events` with the optimizer in the same library and record them under `code_versions.scheduler` [P1].

#### 4.5.4 Words owned

A unit becomes `owned` when `produced_sessions` holds two distinct sessions whose `occurred_at` differ by at least 24 h, both unprompted and correct (PRD-v2 10.6). `owned_at` is the second session's time. This is the one word-level fact the claim gate may use without a standard error (PRD-v2 10.10 "words-owned claims").

### 4.6 Structure lifecycle (PRD-v2 10.5, 10.6, 10.7)

`state` moves on observations, `target_lifecycle` moves on the teacher's decisions and on confirmations; both are computed by `structures.step(map_row, observations, as_of)` after every pass (with `as_of = now()`) and on rebuild (with `as_of` = the replay cursor); every window below is `structure_acc(learner_id, structure_id, as_of, days)`.

| From | To | Rule (code) |
|---|---|---|
| `not_seen` | `heard` | `heard_n >= 1` (the publisher reports realized counts per structure from the fitter report; the pipeline domain sends them in `episode.ready.artifacts.realized_structures`) [ASSUMPTION] |
| `heard` | `attempting` | first observation with `obligatory = true` (correct or not) |
| `attempting` | `taking` | two observations `obligatory and correct and not prompted and clean` in two different sessions (PRD-v2 10.6 "in an obligatory context"), at least one of them ≥ 24 h after `last_targeted_session_id`'s time (or never targeted); `examples` are selected with the same predicate |
| `taking` | `stable` | over `structure_acc(learner, structure, as_of, 14)`: `contexts >= 5 and sessions >= 2 and correct / contexts >= 0.8` and `last_at - first_at >= 14 days`; sets `stable_at = as_of`, `recheck_due_at = stable_at + 14 days` |
| `stable` | `stable` (confirmed) | the assessment domain's recording rater reports the structure held in the next then-and-now recording: `stable_confirmed_at` set; `error_profile.status = 'resolved'` |
| `stable` | `attempting` | a re-check at 2, 4 or 8 weeks (`recheck_due_at`) finds `correct / contexts < 0.8` in `structure_acc(..., recheck_due_at, 14)` with `contexts >= 3`; `target_lifecycle = 'active'` again |
| any | `avoidance = true` [P1, with 05's avoidance cut] | once per 7 learner-local days (inside the first after-pass after `avoidance_checked_at + 7 days`; no calendar week, ADR-16): `expected_from_scale <= skills.speaking.mean` and `state in ('not_seen','heard')` and the learner has had ≥ 5 sessions; cleared on the first `attempting` |

`target_lifecycle`: `active` when the current `EpisodePlan.targets.grammar.structure_id` is this structure (the pipeline's publish step calls `stores.mark_targeted(learner_id, structure_id, session_id)`, which also increments `consecutive_targeted`, reset to 0 when a plan targets something else); `taking`, `stable`, `recheck` mirror `state`; `dropped_by_learner` on a veto. "Learned" for any claim text means `taking` or later, which by construction is "correct, unprompted, a day later, in a different session".

### 4.7 Life facts: the validator, the ladder and time

#### 4.7.1 The quote check

```python
# forone/learner/facts.py
def normalize(s: str, langs: tuple[str, ...]) -> str:
    """Lowercase, strip punctuation, collapse whitespace, then apply each language's normalizer from
    packages/native/<lang>/normalize.py and packages/languages/<lang>/normalize.py for the learner's pair (ADR-02).
    The Arabic one strips diacritics and folds أ/إ/آ→ا, ة→ه, ى→ي; the English one folds curly quotes and hyphens."""
    s = s.lower(); s = re.sub(r"[^\w\s]", " ", s)
    for lang in langs: s = NORMALIZERS[lang](s)
    return re.sub(r"\s+", " ", s).strip()

# Verbatim text only. A typed onboarding answer is verbatim by construction; a spoken one is quoted from its
# call_turn_verbatim (the worker uploads A3 audio and call/verbatim-turn runs on it), never from the streaming text.
# A small-door voice note is a call_turn_verbatim with mode='voice_note' (4.1.1), so it needs no type of its own.
QUOTE_SOURCES = ("call_turn_verbatim", "chat_message", "onboarding_answer")

def verify_quote_text(conn, learner_id, quote: str, quote_event_id: UUID) -> QuoteCheck:
    ev = conn.execute(text("select type, payload from events where learner_id=:l and event_id=:e"), {"l": learner_id, "e": quote_event_id}).one_or_none()
    if ev is None or ev.type not in QUOTE_SOURCES: return QuoteCheck(ok=False, reason="no_source_event")
    if ev.type == "chat_message" and ev.payload.get("speaker") != "learner": return QuoteCheck(ok=False, reason="not_learner_speech")
    if ev.type == "onboarding_answer" and ev.payload.get("answer_mode") != "text": return QuoteCheck(ok=False, reason="streaming_text_not_quotable")
    if ev.type == "call_turn_verbatim" and ev.payload.get("verbatim_status") == "disputed": return QuoteCheck(ok=False, reason="disputed_by_learner")
    langs = learner_langs(conn, learner_id)                       # (native_language, target_language)
    hay = normalize(ev.payload.get("text") or ev.payload.get("answer_text") or "", langs)
    q = normalize(quote, langs)
    ok = q in hay and len(q.split()) >= 2
    low_conf = ev.type == "call_turn_verbatim" and ev.payload.get("low_confidence_reason")
    return QuoteCheck(ok=ok and not low_conf, reason=None if ok else ("quote_not_in_transcript" if not low_conf else "low_confidence_region"))

def verify_quote(conn, fact_id: UUID) -> QuoteCheck:
    """The editor's check 4 form (02 calls it with a fact_id): looks up the row and delegates."""
    f = conn.execute(text("select learner_id, quote, quote_event_id from life_facts where fact_id=:f"), {"f": fact_id}).one_or_none()
    return QuoteCheck(ok=False, reason="no_fact") if f is None else verify_quote_text(conn, f.learner_id, f.quote, f.quote_event_id)
```

A candidate whose quote fails is dropped and counted (`facts.rejected_total` metric); the memory keeper never gets a second chance to "fix" the quote. A quote from a streaming `call_turn`, or from a spoken `onboarding_answer`'s recognizer text, is never accepted: only verbatim text, chat text and typed onboarding answers (PRD-v2 8.4.1); a voice answer at A3 is quoted from its `call_turn_verbatim`, and the card the learner confirmed on screen is the fallback with `confirmed_by='intake_card'` when the verbatim pass has not finished by the end of A3. The editor's check 4 (pipeline domain) calls `verify_quote(fact_id)`; the validator calls `verify_quote_text`.

#### 4.7.2 The confidence ladder

| Rung | Set when | May be spoken by a host or Salma? | Notebook shows |
|---|---|---|---|
| `heard_once` | Candidate passed the quote check, first time this fact (by `fact_type` + normalized `text` similarity ≥ 0.85, computed with `pg_trgm`) | No | "I think..." (the native package's phrase) with the quote and date |
| `usable` | (a) a second candidate matching the same fact arrives from a different `session_id` (`confirmed_by='repeated'`, `repeat_event_id` set); (b) Salma asked and the learner confirmed in the same session (`confirmed_by='asked'`, the analyst marks `confirmed_in_session`); (c) a `fact_card_viewed` for the one expanded card with `dwell_ms >= 4000` and no `fact_card_edit` for that fact in the same `visit_id` (`confirmed_by='viewed_unedited'`); (d) an intake card at A3 left standing when A3 ends (`confirmed_by='intake_card'`; PRD-v2 8.4.2: "left unedited on a card the learner viewed" is `usable`, not ground truth) | Yes | Plain |
| `ground_truth` | `fact_card_edit{action: edit|confirm}` (including ✎ on an A3 card) or `wrong_memory_flag` with a `learner_correction` | Yes | Plain, with "you edited this" |

Rule (c) has a defined trigger and a defined measurement. Measurement: the client (06) counts dwell only for the single expanded or focused card, only while it is in the centre band of the viewport, and sends one `fact_card_viewed` per card per visit when the card is collapsed or the visit ends; cards merely visible in the list accrue nothing, and a tab left open promotes nothing (section 9 item 5 states this requirement to 06). Trigger: the visit ends with a `notebook_visit_ended {visit_id}` marker in the same batch stream; when `api` appends the batch that carries it, `apply_learner_edit` promotes every fact of that visit that meets the rule, in the same transaction. No timer, and "the next after-pass" is not a fallback. Demotion never happens automatically; `fact_card_edit{remove}` sets `status='deleted'`, `dont_bring_up` sets the flag and keeps the fact (PRD-v2 12.3).

#### 4.7.3 Sensitivity

A candidate with `sensitivity` set (the memory keeper proposes the class; code also forces the class from `fact_shelf_life.sensitive_default`) is stored only if `confirmed_in_session = true`; otherwise it is discarded and only the transcript keeps it. A stored sensitive fact follows PRD-v2 8.4.3 strictly: it is used only in the session where the learner raised it, and never brought up first. In code: `facts_usable(learner_id, as_of, role, session_id)` returns a row with `sensitivity is not null` only for `role in ('chat_host', 'salma_explain')` and only when the caller's `session_id` equals the fact's `session_id`; the teacher, the writer, the host brief and the proof never receive it, so it can never seed an idea, a callback or an episode line. The first draft's week rule (usable for the rest of the learner's week, carried over from PRD-v2 5.1's rule for sensitive *topics* in episodes) is dropped as the default and recorded as the alternative in section 10 item 4, because it stretched a rule about topics to cover stored facts and watered down trust promise 6. The `sensitive_usable_until` column is removed. Where PRD-v2 5.1's topic rule needs "that week" (the writer may touch a sensitive *topic* the learner raised in `idea_chosen{source:'tell_salma'}`), the week is the rolling 7 learner-local days from the `idea_chosen` event (`occurred_at` in `learners.tz` + 6 days), the same window 02 already implements as `session_at >= as_of - 7 days`; no calendar week, no first day of the week, no country (ADR-02, ADR-16). Nothing in this domain ever sets a sensitivity class from inference: the class comes only with a quote.

#### 4.7.4 Time: shelf life, supersession, follow-ups

- `expires_at = valid_from + fact_shelf_life.shelf_days` unless the type has `null`. A dated plan (`dated_event_on` set) stays `active` until its follow-up is `used` or `expired` (21 days after the date), and only then moves to `dormant`; the first draft expired it the day after the event, which made the follow-up episode (`due_on = dated_event_on + 1`) impossible because the editor's check 4 would have failed the fact the same morning. `facts_usable` exposes `follow_up_due: bool` on such rows so the teacher can place the callback (PRD-v2 3.1.3, 8.4.5). The week-2 test plan has this case: a fact dated day D, the brief for D+1 carries it with `follow_up_due = true`, check 4 passes, and the fact is `dormant` on D+22 if never used. Expired facts are `status='dormant'`: kept, shown in the notebook under "earlier", never spoken.
- Supersession: a new candidate with the same `fact_type` and a `supersedes_hint` or the same `people.relation` (new job, moved city) sets the old row `status='superseded', superseded_by_fact_id=new` and the new row `supersedes_fact_id=old`; `facts_usable` exposes `history: [old.text]` so the writer can say "how's the new job?".
- Follow-ups: when a stored fact has `dated_event_on`, one `follow_ups` row is created with `due_on = dated_event_on + 1 day`; the teacher's `follow_ups_due` includes rows with `state='pending' and due_on <= next drop date`; the pipeline marks `used` with the episode id; `expired` after 21 days unused; `cancelled` if the fact is deleted.

#### 4.7.5 What "usable" means in one predicate

```sql
create function facts_usable(p_learner uuid, p_as_of date, p_role text, p_session uuid default null)
returns table (like life_facts, history_text text, follow_up_due boolean, may_initiate boolean)
language sql stable as $$
  select f.*,
         (select h.text_native from life_facts h where h.fact_id = f.supersedes_fact_id) as history_text,
         exists (select 1 from follow_ups u where u.fact_id = f.fact_id and u.state = 'pending' and u.due_on <= p_as_of) as follow_up_due,
         (f.sensitivity is null) as may_initiate
  from life_facts f
  where f.learner_id = p_learner
    and f.status = 'active' and f.confidence in ('usable','ground_truth') and f.dont_bring_up = false
    and (f.expires_at is null or f.expires_at >= p_as_of)
    and (f.sensitivity is null
         or (p_role in ('chat_host','salma_explain') and p_session is not null and f.session_id = p_session))   -- PRD-v2 8.4.3: same session only
$$;
```

The editor's check 4 is: every `fact_id` in the package's `facts_used` exists in `facts_usable(learner_id, publish_date, 'writer')` and `verify_quote(fact_id)` passes for each. The date is a parameter, not `current_date`, so a brief compiled for tomorrow's drop and a replayed rebuild both evaluate the right day.

#### 4.7.6 Interests decay

Salience is computed on read, never written back: `salience(at) = salience_base * exp(-(at - last_engaged_at) / interests.decay_tau_days)` with τ = 21 days, and `dormant(at) = salience(at) < interests.dormant_below` (0.2) is a predicate, not a column. The first draft multiplied the stored value by the full decay at every pass, so two passes a day apart compounded `exp(-10/21)` twice instead of `exp(-11/21)` once. Any `interest_signal` with `kind in ('mentioned','talked_long','chose')` sets `salience_base = min(1, salience(now) + strength)` and `last_engaged_at = now` (PRD-v2 8.4.6). `hard_dislike` and `no_go` never decay and are carried over in a rebuild.

#### 4.7.7 Corrections and learner edits (synchronous)

`apply_learner_edit` takes `versions.lock` first, then handles: `wrong_memory_flag` (sets the named fact `status='deleted'` if no correction, or `ground_truth` with the corrected text if `learner_correction` present; increments `learners.wrong_memory_n` for the 16.1 metric; when the flag disputes a quote, the assessment domain's `memory/correct` retracts the claims that cite it, 05 4.13); `fact_card_edit`; `fact_card_viewed` promotions at the visit's end marker (4.7.2); `notebook_edit`; `working_on_edit` (writes `error_profile.status='dropped_by_learner'` for a veto, or inserts a `working_on_additions` row `{text, voice_transcript, at}` that the teacher turns into structures in the nightly run; emits `working_on.changed`); `consent_change` (writes `consents`, below, and relays `learner.consent_changed`). Each bumps the version with cause `learner_edit`. Because the edit names a row id, and ids are deterministic (4.3), the same edit replays correctly after a rebuild.

```sql
create table consents (
  learner_id uuid primary key references learners(id) on delete cascade,
  voice_storage boolean not null default false, voice_storage_at timestamptz,
  data_use boolean not null default false, data_use_at timestamptz,
  drop_notification boolean not null default true, captions boolean not null default true,       -- no notes_mode: there are no notes (ADR-06)
  gap_note jsonb,                                   -- {enabled, days: 7|10|14, text}
  text_versions jsonb not null default '{}',        -- consent copy versions shown, per kind
  updated_at timestamptz not null default now()
);
create table working_on_additions (
  id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  text text not null, event_id uuid not null, state text not null default 'pending' check (state in ('pending','mapped','ignored')),
  mapped_to jsonb, created_at timestamptz not null default now()
);
```

The security domain owns the consent copy (per native language, from `packages/native/<lang>/consent/`, ADR-02 and ADR-20) and the semantics; this table is where the flags live and `media_objects.ephemeral` is derived from `consents.voice_storage` at call start (topology's `audio/expire`). `text_versions` records which native-language text version the learner saw, which is what a regime review (07 §4.9) asks for.

### 4.8 Show canon and the callback index

`show_canon` rows (4.3.9) are written from `AfterPassResult.canon` and from the publisher (the pipeline sends `canon_from_episode: [{kind:'position_host', who, text, episode_id}]` in `episode.ready.artifacts` [ASSUMPTION]). The writer's `SeriesBibleExcerpt` is compiled here: the pipeline's fiction tables (`side_characters`, `running_jokes`, `arcs`, `seasons`, last 5 `episodes`) joined with the last 30 canon rows and the top 10 by `topic_key` match to the idea.

**Beta callbacks (P0, no embeddings).** `search_callbacks(learner_id, query, k)` returns the top `k` of: `show_canon` rows ranked by `similarity(text, query)` (the `pg_trgm` GIN index in 4.3.9) and `topic_key` match to the idea, plus learner turns from `call_turns_v.text_verbatim` and `chat_message{speaker:learner}` ranked by trigram similarity, each as `{canon_id | event_id, text, spoken_at, score}`. Everything the first season can call back to was written to canon by the analyst, so this serves PRD-v2 2.3 and 8.6 without a second processor, an extension or a vector column. Callbacks the teacher proposes must cite a `canon_id` or an `event_id`; the pipeline's `callback.quote` is then checked with `verify_quote_text` against that event. 20 to 50 ms per query.

**Vector callbacks [P1].** When canon and trigram stop finding the callback (measured by 09's "callback accepted by the editor" rate), add `conversation_chunks`:

```sql
create extension if not exists vector;
create table conversation_chunks (
  chunk_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  source text not null check (source in ('call','chat','small_door','onboarding')),
  session_id uuid, call_id uuid, thread_id uuid, first_event_id uuid not null, last_event_id uuid not null,
  spoken_at timestamptz not null, text text not null,               -- about 3 learner turns + the host turn before them, 60 to 120 words, built from
                                                                    -- call_turn_verbatim and chat_message text ONLY (never the streaming text), so a
                                                                    -- callback quote can be checked against first_event_id..last_event_id
  embedding vector not null, embed_model text not null,             -- no typmod: the dimension follows the vendor; Google's embedding model (ADR-10)
  lm_version integer not null
);
create index chunks_learner_time on conversation_chunks (learner_id, spoken_at desc);
-- no ANN index at first (D11): exact search per learner, 20 to 50 ms at 2,000 chunks (not "5 ms"); a partial HNSW index per learner
-- when a learner passes callbacks.exact_search_max_chunks = 5000
```

```python
def search_chunks(conn, learner_id, query, k=5):                   # P1
    q = embed([query])[0]                                          # Google embedding, the existing processor row (ADR-10)
    return conn.execute(text("""select chunk_id, session_id, spoken_at, text, 1 - (embedding <=> :q) as score
                                from conversation_chunks where learner_id=:l order by embedding <=> :q limit :k"""),
                        {"l": learner_id, "q": q, "k": k}).all()
```

Chunks are embedded in the after-pass (one call per session, about 10 chunks, under $0.0005, inside the pipeline's cost line). Chunk text is verbatim text and lives for the account's life regardless of voice storage, like the transcript it is cut from; it is deleted with the learner.

### 4.9 Compiled briefs

`briefs.compile(role, learner_id, scope, as_of)` computes on read; there is no `briefs` table (D12). The first draft's cache keyed by `learner_model_version` would have hit a handful of times a week (the version bumps after every pass and every edit, and each role compiles once per artifact) and would have served date-dependent tails stale (an expired fact, a follow-up that became due overnight). The consumer stores the body it used with the artifact it fed: the pipeline's `episode_artifacts(kind='teacher_input'|'call_brief')` and `brief_ref`, the call bundle in `calls`, the `proofs` row; that is the audit trail, and `learner_model_version` is in every body. The stable part of every brief is ordered first, sorted deterministically, for the vendor's prompt cache.

| Role | Body (PRD-v2 8.6) | Size budget | Stable prefix (cached by the prompt cache) | Volatile tail |
|---|---|---|---|---|
| `teacher` | The pipeline's `TeacherInput` exactly (02-generation-pipeline.md 4.3), compiled here from the map below; one brief for the day's 1 to 3 episodes (ADR-05) | ≤ 12,000 tokens | `profile`, `skills`, `structure_map` (sorted by `structure_id`), `word_bank_summary`, `bible` | `due_list`, `last_14_days`, `facts_usable`, `follow_ups_due`, `energy`, `claims_passed`, `working_on`, `plan` |
| `writer` | Supplied to the pipeline as `WriterBriefInputs`: `facts_allowed` (≤ 2 from `facts_usable(..., 'writer')`, never sensitive, each with quote, event id, `history_text`, `follow_up_due`), `SeriesBibleExcerpt`, `callback` candidates (top 3 from `search_callbacks`), `learner_own_words` (last call's 2 best clean turns from `call_turns_v`), name and pronunciation | ≤ 3,000 tokens | bible excerpt | facts, callbacks, own words |
| `host` | `HostLearnerSlice`: `name`, `name_pronunciation`, `pause_profile.eot_silence_ms`, `anxiety_flag` (from the last pass), `last_call_abandoned`, `callback` (one, with quote), `produced_words` (lemmas with `produced_unprompted_n > 0`), `transcript_default`, `recasts` (the teacher's echo plan: which recurring errors to recast this call, ADR-06, the only correction channel); the pipeline merges it with `episode_artifacts(call_brief)` into the one page | ≤ 600 tokens | everything except `anxiety_flag` and `callback` | those two |
| `salma_talkback` | `produced_words: {lemma: {last_session_date, example_sentence}}` for word-or-hint (PRD-v2 5.4.5), ≤ 400 lemmas, in `native_language` | ≤ 1,500 tokens | all | none |
| `salma_explain` | For "why do we say it like that?" when the learner asks (decisions.md §3, ADR-06): the sentence asked about, the structure's `label` and the native label, the learner's own correct `examples` for it, `facts_usable(..., 'salma_explain', session_id)`; never a target list, never a note | ≤ 1,500 tokens | labels | the asked sentence |
| `chat_host` | Call summary (assessment domain writes it into `episode_artifacts(kind='call_summary')`), the opener artifact, `recasts`, `facts_usable(..., 'chat_host', session_id)` | ≤ 1,200 tokens | opener | summary, facts |
| `proof` | `passed_claims(learner_id, week)` with `claim_evidence` refs and the rows with `notice_pending = true`; `working_on` items; `notebook_counts`; `sessions_in_week` computed from `events` (never stored, ADR-19); nothing else (PRD-v2 8.6) | ≤ 2,000 tokens | none | all |
| `return_win` | One claim from `passed_claims` of kind `first_ever` or `word_owned` for the return episode (PRD-v2 3.8.2) | ≤ 200 tokens | | |
| `finale` | `finale_differences()` (05) plus the season's canon rows and `out_in_world` | ≤ 2,000 tokens | canon | claims |

The `teacher` body, field by field, so a developer can write `compile('teacher')` from this document (02 4.3 lists the fields; 05 writes two of the sources):

| `TeacherInput` field | Source here | Note |
|---|---|---|
| `profile` (`name`, `native_language`, `target_language`, `tz`, `plan.episodes_per_day`, `onboarding_session_id`, `band`) | `learners` (topology), `sessions where kind='onboarding'` (first row), `skills.listening.mean` to band via `skills.scale_anchors` | `onboarding_session_id` is the session that holds A1 to A10 |
| `skills` | `skills` row, means and sds, `calibrated` | never a CEFR word |
| `structure_map` | `structure_map` joined with `structure_acc(..., as_of, 14)` and `error_profile` | sorted by `structure_id` |
| `word_bank_summary` | counts by `status`, `owned` in the last 14 days, `kept` list | |
| `due_list` | `scheduler.due_list(learner_id, next_drop_at)` (`due`, `kept`, `active_targets`) | `next_drop_at` from `learner_schedule` |
| `interests[]` with `entities`, `salience` | `interests`, salience computed at `as_of` (4.7.6), `dormant = false`, `no_go = false` | `hard_dislike` rows are passed as `avoid[]` |
| `facts_usable[]` with `entities`, `session_at`, `history_text`, `follow_up_due` | `facts_usable(learner_id, as_of::date, 'teacher')` | sensitive rows never |
| `follow_ups_due[]` | `follow_ups where state='pending' and due_on <= next drop date` | |
| `last_14_days[]` | the assessment domain's `session_summaries` (05 4.16): `local_date, uptake, energy_signals, talk_share, abandoned, errors_per_100` | 05 writes it in `finish` |
| `energy` | the last `session_summaries` row's `energy_signals` plus `AfterPassResult.low_energy_signals` of the last pass | |
| `claims_passed[]` | `claims where status in ('passed','shown')`, last 28 days | |
| `working_on[]` | `working_on_items` view plus `working_on_additions where state='pending'` | |
| `taste` (`format_completion`, `host_completion`, `swap_count_30d`, `length_pref_min`) | `taste` row; `swap_count_30d = count(*) from events where type='swap' and occurred_at > as_of - 30 days` | computed, not stored |
| `bible` | `series_bible_excerpt(learner_id)` (4.8) | |
| `plan` (`episodes_per_day`, `episodes_today`, `extras_last_7_days`) | `learners.plan` → `plans.yaml`; `episodes` rows for the local day; `episode_next_requested` events in 7 days | ADR-04, ADR-05 |

Measured target: teacher compile under 500 ms (twelve indexed queries and one JSON build); the pipeline's assumption of 5 s holds with margin. The `host` and `salma_talkback` bodies are compiled at episode time by the pipeline's call-brief step and again at call start by `api` for `GET /internal/calls/{id}/brief` if the version moved (a learner edit between episode time and the call must reach the host).

### 4.10 Claims (written by the claim gate; read by the proof, the "New for you" card, the return episode, the finale)

One table, the assessment domain's DDL (05 4.16) so two domains do not ship two tables named `claims`; it lives here because it is learner data under RLS and the purge. The first draft's `claim_invalidations` is gone: retraction is a status with a reason and a notice flag, which also covers `memory/correct`'s `retracted(learner_disputed)`.

```sql
create table claims (
  id uuid primary key default gen_random_uuid(), learner_id uuid not null references learners(id) on delete cascade,
  kind text not null check (kind in ('did_it','first_ever','word_owned','mistake_gone','fluency_change','complexity_change','accuracy_change',
                                     'accuracy_fell_while_trying','talkback_falling','then_and_now','count_corrected')),
  metric text, task_type text, direction text check (direction in ('better','worse','event')),
  subject jsonb not null,                   -- {structure_id} | {lemma} | {can_do_id} | {category} | {count: 'words_owned'|'hours_heard'|'hours_spoken', from, to}
  before_value numeric, after_value numeric, before_points jsonb, after_points jsonb, sem_used numeric, threshold_used numeric,
  before_window daterange, after_window daterange, attempts_before int, attempts_after int, reason text,   -- for worse: trying|harder_task|long_gap|unknown
  text_native text not null,                -- rendered from the kind's template by code in learners.native_language; the only sentence any surface may speak
  status text not null default 'candidate' check (status in ('candidate','passed','failed','shown','retracted')),
  failed_rule text, retracted_reason text, notice_pending boolean not null default false,
  shown_at timestamptz, shown_surface text, shown_event_id uuid, created_at timestamptz not null default now(),
  assessment_version text not null, rater_version_id uuid, learner_model_version integer not null,
  gate jsonb not null default '{}'          -- {like_for_like, beyond_noise, repeated, clean, openable, se_used}
);
create index claims_learner_status on claims (learner_id, status, created_at desc);
create table claim_evidence (               -- 05's; rule 5 "openable": every row points at an event, observation, word_use or recording
  claim_id uuid references claims(id) on delete cascade, ord smallint,
  type text not null check (type in ('event','observation','word_use','recording','word')), ref uuid not null, label text,
  primary key (claim_id, ord)
);

-- this domain's guarantee: a shown claim may change only to retracted and is never deleted (PRD-v2 8.5)
create or replace function claims_shown_guard() returns trigger language plpgsql as $$
begin
  if tg_op = 'DELETE' and old.shown_at is not null and current_setting('forone.purge_mode', true) is distinct from 'on' then
    raise exception 'a shown claim is never deleted';
  end if;
  if tg_op = 'UPDATE' and old.shown_at is not null and new.status not in ('shown','retracted') then
    raise exception 'a shown claim may only be retracted';
  end if;
  if tg_op = 'UPDATE' and old.status = 'shown' and new.status = 'retracted' then new.notice_pending := true; end if;
  return case when tg_op = 'DELETE' then old else new end;
end $$;
create trigger claims_shown_guard before update or delete on claims for each row execute function claims_shown_guard();

create table rebuild_runs (                 -- written by assessment/rebuild through the library (D14)
  rebuild_run_id uuid primary key, learner_id uuid not null, reason text not null, kind text not null check (kind in ('code','model')),
  from_version integer not null, to_version integer, code_versions jsonb not null,
  started_at timestamptz not null default now(), finished_at timestamptz, sessions_replayed int, vendor_cost_usd numeric(8,4) not null default 0,
  diff jsonb, status text not null default 'running'
);
```

Lifecycle (05 4.8.3): `candidate → passed | failed(failed_rule)`; `passed → shown` when any surface emits `claim_shown {claim_id, surface}` (`mark_claim_shown` sets `shown_at` once and is idempotent); `passed | shown → retracted(reason)` only by `assessment/rebuild` or `memory/correct`; a `shown` claim that is retracted gets `notice_pending = true` and the next proof carries one honest line. `failed` candidates are kept 90 days for the audit, then purged by `retention/daily`. The gate logic (the five rules, the standard errors) is the assessment domain's; this domain guarantees that nothing reaches the proof producer except rows with `status in ('passed','shown')`, and that the trigger above holds. `count_corrected` is this domain's one kind: written by the counts writer when a rebuild lowers a `notebook_counts` value (4.3.9), it goes straight to `passed` with `notice_pending = true` and is never spoken as progress.

### 4.11 Object storage layout

This document owns the key layout (D15); 01, 02, 03 and 06 adopt it (section 9 names what each had). Three buckets from the topology (`forone-media`, `forone-voice`, `forone-exports`), every kept learner object under `learners/{lid}/`, every ephemeral learner object under the bucket-root prefix `ephemeral/learners/{lid}/`, indexed in `media_objects` with `encryption` set by kind (ADR-12): learner-voice kinds (`call_turn`, `call_full`, `recording`, `voice_note`, `say_it_once`, `shadow`, `clip`, `name_clip`) are `sse_c_learner` (SSE-C under the learner's DEK, or the per-call key `HKDF(DEK, 'call:' || call_id)` recorded in `media_objects.key_derivation`, 01 D7); produced show kinds (`episode_segment`, `episode_full`, `episode_feed`, `read_aloud`, `recap`, `feed_tag`, `proof`, `mark_cut`) are `sse_kms_env` (SSE-KMS under the environment key, served by 10-minute presigned URLs from `api`'s media route). The file names for show audio are the pipeline's (02 4.x: `episode.m4a`, `episode_feed.m4a`, `episode_feed.mp3`, `scene_{n}.m4a`), so the publisher, the feed (06 serves `episode_feed.mp3`) and this index agree. [DECISION] Keys:

```
forone-media/learners/{lid}/episodes/{episode_id}/scene-{n}.m4a         produced show audio, per scene, kept 24 h after the full file exists (02)
forone-media/learners/{lid}/episodes/{episode_id}/episode.m4a           stitched, app
forone-media/learners/{lid}/episodes/{episode_id}/episode_feed.m4a      stitched + Salma's 5 s tag (feed)
forone-media/learners/{lid}/episodes/{episode_id}/episode_feed.mp3      same, mp3 for podcast apps (06 D5)
forone-media/learners/{lid}/episodes/{episode_id}/article.m4a           read-aloud
forone-media/learners/{lid}/episodes/{episode_id}/recap.m4a             small door
forone-media/learners/{lid}/episodes/{episode_id}/timings.json          word timings, all scenes
forone-media/learners/{lid}/episodes/{episode_id}/glosses.json          the WordIndex (pipeline 4.10)
forone-media/learners/{lid}/episodes/{episode_id}/package.json          script, article, call brief, opener, recap text, shadow lines, why
forone-media/learners/{lid}/proof/{proof_id}/{scene-n|proof}.m4a
forone-media/learners/{lid}/marks/{event_id}.m4a                        a marked moment's cut (show audio, not learner voice; sse_kms_env)
                                                                        (episode_kind = daily_extra shares the layout; the kind is in episodes, not the key)

forone-voice/learners/{lid}/calls/{call_id}/turn-{n}.ogg                learner turns (opus), storage on; key_derivation = 'call:{call_id}'
forone-voice/learners/{lid}/calls/{call_id}/full.m4a                    mixed call, only when storage on
forone-voice/learners/{lid}/recordings/{recording_id}/{retell|opinion|repeat-k}.ogg   then-and-now; storage on, or kept_explicitly
forone-voice/learners/{lid}/say-it-once/{episode_id}/{line_id}.ogg
forone-voice/learners/{lid}/shadow/{episode_id}/{line_id}.ogg
forone-voice/learners/{lid}/voicenotes/{call_id}/{n}.ogg
forone-voice/learners/{lid}/clips/{claim_id}-{then|now}.ogg             cuts for "how we know"
forone-voice/learners/{lid}/name/clip.ogg                               the learner's own name, ≤ 30 s: a learner-voice kind like the others (4.14)

forone-voice/ephemeral/learners/{lid}/<the same seven kinds and paths>  every learner-voice kind when consents.voice_storage = false (and the name
                                                                        clip, recordings not kept_explicitly); ONE lifecycle rule on prefix 'ephemeral/':
                                                                        expire after 1 day, the backstop to audio/expire's 15 minutes

forone-exports/learners/{lid}/{export_id}.zip                           SSE-KMS service key; served through GET /v1/exports/{id} (4.12.1); deleted after 14 days
```

Why `ephemeral/` is first: an S3 lifecycle rule filters by a literal key prefix or by object tags, never by a segment in the middle of a key, so `{lid}/ephemeral/...` would have needed one rule per learner against a 1,000-rule limit; with the segment at the root, one rule covers every learner and every kind, and per-learner listing for export and purge uses two prefixes (`learners/{lid}/` and `ephemeral/learners/{lid}/`; 4.12.2 step 3 says so). The ephemeral objects are also tagged `ephemeral=true` on PUT so a tag-filtered rule can replace the prefix rule without a key change.

Sample episodes (no learner) live at `forone-media/samples/{sample_id}/...` under the service key and expire after 30 days. Bucket settings [DECISION]: versioning **on** for `forone-voice` and `forone-media` with a noncurrent-version expiry of 7 days on the `learners/` prefixes, so a bug in `audio/expire`, the ephemeral logic or the purge cannot erase a learner's paid-for recording irreversibly (PRD-v2 12.5.1 keeps consented audio "until the learner deletes it"; the 15-minute rule never applied to kept objects); versioning is not applied to `ephemeral/` (the lifecycle rule expires current versions, and `audio/expire` deletes them outright; there are no noncurrent versions to keep), and `learner/delete`, `learner/purge-audio` and consent revocation delete **all versions** explicitly (one `ListObjectVersions` per prefix) so the 24-hour and 30-day promises still hold; public access blocked everywhere; the voice bucket has the single lifecycle rule above; object lock is not used.

### 4.12 Export, deletion and retention (PRD-v2 12.5)

#### 4.12.1 Export (`learner/export`, link within 1 h)

Available to a learner in `status in ('active','trial_ended','paused')`; only `deleting` returns 410 (PRD-v2 12.5.9: export and delete stay available for the 90 days after a trial ends). Steps, each an Inngest step: (1) `snapshot`: record `lm_version` and `max(seq)`; (2) `tables`: stream the nine stores plus `word_uses`, `structure_observations`, `claims` and `claim_evidence`, `consents`, `out_in_world`, `notebook_counts`, `learner_model_versions`, `learner_schedule`, `episodes` metadata into `learner_model.json` (one object keyed by table, plain JSON, field names as in the DDL, ISO dates); (3) `events`: `events.ndjson` for the learner in `(coalesce(effective_at, occurred_at), seq)` order, `after_pass_result` rows included; (4) `transcripts`: one `transcripts/{local_date}-{kind}.json` per call and chat thread from `call_turns_v` and `chat_message`, plus a `.txt` rendering [P1 if one engineer]; (5) `audio`: every `media_objects` row of the learner with `deleted_at is null and ephemeral = false` in the learner-voice kinds (`call_turn, call_full, recording, voice_note, say_it_once, shadow, clip, name_clip`) decrypted with the DEK, or with `HKDF(DEK, key_derivation)` when `media_objects.key_derivation` is set (every call turn; 01 D7), and written into the zip; `keys.get_dek` is never cached for `purpose = 'export'` (ADR-18) and the read is one `audit_log` row; show audio is not included by default (02's rule: it is the show's rendering, not the learner's recording; 02 §10 item 12 lets Muath include it), the text artifacts of every episode are (02 supplies them); (6) `zip`: a plain zip (`zipfile`, deflate); no passphrase and no AES (D16); (7) `upload` to `forone-exports/learners/{lid}/{export_id}.zip` under the service key; (8) `email` kind `export_ready` with a link to `GET /v1/exports/{export_id}` via the topology's `Email` adapter: the route requires the learner's session, checks `exports.learner_id`, and redirects to a 15-minute presigned URL signed at click time (a 7-day presigned URL cannot exist under `workflows`' Fargate task role: it dies with the temporary credentials); (9) `export.ready` event. A 100-session learner with voice storage on is about 1.5 GB; step 5 streams and the total runs in 5 to 15 minutes. The zip is tested in week 3 to open in iOS Files, Android Files, macOS Archive Utility and Windows Explorer with no extra app.

```sql
create table exports (
  export_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  requested_at timestamptz not null default now(), ready_at timestamptz, available_until timestamptz,   -- ready_at + export.keep_days
  bytes bigint, lm_version integer, high_water_seq bigint, downloads int not null default 0, last_downloaded_at timestamptz, deleted_at timestamptz
);
```

#### 4.12.2 Deletion (`learner/delete`; access at once, live purge within 24 h, backups 30 days)

1. `revoke` (synchronous in `api` before the function starts): `learners.status='deleting'`, `deletion_requested_at=now()`, all auth sessions and `feed_tokens` revoked, web push subscriptions removed, LiveKit rooms for the learner closed; `api` sends the email kind `deletion_started` ("we started; everything is gone from live systems within 24 hours and from backups within 30 days") synchronously from the request, so no email address passes through Inngest (01: Inngest holds ids and timestamps only). From this moment every request with a revoked session returns 410 and `POST /v1/events` appends nothing; the call-worker's spool for a `deleting` learner is discarded by `api`'s spool ingester; an offline-queue replay that arrives later meets the same 410 and the PWA drops its queue on it.
2. `cancel`: Inngest `cancelOn learner.deletion_requested` stops `day/next`, `episode/produce`, `session/after-pass`, `gap/note`, `proof/make`, `assessment/rebuild` for the learner (topology).
3. `objects`: delete every `media_objects` row's S3 object **and every noncurrent version** (all three buckets, including exports; `ListObjectVersions` then `DeleteObjects`, 1,000 keys per request), show kinds by prefix (`forone-media/learners/{lid}/`, ADR-12), then mark `deleted_at`; verify with a listing of both prefixes in each bucket (`learners/{lid}/` and `ephemeral/learners/{lid}/`, versions included), which must be empty.
4. `research`: delete `research_transcripts where pseudonym = (select pseudonym from research_pseudonyms where learner_id = :l)` and then the `research_pseudonyms` row (ADR-09, D18); ask Langfuse to delete traces for that pseudonym (its deletion API); the request is logged in the ledger and does **not** hold up step 7 (ADR-09 closes the question the first draft left open).
5. `rows`: as `forone_purge` (`bypassrls`, D17) with `set local forone.purge_mode='on'`: the purge order is not a hand-written list. `forone.learner.deletion.plan()` reads `information_schema.columns` for every table with a `learner_id` column, orders them by foreign-key dependency computed at run time from `pg_constraint`, and classifies each against the allow-list in `forone.learner.pii`: **delete** (the default: the nine stores, `word_uses`, `structure_observations`, `claims`, `claim_evidence`, `consents`, `exports`, `learner_model_versions`, `rebuild_runs`, `working_on_additions`, `event_ids`, `events` in every partition, the topology's `doors`, `sessions`, `calls`, `feed_items`, `feed_tokens`, `push_subscriptions`, `episodes`, `episode_artifacts`, `learner_schedule`, `media_objects`, `model_io`, `otp_codes`, `accounts`, chat threads, `waitlist` and `invites` rows, 02's fiction and pipeline tables, 05's `session_summaries`, `recordings`, `recording_ratings`, `proofs`, 07's `subscriptions` and `payment_events` after the aggregate below); **de-identify** (keep a row with `learner_id` replaced by the research pseudonym or null): `deletion_ledger`, cost aggregates (`vendor_calls` and `learner_spend_daily` summed into `cost_aggregates` first, then deleted), `audit_log` (the actor and purpose, no content), `review_items`/`review_findings` (02's rule), and `crisis_log` **pseudonymized** pending the ruling in section 10 item 6 (PRD-v2 7.9.4 says every activation is logged for annual reporting, so deleting it may be wrong); **shared, untouched**: tables without `learner_id`. A CI test fails when a table with a `learner_id` column is in neither list, so a new table cannot slip past the purge. Every `delete` asserts `rowcount >= expected` where rows are expected (expected from a count taken under the same role before the deletes) and records `{table: rows_deleted}` in `deletion_ledger.rows_deleted`; a zero where rows were expected fails the step, which is how an RLS or grant mistake surfaces instead of reporting success over intact data.
6. `key`: set `learner_keys.destroyed_at`, bump `key_version` so every cached DEK misses (ADR-18), then delete the row (crypto-shred; any object the listing missed is unreadable).
7. `ledger`: re-run the step-5 plan once more as a final sweep (rows that landed between the first sweep and the key step, for example a late `after_pass_result` from a pass that was cancelled mid-flight), insert `deletion_ledger {email_hmac, requested_at, live_purged_at=now(), backups_expire_at = live_purged_at + 30 days, rows_deleted, objects_deleted, verified_empty}`; delete the `learners` row last; send the email kind `account_deleted` from a step whose input is only a one-time token that `api`'s mailer resolves to the address captured at step 1 and then forgets (no address in Inngest, D17).
8. `external`: Sentry events are scrubbed of learner ids at emission (nothing to delete); Langfuse was asked at step 4; the payment processor's customer is deleted through the `Payments` adapter (07).

```sql
create table deletion_ledger (
  id bigserial primary key, email_hmac text not null,          -- hmac_sha256(server key, lower(email)): lookup-able for the 30-day re-signup audit; D17
  requested_at timestamptz not null, live_purged_at timestamptz not null, backups_expire_at timestamptz not null,
  sessions_count int, rows_deleted jsonb not null, objects_deleted int not null, versions_deleted int not null,
  verified_empty boolean not null default false, langfuse_requested_at timestamptz
);
```

The per-learner "delete all recordings" control (PRD-v2 12.4) is a flow of its own, distinct from revoking voice-storage consent: `learner/purge-audio` (07's function; this domain's object step) deletes every `media_objects` row of the learner in the learner-voice kinds including `kept_explicitly` recordings and the name clip, all versions, within 24 hours, and leaves consent as it was; the notebook's "Words you own" clips then fall back to the sentence as text (4.3.9), the claims that cited a clip keep their text evidence (`claim_evidence.type = 'word_use'`), and the "then" recording for the finale is gone, which the finale says plainly (`no_recording = true`).

Backups: RDS automated backups with 30-day retention and PITR; snapshots are not scrubbed. The privacy text says "within 30 days" and that is what the retention makes true. Manual snapshots are forbidden by policy (a manual snapshot never expires); the restore drill in week 5 uses PITR.

#### 4.12.3 Retention jobs (data parts of `retention/daily`)

| Rule | Query or action |
|---|---|
| Trial ended, 90 days (12.5.9) | `learners where status='trial_ended' and trial_ended_at < now() - 83 days and warned_at is null` → email `trial_deleting_soon`; `... < now() - 90 days and warned_at is not null` → send `learner.deletion_requested`; export and delete stay available throughout |
| Audio when storage off (12.5.2) | `media_objects where ephemeral and expires_at < now() and deleted_at is null` → delete, alert if any older than 15 min; also the `ephemeral/` lifecycle rule as the backstop |
| Audio after revoke (12.5.3) | `consents.voice_storage=false and voice_storage_at < now() - 24h` and any learner-voice object (the name clip included) alive → alert (the purge function should have done it) |
| Partitions | create `events_{yyyy_mm}` three months ahead; alert if `events_default` holds a row |
| Exports | delete zips (all versions) and rows 14 days after `ready_at` |
| Failed claims | `claims where status='failed' and created_at < now() - 90 days` → delete (05's audit window) |
| Orphans | `media_objects` rows whose S3 object is gone, and S3 objects without a row (sampled listing of both prefixes for 20 learners a day) |
| Research set [P1] | rows whose learner has `data_use=false` → delete (should be empty) |

`retention/daily` runs per learner-local midnight (ADR-16: hourly, over the learners whose local day just closed), so "83 days" and "90 days" are learner-local days and no job is pinned to one timezone.

#### 4.12.4 The opt-in research set

[P1] for the beta: the consent switch exists and writes nothing until the set is built (the skeptic's cut, accepted; 07 approves the consent copy first).

```sql
create table research_pseudonyms (                  -- ADR-09: one random pseudonym per learner; also Langfuse's user_id; deleted with the learner
  learner_id uuid primary key references learners(id) on delete cascade, pseudonym text not null unique, created_at timestamptz not null default now()
);
create table research_transcripts (
  id uuid primary key, pseudonym text not null,       -- research_pseudonyms.pseudonym; no learner_id column
  kind text not null check (kind in ('call','chat')), local_date date not null, turns jsonb not null,  -- learner and host text only, after redaction
  cohort_key date not null,                           -- = invite_date (ADR-19), the only grouping the research set carries
  analyst_tags jsonb, package_version text not null, native_language text not null, target_language text not null,
  created_at timestamptz not null default now()
);
```

Populated by the after-pass only when `consents.data_use = true` at pass time. Redaction, in order: the learner's display name and the names in `life_facts.people` → `{NAME}`; every entity in the analyst's entity list for the session (02's allowed-entity set: employers, cities, teams, products) → `{ENTITY:kind}`; every turn whose text contains the quote of a confirmed sensitive fact (`life_facts.sensitivity is not null`) → dropped whole; dates → `{DATE}`. The result is **pseudonymized, not anonymized**: the learner's phrasing and the pseudonym remain, re-linkable through `research_pseudonyms` until the learner deletes. The consent copy says "pseudonymized" (07 confirms the word; PRD-v2 12.5.5's "anonymized" is corrected in PRD-v3). No audio, ever. Deleted on revoke and on account deletion (D18); 10-decision-records §10 #15 records the answer on keeping rows after deletion: deleted.

### 4.13 Migrations, roles, RLS and backups

- **Postgres version:** 16, stated once here: RDS for PostgreSQL 16 (01 §1 row 6) and `pgvector/pgvector:pg16` in compose. Every DDL in this document runs on 16 (no identity column on the partitioned table, 4.1.2); moving to 17 is a deliberate change, not a side effect.
- **Migrations:** Alembic in `packages/core/migrations`, one revision per PR, forward-only in production, every revision has a `downgrade` that is tested in CI against a fresh database. Alembic runs as `forone_owner`, the table owner, which bypasses RLS by definition and is therefore never used at runtime (no application config holds its password; the `events` trigger fires for it too, and `forone.purge_mode` is the only door). Migration policy for the stores: an **additive** change (a new nullable column, a new index, a new table) is a migration and nothing else; a change that alters what the writers compute (a new column that must be back-filled from the log, a renamed enum, a changed window) bumps the relevant `code_versions` key and is a **code-version rebuild** (D14: stored results replayed, no vendor call, 2 s a session); only a change to the analyst or the memory keeper is a model-version rebuild. Adding a column to `word_bank` for 10,000 learners therefore never costs a Haiku call. Partition creation is not a migration (it is `retention/daily`).
- **Roles (ADR-17):** `forone_owner` (migrations only), `forone_app` (api: insert on `events` and `event_ids`, select on stores, update on the learner-edit tables, RLS enforced through `forone.learner_id`), `forone_workflows` (select and write on everything except update/delete on `events`; the service policy), `forone_purge` (`bypassrls`; delete on everything; used only inside `learner/delete` and `learner/purge-audio`, which set `forone.purge_mode`), `forone_admin` (the `/admin` pages: aggregate reads across learners through views, writes only to the admin tables, every content read in `audit_log`), `forone_human` (psql sessions; `pgaudit` logs every statement of this role and only this role), `forone_readonly` (dashboards; aggregate views, no `pgaudit`). No role has `superuser`.
- **RLS:** every table with `learner_id` has the two policies from 4.1.2, `nullif`-guarded. `api` sets `set local forone.learner_id = '...'` at the start of every request transaction from the session cookie; a missing or empty setting yields zero rows, never all rows and never a cast error. **Pooling:** `set local` lives for the transaction, so every learner-scoped read in `api` runs inside the request transaction; `api` connects through RDS Proxy in session-pinning mode (or SQLAlchemy's own pool, no transaction-mode pgbouncer), and a CI test asserts that no code path issues an autocommit read of a learner table, because under transaction pooling such a read silently returns zero rows.
- **Backups:** RDS automated, 30-day retention, PITR; a quarterly restore drill, first one in build week 5. The weekly `pg_dump --schema-only` drift check is cut for the beta (Alembic's `check` in CI covers drift). S3: no replication in the beta (one region, `HOME_REGION = eu-central-1` by default with `me-central-1` as the alternative, ADR-08; counsel's regime review per ADR-20); the voice bucket's lifecycle rule is the only automatic deletion.
- **Observability of the data layer:** the cost domain's `vendor_calls` is not here; this domain emits metrics `events_appended_total{type,source}`, `events_duplicates_total`, `events_rejected_total{reason}` (schema, source mismatch, age), `facts_rejected_total{reason}`, `lm_bump_total{cause}`, `lm_lock_wait_ms`, `brief_compile_ms{role}`, `rebuild_duration_s{kind}`, `purge_rows_deleted{table}`, `voice_objects_overdue` (anything ephemeral older than 15 min).

### 4.14 PII classification

| Class | Where | Handling |
|---|---|---|
| **Identity** (email, display name, birth date, sign-in ids, payment customer id, `residence_country`) | `learners`, auth tables, processor | Encrypted at rest (RDS); never in Langfuse or Sentry; export includes name, email and country; deletion removes; `deletion_ledger` keeps an HMAC of the email, not the email; `residence_country` is asked, never inferred (ADR-20), and selects the regime row in 07 §4.9 |
| **Voice (biometric-adjacent)** | `forone-voice`, including the name clip | `sse_c_learner` (per-learner DEK or per-call key); every kind ephemeral when consent is off, the name clip included (the hosts then use the respelled text; section 10 item 5 asks for the exception); purged within 24 h of revoke, all versions; never leaves the region except to the transcription vendor during processing; never in the research set |
| **Learner speech and writing (content)** | `events` payloads (`call_turn*`, `chat_message`, `onboarding_answer`, `after_pass_result`), `conversation_chunks` [P1], compiled brief bodies stored by their consumers, 01's `model_io` | RLS; stored for the account's life (core function, disclosed); `model_io` holds prompt and completion text in the home region regardless of consent; Langfuse receives text **only** for learners with `consents.data_use = true`, after `anonymize()`, under the research pseudonym, 30-day retention (ADR-09); the embedding vendor is Google under its existing processor row (ADR-10) |
| **Life facts, sensitive classes** | `life_facts` with `sensitivity` set, `interests.no_go` | Stored only if confirmed in-session; usable only in that session by the chat host and Salma (4.7.3); never in a brief for the teacher, writer or host; never in the research set, and turns that quote them are stripped from it (4.12.4); included in export; never in any shared store |
| **Derived learner model** | the nine stores, `word_uses`, `structure_observations`, `claims`, `skills` (including `pronunciation`, internal) | RLS; exported as plain JSON; never shown as numbers except `notebook_counts`; pronunciation scores never leave `skills` |
| **Behavioral** | all other `events` | RLS; exported; used for rebuilds and metrics |
| **Pseudonymous research** [P1] | `research_transcripts`, `research_pseudonyms` | No `learner_id` on the transcripts; names and entities replaced, sensitive turns dropped; opt-in; deleted on revoke or deletion; called pseudonymized |
| **Operational** | `learner_model_versions`, `rebuild_runs`, `media_objects`, `exports`, `event_ids`, `deletion_ledger` | Contain ids, sizes, counts and hashes only |
| **Shared, no PII** | `gloss_cache`, `lexicon_*`, `structures`, `reporting_categories`, `fact_shelf_life`, `ban_list`, `plans.yaml` | The only cross-learner tables (PRD-v2 12.6); per target language, not per learner |

`forone.learner.pii` is the classification as code: export, the Langfuse scrubber and the purge planner (4.12.2 step 5) read it, and a CI test fails when a table with a `learner_id` column has no row here.

### 4.15 Configuration keys

| Key | Default | Meaning |
|---|---|---|
| `events.client_clock_skew_max_h` / `events.future_skew_max_s` | 24 / 300 | beyond this, `effective_at = received_at` (4.1.4); one rule for 01, 04 and 06; no header |
| `events.id_max_age_days` | 7 | UUIDv7 age check for `source in ('web','worker')`; `import` exempt |
| `events.batch_max` | 50 | events per `POST /v1/events` |
| `events.partition_months_ahead` | 3 | |
| `prior.known_fraction` / `prior.center` / `prior.width` | 0.5 / 1.25 / 0.10 | the saturating prior (4.5.1; moved here from 02 §9 item 3) |
| `prior.k` | 4 | Beta concentration of the frequency prior |
| `prior.size_default` / `prior.size_sd` | 3000 / 1200 | families, when no word check |
| `prior.eye_bonus` / `prior.prod_factor` | 0.05 / 0.6 | per target language in `packages/languages/<target>/lexicon/prior.yaml`; these are `en`'s |
| `scheduler.desired_retention` | 0.85 | PRD-v2 9.4 due threshold |
| `scheduler.structure_early_cap_days` | [1, 3] | |
| `scheduler.pin` | py-fsrs==<pyproject pin>/default | recorded as `code_versions.scheduler`; fitted parameters per `cohort_key` later [P1] |
| `scheduler.due_cap` | 60 | the `due` list only; `kept` and `active_targets` are uncapped |
| `scheduler.stale_days` / `scheduler.stale_floor` | 30 / 0.6 | the shaky-word rule in 4.5.2 |
| `words.owned_sessions` / `words.owned_min_gap_h` | 2 / 24 | |
| `structures.taking_sessions` | 2 | |
| `structures.stable_window_days` / `stable_min_contexts` / `stable_min_sessions` / `stable_acc` | 14 / 5 / 2 / 0.8 | |
| `structures.recheck_weeks` | [2, 4, 8] | |
| `structures.avoidance_min_sessions` / `structures.avoidance_period_days` | 5 / 7 | [P1] learner-local days, no calendar week |
| `errors.pattern_min_obs` / `errors.pattern_min_sessions` | 3 / 2 | PRD-v2 10.5 |
| `facts.viewed_unedited_dwell_ms` | 4000 | D10; the expanded card only; promotion at the visit's end marker |
| `facts.same_fact_similarity` | 0.85 | trigram similarity for "said again" |
| `facts.follow_up_expiry_days` | 21 | a dated fact stays active this long after its date |
| `facts.sensitive_topic_window_days` | 7 | rolling learner-local days for PRD-v2 5.1's topic rule (4.7.3); facts themselves are same-session only |
| `interests.decay_tau_days` / `interests.dormant_below` | 21 / 0.2 | computed on read |
| `briefs.token_budget.{role}` | table in 4.9 | compile fails loudly if exceeded |
| `callbacks.trgm_min_similarity` | 0.3 | the beta's canon and transcript search (4.8) |
| `callbacks.chunk_turns` / `callbacks.exact_search_max_chunks` | 3 / 5000 | [P1] |
| `export.download_url_ttl_min` / `export.keep_days` | 15 / 14 | the re-signed URL behind `GET /v1/exports/{id}` |
| `rebuild.model_ceiling_usd` / `rebuild.parallel_learners` | 50 / 5 | 05 4.14's numbers for a model-version rebuild |
| `retention.backup_days` | 30 | must equal the RDS setting; a CI check reads both |
| `retention.trial_ended_warn_days` / `retention.trial_ended_delete_days` | 83 / 90 | |
| `skills.scale_anchors` | A2 30..42, B1 43..58, B2 59..75, C1 76..84 | |
| `skills.sd_obs_default` | 8 | until standard errors are estimated |
| `pause.default_ms` / `pause.min_ms` / `pause.max_ms` / `pause.margin_ms` | 1500 / 1000 / 2500 / 300 | PRD-v2 5.4.4 |

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Effect | Detection | Fallback | Degraded mode |
|---|---|---|---|---|
| `POST /v1/events` down or Postgres unreachable | No events accepted | ALB health, `events_appended_total` flat | PWA queues in IndexedDB for 24 h and replays (topology); the worker spools to S3 and `api` ingests the spool with `source='worker'` and original timestamps; both meet the same `event_ids` key, so nothing double-counts | Stores lag; the after-pass runs on whatever arrived; a later replay is folded in by the next pass or a rebuild |
| Duplicate storm (a client replays the same batch many times) | Nothing: duplicates are dropped by `event_ids` | `events_duplicates_total` spike | n/a | none |
| A browser posts a producer-only type (`call_turn_verbatim`, `claim_shown`, `after_pass_result`) | Rejected | `events_rejected_total{reason='source_mismatch'}` | D22: 422, nothing appended, the session is flagged for review | none |
| Client clock wrong (over 24 h) | Wrong `occurred_at` | skew check | `effective_at = received_at`, payload flagged; `occurred_at` untouched so the idempotency key still matches a replay | Order within the session may be off by seconds; the after-pass orders call turns by `turn_index`, not by time |
| After-pass result fails validation (schema, quote checks) | The whole result is rejected? No: facts are dropped individually; other sections apply; the `after_pass_result` event records what was rejected | `facts_rejected_total` | Apply what validates; log the rejects with the session id | A fact said once may need a second saying |
| Writer contention (an edit and a pass at once, or two passes for one learner) | The second waits on the `learners` row lock taken first | `lm_lock_wait_ms` p99 | `versions.lock` as the first statement of every writer; Inngest concurrency key per learner on `session/after-pass`; the second writer reads the first's committed result | An edit can wait up to the pass's 1 to 3 s; the "fixed at once" response is late by that much at worst |
| `rater_pin` in a result differs from the window's pin | The result is refused | `after_pass_rater_mismatch_total` | 05's `calibration/run` must pass and bump the pin first; the pass retries after the window is updated | The stores lag one session until the pin is right |
| Verbatim transcription never arrives for a turn (vendor outage, storage off, audio deleted at 15 min) | `call_turns_v.text_verbatim` null | `audio/expire` reports `verbatim_missing` | The pass marks the turn `low_confidence_reason='no_verbatim'`; no observation or word use from that turn is `clean`; no claim; planning uses the streaming text with `confidence=0.5` | Evidence is thinner; nothing is lost |
| Rebuild fails mid-way | Shadow schema partially filled | `rebuild_runs.status='failed'` | Shadow rows dropped; live stores untouched; retry (05's function) | none for the learner |
| Rebuild would retract a shown claim | | diff in `assessment/rebuild` | `status='retracted'`, `notice_pending=true`; Salma says so in the next proof | none |
| A deletion bug (`audio/expire`, the ephemeral logic, the purge) deletes a kept recording | A paid-for recording gone | `voice_objects_overdue` inverse: a `media_objects` row alive whose object is a delete marker (orphan audit) | Versioning on `learners/` prefixes with a 7-day noncurrent expiry: restore the version within 7 days; `media_objects` has the key | none if caught within 7 days; after that, the recording is gone and the learner is told |
| S3 deletion lags (`audio/expire` missed) | Audio past 15 min | `voice_objects_overdue` | The 1-day lifecycle rule on prefix `ephemeral/`; `retention/daily` alert | A promise missed by minutes is logged as an incident, not hidden |
| Export too large or slow (> 1 h) | Link late | step timeout | Step 5 is resumable per object; if the hour is missed, email "still preparing" and finish | none |
| Learner clicks an export link after 14 days, or without a session | 404 / sign-in | | `GET /v1/exports/{id}` asks the learner to sign in and request a new export if expired; nothing is leaked by the link alone | none |
| Learner deletes during a running call | Call continues until the worker's next brief refresh | `learner.deletion_requested` cancels | `api` closes the room at step 1; the worker's spool is discarded for a `deleting` learner; the final sweep in step 7 catches rows that landed in between | none |
| Langfuse deletion API unavailable | Pseudonymous traces remain in a processor for up to 30 days (their retention) | `deletion_ledger.langfuse_requested_at` set, confirmation missing | Retry daily; alert ops; the "deleted" email is not held up (ADR-09: traces are pseudonymous and expire in 30 days) | none |
| RDS failure | Everything | RDS alarms | Multi-AZ failover (topology); PITR restore in the worst case; the last 5 minutes of events can be lost, the PWA queue replays most | A rebuild after restore re-derives stores from the restored log |
| Postgres grows past comfortable size at scale | Slow partitions | table size metrics | After the beta, partitions older than 24 months compacted to Parquet with a reader in `events` (4.1.5); stores stay small (per learner, bounded) | none in the beta |

---

## 6. Cost and performance against the budgets

This domain makes no model calls in the beta. Its cost is the database and the buckets; the P1 embedding call (about $0.0005 a session) sits inside the pipeline's line when it comes. Following 01's reporting rule, fixed infrastructure is a separate line amortized at the actual learner count and never folded into the per-session figure that the $1.00 stop line watches; sessions are 1 to 3 a day per learner under ADR-04, so the per-learner-month figures below assume 20 sessions at the typical use decisions.md states.

| Item | Beta (100 learners, Jan 2027) | 10,000 learners | Note |
|---|---|---|---|
| Events | 300 per session × 20 sessions × 100 = 600k rows/month, about 0.6 GB; `after_pass_result` adds about 20 KB a session | 60M rows/month, about 65 GB/month | RDS gp3 storage about $0.115/GB-month in `eu-central-1` [ASSUMPTION; the same order in `me-central-1`]; 0.8 TB after a year at scale is about $90/month |
| Stores | about 5,000 `word_bank` rows, 2,000 `word_uses` and 300 `structure_map` rows per learner; under 10 MB per learner | 100 GB | bounded per learner |
| `conversation_chunks` [P1] | not built | 10 per session; about 3 KB each at Google's dimension; 120 GB/year | exact search per learner 20 to 50 ms at 2,000 chunks (not 5 ms); an HNSW index past 5,000 |
| Voice audio (storage on, 60% of learners [ASSUMPTION]) | 6 min call × 0.36 MB/min + extras ≈ 2.5 MB per session; 50 MB per learner per month; 3 GB/month | 300 GB/month, 3.6 TB/year, about $85/month at $0.023/GB; noncurrent versions add under 2% at a 7-day expiry | this is the only per-learner line that grows without bound; deletion and revoke remove it |
| Produced audio | the pipeline's line (01 §10 #7 on archive growth) | | |
| Exports | transient | | |
| RDS instance (fixed) | db.t4g.medium Multi-AZ, about $120/month [ASSUMPTION] | db.r6g.xlarge Multi-AZ, about $600/month | shared with every other domain; in 01's fixed-infrastructure line |
| Fixed cost per session, amortized | about $0.06 (the $120 instance over 2,000 sessions) | about $0.003 ($600 over 200,000) | reported as fixed, not variable: the first draft's "$0.002" hid the instance |
| Variable per session (S3 requests, storage growth) | under $0.002 | under $0.002 | inside the 14.5 "proof share and hosting $0.03" line |
| Rebuild, code-version | $0 vendor; about 2 s a session of database time | same | replays `after_pass_result` |
| Rebuild, model-version (05 runs it) | about $0.004 a session; 100 learners × 20 sessions = $8 a run in January | about $8,000 for a year of history at 10,000 learners; the $50 ceiling per run means a scoped rebuild, never a fleet-wide one without a decision | the cost the first draft stated as zero; section 10 item 7 |

Latency commitments: `events.append` batch of 50 under 30 ms (one CTE: `event_ids` then `events`); `p_understood_many` for 1,500 units under 100 ms (one query by `(learner_id, unit_id = any(...))` plus in-memory prior for misses); `due_list` under 150 ms; `briefs.compile('teacher')` 300 to 500 ms on every read (no cache); `apply_after_pass` 1 to 3 s for a session with 25 turns (dominated by FSRS updates for about 200 units, each a few microseconds, and the pg_trgm fact matching), under the per-learner lock; `apply_learner_edit` under 50 ms plus the lock wait; `search_callbacks` 20 to 50 ms (trigram over canon and transcripts); export 5 to 15 minutes; purge under 2 minutes; code-version rebuild about 2 s per session of history, model-version about 20 s plus the vendor's batch latency.

---

## 7. Build plan for 2026-11-18 to 2026-12-22

Dates per ADR-07; the week contents are the first draft's moved 16 days, with two changes the reviews asked for: export, deletion, the ledger and the retention queries move to week 3 (they need only `events`, `media_objects` and the roles, all week-1 work, and were the P0 items most likely to slip from a stacked week 5), and week 5 keeps after-pass integration, claims and the end-to-end run. The cross-domain items 10-decision-records §7 places in this domain are marked (ADR). Milestone 0 runs 2026-10-24 to 11-18 in parallel, so its imported events are dated October and November (the `events_2026_10` partition and the import exemption in 4.1.2 and 4.1.3).

| Week | Dates | Ships (P0 unless marked) | Tested with pilot data |
|---|---|---|---|
| 1 | 2026-11-18 to 11-24 | `events`, `event_ids`, `events_seq` DDL with partitions (`events_2026_10` onward, `events_default`), trigger, RLS with `nullif`; `events.append` with the CTE dedupe, producer binding (`allowed_sources`, D22), `schema_version`, the 24 h skew rule; the type registry and all payload schemas (about 45 types, `after_pass_result` among them); `learner_model_versions`, `versions.lock` and `bump`; `learners.{native_language,target_language,residence_country,plan,tz}` with 01 (ADR-02, ADR-04); `lexicon_lemmas`, `lexicon_chunks`, `structures`, `reporting_categories` loaders from `packages/languages/en/` (ADR-02); `word_bank` and `word_uses` DDL (ADR-19), the saturating prior, `p_understood_many`; py-fsrs wrapper pinned, `due_list` with the three lists; `CallMeta.learner_model_version` wired into the adapter middleware (with the cost domain); `media_objects.encryption` by kind with 01 (ADR-12); Alembic baseline under `forone_owner`; `forone_app`/`forone_workflows`/`forone_purge` (`bypassrls`)/`forone_admin`/`forone_human`/`forone_readonly` roles (ADR-17) | Import the 15 Milestone 0 learner files and Scribe transcripts as `source='import'` events (`tools/m0_import.py`, uuid5 ids, October dates land in `events_2026_10`); a browser-origin `call_turn_verbatim` is rejected with 422; a replayed batch with a corrected clock yields zero new rows; `p_understood_many` against the kit's coverage checker on 10 scripts (same numbers within 0.5 points: the acceptance test for the shared prior curve); run `due_list` against the hand-kept "next due" column in the learner files |
| 2 | 2026-11-25 to 12-01 | `briefs.compile('teacher')` returning the pipeline's `TeacherInput` from the field map in 4.9 (reads 05's `session_summaries`, built the same week); `life_facts` with deterministic ids, `follow_ups`, `fact_shelf_life`, `verify_quote` and `verify_quote_text` with the per-language normalizers, the ladder, the `facts_usable` function with the same-session rule; `interests` with salience on read; `goals`; `show_canon` with the trigram index, `search_callbacks` (canon plus trigram), `SeriesBibleExcerpt`; `briefs.compile('writer')`; `structure_map`, `structure_observations` DDL and the `structure_acc` function; `forone.learner.rebuild` library (shadow, replay, diff, swap) for 05's `assessment/rebuild` | Replay Muath's confirmed facts: every confirmed fact in the learner files must pass `verify_quote` against the imported transcripts (target: 100% of confirmed, and every unconfirmed one that Muath rejected fails or stays `heard_once`); a dated fact on day D appears in D+1's brief with `follow_up_due = true` and passes check 4; a replay of one learner with three edits (remove, don't bring up, correction) keeps all three; compile a teacher brief for each pilot learner and have the pipeline's teacher step produce a plan from it |
| 3 | 2026-12-02 to 12-08 | Onboarding writes: `onboarding_answer` (A9 with `residence_country` and the pair, ADR-20), `word_check_answer` → prior seeding and the first `skills` row; `consents` (no `notes_mode`); intake facts as `usable` via `intake_card`, `ground_truth` on ✎; player and article event ingestion end to end from `web` (play, huh, tap, keep, mark, article_scroll, followed_answer, `episode_next_requested`), `playback_intervals` and the active-day rule with `expects_drop`; `notebook_counts`; `taste`; **`learner/export`** content and `GET /v1/exports/{id}`; **`learner/delete`** with the catalogue-driven purge, row counts and `deletion_ledger`; `learner/purge-audio`'s object step; `retention/daily` data parts; `forone.learner.pii` with the CI classification test | Word-check scoring against the 15 pilot word checks (the band table reproduces the kit's estimates); export a pilot learner and open the zip on iOS Files, Android, macOS and Windows; delete a synthetic learner and assert every `learner_id` table reports its expected count in the ledger and both S3 prefixes list empty (versions included); a purge run as a role without `bypassrls` fails loudly |
| 4 | 2026-12-09 to 12-15 | Call events from the worker (`call_turn`, `talkback`, `hold_floor`, `silence`) and `call_turn_verbatim` (including `mode='voice_note'`) from `call/verbatim-turn`; `call_turns_v`; `briefs.compile('host')` with `recasts` (ADR-06), `('salma_talkback')`, `('salma_explain')`, `('chat_host')`; `pause_profile` updater; `media_objects` writes for turn audio under `learners/{lid}/` or `ephemeral/learners/{lid}/` with `key_derivation`; the `ephemeral/` lifecycle rule and versioning on `learners/`; `audio/expire` data step | 30 pilot clips through the verbatim path: `low_confidence_reason` set correctly from the package threshold; an ephemeral turn written with storage off is gone within 15 min and the lifecycle rule would catch it at 1 day; a kept turn deleted by hand is restored from its noncurrent version |
| 5 | 2026-12-16 to 12-22 | `apply_after_pass` complete (append `after_pass_result`, lock, rater-pin check, words and `word_uses`, structures, errors, skills with `pronunciation`, interests, facts, canon, scheduler from `fsrs_grades`, counts) against the assessment domain's `AfterPassResult`, with the Inngest concurrency key (ADR-06: one function, no stage 1); `apply_learner_edit` (all five edit types plus the visit end marker) and `working_on.changed`; `claims` (05's DDL) with the shown-row trigger, `mark_claim_shown`, `briefs.compile('proof')` with `sessions_in_week` computed, `('return_win')`, `('finale')`; code-version rebuild exercised through 05's `assessment/rebuild` on one learner; PITR restore drill; the Langfuse scrub verified against the PII table (ADR-09) | End-to-end with the Milestone 0 learners under a consent that covers it (10-decision-records §10 #13): a full after-pass over 14 days of one pilot learner's imported sessions produces a word bank and structure map that match Muath's hand-kept file on `owned` words and `pattern` errors (target: agreement on 80% of items; disagreements reviewed by hand); a code-version rebuild of that learner reproduces the live stores exactly and retracts nothing |
| P1 (beta, by 2027-01-26) | | `conversation_chunks` and `search_chunks` with Google embeddings (ADR-10); `research_pseudonyms`, `research_transcripts` with the redaction pass; `skill_snapshots` for the finale; the structure avoidance flag; fitted FSRS parameters per `cohort_key`; `.txt` transcript renderings in the export; the tape's comparison (`recording` events are P0); Parquet archive reader (after the beta) | |

**Freeze:** 2026-12-21 12:00 to 12-24 12:00 UTC (and 2026-12-31 to 2027-01-02); the week-5 exit on 12-22 is the last deploy before it.

What is too much for a one-to-two-engineer team and is cut here, deeper than the first draft (the skeptic's list, accepted): a separate analytics warehouse (the events table is queried directly, with `forone_readonly`); a CDC or stream out of Postgres; cross-region replication; a schema registry service (the Pydantic registry in code is the registry); per-learner physical partitions; the `briefs` cache table and its GC rule (D12); `conversation_chunks` and embeddings (D11, P1); `claim_invalidations` (05's statuses instead); `skill_snapshots` (P1); the `lm_write` mirror event; `research_transcripts` (P1); the weekly `pg_dump` drift check; the structure avoidance job (P1, 05 cuts it too); the fractional-review weighting; automated FSRS parameter fitting. Kept, because the P0 contract needs them: `events` and `event_ids`, versions, `word_bank` and `word_uses`, `structure_observations`/`structure_map`, `error_profile`, `skills`, `interests`, `life_facts`, `goals`, `taste`, `show_canon`, `notebook_counts`, `consents`, `claims` (05's), export, purge, RLS, `pgaudit` on `forone_human` only (ADR-17 keeps it, against the skeptic's cut), and the rebuild library (the runner is 05's and is script-run in the beta). That is still a full five weeks for one engineer on this domain; 10-decision-records §10 #10 is the second-engineer decision. [OPEN for Muath, section 10 item 7] the two remaining scope cuts that touch an untagged PRD-v2 requirement: `assessment/rebuild` automation stays script-run in the beta (PRD-v2 8.5 requires rebuilds; the script satisfies it by hand), and `research_transcripts` writes nothing until P1 (PRD-v2 12.5.5 describes the set; the consent switch exists).

---

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| An event stream (Kafka, Kinesis, Redpanda) in front of Postgres | Nothing consumes events in real time except the after-pass, which Inngest already triggers from `call.ended`; a stream adds an operator and a second source of truth |
| A document database for the learner model | The model is counts, states and probabilities joined to a structure inventory and a lexicon; the fitter's coverage query and the claim gate's windows are relational |
| Chat-style memory (summaries retrieved by similarity) as the fact store | The personalization lens's evidence: 57.7% recall, overwrites, 15 to 30% hallucinated answers; a quote-backed row with dates is the fix |
| Storing facts in the series bible JSON | Facts need a ladder, expiry, supersession and a quote check; the bible is fiction state and belongs to the pipeline |
| Half-life regression or a custom forgetting model | Needs data; FSRS is open, benchmarked and already fits the PRD's "FSRS-style" wording; weights can be fitted later on our own reviews |
| Point probabilities plus a separate confidence number | The Beta gives the range, the update rule and the "shaky after months" behavior in one representation |
| HNSW index across all learners for callbacks | Filtered ANN recall is unreliable at small per-learner cardinalities; exact search is faster and exact at under 20k chunks |
| Materialized views for briefs, or a `briefs` cache table keyed by version | Briefs are role-shaped and date-dependent; the version moves on every pass and edit, so a cache would hit a few times a week and serve stale tails; compile on read and let the consumer keep the body it used (D12) |
| A hand-written `(1 + t/(9S))^-1` retrievability beside the library's scheduler | The pinned py-fsrs release computes its own curve (FSRS-6 shape and parameters); a foreign curve puts the 0.85 threshold about 10 points off at `t = S`; use `Card.get_retrievability` (D7) |
| This document's own `learner/rebuild` function | The assessment domain owns `assessment/rebuild` and the analyst it must re-run; two runners would mean two semantics for one word; the shadow mechanics stay here as a library (D14) |
| Regenerating facts, goals, canon and claims in a rebuild | Their ids would change and every replayed learner edit would point at a missing row, silently losing deletions and "don't bring up" flags; they are carried over (D14) |
| An AES-encrypted export zip with a passphrase, behind a 7-day presigned URL | Python's `zipfile` cannot write AES; phones cannot open it; a presigned URL under a task role dies with the credentials; an authenticated route that re-signs on click needs no long-lived secret (D16) |
| Keying the ephemeral objects as `{lid}/ephemeral/...` | S3 lifecycle rules filter by literal prefix or tag; the backstop rule could not be written (D15) |
| A hand-listed purge order | It had already missed `model_io`, `crisis_log`, `audit_log` and the payment tables; the catalogue plus an allow-list plus a CI test cannot miss a new table (D17) |
| Learner edits through Inngest | "Fixed at once" and the next render must show it; a synchronous path inside the append transaction is the honest implementation |
| Physical partitioning of `events` by learner (hash) | Partition pruning by learner buys nothing over the `(learner_id, occurred_at, seq)` index; month partitions give retention and backup granularity |
| Scrubbing backups on deletion | Not possible with RDS snapshots; 30-day retention makes the promise true by configuration and is written in the privacy text |
| Keeping anonymized research rows after account deletion | Legally defensible, wrong for "the data is theirs"; D18 deletes them (and section 10 asks Muath to confirm) |
| A separate audit log table | `events` plus `after_pass_result` is the audit log of what the model proposed and what code did with it; `learner_model_versions` is the audit of every store write (the first draft's `lm_write` mirror is cut as redundant) |
| Counting "learned" from the map's counters | Claims must open to a turn; `structure_observations` keeps the evidence and the window is a query |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check.

1. **System topology (01).** Python backend on **Postgres 16**; the `events` table is mine and I honor its two requirements (monthly partitions created by `retention/daily`; `inngest_run_id` and `vendor_call_id` columns). Its contract's `client_event_id` is my `event_id` column and its `received_at` is mine too (the first draft said `recorded_at`); its `unique (learner_id, client_event_id)` is enforced by my `event_ids` table, because the partitioned table cannot carry it; its 24 h skew guard is the one rule (my 300 s rule and the replay header are gone). `CallMeta.learner_model_version` is an `int` (its 4.5) and is populated by every caller from `versions.current()`. The `learners` (with `native_language`, `target_language`, `residence_country`, `plan`, `tz`, ADR-02 and ADR-04), `learner_schedule` (with `expects_drop`, ADR-19), `learner_keys`, `sessions`, `doors`, `calls`, `media_objects` (with `encryption` and `key_derivation`, ADR-12), `feed_tokens`, `model_io` tables are its; I add `learners.lm_version` and `learners.wrong_memory_n` columns. Its `learner/export`, `learner/delete`, `retention/daily` shells call my step bodies; `plans.yaml` and `episodes.state` are its names and I use them. **Ruled (10-decision-records §4):** `api` and `workflows` append events, `call_turn_verbatim` is a second event, learner edits are applied synchronously by `api`. **Conflict to rule on:** its key layout `forone-voice/learners/{lid}/calls/{callId}/{ephemeral/}turn-{n}.ogg` puts `ephemeral/` mid-key; 4.11 owns the layout and puts it at the bucket root (`ephemeral/learners/{lid}/...`); the call-worker's PUT path changes accordingly. **Conflict to rule on:** its capacity table says "cold partitions older than 90 days compacted to Parquet"; 4.1.5 rules that nothing is detached in the beta and 24 months after it.
2. **Episode generation pipeline (02).** `TeacherInput` as in its 4.3, with `interests[].entities`, `facts_usable[].entities`, `session_at`, `taste.swap_count_30d`, `onboarding_session_id` and `last_14_days` from 05's `session_summaries`, is what `briefs.compile('teacher')` returns (the field map is in 4.9); the day's 1 to 3 episode briefs come from one teacher brief (ADR-05); the fiction tables (`series_bible`, `side_characters`, `running_jokes`, `arcs`, `seasons`, `episodes`, `episode_artifacts`, `gloss_cache`, `format_history`, `script_embeddings`) are its; it sends realized structure counts and host positions in `episode.ready.artifacts` (`realized_structures`, `canon_from_episode`) so `structure_map.heard_n` and `show_canon{position_host}` can be written; it calls `stores.mark_targeted` at publish; `episodes.state` is the ruled name (ADR-19); its `learner_model_version: string` is the `lm_v_{n}` serialization of my integer; the editor's check 4 calls `facts.verify_quote(fact_id)` and `facts_usable(learner_id, publish_date, 'writer')`; its saturating prior is adopted in 4.5.1 with the three config keys; it stores the brief body it used at `brief_ref` (there is no `briefs` table). **Conflict to rule on:** its §9 item 3 says "A3 card facts are `ground_truth` at once"; 4.7.2 follows PRD-v2 8.4.2 (a card left standing is `usable`, an edited card is `ground_truth`). **Conflict to rule on:** its object keys are `episodes/{learner_id}/{episode_id}/...`; 4.11 uses `learners/{lid}/episodes/{episode_id}/...` with its file names (`episode.m4a`, `episode_feed.m4a`, `episode_feed.mp3`, `scene-{n}.m4a`); the publisher adopts the prefix.
3. **Live call and voice stack (03).** The worker emits `call_turn{speaker:learner|host|salma}`, `talkback` (with `asked_native`), `hold_floor`, `silence` through `POST /internal/events` with the call JWT (which binds `source='worker'`, D22) and UUIDv7 ids, uploads each learner turn to the key layout in 4.11 (`learners/{lid}/...` or `ephemeral/learners/{lid}/...` when `consents.voice_storage=false`, SSE-C under the per-call key, tagged `ephemeral=true`), posts small-door voice notes so that `call/verbatim-turn` writes `call_turn_verbatim{mode:'voice_note'}`, and reads `HostLearnerSlice` (with `recasts`, ADR-06) and the talkback dict through `api`'s brief endpoint; the host brief it uses is the merge of the pipeline's `call_brief` artifact and my slice; the anxiety flag it sets during a call is sent as `silence`/`call_turn` payload fields, not written to stores; the correction guard (07) runs on its output and reads nothing from my stores.
4. **Assessment engine, after-session pass and claim gate (05).** It produces `AfterPassResult` exactly as 4.3.0, including `word_uses` (ADR-19), `pronunciation` and `fsrs_grades` (its evidence-to-grade mapping is the only one; I will adjust field names to its document at integration, not the structure); `session/after-pass` is one function with the 10-minute budget (ADR-06) and runs with a concurrency key per learner; it owns `assessment/rebuild` and calls my `forone.learner.rebuild` library, re-running `analyst.full` only for a model-version rebuild and never the memory keeper, with facts, goals, canon and claims carried over (D14); the `claims` table here is its DDL and lifecycle, and its module, `assessment/rebuild` and `memory/correct` are the only writers of `status`; its `session_summaries` feed `last_14_days`; its calibration job sets `skills.*.calibrated`; the recording rater writes `stable_confirmed_at` through `stores.confirm_stable`; the recognizer confidence threshold is in `packages/languages/<target>/` and is what sets `structure_observations.clean` and `word_uses.clean`; its `rater_versions` row for the window is what `apply_after_pass` checks `rater_pin` against. **Conflict to rule on:** its `notebook_viewed {fact_ids}` event versus my `fact_card_viewed` per card plus `notebook_visit_ended`; mine carries the dwell the rule needs.
5. **Client app, podcast feed and delivery (06).** `web` mints UUIDv7 event ids, batches events, replays the offline queue for up to 24 h with original timestamps and no special header, sends `fact_card_viewed` only for the single expanded card while it is in the centre band, with dwell and a `visit_id`, and a `notebook_visit_ended {visit_id}` marker when the notebook is left (4.7.2); sends `claim_shown` when a claim is rendered (surfaces `proof`, `new_for_you`, `finale`, `return`) and `episode_next_requested` on "next one" (ADR-05); shows no notes, margin note or polish card (ADR-06); every API response carries `learnerModelVersion`; the notebook reads the views in 4.3.9 with labels from `packages/native/<lang>/strings/` and never computes a number client-side; the export download goes through `GET /v1/exports/{id}` with the learner's session; show audio arrives by presigned URL (ADR-12) and `episode_feed.mp3` is the feed file at my key.
6. **Security, privacy, consent and compliance (07).** Owns the consent copy per native language (`packages/native/<lang>/consent/`) and the semantics of `consents`; owns the regime table (ADR-20) that `residence_country` selects; approves the key layout (4.11), the root `ephemeral/` prefix and lifecycle backstop, versioning with a 7-day noncurrent expiry on kept prefixes, the authenticated export link, the `deletion_ledger` HMAC, the 30-day backup statement in the privacy text, the Langfuse rule (metadata only; text for `data_use` learners after `anonymize()`, ADR-09) and the word "pseudonymized" for the research set; owns `learner/purge-audio` (my object step), `crisis_log` (pseudonymized on deletion pending section 10 item 6), `audit_log`, `research_pseudonyms`' consumer in Langfuse; owns the correction guard (`guard.check_output` item 6), which reads nothing here; confirms the name-clip default (ephemeral when consent is off) and the exception Muath may grant (section 10 item 5); `keys.get_dek` caching per ADR-18 applies to every read here except export.
7. **Cost model, vendor strategy and tracing (08).** `vendor_calls` carries `learner_model_version` from `CallMeta` and is written in its own transaction (ADR-13), so `events.vendor_call_id` may reference a row that committed before the event; the weekly cost report joins on `learner_id` and the "Margin by plan" section reads `learners.plan` (ADR-15); the model-version rebuild cost (section 6) is a line in its cost model; the embedding vendor is Google under the existing processor row (ADR-10); Langfuse `user_id` is the research pseudonym (ADR-09).
8. **Evaluation, observability and operations (09).** Reads my metrics (4.13), runs the monthly false-claim audit against `claims where status = 'shown'` and `claim_evidence`, computes "wrong memories per 100 callbacks" from `wrong_memory_flag` events over `show_canon{callback_made}` rows, `explicit_corrections_per_100_turns` from the guard's counters (not from my stores; ADR-06), and the "how much did you follow" comparison from `followed_answer` against the pipeline's `why.predicted`; computes `proofs.sessions_in_week` rather than reading a stored column (ADR-19); `cohort_key = invite_date` is the grouping for the FSRS parameter fit and the research set; `measures/hourly`, `privacy/verify` hourly and `retention/daily` per learner-local midnight (ADR-16) are its schedules for my step bodies; owns the `/admin` button that sends 05's rebuild event with a reason.

---

## 10. Open for Muath

Items 10-decision-records §10 now owns are one line each; the rest are specific to this domain. Settled by the rulings and removed from this list: processors that hold learner text (the first draft's #3: ADR-09 fixes the Langfuse rule and ADR-10 the embedding vendor; approval of the processor list is 10-decision-records §10 #14) and research rows after deletion (the first draft's #2: 10-decision-records §10 #15 records "deleted").

1. **[OPEN for Muath] English Grammar Profile permission (PRD-v2 Part 18 #8), by 2026-11-24 (end of build week 1).** The `structures` table ships either way (D19), but the English inventory's labels, bands and ids come from EGP if permission is granted; if not, the fallback is the kit's hand list plus public CEFR descriptors, which is thinner (about 150 structures instead of 300) and must be grown by hand during the beta. The inventory is the language gate's fifth check for English (ADR-03). Money or a letter to Cambridge.
2. **Home region and the legal view on storing learner voice:** see 10-decision-records §10 item 1 (this domain is indifferent between `eu-central-1` and `me-central-1`; one config key).
3. **Which jurisdictions the beta covers on day one:** see 10-decision-records §10 item 2 (the regime row `residence_country` selects decides the breach clock the deletion ledger must satisfy).
4. **[OPEN for Muath] Sensitive facts: same session only, or the rest of the week.** 4.7.3 follows PRD-v2 8.4.3 strictly: a confirmed health, money, relationship, religion or politics fact is used only by the chat host and Salma in the session where the learner raised it, and never by the teacher, writer or host. The first draft let it be used for episodes for the rest of that week, reading PRD-v2 5.1's rule for sensitive *topics* as covering stored *facts*. The strict reading is the default; if you want the day-after episode to be able to pick up "my father is in hospital" when the learner raised it yesterday, say so and the week rule (rolling 7 learner-local days) becomes the alternative with one sentence in the consent copy. Counsel's view on "explicit consent for sensitive-class facts" (10-decision-records §10 item 1) bears on this.
5. **[OPEN for Muath] The name clip.** The default now complies with PRD-v2 12.5.3: the learner's own recording of their name (A3) is a learner-voice kind like the others, ephemeral when voice storage is off and purged within 24 hours of revoking consent; the hosts then use the respelled text. The request is for the exception: keep the 3-second clip regardless of voice-storage consent so the hosts say the name right, with one sentence of consent copy ("we keep the 3-second clip of your name so the hosts say it right; delete it any time in Controls"). Counsel and brand voice.
6. **[OPEN for Muath, with counsel] `crisis_log` after account deletion.** PRD-v2 7.9.4 logs every crisis activation for annual reporting (SB 243 if it applies, 10-decision-records §10 item 12). The purge (4.12.2) pseudonymizes the row (learner id replaced, text removed) rather than deleting it, so the count survives and the person does not. Confirm, or rule that the row is deleted with everything else.
7. **[OPEN for Muath] Rebuilds in the beta: who runs them, and two scope cuts.** A model-version rebuild re-calls the analyst over a learner's history (about $0.004 a session; $8 for the January cohort, $8,000 for a year at 10,000 learners; the $50 ceiling per run forces a scope) and can retract a shown claim, which Salma must then mention. Decide whether rebuilds during the paid beta need your sign-off per cohort (05's `/admin` button asks for a reason either way). Two cuts touch untagged PRD-v2 requirements and are tagged here as the brief requires: `assessment/rebuild` automation is script-run in the beta (PRD-v2 8.5 requires rebuilds; the script performs them), and `research_transcripts` writes nothing until P1 (PRD-v2 12.5.5 describes the set; the consent switch exists). Accept both or fund the second engineer (10-decision-records §10 item 10).
8. **[OPEN for Muath] The 30-day backup statement.** The privacy text must say "deleted from live systems within 24 hours and from backups within 30 days" and the RDS retention must be exactly 30 days (not longer for operational comfort). Confirm the wording with counsel so engineering sets the number once.
9. **[OPEN for Muath] Storage growth of kept voice (money).** At 10,000 learners with 60% keeping recordings, voice storage grows about 3.6 TB a year (about $85/month at list, plus under 2% for the 7-day noncurrent versions), on top of the produced-audio archive the topology flagged (10-decision-records §10 item 15, archive growth). Both are small now; confirm they are acceptable or set a per-learner retention (for example, call audio older than two seasons is deleted unless marked kept) that the consent copy must then state.
10. **[OPEN for Muath] Export form.** D16 is now a plain zip behind an authenticated link (`GET /v1/exports/{id}`, the learner's session, a 15-minute URL on click), available 14 days; no passphrase, because the AES zip would not open on a phone and the passphrase would be lost by a learner who exports and then deletes. The one question left (10-decision-records §10 item 15 keeps it here): do you want a passphrase in addition to the sign-in for the download? The honest answer is no; say so and the item closes.
11. **Fixed infrastructure budget** (the RDS instance is the largest line this domain adds): see 10-decision-records §10 item 9.
12. **Consents for Milestone 0 data** (the week-1 import and the week-5 end-to-end run depend on it): see 10-decision-records §10 item 13.

---

## 11. Revision log (2026-11-06)

One bullet per finding of the two reviews (conformance 24, skeptic 30; neither had been applied before this revision) and per ADR. Where the review's fix and an ADR disagreed, the ADR won and the bullet says so.

- conformance blocker "rebuild contradicts itself; AfterPassResult never logged" → D21 and the `after_pass_result` event (4.1.1, 4.1.6); two rebuild kinds in flow D (3.3) and D14; both costs in §6; sign-off in §10 item 7.
- conformance major "partitioned table cannot enforce (learner_id, event_id); skew rewrite inserts twice" → `event_ids` table and the CTE append (4.1.2, 4.1.3, D3); `occurred_at` never rewritten, `effective_at` added, `received_at` (01's name) replaces `recorded_at` (4.1.2, 4.1.4); column-name mapping to `client_event_id` stated in 4.1.3 and §9 item 1.
- conformance major "due_list puts never-reviewed cards at R = 0; kept words sliced away" → `due_list` returns `due` (reps ≥ 1, capped 60), `kept` and `active_targets` separately; library retrievability; `next_interval` dropped (4.5.3, D7, 3.4).
- conformance major "sensitive facts usable all week" → same-session-only rule in `facts_usable(…, role, session_id)`; writer never receives them (4.7.3, 4.7.5, 4.9); the 5.1-versus-8.4.3 tension is §10 item 4.
- conformance major "S3 lifecycle cannot match a mid-key segment; not every voice kind has an ephemeral path" → `ephemeral/learners/{lid}/…` at the bucket root, every learner-voice kind under it, one prefix rule plus tags; layout reconciled with 01, 02, 03, 06 and 04 named owner (4.11, D15, §9 items 1 to 3, 5).
- conformance major "hand-listed purge misses tables; crisis_log unruled" → catalogue-driven purge with allow-list and CI test (4.12.2 step 5, D17); `crisis_log` pseudonymized pending §10 item 6.
- conformance major "dated fact dormant before its follow-up" → dated facts stay active until the follow-up is used or expired; `follow_up_due` flag; week-2 test (4.7.4, 4.7.5, §7).
- conformance major "name clip kept against PRD 12.5.3" → default: a learner-voice kind, ephemeral when consent is off, purged on revoke; the exception is §10 item 5 (4.11, 4.14).
- conformance major "week 5 overloaded; P1 cuts untagged" → export, delete, ledger and retention moved to week 3; rebuild automation and research set cuts tagged [OPEN for Muath] in §7 and §10 item 7.
- conformance major "structure_acc_14d anchored on now()" → `structure_acc(learner, structure, as_of, days)` function; the view kept as a convenience over it (4.3.2, 4.6, D8).
- conformance minor "intake card: usable vs ground_truth" → `usable` with `confirmed_by='intake_card'`, `ground_truth` on ✎ (4.3.6 example, 4.7.2, §7 week 3); the conflict with 02 §9 item 3 is listed in §9 item 2.
- conformance minor "ISO week vs Sunday week" → the review's fix (Sunday-to-Saturday local week) was not applied because ADR-02 and ADR-16 forbid a country-specific calendar; the skeptic's rolling 7 learner-local days is used for PRD 5.1's topic rule, and facts themselves are same-session only (4.7.3, 4.15).
- conformance minor "briefs cache serves date-dependent tails stale" → the cache is cut; compile on read with `as_of` (4.9, D12); resolved together with the skeptic's cache finding.
- conformance minor "no October partition; import ids rejected" → `events_2026_10` and `events_default`; `import` exempt from the age check with uuid5 ids (4.1.2, 4.1.3, §7 week 1).
- conformance minor "attempting→taking lacks obligatory" → `obligatory` in the predicate and in `examples` selection (4.6).
- conformance minor "notebook_counts keeps a wrong higher value" → corrected, with a `count_corrected` claim carrying `notice_pending` so Salma says so once (4.3.9, 4.10, §2 law 1 row).
- conformance minor "PII table allows Langfuse text without consent; OpenAI embeddings" → consent gate per ADR-09 and `model_io` noted; embedding vendor is Google per ADR-10, so the review's [OPEN] was not opened (4.14, §10 preamble).
- conformance minor "onboarding_answer as a quote source" → typed answers only; voice A3 answers quoted from `call_turn_verbatim`; the confirmed card as fallback with `intake_card` (4.7.1).
- conformance minor "AES zip cannot be written by zipfile" → no AES, no passphrase; plain zip behind `GET /v1/exports/{id}` (4.12.1, D16); the iOS/Android open test in week 3; §10 item 10 reframed.
- conformance minor "24 months vs 90-day Parquet" → nothing detached in the beta, 24 months after it with a reader in `events`; 01's line superseded (4.1.5, §5, §9 item 1).
- conformance minor "no schema_version" → `events.schema_version` and one upgrader per `(type, version)` (4.1.1, 4.1.2, 3.1).
- conformance minor "HMAC is pseudonymization; sensitive turns in research text" → "pseudonymized" everywhere, `research_pseudonyms` per ADR-09, turns quoting sensitive facts dropped (4.12.4, 4.14, D18).
- conformance minor "half an episode played is unspecified" → `playback_intervals(session_id)` over deduplicated rows, run after each append, `active_day_marked_at` set once (3.3 A, 3.4, 4.3.9, §2 row 3.6).
- conformance minor "FSRS-4.5 label vs current py-fsrs" → version pinned in `code_versions.scheduler`; library computes R and intervals (4.2, 4.5.3, 4.15).
- conformance "Missing" items → pronunciation store `skills.pronunciation` (4.3.4, 4.3.0); export and delete while `trial_ended` (4.12.1, 4.12.3); "delete all recordings" flow (4.12.2); "See all my data" statement (4.3.9, §2); cross-domain conflicts listed (§9); rule (c) trigger (4.7.2); chunks from verbatim text (4.8); `rater_pin` check (4.3.0, §2 row 10.11, §5); events after deletion started (3.3 A, 4.12.2 steps 1 and 7).
- skeptic blocker "idempotency does not exist as written" → same fix as the conformance major above (`event_ids`, `effective_at`); D3 and flow A updated.
- skeptic blocker "identity column on a partitioned table needs PG17" → `events_seq` sequence, `events_learner_seq` index, Postgres 16 stated once (4.1.2, 4.13).
- skeptic blocker "lifecycle backstop cannot be expressed" → as the conformance S3 fix; per-learner listing with two prefixes in 4.12.2 step 3.
- skeptic blocker "prior curve contradicts 02" → 02's saturating prior adopted verbatim; `prior.known_fraction/center/width` in 4.15; the kit comparison as the week-1 acceptance test (4.5.1, §7).
- skeptic blocker "claims DDL incompatible with 05" → 05's `claims` and `claim_evidence` DDL adopted, `claim_invalidations` dropped, shown-row trigger, `rebuild_runs` kept (4.10, D13, 3.1, §8).
- skeptic major "two rebuild runners; zero cost claimed" → `learner/rebuild` deleted; `forone.learner.rebuild` library under 05's `assessment/rebuild`; carry-over list; 05's cost and time (3.1, 3.3 D, 3.4, D14, §6).
- skeptic major "regenerated rows get new ids; edits lost" → deterministic uuid5 ids for learner-governed rows and carry-over in rebuilds; the three-edit replay test (4.3 intro, 4.3.6, 4.3.7, 4.3.9, 3.3 D, §7 week 2).
- skeptic major "TeacherInput cannot be compiled from the DDL" → `entities` on `interests` and `life_facts`, `swap_count_30d` computed, `session_summaries` named, `onboarding_session_id`, the field-to-table map (4.3.5, 4.3.6, 4.9).
- skeptic major "forone_purge has no RLS policy; deletes zero rows" → `bypassrls`, `nullif` on the GUC, row counts asserted and recorded in the ledger (4.1.2, 4.12.2, 4.13, D17).
- skeptic major "October partition and import exemption" → as above (4.1.2, 4.1.3).
- skeptic major "lock taken last; lost updates" → `versions.lock` as the first statement; Inngest concurrency key per learner; failure row rewritten (4.2, 3.3 B and C, 4.7.7, §5, D5).
- skeptic major "per-session cost hides the instance" → fixed and variable lines split, $0.06 at 100 learners (§6).
- skeptic major "hand-written FSRS-4.5 curve; weights; two rating owners" → library R, pinned version, weights dropped, 05 owns the grade mapping (4.5.2, 4.5.3, D7, §8).
- skeptic major "briefs cache has near-zero hit rate" → cut (4.9, D12, 4.12.3, 4.15, §8).
- skeptic major "nothing binds a type to its producer" → `allowed_sources`, `source` from the principal, 422 on mismatch, week-1 test (4.1.1, D22, 3.3 A, §5).
- skeptic major "7-day presigned URL dies with task credentials" → authenticated `GET /v1/exports/{id}` re-signing 15 minutes (4.12.1, D16, §5).
- skeptic major "four key layouts, three file-name sets, per-call key ignored" → one layout owned here with 02's file names and 01's `learners/{lid}` prefix; `key_derivation` in export step 5 (4.11, 4.12.1, §9).
- skeptic major "OpenAI embeddings; 1536 baked in; marginal feature" → `conversation_chunks` P1, no typmod, Google (ADR-10); beta callbacks from canon plus trigram (4.8, D11, §7).
- skeptic major "versioning off gives consented audio zero recovery" → versioning on `learners/` prefixes with 7-day noncurrent expiry, off for `ephemeral/`, all-versions delete in purge; failure row added (4.11, 4.12.2, §5).
- skeptic major "cut deeper for one engineer" → the list in §7 (cache, chunks, invalidations, snapshots, `lm_write`, research set, drift check, avoidance, weights, GC); `pgaudit` kept on `forone_human` only because ADR-17 rules it (ADR wins over the cut).
- skeptic major "view on now() cannot replay" → `structure_acc` function with `first_at`/`last_at` and `as_of` (4.3.2, 4.6).
- skeptic minor "300 s rule bypassed by a header; field names" → one 24 h rule, no header; `received_at` (4.1.4, 4.15, §9 item 1).
- skeptic minor "dwell on a scrollable list; no trigger" → expanded card only, centre band, `notebook_visit_ended` marker, promotion in `api` on that batch (4.1.1, 4.7.2, D10, §9 item 5).
- skeptic minor "decay compounds" → `salience_base` plus `last_engaged_at`, computed on read, `dormant` a predicate (4.3.5, 4.7.6).
- skeptic minor "ISO week contradiction" → rolling 7 learner-local days for the topic rule (4.7.3).
- skeptic minor "email through Inngest; salted hash not lookup-able" → `deletion_started` sent synchronously by `api`, final email from a token-only step, HMAC everywhere (4.12.2 steps 1 and 7, D17).
- skeptic minor "5 ms vector search is wrong" → 20 to 50 ms stated, `exact_search_max_chunks = 5000` (4.8, 4.15, §6).
- skeptic minor "turn_index index on the text expression" → index on `((payload->>'turn_index')::int)` (4.1.2).
- skeptic minor "name replacement is not anonymization" → research set P1, redaction pass, "pseudonymized" (4.12.4).
- skeptic minor "small_door_voice_verbatim not in the taxonomy; verify_quote signatures" → voice notes are `call_turn_verbatim{mode:'voice_note'}`; both `verify_quote(fact_id)` and `verify_quote_text` (4.1.1, 4.7.1, 3.4).
- skeptic "Missing" items → Postgres version (4.13); deterministic ids (4.3); TeacherInput map (4.9); producer rule (4.1.1); concurrency and lock-first (3.3 B); October partition (4.1.2); one owner for grades and for the rebuild (D7, D14); additive-migration versus rebuild policy (4.13); row-count verification (4.12.2); versioning recovery window (4.11); `word_bank` sizing rule (4.3.1); pooling guidance (4.13); Alembic as `forone_owner`, never at runtime (4.13).
- ADR-01 → front matter cites decisions.md and the ADRs where they changed a PRD part.
- ADR-02 → `learners.{native_language,target_language,residence_country,tz}`; `packages/languages/<target>/` for lexicon, inventory, prior and recognizer threshold; `packages/native/<lang>/` for labels, consent copy, Salma's phrases and the quote normalizer; `label_ar`/`text_ar`/`topic_label_ar`/`asked_ar`/`english_line`/`why_english` replaced by `label`, `text_native`, `topic_label_native`, `asked_native`, `target_language_line`, `why_this_language`; `reporting_categories` keyed by `lang`; loader `--lang en`; no Saudi, Riyadh, PDPL-only or Arabic-only assumption remains except as one instance of the general rule (4.3.5 to 4.3.7, 4.4, 4.7.1, 4.7.7, 4.10, §1, §2).
- ADR-03 → the structure inventory named as the gate's fifth check (4.4, §10 item 1).
- ADR-04 → `learners.plan`, `plan.episodes_per_day` and `episodes_today` in the teacher brief, `plans.yaml` as a shared no-PII table (4.9, 4.14, §2, §9 item 1).
- ADR-05 → `episode_next_requested` event, one teacher brief for the day's 1 to 3 episodes, `daily_extra` shares the key layout (4.1.1, 4.5.3, 4.9, 4.11).
- ADR-06 → removed `note_shown`, `margin_note`, the notes door, `notes_mode` (consents and `consent_change`), the `salma_notes` brief role, stage 1 of the after-pass, "notes" from the failure table and the 90 s budget; `say_it_once` and `recording` re-homed; `recasts` on the host brief as the only correction channel; `salma_explain` role; "New for you" as `claim_shown{surface:'new_for_you'}` (3.3 B, 4.1.1, 4.7.7, 4.9, 4.11, §2, §5, §7). Size: the removals are small (about 2 KB); the document grew because the reviews were applied.
- ADR-07 → §7 heading and weeks re-dated (W1 2026-11-18 to W5 12-22), P1 by 2027-01-26, freezes, example rows moved into the beta window, "Beta (Jan 2027)" in §6, EGP deadline 2026-11-24.
- ADR-08 → `eu-central-1` default with `me-central-1` as the alternative (4.13, §6, §10 item 2).
- ADR-09 → `research_pseudonyms` table, Langfuse text only for `data_use` learners after `anonymize()`, deletion by pseudonym does not hold up the "deleted" email (4.12.2 step 4, 4.12.4, 4.14, §5).
- ADR-10 → Google embeddings for the P1 chunks; no OpenAI (4.8, D11, 4.14).
- ADR-12 → `media_objects.encryption in ('sse_c_learner','sse_kms_env')` by kind; show kinds presigned and deleted by prefix; DEK destroyed last (4.11, 4.12.2, §2 row 12.6).
- ADR-13 → `vendor_calls` written in its own transaction noted on `events.vendor_call_id` and in §9 item 7; cost aggregates kept at purge.
- ADR-16 → `retention/daily` per learner-local midnight, avoidance on a rolling 7-day period, no calendar week or fixed timezone anywhere (4.6, 4.12.3, 4.1.6 note).
- ADR-17 → `forone_admin`, `forone_human` (pgaudit only), `forone_owner` for Alembic; `forone_readonly` loses pgaudit (4.13, 4.1.2 revoke list).
- ADR-18 → `keys.get_dek` never cached for export; `key_version` bump at key destruction (4.12.1, 4.12.2 step 6).
- ADR-19 → `word_uses(learner_id, unit_id, event_id, occurred_at, clean, correct, prompted, quote)` defined next to `structure_observations` and fed from `AfterPassResult.word_uses` (4.3.1, 4.3.0, D8); `episodes.state`; `learner_schedule.expects_drop` set from the active-day rule; `cohort_key = invite_date` on the research set and the FSRS fit; `proofs.sessions_in_week` computed in the proof brief (3.3 A, 4.5.3, 4.9, 4.12.4, §9).
- ADR-20 → `residence_country` at A9 in `onboarding_answer`, never inferred; selects the regime row; in the PII table (4.1.1, 4.14, §9 item 6).
- ADR-22 → §10 points to 10-decision-records §10 for items 2, 3, 11, 12; two items settled by rulings removed (processors, research rows after deletion).
- Not applied, deliberately: the conformance fix "define the week as Sunday 00:00 to Saturday 23:59 local" (ADR-02/ADR-16 forbid a country's calendar; the rolling-7-day rule is used instead, and stored facts are same-session only); the conformance request to open the embedding vendor as [OPEN for Muath] (ADR-10 settled it); the skeptic's cut of `pgaudit` (ADR-17 keeps it, scoped to `forone_human`); the skeptic's suggestion to keep fractional weights as a seeded probabilistic review (dropped entirely instead: 05 owns the grades and weak evidence moves only the Beta); the conformance "Fix" of a separate `effective_at`-ordered PK is implemented with the `event_ids` table, which both reviews offered as the alternative.
