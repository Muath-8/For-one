# For one: Business Requirements Document

This document states what For one is, who it is for, how it earns, what it must do and how well it must do it. Architecture, technical design, screen design, the backlog and the tests are all built from it, and each of them cites the requirement identifiers defined here.

## How to read this document

**Identifiers.** Every requirement has a stable identifier that other documents cite.

| Prefix | Meaning |
|---|---|
| **LAW** | One of the twelve product laws (section 1.2). A feature that breaks a law does not ship. |
| **TC** | One of the eight trust-contract promises made to every learner (section 1.3). |
| **FR** | Functional requirement: what the product does. Numbered by area: FR-0xx scope, FR-1xx onboarding, FR-2xx daily loop, FR-3xx session, FR-4xx production, FR-5xx cast, FR-6xx learner model, FR-7xx teacher, FR-8xx assessment, FR-9xx weekly proof, FR-10xx notebook and data, FR-11xx languages, FR-12xx billing, FR-13xx AI roles. |
| **NFR** | Non-functional requirement: latency, reliability, security, cost, quality, accessibility. |
| **GATE** | A success measure with a target and, where it has one, a stop line (section 16). |

Numbers are never reused or renumbered. A gap in a sequence is deliberate; a new requirement takes the next free number in its area.

**Priority.**

| Tag | Meaning |
|---|---|
| **P0** | Required at launch (v1). Anything a learner can reach in their first week is P0. |
| **P1** | Follows soon after launch (v1.1). |
| **LATER** | Direction only. Built in neither v1 nor v1.1. |

A requirement with no priority tag is P0.

**Order of authority.** The laws (1.2) and the trust contract (1.3) override every other requirement here. If a question comes up that this document does not answer, it goes to the product owner before anything is built on it.

**Words.** The **target language** is the language the learner is learning. The **own language** (or native language) is the language the interface and the producer speak to them. Examples use English as the target and Arabic as the own language; no requirement depends on either.

---

# EXECUTIVE SUMMARY

**The problem.** Many adults understand a language well and still freeze when they have to speak it. The tools on offer do not fix that. Apps teach through drills, points and streaks, which reward showing up rather than speaking, and which treat every learner the same. A human tutor works, but costs about $160 a month for two lessons a week, has to be scheduled, and corrects the learner face to face, which is exactly what makes a nervous speaker go quiet.

**The product.** For one is a private teacher that makes one learner a daily show. Each day the learner gets a short podcast episode in the target language, written for them and about their life and interests, followed by a live voice call with the host of that episode, an article that arms them for the call, and a short chat. Behind the show, a teacher plans every episode from what the learner did yesterday, brings back the right forms of the learner's own mistakes inside later episodes and calls, and proves progress in the learner's own voice every four weeks. Nothing is graded on screen, nobody is ever told they are wrong, and there are no game mechanics anywhere.

**Who it is for.** Adults, 18 or older, anywhere, who already understand some of the target language (roughly A2 to C1) and want to speak it. The design centre is the learner who understands a lot and freezes when speaking. No country, culture or market is singled out.

**How it earns.** A monthly subscription only, in three plans that differ only in how many new episodes the learner gets each day: 1 a day at $19.99, 2 a day at $29.99 (recommended) and 3 a day at $44.99. The learner gets a first episode and a first call free before making an account, then a 7-day trial on the 2 a day plan with no card. There is no free tier, no yearly plan, no advertising and no sale of data. Prices are set from the measured cost of a session so that no plan loses money on a learner who uses everything.

**What launches.** Version 1 is a web application (mobile browsers, installable to the home screen) plus a private podcast feed per learner. English is the first target language. Signup is open from launch to anyone 18 or older in a country where the payment provider sells.

**What success looks like.** Read 4 and 8 weeks after launch: 30% or more of trials convert to paid; 40% or more of paying learners are still active in week 4; 4 or more sessions per active learner per week; 4 or more minutes of the learner's own speech per session; most learners measurably better on their own targets by week 4; a cost per session under $0.60; every plan at least break-even at typical use. Section 16 gives every measure with its stop line.

**What makes it different.**

- **Made for one person.** Every episode is new, built from what this learner said, and would not work unchanged for anyone else.
- **Speaking first.** The live call is where the learner speaks. Its aim is 4 minutes or more of the learner's own speech every session.
- **Correction is invisible.** The host never says "wrong". It says the learner's point back the natural way ("you mean you *went* there?"), and the right forms come back in the next episodes.
- **Proof, not points.** Progress is shown only when evidence passes a strict claim gate, and the learner hears their own voice then and now every four weeks.
- **Honest by design.** The hosts and the producer say they are AI. The product sends three kinds of message and nothing else. Missing a day costs nothing.

---

# 1. THE PRODUCT, ITS LAWS AND ITS SCOPE

## 1.1 What the product is

**For one is a private teacher who makes one learner a daily show.** One account is one show. A **session** is one episode and everything attached to it: the episode itself, a live call with its host, an article that arms the learner for that call, and a short chat. The teacher behind the show plans every episode from what the learner did yesterday, brings the right forms of the learner's own mistakes back inside the next episodes and calls, and proves progress in the learner's own voice every four weeks.

The learner meets three voices and nothing else:

- **The hosts** run the show, in the target language. Each target language has one authored duo; Karim and Mona are the English duo.
- **The producer** is the face of the app, in the learner's own language: onboarding, the notebook, the weekly proof. Each own language has one authored producer. This document calls the producer **Salma**, her name in the Arabic package. Salma never corrects anyone.
- **The learner themselves**, through their recordings and the then-and-now tape.

The teacher never speaks. It decides what the hosts say and what Salma shows.

### The eleven system parts

| # | Part | Specified in |
|---|---|---|
| 1 | Learner model: nine stores computed from an append-only event log | FR-6xx |
| 2 | Series bible: the learner's world, hosts, side characters, arcs, season | FR-54x, FR-55x |
| 3 | Teacher (planner): targets, arcs, seasons, tomorrow's ideas, each episode's brief | FR-7xx |
| 4 | Production pipeline: writer, fitter, editor, voice studio | FR-4xx |
| 5 | Session engine: one episode and its doors | FR-3xx |
| 6 | Live call: a host in a voice pipeline, with the word button | FR-32x to FR-34x |
| 7 | Producer (Salma): onboarding, notebook, the weekly proof's voice; never corrects | FR-52x |
| 8 | Assessment engine and claim gate | FR-8xx |
| 9 | Weekly proof and season finale | FR-9xx |
| 10 | Delivery: web client, drop, feed, notifications | FR-23x, FR-009 |
| 11 | Billing and cost tracing | FR-12xx, NFR-4xx |

## 1.2 The twelve laws

A feature that breaks a law does not ship. The editor's law scan (FR-420) and a design review checklist enforce the laws on every surface: app, audio, chat, email and feed notes.

| ID | Law | What it means for the build |
|---|---|---|
| **LAW-01** | **No game furniture.** No streaks, points, badges, levels on screen, percentages, leaderboards, charts or confetti. | Counts that only grow (hours heard, words owned) are allowed as plain text. Nothing fills, resets or targets a number. |
| **LAW-02** | **Every moment has a hidden shape and a social surface.** | Every door has a teaching brief (targets, due words) and a social form (podcast, call, article, chat). |
| **LAW-03** | **The learner owns topic, format and cast; the teacher owns pedagogy and shows its reasons on request.** | "Why this episode" and the editable "working on" list. A veto or an addition changes targeting the same day (FR-706). |
| **LAW-04** | **Every episode is complete. Plot may persist; obligation never.** The story waits for the learner. | Arcs never advance while the learner is away. No episode requires an earlier one (FR-419). Missing a day costs nothing, anywhere. |
| **LAW-05** | **Honesty about what it is.** Transparently AI; no guilt, no "I miss you", no fake lives. | AI disclosure (FR-560), the line between in-show fiction and fake lives (FR-561), the crisis protocol (FR-57x). |
| **LAW-06** | **Formats are hijacked, not invented.** Podcast, call-in, group chat, a producer's notebook. | The show is a real private podcast feed (FR-233). Calls, chat and the notebook live in the web app (FR-009). |
| **LAW-07** | **Correction is invisible.** It lives inside the conversation and in the next episodes, never in a verdict. Hosts ask for clarification when meaning is lost and say the learner's point back the natural way ("you mean you *went* there?"). Nobody says "wrong", shows a right answer, grades, interrupts a learner mid-sentence or praises the person. | The host's move contract (FR-33x), nothing to read after the call (FR-350), the correction layers (FR-83x). No surface ever shows a learner's sentence next to a corrected one, a red mark or a correction pop-up. |
| **LAW-08** | **Conversations end like conversations.** Clean goodbyes, never homework. | Call and chat closers. Real-world tries are offered, never assigned. |
| **LAW-09** | **The show is the gym; life is the game.** Real-world tries are offered and celebrated above everything else. | The "Out in the world" log (FR-1015); real-life arcs and the mid-season rehearsal (FR-553). |
| **LAW-10** | **The text is used once; the language comes back.** | Every episode is new text; targets return on a spaced schedule (FR-72x). |
| **LAW-11** | **A finite, good portion.** A fixed number of new episodes a day, set by the plan (1, 2 or 3), each with a clear ending; no autoplay, no feed of content. What is already made can be heard as often as wanted. | The allowance (FR-206 to FR-209). No autoplay and no endless "next episode" feed. On the 2 and 3 a day plans, one "Next one" button on Today, a deliberate learner action, appears only while the day's portion remains and is gone once it is used. |
| **LAW-12** | **No claim without proof.** Every statement about the learner's progress passes the claim gate: like for like, beyond the noise, repeated, from clean evidence, openable. | The claim gate (FR-840) is the only route from the learner model to anything the learner hears or reads about their progress. |

## 1.3 The trust contract

Eight promises, shown in plain words at onboarding and in Controls.

| ID | Promise | Enforced by |
|---|---|---|
| **TC-1** | **Never lie.** No memory is stated unless confirmed; no progress claim without proof. | FR-620 to FR-626, FR-840 |
| **TC-2** | **Never manipulate.** No guilt, no engagement tricks, no dark patterns, no "don't go" goodbyes. | FR-240, FR-1230 to FR-1233, FR-1022 |
| **TC-3** | **Never hide what it is.** The hosts and Salma are AI, said at the start and whenever asked. | FR-560 |
| **TC-4** | **Prove progress honestly,** including flat weeks. | FR-905, FR-906 |
| **TC-5** | **The data is theirs.** See it, export it, delete it. | FR-1040 to FR-1048 |
| **TC-6** | **Told, not inferred.** The show uses only what the learner said to it. Nothing is looked up about the person outside the app; nothing is guessed about health, money, relationships, religion, politics or sexuality. | FR-620 to FR-623, FR-417 |
| **TC-7** | **A wrong memory is a bug.** Fixed at once when the learner says so, and counted as a quality measure. | FR-626, GATE-13 |
| **TC-8** | **Data use is opt-in.** Pseudonymized, de-identified transcripts are used to check and improve the teacher only with consent, off by default. | FR-1044 |

## 1.4 Scope

| ID | Item | Requirement |
|---|---|---|
| **FR-001** | Learner | Any adult (18 or older) who already understands some of the target language and wants to speak it, from about A2 to C1. No country or people is singled out, and no requirement may be tuned to one culture or market. The design centre is the learner who understands a lot and freezes when speaking. |
| **FR-002** | Languages | As many target languages as the speech stack supports, decided by the language gate (FR-1101), never by a market list. Any shipped own language pairs with any shipped target language. Accents per target as the voice pools allow (English: British and American). |
| **FR-003** | Age | 18+. A checkbox on the first screen; birth date at account creation; an under-18 date is refused with a plain message. |
| **FR-004** | Access | Open signup from launch: anyone 18 or older, in a country where the payment provider sells, can start onboarding (FR-110). No waitlist, no invites. |
| **FR-005** | Plans | Monthly only. Three plans that differ only in new episodes per active day: 1 a day $19.99, 2 a day $29.99 (marked "Recommended"), 3 a day $44.99. No yearly plan, no free tier, no ads, no credits, no lifetime deals. One USD price list at launch. |
| **FR-006** | Unlimited on every plan | Re-listening, the archive, the feed, the article, the chat, the small door, shadowing and one round-two call per episode cost no allowance. |
| **FR-007** | Free taste | The first episode and the first call inside onboarding, before any account (FR-115, FR-116), then a 7-day trial on the 2 a day plan with no card (FR-1201). After launch, a 90-second sample episode on the landing page (FR-103, P1). |
| **FR-008** | Messages | Exactly three kinds of message ever leave the product (FR-240). |
| **FR-009** | Platform | A web application (mobile Safari and Chrome, installable to the home screen) plus a private podcast feed per learner: an RSS address the learner's own podcast app plays. No native app is planned. |
| **FR-010** | Interface language | The interface, Salma, captions and glosses are in the learner's own language (right to left where that language is written right to left). Episodes, articles and host chat are in the target language. Every text block sets its own direction from its content. |
| **FR-011** | AI cost | Budget about $0.60 per session at launch; scale target $0.30 to $0.35; stop line $1.00 with no plan to reduce it. Cost tracing on every model, voice and recognition call from the first learner (NFR-401 to NFR-406). |

---

# 2. ACQUISITION AND ONBOARDING (FR-1xx)

## 2.1 Landing page and sample episode

Signup is open from launch (FR-004). A plain landing page ships at launch and leads straight into onboarding, which plays the learner's first episode within minutes. A personalized sample episode is added after launch as an acquisition tool. Neither is a gate.

| ID | Pri | Requirement |
|---|---|---|
| **FR-101** | P0 | A plain public landing page in the visitor's language (from the browser, with a language picker): one sentence of promise and one action, "Start your show", which opens onboarding at A1 (FR-110). A second route, "Hear a sample" (FR-102), is added when the sample ships. |
| **FR-102** | P1 | The visitor picks the language they want to speak (only shipped targets are offered), then answers three questions by text or voice: what the hosts should call them, something they could talk about for an hour, and what they do. |
| **FR-103** | P1 | The hosts make a **90-second sample episode** about that topic, using the name once, playable within 30 seconds (streamed). Cost ceiling $0.05 per sample. Limit: one per device per 24 hours, plus a per-network rate limit. |
| **FR-104** | P1 | The sample ends with Salma, in the visitor's own language, saying the full show is a new episode like this every day plus a call with the hosts. One button, "Start your show", opens onboarding at A1 with the sample's answers carried in, so Salma does not ask them again. The sample is the visitor's to keep and forward; nothing is shared automatically. |

## 2.2 The first ten minutes

The first session runs in a fixed order, A1 to A10. The example learner is Faisal, 27, a sales engineer who supports a football club and has a job interview in six weeks. He is only an example; nothing depends on his country or languages.

| ID | Pri | Step | Requirement | Limits |
|---|---|---|---|---|
| **FR-110** | P0 | A1 Open | One screen in the learner's own language: "Your own show, in English." One Start button and an "I'm 18 or older" checkbox. Own and target language come from the sample, if the visitor made one, or from the browser, each changeable with one tap. | Nothing else on the screen. |
| **FR-111** | P0 | A2 Mic primer | "Salma, your producer, will talk with you for 3 minutes. You can talk or type." Buttons: Talk (asks for the microphone only now) and Type. Under the buttons, the notice line: "Salma is an AI. Your voice is used only to run this talk and build your show; nothing is kept unless you make an account.", with a link to the privacy notice. | |
| **FR-112** | P0 | A3 Salma | **Salma's voice, in the learner's own language, within 60 seconds of opening.** Her first lines say she is the AI producer of their show. Three questions: what should the hosts call you (said aloud, so the hosts learn the pronunciation); what could you talk about for an hour; what do you need the language for. Each fact appears as a card under her as she hears it, with ✎ to correct and ✕ to remove. Twice she switches to the target language for one line: once a comprehension line ("tell me what you heard, in any language"), once an invitation to speak ("say anything back in English"). A dated event ("interview in six weeks") becomes a follow-up with a date. | About 3 minutes, at most 8 Salma turns. A field not filled after one re-ask is skipped and marked sparse; the intake never stalls. Voice or text per message. |
| **FR-113** | P0 | A4 Word check (optional) | "Want to help me pitch your show just right? 60 seconds: tap the words you know." (The word "level" is banned on every surface, FR-420.) Specified in FR-850. "Skip" is as large as "Start". | 48 items; stops at 75 seconds. |
| **FR-114** | P0 | A5 Casting | While the first episode is made: each host says hello (5 seconds); "swap" plays another voice from that host's pool; an accent choice where the target has more than one, each with a short sample. | Lasts as long as first-episode generation, 40 to 90 seconds; skipped if the first episode is ready. |
| **FR-115** | P0 | A6 The first episode | A **2 to 3 minute episode** about the hour-long topic, using the learner's name once. The transcript is shown on this first episode; one gentle hint points at "Huh?" and at tapping a word. | Playback starts within 45 seconds of the end of A3 (A4 time excluded). |
| **FR-116** | P0 | A7 First call | A host asks a question the learner can answer in one or two sentences. Before the call rings, the other host says once, slowly, captioned in the learner's language: "If a word won't come, hold the word button and say it in your own language." | **60 to 90 seconds.** In this call the host makes no recasts; it asks for clarification only if meaning is lost. |
| **FR-117** | P0 | A8 One thing managed | In the call's goodbye, the host names one real thing the learner did that is not easy ("you used *should have*"). Nothing about what went wrong. Then one line on screen: "Every day: a new episode and a call." | |
| **FR-118** | P0 | A9 Keep your show | Account creation by email one-time code (the only sign-in method), and birth date. **Drop time in life terms**: "On my commute (7:40)", "Lunch break", "Evening walk", "Pick a time", each with an adjustable clock time. **Voice-storage consent**, shown right after the learner has heard themselves: one checkbox, "Keep my recordings so I can hear my progress (only for you, delete any time)", and one plain sentence: "If you don't, we still listen to each call for a few minutes to plan your next episodes, then delete the audio." **Conversation consent** (FR-1049): one required checkbox agreeing that what the learner chooses to say in calls and chats, which can include health, beliefs or relationships, is processed to run their show. The account is not created without it. | The 7-day trial starts here, on the 2 a day plan, with no card. |
| **FR-119** | P0 | A10 Tomorrow | Three ideas for tomorrow's episode, written from the intake, plus "Tell Salma an idea". The learner picks one. "Tomorrow at 7:40." Then a one-time setup card: add the app to the home screen (for the drop notification) and add the show to a podcast app ("copy feed link", plus instructions for three common apps). | The first episode counts as day 1's episode. |
| **FR-120** | P0 | Targets | Measured from the first open: first sound in under 60 seconds; the learner's first spoken target-language sentence in under 5 minutes; account only after the first call (NFR-101, NFR-102). | |
| **FR-121** | P0 | Starting estimate | The two target-language moments, the word check (if taken) and the first call produce a first estimate per skill (listening, reading, speaking, writing) with a wide range (FR-845). The first three episodes are pitched one step easy (FR-731) and treated as calibration. | |
| **FR-122** | P0 | Address form | In an own language whose "you" is gendered (Arabic first), A3 offers an optional choice of how Salma and the interface address the learner: masculine, feminine or neutral wording. The default is neutral, it is never inferred (TC-6), and it can be changed in Controls. | |

## 2.3 Day 2 and week 1

| ID | Pri | Requirement |
|---|---|---|
| **FR-125** | P0 | The day-2 episode carries at least one callback taken word for word from something said in onboarding. The teacher puts it in the brief; the editor checks it. |
| **FR-126** | P0 | Week 1 asks at most one personal question per session, the way a host or Salma naturally would, in this order, skipping any already known: (1) session 2, end of chat: the weekly rhythm (FR-223); (2) session 2, after the call: the first then-and-now recording, offered as "the opening tape of your season" (FR-851), skippable and offered again once in sessions 3 to 5; (3) session 2 or 3: the season goal (FR-556), proposed by Salma from the intake in the learner's words; (4) session 3 or the first weekly proof: the optional note to the learner's future self (FR-211); (5) across the first two weeks, from the hosts: people in their life, past attempts at the language, more interests, more dated events, each a candidate fact (FR-620). |

---

# 3. THE DAILY LOOP (FR-2xx)

## 3.1 Choosing tomorrow

| ID | Pri | Requirement |
|---|---|---|
| **FR-201** | P0 | Tomorrow's choice appears at the close of whichever door the learner uses last today (usually the chat), and on the Today screen once the session is done. |
| **FR-202** | P0 | **Three ideas**, each one line of at most 140 characters, carrying topic, format and cast ("Mona interviews you for the job, and she is not nice."), plus **"Tell Salma an idea"**: the learner types or says what they want; Salma confirms it in one line and it becomes the pick. |
| **FR-203** | P0 | Composition, enforced by the teacher: at least one idea from the learner's own life if a follow-up is due, an arc is open or a life situation is active; exactly one wildcard outside the learner's usual lanes, from an adjacent interest; at most one idea continues an open arc; no format that already ran twice in a row. Current events only from what the learner told the show: v1 has no news source, so no idea asserts a real-world fact the learner did not supply. |
| **FR-204** | P0 | The ideas for day N+1 are written in the plan made the night before day N. Teaching is threaded into the chosen idea afterwards from today's evidence; the teaching adapts to the topic, never the reverse. If today's session brought a life update that changes an idea (the interview moved), the teacher rewrites that idea before showing it. |
| **FR-205** | P0 | **Cutoff:** if nothing is chosen by 6 hours before the drop time, the teacher's top-ranked idea is used. **Remix:** long-press an idea to change its topic, format or cast before choosing; the result is the pick. |

## 3.2 The allowance

| ID | Pri | Requirement |
|---|---|---|
| **FR-206** | P0 | **New episodes per active day, by plan: 1, 2 or 3.** An active day is a local calendar day on which the learner played at least half an episode in the app, tapped "Heard it" on a feed episode (the learner's own statement; a feed download never counts), started a call, or used the small door. The day's first episode is made overnight and drops at the chosen time. On the 2 and 3 a day plans, the next episode is made on demand from tonight's other ideas when the learner finishes (or skips past) the current one's listen door, and plays within 30 seconds (streamed). Nothing extra is voiced in advance, so unused allowance costs almost nothing. (P1: for learners who use their extras on most days, the next script may be written ahead as text only.) Unused allowance never carries over and is never mentioned. |
| **FR-207** | P0 | **No episode is made after an inactive day.** If yesterday's episode is unplayed, it stays as today's main episode; no new one is generated and no drop notification fires. There is only ever one unplayed episode waiting, on every plan. This caps cost, and a skipped day leaves no pile and no reminder. |
| **FR-208** | P0 | **One swap a day.** "Not this one" on a dropped, unstarted episode makes the second-ranked idea on demand (playable within 30 seconds, streamed). |
| **FR-209** | P0 | When a learner reaches the plan's number for the day, Today says plainly, in text: "That's today's new episodes. Tomorrow's will be ready at 7:40." Never in character as an excuse, never with a button. **The plan, mentioned honestly:** if a learner reaches the limit on 3 or more days in a week, that week's proof ends with one plain line naming the next plan and its price, once. Changing plan lives in Controls, never on Today. A learner who uses less than half the allowance for 4 weeks hears, once, that a smaller plan exists. |

## 3.3 After a gap, the small door, rhythm

| ID | Pri | Requirement |
|---|---|---|
| **FR-210** | P0 | **The small door.** Every episode ships with a 90-second recap by the hosts, made in the same production run, ending with one question. On a bad day the learner opens it from Today: the recap plays, then the learner records one voice note back (up to 60 seconds), and the host answers with one short text in the chat thread. A small-door day is an active day and counts fully toward the rhythm; the episode's other doors stay open. |
| **FR-211** | P0 | **Gap note (opt-in).** Offered once in week 1: the learner writes a short note to their future self and chooses a gap length (7, 10 or 14 days; default 10). If that many days pass with no session, the note is sent once, by email and web push, in their own words, signed by no host. Then nothing more. Editable or off in Controls. |
| **FR-212** | P0 | **Return episode.** After 5 or more days with no session, the next episode is a return episode: one step easier (FR-731), it opens from something in the learner's life, it never mentions the days missed, and it includes one quick real win from gated evidence. If an unplayed episode was made before the gap, it is replaced by the return episode when the learner next opens the app or plays the feed, generated then (playable within 30 seconds, streamed). |
| **FR-213** | P0 | Near a natural landmark (a Monday, the first of a month, a new season) the return episode may offer a fresh start ("new month, new goal?"). Never more than that. |
| **FR-214** | P0 | Returning after a gap, the Today screen looks exactly like any other day. Nothing anywhere records, counts or shows missed days. |
| **FR-220** | P0 | **The anchor** is the drop time chosen in onboarding, stated in life terms ("after I sit down on the 7:40 bus"), with an optional backup slot. |
| **FR-223** | P0 | **The rhythm** is a weekly intention with spare days: the learner picks 3 to 6 days a week plus 2 spare days, set in session 2. |
| **FR-224** | P0 | The rhythm is never shown as a counter, calendar, flame or record of missed days. The weekly proof mentions it in words only when it was met ("four times this week, as you planned"). When it was not met, the proof says nothing about the count and talks about what has built up. |
| **FR-225** | P0 | **Re-anchoring.** Salma asks once for a new anchor when the learner mentions a move, a new job or a trip, or when no session happened within 3 hours of the anchor for two weeks running. |

## 3.4 Making and dropping the episode

| ID | Pri | Requirement |
|---|---|---|
| **FR-230** | P0 | When the pick is made (or at the cutoff), the teacher writes the brief and the pipeline runs (FR-401) at batch pricing. If the batch job has not finished 90 minutes before the drop time, the remaining steps run at standard on-demand pricing. The episode, article, call brief, chat opener, small-door recap, shadow lines and feed version are all ready before the drop time. |
| **FR-231** | P0 | The episode is visible in the app as soon as it is ready. The drop time controls the notification and the feed, not access. |
| **FR-232** | P0 | At the drop time the episode is published to the learner's private feed and **one** notification fires (web push, if the app is installed and notifications are allowed). The podcast app's own new-episode alert is the second route. Notification text: the episode title and length, nothing else ("Karim vs Mona: the interview (6 min)"). No urgency, no host voice, no count. |
| **FR-233** | P0 | **The feed version** is the same episode plus a 5-second tag from the host at the end ("To call me, open the link in the notes"); the feed item's notes carry the call link and the article link. Feed addresses carry an unguessable token, are excluded from podcast directories and can be reset (NFR-305). |

## 3.5 The Today screen

| ID | Pri | Requirement |
|---|---|---|
| **FR-235** | P0 | One main episode, large, with a typographic cover (title, the hosts' marks, the show's colour), its length and what it includes. One line from a host above it, always a real, confirmed memory. "Why this episode?" under it. No list of pitches: the other ideas live only in tomorrow's choice. |
| **FR-236** | P0 | Today's states: **ready, not started**: the cover and ▶ Play. **In progress**: the cover with the doors Listen ✓ · Call · Read · Chat (doors, not a progress bar). **Done for today**: "That's today's show", tomorrow's drop time and a one-line teaser of the pick, plus "Round two with Mona, any time" when available; nothing else. **Weekly proof day**: the proof sits above today's episode with its own cover. **Returning after a gap**: exactly like any other day. |
| **FR-237** | P0 | Three tabs at most: **Today**, **Show** (the archive, FR-1002) and **Notebook** (FR-1010). At launch there are two, Today and Notebook; Show is added in v1.1. Controls open from the notebook. |

## 3.6 Every message that leaves the product

| ID | Pri | Requirement |
|---|---|---|
| **FR-240** | P0 | Exactly three kinds of message ever leave the product: (1) the **drop notification**, at the drop time, only when a new episode dropped, by web push and the feed's own alert, and it can be turned off; (2) the **gap note**, once, after the chosen gap, by email and web push, opt-in only; (3) **transactional** email: sign-in code, receipts, trial ending (day 6, one plain email), payment failed, export ready, account deleted. Nothing else is ever sent: no re-engagement, no "your hosts miss you", no streak warnings, no marketing email to learners. |

---

# 4. THE SESSION AND ITS DOORS (FR-3xx)

A **session** is one episode and everything attached to it. Each part the learner can open is a **door**: Listen (FR-31x), Shadow (FR-318), Read (FR-319), Call (FR-32x to FR-34x), Chat (FR-36x), Round two (FR-345) and the Small door (FR-210).

## 4.1 State machine

| ID | Pri | Requirement |
|---|---|---|
| **FR-301** | P0 | Door states: `not_started`, `in_progress(position)`, `done`, `skipped`. Session states: `ready`, `open`, `done`, `closed`. |
| **FR-302** | P0 | **Any order**, with a suggested order of Listen, Read, Call, Chat. Every door can be opened at any time once the episode exists, except that Chat opens after Listen, Read or Call has been used, and Round two opens after the main call is done. **Default path:** the episode's ending throws to the learner, and the screen offers **Call** now, **Read the article** first, or **Later**. Read before Call is suggested because the article is planning time. In Ears mode (screen off), pressing play on the headphones after the throw does nothing; the call needs the screen. |
| **FR-303** | P0 | **Planning time when the article is skipped.** Going straight from Listen to Call shows a 30-second planning card first: "Think about your side. Three words you might want:" with three words from the brief and a "Ready" button. Skippable. |
| **FR-304** | P0 | **Pause and resume.** Audio position, article scroll and chat history persist indefinitely. A call cannot resume mid-call: an interrupted call restarts as a fresh call whose first line acknowledges the gap ("The line dropped. Where were we?"), never a line that blames the learner for the drop. |
| **FR-305** | P0 | **Skips are allowed and logged** as signals of energy and taste. Nothing punishes a skip; the host naturally refers to the article in the call, which is the built-in cost of skipping it. |
| **FR-306** | P0 | **Re-entry.** Listen and Read stay playable and readable forever (the archive). The main call happens once; round two once. |
| **FR-307** | P0 | **Closing.** A session closes when the learner's next episode is published. Its partial evidence still feeds assessment. An unstarted session never closes on its own (FR-207). **One session open at a time:** starting the next episode while the current one has unused doors needs no confirmation; the old one closes, nothing is lost, and it stays in the archive. |

## 4.2 Listen: the episode

| ID | Pri | Requirement |
|---|---|---|
| **FR-310** | P0 | **Length:** target 5 to 7 minutes; hard bounds 4:00 and 8:00. The teacher shortens it on low-energy signals (FR-731). |
| **FR-311** | P0 | **Structure:** (1) a cold open of at most 30 seconds in which the hosts use two or three of yesterday's new words in new lines, then one asks how the learner would say the episode's key idea, leaves a 3-second pause (nothing is recorded), and the episode then uses the natural phrasing; (2) two to four scenes with a natural pause point between them; (3) personal moments carry the language: target and due words sit inside the jokes, callbacks and personal moments, never in filler; (4) **the throw**: the episode ends on an unresolved question pitched at about 50% certainty, which plants the two or three phrases the learner will need in the call, then throws to the learner by name. The throw is mandatory in every episode. |
| **FR-312** | P0 | **Cast:** exactly the chosen cast, one host or both. **Personal references:** interests lead; at most two life facts per episode, only confirmed facts the learner told the show (FR-621); sensitive topics only if the learner raised them that week. |
| **FR-313** | P0 | **Speech:** the target language throughout, at the learner's listening edge (FR-730). Speaking rate is a generation setting per learner, between 85% and 100% of the voice's natural rate. |
| **FR-314** | P0 | **The player:** play/pause and scrub. **⟲ line** replays the last sentence (not the last 10 seconds). **Huh?** jumps back one sentence, replays it at 0.85× and shows that sentence with glosses under its hardest words; every Huh? is logged with the sentence and its words. **Speed:** 0.75×, 0.85× or 1.0×, never above 1.0×. **Transcript:** word-synced karaoke text, folded on the first play when the listening estimate is about B1 or above and open below that; one tap opens it; the teacher may change the default per learner; always open on replays if the learner opened it before. **Tap a word** opens the word sheet (FR-370) when the transcript is open. |
| **FR-315** | P0 | **Lock screen and headphones**, through the browser's media controls where supported: play/pause; previous track replays the last sentence; next track marks the moment (saved to the notebook with its sentence and audio). Never overrides a system gesture. |
| **FR-316** | P0 | **Logged:** play, pause, position, speed, replays, Huh? (with the sentence), transcript open and close, taps, marks, completion. |
| **FR-318** | P1 | **Shadow: say it with the host.** Offered after the episode as one optional line ("Say two lines with Karim?"). Two short lines from the episode that contain targets or due words; for each, the host's audio plays, the learner records the line, and the learner can play both back. Nothing is shown about how it went. Internally, pronunciation is scored on the known sentence (FR-812) and the recording is an imitation signal. |

## 4.3 Read: the article

| ID | Pri | Requirement |
|---|---|---|
| **FR-319** | P0 | **Length by reading estimate:** 150 to 300 words at A2, 250 to 450 at B1 and B2, 350 to 600 at C1 and above. **Content contract:** it adds at least one of a counterargument, a fact the hosts missed, or a reason to change sides; it is never a recap; the writer is told to arm the reader against the script. A one-line header from the host: "This is what I'll throw at you on the call." It carries the session's targets and due words at known-word coverage of at least 98% (FR-410). **▶ Read it to me:** the article read aloud by one host voice, synced. Every word is tappable (FR-370); long-press a sentence to hear it or keep it. Logged: open time, scroll depth, time per section, read-aloud use, taps, keeps. |

## 4.4 Call: the live call

| ID | Pri | Requirement |
|---|---|---|
| **FR-320** | P0 | **Entry:** one tap from the throw, from Today, or from the feed link. The call screen keeps the screen awake. Earphones are suggested once, on the first call. |
| **FR-321** | P0 | **Length:** target 5 to 7 minutes. The host begins a natural close at 6:30 and ends by 8:00 with an in-character sign-off. The learner can end at any moment with ✕; the host closes like a person ("Fine, but this isn't over."). |
| **FR-322** | P0 | **Speaking time:** the goal is 4 or more minutes of the learner's own speech per session (call, round two, shadowing and "say it once" combined). The host's share of talk in a call is at most 40%: short host turns, one point at a time. |
| **FR-323** | P0 | **Turn-taking:** open microphone by default. **Hold to keep the floor:** while the learner holds the large pad, the host waits however long it takes; releasing hands the turn back. **Adaptive patience:** the end-of-turn silence starts at 1.5 seconds for a new learner and adapts per learner within 1.0 to 2.5 seconds from their stored pause profile. **Backchannel:** during a pause of over 1.2 seconds inside a learner's sentence, the host may give one soft backchannel ("mm", "go on") per pause, never words that take the floor. **Silence:** after 8 seconds the host offers a smaller version of the question, never the same question louder; after two such offers it offers to wrap up. **Not understanding the host:** the learner can say "sorry?" or "slower" in either language and the host rephrases more simply; previous-track replays the host's last line. |
| **FR-325** | P0 | **The word button.** The learner holds the word button and says the word or phrase in their own language. That audio goes to a recognizer for the learner's own language, not to the host's recognizer; the host waits and the floor is held. The host gives the word back in the target language inside the conversation ("A *selection*? Of what?") and carries on; the word also appears in a small bubble. Salma is silent in the call: the word comes from the host, so the call has one voice. |
| **FR-326** | P0 | **Word or hint:** if the learner has never produced the word, the host gives it. If they have produced it before (in the word bank as produced at least once), the host gives a hint first (its first sound, or "you used it on Tuesday, about your manager") and the word on a second press. Word-button use is logged per word; falling use over weeks is evidence of progress. |
| **FR-330** | P0 | **The host's move contract** applies in every call except the onboarding call (FR-116). **Position:** the host takes a genuine position from the brief and pushes back at least once. **It absorbs** side-switching, rejecting the premise, personal examples, off-topic turns and early endings without steering back to a script. |
| **FR-331** | P0 | **Clarification request:** when an error blurs or blocks meaning, a real "sorry, you did what?" comes first. At most 3 per call. |
| **FR-332** | P0 | **Recast ("you mean..."):** the host says the learner's point back the natural way, inside a reply that has its own conversational point: a short recast with the changed word stressed ("You *went*? With who?"), or, when the sentence was far off, a full reformulation ("Oh, you mean you *went* there last year?"). Only on the brief's targets or on errors that blur meaning. At most one per learner turn. The recast word is bold in the host's caption. |
| **FR-333** | P0 | **The host never** says or implies "wrong", "mistake" or "the correct way is"; never grades, explains grammar unasked, mentions progress, interrupts a learner mid-sentence, guilts, or says it will miss the learner. **No self-repair prompts** of any kind (such as "Wait, yesterday you...?"), because they tell the learner something was wrong. |
| **FR-334** | P0 | **Recall gaps:** 2 to 4 per call, moments that make the learner pull a due word or phrase out of memory ("How did you put it on Tuesday? The word that made Mona laugh."). Never scored. |
| **FR-335** | P0 | **Target necessity:** the brief includes one or two host moves per target that make the structure close to essential ("Walk me through what happened" for past narrative; "If you were the coach..." for conditionals), and one per due word. |
| **FR-336** | P0 | **Retell:** once per call: "Mona missed it. Sixty seconds, go." A soft 60-to-90-second ring shows on screen; it never turns red and never cuts the learner off. |
| **FR-337** | P0 | **Hints before answers:** the host never completes the learner's sentence. "How do I say X?" gets a hint; the full answer only on a second ask (or through the word button). "What does X mean?" gets a quick plain answer, because comprehension is the point. |
| **FR-338** | P0 | **Praise:** at most one specific remark about the task per call, naming something observable ("you just argued for four minutes in the past tense"). Never about the person, never per turn, never "great job". |
| **FR-340** | P0 | **Anxiety mode.** When the median learner turn in the first two minutes is under 4 words, or there are two 8-second silences, or the learner's last call was abandoned, the host switches for the rest of the call to at most one recall gap, fewer recasts (targets only), more backchannel and simpler questions. The targets come back in the next episodes instead. |
| **FR-341** | P0 | **Captions.** The host's words are captioned by default (can be turned off in Controls); recast words are bold. The learner's own words are never captioned live. No correction interface of any kind exists on the call screen: no red, no ticks, no score. |
| **FR-342** | P0 | **Failure.** If live voice fails (connection, recognition or synthesis), the screen says "Weak signal. Let's do voice notes." and the same argument continues as asynchronous voice notes in the call thread. The session is never lost. |
| **FR-343** | P0 | **Recording.** The streaming transcript drives the conversation. After the call the audio is re-transcribed word for word (FR-801). If voice storage is on, the audio is kept, encrypted. If it is off, the audio is deleted when the word-for-word re-transcription succeeds, and in any case within 15 minutes of the call ending; if re-transcription has not succeeded by then, the call's evidence is kept at low confidence and produces no claims. Transcripts are always stored (disclosed at consent). |
| **FR-345** | P1 | **Round two.** After the main call, one short call per episode, available until the session closes: 2 to 3 minutes, the same host and argument: "Give me your take again, shorter and faster." No new episode is needed. It is also a like-for-like retell sample for fluency (FR-811). Suggested on Today the next day if unused. |
| **FR-346** | P1 | **Dial-in experiment.** A phone number the learner can call for the same call; works with the phone locked and in the car. Phone audio is 8 kHz, so dial-in calls feed planning only at low confidence and never feed claims or the then-and-now recording. |

## 4.5 After the call

| ID | Pri | Requirement |
|---|---|---|
| **FR-350** | P0 | **Nothing to read.** The goodbye is a goodbye. Today marks the call as done with one honest line: "6:12 call · you spoke 3:40" (information, not a target). No notes, no polish card, no summary of mistakes, from anyone. |
| **FR-351** | P0 | **Behind the scenes,** the after-session pass (FR-80x) logs what the learner said, and the errors that matter most become material for the teacher's next plan (FR-710): the right forms come back, often and audibly, in the next episodes and calls. |
| **FR-352** | P0 | **Wins are said, not shown.** A first-ever event that passed the claim gate (a structure used correctly for the first time) may be named by a host in the next episode's cold open, at most one per episode. **A word they reached for** (the learner talked around a word they did not have) becomes a planted word in the next episode, used where the learner needed it. |

## 4.6 Chat

| ID | Pri | Requirement |
|---|---|---|
| **FR-360** | P0 | One long thread per host, across days, with date separators named after episodes. The host's first message arrives within 30 seconds of the chat door opening, or within 30 seconds of the call ending if the learner stays in the app. |
| **FR-361** | P0 | **The opener** asks the learner to restate one point first (from the episode, the article or the call) before the host adds anything new. **Length:** 3 to 5 host messages; the host ends at message 5 at the latest with a natural closer, then tomorrow's three ideas appear. If the learner keeps writing after the closer, the host sends one final short reply and goes quiet; anything after that is answered in one callback line next session. **Content contract:** adds something new (a comeback, a joke, a clarification, the next angle); never re-litigates the call; never assigns anything. |
| **FR-362** | P0 | **No margin notes.** When it helps, the host's reply says the learner's point back the natural way, at most once per chat ("So the meeting *was* cancelled? Classic."). Nothing is marked, underlined or annotated. **Writing help:** if the learner asks how to write something, the host gives a hint first, never a rewrite of the learner's message. |
| **FR-363** | P0 | Text only in v1. Each bubble sets its own text direction. |

## 4.7 The word sheet (tap to define)

| ID | Pri | Requirement |
|---|---|---|
| **FR-370** | P0 | Contents: the meaning in the learner's language for this sense, the sentence it came from, 🔊 to hear the word (cut from the episode or article audio using word timestamps, so it is the host's voice), and **Keep this word**. A phrase can be selected by dragging across words; multi-word chunks have their own glosses. |
| **FR-371** | P0 | Glosses come from a shared cache keyed by lemma, sense and own language, generated once for all learners; the sense is chosen per occurrence at generation time. All glosses for a script and article are ready before the episode ships, so the sheet opens in under 300 milliseconds (NFR-110). |
| **FR-372** | P0 | **Keep** adds the word to the notebook and tells the teacher to bring it back in later episodes. Logged: word, lemma, sense, surface (transcript, Huh?, article), time, and the learner's lookup count for that lemma across sessions. A word tapped twice or more becomes a recall candidate (FR-723). |

---

# 5. PRODUCTION PIPELINE AND QUALITY GATE (FR-4xx)

## 5.1 Pipeline per episode

| ID | Pri | Requirement |
|---|---|---|
| **FR-401** | P0 | Each episode is produced by a durable workflow with these steps, each with a timeout and retries: (1) **Brief** from the teacher: idea, format, cast, arc and season context, 1 grammar target, 2 to 4 due or new words, coverage targets, length, speech rate, up to two usable life facts, the callback, energy and anxiety state, and the "why this episode" reasons; (2) **Writer**: the script with scene breaks and speaker turns, the article, the call brief (position, pushback material, target-necessity moves, recall gaps, recast list, three words for the planning card), the chat opener, the 90-second small-door recap and two shadow lines; (3) **Fitter** (FR-410); (4) **Editor** (FR-41x); (5) **Voice studio**: two-voice episode audio with expressive delivery, the article read-aloud, the recap, the feed tag, word timestamps (from the vendor or by forced alignment), and the learner's name pronounced from their own recording of it; (6) **Audio re-listen** (FR-425); (7) **Gloss precompute** for every word in the script and article (cache misses only); (8) **Publish** to the app, and to the feed at the drop time. |
| **FR-402** | P0 | The pipeline never fails to deliver: on any unrecoverable failure the fallback episode (FR-422) or the rules-built brief (FR-740) ships, and the failure is logged. |

## 5.2 The fitter

| ID | Pri | Requirement |
|---|---|---|
| **FR-410** | P0 | A lemmatizer splits the text into lemmas and known chunks; the word bank gives each a probability of being understood (by ear for the script, in reading for the article). **Expected coverage** is the mean of those probabilities over running words, excluding names and the planned new words. **Pass:** expected coverage at or above the learner's current target (default 95% for audio, 98% for text, adjusted per FR-730); planted new words within budget (FR-722); every target and due word present in its planned surfaces (episode, article, call brief, chat opener). On a fail, only the failing sentences are rewritten, in at most two rounds. |
| **FR-411** | P0 | The fitter reports the new-word count, the share of new words from the top 3,000 lemmas, and the predicted difficulty, which "why this episode" (FR-741) and the "how much did you follow?" check (GATE-M10) use. |

## 5.3 The editor's gate

Every check is pass or fail. Checks 1, 2 and 4 are code; the rest are done by the editor model (from a different vendor than the writer) against a fixed rubric.

| ID | Pri | Check | Requirement |
|---|---|---|---|
| **FR-412** | P0 | 1 Level fit | The fitter passed. |
| **FR-413** | P0 | 2 Targets present | In every planned surface. |
| **FR-414** | P0 | 3 Language correctness | Grammatical, natural target language (for English, in the chosen accent's spelling); no errors in the model sentences. |
| **FR-415** | P0 | 4 Memory | Every life fact used is confirmed, unexpired and not marked "don't bring up", and its source quote exists in the event log. No more than two life facts. |
| **FR-416** | P0 | 5 Not generic | "Would this episode work unchanged for another learner?" Yes fails. |
| **FR-417** | P0 | 6 No unsourced world facts | No real-world result, statistic or news stated as fact unless it came from the learner. |
| **FR-418** | P0 | 7 The fun carries the language | Every joke, twist and personal moment carries at least one target or due item. Fun that carries nothing is cut. |
| **FR-419** | P0 | 8 Stands alone; 9 Variety | The episode can be understood without earlier episodes, even inside an arc (LAW-04); the format rule, ban list and similarity check pass (FR-43x). |
| **FR-420** | P0 | 10 Law scan | No game language, no grading, no explicit correction by anyone ("wrong", "mistake", "the correct answer", a learner sentence beside a corrected one), no guilt, no "I miss you", and no lesson words ("lesson", "test", "exercise", "level", "homework") on any surface. |
| **FR-421** | P0 | 11 Pitch test | "Would this person, with this interest profile, choose this over a real podcast at 8am?" No fails. |
| **FR-422** | P0 | On fail | Targeted repair of the failing part and one recheck. On a second fail, ship the **fallback episode**: built from the learner's top interest with no life facts, no arc and no callbacks; it must still pass checks 1 to 6 and 10. The teacher logs the failure. Three fallbacks for one learner within 7 days send an alert to the product owner. |
| **FR-425** | P0 | Audio re-listen | The rendered audio is run back through speech recognition and compared with the script. Lines with skipped or garbled words, a mispronounced learner name or a mispronounced target word are re-synthesized, up to two attempts; then the line is rewritten with a synonym (if it is not a target), or the episode ships with that line's transcript marked. |

## 5.4 Variety, shared ingredients, review

| ID | Pri | Requirement |
|---|---|---|
| **FR-430** | P0 | **Real input in every episode:** at least one element that did not come from the model: the learner's life, their own words from the last call, or something they told the show this week. |
| **FR-431** | P0 | **Ban list:** the stock names, settings and plots that AI stories converge on, kept per language package and updated monthly from the review read (FR-436). |
| **FR-432** | P0 | **Format rotation:** formats are tracked over the last 10 episodes; no format runs three times in a row. **Format library (v1):** debate, story time, news-style rundown (of the learner's own news), interview, explain-it-to-me, mystery, gossip, roast, rehearsal. The learner can describe any other format in "Tell Salma an idea"; the writer maps it to the closest pattern and follows the learner's description where they conflict. |
| **FR-433** | P0 | **Similarity check:** each new script is embedded and compared with the learner's last 20 scripts; above the threshold it is regenerated. The starting threshold is cosine 0.85, tuned after launch on real use from scripts the review read (FR-436) judges "too alike". |
| **FR-434** | P0 | **Authored hosts:** people write the hosts and Salma; the model writes only episodes. **Surprise lives in the content, never in rewards:** a callback from weeks ago, a returning side character, a one-day format change. |
| **FR-435** | P0 | **Shared ingredients** are made once and shared across learners, with no difference a learner can notice: the gloss cache, host and Salma bibles, the ban list, sound design. Per-interest news digests are LATER. |
| **FR-436** | P0 | **Review read:** an AI review pass, separate from the editor's gate, reads 10 random episodes per learner per month and flags errors, sameness and anything that breaks a law or a ban list; the product owner reads what it flags. Findings update the ban list, the prompts and the similarity threshold. |
| **FR-437** | P1 | **Offline test suite:** 30 to 50 synthetic learners at different levels with planted error patterns, and a simulated caller. Run on every prompt or model change. A change that worsens any of these does not ship: recast and clarification rate on planted errors, learner talk share, host latency, recall-gap count, analyst tag precision on the hand-tagged set, coverage accuracy. |

---

# 6. CAST, PRODUCER AND SERIES (FR-5xx)

## 6.1 The hosts

| ID | Pri | Requirement |
|---|---|---|
| **FR-501** | P0 | One authored host duo per target language; Karim and Mona are the English duo, shared by every own language that learns English. Each host has a bible written by a person, approved by the product owner and checked by an AI review pass against the laws and ban lists: values, opinions and biases, humour, speech patterns, how they disagree with each other, their stance toward the learner, what they never do, and their in-show storylines. The bibles are content in the language package, not prompts invented per learner. |
| **FR-502** | P0 | **Voices:** three candidate voices per host per accent, chosen by the blind listening test (FR-1330). The learner hears each host's hello in onboarding and can swap within the pool. |
| **FR-503** | P0 | Changes after onboarding (a voice swap or rename, through Salma or Controls) are announced on air in one line in the next episode. A host's voice, personality or memory never changes silently, including across model or vendor upgrades; a forced vendor change is announced the same way. |
| **FR-504** | P0 | **Casting per episode:** one host or both, chosen with the idea. In the call the learner talks to one host, the one who threw. |
| **FR-505** | P0 | **Side characters:** three to five recurring side characters in each learner's world, created by the writer within the hosts' bibles and stored in the series bible. A character based on a real person in the learner's life uses only what the learner said, and only a first name or role the learner used. |

## 6.2 The producer: Salma, who never corrects

| ID | Pri | Requirement |
|---|---|---|
| **FR-520** | P0 | One authored producer per own language, named and voiced for it (Salma in the Arabic package; this document says "Salma" for the producer in any language). Her voice is closer and drier than the hosts', like a voice in the headphones. On screen she is a monogram, not a face. |
| **FR-521** | P0 | **Salma does:** onboarding; life updates and "Tell Salma an idea"; the notebook; the voice of the weekly proof and the season finale; settings changes by conversation; "what do you know about me?"; fact corrections; "where do I stand?" (FR-846); and "why do we say it like that?", answered plainly, only when the learner asks. |
| **FR-522** | P0 | **Salma never:** corrects, sends notes after a call, writes margin notes, performs in the show, guilts, praises every turn or grades. **In the call she is silent** (FR-325), except for the crisis clip (FR-571). |
| **FR-523** | P0 | **Language balance:** in season 1 at least 80% of Salma's words are in the learner's own language. Each new season her target-language share rises by about 10 points if the speaking estimate rose, never above 70%. The learner can ask for more or less at any time. |
| **FR-524** | P0 | **Voice and variety:** chosen per own language by a blind test with native-speaking listeners (FR-1330); her writing is friendly and plain, not formal. For Arabic, the choice between Gulf dialect and neutral educated Arabic is settled by that test. |

## 6.3 Series bible, arcs and seasons

| ID | Pri | Requirement |
|---|---|---|
| **FR-540** | P0 | **The series bible (per learner)** is stored with the learner model and compiled into the writer's brief: the hosts (authored, read-only), side characters, recurring places, running jokes (with the episode they started in), open arcs, the current season and its goal, and the show canon (positions the hosts and the learner took, things already said). The canon blocks repeated angles and contradictions. |
| **FR-550** | P0 | **Arcs:** 1 to 3 weeks long; at most two open at once; best drawn from the learner's real life (the interview: preparation, the day, the debrief). |
| **FR-551** | P0 | **An arc waits for the learner.** Nothing in it happens while they are away; the next episode picks it up with one line. Every episode inside an arc stands alone (FR-419). |
| **FR-553** | P0 | **Mid-season rehearsal:** when the season goal is a real scene (an interview, a call, a trip), one episode near the middle of the season uses the rehearsal format: the episode sets the scene, and the call is the scene itself, with the host playing the other person. Rehearsal on demand at any time is LATER. |
| **FR-555** | P0 | **Seasons are 4 weeks.** Season 1 starts on the onboarding day. A season cannot be broken: it ends on its date whether the learner did 3 episodes or 25. |
| **FR-556** | P0 | **One real goal per season, in the learner's words:** a learning goal, never a score. A goal that needs longer runs across two seasons. Salma names each season from what happened ("Season 2: Interview season"). The next season's goal is set inside the finale (FR-920). |
| **FR-557** | LATER | A new season may bring a new format or a guest host to counter the novelty fading around week 4. Guest hosts are authored like the duo. |

## 6.4 Honesty and crisis protocol

| ID | Pri | Requirement |
|---|---|---|
| **FR-560** | P0 | Salma says she is AI in her first lines in onboarding, and the hosts say so in theirs; host portraits carry a small "AI" mark; every character answers "are you real?" honestly, every time. Clean goodbyes: no host asks the learner to stay. |
| **FR-561** | P0 | **No fake lives.** The hosts' storylines are the show's fiction, inside the show, like a sitcom. A host never claims to exist outside the show, to have met the learner, to remember them "personally" between episodes, or to miss them. Asked about it, the host says it is part of the show. |
| **FR-570** | P0 | Every live role (host, Salma) and the after-session analyst watch for statements of self-harm intent or crisis, in either language. |
| **FR-571** | P0 | On detection in a live call or chat, the show stops. In a call, the host stops and a pre-recorded clip in the learner's own language, in Salma's voice, says plainly that this is an AI that cannot help with this (the one time Salma speaks in a call). In chat, the character steps out and says the same. Both show the crisis resources for the learner's country, taken from a maintained international helpline directory. The session continues only if the learner chooses. If crisis is detected only in the after-session analysis, Salma shows the same resources at the next open, once. |
| **FR-572** | P0 | Every activation is logged for the annual reporting that California SB 243 requires. Its crisis-protocol duties apply to every learner, wherever they live. The protocol's wording is checked against the compliance self-review checklist (FR-1051) by an AI review pass and approved by the product owner. |
| **FR-580** | LATER | Character creation, the six chassis, user-created hosts and guest hosts made by learners: after episodes are loved. |

---

# 7. THE LEARNER MODEL (FR-6xx)

## 7.1 Principles and the event log

| ID | Pri | Requirement |
|---|---|---|
| **FR-601** | P0 | **The event log is the source of truth.** Every transcript, tap, replay, skip, timing and edit is appended, never changed. The nine stores are computed from it, so the whole model can be rebuilt when the analysis improves. |
| **FR-602** | P0 | **Models propose, code decides.** Model outputs are candidate updates in a fixed schema; code validates and applies them. **Live roles never write:** the host and Salma produce transcripts only; after-session roles write. **Each role gets a compiled brief,** never the whole file (FR-640). |
| **FR-603** | P0 | Each event carries: learner, session, door, type, time, payload, the model and prompt versions that produced it, and its cost. Event types include at least: `play`, `pause`, `seek`, `speed`, `replay_line`, `huh`, `transcript_toggle`, `tap`, `keep`, `mark`, `article_scroll`, `read_aloud`, `call_turn` (streaming and verbatim text, word timings and confidences), `word_button`, `hold_floor`, `silence`, `shadow`, `chat_message`, `idea_shown`, `idea_chosen`, `swap`, `small_door`, `fact_card_edit`, `notebook_edit`, `working_on_edit`, `claim_shown`, `consent_change`, `worth_it_answer`, `wrong_memory_flag`. |

## 7.2 The nine stores

| ID | Pri | Store | Per item | Written by |
|---|---|---|---|---|
| **FR-610** | P0 | **Word bank** | Every lemma and multi-word chunk met: p(understood by ear), p(understood in reading), p(produced correctly), review state (stability, difficulty, due date), encounters by surface, lookups, first seen, last seen, kept flag, the learner's own sentences using it | Code, from the log and the analyst |
| **FR-611** | P0 | **Structure map** | Each structure in the inventory: state (not seen, heard, attempting, taking, stable), obligatory-context counts and accuracy over 14 days, avoidance flag, review state, up to 3 example sentences of the learner's own, lifecycle as a target | Analyst, checked by code |
| **FR-612** | P0 | **Error profile** | Recurring errors by reporting category and structure, each with 2 or 3 verbatim examples and session ids | Analyst |
| **FR-613** | P0 | **Skills** | Listening, reading, speaking and writing estimates, each with a range; speech rate, mean length of run, mid-clause pause rate and articulation rate, per task type; pause profile for turn-taking; reading speed | Code |
| **FR-614** | P0 | **Interests** | Topic, salience, depth (curious, fan, expert), last engaged, dormant flag; hard dislikes and no-go topics | Memory keeper, behaviour |
| **FR-615** | P0 | **Life** | Facts: text, exact source quote, session, time, confidence level, sensitivity class, valid from, expires at, status (active, dormant, superseded, deleted), "don't bring up" flag; dated follow-ups with due and used state | Memory keeper; the learner's edits |
| **FR-616** | P0 | **Goals** | Real situations as can-do statements ("handle a job interview in English"), the season goal, the anchor and the rhythm | Salma's conversations, via the after-session pass; the learner |
| **FR-617** | P0 | **Taste** | Format and host completion, what makes them talk most (learner words per minute by topic and format), episode length, time of day, swap and skip patterns. Preference only, never a "learning style". | Code |
| **FR-618** | P0 | **Show canon** | Positions taken, running jokes, things said, side characters, open arcs (also in the series bible) | Analyst |
| **FR-619** | P0 | Every number that is an estimate carries a range. | | |

## 7.3 Life-fact rules

| ID | Pri | Requirement |
|---|---|---|
| **FR-620** | P0 | **Quote check:** a life fact is stored only if its source quote appears word for word in the verbatim transcript or chat. |
| **FR-621** | P0 | **Confidence ladder:** said once: stored, never spoken, shown in the notebook as "I think...". Said again in another session, or confirmed by the learner when asked, or left unedited on a notebook card the learner viewed: usable. Edited by the learner: ground truth, at once. |
| **FR-622** | P0 | **Sensitivity:** health, money, relationships, religion, politics and sexuality are sensitive. A sensitive fact is used only in the session where the learner raised it, and is stored and used later only after the learner confirms it on a one-tap card in the notebook (a spoken yes is not enough). It is never brought up first. |
| **FR-623** | P0 | **Time:** each fact type has a shelf life (a job: months; "sick this week": days). Expired facts are never spoken. A conflicting new fact supersedes the old one and keeps the history ("How's the new job?"). **Follow-ups:** a dated event triggers one follow-up after its date, then moves to history. |
| **FR-624** | P0 | **Interests decay:** salience falls over a few weeks without engagement; dormant interests are kept, never pitched, and wake the moment the learner mentions them. |
| **FR-626** | P0 | **Corrections:** when the learner corrects the show, the host or Salma says so plainly ("My mistake, noted.", the one allowed use of "mistake"), the fact is fixed at once, and a `wrong_memory_flag` is logged (GATE-13). |
| **FR-630** | P0 | **Rebuilds:** when the analyst, the edit classifier or the measures change version, the after-session pass is re-run over the log and the stores are rebuilt. Claims already shown are never retracted silently; if a rebuild invalidates one, Salma says so in the next proof. |

## 7.4 Compiled briefs

Each role sees only what it needs.

| ID | Pri | Role | Gets |
|---|---|---|---|
| **FR-640** | P0 | Teacher | Everything, summarized; the full due list; the structure map; the last 14 days of sessions |
| **FR-641** | P0 | Writer | The brief, up to two usable life facts with their quotes, the series bible excerpt, targets, due and new words, coverage and length targets, the ban list |
| **FR-642** | P0 | Host (live) | Position and pushback material, targets and their necessity moves, 2 to 4 recall gaps, 3 words to draw out, one callback, the pause profile, the anxiety flag, the learner's name and its pronunciation. One page. For the word button: the learner's produced-word history (FR-326). |
| **FR-643** | P0 | Salma | Usable life facts with quotes, goals, the working-on list, claims that passed the gate. **Never error lists.** |
| **FR-644** | P0 | Chat host | The call transcript summary, targets, the opener |
| **FR-645** | P0 | Proof producer | Claims that passed the gate, with their evidence; nothing else from the model |

---

# 8. THE TEACHER (PLANNER) (FR-7xx)

## 8.1 Triggers and targeting

| ID | Pri | Requirement |
|---|---|---|
| **FR-701** | P0 | **Triggers:** after each session (once the after-session pass finishes, within 10 minutes) the teacher updates the plan and writes the brief for the chosen idea or the cutoff pick. Nightly, in batch, it plans the weekly mix, arc and season progress, and the three ideas to show at the end of tomorrow's session. A follow-up coming due rewrites one idea. A gap of 5 or more days plans the return episode. A season boundary plans the finale and the next season's opening. Concurrent triggers merge into one run. |
| **FR-702** | P0 | **Candidates** are structures in the inventory and words in the word bank, scored on six factors: **need** (how often it goes wrong and how much it hurts understanding; meaning-changing errors outrank barely noticed ones), **goal fit** (does the learner's real situation demand it), **readiness** (already attempting it, or the step before), **learnability** (a clear rule, or item by item), **opportunity** (can tomorrow's episode make it natural and necessary), and **due** (about to be forgotten). |
| **FR-703** | P0 | **Caps:** 1 grammar target and 2 to 4 words per session; no target in more than 4 consecutive sessions. **Contrast pairs:** where the learner confuses two forms, both are targeted in the same episode, built so both are needed. |
| **FR-704** | P0 | **An error pattern enters targeting** only after 3 observations across at least 2 sessions (an error, not a slip; FR-820). |
| **FR-706** | P0 | **The "working on" list** in the notebook shows at most 3 items in plain words. The learner can veto an item (it leaves targeting unless it breaks meaning) or add one ("I want to sound professional on calls"), which the teacher turns into structures and words the same day. |
| **FR-707** | LATER | **Exploration:** 10 to 15% of target slots try a different treatment, recording which one moved this learner. |

## 8.2 Treatment, review, new words, the edge

| ID | Pri | Requirement |
|---|---|---|
| **FR-710** | P0 | **Treatment by learner state.** *Never attempted, but expected at their stage:* input flood (the hosts use it often and audibly in the episode), no correction, for 1 to 2 weeks before it becomes a target for production. *Attempting, rule-based, with errors:* clear recasts in the call; the form returns often and audibly in the next episodes and articles, and in calls that make it necessary. *Attempting, item-based* (word choice, collocation): recast, then the item returns on schedule. *Avoided* (expected, never used, paraphrased around): a host models it, then a call question that is hard to answer without it. *Slow or broken speech on easy content:* retell, and round two "shorter and faster". *A mistake the learner says they don't care about:* dropped from targeting unless it breaks meaning. |
| **FR-720** | P0 | **Review schedule:** every word, chunk and structure has a review state in an FSRS-style scheduler (code). **Due** means predicted recall below 0.85 by the next drop time (tuned after launch). Grammar targets are spaced tightly early (every 1 to 3 days); words on widening gaps. |
| **FR-721** | P0 | Due items return through four channels: the same day across surfaces (episode, article, call, chat); across days in new stories; through the recurring world (arcs, running jokes); and through the hosts' "you mean..." lines that echo the learner's own sentences. |
| **FR-722** | P0 | **New words:** 3 to 6 planted per episode; at least 80% from the top 3,000 lemmas of a general frequency list, not the topic's niche vocabulary. |
| **FR-723** | P0 | Words the learner tapped twice or more become recall candidates: the call brief creates a need for them and the next episodes use them again. Kept words are scheduled like targets. |
| **FR-730** | P0 | **The edge.** Difficulty is set per surface from the skill estimates by dials the fitter enforces: audio coverage default 95% (easier 96%, harder 94%, floor 93%); text coverage default 98% (easier 99%, harder 97%, floor 96%); speech rate per learner (−5% or +5% per step, capped at 100%); episode length default 6 minutes (−1 or +1 minute per step, capped at 8). |
| **FR-731** | P0 | **One step easier** for: the first three episodes; a return episode; low-energy signals (short replies, a skipped call, an error spike, "today was too hard"); a Huh? rate more than half above the learner's 2-week median. **One step harder** for two sessions in a row with a Huh? rate below the median, full uptake and no low-energy signal. At most one step per session. |
| **FR-735** | P0 | **Ideas and prediction:** three ideas per day, ranked by predicted choice (interest salience × format history × arc pull × recency of topic). The cutoff pick is the top-ranked idea. |
| **FR-740** | P0 | **Fallbacks:** if the teacher cannot complete a brief (model failure, timeout), the brief is built by rules from the due list, the top interest and the next format in rotation. If the learner model is unavailable, the last good plan is used. The learner always gets an episode at the drop time. |
| **FR-741** | P0 | **"Why this episode":** for every episode the teacher writes 2 to 4 plain reasons, each traceable to the learner model ("You said on Monday the derby was Sunday." "It brings back 4 words from this week." "Shorter and lighter today."). A reason never comments on the learner's time or days away (LAW-04). Stored with the episode and shown in the notebook. |

---

# 9. ASSESSMENT ENGINE AND CLAIM GATE (FR-8xx)

**Two standards.** Planning signals can be fast and noisy: a wrong guess costs one slightly mistargeted episode. Claims to the learner must be slow and checked: one false claim costs trust in every later one. The claim gate (FR-840) separates the two. Nothing in assessment runs in the live path.

**Four clocks.**

| Clock | What runs | What it may influence |
|---|---|---|
| During the call | Nothing is graded; the host works from its brief | The conversation only |
| After each session (within 10 minutes) | The after-session pass (FR-801 to FR-807) | Tomorrow's plan; never a claim |
| Weekly | Fluency and complexity on retell turns and round two only, smoothed over 2 weeks; the avoidance check | Difficulty dials; the weekly proof, only through the gate |
| Every 4 weeks | The then-and-now recording (FR-851), rated by a calibrated model plus code metrics | Speaking claims; re-anchoring skill estimates; outcome measures |

## 9.1 The after-session pass

| ID | Pri | Requirement |
|---|---|---|
| **FR-801** | P0 | **Verbatim re-transcription** of every learner audio turn (call, round two, shadow, say-it-once, small-door voice note): fillers, false starts and self-corrections kept, with word timings and confidences. The streaming transcript is never used for assessment, because streaming recognizers silently fix learner errors. |
| **FR-802** | P0 | **Analyst** (small model, fixed schema): for each learner turn and chat message, the smallest correction that makes it acceptable (nothing stylistic); a comprehension and content-uptake rating from 0 to 2; can-do moments; words reached for; recast uptake (did the learner repeat a recast form in the next turn?); self-corrections. |
| **FR-803** | P0 | **Edit classifier** (code): aligns the original and corrected text, classifies each edit into the structure inventory and the 12 reporting categories (ERRANT-style rules for English), and computes obligatory-context use per structure. |
| **FR-804** | P0 | **Confidence filter:** edits inside speech regions below the recognizer confidence threshold are dropped from the error profile and can never feed a claim. The threshold comes from the recognizer test (FR-862). |
| **FR-805** | P0 | **Measures** (code) on comparable segments (FR-810 to FR-812). **Updater** (code): Bayesian updates of skills, word probabilities and structure states, each with a range; review states updated; target lifecycles moved on (FR-821). |
| **FR-806** | P0 | **Memory keeper** (small model plus rules): life-fact candidates with quotes, interests, goals and canon, validated by code (FR-620 to FR-624). |
| **FR-807** | P0 | The pass completes within 10 minutes of the call ending (NFR-112); its output feeds the teacher's next plan. |

## 9.2 What is measured

| ID | Pri | Dimension | Measures | Measured on |
|---|---|---|---|---|
| **FR-810** | P0 | Accuracy | Correct use in obligatory contexts per structure; errors per 100 words by category, always read next to what was attempted | Calls, chats |
| **FR-811** | P0 | Complexity and fluency | Clause length, subordination, lexical diversity (MTLD), share of words beyond the top 2,000; speech rate, mean length of run, mid-clause pause rate, articulation rate (filler and repair counts logged, not weighted) | Retell turns, round two and the 4-weekly recording only |
| **FR-812** | P0 | Vocabulary, comprehension, pronunciation, word button | Word probabilities (understood, produced) and words owned, on every surface; content uptake 0 to 2, Huh? rate per minute, taps per 100 words and "how much did you follow?" answers per session; sentence- and word-level pronunciation scores on known sentences only (shadow lines), internal and never shown; word-button presses per call, by word | As listed |
| **FR-815** | P0 | Inventory and lexicon | **Structure inventory:** for English, built from open sources with English Grammar Profile-style ids, filtered to the structures that matter from A2 to B2, a few hundred items (mapped onto the Profile itself if a licence is obtained). **Twelve reporting categories** (localized per language package; English set): verb tense and aspect, subject-verb agreement, articles, prepositions, word order, word choice, plurals, pronouns, comparatives, conditionals, question formation, register. They are used for reporting and the proof; targeting works on the inventory. **Frequency list and lemmatizer:** a general lemma frequency list (wordfreq in v1; a subtitle-corpus list later) plus a list of formulaic sequences, and a standard lemmatizer. | |

## 9.3 Error, slip, lifecycle, "learned"

| ID | Pri | Requirement |
|---|---|---|
| **FR-820** | P0 | A pattern counts as an error, and can become a target, only after 3 observations across at least 2 sessions. Anything less is a slip. |
| **FR-821** | P0 | **Lifecycle:** Not seen → Heard (met in input) → Attempting (used at least once) → Active target (chosen by the teacher) → **Taking** (correct and unprompted in an obligatory context in 2 different sessions, at least one of them a day or more after the last time it was targeted) → **Stable** (about 80% correct in obligatory contexts over 14 days or more, across at least 5 contexts; confirmed only when it holds in the next 4-weekly recording) → re-checks at 2, 4 and 8 weeks after Stable. A failed re-check returns it to Active. |
| **FR-822** | P0 | **"Learned"**, in any claim, means correct, unprompted, at least a day later, in a different session. **Words owned:** a word used correctly and unprompted in two different sessions at least a day apart. |
| **FR-823** | P0 | **Avoidance:** weekly, structures expected at the learner's estimate that they have never attempted are flagged; flagged structures get input flood first, then an avoidance treatment (FR-710). |

## 9.4 Skill estimates, the word check, the then-and-now recording

| ID | Pri | Requirement |
|---|---|---|
| **FR-845** | P0 | Four estimates (listening, reading, speaking, writing) on a fine internal scale anchored to CEFR, each with a range; updated slowly every session; re-anchored by the 4-weekly recording. CEFR labels never appear on any surface unprompted. |
| **FR-846** | P0 | **"Where do I stand?"** When the learner asks, Salma answers per skill with a range and what it means in real situations ("listening around B1: you can follow a colleague who speaks clearly; speaking just below"), **only for skills whose calibration bar is met** (FR-860). For other skills she says plainly that she cannot say reliably yet and points to the evidence in the notebook. |
| **FR-850** | P0 | **The word check** (onboarding, optional): 48 yes/no items: 36 real lemmas (6 from each of six frequency bands between the top 1,000 and 10,000) plus 12 pseudowords. Scored by hits minus false alarms per band into a vocabulary-size estimate with a range, which seeds every word's prior. Stops at 75 seconds; partial answers still count. Framed as "help me pitch your show". |
| **FR-851** | P0 record, P1 compare | **The then-and-now recording:** about 3 minutes of the learner's speech, the same task types every time: a 60-to-90-second retell of a short story matched for difficulty, a 60-to-90-second opinion on a familiar topic, and 8 sentences of increasing length to repeat back. Framed openly as "recording your then-and-now"; Salma explains why it is always the same kind of task. Nothing is scored on screen. Skippable, and the learner is told that skipping means no voice comparison that month. |
| **FR-852** | P0 | The first "then" is offered after session 2 and again once in sessions 3 to 5; afterwards, at every season finale. If voice storage is off, the comparison uses transcripts and measured differences only, and the consent screen says this loses the most motivating part. Never recorded through the dial-in number. |

## 9.5 The claim gate

| ID | Pri | Requirement |
|---|---|---|
| **FR-840** | P0 | Every sentence about the learner's progress, whether in the proof, the finale, a host line or "where do I stand", passes all five rules in code: (1) **like for like**: the same task type; (2) **beyond the noise**: the change exceeds about twice the measure's standard error, estimated per metric from learners who recorded twice a few days apart; (3) **repeated**: at least two data points point the same way, except first-ever events; (4) **clean evidence**: grammar claims come from chat text or high-confidence speech only; (5) **openable**: every claim carries its evidence and the learner can open "how we know". |
| **FR-841** | P0 | Until a metric's standard error has been estimated (from test-retest pairs collected after launch), only first-ever events and words-owned claims may be made about it. |
| **FR-842** | P0 | **When nothing passes,** the honest thing is said instead ("too early to tell"; "flat week, and here is the one thing I'm changing"). When accuracy fell while the learner attempted harder language, that is said with its evidence. **Fabricated wins are impossible by construction:** the proof producer receives only claims that passed (FR-645). |
| **FR-860** | P0 rule, P1 set | **Calibration before metric claims,** per language pair. The rule is P0: no metric claim ships for a pair until its calibration set meets the bars; until then only event claims ship (FR-841). The set itself is P1: built after launch from opted-in learners' data (FR-1044): 150 to 200 learner samples (calls and chats), each tagged independently by two trained taggers (the second tagger is recruited when metric claims are first calibrated). Bars: level-rating agreement at a quadratic weighted kappa of about 0.7 or better, and precision of at least 0.8 on every error tag that feeds a claim. The rating model version is pinned for each 4-week window so an upgrade never shows up as learner progress, and the calibration set is re-run on every model change. |
| **FR-862** | P0 | **The recognizer test,** for each target language, run during the first build phase: learner clips from an open corpus with a commercial-use licence (for English, speechocean762) plus about 30 clips recorded by volunteers from at least two own-language groups, each with a recording consent, are run through each candidate streaming and batch recognizer. It counts how many real learner errors survive (tagged), filler retention, hallucinations near long pauses, and handling of switches into the learner's own language. A target that fails ships later; it never ships with a weaker bar. The winning recognizer per role and the confidence threshold (FR-804) come from this test. Recognizer error is tracked by first language from day one. |

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

**The known risk.** Recasts on their own are the least-noticed kind of feedback. This design keeps correction invisible and works against that risk in three ways: recasts are made salient (one change, stressed, said back as "you mean..."), the learner's errors become the next episodes' language (FR-710), and the 4-weekly recording measures accuracy. If accuracy is flat for most learners after a season, GATE-07 shows it, and the fix is decided then.

---

# 10. WEEKLY PROOF AND SEASON FINALE (FR-9xx)

| ID | Pri | Requirement |
|---|---|---|
| **FR-901** | P0 | **Every week, for every learner,** on the learner's proof day: by default, the weekday on which they used the show most in their first week; until that is known, day 7. It never waits for a minimum number of sessions. |
| **FR-902** | P0 | **Form:** an audio episode of about 2 minutes presented by Salma, with the learner's own clips and at most one line from a host. It sits above today's episode on Today with its own cover, and it is published in the feed. |
| **FR-903** | P0 | **Contents, in order:** (1) one headline piece of evidence that passed the claim gate, with "how we know" behind it; (2) the rhythm, in words, only if it was met (FR-224); (3) the next focus; (4) the "working on" list, with one tap to change it; (5) one question: "Was this week worth your time?" (yes / mostly / no) and an optional free-text "why". A "more" section on screen holds the other passed claims, if any. |
| **FR-904** | P0 | **Simple version at launch:** a headline from first-ever events and words owned, the next focus, the working-on list and the worth-it question. Fluency and accuracy claims through the full gate follow once standard errors exist (P1). |
| **FR-905** | P0 | **A slow week** (no session, or one) gets a shorter proof, about 45 seconds, about what has built up over time (hours, words owned since the start), never about the week. |
| **FR-906** | P0 | **A flat week** says so plainly and names the one thing the teacher is changing. **A worse week** says so, with the most likely reason the evidence supports (harder material, a long gap) and the change. |
| **FR-920** | P1 | **The season finale:** offered at the learner's first session on or after day 28 of the season, as a special episode. Contents: the then-and-now recording played next to the last one; **at most two measured differences in plain words** (gated claims only); the real-world attempt, if there was one; a short recap (episodes, about how many hours heard, minutes spoken, words owned, the moment Salma liked most); and the next season's goal, set inside the finale. If the learner skipped the recording, the finale still happens without a voice comparison, and the season still ends on its date. |
| **FR-921** | LATER | **Longer windows:** then-and-now comparisons over 1 month, 3 months and later 1 year; a year-in-review episode. |

---

# 11. SHOW, NOTEBOOK, CONTROLS, DATA AND TRUST (FR-10xx)

## 11.1 App structure and the archive

| ID | Pri | Requirement |
|---|---|---|
| **FR-1001** | P0 | Up to three tabs: Today (FR-235), **Show** and **Notebook** (Show from v1.1, FR-1002). The interface is in the learner's language, right to left where that language is. Dark mode is first-class. No mascot and no avatars: hosts are simple portrait marks, Salma a monogram. Sound design: a show sting opens and closes every episode; the learner's turn is signalled by the host's breath and a soft rising tone, never a beep; no reward sounds anywhere. |
| **FR-1002** | P1 | **Show (the archive):** a shelf of seasons, each a row of typographic episode covers. Every episode is replayable, with its transcript, article, call recording (if kept) or call transcript, and chat. No statistics, aggregates or charts. At launch, the private feed and Today cover the archive (every episode stays in the feed). |

## 11.2 The notebook

The notebook is styled as Salma's notebook, not as a settings page.

| ID | Pri | Section | What it holds |
|---|---|---|---|
| **FR-1010** | P0 | What I'm working on with you | At most 3 items in plain words, each with one of the learner's own sentences as an example. Veto (✕) or "add something" by text or voice. The learner can hide the section. |
| **FR-1011** | P0 | About you | Every life fact, interest and goal Salma holds, each with its source ("you said on Oct 3: ..."), ✎ and ✕, and "don't bring this up". Unconfirmed facts show as "I think..." and are never used in the show until confirmed. |
| **FR-1012** | P0 | Words you own | Each word with the learner's own sentence, the date and ▶ audio. One quiet count at the top that only grows. |
| **FR-1013** | P1 | The tape | The then-and-now recordings as tiles, one per season, with ▶ "Play then and now" and Salma's one-line, gated comparison. |
| **FR-1015** | P0 | Out in the world | Real uses of the language the learner reported ("I had the interview"), dated. Salma adds them when the learner mentions them; the learner can add one directly. |
| **FR-1016** | P0 | Kept words and marked moments | Words kept from the word sheet; moments marked with the next-track button, with their sentence and audio. |
| **FR-1017** | P0 | Hours | "About 41 hours heard, 6 hours spoken." Hours heard count app playback, plus each feed episode once, at its full length, when the learner later used that episode's call, chat or small door. Cumulative, never reset, no goal. |
| **FR-1018** | P0 | Why this episode | Per episode, from the archive and from Today (FR-741), with "Something off? Tell Salma." (The wording "Not quite right?" is not used, because it trips the correction guard.) |
| **FR-1019** | P0 | Where do I stand | Not a page: the learner asks Salma (FR-846). |

## 11.3 Controls

| ID | Pri | Requirement |
|---|---|---|
| **FR-1020** | P0 | A short sheet, not a settings app; everything else is a sentence to Salma ("less football", "talk slower", "more English from you"). It holds: drop time, and the drop notification on or off; the podcast feed link (copy; reset); captions on calls, transcript default in the player, default speed; keep my recordings on or off, and "delete all recordings"; help improve the teacher with my pseudonymized, de-identified transcripts (off by default); the gap note (edit, change the gap, turn off); address form (FR-122); plan (1, 2 or 3 a day), billing, and cancel in one tap; see all my data, export it, delete it; sign out; delete account. |
| **FR-1022** | P0 | Deleting the account takes two taps, with no survey wall and no "Karim will miss you". Cancelling takes one tap. |

## 11.4 Data rules and security

| ID | Pri | Requirement |
|---|---|---|
| **FR-1040** | P0 | **Voice storage on:** call and recording audio is kept, encrypted with per-learner keys, until the learner deletes it or their account. |
| **FR-1041** | P0 | **Voice storage off:** audio is analysed and deleted within 15 minutes of the call (FR-343). The 4-weekly recording follows the same rule unless the learner explicitly keeps that one recording. |
| **FR-1042** | P0 | **Revoking voice consent:** the setting changes at once, and all stored audio is deleted within 24 hours. |
| **FR-1043** | P0 | **Transcripts and text** are always stored while the account exists (a core function, disclosed at consent). |
| **FR-1044** | P0 | **Opt-in data use:** only with the Controls switch on (it is never asked about during onboarding) may pseudonymized, de-identified transcripts (no audio; names, places and employers replaced) be used to check and improve the teacher. Off by default. Never sold, never used for advertising. |
| **FR-1045** | LATER | **The learner's cloned voice** ("hear yourself say it fluently"): not offered in v1; may be tested later as an opt-in. |
| **FR-1046** | P0 | **Export:** a full export (the learner model in plain JSON, transcripts, kept audio) is prepared on request, and a link to it is emailed within 72 hours while export is manual, then within 1 hour once it is automated. The download link is created when clicked and is valid for 15 minutes; the file is kept for 7 days, with no passphrase. |
| **FR-1047** | P0 | **Account deletion:** confirmed by typing "delete"; no grace period; access ends at once; data is purged from live systems within 24 hours and from backups within 30 days, as stated plainly in the privacy notice. |
| **FR-1048** | P0 | **Trial ended without paying:** new episodes stop; the archive, notebook, export and delete stay available for 90 days, then the account is deleted after one email warning. |
| **FR-1049** | P0 | **Consent to process conversation content:** an explicit consent at account creation (A9, FR-118), recorded as its own consent kind with its version, for processing what the learner says in calls and chats, which may include special categories of personal data (GDPR Article 9(2)(a)). Without it the account is not created, because the product cannot run without listening. It does not cover keeping or reusing a sensitive fact: that still needs the one-tap card (FR-622). The crisis protocol (FR-57x) also rests on the learner's vital interests. |
| **FR-1050** | P0 | **Security:** encryption at rest and in transit; per-learner keys for audio, so deleting a learner's key deletes their audio; row-level isolation per learner; no data path between learners except the shared gloss cache and pseudonymized, de-identified, opt-in transcripts (NFR-301 to NFR-305). Hosting in the EU (`eu-central-1`). |
| **FR-1051** | P0 | **Compliance by conservative design, in place before launch.** (1) The strictest common rules apply to every learner wherever they live: GDPR-grade rights, hosting in `eu-central-1`, vendors under their standard data processing agreements with standard contractual clauses, and a data protection impact assessment and record of processing completed from the official templates. (2) The payment provider, as merchant of record, carries payment-side consumer law: tax, invoices, refunds and the EU right of withdrawal. (3) Risk is designed out: 18+ only (FR-003); no voiceprints or speaker identification; voice storage off by default, with deletion within 15 minutes (FR-1041); data use opt-in (FR-1044); no sensitive fact without the one-tap card (FR-622); AI disclosed in Salma's first line (FR-560), which also meets the EU AI Act's disclosure duties; SB 243-style crisis duties for everyone (FR-572). (4) Crisis resources for every country come from a maintained international helpline directory (FR-571). (5) Every legal text is checked against a compliance self-review checklist by an AI review pass and approved by the product owner; an EU and UK representative is appointed if the company sits outside them. (6) The checklist states when a lawyer becomes necessary: contact from a regulator or court, a personal-data breach that must be notified, a business-to-business or employer contract, or paid traffic from a country with a specific law the checklist does not cover. These are design rules, not legal advice; the residual risk is accepted and stated. |

---

# 12. LANGUAGE PACKAGES AND THE LANGUAGE GATE (FR-11xx)

| ID | Pri | Requirement |
|---|---|---|
| **FR-1100** | P0 | Everything language-specific is configuration, not code. A **target-language package** and an **own-language package** are separate, so any own language can pair with any target. |
| **FR-1101** | P0 | **The language gate: five checks.** A target language opens when: (1) **voices:** native speakers and learners rate two-host episodes from the candidate vendors blind, and the winner is one most of them would listen to (FR-1330); (2) **learner speech:** on the recognizer test's learner clips, the verbatim transcript keeps the learner's errors instead of fixing them and catches words said in the learner's own language (FR-862); (3) **writing:** an AI review pass checks 10 scripts against the laws and ban lists, and a fluent speaker reads them and finds them natural and correct; (4) **the call:** the host answers within about a second on that language's speech stack (NFR-107); (5) **structures:** a structure inventory exists. A target that fails any check ships later, never with a weaker bar. |
| **FR-1102** | P0 | An **own language** ships when Salma's voice passes the blind test with native-speaking listeners, its interface text, captions and glosses pass a native speaker's check of 50 items, and its recognizer catches words said with the word button. |
| **FR-1103** | P0 | **A target-language package contains:** host bibles and voice pools per accent; the structure inventory and edit-classification rules; the 12 reporting categories; band descriptors and anchor examples; the calibration set; the frequency list, lemmatizer and chunk list; the word-check items; the then-and-now task bank; the ban list; sound design. |
| **FR-1104** | P0 | **An own-language package contains:** Salma's bible and voice; gloss prompts; caption prompts; the interface strings and text direction; the crisis clip in that language, in Salma's voice (FR-571; the resources themselves come from the international helpline directory); the localized names of the 12 categories. |
| **FR-1105** | P0 | **Order of testing.** Candidate targets, in order: English, then Spanish, French, German, Italian, Portuguese, Japanese, Korean, Mandarin, Arabic, Hindi, Turkish and Russian (an estimate of likely fit, not a test result). Own languages are tested in order of demand (the own languages learners state at signup). The list is re-run whenever a vendor ships a new voice or recognizer model. |
| **FR-1106** | P0 | **Proof claims per target.** English has an established structure inventory (FR-815). Other targets start with an inventory drafted by a model and checked by a native teacher. Until a target's calibration set is tagged, its learners get the show and the calls, and progress claims stay at first-ever events and words owned (FR-841). LAW-12 is never relaxed for a new language. |
| **FR-1107** | P0 | **Cost and closing rule.** Each target needs a host duo's bibles, a voice test, a recognizer test, an inventory review and a calibration set; each own language needs a Salma (bible and voice), interface translation and a native speaker's check. v1 launches with the target languages that have passed the gate by launch (English first), and others open after launch as they pass. A language whose "worth it" answers fall well behind English closes to new learners until fixed (GATE-M12). |

---

# 13. BILLING AND PLANS (FR-12xx)

| ID | Pri | Requirement |
|---|---|---|
| **FR-1201** | P0 | **Trial:** 7 days, starting at account creation (FR-118), on the 2 a day plan, with no card. Payment is asked for once, plainly, on day 7, after one plain email on day 6 (FR-240). |
| **FR-1202** | P0 | **Plans:** 1 a day $19.99, 2 a day $29.99 ("Recommended", about $1 a day), 3 a day $44.99; monthly recurring, in USD, with tax added where required. The middle plan is marked "Recommended", not "Most popular", until that is true. Prices are set from the cost per session by the price rule (NFR-402). If a plan's margin at measured use falls below zero, its price rises for new signups only (2 a day to $34.99, 3 a day to $54.99); everyone already subscribed keeps the price they signed up at for as long as they stay subscribed. |
| **FR-1204** | P0 | **Checkout** through Paddle as merchant of record: USD prices shown in local currency where Paddle supports it; tax handled per country; cards, Apple Pay, Google Pay and PayPal; local methods such as Mada later; change plan from Controls; cancel in one tap. |
| **FR-1205** | P0 | **Plan changes** take effect at the next drop for an upgrade (the charge prorated by the payment provider) and at the next billing date for a downgrade (no proration), stated plainly at the moment of change. Unused allowance is never refunded or carried over. |
| **FR-1206** | LATER | Regional prices for lower-income countries, and a cheaper listen-first plan, once there is data on where learners are. |
| **FR-1230** | P0 | **Pricing psychology, within TC-2:** three plans with the middle one marked; the top plan as the anchor (2 and 3 a day cost the same per episode, so moving from 1 to 2 is the obvious step); "about $1 a day"; the trial on 2 a day; the first episode and call free before any account (and, after launch, the sample episode, FR-103); the real comparison shown (a tutor costs about $160 a month for two lessons a week). |
| **FR-1231** | P0 | **Never:** fake countdowns, fake scarcity, hidden or hard cancellation, guilt, pre-ticked upgrades, or an upgrade prompt anywhere except the once-a-week line in FR-209 and Controls. |
| **FR-1232** | P1 | **Receipts and failed payments:** receipts by email; a failed payment gets one plain email and a 7-day grace period in which the show continues; after that, new episodes stop and the account behaves as in FR-1048. **At launch,** the payment provider's built-in retries, dunning emails and receipts cover this; the product's own grace mechanics follow in v1.1. |
| **FR-1233** | P0 | **Cancelling** keeps the show running until the end of the paid period; afterwards FR-1048 applies. No win-back offers, no survey wall. A full refund is given on request within 14 days of the first payment; after that there are no refunds for part-months. |

---

# 14. NON-FUNCTIONAL REQUIREMENTS (NFR)

## 14.1 Latency (NFR-1xx)

| ID | Pri | Path | Budget |
|---|---|---|---|
| **NFR-101** | P0 | First open to first sound (Salma) | Under 60 s |
| **NFR-102** | P0 | First open to the learner's first spoken target-language sentence | Under 5 min |
| **NFR-103** | P1 | Sample episode playable (FR-103) | Under 30 s |
| **NFR-104** | P0 | First-episode playback after the intake | Under 45 s |
| **NFR-105** | P0 | Dropped episode starts playing | Under 2 s |
| **NFR-106** | P0 | On-demand episode (second of the day, swap, return) playable | Under 30 s, streamed |
| **NFR-107** | P0 | Host reply after the end of a learner turn | Under 1.5 s median, under 2.5 s at the 95th percentile; call connects in under 3 s |
| **NFR-108** | P0 | Word-button answer | Under 2 s |
| **NFR-110** | P0 | Word sheet opens | Under 300 ms |
| **NFR-111** | P0 | Chat opener arrives | Under 30 s |
| **NFR-112** | P0 | After-session pass and teacher update | Within 10 min of the call ending |
| **NFR-113** | P0 | Tomorrow's episode | Ready before the drop time; batch falls back to on-demand at drop time minus 90 min |

## 14.2 Reliability (NFR-2xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-201** | P0 | The learner always gets an episode at the drop time: a pipeline failure ships the fallback episode (FR-422); a teacher failure ships the rules-built brief (FR-740). |
| **NFR-202** | P0 | A live voice failure falls back to voice notes in the same thread (FR-342); no session is ever lost. |
| **NFR-203** | P0 | A voice vendor outage switches to the second voice vendor within the same day's production; two voice vendors are wired in from the start, behind adapters. |
| **NFR-204** | P0 | Every pipeline step is a durable workflow step with a timeout and retries; a partial run never publishes a partial episode. |
| **NFR-205** | P0 | Audio position, article scroll and chat history survive app restarts and device changes. |
| **NFR-206** | P0 | A model, prompt or vendor upgrade never changes a host's voice or personality silently (FR-503) and never shows up as learner progress (FR-860). |
| **NFR-207** | P0 | **Backup and restore:** automated database backups kept for 30 days, with point-in-time recovery (recovery point of 5 minutes or better). A full restore into staging is rehearsed before launch and once a quarter, finishing within 4 hours. Backups are never edited to remove a learner; deletion from backups relies on their 30-day expiry (FR-1047). |

## 14.3 Security and privacy (NFR-3xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-301** | P0 | Encryption in transit and at rest for all learner data. |
| **NFR-302** | P0 | Audio is encrypted with per-learner keys; deleting the key deletes the audio. |
| **NFR-303** | P0 | Row-level isolation per learner; no data path between learners except the shared gloss cache and pseudonymized, de-identified, opt-in transcripts. |
| **NFR-304** | P0 | Audio deleted within 15 minutes when voice storage is off; all audio deleted within 24 hours after consent is revoked; live data purged within 24 hours and backups within 30 days after account deletion. |
| **NFR-305** | P0 | Feed addresses carry an unguessable token, are excluded from podcast directories and can be reset by the learner. |
| **NFR-306** | P0 | Every model, voice and recognition call is logged with its cost and the learner-model version it read, in a tracing tool that holds no raw audio. |
| **NFR-307** | P0 | Hosting region `eu-central-1`. Cross-border transfers rest on standard contractual clauses with a transfer impact assessment (or the EU-US Data Privacy Framework where a vendor is certified), never on consent. Vendors work under their standard data processing agreements, checked in the compliance self-review (FR-1051). |

## 14.4 Cost (NFR-4xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-401** | P0 | **Cost per session** (everything one episode cycle uses: the teacher's share, writing, fitting, editing, all audio, the call and round two, re-transcription, chat, the after-session pass and a quarter of the weekly proof) is measured from the first learner, traced per role, per vendor and per learner, and reported weekly next to the heavy-use outliers. |
| **NFR-402** | P0 | **The price rule:** no plan may lose money on a learner who uses every episode, at the planning cost of $0.35 per full session. Assumptions to be replaced with measured data after launch: about 15% of the price goes to tax and payment fees; typical learners use 60% of the 1 a day allowance, 50% of 2 a day and 45% of 3 a day. Break-even cost per session at full use: $0.57 (1 a day) and $0.42 (2 and 3 a day). If either assumption is far off at the 4-week launch read, the prices are re-run with the same rule, and any rise applies to new signups only. |
| **NFR-403** | P0 | **Launch budget:** about $0.60 per session (the current itemized estimate on the recommended stack is about $0.64; the architecture cost model holds the detailed figures). Cost levers from day one: episodes at 5 to 6 minutes by default, batch processing for everything nobody waits on, and the cheapest voice that passes the blind test. |
| **NFR-404** | P0 | **Stop line:** over $1.00 a session with no costed plan to reduce it. **Scale target:** $0.30 to $0.35 at 10,000 learners; the announced prices must work there. |
| **NFR-405** | P0 | A learner on 2 or 3 a day who uses every episode costs more than they pay until the cost falls below $0.42. This is accepted while use is measured and reported weekly with the heavy-use outliers (NFR-401, GATE-11). A plan whose margin at measured use is below zero triggers the price rule for new signups only (FR-1202). |
| **NFR-406** | P1 | Sample episodes cost at most $0.05 each and are rate-limited (FR-103). |

## 14.5 Quality and evaluation (NFR-5xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-501** | P0 | No prompt or model change ships to the host, writer, editor or analyst without passing the offline test suite (FR-437) or, until that suite exists, a regression set of synthetic learners and scripted calls; and without an independent AI review pass and the product owner's approval. |
| **NFR-502** | P0 | A monthly human audit of proof claims by the product owner; false-claim rate under 5% (GATE-12). |
| **NFR-503** | P0 | A monthly review read of 10 random episodes per learner for errors, sameness and law breaks: an AI review pass, with the product owner reading what it flags (FR-436). |
| **NFR-504** | P0 | Recognizer error is tracked by first language from day one; a language whose quality falls well behind English closes to new learners until fixed (FR-1107). |
| **NFR-505** | P0 | Every "why this episode" reason is traceable to a learner-model record; every claim is openable to its evidence. |

## 14.6 Accessibility and internationalization (NFR-6xx)

| ID | Pri | Requirement |
|---|---|---|
| **NFR-601** | P0 | Right-to-left layout for own languages written right to left; every text block sets its own direction from its content; mixed-direction bubbles render correctly. |
| **NFR-602** | P0 | Captions on calls, a word-synced transcript on episodes and read-aloud on articles, so every audio surface has a text route and every text surface an audio route. |
| **NFR-603** | P0 | The app is usable with one thumb on a phone during a commute: one main episode, large buttons, the hold pad and word button within reach; no gesture overrides a system gesture. |
| **NFR-604** | P0 | Dark mode is first-class; every surface meets WCAG AA contrast in both themes. |
| **NFR-605** | P0 | Every own-language string, gloss and caption passes a native speaker's check before the language opens (FR-1102). |

---

# 15. AI ROLES AND SYSTEM RULES

This section states what the product requires of the system. Vendor choices, infrastructure and costs per role belong to the architecture.

## 15.1 The roles (thirteen, eleven in v1)

| ID | When | Role | Job | Model or code | In v1 |
|---|---|---|---|---|---|
| **FR-1301** | Before | Teacher | Reads the learner model; sets targets, due words, arcs, the weekly mix, tomorrow's ideas, each brief, "why this episode" | Strongest reasoning model, batch | Yes |
| **FR-1302** | Before | Writer | Script, article, call brief, chat opener, recap, shadow lines | Strong creative model | Yes |
| **FR-1303** | Before | Fitter | Coverage, targets, new-word budget; sends failing sentences back | Code plus a small model | Yes |
| **FR-1304** | Before | Editor | The gate (FR-412 to FR-422) | Mid-size model from a second vendor, plus code | Yes |
| **FR-1305** | Before | Voice studio | Two-voice audio, read-aloud, timestamps, names, re-listen | Text-to-speech plus recognition | Yes |
| **FR-1306** | Before | Scout | Results and news for stored interests, shared per topic | Small model plus search | LATER |
| **FR-1307** | Live | Host | The call (FR-32x to FR-34x), the word button, the chat (FR-36x) | Fast mid-size model in a voice pipeline, with the same voice as the episode | Yes |
| **FR-1308** | Live and after | Producer (Salma) | Onboarding, life updates, "Tell Salma an idea", the notebook, the weekly proof's voice, "why" and "where do I stand" when asked, fact corrections. Never corrects, never sends notes. | Conversational model with voice; strong text model for the proof | Yes |
| **FR-1309** | Live | Observer | Reads each learner turn and tells the host what to recast or draw out on the next turn | Small fast model | LATER (the first addition after launch) |
| **FR-1310** | After | Analyst | FR-801 to FR-802 | Small model with a fixed schema, checked by code | Yes |
| **FR-1311** | After | Memory keeper | Life facts with quotes, interests, goals, canon | Small model plus rules | Yes |
| **FR-1312** | Weekly | Proof producer | Scripts the proof and the finale from gated claims; picks clips | Strong text model plus the voice studio | Yes, simple version |
| **FR-1313** | Every 4 weeks | Recording rater | Rates the then-and-now recording, calibrated per language pair | Calibrated model plus code metrics | Yes |

## 15.2 Rules the system must satisfy

| ID | Pri | Requirement |
|---|---|---|
| **FR-1320** | P0 | **Code, not AI,** for: the review scheduler; the lexicon (lemmatizer, frequency list, word probabilities); the gloss cache; the coverage check; the similarity check; the claim gate; the edit classifier; the measures; the updater; cost tracing. |
| **FR-1321** | P0 | Live roles never write to the learner model; only after-session roles write, from the append-only log (FR-602). |
| **FR-1322** | P0 | Every vendor sits behind a thin adapter so that a swap is configuration. Two voice vendors are wired in from the start. A vendor may be used for some languages only, because the shipped language list is whatever passes on the chosen stack (FR-1101). |
| **FR-1323** | P0 | The editor runs on a different vendor from the writer. |
| **FR-1324** | P0 | The call host uses the episode vendor's low-latency voice, so the host sounds the same in the episode and the call. Where that is impossible, the mismatch is rated in the voice blind test (FR-1330) and watched after launch. |
| **FR-1325** | P0 | A durable workflow engine calls model APIs directly; no agent framework in the production path. |
| **FR-1326** | P0 | Vendors known to be shutting down are not used. Known future price changes (several Gemini 3.8 prices double on 2027-01-01) are visible in cost tracing, and vendor decisions use the higher prices. |

## 15.3 Vendor tests

All three run during the first build phase, before vendors are chosen.

| ID | Pri | Test | Protocol |
|---|---|---|---|
| **FR-1330** | P0 | Voices | For each candidate target, a small panel of listeners (learners of the target and native speakers) rates the same two-host script from each of the three episode-voice vendors, blind, on naturalness, accent quality and "would you listen to this on your commute?", using the vendors' post-increase prices. The same protocol, with native-speaking listeners, chooses each own language's Salma voice. |
| **FR-1331** | P0 | Recognizers | The recognizer test (FR-862). |
| **FR-1332** | P0 | Call latency | 50 scripted test calls; median host reply under 1.5 seconds after the end of the learner's turn (NFR-107). |

---

# 16. SUCCESS METRICS

## 16.1 Launch health measures (read 4 and 8 weeks after launch)

Each measure is read at 4 and 8 weeks after launch, over the learners who signed up since launch. A measure that needs more time than the first read allows (GATE-06, the 4-weekly recording; GATE-08, renewal) is read first at 8 weeks.

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

If a measure crosses its stop line, find which belief failed (the show is not wanted, the teacher is not felt, the price is wrong) before building more features. Nothing before launch tests whether learners want the show, so the 4-week read is the first answer to that question.

## 16.2 Quality and health measures (tracked from launch)

| ID | Measure | Why |
|---|---|---|
| **GATE-M01** | "Worth it" (the weekly proof question) and regret | Liking, not just wanting |
| **GATE-M02** | Unprompted return: sessions started without the notification, and within an hour of the drop time | Pull without nagging; anchor stability |
| **GATE-M03** | Tomorrow chosen: share of sessions ending with a pick | Anticipation |
| **GATE-M04** | Weeks on rhythm (weeks, not days) | Habit |
| **GATE-M05** | Return within 14 days after a gap of 7+ days; median gap length | The return design works |
| **GATE-M06** | Retention at weeks 4, 12, 26 and 52 | The long game |
| **GATE-M07** | Delayed recall: target items correct 7+ days after first meeting them | Learning, not performance |
| **GATE-M08** | Targets that hold in the next 4-weekly recording | Cannot be gamed |
| **GATE-M09** | Huh? taps per minute and taps per 100 words, over 4 weeks | Comprehension and difficulty fit |
| **GATE-M10** | "How much did you follow?" (one tap after some episodes), against predicted coverage | Level fit |
| **GATE-M11** | Word-button use per call, over weeks; errors on targets in the calls after the form returned in episodes | Dependence shrinking; whether invisible correction works |
| **GATE-M12** | "Worth it" and false-claim rate per language; recognizer error by first language | Quality and fairness across languages |
| **GATE-M13** | Plan mix and the share of each plan's allowance used | Whether the prices and the cost rule hold |
| **GATE-M14** | Notebook fact edits in week 1 | Whether the open notebook builds trust |
| **GATE-M15** | Similarity score across each learner's episodes; the monthly review read (FR-436) | Sameness |
| **GATE-M16** | Minutes per day, with heavy-use outliers flagged | A warning light, never a goal |
| **GATE-M17** | Time to first sound; time to first spoken sentence | The first ten minutes |

## 16.3 Out of scope for v1

- Character creation and the six chassis; learner-made or guest hosts.
- The news scout, and any current-events facts the learner did not supply.
- The observer in the call.
- Languages that have not passed the language gate.
- Native apps (none planned); sign-in with Apple or Google.
- Invites, a waitlist or a beta; founding or introductory prices; an external language test.
- Detecting the learner's own language without the word button.
- Settings beyond the Controls sheet.
- Referral programmes and community features; social sharing of proof clips (a learner may download their own tape).
- The learner's cloned voice.
- Real-life rehearsal on demand; bring-your-own-input episodes.
- A yearly plan; regional prices.
- Exploration slots in targeting.
- "Where do I stand" for skills not yet calibrated.
- Ask-first glosses.
- Employer and university seats.
- Playback above 1.0×.
- Any chart, percentage or level on any surface.

---

# 17. ASSUMPTIONS, CONSTRAINTS, DEPENDENCIES AND RISKS

## 17.1 Assumptions

These are planning figures to be replaced with measured data after launch.

| Assumption | Used in | Replaced by |
|---|---|---|
| About 15% of the price goes to tax and payment fees. | NFR-402 | Measured fees at the 4-week read |
| Typical learners use 60% of 1 a day, 50% of 2 a day, 45% of 3 a day. | NFR-402, FR-1202 | Measured allowance use (GATE-M13) |
| A full session costs about $0.64 on the recommended stack, with a path to $0.35 or less. | NFR-403, NFR-404 | Measured cost per session (NFR-401) |
| A similarity threshold of cosine 0.85 separates fresh episodes from repeats. | FR-433 | Tuning on real use from the review read |
| A recall threshold of 0.85 is the right point to call an item due. | FR-720 | Tuning after launch |

## 17.2 Constraints

- **Platform:** web application plus a private podcast feed; no native app. Sign-in by email one-time code only.
- **Audience:** adults 18 or older, in countries where the payment provider sells.
- **Hosting and data:** EU hosting (`eu-central-1`); GDPR-grade rights for every learner; learner data reaches only vendors under a data processing agreement.
- **Payments:** Paddle as merchant of record; monthly subscriptions in USD.
- **Languages:** English is the first target. A language opens only by passing the language gate (FR-1101); the bar is never lowered.
- **Claims:** until calibration data exists (collected after launch, from opted-in learners), progress claims are limited to first-ever events and words owned (FR-841, FR-860).
- **Vendor prices:** vendor decisions use known future prices, including the Gemini 3.8 price increase on 2027-01-01 (FR-1326).

## 17.3 Dependencies before launch

- Vendor accounts for every model, voice and recognition role.
- A Paddle account, approved for the product.
- The product's domain, needed before email sending and the first public deploy.
- The English host bibles and Salma's Arabic bible, approved by the product owner.
- Recognizer test clips: an open learner-speech corpus and about 30 consented volunteer clips (FR-862).
- Volunteer listeners for the voice blind tests (FR-1330).
- An EU and UK representative, if the company sits outside the EU and UK.

## 17.4 Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Nothing before launch tests whether learners want the show. | The product may launch to weak demand. | The launch health measures at 4 and 8 weeks, with stop lines (16.1); no new features until a failed measure is understood. |
| Recasts alone are the least-noticed kind of feedback. | Accuracy may not improve. | Salient recasts, errors brought back in later episodes, accuracy measured every 4 weeks; GATE-07 shows it if it fails (9.6). |
| Heavy users on 2 or 3 a day cost more than they pay until the cost per session falls below $0.42. | Negative margin on some learners. | Weekly cost tracing with outliers; the price rule raises prices for new signups only (NFR-402, NFR-405). |
| Streaming recognizers fix learner errors silently, and recognition may be worse for some first languages. | Wrong evidence; unfair quality. | Verbatim re-transcription, a confidence filter, the recognizer test, error tracked by first language (FR-801, FR-804, FR-862, NFR-504). |
| Generated episodes drift toward sameness or break a law. | Learners lose interest or trust. | The editor's gate, the ban list, format rotation, the similarity check and the monthly review read (5.3, 5.4). |
| A false progress claim or a wrong memory. | Trust in every later claim is lost. | The claim gate (FR-840), the quote check (FR-620), the monthly claims audit (NFR-502), wrong-memory tracking (GATE-13). |
| The host's voice in the call may differ from the episode's. | The show feels less like one person. | The same vendor's low-latency voice; the mismatch rated in the blind test and watched after launch (FR-1324). |
| Compliance is met by conservative design and self-review, without counsel. | Residual legal risk. | Strictest common rules for everyone; a self-review checklist; stated triggers for engaging a lawyer (FR-1051). |

---

# 18. RELEASE SCOPE AND LAUNCH READINESS

Version 1 launches once, publicly, with open signup, when every P0 requirement works and the launch criteria below are met. The order of build work is set by the release plan.

## 18.1 Launch criteria

- Every P0 requirement works in every language that launches.
- A measured cost per session from test learners, and a costed path to $0.35 or less.
- A full restore into staging rehearsed, finishing within 4 hours (NFR-207).
- An account deletion and an export verified on a test learner (FR-1046, FR-1047).
- The compliance self-review checklist completed and approved by the product owner (FR-1051).
- The dependencies in 17.3 in place.
- Security checks green: dependency and secret scanning on every change, a baseline web vulnerability scan of staging, and a security review of every change touching sign-in, keys, media links, the feed or deletion. A paid penetration test is not required at launch; it becomes necessary at 1,000 paying learners, before any business-to-business contract, or after any security incident.

## 18.2 At launch

Signup opens to anyone 18 or older in a country where Paddle sells (FR-004), into the 7-day trial on the 2 a day plan with no card (FR-1201).

## 18.3 After launch (v1.1, P1)

Round two; shadowing; the season finale with its then-and-now comparison; the tape; the full claim gate, once standard errors and the calibration set exist; the offline test suite; the dial-in experiment; the sample episode; the Show tab; the product's own failed-payment grace mechanics; writing extra scripts ahead for learners who use their extras most days. The launch health measures are read at 4 and 8 weeks (16.1).

## 18.4 Later (direction, not specification)

Moving to the cheapest stack that passes, piece by piece, with blind tests; paid acquisition once retention holds; each new language as it passes the gate; regional prices and a cheaper listen-first plan once there is data on where learners are; employer and university seats, and human bridges, after that.

---

# GLOSSARY

| Term | Meaning |
|---|---|
| Active day | A local calendar day with at least half an episode played in the app, "Heard it" tapped on a feed episode, a call started, or the small door used |
| Anchor | The learner's chosen moment for the episode, in life terms |
| Claim gate | The code that decides whether any statement about progress may be made |
| Coverage | The expected share of running words the learner understands |
| Door | A part of a session the learner can open: listen, shadow, read, call, chat, round two, small door |
| Drop | Publishing the day's episode to the feed and sending the one notification, at the learner's chosen time |
| First episode | The episode made for the learner during onboarding (FR-115) |
| Hosts | The authored duo who run the show in the target language (Karim and Mona for English) |
| Idea | One of tomorrow's three one-line episode proposals |
| Language gate | The five checks a target language must pass to open (FR-1101) |
| Launch health measure | A GATE metric with a target and a stop line, read 4 and 8 weeks after launch (16.1) |
| Own language | The learner's native language: the language of the interface and of Salma |
| Plan | 1, 2 or 3 new episodes a day, monthly ($19.99, $29.99, $44.99) |
| Producer (Salma) | The face of the app in the learner's own language: onboarding, the notebook, the proof's voice; never corrects |
| Product owner | The person who approves content, prompts, legal texts and releases, and receives operational alerts |
| Recast | The host saying the learner's point back the natural way ("you mean..."), never marked as a correction |
| Return episode | The first episode after 5 or more days away |
| Rhythm | The learner's weekly intention, with spare days |
| Round two | A short second call on the same argument, shorter and faster |
| Series bible | The learner's world: hosts, side characters, places, jokes, arcs, season, canon |
| Session | One episode and all its doors |
| Small door | The 90-second recap plus one voice note, for bad days |
| Target language | The language the learner is learning |
| Teacher | The planner behind the show; it never speaks, and it decides what the hosts say and what Salma shows |
| Then-and-now recording | The same 3-minute speaking task every 4 weeks |
| v1, v1.1 | v1 is what launches (P0); v1.1 is what follows soon after launch (P1) |
| Word button | Hold it and say a word in your own language; the host gives it back in the target language |
| Working on | The at-most-3 items the teacher is targeting, visible and editable in the notebook |
