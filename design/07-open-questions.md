# For one — 07. Open questions for the design

*Part 7 of 8. What this design could not settle when it was written, and how each question was decided. Items 1 and 2 were Muath's open decisions; the rest surfaced while writing parts 0 to 6. Every row is decided under ADR-24 and ADR-25 (`architecture/10-decision-records.md` §3). The last column is what is watched after launch: the evidence that would make a later change worth it.*

*Revised 2026-11-12: converted from open questions to decisions under ADR-24; column "Designed for now" renamed "Decided".*
*Revised 2026-11-12 for ADR-25: web only, one onboarding order, no founding lock, no lawyer, no hired reviewers; the watch column reads after launch instead of in Milestone 0 or beta.*

| # | Question | Owner | Decided | What would make a later change worth it (watched after launch) |
|---|---|---|---|---|
| 1 | **Web app or native app?** (decision 7) | Muath | **A web app plus the private podcast feed; no native app is planned (ADR-24.1, ADR-25.4).** The web app adds a "keep the screen on" hint before calls and an install card once. | Calls abandoned on the move and the feed-to-call handoff are watched as product measures (05 §9). |
| 2 | **First-session order:** sound in 60 seconds with the account after the first call, or account first | Muath | **Sound first, the account after the first call (ADR-24.2):** Salma, the optional word check, casting, the first episode, the first call, then the account (03 flow A). The word check's position after the first call may be A/B tested; nothing else is. | Drop-off at the account step (A8). |
| 3 | **Talkback by voice** ("how do you say…" spoken in the learner's language during the call), or button-only | Muath | Button-only, the word button (ADR-24.22); voice later | Whether the per-language speech stack catches code-switching reliably (language gate check 2). |
| 4 | **Who writes the host and Salma bibles, the sting library, and the per-language ban lists** | Muath | **Drafted in `content/bibles/` (ADR-24.3).** Muath reads and approves the English bibles and Salma's Arabic (ADR-25.7, register A3); an AI review pass checks every bible, prompt and episode sample against the laws and the ban lists. No hired editor or outside writer at launch. The sting library and the ban lists are owned the same way. 06 is the brief the drafts follow. | Sameness by week 4 (R9): if it shows, a writer is hired for season two. |
| 5 | **Dark-only (as the prototype) or dark + light** | Muath | Dark and light; dark by default (01 §9; ADR-24.22) | Learner preference; cost is small since tokens are shared. |
| 6 | **Should Salma's language shift toward the target language be automatic or chosen?** | Design | Automatic, announced once, with "say so if it's too much" (ADR-24.22) | Reaction to the first shift. |
| 7 | **Where the daily allowance line lives on 2 and 3 a day plans:** a quiet row under the hero (current) or inside the wrap only | Design | A quiet row (ADR-24.22) | Whether learners on 2 a day find the second episode without being pushed. |
| 8 | **The weekly proof on a week with no sessions:** a very short "what has built up" proof (current) or none | Design + learning | A short proof; never about the days (ADR-24.22) | Whether a proof after an empty week feels like a nudge (it must not). |
| 9 | **Proof day default:** the last day of the rhythm week (current) or the learner's chosen day | Design | Last day of the rhythm week, changeable in Controls (ADR-24.22) | How often learners change it. |
| 10 | **Captions on calls by default for all levels** | Design + learning | On by default, host side only; off in Controls (ADR-24.22) | Whether advanced learners find them distracting. |
| 11 | **The 90-second sample page:** required before signup, or a shortcut straight to onboarding | Marketing | Optional: the page exists; "Start your show" also exists on A1 for direct links (ADR-24.22) | Where signups come from. |
| 12 | **Price copy on Plans** (the first draft had a founding-member lock and a 100-member cap) | Muath | No founding lock and no cap (ADR-25.5). Plans state the price, per day, per episode and what every plan includes; Paddle carries the payment-side consumer law (ADR-25.3). | Paddle's review of the checkout copy. |
| 13 | Removed: store compliance applied only to a native app, and there is none (ADR-25.4). | | | |
| 14 | **Data deletion grace period** (7 days in the first draft) and the typed "delete" confirmation | Muath | **No grace period and no restore** (ADR-24.B1): a typed "delete"; access ends at once, live data purged within 24 hours, backups expire within 30 days (FR-1047) | The self-review checklist (`legal/00-self-review-checklist.md`, ADR-25.3, register A4). |
| 15 | **Right-to-left mirroring of the scrubber and the hold pad ring** | Design + Arabic speakers | Scrubber stays left-to-right (time); the layout mirrors (ADR-24.22) | How Arabic, Persian and Urdu learners use it. |
| 16 | **Eastern Arabic digits in an Arabic interface** | Design | Follow the locale (ADR-24.22) | Learner preference. |
| 17 | **Headphone "next" = mark moment:** is a 1-second toast enough confirmation in Ears mode | Design | Toast + a soft click (the one sound allowed, because it confirms an action, not a reward) (ADR-24.22) | Marks that are undone right after. |
| 18 | **Second host voice during the call** (both hosts on the line) | Product | One host per call (ADR-24.22) | Cost and latency; later. |
| 19 | **What Today shows on 3 a day after three episodes** | Design | "That's three today." (ADR-24.22) | Nothing; the copy is final. |
| 20 | **Does "Hours" belong in the notebook home or only in the season recap** | Design + consistency lens | Both, quietly (ADR-24.22) | Whether a cumulative number tempts anyone to chase it. |

## What this design does not cover (by scope)
- Character creation and the six chassis (deferred until episodes are loved).
- Any employer or university surface (year 2).
- Settings beyond the controls sheet (by law: everything else is a sentence to Salma).
- Marketing site beyond the sample page.

## Inputs this design would change on
- If Muath reverses decision 3 toward explicit notes after the call, the debrief screen from the UI/UX lens (new / polish / word you reached for) returns as a single optional sheet after C6, and `--recast` gains a tap target. Nothing else moves.
- If the language gate opens a language whose speech stack cannot hold one-second latency, the call for that language launches as voice notes by default (the C2 fallback becomes the main path) and the hold pad becomes a record button.
