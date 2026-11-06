# For one through the lens of learning science

*One of 11 perspectives · 9 October 2026 · written for Muath*

This is one lens on For one: how human memory and skill learning work, and what that means for the product. It covers memory and forgetting, spacing, retrieval, interleaving, desirable difficulties, feedback and its timing, cognitive load, transfer, and what actually makes one-to-one tutoring work. Second-language research appears only where it tests these general principles on language; the SLA, motivation and UX lenses are other threads.

The first rethink already covered comprehension coverage (95 to 98% known words), the weakness of recast-only correction, the Four Strands and the 2-sigma caveat. This page does not repeat those. It goes one level down: why learning sticks or fades, and what the AI should do minute by minute because of it.

**How to read the labels.** *Strong* means replicated across many studies or meta-analyses. *Moderate* means several good studies or one meta-analysis with caveats. *Thin* means a few studies, lab-only, or not yet tested on language. Anything marked **My judgment** is my inference, not the literature's.

---

## Decisions only you can make

Three choices decide how much of this research the product can use. My recommendation is first; the rest of the page assumes it.

| # | Decision | Recommended | Alternative | Why it matters |
|---|---|---|---|---|
| A | Can the show ask you to *recall*? | Yes. Hosts may set up moments where you have to pull a word or phrase out of memory ("how did you put it yesterday?") before they say it. Never scored, never called a test. | Keep "no prompts, no tests" literally, so the learner only ever hears and responds freely | Retrieval is the single strongest memory effect in this literature. Without it, the planner can only re-expose words, which is the weakest way to keep them. |
| B | What does the product count as "learned"? | Only what the learner produces correctly **a day or more later, unprompted, in a new context**. That number drives targets, retirement and the weekly proof. | Count in-session success, as the PRD does now ("produced correctly unprompted once") | Performance during a session is a poor guide to what will last. Measuring at a delay is the difference between a teacher that knows you and one that flatters you. |
| C | When fun and learning conflict inside an episode, which wins? | Neither by rule. **The fun must carry the language**: every joke, twist and personal reference uses that learner's target or due words. Fun that carries nothing gets cut. | "The episode is king": entertainment wins every conflict | Interesting material that is off-target measurably reduces learning. This turns your "entertainment is the strategy" into something a quality gate can check. |

These sit alongside the six decisions in the first rethink. This lens adds weight to two of them: decision 3 (correction) and decision 4 (honest progress).

---

## The verdict

Your core instinct is right: practice beats studying a book, and a teacher who knows one learner beats any course. But the research says *why* practice works, and that changes the design. Practice works when it forces you to **retrieve** and **produce**, **spaced over time**, with **feedback you notice**. Practice that only exposes you to language again (re-listening, re-reading, hearing a recast you don't register) feels productive and is the weakest form of all. Learners cannot tell the difference from the inside.

The current concept is excellent at getting exposure and enjoyment, and at personalization, which turns out to help memory directly, not only motivation. It is weak at the three things memory needs most: making the learner pull things out of memory, bringing them back on a schedule, and judging learning at a delay rather than in the moment. All three can be added without breaking the show. The hosts just need permission to make the learner *do* a little more of the work.

---

## What the research says, and what it means for For one

### 1. Forgetting is the default. Only retrieved, spaced memories last.

**Evidence (Strong).** Memory decays fast after a single exposure unless it is used again (Ebbinghaus, replicated by Murre & Dros 2015). Spreading practice out beats cramming it: across 184 articles, spaced recall averaged 47% against 37% for massed (Cepeda et al. 2006). The best gap between sessions depends on how long you want to remember: about 20 to 40% of the retention interval for a test a week away, falling to 5 to 10% for a test a year away (Cepeda et al. 2008). Foreign vocabulary reviewed 13 times at 56-day intervals was retained as well as vocabulary reviewed 26 times at 14-day intervals, years later (Bahrick et al. 1993). School Spanish that survived the first few years stayed stable for decades (Bahrick 1984). For second languages specifically, a meta-analysis of 48 experiments found a medium-to-large spacing benefit, with longer gaps winning on delayed tests and equal versus expanding schedules performing about the same (Kim & Webb 2022).

**Evidence (Moderate, and an exception).** For *grammar procedures* in beginners, shorter gaps did better: 1 day beat 7 days for speed of producing Japanese morphology (Suzuki & DeKeyser 2017), and 3.3 days beat 7 days for accuracy (Suzuki 2017). Skills seem to want tighter early practice than word memories do.

**What the concept supports.** Daily sessions and the 2-per-day cap are spacing by design. The PRD's target re-checks at 2, 4 and 8 weeks are an expanding spacing schedule. Both are well founded.

**What it contradicts or misses.** "Every session is self-contained; only memory persists" treats the learner file as the only thing that should persist. The *language* also has to persist, on a schedule. Re-checks today exist only for grammar targets (max 4 active). Nothing schedules the hundreds of words a learner meets each week, and nothing models when each one will be forgotten.

**My judgment.** The planner needs a memory model per item, not per learner. Every word, chunk and structure the learner has met gets an estimated "probability you'd still recall this today". That estimate, not topic or recency, decides what gets woven into tomorrow's episode. Grammar targets get tight early spacing (every 1 to 3 days); vocabulary gets widening gaps.

### 2. Pulling something out of memory teaches more than putting it in again.

**Evidence (Strong).** Testing yourself beats restudying: g = 0.50 across 159 effect sizes (Rowland 2014); a later meta-analysis of 272 effect sizes found practice tests beat restudy and every other comparison (Adesope et al. 2017). The classic demonstration used Swahili vocabulary, the closest lab analogue to your product: one week later, learners who kept retrieving recalled about 80%, those who stopped retrieving but kept studying recalled 36% (Karpicke & Roediger 2008). In the same study, every group *predicted* about 50%. Their predictions did not differ by condition and did not track what they actually recalled.

**Evidence (Strong): learners misjudge this.** 84% of students list rereading as a study strategy and 11% list self-testing (Karpicke, Butler & Roediger 2009). In a spacing study, 78% of learners did better with spacing while 78% judged massing as equal or better (Kornell & Bjork 2008). Performance during practice is a poor guide to long-term learning, and learners routinely confuse the two (Soderstrom & Bjork 2015).

**What the concept supports.** "The show owns the pedagogy; difficulty and sequencing are never the user's burden" is exactly right, because users would choose badly. Learners left alone re-listen and re-read.

**What it contradicts.** Law 1 bans "tests" and "prompts", and the call-in host is told never to steer. Read literally, that rules out retrieval. The PRD's retention signals (tap-to-define repeats, replays, scrub clusters) all measure re-exposure.

**My judgment.** "No tests" should mean *no test furniture*, not *no recall*. Retrieval can live inside a conversation:
- The host leaves a gap the learner fills: "What was that word you used for your boss on Tuesday? The one that made Karim laugh."
- The chat opener asks the learner to retell one point from the episode before the host adds anything.
- The weekly proof opens with "three words from your week; say them before we do".
None of these is scored, and all are recall.

### 3. Struggle first, then the answer.

**Evidence (Strong).** Generating an answer yourself is remembered better than reading it: a mean effect of about 0.40 SD across 86 studies (Bertsch et al. 2007). Even *failed* attempts help, as long as the right answer follows: guessing before being told beats extra study time (Kornell, Hays & Bjork 2009; Richland, Kornell & Kao 2009). A 2024 meta-analysis found prequestions improve memory for the tested material (g = 0.54), more so when learners must commit to a guess (g = 0.65 against 0.22 for just reading the question), but give no benefit for untested material (St. Hilaire, Chan & Ahn 2024; review in Pan & Carpenter 2023). Errors made with high confidence are *more* likely to be corrected after feedback than low-confidence ones (Butterfield & Metcalfe 2001).

**What the concept supports.** The call-in is generative by nature, and the article asks the learner to take a side, which is a commitment.

**What's missing.** No moment in the cycle asks the learner to try to say something *before* they hear the model. The episode always gives first and asks later.

**My judgment.** Add "try first" moments in two places. (1) A 30-second cold open before the episode: the host asks how the learner would say the episode's key idea ("how would you tell someone the referee robbed us?"); the episode then uses the natural phrasing; the learner hears the gap themselves. (2) In the polish card the first rethink proposed: show the learner's own sentence and ask them to try fixing it before revealing the better version. Confident errors (said fluently, repeated, not self-corrected) are the best ones to surface, because they are the ones feedback fixes most.

### 4. Feedback works when it is informative, about the task, and noticed.

**Evidence (Strong).** Feedback is one of the larger effects in education, d = 0.48 across 435 studies, and much larger when it carries real information about what to change (d = 0.99) than when it is reward or praise (d = 0.24) (Wisniewski, Zierer & Hattie 2020). But over a third of feedback interventions made performance *worse*, mostly when feedback pulled attention toward the self rather than the task (Kluger & DeNisi 1996). Praise directed at the person is the least effective kind (Hattie & Timperley 2007).

**Evidence (Moderate): timing.** In classroom settings immediate feedback usually wins; in some lab studies of test content, delayed feedback wins, probably because the delay adds spacing (Kulik & Kulik 1988; Butler, Karpicke & Roediger 2007). For second-language grammar, immediate correction during a communicative task was somewhat better than correction at the end, on one of two measures (Li, Zhu & Ellis 2016; Arroyo & Yilmaz 2018). A 2025 review calls the timing evidence "equivocal" and notes learners prefer immediate feedback (Li, Ou & Lee 2026).

**What the concept supports.** "Never grades, never praises per turn" matches the evidence almost exactly: grades and person-praise are the weakest or harmful kinds. This is one of the best-founded laws in the PRD.

**What it contradicts.** Recast-only correction is feedback designed *not* to be noticed. The research says feedback helps when it carries information the learner registers. Invisible feedback is safe from harm but also mostly safe from effect. (The first rethink covers the SLA evidence on recasts; this is the general-psychology version of the same point.)

**My judgment.** Use both timings for different jobs. In the call: a quick, noticeable recast, and at most one "wait, yesterday you...?" prompt, because immediacy helps grammar and keeps the call flowing. After the call or next day: the polish card, which uses the spacing advantage of delay. Feedback language is always about the sentence, never about the person ("*went*, because it's yesterday", not "great job!").

### 5. Mix the things that are easy to confuse.

**Evidence (Strong, with a twist).** Interleaving different kinds of problems beats practicing them in blocks overall, g = 0.42 across 238 effect sizes, but the benefit depends on similarity. It is large when the items are easy to confuse (paintings by similar artists, g = 0.67), and *reversed* for vocabulary lists (g = −0.39) (Brunmair & Richter 2019). For L2 grammar, mixing five English structures caused more errors in practice but better retention a week later, with weaker learners benefiting most (Nakata & Suzuki 2019). For Spanish preterite versus imperfect, interleaving helped when practice spread over two sessions, not in one (Pan et al. 2019).

**What the concept supports.** Natural conversation already interleaves. A show about your week mixes past, present and future without being told to.

**What's missing.** The planner picks 1 to 2 targets per session by "frequency × recency × readiness". That can easily produce one structure per episode, which is blocking.

**My judgment.** Choose targets in **contrast pairs** where the learner confuses them (past simple versus present perfect; *por* versus *para*; *ser* versus *estar*) and build episodes where both are needed. Do not deliberately interleave unrelated vocabulary; let words cluster around the topic.

### 6. Sleep does part of the work.

**Evidence (Strong for the effect; Thin for product design).** New spoken words only start behaving like real words in the mental lexicon after a night's sleep (Dumay & Gaskell 2007). Learners who slept between two sessions of Swahili-French vocabulary needed about half as many trials to relearn the words (3.05 against 5.80) and recalled more than twice as many six months later (8.7 against 3.4 of 16) as those who stayed awake the same 12 hours (Mazza et al. 2016).

**What the concept supports.** The overnight planner is the right rhythm. A product that plans while you sleep and greets you with what you met yesterday lines up with how consolidation works.

**What's missing.** The planner uses the night to plan, but the learner's first contact the next day is new content, not yesterday's language.

**My judgment.** Open each day's episode with a short callback to yesterday's new words or phrases, in a new context. That is relearning after sleep, the condition that produced the biggest effect above. If the learner's session is in the evening, the next morning's cold open is the most valuable 30 seconds in the product.

### 7. Personalization helps memory, not only motivation.

**Evidence (Strong).** Information related to yourself is remembered better than the same information processed for its meaning alone (self-reference effect, Symons & Johnson 1997, average effect about 0.45 SD). States of curiosity improve memory for the answer *and* for unrelated things encountered while waiting for it (Gruber, Gelman & Ranganath 2014). Novel words met in more varied contexts were recognized faster and more accurately than words met in repetitive contexts (Johns, Dye & Jones 2016); in adult reading, varied contexts made words slower to learn at first but gave a larger benefit afterwards (Pagán & Nation 2019).

**Evidence (Moderate).** Humorous sentences are remembered better than plain ones, though mainly when they stand out among non-humorous material (Schmidt 1994). In classrooms, appropriate humor reliably improves climate and motivation; its effect on learning is mixed (Banas et al. 2011).

**What the concept supports.** Strongly. "About you, for you, by you" is not only a retention strategy. A story about *your* derby, *your* interview, with *your* hosts' running jokes, is encoded better. The first rethink said personalization raises motivation more than learning per minute; the self-reference and curiosity evidence suggests the memory benefit is real too, though no study has tested it on AI-personalized language content. "Every lesson used once" is, from a memory standpoint, a contextual diversity engine: each recurring word comes back inside a new story.

**My judgment.** Two mechanics follow. (1) Place target and due words *inside* the personal moments (the callback to the learner's life, the punchline, the twist), because that is where encoding is strongest. (2) Use the unresolved argument at the end of the episode as a curiosity window: put the key phrases the learner will need in the call right there, while curiosity is high.

### 8. Working memory is small, and listening is the hardest place to spend it.

**Evidence (Strong, general).** Spoken information is transient: you cannot look back at it, so long stretches of audio overload working memory in a way the same content as text does not (Leahy & Sweller 2011, 2016). Breaking material into segments the learner advances through at their own pace helped in 10 of 10 experiments, median effect 0.79 (Mayer & Pilegard 2014). Interesting but irrelevant additions ("seductive details") reduce learning, g = −0.33 (Sundararajan & Adesope 2020; Rey 2012). Support that helps novices can stop helping, or hurt, once learners are more expert (expertise reversal, Kalyuga et al. 2003).

**Evidence (Moderate, language-specific).** In general multimedia research, showing text that duplicates narration is a mistake. For second-language listening it is the reverse: captioned video improves vocabulary learning (g ≈ 0.87) with large effects on listening comprehension (Montero Perez, Van Den Noortgate & Desmet 2013). Glosses while reading help: 45% of glossed words learned against 27% without, immediately, and 33% against 20% later; first-language glosses beat target-language ones, and glosses that make you pick between options work best (Yanagisawa, Webb & Uchihara 2020). Slower speech helps lower-intermediate listeners (Griffiths 1992; Thin). Speaking a second language under time pressure splits attention between what to say and how to say it, because formulation is not yet automatic; fluency, accuracy and complexity compete for the same limited attention (Kormos 2006; Skehan 2009). Time to plan before speaking reliably improves fluency; effects on accuracy and complexity are less consistent (Ellis 2009; Johnson & Abdi Tabari 2022).

**What the concept supports.** A lot. The word-synced transcript is captioning. Tap-to-define with a first-language meaning is the better kind of gloss. The 0.8× speed option helps lower levels. The 8-minute ceiling limits transient load. Reading the article before the call is planning time, which is the best-supported way to make L2 speech more fluent.

**What it contradicts or risks.** (1) A show is built from banter, asides and running jokes. Banter that does not carry the learner's language is a seductive detail: enjoyable and slightly harmful to learning. (2) The same supports forever (full transcript visible, every word tappable) will stop helping intermediate-to-advanced learners and may hold them back. (3) The call-in asks for real argument with "real stakes" while speaking a second language, which is the highest load in the product. Grammar correction competes for the same attention, which is one more reason most correction belongs after the call.

**My judgment.**
- Make the episode learner-paced at scene level: a natural pause point between scenes, plus one-tap replay of the last sentence. That is segmenting without breaking the show.
- Fade the transcript as the learner grows: on and synced for early learners; later, a first listen without it and the transcript offered for a second pass. The planner decides, per learner.
- For words the learner has already looked up before, the popover can occasionally ask first ("you looked this up Tuesday; which one?") with two options. That turns a repeat lookup into a retrieval and uses the most effective gloss format. Never for a first lookup.
- Before the call, offer 30 to 60 seconds of planning ("jot your two best points"), optional and skippable.
- Keep in-call correction light and push the rest to the chat and the polish card, because the call is already at the learner's attention limit.

### 9. Practice builds the skill you practice.

**Evidence (Strong).** Learners trained an artificial language's grammar through comprehension practice or production practice for eight weeks; each group improved at the skill it practiced, and performance was "severely reduced if only the opposite skill was practiced" (DeKeyser 1997). Memory works best when the conditions of learning match the conditions of use (transfer-appropriate processing; Morris, Bransford & Franks 1977; applied to classroom L2 learning by Lightbown 2008). Far transfer, to a different context, purpose or format, is hard and cannot be assumed (Barnett & Ceci 2002).

**Evidence (Moderate).** Repeating the same speaking task improves fluency and complexity on the repeat (Bygate 2001); a 2025 meta-analysis found substantial gains for complexity and accuracy and smaller ones for fluency, with longer gaps between repetitions giving smaller effects (Abdi Tabari, Zhuang & Farahanynia 2025). On a *new* task of the same type, fluency and accuracy gains shrink while complexity carries over (Sheppard & Ellis 2018).

**What it means for your 30/15/5/10 hour.** The hour builds the skills it spends time on: strong listening and reading, much less speaking. Comprehension practice will not turn into speaking ability on its own; the DeKeyser result is the cleanest evidence that skills learned through one channel do not automatically appear in the other. Three changes follow, all my judgment:
- **Count the learner's own speech, not the stage.** "Five minutes of speaking" in a call-in is closer to two or three minutes of the learner actually talking. The planner should track the learner's own speaking time per week and aim for at least 4 to 5 minutes per session.
- **Repeat the call, a little.** A short "round two" the next day on the same argument, shorter and faster, is task repetition. It is the cheapest proven fluency builder, and it doubles as spaced retrieval of yesterday's language.
- **Rehearse the real situations.** Transfer favors practice that looks like real use. The learner's actual job interview, landlord call or family dinner should become episodes and calls, which is the "real-life rehearsal" idea in the first rethink, now with a memory reason behind it.

The daily cadence matters more than the length of the hour. Twenty spaced minutes every day beats a long session three times a week, and two shorter sessions hours apart beat one long one.

### 10. What makes one-to-one tutoring work, and how AI tutoring fails.

**Evidence (Strong).** Bloom's famous 2-sigma result was not tutoring alone. It was tutoring *plus mastery learning*: frequent formative checks, correctives, and a parallel check before moving on. Mastery learning alone, in a class of 30, gave about 1 sigma (Bloom 1984); across 108 evaluations it averages 0.52 SD (Kulik, Kulik & Bangert-Drowns 1990). Computer tutors that give feedback at each step of the learner's work come close to human tutors (0.76 against 0.79 SD); those that only judge final answers do much less (0.31) (VanLehn 2011). Students learned just as much when human tutors were stopped from explaining and only prompted them to think (Chi et al. 2001). Learning rises as the learner's activity goes from passive to active to constructive to interactive (ICAP, Chi & Wylie 2014). Expert human tutors rarely give direct negative feedback; over 90% of what they say is questions, and their hints go from general to specific (Lepper & Woolverton 2002).

**Evidence (Strong, and the main warning for AI products).** In a field experiment in high school math classes, unrestricted GPT-4 access during practice raised practice grades 48% and then *lowered* exam grades 17% once access was removed; a tutor version with guardrails that gave hints instead of answers raised practice grades 127% and largely avoided the harm (Bastani et al. 2025). University students who wrote with ChatGPT got the best essay scores but no better knowledge gain or transfer than students with no help (Fan et al. 2025).

**What the concept supports.** The learner file, the planner and the target lifecycle (Active, Taking, Retired, re-check) are a form of mastery learning. That is the half of Bloom's result most products forget.

**What it contradicts.** The host's contract optimizes for a pleasant conversation. A pleasant AI conversation partner is exactly the system that does too much of the learner's work: finishes their sentences, rephrases their meaning, answers "what does X mean" instantly. Passive listening is the bottom rung of ICAP, and it is half of your hour.

**My judgment.** The host's job is to make the learner *construct*, not to be good company. Concretely: the host never completes the learner's sentence; "how do I say X" gets a hint first (first letter, a related word, "you used it last week") and the full answer only on a second ask; "what does X mean" in the call gets a quick answer, because comprehension is the point there; writing help in the chat is a hint ladder, never a rewrite. The Bastani result is the clearest reason the product must not behave like a general chatbot.

### 11. Judge learning later, not now.

**Evidence (Strong).** Performance during or right after practice overestimates what lasts and can even move in the opposite direction from long-term learning (Soderstrom & Bjork 2015). Interleaving and spacing *lower* performance during practice while raising it later (Kornell & Bjork 2008; Nakata & Suzuki 2019). Adaptive review schedules that model each learner's memory beat generic spacing: +10% retention over a generic spaced schedule and +16.5% over massed, a month after a semester of Spanish (Lindsey et al. 2014). Duolingo's half-life regression model predicted recall with about half the error of its older Leitner system (Settles & Meeder 2016).

**What the concept supports.** The PRD's weekly CAF rating over 1- and 2-week windows, and the "2-week window wins" rule, are the right instinct.

**What it contradicts.** A target moves to "Taking" when "produced correctly unprompted once", which can happen 30 seconds after a recast in the same call. That is performance, not learning. A learner who repeats the recast back would advance.

**My judgment.** Redefine the lifecycle: *Taking* requires a correct, unprompted production in a different session at least a day later; *Retired* requires that again after a gap of a week or more in a different topic. The weekly proof should be built only from delayed evidence. This is decision B above.

---

## Scorecard: the current concept against this lens

| Element of the concept | Verdict | Why |
|---|---|---|
| Daily sessions, 2-per-day cap | Supported | Spacing (Cepeda 2006; Kim & Webb 2022) |
| Nightly planner | Supported | Matches sleep consolidation (Dumay & Gaskell 2007; Mazza 2016) |
| Target re-checks at 2, 4, 8 weeks | Supported | Spaced retrieval; equal or expanding both fine (Kang et al. 2014) |
| No grades, no per-turn praise | Strongly supported | Self-level feedback is weakest or harmful (Kluger & DeNisi 1996; Hattie & Timperley 2007) |
| The show owns the pedagogy | Strongly supported | Learners misjudge what works (Karpicke et al. 2009; Kornell & Bjork 2008) |
| About you, for you, by you | Supported, and more than the concept claims | Self-reference, curiosity, contextual diversity |
| Mastery-style target lifecycle | Supported in shape | Mastery learning ~0.5 SD (Kulik et al. 1990) |
| "No tests, no prompts" | Contradicted if read literally | Retrieval is the strongest memory effect (Rowland 2014) |
| Recast-only correction | Contradicted | Feedback must be noticed and informative (Wisniewski 2020) |
| "Taking" after one in-session success | Contradicted | Performance is not learning (Soderstrom & Bjork 2015) |
| One target structure at a time | Weak | Contrasting similar forms helps (Brunmair & Richter 2019) |
| Pleasant, accommodating host | Risky | AI that does the work harms learning (Bastani 2025) |
| Item-level memory model for words | Missing | Adaptive review beats generic (Lindsey 2014) |
| "Try first" moments | Missing | Generation and pretesting (Bertsch 2007; St. Hilaire 2024) |
| Next-day callback of new language | Missing | Relearning after sleep (Mazza 2016) |
| Learning measured at a delay | Missing | Decision B |
| Synced transcript, first-language glosses | Supported | Captions and glosses (Montero Perez 2013; Yanagisawa 2020) |
| Article before the call | Supported | Planning time (Ellis 2009) |
| Banter that carries no target language | Risky | Seductive details (Sundararajan & Adesope 2020) |
| Same supports for every learner forever | Risky | Expertise reversal (Kalyuga et al. 2003) |
| About 2 to 3 minutes of learner speech a day | Weak | Practice is skill-specific (DeKeyser 1997) |

---

## What changes in the product

### The daily cycle, rebuilt around how memory works

The shape stays: one episode, made for one person. What changes is the order of who does the work.

| Moment | Today | With this lens | Mechanism |
|---|---|---|---|
| Opening (30 to 60 s) | Episode starts | Host calls back 2 or 3 of yesterday's new words in a new line, then asks the learner how they'd say the episode's key idea | Relearning after sleep; pretesting |
| Episode | Listen, with transcript | Same, with sentence replay and learner-paced segments; target and due words placed inside the personal moments and the jokes | Self-reference; cognitive load |
| The throw | Unresolved argument | Unresolved argument that plants the 2 or 3 phrases the learner will need in the call | Curiosity window |
| Article | Read to take a side | Same; also the learner's planning time for the call | Pre-task planning |
| Call | Argue; recasts only | Argue; noticeable recasts; one prompt; 2 to 4 recall gaps; one 60-second retell; host gives hints, not answers | Retrieval; feedback; ICAP |
| Chat | 3 to 5 messages | Host's opener asks the learner to restate one point first; focused written correction | Generation; feedback |
| Polish card (optional) | none | Your sentence, try to fix it, then the better one; confident errors first | Pretesting; hypercorrection; delayed feedback |
| Next day | New episode | Yesterday's targets return in a new topic; only that counts toward "learned" | Spacing; learning versus performance |

### What the AI does differently

- **Analyst**: keeps a memory estimate for every word, chunk and structure the learner has met (a half-life model of the kind Duolingo published, or the open-source FSRS scheduler). It records which productions were prompted, which were spontaneous, and how long after the last exposure. This is code plus a small model, not a large model's judgment.
- **Showrunner (planner)**: builds each episode from a "due list" (items whose recall probability has dropped below a threshold) plus 1 to 2 new targets, chosen as contrast pairs. Grammar targets on tight spacing early; vocabulary on widening gaps.
- **Writer**: must place due items inside the personal or funny moments, not in filler. The quality gate gains a check: every joke and personal reference carries at least one target or due item ("no seductive details").
- **Host**: has a recall quota (2 to 4 gaps per call) and hint-first rules. Never completes the learner's sentence. One prompt per call.
- **Coach**: writes the polish card in try-first form, prioritizing confident, repeated errors.
- **Proof**: built only from delayed evidence ("you used *although* on your own on Tuesday and again today, eight days apart").

### Small changes to existing PRD rules

- Law 1: replace "no ... tests, prompts" with "no test *furniture*: nothing scored, nothing labelled a test, no right/wrong screens. Recall inside conversation is the show's job."
- Part 10.10 lifecycle: Taking = correct, unprompted, ≥1 day later, different session. Retired = again ≥7 days later, different topic.
- Part 9 planner: add the due list and contrast-pair selection.
- Part 5.1 player: add sentence replay and 0.75×; keep the 1.0× ceiling. Add scene-level pause points and fade the transcript as the learner grows.
- Part 15 metrics: add delayed recall of target items (share of items recalled correctly ≥7 days after first meeting them) as a primary learning metric next to engagement.

---

## Where the evidence is thin

- Most memory research uses word lists, trivia and short texts in a lab, over days or weeks. How well spacing and retrieval survive inside an entertaining, conversational, months-long product is plausible but untested.
- Incidental word learning from stories needs many encounters (as many as 20 for the maximum effect; Uchihara, Webb & Yanagisawa 2019), and learners' existing vocabulary changes how much repetition helps. Exact numbers per learner are a modelling problem, not a known constant.
- The ideal gap for grammar versus vocabulary in adults past the beginner stage is not settled (Suzuki 2017 versus Kim & Webb 2022).
- There is no study of "content used once" as such, and no strong study yet of LLM-personalized language content on long-term retention. The self-reference and curiosity effects are well established in general, not in this product.
- Evidence on LLM tutors is new: one strong math field experiment (Bastani 2025), a few language trials. Treat the anti-crutch rules as the best current guess.

---

## Sources

Every source below was checked against the paper, its abstract, or a reliable summary on 9 October 2026. Where only a secondary summary could be opened, the entry says so. Numbers marked "about" in the text are rounded from the source.

**Memory, forgetting and spacing**
- Cepeda, Pashler, Vul, Wixted & Rohrer (2006). Distributed practice in verbal recall tasks. *Psychological Bulletin* 132(3). [PDF](https://www.evullab.org/pdf/CepedaPashlerVulWixtedRohrer-PB-2006.pdf)
- Cepeda, Vul, Rohrer, Wixted & Pashler (2008). Spacing effects in learning: a temporal ridgeline of optimal retention. *Psychological Science* 19(11). [PubMed](https://pubmed.ncbi.nlm.nih.gov/19076480/)
- Kim & Webb (2022). The effects of spaced practice on second language learning: a meta-analysis. *Language Learning* 72(1). doi:10.1111/lang.12479 (effect sizes not quoted here; direction from the abstract)
- Bahrick, Bahrick, Bahrick & Bahrick (1993). Maintenance of foreign language vocabulary and the spacing effect. *Psychological Science* 4(5). [PDF](https://www.gwern.net/doc/psychology/spaced-repetition/1993-bahrick.pdf)
- Bahrick (1984). Semantic memory content in permastore. *J. Exp. Psych.: General* 113. Via [Conway et al. summary](https://users.cs.northwestern.edu/~paritosh/papers/KIP/ConwayLongTermRetention.pdf)
- Murre & Dros (2015). Replication and analysis of Ebbinghaus' forgetting curve. *PLOS ONE*. [Article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0120644)
- Suzuki & DeKeyser (2017). Effects of distributed practice on the proceduralization of morphology. *Language Teaching Research* 21(2).
- Suzuki (2017). The optimal distribution of practice for the acquisition of L2 morphology. *Language Learning* 67(3).
- Karpicke & Roediger (2007). Expanding retrieval practice promotes short-term retention, but equally spaced retrieval enhances long-term retention. *JEP: LMC* 33(4). [PDF](https://www.gwern.net/doc/psychology/spaced-repetition/2007-karpicke.pdf)
- Kang, Lindsey, Mozer & Pashler (2014). Retrieval practice over the long term: expanding or equal-interval? *Psychonomic Bulletin & Review* 21(6). [Article](https://link.springer.com/article/10.3758/s13423-014-0636-z)
- Lindsey, Shroyer, Pashler & Mozer (2014). Improving students' long-term knowledge retention through personalized review. *Psychological Science* 25(3). [PDF](https://home.cs.colorado.edu/~mozer/Research/Selected%20Publications/reprints/LindseyShroyerPashlerMozer2014Published.pdf)
- Settles & Meeder (2016). A trainable spaced repetition model for language learning. *ACL 2016*. [PDF](https://aclanthology.org/P16-1174.pdf)
- Uchihara, Webb & Yanagisawa (2019). The effects of repetition on incidental vocabulary learning. *Language Learning* 69(3).

**Sleep**
- Dumay & Gaskell (2007). Sleep-associated changes in the mental representation of spoken words. *Psychological Science* 18(1). [Repository](https://eprints.whiterose.ac.uk/7437)
- Mazza et al. (2016). Relearn faster and retain longer: along with practice, sleep makes perfect. *Psychological Science*. [PDF](https://www.gwern.net/doc/psychology/spaced-repetition/2016-mazza.pdf)

**Retrieval, generation and metacognition**
- Karpicke & Roediger (2008). The critical importance of retrieval for learning. *Science* 319. [PDF](https://www.brucehayes.org/Teaching/papers/2008_Roediger_Karpicke_Science.pdf)
- Rowland (2014). The effect of testing versus restudy on retention. *Psychological Bulletin* 140(6). [PDF](https://courseware.epfl.ch/assets/courseware/v1/fdde2f0aa590bf3b1324077a6bf1540c/asset-v1%3AEPFL%2BDEMO%2B2020%2Btype%40asset%2Bblock/Rowland2014-meta-analysis.pdf)
- Adesope, Trevisan & Sundararajan (2017). Rethinking the use of tests: a meta-analysis of practice testing. *Review of Educational Research* 87(3).
- Bertsch, Pesta, Wiscott & McDaniel (2007). The generation effect: a meta-analytic review. *Memory & Cognition* 35(2).
- Kornell, Hays & Bjork (2009). Unsuccessful retrieval attempts enhance subsequent learning. *JEP: LMC* 35(4). [PubMed](https://pubmed.ncbi.nlm.nih.gov/19586265/)
- Richland, Kornell & Kao (2009). The pretesting effect. *JEP: Applied* 15(3). [PDF](https://learninglab.uchicago.edu/Pre-Testing_files/RichlandKornellKao.pdf)
- St. Hilaire, Chan & Ahn (2024). A meta-analysis of prequestion effects. *Psychonomic Bulletin & Review* 31. [PDF](https://par.nsf.gov/servlets/purl/10511812)
- Pan & Carpenter (2023). Prequestioning and pretesting effects: a review. *Educational Psychology Review* 35. [Article](https://link.springer.com/article/10.1007/s10648-023-09814-5)
- Butterfield & Metcalfe (2001). Errors committed with high confidence are hypercorrected. *JEP: LMC* 27(6). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4084803)
- Karpicke, Butler & Roediger (2009). Metacognitive strategies in student learning. *Memory* 17(4).
- Kornell & Bjork (2008). Learning concepts and categories: is spacing the "enemy of induction"? *Psychological Science* 19(6). [PDF](https://www.gwern.net/docs/spaced-repetition/2008-kornell.pdf)
- Soderstrom & Bjork (2015). Learning versus performance: an integrative review. *Perspectives on Psychological Science* 10(2).

**Interleaving**
- Brunmair & Richter (2019). Similarity matters: a meta-analysis of interleaved learning and its moderators. *Psychological Bulletin* 145(11). [PDF](https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf)
- Nakata & Suzuki (2019). Mixing grammar exercises facilitates long-term retention. *Modern Language Journal* 103(3). [ERIC](https://eric.ed.gov/?id=EJ1225042)
- Pan, Tajran, Lovelett, Osuna & Rickard (2019). Does interleaved practice enhance foreign language learning? *Journal of Educational Psychology* 111(7).

**Feedback**
- Wisniewski, Zierer & Hattie (2020). The power of feedback revisited. *Frontiers in Psychology* 10. [Article](https://www.frontiersin.org/articles/10.3389/fpsyg.2019.03087/full)
- Kluger & DeNisi (1996). The effects of feedback interventions on performance. *Psychological Bulletin* 119(2). [Record](https://cris.huji.ac.il/en/publications/the-effects-of-feedback-interventions-on-performance-a-historical/)
- Hattie & Timperley (2007). The power of feedback. *Review of Educational Research* 77(1). [PDF](https://www.uky.edu/~gmswan3/575/Hattie_Timperly_2007.pdf)
- Kulik & Kulik (1988). Timing of feedback and verbal learning. *Review of Educational Research* 58(1).
- Butler, Karpicke & Roediger (2007). The effect of type and timing of feedback on learning from multiple-choice tests. *JEP: Applied* 13(4).
- Li, Zhu & Ellis (2016). The effects of the timing of corrective feedback on the acquisition of a new linguistic structure. *Modern Language Journal* 100(1).
- Li (2020). What is the ideal time to provide corrective feedback? *Language Teaching* 53(1). [Article](https://www.cambridge.org/core/journals/language-teaching/article/what-is-the-ideal-time-to-provide-corrective-feedback-replication-of-li-zhu-ellis-2016-and-arroyo-yilmaz-2018/61CDB7D7788B67238254362D7C69F798)
- Li, Ou & Lee (2026). The timing of corrective feedback in second language learning. *Language Teaching* 59(1). [Article](https://www.cambridge.org/core/journals/language-teaching/article/timing-of-corrective-feedback-in-second-language-learning/0E8856852D0183E9DD91EDB4C249E245)

**Personalization, curiosity and humor**
- Symons & Johnson (1997). The self-reference effect in memory: a meta-analysis. *Psychological Bulletin* 121(3). Effect size from a secondary summary.
- Gruber, Gelman & Ranganath (2014). States of curiosity modulate hippocampus-dependent learning via the dopaminergic circuit. *Neuron* 84(2). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4252494/)
- Johns, Dye & Jones (2016). The influence of contextual diversity on word learning. *Psychonomic Bulletin & Review* 23(4). [Article](https://link.springer.com/article/10.3758/s13423-015-0980-7)
- Pagán & Nation (2019). Learning words via reading: contextual diversity, spacing, and retrieval effects in adults. *Cognitive Science* 43(1).
- Schmidt, S. R. (1994). Effects of humor on sentence memory. *JEP: LMC* 20(4).
- Banas, Dunbar, Rodriguez & Liu (2011). A review of humor in educational settings. *Communication Education* 60(1).

**Cognitive load, listening and speaking**
- Leahy & Sweller (2011). Cognitive load theory, modality of presentation and the transient information effect. *Applied Cognitive Psychology* 25; and Leahy & Sweller (2016), *Instructional Science* 44(1). [Record](https://researchers.mq.edu.au/en/publications/cognitive-load-theory-and-the-effects-of-transient-information-on/)
- Mayer & Pilegard (2014). Principles for managing essential processing. *Cambridge Handbook of Multimedia Learning*, 2nd ed.
- Sundararajan & Adesope (2020). Keep it coherent: a meta-analysis of the seductive details effect. *Educational Psychology Review* 32(3); Rey (2012), *Educational Research Review* 7. Numbers via a [secondary summary](https://inspire.acu.edu.au/articles/seductive-details).
- Kalyuga, Ayres, Chandler & Sweller (2003). The expertise reversal effect. *Educational Psychologist* 38(1).
- Montero Perez, Van Den Noortgate & Desmet (2013). Captioned video for L2 listening and vocabulary learning: a meta-analysis. *System* 41(3). Vocabulary figure via secondary source.
- Yanagisawa, Webb & Uchihara (2020). How do different forms of glossing contribute to L2 vocabulary learning from reading? A meta-regression analysis. *Studies in Second Language Acquisition*. [Article](https://www.cambridge.org/core/product/38124150D59DF3039EE1FF5AE88FE922)
- Griffiths (1992). Speech rate and listening comprehension. *TESOL Quarterly* 26(2).
- Kormos (2006). *Speech Production and Second Language Acquisition*. Erlbaum. Skehan (2009). Modelling second language performance. *Applied Linguistics* 30(4).
- Ellis (2009). The differential effects of three types of task planning. *Applied Linguistics* 30(4). [Abstract](https://academic.oup.com/applij/article-abstract/30/4/474/165606)
- Johnson & Abdi Tabari (2022). Task planning and oral L2 production: a research synthesis and meta-analysis. *Applied Linguistics*. doi:10.1093/applin/amac026

**Transfer and skill**
- DeKeyser (1997). Beyond explicit rule learning: automatizing second language morphosyntax. *Studies in Second Language Acquisition* 19(2). [Abstract](https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/abs/beyond-explicit-rule-learning/B71581638BF89873F61F03EA1E747E5A)
- Morris, Bransford & Franks (1977). Levels of processing versus transfer appropriate processing. *JVLVB* 16. Lightbown (2008). Transfer appropriate processing as a model for classroom second language acquisition.
- Barnett & Ceci (2002). When and where do we apply what we learn? *Psychological Bulletin* 128(4).
- Bygate (2001). Effects of task repetition on the structure and control of oral language. In *Researching Pedagogic Tasks*.
- Abdi Tabari, Zhuang & Farahanynia (2025). Task repetition and L2 oral performance: a meta-analysis. *System* 135. [Record](https://hilpub.uni-hildesheim.de/handle/ubhi/19120)
- Sheppard & Ellis (2018). In Bygate (ed.), *Learning Language through Task Repetition*. [Chapter](https://benjamins.com/catalog/tblt.11.07she)

**Tutoring and AI tutors**
- Bloom (1984). The 2 sigma problem. *Educational Researcher* 13(6). [PDF](https://www.gwern.net/doc/psychology/1984-bloom.pdf)
- Kulik, Kulik & Bangert-Drowns (1990). Effectiveness of mastery learning programs. *Review of Educational Research* 60(2).
- VanLehn (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist* 46(4).
- Chi, Siler, Jeong, Yamauchi & Hausmann (2001). Learning from human tutoring. *Cognitive Science* 25. [PDF](https://education.asu.edu/sites/default/files/lcl/image3_2.pdf)
- Chi & Wylie (2014). The ICAP framework. *Educational Psychologist* 49(4). [PDF](https://csi.asu.edu/wp-content/uploads/2018/01/ChiWylie2014ICAP.pdf)
- Lepper & Woolverton (2002). The wisdom of practice: lessons learned from the study of highly effective tutors. Via the [INSPIRE guidelines](https://www.eoas.ubc.ca/research/cwsei/resources/INSPIRE-Guidelines.pdf)
- Bastani et al. (2025). Generative AI without guardrails can harm learning. *PNAS* 122(26). [Record](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html)
- Fan et al. (2025). Beware of metacognitive laziness. *British Journal of Educational Technology* 56(2). [arXiv](https://arxiv.org/abs/2412.09315v1)
