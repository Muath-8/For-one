# For one through the UI and UX lens

*Perspective 2026-10-09. One of eleven lenses on the For one product concept. Builds on the PRD v2.0, the Product Concept, and the first rethink ("show, teacher, proof"). It does not repeat their arguments; it asks what those ideas look, sound and feel like on a phone.*

---

## Decisions only you can make

Three calls shape every screen below. My recommendation comes first; the rest of this document assumes it.

| # | Decision | Recommended | Alternative | Why it matters |
|---|---|---|---|---|
| 1 | Who is the teacher on screen? | **A producer**: one persona who runs your show, speaks your native language, keeps your notebook, gives the post-call notes and the weekly proof. The hosts stay pure entertainment and never correct. | The hosts do everything, with recasts only | The rethink says the teacher must show itself more. If the hosts do it, the show turns into a lesson. A separate producer lets the show stay a show and the teacher be a real teacher. |
| 2 | Web app or native app for the beta? | **Web for Milestone 0, a native app (one codebase, e.g. React Native) for the private beta** | Web only through v1, as the PRD says | The product is mostly audio and voice. Lock-screen play, background audio, hands-free calls and a reliable scheduled drop are the core of the commute use case, and phone browsers do them poorly. |
| 3 | What happens in the first ten minutes? | **Sound in under 60 seconds. A 3-minute talk with the producer, a 2-minute pilot episode, a 90-second first call, then the account.** | The PRD order: account, birth date, two language lists, 10-minute intake, then a 4 to 5 minute episode | First sessions decide retention. The PRD makes people fill four screens and talk for ten minutes before they hear the show. |

**Decided 2026-10-23:** Muath chose #1, a producer as the on-screen teacher. #2 (web or native) and #3 (first-session order) are still open.

---

## 1. The design thesis

**A studio with one listener.**

For one is a production studio that makes one show for one person. The design follows from that picture:

- **The show is sound.** Most of the product happens in the ears: the episode, the call, the producer's voice. The screen is the studio window. It is there when you want to look, and the product works when you don't.
- **The teacher is a person.** You never meet a dashboard. You meet a producer who knows you, keeps notes you can read, and talks to you between takes.
- **Each day is a finished thing.** One episode, made overnight, with a beginning and an end. When it ends, the app has nothing left to offer today, on purpose.

Three modes cover every moment in the product. Every flow below is tagged with the mode it needs.

| Mode | What you have free | What happens | Share of time (my estimate) |
|---|---|---|---|
| **Ears** | Ears only: walking, driving, cooking | Listen to the episode; the call; the producer's voice notes | 60 to 70% |
| **Voice** | Ears and mouth, maybe a glance | The call-in; the retell; saying a polished sentence once | 15 to 25% |
| **Eyes** | Hands and eyes: a desk, a sofa | Read the article, chat, read the debrief notes, browse the notebook | 15 to 20% |

The PRD designs an eyes-first web page with an audio player in it. I would design an audio product with screens around it.

---

## 2. Design principles

These are the rules I would hold every screen to. Each one is a test you can apply to a mockup.

1. **One thing, made today.** The home screen shows today's episode, big. It is not a feed, a grid or a path. Alternatives exist but are one tap away, not on display.
   *Test: can someone understand what to do within two seconds of opening the app?*

2. **Ears first, eyes optional.** Every step except reading must be possible with the phone in a pocket: play, replay a sentence, accept the call, ask for a word, end. The screen adds detail; it is never required.
   *Test: can a full session be done on a bus without taking the phone out?*

3. **The teacher has a face and a voice, never a dashboard.** Progress, corrections and plans are delivered by the producer, in sentences and in your own recorded voice. No charts, scores, rings, or bars that fill.
   *Test: would a good human tutor say this out loud? If it only makes sense as a chart, cut it.*

4. **Hidden by default, visible on request.** The pedagogy runs invisibly during the show, as the concept wants. But any learner can open the notebook and see what the producer knows about them, what it is working on, and why today's episode was made. A glass box, not a black box.
   *Test: does every hidden decision have a place where it can be seen and corrected?*

5. **Corrections wait their turn.** Nothing interrupts the learner mid-sentence. Feedback is layered by time: during the call it is only heard (a clear recast); right after the call it is seen (the debrief); weekly it is told as a story (the proof).
   *Test: is there any moment where a red mark appears while the learner is still speaking? There must not be.*

6. **Never leave a debt.** No missed days, no overdue items, no unread counts, no "pick up where you left off" guilt. An unfinished episode waits quietly on the shelf. A returning learner sees today's episode, as if they never left.
   *Test: does any screen look different because the learner was away?*

7. **A finite, good portion.** Every session ends with a clear ending: credits, a closing line, tomorrow's drop time. No autoplay, no "one more", no infinite anything. The 2-episode cap is stated plainly when reached.
   *Test: after the session, is there anything left to scroll? There must not be.*

8. **Make speaking safe.** Speaking in a new language is the most anxious moment in the product. The interface gives control over the floor (hold to think), an escape hatch (ask your producer for a word in your own language), and privacy (no one else hears, recordings are yours).
   *Test: what does a nervous learner do when they freeze? There must be an obvious, kind answer on screen and in the ear.*

9. **Sound is interface.** Turn-taking, mode changes and the producer's presence are carried by sound design, not just pixels: a breath before "your turn", a drier, closer voice for the producer, a show sting that opens and closes each episode.
   *Test: with eyes closed, can the learner tell who is talking and whose turn it is?*

10. **Your life, your words, your voice.** Wherever there is an example, it comes from the learner: their sentence, their recording, their team, their interview. No stock sentences anywhere the learner can see.
    *Test: could this screen be shown to a different learner unchanged? If yes, it is not personal enough.*

---

## 3. Who is who on screen

The concept has hosts and a hidden planner. The rethink adds a coach. On a phone, the learner needs to know who they are talking to at every moment. I recommend three roles, borrowed from a real radio studio.

| Role | Speaks | Job | Never does |
|---|---|---|---|
| **The hosts** (e.g. Karim and Mona) | Target language only | Make the episode, argue on the call, banter in the chat | Correct, grade, explain grammar, mention progress |
| **The producer** (e.g. Salma) | The learner's native language at first, shifting toward the target language as they grow | Onboarding talk; "talkback" help during the call; post-call notes; the notebook; "why this episode"; the weekly proof; changing settings by conversation | Perform in the show, guilt, praise every turn |
| **You** | Both | Co-star: pick topics, take sides, call in | Fill in forms, take tests |

**Talkback.** In a radio studio, the producer talks into the presenter's headphones during a live show, unheard by the audience. For one can do the same. During a call, the learner holds a button (or says, in their own language, "how do you say...") and the producer whispers the word into their ear. The host waits. This one feature solves three problems: it removes the freeze, it keeps the call in the target language, and it gives the teacher a natural, non-grading presence in the moment.

Visually: hosts have warm, saturated portraits and speak in the main audio channel. The producer has a smaller, simpler mark (a monogram, not a face) and a closer, drier voice, like a voice in your headphones rather than in the room. The learner learns the difference in one session without being told.

---

## 4. Core flows, screen by screen

The example learner throughout: **Lina**, 29, Cairo, native Arabic, intermediate English, an Al Ahly fan preparing for job interviews in English. Her hosts are Karim and Mona; her producer is Salma.

### Flow A. The first session: sound in 60 seconds, no questionnaire

The PRD collects goal, situation, interests, life facts, past attempts and follow-up dates through a 10-minute intake. Those are the right fields, but the learner has not heard a single second of the show yet. I would collect the minimum in three minutes, make the rest of the profile grow over the first week, and let the learner watch the notebook fill up as they speak.

**A1. Open** *(Eyes, 5 seconds)*
```
┌─────────────────────────┐
│                         │
│   For one               │
│                         │
│   برنامجك الخاص         │
│   بالإنجليزية.          │
│   (Your own show,       │
│    in English.)         │
│                         │
│  [ Start ]              │
│  ☐ I'm 18 or older      │
│                         │
│  I already have a show  │
└─────────────────────────┘
```
- Native language is taken from the phone's language setting, shown in that language and changeable later. Target language: one tap from a short list, or fixed if launching with one pair.
- No account. The age check is one tap (the full birth date comes with the account at A8).

**A2. Mic primer** *(Eyes, 5 seconds)*
"Salma, your producer, will talk with you for 3 minutes. You can talk back or type." Buttons: **Talk** (asks for the mic) / **Type**. The permission prompt appears only after the learner chose to talk, so it is expected.

**A3. Meet the producer** *(Voice, about 3 minutes)*
```
┌─────────────────────────┐
│  Salma · producer       │
│                         │
│        ◉ ))))           │  ← voice orb, live captions under it
│  "What should Karim and │
│   Mona call you?"       │
│                         │
│ ─── Salma's notes ───── │
│ ┌ Name: Lina  🔊 ✎ ┐    │  ← cards slide in as she speaks
│ ┌ Could talk for hours │
│ │ about: Al Ahly      ✕┐│
│ ┌ English for: job    │ │
│ │ interviews (March) ✕┐ │
│                         │
│   (●) hold to talk  ⌨   │
└─────────────────────────┘
```
- Three questions, in the native language: *What should we call you?* (she says it, so the hosts learn the pronunciation), *What could you talk about for an hour?*, *What do you need English for?*
- **The notes are visible as they are written.** Each fact Salma hears appears as a card. A tap on ✕ removes it, ✎ corrects it. This is the learner model being born in front of the learner, and it is the first proof that "this knows me". It replaces the questionnaire with something better: a conversation that shows its work.
- **Two level moments, not a test.** Salma switches language once: "Can I try something? I'll say one line in English. Tell me what you heard, in any language." Then: "Now say anything back in English. Anything is fine." Those two moments plus the first call give the starting estimate. Nothing is labeled as a check.
- Everything else the PRD asks for (past attempts, people in their life, dated follow-ups) is gathered later, by the hosts and the producer, in small natural moments over week one. The planner already compensates for sparse fields.

**A4. Casting while the pilot is made** *(Eyes and ears, 40 to 90 seconds)*
```
┌─────────────────────────┐
│ Making your first       │
│ episode…  ▓▓▓▓▓░░░      │
│                         │
│ Your hosts              │
│ ┌──────┐   ┌──────┐     │
│ │ ◐    │   │ ◑    │     │
│ │Karim │   │ Mona │     │
│ │▶ hi  │   │▶ hi  │     │
│ │swap  │   │swap  │     │
│ └──────┘   └──────┘     │
│                         │
│ Accent you'd like       │
│ (●) UK   ( ) US  ▶ ▶    │
└─────────────────────────┘
```
- The wait becomes the one meaningful choice: who your hosts are. Each host plays a 5-second hello; "swap" offers another voice. The PRD's dialect choice lives here too, with short samples.
- If generation is fast, this screen can be skipped. It should never feel like a loading screen with something to do; it is casting.

**A5. The pilot** *(Ears, 2 to 3 minutes)*
- A short episode about the thing Lina said she could talk about for an hour, using her name once.
- The transcript is on screen, synced. One gentle hint points at the **Huh?** button (see B3) and at tapping a word. No other coaching.

**A6. The first throw and call** *(Voice, 60 to 90 seconds)*
- Karim: "Lina, settle this. Who's right?" The call screen opens (see B5).
- The first call is deliberately short and easy. Salma's talkback is introduced in one line in Arabic, in her closer voice: "If you're stuck, hold the button and ask me in Arabic."

**A7. The first notes** *(Eyes, 30 seconds)*
- One card only: something Lina did well that was new or hard ("You used *should have*. That's not easy."), plus at most one polish note. The first debrief teaches the format with a win.
- One sentence from Salma on how this works: "Every day: one episode, one call, and my notes. The more you talk, the better I make it."

**A8. Keep your show** *(Eyes, 60 seconds)*
```
┌─────────────────────────┐
│ Keep your show?         │
│ [  Continue with Apple ]│
│ [  Continue with Google]│
│ [  Use email           ]│
│                         │
│ When should tomorrow's  │
│ episode drop?           │
│ (●) On my commute 7:40  │
│ ( ) Lunch break         │
│ ( ) Evening walk        │
│ ( ) Pick a time         │
│                         │
│ ☐ Keep my recordings so │
│   I can hear my progress│
│   (only for you, delete │
│   any time)             │
└─────────────────────────┘
```
- The account comes after the learner has something worth keeping.
- **The cue is designed by the learner** (rethink decision 5), phrased in life terms, not hours.
- Voice-storage consent is asked at the moment it makes sense, right after they heard themselves on the call, with a plain sentence about what is stored and why.

**Timing compared to the PRD**

| | PRD v2.0 | Proposed |
|---|---|---|
| Screens before any sound | 4 (account, birth date, native, target) | 1 |
| First sound | After account setup | Under 60 seconds (Salma's voice) |
| Intake length | ~10 minutes, 12 to 18 turns | ~3 minutes, 3 questions + 2 language moments |
| First episode | 4 to 5 min, up to 3 min wait | 2 to 3 min pilot, wait used for casting |
| First speaking | After the full episode and article | Within 5 minutes of opening |
| Account | First | After the first call |

---

### Flow B. The daily episode

**B1. Today** *(Eyes, 2 seconds)*
```
┌─────────────────────────┐
│ Thursday                │
│ Mona: "Still can't      │
│ believe you called the  │  ← one line from a host,
│ new coach a genius."    │    always a real memory
│                         │
│ ┌─────────────────────┐ │
│ │   KARIM IS NOT OKAY │ │  ← typographic cover:
│ │   ◐ ◑               │ │    title, hosts, show color
│ │   The derby, and    │ │
│ │   who starts Sat.   │ │
│ │   7 min · call ·    │ │
│ │   article           │ │
│ │        [ ▶ Play ]   │ │
│ └─────────────────────┘ │
│  Why this episode? ›    │
│                         │
│  2 other ideas ⌄        │
│  🎙 Tell Salma an idea   │
│                         │
│  Today   Show   Notebook│
└─────────────────────────┘
```
- One hero episode, with its title, cast, length, and what it includes. The PRD's 3 to 5 pitches are behind "2 other ideas" so the screen keeps one decision.
- **Tell Salma an idea** replaces the "from scratch" form: hold and say "do something about my interview on Sunday, make Mona the interviewer". The producer confirms in one line and makes it.
- Long-press the cover to remix: chips for topic, format, cast.
- **Why this episode?** opens a short, honest explanation (see Flow E). This is how the hidden teacher becomes visible on demand.
- Three destinations only: **Today**, **Show** (the shelf of past episodes and seasons), **Notebook** (what Salma knows and your progress).
- Covers are typographic (title, show color, host marks), not generated images. They are cheap, consistent and make the shelf look like a real show's back catalog.

**B2. Today, in its other states**

| State | What the hero area shows |
|---|---|
| Before the drop time | The episode is ready anyway. The drop time controls the notification, not access. |
| Episode in progress | The same card with doors: **Listen ✓ · Call · Read · Chat**. Doors, not a progress bar: any order, any can be skipped. |
| Done for today | "That's today's show." Tomorrow's drop time, and the one-line teaser Salma chose. Below it, quietly: "You can have one more episode today." Nothing else. |
| Second episode done | "That's two today. Tomorrow's will be ready at 7:40." No button. |
| Weekly proof day | The proof episode sits above today's episode, with its own cover. |
| Back after two weeks | Exactly the same as any other day. The hosts may mention what changed in the world (Ahly lost twice), never that Lina was gone. |

**B3. The player** *(Ears, with optional eyes)*
```
┌─────────────────────────┐
│ ⌄  Karim is not okay    │
│                         │
│  Mona: and honestly I   │
│  think he's been        │
│ ▌KARIM: OVERRATED? He   │  ← current line large,
│ ▌scored twice on        │    karaoke highlight,
│ ▌Saturday!              │    any word tappable
│  Mona: Twice against a  │
│  team that…             │
│                         │
│ ──●──────────── 2:14/7:02│
│                         │
│  ⟲ line   ▶❚❚   0.9×   │
│                         │
│      [ Huh? ]           │
└─────────────────────────┘
```
- **⟲ line** replays the last sentence, not 10 seconds. Sentences are the unit learners need.
- **Huh?** jumps back one sentence, slows it to 0.85×, and shows that line with glosses under the hard words. It is the most important button in the player: an honest, one-tap signal of "I didn't get that", which feeds the learner model better than any test. The number of Huh? taps per minute falling over weeks is real evidence of comprehension.
- Speed: 0.75×, 0.85×, 1.0× (rethink: slower helps; keep the 1.0× cap).
- The transcript can be hidden for listening-only practice; the planner can suggest it as the learner grows.

**B4. Tap a word** *(Eyes)*
```
┌─────────────────────────┐
│ overrated   🔊           │
│ مُبالغ في تقديره          │
│ "He's overrated, honestly."   │
│                         │
│ [ Keep this word ]      │
└─────────────────────────┘
```
- Meaning in the native language, the sentence it came from, tap to hear. **Keep** sends it to the notebook and tells the planner to bring it back in later episodes. The PRD excluded audio here; I would include it, because learners need to hear a word to say it.

**B5. The throw becomes the call** *(Voice)*
At the end of the episode, Karim throws to Lina. The player turns into an incoming call, the way a podcast host takes a caller.
```
┌─────────────────────────┐
│                         │
│        ◐                │
│      Karim              │
│   wants your take       │
│                         │
│ "Who starts Saturday?"  │
│                         │
│  [ Read the article ]   │
│                         │
│  ( Later )   ( Call ✆ ) │
└─────────────────────────┘
```
- **Call** now, **read first**, or **later**: the doors model. In Ears mode the same choice is spoken, and pressing play on the headphones accepts the call.

**B6. The call** *(Voice)*
```
┌─────────────────────────┐
│ Karim · 2:41            │
│                         │
│        ◐ ))))           │
│                         │
│ Karim: So you'd start   │  ← host captions on by default,
│ him because he          │    recast words in bold
│ **scored twice**. Fair. │
│ But Saturday…           │
│                         │
│ ┌─────────────────────┐ │
│ │  hold to keep the   │ │  ← large pad: while held,
│ │  floor              │ │    Karim waits
│ └─────────────────────┘ │
│  S  ask Salma   🔇  ✕   │
└─────────────────────────┘
```
- **Open mic by default**, with generous pause tolerance at lower levels. A natural backchannel from the host ("mm", "go on") while the learner pauses, so silence does not feel like failure.
- **Hold to keep the floor.** Touch and hold anywhere on the pad: the host waits, however long the learner needs to think. Release to hand back. This turns the scariest part of a voice call (the AI jumping in while you search for a word) into something the learner controls.
- **Ask Salma (talkback).** Hold the S button and say it in Arabic: "how do you say تشكيلة?" Salma whispers "line-up" in the learner's ear; Karim does not react. In Ears mode, saying the question in Arabic does the same.
- **Captions.** The host's words are captioned by default (reading while listening helps comprehension; the rethink cites it). The recast form appears in bold in the caption, so the learner can notice it without the host stopping. The learner's own words are not captioned live: watching your own errors appear while speaking raises anxiety. They appear in the debrief.
- **No correction UI exists on this screen.** No red, no ticks, no score.
- **Retell.** Once per call the host may ask for a quick retell ("Mona missed it. Sixty seconds, go."). The screen shows a soft 60-second ring that never turns red and never cuts the learner off.

**B7. The debrief** *(Eyes, optional, 30 to 90 seconds)*
```
┌─────────────────────────┐
│ Call with Karim         │
│ 6:12 · you spoke 3:40   │
│                         │
│ Salma's notes (3)       │
│ ┌─────────────────────┐ │
│ │ NEW FOR YOU         │ │
│ │ "If he had played,  │ │
│ │  we would have won" │ │
│ │ First time you used │ │
│ │ this. ▶ hear it     │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ POLISH              │ │
│ │ You: "I go to the   │ │
│ │ stadium yesterday"▶ │ │
│ │ Natural: "I went to │ │
│ │ the stadium         │ │
│ │ yesterday"        ▶ │ │
│ │ [ 🎙 Say it once ]   │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ A WORD YOU REACHED  │ │
│ │ FOR                 │ │
│ │ You said "the list  │ │
│ │ of players who      │ │
│ │ start" → line-up  ▶ │ │
│ └─────────────────────┘ │
│        [ Done ]         │
└─────────────────────────┘
```
- Written by the producer, not the host. At most three cards, one swipe each.
- **Three card types**, in this order:
  1. **New for you**: one real thing the learner did that they could not do before. Not praise; evidence.
  2. **Polish**: their sentence, in their own voice, next to the natural version. Tap to hear, say it once. No score after saying it; the producer just moves on. This is the rethink's "3 things to polish" card.
  3. **A word you reached for**: where the learner talked around a word they didn't have, the producer gives it. Learners rarely get this feedback anywhere, and it is exactly what they wanted in the moment.
- "You spoke 3:40" is information, not a target. It is the honest number for the most important behavior in the product.
- First time only: "Want my notes after each call?" Yes / Only when it matters / No. The learner controls how much teacher they want.

**B8. Read** *(Eyes, 3 to 5 minutes)*
- A clean reading screen, generous type, every word tappable, a ▶ to hear the article read (reading while listening).
- The article's job is shown at the top in one line from Karim: "This is what I'll throw at you on the call." The article arms the learner; the call uses it.
- A sentence can be long-pressed to hear it or to keep it.

**B9. Chat** *(Eyes, 2 to 4 minutes)*
```
┌─────────────────────────┐
│ ◐ Karim                 │
│ ── Thu · Karim is not   │
│    okay ──              │
│      ok but you dodged  │
│      the real question  │
│      who starts Sat? ◐  │
│                         │
│ ◑ Lina: I think he will │
│   start because he is   │
│   more experience       │
│   ✎ 1 note              │  ← collapsed margin note
│                         │
│ ┌ Salma ───────────────┐│
│ │ more experienced:     ││  ← expands on tap
│ │ "more" + adjective.   ││
│ └──────────────────────┘│
│                         │
│ [ message…        ] 🎙 │
└─────────────────────────┘
```
- One long thread per host, across days, with date separators named after episodes. The relationship lives in the thread, like a real chat.
- **Margin notes**: written correction is the best-evidenced correction type (the rethink cites g ≈ 0.68 for focused written feedback), and writing is where it interrupts nothing. A small "✎ 1 note" chip under the learner's bubble, from Salma, collapsed. At most one per chat. The host never mentions it.
- Arabic and English mix in one bubble often. Each bubble sets its own text direction automatically.

**B10. The wrap** *(Ears and eyes, 10 seconds)*
- A short outro sting, the hosts' sign-off, then: "That's today's show. Tomorrow at 7:40: Mona interviews you for the job." The app has nothing else to offer. This ending is part of the design, not a dead end.

---

### Flow C. Ears-only: the commute

The concept is a podcast. A podcast lives on the lock screen, in the car and in headphones. This flow is the strongest argument for a native app (decision 2).

**C1. Lock screen and car**
```
┌─────────────────────────┐
│ 07:41                   │
│ ┌─────────────────────┐ │
│ │ KARIM IS NOT OKAY   │ │
│ │ For one · ch. 2/3   │ │
│ │ ⟲line   ❚❚   ★mark │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

**C2. Headphone and car buttons**

| Button | In the episode | In the call |
|---|---|---|
| Play / pause | Play / pause | Accept the call when it rings; mute |
| Previous track | Replay the last sentence | Repeat what the host just said |
| Next track | **Mark this moment** (saved for later, like a podcast clip) | Ask Salma (talkback) |
| Long press / voice | "Hey Salma, what did he say?" | Speak in Arabic to ask for a word |

Marked moments appear in the notebook later with their sentence and audio. It is the Ears-mode version of tapping a word. These use the app's own previous and next actions only; they never take over a system gesture such as the AirPods triple-click (Snipd users called that "a deal breaker"). In the car, CarPlay and Android Auto give audio apps only the standard Now Playing screen, so the call there is voice-only by design.

**C3. The audio flow**
```
7:40  drop notification: "Karim vs Mona: the derby (7 min)"
      ▼ tap or press play
[sting] episode 7 min ──► Karim: "Lina, call in."
      ▼ chime + Karim's breath
      call 5 min (open mic, talkback on next-track)
      ▼ Karim signs off
[sting] Salma, 15 sec: "Two notes waiting when you have your phone. Article's ready for lunch."
      ▼ end. Nothing autoplays.
```
- The session splits naturally: Ears on the bus, Eyes at lunch (article, chat, notes). The Today card shows which doors are still open.
- Private podcast feed (rethink): good for the episode, but the call cannot happen inside another podcast app. If you use the feed, the episode's last minute says "open For one to call in", and a link in the episode notes opens the call. Worth testing in Milestone 0, because it puts the show inside a habit learners already have.

---

### Flow D. Corrections without breaking flow

The rethink changed the correction law from recast-only to "recast, nudge, polish". Here is where each layer lives and what it looks like.

| When | Who | What the learner experiences | Visible? |
|---|---|---|---|
| During the call | Host | A clear recast, slightly stressed: "You *went*? With who?" | In bold in the host's caption only |
| During the call, once at most | Host | A natural nudge: "Wait, yesterday you...?" with a pause for self-repair | Heard only |
| During the call, on request | Producer (talkback) | A word or phrase whispered in the ear | Shows the word in a small bubble from S |
| Right after the call | Producer | Debrief: up to 3 notes (new / polish / word you reached for) | Yes, opt-in |
| In the chat | Producer | One collapsed margin note under one message | Yes, collapsed |
| Any time | Producer | "Why do you say it like that?" answered plainly, in the native language if needed | Yes, on request |
| Weekly | Producer | The proof: patterns that have disappeared, one that is next | Audio + one screen |
| Across weeks | Planner | The fixed form shows up again in new episodes, spaced | Invisible |

Rules for every layer:
- Never while the learner is speaking or writing.
- Never more than three things in one sitting.
- Always the learner's own sentence first, then the better one.
- Always pair with one real thing they did well, when one exists.
- Never a number, never a grade.

---

### Flow E. The notebook: the teacher's file, open to the learner

The PRD keeps the learner file entirely hidden and offers a text summary "on request". I would make the notebook a real place, styled like a producer's notebook, not like settings.

**E1. Notebook home**
```
┌─────────────────────────┐
│ Notebook                │
│ Salma's notes on Lina   │
│                         │
│ What I'm working on     │
│ with you                │
│ · Past tense in stories │
│ · Talking about plans   │
│   ("I'm going to…")     │
│ · 6 words from this week│
│                         │
│ About you          (14) │
│ Words you own      (212)│
│ The tape            (3) │
│ Out in the world    (4) │
│ Marked moments      (9) │
│                         │
│ Controls ›              │
└─────────────────────────┘
```

**E2. About you.** Every fact Salma holds, each with where it came from ("you said on Oct 3: ..."), and ✎ / ✕ on each. Facts the system is unsure about are shown as "I think..." and never used in the show until confirmed. This is the trust contract made visible.

**E3. Why this episode?**
```
┌─────────────────────────┐
│ Why I made this one     │
│                         │
│ · You said on Monday    │
│   the derby was Sunday. │
│ · It brings back 4 words│
│   from this week:       │
│   line-up, bench, …     │
│ · Karim will push you to│
│   talk about plans:     │
│   "Who's going to…"     │
│ · Shorter than usual:   │
│   you've been busy.     │
│                         │
│ Not quite right?        │
│ 🎙 Tell Salma            │
└─────────────────────────┘
```
- The concept's feature test includes "the feeling of being known". Nothing creates that feeling more than seeing your own reasons. It also gives the learner a way to steer the teacher.
- The learner can turn off "what I'm working on" if they would rather not see the targets. Default: shown in the notebook, never in the show.

**E4. Controls** (a short sheet, not a settings app)
The PRD bans settings screens. I agree with the spirit: most preferences should change by telling Salma. But a few things must be reliable, fast and findable without a conversation:
- Drop time and whether to get the drop notification
- Captions on calls; transcript in the player; default speed
- Notes after calls: always / when it matters / never
- Keep my recordings: on / off, with "delete all recordings"
- See, export, delete all my data
- Sign out

Everything else (hosts, topics, tone, "talk slower", "less football") is a sentence to Salma.

---

### Flow F. Progress without game elements

The rethink allowed honest, informational progress. Here is what it looks like. The rule: progress is shown as **evidence the learner recognizes**, never as a **score they chase**.

**F1. Words you own**
A word is "owned" when the learner used it correctly, unprompted, in two different sessions. Each entry shows the sentence the learner said, with date and audio.
```
  line-up      "The coach changed the line-up again"  ▶  Oct 12
  overrated    "I think he is overrated, honestly" ▶  Oct 9
  negotiate    "I want to negotiate the salary"   ▶  Oct 7
```
The count (212) is shown once at the top, quietly. It only goes up. There is no target number.

**F2. The tape**
```
┌─────────────────────────┐
│ The tape                │
│ Same question, every    │
│ season.                 │
│                         │
│ ┌────┐ ┌────┐ ┌────┐    │
│ │ S1 │ │ S2 │ │ S3 │    │  ← cassette-like tiles
│ │Sep │ │Oct │ │Nov │    │
│ │0:48│ │1:31│ │2:05│    │  ← length of answer
│ └────┘ └────┘ └────┘    │
│                         │
│ [ ▶ Play S1 then S3 ]   │
│                         │
│ Salma: "In September you│
│ stopped 11 times. In    │
│ November, 3."           │
└─────────────────────────┘
```
- Every 4 weeks, the season finale includes the same kind of prompt (the rethink's 4-weekly speaking sample). The tape is where the learner hears it. This is the single most motivating screen in the product, because it uses the one measuring instrument everyone trusts: their own ears.

**F3. Seasons instead of streaks**
- The show runs in 4-week seasons with a title Salma picks from what happened ("Season 2: Interview season").
- A season cannot be broken. It ends on its date whether the learner did 3 episodes or 40.
- Each season ends with a finale: the speaking sample disguised as a special episode, plus a short recap (episodes, hours listened, minutes spoken, words owned, the moment Salma liked most). It is a retrospective, like a year-in-review, not a report card.
- The Show tab is a shelf of seasons, each a row of episode covers.

**F4. Out in the world**
When the learner tells the show they did something real ("I had the interview!"), Salma writes it down. The concept's ninth law ("the show is the gym; life is the game") becomes a page: real conversations, real wins, dated. This is the win the product celebrates most.

**F5. Hours**
"41 hours listened, 6 hours spoken" appears in the notebook and in the season recap. Cumulative, never reset, no goal bar, no milestones that light up. Dreaming Spanish shows that learners find a growing hours count motivating; For one takes the count and leaves out the daily goal and streak calendar Dreaming Spanish puts next to it. Hours measure time, not retention, so they always sit next to words you own and the tape.

**F6. The weekly proof**
Two minutes of audio, opened from its own cover on Today. One screen accompanies it: the side-by-side clips, the 1 to 3 named wins, and the next focus, as text. On a flat week, it says so ("Flat week. Here's what I'm changing.") and names the change.

**Never shown:** percentages, levels, CEFR, rankings, rings, bars that fill, "x days in a row", comparisons with other learners, confetti.

---

### Flow G. The hard moments

| Moment | Design |
|---|---|
| Freezing on the call | Hold to keep the floor; ask Salma; after 8 seconds of silence the host offers a smaller version of the question, never repeats the same one louder |
| Didn't understand the host | Say "sorry?" or "slower" in any language; the host rephrases more simply. Previous-track replays the last host line |
| Bad connection mid-call | Switch to voice notes in the same argument (PRD); the screen says "Weak signal. Let's do voice notes." and keeps the thread |
| Wants to stop early | ✕ ends it at any time. The host closes like a person ("Fine, but this isn't over"). Nothing is lost or penalized |
| Hits the daily cap | "That's two today. Tomorrow's is ready at 7:40." Plain, from Salma, not in character as an excuse |
| Upset or overwhelmed | Salma can say "Do you want an easier one tomorrow?" when the signals suggest it; the learner can say "today was too hard" at any time |
| Asks "are you real?" | Everyone answers honestly: AI, made for you. The hosts never pretend to have a life outside the show |
| Wants to leave | Delete account is in Controls, two taps, no survey wall, no "Karim will miss you" |

---

## 5. What adjacent products teach

What the best-designed products in neighbouring categories do well and badly, and what For one should take. Every observation is sourced (list at the end); lines marked *inferred* are my reading.

| Product | Take | Avoid | For one |
|---|---|---|---|
| **Duolingo Video Call (Lily)** | The call as a named moment; captions added for beginners; Push-To-Talk added to stop Lily "interrupting mid-sentence"; feedback after the call on "how you can sound more natural"; Lily remembers past calls | Calls that end after 2 or 3 exchanges; one character only; a bug where Lily asked the same breakfast questions every call; off-topic answers pushed back to the script; "our characters got pushier" notifications | Hold to keep the floor and post-call notes are now proven needs, not nice ideas. Two hosts with real opinions and memory beat one scripted character |
| **Speak** | Fast, tight speaking reps; a short summary of errors after a roleplay | Speech scoring "overly lenient", giving "a perfect score" to wrong sentences and "a false sense of mastery"; saved phrases "never reintegrated" into later chats | Never show a score you can't stand behind. Kept words must come back in later episodes, which is the planner's job |
| **Praktika** | Some users love an avatar teacher | Others find "low grade" avatars distracting and want voice only; level mismatch ("assumes you have a knowledge of Spanish already"); repetition inside a lesson; hard-to-cancel billing | Voices and simple marks, not faces. Level fit is a design problem, not only a model problem (Huh? taps, coverage checks). Cancel in two taps |
| **Dreaming Spanish** | Progress as hours of input with plain-language milestones ("you can understand a patient speaker"); logging outside hours; learners call watching hours grow "very motivational"; a stated goal of making itself unnecessary | It also has a daily goal, a streak and hours-to-next-level, which For one should not copy; hours measure time, not what was retained | Hours, yes, but next to evidence of retention (words you own, the tape). "Out in the world" is the outside-hours log, made personal |
| **ChatGPT voice, Sesame** | OpenAI made voice "more tolerant of pauses" and moved from a full-screen orb to voice with a live transcript; Sesame's research names timing, pauses, emphasis and a consistent personality as what makes a voice feel present | Language learners: it cuts in after 1 to 2 seconds of silence ("since I'm not fluent I need to pause a lot"); hyper-real voices impress some people and feel "very creepy" to others | Generous pauses plus a floor control the learner owns. Captions by default. Natural but plainly AI |
| **Calm, Headspace** | Daily Calm: a new session every 24 hours, same narrator, one play button on the home screen ("no gulf of execution"); Headspace's Today tab changes by time of day, switching to sleep content in the evening | A Today screen that grows into a checklist of essentials turns a ritual into tasks (*inferred*) | One episode, one button, same hosts. Today can change by time of day: the full episode in the morning, a short chat or an easy listen at night |
| **Podcast and audiobook apps** | Apple Podcasts: word-synced transcripts, tap a word to jump there; Snipd: tap your headphones to save a moment with its clip and transcript; Audible: sleep timer to end of chapter, car mode, speed in small steps | Snipd's snip gesture overrode the AirPods triple-click and couldn't be changed ("a deal breaker"); CarPlay only allows the standard Now Playing screen, so no custom screens in the car | Mark a moment with the app's own next-track action, never by taking over a system gesture. In the car the call is voice-only by design |
| **AI companions (Replika, Character.ai, Pi)** | Visible, editable memory (Replika's memory tab; Character.ai's pinned memories and editable facts); Pi praised as patient and non-judgmental with continuity across sessions | 37% of companion farewells used manipulation, raising engagement through anger and curiosity, not enjoyment; persona changes after an update caused real grief; wrong auto-captured facts kept shaping replies | The notebook's "About you" with sources and "I think..." facts is the safe version. Clean, warm goodbyes. Never change a host's voice or personality silently |
| **LingQ, Readlang, Language Reactor** | Every word tappable; looked-up words fade as you meet them again; a rising known-word count builds confidence; tap a phrase for a phrase meaning | "Clunky and not at all visually appealing"; saved words that only become flashcards | Tap any word or phrase in the transcript and article, and send kept words back into the show rather than into a deck |

**Cross-cutting lessons**
1. Being interrupted while searching for a word is the most common failure in voice practice. Give the learner the floor.
2. Correction belongs after the call, as a short review with the learner's own words. Lenient scores and missing corrections both destroy trust.
3. Memory should be visible, editable and quiet. Repetition (asking the same thing again) is the fastest way to break the feeling of being known.
4. Progress without a game works when it is true: hours plus evidence of retention.
5. A daily ritual is one item, one button, one consistent voice.
6. Audio-first means lock screen, car and headphones first, using system controls rather than fighting them.
7. Goodbyes must be clean. The engagement manipulative farewells buy is anger, and it costs trust.
8. Keep each host the same person across updates, and keep it plainly an AI.

---

## 6. Platform: why voice-first pushes toward native

The PRD says "responsive web app, no native apps in v1". From the UX side, that is the riskiest platform choice in the document, because the best moments in this design are exactly the ones phone browsers handle worst.

| Need | Native app | Mobile web / home-screen web app |
|---|---|---|
| Keep playing with the screen locked, lock-screen and car controls | Standard | Partly possible (Media Session API), but background audio in home-screen web apps on iPhone has a history of being unreliable |
| Headphone buttons mapped to "replay sentence" / "mark moment" | Yes | Partly (previous/next track actions where supported) |
| A hands-free call with the screen off | Yes (audio session, call-style UI) | No reliable way to keep the mic open in the background |
| The daily drop notification at a chosen time | Yes, local or push | iPhone: web push only for home-screen installs |
| Low-latency voice in noisy places | Better control of echo and audio routing | Depends on the browser |

My recommendation (decision 2): build Milestone 0 with no app at all, then the beta as a native app with one codebase for both phones. The web stays for sign-up, the notebook on a laptop, and sharing.

**Milestone 0 without an app.** The concept's sixth law says "formats are hijacked, not invented". Milestone 0 can follow it literally: the episode in a private podcast feed, the call as a real voice call or voice notes in a messaging app, the article and debrief as a message, the notebook as a shared doc. If people want the next episode in that crude form, the app will only make it better. Watch what testers do with those formats (when they listen, whether they call, whether they read the notes) and design the app from that.

---

## 7. Look, sound and language

**Look.** An audio show, not a classroom: typography-led, with each learner's show having its own color, and covers that look like a real show's back catalog. No mascot, no cartoon, no characters in costume. Hosts are represented by simple portrait marks, not realistic avatars: realistic AI faces fall into the uncanny valley and add cost, and podcast loyalty is built on voices, not faces. Dark mode as a first-class theme, because much listening happens early and late.

**Sound.**
- A show sting (3 to 4 seconds) that opens and closes each episode. Ideally each learner's show gets its own, chosen from a library.
- Your turn is signaled by the host's breath and a soft rising tone, not a beep.
- The producer's voice is close and dry, like a voice in your headphones. The hosts sound like they are in a room.
- No reward sounds, no fanfare.

**Language and direction.** The likely first pair (rethink decision 2) is English for Arabic speakers. That makes bidirectional text a first-day requirement, not a later fix:
- The interface, Salma and the notes are in Arabic, right to left. Episode transcripts, articles and host chat are English, left to right.
- Glosses in the word sheet are Arabic inside an English context; chat bubbles mix both. Every text block sets its direction from its content.
- Pick a type pairing that works for Arabic and Latin together (for example, an Arabic face with a matching Latin companion) and test line height with mixed lines.
- The producer's balance of languages shifts over time: mostly Arabic in season 1, more English as the learner grows. This shift is itself a quiet sign of progress.

**Accessibility.** Captions everywhere audio plays. Adjustable text size and line spacing in reading. Transcript-first mode for hard-of-hearing learners. Hold to keep the floor also helps learners who stutter or process slowly. Every control reachable with screen readers; the karaoke transcript announces lines, not words.

---

## 8. How to test the experience

**Measures that tell you the design works** (add to the PRD's Part 15):

| Measure | Target for Milestone 0 | Why |
|---|---|---|
| Time from first open to first sound | < 60 seconds | First impressions; the PRD has no number for this |
| Time from first open to the learner's first spoken sentence | < 5 minutes | Speaking is the scariest step; it should come early and small |
| Learner speech per session | ≥ 4 minutes (rethink gate) | The behavior that matters most |
| Sessions done without looking at the screen for the episode | Track it; expect > 40% if the commute case is real | Confirms or kills the Ears-first bet |
| Huh? taps per episode minute | Falling over 4 weeks | Comprehension evidence without tests |
| Debrief cards opened and "say it once" used | > 50% of calls | Whether the teacher layer is wanted |
| Notebook fact edits | Any, in week 1 | Whether the glass box builds trust |
| Talkback use per call | Falls over time | Dependence shrinking is progress |

**Prototype order.**
1. Milestone 0 with hijacked formats (podcast feed, voice call, messages, a doc). No screens.
2. A clickable prototype of Flows A and B (Figma or similar) with real audio, tested with 5 learners in person. Watch the first session; it is where most products lose people.
3. Wizard-of-Oz calls: a person plays the host with a script and the talkback button, to learn when learners freeze and what they ask for.
4. Only then, the beta app.

---

## 9. What I would cut or defer from the UI

- The 3 to 5 pitch list on the home screen. One hero, two behind a tap.
- Character creation flows in the beta (agrees with the rethink). Swap a voice, rename a host, that's all.
- A free-text format builder. "Tell Salma an idea" covers it.
- Realistic video avatars. Voices and simple marks.
- Any chart, now or later.
- Social sharing of proof clips (the PRD already excludes it). A learner can download their own tape; that is enough.

---

## Sources

The research and evidence claims rely on the first rethink's sources. Platform statements on mobile web audio, microphone and push are from general platform knowledge and should be checked against current iOS and Android releases before the build decision.

**Adjacent products (section 5)**
- Duolingo Max: https://blog.duolingo.com/duolingo-max · product highlights: https://blog.duolingo.com/product-highlights/ · video call research: https://blog.duolingo.com/video-call-research-report
- Duolingo Max reviews: https://davidwilliamrosales.com/2025/09/27/duolingo-max-review/ · https://copycatcafe.com/blog/duolingo-max
- Speak review: https://languatalk.com/blog/speak-app-review/
- Praktika reviews: https://www.trustpilot.com/review/praktika.ai?page=2 · https://www.trustpilot.com/review/praktika.ai?page=6 · https://www.trustpilot.com/review/praktika.ai/location/headquarter
- Dreaming Spanish: https://palteca.com/dreaming-spanish-review · https://www.fluentu.com/blog/reviews/dreaming-spanish/ · https://learningspanish.bearblog.dev/my-spanish-learning-journey-after-1420-hours-of-immersion/
- ChatGPT voice: https://community.openai.com/t/feature-request-advanced-voice-mode-keeps-interrupting-me/962909 · https://macmyths.com/openai-says-chatgpt-voice-is-better-at-conversation-what-changed/ · https://www.androidauthority.com/chatgpt-voice-mode-in-chat-3619633
- Sesame: https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice · https://getcoai.com/news/sesames-ai-voice-presence-creates-emotional-bonds-with-human-like-imperfections
- Calm and Headspace: https://support.calm.com/hc/en-us/articles/115005140414-Calm-Dailies · https://ixd.prattsi.org/2018/01/design-critique-calm-ios-app/ · https://help.headspace.com/hc/en-us/articles/51443842967195-Refreshed-Today-Tab-Experience-June-2026
- Podcasts and audiobooks: https://mobilesyrup.com/2024/03/05/apple-podcasts-transcripts-update/ · https://apps.apple.com/app/id1557206126 · https://www.tapsmart.com/apps/review-snipd/ · https://www.androidauthority.com/audible-listening-settings-3667303/ · https://developer.apple.com/documentation/carplay/cpnowplayingtemplate
- AI companions: https://www.library.hbs.edu/working-knowledge/how-ai-chatbots-try-to-keep-you-from-walking-away · https://arxiv.org/abs/2508.19258 · https://arxiv.org/abs/2412.14190v1 · https://help.replika.com/hc/en-us/articles/37208679176077-How-does-Replika-s-memory-work · https://www.roborhythms.com/character-ai-adds-chat-memories/
- Reading tools: https://www.fluentu.com/blog/lingq-review/ · https://jalt-publications.org/articles/28605-enhancing-functionality-youtube-and-netflix-language-reactor · https://the-ofla-cardinal.org/2023/05/10/readlang-a-useful-tool-to-support-language-acquisition-through-reading-for-pleasure/
- Speaking anxiety and AI practice: https://ideas.repec.org/a/pal/palcom/v12y2025i1d10.1057_s41599-025-05550-z.html
