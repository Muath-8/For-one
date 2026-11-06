# For one — 01. Design system

*Part 1 of 8. Tokens live in tokens.css and tokens.json beside this file. The system formalizes the look the v2 prototype arrived at (night studio, Anybody / Readex Pro / Martian Mono, voice orbs, generated cover art) and adds the light theme, accessibility rules and the component inventory.*

## 1. Character

**A night studio with the window open.** The default surface is near-black with a violet cast, so the voice orbs and the episode art are the light in the room. The daylight theme is warm paper, not clinical white. Type does the work illustration would do elsewhere: the display face is condensed and loud on covers and quiet everywhere else. Nothing is a mascot. Nothing is a chip grid.

Three words to check any screen against: **made, warm, finite.** Made: it looks produced for this one person (title, art, a host's line). Warm: colour comes from the voices, never from status. Finite: there is an end to every screen.

## 2. Tokens

See tokens.css (CSS custom properties, dark default, light under `prefers-color-scheme` and `[data-theme]`) and tokens.json (the same values for native builds). Summary:

| Group | Values |
|---|---|
| Surfaces (dark) | page #09080D · bg #110F17 · s1 #1A1722 · s2 #24202E · s3 #2F2A3B · lines at 8% and 14% white |
| Surfaces (light) | page #F2EEE6 · bg #FBF9F4 · s1 #FFFFFF · s2 #F1EDE5 · s3 #E6E1D8 · lines at 8% and 16% ink |
| Text | text / mute / faint (faint is decoration only) |
| Voices | Karim #FF8A4C · Mona #FF5C9A · Salma #C9BCFF · learner #5FE3B0 (light: #D9601F · #D2306E · #6B57C9 · #178A62) |
| Signals | recast #FFC86B (light #8A5A00) inside host captions only · warn #FF5D5D (light #C8303A) for system failure only |
| Type | display Anybody (wdth 50–150) · body Readex Pro · mono Martian Mono; sizes 12 to 64 on a 1.125–1.33 step |
| Space | 4pt grid; phone gutter 20; wide gutter 32; reading measure 34rem |
| Radius | 6 · 10 · 14 · 20 · pill |
| Motion | ease (.2,.8,.2,1); 120 · 200 · 320 · 600ms; all zero under reduced motion |

**Colour rules that are also product rules**
1. `--warn` never appears near a learner's words. It is for "no connection", "payment failed", "mic blocked".
2. `--recast` is the only mark of the teacher inside a conversation: the host's caption sets the echoed form in weight 600 and this colour. No underline, no icon, no tooltip, no tap target.
3. Green is the learner's voice, not a tick. There are no ticks for learning. The only check mark in the product is the "done" state of a door (Listen ✓), which is a fact about time, not quality.
4. Each learner's show may carry its own hue for cover art (derived at casting from the hosts' voices and the first topic, stored as `show.hue`). It tints art and the lock-screen cover; it never replaces the voice colours.

## 3. Type

| Style | Face | Size / leading / weight | Use |
|---|---|---|---|
| Cover title | Anybody, wdth 62–75 | 36–64 / 1.05 / 800 | Episode covers, season titles, the "That's today's show" closing line |
| Screen title | Anybody, wdth 90 | 28 / 1.1 / 700 | Today, Notebook, Show, sheet titles |
| Host name | Anybody, wdth 110 | 14 / 1 / 600, uppercase, tracked 0.08em | Beside orbs and in captions |
| Body | Readex Pro | 16 / 1.55 / 400 | Everything else |
| Reading | Readex Pro | 18–20 / 1.7 / 400 | Article, transcript, chat; user-adjustable 16–24 |
| Caption (call) | Readex Pro | 20 / 1.4 / 400; recast at 600 | Host captions on the call screen |
| Arabic and other RTL body | Readex Pro | same size, leading 1.9 | Salma's lines, glosses, interface in Arabic, Persian, Urdu |
| Label | Martian Mono, wdth 100 | 12 / 1 / 500, uppercase, tracked | Timecodes, dates, "7 MIN · CALL · ARTICLE", plan prices' per-day line |

Rules: one display face per screen, at most two sizes of it. Never justify text. Arabic numerals follow the interface language (Eastern Arabic digits when the learner's interface is Arabic and their locale uses them; test with real learners). Readex Pro is one of the few faces that sets Arabic and Latin with matching x-height and rhythm; do not substitute a different Arabic face without re-testing mixed lines.

## 4. Layout

- **Phone first, 360 to 430 wide.** One column, 20px gutters, content width 100%. Safe areas respected; the bottom tab bar sits above the home indicator.
- **Tablet and laptop (≥ 768).** The same single column centred at 560px max for Today, player and call. Notebook and Show become two columns (list left, detail right). Reading gets the 34rem measure. The web app is a phone app that happens to work on a laptop; it never becomes a dashboard.
- **Three destinations only:** Today · Show · Notebook. The tab bar hides inside the player, the call and the proof.
- **Sheets, not pages, for anything short:** the word sheet, "why this episode", "2 other ideas", controls, consent. Sheets open from the bottom at 200ms, dismiss by drag or tap outside.
- **No modals that block audio.** A sheet never pauses playback.

## 5. Motion

| Moment | Motion |
|---|---|
| Screen change | Crossfade plus 12px vertical settle, 320ms |
| Voice orb | A breathing blob driven by the speaker's audio level: amplitude maps to radius (±8%), 600ms half-cycle idle breath when silent. Static at mid-amplitude under reduced motion. |
| Captions | Words appear as spoken (word timings from the voice studio); never typewriter per character |
| Cover reveal | Generated contour art fades in over 600ms behind the title on first open of the day |
| Hold pad | Scale 0.98 and fill with the learner colour at 20% while held; releases over 120ms |
| Huh? | The transcript line slides down 8px, slows, and glosses unfold beneath it over 200ms |
| Anything about progress | None. The tape tiles do not animate; counts do not tick up; nothing celebrates. |

Sound motion is in 05-interaction-and-audio-ux.md. There are no reward animations and no confetti, by law 1.

## 6. Voice identity (orbs and marks)

- **Hosts:** a 120px breathing orb in the host's colour with a soft radial glow; the name in the display face beneath. Two hosts side by side on casting and the cover. In a caption row, a 40px orb.
- **Salma:** a 40px lilac orb with a thin ring, never larger; her name only in body text. She appears in the corner of the notebook, on the proof cover and in onboarding. Her voice is closer and drier (05 §6), so her orb is the only one without a glow.
- **The learner:** the green orb only on the hold pad and on the tape. Never a photo, never an avatar.
- **Nobody has a face.** Realistic AI faces fall into the uncanny valley and the show's loyalty is built on voices.

## 7. Cover art

Every episode gets generated contour art: a seeded field of concentric lines in the show's hue, warped by the episode's two host colours (prototype method, canvas, seeded by episode id so it is stable). The title sits on it in the cover style. Covers must work at 48px (shelf), 160px (Today hero), 600px (lock screen) and in both themes. No photographs, no AI illustration, no stock icons.

## 8. Components

Each component names its states and the product rule it carries. Full per-screen states are in 04-screen-specs.md.

| Component | Anatomy | States | Rule it carries |
|---|---|---|---|
| **Hero cover** | Art, title, host orbs, label line (length · doors), one Play button | ready · in progress (doors row replaces label) · done (closing line, tomorrow's time) · proof day (proof cover above) · loading (title and art, button disabled, "making…" from Salma) · offline (art cached, "ready when you're back online") | P1, P7 |
| **Door row** | Four doors: Listen · Call · Read · Chat, each with a ✓ when done | any order; a done door stays tappable (replay); Call shows the host orb | Session state machine: doors in any order, Read before Call suggested |
| **Primary button** | Pill, learner colour, on-accent text, 52px | default · pressed (s3 overlay) · disabled (40%) · loading (label stays, dot breathes) | Only one per screen |
| **Secondary / quiet button** | Pill outline on line-2 / text only | same | Alternatives are visually quieter than the one thing (P1) |
| **Transcript** | Karaoke lines; current line full `--text`, others `--mute`; every word a tap target | playing · paused · hidden (audio-first) · Huh? expanded | Audio-first; tap any word |
| **Huh? button** | 64px pill, display face, centred under the scrubber | idle · held (replays slower, glosses unfold) | The most important button in the player; an honest "I didn't get that" |
| **Word sheet** | Word, gloss in own language, sentence it came from, 🔊, Keep | default · kept (button becomes "Kept", no animation) | Keep sends to the notebook and to the planner |
| **Hold pad** | Full-width 112px pad, learner-green ring, "hold to keep the floor" | idle · held (fills 20%, host waits) · host speaking (pad dims to 60%) · reconnecting | P8 |
| **Word button** | 56px round button beside the pad, labelled "word" | idle · held (listens in own language) · gave (the word appears once in the host caption) | The host gives the word; Salma is silent |
| **Caption row** | 40px orb, host name label, caption text with recast weight | live · ended | No learner captions live (P4) |
| **Retell ring** | 60-second soft ring around the pad | counting · done; never red, never cuts off | |
| **Voice orb** | §6 | silent · speaking · thinking (slow breath) · muted | Sound is interface |
| **Fact card** (notebook, onboarding) | "You said on Oct 3: '…'" quote, the fact, ✎, ✕ | confirmed · "I think…" (unconfirmed, dashed line, never used in the show) · deleted (gone, no undo prompt) | Told, not inferred; a wrong memory is a bug |
| **Three ideas** | Three short cards from the hosts, one tap picks; "or tell Salma" | unpicked (planner's hero waits) · picked | Tomorrow chosen tonight |
| **Plan cards** | Three, middle marked Recommended, price, "about $1 a day", per-episode, what every plan includes | trial active · chosen · founding (price locked) | Honest pricing psychology; no countdowns |
| **Consent row** | Unticked box, one plain sentence, "only for you, delete any time" | off (default) · on | Opt-in only |
| **Controls sheet** | Short list of reliable settings | | Everything else is a sentence to Salma |
| **Tape tiles** | Cassette-like tiles per season, length of answer, Play A then B | | Then-and-now, the learner's own ears |
| **Proof clip pair** | Two clips (then / now), one headline sentence from Salma, "how we know" | good week · flat week ("Flat week. Here's what I'm changing.") · slow week (shorter, about what has built up) | No claim without proof |
| **Small door** | A quieter card under the hero: "90-second recap and one voice note. Counts fully." | | Never leave a debt |
| **System toast** | Top, s2, one line, 3s | offline · back online · saved | Only for system facts; never for learning |

**Not in the system, on purpose:** progress bars for learning, streak counters, badges, confetti, level labels, percentage rings, red error states on text, modals that interrupt audio, infinite lists.

## 9. Themes

Dark is the default because the product is used at 7:40 on a bus and at night in bed, and because the prototype's night studio is the look Muath has seen. Light exists for daylight reading and for learners who need it. Rules: both themes use the same tokens by name; the voice colours shift to darker, more saturated versions in light so contrast holds (see tokens.json `contrast`); cover art re-renders per theme (ink on paper in light); the lock-screen cover is always the dark version. The learner chooses system / dark / light in Controls.

## 10. Accessibility

- **Contrast:** text and mute ≥ 4.5:1 on every surface in both themes; voice colours ≥ 4.5:1 when used as text in light (they are); `faint` is never used for text.
- **Targets:** 44pt minimum; the hold pad and Huh? are deliberately huge; headphone buttons do the same jobs without the screen.
- **Captions everywhere audio plays**, host side; transcript-first mode for hard-of-hearing learners (transcript always visible, call captions larger).
- **Screen readers:** the transcript announces lines, not words; orbs are `aria-hidden` with the speaker's name in text; the hold pad is a button with a described long-press; live regions for the host's caption only.
- **Motor and processing:** hold to keep the floor also serves learners who stutter or need time; nothing times out while the learner holds; the retell ring never cuts off.
- **Text:** reading size 16–24 and line spacing adjustable in Controls; no text in images (covers use live type).
- **Reduced motion:** honoured via tokens; orbs go static.
- **Bidirectional text:** every block sets `dir` from its content; mixed bubbles in chat use `unicode-bidi: plaintext`; the layout mirrors for RTL interface languages (tab order, back arrows, scrubber direction stays left-to-right as time does in both scripts, per platform convention; test with Arabic learners).
- **Cognitive load:** one primary action per screen, no settings beyond the controls sheet, everything else by talking to Salma.

## 11. Platform notes

- **Web (PWA):** the tokens are CSS variables; fonts self-hosted; Media Session API for lock-screen metadata and the two custom actions (replay sentence, mark moment); web push on installed PWAs only; the call runs foreground.
- **Native (if chosen):** tokens.json feeds the theme; the audio session is category playback for episodes and playAndRecord for calls; Now Playing carries the cover; CarPlay / Android Auto get the standard Now Playing only, so the call is never offered in the car UI.
- Both share the same screens and components; 02 §6 lists the exact differences.
