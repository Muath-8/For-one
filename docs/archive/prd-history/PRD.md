# For one — Implementation PRD

**Version 2.0. This document replaces high-level descriptions with exact, buildable specifications. Every section states precisely what happens, in what order, with what limits, and what happens on failure. Decisions the source documents did not make are made here and marked [NEW]. Anything marked OPEN is genuinely deferred and nothing in v1 depends on it.**

---

# PART 1 — SYSTEM OVERVIEW

## 1.1 What the system is

One web application. One user account = one show. The show consists of:

1. A **learner file** (persistent database record per user, four sections — see Part 8).
2. A **cast roster** (1 default duo + up to 6 user-created characters — see Part 7).
3. A **nightly planner** (batch job per user, runs once per night — see Part 9).
4. A **session engine** (produces and runs one Full Cycle: Listen → Read → Speak → Chat — see Part 6).
5. An **assessment engine** (post-hoc analysis pipeline — see Part 10).
6. A **Weekly Proof generator** (weekly batch job — see Part 11).

## 1.2 Hard product laws (constraints on every part below)

1. No levels, courses, streaks, points, tests, badges, dashboards, charts, prompts, or homework exist anywhere in the product, in any wording, in any language surface (UI, audio, chat, email, notifications).
2. The user controls topic, format, and cast. The system controls difficulty, targets, corrections, sequencing — invisibly.
3. Sessions are self-contained. Only memory persists between sessions.
4. Characters are transparently AI. No guilt mechanics, no re-engagement messaging, no dark patterns.
5. In-flow correction is recast-only. Explicit correction happens only when the user explicitly asks.
6. The internal CEFR-anchored proficiency model is never surfaced in any form or wording.

## 1.3 Platform and scope decisions

| Item | Decision |
|---|---|
| Platform | Responsive web app. Must be fully functional on mobile Safari and mobile Chrome. No native apps in v1. |
| Audience | 18+. Age gate: self-declared birth date at account creation; under-18 dates are rejected with a plain message. [NEW: self-declaration is the only check] |
| Sessions per day | Hard cap 2 per calendar day in the user's local timezone. The UI does not advertise the cap; if a user attempts a 3rd, the show says, in character, that tomorrow's episode needs time to be made. [NEW: in-character cap message] |
| Languages | Architecture is language-agnostic (see Part 13). Launch language: OPEN. |
| Business model | OPEN. No pricing surface exists in v1. Cost-per-cycle telemetry is mandatory from day one (Part 12). |
| Accounts | Email + password, plus OAuth (Google, Apple). [NEW] Email verification required before session 2, not before session 1 (nothing blocks the first episode). [NEW] |

---

# PART 2 — ONBOARDING (EXACT SEQUENCE)

## 2.1 Entry

1. User lands on the web app, taps the single start action.
2. Minimal account step: email + password or OAuth, birth date, **name** (what the show should call them — the name is the anchor of all personalization: hosts use it, pitches use it, the Weekly Proof addresses it). One text field; the producer confirms pronunciation conversationally during intake if the user replies by voice. [NEW: name collected at account step, pronunciation confirmed in intake]
3. Native language selection: a single list, searchable. [NEW: this is a UI selection, not conversational — the producer must speak the user's native language before the conversation can begin]
4. Target language selection: single searchable list. [NEW: same reasoning]

## 2.2 The intake conversation

5. The **producer voice** begins. The producer is a neutral authored persona, one per native language, voice + text hybrid: the producer speaks (audio) and the user replies by text or voice, user's choice per message. [NEW: reply modality is per-message user choice]
6. Length target: ~10 minutes, 12–18 producer turns. [NEW: turn budget]
7. The conversation must collect, in natural order, all of the following fields into the learner file:
   - **Goal**: why this language.
   - **Register situation**: the concrete real situation behind the goal (job interviews, in-laws, travel, exams). Determines the register bias of generated content.
   - **Interests**: minimum 3, target 5–8, each stored with a salience score initialized to 1.0. [NEW: salience initialization]
   - **Life situations**: current job, city, ongoing situations the user volunteers.
   - **Past attempts**: what they tried before and what killed it.
   - **Follow-up seeds**: 2–3 future-dated events ("interview Friday", "trip in March"), each stored with a date and a due-state.
8. If the user gives short/closed answers and a field cannot be filled after 2 attempts, the producer moves on; the field is marked sparse and the planner compensates in week 1 by weighting interests higher. The intake never stalls on a field. [NEW: sparse-field rule]

## 2.3 The hidden level estimate

9. Exactly 3–4 target-language moments are woven in (producer switches language naturally: "oh — do you already understand if I say …?"). Each moment is one comprehension probe or one production invitation.
10. Output: internal estimate on the CEFR-anchored scale, stored as a band + confidence (low). Estimate starts one band conservative (if evidence says B1, store A2-high). [NEW: explicit conservative offset]
11. Calibration: during sessions 1–5, every session's production evidence updates the estimate; after session 5 the confidence flag flips to normal and the conservative offset is removed. [NEW]

## 2.4 The two explicit choices and consent

12. Dialect/variant choice: audio samples (10–15 seconds each) per available variant; user picks one. This is the user's only language-related explicit choice.
13. Voice-storage consent: producer explains in-story ("we keep tape — every show does") followed by a plain-language sentence stating exactly what is stored (call-in audio), why (progress comparisons), and that it is deletable any time. Two buttons: consent / decline. Declining sets `voice_storage = false`; every downstream feature that references audio (Weekly Proof side-by-side) automatically uses text quotes instead. No feature is disabled.

## 2.5 Handoff and first episode

14. Producer introduces the default duo by name. The duo plays a pre-authored recorded intro (60–90 seconds, easy target-language speech, same piece for all users of that dialect). [NEW: duration]
15. Character creation is mentioned in one sentence by the producer, never offered as a flow.
16. The duo delivers **one live-generated pitch** built from intake data. The user can accept it or tap "not this one," which generates one alternative pitch (max 1 alternative; if rejected too, the first episode uses the user's top interest with no callback pressure). [NEW: rejection path]
17. First episode: 4–5 minutes, generated live, playable within 3 minutes of pitch acceptance. Streaming: playback begins when the first audio chunk is ready. [NEW: 3-minute ceiling]
18. After Listen, the rest of the cycle (Read → Speak → Chat) continues immediately if the user proceeds, or persists paused indefinitely.

## 2.6 Day-2 rule

19. The day-2 episode must contain ≥1 verbatim-sourced callback to something the user said in intake. The planner enforces this as a generation constraint; the quality gate (Part 6.7) checks it on day 2.

---

# PART 3 — DAILY LOOP (EXACT SEQUENCE)

## 3.1 Pitch delivery

1. The planner (Part 9, event-hooked) writes 3–5 pitches. Exactly how many: 3 if the file is sparse (week 1), 5 once ≥3 interests have engagement history, otherwise 4. [NEW: count rule]
2. Each pitch is one line of text: hook-written, carrying Topic + Format + Cast implicitly or explicitly. Hard length cap: 140 characters. [NEW: cap]
3. Pitches appear when the user opens the app. No push notification announces them (no notifications exist in v1 at all, except account-verification email). [NEW: zero-notification decision]
4. Pitch composition constraints (all enforced by the planner):
   - ≥1 pitch from the user's own life if any follow-up is due or any life situation is active.
   - Exactly 1 wildcard pitch outside the user's usual lanes.
   - Current events appear only when they intersect a stored interest.
   - Every pitch passes the pitch test (Part 6.7 gate includes it).

## 3.2 User paths

5. **Accept**: if it is the planner's predicted pick, playback starts < 2 seconds (pre-generated). Otherwise generation starts; playable < 30 seconds (streaming, host opening generated first).
6. **Remix**: user edits topic, format, or cast independently before starting. Any edit = regeneration; playable < 30 seconds.
7. **From scratch**: user types/says a topic, picks a format (starter library: debate, story time, news rundown, interview, explain-it-to-me, roast — or describes any format in free text), picks cast. Free-text formats are honored; the generator maps them to the closest structural pattern and follows the user's description over the pattern on conflict. [NEW: conflict rule]
8. Pitches expire when the next planner run replaces them. An accepted-but-unfinished session never expires. [NEW: expiry rule]

---

# PART 4 — SESSION STATE MACHINE

States: `pitched → listening → reading → speaking → chatting → complete`, plus `paused(stage, position)` reachable from any active state.

Rules:
1. Forward-only progression; the user cannot re-enter Speak after Chat begins, but can always re-read the article and re-play the episode (read-only) at any time, including after completion. [NEW: re-entry rules]
2. Pause persists: audio position (seconds), article scroll position, chat transcript, call-in state = not resumable mid-call — a paused call-in resumes as a fresh call opening that acknowledges the gap in one line ("you left me hanging — where were we"). [NEW: call-in pause behavior]
3. A session may span up to 48 hours; after 48 hours unfinished it is marked `abandoned`, remains in the archive, and its partial production evidence still feeds assessment. [NEW: 48h rule]
4. Skipping: the user can tap forward from any stage to the next (skips are allowed, logged as energy signals). Skipping Read is permitted; the call-in host will not punish it but naturally references the article, which is the built-in cost. [NEW: explicit skip permission]
5. One session at a time: starting a new session while another is active prompts one confirmation; confirming marks the old one abandoned. [NEW]

---

# PART 5 — SESSION CONTENT SPECIFICATIONS

## 5.1 Listen

- Duration: sized by material, hard ceiling 8:00 minutes, floor 3:00. [NEW: floor]
- Structure: cold open (≤30s) → conflict build → escalation → unresolved throw to the user, verbatim pattern: the hosts name the article and demand the user get in ("the article's in your notes — read it, then get in here"). The throw is mandatory in every episode.
- Cast: exactly the user-selected cast (one host or a pair).
- Language: target language throughout; difficulty pitched at the stored edge (Part 10.9).
- Transcript: word-level synced, always visible below the player, every word tap-to-define.
- Audio player controls: play/pause, scrub, 10s back, speed 0.8×/1.0×. [NEW: speed control is allowed and logged; no speed above 1.0× — faster speeds would let users bypass the pitched difficulty]
- Personal references: ≤2 per episode, only facts the user told the show directly, only high-confidence memories.

## 5.2 Read

- Article length: 150–300 words at A-bands, 250–450 at B-bands, 350–600 at C-bands. [NEW: banded word counts]
- Content contract: must add ≥1 of — a counterargument, a fact the hosts missed, a reason to change sides. Never a recap. The generator receives the episode script and an explicit instruction to arm the reader against it.
- Every word tap-to-define. Reading time and scroll completion logged.

## 5.3 Speak (the call-in)

- Entry: one tap. Target duration 4–5 min; the host initiates ending after 5:30 with a natural close; hard cut at 7:00 with an in-character sign-off. [NEW: end-of-call mechanics]
- Latency: end-to-end voice response < 1.5s.
- Silence: ≥5s tolerance before one gentle in-character prompt; after two consecutive 15s silences the host offers to wrap up. [NEW: double-silence rule]
- Host behavior contract (all mandatory): takes a genuine position; pushes back at least once; never interrupts mid-formulation; absorbs side-switching, premise rejection, personal examples, "what does X mean" (answers plainly, in-character), and early endings; never grades, never praises per-turn, never steers back to a script.
- Recasts: per Part 10.11, embedded only.
- Failure: if live voice fails (connection or synthesis), the UI switches to asynchronous voice-note exchange within the same argument; the session is never lost.
- Recording: audio stored only if `voice_storage = true`; transcript always stored (transcript storage is core functionality, disclosed at consent step). [NEW: transcript-always clarification]

## 5.4 Chat

- Trigger: host sends the first message within 30 seconds of call-in end. [NEW: timing]
- Length: 3–5 host messages total; the host ends the exchange at message 5 at the latest with a natural closer (laugh, concession, "we'll see Saturday"). If the user keeps writing after the closer, the host sends exactly one final short reply and goes quiet; further user messages are answered next session in one callback line. [NEW: post-closer behavior]
- Content contract: adds something new (comeback, joke, clarification, next-angle); never re-litigates the call; never assigns anything.
- Modality: text only in v1. [NEW]

## 5.5 Tap-to-define

- Popover contents: meaning in native language, part of speech, one example sentence in target language. Nothing else (no conjugation tables, no audio in v1). [NEW: scope]
- Source: generated per word-in-context by the model at content-generation time for every word in transcript and article (pre-computed, not on-demand, to guarantee popover latency < 300ms). [NEW: pre-computation + latency]
- Every tap logged: word, lemma, timestamp, surface (transcript/article), repeat-count across sessions.

---

# PART 6 — GENERATION PIPELINE AND QUALITY GATE

## 6.1 Pipeline order per episode

1. Planner brief (topic, format, cast, targets, frontier vocab, difficulty setting, personal references allowed) →
2. Episode script generation →
3. Article generation (receives script) →
4. Call-in host brief generation (position, pushback material, recast list) →
5. Chat opener generation (receives call transcript later, at runtime) →
6. Tap-to-define pre-computation →
7. Audio synthesis →
8. Quality gate.

## 6.2 Quality gate (automated, pre-ship, every episode)

Checks, each pass/fail:
1. **Level fit**: script difficulty within the user's edge band.
2. **Target presence**: assigned targets (1–2) appear in the planned surfaces.
3. **Canon consistency**: no statement contradicts high-confidence learner-file facts; no low-confidence memory is stated.
4. **Pitch test**: an LLM rater answers "would this specific user tap this if it were a real podcast?" with the user's interest profile; fail on no.
5. **Law scan**: no lesson furniture wording, no grading language, no unsolicited correction, ≤2 personal references. [NEW: explicit law scan as a gate check]

Fail → regenerate once. Second fail → ship the fallback: an interest-based, callback-free episode from the user's top interest, which itself must pass checks 1, 3, 5. [NEW: fallback still gated on 3 checks]

---

# PART 7 — CAST SYSTEM

1. **Default duo**: one authored duo per target language + dialect. Each host: name, fixed voice, personality document (values, biases, humor style, relationship stance toward the learner, speech patterns), designed to disagree productively. The duo is fully authored content, not generated.
2. **Character creation**: unlocked from day 1 but never promoted; ships only after the duo passes internal quality bar. Creation is a conversation with the show (the duo interviews the user about who's needed). Collected: name, voice (picked from sample list), 2–4 personality traits, optional quirks, optional backstory lines.
3. **Chassis mapping**: every created character maps to exactly one of six chassis — debater, storyteller, gentle skeptic, comedian, professional, hype-man. Mapping is chosen by the system from the user's description; invisible; stored.
4. **Introduction**: created character introduces itself immediately, 30–60s in-character audio piece. [NEW: duration]
5. **Roster**: max 6 active created characters (the default duo does not count against the cap). [NEW: duo excluded from cap] Editing and retiring happen conversationally; retired characters keep their memory and can be un-retired the same way. [NEW: un-retire]
6. **Relationship memory**: per-character memory section in the learner file (shared facts stay global; jokes, positions taken, and relational history are per-character).
7. **Casting**: per session, any single active host or any pair. Pairs of two user-created characters are allowed. [NEW: explicit]
8. **Voices**: target 12 per launch language (mixed gender/age/energy/dialect). If fewer exist at launch, character creation offers what exists; never blocks.
9. All characters read the same learner file: identical pedagogy, different costume.

---

# PART 8 — LEARNER FILE (DATA SPEC)

Four sections, one record per user:

1. **Their life**: interests (with salience scores), people mentioned, ongoing situations, dated follow-ups (with due/used state), register situation, goal.
2. **Show history**: per session — topic, format, cast, positions the user took, jokes that landed (host-detected engagement moments), completion state.
3. **What works on them**: format completion rates, talk-inducing topics (call-in word-count by topic), host engagement per character, abandonment patterns, preferred session times.
4. **Language profile**: level band + confidence, per-category error rates, target queue with lifecycle states, vocabulary rings (confident/emerging/unseen × receptive/productive), avoidance flags, fluency baselines, energy state.

Update rules:
- One post-session pass updates all four sections and runs assessment extraction, within 10 minutes of session end (or abandonment).
- Salience: referenced/engaged facts gain, unused facts decay per week; below threshold facts become dormant (never deleted, never referenced). [NEW: dormant, not deleted]
- Certainty: every fact carries a confidence value; only high-confidence facts may be spoken by hosts.
- User corrections ("actually I support Ahli now") overwrite immediately at high confidence.

---

# PART 9 — PLANNER (EXACT JOB SPEC)

The planner is event-hooked, not scheduled. Triggers, in priority order:
1. **Post-session hook (primary)**: runs immediately after the post-session analysis pass completes (≤10 min after session end). This produces the next day's pitches while the file is freshest.
2. **Staleness hook**: if no session occurred, pitches older than 20 hours trigger a refresh on the user's next app open — refresh runs before pitches render, budget < 5s for pitch text (pre-generation of the predicted pick continues in background). [NEW: staleness refresh + latency budget]
3. **Follow-up hook**: a follow-up seed coming due triggers a pitch refresh regardless of the above. [NEW]

One planner run per trigger; concurrent triggers coalesce into one run. The output is always a complete fresh pitch set (never a partial patch). [NEW: coalescing + full-set rule]

Steps, in order:
1. **World check**: fetch updates for stored interests (team results, relevant news), check follow-up due dates.
2. **Pitch writing**: produce 3–5 pitches per Part 3.1 constraints.
3. **Pedagogy threading**: for each pitch, attach 1–2 targets from the queue, plant frontier vocabulary, set the difficulty from the current edge and energy state. Pedagogy adapts to topic, never the reverse.
4. **Prediction + pre-generation**: rank pitches by predicted acceptance (interest salience × format history × recency); fully pre-generate the top pitch through the entire pipeline (Part 6.1) including audio.
5. Other pitches store briefs only; they generate on selection.

If the world check fails (no external data available), pitches fall back to interests + follow-ups + wildcard; the planner never fails to deliver pitches. [NEW: planner fallback]

---

# PART 10 — ASSESSMENT ENGINE (EXACT RULES)

1. **No test artifacts.** All analysis post-hoc on natural behavior. Nothing runs in the live path.
2. **Dimensions**: Accuracy (errors per 100 words by category), Complexity (clause depth, tense variety, connectors), Fluency (speech: WPM, pause ratio, fillers; text: reply latency, length trend), Vocabulary (rings × depth).
3. **Inputs**: call-in transcripts, chat messages, tap-to-define logs, replay/scrub clusters, article completion, content uptake.
4. **Error taxonomy**: fixed 12 categories, localized per target language. English reference set: verb tense/aspect, subject-verb agreement, articles, prepositions, word order, word choice, plurals, pronouns, comparatives, conditionals, question formation, register. Raters receive the closed taxonomy + band descriptors + anchor examples; output structured tags only, no free text.
5. **Error vs. slip**: a pattern requires ≥3 observations across ≥2 sessions to enter the target queue.
6. **Avoidance detection**: weekly job compares structures expected at the user's band against structures ever attempted; never-attempted expected structures get flagged for receptive introduction.
7. **Content uptake**: per session, LLM-rated 0–2 — does the call-in argument reflect the article's actual content?
8. **Cadence**: per-session light extraction (errors, new vocab, target produced y/n). Weekly deep CAF rating over pooled production on 1-week and 2-week windows; on sharp disagreement the 2-week window wins.
9. **The edge**: difficulty setting = current band + energy modifier. Energy detection inputs: reply lengths, skipped call-ins, error spikes (ease next session one step); sustained fluent streaks (raise one step). One step per session maximum. [NEW: step cap]
10. **Targeting**: readiness rule — only imperfectly-attempted structures are productively targeted; never-attempted structures get receptive exposure (hosts use them in banter) for 1–2 weeks first. Queue: max 4 active; 1–2 threaded per session; selection = frequency × recency × readiness. Lifecycle: Active → Taking (produced correctly unprompted once) → Retired (correct 3+ times across 2+ sessions) → Re-check at 2, then 4, then 8 weeks; failed re-check → Active.
11. **Correction, three layers**: (a) in-flow recast-only — correct form embedded in a reply that has its own conversational point; (b) on explicit request — plain honest explanation, in-character; (c) weekly — patterns surfaced in the Proof. Unsolicited explicit correction: never.
12. **CEFR anchoring**: internal only. The words "level," "CEFR," "beginner/intermediate/advanced," or any synonym never appear in any user-facing surface.

---

# PART 11 — WEEKLY PROOF

1. Generated weekly per user who completed ≥2 sessions that week; skipped otherwise (no "you missed your proof" messaging — it simply arrives next qualifying week). [NEW: qualification rule]
2. Format: ~2-minute audio mini-episode by the user's most-used cast that week. [NEW: cast selection rule]
3. Mandatory contents: one side-by-side moment (audio clips if consented; verbatim text quotes otherwise), 1–3 named concrete wins ("eleven days since you last said *I go yesterday*"), one teaser of the next focus.
4. Flat-week rule: if the weekly CAF shows no improvement, the proof says so plainly ("Flat week. Happens to everyone. Here's what we're changing") and names one concrete planner change. Fabricated wins are prohibited; the generator receives only real deltas from the learner file.
5. Delivery: appears at the top of the pitch list on the chosen day (default: the user's highest-completion weekday). [NEW: delivery slot]

---

# PART 12 — ARCHIVE, TRUST, DATA, TELEMETRY

1. **Archive**: every episode (re-playable), transcript, article, call-in recording (if consented) or transcript, and chat, browsable by date. No stats, charts, or aggregates anywhere in v1.
2. **Milestones**: host-spoken only, rare (50th show, 100th show). No visual celebration of any kind.
3. **Knowledge summary**: on request ("what do you know about me"), the show renders a plain-language summary of life facts and interests. The language profile is never included.
4. **Correction**: the user corrects facts conversationally; applied immediately.
5. **Voice consent revocation**: immediate flag flip + deletion of all stored audio clips within 24h.
6. **Security**: encryption at rest, row-level isolation per user, no cross-user data access paths.
7. **Cost telemetry**: every session records fully-loaded model + synthesis cost. Reported weekly against the 2-sessions/day worst case. Mandatory from beta day one.
8. **No notifications** in v1 except transactional email (account verification only). No re-engagement email ever. [NEW: reduced to verification-only after removal of export/deletion]

---

# PART 13 — MULTI-LANGUAGE ARCHITECTURE RULES

1. All prompts, taxonomies, band descriptors, and chassis documents are per-language configuration, not code.
2. The error taxonomy structure (12 categories) is fixed; category contents localize per language.
3. Voice inventory, dialect lists, and the default duo are per-language content packages.
4. Adding a language = adding a content package + configuration; zero re-architecture. This is enforced by building the first language through the same package mechanism. [NEW: enforcement rule]

---

# PART 14 — LATENCY AND RELIABILITY BUDGETS (CONSOLIDATED)

| Path | Budget |
|---|---|
| Pre-generated episode start | < 2s |
| On-selection episode playable | < 30s (streaming) |
| First episode after onboarding | < 3 min |
| Call-in voice response | < 1.5s end-to-end |
| Tap-to-define popover | < 300ms |
| Post-session analysis | ≤ 10 min |
| Planner (post-session trigger) | completes within the same 10-min post-session window |
| Planner (staleness trigger) | pitch text < 5s at app open |
| Voice-clip deletion on consent revocation | ≤ 24h |
| Live-voice failure | graceful degrade to async voice-notes, zero session loss |

---

# PART 15 — SUCCESS METRICS (BETA, FIRST 90 DAYS)

| Metric | Target | Measurement |
|---|---|---|
| Sessions/user/week (zero reminders sent) | ≥ 4 | session start events |
| Target retirement within 3 weeks of activation | ≥ 50% | target lifecycle log |
| Week-4 retention among users with ≥1 Proof | ≥ 40% | cohort analysis |
| Full-cycle completion | ≥ 60% | state machine `complete` rate (pauses allowed) |
| Call-in participation | ≥ 70% | sessions entering `speaking` |

---

# PART 16 — OUT OF SCOPE (v1 EXCLUSIONS — DECIDED)

Character sharing · proof-clip social sharing · human guests · duo-shows with friends · community · native apps · pronunciation scoring · non-language domains · notifications beyond transactional email · audio in tap-to-define · playback speeds above 1.0× · settings screens of any kind · statistics/charts in the archive.

# PART 17 — REMAINING OPEN DECISIONS (COMPLETE LIST)

1. Launch language(s) and dialect list per language.(answer:All the languages that are supported by the text-to-speech and speech-to-text provider  )
2. Business model, pricing, trial.(answer:To be decided later. )

# PART 18 — MILESTONE 0 GATE

Before any of the above is built: one complete cycle hand-produced for one real user (LLM-assisted script, generated audio, faked backend). Pass condition: the user, unprompted, wants the next episode. Fail → revise the thesis, not the backlog.

---

**Reading rule:** everything in Parts 1–16 is settled — build as written. [NEW] tags mark decisions made in this document; veto them now or they stand. Part 17 items are the only open questions. If a question during implementation is answered nowhere here, it escalates before it is built.