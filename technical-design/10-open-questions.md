# 10. Open questions and contradictions

*Found while writing this design on 2026-11-06. Items 1 to 8 are contradictions between the architecture documents (written 2026-10-16 to 10-21, before Muath's 2026-10-23 answers) and the decisions as they now stand; the architecture files were not edited. Items 9 onward are decisions this design still needs. "TDD stance" is what this design does meanwhile.*

## A. Contradictions with the architecture documents

| # | Where | The contradiction | TDD stance |
|---|---|---|---|
| 1 | `architecture/05 §4.7`, `06 §4.3 NotesDoc`, `01 §4.3 session/after-pass stage 1` | The architecture builds Salma's after-call notes (new-for-you, **polish**, reached-for cards) and a chat **margin note**. Decision 3 (2026-10-23, "teaching is invisible") dropped the after-call correction notes, the polish card and the margin note from the first version; PRD-v2 v3.1 says "no notes after calls". | Tables and stage-1 code kept behind `notes.enabled = off` and `chat.margin_note = off`; the evidence path still runs for the teacher. **Muath decides**: keep notes off, or allow a non-corrective "new for you" card only. |
| 2 | `architecture/01 §4.2 learners.tz default 'Asia/Riyadh'`, `package_ar_en` everywhere, Arabic-only Salma, SAR prices | Decision 1 removed the launch country and opened languages by the five-check gate. | `tz` has no default; `native_lang`/`target_lang` columns; `packages/language/<pair>/` with `ar-en` first; USD list prices. Every Arabic string in the architecture is read as the `ar-en` package's content. |
| 3 | `architecture/01 episodes unique (learner_id, local_date, kind)`, PRD "one new episode per active day" | Decision 2 sells plans of 1, 2 or 3 new episodes a day. | `episodes.slot` added; allowance = `subscriptions.episodes_per_day` checked by `api`; `TodayDoc.next_slot`. **Open**: how a second episode interacts with "one open session" and the evening pick (this design: the next slot's idea is picked right after a session is done; the previous session closes when the next episode is started, not published). Needs a PRD rule. |
| 4 | `architecture/08 §6.1` cost model counts round two and notes/margin note in the $0.638 per session | With notes off and round two P1, the beta estimate falls by about $0.03 to $0.04; the Gemini doubling on 2027-01-01 adds about $0.18 on the Gemini voice stack. | Re-run `tools/cost-model` after decision 1 on notes; the understudy voice choice should be made against post-doubling prices. |
| 5 | `architecture/03 §4.3` "Rejected: deferring RLS" vs `04` roles; `01 episodes.state` vs `02 status` enums | Two overlapping enums for episode state. | One enum in 01 §3.2 of this design (`requested ... closed, prewritten, failed, superseded`, `streaming` a flag). The integrator renames one column. |
| 6 | `architecture/03 §4.10 CallTurnAudioReady` has `turn_n, media_id, event_id` and "updates the call_turn event's payload"; `01 §4.3` and `04 §4.1` say events are append-only and the verbatim is a separate `call_turn_verbatim` event with `turn_index, media_object_id` | Field names and the update-vs-append rule disagree. | Append-only wins: `call_turn_verbatim` is its own event; field names follow 01 (`turn_index`, `media_object_id`). |
| 7 | `architecture/03 §4.1 end_reason` adds `abandoned, driving, fallback`; `01` has `timeout_8m, policy, drained` | Enum drift. | Union in 01 §3.3 of this design. |
| 8 | `architecture/06` build weeks 2026-11-02 to 12-06; pilot kit dates 11-18 to 12-22 | Calendar moved after the kit. | This design uses week numbers 1 to 5 against 11-18 to 12-22. |

## B. Decisions still owed (by whom, by when)

| # | Question | Needed by | Who | Default if unanswered |
|---|---|---|---|---|
| 9 | Notes after calls: off entirely, or a non-corrective card? (item 1) | before build week 4 (2026-12-09) | Muath | off |
| 10 | Multi-episode days: when does the learner pick the second idea, and does a second episode need its own call? (item 3) | build week 2 | Muath + PRD-v3 thread | pick after each session; each episode has its own call and chat; one session open at a time |
| 11 | Trial plan and whether a card is needed at signup; merchant of record (USD list, local methods) | 2026-12-01 | Muath | 7-day trial on the 2-a-day plan, no card; processor open |
| 12 | Home region and processor register (PDPL, GDPR, SB 243 exposure) | before paid beta 2026-12-23 | Muath with counsel | `me-central-1`, processors as listed in 08 §10 |
| 13 | Voice vendor for episodes and calls; streaming and verbatim recognizers (blind test, 30 clips, 50 calls) | build weeks 1 to 2 | tests | Gemini 3.8 Flash TTS; Soniox; AssemblyAI |
| 14 | English Grammar Profile licensing for the `ar-en` structure inventory, or an alternative inventory | build week 2 | Muath | build the inventory from open sources with EGP-style ids |
| 15 | Who writes the host and Salma bibles (Karim, Mona, Salma) | before build start 2026-11-18 | Muath | pipeline cannot be tested on real voices without them |
| 16 | Second tagger for the calibration set (150 to 200 samples) | build week 5 | Muath | only event claims ship; metric claims stay off |
| 17 | Does an in-conversation "yes" recorded verbatim count as explicit consent for sensitive facts? | before paid beta | counsel | fallback is a one-tap confirmation card in the notebook |
| 18 | Which languages pass the five-check gate for the beta besides English | beta week 1 | tests | English only |
| 19 | Private feed support in the podcast apps the first cohort uses | first cohort | observation | Apple Podcasts, Overcast, Pocket Casts links |
| 20 | Second engineer; infra budget about $800 to $1,100 a month | now | Muath | one engineer, five weeks, P0 only |

## C. Assumptions this design makes that should be measured

- Prior curve `p_known(rank) = sigmoid((N_est − rank)/900)` and the word-check estimate of `N_est` (03 §6).
- One call-worker task per 6 to 8 concurrent calls; cold start inside 60 s.
- Batch escalation 2% (pick) to 15% (cutoff) of episodes.
- `sd_obs = 8` for skills until standard errors exist; `MIN_PAIRS = 12` for a usable `sem`.
- 60M event rows a month at 10,000 learners.
- Move-contract violations under 5% of host turns after prompt tuning.
- Scale anchors for the internal 10..90 skill scale (A2 30 to 42, B1 43 to 58, B2 59 to 75, C1 76 to 84).

## D. Deliberately not designed here

Observer role (whispers the next recast; LATER), scout and news digests, native apps, cloned learner voice, exploration slots, guest hosts, year in review, voice-triggered talkback, dial-in beyond the P1 experiment. Nothing in files 00 to 09 depends on any of them; the host prompt keeps an empty `whisper` slot for the observer.
