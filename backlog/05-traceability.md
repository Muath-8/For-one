# For one: requirements traceability

*Written 2026-11-12 and regenerated the same day after ADR-25, from PRD-v3 and the story files as they stand. Every story carries a `Requirements:` line and `stories.csv` a `requirements` column (semicolon-separated); this page is the reverse view, from each requirement to its stories.*

## How to read it

- **Ids.** PRD-v3 defines 303 FR ids and 42 NFR ids in Parts 1 to 15.
- **Priority** is the PRD's, which ADR-25 redefined: P0 is needed at launch (v1), P1 is after launch (v1.1), LATER is built in neither, and **Retired** ids no longer apply (kept so old citations resolve). An untagged requirement in Parts 2 to 12 is P0. The Part 1 scope rows carry no tag and are read as P0 ("scope, untagged"); the Part 15 roster rows carry a `v1` column, read as P0 when it says yes. Rows with a split tag ("P0 record / P1 compare", "P0 rule / P1 set") count as P0.
- **Stories.** A plain id is a v1 story, built before launch. `(v1.1)` marks a story shipped after launch, `(later)` one not planned. `NF-xx` are the cross-cutting stories in `03-non-functional-stories.md`; their work sits in the owner stories they name.
- **The rule.** A story cites only what its acceptance criteria implement. A P0 requirement must rest on at least one v1 story; a retired requirement must not be cited at all.

## 1. Summary

| | P0 | P1 | LATER | Retired | Total |
|---|---|---|---|---|---|
| FR ids | 279 | 11 | 8 | 5 | 303 |
| NFR ids | 40 | 2 | 0 | 0 | 42 |
| With no story | 0 | 0 | 5 | 5 (by design) | |

Every P0 requirement rests on at least one v1 story; every P1 requirement has a story; no story cites a retired id.

## 2. Requirement to stories

### Part 1

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-001 | P0 (scope, untagged) | Learner: Any adult (18 or older) who already understands some of the target language and ... | E13-S04 |
| FR-002 | P0 (scope, untagged) | Languages: As many target languages as the speech stack supports, decided by the language ... | E02-S06 |
| FR-003 | P0 (scope, untagged) | Age: 18+. A checkbox on the first screen; birth date at account creation; under-18 dates ... | E06-S03, E06-S08, E13-S04 |
| FR-004 | P0 (scope, untagged) | Access: Open signup from launch: anyone 18 or older, in a country where Paddle sells, can ... | E06-S02, E16-S01 |
| FR-005 | P0 (scope, untagged) | Plans: Monthly only. Three plans that differ only in new episodes per active day: 1 a day ... | E12-S01 |
| FR-006 | P0 (scope, untagged) | Unlimited on every plan: Re-listening, the archive, the feed, the article, the chat, the ... | E12-S02 |
| FR-007 | P0 (scope, untagged) | Free taste: The first episode and the first call inside onboarding, before any account ... | E06-S01 (v1.1), E12-S03 |
| FR-008 | P0 (scope, untagged) | Messages: Exactly three kinds of message ever leave the product (FR-240). | E08-S03, NF-17 |
| FR-009 | P0 (scope, untagged) | Platform: Decided: a web application (mobile Safari and Chrome, installable to the home ... | E06-S09, E07-S01, E08-S01 |
| FR-010 | P0 (scope, untagged) | Interface language: The interface, Salma, captions and glosses are in the learner's own ... | E06-S03, E07-S01, NF-25 |
| FR-011 | P0 (scope, untagged) | AI cost: Budget about $0.60 per session at launch; scale target $0.30 to $0.35; stop line ... | E14-S02, E14-S08, NF-06 |

### Part 2

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-101 | P0 | A plain public landing page in the visitor's language (from the browser, with a language ... | E06-S02 |
| FR-102 | P1 | The visitor picks the language they want to speak (only shipped targets are offered) ... | E06-S01 (v1.1) |
| FR-103 | P1 | The hosts make a 90-second sample episode about that topic, using the name once, playable ... | E04-S08, E06-S01 (v1.1) |
| FR-104 | P1 | The sample ends with Salma, in the visitor's own language: the full show is a new episode ... | E06-S01 (v1.1) |
| FR-105 | Retired | Retired (ADR-25.5): there is no waitlist form. | retired |
| FR-106 | Retired | Retired (ADR-25.5): there are no invites or invite batches; signup is open (FR-004). | retired |
| FR-110 | P0 | A1 Open: One screen in the learner's own language: "Your own show, in English." One Start ... | E06-S03 |
| FR-111 | P0 | A2 Mic primer: "Salma, your producer, will talk with you for 3 minutes. You can talk or ... | E06-S04 |
| FR-112 | P0 | A3 Salma: Salma's voice, in the learner's own language, within 60 seconds of opening. Her ... | E05-S04, E06-S04 |
| FR-113 | P0 | A4 Word check (optional): "Want to help me pitch your show just right? 60 seconds: tap ... | E06-S05 |
| FR-114 | P0 | A5 Casting: While the first episode is made: each host says hello (5 seconds); "swap" ... | E04-S10, E06-S06 |
| FR-115 | P0 | A6 The first episode: A 2 to 3 minute episode about the hour-long topic, the learner's ... | E04-S08, E06-S07 |
| FR-116 | P0 | A7 First call: A host throws a question the learner can answer in one or two sentences. ... | E05-S05, E06-S07 |
| FR-117 | P0 | A8 One thing managed: In the call's goodbye, the host names one real thing the learner ... | E05-S05, E06-S08 |
| FR-118 | P0 | A9 Keep your show: Account (email one-time code, the only sign-in; there is no Sign in ... | E06-S08, E07-S02, E13-S03, E16-S04 (v1.1) |
| FR-119 | P0 | A10 Tomorrow: Three ideas for tomorrow's episode, written from the intake, plus "Tell ... | E06-S09 |
| FR-120 | P0 | Targets: Measured from the first open: first sound under 60 seconds; the learner's first ... | E06-S07, E06-S11, E15-S07, NF-02 |
| FR-121 | P0 | Starting estimate: The two target-language moments, the word check (if taken) and the ... | E03-S07 |
| FR-122 | P0 | Address form: In a native language whose "you" is gendered (Arabic first), A3 offers an ... | E06-S04 |
| FR-125 | P0 | The day-2 episode carries at least one callback sourced verbatim from something said in ... | E04-S02 |
| FR-126 | P0 | Week 1 asks at most one personal question per session, the way a host or Salma naturally ... | E06-S12 |

### Part 3

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-201 | P0 | Tomorrow's choice appears at the close of whichever door the learner uses last today ... | E07-S08 |
| FR-202 | P0 | Three ideas, each one line of at most 140 characters, carrying topic, format and cast ... | E04-S09, E07-S08, E10-S08 |
| FR-203 | P0 | Composition, enforced by the teacher: at least one idea from the learner's own life if a ... | E04-S09 |
| FR-204 | P0 | The ideas for day N+1 are written in the plan made the night before day N. Pedagogy is ... | E04-S09 |
| FR-205 | P0 | Cutoff: if nothing is chosen by 6 hours before the drop time, the teacher's top-ranked ... | E04-S09 |
| FR-206 | P0 | New episodes per active day, by plan: 1, 2 or 3. An active day is a local calendar day on ... | E04-S08, E08-S02, E12-S02 |
| FR-207 | P0 | No episode is made after an inactive day. If yesterday's episode is unplayed, it stays as ... | E07-S05, E08-S02 |
| FR-208 | P0 | One swap a day. "Not this one" on a dropped, unstarted episode makes the second-ranked ... | E04-S08, E07-S09 |
| FR-209 | P0 | When a learner reaches the plan's number for the day, Today says plainly, in text ... | E07-S05, E12-S02, E12-S10 |
| FR-210 | P0 | The small door. Every episode ships with a 90-second recap by the hosts, made in the same ... | E04-S08, E07-S10 |
| FR-211 | P0 | Gap note (opt-in). Offered once in week 1: the learner writes a short note to their ... | E06-S12, E08-S05 |
| FR-212 | P0 | Return episode. After 5 or more days with no session, the next episode is a return ... | E04-S08, E08-S06 |
| FR-213 | P0 | Near a natural landmark (a Monday, the first of a month, a new season) the return episode ... | E08-S06 |
| FR-214 | P0 | Returning after a gap, the Today screen looks exactly like any other day. Nothing ... | E07-S05, E08-S06 |
| FR-220 | P0 | The anchor is the drop time chosen in onboarding, stated in life terms ("after I sit down ... | E06-S08, E08-S07 |
| FR-223 | P0 | The rhythm is a weekly intention with spare days: the learner picks 3 to 6 days a week ... | E06-S12, E08-S07 |
| FR-224 | P0 | The rhythm is never shown as a counter, calendar, flame or record of missed days. The ... | E08-S07, E11-S04, NF-14 |
| FR-225 | P0 | Re-anchoring. Salma asks once for a new anchor when the learner mentions a move, a new ... | E08-S07 |
| FR-230 | P0 | When the pick is made (or at the cutoff), the teacher writes the brief and the pipeline ... | E04-S07, E08-S02 |
| FR-231 | P0 | The episode is visible in the app as soon as it is ready. The drop time controls the ... | E07-S05, E08-S02 |
| FR-232 | P0 | At the drop time the episode is published to the learner's private feed and one ... | E08-S01, E08-S03 |
| FR-233 | P0 | The feed version: the same episode plus a 5-second tag from the host at the end ("To call ... | E08-S01, E08-S04 |
| FR-235 | P0 | One hero episode, big, with a typographic cover (title, hosts' marks, the show's colour) ... | E07-S05 |
| FR-236 | P0 | Hero states: ready, not started = cover and ▶ Play; in progress = the cover with doors ... | E07-S05 |
| FR-237 | P0 | Three tabs only: Today, Show (the archive, FR-1002), Notebook (FR-1010). At launch there ... | E07-S05 |
| FR-240 | P0 | Exactly three kinds of message ever leave the product: (1) the drop notification, at the ... | E08-S03, E08-S05, E12-S05, E12-S11 (v1.1), NF-17 |

### Part 4

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-301 | P0 | Door states: not_started, in_progress(position), done, skipped. Session states: ready ... | E07-S13 |
| FR-302 | P0 | Any order (suggested order Listen, Read, Call, Chat, ADR-24.2). Every door can be opened ... | E07-S13 |
| FR-303 | P0 | Planning time when the article is skipped. Listen straight to Call shows a 30-second ... | E07-S07 |
| FR-304 | P0 | Pause and resume. Audio position, article scroll and chat history persist indefinitely. A ... | E05-S10, E07-S13 |
| FR-305 | P0 | Skips are allowed and logged as energy and taste signals. Nothing punishes a skip; the ... | E07-S13 |
| FR-306 | P0 | Re-entry. Listen and Read remain playable and readable forever (archive). The main call ... | E07-S11 (v1.1), E08-S01 |
| FR-307 | P0 | Closing. A session closes when the learner's next episode is published. Its partial ... | E07-S13 |
| FR-310 | P0 | Length: target 5 to 7 minutes; hard bounds 4:00 and 8:00. The teacher shortens it on ... | E04-S02 |
| FR-311 | P0 | Structure: (1) a cold open of at most 30 seconds in which the hosts use two or three of ... | E04-S02 |
| FR-312 | P0 | Cast: exactly the chosen cast, one host or both. Personal references: interests lead; at ... | E04-S02 |
| FR-313 | P0 | Speech: the target language throughout, at the learner's listening edge (FR-730). ... | E04-S03 |
| FR-314 | P0 | The player: play/pause and scrub; ⟲ line replays the last sentence (not 10 seconds); Huh? ... | E07-S03 |
| FR-315 | P0 | Lock screen and headphones: through the Media Session API where the browser supports it ... | E07-S03 |
| FR-316 | P0 | Logged: play, pause, position, speed, replays, Huh? (sentence), transcript open/close ... | E03-S08, E07-S04 |
| FR-318 | P1 | Shadow: say it with the host. Offered after the episode as one optional line ("Say two ... | E16-S04 (v1.1) |
| FR-319 | P0 | Length by reading estimate: 150 to 300 words at A2, 250 to 450 at B1 and B2, 350 to 600 ... | E04-S02, E07-S06 |
| FR-320 | P0 | Entry: one tap from the throw, from Today, or from the feed link. The call screen keeps ... | E07-S07 |
| FR-321 | P0 | Length: target 5 to 7 minutes. The host begins a natural close at 6:30 and ends by 8:00 ... | E05-S09 |
| FR-322 | P0 | Speaking time: the goal is 4 or more minutes of the learner's own speech per session ... | E05-S08 |
| FR-323 | P0 | Turn-taking: open mic by default. Hold to keep the floor: while the learner holds the ... | E05-S06 |
| FR-325 | P0 | The word button. The learner holds the word button and says the word or phrase in their ... | E05-S07 |
| FR-326 | P0 | Word or hint: if the learner has never produced the word, the host gives it. If they have ... | E05-S07 |
| FR-330 | P0 | The host's move contract applies in every call except the onboarding call (FR-116). ... | E05-S02 |
| FR-331 | P0 | Clarification request: when an error blurs or blocks meaning, a real "sorry, you did ... | E05-S02 |
| FR-332 | P0 | Recast ("you mean..."): the host says the learner's point back the natural way inside a ... | E05-S02 |
| FR-333 | P0 | The host never says or implies "wrong", "mistake" or "the correct way is"; never grades ... | E05-S02, E13-S09, NF-15 |
| FR-334 | P0 | Recall gaps: 2 to 4 per call, moments that make the learner pull a due word or phrase out ... | E05-S08 |
| FR-335 | P0 | Target necessity: the brief includes one or two host moves per target that make the ... | E04-S02, E05-S08 |
| FR-336 | P0 | Retell: once per call: "Mona missed it. Sixty seconds, go." A soft 60-to-90-second ring ... | E05-S08 |
| FR-337 | P0 | Hints before answers: the host never completes the learner's sentence. "How do I say X?" ... | E05-S07 |
| FR-338 | P0 | Praise: at most one specific remark about the task per call, naming something observable ... | E05-S02 |
| FR-340 | P0 | Anxiety mode. When the median learner turn in the first two minutes is under 4 words, or ... | E05-S09 |
| FR-341 | P0 | Captions. The host's words are captioned by default (off in Controls); recast words are ... | E07-S07 |
| FR-342 | P0 | Failure. If live voice fails (connection, recognition or synthesis), the screen says ... | E05-S10 |
| FR-343 | P0 | Recording. The streaming transcript drives the conversation. After the call the audio is ... | E05-S03, E13-S05 |
| FR-345 | P1 | Round two. After the main call, one short call per episode, available until the session ... | E05-S13 (v1.1), E16-S04 (v1.1) |
| FR-346 | P1 | Dial-in experiment. A phone number the learner can call for the same call; works with the ... | E05-S13 (v1.1), E16-S04 (v1.1) |
| FR-350 | P0 | Nothing to read. The goodbye is a goodbye. Today marks the call as done with one honest ... | E07-S05 |
| FR-351 | P0 | Behind the scenes, the after-session pass (FR-80x) logs what the learner said; the errors ... | E09-S06 |
| FR-352 | P0 | Wins are said, not shown. A first-ever event that passed the claim gate (a structure used ... | E04-S02 |
| FR-360 | P0 | One long thread per host, across days, with date separators named after episodes. The ... | E07-S08 |
| FR-361 | P0 | The opener asks the learner to restate one point first (from the episode, the article or ... | E07-S08 |
| FR-362 | P0 | No margin note. When it helps, the host's reply says the learner's point back the natural ... | E07-S08 |
| FR-363 | P0 | Text only in v1. Each bubble sets its own text direction. | E07-S08 |
| FR-370 | P0 | Contents: the meaning in the learner's language for this sense, the sentence it came ... | E07-S03, E07-S06 |
| FR-371 | P0 | Glosses come from a shared cache keyed by lemma, sense and native language, generated ... | E04-S06 |
| FR-372 | P0 | Keep adds the word to the notebook and tells the teacher to bring it back in later ... | E03-S08, E07-S03 |

### Part 5

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-401 | P0 | Each episode is produced by a durable workflow with these steps, each with a timeout and ... | E04-S01 |
| FR-402 | P0 | The pipeline never fails to deliver: on any unrecoverable failure the fallback episode ... | E04-S04, E04-S13 |
| FR-410 | P0 | A lemmatizer splits the text into lemmas and known chunks; the word bank gives each a ... | E04-S03 |
| FR-411 | P0 | The fitter reports the new-word count, the share of new words from the top 3,000 lemmas ... | E04-S03 |
| FR-412 | P0 | 1 Level fit: The fitter passed. | E04-S03 |
| FR-413 | P0 | 2 Targets present: In every planned surface. | E04-S04 |
| FR-414 | P0 | 3 Language correctness: Grammatical, natural target language (for English, in the chosen ... | E04-S04 |
| FR-415 | P0 | 4 Memory: Every life fact used is confirmed, unexpired, not marked "don't bring up", and ... | E04-S04 |
| FR-416 | P0 | 5 Not generic: "Would this episode work unchanged for another learner?" Yes fails. | E04-S04 |
| FR-417 | P0 | 6 No unsourced world facts: No real-world result, statistic or news stated as fact unless ... | E04-S04 |
| FR-418 | P0 | 7 The fun carries the language: Every joke, twist and personal moment carries at least ... | E04-S04 |
| FR-419 | P0 | 8 Stands alone, 9 Variety: The episode can be understood without earlier episodes, even ... | E04-S04 |
| FR-420 | P0 | 10 Law scan: No game language, no grading, no explicit correction by anyone ("wrong" ... | E04-S04, NF-15 |
| FR-421 | P0 | 11 Pitch test: "Would this person, with this interest profile, choose this over a real ... | E04-S04 |
| FR-422 | P0 | On fail: Targeted repair of the failing part and one recheck. On a second fail, ship the ... | E04-S04, E04-S13 |
| FR-425 | P0 | Audio re-listen: The rendered audio is run back through speech recognition and compared ... | E04-S05 |
| FR-430 | P0 | Real input in every episode: at least one element that did not come from the model: the ... | E04-S11 |
| FR-431 | P0 | Ban list: stock names, settings and plots that AI stories converge on, kept per language ... | E02-S06, E04-S11 |
| FR-432 | P0 | Format rotation: formats are tracked over the last 10 episodes; no format runs three ... | E04-S09, E04-S11, NF-20 |
| FR-433 | P0 | Similarity check: each new script is embedded and compared with the learner's last 20 ... | E04-S11, NF-20 |
| FR-434 | P0 | Authored hosts: people write the hosts and Salma (drafted in content/bibles/, ADR-24.3) ... | E02-S07 |
| FR-435 | P0 | Shared ingredients, made once and shared across learners with no difference a learner can ... | E02-S07, E04-S06 |
| FR-436 | P0 | Review read: an AI review pass, separate from the editor's gate, reads 10 random episodes ... | E04-S13, E13-S10, E15-S08 |
| FR-437 | P1 | Offline test suite: 30 to 50 synthetic learners at different levels with planted error ... | E15-S03, E15-S10 |

### Part 6

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-501 | P0 | One authored host duo per target language; Karim and Mona are the English duo, shared by ... | E02-S07 |
| FR-502 | P0 | Voices: three candidate voices per host per accent, chosen by the blind listening test ... | E02-S03, E04-S10 |
| FR-503 | P0 | Changes after onboarding (voice swap or rename, through Salma or Controls) are announced ... | E04-S10, E15-S05 |
| FR-504 | P0 | Casting per episode: one host or both, chosen with the idea. In the call the learner ... | E04-S09 |
| FR-505 | P0 | Side characters: three to five recurring side characters per learner's world, created by ... | E03-S05 |
| FR-520 | P0 | One authored producer per native language, named and voiced for it (Salma in the Arabic ... | E02-S07 |
| FR-521 | P0 | Salma does: onboarding; life updates and "tell Salma an idea"; the notebook; the voice of ... | E10-S07, E10-S08 |
| FR-522 | P0 | Salma never: corrects, sends notes after a call, writes margin notes, performs in the ... | E13-S09 |
| FR-523 | P0 | Language balance: in season 1 at least 80% of Salma's words are in the learner's own ... | E05-S04 |
| FR-524 | P0 | Which voice and variety: per native language, chosen by a blind test with Muath and ... | E02-S03 |
| FR-540 | P0 | The series bible (per learner) is stored with the learner model and compiled into the ... | E03-S05, E04-S12 |
| FR-550 | P0 | Arcs: length 1 to 3 weeks; at most two open at once; best drawn from the learner's real ... | E04-S12 |
| FR-551 | P0 | An arc waits for the learner. Nothing in it happens while they are away; the next episode ... | E04-S12 |
| FR-553 | P0 | Mid-season rehearsal: when the season goal is a real scene (an interview, a call, a ... | E11-S08 |
| FR-555 | P0 | Seasons are 4 weeks. Season 1 starts on the onboarding day. A season cannot be broken: it ... | E04-S12, E11-S07 |
| FR-556 | P0 | One real goal per season in the learner's words, a learning goal, never a score; a goal ... | E06-S12, E11-S07 |
| FR-557 | LATER | A new season may bring a new format or a guest host to counter the novelty fade around ... | E16-S10 (later) |
| FR-560 | P0 | Salma says she is AI in her first lines in onboarding, and the hosts in theirs; host ... | E05-S04, E05-S11, E13-S09, NF-13 |
| FR-561 | P0 | No fake lives. The hosts' storylines are the show's fiction, inside the show, like a ... | E05-S11, E13-S09 |
| FR-570 | P0 | Every live role (host, Salma) and the after-session analyst watch for statements of ... | E05-S11, E13-S08 |
| FR-571 | P0 | On detection in a live call or chat: the show stops. In a call, the host stops and a ... | E05-S11, E13-S08, NF-13 |
| FR-572 | P0 | Every activation is logged for the annual reporting California SB 243 requires. Its ... | E05-S11, E13-S08 |
| FR-580 | LATER | Character creation, the six chassis, user-created hosts and guest hosts made by learners ... | none |

### Part 7

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-601 | P0 | The event log is the source of truth. Every transcript, tap, replay, skip, timing and ... | E01-S02, E03-S01 |
| FR-602 | P0 | Models propose, code decides. Model outputs are candidate updates in a fixed schema; code ... | E03-S01, E03-S09, E09-S04 |
| FR-603 | P0 | Each event carries: learner, session, door, type, time, payload, the model and prompt ... | E03-S01, E03-S08, E07-S04 |
| FR-610 | P0 | Word bank: Every lemma and multi-word chunk met: p(understood by ear), p(understood in ... | E03-S02 |
| FR-611 | P0 | Structure map: Each structure in the inventory: state (not seen, heard, attempting ... | E03-S03, E09-S11 |
| FR-612 | P0 | Error profile: Recurring errors by reporting category and structure, each with 2 or 3 ... | E03-S03 |
| FR-613 | P0 | Skills: Listening, reading, speaking and writing estimates, each with a range; speech ... | E09-S03, E09-S07 |
| FR-614 | P0 | Interests: Topic, salience, depth (curious, fan, expert), last engaged, dormant flag ... | E03-S05 |
| FR-615 | P0 | Life: Facts: text, exact source quote, session, time, confidence level, sensitivity ... | E03-S04 |
| FR-616 | P0 | Goals: Real situations as can-do statements ("handle a job interview in English"), the ... | E03-S05, E11-S07 |
| FR-617 | P0 | Taste: Format and host completion, what makes them talk most (learner words per minute by ... | E03-S08 |
| FR-618 | P0 | Show canon: Positions taken, running jokes, things said, side characters, open arcs (also ... | E03-S05 |
| FR-619 | P0 | C: Every number that is an estimate carries a range. | E03-S02, E09-S07 |
| FR-620 | P0 | Quote check: a life fact is stored only if its source quote appears word for word in the ... | E03-S04, E09-S05, NF-09 |
| FR-621 | P0 | Confidence ladder: said once: stored, never spoken, shown in the notebook as "I ... | E03-S04, E09-S05, NF-09 |
| FR-622 | P0 | Sensitivity: health, money, relationships, religion, politics and sexuality are sensitive ... | E03-S04, E10-S04, NF-09 |
| FR-623 | P0 | Time: each fact type has a shelf life (job: months; "sick this week": days). Expired ... | E03-S04, E09-S05 |
| FR-624 | P0 | Interests decay: salience falls over a few weeks without engagement; dormant interests ... | E03-S05 |
| FR-626 | P0 | Corrections: when the learner corrects the show, the host or Salma says so plainly ("My ... | E03-S10, E09-S10, E10-S04 |
| FR-630 | P0 | Rebuilds: when the analyst, edit classifier or measures change version, the after-session ... | E03-S11 |
| FR-640 | P0 | Teacher: Everything, summarized; the full due list; the structure map; the last 14 days ... | E03-S06 |
| FR-641 | P0 | Writer: The brief, up to two usable life facts with their quotes, the series bible ... | E03-S06 |
| FR-642 | P0 | Host (live): Position and pushback material, targets and their necessity moves, 2 to 4 ... | E03-S06 |
| FR-643 | P0 | Salma: Usable life facts with quotes, goals, the working-on list, claims that passed the ... | E03-S06 |
| FR-644 | P0 | Chat host: The call transcript summary, targets, the opener | E03-S06 |
| FR-645 | P0 | Proof producer: Claims that passed the gate, with their evidence; nothing else from the ... | E03-S06 |

### Part 8

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-701 | P0 | Triggers: after each session (once the after-session pass finishes, within 10 minutes) it ... | E04-S01, E09-S06 |
| FR-702 | P0 | Candidates are structures in the inventory and words in the word bank, scored on six ... | E04-S01 |
| FR-703 | P0 | Caps: 1 grammar target and 2 to 4 words per session; no target in more than 4 consecutive ... | E04-S01 |
| FR-704 | P0 | An error pattern enters targeting only after 3 observations across at least 2 sessions ... | E03-S03 |
| FR-706 | P0 | The "working on" list (notebook) shows at most 3 items in plain words. The learner can ... | E03-S10, E10-S01, E10-S02 |
| FR-707 | LATER | Exploration: 10 to 15% of target slots try a different treatment, recording which one ... | none |
| FR-710 | P0 | Treatment by learner state: never attempted but expected at their stage: input flood ... | E04-S01 |
| FR-720 | P0 | Review schedule: every word, chunk and structure has a review state in an FSRS-style ... | E03-S02 |
| FR-721 | P0 | Due items return through four channels: the same day across surfaces (episode, article ... | E04-S01 |
| FR-722 | P0 | New words: 3 to 6 planted per episode; at least 80% from the top 3,000 lemmas of a ... | E04-S01 |
| FR-723 | P0 | Words the learner tapped twice or more become recall candidates: the call brief creates a ... | E03-S08 |
| FR-730 | P0 | The edge. Difficulty is set per surface from the skill estimates by dials the fitter ... | E04-S03, NF-20 |
| FR-731 | P0 | One step easier for: the first three episodes, a return episode, low-energy signals ... | E04-S03 |
| FR-735 | P0 | Ideas and prediction: three ideas per day ranked by predicted choice (interest salience × ... | E04-S09 |
| FR-740 | P0 | Fallbacks: if the teacher cannot complete a brief (model failure, timeout), the brief is ... | E04-S01 |
| FR-741 | P0 | "Why this episode": for every episode the teacher writes 2 to 4 plain reasons, each ... | E04-S09, E10-S05 |

### Part 9

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-801 | P0 | Verbatim re-transcription of every learner audio turn (call, round two, shadow ... | E05-S03, E05-S12, E09-S01 |
| FR-802 | P0 | Analyst (small model, fixed schema): for each learner turn and chat message, the smallest ... | E09-S04 |
| FR-803 | P0 | Edit classifier (code): aligns original and corrected text, classifies each edit into the ... | E09-S02 |
| FR-804 | P0 | Confidence filter: edits inside speech regions below the recognizer confidence threshold ... | E09-S01 |
| FR-805 | P0 | Measures (code) on comparable segments (FR-810 to FR-812); updater (code): Bayesian ... | E03-S09, E09-S03 |
| FR-806 | P0 | Memory keeper (small model plus rules): life-fact candidates with quotes, interests ... | E09-S05 |
| FR-807 | P0 | The pass completes within 10 minutes of the call ending (NFR-112); its output feeds the ... | E09-S06 |
| FR-810 | P0 | Accuracy: Correct use in obligatory contexts per structure; errors per 100 words by ... | E09-S03 |
| FR-811 | P0 | Complexity and fluency: Clause length, subordination, lexical diversity (MTLD), share of ... | E09-S03 |
| FR-812 | P0 | Vocabulary, comprehension, pronunciation, word button | E05-S12, E09-S03 |
| FR-815 | P0 | C; subtitle corpus: PRD call: Structure inventory: for English, seeded from the English ... | E02-S06, E09-S02 |
| FR-820 | P0 | A pattern counts as an error, and can become a target, only after 3 observations across ... | E03-S03 |
| FR-821 | P0 | Lifecycle: Not seen → Heard (met in input) → Attempting (used at least once) → Active ... | E03-S09 |
| FR-822 | P0 | "Learned", in any claim, means correct, unprompted, at least a day later, in a different ... | E03-S09, E10-S03 |
| FR-823 | P0 | Avoidance: weekly, structures expected at the learner's estimate that they have never ... | E09-S11 |
| FR-845 | P0 | Four estimates (listening, reading, speaking, writing) on a fine internal scale anchored ... | E03-S07, E09-S07 |
| FR-846 | P0 | "Where do I stand?" When the learner asks, Salma answers per skill with a range and what ... | E09-S07 |
| FR-850 | P0 | The word check (onboarding, optional): 48 yes/no items, 36 real lemmas (6 from each of ... | E03-S07, E06-S05 |
| FR-851 | P0 record / P1 compare | The then-and-now recording: about 3 minutes of the learner's speech, the same task types ... | E05-S12, E09-S09, E11-S05 |
| FR-852 | P0 | The first "then" is offered after session 2 and again once in sessions 3 to 5 ... | E06-S12, E11-S05 |
| FR-840 | P0 | Every sentence about the learner's progress, in the proof, the finale, a host line or ... | E11-S01, NF-16 |
| FR-841 | P0 | Until a metric's standard error is estimated (from test-retest pairs collected after ... | E11-S01, E11-S06 (v1.1) |
| FR-842 | P0 | When nothing passes, the honest thing is said instead ("too early to tell"; "flat week ... | E11-S03 |
| FR-860 | P0 rule / P1 set | Calibration before metric claims, per language pair. The rule is P0: no metric claim ... | E09-S08 (v1.1), E11-S01, NF-19 |
| FR-861 | Retired | Retired (ADR-25.5): there is no external test. | retired |
| FR-862 | P0 (build phase 1) | The recognizer test: for each target language, learner clips from an open corpus with a ... | E02-S01, E02-S02, E09-S01 |
| FR-830 | P0 | During the call / Host: Clarification requests when meaning blurs; "you mean..." recasts ... | E05-S02 |
| FR-831 | P0 | During the call, on request / Host (word button): A word or a hint, because the learner ... | E05-S07 |
| FR-832 | P0 | Right after the call: Nobody: Nothing to read | E07-S05 |
| FR-833 | P0 | In the chat / Host: At most one "so you mean..." inside a normal reply | E07-S08 |
| FR-834 | P0 | Any time, on request / Host or Salma: "Why do we say it like that?" answered plainly | E07-S08, E10-S07 |
| FR-835 | P0 | Weekly / Salma: The proof: one headline, the next focus, the "working on" list; never a ... | E11-S03 |
| FR-836 | P0 | Across weeks / Teacher: The form returns in new episodes, spaced, and calls make it ... | E04-S01 |
| FR-837 | P0 | Every layer / All: Never "wrong", "mistake" or "correct"; never the learner's sentence ... | E05-S02, E13-S09, NF-15 |

### Part 10

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-901 | P0 | Every week, for every learner, on the learner's proof day: by default the weekday on ... | E11-S03 |
| FR-902 | P0 | Form: an audio episode of about 2 minutes presented by Salma, with the learner's own ... | E11-S03, E11-S04 |
| FR-903 | P0 | Contents, in order: (1) one headline piece of evidence that passed the claim gate, with ... | E11-S02, E11-S03, E11-S04 |
| FR-904 | P0 | Simple version at launch: headline from first-ever events and words owned, the next ... | E11-S03 |
| FR-905 | P0 | A slow week (no session or one) gets a shorter proof, about 45 seconds, about what has ... | E11-S03 |
| FR-906 | P0 | A flat week says so plainly and names the one thing the teacher is changing. A worse week ... | E11-S03 |
| FR-920 | P1 | The season finale: offered at the learner's first session on or after day 28 of the ... | E11-S09 (v1.1), E16-S04 (v1.1), E16-S06 (v1.1) |
| FR-921 | LATER | Longer windows: then-and-now compares 1 month, 3 months, and later 1 year; a ... | none |

### Part 11

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-1001 | P0 | Three tabs: Today (FR-235), Show, Notebook (Show from v1.1, FR-1002). The interface is in ... | E07-S01, NF-14 |
| FR-1002 | P1 | Show (the archive): a shelf of seasons, each a row of typographic episode covers. Every ... | E07-S11 (v1.1) |
| FR-1010 | P0 | What I'm working on with you: At most 3 items in plain words, each with one of the ... | E10-S01 |
| FR-1011 | P0 | About you: Every life fact, interest and goal Salma holds, each with its source ("you ... | E03-S10, E10-S04 |
| FR-1012 | P0 | Words you own: Each word with the learner's own sentence, date and ▶ audio. One quiet ... | E10-S03 |
| FR-1013 | P1 | The tape: The then-and-now recordings as tiles, one per season, with ▶ "Play then and ... | E10-S09 (v1.1), E16-S04 (v1.1) |
| FR-1015 | P0 | Out in the world: Real uses the learner reported ("I had the interview"), dated. Salma ... | E10-S05 |
| FR-1016 | P0 | Kept words and marked moments: Words kept from the word sheet; moments marked with the ... | E10-S03 |
| FR-1017 | P0 | Hours: "About 41 hours heard, 6 hours spoken." Hours heard count app playback, plus each ... | E10-S05, NF-14 |
| FR-1018 | P0 | Why this episode: Per episode, from the archive and from Today (FR-741), with "Something ... | E10-S05 |
| FR-1019 | P0 | Where do I stand: Not a page: asked of Salma (FR-846). | E09-S07 |
| FR-1020 | P0 | A short sheet, not a settings app; everything else is a sentence to Salma ("less ... | E10-S06 |
| FR-1022 | P0 | Delete account takes two taps, with no survey wall and no "Karim will miss you". Cancel ... | E10-S06, E12-S07, E13-S06 |
| FR-1040 | P0 | Voice storage on: call and recording audio kept, encrypted with per-learner keys, until ... | E13-S05 |
| FR-1041 | P0 | Voice storage off: audio is analysed and deleted within 15 minutes of the call (FR-343). ... | E05-S03, E11-S05, E13-S05 |
| FR-1042 | P0 | Revoking voice consent: the flag flips at once; all stored audio is deleted within 24 ... | E10-S06, E13-S05 |
| FR-1043 | P0 | Transcripts and text are always stored while the account exists (core function, disclosed ... | E13-S03 |
| FR-1044 | P0 | Opt-in data use: only with the Controls switch on (never asked during onboarding ... | E10-S06, E13-S07 (v1.1) |
| FR-1045 | LATER | The learner's cloned voice ("hear yourself say it fluently"): not offered in v1; tested ... | none |
| FR-1046 | P0 | Export: a full export (learner model in plain JSON, transcripts, kept audio) is prepared ... | E03-S11, E13-S06, E13-S11, NF-10 |
| FR-1047 | P0 | Account deletion: confirmed by typing "delete"; no grace period (ADR-24.B1); access ends ... | E03-S11, E13-S06, E13-S11, NF-10 |
| FR-1048 | P0 | Trial ended without paying: new episodes stop; the archive, notebook, export and delete ... | E12-S05, E12-S11 (v1.1), NF-10 |
| FR-1049 | P0 | Consent to process conversation content (ADR-25.9): an explicit consent at account ... | E06-S08, E13-S03 |
| FR-1050 | P0 | Security: encryption at rest and in transit; per-learner keys for audio, so deleting a ... | E01-S08, E13-S01, E13-S10, E15-S01, NF-28 |
| FR-1051 | P0 | Compliance by conservative design, before launch, with no counsel step (ADR-25.3). (1) ... | E02-S01, E13-S02, E13-S03 |

### Part 12

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-1100 | P0 | Everything language-specific is configuration, not code. A target-language package and a ... | E02-S06 |
| FR-1101 | P0 | The language gate (five checks). A target language opens when: (1) voices: Muath and ... | E02-S02, E02-S03, E02-S04, E02-S06, E02-S08 (v1.1), NF-27 |
| FR-1102 | P0 | A native language ships when Salma's voice passes the blind test with native-speaking ... | E02-S07, E02-S08 (v1.1) |
| FR-1103 | P0 | A target-language package contains: host bibles and voice pools per accent; the structure ... | E02-S06 |
| FR-1104 | P0 | A native-language package contains: Salma's bible and voice; gloss prompts; caption ... | E02-S07, E13-S08 |
| FR-1105 | P0 | Order of testing. Candidate targets, in order: English, then Spanish, French, German ... | E02-S06, E02-S09 (v1.1) |
| FR-1106 | P0 | Proof claims per target. English has an established structure inventory (built from open ... | E02-S06 |
| FR-1107 | P0 | Cost and closing rule. Each target needs a host duo's bibles, a voice test, a recognizer ... | E02-S06, E02-S08 (v1.1), E02-S09 (v1.1), E16-S07 (v1.1) |
| FR-1110 | Retired | Retired (ADR-25.5): there is no Milestone 0. Which targets open at launch is FR-1107. | retired |

### Part 13

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-1201 | P0 | Trial: 7 days, starting at account creation (FR-118), on the 2 a day plan, with no card. ... | E06-S08, E12-S03, E12-S05 |
| FR-1202 | P0 | Plans: 1 a day $19.99, 2 a day $29.99 ("Recommended", about $1 a day), 3 a day $44.99 ... | E12-S01, E12-S04 |
| FR-1203 | Retired | Retired (ADR-25.5, 25.10): there is no founding-member price lock and no 100 cap; every ... | retired |
| FR-1204 | P0 | Checkout through Paddle as merchant of record (OPEN-04, ADR-24.4): USD prices shown in ... | E12-S04, E12-S08 (v1.1) |
| FR-1205 | P0 | Plan changes take effect at the next drop (upgrade, with the charge prorated by Paddle) ... | E12-S10 |
| FR-1206 | LATER | Regional prices for lower-income countries, and a cheaper listen-first plan, once there ... | E12-S09 (later) |
| FR-1230 | P0 | Pricing psychology, within TC-2: three plans with the middle marked; the top plan as the ... | E12-S01 |
| FR-1231 | P0 | Never: fake countdowns, fake scarcity, hidden or hard cancellation, guilt, pre-ticked ... | E12-S01, E12-S10 |
| FR-1232 | P1 | Receipts and failures: receipts by email; a failed payment gets one plain email and a ... | E12-S11 (v1.1) |
| FR-1233 | P0 | Cancel keeps the show running until the end of the paid period; afterwards FR-1048 ... | E12-S07 |

### Part 14

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| NFR-101 | P0 | First open to first sound (Salma): Under 60 s | E06-S03, E06-S11, NF-02 |
| NFR-102 | P0 | Under 5 min: First open to the learner's first spoken target-language sentence | E06-S07, E06-S11, NF-02 |
| NFR-103 | P1 | Sample episode playable (FR-103): Under 30 s | E04-S08, E06-S01 (v1.1), NF-03 |
| NFR-104 | P0 | First-episode playback after the intake: Under 45 s | E04-S08, E06-S07, E06-S11, NF-02 |
| NFR-105 | P0 | Dropped episode start: Under 2 s | E01-S08, E07-S03, E07-S12, NF-03, NF-24 |
| NFR-106 | P0 | Under 30 s, streamed: On-demand episode (second of the day, swap, return) playable | E04-S08, E07-S09, NF-03 |
| NFR-107 | P0 | Host reply after end of learner turn: Under 1.5 s median, under 2.5 s at the 95th ... | E02-S04, E05-S01, E14-S06, NF-01, NF-24 |
| NFR-108 | P0 | Word-button answer: Under 2 s | E05-S07, NF-04 |
| NFR-110 | P0 | Word sheet: Under 300 ms | E07-S06, NF-04 |
| NFR-111 | P0 | Chat opener: Under 30 s | E07-S08 |
| NFR-112 | P0 | After-session pass and teacher update: Within 10 min of the call ending | E09-S06, NF-05 |
| NFR-113 | P0 | Tomorrow's episode: Ready before the drop time; batch falls back to on-demand at drop ... | E04-S07, E08-S02, E15-S04, NF-05 |
| NFR-201 | P0 | The learner always gets an episode at the drop time: pipeline failure ships the fallback ... | E04-S13, E15-S04, E15-S06, E15-S10, NF-22 |
| NFR-202 | P0 | Live voice failure falls back to voice notes in the same thread (FR-342); no session is ... | E05-S10, E15-S06, NF-21 |
| NFR-203 | P0 | A voice vendor outage switches to the second voice vendor within the same day's ... | E02-S05, E04-S05, E14-S07 (v1.1), NF-21 |
| NFR-204 | P0 | Every pipeline step is a durable workflow step with a timeout and retries; a partial run ... | E01-S04, E04-S06 |
| NFR-205 | P0 | Audio position, article scroll and chat history survive app restarts and device changes. | E07-S04, E07-S13 |
| NFR-206 | P0 | A model, prompt or vendor upgrade never changes a host's voice or personality silently ... | E02-S07, E04-S10, E09-S08 (v1.1), E15-S03, E15-S05, E15-S11 (v1.1), NF-18 |
| NFR-207 | P0 | Backup and restore: automated database backups kept 30 days with point-in-time recovery ... | E01-S09, NF-23 |
| NFR-301 | P0 | Encryption in transit and at rest for all learner data. | E01-S05, E01-S08, E13-S01, NF-28 |
| NFR-302 | P0 | Audio is encrypted with per-learner keys; deleting the key deletes the audio. | E01-S08, E13-S01, NF-12 |
| NFR-303 | P0 | Row-level isolation per learner; no cross-learner data path except the shared gloss cache ... | E01-S02, E13-S01, E13-S07 (v1.1), NF-28 |
| NFR-304 | P0 | Audio deleted within 15 minutes when voice storage is off; all audio deleted within 24 ... | E05-S03, E13-S05, E13-S06, E13-S11, NF-10 |
| NFR-305 | P0 | Feed URLs carry an unguessable token, are excluded from podcast directories and can be ... | E08-S01 |
| NFR-306 | P0 | Every model, voice and recognition call is logged with its cost and the learner-model ... | E01-S06, E14-S02, E15-S01, NF-11 |
| NFR-307 | P0 | Hosting region eu-central-1; cross-border transfers on standard contractual clauses with ... | E01-S05, E01-S09, E13-S02 |
| NFR-401 | P0 | Cost per session (everything one episode cycle uses: the teacher's share, writing ... | E14-S01, E14-S02, E14-S03, E14-S08, NF-06 |
| NFR-402 | P0 | The price rule: no plan may lose money on a learner who uses every episode at the ... | E14-S08, NF-06 |
| NFR-403 | P0 | Launch budget about $0.60 per session (the current itemized estimate on the recommended ... | E04-S07, E14-S03, E14-S04, E14-S06, E16-S08 (v1.1), NF-06, NF-08 |
| NFR-404 | P0 | Stop line: over $1.00 a session with no costed plan to reduce it. Scale target: $0.30 to ... | E14-S04, E14-S05, E14-S08, E16-S08 (v1.1), NF-06, NF-08 |
| NFR-405 | P0 | A learner on 2 or 3 a day who uses every episode costs more than they pay until the cost ... | E14-S08, NF-06 |
| NFR-406 | P1 | Sample episodes cost at most $0.05 each and are rate-limited (FR-103). | E04-S08, E06-S01 (v1.1), E14-S05, NF-07 |
| NFR-501 | P0 | No prompt or model change ships to the host, writer, editor or analyst without the ... | E01-S10, E15-S02, E15-S03, NF-18 |
| NFR-502 | P0 | Monthly human audit of proof claims by Muath, the claims auditor; false-claim rate under ... | E11-S10, E15-S09 (v1.1), E16-S05 (v1.1), NF-16 |
| NFR-503 | P0 | Monthly review read of 10 random episodes per learner for errors, sameness and law ... | E04-S13, E15-S08, NF-19 |
| NFR-504 | P0 | Recognizer error tracked by first language from day one; a language whose quality falls ... | E02-S02, E15-S07, E15-S09 (v1.1), E16-S07 (v1.1) |
| NFR-505 | P0 | Every "why this episode" reason is traceable to a learner-model record; every claim is ... | E04-S09, E11-S01, E11-S02 |
| NFR-601 | P0 | Right-to-left layout for native languages written right to left; every text block sets ... | E07-S01, NF-25 |
| NFR-602 | P0 | Captions on calls, a word-synced transcript on episodes and read-aloud on articles, so ... | E07-S03, E07-S06, E07-S12 |
| NFR-603 | P0 | The app is usable with one thumb on a phone during a commute: one hero, large buttons ... | E05-S06, E07-S07, E07-S12, NF-26 |
| NFR-604 | P0 | Dark mode is first-class; every surface meets WCAG AA contrast in both themes. | E07-S01, E07-S12, NF-26 |
| NFR-605 | P0 | Every native-language string, gloss and caption passes a native speaker's check before ... | E02-S07, E02-S08 (v1.1), NF-27 |

### Part 15

| Id | Priority | Requirement (short) | Stories |
|---|---|---|---|
| FR-1301 | P0 (roster, in v1) | Teacher: Reads the learner model; targets, due words, arcs, the weekly mix, tomorrow's ... | E04-S01 |
| FR-1302 | P0 (roster, in v1) | Writer: Script, article, call brief, chat opener, recap, shadow lines | E04-S02 |
| FR-1303 | P0 (roster, in v1) | Fitter: Coverage, targets, new-word budget; sends failing sentences back | E04-S03 |
| FR-1304 | P0 (roster, in v1) | Editor: The gate (FR-412 to FR-422) | E04-S04 |
| FR-1305 | P0 (roster, in v1) | Voice studio: Two-voice audio, read-aloud, timestamps, names, re-listen | E04-S05 |
| FR-1306 | LATER (roster) | Scout: Results and news for stored interests, shared per topic | none |
| FR-1307 | P0 (roster, in v1) | Host: The call (FR-32x to FR-34x), the word button, the chat (FR-36x) | E05-S01 |
| FR-1308 | P0 (roster, in v1) | Producer (Salma): Onboarding, life updates, "tell Salma an idea", the notebook, the ... | E05-S04 |
| FR-1309 | LATER (roster) | Observer: Reads each learner turn and whispers to the host what to recast or draw out ... | E16-S10 (later) |
| FR-1310 | P0 (roster, in v1) | Analyst: FR-801 to FR-802 | E09-S04 |
| FR-1311 | P0 (roster, in v1) | Memory keeper: Life facts with quotes, interests, goals, canon | E09-S05 |
| FR-1312 | P0 (roster, in v1) | Proof producer: Scripts the proof and finale from gated claims; picks clips | E11-S03 |
| FR-1313 | P0 (roster, in v1) | Recording rater: Rates the then-and-now recording, calibrated per pair | E09-S09 |
| FR-1320 | P0 | Code, not AI: the review scheduler; the lexicon (lemmatizer, frequency list, word ... | E03-S02, E09-S02, E11-S01, E14-S02 |
| FR-1321 | P0 | Live roles never write to the learner model; only after-session roles write, from the ... | E01-S02, E03-S09 |
| FR-1322 | P0 | Every vendor sits behind a thin adapter so a swap is configuration; two voice vendors are ... | E02-S05, E14-S07 (v1.1) |
| FR-1323 | P0 | The editor runs on a different vendor from the writer. | E04-S04 |
| FR-1324 | P0 | The call host uses the episode vendor's low-latency voice so the host sounds the same in ... | E02-S03 |
| FR-1325 | P0 | A durable workflow engine calling model APIs directly; no agent framework in the ... | E01-S04 |
| FR-1326 | P0 | Vendors known to be shutting down are not used; known price events (several Gemini 3.8 ... | E02-S05, E14-S01, E16-S08 (v1.1) |
| FR-1330 | P0 | Voices: For each candidate target, Muath and volunteers (a few listeners, learners of the ... | E02-S03 |
| FR-1331 | P0 | Recognizers: The 30-clip test (FR-862). | E02-S02 |
| FR-1332 | P0 | Call latency: 50 scripted test calls; median host reply under 1.5 seconds after end of ... | E02-S04 |

## 3. P0 requirements with no story

None, and none rests only on v1.1 stories.

## 4. P1 requirements with no story

None. The P1 requirements and their stories: FR-102 (E06-S01); FR-103 (E04-S08, E06-S01); FR-104 (E06-S01); FR-318 (E16-S04); FR-345 (E05-S13, E16-S04); FR-346 (E05-S13, E16-S04); FR-437 (E15-S03, E15-S10); FR-920 (E11-S09, E16-S04, E16-S06); FR-1002 (E07-S11); FR-1013 (E10-S09, E16-S04); FR-1232 (E12-S11); NFR-103 (E04-S08, E06-S01, NF-03); NFR-406 (E04-S08, E06-S01, E14-S05, NF-07).

**LATER requirements** are direction only. 5 have no story by design: FR-580, FR-707, FR-921, FR-1045, FR-1306. The others are cited by LATER stories (E12-S09 regional prices, E16-S10 the plan after the 8-week review).

**Retired requirements** (ADR-25.5), cited by no story: FR-105, FR-106, FR-861, FR-1110, FR-1203.

## 5. Stories with no requirement

| Story | What it enables |
|---|---|
| E01-S01 Monorepo with CI and local compose | The repository, CI and local compose every other story is built in. |
| E01-S03 API skeleton with OpenAPI codegen | The versioned api skeleton and the generated client. |
| E01-S07 Staging deploy pipeline and canary episode | The staging deploy pipeline and its canary; the canary's alerting serves NFR-201 through E15-S10. |
| E13-S12 Incident runbook and tabletop | The security incident runbook and the tabletop, including when a lawyer becomes necessary (ADR-25.3). |
| E16-S02 The daily rhythm after launch | The morning checklist and weekly digest after launch: operations, not a product requirement. |
| E16-S09 Launch health reviews at 4 and 8 weeks | The health reviews at 4 and 8 weeks. They read the GATE ids of PRD Part 16, which are measures, not FR or NFR ids. |

## 6. What changed on 2026-11-12 (ADR-25)

- **Ids cited but not defined in PRD-v3:** none.
- **Removed stories:** E06-S10 (Apple and Google sign-in), E12-S06 (the founding-member lock), E13-S13 (deletion and export by runbook; the automated jobs are v1), E16-S03 (the external test). Their ids are not reused.
- **Rewritten for no trial run before launch (ADR-25.6):** E02-S01 to S04 (volunteer clips, speechocean762, a blind test by Muath and volunteers, agent-written scripted calls), E15-S02 (synthetic fixtures), and every acceptance criterion that replayed Milestone 0 data now replays synthetic learners with planted truth (E03-S02, S04, S07, S09, E04-S04, S10, E05-S02, E09-S01 to S06, E14-S08). E06-S02 is open signup; E06-S11 is the launch rehearsal; E16 is "Launch and the first season".
- **Added:** E01-S10, the coding agent's workflow (instructions file, tests first, an independent AI review in CI, Muath's approvals; ADR-25.2). Acceptance criteria for FR-1049 (the conversation-content consent) in E06-S08 and E13-S03, FR-860's rule in E11-S01, and FR-306 through the feed in E08-S01.
- **Later the same day:** the onboarding episode is "the first episode" and its kind is `first` (ADR-24.B34); a price rise applies to new signups only (ADR-25.10, in E12-S01); security is tested without a paid penetration test (ADR-25.11: NF-28, E01-S10, E13-S12).
- **Releases follow the PRD's priorities:** a story is v1 when it implements a P0 requirement, v1.1 when everything it implements is P1; story priority now equals release (P0 is v1, P1 is v1.1).

