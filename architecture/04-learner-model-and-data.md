# Learner model, event log and data platform

*Architecture domain 4 of 9 for For one. Written 2026-10-17 against PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the personalization, assessment-progress and AI-architecture lenses, and the Milestone 0 kit (04-production.md, 05-prompts.md, learner-file-template.md). It builds on `01-system-topology.md` (Python 3.12, FastAPI, Inngest, Postgres on RDS in one home region, three S3 buckets with per-learner SSE-C keys) and `02-generation-pipeline.md` (the `TeacherInput` contract, `episode_artifacts`, `gloss_cache`, the fiction side of the series bible). Where this document and those two disagree, section 9 says so for the integrator.*

*Scope: PRD-v2 Part 8 (8.1 to 8.6), 9.4, 10.4 to 10.7, 12.3 (the notebook's data), 12.5 (export, deletion, retention). Tags: [DECISION] decided here; [ASSUMPTION] the spec is silent; [OPEN for Muath] only the owner can settle.*

---

## 1. Summary and the decisions in one table

The learner model is one append-only table of events and nine derived tables that any engineer can drop and rebuild from the events in under a minute per learner. Nothing a model says is written directly: the after-session pass hands this domain a fixed-schema result, code validates it (every life fact's quote must exist word for word in a verbatim transcript or chat message), applies it in one transaction, and bumps a per-learner integer `learner_model_version`. Every brief a role reads, every model call and every claim shown carries that integer, so a bad episode can be traced to exactly the model state that produced it. The scheduler is the open FSRS algorithm (py-fsrs) with a 0.85 recall threshold at the next drop time; word knowledge is a Beta distribution per word and surface, so every number has a range for free. Audio lives in S3 under per-learner keys at predictable paths; text lives in Postgres with row-level security; export is a zip built from the same tables; deletion is a row-ordered purge plus key destruction, with the 30-day backup window stated as a fact of RDS retention, not a promise we have to engineer.

| # | Decision | Chosen | Why | Rejected |
|---|---|---|---|---|
| D1 | Event store | One `events` table, append-only (no UPDATE/DELETE grant, trigger guard), range-partitioned by month on `occurred_at`, per-learner ordering by `(occurred_at, seq)` [DECISION, PRD-v2 8.1, 8.2] | One table is what a two-person team can operate; month partitions give retention and backup granularity the topology already asked for | Kafka or a stream (nothing consumes in real time except the after-pass, which Inngest already triggers); hash partitions by learner (no query gains over the btree at under 100M rows) |
| D2 | Verbatim enrichment of call turns | Two event types, `call_turn` (streaming, from the worker) and `call_turn_verbatim` (batch, from `call/verbatim-turn`), joined by `(call_id, turn_index)` in a view [DECISION] | Keeps the table append-only; the topology's "update the call_turn event" becomes an append | Updating the `call_turn` row (breaks D1); one event written only after verbatim (notes would wait for the whole call) |
| D3 | Idempotency | Client-minted UUIDv7 `event_id`; unique `(learner_id, event_id)`; duplicates are ignored, not errors [DECISION] | The PWA replays a 24 h offline queue; the worker retries; Inngest retries steps | Server-assigned ids (replay would double-count) |
| D4 | Learner-model version | Integer per learner, bumped by one in every store-writing transaction, recorded in `learner_model_versions` with the cause, the event high-water mark and the code versions that wrote it; serialized as `lm_v_{n}` in events and traces [DECISION] | The topology's `CallMeta` carries an int; the pipeline carries a string; both map to this | A global version (cannot tell which learner changed); a hash of the stores (not comparable, not ordered) |
| D5 | Who may write stores | `workflows` (after-session pass, rebuilds, retention) and, for learner-authored edits only, `api` synchronously inside the event append transaction [DECISION, PRD-v2 8.4.7 "fixed at once"] | A learner's correction must be true before the next screen renders; it is still an event, so a rebuild reproduces it | Learner edits through Inngest (a visible delay on "my mistake, noted"); models writing anything (PRD-v2 8.1 forbids) |
| D6 | Word knowledge | `word_bank` row per (learner, unit) with Beta(α, β) per surface (ear, eye, produced); prior from frequency rank and the word-check size estimate; ranges are the Beta 10 to 90% interval [DECISION, PRD-v2 8.3] | Gives p(understood) for the fitter and a range for every number in one representation | Point probabilities with a separate "confidence" column; logistic regression (needs data we do not have yet) |
| D7 | Review scheduler | py-fsrs (open FSRS, MIT) with default weights, evidence mapped to ratings with weights; due = R(next drop) < 0.85; grammar structures capped at 3-day intervals for their first three reviews [DECISION, PRD-v2 9.4] | The best-evidenced scheduler available, zero research cost; the caps implement "every 1 to 3 days early" | Half-life regression (needs training data); a hand-made Leitner (worse by the published benchmarks) |
| D8 | Structure evidence | `structure_observations` rows (one per obligatory context) plus a `structure_map` summary; the 14-day accuracy is a query, never a stored counter [DECISION, PRD-v2 8.3, 10.6] | Claims need evidence links to the exact turn; windows must be recomputable after a rebuild | Counters in the map only (no evidence to open) |
| D9 | Life facts | `life_facts` with `quote_event_id`, a three-rung ladder (`heard_once`, `usable`, `ground_truth`), sensitivity class, `valid_from`/`expires_at`, supersession chain; sensitive candidates are never stored unconfirmed [DECISION, PRD-v2 8.4] | The quote check is a database lookup, not a prompt; the editor's check 4 becomes a join | Free-text memory summaries (the lens evidence: drift, overwrite, hallucination) |
| D10 | Fact confirmation by viewing | A `fact_card_viewed` event with dwell ≥ 4 s and no edit within the same notebook visit promotes `heard_once` to `usable` [DECISION, PRD-v2 8.4.2] | The PRD rule needs a measurable "viewed"; 4 s is long enough to read a card | Promotion on any render (the learner may never have looked) |
| D11 | Show canon and callbacks | `show_canon` rows written by the analyst; `conversation_chunks` with a pgvector column and **exact** (brute-force) search filtered by learner, no ANN index in the beta [DECISION, PRD-v2 14.3] | A learner has under 2,000 chunks in year one; exact search is under 5 ms and always correct; the vector column exists only for callbacks, as the PRD limits it | HNSW over all learners (filtered ANN recall problems, operational noise for nothing) |
| D12 | Compiled briefs | `briefs.compile(role, learner_id, scope)` with a `briefs` cache keyed by `(learner_id, role, learner_model_version, scope_id)`; the stable part of every brief is ordered first for prompt caching [DECISION, PRD-v2 8.6] | A new version invalidates by construction; no TTL logic | Compile on every read (5 s teacher compile on every swap); a materialized view (cannot be role-shaped) |
| D13 | Claims store | `claims` table owned here, written only by the assessment domain's claim gate; `shown_at` is set by the surface that shows it; a rebuild never deletes a shown claim, it writes `claim_invalidations` for Salma's next proof [DECISION, PRD-v2 8.5, 10.10] | The proof producer must read exactly one table; the "never retract silently" rule needs a record | Claims recomputed on read (a shown claim would vanish after a rebuild) |
| D14 | Rebuild | `learner/rebuild` Inngest function: replay the learner's events into a shadow schema, run the after-pass writers at the new code versions, diff, swap in one transaction with a version bump of cause `rebuild` [DECISION, PRD-v2 8.5] | Stores are disposable by design; the shadow schema makes a rebuild safe while the learner is using the app | In-place rewrite (a learner mid-session reads half-rebuilt stores) |
| D15 | Object storage keys | `{learner_id}/...` prefix on every learner object in all three buckets; voice objects under `.../ephemeral/...` when storage is off so one lifecycle rule is the backstop [DECISION, PRD-v2 12.5, 12.6] | Per-learner prefix makes export, deletion and lifecycle rules prefix operations; `media_objects` stays the index | Content-addressed keys (deletion needs the index anyway, and prefix listing is the audit) |
| D16 | Export | Zip with `manifest.json`, `learner_model.json` (the nine stores), `events.ndjson`, `transcripts/`, `notebook.json`, `audio/` (kept audio only), built by `learner/export`; presigned link valid 7 days, emailed within 1 h; the zip is encrypted with a one-time passphrase shown in the app, not in the email [DECISION, PRD-v2 12.5.7] | Plain JSON as promised; the passphrase keeps an intercepted email from being the whole data set | Unencrypted zip behind a presigned URL (one forwarded email leaks a voice archive) |
| D17 | Deletion | Access revoked synchronously; purge in a fixed table order inside 24 h; DEK destroyed last; `deletion_ledger` row with a salted hash of the email so a re-signup is not blocked but the 30-day backup expiry can be audited; RDS automated backup retention set to 30 days so "purged from backups within 30 days" is true by configuration [DECISION, PRD-v2 12.5.8] | Matches the promise with no custom backup scrubbing | Rewriting backups (not possible with RDS snapshots); 7-day retention (breaks PITR for an incident) |
| D18 | Research set | `research_transcripts` is populated only while `data_use` consent is on, from text only, under a pseudonymous id; revoking consent or deleting the account removes the learner's rows [DECISION, PRD-v2 12.5.5] | "Never sold" and "theirs" read naturally as revocable | Keeping anonymized rows after deletion (defensible legally, wrong for the trust contract) [OPEN for Muath, section 10] |
| D19 | Structure inventory source | `structures` table seeded from the English Grammar Profile ids with our own labels, loaded from the language package; if permission (PRD-v2 Part 18 #8) is refused, the same table is filled from the kit's hand-written list and Cambridge's public CEFR descriptors [DECISION, PRD-v2 10.4] | The table shape does not depend on the source | Blocking week 1 on the license |
| D20 | Learner edits apply synchronously in `api` | See D5 | | |

---

## 2. Requirements this domain implements

| PRD-v2 part | Requirement | How it is met here |
|---|---|---|
| 1.2 law 1 | No game furniture; only monotonic plain counts | The stores hold no percentage or level intended for display; `notebook_counts` (words owned, hours heard, hours spoken) are the only learner-visible numbers and only ever increase (4.3.9) |
| 1.2 law 3 | Vetoes and additions re-target the same day | `working_on_edit` applied synchronously, version bump, `working_on.changed` emitted (4.7.7) |
| 1.2 law 10 | Text used once, language comes back | FSRS due list per word, chunk and structure (4.5) |
| 1.2 law 12, 1.3 #1 | No claim without proof; no memory stated unless confirmed | `claims` only via the gate (4.10); briefs expose only `usable` or `ground_truth` facts (4.9) |
| 1.3 #5 | See, export, delete | 4.12 |
| 1.3 #6 | Told, not inferred; sensitive classes never inferred | Validator rejects any fact without a quote; sensitive class requires `confirmed_in_session` (4.7.3) |
| 1.3 #7 | Wrong memory is a bug | `wrong_memory_flag` fixes the fact at once and feeds the 16.1 metric (4.7.7) |
| 1.3 #8 | Data use opt-in | `research_transcripts` gated by `consents.data_use` (4.12.4) |
| 2.2 A3, A4, A9 | Intake facts with cards; word check seeds priors; consent at A9 | `onboarding_answer`, `word_check_answer`, `consent_change` events; prior seeding (4.5.1) |
| 2.3 | Day-2 callback sourced verbatim | `facts.verify_quote` and `show_canon` (4.7, 4.8) |
| 3.6 | Active day definition | Derived from `play` (≥ 50% of duration), `call_turn` (any) or `small_door`; computed by `api` on append, stored on `sessions.active_day_marked` (topology table) |
| 4 | Door states persist indefinitely | `doors.position` (topology) holds position; the events hold history |
| 5.1, 5.3, 5.4.5, 5.4.11, 5.5, 5.6, 5.7 | Everything logged | Event taxonomy 4.1.1 |
| 5.4.4 | Pause profile adapts within 1.0 to 2.5 s | `skills.pause_profile` (4.3.4) |
| 5.4.5 | Word or hint from produced-word history | `briefs.compile('salma_talkback')` returns the produced-word dict (4.9) |
| 5.4.11, 12.5.2 | Audio deleted within 15 min when storage is off; evidence kept at low confidence | `media_objects.ephemeral`, `call_turn_verbatim.low_confidence_reason` (4.1, 4.11) |
| 6.3 check 4 | Every fact used is confirmed, unexpired, not "don't bring up", quote exists | One SQL predicate, `facts_usable` view (4.7.5) |
| 7.5 | Series bible stored with the learner model | Fiction side in the pipeline domain's tables; `show_canon` here; `SeriesBibleExcerpt` compiled here (4.8) |
| 8.1 | Event log is the source of truth; models propose, code decides; live roles never write; compiled briefs | D1, D5, 4.3, 4.9 |
| 8.2 | Event fields: learner, session, door, type, time, payload, model and prompt versions, cost | `events` DDL (4.1.2) |
| 8.3 | Nine stores, writers, ranges on every estimate | 4.3 |
| 8.4 | Life-fact rules | 4.7 |
| 8.5 | Rebuilds; shown claims never retracted silently | 4.10, D14 |
| 8.6 | Compiled briefs per role | 4.9 |
| 9.4 | FSRS-style scheduler; due below 0.85 at next drop; grammar 1 to 3 days early | 4.5 |
| 9.5 | Tapped twice or more becomes a recall candidate; kept words scheduled like targets | `word_bank.tapped_n`, `kept` (4.3.1) |
| 10.4 | Inventory of a few hundred structures; 12 categories; frequency list and lemmatizer | 4.4 |
| 10.5, 10.6, 10.7 | Error vs slip; lifecycle; avoidance | 4.6 |
| 10.8 | Skills on a fine scale with ranges, CEFR words never shown unprompted | `skills` (4.3.4) |
| 10.11 | Rating model pinned per 4-week window | `learner_model_versions.code_versions` records it per write; the pin itself is `vendors.yaml` (topology) |
| 12.3 | Notebook sections | Each maps to a store or view (4.3.9) |
| 12.5 | Data rules 1 to 9 | 4.11, 4.12 |
| 12.6 | Row-level isolation; per-learner keys; no cross-learner paths except gloss cache and opt-in transcripts | RLS on every learner table (4.13); only `gloss_cache` (pipeline) and `research_transcripts` lack `learner_id` |
| 14.3 | Postgres; vector index only for past-conversation callbacks | D11 |
| 14.5, 16.1 | Cost traced per role, vendor, learner | `events.cost_usd` for events that cost money; `learner_model_version` on every adapter call via `CallMeta` |
| 15 | Teacher update within 10 min; export within 1 h; audio 15 min / 24 h; deletion 24 h / 30 days | 4.12, section 6 |
| 19.2 week 1 | Event log and learner-model schema; lexicon and scheduler | Section 7 |

Budgets that bind this domain: none of the per-session AI cost is spent here (no model calls); the domain's own cost is storage and database time (section 6). Latency: `briefs.compile('teacher')` under 5 s (pipeline's assumption; target 500 ms), `word_bank.p_understood` for a 1,500-unit script under 100 ms, learner edits applied before the response returns (under 200 ms).

---

## 3. Architecture

### 3.1 Components

Everything in this domain is one Python package, `forone.learner`, imported by `api` (append and learner edits) and `workflows` (everything else). No service of its own.

| Module | Job | Called by |
|---|---|---|
| `forone.learner.events` | `append(batch)`: validate, de-duplicate, assign `seq`, insert; `read(learner_id, since_seq)`; type registry and payload schemas | `api` (`POST /v1/events`, `POST /internal/events`), `workflows` |
| `forone.learner.versions` | `bump(learner_id, cause, code_versions) -> int` inside a caller's transaction; `current(learner_id)` | every store writer |
| `forone.learner.stores` | `apply_after_pass(AfterPassResult)`; `apply_learner_edit(event)`; the nine store writers; `rebuild(learner_id)` | `workflows` (after-pass, rebuild), `api` (learner edits) |
| `forone.learner.lexicon_db` | The `lexicon_lemmas`, `lexicon_chunks`, `structures`, `reporting_categories` tables; loaders from the language package | pipeline's `lexicon`, assessment's classifier |
| `forone.learner.word_bank` | `p_understood(unit, surface)`, `p_understood_many(units, surface)`, priors, Beta updates, owned-word rule | fitter, analyst updater, notebook |
| `forone.learner.scheduler` | py-fsrs wrapper: `review(unit, rating, weight, at)`, `retrievability(unit, at)`, `due_list(learner_id, at_drop)` | teacher brief, updater |
| `forone.learner.facts` | `verify_quote(fact_id)`, `propose(candidates)`, ladder transitions, shelf life, supersession, follow-ups, interests decay | memory keeper validator, editor check 4, notebook |
| `forone.learner.canon` | `show_canon` writes; `conversation_chunks` embed and search; `series_bible_excerpt(learner_id)` | analyst, writer brief |
| `forone.learner.briefs` | `compile(role, learner_id, scope)`, cache | pipeline (teacher, writer, host), call-worker via `api`, after-pass (Salma, chat), proof |
| `forone.learner.claims` | `record(claim)`, `mark_shown`, `invalidate`, `passed_for_proof(learner_id, week)` | claim gate (writes), proof producer, return episode, finale |
| `forone.learner.export` | Build the zip | `learner/export` step bodies |
| `forone.learner.deletion` | Ordered purge, ledger | `learner/delete` step bodies |
| `forone.learner.retention` | Trial-ended queries, orphan audits, partition creation | `retention/daily` step bodies |
| `forone.learner.pii` | The column classification as code (used by export, Langfuse scrubbing and tests) | export, tracing middleware |

### 3.2 Diagram, in text

Draw three lanes left to right: **Producers**, **The log**, **Derived**.

- Producers (left): `web` (player, article, chat, notebook, controls), `call-worker` (call turns, talkback, floor, silence), `workflows` (after-pass outputs, verbatim turns, claims shown, consent jobs). All three arrows enter one box in `api` labelled `POST /v1/events` or `POST /internal/events`, which calls `events.append`.
- The log (middle): one tall box `events` (monthly partitions drawn as shelves). Two side boxes attached to it: `learner_model_versions` (a counter with a pointer into the log: "high-water seq") and `media_objects` (topology; an arrow to S3 drawn as three buckets `media`, `voice`, `exports`, each with a `{learner_id}/` folder icon).
- Derived (right): nine boxes in a 3×3 grid: `word_bank`, `structure_map` (+ `structure_observations` beneath it), `error_profile`, `skills`, `interests`, `life_facts` (+ `follow_ups`), `goals`, `taste`, `show_canon` (+ `conversation_chunks`). Above the grid: `claims`. Below the grid: `briefs` (cache) with six outgoing arrows labelled teacher, writer, host, salma, chat, proof.
- Arrows: a thick arrow from `events` to a box `stores.apply_after_pass` (in `workflows`) that fans into the nine boxes; a thin arrow from `api` labelled `apply_learner_edit` into `life_facts`, `interests`, `goals`, `word_bank(kept)` and `claims(shown)`; a dashed loop from the nine boxes back to `events` labelled "rebuild: drop and replay" with `learner/rebuild` on it. Every arrow into a store passes through a small gate icon labelled `versions.bump`.
- A lock icon on every box on the right and on `events`: RLS by `learner_id`.

### 3.3 The four flows

**A. A session's events (write path, live).** `web` buffers events for up to 2 s and posts batches of up to 50 to `POST /v1/events` with the session cookie; the server sets `forone.learner_id` for RLS, validates each payload against its type schema, drops duplicates on `(learner_id, event_id)`, assigns `seq` from a per-connection bigserial, inserts in one statement, and returns `{accepted, duplicates, rejected[]}`. The same call computes whether the day just became active (PRD-v2 3.6) and, if so, sends `day.became_active` (topology). The worker posts through `POST /internal/events` with a service token; the payload is identical. No store is touched on this path.

**B. The after-session pass (write path, within 10 min).** The assessment domain's `session/after-pass` produces one `AfterPassResult` (4.3.0). Stage 1 (notes within 90 s) reads briefs and events only. At the end of stage 7 it calls `stores.apply_after_pass(result)`, which in one transaction: validates every life-fact candidate against the log, applies word, structure, error, skill, interest, goal, taste and canon updates, runs the scheduler for every unit touched, bumps the version with cause `after_pass`, writes a `learner_model_versions` row with the high-water `seq` and the code versions (`analyst`, `classifier`, `measures`, `memory_keeper`, `scheduler`), and returns the new version. The caller then sends `session.after_pass.completed {learner_id, session_id, learner_model_version}` (topology event).

**C. A learner edit (write path, synchronous).** `web` posts a `fact_card_edit`, `notebook_edit`, `working_on_edit`, `wrong_memory_flag` or `consent_change` event. `api` appends it and, in the same transaction, calls `stores.apply_learner_edit(event)`, which changes the one store row the edit names, bumps the version with cause `learner_edit`, and returns. For `working_on_edit` it then sends `working_on.changed`; for `consent_change` it sends `learner.consent_changed`. The response carries the new `learnerModelVersion` (the topology's cache key). This is the only store write outside `workflows`.

**D. A rebuild.** Triggered by `learner.rebuild_requested {learner_id, reason}` (new event, section 3.4) from `/admin` when a code version in `code_versions` changes, or in bulk by a script. `learner/rebuild` creates shadow copies of the nine tables for that learner (`stores_shadow` schema, same DDL), replays sessions in order by calling the assessment domain's pure functions over the stored verbatim turns and chat messages (no new vendor calls: transcripts are events), applies each result with the shadow writers, replays learner edits at their positions in the log, then swaps shadow rows for live rows in one transaction with cause `rebuild`. It compares the `claims` the new stores would support with the claims already shown; any shown claim no longer supported gets a `claim_invalidations` row (4.10). Duration: about 2 s per session of history on one worker; a learner with 100 sessions rebuilds in under 4 minutes.

### 3.4 Interfaces to other domains

Functions provided (Python, in-process):

```python
# forone/learner/api.py  (the public surface of the package; everything else is internal)
def append_events(learner_id: UUID, batch: list[EventIn], source: Source) -> AppendResult: ...
def current_version(learner_id: UUID) -> int: ...
def apply_after_pass(result: AfterPassResult) -> int: ...                 # returns new learner_model_version
def apply_learner_edit(event: Event) -> int: ...
def compile_brief(role: Role, learner_id: UUID, scope: BriefScope | None = None) -> Brief: ...
def p_understood(learner_id: UUID, unit_id: str, surface: Literal["ear","eye"]) -> float: ...
def p_understood_many(learner_id: UUID, unit_ids: list[str], surface) -> dict[str, float]: ...
def due_list(learner_id: UUID, at: datetime) -> list[DueItem]: ...
def verify_quote(fact_id: UUID) -> QuoteCheck: ...
def facts_usable(learner_id: UUID, on: date) -> list[Fact]: ...
def search_callbacks(learner_id: UUID, query: str, k: int = 5) -> list[Chunk]: ...
def record_claim(claim: ClaimIn) -> UUID: ...                              # claim gate only
def mark_claim_shown(claim_id: UUID, surface: str, event_id: UUID) -> None: ...
def passed_claims(learner_id: UUID, since: date | None) -> list[Claim]: ...
def build_export(learner_id: UUID, export_id: UUID) -> ExportManifest: ...
def purge_learner(learner_id: UUID) -> PurgeReport: ...
```

Inngest events consumed (names from the topology's catalogue unless marked new): `call.ended`, `learner.consent_changed`, `learner.export_requested`, `learner.deletion_requested`, `session.after_pass.completed` (to refresh `briefs` for the teacher ahead of the pipeline), `learner.rebuild_requested` [new: `{learner_id, reason, code_versions}`], `claim.shown` [new, sent by the surface that showed a claim: `{learner_id, claim_id, surface, event_id}`].

Inngest events emitted: `working_on.changed`, `learner.consent_changed` (relayed from the event), `learner.model_updated` [new: `{learner_id, learner_model_version, cause}`; the pipeline may use it to refresh a brief], `learner.rebuild_completed` [new: `{learner_id, from_version, to_version, invalidated_claims}`], `export.ready {learner_id, export_id}` [new], `learner.purged {learner_id}` [new].

Functions I own the step bodies of: `learner/export`, `learner/delete` (purge order), `learner/rebuild` (new), the data parts of `retention/daily` (trial-ended queries, partition creation, orphan audits).

---

## 4. Detailed design

### 4.1 The event log

#### 4.1.1 Taxonomy

Every type from PRD-v2 8.2 plus eleven this design needs (marked +). Payload fields are the Pydantic schema names; `door` is one of `listen, shadow, read, call, notes, chat, round_two, small_door, onboarding, notebook, controls, proof, feed`. "Who" is the producer: `web`, `worker` (call-worker), `wf` (workflows).

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
| `call_turn_verbatim` + | wf | call | `call_id, turn_index, text, words[] {t,s,e,c}, vendor, disfluencies_kept, low_confidence_reason|null` | analyst, classifier, measures, quote check |
| `talkback` | worker | call | `call_id, turn_index, asked_ar, lemma_asked|null, gave (word|hint), hint_kind|null, latency_ms` | word bank, talkback metric |
| `hold_floor` | worker | call | `call_id, turn_index, held_ms` | pause profile |
| `silence` | worker | call | `call_id, turn_index, silence_ms, host_action (backchannel|smaller_question|offer_wrap|none)` | anxiety mode, pause profile |
| `note_shown` | web | notes | `session_id, card (new_for_you|polish|reached_for), card_id, claim_id|null, played_clip: bool` | claims.shown, notes-opened metric |
| `say_it_once` | web | notes | `session_id, card_id, media_object_id, reference_text` | pronunciation (internal) |
| `shadow` | web | shadow | `episode_id, line_id, media_object_id, reference_text` | pronunciation, elicited imitation |
| `chat_message` | web, wf | chat | `thread_id, message_index, speaker (learner|host), text, in_reply_to|null` | analyst, canon, quote check |
| `margin_note` | wf | chat | `thread_id, message_index, structure_id, original, corrected, opened: bool` | correction layers |
| `idea_shown` | wf | chat, today | `plan_id, ideas[] {idea_id, rank, is_wildcard, from_life, arc_id}` | taste, "tomorrow chosen" metric |
| `idea_chosen` | web | chat, today | `plan_id, idea_id, source (pick|tell_salma|remix|cutoff), remix: {topic|format|cast}|null, salma_text|null` | taste, pipeline |
| `swap` | web | today | `episode_id, replaced_by_episode_id` | taste |
| `small_door` | web | small_door | `episode_id, recap_played_ms, voice_note_media_object_id|null, duration_ms` | active day, after-pass |
| `fact_card_edit` | web | notebook, onboarding | `fact_id, action (edit|remove|dont_bring_up|confirm), new_text|null` | life facts (sync) |
| `fact_card_viewed` + | web | notebook | `fact_id, dwell_ms, visit_id` | ladder promotion (4.7.2) |
| `notebook_edit` | web | notebook | `section (about_you|out_in_world|kept|goals), action (add|edit|remove), item_id|null, text|null, date|null` | goals, out-in-world (sync) |
| `working_on_edit` | web | notebook, proof | `action (veto|add|unhide|hide), item_id|null, text|null, voice_media_object_id|null` | targeting (sync), `working_on.changed` |
| `claim_shown` | wf, web | proof, notes, finale, salma | `claim_id, surface, text_shown` | claims.shown_at |
| `consent_change` | web | onboarding, controls | `kind (voice_storage|data_use|notes_mode|drop_notification|captions|gap_note), value, text_shown_version` | retention jobs (sync relay) |
| `worth_it_answer` | web | proof | `proof_id, answer (yes|mostly|no), why_text|null` | 16.2 |
| `wrong_memory_flag` | web, wf | call, chat, notebook | `fact_id|null, canon_id|null, said_by (host|salma), quote_of_show, learner_correction|null` | facts (sync), 16.1 metric |
| `onboarding_answer` + | worker, web | onboarding | `step (A1..A10), question_key, answer_text, answer_mode (voice|text), skipped: bool, english_line: bool` | intake facts, first estimate |
| `word_check_answer` + | web | onboarding | `item_id, lemma|pseudoword, band, answered_known: bool, ms` | priors (4.5.1) |
| `recording` + | web | notes, finale | `recording_id, task (retell|opinion|repeat), media_object_id, reference_text|null, kept_explicitly: bool` | then-and-now rater |
| `followed_answer` + | web | listen | `episode_id, answer (most|about_half|little)` | 16.2 against `why.predicted` |
| `host_turn_text` + | wf | chat | reserved; host chat text is `chat_message{speaker:host}`; this type exists for the small-door host reply: `episode_id, text` | canon |
| `crisis_flag` + | worker, wf | call, chat, after_pass | `source (host|salma|analyst), language, resources_shown: bool, continued: bool` | SB 243 log (security domain reads) |
| `session_closed` + | wf | any | `session_id, reason (next_published|learner_started_next|deleted)` | rebuild ordering |
| `lm_write` + | wf, api | n/a | `learner_model_version, cause, code_versions, high_water_seq` | audit; mirrors `learner_model_versions` so the log alone can be replayed |

Rules: a type not in the registry is rejected with 422 and logged; payload fields beyond the schema are kept (forward compatibility) but never read by the stores; `model_versions`, `prompt_version` and `cost_usd` are set only on events produced by a model (`call_turn{speaker:host|salma}`, `chat_message{speaker:host}`, `margin_note`, `idea_shown`, `call_turn_verbatim`) and are null otherwise.

#### 4.1.2 DDL

```sql
-- forone/learner/sql/001_events.sql
create extension if not exists pgcrypto;

create table events (
  seq               bigint generated always as identity,       -- server order; monotonic per database
  event_id          uuid not null,                             -- UUIDv7, minted by the producer
  learner_id        uuid not null references learners(id),
  session_id        uuid,                                      -- null for onboarding before the first session, controls, feed fetches
  episode_id        uuid,
  call_id           uuid,
  door              text not null,
  type              text not null,
  occurred_at       timestamptz not null,                      -- producer clock, corrected for skew (4.1.4)
  recorded_at       timestamptz not null default now(),
  source            text not null check (source in ('web','worker','wf','api','import')),
  payload           jsonb not null,
  model_versions    jsonb,                                     -- {"host":"anthropic/claude-sonnet-5.5@2026-11-20"} on model-produced events
  prompt_version    text,
  learner_model_version integer,                               -- the version a model-produced event READ
  cost_usd          numeric(8,5),
  vendor_call_id    uuid,                                      -- cost domain's vendor_calls.id
  inngest_run_id    text,
  primary key (learner_id, event_id, occurred_at),             -- partition key must be in the PK
  check (jsonb_typeof(payload) = 'object')
) partition by range (occurred_at);

-- Partitions are created three months ahead by retention/daily (topology). Naming: events_2026_11.
create table events_2026_11 partition of events for values from ('2026-11-01') to ('2026-12-01');
create table events_2026_12 partition of events for values from ('2026-12-01') to ('2027-01-01');
create table events_2027_01 partition of events for values from ('2027-01-01') to ('2027-02-01');

create index events_learner_time on events (learner_id, occurred_at, seq);
create index events_learner_type on events (learner_id, type, occurred_at);
create index events_session on events (session_id, occurred_at) where session_id is not null;
create index events_call on events (call_id, (payload->>'turn_index')) where call_id is not null;
create index events_seq on events (seq);

-- Append-only: the application roles cannot update or delete; a trigger guards even the owner.
revoke update, delete, truncate on events from forone_app, forone_workflows;
create or replace function events_immutable() returns trigger language plpgsql as $$
begin
  if current_setting('forone.purge_mode', true) is distinct from 'on' then
    raise exception 'events is append-only (set forone.purge_mode=on only inside learner/delete)';
  end if;
  return old;
end $$;
create trigger events_no_update before update or delete on events
  for each row execute function events_immutable();

-- Row-level security: every learner-facing query sees one learner.
alter table events enable row level security;
create policy events_by_learner on events
  using (learner_id = current_setting('forone.learner_id', true)::uuid);
create policy events_service on events to forone_workflows using (true);
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

- `event_id` is a UUIDv7 minted by the producer at the moment the event happens (the PWA, the worker, or the workflow step). The time prefix makes it sortable and lets the server reject ids more than 7 days old or in the future.
- Uniqueness is `(learner_id, event_id)`; the primary key includes `occurred_at` only because Postgres requires the partition key in it. A duplicate is detected before insert with `on conflict do nothing` and reported in `AppendResult.duplicates`; it is never an error, because the offline queue and worker retries will send duplicates by design.
- For events the workflow produces inside a retried step, the step derives `event_id` deterministically: `uuid5(namespace, f"{run_id}:{step}:{key}")`, so a retry appends nothing new.
- Batches are atomic per request: either every non-duplicate row is inserted or none.

#### 4.1.4 Ordering

- `occurred_at` is the producer's clock. `api` compares it to its own clock at receipt: if the skew is over `events.client_clock_skew_max_s` (300 s) and the batch is not an offline replay (`X-Forone-Replay: 1` header carrying the queue's original timestamps), `occurred_at` is replaced by `recorded_at` and the event is flagged `payload._clock_corrected=true`.
- Within one learner, replay order is `(occurred_at, seq)`. `seq` breaks ties and preserves arrival order for events with equal timestamps (the worker emits `call_turn` and `silence` at the same millisecond).
- Cross-learner order does not matter anywhere.
- The after-session pass is triggered by `call.ended`/`chat.closed` and reads whatever events have arrived by the time its stage runs; an event that arrives after the pass (an offline replay a day later) is folded in by the next pass or by a rebuild. That is why stores are rebuildable rather than exactly-once.

#### 4.1.5 Retention

Events are kept for the life of the account (they are the learner's data and the only source of rebuilds). On deletion, the learner's rows are removed from every partition (4.12). Months older than 24 months may be moved to cheaper storage later; nothing in the beta does this. [ASSUMPTION] At 10,000 learners, about 300 events per session and 20 sessions a month, the table grows by about 60M rows (about 60 GB with payloads) a month; that is ordinary for RDS with monthly partitions and is addressed in section 6.

#### 4.1.6 Example rows

```json
{ "event_id": "0192f3c1-4b1e-7a63-8d2c-2b5d1e7f0a11", "learner_id": "7d0b...", "session_id": "c4e9...", "episode_id": "a1f2...",
  "door": "listen", "type": "huh", "occurred_at": "2026-12-09T07:52:14.310+03:00", "source": "web",
  "payload": { "episode_id": "a1f2...", "line_id": "s2-l07", "sentence_text": "The referee robbed us, and not for the first time.",
               "unit_ids": ["referee", "rob", "not_for_the_first_time"] } }

{ "event_id": "0192f3c4-9a02-7b11-9f0e-7c1d2a3b4c5d", "learner_id": "7d0b...", "session_id": "c4e9...", "call_id": "e77a...",
  "door": "call", "type": "call_turn", "occurred_at": "2026-12-09T08:03:41.120+03:00", "source": "worker",
  "payload": { "call_id": "e77a...", "turn_index": 6, "speaker": "learner", "text_stream": "I went to the match with my cousin and we was late",
               "started_ms": 61230, "ended_ms": 66010, "words_stream": [{"t":"I","s":61230,"e":61300,"c":0.98}, "..."], "recast": null,
               "clarification": false, "nudge": false, "recall_gap_id": null, "mode": "live" } }

{ "event_id": "0192f3c6-1c40-7c22-a1b2-3c4d5e6f7a8b", "learner_id": "7d0b...", "session_id": "c4e9...", "call_id": "e77a...",
  "door": "call", "type": "call_turn_verbatim", "occurred_at": "2026-12-09T08:03:52.004+03:00", "source": "wf",
  "model_versions": {"verbatim_stt": "assemblyai/universal-3.6@2026-11-10"}, "cost_usd": 0.00061, "vendor_call_id": "5f3e...",
  "payload": { "call_id": "e77a...", "turn_index": 6, "text": "I went to the- I go, I went to the match with my cousin and, uh, we was late",
               "words": [{"t":"I","s":61230,"e":61298,"c":0.97}, {"t":"went","s":61310,"e":61520,"c":0.91}, "..."],
               "vendor": "assemblyai", "disfluencies_kept": true, "low_confidence_reason": null } }
```

### 4.2 Learner-model versioning

```sql
create table learner_model_versions (
  learner_id        uuid not null references learners(id) on delete cascade,
  version           integer not null,
  cause             text not null check (cause in ('onboarding','after_pass','learner_edit','consent','rebuild','retention','import','admin')),
  session_id        uuid,
  high_water_seq    bigint not null,                 -- last events.seq folded into the stores by this write
  code_versions     jsonb not null,                  -- {"analyst":"1.3.0","classifier":"1.1.2","measures":"1.0.4","memory_keeper":"1.2.0","scheduler":"fsrs-4.5/w-default","rater_pin":"claude-sonnet-5.5@2026-12-01"}
  stores_touched    text[] not null,
  created_at        timestamptz not null default now(),
  primary key (learner_id, version)
);
-- the current version is max(version); cached on learners.lm_version for cheap reads
alter table learners add column lm_version integer not null default 0;
```

```python
# forone/learner/versions.py
def bump(conn, learner_id, cause, *, session_id=None, stores_touched, code_versions) -> int:
    """Must run inside the caller's transaction. Serializes writers per learner with a row lock."""
    row = conn.execute(text("select lm_version from learners where id=:l for update"), {"l": learner_id}).one()
    new = row.lm_version + 1
    hw = conn.execute(text("select coalesce(max(seq),0) from events where learner_id=:l"), {"l": learner_id}).scalar()
    conn.execute(text("""insert into learner_model_versions(learner_id, version, cause, session_id, high_water_seq, code_versions, stores_touched)
                         values (:l,:v,:c,:s,:hw,:cv,:st)"""), dict(l=learner_id, v=new, c=cause, s=session_id, hw=hw,
                         cv=json.dumps(code_versions), st=stores_touched))
    conn.execute(text("update learners set lm_version=:v where id=:l"), {"v": new, "l": learner_id})
    append_event(conn, learner_id, type="lm_write", door="n/a", source="wf" if cause != "learner_edit" else "api",
                 payload={"learner_model_version": new, "cause": cause, "code_versions": code_versions, "high_water_seq": hw})
    return new
```

Where the version is recorded: `briefs.learner_model_version`; `CallMeta.learner_model_version` on every adapter call (topology 4.5), so `vendor_calls` and Langfuse carry it; `events.learner_model_version` on model-produced events; `claims.learner_model_version`; `episodes.model_versions` already exists, and the pipeline's `EpisodePlan.learner_model_version` is the string form `lm_v_{n}`. The string form is only for serialization; comparisons use the integer.

### 4.3 The nine stores

Every store table has `learner_id`, `lm_version` (the version of the write that last touched the row), `updated_at`, RLS as in 4.1.2, and an index starting with `learner_id`. Every estimate is stored as parameters from which a range follows (Beta for probabilities, mean and standard deviation for scales), never as a bare point.

#### 4.3.0 The write contract from the after-session pass

```python
# forone/learner/contracts.py (consumed from the assessment domain; this is the only way stores change after a session)
class AfterPassResult(BaseModel):
    learner_id: UUID; session_id: UUID; call_ids: list[UUID]; chat_thread_ids: list[UUID]
    code_versions: dict[str, str]                      # analyst, classifier, measures, memory_keeper, rater_pin
    word_evidence: list[WordEvidence]                  # {unit_id, surface: ear|eye|prod, kind: EvidenceKind, event_id, sentence: str|None, prompted: bool|None, confidence: float}
    structure_observations: list[StructureObs]        # {structure_id, obligatory: bool, correct: bool, prompted: bool, event_id, quote, confidence, blurred_meaning: bool, category}
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

`stores.apply_after_pass` applies these in the order: facts (validator first, because a rejected candidate must not reach canon), words, structures, errors, skills, interests, goals, taste, canon, scheduler, counts; then `versions.bump`.

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
  fsrs              jsonb not null,                -- {state, stability, difficulty, due, last_review, reps, lapses, elapsed_days, scheduled_days}
  lm_version        integer not null, updated_at timestamptz not null default now(),
  primary key (learner_id, unit_id)
);
create index word_bank_due on word_bank (learner_id, ((fsrs->>'due')::timestamptz));
create index word_bank_status on word_bank (learner_id, status);
```

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

Rebuild: delete the learner's rows; for every `tap`, `huh`, `keep`, `play` completion, `talkback`, and every `word_evidence` the replayed after-pass yields, re-apply 4.5.2 in log order. Deterministic given the same `scheduler` version.

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

-- the 14-day accuracy window is a view, never a stored counter (PRD-v2 8.3, 10.6)
create view structure_acc_14d as
select learner_id, structure_id,
       count(*) filter (where obligatory) as contexts,
       count(*) filter (where obligatory and correct) as correct,
       count(distinct session_id) filter (where obligatory) as sessions,
       count(*) filter (where obligatory and clean) as clean_contexts
from structure_observations
where observed_at > now() - interval '14 days'
group by learner_id, structure_id;
```

Example `structure_map` row:

```json
{ "learner_id": "7d0b...", "structure_id": "egp:past_simple_irregular_narrative", "state": "attempting", "target_lifecycle": "active",
  "avoidance": false, "heard_n": 47, "consecutive_targeted": 2, "targeted_sessions": ["c4e9...", "d10a..."],
  "examples": [{"text": "I went to the match with my cousin", "session_id": "c4e9...", "event_id": "0192f3c6..."}],
  "fsrs": {"state": "learning", "stability": 2.1, "difficulty": 6.2, "due": "2026-12-11T04:40:00Z", "reps": 2, "lapses": 1}, "lm_version": 61 }
```

Rebuild: delete observations and map rows; re-insert observations from the replayed pass (ids are deterministic); recompute the map by running 4.6 over observations in time order.

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
  lm_version integer not null, updated_at timestamptz not null default now()
);
create table skill_snapshots (                      -- weekly and at every recording; the then-and-now and re-anchoring read these
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
  topic_label  text not null, topic_label_ar text,
  salience     real not null,                      -- 0..1, decays (4.7.6)
  depth        text not null default 'curious' check (depth in ('curious','fan','expert')),
  source       text not null check (source in ('told','behavior','intake','waitlist')),
  last_engaged_at timestamptz not null, dormant boolean not null default false,
  hard_dislike boolean not null default false, no_go boolean not null default false,  -- no_go = "never bring up" (topic form)
  quote text, quote_event_id uuid,
  lm_version integer not null, updated_at timestamptz not null default now(),
  primary key (learner_id, topic_key)
);
```

#### 4.3.6 Life facts and follow-ups (memory keeper; learner edits)

```sql
create table life_facts (
  fact_id           uuid primary key,
  learner_id        uuid not null references learners(id) on delete cascade,
  fact_type         text not null references fact_shelf_life(fact_type),
  text              text not null,                 -- the fact in Salma's words, Arabic or English as said
  quote             text not null,                 -- the learner's exact words
  quote_event_id    uuid not null,                 -- the call_turn_verbatim, chat_message or onboarding_answer event
  session_id        uuid, said_at timestamptz not null,
  confidence        text not null check (confidence in ('heard_once','usable','ground_truth')),
  confirmed_by      text check (confirmed_by in ('repeated','asked','viewed_unedited','edited','intake_card')),
  confirmed_at      timestamptz, repeat_event_id uuid,
  sensitivity       text check (sensitivity in ('health','money','relationships','religion','politics')),
  sensitive_usable_until date,                     -- end of the ISO week in which it was raised (PRD-v2 5.1 "that week")
  status            text not null default 'active' check (status in ('active','dormant','superseded','deleted')),
  valid_from        date not null, expires_at date,
  dont_bring_up     boolean not null default false,
  supersedes_fact_id uuid references life_facts(fact_id), superseded_by_fact_id uuid,
  dated_event_on    date,                          -- for follow-ups
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

create table fact_shelf_life (                     -- language-package configuration, loaded at deploy
  fact_type text primary key, shelf_days int, sensitive_default boolean not null default false, label_ar text not null
);
insert into fact_shelf_life values
 ('job', 270, false, 'العمل'), ('study', 270, false, 'الدراسة'), ('city', 365, false, 'المدينة'), ('person', 365, false, 'شخص'),
 ('plan_dated', null, false, 'موعد'), ('trip', 60, false, 'سفر'), ('this_week', 7, false, 'هذا الأسبوع'),
 ('possession', 180, false, 'شي يملكه'), ('preference', 120, false, 'تفضيل'), ('routine', 120, false, 'عادة'),
 ('health', 14, true, 'صحة'), ('money', 60, true, 'مال'), ('relationship', 90, true, 'علاقة'), ('religion', 365, true, 'دين'), ('politics', 30, true, 'سياسة');
```

Example rows:

```json
{ "fact_id": "f-8821", "learner_id": "7d0b...", "fact_type": "plan_dated", "text": "مقابلة عمل لمنصب إقليمي", "quote": "I have an interview in six weeks for a regional role",
  "quote_event_id": "0192f2a0-...", "session_id": null, "said_at": "2026-12-07T19:12:40+03:00", "confidence": "ground_truth", "confirmed_by": "intake_card",
  "confirmed_at": "2026-12-07T19:13:05+03:00", "sensitivity": null, "status": "active", "valid_from": "2026-12-07", "expires_at": null,
  "dont_bring_up": false, "dated_event_on": "2027-01-18", "times_used": 3, "lm_version": 3 }

{ "fact_id": "f-9102", "learner_id": "7d0b...", "fact_type": "person", "text": "مديره الجديد صارم", "quote": "my new manager is strict, like really strict",
  "quote_event_id": "0192f3c9-...", "session_id": "c4e9...", "said_at": "2026-12-09T08:05:30+03:00", "confidence": "heard_once", "confirmed_by": null,
  "sensitivity": null, "status": "active", "valid_from": "2026-12-09", "expires_at": "2027-12-09", "people": {"name_used": "my manager", "relation": "manager"}, "lm_version": 61 }

{ "follow_up_id": "fu-31", "learner_id": "7d0b...", "fact_id": "f-8821", "due_on": "2027-01-19", "state": "pending", "lm_version": 3 }
```

#### 4.3.7 Goals (Salma's after-session pass; the learner)

```sql
create table goals (
  goal_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  kind text not null check (kind in ('can_do','season_goal','why_english')),
  text text not null, text_ar text, quote text, quote_event_id uuid,
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
  canon_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  kind text not null check (kind in ('position_learner','position_host','thing_said','joke_used','callback_made','retold')),
  who text not null check (who in ('learner','karim','mona','salma')),
  text text not null, quote text, event_id uuid, episode_id uuid, session_id uuid,
  topic_key text, at timestamptz not null,
  lm_version integer not null
);
create index canon_learner_topic on show_canon (learner_id, topic_key, at desc);

-- learner-visible counts: the only numbers the notebook shows; monotonic by construction (recomputed, never decremented in the UI contract)
create table notebook_counts (
  learner_id uuid primary key references learners(id) on delete cascade,
  words_owned int not null default 0, hours_heard_s bigint not null default 0, hours_spoken_s bigint not null default 0,
  lm_version integer not null, updated_at timestamptz not null default now()
);
```

Hours heard (PRD-v2 12.3): the sum of app playback from `play`/`pause`/`seek` intervals, plus each feed episode's full duration once when a `call_turn`, `chat_message` or `small_door` for that episode exists and no app `play` reached 50%. Hours spoken: learner `call_turn` durations plus `say_it_once`, `shadow`, `small_door` voice notes and recordings. A rebuild recomputes both; if a rebuild would lower a count (it cannot, except after a bug) the UI keeps the higher value and the difference is logged.

Notebook sections as reads: *What I'm working on* = `working_on` items (held in the pipeline's current `EpisodePlan.targets` filtered by `error_profile.status <> 'dropped_by_learner'`, with one `examples[0]` sentence each; the `working_on_items` view joins them); *About you* = `life_facts` (all statuses but `deleted`, with `confidence` rendered as "I think..." for `heard_once`), `interests`, `goals`; *Words you own* = `word_bank where status='owned'` with `own_sentences[0]` and the clip from the sentence's `event_id`; *The tape* = `recording` events [P1]; *Out in the world* = `out_in_world` rows (below); *Kept words and marked moments* = `word_bank.kept` and `mark` events; *Hours* = `notebook_counts`; *Why this episode* = the pipeline's `episode_artifacts(kind='why')`.

```sql
create table out_in_world (
  item_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  text text not null, quote text, event_id uuid, on_date date not null, added_by text not null check (added_by in ('learner','salma')),
  lm_version integer not null
);
```

### 4.4 Lexicon and inventory tables (language package, loaded into Postgres)

```sql
create table lexicon_lemmas (
  lang text not null, lemma text not null, pos text, rank int not null, zipf real not null,
  is_function boolean not null default false, source text not null,   -- 'wordfreq-en-3.x' in the beta; a subtitle list later
  primary key (lang, lemma)
);
create index lexicon_rank on lexicon_lemmas (lang, rank);

create table lexicon_chunks (
  lang text not null, chunk_id text not null, lemma_seq text[] not null, surface_example text not null, rank int,
  primary key (lang, chunk_id)
);

create table structures (
  structure_id text primary key,                   -- 'egp:past_simple_irregular_narrative'
  lang text not null, label_en text not null, label_ar text not null,
  category text not null references reporting_categories(category),
  cefr_band text not null check (cefr_band in ('A1','A2','B1','B2','C1')),
  expected_from_scale real not null,               -- internal scale value from which the structure is "expected" (avoidance check)
  learnability text not null check (learnability in ('rule','item')),
  contrast_group text,                             -- 'past_vs_present_perfect'
  source_ref text, package_version text not null
);
create table reporting_categories (category text primary key, label_en text not null, label_ar text not null, sort int not null);
insert into reporting_categories values
 ('tense_aspect','verb tense and aspect','زمن الفعل',1), ('sv_agreement','subject-verb agreement','مطابقة الفعل والفاعل',2), ('articles','articles','أدوات التعريف',3),
 ('prepositions','prepositions','حروف الجر',4), ('word_order','word order','ترتيب الكلمات',5), ('word_choice','word choice','اختيار الكلمة',6),
 ('plurals','plurals','الجمع',7), ('pronouns','pronouns','الضمائر',8), ('comparatives','comparatives','المقارنة',9),
 ('conditionals','conditionals','الجمل الشرطية',10), ('questions','question formation','تكوين السؤال',11), ('register','register','مستوى اللغة',12);
```

Loaders: `python -m forone.learner.lexicon_db load --package ar-en --version 2026.11.1` reads the package's `lexicon/wordfreq_en.tsv`, `chunks.tsv`, `structures.yaml` and upserts; the package version is recorded in `learner_model_versions.code_versions.package`. Size: about 60,000 lemmas, 300 to 400 chunks, 250 to 350 structures (PRD-v2 10.4 "a few hundred"). The word-check items (36 lemmas in six bands plus 12 pseudowords) and the then-and-now bank are package files, not tables.

### 4.5 Word probabilities and the review scheduler (code)

#### 4.5.1 Priors

For an unseen unit, `p0 = clip(sigmoid((size_est - rank) / (0.35 * size_est)), 0.02, 0.98)` (the pipeline document states this shape; it is owned here). `size_est` comes from the word check: `hits - false_alarms` per band maps to a families estimate by the package's band table; no word check or fewer than 12 answers gives the B1 default `prior.size_default = 3000` with `size_sd = 1200`. Chunks use the rank of their rarest content lemma plus 2,000. Stored as a Beta with concentration `prior.k = 4`: `a = p0 * 4`, `b = (1 - p0) * 4`, so two taps outweigh the prior and ten uneventful hearings are needed to move it far. The eye prior equals the ear prior plus 0.05 (reading is easier for this learner profile, PRD-v2 1.4); the produced prior is `p0 * 0.6`.

#### 4.5.2 Evidence to Beta updates

| Evidence (event or after-pass kind) | ear (Δa, Δb) | eye (Δa, Δb) | prod (Δa, Δb) | FSRS rating, weight |
|---|---|---|---|---|
| `tap` on transcript or Huh? sheet | (0, +2) | (0, +1) | | Again, 1.0 |
| `tap` on article | (0, +1) | (0, +2) | | Again, 1.0 |
| `huh` on a sentence containing the unit (per unit, diluted by units in sentence) | (0, +0.5) | | | Hard, 0.5 |
| Heard in a completed episode (≥ 90% played), no tap | (+0.15, 0) | | | Good, 0.2 |
| Read in an article scrolled to the end, no tap | | (+0.15, 0) | | Good, 0.2 |
| Content uptake 2 on a call that reused the unit | (+0.5, 0) | | | Good, 0.5 |
| Produced correctly, prompted (recall gap completed, Salma gave it) | (+1, 0) | | (+1, 0) | Good, 1.0 |
| Produced correctly, unprompted | (+2, 0) | (+1, 0) | (+2, 0) | Easy, 1.0 |
| Produced incorrectly (word choice error on this unit) | | | (0, +1.5) | Again, 1.0 |
| `talkback` asked for this unit | (0, +0.5) | | (0, +1) | Again, 0.7 |
| `keep` | none | none | none | state unchanged; `kept=true` and the unit enters the due list regardless of R |

Weight is applied as a fractional review: the FSRS update is computed for the rating and the new stability is `S' = S + w * (S_fsrs - S)`. Ranges: `p_low, p_high` are the Beta 10% and 90% quantiles. Time: when `last_seen_at` is older than 30 days, `p_understood` returns `mean * max(R(now), 0.6)`, so a word unused for months is treated as shaky again (the personalization lens's rule) without a separate decay model.

#### 4.5.3 The scheduler

```python
# forone/learner/scheduler.py
from fsrs import Scheduler, Card, Rating, State       # py-fsrs (MIT); weights = FSRS-4.5 defaults until we fit our own
_s = Scheduler(desired_retention=0.85)               # PRD-v2 9.4: due = predicted recall below 0.85

STRUCTURE_EARLY_CAP_DAYS = (1, 3)                    # grammar targets spaced tightly early (PRD-v2 9.4.3)

def review(card: Card, rating: Rating, weight: float, at: datetime, is_structure: bool) -> Card:
    new, _log = _s.review_card(card, rating, review_datetime=at)
    if weight < 1.0:                                 # fractional review for weak evidence
        new.stability = card.stability + weight * (new.stability - card.stability) if card.stability else new.stability
        new.due = at + timedelta(days=_s.next_interval(new.stability))
    if is_structure and new.reps <= 3:
        lo, hi = STRUCTURE_EARLY_CAP_DAYS
        new.due = at + timedelta(days=min(max((new.due - at).days, lo), hi))
    return new

def retrievability(card: Card, at: datetime) -> float:
    if card.state == State.New or not card.stability: return 0.0
    t = max((at - card.last_review).total_seconds() / 86400, 0)
    return (1 + t / (9 * card.stability)) ** -1       # FSRS forgetting curve

def due_list(conn, learner_id, at_drop: datetime) -> list[DueItem]:
    """Everything whose predicted recall at the next drop is below 0.85, plus kept words and active structure targets."""
    rows = conn.execute(text("""
      select 'word' as kind, unit_id as id, fsrs, kept, status from word_bank where learner_id=:l and status <> 'unseen'
      union all
      select 'structure', structure_id, fsrs, false, state from structure_map where learner_id=:l and state <> 'not_seen'"""), {"l": learner_id})
    out = []
    for r in rows:
        card = Card.from_dict(r.fsrs); R = retrievability(card, at_drop)
        if R < 0.85 or r.kept:
            out.append(DueItem(kind=r.kind, id=r.id, p_recall_at_drop=R, stability=card.stability, last_seen=card.last_review, kept=r.kept))
    return sorted(out, key=lambda d: d.p_recall_at_drop)[:60]   # the teacher never needs more than 60 candidates
```

The due list is computed at brief-compile time, not by a cron: it depends on the next drop time, which `learner_schedule` knows. Own weights: once 2,000 reviews per learner cohort exist (about month 3), fit FSRS weights on `events` with the optimizer in the same library and record the weights under `code_versions.scheduler`.

#### 4.5.4 Words owned

A unit becomes `owned` when `produced_sessions` holds two distinct sessions whose `occurred_at` differ by at least 24 h, both unprompted and correct (PRD-v2 10.6). `owned_at` is the second session's time. This is the one word-level fact the claim gate may use without a standard error (PRD-v2 10.10 "words-owned claims").

### 4.6 Structure lifecycle (PRD-v2 10.5, 10.6, 10.7)

`state` moves on observations, `target_lifecycle` moves on the teacher's decisions and on confirmations; both are computed by `structures.step(map_row, observations, now)` after every pass and on rebuild.

| From | To | Rule (code) |
|---|---|---|
| `not_seen` | `heard` | `heard_n >= 1` (the publisher reports realized counts per structure from the fitter report; the pipeline domain sends them in `episode.ready.artifacts.realized_structures`) [ASSUMPTION] |
| `heard` | `attempting` | first observation with `obligatory = true` (correct or not) |
| `attempting` | `taking` | two observations `correct and not prompted and clean` in two different sessions, at least one of them ≥ 24 h after `last_targeted_session_id`'s time (or never targeted) |
| `taking` | `stable` | over `structure_acc_14d`: `contexts >= 5 and sessions >= 2 and correct / contexts >= 0.8` with the window spanning ≥ 14 days; sets `stable_at`, `recheck_due_at = stable_at + 14 days` |
| `stable` | `stable` (confirmed) | the assessment domain's recording rater reports the structure held in the next then-and-now recording: `stable_confirmed_at` set; `error_profile.status = 'resolved'` |
| `stable` | `attempting` | a re-check at 2, 4 or 8 weeks (`recheck_due_at`) finds `correct / contexts < 0.8` in the 14 days before the check with `contexts >= 3`; `target_lifecycle = 'active'` again |
| any | `avoidance = true` | weekly (inside the first after-pass of each ISO week): `expected_from_scale <= skills.speaking.mean` and `state in ('not_seen','heard')` and the learner has had ≥ 5 sessions; cleared on the first `attempting` |

`target_lifecycle`: `active` when the current `EpisodePlan.targets.grammar.structure_id` is this structure (the pipeline's publish step calls `stores.mark_targeted(learner_id, structure_id, session_id)`, which also increments `consecutive_targeted`, reset to 0 when a plan targets something else); `taking`, `stable`, `recheck` mirror `state`; `dropped_by_learner` on a veto. "Learned" for any claim text means `taking` or later, which by construction is "correct, unprompted, a day later, in a different session".

### 4.7 Life facts: the validator, the ladder and time

#### 4.7.1 The quote check

```python
# forone/learner/facts.py
AR_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭ]")
def normalize(s: str) -> str:
    s = s.lower(); s = AR_DIACRITICS.sub("", s)
    s = s.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ة","ه").replace("ى","ي")
    s = re.sub(r"[^\w\s]", " ", s); return re.sub(r"\s+", " ", s).strip()

QUOTE_SOURCES = ("call_turn_verbatim", "chat_message", "onboarding_answer", "small_door_voice_verbatim")

def verify_quote(conn, learner_id, quote: str, quote_event_id: UUID) -> QuoteCheck:
    ev = conn.execute(text("select type, payload from events where learner_id=:l and event_id=:e"), {"l": learner_id, "e": quote_event_id}).one_or_none()
    if ev is None or ev.type not in QUOTE_SOURCES: return QuoteCheck(ok=False, reason="no_source_event")
    if ev.type == "chat_message" and ev.payload.get("speaker") != "learner": return QuoteCheck(ok=False, reason="not_learner_speech")
    hay = normalize(ev.payload.get("text") or ev.payload.get("answer_text") or "")
    ok = normalize(quote) in hay and len(normalize(quote).split()) >= 2
    low_conf = ev.type == "call_turn_verbatim" and ev.payload.get("low_confidence_reason")
    return QuoteCheck(ok=ok and not low_conf, reason=None if ok else ("quote_not_in_transcript" if not low_conf else "low_confidence_region"))
```

A candidate whose quote fails is dropped and counted (`facts.rejected_total` metric); the memory keeper never gets a second chance to "fix" the quote. A quote from a streaming `call_turn` is never accepted: only verbatim text, chat text and onboarding answers (PRD-v2 8.4.1). The editor's check 4 (pipeline domain) calls the same function.

#### 4.7.2 The confidence ladder

| Rung | Set when | May be spoken by a host or Salma? | Notebook shows |
|---|---|---|---|
| `heard_once` | Candidate passed the quote check, first time this fact (by `fact_type` + normalized `text` similarity ≥ 0.85, computed with `pg_trgm`) | No | "I think..." (أظن...) with the quote and date |
| `usable` | (a) a second candidate matching the same fact arrives from a different `session_id` (`confirmed_by='repeated'`, `repeat_event_id` set); (b) Salma asked and the learner confirmed in the same session (`confirmed_by='asked'`, the analyst marks `confirmed_in_session`); (c) a `fact_card_viewed` with `dwell_ms >= 4000` and no `fact_card_edit` for that fact in the same `visit_id` within 10 minutes (`confirmed_by='viewed_unedited'`); (d) an intake card at A3 left standing when A3 ends (`confirmed_by='intake_card'`) | Yes | Plain |
| `ground_truth` | `fact_card_edit{action: edit|confirm}` or `wrong_memory_flag` with a `learner_correction` | Yes | Plain, with "you edited this" |

Rule (c) is applied by a small step at the end of each notebook visit (`api` receives `fact_card_viewed` events in the batch; `apply_learner_edit` handles the promotion when the visit's last event is older than 10 minutes, or the next after-pass does). Demotion never happens automatically; `fact_card_edit{remove}` sets `status='deleted'`, `dont_bring_up` sets the flag and keeps the fact (PRD-v2 12.3).

#### 4.7.3 Sensitivity

A candidate with `sensitivity` set (the memory keeper proposes the class; code also forces the class from `fact_shelf_life.sensitive_default`) is stored only if `confirmed_in_session = true`; otherwise it is discarded and only the transcript keeps it. Stored sensitive facts get `sensitive_usable_until` = the Sunday ending the ISO week of `said_at` (Saudi weeks start Sunday; use the learner's local calendar) and are excluded from `facts_usable` after that date; they are never offered to the teacher as a callback or idea source (`facts_usable` returns them with `may_initiate = false`; the teacher's prompt rule "never brought up first" is enforced by filtering them out of `facts_allowed` unless the idea's topic came from the learner's own `idea_chosen{source:'tell_salma'}` in the same week). Nothing in this domain ever sets a sensitivity class from inference: the class comes only with a quote.

#### 4.7.4 Time: shelf life, supersession, follow-ups

- `expires_at = valid_from + fact_shelf_life.shelf_days` unless the type has `null` (dated plans expire the day after `dated_event_on`). Expired facts are `status='dormant'`: kept, shown in the notebook under "earlier", never spoken.
- Supersession: a new candidate with the same `fact_type` and a `supersedes_hint` or the same `people.relation` (new job, moved city) sets the old row `status='superseded', superseded_by_fact_id=new` and the new row `supersedes_fact_id=old`; `facts_usable` exposes `history: [old.text]` so the writer can say "how's the new job?".
- Follow-ups: when a stored fact has `dated_event_on`, one `follow_ups` row is created with `due_on = dated_event_on + 1 day`; the teacher's `follow_ups_due` includes rows with `state='pending' and due_on <= next drop date`; the pipeline marks `used` with the episode id; `expired` after 21 days unused; `cancelled` if the fact is deleted.

#### 4.7.5 What "usable" means in one predicate

```sql
create view facts_usable as
select f.*, (f.sensitivity is null) as may_initiate,
       (select text from life_facts h where h.fact_id = f.supersedes_fact_id) as history_text
from life_facts f
where f.status = 'active' and f.confidence in ('usable','ground_truth') and f.dont_bring_up = false
  and (f.expires_at is null or f.expires_at >= current_date)
  and (f.sensitivity is null or f.sensitive_usable_until >= current_date);
```

The editor's check 4 is: every `fact_id` in the package's `facts_used` exists in `facts_usable` for that learner on the publish date and `verify_quote` passes for each.

#### 4.7.6 Interests decay

After every pass: `salience = salience * exp(-days_since_last_engaged / interests.decay_tau_days)` with τ = 21; `dormant = salience < 0.2`; any `interest_signal` with `kind in ('mentioned','talked_long','chose')` sets `salience = min(1, salience + strength)` and `dormant=false` at once (PRD-v2 8.4.6). `hard_dislike` and `no_go` never decay.

#### 4.7.7 Corrections and learner edits (synchronous)

`apply_learner_edit` handles: `wrong_memory_flag` (sets the named fact `status='deleted'` if no correction, or `ground_truth` with the corrected text if `learner_correction` present; increments `learners.wrong_memory_n` for the 16.1 metric); `fact_card_edit`; `notebook_edit`; `working_on_edit` (writes `error_profile.status='dropped_by_learner'` for a veto, or inserts a `working_on_additions` row `{text, voice_transcript, at}` that the teacher turns into structures the same evening; emits `working_on.changed`); `consent_change` (writes `consents`, below, and relays `learner.consent_changed`). Each bumps the version with cause `learner_edit`.

```sql
create table consents (
  learner_id uuid primary key references learners(id) on delete cascade,
  voice_storage boolean not null default false, voice_storage_at timestamptz,
  data_use boolean not null default false, data_use_at timestamptz,
  notes_mode text not null default 'always' check (notes_mode in ('always','when_it_matters','never')),
  drop_notification boolean not null default true, captions boolean not null default true,
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

The security domain owns the consent copy and semantics; this table is where the flags live and `media_objects.ephemeral` is derived from `consents.voice_storage` at call start (topology's `audio/expire`).

### 4.8 Show canon and the callback index

`show_canon` rows (4.3.9) are written from `AfterPassResult.canon` and from the publisher (the pipeline sends `canon_from_episode: [{kind:'position_host', who, text, episode_id}]` in `episode.ready.artifacts` [ASSUMPTION]). The writer's `SeriesBibleExcerpt` is compiled here: the pipeline's fiction tables (`side_characters`, `running_jokes`, `arcs`, `seasons`, last 5 `episodes`) joined with the last 30 canon rows and the top 10 by `topic_key` match to the idea.

```sql
create extension if not exists vector;
create table conversation_chunks (
  chunk_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  source text not null check (source in ('call','chat','small_door','onboarding')),
  session_id uuid, call_id uuid, thread_id uuid, first_event_id uuid not null, last_event_id uuid not null,
  spoken_at timestamptz not null, text text not null,               -- about 3 learner turns + the host turn before them, 60 to 120 words
  embedding vector(1536) not null, embed_model text not null,
  lm_version integer not null
);
create index chunks_learner_time on conversation_chunks (learner_id, spoken_at desc);
-- no ANN index in the beta (D11): exact search per learner
```

```python
def search_callbacks(conn, learner_id, query, k=5):
    q = embed([query])[0]
    return conn.execute(text("""select chunk_id, session_id, spoken_at, text, 1 - (embedding <=> :q) as score
                                from conversation_chunks where learner_id=:l order by embedding <=> :q limit :k"""),
                        {"l": learner_id, "q": q, "k": k}).all()
```

Chunks are embedded in the after-pass (one embedding call per session, about 10 chunks, under $0.0005). Callbacks the teacher proposes must cite a `chunk_id` or a `canon_id`; the pipeline's `callback.quote` is then checked with `verify_quote` against `first_event_id..last_event_id`. When a learner passes `callbacks.exact_search_max_chunks = 20000` (not in year one), add a partial HNSW index for that learner; the code path does not change.

### 4.9 Compiled briefs and their cache

```sql
create table briefs (
  learner_id uuid not null references learners(id) on delete cascade,
  role text not null check (role in ('teacher','writer','host','salma_talkback','salma_notes','chat_host','proof','return_win','finale')),
  learner_model_version integer not null,
  scope_id text not null default '',                 -- episode_id for host/writer/chat, call_id for salma_notes, week for proof
  body jsonb not null, body_bytes int not null, token_estimate int not null,
  compiled_at timestamptz not null default now(), compile_ms int not null,
  primary key (learner_id, role, learner_model_version, scope_id)
);
```

| Role | Body (PRD-v2 8.6) | Size budget | Stable prefix (cached by the prompt cache) | Volatile tail |
|---|---|---|---|---|
| `teacher` | The pipeline's `TeacherInput` exactly (02-generation-pipeline.md 4.3), compiled here | ≤ 12,000 tokens | `profile`, `skills`, `structure_map` (sorted by `structure_id`), `word_bank_summary`, `bible` | `due_list`, `last_14_days`, `facts_usable`, `follow_ups_due`, `energy`, `claims_passed`, `working_on` |
| `writer` | Supplied to the pipeline as `WriterBriefInputs`: `facts_allowed` (≤ 2 from `facts_usable`, each with quote, event id, `history_text`), `SeriesBibleExcerpt`, `callback` candidate chunks (top 3), `learner_own_words` (last call's 2 best clean turns), name and pronunciation | ≤ 3,000 tokens | bible excerpt | facts, callbacks, own words |
| `host` | `HostLearnerSlice`: `name`, `name_pronunciation`, `pause_profile.eot_silence_ms`, `anxiety_flag` (from the last pass), `last_call_abandoned`, `callback` (one, with quote), `produced_words` (lemmas with `produced_unprompted_n > 0`), `transcript_default`; the pipeline merges it with `episode_artifacts(call_brief)` into the one page | ≤ 600 tokens | everything except `anxiety_flag` and `callback` | those two |
| `salma_talkback` | `produced_words: {lemma: {last_session_date, example_sentence}}` for word-or-hint (PRD-v2 5.4.5), ≤ 400 lemmas | ≤ 1,500 tokens | all | none |
| `salma_notes` | Active targets with evidence (`structure_map` where `target_lifecycle='active'` plus `error_profile.examples`), the verbatim call transcript (`call_turns_v`), `reached_for` history, `notes_mode` | ≤ 6,000 tokens | targets | transcript |
| `chat_host` | Call summary (assessment domain writes it into `episode_artifacts(kind='call_summary')`), targets, the opener artifact | ≤ 1,200 tokens | opener, targets | summary |
| `proof` | `passed_claims(learner_id, week)` with evidence refs; `working_on` items; `notebook_counts`; nothing else (PRD-v2 8.6) | ≤ 2,000 tokens | none | all |
| `return_win` | One claim from `passed_claims` of kind `first_ever` or `words_owned` for the return episode (PRD-v2 3.8.2) | ≤ 200 tokens | | |

`compile()` reads the cache by `(learner_id, role, current_version, scope_id)`; on a miss it compiles, inserts and returns. Rows older than 14 days or more than 20 versions behind are deleted by `retention/daily`. Measured target: teacher compile under 500 ms (ten indexed queries and one JSON build); the pipeline's assumption of 5 s holds with margin. The `host` and `salma_talkback` bodies are compiled at episode time by the pipeline's call-brief step and again at call start by `api` for `GET /internal/calls/{id}/brief` if the version moved (a learner edit between episode time and the call must reach the host).

### 4.10 Claims (written by the claim gate; read by the proof, notes, return episode, finale)

```sql
create table claims (
  claim_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  kind text not null check (kind in ('first_ever','words_owned','structure_learned','fluency','accuracy','complexity','mistake_gone','can_do','flat','worse')),
  metric text, text_ar text not null, text_en text,
  evidence jsonb not null,                           -- [{type: event|observation|recording|word, ref, label}] ; rule 5 "openable"
  gate jsonb not null,                               -- {like_for_like: true, beyond_noise: true|null, repeated: true, clean: true, openable: true, se_used: 0.0|null}
  learner_model_version integer not null, gate_version text not null,
  made_at timestamptz not null default now(),
  shown_at timestamptz, shown_surface text, shown_event_id uuid,
  invalidated_at timestamptz, invalidation_id uuid
);
create index claims_learner_shown on claims (learner_id, shown_at);

create table claim_invalidations (
  invalidation_id uuid primary key, learner_id uuid not null, claim_id uuid not null references claims(claim_id),
  rebuild_run_id uuid not null, reason text not null, created_at timestamptz not null default now(),
  told_at timestamptz                                -- set when Salma said so in a proof (PRD-v2 8.5)
);
create table rebuild_runs (
  rebuild_run_id uuid primary key, learner_id uuid not null, reason text not null,
  from_version integer not null, to_version integer, code_versions jsonb not null,
  started_at timestamptz not null default now(), finished_at timestamptz, sessions_replayed int, diff jsonb, status text not null default 'running'
);
```

The gate logic (the five rules, the standard errors) is the assessment domain's; this domain guarantees that nothing reaches the proof producer except rows in `claims`, that `shown_at` is set exactly once (`mark_claim_shown` is idempotent on `claim_id`), and that a rebuild never deletes a claim with `shown_at` set: it writes `claim_invalidations` and the `proof` brief includes `invalidated_untold` so Salma can say so.

### 4.11 Object storage layout

Three buckets from the topology (`forone-media`, `forone-voice`, `forone-exports`), every learner object under the learner's prefix, every learner-scoped object SSE-C with the learner's DEK (`learner_keys`), indexed in `media_objects`. [DECISION] Keys:

```
forone-media/{learner_id}/episodes/{episode_id}/seg-{n}.m4a         produced show audio, per segment (topology 3.7)
forone-media/{learner_id}/episodes/{episode_id}/full.m4a            stitched, app
forone-media/{learner_id}/episodes/{episode_id}/feed.m4a            stitched + Salma's 5 s tag
forone-media/{learner_id}/episodes/{episode_id}/article.m4a         read-aloud
forone-media/{learner_id}/episodes/{episode_id}/recap.m4a           small door
forone-media/{learner_id}/episodes/{episode_id}/timings.json        word timings, all segments
forone-media/{learner_id}/episodes/{episode_id}/glosses.json        the WordIndex (pipeline 4.10)
forone-media/{learner_id}/episodes/{episode_id}/package.json        script, article, call brief, opener, recap text, shadow lines, why
forone-media/{learner_id}/proof/{proof_id}/{seg-n|full}.m4a
forone-media/{learner_id}/name/clip.ogg                             the learner's own name, ≤ 30 s (retention: see section 10)

forone-voice/{learner_id}/calls/{call_id}/turn-{index}.ogg          learner turns (opus 48 kbps), ephemeral when storage off
forone-voice/{learner_id}/calls/{call_id}/full.m4a                  mixed call, only when storage on
forone-voice/{learner_id}/ephemeral/calls/{call_id}/turn-{index}.ogg  same objects when voice_storage=false; S3 lifecycle: expire 1 day (backstop to audio/expire)
forone-voice/{learner_id}/recordings/{recording_id}/{retell|opinion|repeat-k}.ogg   then-and-now; ephemeral prefix if storage off and not kept explicitly
forone-voice/{learner_id}/notes/{session_id}/say-it-once.ogg
forone-voice/{learner_id}/shadow/{episode_id}/{line_id}.ogg
forone-voice/{learner_id}/voicenotes/{call_id}/{n}.ogg
forone-voice/{learner_id}/marks/{event_id}.m4a                      a marked moment's cut (show audio, not learner voice)
forone-voice/{learner_id}/clips/{claim_id}-{then|now}.ogg           cuts for "how we know"

forone-exports/{learner_id}/{export_id}.zip                         SSE-KMS service key; presigned 7 days; deleted after 14 days
```

Sample episodes (no learner) live at `forone-media/samples/{sample_id}/...` under the service key and expire after 30 days. Bucket settings: versioning off on `forone-voice` and `forone-media` (a delete must be a delete), on for nothing; public access blocked everywhere; the voice bucket has the single lifecycle rule above; object lock is not used.

### 4.12 Export, deletion and retention (PRD-v2 12.5)

#### 4.12.1 Export (`learner/export`, link within 1 h)

Steps, each an Inngest step: (1) `snapshot`: record `lm_version` and `max(seq)`; (2) `tables`: stream the nine stores plus `claims`, `consents`, `goals`, `out_in_world`, `notebook_counts`, `learner_schedule`, `episodes` metadata into `learner_model.json` (one object keyed by table, plain JSON, field names as in the DDL, ISO dates); (3) `events`: `events.ndjson` for the learner in `(occurred_at, seq)` order; (4) `transcripts`: one `transcripts/{local_date}-{kind}.json` per call and chat thread from `call_turns_v` and `chat_message`, plus a `.txt` rendering; (5) `audio`: every `media_objects` row of the learner with `deleted_at is null and ephemeral = false` in kinds `call_turn, call_full, recording, voice_note, say_it_once, shadow, clip, episode_full, proof`, decrypted with the DEK and written into the zip; (6) `zip`: AES-256 zip with a 20-character passphrase generated now, shown once in Controls (`exports.passphrase_shown_at`), never emailed; (7) `upload` to `forone-exports`; (8) `email` kind `export_ready` with the presigned URL (7 days) via the topology's `Email` adapter; (9) `export.ready` event. A 100-session learner with voice storage on is about 1.5 GB; step 5 streams and the total runs in 5 to 15 minutes.

```sql
create table exports (
  export_id uuid primary key, learner_id uuid not null references learners(id) on delete cascade,
  requested_at timestamptz not null default now(), ready_at timestamptz, url_expires_at timestamptz,
  bytes bigint, lm_version integer, high_water_seq bigint, passphrase_hash text, passphrase_shown_at timestamptz, deleted_at timestamptz
);
```

#### 4.12.2 Deletion (`learner/delete`; access at once, live purge within 24 h, backups 30 days)

1. `revoke` (synchronous in `api` before the function starts): `learners.status='deleting'`, `deletion_requested_at=now()`, all auth sessions and `feed_tokens` revoked, web push subscriptions removed, LiveKit rooms for the learner closed. From this moment every request returns 410.
2. `cancel`: Inngest `cancelOn learner.deletion_requested` stops `day/next`, `episode/produce`, `session/after-pass`, `gap/note`, `proof/make` for the learner (topology).
3. `objects`: delete every `media_objects` row's S3 object (all three buckets, including exports), 1,000 keys per request, then mark `deleted_at`; verify with a prefix listing of `{learner_id}/` in each bucket (must be empty).
4. `research`: delete `research_transcripts where pseudonym = hmac(learner_id)` (D18).
5. `rows`: with `set local forone.purge_mode='on'` and the `forone_purge` role: delete from, in order, `briefs`, `claim_invalidations`, `claims`, `conversation_chunks`, `show_canon`, `out_in_world`, `follow_ups`, `life_facts`, `interests`, `goals`, `taste`, `skill_snapshots`, `skills`, `error_profile`, `structure_observations`, `structure_map`, `word_bank`, `notebook_counts`, `working_on_additions`, `consents`, `exports`, `learner_model_versions`, then the topology's `doors`, `sessions`, `calls`, `feed_items`, `episodes`, `episode_artifacts`, `learner_schedule`, `media_objects`, then `events` (every partition, by `learner_id`), then `vendor_calls` rows for the learner (cost domain table: keep the cost totals in an aggregate first).
6. `key`: set `learner_keys.destroyed_at`, then delete the row (crypto-shred; any object the listing missed is unreadable).
7. `ledger`: insert `deletion_ledger {email_hmac, requested_at, live_purged_at=now(), backups_expire_at = live_purged_at + 30 days}`; delete `learners` row last; email kind `account_deleted` to the address captured at step 1 (the only PII the function still holds, in the step's input).
8. `external`: ask Langfuse to delete traces for `user_id` (its deletion API; the cost domain confirms the mechanism [ASSUMPTION]); Inngest holds ids only (no action); Sentry events are scrubbed of learner ids at emission.

```sql
create table deletion_ledger (
  id bigserial primary key, email_hmac text not null, requested_at timestamptz not null, live_purged_at timestamptz not null,
  backups_expire_at timestamptz not null, sessions_count int, verified_empty boolean not null default false
);
```

Backups: RDS automated backups with 30-day retention and PITR; snapshots are not scrubbed. The privacy text says "within 30 days" and that is what the retention makes true. Manual snapshots are forbidden by policy (a manual snapshot never expires); the restore drill in week 5 uses PITR.

#### 4.12.3 Retention jobs (data parts of `retention/daily`)

| Rule | Query or action |
|---|---|
| Trial ended, 90 days (12.5.9) | `learners where status='trial_ended' and trial_ended_at < now() - 83 days and warned_at is null` → email `trial_deleting_soon`; `... < now() - 90 days and warned_at is not null` → send `learner.deletion_requested` |
| Audio when storage off (12.5.2) | `media_objects where ephemeral and expires_at < now() and deleted_at is null` → delete, alert if any older than 15 min |
| Audio after revoke (12.5.3) | `consents.voice_storage=false and voice_storage_at < now() - 24h` and any voice object alive → alert (the purge function should have done it) |
| Partitions | create `events_{yyyy_mm}` three months ahead |
| Briefs cache | delete rows older than 14 days or more than 20 versions behind |
| Exports | delete zips and rows 14 days after `ready_at` |
| Orphans | `media_objects` rows whose S3 object is gone, and S3 objects without a row (sampled prefix listing of 20 learners a day) |
| Research set | rows whose learner has `data_use=false` → delete (should be empty) |

#### 4.12.4 The opt-in research set

```sql
create table research_transcripts (
  id uuid primary key, pseudonym text not null,       -- hmac_sha256(server_secret, learner_id); no learner_id column
  kind text not null check (kind in ('call','chat')), local_date date not null, turns jsonb not null,  -- learner and host text only, names replaced by {NAME}
  analyst_tags jsonb, package_version text not null, created_at timestamptz not null default now()
);
```

Populated by the after-pass only when `consents.data_use = true` at pass time; the name replacement uses the learner's display name and the names in `life_facts.people`. No audio, ever (PRD-v2 12.5.5). Deleted on revoke and on account deletion (D18).

### 4.13 Migrations, roles, RLS and backups

- **Migrations:** Alembic in `packages/core/migrations`, one revision per PR, forward-only in production, every revision has a `downgrade` that is tested in CI against a fresh database. Store DDL changes that are not backward compatible with the rebuild writers bump a `code_versions` key, which is the trigger for a rebuild (D14). Partition creation is not a migration (it is `retention/daily`).
- **Roles:** `forone_app` (api: insert on `events`, select on stores, update on the learner-edit tables, RLS enforced through `forone.learner_id`), `forone_workflows` (select and write on everything except update/delete on `events`), `forone_purge` (delete on everything, used only inside `learner/delete`, which sets `forone.purge_mode`), `forone_readonly` (Muath's SQL, the admin pages; RLS bypass but audit-logged by `pgaudit`). No role has `superuser`.
- **RLS:** every table with `learner_id` has the two policies from 4.1.2. `api` sets `set local forone.learner_id = '...'` at the start of every request transaction from the session cookie; a missing setting yields zero rows, never all rows.
- **Backups:** RDS automated, 30-day retention, PITR; a weekly `pg_dump --schema-only` into the repo's `ops/` for drift checks; a quarterly restore drill, first one in week 5. S3: no replication in the beta (one region, PDPL review pending); the voice bucket's lifecycle rule is the only automatic deletion.
- **Observability of the data layer:** the cost domain's `vendor_calls` is not here; this domain emits metrics `events_appended_total{type}`, `events_duplicates_total`, `facts_rejected_total{reason}`, `lm_bump_total{cause}`, `brief_compile_ms{role}`, `rebuild_duration_s`, `voice_objects_overdue` (anything ephemeral older than 15 min).

### 4.14 PII classification

| Class | Where | Handling |
|---|---|---|
| **Identity** (email, display name, birth date, sign-in ids, payment customer id) | `learners`, auth tables, processor | Encrypted at rest (RDS); never in Langfuse or Sentry; export includes name and email only; deletion removes; `deletion_ledger` keeps an HMAC of the email, not the email |
| **Voice (biometric-adjacent)** | `forone-voice`, the name clip in `forone-media` | SSE-C per-learner DEK; ephemeral when consent is off; purged within 24 h of revoke; never leaves the region except to the transcription vendor during processing; never in the research set |
| **Learner speech and writing (content)** | `events` payloads (`call_turn*`, `chat_message`, `onboarding_answer`), `conversation_chunks`, briefs | RLS; stored for the account's life (core function, disclosed); allowed in Langfuse prompts (processor approval, topology open item 2) |
| **Life facts, sensitive classes** | `life_facts` with `sensitivity` set, `interests.no_go` | Stored only if confirmed in-session; usable one week; never in the research set; included in export; never in any shared store |
| **Derived learner model** | the nine stores, `claims`, `skills` | RLS; exported as plain JSON; never shown as numbers except `notebook_counts` |
| **Behavioral** | all other `events` | RLS; exported; used for rebuilds and metrics |
| **Pseudonymous research** | `research_transcripts` | No `learner_id`; names replaced; opt-in; deleted on revoke or deletion |
| **Operational** | `learner_model_versions`, `rebuild_runs`, `media_objects`, `exports`, `briefs` | Contain ids and sizes only (`briefs.body` is content and is deleted with the learner) |
| **Shared, no PII** | `gloss_cache`, `lexicon_*`, `structures`, `fact_shelf_life`, `ban_list` | The only cross-learner tables (PRD-v2 12.6) |

### 4.15 Configuration keys

| Key | Default | Meaning |
|---|---|---|
| `events.client_clock_skew_max_s` | 300 | beyond this, `occurred_at` is replaced by server time unless a replay |
| `events.batch_max` | 50 | events per `POST /v1/events` |
| `events.partition_months_ahead` | 3 | |
| `prior.k` | 4 | Beta concentration of the frequency prior |
| `prior.size_default` / `prior.size_sd` | 3000 / 1200 | families, when no word check |
| `prior.eye_bonus` / `prior.prod_factor` | 0.05 / 0.6 | |
| `scheduler.desired_retention` | 0.85 | PRD-v2 9.4 due threshold |
| `scheduler.structure_early_cap_days` | [1, 3] | |
| `scheduler.weights` | fsrs-4.5-default | replaced by fitted weights per cohort later |
| `scheduler.stale_days` / `scheduler.stale_floor` | 30 / 0.6 | the shaky-word rule in 4.5.2 |
| `words.owned_sessions` / `words.owned_min_gap_h` | 2 / 24 | |
| `structures.taking_sessions` | 2 | |
| `structures.stable_window_days` / `stable_min_contexts` / `stable_min_sessions` / `stable_acc` | 14 / 5 / 2 / 0.8 | |
| `structures.recheck_weeks` | [2, 4, 8] | |
| `structures.avoidance_min_sessions` | 5 | |
| `errors.pattern_min_obs` / `errors.pattern_min_sessions` | 3 / 2 | PRD-v2 10.5 |
| `facts.viewed_unedited_dwell_ms` / `facts.viewed_window_min` | 4000 / 10 | D10 |
| `facts.same_fact_similarity` | 0.85 | trigram similarity for "said again" |
| `facts.follow_up_expiry_days` | 21 | |
| `interests.decay_tau_days` / `interests.dormant_below` | 21 / 0.2 | |
| `briefs.cache_days` / `briefs.cache_versions_behind` | 14 / 20 | |
| `briefs.token_budget.{role}` | table in 4.9 | compile fails loudly if exceeded |
| `callbacks.chunk_turns` / `callbacks.exact_search_max_chunks` | 3 / 20000 | |
| `export.link_ttl_h` / `export.keep_days` | 168 / 14 | |
| `retention.backup_days` | 30 | must equal the RDS setting; a CI check reads both |
| `retention.trial_ended_warn_days` / `retention.trial_ended_delete_days` | 83 / 90 | |
| `skills.scale_anchors` | A2 30..42, B1 43..58, B2 59..75, C1 76..84 | |
| `skills.sd_obs_default` | 8 | until standard errors are estimated |
| `pause.default_ms` / `pause.min_ms` / `pause.max_ms` / `pause.margin_ms` | 1500 / 1000 / 2500 / 300 | PRD-v2 5.4.4 |

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Effect | Detection | Fallback | Degraded mode |
|---|---|---|---|---|
| `POST /v1/events` down or Postgres unreachable | No events accepted | ALB health, `events_appended_total` flat | PWA queues in IndexedDB for 24 h and replays (topology); the worker spools to S3 and `api` ingests the spool with `source='worker'` and original timestamps | Stores lag; the after-pass runs on whatever arrived; a later replay is folded in by the next pass or a rebuild |
| Duplicate storm (a client replays the same batch many times) | Nothing: duplicates are dropped | `events_duplicates_total` spike | n/a | none |
| Client clock wrong | Wrong `occurred_at` | skew check | Replace with server time, flag the payload | Order within the session may be off by seconds; the after-pass orders call turns by `turn_index`, not by time |
| After-pass result fails validation (schema, quote checks) | The whole result is rejected? No: facts are dropped individually; other sections apply | `facts_rejected_total` | Apply what validates; log the rejects with the session id | A fact said once may need a second saying |
| Version bump contention (an edit and a pass at once) | One waits on the row lock | p99 of `lm_bump` latency | Row lock on `learners`; the second writer sees the first's result | none |
| Verbatim transcription never arrives for a turn (vendor outage, storage off, audio deleted at 15 min) | `call_turns_v.text_verbatim` null | `audio/expire` reports `verbatim_missing` | The pass marks the turn `low_confidence_reason='no_verbatim'`; no observation from that turn is `clean`; no claim; planning uses the streaming text with `confidence=0.5` | Notes may be thinner; nothing is lost |
| Rebuild fails mid-way | Shadow schema partially filled | `rebuild_runs.status='failed'` | Shadow rows dropped; live stores untouched; retry | none for the learner |
| Rebuild would retract a shown claim | | diff | `claim_invalidations` row; Salma says so in the next proof | none |
| `briefs` cache miss storm after a mass rebuild | Compile cost spike | `brief_compile_ms` | Compiles are 500 ms and per learner; Inngest concurrency caps them | none |
| S3 deletion lags (`audio/expire` missed) | Audio past 15 min | `voice_objects_overdue` | The 1-day lifecycle rule on `/ephemeral/`; `retention/daily` alert | A promise missed by minutes is logged as an incident, not hidden |
| Export too large or slow (> 1 h) | Link late | step timeout | Step 5 is resumable per object; if the hour is missed, email "still preparing" and finish | none |
| Learner deletes during a running call | Call continues until the worker's next brief refresh | `learner.deletion_requested` cancels | `api` closes the room at step 1; the worker's spool is discarded for a `deleting` learner | none |
| Langfuse deletion API unavailable | Learner text remains in a processor | `deletion_ledger.verified_empty=false` | Retry daily for 30 days; alert ops | [OPEN for Muath] whether this blocks the "deleted" email |
| RDS failure | Everything | RDS alarms | Multi-AZ failover (topology); PITR restore in the worst case; the last 5 minutes of events can be lost, the PWA queue replays most | A rebuild after restore re-derives stores from the restored log |
| Postgres grows past comfortable size at scale | Slow partitions | table size metrics | Monthly partitions detached to cheaper storage after 24 months; stores stay small (per learner, bounded) | none in the beta |

---

## 6. Cost and performance against the budgets

This domain makes no model calls. Its cost is the database, the buckets, and one embedding call per session (about $0.0005, inside the pipeline's "analyst and memory keeper" line).

| Item | Beta (100 learners, Dec 2026) | 10,000 learners | Note |
|---|---|---|---|
| Events | 300 per session × 20 sessions × 100 = 600k rows/month, about 0.6 GB | 60M rows/month, about 60 GB/month | RDS gp3 storage about $0.115/GB-month in me-central-1 [ASSUMPTION]; 0.7 TB after a year at scale is about $80/month |
| Stores | about 5,000 `word_bank` rows and 300 `structure_map` rows per learner; under 10 MB per learner | 100 GB | bounded per learner |
| `conversation_chunks` | 10 per session; 1536 floats = 6 KB each; 1.2 MB per learner per month | 120 GB/year | exact search per learner stays under 5 ms up to 20k chunks |
| Voice audio (storage on, 60% of learners [ASSUMPTION]) | 6 min call × 0.36 MB/min + extras ≈ 2.5 MB per session; 50 MB per learner per month; 3 GB/month | 300 GB/month, 3.6 TB/year, about $85/month at $0.023/GB | this is the only per-learner line that grows without bound; deletion and revoke remove it |
| Produced audio | the pipeline's line (topology open item 10 on archive growth) | | |
| Exports | transient | | |
| RDS instance | db.t4g.medium Multi-AZ, about $120/month [ASSUMPTION] | db.r6g.xlarge Multi-AZ, about $600/month | shared with every other domain |
| Per-session share | under $0.002 | under $0.003 | far inside the $0.60 budget; the 14.5 "proof share and hosting $0.03" line covers it |

Latency commitments: `events.append` batch of 50 under 30 ms (one multi-row insert); `p_understood_many` for 1,500 units under 100 ms (one query by `(learner_id, unit_id = any(...))` plus in-memory prior for misses); `due_list` under 150 ms; `briefs.compile('teacher')` 300 to 500 ms; `apply_after_pass` 1 to 3 s for a session with 25 turns (dominated by FSRS updates for about 200 units, each a few microseconds, and the pg_trgm fact matching); `apply_learner_edit` under 50 ms; `search_callbacks` under 5 ms; export 5 to 15 minutes; purge under 2 minutes; rebuild about 2 s per session of history.

---

## 7. Build plan for 2026-11-02 to 2026-12-06

| Week | Dates | Ships (P0 unless marked) | Tested with pilot data |
|---|---|---|---|
| 1 | 2026-11-02 to 11-08 | `events` DDL with partitions, trigger, RLS; `events.append` with idempotency and skew; the type registry and all payload schemas; `learner_model_versions` and `versions.bump`; `lexicon_lemmas`, `lexicon_chunks`, `structures`, `reporting_categories` loaders from the package; `word_bank` DDL, priors, `p_understood_many`; py-fsrs wrapper, `due_list`; `CallMeta.learner_model_version` wired into the adapter middleware (with the cost domain); Alembic baseline; `forone_app`/`forone_workflows`/`forone_purge` roles | Import the 15 Milestone 0 learner files and Scribe transcripts as `source='import'` events (`tools/m0_import.py`); check `p_understood` against the kit's coverage checker on 10 scripts (same numbers within 0.5 points); run `due_list` against the hand-kept "next due" column in the learner files |
| 2 | 11-09 to 11-15 | `briefs.compile('teacher')` returning the pipeline's `TeacherInput`; `life_facts`, `follow_ups`, `fact_shelf_life`, `verify_quote`, the ladder, `facts_usable` view; `interests` with decay; `goals`; `show_canon`, `conversation_chunks`, `search_callbacks`, `SeriesBibleExcerpt`; `briefs.compile('writer')`; `structure_map` and `structure_observations` DDL | Replay Muath's confirmed facts: every confirmed fact in the learner files must pass `verify_quote` against the imported transcripts (target: 100% of confirmed, and every unconfirmed one that Muath rejected fails or stays `heard_once`); compile a teacher brief for each pilot learner and have the pipeline's teacher step produce a plan from it |
| 3 | 11-16 to 11-22 | Onboarding writes: `onboarding_answer`, `word_check_answer` → prior seeding and the first `skills` row; `consents`; intake facts as `ground_truth` via `intake_card`; player and article event ingestion end to end from `web` (play, huh, tap, keep, mark, article_scroll, followed_answer); `notebook_counts`; `taste` | Word-check scoring against the 15 pilot word checks (the band table reproduces the kit's estimates) |
| 4 | 11-23 to 11-29 | Call events from the worker (`call_turn`, `talkback`, `hold_floor`, `silence`) and `call_turn_verbatim` from `call/verbatim-turn`; `call_turns_v`; `briefs.compile('host')`, `('salma_talkback')`, `('salma_notes')`, `('chat_host')`; `pause_profile` updater; `media_objects` writes for turn audio with the ephemeral prefix; `audio/expire` data step | 30 pilot clips through the verbatim path: `low_confidence_reason` set correctly from the package threshold |
| 5 | 11-30 to 12-06 | `apply_after_pass` complete (words, structures, errors, skills, interests, facts, canon, scheduler, counts) against the assessment domain's `AfterPassResult`; `apply_learner_edit` (all five edit types) and `working_on.changed`; `claims`, `mark_claim_shown`, `briefs.compile('proof')`, `('return_win')`; `learner/export` content; `learner/delete` purge order and `deletion_ledger`; `retention/daily` data parts; `research_transcripts`; `learner/rebuild` minimal (replay and swap, diff as a count); PITR restore drill; PII test (every column classified, Langfuse scrub verified) | End-to-end with the Milestone 0 learners: a full after-pass over 14 days of one pilot learner's imported sessions produces a word bank and structure map that match Muath's hand-kept file on `owned` words and `pattern` errors (target: agreement on 80% of items; disagreements reviewed by hand) |
| P1 (beta, by 2027-01-10) | | Rebuild diff report and `claim_invalidations` surfacing in the proof; fitted FSRS weights per cohort; `skill_snapshots` for the finale; the research-set name replacement audited; partial HNSW path; the tape's data (`recording` events are P0, the comparison is P1) | |

What is too much for a one-to-two-engineer team and is cut here: a separate analytics warehouse (the events table is queried directly, with `forone_readonly`); a CDC or stream out of Postgres; cross-region replication; a schema registry service (the Pydantic registry in code is the registry); per-learner physical partitions; automated FSRS weight fitting in the beta. If there is one engineer: the rebuild runner moves to P1 (a code-version change before 2027-01-10 is then handled by a one-off script), `research_transcripts` moves to P1 (the consent switch exists but writes nothing), and export omits the `.txt` transcript renderings.

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
| Materialized views for briefs | Briefs are role-shaped and version-keyed; a cache row keyed by version is simpler and invalidates by construction |
| Learner edits through Inngest | "Fixed at once" and the next render must show it; a synchronous path inside the append transaction is the honest implementation |
| Physical partitioning of `events` by learner (hash) | Partition pruning by learner buys nothing over the `(learner_id, occurred_at, seq)` index; month partitions give retention and backup granularity |
| Scrubbing backups on deletion | Not possible with RDS snapshots; 30-day retention makes the promise true by configuration and is written in the privacy text |
| Keeping anonymized research rows after account deletion | Legally defensible, wrong for "the data is theirs"; D18 deletes them (and section 10 asks Muath to confirm) |
| A separate audit log table | `events` is the audit log; `lm_write` events mirror every store write |
| Counting "learned" from the map's counters | Claims must open to a turn; `structure_observations` keeps the evidence and the window is a query |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check.

1. **System topology (01).** Python backend; the `events` table is mine and I honor its two requirements (monthly partitions created by `retention/daily`; `inngest_run_id` and `vendor_call_id` columns). `CallMeta.learner_model_version` is an `int` (its 4.5) and is populated by every caller from `versions.current()`. The `learners`, `learner_schedule`, `learner_keys`, `sessions`, `doors`, `calls`, `media_objects`, `feed_tokens` tables are its; I add `learners.lm_version` and `learners.wrong_memory_n` columns. Its `learner/export`, `learner/delete`, `retention/daily` shells call my step bodies. **Conflict to rule on:** its 3.3 says "only `workflows` writes stores"; D5 here has `api` apply learner-authored edits synchronously. **Conflict to rule on:** its `call/verbatim-turn` says it updates the `call_turn` event; here it appends `call_turn_verbatim` (D2).
2. **Episode generation pipeline (02).** `TeacherInput` as in its 4.3 is what `briefs.compile('teacher')` returns; the fiction tables (`series_bible`, `side_characters`, `running_jokes`, `arcs`, `seasons`, `episodes`, `episode_artifacts`, `gloss_cache`, `format_history`, `script_embeddings`) are its; it sends realized structure counts and host positions in `episode.ready.artifacts` (`realized_structures`, `canon_from_episode`) so `structure_map.heard_n` and `show_canon{position_host}` can be written; it calls `stores.mark_targeted` at publish; its `episodes.status` versus the topology's `episodes.state` is resolved by the integrator (I reference neither by name); its `learner_model_version: string` is the `lm_v_{n}` serialization of my integer; the editor's check 4 calls `facts.verify_quote` and reads `facts_usable`.
3. **Live call and voice stack.** The worker emits `call_turn{speaker:learner|host|salma}`, `talkback`, `hold_floor`, `silence` through `POST /internal/events` with UUIDv7 ids, uploads each learner turn to the key layout in 4.11 (ephemeral prefix when `consents.voice_storage=false`), and reads `HostLearnerSlice` and the talkback dict through `api`'s brief endpoint; the host brief it uses is the merge of the pipeline's `call_brief` artifact and my slice; the anxiety flag it sets during a call is sent as `silence`/`call_turn` payload fields, not written to stores.
4. **Assessment engine, after-session pass and claim gate.** It produces `AfterPassResult` exactly as 4.3.0 (I will adjust field names to its document at integration, not the structure); its stages are pure functions over `call_turns_v` and `chat_message` events so `learner/rebuild` can re-run them without vendor calls (verbatim text is stored; the analyst and classifier are re-run; measures are recomputed from stored word timings); the claim gate writes `claims` through `record_claim` only; its calibration job sets `skills.*.calibrated`; the recording rater writes `stable_confirmed_at` through `stores.confirm_stable`; the recognizer confidence threshold is in the language package and is what sets `structure_observations.clean`.
5. **Client app, podcast feed and delivery.** `web` mints UUIDv7 event ids, batches events, replays the offline queue with the `X-Forone-Replay` header and original timestamps, sends `fact_card_viewed` with dwell and a `visit_id`, and sends `claim_shown`/`note_shown` when a claim is rendered; every API response carries `learnerModelVersion`; the notebook reads the views in 4.3.9 and never computes a number client-side.
6. **Security, privacy, consent and compliance.** Owns the consent copy and the semantics of `consents`; approves the key layout (4.11), the ephemeral prefix and lifecycle backstop, the export passphrase scheme, the `deletion_ledger` HMAC, the 30-day backup statement in the privacy text, Langfuse holding learner text, and the research-set pseudonymization; owns the crisis log reader of `crisis_flag` events; confirms the name-clip retention (section 10).
7. **Cost model, vendor strategy and tracing.** `vendor_calls` carries `learner_model_version` from `CallMeta`; `events.vendor_call_id` references it; the weekly cost report joins on `learner_id`; the Langfuse deletion mechanism for a `user_id` exists or is replaced; the embedding vendor (its `embeddings` role) is approved as a processor for learner text.
8. **Evaluation, observability and operations.** Reads my metrics (4.13), runs the monthly false-claim audit against `claims`, computes "wrong memories per 100 callbacks" from `wrong_memory_flag` events over `show_canon{callback_made}` rows, and the "how much did you follow" comparison from `followed_answer` against the pipeline's `why.predicted`; owns the `/admin` button that sends `learner.rebuild_requested`.

---

## 10. Open for Muath

1. **[OPEN for Muath] English Grammar Profile permission (PRD-v2 Part 18 #8), by 2026-11-09.** The `structures` table ships either way (D19), but the beta's inventory labels, bands and ids come from EGP if permission is granted; if not, the fallback is the kit's hand list plus public CEFR descriptors, which is thinner (about 150 structures instead of 300) and must be grown by hand during the beta. Money or a letter to Cambridge.
2. **[OPEN for Muath] Research rows after deletion.** D18 deletes a learner's anonymized transcripts when they delete the account or revoke data use. A less strict reading keeps already-anonymized rows. The trust contract reads better with deletion; the teacher improves slower. Confirm D18 or allow retention, and the consent copy changes with it.
3. **[OPEN for Muath] Processors that hold learner text.** Langfuse (traces with prompts and completions) and the embedding vendor (OpenAI by the topology's default) receive learner speech and chat text. Deletion depends on their deletion APIs. Approve both under PDPL, or fund self-hosting Langfuse (the topology's costed alternative) and a local embedding model (about one engineer-week).
4. **[OPEN for Muath] The name clip.** The learner's own recording of their name (A3) is voice data kept for name pronunciation regardless of voice-storage consent in the pipeline's assumption. Either the consent copy says so in one sentence ("we keep the 3-second clip of your name so the hosts say it right; delete it any time in Controls"), or the clip is deleted on revoke and the hosts use the respelled text only. Counsel and brand voice.
5. **[OPEN for Muath] The 30-day backup statement.** The privacy text must say "deleted from live systems within 24 hours and from backups within 30 days" and the RDS retention must be exactly 30 days (not longer for operational comfort). Confirm the wording with counsel so engineering sets the number once.
6. **[OPEN for Muath] Storage growth of kept voice (money).** At 10,000 learners with 60% keeping recordings, voice storage grows about 3.6 TB a year (about $85/month at list), on top of the produced-audio archive the topology already flagged (open item 10 there). Both are small now; confirm they are acceptable or set a per-learner retention (for example, call audio older than two seasons is deleted unless marked kept) that the consent copy must then state.
7. **[OPEN for Muath] Export form.** D16 shows the zip passphrase in the app, not in the email. Learners who export and then delete the account before opening Controls lose the passphrase. Alternative: no passphrase and a 24-hour link. Pick one; both are one line of code.
8. **[OPEN for Muath] Who may run a rebuild in the beta.** A rebuild can invalidate shown claims, which Salma must then mention (PRD-v2 8.5). Decide whether rebuilds during the paid beta need your sign-off per cohort (the `/admin` button asks for a reason either way).
