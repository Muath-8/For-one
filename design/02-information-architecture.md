# For one — 02. Information architecture and navigation

*Part 2 of 8. What exists, where it lives, and how the learner moves between places. Three destinations, a handful of sheets, and two full-screen modes (player, call) that hide the navigation.*

## 1. The map

```
For one
├── (before an account)
│   ├── Sample episode page (web only, shareable): one question, a 90-second episode, "Start your show"
│   └── Onboarding (03 flow A / A′): Open → Salma → word check (optional) → Casting → Pilot → First call → Keep your show
│
├── Today  ──────────────── the only screen most days
│   ├── Hero cover (today's episode)         → Player (full screen)
│   │     doors: Listen · Call · Read · Chat → Player · Call (full screen) · Read · Chat
│   ├── Why this episode?  (sheet)
│   ├── 2 other ideas      (sheet)            → swaps the hero
│   ├── Tell Salma an idea (hold-to-talk sheet)
│   ├── Small door         (quiet card)       → 90-second recap + one voice note
│   ├── Weekly proof cover (on proof day)     → Proof (full screen, audio + one screen)
│   ├── Season finale cover (every 4 weeks)   → Finale (then-and-now recording, the tape)
│   └── Done state: closing line, tomorrow's time, three ideas for tomorrow
│
├── Show  ──────────────── the shelf
│   ├── Seasons (rows of episode covers, newest first)
│   │     └── Episode → Player (re-listen is unlimited) · its article · its chat thread
│   ├── Proofs (one per week)
│   └── Finales (one per season)
│
└── Notebook  ──────────── Salma's file, open to the learner
    ├── Working on (≤ 3 items, each with ✕ and "add one")
    ├── About you (fact cards with quotes; ✎ ✕; "I think…" unconfirmed)
    ├── Words you own (the learner's sentences, with audio; kept words marked)
    ├── The tape (seasons, Play A then B)
    ├── Out in the world (real-world tries, dated)
    ├── Marked moments (from headphone "next" during episodes)
    ├── Hours (heard, spoken; cumulative, no goal)
    └── Controls (sheet)
         ├── Drop time and the drop notification
         ├── Rhythm (e.g. "4 days, 2 spare")
         ├── Captions on calls · transcript in the player · default speed
         ├── Keep my recordings (on/off) · delete all recordings
         ├── Theme (system / dark / light) · reading size
         ├── Plan (current plan, change, cancel in one tap)
         ├── Interface language
         ├── See, export, delete all my data
         └── Sign out
```

Everything not on this map is a sentence to Salma ("talk slower", "less football", "make Mona nicer", "I had the interview").

## 2. Destinations and what they are for

| Destination | Question it answers | Visual weight | Frequency |
|---|---|---|---|
| **Today** | What's on? | The hero takes 60% of the screen | Every visit |
| **Show** | What have we made together? | A shelf of covers, by season | Weekly |
| **Notebook** | What does the show know, and what can I now do? | A list in Salma's voice | Weekly to monthly, and whenever trust needs checking |

The tab bar is a three-item bar with text labels, no badges, no counts, no dots. It is hidden in the player, the call, the proof and the finale, which are modes, not places.

## 3. Modes (full screen, navigation hidden)

| Mode | Enter | Leave | Audio continues? |
|---|---|---|---|
| Player | Play on the hero; a cover on the shelf; lock screen | ⌄ collapses to a mini bar on Today/Show/Notebook | Yes; mini bar shows title, play/pause, replay line |
| Call | "Call" from the throw card or the door row; the lock screen "accept" on native | ✕ ends it like a person; host signs off | No (it is live) |
| Proof | Its cover on Today or Show | Done | Yes while on the one screen |
| Finale | Its cover; Salma invites | Done | Recording stops on ✕ with nothing lost |
| Onboarding | First open | Ends at Keep your show | n/a |

## 4. Navigation rules

1. **Back always means back.** No screen traps. The system back gesture and the ⌄ / ✕ do the same thing.
2. **Audio outlives screens.** Leaving the player leaves a mini bar; closing the app keeps playing (native) or keeps playing while the tab lives (web, Media Session).
3. **Deep links** exist for: today, a specific episode, the call for today's episode (used by the podcast feed's episode notes: "open For one to call in"), the proof, the notebook, plans, and the sample page.
4. **Nothing pulls the learner anywhere.** No in-app banners, no "you have 1 new", no upsell interstitials. The only pull is the one cue the learner designed (the drop) and the one note they wrote to themselves.
5. **State is per day, not per session.** Today's doors remember what is done until midnight local time. An unfinished episode moves to the shelf at the next drop and stays playable forever.
6. **The plan allowance lives in words on Today**, not as a meter: "You can have one more episode today" / "That's two today. Tomorrow's is ready at 7:40."

## 5. The private podcast feed (companion surface)

A per-learner RSS feed (unguessable URL, revocable in Controls) carries each episode's audio and cover. Its episode notes hold one line and a deep link: "Karim wants your take. Open For one to call in." The feed is for the Ears mode on commutes; the call, the article, the chat and the notebook live only in the app. The proof episode is also in the feed. On web-for-beta, this feed is what makes lock-screen play reliable on iPhone.

## 6. Web vs native: what changes in the architecture (open decision 7, both designed)

| | Web app (PWA) + feed | Native app (one codebase) |
|---|---|---|
| Today, Show, Notebook, Read, Chat, plans | Identical | Identical |
| Player | Foreground or background via Media Session; lock-screen artwork and replay/mark actions where the browser supports them; the feed covers the rest | Full Now Playing, CarPlay/Android Auto, headphone actions guaranteed |
| Call | Screen on, earphones recommended; a "keep the screen on" hint before the call; the call pauses if the tab is backgrounded and resumes on return (host: "you still there?") | Hands-free, screen off, accept from the lock screen like a phone call |
| Drop notification | Web push on installed PWAs; the feed's own new-episode alert | Local notification at the chosen time |
| Checkout | Web checkout (Stripe-style), keeps ~96% | In-app purchase required for digital goods on iOS (~85%), or web checkout with store rules respected |
| Install | "Add to home screen" shown once after the first call, with a two-step picture | App Store / Play |
| Offline | Today's episode cached after first play; the notebook cached read-only | Same, plus prefetch at the drop time |

The screens are designed so that the native build adds capabilities and removes hints (the "keep the screen on" hint disappears, the install card disappears); nothing is laid out differently.

## 7. First-session order: two architectures (open, both designed)

- **Order A (recommended by the UI lens and concept v2):** Open → Salma (3 min) → Casting → Pilot → First call → Keep your show (account, drop time, consent, trial). Sound in under 60 seconds; the account comes after there is something to keep.
- **Order B (PRD order):** Open → Account → Languages → Salma → Pilot → First call → Drop time and consent. The account first; useful if abandoned sessions with no account turn out to be costly, or if the store requires sign-in before purchase.

03-user-flows.md specifies both; 04 screens are shared, only the sequence differs. The onboarding screens are built as independent steps with a configurable order so the pilot can A/B them.

## 8. Object model (what the screens are made of)

| Object | Fields the UI shows | Where |
|---|---|---|
| Show | hosts (2), producer, hue, season list, rhythm, drop time | Today, Show, Controls |
| Season | number, title (Salma's), start/end dates, goal (learner's words), finale | Show, Notebook › tape |
| Episode | title, cover seed, length, doors (listen, call, read, chat) with done flags, "why" (3 to 4 lines), transcript with word timings, article, chat thread, kind (regular · small door · return · rehearsal · proof · finale) | Today, Player, Show |
| Call | host, duration, learner speech seconds, retell flag; nothing else is shown | Call screen header; Notebook › hours |
| Fact | text, quote, date said, confidence (confirmed / I think), sensitivity flag | Notebook › about you; onboarding cards |
| Word (owned / kept) | lemma, gloss, the learner's sentence, audio, date | Word sheet, Notebook › words |
| Working-on item | plain-words description, why (one line), veto | Notebook › working on |
| Proof | week, headline claim, clip pair, "how we know", next focus, kind (good · flat · slow) | Proof screen |
| Recording (tape) | season, length, audio; measured differences in plain words (≤ 2) | Finale, Notebook › tape |
| World entry | text, date, source quote | Notebook › out in the world |
| Plan | tier, price, episodes a day, trial end, founding flag | Plans, Controls |
