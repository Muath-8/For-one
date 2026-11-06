# 4. Hand-made production: the episode, the call and the learner file

*Milestone 0 pilot kit. Updated 23 October 2026 for invisible teaching (no correction notes) and learners from any country. How one person makes a personal episode, a call and the producer's messages for 15 learners a day, with the tools available today and no product code. Prompts are in [05-prompts.md](05-prompts.md); the daily checklist is [08-runbook.md](08-runbook.md).*

## What the learner gets each day

The concept's session (episode, article, call, chat) cut down to what WhatsApp and off-the-shelf tools can carry. Muath's own hour was 30 minutes listening, 15 reading, 5 speaking and 10 writing; this is a smaller version of the same four parts.

| Part | What it is in Milestone 0 | Skill | Time for the learner |
|---|---|---|---|
| The episode | 5 to 7 minute two-host audio (Karim and Mona), sent on WhatsApp at the learner's slot. Ends on an open question. | Listening | 6 min (more if replayed) |
| The article | 220 to 320 words of "show notes" in the same WhatsApp drop: the facts and both sides of the question | Reading | 3 to 5 min |
| The call | 4 to 6 minutes with Mona through a link: argue the question, a 60-second retell, recall gaps | Speaking | 5 min |
| Write to the show | One question, answered in 3 to 5 sentences on WhatsApp; the hosts may read it on air next time | Writing | 3 to 5 min |
| Salma's message | In the evening, in the learner's message language, only when there is something to send: the 3 ideas before a personal episode, one line before a generic one, and answers to anything the learner asked. Never anything about their English | Choosing | 1 min |

The learner reacts to the episode audio once they have listened: ❤️ loved it, 👍 good, 😐 meh. The reaction is both the listening record and the cheapest daily rating.

**How the teaching works now (concept v2, law 7; Muath's decision 3).** Nobody tells the learner they were wrong, and nobody sends correction notes. The learner's errors still drive everything, quietly:

1. **In the call**, Mona recasts the way a friend would ("oh, you went there yesterday?") and carries on, or asks "sorry, you what?" when the meaning is lost.
2. **In the evening**, the analyst picks at most 3 **errors to echo** and adds them to the learner file's echo list.
3. **In the next episodes**, the writer puts the right form of each one into the hosts' ordinary lines, at least twice, and Mona's brief carries the same forms. The editor fails any line that quotes or contrasts the learner's mistake.
4. **Every session**, the analyst counts how often each echoed form was needed and how often it was still wrong. That count is gate 8: "the errors the show echoed back appear less often by day 14" (concept v2, section 9).
5. **Explanations only when asked.** If a learner asks "why?" or "what are you working on with me?", Salma answers plainly, in their language.

**Concept laws kept literally:** formats are hijacked, not invented (law 6); teaching is invisible (law 7); no streaks, counters, points or scores anywhere (law 1); the story waits for the learner (law 4). **Changed for Milestone 0:** one new episode a day for everyone (the 1, 2 and 3 a day plans start with the beta); the chat with a host is replaced by "write to the show", because a person typing as an AI host is neither honest nor feasible for 15 people.

**Salma in the pilot.** Concept v2 keeps a producer, Salma, as the face of the app in the learner's own language who never corrects. PRD v2 (3.1) removes the producer from the product. The pilot keeps her small: the evening choice and answers when asked, so the gate report can say whether a third voice earned its place.

## Tools, chosen

Where a lens recommended a tool, it is used. One deviation, explained below.

| Job | Tool | Lens recommendation | Approximate cost for the pilot |
|---|---|---|---|
| Teacher and writer (plan, script, article, call brief) | **Claude** on claude.ai, a Project called "M0 Writer" with the writer prompt as its instructions; use the strongest model offered | Architecture lens: "prompts in a chat model, run by hand"; Opus-class teacher, Sonnet-class writer | Claude Max for the month (Pro is likely to hit usage limits at 15 learners, about 30 long chats a day) |
| Analyst (errors to echo, echo check, Salma's message) | **Claude**, a second Project "M0 Analyst" | Same | Included |
| Editor (pre-ship check) | **Gemini 3.8** in Google AI Studio, the editor prompt saved as a system instruction | Concept v2: the editor runs on a different vendor from the writer | Cents |
| Episode audio | **Gemini 3.8 Flash TTS**, two speakers, in AI Studio's speech playground, or the kit's script [tools/episode_audio.py](tools/episode_audio.py) | Voice lens and concept v2, Milestone 0 column | Cents per episode |
| The call | **ElevenLabs Agents**, one agent per learner, opened from a share link, turn-taking set to Patient | Voice lens: Gemini 3.8 Live with long silence settings; concept v2: "Gemini Live or a phone line". **Deviation, see below.** | ElevenLabs Pro, $99 a month, includes about 1,238 call minutes (15 learners x 14 calls x 6 minutes is about 1,260); check overage on the live page |
| Verbatim transcript of each call | **ElevenLabs Scribe v2** (speech to text in the same account), keeping fillers and restarts | Voice lens: "AssemblyAI with disfluencies, or ElevenLabs Scribe v2, checked by hand" | Included in credits |
| Coverage check (are 95% of the words known?) | **The kit's coverage checker** page, [tools/coverage-checker.html](tools/coverage-checker.html) | Personalization lens: "a coverage script run on every hand-checked episode" | Free |
| Delivery and chat | **WhatsApp Business app** on a second number named "For one" | Business lens | Free (needs a second SIM or eSIM) |
| Learner file | **One Google Doc per learner** ([learner-file-template.md](learner-file-template.md)) plus **[pilot-tracker.xlsx](pilot-tracker.xlsx)** opened in Google Sheets | Concept v2 stack: "a spreadsheet and a shared doc" | Free |
| Forms (screening, consent, check-ins) | Google Forms | | Free |

**Why the call is not on Gemini Live.** Gemini 3.8 Live is the lens's pick because it can use the same voices as the episode. But giving 15 people a link to it, with each person's brief loaded fresh every day, needs a small hosted web page holding an API key: that is product code, and it would have to be written and tested before the pilot starts. ElevenLabs Agents gives every agent a shareable link with no code, a per-agent prompt Muath can paste into each evening, a "Patient" turn-taking setting and a "take turn after silence" timer of up to 30 seconds (the lens wanted long silences so learners can search for words), and it keeps the audio and transcript of every call. The cost is that Mona's call voice will differ from her episode voice. Pick the ElevenLabs voice closest to the Gemini voice chosen for Mona, and have every episode end with Mona saying she is waiting for the call. If the voice mismatch bothers learners (ask on day 7), the beta pipeline in concept v2 fixes it. Fallback if a learner's link fails: voice notes, as the voice lens suggests (the learner sends a voice note answering the question; Muath runs it through the analyst like a call).

**No private podcast feed in Milestone 0.** Concept v2 lists one for Milestone 0, but it means 15 private shows to set up before the pilot starts, and WhatsApp already plays audio with the phone locked. The day-14 survey asks whether learners would rather get the show in their podcast app, which is the evidence decision 7 needs for the beta.

## One-time setup (Saturday 24 to Thursday 29 October)

1. **Second WhatsApp number.** Install WhatsApp Business with a second SIM or eSIM. Profile name "For one", a plain logo, the description "Your own English show. A pilot. / برنامجك الخاص بالإنجليزية. تجربة." Create one chat label per learner (L01 to L15).
2. **Google Drive.** A folder "For one M0" with a subfolder per learner (L01 to L15, R1 to R3). In each: the learner file (a Google Doc copied from [learner-file-template.md](learner-file-template.md)), and folders `episodes`, `calls`, `recordings`. Upload [pilot-tracker.xlsx](pilot-tracker.xlsx) and open it as a Google Sheet.
3. **Claude.** Settings, Privacy: turn "Help improve Claude" off. Create two Projects:
   - **M0 Writer**: paste prompt W (writer) from [05-prompts.md](05-prompts.md) into the project instructions; add the show bible (section S) and the generic topic pool (section G) as project files.
   - **M0 Analyst**: paste prompt A (analyst and producer) into the instructions; add the show bible.
4. **Google AI Studio.** Sign in with a Google account whose Cloud project has billing turned on (that makes AI Studio a paid service under the Gemini API terms, so prompts are not used to improve Google's products). Create a saved prompt "M0 Editor" with prompt E as the system instruction. Create an API key in the same project if you will use the audio script.
5. **Pick the voices (30 minutes).** In AI Studio's speech generation, two-speaker mode, try a few voices for Karim (for example Puck, Charon, Orus) and Mona (for example Aoede, Kore, Leda) on the first 10 lines of the sample script in [05-prompts.md](05-prompts.md#sample-script-for-voice-tests). Choose one pair, write it in the show bible. Then in ElevenLabs pick the voice closest to your Mona.
6. **ElevenLabs.** Subscribe to Pro. Check the workspace's privacy settings and turn off any use of content for training. Build one agent, "Mona (template)", from prompt H in [05-prompts.md](05-prompts.md):
   - Voice: the Mona match. Language: English. For each learner's agent, add their first language as an additional language only if a test shows the agent still answers in English when you say a word in that language (prompt H tells it to); otherwise leave English only.
   - LLM: the newest Claude Sonnet the menu offers (the architecture lens's Sonnet-class host); if none, the newest Gemini Flash.
   - First message: `Hey {name}! Mona here. So, you heard the episode. Where are you on this?` (write the learner's name in, per agent).
   - Turn eagerness: **Patient**. Take turn after silence: **12 seconds**. Interruptions: on. Max conversation duration: **480 seconds**. Authentication: off, so the share link works without an account. Keep conversation audio.
   - Duplicate it 15 times: "Mona L01" to "Mona L15". In each, the brief's FIRST LANGUAGE and EMERGENCY NUMBER lines come from that learner's file. Open each share link on your own phone in a private browser window to check it works without signing in.
7. **Forms.** Screening (from [01-recruiting.md](01-recruiting.md)), consent (from [02-consent.md](02-consent.md)), the day-7 and day-14 check-ins (from [07-measures-and-gates.md](07-measures-and-gates.md)).
8. **Then-and-now audio.** Generate the two story recordings from [06-then-and-now.md](06-then-and-now.md) once (single voice, slow and clear), and save them.
9. **Dry run (Thursday 29 October).** Make yourself learner L00: fill a learner file about yourself, run one full evening cycle (analyst on a test call, writer, coverage, editor, audio, agent brief) and time it. If one cycle takes more than 25 minutes, read the "if it takes too long" section below before accepting 15.

## Intake

One 10 to 15 minute call (or voice notes, if the learner prefers) with Muath himself, on Saturday 31 October or Sunday 1 November, at a time that suits the learner's time zone. Muath speaks as himself, the person running the pilot: this keeps "the producer is AI" honest. Fill the learner file during the call.

1. **How it works (2 minutes).** Every day except your day off: an episode at your time, a short read, a 5-minute call with Mona, a question to write back. Nobody will correct you or test you: the hosts just talk with you, and the show quietly works on what you need. If you ever want to know what it is working on, ask Salma. On the evenings before your own episodes, Salma sends three ideas to pick from. React to the episode once you've listened: ❤️ loved it, 👍 good, 😐 meh. Some days the episode is your pick, other days the hosts pick a general topic: we are testing which you like more. Never take the call while driving.
2. **Three questions** (UI/UX lens): What should Karim and Mona call you? (Hear the pronunciation.) What could you talk about for an hour? What do you need English for, and by when? Turn the last answer into a two-week goal in their own words ("get through the first five minutes of an interview without freezing").
3. **Two language moments, not a test.** Say one English sentence at normal speed and ask what they heard, in any language. Then: "Say anything back in English. Anything is fine." Note how it went.
4. **The anchor** (consistency lens): "What do you already do every day that this could follow? Where will you be? And if that moment doesn't happen, when instead?" Write it as an if-then plan: "After I park at work at 7:40, I play the episode. If I'm late, at lunch." Pick the drop slot (06:30, 12:30, 17:30 or 21:00) and the weekly day off.
5. **Hosts' accent:** British or American.
6. **Anything the show should never bring up.** Then the practical details: confirm their time zone and drop slot in their own time, the language they want Salma's messages in, and their local emergency number (look it up beforehand and check it with them).
7. **The gap note**, if they opted in on the consent form: "Write one message to yourself, in any language. If you're away for [3/5/7] days, it's sent to you once."
8. **The first recording.** Send the week-0 then-and-now task right after the call ([06-then-and-now.md](06-then-and-now.md)); ask for it the same day, before the first episode.

Voice-note version: send the questions as three short voice notes or texts in the learner's message language; the learner answers with voice notes.

## The learner file

Each learner's Google Doc is the show's memory, the only thing Claude sees about them, and the source of every callback. The tracker sheet is only for measurement. The rules come from the personalization, architecture and assessment lenses:

- **Told, not inferred.** A life fact goes in only with the learner's exact words, the date and where they said it. Facts the analyst proposes stay "unconfirmed" until Muath checks them against the recording; only confirmed facts reach a host's mouth.
- **Live roles never write.** Mona's agent and the writer read the file; only the evening analyst step proposes changes, and Muath pastes them in.
- **A wrong memory is a bug.** If a learner says "that's not right", fix the file that evening, mark the Wrong memory column in the tracker and note it in the file's Flags section.
- **Each role gets what it needs.** Paste the whole file into the analyst and writer chats (it is small), but only the brief into Mona's agent.
- **Words come back on a schedule.** A target word returns in the next two episodes, then about 3 and 7 days later, until the learner uses it unprompted in two different sessions (then it is "owned" and stops being scheduled). Each episode carries 1 grammar target and 2 to 4 due or new words, and no target runs more than 4 sessions in a row (assessment lens).
- **Echoes run until used.** An echoed error stays on the echo list until the learner uses the right form unprompted in two different sessions; then it is marked USED and the writer stops planning it. At most 3 echoes per episode.
- **"Learned" means later.** A word or structure counts as learned only when used correctly, unprompted, at least a day later, in a different session (settled point in decisions.md).

## The daily cycle

Muath's times are Saudi time; each learner's slot is converted to their own time in the learner file. The learner's day starts at their slot; Muath's production happens the evening before (his evening).

```
Evening (from 20:00)                    Next day
analyse today's calls  ─┐
Salma's message         ├─ write ─ check ─ voice ─ load brief ─┐   06:30 / 12:30 / 17:30 / 21:00
(3 ideas if next is     │                                       └─► drop on WhatsApp ─► listen, read,
   a personal episode)  ─┘                                                               call, write
```

**Make a new episode only after the learner did something with the last one** (reacted, called or wrote). If they did nothing, send nothing new at their slot: the last episode is still waiting (law 4, the story waits). After 3 or more days with no session, the next episode is a return episode (writer mode RETURN). If they opted in, the gap note goes out once on the day they chose, with no follow-up.

### Personal and generic days

The personalization lens's test: does "about you" beat "at your level"? Within each learner, alternate.

| Episode | Odd IDs (L01, L03...) | Even IDs (L02, L04...) |
|---|---|---|
| 1 (the pilot, day 1) | PILOT, personal, 2 to 3 minutes | PILOT, personal, 2 to 3 minutes |
| 2, 4, 6, 8, 10, 12 | PERSONAL | GENERIC |
| 3, 5, 7, 9, 11, 13 | GENERIC | PERSONAL |
| Last (day 14) | FINALE, personal | FINALE, personal |

A **generic** episode has the same hosts, format, length, level and target words, on a topic from the generic pool, with no name, no life facts and no callbacks to the learner's life. The learner knows the hosts pick that day's topic ("tomorrow is the hosts' pick"). The 3 ideas are offered only before personal episodes, and the episode number counts episodes made, not calendar days, so a skipped day does not break the alternation. Pilot and finale are left out of the comparison.

### Evening, step by step (per learner who had a session today)

Process all learners through one step before moving to the next; the model works while you move on.

| Step | Do | Tool | Minutes |
|---|---|---|---|
| 1. Collect | Download today's call audio from the agent's history to `calls/`. Run it through Scribe v2 with speaker separation; copy the transcript. Copy any written reply, voice-note transcript and any question the learner asked the show. Mark the day in the tracker (reacted, called, wrote, unprompted asks). | ElevenLabs, WhatsApp, tracker | 3 |
| 2. Analyse | New chat in M0 Analyst. Paste: the learner file, today's call brief, the Scribe transcript, the written reply, the learner's questions, and whether the next episode is personal. | Claude | 2 + model time |
| 3. Check and send Salma's message | If the analyst wrote NONE, send nothing. Otherwise check that nothing in it mentions their English or their mistakes, then send. Check the ERRORS TO ECHO against the recording: is the quoted error really what they said, not a transcription slip? Drop any you can't hear. | WhatsApp | 2 |
| 4. Update the file | Paste the analyst's learner-file changes into the doc, including new echo-list items. Confirm or drop proposed life facts (listen to the moment). Copy the measures into the Daily tab and the ECHO CHECK rows into the Echoes tab. | Google Docs, tracker | 4 |
| 5. Write | Wait for the learner's pick until 22:00 (if none, use the analyst's recommended idea). New chat in M0 Writer: paste the learner file, the mode (PERSONAL, GENERIC, RETURN, PILOT or FINALE), the pick or generic topic, and today's analysis (NEXT TARGETS, ERRORS TO ECHO, NEW FOR YOU). | Claude | 2 + model time |
| 6. Coverage | Paste the script into the coverage checker with the learner's vocabulary estimate and the planned new words. Under 95% for the script or 98% for the article: send the flagged sentences back to the writer to rewrite (at most twice). | Coverage checker | 2 |
| 7. Edit | Paste the package into M0 Editor in AI Studio. Fix anything it flags, by asking the writer chat or by hand. | Gemini | 3 |
| 8. Read it yourself | Would this person pick this over a real podcast? Is every callback true and confirmed? Anything they asked never to hear? Would anything feel like a correction if you were them? | You | 3 |
| 9. Voice | AI Studio speech playground, two speakers, the chosen voices; or put the script in a text file and run `episode_audio.py`. Save `episodes/L03-ep05.mp3`. Listen to the first 30 seconds and one random minute. | Gemini TTS | 3 |
| 10. Load the call | Paste the CALL BRIEF section into the learner's Mona agent, replacing yesterday's. | ElevenLabs | 1 |
| 11. Queue | Put the drop messages for tomorrow in a note grouped by slot. | Notes app | 1 |

About 25 minutes per learner by hand, less with batching and the audio script. At 15 learners with everyone active that is 5 to 6 hours an evening; in practice expect 10 to 12 active a day.

**If it takes too long:** in this order, (1) use `episode_audio.py` for all voicing, (2) skip step 7 on generic days, (3) run Scribe only on alternate days per learner and use the agent's own transcript for planning on the others (it smooths grammar, so do not tag errors from it), (4) start with 12 learners and keep 3 as reserves who start on day 3. Do not drop step 8.

## WhatsApp messages

All from the show's number. Hosts speak English; Salma and the show's own messages use the learner's message language. Arabic and English are below; for any other language, have the M0 Analyst translate the English once and keep it in the learner file.

**The drop** (three messages at the learner's slot):

1. The episode audio file, named like a show: `For one – Ep 5 – The interview nobody wanted.mp3`
2. The article:
   ```
   📖 [Article title]
   [Article text]
   ```
3. The actions:
   ```
   🎧 عندما تنتهي من الحلقة، تفاعل عليها: ❤️ أعجبتني جداً، 👍 جيدة، 😐 عادية.
   📞 كلّم منى عندما تكون جاهزاً (٥ دقائق، وليس أثناء القيادة): [share link]
   ✍️ اكتب للبرنامج: [writing question, in English]
   ```
   ```
   🎧 When you've finished the episode, react to it: ❤️ loved it, 👍 good, 😐 meh.
   📞 Call Mona when you're ready (5 minutes, not while driving): [share link]
   ✍️ Write to the show: [writing question]
   ```

**Salma's message** (evening, from the analyst, only when there is something to send). It never mentions the learner's English.

Before a personal episode:
```
مساء الخير [الاسم] 👋 حلقة الغد لك أنت. اختر واحدة أو اقترح فكرتك:
1) [idea]
2) [idea]
3) [idea]

سلمى، منتجة البرنامج (ذكاء اصطناعي)
```
```
Good evening [name] 👋 Tomorrow's episode is yours. Pick one, or suggest your own:
1) [idea]
2) [idea]
3) [idea]

Salma, the show's producer (AI)
```

Before a generic episode: `غداً يختار كريم ومنى الموضوع 🎙️` / `Tomorrow, Karim and Mona pick the topic 🎙️`

When the learner asked something: the analyst's short answer, signed the same way. Example for "what are you working on with me?": "Right now the show is working on telling stories about the past, and on two words for your interview: *responsible* and *deadline*. You can change this any time."

**Day off:** nothing is sent. If the learner asks for an episode on their day off, make one (it counts as an unprompted ask in the tracker).

**After a gap:** the gap note (if opted in) goes once, as the learner wrote it, with nothing added. The next episode is a return episode. Nobody mentions the days missed.

**If a learner wants to stop:** "تمام، شكراً على وقتك 🙏 إذا أردت أن نحذف بياناتك أخبرني وسأحذفها خلال ٧ أيام." / "Of course, thank you for your time 🙏 If you'd like your data deleted, tell me and I'll delete it within 7 days." Ask one optional question: "إذا لم يكن لديك مانع، ما أكثر شيء لم يناسبك؟" / "If you don't mind, what suited you least?" Record the answer; it is the most valuable data in the pilot.

## When something goes wrong

| Problem | Do |
|---|---|
| Call link does not open | Send the voice-note fallback: "Record a voice note answering Mona's question: [question]. Talk for 2 to 3 minutes." Treat it as the call. |
| A learner says a callback is wrong | Fix the learner file tonight, log it as a wrong memory. Next episode: one line from a host, "We got that wrong, sorry", and move on. |
| A learner says something distressing or about self-harm | Mona's prompt steps out of the show and points to help. Muath reads the transcript the same evening, replies personally and kindly as himself, and does not continue the show's content on that topic. If there is immediate danger, encourage calling their local emergency number (learner file). |
| A learner complains about feeling tested, corrected or watched | Thank them, change what they name (fewer recasts, no recall gaps, fewer echoes), log it. It is evidence about the design, and the check-ins ask about it. |
| A learner asks for corrections ("please tell me my mistakes") | Concept v2 says explanations come only when asked, so answer that one request as Salma: the learner file's Working on list and the right forms on the echo list, plainly, without quoting their sentences. Log it in the Changes tab; how many people ask is evidence about decision 3. |
| The audio has a glitch or mispronounced name | Regenerate the line or the whole episode; for names, spell them phonetically in the script (for example "Fy-sal"). |
| Muath is sick or misses an evening | Send each learner one line: "Tomorrow's episode is a day late. The show waits for you, and today it's waiting for us." No other apology. |
