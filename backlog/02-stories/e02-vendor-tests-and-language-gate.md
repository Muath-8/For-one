# E02 · Vendor tests and the language gate

*Architecture domains 02 (pipeline), 03 (live call), 08 (cost and vendors). The tests use the 30 consented Milestone 0 learner clips, Muath's hand tags and the pilot scripts. The recognizer test runs during Milestone 0 (by 2026-11-10) and the voice decision is committed to `vendors.yaml` by 2026-11-17 (architecture 10 §6); the 50-call result completes the file by 27 November. E02-S01, S02, S03 and S06 are Muath's time, not engineering time (release plan §6).*

### E02-S01 · Consent addendum Part 1 before any clip leaves
**As an** operator, **I want** every Milestone 0 learner whose clips are used in vendor tests to have signed Part 1 of the addendum, naming the vendors, **so that** the tests do not break the promise the pilot made (ADR-24.B10).
- **Given** a clip in the test set, **when** the vendor-lab CLI runs, **then** it refuses any clip whose learner has no Part 1 on file and any vendor whose register row is `blocked`.
- **Given** a clip that already went to a vendor without Part 1, **when** found, **then** it is listed for counsel (question A-10 in the question pack) and not used again until counsel answers.
- Size: S · Priority: P0 · Week: M0 · Due: Day-1 · Domain: 07 Security · Depends on: E13-S03
- Requirements: FR-862, FR-1051

### E02-S02 · Recognizer test on 30 learner clips
**As an** operator, **I want** the 30 clips run through Soniox, Deepgram, AssemblyAI and ElevenLabs Scribe with the hand tags, **so that** the streaming and verbatim vendors are chosen on whether they keep learner errors.
- **Given** a clip with tagged errors, **when** each vendor transcribes it, **then** the sheet records, per vendor, the share of tagged errors kept verbatim, the share of own-language words caught, and latency.
- **Given** the sheet, **when** a vendor keeps fewer than 90% of tagged errors, **then** it cannot be the verbatim vendor for English.
- Size: M · Priority: P0 · Week: M0 · Due: Day-1 · Domain: 03 Live call · Depends on: E02-S01, E14-S02
- Requirements: FR-862, FR-1101, FR-1331, NFR-504

### E02-S03 · Blind two-host voice test
**As an** operator, **I want** the same two-host script and the Salma script rendered on Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4 and rated blind by 10 listeners as episode voice and call voice together, **so that** the voice vendor is the one people would listen to.
- **Given** the playlists, **when** 10 raters finish, **then** the decision CLI outputs a winner and a runner-up per language with the rating spread.
- **Given** the winner, **when** its streaming first-byte latency is measured, **then** it is under 300 ms or the runner-up carries the call voice.
- Size: M · Priority: P0 · Week: M0 · Due: Day-1 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E02-S01, E14-S02
- Requirements: FR-502, FR-524, FR-1101, FR-1324, FR-1330

### E02-S04 · Fifty scripted calls for latency
**As an** operator, **I want** 50 scripted calls from Milestone 0 audio run against the minimal call-worker in both worker placements, **so that** the host's reply latency is measured before any learner calls.
- **Given** the 50 calls, **when** `tools/call-bench` finishes, **then** `reply_latency_ms` median is under 1,500 and p95 under 2,500, and `silence_to_sound_ms` is recorded per vendor pair.
- Size: M · Priority: P0 · Week: Phase 2 · Due: Day-1 · Domain: 03 Live call · Depends on: E05-S01, E02-S02
- Requirements: FR-1101, FR-1332, NFR-107

### E02-S05 · Vendors frozen and adapters for the winners only
**As an** engineer, **I want** `vendors.yaml` committed with the voice winners by 17 November and complete (with the 50-call result) by 27 November, and thin adapters (`llm`, `tts`, `asr`, `align`, `embed`) only for the winning and secondary vendors, **so that** nothing in week 3 is built on an untested vendor.
- **Given** a role, **when** code requests a vendor, **then** it goes through the adapter and the tracing middleware, never a vendor SDK directly (a lint rule fails otherwise).
- **Given** the primary voice vendor's key is revoked for an hour, **when** production runs, **then** the secondary carries the same day's production.
- Size: L · Priority: P0 · Week: Phase 2 · Due: Day-1 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E02-S02, E02-S03, E02-S04
- Requirements: FR-1322, FR-1326, NFR-203

### E02-S06 · English language package v1
**As a** teacher role, **I want** an English package with word frequency ranks (wordfreq; no SUBTLEX licence), a lemmatizer, a chunk list of about 300 formulaic sequences, the structure inventory (about 120 structures in Phase 1, a few hundred by Phase 3, built from open sources with English Grammar Profile-style ids, not waiting for the EGP licence, ADR-24.18), a ban list of stock names and tropes, and name rules, **so that** coverage, targeting and classification run on real data.
- **Given** the 10 hand-checked pilot scripts, **when** the coverage check runs, **then** its known-word percentage matches the pilot checker within 0.5 points.
- **Given** English as the only target in the beta (ADR-24.20), **when** the package is marked shippable, **then** the Milestone 0 `vendor-lab gate --target en` result for all five gate checks (voices, recognizers, native read of 10 scripts, call latency, inventory present) is attached to it and linked from the release manifest.
- Size: L · Priority: P0 · Week: Phase 1 · Due: Day-1 · Domain: 02 Generation pipeline, 05 Assessment · Depends on: none
- Requirements: FR-002, FR-431, FR-815, FR-1100, FR-1101, FR-1103, FR-1105, FR-1106, FR-1110

### E02-S07 · The drafted bibles versioned in the packages
**As a** writer role, **I want** the bibles drafted in `content/bibles/` (Karim, Mona and the default world in `lang/en`; Salma and her strings in `native/ar` and `native/en`) versioned inside the packages, **so that** a bible change is a release and the characters stay written by people (ADR-24.3).
- **Given** a bible change, **when** it is merged, **then** the release manifest records the version and the eval gate runs the writer and host suites.
- **Given** the native English editor's read of the hosts' bible and 30 sample lines per host, and Muath's read of Salma's Arabic, both by 2026-12-01 (register A4, A5), **when** a package version is marked shippable, **then** it records the read and its date; an unread `native/ar` does not ship and `native/en` ships alone.
- Size: M · Priority: P0 · Week: Phase 2 · Due: Day-1 · Domain: 02 Generation pipeline · Depends on: E02-S06; the native read of the drafts by 2026-12-01 (A4, A5)
- Requirements: FR-434, FR-435, FR-501, FR-520, FR-1102, FR-1104, NFR-206, NFR-605

### E02-S08 · The language gate as a runnable harness
**As an** operator, **I want** the five gate checks (blind voice rating, 30-clip recognizer test, native read of 10 scripts, call latency, structure inventory present) as jobs with a one-page result per language, **so that** a new language opens by passing a test, not by a vendor's list.
- **Given** a candidate language, **when** the harness runs with its clips, raters and scripts, **then** it outputs pass or fail per check and refuses to mark the package shippable unless all five pass.
- Size: M · Priority: P1 · Week: Beta · Domain: 02 Generation pipeline, 09 Operations · Depends on: E02-S05, E02-S06
- Requirements: FR-1101, FR-1102, FR-1107, NFR-605

### E02-S09 · Second-language dry run through the gate
**As an** operator, **I want** one large candidate language (for example Spanish) run through the harness during the beta, **so that** we know how long a language takes and what breaks before the public launch.
- **Given** the dry run, **when** it finishes, **then** a report lists each check's result, the cost, the days taken and the native-speaker time used.
- Size: M · Priority: P1 · Week: Beta · Domain: 02 Generation pipeline · Depends on: E02-S08
- Requirements: FR-1105, FR-1107, FR-1110
