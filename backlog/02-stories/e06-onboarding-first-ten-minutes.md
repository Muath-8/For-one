# E06 · Onboarding: the first ten minutes

*Architecture domain 06 (client), with 03 (Salma's call) and 07 (consent and age gate). Budgets: first sound under 60 s, first episode playable under 45 s after intake, first spoken sentence under 5 minutes. The order is decided (order A, ADR-24.2): Salma talk, optional word check, casting while the first episode is made, the first episode, the first call, then the account. After launch, the word check's position may be A/B tested (after the first call); nothing else is tested.*

### E06-S01 · The sample episode on the landing page
**As a** visitor, **I want** a free 90-second sample about something I type, playable within 30 seconds, as a second route from the landing page into onboarding, **so that** I hear the product before starting.
- **Given** a topic, **when** submitted with a Turnstile pass, **then** a streamed sample starts under 30 s, costs under $0.05, and the same device or email cannot request another for 24 hours.
- **Given** a sample, **when** the visitor keeps it, **then** it is a plain download link (the share page is cut under the v1 cut list) and nothing is shared automatically.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 06 Client, 02 Pipeline · Depends on: E04-S08
- Requirements: FR-007, FR-102, FR-103, FR-104, NFR-103, NFR-406

### E06-S02 · Open signup from the landing page
**As a** visitor, **I want** to start from the landing page with nothing to wait for, **so that** the show is open to anyone 18 or older, anywhere (ADR-25.5).
- **Given** the plain landing page in the visitor's language (browser language, with a picker), **when** "Start your show" is tapped, **then** onboarding opens at A1; there is no invite code and no waitlist.
- **Given** abuse limits, **when** the same device or network starts onboarding again and again, **then** Turnstile and per-device limits slow it, and a country Paddle cannot sell into is refused at checkout, not at signup.
- Size: S · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client, 01 Topology · Depends on: E01-S03
- Requirements: FR-004, FR-101

### E06-S03 · A1: sound within a minute
**As a** learner, **I want** one screen, one tap and an age checkbox, then Salma's voice in my own language, **so that** I hear the product before I read about it.
- **Given** a first open, **when** the tap happens, **then** Salma's first clip plays within 60 s on a 4G phone and the screen's text is in the learner's language with right-to-left handled.
- **Given** the age box unticked or under 18, **when** continuing, **then** the flow stops with a plain message and nothing is stored.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client · Depends on: E07-S01, E13-S04
- Requirements: FR-003, FR-010, FR-110, NFR-101

### E06-S04 · A3: three minutes with Salma, with fact cards
**As a** learner, **I want** to talk or type with Salma for about 3 minutes and see each fact she heard as a card I can fix or delete, **so that** the show starts from what I said, not what it guessed.
- **Given** a card, **when** I edit or delete it, **then** the stored fact changes before the first episode is written.
- **Given** the typed path, **when** the call cannot connect, **then** the same questions run as text with no loss.
- **Given** the A2 primer, **when** shown, **then** Talk asks for the microphone only at that moment and Type never asks for it, and the primer carries the notice line "Salma is an AI. Your voice is used only to run this talk and build your show; nothing is kept unless you make an account. Privacy notice." with a link to the notice; pre-account voice follows the 15-minute rule (ADR-24.B14).
- **Given** a native language whose "you" is gendered (Arabic first), **when** A3 runs, **then** an optional address-form chip offers masculine, feminine or neutral wording, neutral by default, never inferred, stored as `learners.address_form` (ADR-24.B26).
- Size: L · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client, 03 Live call · Depends on: E05-S04, E03-S04
- Requirements: FR-111, FR-112, FR-122

### E06-S05 · A4: the optional word check
**As a** learner, **I want** an optional 60-second "tap the words you know" with Skip as big as Start, **so that** the show pitches at my level without a test.
- **Given** 48 items, **when** 75 s pass, **then** the check stops and scores what was answered.
- **Given** Skip, **when** tapped, **then** the level comes from Salma's two target-language lines and the band prior.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client · Depends on: E03-S07
- Requirements: FR-113, FR-850

### E06-S06 · A5: casting while the first episode is made
**As a** learner, **I want** to hear each host say hello, swap a voice and pick an accent during the 40 to 90 seconds the first episode takes, **so that** the wait is the cast.
- **Given** the first episode is still rendering, **when** casting ends early, **then** the screen shows the hosts talking about the topic, never a spinner or a percentage.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client · Depends on: E04-S10
- Requirements: FR-114

### E06-S07 · A6 and A7: the first episode and the first call
**As a** learner, **I want** a 2 to 3 minute first episode about my topic, then a 60 to 90 second first call, with Mona telling me once about the word button, **so that** I speak in the first five minutes.
- **Given** intake completed, **when** the first episode is requested, **then** playback starts within 45 s.
- **Given** the first episode ends, **when** Karim throws a question, **then** the first call connects within 3 s and runs with no recasts.
- Size: L · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client, 03 Live call · Depends on: E04-S08, E05-S05
- Requirements: FR-115, FR-116, FR-120, NFR-102, NFR-104

### E06-S08 · A8 and A9: one win, then the account
**As a** learner, **I want** to hear one specific thing I managed, then make the account with an email code, pick my drop time in life terms and answer voice-storage consent in one plain sentence, **so that** I decide after I have heard myself.
- **Given** the account step, **when** completed, **then** the pre-account learner id is re-keyed, the birth date is asked (under 18 refused with a plain message), the drop time is set in life terms as the anchor, the 7-day trial starts on 2 a day, and no card is asked.
- **Given** consent declined, **when** saved, **then** call audio is analysed and deleted within 15 minutes from then on.
- **Given** A9, **when** shown, **then** the terms are accepted as their own consent kind with the version (ADR-24.B18), the trial line reads "Your 7-day trial is on 2 episodes a day. No card needed. On day 7 you choose a plan." (ADR-24.B27), an explicit consent to process what the learner says in calls and chats is recorded as its own kind `special_category` with its version and no account is created without it (ADR-25.9), and the research opt-in is not asked: it lives in Controls only, off by default (ADR-24.B6).
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client, 07 Security · Depends on: E13-S03, E12-S03
- Requirements: FR-003, FR-117, FR-118, FR-220, FR-1049, FR-1201

### E06-S09 · A10: install card and the feed handoff
**As a** learner, **I want** an install card and a one-tap link that puts my private feed in my podcast app, **so that** tomorrow's episode arrives where I already listen.
- **Given** the handoff, **when** tapped on iOS and Android, **then** the feed subscribes in the chosen app; the installed home-screen app asks for one email code, because the signed-in handoff is cut under the v1 cut list.
- Size: M · Priority: P0 · Phase: Phase 3 · Release: v1 · Domain: 06 Client · Depends on: E08-S01
- Requirements: FR-009, FR-119

### E06-S11 · The launch rehearsal on production
**As an** operator, **I want** Muath and a few volunteers to go through A1 to A10 and a first week of sessions on production before launch, **so that** the budgets are measured on real phones and real voices.
- **Given** a rehearsal run, **when** it ends, **then** first sound, first-episode time and first spoken sentence are measured for each person, and their accounts are deleted through the normal deletion path afterwards.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 06 Client · Depends on: E06-S03 to E06-S09, E13-S03
- Requirements: FR-120, NFR-101, NFR-102, NFR-104

### E06-S12 · Week one: one personal question per session
**As a** learner, **I want** the show to ask me at most one personal question per session in my first week, in a sensible order, **so that** it gets to know me without an interview.
- **Given** session 2, **when** the chat ends, **then** Salma asks for the weekly rhythm (3 to 6 days plus 2 spare) and no other personal question is asked in that session.
- **Given** sessions 2 to 5, **when** the next question is due, **then** it follows the order rhythm, the first then-and-now recording ("the opening tape of your season"), the season goal proposed from the intake, the note to the future self; a question already answered, skipped twice, or whose screen has not shipped yet is passed over and offered at the next session after it ships.
- **Given** the first two weeks, **when** the hosts ask about people, past attempts, interests or dated events, **then** each answer becomes a candidate fact only, through the memory keeper.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 04 Learner model, 06 Client · Depends on: E04-S01, E09-S05
- Requirements: FR-126, FR-211, FR-223, FR-556, FR-852
