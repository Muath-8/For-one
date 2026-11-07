# For one: the release plan

*Written 2026-11-06. From the Milestone 0 gate decision on 18 November 2026 to the end of the first post-beta season on 23 February 2027. Companion to `01-epics.md` (16 epics), `02-stories/` (164 stories), `03-non-functional-stories.md`, `04-risks-and-blockers.md` and `stories.csv`. The visual version is the page "For one release plan": https://claude.ai/artifact/NFcJZpKpupvoVyH59Mhwjc (source: `release-plan.html`).*

## 1. Milestones

| # | Milestone | Dates | What is true at the end | Gate |
|---|---|---|---|---|
| M0 | Pilot gate decision | 18 Nov | The hand-run pilot (15 learners, 24 Oct to 18 Nov) is read: start the build, or rethink the claim that failed | 10 of 15 ask for the next episode unprompted; 4+ sessions a week; 4+ minutes of speech; the day-14 recording better for most; 5 of 15 pre-pay |
| W1 | Foundation and vendor tests | 18 to 24 Nov | Repo, CI, staging infrastructure, events and the learner model's tables, tracing middleware, the English package v1, the 30-clip recognizer test done, blind voice playlists rendered, counsel's six requests sent, consent addenda signed | Recognizer and voice tables exist by 24 Nov |
| W2 | Pipeline and the minimal call | 25 Nov to 1 Dec | Vendors frozen on 27 Nov; adapters for the winners; an episode produced end to end on staging for 3 synthetic learners; the minimal call-worker carries the 50 scripted calls; the governor replayed on pilot transcripts; batch mode; release manifest and flags | 20 test episodes with measured cost; host reply median under 1.5 s |
| W3 | Onboarding, Today, feed, payments scaffold | 2 to 8 Dec | A1 to A10 on real phones; Today, the player, the article, swap, the small door; the private feed in three podcast apps; push for the drop; consent flow and age gate; plan catalogue, allowance and the trial ledger; the device matrix passed | Pilot plays under 45 s after intake; first spoken sentence under 5 minutes |
| W4 | The full call and the after-session pass | 9 to 15 Dec | Hold-to-talk, the word button, recall gaps, the retell, anxiety mode, goodbyes, voice-note fallback, crisis step-out; verbatim per turn; the analyst and memory keeper on the live call; the variety system; arcs and seasons; cost alarms and the failover drill | Zero governor violations on 50 calls; after-pass under 10 minutes |
| W5 | Proof, notebook, privacy and production | 16 to 22 Dec | The claim gate wired to a simple weekly proof; the then-and-now recording; the notebook with veto and add; export and delete on the clock; production from the same Terraform, restored once; the 15 pilot learners re-onboarded on production; the tabletop; the cost exit document. Freeze on 19 Dec 12:00 | Measured cost per session and a costed path to $0.35; `privacy/verify` passes on a deleted learner |
| B1 | Founding beta, cohorts 1 to 5 | 23 Dec to 26 Jan | About 50 learners a week into 7-day trials, English only; P1 shipped behind flags (round two, finale, the tape, shadowing, Apple and Google sign-in, dial-in); the first false-claim audit on 1 Jan; first finales from 20 Jan; a second language through the gate harness as a dry run; the gate review on 26 Jan | Trial to paid 30%+ (stop under 15%); week-4 active 40%+ (stop under 25%); 4+ sessions a week (stop under 2.5); 4+ minutes of speech (stop under 2); recording improves for most; renewal 60%+ (stop under 40%); cost under $0.60 (stop over $1.00 with no plan); false claims under 5%; wrong memories under 1 in 100 |
| S2 | Season two, after the gate | 27 Jan to 23 Feb | Prices confirmed for the public; the floor stack migrated piece by piece behind blind tests; the observer tested behind a flag; the second language opened if it passed; the penetration test budgeted before public launch | Retention and renewal hold at public prices |

The build is five weeks, not the architecture documents' five weeks from 2 November: every build-plan week in `architecture/0*-*.md` section 7 moves forward by 16 days. The content of each week is kept; only the dates move.

## 2. What is in the beta, and what is not

**In the beta on 23 December (P0).** The sample episode and landing page; onboarding A1 to A10 with Salma's intake, the optional word check, casting, the pilot and the first call; the web app with Today, Show and Notebook; the player with Huh?, speeds, the folded transcript and tap-to-hear; the article; the daily call with hold-to-talk, the word button, recall gaps, the retell and the voice-note fallback; the chat that ends in three ideas; one swap a day; the small door; the private podcast feed and the drop push; the one opt-in gap note; the return episode; rhythm in words; the after-session pass; the notebook with working-on (veto and add), words you own, about you, why this episode, counts and the out-in-the-world log; the controls sheet; the weekly proof with "how we know" and the worth-it question; the then-and-now recording (the first "then" after session 2); seasons with a goal and the mid-season rehearsal; the three plans, the 7-day trial on 2 a day, web checkout, founding-member price lock and one-tap cancel; per-learner keys, consent with versions, the age gate, deletion and export on the clock, research opt-in, the crisis protocol, AI disclosure; cost tracing, caps and alarms; logging, paging, runbooks, the eval gate and the gates page.

**During the beta (P1, behind flags).** Round two; the season finale with the recording comparison; the tape in the notebook; shadowing; Apple and Google sign-in; the dial-in experiment; the language gate harness and a second-language dry run; metric unlock at 12 pairs; the external test; billing reconcile; the full offline suite with 50 synthetic learners and the simulated caller; the 30-case injection set; vendor regression.

**Not in the beta (LATER).** Character creation and the six chassis; the scout (news per interest); the observer in the call (first thing after the beta); languages that have not passed the gate; native apps; settings beyond the controls sheet; referral programs; the learner's cloned voice; regional prices; paid acquisition; employer seats; human bridges.

**Dropped by decision 3, so never built.** Salma's correction notes after the call, the margin note in chat, the polish card, any "the correct answer is" surface.

## 3. Dependency order

The order below is what must exist before the next thing can be built. Each line names the stories on it.

1. **Infrastructure first (W1).** E01-S01 to S06 (repo, core, api, Inngest, staging, tracing) and E13-S01 (keys), E14-S01 to S02 (price book, tracing middleware). Everything else writes to these.
2. **Pilot data in (W1).** E02-S01 (consent addendum), E15-S02 (fixtures). Every test below uses them.
3. **Vendor tests (W1 to W2).** E02-S02 (recognizers), E02-S03 (voices), E05-S01 (minimal worker), E02-S04 (50 calls). They end in E02-S05 (vendors frozen, 27 November). Nothing in W3 is built on an untested vendor.
4. **The model's tables and the package (W1 to W2).** E03-S01 to S06 and E02-S06 to S07. The pipeline reads briefs from them.
5. **The pipeline (W2).** E04-S01 to S07 in order: teacher, writer, fitter, editor, voice studio, publish, batch. It produces the first real episodes, which E07's player and E08's feed need as fixtures.
6. **The call (W2 to W4).** E05-S02 (governor) and S03 (verbatim) on the minimal worker, then E05-S04 to S05 for onboarding, then E05-S06 to S11 for the full call.
7. **What the learner meets (W3).** E07-S01 to S04 (shell, auth, player, events) in W1 to W2 at low intensity, then E06 (onboarding) and E07-S05 to S11 and E08-S01 to S04 in W3. E12-S01 to S03 (plans, allowance, trial) land the same week because A9 starts the trial.
8. **The after-session pass (W2 to W5).** E09-S01 to S06. It needs the verbatim turns from the call and writes through E03-S09.
9. **Proof, notebook, privacy, production (W5).** E11-S01 to S05, E10-S01 to S08, E13-S05 to S12, E03-S10 to S11, E01-S09, E14-S08, E15-S06 to S09. The pilot learners' re-onboarding (E06-S11) is the end-to-end test of all of it.
10. **The beta (B1).** E16-S01 onward.

## 4. Critical path

The longest chain, in days, runs through the call. A slip anywhere on it moves 23 December.

```
18 Nov  consent addenda signed (E02-S01) and 30 clips through four recognizers (E02-S02)
24 Nov  recognizer and voice tables; minimal call-worker on staging (E05-S01)
27 Nov  vendors frozen (E02-S05); 50 scripted calls measured (E02-S04)
 1 Dec  governor replayed clean on pilot transcripts (E05-S02); verbatim per turn (E05-S03); first episodes end to end (E04-S07)
 8 Dec  Salma's intake and the first call live on real phones (E05-S04, E05-S05, E06-S04, E06-S07)
15 Dec  the full call (E05-S06 to S11); after-pass under 10 minutes on live calls (E09-S06)
19 Dec  freeze at 12:00; proof and notebook on production (E11-S03, E10-S02)
22 Dec  the 15 pilot learners re-onboarded on production (E06-S11); cost per session measured (E14-S08); restore drill done (E01-S09)
23 Dec  cohort 1 invited (E16-S01)
```

Three other chains come within a few days of it and need watching: the legal view on the region (B4) gates production Terraform and the consent copy; the merchant of record (B5) gates checkout by W5; the host and Salma bibles (B3) gate the writer and host prompts in W2.

**Slack.** The Show tab, the admin pages beyond review, Sign in with Apple, the IndexedDB offline queue beyond simple retry, and the invites page can all slip into the first beta week without moving 23 December; the architecture documents list them as the P0 items at risk, and this plan accepts them as beta-week-1 items.

## 5. Team assumption

Two engineers (E1: backend, pipeline, infrastructure; E2: web and the call) plus Muath on prompts, the language package, the blind tests and counsel, as the architecture assumes. With one engineer the architecture's cut lists apply: no Sign in with Apple, no autoscaling (two fixed call-worker tasks, about 16 concurrent calls), no admin pages beyond staff sign-in and the review queue, Terraform replaced by a documented console setup, the dial-in and HLS experiments moved to later, the Show tab and the fuller proof moved to the beta. With one engineer the beta date holds only if the P1 list above is not touched before 23 December.

## 6. Capacity check

| Epic | Stories | S | M | L | Rough engineer-days |
|---|---|---|---|---|---|
| E01 Platform foundation | 9 | 3 | 4 | 2 | 12 |
| E02 Vendor tests and language gate | 9 | 1 | 6 | 2 | 10 (plus Muath's test time) |
| E03 Learner model | 11 | 0 | 7 | 4 | 16 |
| E04 Pipeline | 13 | 1 | 7 | 5 | 20 |
| E05 Live call | 13 | 1 | 9 | 3 | 20 |
| E06 Onboarding | 11 | 2 | 7 | 2 | 12 |
| E07 Daily loop | 12 | 2 | 6 | 4 | 16 |
| E08 Feed and cue | 7 | 3 | 3 | 1 | 7 |
| E09 Assessment | 10 | 1 | 6 | 3 | 14 |
| E10 Notebook and controls | 9 | 1 | 8 | 0 | 9 |
| E11 Proof and seasons | 10 | 2 | 6 | 2 | 12 |
| E12 Plans and payments | 9 | 5 | 3 | 1 | 8 |
| E13 Privacy and security | 12 | 4 | 6 | 2 | 14 |
| E14 Cost | 8 | 2 | 6 | 0 | 8 |
| E15 Evals and operations | 11 | 1 | 9 | 1 | 12 |
| E16 Beta | 10 | 5 | 4 | 1 | 6 (plus operations) |
| **Total** | **164** | | | | **about 196** |

Sizes count as S = 0.5, M = 1, L = 2.5 engineer-days. About 196 days against two engineers for 25 working days (50 days) before 23 December plus 25 working days each in the beta (50 more) is far over capacity if everything P0 is built in full. The plan is feasible only because the architecture's cut lists are taken as given (about 40 days of scope is already cut in those lists), P1 stories (about 35 days) wait for the beta, and the W1 and W2 vendor and fixture work is Muath's time, not engineering time. The honest reading is that the P0 set is about 110 engineer-days for 50 available, so the beta ships the single-engineer cut list even with two engineers, or the date moves. This is the first risk in `04-risks-and-blockers.md`.
