# For one: the epics

*Implementation backlog, written 2026-11-06; re-cut under ADR-24 and then ADR-25 on 2026-11-12. Version 1 is built by an AI coding agent under Muath, in phases ordered by dependency, and launches once, publicly, when every v1 story passes and the launch checklist is green (`00-release-plan.md`). There are no dates. Every story carries a `Phase`, a `Release` (v1 at launch, v1.1 after launch) and a `Requirements:` line (`05-traceability.md`). Sizes S, M and L are relative complexity only. Visual version: https://claude.ai/artifact/NFcJZpKpupvoVyH59Mhwjc (source: `release-plan.html`). Built from the agreed feature map, concept-v2.md, decisions.md, PRD-v3 and the architecture documents, with ADR-25 winning wherever they differ: no trial run and no beta, no lawyer, web only, no hired reviewers.*

**Sixteen epics.** E01 to E05 are the engine (infrastructure and the agent's workflow, vendors, the learner model, the pipeline, the call). E06 to E11 are what the learner meets (onboarding, the daily loop, the feed, assessment, the notebook, the proof). E12 to E15 are the business and the operations wrapper (plans, privacy, cost, evals and operations). E16 is the launch and the first season.

Each epic names its goal, its scope, what is out of scope, the measure that says it worked, and what it depends on. Stories live in `02-stories/<slug>.md`; the phases are in `00-release-plan.md`.

| Id | Epic | Architecture domain | Stories | Where it is built |
|---|---|---|---|---|
| E01 | Platform foundation and the agent's workflow | 01 topology, 09 operations | 10 | Phases 1, 2 and 6 |
| E02 | Vendor tests and the language gate | 02, 03, 08 | 9 | Phases 1 to 2; the gate harness in v1.1 |
| E03 | Learner model and event log | 04 learner model | 11 | Phases 1 to 6 |
| E04 | Episode generation pipeline | 02 generation | 13 | Phases 2 to 4 |
| E05 | The live call | 03 live call | 13 | Phases 2 to 5; round two in v1.1 |
| E06 | Onboarding: the first ten minutes | 06 client, 03, 07 | 11 | Phases 3, 4 and 6; the sample episode in v1.1 |
| E07 | The daily loop in the web app | 06 client | 13 | Phases 1 to 6; the Show tab in v1.1 |
| E08 | Private feed, drop and the one cue | 06 client, 01 | 7 | Phases 3 and 5 |
| E09 | After-session assessment | 05 assessment | 11 | Phases 4 and 5; the calibration set in v1.1 |
| E10 | Notebook, controls and Salma on demand | 06 client, 04 | 9 | Phase 5; the tape in v1.1 |
| E11 | Weekly proof, claim gate, recordings and seasons | 05, 02 | 10 | Phases 5 and 6; metric unlock and the finale in v1.1 |
| E12 | Plans, trial and payments | 07 security, 01 | 10 | Phases 3 and 5; failed payments in v1.1 |
| E13 | Privacy, security and compliance | 07 security | 12 | Phases 1, 3, 4 and 6; research de-identification in v1.1 |
| E14 | Cost tracing and vendor control | 08 cost | 8 | Phases 1, 2, 4 and 6; the failover drill in v1.1 |
| E15 | Evals, observability and operations | 09 operations | 11 | Phases 1, 2, 4 and 6; the health page and vendor regression in v1.1 |
| E16 | Launch and the first season | all | 9 | Launch; the health reviews in v1.1 |

---

## E01 · Platform foundation and the agent's workflow

**Goal.** One repository, one staging and one production environment, the shared services every other epic calls, and the working rules under which an AI coding agent builds everything else, stood up first so nothing later waits on them.

**Scope.** Monorepo with CI; the agent's instructions file, tests-first per story, an independent AI review pass in CI and Muath's approval gates on merges, migrations, prompt and bible changes and production deploys (ADR-25.2); `forone.core` (settings, database, migrations, the `events` contract); FastAPI `api` skeleton; Inngest with a hello function; Terraform for staging in `eu-central-1` reused for production (ADR-24.B19; VPC, RDS Postgres 16 with pgvector, S3 with KMS, ECR, ECS Fargate, ALB with WAF, Secrets Manager); Sentry and Langfuse wiring; staging deploy pipeline; the outbox and relay; messaging and rate limits; production stood up Multi-AZ with a restore rehearsal.

**Out of scope.** Multi-region, self-hosted LiveKit, Inngest or Langfuse, CloudFront for media, an API gateway, a message bus, native apps, a separate admin app.

**Success measure.** A story's tests are committed before its code and CI proves it; no change reaches `main` or production without Muath's approval; a commit on `main` deploys to staging without a hand; production restored from backup into staging within 4 hours before launch.

**Dependencies.** The vendor accounts and keys (register A1). `eu-central-1` is final (ADR-24.8, 25.3); a move is one Terraform variable.

## E02 · Vendor tests and the language gate

**Goal.** Choose every voice and speech vendor on measured results without a trial run, and make the language gate a repeatable test so a second language can open without a redesign.

**Scope.** The recognizer test (streaming and verbatim vendors) on about 30 volunteer clips with a one-line consent each and a speechocean762 sample (Apache-2.0) (ADR-25.6); the blind two-host voice test across Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4, rated by Muath and volunteers; the 50 scripted calls for latency, built from volunteer clips and agent-written scripts; `vendors.yaml` and the thin adapters for the winners only; the English language package (lexicon on wordfreq, lemmatizer, structure inventory built from open sources with English Grammar Profile-style ids per ADR-24.18, ban list, the drafted bibles, Salma strings); the gate harness with the five checks as runnable jobs (v1.1); a candidate second language through the harness after launch.

**Out of scope.** Shipping any target language other than English in v1 unless it passes all five checks; a self-hosted aligner; Hume.

**Success measure.** One table per vendor decision with the numbers (M2); the verbatim vendor keeps learner errors on at least 90% of tagged clips; the host answers in under 1.5 s median on the 50 calls.

**Dependencies.** Volunteer clips with consent (A2); Muath's read of the bibles (A3); cost tracing middleware so every test render is a priced row (E14).

## E03 · Learner model and event log

**Goal.** One append-only event log and one learner model (words, structures, errors, skills, life facts with quotes, show canon) that every role reads through a compiled brief and only after-session roles write.

**Scope.** `events` with partitions, RLS and idempotent append; the type registry; word bank with FSRS-style scheduling per word, structure and corrected form; structure map and observations; life facts with exact quote, confidence, sensitivity and expiry, the confirmation ladder and `verify_quote`; interests with decay; goals; show canon, side characters and the series bible excerpt; `briefs.compile` for teacher, writer, host, Salma, chat and proof; onboarding writes (intake cards, word check scoring, consents); after-pass apply; learner edits (veto, add, fix a fact); export content; delete purge order; rebuild from the log.

**Out of scope.** A separate analytics warehouse, CDC streams, cross-region replication, automated FSRS weight fitting before launch, per-learner physical partitions.

**Success measure.** A replay of a synthetic learner's 14 scripted days produces a word bank and error list that agree with the planted truth on 80% of items; every real life fact passes the quote check and every planted paraphrase fails it; no live role holds a write credential.

**Dependencies.** E01 database; the structure inventory from E02; the analyst output schema from E09; the synthetic fixtures from E15.

## E04 · Episode generation pipeline

**Goal.** A new episode for each learner before their drop time, every day, at about 95% known words, that passes an editor from a second vendor and costs a measured amount.

**Scope.** `episode/produce`: teacher (plan with one grammar target, 2 to 4 words, the right forms of the learner's own mistakes, three ideas for tomorrow), writer (script, article, call brief with planned host moves, chat opener), fitter (coverage in code, up to 2 rewrites), editor (correctness, no uncertain memory, the fun carries the language, nothing reads as a lesson or a correction, variety, laws, "would they pick this over a real podcast?"), voice studio (two voices, timings, names, re-listen), senses and glosses, publish; batch mode with the on-demand fallback 90 minutes before drop; on-demand kinds (first, sample, swap, return, small-door recap, weekly proof audio); the variety system (rotation over 10, ban list, cosine similarity against the last 20 at 0.85 until tuned); ideas with the 6-hour cutoff; "why this episode"; fallback episode and the failed-runs page; series bible writes, arcs and the side-character cap; rehearsal format.

**Out of scope.** The scout (news per interest), the streaming writer, name verification loop, character creation and the six chassis, the finale rules in code (P1), the observer.

**Success measure.** 20 test episodes for synthetic learners produced end to end in phase 2 with cost per episode measured; before launch, five nights of episodes for the synthetic learners and the rehearsal accounts at their drop times with zero missed drops; the editor catches at least 90% of the planted faults in the labelled set.

**Dependencies.** E02 vendors and language package; E03 briefs; E14 tracing. The bibles are drafted in `content/bibles/`, read by Muath and checked by an AI review pass (ADR-25.7).

## E05 · The live call

**Goal.** A 5 to 7 minute argument with a host who answers within about a second, waits while the learner searches for a word, echoes the right form and carries on, and never tells the learner they were wrong.

**Scope.** `call-worker` on LiveKit Agents (VAD, multilingual turn detector, streaming STT, Sonnet-class host with cached brief, call TTS in the episode voice); a minimal worker in phase 2 carrying the 50 calls and the onboarding calls; the governor with per-call budgets (at most 1 recast per turn, 3 clarification requests, 1 nudge, 2 to 4 recall gaps, 1 retell, 1 task remark); hold-to-talk; the word button (say it in your own language, the host gives it back); adaptive patience from the pause profile; backchannels; silence offers; anxiety mode; timers, natural close at 6:30 and end by 8:00; per-turn audio upload and verbatim re-transcription; voice-note fallback; captions; crisis step-out with the fail-safe; pronunciation on "say it once"; Salma as the onboarding voice; round two (P1); dial-in experiment (P1).

**Out of scope.** The observer, realtime speech-to-speech models, the two-track Salma audio mix, word-level captions, the understudy-voice mid-call switch, cloned learner voice.

**Success measure.** On the 50 scripted calls: host reply median under 1.5 s and p95 under 2.5 s, connect under 3 s, zero governor violations in the replay of synthetic transcripts; learner speech 4+ minutes per call in the launch rehearsal.

**Dependencies.** E02 vendor choices; E03 host brief; E09 verbatim adapter; E04 call brief. Order A (ADR-24.2) fixes the onboarding call kinds. A Haiku-class host is pre-approved behind `eval-gate` if the comparison shows no difference (ADR-24.7).

## E06 · Onboarding: the first ten minutes

**Goal.** Sound in under 60 seconds, the learner's first spoken sentence in the new language inside 5 minutes, and an account only after they have heard themselves.

**Scope.** The plain landing page and open signup (ADR-25.5); the 90-second sample episode as a second route (P1, v1.1; one per device per 24 hours, $0.05 ceiling, Turnstile); A1 age checkbox and one tap; A2 with the notice line; A3 Salma intake, talk or type, at most 8 turns, fact cards the learner can fix or delete, two lines in the target language; A4 optional 60-second word check (48 items, stops at 75 s, Skip as big as Start); A5 casting (hello clips, voice swap, accent, name respelling check); A6 the first episode playable within 45 s of intake; A7 first call 60 to 90 s with no recasts or nudges; A8 one specific thing managed; A9 account by email code, drop time in life terms, voice-storage consent, the 7-day trial on 2 a day; A10 install card and feed handoff; week-one questions; the launch rehearsal on production.

**Out of scope.** Sign-in with Apple or Google (ADR-25.4); invites and a waitlist; a free tier; a card at trial start.

**Success measure.** In the launch rehearsal on real phones: first sound under 60 s, the first episode plays under 45 s after intake, first spoken sentence under 5 minutes.

**Dependencies.** E05 minimal worker for A3 and A7; E04 first-episode and sample kinds; E03 onboarding writes; E13 consent texts and age gate; E12 trial ledger. The sequence is order A (ADR-24.2).

## E07 · The daily loop in the web app

**Goal.** An installable web app with three tabs (Today, Show, Notebook) and four doors (Listen, Read, Call, Chat) that works in the learner's own language, including right-to-left, on iOS and Android browsers.

**Scope.** Next.js PWA with logical-property lint and the bidi component; design tokens and typography; email-code auth and sessions; the law lint rule (no counter, streak, chart or percent component exists); Today in every state (dropped, played, skipped, return, trial ended, small door); the player (timings sync, replay line, Huh? at 0.85x with meanings, speeds 0.75 / 0.85 / 1.0, transcript folded on first play, tap any word to hear and keep, Media Session, cache-first playback); the word sheet under 300 ms; the article with read-along audio; the chat thread with 3 to 5 host messages ending in three ideas and "tell Salma an idea"; one swap a day; the small door (90 s recap, one voice note up to 60 s); sessions and doors; the event queue to `POST /v1/events`; the Show shelf (P1, v1.1; the feed and Today are the archive at launch); shadowing (P1); accessibility and bundle budget.

**Out of scope.** Native apps (ADR-25.4), autoplay, a next-episode button, a feed of episodes, settings beyond the controls sheet, margin notes and correction notes (dropped by decision 3).

**Success measure.** Lighthouse performance above 85 on a mid-range Android; dropped episode starts under 2 s; the device checklist (iOS 17 and 18, Android 13 and 14 Chrome) passes for background play, push and install.

**Dependencies.** E01 api; E04 published episodes and timings; E03 event ingestion. Web only, with the private feed (ADR-25.4).

## E08 · Private feed, drop and the one cue

**Goal.** The episode reaches the learner once, at the time and place they chose, in the app and in their own podcast app, and nothing else is ever sent.

**Scope.** A private RSS feed per learner with tokens, enclosure streaming and `feed_fetches`; feed links in Apple Podcasts, Pocket Casts and one Android app; drop scheduling per learner (local time, life terms), batch fallback to on-demand at drop minus 90 minutes; the day's `day/next` rule (nothing made after an inactive day, no backlog); web push for the drop only; the 5-second feed tag from the host and the notes' call and article links (FR-233); the one opt-in gap note, sent once after 7, 10 or 14 days; the return episode after 5+ days; rhythm in words only ("4 days, 2 spare"); re-anchoring prompt when the anchor is missed for two weeks.

**Out of scope.** Any other outbound message, re-engagement jobs, streak or calendar views, email digests.

**Success measure.** Exactly three outbound message kinds exist in code (the drop notification, the gap note, transactional email; FR-240) and a test fails if a fourth is added; dropped episode plays from the feed on all three podcast apps; 95% of drops ready before drop time in the launch rehearsal.

**Dependencies.** E04 batch production; E07 player and push subscription; E01 media route.

## E09 · After-session assessment

**Goal.** Within 10 minutes of a session, every call is re-transcribed verbatim, the learner's errors are classified against the structure inventory, the learner model is updated, and nothing runs in the live path.

**Scope.** Verbatim re-transcription per turn with disfluencies and a confidence threshold from the package; `edit_classifier` (minimal edits classified by rules into the structure inventory, errant plus spaCy); error versus slip (3 observations across 2 sessions); fluency measures from word timings; words used and understood; the analyst (fixed schema, checked by code); the memory keeper (facts with quote, ladder, shelf life); the updater (word bank, structure map, error profile, skills with ranges); `session/after-pass` stages end to end; word-check scoring; the calibration set built after launch from opted-in data and `calibration/run` in CI (ADR-25.6); the recording rater with code metrics; session summaries for the teacher; wrong-memory fix path.

**Out of scope.** Salma's notes after the call, the margin note and the polish card (dropped by decision 3); the observer; any score shown to the learner; assessment in the live path; metric claims before calibration.

**Success measure.** After-pass completes under 10 minutes p99; classifier precision at least 0.8 on the planted errors of the synthetic set; false-fact rate under 1 in 100 on replayed synthetic intakes.

**Dependencies.** E02 verbatim vendor; E03 model and writes; E05 per-turn audio; E15 fixtures.

## E10 · Notebook, controls and Salma on demand

**Goal.** Nothing is hidden: the learner can open what the teacher knows and is working on, veto or add to it, fix a wrong memory, and change the few settings that exist.

**Scope.** Notebook sections: working on (at most 3, veto and add, re-targets the same day), words you own (each in the learner's own sentence with audio), about you (each fact with its source quote and date, edit and delete, the sensitive-fact card), why this episode (2 to 4 reasons), hours heard and minutes spoken as plain counts, out in the world log, the tape (P1 comparison); the controls sheet (drop time, notification, captions, transcript, speed, feed link, voice storage, data use opt-in, plan, export, delete, cancel); Salma explains when asked ("why do we say it like that?") in chat; life updates to Salma; wrong-memory flag event and immediate fix.

**Out of scope.** Charts, percentages, levels, streak views, a settings maze, a mistakes list.

**Success measure.** A veto changes the next day's plan (synchronous re-target); a fact edit never reaches a host's mouth again; the law lint rule rejects any monotonic counter that can decrease.

**Dependencies.** E03 edits API; E07 shell; E09 words and facts.

## E11 · Weekly proof, claim gate, recordings and seasons

**Goal.** Every week the learner hears one piece of evidence that passed a code gate, every four weeks they hear themselves then and now, and a season ends with a finale and the next goal.

**Scope.** The claim gate (like for like, beyond about twice the standard error, at least two points, from clean evidence, openable); claims table and `mark_claim_shown`; the proof producer (about 2 minutes, slow week about 45 s, flat week says so and names the change); proof screen with "how we know" and the worth-it question; the then-and-now recording screen (about 3 minutes: retell, opinion, 8 repeat sentences), the baseline in the learner's first week (ADR-24.B21); test-retest pairs and metric unlock at 12 pairs; seasons (4 weeks, one goal in the learner's words), arcs (1 to 3 weeks, at most 2 open, advance only on sessions), mid-season rehearsal, the finale with at most two measured differences (P1); the monthly false-claim audit by Muath.

**Out of scope.** Scores on screen, comparisons with other learners, "where do I stand" for uncalibrated skills, cloned voice playback.

**Success measure.** Zero progress sentences anywhere that do not resolve to a claims row (grep-level test in CI); a weekly proof for a synthetic learner's first week built only from events before launch; false-claim rate under 5% in the first monthly audit after launch.

**Dependencies.** E09 measures and calibration; E04 voice studio; E07 screens; E03 claims storage.

## E12 · Plans, trial and payments

**Goal.** Three monthly plans that differ only in new episodes a day, a 7-day trial on 2 a day with no card, and a cancel that takes one tap.

**Scope.** Plan catalogue ($19.99 / $29.99 recommended / $44.99 for 1 / 2 / 3 a day); allowance enforced server-side (new episodes per active day, one swap; listening, article, chat and round two unlimited); trial ledger at claim; payments through Paddle as merchant of record (ADR-24.4) with webhook verification and replay protection; hosted checkout with cards, Apple Pay, Google Pay and PayPal; trial-ended and day-7 payment states (archive, notebook, export and delete stay for 90 days); the tutor comparison and "about $1 a day" copy; one-tap cancel and the 14-day refund; plan changes; our own failed-payment grace mechanics (v1.1; Paddle's dunning covers launch); price rises for new signups only (ADR-25.10); `billing/reconcile` (P1); regional prices (later).

**Out of scope.** Yearly plans, a free tier, a founding-member lock (not needed: a price rise applies to new signups only, ADR-25.10), fake countdowns, scarcity, pre-ticked upgrades, guilt copy, intensive plan beyond 3 a day.

**Success measure.** A 3-a-day learner cannot obtain a fourth new episode by any route; a cancelled subscription ends billing with no further message; the price shown equals the price charged in a replayed webhook test.

**Dependencies.** E01 api; E13 consent and age gate; the Paddle account (register A5; the sandbox works before it). Prices are $19.99, $29.99 and $44.99 (ADR-24.5).

## E13 · Privacy, security and compliance

**Goal.** The data is the learner's: per-learner keys, consent with versions, deletion and export on the clock, told-not-inferred enforced in code, and compliance by conservative design with a written self-review instead of a lawyer (ADR-25.3).

**Scope.** `forone.core.keys` with KMS and per-learner data keys, SSE-C for audio, bucket deny rules; audit log; RLS CI test; secrets layout; the processor register, the DPIA from the official template and the self-review checklist (`legal/`); consent texts with versions and the A9 flow; age gate (under 18 refused, pre-account deletion); voice storage off deletes call audio within 15 minutes, revoke deletes all audio within 24 hours; export link within 1 hour; account deletion (access ends at once, no grace, live purge 24 h, backups 30 d); data use opt-in (de-identify and revoke in v1.1); output guard (AI disclosure, no inference of sensitive classes, listener-text sanitizer, injection set, the correction guard); crisis protocol for every learner (SB 243-style duties for all; keyword list with the host's confirmation and the 2-second fail-safe; resources from a maintained international helpline directory; step-out in the call); staff accounts and roles; `privacy/verify`; incident runbook with the lawyer triggers and one tabletop; security testing without a paid test (dependency and secret scans in CI, an OWASP ZAP baseline of staging, an AI security review of changes to auth, keys, media URLs, the feed and deletion; ADR-25.11); Langfuse 30-day retention and vendor training opt-outs recorded.

**Out of scope.** Counsel review of any kind (ADR-25.3; the triggers for when a lawyer becomes necessary are in `legal/README.md`), a paid penetration test (a trigger, not a launch item: 1,000 paying learners, a B2B contract or a security incident, ADR-25.11), staff passkeys, the feed-fetch anomaly rule, a CDN move.

**Success measure.** On staging: delete one test learner and `privacy/verify` passes; revoke voice storage on another and the 24-hour check passes; export a third and every JSON opens; the injection set produces zero disclosures of the brief; every legal text has passed the AI review pass against the checklist and Muath's approval.

**Dependencies.** Muath's self-review and approval of `legal/` (register A4); an EU and UK representative if it applies (A7); E01 infrastructure; E03 purge order; E05 and E07 for the guard and crisis surfaces.

## E14 · Cost tracing and vendor control

**Goal.** Every model, voice and speech call is a priced row from the first test render, so the exit criterion (a measured cost per session and a costed path to $0.35) is a query, not an estimate.

**Scope.** `prices.yaml` and the price book; `vendor_calls` with partitions and RLS; tracing middleware with unit usage and `price_for`; daily spend cap; cost roll-up per session and per role; per-learner daily spend and `costguard`; alarms (kind ceiling, unpriced, low cache hit, session over $1, p50 over $0.80 for 7 days, daily spend); `spend_mode` halt; vendor health and the failover drill (v1.1); the weekly cost report and the exit document; monthly reconcile skeleton; Hume lockfile check; the Haiku-host comparison inside the 50-call run (pre-approved behind `eval-gate`, ADR-24.7).

**Out of scope.** Multi-currency, per-vendor invoice scrapers, a forecasting model, self-hosted Langfuse, conserve mode.

**Success measure.** Measured cost per session on a production week of synthetic learners and the launch rehearsal under $0.66, with the path to $0.35 costed line by line; no unpriced vendor call in production for 7 days.

**Dependencies.** E01 middleware home; E02 vendor choices; E04 and E05 call sites.

## E15 · Evals, observability and operations

**Goal.** One person can run the product safely: logs with no personal data, alerts that reach Muath, runbooks the agent can execute when asked, and an eval gate that stops a prompt change from breaking law 7 (ADR-25.2).

**Scope.** Structured logging with the scrub corpus; Sentry in every service; uptime checks and a heartbeat; alerts to Muath by push and, for a systemic drop failure, by phone; fixtures from synthetic learners, scripted calls and the volunteer clips (ADR-25.6); eval suites (fitter, law scan, claim gate, recognizers, editor, writer, pipeline, memory, host governor replay, injection, analyst) and `eval-gate` in CI on prompt changes; release manifest and `tools/release cut`; feature flags; alert rules for pipeline, client budgets, call, cost, privacy and crisis; measures from launch; review sampling by an AI review pass with what it flags read by Muath; the launch health page (v1.1); the morning checklist the agent runs; the pre-launch freeze; synthetic learners (3 in the build, 50 for the offline suite).

**Out of scope.** An on-call rota, Metabase unless admin tables fall short, the simulated-caller half of the host suite (P1), incidents as a page, sparklines.

**Success measure.** A prompt change to the host that adds "that's wrong" fails CI; a missed drop alerts Muath within 5 minutes; every runbook R1 to R4 and R12 rehearsed by the agent on staging before launch.

**Dependencies.** E01 and the agent workflow; every other epic's events.

## E16 · Launch and the first season

**Goal.** Version 1 opens to everyone when the launch checklist is green, and the first weeks are read honestly against the launch health measures at 4 and 8 weeks.

**Scope.** Opening signup; the morning checklist and weekly digest; v1.1 and P1 items shipped after launch behind flags (round two, finale, dial-in experiment, shadowing, the tape); the first monthly false-claim audit; the first season finales; the per-language close rule; the cost path (batch voices, the negotiated rate); the health reviews at 4 and 8 weeks; a second language through the gate harness.

**Out of scope.** Paid acquisition, referral programs, native apps, invites, cohorts, an external test, languages that did not pass the gate.

**Success measure.** The launch health measures, read 4 and 8 weeks after launch (PRD Part 16): trial to paid 30% or more (stop under 15%); active in week 4 at 40% or more; 4+ sessions a week and 4+ minutes of speech; the 4-week recording improves for most; cost under $0.60 (stop over $1.00 with no plan).

**Dependencies.** Every v1 story in E01 to E15 passing, and the launch checklist green (`00-release-plan.md`).
