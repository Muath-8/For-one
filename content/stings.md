# For one: sting and sound brief

*Commissioning brief. Draft, 2026-11-12, written on delegation (ADR-24.3). Owner: Muath. The finished assets ship to `packages/languages/en/sound_design/` (PRD FR-1103; architecture/02 `TargetPackage.sound_design`) and are shared across every learner (FR-435). Sources: [design/05 §1.2 and §3](../design/05-interaction-and-audio-ux.md), [design/00](../design/00-design-principles.md) (principle P9, "sound is interface"), PRD FR-1001, architecture/03 §4.5 and §4.11, ADR-24.22.*

---

## 1. What we are making

**For one** is a daily podcast in the language you are learning, made for one listener, followed by a short phone-style call with one of its two hosts. Every learner has their own show. We need the small set of sounds that make it feel like a real show: an ident that opens and closes each episode, short transitions between scenes, the ring that turns the episode into a call, and a few interface sounds inside the call.

The listener is an adult anywhere in the world, often on a commute, often in earbuds, often nervous about speaking. The sounds should make them feel they are in a studio with two friends, never in a game and never in a classroom.

## 2. The rules (non-negotiable)

These come from the product's laws. A sound that breaks one is rejected, however good it is.

1. **No reward sounds, anywhere.** No chime, ding, sparkle, fanfare, applause, coin, level-up sweep, "success" arpeggio or ascending flourish that says "you did it". Nothing plays when the learner keeps a word, finishes an episode, hears their weekly proof or finishes a season (design/05 §1.2).
2. **Sound never changes with how the learner did.** The proof sounds the same on a good week, a flat week and an empty week. The call ends the same way after a great call and after a short one. Nothing gets bigger, brighter or happier as the learner progresses.
3. **No urgency.** No ticking, no countdown, no alarm-like timbres, no rising tension before the learner speaks. The learner's turn is an invitation, like a breath.
4. **No music under speech.** Music never plays under a host or under the learner: listeners at B1 need every syllable. Stings live between speech. The only bed under speech is light room tone.
5. **No single country or religion.** The show has no home country. No instrument, scale or texture that a listener would hear as one nation's or one faith's music (bagpipes, sitar drone, oud improvisation, koto, steel drum, mariachi brass, organ and choir, a call-to-prayer-like melisma, and the like). The library as a whole may range widely in colour; no single ident should say "this show is from X".
6. **No voices in the stings.** No sung words, no vocal chops, no "For one" spoken tag. The hosts' and Salma's voices are separate and come from the voice vendors.
7. **Our own notification sound: none.** See §3.6.
8. **Original and owned.** No samples or loops that need clearance, no imitation of an existing show's theme, and no registration with Content ID or any audio fingerprinting service (it would flag learners' private feeds).

## 3. The inventory

### 3.1 Show idents (the library of 12)

Each learner's show has one ident, chosen at casting from a library of about 12; the learner can change it by telling Salma (design/05 §1.2). Each ident comes in four cuts:

| Cut | Duration | Where it plays | Notes |
|---|---|---|---|
| `open` | 3.0 to 4.0 s | After the cold open (never before it), "like a real show" | Starts at full presence (no long fade-in). |
| `close` | 3.0 to 4.0 s | After the host's sign-off and 1 s of silence | Lands level or settles downward. Never a triumphant final chord. Its last 600 ms must crossfade cleanly into the call chime (§3.3). |
| `seam` | 1.0 to 1.5 s | Between scenes, when the script marks `beat_after: "sting"` | A short cut of the same idea; a breath between scenes, not a mini-ident. |
| `dry` | 2.0 to 3.0 s | Opens and closes the weekly proof and the season finale (Salma's episodes) | The same idea stripped back: no percussion, lower level (about −6 dB against `open`), no brightness. Identical every week whatever the week was. |

A scene seam marked `beat` uses no asset: 700 ms of the room tone bed.

### 3.2 Room tone

| Asset | Duration | Where | Notes |
|---|---|---|---|
| `roomtone_a`, `roomtone_b` | 30 s each, seamless loop | Under the two hosts in episodes ("two voices in a room", design/05 §1.2) | A small, quiet, soft-furnished room. No hum, no traffic, no birds, no weather. Barely audible: it should be missed if removed, never noticed when present. Salma has **no** room tone; she is close and dry. |

### 3.3 The call

| Asset | Duration | Where | Notes |
|---|---|---|---|
| `call_chime` | 600 ms | The episode's throw: the closing ident's tail crossfades into it, and the call card appears (design/05 §1.2, design/03 C1) | "A phone-style chime": friendly, round, two soft pulses at most. Not a ringtone loop, not a real phone brand's ring, not insistent. It plays once; it does not repeat while the card waits. |
| `call_connect` | 100 ms | The moment the call connects (architecture/03 §4.11: proves the audio route works) | A tiny "studio" tick or soft tape-start. Barely there. |
| `turn_tone` | 200 ms | After the host finishes a turn and before the learner's turn (design/05 §1.2, architecture/03 §4.5) | Two soft notes, rising by a whole step or less, low-mid register, felt or sine-like, no shimmer. It is played right after the host's own breath (rendered per voice by the voice vendor, not part of this commission). It must say "your turn, no hurry", never "correct" or "go". Sits about 6 dB under the host's speech. |

### 3.4 Interface sounds

| Asset | Duration | Where | Notes |
|---|---|---|---|
| `error_thud` | 100 ms | System failures only (no connection, a call that cannot connect), never for anything the learner said or did (design/05 §1.2) | A single low, soft thud. Not a buzzer, not a "wrong answer" sound. |
| `mark_click` | 40 to 60 ms | With the "Marked" toast when the learner presses next-track on headphones to mark a moment (design/07 #17, ADR-24.22) | The one confirmation sound in the product: it confirms an action in Ears mode, like a camera shutter on a muted phone. Dry, small, no pitch rise. |

### 3.5 What has no sound (do not make these)

- The retell ring and the then-and-now recording ring: visual only.
- Keeping a word, opening the word sheet, finishing an episode, a door marked done, the weekly proof's headline, the season recap: nothing.
- The learner's own recordings: played back as recorded, with no music under them and no processing that changes how they sound (design/05 §6). The finale plays "then" and "now" in silence between them.
- Backchannels ("mm", "go on"), breaths and thinking fillers: rendered per host voice by the voice vendor (architecture/03 §4.5), not part of this commission.

### 3.6 The drop notification

**No custom sound.** The daily drop notification is a web push (PRD FR-232) and uses the phone's default notification sound; the podcast app's own new-episode alert is the second route. The show does not ship a branded alert, now or in a native app later. A distinctive sound attached to "your episode is here" turns into a cue the learner is trained to respond to, which is exactly the kind of pull the product refuses (TC-2: never manipulate).

## 4. The library of 12 (concepts)

Concepts, not scores: the composer may replace any of them, as long as the set stays varied and inside the rules. Spread keys and tempos so two learners' shows rarely sound alike. Ident 01 is the house ident: the 90-second sample episode uses it, because the visitor has not been cast yet.

| # | Working name | Colour | Feel |
|---|---|---|---|
| 01 | Desk lamp (house ident) | Muted upright piano, two-chord figure, a soft felt thump | Warm, late-evening radio |
| 02 | Commute | Fingerpicked nylon guitar, light shaker | Morning, unhurried |
| 03 | Studio | **No music:** a chair creak, a microphone switch, a page turn, a breath of room | For learners who would rather have no music; also the most "real studio" option |
| 04 | Muted brass | Muted trumpet, one short phrase over upright bass | Dry humour |
| 05 | Kitchen | Wooden mallets (marimba-like), short and playful | Light, a little clumsy, in a good way |
| 06 | Warm synth | Analogue-style pad swell and one short pluck | Modern talk show |
| 07 | Pizzicato | Small string pizzicato figure | Witty, quick |
| 08 | Tape keys | Electric piano chord with gentle tape wobble | Calm, lo-fi |
| 09 | Bass and brushes | Two bars of walking bass, brushed snare | Conversational, easy |
| 10 | Low clarinet | A wry low clarinet line | Curious, slightly sly |
| 11 | Swell | Clean electric guitar, one long reverb swell | Spacious, thoughtful |
| 12 | Cello | Plucked then bowed cello, two notes | Grounded, intimate |

**Mood references, by kind rather than by title** (we do not want an imitation of any existing theme): late-night public-radio interstitials; the short bumpers between segments of two-person conversation podcasts; documentary-radio scene transitions; the quieter end of lo-fi instrumental music.

## 5. Technical specification

| Item | Spec |
|---|---|
| Masters | 48 kHz, 24-bit WAV. Stereo where the idea needs width, but mono-compatible (it will be summed on many phones). `turn_tone`, `call_connect`, `error_thud`, `mark_click` are mono. |
| Loudness | Episodes are normalised to −16 LUFS integrated with hosts at that level (design/05 §1.2). Idents must not jump out: deliver `open`, `close` and `seam` so their short-term loudness peaks at or below −16 LUFS; `dry` about 6 dB lower. True peak at or below −1 dBTP on every file. |
| Heads and tails | No silence at the head (trimmed to the first transient). Tails decay naturally to silence inside the stated duration; no hard cuts. |
| Speed | The player runs at 0.75×, 0.85× and 1.0× with pitch preserved. Every asset must still sound intentional at 0.75× (no smeared transients, no warble). |
| Small speakers | Every asset must read clearly on a phone speaker at 30% volume and in cheap earbuds, without being startling at full volume in good headphones. |
| Narrow band | `call_chime` and `turn_tone` must stay recognisable band-limited to 300 to 3,400 Hz (the dial-in experiment, PRD FR-346, is phone audio). |
| Crossfade | Each ident's `close` tail must crossfade with `call_chime` over 600 ms without a clash in key: deliver `call_chime` in a pitch-neutral form, or one version per key used in the library. |
| Loops | Room tone loops seamlessly at any point; deliver with the loop point at the file boundary. |

## 6. Deliverables

All files under `packages/languages/en/sound_design/`, named exactly:

1. `ident_01_desk-lamp_open.wav`, `_close.wav`, `_seam.wav`, `_dry.wav`, and the same four cuts for idents 02 to 12 (48 files).
2. Stems for each ident (one folder per ident) so a cut can be re-edited later without the composer.
3. `roomtone_a.wav`, `roomtone_b.wav`.
4. `call_chime.wav` (plus per-key variants if the chime is pitched).
5. `call_connect.wav`, `turn_tone.wav`, `error_thud.wav`, `mark_click.wav`.
6. `manifest.yaml`: for every file, its id, cut, duration in ms, integrated and short-term-max loudness, true peak, key (if pitched), and a one-line description for the casting screen (in plain English, translated later with the interface strings).
7. A one-page listening sheet (PDF) with every asset in order, for the acceptance test.

## 7. Acceptance

1. **The reward test.** Five listeners (at least two learners of English and two native speakers, from different regions) hear every asset blind and answer: "Does this sound like you won something, got something right, or are being rewarded?" Any asset that two or more listeners answer "yes" to is redone.
2. **The place test.** Same listeners: "Does this sound like it comes from one country or one religion?" Two or more "yes" answers and it is redone.
3. **The variety test.** Listeners hear pairs of `open` cuts and say whether they are the same show. Any two idents confused by three or more listeners are pushed apart.
4. **Loudness and format.** Every file meets §5, checked with an EBU R128 meter; the manifest matches the files.
5. **In context.** Muath hears three real episodes mixed with three different idents, at 1.0× and 0.75×, on a phone speaker and in earbuds, and one call from ring to goodbye.

## 8. Schedule and rights (proposed)

| Date | Milestone |
|---|---|
| 2026-11-19 | Brief sent; quote and a two-ident sketch requested |
| 2026-12-02 | Idents 01 to 04 in all cuts, room tone, and all call and interface sounds delivered (build week 3) |
| 2026-12-09 | Full library delivered (build week 4); acceptance tests run that week |
| 2026-12-16 | Fixes delivered; files committed to the package |
| 2027-03-17 | Beta opens (ADR-24.11) |

Until delivery, the voice studio mixes episodes with ident 01 as a placeholder (or silence) and the call uses a sine placeholder for `call_chime` and `turn_tone` that meets the same durations.

**Rights.** Work made for hire, or a full assignment of all rights, worldwide, perpetual, all media, including the right to edit, re-cut and combine. No third-party samples that need clearance. If any element is generated or assisted by an AI tool, the composer says which, and confirms the tool's terms grant full commercial rights. No Content ID or fingerprint registration of any kind. The composer may show the work in a portfolio after the beta opens.
