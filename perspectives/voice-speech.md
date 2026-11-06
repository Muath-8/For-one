# For one: the voice and speech lens

As of 2026-10-09. Published doc: https://claude.ai/code/artifact/935520f6-7f66-4c6f-8fcc-80a5aca3807f . Prices are list prices read from vendor pages on that date unless marked "unverified". Lens author: the voice and speech technology thread, one of eleven perspectives for the synthesis. Builds on the first rethink (https://claude.ai/code/artifact/21c354e1-9b24-4fcd-bb44-dca39f26d86b) and does not repeat it.

## Decisions only Muath can make

| # | Decision | My recommendation | Alternative | Why it matters |
|---|---|---|---|---|
| 1 | Which target language first | English as the target (for example English for Arabic speakers) | Spanish, French or another target | Every voice tool is strongest in English: voices, transcription of accented speech, and pronunciation scoring (prosody scoring is US English only at Microsoft; Speechace covers only English, French and Spanish). Any other target loses part of the "voice reveals" layer at launch. |
| 2 | How much of the session budget goes to voice | Value voices (about $0.30 to $0.55 a session for all audio), chosen by a blind listening test against a premium voice | Premium voices (about $0.75 to $0.85 a session) | Voice is the largest cost line in a session. At $12 to $20 a month only the value stack leaves room for the text models. |
| 3 | When a learner declines voice storage, may the show still analyse the call audio for a few minutes and then delete it | Yes, disclosed in one plain sentence at the consent step | Analyse only the live transcript | The live transcript is not verbatim enough to build an error profile. A second, careful pass over the audio is what makes the learner model accurate. |
| 4 | Should the show ever speak in the learner's own cloned voice ("hear yourself say it fluently") | Not in beta; test it later as opt-in | Offer it from launch | It is possible today and has early evidence, but it is the most intimate use of their data the product could make. |

If you answer only one, answer #1.

## The short version

- Two-host audio good enough to pass for a real podcast is a solved problem in English and the major languages, at about $0.05 to $0.50 for an 8-minute episode. Quality in smaller languages and dialects is unproven and must be judged by native listeners.
- The live call is solvable with today's tools but not with default settings. Default turn detection waits 0.5 to 0.8 seconds of silence. Learners pause mid-sentence for about 0.75 seconds on average, so out of the box the host will cut them off.
- Transcription is the hidden weak point. Default speech-to-text drops "uh" and "um" and can quietly fix the learner's grammar, which erases exactly the evidence the learner model needs.
- Fluency (speed, pauses, fillers) can be measured reliably from timestamps. Word-level pronunciation can be scored moderately well. Phoneme-level diagnosis in free conversation, and reading the learner's emotions from their voice, are not reliable yet.
- Recommended: generate episodes offline in batch, run the call as a pipeline (speech-to-text, then a language model, then the host's own voice) rather than a single speech-to-speech model, and re-transcribe every call verbatim afterwards for the learner model.

## Listening: the episode voices

Naturalness is no longer the constraint. On the Artificial Analysis speech arena (blind human votes, mostly English), the top five as of today are ElevenLabs v4 Turbo (1329), ElevenLabs v4 (1326), Qwen-Audio-3.1-TTS-Plus (1298), Cartesia Sonic 3.6 (1281) and Gemini 3.8 Flash TTS (1275). The gap between first and fifth is small; the price gap is about 5 times.

| Option | Two hosts in one request | Word timing for the synced transcript | Languages | Cost of an 8-minute episode |
|---|---|---|---|---|
| Gemini 3.8 Flash TTS | Yes, 2 speakers, style per turn | Not documented; align afterwards | 130+ | about $0.11 now, $0.055 in batch; prices double on 2027-01-01 |
| Gemini 3.8 Flash-Lite TTS | Yes | Not documented | 100+ | about $0.07 |
| Inworld TTS-2 | Per turn | Yes | 200+ claimed | about $0.16 ($0.10 Flash) |
| Cartesia Sonic 3.6 | Per turn | Word and phoneme level | 44 | about $0.25 to $0.42 |
| ElevenLabs v4 (Text to Dialogue) | Yes, up to 10 voices, about 2,000 characters per request | Per character, per speaker | 90+ | about $0.52 list ($0.26 on v4 Turbo) |
| OpenAI gpt-4o-mini-tts | No | Not documented | Voices "optimized for English" | about $0.12 (unverified) |

What this means for the episode:

- Episodes can be made overnight, so they qualify for batch pricing (half price at Google). Only a remix or an unpredicted pick needs on-demand generation.
- The speaking rate becomes a teaching dial. The planner can generate the episode a little slower for one learner and at native speed for another. Natively slower speech sounds more natural than a player slowing audio down (my judgment, not tested).
- Word timestamps give three features almost for free: the synced transcript, "replay this sentence", and "tap to hear this word", cut from the episode audio itself instead of a new synthesis.
- Expressive tags (laughs, sighs, whispers, interruptions) are what make banter feel like a show. ElevenLabs v4 and Gemini both support them.
- Hume, a well-known expressive voice vendor, is shutting down its voice APIs on 2026-11-13. Vendor risk is real, so the voice layer should sit behind one internal interface.
- Leaderboards are English-heavy. No vendor publishes per-language quality. Before choosing, have 5 native listeners rate the same script from 3 vendors in the launch language, blind.

## Speaking: the live call

### Two ways to build it

1. Speech-to-speech: one model hears audio and speaks audio (OpenAI gpt-realtime-2.1, Gemini 3.8 Live, Amazon Nova 2.5 Sonic). Lowest latency and the most natural prosody.
2. Pipeline: streaming speech-to-text, then a language model that writes the host's reply as text, then the host's own voice. Orchestrated with LiveKit Agents or Pipecat.

| What the call needs | Speech-to-speech | Pipeline |
|---|---|---|
| Recasts that are planned and audible | Prompt only. The model can "understand through" an error and never recast it. | The reply is text first, so a small error-spotter can mark the error and the host can stress the corrected word. |
| A record of exactly what the learner said | Weak. Both OpenAI and Google say their input transcript is approximate and can differ from what the model heard. | The transcript that drives the reply is the one that is logged. |
| The host sounds the same as in the episode | Only with Gemini, whose Live voices are the same set as its TTS voices. OpenAI and Amazon use their own presets. | Yes, with the same voice ID from ElevenLabs, Cartesia or Inworld. |
| Patience with slow speakers | One setting per call: OpenAI semantic VAD "low", Gemini silence duration, Nova "LOW" (2.0 s). | Most tunable: per-user adaptive endpointing (LiveKit), prosody-based turn models (Pipecat Smart Turn, 23 languages), explicit timeouts (Deepgram Flux, 0.5 to 60 s). |
| Latency | Best | About 1.1 to 1.5 s is achievable |
| Cost of a 5-minute call (estimate) | about $0.15 (OpenAI mini) to $0.47 (OpenAI full); Gemini about $0.20 to $0.25 | about $0.12 to $0.20 self-run; $0.38 to $0.65 on managed platforms |

My recommendation: a pipeline for the beta, because the call is where the teaching happens and the pipeline is the only design where corrections and evidence are under the product's control. Use Gemini 3.8 Live for Milestone 0, where speed of building matters more and it keeps the episode's voices.

### Turn-taking is a teaching problem, not only a latency problem

- Learners pause inside sentences far more often than native speakers (in one storytelling task, almost three times the mid-clause pause rate) and for longer: about 756 ms on average against 523 ms (Huensch 2023). Many single pauses are much longer than the average.
- Default end-of-turn silence is 500 to 800 ms (Gemini recommends 500 to 800 ms, default about 800 ms; OpenAI's example is 500 ms). With defaults, the host will interrupt learners while they are building a sentence, which is the moment that matters most.
- A June 2026 study of 78 German learners talking to gpt-realtime found learners took fewer, longer turns, held less of the floor (37% against 48% with a human partner), and needed longer to start speaking (0.61 s against 0.32 s).

Design rules that follow:

- Patience is a hidden difficulty setting. The learner model stores each person's pause profile and the call adapts to it (adaptive endpointing exists in LiveKit today).
- Fill the wait with a backchannel ("mm", "yeah?") at about 300 ms so the learner knows the host is listening. That hides the extra latency patience costs.
- Short host turns. The host should speak less than the learner; the rethink's concern about too little speaking time is partly a turn-taking setting.
- A "hold on, I'm thinking" gesture (holding a button, or saying a set phrase) for lower levels.
- Track learner talk share per call, and treat it as a quality metric for the host.

### The phone, the bus and the locked screen

The rethink proposes calling hands-free on the commute. In a mobile web app, iOS Safari suspends WebRTC audio when the screen locks or the browser goes to the background (Apple developer forum, February 2025, no fix announced). So a web-only v1 cannot hold a call with the phone in a pocket. Options: keep the screen on during the call (acceptable for 5 minutes), offer a real phone number that the learner calls (works locked and in the car, but phone audio is 8 kHz, which hurts transcription and rules out pronunciation scoring), or move calls to a native app later. Test the phone-number version in Milestone 0; it costs almost nothing and fits the call-in format literally.

## Hearing the learner: transcription

- Accented speech is still harder: on read L2 English, the best systems make about 5 to 6% errors against under 1% for native speakers; on spontaneous L2 speech, 6 to 10% (McGuire 2025, L2-ARCTIC).
- Default transcription erases learner evidence. Deepgram and AssemblyAI drop fillers unless a flag is turned on. Whisper deleted most disfluencies and sometimes rewrote the learner's grammar. Whisper-class models also invent phrases in about 1% of transcripts, more often around long pauses, which learners produce.
- No vendor publishes a test of whether its model keeps learner grammar errors. This has to be tested on recordings of real learners before the error profile is trusted.
- Learners switch into their native language mid-sentence. Code-switching support varies: Soniox, Gladia and AssemblyAI Universal-3.6 claim it broadly; Deepgram's covers 10 languages and not Arabic.
- Transcription is cheap: $0.002 to $0.017 a minute.

Recommendation: two transcripts per call. A fast streaming one drives the conversation. After the call, the stored audio is re-transcribed by a careful batch model in verbatim mode (fillers, false starts and self-corrections kept), and that transcript feeds the learner model. Cost: about $0.03 a call. This is why decision #3 matters.

## What a learner's voice reveals

| Signal | How it is measured | Reliable today? | Use in For one |
|---|---|---|---|
| Fluency: speed, pause ratio, mid-clause pauses, fillers | Word timestamps from a verbatim transcript | Yes | The best progress measure for the weekly proof and the 4-week speaking sample. Mid-clause pausing is the clearest single marker that separates L2 from L1 speech. |
| Grammar errors | Language model over the verbatim transcript | Moderate, if the transcript is faithful | The error taxonomy and target queue in the PRD |
| Vocabulary actually used | Lemmas in the transcript | Yes | "Words you now own" |
| Recast uptake: did the learner repeat the corrected form? | Compare the host's recast with the learner's next turn | Yes, from transcripts | Tune correction strength per learner. This is the measure the classic recast research used. |
| Self-corrections | Verbatim transcript | Yes | A sign the learner is noticing their own errors |
| Pronunciation, sentence and word level | Dedicated engines (Microsoft, Speechace, SpeechSuper) | Moderate: correlation with human raters about 0.7 to 0.8 per sentence, 0.6 per word; better with a known script | The polish card ("say it once") and the speaking sample |
| Pronunciation, individual sounds in free speech | Same engines, or fine-tuned audio models | Weak: about 0.38 correlation at phoneme level | Do not show it to learners |
| Pronunciation judged by a general audio model (GPT-4o, Gemini) | Prompt | Weak: about 0.47 correlation, 41 to 48% of answers unusable | Not for scoring |
| Emotion, confidence, anxiety | Voice tone | Not reliable; in natural conversation even human raters barely agree | Leave it out; it also strains the trust contract |

Pronunciation costs: Speechace $0.008 per 15 seconds; Microsoft's add-on price did not render (about $1 an hour, unverified). The PRD excludes pronunciation scoring from v1. I would keep it out of the call but use it on the polish card, where the learner says one known sentence. That is the setting where scoring is most reliable, and it gives the learner a moment of "I said it right".

A possible later feature: the "golden speaker". A research tool synthesized a learner's own voice with a native accent as their pronunciation model; practising with it improved fluency and comprehensibility (Ding et al. 2019). Voice cloning from 10 seconds of audio makes this cheap now. It is decision #4.

## What is not possible yet

- Phoneme-level pronunciation diagnosis in free conversation.
- A guarantee that transcription keeps the learner's errors. It must be tested per vendor and language.
- Prosody (stress, intonation) scoring outside US English at Microsoft.
- Turn detection trained on learner hesitation. Patient settings and adaptive delays exist; a model for L2 pauses does not.
- Speech-to-speech models speaking in a custom voice. OpenAI, Google and Amazon offer presets only.
- Reading a learner's emotional state from their voice reliably.
- Even quality across all languages and dialects. Launching in "every language the provider supports" would ship unknown quality in most of them.
- Background voice calls in a mobile web app on iPhone.
- Predictable speech-to-speech cost: developers report Gemini Live re-bills the whole conversation on every turn (not officially documented), so cost follows the number of turns rather than minutes.

## Recommended stack

| Role | Milestone 0 (hand-made, 10 to 15 people) | Beta |
|---|---|---|
| Episode audio | Gemini 3.8 Flash TTS, two speakers | Winner of a blind native-listener test between Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4, generated overnight in batch |
| Word timing | Forced alignment of the known script (open-source aligner, or a cheap timestamped transcription) | Same, or the vendor's own timestamps |
| Live call | Gemini 3.8 Live with the episode's voices, silence duration set long (1.2 to 2 s) | Pipeline on LiveKit Agents: Deepgram Flux or Soniox streaming transcription, a fast language model as the host with an error-spotter step, the episode vendor's low-latency voice (ElevenLabs v4 Turbo, Cartesia or Inworld), adaptive turn detection and backchannels |
| Verbatim transcript for the learner model | Batch re-transcription with fillers on (AssemblyAI with disfluencies, or ElevenLabs Scribe v2), checked by hand | Same, plus a per-language test that learner errors survive transcription |
| Pronunciation | None | Speechace or Microsoft on the polish card only (known sentence) |
| Fluency measures | Computed from timestamps | Same, stored per call in the learner model |
| Fallback | Voice notes | Voice notes; phone-number dial-in as an experiment |

## What it means for format and cost

Estimated voice cost per session: a 7-minute episode, a 6-minute call, verbatim re-transcription and one pronunciation check. Text model costs are not included.

| Stack | Voice cost per session | Per month at 25 sessions |
|---|---|---|
| Google: Gemini TTS in batch plus Gemini Live | about $0.30 to $0.40 (call cost uncertain) | about $8 to $10 |
| Pipeline with value voices (Inworld or Cartesia) | about $0.30 to $0.55 | about $8 to $14 |
| Pipeline with premium voices (ElevenLabs v4 and v4 Turbo) | about $0.75 to $0.85 | about $19 to $21 |
| OpenAI gpt-realtime-2.1 for the call | add about $0.30 over the pipeline | |

Format implications:

1. Episodes are cheap; calls are the expensive and valuable minutes. Spend on the call, save on the episode with batch generation.
2. Shorter host turns raise the learner's speaking time and lower the voice bill at the same time.
3. The call should be one-tap, screen-on, earphones-in for v1 web; truly hands-free needs a phone number or a native app.
4. Every voice minute should be logged with its cost per vendor from day one (the PRD already requires cost telemetry). Prices move both ways: Google's double on 2027-01-01, ElevenLabs runs promotions, and one vendor is closing.
5. The voice layer sits behind one internal interface so that switching vendors per language is configuration, matching the PRD's language-package rule.

## Sources

Voices and prices
- Artificial Analysis speech arena: https://artificialanalysis.ai/text-to-speech/leaderboard
- ElevenLabs models: https://elevenlabs.io/docs/overview/models ; API pricing: https://elevenlabs.io/pricing/api ; Text to Dialogue timestamps: https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert-with-timestamps ; Agents pricing: https://elevenlabs.io/pricing/agents
- Gemini API pricing (TTS and Live): https://ai.google.dev/gemini-api/docs/pricing ; speech generation: https://ai.google.dev/gemini-api/docs/speech-generation ; Live guide: https://ai.google.dev/gemini-api/docs/live-guide
- OpenAI pricing: https://developers.openai.com/api/docs/pricing ; realtime VAD: https://developers.openai.com/api/docs/guides/realtime-vad ; realtime transcription: https://developers.openai.com/api/docs/guides/realtime-transcription
- Cartesia pricing: https://cartesia.ai/pricing ; Inworld pricing: https://inworld.ai/pricing
- Hume sunset notice: https://dev.hume.ai/docs/text-to-speech-tts/overview
- Amazon Nova Sonic turn-taking: https://docs.aws.amazon.com/nova/latest/nova2-userguide/sonic-turn-taking.html
- Gemini Live per-turn billing report (forum): https://discuss.ai.google.dev/t/does-gemini-live-native-audio-bill-cumulative-prompt-tokens-on-every-turn-cost-seems-to-scale-with-turn-count-not-call-duration/173248

Transcription and turn-taking
- Deepgram pricing: https://deepgram.com/pricing ; filler words: https://developers.deepgram.com/docs/filler-words ; Flux configuration: https://developers.deepgram.com/docs/flux/configuration
- AssemblyAI pricing: https://www.assemblyai.com/pricing ; filler words: https://www.assemblyai.com/docs/pre-recorded-audio/filler-words
- Soniox: https://soniox.com/pricing ; Speechmatics formatting: https://docs.speechmatics.com/speech-to-text/formatting
- LiveKit turn detection: https://docs.livekit.io/agents/build/turns/ ; Pipecat Smart Turn: https://github.com/pipecat-ai/smart-turn
- Twilio voice-agent latency guide: https://www.twilio.com/en-us/blog/developers/best-practices/guide-core-latency-ai-voice-agents
- McGuire 2025, ASR on L2-ARCTIC: https://arxiv.org/pdf/2503.06924
- LearnerVoice (Interspeech 2024): https://arxiv.org/abs/2407.04280v2
- Careless Whisper (FAccT 2024): https://arxiv.org/abs/2402.08021v2
- Huensch 2023, mid-clause pausing in L1 and L2: https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/effects-of-speaking-task-and-proficiency-on-the-midclause-pausing-characteristics-of-l1-and-l2-speech-from-the-same-speakers/FFE4407BEAF2A0E55D4D797C9AFE80DD
- Learners talking with a realtime voice model (2026): https://arxiv.org/html/2606.22225v1
- Prosody for end-of-turn detection (2026): https://arxiv.org/abs/2609.11066
- iOS Safari background WebRTC: https://developer.apple.com/forums/thread/774239

Pronunciation
- Microsoft pronunciation assessment: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment ; limitations: https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/speech-service/pronunciation-assessment/characteristics-and-limitations-pronunciation-assessment
- Speechace plans: https://www.speechace.com/api-plans ; SpeechSuper: https://www.speechsuper.com/pricing.html
- GPT-4o pronunciation scoring on Speechocean762: https://arxiv.org/html/2503.11229v1
- Fine-tuned audio model scoring: https://arxiv.org/html/2509.15701
- Gemini as a conversation judge (2026): https://arxiv.org/html/2607.07985v1
- Golden Speaker Builder, Ding et al. 2019: https://dr.lib.iastate.edu/engl_pubs/266
