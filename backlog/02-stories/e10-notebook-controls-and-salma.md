# E10 · Notebook, controls and Salma on demand

*Architecture domains 06 and 04. The teacher is invisible, but nothing is hidden. Counts only grow; nothing resets; nothing has a target.*

### E10-S01 · Notebook: what I'm working on
**As a** learner, **I want** to see at most 3 things the teacher is working on with me, each with one of my own sentences, **so that** I know what the show is doing and can steer it.
- **Given** the list, **when** shown, **then** each item has the learner's sentence and no "correct" version beside it.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E03-S03, E07-S01

### E10-S02 · Veto and add
**As a** learner, **I want** to veto an item or add my own, **so that** the teacher works on what I want.
- **Given** a veto or add, **when** saved, **then** the next day's episode reflects it (synchronous re-target) and the item never returns unless re-added.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client, 04 Learner model · Depends on: E03-S10

### E10-S03 · Words you own
**As a** learner, **I want** the words I now use, each in a sentence I actually said with the audio, **so that** I can hear my own competence.
- **Given** a word marked owned (correct, unprompted, a day later, in another session), **when** listed, **then** the sentence and clip are the learner's own, with the date.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E09-S06

### E10-S04 · About you: facts with their source
**As a** learner, **I want** every fact the show knows with when I said it, and to edit or delete it, **so that** deep memory is trusted, not creepy.
- **Given** a fact, **when** shown, **then** the source quote and date appear; edit and delete call `memory/correct`.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E09-S10

### E10-S05 · Hours heard, minutes spoken, "why this episode", out in the world
**As a** learner, **I want** plain counts of hours heard and minutes spoken, the reasons for today's episode, and a place to log a real-world try, **so that** progress is evidence, not a score.
- **Given** the counts, **when** rendered, **then** they are plain text, monotonic and never a chart or a percentage (law lint).
- **Given** "I had the interview", **when** logged, **then** the hosts celebrate it in the next episode above everything else.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E07-S01, E04-S09

### E10-S06 · The controls sheet
**As a** learner, **I want** one short sheet: drop time, notification, captions, transcript, speed, feed link, voice storage, research opt-in, export, delete, cancel, **so that** there is no settings maze.
- **Given** a consent switch flipped, **when** saved, **then** a `consent_change` event with the text version shown is recorded and the deletion clocks start.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client, 07 Security · Depends on: E13-S03, E12-S07

### E10-S07 · Salma explains when asked
**As a** learner, **I want** to ask Salma "why do we say it like that?" and get an explanation in my own language, only when I ask, **so that** explanations exist without ever being pushed.
- **Given** a question, **when** asked in chat, **then** Salma explains and no explanation, note or nudge appears unasked anywhere else.
- Size: M · Priority: P0 · Week: W5 · Domain: 06 Client, 03 Live call · Depends on: E07-S08

### E10-S08 · Life updates and "tell Salma an idea"
**As a** learner, **I want** to tell Salma something new in my life or an idea for an episode, **so that** the show keeps up with me.
- **Given** a life update, **when** saved, **then** it goes through the memory keeper with a quote and reaches the next plan only once confirmed.
- Size: S · Priority: P0 · Week: W5 · Domain: 06 Client · Depends on: E09-S05

### E10-S09 · The tape
**As a** learner, **I want** my then-and-now recordings side by side in the notebook, **so that** I can hear myself improve.
- **Given** two recordings, **when** played, **then** they play in sequence with at most two measured differences in plain words, or none if the gate passed nothing.
- Size: M · Priority: P1 · Week: Beta · Domain: 06 Client · Depends on: E11-S05
