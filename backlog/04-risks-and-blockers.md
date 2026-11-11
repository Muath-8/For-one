# For one: risks and blockers

*Written 2026-11-06; blockers decided 2026-11-12 (ADR-24). Blockers are decisions only Muath (or counsel) can make; each has a date by which the build needs it, what it blocks, and the default the backlog assumes if no answer comes. Risks are things that could move 23 December or break a gate, with what tests them and the fallback.*

## A. Blocking decisions (all decided 2026-11-12)

Muath delegated these on 2026-11-12. Each is recorded in ADR-24 ([architecture/10-decision-records.md](../architecture/10-decision-records.md)); what is left is an owner action (A#) or a measurement (M#) from that document's §10 register.

| Id | Decision | Decided | ADR | Action left |
|---|---|---|---|---|
| B1 | Web or native for the beta | Installable web app plus private podcast feed plus web checkout; calls screen-on with earphones; native after the gates or when GATE-M18 fires | 24.1 | none |
| B2 | First-session order | Order A: Salma's talk, optional word check, casting while the pilot renders, pilot, first call, then the account; the beta may A/B the word check after the first call | 24.2 | none |
| B3 | Who writes the hosts (Karim, Mona) and Salma | Drafted in `content/bibles/` (this pass); Muath owns them; a paid native English editor reads them by 2026-12-01; Muath reads Salma's Arabic; no outside writer for the beta | 24.3 | A4, A5 |
| B4 | Region and the legal view on learner voice | `eu-central-1` final for the beta; SCCs with a transfer impact assessment, never consent (24.B13); voice handled at the biometric standard; `me-central-1` only if counsel requires it | 24.8 | A1 (counsel confirms by 2026-11-17) |
| B5 | Merchant of record and payment processor | Paddle; Stripe with Stripe Tax only if Paddle declines | 24.4 | A6 by 2026-12-02 |
| B6 | The three prices | $19.99 / $29.99 / $44.99 kept; price rises for post-founding signups on any plan whose margin at measured use is below zero (`two_a_day` $34.99, `three_a_day` $54.99) | 24.5 | M6 |
| B7 | Beta countries and invite source | Waitlist learners in any country, 18+, under the generic notice, where Paddle sells; English target only | 24.9, 24.20 | none |
| B8 | External test | Duolingo English Test | 24.19 | A10 |
| B9 | Penetration test budget | $5,000 to $10,000, February, before public launch | 24.13 | A11 |
| B10 | Second engineer, or the single-engineer cut list | Two engineer-equivalents; the cut list applies from day one regardless; P0 split into Day-1 and later (release plan §5 and §6); **the beta opens when the Day-1 work is done: 2027-03-17 with two engineers from build start (a week later per week of delay), 2027-02-17 with a third from 2026-12-01, 2027-07-07 with one** | 24.11 | A2 |

## B. Risks

| Id | Risk | Why it matters | What tests it | Fallback |
|---|---|---|---|---|
| R1 | **The P0 set does not fit** (re-counted 2026-11-12: Day-1 P0 136.5 engineer-days after the rulings, later P0 37, against about 41 before the old 2026-12-21 freeze); settled by ADR-24.11, which moves the open to 2027-03-17 with two engineers. The risk that remains is velocity below the sizes | The open date moves again | The capacity table in `00-release-plan.md` section 6; the W2 and W3 exit checks | Apply the single-engineer cut lists from day one even with two engineers; move the Show tab, admin pages, Apple sign-in and the invites page to beta week 1; if W3's exit (pilot under 45 s, first sentence under 5 minutes) is missed, move the beta to 6 January and tell the waitlist |
| R2 | **Speech-to-text smooths the learner's errors** | The teacher never sees the mistakes it is meant to bring back; invisible teaching then has nothing to work with | E02-S02 (30 clips), E09-S01 error-survival baseline, per-language in the gate | Choose the verbatim vendor on error survival, not accuracy; keep per-turn audio for re-transcription; flag low-confidence turns and never build a claim on them |
| R3 | **Learners do not fix errors when nobody says "wrong"** | Every lens recommended explicit notes; Muath chose invisible teaching (decision 3). Recasts are the least-noticed feedback | The day-14 pilot recordings and the 4-weekly recordings judged blind: do the errors the show worked on fall? | If an error survives two recordings, the teacher raises how often the right form comes back and how often the host echoes it, still without saying it was wrong; the observer is the first thing to add after the beta |
| R4 | **The host is too slow** (over 1.5 s median) | The call stops feeling like a conversation | E02-S04 and the W4 and W5 reruns of the 50 calls | Cached brief, the Haiku-host comparison (E14-S06), the runner-up voice for the call, worker placement closer to the vendor |
| R5 | **Vendor choice slips past 27 November** | Everything in W3 is built on an untested vendor | The W2 decision table | Freeze on the measured leader on 27 Nov regardless; the adapters make a later swap a configuration change |
| R6 | **Cost per session above $0.60** | Stop line at $1.00; the 2 and 3 a day plans lose money above $0.42 | E14 tracing from the first test render; the W5 exit document | Batch everything nobody waits on; the cheapest voice that passes the blind test; shorter default episode (5 to 6 minutes); conserve mode |
| R7 | **Counsel's answer forces a region move or a consent rewrite late** | Production Terraform and the consent copy change in W5 | B4's date | Region as a variable; staging in the EU; consent copy drafted now from the pilot's wording |
| R8 | **Wrong memories reach a host's mouth** | "A wrong memory is a bug"; target under 1 in 100 callbacks | E09-S05 fact precision on replayed pilot intakes; the weekly count | Quote-backed facts only, the confirmation ladder, at most 2 life facts per episode, the notebook fix path |
| R9 | **AI sameness: episodes feel alike by week 4** | The riskiest product assumption | The pilot's week-2 "still choosing tomorrow", the similarity score, the monthly human read | The variety system (E04-S11), real input every day, hosts written by people, a guest host or new format in season two |
| R10 | **iOS web: the call dies when the screen locks** | The commute use case | The W3 device matrix | Calls screen-on with earphones in the beta; the dial-in experiment; native app after the gates |
| R11 | **Apple or Google developer approval does not arrive** | Sign in with Apple and the feed handoff on iOS | Applications filed in W1 | Email code only (P1 for the sign-ins) |
| R12 | **One engineer on call for a 05:40 drop failure** | A missed drop is the one thing the learner notices | E15-S04, the tabletop | Paging with phone escalation; the on-demand fallback at drop minus 90 minutes; the fallback episode kind |
| R13 | **The pilot gate fails on 18 November** | The build should not start on a failed claim | The pilot's gate report on 17 Nov | Find which claim failed (the show not wanted, the teacher not felt, the price wrong) and fix that before writing more code; W1's infrastructure work can still proceed because it is claim-neutral |
| R14 | **The second language opens too early** | Quality falls behind English and the trust brand suffers | The gate harness (E02-S08) and the per-language close rule (E16-S07) | English only in the beta unless all five checks pass; a language that falls 15 points behind closes |
| R15 | **Usage limits on the planning side** (about 50 minutes of agent work per window) | Documentation and prompt work spans days | n/a | Small batches, save each file as it finishes; this backlog was written under that rule |

## C. Assumptions this backlog makes

1. The pilot gate passes on 18 November, or fails on a claim the build can proceed around.
2. The architecture documents' build plans are right in content and 16 days early in date; their stale decisions (a Saudi launch, Arabic only, Salma's notes after the call) are overridden by the 23 October decisions and do not appear in the stories.
3. Two engineers plus Muath, with the single-engineer cut lists applied from day one, except Terraform (ADR-24.11, 24.B19). The open follows the Day-1 work: 2027-03-17 with two engineers from build start, 2027-02-17 with three, re-forecast every build week.
4. English is the only target language in the beta; the learner's own language can be any language with interface strings, glosses and a recognizer that catches it mid-sentence.
5. The A4 to A7 order (order A) and the bibles' authorship (drafted, then read by a native editor) were decided on 2026-11-12 (ADR-24.2, 24.3).
