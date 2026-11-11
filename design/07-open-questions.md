# For one — 07. Open questions for the design

*Part 7 of 8. What this design could not settle when it was written, and how each question was decided. Items 1 and 2 were Muath's open decisions and were designed both ways; the rest surfaced while writing parts 0 to 6. On 2026-11-12 every row was decided under ADR-24 (`architecture/10-decision-records.md` §3: rows 24.1, 24.2, 24.3 and 24.22). The "both ways" designs stay documented: web plus feed and order A are the decided path; native and order A′ are the later or alternative path. The last column is what the pilot and beta watch: the evidence that would make a later change worth it.*

*Revised 2026-11-12: converted from open questions to decisions under ADR-24; column "Designed for now" renamed "Decided (ADR-24.x)"; row 13 marked not applicable under web plus feed.*

| # | Question | Owner | Decided (ADR-24.x) | What would make a later change worth it (observe in pilot/beta) |
|---|---|---|---|---|
| 1 | **Web app + private feed, or native app, for the beta?** (decision 7) | Muath | **Web app plus the private feed (ADR-24.1).** Web adds a "keep the screen on" hint and an install card. The native variant (lock-screen call accept, hands-free calls; 02 §6) stays designed as the later path: after the beta gates, or earlier if GATE-M18 fires. | The beta's commute data (GATE-M18, register M7): calls abandoned on the move, feed-to-call handoff loss. Either one bad moves native earlier. |
| 2 | **First-session order:** sound in 60 seconds with the account after the first call (order A), or account first (order B) | Muath | **Order A (ADR-24.2):** Salma, the optional word check, casting, the pilot, the first call, then the account (03 flow A). Order A′ (03) stays documented as the alternative and is not run in the beta. The beta may A/B the word check after the first call; nothing else is tested. | Drop-off at the account step (A8) in the beta; a high, costly loss of unfinished sessions with no account would argue for order A′. |
| 3 | **Talkback by voice** ("how do you say…" spoken in the learner's language during the call) in the beta, or button-only | Muath / engineering | Button-only, the word button (ADR-24.22); voice later | Whether the per-language speech stack catches code-switching reliably (language gate check 2). |
| 4 | **Who writes the host and Salma bibles, the sting library, and the per-language ban lists** | Muath | **Drafted in this pass in `content/bibles/` (ADR-24.3).** Muath is the owner of record; a paid native English editor reads the hosts' bible and 30 sample lines per host by 2026-12-01; Muath reads Salma's Arabic (register A4, A5). No outside writer for the beta. The sting library and the ban lists are owned the same way. 06 is the brief the drafts follow. | Sameness by week 4 (R9): if it shows, a writer is hired for season two. |
| 5 | **Dark-only (as the prototype) or dark + light** | Muath | Dark and light; dark by default (01 §9; ADR-24.22) | Learner preference in the beta; cost is small since tokens are shared. |
| 6 | **Should Salma's language shift toward the target language be automatic or chosen?** | Design + pilot | Automatic, announced once, with "say so if it's too much" (ADR-24.22) | Reaction to the first shift. |
| 7 | **Where the daily allowance line lives on 2 and 3 a day plans:** a quiet row under the hero (current) or inside the wrap only | Design | A quiet row (ADR-24.22) | Whether learners on 2 a day find the second episode without being pushed. |
| 8 | **The weekly proof on a week with no sessions:** a very short "what has built up" proof (current) or none | Design + learning | A short proof; never about the days (ADR-24.22) | Whether a proof after an empty week feels like a nudge (it must not). |
| 9 | **Proof day default:** the last day of the rhythm week (current) or the learner's chosen day | Design | Last day of the rhythm week, changeable in Controls (ADR-24.22) | Pilot and beta. |
| 10 | **Captions on calls by default for all levels** | Design + learning | On by default, host side only; off in Controls (ADR-24.22) | Whether advanced learners find them distracting. |
| 11 | **The 90-second sample page:** required before signup, or a shortcut straight to onboarding | Marketing | Optional: the page exists; "Start your show" also exists on A1 for direct links (ADR-24.22) | Where waitlist and signups come from. |
| 12 | **Founding-member price lock copy and the 100-member cap** | Muath / legal | A single factual line on Plans (ADR-24.22); the lock covers the first 100 payers (ADR-24.5) | Counsel's review of the terms (register A8) and Paddle's review of the checkout copy. |
| 13 | **Store compliance if native:** in-app purchase for plans, "sign in with Apple" requirement, account deletion in-app | Engineering / legal | **Does not apply under ADR-24.1** (web checkout through Paddle, ADR-24.4). The store variants stay noted in 02 §6 for the native path. | Returns only if native starts (row 1). |
| 14 | **Data deletion grace period** (7 days in the first draft) and the typed "delete" confirmation | Legal | **No grace period and no restore** (ADR-24.B1, amending 24.22): a typed "delete"; access ends at once, live data purged within 24 hours, backups expire within 30 days (FR-1047) | Counsel's review of the privacy notice and terms (register A8). |
| 15 | **Right-to-left mirroring of the scrubber and the hold pad ring** | Design + Arabic testers | Scrubber stays left-to-right (time); the layout mirrors (ADR-24.22) | Testing with Arabic, Persian and Urdu learners. |
| 16 | **Eastern Arabic digits in an Arabic interface** | Design + testers | Follow the locale (ADR-24.22) | Learner preference. |
| 17 | **Headphone "next" = mark moment:** is a 1-second toast enough confirmation in Ears mode | Design | Toast + a soft click (the one sound allowed, because it confirms an action, not a reward) (ADR-24.22) | Pilot and beta. |
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
- If GATE-M18 fires during the beta, native starts early (ADR-24.1): the screens stay, 02 §6's native column and row 13 above apply.
