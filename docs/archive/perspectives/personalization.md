# For one: the personalization engine

Oct 9, 2026 · Personalization lens, one of eleven perspectives on For one. Live doc with diagrams: https://claude.ai/code/artifact/fae8f564-94b9-4f96-9b65-22fd1ab2c56a

## Decisions (settled)

Settled on Oct 23, 2026: Muath accepted the recommended option for all five decisions below. The rest of this doc is built on them.

| # | Decision | Recommended | Alternative | Why it matters |
| --- | --- | --- | --- | --- |
| 1 | Does the learner see the language side of what the show knows? | Yes, in plain words: words you now own, patterns you are working on, each with your own sentence as the example | Hidden, as the PRD says (life facts only) | A visible, editable model is what makes deep memory feel trusted instead of creepy, and it doubles as honest progress. |
| 2 | A 60-second "tap the words you know" check at signup? | Yes, framed as "help the show pitch at your level", with a few fake words mixed in to catch guessing | Only the PRD's 3 to 4 hidden probes | Without it the first week of episodes is pitched by guesswork, and week 1 is when people quit. It breaks the "no tests" law in letter, not in spirit. |
| 3 | How personal is an episode by default? | Interests lead; life facts are seasoning (at most 1 or 2 per episode, only things the learner told the show, sensitive topics only when the learner raises them) | Episodes built around the learner's life | Interests carry the motivation effect. Life details carry most of the creepiness and false-memory risk and can pull attention away from the language. |
| 4 | Can "made once" share ingredients? | Yes. Each episode is unique, but shared parts (news digests per interest, word explanations, host personas) are made once for everyone | Everything generated per learner | Same experience for the learner, much lower cost per session. Your principle is about the lesson, not the raw materials. |
| 5 | Can the show have light continuity between episodes? | Yes: running jokes, the hosts' own lives, an ongoing topic the learner cares about. Still no cliffhangers or obligations | The PRD law "only memory persists, never plot" | A recurring world is the most natural way to bring the same words back without feeling like review. |

Decision 3 matters most, because what the engine collects about people is the hardest thing to walk back.

## The short version

Personalization pays off in the opposite order from where intuition puts it. The biggest learning gains come from the invisible layer (which words this person knows, which errors they make, when each word should come back). Interests mainly bring people back. Life details add the most risk for the least learning.

The first rethink named three depths: about you, for you, by you. Through this lens they rank like this:

| Layer | What it is | What the evidence says it buys | Risk | Build priority |
| --- | --- | --- | --- | --- |
| For you | Level, word bank, errors, review timing | The large, replicated gains: adaptive tutoring and personalized review | Low; mostly code | First |
| By you | Choosing topics, shaping hosts, remixing pitches | Motivation and effort, reliably but modestly | Low | Second |
| About you: interests | Episodes about their team, job, hobbies | Interest and return visits; learning effects are mixed | Narrowing, shallow use | Second |
| About you: life | Their people, plans, week | Feeling known; a small memory boost when the learner actively relates words to themselves | Creepiness, false memories, distraction | Third, used sparingly |

Your "made once, used once" idea is right as a product signature, with one correction carried over from the first rethink: the text is used once, the language is not. The engine's real job is to write a new story every day while bringing the same words back on schedule.

The moat is not that content is personal; anyone can prompt a model with a name and a hobby. The moat is a learner model that is accurate at the word level, honest about what it remembers, and visibly improves the learner. That takes months of one person's data and cannot be copied in a quarter.

## What the evidence says

Adapting to what a learner knows produces large, replicated gains; adapting to what they like reliably raises interest but has mixed effects on learning. "Strong" below means replicated or meta-analytic; "moderate" means good single studies; "weak" means small, preprint or vendor-run. Everything in other sections not tied to a row here is my judgment.

**Adapting to level and memory**

| Finding | Strength | What it means for For one |
| --- | --- | --- |
| Intelligent tutoring systems: median effect 0.66 across 50 evaluations ([Kulik & Fletcher 2016](https://www.ida.org/research-and-publications/publications/all/e/ef/effectiveness-of-intelligent-tutoring-systems-a-meta-analytic-review)); g = 0.42 against teacher-led classes and no significant difference from human one-to-one tutors ([Ma et al. 2014](https://doi.org/10.1037/a0037123)) | Strong | The proven value of "personal" is adapting practice and feedback to the person. |
| Spanish vocabulary review timed per student beat generic spaced review by 10% (d = 0.88) and massed review by 16.5% on an exam 28 days later ([Lindsey et al. 2014](https://doi.org/10.1177/0956797613504302)) | Moderate (one rigorous field study) | Per-learner review timing is the single best-evidenced personalization for vocabulary. |
| Duolingo's per-word forgetting model cut recall-prediction error 45% versus Leitner boxes and raised daily activity 12% in a 3.3M-user test ([Settles & Meeder 2016](https://aclanthology.org/P16-1174)). The open FSRS model predicts recall better still on 727M Anki reviews ([srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark)) | Strong for prediction; engagement result is company-run | Use an off-the-shelf per-word memory model; do not invent one. |
| Well-tuned simple models (logistic regression, IRT, extended Bayesian knowledge tracing) match deep learning below about 1M interactions ([Khajah et al. 2016](https://arxiv.org/abs/1604.02416); [Gervet et al. 2020](https://doi.org/10.5281/zenodo.4143614)) | Strong | At For one's scale, interpretable models win. Deep models can come later. |
| Learners understand far more words than they can produce, and the gap widens for rarer words ([Webb 2008](https://doi.org/10.1017/S0272263108080042)) | Strong | Track understanding and production separately. |
| A 60-item yes/no word test with fake words takes about 3.5 minutes and predicts proficiency better than self-ratings ([LexTALE](https://doi.org/10.3758/s13428-011-0146-0)); the Duolingo English Test uses such items in a 25-item adaptive test that correlates above 0.7 with TOEFL and IELTS ([Settles et al. 2020](https://aclanthology.org/2020.tacl-1.17)) | Strong | A one-minute word check at signup is a sound shortcut (decision 2). |
| Assessing from natural behavior instead of tests correlates only 0.2 to 0.5 with external tests, in small studies from one group, none in language learning ([Shute et al. 2013](https://doi.org/10.1080/00220671.2013.832970)) | Weak | Hidden assessment needs a periodic fixed check to stay honest. |

**Adapting to interests and the self**

| Finding | Strength | What it means for For one |
| --- | --- | --- |
| Interest-based personalization: interest g = 0.55, retention g = 0.48, transfer g = 0.36 across 34 publications, with larger effects in weaker quasi-experiments ([Lin et al. 2024](https://doi.org/10.1007/s10648-024-09933-7)) | Strong for interest; moderate for learning | Real, but smaller than it looks once study quality is counted. |
| The closest test of your idea: AI-generated stories built from each learner's own input raised motivation but produced no difference in vocabulary learning (272 people, randomized) ([Leong et al. 2024](https://www.media.mit.edu/publications/putting-things-into-context)) | Moderate | Personal content alone will not teach more words. The word schedule has to do that. |
| Personalized AI podcasts helped in one subject, not another, and listeners liked the podcast format whether or not it was personal ([Do et al. 2024](https://arxiv.org/html/2409.04645v1)) | Weak (preprint) | The show format itself carries much of the appeal. |
| Personalization helps mostly learners with low prior interest, by triggering situational interest ([Reber et al. 2018](https://doi.org/10.1177/0963721418793140); [Bernacki & Walkington 2018](https://doi.org/10.1037/edu0000250)) | Moderate | Biggest payoff in the first weeks, for people who are not already passionate about the language. |
| Choice raises intrinsic motivation (d about 0.3) and works best with 2 to 4 options ([Patall et al. 2008](https://doi.org/10.1037/0033-2909.134.2.270)) | Strong | Keep pitches to 3 to 4 options, as the PRD does. |
| Relating a new word to yourself improves foreign-language word memory a week later ([Pruss et al. 2025](https://doi.org/10.3758/s13423-025-02674-w); [Qahl & Lambert 2025](https://doi.org/10.1002/tesq.3402)) | Moderate (lab) | The learner must do the relating ("tell Karim about your own boss"). Hearing your name in a script is not the same thing. |
| Interesting but irrelevant details reduce learning, g about -0.33 ([Sundararajan & Adesope 2020](https://doi.org/10.1007/s10648-020-09522-4); [Harp & Mayer 1998](https://doi.org/10.1037/0022-0663.90.3.414)) | Strong | Personal details must carry the target language, not decorate around it. |
| Matching teaching to a "learning style" has virtually no support ([Pashler et al. 2008](https://doi.org/10.1111/j.1539-6053.2009.01038.x)) | Strong | Format taste is for enjoyment only. |

**Generating at a level, and remembering**

| Finding | Strength | What it means for For one |
| --- | --- | --- |
| Comprehension needs about 98% known words for reading and about 95% for listening ([Laufer & Ravenhorst-Kalovski 2010](https://scholarspace.manoa.hawaii.edu/bitstream/10125/66648/1/22_1_10125_66648_laufer.pdf); [van Zeeland & Schmitt 2013](https://doi.org/10.1093/applin/ams074)), but comprehension rises smoothly rather than at a cliff ([Schmitt et al. 2011](https://www.lextutor.ca/cover/papers/schmitt_etal_2011.pdf)) | Strong | Coverage is a dial the planner can turn, easier on tired days. |
| GPT-4 hits the exact requested CEFR level only 48% of the time even with the best prompts ([Imperial et al. 2024](https://aclanthology.org/2024.emnlp-main.94/)); generating 3 candidates and keeping the best-scored one halves the error of the best prompt ([Malik et al. 2024](https://arxiv.org/abs/2406.03030)) | Moderate | Level must be checked by code after generation, never trusted to the prompt. |
| Commercial assistant memory answered 57.7% of long-term memory questions versus 91.8% when the model read the history directly, and tended to overwrite important facts ([LongMemEval 2025](https://arxiv.org/abs/2410.10813)); models are weakest on time questions ([LoCoMo 2024](https://aclanthology.org/2024.acl-long.747)) | Strong | Do not use chat-style memory as the source of truth. Store facts with dates. |
| Memory systems tested missed most required updates, and 15 to 30% of their answers were hallucinated ([HaluMem 2025](https://arxiv.org/abs/2511.03506)) | Weak (preprint) | Every remembered fact needs a source quote and a gate before it is spoken. |
| Users of ChatGPT memory were often unpleasantly surprised by what it held and want visibility and control ([Chen et al. 2026](https://grady.uga.edu/research/ai-never-forgets-exploring-users-perceptions-of-ai-memory-and-chatgpts-memory-feature/); [Zhang et al. 2025](https://arxiv.org/abs/2508.07664)) | Moderate (interviews) | Build the "what the show knows" page from day one. |
| Highly personalized ads did worse than moderately personalized ones (click rate 0.032% versus 0.077%), and the penalty came from data collected without people knowing ([Aguirre et al. 2015](https://openaccess.city.ac.uk/15747/)); showing why works when the data was stated by the user, and backfires when it was inferred ([Kim et al. 2019](https://dash.harvard.edu/entities/publication/4ee65cbf-26d4-49d9-b1b3-542e49a05fdd)) | Strong | Use only what the learner told the show, and say where it came from. |

## The learner model

The learner model is nine stores, and the first three are where the learning value lives. The PRD's four-section learner file has the right instincts, but its language side is too coarse to drive generation: "vocabulary rings" (confident, emerging, unseen) cannot tell the writer whether a given script is 95% known. The engine needs a probability per word.

| Store | What it holds, per item | Written by | Used for |
| --- | --- | --- | --- |
| Word bank | Every word and multi-word chunk met: chance they understand it, chance they can produce it, encounters, last seen, next review due | Code, from taps, replays, transcripts | The coverage check, the review schedule, the new-word budget |
| Structure map | Each grammar construction of the target language: never met, heard, attempted, accurate, or avoided, with the learner's own example sentences | Analyst, checked by code | Targets, nudges, the polish card |
| Error profile | Recurring errors in the fixed taxonomy, each with 2 or 3 verbatim examples and a lifecycle state (active, taking, retired, re-check) | Analyst | Correction, the weekly proof |
| Skills | Listening speed they cope with, reading speed, speech rate, pause ratio, average turn length | Code | Episode speed and length, call pacing |
| Interests | Topics with salience, depth (curious, fan, expert) and recency, plus hard dislikes and no-go topics | Producer and behavior | Pitches, the wildcard |
| Life | People, places, plans, dated events; each with the source quote, a confidence, a sensitivity class and an expiry | Producer and analyst, confirmed before use | Callbacks, real-life rehearsal, follow-ups |
| Goals | The real situations they need the language for, as can-do statements ("handle a call with my landlord") | Producer | Register, rehearsal scenes, the proof |
| Taste | Formats, hosts, humor, episode length, time of day, and what makes them talk the most | Code, from behavior | Pitch ranking, the writer's brief |
| Show canon | What has been said, host opinions, running jokes, positions the learner took | Analyst | No repeats, callbacks, continuity |

Two rules keep the model honest. Taste is preference, never "learning style": the evidence says matching instruction to a style does not improve learning, so taste only decides what people enjoy and choose. And understanding and producing a word are tracked separately, because learners can understand far more words than they can use.

## Learning about the learner without interrogating them

Everything the show needs can be read from what the learner already does, except the first guess about their level. So the plan is: a very short start, then let behavior do the work, and ask only when asking is natural.

**What each action tells the model**

| What the learner does | What the model learns | How strong |
| --- | --- | --- |
| Taps a word for its meaning | They probably do not understand it yet | Strong for that word |
| Finishes a script without tapping a word | Weak sign they know it (many people just do not tap) | Weak; never enough on its own |
| Replays a sentence or slows the audio | Listening load was too high there | Medium, for listening speed and that sentence's words |
| Uses a word correctly without being prompted | They can produce it | Strong |
| Avoids a structure when the host set it up | Not ready to produce it | Medium, after repeats |
| Makes an error | Evidence for an error pattern (3 times across 2 sessions to count, as the PRD says) | Medium |
| Picks, remixes or skips a pitch | Interest and format taste | Medium |
| Talks much longer on one topic | What makes them talk | Strong, and the most useful taste signal |
| Mentions something about their life | A candidate life fact, stored with its quote at low confidence | Low until repeated or confirmed |
| Corrects the show | Ground truth | Overrides everything |

**Cold start in three minutes, not ten.** The PRD's 10-minute intake asks a lot before the learner has seen anything good. I would collect four things up front (name, why this language, three interests, one real situation coming up), run the optional 60-second word check from decision 2, and start the first episode. A short yes/no list with fake words mixed in is a proven shortcut: LexTALE uses 60 items in about 3.5 minutes, and the Duolingo English Test uses yes/no items with pseudowords inside a 25-item adaptive test. The first three episodes are pitched one step easy and treated as calibration.

**Ask the way a host would.** Life details arrive as part of the show: the host asks "wait, you said you have an interview, when is it?" because a friend would, the answer is stored, and the show follows up after the date. Never a form, never more than one personal question per session.

**Borrow from other learners.** What is hard for Arabic speakers learning English (articles, for example) is a good starting guess for the next Arabic speaker. Population priors let the personal model start closer to right and need fewer observations. This needs some scale, so it comes after launch.

## Memory architecture

Structured memory is the source of truth, and no model writes to it directly. Chat-history memory (summaries of past conversations, retrieved by similarity) is how general assistants remember, and it is exactly where they drift, forget updates and invent. For one needs something closer to a medical record than a diary.

*Diagram: Models propose memories; code decides what is kept and who sees it.* Session (call, chat, taps, replays) → Analyst (a model; proposes updates as structured data) → Validator (code; checks each quote is real, flags conflicts) → **Ledger, the source of truth** (word bank, grammar and errors, life facts, interests and taste, goals, show canon; every fact keeps its quote and date). The raw session is also kept as is in the Archive (transcripts, scripts, consented audio; searched for callbacks). The "What the show knows" page lets the learner see, edit and delete anything, and edits win. From the ledger, code compiles a brief per role before each session: Showrunner (everything, summarized; plans the next day), Writer (interests, target words, 1 or 2 facts), Host live (words to elicit, one callback, one nudge), Coach (error patterns, the learner's sentences).

Three layers, each with one job:

- **Ledger.** A plain database. Every word, structure, error and fact is a row. Every life fact carries its source quote, session, date, confidence, sensitivity class and the period it is true for.
- **Archive.** Raw transcripts, scripts and consented audio. Searched for callbacks ("the time you argued the coach should go"), never fed whole to a model.
- **Briefs.** Before each session, code compiles a small packet per role. The live host gets the words to elicit, one callback and one nudge, not the whole file. Smaller briefs mean fewer chances to say something wrong, lower cost, and a stable prefix that prompt caching can reuse.

Rules for the write path:

1. **Models propose, code decides.** The analyst outputs candidate updates as structured data. A life fact is stored only if its quote appears word for word in the transcript.
2. **Facts have time.** "Works at the bank" is true from a date. A conflicting new fact supersedes the old one and keeps the history, so the show can say "how is the new job?" instead of mixing the two.
3. **A confidence ladder.** Heard once: stored, never said aloud. Repeated or confirmed: usable in content. Edited by the learner: ground truth.
4. **A weekly reflection.** A job turns raw evidence into a few insights ("talks most when defending an unpopular opinion"), each linked to the sessions that support it. An insight with no fresh evidence expires.

## Made once, language comes back

The planner picks the words first and the story second. "Used once" applies to the text; the language inside it is chosen by a review schedule, so the same words keep returning in new stories until the learner owns them.

*Diagram: Every episode is new text; the schedule decides which words are in it.* Planner (interest and format, words due for review, 1 or 2 structures, a few new words) → Writer (script, article, call brief, chat opener) → **Coverage check, code not a model** (95% known in audio, 98% in text, targets in every surface). Fail → Targeted rewrite (only failing sentences, at most twice) → back to the check. Pass → Ship (episode, article, call and chat all carry the targets) → Session (listens, reads, talks, writes) → Analyst (logs each word heard, read, or used) → Review scheduler (sets when each word comes back next) → Planner for the next episode.

Words come back through four channels, and only the first is review in disguise:

- **Same day, four surfaces.** A target word is heard in the episode, read in the article, asked for by the host in the call, and used or polished in the chat. One episode can deliver four to six encounters.
- **Across days.** The scheduler brings each word back at growing intervals until the learner uses it without prompting in two sessions.
- **Through a recurring world.** Hosts with ongoing opinions, running jokes and a topic that continues (the learner's team across a season) bring back the same vocabulary naturally. This is why decision 5 matters.
- **Through the learner's own sentences.** Nudges and the polish card reuse what the learner actually said, the most personal content there is.

The coverage check is code, not a prompt. A lemmatizer splits the script into words, the word bank gives the chance each is known, and the script passes when expected coverage clears the threshold and every target appears where planned. A failing script gets only its failing sentences rewritten, which is cheaper and keeps the story intact. Names and planned new words (glossed on tap) do not count against coverage.

Personal content plugs into this loop at the planner, not the writer. The interest decides the topic, at most one or two life facts decide the angle, and the schedule decides the words. That order is what stops personalization from being Mad Libs (the learner's name pasted into a generic script).

## Staying current and trusted

The model has to forget on purpose, change when the learner's life changes, and show its work. The ad research gives the clearest rule: people accept personalization built from what they chose to tell you, and recoil from what you inferred or collected quietly.

**Forgetting on purpose**

- Interests lose salience over a few weeks unless the learner engages with them again. Dormant interests are kept, never pitched, and come back the moment the learner mentions them.
- Each kind of life fact has its own shelf life: a job lasts months, "sick this week" lasts days. Expired facts are never spoken.
- A dated event ("interview Friday") triggers one follow-up after the date, then moves to history.
- Word knowledge decays on the forgetting curve the review scheduler already models, so a word unused for months is treated as shaky again.

**Five trust rules**

1. **Told, not inferred.** The show uses only what the learner said to it. No guessing at health, money, relationships, religion or politics, and nothing looked up about the person outside the app.
2. **Say where it came from.** A callback names its source naturally: "you told me on Tuesday the new manager is strict."
3. **Sensitive topics are learner-led.** If the learner raises something sensitive, the host can engage in that session. It is stored only if the learner confirms, and never brought up first.
4. **Everything is visible and editable.** The "what the show knows" page lists life facts, interests and (per decision 1) the language side in plain words, each with its source and date. Every item can be edited, deleted, or marked "don't bring this up".
5. **A wrong memory is a bug, not a quirk.** When the learner corrects the show, the host says so plainly, the fact is fixed, and the error is logged and counted as a quality metric.

## Risks and how to blunt them

The most likely failure is not creepiness; it is personalization so shallow that episode 30 feels like episode 3 with a different noun.

| Risk | What it looks like | How to blunt it |
| --- | --- | --- |
| Shallow personalization | The learner's name and team pasted into a generic script | The personal angle must drive the episode's conflict. The quality gate asks "would this episode work unchanged for another learner?" and fails it if yes. |
| Sameness over time | Every episode about football, same jokes, same shape | Show canon blocks repeated angles; one wildcard pitch from an adjacent interest; format rotation tracked by the planner |
| Narrowing | Vocabulary stays inside a few topics; the learner never meets general language | The planner also tracks coverage of a general frequency list and steers topics toward gaps (a design hypothesis; there is little direct evidence on educational filter bubbles) |
| Distraction | Fun personal details pull attention from the target language | Personal details carry target words; at most 1 or 2 life references per episode |
| False memories | "How was your sister's wedding?" when there was no wedding | Quote-backed facts, the confidence ladder, a canon check before shipping, and the wrong-memory rate as a tracked metric |
| Creepiness | The show seems to know things the learner never said | Told-not-inferred rule, sources named, sensitive topics learner-led, the visible "what the show knows" page |
| Level drift | Scripts creep above the learner's level, or a model update changes the writing | The coverage check is code; a fixed set of test briefs is re-run whenever the model or prompts change |
| Blind spots in the model | It learns only from what it chose to show | A small exploration budget (a slightly harder word, an untried format) and a fixed speaking sample every 4 weeks |
| Cost | Content that is never reused cannot get cheaper with scale | Shared ingredients (decision 4), prompt caching of the stable brief prefix (cache reads cost a tenth of normal input or less on [Anthropic's API](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)), overnight work through batch APIs at [half price](https://platform.claude.com/docs/en/build-with-claude/batch-processing), and rewriting failing sentences instead of whole scripts |
| Privacy and law | Voice recordings and life details are sensitive personal data | Collect the minimum, keep audio opt-in, honor export and delete instantly as the trust contract promises; get legal review before launch in the EU |

## How to know personalization is working

Personalization has to earn its cost on two separate scores: does it make people come back, and does it make the time count. Test each layer on its own, starting in Milestone 0.

| Question | Test | Pass looks like |
| --- | --- | --- |
| Does "about you" beat "at your level"? | Within each tester, alternate days: a fully personal episode, and a generic one at the same level with the same target words | Personal days win on choice, finishing and minutes of speech. If they do not, the life layer is decoration and should stay thin. |
| Is the level right? | After each episode, one tap: "how much did you follow?" Compare with the coverage the engine predicted | Predicted coverage and felt comprehension move together; misses shrink over the first 2 weeks |
| Do recycled words stick? | Count words that move from "heard" to "used correctly without prompting in 2 sessions" | A steady weekly count of words owned, rising faster for words the engine scheduled than for words it did not |
| Is memory accurate? | Every callback the learner flags as wrong, or edits on the "what the show knows" page | Under 1 in 100 callbacks flagged wrong (my target, not a benchmark) |
| Does it feel too personal? | A one-tap "that was a bit much" on any callback | Rare, and never twice for the same kind of fact |

The last two are guardrails, not goals. A product whose memory is wrong once in twenty callbacks loses the "knows me" feeling faster than it ever built it.

## Build order

Build the invisible "for you" layer first, because it is where learning comes from and it is mostly ordinary code.

1. **Milestone 0 (hand-run, 10 to 15 people).** A frequency-list word bank seeded by the 60-second check, a coverage script run on every hand-checked episode, a spreadsheet of target words with their review dates, and interests plus a few life facts kept by hand. Run the personal-versus-generic test above.
2. **Private beta.** The ledger with provenance on every fact, the analyst and its validator, the coverage checker with targeted rewrites, a per-word review scheduler, compiled briefs per role, and the "what the show knows" page. Shared ingredients and prompt caching from day one.
3. **After launch.** Priors learned across learners with the same native language (which words and structures are hard for Arabic speakers, for example) so a new learner's model starts closer to right; a learned taste model; the weekly reflection job; bring-your-own-input episodes that run through the same coverage check.
4. **Later.** Real-life rehearsal scenes built from goals and dated events, and an export of the learner model a human tutor can read.

## Sources

Each source was opened during this research. Figures marked "about" or taken from secondary summaries (the self-reference and seductive-detail effect sizes) should be rechecked before quoting publicly. Vendor-run benchmarks (Mem0, Zep) are not cited for claims.

**Learner modeling and review**

- [Corbett & Anderson 1994, knowledge tracing](https://doi.org/10.1007/BF01099821)
- [Piech et al. 2015, deep knowledge tracing](https://papers.neurips.cc/paper/2015/hash/bac9162b47c56fc8a4d2a519803d51b3-Abstract.html)
- [Khajah, Lindsey & Mozer 2016, How deep is knowledge tracing?](https://arxiv.org/abs/1604.02416)
- [Wilson et al. 2016, Bayesian IRT versus neural networks](https://arxiv.org/abs/1604.02336)
- [Gervet et al. 2020, when deep learning is best for knowledge tracing](https://doi.org/10.5281/zenodo.4143614)
- [Liu et al. 2022, pyKT benchmark](https://proceedings.neurips.cc/paper_files/paper/2022/hash/75ca2b23d9794f02a92449af65a57556-Abstract.html)
- [Settles & Meeder 2016, half-life regression](https://aclanthology.org/P16-1174)
- [Settles et al. 2018, SLAM shared task](https://aclanthology.org/W18-0506)
- [Duolingo Birdbrain, IEEE Spectrum 2023](https://spectrum.ieee.org/duolingo)
- [Lindsey et al. 2014, personalized review](https://doi.org/10.1177/0956797613504302)
- [Ye, Su & Cao 2022, SSP-MMC scheduling](https://doi.org/10.1145/3534678.3539081)
- [Open spaced-repetition benchmark (FSRS)](https://github.com/open-spaced-repetition/srs-benchmark)
- [Settles, LaFlair & Hagiwara 2020, Duolingo English Test](https://aclanthology.org/2020.tacl-1.17)
- [Lemhöfer & Broersma 2012, LexTALE](https://doi.org/10.3758/s13428-011-0146-0)
- [Nation, Vocabulary Size Test specification](https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-tests/the-vocabulary-size-test/Vocabulary-Size-Test-information-and-specifications.pdf)
- [Webb 2008, receptive and productive vocabulary](https://doi.org/10.1017/S0272263108080042)
- [Shute, Ventura & Kim 2013, stealth assessment validity](https://doi.org/10.1080/00220671.2013.832970)

**Personalization and learning**

- [Kulik & Fletcher 2016, tutoring systems meta-analysis](https://www.ida.org/research-and-publications/publications/all/e/ef/effectiveness-of-intelligent-tutoring-systems-a-meta-analytic-review)
- [Ma et al. 2014, tutoring systems meta-analysis](https://doi.org/10.1037/a0037123)
- [Pane et al. 2015, RAND personalized learning](https://doi.org/10.7249/RR1365) and [2017 follow-up](https://doi.org/10.7249/RR2042)
- [Escueta et al. 2020, education technology review](https://doi.org/10.1257/jel.20191507)
- [Lin et al. 2024, personalized learning by interest meta-analysis](https://doi.org/10.1007/s10648-024-09933-7)
- [Leong et al. 2024, AI context personalization for vocabulary](https://www.media.mit.edu/publications/putting-things-into-context)
- [Tasdelen & Bodemer 2025, AI-personalized material](https://doi.org/10.1007/s40593-025-00491-9)
- [Do et al. 2024, personalized AI podcasts (preprint)](https://arxiv.org/html/2409.04645v1)
- [Cordova & Lepper 1996, personalization and choice](https://www.kellogg.northwestern.edu/academics-research/research/detail/1996/intrinsic-motivation-and-the-process-of-learning-beneficial-effects)
- [Walkington 2013, interest-based algebra (coverage)](https://edsurge.com/news/2013-11-08-can-interest-based-personalization-deliver-better-learning-outcomes)
- [Bernacki & Walkington 2018, situational interest](https://doi.org/10.1037/edu0000250)
- [Walkington & Bernacki 2018, design dimensions of personalization](https://doi.org/10.1080/00220973.2017.1380590)
- [Reber, Canning & Harackiewicz 2018, personalized education](https://doi.org/10.1177/0963721418793140)
- [Patall, Cooper & Robinson 2008, choice meta-analysis](https://doi.org/10.1037/0033-2909.134.2.270)
- [Hidi & Renninger 2006, four-phase model of interest](https://doi.org/10.1207/s15326985ep4102_4)
- [Pruss, Karni & Prior 2025, self-reference and L2 vocabulary](https://doi.org/10.3758/s13423-025-02674-w)
- [Qahl & Lambert 2025, self-reference in L2 word learning](https://doi.org/10.1002/tesq.3402)
- [Harp & Mayer 1998, seductive details](https://doi.org/10.1037/0022-0663.90.3.414)
- [Sundararajan & Adesope 2020, seductive details meta-analysis](https://doi.org/10.1007/s10648-020-09522-4)
- [Pashler et al. 2008, learning styles](https://doi.org/10.1111/j.1539-6053.2009.01038.x)
- [Pardos & Jiang 2019, novelty in course recommenders](https://arxiv.org/abs/1907.01591)

**Generation, memory and trust**

- [Laufer & Ravenhorst-Kalovski 2010, lexical threshold](https://scholarspace.manoa.hawaii.edu/bitstream/10125/66648/1/22_1_10125_66648_laufer.pdf)
- [van Zeeland & Schmitt 2013, coverage for listening](https://doi.org/10.1093/applin/ams074)
- [Schmitt, Jiang & Grabe 2011, coverage and comprehension](https://www.lextutor.ca/cover/papers/schmitt_etal_2011.pdf)
- [Malik et al. 2024, controlling LLM proficiency level](https://arxiv.org/abs/2406.03030)
- [Imperial et al. 2024, aligning LLMs with CEFR standards](https://aclanthology.org/2024.emnlp-main.94/)
- [Almasi & Kristensen-McLachlan 2025, level drift in tutoring (preprint)](https://arxiv.org/abs/2505.08351)
- [Park et al. 2023, generative agents memory](https://arxiv.org/abs/2304.03442)
- [Packer et al. 2023, MemGPT](https://arxiv.org/abs/2310.08560)
- [Rasmussen et al. 2025, Zep temporal knowledge graph](https://arxiv.org/abs/2501.13956)
- [Wu et al. 2025, LongMemEval](https://arxiv.org/abs/2410.10813)
- [Maharana et al. 2024, LoCoMo](https://aclanthology.org/2024.acl-long.747)
- [Chen et al. 2025, HaluMem (preprint)](https://arxiv.org/abs/2511.03506)
- [Chen, Molina, Liao & Cho 2026, users' perceptions of ChatGPT memory](https://grady.uga.edu/research/ai-never-forgets-exploring-users-perceptions-of-ai-memory-and-chatgpts-memory-feature/)
- [Zhang et al. 2025, privacy perceptions of LLM memory](https://arxiv.org/abs/2508.07664)
- [Aguirre et al. 2015, the personalization paradox](https://openaccess.city.ac.uk/15747/)
- [Kim, Barasz & John 2019, Why am I seeing this ad?](https://dash.harvard.edu/entities/publication/4ee65cbf-26d4-49d9-b1b3-542e49a05fdd)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
