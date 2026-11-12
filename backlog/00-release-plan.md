# For one: the release plan

*Written 2026-11-06; re-cut 2026-11-12 under ADR-25 ([architecture/10-decision-records.md](../architecture/10-decision-records.md)), which wins over ADR-24 where they differ. Companion to `01-epics.md` (16 epics), `02-stories/` (167 stories: 144 v1, 21 v1.1, 2 later), `03-non-functional-stories.md` (28), `04-risks-and-blockers.md`, `05-traceability.md` and `stories.csv`. The visual version is the page "For one release plan": https://claude.ai/artifact/NFcJZpKpupvoVyH59Mhwjc (source: `release-plan.html`).*

**How to read this plan.** There are no dates (ADR-25.1). An AI coding agent builds For one story by story under Muath (ADR-25.2), in six phases ordered by dependency. A phase is done when its exit check passes, not when a week ends. Version 1 launches once, publicly, with open signup, when every v1 story passes and the launch checklist in section 4 is green (ADR-25.5). There is no trial run before launch and no beta. Every story says `Release: v1` (needed at launch) or `Release: v1.1` (after launch, in the order learners reach it). Sizes S, M and L are relative complexity, not time.

## 1. How the work is done

1. **One story at a time.** The agent picks the next v1 story whose dependencies are done, in phase order.
2. **Tests first.** The story's acceptance criteria are committed as failing tests before any code; CI checks the order (E01-S10).
3. **Code, then CI.** Lint, types, tests and the mapped eval suites (`eval-gate`) must pass.
4. **An independent AI review.** A second AI reviewer that did not write the change reads the diff, the story and the laws; a blocking finding fails the check.
5. **Muath approves** every merge to `main`, every database migration, every prompt or bible change and every production deploy (register A8). The agent never approves its own change.
6. **Operations.** Automated fallbacks first (yesterday's episode stays; the call falls back to voice notes); alerts go to Muath; runbooks are scripts the agent runs when Muath asks (E15-S06).

Muath's own actions are in architecture 10 §10 (A1 to A9). Each is tied to the phase that needs it below, never to a date.

## 2. The phases

| Phase | What is built | Needs first | Exit check |
|---|---|---|---|
| **1. Foundation and vendor choice** | The repo, CI and the agent's workflow (E01-S01 to S06, S10); events and the word bank (E03-S01, S02); keys (E13-S01); the processor register, DPIA and self-review checklist (E13-S02); price book and tracing (E14-S01, S02); logging and alerts (E15-S01); fixtures from synthetic learners, scripted calls and volunteer clips (E15-S02); the web shell (E07-S01); the volunteer clips and the corpus, the recognizer and voice tests (E02-S01 to S03); the English package with its gate result (E02-S06) | Vendor accounts and keys (A1); volunteer clips and blind raters (A2) | A story's tests precede its code in CI and nothing merges without Muath's approval; every test render is a priced row; the scrub test passes; `vendors.yaml` holds the measured winners (M2, M3) |
| **2. The pipeline and the minimal call** | The rest of the model's tables and the briefs (E03-S04 to S06); the pipeline from teacher to batch and the variety system (E04-S01 to S07, S11); the minimal call-worker, the governor and verbatim turns (E05-S01 to S03); the 50 scripted calls and the adapters (E02-S04, S05); the bibles in the packages (E02-S07); media and per-learner keys, the deploy pipeline (E01-S07, S08); the eval gate and release manifest (E15-S03, S05); cost roll-up (E14-S03); sign-in, the player and the event queue (E07-S02 to S04) | Phase 1; Muath's read of the bibles (A3) | 20 test episodes for synthetic learners end to end with measured cost; host reply median under 1.5 s on the 50 calls; the governor replay on synthetic transcripts is clean |
| **3. Onboarding, Today and the feed** | The plain landing page and open signup, A1 to A10 (E06-S02 to S09); on-demand kinds, ideas, casting (E04-S08 to S10); Salma's intake and the first call (E05-S04, S05); onboarding writes and event ingestion (E03-S07, S08); Today, the article, swap, the small door, sessions and doors (E07-S05, S06, S09, S10, S13); the feed, the drop, push and the feed tag (E08-S01 to S04); allowance and the trial (E12-S02, S03); consent and the age gate (E13-S03, S04) | Phase 2 | On real phones: first sound under 60 s, the first episode plays under 45 s after intake, first spoken sentence under 5 minutes; the feed plays in three podcast apps |
| **4. The full call and the after-session pass** | Hold-to-talk, the word button, recall gaps, the retell, anxiety mode, the voice-note fallback, crisis step-out (E05-S06 to S11); the call screen and chat (E07-S07, S08); verbatim, the edit classifier, measures, analyst, memory keeper, after-pass, the avoidance flag, wrong-memory fix (E09-S01 to S06, S10, S11); the structure map and applying the after-pass (E03-S03, S09); arcs and seasons in code (E04-S12); week-one questions (E06-S12); voice deletion in 15 minutes, crisis protocol, output and correction guards (E13-S05, S08, S09); spend guard, alarms, the Haiku comparison (E14-S04 to S06); alert rules, the fallback episode (E15-S04, E04-S13) | Phase 3 | Zero governor violations on the 50 calls; after-pass under 10 minutes p99; a crisis keyword with no confirmation fires the protocol within 2 seconds; storage-off audio is gone within 15 minutes |
| **5. The first week's surfaces** | The claim gate, claims, the simple weekly proof and its screen (E11-S01 to S04); the baseline then-and-now recording (E11-S05, E05-S12); the season goal and the mid-season rehearsal (E11-S07, S08); skills, "where do I stand" and the recording rater (E09-S07, S09); the notebook: working on with veto and add, words you own, about-you, hours, why, Salma explaining, life updates, edits (E10-S01 to S08, E03-S10); the return episode, gap note, rhythm (E08-S05 to S07); plans, Paddle checkout, the day-6 email, cancel and refund, plan changes (E12-S01, S04, S05, S07, S10) | Phase 4; the Paddle account for live checkout (A5; the sandbox works before it) | A synthetic learner's first week produces a proof built only from events; checkout, plan change, cancel and refund round-trip in Paddle's sandbox |
| **6. Production and the exit** | Production from the same Terraform and a restore rehearsal (E01-S09); automated deletion, export and `privacy/verify` (E13-S06, S11, E03-S11); the incident runbook and tabletop (E13-S12, E15-S06); the device checklist (E07-S12); synthetic learners and the canary (E15-S10); staff roles, review sampling, measures and the false-claim audit tooling (E13-S10, E15-S07, S08, E11-S10); the launch rehearsal (E06-S11); the cost exit document (E14-S08) | Phase 5; the domain (A6) | A full restore into staging within 4 hours; `privacy/verify` passes on a deleted rehearsal account; the launch rehearsal meets the onboarding budgets; measured cost per session with a costed path to $0.35 |

## 3. The longest chain

The order below is the critical path. A delay anywhere on it delays launch; nothing else does.

```
Vendor accounts (A1) and volunteer clips (A2)
  -> recognizer and voice tests; vendors.yaml (phase 1)
  -> minimal call-worker; 50 scripted calls; governor clean (phase 2)
  -> Salma's intake and the first call on real phones (phase 3)
  -> the full call; after-pass under 10 minutes (phase 4)
  -> the first week's proof and checkout (phase 5)
  -> production, restore, the launch rehearsal (phase 6)
  -> launch checklist green; Muath approves the production deploy; signup opens (E16-S01)
```

Three side chains join it: the bibles (Muath's read, A3) before the writer and host prompts are tuned in phase 2; the Paddle account (A5) before live checkout in phase 5; the self-review of `legal/` (A4) before launch.

## 4. The launch checklist

Version 1 launches when every line is green. Muath ticks each one; the agent produces the evidence.

1. Every v1 story's acceptance tests pass in CI on `main`, and every phase exit check above has passed.
2. The non-functional stories in `03-non-functional-stories.md` pass for v1: latency budgets, cost tracing, deletion windows, no personal data in logs, AI disclosure and crisis, the laws in lint, the eval gate, security testing (NF-28).
3. `eval-gate` is green on the release: law scan, governor replay, editor, injection set (zero disclosures of the brief).
4. The self-review checklist (`legal/00-self-review-checklist.md`) has a final position for every question; every legal text (privacy notice, terms, consent strings, crisis wording) passed the AI review pass and Muath's approval (A4); the DPIA and RoPA are complete.
5. Every vendor in `vendors.yaml` has its standard DPA accepted and its training opt-out recorded (A1); zero data retention requested from Anthropic.
6. An EU and UK representative is appointed if the company is outside the EU and UK (A7).
7. Paddle is live, with the three prices, the 7-day trial without a card and the 14-day refund (A5).
8. The domain is live with email sending (A6).
9. Production restored once into staging within 4 hours; backups at 30 days with point-in-time recovery.
10. The launch rehearsal on production: first sound under 60 s, the first episode under 45 s after intake, first sentence under 5 minutes, five nights of drops with none missed.
11. Measured cost per session on production with a costed path to $0.35; the daily spend cap and halt tested.
12. Alerts reach Muath; runbooks R1 to R4 and R12 rehearsed by the agent on staging; the crisis fail-safe tested.
13. Security checks green (ADR-25.11): dependency and secret scans clean in CI, an OWASP ZAP baseline of staging with no open high finding, and the AI security review passed on every change that touched auth, keys, media URLs, the feed or deletion. There is no paid penetration test at launch.
14. The English package is shippable (all five gate checks); `native/en` ships, and `native/ar` only if Muath has read Salma's Arabic and its blind test (M8) passed.

## 5. What is v1, what is v1.1, what is later

**v1 (built before launch).** Everything a learner can reach in their first weeks, and every rule the PRD marks P0: the plain landing page and open signup; onboarding A1 to A10; week-one questions and the baseline recording; the web app with Today, the player, the article, the call screen, the chat, one swap, the small door, sessions and doors, the controls sheet; the pipeline with batch, on-demand kinds, the variety system, arcs and seasons, the return and fallback episodes; the private feed and Today (the archive until the Show tab), the drop and push; the call with hold-to-talk, the word button, recall gaps, the retell, anxiety mode and the voice-note fallback; learner-model writes, the classifier, measures, the analyst, the memory keeper and the after-session pass; the claim gate (event claims only until calibration), the simple weekly proof, the mid-season rehearsal, the recording rater; the notebook in full; plans, Paddle checkout, cancel, refund and plan changes; per-learner keys, consent (including the conversation-content consent), voice deletion in 15 minutes, automated deletion and export, the crisis protocol with its fail-safe, the guards; cost tracing, the spend guard and alarms; logging, alerts, runbooks, measures, the AI review read, the audit tooling, the eval gate, the canary.

**v1.1 (after launch; P1 in the PRD).**

| When it is first needed | Stories |
|---|---|
| Soon after launch | The sample episode on the landing page (E06-S01); the Show tab (E07-S11; the feed and Today are the archive at launch); the launch health page (E15-S09); the per-language close rule (E16-S07) |
| A month after launch | The calibration set from opted-in data (E09-S08) and metric unlock (E11-S06); the first false-claim audit (E16-S05); the failover drill (E14-S07); the 4-week health review (E16-S09) |
| Before the first renewal | Our own failed-payment grace mechanics (E12-S11; Paddle's dunning covers launch) |
| Behind flags | Round two and the dial-in experiment (E05-S13); the finale and the tape (E11-S09, E10-S09, E16-S06); the gate harness and a second language (E02-S08, S09); research de-identification (E13-S07); billing reconcile (E12-S08); vendor regression (E15-S11); the cost path (E16-S08); shadowing (E16-S04) |

Until a v1.1 story ships, its surface does not exist; nothing is faked by hand (ADR-25.5).

**Later.** Regional prices (E12-S09); the plan after the 8-week review (E16-S10); character creation and the six chassis; the scout; the observer in the call; native apps (not planned, ADR-25.4); the learner's cloned voice; referral programs; paid acquisition; employer seats.

**Never built, by decision 3.** Salma's correction notes after the call, the margin note in chat, the polish card, any "the correct answer is" surface.

## 6. What v1 deliberately leaves out

| Left out | Why, and what stands in |
|---|---|
| Admin pages beyond staff sign-in, the review queue and the measures page | Muath reads SQL views as `forone_human` and the Inngest dashboard; the health page arrives in v1.1 |
| Autoscaling of the call-worker | Two fixed tasks, about 16 concurrent calls; NF-24 tests 15 |
| Sign in with Apple and Google | Removed (ADR-25.4); email one-time code only |
| The streaming writer, the name-verification loop | Respellings only; the split call meets the first-episode and sample budgets |
| Conserve spend mode | Halt only on the daily cap |
| A signed-in install handoff, SSE, phrase drag, a share page, crossfades, the Playwright device suite | Polling, one email code in the installed app, tap-only selection, a download link, a manual device checklist |
| `research_transcripts` and the briefs cache | The data-use switch exists, off by default; nothing reads transcripts for research before E13-S07 |
| The fuller weekly proof | The simple proof from first-ever events and words owned |

## 7. After launch

The beta gates are now **launch health measures** (ADR-25.5), read 4 and 8 weeks after launch with the same targets and stop lines (PRD Part 16; E16-S09): trial to paid, week-4 active, sessions a week, minutes of speech, the 4-week recording, renewal, worth it, cost per session, false claims and wrong memories. Each review names the one change each failed measure implies. Nothing in this plan is scheduled by date; v1.1 follows the order in section 5.
