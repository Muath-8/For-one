# Knowing the learner: assessment, error analysis and progress

*For one, one of 11 perspectives · lens: how the AI teacher measures the learner, decides what comes next, and lets them feel real improvement. Written 2026-10-09. Builds on the first rethink ("For one: the next evolution, a rethink") and does not repeat it. Published doc (with a pipeline diagram): https://claude.ai/code/artifact/62a5d6d5-b169-4cac-8aca-3861a0133305*

---

## Decisions only you can make

My recommendation is first in each row. The rest of this document assumes it until you say otherwise.

| # | Decision | Recommended | Alternative | Why it matters |
|---|---|---|---|---|
| 1 | Can a learner ever learn "where they stand"? | Never pushed, always answered honestly when asked: a per-skill estimate with a range ("your listening is around B1, your speaking is just below it, here is what that means") | Never surfaced in any form (the current PRD law) | People with real goals (a job that needs B2, a visa, an exam) will leave to find out elsewhere. Refusing to answer also breaks your own "never hide" promise. |
| 2 | Is there one recurring, like-for-like speaking sample? | Yes, every 4 weeks, openly framed as "recording your then-and-now" (about 3 minutes, same task types each time) | Measure only from everyday sessions | Without the same task repeated, no honest "you improved" claim about speaking is possible: topic and task move the numbers more than a month of growth does. This bends the "no tests" law, so it is your call. |
| 3 | Can the learner see and change what the teacher is working on? | Yes: a short "working on" list (at most 3 items), which the learner can veto or add to ("I don't care about articles, I care about sounding professional") | Targets stay invisible (current PRD) | Choice is a core motivation need, and the learner knows things the data can't (which mistakes embarrass them at work). It also makes the Weekly Proof believable. |
| 4 | Pay for an external test for a beta cohort? | Yes: 20 to 30 beta learners take a recognized test at week 0 and week 8 | Trust internal measures only | It is the only way to prove the internal model measures real proficiency before you tell thousands of people they improved. Expect roughly $50 to $250 per test sitting, depending on the test (my estimate, not quoted prices). |

If you answer only one, answer #2. Everything in "felt progress" below depends on it.

---

## The short version

1. **The learner model is the product's real asset, and today it is under-specified.** The PRD's assessment engine (Part 10) has the right instincts (no tests in the live path, an error-versus-slip rule, avoidance detection, a target lifecycle, an honest flat-week rule), but it treats noisy signals as facts. It has no uncertainty, no like-for-like comparison, and no protection against the speech recognizer and the LLM rater being wrong.
2. **Two kinds of measurement, two standards.** Planning signals can be fast and noisy, because a wrong guess costs one slightly mistargeted episode. Claims made to the learner ("you no longer say *I go yesterday*") must be slow, conservative and checked, because one false claim destroys trust in every later one. The design separates them with a "claim gate".
3. **Speech-to-text quietly hides the errors you most want to find.** Off-the-shelf recognizers smooth over learner grammar and drop hesitations; on learner speech, over half of Whisper's mistakes come from exactly those features. Error analysis must run on a verbatim, timestamped, confidence-scored transcript, and grammar claims should lean on the written chat, where the evidence is clean.
4. **Plan from a fine inventory, report in broad categories.** Twelve error categories are fine for the Weekly Proof but too coarse to decide tomorrow's episode. The planner needs a list of several hundred concrete structures and the learner's state on each, plus a probability per word.
5. **Choose what to inject by need, readiness, goal and opportunity, not frequency alone.** The most frequent error is often not the most important one, and a learner who is not yet attempting a structure will not pick it up from correction.
6. **Felt progress comes from evidence about the task, compared with your past self, never with other people or a score.** The research on feedback is blunt: over a third of feedback interventions make performance worse, mostly when the feedback is about the person rather than the work. Show the learner their own sentences, their own voice and their own real-world wins, and admit flat weeks.

---

## Where the current design stands

**Keep, because it is right:**

- All analysis after the session, never in the live call.
- The rule that a pattern needs at least 3 observations across at least 2 sessions before it becomes a target.
- Avoidance detection (structures expected at this stage that the learner never attempts).
- The target lifecycle with spaced re-checks at 2, 4 and 8 weeks.
- Accuracy, complexity and fluency as separate dimensions.
- The flat-week rule and the ban on fabricated wins.

**Fix, because it will mislead the teacher or the learner:**

| Gap in the PRD | What goes wrong | Fix |
|---|---|---|
| Every estimate is a single number with no uncertainty | The planner overreacts to one bad call; the Proof claims changes that are noise | Every estimate carries a range; claims need the change to exceed that range |
| Weekly accuracy, complexity and fluency are computed on whatever the learner talked about that week | A hard topic looks like a bad week; a familiar topic looks like progress | Compare only like-for-like tasks: retell turns week to week, the 4-weekly sample month to month |
| Accuracy is read on its own | When learners try harder structures, error rates go up. A "flat" or "worse" week is often a growth week | Always read accuracy next to what was attempted |
| Speaking transcripts are treated as truth | Recognizers "fix" learner grammar and drop fillers, so errors are undercounted and fluency is overstated | Verbatim transcription with word timings and confidence; low-confidence regions never produce claims |
| LLM raters produce the error tags | LLMs over-correct and rewrite style, and their category labels drift | LLM proposes the smallest possible correction; code classifies the edit; humans calibrate per language |
| 12 fixed categories drive targeting | "Verb tense" lumps the irregular past with the present perfect; the planner can't target either well | Plan on a fine structure inventory; roll up to the 12 categories only for reporting |
| Vocabulary rings come from tap logs | A tap means "not sure", not "unknown"; no tap does not mean "known" | A probability per word, updated from several kinds of evidence |
| One difficulty "edge" for everything | Many intermediates understand far more than they can say; one edge either bores their ears or overloads their mouth | Separate estimates for listening, reading, speaking and writing |
| Success metric "50% of targets retired in 3 weeks" | The planner can hit it by choosing easy targets | Count a target as learned only when it holds in the 4-weekly sample |

---

## What the evidence says

"Strong" means replicated or meta-analytic; "moderate" means a few good studies or one meta-analysis with caveats; "my judgment" is mine.

| Finding | Strength | What it means for For one |
|---|---|---|
| CEFR bands are broad. Cambridge estimates about 200 guided learning hours to move one level, and finer scales (Pearson's GSE, 10 to 90; Duolingo Score, out of 160) exist because a learner can grow a lot inside one band without it showing | Strong (as a description of practice) | CEFR is the right anchor to talk to the outside world, and the wrong ruler for week-to-week progress. The internal model needs finer grain. |
| Corpus-based profiles list which grammar and words learners actually use at each level (English Grammar Profile, English Vocabulary Profile) | Moderate (English only; other languages have thinner equivalents) | A ready-made structure inventory for English. Other languages need one built, which is a per-language content cost. |
| Speech rate (r = .76) and mean length of run (r = .72) track how fluent listeners judge you to be; pauses inside clauses matter more than pauses between them (r = -.72 vs -.48); counting repairs and restarts tells you little (r = -.20) (Suzuki, Kormos & Uchihara 2021) | Strong | Fluency can be measured automatically from word timings, cheaply and meaningfully. Track speech rate, run length and mid-clause pauses. Ignore filler counts. |
| Complexity, accuracy and fluency trade off: under pressure, learners gain on one and lose on another (Skehan 2009). Each is multidimensional and sensitive to the task (Norris & Ortega 2009) | Strong | Never judge a week on accuracy alone, and never compare different task types. |
| Repeating sentences back (elicited imitation) correlates with general proficiency at r = .66 across 60 samples (Kostromitina & Plonsky 2022) | Moderate | A 1-minute "say it back" set inside the 4-weekly sample is a cheap, stable anchor. |
| Learners' self-assessment correlates with measured ability at about r = .45 overall and .44 for speaking; concrete, real-life can-do statements do better (about .49) (Li & Zhang 2021, as reported in Winke et al. 2023) | Strong | Asking "can you do X?" is a useful signal and a motivating moment, never the measurement itself. The gap between felt and measured ability is worth showing the learner when they underrate themselves. |
| With calibration examples, GPT-4 rates short learner essays on CEFR almost as well as dedicated scoring systems, but agreement varies with the writer's first language (Yancey et al. 2023) | Moderate | LLM rating is viable if calibrated per language pair and checked against humans. Never trust it uncalibrated. |
| LLMs used as grammar correctors rewrite too much: high fluency, many unnecessary edits, weak on tense and agreement across sentences (Fang et al. 2023) | Moderate | Ask the model for minimal edits only, then classify the edits with rules (the ERRANT approach, Bryant et al. 2017). |
| Whisper's word error rate on learners' spontaneous English is about 18 to 19%; over half of its mistakes come from fillers, self-repairs and ungrammatical expressions; fine-tuning on learner speech nearly halves the error rate (Kim et al. 2024) | Moderate | The recognizer is the first source of measurement error. Budget for learner-speech tuning and keep confidence scores. |
| Feedback improves performance on average, but over a third of feedback interventions made performance worse, mostly when feedback pulled attention to the self instead of the task (Kluger & DeNisi 1996). Praise of the person is the least effective feedback (Hattie & Timperley 2007) | Strong | All progress messages are about the task and the learner's own work ("you used *would have* three times"), never about the person ("you're doing great"). |
| Task comments raised interest more than normative grades, and adding grades to comments cancelled the benefit; the effect was concentrated in low achievers (Butler 1988) | Moderate (one well-known study with nuances) | No scores next to feedback. The learners most likely to quit are the ones a score hurts most. |
| Anxiety correlates with lower achievement, r = -.36 across 105 samples (Teimouri, Goetze & Plonsky 2019) | Strong | Assessment that feels like a test has a learning cost, not only a churn cost. The 4-weekly sample must feel like recording, not examination. |
| Learners benefit from feedback on structures they are developmentally ready for (Mackey & Philp 1998; Pienemann's Processability Theory) | Moderate | Target what the learner is already attempting imperfectly; give never-attempted structures input first. The PRD already says this; keep it. |
| A trainable per-item memory model (half-life regression) cut recall-prediction error by more than 45% and raised daily engagement 12% at Duolingo (Settles & Meeder 2016) | Strong (industrial) | Words and structures need a per-learner memory model; it pays for itself in both learning and return visits. |
| Comparing yourself with your own past ("ipsative" assessment) supports motivation better than comparing with others, especially for weaker learners (Hughes 2011) | Moderate | The only comparison For one ever shows is you then versus you now. |

---

## The design

### 1. The learner model: what the teacher keeps track of

One structured record per learner. Every number in it carries a range, and every entry links back to the moments that produced it, so any claim can be traced to a clip or a sentence.

| Part | What it holds | Updated from |
|---|---|---|
| **Skill estimates** | Listening, reading, speaking and writing, each on a fine internal scale anchored to CEFR (think GSE-like grain), with a range | Every session, slowly; re-anchored by the 4-weekly sample |
| **Word knowledge** | For each word: probability it is understood when heard, when read, and used correctly; plus a memory strength that decays | Taps, replays near the word, comprehension in the call, unprompted use, spaced re-exposure |
| **Structure inventory** | For each of several hundred concrete structures (for English, seeded from the English Grammar Profile): not seen / heard often / attempting / mostly right / stable, plus an avoidance flag | Error analysis of calls and chats, using "obligatory context" scoring: did the learner use the form where it was needed? |
| **Fluency profile** | Speech rate, mean length of run, mid-clause pause rate, articulation rate, all per task type | Retell turns and the 4-weekly sample only |
| **Complexity profile** | Clause length, subordination, lexical diversity (MTLD, not type-token ratio), share of words beyond the most frequent 2,000 | Same comparable segments |
| **Comprehension** | How well the call reflected the episode and the article; answers to the host's embedded questions | Each session |
| **Self-view** | Monthly can-do answers tied to their own goal | Monthly, optional, one minute |

Two design rules make this work:

- **Probability, not rings.** A word starts with a prior from its frequency and the learner's estimated vocabulary size (a learner who knows about 3,000 word families probably knows most of the top 2,000 and few beyond 5,000). Evidence then moves it. A tap is strong evidence of "not sure" for that word in that moment. Hearing it many times without tapping, then arguing correctly about the passage, is weak evidence of knowing it. Using it unprompted and correctly is strong evidence of productive knowledge. This replaces the PRD's confident/emerging/unseen rings with something the coverage check (from the first rethink) can compute against.
- **Fine inventory for planning, twelve categories for reporting.** The PRD's 12 categories become a reporting layer over the inventory. "Past tense: irregular verbs in narratives" is targetable; "verb tense/aspect" is not.

### 2. How the teacher measures: four clocks

Nothing here is a test in the live path. Each clock uses the instrument that is reliable at that time scale.

| Clock | What runs | What it is allowed to influence |
|---|---|---|
| **During the call** | Nothing is graded. The host has a short brief (today's 1 to 2 targets, words due for review) and recasts or nudges per the revised correction law | The conversation only |
| **After each session** (within the PRD's 10-minute window) | Verbatim transcript with word timings → minimal-edit corrections proposed by an LLM → edits classified by rules into the inventory → low-confidence regions dropped → word and structure evidence updated | Tomorrow's plan. Never a claim to the learner |
| **Weekly** | Fluency and complexity on retell turns only (the 60 to 90 second "tell Karim what happened" the first rethink added), smoothed over 2 weeks | Difficulty settings; the Weekly Proof only through the claim gate |
| **Every 4 weeks** | The anchor sample (about 3 minutes): a retell of a matched-difficulty story, a 2-minute opinion on a familiar topic, and 8 to 10 sentences to repeat back. Same task types every time, rated by calibrated LLM plus code metrics | Then-and-now claims about speaking; re-anchoring the skill estimates; the team's outcome metrics |

The anchor sample is the one place the product asks for a performance on purpose. Done right, it is the most loved moment in the month, because it produces the clip the learner will play to their friends. The framing matters: it is "recording your then-and-now", the host explains why it is always the same kind of task, nothing is scored on screen, and the learner can skip it (and is told that skipping means no voice comparison that month).

### 3. The honesty layer: when the system may claim something

Your trust contract says "prove progress honestly". This is how that becomes code. Every sentence the Weekly Proof or a host says about the learner's progress must pass a **claim gate**:

1. **Like for like.** The comparison is between the same task type (two anchor samples, or two retell turns on similar difficulty).
2. **Beyond the noise.** The change must exceed what the measure normally wobbles by. Practically: the difference must be larger than about twice the measurement's standard error, which the team estimates per metric from learners who did two samples a few days apart. My judgment on a starting rule; the statistics are the standard "reliable change" idea.
3. **Repeated.** At least two data points point the same way, except for first-ever events ("first time you used the conditional").
4. **Clean evidence.** Grammar claims come from text chat or from speech regions the recognizer was confident about.
5. **Traceable.** Every claim carries its evidence (the two clips, the sentence then and now) and the learner can open it.

When a claim fails the gate, the system says the honest thing instead: "Too early to tell", or "Flat week, and here is the one thing we're changing". When a metric goes the wrong way and the learner was attempting harder language, the system says so ("more mistakes this week, because you tried the past perfect eleven times; in June you never tried it"). That sentence is both true and motivating, which is the whole point of reading accuracy next to complexity.

**Calibration before claims.** Per language pair, before beta:

- 150 to 200 learner samples (calls and chats) double-tagged by trained teachers.
- LLM-plus-rules pipeline compared against them. My suggested bar, a judgment: agreement on CEFR-level rating at a quadratic weighted kappa of about 0.7 or better, and precision of at least 0.8 on the error tags that feed claims (recall matters less: a missed error costs a little planning, a false error costs trust).
- The rating model version is pinned for each 4-week window, so a model upgrade never shows up as learner progress. Re-run the calibration set on every model change.

### 4. From mistakes to the next episode: deciding what to inject

The PRD selects targets by frequency × recency × readiness. That is a good start but misses why some mistakes matter more. The planner should score each candidate (a structure or a word) on six things:

| Factor | Question | Example |
|---|---|---|
| **Need** | How often does it go wrong, and how much does it hurt understanding? | Errors that change meaning (wrong tense in a story, missing negation) outrank errors listeners barely notice (a dropped article) |
| **Goal fit** | Does the learner's real situation demand it? | Job interviews need past narratives, hedging and polite disagreement; a trip needs questions and requests |
| **Readiness** | Is the learner already attempting it, or using the step just before it? | Attempting the present perfect with errors → ready. Never attempted → input first |
| **Learnability** | Is it a clear rule (explain once, then practice) or item by item (needs lots of input)? | Third-person -s is a rule; which preposition goes with which verb is item by item |
| **Opportunity** | Can tomorrow's episode make it natural and necessary? | A "what would you have done" argument makes the third conditional necessary, not optional |
| **Due** | Is something learned earlier about to be forgotten? | The memory model says yesterday's 3 new words need a return today |

Then two caps: one grammar target and two to four words per session, and no target more than four sessions in a row (fatigue is real and the learner starts to notice the pattern).

Each target type gets a matching treatment, because the research says different problems respond to different feedback:

| Learner state | Treatment |
|---|---|
| Never attempted but expected at their stage | Hosts use it often and audibly in the episode (input flood), no correction |
| Attempting, rule-based, with errors | Clear recast in the call, one natural nudge, then the optional polish card after the chat |
| Attempting, item-based (word choice, collocation) | Recast, then the word returns in later episodes and articles on a spaced schedule |
| Avoided (expected, never used, and the learner chooses paraphrases) | Host models it, then a call-in question that is hard to answer without it |
| Slow or broken speech on easy content (a fluency problem, not a knowledge problem) | Retell the same story twice, faster the second time (the 4/3/2 idea) |
| Mistake the learner says they don't care about | Drop it from targeting unless it breaks meaning |

**Lifecycle, tightened.** "Taking" requires correct use where the form was needed, unprompted, in at least two sessions. "Stable" requires about 80% correct use in obligatory contexts over two weeks or more, and it is confirmed only when it holds in the next anchor sample. Re-checks stay at 2, 4 and 8 weeks.

**Learning what works for this learner.** Keep 10 to 15% of target slots for trying a different treatment (more explicit, more input, a different format) and record which one moved the learner. Over months, this is the personal teacher learning how *you* learn. My judgment; the method is a standard explore-exploit approach.

### 5. Making improvement felt without points or levels

What the research says to do: feedback about the task and the process, comparison with your own past, information rather than control, concrete and checkable, and honest about flat stretches. What it says to avoid: scores beside feedback, comparison with others, praise of the person.

Seven surfaces, all evidence, none a game:

1. **Then and now.** Two anchor clips side by side, with at most two measured differences in plain words: "This time you spoke for 40 seconds before your first long pause. In June it was 12." "You used *would have* three times. In June, never."
2. **Things you can do now.** Moments the Analyst found in real sessions that match a can-do description, phrased as an accomplishment with the clip attached: "You disagreed with Karim, gave a reason, and conceded half his point. That's a skill people work on for years."
3. **Words you own.** Words that went from never used to used unprompted, each shown in the learner's own sentence.
4. **Mistakes that went away.** Only after the claim gate and the next anchor sample confirm it, with the last date it appeared.
5. **Hours.** Hours heard and minutes spoken, as plain information (the Dreaming Spanish model), never as a goal or a streak.
6. **Out in the world.** A log of real uses the learner reports ("ordered at the café in Spanish"). The show celebrates these above everything else, in keeping with "the show is the gym, life is the game".
7. **Where do I stand?** Only when asked (decision #1): a per-skill estimate with a range, what that means in real situations, and what the next step looks like.

Never: points, XP, levels on screen, percentages ("accuracy 78%"), percentiles, leaderboards, red marks, per-turn praise, streak counters.

**The intermediate plateau.** Your first learner is the stuck intermediate, and their main feeling is "I'm not improving". Part of that is arithmetic: each CEFR level takes about 200 more guided hours, and the gains get harder to see. The answer is not a fake number; it is finer evidence. A learner who cannot see a level change in three months can see twelve new words they now use, two structures they now attempt, and a run length that grew from 12 to 40 seconds. Fine-grained, real, and theirs.

**When the news is bad.** If an anchor sample is worse, the show says so, gives the most likely reason it can support with evidence (harder story, a tired evening, a long gap), and names the one change it is making. It never invents a win to compensate.

### 6. The Weekly Proof, rebuilt on this

- Built only from claims that passed the gate. If nothing passed, it is a flat-week Proof (already in the PRD), which is fine.
- One headline piece of evidence, not three. The other two go in a "more" section the learner can open.
- Every claim can be expanded to "how we know": the two clips or sentences behind it.
- The anchor-sample week gets the special edition: the then-and-now clip.
- The "working on" list (decision #3) appears at the end, with one tap to change it.

### 7. The machinery

This maps onto the first rethink's roles; it mostly specifies the Analyst and adds two pieces of code.

1. **Transcriber.** Speech-to-text set up for learners: verbatim mode keeping fillers and restarts, word-level timestamps and confidence. Fine-tune on learner speech per launch language once you have consented data.
2. **Analyst (LLM, fixed schema).** For each learner turn: the smallest correction that makes it acceptable, nothing stylistic. Comprehension and content-uptake ratings. Can-do moment detection.
3. **Edit classifier (code).** Aligns original and corrected text and classifies each edit into the structure inventory and the 12 reporting categories (ERRANT-style for English; per-language rules elsewhere). Drops edits in low-confidence speech regions.
4. **Measures (code).** Fluency from timestamps, complexity from parses, lexical diversity, obligatory-context scores per structure.
5. **Learner model updater (code).** Bayesian updates of skills, words and structures with ranges; memory model per word and structure.
6. **Claim gate (code).** The five rules in section 3. The only route from the learner model to anything the learner hears or reads about their progress.
7. **Showrunner** (planner) reads the learner model and applies the targeting policy in section 4.

LLMs judge only what needs judgment (what the learner meant, what the minimal fix is, whether a moment shows a skill). Code does everything that must be consistent.

---

## How the team will know it works

| Metric | Why |
|---|---|
| Change in the anchor sample at 4, 8 and 12 weeks (fluency, complexity, accuracy in obligatory contexts) | The real learning outcome; replaces engagement-only success metrics |
| Agreement with the external test for the beta cohort (decision #4) | Proves the internal scale measures real proficiency |
| False-claim rate: a monthly human audit of a sample of Proof claims, target under 5% (judgment) | The trust contract, measured |
| Targets that hold in the next anchor sample | Replaces "50% retired in 3 weeks", which the planner could game |
| "I can tell I'm improving" (a one-question monthly check, 1 to 5) | Felt progress, measured directly |
| Recognizer word error rate on learner speech, per language | The first link in the chain |

---

## Build order

**Milestone 0 (hand-made, 10 to 15 people, 14 days).** A teacher tags every call and chat by hand, using the planned structure inventory. Record the anchor sample on day 1 and day 14. Run the automated pipeline in the background and compare it with the teacher's tags. This gives the first calibration set for free, and tells you whether learners believe the hand-written Proof.

**Private beta.** Verbatim transcription with timings, the Analyst plus edit classifier, the word probability model, the inventory for one language, the anchor sample, and the claim gate. Simple targeting rules (section 4) without the exploration slots. External test for 20 to 30 people.

**After beta.** Exploration slots (learning which treatment works per learner), recognizer fine-tuning on consented learner speech, "where do I stand" answers, and inventories for the next language.

---

## Risks and open questions

- **The anchor sample becomes a chore.** If learners skip it, speaking claims stop. Test the framing in Milestone 0; it must feel like recording a memory, not sitting an exam.
- **Per-language cost.** English has published learner profiles; most languages do not. Each new language needs an inventory, error rules and a calibration set double-tagged by teachers. This is real money and should be in the language-launch plan.
- **Voice consent.** Learners who decline voice storage get text-only then-and-now. The anchor sample still works from transcripts, but it loses its most motivating form. Worth telling them that at the consent moment, honestly.
- **Recognizer bias by accent and first language.** Error rates differ by speaker group; the claim gate protects claims, but planning may be worse for some groups. Track recognizer error by first language from day one.
- **Measurement as surveillance.** A learner who discovers how much is tracked may feel watched. The answer is the trust contract: the learner can see their learner model in plain language (which the PRD currently excludes for the language profile), and everything shown is about their work, never a judgment of them.

---

## Sources

**Scales and inventories**
- Council of Europe (2020). *CEFR Companion Volume*. https://www.coe.int/en/web/common-european-framework-reference-languages
- Cambridge English. Guided learning hours. https://support.cambridgeenglish.org/hc/en-gb/articles/202838506-Guided-learning-hours
- Pearson. Global Scale of English: granular insight into learner progress. https://languagescanada.ca/web/default/files/users/jtannous@languagescanada.ca/Granular%20Insight%20into%20Learner%20Assessment%2C%20Progress%20and%20Performance_Pearson.pdf
- Duolingo (2024). The Duolingo Score. https://blog.duolingo.com/duolingo-score/
- O'Keeffe, A. & Mark, G. (2017). The English Grammar Profile of learner competence. *International Journal of Corpus Linguistics*. https://dspace.mic.ul.ie/items/ef5b4f7e-3b35-4db7-a5bf-9578bc618905/full

**Measuring speech and writing**
- Suzuki, S., Kormos, J. & Uchihara, T. (2021). The relationship between utterance and perceived fluency: a meta-analysis. *Modern Language Journal*. Figures as reported in Takizawa & Suzuki (2025), https://www.cambridge.org/core/product/FAB18835B2117A299C33F8F502248C81
- Skehan, P. (2009). Modelling second language performance: integrating complexity, accuracy, fluency and lexis. *Applied Linguistics*.
- Norris, J. & Ortega, L. (2009). Towards an organic approach to investigating CAF in instructed SLA. *Applied Linguistics*.
- McCarthy, P. & Jarvis, S. (2010). MTLD, vocd-D and HD-D. *Behavior Research Methods*.
- Kostromitina, M. & Plonsky, L. (2022). Elicited imitation tasks as a measure of L2 proficiency: a meta-analysis. *Studies in Second Language Acquisition*. https://experts.nau.edu/en/publications/elicited-imitation-tasks-as-a-measure-of-l2-proficiency/
- Winke, P., Zhang, X. & Pierce, S. (2023). Self-assessment as a measure of speaking proficiency (reports Li & Zhang 2021 and Ross 1998). *Studies in Second Language Acquisition*. https://www.cambridge.org/core/product/786D4E0E0D500DCDD43CCE24ED610592/core-reader

**Automated analysis**
- Yancey, K. et al. (2023). Rating short L2 essays on the CEFR scale with GPT-4. BEA workshop. https://aclanthology.org/2023.bea-1.49
- Fang, T. et al. (2023). Is ChatGPT a highly fluent grammatical error correction system? https://arxiv.org/abs/2304.01746
- Bryant, C., Felice, M. & Briscoe, T. (2017). Automatic annotation and evaluation of error types for grammatical error correction (ERRANT). ACL.
- Kim, H. et al. (2024). LearnerVoice: a dataset of non-native English learners' spontaneous speech. Interspeech. https://arxiv.org/abs/2407.04280
- Graham, C. & Roll, N. (2024). Evaluating OpenAI's Whisper ASR across accents and speaker traits. https://www.repository.cam.ac.uk/items/b1b02204-7d9e-4f90-95f3-07619329bf35
- Settles, B. & Meeder, B. (2016). A trainable spaced repetition model for language learning. ACL. https://aclanthology.org/P16-1174

**Feedback, motivation and readiness**
- Kluger, A. & DeNisi, A. (1996). The effects of feedback interventions on performance. *Psychological Bulletin*. https://cris.huji.ac.il/en/publications/the-effects-of-feedback-interventions-on-performance-a-historical/
- Hattie, J. & Timperley, H. (2007). The power of feedback. *Review of Educational Research*.
- Butler, R. (1988). Enhancing and undermining intrinsic motivation: the effects of task-involving and ego-involving evaluation. *British Journal of Educational Psychology*. Discussion of nuances: https://edweek.org/education/opinion-grades-versus-comments-what-does-the-research-really-tell-us/2019/06
- Teimouri, Y., Goetze, J. & Plonsky, L. (2019). Second language anxiety and achievement: a meta-analysis. *Studies in Second Language Acquisition*. https://experts.nau.edu/en/publications/second-language-anxiety-and-achievement/
- Hughes, G. (2011). Towards a personal best: a case for introducing ipsative assessment in higher education. *Studies in Higher Education*.
- Mackey, A. & Philp, J. (1998). Conversational interaction and second language development: recasts, responses, and red herrings? *Modern Language Journal*.
- Pienemann, M. (1998). *Language Processing and Second Language Development: Processability Theory*.
