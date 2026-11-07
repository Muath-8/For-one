# E04 · Episode generation pipeline

*Architecture domain 02. Roles: teacher (Opus-class, batch), writer (Sonnet-class), fitter (code plus Haiku-class), editor (Gemini Flash class, a second vendor), voice studio. Everything nobody waits on runs in batch.*

### E04-S01 · Teacher plans the session
**As a** learner, **I want** an unseen teacher to pick one grammar target, 2 to 4 words by need and readiness, the right forms of my own mistakes to bring back, and three ideas for tomorrow, **so that** every episode teaches without looking like a lesson.
- **Given** a compiled teacher brief, **when** the teacher runs, **then** `validate_plan` passes: exactly 1 grammar target, 2 to 4 words, no target used 4 sessions in a row, at least 80% of new words from the top 3,000 lemmas.
- **Given** an error in the profile, **when** the plan is made, **then** the right form appears in the plan's "bring back" list with a count of natural uses.
- Size: L · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E03-S06, E02-S05

### E04-S02 · Writer produces the package
**As a** learner, **I want** a script of 2 to 4 scenes with a 30-second cold open that calls back yesterday's words, an article at my level, a call brief with planned host moves, and a chat opener, **so that** the four doors tell one story.
- **Given** a plan, **when** the writer runs, **then** `validate_package` passes: scenes 2 to 4, cold open at most 30 s, at most 2 life facts, target words present in the dialogue, the ending is a question to the learner by name.
- Size: L · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E04-S01, E02-S07

### E04-S03 · Fitter: coverage in code with targeted rewrites
**As a** learner, **I want** about 95% of the episode's words to be ones I know (98% for text), **so that** I follow it without a dictionary.
- **Given** a script below the coverage dial, **when** the fitter runs, **then** only the failing sentences go back for a rewrite, at most 2 rounds, and the result is logged with the new-word count (3 to 6).
- **Given** the first three episodes of a learner, **when** fitted, **then** the dial is one step easier.
- Size: M · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E02-S06, E03-S02

### E04-S04 · Editor from a second vendor
**As a** learner, **I want** every episode checked for correctness, no uncertain memory, the fun carrying the language, nothing that reads as a lesson or a correction, variety, the laws, and "would they pick this over a real podcast?", **so that** a bad episode never ships.
- **Given** an editor fail, **when** repair runs, **then** one targeted repair and one recheck happen; a second fail ships the fallback episode and a human is paged after 3 fallbacks in 7 days.
- **Given** the Milestone 0 packages and Muath's reads, **when** the editor runs over them, **then** agreement with his step-8 reads is above 80%.
- Size: M · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E04-S02

### E04-S05 · Voice studio with re-listen
**As a** learner, **I want** two distinct host voices, word timings, correctly pronounced names, and a mix within 4:00 to 8:00, **so that** the show sounds like a show.
- **Given** a script, **when** rendered scene-parallel, **then** `check_duration` passes, timings align to words, and every line passes the re-listen check within 2 re-synthesis attempts.
- **Given** the primary voice vendor fails, **when** production runs, **then** the secondary voice renders the same script that day.
- Size: L · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E02-S05

### E04-S06 · Senses, glosses and publish
**As a** learner, **I want** a meaning in my own language under any hard word and the episode published atomically, **so that** "Huh?" always has something to show.
- **Given** a package, **when** published, **then** uploads finish before the transaction commits, `episodes.cost_usd` is set, and the gloss bundle is shared across learners for the same sense.
- Size: M · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline · Depends on: E04-S05, E01-S08

### E04-S07 · Batch mode with the on-demand fallback
**As an** operator, **I want** everything nobody waits on submitted in pooled batches with `batch/watch`, and an on-demand fallback at drop time minus 90 minutes, **so that** cost is low and no drop is missed.
- **Given** a batch not returned 90 minutes before a learner's drop, **when** the watcher checks, **then** the episode is produced on-demand and the batch result is discarded.
- **Given** 20 test episodes, **when** produced in batch, **then** cost per episode and cache hit rate per step are in the cost report.
- Size: M · Priority: P0 · Week: W2 · Domain: 02 Generation pipeline, 08 Cost · Depends on: E04-S06, E14-S03

### E04-S08 · On-demand kinds: pilot, sample, swap, return, recap
**As a** learner, **I want** the pilot and sample to start playing within 30 to 45 seconds and a swap or return episode within 30 seconds, **so that** the first ten minutes and a bad day never wait on a batch.
- **Given** the pilot kind, **when** scene 1 passes its gate, **then** streaming starts while scenes 2 and 3 render.
- **Given** the sample kind, **when** produced, **then** cost is under $0.05 and moderation runs on the input.
- **Given** the return kind after 5+ days away, **when** produced, **then** it is one step easier, opens from the learner's life and never mentions the days missed.
- Size: L · Priority: P0 · Week: W3 · Domain: 02 Generation pipeline · Depends on: E04-S07

### E04-S09 · Ideas, the cutoff and "why this episode"
**As a** learner, **I want** three ideas each night (one from my life, one wildcard, at most one arc), a 6-hour cutoff before my drop, and 2 to 4 reasons for the episode I got, **so that** I own the topic and can see the teacher's reasons.
- **Given** no pick by the cutoff, **when** production starts, **then** the top-ranked idea is used and shown as the hero.
- **Given** an episode, **when** "why this episode" is opened, **then** 2 to 4 reasons appear, each tied to a plan element.
- Size: M · Priority: P0 · Week: W3 · Domain: 02 Generation pipeline · Depends on: E04-S01

### E04-S10 · Casting: hello clips, voice swap, name respelling
**As a** learner, **I want** to hear each host say hello, swap a voice, pick an accent and have my name said right, **so that** the show sounds like mine.
- **Given** a casting change after the pilot is made, **when** saved, **then** the pilot re-renders with the new voice version.
- **Given** the 15 pilot intake names, **when** respelled, **then** every name passes Muath's listen check.
- Size: M · Priority: P0 · Week: W3 · Domain: 02 Generation pipeline · Depends on: E04-S05

### E04-S11 · The variety system
**As a** learner, **I want** no format three times in a row, no stock names or tropes, and no episode too like my last 20, **so that** the show never goes stale.
- **Given** a new script, **when** its cosine similarity to any of the last 20 exceeds the threshold set from the pilot's "too alike" pairs, **then** the writer is re-run with a variety note.
- Size: M · Priority: P0 · Week: W4 · Domain: 02 Generation pipeline · Depends on: E04-S04, E15-S02

### E04-S12 · Arcs, seasons and the series bible writes
**As a** learner, **I want** arcs of 1 to 3 weeks, at most 2 open, that advance only when I show up, inside a 4-week season with a goal in my words, **so that** the story waits for me and never becomes a debt.
- **Given** a learner away for 10 days, **when** they return, **then** arc state is unchanged and the return episode picks up the open arc or none.
- **Given** a third arc proposed, **when** the teacher plans, **then** it is refused.
- Size: M · Priority: P0 (finale rules P1) · Week: W4 · Domain: 02 Generation pipeline · Depends on: E03-S05, E04-S01

### E04-S13 · Fallback episode, human page and review sampling
**As an** operator, **I want** a fallback episode kind, a page listing failed runs, and 10 random episodes per learner per month queued for a human read, **so that** a bad night is survivable and quality is checked by a person.
- **Given** a run fails after repair, **when** the fallback ships, **then** the failed package is on the human page with the editor's reasons.
- Size: S · Priority: P0 · Week: W4 · Domain: 02 Generation pipeline, 09 Operations · Depends on: E04-S04
