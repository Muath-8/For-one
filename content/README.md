# content/

*The authored creative content of For one: the hosts, the producer, the ban lists and the sound brief. Drafted on 2026-11-12 under ADR-24.3 ([architecture/10-decision-records.md](../architecture/10-decision-records.md)), which made these drafts the answer to OPEN-03 ("who writes the hosts and Salma"). Muath is the owner of record. The model writes episodes, calls and chats inside these documents; it never writes or edits them (design/06 §7, PRD FR-434).*

## What is here

| File | What it is | Status | Ships to | Reviewed by |
|---|---|---|---|---|
| [bibles/hosts-en.md](bibles/hosts-en.md) | The English show bible: premise and tone; Karim and Mona in full; the default world (places, side characters, running jokes, canon rules); arcs and the 4-week season with an example; the episode format and timing; how recasts sound; what hosts never say; 30 sample lines per host; the fixed lines (casting hellos, on-air announcements, call clips, feed tag) | Draft 2026-11-12; needs the native read | `packages/languages/en/bibles/karim.md` and `mona.md` (each carries its host's sections plus the shared ones, because the package interface holds two bible strings, architecture/02 §4.5); the fixed lines in §10 as a lines file in the same folder | The paid native English editor, by **2026-12-01** (ADR-24.3, 24.14); Muath signs off |
| [bibles/salma.md](bibles/salma.md) | Salma, the producer: who she is, her voice, that she never corrects, when she speaks, the language-shift rule; her string set (onboarding A1 to A10, notebook, "why this episode", conversation lines, weekly proof including the empty week, finale, trial and allowance, errors, the sample close) in English and Arabic. Consent, AI disclosure, billing, deletion and crisis strings are not duplicated here: they live in [legal/03](../legal/03-consent-texts.md) and [legal/06](../legal/06-crisis-protocol.md), and salma.md points to their ids (with Arabic drafts where legal/ has none) | Draft 2026-11-12. English needs the native read; **Arabic is a draft for Muath's read** | Bible prose: `packages/native/ar/salma/bible.md` and `packages/native/en/salma/bible.md`. Strings: the Arabic column to `packages/native/ar/ui_strings/`, the English column to `packages/native/en/ui_strings/` (the English fallback for every learner whose language is not shipped, ADR-02) | English: the native English editor by 2026-12-01. Arabic: Muath (ADR-24.3, 24.14). The legal/ strings: counsel |
| [ban-lists/en.md](ban-lists/en.md) | (A) the English sameness ban list: 92 stock names, settings, plots and phrases, seeded from the pilot's list; (B) the English law-word and correction-guard corpus: 69 entries with the law each protects, and the YAML shape the guard reads | Draft 2026-11-12; needs the native read; then updated monthly from review findings (FR-431, FR-436) | `packages/languages/en/ban_list.yaml`; `packages/languages/en/guard/correction_words.yaml` and `guard/law_words.yaml` (architecture/07 §4.10) | The paid native English reader (ADR-24.14), by 2026-12-01; the 50-call bench in build week 4 measures each guard row |
| [stings.md](stings.md) | The commissioning brief for sound: 12 show idents in four cuts, room tone, the call chime, the turn tone, the connect tick, the error thud, the mark click; no reward sounds and no notification sound of our own; specs, deliverables, acceptance tests, schedule and rights | Draft 2026-11-12; ready to send once Muath approves | `packages/languages/en/sound_design/` (PRD FR-1103) | Muath approves the brief; five listeners run the acceptance tests in build week 4 |

## Dates that depend on these files

| Date | What | Source |
|---|---|---|
| 2026-11-25 (build week 2) | The writer and host prompts are tested against the bibles; a bible change runs the writer and host eval suites | backlog B3, E02-S07; release plan |
| 2026-12-01 | Native English read of the host bible, the 30 sample lines per host, Salma's English and the English ban lists | ADR-24.3 |
| 2026-12-09 (build week 4) | The on-air announcement lines are needed (in hosts-en.md §10.3); the sound library is due | architecture/02 §11 item 3; stings.md §8 |
| 2026-12-15 | Counsel's crisis clip wording approved in legal/06; salma.md §7.10 points to it | ADR-24.15 |
| 2027-03-17 | Beta opens with `native/en` and `native/ar` (date re-set by ADR-24.11) | ADR-24.20 |

## Rules for editing

- These are package content. A change goes through a pull request, bumps the package's `versions.yaml`, and runs the eval suites the change touches (backlog NF-18, E02-S07).
- A host's voice, personality or memory never changes silently (PRD FR-503). A change a learner would hear is announced on air with the lines in hosts-en.md §10.3.
- Where these drafts disagree with PRD-v3, the PRD wins; each draft lists the places it had to choose between two documents.
