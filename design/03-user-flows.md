# For one — 03. User flows

*Part 3 of 8. Each flow is a numbered sequence of steps with the mode (Ears / Voice / Eyes), what the learner hears and sees, the branch points, and the failure paths. Screens are specified in 04-screen-specs.md; the numbers here (A1, B3…) match the screen ids there. The example learner is Faisal (Arabic, learning English, hosts Karim and Mona, producer Salma); nothing is tuned to his country.*

Flows: A first session (two orders) · B daily episode · C the call · D after the session · E weekly proof · F season finale · G subscribe and paywall · H cancel · I data and deletion · J return after a gap · K the small door · L the sample page (before signup)

---

## Flow A. The first session, order A: sound within a minute, account after the first call

Target timings: first sound < 60s · first spoken sentence < 5 min · account at ~9 min · total 8 to 11 minutes.

| # | Step | Mode | What happens | Branches and failures |
|---|---|---|---|---|
| A1 | **Open** | Eyes, 5s | One screen in the phone's language: wordmark, one line ("Your own show, in English."), target language as a short list if more than one has passed the gate, an age checkbox, **Start**, and a quiet "I already have a show". | Under 18: a plain sentence, no door. Phone language not supported for the interface: English interface, Salma asks which language she should speak. |
| A2 | **Mic primer** | Eyes, 5s | "Salma, your producer, will talk with you for 3 minutes. You can talk back or type." **Talk** / **Type**. The mic permission appears only after Talk. | Mic refused: continue by typing; Salma's voice still plays. No audio output (muted phone): a one-line system toast "Turn your sound on to hear Salma". |
| A3 | **Meet Salma** | Voice, ~3 min | Salma speaks in the learner's language; live captions under her orb. Three questions: what should the hosts call you (she repeats the name so the hosts learn it), what could you talk about for an hour, what do you need English for. Each fact appears as a **fact card** with its quote; ✕ removes, ✎ edits. Twice she switches to English for one line ("tell me what you heard, in any language" / "now say anything back in English"). | The learner says little: Salma offers two examples and moves on; the planner can work from sparse fields. The learner refuses a question: card never appears. Network drops: cards saved locally, Salma pauses ("one moment") and resumes. |
| A3b | **Word check (optional)** | Eyes, 60s | "Help the show pitch at your level: tap the words you know." 40 to 60 words incl. fakes, one screen, skip allowed. Nothing scored on screen. | Skip: level comes from A3's two moments and the first call. |
| A4 | **Casting** | Eyes + ears, 40–90s | "Making your first episode…" (Salma's line, a slow breathing dot, no percentage). Two host orbs; each plays a 5-second hello; **swap** offers another voice; accent choice with samples. | Generation finishes early: the pilot button appears; casting stays available. Generation fails: Salma says so in one line and plays a pre-made pilot about the learner's topic class; the real one arrives tomorrow. |
| A5 | **The pilot** | Ears, 2–3 min | A short episode about the thing they could talk about for an hour, using their name once. Transcript visible on this first play. One hint, once: the Huh? button and "tap any word". | Huh? tapped: works as in B3 and is the first comprehension signal. |
| A6 | **The throw and the first call** | Voice, 60–90s | Karim: "Faisal, settle this." The throw card: **Call** / **Later**. The call screen; Mona says once, in English, that if a word won't come, hold the word button and say it in your language. Open mic, generous pauses, one easy question. The host closes like a person. | Later: Today shows the call door open; the flow continues to A7 anyway. Call fails to connect within 6s: "Weak signal. Let's do a voice note instead." (same screen, record one answer). Silence 8s: the host offers a smaller version of the question. |
| A7 | **One thing you managed** | Ears, 15s | Karim (in the show's language) names one specific thing the learner did ("you argued for a minute in English, first try") and signs off. No notes, no cards. | |
| A8 | **Keep your show** | Eyes, 60s | Account (Apple / Google / email), birth date if the store or law needs it; **when should tomorrow's drop?** in life terms (commute 7:40 / lunch / evening walk / pick a time); the weekly rhythm ("4 days, 2 spare", editable); the **consent row** for keeping recordings (unticked, "only for you, delete any time"); a second unticked row for anonymized transcripts to improve the teacher; the 7-day trial starts on 2 a day, said in one sentence with the price it becomes. | Account abandoned: the show waits 24h on this device; reopening resumes at A8. Consent refused: audio is analysed for a few minutes after each call then deleted; the tape still works from in-session recordings that are not stored (said in one sentence). |
| A9 | **Tomorrow** | Eyes, 10s | Three ideas for tomorrow from the hosts; one tap; "or tell Salma". Then Today in its done state: "That's today's show. Tomorrow at 7:40: …" | Nothing picked: the planner's pick waits as the hero. |

## Flow A′. The first session, order B: account first (PRD order)

A1 → **A1b Account** (Apple / Google / email, birth date, native and target language) → A2 → A3 → A3b → A4 → A5 → A6 → A7 → **A8′ Drop time, rhythm, consent, trial** (same screen minus the account block) → A9. Screens are identical; A1b is A8's account block as its own step. Expected cost: first sound at about 90 to 120 seconds instead of under 60. The build keeps the order configurable so the pilot can compare drop-off at A1b against drop-off at A8.

## Flow B. The daily episode

| # | Step | Mode | What happens | Branches |
|---|---|---|---|---|
| B0 | **The drop** | Ears | At the chosen time: one notification ("Mona interviews you for the job · 7 min") and the feed's new episode. The episode was ready before the drop time; the time only controls the cue. | Notification off: nothing is sent; Today still shows it. |
| B1 | **Today** | Eyes, 2s | A date line, one line from a host that is a real memory, the hero cover (title, hosts, length, doors), **Play**. Below, quieter: Why this episode? · 2 other ideas · Tell Salma an idea · the small door. | Proof day: the proof cover sits above. Finale day: the finale cover. 2 or 3 a day plan after one episode: a second hero appears only after the first is done. Back after a gap: a return episode in the hero, nothing else different (flow J). |
| B2 | **Doors** | | Listen · Call · Read · Chat, any order; Read before Call is the suggested order (the article arms the call). A ✓ marks a door that has been through, as a fact. | Skipped article: the throw card offers "Read the article first" once. |
| B3 | **Player** | Ears (+eyes) | Cold open (30s callback to three words from yesterday, then "how would you say…?"), the episode 5–7 min, audio-first: transcript folded for intermediates on first play, open on tap. **⟲ line** replays the last sentence; **Huh?** replays slower (0.85×) and shows the line with glosses; speed 0.75 / 0.85 / 1.0×; tap any word → word sheet. | Huh? on the same line twice: the gloss stays open and the planner notes it. Transcript hidden by preference: Huh? still shows the one line. Offline: cached episode plays; word sheets work from the cached gloss cache; Keep queues. |
| B4 | **Tap a word** | Eyes | Word sheet: word, gloss in own language, the sentence, 🔊, **Keep**. | Kept: it goes to the notebook and the planner brings it back; no animation. |
| B5 | **The throw** | Ears / Voice | The episode ends on a question; Karim throws to the learner. The player turns into an incoming call card: **Call** / **Read the article** / **Later**. In Ears mode the choice is spoken and play/pause accepts. | Later: the call door stays open until the next drop. |
| B6 | **Read** | Eyes, 3–5 min | A clean article, every word tappable, ▶ to hear it read, a long-press keeps a sentence. One line at the top from the host: "This is what I'll throw at you." | |
| B7 | **Chat** | Eyes, 2–4 min | One thread per host across days, date separators named after episodes. The host echoes the right form inside its replies; no margin notes. Mixed-language bubbles set their own direction. Ends with the three ideas for tomorrow. | "Why do we say it like that?": the host explains, because the learner asked. |
| B8 | **The wrap** | Ears + eyes, 10s | Sting, sign-off, "That's today's show. Tomorrow at 7:40: …" and the three ideas if not yet picked. Nothing else on the screen. | 2 or 3 a day: "You can have one more episode today." as a quiet line, no button until tapped. |

## Flow C. The call

| # | Step | Mode | What happens | Branches and failures |
|---|---|---|---|---|
| C1 | **Ring** | Ears | A chime and the host's breath; the call card (B5). Web: "keep the screen on" hint shown once; native: a lock-screen accept. | |
| C2 | **Connect** | | Host orb breathes; "Karim · 0:00" header; captions on by default (host only). | > 6s: "Weak signal. Let's do voice notes." Same argument continues as voice notes on the same screen. |
| C3 | **Talk** | Voice, 5–7 min | Open mic with generous pause tolerance; backchannels ("mm", "go on") while the learner pauses. **Hold the pad** to keep the floor as long as needed; release to hand back. The host answers errors as a friend would ("oh, you *went* there yesterday?") and the echoed form is set heavier in the caption; "sorry, you what?" when meaning is lost. The host leaves recall gaps for last week's words. | Silence 8s not holding: the host offers a smaller version of the question, never the same one louder. "Slower" / "sorry?" in any language: the host rephrases simply. |
| C4 | **Word button** | Voice | Hold the round **word** button and say the word in your own language; the host gives it back in English inside the conversation and carries on. The given word appears once in the host caption. | Not understood: the host asks "the word for what?" |
| C5 | **Retell** | Voice, 60s | Once per call the host may ask for a retell; a soft 60-second ring around the pad; never red, never cuts off. | |
| C6 | **End** | | The learner's ✕ or the host's sign-off ("Fine, but this isn't over."). The screen shows "Call with Karim · 6:12 · you spoke 3:40" for a beat and returns to Today. **Nothing else.** No notes, no cards, no score. | Connection lost mid-call: 10s reconnect ring; then voice notes; the thread is never lost. Learner upset: ✕ always works; Salma may ask on Today the next day "Easier one tomorrow?" when signals suggest it. |

## Flow D. After the session (what the learner sees: almost nothing)

1. The wrap (B8). 2. Tomorrow's three ideas (if not picked). 3. On Today, the door row shows what went through. 4. Behind the scenes (never shown): the analyst, the memory keeper, the planner. The only visible trace later is in the notebook: a new fact card (if the learner told the show something), a word now owned, hours updated, and the "working on" list changing at most once a week with a one-line why.

## Flow E. The weekly proof

| # | Step | What happens |
|---|---|---|
| E1 | On the chosen day (default: the last day of the rhythm week), the proof cover sits above the hero on Today, in Salma's colour, titled by its headline ("You told the whole story in the past tense"). Also in the feed. |
| E2 | Play: 2 minutes of Salma. One headline piece of evidence that passed the claim gate, with the clip; what the show will focus on next. |
| E3 | One screen accompanies it: the clip pair (then / now) with Play, the headline sentence, "how we know" (expandable, in plain words), next focus. No list of mistakes. |
| E4 | Variants: **good week** (as above); **flat week** ("Flat week. Here's what I'm changing." and the one change, in words); **slow week** (shorter, about what has built up over time, never about days missed). |
| E5 | Done returns to Today. The proof stays on the shelf. |

## Flow F. The season finale (every 4 weeks)

F1 Salma invites on Today ("Season 2 ends Thursday. Three minutes, same as last time.") → F2 the recording: three tasks of the same kind every season (describe, retell, argue), each with a soft ring, skippable, nothing scored on screen → F3 the tape: this recording beside the last one, Play A then B, at most two measured differences in plain words ("In October you stopped 11 times. Now, 3."), the real-world attempt from the season, and → F4 next season's goal, asked in the learner's words inside the finale, so finishing never becomes a reason to stop → F5 Season recap on the shelf: episodes, hours heard, minutes spoken, words owned, the moment Salma liked most. A retrospective, never a report card.

## Flow G. Subscribe (trial end and paywall)

| # | Step | What happens | Rules |
|---|---|---|---|
| G1 | Day 5 of the trial: Salma says on Today, once, in one line: "Two more days of the trial. Your plan after that is 2 a day at $29.99 a month; change it any time." Tappable to Plans. | One mention. No countdown component, no red, no modal. |
| G2 | Day 7, after the session: Plans sheet. Three cards; the middle one marked **Recommended**; price, "about $1 a day", per-episode price, what every plan includes (unlimited re-listening, the article, the chat, round two); the tutor comparison line ("a tutor is about $160 a month for two lessons a week"); founding-member line if applicable ("the first 100 keep this price while subscribed"). | Honest psychology only: three plans, middle recommended, top anchors, per-day framing, trial on 2 a day. **Never:** fake countdowns, scarcity, pre-ticked upgrades, guilt. |
| G3 | Choose → checkout (web checkout, or store purchase on native). Payment confirmed → "Welcome to the show, properly." from Salma; Today. | Payment failed: one system line in `--warn`, retry, "try later" keeps the show playable for 48h. |
| G4 | Trial ends without choosing: Today keeps re-listening and the notebook; the hero says, in Salma's words, "No new episodes until you pick a plan" with one button. Nothing is deleted. | No lockout of what was made; no nag beyond the hero line. |

## Flow H. Cancel

H1 Controls › Plan › **Cancel** (one tap) → H2 one sentence: "Your show runs until Dec 12. Nothing is deleted. Come back any time and it continues." **Confirm** / Keep → H3 done; Controls shows the end date. No survey wall, no retention offer screen, no "Karim will miss you". An optional single question after the fact ("Anything we should know?") with a Skip that is as big as Send.

## Flow I. Data: see, export, delete

I1 Controls › **See, export, delete my data** → I2 three plain rows: **See everything** (opens the notebook's full export view), **Export** (a zip of transcripts, recordings if kept, the notebook; emailed link within minutes), **Delete recordings only** (two taps: Delete → "Delete 23 recordings? The tape will be empty." Delete) and **Delete my account and everything** (two taps: Delete → a typed "delete" or a biometric → done; a 7-day grace during which signing in restores it, stated in one sentence). No reasons asked. Consent toggles (keep recordings; anonymized transcripts) are on the same sheet, each with its plain sentence.

## Flow J. Return after a gap

J1 Nothing happens for the gap's duration except the one note the learner wrote to themselves at A8, sent once after the gap they chose (default 7 days; "It's you from October. The interview is in March."). → J2 First open: Today exactly as any day; the hero is a **return episode**: one step easier, opening from the learner's life ("how did the move go?"), never mentioning days missed, with a quick real win set up by the hosts. → J3 The rhythm shows the current week only. The season continues from its calendar; arcs that were open wait.

## Flow K. The small door (a bad day)

K1 Today's quiet card: "Short on time? Karim's 90-second recap and one voice note back. Counts fully." → K2 the recap plays → K3 one voice note (the hold pad, one answer) → K4 the wrap. The day counts toward the rhythm like any other. The full episode stays on the shelf.

## Flow L. The sample page (before signup, web, shareable)

L1 A public page with one question in the visitor's language ("What could you talk about for an hour?") and a Make my sample button → L2 60 to 90 seconds later, a 90-second two-host episode about their answer, with the transcript → L3 one button: **Start your show** (to A1). Forwardable link. No account, no email required to listen; an email field afterwards for the waitlist in languages that have not passed the gate.

## Cross-flow failure states

| Failure | Design |
|---|---|
| Offline on open | Today loads from cache; the hero plays if cached, else the cover shows "ready when you're back online"; notebook read-only; a one-line toast when back online |
| Episode not ready at the drop | Salma, one line: "Still making today's. A few minutes." The small door and the shelf are offered. Never a spinner over the hero for more than 10s |
| Mic blocked | The call screen explains in one line how to allow it (platform-specific), or offers voice notes by typing |
| Payment failed | System line in warn, retry, 48h grace |
| Wrong memory used by a host | Any fact card can be deleted at once; the learner can say "that's not right" to Salma; the fix is immediate and counted as a bug |
