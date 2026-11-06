# For one — 07. Open questions for the design

*Part 7 of 8. What this design could not settle, who decides, and what the design does meanwhile. Items 1 and 2 are Muath's open decisions and are deliberately designed both ways; the rest surfaced while writing parts 0 to 6.*

| # | Question | Owner | Designed for now | What would settle it |
|---|---|---|---|---|
| 1 | **Web app + private feed, or native app, for the beta?** (decision 7) | Muath | Both: the same screens; web adds a "keep the screen on" hint and an install card, native adds lock-screen call accept and hands-free calls (02 §6) | The pilot's commute data: calls abandoned on the move, feed-to-call handoff loss. Switch to native early if either is bad. |
| 2 | **First-session order:** sound in 60 seconds with the account after the first call (order A), or account first (order B) | Muath | Both, as a configurable step order (03 flows A and A′) | Drop-off at the account step in each order during Milestone 0 / early beta; store rules if native. |
| 3 | **Talkback by voice** ("how do you say…" spoken in the learner's language during the call) in the beta, or button-only | Muath / engineering | Button-only (the word button); voice later | Whether the per-language speech stack catches code-switching reliably (language gate check 2). |
| 4 | **Who writes the host and Salma bibles, the sting library, and the per-language ban lists** | Muath | 06 is the brief; nothing is written | An owner named before Nov 18. |
| 5 | **Dark-only (as the prototype) or dark + light** | Muath | Both; dark default (01 §9) | Learner preference in the beta; cost is small since tokens are shared. |
| 6 | **Should Salma's language shift toward the target language be automatic or chosen?** | Design + pilot | Automatic, announced once, with "say so if it's too much" | Pilot reaction to the first shift. |
| 7 | **Where the daily allowance line lives on 2 and 3 a day plans:** a quiet row under the hero (current) or inside the wrap only | Design | Quiet row | Whether learners on 2 a day find the second episode without being pushed. |
| 8 | **The weekly proof on a week with no sessions:** a very short "what has built up" proof (current) or none | Design + learning | A short proof; never about the days | Whether a proof after an empty week feels like a nudge (it must not). |
| 9 | **Proof day default:** the last day of the rhythm week (current) or the learner's chosen day | Design | Last day of the rhythm week, changeable in Controls | Pilot. |
| 10 | **Captions on calls by default for all levels** | Design + learning | On by default, host side only; off in Controls | Whether advanced learners find them distracting. |
| 11 | **The 90-second sample page:** required before signup, or a shortcut straight to onboarding | Marketing | The page exists; "Start your show" also exists on A1 for direct links | Where waitlist and signups come from. |
| 12 | **Founding-member price lock copy and the 100-member cap** | Muath / legal | A single factual line on Plans | Legal and payment-processor review. |
| 13 | **Store compliance if native:** in-app purchase for plans, "sign in with Apple" requirement, account deletion in-app | Engineering / legal | Web checkout designed; store variants noted | Decision 1. |
| 14 | **Data deletion grace period** (7 days in this design) and the typed "delete" confirmation | Legal | 7 days, typed or biometric | Legal review for the countries learners come from. |
| 15 | **Right-to-left mirroring of the scrubber and the hold pad ring** | Design + Arabic testers | Scrubber stays LTR (time), layout mirrors | Testing with Arabic, Persian and Urdu learners in the pilot. |
| 16 | **Eastern Arabic digits in an Arabic interface** | Design + testers | Follow the locale | Pilot preference. |
| 17 | **Headphone "next" = mark moment:** is a 1-second toast enough confirmation in Ears mode | Design | Toast + a soft click (the one sound allowed, because it confirms an action, not a reward) | Pilot. |
| 18 | **Second host voice during the call** (both hosts on the line) | Product | One host per call | Cost and latency; later. |
| 19 | **What Today shows on 3 a day after three episodes** | Design | "That's three today." | Trivial; confirm the copy. |
| 20 | **Does "Hours" belong in the notebook home or only in the season recap** | Design + consistency lens | Both, quietly | Whether a cumulative number tempts anyone to chase it. |

## What this design does not cover (by scope)
- Character creation and the six chassis (deferred until episodes are loved).
- Any employer or university surface (year 2).
- Settings beyond the controls sheet (by law: everything else is a sentence to Salma).
- Marketing site beyond the sample page.

## Inputs this design would change on
- If Muath reverses decision 3 toward explicit notes after the call, the debrief screen from the UI/UX lens (new / polish / word you reached for) returns as a single optional sheet after C6, and `--recast` gains a tap target. Nothing else moves.
- If the language gate opens a language whose speech stack cannot hold one-second latency, the call for that language launches as voice notes by default (the C2 fallback becomes the main path) and the hold pad becomes a record button.
