# English ban lists: sameness and the correction guard

*Draft, written on delegation (ADR-24.3). Read by Muath and checked by the AI review pass (ADR-25.7); afterwards updated monthly from review findings (PRD FR-431, FR-436). Ships to `packages/languages/en/` (see [../README.md](../README.md)).*

Two lists live here, for two different jobs:

- **A. The sameness ban list** keeps the writer away from the names, settings, plots and phrases that AI stories converge on (PRD FR-431, editor check 9 in FR-419; architecture/02 §4.6 and §4.9). It ships as `packages/languages/en/ban_list.yaml`.
- **B. The law-word and correction-guard corpus** lists the phrases that read as correction, grading, homework, a count, guilt or a false claim (PRD FR-420, LAW-01, -04, -05, -07, -08, -12; ADR-06; architecture/07 §4.10 `guard.check_output` items 1 to 3 and 6). It ships as two files with one schema: `packages/languages/en/guard/correction_words.yaml` (the correction rows, file **C**) and `packages/languages/en/guard/law_words.yaml` (everything else, file **L**).

Salma's lines are checked against the native package's own lists, in her language (`packages/native/<lang>/guard/`); [../bibles/salma.md §8](../bibles/salma.md) starts the Arabic one.

---

## A. The sameness ban list

### A.1 How it is applied

- **Scope: invented fiction and host phrasing only.** The list never blocks the learner's own name, a name in FACTS_ALLOWED or INTEREST_ENTITIES, the hosts' names, or the default world's names ([../bibles/hosts-en.md §5](../bibles/hosts-en.md)). If the learner is called Sarah, the hosts say Sarah.
- **Matching** (architecture/02 §4.9): code matches names and phrases by lemma sequence, settings and plots by keyword sets; the editor model catches paraphrased plots ("a note nobody signed" is still the mysterious letter).
- **Entry shape** (architecture/02): `{kind: name|setting|plot|phrase, value, lemma_seq, added_from, added_at}`. The seed rows below have `added_from: "seed:content/ban-lists/en.md@v1"`; later rows carry the review finding id.
- **Seed.** The rows marked **seed** are the BANNED block of the first draft bible, carried over unchanged ([milestone-0/05-prompts.md §S](../../milestone-0/05-prompts.md), kept as source material).

### A.2 Names (28 first names, 4 stock name-constructions)

The names AI fiction reaches for first. Banned as names for invented characters only.

| Value | Note |
|---|---|
| Alex **seed** | The default gender-neutral protagonist |
| Sam **seed** | Same |
| Sarah **seed** | The default friend, colleague or neighbour |
| John **seed** | The default man |
| Emily **seed** | The default woman |
| Elara **seed** | The default fantasy heroine |
| Lila **seed** | Same family as Elara |
| Max **seed** | The default dog, child or rival |
| Maya | Very high frequency in model stories |
| Mia | Same |
| Lily | Same |
| Clara | Same |
| Elena | Same |
| Chloe | Same |
| Olivia | Same |
| Luna | Also the default pet name |
| Aria | Same |
| Zara | Same |
| Nora | Same |
| Liam | Same |
| Ethan | Same |
| Leo | Same |
| Theo | Same |
| Finn | Same |
| Jake | Same |
| Marcus | The default mentor or boss |
| Kai | The default "cool" character |
| Jasper | The default eccentric |
| "Mr. Thompson" / "Mrs. Thompson" | The default neighbour or teacher construction |
| "Mrs. Henderson" | Same |
| "Old Mr. Jenkins" | The default kindly old man |
| "Dr. Chen" | The default doctor or scientist; the construction is banned, not the surname a learner gives |

**What to do instead.** Name a new side character after something the learner said (their colleague "the one who answers at midnight"), give them a role instead of a name ("the new manager"), or pick a less common name from anywhere in the world that is not on this list. Never pick a name to signal a nationality the learner did not give.

### A.3 Settings (16)

| Value | Note |
|---|---|
| A lighthouse **seed** | |
| A small coastal town **seed** | Also "a sleepy seaside village" |
| A quiet café on a rainy day **seed** | Cafés are allowed; this mood-piece café is not |
| A cosy bookshop / an old second-hand bookstore | |
| A bustling market or marketplace | Also banned as a phrase (A.5) |
| An old library with dusty books | |
| An attic with an old trunk | |
| A quaint village | |
| A cottage by the sea | |
| A cabin in the mountains or the woods | |
| An enchanted, whispering or ancient forest | |
| A rooftop at sunset or under the stars | |
| A clock tower | |
| An abandoned train station | |
| A small bakery at dawn | |
| A hidden garden | |

**What to do instead.** Use the learner's places (their office, their club's ground, the bus they take), the default world's places, or an ordinary specific place: a dentist's waiting room, a car park at 7am, a supermarket queue.

### A.4 Plots (16)

| Value | Note |
|---|---|
| An unexpected friendship **seed** | |
| A mysterious letter **seed** | Also a mysterious note, package, key or voicemail |
| A lesson learned **seed** | Also any moral stated at the end |
| A stranger with a secret | |
| A found diary or journal | |
| A map that leads to treasure | |
| A secret family recipe revealed | Karim's grandmother's soup is a running joke, never a secret |
| Mistaken identity | |
| A wise old mentor's advice changes everything | |
| A last-minute win in a big competition | |
| A lost pet found | |
| A power cut that brings the neighbours together | |
| A childhood friend returns | |
| A time capsule is opened | |
| An inheritance from someone unexpected | |
| A kindness to a stranger who turns out to be the interviewer or the boss | Especially tempting in interview arcs |

**What to do instead.** Start from what the learner told the show this week, or from a small real problem with a 50/50 answer (the format library in [../bibles/hosts-en.md §6.5](../bibles/hosts-en.md)).

### A.5 Phrases (28)

Banned in every host-written surface: script, article, chat opener, recap, the call.

| Value | Note |
|---|---|
| "buckle up" **seed** | |
| "let's dive in" / "dive into" **seed** | |
| "game-changer" **seed** | |
| "in today's fast-paced world" **seed** | |
| "it's not just X, it's Y" **seed** | Also "not just X but Y" as a structure |
| "delve" | Any form |
| "tapestry" | |
| "a testament to" | |
| "navigate the complexities" | Also "navigate the world of" |
| "unlock your potential" | Also a law word (B, `game.unlock`) |
| "embark on a journey" | Also "journey" as a metaphor for learning |
| "nestled" | |
| "bustling" | |
| "vibrant" | |
| "hidden gem" | |
| "little did they know" | |
| "picture this" | |
| "let that sink in" | |
| "the rest is history" | |
| "at the end of the day" | |
| "a breath they didn't know they were holding" | |
| "elevate" | In the sense of improving something |
| "seamless" | |
| "resonates with" | |
| "Great question!" | Also "That's a great question" |
| "Absolutely!" as a one-word answer | |
| "stay tuned" | The show has no next episode to tease |
| "without further ado" | |

---

## B. The law-word and correction-guard corpus (69 entries)

### B.1 How the guard reads it

From architecture/07 §4.10 (`guard.check_output`):

- **Hard** entries always block. **Soft** entries block only when a second-person word (`you`, `your`, `you're`, `yours`, `yourself`, `you've`, `you'd`, `you'll`) is within six tokens; "the test match", "a job interview with three levels" and "a football score" pass.
- A block in a live call cancels the sentence and re-requests once; a second hit plays the package line "Hang on, say that again?" (architecture/03 §4.3). A block in a script, article, chat opener or recap is repaired once, then the fallback episode ships (PRD FR-422). Every correction hit counts toward `explicit_corrections_per_100_turns`, whose ceiling is 0.
- **Precision floors:** 0.95 for hard entries, 0.99 for soft ones, measured on the clean corpus (architecture/09). A soft entry that cannot meet 0.99 is dropped rather than kept.
- **Roles** say which surfaces an entry applies to: `writer` (script, article, chat opener, recap), `host` (live call), `chat_host`. Unless a row says otherwise, an entry applies to all three. Salma has her own lists.
- **Allow** lists exact phrases that pass despite a match.

Two writing rules the guard depends on, from the bible: hosts avoid verdict words even with each other, because the guard reads "you" as the listener; and explanations the learner asked for are phrased positively, without "not" and without quoting the learner (an explanation of the form "we say X, not Y" will block).

### B.2 The corpus

Column **F** is the file: **C** = `correction_words.yaml`, **L** = `law_words.yaml`. Column **K** is hard (H) or soft (S).

**Correction (LAW-07; ADR-06; PRD FR-333, FR-837)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `corr.wrong` | "wrong" | C | H | A verdict. Hosts avoid it even with each other; "what went wrong with the bread" is rewritten as "what happened to the bread". |
| `corr.thats_wrong` | "that's wrong", "that's not right", "that isn't right" | C | H | |
| `corr.incorrect` | "incorrect", "not correct" | C | H | |
| `corr.correct_form` | "the correct (form, word, answer, way, sentence, version)" | C | H | architecture/07 item 6's own example. |
| `corr.correct_verdict` | "Correct." / "That's correct." as a reply | C | H | A positive verdict is still a verdict. |
| `corr.right_word` | "the right (word, form, way to say)" | C | H | |
| `corr.should_say` | "you should say", "you should have said", "you need to say" | C | H | |
| `corr.we_say_not` | "we say X, not Y", "it's X, not Y" with X or Y quoted | C | H | Contrasting the error. Also catches explanations phrased negatively. |
| `corr.actually_its` | "actually, it's", "actually it is", "actually, we say" | C | H | |
| `corr.mistake` | "mistake" (any form) | C | H | Allow: "my mistake", "my mistake, noted" (PRD FR-626). |
| `corr.error` | "error" | C | H | |
| `corr.repeat_after_me` | "repeat after me", "say it with me" (in a call) | C | H | Shadowing lines are offered by the player, not by a host in conversation. |
| `corr.say_again_properly` | "say it again (properly, correctly, the right way)", "try saying it" | C | H | Allow: "say that again?" (a clarification; the package filler line). |
| `corr.try_again` | "try again" | C | H | Roles: host, chat_host, writer. Salma's system copy ("Try again in a moment") is checked by the native list, where it is allowed. |
| `corr.almost` | "almost!", "almost there", "so close" as a reply | C | H | "Almost ten years" passes; the pattern is the reply form. |
| `corr.not_quite` | "not quite" | C | H | |
| `corr.close_but` | "close, but" | C | H | |
| `corr.careful_with` | "careful with (the, your)" | C | H | |
| `corr.remember_its` | "remember, it's", "don't forget the (s, -ed, article)" | C | H | |
| `corr.let_me_correct` | "let me correct", "(small, quick, little) correction", "to correct you" | C | H | |
| `corr.grammar_label` | "grammar rule", "the rule is", "the past tense of", "irregular verb" (unasked) | C | H | Grammar labels only if the learner used them first (design/06 §2). |
| `corr.you_mean_quoted` | "you mean" followed by a quotation mark | C | H | The recast says the form inside a sentence ("you mean you went?"); a quoted form is a correction. |
| `corr.instead_of` | "instead of saying" | C | H | |
| `corr.common_learner_error` | "a common mistake", "learners often say", "people who speak {language} often" | C | H | Generalising about the learner's errors or first language. |
| `corr.pronunciation` | "your pronunciation", "your accent", "pronounce it (properly, like this)" | C | H | Pronunciation is scored only internally (PRD FR-318). |
| `corr.your_english` | "your English" | C | H | Also a progress claim (below). |

**Grading and praise of the person (LAW-01, LAW-07; PRD FR-338)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `grade.good_job` | "good job", "great job", "nice job" | L | H | |
| `grade.well_done` | "well done" | L | H | |
| `grade.perfect` | "perfect!", "that was perfect", "perfect English" | L | H | "A perfect Sunday" passes. |
| `grade.proud` | "proud of you" | L | H | |
| `grade.excellent` | "excellent" | L | S | |
| `grade.nailed_it` | "nailed it", "crushed it", "crushing it" | L | H | |
| `grade.so_good` | "you're so good", "you're a natural", "you're doing great" | L | H | Praise of the person. One specific remark about the task per call is allowed (FR-338). |
| `grade.score` | "score" | L | S | A football score passes. |
| `grade.points_earned` | "(you) earned, got, scored, won ... points" | L | H | "You made two good points" passes. |
| `grade.grade_marks` | "grade", "marks", "out of ten", "/10" | L | S | |
| `grade.percent` | any percentage ("40%", "forty percent") | L | H | Hosts turn a learner-supplied figure into words ("almost half"). |
| `grade.cefr` | "A1", "A2", "B1", "B2", "C1", "C2" as standalone tokens | L | H | Salma may name a range only in a "where do I stand" answer (native list). |
| `grade.level` | "level" | L | S | "Three levels of the car park" passes. |
| `grade.fluent` | "you're fluent", "your fluency" | L | H | Also a progress claim. |

**Progress claims (LAW-12; PRD FR-840; architecture/07 item 3)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `prog.improved` | "you've improved", "you have improved", "you're improving" | L | H | The claim gate is the only route to a progress sentence. |
| `prog.getting_better` | "getting better" | L | H | Kept hard as architecture/07 specifies; "the bread is getting better" will block too, so the writer says "the bread is less bad". |
| `prog.your_english_is` | "your English is", "your English has" | L | H | |
| `prog.progress` | "your progress", "you're making progress" | L | H | Salma's consent line uses "progress" and is checked by the native list. |

**Lessons and homework (LAW-08; PRD FR-420)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `hw.homework` | "homework" | L | H | |
| `hw.practise_this` | "practise / practice (this, that, it, at home)", "go and practise" | L | H | Both spellings. |
| `hw.for_next_time` | "for next time, (try, remember)" | L | H | |
| `hw.your_task` | "your task", "your assignment", "your challenge (for, this)" | L | H | |
| `hw.lesson` | "lesson" | L | S | "A lesson learned" is also a banned plot (A.4). |
| `hw.exercise` | "exercise" | L | S | Mona's run is exercise; that passes. |
| `hw.test_quiz` | "test", "quiz", "exam" | L | S | "The interview has a practical test" passes. |
| `hw.dont_forget_to` | "don't forget to" | L | H | design/06 §2. |
| `hw.make_sure_you` | "make sure you" | L | H | |
| `hw.study_review` | "study (this, these)", "review (this, these) words", "revise" | L | H | |

**Counts and game furniture (LAW-01)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `game.streak` | "streak" | L | H | |
| `game.in_a_row` | "(number) (days, episodes, times) in a row" | L | H | |
| `game.badge` | "badge", "level up", "XP", "leaderboard" | L | H | |
| `game.unlock_reward` | "unlock", "reward" | L | S | "Unlock the door" in a story passes. |

**Guilt and obligation (LAW-04, LAW-05; TC-2; PRD FR-240, FR-1022)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `guilt.miss_you` | "I missed you", "we missed you", "I miss you", "I'll miss you", "we'll miss you" | L | H | |
| `guilt.where_were_you` | "where were you", "where have you been" | L | H | |
| `guilt.you_missed` | "you missed (a, an, the, yesterday, some, a number)" | L | H | "Mona missed it" (the retell prompt) passes. |
| `guilt.been_a_while` | "it's been a while", "long time no see", "haven't heard from you" | L | H | |
| `guilt.welcome_back` | "welcome back" | L | H | Return episodes never mention time away (FR-212). |
| `guilt.dont_go` | "don't go", "stay a bit longer", "stay a little longer", "just one more" | L | H | |
| `guilt.waiting_for_you` | "(I was, we were) waiting for you", "we waited" | L | H | The driving line "I'll be here" and the feed tag "I'll be on the line" pass. |
| `guilt.come_back` | "come back (tomorrow, soon)", "promise (me, you'll)" | L | H | |
| `guilt.feelings` | "I'll be (lonely, sad)", "I was (worried, lonely)" | L | H | |

**False humanity (LAW-05; TC-3; architecture/07 item 1)**

| Id | Phrase or pattern | F | K | Note |
|---|---|---|---|---|
| `human.claim` | "I'm (a) (real) (human, person)", "I'm not an AI", "I'm real" | L | H | Replaced by the pre-rendered `ai_disclosure` line rather than re-requested. |
| `human.outside_show` | "when (we, I) met (you)", "I've been thinking about you", "I thought about you (yesterday, last night)" | L | H | PRD FR-561. |

### B.3 The file shape the guard reads

One schema for both files. This is the shape for `packages/languages/en/guard/correction_words.yaml`; `law_words.yaml` is the same with its own rows.

```yaml
# packages/languages/en/guard/correction_words.yaml
schema: forone.guard/v1
language: en
version: "1.0"                # a bump runs the writer and host suites (backlog E02-S07)
second_person: [you, your, "you're", yours, yourself, "you've", "you'd", "you'll"]
soft_window_tokens: 6         # architecture/07 §4.10 item 2
entries:
  - id: corr.correct_form
    kind: hard                # hard | soft
    match: {regex: "\\bthe (correct|right) (form|word|answer|way|sentence|version)\\b"}
    roles: [writer, host, chat_host]
    law: LAW-07
    note: A verdict on the learner's language.
    examples:
      block: ["The correct form is 'went'."]
      pass: []
  - id: corr.mistake
    kind: hard
    match: {lemma: mistake}   # lemma | phrase | regex
    allow: ["my mistake", "my mistake, noted"]
    roles: [writer, host, chat_host]
    law: LAW-07
    note: FR-626 lets a host own a wrong memory; nothing else.
    examples:
      block: ["That's a common mistake."]
      pass: ["My mistake, noted."]
  - id: corr.you_mean_quoted
    kind: hard
    match: {regex: "\\byou mean\\s*[\"'“‘]"}
    roles: [writer, host, chat_host]
    law: LAW-07
    note: A recast says the form inside a sentence; a quoted form is a correction.
    examples:
      block: ["You mean 'went'?"]
      pass: ["Oh, you mean you went there last year?"]
```

Every `examples.block` and `examples.pass` string becomes a fixture in the guard suite (`eval/fixtures/`), so a changed pattern that starts passing a blocked example, or blocking a passing one, fails CI.

### B.4 Maintenance

- **Monthly**, findings from Muath's reads and the AI review pass over sampled episodes (FR-436, ADR-25.7) add or retire rows through `review_items` (architecture/02 D17); nobody edits the YAML by hand in production.
- **A new row** needs an id, a law, a hard or soft kind, and at least one block and one pass example.
- **A soft row** that falls under 0.99 precision on the clean corpus is dropped, not loosened into a hard one.
- **The 50-call bench** (before launch) reports the re-request rate per row; a row that re-requests often on clean turns is rewritten, not ignored.
