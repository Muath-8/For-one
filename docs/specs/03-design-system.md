# 03 — Design System

**Status: NORMATIVE.** This document is the sole owner of design foundations: environments, tokens, typography, spacing, shape, motion, iconography, the component system (`DS-*`), the audio system's visual contracts, the responsive system, internationalisation foundations, accessibility standards, the state system, and the design QA gates.

**Derivation.** This document is the normative split of `docs/For_one_Design_System_and_UI_Specification.md` (adopted as canonical design authority by `00-decisions.md` §9.1, ADR-0016), together with the four deltas authorised in `00-decisions.md` §9.3. Every value here — hex, pixel, millisecond, string — is transcribed from that source unless it is marked as a §9.3 delta. No value in this document may be altered without an ADR.

**Companion document.** `02-ux-spec.md` owns screens (`SCR-##`), screen states (`SCR-##/S<n>`), the copy catalogue, the banned lexicon, and information architecture. This document names screens by ID and never restates screen logic; `02-ux-spec.md` names components by ID and never restates component anatomy.

**Precedence.** `00-decisions.md` → this document → `docs/For_one_Design_System_and_UI_Specification.md`.

**Normative language.** MUST / MUST NOT / MAY per RFC 2119.

---

# 1. Executive design direction

## 1.1 Design thesis

For one should feel like opening **today's edition of a private recurring programme**: a finite, authored set of possibilities has arrived; one of them is already produced; familiar hosts are waiting inside; and the user is expected to take part, not administer the system.

The interface is therefore organised around a **daily programme sheet** — not a dashboard, feed, catalogue, prompt box, or curriculum. The programme sheet has one lead item that is ready now and two to four supporting pitches. Selecting an item opens a continuous episode folio that moves through four familiar media forms:

**Episode → Notes → Call-in → After-show**

Those are the user-facing labels. Internally they map to Listen → Read → Speak → Chat, but the skill model MUST NOT appear in the interface.

## 1.2 For one in one visual sentence

> A warm independent publication that turns into a quiet radio booth when the show goes on air — typographic, intimate, precise, and unmistakably made for one person.

Restated at the level of environment: a warm private programme printed in type, turning into a charcoal radio booth when the user goes on air.

## 1.3 The central interface idea

Every design decision MUST preserve one idea: **the user is not searching for something to do; their show has arrived carrying something made for them.**

The main screen is a dated programme, not a content grid. The episode is a produced object, not generated output. The article is a piece of editorial material, not reading comprehension. The call-in is the climax of the show, not voice mode. The chat is an after-show thread with a visible ending, not an open companion.

## 1.4 Five defining design decisions

1. **One lead pitch is distinguished by readiness, not recommendation.** It is larger and marked "Ready now" because it is factually pre-produced. The interface MUST NOT say "best for you," explain the prediction, or expose personalisation logic.
2. **The product has two environmental surfaces.** "Paper" supports arrival, reading, archive, and trust. "Booth" supports produced audio and live voice. This creates media presence without a user-facing theme setting.
3. **Typography is the artwork.** Episode identity comes from deterministic title plates, host marks, date, cast, and format — not stock photography, generated portraits, or decorative AI imagery.
4. **The cycle has no educational stepper.** Each medium hands the user to the next: the episode throws to the notes; the notes arm the call; the call creates the after-show message.
5. **The interface ends.** After the final host reply, the composer closes and the page says only "That's the show." No next-session push, celebration, score, or obligation appears.

## 1.5 Product boundaries the design preserves

The design MUST NOT introduce, in any surface, wording, or language:

- levels, streaks, scores, progress dashboards, courses, tests, goals, badges, homework, or lesson terminology;
- a large prompt box on arrival;
- a generic streaming grid, social feed, or card wall;
- portraits that imply hosts are real people;
- a persistent chatbot or endless message composer;
- any explanation of targets, difficulty, CEFR, assessment, salience, energy, or planner logic;
- a notification centre, re-engagement surface, or "come back" pressure;
- a conventional settings dashboard.

The complete banned lexicon is owned by `02-ux-spec.md` Appendix B and is the single list the QA gates in §14 cite.

## 1.6 Source authority and the resolved data-rights gap

**This subsection supersedes the "Source authority and one explicit v1 trust gap" paragraph of the source design document (§9.3 delta 1).**

The source design document recorded a material tension: the Product Concept promised that users can see, export, and delete their data, while PRD v2.0 removed general export and account deletion from v1. That tension is resolved. Per `00-decisions.md` §1 (ADR-0001), **full data export and full account deletion are in v1**. The design therefore specifies both, in the legal and consent voice, on the Account essentials surface inside Your show. Deletion of stored call-in clips on consent revocation within 24 hours remains as designed.

Consequently:

- The source document's "Unsupported data actions" paragraph MUST NOT be applied.
- The source document's "Unsupported deletion copy" note MUST NOT be applied.
- The QA-gate line "Does any control claim export/deletion functionality not supported by v1?" is replaced by the line in §14.4 of this document.
- `02-ux-spec.md` owns the exact copy for both flows (SCR-25, SCR-26, SCR-27).

# 2. Design principles

Each principle is an acceptance criterion. A screen that violates one is rejected at the gate in §14.

| Principle | What it means | Interface requirement | Violation | For one example |
|---|---|---|---|---|
| **Arrive authored** | The product brings a made object rather than waiting for a prompt. | Render a complete dated programme; distinguish readiness; use specific titles. | Empty home state dominated by "What do you want to talk about?" | "Karim watched the derby and has one terrible idea about Saturday's lineup." |
| **Programme, not platform** | The daily set is finite, paced, and editorially arranged. | One lead item, a short supporting list, no endless scroll or recommendation rails. | A Netflix-style grid of episode covers. | Three pitches in week one, with one lead and two supporting lines. |
| **Participation is the climax** | Listening and reading exist to create a position the user wants to defend. | Make the unresolved throw and call-in the dramatic peak; show a real host stance. | Treating the call as an optional practice tool under the player. | "The article's in your notes. Read it, then get on the line." |
| **Personal, never forensic** | Memory should feel like continuity, not surveillance. | Use at most two high-confidence references; never show "why this was recommended." | Tags reading "Based on your location and recent activity." | A pitch naturally mentions the interview the user volunteered. |
| **Warmth with the labels on** | The show may be intimate while remaining explicit that hosts are AI. | Use crafted voices and recurring marks; disclose AI plainly; avoid human portraits and fake lives. | "Mara missed you" or a photorealistic host portrait. | "Mara and Sami are your AI hosts. They remember only what the show has stored." |
| **Complexity stays backstage** | The product makes hard decisions without asking the user to manage learning. | Hide targets, bands, assessment, model status, and generation stages. | Difficulty sliders, goals, or grammar target chips. | Topic, format, and cast are editable; difficulty is not. |
| **Finish without pressure** | Every session closes as a complete piece of media. | End chat, remove the composer, offer a quiet exit. | Confetti, "keep the streak," or auto-opening the next pitch. | "That's the show." |
| **Trust is an interaction, not a policy link** | Users can inspect and correct memory, control optional audio, take their data, and leave. | Put "What the show knows," "Voice tape," and Account essentials in an accessible show sheet with direct actions. | Burying consent inside legal text or a generic settings maze. | "That changed" opens a direct correction flow. |

# 3. Visual direction

## 3.1 Art-direction statement

For one combines the restraint of an independent cultural publication with the functional clarity of a radio control room. Paper surfaces are warm, matte, and typographic. Audio surfaces become charcoal and acoustically quiet. The visual energy comes from titles, spacing, live state, and voice — not gradients, illustration noise, or interface ornament.

The recognisable For one signature is the combination of:

- a dated daily programme;
- typographic episode plates;
- non-human host marks;
- the Paper-to-Booth environmental shift;
- a single warm broadcast signal colour;
- editorial rules and asymmetry instead of card grids.

## 3.2 Reference qualities and clichés to avoid

| Tradition | Borrow | Avoid |
|---|---|---|
| Independent editorial design | Strong hierarchy, generous but purposeful margins, confident type scale | Fashion-magazine illegibility and tiny grey type |
| Printed radio programmes | Finite schedule, numbering, dates, cast credits | Nostalgic imitation, paper textures, faux stamps |
| Liner notes | Credits, intimate details, typography as identity | Collectible-object clutter |
| Broadcast graphics | Clear live/ready states and disciplined information density | Breaking-news urgency and red overload |
| Film titles | Dramatic title composition and pacing | Cinematic spectacle that delays action |
| Studio equipment | Quiet functional controls and truthful status | Skeuomorphic knobs, meters, fake waveforms |

## 3.3 Composition system

### 3.3.1 Grid and width

| Breakpoint | Grid | Outer margin | Gap | Content maximum |
|---|---:|---:|---:|---:|
| Mobile, 320–599 | 4 columns | 20 px (16 px below 360) | 16 px | viewport |
| Tablet, 600–1023 | 8 columns | 32 px | 20 px | 920 px |
| Desktop, 1024–1439 | 12 columns | 48 px | 24 px | 1248 px |
| Wide, 1440+ | 12 columns | 64 px | 24 px | 1320 px |

- The programme MUST use a 7/5 split on desktop and a single column on mobile.
- The Episode player and transcript MUST use a centred 8-column region, maximum 840 px.
- Long-form Notes MUST use a 640–720 px text measure and MUST NOT use a full-width column.
- Supporting rails are permitted only for contextual metadata. They MUST NOT carry advertising, recommendations, or metrics.
- Full-bleed treatment is reserved for Booth surfaces and mobile call-in. Paper content MUST remain within the grid.

### 3.3.2 Spacing rhythm

The base unit is 4 px. The production scale is 4, 8, 12, 16, 24, 32, 48, 64, 96, and 128 px. Components MAY use 20 or 40 only where optical alignment requires it. Arbitrary spacing values are prohibited.

### 3.3.3 Density

| Surface family | Density rule |
|---|---|
| Today | Medium density. The first viewport MUST contain the whole lead item and at least two supporting titles on a standard laptop. |
| Episode | Low visual density around transport; higher density in transcript. |
| Notes | Editorial density, 19 px text with 31 px line height. |
| Archive | High but calm density; chronological rows, not cards. |
| Trust and Cast | Compact, explicit, and text-led. |

### 3.3.4 Asymmetry

Asymmetry signals editorial authorship, not randomness. The lead pitch MAY span seven columns while supporting pitches stack in five. Episode plates MAY offset cast credits. Controls, form fields, and legal consent MUST remain aligned and predictable.

## 3.4 Shape language

| Element | Rule |
|---|---|
| Ordinary content | No enclosing card. Use whitespace and horizontal rules. |
| Interactive list rows | Flat surface with 1 px divider; hover MAY tint the row. |
| Primary buttons | 8 px radius; never pill-shaped unless the control is a compact toggle. |
| Inputs | 6 px radius, visible border, no floating label. |
| Sheets and dialogs | 16 px radius on desktop; top corners 16 px on mobile bottom sheets. |
| Definition popover | 8 px radius, 1 px border, restrained shadow. |
| Compact player | 12 px radius because it floats above content. |
| Host marks | 4 px radius, or circular only when the mark's geometry requires it. |
| Episode plate | Usually no border and no container; composition itself defines the object. |

Shadows are used only for overlays, popovers, and the compact player. Active media MUST differ through environment, scale, and state — not elevation.

## 3.5 Image and illustration policy

V1 uses **no photography, no photorealistic host portraits, and no free-form generated episode imagery**.

Episode identity is produced by a deterministic title-plate system using:

- title;
- date and issue number;
- format;
- one or two host marks;
- one accent rule or field;
- optional typographic crop or repeated title fragment.

This system scales to every language, avoids inconsistent generated artwork, and makes the show feel produced rather than decorated.

Hosts have visual identities without faces. Each host receives a stable mark made from a monogram or abstract letterform, one accent colour, and a typographic nameplate. The mark MUST NOT suggest a body, age, ethnicity, or photographic reality. Voice samples and writing establish character; the interface MUST NOT fabricate a human appearance.

Illustration is reserved for rare functional diagrams in help or permission education. None is required in the core v1 experience.

## 3.6 Iconography

- Use a curated 1.75 px outline family with square optical construction and restrained rounded joins.
- Standard optical sizes are 16, 20, and 24 px. The live-call primary control MAY use 28 px.
- Filled icons are reserved for active Play, Pause, Mute, and selected microphone states.
- Navigation icons MUST carry text labels on desktop and accessible names on mobile. Archive and Your show MUST NOT be represented by ambiguous decorative symbols alone.
- The 10-seconds-back icon remains counter-clockwise in both LTR and RTL.
- Sparkles, magic wands, brains, robots, orbit icons, and decorative microphone patterns are prohibited.

# 4. Environment strategy

V1 launches with a **context-driven editorial theme**, not a light/dark mode selector.

| Environment | Applies to | Character |
|---|---|---|
| **Paper** | Entry, onboarding, Today, Notes, After-show, Archive, Cast, Trust, Account essentials | Warm, matte, typographic |
| **Booth** | Episode playback and Call-in | Charcoal, acoustically quiet, low ornament |
| **Proof** | Weekly Proof | Quiet blue-grey field within Paper |

The user MUST NOT be given a control to configure these environments; they are part of the show's media grammar. The Paper base is warm enough for evening use without becoming low-contrast. Browser and operating-system high-contrast modes MUST remain supported.

Environment is expressed as a `data-environment` attribute on the surface root, which reassigns semantic tokens (§5.9). Components MUST read semantic tokens and MUST NOT hard-code primitives.

# 5. Design tokens

## 5.1 Colour primitives

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

Measured contrast: primary text on Paper exceeds 16:1; muted text remains above 5.4:1. Broadcast, Petrol, Proof, Success, Warning, and Error foregrounds all exceed 5.5:1 on Paper. Booth text exceeds 16:1 and the Booth broadcast accent exceeds 5.5:1.

## 5.2 Semantic colour tokens

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

Brand colour is not a background default. It identifies live, ready, or decisive moments and MUST occupy less than 10% of an ordinary Paper screen.

The Proof environment uses `proof-100` as `color.bg.canvas` and `proof-700` as its accent, with Paper text tokens unchanged.

## 5.3 Host accents

A host receives one stable accent from a controlled palette. Accents MAY colour a 3 px rule, host mark, speaker label, or selected cast chip. They MUST NOT colour long text unless the pairing passes contrast.

| Accent | Value |
|---|---|
| Ochre | `#8D5D16` |
| Teal | `#2F6662` |
| Plum | `#744C63` |
| Slate blue | `#3F5F7A` |
| Rust | `#914735` |
| Olive | `#5E6531` |

Host accent is identity, not hierarchy (§6.1 rule 5) and never the only carrier of speaker or selection meaning (§12.2).

## 5.4 Typography

### 5.4.1 Typeface strategy

| Role | Family |
|---|---|
| Latin display and editorial | Source Serif 4 |
| Latin interface, transcript, controls | Inter |
| Arabic editorial | Noto Naskh Arabic |
| Arabic interface and transcript | Noto Sans Arabic |
| Other scripts | Vetted Noto Serif/Sans pair where quality permits; otherwise Noto Sans in both roles rather than forcing a weak serif |
| Monospace | Noto Sans Mono, restricted to timecodes, token examples, and technical documentation |

All families are open-source and practical to ship. The application MUST load only the scripts required by the selected native and target languages.

### 5.4.2 Type scale

| Role | Desktop | Mobile | Weight | Notes |
|---|---|---|---|---|
| Programme display | 56/58 px | 40/43 px | 500 serif | Lead pitch; maximum 5 lines on mobile |
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

### 5.4.3 Typography rules

- Large Latin titles MAY use `letter-spacing: -0.02em`. Arabic and other connected scripts use zero tracking.
- Interface text uses sentence case. All caps is limited to short Latin date and status kickers; localisations MAY use weight instead of case.
- Reading measure is 62–68 characters by default, hard range 55–72.
- Paragraph spacing equals 0.75 line height. UI articles MUST NOT use a first-line indent.
- Italics MAY mark publication titles or quoted emphasis in Latin. Italics MUST NOT be synthesised for scripts without a native italic.
- Playback time and issue numbers MUST use tabular numerals.
- Episode titles MUST NOT be truncated on detail surfaces. Supporting pitches MAY clamp at three lines on desktop and four lines on mobile, with the full title exposed to assistive technology.
- Mixed-direction names and titles MUST be wrapped in component-level `dir="auto"` spans.

## 5.5 Spacing, sizing, and shape tokens

| Category | Tokens |
|---|---|
| Spacing | `space-1:4`, `space-2:8`, `space-3:12`, `space-4:16`, `space-6:24`, `space-8:32`, `space-12:48`, `space-16:64`, `space-24:96`, `space-32:128` px |
| Radius | `radius-0:0`, `radius-1:4`, `radius-2:6`, `radius-3:8`, `radius-4:12`, `radius-5:16`, `radius-round:999` px |
| Border | `border-hairline:1px`, `border-strong:2px`, `border-live:3px` |
| Control height | `control-sm:36`, `control-md:44`, `control-lg:52`, `control-call:64` px |
| Touch target | 44 px minimum; 48 px preferred on mobile |
| Icon | 16, 20, 24, 28 px |
| Audio scrubber | 4 px track, 20 px thumb, 44 px interaction hit area |
| Transcript measure | 760 px max |
| Article measure | 680 px default, 720 px max |
| Programme width | 1320 px max |

## 5.6 Shadows and layers

| Token | Value | Use |
|---|---|---|
| `shadow-popover` | `0 8px 28px rgba(23,23,22,.16)` | Definition popover |
| `shadow-sheet` | `0 16px 48px rgba(23,23,22,.22)` | Desktop show sheet and dialog |
| `shadow-player` | `0 6px 24px rgba(23,23,22,.18)` | Compact persistent player |
| `z-base` | 0 | Page |
| `z-sticky` | 20 | Masthead and compact player |
| `z-popover` | 40 | Definitions and selectors |
| `z-sheet` | 60 | Your show, production sheet |
| `z-dialog` | 80 | Confirmation and permission |
| `z-toast` | 100 | Rare transient system notice |

Toasts MUST NOT carry critical actions or consent. Critical states remain in the page.

## 5.7 Motion tokens

| Token | Duration | Easing | Use |
|---|---:|---|---|
| `motion-instant` | 80 ms | linear | State colour and word highlight |
| `motion-fast` | 140 ms | cubic-bezier(.2,.0,.2,1) | Hover, focus, compact controls |
| `motion-standard` | 220 ms | cubic-bezier(.2,.0,0,1) | Sheets, pitch selection |
| `motion-emphasis` | 320 ms | cubic-bezier(.16,1,.3,1) | Player expansion, environment change |
| `motion-stage` | 420 ms max | cubic-bezier(.16,1,.3,1) | Paper ↔ Booth transition |

Spring motion is allowed only for bottom-sheet settling and compact-player expansion, with no visible bounce. Reduced-motion mode removes translation and uses an 80 ms crossfade or an immediate state change.

## 5.8 Breakpoint tokens

```css
--bp-mobile: 0px;
--bp-tablet: 600px;
--bp-desktop: 1024px;
--bp-wide: 1440px;
--content-programme: 1320px;
--content-media: 840px;
--content-reading: 680px;
```

## 5.9 Token hierarchy example

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

## 5.10 Token governance

- Three tiers only: primitive → semantic → component. Components MUST consume semantic or component tokens and MUST NOT reference primitives directly.
- A new primitive requires an ADR. A new component token requires a named component in §6.
- Tailwind theme values are generated from this table set; a value present in Tailwind but absent here is a defect.

# 6. Component system

## 6.1 Component rules

1. A component MUST correspond to a real recurring behaviour, not merely a visual treatment.
2. Flat composition is the default. A container is added only when it groups controls, floats above content, changes environment, or represents a discrete state.
3. Every component MUST support text expansion, `dir="auto"`, keyboard focus, and 200% text zoom.
4. Status MUST be communicated by text plus colour or icon. Colour alone is never sufficient.
5. Host accent is identity, not hierarchy. The current action remains dominant regardless of host colour.
6. Components MUST NOT expose internal AI, pedagogy, or pipeline terminology. The banned lexicon in `02-ux-spec.md` Appendix B is binding on every component label, placeholder, tooltip, and accessible name.
7. Every component declares its environment support (Paper, Booth, Proof). A component used in Booth MUST be verified against Booth focus and contrast tokens.

## 6.2 Component index

| ID | Family | Purpose | Primary screens |
|---|---|---|---|
| `DS-Masthead` | Shell | Persistent Paper navigation | SCR-06, SCR-16, SCR-17, SCR-19 |
| `DS-ContextHeader` | Shell | Contracted header inside a session folio | SCR-09, SCR-11, SCR-12, SCR-14, SCR-18 |
| `DS-Sheet` | Shell | Base modal sheet container | SCR-07, SCR-08, SCR-21 |
| `DS-YourShowSheet` | Shell | Trust and account table of contents | SCR-21 |
| `DS-ProductionSheet` | Shell | Topic, format, and cast editing surface | SCR-07, SCR-08 |
| `DS-OverflowMenu` | Shell | Secondary actions behind one control | SCR-06, SCR-09, SCR-11, SCR-12 |
| `DS-ActiveSessionBand` | Shell | Resume an unfinished session | SCR-06 |
| `DS-ProgrammePitch` | Programme | One selectable authored idea | SCR-05, SCR-06 |
| `DS-EpisodePlate` | Programme | Deterministic typographic episode identity | SCR-05, SCR-06, SCR-07, SCR-09, SCR-16, SCR-18 |
| `DS-HostMark` | Programme | Non-human host identity | Every host-bearing surface |
| `DS-CastPairing` | Programme | Two host marks joined by a connector | SCR-05, SCR-06, SCR-09, SCR-19 |
| `DS-WeeklyProofItem` | Programme | Weekly Proof as a special broadcast | SCR-06, SCR-16, SCR-17 |
| `DS-ProofComparison` | Programme | The "On tape" clip or quote pair | SCR-16 |
| `DS-FullPlayer` | Audio | Produced-audio transport | SCR-05, SCR-09, SCR-16, SCR-18 |
| `DS-CompactPlayer` | Audio | Floating persistent transport | SCR-06, SCR-11, SCR-17, SCR-21 |
| `DS-Scrubber` | Audio | Timeline control | `DS-FullPlayer` |
| `DS-AudioStatus` | Audio | Truthful inline audio state | `DS-FullPlayer`, `DS-CompactPlayer` |
| `DS-TranscriptLine` | Audio | One synced utterance | SCR-09, SCR-16, SCR-18 |
| `DS-ArticleHeader` | Reading | Editorial article identity | SCR-11, SCR-18 |
| `DS-DefineTrigger` | Reading | Every word is definable | SCR-09, SCR-11, SCR-18 |
| `DS-DefinePopover` | Reading | Word-in-context meaning | SCR-10 |
| `DS-CallInStage` | Voice | Live call surface | SCR-12 |
| `DS-VoiceNote` | Voice | Asynchronous turn-based audio | SCR-13 |
| `DS-MicPermissionPanel` | Voice | Permission education and fallback | SCR-12, SCR-13 |
| `DS-AfterShowThread` | Messaging | Short closing text exchange | SCR-14, SCR-18 |
| `DS-Composer` | Messaging | Reply field with a lifecycle | SCR-14 |
| `DS-IntakeTurn` | Messaging | One producer or user interview turn | SCR-04, SCR-20 |
| `DS-ReplyDock` | Messaging | Type or record reply control | SCR-04, SCR-20 |
| `DS-PrimaryButton` | Control | The one primary action in a region | All |
| `DS-SecondaryButton` | Control | Alternative bounded action | All |
| `DS-TextAction` | Control | Quiet inline action | All |
| `DS-TextField` | Control | Labelled text input | SCR-02, SCR-07, SCR-08, SCR-14, SCR-22, SCR-27 |
| `DS-LanguageSelector` | Control | Searchable single-selection language list | SCR-02 |
| `DS-SegmentedChoice` | Control | Up to three exclusive choices | SCR-04 |
| `DS-FormatSelector` | Control | Editorial format list plus free text | SCR-07, SCR-08 |
| `DS-CastSelector` | Control | One or two hosts | SCR-07, SCR-08 |
| `DS-VoiceSample` | Control | Playable dialect or voice option row | SCR-04, SCR-20 |
| `DS-ConsentChoice` | Trust | Two equally legible consent options | SCR-04, SCR-23 |
| `DS-ConsentHistory` | Trust | Ordered append-only consent event list | SCR-23 |
| `DS-ConfirmationDialog` | Trust | Named consequence before a state change | SCR-06, SCR-12, SCR-19, SCR-23, SCR-27 |
| `DS-InlineCorrection` | Trust | Correct one remembered fact | SCR-22 |
| `DS-KnowledgeStatement` | Trust | One plain-language remembered fact | SCR-22 |
| `DS-DisclosureLine` | Trust | AI identity and recording status | SCR-01, SCR-04, SCR-12, SCR-24 |
| `DS-CastRow` | Trust | One host in the roster | SCR-19 |
| `DS-ArchiveRow` | Trust | One chronological record | SCR-17 |
| `DS-SystemBanner` | State | Persistent page-level notice | SCR-06, SCR-11, SCR-17, SCR-21, SCR-25 |
| `DS-RequestStatus` | State | Honest state of an asynchronous request | SCR-23, SCR-25, SCR-26 |
| `DS-GenerationState` | State | Authored object while media is produced | SCR-05, SCR-07, SCR-08 |
| `DS-Skeleton` | State | Known-geometry placeholder | SCR-06, SCR-11, SCR-17, SCR-23 |
| `DS-EmptyState` | State | What will appear and after what action | SCR-17, SCR-19, SCR-22, SCR-23 |
| `DS-ErrorState` | State | What failed, what is safe, one recovery | All |
| `DS-Toast` | State | Rare transient non-critical notice | Limited |

## 6.3 Navigation and shell components

### DS-Masthead

**Purpose.** Persistent, restrained navigation on Paper surfaces.

**Anatomy.** For one wordmark (returns to Today); Today; Archive; Your show; optional verification-notice slot below the bar.

**Variants.** `desktop-text` (labelled text navigation), `mobile-compact` (wordmark or back control at the inline start, Archive control, Your show control).

**States.** Default; scrolled; notice present; hidden (mobile reading scroll only).

**Behaviour.**
- The masthead MUST NOT persist inside an active Call-in.
- In Episode and Notes it collapses to `DS-ContextHeader`.
- On mobile the bar hides on downward reading scroll at a 12 px threshold and returns on an 8 px reverse scroll. It MUST NOT hide while playback is paused, permission is needed, or an error is present. Time-based hiding is prohibited.
- Mobile height is 56 px plus safe area.

**Responsive.** Desktop uses text navigation. Mobile uses compact controls with 44 px targets and labels carried in accessible names.

**Accessibility.** The current destination carries `aria-current`. Icon-only mobile controls retain accessible names. There is no bottom navigation bar; a bottom bar is rejected because it would overstate the information architecture, compete with the compact player and call controls, and make the product feel like a generic app shell.

**Misuse.** MUST NOT gain Learn, Progress, Explore, notifications, or a search field. MUST NOT display counts or unread markers.

### DS-ContextHeader

**Purpose.** Let the episode become the environment while keeping escape and identity available.

**Anatomy.** Back; episode title; optional stage action; overflow (`DS-OverflowMenu`).

**Variants.** `paper`, `booth`, `sticky`, `collapsed`.

**States.** Default; scrolled and collapsed; stage action present; overflow open.

**Accessibility.** The title MAY visually clamp; the full name MUST remain in the accessible label. Back MUST follow browser history safely.

**Misuse.** MUST NOT become a four-step lesson header, MUST NOT show stage numbers, and MUST NOT show completion state.

### DS-Sheet

**Purpose.** The single modal container primitive behind Your show and the production sheet.

**Anatomy.** Optional drag handle (mobile); title; body; optional sticky action region.

**Variants.** `desktop-right` (16 px radius, `shadow-sheet`), `mobile-bottom` (top corners 16 px), `mobile-full` (full height).

**States.** Entering, open, scrolled, exiting.

**Behaviour.** Layer `z-sheet`. Entry uses `motion-standard`; a critically damped spring MAY be used for bottom-sheet settling, with no visible bounce.

**Accessibility.** Focus trap while modal; Escape closes; initial focus lands on the sheet title; closing restores focus to the exact trigger. Swipe-to-dismiss MUST NOT be the only way to close.

**Misuse.** MUST NOT stack more than one sheet. A dialog opened from a sheet uses `z-dialog` and returns focus to the sheet.

### DS-YourShowSheet

**Purpose.** A table of contents for the show's memory, voice, identity, and account — not a settings dashboard.

**Anatomy.** Sheet title; exactly five top-level editorial rows in this order: Cast; What the show knows; Voice tape; About this AI show; Account essentials. Sign out is a quiet action below the rows.

**Variants.** Desktop right sheet 480–560 px; mobile full-height sheet showing one section at a time.

**States.** Index; section open; section loading; section error; signing out; account-deletion handoff.

**Accessibility.** Focus trap, Escape close, initial focus on the title, focus restored to the trigger. Each row is a single link carrying a complete accessible name.

**Misuse.** MUST NOT display a "Settings" heading, notification controls, appearance controls, difficulty controls, or any control unrelated to cast, memory, voice, identity, or account.

### DS-ProductionSheet

**Purpose.** Give ownership of topic, format, and cast without asking the user to write a production prompt.

**Anatomy.** Pitch title as the heading; three editable rows (Topic → `DS-TextField`; Format → `DS-FormatSelector`; Cast → `DS-CastSelector`); primary action; secondary actions Close, Start over, Bring your own idea.

**Variants.** `desktop-right-5col` (the programme remains visible behind it), `tablet-80pct`, `mobile-fullscreen` with a sticky bottom action.

**States.** Default; row editing; changed (the primary action label changes); generating (`DS-GenerationState`); ready; topic-refused with the edited values retained and an inline `DS-ErrorState`; offline with edits disabled; blocked by active-session conflict; session-cap/verification admission overlay; retired-cast refresh with the editable values retained; cost-refused before pitch creation; cost-refused after pitch creation with the saved active pitch retained; persistent terminal support through `DS-GenerationState`.

**Misuse.** MUST NOT contain advanced settings, tone sliders, target vocabulary, difficulty, temperature, model choice, episode-length control, or any client generation-retry/fallback action. A topic-refused state MUST NOT clear or replace the user's topic.

### DS-OverflowMenu

**Purpose.** Hold secondary actions without adding visual weight beside the primary action.

**Anatomy.** One 44 px trigger with an accessible name; a popover list of labelled actions.

**Variants.** `context-header`, `active-session-band` (Abandon and the 48-hour note, FR-206), `player-speed` (0.8×, 1.0×), `call-in` (elapsed time for accessibility and support).

**States.** Closed, open, item focused, destructive item present.

**Accessibility.** Layer `z-popover`. Arrow-key navigation; Escape closes and restores trigger focus. A destructive item MUST name the action and MUST NOT be the first item.

**Misuse.** MUST NOT hide the only path to a primary or safety-critical action.

### DS-ActiveSessionBand

**Purpose.** Return the user to an unfinished session before anything new is offered.

**Anatomy.** Episode title; natural-language position; Continue; overflow containing Abandon.

**Variants.** `listening`, `notes`, `call-in`, `after-show`, `nearing-48h`.

**States.** Default; announced on load; overflow open; conflict confirmation open.

**Behaviour.**
- A full-width flat band above every other item on Today.
- Position MUST be natural language. During Episode the factual time position MAY be shown. During Notes the copy says "midway" only when the stored scroll position is beyond 35%, otherwise "near the beginning." A Call-in band exists only for a durably degraded voice-note exchange and uses COPY-073 to state that the same exchange continues where it stopped; ordinary live speaking is not pausable and the band MUST NOT imply a fresh room.
- The 48-hour expiry note (FR-206) appears only inside the overflow.

**Accessibility.** Screen readers announce the band once when Today opens. Continue is the first tab stop after the masthead.

**Misuse.** MUST NOT show a percentage, a four-step progress indicator, a celebratory icon, or an urgency countdown.

## 6.4 Programme and episode components

### DS-ProgrammePitch

**Purpose.** Make a one-line idea feel written and selectable rather than generated and configurable.

**Anatomy.** Issue number; title (hard cap 140 characters, owned by FR-101); cast pair; format; factual readiness status when applicable; primary action; optional overflow for remix.

**Variants.**
- **Lead prepared:** large serif title, "Ready now," prominent Play action.
- **Supporting:** smaller title row, no readiness claim, opens the production sheet.
- **Selected:** the title holds position while the production sheet opens. There is no bright selected card.
- **Lead unprepared:** a complete programme pitch without a readiness label after predicted pre-generation failed; selection follows SCR-06/S1's ordinary on-selection path and exposes no Retry.
- **First-show pitch:** one isolated cue-sheet composition with Accept and one "Another idea" action.

**States.** Default, hover, keyboard focus, pressed, generating, ready, unprepared lead, and load error. Selection remains enabled while another session is active and opens SCR-06/S9's confirmation; the component owns no disabled conflict state.

**Content limits.** Title 140 characters (FR-101); format label 28 characters (FR-101); one or two host names; no reason-for-recommendation text.

**Responsive.** Lead occupies seven columns on desktop and full width on mobile. Supporting rows use 20 px titles and 24 px vertical padding, clamp at three lines on desktop and four on mobile, and MUST NOT become swipeable carousels.

**Accessibility.** The full title is the accessible name; metadata follows in the label. Readiness is text. Each row is a link or button with a single primary target and MUST NOT nest click traps.

**Misuse.** MUST NOT carry a thumbnail, confidence score, "recommended" label, topic tag, learning target, wait estimate before selection, or more than one badge.

### DS-EpisodePlate

**Purpose.** A deterministic typographic identity for an episode, produced without imagery.

**Anatomy.** Title; issue date; cast marks; format; optional single accent field or rule; optional typographic crop or repeated title fragment.

**Variants.** `programme-lead`, `full-episode`, `compact-archive`, `weekly-proof`.

**States.** Static; expanding into Booth (`motion-emphasis`); generating (paired with `DS-GenerationState`).

**Behaviour.** Long titles recompose rather than truncate: the plate reduces display size one step after 70 characters and permits up to five lines on mobile. The plate normally carries no border and no container. The accent rule MAY mirror as part of the composition template in RTL.

**Misuse.** MUST NOT use generated imagery, photography, or a fake cover-art square.

### DS-HostMark

**Purpose.** Give a host a stable visual identity without a face.

**Anatomy.** Abstract mark built from a monogram or letterform; host name; one accent from §5.3; optional descriptive voice label.

**Variants.** `mark-only`, `mark-with-name`, `nameplate` (typographic, used on plates).

**States.** Default, speaking, listening, selected for cast, retired, unavailable voice.

**Behaviour.** Speaking MAY strengthen the accent rule or fill the mark using real audio state. Continuous decorative pulsing is prohibited. Radius is 4 px, or circular only where the mark's geometry requires it. Internal artwork MUST NOT mirror in RTL; the mark repositions with the layout.

**Content.** Host names MUST support 30 characters and mixed scripts and MUST NOT truncate on primary surfaces. The voice label is descriptive and neutral ("warm, low energy"; "bright, fast") and MUST NOT assert demographic fiction.

**Misuse.** MUST NOT imply a body, age, ethnicity, or photographic reality. MUST NOT carry an online dot.

### DS-CastPairing

**Purpose.** Present two hosts as a duo without implying a photograph.

**Anatomy.** Two `DS-HostMark` instances, aligned or overlapping, joined by an explicit localised connector.

**Variants.** `aligned`, `overlapped`, `metadata-inline` (names only, inside a pitch metadata line).

**States.** Default, one host speaking, one host selected, one host retired.

**Behaviour.** Marks MUST NOT be blended. The connector is a real localised word, not a glyph that assumes English.

**Misuse.** MUST NOT imply a relationship the audio has not established.

### DS-WeeklyProofItem

**Purpose.** Present the Weekly Proof as an editorial special rather than a metric panel.

**Anatomy.** Proof surface field; "Weekly Proof" kicker; title; two-minute duration; cast; Play; a "tape splice" typographic rule.

**Variants.** `today-placement` (full-width `proof-100` field above the programme), `archive-row` (Proof accent inside `DS-ArchiveRow`).

**States.** Available; playing; played with the comparison section revealed; flat-week; absent.

**Behaviour.** It MUST NOT preview wins as metrics before playback. After listening it MAY reveal the clips or quotes included in the piece through `DS-ProofComparison`. The flat-week variant uses the same calm treatment and MUST NOT turn warning-red or apologise. It differs from an ordinary episode through colour, compact duration, and the splice rule only.

**Misuse.** MUST NOT carry a chart, badge, trophy, percentage, aggregate score, or red downward arrow.

### DS-ProofComparison

**Purpose.** Show the concrete "On tape" evidence behind the Proof under the user's current consent.

**Anatomy.** Two dated items; each item is a short clip player (voice consent on) or a verbatim text excerpt (voice consent off); a maximum of three editorial annotations.

**Variants.** `clips`, `quotes`.

**States.** Hidden before playback; available; one clip removed after revocation; loading.

**Accessibility.** Every clip and quote MUST carry a date and a context label.

**Misuse.** MUST NOT display an aggregate score, a delta percentage, or a goal card. The next focus appears as one host-spoken line and one transcript line only.

## 6.5 Audio and transcript components

### DS-FullPlayer

**Purpose.** Deliver produced audio as premium media with truthful state.

**Anatomy.** Title context; large Play/Pause; 10 seconds back; `DS-Scrubber`; elapsed and total time; speed menu limited to 0.8× and 1.0× inside `DS-OverflowMenu`; buffering state; output and permission messages only when relevant.

**States.** Idle, loading metadata, playable partial stream, playing, paused, scrubbing, buffering, source replaced, ended, synthesis error, offline-cached.

**Rules.**
- The scrubber MUST show the known total duration. During partial streaming the available range MUST be visually distinguished from the total and MUST remain truthful.
- Seeking beyond the buffered range requests the segment and shows local buffering. It MUST NOT fake availability.
- Speed selection is a small text control and MUST NOT be presented as a learning tool. No speed above 1.0× exists.
- The primary control is 52 px on desktop and 56 px on mobile, with a 48 px minimum target.
- There is no forward-skip control.
- Metadata loading shows the player shell with the title and MUST NOT show a fake duration.
- Audio blocked by the browser shows a manual Play; automatic retry of autoplay is prohibited.
- A higher EP-53 `manifestEpoch` is a material source replacement, not an appended segment. The player lets only the currently buffered lower-epoch segment reach its clean boundary, stops, deletes every lower-epoch URL and timing/position value from memory and persistence, resets to 0:00, and requires an explicit Play on the validated higher epoch. It MUST NOT merge epochs, autoplay the replacement, resume the old position, or seek through a superseded manifest.

**Responsive.** At 200% text, controls wrap into two rows without covering the timeline.

**Accessibility.** Transport carries visible labels or tooltips. Keyboard shortcuts MUST NOT override text input and work only when focus is within the player or the user has opted into global shortcuts. Elapsed time is not announced every second.

**Misuse.** MUST NOT display a waveform grade, pronunciation score, comprehension question, vocabulary sidebar, or "complete listening" action.

### DS-CompactPlayer

**Purpose.** Let produced audio survive navigation between Paper surfaces.

**Anatomy.** Host mark; title; play/pause; elapsed time; expand; close.

**States.** Playing, paused, buffering, error.

**Behaviour.**
- Appears only after audio has actually started. Bottom sticky at `z-sticky`, 12 px radius, `shadow-player`, height `--compact-player-height` 4.5rem, with bottom safe-area padding.
- Persists across Today, Notes, Archive, Cast, and Trust. It MUST NOT persist across sign-out.
- MUST NOT appear during a live call and MUST NOT hide a blocking error.
- On Notes it defaults to paused after a stage transition and remains expandable.
- During form entry or After-show composition it moves above the keyboard while playing; while paused it MAY collapse to a 44 px title strip.
- Expansion to `DS-FullPlayer` uses a shared title and control transform over 280–340 ms, critically damped spring permitted.
- It MUST NOT overlap the composer or a system permission banner.

**Accessibility.** Controls are 44 px minimum. Media Session API metadata carries episode title, show name, and the deterministic plate where supported.

### DS-Scrubber

**Purpose.** Truthful position control.

**Anatomy.** 4 px visual track; 20 px thumb increasing to 24 px while dragging; 44 px hit area; buffered range shown distinctly from total duration.

**States.** Idle, hover, focus, dragging, buffering, disabled when no duration is known.

**Keyboard.** Left and Right move 5 seconds; Shift+Left and Shift+Right move 10 seconds; Home and End move to the bounds. Physical Left decreases time and Right increases time in both directions. Time announcements occur on command, not every second.

**RTL.** The Play triangle and the time direction MUST NOT mirror. The 10-seconds-back icon remains counter-clockwise.

**Misuse.** MUST NOT show a fake buffered range or present an estimated duration as known.

### DS-AudioStatus

**Purpose.** State the real audio condition in words.

**Anatomy.** One short text line with an optional icon, inline beside the transport.

**Variants.** `partial-ready`, `buffering`, `failed`, `local-playback`, `other-tab`, `interrupted`, `output-changed`, `timing-unavailable`.

**Timing rules.** Buffering under 500 ms shows control state only, with no copy. Between 500 ms and 5 s it shows "Buffering" beside the time. Above 5 s it shows an explanatory inline state and a Retry connection action while the transcript remains usable.

**Misuse.** MUST NOT use fake percentages, decorative waveform loops, or a network-quality score.

### DS-TranscriptLine

**Purpose.** Make produced audio readable and every word definable.

**Anatomy.** Speaker name or mark; one semantic utterance; timed word spans; optional current-line indicator.

**States.** Inactive, active line, active word, auto-follow on, auto-follow off, timing unavailable.

**Behaviour.**
- The default transcript reads as ordinary paragraphs at 18/30 px desktop and 17/28 px mobile, measure 760 px, with generous space between speakers.
- The active word receives a quiet selection field and underline over `motion-instant`. Karaoke bounce, colour chase, and per-word screen-reader announcement are prohibited.
- Speaker changes create spacing, not message bubbles. Speaker labels use host accent while body text remains neutral.
- Auto-follow keeps the active utterance within the middle third of the viewport and pauses immediately on manual scroll or touch; "Follow audio" then reappears as a `DS-TextAction`. The user MAY turn off auto-follow without stopping playback.
- Word timing uses the media clock and corrects drift at utterance boundaries. Highlighting MAY lag by no more than 150 ms under ordinary conditions. Beyond the drift threshold the system falls back to line-level highlighting and states that word timing is temporarily unavailable. It MUST NOT repeatedly jump the scroll to catch up.
- EP-53 timing state is literal component input. Only `timingState='ready'` with two concrete ordered times may receive active-word highlighting, seeking, or sentence-position derivation. `pending` and `unavailable` always carry null times: both remain readable and definable, but neither highlights, seeks, fabricates an offset, or enters sentence fallback until a later manifest makes that exact token ready. An `unavailable` token never becomes ready in the same epoch.
- Timing tokens are language-aware and MAY represent morphemes or character sequences where whitespace is absent. The visible highlight MAY span multiple glyphs. RTL highlighting follows logical reading order and auto-scroll uses block position.

**Accessibility.** Screen readers receive the transcript as paragraph text. Word exploration uses a roving-focus mode so thousands of words do not flood the tab order. The active line uses `aria-current` rather than a constantly changing live region; the current sentence is available through a dedicated control. Desktop MAY make the speaker label sticky within the current utterance only; mobile uses ordinary inline labels so text is not occluded.

## 6.6 Reading and definition components

### DS-ArticleHeader

**Purpose.** Establish the article as an editorial object.

**Anatomy.** Contextual kicker; title, which may differ from the episode title; optional one-sentence deck; cast reference; date; estimated reading time.

**States.** Default; with deck; without deck; loading, using `DS-Skeleton` on known title and body-line geometry.

**Body rules.** The body supports paragraphs, subheads (permitted after 350 words), block quotes when editorially warranted, and source or context notes only where the generated article genuinely relies on a named source. Decorative pull quotes MUST NOT be used to fill space. Measure is 680 px default and 720 px maximum, at 19/31 px desktop and 18/29 px mobile. Notes MUST NOT use multi-column newspaper text and MUST NOT use a sticky table of contents. Reading time is permitted because it describes the media object.

**Misuse.** MUST NOT contain learning objectives, vocabulary counts, completion status, comprehension prompts, word counters, completion rings, answer fields, or highlighted target language.

### DS-DefineTrigger

**Purpose.** Make every word definable without changing the article's visual texture.

**Anatomy.** The whole word is the target. No persistent affordance is drawn.

**States.** Unavailable (the surface's complete definition set is absent or locally invalid), rest (no visual change), hover (subtle underline after 120 ms), focus, open.

**Behaviour.**
- A surface MUST remain in the unavailable state until its complete definition set is present and passes local payload validation. Unavailable triggers receive no hover, focus, or tap action and MUST NOT open `DS-DefinePopover`.
- On an available trigger, the first touch tap opens the definition from the already-delivered local set and MUST NOT select text first. Native text selection remains available through long press. A tap MUST NOT start `EP-50`, another network request, or a model call.
- Punctuation attaches visually but is excluded from the definition token unless linguistically necessary.
- Scripts without whitespace use language-specific segmentation aligned with definition pre-computation; the selected unit MAY be a character sequence rather than a space-delimited word.
- Repeat taps are logged invisibly through the existing buffered event path and MUST NOT create history, stars, flashcards, or a tap-triggered request.
- Hover MUST NOT be the only route to a definition.

**Accessibility.** Enter on a transcript or article line enters word-exploration mode; arrow keys move among word tokens; Enter opens Define; Escape returns to line navigation. Focus MUST NOT enter decorative punctuation tokens.

### DS-DefinePopover

**Purpose.** Remove a momentary comprehension obstacle without starting dictionary work.

**Anatomy, in order.** Selected surface form with the short surrounding phrase; native-language meaning; part of speech; one target-language example. Nothing else.

**Variants.** `desktop-popover` (anchored, maximum 352 px wide, maximum 50vh body, 8 px radius, 1 px border, `shadow-popover`, `z-popover`), `mobile-sheet` (bottom sheet with drag handle, repeating the selected word, at most 70% of the visual viewport).

**States.** Opening, open, updating in place, local-payload-invalid, closing.

**Behaviour.**
- The desktop popover flips above and below and to either side to remain in view.
- A second word updates the same surface in place. Popovers MUST NOT stack.
- Long meanings scroll inside the body while the surface itself remains dismissible.
- Escape, outside click, Close, and browser Back all dismiss it. The selected word returns to focus on close.
- The mobile sheet MUST NOT cover the word without also repeating it, and MUST NOT trap the user below the keyboard.
- Underlying audio continues by default; it pauses only under an explicit screen-reader preference.
- A missing, corrupt, or schema-invalid local entry after the surface was marked definition-ready fails closed into `local-payload-invalid`: no partial or mismatched definition renders, and the only actions are Close and Reload this page. The tap and error surface MUST NOT start a network request, `EP-50`, or a model call; Reload this page reloads the whole owning surface.
- Open on desktop uses fade plus a 4 px scale or translate over 140–220 ms; mobile uses a sheet rise.

**Accessibility.** The selected word, meaning, part of speech, and example are announced as a dialog.

**Misuse.** MUST NOT contain conjugation tables, audio pronunciation, save-to-list, a quiz, mastery status, similar words, etymology, or a vocabulary count.

## 6.7 Voice-interaction components

### DS-CallInStage

**Purpose.** Make the user feel the show genuinely needs their position, while keeping live voice safe and low-anxiety.

**Anatomy.** Show title; host mark and name; AI-host disclosure available in context (`DS-DisclosureLine`); live-state label; primary microphone state; Mute; Captions; End; connection message; optional recording-status line.

**Visual states.**
- **Connecting:** static status and a cancel action. No fake waveform.
- **Host speaking:** the host mark gains a 3 px accent edge (`border-live`); real audio energy MAY modulate a short line within a narrow range.
- **Host listening:** status reads "On the line" or "Listening"; the user microphone control becomes primary.
- **User speaking:** status reads "You're on" and the mic fill changes. No score, waveform judgement, or fluency feedback appears.
- **Silence:** no countdown. After the host's prompt, status returns to listening.
- **Ending:** controls simplify while the host signs off; Mute remains and the primary control becomes End now.
- **Failed live line:** a recovery surface offers voice notes within the same session.

**Behaviour.**
- The environment is Booth and full-bleed. The stage is full-height on mobile and centred to 760 px on desktop. Controls sit in a safe bottom dock.
- There is no visible countdown. A small elapsed time MAY appear inside `DS-OverflowMenu` for accessibility and support, never as a central pressure cue.
- If real energy data is unavailable the modulating line remains static. Fake waveforms are prohibited.
- The masthead and compact player MUST NOT appear. The call owns audio focus.
- Landscape mobile uses a two-column arrangement, host state at the inline start and controls at the inline end, preserving an obvious End control.
- The primary control uses `control-call` 64 px; its icon MAY be 28 px.
- End and Mute order MAY mirror in RTL only where usability testing confirms it; End remains visually isolated.
- The first activation of End MUST stop local microphone publication and remote playout immediately. When the user is not actively recording, that activation submits EP-60. During the user's active recording it instead opens SCR-12/S12 after the cutoff and MUST NOT submit EP-60 until **End the call** is confirmed. Opening the dialog never resumes audio. **Keep talking** submits nothing and restores both directions only when the same session remains live and eligible; otherwise the component keeps audio cut off and refreshes owner state.
- The failed-live-line state and voice-note offer MUST appear only when FR-230's closed set is satisfied: live entry is unavailable; connection or transport recovery is exhausted or declared unrecoverable; agent-worker reassignment or recovery is exhausted; STT or TTS recovery is exhausted or declared unrecoverable; or the configured realtime-LLM chain is exhausted or declared unrecoverable. Recoverable connection instability, one recoverable worker/provider fault, connection quality alone, and latency alone MUST NOT trigger the voice-note offer.

**Accessibility.** State changes use `aria-live="polite"`. Microphone denied and connection lost use assertive announcement only where immediate action is required. Live regions MUST NOT fire on audio energy. Captions are available without implying correction. End is always visible and its first activation is the single reachable safety action that cuts both local audio directions; SCR-12/S12's conditional confirmation is permitted because it neither hides nor delays that cutoff. Escape MUST NOT end a live call without confirmation. There is no forced full-screen mode, camera, speaking score, interruptive haptic, or countdown.

**Misuse.** MUST NOT display pronunciation meters, confidence bars, per-turn praise, a tutor face, script suggestions, answer choices, or a pulsing red recording theatre unrelated to actual state.

### DS-VoiceNote

**Purpose.** Keep the argument alive when the live line fails, as a turn-based audio exchange rather than a chat substitute.

**Anatomy.** Duration; Play; transcript reveal; state line; COPY-154 pre-record loss warning; Discard recording action for an unaccepted Blob; persistent End control.

**States.** Recording, uploading, sent, host replying, failed, played, paused after fallback recovery is exhausted.

**Behaviour.** Recording uses tap-to-start and tap-to-stop, never press-and-hold only. Before recording begins, the exact COPY-154 warning states that navigating away, reloading, or closing the tab loses an unsent note. While an unaccepted Blob exists, **Discard recording** stops active tracks, destroys the Blob, returns to the no-draft offered state, and calls neither EP-26 nor EP-27. The Blob is never placed in durable browser storage or a service-worker queue. Send exposes an in-flight state; a failure returns the same-document Blob, warning, retry, and Discard action, while EP-27 acceptance alone changes the note to Sent and removes the warning and Discard action. Exactly one accepted user note MAY await a host reply; recording and Send remain unavailable until that reply is durably stored. Every accepted note receives exactly one generated host voice note and transcript. End remains visible throughout. A terminal reply, the fifth host reply, or End closes the exchange under FR-231; a pending terminal reply is stored before the component leaves Call-in. Each user note shows its upload and storage state. Transcripts are exposed for both sides. If fallback recovery exhausts, every durable turn remains resumable. An unaccepted recording survives only while the same document remains open; SCR-13/S10 keeps its warning and Discard action, and navigating Back to Today loses that Blob without abandoning or restarting the durable session.

**Misuse.** MUST NOT be presented as a chat thread, MUST NOT accept attachments, and MUST NOT show read receipts.

### DS-MicPermissionPanel

**Purpose.** Explain the microphone before the browser asks, and keep a path open after denial.

**Anatomy.** Plain-language purpose; a statement of what is stored under the current consent choice; two actions — Try again and Continue with voice notes; browser-specific help shown only after denial and only when the browser is known.

**States.** Pre-permission education; prompt pending; denied and re-promptable; denied and requiring browser settings; device unavailable.

**Behaviour.** Permission MUST NOT be requested before the user taps the call action. After denial the UI detects whether the browser allows another prompt or requires settings. Automatic repeated prompting is prohibited. On iOS, permission education appears before the system prompt so the browser dialog is not the first explanation.

**Misuse.** MUST NOT block the session, MUST NOT imply the session is lost, and MUST NOT moralise.

## 6.8 Messaging components

### DS-AfterShowThread

**Purpose.** Reproduce the last few messages after a real argument, and then stop.

**Anatomy.** Episode title context; host turns as short editorial lines carrying host name and mark; user turns on a subtle `paper-100` inset; closing rule.

**States.** Waiting for the first reply; open; closing; closed with one final reply; closed; outgoing message failed; reply delayed.

**Behaviour.**
- Maximum thread width 640 px. Host turns MUST NOT use large coloured bubbles. User turns keep turn ownership through the inset surface.
- Timestamps appear only when the session spans a long pause.
- The thread supports target-language text and native-language system messages without mixing voices.
- A new message settles 6 px upward and fades over 160 ms; only the new line moves.
- No typing indicator remains once the host has closed the thread, and typing indicators are never announced.
- Host turns serialize by ordinal. With no user reply, the next turn is scheduled 15 seconds after the prior durable turn and message 3 closes; scheduling continues while the user is away. Interactive threads close at message 4 or 5 under FR-235.
- After the closer, the optional final-reply lifecycle remains open for 60 seconds only while the surface is open. A final user reply receives exactly one host reply; navigation away or expiry closes without it.
- After closure a horizontal rule closes the thread and a collapsed note field accepts later text.

**Accessibility.** New messages announce sender and text once.

**Misuse.** MUST NOT offer open-ended "Ask anything," attachment tools, voice input, online status, read receipts, infinite history, or companion-style availability copy.

### DS-Composer

**Purpose.** A reply field with a designed ending.

**Anatomy.** Text input growing from one to three lines by default to six lines and then scrolling; an accessibly labelled Send control.

**Lifecycle variants.**
1. **Open:** ordinary reply field.
2. **Closing:** after the host's natural closer the placeholder changes to the closing placeholder and supporting text states that the thread is ending; the optional final-reply window is 60 seconds while the surface remains open.
3. **Closed with one final reply:** the composer is removed.
4. **Note for next time:** a collapsed field accepts further text without promising an immediate answer; submission confirms that the note is saved for next time.

**States.** Empty, typing, sending, send failed with the message still editable and a Retry, disabled offline with the text stored locally and marked as saved on this device, removed.

**Behaviour.** Text only in v1. Enter sends only where the user's locale and platform convention support it; Shift+Enter always creates a new line. The composer uses `position: sticky` inside the document flow where possible, with fixed positioning as a fallback using visual-viewport calculations. Height collapse after the final reply takes 220 ms and the closing rule draws once.

**Misuse.** MUST NOT persist after the thread closes and MUST NOT promise a response time.

### DS-IntakeTurn

**Purpose.** Present the intake as a continuous interview script rather than a chat app.

**Anatomy.** The current producer turn as a large authored paragraph with a compact Play/Pause control; earlier producer turns as transcript paragraphs; user responses as inset quotations with a small "You" label.

**States.** Current (high contrast), previous (softened but readable), playing, replayable, editing a text reply, replaced voice reply, offline-cached.

**Behaviour.** Producer audio MUST NOT autoplay over user recording. When producer audio ends, focus moves to `DS-ReplyDock` without opening the microphone. The user MAY replay a producer turn, edit a text reply before sending, and replay or replace a sent voice reply before the producer responds. Column width is 760 px. Target-language moments preserve the target script in the transcript and offer a small native-language replay or meaning action only on request or apparent difficulty; no score follows.

**Misuse.** MUST NOT use speech bubbles, avatars, typing dots, assistant tool labels, a completion indicator, or a marker that an answer was incomplete.

### DS-ReplyDock

**Purpose.** Let the user choose text or voice for every reply.

**Anatomy.** Type mode (text field plus Send); Record mode (record control, elapsed time, Stop, review, Send).

**States.** Type, recording, reviewing, uploading, upload failed with the local recording retained until Retry or Replace, read-only offline.

**Behaviour.** Modality is chosen per message. Record mode shows elapsed time and Stop and MUST NOT show pronunciation quality. Selecting Type dismisses microphone UI cleanly. Recording controls remain visible when the software keyboard is closed. When the keyboard opens, the current field scrolls into the upper 40% of the visual viewport.

**Misuse.** MUST NOT force a modality and MUST NOT discard a recorded reply on failure.

## 6.9 Inputs and controls

| Component | Specification | Content and misuse rules |
|---|---|---|
| `DS-PrimaryButton` | Solid `color.action.primary` (Petrol on Paper, Broadcast on Booth); heights 44 px and 52 px; `radius-3` 8 px; grows vertically with text | One primary action per region. No gradient or shine. Fixed-width text buttons are prohibited. |
| `DS-SecondaryButton` | Transparent with a 1 px border; same heights and radius | MUST NOT be used for a destructive action placed beside a weak primary. |
| `DS-TextAction` | Underlined on hover and focus; minimum 44 px target when standalone | Suitable for Skip, Another idea, and Back. MUST NOT carry primary consent. |
| `DS-TextField` | Persistent label; helper and error below; `radius-2` 6 px; visible border | No placeholder-only labels. No prompt-engineering examples unless genuinely needed. Errors linked with `aria-describedby`. Password managers MUST work. |
| `DS-LanguageSelector` | Search input; locale name; native-script name; single selection | MUST NOT group languages by popularity in a way that hides the full list. |
| `DS-SegmentedChoice` | Maximum 3 short mutually exclusive choices | Longer format or voice inventories MUST use a list or select. |
| `DS-FormatSelector` | Editorial list of name plus one-line description; free-text option last | MUST NOT show "best for your level" or any difficulty metadata. The system mapping stays invisible. |
| `DS-CastSelector` | One or two stable host marks; prevents a third selection | Selecting a third replaces only after an explicit choice and MUST NOT silently deselect. Retired hosts are absent. No avatar-marketplace layout. |
| `DS-VoiceSample` | Row with variant or voice name, Play, and Select; 10–15 second samples | Only one sample plays at a time. Descriptions are neutral. MUST NOT infer or label sensitive demographic attributes beyond what the provider legitimately exposes and the user chooses. |

**Shared control rules.** Minimum hit area 44×44 px, 48 px preferred on mobile. Focus is never removed because a control also has hover styling. Cast and format selectors support arrow navigation and explicit selection announcements. Destructive actions require deliberate activation but MUST NOT require complex gestures. Buttons grow vertically under text expansion; a text button MUST NOT have a fixed width.

## 6.10 Trust and account components

### DS-ConsentChoice

**Purpose.** Present a storage choice with equal weight and stated consequences.

**Anatomy.** Plain title; consequence paragraph; two equally legible actions; an available "How this works" disclosure.

**States.** Unselected (default), selected, saving, saved, save failed requiring server confirmation, offline and disabled with an explanation.

**Behaviour.** Neither option is preselected. Neither option is visually shamed or de-emphasised. Declining MUST NOT introduce a warning or a disabled-feature list. Animation is forbidden on this component. Consent changes require a confirmed server connection and MUST NOT show optimistic success offline.

**Misuse.** MUST NOT use preselection, guilt colour, deceptive primary emphasis, or consent hidden inside legal text.

### DS-ConsentHistory

**Purpose.** Present the user's append-only voice-storage choice history as a readable trust record, separate from the current consent control.

**Anatomy.** Heading; flat event list; one action label and one localised full date-and-time value per row; an inline loading, empty, or error region in the same list position.

**States.** Loading with known row geometry; populated; empty; read failed with retry; offline with previously loaded rows; offline before history was loaded.

**Behaviour.** The component renders every voice-storage consent event in the exact order returned by the read contract owned by `06-data-api-spec.md`. It MUST NOT locally reorder, merge, edit, or delete events. A row uses the exact on/off label owned by SCR-23 and the event timestamp; the current consent control remains `DS-ConsentChoice`. A history-read failure stays local to this component, preserves the current choice, states that the choice did not change, and retries only the history read. Offline state preserves previously loaded rows and MUST NOT represent an unavailable history as empty.

**Accessibility.** The heading labels the list. Each row exposes one complete accessible phrase containing the action and full localised date and time. Loading is announced once; retry does not move focus unless the user activated it.

**Misuse.** MUST NOT expose database identifiers or copy-version internals, permit history editing, use a timeline animation, or substitute a mutation error for a read failure.

### DS-ConfirmationDialog

**Purpose.** Name the object and the consequence before a state change.

**Anatomy.** A title naming the specific object; consequence text; the safe action first; a destructive action naming the result.

**Variants.**
- `standard` — one confirmation, two actions. Used for active-session conflict, abandonment, leaving a live line, retiring a host, and revoking voice storage.
- `type-to-confirm` — adds a `DS-TextField` requiring an exact, case-insensitive match of a single localised confirmation word shown in the field label. The destructive action stays disabled until the field matches. **Reserved for account deletion (SCR-27).**

**States.** Open, field empty, field mismatched, field matched, submitting, failed, closed.

**Behaviour.** Layer `z-dialog`. The safe action is first and visually primary. The destructive action uses `error-700` only on hover, focus, and confirmation, never as a large red block. Animation is forbidden on destructive confirmation. One confirmation is the maximum; repeated confirmation of the same action is prohibited.

**Misuse.** MUST NOT use a generic "Are you sure?" title, MUST NOT hide the consequence behind a link, and MUST NOT use guilt colour or a labyrinthine cancellation path.

### DS-InlineCorrection

**Purpose.** Correct one remembered fact in one direct action.

**Anatomy.** The current remembered statement; a correction field accepting text or voice; Save and Cancel; for voice, a permission explanation, recording indicator, Stop/Cancel controls, and a non-optimistic processing status.

**States.** Closed; open; text editing; text saving; voice permission education; voice recording; voice processing; permission denied; saved with the new wording echoed; failed.

**Behaviour.** The correction begins from the current plain-language statement and overwrites the fact immediately. Text and voice use the same durable EP-43 `operationId`. Voice bytes upload directly to the owner-signed temporary key and remain neither learner memory nor call-audio; the component MUST NOT render a transcript candidate or success while the operation is awaiting upload, queued, transcribing, or failed. Permission denial preserves the text path. The confirmation echoes the new fact in plain language only after the committed result. Ordinary corrections MUST NOT require a confirmation dialog.

**Misuse.** MUST NOT expose confidence values, provenance, salience, or the full internal learner file.

### DS-KnowledgeStatement

**Purpose.** Show one thing the show remembers, in the user's own terms.

**Anatomy.** One plain-language sentence; a "That changed" action opening `DS-InlineCorrection`; in the active variant, a dormancy action worded as stopping use in the show; in the pinned-dormant variant, an explicit undo action worded as resuming use in the show.

**States.** Active; correcting; corrected; dormancy saving; dormancy saved; dormancy failed; pinned dormant; undo saving; undo saved; undo failed; offline with mutations unavailable.

**Behaviour.** The dormancy action MUST use honest wording. It writes `dormant: true` through EP-44, keeps the row active until server confirmation, and MUST NOT claim deletion. EP-42's `dormant` field determines the rendered variant. Explicitly pinned dormant rows remain reachable in SCR-22's dormant group and offer its exact undo action, which writes `dormant: false` through EP-44; automatically dormant, unpinned rows do not render there. Correction remains available on a pinned dormant row and MUST NOT unpin it. Failed dormancy or undo writes keep the prior variant; offline mutations MUST NOT show optimistic success. Grouping, state copy, and action copy are owned by SCR-22.

**Misuse.** MUST NOT display confidence, error analytics, proficiency, targets, engagement scoring, inferred energy, or any language-profile content.

### DS-DisclosureLine

**Purpose.** State AI identity or recording status wherever a user reasonably needs it.

**Variants.** `ai-identity` (the producer and hosts are AI characters), `recording-status` (transcript and audio storage under the current choice).

**States.** Static; expanded through an adjacent labelled information control during a call.

**Behaviour.** Recording status MUST appear before Call-in entry and MUST remain reachable during the call through a labelled information control. It MUST NOT be represented by an ambiguous red dot alone. AI disclosure appears at producer introduction, first host introduction, Voice tape, About this AI show, and wherever confusion with a human live service is plausible. It MUST NOT prefix every host line. Animation is forbidden on the recording-status variant.

### DS-CastRow

**Purpose.** One host in the roster, as an editorial row.

**Anatomy.** `DS-HostMark`; name; one-line character description; `DS-VoiceSample`; status; actions.

**Variants.** `default-duo` (labelled as the default duo; no edit or retire), `created-active` (Edit through conversation, Retire), `retired` (inside a collapsed section, Bring back).

**States.** Default, sample playing, editing, retiring, retired, unavailable voice, creation draft retained.

**Behaviour.** Retired hosts MUST NOT be castable until restored. The roster shows a capacity line only when the maximum of six created hosts is reached, and states it as capacity rather than achievement. Delete is not offered; retiring preserves history and memory.

**Misuse.** MUST NOT become a marketplace card and MUST NOT display likes, rarity, bond level, public sharing, age or gender sliders, human portraits, or romance framing.

### DS-ArchiveRow

**Purpose.** One chronological record, readable as an index rather than a catalogue tile.

**Anatomy.** Date; episode title; cast; format; state (Complete or Ended early); duration when audio exists.

**Variants.** `episode`, `weekly-proof` (Proof accent and the Weekly Proof label).

**States.** Default, hover, focus, audio removed, partially available for an abandoned record.

**Responsive.** Desktop uses a date column and a flexible title column. Mobile stacks date and state above the title with cast and format below. Rows are 56 px minimum and separated by rules.

**Accessibility.** Month headings are real headings for screen-reader navigation. A row MAY clamp the title visually while the full text remains in the accessible name and on the detail surface. State is text, not only an icon.

**Misuse.** MUST NOT become a cover tile and MUST NOT display totals, charts, streaks, hours listened, completion percentages, leaderboards, or social sharing.

## 6.11 Feedback and system-state components

### DS-SystemBanner

**Purpose.** A page-level notice that persists until its condition resolves.

**Variants.** `verification` (slim, Paper surfaces only, with a resend action), `offline` (persistent slim banner), `export-ready` (§9.3 delta 1; links to Account essentials).

**States.** Present, action pending, resolved and removed.

**Behaviour.** Banners render inside the page rather than as overlays and MUST NOT obscure a primary action. The offline banner keeps loaded reading and audio available while live and new-generation actions are disabled with an inline explanation. A banner MUST NOT be the only place a state is available; the owning surface always states it too.

**Misuse.** MUST NOT be used for marketing, re-engagement, or celebration.

### DS-RequestStatus

**Purpose.** State the honest condition of an asynchronous request the user made.

**Anatomy.** One status line; an optional secondary detail line; at most one action.

**Variants.** `audio-removal` (removal in progress, shown beside affected archive items), `export` (preparing, ready with an expiry date, expired, failed).

**States.** Requested, in progress, complete, expired, failed with Retry, failed persistently with a support path.

**Behaviour.** Progress MUST be stated in words, with no percentage and no time promise beyond a settled budget. A persistent failure remains on the owning trust surface with Retry and a support path and MUST NOT be delivered as a transient toast.

### DS-GenerationState

**Purpose.** Preserve the authored object while media is produced.

**Anatomy.** The real `DS-EpisodePlate`; one honest stage-neutral line; a statement that leaving is safe; the primary action once it becomes real.

**States.** Making; partially ready; ready; delayed under FR-110; automatic primary regeneration; generated fallback; terminal authored fallback; persistent terminal failure with the owning support path.

**Behaviour.** No spinner in empty space, no percentage, no time countdown, and no pipeline wording. A generated title MUST NOT be replaced by a generic grey card once it is known. The user MUST be able to leave the page without losing the work. A loading state MUST NOT delay a control that is already ready. Primary regeneration, generated fallback, and terminal authored fallback are automatic owner-state projections and expose no client mutation. Every readable authored-fallback reason uses the owning Play state; if the authored-fallback job itself exhausts, the persistent terminal-failure state renders COPY-341 and the single configured support link from SCR-05/S15, SCR-07/S18, or SCR-08/S15, with no Retry or Play action. When FR-110's no-progress delay threshold elapses, the determinate wait MUST change to the delayed state owned by SCR-05/S13, SCR-07/S14, and SCR-08/S11; the authored plate remains visible and the in-app readiness action keeps generation alive while returning the user to Today. The only explicit pre-pitch Retry is SCR-05/S9's infrastructure recovery through EP-11 and is outside this component.

**Misuse.** MUST NOT name the planner, a model, the quality gate, synthesis, transcription, or assessment.

### DS-Skeleton

**Purpose.** Hold known geometry while known content loads.

**Behaviour.** Permitted only for text-line and player-shell geometry whose shape is known. Uses static `paper-100` or `booth-800` blocks with no shimmer under reduced motion and a very slow single luminance shift otherwise. Skeletons MUST NOT be used where a real title, cast, or state is already known, and MUST NOT move.

### DS-EmptyState

**Purpose.** Explain what will appear and after which action.

**Anatomy.** One plain sentence; at most one action returning to the relevant surface.

**Misuse.** MUST NOT insert demo statistics, sample episodes, fake history, or an illustration implying achievement.

### DS-ErrorState

**Purpose.** Say what failed, what remains safe, and what to do.

**Anatomy.** A statement of the failure; a statement of what is preserved; exactly one primary recovery action; an optional secondary path that continues the session.

**Variants.** `inline` (within the affected region), `blocking` (only where the user genuinely cannot proceed), `persistent-trust` (consent, export, and deletion failures).

**Behaviour.** The voice is calm and specific. It MUST NOT blame the user or anthropomorphise the failure, and MUST NOT name a provider, model, or internal stage. Animation is forbidden. Ordinary silence, pauses, and ending early MUST NOT use error styling.

### DS-Toast

**Purpose.** A rare transient system notice at `z-toast`.

**Behaviour.** MUST NOT carry critical actions, consent, destructive confirmation, or the only notice of a failure. Critical states remain in the page.

# 7. Interaction and motion

## 7.1 Interaction character

For one should feel **composed, immediate, and acoustically quiet**. Motion indicates continuity between media forms and confirms state. It MUST NOT advertise intelligence, create anticipation, or reward completion.

## 7.2 Motion hierarchy

| Interaction | Behaviour | Duration |
|---|---|---:|
| Hover and focus | Colour or border change only | 80–140 ms |
| Programme row open | The row title holds position while the sheet enters from the edge | 220 ms |
| Prepared pitch to Episode | The title plate expands; Paper crossfades to Booth | 320–420 ms |
| Supporting pitch generation | The sheet remains; the title plate settles; status changes without looping spectacle | 220 ms |
| Full player to compact player | Shared title and control transform; critically damped spring permitted | 280–340 ms |
| Transcript word change | Background and underline crossfade, no translation | 80 ms |
| Define open | Fade plus 4 px scale or translate on desktop; sheet rise on mobile | 140–220 ms |
| Episode to Notes | Booth recedes; Paper rises beneath the final transcript line | 320 ms |
| Notes to Call-in | The host accent rule expands into the Booth edge; no countdown | 320–420 ms |
| Live state change | Text and the real state indicator crossfade | 100–160 ms |
| Call end to After-show | Booth dims, the host sign-off completes, the Paper thread appears | 320 ms |
| Chat message arrival | 6 px upward settle and fade; only the new line moves | 160 ms |
| Thread close | Composer height collapses after the final reply; the closing rule draws once | 220 ms |
| Weekly Proof open | The Proof field expands to its player; no celebration | 260 ms |

## 7.3 Easing

- Standard interface motion: `cubic-bezier(.2, 0, 0, 1)`.
- Emphasised media transition: `cubic-bezier(.16, 1, .3, 1)`.
- Exit: the slightly faster `cubic-bezier(.4, 0, 1, 1)`, used only when content is truly leaving.
- Spring: only for bottom-sheet and player settling, damped enough to prevent visible bounce.

## 7.4 Concurrent-motion rules

- One dominant spatial motion at a time.
- Audio controls MUST remain responsive during page transitions.
- Transcript highlighting MAY continue while a compact player transforms; no other decorative motion runs at the same time.
- A loading state MUST NOT delay a control that is already ready.
- Motion MUST NOT be required to understand order, status, or speaker identity.

## 7.5 When animation is forbidden

Animation MUST NOT be used on:

- consent and destructive confirmation;
- error copy and recovery actions;
- under-age rejection;
- flat-week messaging;
- audio recording disclosure;
- account deletion and data-export confirmation (§9.3 delta 1);
- any state where motion would imply that the system is listening, recording, or generating when it is not;
- completion celebration.

## 7.6 Reduced motion

With `prefers-reduced-motion: reduce`:

- spatial page transitions become an 80 ms opacity change or an immediate swap;
- player expansion becomes an instantaneous layout change with focus preserved;
- the active transcript word changes without animation;
- live state uses text and static colour only;
- sheets appear without spring or drag-settle animation, while swipe-to-dismiss MAY remain functional;
- skeletons lose the luminance shift entirely.

# 8. Audio system behaviour

This section owns the cross-screen behavioural contracts for every audio object. Screens cite it; they do not restate it.

## 8.1 Audio objects and their visual contracts

| Audio type | Surface and controls | Persistence | Recording and storage indication |
|---|---|---|---|
| Produced episode | Booth `DS-FullPlayer`; timeline, 10s back, 0.8×/1.0×, transcript | Continues on Paper navigation where the browser permits; state always restores | No user recording |
| Producer intake audio | Paper inline player inside the current `DS-IntakeTurn` | Stops before user recording; MUST NOT become a compact player | User voice reply state is shown separately |
| Host introduction | Paper title plate with a short player and optional transcript | Replayable in onboarding and the cast record | No user recording |
| Live Call-in | Booth `DS-CallInStage`; Mute, Captions, End; no timeline | Exclusive audio focus; leaving may end the line | A persistent line states whether audio is stored or transcript-only |
| Voice-note fallback | `DS-VoiceNote` player and recorder with transcript | Persists as part of the current session | Each user note shows its upload and storage state |
| Weekly Proof | Proof surface player; optional comparison clips | Persists in Archive | Comparison type follows consent |
| Archived user call recording | Archive player only when consented and not deleted | Read-only; removed after revocation | After deletion the player is replaced by the audio-removed state |

## 8.2 Audio focus

- Starting produced episode audio pauses other For one produced audio.
- Starting intake playback pauses episode audio if onboarding is revisited.
- Entering Call-in pauses all produced audio and clears the compact player from view.
- Starting microphone capture pauses output until echo-cancellation setup is complete. Host audio and the microphone MUST NOT compete.
- A second browser tab acquiring For one audio focus pauses the first tab and states that playback moved to another tab.

## 8.3 Player persistence and navigation

Produced-audio state includes source, episode identifier, elapsed position, duration, speed, buffered range, and transcript-follow preference. It persists across Today, Notes, Archive, Cast, and Trust. It MUST NOT persist across sign-out.

Selecting another episode while one is playing prompts only when doing so would replace active session state. Replaying an archived episode MAY replace the compact player without a destructive confirmation because it does not alter session state.

## 8.4 Interruptions

**Operating-system interruptions.** When the platform emits an interruption or pause event, the position is stored immediately and the interface states that another audio app paused playback. Playback MUST NOT resume automatically after a phone call ends; the user resumes explicitly.

**Output-device changes.** Where the browser exposes output changes: a valid device switch continues playback and shows a short non-modal status; loss of output pauses and states that the output changed and playback can resume when ready. The application MUST NOT present a custom device picker unless the platform safely supports it.

**Browser background.** Produced audio MAY continue using Media Session metadata carrying episode title, show name, and the deterministic plate where supported. Live calls MUST NOT be promised in the background; before the user backgrounds or navigates away from an active call, the interface warns that the line may close. If the browser suspends the call, recovery uses the saved partial transcript and the fresh-opening rule rather than pretending continuity.

## 8.5 Streaming and partial readiness

- The player becomes actionable when the first playable chunk and a duration estimate are available.
- The scrubber displays the loaded and available range separately from total duration.
- If later chunks stall, playback continues to the buffer boundary and then shows local buffering. The page MUST NOT reset to a full-generation state.
- Article production readiness is independent, but downstream exposure is not. When Notes finish before the active Episode folio becomes content-terminal, they remain inaccessible behind the Episode and the skip action is absent; once EP-52/EP-53 returns `contentTerminal: true`, the user may advance or skip without waiting for playback to finish. An Episode or Notes surface becomes definition-ready only when its complete delivered definition set passes local validation; before that point `DS-DefineTrigger` remains unavailable and no tap starts recovery work.

## 8.6 Buffering and error thresholds

Thresholds are owned by `DS-AudioStatus` (§6.5). A recovered stream resumes from the stored time and MUST NOT restart unless the source changed materially. A synthesis failure after partial playback preserves the transcript and the ready audio and offers Resume on recovery or a path to the notes.

## 8.7 Microphone permission

The pre-permission surface explains purpose and current storage. After denial the interface detects whether the browser allows another prompt or requires settings, and names the browser only when it is known. Voice notes are always offered as the fallback.

## 8.8 Echo and connection warnings

Warnings MUST be actionable and non-judgemental. They MUST NOT display a network-quality score or technical codec details.

## 8.9 Audio recording consent visibility

Recording status appears before Call-in entry and remains accessible during the call through a labelled information control. A small persistent line states the current storage condition. It MUST NOT be represented by an ambiguous red dot alone.

# 9. Responsive system

## 9.1 Responsive philosophy

Mobile is the primary participation environment, not a compressed desktop. Desktop offers wider editorial composition and more simultaneous context; mobile prioritises one clear media object, thumb-reachable controls, and safe audio interruption handling.

The system responds to **available width, text size, input mode, and safe area**, not device names. Components MUST reflow before text overlaps. Horizontal scrolling is prohibited for core content, except the browser's native behaviour for unusually long unbroken strings, which MUST NOT occur in ordinary show content.

## 9.2 Global mobile rules

- Respect `env(safe-area-inset-top/right/bottom/left)` on iOS.
- Fixed bottom controls sit above browser chrome and the keyboard using visual-viewport measurements.
- Primary touch targets are 48 px where space permits and never below 44 px.
- Hover MUST NOT be required for definitions, metadata, or secondary actions.
- The compact player and call controls MUST NOT overlap the composer or a system permission banner.
- When the keyboard opens, the current field scrolls into the upper 40% of the visual viewport; headers MAY collapse.
- Landscape Call-in uses a two-column arrangement — host state on one side, controls on the other — while preserving an obvious End control.
- Below 360 px, outer margins reduce to 16 px, metadata stacks, and display type reduces one step but never below 32 px for the lead pitch.
- Large-text mode takes priority over decorative composition. At 200% text, all multi-column core layouts become one column.

## 9.3 Core-surface responsive differences

| Surface | Mobile | Tablet | Desktop |
|---|---|---|---|
| Start and account (SCR-01, SCR-02) | One question per viewport; action above the safe-area bottom | Statement above form, or a 3/5 split | 5/7 editorial statement and form; no tall hero lock |
| Intake (SCR-04) | Continuous script; reply dock; audio control inline | Script plus a narrow disclosure rail | 760 px script with a 240 px contextual rail |
| First handoff (SCR-05) | Host marks and intro player stacked; pitch below | Title plate and pitch MAY sit side by side | Title plate 7 columns, pitch cue 5 columns |
| Today (SCR-06) | Lead then a ruled supporting list; no carousel | Lead 5 columns, support 3 columns | Lead 7 columns, support 5 columns |
| Production sheet (SCR-07, SCR-08) | Full-screen sheet with a sticky bottom action | 80% width sheet | Right-side 5-column sheet; the programme remains visible |
| Episode (SCR-09) | Player controls wrap; transcript 17/28 | Centred 7 columns | Player 840 px; transcript 760 px |
| Define (SCR-10) | Bottom sheet | Bottom sheet or anchored popover by pointer mode | Anchored popover |
| Notes (SCR-11) | 18/29 text; 20 px margin | 640 px measure | 680 px measure with an optional metadata rail |
| Call-in (SCR-12, SCR-13) | Full-height; bottom dock; captions overlay | Centred stage; larger host mark | 760 px stage with extra room for a status and disclosure rail |
| After-show (SCR-14) | Full-width thread within margins; composer above the keyboard | 600 px thread | 640 px thread with episode context in a narrow rail |
| Archive (SCR-17, SCR-18) | Date and status stacked above the title | Two-column date and title row | Date, title, cast, format, and state columns |
| Cast (SCR-19, SCR-20) | One host per row; sample opens inline | Two-column roster only where text remains readable | Default duo two-up; created hosts as editorial rows, not cards |
| Trust and account (SCR-21 to SCR-27) | Full-screen Your show; one section at a time | Wide sheet | 480–560 px right-side sheet |

## 9.4 Player placement

- The produced-audio compact player sits at the visual viewport bottom with bottom safe-area padding.
- On Notes it defaults to paused after a stage transition and remains expandable.
- During form entry or After-show composition it moves above the keyboard while playing; while paused it MAY collapse to a 44 px title strip.
- Live Call-in never uses the compact player. The call owns audio focus and the full bottom control dock.

## 9.5 Transcript and reading behaviour

- Transcript speaker labels remain sticky only within the current utterance on desktop; on mobile they are ordinary inline labels so text is not occluded.
- Auto-follow accounts for mobile browser chrome and stops when the user touches or scrolls the transcript.
- Notes MUST NOT use multi-column newspaper text. RTL and large text preserve a single readable column.
- Definition bottom sheets use at most 70% of the visual viewport and MUST NOT trap the user below the keyboard.

## 9.6 Keyboard avoidance and input

- The After-show composer uses `position: sticky` inside the document flow where possible; fixed positioning is the fallback, using visual-viewport calculations.
- Voice recording controls remain visible when the software keyboard is closed. Selecting Type dismisses microphone UI cleanly.
- On iOS, permission education appears before the system prompt.

# 10. Internationalisation and bidirectionality

## 10.1 Language roles

Every surface distinguishes:

- **Interface language:** normally the user's native language, carrying product controls, consent, failures, and trust.
- **Show language:** the target language, carrying episode, Notes, Call-in, After-show, and host dialogue.
- **Mixed support:** native-language meanings in Define and occasional producer clarification.

Direction is set at the smallest meaningful component. The page MAY be LTR while a target-language title is RTL, or the reverse.

## 10.2 Mirroring rules

| Element | RTL behaviour |
|---|---|
| Page grid and alignment | Mirror |
| Masthead order | Mirror, preserving wordmark prominence |
| Back navigation arrow | Mirror to follow navigation direction |
| Play triangle | Do not mirror |
| 10-seconds-back icon | Do not mirror; counter-clockwise remains "back" |
| Audio timeline | Time advances left to right for platform consistency; labels localise |
| Previous and next textual navigation | Mirror spatial placement and localise labels |
| Host marks | Do not mirror internal artwork; reposition with the layout |
| Episode plate accent rule | MAY mirror as part of the composition template |
| Scrubber keyboard arrows | Follow media semantics documented in help; physical Left decreases time, Right increases time |
| Call End, Mute, and Captions order | Mirror layout only where usability testing confirms it; End remains visually isolated |

## 10.3 Bidirectional text

- Wrap user names, host names, titles, and imported facts in `<bdi>` or `dir="auto"`.
- Use Unicode isolation controls only through a trusted formatting layer. Raw direction markers from generated content MUST NOT be concatenated.
- Punctuation belongs to the linguistic run, not the surrounding interface direction.
- URLs, email addresses, and timecodes use LTR isolation even inside RTL paragraphs.
- Quoted target-language phrases inside native-language consent remain isolated and readable.

## 10.4 Text expansion and truncation

- Plan for 35% expansion from English, and substantially more for compact labels.
- Buttons grow vertically. Fixed-width text buttons are prohibited.
- Navigation labels MAY wrap only in Your show; the masthead uses tested short localisations.
- Host names and titles MUST NOT truncate on primary surfaces. Archive rows MAY clamp visually with the full text in the accessible name and detail view.
- German-like compounds and Thai or Khmer line breaking use language-aware CSS and fonts. Arbitrary hyphens MUST NOT be inserted into names.

## 10.5 Script-aware typography

- Arabic display uses Noto Naskh Arabic with increased line height, approximately 1.55–1.7 depending on size.
- Arabic interface and transcript use Noto Sans Arabic; Latin numerals inside Arabic follow the selected locale convention.
- CJK reading body uses a vetted Noto Serif CJK package with 1.8 line height and a shorter character measure.
- Scripts without case MUST NOT imitate uppercase kickers; weight, colour, or spacing is used instead.
- Faux bold and faux italic are disabled when the font lacks a real face.

## 10.6 Dates, numerals, and time

- Date order and month names follow the interface locale.
- The programme issue number MAY use local numerals where legible; it is decorative metadata, not a global identifier.
- Playback time uses locale digits where platform conventions support them, with tabular width and a colon separator.
- Speed notation remains `0.8×` and `1.0×`, positioned according to local typography. The multiplication sign MUST NOT be translated into an ambiguous letter.

## 10.7 Localisation of copy

Copy is transcreated, not literally translated. `02-ux-spec.md` owns the copy catalogue and the per-language review criteria.

# 11. State system

## 11.1 State-design principles

1. Preserve the authored object — the title, cast, and chosen idea — while work continues.
2. Say only what the system knows. Fake percentages and time promises beyond settled budgets are prohibited.
3. Keep completed media available when another part fails.
4. Recover silently when the user does not need to decide.
5. Expose one primary recovery action and state what was preserved.
6. Never surface planner, model, quality-gate, synthesis, transcription, or assessment terminology.

Indefinite loading states are prohibited. Every asynchronous state MUST resolve to a success state, a recovery state, or an honest waiting state that permits leaving.

## 11.2 Skeleton policy

Skeletons are permitted only for known text-line and player-shell geometry. They use static `paper-100` or `booth-800` blocks, with no shimmer under reduced motion and a very slow single luminance shift otherwise. A generated title MUST NOT be replaced by a generic grey card once it is known.

## 11.3 Offline rules

- Loaded transcript, Notes, Archive text, and buffered audio remain usable.
- New pitch generation, remix, live calls, and new host creation are disabled with an inline explanation. A readable surface loaded with its complete definition set remains fully definable offline; a surface not loaded before disconnection is unavailable as a whole, never partly definition-ready.
- User text in intake and After-show is stored locally and queued only when the operation is idempotent; the interface states that it is saved on this device until it uploads.
- Consent changes, export requests, and account deletion require a confirmed server connection. The interface MUST NOT pretend success offline.

# 12. Accessibility standards

## 12.1 Standard

Target **WCAG 2.2 AA** across the full responsive web app, with AAA contrast for core body text where feasible. Accessibility requirements are component acceptance criteria, not a final audit checklist.

## 12.2 Colour and focus

- Normal text meets at least 4.5:1; large text 3:1; controls and focus indicators 3:1 against adjacent colours.
- Core body text exceeds 5.4:1 and primary text exceeds 16:1 in both environments.
- The focus ring is 2 px plus a 2 px offset on Paper, and a 3 px high-contrast ring on Booth.
- Focus MUST NOT be removed because a control also has hover styling.
- Host colour MUST NOT carry speaker or selection meaning alone; name and state text accompany it.

## 12.3 Keyboard navigation

- Logical order follows visual reading order in both LTR and RTL.
- A skip link targets the main programme or media content.
- Sheets and dialogs trap focus only while modal; closing restores the exact trigger.
- Escape closes popovers and sheets but MUST NOT end a live call without confirmation.
- Player shortcuts work only when focus is within the player or the user has opted into global shortcuts.
- The transcript uses line-level tab stops and roving word exploration.
- Cast and format selectors support arrow navigation and explicit selection announcements.

## 12.4 Screen readers and live regions

- Page titles identify the current episode and medium.
- Player controls include state and time. Elapsed time is not announced every second.
- Call state changes use `aria-live="polite"`. Microphone denied and connection lost use assertive announcement only where immediate action is required.
- New After-show messages announce sender and text once. Typing indicators are never announced.
- The active transcript word is visual only. Screen readers query the current sentence through a dedicated control rather than receiving constant updates.
- Weekly Proof comparison clips carry date and context labels.

## 12.5 Audio alternatives

- Produced episodes always have full transcripts.
- Host introductions and Weekly Proof have transcripts.
- Call-in has optional live captions and a stored transcript.
- The voice-note fallback exposes transcripts for both sides.
- Intake producer audio is mirrored in text and the user MAY respond by text on every turn.
- Audio-only information is prohibited in consent, errors, and navigation.

## 12.6 Large text and zoom

- Browser zoom to 200% MUST produce no loss, overlap, or horizontal page scrolling at a 1280 CSS px equivalent.
- Text-only scaling to 200% is supported on mobile where the browser provides it.
- Multi-column layouts collapse. Sticky and fixed regions become in-flow when they would obscure content.
- Controls grow in height and text wraps. Icon-only controls retain accessible labels and MUST NOT shrink.
- Episode titles MAY extend beyond the first viewport; Play remains reachable immediately after metadata.

## 12.7 Touch and motor access

- Minimum 44×44 px hit areas, 48 px preferred.
- The scrubber has a large invisible hit area and keyboard alternatives.
- Swipe-to-dismiss MUST NOT be the only way to close a sheet.
- Voice recording uses tap-to-start and tap-to-stop, not press-and-hold only.
- Destructive actions require deliberate activation but MUST NOT require complex gestures.

## 12.8 Cognitive load and anxiety

- One primary action per region.
- No countdown during Call-in.
- Permission and consent explain consequences before the browser prompt.
- The user can leave the call at any time.
- Ordinary silence, pauses, and ending early MUST NOT use red error styling.
- Generation and buffering use stable layouts rather than moving skeletons.
- Copy avoids performance judgement.

## 12.9 Voice-only limitations

Call-in requires voice or asynchronous voice notes. The entry surface MUST state this before permission is requested. A user who cannot speak at that moment MAY pause the session, skip forward, or use voice notes where technically possible. The product MUST NOT claim a fully text-equivalent live call that does not exist. Intake always retains text.

## 12.10 RTL accessibility

Accessible names follow semantic order, never visually mirrored DOM manipulation. Focus order MUST be tested with Arabic and Hebrew screen readers. Mixed-direction titles MUST announce cleanly without reading isolation characters aloud.

# 13. Destructive actions, consent, and content safety

## 13.1 Destructive-action design

- Safe choices appear first and are visually primary.
- Destructive labels name the result rather than saying "Confirm" or "Yes."
- Guilt colours, labyrinthine cancellation paths, and repeated confirmation are prohibited.
- One confirmation is required for: revoking voice storage (it deletes stored media), abandoning an active session (it changes state), leaving an active live line, retiring a host, and deleting the account (which additionally requires type-to-confirm, §6.10).
- Ordinary memory correction requires no confirmation.
- Destructive and consent changes require a confirmed server connection.

## 13.2 Visual honesty rules

The interface MUST NOT present:

- photorealistic host images;
- a green "online" dot or any simulated presence;
- a human biography presented as factual life experience;
- a claim that a host independently waited, missed, worried, or felt abandoned;
- a memory icon, "personalised" label, or any display of confidence values;
- an explanation of why a pitch was generated or which data drove it.

Voice and character MAY be warm, opinionated, and consistent. `02-ux-spec.md` owns the host copy boundaries.

## 13.3 Data-rights surfaces (§9.3 delta 1)

Export and account deletion are supported product behaviour. Their design obligations at the system level are:

- Both live under Account essentials inside `DS-YourShowSheet` and MUST NOT be presented as settings.
- Both use the legal and consent voice: plain, literal, free of jokes, stating what is stored, what changes, and how long completion takes.
- Export uses `DS-PrimaryButton` plus `DS-RequestStatus`; readiness is additionally surfaced by the `export-ready` variant of `DS-SystemBanner` and one transactional email.
- Deletion uses the `type-to-confirm` variant of `DS-ConfirmationDialog`, names every consequence before the field, signs the user out immediately on success, and is confirmed by one transactional email.
- Neither flow may use animation, celebration, retention copy, or a persuasive alternative offered in place of the destructive action.

# 14. Design QA gates

A screen is rejected if any applicable critical rule fails. "Looks attractive" is not a substitute for passing these checks. The banned lexicon cited by these gates is `02-ux-spec.md` Appendix B.

## 14.1 Product identity gate

- [ ] Does the screen feel like media made for the user rather than educational software?
- [ ] Is the primary object a programme, episode, article, call, or conversation rather than a dashboard metric?
- [ ] Is anything asking the user to manage difficulty, targets, sequencing, or assessment?
- [ ] Does the screen resemble a generic chatbot, streaming grid, task list, or course?
- [ ] Is there a large prompt box where an authored object should be?
- [ ] Would removing the logo make the screen indistinguishable from a generic AI template? If yes, reject.

## 14.2 Authorship and hierarchy gate

- [ ] Is the primary action obvious within three seconds?
- [ ] Does the composition identify what is ready, what is selectable, and what is secondary?
- [ ] Are titles specific and content-bearing rather than generic marketing copy?
- [ ] Has a rounded card been used where whitespace and a rule would be stronger?
- [ ] Is every badge and status factually necessary?
- [ ] Does the first viewport contain enough real programme information rather than decorative emptiness?

## 14.3 Participation gate

- [ ] Does the episode clearly create a reason to read and call in?
- [ ] Does the Call-in feel like joining the show rather than activating a tutor voice mode?
- [ ] Is the host's stance visible without scripts or suggested answers?
- [ ] Can the user leave without shame or loss?
- [ ] Does After-show visibly end?

## 14.4 Personalisation and trust gate

- [ ] Is every personal callback high-confidence, directly volunteered, relevant, and limited?
- [ ] Does the design avoid explaining or displaying prediction logic?
- [ ] Are hosts transparently AI wherever confusion is plausible?
- [ ] Does any visual imply a real human portrait, online status, or emotional dependence?
- [ ] Are recording and transcript states stated in text before Call-in?
- [ ] Can a remembered fact be corrected directly?
- [ ] **Does every export and deletion control state exactly what it includes or removes, how long completion takes, and whether it can be undone — and does every other control avoid implying a data action it does not perform?** *(replaces the superseded v1 export/deletion line; §9.3 delta 1)*

## 14.5 Language-learning-law gate

- [ ] Are every term and construct in the banned lexicon absent from the screen, in every language it ships in?
- [ ] Is correction invisible in flow unless the user explicitly asks?
- [ ] Are word meanings lightweight and contextual rather than a vocabulary system?
- [ ] Is Weekly Proof an authored piece of media rather than analytics?
- [ ] Is the user free to choose topic, format, and cast while pedagogy remains absent?

## 14.6 State and reliability gate

- [ ] Does every loading state preserve known content and avoid fake percentages?
- [ ] Does every error say what failed, what remains safe, and what to do?
- [ ] Can offline-loaded media still be used?
- [ ] Does live-call failure degrade to voice notes without session loss?
- [ ] Does pause restore the exact stage and a meaningful position?
- [ ] Are abandoned sessions neutral rather than shameful?
- [ ] Does every asynchronous request expose an honest in-progress, complete, and failed state?

## 14.7 Responsive and accessibility gate

- [ ] Does the mobile version preserve the same hierarchy rather than merely stack everything?
- [ ] Are all targets at least 44 px and reachable above safe areas and browser chrome?
- [ ] Does 200% text produce no overlap, clipping, or hidden action?
- [ ] Does the design work with the keyboard alone and with visible focus?
- [ ] Are colour and host accent never the only state cue?
- [ ] Is RTL handled at component level, including mixed target and native text?
- [ ] Are audio states, transcripts, captions, and text alternatives complete?
- [ ] Is reduced motion meaningful rather than just slower animation?

## 14.8 Completion gate

- [ ] Does the screen push another session, celebrate visually, or create obligation? If yes, reject.
- [ ] Does the completion feel socially and editorially finished?
- [ ] Does the final action return the user to ordinary life rather than keep them inside an engagement loop?

# 15. Design priorities and validation

## 15.1 Five most dangerous mistakes

1. Turning Today into a grid of generated content cards.
2. Making the Call-in look like a tutor, voice assistant, or speaking assessment.
3. Using personal data as visible recommendation evidence or surprise intimacy.
4. Allowing chat to remain open and companion-like after the show should end.
5. Decorating the product with AI clichés — glows, gradients, portraits, "magic" — instead of resolving hierarchy and media form.

## 15.2 Build order for design

1. **Today in three variants** (ordinary day, active session, Weekly Proof day) — establishes category and hierarchy.
2. **Episode player and synced transcript** — proves premium media quality and the Booth environment.
3. **Call-in in all live states plus voice-note recovery** — highest interaction and anxiety risk.
4. **Notes and Define** — proves editorial reading and invisible language support.
5. **After-show open, closing, final reply, and completed** — proves that conversation can end naturally.
6. **Pitch production sheet** — proves user control without prompt engineering.
7. **Intake and first-show handoff.**
8. **Archive, Cast, and Trust, including export and deletion.**
9. **Entry and account** — last among major flows, because it should inherit the product identity rather than define it.

## 15.3 Smallest high-fidelity prototype

Prototype one realistic cycle for one real user on mobile first, then validate the desktop Today composition.

**Sequence.** Arrive on Today with one high-confidence callback, one "Ready now" lead pitch, and two supporting pitches → open the lead pitch, change cast once, return to the prepared version → play a fully produced 5–7 minute episode with at least 60–90 seconds of accurate word-synced transcript and working Define → read a complete 250–450 word Notes article that genuinely changes the argument → join a live or human-operated Call-in where the host takes a position, pushes back, recasts once naturally, and responds within the perceived 1.5-second budget → end the call and receive a three-to-five-message After-show thread that visibly closes → reach "That's the show" without a next-session prompt.

**What must be real.** The episode title, script, audio, article, host stance, and personal callback, authored specifically for the test user; audio quality, mobile player controls, transcript readability, call entry, microphone permission, and the chat ending; the host responding to the user's actual position rather than a fixed branching script; the ability to leave and resume at least once.

**What may be simulated.** Planning, learner-file updates, assessment, the quality gate, archive persistence, and the generation pipeline; word definitions beyond the tested sample; call intelligence behind a realistic interface and latency; Weekly Proof as a separate high-fidelity screen.

**Pass condition.** Behavioural: the user wants the next episode because this episode was worth hearing, not because the prototype explained the vision.
