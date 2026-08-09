# Lucent — User Flows & User Stories

**Version 1.0 · Companion to PRD v1.1 · UI-agnostic (no screen/layout decisions implied)**

---

# Part A — User Flows

## Flow 1: First-Time User (Onboarding → First Episode)

**Goal: from landing to first episode playing in under 15 minutes, with the user feeling met, not processed.**

1. User arrives at the web app and starts. Minimal account step (just enough to persist state; completes fully later — FR6).
2. The **producer voice** opens the intake conversation in the user's **native language** (FR1).
3. Conversation covers, naturally (FR2):
   - Why this language — and the real situation behind it (goal + register)
   - Their life: interests, work, what they watch, who they support
   - Past learning attempts and what killed them
   - 2–3 follow-up seeds with dates captured silently
4. Woven into the chat: 3–4 natural target-language moments → internal level estimate (FR3). *User never perceives a test.*
5. User makes their **one choice**: target-language dialect/variant, with audio samples (FR4).
6. Voice-storage consent requested, framed in-story: "we keep tape — every show does" (FR6). Decline = fully functional product, text-only proof.
7. **Handoff moment:** the producer introduces the default duo. The duo plays a short authored intro piece in easy target-language speech (FR4). Character creation is mentioned in passing, not offered (FR4).
8. The duo delivers **one live-generated pitch** built from the intake ("You said the derby's Saturday and your brother supports the wrong team — we have to do this") (FR5).
9. User accepts → **first episode (4–5 min) plays within minutes** (FR5).
10. The rest of the first cycle (article → call-in → chat) continues if the user has time, or waits (FR18).

**Exit state:** learner file seeded (interests, situations, follow-up seeds, level estimate); first session experienced or in progress.

---

## Flow 2: Daily Core Loop (Returning User)

**Goal: from opening the app to inside an episode in under 30 seconds.**

1. User opens the app. Today's **3–5 pitches** are waiting (FR8) — each one line: Topic + Format + Cast, written as a hook.
2. User chooses one of three paths (FR9):
   - **a. Accept a pitch** → episode starts (< 2s if it's the pre-generated pick — NFR1)
   - **b. Remix a pitch** → change topic, format, or cast independently → episode generates (playable < 30s — NFR1)
   - **c. Build from scratch** → own topic + any format (starter library or described freely — FR11) + any cast (FR26)
3. **The Full Cycle runs** (see Flow 3).
4. After the cycle: post-session analysis runs in the background within 10 min (NFR3). No visible grading, ever.
5. Overnight: the planner reads the updated file and writes tomorrow's pitches (FR45).

---

## Flow 3: The Session (Full Cycle)

**One continuous argument through four media. Self-contained (FR19). Pausable at any point, resumable with one tap (FR18).**

1. **Listen (≤ 8 min, FR14)**
   - Episode plays with the user's chosen cast; synced transcript below; every word tap-to-define (FR20).
   - Hosts build a genuine conflict → leave it unresolved → throw to the user: *"The article's in your notes. Read it, then get in here."*
2. **Read (3–4 min, FR15)**
   - Article appears — level-pitched, tap-to-define.
   - Contains **ammunition the episode didn't have**: a counterargument, a missed fact, a reason to change sides.
3. **Speak (4–5 min, FR16)**
   - One tap → live call-in with a host. The host defends a position, pushes back, plays devil's advocate.
   - Silence ≥ 5s tolerated before any gentle prompt (NFR2); no mid-formulation interruptions.
   - User may change sides, reject the premise, bring personal examples, ask "what does X mean?", or end early — host responds genuinely to each (FR16).
   - If live voice fails → graceful fallback to asynchronous voice-note exchange; the argument survives (NFR5).
4. **Chat (2–4 min, FR17)**
   - The host sends a needling follow-up message. 3–5 written exchanges.
   - Adds something new (a comeback, a joke, a fresh angle) — never re-litigates the call.
   - Ends like a real conversation: a laugh, a concession, "we'll see Saturday."

**Invisible throughout:** 1–2 targets threaded through all four media (FR37); recasts in-flow (FR38); every tap, replay, utterance, and message logged as evidence (FR29–FR34).

**Pause behavior:** any stage, any moment → state persists (audio position, article, chat) → resume with one tap, even hours later (FR18).

---

## Flow 4: Character Creation

*Available any time after onboarding; never required. Ships after the default duo is excellent (FR21).*

1. User tells the show they want a new host ("I want someone who argues like my uncle").
2. Short creation conversation (never a form — FR22): the show asks who's needed, name, and key traits; user picks a voice from samples (FR27).
3. System maps inputs onto one of six authored chassis, skinned by the user's choices (FR23). *Invisible to the user.*
4. **The new character introduces itself immediately** in a short in-character piece (FR24).
5. Character joins the roster (max 6 active — FR25) and is castable from the next pitch onward (FR26).
6. Editing/retiring: user just tells the show ("make Karim less aggressive" / "retire Omar") (FR25).

---

## Flow 5: The Weekly Proof

1. Once a week, a ~2-minute **mini-episode** arrives from the user's own hosts — a "listener retrospective" (FR47).
2. Contents:
   - One **side-by-side moment**: the user weeks ago vs. now (audio if consented; text quotes otherwise)
   - **Named concrete wins**: "Eleven days since you last said *I go yesterday*"
   - One **teaser**: what the show goes after next
3. Flat week → said honestly: "Flat week. Happens to everyone. Here's what we're changing" (FR48).
4. All numbers live inside sentences the hosts say — no dashboard renders anywhere (FR49).

---

## Flow 6: Returning After Absence

1. User disappears for days or weeks. **The show sends nothing** — no re-engagement notifications, no guilt (FR53).
2. User returns → greeted the way a friend greets: one warm line, zero guilt, fresh pitches waiting.
3. No "catch-up," no broken streak, nothing missed — sessions are self-contained (FR19). The show simply continues, memory intact.
4. If energy signals suggest rust, the next session quietly runs easier (FR39). Invisible.

---

## Flow 7: Preferences, Trust & Data

1. **All preference changes happen by talking to the show** ("talk slower," "less politics," "more stories, fewer debates") — acknowledged in character, applied from the next session. No settings screens exist (Principle 3).
2. Voice consent is revocable any time → stored clips deleted (FR51).
3. Export everything / delete everything: instant, complete, friction-free (FR52; deletion executes within 24h across backups — NFR6).

---

# Part B — User Stories

*Format: As a [user], I want [X] so that [Y] — with acceptance criteria (AC) traceable to the PRD.*

## Epic 1: Onboarding

**US-1.1** — As a new user, I want to start by having a real conversation about my life and goals instead of filling forms and taking a placement test, so that the product feels like meeting someone, not enrolling in a course.
- AC: intake is fully conversational in my native language (FR1); no visible test exists (FR3); the only explicit choice I make is dialect (FR4).

**US-1.2** — As a new user, I want to hear my first personalized episode within minutes of finishing the conversation, so that the "show made for me" promise is proven before I leave.
- AC: one live pitch built from my intake (FR5); first episode (4–5 min) plays within minutes (FR5).

**US-1.3** — As a privacy-conscious user, I want to understand and control whether my voice is stored, so that I can use the product on my terms.
- AC: consent requested in plain language during onboarding (FR6); declining keeps the product fully functional (FR6); revocable later with clip deletion (FR51).

**US-1.4** — As a day-2 user, I want the show to reference something I said yesterday, so that I know it actually listened.
- AC: day-2 episode contains ≥1 intake callback (FR7).

## Epic 2: Daily Pitches

**US-2.1** — As a returning user, I want to choose between episode ideas made for me each day, so that my daily decision is "which episode?" — never "should I study?"
- AC: 3–5 one-line pitches daily (FR8); each carries an editorial point of view, hook-written (FR12).

**US-2.2** — As a user with my own idea, I want to override everything — topic, format, cast — or build a session from scratch, so that the show is mine.
- AC: every pitch element independently modifiable; my choice is final (FR9); free-form format requests are honored (FR11).

**US-2.3** — As a user whose life the show knows, I want pitches drawn from what's actually happening to me — my decisions, my trips, my team, my follow-ups — so that episodes feel like they're about my week.
- AC: sourcing priority is my life first, current events as one source among several (FR10); open follow-ups get at least one pitch (FR10).

## Epic 3: The Session

**US-3.1** — As a learner, I want the episode to be genuinely entertaining at my exact level with the transcript there when I need it, so that I listen because I want to know what happens.
- AC: edge-pitched banter, synced transcript, tap-to-define on every word (FR14, FR20); compact-over-filler sizing (FR14).

**US-3.2** — As a listener pulled into the argument, I want the article to arm me with something the hosts don't know, so that reading it gives me an advantage in the call-in.
- AC: article adds a counterargument, missed fact, or side-switching reason — never a recap (FR15).

**US-3.3** — As a nervous speaker, I want the host to wait while I form sentences and never cut me off or grade me, so that speaking feels like arguing with a friend, not performing for a teacher.
- AC: ≥5s silence tolerance (NFR2); no mid-formulation interruptions (FR16); no per-turn praise or grading language (NFR8).

**US-3.4** — As an opinionated user, I want to change sides, reject the premise, or take the debate somewhere personal, so that the conversation is genuinely mine.
- AC: the call-in absorbs side-switching, premise rejection, personal examples, explain-this requests, and early endings — responding genuinely to each (FR16).

**US-3.5** — As a busy person, I want to pause anywhere and resume hours later with one tap, so that one session fits inside my real day.
- AC: mid-stage pause persists all state; one-tap resume; a cycle may span a day (FR18).

**US-3.6** — As a user texting after the call, I want the chat to feel like a friend needling me — short, funny, ending naturally — so that I write without ever receiving a writing task.
- AC: 3–5 exchanges; adds something new; ends like a real conversation, never with a task (FR17).

## Epic 4: Cast & Characters

**US-4.1** — As a new user, I want two hosts with real, distinct personalities from day one, so that the show is alive before I've customized anything.
- AC: authored default duo with stable values, biases, distinct humour (FR21).

**US-4.2** — As an invested user, I want to create and name my own host by describing them in conversation and picking a voice, so that my cast feels like mine.
- AC: conversational creation, never a form (FR22); immediate in-character introduction (FR24); castable next session (FR26).

**US-4.3** — As a returning user, I want each character to remember their own history with me, so that my relationship with Karim is different from my relationship with Layla.
- AC: per-character relationship memory (FR25); certainty rule on all callbacks (FR43).

## Epic 5: Learning (Invisible)

**US-5.1** — As a learner, I want my mistakes corrected the way a friend does it — inside the reply, never as a correction — so that I keep talking instead of feeling graded.
- AC: recast-only in flow (FR38); recasts socially natural (Principle 6); recurring errors targeted across sessions until they stick (FR37).

**US-5.2** — As a curious learner, I want an honest, clear explanation when I ask why a form is right, so that the show respects my question instead of protecting its illusion.
- AC: on explicit request, plain explanation (FR38, layer 2).

**US-5.3** — As a learner, I want the difficulty to always sit exactly at my edge without ever seeing a level, so that I'm stretched but never labeled.
- AC: invisible difficulty adaptation both directions (FR39); no level surfaced anywhere in any wording (FR40).

**US-5.4** — As a tired user, I want the show to notice my energy and ease up tomorrow without telling me, so that a bad day never becomes a confrontation.
- AC: energy detection adjusts next session invisibly (FR39).

## Epic 6: Progress & Memory

**US-6.1** — As a long-term user, I want weekly, concrete, audible evidence that I'm improving — my own voice then vs. now — so that I believe the show is working.
- AC: weekly ~2-min mini-episode with side-by-side moment, named wins, one teaser (FR47).

**US-6.2** — As a user having a bad stretch, I want flat weeks reported honestly with what changes next, so that I can trust the good weeks too.
- AC: no fabricated wins, ever (FR48).

**US-6.3** — As a nostalgic user, I want to browse everything we've ever made — episodes, my recordings, our chats — so that I can hear how far I've come.
- AC: full archive by date; no stats layered on it (FR49).

**US-6.4** — As a person with a life, I want the show to remember what matters (and ask about the interview on Friday) without constantly announcing that it remembers, so that it feels like a friend, not a database.
- AC: dated follow-ups drive pitches (FR10, FR41); ≤2 personal references per episode, only things I told it directly (FR44); nothing stated unless certain (FR43).

## Epic 7: Trust & Control

**US-7.1** — As any user, I want to change how the show behaves by simply telling it, so that I never hunt through settings.
- AC: conversational preference changes take effect from the next session; no settings UI exists (Principle 3, Flow 7).

**US-7.2** — As a data-conscious user, I want to see what the show knows about me, correct it, export everything, or delete everything instantly, so that this intimacy stays on my terms.
- AC: plain-language knowledge summary (FR52); one-step export and full deletion (FR52, NFR6).

**US-7.3** — As a user who disappeared for two weeks, I want zero guilt — no "we miss you" messages, no broken anything — so that coming back costs nothing.
- AC: no re-engagement messaging (FR53); warm single-line greeting on return; sessions self-contained (FR19).

---

## Traceability Note

Every acceptance criterion maps to PRD v1.1 requirements (FR1–FR53, NFR1–NFR9). Flows introduce no requirements not present in the PRD; where the PRD is silent (visual layout, navigation, component design), these flows deliberately remain silent too — UI/UX is a separate, undecided workstream.