# 3. The schedule, day by day

*Milestone 0 pilot kit. Re-dated on 23 October 2026 (the pilot had not started): Saturday 24 October to Wednesday 18 November 2026, in Muath's time (Saudi time); learners anywhere get their slot in their own time. Two cohorts so intake calls fit in two days: **cohort A** has its intake on Saturday 31 October and starts Sunday 1 November; **cohort B** has its intake on Sunday 1 November and starts Monday 2. "Day 1" is each learner's first episode. Each learner also has one day off a week that they chose.*

Concept v2 planned 14 days with 15 learners from 12 October to 1 November. This keeps the same shape 16 to 17 days later: recruiting first, then 14 days of episodes, then rating and the gate. The beta's dates move by the same amount (build from 18 November, founding beta from 23 December to 26 January). Concept v2 and PRD v2 now show the same dates (checked 23 October).

## Before the pilot

| Date | Muath does | Learners |
|---|---|---|
| **Sat 24 Oct** | Accounts and tools: second WhatsApp number, Google Drive folders, Claude Projects with training off, AI Studio with billing, ElevenLabs Pro ([04-production.md](04-production.md#one-time-setup-saturday-24-to-thursday-29-october), steps 1 to 4). Build the screening form. **Post the recruiting message** in the evening and message 20 to 30 people directly ([01-recruiting.md](01-recruiting.md)). | |
| **Sun 25 Oct** | Pick the voices; build the Mona template agent and test its link on your phone; make the then-and-now audio ([06-then-and-now.md](06-then-and-now.md)). Build the consent form. Answer applicants; ask for their voice notes. | Apply |
| **Mon 26 Oct** | Score applicants as they arrive (Screening tab). Duplicate the agent 15 times. | Apply, send voice notes |
| **Tue 27 Oct** | Keep scoring. Second round of posts in groups if under 20 applicants. | Apply, send voice notes |
| **Wed 28 Oct** | Recruiting closes 23:59. | Last applications |
| **Thu 29 Oct** | **Choose 15 and 3 reserves**; send accepted, reserve and waitlist messages with the consent form and intake times. **Dry run on yourself as L00** and time it. Decide the payment method for the pre-pay ask. | Sign consent, book intake |
| **Fri 30 Oct** | Spare day: chase missing consents, finish anything the dry run showed was slow. | Sign consent |

## The pilot

| Date | Cohort A (L01 to L08) | Cohort B (L09 to L15) | Muath, in the evening |
|---|---|---|---|
| **Sat 31 Oct** | Intake calls (about 15 min each); week-0 recording the same day | | Fill learner files (prompt I). Make A's pilot episodes (2 to 3 min) and short first-call briefs |
| **Sun 1 Nov** | **Day 1**: pilot episode, first call (2 min) | Intake calls; week-0 recording | First full evening cycle for A. B's pilot episodes |
| **Mon 2 Nov** | Day 2 | **Day 1** | Full cycle |
| **Tue 3 Nov** | Day 3 | Day 2 | **Last day to swap in a reserve** for anyone who has not started or has dropped |
| **Wed 4 Nov** | Day 4 | Day 3 | Full cycle |
| **Thu 5 Nov** | Day 5 | Day 4 | Full cycle |
| **Fri 6 Nov** | Day 6 | Day 5 | Weekend: expect more listening, different times. Weekly costs into the Costs tab |
| **Sat 7 Nov** | Day 7: **day-7 check-in** | Day 6 | Full cycle |
| **Sun 8 Nov** | Day 8 | Day 7: **day-7 check-in** | **Mid-pilot review** (below) |
| **Mon 9 Nov** | Day 9 | Day 8 | Make the next personal episode on a *6 Minute English* topic for the **side-by-side** ([07](07-measures-and-gates.md#the-side-by-side-with-a-human-made-show)) |
| **Tue 10 Nov** | Day 10 | Day 9 | Side-by-side for B |
| **Wed 11 Nov** | Day 11 | Day 10 | Full cycle |
| **Thu 12 Nov** | Day 12 | Day 11 | Full cycle |
| **Fri 13 Nov** | Day 13 | Day 12 | Make A's finale episodes (writer mode FINALE). Weekly costs |
| **Sat 14 Nov** | **Day 14: finale**, **day-14 check-in** | Day 13 | Make B's finale episodes |
| **Sun 15 Nov** | Day 15: **week-3 recording** and the **pre-pay message**. No new episode: count who asks for one | **Day 14: finale**, day-14 check-in | Collect A's recordings |
| **Mon 16 Nov** | No episode; count unprompted asks | Day 15: week-3 recording and pre-pay message | Run `blind_pairs.py` on A's recordings; send pairs to the teacher; Muath rates too |
| **Tue 17 Nov** | | No episode; count unprompted asks | B's pairs rated. Unblind; transcript measures (prompt R); send each learner their **then-and-now message** (prompt F) with both clips. Pre-pay closes 23:59. Fill the Gates tab. Write the gate report (below) |
| **Wed 18 Nov** | | | **Gate decision**: start the beta build, or rethink the claim that failed |

From Sunday 15 November, learners who ask for more get a warm answer: "Season one is over; the next season starts with the beta in December. I'll let you know first." Their asks are the gate-1 count.

## The mid-pilot review (Sunday 8 November, about an hour)

Look at the tracker and the Notes column for the first week, then decide.

- Who has had no session for 3+ days? (Return episodes are going out; the gap note too, if they opted in. Nothing else.)
- Reactions and call rates by episode type: is anything clearly broken (a voice, a format, the call link, the article length)?
- Day-7 check-in answers: "stressful" calls, "less than half" understood, the voice mismatch, anyone who "often" felt corrected or tested.
- The Echoes tab: are echoes being logged for everyone? An empty tab on day 8 means gate 8 cannot be read.
- Production minutes: is the evening sustainable to day 14?

**Change only what is broken or harmful.** Changing the design mid-pilot blurs every comparison. Write any change, with its date, in the tracker's Changes tab.

## The gate report (Tuesday 17 November)

One page in `For one M0/`, for Muath and for the next build threads:

1. The Gates tab, each line pass, fail or stop.
2. Personal versus generic, per learner.
3. Five quotes from learners, good and bad, in their words.
4. Every reason anyone gave for stopping.
5. Cost per session and production minutes per learner, measured.
6. Which claim, if any, failed, and the one change it implies for the beta (see [07-measures-and-gates.md](07-measures-and-gates.md#reading-the-results-on-18-november)).
