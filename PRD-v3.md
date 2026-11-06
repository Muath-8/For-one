# For one — Product Requirements Document, PRD v3

**PRD v3, 2026-11-06.** Supersedes [PRD-v2.md](PRD-v2.md) (whose internal version numbers were 3.0 of 2026-10-10 and 3.1 of 2026-10-23). PRD-v2.md is kept unchanged so the two can be compared; [PRD.md](PRD.md) (2.0) is history only.

**What this document is.** The single product requirements document that the architecture, technical design, epics and stories, design and engineering documents are built from. Every requirement has a stable identifier so those documents can cite it (`FR-312`, `NFR-104`, `LAW-07`, `GATE-03`, `OPEN-02`). Nothing here is new product thinking: the requirements come from the decisions Muath took on 2026-10-23 ([decisions.md](decisions.md)), concept v2 ([concept-v2.md](concept-v2.md)), the agreed feature map ([features/for-one-features.html](features/for-one-features.html)), the eleven lens documents ([perspectives/](perspectives/)) and the Milestone 0 kit ([milestone-0/](milestone-0/)). Where PRD-v2 had to make a call that none of those sources made, that call is carried over here and still marked **[PRD call]**: veto it or it stands.

**Sources of truth, in order.** When two sources disagree: decisions.md, then concept v2, then the feature map, then the lens documents and the Milestone 0 kit. This PRD follows that order and says so where it mattered (Part 0.2).

## How to read a requirement

```
FR-312  [P0] [D3]   The host never says "wrong", "mistake" or "the correct answer" ...
│       │    │
│       │    └─ source: D1..D5 decided/agreed by Muath; S = settled point every lens agreed on;
│       │       C = concept v2; L = a lens document; M0 = Milestone 0 kit; [PRD call] = this PRD's own call
│       └────── priority: P0 = works on day one of the paid beta (2026-12-23);
│               P1 = works before the beta gate review (2027-01-26); LATER = direction only, not built in the beta
└────────────── identifier, stable from this version on. Numbers are grouped by area (FR-1xx onboarding, FR-2xx daily loop ...).
                Gaps in numbering are deliberate; new requirements take the next free number in their area and are never renumbered.
```

- **FR** = functional requirement (what the product does). **NFR** = non-functional requirement (how well: latency, reliability, security, cost, quality, accessibility). **LAW** = one of the twelve product laws; a feature that breaks one does not ship. **TC** = one of the eight trust-contract promises. **GATE** = a success metric with a target and a stop line. **OPEN** = genuinely undecided; Part 15 lists every one, with its working default where the build cannot wait.
- A requirement with no priority tag inside Parts 2 to 12 is **[P0]**.
- "Target language" is the language the learner is learning; "own language" (or "native language") is the language the interface and the producer speak to them. "English" and "Arabic" appear only in examples.

---

# PART 0 — WHAT CHANGED, AND WHAT IS STILL OPEN

## 0.1 The five decisions this PRD is built on (Muath, 2026-10-23)

| # | Decision | What it fixes in this PRD |
|---|---|---|
| **D1** | **No single target country or people.** Languages open per the five-check language gate (concept v2 §8); the pilot is English only. | FR-11xx language packages; FR-101 to FR-106 onboarding in any native language; no requirement anywhere is tuned to one market. |
| **D2** | **Monthly subscription only.** Three plans that differ only in new episodes a day: 1 a day $19.99, 2 a day $29.99 (recommended), 3 a day $44.99. Cost per session sets price and allowance. Pricing psychology used to push people to subscribe, honestly. | FR-12xx billing; FR-206 to FR-209 allowance; NFR-4xx cost; GATE-10, GATE-11. |
| **D3** | **Teaching is invisible.** No "wrong, the correct answer is X", no pop-ups. Corrections come inside the conversation as recasts ("you mean..."). The producer, Salma, never corrects. | LAW-07; FR-33x call move contract; FR-36x chat; FR-83x correction layers; the editor's law scan FR-420. |
| **D4** | **Evidence instead of tests.** Recall in conversation, a 60-second word check, a then-and-now recording every 4 weeks, a notebook the learner can open. Still no points, streaks or levels. | LAW-01, LAW-12; FR-8xx assessment and claim gate; FR-9xx weekly proof; FR-10xx notebook. |
| **D5** | **A continuing series.** Plot may persist, obligation never; 4-week seasons with one real goal; missing a day never costs anything. | LAW-04; FR-55x arcs and seasons; FR-210 to FR-214 after a gap; FR-224 rhythm never shown as a counter. |

The six settled points (what counts as learned, fun carries the language, audio-first transcript, light pronunciation, the first ten minutes, what counts as success) are adopted as in decisions.md and tagged **[S]**. Decisions 6 to 10 (the daily cue, platform, personalization depth, data use, how the beta earns) run on decisions.md's recommendations and are tagged **[C]**; where one of them is still open for Muath it is also an OPEN item.

## 0.2 What changed from PRD-v2 (3.1)

PRD-v2 3.1 had already folded in the 2026-10-23 decisions. This version keeps its substance and changes the following. The full map from PRD-v2 sections to requirement IDs is in Appendix A; the list of requirement IDs whose substance differs from PRD-v2 is in Appendix B.

| # | Change | Why | Where |
|---|---|---|---|
| 1 | Every rule is now a numbered requirement with a priority and a source tag. | Six documents are being written from this one in parallel; they need stable references. | Whole document |
| 2 | **Web versus native for the beta is reopened as OPEN-01.** PRD-v2 decided "installable web app plus private podcast feed". That was decisions.md's recommendation for decision 7, which Muath has not answered. The web app plus feed stays as the **working default** so the build can start; every requirement that depends on it is tagged `[OPEN-01]`. | Project memory and the UI lens list it as still open for Muath. | FR-130, FR-23x, FR-31x, NFR-1xx |
| 3 | **The first-session order is reopened as OPEN-02.** The A1 to A10 flow and the suggested door order (Listen, Read, Call, Chat) stay as the working default. | Same reason: the UI lens left it open; nobody has decided it. | FR-110 to FR-121, FR-302 |
| 4 | **Who writes the hosts and Salma is OPEN-03**, as before, now with the consequence stated: no language can open in the beta without finished bibles, and Milestone 0 runs on drafts. | Due before the build starts on 2026-11-18. | FR-501, FR-520, OPEN-03 |
| 5 | **Milestone 0 is English only.** PRD-v2 allowed "English plus any language with a native-speaker helper". The kit recommends English only and the coordinator's brief confirms it. | D1 as applied to the pilot. | FR-1110, Part 16 |
| 6 | Three editorial errors in PRD-v2 are fixed: a stray "Salma" row inside the measures table (10.3), a malformed "Host" row in the agent roster (14.1), and "English throughout" in the episode spec (5.1), which now reads "the target language throughout". | They contradicted D1 and D3 as written. | FR-301, FR-810, Part 13 |
| 7 | **Status as of 2026-11-06:** Milestone 0 is running (cohort A on day 6, cohort B on day 5 by the kit's schedule); the gate decision is Wed 2026-11-18. The beta build (2026-11-18 to 2026-12-22) and paid beta (2026-12-23 to 2027-01-26) dates are unchanged and depend on the gate passing. | Dates follow the pilot kit. | Part 16 |
| 8 | The agents-and-stack part is cut to what the product requires (roles, what is code and what is a model, vendor tests). Vendor choices, costs per role and infrastructure now live in the architecture documents and are referenced, not repeated. | The architecture thread owns them; two copies drift. | Part 13, NFR-4xx |

Everything else is PRD-v2's content, re-stated as requirements. The **[PRD call]** decisions PRD-v2 made (its "[NEW]" tags) are carried over with that tag; they remain vetoable.

## 0.3 What only Muath can settle, and by when

| ID | Question | Working default until answered | Needed by |
|---|---|---|---|
| OPEN-01 | Web app plus private podcast feed, or a native app, for the beta | Installable web app plus feed (decision 7 recommendation) | 2026-11-18 (build start), because it decides the client work in build weeks 3 and 4 |
| OPEN-02 | The first-session order (A1 to A10) and the suggested door order | As specified in FR-110 to FR-121 and FR-302 | 2026-12-02 (build week 3, onboarding) |
| OPEN-03 | Who writes the host bibles (one duo per target language) and Salma's (one per native language) | Milestone 0 drafts | 2026-11-18 |
| OPEN-04 | Company and payment provider (a merchant of record is recommended) | None; checkout cannot be built without it | 2026-12-02 |
| OPEN-05 | Legal review scoped by the countries the beta invites from | None | Before 2026-12-23 |
| OPEN-06 | Confirm the three prices, or change the cost rule behind them | $19.99 / $29.99 / $44.99 | Before 2026-12-23 |
| OPEN-07 | Which countries the beta invites from | Wherever waitlist demand is, within what the legal review clears | 2026-12-02 |

The complete open list, including the items that tests rather than Muath decide, is Part 15.

---

# PART 1 — PRODUCT, LAWS, TRUST, SCOPE

## 1.1 What the product is

**For one is a private teacher who makes one learner a daily show.** One account is one show. A show is a short podcast episode made for, about and with one learner, followed by a live call with its host, an article that arms the learner for that call, and a short chat. The teacher behind it plans every episode from what the learner did yesterday, brings the right forms of the learner's own mistakes back inside the next episodes and calls, and proves progress in the learner's own voice every four weeks. Nothing is graded on screen, nobody is told they are wrong, and no game mechanic exists anywhere.

The learner meets three voices and nothing else: **the hosts** (the show, in the target language), **Salma, the producer** (the face of the app, in the learner's own language), and **themselves**. The teacher never speaks; it decides what the hosts say and what Salma shows. **[D3]**

### The eleven system parts

| # | Part | Specified in |
|---|---|---|
| 1 | Learner model: nine stores computed from an append-only event log | FR-6xx |
| 2 | Series bible: the learner's world, hosts, side characters, arcs, season | FR-54x, FR-55x |
| 3 | Teacher (planner): targets, arcs, seasons, tomorrow's ideas, each episode's brief | FR-7xx |
| 4 | Production pipeline: writer, fitter, editor, voice studio | FR-4xx |
| 5 | Session engine: one episode and its doors | FR-3xx |
| 6 | Live call: a host in a voice pipeline, with the word button | FR-32x to FR-34x |
| 7 | Producer, Salma: onboarding, notebook, the weekly proof's voice; never corrects | FR-52x |
| 8 | Assessment engine and claim gate | FR-8xx |
| 9 | Weekly proof and season finale | FR-9xx |
| 10 | Delivery: client, drop, feed, notifications | FR-23x, FR-130 [OPEN-01] |
| 11 | Billing and cost tracing | FR-12xx, NFR-4xx |

## 1.2 The twelve laws

A feature that breaks a law does not ship. The editor's law scan (FR-420) and a design review checklist enforce them on every surface: app, audio, chat, email, feed notes.

| ID | Law | What it means for the build | Source |
|---|---|---|---|
| **LAW-01** | **No game furniture.** No streaks, points, badges, levels on screen, percentages, leaderboards, charts or confetti. | Counts that only grow (hours heard, words owned) are allowed as plain text; nothing fills, resets or targets a number. | D4 |
| **LAW-02** | **Every moment has a hidden shape and a social surface.** | Every door has a pedagogical brief (targets, due words) and a social form (podcast, call, article, chat). | C |
| **LAW-03** | **The learner owns topic, format and cast; the teacher owns pedagogy and shows its reasons on request.** | "Why this episode" and the editable "working on" list; vetoes and additions change targeting the same day (FR-706). | C |
| **LAW-04** | **Every episode is complete. Plot may persist; obligation never.** The story waits for the learner. | Arcs never advance while the learner is away; no episode requires an earlier one (editor check FR-419). Missing a day costs nothing, anywhere. | D5 |
| **LAW-05** | **Honesty about what it is.** Transparently AI; no guilt, no "I miss you", no fake lives. | AI disclosure (FR-560), the line between in-show fiction and fake lives (FR-561), the crisis protocol (FR-57x). | C |
| **LAW-06** | **Formats are hijacked, not invented.** Podcast, call-in, group chat, a producer's notebook. | Milestone 0 runs on WhatsApp and a podcast feed; the beta keeps the feed [OPEN-01]. | C |
| **LAW-07** | **Correction is invisible.** It lives inside the conversation and in the next episodes, never in a verdict. Hosts ask for clarification when meaning is lost and say the learner's point back the natural way ("you mean you *went* there?"). Nobody says "wrong", shows a right answer, grades, interrupts a learner mid-sentence or praises the person. | The host move contract (FR-33x), nothing after the call (FR-350), the correction layers (FR-83x). No surface ever shows a learner's sentence next to a corrected one, a red mark or a correction pop-up. | D3 |
| **LAW-08** | **Conversations end like conversations.** Clean goodbyes, never homework. | Call and chat closers; real-world tries are offered, never assigned. | C |
| **LAW-09** | **The show is the gym; life is the game.** Real-world tries are offered and celebrated above everything else. | "Out in the world" log (FR-1015); real-life arcs and the mid-season rehearsal (FR-553). | C |
| **LAW-10** | **The text is used once; the language comes back.** | Every episode is new text; targets return on a spaced schedule (FR-72x). | C |
| **LAW-11** | **A finite, good portion.** A fixed number of new episodes a day, set by the plan (1, 2 or 3), each with a clear ending; no autoplay, no feed of content. What is already made can be heard as often as wanted. | The allowance (FR-206 to FR-209). No "next episode" control exists anywhere. | D2, C |
| **LAW-12** | **No claim without proof.** Every statement about the learner's progress passes the claim gate: like for like, beyond the noise, repeated, from clean evidence, openable. | The claim gate (FR-840) is the only route from the learner model to anything the learner hears or reads about their progress. | D4 |

## 1.3 The trust contract

Eight promises, shown in plain words at onboarding and in Controls.

| ID | Promise | Enforced by |
|---|---|---|
| **TC-1** | **Never lie.** No memory is stated unless confirmed; no progress claim without proof. | FR-620 to FR-626, FR-840 |
| **TC-2** | **Never manipulate.** No guilt, no engagement tricks, no dark patterns, no "don't go" goodbyes. | FR-240, FR-1230 to FR-1233, FR-1022 |
| **TC-3** | **Never hide what it is.** The hosts and Salma are AI, said at the start and whenever asked. | FR-560 |
| **TC-4** | **Prove progress honestly,** including flat weeks. | FR-905 to FR-907 |
| **TC-5** | **The data is theirs.** See it, export it, delete it. | FR-1040 to FR-1048 |
| **TC-6** | **Told, not inferred.** The show uses only what the learner said to it. Nothing is looked up about the person outside the app; nothing is guessed about health, money, relationships, religion or politics. | FR-620 to FR-623, FR-417 |
| **TC-7** | **A wrong memory is a bug.** Fixed at once when the learner says so, and counted as a quality metric. | FR-626, GATE-13 |
| **TC-8** | **Data use is opt-in.** Anonymized transcripts are used to check and improve the teacher only with consent, off by default. | FR-1044 |

## 1.4 Scope

| ID | Item | Requirement | Source |
|---|---|---|---|
| **FR-001** | Learner | Any adult (18 or older) who already understands some of the target language and wants to speak it, from about A2 to C1. No launch country or people is singled out, and no requirement may be tuned to one culture or market. The design centre is still the learner who understands a lot and freezes when speaking. | D1 |
| **FR-002** | Languages | As many target languages as the speech stack supports, decided by the language gate (FR-1101), never by a market list. Any shipped native language pairs with any shipped target language. Accents per target as the voice pools allow (English: British and American). | D1 |
| **FR-003** | Age | 18+. A checkbox on the first screen; birth date at account creation; under-18 dates are refused with a plain message. | C |
| **FR-004** | Access | Invite-only from the waitlist during the beta (FR-106). | PRD call |
| **FR-005** | Plans | Monthly only. Three plans that differ only in new episodes per active day: 1 a day $19.99, 2 a day $29.99 (marked "Recommended"), 3 a day $44.99. No yearly plan, no free tier, no ads, no credits, no lifetime deals. One USD price list at launch. Prices: OPEN-06. | D2 |
| **FR-006** | Unlimited on every plan | Re-listening, the archive, the feed, the article, the chat, the small door, shadowing and one round-two call per episode cost no allowance. | D2, C |
| **FR-007** | Free taste | A 90-second sample episode before signup (FR-101), then a 7-day trial after onboarding, on the 2 a day plan, with no card (FR-1201). | C, D2 |
| **FR-008** | Messages | Exactly three kinds of message ever leave the product (FR-240). | C |
| **FR-009** | Platform | **Working default [OPEN-01]:** an installable web app (mobile Safari and Chrome, installable to the home screen) plus a private podcast feed per learner. Native apps after the beta gates. If OPEN-01 is answered "native", the requirements tagged [OPEN-01] change and nothing else does. | C (decision 7 recommendation) |
| **FR-010** | Interface language | The interface, Salma, captions and glosses are in the learner's own language (right to left where that language is written right to left); episodes, articles and host chat are in the target language; every text block sets its own direction from its content. | D1, C |
| **FR-011** | AI cost | Budget about $0.60 per session in the beta; scale target $0.30 to $0.35; stop line $1.00 with no plan to reduce it. Cost tracing on every model, voice and recognition call from the first learner (NFR-401 to NFR-405). | C |

---

# PART 2 — ACQUISITION AND ONBOARDING (FR-1xx)

## 2.1 Sample episode and waitlist

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-101** | P0 | A public landing page in the visitor's language (from the browser, with a language picker), one sentence of promise and one action: "Hear your own show." | C |
| **FR-102** | P0 | The visitor picks the language they want to speak (only shipped targets are offered), then answers three questions by text or voice: what the hosts should call them, something they could talk about for an hour, what they do. | C |
| **FR-103** | P0 | The hosts make a **90-second sample episode** about that topic, using the name once, playable within 30 seconds (streamed). Cost ceiling $0.05 per sample. Limit: one per device and per phone number or email per 24 hours. | C; limits: PRD call |
| **FR-104** | P0 | The sample ends with Salma, in the visitor's own language: the full show is a new episode like this every day, plus a call with the hosts. | C |
| **FR-105** | P0 | Waitlist form: name, WhatsApp number or email, native language, why this language (job, studies, travel, family, other), self-rated speaking from three plain statements, country. The sample is the learner's to keep and forward; nothing is shared automatically. | C |
| **FR-106** | P0 | Invites go out in batches of about 50 a week from 2026-12-23, filtered only for a shipped language pair, a country the legal review cleared (OPEN-05, OPEN-07) and about A2 or above. Each batch is spread across language pairs so every pair gets enough learners to calibrate. Each invite carries the waitlist answers into onboarding so Salma does not ask them again. | D1; carry-over: PRD call |

## 2.2 The first ten minutes [OPEN-02: order is the working default]

Example learner throughout: Faisal, 27, a sales engineer, supports a football club, has a job interview in six weeks. He is an example only; nothing depends on his country or languages.

| ID | Pri | Step | Requirement | Limits | Source |
|---|---|---|---|---|---|
| **FR-110** | P0 | A1 Open | One screen in the learner's own language: "Your own show, in English." One Start button and an "I'm 18 or older" checkbox. Native and target language come from the invite (or the browser), each changeable with one tap. | Nothing else on the screen. | S |
| **FR-111** | P0 | A2 Mic primer | "Salma, your producer, will talk with you for 3 minutes. You can talk or type." Buttons: Talk (asks for the microphone only now) / Type. | | S |
| **FR-112** | P0 | A3 Salma | **Salma's voice, in the learner's own language, within 60 seconds of opening.** Her first lines say she is the AI producer of their show. Three questions: what should the hosts call you (said aloud, so the hosts learn the pronunciation); what could you talk about for an hour; what do you need the language for. Each fact appears as a card under her as she hears it, with ✎ to correct and ✕ to remove. Twice she switches to the target language for one line: once a comprehension line ("tell me what you heard, in any language"), once a production invitation ("say anything back in English"). A dated event ("interview in six weeks") becomes a follow-up with a date. | About 3 minutes, at most 8 Salma turns. A field not filled after one re-ask is skipped and marked sparse; the intake never stalls. Voice or text per message. | S, D3 |
| **FR-113** | P0 | A4 Word check (optional) | "Want to help me pitch your show at the right level? 60 seconds: tap the words you know." Spec FR-850. "Skip" is as large as "Start". | 48 items, stops at 75 seconds. | D4 |
| **FR-114** | P0 | A5 Casting | While the pilot episode is made: each host says hello (5 seconds); "swap" plays another voice from that host's pool; accent choice where the target has more than one, each with a short sample. | Lasts as long as pilot generation, 40 to 90 seconds; skipped if the pilot is ready. | C |
| **FR-115** | P0 | A6 The pilot | A **2 to 3 minute episode** about the hour-long topic, the learner's name used once. The transcript is shown on the pilot (first contact); one gentle hint points at "Huh?" and at tapping a word. | Playback starts within 45 seconds of the end of A3 (A4 time excluded). | S; timing: PRD call |
| **FR-116** | P0 | A7 First call | A host throws a question the learner can answer in one or two sentences. Before it rings, the other host says once, slowly, captioned in the learner's language: "If a word won't come, hold the word button and say it in your own language." | **60 to 90 seconds.** In this call the host makes no recasts; it clarifies only if meaning is lost. | S; no-recast rule: PRD call |
| **FR-117** | P0 | A8 One thing managed | In the call's goodbye, the host names one real thing the learner did that is not easy ("you used *should have*"). Nothing about what went wrong. Then one line on screen: "Every day: a new episode and a call." | | D3 |
| **FR-118** | P0 | A9 Keep your show | Account (Apple, Google, or email one-time code) and birth date. **Drop time in life terms**: "On my commute (7:40)", "Lunch break", "Evening walk", "Pick a time", each with an adjustable clock time. **Voice-storage consent** right after the learner heard themselves: one checkbox, "Keep my recordings so I can hear my progress (only for you, delete any time)", and one plain sentence: "If you don't, we still listen to each call for a few minutes to plan your next episodes, then delete the audio." | The 7-day trial starts here, on the 2 a day plan, with no card. | S, C (decision 9a); code instead of password: PRD call |
| **FR-119** | P0 | A10 Tomorrow | Three ideas for tomorrow's episode, written from the intake, plus "Tell Salma an idea". The learner picks one. "Tomorrow at 7:40." Then a one-time setup card: add the app to the home screen (for the drop notification) and add the show to a podcast app ("copy feed link" plus instructions for three common apps) [OPEN-01]. | The pilot counts as day 1's episode. | C |
| **FR-120** | P0 | Targets | Measured from the first open: first sound under 60 seconds; the learner's first spoken target-language sentence under 5 minutes; account only after the first call (NFR-101, NFR-102). | | S |
| **FR-121** | P0 | Starting estimate | The two target-language moments, the word check (if taken) and the first call produce a first estimate per skill (listening, reading, speaking, writing) with a wide range (FR-845). The first three episodes are pitched one step easy (FR-731) and treated as calibration. | | C |

## 2.3 Day 2 and week 1

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-125** | P0 | The day-2 episode carries at least one callback sourced verbatim from something said in onboarding. The teacher puts it in the brief; the editor checks it. | PRD 2.0, kept |
| **FR-126** | P0 | Week 1 asks at most one personal question per session, the way a host or Salma naturally would, in this order, skipping any already known: (1) session 2, end of chat: the weekly rhythm (FR-223); (2) session 2, after the call: the first then-and-now recording, offered as "the opening tape of your season" (FR-851), skippable and offered again once in sessions 3 to 5; (3) session 2 or 3: the season goal (FR-556), proposed by Salma from the intake in the learner's words; (4) session 3 or the first weekly proof: the optional note to the learner's future self (FR-211); (5) across the first two weeks, from the hosts: people in their life, past attempts at the language, more interests, more dated events, each a candidate fact (FR-620). | C; order: PRD call |

---

# PART 3 — THE DAILY LOOP (FR-2xx)

## 3.1 Choosing tomorrow

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-201** | P0 | Tomorrow's choice appears at the close of whichever door the learner uses last today (usually the chat), and on the Today screen once the session is done. | C (decision 6) |
| **FR-202** | P0 | **Three ideas**, each one line of at most 140 characters, carrying topic, format and cast ("Mona interviews you for the job, and she is not nice."), plus **"Tell Salma an idea"**: the learner types or says what they want; Salma confirms it in one line and it becomes the pick. | C |
| **FR-203** | P0 | Composition, enforced by the teacher: at least one idea from the learner's own life if a follow-up is due, an arc is open or a life situation is active; exactly one wildcard outside the learner's usual lanes, from an adjacent interest; at most one idea continues an open arc; no format that already ran twice in a row; current events only from what the learner told the show (the beta has no news scout, so no idea asserts a real-world fact the learner did not supply). | C; no-scout rule: PRD call |
| **FR-204** | P0 | The ideas for day N+1 are written in the plan made the night before day N. Pedagogy is threaded into the chosen idea afterwards from today's evidence; pedagogy adapts to the topic, never the reverse. If today's session brought a life update that changes an idea (the interview moved), the teacher rewrites that idea before showing it. | C; rewrite rule: PRD call |
| **FR-205** | P0 | **Cutoff:** if nothing is chosen by 6 hours before the drop time, the teacher's top-ranked idea is used. **Remix:** long-press an idea to change topic, format or cast before choosing; the result is the pick. | PRD call |

## 3.2 The allowance

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-206** | P0 | **New episodes per active day, by plan: 1, 2 or 3.** An active day is a local calendar day on which the learner played at least half an episode, started a call or used the small door. The day's first episode is made overnight and drops at the chosen time. On the 2 and 3 a day plans, the next episode is made on demand from tonight's other ideas when the learner finishes (or skips past) the current one's listen door, and plays within 30 seconds (streamed). Nothing extra is made in advance, so unused allowance costs nothing. Unused allowance never carries over and is never mentioned. | D2; active-day definition: PRD call |
| **FR-207** | P0 | **No episode is made after an inactive day.** If yesterday's episode is unplayed, it stays as today's hero; no new one is generated and no drop notification fires. There is only ever one unplayed episode waiting, on every plan. | PRD call (caps cost; a skipped day leaves no pile and no reminder) |
| **FR-208** | P0 | **One swap a day.** "Not this one" on a dropped, unstarted episode makes the second-ranked idea on demand (playable within 30 seconds, streamed). | PRD call |
| **FR-209** | P0 | When a learner reaches the plan's number for the day, Today says plainly, in text: "That's today's new episodes. Tomorrow's will be ready at 7:40." Never in character as an excuse, never with a button. **The plan, mentioned honestly:** if a learner reaches the limit on 3 or more days in a week, that week's proof ends with one plain line naming the next plan and its price, once; changing plan lives in Controls, never on Today. A learner who uses less than half the allowance for 4 weeks hears, once, that a smaller plan exists. | D2 (pricing psychology within TC-2) |

## 3.3 After a gap, the small door, rhythm

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-210** | P0 | **The small door.** Every episode ships with a 90-second recap by the hosts, made in the same pipeline run, ending with one question. On a bad day the learner opens it from Today: the recap plays, then the learner records one voice note back (up to 60 seconds); the host answers with one short text in the chat thread. A small-door day is an active day and counts fully toward the rhythm; the episode's other doors stay open. | C; host text reply: PRD call |
| **FR-211** | P0 | **Gap note (opt-in).** Offered once in week 1: the learner writes a short note to their future self and chooses a gap length (7, 10 or 14 days; default 10). If that many days pass with no session, the note is sent once, by email and web push, in their own words, signed by no host. Then nothing more. Editable or off in Controls. | C (decision 6); week-1 timing: PRD call |
| **FR-212** | P0 | **Return episode.** After 5 or more days with no session, the next episode is a return episode: one step easier (FR-731), it opens from something in the learner's life, it never mentions the days missed, and it includes one quick real win from gated evidence. If an unplayed episode was made before the gap, it is replaced by the return episode when the learner next opens the app or plays the feed, generated then (playable within 30 seconds, streamed). | C, D5; 5 days and replacement: PRD call |
| **FR-213** | P0 | Near a natural landmark (a Monday, the first of a month, a new season) the return episode may offer a fresh start ("new month, new goal?"). Never more than that. | C |
| **FR-214** | P0 | Returning after a gap, the Today screen looks exactly like any other day. Nothing anywhere records, counts or shows missed days. | D5 |
| **FR-220** | P0 | **The anchor** is the drop time chosen in onboarding, stated in life terms ("after I sit down on the 7:40 bus"), with an optional backup slot. | C |
| **FR-223** | P0 | **The rhythm** is a weekly intention with spare days: the learner picks 3 to 6 days a week plus 2 spare days, set in session 2. | C; range: PRD call |
| **FR-224** | P0 | The rhythm is never shown as a counter, calendar, flame or record of missed days. The weekly proof mentions it in words only when it was met ("four times this week, as you planned"); when it was not met, the proof says nothing about the count and talks about what has built up. | D4, D5; not-met rule: PRD call |
| **FR-225** | P0 | **Re-anchoring.** Salma asks once for a new anchor when the learner mentions a move, a new job or a trip, or when no session happened within 3 hours of the anchor for two weeks running. | PRD call |

## 3.4 Making and dropping the episode

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-230** | P0 | When the pick is made (or at the cutoff), the teacher writes the brief and the pipeline runs (FR-401) on batch pricing. If the batch job has not finished 90 minutes before the drop time, the remaining steps run on standard on-demand pricing. The episode, article, call brief, chat opener, small-door recap, shadow lines and feed version are all ready before the drop time. | C; 90-minute fallback: PRD call |
| **FR-231** | P0 | The episode is visible in the app as soon as it is ready. The drop time controls the notification and the feed, not access. | C |
| **FR-232** | P0 | At the drop time the episode is published to the learner's private feed [OPEN-01] and **one** notification fires (web push if the app is installed and notifications are allowed). The podcast app's own new-episode alert is the second route. Notification text: the episode title and length, nothing else ("Karim vs Mona: the interview (6 min)"). No urgency, no host voice, no count. | C (decision 6) |
| **FR-233** | P0 | **The feed version** [OPEN-01]: the same episode plus a 5-second tag from the host at the end ("To call me, open the link in the notes"); the feed item's notes carry the call link and the article link. Feed URLs carry an unguessable token, are excluded from podcast directories and can be reset (NFR-305). | PRD call |

## 3.5 The Today screen

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-235** | P0 | One hero episode, big, with a typographic cover (title, hosts' marks, the show's colour), length and what it includes. One line from a host above it, always a real, confirmed memory. "Why this episode?" under it. No list of pitches: the other ideas live only in tomorrow's choice. | C |
| **FR-236** | P0 | Hero states: **ready, not started** = cover and ▶ Play; **in progress** = the cover with doors Listen ✓ · Call · Read · Chat (doors, not a progress bar); **done for today** = "That's today's show", tomorrow's drop time and the one-line teaser of the pick, plus "Round two with Mona, any time" when available, nothing else; **weekly proof day** = the proof sits above today's episode with its own cover; **returning after a gap** = exactly like any other day. | C, LAW-01 |
| **FR-237** | P0 | Three tabs only: **Today**, **Show** (the archive, FR-1001), **Notebook** (FR-1010). Controls open from the notebook. | C |

## 3.6 Every message that leaves the product

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-240** | P0 | Exactly three kinds of message ever leave the product: (1) the **drop notification**, at the drop time, only when a new episode dropped, by web push and the feed's own alert, can be turned off; (2) the **gap note**, once, after the chosen gap, by email and web push, opt-in only; (3) **transactional** email: sign-in code, receipts, trial ending (day 6, one plain email), payment failed, export ready, account deleted. Nothing else is ever sent: no re-engagement, no "your hosts miss you", no streak warnings, no marketing email to learners in the beta. | C (decision 6), TC-2 |

---

# PART 4 — THE SESSION AND ITS DOORS (FR-3xx)

A **session** is one episode and everything attached to it. Each part the learner can open is a **door**: Listen (FR-31x), Shadow (FR-318), Read (FR-319), Call (FR-32x to FR-34x), Chat (FR-36x), Round two (FR-345), Small door (FR-210).

## 4.1 State machine

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-301** | P0 | Door states: `not_started`, `in_progress(position)`, `done`, `skipped`. Session states: `ready`, `open`, `done`, `closed`. | C |
| **FR-302** | P0 | **Any order** [OPEN-02 for the suggested order]. Every door can be opened at any time once the episode exists, except: Chat opens after Listen, Read or Call has been used; Round two opens after the main call is done. **Working default path:** the episode's ending throws to the learner and the screen offers **Call** now, **Read the article** first, or **Later**; Read-before-Call is suggested because the article is planning time. In Ears mode (screen off), pressing play on the headphones after the throw does nothing; the call needs the screen in the beta [OPEN-01]. | C |
| **FR-303** | P0 | **Planning time when the article is skipped.** Listen straight to Call shows a 30-second planning card first: "Think about your side. Three words you might want:" with three words from the brief and a "Ready" button. Skippable. | C; card form: PRD call |
| **FR-304** | P0 | **Pause and resume.** Audio position, article scroll and chat history persist indefinitely. A call cannot resume mid-call: an interrupted call restarts as a fresh call whose first line acknowledges the gap ("You left me hanging. Where were we?"). | C |
| **FR-305** | P0 | **Skips are allowed and logged** as energy and taste signals. Nothing punishes a skip; the host naturally refers to the article in the call, which is the built-in cost of skipping it. | C |
| **FR-306** | P0 | **Re-entry.** Listen and Read remain playable and readable forever (archive). The main call happens once; round two once. | C |
| **FR-307** | P0 | **Closing.** A session closes when the learner's next episode is published. Its partial evidence still feeds assessment. An unstarted session never closes on its own (FR-207). **One session open at a time:** starting the next episode while the current one has unused doors needs no confirmation; the old one closes, nothing is lost, and it stays in the archive. | PRD call (replaces 2.0's 48-hour abandonment rule) |

## 4.2 Listen: the episode

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-310** | P0 | **Length:** target 5 to 7 minutes; hard bounds 4:00 and 8:00. The teacher shortens it on low-energy signals (FR-731). | C |
| **FR-311** | P0 | **Structure:** (1) a cold open of at most 30 seconds in which the hosts use two or three of yesterday's new words in new lines, then one asks how the learner would say the episode's key idea, leaves a 3-second pause (nothing is recorded), and the episode then uses the natural phrasing; (2) two to four scenes with a natural pause point between them; (3) personal moments carry the language: target and due words sit inside the jokes, callbacks and personal moments, never in filler; (4) **the throw**: the episode ends on an unresolved question pitched at about 50% certainty, which plants the two or three phrases the learner will need in the call, then throws to the learner by name. Mandatory in every episode. | C; pause rule: PRD call |
| **FR-312** | P0 | **Cast:** exactly the chosen cast, one host or both. **Personal references:** interests lead; at most two life facts per episode, only confirmed facts the learner told the show (FR-621), sensitive topics only if the learner raised them that week. | C (decision 8); "that week": PRD call |
| **FR-313** | P0 | **Speech:** the target language throughout, at the learner's listening edge (FR-730). Speaking rate is a generation setting per learner, between 85% and 100% of the voice's natural rate. | C; range: PRD call |
| **FR-314** | P0 | **The player:** play/pause and scrub; **⟲ line** replays the last sentence (not 10 seconds); **Huh?** jumps back one sentence, replays it at 0.85× and shows that sentence with glosses under its hardest words, every Huh? logged with the sentence and its words; **speed** 0.75×, 0.85×, 1.0×, never above 1.0×; **transcript** as word-synced karaoke text, folded on the first play when the listening estimate is about B1 or above and open for lower, one tap opens it, the teacher may change the default per learner, always open on replays if the learner opened it before; **tap a word** opens the word sheet (FR-370) when the transcript is open. | S (audio-first) |
| **FR-315** | P0 | **Lock screen and headphones** [OPEN-01]: through the Media Session API where the browser supports it: play/pause; previous track replays the last sentence; next track marks the moment (saved to the notebook with its sentence and audio). Never overrides a system gesture. | C |
| **FR-316** | P0 | **Logged:** play, pause, position, speed, replays, Huh? (sentence), transcript open/close, taps, marks, completion. | C |
| **FR-318** | P1 | **Shadow: say it with the host.** Offered after the episode as one optional line ("Say two lines with Karim?"). Two short lines from the episode that contain targets or due words; for each, the host's audio plays, the learner records the line, the learner can play both back. Nothing is shown about how it went; internally pronunciation is scored on the known sentence (FR-812) and the recording is an elicited-imitation signal. | S (light pronunciation) |

## 4.3 Read: the article

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-319** | P0 | **Length by reading estimate:** 150 to 300 words at A2, 250 to 450 at B1 and B2, 350 to 600 at C1 and above. **Content contract:** it must add at least one of a counterargument, a fact the hosts missed, or a reason to change sides; never a recap; the writer is told to arm the reader against the script. A one-line header from the host: "This is what I'll throw at you on the call." It carries the session's targets and due words at known-word coverage of at least 98% (FR-410). **▶ Read it to me**: the article read aloud by one host voice, synced. Every word is tappable (FR-370); long-press a sentence to hear it or keep it. Logged: open time, scroll depth, time per section, read-aloud use, taps, keeps. | C; lengths kept from PRD 2.0 |

## 4.4 Call: the live call

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-320** | P0 | **Entry:** one tap from the throw, from Today, or from the feed link [OPEN-01]. The call screen keeps the screen awake (Screen Wake Lock). Earphones are suggested once, on the first call. | C |
| **FR-321** | P0 | **Length:** target 5 to 7 minutes. The host begins a natural close at 6:30 and ends by 8:00 with an in-character sign-off. The learner can end at any moment with ✕; the host closes like a person ("Fine, but this isn't over."). | C; 6:30 and 8:00: PRD call |
| **FR-322** | P0 | **Speaking time:** the goal is 4 or more minutes of the learner's own speech per session (call, round two, shadowing and "say it once" combined). The host's share of talk in a call is at most 40%: short host turns, one point at a time. | C; 40%: PRD call |
| **FR-323** | P0 | **Turn-taking:** open mic by default. **Hold to keep the floor:** while the learner holds the large pad, the host waits however long it takes; releasing hands the turn back. **Adaptive patience:** end-of-turn silence starts at 1.5 seconds for a new learner and adapts per learner within 1.0 to 2.5 seconds from their stored pause profile. **Backchannel:** during a pause inside a learner's sentence over 1.2 seconds the host may give one soft backchannel ("mm", "go on") per pause, never words that take the floor. **Silence:** after 8 seconds the host offers a smaller version of the question, never the same question louder; after two such offers it offers to wrap up. **Not understanding the host:** the learner can say "sorry?" or "slower" in either language and the host rephrases more simply; previous-track replays the host's last line. | C; values: PRD call |
| **FR-325** | P0 | **The word button.** The learner holds the word button and says the word or phrase in their own language. That audio goes to a recognizer for the learner's own language, not to the host's recognizer; the host waits and the floor is held. The host gives the word back in the target language inside the conversation ("A *selection*? Of what?") and carries on; the word also appears in a small bubble. Salma is silent in the call: the word comes from the host, so the call has one voice. | D3, C; button rather than switch detection: PRD call |
| **FR-326** | P0 | **Word or hint:** if the learner has never produced the word, the host gives it. If they have produced it before (in the word bank as produced at least once), the host gives a hint first (its first sound, or "you used it on Tuesday, about your manager") and the word on a second press. Word-button use is logged per word; falling use over weeks is progress evidence. | PRD call (reconciles "give the word" with "hints before answers") |
| **FR-330** | P0 | **The host's move contract** applies in every call except the onboarding call (FR-116). **Position:** the host takes a genuine position from the brief and pushes back at least once. **Absorbs** side-switching, rejecting the premise, personal examples, off-topic turns and early endings without steering back to a script. | C |
| **FR-331** | P0 | **Clarification request:** when an error blurs or blocks meaning, a real "sorry, you did what?" first. At most 3 per call. | D3; cap: PRD call |
| **FR-332** | P0 | **Recast ("you mean..."):** the host says the learner's point back the natural way inside a reply that has its own conversational point: a short recast with the changed word stressed ("You *went*? With who?"), or, when the sentence was far off, a full reformulation ("Oh, you mean you *went* there last year?"). Only on the brief's targets or on errors that blur meaning. At most one per learner turn. The recast word is bold in the host's caption. | D3 |
| **FR-333** | P0 | **The host never** says or implies "wrong", "mistake" or "the correct way is"; never grades, explains grammar unasked, mentions progress, interrupts a learner mid-sentence, guilts, or says it will miss the learner. **No self-repair prompts** of any kind (the earlier "Wait, yesterday you...?" nudge is dropped because it tells the learner something was wrong). | D3, LAW-07 |
| **FR-334** | P0 | **Recall gaps:** 2 to 4 per call, moments that make the learner pull a due word or phrase out of memory ("How did you put it on Tuesday? The word that made Mona laugh."). Never scored. | D4 (a) |
| **FR-335** | P0 | **Target necessity:** the brief includes one or two host moves per target that make the structure close to essential ("Walk me through what happened" for past narrative; "If you were the coach..." for conditionals), and one per due word. | C |
| **FR-336** | P0 | **Retell:** once per call: "Mona missed it. Sixty seconds, go." A soft 60-to-90-second ring shows on screen; it never turns red and never cuts the learner off. | C |
| **FR-337** | P0 | **Hints before answers:** the host never completes the learner's sentence. "How do I say X?" gets a hint; the full answer only on a second ask (or through the word button). "What does X mean?" gets a quick plain answer, because comprehension is the point. | C |
| **FR-338** | P0 | **Praise:** at most one specific remark about the task per call, naming something observable ("you just argued for four minutes in the past tense"). Never about the person, never per turn, never "great job". | C |
| **FR-340** | P0 | **Anxiety mode.** When the median learner turn in the first two minutes is under 4 words, or there are two 8-second silences, or the learner's last call was abandoned, the host switches for the rest of the call: at most one recall gap, fewer recasts (targets only), more backchannel, simpler questions. The targets come back in the next episodes instead. | C; thresholds: PRD call |
| **FR-341** | P0 | **Captions.** The host's words are captioned by default (off in Controls); recast words are bold. The learner's own words are never captioned live. No correction interface of any kind exists on the call screen: no red, no ticks, no score. | D3 |
| **FR-342** | P0 | **Failure.** If live voice fails (connection, recognition or synthesis), the screen says "Weak signal. Let's do voice notes." and the same argument continues as asynchronous voice notes in the call thread. The session is never lost. | C |
| **FR-343** | P0 | **Recording.** The streaming transcript drives the conversation. After the call the audio is re-transcribed verbatim (FR-801). If voice storage is on, the audio is kept, encrypted. If it is off, the audio is deleted when the verbatim re-transcription succeeds, and in any case within 15 minutes of the call ending; if re-transcription has not succeeded by then, the call's evidence is kept at low confidence and produces no claims. Transcripts are always stored (disclosed at consent). | C (decision 9a); 15 minutes: PRD call |
| **FR-345** | P1 | **Round two.** After the main call, one short call per episode, available until the session closes: 2 to 3 minutes, the same host and argument, "Give me your take again, shorter and faster." No new episode is needed. It is also a like-for-like retell sample for fluency (FR-811). Suggested on Today the next day if unused. | C |
| **FR-346** | P1 | **Dial-in experiment** [OPEN-01]. A phone number the learner can call for the same call; works with the phone locked and in the car. Phone audio is 8 kHz, so dial-in calls feed planning only at low confidence and never feed claims or the then-and-now recording. | C (decision 7) |

## 4.5 After the call

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-350** | P0 | **Nothing to read.** The goodbye is a goodbye. Today marks the call as done with one honest line: "6:12 call · you spoke 3:40" (information, not a target). No notes, no polish card, no summary of mistakes, from anyone. | D3 |
| **FR-351** | P0 | **Behind the scenes,** the after-session pass (FR-80x) logs what the learner said; the errors that matter most become material for the teacher's next plan (FR-710): the right forms come back, often and audibly, in the next episodes and calls. | D3 |
| **FR-352** | P0 | **Wins are said, not shown.** A first-ever event that passed the claim gate (a structure used correctly for the first time) may be named by a host in the next episode's cold open, at most one per episode. **A word they reached for** (talked around a word they did not have) becomes a planted word in the next episode, used where the learner needed it. | C, LAW-12 |

## 4.6 Chat

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-360** | P0 | One long thread per host, across days, with date separators named after episodes. The host's first message arrives within 30 seconds of the chat door opening, or within 30 seconds of the call ending if the learner stays in the app. | C |
| **FR-361** | P0 | **The opener** asks the learner to restate one point first (from the episode, the article or the call) before the host adds anything new. **Length:** 3 to 5 host messages; the host ends at message 5 at the latest with a natural closer, then tomorrow's three ideas appear. If the learner keeps writing after the closer, the host sends one final short reply and goes quiet; anything after that is answered in one callback line next session. **Content contract:** adds something new (a comeback, a joke, a clarification, the next angle); never re-litigates the call; never assigns anything. | C |
| **FR-362** | P0 | **No margin note.** When it helps, the host's reply says the learner's point back the natural way, at most once per chat ("So the meeting *was* cancelled? Classic."). Nothing is marked, underlined or annotated. **Writing help:** if the learner asks how to write something, the host gives a hint first, never a rewrite of the learner's message. | D3 |
| **FR-363** | P0 | Text only in the beta. Each bubble sets its own text direction. | C |

## 4.7 The word sheet (tap to define)

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-370** | P0 | Contents: the meaning in the learner's language for this sense, the sentence it came from, 🔊 to hear the word (cut from the episode or article audio using word timestamps, so it is the host's voice), and **Keep this word**. A phrase can be selected by dragging across words; multi-word chunks have their own glosses. | C |
| **FR-371** | P0 | Glosses come from a shared cache keyed by lemma, sense and native language, generated once for all learners; sense is chosen per occurrence at generation time. All glosses for a script and article are ready before the episode ships, so the sheet opens in under 300 milliseconds (NFR-110). | C (decision 8, shared ingredients) |
| **FR-372** | P0 | **Keep** adds the word to the notebook and tells the teacher to bring it back in later episodes. Logged: word, lemma, sense, surface (transcript, Huh?, article), time, and the learner's lookup count for that lemma across sessions. A word tapped twice or more becomes a recall candidate (FR-723). | C |

---

# PART 5 — GENERATION PIPELINE AND QUALITY GATE (FR-4xx)

## 5.1 Pipeline per episode

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-401** | P0 | Each episode is produced by a durable workflow with these steps, each with a timeout and retries: (1) **Brief** from the teacher: idea, format, cast, arc and season context, 1 grammar target, 2 to 4 due or new words, coverage targets, length, speech rate, up to two usable life facts, the callback, energy and anxiety state, "why this episode" reasons; (2) **Writer**: script with scene breaks and speaker turns, article, call brief (position, pushback material, target-necessity moves, recall gaps, recast list, three words for the planning card), chat opener, 90-second small-door recap, two shadow lines; (3) **Fitter** (FR-410); (4) **Editor** (FR-41x); (5) **Voice studio**: two-voice episode audio with expressive tags, article read-aloud, recap, feed tag, word timestamps (from the vendor or by forced alignment), name pronunciation from the learner's own recording of their name; (6) **Audio re-listen** (FR-425); (7) **Gloss precompute** for every word in script and article (cache misses only); (8) **Publish** to the app, and to the feed at the drop time. | C |
| **FR-402** | P0 | The pipeline never fails to deliver: on any unrecoverable failure the fallback episode (FR-422) or the rules-built brief (FR-740) ships, and the failure is logged. | C |

## 5.2 The fitter

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-410** | P0 | A lemmatizer splits the text into lemmas and known chunks; the word bank gives each a probability of being understood (by ear for the script, in reading for the article). **Expected coverage** is the mean of those probabilities over running words, excluding names and the planned new words. **Pass:** expected coverage at or above the learner's current target (default 95% for audio, 98% for text, adjusted per FR-730); planted new words within budget (FR-722); every target and due word present in its planned surfaces (episode, article, call brief, chat opener). On fail, only the failing sentences are rewritten; at most two rewrite rounds. | C |
| **FR-411** | P0 | The fitter reports the new-word count, the share of new words from the top 3,000 lemmas, and the predicted difficulty, which "why this episode" (FR-741) and the "how much did you follow?" check (GATE-M10) use. | C |

## 5.3 The editor's gate

Every check is pass or fail. Checks 1, 2 and 4 are code; the rest are the editor model (a different vendor from the writer) with a fixed rubric.

| ID | Pri | Check | Requirement | Source |
|---|---|---|---|---|
| **FR-412** | P0 | 1 Level fit | The fitter passed. | C |
| **FR-413** | P0 | 2 Targets present | In every planned surface. | C |
| **FR-414** | P0 | 3 Language correctness | Grammatical, natural target language (for English, in the chosen accent's spelling); no errors in the model sentences. | C |
| **FR-415** | P0 | 4 Memory | Every life fact used is confirmed, unexpired, not marked "don't bring up", and its source quote exists in the event log. No more than two life facts. | C, TC-1 |
| **FR-416** | P0 | 5 Not generic | "Would this episode work unchanged for another learner?" Yes fails. | C |
| **FR-417** | P0 | 6 No unsourced world facts | No real-world result, statistic or news stated as fact unless it came from the learner. | PRD call (the beta has no scout) |
| **FR-418** | P0 | 7 The fun carries the language | Every joke, twist and personal moment carries at least one target or due item. Fun that carries nothing is cut. | S |
| **FR-419** | P0 | 8 Stands alone, 9 Variety | The episode can be understood without earlier episodes, even inside an arc (LAW-04); the format rule, ban list and similarity check pass (FR-43x). | D5, C |
| **FR-420** | P0 | 10 Law scan | No game language, no grading, no explicit correction by anyone ("wrong", "mistake", "the correct answer", a learner sentence beside a corrected one), no guilt, no "I miss you", no lesson words ("lesson", "test", "exercise", "level", "homework") in any surface. | D3, D4, LAW-01, LAW-07 |
| **FR-421** | P0 | 11 Pitch test | "Would this person, with this interest profile, choose this over a real podcast at 8am?" No fails. | C |
| **FR-422** | P0 | On fail | Targeted repair of the failing part and one recheck. On a second fail, ship the **fallback episode**: built from the learner's top interest with no life facts, no arc and no callbacks; it must still pass checks 1 to 6 and 10. The teacher logs the failure; three fallbacks for one learner in 7 days page a human. | C; paging rule: PRD call |
| **FR-425** | P0 | Audio re-listen | The rendered audio is run back through speech recognition and compared with the script. Lines with skipped or garbled words, a mispronounced learner name or a mispronounced target word are re-synthesized, up to two attempts; then the line is rewritten with a synonym (if not a target) or the episode ships with that line's transcript marked. | C; fallback: PRD call |

## 5.4 Variety, shared ingredients, review

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-430** | P0 | **Real input in every episode:** at least one element that did not come from the model: the learner's life, their own words from the last call, or something they told the show this week. | C |
| **FR-431** | P0 | **Ban list:** stock names, settings and plots that AI stories converge on, kept per language package and updated monthly from the human read (FR-436). | C |
| **FR-432** | P0 | **Format rotation:** formats are tracked over the last 10 episodes; no format runs three times in a row. **Format library (beta):** debate, story time, news-style rundown (of the learner's own news), interview, explain-it-to-me, mystery, gossip, roast, rehearsal. The learner can describe any other format in "Tell Salma an idea"; the writer maps it to the closest pattern and follows the learner's description on conflict. | C |
| **FR-433** | P0 | **Similarity check:** each new script is embedded and compared with the learner's last 20 scripts; above the threshold it is regenerated. Threshold set in Milestone 0 from scripts the human reviewer judges "too alike" (starting value: cosine 0.85; OPEN-10). | C; starting value: PRD call |
| **FR-434** | P0 | **Authored hosts:** people write the hosts and Salma (OPEN-03); the model writes only episodes. **Surprise in the content, never in rewards:** a callback from weeks ago, a returning side character, a one-day format change. | C |
| **FR-435** | P0 | **Shared ingredients,** made once and shared across learners with no difference a learner can notice: the gloss cache, host and Salma bibles, the ban list, sound design. Per-interest news digests are LATER with the scout. | C (decision 8) |
| **FR-436** | P0 | **Human review:** a paid native reviewer of each target language reads 10 random episodes per learner per month in the beta (in Milestone 0, every episode) and flags errors, sameness and anything that breaks a law. Findings update the ban list, prompts and the similarity threshold. | C |
| **FR-437** | P1 | **Offline test suite:** 30 to 50 synthetic learners at different levels with planted error patterns, and a simulated caller. Run on every prompt or model change; a change that worsens recast and clarification rate on planted errors, learner talk share, host latency, recall-gap count, analyst tag precision on the hand-tagged set or coverage accuracy does not ship. | C |

---

# PART 6 — CAST, PRODUCER AND SERIES (FR-5xx)

## 6.1 The hosts

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-501** | P0 | One authored host duo per target language; Karim and Mona are the English duo, shared by every native language that learns English. Each host has a bible written by a person (OPEN-03): values, opinions and biases, humour, speech patterns, how they disagree with each other, their stance toward the learner, what they never do, and their in-show storylines. The bibles are content in the language package, not prompts invented per learner. | C, D1 |
| **FR-502** | P0 | **Voices:** three candidate voices per host per accent, chosen by the blind listening test (FR-1330). The learner hears each host's hello in onboarding and can swap within the pool. | C |
| **FR-503** | P0 | Changes after onboarding (voice swap or rename, through Salma or Controls) are announced on air in one line in the next episode. A host's voice, personality or memory never changes silently, including across model or vendor upgrades; a forced vendor change is announced the same way. | C |
| **FR-504** | P0 | **Casting per episode:** one host or both, chosen with the idea. In the call the learner talks to one host, the one who threw. | C |
| **FR-505** | P0 | **Side characters:** three to five recurring side characters per learner's world, created by the writer within the hosts' bibles and stored in the series bible. A character based on a real person in the learner's life uses only what the learner said, and only a first name or role the learner used. | C (decision 5) |

## 6.2 The producer: Salma, who never corrects

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-520** | P0 | One authored producer per native language, named and voiced for it (Salma in the Arabic package; this document says "Salma" for the producer in any language). Her voice is closer and drier than the hosts', like a voice in the headphones. On screen she is a monogram, not a face. | C, D1 |
| **FR-521** | P0 | **Salma does:** onboarding; life updates and "tell Salma an idea"; the notebook; the voice of the weekly proof and the season finale; settings changes by conversation; "what do you know about me?"; fact corrections; "where do I stand?" (FR-846); "why do we say it like that?" answered plainly, only when the learner asks. | D3, C |
| **FR-522** | P0 | **Salma never:** corrects, sends notes after a call, writes margin notes, performs in the show, guilts, praises every turn, grades. **In the call she is silent** (FR-325). | D3 |
| **FR-523** | P0 | **Language balance:** in season 1 at least 80% of Salma's words are in the learner's own language. Each new season her target-language share rises by about 10 points if the speaking estimate rose, never above 70%. The learner can ask for more or less at any time. | PRD call |
| **FR-524** | P0 | **Which voice and variety:** per native language, chosen by a blind test with 5 native listeners (FR-1330); her writing is friendly and plain, not formal. (For Arabic, Gulf dialect versus neutral educated Arabic is settled by that test.) | PRD call |

## 6.3 Series bible, arcs and seasons

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-540** | P0 | **The series bible (per learner)** is stored with the learner model and compiled into the writer's brief: the hosts (authored, read-only), side characters, recurring places, running jokes (with the episode they started in), open arcs, the current season and its goal, and the show canon (positions the hosts and the learner took, things already said). The canon blocks repeated angles and contradictions. | D5 |
| **FR-550** | P0 | **Arcs:** length 1 to 3 weeks; at most two open at once; best drawn from the learner's real life (the interview: prep, the day, the debrief). | D5 |
| **FR-551** | P0 | **An arc waits for the learner.** Nothing in it happens while they are away; the next episode picks it up with one line. Every episode inside an arc stands alone (FR-419). | D5, LAW-04 |
| **FR-553** | P0 | **Mid-season rehearsal:** when the season goal is a real scene (an interview, a call, a trip), one episode near the middle of the season uses the rehearsal format: the episode sets the scene, and the call is the scene itself, with the host playing the other person. Rehearsal on demand at any time is LATER. | C; PRD call reconciling concept v2 §6 and §9 |
| **FR-555** | P0 | **Seasons are 4 weeks.** Season 1 starts on the onboarding day. A season cannot be broken: it ends on its date whether the learner did 3 episodes or 25. | D5 |
| **FR-556** | P0 | **One real goal per season in the learner's words**, a learning goal, never a score; a goal that needs longer runs across two seasons. Salma names each season from what happened ("Season 2: Interview season"). The next season's goal is set inside the finale (FR-920). | D5 |
| **FR-557** | LATER | A new season may bring a new format or a guest host to counter the novelty fade around week 4. Guest hosts are authored like the duo. | C |

## 6.4 Honesty and crisis protocol

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-560** | P0 | Salma says she is AI in her first lines in onboarding, and the hosts in theirs; host portraits carry a small "AI" mark; every character answers "are you real?" honestly, every time. Clean goodbyes: no host asks the learner to stay. | LAW-05, TC-3 |
| **FR-561** | P0 | **No fake lives.** The hosts' storylines are the show's fiction, inside the show, like a sitcom. A host never claims to exist outside the show, to have met the learner, to remember them between episodes "personally", or to miss them. Asked about it, the host says it is part of the show. | PRD call (the line between in-show fiction and fake lives) |
| **FR-570** | P0 | Every live role (host, Salma) and the after-session analyst watch for statements of self-harm intent or crisis, in either language. | C (decision 9 flags), L |
| **FR-571** | P0 | On detection in a live call or chat: the character steps out of the show, says plainly that it is an AI and cannot help with this, and shows the crisis resources for the learner's country from the language package (reviewed by counsel). The session continues only if the learner chooses. Detected in after-session analysis only: Salma shows the same resources at the next open, once. | L |
| **FR-572** | P0 | Every activation is logged for the annual reporting California SB 243 may require. Details pending legal review (OPEN-05). | L |
| **FR-580** | LATER | Character creation, the six chassis, user-created hosts and guest hosts made by learners: after episodes are loved. | C |

---

# PART 7 — THE LEARNER MODEL (FR-6xx)

## 7.1 Principles and the event log

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-601** | P0 | **The event log is the source of truth.** Every transcript, tap, replay, skip, timing and edit is appended, never changed. The nine stores are computed from it, so the whole model can be rebuilt when the analyst improves. | C |
| **FR-602** | P0 | **Models propose, code decides.** Model outputs are candidate updates in a fixed schema; code validates and applies them. **Live roles never write:** the host and Salma produce transcripts only; after-session roles write. **Each role gets a compiled brief,** never the whole file (FR-640). | C |
| **FR-603** | P0 | Each event carries: learner, session, door, type, time, payload, the model and prompt versions that produced it, and cost. Types include at least: `play`, `pause`, `seek`, `speed`, `replay_line`, `huh`, `transcript_toggle`, `tap`, `keep`, `mark`, `article_scroll`, `read_aloud`, `call_turn` (streaming and verbatim text, word timings and confidences), `word_button`, `hold_floor`, `silence`, `shadow`, `chat_message`, `idea_shown`, `idea_chosen`, `swap`, `small_door`, `fact_card_edit`, `notebook_edit`, `working_on_edit`, `claim_shown`, `consent_change`, `worth_it_answer`, `wrong_memory_flag`. | C |

## 7.2 The nine stores

| ID | Pri | Store | Per item | Written by |
|---|---|---|---|---|
| **FR-610** | P0 | **Word bank** | Every lemma and multi-word chunk met: p(understood by ear), p(understood in reading), p(produced correctly), review state (stability, difficulty, due date), encounters by surface, lookups, first seen, last seen, kept flag, the learner's own sentences using it | Code, from the log and the analyst |
| **FR-611** | P0 | **Structure map** | Each structure in the inventory: state (not seen, heard, attempting, taking, stable), obligatory-context counts and accuracy over 14 days, avoidance flag, review state, up to 3 example sentences of the learner's own, lifecycle as a target | Analyst, checked by code |
| **FR-612** | P0 | **Error profile** | Recurring errors by reporting category and structure, each with 2 or 3 verbatim examples and session ids | Analyst |
| **FR-613** | P0 | **Skills** | Listening, reading, speaking and writing estimates, each with a range; speech rate, mean length of run, mid-clause pause rate, articulation rate, per task type; pause profile for turn-taking; reading speed | Code |
| **FR-614** | P0 | **Interests** | Topic, salience, depth (curious, fan, expert), last engaged, dormant flag; hard dislikes and no-go topics | Memory keeper, behaviour |
| **FR-615** | P0 | **Life** | Facts: text, exact source quote, session, time, confidence level, sensitivity class, valid from, expires at, status (active, dormant, superseded, deleted), "don't bring up" flag; dated follow-ups with due and used state | Memory keeper; the learner's edits |
| **FR-616** | P0 | **Goals** | Real situations as can-do statements ("handle a job interview in English"), the season goal, the anchor and rhythm | Salma's conversations via the after-session pass; the learner |
| **FR-617** | P0 | **Taste** | Format and host completion, what makes them talk most (learner words per minute by topic and format), episode length, time of day, swap and skip patterns. Preference only, never a "learning style". | Code |
| **FR-618** | P0 | **Show canon** | Positions taken, running jokes, things said, side characters, open arcs (also in the series bible) | Analyst |
| **FR-619** | P0 | Every number that is an estimate carries a range. | C |

## 7.3 Life-fact rules

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-620** | P0 | **Quote check:** a life fact is stored only if its source quote appears word for word in the verbatim transcript or chat. | TC-1, TC-6 |
| **FR-621** | P0 | **Confidence ladder:** said once: stored, never spoken, shown in the notebook as "I think...". Said again in another session, or confirmed by the learner when asked, or left unedited on a notebook card the learner viewed: usable. Edited by the learner: ground truth, at once. | C; "left unedited after viewing": PRD call |
| **FR-622** | P0 | **Sensitivity:** health, money, relationships, religion and politics are sensitive. A sensitive fact is used only in the session where the learner raised it, stored only if the learner confirms, and never brought up first. | C (decision 8), TC-6 |
| **FR-623** | P0 | **Time:** each fact type has a shelf life (job: months; "sick this week": days). Expired facts are never spoken. A conflicting new fact supersedes the old one and keeps the history ("How's the new job?"). **Follow-ups:** a dated event triggers one follow-up after its date, then moves to history. | C |
| **FR-624** | P0 | **Interests decay:** salience falls over a few weeks without engagement; dormant interests are kept, never pitched, and wake the moment the learner mentions them. | C |
| **FR-626** | P0 | **Corrections:** when the learner corrects the show, the host or Salma says so plainly ("My mistake, noted."), the fact is fixed at once, and a `wrong_memory_flag` is logged (GATE-13). | TC-7 |
| **FR-630** | P0 | **Rebuilds:** when the analyst, edit classifier or measures change version, the after-session pass is re-run over the log and the stores are rebuilt. Claims already shown are never retracted silently; if a rebuild invalidates one, Salma says so in the next proof. | PRD call |

## 7.4 Compiled briefs

| ID | Pri | Role | Gets |
|---|---|---|---|
| **FR-640** | P0 | Teacher | Everything, summarized; the full due list; the structure map; the last 14 days of sessions |
| **FR-641** | P0 | Writer | The brief, up to two usable life facts with their quotes, the series bible excerpt, targets, due and new words, coverage and length targets, the ban list |
| **FR-642** | P0 | Host (live) | Position and pushback material, targets and their necessity moves, 2 to 4 recall gaps, 3 words to draw out, one callback, pause profile, anxiety flag, the learner's name and pronunciation. One page. For the word button: the learner's produced-word history (FR-326). |
| **FR-643** | P0 | Salma | Usable life facts with quotes, goals, the working-on list, claims that passed the gate. **Never error lists.** |
| **FR-644** | P0 | Chat host | The call transcript summary, targets, the opener |
| **FR-645** | P0 | Proof producer | Claims that passed the gate, with their evidence; nothing else from the model |

---

# PART 8 — THE TEACHER (PLANNER) (FR-7xx)

## 8.1 Triggers and targeting

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-701** | P0 | **Triggers:** after each session (once the after-session pass finishes, within 10 minutes) it updates the plan and writes the brief for the chosen idea or the cutoff pick; nightly in batch it plans the weekly mix, arc and season progress, and the three ideas to show at the end of tomorrow's session; a follow-up coming due rewrites one idea; a gap of 5+ days plans the return episode; a season boundary plans the finale and the next opening. Concurrent triggers coalesce into one run. | C |
| **FR-702** | P0 | **Candidates** are structures in the inventory and words in the word bank, scored on six factors: **need** (how often it goes wrong and how much it hurts understanding; meaning-changing errors outrank barely noticed ones), **goal fit** (does the learner's real situation demand it), **readiness** (already attempting it, or the step before), **learnability** (a clear rule, or item by item), **opportunity** (can tomorrow's episode make it natural and necessary), **due** (about to be forgotten). | C |
| **FR-703** | P0 | **Caps:** 1 grammar target and 2 to 4 words per session; no target in more than 4 consecutive sessions. **Contrast pairs:** where the learner confuses two forms, both are targeted in the same episode, built so both are needed. | C |
| **FR-704** | P0 | **An error pattern enters targeting** only after 3 observations across at least 2 sessions (error, not slip; FR-820). | S |
| **FR-706** | P0 | **The "working on" list** (notebook) shows at most 3 items in plain words. The learner can veto an item (it leaves targeting unless it breaks meaning) or add one ("I want to sound professional on calls"), which the teacher turns into structures and words the same day. | D4 (d), LAW-03 |
| **FR-707** | LATER | **Exploration:** 10 to 15% of target slots try a different treatment, recording which one moved this learner. | C |

## 8.2 Treatment, review, new words, the edge

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-710** | P0 | **Treatment by learner state:** never attempted but expected at their stage: input flood (hosts use it often and audibly in the episode), no correction, 1 to 2 weeks before it becomes a productive target. Attempting, rule-based, with errors: clear recasts in the call; the form returns often and audibly in the next episodes and articles, and in calls that make it necessary. Attempting, item-based (word choice, collocation): recast, then the item returns on schedule. Avoided (expected, never used, paraphrased around): a host models it, then a call question that is hard to answer without it. Slow or broken speech on easy content: retell, and round two "shorter and faster". A mistake the learner says they don't care about: dropped from targeting unless it breaks meaning. | D3, C |
| **FR-720** | P0 | **Review schedule:** every word, chunk and structure has a review state in an FSRS-style scheduler (code). **Due** means predicted recall below 0.85 by the next drop time (tuned in the beta). Grammar targets are spaced tightly early (every 1 to 3 days); words on widening gaps. | C; 0.85: PRD call |
| **FR-721** | P0 | Due items return through four channels: the same day across surfaces (episode, article, call, chat); across days in new stories; through the recurring world (arcs, running jokes); and through the hosts' "you mean..." lines that echo the learner's own sentences. | C, LAW-10 |
| **FR-722** | P0 | **New words:** 3 to 6 planted per episode; at least 80% from the top 3,000 lemmas of a general frequency list, not the topic's niche vocabulary (frequency floor). | PRD call |
| **FR-723** | P0 | Words the learner tapped twice or more become recall candidates: the call brief creates a need for them and the next episodes use them again. Kept words are scheduled like targets. | C |
| **FR-730** | P0 | **The edge.** Difficulty is set per surface from the skill estimates by dials the fitter enforces: audio coverage default 95% (easier 96%, harder 94%, floor 93%); text coverage default 98% (99%, 97%, floor 96%); speech rate per learner (−5% / +5%, cap 100%); episode length default 6 minutes (−1 / +1, cap 8). | C; table: PRD call |
| **FR-731** | P0 | **One step easier** for: the first three episodes, a return episode, low-energy signals (short replies, a skipped call, an error spike, "today was too hard"), a Huh? rate above the learner's 2-week median by half. **One step harder** for: two sessions in a row with a Huh? rate below median, full uptake and no low-energy signal. At most one step per session. | PRD call |
| **FR-735** | P0 | **Ideas and prediction:** three ideas per day ranked by predicted choice (interest salience × format history × arc pull × recency of topic); the cutoff pick is the top-ranked idea. | C |
| **FR-740** | P0 | **Fallbacks:** if the teacher cannot complete a brief (model failure, timeout), the brief is built by rules from the due list, the top interest and the next format in rotation. If the learner model is unavailable, the last good plan is used. The learner always gets an episode at the drop time. | C |
| **FR-741** | P0 | **"Why this episode":** for every episode the teacher writes 2 to 4 plain reasons, each traceable to the learner model ("You said on Monday the derby was Sunday." "It brings back 4 words from this week." "Shorter than usual: you've been busy."). Stored with the episode and shown in the notebook. | LAW-03 |

---

# PART 9 — ASSESSMENT ENGINE AND CLAIM GATE (FR-8xx)

**Two standards, four clocks.** Planning signals can be fast and noisy: a wrong guess costs one slightly mistargeted episode. Claims to the learner must be slow and checked: one false claim costs trust in every later one. The claim gate (FR-840) separates them. Nothing in assessment runs in the live path.

| Clock | What runs | What it may influence |
|---|---|---|
| During the call | Nothing is graded; the host works from its brief | The conversation only |
| After each session (within 10 minutes) | The after-session pass (FR-801 to FR-807) | Tomorrow's plan; never a claim |
| Weekly | Fluency and complexity on retell turns and round two only, smoothed over 2 weeks; avoidance check | Difficulty dials; the weekly proof only through the gate |
| Every 4 weeks | The then-and-now recording (FR-851), rated by a calibrated model plus code metrics | Speaking claims; re-anchoring skill estimates; outcome metrics |

## 9.1 The after-session pass

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-801** | P0 | **Verbatim re-transcription** of every learner audio turn (call, round two, shadow, say-it-once, small-door voice note): fillers, false starts and self-corrections kept, with word timings and confidences. The streaming transcript is never used for assessment, because streaming recognizers silently fix learner errors. | L (voice lens) |
| **FR-802** | P0 | **Analyst** (small model, fixed schema): for each learner turn and chat message, the smallest correction that makes it acceptable (nothing stylistic); comprehension and content-uptake rating 0 to 2; can-do moments; words reached for; recast uptake (did the learner repeat a recast form in the next turn?); self-corrections. | C |
| **FR-803** | P0 | **Edit classifier** (code): aligns original and corrected text, classifies each edit into the structure inventory and the 12 reporting categories (ERRANT-style rules for English), and computes obligatory-context use per structure. | C |
| **FR-804** | P0 | **Confidence filter:** edits inside speech regions below the recognizer confidence threshold are dropped from the error profile and can never feed a claim. The threshold comes from the 30-clip test (FR-862). | PRD call (empirical threshold) |
| **FR-805** | P0 | **Measures** (code) on comparable segments (FR-810 to FR-812); **updater** (code): Bayesian updates of skills, word probabilities and structure states, each with a range; review states updated; target lifecycles moved (FR-821). | C |
| **FR-806** | P0 | **Memory keeper** (small model plus rules): life-fact candidates with quotes, interests, goals, canon; validated by code (FR-620 to FR-624). | C |
| **FR-807** | P0 | The pass completes within 10 minutes of the call ending (NFR-112); its output feeds the teacher's next plan. | C |

## 9.2 What is measured

| ID | Pri | Dimension | Measures | Measured on |
|---|---|---|---|---|
| **FR-810** | P0 | Accuracy | Correct use in obligatory contexts per structure; errors per 100 words by category, always read next to what was attempted | Calls, chats |
| **FR-811** | P0 | Complexity and fluency | Clause length, subordination, lexical diversity (MTLD), share of words beyond the top 2,000; speech rate, mean length of run, mid-clause pause rate, articulation rate (filler and repair counts logged, not weighted) | Retell turns, round two, the 4-weekly recording only |
| **FR-812** | P0 | Vocabulary, comprehension, pronunciation, word button | Word probabilities (understood, produced) and words owned on every surface; content uptake 0 to 2, Huh? rate per minute, taps per 100 words and "how much did you follow?" answers per session; sentence- and word-level pronunciation scores on known sentences only (shadow lines), internal and never shown; word-button presses per call, by word | As listed |
| **FR-815** | P0 | **Structure inventory:** for English, seeded from the English Grammar Profile, filtered to the structures that matter from A2 to B2, a few hundred items (commercial-use permission: OPEN-08). **Twelve reporting categories** (localized per language package; English set): verb tense and aspect, subject-verb agreement, articles, prepositions, word order, word choice, plurals, pronouns, comparatives, conditionals, question formation, register. Used for reporting and the proof; targeting works on the inventory. **Frequency list and lemmatizer:** a general lemma frequency list from subtitle corpora plus a formulaic-sequence list; a standard lemmatizer. | C; subtitle corpus: PRD call |

## 9.3 Error, slip, lifecycle, "learned"

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-820** | P0 | A pattern counts as an error, and can become a target, only after 3 observations across at least 2 sessions. | S |
| **FR-821** | P0 | **Lifecycle:** Not seen → Heard (met in input) → Attempting (used at least once) → Active target (chosen by the teacher) → **Taking** (correct and unprompted in an obligatory context in 2 different sessions, at least one a day or more after the last time it was targeted) → **Stable** (about 80% correct in obligatory contexts over 14 days or more, across at least 5 contexts; confirmed only when it holds in the next 4-weekly recording) → re-checks at 2, 4 and 8 weeks after Stable; a failed re-check returns it to Active. | S |
| **FR-822** | P0 | **"Learned"**, in any claim, means correct, unprompted, at least a day later, in a different session. **Words owned:** a word used correctly and unprompted in two different sessions at least a day apart. | S |
| **FR-823** | P0 | **Avoidance:** weekly, structures expected at the learner's estimate that they have never attempted are flagged; flagged structures get input flood first, then an avoidance treatment (FR-710). | C |

## 9.4 Skill estimates, the word check, the then-and-now recording

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-845** | P0 | Four estimates (listening, reading, speaking, writing) on a fine internal scale anchored to CEFR, each with a range; updated slowly every session; re-anchored by the 4-weekly recording. CEFR words never appear on any surface unprompted. | D4 (f) |
| **FR-846** | P0 | **"Where do I stand?"** When the learner asks, Salma answers per skill with a range and what it means in real situations ("listening around B1: you can follow a colleague who speaks clearly; speaking just below"), **only for skills whose calibration bar is met** (FR-860). For other skills she says plainly she cannot say reliably yet and points to the evidence in the notebook. | D4 (f); calibration condition: PRD call |
| **FR-850** | P0 | **The word check** (onboarding, optional): 48 yes/no items, 36 real lemmas (6 from each of six frequency bands between the top 1,000 and 10,000) plus 12 pseudowords. Scored by hits minus false alarms per band into a vocabulary-size estimate with a range, which seeds every word's prior. Stops at 75 seconds; partial answers still count. Framed as "help me pitch your show". | D4 (b); item counts: PRD call |
| **FR-851** | P0 record / P1 compare | **The then-and-now recording:** about 3 minutes of the learner's speech, the same task types every time: a 60-to-90-second retell of a short story matched for difficulty, a 60-to-90-second opinion on a familiar topic, and 8 sentences to repeat back of increasing length. Framed openly as "recording your then-and-now"; Salma explains why it is always the same kind of task. Nothing is scored on screen. Skippable, and the learner is told that skipping means no voice comparison that month. | D4 (c); 90-second opinion: PRD call |
| **FR-852** | P0 | The first "then" is offered after session 2 and again once in sessions 3 to 5; afterwards, every season finale. If voice storage is off, the comparison uses transcripts and measured differences only, and the consent screen says this loses the most motivating part. Never recorded through the dial-in number. | PRD call (baseline in week 1, not onboarding) |

## 9.5 The claim gate

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-840** | P0 | Every sentence about the learner's progress, in the proof, the finale, a host line or "where do I stand", passes all five rules in code: (1) **like for like**: the same task type; (2) **beyond the noise**: the change exceeds about twice the measure's standard error, estimated per metric from learners who recorded twice a few days apart; (3) **repeated**: at least two data points point the same way, except first-ever events; (4) **clean evidence**: grammar claims from chat text or high-confidence speech only; (5) **openable**: every claim carries its evidence and the learner can open "how we know". | LAW-12, D4 |
| **FR-841** | P0 | Until a metric's standard error is estimated (from Milestone 0 and early beta test-retest pairs), only first-ever events and words-owned claims may be made about it. | PRD call |
| **FR-842** | P0 | **When nothing passes,** the honest thing is said instead ("too early to tell"; "flat week, and here is the one thing I'm changing"). When accuracy fell while the learner attempted harder language, that is said with its evidence. **Fabricated wins are impossible by construction:** the proof producer receives only claims that passed (FR-645). | TC-4 |
| **FR-860** | P0 | **Calibration before claims,** per language pair, before the paid beta: 150 to 200 learner samples (calls and chats, starting with Milestone 0's hand-tagged calls) double-tagged by trained teachers. Bars: level rating agreement at a quadratic weighted kappa of about 0.7 or better; precision of at least 0.8 on every error tag that feeds a claim. The rating model version is pinned for each 4-week window so an upgrade never shows up as learner progress; the calibration set is re-run on every model change. | C |
| **FR-861** | P1 | **External test:** 20 to 30 beta learners take a recognized test of their target language with a speaking component at week 0 and week 8, paid by For one, starting with English learners (default: the Duolingo English Test; OPEN-09). Results calibrate the internal scale; never shown to other learners, never used in marketing without consent. | C (decision 10c) |
| **FR-862** | P0 (before build week 2) | **The recognizer test:** for each target language, 30 recorded clips of real learners from at least two native-language groups are run through each candidate streaming and batch recognizer; count how many real learner errors survive (hand-tagged), filler retention, hallucinations near long pauses, and handling of switches into the learner's own language. A target that fails ships later; it never ships with a weaker bar. The winner per role and the confidence threshold (FR-804) come from this test. Recognizer error is tracked by first language from day one. | L (voice lens), D1 |

## 9.6 Correction layers (what the learner experiences)

| ID | Pri | When | Who | What the learner experiences |
|---|---|---|---|---|
| **FR-830** | P0 | During the call | Host | Clarification requests when meaning blurs; "you mean..." recasts (bold in the caption); recall gaps; hints before answers |
| **FR-831** | P0 | During the call, on request | Host (word button) | A word or a hint, because the learner asked |
| **FR-832** | P0 | Right after the call | Nobody | Nothing to read |
| **FR-833** | P0 | In the chat | Host | At most one "so you mean..." inside a normal reply |
| **FR-834** | P0 | Any time, on request | Host or Salma | "Why do we say it like that?" answered plainly |
| **FR-835** | P0 | Weekly | Salma | The proof: one headline, the next focus, the "working on" list; never a list of mistakes |
| **FR-836** | P0 | Across weeks | Teacher | The form returns in new episodes, spaced, and calls make it necessary |
| **FR-837** | P0 | Every layer | All | Never "wrong", "mistake" or "correct"; never the learner's sentence beside a corrected one; never while the learner is speaking or writing; paired with a real win when one exists; never a number or a grade. Grammar is explained only when the learner asks. |

**The risk, stated once.** Recasts alone are the least-noticed kind of feedback. This spec keeps correction invisible and works against that risk in three ways: recasts are salient (one change, stressed, said back as "you mean..."), the learner's errors become the next episodes' language (FR-710), and the 4-weekly recording measures accuracy. If accuracy is flat for most learners after a season, GATE-07 shows it and the fix is decided then.

---

# PART 10 — WEEKLY PROOF AND SEASON FINALE (FR-9xx)

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-901** | P0 | **Every week, for every learner,** on the learner's proof day: by default the weekday on which they used the show most in their first week; until then, day 7. It never waits for a minimum number of sessions. | C |
| **FR-902** | P0 | **Form:** an audio episode of about 2 minutes presented by Salma, with the learner's own clips and at most one line from a host. It sits above today's episode on Today with its own cover, and in the feed [OPEN-01]. | C |
| **FR-903** | P0 | **Contents, in order:** (1) one headline piece of evidence that passed the claim gate, with "how we know" behind it; (2) the rhythm, in words, only if it was met (FR-224); (3) the next focus; (4) the "working on" list, with one tap to change it; (5) one question: "Was this week worth your time?" (yes / mostly / no) and an optional free-text "why". A "more" section on screen holds the other passed claims, if any. | C, D4; answer options: PRD call |
| **FR-904** | P0 | **Simple version for 2026-12-23:** headline from first-ever events and words owned, the next focus, the working-on list, the worth-it question. The full gate on fluency and accuracy claims follows once standard errors exist (P1). | C |
| **FR-905** | P0 | **A slow week** (no session or one) gets a shorter proof, about 45 seconds, about what has built up over time (hours, words owned since the start), never about the week. | D5, TC-4 |
| **FR-906** | P0 | **A flat week** says so plainly and names the one thing the teacher is changing. **A worse week** says so with the most likely reason the evidence supports (harder material, a long gap) and the change. | TC-4 |
| **FR-920** | P1 | **The season finale:** offered at the learner's first session on or after day 28 of the season, as a special episode. Contents: the then-and-now recording played next to the last one; **at most two measured differences in plain words** (gated claims only); the real-world attempt if there was one; a short recap (episodes, about how many hours heard, minutes spoken, words owned, the moment Salma liked most); and the next season's goal, set inside the finale. If the learner skips the recording, the finale still happens without a voice comparison, and the season still ends on its date. | D4, D5 |
| **FR-921** | LATER | **Longer windows:** then-and-now compares 1 month, 3 months, and later 1 year; a year-in-review episode. | C |

---

# PART 11 — SHOW, NOTEBOOK, CONTROLS, DATA AND TRUST (FR-10xx)

## 11.1 App structure and the archive

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-1001** | P0 | Three tabs: Today (FR-235), **Show**, **Notebook**. The interface is in the learner's language, right to left where that language is. Dark mode is first-class. No mascot, no avatars: hosts are simple portrait marks, Salma a monogram. Sound design: a show sting opens and closes every episode; the learner's turn is signalled by the host's breath and a soft rising tone, never a beep; no reward sounds anywhere. | C, LAW-01 |
| **FR-1002** | P0 | **Show (the archive):** a shelf of seasons, each a row of typographic episode covers. Every episode is replayable, with its transcript, article, call recording (if kept) or transcript, and chat. No statistics, aggregates or charts. | C, LAW-01 |

## 11.2 The notebook (styled as Salma's notebook, not as settings)

| ID | Pri | Section | What it holds |
|---|---|---|---|
| **FR-1010** | P0 | What I'm working on with you | At most 3 items in plain words, each with one of the learner's own sentences as an example. Veto (✕) or "add something" by text or voice. Can be hidden by the learner. |
| **FR-1011** | P0 | About you | Every life fact, interest and goal Salma holds, each with its source ("you said on Oct 3: ..."), ✎ and ✕, and "don't bring this up". Unconfirmed facts show as "I think..." and are never used in the show until confirmed. |
| **FR-1012** | P0 | Words you own | Each word with the learner's own sentence, date and ▶ audio. One quiet count at the top that only grows. |
| **FR-1013** | P1 | The tape | The then-and-now recordings as tiles, one per season, with ▶ "Play then and now" and Salma's one-line, gated comparison. |
| **FR-1015** | P0 | Out in the world | Real uses the learner reported ("I had the interview"), dated. Salma adds them when the learner mentions them; the learner can add one directly. |
| **FR-1016** | P0 | Kept words and marked moments | Words kept from the word sheet; moments marked with the next-track button, with their sentence and audio. |
| **FR-1017** | P0 | Hours | "About 41 hours heard, 6 hours spoken." Hours heard count app playback, plus each feed episode once at its full length when the learner later used that episode's call, chat or small door. Cumulative, never reset, no goal. |
| **FR-1018** | P0 | Why this episode | Per episode, from the archive and from Today (FR-741), with "Not quite right? Tell Salma". |
| **FR-1019** | P0 | Where do I stand | Not a page: asked of Salma (FR-846). |

## 11.3 Controls

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-1020** | P0 | A short sheet, not a settings app; everything else is a sentence to Salma ("less football", "talk slower", "more English from you"). It holds: drop time and the drop notification on or off; the podcast feed link (copy; reset) [OPEN-01]; captions on calls, transcript default in the player, default speed; keep my recordings on or off, and "delete all recordings"; help improve the teacher with my anonymized transcripts (off by default); gap note (edit, change the gap, turn off); plan (1, 2 or 3 a day), billing, and cancel in one tap; see all my data, export it, delete it; sign out; delete account. | C |
| **FR-1022** | P0 | Delete account takes two taps, with no survey wall and no "Karim will miss you". Cancel takes one tap. | TC-2 |

## 11.4 Data rules and security

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-1040** | P0 | **Voice storage on:** call and recording audio kept, encrypted with per-learner keys, until the learner deletes it or their account. | C (decision 9) |
| **FR-1041** | P0 | **Voice storage off:** audio is analysed and deleted within 15 minutes of the call (FR-343). The 4-weekly recording follows the same rule unless the learner keeps that one recording explicitly. | C (decision 9a); recording clause: PRD call |
| **FR-1042** | P0 | **Revoking voice consent:** the flag flips at once; all stored audio is deleted within 24 hours. | C |
| **FR-1043** | P0 | **Transcripts and text** are always stored while the account exists (core function, disclosed at consent). | C |
| **FR-1044** | P0 | **Opt-in data use:** only with the Controls switch on may anonymized transcripts (no audio) be used to check and improve the teacher. Off by default. Never sold, never used for ads. | TC-8, C (decision 9b) |
| **FR-1045** | LATER | **The learner's cloned voice** ("hear yourself say it fluently"): not offered in the beta; tested later as opt-in. | C (decision 9c) |
| **FR-1046** | P0 | **Export:** a full export (learner model in plain JSON, transcripts, kept audio) is prepared on request and a download link emailed within 1 hour. | TC-5; 1 hour: PRD call |
| **FR-1047** | P0 | **Account deletion:** access ends at once; data is purged from live systems within 24 hours and from backups within 30 days, as stated plainly in the privacy text. | TC-5; windows: PRD call |
| **FR-1048** | P0 | **Trial ended without paying:** new episodes stop; the archive, notebook, export and delete stay available for 90 days, then the account is deleted after one email warning. | PRD call |
| **FR-1050** | P0 | **Security:** encryption at rest and in transit; per-learner keys for audio, so deleting a learner's key deletes their audio; row-level isolation per learner; no cross-learner data paths except the shared gloss cache and anonymized, opt-in transcripts (NFR-301 to NFR-305). Hosting region pending the legal review (OPEN-05). | C |
| **FR-1051** | P0 | **Legal work before the paid beta** (OPEN-05), scoped by the countries the beta invites from: GDPR in the EU and UK, Saudi PDPL and other national privacy laws (consent wording, voice data, cross-border transfer, hosting region); California SB 243 (disclosure, crisis protocol, reporting); the EU AI Act's disclosure duties; subscription, cancellation and refund rules per country. Crisis resources are needed for every country the beta opens to. These are flags from the lenses, not legal advice. | L |

---

# PART 12 — LANGUAGE PACKAGES AND THE LANGUAGE GATE (FR-11xx)

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-1100** | P0 | Everything language-specific is configuration, not code. A **target-language package** and a **native-language package** are separate, so any native language can pair with any target. | D1 |
| **FR-1101** | P0 | **The language gate (five checks).** A target language opens when: (1) **voices**: 5 native listeners rate two-host episodes from the candidate vendors blind, and the winner is one most of them would listen to (FR-1330); (2) **learner speech**: on 30 real learner clips the verbatim transcript keeps the learner's errors instead of fixing them and catches words said in the learner's own language (FR-862); (3) **writing**: a native speaker reads 10 scripts and finds them natural and correct; (4) **the call**: the host answers within about a second on that language's speech stack (NFR-107); (5) **structures**: a structure inventory exists. A target that fails any check ships later, never with a weaker bar. | D1, C §8 |
| **FR-1102** | P0 | A **native language** ships when Salma's voice passes the blind test with 5 native listeners, its interface text, captions and glosses pass a native reviewer's check of 50 items, and its recognizer catches words said with the word button. | D1 |
| **FR-1103** | P0 | **A target-language package contains:** host bibles and voice pools per accent; the structure inventory and edit-classification rules; the 12 reporting categories; band descriptors and anchor examples; the calibration set; the frequency list, lemmatizer and chunk list; the word-check items; the then-and-now task bank; the ban list; sound design. | C |
| **FR-1104** | P0 | **A native-language package contains:** Salma's bible and voice; gloss prompts; caption prompts; the UI strings and text direction; crisis resources for the countries where it is spoken; the localized names of the 12 categories. | C |
| **FR-1105** | P0 | **Order of testing.** Candidate targets, in order: English, then Spanish, French, German, Italian, Portuguese, Japanese, Korean, Mandarin, Arabic, Hindi, Turkish and Russian (concept v2's estimate, not a test result). Native languages are tested in order of waitlist demand. The list is re-run whenever a vendor ships a new voice or recognizer model. | C §8 |
| **FR-1106** | P0 | **Proof claims per target.** English has an established structure inventory (the English Grammar Profile, OPEN-08). Other targets start with an inventory drafted by a model and checked by a native teacher. Until a target's calibration set is tagged, its learners get the show and the calls, and progress claims stay at first-ever events and words owned (FR-841). LAW-12 is never relaxed for a new language. | D1, LAW-12 |
| **FR-1107** | P0 | **Cost and closing rule.** Each target needs a host duo's bibles, a voice test, a recognizer test, an inventory review and a calibration set; each native language needs a Salma (bible and voice), interface translation and a reviewer. The beta opens the languages that pass by the end of build week 2 and adds others during the beta as they pass. A language whose "worth it" answers fall well behind English closes to new learners until fixed (GATE-M12). | C |
| **FR-1110** | P0 | **Milestone 0 is English only** as the target language (any native language), because episodes are checked by hand. The gate runs on other candidate targets during the beta build, and the beta opens in every language that passed. | D1 as applied; M0 kit |

---

# PART 13 — BILLING AND PLANS (FR-12xx)

| ID | Pri | Requirement | Source |
|---|---|---|---|
| **FR-1201** | P0 | **Trial:** 7 days, starting at account creation (FR-118), on the 2 a day plan, with no card. Payment is asked for once, plainly, on day 7 (one plain email on day 6, FR-240). | D2, Muath 2026-10-23 |
| **FR-1202** | P0 | **Plans:** 1 a day $19.99, 2 a day $29.99 ("Recommended", about $1 a day), 3 a day $44.99, monthly recurring, USD, tax added where required. The middle plan is marked "Recommended", not "Most popular", until that is true. Prices are set from the cost per session by the rule in NFR-402 (OPEN-06 to confirm). | D2 |
| **FR-1203** | P0 | **Founding members:** the first 100 paying learners keep their plan's price for as long as they stay subscribed. | C |
| **FR-1204** | P0 | **Checkout** through a merchant of record (OPEN-04): USD prices shown in local currency where the provider supports it; tax handled per country; cards, Apple Pay, Google Pay, PayPal and local methods (such as Mada) where the provider supports them; change plan from Controls; cancel in one tap. | PRD call (merchant of record) |
| **FR-1205** | P0 | **Plan changes** take effect at the next drop (upgrade) or the next billing date (downgrade), stated plainly at the moment of change; unused allowance is never refunded or carried. | PRD call |
| **FR-1206** | LATER | Regional prices for lower-income countries, and a cheaper listen-first plan, once there is data on where learners are. | C |
| **FR-1230** | P0 | **Pricing psychology, within TC-2:** three plans with the middle marked; the top plan as the anchor (2 and 3 a day cost the same per episode, so 1 to 2 is the obvious step); "about $1 a day"; the trial on 2 a day; a free sample episode before signup; the real comparison shown (a tutor costs about $160 a month for two lessons a week); founding members keep their price. | D2, C §8 |
| **FR-1231** | P0 | **Never:** fake countdowns, fake scarcity, hidden or hard cancellation, guilt, pre-ticked upgrades, or an upgrade prompt anywhere but the once-a-week line in FR-209 and Controls. | TC-2 |
| **FR-1232** | P0 | **Receipts and failures:** receipts by email; a failed payment gets one plain email and a 7-day grace period in which the show continues; after that, new episodes stop and the account behaves as in FR-1048. | PRD call |
| **FR-1233** | P0 | **Cancel** keeps the show running until the end of the paid period; afterwards FR-1048 applies. No win-back offers, no survey wall. | TC-2 |

---

# PART 14 — NON-FUNCTIONAL REQUIREMENTS (NFR)

## 14.1 Latency (NFR-1xx)

| ID | Pri | Path | Budget |
|---|---|---|---|
| **NFR-101** | P0 | First open to first sound (Salma) | Under 60 s |
| **NFR-102** | P0 | First open to the learner's first spoken target-language sentence | Under 5 min |
| **NFR-103** | P0 | Sample episode playable | Under 30 s |
| **NFR-104** | P0 | Pilot playback after the intake | Under 45 s |
| **NFR-105** | P0 | Dropped episode start | Under 2 s |
| **NFR-106** | P0 | On-demand episode (second of the day, swap, return) playable | Under 30 s, streamed |
| **NFR-107** | P0 | Host reply after end of learner turn | Under 1.5 s median, under 2.5 s at the 95th percentile; call connect under 3 s |
| **NFR-108** | P0 | Word-button answer | Under 2 s |
| **NFR-110** | P0 | Word sheet | Under 300 ms |
| **NFR-111** | P0 | Chat opener | Under 30 s |
| **NFR-112** | P0 | After-session pass and teacher update | Within 10 min of the call ending |
| **NFR-113** | P0 | Tomorrow's episode | Ready before the drop time; batch falls back to on-demand at drop time minus 90 min |

## 14.2 Reliability (NFR-2xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-201** | P0 | The learner always gets an episode at the drop time: pipeline failure ships the fallback episode (FR-422); teacher failure ships the rules-built brief (FR-740). |
| **NFR-202** | P0 | Live voice failure falls back to voice notes in the same thread (FR-342); no session is ever lost. |
| **NFR-203** | P0 | A voice vendor outage switches to the second voice vendor within the same day's production; two voice vendors are wired from the start, behind adapters. |
| **NFR-204** | P0 | Every pipeline step is a durable workflow step with a timeout and retries; a partial run never publishes a partial episode. |
| **NFR-205** | P0 | Audio position, article scroll and chat history survive app restarts and device changes. |
| **NFR-206** | P0 | A model, prompt or vendor upgrade never changes a host's voice or personality silently (FR-503) and never shows up as learner progress (FR-860). |

## 14.3 Security and privacy (NFR-3xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-301** | P0 | Encryption in transit and at rest for all learner data. |
| **NFR-302** | P0 | Audio is encrypted with per-learner keys; deleting the key deletes the audio. |
| **NFR-303** | P0 | Row-level isolation per learner; no cross-learner data path except the shared gloss cache and anonymized opt-in transcripts. |
| **NFR-304** | P0 | Audio deleted within 15 minutes when voice storage is off; all audio deleted within 24 hours after consent is revoked; live purge within 24 hours and backup purge within 30 days after account deletion. |
| **NFR-305** | P0 | Feed URLs carry an unguessable token, are excluded from podcast directories and can be reset by the learner [OPEN-01]. |
| **NFR-306** | P0 | Every model, voice and recognition call is logged with its cost and the learner-model version it read, in a tracing tool that holds no raw audio. |
| **NFR-307** | P0 | Hosting region and cross-border transfer follow the legal review (OPEN-05). |

## 14.4 Cost (NFR-4xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-401** | P0 | Cost per session (everything one episode cycle uses: the teacher's share, writing, fitting, editing, all audio, the call and round two, re-transcription, chat, the after-session pass and a quarter of the weekly proof) is measured from the first learner, traced per role, per vendor and per learner, and reported weekly next to the heavy-use outliers. |
| **NFR-402** | P0 | **The price rule:** no plan may lose money on a learner who uses every episode at the planning cost of $0.35 a full session. Assumptions to replace with beta data: about 15% of the price goes to tax and payment fees; typical learners use 60% of 1 a day, 50% of 2 a day, 45% of 3 a day. Break-even cost per session at full use: $0.57 (1 a day), $0.42 (2 and 3 a day). If either assumption is far off by week 4 of the beta, the prices are re-run with the same rule before public launch. |
| **NFR-403** | P0 | Beta budget about $0.60 per session (the current itemized estimate on the recommended stack is about $0.64; the architecture cost page is the authority for the numbers). First levers from day one: episodes at 5 to 6 minutes by default, batch for everything nobody waits on, the cheapest voice that passes the blind test. |
| **NFR-404** | P0 | **Stop line:** over $1.00 a session with no costed plan to reduce it. **Scale target:** $0.30 to $0.35 at 10,000 learners; the announced prices must work there. |
| **NFR-405** | P0 | A learner on 2 or 3 a day who uses every episode costs more than they pay until the cost falls below $0.42; with about 50 beta learners that is at most about $560 a month, accepted as research and tracked weekly (GATE-11). |
| **NFR-406** | P0 | Sample episodes cost at most $0.05 each and are rate-limited (FR-103). |

## 14.5 Quality and evaluation (NFR-5xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-501** | P0 | No prompt or model change ships to the host, writer, editor or analyst without the offline test suite (FR-437, P1) or, before it exists, a hand-tagged regression set from Milestone 0. |
| **NFR-502** | P0 | Monthly human audit of proof claims; false-claim rate under 5% (GATE-12). |
| **NFR-503** | P0 | Monthly human read of 10 random episodes per learner for errors, sameness and law breaks (FR-436). |
| **NFR-504** | P0 | Recognizer error tracked by first language from day one; a language whose quality falls well behind English closes to new learners until fixed (FR-1107). |
| **NFR-505** | P0 | Every "why this episode" reason is traceable to a learner-model record; every claim is openable to its evidence. |

## 14.6 Accessibility and internationalization (NFR-6xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-601** | P0 | Right-to-left layout for native languages written right to left; every text block sets its own direction from its content; mixed-direction bubbles render correctly. |
| **NFR-602** | P0 | Captions on calls, a word-synced transcript on episodes and read-aloud on articles, so every audio surface has a text route and every text surface an audio route. |
| **NFR-603** | P0 | The app is usable with one thumb on a phone during a commute: one hero, large buttons, the hold pad and word button reachable; no gesture overrides a system gesture. |
| **NFR-604** | P0 | Dark mode is first-class; every surface meets WCAG AA contrast in both themes. |
| **NFR-605** | P0 | Every native-language string, gloss and caption passes a native reviewer's check before the language opens (FR-1102). |

---

# PART 15 — AGENTS AND STACK: WHAT THE PRODUCT REQUIRES

The architecture documents own vendor choices, infrastructure and costs per role. This part states only what the product requires of them.

## 15.1 The roster (thirteen roles, eleven in the beta)

| ID | When | Role | Job | Model or code | Beta |
|---|---|---|---|---|---|
| **FR-1301** | Before | Teacher | Reads the learner model; targets, due words, arcs, the weekly mix, tomorrow's ideas, each brief, "why this episode" | Strongest reasoning model, batch | Yes |
| **FR-1302** | Before | Writer | Script, article, call brief, chat opener, recap, shadow lines | Strong creative model | Yes |
| **FR-1303** | Before | Fitter | Coverage, targets, new-word budget; sends failing sentences back | Code plus a small model | Yes |
| **FR-1304** | Before | Editor | The gate (FR-412 to FR-422) | Mid model from a second vendor, plus code | Yes |
| **FR-1305** | Before | Voice studio | Two-voice audio, read-aloud, timestamps, names, re-listen | Text-to-speech plus recognition | Yes |
| **FR-1306** | Before | Scout | Results and news for stored interests, shared per topic | Small model plus search | LATER |
| **FR-1307** | Live | Host | The call (FR-32x to FR-34x), the word button, the chat (FR-36x) | Fast mid model in a voice pipeline, same voice as the episode | Yes |
| **FR-1308** | Live and after | Producer (Salma) | Onboarding, life updates, "tell Salma an idea", the notebook, the weekly proof's voice, "why" and "where do I stand" when asked, fact corrections. Never corrects, never sends notes. | Conversational model with voice; strong text model for the proof | Yes |
| **FR-1309** | Live | Observer | Reads each learner turn and whispers to the host what to recast or draw out next turn | Small fast model | LATER (first addition after the beta) |
| **FR-1310** | After | Analyst | FR-801 to FR-802 | Small model with a fixed schema, checked by code | Yes |
| **FR-1311** | After | Memory keeper | Life facts with quotes, interests, goals, canon | Small model plus rules | Yes |
| **FR-1312** | Weekly | Proof producer | Scripts the proof and finale from gated claims; picks clips | Strong text model plus the voice studio | Yes, simple |
| **FR-1313** | Every 4 weeks | Recording rater | Rates the then-and-now recording, calibrated per pair | Calibrated model plus code metrics | Yes |

## 15.2 Rules the stack must satisfy

| ID | Pri | Requirement |
|---|---|---|
| **FR-1320** | P0 | **Code, not AI:** the review scheduler; the lexicon (lemmatizer, frequency list, word probabilities); the gloss cache; the coverage check; the similarity check; the claim gate; the edit classifier; the measures; the updater; cost tracing. |
| **FR-1321** | P0 | Live roles never write to the learner model; only after-session roles write, from the append-only log (FR-602). |
| **FR-1322** | P0 | Every vendor sits behind a thin adapter so a swap is configuration; two voice vendors are wired from the start; a vendor may be used for some languages only, because the shipped language list is whatever passes on the chosen stack (FR-1101). |
| **FR-1323** | P0 | The editor runs on a different vendor from the writer. |
| **FR-1324** | P0 | The call host uses the episode vendor's low-latency voice so the host sounds the same in the episode and the call; where that is impossible, the mismatch is tested in Milestone 0 (the day-7 check-in asks whether it matters). |
| **FR-1325** | P0 | A durable workflow engine calling model APIs directly; no agent framework in the production path. |
| **FR-1326** | P0 | Vendors known to be shutting down are not used; known price events (several Gemini 3.8 prices double on 2027-01-01) are visible in cost tracing. |

## 15.3 Vendor tests (P0, in the beta build's first two weeks)

| ID | Pri | Test | Protocol |
|---|---|---|---|
| **FR-1330** | P0 | Voices | For each candidate target, 5 learners of it and 5 native speakers rate the same two-host script from each of the 3 episode-voice vendors, blind, on naturalness, accent quality and "would you listen to this on your commute?". Same protocol, with 5 native listeners, for each native language's Salma voice. |
| **FR-1331** | P0 | Recognizers | The 30-clip test (FR-862). |
| **FR-1332** | P0 | Call latency | 50 scripted test calls; median host reply under 1.5 seconds after end of turn (NFR-107). |

---

# PART 16 — SUCCESS METRICS AND GATES

## 16.1 Beta gates (paid founding beta, 2026-12-23 to 2027-01-26)

| ID | Metric | Target | Stop and rethink |
|---|---|---|---|
| **GATE-01** | Trial to paid (any plan) | 30%+ | Under 15% |
| **GATE-02** | Paid on 2 or 3 a day | Watched, no target | |
| **GATE-03** | Active in week 4 (paid) | 40%+ | Under 25% |
| **GATE-04** | Sessions per active learner per week | 4+ | Under 2.5 |
| **GATE-05** | Learner's own speech per session | 4+ min | Under 2 min |
| **GATE-06** | The 4-weekly recording | Improves for most learners on accuracy, fluency or complexity | No measurable change |
| **GATE-07** | Accuracy on the learner's own targets by week 4 (the test of invisible correction) | Better for most learners | Flat for most learners |
| **GATE-08** | Second-month renewal | 60%+ | Under 40% |
| **GATE-09** | "Very disappointed" if For one disappeared | 40%+ | Under 25% |
| **GATE-10** | Cost per session | Under $0.60 | Over $1.00 with no plan |
| **GATE-11** | Margin by plan at measured use | At least break-even on every plan at typical use | A plan loses money at typical use |
| **GATE-12** | False-claim rate (monthly human audit of proof claims) | Under 5% | |
| **GATE-13** | Wrong memories | Under 1 in 100 callbacks | |
| **GATE-14** | New trials from referrals and forwarded samples | 30%+ | Under 10% |

If a gate fails, find which claim failed (the show is not wanted, the teacher is not felt, the price is wrong) before writing more code.

## 16.2 Quality and health measures (tracked from day one)

| ID | Measure | Why |
|---|---|---|
| **GATE-M01** | "Worth it" (weekly proof question) and regret | Liking, not just wanting |
| **GATE-M02** | Unprompted return: sessions started without the notification, and within an hour of the drop time | Pull without nagging; anchor stability |
| **GATE-M03** | Tomorrow chosen: share of sessions ending with a pick | Anticipation |
| **GATE-M04** | Weeks on rhythm (weeks, not days) | Habit |
| **GATE-M05** | Return within 14 days after a gap of 7+ days; median gap length | The return design works |
| **GATE-M06** | Retention at weeks 4, 12, 26 and 52 | The long game |
| **GATE-M07** | Delayed recall: target items correct 7+ days after first meeting them | Learning, not performance |
| **GATE-M08** | Targets that hold in the next 4-weekly recording | Cannot be gamed |
| **GATE-M09** | Huh? taps per minute and taps per 100 words, over 4 weeks | Comprehension and difficulty fit |
| **GATE-M10** | "How much did you follow?" one tap after some episodes, against predicted coverage | Level fit |
| **GATE-M11** | Word-button use per call, over weeks; errors on targets in the next calls after the form returned in episodes | Dependence shrinking; whether invisible correction works |
| **GATE-M12** | "Worth it" and false-claim rate per language; recognizer error by first language | Quality and fairness across languages |
| **GATE-M13** | Plan mix and share of each plan's allowance used | Whether the prices and the cost rule hold |
| **GATE-M14** | Notebook fact edits in week 1 | Whether the glass box builds trust |
| **GATE-M15** | Similarity score across each learner's episodes; monthly human read | Sameness |
| **GATE-M16** | Minutes per day: heavy-use outliers flagged | A warning light, never a goal |
| **GATE-M17** | Time to first sound; time to first spoken sentence | The first ten minutes |
| **GATE-M18** | Calls abandoned on the move; feed-to-call handoff | When to switch to native early (OPEN-01) |

## 16.3 Out of scope for the beta

Character creation and the six chassis · learner-made or guest hosts · the news scout and any current-events facts the learner did not supply · the observer in the call · languages that have not passed the gate · native apps (unless OPEN-01 says otherwise) · detecting the learner's own language without the word button · settings beyond the Controls sheet · referral programs and community · social sharing of proof clips (a learner may download their own tape) · the learner's cloned voice · real-life rehearsal on demand · bring-your-own-input episodes · a yearly plan · regional prices · exploration slots in targeting · "where do I stand" for skills not yet calibrated · ask-first glosses · employer and university seats · playback above 1.0× · any chart, percentage or level on any surface.

---

# PART 17 — OPEN ITEMS (COMPLETE LIST)

| ID | Item | Working default | Needed by | Who decides |
|---|---|---|---|---|
| **OPEN-01** | Web app plus private podcast feed, or native app, for the beta | Web app plus feed | 2026-11-18 | Muath |
| **OPEN-02** | First-session order (A1 to A10) and the suggested door order | As in FR-110 to FR-121, FR-302 | 2026-12-02 | Muath |
| **OPEN-03** | Who writes the host bibles (one duo per target) and Salma's (one per native language) | Milestone 0 drafts | 2026-11-18 | Muath |
| **OPEN-04** | Company and payment provider (merchant of record recommended) | None | 2026-12-02 | Muath |
| **OPEN-05** | Legal review scoped by the beta's countries: GDPR, PDPL and others, SB 243, EU AI Act, subscription rules; hosting region | None | Before 2026-12-23 | Muath with counsel |
| **OPEN-06** | Confirm the three prices or the rule behind them | $19.99 / $29.99 / $44.99 | Before 2026-12-23 | Muath |
| **OPEN-07** | Which countries the beta invites from | Waitlist demand within what legal clears | 2026-12-02 | Muath |
| **OPEN-08** | English Grammar Profile commercial-use permission, or another inventory source; native-teacher review of drafted inventories for other targets | Request pending | Build week 2 | Muath (a request to its publisher) |
| **OPEN-09** | External test choice | Duolingo English Test for English | 2026-12-23 | Muath |
| **OPEN-10** | Similarity threshold and recognizer confidence threshold | Cosine 0.85; threshold from the 30-clip test | End of Milestone 0 | Data |
| **OPEN-11** | Which target languages open, and which vendors per language | Tests | Build weeks 1 to 2 | Tests (FR-1330 to FR-1332) |
| **OPEN-12** | Private feed support in the podcast apps learners use | Beta observation | First beta cohort | Beta observation [OPEN-01] |

Settled and not reopened: the trial needs no card; there is no launch learner, language pair or recruitment fallback (D1); Salma's Arabic variety is part of the per-language voice test (FR-524). A question during the build that this document does not answer escalates before it is built.

---

# PART 18 — MILESTONE 0 AND THE BUILD SEQUENCE

## 18.1 Milestone 0, hand-made: 2026-10-24 to 2026-11-18 (running)

The pilot kit, scripts, protocols and day-by-day schedule live in [milestone-0/](milestone-0/) (start at 00-start-here.md). As of 2026-11-06, cohort A is on day 6 and cohort B on day 5 by that schedule; finales are Nov 14 and 15; blind rating and pre-pay close Nov 17; **the gate decision is Wed 2026-11-18.** What the PRD needs from it:

1. 15 learners for 14 days, recruited by hand; English as the target language (FR-1110); episodes written with model help and checked by hand; delivered by WhatsApp; calls on ElevenLabs Agents with patient turn-taking; every call hand-tagged with the planned structure inventory.
2. The pilot follows D3 where it touches the learner: no notes that correct, only "you mean..." in the call and the right forms in later episodes (the kit's "errors to echo").
3. Week-0 and week-3 recordings of the then-and-now task (FR-851); personal versus generic days alternated within each learner; one blind comparison against a human-made learner podcast.
4. **The gate:** 10 of 15 ask for the next episode unprompted; median 4+ sessions a week; 4+ minutes of their own speech a session; in week 2 most still choose tomorrow's episode and say the week was worth it; the week-3 recording is better, judged blind, on at least one of accuracy, fluency or complexity for most; personal days beat generic days; echoed-error rate falls from week 1 to week 2 for more than half of learners with data; 5 of 15 pre-pay.
5. **What the beta inherits:** the first calibration set, the 30 recognizer clips for English, test-retest pairs for standard errors, the similarity threshold, the first ban list, evidence on the call timing and on the episode-versus-call voice mismatch.
6. **If the gate fails,** find which claim failed before building. Revise the thesis, not the backlog.

## 18.2 Beta build: 2026-11-18 to 2026-12-22

| Week | Build | Requirements |
|---|---|---|
| 1 (Nov 18) | Vendor tests and the language gate per candidate target; event log and learner-model schema; lexicon and scheduler; language package skeleton; cost tracing | FR-1330 to FR-1332, FR-1101, FR-6xx, FR-720, FR-1100, NFR-401 |
| 2 (Nov 25) | Teacher, writer, fitter, editor and voice studio end to end for test learners in each language that passed; gloss cache; **the language list for the beta is fixed at the end of this week** | FR-7xx, FR-4xx, FR-371, FR-1107 |
| 3 (Dec 2) | Onboarding A1 to A10; the player; the word sheet; the feed and drop notifications [OPEN-01]; the three plans, checkout and plan changes | FR-1xx, FR-31x, FR-37x, FR-23x, FR-12xx |
| 4 (Dec 9) | The call pipeline with the word button, hold-to-talk and adaptive patience; "you mean..." recasts; voice-note fallback; chat | FR-32x to FR-34x, FR-36x |
| 5 (Dec 16) | After-session pass, memory keeper, notebook, Controls, simple weekly proof, first then-and-now recording, data rules, crisis resources per country; the sample-episode landing page in many languages; end-to-end run with Milestone 0 learners | FR-8xx, FR-10xx, FR-904, FR-851, FR-57x, FR-101 |

**Exit criteria for 2026-12-23:** every P0 requirement works in every language that opens; a measured cost per session; a costed path to $0.35 or less.

## 18.3 Paid founding beta: 2026-12-23 to 2027-01-26

About 50 invites a week into 7-day trials on the 2 a day plan, spread across the languages that passed; 20 to 30 English learners take the external test at week 0 and week 8. The beta starts over the year-end holidays, so the first week's numbers are read with that in mind; several Gemini 3.8 prices double on 2027-01-01, inside the beta. P1 requirements ship during it: round two, shadowing, the season finale with its then-and-now comparison, the full claim gate, the tape, the offline test suite, the dial-in experiment. **Switch to a native app early** if many calls are abandoned on the move or the feed-to-call handoff loses most learners (GATE-M18).

## 18.4 After the beta (direction, not spec)

Public launch worldwide in every language that passed, at the three plans, moving to the floor stack piece by piece with blind tests (months 4 to 6); native apps and paid acquisition after retention holds (months 6 to 9); each new language opens as it passes the gate, and regional prices with a cheaper listen-first plan come once there is data on where learners are (months 9 to 12); employer and university seats and human bridges (year 2).

---

# APPENDIX A — WHERE EACH PRD-v2 SECTION WENT

| PRD-v2 (3.1) | PRD v3 |
|---|---|
| 0.0 to 0.3 | Part 0 |
| 1.1 to 1.4 | Part 1: FR-001 to FR-011, LAW-01 to LAW-12, TC-1 to TC-8 |
| 2.1 to 2.4 | FR-101 to FR-126 |
| 3.1 to 3.10 | FR-201 to FR-240 |
| 4 | FR-301 to FR-307 |
| 5.1 to 5.7 | FR-310 to FR-372 |
| 6.1 to 6.8 | FR-401 to FR-437 |
| 7.1 to 7.10 | FR-501 to FR-580 |
| 8.1 to 8.6 | FR-601 to FR-645 |
| 9.1 to 9.9 | FR-701 to FR-741 |
| 10.1 to 10.14 | FR-801 to FR-862 |
| 11.1 to 11.3 | FR-901 to FR-921 |
| 12.1 to 12.7 | FR-1001 to FR-1051 |
| 13 | FR-1100 to FR-1110 |
| 14.1 to 14.4 | FR-1301 to FR-1332 (cost model moved to NFR-401 to NFR-406 and the architecture documents) |
| 14.5 | FR-1202, FR-1230, NFR-402 to NFR-405 |
| 15 | NFR-101 to NFR-113, NFR-201 to NFR-206 |
| 16.1, 16.2 | GATE-01 to GATE-14, GATE-M01 to GATE-M18 |
| 17 | Part 16.3 |
| 18 | Part 17, OPEN-01 to OPEN-12 |
| 19 | Part 18 |

# APPENDIX B — REQUIREMENTS WHOSE SUBSTANCE DIFFERS FROM PRD-v2

Everything not listed here is PRD-v2's rule re-stated with an identifier.

| ID | What changed | Reason |
|---|---|---|
| **FR-009**, FR-119, FR-232, FR-233, FR-302, FR-315, FR-320, FR-346, FR-902, FR-1020, NFR-305, OPEN-12 | Web app plus feed is now a **working default under OPEN-01**, not a decision. | Decision 7 was never answered by Muath; the UI lens and project memory keep it open. |
| **FR-110 to FR-121**, FR-302 | The first-session order and the suggested door order are a **working default under OPEN-02**. | Same: left open by the UI lens. |
| **FR-313** | "English throughout" became "the target language throughout". | D1; the sentence contradicted the multi-language rule. |
| **FR-812** | The stray "Salma" row in PRD-v2's measures table (10.3) is removed; Salma is specified in FR-520 to FR-524 only. | Editorial error in PRD-v2. |
| **FR-1307**, FR-1308 | The host and producer rows of the roster are rewritten as two clean rows (PRD-v2's 14.1 had them merged into one malformed row). | Editorial error in PRD-v2. |
| **FR-1110** | Milestone 0 is **English only** as the target language. | D1 as applied; the kit recommends it and the brief confirms it. |
| **FR-1205**, FR-1232, FR-1233 | New: plan-change timing, failed-payment grace period, cancel behaviour. | PRD-v2 left billing mechanics unstated; the backlog needs them. **[PRD call]**, vetoable. |
| **FR-402**, NFR-201 to NFR-206 | Reliability stated as requirements rather than scattered sentences. | Needed as acceptance criteria; no new behaviour. |
| **NFR-403** | The $0.64 estimate is kept but the architecture cost page is named as the authority. | The architecture thread owns the cost model. |
| **NFR-501**, NFR-6xx | New: a regression set before the offline suite exists; accessibility and right-to-left stated as requirements. | They were implied by PRD-v2's text; the design and engineering docs need them explicit. **[PRD call]**, vetoable. |
| **Part 18.1** | Milestone 0 status updated to "running" with the kit's gate list, including the echoed-error gate. | The kit added gate 8 on 2026-10-23; dates unchanged. |

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
| Language gate | The five tests a target language must pass to open (FR-1101) |
| Word button | Hold and say a word in your own language; the host gives it back in the target language |
| Recast | The host saying the learner's point back the natural way ("you mean..."), never marked as a correction |
| Producer | Salma: the face of the app in the learner's own language; onboarding, notebook, the proof's voice; never corrects |

---

**Reading rule.** Parts 1 to 16 are settled; build as written. **[PRD call]** marks a decision this document (or PRD-v2 before it) made that no source made: veto it now or it stands. Part 17 lists the only open questions, each with its working default. If a question during implementation is answered nowhere here, it escalates before it is built.
