# E02 · Vendor tests and the language gate

*Architecture domains 02 (pipeline), 03 (live call), 08 (cost and vendors). There is no trial run before launch (ADR-25.5): the tests use an open corpus with a commercial-use licence (speechocean762, Apache-2.0), about 30 clips recorded by volunteers from at least two native-language groups, and scripted calls and scripts the agent generates (ADR-25.6). E02-S01, S02, S03 and S06 are largely Muath's work (register A2, A3).*

### E02-S01 · Volunteer clips and the open corpus, with consent
**As an** operator, **I want** about 30 learner clips recorded by volunteers from at least two native-language groups, each with a one-line recording consent naming the vendors, plus the speechocean762 corpus under its Apache-2.0 licence, **so that** the vendor tests run on real learner speech without a trial run (ADR-25.6, register A2).
- **Given** a clip in the test set, **when** the vendor-lab CLI runs, **then** it refuses any clip with no consent record or licence on file and any vendor whose register row is `blocked`.
- **Given** a volunteer who withdraws, **when** recorded, **then** their clips are deleted from the test set and from any vendor that kept them.
- Size: S · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 07 Security · Depends on: E13-S02
- Requirements: FR-862, FR-1051

### E02-S02 · Recognizer test on the volunteer clips and the corpus
**As an** operator, **I want** the volunteer clips and a speechocean762 sample run through Soniox, Deepgram, AssemblyAI and ElevenLabs Scribe, **so that** the streaming and verbatim vendors are chosen on whether they keep learner errors.
- **Given** a clip with tagged errors (Muath tags the volunteer clips; the corpus brings its own annotations), **when** each vendor transcribes it, **then** the sheet records, per vendor, the share of tagged errors kept verbatim, the share of own-language words caught, and latency.
- **Given** the sheet, **when** a vendor keeps fewer than 90% of tagged errors, **then** it cannot be the verbatim vendor for English.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 03 Live call · Depends on: E02-S01, E14-S02
- Requirements: FR-862, FR-1101, FR-1331, NFR-504

### E02-S03 · Blind two-host voice test
**As an** operator, **I want** the same two-host script and the Salma script rendered on Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4 and rated blind by Muath and a few volunteers as episode voice and call voice together (ADR-25.6), **so that** the voice vendor is the one people would listen to.
- **Given** the playlists, **when** the raters finish, **then** the decision CLI outputs a winner and a runner-up per language with the rating spread.
- **Given** the winner, **when** its streaming first-byte latency is measured, **then** it is under 300 ms or the runner-up carries the call voice.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E02-S01, E14-S02
- Requirements: FR-502, FR-524, FR-1101, FR-1324, FR-1330

### E02-S04 · Fifty scripted calls for latency
**As an** operator, **I want** 50 scripted calls (learner turns from the volunteer clips and agent-written scripts) run against the minimal call-worker in both worker placements, **so that** the host's reply latency is measured before any learner calls.
- **Given** the 50 calls, **when** `tools/call-bench` finishes, **then** `reply_latency_ms` median is under 1,500 and p95 under 2,500, and `silence_to_sound_ms` is recorded per vendor pair.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 03 Live call · Depends on: E05-S01, E02-S02
- Requirements: FR-1101, FR-1332, NFR-107

### E02-S05 · Vendors frozen and adapters for the winners only
**As the** coding agent, **I want** `vendors.yaml` committed with the voice winners after the blind test and complete with the 50-call result before phase 2, and thin adapters (`llm`, `tts`, `asr`, `align`, `embed`) only for the winning and secondary vendors, **so that** nothing in week 3 is built on an untested vendor.
- **Given** a role, **when** code requests a vendor, **then** it goes through the adapter and the tracing middleware, never a vendor SDK directly (a lint rule fails otherwise).
- **Given** the primary voice vendor's key is revoked for an hour, **when** production runs, **then** the secondary carries the same day's production.
- Size: L · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E02-S02, E02-S03, E02-S04
- Requirements: FR-1322, FR-1326, NFR-203

### E02-S06 · English language package v1
**As a** teacher role, **I want** an English package with word frequency ranks (wordfreq; no SUBTLEX licence), a lemmatizer, a chunk list of about 300 formulaic sequences, the structure inventory (about 120 structures in Phase 1, a few hundred by Phase 3, built from open sources with English Grammar Profile-style ids, not waiting for the EGP licence, ADR-24.18), a ban list of stock names and tropes, and name rules, **so that** coverage, targeting and classification run on real data.
- **Given** 10 fixture scripts whose coverage was computed by hand from the frequency list, **when** the coverage check runs, **then** its known-word percentage matches within 0.5 points.
- **Given** English as the only target in v1 unless another passes the gate (ADR-24.20), **when** the package is marked shippable, **then** the `vendor-lab gate --target en` result for all five gate checks (voices, recognizers, native read of 10 scripts, call latency, inventory present) is attached to it and linked from the release manifest.
- Size: L · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 02 Generation pipeline, 05 Assessment · Depends on: none
- Requirements: FR-002, FR-431, FR-815, FR-1100, FR-1101, FR-1103, FR-1105, FR-1106, FR-1107

### E02-S07 · The drafted bibles versioned in the packages
**As a** writer role, **I want** the bibles drafted in `content/bibles/` (Karim, Mona and the default world in `lang/en`; Salma and her strings in `native/ar` and `native/en`) versioned inside the packages, **so that** a bible change is a release and the characters stay written by people (ADR-24.3).
- **Given** a bible change, **when** it is merged, **then** the release manifest records the version and the eval gate runs the writer and host suites.
- **Given** Muath's read of the English bibles and of Salma's lines in English and Arabic (register A3), and an AI review pass of every bible against the laws and the ban lists (ADR-25.7), **when** a package version is marked shippable, **then** it records both; an unread `native/ar` does not ship and `native/en` ships alone.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 02 Generation pipeline · Depends on: E02-S06; Muath's read (A3)
- Requirements: FR-434, FR-435, FR-501, FR-520, FR-1102, FR-1104, NFR-206, NFR-605

### E02-S08 · The language gate as a runnable harness
**As an** operator, **I want** the five gate checks (blind voice rating, 30-clip recognizer test, native read of 10 scripts, call latency, structure inventory present) as jobs with a one-page result per language, **so that** a new language opens by passing a test, not by a vendor's list.
- **Given** a candidate language, **when** the harness runs with its clips, raters and scripts, **then** it outputs pass or fail per check and refuses to mark the package shippable unless all five pass.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 02 Generation pipeline, 09 Operations · Depends on: E02-S05, E02-S06
- Requirements: FR-1101, FR-1102, FR-1107, NFR-605

### E02-S09 · Second-language dry run through the gate
**As an** operator, **I want** one large candidate language (for example Spanish) run through the harness after launch, **so that** we know how long a language takes and what breaks before the public launch.
- **Given** the dry run, **when** it finishes, **then** a report lists each check's result, the cost, the days taken and the native-speaker time used.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 02 Generation pipeline · Depends on: E02-S08
- Requirements: FR-1105, FR-1107
