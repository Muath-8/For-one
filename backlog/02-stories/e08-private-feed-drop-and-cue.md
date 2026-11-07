# E08 · Private feed, drop and the one cue

*Architecture domains 06 and 01. Exactly three outbound message kinds exist: the drop, the one opt-in gap note, and the weekly proof. Nothing else is ever sent.*

### E08-S01 · A private podcast feed per learner
**As a** learner, **I want** a private RSS feed with my episodes, **so that** I can listen in Apple Podcasts or any podcast app with the phone locked.
- **Given** the feed token, **when** fetched by Apple Podcasts, Pocket Casts and one Android app, **then** the episode plays with the enclosure streamed and the fetch logged in `feed_fetches`.
- **Given** a reset of the token, **when** done from controls, **then** the old link stops working at once.
- Size: L · Priority: P0 · Week: W3 · Domain: 06 Client, 01 Topology · Depends on: E01-S08, E04-S06

### E08-S02 · Drop scheduling and the day's rule
**As a** learner, **I want** my episode ready before the time I chose, in my local time, and nothing made after a day I skipped, **so that** nothing piles up.
- **Given** an active day (half an episode played, a call started or the small door used), **when** the night runs, **then** tomorrow's episode is produced; otherwise nothing is.
- **Given** the drop minute, **when** 95% of the week's drops are checked, **then** they were ready before drop time.
- Size: M · Priority: P0 · Week: W3 · Domain: 01 Topology, 02 Pipeline · Depends on: E04-S07

### E08-S03 · Web push for the drop only
**As a** learner, **I want** one notification when the episode drops, and no other, **so that** the cue is mine.
- **Given** the push subscription, **when** the episode drops, **then** one push arrives; a test fails if any code path sends a push for another reason.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E08-S02

### E08-S04 · Salma's 5-second feed tag
**As a** learner, **I want** a 5-second tag from Salma in my own language at the start of each feed episode, **so that** the feed episode feels like mine.
- **Given** a published episode, **when** the feed item is built, **then** the tag is prepended and the timings shift accordingly.
- Size: S · Priority: P0 · Week: W3 · Domain: 02 Pipeline · Depends on: E08-S01

### E08-S05 · The one opt-in gap note
**As a** learner, **I want** to write one note to myself at signup that is sent once after a gap I chose (7, 10 or 14 days), **so that** the only reminder is in my own words.
- **Given** the gap, **when** reached, **then** the note is sent exactly once and never again; with no opt-in, nothing is sent.
- Size: S · Priority: P0 · Week: W5 · Domain: 01 Topology · Depends on: E08-S02

### E08-S06 · Return episode after a gap
**As a** learner, **I want** the first session after 5+ days to be a return episode, one step easier, opening from my life, **so that** coming back is easy and never guilty.
- **Given** 5 days without a session, **when** the learner opens the app or the feed, **then** the return kind is produced on demand within 30 s.
- Size: M · Priority: P0 · Week: W5 · Domain: 02 Pipeline · Depends on: E04-S08

### E08-S07 · Rhythm in words and re-anchoring
**As a** learner, **I want** my rhythm ("4 days, 2 spare") mentioned only in words by the hosts, and a re-anchoring offer when life has moved my cue, **so that** there is no counter and no guilt.
- **Given** no session within 3 hours of the anchor for two weeks, **when** detected, **then** Salma offers once to change the drop time, in the app only.
- Size: S · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E08-S02
