# Live call and voice stack

Domain 3 of 9 of the For one technical architecture. Written 2026-10-16 against PRD-v2 (Implementation PRD v3.0, 2026-10-10), concept-v2 sections 7 to 10, decisions.md, the voice-speech, AI-architecture and UI-UX lenses, and the Milestone 0 kit (04-production.md, 05-prompts.md). "PRD x.y" means PRD-v2 part x.y. Tags: [DECISION] decided here; [ASSUMPTION] assumed because the spec is silent; [OPEN for Muath] only the owner can settle. Where this document names a service, table or event that the topology document (01-system-topology.md) or the pipeline document (02-generation-pipeline.md) already named, it uses their name; where it deviates, it says so in section 9.

This document covers everything that happens between the learner's tap on "Call" and the moment the call's evidence is safely in the event log: the LiveKit Agents pipeline, the host's move contract as a state machine, hold-to-talk and adaptive patience, the Huh? signal on the call, talkback to Salma, Salma's voice at onboarding, the client's audio handling, recording and the deletion windows, verbatim re-transcription and pronunciation scoring, the two vendor tests, outage behaviour and cost. It does not design the after-session analyst, the learner model, the generation pipeline that writes the call brief, the client app beyond the call screen, or billing.

---

## 1. Summary and the decisions in one table

The call is one Python process per concurrent call inside the `call-worker` service (LiveKit Agents), fed by a streaming recognizer, a Sonnet-class host whose brief sits in a cached prompt prefix, and the episode vendor's streaming voice, so the host sounds like the episode. Code, not the model, enforces every budget in the host's move contract (PRD 5.4.6): the host declares its moves in a one-line header before it speaks, and a governor in the worker checks that header against the remaining budgets before any audio is synthesized. Turn-taking is a learner-specific setting, not a vendor default: end-of-turn silence starts at 1.5 s and comes from the pause profile within 1.0 to 2.5 s, the floor can be held with a pad, and the host backchannels from pre-rendered clips instead of waiting in silence. Talkback is a second recognizer stream (Arabic-capable) opened only while the S button is held, answered by Salma on a separate audio track in under 2 s. Every learner turn is uploaded as it ends and transcribed verbatim while the call continues, which is what makes Salma's notes possible 90 s after the call and makes the 15-minute deletion window safe to honour. When live voice fails, the same call thread continues as voice notes through one Inngest function and nothing is lost.

| # | Decision | Reason | Alternative rejected |
|---|---|---|---|
| D1 | Pipeline (streaming STT, text host, streaming TTS) on LiveKit Agents, one `AgentSession` per call [DECISION, PRD 14.3] | The only design where the recast, the transcript and the voice are all under the product's control; LiveKit's multilingual turn model covers Arabic for talkback | Speech-to-speech models (no custom voice, approximate transcripts, per-turn re-billing); Pipecat (English-only turn model) |
| D2 | Host declares moves in a header line before its reply text; a code governor enforces the PRD 5.4.6 budgets and can abort and re-request once [DECISION] | Law 7 and the move caps are hard constraints; a prompt alone cannot be trusted to count | Structured-output JSON for the whole reply (delays first audio until the JSON closes); post-hoc filtering of text (cannot remove a nudge once spoken) |
| D3 | End-of-turn silence `p` from the pause profile, 1.5 s for a new learner, clamp 1.0 to 2.5 s; when the turn model says the sentence is unfinished, wait up to `p + 1.5 s` with one backchannel at 1.2 s [DECISION, PRD 5.4.4] | Learners pause mid-clause about three times as often as natives (voice lens); the vendor defaults of 0.5 to 0.8 s cut them off | A fixed long silence (makes every reply slow); vendor semantic VAD only (not tunable per learner) |
| D4 | Backchannels are pre-rendered clips per host voice, chosen by code, never synthesized live [DECISION] | Zero latency and zero cost at the moment latency matters most; the words never take the floor because the list is fixed | Asking the model for a backchannel (adds a model round trip inside the learner's pause) |
| D5 | Talkback audio goes to a second recognizer stream (Soniox, `ar`+`en`) opened on S-down and closed on S-up; the host stream is paused and its turn detector frozen; Salma answers on a second published audio track [DECISION, PRD 5.4.5, 0.1 row 7] | Keeps Arabic out of the host's transcript, keeps the floor held, and lets the client draw the bubble from S | One multilingual stream for both (code-switch errors leak into the host's input); client-side recording and upload (adds 1 to 2 s) |
| D6 | Word-or-hint is decided by code from the Salma talkback brief (produced-word set), not by the model [DECISION, PRD 5.4.5 rule 4] | A rule with a lookup is exact; a model would sometimes give the word to a learner who has it | Model decides from the brief in the prompt |
| D7 | Host LLM: `claude-sonnet-5-5`, `output_config.effort: low`, `thinking: {type: "between_tools"}` (no tools, so no thinking before the reply), brief in the cached prefix, per-turn operator notes as mid-conversation system messages [DECISION, PRD 14.3] | First token in 300 to 600 ms with the cache warm; mid-conversation system messages keep the cached history intact; Haiku 5.5 is the measured fallback if the 50-call test says quality holds | Opus-class host (latency and cost); Haiku-class by default (quality in the recast moves unproven) |
| D8 | Call TTS is the episode vendor's streaming voice with the same `voice_id`; the pipeline's blind test only admits vendors whose streaming endpoint has a first-byte latency under 300 ms at p95 [DECISION, PRD 14.3, 7.1] | "The host sounds the same" is a PRD rule; a vendor that cannot stream fast enough cannot be the episode vendor either | Different vendor on the call with an "understudy" voice (Milestone 0 did this; the day-7 check-in asks whether it mattered, and the PRD chose sameness) |
| D9 | Each learner turn is uploaded as it ends (`call.turn_audio_ready`) and transcribed verbatim during the call; the full mixed recording is uploaded only when voice storage is on [DECISION, PRD 5.4.11, 10.2] | Notes within 90 s need the verbatim text at call end, not 3 minutes later; the 15-minute deletion window is met with margin | Transcribe the whole call after it ends (notes late; one big deletion race) |
| D10 | Voice-note fallback runs as the Inngest function `call/voice-note-reply` using the same brief, host prompt and voice; the client switches when the room is not joined within 3 s, on two pipeline errors, or on an ICE failure longer than 5 s [DECISION, PRD 5.4.10] | One brief, one host, one thread; the learner's argument continues | A separate "voice note host" prompt (two hosts to keep in character) |
| D11 | The first host line of every call is synthesized at episode time by the pipeline and stored with the brief; the worker plays it while the vendor websockets open [DECISION, PRD 15 "call connect under 3 s"] | The learner hears the host within the connect budget even on a cold worker | Synthesize on connect (adds 0.5 to 1 s to the first sound) |
| D12 | Client audio: `getUserMedia` with echo cancellation, noise suppression and AGC on; Screen Wake Lock re-acquired on every `visibilitychange`; a backgrounded page is treated as an abandoned call after 10 s [DECISION, PRD 1.4] | iOS Safari suspends WebRTC in the background with no fix (voice lens); pretending otherwise loses evidence | Keep-alive tricks (unreliable, and they drain the battery) |
| D13 | The 30-clip test and the 50-call test run from one tool, `tools/call-bench`, against the staging worker with the Milestone 0 clips as the scripted caller [DECISION, PRD 10.14, 14.4] | One harness measures recognizers, latency and the move contract on the same audio, and reruns on every prompt or vendor change | Separate scripts per vendor (never rerun) |
| D14 | The observer (PRD 14.1, [LATER]) has a reserved slot: one mid-conversation system message per turn, keyed `whisper`; nothing in the beta depends on it [DECISION] | Costs nothing now; prevents a redesign later | Building it in the beta (PRD 17 excludes it) |
| D15 | Crisis protocol in the call: the host declares `crisis` in its header or a package keyword list fires on a learner turn; the worker then plays the pre-rendered package lines (English, then Arabic), sends the resources card to the client, logs `crisis_activation` and ends the argument [DECISION, PRD 7.9] | Two independent triggers; fixed, counsel-reviewed lines rather than generated ones | Model-only detection; generated crisis text |

---

## 2. Requirements this domain implements

| PRD part | Requirement | Where in this document |
|---|---|---|
| 2.2 A2, A3 | Salma's voice in Arabic within 60 s of first open; at most 8 turns, two English lines, fact cards as she hears them; talk or type | 4.9 |
| 2.2 A7 | First call 60 to 90 s; no recasts or nudges; Salma's one-line introduction of talkback before it rings | 4.3 (budgets by call kind), 4.9 |
| 4 rule 4 | A call cannot resume; an interrupted call restarts fresh with a line that acknowledges the gap | 4.2 (`resumed_after_drop`) |
| 4 rule 3 | Planning card before Call when Read was skipped | 4.11 (client), the words come from the brief |
| 5.4.1 | One tap from the throw, Today or the feed link; screen awake; earphones suggested once | 4.11 |
| 5.4.2 | Target 5 to 7 min; natural close from 6:30; end by 8:00; learner may end any time with an in-character close | 4.3 timers |
| 5.4.3 | Host share of talk at most 40%; short turns | 4.4 prompt, 4.3 governor, 6 metrics |
| 5.4.4 | Open mic; hold to keep the floor; adaptive patience 1.0 to 2.5 s from the pause profile; one backchannel per pause over 1.2 s; 8 s silence handling; "sorry?" and "slower"; previous-track replays the host's last line | 4.5, 4.6 |
| 5.4.5 | Talkback to an Arabic-capable recognizer; the host waits; Salma's closer voice; word or hint; logged per word | 4.7 |
| 5.4.6 | The move contract with its caps | 4.3, 4.4 |
| 5.4.7 | Anxiety mode and its three triggers | 4.3 |
| 5.4.8 | Host captions by default, recast word bold, learner never captioned live, no correction UI | 4.8, 4.11 |
| 5.4.9 [P1] | Round two: 2 to 3 min, same host and argument, a like-for-like retell sample | 4.3 (kind `round_two`), 7 |
| 5.4.10 | Live voice failure falls back to voice notes in the same thread | 5.1 |
| 5.4.11, 12.5, 15 | Streaming transcript drives the call; verbatim re-transcription after; audio kept only with consent; deletion within 15 min when storage is off, within 24 h on revoke; transcripts always kept | 4.10 |
| 5.4.12 [P1] | Dial-in: 8 kHz, planning only, low confidence, no claims | 7 |
| 5.5 | Notes within 90 s depend on the verbatim transcript being ready at call end | 4.10 (per-turn verbatim) |
| 7.3 | Salma's voice closer and drier than the hosts'; Arabic variety OPEN | 4.7, 4.9 |
| 7.8, 7.9 | AI disclosure on request by every character; crisis protocol in live roles | 4.4, 4.3 |
| 8.1, 14.2 | Live roles never write; the worker produces events only | 3.3 |
| 8.2 | Events `call_turn`, `talkback`, `hold_floor`, `silence` with streaming and verbatim text, word timings, confidences | 4.12 |
| 8.6 | The host's one-page brief; Salma's talkback brief (produced-word history) | 4.2 |
| 10.2 step 1, 10.3 | Verbatim re-transcription of every learner audio turn (call, round two, shadow, say it once, small-door note); pronunciation on known sentences only, internal | 4.10 |
| 10.14 [P0] | The 30-clip recognizer test, before build week 2; confidence threshold from it | 4.13 |
| 14.3 | LiveKit Agents; Soniox or Deepgram; AssemblyAI or ElevenLabs Scribe; Speechace or Microsoft; adapters; two voice vendors wired | 3, 4.14 |
| 14.4 #3 [P0] | 50 scripted calls, median host reply under 1.5 s | 4.13 |
| 14.5 | Call plus round two at about $0.16; re-transcription plus pronunciation $0.03 | 6 |
| 15 | Call connect under 3 s; host reply median under 1.5 s and p95 under 2.5 s; talkback under 2 s; voice-vendor outage covered by the second vendor the same day | 4.15, 5 |
| 16.2 | Talkback use per call; recognizer error by first language; calls abandoned on the move; feed-to-call handoff | 4.12, 6 |
| 1.2 laws 1, 5, 7, 8, 12 | No game furniture on the call screen; honesty; conversational corrections only; conversations end like conversations; no claims from the live path | throughout; 3.3 |

---

## 3. Architecture

### 3.1 Components

Draw as four columns, left to right: the phone, LiveKit Cloud, the `call-worker` process, and the vendors; with `api`, Postgres, S3 and Inngest as a row underneath.

| Component | Runs in | What it does |
|---|---|---|
| Call screen (`web`, client domain; the audio parts are specified in 4.11) | the phone's browser | Mints a call through `api`, joins the room, publishes the mic, plays two agent tracks (`host`, `salma`), sends control messages, renders captions and the bubbles, records voice notes in the fallback |
| LiveKit Cloud | managed | WebRTC media between phone and worker, data channel, agent dispatch, room lifecycle, SIP ingress for the dial-in experiment [P1] |
| `call-worker` | ECS Fargate, Python 3.12, LiveKit Agents | One job per call. Inside the job: `CallSession` (our wrapper around `AgentSession`), the turn-taking controller, the move governor, the talkback controller, the recorder, the event emitter |
| `turn-controller` (module) | in the job | Silero VAD, LiveKit multilingual turn detector, pause profile, hold-floor state, backchannel scheduler, silence timers |
| `host-governor` (module) | in the job | Budgets per call kind, phase clock (open, argue, retell, close), parses the `@moves` header, aborts and re-requests, anxiety mode, crisis switch |
| `talkback-controller` (module) | in the job | Opens the Arabic stream on S-down, resolves word-or-hint, synthesizes Salma on the `salma` track, logs `talkback` |
| `recorder` (module) | in the job | Buffers each learner turn's PCM, encodes, uploads with SSE-C, emits `call.turn_audio_ready`; mixes the full recording when voice storage is on |
| `event-emitter` (module) | in the job | `POST /internal/events` in batches of 20 or every 2 s; spools to S3 if `api` is unreachable |
| Streaming recognizer adapter | LiveKit STT plugin | Soniox primary, Deepgram secondary, chosen by `vendors.yaml` role `streaming_stt`; a second instance for talkback (`talkback_stt`) |
| Host LLM adapter | LiveKit LLM plugin | Anthropic `claude-sonnet-5-5`; fallback `claude-haiku-5-5`, then the second vendor |
| Call TTS adapter | LiveKit TTS plugin | The episode vendor's streaming endpoint with the casting's `voice_id`; the understudy vendor during failover |
| Salma TTS adapter | LiveKit TTS plugin | The Arabic voice from the 7.3 test, role `salma_tts` |
| `api` | ECS | `POST /v1/calls`, `GET /internal/calls/{id}/brief`, `POST /internal/events`, `POST /v1/calls/{id}/voicenotes`, `POST /v1/calls/{id}/end` |
| Inngest functions | `workflows` | `call/verbatim-turn`, `call/voice-note-reply`, `call/pronunciation-score`, `audio/expire` (topology), and the hooks into `session/after-pass` (assessment) |
| `tools/call-bench` | developer laptop or CI | The scripted caller for the 30-clip and 50-call tests, and the simulated caller of the P1 offline suite |

### 3.2 Data flow for one main call (draw as a sequence diagram with the five lanes above)

1. The learner taps Call. `web` calls `POST /v1/calls {sessionId, kind: "main"}`. `api` checks the door rules (PRD 4), writes the `calls` row, creates room `call-{callId}` with agent dispatch metadata `{callId}`, and returns `{callId, roomUrl, token, openingClipUrl}`.
2. `web` joins the room and publishes the mic. In parallel, the worker accepts the job, calls `GET /internal/calls/{callId}/brief`, receives the `CallBundle` (4.2), opens the STT websocket and the TTS websocket, and publishes the `host` and `salma` tracks. The moment the learner's mic track is subscribed, the worker plays the pre-rendered opening line from the bundle on the `host` track (D11) and sends `state {phase: "opening"}`.
3. The learner speaks. VAD frames and STT partials flow; the turn controller decides end-of-turn (4.5). On end-of-turn the worker has the final streaming text with word timings; it emits `call_turn` (speaker `learner`, streaming text), hands the turn's PCM to the recorder, and asks the governor for this turn's allowances.
4. The governor appends a mid-conversation system note (allowances, clock, mode) and the learner's text to the conversation and calls the host LLM with streaming. The first line of the reply is the `@moves` header; the governor parses it, checks it, and either lets the rest stream into TTS or aborts and re-requests once (4.3).
5. The TTS stream plays on the `host` track; caption segments go to the client over the data channel with the recast span marked. When the host finishes, the worker emits `call_turn` (speaker `host`, text, moves, `reply_latency_ms`) and the turn controller returns to listening.
6. Meanwhile the recorder has encoded the learner's turn, uploaded it to `forone-voice/learners/{lid}/calls/{callId}/turn-{n}.ogg` with SSE-C under the learner's DEK and emitted `call.turn_audio_ready`. Inngest runs `call/verbatim-turn`: verbatim transcription with disfluencies and confidences, written back as an update to that `call_turn` event; if voice storage is off, the turn object is deleted when the verbatim write succeeds.
7. If the learner holds S: the talkback controller freezes the turn detector, opens the Arabic stream, and on release resolves the ask and speaks Salma's answer on the `salma` track within 2 s; `talkback` is logged with the word, the mode (word or hint) and the latency.
8. At 6:30 the governor tells the host to begin the close; at 7:40 to say goodbye in one line; at 8:00 the worker ends the session after the current sentence. Or the learner taps ✕: the worker lets the host say one in-character line, then ends. The worker emits `call.ended {end_reason, voice_storage, turns, learner_speech_ms, host_speech_ms}`, closes the vendor streams and leaves the room. If voice storage is on, it uploads the full mixed recording as `call_full`.
9. `session/after-pass` (assessment domain) starts on `call.ended`; stage 1 waits only for the last turn's verbatim result, so the notes are ready within 90 s. `audio/expire` (topology) sleeps 14 minutes and deletes whatever ephemeral audio remains when storage is off.

### 3.3 Boundaries and the writing rule

The worker never reads the learner model and never writes a store. It receives one `CallBundle` at dispatch, keeps everything in memory for the call, and emits events. The only durable writes it causes are `events` rows (through `api`), `media_objects` rows (through the upload path) and the `calls` row's `ended_at`, `end_reason`, `vendors` and `metrics` columns (through `POST /internal/calls/{id}/end`). This is PRD 8.1 rule 3 and 14.2 made structural: there is no code path from the worker to the nine stores, so a host cannot "remember" what it misheard.

### 3.4 Interfaces to other domains

| Direction | Interface | Owner |
|---|---|---|
| in | `episode_artifacts(kind=call_brief)` with the `CallBrief` type, `voice_casting` for the learner, the opening-line clip ref | pipeline domain |
| in | Compiled `HostBrief` and `SalmaTalkbackBrief` (4.2) built by the host brief compiler, which this domain owns as a module in `forone.core.briefs` but which runs inside `episode/make` at publish time and again at `POST /v1/calls` when the learner model version has changed since | this domain (module), pipeline domain (call site) |
| in | `vendors.yaml` and `vendor_config` rows; the learner's DEK unwrapped by `api` | topology, security domains |
| in | Pause profile, anxiety prior, last-call-abandoned flag, produced-word set | learner model domain (Skills and Word bank stores) |
| out | Events `call_turn`, `talkback`, `hold_floor`, `silence`, `replay_line` (door `call`), `crisis_activation`, `call_started`, `call_ended`; Inngest events `call.turn_audio_ready`, `call.ended`, `voicenote.received`, `pronunciation.requested` | data domain (event log), topology (Inngest shells) |
| out | `media_objects` of kinds `call_turn`, `call_full`, `voice_note`, `say_it_once`, `shadow`, `recording` | security and data domains |
| out | Per-call metrics in `calls.metrics` and `vendor_calls` rows per adapter call | cost and evaluation domains |

---

## 4. Detailed design

### 4.1 Call kinds and the `calls` row

The `calls` table is the topology's (01-system-topology.md 4.2). This domain adds two columns and fixes the enums:

```sql
alter table calls add column metrics jsonb not null default '{}';   -- CallMetrics (4.12)
alter table calls add column bundle_version int not null default 1; -- which HostBrief compile was used
-- kind: onboarding | first | main | round_two | small_door | then_and_now
-- mode: live | voice_notes
-- end_reason: natural_close | learner_ended | timeout_8m | pipeline_error | fallback | crisis | abandoned | driving
```

| kind | PRD | Persona | Length | Budgets (4.3) | Enters the after-session pass as |
|---|---|---|---|---|---|
| `onboarding` | 2.2 A3 | Salma, Arabic | about 3 min, at most 8 Salma turns | n/a (Salma has her own contract, 4.9) | intake facts, two English moments |
| `first` | 2.2 A7 | throwing host | 60 to 90 s | no recast, no nudge, clarify only if meaning is lost, no recall gaps, no retell, praise 1 at the end | first speaking estimate |
| `main` | 5.4 | throwing host | close from 6:30, end 8:00 | full contract | the main call |
| `round_two` [P1] | 5.4.9 | same host | close from 2:00, end 3:00 | retell first, 1 recall gap, recasts kept, no nudge | fluency sample |
| `small_door` | 3.7 | none live | one voice note up to 60 s | n/a | voice note |
| `then_and_now` | 10.9.2 | Salma narrates from pre-rendered clips | about 3 min | no live model; the client records three tasks | recording |

`small_door` and `then_and_now` are not live calls: they are recordings captured by the client and uploaded through the same `/voicenotes` and `/recordings` routes, listed here because the recorder, the verbatim path and the deletion rules are shared.

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
  anxiety: { prior: boolean; last_call_abandoned: boolean };
  voice: { host: "karim"|"mona"|null; vendor: string; voice_id: string; rate: number; understudy: { vendor: string; voice_id: string };
           salma: { vendor: string; voice_id: string; variety: "gulf"|"white" };
           backchannel_clips: { id: string; url: string; duration_ms: number }[];   // pre-rendered per host voice
           opening_clip: { url: string; text: string; duration_ms: number } | null;
           package_clips: { crisis_en: string; crisis_ar: string; talkback_intro_ar: string } };
  vendors: { streaming_stt: string; talkback_stt: string; host_llm: { vendor: string; model: string; fallback: { vendor: string; model: string } };
             call_tts: string; salma_tts: string };
  consent: { voice_storage: boolean };
  crypto: { dek: string /* base64, 32 bytes, memory only */; key_version: number };
  language: { repair_phrases: string[]; crisis_keywords: string[]; name: { display: string; respelling: string } };
  limits: { close_begin_s: number; hard_end_s: number };
  bundle_version: number; learner_model_version: number; prompt_version: string;
};

type HostBrief = {                                 // PRD 8.6: one page; target under 900 tokens
  host: "karim"|"mona"; learner_name: { display: string; respelling: string; pronouns: "he"|"she"|null };
  episode_in_3_lines: string[]; question: string; planted_phrases: string[];
  position: string; pushback: string[];
  targets: { grammar: { id: string; label: string; necessity_moves: string[]; recast_list: { expected_error: string; recast_form: string }[] };
             words: { lemma: string; move: string }[] };
  recall_gaps: { id: string; line: string; expected: string }[];     // 2 to 4
  retell_prompt: string;
  callback: { text: string; fact_id: string } | null;               // exactly one, confirmed
  never_mention: string[];
  budgets: Budgets;                                                 // from the kind table, adjusted by anxiety.prior
  style: { accent: "british"|"american"; max_words_per_turn: number /* 25 */ };
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

The `HostBrief` is assembled from `CallBrief` (pipeline) plus four learner-model reads: name and respelling from `voice_casting.name`, the pause profile and anxiety prior from Skills, the `never_mention` list from Life ("don't bring up") and `working_on` vetoes, and `callbacks_allowed` filtered again at compile time against the fact's current status (a fact deleted in the notebook after the brief was written is dropped here; PRD 8.4 rule 7).

### 4.3 The host move contract as a state machine

Two machines run together: the call phase machine (time and content) and the turn machine (who has the floor). The governor owns the phase machine and the budgets; the turn controller owns the turn machine.

**Phase machine (per call, kind `main`; `first` and `round_two` use the same states with the timers from 4.1):**

```
CONNECTING ─(mic subscribed)─► OPENING ─(host opening line done)─► ARGUE
ARGUE ─(host declares retell, window 2:00..4:30 and recall_gaps_used >= 1)─► RETELL
RETELL ─(learner turn ends, or 90 s)─► ARGUE_AFTER
ARGUE | ARGUE_AFTER ─(t >= close_begin_s)─► CLOSING
CLOSING ─(host declares close, or t >= hard_end_s - 20 s)─► GOODBYE
GOODBYE ─(host line done)─► ENDED
any ─(learner ✕)─► GOODBYE(reason=learner_ended)        one in-character line, then end
any ─(crisis)─► CRISIS ─► ENDED(reason=crisis)
any ─(driving phrase)─► GOODBYE(reason=driving)         "Call me back when you've parked."
any ─(pipeline failure x2 | room lost > 5 s)─► FALLBACK ─► ENDED(reason=fallback)
```

**Turn machine:**

```
HOST_SPEAKING ─(TTS done)─► LISTENING
LISTENING ─(speech starts)─► LEARNER_SPEAKING
LEARNER_SPEAKING ─(silence >= endpoint, turn complete)─► TURN_ENDED ─► THINKING ─► HOST_SPEAKING
LEARNER_SPEAKING ─(silence >= 1.2 s, turn incomplete, no backchannel yet this pause)─► BACKCHANNEL ─► LEARNER_SPEAKING
LEARNER_SPEAKING ─(silence >= endpoint + max_extend)─► TURN_ENDED
LISTENING ─(silence >= 8 s)─► SILENT ─(governor: smaller question)─► HOST_SPEAKING
any listening state ─(hold.down)─► FLOOR_HELD ─(hold.up, 300 ms grace)─► LEARNER_SPEAKING | TURN_ENDED
any listening state ─(talkback.down)─► TALKBACK ─(talkback.up, Salma answered)─► FLOOR_HELD (if pad still held) | LISTENING
HOST_SPEAKING ─(learner speech >= interruption_min_ms and >= 2 words)─► LEARNER_SPEAKING   (host stops; the cut text is logged as unsaid)
```

**Budgets and the governor.** Before each host turn the governor computes `Allowances` from the budgets, the phase, the mode and the counters, writes them into the operator note (4.4), and after the reply checks the header against them.

```python
# apps/call-worker/forone_call/governor.py
from dataclasses import dataclass, field

@dataclass
class Counters:
    clarify: int = 0; nudge: int = 0; recall_gaps: int = 0; retell: int = 0; praise: int = 0
    silence_offers: int = 0; recasts_this_turn: int = 0; violations: int = 0

@dataclass
class Allowances:
    recast: bool; clarify: bool; nudge: bool; recall_gap: bool; retell: bool; praise: bool
    close: bool; goodbye: bool; smaller_question: bool; wrap_offer: bool

BUDGETS = {
  "first":     dict(clarify=1, recast_per_turn=0, nudge=0, recall_gaps_min=0, recall_gaps_max=0, retell=0, praise=1, silence_offers=2),
  "main":      dict(clarify=3, recast_per_turn=1, nudge=1, recall_gaps_min=2, recall_gaps_max=4, retell=1, praise=1, silence_offers=2),
  "round_two": dict(clarify=2, recast_per_turn=1, nudge=0, recall_gaps_min=0, recall_gaps_max=1, retell=1, praise=1, silence_offers=2),
}
ANXIETY_OVERRIDE = dict(nudge=0, recall_gaps_max=1)          # PRD 5.4.7: recasts kept, more backchannel, simpler questions

class Governor:
    def __init__(self, kind, budgets, limits, anxiety_prior):
        self.b = dict(budgets); self.c = Counters(); self.phase = "CONNECTING"; self.mode = "normal"
        self.limits = limits; self.turn_words = []           # learner words per turn in the first 2 min
        self.silences_8s = 0
        if anxiety_prior: self.enter_anxiety("prior")

    def enter_anxiety(self, why):
        if self.mode == "anxiety": return
        self.mode = "anxiety"; self.b.update(ANXIETY_OVERRIDE); self.why_anxiety = why   # logged on call_turn

    def observe_learner_turn(self, words: int, t_s: float):
        if t_s <= 120: self.turn_words.append(words)
        if t_s >= 120 and self.turn_words and median(self.turn_words) < 4: self.enter_anxiety("short_turns")

    def observe_silence_8s(self):
        self.silences_8s += 1
        if self.silences_8s >= 2: self.enter_anxiety("two_silences")

    def allowances(self, t_s: float, in_retell_window: bool, meaning_lost: bool) -> Allowances:
        b, c = self.b, self.c
        return Allowances(
            recast=b["recast_per_turn"] > 0,
            clarify=c.clarify < b["clarify"] and (meaning_lost or self.mode == "normal"),
            nudge=c.nudge < b["nudge"] and self.mode == "normal" and self.phase in ("ARGUE", "ARGUE_AFTER"),
            recall_gap=c.recall_gaps < b["recall_gaps_max"] and self.phase in ("ARGUE", "ARGUE_AFTER"),
            retell=c.retell < b["retell"] and in_retell_window and c.recall_gaps >= 1 and self.phase == "ARGUE",
            praise=c.praise < b["praise"] and self.phase in ("CLOSING", "GOODBYE"),
            close=t_s >= self.limits["close_begin_s"],
            goodbye=t_s >= self.limits["hard_end_s"] - 20 or self.phase == "GOODBYE",
            smaller_question=self.phase == "SILENT" and c.silence_offers < b["silence_offers"],
            wrap_offer=self.phase == "SILENT" and c.silence_offers >= b["silence_offers"],
        )

    def check(self, moves: dict, a: Allowances) -> list[str]:
        bad = []
        if moves.get("recast") and not a.recast: bad.append("recast")
        if moves.get("clarify") and not a.clarify: bad.append("clarify")
        if moves.get("nudge") and not a.nudge: bad.append("nudge")
        if moves.get("recall_gap") and not a.recall_gap: bad.append("recall_gap")
        if moves.get("retell") and not a.retell: bad.append("retell")
        if moves.get("praise") and not a.praise: bad.append("praise")
        if moves.get("grades") or moves.get("explains_grammar"): bad.append("never")
        return bad

    def commit(self, moves: dict):
        c = self.c
        c.clarify += bool(moves.get("clarify")); c.nudge += bool(moves.get("nudge"))
        c.recall_gaps += bool(moves.get("recall_gap")); c.retell += bool(moves.get("retell")); c.praise += bool(moves.get("praise"))
        if moves.get("retell"): self.phase = "RETELL"
        if moves.get("close") and self.phase in ("ARGUE", "ARGUE_AFTER", "CLOSING"): self.phase = "CLOSING"
        if moves.get("goodbye"): self.phase = "GOODBYE"
```

**The declare-then-speak protocol.** The host's reply begins with one line:

```
@moves {"recast":{"heard":"I go","form":"went"},"clarify":false,"nudge":false,"recall_gap":"rg2","retell":false,"praise":false,"close":false,"goodbye":false,"crisis":false,"ai_disclosure":false}
You WENT to the derby with your manager? With who else?
```

The worker buffers tokens until the first newline (about 40 tokens, 100 to 200 ms), parses the JSON, runs `check()`. On an empty `bad` list it streams the rest of the text into TTS sentence by sentence and marks the recast span for the caption. On a violation it cancels the stream, appends a system message `Do not use: nudge. Reply again.` and re-requests once (measured cost about 600 ms, expected on well under 5% of turns after prompt tuning; `violations` is a quality metric and the offline suite's first regression check). A second violation is spoken anyway and logged as `move_violation`; the call never stalls on the governor. A missing or malformed header is treated as `{}` and logged as `header_missing`.

**Timers.** `t` is seconds since the opening line started. At `close_begin_s` (390 for main) the operator note says "begin a natural close"; at `hard_end_s - 20` (460) it says "say goodbye now in one line"; at `hard_end_s` (480) the worker ends after the current TTS sentence, even mid-reply. For `first`: 60 and 90. For `round_two`: 120 and 180. The learner's ✕ sends `end_call`; the worker lets the current learner turn finish (at most 3 s), requests one host line with `goodbye` allowed only, speaks it, ends. Round two is offered on Today the next day by the client domain from `calls` (kind `main` done, no `round_two` row).

**Retell.** When the host declares `retell`, the worker sends `retell_ring {seconds: 75}` to the client (a soft ring, never red), sets the turn controller's max extension to 2.5 s for the retell turn and disables the 8 s silence offer until the first speech; the retell ends when the learner's turn ends or at 90 s, when the host simply replies.

**Interrupted call.** A call cannot resume (PRD 4 rule 4). If `web` reconnects to a room whose job has ended, or the learner returns after an abandoned call, `POST /v1/calls` creates a new call with `resumed_after_drop: true`; the bundle's opening clip is then the pre-rendered "gap" variant ("You left me hanging. Where were we?"), and the previous call's turns are still in the event log for assessment.

### 4.4 The host prompt and the request shape

The request to the host model has three layers, rendered in cache order (tools, system, messages). Layer A is identical for every learner of one host and accent, so it is cache-warm across the whole fleet; layer B is per call and warm from the second turn; the messages carry a cache breakpoint on the last learner turn so the growing history is read from cache.

```
[SYSTEM, breakpoint 1: static per host and accent, about 1,800 tokens]
You are {Mona|Karim}, co-host of "For one", on a short voice call with one listener who has just heard today's episode. {host bible, authored: values, humour, speech patterns, what you never do, stance toward the listener}
You are an AI host. If asked whether you are real, say so plainly in one short sentence and carry on. Your storylines are the show's fiction; you never claim to exist outside the show or to miss the listener.
HOW YOU TALK: English only; one or two sentences, under {max_words_per_turn} words; one question at a time; the listener should talk at least twice as much as you; never finish their sentence; never grade, explain grammar, mention progress or levels, guilt, or say you will miss them; no homework.
HOW YOU HELP (the listener must never feel tested): clarification request when meaning is lost ("Sorry, you went, or you're going?"); recast one error at most per reply, only on the target or on an error that blurred meaning, the corrected word stressed, inside a reply with its own point; one nudge per call ("Wait, yesterday you...?") then wait; recall gaps from the brief: start the line and stop; hints before answers: "how do I say X" gets a hint, the word only on a second ask; "what does X mean" gets a plain answer; absorb side-switching, rejected premises, off-topic turns and early endings without steering back to a script.
IF THE LISTENER IS IN DANGER OR DISTRESS: declare crisis in the header and say nothing else; the producer takes over.
IF THEY SAY THEY ARE DRIVING: "Call me back when you've parked. I'll be here." and declare goodbye.
OUTPUT FORMAT: first line exactly `@moves {json}` with keys recast{heard,form}|null, clarify, nudge, recall_gap (id|null), retell, praise, close, goodbye, crisis, ai_disclosure (booleans). Then a newline, then only what you say aloud. No stage directions, no markdown. The operator note before each listener turn tells you which moves are allowed; a move that is not allowed must not be used.

[SYSTEM, breakpoint 2: per call, the HostBrief rendered as text, about 700 tokens]
LISTENER: Faisal (FY-sal), he. EPISODE IN 3 LINES: ... THE QUESTION: ... PHRASES THE EPISODE PLANTED: ...
YOUR POSITION: ... PUSHBACK: ... GRAMMAR TARGET: past simple in narratives. MOVES THAT MAKE IT NECESSARY: "Walk me through exactly what happened on Saturday." ... RECAST LIST: "I go" -> "went" ... WORDS: line-up ("ask who starts") ... RECALL GAPS: rg1 "Karim said the plan was a bit too... what was the word?" (expected: ambitious) ... RETELL: "Mona missed it. Sixty seconds: what happened at the derby?" CALLBACK ALLOWED: "the manager who supports Al Hilal" (one use). NEVER MENTION: ... DAY TYPE: main.

[MESSAGES]
user: (the listener's first turn, streaming text)
system: {"note":"t=0:41 mode=normal allowed: recast clarify(3 left) recall_gap(2..4, used 0) ; not allowed: nudge retell praise close ; listener held floor: no"}   <- mid-conversation operator note, every turn
assistant: @moves {...}\nYou WENT to the derby...
user: ...
system: {"note":"t=2:14 ... allowed: retell ...","whisper":null}                                 <- the observer's slot (D14), null in the beta
```

Request parameters: `model: claude-sonnet-5-5`, `max_tokens: 120`, `output_config: {effort: "low"}`, `thinking: {type: "between_tools"}` (the host has no tools, so the reply starts at once; `effort` is `low` because the reply is one or two sentences; the 50-call test compares `low` with adaptive thinking at `low` and keeps whichever meets the latency gate with the better move-contract score), `stream: true`, cache breakpoints on the two system blocks and the last user turn. Operator notes are `{"role": "system"}` entries inside `messages`, which Sonnet 5.5 accepts without a beta header and which leave the cached prefix intact. The host never uses prefill (removed on this model family) and never uses forced tool choice. On a `refusal` stop reason (rare on this content) the worker speaks a neutral in-character line from the package ("Hang on, say that again?") and logs it.

Fallback order on a model error or a first-token wait over 1.2 s: retry once on the same model with a 1.5 s timeout; then `claude-haiku-5-5` with the same prompt; then the second vendor from `vendors.yaml` (`google/gemini-3.8-flash`) with the same prompt text rendered as a plain system prompt (no cache). The fallback used is recorded on the `call_turn` event and in `calls.vendors`.

Learner "sorry?", "slower", "again" and the Arabic equivalents in `language.repair_phrases` are matched by code on the streaming final; the operator note then says `listener did not understand: rephrase your last line more simply, shorter, no new question`, and the turn is logged as `repair_request`. Previous-track (Media Session) on the call replays the host's last TTS audio from the client's buffer and logs `replay_line {door: "call"}`; the host is not told.

### 4.5 Turn-taking: adaptive patience, hold-to-talk, backchannels, silence

**Pause profile.** Stored in the Skills store by code after each call (learner model domain writes it; this domain specifies the formula): `p = clamp(P90 of within-turn pauses over the last 3 calls, 1.0, 2.5)` where a within-turn pause is a gap between two verbatim words inside one learner turn, in seconds. A new learner has `p = 1.5`. During a call the worker adapts within the call: each time the learner resumes speech within 700 ms of the host starting to speak (a cut-off), `p += 0.25` for the rest of the call (cap 2.5); each cut-off is logged on the `call_turn` as `cut_off: true`. The adapted value is reported in `call_ended.metrics.endpoint_ms_final` so the profile converges.

**Endpointing.** The turn controller combines three signals: Silero VAD (speech or silence per 20 ms frame), the LiveKit multilingual turn detector's end-of-utterance probability on the running transcript, and the hold state.

| Condition at a silence of length `s` | Action |
|---|---|
| `s >= 1.2 s`, turn incomplete (EOU probability under 0.5), no backchannel yet in this pause, floor not held or held | play one backchannel clip (4.5 below); keep listening |
| `s >= p` and EOU probability at least 0.5 | end of turn |
| `s >= p + max_extend` (max_extend 1.5 s; during the retell 2.5 s) | end of turn regardless |
| floor held | never end the turn; backchannel allowed once per pause as above |
| `hold.up` received | 300 ms grace; if speech resumes, continue; else end of turn |
| `s >= 8 s` in `LISTENING` (the learner has not started) | `SILENT`: the governor allows `smaller_question`; after two offers, `wrap_offer` |

LiveKit's `AgentSession` is configured with `min_endpointing_delay = p`, `max_endpointing_delay = p + max_extend`, the multilingual turn detector, `min_interruption_duration = 0.5 s`, `min_interruption_words = 2`, and `allow_interruptions = true` so an open-mic learner can cut the host off with real speech but not with "mm". The hold state is applied by pausing the session's end-of-turn (the `turn-controller` flips `session.input.audio` to a buffering mode where frames still reach STT but end-of-turn is suppressed).

**Backchannels (D4).** The package holds a list per host of 8 to 10 short lines ("mm", "go on", "yeah?", "right", "okay", a breath) rendered once per host voice at casting time by the voice studio and cached under `voice.backchannel_clips`. The controller picks one at random excluding the last two, plays it on the `host` track at -6 dB, and never plays more than one per pause or more than one per 10 s. In anxiety mode the threshold drops to 1.0 s. Backchannels are logged inside the learner's `call_turn` payload (`backchannels: [{t_ms, clip_id}]`) and never count as host talk time.

**Hold-to-talk.** The pad sends `hold.down` and `hold.up` over the data channel (reliable). `hold_floor` events are logged with the duration. Holding is also how a learner reads from the planning card without being interrupted.

### 4.6 The Huh? signal on the call

On the call screen the Huh? affordance of the player maps to "repeat what you just said": previous-track on the headphones or a small ⟲ under the caption. [DECISION] It replays the host's last line from the client's audio buffer (no vendor call, no delay), logs `replay_line {door:"call", host_line_id}`, and does not inform the host; if the learner then says "sorry?" the repair path in 4.4 handles rephrasing. The learner's own Huh? taps during the call feed the teacher's difficulty dial like the player's (PRD 9.6) through the same event type.

### 4.7 Talkback to Salma

```
S down ─► client: talkback.down {t_client}     worker: freeze turn detector; mark floor held; open talkback STT stream (Soniox, languages [ar, en], code-switch on);
                                                       feed frames from (t_down - 400 ms pre-roll buffer) onward; host STT frames muted
S up   ─► client: talkback.up                  worker: finalize talkback stream (<= 400 ms); resolve (4.7.1); synthesize Salma; play on `salma` track;
                                                       send ui.talkback {text_ar, word_en, mode}; log talkback; unfreeze (floor stays held if pad is down)
```

**4.7.1 Resolution.** Code first, then one small model call.

1. Normalize the Arabic transcript; match the three package patterns for "how do you say X" (كيف أقول, وش أقول, إيش معنى بالإنجليزي ...). If X is a single token with an entry in the gloss cache's reverse index (ar→en, built by the pipeline's gloss precompute for every gloss ever produced), the candidate word is known in under 10 ms.
2. Otherwise, or when the ask is a phrase, a question about meaning, or anything else: `claude-haiku-5-5`, Salma's talkback prompt (Arabic persona excerpt, 300 tokens cached), input: the transcript, the produced-lemma list (names only), the active targets. Output schema (structured output): `{kind: "word"|"phrase"|"meaning"|"other", en: string, ar_answer: string, lemma: string|null}`. Timeout 800 ms; on timeout Salma says, in Arabic, "say it again, slower" and the ask is logged as `unresolved`.
3. Word-or-hint (D6): `mode = "word"` if `lemma not in produced_lemmas` or this is the second ask for the same lemma in this call; else `mode = "hint"` and the hint is the first sound of the word plus, when `last_session_label` exists, "you used it on {label}". The hint text comes from a template in the package, not the model.
4. Salma's line: `{ar_answer}` with the English word embedded (for example "لاين-أب... line-up"); the English share of her words follows `english_share` only in the framing, never in the word itself.

**4.7.2 Voice.** Salma's talkback uses `salma_tts` with the casting's Salma voice and `style: "close"`: the adapter maps this to the vendor's lowest-energy, intimate delivery where style tags exist, and in every case the worker applies a 3 dB level reduction and a high-shelf cut at 8 kHz on the `salma` track so she sits "closer and drier" than the host (PRD 7.3). The host track is silent during talkback because the floor is held, so no ducking is needed.

**4.7.3 Latency.** Budget under 2 s from S-up: STT finalization 300 ms, resolution 10 ms (cache hit) or 400 to 700 ms (Haiku), Salma TTS first byte 200 to 400 ms, network 100 to 200 ms. Measured `talkback_ms` on every `talkback` event.

**4.7.4 Host isolation.** The host receives nothing about the talkback (PRD 5.4.5: the audio goes to the Arabic recognizer, not the host). The learner's next English turn arrives as usual. The worker only adds `listener held floor: yes` to the operator note so the host does not comment on the pause.

**4.7.5 Logged.** `talkback {t_ms, ask_ar, kind, lemma, mode, resolved_by: "cache"|"model"|"none", talkback_ms, cost_usd}`. Talkback asks per call by lemma is a PRD 16.2 measure and a PRD 5.4.5 progress signal; the Word bank's `lookups` per lemma are updated from this event by the data domain.

### 4.8 Captions

Host captions are built from the TTS stream: when the adapter returns word timings (ElevenLabs and Cartesia do; Inworld and Gemini are verified in week 1), the client receives `ui.caption {host_line_id, words: [{w, s_ms, e_ms}], recast_span: [i, j] | null, final}` and renders word by word; otherwise one `ui.caption` per sentence as that sentence's audio starts, with the recast word bold from the header's `form` string matched in the text. The learner's words are never sent to the client as captions (PRD 5.4.8); the client does not even subscribe to the worker's learner transcription events. The Controls switch for captions lives on the client; the worker always sends them (cheap) so turning them on mid-call is instant.

### 4.9 Salma at onboarding (PRD 2.2 A3) and the first call (A7)

The same worker runs a second persona, chosen by `call.kind`. The pipeline is the same with three differences: the recognizer is the talkback configuration (Arabic plus English) on the main stream; the model is `claude-sonnet-5-5` with Salma's bible and the onboarding contract; the voice is `salma_tts`.

**First sound under 60 s.** `POST /v1/onboarding/start` (client domain) creates the pre-account learner and the room before the mic prompt; the worker's first two Salma lines are static package clips (`salma_intro_1_ar`, the AI disclosure, and `salma_intro_2_ar`, the first question) played the moment the learner's track is subscribed, which covers the 1 to 2 s of vendor websocket setup. Measured `first_sound_ms` is reported on `call_ended` for `onboarding`.

**The onboarding contract (code-enforced like the host's).** `turns_max = 8`; fields `name`, `talk_for_an_hour`, `need_english_for`; two English lines, one comprehension ("tell me what you heard, in any language"), one production ("say anything back in English"), each used exactly once and placed by the governor (after field 1 and after field 3); each field gets one re-ask then is marked `sparse`; a dated event in an answer becomes a follow-up candidate with a date. Salma's reply header:

```
@salma {"fact":{"field":"name","value":"Faisal","quote":"اسمي فيصل"}|null,"english_line":"comprehension"|"production"|null,"followup":{"text":"interview","date":"2026-11-27"}|null,"done":false}
```

The worker turns `fact` into `ui.fact_card {field, value, quote, card_id}` at once (the card appears under Salma as she hears it), and the client's ✎ and ✕ send `fact_card.edit` and `fact_card.remove`, which the worker folds into the next operator note and logs as `fact_card_edit`. "Type" mode sends `text.turn {text}` over the data channel; the worker injects it as the learner turn without STT. At `done` or turn 8 the worker emits `onboarding.intake_completed {learner_id, intake_facts, name_clip_ref, english_moments: [...]}` (the pipeline's trigger for the pilot) and ends. The name clip is the learner's turn audio for the `name` field, uploaded like any turn and referenced by `name_clip_ref` for the voice studio's name pronunciation step.

**The first call (A7).** Kind `first`: the throwing host, budgets from 4.1 (no recast, no nudge), the Salma talkback introduction played as the package clip `talkback_intro_ar` on the `salma` track before the host's opening clip ("If you're stuck, hold the S button and ask me in Arabic"), close at 60 s, end at 90 s. The host's opening line is the pilot's throw question re-asked.

Salma's Arabic variety (Gulf or neutral) is the 7.3 blind test's choice and is a `voice_casting.salma.variety` value; this domain reads it. [OPEN for Muath] see section 10.

### 4.10 Recording, verbatim re-transcription, pronunciation, deletion

**Capture.** The recorder keeps the learner's decoded PCM (48 kHz mono from WebRTC, downsampled to 16 kHz) per turn in memory. At end of turn it encodes the turn as Opus in Ogg at 24 kHz (the topology's chosen format; 16 kHz FLAC would serve ASR equally and is the swap if a verbatim vendor rejects Opus) and uploads it with SSE-C under the learner's DEK to `forone-voice/learners/{lid}/calls/{callId}/turn-{n}.ogg`, writing a `media_objects` row `{kind: "call_turn", call_id, turn_n, duration_ms, ephemeral: !voice_storage, expires_at: voice_storage ? null : call_end + 15m}`, then emits:

```python
class CallTurnAudioReady(BaseModel):   # "call.turn_audio_ready"  sender: call-worker (through api)
    learner_id: UUID; call_id: UUID; turn_n: int; media_id: UUID; event_id: UUID   # the call_turn event to update
    duration_ms: int; voice_storage: bool; is_last: bool; language: Literal["en", "ar"]
```

**`call/verbatim-turn`** (Inngest; shell in the topology, step bodies shared between this domain and the assessment domain): `verbatim_stt.transcribe(audio, language="en", disfluencies=True, word_timings=True)` through the `VerbatimRecognizer` adapter (AssemblyAI primary, ElevenLabs Scribe secondary, decided by the 30-clip test); the result updates the `call_turn` event's payload with `verbatim_text`, `words[{text, start_ms, end_ms, confidence}]`, `vendor`, `disfluencies_kept`; emits `verbatim.turn_completed`. If `voice_storage` is false the step then deletes the turn's object and marks `media_objects.deleted_at`. Concurrency 20 global; retries 2 with the secondary vendor on the second retry; a turn that still fails is marked `verbatim_failed` and its evidence is low confidence (PRD 5.4.11).

**The full recording.** When voice storage is on, the worker also mixes both sides (learner mono plus host plus Salma) into one Ogg Opus file at call end and uploads `call_full` (not ephemeral). It is what the archive plays (PRD 12.2) and what the polish card's ▶ plays by range. When storage is off, no full recording is ever written; the polish card plays nothing and shows the text (PRD 5.5).

**Say it once, shadow lines [P1], small-door voice note, then-and-now.** The client records with `MediaRecorder` (`audio/mp4` on Safari, `audio/webm;codecs=opus` on Chrome; at most 60 s for the small door, 20 s for say-it-once, 90 s per then-and-now task) and uploads to `POST /v1/calls/{id}/voicenotes` or `POST /v1/recordings` with the reference text where one exists. Every upload is a `media_objects` row under the same rules and a `call.turn_audio_ready`-shaped event (`recording.turn_audio_ready`) so the verbatim path is one function.

**Pronunciation.** `call/pronunciation-score` runs on `pronunciation.requested {media_id, reference_text}` for say-it-once and shadow lines only (PRD 10.3): `Pronunciation.score(audio, reference_text)` on Speechace (secondary Microsoft), stores `{sentence_score, word_scores[], vendor, version}` as a `say_it_once` or `shadow` event payload update. Nothing is shown to the learner; the client gets no response body beyond `202`. Dial-in audio [P1] never reaches this function.

**Deletion windows.**

| Rule | Mechanism | Backstop |
|---|---|---|
| Storage off: audio deleted when verbatim succeeds, and in any case within 15 min of call end (PRD 5.4.11) | per-turn delete in `call/verbatim-turn`; `audio/expire` (topology) at `call.ended + 14 min` deletes anything with `ephemeral = true` | S3 lifecycle on the `ephemeral/` prefix at 1 day; `retention/daily` reports leftovers |
| Revoke: all stored audio within 24 h (PRD 12.5 rule 3) | `learner/purge-audio` (topology) on `learner.consent_changed {voice_storage: false}`; a call in progress reads the flag at `call.ended` and treats the call as storage-off | key destruction on account deletion |
| Transcripts always kept | `call_turn` events are never deleted while the account exists | n/a |
| Then-and-now with storage off: kept only if the learner explicitly keeps that one (PRD 12.5 rule 2) | the client's "keep this recording" sets `media_objects.ephemeral = false` for that object only | |

The worker holds the DEK in memory only, zeroes it at job end, and never logs it; the full recording's mix happens in the worker's memory, not on disk.

### 4.11 Client-side audio (the call screen's audio contract; the screen itself is the client domain's)

| Concern | Decision |
|---|---|
| Mic | `getUserMedia({audio: {echoCancellation: true, noiseSuppression: true, autoGainControl: true, channelCount: 1}})`, requested only at A2 "Talk" or at the first Call tap (PRD 2.2 A2) |
| Playback | Two `HTMLAudioElement`s attached to the `host` and `salma` tracks with `playsinline`; the `AudioContext` is resumed in the tap handler that starts the call (iOS requires a user gesture); a 100 ms "studio" sting from the package plays on connect to prove the output route works |
| Echo | Hardware AEC through the constraints above; the worker's interruption threshold (0.5 s and 2 words) absorbs residual echo; the client additionally mutes the mic track for 150 ms after each host sentence starts when no earphones are detected |
| Earphones | Not reliably detectable on iOS; the client checks `enumerateDevices()` labels and `MediaTrackSettings.deviceId` on Chrome and suggests earphones once on the first call either way (PRD 5.4.1); the suggestion never blocks |
| Screen Wake Lock | `navigator.wakeLock.request("screen")` on call start; re-request on `visibilitychange` to visible; if the API is missing (older Safari) the screen shows a one-line notice and keeps a silent `<video>` loop playing |
| Background | On `visibilitychange` to hidden the client sends `client.hidden`; the worker waits 10 s for `client.visible`, then ends the call with `end_reason: abandoned` (iOS suspends WebRTC in the background, voice lens). The learner returns to a fresh call (4.3). `calls abandoned on the move` is computed from this reason plus motion hints |
| Headphone buttons | Media Session actions: `pause`/`play` toggles mute; `previoustrack` replays the host's last line (4.6); `nexttrack` triggers talkback for 5 s (an Ears-mode press-and-release equivalent; the S bubble still shows) |
| Route changes | On `devicechange` (AirPods connect or disconnect) the client re-attaches the audio elements; LiveKit's reconnect handles the transport |
| Bandwidth | Opus 48 kHz, 32 kbps, DTX on, FEC on; LiveKit adaptive stream off for audio (there is no video) |
| Pad and S button | Pointer events (`pointerdown`, `pointerup`, `pointercancel`) with `touch-action: none`; `pointercancel` (a system gesture) is treated as release; messages carry the client timestamp so the worker can align the pre-roll |
| Planning card | Shown by the client before connecting when `Read` is `not_started` or `skipped` (PRD 4 rule 3) with the three `planning_words` from the brief; "Ready" starts `POST /v1/calls` |
| Feed entry | The feed item's call link opens `/call/{episodeId}` which runs the same flow; the handoff time from link open to room joined is logged as `feed_to_call_ms` (PRD 16.2) |

### 4.12 The message and event protocol

**Client to worker (data channel, reliable, topic `forone.ctrl`, JSON `{v:1, t: client_ms, type, ...}`):**

| type | payload | effect |
|---|---|---|
| `hold.down` / `hold.up` | | floor held or released (4.5) |
| `talkback.down` / `talkback.up` | | talkback window (4.7) |
| `end_call` | | goodbye line then end |
| `text.turn` | `{text}` | onboarding Type mode |
| `fact_card.edit` / `fact_card.remove` | `{card_id, value?}` | onboarding fact cards |
| `client.hidden` / `client.visible` | | background handling |
| `planning.ready` | | logged; the pilot's call starts |
| `replay.host_line` | `{host_line_id}` | logged only (the client replays locally) |

**Worker to client (topic `forone.ui`):**

| type | payload |
|---|---|
| `state` | `{phase, turn: "host_speaking"|"listening"|"learner_speaking"|"floor_held"|"talkback"|"silent", t_s}` |
| `caption` | `{host_line_id, words?, text?, recast_span?, final}` |
| `talkback` | `{text_ar, word_en, mode: "word"|"hint"|"none"}` |
| `retell_ring` | `{seconds}` |
| `fact_card` | `{card_id, field, value, quote}` |
| `crisis` | `{resources_ref}` (the client shows the package's resources card) |
| `fallback_required` | `{reason}` |
| `ended` | `{end_reason}` |

**Worker to `api` (`POST /internal/events`, batched):** event rows per PRD 8.2 with `learner_id, session_id, door: "call", type, occurred_at, payload, model_version, prompt_version, cost_usd, call_id`.

```ts
type CallTurnPayload = {
  turn_n: number; speaker: "learner"|"host"|"salma"; t_start_ms: number; t_end_ms: number;
  // learner
  streaming_text?: string; streaming_words?: {w: string; s: number; e: number; c: number}[]; streaming_vendor?: string;
  verbatim_text?: string; verbatim_words?: {w: string; s: number; e: number; c: number}[]; verbatim_vendor?: string; verbatim_status?: "pending"|"done"|"failed";
  speech_ms?: number; pauses_ms?: number[]; backchannels?: {t_ms: number; clip_id: string}[]; cut_off?: boolean; repair_request?: boolean; media_id?: string;
  // host
  text?: string; moves?: object; allowances?: object; violations?: string[]; reply_latency_ms?: number; first_token_ms?: number; tts_first_byte_ms?: number;
  model?: string; fallback_used?: string|null; unsaid_text?: string|null; host_line_id?: string;
};
type CallMetrics = {                                   // calls.metrics, written at end
  connect_ms: number; first_sound_ms: number; turns_learner: number; turns_host: number;
  learner_speech_ms: number; host_speech_ms: number; host_talk_share: number;
  reply_latency_p50_ms: number; reply_latency_p95_ms: number; silence_to_sound_p50_ms: number;
  talkback_count: number; talkback_p50_ms: number; hold_count: number; hold_total_ms: number;
  silences_8s: number; cut_offs: number; barge_ins: number; anxiety_mode: null|"prior"|"short_turns"|"two_silences";
  moves: {clarify: number; recasts: number; nudge: number; recall_gaps: number; retell: number; praise: number; violations: number};
  endpoint_ms_initial: number; endpoint_ms_final: number; vendors: {stt: string; llm: string; tts: string; fallbacks: string[]};
  cost_usd: number;
};
```

Events `hold_floor {t_ms, duration_ms}`, `silence {t_ms, duration_ms, offer_n}`, `talkback` (4.7.5), `replay_line {door: "call", host_line_id}`, `crisis_activation {t_ms, trigger: "header"|"keywords", role: "host"|"salma"}`, `call_started {kind, started_by, resumed_after_drop}`, `call_ended {end_reason, metrics}`.

**Inngest events emitted by this domain:** `call.turn_audio_ready` (4.10), `call.ended {learner_id, call_id, session_id, kind, end_reason, voice_storage}`, `voicenote.received {learner_id, call_id, media_id, event_id}`, `pronunciation.requested {learner_id, media_id, reference_text, surface}`, `recording.turn_audio_ready` (same shape as the call one with `surface`), `onboarding.intake_completed`.

### 4.13 The two vendor tests

**The 30-clip recognizer test (PRD 10.14, [P0], done before 2026-11-09).** Input: 30 Milestone 0 learner clips with consent, 20 to 60 s each, with Muath's hand-tagged verbatim transcript and error tags; at least 6 clips containing an Arabic code-switch and 6 containing a pause over 2 s. `tools/call-bench recognizers --clips m0/clips --tags m0/tags` runs each clip through every candidate in both roles (streaming: Soniox, Deepgram; verbatim: AssemblyAI, ElevenLabs Scribe) and reports per vendor:

| Metric | Definition | Pass line for the role |
|---|---|---|
| Error survival | share of hand-tagged learner errors whose surface form appears unchanged in the output | verbatim: at least 0.85; streaming: at least 0.70 |
| Filler retention | share of hand-tagged fillers kept | verbatim: at least 0.80 |
| Hallucination near pauses | inserted words within 1 s of a pause over 2 s, per clip | at most 0.1 per clip |
| Code-switch handling | Arabic spans transcribed as Arabic (not dropped, not transliterated as English) | talkback stream: at least 0.8 of spans |
| WER against the hand transcript | standard | reported, not gated |
| Confidence threshold | the per-word confidence below which error survival falls under 0.8, found by sweeping | becomes `language_package.recognizer.confidence_threshold` (PRD 10.2 step 4) |
| Streaming latency | final-after-end-of-speech, p50 and p95 | streaming: p95 under 500 ms |

The winner for each role goes into `vendors.yaml`; the loser is the secondary. Recognizer error by first language is tracked from these numbers onward (PRD 16.2) by rerunning the tool monthly on new consented clips.

**The 50-call latency test (PRD 14.4 #3, [P0], staging, build week 4, rerun in week 5 and on every host prompt or vendor change).** `tools/call-bench calls --n 50 --script m0/scripted-calls` drives the staging worker from a headless LiveKit client that plays Milestone 0 learner turns (audio files) as the caller, following a script of 20 to 25 turns with realistic pauses (including mid-clause pauses of 1 to 2 s and two holds), and records per host turn `reply_latency_ms` (end-of-turn decision to first host audio frame received), `silence_to_sound_ms` (last learner speech frame to first host audio frame), `connect_ms`, `talkback_ms` for two scripted S presses, and the move-contract counters. Gates: reply latency median under 1.5 s and p95 under 2.5 s; connect under 3 s at p95; talkback p50 under 2 s; `violations` under 5% of turns; host talk share at most 40%; cut-offs at most 1 per call. The run also produces the per-call cost from `vendor_calls`. The tool keeps every run's report under `bench/reports/{date}-{git_sha}.json` so a regression is visible.

### 4.14 Vendor adapters for the live path

The interfaces are the topology's (`StreamingRecognizer.livekit_plugin`, `StreamingSpeechSynth.livekit_plugin`, `VerbatimRecognizer.transcribe`, `Pronunciation.score`). This domain adds the roles and keys it needs:

```yaml
# packages/adapters/vendors.yaml (additions)
roles:
  talkback_stt:   {vendor: soniox, secondary: deepgram, languages: [ar, en], code_switch: true}
  talkback_resolver: {vendor: anthropic, model: claude-haiku-5-5, pricing: standard}
  salma_live:     {vendor: anthropic, model: claude-sonnet-5-5, pricing: standard, fallback: {vendor: anthropic, model: claude-haiku-5-5}}
  host:           {vendor: anthropic, model: claude-sonnet-5-5, pricing: standard,
                   fallback: [{vendor: anthropic, model: claude-haiku-5-5}, {vendor: google, model: gemini-3.8-flash}]}
call:
  endpoint_ms_default: 1500
  endpoint_ms_min: 1000
  endpoint_ms_max: 2500
  max_extend_ms: 1500
  retell_extend_ms: 2500
  backchannel_after_ms: 1200
  backchannel_after_ms_anxiety: 1000
  silence_offer_ms: 8000
  interruption_min_ms: 500
  interruption_min_words: 2
  hold_release_grace_ms: 300
  talkback_preroll_ms: 400
  talkback_resolver_timeout_ms: 800
  llm_first_token_timeout_ms: 1200
  llm_retry_timeout_ms: 1500
  hidden_abandon_s: 10
  limits: {first: {close_begin_s: 60, hard_end_s: 90}, main: {close_begin_s: 390, hard_end_s: 480}, round_two: {close_begin_s: 120, hard_end_s: 180}}
  tts_stream_tfb_gate_ms: 300       # D8: a call TTS vendor must beat this at p95 in the 50-call test
  worker: {calls_per_task: 8, min_tasks: 1, max_tasks: 40}
```

Each TTS vendor's live plugin is configured with the casting's `voice_id`, `rate` (vendor rate control where supported; otherwise the host simply speaks at the voice's natural rate on the call, because resampling live audio costs latency), PCM 24 kHz output, and sentence-level chunking. Vendor-specific notes to verify in week 1: ElevenLabs streaming (Flash model, websocket with alignment) gives word timings; Cartesia gives them; Inworld's streaming timestamps and Gemini TTS's streaming first-byte latency are unverified (voice lens) and are measured by `call-bench` before the blind test is run (D8).

### 4.15 Latency budget, host reply (PRD 15)

Measured from the end-of-turn decision. The silence window `p` is the learner's and is reported separately as `silence_to_sound`.

| Stage | Budget p50 | Budget p95 | How it is held |
|---|---|---|---|
| STT final after end-of-turn | 150 ms | 400 ms | streaming partials are already in hand; only the final is awaited |
| Operator note and request build | 10 ms | 20 ms | no I/O |
| Host first token | 350 ms | 700 ms | cached prefix (A and B), `effort: low`, no thinking, `max_tokens: 120` |
| `@moves` header parsed | 120 ms | 250 ms | about 40 tokens at streaming speed |
| TTS first byte for sentence 1 | 200 ms | 400 ms | websocket pre-opened at job start; sentence flush on the first `.?!` or 12 words |
| LiveKit and network to the phone | 120 ms | 250 ms | LiveKit edge; Opus 20 ms frames |
| **Total** | **about 950 ms** | **about 2.0 s** | gates 1.5 s and 2.5 s leave margin for the governor's re-request on a few turns |

Connect: `POST /v1/calls` 100 ms, room join 500 to 1,500 ms, job accept under 500 ms on a warm task, bundle fetch under 100 ms, opening clip plays at track subscription: under 2.5 s typical, under 3 s at p95 with at least one warm worker task per environment.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detected by | Behaviour | Learner sees | Evidence |
|---|---|---|---|---|
| Room not joined within 3 s, or two pipeline errors in one call, or ICE disconnected over 5 s | client timers; worker error count | **Voice-note fallback (5.1)** | "Weak signal. Let's do voice notes." then the same argument in voice notes | thread continues; `end_reason: fallback` |
| Streaming STT vendor error or no partial for 3 s while speech is detected | worker | reopen the stream on the secondary vendor (`vendor_config`), re-feed the last 2 s from the pre-roll buffer; second failure in the call triggers fallback | nothing, or one lost half-turn | `vendors.fallbacks` |
| Host LLM slow (first token over 1.2 s) or error | worker | retry 1.5 s; then Haiku 5.5; then the second vendor (4.4) | a slightly longer pause, filled by one backchannel at 1.2 s | `fallback_used` on the turn |
| Call TTS error or first byte over 1.5 s | worker | the sentence is retried on the understudy voice and vendor from `voice.understudy`; the switch is announced on air by the pipeline next episode (PRD 7.1 rule 3) | a voice change mid-call, once; rare | `vendors.fallbacks`, `vendor.degraded` |
| Both voice vendors down | `vendor/health` | fallback to voice notes with text replies from the host (no audio) for the rest of the day | text bubbles instead of voice | logged; PRD 15 "second vendor the same day" is met by the understudy path above |
| Salma TTS down | worker | talkback answers as text in the bubble only | word appears, no voice | `talkback.mode` unchanged |
| Talkback resolver timeout | worker | Salma's package clip "قلها مرة ثانية ببطء" plays; ask logged as unresolved | | `resolved_by: none` |
| `api` unreachable | worker | events and `turn_audio_ready` spooled to `forone-voice/spool/{callId}.ndjson` (encrypted) and ingested by `retention/daily`; audio uploads go straight to S3 and are unaffected | nothing | delayed events; notes may be late |
| Postgres down | `api` | `POST /v1/calls` fails: the client offers voice notes at once (they also need `api`, so it queues them in IndexedDB and shows "will send when back") | "Weak signal" | queued |
| Worker task dies mid-call | LiveKit job failure, client sees agent leave | client offers a fresh call (4.3 `resumed_after_drop`) or voice notes | "Lost you. Call again?" | partial turns already uploaded |
| LiveKit Cloud down | client connect failure | voice notes | | |
| Verbatim vendor down | `call/verbatim-turn` retries exhaust | secondary vendor; if both fail within 15 min and storage is off, the audio is deleted and the turn is `verbatim_failed`: planning signals only, no claims | notes may show fewer cards | PRD 5.4.11 honoured |
| Learner backgrounds the app | `client.hidden` | end after 10 s as `abandoned`; a fresh call later | | counted in "abandoned on the move" |
| Learner says they are driving | package phrase list on the streaming final, and the host's `goodbye` | "Call me back when you've parked." and end | | `end_reason: driving` |
| Crisis | host header or keyword list | CRISIS state (D15): package clips in English then Arabic, resources card, `crisis_activation` logged; the session continues only if the learner chooses (the screen offers "continue" or "stop") | | SB 243 log |
| Host move violation twice | governor | spoken anyway, logged | | quality metric |
| Hard end reached mid-sentence | timer | end after the current TTS sentence | a short goodbye | `timeout_8m` |
| Cost runaway (a call over 12 minutes of vendor time, which cannot happen under the timers but could under a bug) | worker watchdog | end the job | | paged |

### 5.1 The voice-note fallback in detail

1. The client ends the live attempt, shows the line, and records a note (`MediaRecorder`, at most 90 s) with a single large button; sending uploads to `POST /v1/calls/{id}/voicenotes {media, duration_ms}`; `api` writes `media_objects {kind: voice_note}`, a `call_turn` event with `mode: voice_notes`, flips `calls.mode = voice_notes`, and emits `voicenote.received`.
2. `call/voice-note-reply` (Inngest, concurrency 1 per call): verbatim transcription of the note (the same adapter; this transcript is both the streaming and the verbatim text for this turn); the host LLM with the same system layers A and B and the thread so far, the operator note `mode=voice_notes` (no backchannels, no silence offers; the move contract still applies with the same counters, carried in `calls.metrics`); call TTS of the reply (non-streaming, the same voice); the reply audio is stored as a host `call_turn` with `media_id` and pushed to the thread; the client plays it. Each exchange takes 20 to 40 s.
3. Talkback in this mode is a text ask to Salma in the thread (`POST /v1/calls/{id}/talkback {text_ar}`) answered by the same resolver, as text.
4. The thread closes when the learner taps "done" or at the session's close; the after-session pass treats voice-note turns like call turns (lower weight for fluency because the learner could re-record, flagged `mode: voice_notes`).
5. A call that started live and fell back keeps one `calls` row; its live turns and note turns are one thread in order.

---

## 6. Cost and performance against the budgets

Estimates from list prices on 2026-10-09 (voice and AI-architecture lenses, the API reference for Anthropic models); measured cost replaces them from the first call through `vendor_calls`. Assumptions: a 6:30 main call, 25 learner turns averaging 9 s of speech, host share 35% (2.3 min, about 340 words, 1,900 characters), 3 talkback asks, cache warm.

| Item | Vendor and unit | Estimate per main call |
|---|---|---|
| Streaming STT, host stream | Soniox $0.002/min × 7 min | $0.014 |
| Streaming STT, talkback stream | Soniox, about 0.5 min | $0.001 |
| Host LLM input | Sonnet 5.5: cached reads about 90k tokens over 25 turns × $0.20/M = $0.018; cache writes about 4k new tokens × $2.50/M = $0.010; uncached about 3k × $2/M = $0.006 | $0.034 |
| Host LLM output | 25 turns × 60 tokens (header plus text) = 1.5k × $10/M | $0.015 |
| Governor re-requests | 1 per call on average, half the input again | $0.002 |
| Call TTS | Inworld TTS-2 Flash $15/M chars → $0.029; ElevenLabs Flash v2.5 $40/M → $0.076; Gemini 3.8 Flash TTS $9/M audio tokens × 3,500 tokens → $0.032 (doubling 2027-01-01) | $0.03 to $0.08 |
| Talkback resolver | Haiku 5.5, 3 × 600 input + 60 output tokens | $0.001 |
| Salma TTS | 3 × 40 Arabic characters | under $0.005 |
| Backchannels, opening line | pre-rendered | $0 live (about $0.002 at episode time for the opening line) |
| LiveKit Cloud | 2 participants × 7 min at the Ship plan's per-minute rate | about $0.01 to $0.02 [ASSUMPTION; the topology flags this rate for verification] |
| Compute | 1/8 of a Fargate task (2 vCPU, 4 GB) for 8 min | about $0.004 |
| **Live call total** | | **$0.11 to $0.17** |
| Verbatim re-transcription | AssemblyAI, 7 min of learner audio at about $0.004/min (the lens range is $0.002 to $0.017) | $0.03 at the top of the range |
| Pronunciation | Speechace $0.008 per 15 s, one say-it-once | $0.008 |
| Round two [P1] | the same pipeline at 2.5 min, no talkback | about $0.05 |
| Onboarding Salma + first call | about 4.5 min of Salma and host time; charged to the learner's first session once | about $0.10 |

Against PRD 14.5: "Call (main and round two) $0.16" holds at $0.16 to $0.22 with ElevenLabs on the call and $0.14 to $0.16 with Inworld or Gemini; "re-transcription and pronunciation $0.03" holds at about $0.035. The ElevenLabs case is the one that breaks the line, which is why D8 ties the call vendor to the episode vendor and why the blind test's "cheapest voice that passes" rule (PRD 14.5) matters here as much as for episodes. Levers in order if the measured number is high: shorter host turns (every 10% of host talk removed is 10% of TTS cost and more learner speech); Haiku 5.5 as host if the 50-call test's move-contract score holds (saves about $0.03); Inworld as the call voice with ElevenLabs as the episode voice only if a blind test says listeners cannot tell on a 6-minute call (gives up D8, needs the on-air announcement). The scale target of $0.30 to $0.35 per session needs the call at about $0.08: Haiku host, Inworld or Gemini voice, and 5-minute calls, all of which are configuration in this design.

Performance: section 4.15 for latency; capacity is 8 calls per task [ASSUMPTION from the topology, measured in the week-4 load test], 1 warm task per environment, autoscaling to 40; the beta's peak of 15 concurrent calls fits on 2 tasks. The vendor concurrency limits (Soniox and the TTS vendor's concurrent streams) are the real ceiling and are requested in week 1 for 50 concurrent streams.

---

## 7. Build plan for 2026-11-02 to 2026-12-06

The call pipeline is scheduled for week 4 in PRD 19.2, but the vendor tests (week 1 to 2) and Salma's onboarding voice (week 3) need parts of it earlier. This plan front-loads the skeleton so that nothing in week 3 or 4 is built on untested vendors.

| Week | Dates | Ships | Priority | What the Milestone 0 data lets you test |
|---|---|---|---|---|
| 1 | 2026-11-02 to 11-08 | `call-worker` skeleton on LiveKit Agents (`AgentSession` with Silero VAD, the multilingual turn detector, Soniox and Deepgram STT plugins, Anthropic LLM plugin, two TTS plugins for the two voice vendors in play, Salma TTS plugin); the `CallBundle` route returning a hand-written bundle; `tools/call-bench recognizers` run on the 30 clips, results and the confidence threshold written into the language package; `tools/call-bench calls` v0 (scripted caller from M0 audio) against the skeleton with a stub host prompt; TTS streaming first-byte measured per vendor (the D8 gate, handed to the pipeline domain before its blind test) | P0 | The 30 consented clips and Muath's tags are the test set; M0 call audio is the scripted caller's voice |
| 2 | 2026-11-09 to 11-15 | Recognizer decision frozen in `vendors.yaml`; host prompt layers A and B from M0 prompt H plus the bible drafts; the governor with budgets, the `@moves` header and re-request; operator notes; per-turn recorder and upload with SSE-C; `call.turn_audio_ready` and `call/verbatim-turn` with the verbatim adapter; 50-call run #1 (latency only); Salma persona (`salma_live`) with the onboarding contract and fact-card header | P0 | M0 call transcripts replayed through the governor to count violations before any live call |
| 3 | 2026-11-16 to 11-22 | Onboarding A3 live end to end (static intro clips, Type mode, fact cards, `onboarding.intake_completed`); kind `first` with its budgets and the talkback intro clip; captions over the data channel; the client audio contract (4.11) in `web` with the client domain; backchannel clips rendered per host voice by the voice studio; opening-line clip stored with the brief (D11) | P0 | A3 transcripts from M0 intakes become the onboarding fixture set |
| 4 | 2026-11-23 to 11-29 | The full main call: adaptive patience from the pause profile, hold-to-talk, talkback with the reverse gloss index and the Haiku resolver, word-or-hint, retell ring, silence offers, anxiety mode, timers and goodbyes, `resumed_after_drop`, repair phrases, driving phrase; voice-note fallback end to end (`call/voice-note-reply`); `audio/expire` wiring; `calls.metrics`; worker autoscaling; 50-call run #2 with the full gates; per-call cost visible in `vendor_calls` | P0 | M0's evidence on call timing (how long learners search for words) sets the first `p` distribution and the retell window |
| 5 | 2026-11-30 to 12-06 | Pronunciation on say-it-once (`call/pronunciation-score`); recordings route for the first then-and-now and the small door; crisis protocol with the package clips and keyword list; `learner/purge-audio` and deletion verification with the security domain; load test at 15 concurrent calls; 50-call run #3 after prompt tuning; end-to-end with Milestone 0 learners on staging; runbook for `/admin/vendors` failover | P0 | The M0 learners' real calls on the real pipeline are the exit evidence: measured cost per call and the latency gates |
| P1 | 2026-12-07 to 2027-01-10 | Round two (kind `round_two`, offered from Today); shadow lines with pronunciation; the dial-in experiment (LiveKit SIP ingress, 8 kHz flag `low_confidence`, no talkback, no claims); the observer slot test behind a flag; the simulated-caller half of the offline suite (PRD 6.7) built on `call-bench`; Deepgram as a hot secondary exercised weekly by a canary call | P1 | |

**Too much for one to two engineers, and the cut:** the two-track Salma audio (play Salma on the host track instead and show the bubble; loses the "closer" mix, keeps the function); word-level captions (sentence captions only; the recast word is still bold); the reverse gloss index for talkback (Haiku resolves everything; adds 400 ms, still under 2 s); in-call adaptation of `p` (keep the profile value only); the headphone-button mappings on the call; `tools/call-bench` as a CI job (run it by hand before each release); the understudy-voice mid-call switch (end the call and fall back to voice notes instead). Do not cut: per-turn upload and verbatim (notes and the deletion window depend on it), the governor (law 7), hold-to-talk (the one feature Duolingo's own research says users demanded), the voice-note fallback (PRD 15), the 50-call test (PRD 14.4).

---

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Speech-to-speech (OpenAI gpt-realtime, Gemini 3.8 Live, Nova Sonic) | No custom voice, so the host does not sound like the episode; input transcripts are approximate (the assessment domain needs the exact streaming text and the verbatim pass); per-turn re-billing makes cost follow turn count; patience is one setting per call |
| Pipecat instead of LiveKit Agents | Smart Turn is designed for English; LiveKit's turn detector covers Arabic for talkback; the topology already runs LiveKit Cloud |
| ElevenLabs Agents (the Milestone 0 call) | Hosted convenience, but the voice differs from the episode, the turn-taking is a global setting, the brief is pasted by hand, and the transcript smooths learner errors; right for a no-code pilot, wrong for the product |
| Whole-reply structured output (JSON with `moves` and `text`) | First audio waits for the JSON to close; the header line streams the same information in 100 to 200 ms |
| A separate observer model in the beta | PRD 17 excludes it; the brief already lists recasts and gaps; the slot is reserved (D14) |
| Backchannels generated by the host model | A model round trip inside the learner's pause is the latency the backchannel exists to hide |
| One recognizer stream with code-switching for talkback | Code-switch errors would leak Arabic into the host's input and into the error profile; the S button makes routing exact (PRD 0.1 row 7) |
| Transcribing the whole call after it ends | Notes within 90 s would need a 7-minute file transcribed in 60 s; the 15-minute deletion would race the transcription |
| Live `p` learned by a model | No model for L2 pauses exists (voice lens); P90 of measured pauses with in-call cut-off correction is honest and cheap |
| Dial-in as the P0 hands-free answer | 8 kHz audio, no talkback, no pronunciation; PRD makes it a P1 experiment |
| Client-side recording of the whole call (MediaRecorder) as the evidence source | Browser recording of a WebRTC call is unreliable on iOS; the worker already has the decoded frames |
| Opus-class host | Latency and cost; the host's job is short turns from a brief, not reasoning |
| Haiku-class host by default | Unproven on the recast moves; kept as the measured fallback and the scale lever |

---

## 9. Assumptions about other domains

1. **System topology.** `call-worker` on Fargate with LiveKit Cloud, `POST /v1/calls`, `GET /internal/calls/{id}/brief`, `POST /internal/events`, room naming `call-{callId}`, dispatch metadata `{callId}`, the `calls` table, `audio/expire`, `learner/purge-audio`, `vendor/health` and `/admin/vendors` exist as the topology describes. Deviations recorded here: the host's fallback chain is Haiku 5.5 first, then Gemini 3.8 Flash (the topology lists Gemini only); `calls` gains `metrics` and `bundle_version`; the `CallBundle` is compiled at `POST /v1/calls` (not only at episode time) so notebook vetoes are honoured; the worker publishes two audio tracks.
2. **Episode generation pipeline.** `CallBrief` has the fields in 02-generation-pipeline.md 4.4; the voice studio renders the opening-line clip (normal and `resumed_after_drop` variants) and the backchannel clips per host voice at casting time, and the package's static Salma and crisis clips once; the blind test admits only vendors that pass the streaming first-byte gate (D8), and `voice_casting.hosts.*.understudy` is the mid-call failover voice; the gloss precompute also writes a reverse index ar→en for talkback.
3. **Learner model, event log and data platform.** `events` accepts `call_turn` updates in place for the verbatim fields (an append-only log with one allowed late-binding update per turn event, or a second event `call_turn_verbatim` keyed to the first; either satisfies this domain, the data domain chooses); the Skills store holds `pause_profile.endpoint_ms` computed by the formula in 4.5 and the anxiety prior; the Word bank exposes the produced-lemma set for the talkback brief; `media_objects` has `ephemeral`, `expires_at`, `deleted_at`.
4. **Assessment engine.** `session/after-pass` stage 1 waits for `verbatim.turn_completed` of the last turn, not for a whole-call transcript; the recognizer confidence threshold is read from the language package where `call-bench` writes it; voice-note turns are weighted down for fluency; dial-in turns carry `low_confidence` and never feed claims; the first "then" recording arrives through `/v1/recordings` with task ids.
5. **Client app and delivery.** The call screen implements 4.11 and 4.12; the planning card, the earphones suggestion, the captions switch, the "keep this recording" control, the crisis resources card and the Today-screen round-two offer are client surfaces; the feed item's call link opens `/call/{episodeId}`.
6. **Security, privacy, consent and compliance.** `api` unwraps the DEK for the worker for the call's duration; SSE-C uploads from the worker are approved; LiveKit Cloud, Soniox, Deepgram, AssemblyAI or ElevenLabs, Speechace or Microsoft, and the TTS vendors are approved processors for audio in transit (and, for the verbatim vendor, at rest for the minutes of transcription), or replacements are named; the consent flag's semantics at `call.ended` are as in 4.10.
7. **Cost model, vendor strategy and tracing.** Every adapter call from the worker writes a `vendor_calls` row through the shared middleware with `call_id`; `prices.yaml` carries the per-minute, per-character and per-token rates used in section 6 and the 2027-01-01 Gemini row; Langfuse spans carry `call_id` and `turn_n`.
8. **Evaluation, observability and operations.** `calls.metrics` and the `call-bench` reports are the inputs for the latency, talk-share, violation and talkback dashboards; the "calls abandoned on the move" and "feed-to-call handoff" measures are computed from `end_reason: abandoned` and `feed_to_call_ms`; the weekly canary call per voice vendor is scheduled by operations.

---

## 10. Open for Muath

1. **[OPEN for Muath] The call-voice gate on the episode vendor (D8).** If the blind test's favourite voice (ElevenLabs is the likeliest, voice lens) is the only one that passes naturalness but its streaming price puts the call line at about $0.22 instead of $0.16, choose: keep sameness and accept about $0.06 more per session in the beta, or let the call use the runner-up vendor's closest voice with an on-air announcement, as Milestone 0 did. The M0 day-7 check-in ("does the different call voice bother you?") is the evidence; decide by 2026-11-15, when `vendors.yaml` freezes.
2. **[OPEN for Muath] Salma's Arabic variety and voice vendor** (PRD 18 #6). The talkback and onboarding pipeline is variety-agnostic; the blind test with 5 Saudi listeners needs to run by 2026-11-15 so the static intro and talkback clips can be rendered in week 3.
3. **[OPEN for Muath] Vendor contracts for concurrency.** Soniox, the TTS vendor(s) and AssemblyAI or ElevenLabs need paid tiers with at least 50 concurrent streams before the beta; ElevenLabs' concurrency sits on its plan tier. Approve the spend (roughly $100 to $300 a month in minimums during the beta, on top of usage) or name the cap.
4. **[OPEN for Muath] Crisis protocol lines and resources** (PRD 7.9, with counsel). The worker plays fixed package clips in English and Arabic and shows a resources card; the text, the Saudi resources and whether the keyword list may trigger on its own (false positives step the host out of the show) need counsel's review before 2026-12-07. Milestone 0's "call 911" line is a placeholder.
5. **[OPEN for Muath] Processors for audio.** The security domain lists them; the ones specific to this domain are LiveKit Cloud (media in transit), the streaming recognizer (audio in transit, no retention to be confirmed in the contract), the verbatim recognizer (audio held for the transcription job) and the pronunciation vendor (a 15-second clip). Any "no" names a replacement in section 4.14's secondary column.
6. **[OPEN for Muath] The dial-in experiment's number and telephony provider** [P1]: a Saudi number through a SIP provider into LiveKit, roughly $5 to $20 a month plus per-minute rates; it also needs the PDPL view on phone audio. Not needed before 2026-12-07.
7. **[OPEN for Muath] Haiku 5.5 as the host at scale.** This document keeps Sonnet 5.5 for the beta and makes Haiku the measured fallback. If the week-5 run shows Haiku meets the move-contract and violation gates on the M0 scripts, switching saves about $0.03 a session and is one line in `vendors.yaml`; it is the owner's call because the host's quality is the product's voice.
