# E02 · Vendor tests and the language gate

*Architecture domains 02 (pipeline), 03 (live call), 08 (cost and vendors). The tests use the 30 consented Milestone 0 learner clips, Muath's hand tags and the pilot scripts. Every decision is frozen in `vendors.yaml` by 27 November.*

### E02-S01 · Consent addendum before any clip leaves
**As an** operator, **I want** every Milestone 0 learner whose clips are used in vendor tests to have accepted an addendum naming the vendors, **so that** the tests do not break the promise the pilot made.
- **Given** a clip in the test set, **when** the vendor-lab CLI runs, **then** it refuses any clip whose learner has no addendum on file and any vendor whose register row is `blocked`.
- Size: S · Priority: P0 · Week: W1 · Domain: 07 Security · Depends on: E13-S03

### E02-S02 · Recognizer test on 30 learner clips
**As an** operator, **I want** the 30 clips run through Soniox, Deepgram, AssemblyAI and ElevenLabs Scribe with the hand tags, **so that** the streaming and verbatim vendors are chosen on whether they keep learner errors.
- **Given** a clip with tagged errors, **when** each vendor transcribes it, **then** the sheet records, per vendor, the share of tagged errors kept verbatim, the share of own-language words caught, and latency.
- **Given** the sheet, **when** a vendor keeps fewer than 90% of tagged errors, **then** it cannot be the verbatim vendor for English.
- Size: M · Priority: P0 · Week: W1 · Domain: 03 Live call · Depends on: E02-S01, E14-S02

### E02-S03 · Blind two-host voice test
**As an** operator, **I want** the same two-host script and the Salma script rendered on Gemini 3.8 Flash TTS, Inworld TTS-2 and ElevenLabs v4 and rated blind by 10 listeners as episode voice and call voice together, **so that** the voice vendor is the one people would listen to.
- **Given** the playlists, **when** 10 raters finish, **then** the decision CLI outputs a winner and a runner-up per language with the rating spread.
- **Given** the winner, **when** its streaming first-byte latency is measured, **then** it is under 300 ms or the runner-up carries the call voice.
- Size: M · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E02-S01, E14-S02

### E02-S04 · Fifty scripted calls for latency
**As an** operator, **I want** 50 scripted calls from Milestone 0 audio run against the minimal call-worker in both worker placements, **so that** the host's reply latency is measured before any learner calls.
- **Given** the 50 calls, **when** `tools/call-bench` finishes, **then** `reply_latency_ms` median is under 1,500 and p95 under 2,500, and `silence_to_sound_ms` is recorded per vendor pair.
- Size: M · Priority: P0 · Week: W2 · Domain: 03 Live call · Depends on: E05-S01, E02-S02

### E02-S05 · Vendors frozen and adapters for the winners only
**As an** engineer, **I want** `vendors.yaml` committed with the winners by 27 November and thin adapters (`llm`, `tts`, `asr`, `align`, `embed`) only for the winning and secondary vendors, **so that** nothing in week 3 is built on an untested vendor.
- **Given** a role, **when** code requests a vendor, **then** it goes through the adapter and the tracing middleware, never a vendor SDK directly (a lint rule fails otherwise).
- **Given** the primary voice vendor's key is revoked for an hour, **when** production runs, **then** the secondary carries the same day's production.
- Size: L · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E02-S02, E02-S03, E02-S04

### E02-S06 · English language package v1
**As a** teacher role, **I want** an English package with word frequency ranks, a lemmatizer, a chunk list of about 300 formulaic sequences, the structure inventory (about 120 structures at W1, a few hundred by W3, from the English Grammar Profile), a ban list of stock names and tropes, and name rules, **so that** coverage, targeting and classification run on real data.
- **Given** the 10 hand-checked pilot scripts, **when** the coverage check runs, **then** its known-word percentage matches the pilot checker within 0.5 points.
- Size: L · Priority: P0 · Week: W1 · Domain: 02 Generation pipeline, 05 Assessment · Depends on: none

### E02-S07 · Host and Salma bibles in the package
**As a** writer role, **I want** the host bibles (Karim, Mona, the default world) and Salma's strings versioned inside the language package, **so that** a prompt change is a release and the characters stay written by people.
- **Given** a bible change, **when** it is merged, **then** the release manifest records the version and the eval gate runs the writer and host suites.
- Size: M · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E02-S06; who writes the hosts and Salma (blocking item B3)

### E02-S08 · The language gate as a runnable harness
**As an** operator, **I want** the five gate checks (blind voice rating, 30-clip recognizer test, native read of 10 scripts, call latency, structure inventory present) as jobs with a one-page result per language, **so that** a new language opens by passing a test, not by a vendor's list.
- **Given** a candidate language, **when** the harness runs with its clips, raters and scripts, **then** it outputs pass or fail per check and refuses to mark the package shippable unless all five pass.
- Size: M · Priority: P1 · Week: Beta · Domain: 02 Generation pipeline, 09 Operations · Depends on: E02-S05, E02-S06

### E02-S09 · Second-language dry run through the gate
**As an** operator, **I want** one large candidate language (for example Spanish) run through the harness during the beta, **so that** we know how long a language takes and what breaks before the public launch.
- **Given** the dry run, **when** it finishes, **then** a report lists each check's result, the cost, the days taken and the native-speaker time used.
- Size: M · Priority: P1 · Week: Beta · Domain: 02 Generation pipeline · Depends on: E02-S08
