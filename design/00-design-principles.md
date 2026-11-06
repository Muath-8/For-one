# For one — 00. Design principles

*Design documentation, part 0 of 8. Written 2026-11-06 from concept-v2.md, decisions.md (Muath's answers of 2026-10-23), perspectives/ui-ux.md, perspectives/enjoyment-pull.md, perspectives/consistency-motivation.md, the feature map (features/for-one-features.html) and the v2 prototype (design/prototype/for-one-prototype.html). Where the UI/UX lens of 2026-10-09 and the decisions of 2026-10-23 disagree, the decisions win; the differences are listed at the end.*

**Entry page for this documentation set:** the designed overview artifact (link in README.md once published). Files: 00 principles · 01 design system (+ tokens.css, tokens.json) · 02 information architecture · 03 user flows · 04 screen specs · 05 interaction and audio UX · 06 content and voice guidelines · 07 open questions.

---

## 0. One sentence

**For one is a studio that makes one show for one listener.** Everything on screen is the studio window: it is there when the learner wants to look, and the product works when they don't.

## 1. The three facts every screen is built on

| Fact | Where it comes from | What it forces |
|---|---|---|
| **The product is sound.** The episode, the call and Salma's voice are the product; the screen is secondary. | UI/UX lens, concept v2 §2 | Every step except reading must be possible with the phone in a pocket. Lock screen, headphones and car controls come before any screen. |
| **Teaching is invisible.** Nobody ever tells the learner they were wrong. Corrections happen inside conversation as friendly echoes ("oh, you *went* there yesterday?"). No pop-ups, no red marks, no notes after the call, no margin notes in chat. | Decision 3, law 7 | There is no "correction UI" anywhere. No component in the design system renders an error state on a learner's sentence. The teacher is felt through what comes back in later episodes, and seen only in the notebook and the weekly proof. |
| **Evidence, not games.** The learner is shown what they can now do (their own sentences, their own voice four weeks apart, hours heard, minutes spoken, words they own). Never points, streaks, levels, percentages, bars that fill, leaderboards, confetti. | Decision 4, law 1, law 12 | No progress bar exists for learning. No counter resets. Nothing on screen looks different because the learner was away. |

## 2. The ten principles, each with a test

A principle without a test is a mood. Each one below can be applied to a mockup and answered yes or no.

### P1. One thing, made today
The home screen shows today's episode, large, with one button. Not a feed, not a grid, not a path. Alternatives ("2 other ideas", "tell Salma an idea") are one tap away and visually quieter.
*Test: within two seconds of opening, does the learner know the one thing to do?*

### P2. Ears first, eyes optional
Play, replay a sentence, accept the call, hold the floor, ask for a word, end: all reachable from headphone and lock-screen controls. The screen adds detail and is never required to finish a session.
*Test: can a whole session happen on a bus with the phone in a pocket?*

### P3. The teacher has a voice, never a dashboard
Progress and plans arrive as Salma's sentences and as the learner's own recordings. If something only makes sense as a chart, it is cut.
*Test: would a good human tutor say this out loud?*

### P4. Nobody is ever told they were wrong
No screen, sheet, card, toast, badge, color or sound marks a learner sentence as incorrect. The right form is heard in the host's reply (and may be set in a slightly heavier weight in the host's caption so it can be noticed, never labelled) and returns in later episodes.
*Test: find any pixel that says "this was wrong". There must be none.*

### P5. Hidden by default, open on request
The pedagogy runs out of sight during the show. The notebook shows everything the show knows (each fact with its source and a delete), the "working on" list (at most 3 items, each vetoable), and "why this episode". Explanations exist, but only when the learner asks.
*Test: does every hidden decision have a place where it can be seen and corrected?*

### P6. Never leave a debt
No missed days, overdue items, unread counts or "pick up where you left off". An unfinished episode waits on the shelf. A learner back after three weeks sees a day exactly like any other, plus a return episode that is one step easier and never mentions the gap.
*Test: does any screen change because the learner was away? It must not.*

### P7. A finite, good portion
A session ends like a show: a sting, a sign-off, tomorrow's drop time. No autoplay, no "one more", no infinite scroll. The plan's allowance is stated plainly when reached, by Salma, never as an excuse in character.
*Test: after the session, is there anything left to scroll?*

### P8. Make speaking safe
Speaking is the most anxious moment in the product. The learner controls the floor (hold to keep it, the host waits as long as needed), has a way out (hold the word button and say the word in their own language; the host gives it back and carries on), and privacy (nobody else hears; recordings are theirs and deletable).
*Test: what does a frozen learner do? There must be an obvious, kind answer on screen and in the ear.*

### P9. Sound is interface
Whose turn it is, who is speaking and what just changed are carried by sound: a breath and a soft rising tone before the learner's turn, a closer and drier voice for Salma, a show sting at each end of an episode. No reward sounds, ever.
*Test: with eyes closed, can the learner tell who is talking and whose turn it is?*

### P10. Your life, your words, your voice
Every example on screen is the learner's: their sentence, their recording, their team, their interview. No stock sentences anywhere the learner can see. The only exception is the 90-second sample episode before signup, which is about the visitor's own answer to one question.
*Test: could this screen be shown to a different learner unchanged? If yes, it is not personal enough.*

## 3. Who is who on screen

| Role | Speaks | Does | Never does |
|---|---|---|---|
| **The hosts** (Karim, Mona in the example) | The target language only | Make the episode, argue on the call, banter in the chat, echo the right form inside a reply, leave a gap for a word from last week, ask for a 60-second retell, give a word back when the learner says it in their own language, explain when the learner asks "why do you say it like that?" | Say "wrong", grade, mention progress, interrupt a learner mid-sentence, praise the person, pretend to have a life outside the show |
| **Salma, the producer** | The learner's own language first; more of the target language as they grow | Onboarding (3 minutes), the notebook, "why this episode", the weekly proof (voice), the season finale, life updates ("tell Salma"), answers when asked, the plan and controls in plain words | Correct, send notes after a call, speak during a call, guilt, praise every turn, appear in the show |
| **The learner** | Both | Picks tomorrow from three ideas, takes sides, calls in, keeps words, vetoes what the show works on | Fill in forms, take tests |

Visual identity follows the roles: the hosts are warm, saturated voice orbs (Karim orange, Mona pink in the prototype) with their names in the display face; Salma is a cool, lighter lilac mark, smaller, closer; the learner is the green orb and the only one that appears on the hold pad. Nobody has a face. See 01-design-system.md §6.

## 4. Three modes

| Mode | The learner has free | Covers | Design consequence |
|---|---|---|---|
| **Ears** (60 to 70% of time) | Ears only | The episode, the call, Salma's proof | Lock-screen artwork is the cover; headphone buttons map to replay-sentence and mark-moment; the call can be accepted from the lock screen (native) or from a foreground tab (web) |
| **Voice** (15 to 25%) | Ears and mouth, maybe a glance | The call, the retell, "say it once" | One huge hold pad; captions for the host only; no live caption of the learner's own words |
| **Eyes** (15 to 20%) | Hands and eyes | The article, the chat, the notebook, plans | Generous reading type; every word tappable; bidirectional text handled per block |

Every screen spec in 04-screen-specs.md is tagged with the mode it serves.

## 5. The laws that constrain the design (from concept v2 §5)

1. No game furniture. 2. Every moment has a hidden shape and a social surface. 3. The learner owns topic, format and cast; the teacher owns pedagogy and shows its reasons on request. 4. Every episode is complete; plot may persist, obligation never. 5. Honesty about what it is (AI disclosure built in). 6. Formats are hijacked, not invented (podcast, call-in, chat, notebook). 7. Teaching is invisible. 8. Conversations end like conversations. 9. The show is the gym; life is the game. 10. The text is used once; the language comes back. 11. A finite, good portion. 12. No claim without proof.

The trust contract adds, in the UI: **told, not inferred** (a fact card always shows its quote), **a wrong memory is a bug** (delete is one tap and never asks why), **data use is opt-in** (every consent is an unticked box in a plain sentence), and **never manipulate** (no countdowns, fake scarcity, hidden cancellation, guilt or pre-ticked upgrades, including on the plans screen).

## 6. Where this design departs from the UI/UX lens of 2026-10-09

The lens was written before Muath's decisions. These parts of it are **not** in this design:

| Lens proposal | Status now | Why |
|---|---|---|
| Post-call debrief with "new for you / polish / word you reached for" cards | Removed | Decision 3: no notes after the call. The goodbye is a goodbye. |
| Collapsed margin notes from Salma under chat messages | Removed | Decision 3: the host echoes the right form in the reply instead. |
| Salma's "talkback" whisper during the call | Replaced by the word button | PRD v3.1: the host gives the word back; Salma is silent in calls. "Talkback" is button-only in the beta (no voice command). |
| "Want my notes after each call?" preference | Removed | There are no notes. |
| Native app for the beta | Open (decision 7, open) | Both are designed; see 02 §6 and 07. |
| Sound in 60 seconds, account after the first call | Open (first-session order) | Both orders are designed; see 03 flow A and A′. |
| Season length 4 weeks, finale = then-and-now recording | Kept | Decision 5. |
| Hold to keep the floor, Huh?, tap any word, the notebook, the tape, seasons, out in the world, the controls sheet | Kept | Agreed everywhere. |

## 7. What "polished" means for this product

Muath rejected first drafts that were "cards of text and chips". For one's screens must look like a real audio product: typography-led, one strong display face, generated cover art per episode rather than stock illustration, voice orbs rather than avatars, a dark "night studio" surface by default and a daylight surface that is equally considered, Arabic and Latin set with equal care. Explanatory text never lives inside the app; the app says what the show says. See 01-design-system.md.
