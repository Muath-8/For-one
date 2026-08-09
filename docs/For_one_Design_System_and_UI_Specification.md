---
title: "For one — Complete Design System and UI Specification"
subtitle: "A private recurring show, authored for one person"
author: "Product design specification"
date: "8 August 2026"
lang: en-US
---

# Executive design direction

## Design thesis

For one should feel like opening **today's edition of a private recurring programme**: a finite, authored set of possibilities has arrived; one of them is already produced; familiar hosts are waiting inside; and the user is expected to take part, not administer the system.

The interface is therefore organised around a **daily programme sheet**, not a dashboard, feed, catalogue, prompt box, or curriculum. The programme sheet has one lead item that is ready now and two to four supporting pitches. Selecting an item opens a continuous episode folio that moves through four familiar media forms:

**Episode → Notes → Call-in → After-show**

Those are the user-facing labels. Internally they map to Listen → Read → Speak → Chat, but the skill model never appears in the interface.

## For one in one visual sentence

> A warm independent publication that turns into a quiet radio booth when the show goes on air—typographic, intimate, precise, and unmistakably made for one person.

## The central interface idea: the daily programme sheet

Every important design decision should preserve one idea: **the user is not searching for something to do; their show has arrived carrying something made for them.**

The main screen is a dated programme, not a content grid. The episode is a produced object, not generated output. The article is a piece of editorial material, not reading comprehension. The call-in is the climax of the show, not voice mode. The chat is an after-show thread with a visible ending, not an open companion.

## Five defining design decisions

1. **One lead pitch is distinguished by readiness, not recommendation.** It is larger and marked “Ready now” because it is factually pre-produced. The interface never says “best for you,” explains the prediction, or exposes personalisation logic.
2. **The product has two environmental surfaces.** “Paper” supports arrival, reading, archive, and trust. “Booth” supports produced audio and live voice. This creates media presence without a user-facing theme setting.
3. **Typography is the artwork.** Episode identity comes from deterministic title plates, host marks, date, cast, and format—not stock photography, generated portraits, or decorative AI imagery.
4. **The cycle has no educational stepper.** Each medium naturally hands the user to the next: the episode throws to the notes; the notes arm the call; the call creates the after-show message.
5. **The interface ends.** After the final host reply, the composer closes and the page says only “That’s the show.” No next-session push, celebration, score, or obligation appears.

## Product boundaries that the design must preserve

- No levels, streaks, scores, progress dashboards, courses, tests, goals, badges, homework, or lesson terminology.
- No large prompt box on arrival.
- No generic streaming grid, social feed, or card wall.
- No portraits that imply hosts are real people.
- No persistent chatbot or endless message composer.
- No explanation of targets, difficulty, CEFR, assessment, salience, energy, or planner logic.
- No notification centre, re-engagement surface, or “come back” pressure.
- No conventional settings dashboard.

## Source authority and one explicit v1 trust gap

The Implementation PRD governs behaviour, limits, state, latency, failure handling, and v1 scope. The Product Concept governs emotional ambition, product laws, and the trust standard. Design judgement is used only where those sources leave visual or interaction decisions open.

There is one material source tension that must not be hidden. The Product Concept promises that users can see, export, and delete their data. The Implementation PRD supports a knowledge summary, conversational correction, and revocation of call-in audio storage, but explicitly removes general export/deletion and excludes settings screens in v1. This specification follows the PRD: it designs the supported controls and does **not** invent export, account deletion, or a data dashboard. The product must not repeat the broader promise in v1 marketing until the behaviour exists.

# Experience model

## What the user believes they are entering

The primary mental model is **opening today’s programme from a private recurring show**.

This is stronger than “entering a studio” because the user should not feel responsible for production. It is stronger than “receiving an episode” because the user first chooses among authored pitches. It is stronger than “opening a publication” alone because audio, recurring hosts, and the live call are central.

The programme model communicates five things immediately:

- the show has a cadence without imposing a streak;
- the material is finite and prepared, not an infinite feed;
- the hosts recur and accumulate history;
- the user chooses what goes on air;
- every edition ends cleanly.

## Experience hierarchy

| Priority | What dominates | Design consequence |
|---|---|---|
| 1 | Today’s programme | The first viewport is dated, finite, and centred on pitches. |
| 2 | The lead prepared pitch | It receives the strongest typography and the only “Ready now” state. |
| 3 | The selected episode | Once chosen, all navigation recedes and the episode becomes the environment. |
| 4 | The user’s role | The unresolved throw, call-in invitation, and host pushback make participation the climax. |
| 5 | Recurring hosts | Names, voices, marks, and relationship history remain visible but never overpower the episode. |
| 6 | Previous episodes | Archive is one persistent destination, deliberately quieter than Today. |
| 7 | Cast and trust controls | Accessible from “Your show,” but not promoted as primary work. |

## What remains nearly invisible

| Hidden system | User-facing substitute |
|---|---|
| Pedagogical targets | Natural repetition across episode, notes, call, and after-show |
| Internal proficiency and difficulty | Language that simply feels demanding but followable |
| Assessment | Weekly Proof as an authored media event |
| Prediction ranking | One item marked “Ready now” |
| Planner and quality gate | A complete programme that arrives without technical explanation |
| Generation pipeline | “Making the opening” and honest readiness states |
| Learner-file structure | “What the show remembers” in plain language on request |
| Telemetry and cost | No user-facing surface |
| AI configuration | Transparent identity, no model/provider terminology |

## Emotional arc translated into interface behaviour

| Moment | Intended feeling | Interface behaviour |
|---|---|---|
| Arrival | Something is here | The dated programme renders immediately; no blank prompt or setup request. |
| Recognition | This is mine | One pitch may contain a restrained, high-confidence callback inside its title; familiar host names are visible. |
| Anticipation | I want to hear this | The lead title and “Ready now” control dominate; supporting pitches remain legible but quieter. |
| Selection | I am choosing the show | The production sheet lets the user accept or change topic, format, and cast without prompt engineering. |
| Immersion | The software disappears | Navigation contracts; the booth surface, player, and transcript become the page. |
| Participation | They need my position | The episode ends unresolved; the notes and call-in use direct, social language. |
| Resolution | The argument has landed | The host closes the call and the short after-show thread ends visibly. |
| Return to life | Nothing is hanging over me | “That’s the show” offers a quiet exit; no next action is promoted. |

## The continuous episode folio

A selected session is one object with four media surfaces, not four tasks in a workflow. The browser URL may change by stage for restoration, but the visual identity, episode title, cast, and position remain continuous.

- **Episode:** produced audio, transport, synced transcript.
- **Notes:** editorial article that complicates the hosts’ position.
- **Call-in:** live or asynchronous voice argument.
- **After-show:** short text exchange with a hard social ending.

The user may pause from any surface. Episode audio and notes remain replayable after completion. The live call cannot resume mid-conversation; returning opens a fresh line that acknowledges the gap once.

# Design principles

| Principle | What it means | Interface requirement | Violation | For one example |
|---|---|---|---|---|
| **Arrive authored** | The product brings a made object rather than waiting for a prompt. | Render a complete dated programme; distinguish readiness; use specific titles. | Empty home state dominated by “What do you want to talk about?” | “Karim watched the derby and has one terrible idea about Saturday’s lineup.” |
| **Programme, not platform** | The daily set is finite, paced, and editorially arranged. | One lead item, a short supporting list, no endless scroll or recommendation rails. | A Netflix-style grid of episode covers. | Three pitches in week one, with one lead and two supporting lines. |
| **Participation is the climax** | Listening and reading exist to create a position the user wants to defend. | Make the unresolved throw and call-in the dramatic peak; show a real host stance. | Treating the call as an optional practice tool under the player. | “The article’s in your notes. Read it, then get on the line.” |
| **Personal, never forensic** | Memory should feel like continuity, not surveillance. | Use at most two high-confidence references; never show “why this was recommended.” | Tags such as “Based on your location and recent activity.” | A pitch naturally mentions the interview the user volunteered. |
| **Warmth with the labels on** | The show may be intimate while remaining explicit that hosts are AI. | Use crafted voices and recurring marks; disclose AI plainly; avoid human portraits and fake lives. | “Mara missed you” or a photorealistic host portrait. | “Mara and Sami are your AI hosts. They remember only what the show has stored.” |
| **Complexity stays backstage** | The product makes hard decisions without asking the user to manage learning. | Hide targets, bands, assessment, model status, and generation stages. | Difficulty sliders, goals, or grammar target chips. | Topic, format, and cast are editable; difficulty is not. |
| **Finish without pressure** | Every session closes as a complete piece of media. | End chat, remove the composer, offer a quiet exit. | Confetti, “keep the streak,” or auto-opening the next pitch. | “That’s the show.” |
| **Trust is an interaction, not a policy link** | Users can inspect and correct memory and control optional audio. | Put “What the show knows” and “Voice tape” in an accessible show sheet with direct actions. | Burying consent inside legal text or a generic settings maze. | “That changed” opens a direct correction flow. |

# Information architecture

## Sitemap

```text
For one
├── Today
│   ├── Resume active session (conditional)
│   ├── Weekly Proof (conditional)
│   ├── Daily programme: 3–5 pitches
│   ├── Pitch production sheet
│   └── Bring your own idea
├── Session folio
│   ├── Episode
│   ├── Notes
│   ├── Call-in
│   └── After-show
├── Archive
│   ├── Episode record
│   └── Weekly Proof record
└── Your show (sheet, not a settings dashboard)
    ├── Cast
    │   ├── Default duo
    │   ├── Created hosts
    │   ├── Create through conversation
    │   └── Retired hosts
    ├── What the show knows
    ├── Voice tape
    ├── About the AI show
    └── Account essentials
```

## Persistent navigation

### Desktop

A restrained masthead persists on Paper surfaces:

- **For one** wordmark: returns to Today.
- **Today**: primary destination.
- **Archive**: chronological record.
- **Your show**: opens a right-side sheet containing cast, memory, voice consent, disclosure, verification, and sign-out.

The masthead is not persistent inside an active Call-in. In Episode and Notes it collapses to a contextual header with Back, episode title, and an overflow menu.

### Mobile

There is no bottom navigation bar. The product has only two primary destinations, so a compact top masthead is clearer and less app-like:

- wordmark/back control on the left;
- Archive icon with visible label in its accessible name;
- Your show button on the right.

The bar hides on downward reading scroll and returns on reverse scroll. It never hides while playback is paused, permission is needed, or an error is present.

## User-facing labels

| Internal concept | Interface label |
|---|---|
| Home | Today |
| Listen stage | Episode |
| Read stage | Notes |
| Speak stage | Call-in |
| Chat stage | After-show |
| History | Archive |
| Settings/profile | Your show |
| Learner-file summary | What the show knows |
| Voice-storage consent | Voice tape |
| Character management | Cast |
| Custom creation | Bring your own idea |

## What does not receive a destination

- Pedagogy, language profile, targets, and assessment.
- Generation status history.
- Notifications.
- Usage analytics or progress.
- A separate search destination.
- A separate “learning” or “practice” area.
- General settings.

## Active and unfinished sessions

An active session appears above everything else on Today as a single resume band:

> **Continue “The case against five-day trips”**  
> You left midway through the notes. · Continue

Stage is described in natural language; no percentage or four-step progress indicator appears. During Episode, factual time position may be shown. During Notes, the copy says “midway” only if the stored scroll position is beyond 35%; otherwise it says “near the beginning.” During Call-in, it says “The line will reopen with a fresh start.”

Starting another session opens one confirmation. Continuing is the primary action. Abandoning the current session is explicit and destructive. After 48 hours, the session moves to Archive as “Ended early”; it no longer blocks a new session.

## Weekly Proof placement

When available, Weekly Proof appears below the active-session band and above the daily programme. It is visually a **special broadcast**, not a metric panel. It has its own proof surface, a two-minute player, and one title. It does not show charts, counts, or a progress summary before playback.

## First viewport blueprint

### Desktop, no active session

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ For one                         Today   Archive                 Your show   │
├────────────────────────────────────────────────────────────────────────────┤
│ SATURDAY, 8 AUGUST                                                      01 │
│                                                                            │
│ [Lead programme item — 7 columns]     [Supporting programme — 5 columns]   │
│ Large title                           02 Supporting pitch title             │
│ Cast · format · Ready now             Cast · format                         │
│ Play this episode                     ─────────────────────────────          │
│                                       03 Supporting pitch title             │
│                                       Cast · format                         │
│                                                                            │
│ Bring your own idea                                                        │
└────────────────────────────────────────────────────────────────────────────┘
```

### Mobile

```text
For one                                      Archive   Your show
SATURDAY, 8 AUGUST

01  READY NOW
Large lead pitch title wrapping naturally over several lines
Cast · format
[Play this episode]

────────────────────────────────
02  Supporting pitch title
Cast · format
────────────────────────────────
03  Supporting pitch title
Cast · format

Bring your own idea
```

# Visual direction

## Art-direction statement

For one combines the restraint of an independent cultural publication with the functional clarity of a radio control room. Paper surfaces are warm, matte, and typographic. Audio surfaces become charcoal and acoustically quiet. The visual energy comes from titles, spacing, live state, and voice—not gradients, illustration noise, or interface ornament.

The recognisable For one signature is the combination of:

- a dated daily programme;
- typographic episode plates;
- non-human host marks;
- the Paper-to-Booth environmental shift;
- a single warm broadcast signal colour;
- editorial rules and asymmetry instead of card grids.

## Reference qualities and clichés to avoid

| Tradition | Borrow | Avoid |
|---|---|---|
| Independent editorial design | Strong hierarchy, generous but purposeful margins, confident type scale | Fashion-magazine illegibility and tiny grey type |
| Printed radio programmes | Finite schedule, numbering, dates, cast credits | Nostalgic imitation, paper textures, faux stamps |
| Liner notes | Credits, intimate details, typography as identity | Collectible-object clutter |
| Broadcast graphics | Clear live/ready states and disciplined information density | Breaking-news urgency and red overload |
| Film titles | Dramatic title composition and pacing | Cinematic spectacle that delays action |
| Studio equipment | Quiet functional controls and truthful status | Skeuomorphic knobs, meters, fake waveforms |

## Composition system

### Grid and width

| Breakpoint | Grid | Outer margin | Gap | Content maximum |
|---|---:|---:|---:|---:|
| Mobile, 320–599 | 4 columns | 20 px (16 px below 360) | 16 px | viewport |
| Tablet, 600–1023 | 8 columns | 32 px | 20 px | 920 px |
| Desktop, 1024–1439 | 12 columns | 48 px | 24 px | 1248 px |
| Wide, 1440+ | 12 columns | 64 px | 24 px | 1320 px |

- The programme uses a 7/5 split on desktop and a single column on mobile.
- The Episode player and transcript use a centred 8-column region, maximum 840 px.
- Long-form Notes use a 640–720 px text measure, never a full-width column.
- Supporting rails are permitted only for contextual metadata, never for ads, recommendations, or metrics.
- Full-bleed treatment is reserved for Booth surfaces and mobile call-in. Paper content remains within the grid.

### Spacing rhythm

The base unit is 4 px. The production scale is 4, 8, 12, 16, 24, 32, 48, 64, 96, and 128 px. Components may use 20 or 40 only when required by optical alignment; arbitrary spacing values are prohibited.

### Density

- Today: medium density; the first viewport should contain the whole lead item and at least two supporting titles on a standard laptop.
- Episode: low visual density around transport, higher density in transcript.
- Notes: editorial density, 19 px text with 31 px line height.
- Archive: high but calm density; chronological rows, not cards.
- Trust and Cast: compact, explicit, and text-led.

### Asymmetry

Asymmetry is used to signal editorial authorship, not randomness. The lead pitch may span seven columns while supporting pitches stack in five. Episode plates may offset cast credits. Controls, form fields, and legal consent remain aligned and predictable.

## Shape language

| Element | Rule |
|---|---|
| Ordinary content | No enclosing card. Use whitespace and horizontal rules. |
| Interactive list rows | Flat surface with 1 px divider; hover may tint the row. |
| Primary buttons | 8 px radius; never pill-shaped unless the control is a compact toggle. |
| Inputs | 6 px radius, visible border, no floating label. |
| Sheets and dialogs | 16 px radius on desktop; top corners 16 px on mobile bottom sheets. |
| Definition popover | 8 px radius, 1 px border, restrained shadow. |
| Compact player | 12 px radius because it floats above content. |
| Host marks | 4 px radius or circular only when the mark’s geometry requires it. |
| Episode plate | Usually no border and no container; composition itself defines the object. |

Shadows are used only for overlays, popovers, and the compact player. Active media differs through environment, scale, and state—not elevation.

## Image and illustration policy

V1 uses **no photography, no photorealistic host portraits, and no free-form generated episode imagery**.

Episode identity is produced by a deterministic title-plate system using:

- title;
- date/issue number;
- format;
- one or two host marks;
- one accent rule or field;
- optional typographic crop or repeated title fragment.

This system scales to every language, avoids inconsistent AI artwork, and makes the show feel produced rather than decorated.

Hosts have visual identities without faces. Each host receives a stable mark made from a monogram or abstract letterform, one accent colour, and a typographic nameplate. The mark never suggests a body, age, ethnicity, or photographic reality. Voice samples and writing establish character; the interface does not fabricate a human appearance.

Illustration is reserved for rare functional diagrams in help or permission education; none is required in the core v1 experience.

## Iconography

- Use a curated 1.75 px outline family with square optical construction and restrained rounded joins.
- Standard optical sizes: 16, 20, and 24 px; live-call primary control may use 28 px.
- Filled icons are reserved for active Play, Pause, Mute, and selected microphone states.
- Navigation icons require text labels on desktop and accessible names on mobile. Archive and Your show must not be represented by ambiguous decorative symbols alone.
- The 10-second-back icon remains counter-clockwise in both LTR and RTL.
- Do not use sparkles, magic wands, brains, robots, orbit icons, or decorative microphone patterns.

# Foundations and design tokens

## Environment strategy

V1 launches with a **context-driven editorial theme**, not a light/dark mode selector.

- **Paper environment:** Today, onboarding, Notes, After-show, Archive, Cast, and Trust.
- **Booth environment:** Episode playback and Call-in.
- **Proof environment:** Weekly Proof, using a quiet blue-grey field within Paper.

The user does not configure these environments. They are part of the show’s media grammar. The Paper base is warm enough for evening use without becoming low-contrast. Browser and operating-system high-contrast modes must remain supported.

## Colour primitives

| Token | Value | Role |
|---|---|---|
| `paper-0` | `#FCFAF4` | Raised paper surface |
| `paper-50` | `#F7F3EA` | Primary Paper canvas |
| `paper-100` | `#EDE6DA` | Subtle inset/hover |
| `paper-200` | `#E1D7C7` | Selected field |
| `paper-300` | `#D4C8B8` | Borders/dividers |
| `ink-950` | `#171716` | Primary text |
| `ink-800` | `#353431` | Strong secondary text |
| `ink-650` | `#4B4945` | Secondary text |
| `ink-550` | `#66625C` | Muted text; minimum for normal text on Paper |
| `broadcast-700` | `#A5432F` | Brand signal and primary accent on Paper |
| `broadcast-400` | `#E06A4D` | Primary accent on Booth |
| `petrol-700` | `#245C63` | Link/action on Paper |
| `petrol-800` | `#1C484E` | Action hover |
| `proof-700` | `#355C72` | Proof foreground/accent |
| `proof-100` | `#DDE8EC` | Proof surface |
| `booth-950` | `#121415` | Booth canvas |
| `booth-900` | `#1B1D1E` | Booth raised surface |
| `booth-800` | `#292B2C` | Booth hover/inset |
| `booth-650` | `#3B3D3E` | Booth border |
| `booth-text` | `#F7F2E8` | Booth primary text |
| `booth-muted` | `#CAC3B9` | Booth secondary text |
| `focus-600` | `#2356C4` | Focus on Paper |
| `focus-300` | `#86A8FF` | Focus on Booth |
| `success-700` | `#2F6B4F` | Confirmed/saved state |
| `warning-800` | `#7A510F` | Warning text |
| `error-700` | `#A33232` | Error and destructive action |

Primary text contrast on Paper is greater than 16:1; muted text remains above 5.4:1. Broadcast, Petrol, Proof, Success, Warning, and Error foregrounds all exceed 5.5:1 on Paper. Booth text exceeds 16:1 and the Booth broadcast accent exceeds 5.5:1.

## Semantic colour tokens

| Semantic token | Paper | Booth |
|---|---|---|
| `color.bg.canvas` | `paper-50` | `booth-950` |
| `color.bg.surface` | `paper-0` | `booth-900` |
| `color.bg.subtle` | `paper-100` | `booth-800` |
| `color.text.primary` | `ink-950` | `booth-text` |
| `color.text.secondary` | `ink-650` | `booth-muted` |
| `color.text.muted` | `ink-550` | `#A9A39A` |
| `color.border.default` | `paper-300` | `booth-650` |
| `color.action.primary` | `petrol-700` | `broadcast-400` |
| `color.action.hover` | `petrol-800` | `#F07A5B` |
| `color.signal.live` | `broadcast-700` | `broadcast-400` |
| `color.focus` | `focus-600` | `focus-300` |
| `color.selection` | `paper-200` | `#40302B` |
| `color.overlay` | `rgba(23,23,22,.55)` | `rgba(0,0,0,.70)` |
| `color.disabled.text` | `#8B867E` | `#777A7A` |
| `color.disabled.bg` | `#E8E1D6` | `#252728` |

Brand colour is not a background default. It identifies live, ready, or decisive moments and should occupy less than 10% of an ordinary Paper screen.

## Host accents

A host receives one stable accent from a controlled palette. Accents may colour a 3 px rule, host mark, speaker label, or selected cast chip. They are not used for long text unless the pairing passes contrast.

| Accent | Value |
|---|---|
| Ochre | `#8D5D16` |
| Teal | `#2F6662` |
| Plum | `#744C63` |
| Slate blue | `#3F5F7A` |
| Rust | `#914735` |
| Olive | `#5E6531` |

## Typography

### Typeface strategy

- **Latin display and editorial:** Source Serif 4.
- **Latin interface, transcript, controls:** Inter.
- **Arabic editorial:** Noto Naskh Arabic.
- **Arabic interface and transcript:** Noto Sans Arabic.
- **Other scripts:** vetted Noto Serif/Sans pair when quality permits; otherwise use Noto Sans for both roles rather than forcing a weak serif.
- **Monospace:** Noto Sans Mono for timecodes, token examples, and technical documentation only.

All recommended families are open-source and practical to ship. The application must load only the scripts required by the selected native and target languages.

### Type scale

| Role | Desktop | Mobile | Weight | Notes |
|---|---|---|---|---|
| Programme display | 56/58 px | 40/43 px | 500 serif | Lead pitch; max 5 lines mobile |
| Episode display | 48/51 px | 36/40 px | 500 serif | No truncation on episode page |
| Page title | 36/40 px | 30/35 px | 500 serif | Archive, Cast, Trust |
| Section title | 28/34 px | 24/30 px | 500 serif | Editorial sections |
| Component title | 20/26 px | 19/25 px | 600 sans | Supporting pitch, dialog title |
| Reading body | 19/31 px | 18/29 px | 400 serif | 55–72 characters per line |
| Transcript | 18/30 px | 17/28 px | 400 sans | Speaker labels 13/18 |
| UI body | 16/24 px | 16/24 px | 400 sans | Default controls and copy |
| UI small | 14/20 px | 14/20 px | 500 sans | Metadata, labels |
| Caption | 12/16 px | 12/16 px | 600 sans | Dates, time, status |
| Timecode | 13/18 px | 13/18 px | 500 mono/tabular | Never below 12 px |

### Typography rules

- Large Latin titles may use `letter-spacing: -0.02em`; Arabic and other connected scripts use zero tracking.
- Interface text uses sentence case. All caps is limited to short Latin date/status kickers; localisations may use weight instead of case.
- Reading measure: 62–68 characters by default, hard range 55–72.
- Paragraph spacing equals 0.75 line height; no first-line indent in UI articles.
- Italics may mark publication titles or quoted emphasis in Latin; never synthesize italics for scripts without a native italic.
- Use tabular numerals for playback time and issue numbers.
- Do not truncate episode titles on detail surfaces. Supporting pitches may clamp at three lines desktop and four lines mobile, with the full title exposed to assistive technology.
- Mixed-direction names and titles must be wrapped in component-level `dir="auto"` spans.

## Spacing, sizing, and shape tokens

| Category | Tokens |
|---|---|
| Spacing | `space-1:4`, `2:8`, `3:12`, `4:16`, `6:24`, `8:32`, `12:48`, `16:64`, `24:96`, `32:128` px |
| Radius | `radius-0:0`, `radius-1:4`, `radius-2:6`, `radius-3:8`, `radius-4:12`, `radius-5:16`, `radius-round:999` px |
| Border | `border-hairline:1px`, `border-strong:2px`, `border-live:3px` |
| Control height | `control-sm:36`, `control-md:44`, `control-lg:52`, `control-call:64` px |
| Touch target | 44 px minimum; 48 px preferred on mobile |
| Icon | 16, 20, 24, 28 px |
| Audio scrubber | 4 px track, 20 px thumb; 44 px interaction hit area |
| Transcript measure | 760 px max |
| Article measure | 680 px default, 720 px max |
| Programme width | 1320 px max |

## Shadows and layers

| Token | Value | Use |
|---|---|---|
| `shadow-popover` | `0 8px 28px rgba(23,23,22,.16)` | Definition popover |
| `shadow-sheet` | `0 16px 48px rgba(23,23,22,.22)` | Desktop show sheet/dialog |
| `shadow-player` | `0 6px 24px rgba(23,23,22,.18)` | Compact persistent player |
| `z-base` | 0 | Page |
| `z-sticky` | 20 | Masthead/compact player |
| `z-popover` | 40 | Definitions/selectors |
| `z-sheet` | 60 | Your show, production sheet |
| `z-dialog` | 80 | Confirmation/permission |
| `z-toast` | 100 | Rare transient system notice |

Toasts never carry critical actions or consent. Critical states remain in the page.

## Motion tokens

| Token | Duration | Easing | Use |
|---|---:|---|---|
| `motion-instant` | 80 ms | linear | State colour/word highlight |
| `motion-fast` | 140 ms | cubic-bezier(.2,.0,.2,1) | Hover, focus, compact controls |
| `motion-standard` | 220 ms | cubic-bezier(.2,.0,0,1) | Sheets, pitch selection |
| `motion-emphasis` | 320 ms | cubic-bezier(.16,1,.3,1) | Player expansion, environment change |
| `motion-stage` | 420 ms max | cubic-bezier(.16,1,.3,1) | Paper ↔ Booth transition |

Spring motion is allowed only for bottom-sheet settling and compact-player expansion, with no bounce. Reduced-motion mode removes translation and uses an 80 ms crossfade or immediate state change.

## Breakpoint tokens

```css
--bp-mobile: 0px;
--bp-tablet: 600px;
--bp-desktop: 1024px;
--bp-wide: 1440px;
--content-programme: 1320px;
--content-media: 840px;
--content-reading: 680px;
```

## Example token hierarchy

```css
:root {
  /* primitives */
  --paper-0: #fcfaf4;
  --paper-50: #f7f3ea;
  --paper-100: #ede6da;
  --paper-300: #d4c8b8;
  --ink-950: #171716;
  --ink-650: #4b4945;
  --broadcast-700: #a5432f;
  --petrol-700: #245c63;

  /* semantic */
  --color-bg-canvas: var(--paper-50);
  --color-bg-surface: var(--paper-0);
  --color-text-primary: var(--ink-950);
  --color-text-secondary: var(--ink-650);
  --color-border-default: var(--paper-300);
  --color-action-primary: var(--petrol-700);
  --color-signal-live: var(--broadcast-700);

  /* component */
  --pitch-lead-title-size: clamp(2.5rem, 4vw, 3.5rem);
  --player-control-size: 3.25rem;
  --definition-max-width: 22rem;
  --compact-player-height: 4.5rem;
}

[data-environment="booth"] {
  --color-bg-canvas: #121415;
  --color-bg-surface: #1b1d1e;
  --color-text-primary: #f7f2e8;
  --color-text-secondary: #cac3b9;
  --color-border-default: #3b3d3e;
  --color-action-primary: #e06a4d;
  --color-signal-live: #e06a4d;
  --color-focus: #86a8ff;
}
```

# Component system

## Component rules

1. A component must correspond to a real recurring behaviour, not merely a visual treatment.
2. Flat composition is the default. Add a container only when it groups controls, floats above content, changes environment, or represents a discrete state.
3. Every component must support text expansion, `dir="auto"`, keyboard focus, and 200% text zoom.
4. Status is communicated by text plus colour or icon; colour alone is never sufficient.
5. Host accent is identity, not hierarchy. The current action remains dominant regardless of host colour.
6. Components may not expose internal AI, pedagogy, or pipeline terminology.

## Navigation components

| Component | Purpose and anatomy | Variants and states | Responsive and accessibility | Misuse rules |
|---|---|---|---|---|
| **Masthead** | Wordmark, Today, Archive, Your show; optional verification notice below | Default, scrolled, notice present | Desktop text navigation; mobile compact controls with 44 px targets; current destination uses `aria-current` | Do not add Learn, Progress, Explore, notifications, or a search field |
| **Context header** | Back, episode title, optional stage action, overflow | Paper, Booth, sticky, collapsed | Title may visually clamp but full name remains in accessible label; back follows browser history safely | Do not turn it into a four-step lesson header |
| **Your show sheet** | Sheet title, Cast, What the show knows, Voice tape, About, Account essentials | Desktop right sheet; mobile full-height bottom/side sheet | Focus trap, Escape close, initial focus on title, restores trigger focus | Not a settings dashboard; no unrelated toggles |
| **Active-session band** | Episode title, natural-language position, Continue | Listening, Notes, Call-in, After-show; nearing 48h | Full-width flat band; screen reader announces once when Today opens | No percentage, celebratory icon, or urgency countdown |
| **Compact player** | Host mark, title, play/pause, elapsed time, expand/close | Playing, paused, buffering, error | Bottom sticky; respects safe area; controls 44 px; Media Session API | Never persists during a live call or hides a blocking error |

## Programme and episode components

### Programme pitch

**Purpose:** Make a one-line idea feel written and selectable rather than generated and configurable.

**Anatomy:** issue number; title (hard cap 140 characters); cast pair; format; factual readiness status when applicable; primary action; optional overflow for remix.

**Variants:**

- **Lead prepared:** large serif title, “Ready now,” prominent Play action.
- **Supporting:** smaller title row, no readiness claim, opens production sheet.
- **Selected:** title holds position while production sheet opens; no bright selected card.
- **Unavailable:** retained only when a generation attempt failed; explanatory inline state and Retry.
- **First-show pitch:** one isolated cue-sheet composition with Accept and one “Another idea” action.

**States:** default, hover, keyboard focus, pressed, generating, ready, error, disabled by active-session conflict.

**Accessibility:** the full title is the accessible name; metadata follows in the label; readiness is text; rows are links/buttons with a single primary target rather than nested click traps.

**Content limits:** title 140 characters; format label 28 characters; one or two host names; no reason-for-recommendation text.

**Misuse:** no thumbnail, confidence score, “recommended,” topic tags, learning target, or multiple badges.

### Episode plate

A deterministic typographic identity for an episode. It contains title, issue date, cast marks, and format. It may use one accent field or rule. It never uses generated imagery or a fake cover-art square by default.

Variants: programme lead, full episode, compact archive, Weekly Proof. Long titles recompose rather than truncate: the plate reduces display size one step after 70 characters and permits up to five lines on mobile.

### Host identity and cast pairing

A **host mark** combines a stable abstract mark, host name, and accent. A **cast pairing** overlaps or aligns two marks with an explicit “and”/localised connector; it never blends faces or implies a photograph.

States: speaking, listening, selected for cast, retired, unavailable voice. Speaking may strengthen the accent rule or fill the mark using real state, not continuous decorative pulsing.

Content: host names must support 30 characters and mixed scripts. The voice label is descriptive and neutral (“warm, low energy”; “bright, fast”) rather than demographic fiction.

### Weekly Proof item

An editorial special with proof surface, “Weekly Proof” kicker, title, two-minute duration, cast, and Play. It does not preview wins as metrics. After listening, it may reveal the exact clips/quotes included in the piece.

## Audio and transcript components

### Full produced-audio player

**Anatomy:** title context; large Play/Pause; 10 seconds back; scrubber; elapsed/total; speed menu limited to 0.8× and 1.0×; buffering state; output/permission messages only when relevant.

**States:** idle, loading metadata, playable partial stream, playing, paused, scrubbing, buffering, ended, synthesis error, offline-cached.

**Rules:**

- The scrubber shows the known total duration. During partial streaming, the available range is visually distinguished from the total but remains truthful.
- Seeking beyond the buffered range requests the segment and shows local buffering; it does not fake availability.
- Speed selection is a small text control, not a prominent learning tool.
- The primary control is 52 px desktop and 56 px mobile, with a 48 px minimum target.

### Transcript line

**Anatomy:** speaker name/mark, one semantic utterance, timed word spans, optional current-line indicator.

- Default transcript is readable as ordinary paragraphs.
- The active word receives a quiet background and underline; there is no karaoke bounce.
- Speaker changes create spacing, not message bubbles.
- A user can turn off auto-follow without stopping playback.
- Screen readers receive the transcript as paragraph text; word exploration uses a roving-focus mode so thousands of words do not flood the tab order.

### Scrubber and transport

- Track: 4 px visual, 44 px hit area.
- Thumb: 20 px visual, increases to 24 px while dragging.
- Keyboard: Left/Right 5 seconds; Shift+Left/Right 10 seconds; Home/End to bounds.
- Time announcements occur on command, not every second.
- The Play triangle and time direction do not mirror in RTL.

### Audio status

A compact inline status with text and optional icon: “Opening ready; the rest is arriving,” “Buffering,” “Audio could not start,” or “Playing from this device.” It never uses fake percentages or decorative waveform loops.

## Reading and definition components

### Article header and body

The header contains a contextual kicker, title, optional one-sentence deck, cast reference, date, and estimated reading time. It does not contain learning objectives, vocabulary count, or completion status.

Body supports paragraphs, subheads, block quotes when editorially warranted, and source/context notes only when the generated article genuinely relies on a named source. Decorative pull quotes are not used merely to fill space.

### Tap-to-define trigger

The whole word is tappable without changing the article’s visual texture. On pointer hover, a subtle underline appears after 120 ms. On touch, the first tap opens the definition; it does not select text first. Native text selection remains available through long press.

### Definition popover / bottom sheet

**Contents, in order:** selected word in context; native-language meaning; part of speech; one target-language example. Nothing else.

- Desktop: anchored popover, maximum 352 px wide, repositions to remain in viewport.
- Mobile: bottom sheet with drag handle, selected word, and close button; it never covers the word without also repeating it.
- Long meaning: scrolls inside a maximum 50vh body; sheet itself remains dismissible.
- Repeated taps update the same open surface rather than stacking popovers.
- Escape, outside click, Close, or browser Back dismisses correctly.
- The selected word is returned to focus on close.

## Voice-interaction components

### Call-in stage

**Anatomy:** show title; host mark/name; explicit “AI host” disclosure available in context; live-state label; primary microphone state; mute; captions; End; connection message; optional recording-status line.

**Visual states:**

- **Connecting:** static status and cancel action; no fake waveform.
- **Host speaking:** host mark gains a 3 px accent edge; real audio energy may modulate a short line if available.
- **Host listening:** copy “On the line” / “Listening”; user mic control becomes primary.
- **User speaking:** text “You’re on”; mic fill changes; no score or waveform judgement.
- **Silence:** no countdown; after the host’s prompt, status returns to listening.
- **Ending:** controls simplify while the host signs off.
- **Failed live line:** recovery sheet offers voice notes within the same session.

### Voice-note fallback

A turn-based audio exchange, not a chat substitute. Each note displays duration, Play, transcript reveal, and state: recording, uploading, sent, host replying, failed. The host may answer with a generated voice note and transcript. The argument and stage remain Call-in.

### Microphone permission panel

Plain language, browser-specific help only after denial, and two actions: Try again / Continue with voice notes. It states whether call-in audio will be stored under the current consent choice. Permission prompts are never triggered before the user taps Get on the line.

## Messaging components

### After-show thread

Host messages are set as short editorial lines with host name and mark, not large coloured bubbles. User messages use a subtle inset surface to preserve turn ownership. The thread width is 640 px maximum.

### Composer

Text only in v1. One to three lines by default, grows to six lines, then scrolls. Send is labelled accessibly. Enter sends only when the user’s locale and platform convention support it; Shift+Enter always creates a new line.

**Lifecycle variants:**

1. **Open:** ordinary reply field.
2. **Closing:** after the host’s natural closer, placeholder changes to “One last thing…” and supporting text says the thread is ending.
3. **Closed with one final reply:** composer is removed.
4. **Note for next time:** a collapsed “Leave this for the next show” field accepts further text without promising an immediate answer. Submitted notes show “Saved for next time.”

No typing indicator remains on screen once the host has closed the thread.

## Inputs and controls

| Component | Specification | Content and misuse rules |
|---|---|---|
| Primary button | Solid Petrol on Paper, Broadcast on Booth; 44/52 px heights | One primary action per region; no gradient or shine |
| Secondary button | Transparent with 1 px border | Do not use for destructive action beside a weak primary |
| Text action | Underlined on hover/focus, minimum 44 px target when standalone | Suitable for Skip, Another idea, or Back—not primary consent |
| Text field | Persistent label, helper/error below, 6 px radius | No placeholder-only labels; no prompt-engineering examples unless needed |
| Searchable language selector | Search input, locale name, native-script name, single selection | Do not group languages by popularity in a way that hides the full list |
| Segmented choice | Maximum 3 short mutually exclusive choices | Use list/select for longer format or voice inventories |
| Format selector | Editorial list with name and one-line description; free-text option last | No “best for your level” metadata |
| Cast selector | One or two stable host marks; prevents third selection | No avatar marketplace layout |
| Consent choice | Two equally legible choices with consequence text | No preselection, visual guilt, or deceptive primary emphasis |
| Confirmation dialog | Specific object and consequence, safe action first | Destructive verb must name the action |
| Inline correction | Current remembered fact, correction field, Save/Cancel | Does not expose confidence scores or full learner file |

## Feedback and system-state components

| State | Treatment |
|---|---|
| Loading known content | Preserve layout; use text/line skeleton only where shape is known |
| Generating new media | Show the real title plate and an honest stage-neutral message; allow leaving |
| Empty | Explain what will appear after the first relevant action; never add demo stats |
| Error | State what failed, what remains safe, and one recovery action |
| Offline | Persistent slim banner; loaded reading/audio remains available; live/new generation disabled |
| Paused | Preserve exact position; show Continue, not Restart |
| Abandoned | Neutral archive label “Ended early”; no shame colour or copy |
| Deleted audio | Replace player with “Audio removed; transcript remains” |
| Permission denied | Inline panel with browser help and non-blocking fallback |

# Core screen specifications

## Entry and account creation

### Purpose and first question

Establish the category in one glance and collect only what is required before the producer can speak. The user’s question is: **“What is this, and can I begin without administering a course?”**

### Start screen

**First viewport:** warm Paper canvas; small For one wordmark; one large editorial statement; one concrete supporting line; one action.

Suggested composition:

> **A show made around you, in the language you want to live in.**  
> Recurring AI hosts. New episodes shaped by your interests and your week. You decide what goes on air.
>
> **Make my show**

A short disclosure below the action says, “The hosts are AI characters you create and control.” No feature grid, testimonials, app screenshots, or animated AI motif appears.

### Account sequence

1. Email/password or Google/Apple.
2. Name: label “What should the show call you?”
3. Birth date, with 18+ plain-language requirement.
4. Native language: searchable single-selection list.
5. Target language: searchable single-selection list.

The sequence uses one question per viewport on mobile and a two-column editorial/form composition on desktop. Back is always available until account creation completes. OAuth buttons are equal in hierarchy to email, not oversized promotional blocks.

### Email verification

Verification does not block the first session. After account creation, a slim notice appears only on Paper surfaces:

> **Check your email before the next show.** We sent a verification link to name@example.com. · Send again

Before session two, selecting a pitch opens a blocking but calm verification panel. The current programme remains visible behind it. Successful verification returns directly to the selected pitch.

### Empty, loading, and failure

- OAuth loading keeps the provider button in place and disables duplicate submission.
- Existing-account conflict offers Sign in without losing language selections.
- Under-18 date: “For one is currently for adults aged 18 and over.” No moralising or workarounds.
- Email delivery failure leaves session one available and provides Resend.
- Language inventory failure falls back to the cached launch list; it never guesses unsupported languages.

### Responsive and accessibility

At 200% text, the statement and form stack naturally; no viewport-locked hero. Labels are persistent, errors are linked with `aria-describedby`, password managers work, and birth date accepts locale-appropriate segmented or native date input without forcing a calendar picker.

### Must never appear

A level selector, placement test, learning goal checklist, streak promise, “AI-powered” headline, prompt box, or testimonial carousel.

## Intake conversation

### Purpose and first question

Build enough personal and linguistic context to produce the first real show while keeping the interaction human-scale and transparent. The user asks: **“Can this producer understand me without turning me into a form?”**

### Composition: the producer desk

The intake does not resemble a chat app. It is a continuous interview script in a centred 760 px column:

- current producer turn appears as a large authored paragraph with a compact Play/Pause control;
- earlier producer turns remain as transcript paragraphs;
- user responses appear as inset quotations with a small “You” label;
- the reply dock sits at the bottom with **Type** and **Record** modes;
- a narrow side note on desktop shows “About 10 minutes” and the AI/recording disclosure, not a checklist of fields.

Only the current exchange has high contrast; older turns soften slightly but remain readable. There are no speech bubbles, avatars, typing dots, or assistant tool labels.

### Turn-taking

- Producer audio never autoplays over user recording.
- When producer audio ends, focus moves to the reply dock without opening the microphone.
- The user chooses text or voice for every reply.
- Record mode shows elapsed time and Stop; it does not show pronunciation quality.
- The user may replay the producer turn and edit a text reply before sending.
- A sent voice reply may be replayed and replaced before the producer responds.

### Progress without a progress bar

No percent, step count, or checklist appears. Progress is communicated in three ways:

1. At the beginning: “This takes about ten minutes.”
2. At natural transitions, the producer says concrete lines such as “I know why you’re here. Now I need to know what would make the show worth hearing.”
3. Near the end, the producer says “Two things left: how you want the language to sound, and what we keep on tape.”

If the user leaves, Today is replaced by a single resume state: “Continue setting up your show.”

### Short answers and sparse fields

After two attempts on a topic, the producer moves on without exposing missing data. The interface never marks an answer incomplete. If silence or a one-word reply is accepted, the script simply continues. The producer may use an optional quick choice only when it fits conversation (“Mostly work, travel, or family?”), followed by an open reply opportunity.

### Target-language moments

Three or four brief target-language moments are embedded in producer audio. The interface does not label them as tests. When the producer switches language, the transcript preserves the target script and provides a small native-language replay/meaning action only if the user asks or appears stuck. No score follows.

### Dialect samples

A flat list of 10–15 second sample players appears inside the script at the relevant turn. Each row has variant name, Play, and Select. Only one sample may play at a time. Selecting a variant is reversible until the handoff begins.

### Voice-storage consent

The producer introduces the choice in-story, then the product voice takes over in a visibly plain consent panel:

> **Keep call-in audio for future comparisons?**  
> We always keep the written transcript because it is part of your show. Keeping audio is optional. If you allow it, future Weekly Proof episodes can compare your voice over time. You can stop and remove stored clips later.
>
> **Keep call-in audio**  
> **Use transcripts only**

Neither option is preselected or visually shamed. Declining does not introduce a warning or disabled-feature list.

### AI disclosure

The first producer turn says plainly that the producer and hosts are AI characters. The disclosure is repeated in the consent panel’s “How this works” link and later in Your show. It is not repeated on every message.

### Failure and recovery

- Producer audio failure: text remains; Retry audio; user may continue by text.
- Speech upload/transcription failure: keep local recording until Retry or Replace; do not lose the reply.
- Connection loss: all completed turns are local-cached; the reply dock becomes read-only with Offline state.
- Intake generation failure: one neutral recovery line and Retry; never reveal model/provider details.

### Transition to the default duo

The final producer paragraph visually closes with a horizontal rule and the line “I have enough to make the first show.” The page then transitions into the first-show handoff; it does not return to a dashboard.

### Must never appear

A profile-completion percentage, question count, personality radar, CEFR result, “analysing you” animation, assistant bubbles, or a list of stored learner-file fields.

## First-show handoff

### Purpose and first question

Turn setup into a real piece of media as quickly as possible. The user asks: **“Did all of that actually become a show?”**

### Host introduction

The Paper surface becomes an episode plate carrying the duo’s names and non-human marks. A concise line states:

> **Meet Inés and Rafa—your AI hosts.** They have one job: make a show worth joining.

The 60–90 second recorded introduction has a compact produced-audio player and an optional transcript. The duo’s relationship is demonstrated through the audio, not a trait list.

Character creation is mentioned once after playback: “You can add other voices to the cast later.” It is a text link to Cast, not a branching flow.

### First live-generated pitch

One pitch appears as a printed cue-sheet block, using a real intake interest and no exaggerated callback. Actions:

- **Put this on**
- **Another idea**

“Another idea” may be used once. If the alternative is also rejected, the UI opens a minimal topic field based on the top interest; it does not present infinite regeneration.

### Generation wait

After acceptance, the pitch becomes the episode plate. The interface says:

> **Making the opening.**  
> The episode can start as soon as the first part is ready. You can leave this page; nothing will be lost.

The host introduction remains replayable. There is no spinner in empty space and no percentage. When the first audio chunk is ready, Play becomes active and the line changes to “The opening is ready; the rest is arriving.”

The three-minute ceiling is handled with progressive readiness. If it is exceeded, the interface offers Retry and “Use a simpler version of this idea,” which invokes the PRD fallback without exposing the quality gate.

### Transition into the cycle

Pressing Play expands the title plate into the Booth environment. The first-show episode may be shorter, but the visual system is identical to later episodes so the user learns the real product immediately.

## Daily arrival / Today

### Purpose and first question

Present a finite set of genuinely tempting ideas while proving that one has already been made. The user asks: **“What did my show bring me today?”**

### Information hierarchy

1. Active-session band, when present.
2. Weekly Proof, when present.
3. Date/issue line.
4. Lead prepared pitch.
5. Supporting pitches.
6. Bring your own idea.
7. Quiet footer with Archive and Your show links on very small screens.

### Chosen composition

Pitches are an **editorial programme**, not cards, covers, tiles, or a schedule with times.

- Lead pitch occupies seven columns desktop and full width mobile.
- Supporting pitches form a ruled list in five columns desktop.
- Issue numbers 01–05 create order without implying ranking quality.
- Topic, format, and cast are communicated through the title and one compact metadata line.
- Only the prepared pitch receives “Ready now.” Other pitches do not show a wait estimate until selected.
- The wildcard is not labelled; it should feel like an interesting editorial surprise, not a system category.

### Personal references

Personal callbacks appear only inside naturally written pitch language. There is no “from your life,” memory icon, or explanation of why the detail is known. A callback that could feel sensitive or uncertain is omitted. On hover or tap, no source memory is revealed.

### Host presence

Host marks and names appear in pitch metadata. There is no large duo hero, mascot greeting, or simulated “online” presence. The content, not the characters’ faces, owns the first viewport.

### Persistent playback

No player appears until audio has actually started. Produced audio may persist as a compact player while the user navigates among Paper surfaces. Live call audio never becomes a compact player.

### Loading and staleness refresh

If pitch text is refreshing at app open, retain the dated programme frame and use three short typographic skeleton lines for no more than five seconds. Copy says “Preparing today’s programme” only if the delay exceeds 800 ms. Do not show old and new pitches interleaving; the set replaces atomically.

### Empty and failure

A true empty programme should occur only before onboarding or during a recoverable system failure. If the world check fails, interest-based pitches render normally with no warning. If pitch creation itself fails, show one fallback pitch from the user’s top interest and a quiet Retry for the full programme.

### Responsive specifics

- Desktop first viewport must show the complete lead item and at least the titles of supporting items 02 and 03 at 768 px height.
- Mobile places the primary Play action immediately after the lead metadata, within the first 600–700 px for ordinary title lengths.
- Supporting rows use 20 px titles and 24 px vertical padding; they do not become swipeable carousels.
- At 200% text, the two-column layout collapses before overlap; metadata wraps rather than truncates names.

### Must never appear

Search, filter chips, recommendation explanations, “official” tags, content thumbnails, time-to-learn, streak status, prompt field, infinite scroll, or a greeting that claims emotional need.

## Pitch detail and remix

### Purpose and first question

Give the user ownership over topic, format, and cast without making them write a production prompt. The user asks: **“Can I make this mine without becoming the producer?”**

### Production sheet

Desktop opens a five-column right sheet while the programme remains visible. Mobile opens a full-screen sheet. The pitch title remains the heading. Three editable rows follow:

1. **Topic** — current hook; Edit opens a single text field.
2. **Format** — current format; Change opens the starter list and “Describe another format.”
3. **Cast** — one host or pair; Change opens the cast selector.

Primary action:

- Prepared unchanged pitch: **Play this episode**.
- Changed or supporting pitch: **Make this episode**.

Secondary actions: Close; Start over; Bring your own idea.

### Topic editing

The topic field asks for the subject or question, not a multi-part prompt. It may accept voice input where browser speech capture exists, but text is always available. The helper copy says, “A subject, argument, story, or thing that happened is enough.”

### Format editing

Starter formats are displayed as editorial rows with one-line descriptions: Debate, Story time, News rundown, Interview, Explain it to me, Roast. A final row, “Describe another format,” opens a short free-text field. The system mapping remains invisible.

### Cast editing

The selector shows active host marks, names, and one short voice/character phrase. The user may select one or two. Selecting a third replaces only after a clear choice; it never silently deselects. Retired characters are absent but available through Cast management.

### Generation and readiness

After Make this episode, the sheet becomes a stable generation state containing the final title plate. The user may close the sheet and return later. Today shows “Being made” in place of readiness. Once the opening is playable, the compact system notice says “The opening is ready” without a push notification.

### Failure

- First failure: “That version did not come together.” Retry same idea.
- Second/fallback: “We made a simpler version from the same idea.” Offer Play or Change it.
- Voice or format unsupported: preserve the user’s wording and explain the closest available behaviour only when necessary.

### Must never appear

A JSON-like prompt, advanced settings, tone sliders, target vocabulary, difficulty, temperature, model choice, episode length control, or more than one regeneration action at a time.

## Episode / Listen

### Purpose and first question

Deliver a premium produced episode while keeping language support inside the media experience. The user asks: **“Can I forget that I am using software and follow the show?”**

### Layout

The environment shifts to Booth. The page has three vertical zones:

1. Context header with Back, compact title, cast, and overflow.
2. Episode plate and full player, centred to 840 px.
3. Word-synced transcript, centred to 760 px, with generous space between speakers.

The primary player remains above the fold on mobile. The transcript begins close enough that the first lines are visible without a full screen of ornament.

### Player behaviour

Controls are Play/Pause, 10 seconds back, scrub, 0.8×/1.0×, elapsed/total. Speed is in an overflow or compact menu. No forward-skip control is added because it is not specified.

The episode may start from partial audio. The available range is shown truthfully. If the user seeks beyond it, local buffering appears. A synthesis failure after partial playback preserves the transcript and ready audio, then offers Resume when recovered or Read the notes.

### Transcript

- Always visible below the player.
- Auto-scroll keeps the active utterance within the middle third of the viewport, but pauses immediately when the user scrolls manually.
- “Follow audio” reappears as a small text action after manual scrolling.
- Active word treatment is a quiet selection field and underline; no bounce, colour chase, or per-word screen-reader announcement.
- Speaker labels use host accent but body text remains neutral.
- Every word opens Define.

### Transition to Notes

The unresolved throw is part of the audio and transcript. At the episode end, the final transcript line is followed by a Paper-coloured transition panel:

> **The notes are ready.**  
> They left out one part of the argument.
>
> **Read the notes**

If the user chooses Notes before audio ends, that is treated as a skip. Playback pauses at the stored position, the compact player persists, and the Notes page opens. It does not continue speaking over the article by default. The user may explicitly resume from the compact player.

### Pause, resume, and replay

Closing or navigating away stores audio position. Today says the exact time when useful (“4:12 into the episode”). After completion, replay does not reopen the forward cycle; the episode record shows Listen again and links to the other archived surfaces.

### Loading and errors

- Metadata loading: player shell with title, no fake duration.
- Buffering: current control becomes spinner with visible “Buffering.”
- Audio blocked by browser: show Play manually; never repeatedly attempt autoplay.
- Transcript sync failure: transcript remains readable with “Word timing is unavailable” and a Retry; audio continues.
- Total audio failure: transcript and Notes remain available; offer Retry audio.

### Accessibility

Transport has visible labels/tooltips; keyboard shortcuts do not override text input. Transcript supports roving word focus. The active line uses `aria-current`, not a constantly changing live region. Captions are the transcript itself. At 200% text, player controls wrap into two rows without covering the timeline.

### Must never appear

Waveform grading, comprehension questions, vocabulary sidebar, pronunciation score, learning target, “complete listening” button, or animated host faces.

## Define

### Purpose and first question

Remove a momentary comprehension obstacle without turning the session into dictionary work. The user asks: **“What does this mean here?”**

### Desktop behaviour

Click or keyboard activation opens an anchored popover adjacent to the word. It contains:

- selected surface form and the short surrounding phrase;
- native-language meaning;
- part of speech;
- one target-language example.

The popover uses a 352 px maximum width and 50vh maximum height. It flips above/below and left/right to stay in view. A second word updates the same popover in place. Escape closes and returns focus.

### Mobile behaviour

Tap opens a bottom sheet. The sheet repeats the selected word at the top, so covering the original text is acceptable. Swiping down, Close, or browser Back dismisses it. The underlying audio continues unless the user has enabled a screen-reader preference that pauses on definition; default behaviour does not pause.

### Keyboard and screen reader

Press Enter on a transcript/article line to enter word-exploration mode. Arrow keys move among word tokens; Enter opens Define; Escape returns to line navigation. The selected word, meaning, part of speech, and example are announced as a dialog. Focus does not enter decorative punctuation tokens.

### Edge cases

- Very long definitions scroll inside the sheet/popover.
- Scripts without whitespace use language-specific segmentation; the selected unit may be a character sequence rather than a space-delimited word.
- Punctuation attaches visually but is excluded from the definition token unless linguistically necessary.
- If a definition is not yet available, show “Meaning is still arriving” and retry silently; do not generate a visible spinner for every word.
- Repeat taps are logged invisibly and do not add history, stars, or flashcards.

### Must never appear

Conjugation tables, audio pronunciation, save-to-list, quiz, mastery status, similar words, etymology, or a vocabulary count.

## Notes / Read

### Purpose and first question

Give the user material that changes or sharpens their position before the call. The user asks: **“What did the hosts miss, and what do I now think?”**

### Editorial composition

Paper returns. The article is a genuine editorial object:

- kicker: “Notes for the argument” or a content-specific equivalent;
- title, which may differ from the episode title;
- one-sentence deck only when useful;
- 3–4 minute estimate;
- 19/31 px serif body, 680 px measure;
- optional subheads after 350 words;
- no questions, answer fields, or highlighted target language.

A compact player persists at the bottom if episode audio exists. It is paused on entry unless the user explicitly resumes.

### Relationship to the episode

The opening sentence must immediately add a counterargument, fact, or reason to change sides. A small “From today’s episode” link returns to the episode at the stored position. Host references may appear in the article as editorial context, not as instructions.

### Reading position

There is no progress bar or completion percentage. Scroll position is stored continuously. On return, the page restores position and briefly shows “Back where you left off” as a non-blocking status. Estimated read time is allowed because it describes the media object, not achievement.

### Moving to the Call-in

At the end, a host-coloured rule introduces the invitation:

> **Rafa is still on the other side of this.**  
> Get on the line and settle it.
>
> **Get on the line**

A quiet “Go straight to the call” action is available in the context header from the beginning, supporting the PRD’s skip rule without making skipping the dominant path.

### Long, short, and RTL articles

- Short articles keep the invitation below content; they do not vertically centre to look empty.
- Long articles may use two or three subheads but never a sticky table of contents.
- RTL pages mirror text alignment and editorial offsets; the audio timeline and Play icon remain directionally conventional.
- Mixed-language quotations use explicit directional isolation.

### Failure

If Notes are unavailable but audio is complete, offer Retry and Go to the call. The host does not punish the missing article. If definitions are delayed, reading remains fully available.

### Must never appear

Reading-comprehension prompts, word counters, completion rings, “key vocabulary,” answer submission, source badges that imply an academic exercise, or a floating AI assistant.

## Call-in / Speak

### Purpose and first question

Make the user feel that the show genuinely needs their position while keeping live voice safe and low-anxiety. The user asks: **“Can I join this argument without being judged?”**

### Entry moment

The Paper invitation transitions to Booth. Before requesting microphone permission, the page shows:

- host name and mark;
- one-line stance from the host;
- expected shape: “A few minutes. Leave whenever you want.”
- recording status: “Transcript kept · Audio kept for Weekly Proof” or “Transcript kept · Audio not stored.”
- primary action **Get on the line**.

Permission is requested only after that tap.

### Live composition

The call is full-height on mobile and centred to 760 px desktop. The host mark is large but abstract. The dominant information is a textual state:

- Connecting…
- [Host] is speaking
- Listening
- You’re on
- Bringing it home

Controls sit in a safe bottom dock: Mute, End, Captions. There is no visible countdown. A small elapsed time may appear in the overflow for accessibility/support, but not as a central pressure cue.

### Speaking and listening states

Real audio energy may modulate a simple 3 px line within a narrow range. If real energy data is unavailable, the line remains static; no fake waveform is generated. User speaking is shown by the mic state and “You’re on,” never by correctness or fluency feedback.

### Silence handling

The UI does nothing at five seconds; the host handles it conversationally. After the host offers to wrap following repeated silence, the End action becomes slightly more prominent, but no warning or timer appears.

### Natural and early ending

The host initiates a natural close after the target duration. During sign-off, Mute remains; the primary control changes to End now. At the hard boundary, the sign-off completes and the call transitions to the After-show waiting state. The UI never says “time’s up.”

The user may end early at any time. One confirmation is used only if they tap End during their own active recording; otherwise the host responds to the early ending and closes.

### Leaving and resuming

Navigating away opens:

> **Leave the line?**  
> The episode stays open. When you return, the host will start the call again rather than resuming mid-sentence.

On return, the host receives the prior partial transcript and opens with one acknowledgement. The UI does not replay a fake “live” moment from before.

### Voice failure and fallback

If connection or synthesis fails:

> **The live line dropped. Nothing was lost.**  
> Keep the argument going by voice note, or try the live line again.

Voice-note mode appears within the Call-in stage. The user records, reviews, and sends a note; the host replies asynchronously with audio and transcript. Session state remains preserved.

### Accessibility and anxiety sensitivity

- Captions are available without implying correction.
- Text-only participation in the live call is not part of the settled PRD; if voice is impossible, voice notes remain the specified fallback. Intake always retains text.
- Status changes use a polite live region only when state changes, not on audio energy.
- There is no forced full-screen mode, camera, speaking score, interruptive haptic, or countdown.
- End is always visible and requires at most one action.

### Must never appear

Pronunciation meters, confidence bars, “great job,” per-turn praise, tutor face, script suggestions, answer choices, or a pulsing red recording theatre unrelated to actual state.

## After-show / Chat

### Purpose and first question

Let the social energy decay naturally after the call, add one new angle, and then close. The user asks: **“Does this feel like the last few messages after a real argument?”**

### Entry and delay

After the call, Paper returns with the episode title and a narrow thread. If the first host message is not ready, the page says “They’re writing back” for up to 30 seconds. The user may leave; Today shows “After-show reply arriving.” There is no typing bubble animation that continues indefinitely.

### Message composition

Host turns are short lines with host name/mark and no enclosing bubble. User turns use a subtle Paper-100 inset. The page does not show timestamps unless the session spans a long pause. The thread supports target-language text and native-language system messages without mixing voices.

### Ending behaviour

The host sends three to five messages and closes naturally. After the closer:

1. Composer remains for one optional “One last thing…” reply.
2. If used, the host sends exactly one final short reply.
3. Composer disappears and a horizontal rule closes the thread.
4. A collapsed **Leave this for the next show** field accepts later notes without immediate response.

After closure, the page footer reads:

> **That’s the show.**  
> Back to Today

No next pitch is shown inside the thread.

### If the user writes again later

Text entered through “Leave this for the next show” is saved as a future callback seed. The UI says “Saved for next time.” It does not show a waiting indicator or promise a response time. The next session may contain one callback line as specified.

### Failure

A failed outgoing message remains editable with Retry. If the host response is delayed, the user’s message is safely stored and the thread shows “Reply will appear here when it is ready.” No notification is promised.

### Must never appear

Open-ended “Ask anything,” attachment tools, voice input, online status, read receipts, typing games, infinite message history, or a companion-style “I’m always here.”

## Session completion

Completion is handled **inside the After-show surface**, not a separate celebration screen. A dedicated page would turn completion into an achievement state and interrupt the social ending.

The completion footer contains only:

- the closing line “That’s the show”;
- date and cast in small metadata;
- Back to Today;
- optional Close player if archived audio is still active.

It does not display a summary, score, vocabulary list, time spent, call duration, next episode, confetti, applause, or a host asking the user to return.

If the user skipped After-show, the Call-in ending may show the same quiet footer after the 30-second message window, with “Read the after-show message” as a secondary link when it arrives.

## Paused and resumed sessions

### Persistence contract

The UI restores:

- Episode audio position and follow-transcript preference;
- Notes scroll position and open definition dismissed;
- Call-in as a fresh opening with prior partial transcript available to the host;
- After-show transcript and composer lifecycle.

### Resume presentation

Today displays one active-session band above all new content. The label is stage-specific:

- “4:12 into the episode”
- “You left midway through the notes”
- “The line will reopen with a fresh start”
- “The after-show thread is still open”

There is one Continue action. An overflow contains Abandon.

### Active-session conflict

Selecting a new pitch opens a confirmation with the old title and position:

> **You still have “The case against five-day trips” open in the notes.**  
> Starting this episode will end the other one early.
>
> **Continue the open episode**  
> End it and start this one

The safe action is first and visually primary. The destructive action uses Error colour only on hover/focus/confirmation, not as a large red block.

### Forty-eight-hour expiration

The active band may quietly say “Available until tomorrow evening” only inside its overflow; no countdown is shown on Today. At 48 hours it moves to Archive as “Ended early.” Partial media remains replayable where available. It no longer appears as a task or warning.

## Weekly Proof

### Purpose and first question

Reveal concrete change without converting the product into analytics. The user asks: **“Is this actually changing how I speak?”**

### Placement and distinction

When available, the Proof occupies a full-width Proof-100 field above the programme. It is labelled “Weekly Proof,” has a title such as “Two ways your past tense changed,” the week date, cast, and a two-minute Play control.

It differs from an ordinary episode through colour, compact duration, and a “tape splice” typographic rule—not a chart, badge, trophy, or percentage.

### Playback and comparison

The Proof is a produced audio mini-episode. After playback begins, a “On tape” section becomes available below:

- voice consent on: two short clip players labelled by date;
- voice consent off: two verbatim text excerpts labelled by date.

Concrete wins are written as editorial annotations, maximum three. There is no aggregate score. The “next focus” appears as one host-spoken line and one transcript line, not a goal card.

### Flat week

The Proof says so plainly. The surface does not turn warning-red or apologise. Example:

> **Flat week. No invented win.** The show is easing the next call-in and bringing the same structure back from a different angle.

This may be delivered by the hosts in their established voice, followed by a plain product transcript.

### Completion and archive

After the two-minute piece, the page returns to the programme with a single Back to Today action. The Proof remains in Archive in chronological order with its own label. It does not permanently pin to a progress area.

### Unavailable state

If the user did not qualify or generation failed, the Proof simply does not appear. There is no empty placeholder, missed-proof message, or retry pressure on Today. A transient generation failure may be retried silently before omission.

## Archive

### Purpose and first question

Preserve the show’s history as media, not convert it into a performance record. The user asks: **“What have we made together, and can I revisit it?”**

### Composition

Archive is a chronological editorial index grouped by month. Each flat row contains:

- date;
- episode title;
- cast;
- format;
- state: Complete or Ended early;
- duration when audio exists.

Weekly Proof entries use the Proof accent and “Weekly Proof” label. Rows are separated by rules; there are no cover tiles.

### Search decision

V1 has **no archive search** because the PRD specifies browsing by date but does not authorise search. The index remains usable through month headings, sticky year selector on large archives, and browser Find. Search can be added later as a product decision, not silently invented.

### Episode record

Selecting an entry opens a read-only episode record with in-page sections:

- Episode and transcript;
- Notes;
- Call-in recording if consented and still stored, otherwise transcript;
- After-show.

A compact in-page index uses these media labels. Speak is never reactivated. Replay is allowed. Abandoned records show only the surfaces that exist and a neutral “Ended early” note.

### Empty state

> **Your archive starts after the first show.**

The action returns to the current setup or Today. No sample episodes or fake history are inserted.

### Responsive and accessibility

Desktop rows use a date column and flexible title column. Mobile stacks date/state above title, with cast/format below. Rows remain 56 px minimum. Month headings are real headings for screen-reader navigation. Status is text, not only an icon.

### Must never appear

Charts, totals, streaks, hours listened, words learned, heat maps, completion percentages, leaderboards, milestones, or social sharing.

## Cast creation and roster

### Purpose and first question

Let the show’s cast grow as a relationship and editorial choice, not as a game or companion marketplace. The user asks: **“Who belongs in my show, and how do I shape them?”**

### Discoverability

Cast is accessed from Your show and from the cast row in a production sheet. It is mentioned once during first-show handoff but never promoted on Today. The roster page has the default duo first, then active created hosts, then a collapsed Retired section.

### Roster composition

Each host row uses mark, name, one-line character description, voice sample, and status. Default duo is labelled “Default duo.” Created hosts have Edit through conversation and Retire actions. The page shows “6 of 6 created hosts” only when the maximum is reached; it is capacity, not gamification.

### Conversational creation

“Add a voice to the show” opens a producer-led interview using the same script-like composition as intake, but much shorter. It gathers name, voice, two to four traits, optional quirk, and optional backstory. The chassis mapping remains invisible.

Voice samples appear as a flat selectable list with neutral descriptions. The product must not infer or label sensitive demographic attributes beyond what the provider legitimately exposes and the user chooses.

### Introduction audio

After confirmation, the new host’s deterministic title plate appears and a 30–60 second introduction plays. The user may Keep, Change the voice, or Edit the description. “Delete” is not used; Retire preserves history.

### Editing, retiring, and un-retiring

Editing opens a short conversation with the current description in context. Retire confirmation explains that past episodes and memory remain. Retired hosts appear in a collapsed section with Bring back. They cannot be cast until restored.

### Maximum roster

At six active created hosts, Add is disabled with clear copy:

> **The active cast is full.** Retire one voice before adding another. Past episodes and relationships stay intact.

No upgrade or scarcity message appears.

### Must never appear

Human portraits, avatar body builders, age/gender sliders, romance framing, rarity, marketplace cards, likes, public sharing, or “bond level.”

## Knowledge and trust controls

### Purpose and first question

Make the show’s memory and recording behaviour inspectable without creating a settings dashboard. The user asks: **“What does this show know, what is stored, and how do I correct it?”**

### Your show sheet

Your show is a table-of-contents sheet, not a dashboard. It contains four editorial rows:

1. **Cast** — “The voices in your show.”
2. **What the show knows** — “Life facts and interests you have shared.”
3. **Voice tape** — current audio-storage choice.
4. **About this AI show** — identity, memory, and limits.

Account essentials appear in a quiet footer: email verification, email address, Sign out. No notification, appearance, difficulty, or learning settings appear.

### What the show knows

The summary is grouped in plain language:

- Why you want the language;
- Things you care about;
- What is happening in your life;
- Things to follow up on.

It excludes the language profile, errors, proficiency, targets, engagement scoring, and inferred energy. Each statement has **That changed** or **Remove this from the show’s active memory** only if the PRD/data model supports dormancy; removal makes it dormant rather than claiming deletion. The UI must use honest wording: “Stop using this in the show” rather than “Delete forever.”

Corrections open a direct text/voice input and overwrite the fact immediately. The system confirms the new wording in plain language. Confidence values are never shown.

### Voice tape

The surface states:

- whether future call-in audio is stored;
- that transcripts are always stored as core show records;
- how Weekly Proof works under the current choice;
- the supported revocation action.

Revocation copy:

> **Stop keeping call-in audio?**  
> Future calls will keep transcripts only. Stored call-in clips will be removed within 24 hours. Weekly Proof will use text comparisons instead.
>
> **Stop keeping audio**  
> Keep current choice

After confirmation, archived audio players are replaced as deletion completes. The transcript remains.

### AI disclosure

“About this AI show” states that producer and hosts are AI characters, their voices and replies are generated, they use the stored show memory, and they may be wrong. It also states that a host will not claim a memory unless the system is confident; corrections are available.

### Unsupported data actions

General data export, account deletion, and instant deletion of all product data are not specified in the v1 PRD and therefore are **not designed here**. The interface must not imply that Voice tape revocation deletes transcripts or the account. This is a known gap against the Product Concept’s broader trust promise.

### Confirmation and recovery

Consent changes are immediate in the UI. Audio deletion may take up to 24 hours and shows “Removal in progress” beside affected archive items. If deletion fails, the system retries automatically and shows a persistent trust-surface error with Support/Retry—not a transient toast.

### Must never appear

A generic Settings heading, dozens of toggles, hidden consent, prechecked storage, dark-pattern button hierarchy, full internal learner file, error analytics, or a statement implying the hosts are human.

# Responsive behaviour

## Responsive philosophy

Mobile is the primary participation environment, not a compressed desktop. Desktop offers wider editorial composition and more simultaneous context; mobile prioritises one clear media object, thumb-reachable controls, and safe audio interruption handling.

The system responds to **available width, text size, input mode, and safe area**, not device names alone. Components must reflow before text overlaps. Horizontal scrolling is prohibited for core content, except the browser’s native behaviour for unusually long unbroken code-like strings—which should not occur in ordinary show content.

## Global mobile rules

- Respect `env(safe-area-inset-top/right/bottom/left)` on iOS.
- Fixed bottom controls sit above browser chrome and the keyboard using visual-viewport measurements.
- Primary touch targets are 48 px where space permits; never below 44 px.
- Do not rely on hover for definitions, metadata, or secondary actions.
- The compact player and call controls never overlap the chat composer or system permission banners.
- When the keyboard opens, the current field scrolls into the upper 40% of the visual viewport; headers may collapse.
- Landscape call-in uses a two-column arrangement—host state left, controls right—while preserving an obvious End control.
- On screens below 360 px, outer margins reduce to 16 px and metadata stacks; display type reduces one step, never below 32 px for the lead pitch.
- Large-text mode takes priority over decorative composition. At 200% text, all multi-column core layouts become one column.

## Core-screen responsive differences

| Surface | Mobile | Tablet | Desktop |
|---|---|---|---|
| Start/account | One question per viewport; action above safe-area bottom | Statement above form or 3/5 split | 5/7 editorial statement and form; no tall hero lock |
| Intake | Continuous script; reply dock; audio control inline | Script plus narrow disclosure rail | 760 px script with 240 px contextual rail |
| First handoff | Host marks and intro player stacked; pitch below | Title plate and pitch may sit side by side | Title plate 7 cols, pitch cue 5 cols |
| Today | Lead then ruled supporting list; no carousel | Lead 5 cols, support 3 cols | Lead 7 cols, support 5 cols |
| Production sheet | Full-screen sheet, sticky action at bottom | 80% width sheet | Right-side 5-column sheet, programme remains visible |
| Episode | Player controls wrap; transcript 17/28 | Centred 7 columns | Player 840 px; transcript 760 px |
| Define | Bottom sheet | Bottom sheet or anchored popover by pointer mode | Anchored popover |
| Notes | 18/29 text; 20 px margin | 640 px measure | 680 px measure with optional metadata rail |
| Call-in | Full-height; bottom dock; captions overlay | Centred stage; larger host mark | 760 px stage; extra room for status/disclosure rail |
| After-show | Full-width thread within margins; composer above keyboard | 600 px thread | 640 px thread with episode context in narrow rail |
| Archive | Date/status stacked above title | Two-column date/title row | Date, title, cast, format, state columns |
| Cast | One host per row; sample opens inline | Two-column roster only if text remains readable | Default duo 2-up; created hosts as editorial rows, not cards |
| Trust | Full-screen Your show; one section at a time | Wide sheet | 480–560 px right-side sheet |

## Mobile navigation

The top masthead is 56 px plus safe area. On Today it contains the wordmark, Archive, and Your show. On contextual surfaces it contains Back, a short title, and overflow. It hides only during deliberate reading scroll, using a 12 px downward threshold and 8 px reverse-scroll reveal; no time-based hiding.

A bottom navigation bar is deliberately rejected because it would overstate the IA, compete with the compact player/call controls, and make the product feel like a generic app shell.

## Player placement

- Produced audio compact player sits at the visual viewport bottom and includes bottom safe-area padding.
- On Notes, it defaults to paused after a stage transition but remains expandable.
- During form entry or After-show composition, it moves above the keyboard if playing; if paused, it may collapse to a 44 px title strip to preserve space.
- Live Call-in never uses the compact player. The call owns audio focus and the full bottom control dock.

## Transcript and reading behaviour

- Transcript speaker labels remain sticky only within the current utterance on desktop; on mobile they are ordinary inline labels to avoid occluding text.
- Auto-follow accounts for mobile browser chrome and stops when the user touches or scrolls the transcript.
- Notes never use multi-column newspaper text. RTL and large text preserve a single readable column.
- Definition bottom sheets use at most 70% of the visual viewport and never trap the user below the keyboard.

## Keyboard avoidance and input

- The After-show composer uses `position: sticky` inside the document flow where possible; fixed positioning is a fallback with visual-viewport calculations.
- Voice recording controls remain visible when the software keyboard is closed; selecting Type dismisses microphone UI cleanly.
- On iOS, permission education appears before the system prompt so the abrupt browser dialog is not the first explanation.

## Browser chrome and background behaviour

Produced audio uses the Media Session API where available and can continue when the browser backgrounds it. The interface never promises background live calls; before the user backgrounds or navigates from an active call, it warns that the line may close. Restoration returns to the Call-in recovery state rather than pretending continuity.

# Interaction and motion

## Interaction character

For one should feel **composed, immediate, and acoustically quiet**. Motion indicates continuity between media forms and confirms state. It does not advertise intelligence, create anticipation, or reward completion.

## Motion hierarchy

| Interaction | Behaviour | Duration |
|---|---|---:|
| Hover/focus | Colour/border change only | 80–140 ms |
| Programme row open | Row title holds position while sheet enters from edge | 220 ms |
| Prepared pitch to Episode | Title plate expands; Paper crossfades to Booth | 320–420 ms |
| Supporting pitch generation | Sheet remains; title plate settles; status changes without looping spectacle | 220 ms |
| Full player to compact player | Shared title/control transform; critically damped spring permitted | 280–340 ms |
| Transcript word change | Background/underline crossfade, no translation | 80 ms |
| Define open | Fade + 4 px scale/translate on desktop; sheet rise on mobile | 140–220 ms |
| Episode to Notes | Booth recedes; Paper rises beneath final transcript line | 320 ms |
| Notes to Call-in | Host accent rule expands into Booth edge; no countdown | 320–420 ms |
| Live state change | Text and real state indicator crossfade | 100–160 ms |
| Call end to After-show | Booth dims, host sign-off completes, Paper thread appears | 320 ms |
| Chat message arrival | 6 px upward settle and fade; only new line moves | 160 ms |
| Thread close | Composer height collapses after final reply; closing rule draws once | 220 ms |
| Weekly Proof open | Proof field expands to its player; no celebration | 260 ms |

## Easing

- Standard UI: `cubic-bezier(.2, 0, 0, 1)`.
- Emphasised media transition: `cubic-bezier(.16, 1, .3, 1)`.
- Exit: slightly faster `cubic-bezier(.4, 0, 1, 1)` only when content is truly leaving.
- Spring: only for bottom-sheet/player settling, damping ratio high enough to prevent visible bounce.

## Concurrent-motion rules

- One dominant spatial motion at a time.
- Audio controls remain responsive during page transitions.
- Transcript highlighting may continue while a compact player transforms, but no other decorative motion runs.
- A loading state must never delay a control that is already ready.
- Motion cannot be required to understand order, status, or speaker identity.

## When animation is forbidden

- Consent and destructive confirmation.
- Error copy and recovery actions.
- Under-age rejection.
- Flat-week messaging.
- Audio recording disclosure.
- Any state where motion could imply that the system is listening, recording, or generating when it is not.
- Completion celebration.

## Reduced motion

With `prefers-reduced-motion: reduce`:

- spatial page transitions become an 80 ms opacity change or immediate swap;
- player expansion becomes an instantaneous layout change with focus preserved;
- active transcript word changes without animation;
- live state uses text and static colour only;
- sheets appear without spring or drag-settle animation, while swipe-to-dismiss may remain functional.

# Audio-specific UI

## Audio objects and their visual contracts

| Audio type | Surface and controls | Persistence | Recording/storage indication |
|---|---|---|---|
| Produced episode | Booth full player; timeline, 10s back, 0.8×/1.0×, transcript | Continues on Paper navigation where browser permits; state always restores | No user recording |
| Producer intake audio | Paper inline player in current interview turn | Stops before user recording; does not become compact player | User voice reply state shown separately |
| Host introduction | Paper title plate with short player and optional transcript | Replayable in onboarding/cast record | No user recording |
| Live Call-in | Booth live stage; Mute, Captions, End; no timeline | Exclusive audio focus; leaving may end line | Persistent line states whether audio is stored or transcript-only |
| Voice-note fallback | Call-in turn player/recorder with transcript | Persists as part of current session | Each user note shows upload/storage state |
| Weekly Proof | Proof surface produced player; optional comparison clips | Persists in Archive | Comparison type follows consent |
| Archived user call recording | Archive player only when consented and not deleted | Read-only; removed after revocation | “Audio removed; transcript remains” after deletion |

## Audio focus

- Starting produced episode audio pauses other For one produced audio.
- Starting intake playback pauses episode audio if onboarding is somehow revisited.
- Entering Call-in pauses all produced audio and clears the compact player from view.
- Starting microphone capture pauses output until echo-cancellation setup is complete; host audio and microphone never compete.
- A second browser tab acquiring For one audio focus pauses the first tab and shows “Playing in another tab.”

## Player persistence and navigation

Produced audio state includes source, episode ID, elapsed position, duration, speed, buffered range, and transcript-follow preference. It persists across Today, Notes, Archive, Cast, and Trust. It does not persist across sign-out.

Selecting another episode while one is playing prompts only when it would replace active session state. Replaying an archived episode may replace the compact player without a destructive confirmation because it does not alter session state.

## Interruptions

### Phone calls and operating-system interruptions

When the platform emits an interruption/pause event, For one stores position immediately and shows “Paused by another audio app.” It does **not** autoplay after a phone call ends; the user resumes explicitly.

### Bluetooth and output-device changes

Where the browser exposes output changes:

- a valid device switch continues playback and shows a short non-modal status;
- loss of output pauses and says “Audio output changed. Resume when ready.”
- the web app does not present a custom device picker unless the platform safely supports it.

### Browser background

Produced audio may continue using Media Session metadata: episode title, show name, and deterministic episode plate where supported. Live calls are not promised in background; if the browser suspends, recovery uses the saved partial transcript and fresh-opening rule.

## Streaming and partial readiness

- The player becomes actionable when the first playable chunk and duration estimate are available.
- The scrubber displays loaded/available range separately from total duration.
- Copy: “The opening is ready; the rest is arriving.”
- If later chunks stall, playback continues to the buffer boundary, then shows local Buffering. The page does not reset to a full-generation state.
- Article readiness is independent. If Notes are ready before audio, they remain hidden behind the normal Episode stage unless the user explicitly skips. If audio is ready before definitions, playback starts and definitions retry in the background.

## Transcript synchronisation

Word timing uses the media clock and corrects drift at utterance boundaries. Visual highlighting may lag by no more than 150 ms under ordinary conditions. If drift exceeds a threshold, the system falls back to line-level highlighting and says “Word timing is temporarily unavailable.” It never jumps the scroll repeatedly trying to catch up.

## Buffering and errors

- Buffering under 500 ms: control state only, no copy.
- 500 ms–5 s: “Buffering” beside time.
- Above 5 s: explanatory inline state and Retry connection; transcript remains usable.
- Failed synthesis: Retry audio and Continue with transcript/Notes where available.
- A recovered stream resumes from the stored time; it does not restart unless the source changed materially.

## Microphone permission

The pre-permission screen explains purpose and current storage. After denial, the UI detects whether the browser allows another prompt or requires settings. Instructions name the browser only when known. Voice notes are always offered as the specified fallback.

## Echo and connection warnings

Warnings are actionable and non-judgemental:

- “We’re hearing the host come back through your microphone. Headphones may help.”
- “The line is unstable. We can keep going by voice note without losing the argument.”

The interface never displays a network quality score or technical codec details.

## Audio recording consent visibility

Recording status appears before Call-in entry and remains accessible during the call through a labelled information control. A small persistent line may say “Transcript kept · Audio not stored” or “Transcript and audio kept.” It is not represented by an ambiguous red dot alone.

# Content design and UX writing

## Voice architecture

### Product-interface voice

Clear, authored, adult, and concrete. It describes what is happening and what the user can do. It does not perform a character, praise, tease, or pretend intimacy.

### Producer voice

Warm, observant, economical, and conversational in the user’s native language. The producer asks one thing at a time, acknowledges without flattery, moves on from sparse answers, and is explicit about AI and consent.

### Host voice

Character-specific and primarily in the target language. Hosts may disagree, joke, push back, recast naturally, and close socially. They never act as product support, deliver consent, claim human experiences as fact, or manipulate return behaviour.

### Legal and consent voice

Plain, literal, and free of jokes. It states what is stored, why, what changes after a choice, and how long deletion takes. Button hierarchy is neutral.

### Failure-state voice

Calm and specific: what failed, what was preserved, and the next action. It never blames the user or anthropomorphises the system’s failure.

## Vocabulary rules

Prefer: show, programme, episode, notes, line, call-in, after-show, cast, voice, tape, archive, ready, make, continue, end early, stored, transcript.

Avoid: lesson, exercise, practice, test, score, streak, level, training, assignment, objective, unlock, master, journey, AI-powered, magic, personalised experience, congratulations, great job.

Use “AI host” when disclosure is relevant. Do not use model, agent, LLM, generation pipeline, assessment engine, target queue, or CEFR in user-facing copy.

## Example interface copy

| Situation | Recommended copy |
|---|---|
| Primary start action | **Make my show** |
| Account name | **What should the show call you?** |
| Birth date | **Your birth date** · For one is currently for adults aged 18 and over. |
| Native language | **Which language should we use with you?** |
| Target language | **Which language should the show be in?** |
| Email verification notice | **Check your email before the next show.** We sent a link to {email}. |
| Producer introduction | “I’m the producer—an AI voice helping build your show. I’ll ask about what you care about, then introduce the hosts.” |
| Voice-storage consent title | **Keep call-in audio for future comparisons?** |
| Consent choice | **Keep call-in audio** / **Use transcripts only** |
| Introducing the duo | **Meet Inés and Rafa—your AI hosts.** They disagree professionally. |
| Example pitch | **Karim watched the derby and has one terrible idea about Saturday’s lineup.** |
| Reject first pitch | **Another idea** |
| Remix entry | **Change this episode** |
| Topic field helper | **A subject, argument, story, or thing that happened is enough.** |
| Episode generating | **Making the opening. You can leave; it will be here when it is ready.** |
| Partial readiness | **The opening is ready; the rest is arriving.** |
| Episode ready | **Play this episode** |
| Resume listening | **Continue “The derby committee” — 4:12 into the episode.** |
| Resume reading | **Continue “The derby committee” — you left midway through the notes.** |
| Skip article | **Go straight to the call** |
| Join call | **Get on the line** |
| Pre-call boundary | **A few minutes. Leave whenever you want.** |
| Microphone denied | **Your browser has not allowed the microphone. Allow it in browser settings, or continue by voice note.** |
| Connection failure | **The live line dropped. Nothing was lost.** |
| Voice-note fallback | **Keep the argument going by voice note.** |
| Post-call delay | **They’re writing back. You can leave; the reply will stay here.** |
| Chat closing placeholder | **One last thing…** |
| Closed chat note action | **Leave this for the next show** |
| Saved delayed note | **Saved for next time.** |
| Session completion | **That’s the show.** |
| Weekly Proof title | **This week, on tape** |
| Flat week | **Flat week. No invented win. Here’s what the show is changing.** |
| Archive empty | **Your archive starts after the first show.** |
| Abandoned state | **Ended early** |
| Active-session conflict | **Starting this episode will end “{title}” early.** |
| Safe conflict action | **Continue the open episode** |
| Destructive conflict action | **End it and start this one** |
| Daily cap | Host: “Two shows is enough for one day. We need tomorrow to make the next one worth hearing.” |
| Knowledge summary action | **Show me what you remember** |
| Correct remembered fact | **That changed** |
| Dormant-memory action | **Stop using this in the show** |
| Voice revocation | **Stop keeping call-in audio** |
| Voice deletion status | **Removal in progress. Stored clips will be gone within 24 hours.** |
| General offline | **You’re offline. Anything already loaded still works; live calls and new episodes need a connection.** |
| Audio failed | **Audio could not start. The transcript and notes are still here.** |
| Transcript timing failed | **Word timing is unavailable. The transcript is still complete.** |

### Unsupported deletion copy

No general “Delete all data” or account-deletion copy is provided because those actions are not supported by the settled v1 PRD. Product and legal teams must not insert a misleading control to satisfy the concept language without implementation.

## Host copy boundaries

Hosts may say:

- “You dodged the real question.”
- “I still think your lineup is a disaster.”
- “You went on Friday? Then why did you say Saturday earlier?”
- “We’ll see after the match.”

Hosts may not say:

- “I missed you.”
- “Don’t leave me.”
- “You’re doing amazing.”
- “Come back tomorrow to keep your momentum.”
- “As a person who grew up in…” unless that fictional framing is explicitly, transparently authored and never presented as a real life.

# Internationalisation and bidirectionality

## Language roles

Every surface distinguishes:

- **Interface language:** normally the user’s native language; product controls, consent, failures, and trust.
- **Show language:** target language; episode, Notes, Call-in, After-show, and host dialogue.
- **Mixed support:** native-language meanings in Define and occasional producer clarification.

Direction is set at the smallest meaningful component. The page may be LTR while a target-language title is RTL, or vice versa.

## Mirroring rules

| Element | RTL behaviour |
|---|---|
| Page grid and alignment | Mirror |
| Masthead order | Mirror, preserving wordmark prominence |
| Back navigation arrow | Mirror to follow navigation direction |
| Play triangle | Do not mirror |
| 10-seconds-back icon | Do not mirror; counter-clockwise remains “back” |
| Audio timeline | Keep time advancing left-to-right for platform consistency; labels localise |
| Previous/next textual navigation | Mirror spatial placement and localise labels |
| Host marks | Do not mirror internal artwork; reposition with layout |
| Episode plate accent rule | May mirror as part of composition template |
| Scrubber keyboard arrows | Follow media semantics documented in help; physical Left decreases time, Right increases time |
| Call End/Mute/Captions order | Mirror layout only if usability testing confirms; End remains visually isolated |

## Bidirectional text

- Wrap user names, host names, titles, and imported facts with `<bdi>` or `dir="auto"`.
- Use Unicode isolation controls only through a trusted formatting layer; never concatenate raw direction markers from generated content.
- Punctuation belongs to the linguistic run, not the surrounding UI direction.
- URLs, email addresses, and timecodes use LTR isolation even inside RTL paragraphs.
- Quoted target-language phrases inside native-language consent remain isolated and readable.

## Text expansion and truncation

- Plan for 35% expansion from English and substantially more for compact labels.
- Buttons grow vertically; fixed-width text buttons are prohibited.
- Navigation labels may wrap only in Your show; masthead uses tested short localisations.
- Host names and titles do not truncate on primary surfaces. Archive rows may clamp visually with full text in accessible name and detail view.
- German-like compounds and Thai/Khmer line breaking use language-aware CSS and fonts; never insert arbitrary hyphens into names.

## Script-aware typography

- Arabic display uses Noto Naskh Arabic with increased line height—approximately 1.55–1.7 depending size.
- Arabic UI/transcript uses Noto Sans Arabic; Latin numerals inside Arabic may use the selected locale convention.
- CJK reading body uses a vetted Noto Serif CJK package with 1.8 line height and a shorter character measure.
- Scripts without case do not imitate uppercase kickers; use weight, colour, or spacing instead.
- Faux bold/italic is disabled when the font lacks a real face.

## Transcript timing and word selection

- Timing tokens are language-aware and may represent morphemes or character sequences where whitespace is absent.
- Thai, Chinese, Japanese, Khmer, and similar scripts require a segmentation service aligned with tap-to-define precomputation.
- The visible highlight may span multiple glyphs. The accessible label reads the selected unit and context.
- RTL transcript highlighting follows logical reading order; auto-scroll uses block position, not assumed left-to-right word geometry.

## Dates, numerals, and time

- Date order and month names follow the interface locale.
- Programme issue number may use local numerals if legible; it is decorative metadata, not a global identifier.
- Playback time uses locale digits where platform conventions support them, with tabular width and colon separator.
- Speed notation remains `0.8×` and `1.0×`, positioned according to local typography; the multiplication sign is not translated into an ambiguous letter.

## Localised voice and tone

Copy is transcreated, not literally translated. Each launch language requires review of:

- adult warmth versus childishness;
- natural radio/podcast terminology;
- how direct disagreement feels;
- consent clarity;
- whether “programme,” “notes,” “line,” and “after-show” have natural equivalents;
- culturally appropriate but non-manipulative closing phrases.

# Accessibility

## Standard

Target **WCAG 2.2 AA** for the full responsive web app, with AAA contrast for core body text where feasible. Accessibility requirements are component acceptance criteria, not a final audit checklist.

## Colour and focus

- Normal text meets at least 4.5:1; large text 3:1; controls and focus indicators 3:1 against adjacent colours.
- Core body text exceeds 5.4:1 and primary text exceeds 16:1 in both environments.
- Focus ring is 2 px plus 2 px offset on Paper; 3 px high-contrast ring on Booth.
- Focus is never removed because a control also has hover styling.
- Host colour never carries speaker or selection meaning alone; name and state text accompany it.

## Keyboard navigation

- Logical order follows visual reading order in LTR/RTL.
- Skip link targets main programme/media content.
- Sheets and dialogs trap focus only while modal; closing restores the exact trigger.
- Escape closes popovers/sheets but does not end a live call without confirmation.
- Player shortcuts work only when focus is within the player or the user has opted into global shortcuts.
- Transcript uses line-level tab stops and roving word exploration.
- Cast and format selectors support arrow navigation and explicit selection announcements.

## Screen readers and live regions

- Page titles identify current episode and medium.
- Player controls include state and time; elapsed time is not announced every second.
- Call state changes use `aria-live="polite"`; microphone denied and connection lost use assertive only when immediate action is required.
- New After-show messages announce sender and text once. Typing indicators are not announced.
- Active transcript word is visual only; screen readers may query current sentence through a dedicated control rather than receiving constant updates.
- Weekly Proof comparison clips have date and context labels.

## Audio alternatives

- Produced episodes always have full transcripts.
- Host introductions and Weekly Proof have transcripts.
- Call-in has optional live captions and a stored transcript.
- Voice-note fallback exposes transcripts for both sides.
- Intake producer audio is mirrored in text; the user may respond by text each turn.
- Audio-only information is prohibited in consent, errors, and navigation.

## Large text and zoom

- Support browser zoom to 200% without loss, overlap, or horizontal page scrolling at 1280 CSS px equivalent.
- Support text-only scaling to 200% on mobile where the browser provides it.
- Multi-column layouts collapse; sticky/fixed regions become in-flow when they would obscure content.
- Controls grow in height and text wraps. Icon-only controls retain accessible labels and do not shrink.
- Episode titles may extend beyond the first viewport; Play remains reachable immediately after metadata.

## Touch and motor access

- Minimum 44×44 px hit areas, 48 px preferred.
- Scrubber has a large invisible hit area and keyboard alternatives.
- Swipe-to-dismiss is never the only way to close a sheet.
- Voice recording uses tap-to-start/tap-to-stop, not press-and-hold only.
- Destructive actions require deliberate activation but not complex gestures.

## Cognitive load and anxiety

- One primary action per region.
- No countdown during Call-in.
- Permission and consent explain consequences before the browser prompt.
- User can leave the call at any time.
- No red error styling for ordinary silence, pauses, or ending early.
- Generation and buffering use stable layouts rather than moving skeletons.
- Copy avoids performance judgement.

## Voice-only limitations

Call-in requires voice or asynchronous voice notes under the settled PRD. The entry surface must say this before permission. Users who cannot speak at that moment can pause the session, skip forward, or use voice notes if technically possible; the product must not claim a fully text-equivalent live call that does not exist.

## RTL accessibility

Accessible names follow semantic order, not visually mirrored DOM hacks. Focus order must be tested with Arabic/Hebrew screen readers. Mixed-direction titles must announce cleanly without reading isolation characters.

# Loading, generation, and failure states

## State-design principles

1. Preserve the authored object—the title, cast, and chosen idea—while work continues.
2. Say only what the system knows. Do not use fake percentages or deterministic time promises beyond settled budgets.
3. Keep completed media available when another part fails.
4. Recover silently when the user does not need to decide.
5. Expose one primary recovery action and state what was preserved.
6. Never surface planner, model, quality-gate, TTS, STT, or assessment terminology.

## Scenario specification

| Scenario | What the user sees | Available actions | Recovery behaviour |
|---|---|---|---|
| Pitch refresh under 800 ms | Existing programme frame, no message | None | Atomic replacement |
| Pitch refresh 0.8–5 s | “Preparing today’s programme” with typographic skeleton lines | Archive/Your show remain available | Full set replaces at once |
| Predicted episode prepared | Lead pitch marked “Ready now” | Play; Change | Starts under budget |
| Supporting pitch selected | Stable title plate, “Making the opening” | Leave; Change idea | Play activates on first chunk |
| Remix generation | Final edited title/cast shown; no old version flicker | Leave; Cancel before production begins | Restores programme if cancelled safely |
| First episode generation | Host intro remains playable; selected pitch visible | Leave; replay intro | First chunk enables Play |
| Partial audio ready | “Opening ready; the rest is arriving” and truthful buffer | Play; wait | Additional chunks append |
| Notes ready before audio | No unsolicited stage jump | Continue waiting; explicit Skip to Notes if user chooses | Normal cycle remains |
| Audio ready before definitions | Episode plays normally | Play | Definitions retry silently; missing word state only on tap |
| Quality retry | Same stable production state; no pipeline wording | Leave | One internal retry |
| Fallback episode | “That version did not come together. We made a simpler one from the same idea.” | Play; Change | Fallback still respects cast/topic where possible |
| World check failure | Normal interest/follow-up programme | Normal actions | Silent fallback; no alarming banner |
| Slow network | Inline status in affected media; loaded content stays | Retry connection; continue loaded content | Resume from stored point |
| Offline on Today | Slim offline banner; cached programme if valid | Open loaded/archived items | Refresh on reconnection |
| Offline during Episode | Cached/buffered playback and transcript remain | Play available media; retry | Resume stream at position |
| Audio synthesis failure | “Audio could not start. The transcript and notes are still here.” | Retry audio; Read notes | Keep session state |
| Live-call failure | “The live line dropped. Nothing was lost.” | Try live again; Voice notes | Preserve partial transcript |
| Microphone denied | Plain browser guidance | Try again; Voice notes | No repeated automatic prompt |
| Transcript sync failure | Complete transcript without word highlight | Retry timing; continue | Fall back to line-level timing |
| Session restoration | Resume band and exact stage context | Continue; Abandon | Restore stored state |
| Post-call reply delayed | “They’re writing back. You can leave.” | Leave; stay | Reply saved in thread on completion |
| Weekly Proof unavailable | Nothing appears | None | Silent omission |
| Audio clips deleted | Archive placeholder “Audio removed; transcript remains” | Open transcript | No broken player |

## Skeleton policy

Skeletons are permitted only for known text-line and player-shell geometry. They use static Paper-100/Booth-800 blocks with no shimmer under reduced motion and a very slow single luminance shift otherwise. A generated title is never replaced by a generic grey card once known.

## Offline rules

- Loaded transcript, Notes, Archive text, and buffered audio remain usable.
- New pitch generation, remix, live call, definitions not already cached, and new host creation are disabled with inline explanation.
- User text in intake/After-show is stored locally and queued only when idempotent; the interface states “Saved on this device” until uploaded.
- Consent changes and destructive actions require a confirmed server connection; the UI does not pretend success offline.

# Privacy and trust by design

## Memory presentation

Personal details are not decorated with memory icons or called out as “personalised.” They appear only when context makes them socially natural. The UI does not show why a pitch was generated or which data points drove it.

High-confidence memories may be stated. Uncertain memories are either omitted or phrased as a genuine question by the host. The interface itself never displays confidence values.

## Callback rules

**Do:**

- use facts the user directly volunteered;
- limit an episode to two personal references;
- keep references relevant to the topic;
- ask when a dated event may have changed;
- allow correction in one direct action.

**Do not:**

- mention inferred sensitive attributes;
- combine several details to demonstrate memory;
- use a private detail as clickbait;
- explain recommendation logic;
- turn dormant facts into surprise callbacks;
- imply surveillance of external activity beyond explicit world checks tied to interests.

## AI identity

AI disclosure appears at producer introduction, first host introduction, Voice tape/About, and wherever a user could reasonably mistake an interaction for a human live service. It does not need to prefix every host line.

Visual honesty rules:

- no photorealistic host images;
- no green “online” dot;
- no human biography presented as factual life experience;
- no claim that a host independently waited, missed, worried, or felt abandoned;
- voice and character can be warm, opinionated, and consistent.

## Recording and consent

- Explain before asking browser permission.
- State transcript storage separately from optional audio storage.
- No preselected consent.
- Equal visual weight for consent and decline.
- Current state visible before every Call-in and inside Voice tape.
- Revocation flips immediately and deletion status is honest about the 24-hour window.
- Archived players disappear only when deletion is confirmed; during processing they show Removal in progress and cannot be replayed if the policy requires immediate access removal.

## Correcting memory

A correction begins from the current plain-language statement. The user can type or speak the replacement. The confirmation echoes the new fact:

> **Updated:** You support Al Ahli now, not Al Ittihad.

No “Are you sure?” is required for ordinary corrections. Removing a fact from active use states that it will no longer appear in new shows; it does not claim physical deletion unless implemented.

## Flat weeks

The Weekly Proof uses the same calm Proof treatment for improvement and flat weeks. It names no fabricated win and one concrete adaptation. It never blames attendance, displays a red down arrow, or pressures the user to do more sessions.

## Parasocial safeguards

| Allowed authored warmth | Prohibited manipulation |
|---|---|
| Running jokes based on show history | “I missed you” after absence |
| Host remembers a position the user took | Guilt for ending early |
| Host disagrees and follows up next time | Claiming loneliness or need |
| Rare spoken milestone in context | Visual celebration or scarcity |
| “We’ll settle this next time” as ordinary dialogue | Countdown, notification, or promise designed to compel return |
| Transparent fictional character traits | Fake real-world personal life presented as truth |

## Destructive-action design

Safe choices appear first. Destructive labels name the result. There are no guilt colours, labyrinthine cancellation paths, or repeated confirmation. Voice revocation requires one confirmation because it deletes stored media; active-session abandonment requires one because it changes state. Ordinary memory correction does not.

# Screen-state matrix

The matrix is split into two tables for legibility while retaining the required state columns.

## Matrix A — default through offline

| Surface | Default | Loading | Empty | Partial | Error | Offline |
|---|---|---|---|---|---|---|
| Entry/account | Start statement or current field | Button-local provider state | Not applicable | Account created, verification pending | Inline field/provider error | Existing form remains; submission blocked clearly |
| Intake | Current producer turn + reply dock | Producer response/audio state | New intake starts at first turn | Sparse fields remain invisible; saved turns restored | Text fallback, Retry audio/response | Read saved turns; queue safe text reply locally |
| Today | Dated programme | Atomic refresh frame | Setup/resume or fallback pitch | One pitch may be ready while others are briefs | Fallback pitch + Retry full set | Cached programme and archive; no new generation |
| Production sheet | Topic/format/cast | Stable title plate, making opening | Blank “Bring your own idea” sheet | Opening playable, rest arriving | Retry or simpler version | Existing prepared episode only; edits disabled |
| Episode | Player + transcript | Metadata/player shell | Not applicable | Partial stream, transcript/definitions may differ in readiness | Keep transcript/Notes, Retry audio | Buffered/cached media only |
| Define | Meaning, part of speech, example | “Meaning is still arriving” only on tap | Not applicable | One field may be missing only if source safely permits; otherwise retry | Close + Retry | Cached meanings only |
| Notes | Editorial article | Known title/body line skeleton | Not applicable | Definitions delayed; article usable | Retry Notes or Go to call | Cached article works |
| Call-in | Entry or live state | Connecting | Not applicable | Partial transcript before recovery | Live line dropped; Voice notes | Cannot begin live; saved voice notes queue only if safe |
| After-show | Short open thread | “They’re writing back” | No reply yet within 30s window | User message stored, host reply pending | Retry outgoing; delayed reply preserved | Existing thread readable; queue text locally |
| Weekly Proof | Special audio item | Silent generation before delivery | Omitted | Audio ready before comparison detail | Omit or retry silently | Cached Proof only |
| Archive | Chronological index | Month-row skeleton | “Archive starts after first show” | Some archived audio removed, transcripts present | Retry failed record | Cached records only |
| Cast | Duo + active roster | Voice sample/creation state | No created hosts; duo remains | New host intro ready while metadata finalises | Preserve draft; Retry | View roster; creation/edit disabled |
| Trust | Show table of contents | Specific section loading | Knowledge summary may have no life facts yet | Audio removal in progress | Persistent consent/deletion error | View cached facts; changes disabled |

## Matrix B — paused through recovery

| Surface | Paused | Completed | Abandoned | Permission-related | Recovery action |
|---|---|---|---|---|---|
| Entry/account | Form draft retained | Account proceeds to intake | Not applicable | OAuth popup/browser issue | Retry, use email, or sign in |
| Intake | “Continue setting up your show” | Handoff begins | Not marked abandoned | Microphone denied affects voice replies only | Continue by text or retry mic |
| Today | Resume band above programme | Completed session absent from band | Old session moves to Archive as Ended early | Verification blocks session two only | Verify, Continue old session, or retry programme |
| Production sheet | Draft edits retained briefly | Episode opens | Cancelling before build returns to Today | Voice input unavailable; text remains | Retry, edit, or use simpler version |
| Episode | Exact audio position | Replay available in Archive | Partial episode replay where available | Autoplay blocked | Manual Play, Retry audio, Read Notes |
| Define | Dismisses on pause/navigation | Available in archived text | Available on existing text | Screen-reader word mode | Reopen on word, Retry meaning |
| Notes | Exact scroll position | Read-only in Archive | Existing article remains | Not applicable | Continue, Retry article, Go to call |
| Call-in | Returns with fresh opening | Recording/transcript archived per consent | Partial transcript retained | Mic denied | Retry live or Voice notes |
| After-show | Thread state retained | Composer closed; That’s the show | Existing turns retained | Not applicable | Retry message or leave note for next time |
| Weekly Proof | Audio position retained | Archived special | Not applicable | Audio output issue | Resume/Retry; text comparison remains |
| Archive | Not applicable | Complete label | Ended early label | Stored audio unavailable after revocation | Open available surfaces |
| Cast | Creation draft retained | Host active after intro | Retired host in Retired section | Mic unavailable; text interview works | Resume draft, change voice, bring back |
| Trust | Sheet state retained | Consent change confirmed | Not applicable | Server required for destructive change | Retry online; contact support on deletion failure |

# Design QA rules

A screen is rejected if any applicable critical rule fails. “Looks attractive” is not a substitute for passing these checks.

## Product identity gate

- [ ] Does the screen feel like media made for the user rather than educational software?
- [ ] Is the primary object a programme, episode, article, call, or conversation—not a dashboard metric?
- [ ] Is anything asking the user to manage difficulty, targets, sequencing, or assessment?
- [ ] Does the screen resemble a generic chatbot, streaming grid, task list, or course?
- [ ] Is there a large prompt box where an authored object should be?
- [ ] Would removing the logo make the screen indistinguishable from an AI template? If yes, reject.

## Authorship and hierarchy gate

- [ ] Is the primary action obvious within three seconds?
- [ ] Does the composition identify what is ready, what is selectable, and what is secondary?
- [ ] Are titles specific and content-bearing rather than generic marketing copy?
- [ ] Has a rounded card been used where whitespace and a rule would be stronger?
- [ ] Is every badge/status factually necessary?
- [ ] Does the first viewport contain enough real programme information, not decorative emptiness?

## Participation gate

- [ ] Does the episode clearly create a reason to read and call in?
- [ ] Does the Call-in feel like joining the show rather than activating tutor voice mode?
- [ ] Is the host’s stance visible without scripts or suggested answers?
- [ ] Can the user leave without shame or loss?
- [ ] Does After-show visibly end?

## Personalisation and trust gate

- [ ] Is every personal callback high-confidence, directly volunteered, relevant, and limited?
- [ ] Does the design avoid explaining or displaying prediction logic?
- [ ] Are hosts transparently AI where confusion is plausible?
- [ ] Does any visual imply a real human portrait, online status, or emotional dependence?
- [ ] Are recording and transcript states stated in text before Call-in?
- [ ] Can a remembered fact be corrected directly?
- [ ] Does any control claim export/deletion functionality not supported by v1?

## Language-learning-law gate

- [ ] Are level, CEFR, score, streak, test, practice, lesson, objective, and achievement absent?
- [ ] Is correction invisible in flow unless the user explicitly asks?
- [ ] Are word meanings lightweight and contextual rather than a vocabulary system?
- [ ] Is Weekly Proof an authored piece of media rather than analytics?
- [ ] Is the user free to choose topic, format, and cast while pedagogy remains absent?

## State and reliability gate

- [ ] Does every loading state preserve known content and avoid fake percentages?
- [ ] Does every error say what failed, what remains safe, and what to do?
- [ ] Can offline-loaded media still be used?
- [ ] Does live-call failure degrade to voice notes without session loss?
- [ ] Does pause restore the exact stage and meaningful position?
- [ ] Are abandoned sessions neutral rather than shameful?

## Responsive and accessibility gate

- [ ] Does the mobile version preserve the same hierarchy rather than merely stack everything?
- [ ] Are all targets at least 44 px and reachable above safe areas/browser chrome?
- [ ] Does 200% text produce no overlap, clipping, or hidden action?
- [ ] Does the design work with keyboard alone and visible focus?
- [ ] Are colour and host accent never the only state cue?
- [ ] Is RTL handled at component level, including mixed target/native text?
- [ ] Are audio states, transcripts, captions, and text alternatives complete?
- [ ] Is reduced motion meaningful rather than just slower animation?

## Completion gate

- [ ] Does the screen push another session, celebrate visually, or create obligation? If yes, reject.
- [ ] Does the completion feel socially and editorially finished?
- [ ] Does the final action return the user to ordinary life rather than keep them inside an engagement loop?

# Final recommended direction

## For one in one visual sentence

A warm private programme printed in type, turning into a charcoal radio booth when the user goes on air.

## Central organising idea

**Design every visit as today’s finite edition of a recurring personal show.** The programme arrives authored; the selected episode becomes one continuous media folio; the call-in is the climax; the interface ends when the show ends.

## Five most important decisions

1. **Daily programme instead of home dashboard:** one prepared lead pitch and a short ruled list of alternatives.
2. **Readiness instead of recommendation:** “Ready now” is factual and avoids exposing prediction or manipulation.
3. **Paper and Booth environments:** visual context changes with media mode rather than through a generic dark-mode setting.
4. **Type-led episode identity and non-human host marks:** scalable, honest, and distinct from AI portrait culture.
5. **No educational or engagement furniture at any point:** progress appears only through Weekly Proof; completion has no push.

## Five most dangerous mistakes

1. Turning Today into a grid of generated content cards.
2. Making the Call-in look like a tutor, voice assistant, or speaking assessment.
3. Using personal data as visible recommendation evidence or surprise intimacy.
4. Allowing chat to remain open and companion-like after the show should end.
5. Decorating the product with AI clichés—glows, gradients, portraits, or “magic”—instead of resolving hierarchy and media form.

## First screens to design, in order

1. **Today with three simultaneous variants:** ordinary day; active session; Weekly Proof day. This establishes the product category and hierarchy.
2. **Episode / produced player + synced transcript:** proves premium media quality and the Booth environment.
3. **Call-in in all live states and failure-to-voice-note recovery:** highest interaction and anxiety risk.
4. **Notes + Define:** proves editorial reading and invisible language support.
5. **After-show open, closing, final reply, and completed:** proves that conversation can end naturally.
6. **Pitch production sheet:** proves user control without prompt engineering.
7. **Intake and first-show handoff:** only after the core show feels desirable.
8. **Archive, Cast, and Trust:** apply the established system to secondary destinations.
9. **Entry/account:** last among major flows because it should inherit, not define, the product identity.

## Smallest high-fidelity prototype

Prototype one realistic cycle for one real user on mobile first, then validate the desktop Today composition.

### Sequence

1. Arrival on Today with one high-confidence callback, one “Ready now” lead pitch, and two supporting pitches.
2. Open lead pitch, change cast once, then return to the prepared version.
3. Play a fully produced 5–7 minute episode with at least 60–90 seconds of accurate word-synced transcript and working Define.
4. Move into a complete 250–450 word Notes article that genuinely changes the argument.
5. Join a live or Wizard-of-Oz Call-in where the host takes a position, pushes back, recasts once naturally, and responds within the perceived 1.5-second budget.
6. End the call and receive a three-to-five-message After-show thread that visibly closes.
7. Reach “That’s the show” without a next-session prompt.

### What must be real

- The episode title, script, audio, article, host stance, and personal callback must be specifically authored for the test user.
- Audio quality, mobile player controls, transcript readability, call entry, microphone permission, and chat ending must be high fidelity.
- The host must respond to the user’s actual position rather than follow a fixed branching script.
- The user must be able to leave and resume at least once.

### What may be simulated

- Nightly planning, full learner-file updates, assessment, quality gate, archive persistence, and generation pipeline.
- Word definitions beyond the tested sample.
- Call intelligence may be human-operated or LLM-assisted behind the scenes, provided the interface and latency are realistic.
- Weekly Proof may be represented as a separate high-fidelity screen rather than generated from longitudinal data in the first test.

### What to test

- Does the user understand that something was prepared without explanation?
- Do they choose a pitch because it sounds genuinely entertaining, not because they agreed to test?
- Does any screen feel like a lesson, tutor, or chatbot?
- Is the personal callback welcome, neutral, or invasive?
- Can they change topic/format/cast without wanting a prompt box?
- Do they naturally take a side after Episode and Notes?
- Does the Call-in create productive social pressure without assessment anxiety?
- Do they understand when the After-show is over?
- After the experience has ended and the researcher stops prompting, do they independently ask when the next episode will be available?

The pass condition remains behavioural: the user wants the next episode because this episode was worth hearing—not because the prototype explains the vision.
