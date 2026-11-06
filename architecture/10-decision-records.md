# Architecture decision records and the cross-domain pass

Domain 10 of the For one technical architecture. Written 2026-11-06 by the "Finish the architecture documentation" thread after reviewing domains 07 to 09 and cross-checking all nine domain documents against each other, against [decisions.md](../decisions.md) (Muath's answers of 2026-10-23) and against [concept-v2.md](../concept-v2.md). Each record below is a ruling that two or more documents now follow; the nine documents were revised on the same day to match. Tags as in the other documents: [DECISION] ruled here; [ASSUMPTION] assumed because the sources are silent; [OPEN for Muath] only the owner can settle, and section 10 lists every one of them.

The one fact behind most records: the nine documents were written on 2026-10-16 and 10-17 against PRD-v2, which encodes the decisions as they stood on 2026-10-10 (one launch pair, Saudi Arabic speakers learning English, SAR prices, a founding year, Salma's correction notes). On 2026-10-23 Muath decided differently on five points and the pilot kit re-dated the schedule. PRD-v2 remains the build spec wherever decisions.md and concept-v2 are silent; where they differ, decisions.md wins, and the PRD-v3 thread is carrying the same changes into the PRD.

---

## 1. Summary and the decisions in one table

| # | Decision | Chosen | Reason in one line | Rejected |
|---|---|---|---|---|
| ADR-01 | Source of truth for the architecture | decisions.md (2026-10-23) over concept-v2 over PRD-v2; the nine documents are revised to it; a PRD-v3 carries the same changes [DECISION] | The architecture must build what Muath decided, not what the PRD said two weeks earlier | Waiting for PRD-v3 before revising (the technical design depends on these documents now) |
| ADR-02 | Languages as two package kinds | A target-language package `packages/languages/<target>/` (voices, recognizers, lexicon, structure inventory, calibration set, law words, crisis keywords, prompts) and a native-language package `packages/native/<lang>/` (interface strings, consent texts, privacy notice, gloss language, Salma's voice and lines, crisis clips and resources); `package_ar_en` is split into `lang/en` and `native/ar`; every learner carries `native_language`, `target_language`, `residence_country`, `tz` [DECISION, decisions.md §1, concept-v2 §7 and §8] | No launch pair means the pair is a per-learner fact; the two sides have different bars (the gate for a target, strings for a native language) | One package per pair (n × m packages); hard-coding English and Arabic until "later" |
| ADR-03 | The language gate as code | `forone.langgate` runs concept-v2 §8's five checks per target language from `vendor-lab`; a target opens when its gate run passes; English is the pilot target and the only one that must pass before the beta; the gate runs in parallel with Milestone 0 [DECISION] | 08's vendor tests and 09's recognizer suite are the gate's first three checks; one harness, one evidence folder | Vendor tests as one-off scripts per language |
| ADR-04 | Plans and allowance | Three monthly USD plans: `one_a_day` $19.99, `two_a_day` $29.99 (recommended, the trial plan), `three_a_day` $44.99; the allowance is `plan.episodes_per_day` new episodes per learner-local day; one swap a day stays; listening, the article, the chat and round two are unlimited; founding = the first 100 payers keep their plan's price (`founding_locked`), no yearly plan [DECISION, decisions.md §2] | Decided by Muath; the cost model sets the price | SAR founding year and yearly plan (PRD-v2 1.4) |
| ADR-05 | How episodes 2 and 3 are made | The first new episode of the day is produced by the batch pipeline for the drop; episodes 2 and 3 are made on request ("next one", a learner action, never autoplay) through the on-demand path, streamed under 30 s, with the teacher's plan for them prepared in the nightly run so no Opus call sits on the path; the nightly run may pre-produce episode 2 for learners whose last 7 days show they use it [DECISION, concept-v2 law 11] | Typical use is 50 to 60% of the allowance, so pre-producing everything wastes about a third of the voice line; the on-demand path already exists | Pre-producing the full allowance; a "next episode" feed |
| ADR-06 | Invisible teaching in the architecture | Salma's after-call notes, the polish card and the chat margin note are removed; `session/after-pass` loses stage 1 (the 90-second notes step) and keeps the 10-minute pass; the correction guard (07) blocks explicit corrections from every host and Salma line in code; the editor's check "nothing reads as a correction" is a model check; "say it once" and shadowing stay as pronunciation; the notebook, the weekly proof, "why this episode" and "where do I stand" stay as evidence [DECISION, decisions.md §3 and §4, concept-v2 law 7] | Muath's call; law 7 must be enforced by code the way law 12 is | Keeping notes as an option behind a flag (a flag never changes a law, 09 D8) |
| ADR-07 | Dates | Milestone 0 2026-10-24 to 11-18; language gate and vendor tests during it; build 2026-11-18 to 12-22 in five weeks; beta 2026-12-23 to 2027-01-26; gate review 2027-01-26; every "2026-11-02" in the first drafts moves 16 days [DECISION, milestone-0/03-schedule.md] | The pilot had not started when the first drafts were written | Keeping the old dates "until the PRD moves" |
| ADR-08 | Home region | Default `HOME_REGION = eu-central-1` (Frankfurt) for a worldwide cohort; `me-central-1` (UAE) remains a one-day config move if counsel and the cohort favour it; `call-worker` runs where the vendors are fastest; **final answer stays [OPEN for Muath, with counsel]** [DECISION on the default only] | With no launch country, EU and UK learners' data in the UAE is itself a transfer without adequacy; an EU region needs only the AWS DPA for them | GCP Dammam now; a region per learner (two of everything) |
| ADR-09 | Tracing data (Langfuse) | 01 D15 stands for every domain: metadata only by default (ids, versions, usage, cost, latency, prompt hash); prompt and completion text only for learners with `data_use = true`, after `anonymize()`; `user_id` is the research pseudonym, never the learner id; 30-day retention; debugging reads prompts from the home region (02's `pipeline_steps` artifacts, the call brief and turns in `events`) [DECISION] | Three documents had three rules for one processor; the strictest one is also the one 01 already designed | 08 D3 (full text, learner id, 100%) |
| ADR-10 | Embeddings vendor | Google's embedding model under the existing Google processor row; no OpenAI processor [DECISION, 02 §9.7] | One fewer processor for one cosine check | OpenAI `text-embedding-3-small` (07 and 08 first drafts) |
| ADR-11 | Editor fallback | When the second vendor is down the editor runs on `claude-opus-5-5` (standard), flagged `same_vendor_edit` for review; never code checks only [DECISION, 02 §9.7] | The editor must be at least as strong as the writer when it shares the writer's vendor | Haiku as the fallback editor (08 first draft) |
| ADR-12 | Media key model | Learner-voice kinds (`call_turn`, `call_full`, `recording`, `voice_note`, `say_it_once`, `shadow`, `clip`, the name clip) are SSE-C under the learner's DEK; produced show kinds (`episode_segment`, `episode_full`, `episode_feed`, `read_aloud`, `recap`, `feed_tag`, `proof`) are SSE-KMS under the environment key, served by short-lived presigned URLs, deleted by prefix in `learner/delete` [DECISION, amends 07 D1 and D3, 01 D7] | SSE-C can never be served by a presigned URL, a CDN or `<audio src>`; locking show audio behind `api` bandwidth forever was an accident of the first draft | Everything SSE-C (07 D1); everything SSE-KMS (loses "key deletion deletes the voice") |
| ADR-13 | Cost rows and the spend counter | `vendor_calls` rows are written in their own short transaction the moment a vendor responds, idempotent on `(inngest_run_id, step, attempt)` or `(call_id, turn_index, capability)`; the same statement upserts `learner_spend_daily`; the worker appends each turn's rows to an S3 spool before any buffered flush; reconciliation hourly [DECISION, amends 08 §3.2 and 07 §4.11] | A cost row inside the caller's transaction is lost on exactly the retry the spend guard exists to catch | Same-transaction writes; nightly reconciliation |
| ADR-14 | Spend modes and model levers | Automatic spend modes may change only what no learner hears (force batch, cap rewrites, skip canaries and the nightly smoke, defer anonymization) and may pause on-demand extras under the daily cap; model downgrades (Haiku host, Sonnet teacher) are feature flags a person flips after `eval-gate` passes [DECISION, 09 D8 over 08 D4 `conserve`] | A quality change is a human decision, not an alarm's | 08's automatic `conserve` downgrades |
| ADR-15 | Per-plan cost guard and caps | Soft guard 2.5 × `episodes_per_day` × budget, hard 4 × episodes × budget; call starts 6 × episodes a day; ideas 3 per episode slot; daily spend cap Σ `episodes × $1.00` over learners; the weekly report gains "Margin by plan", `plan_mix` and `blended_margin` [DECISION, amends 07 D11 and 08] | Every per-day limit in the first drafts assumed one episode a day | Fixed $2.50 / $5.00 guards |
| ADR-16 | Operations around the clock | No protected hour and no timezone-fixed job: every rule is relative to each learner's `drop_at`; `measures/daily` and `privacy/verify` run hourly over learner-local days that closed; reports at fixed UTC times; the release tool computes the deploy window from `learner_schedule` (deploy only when under 2% of learners have a drop in the next 45 min, `call-worker` only when idle) and the check is binding; per-learner lateness is P2, systemic lateness (3+ learners or 5%) is P1; staging stays up from build week 2 through the beta [DECISION, amends 09 D9, D11, 4.10 and 01 D14] | Learners anywhere means drops at every hour | A Riyadh-centred rota and release window |
| ADR-17 | Database roles for staff surfaces | `forone_admin` serves the `/admin` pages (aggregate reads across learners, writes only to the admin tables), with every content read in `audit_log`; pgaudit applies only to `forone_human`, the role psql sessions use [DECISION, amends 07 §4.2 and 09 D2] | pgaudit on the dashboards' role would bury the human-SQL audit it exists for | Dashboards on `forone_readonly` under pgaudit |
| ADR-18 | DEK cache and audit | `keys.get_dek` caches 60 s in `api` and `workflows`, never for `admin_break_glass` or `export`; one `audit_log` row per `(learner_id, purpose, actor)` per cache window with a `uses` count; cache entries are keyed by `(learner_id, key_version)` and `destroy()` bumps the version in the row so every process misses on its next read; the zeroization claim is dropped [DECISION, amends 07 D2 and §4.1] | A 10-minute cache made the audit log incomplete and let a destroyed key keep working in other tasks | Per-read KMS calls (latency and cost); the first draft's cache |
| ADR-19 | Naming rulings | `episodes.state` (not `status`); `events` append-only with `call_turn_verbatim` as a second event appended by `workflows` through `events.append()`; `word_uses` is 04's per-use word evidence table written by 05 (the twin of `structure_observations`); `learner_schedule.expects_drop`; `tools/call-bench` is the one load and latency tool; `cohort_key = invite_date`; `proofs.sessions_in_week` is computed, not stored [DECISION] | Nine documents, one vocabulary; the technical design needs the names fixed | Leaving each document's spelling |
| ADR-20 | Jurisdiction and crisis resources | `learners.residence_country` is asked at A9, never inferred; 07 §4.9 becomes a regime table (EU and UK GDPR, Saudi PDPL, a generic baseline for unreviewed countries) with the breach clock and DPIA per regime; crisis resources per ISO country with an international directory as the fallback; a DPIA is the fifth counsel artifact [DECISION; which regimes counsel covers on day one is OPEN] | A Saudi-only privacy design cannot serve a learner in Berlin | PDPL-only (07 first draft); blocking signups from unreviewed countries |
| ADR-21 | Payments | Three USD plans as in ADR-04; hosted checkout; cards, Apple Pay and Google Pay worldwide; a merchant-of-record processor recommended (Paddle; Stripe with Stripe Tax as the fallback) because tax falls due in many countries; Mada and other regional methods later; founding price lock, not a founding plan; **processor stays [OPEN for Muath]** [DECISION on the model] | No launch country means no single tax jurisdiction | SAR-first, Mada-first processors (07 §4.14 first draft) |
| ADR-22 | Open-item register | The items only Muath can settle are listed once, in section 10 of this document, with the domain that waits on each; the other nine documents' section 10 lists point here where they overlap [DECISION] | Thirteen plus eleven plus ten open lists in nine documents hid the few that block the build | Each document keeping its own full list |
| ADR-23 | Second-pass naming (integration, 2026-11-06 evening) | After the nine revisions: Inngest event `learner.extra_requested {learner_id, local_date, slot, episode_id}`; `episodes.slot` (1 = the drop, 2 and 3 = `daily_extra`); terminal state `superseded` for unused extras and swapped dailies; `turn_index` everywhere; `cost/reconcile-spend` hourly; `rater.pinned_until = 2027-02-16` (05's cohort-aligned first window); object keys `learners/{lid}/...` with the bucket-level `ephemeral/` prefix (04 D15); `client_perf.first_sentence_ms`; A3 facts stored `usable`; no zeroization claim anywhere | Nine agents revising in parallel chose different spellings for the same new things; one spelling per thing before the technical design reads them | `day_seq`, `learner.next_requested`, `unused`, `turn_n`, `cost/reconcile`, a 2027-01-19 rater window, `episodes/{learner_id}/` prefixes |

---

## 2. What changed on 2026-10-23 and what it does to the architecture

| Decision (decisions.md) | What the first drafts assumed | What the architecture now does | Domains touched |
|---|---|---|---|
| 1. No launch country or group; a language gate | Saudi Arabic speakers learning English; `package_ar_en`; Arabic UI, consent and Salma; PDPL and SDAIA; Riyadh time everywhere; 5 Saudi raters | ADR-02, 03, 08, 16, 20: two package kinds, a per-learner pair and country, EU default region, round-the-clock operations, the gate as code | all nine |
| 2. Monthly USD tiers of 1, 2 or 3 episodes a day | One new episode a day; SAR 89 monthly, SAR 449 yearly, SAR 349 founding year; Mada | ADR-04, 05, 15, 21: plans, allowance by plan, on-demand episodes 2 and 3, per-plan guards and margins, MoR payments | 01, 02, 06, 07, 08, 09 |
| 3. Teaching is invisible | Salma's notes in 90 s, polish card, margin note; `notes` tables, door, measures, latency budget, cost line | ADR-06: all removed; the correction guard added; the after-pass is one stage | 02, 03, 05, 06, 07, 08, 09 |
| 4. Evidence instead of tests | Already in PRD-v2 (word check, recordings, notebook, claim gate) | No change beyond ADR-06's note that "New for you", the notebook and the proof are evidence and stay | 04, 05, 06 |
| 5. 4-week seasons | Already in PRD-v2 | No change; dates of the first finales move with ADR-07 | 02, 05, 09 |
| Pilot kit re-dated (2026-10-23) | Build 11-02 to 12-06, beta 12-07, gate 2027-01-10 | ADR-07 | all nine |

---

## 3. The decision records

Each record: context, the ruling, consequences per domain, and what stays open.

### ADR-01 Source of truth

**Context.** PRD-v2 (2026-10-10) is the build spec every document cites by part number. Muath's answers of 2026-10-23 overruled parts of it; concept-v2 and decisions.md were updated the same day; the PRD was not. **Ruling.** decisions.md wins over concept-v2, which wins over PRD-v2; PRD part numbers stay as citations for the unchanged parts; where a document cites a changed part it now cites the decision. **Consequences.** Every document's front matter says "revised 2026-11-06 to the decisions of 2026-10-23"; the PRD-v3 thread is told which parts changed (section 5 lists them).

### ADR-02 Languages as two package kinds

**Context.** `package_ar_en` appears in 02 (gloss language, prompts), 03 (Salma persona, talkback), 06 (`lang="ar"`, RTL), 07 (consent texts, notice, crisis), 08 (`packages/language/ar-en/recognizer.yaml`), 09 (`versions.yaml`). Concept-v2 §7 says the target language is a package that passes the gate and the learner's own language "needs only interface text, glosses, and a recognizer that catches it when the learner switches". **Ruling.** Two package kinds. `packages/languages/<target>/`: episode and call voices, streaming and verbatim recognizers with thresholds, lexicon and frequency list, structure inventory and rules, calibration set, law words and correction phrases, crisis keywords, host prompts, format patterns, the ban list. `packages/native/<lang>/`: interface strings (direction from the package: `dir`), consent texts and the privacy notice, gloss target language, Salma's voice and persona lines, crisis clips and the resources card copy, the talkback language hint. `learners` gains `native_language`, `target_language`, `residence_country`; every brief compiler, prompt loader and TTS request reads the pair from the learner row. The pilot's packages are `lang/en` and `native/ar`; `native/en` is the universal fallback for interface and consent. **Consequences.** 02: gloss cache key already carries `native_lang`; prompts load from `lang/<target>`. 03: Salma's talkback and persona from `native/<lang>`; `talkback_stt.languages = [native, target]` per call. 06: `dir` and `lang` from the native package; the landing page is served per `Accept-Language` with English as the default. 07: ADR-20. 08: the gate per target. 09: `versions.yaml` per package; corpora per language. **Open.** None for the mechanism; which native packages exist on 2026-12-23 depends on the beta cohort (English and Arabic are certain).

### 

**Reconciled 2026-11-06 with the sibling threads.** The engineering handbook (engineering/01-repository-layout.md) already uses `packages/languages/<target>/` with `gate.yaml` inside it, so that is the path; the architecture's earlier `packages/lang/` spelling is dropped. The technical design (technical-design/00-overview.md) chose a per-pair package `packages/language/<pair>/` with `ar-en` first and columns `native_lang` / `target_lang`; this record overrides it: two axes, not pairs (a pair package would multiply content by every native language), `packages/languages/<target>/` plus `packages/native/<lang>/`, and the column names `native_language` and `target_language`. The handbook's `ui_strings/` is the UI part of `packages/native/<lang>/`.

ADR-03 The language gate as code

**Context.** 08 §4.6 specifies the voice blind test, the 50-call latency test and the 30-clip recognizer test for one pair; 09 §4.2 wraps them as suites; concept-v2 §8 names five checks (voices, learner speech to text, writing, the call, structures) that open a language. **Ruling.** `forone.langgate` (in the `vendor-lab` CLI) runs the five checks for a target language and writes one evidence folder `langgate/<target>/<date>/`; a `lang/<target>/gate.yaml` records the pass with the date and the winners; `vendors.yaml` roles that depend on the target (`episode_tts`, `call_tts`, `streaming_stt`, `verbatim_stt`, `pronunciation`) are keyed by target language. Raters: 5 native speakers of the target plus 5 learners of it from anywhere; clips: 30 real learner clips per target. **Consequences.** 08 §4.6 is rewritten as the gate's checks 1, 2 and 4; 09's `recognizers`, `voices-blind` and `calls_50` suites are the gate's regression form; 02's writing check (a native speaker reads 10 scripts) and 04's structure inventory are checks 3 and 5. English runs during Milestone 0 on the pilot's clips.

### ADR-04 Plans and allowance

**Ruling.** `plans.yaml`: `one_a_day` $19.99, `two_a_day` $29.99 (recommended; the 7-day trial plan), `three_a_day` $44.99, USD, monthly, VAT or sales tax handled by the processor (ADR-21). `subscriptions.plan` takes these three values; `founding_locked boolean` and `founding_seq` 1 to 100 lock the price for as long as the subscription lasts. The allowance is `plan.episodes_per_day` new episodes per learner-local day, enforced in `api` (`episodes_today < plan.episodes_per_day`), with one swap a day (PRD 3.6) and unlimited listening, article, chat and round two. **Consequences.** 01: `plans.yaml`, the allowance check, `learners.plan`. 06: the plan picker on day 7, "about $1 a day", the compromise and anchor layout from concept-v2 §8, cancel in one tap. 07: ADR-21. 08: ADR-15. 09: `plan_mix`, `blended_margin`. **Open.** The exact price points stay adjustable (decisions.md); see section 10 #4 for the break-even warning.

### ADR-05 Episodes 2 and 3

**Context.** Law 11 (concept-v2 §5): "One, two or three new episodes a day depending on the plan, each with a clear ending, no autoplay and no feed." The batch pipeline makes one episode for the drop; the on-demand path (swap, return) streams in under 30 s. Typical use is 60%, 50% and 45% of the allowance (concept-v2 §8). **Ruling.** Episode 1 is the drop (batch). Episodes 2 and 3 are made when the learner asks ("next one" on Today after the current session's episode is heard), through the on-demand path with `episode_kind = daily_extra`, standard pricing, scene 1 first. The nightly teacher run plans all of the day's episodes (one plan with 1 to 3 episode briefs, each with its own targets so the day's language load stays within the 2 to 4 words and 1 structure per episode rule), so the on-demand run starts at the writer. Learners whose last 7 days show 5 or more extra episodes get episode 2 pre-produced in the nightly batch (`prewrite_extra`), the way 02 D15 pre-writes the rank-2 idea. The feed carries only the drop episode plus any extra the learner has played. **Consequences.** 01: `day/next` creates up to `episodes_per_day` `episodes` rows in state `planned`; `POST /v1/episodes/next`. 02: `daily_extra` kind; the teacher's multi-episode plan schema; `prewrite_extra`. 06: the "next one" control (one button, after the episode ends, never autoplay); the Show tab lists all of the day's episodes. 08: the cost model prices a learner-day as 1 + extras × on-demand premium (about +$0.05 an episode for standard pricing), and the margin by plan uses measured extras.

### ADR-06 Invisible teaching

**Context.** decisions.md §3 drops "the after-call correction notes, the polish card, the chat margin note"; concept-v2 law 7 forbids "the correct answer is" and correction notes; Salma "never corrects, never sends notes". 05 built `notes`, `margin_notes`, a 90-second stage 1, the polish TTS, the notes door; 06 renders them; 08 prices them; 09 measures them; 07 guards them. **Ruling.** Remove: `notes`, `margin_notes` tables and functions; `session/after-pass` stage 1; the notes door and the margin chip; `notes.enabled`; `notes_late`, `chat_opener_late` stays; the "Notes under 90 s" budget; the cost line "Salma's notes and chat" becomes "Salma (when asked) and chat". Keep as evidence (decision 4): the notebook with its "working on" list, "words you own", the tape, "how we know"; the weekly proof and finale through the claim gate; "why this episode"; "where do I stand" when asked, with a range; the "New for you" card from `did_it` and `first_ever` claims; "say it once" and shadowing as pronunciation with internal scoring only. Add: the correction guard in `guard.check_output` (07) with a per-language phrase list, counted in `moves.violations` and in 09's `explicit_corrections_per_100_turns` (ceiling 0); the editor's check "nothing reads as a correction or a lesson" as a model check on every script, article and chat opener (02 check 10 widened); the teacher's "echo plan" (which of the learner's recurring errors the host should recast this call and which right forms the next episodes carry), already the host brief's `recasts` field in 03, now the only correction channel. The after-session pass is one function with the 10-minute budget; the analyst's first stage runs inside it. **Consequences.** 02, 03, 05, 06, 07, 08, 09 revised; the technical-design thread should drop the notes screens and the margin chip. Salma's remaining per-session role is explanations when the learner asks (`salma_explain`, Sonnet, on demand).

### ADR-07 Dates

**Ruling.** Milestone 0: 2026-10-24 to 11-18 (gate decision 11-18). Language gate for English and the vendor tests: 2026-11-01 to 11-17 on the pilot's clips (recognizer by 11-10, voice by 11-17, `vendors.yaml` committed before build week 1). Build weeks: W1 2026-11-18 to 11-24, W2 11-25 to 12-01, W3 12-02 to 12-08, W4 12-09 to 12-15, W5 12-16 to 12-22; exit 12-22 (measured cost per session and a costed path to $0.35). Beta: 2026-12-23 to 2027-01-26; first cohort 12-23 (a Wednesday; the invite cadence is weekly on the beta's weekday, `cohort_key = invite_date`); the Gemini price doubling lands in beta week 2; first finales from 2027-01-19; first "active in week 4" readable 2027-01-20; gate review 2027-01-26. Freezes: 2026-12-21 12:00 to 12-24 12:00 UTC and 2026-12-31 to 2027-01-02. Counsel's answers (region, consents, crisis lines) due before build week 1: 2026-11-17. **Consequences.** Every build plan (section 7 of each document) is re-dated by 16 days with the same week contents unless a record above changes them; the hub's "due soon" list is re-dated.

### ADR-08 Home region

**Context.** 01 D8 chose `me-central-1` for Saudi residents' data; 07 D7 accepted it; 01 §10 #1 asked counsel "may Saudi residents' voice rest in the UAE or EU". With learners anywhere the question is different: EU and UK learners' data in the UAE is a transfer without an adequacy decision; the same data in Frankfurt needs only the AWS DPA, while the US vendor transfers are the same in every option. Latency does not decide it: 01 §3.6 already lets `call-worker` run near the vendors and no database sits on the turn path. **Ruling.** The default becomes `HOME_REGION = eu-central-1`; `me-central-1` stays available as the alternative if counsel and the first cohort's residence countries favour it; Vercel region follows (`fra1`); Inngest and Langfuse stay EU. The architecture is indifferent between the two AWS regions (one config key), so the choice can be made as late as the Terraform apply in build week 1. **Open.** [OPEN for Muath, with counsel] the final region and the transfer basis for the US vendors (section 10 #1). This is the item the coordinator asked to keep open.

### ADR-09 Tracing data

**Ruling.** 01 D15 as revised on 2026-10-17 stands for every domain (see the table). 08 D3 and §4.3 are rewritten; 07's Langfuse register row says "metadata and pseudonymous ids by default; anonymized text only for `data_use` learners; 30 days"; 09 §4.9's Langfuse row says the same. The research pseudonym is a row in `research_pseudonyms(learner_id, pseudonym)` (deleted with the learner) rather than an HMAC of a never-rotated secret, so the secret can rotate and deletion by pseudonym still works (07 skeptic minor). Langfuse deletion is by pseudonym and does not hold up the "deleted" email (closes 04 §10's question).

### ADR-10 and ADR-11 Embeddings and the editor fallback

As in the table; 07 §4.9 loses the OpenAI row, 08 §4.2 and §4.7 change the `embeddings` and `editor` rows, 02 §4 keeps its similarity check on the Google model. The editor fallback's cost (about $0.05 on a fallback day) is in 08's failure table.

### ADR-12 Media key model

**Context.** 07 skeptic finding: SSE-C objects cannot be served by presigned URLs, a CDN or `<audio src>`, so every byte of show audio was routed through `api` forever; 06 §4.4.4 already proxies media through `api` with Range support, which hides the consequence. **Ruling.** As in the table. `media_objects.encryption in ('sse_c_learner', 'sse_kms_env')` set by kind; `api`'s media route issues 10-minute presigned URLs for `sse_kms_env` kinds (the feed's enclosure URLs are already tokenized and stay proxied, because podcast apps cache URLs); learner-voice kinds stay behind `api` with the DEK. `learner/delete` deletes show kinds by prefix (already in 04's purge order) and destroys the DEK last. **Consequences.** 01 D7 and the media route; 06 §4.4.4 source selection (case 2 becomes a presigned URL); 07 D1, D3, §4.1; 08's hosting line (egress moves from Fargate to S3, cheaper).

### ADR-13 to ADR-15 Cost rows, spend modes, per-plan guards

As in the table. The report's "Margin by plan" section: net price (list less the processor's measured fee and tax), measured episodes used, measured cost per learner-month, margin, and the break-even cost per session at full use ($0.57 / $0.42 / $0.42 from decisions.md); `plan_mix` and `blended_margin` are measures in 09 and lines in the Tuesday review. Section 10 #4 carries the warning that the post-doubling floor ($0.43 to $0.45) is above the 2 and 3 a day break-even at full use.

### ADR-16 Operations around the clock

As in the table. Jobs: `measures/daily` → `measures/hourly` computing learner-local days that closed in the last hour; `privacy/verify` hourly over the last 25 hours with `expires_at`-based checks; `retention/daily` per learner-local midnight; the digest at 06:00 UTC; the weekly report Mondays 06:00 UTC. Alerts: `episode_not_ready_before_drop` is P2 per learner with dedupe, and a new `drops_late_systemic` rule is P1 at 3 or more learners or 5%. Release: `tools/release` refuses a deploy when more than 2% of learners have a drop in the next 45 minutes (an override needs a reason row); `call-worker` deploys drain as 01 §4.4 #7 says, at any hour. On-call: P1 pages at any hour; the honest beta statement is that a one-engineer rota means some overnight P1s are answered by the product's fallbacks (yesterday's episode stays; voice notes) and a human at the next working hour; section 10 #7 asks Muath to accept that. Staging stays up from build week 2 through the beta (about +$180 a month, carried into 01 §6 and §10 #4).

### ADR-17 to ADR-19

As in the table. For ADR-19, the full list of renamings is in section 4.

### ADR-20 Jurisdiction and crisis resources

**Ruling.** `learners.residence_country` (ISO 3166-1) asked at A9 as one question with a country picker, never from IP (trust promise 6). 07 §4.9 becomes a table of regimes with, per regime: lawful basis for voice and for the research set, breach clock and regulator, DPIA requirement, children's age threshold (the product's 18+ gate exceeds all of them), transfer basis for US vendors, and the status of counsel's review; a generic baseline row applies to a learner whose country is not reviewed and says so in the notice. `packages/native/<lang>/crisis/resources.yaml` keyed by ISO country with an international directory entry as the fallback; the card shows the learner's country's lines or the directory. Counsel artifacts: consent texts, notice, crisis files, processor register, DPIA. **Open.** Section 10 #2: which regimes counsel covers for 2026-12-23 and whether signups from unreviewed countries are accepted under the generic notice.

### ADR-21 Payments

As in the table. The `Payments` adapter interface (01 §4.5) is unchanged; a merchant-of-record processor changes who issues the invoice and remits tax, not the webhook model. Fees: about 5% (MoR) against about 3% plus tax registrations; the margin section reads the real fee row. **Open.** Section 10 #3.

### ADR-22 Open-item register

Section 10 below is the register. Each domain document's section 10 keeps only the items specific to that domain and points here for the shared ones.

---

## 4. Naming and interface rulings

| Item | First drafts | Ruled | Documents changed |
|---|---|---|---|
| Episode lifecycle column | `episodes.state` (01, 06), `episodes.status` (02, 09) | `episodes.state` | 02, 09 |
| Verbatim result | update of `call_turn` (01 first draft) vs second event | `call_turn_verbatim` appended by `workflows` through `events.append()` | confirmed in 01, 03, 04, 05 |
| Who appends events | "only `api`" (01 first draft) | `api` and `workflows`; `call-worker` never holds a connection | confirmed |
| Word-use evidence | `word_uses` [ASSUMPTION in 09]; a list in 05's `AnalystOutput.target_uses` | `word_uses(learner_id, unit_id, event_id, occurred_at, clean, correct, prompted, quote)` owned by 04, written by 05 | 04, 05, 09 |
| Drop expectation | `learner_schedule.expects_drop` [ASSUMPTION in 09] | Added to `learner_schedule`; set when the previous local day was active | 01, 09 |
| Load and latency tool | `tools/load-call` (01), `tools/call-bench` (03) | `tools/call-bench` | 01 |
| Cohort key | `cohort_monday` | `cohort_key = invite_date` | 09, 04 |
| Package paths | `packages/package_ar_en/...`, `packages/language/ar-en/...` | `packages/languages/<target>/...`, `packages/native/<lang>/...` | 02, 03, 06, 07, 08, 09 |
| Learner columns | `native_language` only | `native_language`, `target_language`, `residence_country`, `plan`, `tz` | 01, 04 |
| Plans | `founding`, `monthly`, `yearly` | `one_a_day`, `two_a_day`, `three_a_day`; `founding_locked` | 01, 06, 07, 08, 09 |
| Episode kinds | daily, swap, return, pilot, sample, fallback, rehearsal, finale, proof, canary | plus `daily_extra` | 01, 02, 06, 08 |
| Media encryption | SSE-C for all learner-scoped objects | `media_objects.encryption in ('sse_c_learner','sse_kms_env')` by kind | 01, 02, 06, 07 |
| Removed tables and functions | `notes`, `margin_notes`, `chat/margin-note`, `stage1_notes`, `notes.ready`, `note_shown` (event type), `notes_mode` | removed | 02, 03, 05, 06, 07, 08, 09 |
| New guard items | law words, humanity, progress claims | plus the correction guard (`guard/correction_words.yaml` per language) | 03, 07, 09 |
| Langfuse `user_id` | learner id (08), tokenized names (07) | research pseudonym; metadata only unless `data_use` | 07, 08, 09 |
| Database roles | `forone_app`, `forone_workflows`, `forone_purge`, `forone_readonly` | plus `forone_admin` (pages), `forone_human` (psql, pgaudit) | 04, 07, 09 |
| Cost tables | `session_costs` as a table (08) and "a view" (09) | a table filled by `cost/rollup`, with `plan` | 09 |
| Alert for the stop line | P1 `spend_cap_or_stop_line` | `cost_runaway` P1; `cost_stop_line` P3 plus the ticket | 09 |

| Extra-episode trigger (Inngest) | `learner.next_requested` (01), `learner.extra_requested` (02); log event `episode_next_requested` (04) | Inngest `learner.extra_requested {learner_id, local_date, slot, episode_id}`; the learner-log event stays `episode_next_requested` (04 owns the log catalogue) | 01, 02, 04 |
| Episode sequence in the day | `episodes.day_seq` (01), `episodes.slot` (02, technical design) | `episodes.slot smallint`, unique `(learner_id, local_date, kind, slot)` | 01, 02, 04 |
| Unused extra / swapped daily | `unused` (01), `superseded` (02) | `superseded` | 01, 02 |
| Turn counter | `turn_n` (08), `turn_index` (03, 04, 05) | `turn_index` | 08 |
| Hourly spend reconcile | `cost/reconcile` (01), `cost/reconcile-spend` (08) | `cost/reconcile-spend` | 01 |
| Rater pin window | 2026-12-31 (08), 2027-01-19 (01), 2027-02-16 (05) | `rater.pinned_until = 2027-02-16`; 09's window calendar starts the next window on 2027-02-17 | 01, 08, 09 |
| Object key layout | `episodes/{learner_id}/` (02), `learners/{lid}/calls/{id}/{ephemeral/}` (01), `learners/{lid}/ephemeral/calls/` (03) | 04 D15: `learners/{lid}/...`; storage-off voice under the bucket-level prefix `ephemeral/learners/{lid}/...` so a lifecycle rule can match it | 01, 02, 03 |
| First-sound client metric | `client_perf.first_english_ms` (06) | `client_perf.first_sentence_ms` (language-neutral) | 06, 09 |
| A3 intake facts | `ground_truth` at once (02) | `usable` at once; `ground_truth` after a later confirmation (04, PRD 8.4.2) | 02 |
| Research pseudonym | "the secret can rotate" (ADR-09 as first written) | a random stored value in `research_pseudonyms`; there is no HMAC secret and no `RESEARCH_PSEUDONYM_SECRET` (07) | 07, 08, 09 |

**For the technical-design thread.** (Updated after the nine revisions: each document's section 11 lists every new name it introduced; the ten rows above this paragraph are the ones two documents spelled differently. The technical design's `packages/language/<pair>/` with `ar-en` first, and its `native_lang`/`target_lang` columns, are overridden by ADR-02: two axes, `packages/languages/<target>/` plus `packages/native/<lang>/`, columns `native_language` and `target_language`.) Interfaces that changed name or shape in this pass: `episodes.state`; `POST /v1/episodes/next` and `episode_kind = daily_extra`; `learners.{native_language,target_language,residence_country,plan}`; `plans.yaml` and `subscriptions.plan`; `media_objects.encryption` and presigned URLs for show audio; `word_uses`; `learner_schedule.expects_drop`; `research_pseudonyms`; `forone_admin`; `guard.check_output` item 6; the removal of `notes`, `margin_notes`, the notes door and `note_shown`; package paths `packages/lang/<target>` and `packages/native/<lang>`; `keys.get_dek` cache semantics; `vendor_calls` written in its own transaction; `measures/hourly`.

---

## 5. What the PRD-v3 thread needs to carry

Parts of PRD-v2 that these rulings change: 1.4 (plans, prices, payments, platform note unchanged); 2.2 A9 (residence country question, consent per native language); 3.6 (allowance by plan, "next one"); 5.5 and 5.6 rule 6 (notes and margin note removed); 6.3 check 10 (widened to corrections); 7.3 (Salma's language is the learner's native language); 8.6 (host brief's echo plan); 10.2 (no stage 1 notes; the pass is one function); 12.5 and 12.6 (regimes, region default); 13 (two package kinds); 14.3 (Langfuse rule, embeddings vendor); 14.5 (cost lines, margin by plan); 15 (notes budget removed); 16.1 (gates re-dated; renewal reads all subscribers); 18 (open items replaced by section 10 here); 19 (dates).

---

## 6. Dates, in one table

| Milestone | First drafts | Now |
|---|---|---|
| Milestone 0 | 2026-10-12 to 11-01 | 2026-10-24 to 11-18 |
| Recognizer test | by 2026-11-08 | by 2026-11-10 (during Milestone 0) |
| Voice decision, `vendors.yaml` committed | 2026-11-13 | by 2026-11-17 |
| Counsel: region, consent copy, crisis lines | 2026-11-01 and 11-16 | 2026-11-17 (before build week 1) |
| Build | 2026-11-02 to 12-06 | 2026-11-18 to 12-22 |
| Payment processor and entity | 2026-11-16 | 2026-12-02 (start of build week 3) |
| Exit (measured cost, costed path) | 2026-12-06 | 2026-12-22 |
| Beta opens, first cohort | 2026-12-07 | 2026-12-23 |
| Gemini prices double | 2027-01-01 (beta week 4) | 2027-01-01 (beta week 2) |
| First finales | 2027-01-03 | 2027-01-19 |
| First "active in week 4" readable | 2027-01-04 | 2027-01-20 |
| Gate review | 2027-01-10 | 2027-01-26 |

---

## 7. Build plan for 2026-11-18 to 2026-12-22

The five weeks keep the contents of each document's section 7, moved by 16 days, with these cross-domain changes placed where they must land.

| Week | Dates | Cross-domain items added or moved by this pass |
|---|---|---|
| 0 (Milestone 0, in parallel) | 2026-11-01 to 11-17 | `vendor-lab gate --target en` on the pilot's clips and scripts (ADR-03); `vendors.yaml` committed by 11-17; counsel's answers on region, consents and crisis lines by 11-17; Terraform written for `eu-central-1` with the region as one variable (ADR-08) |
| 1 | 2026-11-18 to 11-24 | `learners.{native_language,target_language,residence_country,plan,tz}`; the two package directories with `lang/en` and `native/ar` and `native/en` skeletons (ADR-02); `media_objects.encryption` and the two bucket policies (ADR-12); `vendor_calls` own-transaction write and the worker S3 spool (ADR-13); `events` append-only with `call_turn_verbatim`; `word_uses` DDL (ADR-19); `forone_admin` and `forone_human` roles (ADR-17); `keys.get_dek` with the 60 s versioned cache (ADR-18); logging and paging skeleton (09) |
| 2 | 2026-11-25 to 12-01 | Teacher's multi-episode day plan and `daily_extra` kind in `episode/produce` (ADR-05); editor check widened to corrections (ADR-06); Google embeddings (ADR-10); editor fallback on Opus (ADR-11); Langfuse metadata-only wiring with the pseudonym (ADR-09); `eval-gate` with the per-package path map; staging stays up from here (ADR-16) |
| 3 | 2026-12-02 to 12-08 | `plans.yaml`, allowance by plan, `POST /v1/episodes/next`, the "next one" control (ADR-04, 05); A9 with the country question and consent per native language (ADR-20); payments scaffold on the chosen processor with the three plans and the founding lock (ADR-21); processor decision by 12-02 |
| 4 | 2026-12-09 to 12-15 | Correction guard in the worker and chat paths (ADR-06); crisis clips per pair and resources per country (ADR-20); `talkback_stt` language hint per learner (ADR-02); `call-bench` 50-call run on the English stack; per-plan cost guard (ADR-15) |
| 5 | 2026-12-16 to 12-22 | `session/after-pass` as one function (ADR-06); `measures/hourly`, `privacy/verify` hourly, `drops_late_systemic`, the binding release window (ADR-16); "Margin by plan" in the weekly report (ADR-15); the end-to-end run with the Milestone 0 learners under a consent that covers it; the exit document with measured cost and the costed path |

**Freeze:** 2026-12-21 12:00 to 12-24 12:00 UTC. **Beta week 2 (2027-01-01):** the Gemini doubling lands; the voice plan from 08 §6.1 note 3 is executed in the first release after 2027-01-02.

---

## 8. Alternatives rejected in the cross-domain pass

| Alternative | Why rejected |
|---|---|
| Revising only 07 to 09 and leaving 01 to 06 on the old decisions | The technical design would inherit two incompatible products (one pair, SAR, notes; versus anyone anywhere, USD tiers, invisible teaching) |
| Keeping one package per language pair | n × m packages; the native side needs strings and a voice, the target side needs a gate; they change at different rates |
| Pre-producing every episode of the allowance in the nightly batch | About a third of the voice line spent on episodes 50% of learners never ask for; the on-demand path already meets 30 s |
| Keeping Salma's notes behind a flag "in case Muath changes his mind" | A flag never changes a law (09 D8); decisions.md says the reversal would be his explicit call, and the correction guard would then need a hole |
| A region per learner (EU for Europeans, UAE for Gulf learners) | Two of every store and job for a two-engineer team; one region plus the vendor transfers that every option shares is the honest minimum |
| Blocking signups from countries counsel has not reviewed | Contradicts "anyone, anywhere"; the generic notice plus the strictest regime's controls is the defensible default, confirmed by counsel |
| Leaving `episodes.status` and `episodes.state` to the integrator | The integrator is this pass |

---

## 9. How the findings were applied

| Document | Reviews applied on 2026-11-06 | Status after this pass |
|---|---|---|
| 01 System topology | Cross-domain rulings only (its two reviews were applied on 2026-10-17) | Revised to the 2026-10-23 decisions |
| 02 Generation pipeline | Cross-domain rulings only (its two reviews were applied on 2026-10-17) | Revised to the 2026-10-23 decisions |
| 03 Live call and voice | Conformance (24 findings) and skeptic (19) reviews of 2026-10-21, plus the rulings | Reviewed twice, revised |
| 04 Learner model and data | Conformance (24) and skeptic (30), plus the rulings | Reviewed twice, revised |
| 05 Assessment and after-session | Conformance (28) and skeptic (22), plus the rulings | Reviewed twice, revised |
| 06 Client and delivery | Conformance (20), plus the rulings; no skeptic review exists | Reviewed once, revised |
| 07 Security, privacy, compliance | Conformance (12) and skeptic (11) of 2026-11-06, plus the rulings | Reviewed twice, revised |
| 08 Cost model and vendors | Conformance (9) and skeptic (9) of 2026-11-06, plus the rulings | Reviewed twice, revised |
| 09 Evaluation and operations | Conformance (8) and skeptic (10) of 2026-11-06, plus the rulings | Reviewed twice, revised |
| 10 Decision records | None; the integration pass of the same evening added ADR-23 and the ten naming rows in §4 | Written, unreviewed |

Where a finding's fix was applied, the document says so in its section 11 (revision log) and the finding stays in `_review-findings.md` as history. Where a finding was declined, the revision log says why. The skeptic review of 06 was never run and is the one review still missing.

---

## 10. Open for Muath

The register of everything only Muath can settle, across the ten documents. The domain in brackets waits on the answer.

1. **Home region and the legal view on storing learner voice (counsel, by 2026-11-17).** ADR-08 makes `eu-central-1` the default for a worldwide cohort and keeps `me-central-1` as a one-day config move. Counsel confirms: where a worldwide cohort's voice recordings and transcripts may rest, the transfer basis for the US model, voice and recognition vendors (standard contractual clauses plus consent is the working assumption), whether voice used only for the learner's own progress counts as biometric data under GDPR or PDPL, and whether the in-session verbatim "yes" is explicit consent for sensitive-class facts. [01, 07]
2. **Which jurisdictions the beta covers on day one (counsel, by 2026-11-17).** Recommended: EU and UK GDPR, Saudi PDPL and the generic baseline; signups from unreviewed countries accepted under the generic notice. Also the DPIA, the consent and notice copy per native language, and the reviewer and tagger confidentiality agreement. [07, 06]
3. **Payment processor and legal entity (by 2026-12-02).** A merchant-of-record processor (Paddle, about 5%) handles tax in every country; Stripe with Stripe Tax (about 3% plus registrations) needs an entity in a Stripe country. Trial without a card (PRD 18 #4) is assumed. [07, 01, 06]
4. **Tier prices against the break-even.** At the post-doubling floor stack ($0.43 to $0.45 a session) the 2 and 3 a day plans lose money on a learner who uses every episode (break-even $0.42). Options: keep the prices and accept the loss on full-use learners (typical use is about half), raise 2 a day to $34.99, or commit to the voice contract in #5. The exit document on 2026-12-22 carries the measured number. [08]
5. **The last lever to $0.35 and the voice contract (by 2026-12-22).** A negotiated voice rate near $12 to $15 per million characters (no product change), read-aloud and recap rendered on first tap (about four engineer-days across 02, 03 and 06 and a 2 to 4 s wait), or 5-minute calls (in tension with the 4-minute speech gate). If Gemini wins the English blind test, decide the January plan now: swap the episode voice to the runner-up on 2027-01-01 with the on-air line, or ask Google for a rate. [08, 02, 03, 06]
6. **Haiku 5.5 as the call host** if the 50-call comparison in build week 4 shows no difference in move-contract violations, talk share and the human read; worth $0.046 a session. [03, 08]
7. **On-call for a worldwide cohort.** With learners in every timezone there is no quiet hour. Accept that in the beta a one-engineer rota answers overnight P1s with the product's fallbacks (yesterday's episode stays; voice notes) and a human at the next working hour, or fund a second responder; and approve Better Stack's on-call plan (about $30 a month). [09, 01]
8. **Web or native for the beta.** The architecture builds the installable web app plus the private feed (decisions.md §7's recommendation); the switch-to-native triggers (calls abandoned on the move, feed-to-call handoff lost) are measured from day one. This stays open as the coordinator asked; nothing in this pass changes it. [06, 01]
9. **Fixed infrastructure budget: about $1,000 to $1,300 a month** (01's $800 to $1,100 plus staging kept up through the beta, ADR-16), plus vendor minimums (voice winner's paid tier $100 to $330, LiveKit Ship $50, Langfuse Core up to $59, Speechace, Better Stack $30) and the Anthropic prepaid balance (about $2,500 for the beta's first month at the upper plans' usage). [01, 08, 09]
10. **Second engineer, and the week-6 slips** (01 §10 #5). Decide by 2026-11-18. [01]
11. **The reviewers.** A paid native reader per target language (English first; about 4 hours a day at 100 learners, less with 09's cut), who also performs the language gate's writing check; the claims auditor (Muath or a second trained person); the native-language law-scan reader (Muath for Arabic). [09, 02]
12. **Crisis protocol details (counsel, by 2026-12-15).** Clip wording per pair, the per-country resources list and the international fallback, whether the keyword list may fire alone (ADR default: the host confirms first, 2-second cap), whether SB 243 applies, and whether Muath wants to be told of activations and write personally. [07, 03]
13. **Consents for Milestone 0 data** (01 §10 #11): the vendor-test addendum before any clip leaves (by 2026-11-01), and whether the pilot consent covers re-onboarding the 15 learners in build week 5 and keeping de-identified fixtures. [01, 07, 09]
14. **Processors to approve** (07 §4.9 as revised): Langfuse Cloud EU under ADR-09, Resend with tracking off, Sentry EU, Vercel, LiveKit Cloud, Inngest EU, the verbatim recognizer with minimum retention; and the Anthropic zero-data-retention request. [07, 01, 08]
15. **Smaller items that stay with their documents:** archive growth (01 §10 #7), WhatsApp invites (01 #8), the 30 s median / 45 s p95 budgets (01 #9), the PRD 3.10 amendment for two transactional emails (01 #10), the brand domain (01 #13), research rows after deletion (04 and 07: deleted), the export passphrase (04), the "very disappointed" question mechanism (09), pulling a shipped episode (09 R4), the stop line's owner and window (08, 09: a human, 48 hours), the daily cap formula (08), cost figures in the review packet (08), staff passkeys and a penetration test before public launch (07), age verification beyond self-attestation (07), waitlist retention (07), the first rater window to 2027-02-16 (05 §10 #6), and the fact that `renewal_m2` for the first cohort is not readable before the 2027-01-26 gate review (09): the review reads it as "not yet".

---

## 11. Revision log

- 2026-11-06: written. Companion changes: `_review-findings.md` gained the six reviews of 07 to 09; the nine domain documents were revised to these records; the pages and hub were rebuilt.
- 2026-11-06, evening: integration pass after the nine parallel revisions. ADR-23 added; §4 gained ten rows for names two documents spelled differently; the post-doubling floor is now $0.43 to $0.45 (08 §6.3, after re-adopting 02 §6's unit table); ADR-02's package path is `packages/languages/<target>/` to match the engineering handbook; the pseudonym has no secret (07). The edits were applied to 01, 02, 03, 06, 08 and 09 directly.
