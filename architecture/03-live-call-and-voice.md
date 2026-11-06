# Live call and voice stack

Domain 3 of 9 of the For one technical architecture. Written 2026-10-16 against PRD-v2 (Implementation PRD v3.0, 2026-10-10), concept-v2 sections 7 to 10, decisions.md, the voice-speech, AI-architecture and UI-UX lenses, and the Milestone 0 kit (04-production.md, 05-prompts.md); revised 2026-11-06 against the 2026-10-23 decisions (decisions.md), the conformance and skeptic reviews of 2026-10-21 (both unapplied until now) and the cross-domain rulings in 10-decision-records.md (ADR-01 to ADR-22). "PRD x.y" means PRD-v2 part x.y; where decisions.md or an ADR changed a part, the decision is cited instead. Tags: [DECISION] decided here; [ASSUMPTION] assumed because the spec is silent; [OPEN for Muath] only the owner can settle. Where this document names a service, table or event that the topology document (01-system-topology.md) or the pipeline document (02-generation-pipeline.md) already named, it uses their name; where it deviates, it says so in section 9.

**What changed in this revision, in one paragraph.** The latency budget is rebuilt honestly (sparse `@m` header, vendor round trips, preemptive generation, a learner-felt `silence_to_sound` gate); the turn controller becomes the single owner of end-of-turn on LiveKit's manual turn mode with the audio turn detector; the worker gets the per-call HKDF key and JWT the topology specifies, an `ephemeral/` prefix, a local deletion duty when `api` is down and `call_turn_verbatim` as an appended event; the crisis path gains a "continue" branch; the governor enforces the move minima and the anxiety trigger it missed, and the correction guard runs on every live line (ADR-06: no notes, no polish card, recasts inside the conversation only); languages come from the learner's `target_language` and `native_language` packages (ADR-02), so every Arabic-only or Saudi-only assumption is now one instance of a general rule; the build plan is re-dated to 2026-11-18 to 12-22 (ADR-07) and cut to what two engineers can ship; section 10 points at the shared register (ADR-22). Section 11 lists every finding and ADR applied.

This document covers everything that happens between the learner's tap on "Call" and the moment the call's evidence is safely in the event log: the LiveKit Agents pipeline, the host's move contract as a state machine, hold-to-talk and adaptive patience, the Huh? signal on the call, talkback to Salma (the producer, who speaks the learner's native language), Salma's voice at onboarding, the client's audio handling, recording and the deletion windows, verbatim re-transcription and pronunciation scoring, the two vendor tests, outage behaviour and cost. Salma never corrects and never sends notes (decisions.md §3, ADR-06); her other per-session role, explanations when the learner asks (`salma_explain`), is the chat's and is not designed here. It does not design the after-session analyst, the learner model, the generation pipeline that writes the call brief, the client app beyond the call screen, or billing.

---

## 1. Summary and the decisions in one table

The call is one Python process per concurrent call inside the `call-worker` service (LiveKit Agents), fed by a streaming recognizer, a Sonnet-class host whose brief sits in a cached prompt prefix, and the episode vendor's streaming voice, so the host sounds like the episode. Code, not the model, enforces the host's move contract (PRD 5.4.6), its maxima and its minima: the host declares its moves in a short header before it speaks, a governor in the worker checks that header against the remaining budgets and the moves still owed before any audio is synthesized, and the correction guard (07, ADR-06) blocks any line that reads as an explicit correction, because teaching is invisible and the only correction channel is a recast inside the conversation. Turn-taking is a learner-specific setting owned by one module: the `turn-controller` runs LiveKit in manual turn mode, end-of-turn silence starts at 1.5 s and comes from the pause profile within 1.0 to 2.5 s, the floor can be held with a pad, and the host backchannels from pre-rendered clips instead of waiting in silence. Talkback is a second recognizer stream in the learner's native language and the target language, fed only while the S button is held, answered by Salma on a separate audio track in under 2 s. Every learner turn is uploaded under a per-call key as it ends and transcribed verbatim while the call continues, which is what gives the after-session pass its evidence at call end and makes the 15-minute deletion window safe to honour. When live voice fails, the same call thread continues as voice notes through one Inngest function and nothing is lost. The honest latency figure is 1.3 to 1.6 s at p50 against the 1.5 s gate (4.15); the margin comes from the sparse header, preemptive generation and placing the worker next to the vendors, all measured in the week-2 50-call run.

| # | Decision | Reason | Alternative rejected |
|---|---|---|---|
| D1 | Pipeline (streaming STT, text host, streaming TTS) on LiveKit Agents, one `AgentSession` per call in manual turn mode (`turn_detection="manual"`); the `turn-controller` is the single owner of end-of-turn, fed by Silero VAD and LiveKit's audio turn detector [DECISION, PRD 14.3] | The only design where the recast, the transcript and the voice are all under the product's control; manual mode is the only way to express hold-to-talk, backchannels and the retell extension without two owners of end-of-turn; the audio turn detector (not the deprecated text model) is the one that lists Arabic and other native languages for onboarding | Speech-to-speech models (no custom voice, approximate transcripts, per-turn re-billing); Pipecat (Smart Turn is designed for English); LiveKit's built-in endpointing (`turn_handling.min_delay`/`max_delay`) as the decider |
| D2 | Host declares moves in a sparse one-line header (`@m`, 8 to 15 tokens, only the moves used; absent means not used) before its reply text; a code governor enforces the PRD 5.4.6 maxima and minima, then `guard.check_output` (07) checks the text, and the worker can abort and re-request once [DECISION] | Law 7 and the move caps are hard constraints; a prompt alone cannot be trusted to count; a full JSON header (the first draft, 55 to 70 tokens) cost 0.6 to 1.0 s of first audio | Structured-output JSON for the whole reply (delays first audio until the JSON closes); the full JSON header; post-hoc filtering of text (cannot remove a nudge once spoken) |
| D3 | End-of-turn silence `p` from the pause profile (owned by 04 §4.3.4), 1.5 s for a new learner, clamp 1.0 to 2.5 s; when the audio turn detector says the sentence is unfinished, wait up to `p + max_extend` (1.5 s for `p < 1.5`, capped at 1.0 s for `p >= 1.5`, set from the M0 "incomplete" rate in week 1) with one backchannel at 1.2 s; the extension is a deliberate departure from PRD 5.4.4's 1.0 to 2.5 s ceiling [DECISION, PRD 5.4.4, voice lens] | Learners pause mid-clause about three times as often as natives (voice lens); the vendor defaults of 0.5 to 0.8 s cut them off; cutting at 2.5 s regardless breaks law 7 more often than a 1.0 s extension slows a reply | A fixed long silence (makes every reply slow); vendor semantic VAD only (not tunable per learner); a hard 2.5 s cap with hold-to-talk as the only escape |
| D4 | Backchannels are pre-rendered clips per host voice, chosen by code, never synthesized live [DECISION] | Zero latency and zero cost at the moment latency matters most; the words never take the floor because the list is fixed | Asking the model for a backchannel (adds a model round trip inside the learner's pause) |
| D5 | Talkback audio goes to a second recognizer stream (`talkback_stt`, languages `[native_language, target_language]`, code-switch on) opened at job start and fed only between S-down and S-up; the host stream is muted for those frames and its turn detector frozen; talkback audio is streamed only, never recorded; Salma answers on a second published audio track [DECISION, PRD 5.4.5, 0.1 row 7, ADR-02] | Keeps the native language out of the host's transcript and the verbatim pass, keeps the floor held, lets the client draw the bubble from S, and does not put 200 to 500 ms of websocket setup inside a 1 to 2 s hold (cost of the always-open stream about $0.013 a call) | One stream for both (code-switch errors leak into the host's input); opening the stream on S-down (first draft); client-side recording and upload (adds 1 to 2 s) |
| D6 | Word-or-hint is decided by code from the Salma talkback brief (produced-word set), not by the model; the ask itself is resolved by Haiku 5.5 for every ask in the beta (no reverse gloss index) [DECISION, PRD 5.4.5 rule 4] | A rule with a lookup is exact; a model would sometimes give the word to a learner who has it; the reverse index saved 400 ms on a minority of asks and was unowned work in 02 | Model decides from the brief in the prompt; the ar→en reverse gloss index (first draft; cut for the beta) |
| D7 | Host LLM: `claude-sonnet-5-5`, `output_config.effort: low`, `thinking: {type: "between_tools"}` (no tools, so no thinking before the reply), `max_tokens: 200`, brief in the cached prefix, one per-turn operator note as a mid-conversation system message; a per-model request builder in the adapter (Haiku 5.5 without `thinking`, Gemini with the note folded into the user turn); a thin `llm.LLM` subclass over the Anthropic SDK if the stock plugin cannot place the cache breakpoints (verified by the week-1 cache probe) [DECISION, PRD 14.3] | First token in 300 to 600 ms with the cache warm; mid-conversation system messages keep the cached history intact; the same body sent to Haiku 5.5 returns 400 (`between_tools` is Sonnet-only), so the fallback needs its own shape; Haiku 5.5 is the measured fallback if the 50-call test says quality holds | Opus-class host (latency and cost); Haiku-class by default (quality in the recast moves unproven); one request body for every model |
| D8 | Call TTS is the episode vendor's streaming voice with the same `voice_id`; the pipeline's blind test only admits vendors whose streaming endpoint has a first-byte latency under 300 ms at p95 [DECISION, PRD 14.3, 7.1] | "The host sounds the same" is a PRD rule; a vendor that cannot stream fast enough cannot be the episode vendor either | Different vendor on the call with an "understudy" voice (Milestone 0 did this; the day-7 check-in asks whether it mattered, and the PRD chose sameness) |
| D9 | Each learner turn is uploaded as it ends (`call.turn_audio_ready`) under the per-call key and transcribed verbatim during the call; the result is a second event `call_turn_verbatim` appended by `workflows` (04 D2, ADR-19); the full mixed recording is uploaded only when voice storage is on [DECISION, PRD 5.4.11, 10.2] | The after-session pass (05, one function since ADR-06) needs the verbatim text at call end, not 3 minutes later; the 15-minute deletion window is met with margin; appending keeps `events` append-only | Transcribe the whole call after it ends (one big deletion race); updating the `call_turn` event in place (first draft) |
| D10 | Voice-note fallback runs as the Inngest function `call/voice-note-reply` using the same brief, host prompt and voice; the client switches when the room is not joined within 3 s, on two pipeline errors, or on an ICE failure longer than 5 s [DECISION, PRD 5.4.10] | One brief, one host, one thread; the learner's argument continues | A separate "voice note host" prompt (two hosts to keep in character) |
| D11 | The first host line of every call is synthesized at episode time by the pipeline and stored with the brief; the worker plays it while the vendor websockets open [DECISION, PRD 15 "call connect under 3 s"] | The learner hears the host within the connect budget even on a cold worker | Synthesize on connect (adds 0.5 to 1 s to the first sound) |
| D12 | Client audio: `getUserMedia` with echo cancellation, noise suppression and AGC on; Screen Wake Lock re-acquired on every `visibilitychange`; a backgrounded page is treated as an abandoned call after 10 s [DECISION, PRD 1.4] | iOS Safari suspends WebRTC in the background with no fix (voice lens); pretending otherwise loses evidence | Keep-alive tricks (unreliable, and they drain the battery) |
| D13 | Two tools, as 01, 08 and ADR-03 and ADR-19 rule: the 30-clip recognizer test and the talkback-ask fixture run as `vendor-lab recognizers` (the language gate's check 2, scripts on the vendor SDKs, during Milestone 0); the 50-call test runs as `tools/call-bench calls`, which drives the staging worker by pushing Milestone 0 learner audio into the `AgentSession` input in-process, with `connect_ms` over the real WebRTC path measured by hand on phones [DECISION, PRD 10.14, 14.4] | Routing 30 audio files through a WebRTC worker to test four batch and streaming APIs is a week of plumbing for a one-day script; in-process injection measures latency and the governor without a headless WebRTC caller; `call-bench` keeps one report directory 09 already references | One tool for both (first draft); a headless LiveKit client as the scripted caller; separate scripts per vendor (never rerun) |
| D14 | The observer (PRD 14.1, [LATER]) has a reserved slot: one mid-conversation system message per turn, keyed `whisper`; nothing in the beta depends on it [DECISION] | Costs nothing now; prevents a redesign later | Building it in the beta (PRD 17 excludes it) |
| D15 | Crisis protocol in the call: the host declares `crisis` in its header or the package keyword lists (target and native language) fire on a learner turn or a talkback ask; the worker plays the pre-rendered clips (target language from `packages/languages/<target>/`, then the native language from `packages/native/<lang>/`), sends the resources card for `learners.residence_country` (ADR-20), logs `crisis_activation`, and waits: `crisis.continue` from the client resumes the argument with the host told to go on without referring to the crisis turn (a second activation ends the call), `crisis.stop` or 60 s without an answer ends it [DECISION, PRD 7.9.2] | Two independent triggers; fixed, counsel-reviewed lines rather than generated ones; PRD 7.9.2 says the session continues only if the learner chooses, so continuation must exist as a path | Model-only detection; generated crisis text; always ending the call on crisis (first draft) |
| D16 | The worker holds a per-call key `HKDF(DEK, "call:" + call_id)` and a per-call JWT (5-minute TTL, audience `call-worker`), both delivered in the brief response; every `media_objects` row the recorder creates carries `key_derivation = 'call:{call_id}'`; storage-off audio is written under an `ephemeral/` prefix [DECISION, 01 D7, 07 D2, ADR-12] | The most exposed service never holds the key that protects every recording the learner ever made; `api` re-derives the call key for Range reads; the lifecycle backstop applies to a prefix that is actually written | The raw learner DEK in the bundle (the first draft of this document, rejected in 01); a static internal service token |
| D17 | The correction guard runs on the live host turn: `guard.check_output("host", text)` (07, ADR-06) sits between the governor's `check()` and the TTS flush, under 20 ms; a hit means re-request once, then the package filler line; hits are counted in `moves.violations` and in 09's `explicit_corrections_per_100_turns` (ceiling 0) [DECISION, decisions.md §3, ADR-06] | Invisible teaching is a law; a law is enforced by code the way law 12 is; the host never says "wrong" or "the correct form is" | Prompt-only enforcement; Salma's correction notes as the correction channel (removed by decisions.md §3) |
| D18 | Preemptive generation: the host request starts on the interim transcript when silence reaches about 600 ms and the audio turn detector's end-of-utterance probability is at least 0.8, and is cancelled if speech resumes before the endpoint; nothing is spoken before the endpoint [DECISION, verify the SDK option in week 1] | Removes 300 to 600 ms of model latency from the learner-felt silence at the cost of a wasted request on about 10 to 20% of turns (input is cached, so about $0.002 a call) | Waiting for the endpoint before any request (the first draft's budget, which did not meet the gate) |

---

## 2. Requirements this domain implements

| PRD part | Requirement | Where in this document |
|---|---|---|
| 2.2 A2, A3 | Salma's voice in the learner's native language within 60 s of first open; at most 8 turns, two target-language lines, fact cards as she hears them; talk (this worker) or type (`api`, 01) | 4.9 |
| 2.2 A7 | First call 60 to 90 s; no recasts or nudges; Salma's one-line introduction of talkback before it rings | 4.3 (budgets by call kind), 4.9 |
| 4 rule 4 | A call cannot resume; an interrupted call restarts fresh with a line that acknowledges the gap | 4.2 (`resumed_after_drop`) |
| 4 rule 3 | Planning card before Call when Read was skipped | 4.11 (client), the words come from the brief |
| 5.4.1 | One tap from the throw, Today or the feed link; screen awake; earphones suggested once | 4.11 |
| 5.4.2 | Target 5 to 7 min; natural close from 6:30; end by 8:00; learner may end any time with an in-character close | 4.3 timers |
| 5.4.3 | Host share of talk at most 40%; short turns | 4.4 prompt, 4.3 governor, 6 metrics |
| 5.4.4 | Open mic; hold to keep the floor; adaptive patience 1.0 to 2.5 s from the pause profile (the `p + max_extend` wait when the sentence is judged unfinished is a tagged departure, D3); one backchannel per pause over 1.2 s; 8 s silence handling; "sorry?" and "slower" in either language; previous-track replays the host's last line | 4.5, 4.6 |
| 5.4.5 | Talkback to a recognizer that covers the learner's native language; the host waits; Salma's closer voice; word or hint; logged per word | 4.7 |
| 5.4.6 | The move contract with its caps and its minima (recall gaps 2 to 4, retell once, pushback at least once); recast only on targets or meaning-blurring errors; nudge followed by a self-repair pause | 4.3, 4.4 |
| decisions.md §3, concept-v2 law 7 (ADR-06) | Teaching is invisible: no notes, no polish card, no correction UI; the host corrects only by recast inside the conversation; the correction guard blocks explicit corrections in code; `explicit_corrections_per_100_turns` ceiling 0 | 4.3 (D17), 4.4, 4.13 |
| 5.4.7 | Anxiety mode and its three triggers | 4.3 |
| 5.4.8 | Host captions by default, recast word bold, learner never captioned live (room transcription output disabled in the worker), no correction UI | 4.8, 4.11 |
| 5.4.9 [P1] | Round two: 2 to 3 min, same host and argument, a like-for-like retell sample | 4.3 (kind `round_two`), 7 |
| 5.4.10 | Live voice failure falls back to voice notes in the same thread | 5.1 |
| 5.4.11, 12.5, 15 | Streaming transcript drives the call; verbatim re-transcription after; audio kept only with consent; deletion within 15 min when storage is off, within 24 h on revoke; transcripts always kept | 4.10 |
| 5.4.12 [P1] | Dial-in: 8 kHz, planning only, low confidence, no claims | 7 |
| 10.2 (as amended by decisions.md §3) | The after-session pass, one function with the 10-minute budget, reads the verbatim turns that are ready at call end; there is no 90-second notes stage | 4.10 (per-turn verbatim) |
| 8.4 rule 7, 16.1 | A wrong callback is acknowledged plainly, never argued, and logged as `wrong_memory_flag` | 4.3, 4.4, 4.12 |
| 12.1 | The learner's turn is signalled by the host's breath and a soft rising tone, never a beep | 4.5 |
| 7.3 (as amended by ADR-02) | Salma's voice closer and drier than the hosts'; she speaks the learner's native language from `packages/native/<lang>/`; the variety per native language is OPEN | 4.7, 4.9 |
| 7.8, 7.9 | AI disclosure on request by every character; crisis protocol in live roles | 4.4, 4.3 |
| 8.1, 14.2 | Live roles never write; the worker produces events only | 3.3 |
| 8.2 | Events `call_turn`, `talkback`, `hold_floor`, `silence` with streaming and verbatim text, word timings, confidences | 4.12 |
| 8.6 | The host's one-page brief; Salma's talkback brief (produced-word history) | 4.2 |
| 10.2 step 1, 10.3 | Verbatim re-transcription of every learner audio turn (call, round two, shadow, say it once, small-door note); pronunciation on known sentences only, internal | 4.10 |
| 10.14 [P0], ADR-03, ADR-07 | The 30-clip recognizer test as the language gate's check 2, by 2026-11-10 during Milestone 0; confidence threshold from it | 4.13 |
| 14.3 | LiveKit Agents; Soniox or Deepgram for the host stream; Soniox or AssemblyAI Universal realtime for talkback (a secondary that covers the native language); AssemblyAI or ElevenLabs Scribe; Speechace or Microsoft; adapters; two voice vendors wired | 3, 4.14 |
| 14.4 #3 [P0] | 50 scripted calls, median host reply under 1.5 s; run #1 in build week 2 on the minimal worker (by 2026-12-01), reruns in weeks 4 and 5 | 4.13 |
| 14.5 | Call plus round two at about $0.16 (met at $0.16 to $0.17 only with Inworld or Gemini and the shorter-host-turn lever); re-transcription plus pronunciation $0.03 | 6 |
| 15 | Call connect under 3 s; host reply median under 1.5 s and p95 under 2.5 s (clock: end-of-turn decision, with a second gate on the learner-felt `silence_to_sound_ms`); talkback under 2 s; first sound at onboarding under 60 s; voice-vendor outage covered by the second vendor the same day | 4.15, 5 |
| 16.2 | Talkback use per call; recognizer error by native language; calls abandoned on the move (from `end_reason` and `started_by`, never from motion sensors); feed-to-call handoff | 4.12, 6 |
| 1.2 laws 1, 5, 7, 8, 12 | No game furniture on the call screen; honesty; conversational corrections only; conversations end like conversations; no claims from the live path | throughout; 3.3 |

---

## 3. Architecture

### 3.1 Components

Draw as four columns, left to right: the phone, LiveKit Cloud, the `call-worker` process, and the vendors; with `api`, Postgres, S3 and Inngest as a row underneath.

| Component | Runs in | What it does |
|---|---|---|
| Call screen (`web`, client domain; the audio parts are specified in 4.11) | the phone's browser | Mints a call through `api`, joins the room, publishes the mic, plays two agent tracks (`host`, `salma`), sends control messages, renders captions and the bubbles, records voice notes in the fallback |
| LiveKit Cloud | managed | WebRTC media between phone and worker, data channel, agent dispatch, room lifecycle, SIP ingress for the dial-in experiment [P1] |
| `call-worker` | ECS Fargate, Python 3.12, LiveKit Agents (SDK version pinned in week 1; every option name in this document is verified against that version and the result written to `apps/call-worker/SDK-NOTES.md`), region `CALL_WORKER_REGION` (01 §3.6: next to the STT, LLM and TTS endpoints) | One job per call, authenticated to `api` by the per-call JWT from the dispatch metadata. Inside the job: `CallSession` (our wrapper around `AgentSession` in manual turn mode), the turn-taking controller, the move governor, the talkback controller, the recorder, the event emitter |
| `turn-controller` (module) | in the job | The single owner of end-of-turn: Silero VAD frames, the audio turn detector's end-of-utterance probability, the pause profile, hold-floor state, backchannel and filler scheduler, silence timers, preemptive generation (D18); it calls `session.commit_user_turn()`, `session.clear_user_turn()` and `session.interrupt()` |
| `host-governor` (module) | in the job | Budgets per call kind (maxima and minima), phase clock (`tick`), parses the `@m` header, calls the correction guard, aborts and re-requests, anxiety mode, host-share lever, wrong-memory handling, crisis switch |
| `talkback-controller` (module) | in the job | Gates frames into the native-language stream while S is held, runs the crisis keyword list on that stream, resolves word-or-hint, synthesizes Salma on the `salma` track, logs `talkback` |
| `recorder` (module) | in the job | Buffers each learner turn's PCM minus the talkback frames, encodes, uploads with SSE-C under the per-call key to the `ephemeral/` or stored prefix, emits `call.turn_audio_ready`; mixes the full recording when voice storage is on; deletes the call's ephemeral objects itself at call end + 14 min when any `turn_audio_ready` post failed |
| `event-emitter` (module) | in the job | `POST /internal/events` in batches of 20 or every 2 s with the per-call JWT; appends each turn's `vendor_calls` rows to the S3 spool before any buffered flush (ADR-13); spools events and the end record to `forone-voice/spool/{callId}.ndjson` (SSE-KMS under the environment key) if `api` is unreachable, read by `spool/ingest` every minute |
| Streaming recognizer adapter | LiveKit STT plugin | Role `streaming_stt` keyed by `target_language` (English: Soniox primary, Deepgram secondary) with languages `[target, native]` and code-switch on so repair and crisis phrases in the native language are matched on the open mic; a second instance for talkback (`talkback_stt`: Soniox primary, AssemblyAI Universal realtime secondary, both covering the native language) |
| Host LLM adapter | LiveKit LLM plugin, or a thin `llm.LLM` subclass over the Anthropic SDK if the week-1 cache probe shows the stock plugin cannot place the breakpoints and the system entries | Anthropic `claude-sonnet-5-5`; fallback `claude-haiku-5-5`, then the second vendor; one request builder per model (4.4) |
| Call TTS adapter | LiveKit TTS plugin | The episode vendor's streaming endpoint with the casting's `voice_id`; the understudy vendor during failover |
| Salma TTS adapter | LiveKit TTS plugin | The native-language voice from `packages/native/<lang>/` (the 7.3 test per native language), role `salma_tts` |
| `api` | ECS | `POST /v1/calls` (idempotent on a client key), `GET /internal/calls/{id}/brief`, `POST /internal/events`, `POST /internal/calls/{id}/turns` (01's name; this document's end record travels on it with `kind: end`), `POST /v1/calls/{id}/voicenotes`, `POST /v1/onboarding/{id}/messages` (the typed onboarding exchange, 01 §3.6) |
| Inngest functions | `workflows` | `call/verbatim-turn`, `call/voice-note-reply`, `call/pronunciation-score`, `spool/ingest` (every minute), `audio/expire` (topology), and the hooks into `session/after-pass` (assessment; one function since ADR-06) |
| `tools/call-bench` | developer laptop or CI | The 50-call latency and move-contract test by in-process audio injection into the staging worker, the simulated caller of the P1 offline suite; reports under `bench/reports/` |
| `vendor-lab` (`forone.langgate`, ADR-03) | developer laptop | The 30-clip recognizer test, the talkback-ask fixture and the vendor-chain latency check per region, as scripts on the vendor SDKs during Milestone 0 |

### 3.2 Data flow for one main call (draw as a sequence diagram with the five lanes above)

1. The learner taps Call. `web` calls `POST /v1/calls {sessionId, kind: "main", clientKey}` (idempotent on `clientKey` for 60 s, so a double tap returns the same call rather than two rooms). `api` checks the door rules (PRD 4; an abandoned, dropped, drained or failed main call with under 120 s of learner speech does not count as "done", so the fresh call is allowed), writes the `calls` row, derives the per-call key `HKDF(DEK, "call:" + call_id)`, mints the per-call JWT (5-minute TTL, audience `call-worker`, subject `callId`), creates room `call-{callId}` with agent dispatch metadata `{callId, jwt}`, and returns `{callId, roomUrl, token, openingClipUrl}`. The participant token has a 10-minute TTL; the client refreshes it through `GET /v1/calls/{id}/token` at minute 8 if the call is still live, so a reconnect at minute 9 is possible.
2. `web` joins the room and publishes the mic. In parallel, the worker accepts the job, calls `GET /internal/calls/{callId}/brief` with the JWT, receives the `CallBundle` (4.2), opens the host STT websocket, the talkback STT websocket and the TTS websocket, disables the session's room transcription output, and publishes the `host` and `salma` tracks. The moment the learner's mic track is subscribed, the worker plays the pre-rendered opening line from the bundle on the `host` track (D11) and sends `state {phase: "opening"}`.
3. The learner speaks. VAD frames and STT partials flow; the turn controller decides end-of-turn (4.5) and calls `session.commit_user_turn()`. When silence has reached about 600 ms with a high end-of-utterance probability, the host request has already started on the interim transcript (D18) and is cancelled if speech resumes. On end-of-turn the worker has the final streaming text with word timings; it strips any native-language spans from the text sent to the host (their timings are logged on the turn), emits `call_turn` (speaker `learner`, streaming text), hands the turn's PCM to the recorder, and asks the governor for this turn's allowances and the moves it owes.
4. The governor appends one mid-conversation system note (allowances, owed moves, clock, mode) and the learner's text to the conversation and calls the host LLM with streaming. The first line of the reply is the `@m` header; the governor parses it, checks it, runs `guard.check_output("host", text)` on the text as sentences arrive, and either lets the rest stream into TTS or aborts and re-requests once (4.3).
5. The TTS stream plays on the `host` track with the recast word wrapped in the vendor's emphasis markup; caption segments go to the client over the data channel with the recast span marked. When the host finishes, the worker emits `call_turn` (speaker `host`, text, moves, the per-stage latencies) and the turn controller returns to listening after the turn-signal clip (a breath and a soft rising tone, PRD 12.1).
6. Meanwhile the recorder has encoded the learner's turn (minus any talkback frames), uploaded it to `forone-voice/ephemeral/learners/{lid}/calls/{callId}/turn-{n}.ogg` (storage off) or `forone-voice/learners/{lid}/calls/{callId}/turn-{n}.ogg` (storage on) with SSE-C under the per-call key, written the `media_objects` row with `key_derivation = 'call:{call_id}'`, and emitted `call.turn_audio_ready`. Inngest runs `call/verbatim-turn`: verbatim transcription with disfluencies and confidences, appended as a `call_turn_verbatim` event joined on `(call_id, turn_index)` (04 D2); if voice storage is off, the turn object is deleted when the append succeeds.
7. If the learner holds S: the talkback controller freezes the turn detector, routes the frames to the native-language stream (open since job start) instead of the host stream and the recorder, runs the crisis keyword list on that transcript, and on release resolves the ask and speaks Salma's answer on the `salma` track within 2 s; `talkback` is logged with the word, the mode (word or hint) and the latency.
8. At 6:30 the governor tells the host to begin the close; at 7:40 to say goodbye in one line; at 8:00 the worker waits for the current learner turn to end (bounded by `p + max_extend`), then plays the goodbye line. Or the learner taps ✕: the worker lets the host say one in-character line, then ends. The worker posts the end record (`end_reason`, `voice_storage`, `vendors`, `metrics`) to `POST /internal/calls/{id}/turns` with `kind: end`, emits `call.ended {end_reason, voice_storage, turns, learner_speech_ms, host_speech_ms}`, closes the vendor streams and leaves the room. If voice storage is on, it uploads the full mixed recording as `call_full`. If any `turn_audio_ready` post failed during the call and storage is off, the recorder deletes the call's ephemeral objects itself at call end + 14 min before the job exits (5).
9. `session/after-pass` (assessment domain; one function with the 10-minute budget since ADR-06) starts on `call.ended` and waits for the last turn's `call_turn_verbatim` before it reads the call. `audio/expire` (topology) sleeps 14 minutes and deletes whatever ephemeral audio remains when storage is off.

### 3.3 Boundaries and the writing rule

The worker never reads the learner model and never writes a store. It receives one `CallBundle` at dispatch, keeps everything in memory for the call, and emits events. The only durable writes it causes are `events` rows (through `api`, with the per-call JWT), `media_objects` rows (through the upload path), `vendor_calls` rows (appended per turn to the S3 spool and reconciled hourly, ADR-13) and the `calls` row's `ended_at`, `end_reason`, `vendors` and `metrics` columns (through the end record on `POST /internal/calls/{id}/turns`). This is PRD 8.1 rule 3 and 14.2 made structural: there is no code path from the worker to the nine stores, so a host cannot "remember" what it misheard. The worker holds no database connection and no static secret; the JWT and the per-call key die with the job.

### 3.4 Interfaces to other domains

| Direction | Interface | Owner |
|---|---|---|
| in | `episode_artifacts(kind=call_brief)` with the `CallBrief` type, `voice_casting` for the learner, the opening-line clip ref | pipeline domain |
| in | Compiled `HostBrief` and `SalmaTalkbackBrief` (4.2) built by the host brief compiler, which this domain owns as a module in `forone.core.briefs` but which runs inside `episode/make` at publish time and again at `POST /v1/calls` when the learner model version has changed since | this domain (module), pipeline domain (call site) |
| in | `vendors.yaml` roles keyed by `target_language` and `vendor_config` rows; the per-call key `HKDF(DEK, "call:" + call_id)` and the per-call JWT, both minted by `api` at dispatch (never the learner DEK) | topology, security domains |
| in | The learner's `native_language`, `target_language`, `residence_country` and `tz`; the two packages `packages/languages/<target>/` (host prompts, recognizer thresholds, repair and crisis phrases, law and correction words) and `packages/native/<lang>/` (Salma's voice and lines, crisis clips, resources per country, the talkback language hint) | topology (learner row), ADR-02 packages |
| in | Pause profile (`skills.pause_profile`, formula owned by 04 §4.3.4), anxiety prior, last-call-abandoned flag, produced-word set | learner model domain (Skills and Word bank stores) |
| out | Events `call_turn`, `talkback`, `hold_floor`, `silence`, `replay_line` (door `call`), `crisis_activation`, `wrong_memory_flag`, `call_started`, `call_ended`; Inngest events `call.turn_audio_ready`, `call.ended`, `voicenote.received`, `pronunciation.requested`; `call_turn_verbatim` is appended by `workflows` (`call/verbatim-turn`), not by the worker | data domain (event log), topology (Inngest shells) |
| out | `media_objects` of kinds `call_turn`, `call_full`, `voice_note`, `say_it_once`, `shadow`, `recording`, each with `key_derivation` and `encryption = 'sse_c_learner'` (ADR-12) | security and data domains |
| out | Per-call metrics in `calls.metrics`; `vendor_calls` rows per adapter call, spooled per turn and reconciled hourly (ADR-13); `cache_read_tokens` per host turn so a silent cache miss is visible | cost and evaluation domains |

---

## 4. Detailed design

### 4.1 Call kinds and the `calls` row

The `calls` table is the topology's (01-system-topology.md 4.2). This domain adds two columns and fixes the enums:

```sql
alter table calls add column metrics jsonb not null default '{}';   -- CallMetrics (4.12)
alter table calls add column bundle_version int not null default 1; -- which HostBrief compile was used
-- kind: onboarding | first | main | round_two | small_door | then_and_now
-- mode: live | voice_notes
-- end_reason: natural_close | learner_ended | timeout_8m | pipeline_error | fallback | crisis | abandoned | driving | drained | policy
```

The door rule for "the main call happens once" (PRD 4 rule 6) lives in `api` and reads this table: a main call counts as done only when `end_reason in (natural_close, learner_ended, timeout_8m, crisis)` or `metrics.learner_speech_ms >= 120000`; otherwise `POST /v1/calls` allows a fresh call with `resumed_after_drop: true` (4.3). [DECISION] The 120 s threshold is the point at which the after-session pass has enough speech to assess.

| kind | PRD | Persona | Length | Budgets (4.3) | Enters the after-session pass as |
|---|---|---|---|---|---|
| `onboarding` | 2.2 A3 | Salma, in `native_language` | about 3 min, at most 8 Salma turns | n/a (Salma has her own contract, 4.9) | intake facts, two target-language moments |
| `first` | 2.2 A7 | throwing host | 60 to 90 s | no recast, no nudge, clarify only if meaning is lost, no recall gaps, no retell, praise 1 at the end | first speaking estimate |
| `main` | 5.4 | throwing host | close from 6:30, end 8:00 | full contract | the main call |
| `round_two` [P1] | 5.4.9 | same host | close from 2:00, end 3:00 | retell first, 1 recall gap, recasts kept, no nudge | fluency sample |
| `small_door` | 3.7 | none live | one voice note up to 60 s | n/a | voice note |
| `then_and_now` | 10.9.2 | Salma narrates from pre-rendered clips | about 3 min | no live model; the client records three tasks | recording |

`small_door` and `then_and_now` are not live calls: they are recordings captured by the client and uploaded through the same `/voicenotes` and `/recordings` routes, listed here because the recorder, the verbatim path and the deletion rules are shared. The `onboarding` kind covers the talk path only; a typed onboarding (A2 "Type", or mic denied) runs through `api` as `POST /v1/onboarding/{id}/messages` with `calls.mode = typed` and never touches this worker (01 §3.6).

### 4.2 The call bundle and the host brief

`GET /internal/calls/{callId}/brief` returns one object. It is compiled by `forone.core.briefs.compile_call_bundle(call_id)`; the compile is cheap (one Postgres read per store) and runs at `POST /v1/calls`, so a veto in the notebook an hour before the call is honoured.

```ts
type CallBundle = {
  call: { id: string; kind: CallKind; learner_id: string; session_id: string|null; episode_id: string|null;
          resumed_after_drop: boolean; started_by: "throw"|"today"|"feed"|"onboarding" };
  host_brief: HostBrief | null;                  // null for onboarding, small_door, then_and_now
  salma_brief: SalmaTalkbackBrief | null;        // null when talkback is unavailable (onboarding)
  salma_onboarding: SalmaOnboardingBrief | null; // only kind = onboarding (4.9)
  turn_taking: { endpoint_ms: number; max_extend_ms: number; backchannel_after_ms: number;
                 silence_offer_ms: number; interruption_min_ms: number; interruption_min_words: number };
  anxiety: { prior: boolean; last_call_abandoned: boolean };   // either one enters anxiety mode (PRD 5.4.7)
  voice: { host: "karim"|"mona"|null; vendor: string; voice_id: string; rate: number; understudy: { vendor: string; voice_id: string };
           salma: { vendor: string; voice_id: string; variety: string /* per native package, e.g. "gulf"|"msa" for ar */ };
           backchannel_clips: { id: string; url: string; duration_ms: number }[];   // pre-rendered per host voice (4.5)
           filler_clips: { id: string; url: string; duration_ms: number }[];        // "hmm", a breath: played in THINKING, never a word
           turn_signal_clip: { url: string; duration_ms: number };                 // breath plus soft rising tone (PRD 12.1)
           opening_clip: { url: string; text: string; duration_ms: number } | null;
           package_clips: { crisis_target: string; crisis_native: string; talkback_intro_native: string; salma_wait_native: string } };
  vendors: { streaming_stt: string; talkback_stt: string; host_llm: { vendor: string; model: string; fallback: { vendor: string; model: string }[] };
             call_tts: string; salma_tts: string };
  consent: { voice_storage: boolean };
  crypto: { call_key: string /* base64, 32 bytes = HKDF(DEK, "call:" + call_id), memory only */; key_derivation: string /* "call:{call_id}" */; key_version: number };
  languages: { native: string; target: string;                          // learners.native_language, learners.target_language (ADR-02)
               repair_phrases: { target: string[]; native: string[] }; crisis_keywords: { target: string[]; native: string[] };
               driving_phrases: { target: string[]; native: string[] }; name: { display: string; respelling: string } };
  resources_country: string;                                           // learners.residence_country for the crisis card (ADR-20)
  limits: { close_begin_s: number; hard_end_s: number };
  bundle_version: number; learner_model_version: number; prompt_version: string;
};
// The per-call JWT is not in the bundle: it arrives in the dispatch metadata {callId, jwt} and is what authorizes this fetch.

type HostBrief = {                                 // PRD 8.6: one page; target under 900 tokens
  host: "karim"|"mona"; learner_name: { display: string; respelling: string; pronouns: "he"|"she"|null };
  episode_in_3_lines: string[]; question: string; planted_phrases: string[];
  position: string; pushback: string[];
  targets: { grammar: { id: string; label: string; necessity_moves: string[]; recast_list: { expected_error: string; recast_form: string }[] };
             words: { lemma: string; move: string }[] };                // recast_list is the teacher's "echo plan" (ADR-06): the only correction channel
  recall_gaps: { id: string; line: string; expected: string }[];     // 2 to 4
  retell_prompt: string;
  callback: { text: string; fact_id: string } | null;               // exactly one, confirmed
  never_mention: string[];
  budgets: Budgets;                                                 // from the kind table, adjusted by anxiety.prior
  style: { accent: string /* per target package, e.g. "british"|"american" */; max_words_per_turn: number /* 25 */; language: string /* target_language */ };
  day_type: "first"|"main"|"round_two"|"return"|"rehearsal";
  rehearsal: { role: string; scene: string } | null;                // PRD 7.6 rule 5: the host plays the other person
};

type SalmaTalkbackBrief = {
  produced_lemmas: Record<string, { count: number; last_session_label: string /* "Tuesday, about your manager" */ }>;
  active_targets: { id: string; label: string }[];
  english_share: number;                                            // PRD 7.3: 0.2 in season 1
};

type Budgets = { clarify: number; recast_per_turn: number; nudge: number; recall_gaps_min: number; recall_gaps_max: number;
                 retell: number; praise: number; silence_offers: number };
```

The `HostBrief` is assembled from `CallBrief` (pipeline) plus four learner-model reads: name and respelling from `voice_casting.name`, the pause profile and anxiety flags from Skills, the `never_mention` list from Life ("don't bring up") and `working_on` vetoes, and `callbacks_allowed` filtered again at compile time against the fact's current status (a fact deleted in the notebook after the brief was written is dropped here; PRD 8.4 rule 7). The prompt text, the phrase lists and the recognizer thresholds come from `packages/languages/<target_language>/`; Salma's persona, voice, clips and the resources card from `packages/native/<native_language>/` (ADR-02). Nothing in the bundle is specific to one pair.

### 4.3 The host move contract as a state machine

Two machines run together: the call phase machine (time and content) and the turn machine (who has the floor). The governor owns the phase machine and the budgets; the turn controller owns the turn machine.

**Phase machine (per call, kind `main`; `first` and `round_two` use the same states with the timers from 4.1):**

```
CONNECTING ─(mic subscribed)─► OPENING ─(host opening line done)─► ARGUE
ARGUE ─(host declares retell, window 2:00..close_begin_s)─► RETELL          no recall-gap precondition; owed at the window's end
RETELL ─(learner turn ends; the 75 s ring disappearing never ends the turn)─► ARGUE_AFTER
ARGUE | ARGUE_AFTER ─(tick: t >= close_begin_s)─► CLOSING                  time-driven, in Governor.tick()
CLOSING ─(host declares close, or tick: t >= hard_end_s - 20 s)─► GOODBYE
GOODBYE ─(host line done)─► ENDED
any ─(learner ✕)─► GOODBYE(reason=learner_ended)        one in-character line, then end
any ─(crisis)─► CRISIS ─(client crisis.continue)─► ARGUE_AFTER             host told: resume, never refer to the crisis turn; a 2nd activation ends the call
                CRISIS ─(client crisis.stop | 60 s no answer)─► ENDED(reason=crisis)
any ─(driving phrase)─► GOODBYE(reason=driving)         "Call me back when you've parked."
any ─(pipeline failure x2 | room lost > 5 s)─► FALLBACK ─► ENDED(reason=fallback)
any ─(worker drain, 01 §4.4 #7)─► GOODBYE(reason=drained)
```

The diagram and the code below describe one machine: every time-driven arrow is `Governor.tick(t_s)`, called by the worker once a second and before each host request; every host-driven arrow is `Governor.commit()`.

**Turn machine:**

```
HOST_SPEAKING ─(TTS done)─► TURN_SIGNAL (breath + soft rising tone clip, PRD 12.1; not host talk time) ─► LISTENING
LISTENING ─(speech starts)─► LEARNER_SPEAKING
LEARNER_SPEAKING ─(silence >= ~600 ms, EOU >= 0.8)─► (preemptive host request starts, D18; cancelled if speech resumes)
LEARNER_SPEAKING ─(silence >= endpoint, turn complete)─► TURN_ENDED ─► THINKING ─► HOST_SPEAKING
LEARNER_SPEAKING ─(silence >= 1.2 s, turn incomplete, no backchannel yet this pause)─► BACKCHANNEL ─► LEARNER_SPEAKING
LEARNER_SPEAKING ─(silence >= endpoint + max_extend)─► TURN_ENDED
LEARNER_SPEAKING after a declared nudge ─(silence >= endpoint + 1.0 s, no backchannel on this pause)─► TURN_ENDED   (the self-repair window, PRD 5.4.6)
THINKING ─(1.2 s, no host audio yet)─► FILLER clip ("hmm", a breath; never a word) ─► THINKING
LISTENING ─(silence >= 8 s)─► SILENT ─(governor: smaller question)─► HOST_SPEAKING
any listening state ─(hold.down)─► FLOOR_HELD ─(hold.up, 300 ms grace)─► LEARNER_SPEAKING | TURN_ENDED      (never commit while hold.down)
any listening state ─(talkback.down)─► TALKBACK ─(talkback.up, Salma answered)─► FLOOR_HELD (if pad still held) | LISTENING   (clear_user_turn on the talkback frames)
HOST_SPEAKING ─(learner speech >= interruption_min_ms and >= 2 words)─► LEARNER_SPEAKING   (session.interrupt(); the cut text is logged as unsaid)
any ─(t >= hard_end_s)─► wait for the current learner turn to end (bounded by endpoint + max_extend) ─► GOODBYE   (law 7: nobody interrupts a learner mid-sentence)
```

All of this runs in the `turn-controller` on `AgentSession(turn_detection="manual")`: the controller consumes Silero VAD events and the audio turn detector's end-of-utterance probability, and it alone calls `session.commit_user_turn()` (with `stt_flush_duration` tuned in week 2), `session.clear_user_turn()` and `session.interrupt()`. The session's built-in endpointing is not used, so there is exactly one owner of end-of-turn.

**Budgets and the governor.** Before each host turn the governor computes `Allowances` from the budgets, the phase, the mode and the counters, writes them into the operator note (4.4), and after the reply checks the header against them.

```python
# apps/call-worker/forone_call/governor.py
from dataclasses import dataclass, field

@dataclass
class Counters:
    clarify: int = 0; nudge: int = 0; recall_gaps: int = 0; retell: int = 0; praise: int = 0; pushback: int = 0
    silence_offers: int = 0; recasts_this_turn: int = 0; violations: int = 0; guard_hits: int = 0
    recast_off_target: int = 0; clarify_on_clean_turn: int = 0; wrong_memory: int = 0

@dataclass
class Allowances:
    recast: bool; clarify: bool; nudge: bool; recall_gap: bool; retell: bool; praise: bool
    close: bool; goodbye: bool; smaller_question: bool; wrap_offer: bool
    must: list[str] = field(default_factory=list)   # the "due" side: moves the host owes this turn (PRD 5.4.6 minima)
    shorter: bool = False                           # host share over 40% after minute 2 (PRD 5.4.3)

BUDGETS = {
  "first":     dict(clarify=1, recast_per_turn=0, nudge=0, recall_gaps_min=0, recall_gaps_max=0, retell=0, praise=1, silence_offers=2, pushback_min=0),
  "main":      dict(clarify=3, recast_per_turn=1, nudge=1, recall_gaps_min=2, recall_gaps_max=4, retell=1, praise=1, silence_offers=2, pushback_min=1),
  "round_two": dict(clarify=2, recast_per_turn=1, nudge=0, recall_gaps_min=0, recall_gaps_max=1, retell=1, praise=1, silence_offers=2, pushback_min=0),
}
ANXIETY_OVERRIDE = dict(nudge=0, recall_gaps_max=1, recall_gaps_min=0)   # PRD 5.4.7: recasts kept, more backchannel, simpler questions
RETELL_WINDOW_START_S = 120                                              # [ASSUMPTION] 2:00; the M0 call timings set it in week 4

class Governor:
    def __init__(self, kind, budgets, limits, anxiety: dict, recast_targets: set[str]):
        self.b = dict(budgets); self.c = Counters(); self.phase = "CONNECTING"; self.mode = "normal"
        self.limits = limits; self.turn_words = []           # learner words per turn in the first 2 min
        self.silences_8s = 0; self.crisis_activations = 0; self.recast_targets = recast_targets
        self.host_ms = 0; self.learner_ms = 0
        if anxiety["prior"]: self.enter_anxiety("prior")
        elif anxiety["last_call_abandoned"]: self.enter_anxiety("last_call_abandoned")   # PRD 5.4.7's third trigger

    def enter_anxiety(self, why):
        if self.mode == "anxiety": return
        self.mode = "anxiety"; self.b.update(ANXIETY_OVERRIDE); self.why_anxiety = why   # logged on call_turn and call_ended

    def tick(self, t_s: float):                              # time-driven transitions, once a second and before each request
        if self.phase in ("ARGUE", "ARGUE_AFTER") and t_s >= self.limits["close_begin_s"]: self.phase = "CLOSING"
        if self.phase == "CLOSING" and t_s >= self.limits["hard_end_s"] - 20: self.phase = "GOODBYE"

    def retell_ended(self):                                  # the learner's retell turn ended (never cut by the 90 s ring)
        if self.phase == "RETELL": self.phase = "ARGUE_AFTER"

    def observe_learner_turn(self, words: int, speech_ms: int, t_s: float):
        self.learner_ms += speech_ms
        if t_s <= 120: self.turn_words.append(words)
        if t_s >= 120 and self.turn_words and median(self.turn_words) < 4: self.enter_anxiety("short_turns")

    def observe_host_turn(self, speech_ms: int): self.host_ms += speech_ms

    def observe_silence_8s(self):
        self.silences_8s += 1
        if self.silences_8s >= 2: self.enter_anxiety("two_silences")

    def allowances(self, t_s: float) -> Allowances:
        b, c = self.b, self.c
        in_argue = self.phase in ("ARGUE", "ARGUE_AFTER")
        in_retell_window = RETELL_WINDOW_START_S <= t_s < self.limits["close_begin_s"] and self.phase == "ARGUE"
        must = []
        if in_argue and t_s >= 150 and c.recall_gaps == 0: must.append("recall_gap")
        if in_argue and t_s >= 240 and c.recall_gaps < b["recall_gaps_min"]: must.append("recall_gap")
        if in_retell_window and c.retell == 0 and t_s >= self.limits["close_begin_s"] - 90: must.append("retell")
        if in_argue and t_s >= 120 and c.pushback < b["pushback_min"]: must.append("pushback")
        share = self.host_ms / max(1, self.host_ms + self.learner_ms)
        return Allowances(
            recast=b["recast_per_turn"] > 0,
            clarify=c.clarify < b["clarify"],                 # the cap is the only hard gate; "clarify on a clean turn" is a logged quality metric
            nudge=c.nudge < b["nudge"] and self.mode == "normal" and in_argue,
            recall_gap=c.recall_gaps < b["recall_gaps_max"] and in_argue,
            retell=c.retell < b["retell"] and in_retell_window,
            praise=c.praise < b["praise"] and self.phase in ("CLOSING", "GOODBYE"),
            close=self.phase in ("CLOSING", "GOODBYE"),
            goodbye=self.phase == "GOODBYE",
            smaller_question=self.phase == "SILENT" and c.silence_offers < b["silence_offers"],
            wrap_offer=self.phase == "SILENT" and c.silence_offers >= b["silence_offers"],
            must=must, shorter=t_s >= 120 and share > 0.40,
        )

    def check(self, moves: dict, a: Allowances, turn_confidence: float, threshold: float) -> list[str]:
        bad = []
        if moves.get("recast") and not a.recast: bad.append("recast")
        if moves.get("clarify") and not a.clarify: bad.append("clarify")
        if moves.get("nudge") and not a.nudge: bad.append("nudge")
        if moves.get("recall_gap") and not a.recall_gap: bad.append("recall_gap")
        if moves.get("retell") and not a.retell: bad.append("retell")
        if moves.get("praise") and not a.praise: bad.append("praise")
        # the never-list (grading, explaining grammar, "wrong", "the correct form is") is not a header key:
        # it is enforced by the prompt, by guard.check_output on the text (D17) and by the offline suite
        r = moves.get("recast")
        if r and r["form"].lower() not in self.recast_targets: self.c.recast_off_target += 1      # PRD 5.4.6: targets or meaning-blurring errors only; logged, not blocked
        if moves.get("clarify") and turn_confidence >= threshold: self.c.clarify_on_clean_turn += 1
        return bad

    def commit(self, moves: dict):
        c = self.c
        c.clarify += bool(moves.get("clarify")); c.nudge += bool(moves.get("nudge")); c.pushback += bool(moves.get("pushback"))
        c.recall_gaps += bool(moves.get("recall_gap")); c.retell += bool(moves.get("retell")); c.praise += bool(moves.get("praise"))
        c.wrong_memory += bool(moves.get("wrong_memory"))
        if moves.get("retell"): self.phase = "RETELL"
        if moves.get("close") and self.phase in ("ARGUE", "ARGUE_AFTER", "CLOSING"): self.phase = "CLOSING"
        if moves.get("goodbye"): self.phase = "GOODBYE"

    def minima_unmet(self) -> list[str]:                     # logged on call_ended; a 50-call gate
        b, c = self.b, self.c
        out = []
        if c.recall_gaps < b["recall_gaps_min"]: out.append("recall_gap")
        if b["retell"] and c.retell == 0: out.append("retell")
        if c.pushback < b["pushback_min"]: out.append("pushback")
        return out
```

`anxiety.last_call_abandoned` is the third PRD 5.4.7 trigger and is read here (the first draft read only the prior). `meaning_lost` is gone: nothing could compute it; the clarify cap is the only hard gate and a clarification on a turn whose mean recognizer confidence is at or above the package threshold is counted as `clarify_on_clean_turn`, a quality metric. The `must` list is rendered in the operator note as "do this turn: a recall gap" and the retell as "ask for the retell now"; `minima_unmet` and `violations` are both 50-call gates (4.13). Anxiety mode no longer moves a correction anywhere (the notes it moved to were removed by ADR-06); `anxiety_mode` and `why_anxiety` are carried on `call_ended` so 05 can weight the call.

**The declare-then-speak protocol.** The host's reply begins with one line:

```
@m r="I go">went g=rg2
You WENT to the derby with your manager? With who else?
```

The header grammar (layer A of the prompt spells it out): `@m` then zero or more space-separated keys; absent means not used. `r="<heard>"><form>` recast; `c` clarify; `n` nudge; `g=<id>` recall gap; `t` retell; `p` praise; `pb` pushback; `x` close; `bye` goodbye; `wm="<quote>"` wrong memory (4.4); `ai` AI disclosure; `crisis`. The example is 11 tokens; the first draft's full JSON header (`@moves {"recast":{...},"clarify":false, ... "ai_disclosure":false}`) was 55 to 70 tokens and, at the 60 to 90 tokens/s a Sonnet-class model streams, cost 0.6 to 1.0 s of first audio, which is why the budget in 4.15 did not add up. The worker buffers tokens until the first newline (8 to 15 tokens, 100 to 200 ms, measured as `header_tokens` and `header_ms` on every host turn), parses the line, runs `check()`. On an empty `bad` list it streams the rest of the text into TTS sentence by sentence, each sentence first through `guard.check_output("host", sentence)` (D17, under 20 ms), with the recast `form` wrapped in the vendor's emphasis markup and the span marked for the caption. On a violation, a guard hit or a malformed header it cancels the stream, discards the partial reply, rebuilds the single operator note for this turn with the prohibition appended (`forbidden this turn: nudge (you declared it; reply again without it)`; never a second system entry, because a mid-conversation system message must follow a user message and be last or followed by an assistant turn) and re-requests once (measured cost about 600 ms, expected on well under 5% of turns after prompt tuning; `violations` is a quality metric and the offline suite's first regression check). A second violation is spoken anyway and logged as `move_violation`; a second guard hit is replaced by the package filler line ("Hang on, say that again?") and logged, because an explicit correction is never spoken (ADR-06); the call never stalls on the governor. A missing or malformed header on the re-request is spoken and logged as `header_missing`. `stop_reason: max_tokens` (with `max_tokens: 200` this needs a 40-word reply, which the prompt forbids) speaks what was produced up to the last sentence end and logs `truncated`.

**Timers.** `t` is seconds since the opening line started. At `close_begin_s` (390 for main) the operator note says "begin a natural close"; at `hard_end_s - 20` (460) it says "say goodbye now in one line"; at `hard_end_s` (480) the worker stops the host after the current TTS sentence if the host is speaking, or, if the learner is speaking, waits for that turn to end (bounded by `p + max_extend`), then plays the goodbye line; nobody is cut mid-sentence (law 7). For `first`: 60 and 90. For `round_two`: 120 and 180. The learner's ✕ sends `end_call`; the worker lets the current learner turn finish (at most 3 s), requests one host line with `goodbye` allowed only, speaks it, ends. Round two is available from the moment the `calls` row of kind `main` is done until the session closes (PRD 5.4.9, PRD 4 rule 1); the client suggests it on Today the next day from `calls` (kind `main` done, no `round_two` row).

**Retell.** When the host declares `retell`, the worker sends `retell_ring {seconds: 75}` to the client (a soft ring, never red), sets the turn controller's max extension to 2.5 s for the retell turn and disables the 8 s silence offer until the first speech; the retell ends only when the learner's turn ends. At 90 s the ring simply disappears and the host keeps waiting for the end of the learner's turn; the host never cuts a retell short (PRD 5.4.6 "never cuts the learner off"). [ASSUMPTION] The retell window opens at 2:00 and closes at `close_begin_s` (the first draft's 4:30 close and its "one recall gap first" precondition are gone, because they could silently skip the mandatory retell); the Milestone 0 call timings (how long learners take to warm up) set the 2:00 figure in build week 4.

**Interrupted call.** A call cannot resume (PRD 4 rule 4). If `web` reconnects to a room whose job has ended, or the learner returns after an abandoned call, `POST /v1/calls` creates a new call with `resumed_after_drop: true` under the door rule in 4.1 (the earlier call does not count as "done" when `end_reason in (abandoned, fallback, pipeline_error, drained)` and under 120 s of learner speech); the bundle's opening clip is then the pre-rendered "gap" variant ("You left me hanging. Where were we?"), and the previous call's turns are still in the event log for assessment. In the beta the gap variant is one line per host voice, rendered with the backchannels (4.5), not per episode.

**Wrong memory (PRD 8.4 rule 7).** When the listener says that something the host was told about them is wrong, the host declares `wm="<the listener's words>"`, says "My mistake, noted" (or the bible's equivalent) and never uses that fact again in the call; the worker emits `wrong_memory_flag {fact_id|null, learner_quote, turn_index, door: "call"}`, adds `do not mention: <fact>` to every later operator note, and the memory keeper (04) fixes the fact after the call. The count feeds PRD 16.1's "wrong memories under 1 in 100 callbacks"; the host never argues back from the brief.

### 4.4 The host prompt and the request shape

The request to the host model has three layers, rendered in cache order (tools, system, messages). Layer A is identical for every learner of one host and accent, so it is cache-warm across the whole fleet; layer B is per call and warm from the second turn; the messages carry a cache breakpoint on the last learner turn so the growing history is read from cache.

```
[SYSTEM, breakpoint 1: static per host and accent, about 1,800 tokens]
You are {Mona|Karim}, co-host of "For one", on a short voice call with one listener who has just heard today's episode. {host bible, authored: values, humour, speech patterns, what you never do, stance toward the listener}
You are an AI host. If asked whether you are real, say so plainly in one short sentence and carry on. Your storylines are the show's fiction; you never claim to exist outside the show or to miss the listener.
HOW YOU TALK: {target_language} only; one or two sentences, under {max_words_per_turn} words; one question at a time; the listener should talk at least twice as much as you; never finish their sentence; never grade, explain grammar, mention progress or levels, guilt, or say you will miss them; no homework.
HOW YOU HELP (the listener must never feel tested or taught): clarification request when meaning is lost ("Sorry, you went, or you're going?"); recast one error at most per reply, only on the target or on an error that blurred meaning, the corrected word stressed, inside a reply with its own point ("You WENT to the derby?"), and then a pause for them; never say "wrong", "the correct form is", "you should say", never repeat their error back as an error; one nudge per call ("Wait, yesterday you...?") then wait; recall gaps from the brief: start the line and stop; push back on your position at least once, like a person who disagrees; hints before answers: "how do I say X" gets a hint, the word only on a second ask; "what does X mean" gets a plain answer; absorb side-switching, rejected premises, off-topic turns and early endings without steering back to a script.
IF THE OPERATOR NOTE SAYS anxiety mode: shorter turns, one idea per turn, yes/no or either/or questions, no nudge, keep the recasts, let silences be.
IF THE OPERATOR NOTE SAYS "do this turn: ...": that move is owed; make it this turn.
IF THE LISTENER SAYS SOMETHING YOU WERE TOLD ABOUT THEM IS WRONG: say "My mistake, noted", declare wm, and never use that fact again.
IF THE LISTENER IS IN DANGER OR DISTRESS: declare crisis in the header and say nothing else; the producer takes over.
IF THEY SAY THEY ARE DRIVING: "Call me back when you've parked. I'll be here." and declare bye.
OUTPUT FORMAT: first line `@m` followed by only the moves you use, space-separated: r="<what you heard>"><the form> (recast), c (clarify), n (nudge), g=<id> (recall gap), t (retell), p (praise), pb (pushback), x (close), bye, wm="<their words>", ai (you said you are an AI), crisis. Nothing else on that line; an absent key means you did not use the move. Then a newline, then only what you say aloud. No stage directions, no markdown. The operator note before each listener turn tells you which moves are allowed and which are owed; a move that is not allowed must not be used.

[SYSTEM, breakpoint 2: per call, the HostBrief rendered as text, about 700 tokens]
LISTENER: Faisal (FY-sal), he. EPISODE IN 3 LINES: ... THE QUESTION: ... PHRASES THE EPISODE PLANTED: ...
YOUR POSITION: ... PUSHBACK: ... GRAMMAR TARGET: past simple in narratives. MOVES THAT MAKE IT NECESSARY: "Walk me through exactly what happened on Saturday." ... ECHO PLAN (recast list): "I go" -> "went" ... WORDS: line-up ("ask who starts") ... RECALL GAPS: rg1 "Karim said the plan was a bit too... what was the word?" (expected: ambitious) ... RETELL: "Mona missed it. Sixty seconds: what happened at the derby?" CALLBACK ALLOWED: "the manager who supports the local club" (one use). NEVER MENTION: ... DAY TYPE: main.

[MESSAGES]
user: (the listener's first turn, streaming text)
system: {"note":"t=0:41 mode=normal allowed: recast clarify(3 left) recall_gap(2..4, used 0) pushback ; not allowed: nudge retell praise close ; listener held floor: no"}   <- the one operator note per turn, cleared on the next user message (clear_at: next_user_message)
assistant: @m r="I go">went\nYou WENT to the derby...
user: ...
system: {"note":"t=2:34 mode=normal ... do this turn: a recall gap ; shorter: one sentence, one question","whisper":null}   <- owed moves and the host-share lever; the observer's slot (D14) is null in the beta
```

The operator note uses the `clear_at: "next_user_message"` option so the history carries one note at a time rather than about 25 accumulated system entries; the cached prefix is unaffected because the notes sit after the breakpoint on the last user turn. If the pinned SDK or API version does not offer the option, the notes accumulate and the week-1 probe measures the cost (about 25 × 40 tokens, read from cache). Anxiety mode is rendered as `mode=anxiety (simpler questions)`, the host-share lever as `shorter: one sentence, one question` whenever the running host share exceeds 40% after minute 2, and a wrong memory as `do not mention: <fact>` on every later note.

Request parameters for Sonnet 5.5: `model: claude-sonnet-5-5`, `max_tokens: 200` (the first draft's 120 with a 60-token header risked truncating the spoken sentence), `output_config: {effort: "low"}`, `thinking: {type: "between_tools"}` (the host has no tools, so the reply starts at once; `effort` is `low` because the reply is one or two sentences; the 50-call test compares `low` with adaptive thinking at `low` and keeps whichever meets the latency gate with the better move-contract score), `stream: true`, cache breakpoints on the two system blocks and the last user turn. Operator notes are `{"role": "system"}` entries inside `messages`, which Sonnet 5.5 accepts without a beta header and which leave the cached prefix intact. The host never uses prefill (removed on this model family) and never uses forced tool choice. On a `refusal` stop reason (rare on this content) the worker speaks a neutral in-character line from the package ("Hang on, say that again?") and logs it. Every host turn logs `usage.cache_read_input_tokens` as `cache_read_tokens` on `call_turn`, so a silent cache miss (a byte changed in the prefix, a plugin that moved a breakpoint) shows up in `calls.metrics` rather than on the invoice. [DECISION] The week-1 probe (30 lines through the stock LiveKit Anthropic plugin, logging `cache_read_input_tokens` and `cache_creation_input_tokens` per turn) decides whether the plugin can place the three breakpoints, the system entries, `effort` and `between_tools`; if not, the adapter is a thin `llm.LLM` subclass over the Anthropic SDK (one file), and 3.1 says so.

**One request builder per model (D7).** The adapter renders the same conversation three ways: Sonnet 5.5 as above; Haiku 5.5 with `thinking` omitted (the field is accepted only by Sonnet 5.5 and returns 400 elsewhere) and `output_config.effort: "low"` set explicitly (Haiku's default is `medium`); Gemini 3.8 Flash with layers A and B as its system instruction (no cache) and each operator note folded into the next user turn as a bracketed first line (`[operator: t=2:34 allowed: ...]`), so the governor's contract stays enforced on that path too. A 20-line fixture test sends each shape to each model in build week 2 and the weekly canary call repeats it.

Fallback order on a model error or a first-token wait over 1.2 s: retry once on the same model with a 1.5 s timeout; then `claude-haiku-5-5` in its own request shape; then the second vendor from `vendors.yaml` (`google/gemini-3.8-flash`) in its shape. The fallback used is recorded on the `call_turn` event and in `calls.vendors`. Rate limits: 15 concurrent calls are about 60 host requests a minute with 6 to 10k-token prefixes (mostly cached reads); the Anthropic tier and the ITPM accounting for cached tokens are checked in build week 1 against the beta's peak and the number is written into 08's vendor contracts list.

**Repair and crisis phrases on the open mic (PRD 5.4.4 rule 6 and 7.9.1, "in either language").** [DECISION] The host stream runs with `languages: [target, native]` and code-switch on (the recognizer returns per-token language tags); the worker matches `languages.repair_phrases` and `languages.crisis_keywords` in both languages on the raw streaming final, then strips the native-language spans from the text sent to the host and logs their timings as `native_spans` on `call_turn` so the analyst can mask them in the verbatim text; D5's isolation is kept by code, not by vendor configuration. The host-stream secondary (Deepgram) does not code-switch to Arabic, so on the secondary the native-language detection on the open mic is off and the call is logged `native_detection: off`; the talkback stream still catches the native-language crisis keywords whenever S is held. [OPEN for Muath, with counsel] whether that narrowing on the secondary is acceptable for the beta (10-decision-records §10 item 12). On a match the operator note says `listener did not understand: rephrase your last line more simply, shorter, no new question`, and the turn is logged as `repair_request`. Previous-track (Media Session) on the call replays the host's last line from the worker (4.6) and logs `replay_line {door: "call"}`; the host is not told.

### 4.5 Turn-taking: adaptive patience, hold-to-talk, backchannels, silence

**Pause profile.** `skills.pause_profile.eot_silence_ms` is owned and written by the learner model domain (04 §4.3.4), which has the one formula; this domain reads `p = clamp(eot_silence_ms / 1000, 1.0, 2.5)` and a new learner has `p = 1.5`. The first draft specified a P90 of within-turn pauses here, which 04 did not adopt and which measured a censored distribution: any silence of at least `p` ends the turn, so no pause longer than the endpoint is ever observed except under a held floor, and a P90 of a distribution truncated at `p` can only ratchet `p` down toward 1.0 s, which is the "host cuts the learner off" failure. What this domain gives 04 instead are two signals with an explicit direction, both on `call_turn` and summed in `call_ended.metrics`: `cut_offs` (the learner resumed speech within 700 ms of the host starting, gated by the same 0.5 s / 2-word threshold as interruptions so speaker echo does not count), which should push `p` up by 0.25 s per call, and `pauses_ms[]` from held-floor turns plus the pre-endpoint pauses between 0.6 s and `p`, whose P90 may pull `p` down only when no cut-off occurred in the last 3 calls. Section 9 carries this as an ask of 04. Within a call the worker still adapts: each cut-off adds 0.25 s to `p` for the rest of the call (cap 2.5), stays in P0 (it is a counter and one `+=`), and the adapted value is reported as `endpoint_ms_final`.

**Endpointing.** The turn controller combines three signals: Silero VAD (speech or silence per 20 ms frame), the end-of-utterance probability of LiveKit's audio turn detector (the model that lists Arabic and the other native languages; the text-based `MultilingualModel` is deprecated, slated for removal in Agents 2.0, and does not list Arabic, so D1's first-draft justification was wrong), and the hold state. The detector costs about 50 to 160 ms of CPU per decision and a 396 MB model baked into the image (01 §4.8).

| Condition at a silence of length `s` | Action |
|---|---|
| `s >= ~0.6 s` and EOU probability at least 0.8 | start the host request on the interim transcript (D18); cancel it if speech resumes |
| `s >= 1.2 s`, turn incomplete (EOU probability under 0.5), no backchannel yet in this pause, floor not held or held | play one backchannel clip (4.5 below); keep listening |
| `s >= p` and EOU probability at least 0.5 | end of turn: `commit_user_turn()` |
| `s >= p + max_extend` (max_extend 1.5 s for `p < 1.5`, 1.0 s for `p >= 1.5`; during the retell 2.5 s) | end of turn regardless |
| after a declared nudge: `s >= p + 1.0 s` and no backchannel on this pause | end of turn (the self-repair window) |
| floor held | never commit; backchannel allowed once per pause as above |
| `hold.up` received | 300 ms grace; if speech resumes, continue; else end of turn |
| `s >= 8 s` in `LISTENING` (the learner has not started) | `SILENT`: the governor allows `smaller_question`; after two offers, `wrap_offer` |

`AgentSession` runs with `turn_detection="manual"`: the controller alone calls `session.commit_user_turn()` for end-of-turn, `session.clear_user_turn()` when talkback frames must not become part of the turn, and `session.interrupt()` on a barge-in of at least 0.5 s and 2 words (so an open-mic learner can cut the host off with real speech but not with "mm"). Hold-to-talk is "never commit while `hold.down`". The built-in `turn_handling.min_delay`/`max_delay` and `InterruptionOptions` are not used, because the custom table above (backchannel at 1.2 s, hold state, retell and nudge extensions, in-call `p` changes) cannot be expressed through them and two deciders of end-of-turn is the bug the first draft had. The option names are verified against the pinned SDK version in week 1 and written to `SDK-NOTES.md`. In week 1 the detector also runs over the Milestone 0 learner transcripts to report its "incomplete" rate on finished learner sentences ("I go to... the mall"); if it is over 30% the controller uses VAD plus `p` only, with no detector, and `max_extend` is set from that data rather than by assumption. Onboarding turns in the learner's native language use VAD plus a fixed 1.8 s delay (4.9).

**Backchannels, fillers and the turn signal (D4, PRD 12.1).** [DECISION] This domain owns the clips: the first time a `voice_id` is used, the worker (through `voice-studio.render(RenderJob)`, 02's public API) renders 8 to 10 short backchannel lines per host ("mm", "go on", "yeah?", "right", "okay", a breath), 2 to 3 filler clips ("hmm", a breath) for the `THINKING` state, the turn-signal clip (a breath and a soft rising tone, never a beep) and the two opening-line variants for `resumed_after_drop`, and caches them under `forone-media/package/voices/{voice_id}/` (SSE-KMS, ADR-12); the bundle's `voice.*_clips` point at them. The per-episode opening line (D11) is rendered by the brief compiler at episode publish through the same API, an ask of 02 in section 9. The controller picks a backchannel at random excluding the last two, plays it on the `host` track at -6 dB, and never plays more than one per pause or more than one per 10 s. In anxiety mode the threshold drops to 1.0 s. The filler plays once when `THINKING` has lasted 1.2 s with no host audio (the "slow model" case in section 5). Backchannels, fillers and the turn signal are logged inside the learner's `call_turn` payload (`backchannels: [{t_ms, clip_id}]`) and never count as host talk time.

**Hold-to-talk.** The pad sends `hold.down` and `hold.up` over the data channel (reliable). `hold_floor` events are logged with the duration. Holding is also how a learner reads from the planning card without being interrupted.

### 4.6 The Huh? signal on the call

On the call screen the Huh? affordance of the player maps to "repeat what you just said": previous-track on the headphones or a small ⟲ under the caption. [DECISION] The client only sends `replay.host_line {host_line_id}`; the worker keeps the last host line's PCM in memory and re-plays it on the `host` track (no vendor call, about one network round trip), logs `replay_line {door:"call", host_line_id}`, and does not inform the host; if the learner then says "sorry?" the repair path in 4.4 handles rephrasing. The first draft replayed from a client-side buffer; capturing a remote WebRTC track into a replayable buffer on iOS Safari is unreliable and was work 06 had not planned. The learner's own Huh? taps during the call feed the teacher's difficulty dial like the player's (PRD 9.6) through the same event type.

### 4.7 Talkback to Salma

```
job start ─►                                   worker: open the talkback STT stream (talkback_stt, languages [native, target], code-switch on) beside the host stream; no frames yet
S down ─► client: talkback.down {t_client}     worker: freeze turn detector; mark floor held; route frames from (t_down - 400 ms pre-roll) to the talkback stream;
                                                       host STT frames muted; the recorder drops the same frames from the turn PCM and the full mix
S up   ─► client: talkback.up                  worker: finalize talkback segment (<= 400 ms); run the native-language crisis keyword list; resolve (4.7.1);
                                                       synthesize Salma; play on `salma` track; send ui.talkback {text_native, word_target, mode}; log talkback;
                                                       unfreeze (floor stays held if pad is down)
```

Keeping the stream open from job start (D5) costs about $0.013 a call and takes the 200 to 500 ms websocket setup off the critical path of a 1 to 2 s hold; a short press that releases before the segment is final still resolves. Talkback audio is streamed only: no object is written, nothing is retained beyond the vendor's in-transit processing, and the frames between `talkback.down` (minus the pre-roll) and `talkback.up` are excluded from the learner turn's PCM and from the full mix, so native-language speech never enters the verbatim transcript or the error profile; `talkback_ms_excluded` on the `call_turn` keeps the fluency measures honest (05 §4.1 assumes talkback clips never reach it, which is now true by construction).

**4.7.1 Resolution.** One small model call for every ask (D6; the reverse gloss index of the first draft is cut for the beta, see 10-decision-records and section 7).

1. Normalize the native-language transcript; match the package's patterns for "how do you say X" and "what does X mean" (`packages/native/<lang>/talkback/patterns.yaml`; for Arabic كيف أقول, وش أقول, إيش معنى بالإنجليزي ...). The match sets `kind` early so the model call can be skipped for "are you real?" (kind `other`, answered honestly by Salma from a package line, PRD 7.8.1) and for a crisis keyword (the crisis path, 4.3; `crisis_activation.role = "salma"`).
2. Otherwise: `claude-haiku-5-5`, Salma's talkback prompt (persona excerpt from the native package, 300 tokens cached), input: the transcript, the produced-lemma list (names only), the active targets. Output schema (structured output): `{kind: "word"|"phrase"|"meaning"|"other", target: string, native_answer: string, lemma: string|null}`. Timeout 1.5 s; at 700 ms Salma's 300 ms wait clip (`salma_wait_native`, for Arabic "لحظة") plays so the 2 s budget is felt as a pause, not a failure; on timeout Salma says, in the native language, "say it again, slower" and the ask is logged as `unresolved`.
3. Word-or-hint (D6): `mode = "word"` if `lemma not in produced_lemmas` or this is the second ask for the same lemma in this call; else `mode = "hint"` and the hint is the first sound of the word plus, when `last_session_label` exists, "you used it on {label}". The hint text comes from a template in the native package, not the model.
4. Salma's line: `{native_answer}` with the target-language word embedded (for example "لاين-أب... line-up"); the target-language share of her words follows `english_share` (renamed `target_share` in the brief) only in the framing, never in the word itself.

**4.7.2 Voice.** Salma's talkback uses `salma_tts` with the native package's Salma voice and `style: "close"`: the adapter maps this to the vendor's lowest-energy, intimate delivery where style tags exist, and in every case the worker applies a 3 dB level reduction and a high-shelf cut at 8 kHz on the `salma` track so she sits "closer and drier" than the host (PRD 7.3). The host track is silent during talkback because the floor is held, so no ducking is needed.

**4.7.3 Latency.** Budget under 2 s from S-up: STT finalization 300 ms, resolution 400 to 700 ms (Haiku; the wait clip covers the tail), Salma TTS first byte 200 to 400 ms, network 100 to 200 ms. Measured `talkback_ms` on every `talkback` event. The talkback-ask fixture (4.13) measures the whole path on real asks.

**4.7.4 Host isolation.** The host receives nothing about the talkback (PRD 5.4.5: the audio goes to the native-language recognizer, not the host). The learner's next target-language turn arrives as usual. The worker only adds `listener held floor: yes` to the operator note so the host does not comment on the pause.

**4.7.5 Logged.** `talkback {t_ms, ask_native, kind, lemma, mode, resolved_by: "pattern"|"model"|"none", talkback_ms, cost_usd}`. Talkback asks per call by lemma is a PRD 16.2 measure and a PRD 5.4.5 progress signal; the Word bank's `lookups` per lemma are updated from this event by the data domain.

### 4.8 Captions

Host captions are built from the TTS stream: in the beta one `ui.caption` per sentence as that sentence's audio starts, with the recast word bold from the header's `form` string matched in the text (word-level captions from vendor word timings are P1; ElevenLabs and Cartesia return timings, Inworld and Gemini are verified in week 1). The recast is also audible, not only visible: the TTS adapter wraps the `form` span in the vendor's emphasis markup where one exists (ElevenLabs audio tags, Inworld markup, a style instruction for Gemini), the result is checked by ear in week 1, and `recast_emphasis_supported` is logged per vendor on `vendor_calls`, because PRD 5.4.6 asks for the corrected word "stressed in the voice" and plain text leaves that to chance. The learner's words are never sent to the client as captions (PRD 5.4.8): the worker disables the session's room transcription output for both user and agent segments (captions travel only on `forone.ui`), so nothing in the room ever carries a learner segment, and `call-bench` checks that no `lk.transcription` stream does; the first draft's "the client does not subscribe" would have shipped the learner's words to the phone regardless. The Controls switch for captions lives on the client; the worker always sends them (cheap) so turning them on mid-call is instant.

### 4.9 Salma at onboarding (PRD 2.2 A3) and the first call (A7)

The same worker runs a second persona, chosen by `call.kind`, for the talk path only. The pipeline is the same with four differences: the recognizer is the talkback configuration (`[native, target]`, code-switch on) on the main stream; end-of-turn is VAD plus a fixed 1.8 s delay with no turn detector (the detector's native-language coverage is not relied on for a three-minute intake); the model is `claude-sonnet-5-5` with Salma's bible from `packages/native/<lang>/` and the onboarding contract; the voice is `salma_tts`. The typed path (A2 "Type", or mic denied) is 01's: `POST /v1/onboarding/{id}/messages`, one streamed Sonnet call per turn in `api`, with the same contract and fact cards rendered from the response; it needs no room, no worker and no data channel, and this document no longer carries a `text.turn` message (the first draft had both paths, which is wasted work for this team). `POST /v1/onboarding/start` requires an unredeemed invite code (01) and the per-learner call-start cap from `forone.core.costguard` (07, 6 × `episodes_per_day` a day, ADR-15) applies to pre-account learners as one start an hour, because an anonymous room costs about $0.10.

**First sound under 60 s (PRD 15; the A3 path's own budget).** `POST /v1/onboarding/start` (client domain) creates the pre-account learner and the room before the mic prompt; the worker's first two Salma lines are static clips from the native package (`salma_intro_1`, the AI disclosure, and `salma_intro_2`, the first question) played the moment the learner's track is subscribed, which covers the 1 to 2 s of vendor websocket setup. The components: page load 1 to 3 s (A1 and A2 are static at the edge), the invite form and the mic prompt (the learner's time, typically 10 to 30 s), `POST /v1/onboarding/start` 150 ms, room join 0.5 to 1.5 s, worker job accept under 500 ms on a warm task, bundle fetch under 100 ms, first clip at track subscription: about 3 s of system time, so the 60 s budget is met unless the learner lingers on the mic prompt, which `first_sound_ms` on `call_ended` (kind `onboarding`) distinguishes from `first_sound_system_ms`. Salma's live reply latency after the intro clips follows 4.15 with one difference: no header and no governor re-request, so about 1.1 to 1.4 s at p50.

**The onboarding contract (code-enforced like the host's).** `turns_max = 8`; fields `name`, `talk_for_an_hour`, `need_english_for`; two English lines, one comprehension ("tell me what you heard, in any language"), one production ("say anything back in English"), each used exactly once and placed by the governor (after field 1 and after field 3); each field gets one re-ask then is marked `sparse`; a dated event in an answer becomes a follow-up candidate with a date. Salma's reply header:

```
@salma {"fact":{"field":"name","value":"Faisal","quote":"اسمي فيصل"}|null,"english_line":"comprehension"|"production"|null,"followup":{"text":"interview","date":"2026-11-27"}|null,"done":false}
```

The worker turns `fact` into `ui.fact_card {field, value, quote, card_id}` at once (the card appears under Salma as she hears it), and the client's ✎ and ✕ send `fact_card.edit` and `fact_card.remove`, which the worker folds into the next operator note and logs as `fact_card_edit` (on the typed path the same edits go to `api`). At `done` or turn 8 the worker emits `onboarding.intake_completed {learner_id, intake_facts, name_clip_ref, name_clip_text, english_moments: [...]}` (the pipeline's trigger for the pilot) and ends. The name clip is the learner's turn audio for the `name` field, uploaded like any turn but with `media_objects.hold_until_consumed = true`, so the per-turn delete in `call/verbatim-turn` skips it and only `audio/expire` at +15 min removes it (pre-account learners have `voice_storage = false`, so without the flag the clip would be deleted seconds after it was spoken while 02 §4.9 reads it at `onboarding.intake_completed`); 02's name-pronunciation step must finish inside that window or work from `name_clip_text`, the native-language streaming output the worker already has. Salma's intake answers never leave the native language except the two scripted target-language moments.

**The first call (A7).** Kind `first`: the throwing host, budgets from 4.1 (no recast, no nudge), the Salma talkback introduction played as the native package clip `talkback_intro_native` on the `salma` track before the host's opening clip ("If you're stuck, hold the S button and ask me in {native_language}"), close at 60 s, end at 90 s. The host's opening line is the pilot's throw question re-asked.

Salma's variety within a native language (for Arabic: Gulf or a neutral standard) is the 7.3 blind test's choice per native package and is a `voice_casting.salma.variety` value; this domain reads it. [OPEN for Muath] see section 10.

### 4.10 Recording, verbatim re-transcription, pronunciation, deletion

**Capture.** The recorder keeps the learner's decoded PCM (48 kHz mono from WebRTC, downsampled to 16 kHz) per turn in memory, minus the frames routed to talkback (4.7). At end of turn it encodes the turn as Opus in Ogg at 24 kHz (the topology's chosen format; 16 kHz FLAC would serve ASR equally and is the swap if a verbatim vendor rejects Opus) and uploads it with SSE-C under the per-call key (`crypto.call_key`, D16) to `forone-voice/ephemeral/learners/{lid}/calls/{callId}/turn-{n}.ogg` when storage is off or `forone-voice/learners/{lid}/calls/{callId}/turn-{n}.ogg` when it is on (the recorder picks the prefix from `consent.voice_storage` at upload time; a consent flip mid-call moves nothing, because the call is treated as storage-off at `call.ended` and the full recording is simply not written), writing a `media_objects` row `{kind: "call_turn", call_id, turn_index, duration_ms, encryption: "sse_c_learner", key_derivation: "call:{call_id}", ephemeral: !voice_storage, expires_at: voice_storage ? null : call_end + 15m, hold_until_consumed: false}`, then emits:

```python
class CallTurnAudioReady(BaseModel):   # "call.turn_audio_ready"  sender: call-worker (through api)
    learner_id: UUID; call_id: UUID; turn_index: int; media_id: UUID; event_id: UUID   # the call_turn event this verbatim joins
    duration_ms: int; voice_storage: bool; is_last: bool; language: str                 # target_language; talkback audio has no object, so no "native" value
    talkback_ms_excluded: int; key_derivation: str
```

**`call/verbatim-turn`** (Inngest; shell in the topology, step bodies shared between this domain and the assessment domain): `verbatim_stt.transcribe(audio, language=target_language, disfluencies=True, word_timings=True)` through the `VerbatimRecognizer` adapter (role keyed by target language; for English AssemblyAI primary, ElevenLabs Scribe secondary, decided by the 30-clip test); `api` re-derives the call key from `key_derivation` for the read; the result is appended as a `call_turn_verbatim` event through `events.append()` with `{call_id, turn_index, text, words[{t, s, e, c}], vendor, disfluencies_kept, low_confidence_reason|null}` joined to the `call_turn` on `(call_id, turn_index)` (04 D2, ADR-19; nothing updates an event); it emits `verbatim.turn_completed`. If `voice_storage` is false and `hold_until_consumed` is false the step then deletes the turn's object and marks `media_objects.deleted_at`. Concurrency 20 global; retries 2 with the secondary vendor on the second retry; a turn that still fails is appended with `low_confidence_reason: "verbatim_failed"` and its evidence is low confidence (PRD 5.4.11).

**The full recording.** When voice storage is on, the worker also mixes both sides (learner mono plus host plus Salma, minus talkback frames) into one Ogg Opus file at call end and uploads `call_full` (not ephemeral, same key and `key_derivation`). It is what the archive plays (PRD 12.2) and what the notebook's tape plays by Range through `api`, which re-derives the key. When storage is off, no full recording is ever written and the tape shows the transcript. (The first draft named the polish card here; it was removed by decisions.md §3 and ADR-06.)

**Say it once, shadow lines [P1], small-door voice note, then-and-now.** The client records with `MediaRecorder` (`audio/mp4` on Safari, `audio/webm;codecs=opus` on Chrome; at most 60 s for the small door, 20 s for say-it-once, 90 s per then-and-now task) and uploads to `POST /v1/calls/{id}/voicenotes` or `POST /v1/recordings` with the reference text where one exists. Every upload is a `media_objects` row under the same rules and a `call.turn_audio_ready`-shaped event (`recording.turn_audio_ready`) so the verbatim path is one function.

**Pronunciation.** `call/pronunciation-score` runs on `pronunciation.requested {media_id, reference_text}` for say-it-once and shadow lines only (PRD 10.3): `Pronunciation.score(audio, reference_text)` on Speechace (secondary Microsoft), stores `{sentence_score, word_scores[], vendor, version}` as a `say_it_once` or `shadow` event payload update. Nothing is shown to the learner; the client gets no response body beyond `202`. Dial-in audio [P1] never reaches this function.

**Deletion windows.**

| Rule | Mechanism | Backstop |
|---|---|---|
| Storage off: audio deleted when verbatim succeeds, and in any case within 15 min of call end (PRD 5.4.11) | per-turn delete in `call/verbatim-turn`; `audio/expire` (topology) at `call.ended + 14 min` deletes anything with `ephemeral = true`; **when `api` was unreachable** for any `turn_audio_ready` post (so no `media_objects` row and no Inngest event exist), the worker, which holds the key and the S3 credentials, deletes the call's `ephemeral/calls/{callId}/` objects itself at call end + 14 min before the job exits, or hands the delete list to the task's drain timer if it is draining | S3 lifecycle on the `learners/*/ephemeral/` prefix at 1 day (the prefix that is actually written; the first draft's lifecycle rule pointed at a prefix nothing used); `privacy/verify` (07) checks hourly that no `ephemeral` object outlives `expires_at`, including the spool case |
| Revoke: all stored audio within 24 h (PRD 12.5 rule 3) | `learner/purge-audio` (topology) on `learner.consent_changed {voice_storage: false}`; a call in progress reads the flag at `call.ended` and treats the call as storage-off | key destruction on account deletion |
| Transcripts always kept | `call_turn` events are never deleted while the account exists | n/a |
| Then-and-now with storage off: kept only if the learner explicitly keeps that one (PRD 12.5 rule 2) | the client's "keep this recording" sets `media_objects.ephemeral = false` for that object only | |

The worker holds the per-call key in memory only for the job's lifetime and never logs it (ADR-18 drops the zeroization claim: Python cannot promise it, and the key is useless after the call because reads re-derive it from the DEK); the full recording's mix happens in the worker's memory, not on disk. The spool file (`forone-voice/spool/{callId}.ndjson`, section 5) holds events and the end record, never audio or keys, and is SSE-KMS under the environment key (07), readable by `spool/ingest` in `workflows` only.

### 4.11 Client-side audio (the call screen's audio contract; the screen itself is the client domain's)

| Concern | Decision |
|---|---|
| Mic | `getUserMedia({audio: {echoCancellation: true, noiseSuppression: true, autoGainControl: true, channelCount: 1}})`, requested only at A2 "Talk" or at the first Call tap (PRD 2.2 A2) |
| Playback | Two `HTMLAudioElement`s attached to the `host` and `salma` tracks with `playsinline`; the `AudioContext` is resumed in the tap handler that starts the call (iOS requires a user gesture); a 100 ms "studio" sting from the package plays on connect to prove the output route works |
| Echo | Hardware AEC through the constraints above; the worker's interruption threshold (0.5 s and 2 words) absorbs residual echo and gates the cut-off counter (4.5). The first draft's 150 ms client-side mic mute after each host sentence is removed: it cannot be timed (the client learns of a sentence only from a caption that arrives after the audio), it would clip a learner's barge-in, and on iOS, where earphones are not detectable, it would fire on every sentence. If echo proves a problem in build week 4 the mute returns only on Chrome where `enumerateDevices` confirms the speaker route |
| Earphones | Not reliably detectable on iOS; the client checks `enumerateDevices()` labels and `MediaTrackSettings.deviceId` on Chrome and suggests earphones once on the first call either way (PRD 5.4.1); the suggestion never blocks. Bluetooth earphones with the mic in use drop the audio session to the hands-free profile (narrowband, 8 to 16 kHz) in both directions; the recognizer test includes clips captured that way (4.13) and the one-time hint says "wired earphones work best" if those numbers are bad |
| Screen Wake Lock | `navigator.wakeLock.request("screen")` on call start; re-request on `visibilitychange` to visible; if the API is missing (older Safari) the screen shows a one-line notice and keeps a silent `<video>` loop playing |
| Background | On `visibilitychange` to hidden the client sends `client.hidden`; the worker waits 10 s for `client.visible`, then ends the call with `end_reason: abandoned` (iOS suspends WebRTC in the background, voice lens). The learner returns to a fresh call (4.3). "Calls abandoned on the move" (PRD 16.2) is computed from `end_reason: abandoned` plus `started_by: feed` and the M0 day-7 self-report; the first draft's "motion hints" are dropped (device motion needs an iOS permission prompt 06 does not have and is sensing about the person that trust promise 6, "told, not inferred", does not cover) |
| Headphone buttons [P1] | Media Session actions: `pause`/`play` toggles mute; `previoustrack` replays the host's last line (4.6); `nexttrack` triggers talkback for 5 s (an Ears-mode press-and-release equivalent; the S bubble still shows). The mappings ship after 2026-12-22 (section 7); in the beta the pad and the S button are the only controls |
| Route changes | On `devicechange` (AirPods connect or disconnect) the client re-attaches the audio elements; LiveKit's reconnect handles the transport |
| Bandwidth | Opus 48 kHz, 32 kbps, DTX on, FEC on; LiveKit adaptive stream off for audio (there is no video) |
| Pad and S button | Pointer events (`pointerdown`, `pointerup`, `pointercancel`) with `touch-action: none`; `pointercancel` (a system gesture) is treated as release; messages carry the client timestamp so the worker can align the pre-roll |
| Planning card | Shown by the client before connecting when `Read` is `not_started` or `skipped` (PRD 4 rule 3) with the three `planning_words` from the brief; "Ready" starts `POST /v1/calls` with a `clientKey` (idempotent for 60 s, so a double tap never creates two rooms) |
| Token lifetime | The participant token lives 10 minutes (01); at minute 8 of a live call the client fetches a fresh one (`GET /v1/calls/{id}/token`) so a reconnect at minute 9 is possible; a reconnect to a room whose job has ended is a fresh call (4.3) |
| Crisis card | On `crisis` the client shows the resources card for `residence_country` and two buttons; "continue" sends `crisis.continue`, "stop" sends `crisis.stop`; no answer in 60 s is a stop (4.3) |
| Feed entry | The feed item's call link opens `/call/{episodeId}` which runs the same flow; the handoff time from link open to room joined is logged as `feed_to_call_ms` (PRD 16.2) |

### 4.12 The message and event protocol

**Client to worker (data channel, reliable, topic `forone.ctrl`, JSON `{v:1, t: client_ms, type, ...}`):**

| type | payload | effect |
|---|---|---|
| `hold.down` / `hold.up` | | floor held or released (4.5) |
| `talkback.down` / `talkback.up` | | talkback window (4.7) |
| `end_call` | | goodbye line then end |
| `crisis.continue` / `crisis.stop` | | after the crisis clips: resume the argument (host told to go on without referring to the crisis turn) or end the call (4.3) |
| `fact_card.edit` / `fact_card.remove` | `{card_id, value?}` | onboarding fact cards (talk path; the typed path sends them to `api`) |
| `client.hidden` / `client.visible` | | background handling |
| `planning.ready` | | logged; the pilot's call starts |
| `replay.host_line` | `{host_line_id}` | the worker re-plays the last host line from memory (4.6) and logs it |

**Worker to client (topic `forone.ui`):**

| type | payload |
|---|---|
| `state` | `{phase, turn: "host_speaking"|"listening"|"learner_speaking"|"floor_held"|"talkback"|"silent", t_s}` |
| `caption` | `{host_line_id, words?, text?, recast_span?, final}` |
| `talkback` | `{text_native, word_target, mode: "word"|"hint"|"none"}` |
| `retell_ring` | `{seconds}` |
| `fact_card` | `{card_id, field, value, quote}` |
| `crisis` | `{resources_ref, country}` (the client shows the resources card for `residence_country`, with continue and stop) |
| `fallback_required` | `{reason}` |
| `ended` | `{end_reason}` |

**Worker to `api` (`POST /internal/events`, batched, `Authorization: Bearer <per-call JWT>`):** event rows per PRD 8.2 with `learner_id, session_id, door: "call", type, occurred_at, payload, model_version, prompt_version, cost_usd, call_id, source: "worker"`.

```ts
type CallTurnPayload = {                               // event type call_turn (worker); the verbatim fields live on call_turn_verbatim (workflows), joined on (call_id, turn_index)
  turn_index: number; speaker: "learner"|"host"|"salma"; t_start_ms: number; t_end_ms: number;
  // learner
  streaming_text?: string; streaming_words?: {w: string; s: number; e: number; c: number}[]; streaming_vendor?: string;
  native_spans?: {s: number; e: number}[];             // native-language spans stripped from the host's text (4.4); the analyst masks them
  speech_ms?: number; pauses_ms?: number[]; backchannels?: {t_ms: number; clip_id: string}[]; cut_off?: boolean; repair_request?: boolean; media_id?: string;
  talkback_ms_excluded?: number; turn_confidence?: number;
  // host
  text?: string; moves?: object; allowances?: object; violations?: string[]; guard_hit?: boolean; truncated?: boolean;
  latency?: { stt_final_ms: number; preempted: boolean; first_token_ms: number; header_ms: number; header_tokens: number; guard_ms: number;
              tts_first_byte_ms: number; vendor_rtt_ms: number; reply_latency_ms: number; silence_to_sound_ms: number };   // every 4.15 stage, so the 50-call test can say which stage missed
  cache_read_tokens?: number; cache_creation_tokens?: number; output_tokens?: number;
  model?: string; fallback_used?: string|null; unsaid_text?: string|null; host_line_id?: string;
};
type CallMetrics = {                                   // calls.metrics, written at end
  connect_ms: number; first_sound_ms: number; first_sound_system_ms: number; turns_learner: number; turns_host: number;
  learner_speech_ms: number; host_speech_ms: number; host_talk_share: number;
  reply_latency_p50_ms: number; reply_latency_p95_ms: number; silence_to_sound_p50_ms: number; silence_to_sound_p95_ms: number;
  talkback_count: number; talkback_p50_ms: number; hold_count: number; hold_total_ms: number;
  silences_8s: number; cut_offs: number; barge_ins: number; preempted_turns: number; preempt_cancelled: number;
  anxiety_mode: null|"prior"|"last_call_abandoned"|"short_turns"|"two_silences";
  moves: {clarify: number; recasts: number; nudge: number; recall_gaps: number; retell: number; praise: number; pushback: number;
          violations: number; guard_hits: number; explicit_corrections: number; recast_off_target: number; clarify_on_clean_turn: number; wrong_memory: number;
          minima_unmet: string[]};
  native_detection: "on"|"off"; cache_miss_turns: number; truncated_turns: number;
  endpoint_ms_initial: number; endpoint_ms_final: number; vendors: {stt: string; llm: string; tts: string; fallbacks: string[]};
  cost_usd: number;
};
```

`explicit_corrections` is the count of guard hits on correction phrases (`guard/correction_words.yaml` per target language, 07) and feeds 09's `explicit_corrections_per_100_turns` (ceiling 0, ADR-06); `minima_unmet` and `violations` are the governor's two 50-call gates (4.13).

Events `hold_floor {t_ms, duration_ms}`, `silence {t_ms, duration_ms, offer_n}`, `talkback` (4.7.5), `replay_line {door: "call", host_line_id}`, `crisis_activation {t_ms, trigger: "header"|"keywords", role: "host"|"salma", language: "target"|"native", continued: boolean}`, `wrong_memory_flag {fact_id|null, learner_quote, turn_index, door: "call"}`, `call_started {kind, started_by, resumed_after_drop}`, `call_ended {end_reason, metrics, anxiety_mode, why_anxiety}`.

**Inngest events emitted by this domain:** `call.turn_audio_ready` (4.10), `call.ended {learner_id, call_id, session_id, kind, end_reason, voice_storage}`, `voicenote.received {learner_id, call_id, media_id, event_id}`, `pronunciation.requested {learner_id, media_id, reference_text, surface}`, `recording.turn_audio_ready` (same shape as the call one with `surface`), `onboarding.intake_completed`. `spool/ingest` (every minute) replays a spool file's events through `events.append()` and its end record through the `calls` update, then emits `call.turn_audio_ready` for the objects named in it.

### 4.13 The two vendor tests

**The 30-clip recognizer test (PRD 10.14, [P0]; the language gate's check 2, ADR-03; by 2026-11-10 during Milestone 0, ADR-07).** Input: 30 Milestone 0 learner clips with consent (the vendor-test consent addendum, 10-decision-records §10 item 13), 20 to 60 s each, with Muath's hand-tagged verbatim transcript and error tags; at least 6 clips containing a native-language code-switch, 6 containing a pause over 2 s, and 6 re-captured through Bluetooth earphones (the hands-free profile the beta will often hear). `vendor-lab recognizers --target en --clips m0/clips --tags m0/tags` (scripts on the vendor SDKs, no worker, no LiveKit) runs each clip through every candidate in both roles (streaming: Soniox, Deepgram; talkback: Soniox, AssemblyAI Universal realtime; verbatim: AssemblyAI, ElevenLabs Scribe) and reports per vendor:

| Metric | Definition | Pass line for the role |
|---|---|---|
| Error survival | share of hand-tagged learner errors whose surface form appears unchanged in the output | verbatim: at least 0.85; streaming: at least 0.70 [ASSUMPTION: 0.85 is the point below which 05's error profile needs a confidence discount on most turns; 0.70 because the streaming text only drives the host] |
| Filler retention | share of hand-tagged fillers kept | verbatim: at least 0.80 [ASSUMPTION: 05's fluency measures need most fillers] |
| Hallucination near pauses | inserted words within 1 s of a pause over 2 s, per clip | at most 0.1 per clip [ASSUMPTION: one invented word per 10 clips is below what the claim gate's quote check would catch] |
| Code-switch handling | native-language spans transcribed in the native language (not dropped, not transliterated into the target language) | talkback stream and host stream: at least 0.8 of spans [ASSUMPTION: the repair and crisis phrase match needs most spans, not all; the keyword list is also run on the talkback stream] |
| Talkback-ask resolution | a 20-ask fixture recorded by two M0 learners on their phones, half through AirPods, each with the expected lemma, scored as exact-lemma resolution through the full 4.7.1 path | at least 0.8 [ASSUMPTION; this is the whole talkback feature and Salma's intake, tested only indirectly in the first draft] |
| WER against the hand transcript | standard | reported, not gated |
| Confidence threshold | the per-word confidence below which error survival falls under 0.8, found by sweeping | becomes `packages/languages/<target>/recognizer.yaml: confidence_threshold` (PRD 10.2 step 4; PRD 18 #10 says it comes from data) |
| Streaming latency | final-after-end-of-speech, p50 and p95 | streaming: p95 under 500 ms [ASSUMPTION: the 4.15 budget has 400 ms for it at p95] |

Every pass line is a choice this document makes, tagged as such, because the PRD names only the metrics. If no vendor passes a line, the best one ships and the confidence threshold is raised so fewer edits feed claims; the gate record (`languages/en/gate.yaml`) says which lines were missed. The winner for each role goes into `vendors.yaml` keyed by target language; the loser is the secondary. Recognizer error by native language is tracked from these numbers onward (PRD 16.2) by rerunning the tool monthly on new consented clips.

**The 50-call latency test (PRD 14.4 #3, [P0]).** Three runs, each with its gates (the first draft scheduled the first run in week 4, which contradicted PRD 14.4 and 01 §7):

| Run | When | On what | Gates |
|---|---|---|---|
| Vendor-chain check (the gate's check 4) | Milestone 0, by 2026-11-17 | `vendor-lab call-chain`: STT final → Sonnet 5.5 first token and tokens/s → TTS first byte, scripted, from both candidate worker regions, no LiveKit | measured time-to-first-token and tokens/s for 4.15; TTS first byte under 300 ms at p95 (D8, handed to the blind test); `CALL_WORKER_REGION` chosen with 01 |
| #1 | build week 2, by 2026-12-01 | the minimal worker on staging (stock plugins, static brief, no governor, no talkback), both worker placements | `reply_latency_ms` median under 1.5 s, p95 under 2.5 s; `silence_to_sound_ms` p50 under 2.5 s and p95 under 4.0 s on completed sentences; connect under 3 s at p95; cache hit on every turn after the first |
| #2 | build week 4 (10-decision-records §7) | the full worker: governor, talkback, hold, patience, correction guard | all of #1 plus: `violations` under 5% of turns; `minima_unmet` on at most 10% of calls; `explicit_corrections` 0; host talk share at most 40%; cut-offs at most 1 per call; talkback p50 under 2 s on the two scripted S presses; no learner segment on any `lk.transcription` stream |
| #3 | build week 5, after prompt tuning, and on every later host prompt or vendor change | the release candidate | all of #2; the per-call cost from `vendor_calls` against section 6 |

`tools/call-bench calls --n 50 --script m0/scripted-calls` drives the staging worker by pushing Milestone 0 learner turns (audio files) into the `AgentSession` input in-process, following a script of 20 to 25 turns with realistic pauses (including mid-clause pauses of 1 to 2 s and two holds), and records per host turn every stage in `CallTurnPayload.latency`, so a missed gate names its stage. `connect_ms` over the real WebRTC path is measured separately by hand on two phones per run. [OPEN for Muath] which clock PRD 15 means: 01 adopted the end-of-turn decision as the gate and this document adds the learner-felt `silence_to_sound_ms` as a second gate; if the PRD means the learner-felt clock alone, the 1.5 s figure is not reachable with `p = 1.5 s` and PRD 5.4.4's patience and the two numbers have to be reconciled in PRD-v3. The tool keeps every run's report under `bench/reports/{date}-{git_sha}.json` (shared with 09) so a regression is visible.

### 4.14 Vendor adapters for the live path

The interfaces are the topology's (`StreamingRecognizer.livekit_plugin`, `StreamingSpeechSynth.livekit_plugin`, `VerbatimRecognizer.transcribe`, `Pronunciation.score`). This domain adds the roles and keys it needs:

```yaml
# packages/adapters/vendors.yaml (additions); roles that depend on the target language are keyed by it (ADR-03)
roles:
  streaming_stt:
    en: {vendor: soniox, secondary: deepgram, languages: [target, native], code_switch: true}   # native-language repair and crisis phrases on the open mic (4.4)
  talkback_stt:
    en: {vendor: soniox, secondary: assemblyai_realtime, languages: [native, target], code_switch: true}   # the secondary must cover the native language; Deepgram's code-switching does not cover Arabic
  talkback_resolver: {vendor: anthropic, model: claude-haiku-5-5, pricing: standard, request_shape: haiku}
  salma_live:     {vendor: anthropic, model: claude-sonnet-5-5, pricing: standard, fallback: {vendor: anthropic, model: claude-haiku-5-5, request_shape: haiku}}
  host:
    en: {vendor: anthropic, model: claude-sonnet-5-5, pricing: standard, request_shape: sonnet,
         fallback: [{vendor: anthropic, model: claude-haiku-5-5, request_shape: haiku}, {vendor: google, model: gemini-3.8-flash, request_shape: gemini}]}
call:
  endpoint_ms_default: 1500
  endpoint_ms_min: 1000
  endpoint_ms_max: 2500
  max_extend_ms: 1500               # for p < 1.5 s
  max_extend_ms_long_p: 1000        # for p >= 1.5 s (D3); both re-set from the week-1 "incomplete" rate
  retell_extend_ms: 2500
  nudge_extend_ms: 1000             # the self-repair window after a declared nudge
  preempt_silence_ms: 600           # D18
  preempt_eou_min: 0.8
  onboarding_endpoint_ms: 1800      # VAD plus fixed delay, no turn detector (4.9)
  backchannel_after_ms: 1200
  backchannel_after_ms_anxiety: 1000
  filler_after_ms: 1200             # THINKING with no host audio
  silence_offer_ms: 8000
  interruption_min_ms: 500
  interruption_min_words: 2
  hold_release_grace_ms: 300
  talkback_preroll_ms: 400
  talkback_resolver_timeout_ms: 1500
  talkback_wait_clip_at_ms: 700
  llm_first_token_timeout_ms: 1200
  llm_retry_timeout_ms: 1500
  llm_max_tokens: 200
  hidden_abandon_s: 10
  crisis_answer_timeout_s: 60
  limits: {first: {close_begin_s: 60, hard_end_s: 90}, main: {close_begin_s: 390, hard_end_s: 480}, round_two: {close_begin_s: 120, hard_end_s: 180}}
  retell_window_start_s: 120        # [ASSUMPTION], 4.3
  tts_stream_tfb_gate_ms: 300       # D8: a call TTS vendor must beat this at p95 in the vendor-chain check and the 50-call test
  worker: {calls_per_task: 8, min_tasks: 2, max_tasks: 2}   # fixed 2 tasks for the beta (about 16 concurrent calls, 01 §7); autoscaling is P1
```

`request_shape` selects the per-model request builder in 4.4. `min_tasks: 2` because with one warm task of 8 calls the ninth concurrent call would wait minutes for a Fargate task to start, which is a connect-budget failure at the beta's stated peak of 15; two fixed tasks cost about $70 a month more and remove autoscaling from the build.

Each TTS vendor's live plugin is configured with the casting's `voice_id`, `rate` (vendor rate control where supported; otherwise the host simply speaks at the voice's natural rate on the call, because resampling live audio costs latency), PCM 24 kHz output, and sentence-level chunking. Vendor-specific notes to verify in week 1: ElevenLabs streaming (Flash model, websocket with alignment) gives word timings; Cartesia gives them; Inworld's streaming timestamps and Gemini TTS's streaming first-byte latency are unverified (voice lens) and are measured by `call-bench` before the blind test is run (D8).

### 4.15 Latency budget, host reply (PRD 15)

`reply_latency_ms` is measured from the end-of-turn decision (01 §3.6 adopted this clock as the PRD 15 gate). The silence window `p` is the learner's and is pedagogy, not latency, but the number the learner feels is `silence_to_sound_ms` (last speech frame to first host audio), which has its own gate in 4.13 (p50 under 2.5 s, p95 under 4.0 s on completed sentences). The first draft's table summed to "about 950 ms" by counting a 60-token header as 120 ms (330 tokens/s) and by leaving out the vendor round trips 01 counts; this table carries list figures (the lenses and 01 §3.6) until the vendor-chain check (4.13) replaces them with measured Sonnet 5.5 time-to-first-token and tokens/s, which the build-week-2 run then confirms on the worker.

| Stage | Budget p50 | Budget p95 | How it is held |
|---|---|---|---|
| STT final after end-of-turn | 150 ms | 400 ms | streaming partials are already in hand; only the final is awaited |
| Operator note, guard of the learner text and request build | 10 ms | 20 ms | no I/O |
| Host first token | 350 to 500 ms | 700 ms | cached prefix (A and B), `effort: low`, no thinking, `max_tokens: 200`; **preemptive generation (D18) starts the request about 600 ms before the endpoint on turns the detector judges complete, so on those turns this row is mostly hidden inside `p`** |
| `@m` header parsed | 100 to 200 ms | 250 ms | 8 to 15 tokens at 60 to 90 tokens/s (measured as `header_ms`); the first draft's JSON header was 650 to 1,000 ms here |
| Correction guard on sentence 1 | under 20 ms | 20 ms | `guard.check_output`, in process (07) |
| TTS first byte for sentence 1 | 200 ms | 400 ms | websocket pre-opened at job start; sentence flush on the first `.?!` or 12 words; D8 gate 300 ms at p95 |
| Vendor round trips (STT, LLM, TTS) | 3 × 40 to 60 ms = 150 ms | 300 ms | `call-worker` runs in `CALL_WORKER_REGION`, next to the vendors' endpoints (01 §3.6); from a region far from them 01 counts 400 to 550 ms, which alone eats the margin |
| LiveKit and network to the phone | 120 ms | 250 ms | LiveKit edge; Opus 20 ms frames |
| **Total without preemption** | **about 1.3 to 1.6 s** | **about 2.3 s** | at the gate, not under it: the 1.5 s median depends on the sparse header and the region placement, and the governor's re-request (about 600 ms on under 5% of turns) is what the p95 margin pays for |
| **Total with preemption** (turns judged complete at 600 ms) | **about 0.9 to 1.2 s** | **about 1.9 s** | the model's first token and most of the header arrive during the learner's own silence; expected on the majority of turns, measured as `preempted_turns` |

Honestly stated: without preemptive generation and the sparse header this design does not meet the median gate; with them it meets it with 200 to 400 ms to spare at p50. `silence_to_sound_ms` on a completed sentence is `p` plus the total above: about 2.4 to 2.9 s with `p = 1.5 s` and no preemption, 2.0 to 2.5 s with it; when the detector judges a finished sentence unfinished the turn waits up to `p + max_extend` (now capped at 1.0 s for `p >= 1.5`), which is why the week-1 "incomplete" rate measurement decides whether the detector is used at all.

Connect: `POST /v1/calls` 100 ms (key derivation and JWT minting are in-process), room join 500 to 1,500 ms, job accept under 500 ms on a warm task, bundle fetch under 100 ms, opening clip plays at track subscription: under 2.5 s typical, under 3 s at p95 with two warm worker tasks per environment. Onboarding's first-sound budget is laid out in 4.9.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detected by | Behaviour | Learner sees | Evidence |
|---|---|---|---|---|
| Room not joined within 3 s, or two pipeline errors in one call, or ICE disconnected over 5 s | client timers; worker error count | **Voice-note fallback (5.1)** | "Weak signal. Let's do voice notes." then the same argument in voice notes | thread continues; `end_reason: fallback` |
| Streaming STT vendor error or no partial for 3 s while speech is detected | worker | reopen the stream on the secondary vendor (`vendor_config`), re-feed the last 2 s from the pre-roll buffer; second failure in the call triggers fallback | nothing, or one lost half-turn | `vendors.fallbacks` |
| Host LLM slow (first token over 1.2 s) or error | worker | retry 1.5 s; then Haiku 5.5 in its own request shape; then the second vendor (4.4) | a slightly longer pause, filled by one filler clip at 1.2 s in `THINKING` (4.3) | `fallback_used` on the turn |
| Call TTS error or first byte over 1.5 s | worker | the sentence is retried on the understudy voice and vendor from `voice.understudy`; the switch is announced on air by the pipeline next episode (PRD 7.1 rule 3) | a voice change mid-call, once; rare | `vendors.fallbacks`, `vendor.degraded` |
| Both voice vendors down | `vendor/health` | fallback to voice notes with text replies from the host (no audio) for the rest of the day | text bubbles instead of voice | logged; PRD 15 "second vendor the same day" is met by the understudy path above |
| Salma TTS down | worker | talkback answers as text in the bubble only | word appears, no voice | `talkback.mode` unchanged |
| Talkback resolver timeout (1.5 s) | worker | the wait clip played at 700 ms; on timeout Salma's native package clip "say it again, slower" plays; ask logged as unresolved | a pause, then the ask | `resolved_by: none` |
| Host-stream recognizer on the secondary (Deepgram) | worker | the call continues; native-language repair and crisis phrases on the open mic are not detectable (4.4); the talkback stream still catches them while S is held | nothing | `native_detection: off` on `call_ended`; counted for counsel |
| Both recognizers that cover the native language down (Soniox and AssemblyAI realtime) | `vendor/health` | talkback degrades to the typed ask over the data channel (`talkback.text {text_native}`, answered by the same resolver as text); onboarding A3 runs typed through `api` (01) | a text box instead of the S button | `vendors.fallbacks` |
| `api` unreachable | worker | events, `vendor_calls` rows, `turn_audio_ready` and the end record spooled to `forone-voice/spool/{callId}.ndjson` (SSE-KMS under the environment key); `spool/ingest` polls the prefix every minute and replays them; audio uploads go straight to S3 and are unaffected; **because no `media_objects` row and no Inngest event exist for the spooled turns, the worker itself deletes the call's `ephemeral/` objects at call end + 14 min when storage is off** (4.10), so the 15-minute rule holds in this failure mode (the first draft's daily ingestion would have let the audio live up to 24 h) | nothing | delayed events; the after-session pass may run late; `privacy/verify` checks the case |
| Postgres down | `api` | `POST /v1/calls` fails: the client offers voice notes at once (they also need `api`, so it queues them in IndexedDB and shows "will send when back") | "Weak signal" | queued |
| Worker task dies mid-call | LiveKit job failure, client sees agent leave | client offers a fresh call (4.3 `resumed_after_drop`) or voice notes | "Lost you. Call again?" | partial turns already uploaded |
| LiveKit Cloud down | client connect failure | voice notes | | |
| Verbatim vendor down | `call/verbatim-turn` retries exhaust | secondary vendor; if both fail within 15 min and storage is off, the audio is deleted and the turn is `verbatim_failed`: planning signals only, no claims | notes may show fewer cards | PRD 5.4.11 honoured |
| Learner backgrounds the app | `client.hidden` | end after 10 s as `abandoned`; a fresh call later | | counted in "abandoned on the move" |
| Learner says they are driving | package phrase list on the streaming final, and the host's `goodbye` | "Call me back when you've parked." and end | | `end_reason: driving` |
| Crisis | host header or keyword list (target or native language, host stream or talkback stream) | CRISIS state (D15, 4.3): package clips in the target then the native language, resources card for `residence_country`, `crisis_activation` logged; `crisis.continue` resumes the argument with the host told to go on and never refer to the crisis turn (the turn is quarantined per 07 D9), a second activation ends the call; `crisis.stop` or 60 s without an answer ends it as `end_reason: crisis` | the card with continue and stop | SB 243 log; `continued` on the event |
| Host move violation twice | governor | spoken anyway, logged | | quality metric |
| Correction guard hit twice | `guard.check_output` | the package filler line replaces the sentence; an explicit correction is never spoken | one bland line | `explicit_corrections` |
| Hard end reached during a host sentence | timer | end after the current TTS sentence, then the goodbye line | a short goodbye | `timeout_8m` |
| Hard end reached during a learner turn | timer | wait for the turn to end (bounded by `p + max_extend`), then the goodbye line; the learner is never cut (law 7) | the host waits, then says goodbye | `timeout_8m` |
| Worker task draining for a deploy (01 §4.4 #7, ADR-16) | drain signal | no new jobs; calls in progress run to their natural end; a call still live at the drain deadline gets the goodbye line | a short goodbye | `end_reason: drained`; counts as not done for the door rule |
| Cost runaway (a call over 12 minutes of vendor time, which cannot happen under the timers but could under a bug) | worker watchdog | end the job | | paged |

### 5.1 The voice-note fallback in detail

1. The client ends the live attempt, shows the line, and records a note (`MediaRecorder`, at most 90 s) with a single large button; sending uploads to `POST /v1/calls/{id}/voicenotes {media, duration_ms}`; `api` writes `media_objects {kind: voice_note}`, a `call_turn` event with `mode: voice_notes`, flips `calls.mode = voice_notes`, and emits `voicenote.received`.
2. `call/voice-note-reply` (Inngest, concurrency 1 per call): verbatim transcription of the note (the same adapter; this transcript is both the streaming and the verbatim text for this turn); the host LLM with the same system layers A and B and the thread so far, the operator note `mode=voice_notes` (no backchannels, no silence offers; the move contract and the correction guard still apply with the same counters, carried in `calls.metrics`); call TTS of the reply (non-streaming, the same voice); the reply audio is stored as a host `call_turn` with `media_id` and pushed to the thread; the client plays it. Each exchange takes 20 to 40 s.
3. Talkback in this mode is a text ask to Salma in the thread (`POST /v1/calls/{id}/talkback {text_native}`) answered by the same resolver, as text.
4. The thread closes when the learner taps "done" or at the session's close; the after-session pass treats voice-note turns like call turns (lower weight for fluency because the learner could re-record, flagged `mode: voice_notes`).
5. A call that started live and fell back keeps one `calls` row; its live turns and note turns are one thread in order.

---

## 6. Cost and performance against the budgets

Estimates from list prices on 2026-10-09 (voice and AI-architecture lenses, the API reference for Anthropic models); measured cost replaces them from the first call through `vendor_calls`. Assumptions: a 6:30 main call, 25 learner turns averaging 9 s of speech, host share 35% (2.3 min, about 340 words, 1,900 characters), 3 talkback asks, cache warm.

| Item | Vendor and unit | Estimate per main call |
|---|---|---|
| Streaming STT, host stream | Soniox $0.002/min × 7 min | $0.014 |
| Streaming STT, talkback stream | Soniox, open for the call but billed on frames sent, about 0.5 min of audio (vendor idle-connection terms to confirm; worst case 7 min, $0.014) | $0.001 to $0.014 |
| Host LLM input | Sonnet 5.5: cached reads about 90k tokens over 25 turns × $0.20/M = $0.018; cache writes about 4k new tokens × $2.50/M = $0.010; uncached about 3k × $2/M = $0.006 | $0.034 |
| Host LLM output | 25 turns × about 45 tokens (sparse header 8 to 15 plus 30 to 35 of text) = 1.1k × $10/M (the first draft's JSON header made this about 90 tokens a turn, $0.022) | $0.011 |
| Governor re-requests and preemption cancels | 1 re-request per call on average plus 3 to 5 cancelled preemptive requests, cached input | $0.004 |
| Call TTS | Inworld TTS-2 Flash $15/M chars → $0.029; ElevenLabs Flash v2.5 $40/M → $0.076; Gemini 3.8 Flash TTS $9/M audio tokens × 3,500 tokens → $0.032 (doubling 2027-01-01) | $0.03 to $0.08 |
| Talkback resolver | Haiku 5.5, 3 × 600 input + 60 output tokens | $0.001 |
| Salma TTS | 3 × 40 native-language characters | under $0.005 |
| Backchannels, opening line | pre-rendered | $0 live (about $0.002 at episode time for the opening line) |
| LiveKit Cloud | 2 participants × 7 min at the Ship plan's per-minute rate | about $0.01 to $0.02 [ASSUMPTION; the topology flags this rate for verification] |
| Compute | 1/8 of a Fargate task (2 vCPU, 4 GB) for 8 min | about $0.004 |
| **Live call total** | | **$0.11 to $0.17** (Inworld or Gemini about $0.11 to $0.12; ElevenLabs about $0.16 to $0.17) |
| Verbatim re-transcription | AssemblyAI, 7 min of learner audio at about $0.004/min (the lens range is $0.002 to $0.017) | $0.03 at the top of the range |
| Pronunciation | Speechace $0.008 per 15 s, one say-it-once | $0.008 |
| Round two [P1] | the same pipeline at 2.5 min, no talkback | about $0.05 |
| Onboarding Salma + first call | about 4.5 min of Salma and host time; charged to the learner's first session once | about $0.10 |

Against PRD 14.5: "Call (main and round two) $0.16" comes out at about $0.16 to $0.17 with Inworld or Gemini ($0.11 to $0.12 live plus about $0.05 for round two) and $0.21 to $0.22 with ElevenLabs on the call; the first draft's "$0.14 to $0.16" did not follow from its own table. So the line is met only at the bottom of the estimate, with the shorter-host-turn lever applied or with the Haiku host; this is carried into 08's day-one levers and into 10-decision-records §10 items 5 and 6. "Re-transcription and pronunciation $0.03" holds at about $0.035. The ElevenLabs case is the one that breaks the line, which is why D8 ties the call vendor to the episode vendor and why the blind test's "cheapest voice that passes" rule (PRD 14.5) matters here as much as for episodes. Levers in order if the measured number is high: shorter host turns (every 10% of host talk removed is 10% of TTS cost and more learner speech; the governor's `shorter` lever already exists for the talk-share rule); Haiku 5.5 as host if the 50-call test's move-contract score holds (saves about $0.03 a call); Inworld as the call voice with ElevenLabs as the episode voice only if a blind test says listeners cannot tell on a 6-minute call (gives up D8, needs the on-air announcement). The scale target of $0.30 to $0.35 per session needs the call at about $0.08: Haiku host, Inworld or Gemini voice, and 5-minute calls, all of which are configuration in this design. With the `one_a_day`, `two_a_day` and `three_a_day` plans (ADR-04) the call cost is per episode, so a learner on three a day who uses the allowance costs three calls; 08's "Margin by plan" reads the measured figure.

Performance: section 4.15 for latency; capacity is 8 calls per task [ASSUMPTION from the topology, measured in the week-5 load test], 2 fixed tasks per environment (about 16 concurrent calls; the beta's peak of 15 fits), autoscaling in P1. The vendor concurrency limits (Soniox, AssemblyAI realtime and the TTS vendor's concurrent streams) and the Anthropic tier (about 60 host requests a minute at peak, mostly cached reads) are the real ceiling and are requested during Milestone 0 for 50 concurrent streams, tied to the vendor contracts date in 10-decision-records §10 item 9.

---

## 7. Build plan for 2026-11-18 to 2026-12-22

This plan is written against 01 §7's E2 column (two engineers: E1 backend, E2 web and call), re-dated by ADR-07, and it carries the cross-domain items 10-decision-records §7 places in this domain. The first draft needed one engineer full time on the call for all five weeks, built a production worker skeleton in week 1 for a test that needs no LiveKit, and ran the 50-call test in week 4; this plan does the vendor tests during Milestone 0 as scripts, stands up a minimal worker in week 2 for the 50 calls, and moves everything the beta can live without to P1. The skeptic review's cut list is adopted in full.

| Week | Dates | Ships (E2's call half, plus E1 where named) | Priority | What the Milestone 0 data lets you test |
|---|---|---|---|---|
| 0 (Milestone 0, in parallel) | 2026-11-01 to 11-17 | `vendor-lab recognizers --target en` on the 30 clips (plus the Bluetooth clips and the 20-ask talkback fixture) by 11-10, the confidence threshold written into `packages/languages/en/recognizer.yaml`; `vendor-lab call-chain` from both candidate worker regions (STT final, Sonnet 5.5 time-to-first-token and tokens/s, TTS first byte; the D8 gate handed to the blind test) by 11-17; `vendors.yaml` committed with the winners and the Arabic-capable talkback secondary by 11-17 (ADR-03, ADR-07); the vendor concurrency and Anthropic tier requests sent | P0 | The 30 consented clips and Muath's tags are the test set; the talkback fixture is recorded by two M0 learners |
| 1 | 2026-11-18 to 11-24 | LiveKit Agents quickstart locally with the SDK version pinned and every option name in this document verified (`SDK-NOTES.md`: manual turn mode, audio turn detector and its language list, preemptive generation, second audio track, disabling transcription output, `clear_at` on operator notes); the 30-line cache probe through the Anthropic plugin (`cache_read_input_tokens` per turn) and the decision on the thin `llm.LLM` subclass; the turn detector's "incomplete" rate on the M0 learner transcripts (sets `max_extend` and whether the detector is used); the recast emphasis markup checked by ear per TTS vendor; E1: `learners.{native_language,target_language,residence_country,tz}`, the two package directories (`languages/en`, `native/ar`, `native/en`), `events` append-only with `call_turn_verbatim`, the per-call HKDF key and JWT in `POST /v1/calls`, `media_objects.key_derivation` and `encryption`, the worker's `vendor_calls` S3 spool (ADR-13) | P0 | M0 call transcripts replayed through the turn detector |
| 2 | 2026-11-25 to 12-01 | **Minimal `call-worker` on staging** (stock plugins, a static hand-written `CallBundle`, the sparse `@m` header parsed but not governed, no talkback, no recorder), with drain mode and scale-in protection from the start (01); `tools/call-bench calls` v0 by in-process audio injection; **50-call run #1 by 2026-12-01 in both worker placements** (`reply_latency_ms`, `silence_to_sound_ms`, connect, cache hit; `CALL_WORKER_REGION` chosen with 01); the per-model request builders and their 20-line fixture test; host prompt layers A and B from M0 prompt H plus the bible drafts, with the no-correction language | P0 | M0 scripted calls are the caller's voice |
| 3 | 2026-12-02 to 12-08 | Onboarding A3 talk path on the minimal worker (static intro clips from `native/ar`, VAD plus fixed delay, fact cards, `onboarding.intake_completed` with `name_clip_text`, the `hold_until_consumed` name clip); the typed path through `api` is E1's (01); kind `first` with its budgets and the talkback intro clip; sentence captions over the data channel; the client audio contract (4.11) in `web` with the client domain; the backchannel, filler, turn-signal and gap clips rendered per host voice through `voice-studio.render` on first use | P0 | A3 transcripts from M0 intakes become the onboarding fixture set |
| 4 | 2026-12-09 to 12-15 | The governor with budgets, minima, `tick`, the re-request and `minima_unmet`; **the correction guard in the worker path (ADR-06, 10-decision-records §7)**; the operator notes; per-turn recorder and upload under the per-call key to the `ephemeral/` or stored prefix, `call.turn_audio_ready`, `call/verbatim-turn` appending `call_turn_verbatim`, the worker's local deletion duty and `spool/ingest`; talkback with the Haiku resolver, word-or-hint, the wait clip and the **`talkback_stt` language hint per learner (ADR-02)**; hold-to-talk; adaptive patience from the pause profile with the cut-off counter; preemptive generation; silence offers; anxiety mode with all three triggers; timers, goodbyes and the hard-end wait; `resumed_after_drop` under the door rule; repair phrases in both languages; wrong-memory handling; `calls.metrics`; **50-call run #2 with the full gates (10-decision-records §7)**; per-call cost visible in `vendor_calls` | P0 | M0's evidence on call timing sets the first `p` distribution and the retell window start |
| 5 | 2026-12-16 to 12-22 | Voice-note fallback end to end (`call/voice-note-reply`); **crisis protocol with the clips per pair and the resources per country (ADR-20)**, the continue and stop path, the keyword lists on both streams; `audio/expire` and `learner/purge-audio` wiring and deletion verification with the security domain, including the `api`-down case; pronunciation on say-it-once (`call/pronunciation-score`); recordings route for the first then-and-now and the small door; load test at 15 concurrent calls on the 2 fixed tasks; 50-call run #3 after prompt tuning; end-to-end with Milestone 0 learners on staging under a consent that covers it; runbook for `/admin/vendors` failover; the exit document's measured cost per call | P0 | The M0 learners' real calls on the real pipeline are the exit evidence: measured cost per call and the latency gates |
| P1 | from 2026-12-23 (beta) to 2027-01-26 | Round two (kind `round_two`, available after the main call, suggested from Today); shadow lines with pronunciation; word-level captions from vendor word timings; the second Salma audio track with the "closer" mix (the beta plays Salma on the `host` track and shows the bubble); the headphone-button mappings; the retell ring; `calls.metrics` percentiles beyond reply latency and silence-to-sound; worker autoscaling (the beta runs 2 fixed tasks); the understudy-voice mid-call switch (the beta ends the call and falls back to voice notes); the dial-in experiment (LiveKit SIP ingress, 8 kHz flag `low_confidence`, no talkback, no claims); the observer slot test behind a flag; the simulated-caller half of the offline suite (PRD 6.7) built on `call-bench`; `call-bench` as a CI job; the secondary recognizers exercised weekly by a canary call | P1 | |

**Freezes:** 2026-12-21 12:00 to 12-24 12:00 UTC and 2026-12-31 to 2027-01-02 (ADR-07); `call-worker` deploys drain and run at any hour the release tool's window check allows (ADR-16).

**What ships after 2026-12-22, stated plainly (PRD 5.4 rules affected):** the two-track Salma mix (PRD 7.3's "closer" voice is approximated by the level and EQ treatment on the shared track); word-level captions (PRD 5.4.8 is met with sentence captions and the bold recast word); the retell ring (PRD 5.4.6's retell runs without the visual ring; the host's line carries the "sixty seconds"); round two (PRD 5.4.9, already P1); the reverse gloss index (cut outright, D6); in-call `p` adaptation stays in P0 because it is one counter; the driving-phrase path stays in P0 because it is a phrase list and one `goodbye`. Do not cut: per-turn upload and verbatim (the after-session pass and the deletion window depend on it), the governor (law 7), the correction guard (ADR-06), hold-to-talk (the one feature Duolingo's own research says users demanded), the voice-note fallback (PRD 15), the three 50-call runs (PRD 14.4).

---

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Speech-to-speech (OpenAI gpt-realtime, Gemini 3.8 Live, Nova Sonic) | No custom voice, so the host does not sound like the episode; input transcripts are approximate (the assessment domain needs the exact streaming text and the verbatim pass); per-turn re-billing makes cost follow turn count; patience is one setting per call |
| Pipecat instead of LiveKit Agents | Smart Turn is designed for English; LiveKit's audio turn detector lists Arabic and other native languages (its text model does not, which is why D1 uses the audio one); the topology already runs LiveKit Cloud |
| LiveKit's built-in endpointing (`turn_handling.min_delay`/`max_delay`) as the decider | Two owners of end-of-turn; hold-to-talk, the backchannel at 1.2 s, the retell and nudge extensions and in-call `p` changes cannot be expressed through it; manual mode with `commit_user_turn()` costs the same to build and has one owner |
| The full JSON `@moves` header (first draft) | 55 to 70 tokens at 60 to 90 tokens/s is 0.6 to 1.0 s of first audio; the sparse `@m` header carries the same information in 8 to 15 tokens |
| The learner DEK in the bundle (first draft) | The most exposed service would hold the key to every recording; the per-call HKDF key costs one line and reads re-derive it (01 D7, 07 D2) |
| Replaying the host's last line from a client-side buffer (first draft) | Capturing a remote WebRTC track into a buffer on iOS Safari is unreliable; the worker already has the PCM |
| Opening the talkback stream on S-down (first draft) | 200 to 500 ms of websocket setup inside a 1 to 2 s hold; the always-open stream costs about $0.013 a call |
| Ending the call on every crisis activation (first draft) | PRD 7.9.2 says the session continues only if the learner chooses, so a "continue" path has to exist |
| Salma's correction notes as the correction channel (PRD-v2 5.5) | Removed by decisions.md §3 and ADR-06; the recast inside the conversation is the only correction channel, and the correction guard enforces it in code |
| ElevenLabs Agents (the Milestone 0 call) | Hosted convenience, but the voice differs from the episode, the turn-taking is a global setting, the brief is pasted by hand, and the transcript smooths learner errors; right for a no-code pilot, wrong for the product |
| Whole-reply structured output (JSON with `moves` and `text`) | First audio waits for the JSON to close; the header line streams the same information in 100 to 200 ms |
| A separate observer model in the beta | PRD 17 excludes it; the brief already lists recasts and gaps; the slot is reserved (D14) |
| Backchannels generated by the host model | A model round trip inside the learner's pause is the latency the backchannel exists to hide |
| One recognizer stream for talkback and the host | Code-switch errors would leak the native language into the host's input and into the error profile; the S button makes routing exact (PRD 0.1 row 7). The host stream still runs with both languages for phrase detection, but its native-language spans are stripped by code before the host sees them (4.4) |
| Transcribing the whole call after it ends | The after-session pass would wait for a 7-minute file; the 15-minute deletion would race the transcription |
| Live `p` learned by a model | No model for L2 pauses exists (voice lens); 04's formula plus the cut-off counter with an explicit direction is honest and cheap |
| P90 of within-turn pauses as the pause-profile formula (first draft) | A censored distribution: nothing longer than the endpoint is ever observed, so the profile could only ratchet down toward 1.0 s |
| Motion sensors for "abandoned on the move" (first draft) | An iOS permission prompt and sensing about the person that trust promise 6 does not cover; `end_reason` plus `started_by` answers the PRD measure |
| Dial-in as the P0 hands-free answer | 8 kHz audio, no talkback, no pronunciation; PRD makes it a P1 experiment |
| Client-side recording of the whole call (MediaRecorder) as the evidence source | Browser recording of a WebRTC call is unreliable on iOS; the worker already has the decoded frames |
| Opus-class host | Latency and cost; the host's job is short turns from a brief, not reasoning |
| Haiku-class host by default | Unproven on the recast moves; kept as the measured fallback and the scale lever |

---

## 9. Assumptions about other domains

1. **System topology.** `call-worker` on Fargate in `CALL_WORKER_REGION` with LiveKit Cloud, `POST /v1/calls` (minting the per-call key `HKDF(DEK, "call:" + call_id)` and the per-call JWT, 5-minute TTL, audience `call-worker`), `GET /internal/calls/{id}/brief`, `POST /internal/events`, `POST /internal/calls/{id}/turns`, room naming `call-{callId}`, dispatch metadata `{callId, jwt}`, the `calls` table, `audio/expire`, `learner/purge-audio`, `vendor/health`, `/admin/vendors`, `POST /v1/onboarding/{id}/messages` for typed onboarding and `HOME_REGION = eu-central-1` by default (ADR-08) exist as the topology describes. Asks of 01: `POST /v1/calls` takes a `clientKey` and is idempotent for 60 s; `GET /v1/calls/{id}/token` refreshes the participant token; the door rule in 4.1 (an abandoned, dropped, drained or failed main call with under 120 s of speech is not "done"); `calls.end_reason` gains `drained`; a `spool/ingest` cron every minute replaces `retention/daily` for the worker's spool. Deviations recorded here: the host's fallback chain is Haiku 5.5 first, then Gemini 3.8 Flash (the topology lists Gemini only); `calls` gains `metrics` and `bundle_version`; the `CallBundle` is compiled at `POST /v1/calls` (not only at episode time) so notebook vetoes are honoured; the end record travels on `/turns` with `kind: end` rather than a separate `/end` route; the worker publishes two audio tracks (one in the beta, section 7); `min_tasks` is 2, not 1.
2. **Episode generation pipeline.** `CallBrief` has the fields in 02-generation-pipeline.md 4.4 and its recast list is the teacher's echo plan (ADR-06); `voice-studio.render(RenderJob)` is callable from the worker and from the brief compiler, which is how this domain renders the backchannel, filler, turn-signal and gap clips per host voice (owned here, 4.5) and the per-episode opening-line clip at publish (D11; an ask of 02's `episode/produce` publish step, needed by build week 3); the blind test admits only vendors that pass the streaming first-byte gate (D8), and `voice_casting.hosts.*.understudy` is the failover voice; the name-pronunciation step reads the name clip inside the 15-minute `hold_until_consumed` window or works from `name_clip_text`. The first draft's reverse gloss index ar→en is withdrawn (D6).
3. **Learner model, event log and data platform.** `events` is append-only; the verbatim result is the second event `call_turn_verbatim` appended by `workflows` and joined on `(call_id, turn_index)` (04 D2, ADR-19); `skills.pause_profile.eot_silence_ms` is computed by 04's formula (04 §4.3.4), and this domain asks 04 to read `cut_offs` as an upward signal and the held-floor and pre-endpoint `pauses_ms[]` as the only downward one (4.5); the anxiety prior and `last_call_abandoned` are in the bundle; the Word bank exposes the produced-lemma set for the talkback brief; `media_objects` has `ephemeral`, `expires_at`, `deleted_at`, `key_derivation`, `encryption`, `hold_until_consumed`; `wrong_memory_flag` is handled by the memory keeper; `word_uses` is written by 05, never by the worker.
4. **Assessment engine.** `session/after-pass` is one function with the 10-minute budget (ADR-06; no 90-second notes stage) and waits for `verbatim.turn_completed` of the last turn, not for a whole-call transcript; it masks `native_spans` and reads `talkback_ms_excluded` when computing fluency; the recognizer confidence threshold is read from `packages/languages/<target>/recognizer.yaml` where `vendor-lab` writes it; voice-note turns are weighted down for fluency; `anxiety_mode` on `call_ended` is read for weighting; dial-in turns carry `low_confidence` and never feed claims; the first "then" recording arrives through `/v1/recordings` with task ids.
5. **Client app and delivery.** The call screen implements 4.11 and 4.12 (including `crisis.continue`/`crisis.stop`, the `clientKey`, the token refresh and `replay.host_line` as a message only, no client-side audio buffer and no 150 ms mute); the planning card, the earphones suggestion, the captions switch, the "keep this recording" control, the crisis resources card per `residence_country` and the Today-screen round-two suggestion are client surfaces; the feed item's call link opens `/call/{episodeId}`; typed onboarding renders fact cards from `api`'s responses; no DeviceMotion permission is requested.
6. **Security, privacy, consent and compliance.** `api` derives the per-call key and the worker never sees the DEK (07 D2, `keys.get_dek` with the 60 s versioned cache, ADR-18); SSE-C uploads from the worker under `encryption = 'sse_c_learner'` are approved (ADR-12); `guard.check_output(role, text)` includes the correction guard with `guard/correction_words.yaml` per target language and runs before every TTS sentence and Salma line (ADR-06); the crisis keyword lists exist per target and native language and the resources per ISO country (ADR-20); `privacy/verify` checks the worker's local-deletion case hourly (ADR-16); LiveKit Cloud, Soniox, Deepgram, AssemblyAI (realtime and verbatim) or ElevenLabs, Speechace or Microsoft, and the TTS vendors are approved processors for audio in transit (and, for the verbatim vendor, at rest for the minutes of transcription), or replacements are named; the regime table (07 §4.9) covers the beta's residence countries; the consent flag's semantics at `call.ended` are as in 4.10; `forone.core.costguard` caps call starts per learner-day at 6 × `episodes_per_day` (ADR-15) and pre-account starts at one an hour.
7. **Cost model, vendor strategy and tracing.** Every adapter call from the worker writes a `vendor_calls` row through the shared middleware with `call_id`, appended to the worker's S3 spool per turn and reconciled hourly (ADR-13); `prices.yaml` carries the per-minute, per-character and per-token rates used in section 6 and the 2027-01-01 Gemini row; Langfuse spans carry `call_id` and `turn_index` and metadata only unless `data_use` (ADR-09); the vendor contracts list carries the Anthropic tier check; "Margin by plan" reads the measured call cost per episode (ADR-04, ADR-15).
8. **Evaluation, observability and operations.** `calls.metrics` and the `call-bench` reports under `bench/reports/` are the inputs for the latency, silence-to-sound, talk-share, violation, `minima_unmet`, `explicit_corrections_per_100_turns` and talkback dashboards; the "calls abandoned on the move" and "feed-to-call handoff" measures are computed from `end_reason: abandoned` plus `started_by` and `feed_to_call_ms`; the weekly canary call per voice vendor and per host request shape is scheduled by operations at any hour the release window allows (ADR-16); staging stays up from build week 2.

---

## 10. Open for Muath

1. **[OPEN for Muath] The call-voice gate on the episode vendor (D8).** If the blind test's favourite voice (ElevenLabs is the likeliest, voice lens) is the only one that passes naturalness but its streaming price puts the call line at about $0.22 instead of $0.16, choose: keep sameness and accept about $0.06 more per session in the beta, or let the call use the runner-up vendor's closest voice with an on-air announcement, as Milestone 0 did. The M0 day-7 check-in ("does the different call voice bother you?") is the evidence; decide by 2026-11-17, when `vendors.yaml` is committed (ADR-07). The voice contract and the January plan are 10-decision-records §10 item 5.
2. **[OPEN for Muath] Salma's variety and voice vendor per native language** (PRD 18 #6, ADR-02). The talkback and onboarding pipeline is variety-agnostic; for `native/ar` the blind test (5 native listeners of the variety, from anywhere) needs to run by 2026-11-17 so the static intro, wait and talkback clips can be rendered in build week 3; `native/en` needs the same decision only if an English-native learner who is learning another target language joins the beta, which the English-only gate makes unlikely before 2027.
3. **Vendor contracts for concurrency and the Anthropic tier:** see 10-decision-records §10 item 9 (vendor minimums); this domain's specific need is 50 concurrent streams on Soniox, AssemblyAI realtime and the TTS vendor(s) before 2026-12-23, and the Anthropic tier for about 60 host requests a minute.
4. **Crisis protocol lines and resources:** see 10-decision-records §10 item 12. Specific to this domain and added here: whether native-language crisis detection on the open mic may be off while the host stream runs on its secondary recognizer (4.4; the talkback stream still catches it), and whether a `crisis.continue` after the clips is acceptable to counsel as written in 4.3.
5. **Processors for audio:** see 10-decision-records §10 item 14. The ones specific to this domain are LiveKit Cloud (media in transit), the streaming recognizers (audio in transit, no retention to be confirmed in the contract; AssemblyAI realtime is new in this revision), the verbatim recognizer (audio held for the transcription job) and the pronunciation vendor (a 15-second clip).
6. **[OPEN for Muath] The dial-in experiment's number and telephony provider** [P1]: a number in the beta cohort's most common residence country through a SIP provider into LiveKit, roughly $5 to $20 a month plus per-minute rates; it also needs the regime view (07 §4.9, ADR-20) on phone audio for that country. Not needed before 2026-12-23.
7. **Haiku 5.5 as the host:** see 10-decision-records §10 item 6 (the week-4 and week-5 50-call comparisons are the evidence; about $0.03 a call).
8. **[OPEN for Muath] Which clock PRD 15 means for the 1.5 s host reply.** 01 and this document gate `reply_latency_ms` from the end-of-turn decision and add a second gate on the learner-felt `silence_to_sound_ms` (p50 under 2.5 s, p95 under 4.0 s). If PRD 15 means the learner-felt clock alone, 1.5 s is not reachable together with PRD 5.4.4's 1.0 to 2.5 s patience, and PRD-v3 has to reconcile the two numbers. Decide before the build-week-2 run (2026-12-01) so the run is scored against the right clock.

Items of the first draft settled by the rulings and removed from this list: the Saudi dial-in number and the PDPL view (now per residence country, ADR-20, kept as item 6 in general form); the crisis review date of 2026-12-07 (now 2026-12-15 in 10-decision-records §10 item 12); the `vendors.yaml` freeze of 2026-11-15 (now 11-17, ADR-07).

---

## 11. Revision log (2026-11-06)

Both reviews of 2026-10-21 were applied in this revision for the first time (10-decision-records §9 had recorded them as applied; they were not). One bullet per finding or ADR.

- conformance major "header cost under-counted" → sparse `@m` header grammar (4.3, 4.4), `header_tokens`/`header_ms` measured, 4.15 rebuilt with vendor round trips, measured tokens/s from the vendor-chain check and `CALL_WORKER_REGION`; honest total stated.
- conformance major "crisis always ends the call" → `CRISIS ─(crisis.continue)─► ARGUE_AFTER` and `crisis.stop | 60 s` paths (4.3), `crisis.continue`/`crisis.stop` messages (4.12), D15 and the section 5 row agree; quarantine per 07 D9.
- conformance major "native-language repair and crisis phrases unmatched on the open mic" → host stream `[target, native]` with code-switch, matching on the raw final, spans stripped by code (`native_spans`), the secondary's narrowing logged and tagged [OPEN] (4.4, 4.14, 5, 10 #4).
- conformance major "`api` unreachable breaches the 15-minute rule" → worker local deletion duty at call end + 14 min, `spool/ingest` every minute, end record in the spool, `privacy/verify` check (3.1, 4.10, 5).
- conformance major "anxiety trigger and meaning" → `anxiety.last_call_abandoned` read by the governor, `"last_call_abandoned"` in `CallMetrics.anxiety_mode`, anxiety paragraph in layer A, `mode=anxiety (simpler questions)` in the note, `anxiety_mode`/`why_anxiety` on `call_ended` (4.3, 4.4, 4.12); the "correction moves to Salma's notes" part is void under ADR-06 (the ADR wins).
- conformance major "governor enforces only maxima" → `Allowances.must`, `pushback` counter, `minima_unmet()` logged and gated, retell window tagged [ASSUMPTION] (4.3, 4.13).
- conformance major "50-call test in week 4 contradicts PRD 14.4" → three runs with gates per run: vendor-chain check in Milestone 0, run #1 week 2 by 2026-12-01, run #2 week 4, run #3 week 5 (4.13, 7); dates per ADR-07.
- conformance major "talkback secondary cannot do Arabic" → `talkback_stt` secondary AssemblyAI Universal realtime, in the recognizer test; "both native-capable recognizers down" row (4.14, 4.13, 5); Deepgram stays the host-stream secondary.
- conformance major "raw DEK in the bundle" → `crypto.call_key` + `key_derivation`, `media_objects.key_derivation` on every row, SSE-KMS spool, `call_turn_verbatim` append (4.2, 4.10, D16, 9.1, 9.6).
- conformance major "talkback audio in the turn PCM" → frames dropped from the turn PCM and the full mix, streamed only, `"ar"` removed from `CallTurnAudioReady.language`, `talkback_ms_excluded` (4.7, 4.10, 4.12).
- conformance major "no wrong-memory path" → `wm="<quote>"` header key, layer A instruction, `wrong_memory_flag` event, `do not mention` in later notes (4.3, 4.4, 4.12).
- conformance minor "`p + max_extend` departs from PRD 5.4.4" → tagged [DECISION] in D3 with the cap at 1.0 s for `p >= 1.5`; said in 4.5 and the 5.4.4 requirements row.
- conformance minor "retell 90 s and hard end can cut the learner" → ring disappears, host waits; hard end waits for the learner turn; both in the turn machine and timers (4.3, 5).
- conformance minor "Haiku fallback 400s" → per-model request builder (Haiku without `thinking`, `effort: low`; Gemini notes folded into the user turn), fixture test and canary (4.4, D7, 4.14 `request_shape`).
- conformance minor "cost prose understates" → $0.16 to $0.17 (Inworld or Gemini) and $0.21 to $0.22 (ElevenLabs), levers named (6).
- conformance minor "typed onboarding needs a room" → 01's typed route adopted, `text.turn` deleted, recorded in 4.9 and 9.1.
- conformance minor "name clip deleted before 02 reads it" → `hold_until_consumed`, `name_clip_text` on `onboarding.intake_completed` (4.9, 4.10, 9.2).
- conformance minor "two pause-profile formulas" → 04's formula referenced; this domain emits `cut_offs` and `pauses_ms[]` with an explicit direction as an ask of 04 (4.5, 9.3).
- conformance minor "motion hints" → dropped; measure from `end_reason` plus `started_by` and the M0 self-report (4.11, 8, 9.5).
- conformance minor "recast stress left to the vendor" → emphasis markup in the TTS adapter, `recast_emphasis_supported` on `vendor_calls` (4.8, 3.2).
- conformance minor "untagged pass lines" → every line tagged [ASSUMPTION] with its rationale and the no-vendor-passes rule (4.13).
- conformance minor "round two next-day only" → available from main done until the session closes; suggested next day (4.3).
- conformance minor "150 ms client mute" → removed; Chrome-only fallback if echo proves a problem (4.11).
- conformance minor "`meaning_lost` undefined" → removed; clarify cap is the only hard gate; `clarify_on_clean_turn` logged (4.3).
- conformance missing: PRD 12.1 turn signal → `turn_signal_clip` at HOST_SPEAKING → LISTENING (4.3, 4.5); nudge self-repair pause → `p + 1.0 s` rule (4.3, 4.5); recast on targets only → `recast_off_target` (4.3); main-call-once door rule → 4.1; Salma crisis and "are you real?" on the talkback stream → 4.7.1; host share lever → `Allowances.shorter` (4.3, 4.4); `clear_at: next_user_message` → 4.4; onboarding first-sound budget → 4.9; asks carried in section 9.
- skeptic blocker "latency arithmetic wrong by 2×" → as the conformance header finding, plus `max_tokens: 200` with the `max_tokens` stop-reason path, preemptive generation (D18), per-stage `latency` on `CallTurnPayload` (4.3, 4.4, 4.12, 4.15).
- skeptic blocker "plan needs one engineer full time" → section 7 rewritten against 01 §7's E2 column and ADR-07 dates; cut list adopted in full with the P1 list and the "ships after 2026-12-22" statement (7).
- skeptic major "LiveKit API does not match; two owners of end-of-turn; text turn model deprecated and without Arabic" → manual turn mode, `turn-controller` as single owner, audio turn detector, option names verified in week 1 (`SDK-NOTES.md`), VAD plus 1.8 s for onboarding, "incomplete" rate measured (D1, 4.3, 4.5, 4.9, 7).
- skeptic major "raw DEK, no worker auth, route names" → per-call key and JWT (D16, 3.2, 3.3, 4.2), `/internal/calls/{id}/turns` adopted with the `/end` deviation recorded (3.1, 9.1), spool encryption stated (4.10).
- skeptic major "pause profile measures a censored distribution" → formula withdrawn; two directional signals; cut-off rule kept in P0 (4.5, 8, 9.3).
- skeptic major "no gate on the learner-felt silence" → `silence_to_sound_ms` gate p50 2.5 s / p95 4.0 s, preemption, extension cap, incomplete-rate measurement, [OPEN] on the clock (4.13, 4.15, 10 #8).
- skeptic major "pre-rendered assets unowned" → clips rendered by this domain through `voice-studio.render` on first voice use; opening line as a dated ask of 02; reverse gloss index cut (4.5, D6, 9.2, 7).
- skeptic major "request-shape errors (Haiku 400, double system entry)" → per-model builder; re-request rebuilds the single operator note, never a second system entry (4.3, 4.4).
- skeptic major "cache breakpoints through the stock plugin unverified" → week-1 probe, thin `llm.LLM` subclass decision, `cache_read_tokens` on `call_turn` (3.1, 4.4, 4.12, 7).
- skeptic minor "diagram and code describe different machines" → `tick()`, RETELL exit, owed recall gaps, retell precondition removed, dead `grades` check deleted with the never-list enforcement stated, malformed header re-requested, `last_call_abandoned` wired (4.3).
- skeptic minor "`call_turn` update and typed onboarding contradict 04 and 01" → `call_turn_verbatim` append with `turn_index`; `text.turn` deleted (4.10, 4.12, 4.9).
- skeptic minor "lifecycle backstop on an unused prefix" → `ephemeral/learners/{lid}/calls/...` (04 D15 puts `ephemeral/` first so the lifecycle rule can match it) for storage-off audio, prefix chosen at upload time (4.10).
- skeptic minor "talkback stream opened on S-down; 800 ms timeout" → open at job start, gated by S; 1.5 s timeout with the wait clip at 700 ms (D5, 4.7, 4.14).
- skeptic minor "client-side replay, 150 ms mute, echo counted as cut-offs" → replay from the worker; mute deleted; cut-offs gated on the interruption threshold (4.6, 4.11, 4.5).
- skeptic minor "learner transcriptions still published to the room" → room transcription output disabled in the worker; `call-bench` check (4.8, 4.13).
- skeptic minor "cost table" → output line recomputed for the sparse header; totals restated; `min_tasks: 2`, autoscaling P1 (6, 4.14).
- skeptic minor "one tool for both tests" → `vendor-lab recognizers` and `tools/call-bench calls` with in-process injection (D13, 4.13, 3.1); ADR-19's `tools/call-bench` name kept for the latency tool.
- skeptic minor "output guard never called; no backchannel in THINKING" → `guard.check_output` between `check()` and TTS (D17); `THINKING ─(1.2 s)─► FILLER` with filler clips (4.3, 4.5, 5).
- skeptic minor "talkback path untested; Bluetooth capture" → 20-ask talkback fixture and 6 Bluetooth clips in the recognizer test; earphones hint (4.13, 4.11).
- skeptic missing: SDK verification scheduled (7, week 1); asset ownership (4.5, 9.2); worker auth and key (D16); Anthropic rate limits (4.4, 6, 10 #3); `POST /v1/calls` idempotency and token TTL (3.2, 4.11); `max_tokens` handling and `cache_read_tokens` (4.3, 4.4); onboarding endpointing and Salma's reply latency (4.9); talkback fixture (4.13); costguard and invite gate on onboarding (4.9); `audio/expire` under an `api` outage (4.10, 5); per-stage latency on `CallTurnPayload` (4.12).
- ADR-01 → front matter cites decisions.md and the ADRs where they changed a PRD part.
- ADR-02 → `languages: {native, target}` in the bundle, `packages/languages/<target>/` and `packages/native/<lang>/` throughout, `talkback_stt.languages = [native, target]`, Salma from the native package, repair, crisis and driving phrases per language, `vendors.yaml` roles keyed by target; every Arabic-only or Saudi-only assumption rewritten as one instance of the rule (sections 1 to 10). "Arabic" remains only as the pilot example (`native/ar`), in the LiveKit detector's language-list fact, and in Salma's example lines.
- ADR-03 → the 30-clip test and the vendor-chain check run as the language gate's checks 2 and 4 from `vendor-lab`; the threshold lands in `packages/languages/en/recognizer.yaml` (4.13, 7).
- ADR-04 / ADR-15 → plan-aware cost note and `costguard` call-start cap of 6 × `episodes_per_day` (6, 4.9, 9.6).
- ADR-06 → Salma's notes, the polish card and the 90-second stage removed from the summary, D9, the requirements table, 3.2 step 9, 4.10 and 9.4; correction guard on the live turn (D17, 4.3, 4.4, 5); `explicit_corrections` and `explicit_corrections_per_100_turns` (4.12, 4.13); layer A forbids "wrong"/"the correct form is"; the brief's recast list named as the echo plan (4.2, 4.4); `salma_explain` noted as out of scope (front matter).
- ADR-07 → section 7 re-dated (W1 Nov 18–24 to W5 Dec 16–22, freezes, beta from 12-23, P1 to 2027-01-26); 10.14 by 11-10; `vendors.yaml` by 11-17; every 2026-11-02, 11-15 and 12-07 date moved (2, 4.13, 7, 10).
- ADR-08 → `HOME_REGION = eu-central-1` default noted in 9.1; `CALL_WORKER_REGION` kept as 01's latency placement.
- ADR-09 → Langfuse metadata-only wording in 9.7.
- ADR-12 → `media_objects.encryption = 'sse_c_learner'` on learner-voice kinds; clips under SSE-KMS (3.4, 4.5, 4.10).
- ADR-13 → `vendor_calls` rows appended to the worker's S3 spool per turn, reconciled hourly (3.1, 3.3, 5, 9.7).
- ADR-16 → no Riyadh-centric window; `call-worker` deploys drain at any hour; `drained` end reason; `privacy/verify` hourly; staging up from week 2 (4.1, 5, 7, 9.8).
- ADR-18 → the zeroization claim dropped for the per-call key; `keys.get_dek` 60 s versioned cache referenced (4.10, 9.6).
- ADR-19 → `call_turn_verbatim` as the second event with `turn_index`; `tools/call-bench` as the latency tool; `word_uses` written by 05; `episodes.state` not referenced here (3.4, 4.10, 4.12, 9.3).
- ADR-20 → resources card per `residence_country`, crisis clips per pair, the dial-in item generalised (D15, 4.2, 4.12, 10 #6).
- ADR-22 → section 10 items 3, 4, 5 and 7 point to the register; items 1, 2, 6 and the new 8 stay here.
- Not applied, deliberately: (a) the conformance fix's second option for the open-mic Arabic case ("declare it not possible in the beta") was not taken; the first option (both languages on the host stream, spans stripped by code) was, with only the secondary-recognizer narrowing left [OPEN]; (b) the conformance fix "render `mode=anxiety` and carry it so 05 can move the correction to the notes" was applied without the notes part, because ADR-06 removed the notes (the ADR wins); (c) the skeptic's suggestion to cut the driving-phrase path and in-call `p` adaptation was not taken (each is a phrase list or one counter; section 7 says so); (d) the skeptic's `@m recast="I go">went gap=rg2` spelling was shortened further to `r=...`/`g=...` for the same token count; (e) the 90k-cached-tokens-per-call figure in section 6 is kept as is (it is per call over 25 turns and is correct).
