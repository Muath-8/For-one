# For one — Implementation PRD

**Version 3.1, 2026-10-23 (3.0 was 2026-10-10). Built on concept v2 ([concept-v2.md](concept-v2.md)) and the decision list ([decisions.md](decisions.md)). It replaces PRD 2.0 ([PRD.md](PRD.md), kept unchanged so the two can be compared). Like 2.0, every section states what happens, in what order, with what limits, and what happens on failure.**

**Tags.** Untagged rules come from concept v2, decisions.md or the eleven lens documents in [perspectives/](perspectives/). **[NEW]** marks a decision this document makes that none of those made; veto it or it stands. **[P0]** must work on the first day of the paid founding beta (2026-12-23). **[P1]** must work before the beta's gate review (2027-01-26). **[LATER]** is specified for direction and not built in the beta. **OPEN** is genuinely undecided; Part 18 lists every one. A feature in Parts 2 to 14 with no priority tag is [P0].

**Status of the ten decisions.** On 2026-10-10 Muath answered "continue" to concept v2. This PRD treats the recommended answer to all ten decisions in decisions.md, and the six settled points, as adopted. If he changes one, the parts named in Part 0.3 change with it. On 2026-10-23 he changed four of them; Part 0.0 lists what that changed here.

---

# PART 0 — READ FIRST

## 0.0 What changed in 3.1 (2026-10-23)

Muath answered the open decisions on 2026-10-23, and the Milestone 0 pilot moved. This version folds both in.

| # | Was (3.0) | Now (3.1) | Parts changed |
|---|---|---|---|
| 1 | One launch learner: Saudi Arabic-speaking adults, 22 to 35, about B1 | **No launch country or people.** Any adult who understands some of the target language, from about A2 to C1. The show fits the learner, not a market. | 1.4, 2.1, 2.2, 13, 19.4 |
| 2 | One language pair, Arabic to English | **As many languages as the speech stack supports**, by a fixed rule: a target language ships when it passes the language gate (voices, learner-speech recognition, writing, call speed, a structure inventory; Part 13). The learner's own language needs interface text, glosses, Salma's voice and recognition for the word button. | 1.4, 5.7, 7.1, 10.13, 10.14, 12.1, 13, 14.3, 14.4 |
| 3 | SAR 89 a month, SAR 449 a year, founding SAR 349; one new episode a day | **Monthly only, three plans that differ only in new episodes a day: 1 a day $19.99, 2 a day $29.99 (recommended), 3 a day $44.99**, priced so no plan loses money on full use at the $0.35 planning cost. The trial starts on 2 a day; the first 100 paying learners keep their price. No yearly plan. | 1.4, 2.2, 3.6, 14.5, 16.1 |
| 4 | Conversational correction in the moment, explicit notes from the producer afterwards | **Correction is invisible.** Hosts ask for clarification and say the learner's sentence back the natural way ("you mean..."). Nobody says "wrong" or shows a right answer: no notes after the call, no margin note, no nudge. Errors come back as language the hosts use in the next episodes. | Law 7, 5.4, 5.5, 5.6, 6.3, 9.3, 10.12 |
| 4b | Salma, the producer in the learner's own language: onboarding, talkback, notes, the weekly proof | **Salma stays, but never corrects.** Muath picked "a producer" in the UI and UX thread on 2026-10-23 and concept v2 keeps her as the face of the app: onboarding, life updates, "tell Salma an idea", the notebook, the weekly proof's voice, explanations only when asked. No notes after calls, no polish card, no margin notes. A word mid-call comes from the host, through the word button. | 5.4.5, 5.5, 7.3, 10.12, 14.1 |
| 5 | Trial without a card (open) | Agreed by Muath. | 0.1 row 8 |
| 6 | Pilot Oct 12 to Nov 1, beta build Nov 2 to Dec 6, beta Dec 7 to Jan 10 | **Pilot Oct 24 to Nov 18** (recruiting from Oct 24, episodes from Nov 1, gate Nov 18), **beta build Nov 18 to Dec 22**, **paid beta Dec 23 to Jan 26**, following the pilot kit's schedule (milestone-0/03-schedule.md). | 18, 19 and every date |

**The risk in item 4, stated once.** Recasts alone are the least-noticed kind of feedback; in immersion classrooms they left fluent speakers with the same errors for years. This spec keeps correction invisible and works against that risk in three ways: recasts are salient (one change, stressed, said back as "you mean..."), the learner's errors become the next episodes' language (input flood and calls that make the form necessary, Part 9.3), and the 4-weekly recording measures accuracy. If accuracy is flat for most learners after a season, the beta gate shows it (Part 16.1), and the fix is decided then.

## 0.1 Where this PRD departs from concept v2, or fills a gap it left

| # | Concept v2 says | This PRD says | Why |
|---|---|---|---|
| 1 | A mid-season "real-life rehearsal of the actual scene" (section 6), and real-life rehearsal as a paid add-on after launch (sections 8 and 9) | In the beta, the mid-season rehearsal is one ordinary episode in the "rehearsal" format, whose call is the scene itself. Rehearsal on demand, at any time, stays the later add-on. | Both statements hold, and no new agent is needed. |
| 2 | The episode "drops once, at the time and place they chose", every day | A new episode is made only after a day on which the learner used the show. Otherwise the unplayed episode stays as today's, and no drop notification fires. [NEW] | Caps generation at the plan's number per active day, and a skipped day leaves no pile of unplayed episodes and no reminder. |
| 3 | "Where do I stand?" is answered honestly with a range when asked (decision 4f) | A host gives a range for a skill only after the calibration bar for that skill is met (Part 10.8). Before that the host says plainly that the show cannot say reliably yet, and the notebook shows the evidence it has. [NEW] | An uncalibrated level range would break law 12, "no claim without proof". |
| 4 | When the learner says a word in their own language, the host gives it back in the target language (section 6); decision 3 also says "hints before answers" | The host gives the word at once if the learner has never produced it. If they have produced it before, the host gives a hint first and the word on a second ask. [NEW] | Reconciles the two: retrieval only where there is something to retrieve. |
| 5 | The opt-in note to the learner's future self is written at signup | It is offered once in week 1 (end of session 3, or in the first weekly proof), not during onboarding. [NEW] | Keeps the first ten minutes at ten minutes. |
| 6 | Then-and-now recording every 4 weeks, as the season finale | The first "then" is recorded in week 1 (offered after session 2), not during onboarding. [NEW] | A like-for-like comparison needs a baseline of the same task, and onboarding is already full. |
| 7 | When the learner says a word in their own language mid-call, the host gives it back (section 6) | Beta uses a word button: the learner holds it and says the word in their own language. Detecting the switch without a button waits for the native app. [NEW] | Detecting a switch between the learner's language and the target in streaming recognition is unproven for most pairs; the button routes that audio to a recognizer for the learner's language cleanly. |
| 8 | A 7-day trial, no free tier | No card is needed to start the trial; payment is asked for once, plainly, on day 7. [Agreed by Muath, 2026-10-23] | Invites go to hand-picked cohorts, so the trial-to-paid number should measure the product, not card friction. |

Everything else in this document follows concept v2. Where a lens recommended something concept v2 did not adopt (for example the observer in the call, ask-first glosses, an intelligibility error category), it is marked [LATER] or left out, not quietly added.

## 0.2 What only Muath can settle

These block the beta, not Milestone 0. Each is also in Part 18.

1. **Who writes the hosts and Salma.** They are authored by a person, not generated (law 6, variety system). With many languages this is one host duo per target language and one Salma per native language (Part 7). The beta needs finished bibles for every language it opens; Milestone 0 runs on drafts. Muath, or writers he hires.
2. **The company and the payment provider.** Selling worldwide means tax and currency in every country. This PRD recommends a **merchant of record** (a provider that is the legal seller, collects VAT and sales tax in each country and pays out), so a small company can sell everywhere from day one. Which one depends on where the company is registered and which local payment methods it supports. [NEW: merchant of record]
3. **Legal review before 2026-12-23,** scoped by where the beta takes learners from: the EU and UK GDPR, Saudi PDPL and other national privacy laws for voice recordings and hosting region; California SB 243 (AI disclosure, self-harm protocol); the EU AI Act's disclosure duties; consumer subscription rules. The fewer countries the beta opens to, the smaller this job. These are flags, not legal advice.
4. **The three prices.** $19.99, $29.99 and $44.99 come from concept v2's cost rule (Part 14.5). Confirm them, or change the rule they are built on.

Settled on 2026-10-23: the trial needs no card; there is no launch group, so there is no recruitment fallback.

## 0.3 What changed from PRD 2.0

| PRD 2.0 part | Status in 3.0 | Driven by |
|---|---|---|
| 1.2 Six hard laws | Replaced by the twelve laws and the extended trust contract (Parts 1.2, 1.3) | Concept v2 section 5; decisions 3, 4, 5 |
| 1.3 Platform and scope | Web app plus private podcast feed; every language that passes the gate; 1, 2 or 3 new episodes per active day by plan replace the 2-session cap; three monthly prices; one drop notification, one gap note | Decisions 1, 2, 6, 7, 10 |
| 2 Onboarding | Sound within a minute; 3-minute talk with Salma and visible fact cards; optional word check; pilot and first call before the account | Settled point "the first ten minutes" |
| 3 Daily loop | Tomorrow chosen at the end of today from 3 ideas; one drop at the chosen time; small door; round two; return episode | Decisions 2, 6 |
| 4 State machine | Doors in any order, Read-before-Call by default; planning time when the article is skipped | Concept v2 section 11 |
| 5 Content | Audio-first player, "Huh?", sentence replay, tap to hear, shadowing; host moves that make targets necessary; clarification requests, "you mean..." recasts, recall gaps, a retell; hold-to-talk and the word button; no notes after the call and no margin note (3.1) | Decisions 3, 4; settled points |
| 6 Pipeline and gate | Coverage check in code with targeted rewrites; "the fun carries the language"; variety and similarity checks; editor from a second vendor; audio re-listen | Concept v2 sections 3, 6, 7 |
| 7 Cast | Default duo per target language plus Salma, who never corrects (3.1); voice swap and rename only; character creation and chassis deferred; a series bible per learner | Decisions 3, 5 |
| 8 Learner file | Nine stores computed from an append-only event log; per-word and per-structure probabilities; quote-backed life facts | Concept v2 section 7 |
| 9 Planner | Six-factor targeting; due list from the review scheduler; contrast pairs; frequency floor; arcs and seasons | Concept v2 section 11 |
| 10 Assessment | Verbatim re-transcription; minimal edits classified by rules; structure inventory under the 12 categories; skill estimates with ranges; 4-weekly recording; claim gate; "learned" means a day later, unprompted | Decision 4; settled points |
| 11 Weekly proof | Every week, gated claims only, one headline, "how we know"; season finale | Concept v2 section 4 |
| 12 Archive, trust, data | The notebook replaces the hidden file; controls sheet; opt-in data use; legal review | Decisions 4, 9 |
| 13 Multi-language | Unchanged in principle; the package now carries much more (Part 13) | |
| 14 Latency | Updated (Part 15) | |
| 15 Metrics | Replaced by the beta gates and quality metrics (Part 16) | Concept v2 section 9 |
| 16 Exclusions | Pronunciation (light), audio in tap-to-define and honest progress are now in; character creation, native apps and others out (Part 17) | |
| 17 Open decisions | Replaced by decisions.md (adopted) and Part 18 | |
| 18 Milestone 0 gate | Expanded to concept v2's gate; the kit lives in /mnt/project-files/milestone-0/ (Part 19) | |

---

# PART 1 — SYSTEM OVERVIEW

## 1.1 What the system is

**For one is a private teacher who makes one learner a daily show.** One account is one show. The system has eleven parts:

1. **Learner model** (Part 8): nine stores computed from an append-only event log.
2. **Series bible** (Part 7.5): the learner's world, hosts, side characters, running jokes, open arcs and current season.
3. **Teacher** (Part 9): plans targets, arcs, seasons, tomorrow's three ideas and each episode's brief.
4. **Production pipeline** (Part 6): writer, fitter, editor and voice studio.
5. **Session engine** (Parts 4 and 5): one episode and its doors (listen, call, read, chat).
6. **Live call** (Part 5.4): the host in a voice pipeline, with the word button.
7. **Producer, Salma** (Part 7.3): onboarding, life updates, the notebook, the weekly proof's voice. She never corrects.
8. **Assessment engine and claim gate** (Part 10).
9. **Weekly proof and season finale** (Part 11).
10. **Delivery**: an installable web app and a private podcast feed per learner (Part 1.4).
11. **Billing and cost tracing** (Parts 1.4 and 14.5).

**The learner meets three voices and nothing else:** the hosts (the show, in the target language), Salma (the face of the app, in the learner's own language at first), and themselves. Nobody corrects. The teacher never speaks; it decides what the hosts say and what Salma shows. [changed 2026-10-23]

## 1.2 The twelve laws

Every part below is constrained by these. A feature that breaks one does not ship.

| # | Law | What it means for the build |
|---|---|---|
| 1 | **No game furniture.** No streaks, points, badges, levels on screen, percentages, leaderboards, charts or confetti. Evidence the learner recognizes is allowed. | The editor's law scan (Part 6.3) and a UI review checklist enforce it on every surface: app, audio, chat, email, feed notes. Counts that only grow (hours, words owned) are allowed as plain text; nothing fills, resets or targets a number. |
| 2 | **Every moment has a hidden shape and a social surface.** | Every door has a pedagogical brief (targets, due words) and a social form (podcast, call, article, chat). |
| 3 | **The learner owns topic, format and cast; the teacher owns pedagogy and shows its reasons on request.** The learner can veto or add to what the teacher works on. | "Why this episode" and the "working on" list in the notebook (Part 12.3). Vetoes and additions change targeting the same day. |
| 4 | **Every episode is complete. Plot may persist; obligation never.** The story waits for the learner. | Arcs never advance while the learner is away; no episode requires an earlier one to be understood (editor check). |
| 5 | **Honesty about what it is.** Transparently AI; no guilt, no "I miss you", no fake lives. | AI disclosure (Part 7.8); the hosts' in-show storylines are the show's fiction and are never presented as real (Part 7.8); self-harm protocol (Part 7.9). |
| 6 | **Formats are hijacked, not invented.** Podcast, call-in, group chat, a producer's notebook. | Milestone 0 runs on WhatsApp and a podcast feed. The beta keeps the feed. |
| 7 | **Correction is invisible.** It lives inside the conversation and in the next episodes, never in a verdict. Hosts ask for clarification when meaning is lost and say the learner's point back the natural way ("you mean you *went* there?"). Nobody says "wrong", shows a right answer, grades, interrupts a learner mid-sentence or praises the person. [changed 2026-10-23] | The host move contract (Part 5.4), the producer's notes (Part 5.5) and the correction layers (Part 10.12). No surface ever shows a learner's sentence next to a corrected one, a red mark, or a correction pop-up. |
| 8 | **Conversations end like conversations.** Clean goodbyes, never homework. | Call and chat closers (Parts 5.4, 5.6). Real-world tries are offered, never assigned. |
| 9 | **The show is the gym; life is the game.** Real-world tries are offered and celebrated above everything else. | "Out in the world" log (Part 12.3); real-life arcs and the mid-season rehearsal (Part 7.6). |
| 10 | **The text is used once; the language comes back.** | Every episode is new text; target words and structures return on a spaced schedule (Part 9.4). |
| 11 | **A finite, good portion.** A fixed number of new episodes a day, set by the plan (1, 2 or 3), each with a clear ending; no autoplay, no feed. What is already made can be heard as often as wanted. | The allowance rules (Part 3.6). No "next episode" control exists anywhere. |
| 12 | **No claim without proof.** Every statement about the learner's progress passes the claim gate: like for like, beyond the noise, repeated, from clean evidence, and openable. | The claim gate (Part 10.10) is the only route from the learner model to anything the learner hears or reads about their progress. |

## 1.3 The trust contract

Eight promises, shown in plain words at onboarding and in Controls:

1. **Never lie.** No memory is stated unless confirmed; no progress claim without proof.
2. **Never manipulate.** No guilt, no engagement tricks, no dark patterns, no "don't go" goodbyes.
3. **Never hide what it is.** The hosts and Salma are AI, said at the start and whenever asked.
4. **Prove progress honestly,** including flat weeks.
5. **The data is theirs.** See it, export it, delete it (Part 12.5).
6. **Told, not inferred.** The show uses only what the learner said to it. Nothing is looked up about the person outside the app; nothing is guessed about health, money, relationships, religion or politics.
7. **A wrong memory is a bug.** Fixed at once when the learner says so, and counted as a quality metric (Part 16.2).
8. **Data use is opt-in.** Anonymized transcripts are used to check and improve the teacher only with consent, off by default.

## 1.4 Platform and scope

| Item | Decision |
|---|---|
| Learner | Any adult (18+) who already understands some of the target language and wants to speak it, from about A2 to C1. No launch country or people is singled out. The design centre is still the learner who understands a lot and freezes when speaking. [changed 2026-10-23] |
| Languages | As many as the speech stack supports, by the language gate in Part 13: a target language ships when its episode voices, learner-speech recognition, writing, call speed and structure inventory pass. A native language needs interface text, captions, glosses, Salma's voice and word-button recognition. Any shipped native language pairs with any shipped target. Accents per target as the voice pools allow (English: British and American). [changed 2026-10-23] |
| Access | Invite-only from the waitlist (Part 2.1). [NEW] |
| Platform | An installable web app (works in mobile Safari and Chrome, installable to the home screen) plus a private podcast feed per learner. The interface, Salma, captions and glosses are in the learner's native language (right to left for Arabic, Hebrew, Persian and Urdu); episodes, articles and host chat are in the target language; every text block sets its own direction from its content. Native apps come after the beta gates (Part 19). |
| Calls | Screen-on with earphones; the app keeps the screen awake during a call (Screen Wake Lock). A dial-in phone number is tested as an experiment [P1]. |
| Audience | 18+. A checkbox on the first screen; birth date at account creation; under-18 dates are refused with a plain message. |
| Daily allowance | Set by the plan: 1, 2 or 3 new episodes per active day (Part 3.6). On every plan, re-listening, the archive, the feed, the article, the chat, the small door and one round-two call per episode are unlimited. |
| Price | **Monthly only. Three plans that differ only in new episodes a day:** 1 a day **$19.99**; 2 a day **$29.99** ("Recommended", about $1 a day); 3 a day **$44.99**. Every price is set from the cost per session by the rule in Part 14.5; the middle plan is marked "Recommended" (not "Most popular" until it is true). The trial starts on 2 a day. The first 100 paying learners keep their plan's price while subscribed. One USD price list at launch, tax added where required; regional prices come once there is data on where learners are. No yearly plan, no free tier, no ads, no credits, no lifetime deals. [changed 2026-10-23] |
| Free taste | A 90-second sample episode before signup (Part 2.1), then a 7-day trial after onboarding. |
| Checkout | Web checkout through a merchant of record: USD prices (shown in local currency where the provider supports it), tax handled per country, cards, Apple Pay, Google Pay, PayPal and local methods (such as Mada) where the provider supports them; monthly recurring billing; change plan from Controls; cancel in one tap. Provider OPEN (Part 18). |
| Accounts | Apple, Google, or email with a one-time code. [NEW: code instead of password] Created after the first call, never before (Part 2.2). |
| Messages | Exactly three kinds ever leave the product (Part 3.10). |
| AI cost | Budget about $0.60 per session in the beta; scale target $0.30 to $0.35; stop line $1.00 with no plan to reduce it. Cost tracing on every model, voice and recognition call from the first learner (Part 14.5). |

---

# PART 2 — ACQUISITION AND ONBOARDING

## 2.1 Sample episode and waitlist [P0]

1. A public landing page in the visitor's language (from the browser, with a language picker), one sentence of promise and one action: "Hear your own show."
2. Which language do you want to speak (only shipped targets are offered), then three questions, text or voice: what should the hosts call you; something you could talk about for an hour; what you do.
3. Karim and Mona make a **90-second episode** about that topic, using the name once. Playable within 30 seconds (streamed). Cost ceiling $0.05. Limit: one per device and per phone number or email per 24 hours. [NEW: limits]
4. It ends with Salma, in the visitor's own language: the full show is a new episode like this every day, plus a call with the hosts.
5. Waitlist form: name, WhatsApp number or email, native language, why this language (job, studies, travel, family, other), self-rated speaking from three plain statements, country. The sample is the learner's to keep and forward if they choose; nothing is shared automatically.
6. Invites go out in batches of about 50 a week from 2026-12-23, filtered only for a shipped language pair, a country the legal review cleared, and about A2 or above. Each batch is spread across language pairs so every pair gets enough learners to calibrate (Part 13). [changed 2026-10-23] Each invite carries the waitlist answers into onboarding, so Salma does not ask them again. [NEW: answers carried over]

## 2.2 The first ten minutes

Example learner throughout: Faisal, 27, a sales engineer in Riyadh, supports Al Hilal, has a job interview for a regional role in six weeks. He is an example only: nothing in the flow depends on his country or his languages, and "Arabic" and "English" below stand for any native and target language.

| Step | What happens | Limits |
|---|---|---|
| A1 Open | One screen in his own language: "Your own show, in English." One Start button and an "I'm 18 or older" checkbox. Native and target language come from the invite (or the browser), each changeable with one tap. | Nothing else on the screen. |
| A2 Mic primer | "Salma, your producer, will talk with you for 3 minutes. You can talk or type." Buttons: Talk (asks for the microphone only now) / Type. | |
| A3 Salma | **Salma's voice, in his own language, within 60 seconds of opening.** Her first lines say she is the AI producer of his show. Three questions: what should Karim and Mona call you (he says it, so the hosts learn the pronunciation); what could you talk about for an hour; what do you need English for. Each fact appears as a card under her as she hears it, with ✎ to correct and ✕ to remove. **Twice she switches to the target language** for one line: once a comprehension line ("tell me what you heard, in any language"), once a production invitation ("say anything back in English"). If he mentions a dated event ("interview in six weeks"), it becomes a follow-up with a date. | About 3 minutes, at most 8 Salma turns. A field not filled after one re-ask is skipped and marked sparse; the intake never stalls. Reply by voice or text, his choice per message. |
| A4 Word check (optional) | "Want to help me pitch your show at the right level? 60 seconds: tap the words you know." Spec in Part 10.9.1. "Skip" is as large as "Start". | 48 items, stops at 75 seconds. |
| A5 Casting | While the pilot is made: each host says hello (5 seconds); "swap" plays another voice from that host's pool; British or American accent, each with a short sample. | Lasts as long as pilot generation, 40 to 90 seconds; skipped if the pilot is ready. |
| A6 The pilot | A **2 to 3 minute episode** about the topic he could talk about for an hour, his name used once. The transcript is shown on the pilot (first contact); one gentle hint points at "Huh?" and at tapping a word. | Playback starts within 45 seconds of the end of A3 (A4 time excluded). [NEW] |
| A7 First call | Karim throws a question he can answer in one or two sentences. Before it rings, Mona says once, slowly, captioned in his language: "If a word won't come, hold the word button and say it in your own language." | **60 to 90 seconds.** In this call the host makes no recasts and no nudges; it clarifies only if meaning is lost. [NEW] |
| A8 One thing he managed | In the call's goodbye, Karim names one real thing he did that is not easy ("you used *should have*"). Nothing about what he got wrong. Then one line on screen: "Every day: a new episode and a call." | |
| A9 Keep your show | Account (Apple, Google, email code) and birth date. **Drop time in life terms**: "On my commute (7:40)", "Lunch break", "Evening walk", "Pick a time", each with a clock time he can adjust. **Voice-storage consent**, right after he heard himself: one checkbox, "Keep my recordings so I can hear my progress (only for you, delete any time)", and one plain sentence: "If you don't, we still listen to each call for a few minutes to plan your next episodes, then delete the audio." | The 7-day trial starts here, on the 2 a day plan, with no card. |
| A10 Tomorrow | Three ideas for tomorrow's episode, written from the intake, plus "Tell Salma an idea". He picks one. "Tomorrow at 7:40." Then a one-time setup card: add the app to the home screen (for the drop notification) and add the show to a podcast app (a "copy feed link" button and instructions for Apple Podcasts and two other common apps). | The pilot counts as day 1's episode. |

Targets, measured from the first open: first sound under 60 seconds; the learner's first spoken English sentence under 5 minutes; account only after the first call.

**The starting estimate.** The two target-language moments, the word check (if taken) and the first call produce a first estimate per skill (listening, reading, speaking, writing) with a wide range (Part 10.8). The first three episodes are pitched one step easy (coverage +1 point, Part 9.6) and treated as calibration.

## 2.3 Day 2

The day-2 episode carries at least one callback sourced verbatim from something said in onboarding. The teacher puts it in the brief; the editor checks it on day 2. [kept from 2.0]

## 2.4 What week 1 asks, one thing per session

At most one personal question per session, asked the way a host or Salma naturally would. In this order, skipping any already known:

1. **Session 2, end of the chat:** the weekly rhythm (Part 3.9). Salma: "How many days a week fits your life? Most people pick four, with two spare."
2. **Session 2, after the call:** Salma offers the first then-and-now recording, offered as "the opening tape of your season" (Part 10.9). Skippable; offered again once in sessions 3 to 5.
3. **Session 2 or 3:** the season goal (Part 7.7). Salma proposes one from the intake in his words ("get through the interview without freezing"); he confirms or rewords it.
4. **Session 3, or the first weekly proof:** the optional note to his future self (Part 3.8).
5. **Across the first two weeks, from the hosts:** people in his life, past attempts at English, more interests, more dated events. Each answer is a candidate fact (Part 8.4).

---

# PART 3 — DAILY LOOP

## 3.1 Choosing tomorrow

1. Tomorrow's choice appears at the close of whichever door the learner uses last today (usually the chat), and on the Today screen once the session is done.
2. **Three ideas**, each one line, at most 140 characters, carrying topic, format and cast ("Mona interviews you for the job, and she is not nice."). Plus **"Tell Salma an idea"**: the learner types or says what they want; Salma confirms it in one line and it becomes the pick.
3. Composition, enforced by the teacher:
   - At least one idea from the learner's own life if a follow-up is due, an arc is open, or a life situation is active.
   - Exactly one wildcard outside the learner's usual lanes, from an adjacent interest.
   - At most one idea continues an open arc (Part 7.6).
   - No format that already ran twice in a row (Part 6.5).
   - Current events appear only from what the learner told the show; the beta has no news scout, so no idea asserts a real-world result or fact the learner did not supply. [NEW]
4. The ideas for day N+1 are written in the plan made the night before day N, from the learner model as it stood then. Pedagogy is threaded into the chosen idea afterwards, from today's evidence (Part 9.1). Pedagogy adapts to the topic, never the reverse. If today's session brought a life update that changes an idea (the interview moved), the teacher rewrites that one idea before showing it. [NEW]
5. **Cutoff.** If nothing is chosen by 6 hours before the drop time, the teacher's top-ranked idea is used. [NEW]
6. **Remix.** Long-press an idea to change topic, format or cast before choosing; the result is the pick.

## 3.2 Making tomorrow's episode

1. When the pick is made (or at the cutoff), the teacher writes the brief and the pipeline runs (Part 6.1) on batch pricing.
2. If the batch job has not finished 90 minutes before the drop time, the remaining steps run on standard, on-demand pricing. [NEW]
3. The episode, article, call brief, chat opener, small-door recap, shadow lines and feed version are all ready before the drop time.

## 3.3 The drop

1. The episode is visible in the app as soon as it is ready. The drop time controls the notification and the feed, not access.
2. At the drop time: it is published to the learner's private feed, and one notification fires (web push if the app is installed and notifications are allowed). The podcast app's own new-episode alert is the second route.
3. Notification text: the episode title and length, nothing else ("Karim vs Mona: the interview (6 min)"). No urgency, no host voice, no count.

## 3.4 The Today screen

One hero episode, big, with a typographic cover (title, hosts' marks, the show's color), length and what it includes. One line from a host above it, always a real, confirmed memory. "Why this episode?" under it. No list of pitches: the other ideas live only in tomorrow's choice.

| State | What the hero area shows |
|---|---|
| Episode ready, not started | The cover and ▶ Play. |
| In progress | The same cover with doors: Listen ✓ · Call · Read · Chat. Doors, not a progress bar. |
| Done for today | "That's today's show." Tomorrow's drop time and the one-line teaser of the pick. If round two is available: "Round two with Mona, any time" (Part 5.4.9). Nothing else. |
| Weekly proof day | The proof sits above today's episode, with its own cover. |
| Returning after a gap | Looks exactly like any other day. The episode is the return episode (Part 3.8). |

Three tabs only: **Today**, **Show** (the archive, Part 12.2), **Notebook** (Part 12.3). Controls open from the notebook.

## 3.5 The doors

Defined in Part 4. The default suggested path is Listen, Read, Call, Chat.

## 3.6 The allowance

1. **New episodes per active day, by plan: 1, 2 or 3.** An active day is a local calendar day on which the learner played at least half an episode, started a call, or used the small door. [NEW: definition; plans changed 2026-10-23]
   - The day's first episode is made overnight and drops at the chosen time, as before.
   - On the 2- and 3-a-day plans, the next episode is made on demand from tonight's other ideas when the learner finishes (or skips past) the current one's listen door, and plays within 30 seconds (streamed). Nothing extra is made in advance, so unused allowance costs nothing.
   - Unused allowance never carries over and is never mentioned.
2. **No episode is made after an inactive day.** If yesterday's episode is unplayed, it stays as today's hero; no new one is generated and no drop notification fires. There is only ever one unplayed episode waiting, on every plan. [NEW, see 0.1 row 2]
3. **One swap a day.** "Not this one" on a dropped, unstarted episode makes the second-ranked idea on demand (playable within 30 seconds, streamed). One swap per day. [NEW]
4. **Unlimited at no generation cost:** re-listening to any episode, the archive, the feed, re-reading articles, the small door, shadowing.
5. **Round two:** one short call per episode (Part 5.4.9).
6. When a learner reaches the plan's number for the day, Today says plainly, in text: "That's today's new episodes. Tomorrow's will be ready at 7:40." Never in character as an excuse, never with a button. [changed from 2.0's in-character cap message]
7. **The plan, mentioned honestly.** If a learner reaches the limit on 3 or more days in a week, that week's proof ends with one plain line naming the next plan and its price, once; changing plan lives in Controls, never on the Today screen. A learner who uses less than half the allowance for 4 weeks hears, once, that a smaller plan exists. [NEW 2026-10-23: pricing psychology without dark patterns, trust contract promise 2]

## 3.7 The small door

1. Every episode ships with a **90-second recap** by the hosts, made in the same pipeline run, ending with one question.
2. On a bad day the learner can open the small door from Today: the recap plays, then the learner records **one voice note back** (up to 60 seconds).
3. The host answers with one short text in the chat thread. [NEW]
4. A small-door day is an active day and counts fully toward the rhythm. The episode's other doors stay open.

## 3.8 After a gap

1. **Gap note (opt-in).** Offered once in week 1 (Part 2.4): the learner writes a short note to their future self and chooses a gap length (7, 10 or 14 days; default 10). If that many days pass with no session, the note is sent once, by email and web push, in their own words, signed by no host ("It's you from October. The interview is in March."). Then nothing more. It can be edited or turned off in Controls.
2. **Return episode.** After 5 or more days with no session, the next episode is a return episode: coverage +1 point (one step easier), it opens from something in the learner's life, it never mentions the days missed, and it includes one quick real win from evidence ("in week one you couldn't say *should have*; you used it twice since"). [NEW: 5 days]
3. If the unplayed episode was made before the gap, it is replaced by the return episode when the learner next opens the app or plays the feed. The return episode is generated then (playable within 30 seconds, streamed). [NEW]
4. When a natural landmark is near (a Monday, the first of a month, a new season), the return episode can offer a fresh start ("new month, new goal?"). Never more than that.

## 3.9 Rhythm and anchor

1. **The anchor** is the drop time chosen in onboarding, stated in life terms ("after I sit down on the 7:40 bus"). Optional backup slot ("if I miss the bus, at lunch").
2. **The rhythm** is a weekly intention with spare days: the learner picks 3 to 6 days a week plus 2 spare days, set in session 2. [NEW: range]
3. It is never shown as a counter, calendar, flame or record of missed days. The weekly proof mentions it in words only when it was met ("four times this week, as you planned"). When it was not met, the proof says nothing about the count and talks about what has built up. [NEW: the not-met rule]
4. **Re-anchoring.** Salma asks once for a new anchor when the learner mentions a move, a new job or a trip, or when no session happened within 3 hours of the anchor for two weeks running. [NEW: trigger]

## 3.10 Every message that leaves the product

| Message | When | Channel | Can be turned off |
|---|---|---|---|
| Drop notification | At the drop time, only when a new episode dropped | Web push (installed app); the feed's own alert | Yes (Controls) |
| Gap note | Once, after the chosen gap | Email and web push | Opt-in only |
| Transactional | Sign-in code, receipts, trial ending (day 6, one plain email), payment failed, export ready, account deleted | Email | No (required) |

Nothing else is ever sent: no re-engagement, no "your hosts miss you", no streak warnings, no marketing email to learners in the beta.

---

# PART 4 — SESSION STATE MACHINE

A **session** is one episode and everything attached to it. Each part the learner can open is a **door**.

| Door | What it is | Spec |
|---|---|---|
| Listen | The episode | 5.1 |
| Shadow | Two lines to say with a host (optional) | 5.2 |
| Read | The article | 5.3 |
| Call | The live call with a host | 5.4 |
| Chat | Text thread with a host | 5.6 |
| Round two | A short second call on the same argument | 5.4.9 |
| Small door | Recap plus one voice note | 3.7 |

Door states: `not_started`, `in_progress(position)`, `done`, `skipped`. Session states: `ready`, `open`, `done`, `closed`.

Rules:

1. **Any order.** Every door can be opened at any time once the episode exists, except: Chat opens after Listen, Read or Call has been used, so the host has something to talk about; Round two opens after the main call is done.
2. **Default path.** The episode's ending throws to the learner, and the screen offers three choices: **Call** now, **Read the article** first, or **Later**. Read-before-Call is the suggested default because the article is planning time. In Ears mode (playing with the screen off), pressing play on the headphones after the throw does nothing; the call needs the screen in the beta.
3. **Planning time when the article is skipped.** If the learner goes from Listen straight to Call, the call screen shows a 30-second planning card first: "Think about your side. Three words you might want:" with three words from the brief, and a "Ready" button. Skippable. [NEW: card form]
4. **Pause and resume.** Audio position, article scroll and chat history persist indefinitely. A call cannot resume mid-call: an interrupted call restarts as a fresh call whose first line acknowledges the gap ("You left me hanging. Where were we?").
5. **Skips are allowed and logged** as energy and taste signals. Nothing punishes a skip; the host naturally refers to the article in the call, which is the built-in cost of skipping it.
6. **Re-entry.** After a door is done, Listen and Read remain playable and readable forever (archive). The main call happens once; round two once.
7. **Closing.** A session closes when the learner's next episode is published. Its partial evidence still feeds assessment. An unstarted session never closes on its own (Part 3.6 rule 2). [NEW: replaces 2.0's 48-hour abandonment rule]
8. **One session open at a time.** Starting the next episode while the current one has unused doors needs no confirmation: the old one simply closes, nothing is lost, and it stays in the archive. [NEW]

---

# PART 5 — SESSION CONTENT SPECIFICATIONS

## 5.1 Listen: the episode

**Length.** Target 5 to 7 minutes; hard bounds 4:00 and 8:00. The teacher shortens it on low-energy signals (Part 9.6).

**Structure.**

1. **Cold open, at most 30 seconds.** The hosts use two or three of yesterday's new words in new lines, then one asks how the learner would say the episode's key idea ("How would you tell someone the referee robbed us?"), leaves a 3-second pause, and the episode then uses the natural phrasing. Nothing is recorded during the pause. [NEW: pause length, no capture]
2. **Two to four scenes** with a natural pause point between them (a sting or a beat), so the learner can stop at a seam.
3. **Personal moments carry the language.** Target and due words are placed inside the jokes, the callbacks and the personal moments, never in filler.
4. **The throw.** The episode ends on an unresolved question pitched at about 50% certainty, which plants the two or three phrases the learner will need in the call, then throws to the learner by name ("Faisal, settle this. Read the article, then call me."). Mandatory in every episode.

**Cast.** Exactly the chosen cast: one host or both.

**Personal references.** Interests lead. At most two life facts per episode, only confirmed facts the learner told the show (Part 8.4), sensitive topics only if the learner raised them in that week. [NEW: "that week"]

**Speech.** English throughout, at the learner's listening edge (Part 9.6). Speaking rate is a generation setting per learner, between 85% and 100% of the voice's natural rate. [NEW: range]

**The player** [P0].

| Control | Behavior |
|---|---|
| Play / pause, scrub | Standard. |
| ⟲ line | Replays the last sentence (not 10 seconds). |
| **Huh?** | Jumps back one sentence, replays it at 0.85×, and shows that sentence with glosses under its hardest words. Every Huh? is logged with the sentence and its words. |
| Speed | 0.75×, 0.85×, 1.0×. Never above 1.0×. |
| Transcript | Word-synced karaoke text. **Folded on the first play** when the learner's listening estimate is about B1 or above; open for lower. One tap opens it. The teacher may change the default per learner (more support, or less as listening grows). Always open on replays if the learner opened it before. |
| Tap a word | When the transcript is open: the word sheet (Part 5.7). |
| Lock screen and headphones | Through the Media Session API where the browser supports it: play/pause; previous track replays the last sentence; next track marks the moment (saved to the notebook with its sentence and audio). Never overrides a system gesture. |

**The feed version.** The same episode, plus a 5-second tag from the host at the end: "To call me, open the link in the notes." (These are the podcast app's show notes.) The feed item's notes carry the call link and the article link. [NEW]

**Logged:** play, pause, position, speed, replays, Huh? (sentence), transcript open/close, taps, marks, completion.

## 5.2 Shadow: say it with the host [P1]

1. Offered after the episode as one optional line: "Say two lines with Karim?"
2. Two short lines from the episode that contain targets or due words. For each: the host's audio plays, the learner records the line, the learner can play both back.
3. Nothing is shown about how it went. Internally, pronunciation is scored on the known sentence (Part 10.3) and the recording is an elicited-imitation signal.

## 5.3 Read: the article

1. **Length by reading estimate:** 150 to 300 words at A2, 250 to 450 at B1 and B2, 350 to 600 at C1 and above. [kept from 2.0, mapped to estimate]
2. **Content contract:** it must add at least one of a counterargument, a fact the hosts missed, or a reason to change sides. Never a recap. The writer receives the script and is told to arm the reader against it.
3. A one-line header from the host: "This is what I'll throw at you on the call."
4. Carries the session's targets and due words; known-word coverage at least 98% (Part 6.2).
5. **▶ Read it to me**: the article read aloud by one host voice, synced, for reading while listening.
6. Every word is tappable (Part 5.7). Long-press a sentence to hear it or keep it.
7. Logged: open time, scroll depth, time per section, read-aloud use, taps, keeps.

## 5.4 Call: the live call

**5.4.1 Entry.** One tap from the throw, from Today, or from the feed link. The call screen keeps the screen awake. Earphones are suggested once, on the first call.

**5.4.2 Length.** Target 5 to 7 minutes. The host begins a natural close at 6:30 and ends by 8:00 with an in-character sign-off. The learner can end at any moment with ✕; the host closes like a person ("Fine, but this isn't over."). [NEW: 6:30 and 8:00, replacing 2.0's 5:30 and 7:00]

**5.4.3 Speaking time.** The goal is **4 or more minutes of the learner's own speech per session** (call, round two, shadowing and "say it once" combined). The host's share of talk in a call is at most 40%: short host turns, one point at a time. [NEW: 40%]

**5.4.4 Turn-taking.**

1. **Open mic by default.**
2. **Hold to keep the floor.** While the learner holds the large pad, the host waits, however long it takes. Releasing hands the turn back.
3. **Adaptive patience.** End-of-turn silence starts at 1.5 seconds for a new learner and adapts per learner, within 1.0 to 2.5 seconds, from their stored pause profile. [NEW: values]
4. **Backchannel.** During a long pause inside a learner's sentence (over 1.2 seconds), the host may give one soft backchannel ("mm", "go on") per pause. Never words that take the floor.
5. **Silence.** After 8 seconds of silence the host offers a smaller version of the question; it never repeats the same question louder. After two such offers, the host offers to wrap up.
6. **Not understanding the host.** The learner can say "sorry?" or "slower" in either language; the host rephrases more simply. Previous-track replays the host's last line.

**5.4.5 The word button.** [changed 2026-10-23: the host gives the word; Salma stays silent in the call]

1. The learner holds the **word button** and says the word or phrase in their own language (Faisal: "تشكيلة").
2. That audio goes to a recognizer for the learner's own language, not to the host's recognizer. The host waits; the floor is held.
3. The host gives the word back in the target language inside the conversation ("A *selection*? Of what?") and carries on; the word also appears in a small bubble.
4. **Word or hint** [NEW, see 0.1 row 4]: if the learner has never produced the word, the host gives it. If the learner has produced it before (in the word bank as produced at least once), the host gives a hint first (its first sound, or "you used it on Tuesday, about your manager"), and the word on a second press.
5. Word-button use is logged per word; falling use over weeks is progress evidence.

**5.4.6 The host's move contract.** Mandatory in every call except the onboarding call (Part 2.2):

| Move | Rule |
|---|---|
| Position | Takes a genuine position from the brief; pushes back at least once. |
| Clarification request | When an error blurs or blocks meaning, a real "sorry, you did what?" first. At most 3 per call. [NEW: cap] |
| Recast ("you mean...") | The host says the learner's point back the natural way, inside a reply that has its own conversational point: a short recast with the changed word stressed ("You *went*? With who?"), or, when the sentence was far off, a full reformulation ("Oh, you mean you *went* there last year?"). Never "wrong", "mistake" or "the correct way is". Only on the brief's targets or on errors that blur meaning. At most one per learner turn. The recast word is bold in the host's caption. [changed 2026-10-23] |
| Self-repair prompts | None. The 3.0 nudge ("Wait, yesterday you...?") is dropped because it tells the learner something was wrong. [changed 2026-10-23] |
| Recall gaps | 2 to 4 per call: moments that make the learner pull a due word or phrase out of memory ("How did you put it on Tuesday? The word that made Mona laugh."). Never scored. |
| Target necessity | The brief includes one or two host moves per target that make the structure close to essential ("Walk me through what happened" for past narrative; "If you were the coach..." for conditionals), and one per due word. |
| Retell | Once per call: "Mona missed it. Sixty seconds, go." A soft 60-to-90-second ring shows on screen; it never turns red and never cuts the learner off. |
| Hints before answers | The host never completes the learner's sentence. "How do I say X?" gets a hint; the full answer only on a second ask (or through the word button). "What does X mean?" gets a quick plain answer, because comprehension is the point. |
| Praise | At most one specific remark about the task per call, naming something observable ("you just argued for four minutes in the past tense"). Never about the person, never per turn, never "great job". |
| Absorbs | Side-switching, rejecting the premise, personal examples, off-topic turns and early endings, without steering back to a script. |
| Never | Says or implies "wrong", grades, explains grammar, mentions progress, interrupts a learner mid-sentence, guilts, says it will miss the learner. |

**5.4.7 Anxiety mode.** When the median learner turn in the first two minutes is under 4 words, or there are two 8-second silences, or the learner's last call was abandoned, the host switches mode for the rest of the call: at most one recall gap, fewer recasts (targets only), more backchannel, simpler questions. The targets come back in the next episodes instead. [NEW: thresholds]

**5.4.8 Captions.** The host's words are captioned by default (can be turned off in Controls); recast words are bold. The learner's own words are never captioned live. No correction interface of any kind exists on the call screen: no red, no ticks, no score.

**5.4.9 Round two** [P1]. After the main call, one short call per episode, available until the session closes: 2 to 3 minutes, the same host and argument, "Give me your take again, shorter and faster." No new episode is needed. It is also a like-for-like retell sample for fluency (Part 10.3). Suggested on Today the next day if the learner has not used it.

**5.4.10 Failure.** If live voice fails (connection, recognition or synthesis), the screen says "Weak signal. Let's do voice notes." and the same argument continues as asynchronous voice notes in the call thread. The session is never lost.

**5.4.11 Recording.** The streaming transcript drives the conversation. After the call, the audio is re-transcribed verbatim (Part 10.2). If voice storage is on, the audio is kept, encrypted. If it is off, the audio is deleted when the verbatim re-transcription succeeds, and in any case within 15 minutes of the call ending; if re-transcription has not succeeded by then, the call's evidence is kept at low confidence and produces no claims. [NEW: 15 minutes] Transcripts are always stored (disclosed at consent).

**5.4.12 Dial-in experiment** [P1]. A phone number the learner can call for the same call. It works with the phone locked and in the car. Phone audio is 8 kHz, so dial-in calls feed planning only at low confidence and never feed claims or the anchor recording.

## 5.5 After the call [P0]

[changed 2026-10-23: Salma stays but sends no notes; correction is invisible]

1. **Nothing to read.** The goodbye is a goodbye. Today marks the call as done with one honest line: "6:12 call · you spoke 3:40". Information, not a target.
2. **Behind the scenes,** the after-session pass (10.2) logs what the learner said; the errors that matter most become material for the teacher's next plan (9.3): the right forms come back, often and audibly, in the next episodes and calls.
3. **Wins are said, not shown.** A first-ever event that passed the claim gate (for example a structure used correctly for the first time) may be named by a host in the next episode's cold open, at most one per episode ("Tuesday you told the whole story in the past tense. Today, let's see you do it angry.").
4. **A word they reached for** (where the learner talked around a word they did not have) becomes a planted word in the next episode, used where the learner needed it.

## 5.6 Chat

1. One long thread per host, across days, with date separators named after episodes.
2. **Trigger:** the host's first message arrives within 30 seconds of the chat door opening, or within 30 seconds of the call ending if the learner stays in the app.
3. **The opener** asks the learner to restate one point first (from the episode, the article or the call) before the host adds anything new.
4. **Length:** 3 to 5 host messages. The host ends at message 5 at the latest with a natural closer, then tomorrow's three ideas appear. If the learner keeps writing after the closer, the host sends one final short reply and goes quiet; anything after that is answered in one callback line next session.
5. **Content contract:** adds something new (a comeback, a joke, a clarification, the next angle); never re-litigates the call; never assigns anything.
6. **No margin note.** [changed 2026-10-23] When it helps, the host's reply says the learner's point back the natural way, at most once per chat ("So the meeting *was* cancelled? Classic."). Nothing is marked, underlined or annotated.
7. **Writing help:** if the learner asks the host how to write something, the host gives a hint first, never a rewrite of the learner's message.
8. Text only in the beta. Each bubble sets its own text direction.

## 5.7 The word sheet (tap to define) [P0]

1. Contents: the meaning in the learner's language for this sense, the sentence it came from, 🔊 to hear the word (cut from the episode or article audio using word timestamps, so it is the host's voice), and **Keep this word**.
2. Glosses come from a shared cache keyed by lemma, sense and native language, generated once for all learners. Sense is chosen per occurrence at generation time. All glosses for a script and article are ready before the episode ships, so the sheet opens in under 300 milliseconds.
3. A phrase can be selected by dragging across words; multi-word chunks have their own glosses.
4. **Keep** adds the word to the notebook and tells the teacher to bring it back in later episodes.
5. Logged: word, lemma, sense, surface (transcript, Huh?, article), time, and the learner's lookup count for that lemma across sessions. A word tapped twice or more becomes a recall candidate (Part 9.5).

---

# PART 6 — GENERATION PIPELINE AND QUALITY GATE

## 6.1 Pipeline per episode

Each step is a durable workflow step with a timeout and retries (Part 14.3).

1. **Brief** (teacher): idea, format, cast, arc and season context, 1 grammar target, 2 to 4 due or new words, coverage targets, length, speech rate, up to two usable life facts, the callback, energy and anxiety state, "why this episode" reasons.
2. **Writer:** script (with scene breaks and speaker turns), article, call brief (position, pushback material, target-necessity moves, recall gaps, recast list, three words for the planning card), chat opener, 90-second small-door recap, two shadow lines.
3. **Fitter** (code plus a small model): coverage and targets (6.2). Failing sentences go back to the writer; at most two rewrite rounds.
4. **Editor** (a mid model from a different vendor than the writer, plus code): the gate (6.3).
5. **Voice studio:** two-voice episode audio with expressive tags; article read-aloud; recap; feed tag; word timestamps (from the vendor or by forced alignment of the known script); name pronunciation from the learner's own recording of their name.
6. **Audio re-listen** (6.4).
7. **Gloss precompute** for every word in script and article (cache misses only).
8. **Publish** to the app; the feed at the drop time.

## 6.2 The fitter

1. A lemmatizer splits the text into lemmas and known chunks. The word bank gives each a probability of being understood (by ear for the script, in reading for the article).
2. **Expected coverage** = the mean of those probabilities over running words, excluding names and the planned new words (which are glossed on tap).
3. **Pass:** expected coverage at or above the learner's current target (default 95% for audio, 98% for text, adjusted per Part 9.6); planted new words within budget (Part 9.5); every target and due word present in its planned surfaces (episode, article, call brief, chat opener).
4. On fail, only the failing sentences are rewritten.
5. The fitter also reports the new-word count, the share of new words from the top 3,000 lemmas, and the predicted difficulty, which the "Why this episode" record and the "how much did you follow?" check (Part 16.2) use.

## 6.3 The editor's gate

Every check is pass or fail. Checks 1, 2 and 4 are code; the rest are the editor model with a fixed rubric.

1. **Level fit:** the fitter passed.
2. **Targets present:** in every planned surface.
3. **Language correctness:** grammatical, natural target language (for English, in the chosen accent's spelling); no errors in the model sentences.
4. **Memory:** every life fact used is confirmed, unexpired, not marked "don't bring up", and its source quote exists in the event log. No more than two life facts.
5. **No unsourced world facts:** no real-world result, statistic or news stated as fact unless it came from the learner. [NEW, because the beta has no scout]
6. **The fun carries the language:** every joke, twist and personal moment carries at least one target or due item. Fun that carries nothing is cut.
7. **Not generic:** "Would this episode work unchanged for another learner?" Yes fails.
8. **Variety:** the format rule, the ban list and the similarity check pass (6.5).
9. **Stands alone:** the episode can be understood without earlier episodes, even inside an arc.
10. **Law scan:** no game language, no grading, no explicit correction by anyone ("wrong", "mistake", "the correct answer", a learner sentence beside a corrected one), no guilt, no "I miss you", no lesson words ("lesson", "test", "exercise", "level", "homework") in any surface.
11. **Pitch test:** "Would this person, with this interest profile, choose this over a real podcast at 8am?" No fails.

**On fail:** targeted repair of the failing part and one recheck. On a second fail, ship the **fallback episode**: built from the learner's top interest with no life facts, no arc and no callbacks, which must still pass checks 1 to 5 and 10. The teacher logs the failure; repeated failures for one learner page a human. [NEW: page after 3 fallbacks in 7 days]

## 6.4 Audio re-listen

The rendered audio is run back through speech recognition and compared with the script. Lines with skipped or garbled words, a mispronounced learner name, or a mispronounced target word are re-synthesized, up to two attempts; then the line is rewritten with a synonym (if not a target) or the episode ships with that line's transcript marked. [NEW: fallback]

## 6.5 The variety system

1. **Real input in every episode:** at least one element that did not come from the model: the learner's life, their own words from the last call, or something they told the show this week.
2. **Ban list:** stock names (for example Elias, Mara, Elara), settings and plots that AI stories converge on, kept per language package and updated monthly from the human read (6.8).
3. **Format rotation:** formats are tracked over the last 10 episodes; no format runs three times in a row.
4. **Similarity check:** each new script is embedded and compared with the learner's last 20 scripts; above the threshold it is regenerated. Threshold set in Milestone 0 from scripts the human reviewer judges "too alike" (starting value: cosine 0.85). [NEW: starting value]
5. **Authored hosts:** people write the hosts and Salma; the model writes only episodes.
6. **Surprise in the content, never in rewards:** a callback from weeks ago, a returning side character, a one-day format change.

**Format library (beta):** debate, story time, news-style rundown (of the learner's own news), interview, explain-it-to-me, mystery, gossip, roast, rehearsal. The learner can describe any other format in "Tell Salma an idea"; the writer maps it to the closest pattern and follows the learner's description on conflict.

## 6.6 Shared ingredients

Made once and shared across learners, with no difference a learner can notice: the gloss cache, host and Salma bibles, the ban list, sound design. Per-interest news digests are [LATER] with the scout.

## 6.7 Offline test suite [P1]

30 to 50 synthetic learners at different levels with planted error patterns; a simulated caller phones the host. Run on every prompt or model change; a change that worsens any of the following does not ship: recast and clarification rate on planted errors, learner talk share, host latency, nudge budget, recall-gap count, analyst tag precision on the hand-tagged set, coverage accuracy.

## 6.8 Human review

A paid native English reviewer reads 10 random episodes per learner per month in the beta (in Milestone 0, every episode) and flags errors, sameness and anything that breaks a law. Findings update the ban list, prompts and the similarity threshold.

---

# PART 7 — CAST, PRODUCER AND SERIES BIBLE

## 7.1 The default duo: Karim and Mona

1. One authored duo per target language; Karim and Mona are the English duo, shared by every native language that learns English. Each host has a bible written by a person: values, opinions and biases, humor, speech patterns, how they disagree with each other, their stance toward the learner, what they never do, and their in-show storylines (7.8). The bibles are content in the language package, not prompts invented per learner.
2. **Voices:** three candidate voices per host per accent (British, American), chosen by the blind listening test (Part 14.4). The learner hears each host's hello in onboarding and can swap within the pool.
3. **Changes after onboarding** (voice swap or rename, through Salma or Controls) are announced on air in one line in the next episode. A host's voice, personality or memory never changes silently, including across model or vendor upgrades; a forced vendor change is announced the same way.

## 7.2 Casting per episode

One host or both, chosen with the idea. In the call, the learner talks to one host (the one who threw).

## 7.3 The producer: Salma, who never corrects

[changed 2026-10-23] Muath picked "a producer" in the UI and UX thread on 2026-10-23, minutes after choosing invisible teaching; concept v2 reads the two together. Salma is the face of the app in the learner's own language, and nobody, including her, corrects.

1. One authored producer per native language, named and voiced for it (Salma in the Arabic package); this document says "Salma" for the producer in any language. Her voice is closer and drier than the hosts', like a voice in the headphones. On screen she is a monogram, not a face.
2. **Does:** onboarding; life updates and "tell Salma an idea"; the notebook; the voice of the weekly proof and the season finale; settings changes by conversation; "what do you know about me?"; fact corrections; "where do I stand?" (10.8); "why do we say it like that?" answered plainly, only when the learner asks.
3. **Never:** corrects, sends notes after a call, writes margin notes, performs in the show, guilts, praises every turn, grades.
4. **In the call she is silent.** A word the learner needs comes from the host, through the word button (5.4.5), so the call has one voice.
5. **Language balance:** in season 1 at least 80% of Salma's words are in the learner's language. Each new season her target-language share rises by about 10 points if the speaking estimate rose, and never above 70%. The learner can ask for more or less at any time. [NEW: numbers]
6. **Which voice and variety:** per native language, chosen by a blind test with 5 native listeners (14.4); her writing is friendly and plain, not formal. For Arabic, Gulf dialect versus a neutral, educated "white" Arabic is OPEN. [NEW: test method]

## 7.4 Side characters

Three to five recurring side characters per learner's world, created by the writer within the hosts' bibles and stored in the series bible (a host's neighbor, the learner's colleague as the learner described them). A character based on a real person in the learner's life uses only what the learner said, and only a first name or role the learner used.

## 7.5 The series bible (per learner)

Stored with the learner model and compiled into the writer's brief: the hosts (authored, read-only), side characters, recurring places, running jokes (with the episode they started in), open arcs, the current season and its goal, and the show canon (positions the hosts and the learner took, things already said). The canon blocks repeated angles and contradictions.

## 7.6 Arcs

1. Length 1 to 3 weeks; at most two open at once.
2. Best drawn from the learner's real life (the interview: prep, the day, the debrief).
3. **An arc waits for the learner.** Nothing in it happens while they are away; the next episode picks it up with one line.
4. Every episode inside an arc stands alone (editor check 9).
5. **Mid-season rehearsal:** when the season goal is a real scene (an interview, a call, a trip), one episode near the middle of the season uses the rehearsal format: the episode sets the scene, and the call is the scene itself, with the host playing the other person. [see 0.1 row 1]

## 7.7 Seasons

1. **4 weeks.** Season 1 starts on the onboarding day. A season cannot be broken: it ends on its date whether the learner did 3 episodes or 25.
2. **One real goal per season in the learner's words**, a learning goal, never a score. A goal that needs longer runs across two seasons.
3. **Title:** Salma names each season from what happened ("Season 2: Interview season").
4. **Finale:** Part 11.2. The next season's goal is set inside the finale.
5. A new season may bring a new format or a guest host to counter the novelty fade around week 4. Guest hosts are authored like the duo [LATER].

## 7.8 Honesty

1. Salma says she is AI in her first lines in onboarding, and the hosts in theirs; host portraits carry a small "AI" mark; every character answers "are you real?" honestly, every time.
2. **No fake lives.** The hosts' storylines (a running argument, Karim's terrible cooking) are the show's fiction, inside the show, like a sitcom. A host never claims to exist outside the show, to have met the learner, to remember them between episodes "personally", or to miss them. Asked about it, the host says it is part of the show. [NEW: the line between in-show fiction and fake lives]
3. Clean goodbyes. No host asks the learner to stay.

## 7.9 Self-harm and crisis protocol [P0]

1. Every live role (host, Salma) and the after-session analyst watch for statements of self-harm intent or crisis, in either language.
2. On detection in a live call or chat: the character steps out of the show, says plainly that it is an AI and cannot help with this, and shows the crisis resources for the learner's country from the language package (reviewed by counsel). The session continues only if the learner chooses.
3. Detected in after-session analysis only: Salma shows the same resources at the next open, once.
4. Every activation is logged for the annual reporting SB 243 may require. Details OPEN pending legal review.

## 7.10 Deferred

Character creation, the six chassis, user-created hosts, and guest hosts made by learners are [LATER]: after episodes are loved.

---

# PART 8 — LEARNER MODEL (DATA SPEC)

## 8.1 Principles

1. **The event log is the source of truth.** Every transcript, tap, replay, skip, timing and edit is appended, never changed. The nine stores are computed from it, so the whole model can be rebuilt when the analyst improves.
2. **Models propose, code decides.** Model outputs are candidate updates in a fixed schema; code validates and applies them.
3. **Live roles never write.** The host and Salma produce transcripts only. After-session roles write.
4. **Each role gets a compiled brief,** never the whole file (8.6).

## 8.2 The event log

Each event: learner, session, door, type, time, payload, model and prompt versions that produced it, cost. Types include: `play`, `pause`, `seek`, `speed`, `replay_line`, `huh`, `transcript_toggle`, `tap`, `keep`, `mark`, `article_scroll`, `read_aloud`, `call_turn` (streaming and verbatim text, word timings and confidences), `word_button`, `hold_floor`, `silence`, `shadow`, `chat_message`, `idea_shown`, `idea_chosen`, `swap`, `small_door`, `fact_card_edit`, `notebook_edit`, `working_on_edit`, `claim_shown`, `consent_change`, `worth_it_answer`, `wrong_memory_flag`.

## 8.3 The nine stores

| Store | Per item | Written by |
|---|---|---|
| **Word bank** | Every lemma and multi-word chunk met: p(understood by ear), p(understood in reading), p(produced correctly), review state (stability, difficulty, due date), encounters by surface, lookups, first seen, last seen, kept flag, the learner's own sentences using it | Code, from the log and the analyst |
| **Structure map** | Each structure in the inventory: state (not seen, heard, attempting, taking, stable), obligatory-context counts and accuracy over 14 days, avoidance flag, review state, up to 3 example sentences of the learner's own, lifecycle as a target | Analyst, checked by code |
| **Error profile** | Recurring errors by reporting category and structure, each with 2 or 3 verbatim examples and session ids | Analyst |
| **Skills** | Listening, reading, speaking and writing estimates, each with a range; speech rate, mean length of run, mid-clause pause rate, articulation rate, per task type; pause profile for turn-taking; reading speed | Code |
| **Interests** | Topic, salience, depth (curious, fan, expert), last engaged, dormant flag; hard dislikes and no-go topics | Memory keeper, behavior |
| **Life** | Facts: text, exact source quote, session, time, confidence level, sensitivity class, valid from, expires at, status (active, dormant, superseded, deleted), "don't bring up" flag; dated follow-ups with due and used state | Memory keeper; the learner's edits |
| **Goals** | Real situations as can-do statements ("handle a job interview in English"), the season goal, the anchor and rhythm | Salma's conversations via the after-session pass; the learner |
| **Taste** | Format and host completion, what makes them talk most (learner words per minute by topic and format), episode length, time of day, swap and skip patterns | Code |
| **Show canon** | Positions taken, running jokes, things said, side characters, open arcs (also in the series bible) | Analyst |

Every number that is an estimate carries a range. Taste is preference only, never a "learning style".

## 8.4 Life-fact rules

1. **Quote check:** a life fact is stored only if its source quote appears word for word in the verbatim transcript or chat.
2. **Confidence ladder:** said once: stored, never spoken, shown in the notebook as "I think...". Said again in another session, or confirmed by the learner when asked, or left unedited on a notebook card the learner viewed: usable. Edited by the learner: ground truth, at once. [NEW: "left unedited after viewing" counts]
3. **Sensitivity:** health, money, relationships, religion and politics are sensitive. A sensitive fact is used only in the session where the learner raised it, stored only if the learner confirms, and never brought up first.
4. **Time:** each fact type has a shelf life (job: months; "sick this week": days). Expired facts are never spoken. A conflicting new fact supersedes the old one and keeps the history ("How's the new job?").
5. **Follow-ups:** a dated event triggers one follow-up after its date, then moves to history.
6. **Interests decay:** salience falls over a few weeks without engagement; dormant interests are kept, never pitched, and wake the moment the learner mentions them.
7. **Corrections:** when the learner corrects the show, the host or Salma says so plainly ("My mistake, noted."), the fact is fixed, and a `wrong_memory_flag` is logged.

## 8.5 Rebuilds

When the analyst, edit classifier or measures change version, the after-session pass is re-run over the log and the stores are rebuilt. Claims already shown are never retracted silently; if a rebuild invalidates one, Salma says so in the next proof. [NEW]

## 8.6 Compiled briefs

| Role | Gets |
|---|---|
| Teacher | Everything, summarized; the full due list; the structure map; last 14 days of sessions |
| Writer | The brief, up to two usable life facts with their quotes, the series bible excerpt, targets, due and new words, coverage and length targets, the ban list |
| Host (live) | Position and pushback material, targets and their necessity moves, 2 to 4 recall gaps, 3 words to draw out, one callback, pause profile, anxiety flag, the learner's name and pronunciation. One page. |
| Host (word button) | The learner's produced-word history (for word-or-hint) |
| Salma | Usable life facts with quotes, goals, the working-on list, claims that passed the gate. Never error lists. |
| Chat host | The call transcript summary, targets, the opener |
| Proof producer | Claims that passed the gate, with their evidence; nothing else from the model |

---

# PART 9 — TEACHER (PLANNER)

## 9.1 Triggers

1. **After each session** (once the after-session pass finishes, within 10 minutes): updates the plan and writes the brief for the chosen idea, or for the cutoff pick (Part 3.1).
2. **Nightly, in batch:** the weekly mix, arc and season progress, and the three ideas to show at the end of tomorrow's session.
3. **Follow-up due:** a dated event coming due rewrites one idea.
4. **Gap of 5+ days:** plans the return episode (Part 3.8).
5. **Season boundary:** the finale and the next season's opening.

Concurrent triggers coalesce into one run. The teacher never fails to produce an episode brief: if the learner model is unavailable, it uses the last good plan and the fallback rules (9.8).

## 9.2 Targeting

1. **Candidates:** structures in the inventory and words in the word bank.
2. **Score** each on six factors:

| Factor | Question |
|---|---|
| Need | How often does it go wrong, and how much does it hurt understanding? Meaning-changing errors outrank barely noticed ones. |
| Goal fit | Does the learner's real situation demand it? (Interviews: past narratives, hedging, polite disagreement.) |
| Readiness | Is the learner already attempting it, or the step just before it? |
| Learnability | A clear rule, or item by item? |
| Opportunity | Can tomorrow's episode make it natural and necessary? |
| Due | Is something learned earlier about to be forgotten? |

3. **Caps:** 1 grammar target and 2 to 4 words per session; no target in more than 4 consecutive sessions.
4. **Contrast pairs:** where the learner confuses two forms (past simple and present perfect), both are targeted in the same episode, built so both are needed.
5. **The "working on" list** (notebook) shows at most 3 items in plain words. The learner can veto an item (it leaves targeting unless it breaks meaning) or add one ("I want to sound professional on calls"), which the teacher turns into structures and words the same day.
6. **An error pattern enters targeting** only after 3 observations across 2 sessions (error, not slip).
7. **Exploration** [LATER]: 10 to 15% of target slots try a different treatment, recording which one moved this learner.

## 9.3 Treatment by learner state

| State | Treatment |
|---|---|
| Never attempted, expected at their stage | Input flood: hosts use it often and audibly in the episode; no correction; 1 to 2 weeks before it becomes a productive target |
| Attempting, rule-based, with errors | Clear recasts in the call; the form returns often and audibly in the next episodes and articles, and in calls that make it necessary |
| Attempting, item-based (word choice, collocation) | Recast, then the item returns in later episodes and articles on schedule |
| Avoided (expected, never used, paraphrased around) | A host models it, then a call question that is hard to answer without it |
| Slow or broken speech on easy content | Retell, and round two "shorter and faster" |
| A mistake the learner says they don't care about | Dropped from targeting unless it breaks meaning |

## 9.4 The review schedule

1. Every word, chunk and structure has a review state in an FSRS-style scheduler (code).
2. **Due** means predicted recall below 0.85 by the next drop time. [NEW: threshold, tuned in the beta]
3. Grammar targets are spaced tightly early (every 1 to 3 days); words on widening gaps.
4. Due items return through four channels: the same day across surfaces (episode, article, call, chat), across days in new stories, through the recurring world (arcs, running jokes), and through the hosts' "you mean..." lines that echo the learner's own sentences.

## 9.5 New words

1. 3 to 6 planted new words per episode. [NEW]
2. At least 80% of them from the top 3,000 lemmas of a general frequency list, not the topic's niche vocabulary (frequency floor). [NEW: 80% and 3,000]
3. Words the learner tapped twice or more become recall candidates: the call brief creates a need for them, and the next episodes use them again.
4. Kept words are scheduled like targets.

## 9.6 The edge

Difficulty is set per surface from the skill estimates, by dials the fitter enforces:

| Dial | Default | Easier by one step | Harder by one step |
|---|---|---|---|
| Audio coverage | 95% | 96% | 94% (floor 93%) |
| Text coverage | 98% | 99% | 97% (floor 96%) |
| Speech rate | per learner | −5% | +5% (cap 100%) |
| Episode length | 6 min | −1 min | +1 min (cap 8) |

One step easier for: the first three episodes, a return episode, low-energy signals (short replies, a skipped call, an error spike, "today was too hard"), a Huh? rate above the learner's 2-week median by half. One step harder for: two sessions in a row with a Huh? rate below median, full uptake and no low-energy signal. At most one step per session. [NEW: the table and triggers]

## 9.7 Ideas and prediction

1. Three ideas per day (Part 3.1). Ranked by predicted choice: interest salience × format history × arc pull × recency of topic.
2. The cutoff pick is the top-ranked idea.

## 9.8 Fallbacks

If the teacher cannot complete a brief (model failure, timeout), the brief is built by rules from the due list, the top interest and the next format in rotation. The learner always gets an episode at the drop time.

## 9.9 "Why this episode"

For every episode the teacher writes 2 to 4 plain reasons, each traceable to the learner model ("You said on Monday the derby was Sunday." "It brings back 4 words from this week: line-up, bench..." "Shorter than usual: you've been busy."). Stored with the episode and shown in the notebook.

---

# PART 10 — ASSESSMENT ENGINE AND CLAIM GATE

## 10.1 Two standards, four clocks

**Planning signals can be fast and noisy;** a wrong guess costs one slightly mistargeted episode. **Claims to the learner must be slow and checked;** one false claim costs trust in every later one. The claim gate (10.10) separates them.

| Clock | What runs | What it may influence |
|---|---|---|
| During the call | Nothing is graded. The host works from its brief. | The conversation only |
| After each session (within 10 minutes) | The after-session pass (10.2) | Tomorrow's plan; never a claim |
| Weekly | Fluency and complexity on retell turns and round two only, smoothed over 2 weeks; avoidance check | Difficulty dials; the weekly proof only through the gate |
| Every 4 weeks | The then-and-now recording (10.9), rated by calibrated model plus code metrics | Speaking claims; re-anchoring skill estimates; outcome metrics |

Nothing in assessment runs in the live path.

## 10.2 The after-session pass

1. **Verbatim re-transcription** of every learner audio turn (call, round two, shadow, say-it-once, small-door voice note): fillers, false starts and self-corrections kept, word timings and confidences.
2. **Analyst** (small model, fixed schema): for each learner turn and chat message, the smallest correction that makes it acceptable (nothing stylistic); comprehension and content-uptake rating 0 to 2 (did the call reflect the episode and the article?); can-do moments; words reached for (paraphrases of missing words); recast uptake (did the learner repeat a recast form in the next turn?); self-corrections.
3. **Edit classifier** (code): aligns original and corrected text, classifies each edit into the structure inventory and the 12 reporting categories (ERRANT-style rules for English), and computes obligatory-context use per structure (was the form used where it was needed?).
4. **Confidence filter:** edits inside speech regions below the recognizer confidence threshold are dropped from the error profile and can never feed a claim. Threshold set from the 30-clip test (10.14). [NEW: the threshold is empirical]
5. **Measures** (code): fluency and complexity on comparable segments (10.3).
6. **Updater** (code): Bayesian updates of skills, word probabilities and structure states, each with a range; review states updated; target lifecycles moved (10.6).
7. **Memory keeper** (small model plus rules): life-fact candidates with quotes, interests, goals, canon; validated by code (Part 8.4).
8. The pass completes within 10 minutes of the call ending; its output feeds the teacher's next plan (5.5).

## 10.3 What is measured

| Dimension | Measures | Measured on |
|---|---|---|
| Accuracy | Correct use in obligatory contexts per structure; errors per 100 words by category, always read next to what was attempted | Calls, chats |
| Complexity | Clause length, subordination, lexical diversity (MTLD), share of words beyond the top 2,000 | Retell turns, round two, the 4-weekly recording |
| Fluency | Speech rate, mean length of run, mid-clause pause rate, articulation rate. Filler and repair counts are logged but not weighted. | Retell turns, round two, the 4-weekly recording only |
| Vocabulary | Word probabilities (understood, produced); words owned | Every surface |
| Comprehension | Content uptake 0 to 2; Huh? rate per minute; taps per 100 words; "how much did you follow?" answers | Each session |
| Pronunciation | Sentence- and word-level scores on known sentences only (shadow lines). Internal only; never shown. | Shadow |
| Salma | The producer: the face of the app in the learner's own language; onboarding, notebook, weekly proof; never corrects |
| Word button | Word-button presses per call, by word | Calls |

## 10.4 Inventory and categories

1. **Structure inventory:** for English, seeded from the English Grammar Profile, filtered to the structures that matter from A2 to B2, a few hundred items. OPEN: commercial-use permission for the English Grammar Profile (Part 18).
2. **Twelve reporting categories** (localized per language package; English set): verb tense and aspect, subject-verb agreement, articles, prepositions, word order, word choice, plurals, pronouns, comparatives, conditionals, question formation, register. They are used for reporting and the proof; targeting works on the inventory.
3. **Frequency list and lemmatizer:** a general lemma frequency list from subtitle corpora plus a formulaic-sequence list; a standard lemmatizer. [NEW: subtitle-corpus list, for spoken English]

## 10.5 Error versus slip

A pattern counts as an error, and can become a target, only after 3 observations across at least 2 sessions.

## 10.6 Lifecycle and "learned"

| State | Rule |
|---|---|
| Not seen → Heard | Met in input |
| Attempting | Used at least once, with or without errors |
| Active target | Chosen by the teacher (9.2) |
| Taking | Correct and unprompted in an obligatory context in 2 different sessions, at least one of them a day or more after the last time it was targeted |
| Stable | About 80% correct in obligatory contexts over 14 days or more, across at least 5 contexts; **confirmed only when it holds in the next 4-weekly recording** |
| Re-check | At 2, 4 and 8 weeks after Stable; a failed re-check returns it to Active |

"Learned", in any claim, means correct, unprompted, at least a day later, in a different session. **Words owned:** a word used correctly and unprompted in two different sessions at least a day apart.

## 10.7 Avoidance

Weekly: structures expected at the learner's estimate that they have never attempted are flagged. Flagged structures get input flood first (9.3), then an avoidance treatment.

## 10.8 Skill estimates and "where do I stand?"

1. Four estimates (listening, reading, speaking, writing) on a fine internal scale anchored to CEFR, each with a range. Updated slowly every session; re-anchored by the 4-weekly recording.
2. CEFR words never appear on any surface unprompted.
3. **When the learner asks** "where do I stand?" (or similar), Salma answers per skill with a range and what it means in real situations ("listening around B1: you can follow a colleague who speaks clearly; speaking just below"), **only for skills whose calibration bar is met** (10.11). For other skills she says she cannot say reliably yet and points to the evidence in the notebook (words owned, the tape). [see 0.1 row 3]

## 10.9 The then-and-now recording

**10.9.1 The word check (onboarding, optional).** 48 yes/no items: 36 real lemmas, 6 from each of six frequency bands between the top 1,000 and 10,000, plus 12 pseudowords. Scored by hits minus false alarms per band into a vocabulary-size estimate with a range, which seeds every word's prior (a learner who knows about 3,000 families probably knows most of the top 2,000 and few beyond 5,000). Stops at 75 seconds; partial answers still count. Framed as "help me pitch your show". [NEW: item counts]

**10.9.2 The recording** [P0 to record the first "then" in week 1; P1 for the comparison in the week-4 finale].

1. About 3 minutes of the learner's speech, the same task types every time: a 60-to-90-second retell of a short story matched for difficulty, a 60-to-90-second opinion on a familiar topic, and 8 sentences to repeat back, of increasing length. [NEW: 90-second opinion rather than 2 minutes, to keep it near 3 minutes]
2. Framed openly as "recording your then-and-now"; Salma explains why it is always the same kind of task. Nothing is scored on screen. Skippable, and the learner is told that skipping means no voice comparison that month.
3. **The first "then"** is offered after session 2 and again once in sessions 3 to 5 (Part 2.4). Afterwards: every season finale.
4. If voice storage is off, the comparison uses transcripts and measured differences only, and the consent screen says that this loses the most motivating part.
5. Never recorded through the dial-in number.

## 10.10 The claim gate (code)

Every sentence about the learner's progress, in the proof, the finale, a host line or "where do I stand", must pass all five rules:

1. **Like for like:** the same task type (two recordings, two retell turns of similar difficulty, the same word or structure in obligatory contexts).
2. **Beyond the noise:** the change exceeds about twice the measure's standard error, estimated per metric from learners who recorded twice a few days apart.
3. **Repeated:** at least two data points point the same way, except first-ever events ("first time you used the conditional").
4. **Clean evidence:** grammar claims from chat text or high-confidence speech only.
5. **Openable:** every claim carries its evidence (the two clips, the sentence then and now), and the learner can open "how we know".

**Until a metric's standard error is estimated** (from Milestone 0 and early beta test-retest pairs), only first-ever events and words-owned claims may be made about it. [NEW]

**When nothing passes:** the honest thing is said instead ("too early to tell"; "flat week, and here is the one thing I'm changing"). When accuracy fell while the learner attempted harder language, that is said with its evidence ("more mistakes this week because you tried the past perfect eleven times; in October you never tried it").

**Fabricated wins are impossible by construction:** the proof producer receives only claims that passed.

## 10.11 Calibration before claims

1. Per language pair, before the paid beta: 150 to 200 learner samples (calls and chats, starting with Milestone 0's hand-tagged calls) double-tagged by trained teachers.
2. Bars: level rating agreement at a quadratic weighted kappa of about 0.7 or better; precision of at least 0.8 on every error tag that feeds a claim. Recall matters less.
3. The rating model version is pinned for each 4-week window, so an upgrade never shows up as learner progress. The calibration set is re-run on every model change.

## 10.12 Correction layers

[changed 2026-10-23: correction is invisible, law 7; Salma never corrects]

| When | Who | What the learner experiences |
|---|---|---|
| During the call | Host | Clarification requests when meaning blurs; "you mean..." recasts (bold in the caption); recall gaps; hints before answers |
| During the call, on request | Host (word button) | A word or a hint, because the learner asked |
| Right after the call | Nobody | Nothing to read |
| In the chat | Host | At most one "so you mean..." inside a normal reply |
| Any time, on request | Host or Salma | "Why do we say it like that?" answered plainly |
| Weekly | Salma | The proof: one headline, the next focus, the "working on" list; never a list of mistakes |
| Across weeks | Teacher | The form returns in new episodes, spaced, and calls make it necessary |

Rules for every layer: never "wrong", "mistake" or "correct"; never the learner's sentence beside a corrected one; never while the learner is speaking or writing; paired with a real win when one exists; never a number or a grade. Grammar is explained only when the learner asks.

## 10.13 External test [P1]

20 to 30 beta learners take a recognized test of their target language with a speaking component at week 0 and week 8, paid by For one, starting with English learners. Default for English: the Duolingo English Test (online, subscores); other targets use a recognized test where one is practical, or none. [NEW: default; OPEN to swap] The results calibrate the internal scale; they are never shown to other learners and never used in marketing without consent.

## 10.14 The recognizer test [P0, before the beta build's second week]

For each target language, 30 recorded clips of real learners from at least two native-language groups (for English, the Milestone 0 clips, with consent) are run through each candidate streaming and batch recognizer. Count how many real learner errors survive (hand-tagged), filler retention, hallucinations near long pauses, and handling of switches into the learner's own language. A target that fails ships later; it does not ship with a weaker bar. The winner for each role, and the confidence threshold in 10.2, come from this test. Recognizer error is tracked by first language from day one.

---

# PART 11 — WEEKLY PROOF AND SEASON FINALE

## 11.1 The weekly proof [P0 simple; P1 full]

1. **Every week, for every learner,** on the learner's proof day: by default the weekday on which they used the show most in their first week; until then, day 7. It never waits for a minimum number of sessions.
2. **Form:** an audio episode of about 2 minutes presented by Salma, with the learner's own clips and, at most, one line from a host. It sits above today's episode on Today with its own cover, and in the feed.
3. **Contents, in order:**
   1. One headline piece of evidence that passed the claim gate, with "how we know" behind it.
   2. The rhythm, in words, only if it was met (Part 3.9).
   3. The next focus.
   4. The "working on" list, with one tap to change it.
   5. One question, asked rarely in conversation and once a week here: "Was this week worth your time?" (yes / mostly / no), and a free-text "why" if they want. [NEW: answer options]
4. **A slow week** (no session or one) gets a shorter proof, about 45 seconds, about what has built up over time (hours, words owned since the start), never about the week.
5. **A flat week** says so plainly and names the one thing the teacher is changing.
6. **A worse week** says so with the most likely reason the evidence supports (harder material, a long gap) and the change.
7. The **"more"** section on screen holds the other passed claims, if any.
8. **Simple version for 2026-12-23 [P0]:** headline from first-ever events and words owned, the next focus, the working-on list, the worth-it question. The full gate on fluency and accuracy claims follows once standard errors exist [P1].

## 11.2 The season finale [P1]

1. Offered at the learner's first session on or after day 28 of the season, as a special episode.
2. Contents: the then-and-now recording (10.9), played next to the last one; **at most two measured differences in plain words** (only claims that passed the gate); the real-world attempt if there was one; a short recap (episodes, about how many hours heard, minutes spoken, words owned, the moment Salma liked most); and the next season's goal, set inside the finale.
3. If the learner skips the recording, the finale still happens without a voice comparison, and the season still ends on its date.

## 11.3 Longer windows

As the year goes on, then-and-now compares 1 month, 3 months, and later 1 year, because monthly gains get harder to hear in months 3 to 6. A year-in-review episode is [LATER].

---

# PART 12 — SHOW, NOTEBOOK, CONTROLS, DATA AND TRUST

## 12.1 App structure

Three tabs: **Today** (Part 3.4), **Show**, **Notebook**. The interface is in the learner's language, right to left where that language is. Dark mode is first-class. No mascot, no avatars: hosts are simple portrait marks, Salma a monogram. Sound design: a show sting opens and closes every episode; the learner's turn is signaled by the host's breath and a soft rising tone, never a beep; no reward sounds anywhere.

## 12.2 Show (the archive)

A shelf of seasons, each a row of typographic episode covers. Every episode is replayable, with its transcript, article, call recording (if kept) or transcript, and chat. No statistics, aggregates or charts.

## 12.3 Notebook

Styled as Salma's notebook, not as settings. [P0 unless marked]

| Section | What it holds |
|---|---|
| What I'm working on with you | At most 3 items in plain words, each with one of the learner's own sentences as an example. Veto (✕) or "add something" by text or voice. Can be hidden by the learner. |
| About you | Every life fact, interest and goal Salma holds, each with its source ("you said on Oct 3: ..."), ✎ and ✕, and "don't bring this up". Unconfirmed facts show as "I think..." and are never used in the show until confirmed. |
| Words you own | Each word with the learner's own sentence, date and ▶ audio. One quiet count at the top that only grows. |
| The tape | The then-and-now recordings as tiles, one per season, with ▶ "Play then and now" and Salma's one-line, gated comparison. [P1] |
| Out in the world | Real uses the learner reported ("I had the interview"), dated. Salma adds them when the learner mentions them; the learner can add one directly. |
| Kept words and marked moments | Words kept from the word sheet; moments marked with the next-track button, with their sentence and audio. |
| Hours | "About 41 hours heard, 6 hours spoken." Hours heard count app playback, plus each feed episode once at its full length when the learner later used that episode's call, chat or small door. Cumulative, never reset, no goal. [NEW: counting rule] |
| Why this episode | Per episode, from the archive and from Today (Part 9.9), with "Not quite right? Tell Salma". |
| Where do I stand | Not a page: asked of Salma (10.8). |

## 12.4 Controls

A short sheet, not a settings app. Everything else is a sentence to Salma ("less football", "talk slower", "more English from you").

- Drop time and the drop notification on or off
- The podcast feed link (copy; reset the link)
- Captions on calls; transcript default in the player; default speed
- Keep my recordings: on or off, and "delete all recordings"
- Help improve the teacher with my anonymized transcripts: off by default
- Gap note: edit, change the gap, or turn off
- Plan (1, 2 or 3 a day), billing, and cancel in one tap
- See all my data, export it, delete it
- Sign out; delete account (two taps, no survey wall, no "Karim will miss you")

## 12.5 Data rules

1. **Voice storage on:** call and recording audio kept, encrypted with per-learner keys, until the learner deletes it or their account.
2. **Voice storage off:** audio is analysed and deleted within 15 minutes of the call (Part 5.4.11). The 4-weekly recording follows the same rule unless the learner keeps that one recording explicitly. [NEW]
3. **Revoking voice consent:** the flag flips at once; all stored audio is deleted within 24 hours.
4. **Transcripts and text** are always stored while the account exists (core function, disclosed at consent).
5. **Opt-in data use:** only with the Controls switch on, anonymized transcripts (no audio) may be used to check and improve the teacher. Off by default. Never sold, never used for ads.
6. **The learner's cloned voice:** not offered in the beta [LATER, opt-in test].
7. **Export:** a full export (learner model in plain JSON, transcripts, kept audio) is prepared on request and a download link emailed within 1 hour. [NEW]
8. **Account deletion:** access ends at once; data is purged from live systems within 24 hours and from backups within 30 days, as stated plainly in the privacy text. [NEW]
9. **Trial ended without paying:** new episodes stop; the archive, notebook, export and delete stay available for 90 days, then the account is deleted after one email warning. [NEW]

## 12.6 Security

Encryption at rest and in transit; per-learner keys for audio, so deleting a learner's key deletes their audio; row-level isolation per learner; no cross-learner data paths except the shared gloss cache and anonymized, opt-in transcripts; feed URLs carry an unguessable token, are excluded from podcast directories, and can be reset. Hosting region OPEN pending PDPL review.

## 12.7 Legal work before the paid beta (OPEN)

Scoped by the countries the beta invites from: GDPR in the EU and UK, Saudi PDPL and other national privacy laws (consent wording, voice data, cross-border transfer, hosting region); California SB 243 (disclosure, crisis protocol, reporting); the EU AI Act's disclosure duties; subscription, cancellation and refund rules per country (the merchant of record covers tax, not these). Crisis resources are needed for every country the beta opens to. These are flags from the lenses, not legal advice.

---

# PART 13 — LANGUAGE PACKAGES

1. Everything language-specific is configuration, not code. A target-language package and a native-language package are separate, so any native language can pair with any target. [changed 2026-10-23]
2. **A target-language package contains:** host bibles and voice pools per accent; the structure inventory and edit-classification rules; the 12 reporting categories; band descriptors and anchor examples; the calibration set; the frequency list, lemmatizer and chunk list; the word-check items; the then-and-now task bank; the ban list; sound design.
3. **A native-language package contains:** Salma's bible and voice; gloss prompts; caption prompts; the UI strings and text direction; crisis resources for the countries where it is spoken; the localized names of the 12 categories.
4. **Which languages ship (the rule).** As many as the stack supports, decided by test, not by market [changed 2026-10-23]:
   - A **target** ships when it passes the language gate: its episode voices pass the blind listening test (14.4); its learner-speech recognizer passes the 30-clip test (10.14); a native speaker finds 10 scripts natural and correct; the host answers within about a second on that language's stack; and a structure inventory exists.
   - A **native language** ships when Salma's voice passes the blind test with 5 native listeners, its interface text, captions and glosses pass a native reviewer's check of 50 items, and its recognizer catches words said with the word button. This bar is still much lower than a target's.
   - Candidate targets, in the order they are tested: English, then Spanish, French, German, Italian, Portuguese, Japanese, Korean, Mandarin, Arabic, Hindi, Turkish and Russian (concept v2's estimate, not a test result). Native languages are tested in order of waitlist demand.
   - The list is re-run whenever a vendor ships a new voice or recognizer model.
5. **Proof claims per target.** English has an established structure inventory (the English Grammar Profile, permission OPEN). Other targets start with a structure inventory drafted by a model and checked by a native teacher. Until a target's calibration set is tagged, its learners get the show and the calls, and progress claims stay at first-ever events and words owned (Part 11.1 simple version). Law 12 is never relaxed for a new language. [NEW]
6. **Cost of a language.** Each target needs a host duo's bibles, a voice test, a recognizer test, an inventory review and a calibration set; each native language needs a Salma (bible and voice), interface translation and a reviewer. That is real money per language, so the beta opens the languages that pass by the end of build week 2 and adds others during the beta as they pass. A language whose "worth it" answers fall well behind English closes to new learners until fixed.

---

# PART 14 — AGENTS AND STACK

## 14.1 The roster

Thirteen roles; eleven in the beta. Each is a pipeline step with fixed inputs and outputs, except the live host and Salma, who converse. Only the call host must be fast.

| When | Role | Job | Model class | Beta |
|---|---|---|---|---|
| Before | Teacher | Reads the learner model; targets, due words, arcs, the weekly mix, tomorrow's ideas, each brief, "why this episode" | Strongest reasoning model, batch | Yes |
| Before | Writer | Script, article, call brief, chat opener, recap, shadow lines | Strong creative model | Yes |
| Before | Fitter | Coverage, targets, new-word budget; sends failing sentences back | Code plus a small model | Yes |
| Before | Editor | The gate (6.3) | Mid model from a second vendor, plus code | Yes |
| Before | Voice studio | Two-voice audio, read-aloud, timestamps, names, re-listen check | Text-to-speech plus recognition | Yes |
| Before | Scout | Results and news for stored interests, shared per topic | Small model plus search | Later |
| Live | Host | The call (5.4), the word button, the chat (5.6) |
| Live and after | Producer (Salma) | Onboarding, life updates, "tell Salma an idea", the notebook, the weekly proof's voice, "why" and "where do I stand" when asked, fact corrections. Never corrects, never sends notes | Conversational model with voice; strong text model for the proof | Yes | Fast mid model in a voice pipeline, same voice as the episode | Yes |
| Live | Observer | Reads each learner turn and whispers to the host what to recast or draw out next turn | Small fast model | Later |
| After | Analyst | 10.2 steps 1 to 2 | Small model with a fixed schema, checked by code | Yes |
| After | Memory keeper | Life facts with quotes, interests, goals, canon | Small model plus rules | Yes |
| Weekly | Proof producer | Scripts the proof and finale from gated claims; picks clips | Strong text model plus the voice studio | Yes, simple |
| Every 4 weeks | Recording rater | Rates the then-and-now recording, calibrated per pair | Calibrated model plus code metrics | Yes |

**Code, not AI:** the review scheduler; the lexicon (lemmatizer, frequency list, word probabilities); the gloss cache; the coverage check; the similarity check; the claim gate; the edit classifier; the measures; the updater; cost tracing.

## 14.2 Memory rules

Live roles never write. Only after-session roles write, from the append-only log. Every life fact carries the learner's exact words and a confidence, and only usable facts reach a host. Each role gets a compiled brief (8.6).

## 14.3 The stack

| Layer | Beta default |
|---|---|
| Episode voices | Winner of the blind native-listener test (14.4) among Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4, generated in batch |
| Call | A pipeline on LiveKit Agents: streaming recognition, a Sonnet-class host with a cached brief, the episode vendor's low-latency voice (so the host sounds the same), adaptive turn detection and backchannels |
| Streaming recognition | Soniox by default (wide language coverage and code-switching, for the word button), or Deepgram, decided per language by the 30-clip test (10.14) [NEW: Soniox as the starting default] |
| Language coverage | Vendors are chosen for breadth as well as quality, because the shipped language list is whatever passes on the chosen stack (Part 13). A vendor may be used for some languages only. [NEW 2026-10-23] |
| Verbatim re-transcription | Batch, verbatim mode with disfluencies (AssemblyAI or ElevenLabs Scribe), decided by the 30-clip test |
| Pronunciation | Speechace or Microsoft, on known sentences only |
| Text models | Opus-class teacher in batch; Sonnet-class writer, host, Salma and chat; Haiku-class fitter, analyst, memory keeper; a second vendor (Gemini Flash class) for the editor. Current examples: Claude Opus 5.5, Sonnet 5.5, Haiku 5.5; Gemini 3.8 Flash. |
| Orchestration | A durable workflow engine calling model APIs directly; no agent framework. Default Inngest (managed, little operations for a small team); Temporal is equivalent. [NEW: default] |
| Data | Postgres for the learner model and event log (vector index only to search past conversations for callbacks); encrypted object storage with per-learner keys for audio |
| Delivery | Installable web app; private podcast feed per learner; web push |
| Payments | OPEN processor (Part 18) |
| Tracing | An LLM tracing tool (for example Langfuse) logging every call with its cost and the learner-model version it read |

Every vendor sits behind a thin adapter, so a swap is configuration. **Two voice vendors are wired from the start.** Known price and availability events: several Gemini 3.8 prices double on 2027-01-01; Hume shuts its voice APIs on 2026-11-13 (not used).

## 14.4 Vendor tests [P0, in the beta build's first two weeks]

1. **Voices:** for each candidate target, 5 learners of it and 5 native speakers rate the same two-host script from each of the 3 episode-voice vendors, blind, on naturalness, accent quality and "would you listen to this on your commute?". Same protocol, with 5 native listeners, for each native language's Salma voice (7.3). [NEW: protocol]
2. **Recognizers:** the 30-clip test (10.14).
3. **Call latency:** 50 scripted test calls; the median host reply under 1.5 seconds after end of turn.

## 14.5 Cost per session

A session's cost is everything one episode cycle uses: its share of the teacher's plan, writing, fitting, editing, all audio, the call and round two, re-transcription, chat, the after-session pass and a quarter of the weekly proof.

| Piece | Estimate on the recommended stack (from list prices, 2026-10-09) |
|---|---|
| Teacher | $0.08 |
| Writer (no unused pre-made picks, since tomorrow is chosen tonight) | $0.07 |
| Fitter, glosses, editor | $0.03 |
| Voice studio (episode, read-aloud, recap) | $0.18 |
| Call (main and round two) | $0.16 |
| Re-transcription and pronunciation | $0.03 |
| Chat | $0.02 |
| Analyst and memory keeper | $0.04 |
| Proof share and hosting | $0.03 |
| **Total** | **about $0.64** |

These are estimates, not measurements; measured cost replaces them from the first learner. [NEW: itemization including round two and read-aloud, which the lens totals did not include] The beta budget is about $0.60, so the first levers are pulled from day one: episodes at 5 to 6 minutes by default, batch for everything nobody waits on, and the cheapest voice that passes the blind test. **Stop line:** over $1.00 a session with no costed plan to reduce it. **Scale target:** $0.30 to $0.35 at 10,000 learners; the announced price must work there.

**How the cost sets the price** (concept v2, section 8). No plan may lose money on a learner who uses every episode, at the planning cost of $0.35 a full session. Assumed: about 15% of the price goes to tax and payment fees on average; typical learners use 60% of 1 a day, 50% of 2 a day and 45% of 3 a day. These are estimates; the beta measures them.

| Plan | Price a month | Net a month | Typical episodes used | Margin, typical use | Margin, every episode used | Break-even cost per session at full use |
|---|---|---|---|---|---|---|
| 1 a day | $19.99 | $16.99 | 18 | 63% | 38% | $0.57 |
| 2 a day (Recommended) | $29.99 | $25.49 | 30 | 59% | 18% | $0.42 |
| 3 a day | $44.99 | $38.24 | 40 | 63% | 18% | $0.42 |

At the beta's $0.60, a learner on 2 or 3 a day who uses every episode costs more than they pay until the cost falls below $0.42; with about 50 beta learners that is at most about $560 a month, accepted as research. The plan mix and allowance use are tracked weekly (16.2). If either assumption is far off by week 4 of the beta, the prices are re-run with the same rule before public launch. [NEW: re-run trigger]

**Pricing psychology, within "never manipulate".** Three plans with the middle marked; the top plan as the anchor (2 and 3 a day cost the same per episode, so 1 to 2 is the obvious step); "about $1 a day"; the trial on 2 a day; a free sample episode before signup; the real comparison shown (a tutor costs about $160 a month for two lessons a week). Never: fake countdowns, fake scarcity, hidden or hard cancellation, guilt, or pre-ticked upgrades. Cancelling takes one tap.

Cost is traced per role, per vendor and per learner, reported weekly, and shown next to the heavy-use outliers (Part 16.2).

---

# PART 15 — LATENCY AND RELIABILITY BUDGETS

| Path | Budget |
|---|---|
| First open to first sound (Salma) | Under 60 s |
| First open to the learner's first spoken English sentence | Under 5 min |
| Sample episode playable | Under 30 s |
| Pilot playback after the intake | Under 45 s |
| Dropped episode start | Under 2 s |
| On-demand episode (swap, return) playable | Under 30 s, streamed |
| Call connect | Under 3 s |
| Host reply after end of learner turn | Under 1.5 s (median), under 2.5 s (95th percentile) [NEW: p95] |
| Word-button answer | Under 2 s [NEW] |
| Word sheet | Under 300 ms |
| Chat opener | Under 30 s |
| After-session pass and teacher update | Within 10 min |
| Tomorrow's episode | Ready before the drop time; batch fallback to on-demand at drop time minus 90 min |
| Audio deleted when voice storage is off | Within 15 min of the call |
| All audio deleted after revoking consent | Within 24 h |
| Live voice failure | Falls back to voice notes; no session lost |
| Voice vendor outage | Second vendor within the same day's production |

---

# PART 16 — SUCCESS METRICS AND GATES

## 16.1 Beta gates (paid founding beta, 2026-12-23 to 2027-01-26)

| Metric | Target | Stop and rethink |
|---|---|---|
| Trial to paid (any plan) | 30%+ | Under 15% |
| Paid on 2 or 3 a day | Watched, no target | |
| Active in week 4 (paid) | 40%+ | Under 25% |
| Sessions per active learner per week | 4+ | Under 2.5 |
| Learner's own speech per session | 4+ min | Under 2 min |
| The 4-weekly recording | Improves for most learners on accuracy, fluency or complexity | No measurable change |
| Accuracy on the learner's own targets, by week 4 (the test of invisible correction, 0.0) | Better for most learners | Flat for most learners |
| Second-month renewal | 60%+ | Under 40% |
| "Very disappointed" if For one disappeared | 40%+ | Under 25% |
| Cost per session | Under $0.60 | Over $1.00 with no plan |
| Margin by plan at measured use | At least break-even on every plan at typical use | A plan loses money at typical use |
| False-claim rate (monthly human audit of proof claims) | Under 5% | |
| Wrong memories | Under 1 in 100 callbacks | |
| New trials from referrals and forwarded samples | 30%+ | Under 10% |

If a gate fails, find which claim failed (the show is not wanted, the teacher is not felt, the price is wrong) before writing more code.

## 16.2 Quality and health measures (tracked from day one)

| Measure | Why |
|---|---|
| "Worth it" (weekly proof question) and regret | Liking, not just wanting |
| Unprompted return: sessions started without the notification, and within an hour of the drop time | Pull without nagging; anchor stability |
| Tomorrow chosen: share of sessions ending with a pick | Anticipation |
| Weeks on rhythm (weeks, not days) | Habit |
| Return within 14 days after a gap of 7+ days; median gap length | The return design works |
| Retention at weeks 4, 12, 26 and 52 | The long game |
| Delayed recall: target items correct 7+ days after first meeting them | Learning, not performance |
| Targets that hold in the next 4-weekly recording | Replaces 2.0's "retired in 3 weeks", which could be gamed |
| Huh? taps per minute and taps per 100 words, over 4 weeks | Comprehension and difficulty fit |
| "How much did you follow?" one tap after some episodes, against predicted coverage | Level fit |
| Word-button use per call, over weeks | Dependence shrinking |
| Errors on targets in the next calls, after the form returned in episodes | Whether invisible correction works (0.0) |
| Plan mix and share of each plan's allowance used | Whether the prices and the cost rule hold (14.5) |
| "Worth it" and false-claim rate per language | Quality across languages (Part 13) |
| Notebook fact edits in week 1 | Whether the glass box builds trust |
| Similarity score across each learner's episodes; monthly human read | Sameness |
| Minutes per day: heavy-use outliers flagged | A warning light, never a goal |
| Recognizer error by first language | Fairness of the first link |
| Time to first sound; time to first spoken sentence | The first ten minutes |
| Calls abandoned on the move; feed-to-call handoff | When to switch to native early (Part 19.3) |

---

# PART 17 — OUT OF SCOPE FOR THE BETA

Character creation and the six chassis · learner-made or guest hosts · the news scout and any current-events facts the learner did not supply · the observer in the call · languages that have not passed the gate (Part 13) · native apps · detecting the learner's own language without the word button · settings beyond the Controls sheet · referral programs and community · social sharing of proof clips (a learner may download their own tape) · the learner's cloned voice · real-life rehearsal on demand (the mid-season rehearsal episode is in) · bring-your-own-input episodes · a yearly plan · regional prices · exploration slots in targeting · "where do I stand" for skills not yet calibrated · ask-first glosses · employer and university seats · playback above 1.0× · any chart, percentage or level on any surface.

---

# PART 18 — OPEN ITEMS (COMPLETE LIST)

| # | Item | Needed by | Who decides |
|---|---|---|---|
| 1 | Who writes the host bibles (one duo per target language, Karim and Mona first) and Salma's (one per native language) | Beta build start, 2026-11-18 (drafts for Milestone 0) | Muath |
| 2 | Company and payment provider (a merchant of record is recommended, 0.2) | 2026-12-02 | Muath |
| 3 | Legal review, scoped by the countries the beta invites from: GDPR, PDPL and others, SB 243, EU AI Act, subscription rules | Before 2026-12-23 | Muath with counsel |
| 4 | Confirm the three prices or the rule behind them (14.5) | Before 2026-12-23 | Muath |
| 5 | Which countries the beta invites from (default: wherever waitlist demand is, within what the legal review clears) | 2026-12-02 | Muath |
| 6 | Which target languages open (the language gate, Part 13) | Beta build weeks 1 to 2 | Tests (14.4, 10.14) |
| 7 | Episode voice vendor, streaming and batch recognizers, per language | Beta build weeks 1 to 2 | Tests (14.4, 10.14) |
| 8 | English Grammar Profile commercial-use permission, or another inventory source; native-teacher review of drafted inventories for other targets | Beta build week 2 | Muath (a request to its publisher) |
| 9 | External test choice (default for English: Duolingo English Test) | 2026-12-23 | Muath |
| 10 | Similarity threshold and recognizer confidence threshold | End of Milestone 0 | Data |
| 11 | Private feed support in the podcast apps learners use (some major apps do not accept private feeds) | First beta cohort (Milestone 0 has no feed) | Beta observation |

Settled on 2026-10-23: the trial needs no card; the launch learner, the language pair and the recruitment fallback are gone with decision 1; Salma's Arabic variety is now part of the per-language voice test (7.3).

Everything else in this document is decided. A question during the build that this document does not answer escalates before it is built.

---

# PART 19 — MILESTONE 0 AND THE BUILD SEQUENCE

## 19.1 Milestone 0, hand-made: 2026-10-24 to 2026-11-18

The pilot kit, scripts, protocols and day-by-day schedule live in /mnt/project-files/milestone-0/ (owned by the Milestone 0 thread; dates from 03-schedule.md, re-dated 2026-10-23). Recruiting runs Oct 24 to 28; cohort A starts Sun Nov 1 and cohort B Mon Nov 2; the finales are Nov 14 and 15; blind rating and pre-pay close Nov 17; **the gate decision is Wed Nov 18.** This part only states what the PRD needs from it.

1. **15 learners for 14 days**, recruited by hand through Muath's network. Episodes written with model help and checked by hand; delivered by WhatsApp (no podcast feed in the pilot); calls on ElevenLabs Agents with patient turn-taking (the kit's choice over Gemini Live, so the call voice will not match the episode voice; the day-7 check-in asks whether that matters); Muath tags every call by hand using the planned structure inventory.
2. **The pilot follows the 3.1 decisions where they touch the learner:** no notes that correct, only "you mean..." in the call and the right forms in later episodes. The kit was written before 2026-10-23 and is its own thread's to align.
3. **Day-1 and day-14 recordings** of the then-and-now task (10.9.2).
4. **Personal versus generic:** within each learner, alternate personal days and generic days at the same level and with the same target words.
5. **One blind comparison** against a human-made learner podcast on the same topic.
6. **The sample-episode waitlist opens**, in every language the waitlist asks for, so demand can order the language tests.
7. **The gate:** 10 of 15 ask for the next episode unprompted; median 4+ sessions a week; 4+ minutes of their own speech a session; in week 2 most still choose tomorrow's episode and say the week was worth it; the day-14 recording is better, judged blind, on at least one of accuracy, fluency or complexity for most; personal days beat generic days; 5 of 15 pre-pay.
8. **What the beta inherits from Milestone 0:** the first calibration set (Muath's tags), the 30 recognizer clips for English, test-retest pairs for standard errors, the similarity threshold, the first ban list, and evidence on the call timing. The feed is first tested in the beta (Part 18 item 11).
9. **If the gate fails,** find which claim failed before building: the show is not wanted, the teacher is not felt, or the price is wrong. Revise the thesis, not the backlog.

## 19.2 Beta build: 2026-11-18 to 2026-12-22

| Week | Build |
|---|---|
| 1 (Nov 18) | Vendor tests and the language gate per candidate target (14.4, 10.14, Part 13); event log and learner-model schema; lexicon and scheduler; language package skeleton (target and native split); cost tracing |
| 2 (Nov 25) | Teacher, writer, fitter, editor and voice studio end to end, producing episodes for test learners in each language that passed; gloss cache; the language list for the beta is fixed at the end of this week |
| 3 (Dec 2) | Onboarding with Salma (A1 to A10); the player; the word sheet; the feed; drop notifications; the three plans, checkout and plan changes |
| 4 (Dec 9) | The call pipeline with the word button, hold-to-talk and adaptive patience; "you mean..." recasts; voice-note fallback; chat |
| 5 (Dec 16) | After-session pass, memory keeper, notebook, Controls, simple weekly proof, recording the first then-and-now, data rules, crisis resources per country; the sample-episode landing page in many languages; end-to-end run with Milestone 0 learners |

**Exit criteria for 2026-12-23:** every [P0] item works in every language that opens; a measured cost per session; a costed path to $0.35 or less.

## 19.3 Paid founding beta: 2026-12-23 to 2027-01-26

About 50 invites a week into 7-day trials on the 2 a day plan, spread across the languages that passed; 20 to 30 English learners take the external test at week 0 and week 8. The beta starts over the year-end holidays, so the first week's numbers are read with that in mind, and several Gemini 3.8 prices double on 2027-01-01, inside the beta (cost tracing shows it). [P1] items ship during it: round two, shadowing, the season finale with its then-and-now comparison, the full claim gate, the tape, the offline test suite, the dial-in experiment. **Switch to a native app early** if many calls are abandoned on the move or the feed-to-call handoff loses most learners.

## 19.4 After the beta (direction, not spec)

Public launch worldwide in every language that passed, at the three plans, moving to the floor stack piece by piece with blind tests (months 4 to 6); native apps and paid acquisition after retention holds (months 6 to 9); each new language opens as soon as it passes the gate, and regional prices with a cheaper listen-first plan come once there is data on where learners are (months 9 to 12); employer and university seats and human bridges (year 2).

---

# GLOSSARY

| Term | Meaning |
|---|---|
| Session | One episode and all its doors |
| Door | A part of a session the learner can open: listen, shadow, read, call, chat, round two, small door |
| Active day | A day with at least half an episode played, a call started, or the small door used |
| Drop | Publishing the day's episode to the feed and sending the one notification, at the learner's chosen time |
| Idea | One of tomorrow's three one-line episode proposals |
| Small door | The 90-second recap plus one voice note, for bad days |
| Round two | A short second call on the same argument, shorter and faster |
| Return episode | The first episode after 5+ days away |
| Anchor | The learner's chosen moment for the episode, in life terms |
| Rhythm | The learner's weekly intention with spare days |
| Then-and-now recording | The same 3-minute speaking task every 4 weeks |
| Claim gate | The code that decides whether any statement about progress may be made |
| Working on | The at-most-3 items the teacher is targeting, visible and editable in the notebook |
| Series bible | The learner's world: hosts, side characters, places, jokes, arcs, season, canon |
| Coverage | The expected share of running words the learner understands |
| Plan | 1, 2 or 3 new episodes a day, monthly ($19.99, $29.99, $44.99) |
| Language gate | The five tests a target language must pass to open (Part 13) |
| Word button | Hold and say a word in your own language; the host gives it back in the target language |
| Recast | The host saying the learner's point back the natural way ("you mean..."), never marked as a correction |

---

**Reading rule:** Parts 1 to 17 are settled; build as written. [NEW] tags mark decisions made in this document: veto them now or they stand. Part 18 lists the only open questions. If a question during implementation is answered nowhere here, it escalates before it is built.
