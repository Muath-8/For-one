# E07 · The daily loop in the web app

*Architecture domain 06. An installable web app (Next.js PWA on Vercel) with three tabs and four doors, in the learner's own language. Assumes the web-plus-feed platform decision (blocking item B1).*

### E07-S01 · Web shell: PWA, bidi, tokens, law lint
**As a** learner, **I want** an app that installs, reads right in my language's direction, and has no counter, streak, chart or percent component anywhere, **so that** the laws are enforced by the build.
- **Given** a component named or rendering a streak, level, percentage or chart, **when** lint runs, **then** the build fails.
- **Given** Arabic interface text quoting English, **when** rendered, **then** the bidi snapshot suite passes.
- Size: L · Priority: P0 · Week: W1 · Domain: 06 Client · Depends on: E01-S03

### E07-S02 · Email-code auth and sessions
**As a** learner, **I want** to sign in with a code sent to my email and stay signed in on my phone, **so that** there is no password to forget.
- **Given** a code, **when** used twice or after 10 minutes, **then** it is refused.
- Size: S · Priority: P0 · Week: W2 · Domain: 06 Client, 07 Security · Depends on: E07-S01

### E07-S03 · The player
**As a** learner, **I want** audio first with the transcript folded, a replay-line button, "Huh?" that replays the last sentence at 0.85x with meanings under hard words, speeds of 0.75, 0.85 and 1.0, and tap any word to hear and keep it, **so that** I can follow at the edge of what I understand.
- **Given** a dropped episode, **when** Play is tapped, **then** sound starts under 2 s from cache or network fallback.
- **Given** "Huh?", **when** tapped, **then** the previous sentence replays slower and the gloss appears; the event is logged.
- **Given** the phone locks, **when** playing, **then** Media Session keeps playback and lock-screen controls on iOS 17 and 18 and Android 13 and 14.
- Size: L · Priority: P0 · Week: W2 · Domain: 06 Client · Depends on: E07-S01, E04-S06

### E07-S04 · Event queue to the api
**As a** teacher role, **I want** every play, huh, tap, keep and scroll event queued on the device and sent in order, **so that** the model sees the session even on a bad connection.
- **Given** an api outage, **when** events accumulate, **then** they are sent in order when the api returns with no duplicates.
- Size: M · Priority: P0 · Week: W2 · Domain: 06 Client · Depends on: E03-S01

### E07-S05 · Today in every state
**As a** learner, **I want** Today to show one thing: my episode, with the four doors, "why this episode?", and the small door, in the right state (dropped, played, skipped yesterday, return, trial ended), **so that** opening the app means pressing play.
- **Given** a skipped day, **when** Today opens, **then** nothing new is shown, nothing piles up, and no reminder was sent.
- **Given** the return state, **when** Today opens, **then** the return episode is the hero and the days missed are never mentioned.
- Size: L · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E07-S03, E08-S02

### E07-S06 · Read: the article with read-along audio
**As a** learner, **I want** the article that arms me for the call, at my level, with audio to read along, **so that** reading and listening happen together.
- **Given** the article, **when** opened, **then** the word sheet opens under 300 ms on tap and the scroll depth is logged.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E04-S02, E07-S03

### E07-S07 · The call screen
**As a** learner, **I want** a call screen with the host's orb, sentence captions, hold-to-talk, the word button, a planning card for 30 seconds before the call and the voice-note fallback, **so that** the call works with earphones on a bus.
- **Given** the call connects, **when** captions arrive on the data channel, **then** they show per sentence with the recast word in bold and no correction mark.
- **Given** the feed-to-call handoff, **when** measured, **then** the time from tapping the push to the host's first line is logged.
- Size: L · Priority: P0 · Week: W4 · Domain: 06 Client, 03 Live call · Depends on: E05-S06, E05-S10

### E07-S08 · Chat and choosing tomorrow
**As a** learner, **I want** a short chat with the host (3 to 5 messages) that ends with three ideas for tomorrow and "tell Salma an idea", **so that** I choose tonight and have nothing to decide in the morning.
- **Given** the fifth host message, **when** sent, **then** the thread closes with the three ideas and a clean goodbye.
- **Given** "why do we say it like that?", **when** asked, **then** the host explains, because the learner asked, and no explanation appears otherwise.
- Size: M · Priority: P0 · Week: W4 · Domain: 06 Client · Depends on: E04-S09, E07-S05

### E07-S09 · One swap a day
**As a** learner, **I want** to swap the dropped episode for another idea once a day, **so that** a dud never costs me the day.
- **Given** a swap, **when** requested, **then** the new episode streams under 30 s and a second swap is not offered.
- Size: S · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E04-S08

### E07-S10 · The small door
**As a** learner, **I want** a 90-second recap and one voice note up to 60 s on a bad day, **so that** a bad day still counts fully.
- **Given** the small door used, **when** the day closes, **then** it counts as an active day and the next episode is made.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E04-S08, E05-S12

### E07-S11 · Show shelf and the episode page
**As a** learner, **I want** every past episode reachable and replayable without limit, **so that** listening to what exists is free on every plan.
- **Given** the Show tab, **when** opened, **then** episodes list newest first with no count, no completion marks and no progress bar.
- Size: M · Priority: P0 (may slip to beta week 1) · Week: W3 · Domain: 06 Client · Depends on: E07-S03

### E07-S12 · Accessibility, performance and the device matrix
**As a** learner on a mid-range Android, **I want** the app to be fast and usable with a screen reader, **so that** the product is not only for new iPhones.
- **Given** Lighthouse on a mid-range Android, **when** run, **then** performance is above 85 and the bundle is under the budget.
- **Given** the week-3 device matrix, **when** run, **then** background play, push and install pass on iOS 17 and 18 and Android 13 and 14 Chrome.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E07-S03, E08-S03
