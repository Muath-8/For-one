# E08 · Private feed, drop and the one cue

*Architecture domains 06 and 01. Exactly three kinds of message ever leave the product (FR-240): the drop notification, the one opt-in gap note, and transactional email (sign-in code, receipts, the day-6 trial email, payment failed, export ready, account deleted). The weekly proof is not a message: it sits on Today and in the feed. Nothing else is ever sent.*

### E08-S01 · A private podcast feed per learner
**As a** learner, **I want** a private RSS feed with my episodes, **so that** I can listen in Apple Podcasts or any podcast app with the phone locked.
- **Given** the feed token, **when** fetched by Apple Podcasts, Pocket Casts and one Android app, **then** the episode plays with the enclosure streamed and the fetch logged in `feed_fetches`.
- **Given** a reset of the token, **when** done from controls, **then** the old link stops working at once.
- **Given** past episodes, **when** the feed is fetched, **then** every episode stays in it with its article link in the notes, so Listen and Read stay available for good even before the Show tab ships.
- Size: L · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client, 01 Topology · Depends on: E01-S08, E04-S06
- Requirements: FR-009, FR-232, FR-233, FR-306, NFR-305

### E08-S02 · Drop scheduling and the day's rule
**As a** learner, **I want** my episode ready before the time I chose, in my local time, and nothing made after a day I skipped, **so that** nothing piles up.
- **Given** an active day (half an episode played, a call started or the small door used), **when** the night runs, **then** tomorrow's episode is produced; otherwise nothing is.
- **Given** the drop minute, **when** 95% of the week's drops are checked, **then** they were ready before drop time.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 01 Topology, 02 Pipeline · Depends on: E04-S07
- Requirements: FR-206, FR-207, FR-230, FR-231, NFR-113

### E08-S03 · Web push for the drop only
**As a** learner, **I want** one notification when the episode drops, and no other, **so that** the cue is mine.
- **Given** the push subscription, **when** the episode drops, **then** one push arrives with the title and length only; a test fails if any code path sends a push or an email outside the three kinds.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client · Depends on: E08-S02
- Requirements: FR-008, FR-232, FR-240

### E08-S04 · The 5-second feed tag and the notes links
**As a** learner, **I want** each feed episode to end with a 5-second line from the host ("To call me, open the link in the notes") and the item's notes to carry the call and article links, **so that** the podcast app leads me to the call.
- **Given** a published episode, **when** the feed item is built, **then** the cached tag is appended, the notes carry the call link and the article link, and the app version is unchanged.
- Size: S · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 02 Pipeline · Depends on: E08-S01
- Requirements: FR-233

### E08-S05 · The one opt-in gap note
**As a** learner, **I want** to write one note to myself at signup that is sent once after a gap I chose (7, 10 or 14 days), **so that** the only reminder is in my own words.
- **Given** the gap, **when** reached, **then** the note is sent exactly once and never again; with no opt-in, nothing is sent.
- Size: S · Priority: P0 · Phase: Phase 5 · Release: v1 · Domain: 01 Topology · Depends on: E08-S02
- Requirements: FR-211, FR-240

### E08-S06 · Return episode after a gap
**As a** learner, **I want** the first session after 5+ days to be a return episode, one step easier, opening from my life, **so that** coming back is easy and never guilty.
- **Given** 5 days without a session, **when** the learner opens the app or the feed, **then** the return kind is produced on demand within 30 s.
- Size: M · Priority: P0 · Phase: Phase 5 · Release: v1 · Domain: 02 Pipeline · Depends on: E04-S08
- Requirements: FR-212, FR-213, FR-214

### E08-S07 · Rhythm in words and re-anchoring
**As a** learner, **I want** my rhythm ("4 days, 2 spare") mentioned only in words by the hosts, and a re-anchoring offer when life has moved my cue, **so that** there is no counter and no guilt.
- **Given** no session within 3 hours of the anchor for two weeks, **when** detected, **then** Salma offers once to change the drop time, in the app only.
- Size: S · Priority: P0 · Phase: Phase 5 · Release: v1 · Domain: 06 Client · Depends on: E08-S02
- Requirements: FR-220, FR-223, FR-224, FR-225
