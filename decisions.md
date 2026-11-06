# For one: the decisions, once

*Synthesis of the first rethink and the eleven lens perspectives, 2026-10-09; updated 2026-10-23 with Muath's answers. Companion to [concept-v2.md](concept-v2.md) and the page "For one, concept v2" (https://claude.ai/code/artifact/7064a875-8cc4-41b8-a571-494d3e99d639).*

The twelve threads asked Muath 48 questions. Many are the same question asked from a different angle, so they collapse into **10 real decisions**, plus **6 that every lens agrees on** and that stand unless he objects. They are ordered so the ones that change everything else come first. Each decision lists which questions it absorbs, the recommendation, and the one-line consequence of each option. Evidence and judgment are kept apart: "Evidence" lines cite what a lens found; "Why I picked it" is the synthesis's judgment.

## Status on 2026-10-23

| # | Decision | Status |
|---|---|---|
| 1 | Who it is for, and which languages | **Decided by Muath:** no first learner, no launch country or group; as many languages as the speech technology supports well |
| 2 | Price and allowance | **Decided by Muath:** monthly only, tiers by new episodes a day, prices set from the cost, pricing psychology used to push people to subscribe. Costed below as $19.99 / $29.99 / $44.99 |
| 3 | How teaching works | **Decided by Muath:** invisible; the AI answers "you meant…" and corrects the sentence inside the conversation, never "you are wrong, the correct answer is" and never a pop-up |
| 4 | Evidence instead of "no tests" | **Agreed by Muath** with the recommendation |
| 5 | A series | **Accepted** with Muath's Oct 10 "continue" (taken as go-ahead on all five recommendations); not changed on Oct 23 |
| 6 to 10 | Cue, platform, personalization depth, data use, how the beta earns | Open; built on the recommendations (10a adjusted for monthly-only pricing) |

## The five that gate everything

1. **Who it is for and which languages:** anyone, anywhere; every target language that passes the language gate (decided).
2. **Price and daily allowance:** 1 a day $19.99, 2 a day $29.99 (recommended), 3 a day $44.99, monthly; listening unlimited (decided; tiers costed).
3. **How teaching works:** invisible, through the hosts' conversation only (decided).
4. **Evidence instead of "no tests":** recall in conversation, a 60-second word check, a then-and-now recording every 4 weeks, and a notebook the learner can open. Still no points, streaks or levels (agreed).
5. **A series, not one-offs:** plot may persist across episodes, obligation never; 4-week seasons with a real goal (accepted).

---

## 1. Who it is for, and which languages

**Absorbs 7 questions:** rethink #1 (who is the first learner) and #2 (launch language), market #1 (launch market) and #3 (languages at launch), business #1 (launch wedge), voice #1 (first target language), architecture #3 (launch pair).

**Decided by Muath on 2026-10-23:** "we don't have a first learner, so we're not overfitting on a country or a people... the language, as much language as we can, that's going to be based off the technical limitation... but as much as possible."

All seven lenses had recommended one pair (English for Saudi Arabic-speaking adults at about B1). Muath overruled that. How the concept now carries it:

- **No launch country or group.** Every show is built from the learner's own life, so nothing is tuned to one culture. Level still matters: the show works best from about 2,000 known words, and the beginner version is the least tested.
- **A language gate instead of a list.** A target language opens when it passes five checks: blind native rating of the episode voices, learner speech transcribed without silently fixing errors (30 real clips), natural scripts judged by a native speaker, call latency of about a second, and a structure inventory. Details are in concept v2, section 8.
- **Milestone 0** recruits from anywhere through Muath's own network. Because episodes are checked by hand, its target language is English plus any language for which there is a native-speaker helper. The gate runs on the other candidate languages in parallel, and the beta opens in every language that passed.

**What this costs, kept visible:** each language needs its own calibration set, so progress claims in a new language start more cautious; quality is checked per language in the beta, and a language that falls well behind English on "worth it" closes until fixed; with no launch market there is no single channel or community to aim at (concept v2, section 10).

**Evidence (from the lenses, still true):** no voice vendor publishes per-language quality; dialect Arabic TTS still trails English (Habibi 2026); code-switching support varies by speech-to-text vendor (Deepgram's covers 10 languages and not Arabic).

## 2. Set the price and the daily allowance

**Absorbs 7 questions:** rethink #6 (price band), market #2 (what you sell), business #2 (price position) and #3 (daily allowance), architecture #1 (AI cost per session), voice #2 (voice budget), language acquisition A (session as the whole dose or the hub of a listening diet).

**Decided by Muath on 2026-10-23:** a monthly subscription; the cost calculation sets the price and the allowance; simple tiers such as one, two or three new episodes a day; use the psychology of pricing to push people to subscribe.

**What the synthesis set from that:**

| Plan | Price a month | Per episode | Margin, typical use, at $0.35 a session | Margin, every episode used |
|---|---|---|---|---|
| 1 a day | $19.99 | $0.67 | 63% | 38% |
| **2 a day (recommended)** | **$29.99** | **$0.50** | **59%** | **18%** |
| 3 a day | $44.99 | $0.50 | 63% | 18% |

- **Rule:** no plan loses money on a learner who uses every episode at the planning cost of $0.35 a session. Listening to what exists, the article, the chat and a round-two call stay unlimited on every plan.
- **Pushing people to subscribe, honestly:** the middle plan is marked "Recommended"; the top plan anchors it; 2 and 3 a day cost the same per episode, so 1 to 2 is the obvious step; "about $1 a day"; the 7-day trial starts on 2 a day; no free tier, only a 90-second sample episode; founding members keep their price while subscribed; the tutor comparison shown.
- **Never:** fake countdowns, fake scarcity, hard cancellation, guilt, pre-ticked upgrades.
- **The beta caveat:** at the beta's $0.55 to $0.60 a session, a 2 or 3 a day learner who uses everything costs more than they pay until the cost falls below $0.42 (at most about $560 a month across 50 beta learners).

**Still adjustable without reopening the decision:** the exact price points, the trial plan, and regional prices for lower-income countries (one USD list at launch). The assumptions behind the margins (15% to tax and fees; 60%, 50% and 45% of the allowance used) are estimates to replace with beta data.

## 3. How teaching works

**Absorbs 3 questions:** rethink #3 (correction law), language acquisition B (can the host "not understand" you), UI/UX #1 (who is the teacher on screen).

**Decided by Muath on 2026-10-23:** teaching is invisible. "In speaking... the AI can reply with you meant, and it corrects the sentence, not saying you are wrong, this is the correct answer." No pop-ups. "Similar to the first option."

How the concept now carries it (law 7):

- **In the call and chat, the hosts only converse.** An error gets a friendly echo with the right form ("oh, you went there yesterday?") and the conversation carries on. When the meaning is lost, a real "sorry, you what?". Recall gaps and the retell stay, because they are conversation, not correction.
- **The teaching moves into the episodes.** The planner brings the right forms of the learner's own mistakes back in the next episodes and calls, many times and naturally, until the learner uses them.
- **Dropped from the first version:** the after-call correction notes, the polish card, the chat margin note.
- **The producer stays, without correcting.** In the UI and UX thread Muath picked a producer as the teacher on screen (2026-10-23, four minutes after his answer here). Read together: the producer (for example "Salma") is the face of the app in the learner's own language. She runs onboarding, keeps the notebook, voices the weekly proof and explains when asked, and never corrects. If he wants her to give notes after all, that reverses this line.
- **Kept, because the learner asks:** a word given back when the learner says it in their own language, and an explanation when the learner asks "why do we say it like that?".
- **The weekly proof and notebook** show what the learner can now do and a "working on" list of at most 3 items. They are never a list of mistakes.

**The risk, kept visible:** every lens recommended some explicit feedback after the call, because echoing the right form is the least-noticed kind of feedback (uptake 31% for recasts against 88% for clarification requests in classrooms, Lyster & Ranta 1997; better one-to-one, Li 2010; immersion learners can stay inaccurate for years). The 4-weekly recording tests it: if an error survives two recordings, the teacher raises how often the right form comes back and how often the host echoes it, still without saying it was wrong. The observer role becomes the first thing to add after the beta, because it decides which form to echo next turn.

## 4. Rewrite "no tests, no levels" so the learner gets evidence

**Agreed by Muath on 2026-10-23** with the recommendation below.

**Absorbs 7 questions:** rethink #4 (honest progress), learning science A (may the show ask you to recall), personalization #1 (see the language side of the model) and #2 (60-second word check), assessment #1 (where do I stand), #2 (4-weekly speaking sample) and #3 (visible "working on" list).

**All seven point the same way**: keep the ban on game furniture, drop the ban on evidence. They differ only in how far to go. Each piece below can be accepted or refused on its own.

| Piece | Recommended | Consequence of refusing it |
|---|---|---|
| a. Recall in conversation | Hosts may set up moments where the learner pulls a word out of memory ("how did you put it on Tuesday?"). Never scored. | The planner can only re-expose words, the weakest way to keep them. |
| b. 60-second word check at signup | Optional "tap the words you know", with fake words mixed in, framed as "help the show pitch at your level". | Week 1, when people quit, is pitched from 3 or 4 guesses. |
| c. Then-and-now recording every 4 weeks | About 3 minutes, same task types each time, skippable, nothing scored on screen. It is the season finale. | No honest "you improved" claim about speaking is possible, because topic and task move the numbers more than a month of growth. |
| d. A notebook the learner can open | What the show knows about them (life and language), each fact with its source; a "working on" list of at most 3 items they can veto or add to; "why this episode". | Deep memory feels creepy instead of trusted; the learner cannot steer the teacher. |
| e. Honest progress surfaces | Words you own (in your own sentences), the tape, hours heard and minutes spoken, an "out in the world" log. | The learner cannot feel competence, the strongest motivator in the evidence. |
| f. "Where do I stand?" | Answered honestly with a range when asked ("listening around B1, speaking just below"), never pushed. | Learners with a real target (a job needing B2) leave to find out elsewhere, and "never hide what it is" is broken. |

**Never, under any option:** points, XP, streaks, levels on screen, percentages, leaderboards, charts, confetti, comparison with other learners.
**Evidence:** retrieval beats restudy, g = 0.50 (Rowland 2014); scores beside comments cancel their benefit, mostly for weak learners (Butler 1988); a 60-item yes/no word test takes about 3.5 minutes and predicts proficiency (LexTALE); stealth assessment alone correlates only 0.2 to 0.5 with external tests (Shute 2013).
**Why I picked it:** the original law protected learners from anxiety and gamification. These six pieces carry neither, and without them the trust contract's own promise, "prove progress honestly", cannot be kept.

## 5. Let the show be a series

**Absorbs 4 questions:** enjoyment #1 (story arcs), consistency #3 (seasons) and #4 (optional threads), personalization #5 (light continuity).

**All four agree** on continuity; they differ on season length (consistency 6 to 8 weeks, enjoyment 4 to 6, UI/UX 4).

| Option | Consequence |
|---|---|
| **Recommended: Law 4 becomes "every episode is complete; plot may persist, obligation never". Each learner's show gets a world (hosts, 3 to 5 recurring side characters, places, running jokes). Arcs of 1 to 3 weeks, at most 2 open, best drawn from the learner's real life (the interview: prep, the day, the debrief). The story waits for the learner. 4-week seasons, each with one real-world goal in the learner's words and a finale built on the then-and-now recording.** | Words come back naturally (one TV series needs about 11% fewer word families than unrelated shows and repeats rare words far more); a reason to return with no debt; the best defence against AI sameness. |
| Optional threads only, no seasons | Keeps continuity, loses the near goal and the fresh start that counters the week-4 novelty fade. |
| Keep strictly self-contained (current law) | Every episode is a one-off; word recycling falls to the scheduler alone; sameness risk is highest. |

**Why 4 weeks:** it lines the finale up with the 4-weekly recording, lands the first finale inside the beta's week-4 gate, and falls where gamification novelty starts to fade (Rodrigues 2022). A real goal that needs longer simply runs across two seasons.

## 6. Choose how the show reaches the learner each day and after a gap

**Absorbs 4 questions:** rethink #5 (reminders), enjoyment #2 (when the learner chooses), consistency #1 (weekly rhythm) and #2 (when a learner goes quiet).

**All four agree** on replacing "zero notifications" with one cue the learner designs.

| Option | Consequence |
|---|---|
| **Recommended: at the end of each session the learner picks tomorrow's episode from 3 ideas (or tells the hosts one). It drops once, at the time and place they chose ("on the bus at 7:40"), in the app and in their own podcast app through a private feed. A weekly rhythm with spare days ("4 days, 2 spare"), mentioned only in words. One opt-in note the learner writes to themselves at signup, sent once after a gap they choose. A return episode after any gap. No other message, ever.** | A cue during the 2 to 5 months before a habit runs itself; opening the app means pressing play; nothing to feel guilty about. |
| Zero notifications (current PRD) | Nothing reaches the learner during the habit window; time since the last visit is the strongest dropout predictor (Buyalskaya 2023). |
| Conventional reminders and streaks | They work for daily return (Duolingo: 84% next-day), but a broken streak lowers continuation (78% versus 53%, Silverman & Barasch 2023) and it gives up the counter-positioning against Duolingo. |

## 7. Decide what the beta runs on

**Absorbs 2 questions:** UI/UX #2 (web or native for the beta), business #6 (where people pay). The voice lens's platform facts are the evidence.

**This is a real conflict.** The UI/UX lens wants a native app for the beta because lock-screen play, background audio, hands-free calls and a reliable drop are the commute use case. The rethink and business lenses want an installable web app plus a private podcast feed and web checkout.

| Option | Consequence |
|---|---|
| **Recommended: Milestone 0 with no app (WhatsApp, a private podcast feed, a call link). Beta as an installable web app plus the private feed and web checkout; calls run screen-on with earphones; a dial-in phone number is tested as an experiment. Native app after the beta gates pass.** | The feed already gives lock-screen and car play, background audio and new-episode alerts, which covers the listening that is 60 to 70% of the time; one person ships web weeks faster; web keeps about 96% of revenue against 85%. The cost: no pocketed call in the beta. |
| Native app (one codebase) from the beta | The best commute experience, including hands-free calls; a longer build, App Store review and a 15% fee. |
| Web only, no feed (current PRD) | On an iPhone, no lock-screen listening and the call stops when the screen locks; the weakest commute case. |

**Why I picked it:** the beta's job is to test whether the show is wanted and the teacher felt. The feed carries the part of the experience web does worst. **Switch to native early** if the beta shows many calls abandoned on the commute or the feed-to-call handoff losing most learners.

## 8. Set how personal an episode gets

**Absorbs 2 questions:** personalization #3 (how personal by default) and #4 (can "made once" share ingredients).

| Option | Consequence |
|---|---|
| **Recommended: interests lead each episode; at most 1 or 2 life facts as seasoning, only things the learner told the show, quote-backed and confirmed; sensitive topics only when the learner raises them; real-life arcs when the learner brings an event. Shared ingredients (news digests per interest, word glosses, host personas) are made once for everyone, while every episode stays unique.** | Interests drive return; life details carry most of the creepiness and false-memory risk for little learning; shared ingredients cut cost with no difference the learner can see. |
| Episodes built around the learner's life | The strongest "it knows me", and the highest risk of wrong memories and distraction from the language. |
| Every ingredient generated per learner | A purer reading of "made once", at higher cost, with nothing the learner can tell apart. |

**Evidence:** AI stories built from each learner's own input raised motivation but not vocabulary learning in a 272-person randomized study (Leong 2024); people accept personalization from what they told you and recoil from what was inferred (Aguirre 2015; Kim 2019).
**Why it matters early:** it decides what the product collects about people, which is the hardest thing to walk back.

## 9. Decide what the product may do with voice and transcripts

**Absorbs 3 questions:** voice #3 (analyse audio when storage is declined), voice #4 (the learner's cloned voice), architecture #2 (anonymized transcripts to improve the teacher).

| Sub-decision | Recommended | Alternative and its consequence |
|---|---|---|
| a. Learner declines voice storage | Still analyse the call audio for a few minutes after the call, then delete it; said in one plain sentence at consent. | Analyse only the live transcript: it drops fillers and can silently fix grammar, so the error profile is unreliable. |
| b. Improving the teacher | Opt-in, off by default, anonymized transcripts used to check and improve it. | No opt-in: quality checks rely on synthetic learners and paid annotators, and the analyst improves slower. |
| c. The learner's own cloned voice ("hear yourself say it fluently") | Not in the beta; test later as opt-in. | Offer at launch: early evidence it helps (Ding 2019), but the most intimate use of their data the product could make. |

**Also flagged by lenses, for legal review before the paid beta:** data protection law wherever learners come from (GDPR in Europe, Saudi Arabia's Personal Data Protection Law, and others) for voice recordings and cross-border storage; California SB 243 if a recurring AI host counts as a companion chatbot (AI disclosure, a self-harm protocol). These are flags, not legal advice.

## 10. Decide how the beta earns and proves itself

**Absorbs 3 questions:** business #4 (charge from the beta), #5 (free tier), assessment #4 (external test).

| Sub-decision | Recommended | Alternative and its consequence |
|---|---|---|
| a. Charge from day one | Yes: after the 7-day trial, founding members (the first 100) pay the monthly plan price and keep it for as long as they stay subscribed. | Free beta: it tells you whether people like it, not whether it is a business. |
| b. Free tier | None. A free 90-second sample episode before signup, then a 7-day trial. | Freemium: about 2.1% of downloads convert against 10.7% for hard paywalls, with similar one-year retention. |
| c. External test | 20 to 30 beta learners take a recognized test at week 0 and week 8 (about $50 to $250 a sitting, an estimate). | Trust internal measures only: no proof the internal scale measures real proficiency before telling thousands they improved. |

---

## Settled: every lens agrees, so these stand unless Muath objects

| Question it closes | What stands | From |
|---|---|---|
| What counts as "learned"? | Correct, unprompted, at least a day later, in a different session; "stable" only when it holds in the next 4-weekly recording. | Learning science B, assessment |
| When fun and learning clash? | The fun must carry the language: every joke, twist and personal reference carries a target or due word, and the quality gate checks it. | Learning science C, personalization, enjoyment |
| Transcript always on? | Audio-first: on the first play the transcript is folded for intermediate learners; a "Huh?" button replays the last sentence slower and shows it; the planner fades or adds support per learner. | Language acquisition C, learning science, UI/UX |
| Pronunciation in v1? | Light: tap to hear any word, shadow two lines, "say it once" after the hosts. The engine may score that known sentence internally; the learner never sees a number. | Language acquisition D, voice, UI/UX |
| The first ten minutes? | A voice in under 60 seconds, a 3-minute talk with the hosts, a short pilot episode, a 60 to 90 second first call, the account after that. | UI/UX #3, personalization cold start |
| What counts as success? | Add "worth it", unprompted return, change in the 4-weekly recording and delayed recall to the beta metrics; minutes per day are a warning light, not a goal. | Enjoyment #3, consistency, assessment |

## Index: all 48 questions and where each went

| Thread | Question | Goes to |
|---|---|---|
| First rethink | 1 First learner | Decision 1 |
| First rethink | 2 Launch language | Decision 1 |
| First rethink | 3 Correction law | Decision 3 |
| First rethink | 4 Progress law | Decision 4 |
| First rethink | 5 Notification law | Decision 6 |
| First rethink | 6 Price band | Decision 2 |
| Learning science | A Recall | Decision 4 |
| Learning science | B What counts as learned | Settled |
| Learning science | C Fun versus learning | Settled |
| Language acquisition | A Session as the dose or the hub | Decision 2 |
| Language acquisition | B Clarification requests | Decision 3 |
| Language acquisition | C Audio-first listening | Settled |
| Language acquisition | D Pronunciation | Settled |
| Consistency and motivation | 1 Weekly rhythm | Decision 6 |
| Consistency and motivation | 2 Note after a gap | Decision 6 |
| Consistency and motivation | 3 Seasons | Decision 5 |
| Consistency and motivation | 4 Story threads | Decision 5 |
| Enjoyment and pull | 1 Story arcs | Decision 5 |
| Enjoyment and pull | 2 Choose tomorrow tonight | Decision 6 |
| Enjoyment and pull | 3 Success measures | Settled |
| Personalization | 1 Show the language model | Decision 4 |
| Personalization | 2 60-second word check | Decision 4 |
| Personalization | 3 How personal by default | Decision 8 |
| Personalization | 4 Shared ingredients | Decision 8 |
| Personalization | 5 Light continuity | Decision 5 |
| AI architecture | 1 Cost per session | Decision 2 |
| AI architecture | 2 Anonymized transcripts | Decision 9 |
| AI architecture | 3 Launch pair | Decision 1 |
| Voice and speech | 1 First target language | Decision 1 |
| Voice and speech | 2 Voice budget | Decision 2 |
| Voice and speech | 3 Analyse audio when storage declined | Decision 9 |
| Voice and speech | 4 Cloned learner voice | Decision 9 |
| UI and UX | 1 Producer as on-screen teacher | Decision 3 |
| UI and UX | 2 Web or native for the beta | Decision 7 |
| UI and UX | 3 The first ten minutes | Settled |
| Market and competitors | 1 Launch market | Decision 1 |
| Market and competitors | 2 What you sell | Decision 2 |
| Market and competitors | 3 One pair or all languages | Decision 1 |
| Assessment and progress | 1 Where do I stand | Decision 4 |
| Assessment and progress | 2 4-weekly speaking sample | Decision 4 |
| Assessment and progress | 3 Visible "working on" list | Decision 4 |
| Assessment and progress | 4 External test | Decision 10 |
| Business and launch | 1 Launch wedge | Decision 1 |
| Business and launch | 2 Price position | Decision 2 |
| Business and launch | 3 Daily allowance | Decision 2 |
| Business and launch | 4 Charge from the beta | Decision 10 |
| Business and launch | 5 Free tier | Decision 10 |
| Business and launch | 6 Where people pay | Decision 7 |
