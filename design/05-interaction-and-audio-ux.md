# For one — 05. Interaction and audio UX

*Part 5 of 8. How listening, speaking and waiting feel. Sound is interface (principle P9): this document specifies the sounds, the turn-taking, the latency masking, the headphone and lock-screen behaviour, and the hard moments. Numbers marked "target" are design targets to measure in the pilot, not guarantees.*

## 1. Listening

### 1.1 The player's unit is the sentence
- **⟲ line** replays the last sentence (from word timings), not 10 seconds.
- **Huh?** replays the last sentence at 0.85×, shows that line with glosses under hard words, and logs an honest comprehension signal. Two Huh? on the same line keeps the gloss open. Huh? per minute falling over weeks is evidence; it is never shown to the learner as a number.
- Speeds: 0.75×, 0.85×, 1.0×. No speed above 1.0× (the show is already pitched at ~95% known words; faster is not the goal).
- Audio-first: for intermediates the transcript is folded on the first play of each episode. "Show words" opens it; the preference sticks per learner and the planner may suggest folding again as they grow.
- Tap any word: a sheet, playback continues (the sheet never pauses audio).

### 1.2 Sound design of an episode
| Element | Spec |
|---|---|
| Show sting | 3 to 4 seconds, opens and closes every episode; one per learner's show, chosen at casting from a library of about 12 (the learner can change it by telling Salma) |
| Cold open | 30 seconds; no sting before it; the sting lands after the cold open, like a real show |
| Hosts | Two voices "in a room": light room tone, consistent levels (loudness normalised to −16 LUFS integrated), panned slightly apart (Karim 15% left, Mona 15% right) so they are distinguishable with eyes closed |
| Salma | Close and dry, no room tone, mono-centred, 2 dB quieter than the hosts: a voice in the headphones, not in the room |
| Your turn | The host's breath plus a soft rising two-note tone (200ms); never a beep |
| Transitions | Episode → call: the sting's tail crossfades into a phone-style chime (600ms); call → wrap: the host's sign-off, 1 second of silence, the closing sting |
| Reward sounds | None. No chime on Keep, no fanfare on the proof, no sound on a ✓ |
| Errors | System failures use a single low thud (100ms), never for anything the learner said |

## 2. Speaking

### 2.1 Turn-taking
- **Open mic by default.** The host's end-of-turn detection waits longer than a consumer assistant: silence threshold 1.6s (target) at lower levels, 1.2s at higher, adapted per learner from their own pause lengths over the first week.
- **Backchannels.** While the learner pauses under the threshold, the host may breathe or say "mm", "go on", "right" at low volume. Backchannels never overlap the learner's speech.
- **Hold to keep the floor.** While the pad is held, end-of-turn detection is off and the host does not speak, however long. Release hands the turn back after 400ms, so a late syllable is not cut.
- **Barge-in.** The learner can talk over the host; the host yields within 300ms and does not resume the interrupted sentence (it rephrases if needed). The host never barges in on the learner.
- **Silence.** After 8 seconds with no hold and no speech, the host offers a smaller version of the question. It never repeats the same question louder, and never says "are you there?" before 20 seconds.

### 2.2 The word button
Hold the round **word** button, say the word or phrase in your own language, release. The host gives it back in the target language inside its next line ("line-up, yes, the line-up") and continues the thought. The given word appears once in the host's caption. The host, not Salma, gives it; Salma is silent during calls. In the beta this is button-only; a spoken "how do you say…" is a later addition.

### 2.3 Echoes (the only correction the learner ever meets)
- The host answers an error as a friend would, using the right form: "oh, you *went* there yesterday? And what happened?"
- In the caption, the echoed form is set at weight 600 in `--recast`. No underline, no icon, no tap target, no pause.
- When meaning is lost: "sorry, you what?", "the what?", once, then a rephrase of the host's own question.
- The host never says "wrong", "actually", "the correct way is", "you should say". These strings are blocked in the host prompt and checked by the editor role.

### 2.4 The retell
Once per call at most. The host asks ("Mona missed it. Sixty seconds, go."). A soft ring around the pad counts 60 seconds in the learner colour at 30% and simply completes; the host waits for the learner to finish regardless. The ring is never red and never cuts off.

### 2.5 Pronunciation, light
Tap any word to hear it; shadow two lines (the player can loop a line with a 1s gap); "say it once" after the hosts, offered in the chat or the small door. The engine may score a known sentence internally; no score reaches the screen.

## 3. Latency masking

Latency is the enemy of a conversation. The pipeline target is a host reply within about one second of the learner's end of turn (language gate check). The UI covers the gap so that it never feels like a machine thinking.

| Gap | What the learner hears and sees |
|---|---|
| 0 to 400ms | Nothing; this is a natural pause |
| 400 to 1200ms | The host's breath (pre-recorded per host, 6 variants, random) at 400ms; the orb shifts to a slow "thinking" breath |
| 1.2 to 2.5s | A filler in the host's voice from a small pre-synthesised set ("hmm", "okay so", "right", 8 variants per host, played at most once per turn) |
| > 2.5s | The host's first clause is streamed as soon as the model's first sentence is ready; captions start with it |
| > 6s (connecting) or > 10s (mid-call) | "Weak signal. Let's do voice notes." The same argument continues as voice notes on the same screen |

Rules: never a spinner, never "thinking…", never a typing indicator. Fillers are tagged so the analyst can exclude them from the transcript.

Episode generation is never waited for in front of the learner: episodes are made overnight; the pilot in onboarding is masked by casting; the sample page states "60 to 90 seconds" and shows the two orbs "recording".

## 4. Headphones, lock screen, car

| Control | In the episode | In the call | In the proof |
|---|---|---|---|
| Play / pause | Play / pause | Accept the ring; mute / unmute | Play / pause |
| Previous track | Replay the last sentence | Repeat what the host just said | Replay the clip |
| Next track | Mark this moment (toast "Marked", saved to the notebook with its sentence and audio) | Hold-equivalent: toggles "keep the floor" | Skip to "now" clip |
| Long press (where the platform exposes it) | Not used; system gestures are never overridden | | |

- The app uses the platform's media actions only; it never captures AirPods triple-click or the like.
- Lock screen: cover (dark), title, show name, scrubber; the two custom actions above where supported.
- Car (CarPlay / Android Auto): the standard Now Playing only; the call is never offered; the episode's last minute says "open For one to call in when you're parked".
- Web: Media Session API gives title, artwork, play/pause, seek, and (where supported) previous/next mapped as above. The call needs the screen on; the "keep the screen on" hint shows once.

## 5. Touch and gesture

- Hold pad: touch and hold anywhere on it; pressure not required; haptic tick (light) on hold start and release on native; a 2px ring breath while held.
- Word button: hold to speak; a light haptic on release.
- Transcript: tap a word (the sheet), long-press a sentence (hear it / keep it); scrubbing on the scrubber only, never on the transcript.
- Sheets: drag down or tap outside to dismiss; a sheet never blocks playback.
- No swipe-to-delete anywhere (a wrong memory is deleted by its ✕, in view). No pull-to-refresh (there is nothing to refresh; the day is made).

## 6. Voices and presence

| Voice | Spatial | Dynamics | Personality cues |
|---|---|---|---|
| Hosts | In the room, slightly panned | Normal conversational | Each host has a fixed set of verbal habits written by people (06 §2); the model only writes the episode |
| Salma | Close, dry, centred, quieter | Calm | Fewer words; never exclaims; never a joke at the learner's expense |
| The learner's own recordings | As recorded, lightly levelled, no processing that changes how they sound | | On the tape, played back without any filter: the learner must recognise themselves |

The host's voice in the call must be the same voice as in the episode (one voice vendor for both in the beta). A voice change after an update is treated as a bug: the companion-app research shows persona drift causes real grief.

## 7. The hard moments (interaction answers)

| Moment | The ear | The screen |
|---|---|---|
| Freezing | The host waits; after 8s, a smaller question | The hold pad is the biggest thing on screen; the word button is beside it |
| Didn't understand | "slower" / "sorry?" in any language makes the host rephrase simply | Previous-track replays the host's last line |
| Bad connection | "Weak signal. Let's do voice notes." | The pad becomes a record button; the thread continues |
| Wants to stop | The host closes like a person | ✕ is always visible; nothing is lost |
| Allowance reached | Salma's plain line (not in character) | One sentence on Today, no button |
| Overwhelmed | Salma next day: "Easier one tomorrow?" | A yes / no card on Today, once |
| "Are you real?" | Everyone answers honestly: AI, made for you | Also a one-line "about" in Controls |

## 8. Accessibility in interaction
- Captions for every host line; transcript-first mode enlarges call captions to 24 and keeps them persistent.
- The hold pad serves learners who stutter or process slowly; nothing times out while held.
- Screen readers: the hold pad announces "hold to keep the floor; the host waits while you hold"; captions are a polite live region; orbs are decorative.
- Reduced motion: orbs static at mid-amplitude; captions appear per line rather than per word.
- Haptics are optional (Controls follows the system setting).

## 9. Measures that tell the interaction works (pilot targets)
| Measure | Target | Why |
|---|---|---|
| First open to first sound | < 60s | First impressions |
| First open to first spoken sentence | < 5 min | Speaking early and small |
| Learner speech per session | ≥ 4 min | The behaviour that matters most |
| Host reply latency (end of learner turn to first audio) | median ≤ 1.2s, p95 ≤ 2.5s | Conversation, not a machine |
| Host barge-ins on learner speech | 0 per call | Floor control |
| Huh? per minute, week 1 vs week 4 | Falling | Comprehension evidence (never shown) |
| Calls abandoned on the commute (web) | Watched; high values argue for native | Decision 7 |
