# For one: the language acquisition lens

> Live doc: https://claude.ai/code/artifact/b1fb6113-b6d2-44d0-878b-ff6c01c09ff1 (this file is a markdown export of it, 2026-10-09). One of eleven lens perspectives on For one; builds on the first rethink at https://claude.ai/code/artifact/21c354e1-9b24-4fcd-bb44-dca39f26d86b.


Oct 9, 2026 · @Muath

## Decisions, settled

Muath settled all four on 2026-10-23 and chose the recommended option each time: A, the session is the centre of a bigger listening routine; B, the host may ask "sorry, you what?"; C, listening is audio-first; D, light pronunciation help without scores in v1. The rest of this doc assumes these. Decision B narrows the first rethink's correction decision rather than adding a new one.

| # | Decision | Recommended | Alternative | Why it matters |
| --- | --- | --- | --- | --- |
| A | Is a session the whole daily dose, or the hub of a bigger listening diet? | Hub. Keep the cap on new episodes, but make re-listening, the archive and a private podcast feed unlimited | The session is the whole thing | As specified, one session a day gives about 64 hours of input a year. Your own hour gave about 274. Hours are the dose. |
| B | Can the host "not understand" you? | Yes. A natural "sorry, you what?" is the host's first correction move, before any recast | Recast-only | Clarification requests got 88% uptake versus 31% for recasts in the classic classroom study, and they are the most socially natural correction there is. |
| C | Audio-first or transcript-first listening? | Audio-first: the first play has the transcript folded, one tap to open it, plus a "missed that" replay | Transcript always visible (current PRD) | An always-on transcript turns listening into reading. Intermediate listeners mostly fail at hearing words they already know. |
| D | Pronunciation in v1? | Comprehensibility only: tap-to-hear any word, shadow a line or two, the host asks when it truly cannot catch a word. No scores | Fully out of scope (current PRD) | Pronunciation teaching works (d = 0.89), and ear training carries over to speech. Being understood is a real-world goal the show ignores today. |

A is the most consequential: it decides whether For one can deliver enough hours to make anyone fluent.

## The short version

The SLA research backs the core of For one more than the first rethink gave it credit for. Personal topics improve comprehension, not just motivation. Reading the article before the call is textbook pre-task planning, which reliably makes speech more fluent and complex. Text chat transfers to speaking.

The two biggest problems are not correction style or the order of stages. First, the dose: the product as specified delivers about a quarter of the input your own hour delivered, and input hours are the strongest predictor of where a learner ends up. Second, the call is designed as a free debate. In free conversation learners steer around what they cannot say, so planned targets rarely get practised, and the host's only correction move, the recast, is the easiest one to miss.

The fix keeps the vision. Spend the expensive live minutes on what only an AI teacher can do: interaction that pushes the learner, and feedback they notice. Spend the cheap minutes on input volume: re-listening, the archive, a private feed. Then teach listening itself, not only expose people to it.

Evidence labels used below: **Strong** = several meta-analyses agree. **Moderate** = one meta-analysis or several consistent studies. **Weak** = single studies, surveys or practitioner reports. **My judgment** = my inference, not the literature's.

## The evidence, mechanism by mechanism

Eleven mechanisms, each with what the research says and how strong it is. Product consequences are collected in the last two sections.

### 1. Input: necessary, and the amount is what matters

- **Input drives acquisition, mostly implicitly.** A 40-year review concludes Krashen's core claims survive in modern form: acquisition is largely implicit and input-driven and explicit knowledge plays a limited role, though "i+1" was never testable as stated ([Lichtman & VanPatten 2021](https://doi.org/10.1111/flan.12552); McLaughlin 1987 on testability). **Moderate** (a review, by input-leaning researchers).
- **Reading volume works.** Extensive reading meta-analyses: d = 0.46 between groups across 34 studies ([Nakanishi 2015](https://doi.org/10.1002/tesq.157)); d ≈ 0.57 across 49 studies, larger for adults and longer programmes ([Jeon & Day 2016](https://nflrc.hawaii.edu/rfl/item/341)). **Strong.**
- **The amount needed is large.** The US Foreign Service Institute plans 600 to 750 class hours for Spanish or French and 2,200 for Arabic, Chinese, Japanese or Korean to reach professional proficiency, full time with homework ([FSI](https://www.state.gov/foreign-language-training/)). Dreaming Spanish's roadmap puts level 5 at 600 hours and level 7 at 1,500 hours of input for an English speaker, doubled for distant languages ([community copy of the roadmap](https://r.datuan.dev/r/dreaminglanguages/wiki/index)). **Weak as precise numbers, strong as an order of magnitude.**
- **Out-of-class exposure predicts outcomes.** Time with TV and films (without subtitles), the internet, reading and games predicted vocabulary more than years of instruction did ([Peters 2018](https://doi.org/10.1075/itl.00010.pet)); among 1,069 Swedish teens, gaming time predicted vocabulary ([Sundqvist 2019](https://www.lltjournal.org/item-detail/903/)). **Moderate, correlational.**

### 2. Listening has to be taught, not only done

- **Intermediate listeners fail at decoding.** The most common problems are perceptual: "I don't recognise words I know", "I miss the next part while thinking about this one" ([Goh 2000](<https://doi.org/10.1016/S0346-251X(99)00060-3>)). Field argues most listening teaching tests comprehension instead of training word recognition in connected speech ([Field 2008](https://doi.org/10.1017/CBO9780511575945)). **Moderate.**
- **Teaching listening works.** Strategy instruction has a medium effect on listening comprehension, d = 0.69 across 45 studies ([Dalman & Plonsky](https://doi.org/10.1177/13621688211072981)); less-skilled listeners gained most in [Vandergrift & Tafaghodtari 2010](https://doi.org/10.1111/j.1467-9922.2009.00559.x). **Moderate to strong.**
- **Knowing the topic and hearing it again both help.** Of four listening supports, topic preparation helped most and repetition came second; pre-teaching vocabulary helped least ([Chang & Read 2006](https://nccur.lib.nccu.edu.tw/handle/140.119/60028)). Narrow listening (many short recordings on one familiar topic) beat a control group, +18.7 versus +7.4 points, with transfer to new topics ([Yến & Waring 2022](https://www.culi.chula.ac.th/Images/asset/pasaa_journal/file-2-23-9jdhtg698061.pdf)); earlier support was self-report ([Krashen 1996](<https://doi.org/10.1016/0346-251X(95)00054-N>); [Dupuy 1999](<https://doi.org/10.1016/S0346-251X(99)00030-5>)). **Moderate.**
- **Reading while listening builds listening fluency.** Learners who read with audio made the most consistent listening-fluency gains, ahead of reading-only and listening-only groups ([Chang & Millett 2014](https://doi.org/10.1093/elt/cct052)). **Moderate.** The tension: the transcript helps vocabulary and fluency, and the bare audio trains decoding. A product needs both, in that order.

### 3. Personalization helps comprehension, not only motivation

- Familiar topics produced significantly better listening recall at every course level ([Schmidt-Rinehart 1994](https://doi.org/10.1111/j.1540-4781.1994.tb02030.x)); topic familiarity also helped readers process grammatical form (Leeser 2007). **Moderate** (robust effect, no meta-analysis found).
- **My judgment:** this is a learning argument for For one's core idea that the first rethink did not make. When the topic is your team or your job, less attention goes to working out what is happening and more is left for the language.
- **The risk is narrowing.** Language processing is tuned to frequency ([N. Ellis 2002](https://doi.org/10.1017/S0272263102002024)). A show built only around football will over-teach football words and under-teach the high-frequency language every situation needs. **My judgment** on the risk; strong evidence on frequency.

### 4. Output: speaking is how learners find the gaps

- **Output has three jobs:** you notice what you cannot say, you test guesses, and you reflect on form. Swain built this from immersion students who had years of input but kept non-target grammar (Swain 1985, 1995). **Moderate, foundational.**
- **Practice is skill-specific.** In an 8-week study, comprehension practice improved comprehension and production practice improved production, with gains following a power-law curve ([DeKeyser 1997](https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/abs/beyond-explicit-rule-learning/B71581638BF89873F61F03EA1E747E5A)); classroom versions of this are messier and depend on the structure (DeKeyser & Sokalski 1996). Comprehension-based instruction was better on immediate receptive tests and production-based instruction on delayed productive tests ([Shintani, Li & Ellis 2013](https://doi.org/10.1111/lang.12001)). **Strong.**
- **Free conversation rarely forces a structure.** In production tasks a structure is at best useful, almost never essential, because speakers can talk around it (Loschky & Bley-Vroman 1993). **Moderate,** theoretical but widely accepted. This is the hidden weak point of "threading 1 to 2 invisible targets" into a debate call.
- **Productive vocabulary needs production.** Writing with new words built more productive knowledge than reading them ([Webb 2005](https://doi.org/10.1017/S0272263105050023)); active recall is the hardest level of word knowledge (Laufer & Goldstein 2004). **Moderate.**

### 5. Interaction: the call is the strongest part of the design

- **Conversation with feedback works.** Interaction gave d = 0.71 immediately and 1.09 at delayed tests across 28 studies ([Mackey & Goo 2007](https://www.researchgate.net/publication/284789919), figures as quoted by Lyster & Saito 2010); a later review finds "a robust connection between interaction and learning" ([Loewen & Sato 2018](https://doi.org/10.1017/S0261444818000125)). **Strong.**
- **Task-based programmes beat comparisons,** d = 0.93 across 52 studies ([Bryfonski & McKay 2019](https://doi.org/10.1177/1362168817744389)). **Contested:** later reviews say the field is not yet ready for a reliable overall estimate, and a reanalysis found a smaller positive effect ([Boers & Faez 2023](https://doi.org/10.1177/13621688231167573)).
- **Planning improves the talk.** Pre-task planning reliably improves fluency and usually complexity; accuracy is mixed ([Ellis 2009](https://doi.org/10.1093/applin/amp042); [Yuan & Ellis 2003](https://doi.org/10.1093/applin/24.1.1)). The article before the call is exactly this. **Strong.**
- **Repeating a task improves it.** A 2025 meta-analysis of oral task repetition found large effects on complexity and accuracy and smaller ones on fluency, with longer gaps between repetitions giving smaller effects ([Abdi Tabari, Zhuang & Farahanynia 2025](https://doi.org/10.1016/j.system.2025.103868)). Repeating a talk on the same topic built fluency that carried over to new topics ([de Jong & Perfetti 2011](https://doi.org/10.1111/j.1467-9922.2010.00620.x)). **Moderate.** A next-day repeat is a short gap, which is the effective kind.

* **AI conversation partners work, with conditions.** Dialogue systems for learners: d = 0.58 across 17 studies, stronger for goal-oriented bots that give corrective feedback ([Bibauw et al. 2022](https://www.lltjournal.org/item-detail/1035)). AI chatbots improved speaking, g = 0.61 across 16 studies, with no effect on grammatical accuracy; multimodal bots did best and voice-only bots had only a small effect ([Hou & Min 2025](https://www.cambridge.org/core/product/31847710516602398819C5E594038E7B)). **Moderate.** The call needs goals, feedback and text support, not voice alone.
* **The call is generous by classroom standards.** Students speak roughly 20 to 25% of lesson time, shared by the whole class ([Rezaee & Farahian 2012](https://www.researchgate.net/figure/The-Percentage-of-Teacher-Talk-Student-Talk-and-Other-Activities-in-the-Total-Class-Time_tbl1_271889540); [English in Action 2010](https://assets.publishing.service.gov.uk/media/57a08ad9ed915d622c00093f/2a_the_classroom_practices-teachers_participating_in_english_in_action.pdf)). That is under half a minute per student per lesson, so a 4 to 5 minute call is about ten times a lesson's speaking turn. **My inference** from weak data. Volume still matters (section 4), but the call is not a token amount.

### 6. Corrective feedback: what kind, and for whom

- **Recasts are the most used and least noticed in classrooms.** In immersion classrooms, recasts were 55% of all feedback but led to uptake 31% of the time and repair 18%. Elicitation got 100% uptake, clarification requests 88%, metalinguistic clues 86% ([Lyster & Ranta 1997](https://doi.org/10.1017/S0272263197001034)). **Strong** (a replicated pattern; uptake is not the same as learning).
- **Prompts beat recasts in classrooms.** Feedback had significant, durable effects (d = 0.74), larger for prompts (0.83) than recasts (0.53), and larger for younger learners ([Lyster & Saito 2010](https://doi.org/10.1017/S0272263109990520)). Explicit feedback was larger at first and implicit feedback held up better at long delay, though the differences were not significant ([Li 2010](https://doi.org/10.1111/j.1467-9922.2010.00561.x)). **Strong in direction, contested in degree** ([Goo & Mackey 2013](https://doi.org/10.1017/S0272263112000708)).
- **One-on-one is different, in recasts' favour.** Feedback effects were about twice as large in lab studies, which are mostly one-on-one, as in classrooms (d = 1.09 versus 0.47; Li 2010), and recasts did well in interaction studies (d = 0.96; Mackey & Goo 2007). **Moderate.** **My judgment:** an AI call is one-on-one, so recasts will work better there than classroom figures suggest. The case for clarification requests is to add a move, not to drop recasts.
- **How a recast is said matters.** Short, partial recasts with one change, stress on the corrected part and declarative intonation get more uptake and repair ([Sheen 2006](https://doi.org/10.1191/1362168806lr203oa); [Loewen & Philp 2006](https://doi.org/10.1111/j.1540-4781.2006.00465.x)). **Moderate.**
- **Anxiety changes which feedback works.** High-anxiety learners did not benefit from recasts in one study ([Sheen 2008](https://doi.org/10.1111/j.1467-9922.2008.00480.x)), while in another they did better with recasts than with metalinguistic feedback, which suited low-anxiety learners ([Rassaei 2015](https://doi.org/10.1016/j.system.2015.01.002)). **Weak and mixed**, but both say feedback should adapt to the person. Anxiety correlates with lower achievement, r = −.36 across 19,933 learners ([Teimouri, Goetze & Plonsky 2019](https://doi.org/10.1017/S0272263118000311)). **Strong.** I found no study showing feedback itself raises anxiety.
- **Learners want correction.** 90% of students wanted spoken errors corrected, while 70% of their teachers did not see this as important ([Schulz 1996](https://doi.org/10.1111/j.1944-9720.1996.tb01247.x); [Schulz 2001](https://doi.org/10.1111/0026-7902.00107), figures via Kartchava 2016). **Moderate** (stated preference, not effect).
- **Written correction in chat is effective,** d ≈ 0.68 ([Kang & Han 2015](https://doi.org/10.1111/modl.12189), figure via a secondary source). **Strong.**

### 7. Noticing, and why highlighting is not the answer

- Schmidt's noticing hypothesis says form must be consciously registered to be learned ([Schmidt 1990](https://doi.org/10.1093/applin/11.2.129)); the strong version is contested. **Moderate.**
- Making forms visually salient (bold, colour) has a small effect on grammar, d = 0.22, and slightly hurts comprehension, d ≈ −0.26 ([Lee & Huang 2008](https://doi.org/10.1017/S0272263108080479)). **Moderate.** Noticing should come from feedback and from the learner's own output gaps, not from highlighting the transcript.

### 8. Skills transfer, partly

- **Text chat builds speaking.** Learners in chat-based sections gained more oral proficiency than face-to-face groups ([Payne & Whitney 2002](https://doi.org/10.1558/cj.v20i1.7-32)), and a meta-analysis found chat and face-to-face interaction equally effective ([Ziegler 2016](https://doi.org/10.1017/S027226311500025X)). **Moderate.** The chat stage is slow-motion speaking with time to notice, not a lesser stage.
- **Listening does not build speaking fluency on its own** (skill-specific practice, section 4), and in a 2026 conference meta-analysis of 67 chatbot studies, effects were about 2.5 times larger when the practice and the test used the same mode. **Strong.**

### 9. Vocabulary: what a podcast does and doesn't teach

- **Listening alone teaches word meanings slowly.** Reading beat listening for incidental vocabulary at every level, with the gap narrowing as proficiency rose ([Vidal 2011](https://doi.org/10.1111/j.1467-9922.2010.00593.x)). In one study, listening alone taught the meaning of 2% of new words, against 15% for reading and 16% for reading while listening ([Brown, Waring & Donkaewbua 2008](https://www2.hawaii.edu/~readfl/rfl/October2008/brown/brown.html)); in another, meaning recall from listening was 8.5% even after up to 15 encounters ([van Zeeland & Schmitt 2013](https://doi.org/10.1016/j.system.2013.07.012)). A pooled analysis is kinder, with listening (15% of words) close to reading (17%) ([Webb, Uchihara & Yanagisawa 2023](https://doi.org/10.1017/S0261444822000507)). **Moderate.** The transcript and article matter for vocabulary.
- Encounters matter but are not enough: r = .34 between number of encounters and learning, with no magic number ([Uchihara, Webb & Yanagisawa 2019](https://doi.org/10.1111/lang.12343)); even 10 encounters did not give full knowledge ([Webb 2007](https://doi.org/10.1093/applin/aml048)). **Strong.**
- Spacing beats massing with a medium-to-large effect across 48 experiments, and longer spacing wins on delayed tests ([Kim & Webb 2022](https://doi.org/10.1111/lang.12479)). Five retrievals in a session beat one or three, though one is the most efficient per minute ([Nakata 2017](https://doi.org/10.1017/S0272263116000280)). **Strong.**
- Glosses help: 45% of glossed words learned against 27% unglossed, and native-language glosses beat target-language ones ([Yanagisawa, Webb & Uchihara 2020](https://doi.org/10.1017/S0272263119000688)). **Strong.** This backs tap-to-define in the native language.
- **Chunks make people sound fluent.** Learners taught to notice formulaic sequences were rated more proficient by blind judges ([Boers et al. 2006](https://doi.org/10.1191/1362168806lr195oa)); collocations are picked up from reading while listening with enough encounters ([Webb, Newton & Chang 2013](https://doi.org/10.1111/j.1467-9922.2012.00729.x)), and explicit collocation teaching beat implicit across 17 studies ([Li & Lei 2022](https://doi.org/10.1515/iral-2021-0218)). **Moderate.**

### 10. Pronunciation and perception

- Pronunciation instruction has a large effect, d = 0.89 across 86 studies ([Lee, Jang & Plonsky 2015](https://doi.org/10.1093/applin/amu040)), but the evidence is much less clear in spontaneous speech than in controlled tasks ([Saito & Plonsky 2019](https://doi.org/10.1111/lang.12345)). **Strong.**
- A strong accent does not necessarily make speech hard to understand; accent, comprehensibility and intelligibility are partly independent ([Munro & Derwing 1995](https://doi.org/10.1111/j.1467-1770.1995.tb00963.x)). **Strong.** Aim at being understood, not at sounding native.
- Training the ear helps the mouth, partly. Perception training gave d = 0.92 for perception and d = 0.54 for production ([Sakai & Moorman 2018](https://doi.org/10.1017/S0142716417000418)). Across 79 high-variability studies (many voices, identify-the-sound tasks), the gain against controls was g = 0.67, plateauing around 400 minutes of training with about six voices ([Uchihara, Karas & Thomson 2025](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6ABB8C1F32D88D53EA8D05A4565E76F6/S0272263125100879a.pdf/high-variability-phonetic-training-hvpt-a-meta-analysis-of-l2-perceptual-training-studies.pdf)); production gains were smaller and weakly tied to perception gains ([Uchihara, Karas & Thomson 2024](https://www.cambridge.org/core/product/E38D8F5CE65DC708137B0E95F97C6BC7)). **Strong.**
- Shadowing (repeating audio just behind the speaker) helped lower-level learners' listening and sound perception ([Hamada 2016](https://doi.org/10.1177/1362168815597504)). A 2024 systematic review of 44 studies found benefits for comprehensibility, intelligibility and fluency, mostly on controlled tasks ([Whitworth 2024](https://ora.ox.ac.uk/ark:/29072/ora_3104cae13a6b400ab173de44384238d2)). **Weak to moderate:** no meta-analysis, mostly small Japanese EFL studies, and some null results.

### 11. Measuring progress without tests

- Speed of speech best reflects underlying language knowledge, while pause length is only weakly related ([de Jong et al. 2013](https://dare.uva.nl/id/a6d0ce87-9e8a-4f40-9c3d-8a002907c794)). Across 22 studies, speech rate correlated r = .76 with how fluent listeners judged speech, mid-clause pauses r = −.72, and repairs only r = −.20 (Suzuki, Kormos & Uchihara 2021, as reported in [Takizawa & Suzuki 2025](https://www.cambridge.org/core/product/FAB18835B2117A299C33F8F502248C81)). **Moderate.** The PRD's fluency measures are on the right track; weight speech rate and mid-clause pauses, and drop repair counts.
- Repeating sentences of increasing length (elicited imitation) separates proficiency levels well, g = 1.34 ([Yan et al. 2016](https://doi.org/10.1177/0265532215594643)), and correlates r = .66 with proficiency across 46 reports ([Kostromitina & Plonsky 2022](https://experts.nau.edu/en/publications/elicited-imitation-tasks-as-a-measure-of-l2-proficiency/)). **Moderate.** **My judgment:** shadowing a line from your own episode is the same act, so it can double as a hidden speaking check without becoming a test.

## Does the 30/15/5/10 hour hold up?

Mostly yes on the shape, and the bigger lesson is the size. Your hour is 45 minutes of input, 15 of output (5 speaking, 10 writing), and no deliberate focus-on-form or fluency time.

**What holds up**

- **The input share.** Input-heavy learning is where the comprehensible-input research, the extensive reading meta-analyses and the immersion communities all converge. **Strong.**
- **Writing counted as output.** If your writing was conversational, chat-style writing transfers to speaking (Payne & Whitney; Ziegler), so your real output share was closer to 25%. That matches the meaning-focused output share in Nation's Four Strands ([Nation 2007](https://doi.org/10.2167/illt039.0)). **My inference.**
- **Every day, at a fixed time.** Spaced practice beats massed practice for retention (Kim & Webb 2022), and a fixed daily slot is how habits form. But the timing research does not show short daily sessions beat longer ones: the most intensive schedule did best for a 110-hour adult course ([Serrano & Muñoz 2007](https://diposit.ub.edu/dspace/handle/2445/164086)), and 1-day and 7-day spacing gave similar speaking-fluency gains ([Kakitani & Kormos 2024](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4F6787916C198376CAD222934D3B37E4/S0272263124000251a.pdf/the-effects-of-distributed-practice-on-second-language-fluency-development.pdf)). Daily is justified by habit, not by a timing advantage. **Moderate.**

**What doesn't**

- **Five minutes of speaking is too little** to build speaking fluency, because practice is skill-specific (DeKeyser 1997; Shintani et al. 2013). **Strong.**
- **There is no feedback slot.** Input alone produced fluent but inaccurate speakers in Canadian immersion (Swain). Your hour likely worked because correction came from somewhere else. **My inference.**
- **There is no fluency strand** (fast retelling, re-listening easy material) and no focus-on-form time. Nation suggests roughly a quarter each. **Moderate:** the equal split is principled guidance, never tested as a ratio.

**The bigger lesson is the dose.** Your hour delivers about 274 hours of input a year. For one as specified delivers far less:

| Pattern | Input min per day | Input hours per year | Years to 600 hours |
| --- | --- | --- | --- |
| Your hour, daily | 45 | \~274 | \~2.2 |
| For one, 2 sessions every day (the cap) | \~21 | \~128 | \~4.7 |
| For one, 1 session every day | \~10.5 | \~64 | \~9.4 |
| For one, 4 sessions a week (the PRD's success target) | \~6 | \~36 | \~16.5 |

Assumes about 7 minutes of episode plus 3.5 minutes of article per session. 600 hours is Dreaming Spanish's level 5 and the low end of FSI's estimate for Spanish. **My arithmetic.**

**My suggested hour.** I agree with the first rethink's stage-by-stage table for the session itself. The new point is where the minutes come from. Live AI minutes are expensive and only they give interaction and feedback; listening minutes are nearly free once an episode exists. For an intermediate learner with an hour:

- **20 to 30 min listening, anywhere:** today's episode, then yesterday's again, then archive episodes chosen for their target words. Cheap, mostly away from the screen.
- **10 min reading:** the article, with audio when wanted.
- **10 to 12 min live call:** the push, the feedback, one quick retell.
- **5 min chat:** focused written correction.
- **5 min focus:** the polish card, two shadowed lines, words due for recall.

The product should own this mix and shift it by stage and by goal. Someone preparing for a job interview needs more call minutes than someone who wants to watch films.

## What polyglots and immersion learners actually do

Successful self-directed learners converge on five habits; For one already has the hardest one (personal input) and lacks volume and recall. The evidence here is practitioner reports and correlational data, not controlled studies, and it suffers from survivorship bias: we hear from those who succeeded.

| Habit | Who does it | What For one has today | Gap |
| --- | --- | --- | --- |
| Huge volume of enjoyable input they chose | Dreaming Spanish, LingQ, Refold; the hyperpolyglots in Erard's Babel No More (2012) | The best-personalised input there is | Volume (see the dose table) |
| Counting hours or known words as progress | Dreaming Spanish hours, LingQ known-word counts | Nothing visible, by law | The first rethink's "honest progress" decision covers it |
| Saving sentences from their own input into spaced review | Anki-based self-learners (practitioner reports, no study found) | Tap-to-define logs every word tapped | Nothing turns those taps into recall (change 12) |
| Shadowing | Self-learners; Japanese EFL classrooms | None | Line shadowing (change 8) |
| Talking to real people after a listening phase, then reviewing mistakes | [Refold's roadmap](https://refold.la/roadmap/stage-0/a/roadmap-overview) puts speaking in phase 4; [Steve Kaufmann](https://www.lingq.com/en/learn-english-online/courses/135380/how-to-start-talking-in-a-new-languag-6755385/) reviews the 10 to 20 words he misused after each tutor session | The call; "life is the game" | Kaufmann's habit is the polish card. Human bridges later (first rethink) |

Two claims from this world are not supported. The Automatic Language Growth claim that speaking early causes lasting errors rests on its founder's own observations at a Bangkok language school, with no peer-reviewed test ([J. Marvin Brown](https://en.wikipedia.org/wiki/J._Marvin_Brown)), and evidence for a "silent period" comes almost entirely from children. Meanwhile production practice helps production (section 4). For the intermediate learner For one targets, delaying speech has no basis. For true beginners, listening first is reasonable.

## What the concept gets right, contradicts, and misses

Most of the design is supported; five rules in the PRD run against the evidence, and seven things are missing.

**Supported by the evidence**

- An input-first show (section 1).
- Personal topics, which help comprehension as well as motivation (section 3).
- Read before Speak, which is pre-task planning (section 5). This argues for keeping that order as the default even inside the first rethink's "many doors".
- A live call with a host who takes positions and pushes back (section 5).
- The chat stage, which transfers to speaking and suits written correction (sections 6 and 8).
- Native-language tap-to-define (section 9).
- The target lifecycle with re-checks at 2, 4 and 8 weeks, which is expanding spacing (section 9).
- The readiness rule, the error-versus-slip rule, and assessment from natural speech (section 11).
- No typographic highlighting of targets (section 7).
- Killing anxiety as a design goal (section 6).

**Contradicted by the evidence**

- Recast-only correction (PRD 1.2 law 5, 10.11), especially for anxious learners, who are the users For one wants (section 6).
- Transcript always visible (PRD 5.1), which removes decoding practice (section 2).
- No audio in tap-to-define, and pronunciation out of scope (PRD 5.5, 16) (section 10).
- The 2-session cap and 8-minute ceiling capping input, not just generation (PRD 1.3, 5.1) (section 1 and the dose table).
- "Used once" applied to listening. Re-listening the same episode is one of the best listening supports (section 2). The first rethink already said words must recur; the episode itself should too.

**Missing**

- Moments in the call that make targets necessary (section 4).
- Listening skill training (section 2).
- Productive vocabulary elicitation (section 4).
- Chunks as a unit of the learner file (section 9).
- A guardrail against topic-narrowed vocabulary (section 3).
- Task repetition (section 5).
- Perception and comprehensibility (section 10).

## Product changes

Fourteen changes, each naming the PRD part it touches and the evidence behind it. Changes already in the first rethink (coverage check, spaced word recycling, polish card, retell, 0.75x speed, outcome sample) are not repeated.

1. **The host negotiates meaning first** (PRD 5.3, 10.11; Law 7). When an error blocks or blurs meaning, the host's first move is a real clarification request: "Wait, you *go*, or you *went*?" or "Sorry, thirty or thirteen?" Only then a recast. Clarification requests fit "socially natural" better than recasts, because real people ask them. Evidence: Lyster & Ranta 1997; Lyster & Saito 2010.
2. **Recasts are built to be heard** (PRD 10.11). One change, short, partial where possible, the corrected word stressed in the synthesized voice. Evidence: Sheen 2006; Loewen & Philp 2006.
3. **Feedback adapts to anxiety** (PRD 10.9 energy state). When signals suggest anxiety (very short turns, long silences, abandoned calls), the host drops prompts, keeps clear recasts, and moves correction to the written polish card. When the learner is confident, it prompts more. Evidence: Sheen 2008; Teimouri et al. 2019.
4. **The call brief engineers need, not just chances** (PRD 9 step 3, 5.3). For each target, the Writer plans one or two host moves that make the structure close to essential: "Walk me through what happened" for past tense, "If you were the coach…" for conditionals, "Which is worse…" for comparatives. For each due word, one move that creates a need for it. Evidence: Loschky & Bley-Vroman 1993; Webb 2005.
5. **Audio-first listening with a "missed that" button** (PRD 5.1). The first play shows the transcript folded. "Missed that" replays the last sentence, then shows it, then plays it at 0.75x. Every replayed line is logged as a decoding signal for the planner. Evidence: Field 2008; Goh 2000; Dalman & Plonsky.
6. **Listening is uncapped; generation is capped** (PRD 1.3, 12.1, 16). Keep the 2-new-episodes cap for cost. Make the archive a listening library, offer "yesterday's episode again" as a free second listen, and deliver episodes to a private podcast feed. Optionally run 2 or 3 episodes in a row on one topic area (narrow listening) when the learner wants depth. Topic threads are not plot, so Law 4 holds. Evidence: Chang & Read 2006; Krashen 1996; the dose table.
7. **Round two** (PRD 4, 5.3). The next day, an optional two-minute call: "Saturday's settled. Give me your take again, faster." Same content, more fluent. Evidence: Bygate 2001; de Jong & Perfetti 2011.
8. **Hear any word, shadow any line** (PRD 5.5, 16). Tap-to-hear on every word and sentence. After the episode, an optional "say it with Karim" moment: two short lines from the episode to shadow. Shadowed lines double as an elicited-imitation signal for assessment. No scores shown. Evidence: Sakai & Moorman 2018; Hamada 2016; Yan et al. 2016.
9. **Comprehensibility, not accent** (PRD 10.4). Add intelligibility as a 13th error category, fed only by words the speech recognizer could not catch and the host had to ask about, so it tracks real communication breakdowns. Evidence: Munro & Derwing 1995; Saito & Plonsky 2019.
10. **Chunks in the learner file** (PRD 8 section 4). Track formulaic sequences ("to be honest", "make a decision", "it depends on") as their own ring, receptive and productive, threaded and recycled like words. Evidence: Boers et al. 2006; Webb, Newton & Chang 2013.
11. **A frequency floor on new vocabulary** (PRD 6.2, 9 step 3). Most new words a script plants must come from the top few thousand words of the language, not the topic's niche vocabulary. The wildcard pitch stays as a breadth tool. Evidence: N. Ellis 2002; Nation 2006.
12. **Turn taps into recall** (PRD 5.5, 9). Words tapped twice or more become recall targets: the host creates a need for them in the next call, and the polish card shows the sentence where the learner first met them. This is sentence mining without flashcards. Evidence: Kim & Webb 2022; Nakata 2017; Refold practice.
13. **Planning time when the article is skipped** (PRD 4 rule 4). If the learner goes straight from episode to call, the host gives 30 seconds: "Think about your side; here are three words you might want." Evidence: Ellis 2009; Yuan & Ellis 2003.
14. **Weight speech rate and mid-clause pauses in the fluency measure** (PRD 10.2), and drop repair counts, which say little. Evidence: de Jong et al. 2013; Suzuki, Kormos & Uchihara 2021.

## Notes for the synthesis

- Hou & Min 2025, cited in the [first rethink](https://claude.ai/code/artifact/21c354e1-9b24-4fcd-bb44-dca39f26d86b), is confirmed (ReCALL 38(1)). It adds that voice-only bots had only a small effect and grammar accuracy did not improve, which supports giving the call text support and feedback.
- The first rethink calls recasts the weakest correction type. That holds in classrooms; in one-on-one settings recasts do considerably better (section 6), so the honest claim is "add clarification requests", not "recasts fail".
- DeKeyser & Sokalski 1996 is weaker than it is often cited; DeKeyser 1997 is the clean skill-specificity result.
- Peters 2018's TV finding is for TV without subtitles.
- Some figures come from papers citing the original (Mackey & Goo, Schulz, Kang & Han, Suzuki et al. 2021); they are marked where used.
- I found no meta-analysis of shadowing or narrow listening, and no outcome study of Refold or similar communities.
- Markdown copy for the synthesis thread: /mnt/project-files/perspectives/language-acquisition.md

## Sources

Links were found and checked on 2026-10-09; DOIs are given where available. Leeser 2007, Laufer & Goldstein 2004, Lindgren & Muñoz 2013, Sundqvist 2009, Swain 1985/1995, Loschky & Bley-Vroman 1993, Bygate 1996/2001, DeKeyser 2007, Granger 2004, McLaughlin 1987 and Erard 2012 are cited without links because I could not confirm a stable page.

**Input, listening, reading**

- [Lichtman & VanPatten 2021, Was Krashen right?](https://doi.org/10.1111/flan.12552)
- [Nakanishi 2015, extensive reading meta-analysis](https://doi.org/10.1002/tesq.157)
- [Jeon & Day 2016, extensive reading meta-analysis](https://nflrc.hawaii.edu/rfl/item/341)
- [Goh 2000, listening comprehension problems](<https://doi.org/10.1016/S0346-251X(99)00060-3>)
- [Field 2008, Listening in the Language Classroom](https://doi.org/10.1017/CBO9780511575945)
- [Dalman & Plonsky, listening strategy instruction meta-analysis](https://doi.org/10.1177/13621688211072981)
- [Vandergrift & Tafaghodtari 2010](https://doi.org/10.1111/j.1467-9922.2009.00559.x)
- [Chang & Read 2006, listening support](https://nccur.lib.nccu.edu.tw/handle/140.119/60028)
- [Krashen 1996, narrow listening](<https://doi.org/10.1016/0346-251X(95)00054-N>)
- [Dupuy 1999, narrow listening](<https://doi.org/10.1016/S0346-251X(99)00030-5>)
- [Chang & Millett 2014, extensive listening](https://doi.org/10.1093/elt/cct052)
- [Schmidt-Rinehart 1994, topic familiarity](https://doi.org/10.1111/j.1540-4781.1994.tb02030.x)
- [N. Ellis 2002, frequency effects](https://doi.org/10.1017/S0272263102002024)
- [Nation 2006, vocabulary size for reading and listening](https://doi.org/10.3138/cmlr.63.1.59)

**Output, interaction, tasks, feedback**

- [DeKeyser & Sokalski 1996, skill-specific practice](https://doi.org/10.1111/j.1467-1770.1996.tb01354.x)
- [Shintani, Li & Ellis 2013, comprehension vs production instruction](https://doi.org/10.1111/lang.12001)
- [Webb 2005, receptive and productive vocabulary](https://doi.org/10.1017/S0272263105050023)
- [Mackey & Goo 2007, interaction meta-analysis](https://www.researchgate.net/publication/284789919)
- [Loewen & Sato 2018, interaction review](https://doi.org/10.1017/S0261444818000125)
- [Bryfonski & McKay 2019, TBLT meta-analysis](https://doi.org/10.1177/1362168817744389)
- [Ellis 2009, task planning](https://doi.org/10.1093/applin/amp042)
- [Yuan & Ellis 2003, pre-task and online planning](https://doi.org/10.1093/applin/24.1.1)
- [de Jong & Perfetti 2011, fluency through repetition](https://doi.org/10.1111/j.1467-9922.2010.00620.x)
- [Lyster & Ranta 1997, feedback and uptake](https://doi.org/10.1017/S0272263197001034)
- [Lyster & Saito 2010, oral feedback meta-analysis](https://doi.org/10.1017/S0272263109990520)
- [Li 2010, corrective feedback meta-analysis](https://doi.org/10.1111/j.1467-9922.2010.00561.x)
- [Goo & Mackey 2013, the case against the case against recasts](https://doi.org/10.1017/S0272263112000708)
- [Sheen 2006, recast characteristics](https://doi.org/10.1191/1362168806lr203oa)
- [Loewen & Philp 2006, recasts in adult ESL](https://doi.org/10.1111/j.1540-4781.2006.00465.x)
- [Sheen 2008, recasts and anxiety](https://doi.org/10.1111/j.1467-9922.2008.00480.x)
- [Teimouri, Goetze & Plonsky 2019, anxiety meta-analysis](https://doi.org/10.1017/S0272263118000311)
- [Schulz 1996, student and teacher views on correction](https://doi.org/10.1111/j.1944-9720.1996.tb01247.x)
- [Schulz 2001, USA and Colombia](https://doi.org/10.1111/0026-7902.00107)
- [Kang & Han 2015, written feedback meta-analysis](https://doi.org/10.1111/modl.12189)
- [Schmidt 1990, noticing](https://doi.org/10.1093/applin/11.2.129)
- [Lee & Huang 2008, input enhancement meta-analysis](https://doi.org/10.1017/S0272263108080479)
- [Payne & Whitney 2002, chat and oral proficiency](https://doi.org/10.1558/cj.v20i1.7-32)
- [Ziegler 2016, chat vs face-to-face meta-analysis](https://doi.org/10.1017/S027226311500025X)

**Vocabulary**

- [Vidal 2011, reading vs listening vocabulary](https://doi.org/10.1111/j.1467-9922.2010.00593.x)
- [van Zeeland & Schmitt 2013, vocabulary from listening](https://doi.org/10.1016/j.system.2013.07.012)
- [Uchihara, Webb & Yanagisawa 2019, repetition meta-analysis](https://doi.org/10.1111/lang.12343)
- [Webb 2007, repetition](https://doi.org/10.1093/applin/aml048)
- [Kim & Webb 2022, spacing meta-analysis](https://doi.org/10.1111/lang.12479)
- [Nakata 2017, repeated retrieval](https://doi.org/10.1017/S0272263116000280)
- [Yanagisawa, Webb & Uchihara 2020, glossing meta-analysis](https://doi.org/10.1017/S0272263119000688)
- [Boers et al. 2006, formulaic sequences and oral proficiency](https://doi.org/10.1191/1362168806lr195oa)
- [Webb, Newton & Chang 2013, collocations](https://doi.org/10.1111/j.1467-9922.2012.00729.x)

**Speaking, pronunciation, measurement**

- [Lee, Jang & Plonsky 2015, pronunciation meta-analysis](https://doi.org/10.1093/applin/amu040)
- [Saito & Plonsky 2019, pronunciation meta-analysis revisited](https://doi.org/10.1111/lang.12345)
- [Munro & Derwing 1995, accent and comprehensibility](https://doi.org/10.1111/j.1467-1770.1995.tb00963.x)
- [Sakai & Moorman 2018, perception training meta-analysis](https://doi.org/10.1017/S0142716417000418)
- [Thomson 2018, high-variability phonetic training](https://doi.org/10.1075/jslp.17038.tho)
- [Hamada 2016, shadowing](https://doi.org/10.1177/1362168815597504)
- [Kadota 2019, Shadowing as a Practice in SLA](https://doi.org/10.4324/9780429429866)
- [Yan et al. 2016, elicited imitation meta-analysis](https://doi.org/10.1177/0265532215594643)
- [de Jong et al. 2012, facets of speaking proficiency](https://doi.org/10.1017/S0272263111000489)
- [de Jong et al. 2013, linguistic skills and speaking fluency](https://dare.uva.nl/id/a6d0ce87-9e8a-4f40-9c3d-8a002907c794)

**Time, hours, immersion practice**

- [Nation 2007, the four strands](https://doi.org/10.2167/illt039.0)
- [US Foreign Service Institute, language training hours](https://www.state.gov/foreign-language-training/)
- [Dreaming languages roadmap, community copy](https://r.datuan.dev/r/dreaminglanguages/wiki/index)
- [Serrano & Muñoz 2007, same hours, different distribution](https://diposit.ub.edu/dspace/handle/2445/164086)
- [Peters 2018, out-of-class media exposure](https://doi.org/10.1075/itl.00010.pet)
- [Refold method](https://refold.la)
- [ALG World, Automatic Language Growth](https://algworld.com)

**Added in the final check**

- [DeKeyser 1997, Beyond explicit rule learning](https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/abs/beyond-explicit-rule-learning/B71581638BF89873F61F03EA1E747E5A)
- [Bibauw et al. 2022, dialogue systems meta-analysis](https://www.lltjournal.org/item-detail/1035)
- [Hou & Min 2025, AI chatbots and speaking](https://www.cambridge.org/core/product/31847710516602398819C5E594038E7B)
- [Wang, Bibauw, Noreillie & Desmet 2026, chatbot meta-analysis (conference abstract)](https://research.dial.uclouvain.be/entities/publication/29791a54-111b-40eb-bacb-346494980619)
- [Rezaee & Farahian 2012, teacher and student talk](https://www.researchgate.net/figure/The-Percentage-of-Teacher-Talk-Student-Talk-and-Other-Activities-in-the-Total-Class-Time_tbl1_271889540)
- [English in Action 2010, classroom practice](https://assets.publishing.service.gov.uk/media/57a08ad9ed915d622c00093f/2a_the_classroom_practices-teachers_participating_in_english_in_action.pdf)
- [Uchihara, Karas & Thomson 2025, HVPT meta-analysis](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6ABB8C1F32D88D53EA8D05A4565E76F6/S0272263125100879a.pdf/high-variability-phonetic-training-hvpt-a-meta-analysis-of-l2-perceptual-training-studies.pdf)
- [Uchihara, Karas & Thomson 2024, HVPT and production](https://www.cambridge.org/core/product/E38D8F5CE65DC708137B0E95F97C6BC7)
- [Whitworth 2024, shadowing systematic review](https://ora.ox.ac.uk/ark:/29072/ora_3104cae13a6b400ab173de44384238d2)
- [Kostromitina & Plonsky 2022, elicited imitation meta-analysis](https://experts.nau.edu/en/publications/elicited-imitation-tasks-as-a-measure-of-l2-proficiency/)
- [Takizawa & Suzuki 2025, reporting Suzuki, Kormos & Uchihara 2021](https://www.cambridge.org/core/product/FAB18835B2117A299C33F8F502248C81)
- [Kakitani & Kormos 2024, distributed practice and fluency](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4F6787916C198376CAD222934D3B37E4/S0272263124000251a.pdf/the-effects-of-distributed-practice-on-second-language-fluency-development.pdf)
- [Sundqvist 2019, gaming and vocabulary](https://www.lltjournal.org/item-detail/903/)
- [Refold roadmap overview](https://refold.la/roadmap/stage-0/a/roadmap-overview)
- [Steve Kaufmann on starting to speak](https://www.lingq.com/en/learn-english-online/courses/135380/how-to-start-talking-in-a-new-languag-6755385/)
- [J. Marvin Brown](https://en.wikipedia.org/wiki/J._Marvin_Brown)

* [Yến & Waring 2022, narrow listening](https://www.culi.chula.ac.th/Images/asset/pasaa_journal/file-2-23-9jdhtg698061.pdf)
* [Brown, Waring & Donkaewbua 2008, vocabulary from reading, listening and both](https://www2.hawaii.edu/~readfl/rfl/October2008/brown/brown.html)
* [Webb, Uchihara & Yanagisawa 2023, incidental vocabulary meta-analysis](https://doi.org/10.1017/S0261444822000507)
* [Li & Lei 2022, collocation instruction meta-analysis](https://doi.org/10.1515/iral-2021-0218)
* [Abdi Tabari, Zhuang & Farahanynia 2025, task repetition meta-analysis](https://doi.org/10.1016/j.system.2025.103868)
* [Boers & Faez 2023, on TBLT meta-analyses](https://doi.org/10.1177/13621688231167573)
* [Rassaei 2015, feedback and anxiety](https://doi.org/10.1016/j.system.2015.01.002)
