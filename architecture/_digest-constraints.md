# Architecture constraints digest

Source: /mnt/project-files/PRD-v2.md (Implementation PRD v3.0, 2026-10-10), read in full; /mnt/project-files/concept-v2.md sections 7 to 10; /mnt/project-files/decisions.md. Compiled 2026-10-16 for the architecture workers. Numbers are quoted from the source, not interpreted. "PRD x.y" means PRD-v2 part x.y. Where concept-v2 differs from PRD-v2, PRD-v2 wins and the difference is noted.

PRD tagging rule (PRD header): [P0] works on 2026-12-07; [P1] works before the gate review 2027-01-10; [LATER] not built in the beta; "A feature in Parts 2 to 14 with no priority tag is [P0]." [NEW] items stand unless vetoed. "A question during the build that this document does not answer escalates before it is built" (PRD 18).

---

## 1. The twelve laws and the trust contract (PRD 1.2, 1.3)

| # | Law | Technical implication |
|---|---|---|
| 1 | No game furniture | Editor law scan (6.3 check 10) on every generated surface incl. audio, chat, email, feed notes; UI checklist; only monotonic plain-text counts (hours, words owned); no chart/percent/level component exists. |
| 2 | Hidden shape, social surface | Every door carries a pedagogical brief (targets, due words) in its data model, not just content. |
| 3 | Learner owns topic/format/cast; teacher owns pedagogy and shows reasons | Store "why this episode" reasons per episode (9.9); vetoes/additions to "working on" must re-target the same day (synchronous planner trigger). |
| 4 | Every episode complete; plot persists, obligation never | Arc state advances only on learner sessions, never on wall-clock; editor check 9 "stands alone". |
| 5 | Honesty about what it is | AI disclosure strings, "AI" mark, crisis protocol path (7.9) in every live role and the analyst. |
| 6 | Formats hijacked | Private podcast feed per learner is a first-class delivery channel. |
| 7 | Conversational in the moment, explicit afterwards | Host prompt contract with per-call counters (recasts, nudge, clarifications); no correction UI on call screen; notes generated after call. |
| 8 | Conversations end like conversations | Host closes at 6:30 to 8:00; chat closes at message 5; no homework strings (law scan). |
| 9 | Show is the gym, life is the game | "Out in the world" log store; real-life arcs; rehearsal format. |
| 10 | Text used once, language comes back | Every episode generated fresh; FSRS-style scheduler drives reuse of items, not text. |
| 11 | Finite, good portion | Allowance enforced server-side (one new episode per active day, one swap); no "next episode" endpoint or control; no autoplay. |
| 12 | No claim without proof | The claim gate (code, 10.10) is the only route from learner model to any progress statement; the proof producer receives only passed claims. |

| # | Trust promise | Technical implication |
|---|---|---|
| 1 | Never lie | Memory used only if confirmed (8.4 ladder); claims only via gate. |
| 2 | Never manipulate | Exactly three outbound message kinds (3.10); no re-engagement jobs. |
| 3 | Never hide what it is | Disclosure at start and whenever asked, by every character. |
| 4 | Prove progress honestly, incl. flat weeks | Proof templates for slow/flat/worse weeks (11.1). |
| 5 | Data is theirs | See, export (link within 1 h), delete (24 h live, 30 d backups) (12.5). |
| 6 | Told, not inferred | No external lookup about the person; sensitive classes (health, money, relationships, religion, politics) never inferred; no enrichment services. |
| 7 | A wrong memory is a bug | `wrong_memory_flag` event; immediate fact fix; metric "under 1 in 100 callbacks" (16.1). |
| 8 | Data use opt-in | Consent flag gates any use of anonymized transcripts; off by default; never audio. |

---

## 2. Numeric budgets

### 2.1 Latency and reliability (PRD 15, plus sources)

| Path | Budget | Part |
|---|---|---|
| First open to first sound (Salma) | under 60 s | 15, 2.2 A3 |
| First open to learner's first spoken English sentence | under 5 min | 15, 2.2 |
| Sample episode playable | under 30 s (streamed) | 15, 2.1 |
| Pilot playback after intake (A3 end, A4 excluded) | under 45 s | 15, 2.2 A6 |
| Pilot generation window (casting fills it) | 40 to 90 s | 2.2 A5 |
| Dropped episode start | under 2 s | 15 |
| On-demand episode (swap, return) playable | under 30 s, streamed | 15, 3.6, 3.8 |
| Call connect | under 3 s | 15 |
| Host reply after end of learner turn | median under 1.5 s, p95 under 2.5 s | 15, 14.4 |
| Talkback answer | under 2 s | 15 |
| Word sheet open | under 300 ms | 15, 5.7 |
| Salma's notes after a call | under 90 s | 15, 5.5, 10.2 |
| Chat opener | under 30 s after door opens or call ends | 15, 5.6 |
| After-session pass and teacher update | within 10 min | 15, 9.1, 10.2 |
| Tomorrow's episode | ready before drop time; batch falls back to on-demand at drop time minus 90 min | 15, 3.2 |
| Idea cutoff | 6 h before drop time, top-ranked idea used | 3.1 |
| Audio deleted, voice storage off | within 15 min of call end | 15, 5.4.11, 12.5 |
| All audio deleted after consent revoked | within 24 h | 15, 12.5 |
| Export link emailed | within 1 h | 12.5 |
| Account deletion | access ends at once; live purge 24 h; backups 30 d | 12.5 |
| Trial ended without paying | archive/notebook/export/delete for 90 days, then deletion after one email | 12.5 |
| Live voice failure | fall back to voice notes; no session lost | 15, 5.4.10 |
| Voice vendor outage | second vendor within the same day's production | 15, 14.3 |

### 2.2 Cost (PRD 1.4, 14.5, 2.1, concept 8)

| Item | Value | Part |
|---|---|---|
| Beta budget per session | about $0.60 | 1.4, 14.5, 16.1 |
| Current estimate | about $0.66 | 14.5 |
| Scale target | $0.30 to $0.35 at 10,000 learners | 1.4, 14.5 |
| Stop line | over $1.00 a session with no costed plan | 1.4, 14.5, 16.1 |
| Exit criterion 2026-12-07 | measured cost per session; costed path to $0.35 or less | 19.2 |
| Sample episode | cost ceiling $0.05 | 2.1 |
| Estimate breakdown | teacher $0.08; writer $0.07; fitter+glosses+editor $0.03; voice studio $0.18; call (main+round two) $0.16; re-transcription+pronunciation $0.03; notes+chat $0.04; analyst+memory keeper $0.04; proof share+hosting $0.03 | 14.5 |
| Session cost scope | teacher share, writing, fitting, editing, all audio, call and round two, re-transcription, notes, chat, after-session pass, a quarter of the weekly proof | 14.5 |
| Day-one levers | episodes 5 to 6 min default; batch for everything nobody waits on; cheapest voice that passes blind test | 14.5 |
| Concept stacks | floor $0.25 to $0.36 (rises to about $0.36 when Gemini doubles); recommended about $0.60; premium $1.10 to $2.00 | concept 8 |
| Price | founding SAR 349 first year (first 100); monthly SAR 89 ($19.99); yearly SAR 449 ($119); 15% VAT included; intensive about SAR 179 [LATER] | 1.4 |

### 2.3 Content, session and pedagogy limits

| Item | Value | Part |
|---|---|---|
| Sample episode | 90 s; one per device and per phone/email per 24 h | 2.1 |
| Onboarding Salma | about 3 min, at most 8 turns; 2 English lines; 1 re-ask then skip | 2.2 A3 |
| Word check | 48 items (36 real lemmas, 6 per each of 6 bands top 1,000 to 10,000, plus 12 pseudowords); stops at 75 s | 2.2 A4, 10.9.1 |
| Pilot | 2 to 3 min | 2.2 A6 |
| First call | 60 to 90 s; no recasts or nudges | 2.2 A7 |
| First three episodes | one step easy (coverage +1 point) | 2.2, 9.6 |
| Personal questions | at most 1 per session in week 1 | 2.4 |
| Ideas | 3 per day, each at most 140 chars; exactly one wildcard; at most one arc idea | 3.1 |
| Swap | 1 per day | 3.6 |
| Active day | at least half an episode played, a call started, or small door used (local calendar day) | 3.6 |
| Small door | 90 s recap; one voice note up to 60 s | 3.7 |
| Gap note | gap 7, 10 or 14 days (default 10); sent once | 3.8 |
| Return episode | after 5+ days with no session | 3.8, 9.1 |
| Rhythm | 3 to 6 days a week plus 2 spare | 3.9 |
| Re-anchoring trigger | no session within 3 h of anchor for two weeks running | 3.9 |
| Planning card | 30 s, 3 words | 4 |
| Episode length | target 5 to 7 min; hard bounds 4:00 and 8:00; default dial 6 min | 5.1, 9.6 |
| Cold open | at most 30 s; 3 s pause, nothing recorded | 5.1 |
| Scenes | 2 to 4 | 5.1 |
| Life facts per episode | at most 2 | 5.1, 6.3 |
| Speech rate | 85% to 100% of natural rate; steps of 5% | 5.1, 9.6 |
| Player speeds | 0.75x, 0.85x, 1.0x; Huh? replays at 0.85x | 5.1 |
| Feed tag | 5 s Salma, Arabic | 5.1 |
| Article length | 150 to 300 words A2; 250 to 450 B1/B2; 350 to 600 C1+ | 5.3 |
| Call | target 5 to 7 min; natural close at 6:30; end by 8:00 | 5.4.2 |
| Learner speech | 4+ min per session; host talk share at most 40% | 5.4.3 |
| End-of-turn silence | starts 1.5 s; adapts within 1.0 to 2.5 s | 5.4.4 |
| Backchannel | on pauses over 1.2 s, one per pause | 5.4.4 |
| Silence | after 8 s smaller question; after two offers, offer to wrap | 5.4.4 |
| Clarification requests | at most 3 per call | 5.4.6 |
| Recasts | at most 1 per learner turn | 5.4.6 |
| Nudge | at most 1 per call | 5.4.6 |
| Recall gaps | 2 to 4 per call (at most 1 in anxiety mode) | 5.4.6, 5.4.7 |
| Retell | once per call, 60 to 90 s ring | 5.4.6 |
| Praise | at most 1 task remark per call | 5.4.6 |
| Anxiety mode | median turn under 4 words in first 2 min, or two 8 s silences, or last call abandoned | 5.4.7 |
| Round two | 2 to 3 min, one per episode | 5.4.9 |
| Dial-in audio | 8 kHz, planning only, low confidence | 5.4.12 |
| Notes | at most 3 cards | 5.5, 10.12 |
| Chat | 3 to 5 host messages; margin note at most 1 | 5.6 |
| Grammar target / words | 1 grammar target, 2 to 4 words per session; no target more than 4 consecutive sessions | 6.1, 9.2 |
| Rewrite rounds (fitter) | at most 2 | 6.1 |
| Coverage | audio default 95% (easier 96%, harder 94%, floor 93%); text default 98% (99%, 97%, floor 96%) | 6.2, 9.6 |
| Editor fail | targeted repair + 1 recheck; then fallback episode; page a human after 3 fallbacks in 7 days | 6.3 |
| Audio re-listen | up to 2 re-synthesis attempts per line | 6.4 |
| Format rotation | tracked over last 10; no format 3 times in a row | 6.5 |
| Similarity | vs last 20 scripts; starting cosine 0.85 | 6.5 |
| Human review | 10 random episodes per learner per month | 6.8 |
| Offline suite | 30 to 50 synthetic learners | 6.7 |
| Voices | 3 candidate voices per host per accent | 7.1 |
| Salma Arabic share | season 1 at least 80% Arabic; English +about 10 points per season if speaking rose; English never above 70% | 7.3 |
| Side characters | 3 to 5 per world | 7.4 |
| Arcs | 1 to 3 weeks; at most 2 open | 7.6 |
| Season | 4 weeks; finale at first session on or after day 28 | 7.7, 11.2 |
| Error vs slip | 3 observations across at least 2 sessions | 9.2, 10.5 |
| "Working on" list | at most 3 items | 9.2, 12.3 |
| Exploration slots | 10 to 15% [LATER] | 9.2 |
| Due threshold | predicted recall below 0.85 by next drop time | 9.4 |
| Grammar spacing | every 1 to 3 days early | 9.4 |
| New words | 3 to 6 per episode; at least 80% from top 3,000 lemmas | 9.5 |
| Recall candidate | tapped twice or more | 5.7, 9.5 |
| Difficulty step | at most one step per session; Huh? rate trigger: above 2-week median by half | 9.6 |
| "Why this episode" | 2 to 4 reasons | 9.9 |
| Structure accuracy window | 14 days | 8.3, 10.6 |
| Stable | about 80% correct over 14+ days across at least 5 contexts; confirmed in next 4-weekly recording; re-check at 2, 4, 8 weeks | 10.6 |
| Then-and-now | about 3 min: 60 to 90 s retell, 60 to 90 s opinion, 8 repeat sentences | 10.9.2 |
| Claim gate noise | change exceeds about twice the metric's standard error; at least 2 data points | 10.10 |
| Calibration | 150 to 200 double-tagged samples; QWK about 0.7; tag precision at least 0.8 | 10.11 |
| External test | 20 to 30 learners, week 0 and week 8 | 10.13 |
| Recognizer test | 30 clips | 10.14 |
| Weekly proof | about 2 min; slow week about 45 s; default day 7 until proof day known | 11.1 |
| Finale | at most two measured differences | 11.2 |
| Vendor tests | 5 Saudi + 5 native English listeners; 50 scripted test calls | 14.4 |
| Invites | batches of about 50 a week from 2026-12-07 | 2.1, 19.3 |

---

## 3. Roster of roles (PRD 14.1; thirteen roles, eleven in beta)

| When | Role | Model class (PRD 14.1 / 14.3 example) | Runs | Beta |
|---|---|---|---|---|
| Before | Teacher | Strongest reasoning, batch (Opus-class; Claude Opus 5.5) | After each session (within 10 min), nightly batch, follow-up due, 5+ day gap, season boundary; triggers coalesce (9.1) | Yes |
| Before | Writer | Strong creative (Sonnet-class; Sonnet 5.5) | Per episode after pick or cutoff, batch | Yes |
| Before | Fitter | Code plus small model (Haiku-class) | Per episode, up to 2 rewrite rounds | Yes |
| Before | Editor | Mid model from second vendor plus code (Gemini Flash class; Gemini 3.8 Flash) | Per episode | Yes |
| Before | Voice studio | TTS plus recognition | Per episode: audio, read-aloud, recap, feed tag, timestamps, names, re-listen | Yes |
| Before | Scout | Small model plus search | n/a | Later |
| Live | Host | Fast mid model in voice pipeline, same voice as episode (Sonnet-class, cached brief) | Call, round two | Yes |
| Live | Observer | Small fast model | n/a | Later (concept: "Phase 2") |
| Live and after | Producer (Salma) | Conversational model with voice; strong text model for notes (Sonnet-class) | Onboarding, talkback, notes, margin note, "why", life updates, fact corrections | Yes |
| After | Analyst | Small model, fixed schema, checked by code (Haiku-class) | After-session pass 10.2 steps 1 to 2 | Yes |
| After | Memory keeper | Small model plus rules (Haiku-class) | After-session pass | Yes |
| Weekly | Proof producer | Strong text model plus voice studio | Weekly, on proof day | Yes, simple |
| Every 4 weeks | Recording rater | Calibrated model plus code metrics | Then-and-now recordings | Yes |

Chat host: Sonnet-class (14.3). Code, not AI (14.1): review scheduler, lexicon (lemmatizer, frequency list, word probabilities), gloss cache, coverage check, similarity check, claim gate, edit classifier, measures, updater, cost tracing. Live roles never write; only after-session roles write (8.1, 14.2). "Nothing in assessment runs in the live path" (10.1).

---

## 4. Stack defaults and open vendor choices (PRD 14.3, 14.4)

| Layer | Beta default | Status |
|---|---|---|
| Episode voices | Winner of blind test among Gemini 3.8 Flash TTS, Inworld TTS-2, ElevenLabs v4; batch | OPEN (Part 18 #7), weeks 1 to 2 |
| Call | LiveKit Agents pipeline: streaming STT, Sonnet-class host with cached brief, episode vendor's low-latency voice, adaptive turn detection, backchannels | Default |
| Streaming recognition | Soniox default (Arabic + code-switch for talkback), or Deepgram | OPEN, 30-clip test (concept-v2 listed "Deepgram or Soniox") |
| Verbatim re-transcription | Batch verbatim with disfluencies: AssemblyAI or ElevenLabs Scribe | OPEN, 30-clip test |
| Pronunciation | Speechace or Microsoft, known sentences only | Not tagged OPEN in Part 18; choice unstated |
| Text models | Opus-class teacher; Sonnet-class writer, host, Salma, chat; Haiku-class fitter, analyst, memory keeper; Gemini Flash class editor | Default |
| Orchestration | Durable workflow engine, direct model API calls, no agent framework; default Inngest, Temporal equivalent | Default [NEW] |
| Data | Postgres (learner model + event log; vector index only for callback search); encrypted object storage, per-learner keys for audio | Default |
| Delivery | Installable web app; private podcast feed per learner; web push | Default |
| Payments | SAR, VAT invoices, Mada, Apple Pay, Visa, Mastercard, recurring | OPEN processor (Part 18 #2, by 2026-11-16) |
| Tracing | LLM tracing tool (e.g. Langfuse), every call with cost and learner-model version | Default |
| Hosting region | Pending PDPL review | OPEN (12.6, Part 18 #3) |
| Salma's Arabic voice/variety | Gulf dialect vs neutral "white" Arabic, blind test with 5 Saudi listeners | OPEN (Part 18 #6) |
| Accounts | Apple, Google, email one-time code | Default [NEW] |

Rules: every vendor behind a thin adapter, swap is configuration; two voice vendors wired from the start; several Gemini 3.8 prices double 2027-01-01; Hume shuts voice APIs 2026-11-13 (not used). Milestone 0 calls run on ElevenLabs Agents (PRD 19.1; concept-v2 said Gemini Live). Call screen uses Screen Wake Lock; player uses Media Session API. Vendor tests (14.4): call latency gate is "median host reply under 1.5 seconds" over 50 scripted calls.

---

## 5. Data rules

**Event log (8.1, 8.2).** Append-only, never changed; source of truth; nine stores computed from it and rebuildable. Each event: learner, session, door, type, time, payload, model and prompt versions, cost. Types: `play`, `pause`, `seek`, `speed`, `replay_line`, `huh`, `transcript_toggle`, `tap`, `keep`, `mark`, `article_scroll`, `read_aloud`, `call_turn` (streaming and verbatim text, word timings, confidences), `talkback`, `hold_floor`, `silence`, `note_shown`, `say_it_once`, `shadow`, `chat_message`, `margin_note`, `idea_shown`, `idea_chosen`, `swap`, `small_door`, `fact_card_edit`, `notebook_edit`, `working_on_edit`, `claim_shown`, `consent_change`, `worth_it_answer`, `wrong_memory_flag`.

**Writers per store (8.3).**

| Store | Written by |
|---|---|
| Word bank | Code, from log and analyst |
| Structure map | Analyst, checked by code |
| Error profile | Analyst |
| Skills (incl. pause profile, reading speed) | Code |
| Interests | Memory keeper, behavior |
| Life (facts with exact quote, confidence, sensitivity, valid from, expires at, status, "don't bring up"; follow-ups) | Memory keeper; learner edits |
| Goals (can-do, season goal, anchor, rhythm) | Salma's after-session pass; learner |
| Taste | Code |
| Show canon | Analyst |

Series bible stored with learner model (7.5). Every estimate carries a range (8.3). "Models propose, code decides": model outputs are candidate updates in a fixed schema (8.1).

**Life facts (8.4).** Stored only if source quote appears word for word in verbatim transcript or chat. Ladder: said once = stored, never spoken ("I think..."); said again in another session, confirmed, or left unedited after viewing = usable; edited by learner = ground truth. Sensitive classes used only in the session raised, stored only if confirmed, never brought up first. Shelf life per fact type; expired never spoken; superseded keeps history. One follow-up per dated event. Interests decay to dormant. Corrections fixed at once and logged.

**Rebuilds (8.5).** On analyst, edit classifier or measures version change, re-run after-session pass over the log and rebuild stores; shown claims never silently retracted.

**Audio and transcripts (5.4.11, 12.5).**
- Voice storage on: call and recording audio kept, encrypted with per-learner keys, until learner deletes it or account.
- Voice storage off: deleted when verbatim re-transcription succeeds and in any case within 15 min of call end; if re-transcription not done by then, evidence kept at low confidence, no claims. 4-weekly recording follows the same rule unless kept explicitly.
- Revoke: flag flips at once; all stored audio deleted within 24 h.
- Transcripts and text always stored while account exists.
- Opt-in data use: anonymized transcripts only (no audio), off by default, never sold or used for ads.
- Cloned voice: not in beta.
- Export: learner model in plain JSON, transcripts, kept audio; link emailed within 1 h.
- Deletion: access ends at once; live 24 h; backups 30 days.
- Unpaid trial end: 90 days, one warning email, then delete.

**Security (12.6).** Encryption at rest and in transit; per-learner audio keys (key deletion deletes audio); row-level isolation per learner; only cross-learner paths: shared gloss cache and opt-in anonymized transcripts; feed URLs with unguessable token, excluded from directories, resettable. Shared ingredients (6.6): gloss cache keyed by lemma, sense, native language; host and Salma bibles; ban list; sound design.

**Consents and age (1.4, 2.2 A9).** 18+ checkbox; birth date at account creation, under-18 refused. Voice-storage consent at A9 (one checkbox). Data-use switch in Controls, default off. Crisis activations logged for SB 243 reporting (7.9).

**Compiled briefs (8.6).** Teacher: everything summarized, full due list, structure map, last 14 days. Writer: brief, up to 2 usable facts with quotes, bible excerpt, targets, words, coverage and length, ban list. Host: one page (position, pushback, necessity moves, 2 to 4 recall gaps, 3 words, one callback, nudge budget, pause profile, anxiety flag, name and pronunciation). Salma: produced-word history, active targets with evidence, verbatim call transcript. Chat host: call summary, targets, opener. Proof producer: passed claims with evidence only.

---

## 6. Priority lists

### 6.1 P0 (works 2026-12-07)
Explicitly tagged:
- 2.1 sample episode and waitlist
- 5.1 the player
- 5.5 Salma's notes
- 5.7 word sheet
- 7.9 self-harm and crisis protocol
- 10.9.2 recording the first "then" in week 1
- 10.14 recognizer test (before beta build week 2)
- 11.1 weekly proof, simple version (first-ever events, words owned, next focus, working-on list, worth-it question)
- 12.3 notebook (all sections except the tape)
- 14.4 vendor tests (build weeks 1 to 2)

Untagged in Parts 2 to 14, therefore P0:
- 2.2 first ten minutes A1 to A10; 2.3 day-2 callback; 2.4 week-1 questions
- 3.1 to 3.10 daily loop: ideas, cutoff, remix, batch with on-demand fallback, drop, Today screen, allowance, swap, small door, gap note, return episode, rhythm and anchor, three message kinds
- 4 session state machine
- 5.3 article with read-aloud; 5.4.1 to 5.4.8, 5.4.10, 5.4.11 live call (turn-taking, hold-to-talk, adaptive patience, talkback, move contract, anxiety mode, captions, voice-note fallback, recording rules); 5.6 chat
- 6.1 to 6.5 pipeline, fitter, editor's gate, audio re-listen, variety system; 6.6 shared ingredients; 6.8 human review
- 7.1 to 7.8 cast, bibles, Salma, side characters, series bible, arcs (incl. mid-season rehearsal), seasons, honesty
- 8 learner model, event log, nine stores, life-fact rules, rebuilds, compiled briefs
- 9.1 to 9.6, 9.7 to 9.9 teacher (except exploration)
- 10.1 to 10.8, 10.10 to 10.12 assessment, claim gate, calibration, correction layers (10.10: until standard error is estimated, only first-ever events and words-owned claims; 10.11 calibration is "before the paid beta")
- 10.9.1 word check
- 12.1, 12.2, 12.4 to 12.6 app structure, archive, Controls, data rules, security
- 13 language package ar to en (configuration, not code)
- 14.1 to 14.3, 14.5 roster, memory rules, stack, cost tracing from the first learner
- 1.4 payments, web push, Screen Wake Lock, 18+ gate

### 6.2 P1 (before 2027-01-10)
- 1.4 / 5.4.12 dial-in phone number experiment
- 5.2 shadowing
- 5.4.9 round two
- 6.7 offline test suite
- 10.9.2 then-and-now comparison in the week-4 finale
- 10.13 external test (default Duolingo English Test)
- 11.1 full weekly proof (gated fluency and accuracy claims once standard errors exist)
- 11.2 season finale
- 12.3 the tape
- 19.3 also lists "the full claim gate"

Note: the 14.5 cost table includes round two ($0.16 "Call (main and round two)") although round two is P1.

### 6.3 LATER (for boundary-setting)
Scout and news digests (6.6, 14.1); observer (14.1); exploration slots (9.2.7); guest hosts (7.7.5); character creation, chassis, user-created hosts (7.10); cloned voice (12.5.6); intensive plan (1.4); year-in-review (11.3); rehearsal on demand (0.1 row 1); voice-triggered talkback (0.1 row 7); full Part 17 list.

---

## 7. The five build weeks (PRD 19.2)

| Week | Start | Build |
|---|---|---|
| 1 | 2026-11-02 | Vendor tests (14.4, 10.14); event log and learner-model schema; lexicon and scheduler; language package skeleton; cost tracing |
| 2 | 2026-11-09 | Teacher, writer, fitter, editor and voice studio end to end for test learners; gloss cache |
| 3 | 2026-11-16 | Onboarding A1 to A10 and Salma; player; word sheet; feed; drop notifications; payments |
| 4 | 2026-11-23 | Call pipeline with talkback, hold-to-talk, adaptive patience; voice-note fallback; Salma's notes; chat |
| 5 | 2026-11-30 | After-session pass, memory keeper, notebook, Controls, simple weekly proof, first then-and-now recording, data rules, crisis protocol; sample-episode landing page; end-to-end run with Milestone 0 learners |

Exit 2026-12-07: every P0 works; measured cost per session; costed path to $0.35 or less. Beta 2026-12-07 to 2027-01-10: about 50 invites a week into 7-day trials; P1 items ship during it; switch to native early if many calls abandoned on the move or feed-to-call handoff loses most learners (19.3). Milestone 0 (2026-10-12 to 2026-11-01) hands the beta: first calibration set, 30 recognizer clips, test-retest pairs, similarity threshold, first ban list, evidence on call timing and notes (19.1).

Sequencing tensions visible in the source (not resolved here): notes (week 4) need verbatim re-transcription and the analyst's first stages, which the after-session pass delivers in week 5; payments land in week 3 while the processor decision is due 2026-11-16 (the same day); the 10.14 test must finish "before the beta build's second week".

---

## 8. Part 18 open items

| # | Item | Needed by | Who |
|---|---|---|---|
| 1 | Who writes Karim, Mona and Salma bibles | 2026-11-02 (drafts for M0) | Muath |
| 2 | Legal entity and payment processor (SAR, VAT invoices, Mada, Apple Pay, cards, recurring) | 2026-11-16 | Muath |
| 3 | Legal review: PDPL, hosting region, SB 243, consumer subscription rules | before 2026-12-07 | Muath with counsel |
| 4 | Trial with or without card (PRD: without; payment asked on day 7) | before 2026-12-07 | Muath |
| 5 | Recruitment fallback (pair moves; Part 13 moves with it) | M0 week 1 | Muath |
| 6 | Salma's Arabic variety | build weeks 1 to 2 | Blind test |
| 7 | Episode voice vendor, streaming and batch recognizers | build weeks 1 to 2 | Tests 14.4, 10.14 |
| 8 | English Grammar Profile commercial permission, or other inventory | build week 2 | Muath |
| 9 | External test choice (default DET) | 2026-12-07 | Muath |
| 10 | Similarity threshold and recognizer confidence threshold | end of M0 | Data |
| 11 | Private feed support in podcast apps Saudi learners use | first beta cohort | Observation |

Also flagged OPEN elsewhere: crisis-protocol details pending legal review (7.9); 12.7 VAT registration and Saudi refund rules.

---

## 9. Part-number index: what each part requires of the architecture

- **Part 2:** streamed 90 s sample (under 30 s, $0.05, 24 h rate limits); waitlist answers carried into onboarding; low-latency onboarding (Salma under 60 s, live fact cards, pilot under 45 s, 60 to 90 s first call); account only after first call.
- **Part 3:** per-learner scheduler on local drop time and active-day logic; cutoff at drop minus 6 h; batch generation with on-demand fallback at drop minus 90 min; feed publish plus one web push; streamed on-demand swap and return; gap-note timer; three message kinds only.
- **Part 4:** door and session state model; indefinite position persistence; one open session; close on next publish; calls not resumable.
- **Part 5:** word-synced player with sentence replay and Huh?; synced read-aloud; LiveKit call with hold-to-floor, adaptive end-of-turn, backchannels, talkback to an Arabic-capable recognizer, captions, voice-note fallback; notes under 90 s; chat threads; word sheet under 300 ms from precomputed glosses.
- **Part 6:** durable workflow steps with timeouts and retries; code checks plus cross-vendor editor; fallback episode; human paging; embedding similarity vs last 20 scripts.
- **Part 7:** authored bibles as read-only package content; voice swap and rename; series bible, arc and season state; on-air announcement of voice or vendor changes; crisis detection and logging.
- **Part 8:** append-only event log with versions and cost; nine derived stores with ranges; quote-verified facts; full rebuild; per-role compiled briefs.
- **Part 9:** coalescing event and nightly triggers; six-factor targeting; FSRS-style scheduler; difficulty dials; rule-based fallback brief.
- **Part 10:** after-session pass off the live path within 10 min; claim gate in code with evidence links; pinned rating model per 4-week window; calibration re-run on model change.
- **Part 11:** weekly per-learner proof job (about 2 min audio from gated claims only) into app and feed; finale on or after day 28 (P1).
- **Part 12:** three-tab RTL app; archive; notebook edits written as events; Controls; export, deletion and retention jobs; per-learner keys, row-level isolation, tokenized feed URLs.
- **Part 13:** all language-specific material as one configuration package; ar to en built through it.
- **Part 14:** eleven beta roles; read-only live roles; LiveKit, Inngest, Postgres, encrypted object storage, tracing; adapters with two voice vendors live; cost per role, vendor, learner.
- **Part 15:** the budgets in section 2.1; same-day voice-vendor failover.
- **Part 16:** instrumentation for every gate and health measure from day one; none of it shown to the learner.
- **Part 17:** nothing may depend on observer, scout, native apps, multiple pairs or voice-triggered talkback.
- **Part 18:** keep voice vendor, recognizers, payment processor, hosting region, inventory source and Salma's voice swappable until settled.
- **Part 19:** the five weeks in section 7; import Milestone 0 artifacts; exit needs measured cost and a costed path to $0.35.
