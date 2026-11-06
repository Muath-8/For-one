# For one — 04. Screen specifications

*Part 4 of 8. One section per screen: purpose, mode, layout (top to bottom), components (from 01 §8), states (empty, loading, error, offline), copy, and what Salma or the hosts say on it. Copy is in English here; Salma's lines are in the learner's own language in the product. Screen ids match 03-user-flows.md. The prototype at design/prototype/for-one-prototype.html shows most of these in its v2 form and is the visual reference; where this spec and the prototype differ, this spec wins.*

**Conventions.** Every screen: 20px gutters, one primary action, no badges. "Copy" sections give the exact strings for the beta. "Never" lists what must not appear on that screen. States that are the same on every screen are in §0.

## 0. Global states

| State | Treatment |
|---|---|
| Loading (< 300ms) | Nothing. No skeletons flash. |
| Loading (> 300ms) | The screen's static parts render; the dynamic part shows one breathing dot in `--mute` and, if Salma owns the screen, her one-line "One moment." No spinners, no percentages. |
| Error (system) | One line in `--warn` at the top of the affected component, a Retry quiet button. Never a full-screen error for anything short of a crash. |
| Offline | A system toast on transition ("You're offline. Today's episode is ready."); cached content plays; actions that need the network queue silently and show "saved" when back. |
| Empty | Never a drawing of an empty box. Salma says the one sentence that explains why it is empty and what fills it. |

---

## A1. Open
**Mode:** Eyes · **Purpose:** first sound within a minute.
**Layout:** wordmark (display, wdth 70, 48) · one line in the phone's language ("Your own show, in English.") · target language (hidden if only one passed the gate; otherwise a short list of names in their own script) · age checkbox · **Start** · quiet "I already have a show".
**States:** default · unsupported interface language (English interface, Salma asks on A3) · under 18 (one sentence, no door).
**Copy:** "Your own show, in English." · "I'm 18 or older" · "Start" · "I already have a show".
**Never:** a carousel, testimonials, a sign-up form.

## A2. Mic primer
**Layout:** Salma's 40px orb · "Salma, your producer, will talk with you for 3 minutes. You can talk back or type." · **Talk** (primary) · Type (quiet).
**States:** mic refused (continues as Type; one toast "No mic. You can type, and still hear Salma.") · silent phone (toast "Turn your sound on to hear Salma").

## A3. Meet Salma
**Mode:** Voice · **Purpose:** intake as a conversation that shows its work.
**Layout:** "Salma · producer" label · 120px lilac orb with live captions under it (Readex Pro 20, learner's language, RTL when needed) · "Salma's notes" divider · fact cards sliding in as spoken (quote in mono 12, the fact in body 16, ✎ ✕) · bottom: hold-to-talk pad (shorter, 72px) and a keyboard toggle.
**Components:** voice orb, caption row, fact card, hold pad (short).
**States:** listening (pad ring breathes) · Salma speaking (pad dims) · typing · network pause (Salma: "One moment." cards stay) · sparse answers (Salma offers two examples once).
**Copy (Salma, in the learner's language):** "What should Karim and Mona call you?" · "What could you talk about for an hour?" · "What do you need English for?" · "Can I try something? I'll say one line in English. Tell me what you heard, in any language." · "Now say anything back in English. Anything is fine." · "I'll remember these. You can change or delete any of them, now or later."
**Never:** a form, a progress indicator, a level label.

## A3b. Word check (optional)
**Layout:** "Help the show pitch at your level. Tap the words you know." · a flowing cloud of 40 to 60 words in the target language (16, s2 pills; selected becomes s3 with text) incl. 10 fakes · **Done** · Skip (quiet).
**States:** default · skipped.
**Never:** a score, a count, a level, any feedback on fakes.

## A4. Casting
**Layout:** Salma line "Making your first episode…" with one breathing dot (no bar) · "Your hosts" · two host orbs with name, ▶ hi (5s), swap · "Accent you'd like" with two or three samples · **Start the pilot** appears when ready (primary).
**States:** making · ready · generation failed (Salma: "The first one is taking longer than it should. Here's one I made earlier about [topic]; yours is ready tomorrow.") · swapped (the new voice says hi).
**Never:** a percentage, "this may take a while", a spinner on its own.

## A5. The pilot
Player (B3) with the transcript open on first play, and two one-time hints as quiet labels: "Huh? replays the last line slowly" · "Tap any word".

## A6. The throw and first call
Throw card (B5) then Call (C). Mona's one-time line is spoken, not shown, and also appears once as the caption.

## A7. One thing you managed
Audio only; the Today card beneath is dimmed; a single line of caption in the host's colour: "You argued for a minute in English, first try. See you tomorrow." No card, no list.

## A8. Keep your show
**Mode:** Eyes · **Purpose:** the account after there is something to keep.
**Layout:** title "Keep your show?" · Continue with Apple / Google · Use email (quiet) · divider · "When should tomorrow's episode drop?" radios in life terms (On my commute 7:40 · Lunch break · Evening walk · Pick a time) · "How many days a week?" (default "4 days, 2 spare", stepper 2–7) · consent row "Keep my recordings so I can hear my progress. Only for you, delete any time." (unticked) · consent row "Use my transcripts, with my name removed, to improve the teacher." (unticked) · one sentence: "Your 7-day trial is on 2 episodes a day. After that it's $29.99 a month unless you pick another plan. Cancel in one tap." · **Keep my show**.
**States:** default · email path (one field, magic link) · abandoned (resumes here for 24h) · consent off.
**Never:** pre-ticked boxes, "free" in large type, a timer.

## A9. Tomorrow (three ideas)
A sheet: "Tomorrow?" · three cards, each one host line (Karim or Mona orb, the pitch in one sentence, length) · "or tell Salma an idea" (hold-to-talk) · Skip (quiet; the planner's pick waits).

---

## B1. Today
**Mode:** Eyes (2 seconds) · **Purpose:** one thing, made today.
**Layout (top to bottom):** date line (mono) · a host line that is a real memory (body 16, host orb 24px: "Mona: Still can't believe you called the new coach a genius.") · **hero cover** (art, title in cover style, two host orbs, label "7 MIN · CALL · ARTICLE", **Play**) · Why this episode? › (quiet row) · 2 other ideas ⌄ (quiet row) · 🎙 Tell Salma an idea (quiet row) · small door card (quieter still) · tab bar.
**States:**
- *Ready:* as above.
- *In progress:* the label line becomes the door row (Listen ✓ · Call · Read · Chat); Play becomes Continue.
- *Done for today:* cover shrinks to 50%, closing line in cover style "That's today's show." · "Tomorrow at 7:40: Mona interviews you for the job." · three ideas if unpicked · on 2 or 3 a day: "You can have one more episode today." as a quiet row.
- *Allowance reached:* "That's two today. Tomorrow's is ready at 7:40." No button.
- *Proof day:* the proof cover (Salma's colour, smaller) sits above the hero.
- *Finale day:* the finale cover above the hero.
- *Return day:* the hero is the return episode; nothing else differs.
- *Not ready:* art and title show; Play disabled; Salma: "Still making today's. A few minutes." Small door and shelf offered.
- *Loading > 300ms:* static frame, one dot.
- *Offline:* cached hero plays; else "Ready when you're back online."
- *Trial ended, no plan:* the hero is replaced by Salma's one line "No new episodes until you pick a plan." and one button Plans; shelf and notebook unchanged.
**Never:** a feed, a calendar, a streak, a counter, a badge, more than one Play.

## B2. Why this episode? (sheet)
Three to four lines from Salma, each a reason with its source: "You said on Monday the derby was Sunday." · "It brings back 4 words from this week: line-up, bench, …" · "Karim will push you to talk about plans." · "Shorter than usual: you've been busy." · "Not quite right? 🎙 Tell Salma".
**Never:** a target list ("grammar: past simple"), a level.

## B3. Player
**Mode:** Ears, eyes optional.
**Layout:** ⌄ collapse · title (display 22) · the transcript (karaoke; current line `--text` 20/1.7, others `--mute`; every word tappable; folded by default for intermediates on first play: a single "Show words" quiet button) · scrubber (mono timecode "2:14 / 7:02") · controls row: ⟲ line · ▶❚❚ (64px) · speed (0.75× / 0.85× / 1.0×) · **Huh?** (64px pill, display face, centred).
**Components:** transcript, Huh?, word sheet.
**States:** playing · paused · transcript hidden · Huh? expanded (the line slides down, slows, glosses unfold under hard words in the learner's language, 14) · marked moment (from headphone "next": a 1s "Marked" toast) · offline (cached) · end (the throw card replaces the controls).
**Copy:** "Huh?" · "Show words" / "Hide words" · "Marked".
**Never:** a "words learned" counter, a comprehension score, autoplay to the next episode.

## B4. Word sheet
word (display 28) · gloss (own language, 18) · the sentence it came from (16, mute) · 🔊 · **Keep this word** → "Kept" (quiet, no animation).
**States:** default · kept · offline (gloss from cache; Keep queues).

## B5. The throw (incoming call card)
Host orb (120px, breathing to the host's line) · "Karim wants your take" · the question in quotes · **Call ✆** (primary) · Read the article (secondary) · Later (quiet).
**States:** default · article done (the Read button hides) · later chosen (returns to Today with the call door open).

## B6. Read
Host line at top ("This is what I'll throw at you on the call.") · ▶ Hear it read · article (Readex Pro 18–20 / 1.7, 34rem measure; every word tappable; long-press a sentence: hear it / keep it) · at the end: **Call Karim** (primary) if the call door is open.
**States:** reading · listening (karaoke highlight by sentence) · offline (cached).

## B7. Chat
One thread per host · date separators named after episodes ("Thu · Karim is not okay") · host bubbles (s1, 16) · learner bubbles (s2) · mixed-language bubbles set their own direction · composer: text field + 🎙 hold.
**States:** empty (host opener always exists, so never truly empty) · typing · host thinking (orb slow breath, no "typing…" dots) · end of day (the three ideas card inside the thread) · offline (compose queues).
**Never:** a margin note, an edit mark on the learner's bubble, read receipts.

## B8. The wrap
Full-bleed closing: "That's today's show." (cover style) · "Tomorrow at 7:40: …" · three ideas if unpicked · Done.

---

## C. The call
**Mode:** Voice · **Purpose:** make speaking safe.
**Layout:** header "Karim · 2:41" (mono) · host orb (120px) · host caption (Readex Pro 20 / 1.4; the echoed form in weight 600 and `--recast`; a word given back appears once in the caption) · **hold pad** (full width, 112px, "hold to keep the floor") · row: **word** button (56px round) · mute · ✕.
**Components:** voice orb, caption row, hold pad, word button, retell ring.
**States:**
- *Ringing:* chime, breath, the throw card.
- *Connecting:* orb dim; > 6s: "Weak signal. Let's do voice notes." and the pad becomes a record button, the same argument.
- *Host speaking:* pad at 60% opacity; caption streams by word.
- *Learner's turn:* a breath and a soft rising tone; pad at 100%; backchannels while they pause.
- *Held:* pad fills 20% learner green, ring breathes, host waits indefinitely.
- *Word button held:* "say it in your language" caption under the button; released: the host gives the word inside the next line.
- *Retell:* a soft 60-second ring around the pad; never red; never cuts off.
- *Reconnecting:* 10s ring; then voice notes.
- *Ended:* "Call with Karim · 6:12 · you spoke 3:40" for 2 seconds; then Today. Nothing else.
- *Mic blocked:* one line with the platform's steps; voice notes by typing.
- *Web only:* "Keep your screen on during the call" shown once above the pad; if backgrounded, the call pauses and the host says "you still there?" on return.
**Copy:** "hold to keep the floor" · "word" · "say it in your language" · "Weak signal. Let's do voice notes." · "you spoke 3:40".
**Never:** the learner's live transcript, a score, a tick, a red anything, a notes screen after.

---

## D. Notebook (home)
**Mode:** Eyes · **Purpose:** the teacher's file, open to the learner.
**Layout:** "Notebook" · "Salma's notes on Faisal" (Salma's 40px orb) · **Working on with you** (≤ 3 rows, each with a one-line why and ✕; "add one" quiet) · list rows: About you (14) · Words you own (212) · The tape (3) · Out in the world (4) · Marked moments (9) · Hours (41 heard · 6 spoken) · Controls ›.
**States:** week 1 (About you has 3 cards; Words you own empty: Salma "Words you've used on your own, twice, in different days. They'll show up here." ; The tape: "Your first recording is at the end of season 1.") · normal · offline (read-only, "saved" when back).
**Never:** charts, percentages, levels, CEFR, a goal bar, a mistakes list.

## D1. About you
Fact cards: the fact (16), "you said on Oct 3: '…'" (mono 12 quote), ✎ ✕. Unconfirmed facts have a dashed border and start "I think…"; a tap confirms or deletes. Sensitive facts (health, religion, politics, money) carry a lock glyph and the line "only if you bring it up".
**States:** normal · empty (never: at least the three onboarding facts) · deleted (gone at once; no "are you sure").

## D2. Words you own
Count once at the top, quietly (mono). Rows: word · the learner's own sentence · ▶ · date. Kept words (not yet owned) in a second section "Kept, coming back soon".
**Never:** a target count, a review button, flashcards.

## D3. The tape
"Same questions, every season." · cassette tiles per season (S1 Sep 0:48 · S2 Oct 1:31 · S3 Nov 2:05) · **Play S1 then S3** · Salma's line with at most two measured differences in plain words.
**States:** one recording ("One so far. The next is at the end of this season.") · two or more · recordings not kept ("You chose not to keep recordings, so the tape is empty. Change that in Controls.").

## D4. Out in the world
Dated entries in the learner's words with the quote: "Had the interview. They asked about the project and I didn't freeze." · "add one" via Salma.

## D5. Marked moments
Sentence + audio from headphone "next" presses; each can be kept as a word or deleted.

## D6. Hours
"41 hours heard · 6 hours spoken" (display 28) · "Since September." · nothing else. Cumulative, never a bar.

## D7. Controls (sheet)
Rows: Drop time (7:40, On my commute) · Drop notification (on/off) · Rhythm ("4 days, 2 spare") · Captions on calls · Transcript in the player (open / folded) · Default speed · Keep my recordings (with "Delete all recordings") · Theme (System / Dark / Light) · Reading size · Interface language · Plan (2 a day · $29.99 · renews Dec 12 · Change · **Cancel**) · See, export, delete my data › · Sign out.
**Never:** more than one screen of settings; host or topic settings (those are sentences to Salma).

---

## E. Show (shelf)
"Show" · season rows (title from Salma: "Season 2 · Interview season", dates) with covers in a horizontal row (48–96px) · proofs row · finales row · unfinished episode covers carry a small "waiting" label, never "overdue".
**States:** week 1 (one row with the pilot and today) · normal · offline (covers cached; uncached play greyed with "online").

## F. Proof
Proof cover (Salma's colour) · ▶ (2 min) · clip pair (then / now, each with ▶ and its date) · the headline sentence (display 22) · "How we know" (expandable: "Same task, three sessions, judged against your own September recording. Not a guess.") · "Next: …" · Done.
**Variants:** good · flat ("Flat week. Here's what I'm changing: …") · slow (shorter, about what has built up; never the days).
**Never:** a list of errors, numbers beyond the clip lengths, comparison to others.

## G. Finale
Salma's invitation card → recording screen (one task at a time, the prompt in the target language, a soft ring, Skip, ✕ keeps what was recorded) → the tape (D3) with this season's differences → "Next season, what's the one thing?" (hold-to-talk or type) → season recap card (episodes · hours heard · minutes spoken · words owned · "the moment I liked most" with ▶).

## H. Plans
"Your plan" · three cards side by side on wide, stacked on phone (1 a day $19.99 · **2 a day $29.99 Recommended** · 3 a day $44.99), each with "about $1 a day" style line (mono), per-episode price, episodes a month · beneath: "Every plan: listen again as often as you like, the article, the chat, round two." · "A tutor is about $160 a month for two lessons a week." · founding line if applicable · **Choose** on each · "Cancel in one tap, any time."
**States:** trial active (the current plan says "your trial") · chosen · founding (price locked line) · payment failed (warn line, retry).
**Never:** countdowns, "only X left", crossed-out fake prices, pre-selected upgrades, a "best value" sticker on the top tier.

## I. Data and deletion (sheet)
Rows as in 03 flow I. Each destructive row: first tap turns the row into its confirmation sentence with Delete / Keep inline (no modal); account deletion asks for a typed "delete" or biometrics. Grace period sentence stated once.

## J. Sample page (web, public)
Wordmark · one question in the visitor's language · a text field or 🎙 · **Make my sample** · (60–90s: two host orbs and "Karim and Mona are recording…") · the 90-second player with transcript · **Start your show** · share link · "Not in your language yet? Leave an email."

## K. Small door
A quiet card on Today → recap player (90s, no transcript by default) → the hold pad for one voice note ("One voice note back. Anything.") → the wrap. The door row shows Listen ✓ · Call ✓ for the day.

## L. Install card (web only)
Shown once, after the first call, on Today: "Put For one on your home screen so the drop reaches you." Two-step picture for the platform · Done · Not now. Never shown again after dismissal.

## M. The lock screen / Now Playing
Cover (dark version) · title · "For one" · ⟲ line · ❚❚ · mark (as previous / next actions). During a call on native: accept / decline like a phone call. CarPlay / Android Auto: standard Now Playing only; the call is never offered there.
