# For one: the epics

*Implementation backlog, written 2026-11-06. Visual version: https://claude.ai/artifact/NFcJZpKpupvoVyH59Mhwjc.  for the beta build (18 November to 22 December 2026) and the paid founding beta (23 December 2026 to 26 January 2027). Built from the agreed feature map (features/for-one-features.html), concept-v2.md, decisions.md and the nine architecture documents. Where an architecture document still carries a stale decision (a Saudi launch, Arabic as the only first language, Salma's correction notes after the call, build weeks dated 2 November to 6 December), this backlog follows the 23 October decisions: no target country, languages by the language gate, English-only pilot, invisible teaching through recasts, evidence instead of tests, 4-week seasons, and the re-dated build.*

**Sixteen epics.** E01 to E05 are the engine (infrastructure, vendors, the learner model, the pipeline, the call). E06 to E11 are what the learner meets (onboarding, the daily loop, the feed, assessment, the notebook, the proof). E12 to E15 are the business and the operations wrapper (plans, privacy, cost, evals and operations). E16 is the beta itself.

Each epic names its goal, its scope, what is out of scope, the measure that says it worked, and what it depends on. Stories live in `02-stories/<slug>.md`; the release order is in `00-release-plan.md`.

| Id | Epic | Architecture domain | Stories | Beta week it must land |
|---|---|---|---|---|
| E01 | Platform foundation | 01 topology, 09 operations | 9 | W1 to W2 |
| E02 | Vendor tests and the language gate | 02, 03, 08 | 9 | W1 to W2 |
| E03 | Learner model and event log | 04 learner model | 11 | W1 to W5 |
| E04 | Episode generation pipeline | 02 generation | 13 | W2 to W5 |
| E05 | The live call | 03 live call | 13 | W2 to W5, round two P1 |
| E06 | Onboarding: the first ten minutes | 06 client, 03, 07 | 11 | W3 |
| E07 | The daily loop in the web app | 06 client | 12 | W3 to W5 |
| E08 | Private feed, drop and the one cue | 06 client, 01 | 7 | W3 to W4 |
| E09 | After-session assessment | 05 assessment | 10 | W2 to W5 |
| E10 | Notebook, controls and Salma on demand | 06 client, 04 | 9 | W5 |
| E11 | Weekly proof, claim gate, recordings and seasons | 05, 02 | 10 | W5, finale P1 |
| E12 | Plans, trial and payments | 07 security, 01 | 9 | W3 to W5 |
| E13 | Privacy, security and compliance | 07 security | 12 | W1 to W5 |
| E14 | Cost tracing and vendor control | 08 cost | 8 | W1 to W5 |
| E15 | Evals, observability and operations | 09 operations | 11 | W1 to W5 |
| E16 | Founding beta and season one | all | 10 | Dec 23 to Jan 26 |

---

## E01 · Platform foundation

**Goal.** One repository, one staging and one production environment, and the shared services every other epic calls, stood up in the first two weeks so nothing later waits on infrastructure.

**Scope.** Monorepo with CI; `forone.core` (settings, database, migrations, the `events` contract); FastAPI `api` skeleton; Inngest with a hello function; Terraform for staging reused for production (VPC, RDS Postgres 16 with pgvector, S3 with KMS, ECR, ECS Fargate, ALB with WAF, Secrets Manager); Sentry and Langfuse wiring; staging deploy pipeline; the outbox and relay; messaging and rate limits; production stood up Multi-AZ in week 5 with a restore drill.

**Out of scope.** Multi-region, self-hosted LiveKit, Inngest or Langfuse, CloudFront for media, an API gateway, a message bus, native apps, a separate admin app.

**Success measure.** A commit on `main` deploys to staging without a hand; an episode produced on staging is readable from the web shell by 1 December; production restored from backup in a drill before 22 December.

**Dependencies.** The legal view on the home region (AWS me-central-1 versus an EU region) is needed before Terraform is applied to production; staging can start in the EU region and move. Nothing else blocks it.

## E02 · Vendor tests and the language gate

**Goal.** Choose every voice and speech vendor on measured results from pilot data, freeze the choices by 27 November, and make the language gate a repeatable test so a second language can open without a redesign.

**Scope.** The 30-clip recognizer test (streaming and verbatim vendors) on consented Milestone 0 clips; the blind two-host voice test across Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4 with 10 raters; the 50 scripted calls for latency; `vendors.yaml` and the thin adapters for the winners only; the English language package (lexicon, lemmatizer, structure inventory from the English Grammar Profile, ban list, bibles, Salma strings); the language gate harness with the five checks as runnable jobs; a candidate second language run through the harness during the beta.

**Out of scope.** Shipping any language other than English in the beta unless it passes all five checks; a self-hosted aligner; Hume (its voice APIs close 13 November).

**Success measure.** By 27 November, one table per vendor decision with the numbers; the verbatim vendor keeps learner errors on at least 90% of tagged clips; the host answers in under 1.5 s median on the 50 calls.

**Dependencies.** Consent addendum from Milestone 0 learners naming the vendors before any clip leaves (E13); cost tracing middleware so every test render is a priced row (E14).

## E03 · Learner model and event log

**Goal.** One append-only event log and one learner model (words, structures, errors, skills, life facts with quotes, show canon) that every role reads through a compiled brief and only after-session roles write.

**Scope.** `events` with partitions, RLS and idempotent append; the type registry; word bank with FSRS-style scheduling per word, structure and corrected form; structure map and observations; life facts with exact quote, confidence, sensitivity and expiry, the confirmation ladder and `verify_quote`; interests with decay; goals; show canon, side characters and the series bible excerpt; `briefs.compile` for teacher, writer, host, Salma, chat and proof; onboarding writes (intake cards, word check scoring, consents); after-pass apply; learner edits (veto, add, fix a fact); export content; delete purge order; rebuild from the log.

**Out of scope.** A separate analytics warehouse, CDC streams, cross-region replication, automated FSRS weight fitting in the beta, per-learner physical partitions.

**Success measure.** A replay of one pilot learner's 14 days produces a word bank and error list that agree with Muath's hand-kept file on 80% of items; every confirmed life fact passes the quote check against the transcript; no live role holds a write credential.

**Dependencies.** E01 database; the structure inventory from E02; the analyst output schema from E09.

## E04 · Episode generation pipeline

**Goal.** A new episode for each learner before their drop time, every day, at about 95% known words, that passes an editor from a second vendor and costs a measured amount.

**Scope.** `episode/produce`: teacher (plan with one grammar target, 2 to 4 words, the right forms of the learner's own mistakes, three ideas for tomorrow), writer (script, article, call brief with planned host moves, chat opener), fitter (coverage in code, up to 2 rewrites), editor (correctness, no uncertain memory, the fun carries the language, nothing reads as a lesson or a correction, variety, laws, "would they pick this over a real podcast?"), voice studio (two voices, timings, names, re-listen), senses and glosses, publish; batch mode with the on-demand fallback 90 minutes before drop; on-demand kinds (pilot, sample, swap, return, small-door recap, weekly proof audio); the variety system (rotation over 10, ban list, cosine similarity against the last 20); ideas with the 6-hour cutoff; "why this episode"; fallback episode and the human page; series bible writes, arcs and the side-character cap; rehearsal format.

**Out of scope.** The scout (news per interest), the streaming writer, name verification loop, character creation and the six chassis, the finale rules in code (P1), the observer.

**Success measure.** 20 test episodes from pilot learner files by 1 December with cost per episode measured; by 22 December five nights of episodes for the 15 pilot learners at their real drop times with zero missed drops; editor agreement with Muath's reads above 80%.

**Dependencies.** E02 vendors and language package; E03 briefs; E14 tracing. The host and Salma bibles need a named writer (open decision).

## E05 · The live call

**Goal.** A 5 to 7 minute argument with a host who answers within about a second, waits while the learner searches for a word, echoes the right form and carries on, and never tells the learner they were wrong.

**Scope.** `call-worker` on LiveKit Agents (VAD, multilingual turn detector, streaming STT, Sonnet-class host with cached brief, call TTS in the episode voice); minimal worker by week 2 carrying the 50 calls and the onboarding calls; the governor with per-call budgets (at most 1 recast per turn, 3 clarification requests, 1 nudge, 2 to 4 recall gaps, 1 retell, 1 task remark); hold-to-talk; the word button (say it in your own language, get it back); adaptive patience from the pause profile; backchannels; silence offers; anxiety mode; timers, natural close at 6:30 and end by 8:00; per-turn audio upload and verbatim re-transcription; voice-note fallback; captions; crisis step-out; pronunciation on "say it once"; Salma as the onboarding voice; round two (P1); dial-in experiment (P1).

**Out of scope.** The observer, realtime speech-to-speech models, the two-track Salma audio mix, word-level captions, the understudy-voice mid-call switch, cloned learner voice.

**Success measure.** On the 50 scripted calls: host reply median under 1.5 s and p95 under 2.5 s, connect under 3 s, zero governor violations in the replay of pilot transcripts; learner speech 4+ minutes per call on the pilot learners' real calls in week 5.

**Dependencies.** E02 vendor choices; E03 host brief; E09 verbatim adapter; E04 call brief. The first-session order decision shapes the onboarding call kinds.

## E06 · Onboarding: the first ten minutes

**Goal.** Sound in under 60 seconds, the learner's first spoken sentence in the new language inside 5 minutes, and an account only after they have heard themselves.

**Scope.** The 90-second sample episode and landing page (one per device per 24 hours, $0.05 ceiling, Turnstile); A1 age checkbox and one tap; A3 Salma intake, talk or type, at most 8 turns, fact cards the learner can fix or delete, two lines in the target language; A4 optional 60-second word check (48 items, stops at 75 s, Skip as big as Start); A5 casting (hello clips, voice swap, accent, name respelling check); A6 pilot episode playable within 45 s of intake; A7 first call 60 to 90 s with no recasts or nudges; A8 one specific thing managed; A9 account by email code, drop time in life terms, voice-storage consent, the 7-day trial on 2 a day; A10 install card and feed handoff; invites and waitlist; re-onboarding of the 15 pilot learners under the beta consent.

**Out of scope.** Sign in with Apple and Google if the developer accounts are not approved (P1); a free tier; card at trial start.

**Success measure.** On staging with real phones: first sound under 60 s, pilot plays under 45 s after intake, first spoken sentence under 5 minutes, measured on the pilot learners' re-onboarding.

**Dependencies.** E05 minimal worker for A3 and A7; E04 pilot and sample kinds; E03 onboarding writes; E13 consent texts and age gate; E12 trial ledger. Blocked on the first-session order decision for the exact A4 to A7 sequence.

## E07 · The daily loop in the web app

**Goal.** An installable web app with three tabs (Today, Show, Notebook) and four doors (Listen, Read, Call, Chat) that works in the learner's own language, including right-to-left, on iOS and Android.

**Scope.** Next.js PWA with logical-property lint and the bidi component; design tokens and typography; email-code auth and sessions; the law lint rule (no counter, streak, chart or percent component exists); Today in every state (dropped, played, skipped, return, trial ended, small door); the player (timings sync, replay line, Huh? at 0.85x with meanings, speeds 0.75 / 0.85 / 1.0, transcript folded on first play, tap any word to hear and keep, Media Session, cache-first playback); the word sheet under 300 ms; the article with read-along audio; the chat thread with 3 to 5 host messages ending in three ideas and "tell Salma an idea"; one swap a day; the small door (90 s recap, one voice note up to 60 s); the event queue to `POST /v1/events`; the Show shelf; shadowing (P1); accessibility and bundle budget.

**Out of scope.** Native apps, autoplay, a next-episode button, a feed of episodes, settings beyond the controls sheet, margin notes and correction notes (dropped by decision 3).

**Success measure.** Lighthouse performance above 85 on a mid-range Android; dropped episode starts under 2 s; the week-3 device matrix (iOS 17 and 18, Android 13 and 14 Chrome) passes for background play, push and install.

**Dependencies.** E01 api; E04 published episodes and timings; E03 event ingestion. Blocked on the web-versus-native decision (recommended: web plus feed; a native choice replaces this epic's shell with a one-codebase app and moves the beta).

## E08 · Private feed, drop and the one cue

**Goal.** The episode reaches the learner once, at the time and place they chose, in the app and in their own podcast app, and nothing else is ever sent.

**Scope.** A private RSS feed per learner with tokens, enclosure streaming and `feed_fetches`; feed links in Apple Podcasts, Pocket Casts and one Android app; drop scheduling per learner (local time, life terms), batch fallback to on-demand at drop minus 90 minutes; the day's `day/next` rule (nothing made after an inactive day, no backlog); web push for the drop only; the Salma 5-second feed tag in the learner's own language; the one opt-in gap note written at signup, sent once after 7, 10 or 14 days; the return episode after 5+ days; rhythm in words only ("4 days, 2 spare"); re-anchoring prompt when the anchor is missed for two weeks.

**Out of scope.** Any other outbound message, re-engagement jobs, streak or calendar views, email digests.

**Success measure.** Exactly three outbound message kinds exist in code (drop, gap note, weekly proof) and a test fails if a fourth is added; dropped episode plays from the feed on all three podcast apps; 95% of drops ready before drop time in the week-5 run.

**Dependencies.** E04 batch production; E07 player and push subscription; E01 media route.

## E09 · After-session assessment

**Goal.** Within 10 minutes of a session, every call is re-transcribed verbatim, the learner's errors are classified against the structure inventory, the learner model is updated, and nothing runs in the live path.

**Scope.** Verbatim re-transcription per turn with disfluencies and a confidence threshold from the package; `edit_classifier` (minimal edits classified by rules into the structure inventory, errant plus spaCy); error versus slip (3 observations across 2 sessions); fluency measures from word timings; words used and understood; the analyst (fixed schema, checked by code); the memory keeper (facts with quote, ladder, shelf life); the updater (word bank, structure map, error profile, skills with ranges); `session/after-pass` stages end to end; word-check scoring; calibration samples from Muath's pilot tags and `calibration/run` in CI; the recording rater with code metrics; session summaries for the teacher; wrong-memory fix path.

**Out of scope.** Salma's notes after the call, the margin note and the polish card (dropped by decision 3); the observer; any score shown to the learner; assessment in the live path.

**Success measure.** After-pass completes under 10 minutes p99; classifier precision at least 0.8 on the claim-feeding tags of the pilot set; false-fact rate under 1 in 100 on replayed pilot intakes.

**Dependencies.** E02 verbatim vendor; E03 model and writes; E05 per-turn audio.

## E10 · Notebook, controls and Salma on demand

**Goal.** Nothing is hidden: the learner can open what the teacher knows and is working on, veto or add to it, fix a wrong memory, and change the few settings that exist.

**Scope.** Notebook sections: working on (at most 3, veto and add, re-targets the same day), words you own (each in the learner's own sentence with audio), about you (each fact with its source quote and date, edit and delete), why this episode (2 to 4 reasons), hours heard and minutes spoken as plain counts, out in the world log, the tape (P1 comparison); the controls sheet (drop time, notification, captions, transcript, speed, feed link, voice storage, research opt-in, export, delete, cancel); Salma explains when asked ("why do we say it like that?") in chat; life updates to Salma; wrong-memory flag event and immediate fix.

**Out of scope.** Charts, percentages, levels, streak views, a settings maze, a mistakes list.

**Success measure.** A veto changes the next day's plan (synchronous re-target) in the week-5 run; a fact edit never reaches a host's mouth again; the law lint rule rejects any monotonic counter that can decrease.

**Dependencies.** E03 edits API; E07 shell; E09 words and facts.

## E11 · Weekly proof, claim gate, recordings and seasons

**Goal.** Every week the learner hears one piece of evidence that passed a code gate, every four weeks they hear themselves then and now, and a season ends with a finale and the next goal.

**Scope.** The claim gate (like for like, beyond about twice the standard error, at least two points, from clean evidence, openable); claims table and `mark_claim_shown`; the proof producer (about 2 minutes, slow week about 45 s, flat week says so and names the change); proof screen with "how we know" and the worth-it question; the then-and-now recording screen (about 3 minutes: retell, opinion, 8 repeat sentences), the first "then" after session 2; test-retest pairs and metric unlock at 12 pairs; seasons (4 weeks, one goal in the learner's words), arcs (1 to 3 weeks, at most 2 open, advance only on sessions), mid-season rehearsal, the finale with at most two measured differences (P1); false-claim audit.

**Out of scope.** Scores on screen, comparisons with other learners, "where do I stand" for uncalibrated skills, cloned voice playback.

**Success measure.** Zero progress sentences anywhere that do not resolve to a claims row (grep-level test in CI); a weekly proof for each returning pilot learner built only from events by 22 December; false-claim rate under 5% in the first audit on 1 January.

**Dependencies.** E09 measures and calibration; E04 voice studio; E07 screens; E03 claims storage.

## E12 · Plans, trial and payments

**Goal.** Three monthly plans that differ only in new episodes a day, a 7-day trial on 2 a day with no card, founding members who keep their price, and a cancel that takes one tap.

**Scope.** Plan catalogue ($19.99 / $29.99 recommended / $44.99 for 1 / 2 / 3 a day); allowance enforced server-side (new episodes per active day, one swap; listening, article, chat and round two unlimited); trial ledger at claim; payments against the chosen processor (Stripe test mode scaffold, swapped when the merchant of record is decided) with webhook verification and replay protection; checkout redirect and Apple Pay domain file; trial-ended and day-7 payment states (archive, notebook, export and delete stay for 90 days); founding-member price lock for the first 100; the tutor comparison and "about $1 a day" copy; one-tap cancel; `billing/reconcile` (P1); regional prices (later).

**Out of scope.** Yearly plans, a free tier, fake countdowns, scarcity, pre-ticked upgrades, guilt copy, intensive plan beyond 3 a day.

**Success measure.** A 3-a-day learner cannot obtain a fourth new episode by any route; a cancelled subscription ends billing with no further message; the price shown equals the price charged in a replayed webhook test.

**Dependencies.** E01 api; E13 consent and age gate; the merchant-of-record decision (open, due 1 December); confirmation of the three prices (open).

## E13 · Privacy, security and compliance

**Goal.** The data is the learner's: per-learner keys, consent with versions, deletion and export on the clock, told-not-inferred enforced in code, and counsel's answers loaded before the first paying learner.

**Scope.** `forone.core.keys` with KMS and per-learner data keys, SSE-C for audio, bucket deny rules; audit log; RLS CI test; secrets layout; processor register (`docs/ropa.md`) with DPA status per vendor; counsel requests (region and transfer basis, consent copy, crisis lines, California SB 243, subscription and refund rules); consent texts with versions and the A9 flow; age gate (under 18 refused, pre-account deletion); voice storage off deletes call audio within 15 minutes, revoke deletes all audio within 24 hours; export link within 1 hour; account deletion (access ends at once, live purge 24 h, backups 30 d); research opt-in with anonymization and revoke; output guard (AI disclosure on demand, no inference of sensitive classes, listener-text sanitizer, injection set); crisis protocol (keyword list, quarantine, resources card, step-out in the call); staff accounts and roles; `privacy/verify` and the admin privacy page; incident runbook and one tabletop; Langfuse 30-day retention and vendor training opt-outs recorded.

**Out of scope.** A penetration test before public launch (budget open), staff passkeys, the feed-fetch anomaly rule, a CDN move.

**Success measure.** On staging: delete one pilot learner and `privacy/verify` passes; revoke voice storage on another and the 24-hour check passes; export a third and every JSON opens; the injection set produces zero disclosures of the brief.

**Dependencies.** The legal view on the storage region (blocking, due 24 November); E01 infrastructure; E03 purge order; E05 and E07 for the guard and crisis surfaces.

## E14 · Cost tracing and vendor control

**Goal.** Every model, voice and speech call is a priced row from the first test render, so the exit criterion (a measured cost per session and a costed path to $0.35) is a query, not an estimate.

**Scope.** `prices.yaml` and the price book; `vendor_calls` with partitions and RLS; tracing middleware with unit usage and `price_for`; daily spend cap; cost roll-up per session and per role; per-learner daily spend and `costguard`; alarms (kind ceiling, unpriced, low cache hit, session over $1, p50 over $0.80 for 7 days, daily spend); `spend_mode` with conserve and halt; vendor health and the failover drill (kill the primary voice key for an hour and ship); the weekly cost report and the exit document; monthly reconcile skeleton; Hume lockfile check; the Haiku-host comparison inside the 50-call run.

**Out of scope.** Multi-currency, per-vendor invoice scrapers, a forecasting model, self-hosted Langfuse unless counsel requires it.

**Success measure.** Measured cost per session on the pilot learners' production week under $0.66 with the path to $0.35 costed line by line; no unpriced vendor call in production for 7 days.

**Dependencies.** E01 middleware home; E02 vendor choices; E04 and E05 call sites.

## E15 · Evals, observability and operations

**Goal.** The beta can be run safely by one or two people: logs with no personal data, alerts that page, runbooks for the twelve things that go wrong, and an eval gate that stops a prompt change from breaking law 7.

**Scope.** Structured logging with the scrub corpus; Sentry in every service; uptime checks and a heartbeat; paging with phone escalation; pilot fixtures imported (learner files, scripts with hand coverage, editor reads, transcripts and tags, 30 clips, facts, similarity pairs); eval suites (fitter, law scan, claim gate, recognizers, editor, writer, pipeline, memory, host governor replay, injection, analyst) and `eval-gate` in CI on prompt changes; release manifest and `tools/release cut`; feature flags; alert rules for pipeline, client budgets, call, cost, privacy and crisis; measures and the admin measures page; review sampling (10 random episodes per learner per month) and the review pages; the gates page with readable-from dates; the 08:30 checklist; on-call rota; the freeze from 19 December 12:00; synthetic learners (3 in the build, 50 in the beta).

**Out of scope.** Metabase unless admin tables fall short, the simulated-caller half of the host suite (P1), incidents as a page, sparklines.

**Success measure.** A prompt change to the host that adds "that's wrong" fails CI; a missed drop pages within 5 minutes; every runbook R1 to R4 and R12 rehearsed once before 22 December.

**Dependencies.** E01; fixtures from the Milestone 0 kit; every other epic's events.

## E16 · Founding beta and season one

**Goal.** About 50 learners a week into 7-day trials from 23 December, in English, with the gates read honestly on 26 January and a decision taken on the day.

**Scope.** Waitlist loaded from Milestone 0 sign-ups; invite batches of about 50 a week; the 15 pilot learners re-onboarded in week 5 under the beta consent; an external test (20 to 30 learners at week 0 and week 8); the gate dashboard (trial to paid, week-4 active, sessions a week, speech minutes, recording change, renewal, worth it, cost, false claims, wrong memories, per-language quality); the first season finales from 20 January; the first false-claim audit on 1 January; P1 items shipped during the beta (round two, finale, Apple and Google sign-in, dial-in experiment, shadowing, the tape); the gate review on 26 January; a second language through the gate harness as a dry run.

**Out of scope.** Paid acquisition, referral programs, native apps, public launch, languages that did not pass the gate.

**Success measure.** Trial to paid 30% or more (stop under 15%); active in week 4 at 40% or more; 4+ sessions a week and 4+ minutes of speech; the 4-week recording improves for most; cost under $0.60 (stop over $1.00 with no plan).

**Dependencies.** Everything P0 in E01 to E15 landed by 22 December; the gate decision on 18 November passed.
