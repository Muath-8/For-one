# E05 · The live call

*Architecture domain 03. The call is a pipeline on LiveKit Agents: streaming speech-to-text, a Sonnet-class host with a cached brief, the episode's own voice. Law 7: the host only converses. Nobody says "wrong".*

### E05-S01 · Minimal call-worker on staging
**As the** coding agent, **I want** a `call-worker` on LiveKit Agents with Silero VAD, the multilingual turn detector, the two STT plugins in play, the Anthropic LLM plugin and the two TTS plugins, serving a hand-written call bundle, **so that** the 50 calls and the onboarding calls run on real vendors by week 2.
- **Given** a call request, **when** the worker joins the room, **then** the host speaks an opening line within 3 s of connect.
- **Given** drain mode, **when** a deploy happens, **then** live calls finish before the task stops.
- Size: L · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 03 Live call · Depends on: E01-S05, E02-S02
- Requirements: FR-1307, NFR-107

### E05-S02 · Host prompt with the governor
**As a** learner, **I want** a host who answers my mistake with the right form in a friendly echo and carries on, asks "sorry, you what?" only when meaning is lost, and never says I was wrong, **so that** teaching stays invisible.
- **Given** a learner turn with an error, **when** the host replies, **then** at most 1 recast is present, phrased as a question or continuation, and no string from the law corpus ("wrong", "the correct answer", "you should say") appears.
- **Given** the per-call budgets (3 clarification requests, 1 nudge, 2 to 4 recall gaps, 1 retell, 1 task remark), **when** the governor sees a reply over budget, **then** it re-requests with the `@moves` header and the violation is counted.
- **Given** the synthetic call transcripts with planted errors, **when** replayed through the governor, **then** zero violations before any live call.
- Size: L · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 03 Live call · Depends on: E05-S01, E02-S07
- Requirements: FR-330, FR-331, FR-332, FR-333, FR-338, FR-830, FR-837

### E05-S03 · Per-turn audio upload and verbatim re-transcription
**As a** teacher role, **I want** each learner turn uploaded under the learner's key and re-transcribed verbatim with disfluencies after the turn, **so that** the analyst sees what was actually said, not what the streaming recognizer smoothed.
- **Given** a turn ends, **when** `call.turn_audio_ready` fires, **then** `call/verbatim-turn` appends `call_turn_verbatim` with a confidence and `low_confidence_reason` from the package threshold.
- **Given** voice storage is off, **when** the call ends, **then** every turn's audio is deleted within 15 minutes and only the verbatim text remains.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 03 Live call, 05 Assessment · Depends on: E05-S01, E02-S05, E01-S08
- Requirements: FR-343, FR-801, FR-1041, NFR-304

### E05-S04 · Salma as the onboarding voice
**As a** learner, **I want** Salma to talk with me in my own language for about 3 minutes, at most 8 turns, with each fact she hears shown as a card, **so that** the show knows me before it starts.
- **Given** the intake, **when** Salma asks a question twice without an answer, **then** she skips it.
- **Given** two lines in the target language, **when** I answer, **then** the answers feed the level estimate and nothing is corrected.
- **Given** Salma's first lines, **when** spoken, **then** she says she is the AI producer of the show; across season 1 at least 80% of her words are in the learner's own language.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 03 Live call · Depends on: E05-S01, E05-S02
- Requirements: FR-112, FR-523, FR-560, FR-1308

### E05-S05 · The first call
**As a** learner, **I want** a 60 to 90 second first call with no recasts and no nudges, ending with one specific thing I managed, **so that** the first call is a win, not a test.
- **Given** kind `first`, **when** the call runs, **then** the governor budget is zero recasts, zero nudges, and the close names one task-level thing done.
- Size: S · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 03 Live call · Depends on: E05-S02
- Requirements: FR-116, FR-117

### E05-S06 · Hold-to-talk and adaptive patience
**As a** learner, **I want** to hold one button to keep the floor while I search for a word, and a host whose silence threshold adapts to how I pause, **so that** nobody interrupts me mid-sentence.
- **Given** the button is held, **when** I pause 5 s, **then** the host does not speak.
- **Given** the pause profile, **when** a call starts, **then** end-of-turn silence starts at 1.5 s and adapts within 1.0 to 2.5 s; backchannels play once per pause over 1.2 s.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 03 Live call, 06 Client · Depends on: E05-S01, E07-S07
- Requirements: FR-323, NFR-603

### E05-S07 · The word button
**As a** learner, **I want** to say a word in my own language and have the host give it back in the language I am learning and keep going, **so that** a missing word never ends the conversation.
- **Given** a word in the learner's language, **when** the button is used, **then** the target word is spoken within 2 s and the conversation continues; if the word was produced before, a hint comes first.
- **Given** "how do I say X?" asked aloud, **when** the host answers, **then** it gives a hint first and the full answer only on a second ask; the host never completes the learner's sentence.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 03 Live call · Depends on: E05-S02, E02-S02
- Requirements: FR-325, FR-326, FR-337, FR-831, NFR-108

### E05-S08 · Recall gaps, the retell and the call brief moves
**As a** learner, **I want** the host to leave 2 to 4 gaps for words from last week and ask once for a 60 to 90 second retell, **so that** I pull language out of memory and speak for 4+ minutes.
- **Given** a call brief with planned moves, **when** the call runs, **then** each move is attempted once and logged with whether the learner produced the target.
- **Given** the host's talk share, **when** measured per call, **then** it is at most 40%.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 03 Live call · Depends on: E05-S02, E04-S02
- Requirements: FR-322, FR-334, FR-335, FR-336

### E05-S09 · Anxiety mode, silence offers, timers and goodbyes
**As a** learner, **I want** the host to get gentler and simpler when I freeze, to offer a smaller question after 8 s of silence, and to close naturally around 6:30 and never after 8:00, **so that** a call ends like a conversation.
- **Given** median turn under 4 words in the first 2 minutes, or two 8 s silences, or the last call abandoned, **when** detected, **then** anxiety mode sets recall gaps to at most 1 and the host simplifies.
- **Given** 8:00, **when** reached, **then** the host says goodbye within one turn; no homework string appears.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 03 Live call · Depends on: E05-S02
- Requirements: FR-321, FR-340

### E05-S10 · Voice-note fallback and the restart after a drop
**As a** learner, **I want** a bad connection to turn the call into voice notes with the same host, and a dropped call to restart as a fresh call whose first line acknowledges the gap in the bible's words (ADR-24.B25), **so that** no session is lost.
- **Given** two reconnect failures, **when** the client falls back, **then** a voice note to the host gets a voiced reply within 30 s and the session counts fully.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 03 Live call, 06 Client · Depends on: E05-S01, E07-S07
- Requirements: FR-304, FR-342, NFR-202

### E05-S11 · Crisis step-out and AI disclosure in the call
**As a** learner, **I want** the host to say it is an AI whenever I ask, and to step out of character and give real resources if I say something that suggests I am in danger, **so that** the show is honest and safe.
- **Given** "are you a real person?", **when** asked in any language, **then** the host answers plainly that it is an AI.
- **Given** a keyword-list hit, **when** the host confirms within 2 s, or no confirmation arrives within 2 s (fail safe, ADR-24.B12), **then** the host steps out, the resources card for the learner's country is sent (the international directory where none exists), the call audio is quarantined, and a `crisis.activated` event exists, for every learner wherever they live (SB 243 duties for all, ADR-24.9).
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 03 Live call, 07 Security · Depends on: E13-S08
- Requirements: FR-560, FR-561, FR-570, FR-571, FR-572

### E05-S12 · Pronunciation on "say it once" and the recordings route
**As a** learner, **I want** to say one known sentence after the hosts and have it scored only internally, and to record the then-and-now and small-door notes through the same path, **so that** being understood is measured without a number on screen.
- **Given** a say-it-once clip, **when** scored, **then** the score is stored in the model and no client payload carries it.
- Size: M · Priority: P0 · Phase: Phase 5 · Release: v1 · Domain: 03 Live call · Depends on: E05-S03
- Requirements: FR-801, FR-812, FR-851

### E05-S13 · Round two and the dial-in experiment
**As a** learner, **I want** the same argument again, shorter and faster, and the option to join by phone on a commute, **so that** I speak more on the days I can.
- **Given** kind `round_two`, **when** offered from Today, **then** it lasts 2 to 3 minutes, once per episode, on every plan.
- **Given** a dial-in call, **when** it runs, **then** audio is flagged `low_confidence`, no talkback is offered and no claim is built from it.
- Size: L · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 03 Live call · Depends on: E05-S09, E07-S02
- Requirements: FR-345, FR-346
