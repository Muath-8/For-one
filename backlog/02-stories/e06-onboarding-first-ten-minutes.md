# E06 · Onboarding: the first ten minutes

*Architecture domain 06 (client), with 03 (Salma's call) and 07 (consent and age gate). Budgets: first sound under 60 s, pilot playable under 45 s after intake, first spoken sentence under 5 minutes. The A4 to A7 order is the open "first-session order" decision; the stories assume the recommended order: Salma talk, optional word check, casting while the pilot is made, pilot, first call, account.*

### E06-S01 · Sample episode and landing page
**As a** visitor, **I want** a free 90-second sample about something I type, playable within 30 seconds, **so that** I hear the product before signing up.
- **Given** a topic, **when** submitted with a Turnstile pass, **then** a streamed sample starts under 30 s, costs under $0.05, and the same device or email cannot request another for 24 hours.
- **Given** a sample, **when** shared, **then** the share page plays it and shows where the signup is.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client, 02 Pipeline · Depends on: E04-S08

### E06-S02 · Waitlist and invites
**As an** operator, **I want** a waitlist loaded from the Milestone 0 sign-ups and invite batches of about 50 a week, **so that** the beta opens in cohorts.
- **Given** an invite code, **when** redeemed, **then** onboarding starts; an unredeemed or used code shows the waitlist.
- Size: S · Priority: P0 · Week: W3 · Domain: 06 Client, 01 Topology · Depends on: E01-S03

### E06-S03 · A1: sound within a minute
**As a** learner, **I want** one screen, one tap and an age checkbox, then Salma's voice in my own language, **so that** I hear the product before I read about it.
- **Given** a first open, **when** the tap happens, **then** Salma's first clip plays within 60 s on a 4G phone and the screen's text is in the learner's language with right-to-left handled.
- **Given** the age box unticked or under 18, **when** continuing, **then** the flow stops with a plain message and nothing is stored.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E07-S01, E13-S04

### E06-S04 · A3: three minutes with Salma, with fact cards
**As a** learner, **I want** to talk or type with Salma for about 3 minutes and see each fact she heard as a card I can fix or delete, **so that** the show starts from what I said, not what it guessed.
- **Given** a card, **when** I edit or delete it, **then** the stored fact changes before the pilot is written.
- **Given** the typed path, **when** the call cannot connect, **then** the same questions run as text with no loss.
- Size: L · Priority: P0 · Week: W3 · Domain: 06 Client, 03 Live call · Depends on: E05-S04, E03-S04

### E06-S05 · A4: the optional word check
**As a** learner, **I want** an optional 60-second "tap the words you know" with Skip as big as Start, **so that** the show pitches at my level without a test.
- **Given** 48 items, **when** 75 s pass, **then** the check stops and scores what was answered.
- **Given** Skip, **when** tapped, **then** the level comes from Salma's two target-language lines and the band prior.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E03-S07

### E06-S06 · A5: casting while the pilot is made
**As a** learner, **I want** to hear each host say hello, swap a voice and pick an accent during the 40 to 90 seconds the pilot takes, **so that** the wait is the cast.
- **Given** the pilot is still rendering, **when** casting ends early, **then** the screen shows the hosts talking about the topic, never a spinner or a percentage.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E04-S10

### E06-S07 · A6 and A7: the pilot and the first call
**As a** learner, **I want** a 2 to 3 minute pilot about my topic, then a 60 to 90 second first call, with Mona telling me once about the word button, **so that** I speak in the first five minutes.
- **Given** intake completed, **when** the pilot is requested, **then** playback starts within 45 s.
- **Given** the pilot ends, **when** Karim throws a question, **then** the first call connects within 3 s and runs with no recasts.
- Size: L · Priority: P0 · Week: W3 · Domain: 06 Client, 03 Live call · Depends on: E04-S08, E05-S05

### E06-S08 · A8 and A9: one win, then the account
**As a** learner, **I want** to hear one specific thing I managed, then make the account with an email code, pick my drop time in life terms and answer voice-storage consent in one plain sentence, **so that** I decide after I have heard myself.
- **Given** the account step, **when** completed, **then** the pre-account learner id is re-keyed, the 7-day trial starts on 2 a day, and no card is asked.
- **Given** consent declined, **when** saved, **then** call audio is analysed and deleted within 15 minutes from then on.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client, 07 Security · Depends on: E13-S03, E12-S03

### E06-S09 · A10: install card and the feed handoff
**As a** learner, **I want** an install card and a one-tap link that puts my private feed in my podcast app, **so that** tomorrow's episode arrives where I already listen.
- **Given** the handoff, **when** tapped on iOS and Android, **then** the feed subscribes in the chosen app and the installed app signs in without a second email code.
- Size: M · Priority: P0 · Week: W3 · Domain: 06 Client · Depends on: E08-S01

### E06-S10 · Apple and Google sign-in
**As a** learner, **I want** to sign in with Apple or Google, **so that** I do not need an email code every time.
- **Given** the developer accounts are approved, **when** sign-in runs, **then** the Apple relay email is accepted as the account email.
- Size: M · Priority: P1 · Week: Beta · Domain: 06 Client · Depends on: Apple Developer approval

### E06-S11 · Re-onboard the Milestone 0 learners
**As an** operator, **I want** the 15 pilot learners to go through A1 to A10 on production under the beta consent, with their pilot recordings as the "then" baseline where they consented, **so that** the exit numbers come from real people.
- **Given** a pilot learner, **when** re-onboarded, **then** first sound, pilot time and first spoken sentence are measured and their imported model is linked to the new account.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E06-S03 to E06-S09, E13-S03
