# 10. Open questions and contradictions

*Found while writing this design on 2026-11-06. On the same day the architecture thread revised all nine documents and wrote `architecture/10-decision-records.md` (23 ADRs and the naming rulings in its §4); this file was updated on 2026-11-07 to match. Items 1 to 8 were contradictions with the architecture as first drafted; each row now says how the ADRs settled it and what the design does. Items 9 onward are decisions still owed.*

## A. Contradictions with the architecture documents

| # | Where | The contradiction | TDD stance |
|---|---|---|---|
| 1 | `architecture/05 §4.7`, `06 §4.3 NotesDoc`, `01 §4.3 session/after-pass stage 1` | The architecture builds Salma's after-call notes (new-for-you, **polish**, reached-for cards) and a chat **margin note**. Decision 3 (2026-10-23, "teaching is invisible") dropped the after-call correction notes, the polish card and the margin note from the first version; PRD-v2 v3.1 says "no notes after calls". | **Settled by ADR-06**: notes, the polish card and the margin note do not exist; no tables, no flag. The after-session pass is one function; corrections are recasts planned by the teacher's echo plan; a "New for you" card comes only from `did_it` and `first_ever` claims; Salma explains when asked (`salma_explain`). The design now follows this. |
| 2 | `architecture/01 §4.2 learners.tz default 'Asia/Riyadh'`, `package_ar_en` everywhere, Arabic-only Salma, SAR prices | Decision 1 removed the launch country and opened languages by the five-check gate. | **Settled by ADR-02 and ADR-03**: two package axes, `packages/languages/<target>/` and `packages/native/<lang>/` (not pairs); columns `native_language`, `target_language`, `residence_country`; `tz` has no default; USD list prices. The design's first stance (`packages/language/<pair>/`, `native_lang`/`target_lang`) was overridden and is corrected. |
| 3 | `architecture/01 episodes unique (learner_id, local_date, kind)`, PRD "one new episode per active day" | Decision 2 sells plans of 1, 2 or 3 new episodes a day. | **Settled by ADR-04 and ADR-05**: plans `one_a_day`, `two_a_day`, `three_a_day` with `plan.episodes_per_day` from `plans.yaml`; `episodes.slot` (kept); episodes 2 and 3 are `daily_extra`, planned by the nightly teacher run (one plan, up to three briefs), made on demand through `POST /v1/episodes/next` after the current episode is heard, Inngest `learner.extra_requested`; unused extras end `superseded`; the feed carries only the drop plus played extras. The PRD-v3 thread carries the rule into part 3.6. |
| 4 | `architecture/08 §6.1` cost model counts round two and notes/margin note in the $0.638 per session | With notes removed and round two P1, the beta estimate falls by about $0.03 to $0.04; the Gemini doubling on 2027-01-01 adds about $0.18 on the Gemini voice stack (ADR-13: the cost line becomes "Salma (when asked) and chat"). | The architecture's cost model was re-run; the "Margin by plan" report carries the post-doubling warning (floor $0.43 to $0.45 above the 2 and 3 a day break-even at full use). |
| 5 | `architecture/03 §4.3` "Rejected: deferring RLS" vs `04` roles; `01 episodes.state` vs `02 status` enums | Two overlapping enums for episode state. | **Settled** (§4 rulings): `episodes.state`, never `status`; one enum in 01 §3.2 of this design plus `planned`. |
| 6 | `architecture/03 §4.10 CallTurnAudioReady` has `turn_n, media_id, event_id` and "updates the call_turn event's payload"; `01 §4.3` and `04 §4.1` say events are append-only and the verbatim is a separate `call_turn_verbatim` event with `turn_index, media_object_id` | Field names and the update-vs-append rule disagree. | **Settled** (§4 rulings): `call_turn_verbatim` appended by `workflows` through `events.append()`; `turn_index` everywhere. |
| 7 | `architecture/03 §4.1 end_reason` adds `abandoned, driving, fallback`; `01` has `timeout_8m, policy, drained` | Enum drift. | Union in 01 §3.3 of this design; unused extras and swapped dailies end `superseded`. |
| 8 | `architecture/06` build weeks 2026-11-02 to 12-06; pilot kit dates 11-18 to 12-22 | Calendar moved after the kit. | **Settled by ADR-07**: W1 11-18, W2 11-25, W3 12-02, W4 12-09, W5 12-16, exit 12-22, beta 12-23 to 2027-01-26, gate review 2027-01-26; the architecture was re-dated to match. |

## B. Decisions still owed (by whom, by when)

| # | Question | Needed by | Who | Default if unanswered |
|---|---|---|---|---|
| 9 | Settled by ADR-06 (no notes); only the wording of the "New for you" card remains a design question | build week 5 | design thread | card from `did_it` and `first_ever` claims only |
| 10 | Settled by ADR-05 for the mechanism; still open: does a `daily_extra` get its own call, and does the teacher's multi-episode plan reuse the day's cast and arc? | build week 2 | PRD-v3 thread | each episode has its own call and chat; one session open at a time |
| 11 | Trial plan and whether a card is needed at signup; merchant of record (USD list, local methods) | 2026-12-01 | Muath | 7-day trial on the 2-a-day plan, no card; processor open |
| 12 | Final home region (`eu-central-1` default, `me-central-1` alternative, ADR-08), the transfer basis for US vendors, which regimes counsel covers for 2026-12-23 and whether unreviewed countries sign up under the generic notice (ADR-20) | counsel answers due 2026-11-17 | Muath with counsel | `eu-central-1`; generic baseline row |
| 13 | Voice vendor for episodes and calls; streaming and verbatim recognizers (blind test, 30 clips, 50 calls) | build weeks 1 to 2 | tests | Gemini 3.8 Flash TTS; Soniox; AssemblyAI |
| 14 | English Grammar Profile licensing for the `languages/en` structure inventory, or an alternative inventory | build week 2 | Muath | build the inventory from open sources with EGP-style ids |
| 15 | Who writes the host and Salma bibles (Karim, Mona, Salma) | before build start 2026-11-18 | Muath | pipeline cannot be tested on real voices without them |
| 16 | Second tagger for the calibration set (150 to 200 samples) | build week 5 | Muath | only event claims ship; metric claims stay off |
| 17 | Does an in-conversation "yes" recorded verbatim count as explicit consent for sensitive facts? | before paid beta | counsel | fallback is a one-tap confirmation card in the notebook |
| 18 | Which target languages pass the gate (`forone.langgate`, ADR-03) besides English, and which native packages exist on 2026-12-23 (English and Arabic certain) | beta week 1 | tests, cohort | `languages/en`; `native/ar`, `native/en` |
| 21 | One-engineer on-call: accept that some overnight P1s are answered by the product's fallbacks and a human at the next working hour (ADR-16) | before beta | Muath | accepted as the honest beta statement |
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
