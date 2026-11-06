# For one, concept v2

*Written 2026-10-09; updated 2026-10-23 with Muath's answers to decisions 1 to 4 and his pick of a producer in the UI and UX thread. Merges the first rethink and the eleven lens perspectives in /mnt/project-files/perspectives/. Page: https://claude.ai/code/artifact/7064a875-8cc4-41b8-a571-494d3e99d639. The decision list is in [decisions.md](decisions.md). Where Muath has not answered, the text assumes the recommended answer.*

**For one is your own private teacher who makes you a daily show.** It knows your words, your errors and your life, makes something new for you every day, proves you are improving in your own voice, and keeps you coming back without a single game mechanic. It never tells you that you were wrong.

## 1. The decisions that gate everything

Forty-eight questions across twelve threads collapse into ten decisions, and five of them change everything else. Muath answered decisions 1 to 4 on 2026-10-23; decision 5 stands on his Oct 10 go-ahead. The full list, with every option's consequence, is in [decisions.md](decisions.md).

| # | Decision | Status | What stands now |
|---|---|---|---|
| 1 | Who it is for, and which languages | Decided by Muath | No launch country or group of people. Every target language the speech technology carries well, decided by a language gate (section 8). |
| 2 | Price and daily allowance | Decided by Muath; tiers costed here | Monthly only, three plans by new episodes a day: 1 a day $19.99, 2 a day $29.99 (recommended), 3 a day $44.99. Listening to what exists is unlimited on every plan. |
| 3 | How teaching works | Decided by Muath | Invisible. The hosts answer like a friend would ("oh, you went there yesterday?") and carry on. No "that's wrong", no pop-ups, no correction notes. A producer, Muath's pick in the UI and UX thread, is the face of the app in the learner's own language, and she never corrects either. |
| 4 | Evidence instead of "no tests" | Agreed by Muath | Recall in conversation, a 60-second word check, a then-and-now recording every 4 weeks, a notebook the learner can open. Still no points, streaks or levels. |
| 5 | A series, not one-offs | Accepted with Muath's Oct 10 go-ahead | Plot may persist, obligation never. 4-week seasons, each with one real-world goal. |

The other five (cue and return, platform, personalization depth, data use, how the beta earns) are built on their defaults and can change later.

**What Muath's answers changed.** Decisions 1 and 3 overruled points every lens had agreed on: one market first, one language pair, and corrections that become explicit after the call. The concept now follows his calls. The risks they add are named in section 10 together with what tests them. The two answers also help each other: because nobody corrects, the producer's lines in the learner's own language are few and simple (welcome, the notebook, the weekly proof, answers when asked), which keeps supporting many native languages cheap.

## 2. The thesis

**Show, teacher, proof, rhythm.** The first rethink's three-part bet holds after eleven lenses tested it; the consistency lens adds a fourth part the original design had no answer for.

1. **The show earns the time.** Fluency takes hundreds of hours, and only something people want to hear accumulates them. The show is made from the learner's interests, pitched at about 95% known words for audio and 98% for text, and runs as a series with hosts they know.
2. **The teacher makes the time count, without ever showing itself.** Behind the show, one learner model knows every word and structure the learner has met and how likely they are to remember it. It brings words back on schedule, puts the right form of the learner's own mistakes into the next episodes until it sticks, and sets up moments where the learner has to pull language out of memory and say it. This is where the large, replicated learning gains are; personal content alone did not improve vocabulary learning in the closest randomized test (Leong 2024).
3. **The proof keeps them going.** People continue when they can hear themselves improving: their voice four weeks ago next to today, the words they now use, the first real conversation they handled. Every claim passes a code-enforced gate, so the product is believed on good weeks because it admits flat ones.
4. **The rhythm carries them through the months.** Wanting to learn is rarely what runs out; the routine is. A cue the learner designs, a weekly rhythm with spare days, a small door for bad days, a return episode after gaps and seasons with near goals carry the 2 to 5 months before the habit runs itself.

**Why this can disrupt the market.** Talking to an AI is becoming free: Duolingo says a video call costs it under one cent, ChatGPT voice and Google Translate practice are free. So For one does not sell conversation. It sells what only the rich ever had, a private teacher who knows you, plus something no teacher could ever do, a new show about your life every day, for about the price of one or two tutor lessons a month. Duolingo owns the habit but not the outcome, and cannot drop the streaks its growth depends on; AI tutors converge on the same chatbot with the same complaints; nobody funded makes daily personal episodes. The moat is not any feature but a model of each learner's language that compounds, a measured outcome, and a trust brand.

**What changed from the original concept.** It optimized for enjoyment and hid the teacher completely. The twelve threads found the vision right and rare, but the original laws quietly removed what learning needs (recall, enough speaking, seeing improvement) and what consistency needs (a cue, a way back after a lapse, a near goal). Concept v2 keeps the teacher invisible, as Muath chose, and makes the evidence visible instead.

## 3. What the twelve threads agree on

These had no dissent and are treated as settled. Four further points the lenses agreed on (the stuck intermediate as the first learner, one language pair at launch, English for Arabic speakers as that pair, and explicit corrections after the call) were overruled by Muath on 2026-10-23 and are no longer listed.

| Settled point | Lenses that reached it |
|---|---|
| "Made once" applies to the text; the language inside returns on a spaced schedule | Rethink, learning science, personalization, assessment |
| A coverage check in code, not in a prompt: about 95% known words for audio, 98% for text | Rethink, personalization, architecture, assessment |
| A per-word, per-structure memory model (FSRS or half-life style), not vocabulary "rings" | Learning science, personalization, assessment, architecture |
| No streaks, points, badges, levels on screen, leaderboards or confetti | Every lens |
| Honest progress as evidence the learner recognizes: their sentences, their voice, hours | Rethink, consistency, assessment, UI/UX, market |
| A 4-weekly like-for-like speaking sample is the real outcome measure | Rethink, assessment, market, consistency, UI/UX, business |
| Zero notifications is the riskiest bet; one cue the learner designs replaces it | Rethink, consistency, enjoyment, UI/UX |
| Some continuity between episodes; never obligation, never a backlog | Enjoyment, consistency, personalization, language acquisition |
| Keep the trust contract, the anti-guilt stance and the bounded daily portion | Every lens |
| Speaking time is too low; count the learner's own speech, aim for 4+ minutes a session | Rethink, learning science, language acquisition, business, UI/UX |
| A 60 to 90 second retell, and the same argument again shorter the next day | Rethink, learning science, language acquisition |
| Structured memory with source quotes is the truth; models propose, code decides | Personalization, architecture, assessment |
| The call is a pipeline (speech-to-text, a text model, the episode's own voice) in the beta | Architecture, voice, business |
| Speech-to-text quietly fixes learner grammar; every call is re-transcribed verbatim afterwards | Voice, architecture, assessment |
| The host waits while the learner searches for a word; default turn-taking interrupts learners | Voice, UI/UX |
| Character creation and the six chassis are deferred until episodes are loved | Rethink, enjoyment, business, UI/UX |
| Milestone 0, hand-made for 10 to 15 real people, before any product code | Every lens that discussed launch |
| Shorter onboarding: sound within a minute, a 3-minute intake, the first call within 5 minutes | UI/UX, personalization |

## 4. Where they disagreed, and what I picked

Evidence and judgment are kept apart: the "Positions" column is what the lenses said; the "Pick" and "Why" columns are this synthesis's judgment. Three conflicts from the first version (the price, the daily allowance, and who corrects) were settled by Muath and are covered in sections 1, 5 and 8.

| Conflict | Positions | Pick | Why |
|---|---|---|---|
| Cost per session | Rethink $0.20 to $0.45 budget, $1 to $1.50 premium; architecture $0.43 / $0.62 / $1.89; business $0.25 / $0.55 / $1.11 / $2.01; voice lens audio alone $0.30 to $0.55 value, $0.75 to $0.85 premium | Beta budget $0.60; planning cost $0.35; stop line $1.00 | The spread comes from three choices: a cascade call versus a realtime speech model, batch versus on-demand voices, and Opus versus Sonnet for planning. All lenses agree voice and the call are about half the bill. |
| "Never plot" | PRD law 4; enjoyment arcs; consistency optional threads; personalization light continuity; SLA topic threads | Plot may persist, obligation never | Unanimous among lenses that addressed it. |
| Season length | Consistency 6 to 8 weeks; enjoyment 4 to 6; UI/UX 4 | 4 weeks | Lines up with the 4-weekly recording, lands inside the week-4 gate, matches the novelty fade. A long goal runs across two seasons. |
| Platform for the beta | PRD web only; rethink and business web app plus private feed; UI/UX native; voice: web calls stop when an iPhone locks | Web app plus private podcast feed; calls screen-on; test a dial-in number; native after the gates | The feed covers the listening (60 to 70% of time) on the lock screen; a single founder ships web faster. Switch early if calls die on the commute. |
| Weekly proof cadence | PRD only in weeks with 2+ sessions; consistency: always | Always; shorter in a slow week, about what has built up over time | Withholding it hits exactly the learners who are slipping. |
| Proof in the first build | Architecture: phase 2; rethink and business: in the first paid version | In the beta, simple | It is the strongest evidence-backed retention lever; most of it is code (the claim gate) plus a short script. |
| When the learner chooses | PRD pitches at app open; enjoyment: tomorrow chosen tonight; UI/UX one hero plus two ideas behind a tap | Chosen at the end of today's session from 3 ideas; if skipped, the planner's pick waits as the hero | Anticipation, and no decision at the moment of starting. |
| Transcript | PRD always on; SLA audio-first; learning science fades with level; UI/UX on with hide option | Audio-first on the first play for intermediates, a "Huh?" button, the planner adjusts per learner | Decoding practice and support are both needed, in that order. |
| Praise | PRD never praises; consistency specific, rare praise; learning science never person-praise; UI/UX "new for you" card | Specific, rare, about the task: "you argued for four minutes in the past tense" | All four agree once person-praise is separated from task feedback. |
| Pronunciation | PRD out of scope; SLA light; voice: score only on a known sentence; UI/UX no scores | Tap to hear, shadow two lines; scored internally on a known sentence only | Being understood is a real goal; numbers on screen are banned. |
| Who writes life memory | PRD single post-session pass; personalization and architecture: models propose, code validates quotes | Quote-backed facts with confidence, only after-session roles write | Commercial AI memory answers 57.7% of long-term questions and invents some; a wrong memory is a bug. |

## 5. The laws, v2

Two sets of laws existed: the concept's nine and the PRD's six hard laws. They merge into twelve. Five stand as written, four change, three are new.

| # | Law | Status | What changed and why |
|---|---|---|---|
| 1 | **No game furniture.** No streaks, points, badges, levels on screen, percentages, leaderboards, charts or confetti. Evidence the learner recognizes is allowed. | Changed | Was "no lesson furniture: no levels, tests, prompts...". Recall, a word check, a 4-weekly recording and honest progress are evidence, not games (decision 4, agreed). |
| 2 | **Every moment has a hidden shape and a social surface.** | Stays | |
| 3 | **The learner owns topic, format and cast; the teacher owns pedagogy and shows its reasons on request.** The learner can veto or add to what the teacher works on. | Changed | Was fully hidden. A glass box makes deep memory trusted (decision 4). |
| 4 | **Every episode is complete. Plot may persist; obligation never.** The story waits for the learner. | Changed | Was "only memory persists, never plot" (decision 5, recommended). |
| 5 | **Honesty about what it is.** Transparently AI; no guilt, no "I miss you", no fake lives. | Stays | Now partly required by law (California SB 243 for recurring AI characters); build disclosure and a self-harm protocol in. |
| 6 | **Formats are hijacked, not invented.** Podcast, call-in, group chat, a notebook. | Stays | Milestone 0 follows it literally: WhatsApp and a podcast feed. |
| 7 | **Teaching is invisible.** Nobody tells the learner they were wrong. The hosts answer the way a friend would: "oh, you went there yesterday?" and carry on, or "sorry, you what?" when the meaning is lost. The right form then keeps coming back in later episodes and calls until the learner uses it. No pop-ups, no red marks, no "the correct answer is", no correction notes. Explanations only when the learner asks. Nobody interrupts a learner mid-sentence or praises the person. | Stays, sharpened | Muath's call (decision 3). The first version of concept v2 added explicit notes after the call; those are gone. |
| 8 | **Conversations end like conversations.** Clean goodbyes, never homework. | Stays | |
| 9 | **The show is the gym; life is the game.** Real-world tries are offered and celebrated above everything else. | Stays, now a mechanic | Real-world tries, an "out in the world" log, and real-life rehearsal before the learner's actual interview or trip. |
| 10 | **The text is used once; the language comes back.** | New | Every episode is new, and target words, structures and the right forms of the learner's own mistakes return on a spaced schedule until the learner owns them. |
| 11 | **A finite, good portion.** One, two or three new episodes a day depending on the plan, each with a clear ending, no autoplay and no feed. What is already made can be heard as often as wanted. | New | Replaces the 2-session cap with a generation cap per plan, so listening hours can grow (decision 2). |
| 12 | **No claim without proof.** Every statement about the learner's progress passes the claim gate: like for like, beyond the noise, repeated, from clean evidence, and openable. | New | The trust contract's "prove progress honestly", made into code (assessment lens). |

**The trust contract** keeps its five promises (never lie, never manipulate, never hide what it is, prove progress honestly, the data is theirs) and adds three: **told, not inferred** (the show uses only what the learner said to it); **a wrong memory is a bug** (fixed at once, counted as a quality metric); **data use is opt-in** (anonymized transcripts only with consent, off by default). "Never manipulate" also covers pricing: no fake countdowns, fake scarcity, hidden cancellation or guilt (section 8).

## 6. The experience

The example learner is Faisal, 27, a sales engineer who studied English for years, understands most of what he hears, freezes when he speaks, supports his football club, and has a job interview in six weeks. He is one example among many: nothing in the product is written for one country, and the same flow serves a nurse in Manila learning Japanese or a student in Lyon learning Spanish. His hosts are Karim and Mona. His producer is Salma, who speaks to him in his own language, keeps his notebook and never corrects him.

### The first ten minutes

1. **Sound within a minute.** One screen, one tap, an age checkbox. Salma's voice, in his own language; the screen's text is too.
2. **Three minutes with Salma.** What should the hosts call you? What could you talk about for an hour? What do you need it for? Each fact appears as a card he can correct or delete. Twice she switches to the language he is learning for a line, which, with an optional 60-second word check, sets the starting level.
3. **Casting while the pilot is made.** He hears each host say hello and can swap a voice; he picks an accent.
4. **A 2 to 3 minute pilot** about the thing he could talk about for an hour, then Karim throws him a question and **a 60 to 90 second first call**. Mona tells him once: if a word won't come, hold the button and say it in your own language.
5. **One specific thing he managed**, said by the hosts, then the account, the drop time ("on my commute, 7:40") and voice-storage consent, asked right after he heard himself. His 7-day trial starts on the 2 a day plan.

### A day

| When | What happens | Who |
|---|---|---|
| Last night, end of the chat | Faisal picked tomorrow's episode from three ideas: "Mona interviews you for the job, and she is not nice." | Hosts, planner |
| 7:40, on the bus | It drops into his podcast app. A 30-second cold open calls back three words from yesterday in a new line, then asks how he would say the episode's key idea. | Hosts |
| The episode, 5 to 7 minutes | Audio-first. The interview arc's second episode. His target words sit inside the jokes and the personal moments, and the hosts use, many times and naturally, the two forms he got wrong yesterday. "Huh?" replays any sentence slower. It ends on a question he is about half sure of. | Hosts |
| The call, 5 to 7 minutes | Mona pushes back. When he says "I go there yesterday", she answers "oh, you went there yesterday? And what happened?" and carries on. When the meaning is lost she asks "sorry, you did what?". Twice she leaves a gap for a word from last week; once she asks for a 60-second retell. Hold-to-talk keeps the floor while he searches; when he says a word in his own language, she gives it back in the language he is learning and keeps going. Target: 4+ minutes of his own speech. | Host |
| Right after | Nothing to read. The goodbye is a goodbye. Behind the scenes the analyst logs what he said, and the errors that matter most become material for the next episodes. | Analyst (unseen) |
| Lunch, at a desk | The article that arms him for round two, with audio for reading while listening; then a short chat with Mona that ends with tomorrow's choice. If he asks "why do we say it like that?", she explains, because he asked. | Hosts |
| A bad day | The small door: the hosts' 90-second recap and one voice note back. It counts fully. | Hosts |
| A second visit | On the 2 or 3 a day plan, a second new episode. On every plan, "round two": the same argument, shorter and faster, plus a re-listen. | Hosts |

### A week

- **A rhythm, not a streak.** Faisal chose "4 days, 2 spare". The show mentions it only in words ("four times this week, as you planned"); no counter, calendar or flame exists.
- **The weekly proof** arrives on his chosen day, every week: a 2-minute episode from Salma with one headline piece of evidence that passed the claim gate ("on Tuesday you told the whole story in the past tense") and what the show will focus on next. A slow week gets a shorter proof about what has built up over time. A flat week says so and names the one thing the teacher is changing. It shows what he can now do, never a list of his mistakes.
- **The notebook** is Salma's and always open to him: what she knows about him (each fact with its source), words he owns in his own sentences, the tape, hours heard and minutes spoken, "why this episode", and a "working on" list of at most 3 items he can veto or add to.

### A season (4 weeks)

- **One real goal in his words:** "get through the interview without freezing".
- **Arcs** run inside it: the interview prep, the day, the debrief. At most two arcs are open at once, and they wait if he is away.
- **Mid-season**, a real-life rehearsal of the actual scene.
- **The finale** is the then-and-now recording (about 3 minutes, the same task types every time), played next to the last one, with at most two measured differences in plain words, the real-world attempt, and next season's goal set inside the finale so finishing never becomes a reason to stop.

### A year

| Phase | What usually goes wrong | What carries the learner |
|---|---|---|
| Days 1 to 14 | The first live call scares; no routine yet | The anchor plan, a short first call, the day-2 callback to something said in onboarding, one specific win named in week 1 |
| Weeks 3 to 10 | Novelty fades around week 4; the first lapse | The weekly rhythm, the small door, the return episode, the first season finale |
| Months 3 to 6 | Progress gets harder to feel; episodes feel alike | A new season goal, then-and-now over 3 months, the variety system, a guest host or new format |
| Months 6 to 12 | Moves, trips and new jobs break the cue | Re-anchoring when life changes, pause without penalty, bigger real-world goals, a year-in-review episode |

**After a gap**, one opt-in note Faisal wrote to himself at signup arrives once ("It's you from October. The interview is in March."). The first session back is a return episode: one step easier, opening from his life, never mentioning the days missed, with a quick real win.

### What keeps it from going stale

AI-written stories converge on the same plots and names, so a variety system sits next to the trust contract: real input every day (his life, today's news on his interests, his own words from the last call); a ban list of stock names and tropes; format rotation tracked over the last 10 episodes; a similarity check in code across his last 20 episodes; and hosts written by people, with the model writing only the episodes.

## 7. Agents and stack

**One teacher with many faces, not a swarm of bots.** Thirteen narrow roles, eleven in the first beta; each is a pipeline step with fixed inputs and outputs. Only the call host must be fast. Everything that needs deep thinking runs before or after the session, where it can be slow, cheap and checked.

**The learner meets three voices and nothing else:** the hosts (the show, in the language being learned), the producer Salma (the face of the app, in the learner's own language at first and more in the new language as they grow), and themselves. Nobody corrects. The teacher behind them decides what the hosts say and what Salma shows. The producer's correction notes from the first version are gone, because Muath chose invisible teaching.

| When | Role | Job | Model class | In beta? |
|---|---|---|---|---|
| Before | Teacher (showrunner) | Reads the whole learner model; picks 1 grammar target, the forms to bring back from the learner's own mistakes, and 2 to 4 due or new words by need, goal fit, readiness, learnability, opportunity and what is due; plans arcs, the weekly mix and 3 ideas for tomorrow | Strongest reasoning model, batch | Yes |
| Before | Writer | Script, article, call brief with planned host moves that make targets necessary and bring the right forms back naturally, chat opener | Strong creative model | Yes |
| Before | Fitter | Measures known-word coverage and new-word count; sends failing sentences back for a rewrite | Code plus a small model | Yes |
| Before | Editor | Pre-ship gate: language correctness, no uncertain memory, the fun carries the language, nothing that reads as a lesson or a correction, the variety check, no law broken, "would this person pick this over a real podcast?" | Mid model from a different vendor than the writer | Yes |
| Before | Voice studio | Two-voice audio, word timings, name pronunciations, a re-listen check | Text-to-speech plus speech recognition | Yes |
| Before | Scout | Results and news for stored interests, shared per topic | Small model plus search | Later |
| Live | Host | The call and the chat: argues, answers errors with a friendly "you meant…?" and carries on, asks when meaning is lost, leaves recall gaps, asks for the retell, gives a word back when the learner says it in their own language, explains only when asked; waits while the learner holds the floor | Fast mid model in a voice pipeline, same voice as the episode | Yes |
| Live | Observer | Reads each learner turn and whispers to the host which form to echo back next turn; never adds delay. More valuable now that all correction happens through the host | Small fast model | Phase 2, first to add |
| Live and after | Producer (Salma) | Onboarding, life updates, "tell Salma an idea", the notebook, the voice of the weekly proof, explanations when the learner asks. Never corrects, never sends notes | Conversational model with voice; strong text model for the proof | Yes |
| After | Analyst | Verbatim re-transcription, minimal-edit corrections classified by rules into the structure inventory, fluency from timings, words used and understood | Small model with a fixed schema, checked by code | Yes |
| After | Memory keeper | Life facts with the exact quote, confidence, sensitivity and expiry; show canon and cast memory | Small model plus rules | Yes |
| Weekly | Proof producer | Turns claims that passed the gate into the weekly proof script and picks the clips | Strong text model plus the voice studio | Yes, simple |
| Every 4 weeks | Recording rater | Rates the then-and-now recording, calibrated per language against teacher tags | Calibrated model plus code metrics | Yes |

**Code, not AI:** the review scheduler (FSRS-style, per word, per structure and per corrected form); the lexicon (lemmatizer and known-word probabilities); the gloss cache shared by all learners; the coverage check; the similarity check; the claim gate; cost tracing on every call; the language gate's test harness.

**Three rules for memory.** Live roles never write to the learner model; only after-session roles do, from an append-only event log, so the whole model can be rebuilt when the analyst improves. Every life fact carries the learner's exact words and a confidence, and only confirmed facts reach a host's mouth. Each role gets a compiled brief, never the whole file.

**Languages as packages.** Each target language is a package: its episode voices, its speech recognizer for learner speech, its lexicon, its structure inventory and its calibration set. A package ships only when it passes the language gate (section 8). The learner's own language needs only interface text, glosses, and a recognizer that catches it when the learner switches mid-sentence.

**The stack at a high level.**

| Layer | Beta default | Milestone 0 |
|---|---|---|
| Episode voices | Per language, the winner of a blind native-listener test among Gemini 3.8 Flash TTS (130+ languages), Inworld TTS-2 (200+ claimed) and ElevenLabs v4 (90+), generated overnight in batch | Gemini 3.8 Flash TTS, two speakers |
| The call | Pipeline on LiveKit Agents: streaming speech-to-text chosen per language (Deepgram, Soniox or another that passes the learner-clip test; code-switching support varies by vendor), a Sonnet-class host with a cached brief, the episode vendor's low-latency voice; adaptive turn detection and backchannels | An ElevenLabs agent link per learner with patient turn-taking |
| Learner transcript | Batch re-transcription in verbatim mode, tested per language on 30 real learner clips before trusting it | Same, checked by hand |
| Text models | Opus-class teacher in batch; Sonnet-class writer and host; Haiku-class fitter, analyst and observer; a second vendor for the editor | Prompts in a chat model, run by hand |
| Orchestration | A durable workflow engine (Temporal or Inngest) calling model APIs directly; no agent framework | None |
| Data | Postgres for the learner model, encrypted object storage with per-learner keys for audio | A spreadsheet and a shared doc |
| Delivery | Installable web app with its interface in many languages (including right-to-left), private podcast feed, web checkout | WhatsApp only |

Every vendor sits behind a thin adapter; prices move both ways (several Gemini 3.8 prices double on 2027-01-01; Hume shuts its voice APIs on 2026-11-13).

## 8. Who it is for, which languages, price and cost

**Who it is for.** Anyone, anywhere. There is no launch country and no target group, so nothing is tuned to one culture: each learner's show is built from their own life and interests. The one real limit is level. A show is easiest to follow from about 2,000 known words (rethink, business and voice lenses), so people who already know some of the language get the best version. True beginners get a slower, shorter show with more help in their own language, and that version is the least tested.

**Which languages.** As many target languages as the technology carries well, decided by a test rather than by a vendor's list. Voice vendors list 44 to 200+ languages, but none publishes quality per language, and transcribing learner speech without silently fixing it is the hardest part outside English (voice lens). A language opens when it passes the language gate:

| Check | What passes |
|---|---|
| Episode voices | 5 native listeners rate two-host episodes from 3 vendors blind; the winner is one most of them would listen to |
| Learner speech to text | On 30 real learner clips, the verbatim transcript keeps the learner's errors instead of fixing them, and catches words said in the learner's own language |
| Writing | A native speaker reads 10 scripts and finds them natural and correct |
| The call | The host answers within about a second on that language's speech stack |
| Structures | A structure inventory exists (English has the English Grammar Profile; other languages get one drafted by a model and checked by a native teacher) |

My estimate, not a test result: English passes easily, and the large languages (Spanish, French, German, Italian, Portuguese, Japanese, Korean, Mandarin, Arabic, Hindi, Turkish, Russian) are likely next. Progress claims in a new language start more cautious until its calibration set exists. The learner's own language is a much lower bar, since it only needs interface text, glosses and recognition when the learner switches into it. The producer speaks it too, but because she never corrects, her lines are few and simple.

**What is sold.** A monthly subscription, priced against a private teacher, with a measured outcome: the then-and-now recording every 4 weeks is the promise. Three plans differ only in how many new episodes are made each day. Listening to what is already made, the article, the chat and a short round-two call are unlimited on every plan, because they cost almost nothing.

| Plan | Price a month | New episodes a month | Price per episode | Practice a day, roughly |
|---|---|---|---|---|
| 1 a day | $19.99 | 30 | $0.67 | 20 to 25 minutes |
| **2 a day (recommended)** | **$29.99** | **60** | **$0.50** | **40 to 50 minutes** |
| 3 a day | $44.99 | 90 | $0.50 | About an hour, like Muath's own routine |

**How the cost sets the price.** The rule is that no plan may lose money on a learner who uses every episode, at the planning cost of $0.35 a full session (the scale target, which already allows for Gemini's January price rise). The assumptions are my estimates: about 15% of the price goes to tax and payment fees on average, and typical learners use 60% of the 1 a day allowance, 50% of 2 a day and 45% of 3 a day.

| Plan | Net a month | Typical episodes used | Margin, typical use | Margin, every episode used | Highest cost per session that still breaks even at full use |
|---|---|---|---|---|---|
| 1 a day | $16.99 | 18 | 63% | 38% | $0.57 |
| 2 a day | $25.49 | 30 | 59% | 18% | $0.42 |
| 3 a day | $38.24 | 40 | 63% | 18% | $0.42 |

The beta runs at about $0.55 to $0.60 a session, so a beta learner on 2 or 3 a day who uses every episode costs more than they pay until the cost falls below $0.42. With about 50 beta learners that is at most about $560 a month even in the worst case, which is acceptable as research. The intensive plans are the reason the floor-stack work in section 9 matters.

**How the pricing pushes people to subscribe, honestly.**

- **Three plans, the middle one marked "Recommended".** People lean toward the middle of three options (the compromise effect, Simonson 1989). It is labeled "Recommended", not "Most popular", until that is true.
- **The top plan is the anchor.** $44.99 makes $29.99 feel reasonable, and because 2 a day and 3 a day cost the same per episode, the step from 1 to 2 is the obvious deal (the decoy effect, Huber, Payne and Puto 1982; Ariely's Economist test).
- **Price per day.** "About $1 a day" for the recommended plan (the pennies-a-day effect, Gourville 1998).
- **The trial starts on 2 a day.** After 7 days the learner picks a plan, and dropping to 1 a day feels like giving something up. A trial costs about $4 to $8 per person at beta cost.
- **No free tier.** A free 90-second sample episode about the person's own life comes before signup, then the trial. Hard paywalls convert about 10.7% of downloads against 2.1% for freemium, with similar one-year retention (business lens).
- **Founding members keep their price.** The first 100 paying learners keep their plan's price for as long as they stay subscribed. That is believable because some AI prices are rising.
- **The real comparison is shown.** A tutor costs about $160 a month for two lessons a week.

**Never:** fake countdowns, fake scarcity, hidden or hard cancellation, guilt messages or pre-ticked upgrades. Cancelling takes one tap. These would break "never manipulate", and the trust brand is part of the moat.

**Regional prices.** One USD price list at launch. Lower prices for lower-income countries come once there is data on where learners come from; the app stores already adjust prices by country.

**Cost per full session** (episode, article, call, chat, a share of the weekly proof), from list prices on 2026-10-09. These are the lenses' estimates, not measurements.

| Stack | Per session | What it uses |
|---|---|---|
| Floor (scale target) | $0.25 to $0.36 | Batch for everything not live, Flash-Lite voices, a cascade call on a small model; rises to about $0.36 when Gemini prices double |
| Recommended (beta) | About $0.55 to $0.60 | Opus teacher in batch, Sonnet writer and host, one voice vendor for episode and call so the host sounds the same |
| Premium | $1.10 to $2.00 | Realtime speech-to-speech call, premium voices everywhere |

Voice and the call are about half of every stack. **The rule:** the beta can afford the recommended stack; the announced prices must work at the planning cost. A cost above $1.00 a session with no plan to reduce it is a stop signal.

## 9. Launch sequence and gates

Dates match the Milestone 0 pilot kit (milestone-0/03-schedule.md, re-dated 2026-10-23): the first version's dates slipped by about two and a half weeks while the decisions were open. If a gate fails, find which claim failed (the show is not wanted, the teacher is not felt, the price is wrong) before writing more code.

| Phase | When | What happens | Gate to pass |
|---|---|---|---|
| Milestone 0, hand-made | Oct 24 to Nov 18 (recruiting first, episodes from Nov 1, gate decision Nov 18) | 15 learners from anywhere for 14 days, recruited through Muath's own network. Because every episode is checked by hand, the target language is one the checker can judge: English, plus any language for which Muath has a native-speaker helper. Episodes written with model help, delivered by WhatsApp; calls on an ElevenLabs agent link (one agent per learner, patient turn-taking); every call tagged by hand. Start and end recordings (week 0 at intake, week 3 on day 15, after the finale). Alternate personal and generic episodes at the same level. One blind comparison against a human-made learner podcast. In parallel, run the language gate on the candidate languages. The sample-episode waitlist opens. | 10 of 15 ask for the next episode unprompted; median 4+ sessions a week; 4+ minutes of their own speech a session; in week 2 most still choose tomorrow's episode and say the week was worth it; the day-14 recording is better, judged blind, on at least one of accuracy, fluency or complexity for most; the errors the show echoed back appear less often by day 14; personal days beat generic days; 5 of 15 pre-pay |
| Build the beta | Nov 18 to Dec 22 | Web app, private feed, the call pipeline, weekly proof, the notebook, the claim gate, the three plans and checkout, cost tracing, language packages for every language that passed the gate | A measured cost per session and a costed path to $0.35 or less |
| Paid founding beta | Dec 23 to Jan 26 | About 50 a week into 7-day trials, in every language that passed; 20 to 30 take an external test at week 0 and week 8 | Trial to paid 30%+ (stop under 15%); active in week 4 40%+ (stop under 25%); 4+ sessions a week (stop under 2.5); 4+ minutes of speech a session (stop under 2); the 4-week recording improves for most; second-month renewal 60%+ (stop under 40%); "very disappointed" without it 40%+; cost under $0.60 (stop over $1.00 with no plan); false-claim rate under 5%; wrong memories under 1 in 100 callbacks; no open language far behind English on "worth it" (close it until fixed) |
| Public launch, worldwide | Months 4 to 6 | Every language that passed, at the three plans; move to the floor stack piece by piece with blind tests; real-life rehearsal and bring-your-own-input as the first add-ons | Retention and renewal hold at public prices; the plan mix keeps the blended margin above about 50% |
| Native apps and paid acquisition | Months 6 to 9 | One-codebase native app for hands-free calls and lock-screen control; paid ads only now, behind the hard paywall | Cost per payer under about a third of what a payer is worth |
| More languages and regional prices | Months 9 to 12 | Each new language opens as soon as it passes the gate; regional prices for lower-income countries, with a cheaper listen-first plan | Margin at local prices |
| Year 2 | | Employer and university seats (the proof becomes the progress report, with consent); human bridges (a real tutor who receives the learner file) | |

**Not in the beta:** character creation and the six chassis, the world-news scout, languages that have not passed the gate, native apps, settings beyond a short controls sheet, the observer, referral programs.

## 10. The riskiest assumptions

| Assumption | Why it is risky | What tests it |
|---|---|---|
| A personal AI episode is chosen over a real podcast day after day, not just on day 1 | AI stories converge on the same plots and names; listeners rate AI writing about 6% lower when told; non-experts and AI judges overrate AI stories | Milestone 0's week-2 "still choosing tomorrow" and "worth it", the blind comparison, the variety system's similarity score, a monthly human read of 10 random episodes per learner |
| Learners fix their errors when nobody tells them they were wrong | Echoing back the right form is the least-noticed kind of feedback; immersion learners can stay fluent and inaccurate for years (Canadian immersion); speech-to-text may hide the errors the teacher needs. Every lens recommended explicit notes after the call; Muath chose invisible teaching | The day-14 and 4-weekly recordings judged blind: do the errors the show worked on fall? If an error survives two recordings, the teacher raises how often the right form comes back and how often the host echoes it, still without saying it was wrong. The 30-clip recognizer test per language |
| Quality holds across many languages | No vendor publishes quality per language; learner speech is transcribed worst outside English; most languages have no structure inventory | The language gate; "worth it" and false-claim rates per language in the beta; a language that falls behind closes until fixed |
| People come back without streaks | The default is near-total loss within a month (about 4% at day 30 for education apps) | Week-4 and week-12 retention, return rate within 14 days of a 7-day gap, weeks on rhythm |
| The cost per session fits the price | Nothing amortizes; cost rises with engagement and with the 2 and 3 a day plans; vendor prices can rise | Cost tracing from the first learner; the floor-stack migration with blind tests |
| Growth without a launch market | With no country or group, there is no single channel, community or local price to aim at, and early learners come only from Muath's network and shared sample episodes | Milestone 0 recruiting; how often the sample episode is forwarded; where waitlist signups come from |
| The internal measure is real | Hidden assessment alone correlates weakly with external tests | The external test for 20 to 30 beta learners; calibration against teacher tags (quadratic weighted kappa about 0.7, tag precision 0.8) |
| A competitor ships personal episodes first | Duolingo already generates DuoRadio at scale; Langua and Praktika could add daily stories | Speed to a loved show; the learner model and 50 episodes of shared history as the moat |

## 11. What changes in the PRD

The PRD is still the build spec; concept v2 changes these parts of it.

| PRD part | Change |
|---|---|
| 1.2 Hard laws | Replace with the twelve laws above and the extended trust contract |
| 1.3 Platform and scope | Web app plus private podcast feed for the beta; native after the gates; every target language that passes the language gate; three monthly plans of 1, 2 or 3 new episodes a day instead of a 2-session cap |
| 2 Onboarding | Sound within a minute; 3-minute talk with the producer with visible fact cards; optional 60-second word check; pilot episode and short first call before the account; drop time, voice consent and a 7-day trial on 2 a day at the end |
| 3 Daily loop | Tomorrow chosen at the end of today's session from 3 ideas; drops at the learner's chosen time; more new episodes on the larger plans; the small door; round two |
| 4 Session state machine | Doors in any order (Listen, Call, Read, Chat) with Read-before-Call as the default; planning time offered when the article is skipped |
| 5 Content | Cold open callback and try-first; audio-first player with "Huh?" and sentence replay; tap to hear any word; host moves that make targets necessary; the right forms of the learner's mistakes woven into later episodes; friendly "you meant…?" echoes and recall gaps in the call; a retell; hold-to-talk and say-it-in-your-language; no correction notes or margin notes |
| 6 Pipeline and gate | Coverage check in code with targeted rewrites; "the fun carries the language" check; a "nothing reads as a correction" check; variety and similarity check; editor from a second vendor; audio re-listen check |
| 7 Cast | Default duo plus the producer persona, who never corrects; voice swap and renaming only; character creation deferred; a series bible per learner |
| 8 Learner file | The nine-store ledger with per-word and per-structure probabilities and the learner's own recurring errors, quote-backed life facts with time and confidence, an append-only event log |
| 9 Planner | The six-factor targeting policy; due list from the review scheduler, including corrected forms; contrast pairs; arcs and seasons; a frequency floor on new words |
| 10 Assessment | Verbatim re-transcription; minimal edits classified by rules; a fine structure inventory under the 12 reporting categories, per language; separate skill estimates with ranges; the 4-weekly recording; the claim gate; "learned" means a day later, unprompted |
| 11 Weekly proof | Every week, built only from gated claims; one headline piece of evidence about what the learner can now do; "how we know" behind each claim |
| 12 Archive, trust, data | The notebook replaces the hidden file; the controls sheet; one opt-in note after a gap; opt-in transcript use; no manipulative pricing; legal review for the countries learners come from (GDPR, Saudi PDPL and others) and California SB 243 |
| 15 Metrics | Add worth-it, unprompted return, return after a gap, learner speech minutes, recording change, delayed recall, false-claim and wrong-memory rates, cost per session, plan mix, quality per language |
| 16 Exclusions | Remove pronunciation (light version in), audio in tap-to-define (in), statistics in the archive (honest progress in) |
| 17 Open decisions | Replaced by decisions.md; "every language the voice provider supports" becomes "every language that passes the language gate" |

## 12. Sources

This concept merges these twelve documents; each carries its own research sources. Pricing psychology: Simonson 1989 (compromise effect), Huber, Payne and Puto 1982 (decoy effect), Gourville 1998 (pennies-a-day framing), cited from memory rather than fetched for this update.

- First rethink, "For one: the next evolution, a rethink": https://claude.ai/code/artifact/21c354e1-9b24-4fcd-bb44-dca39f26d86b
- Learning science: /mnt/project-files/perspectives/learning-science.md
- Language acquisition: https://claude.ai/code/artifact/b1fb6113-b6d2-44d0-878b-ff6c01c09ff1 (perspectives/language-acquisition.md)
- Consistency and motivation: https://claude.ai/code/artifact/5d21e0ee-dd03-4ae9-a35c-2b4e49b20924 (perspectives/consistency-motivation.md)
- Enjoyment and pull: https://claude.ai/code/artifact/ccae704e-41dd-44e4-8cc3-cbccc641027a (perspectives/enjoyment-pull.md)
- Personalization engine: https://claude.ai/code/artifact/fae8f564-94b9-4f96-9b65-22fd1ab2c56a (perspectives/personalization.md)
- AI agents and architecture: https://claude.ai/code/artifact/44b69d3c-febd-406d-9260-fd85ba07b745 (perspectives/ai-architecture.md)
- Voice and speech: https://claude.ai/code/artifact/935520f6-7f66-4c6f-8fcc-80a5aca3807f (perspectives/voice-speech.md)
- UI and UX: /mnt/project-files/perspectives/ui-ux.md
- Market and competitors: https://claude.ai/code/artifact/edae352d-9dd3-4100-9ff0-dd93c7eb65bf (perspectives/market-competitors.md)
- Assessment and progress: https://claude.ai/code/artifact/62a5d6d5-b169-4cac-8aca-3861a0133305 (perspectives/assessment-progress.md)
- Business model and launch: https://claude.ai/code/artifact/b8b95e36-45e6-4bf2-8984-198d4d22ffa3 (perspectives/business-launch.md)
