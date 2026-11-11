# For one: the release plan

*Written 2026-11-06; re-cut twice on 2026-11-12 under ADR-24 ([architecture/10-decision-records.md](../architecture/10-decision-records.md)). From the Milestone 0 gate decision on 18 November 2026 to the end of the first post-beta season on 18 May 2027. Companion to `01-epics.md` (16 epics), `02-stories/` (170 stories), `03-non-functional-stories.md` (27), `04-risks-and-blockers.md`, `05-traceability.md` and `stories.csv`. The visual version is the page "For one release plan": https://claude.ai/artifact/NFcJZpKpupvoVyH59Mhwjc (source: `release-plan.html`; it still shows the 2026-11-06 cut).*

**The date follows the work (ADR-24.11).** Plan of record: two engineers from build start (2026-11-18); the build runs to 2027-03-12; the pre-open freeze is 2027-03-15 12:00 to 03-17 12:00 UTC; the beta opens on **Wednesday 2027-03-17**. Each week the second engineer starts later moves the open a week (from 2026-11-25: 2027-03-24); a third engineer from 2026-12-01 gives 2027-02-17; one engineer gives 2027-07-07. The date is re-forecast weekly from measured velocity and moves earlier only in whole weeks with a 15% buffer. Section 6 shows the arithmetic from the story sizes, which are unchanged: 136.5 engineer-days of Day-1 work. Day-1 has been made as small as an honest founding beta allows: what a cohort of about 50 a week can live without on day one is done by hand behind a named runbook line (section 5), and the learner-facing core is real.

## 1. Milestones

| # | Milestone | Dates | What is true at the end | Gate |
|---|---|---|---|---|
| M0 | Pilot gate decision | to 18 Nov 2026 | The hand-run pilot (15 learners, 24 Oct to 18 Nov) is read: start the build, or rethink the claim that failed. During Milestone 0 Muath ran the 30-clip recognizer test (by 10 Nov) and the blind voice test on post-doubling prices, and committed the voice winners to `vendors.yaml` (by 17 Nov); counsel received the question pack (13 Nov) | 10 of 15 ask for the next episode unprompted; 4+ sessions a week; 4+ minutes of speech; the day-14 recording better for most; 5 of 15 pre-pay |
| Bridge | Pilot pre-payers until the open | 19 Nov 2026 to 16 Mar 2027 | Milestone 0 learners who pre-paid and signed Part 2 of the addendum by 15 Dec keep receiving hand-made episodes (two a week, no calls, opt-in; ADR-24.B33); their founding lock starts at the open; the others are refunded (ADR-24.11, 24.B28) | none |
| Phase 1 | Foundation | 18 Nov to 2 Dec 2026 | Repo, CI, staging on Terraform in `eu-central-1`, events and the word bank, keys, tracing and the price book, logging and paging, fixtures, the web shell, the English package with its gate result (18.0 days) | Every test render is a priced row; the scrub test passes |
| Phase 2 | Pipeline and the minimal call | 3 Dec 2026 to 7 Jan 2027 | 50 scripted calls on the minimal call-worker; `vendors.yaml` complete; adapters; facts, canon and briefs; the pipeline from teacher to batch; governor and verbatim; media and per-learner keys; the eval gate; the player and the event queue (38.5 days). Half capacity 24 Dec to 1 Jan; no releases 31 Dec to 2 Jan. Gemini's price doubling on 1 Jan falls before the open, so the voice decision is made on post-doubling prices and there is no mid-beta voice swap (ADR-24.6) | 20 test episodes with measured cost; host reply median under 1.5 s |
| Phase 3 | Onboarding, Today, feed | 8 Jan to 3 Feb 2027 | A1 to A10 in order A; on-demand kinds; Today, the article, sessions and doors, swap, the small door; the feed, the drop and push; allowance and the trial; consent and the age gate (32.5 days) | Pilot plays under 45 s after intake; first spoken sentence under 5 minutes |
| Phase 4 | The full call and the after-session pass | 4 to 25 Feb 2027 | Hold-to-talk, the word button, recall gaps, the retell, anxiety mode, the voice-note fallback, crisis with the fail-safe; the analyst, the memory keeper and the after-pass; voice deletion in 15 minutes; spend guard and alarms; the Haiku comparison; week-one questions (27.5 days) | Zero governor violations on 50 calls; after-pass under 10 minutes |
| Phase 5 | The first week's surfaces | 26 Feb to 8 Mar 2027 | The claim gate and the simple weekly proof; the baseline then-and-now recording; plans, Paddle checkout and the day-6 email; the return episode; the controls sheet (13.0 days) | A proof built only from events for a replayed pilot learner |
| Phase 6 | Production and the exit | 9 to 12 Mar 2027 | Production applied from the same Terraform, with a full restore into staging rehearsed within 4 hours (NFR-207); deletion and export runbooks rehearsed; the pilot learners who signed Part 2 re-onboarded on production; the tabletop; the device checklist; the cost exit document (7.0 days) | Measured cost per session and a costed path to $0.35; a deletion verified on a test learner |
| Freeze | Pre-open freeze | 15 Mar 12:00 to 17 Mar 12:00 UTC 2027 | Hotfixes only, with a named approver | none |
| B1 | Founding beta, cohorts 1 to 5 | 17 Mar to 20 Apr 2027 (beta days 1 to 35) | About 50 learners a week into 7-day trials, English only; the *Later* stories land by their due days (section 6.4); the manual substitutes retire as their stories ship; first finales from day 28 (13 Apr); the gate review on day 35 | Trial to paid 30%+ (stop under 15%); week-4 active 40%+ (stop under 25%); 4+ sessions a week (stop under 2.5); 4+ minutes of speech (stop under 2); recording improves for most; renewal 60%+ (stop under 40%); cost under $0.60 (stop over $1.00 with no plan); false claims under 5%; wrong memories under 1 in 100 |
| S2 | Season two, after the gate | 21 Apr to 18 May 2027 | P1 shipped behind flags; prices confirmed for the public (ADR-24.5); the observer tested behind a flag; a second language opened if it passed; the penetration test before public launch | Retention and renewal hold at public prices |

Dates after the open are relative to it: beta day N is 2027-03-17 plus N minus 1, which is every date of the 2026-12-23 plan plus 84 days (the gate review moves from 2027-01-26 to 2027-04-20). If the open moves under ADR-24.11, every *Later* due date moves with it.

## 2. What is in the beta, and when

**Day-1 (P0, built before the open).** The learner-facing core, all real: onboarding A1 to A10 in order A (Salma's intake with the A2 notice line, the optional word check, casting, the pilot, the first call, the account by email code, the trial on 2 a day); week-one questions and the baseline then-and-now recording; the web app with Today, the player, the article, the call screen, the chat that ends in three ideas, one swap a day, the small door, sessions and doors, the controls sheet; the pipeline from teacher to publish with batch, the on-demand kinds, the return episode and the fallback episode; the private feed with the host's tag, the drop and the push; the call with hold-to-talk, the word button, recall gaps, the retell, anxiety mode and the voice-note fallback; learner-model writes, the analyst, the memory keeper and the after-session pass; the claim gate and the simple weekly proof on day 7; plans, Paddle checkout and the day-6 email; per-learner keys, consent with versions, voice deletion in 15 minutes, deletion and export requests by runbook, the crisis protocol for every learner with its fail-safe, AI disclosure, the output and correction guards; cost tracing, the spend guard and alarms; logging, paging, alerts, the release manifest, runbooks, the eval gate (law scan, governor, editor) and the canary.

**Later in the beta (P0, each due on the beta day a learner first reaches it, or later with a manual substitute).** Day 6 (22 Mar): the notebook's about-you with the sensitive-fact card, hours, out in the world, learner edits. Day 7: the gap note, rhythm in words, the season goal. Day 8: the similarity check. Day 14 (30 Mar): the edit classifier and the structure map, working on with veto and add, the mid-season rehearsal, the measures job. Day 15: the per-language close rule. Day 21 (6 Apr): measures from timings, skills and "where do I stand", the avoidance flag, Salma explaining, one-tap cancel, arcs in code, staff roles and review pages. Day 28 (13 Apr): the Show tab, calibration CI, the recording rater, words you own, life updates, founding lock, plan changes, the privacy page, the failover drill. Day 29: the gates page. Day 30: the false-claim audit tooling. Day 35 (20 Apr): the automated export and purge, the sample episode and landing page. Day 37 (after the gate review): failed-payment handling, first reachable at the first renewal. Section 6.4 has the full list.

**During the beta, if capacity allows, otherwise in season two (P1, behind flags).** Round two; the season finale with the recording comparison; the tape; shadowing; Apple and Google sign-in; the dial-in experiment; the language gate harness and a second-language dry run; metric unlock at 12 pairs; the external test (Duolingo English Test); billing reconcile; research de-identify and revoke (the switch is Day-1, off by default); the full offline suite; the 30-case injection set; vendor regression. Section 6.4 shows about 3.5 engineer-days of room for them before the gate review.

**Not in the beta (LATER).** Character creation and the six chassis; the scout; the observer in the call (first thing after the beta); languages that have not passed the gate; native apps (unless GATE-M18 fires); settings beyond the controls sheet; referral programs; the learner's cloned voice; regional prices; paid acquisition; employer seats; human bridges.

**Dropped by decision 3, so never built.** Salma's correction notes after the call, the margin note in chat, the polish card, any "the correct answer is" surface.

## 3. Dependency order

The phases of section 1 are the dependency order. Each line names its stories (Day-1 only).

1. **Before the build (Milestone 0, Muath).** E02-S01 (addendum Part 1), E02-S02 (recognizers), E02-S03 (voices); E13-S02 (register and question pack).
2. **Phase 1.** E01-S01 to S06, E13-S01, E14-S01 and S02, E15-S01 and S02, E03-S01 and S02, E07-S01; E02-S06 (Muath). Everything else writes to these.
3. **Phase 2.** E05-S01, E02-S04, E02-S05, E02-S07; E03-S04 to S06; E04-S01 to S07 in order (teacher, writer, fitter, editor, voice studio, publish, batch); E05-S02, S03; E01-S07, S08; E15-S03, S05; E14-S03; E07-S02 to S04.
4. **Phase 3.** E04-S08 to S10; E05-S04, S05; E06-S02 to S09; E07-S05, S06, S09, S10, S13; E08-S01 to S04; E12-S02, S03; E13-S03, S04; E03-S07, S08.
5. **Phase 4.** E05-S06 to S11; E07-S07, S08; E09-S01, S04, S05, S06, S10; E03-S09; E13-S05, S08, S09; E14-S04 to S06; E06-S12; E15-S04; E04-S13.
6. **Phase 5.** E11-S01 to S05; E05-S12; E12-S01, S04, S05; E08-S06; E10-S06.
7. **Phase 6.** E01-S09, E06-S11, E07-S12, E13-S12, E13-S13, E14-S08, E15-S06, E15-S10. The pilot learners' re-onboarding (E06-S11) is the end-to-end test of all of it.
8. **The beta.** E16-S01 on the open, then the *Later* stories in due-day order (section 6.4).

## 4. Critical path

The longest chain runs through the call. A slip anywhere on it moves the open, by ADR-24.11's weekly re-forecast.

```
2026-11-10  30 clips through the recognizers (E02-S02, Milestone 0)
2026-11-17  voice winners in vendors.yaml (E02-S03); counsel confirms region and regimes (A1)
2026-11-19  every pilot pre-payer told the new date, with a refund or a bridge place (A15)
2026-11-24  staging up on Terraform (E01-S05), or the console-and-runbook fallback (ADR-24.B19)
2026-12-01  bibles read by the native editor and by Muath (A4, A5)
2026-12-02  Phase 1 done: events, keys, tracing; Paddle account open (A6)
2026-12-15  addendum Part 2 signed (A9): bridge, re-onboarding, fixtures
2027-01-07  Phase 2 done: governor clean, verbatim per turn, first episodes end to end
2027-02-03  Phase 3 done: Salma's intake and the first call on real phones
2027-02-15  counsel's review of legal/ (A8)
2027-02-25  Phase 4 done: the full call; after-pass under 10 minutes
2027-03-08  Phase 5 done: proof, baseline recording, checkout
2027-03-12  Phase 6 done: restore rehearsed (NFR-207); pilot learners re-onboarded; cost exit document
2027-03-15  freeze at 12:00 UTC
2027-03-17  beta opens; cohort 1 invited (E16-S01)
2027-03-23  first weekly proof (day 7); first checkout (day 7)
2027-04-13  first finales (day 28, P1)
2027-04-20  gate review (day 35)
```

Three other chains come within days of it: counsel's confirmation (A1) gates the production apply; the Paddle account (A6) gates checkout in Phase 5; the native read of the bibles (A4, A5) gates `native/ar` and the shippable English package.

## 5. Team assumption, cuts and manual substitutes

**Plan of record (ADR-24.11, register A2): two engineers from build start, 2026-11-18** (E1: backend, pipeline, infrastructure; E2: web and the call), plus Muath on prompts, the packages, the vendor tests, counsel and beta operations. The beta opens **Wednesday 2027-03-17**. Each week the second engineer starts later moves the open a week (a start on 2026-11-25 gives 2027-03-24). A third engineer from 2026-12-01 gives 2027-02-17. One engineer gives 2027-07-07, which ADR-24.11 treats as no beta plan: the date is recomputed once a second engineer starts. There is no fixed-date trigger: the open is re-forecast weekly from measured velocity and moves earlier only in whole weeks with the 15% buffer intact.

**The single-engineer cut list applies from day one, except Terraform (ADR-24.B19).** Terraform stays; a console setup with a written runbook is only the fallback if Terraform is not applying by the end of build week 1. The other cuts, and what they do to the stories:

| Cut (source) | Effect on the backlog |
|---|---|
| No admin pages beyond staff sign-in and the review queue (01, 07, 08) | The measures page (E15-S07), the privacy page (E13-S11), the gates page (E15-S09) and the vendor page (E14-S07) are *Later*, with SQL in the 08:30 checklist until then; `/admin/cost` and `/admin/audit` are cut |
| Sign in with Apple and Google to P1 (01, 06) | E06-S10 stays P1; email code only |
| No autoscaling: two fixed call-worker tasks, about 16 concurrent calls (01) | Enough for 50 learners a week; NF-24 tests 15 concurrent calls |
| The Show tab and the proof beyond the simple proof move to the beta (01) | E07-S11 due day 28; E11-S03 ships the simple proof |
| `prewrite_extra`, the dial-in experiment, the HLS fallback later (01, 02) | E05-S13 stays P1 |
| Streaming writer and name-verification loop to P1; offline suite beyond 10 fixtures to P1; reviewer page as a list and a form; seasons and finale rules in code later (02) | E04-S10 uses respellings only; E15-S03 runs law scan, governor and editor; E15-S08 is a list and a form; E04-S12 holds arcs in the bible excerpt until day 21 |
| `research_transcripts`, the briefs cache, conversation chunks and skill snapshots to P1 (04) | E13-S07 is P1; the off-by-default switch stays in E10-S06 and is never asked in onboarding (ADR-24.B6) |
| Assessment for a small team: verbatim, analyst, memory keeper, updater as counts, event claims and the simple proof first (05) | E09-S02, S03, S07, S08, S09 are *Later*; only event claims ship until a second tagger exists (ADR-24.14) |
| Polling only; no signed-in install handoff; tap-only phrase selection; share page as a plain link; no crossfade; manual device checklist (06) | E06-S09, E06-S01 and E07-S12 rewritten to match |
| Conserve mode dropped, halt only; monthly reconcile by hand (08) | E14-S04 rewritten; E12-S08 stays P1 |

**Manual substitutes.** Each *Later* story whose due day comes after a learner could first reach it carries an `Until it ships:` line, and E15-S06 holds the runbook lines with an owner and a time limit. The ones that touch a learner:

| Until this story ships | The substitute | Limit |
|---|---|---|
| E13-S06, E03-S11 automated purge and export (day 35) | E13-S13: access ends at once and the key is destroyed on request, with no grace (ADR-24.B1); the purge runbook; export prepared by hand (ADR-24.B7) | Purge 24 hours; export 72 hours, 1 hour once automated |
| E12-S07 one-tap cancel (day 21) | Paddle's cancel link in every receipt; "cancel" in Controls is completed in Paddle by the on-call | Same working day |
| E12-S10 plan changes (day 28) | "Change plan" in Controls, completed in Paddle by the on-call | One working day |
| E12-S11 failed payments (day 37) | Paddle's own failed-payment emails and retries; the 7-day grace applied by hand | 7 days |
| E07-S11 Show tab (day 28) | The private feed is the archive | none |
| E10-S04 about-you card (day 6) and E03-S10 edits (day 6) | Facts corrected by telling the host or Salma (E09-S10); sensitive facts stay in their session | At once |
| E10-S02 veto (day 14) | A veto said to Salma or the host is applied by hand from the transcript | One working day |
| E09-S07 "where do I stand" (day 21) | Salma says plainly she cannot say reliably yet | none |
| E13-S11, E15-S07, E15-S09 pages (days 14 to 29) | SQL in the 08:30 checklist; the 15-minute voice deletion itself is automatic (E13-S05) | Daily |
| E13-S10, E15-S08 review pages (day 21) | A tokenized sheet export for the native reader | Monthly |

## 6. Capacity check

### 6.1 How the days are counted

Sizes are unchanged from the 2026-11-06 backlog: S = 0.5, M = 1, L = 2.5 engineer-days. E01-S05 is back at L, because Terraform stays. Nine P0 stories are Muath's time and are left out of the engineering totals (7.5 days): E02-S01, E02-S02, E02-S03, E02-S06 (vendor tests and the package), E13-S02 (register and counsel), E16-S01, E16-S02, E16-S05, E16-S09 (beta operations, the false-claim audit as auditor, the gate review).

### 6.2 Day-1 and the open date

| Phase | Engineer-days | Dates (plan of record) |
|---|---|---|
| 1 Foundation | 18.0 | 18 Nov to 2 Dec 2026 |
| 2 Pipeline and the minimal call | 38.5 | 3 Dec 2026 to 7 Jan 2027 |
| 3 Onboarding, Today, feed | 32.5 | 8 Jan to 3 Feb |
| 4 The full call and the after-pass | 27.5 | 4 to 25 Feb |
| 5 The first week's surfaces | 13.0 | 26 Feb to 8 Mar |
| 6 Production and the exit | 7.0 | 9 to 12 Mar |
| **Day-1 total** | **136.5** (108 stories) | |

**The arithmetic.** Engineers work 5 days a week; the seven weekdays from 2026-12-24 to 2027-01-01 count half. Day-1 with a 15% buffer is 136.5 × 1.15 = 157.0 engineer-days. Two engineers from 2026-11-18 have 52 by 2026-12-23, 7 more in the half-capacity week and a half, and reach 157.0 on Thursday 2027-03-11; with Friday 03-12 the build has 159.0 (a 16.5% buffer). The two-day freeze and the next Wednesday give the open.

| Staffing | Day-1 plus 15% reached | Open (Wednesday) |
|---|---|---|
| **Plan of record: two engineers from 2026-11-18** | 2027-03-11 | **2027-03-17** |
| Second engineer from 2026-11-25 (each week later adds a week) | 2027-03-16 | 2027-03-24 |
| Third engineer from 2026-12-01 | 2027-02-08 | 2027-02-17 |
| One engineer | 2027-06-30 | 2027-07-07 |

**Week by week, plan of record.** Capacity is in engineer-days; "done" is cumulative capacity spent on Day-1 work (136.5 plus the buffer, spread evenly to 03-12).

| Build week | Dates | Capacity | Done | Phase in progress |
|---|---|---|---|---|
| 1 | 18 to 24 Nov | 10.0 | 10.0 | 1 |
| 2 | 25 Nov to 1 Dec | 10.0 | 20.0 | 1 |
| 3 | 2 to 8 Dec | 10.0 | 30.0 | 1, 2 |
| 4 | 9 to 15 Dec | 10.0 | 40.0 | 2 |
| 5 | 16 to 22 Dec | 10.0 | 50.0 | 2 |
| 6 | 23 to 29 Dec | 6.0 | 56.0 | 2 (half capacity) |
| 7 | 30 Dec to 5 Jan | 7.0 | 63.0 | 2 (half capacity; no releases 31 Dec to 2 Jan) |
| 8 | 6 to 12 Jan | 10.0 | 73.0 | 2, 3 |
| 9 | 13 to 19 Jan | 10.0 | 83.0 | 3 |
| 10 | 20 to 26 Jan | 10.0 | 93.0 | 3 |
| 11 | 27 Jan to 2 Feb | 10.0 | 103.0 | 3 |
| 12 | 3 to 9 Feb | 10.0 | 113.0 | 3, 4 |
| 13 | 10 to 16 Feb | 10.0 | 123.0 | 4 |
| 14 | 17 to 23 Feb | 10.0 | 133.0 | 4 |
| 15 | 24 Feb to 2 Mar | 10.0 | 143.0 | 4, 5 |
| 16 | 3 to 9 Mar | 10.0 | 153.0 | 5, 6 |
| 17 | 10 to 12 Mar | 6.0 | 159.0 | 6 |

**Third-engineer variant, in one line:** a third engineer from 2026-12-01 adds about 5 engineer-days a week from build week 3, reaches Day-1 plus 15% on 2027-02-08, and opens the beta on 2027-02-17.

Day-1 grew from 121.5 in the first re-cut to 136.5. Three rulings and one capacity fact add 15 days: Terraform stays (+1.5, ADR-24.B19); the baseline recording is Day-1 (+2, ADR-24.B21); the weekly proof, checkout, the day-6 email, the return episode and the feed tag are reached in the first beta week, and that week has about 8 engineer-days, not enough to build them after the open (+10.5); the Haiku comparison is a build measurement (+1). The cuts and substitutes of section 5 moved 37 engineer-days out of Day-1.

### 6.3 The split, by epic

| Epic | Stories | Day-1 | Later in the beta | P1 | Muath (P0) |
|---|---|---|---|---|---|
| E01 Platform foundation | 9 | 10.5 | 0 | 0 | 0 |
| E02 Vendor tests and language gate | 9 | 4.5 | 0 | 2.0 | 5.0 |
| E03 Learner model | 11 | 12.5 | 4.5 | 0 | 0 |
| E04 Pipeline | 13 | 16.5 | 2.0 | 0 | 0 |
| E05 Live call | 13 | 14.5 | 0 | 2.5 | 0 |
| E06 Onboarding | 12 | 12.5 | 1.0 | 1.0 | 0 |
| E07 Daily loop | 13 | 17.0 | 1.0 | 0 | 0 |
| E08 Feed and cue | 7 | 6.0 | 1.0 | 0 | 0 |
| E09 Assessment | 11 | 7.5 | 7.0 | 0 | 0 |
| E10 Notebook and controls | 9 | 1.0 | 6.5 | 1.0 | 0 |
| E11 Proof and seasons | 10 | 6.0 | 2.5 | 3.5 | 0 |
| E12 Plans and payments | 11 | 5.5 | 2.5 | 1.0 | 0 |
| E13 Privacy and security | 13 | 8.0 | 4.5 | 1.0 | 0.5 |
| E14 Cost | 8 | 6.0 | 1.0 | 0 | 0 |
| E15 Evals and operations | 11 | 8.5 | 3.0 | 0.5 | 0 |
| E16 Beta | 10 | 0 | 0.5 | 5.5 | 2.0 |
| **Total** | **170** | **136.5** (108) | **37.0** (37) | **18.0** (14) | **7.5** (9) |

All P0 together: 181.0 days, 173.5 of them engineering.

### 6.4 *Later in the beta*, by due day

Each story carries `Due: beta day N (date)` on its size line and in the `due` column of `stories.csv`. It must be live by the morning of its due day.

| Due day (date) | Stories | Engineer-days |
|---|---|---|
| 6 (2027-03-22) | E03-S10, E10-S04, E10-S05 | 3.0 |
| 7 (2027-03-23) | E08-S05, E08-S07, E11-S07 | 2.0 |
| 8 (2027-03-24) | E04-S11 | 1.0 |
| 14 (2027-03-30) | E03-S03, E09-S02, E10-S01, E10-S02, E11-S08, E15-S07 | 7.5 |
| 15 (2027-03-31) | E16-S07 | 0.5 |
| 21 (2027-04-06) | E04-S12, E09-S03, E09-S07, E09-S11, E10-S07, E12-S07, E13-S10, E15-S08 | 7.0 |
| 28 (2027-04-13) | E07-S11, E09-S08, E09-S09, E10-S03, E10-S08, E12-S06, E12-S10, E13-S11, E14-S07 | 8.0 |
| 29 (2027-04-14) | E15-S09 | 1.0 |
| 30 (2027-04-15) | E11-S10 | 0.5 |
| 35 (2027-04-20) | E03-S11, E06-S01, E13-S06 | 6.0 |
| 37 (2027-04-22) | E12-S11 | 0.5 |

Muath's two *Later* stories are E16-S05 (the first monthly audit, day 31) and E16-S09 (the gate review, day 35).

| Beta week | Later P0 due | Capacity (2 engineers, 80% after on-call and support) | Balance |
|---|---|---|---|
| 1 (17 to 23 Mar) | 5.0 | 8.0 | +3.0 |
| 2 (24 to 30 Mar) | 8.5 | 8.0 | -0.5 (covered by week 1) |
| 3 (31 Mar to 6 Apr) | 7.5 | 8.0 | +0.5 |
| 4 (7 to 13 Apr) | 8.0 | 8.0 | 0 |
| 5 (14 to 20 Apr) | 7.5 | 8.0 | +0.5 |
| **Beta total** | **36.5** (+0.5 on day 37) | **40.0** | **+3.5** |

Every due day is met cumulatively (the tightest is day 14: 13.5 due against 14.4 available). P1 adds 18.0 days with no due day; about 3.5 fit before the gate review, so most P1 ships in season two unless measured velocity is better than the sizes. The 15% buffer is spent on Day-1 only; the beta has no buffer beyond the 20% on-call reserve, which is the honest weak point of this plan.

### 6.5 What moves the date

ADR-24.11 re-forecasts the open at the end of every build week from measured velocity: it moves earlier, in whole weeks, only when the remaining Day-1 work plus 15% fits before the earlier Wednesday, and it never moves later without the waitlist being told. The levers, in order of effect: a third engineer from 2026-12-01 (open 2027-02-17); velocity above the sizes, measured from Phase 1. A second engineer who starts late moves the open a week for each week of delay.
