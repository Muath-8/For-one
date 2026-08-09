# 00 — Canonical Decisions & Conventions

**Status: BINDING. Every document in `docs/specs/` must conform to this file. If any document contradicts this file, this file wins and the other document has a defect. One source of truth per fact: each fact names its owning document; other documents cite the ID, never restate the value.**

Precedence: `00-decisions.md` → other `docs/specs/*` → `docs/*` (source material, historical). Exception: `docs/For_one_Design_System_and_UI_Specification.md` (2026-08-08) is **adopted as the canonical design authority**; specs 02 and 03 are its normative split plus the deltas in §9.3 below (ADR-0016).

Normative language: RFC 2119 MUST/MUST NOT/MAY. Forbidden in normative sections of every spec: "TBD", "for example", "such as", "could", "or similar", "etc.".

---

## 1. Product identity

| Fact | Decision |
|---|---|
| Product name | **For one** (user-confirmed 2026-08-08; "Lucent" in older docs is dead) |
| One-sentence promise | Your own podcast, in the language you're learning — where you're the co-star. |
| Platform | Responsive web app only. Fully functional on mobile Safari ≥ 17 and mobile Chrome ≥ 120; desktop Chrome/Edge/Firefox/Safari last 2 majors. No native apps in v1. |
| Audience | 18+, self-declared birth date at signup; under-18 rejected with the plain message owned by 02. |
| Business model | Deferred (user decision). No pricing surface and no Stripe integration in v1. Cost telemetry mandatory from day one. |
| Session cap | Hard cap 2 completed-or-started sessions per calendar day in the user's local timezone (IANA zone captured client-side at signup, refreshed every app open). Never advertised; 3rd attempt gets the in-character host line (copy owned by 02). |
| Session vocabulary | User-facing stage labels are **Episode / Notes / Call-in / After-show**; destinations are **Today / Archive / Your show**. Internal stage names `listening` / `reading` / `speaking` / `chatting` appear only in engineering docs. |
| Person vocabulary | Engineering documents (01–06, 08, 09) say **"user"**. **"Listener"** is reserved for the registers where the show's own voice speaks: 07's prompt texts, verbatim interface copy quoted from 02, and the user-story narrative voice in 01 §5. In all other engineering prose, "listener" is a defect. |

**Product laws (bind every spec; the automated law scan enforces them at generation time):**

1. No lesson furniture anywhere: no levels, courses, streaks, points, tests, badges, dashboards, charts, prompt boxes, or homework — in any wording, any surface, any language.
2. User owns topic, format, and cast. The sole cast exception is ADR-0022's terminal reviewed-folio recovery after the selected-cast generation path is no longer shippable: the package-authored duo delivers that one cycle and the interface attributes the actual duo plainly. The system owns difficulty, targets, corrections, and sequencing — invisibly.
3. Sessions are self-contained; only memory persists between sessions.
4. Characters are transparently AI; no guilt mechanics, no re-engagement messaging, no dark patterns.
5. In-flow correction is recast-only; explicit correction only on explicit user request.
6. Internal CEFR anchoring is never surfaced in any form or wording.
7. Recasts must be socially natural; hosts never grade or praise per-turn.
8. Conversations end like conversations; the interface ends ("That's the show").
9. Trust contract: never lie, never manipulate, never hide what it is, prove progress honestly (flat weeks included), the data is theirs — see it, export it, delete it.

**Resolved contradictions (user-ratified 2026-08-08):**

- **Name:** For one.
- **Data rights (ADR-0001):** full data **export** and full **account deletion** ARE in v1, reversing PRD v2.0 Part 12.8. Voice-clip deletion on consent revocation ≤ 24 h stays. Account deletion purges primary stores ≤ 24 h; backups age out ≤ 30 days under a deletion-on-restore policy. The design doc's "unsupported data actions" paragraph and QA-gate line are superseded (§9.3).
- **Languages (ADR-0002):** one package-generation pipeline produces content packages for **every language supported by both `eleven_flash_v2_5` (TTS) and `scribe_v2` (STT, ADR-0019)**; all available at launch. The enumerated catalog is seed data owned by 06.
- **Planner:** the steady-state pitch-set replacement planner is event-hooked by exactly post-session, staleness, and follow-up-due triggers, never nightly cron and never manual refresh (ADR-0009). The one-pitch onboarding initialization is a separate workflow and MUST NOT enter the planner trigger register. "Nightly/overnight planner" wording in source docs is dead.
- **Weekly Proof window identity (ADR-0023):** assessment week W is the completed user-local Monday–Sunday interval rated at Monday 03:00 in W+1. Its Proof delivery week is that immediately following user-local Monday–Sunday interval W+1. The preferred-weekday slot is 09:00 local inside the delivery week; a late Proof may surface only on the next app open before the following Monday 00:00 exclusive, then is silently omitted.
- **Email:** transactional only — verification, password reset, export-ready notice, deletion confirmation. Never re-engagement, never digest.
- **Settings (ADR-0003):** no settings/preferences screens. "Your show" sheet (per design doc) holds Cast, What the show knows, Voice tape, About this AI show, and Account essentials; Account essentials now additionally holds **Export my data** and **Delete my account**. All behavioral preferences remain conversational.

## 2. ID schemes & traceability (owner: this file)

| Artifact | Scheme | Owner doc | Example |
|---|---|---|---|
| Feature | `F-##` | 01-prd | F-07 |
| User story | `US-<epic>.<n>` | 01-prd | US-3.2 |
| Functional requirement | `FR-###` | 04-srs | FR-101 |
| Non-functional requirement | `NFR-##` | 04-srs | NFR-04 |
| Screen | `SCR-##` | 02-ux-spec | SCR-05 |
| Screen state | `SCR-##/S<n>` | 02-ux-spec | SCR-05/S3 |
| Component | `DS-<PascalCase>` | 03-design-system | DS-ProgrammePitch |
| Design token | as defined by the design doc (`paper-50`, `color.bg.canvas`, `space-4`, `motion-standard`) | 03-design-system | `broadcast-700` |
| Entity / table | PascalCase prose / snake_case plural tables | 06-data-api-spec | LearnerFact / `learner_facts` |
| API endpoint | REST `/api/v1/<kebab>` | 06-data-api-spec | `POST /api/v1/sessions` |
| Background job | `JOB-<kebab>` | 05-tdd | JOB-post-session |
| Prompt | `PRM-<kebab>@v<n>` | 07-ai-spec | PRM-episode-script@v1 |
| Model role | `MDL-<kebab>` | 07-ai-spec | MDL-realtime |
| Error code | SCREAMING_SNAKE closed catalog | 06-data-api-spec | SESSION_CAP_REACHED |
| Endpoint ID | `EP-##` | 06-data-api-spec | EP-17 |
| Copy string | `COPY-###` | 02-ux-spec Appendix A | COPY-165 |
| Invariant | `INV-<AREA>-<n>` | 05-tdd §13 | INV-COST-1 |
| Query register entry | `Q-<KEBAB>` | 06-data-api-spec §14 | Q-DEFINITION-CACHE-PROBE |
| Rate-limit class | `RL-<KEBAB>` | 06-data-api-spec §11.1 | RL-SESSION-CREATE |
| Test case | `TC-####` | 08-eval-testing-plan | TC-0117 |
| ADR | `ADR-####` | 09-adrs/ | ADR-0004 |

`US-x.y` user-story IDs are narrative aids inside 01; the binding chain is F → FR → TC, and no downstream document is required to cite a US ID.

**Traceability chain (Phase-3 reviewers verify mechanically):** every F-## → ≥1 FR-###; every FR-###/NFR-## → ≥1 TC-####; every user-facing FR names its SCR-##; every AI-behavior FR names its PRM-*; no orphans in either direction.

## 3. Stack (pinned; owner: this file for the list, 05-tdd for wiring)

| Layer | Choice | Pin |
|---|---|---|
| Language | TypeScript, `strict: true` | 5.9.x |
| Runtime | Node.js | 22 LTS |
| Framework | Next.js App Router + React | Next 15.4.x, React 19.1.x |
| Styling | Tailwind CSS mapped to the design-doc tokens | 4.1.x |
| ORM & migrations | Drizzle ORM + drizzle-kit SQL migrations (ADR-0006) | 0.44.x |
| Validation | Zod — the single validation library everywhere | 4.x |
| Database | Supabase Postgres + pgvector | Postgres 16 |
| Object storage & CDN | Supabase Storage behind its CDN. Signed URLs for every user-owned/derived object; the authored `catalog` bucket is public-immutable (ADR-0017) | n/a |
| Auth | Clerk: email+password, Google, Apple (ADR-0014) | @clerk/nextjs 6.x |
| Jobs | Trigger.dev (all async pipelines, retries, idempotency) | v4 |
| Cache / locks / rate limits | Upstash Redis | @upstash/redis 1.x |
| Real-time voice | LiveKit Cloud + LiveKit Agents, Node (ADR-0011) | @livekit/agents 1.x |
| LLM gateway | OpenRouter — every LLM call; model matrix owned by 07 | API v1 |
| Embeddings | OpenAI `text-embedding-3-small`, 1536 dims (ADR-0007) | n/a |
| TTS | ElevenLabs `eleven_multilingual_v2` (produced audio), `eleven_flash_v2_5` (real-time) | n/a |
| STT | ElevenLabs Scribe `scribe_v2` (batch) + `scribe_v2_realtime` (live) (ADR-0019) | n/a |
| World check / news | Exa API | n/a |
| Email | Resend | n/a |
| Analytics / errors / flags | PostHog — sole tool for all three (ADR-0013) | posthog-js 1.x |
| Testing | Vitest (unit/integration), Playwright (E2E + cross-browser), axe-core (accessibility, inside Playwright), k6 (load) — suite membership and budgets owned by 08 | Vitest 3.x, Playwright 1.x, axe-core 4.x, k6 0.x |
| Hosting | Vercel (app), LiveKit Cloud (voice agent), Trigger.dev cloud (jobs) | n/a |

Exact patch versions freeze in the lockfile at scaffold; majors/minors above are binding. No library may introduce a second way to do something this table covers.

**Regions (ADR-0008):** Vercel `iad1`, Supabase `us-east-1`, Upstash `us-east-1`, LiveKit Cloud US East, Trigger.dev US. Single region v1; the 10×/multi-region path is written in 05, not built.

## 4. Architecture style (owner: 05-tdd for full detail)

- **Modular monolith**, one repository, one Next.js app — plus exactly two satellite runtimes: the LiveKit voice agent (own deployable, same repo) and Trigger.dev tasks (same repo). No microservices, no event bus, no extra queues (ADR-0004).
- Modules (folder = boundary; cross-module imports only via each module's public `index.ts`): `identity`, `learner-file`, `cast`, `planner`, `generation`, `session`, `realtime`, `assessment`, `proof`, `archive`, `trust`, `telemetry`, `language-packages`, `lexicon`.
- All client↔server data flows through REST route handlers under `/api/v1/*` (ADR-0005). No client-side Supabase queries (ADR-0012). Server actions are not used for data mutation (one-path rule).
- Postgres RLS enabled on every user-owned table as structural defense; app code adds repository-layer `userId` scoping; Trigger.dev tasks and the agent use service role only through the same scoped repositories. Single sanctioned exception: the read-only `app_scanner` role for scheduled-job discovery over the content-free scan views enumerated in 06 §7.4 (ADR-0018); all fanned-out work runs user-scoped.
- Generation and assessment never run in request handlers; they run as Trigger.dev tasks with idempotency keys. The only latency-critical server path is the real-time voice loop, which lives in the LiveKit agent.

## 5. Data model core (owner: 06-data-api-spec for field-level schema)

Entity census — 06 defines exactly these; adding an entity requires an ADR:

`users`, `language_packages`, `dialects`, `voices`, `characters` (authored duo + created; chassis enum of 6; active/retired), `character_memories`, `learner_facts` (typed memory with salience, confidence, provenance, dormant flag), `interests`, `follow_ups`, `pitches` (atomic set replacement), `sessions` (state machine `pitched → listening → reading → speaking → chatting → complete`, `abandoned`, pause sub-state), `episodes` (script + audio ref + word-timed transcript), `articles`, `call_turns` (transcript always; audio ref only under consent), `chat_messages`, `definitions` (pre-computed word-in-context), `define_events`, `targets` (lifecycle active/taking/retired/recheck), `error_observations` (12-category taxonomy; raw evidence + structured tag), `assessments` (weekly CAF), `vocab_items` (rings × receptive/productive), `proofs`, `planner_runs`, `generation_jobs` (per-stage pipeline state + QA gate results), `cost_events`, `consent_events` (append-only), `export_jobs`, `deletion_jobs`, `embeddings` (pgvector, typed by source).

Rules: evidence and interpretation live in separate rows and interpretations are regenerable; every inference carries confidence + provenance; happened-things are append-only (turns, messages, observations, consent), is-things mutate (users, fact salience). CEFR is stored as `level_band` (`A1..C2`) + `level_step` (1–3) + `level_confidence` (`calibrating|normal`) and MUST NOT appear in any API response schema.

## 6. API conventions (owner: 06 for the endpoint catalog)

REST, JSON camelCase, Clerk session JWT in `Authorization`. Single error envelope: `{ "error": { "code", "message", "requestId" } }` with the closed code catalog in 06. Status mapping: 400 validation / 401 unauthenticated / 403 forbidden / 404 not-found-or-not-yours / 409 state conflict / 422 domain rule / 429 rate limit / 500 internal / 503 upstream unavailable. Cursor pagination (`cursor`, `limit` default 20 max 100 → `{ items, nextCursor }`). Mutating POSTs accept `Idempotency-Key`; it is REQUIRED on session-creating and generation-triggering endpoints. LiveKit room tokens come from `POST /api/v1/call-tokens`; audio never transits our API. APIs are designed around product behavior (accept pitch, get on the line), not entity CRUD.

## 7. AI conventions (owner: 07 for prompts, model matrix, budgets, fallbacks)

- Model roles: `MDL-author` (pitches, episode scripts, articles, proof scripts, intake persona), `MDL-realtime` (call-in + after-show), `MDL-judge` (QA gate, pitch test, uptake rating), `MDL-assess` (error extraction, weekly CAF), `MDL-lexicon` (definitions/translation), `MDL-package` (language-package generation). 07 pins one OpenRouter model ID + an ordered fallback chain per role and routes by task complexity (cheap models wherever measured quality permits).
- Structured outputs everywhere: every non-conversational call has a Zod schema validated on exit; one retry on validation failure, then the role's designed fallback. Model output is evidence, never truth — every write to `learner_facts` / `targets` / `error_observations` passes a deterministic gate (schema + rule checks + confidence threshold).
- Prompts are versioned in-repo artifacts (`PRM-*@v<n>`); every call logs prompt version, model ID, tokens, latency, cost, validation outcome, and disposition — queryable per user session (the observability questions in 05 §9 and §9.3).
- Context assembly is retrieval-based and budgeted per role; full history is never sent. User isolation is structural: context builders accept `userId` and can only read that user's rows.
- Provider privacy posture: OpenRouter training-opt-out; ElevenLabs no-retention where offered; the exact data-to-provider inventory lives in 07 §12 and §12.2.

## 8. Budget envelopes (normative NFR copies live in 04-srs)

Latency (from PRD v2.0 Part 14, unchanged): pre-generated episode start < 2 s · on-selection playable < 30 s (streaming) · first episode < 3 min · call-in voice response < 1.5 s end-to-end · tap-to-define popover < 300 ms (pre-computed) · post-session analysis ≤ 10 min · staleness pitch refresh < 5 s at app open · voice-clip purge ≤ 24 h · live-voice failure degrades to voice notes with zero session loss.

Cost: fully-loaded variable cost ≤ **$1.50 per completed full cycle at p50**; alert at $2.50 p95. Every session writes `cost_events`; weekly review against the 2-sessions/day worst case. 07 owns the per-stage breakdown that must sum inside this envelope.

## 9. Design authority (owner: 02 + 03, derived from the design doc)

### 9.1 Adopted as-is
`docs/For_one_Design_System_and_UI_Specification.md` is canonical for: Paper/Booth/Proof environments (no user theme setting), all color/type/spacing/radius/motion/z tokens, the component system, screen compositions, responsive rules, i18n/RTL rules, accessibility standard (WCAG 2.2 AA), content voice, example copy, QA gates. Typefaces: Source Serif 4 + Inter (+ Noto per-script pairs).

### 9.2 Spec split
03-design-system = foundations + tokens + components + motion + iconography + accessibility standards (with DS-* IDs). 02-ux-spec = IA + journeys + every screen SCR-## with every state + exact copy catalog (with the design doc's copy adopted verbatim). Neither may alter an adopted value without an ADR.

### 9.3 Deltas the split MUST apply (the only permitted changes) and ratified additions

Copy adoption is verbatim **including typographic punctuation** (curly quotes/apostrophes, em dashes, ellipses); ASCII normalization is a fidelity defect. The `[source]`/`[new]` tags in 02's copy catalog record provenance only, never typography: `[new]` strings MUST follow the authority's typographic punctuation rules exactly as `[source]` strings do, and a `[source]` tag MUST be carried only by a rendered string with a byte-exact Unicode counterpart in the authority after removing Markdown emphasis delimiters (`*` or `**`) around the same words. No other whitespace, punctuation, token, wording, or markup normalization is permitted. A string composed or derived from authority prose is `[new]` with a composition note in 02 Appendix A.1. Two 03 additions are ratified post-review (they add enforcement without altering any adopted value): §5.10 token governance and component rule 7 (environment declaration). Any other addition or narrowing of adopted wording is a defect.
1. **Export & account deletion exist (ADR-0001):** "Your show → Account essentials" gains **Export my data** (async job → in-app banner + email when ready; signed link, 7-day expiry) and **Delete my account** (type-to-confirm; consequence text; immediate sign-out; ≤ 24 h purge; confirmation email). The design doc's "Unsupported data actions" paragraph, "Unsupported deletion copy" note, and the QA-gate line about unsupported export/deletion are superseded; 02 writes the exact copy for both flows in the established legal/consent voice.
2. **ID overlay:** screens get SCR-## and components DS-* identifiers.
3. **Banned-lexicon consolidation:** 02 owns the complete banned word list (design doc vocabulary rules + law-scan list) as one catalog the QA gate and copy reviews cite.
4. **Knowledge-summary honesty wording stays** ("Stop using this in the show" = dormancy) — unchanged, but 02 adds one sentence distinguishing it from account deletion, which now exists.
5. **Authored-duo names are runtime data:** where the adopted document's default-pair copy names Inés and Rafa, 02 preserves the sentence as an exact two-name template and substitutes the actual package-authored duo selected by the user's dialect. A non-default duo MUST NOT be mislabeled as Inés and Rafa.
6. **Generation recovery is automatic:** FR-416 owns one automatic primary regeneration. FR-417 then owns a generated callback-free fallback with at most one regeneration of its own before the reviewed terminal folio. FR-411 forbids model generation in a request handler. The adopted design's client retry/simpler-generation actions are replaced by honest no-action recovery states; only an infrastructure failure before any onboarding pitch exists retains the explicit EP-11 retry. If publication of the reviewed terminal folio itself exhausts its infrastructure bound, no partial folio becomes readable: EP-52 exposes the one closed `support_required` result and 02 renders persistent human support with no Retry. That terminal-publication failure is the sole exception to FR-027/FR-418's first-frame/show-delivery guarantees; Today and all previously completed work remain available.
7. **Unsafe topics are refused without consuming a session:** FR-117 and 07's safety policy require a closed, in-character refusal before any pitch/session write. SCR-07 and SCR-08 add the exact refusal state and 02-owned reason copy because the adopted design has no refusal surface; no different topic is substituted.
8. **Terminal live degradation is one-way:** after any FR-230 terminal cause is durable, the adopted design's “try live again” action is removed. The only action is the voice-note continuation; microphone permission denial retains its browser-permission retry before degradation is committed.
9. **Planner failure preserves a complete programme:** FR-127's package-authored starter set replaces the adopted design's one-pitch fallback and client retry. `SCR-06/S5` and `COPY-069` are retired; a world-check failure remains invisible and a terminal planner failure publishes a normal complete set.
10. **The cost guard has honest, distinct copy:** the per-user money guard is not the two-session cap. When it blocks new work, 02 owns a separate no-number explanation and existing completed work remains usable; `COPY-083` is reserved exclusively for the third-session attempt.
11. **Terminal authored-folio cast is attributed honestly (ADR-0022):** only after the selected-cast path exhausts FR-417's generated mode, an eligible stage exhausts its 05-owned provider/orchestrator bound with `orchestrator_exhausted`, the first-episode deadline claim wins, or an already-readable generated epoch cannot close inside its applicable FR-027/FR-210 duration band and claims `postpublication_duration_failure`, the reviewed package-authored duo MAY deliver the terminal folio. The last case is the sole manifest-epoch replacement: the current segment ends cleanly, the old epoch is retired, position resets, and exact 02-owned copy announces the authored folio before a new Play. The selected cast remains recorded; every delivered surface uses and names the actual authored duo. No ordinary generation, cost decision, or pedagogical decision may substitute cast.
12. **Forward stages never observe a replaceable episode folio:** Notes MAY open before playback reaches the end, but only after the active episode manifest has a terminal duration and its epoch is frozen. Until the 06-owned `content_terminal_at` writer commits, the Notes transition remains unavailable and the session cannot advance from `listening` to `reading`. Once it commits, no manifest/folio replacement is legal. This narrows only the adopted design's early-navigation timing; it does not require the user to finish listening.

## 10. Security, privacy, trust (owner: 05 for mechanics, 06 for schema)

RLS + repository scoping on every user table; a mechanical "A cannot read B" test per resource in 08. Secrets only in platform vaults; Clerk webhooks svix-verified; signed URLs for all media; SSRF-safe world-check fetching (Exa only, no arbitrary URL fetch). Voice audio written only when `voice_consent = true` at record time; consent history append-only. Export/deletion flows per §1. Prompt injection: external world-check content is data-not-instructions and everything it touches passes the QA gate; user free-text steers content, never pedagogy rules or isolation. Rate limits use Upstash and the closed endpoint-class catalog in 06 §11.1. Generation count is bounded only by the two-session cap, the one onboarding alternative, FR-416's one primary quality-gate regeneration, FR-417's one generated-fallback quality-gate regeneration, and FR-210's one synthesized-duration regeneration in each generated execution mode; there is no independent universal daily generation counter. Duration validation is the deterministic `audio`-stage edge and is not a sixth FR-415 check. The separate per-user money guard is an admission backstop, not a count budget. Tap-to-define is a local lookup over complete delivered data under ADR-0010 and has no endpoint rate limit.

## 11. Environments & delivery (owner: 05)

`local` (Supabase CLI + Trigger.dev dev + LiveKit dev project) → `preview` (Vercel previews + branch DB) → `production`. Trunk-based; merges to `main` ship after preview checks. Migrations forward-only, expand-and-contract. The v1 PostHog feature-flag registry is empty: character creation and Weekly Proof are mandatory v1 behavior and MUST NOT be gated. A future staged-rollout flag MAY gate only behavior that no active FR mandates, and 05 owns its expiry and removal. Rollback = redeploy previous build + never-destructive migrations inside a release window.

## 12. Document ownership map

| Doc | Sole owner of |
|---|---|
| 00 (this) | Cross-cutting decisions, conventions, ID schemes, stack list, product laws, budget envelopes |
| 01-prd | Features F-##, user stories, personas, success metrics, scope boundaries |
| 02-ux-spec | Screens SCR-## + states, exact user-facing copy, banned lexicon, IA |
| 03-design-system | Tokens, type scale, palettes, spacing, motion, components DS-* with variants/states |
| 04-srs | FR-###/NFR-## with exact limits, validation rules, state machines, failure behavior |
| 05-tdd | Architecture detail, folder structure, module contracts, auth flows, jobs JOB-*, env config, deployment, observability, threat model |
| 06-data-api-spec | Full schema (types, nullability, defaults, constraints, indexes, delete behavior), ERD, endpoints, error-code catalog, seed data (language catalog, chassis, taxonomy, formats) |
| 07-ai-spec | Prompt texts PRM-*, model matrix MDL-*, output schemas, context assembly, fallback tables, per-stage cost/latency budgets |
| 08-eval-testing-plan | Test cases TC-####, FR/NFR→TC matrix, AI eval sets + thresholds, release gates |
| 09-adrs/ | Decision rationales (context, alternatives, decision, consequences) |

## 13. ADR register (initial)

ADR-0001 data rights restored · ADR-0002 all-languages package pipeline · ADR-0003 Your-show sheet is trust surface, not settings · ADR-0004 modular monolith + two satellites · ADR-0005 REST over tRPC/GraphQL · ADR-0006 Drizzle over Prisma/Supabase-js · ADR-0007 OpenAI embeddings alongside OpenRouter · ADR-0008 single US region v1 · ADR-0009 event-hooked planner over nightly cron · ADR-0010 pre-computed tap-to-define over on-demand · ADR-0011 LiveKit Agents Node over Python with one same-room recovery/degraded-voice-note path · ADR-0012 no client-side DB access · ADR-0013 PostHog as sole analytics/errors/flags · ADR-0014 Clerk over Supabase Auth · ADR-0015 recast enforcement via prompt+gate design · ADR-0016 adopt existing design doc as canonical with §9.3 deltas · ADR-0017 public-immutable catalog media (narrows the signed-URL rule) · ADR-0018 scanner role for cross-user job discovery (narrows the scoped-repository rule) · ADR-0019 STT pin updated to Scribe v2 identifiers · ADR-0020 polling over SSE for session progress · ADR-0021 segment-manifest progressive audio playback · ADR-0022 terminal authored-folio cast attribution · ADR-0023 Weekly Proof assessment/delivery week identity.

**Lead rulings on 06 §17 flags (recorded here so reviewers treat them as settled):** intake and cast-creation transcripts stay bounded JSONB on `users`/`characters` in v1 (census unchanged; an ADR adds `conversation_turns` only if turn-level evals demand it); session-cap counting is the strict reading — every session row created on the local date consumes a slot, with accidental starts guarded by the active-session confirmation dialog and regeneration limited by the one onboarding alternative, FR-416's one primary regeneration, and FR-417's one generated-fallback regeneration; `deletion_jobs` deliberately has no FK to `users` (the receipt must outlive the account); dialect count per language follows ADR-0002's amended rule.

Authors may add ADRs; none may contradict this file without lead sign-off updating this file first.
