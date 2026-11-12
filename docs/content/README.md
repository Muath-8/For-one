# content/

*The authored creative content of For one: the hosts, the producer, the ban lists and the sound brief. Drafted on delegation under ADR-24.3 ([architecture/10-decision-records.md](../architecture/10-decision-records.md)), as changed by ADR-25. Muath is the owner of record. The model writes episodes, calls and chats inside these documents; it never writes or edits them (design/06 §7, PRD FR-434).*

## What is here

| File | What it is | Status | Ships to | Reviewed by |
|---|---|---|---|---|
| [bibles/hosts-en.md](bibles/hosts-en.md) | The English show bible: premise and tone; Karim and Mona in full; the default world (places, side characters, running jokes, canon rules); arcs and the 4-week season with an example; the episode format and timing; how recasts sound; what hosts never say; 30 sample lines per host; the fixed lines (casting hellos, on-air announcements, call clips, the feed tag, the word button, the crisis hand-off) | Draft, waiting for Muath's read | `packages/languages/en/bibles/karim.md` and `mona.md` (each carries its host's sections plus the shared ones, because the package interface holds two bible strings, architecture/02 §4.5); the fixed lines in §10 as a lines file in the same folder | Muath, and an AI review pass against the laws and the ban lists (ADR-25.7) |
| [bibles/salma.md](bibles/salma.md) | Salma, the producer: who she is, her voice, that she never corrects, when she speaks, the language-shift rule; her string set (onboarding A1 to A10 with the address-form chip, notebook, "why this episode", conversation lines, weekly proof including the empty week, finale, trial and allowance, errors, the sample close, the feed notes with "Heard it"), in English and Arabic. Consent, AI disclosure, billing, deletion and crisis strings are not duplicated here: they live in [legal/03](../legal/03-consent-texts.md) and [legal/06](../legal/06-crisis-protocol.md), and salma.md points to their ids | Draft. **The Arabic is a draft for Muath's read** | Bible prose: `packages/native/ar/salma/bible.md` and `packages/native/en/salma/bible.md`. Strings: the Arabic column to `packages/native/ar/ui_strings/`, the English column to `packages/native/en/ui_strings/` (the fallback for every learner whose language is not shipped, ADR-02) | Muath reads both columns; an AI review pass checks them (ADR-25.7). The legal/ strings follow the self-review checklist (ADR-25.3) |
| [ban-lists/en.md](ban-lists/en.md) | (A) the English sameness ban list: 92 stock names, settings, plots and phrases, seeded from the first draft bible; (B) the English law-word and correction-guard corpus: 69 entries with the law each protects, and the YAML shape the guard reads | Draft; then updated monthly from review findings (FR-431, FR-436) | `packages/languages/en/ban_list.yaml`; `packages/languages/en/guard/correction_words.yaml` and `guard/law_words.yaml` (architecture/07 §4.10) | Muath and the AI review pass; the 50-call bench measures each guard row before launch |
| [stings.md](stings.md) | The commissioning brief for sound: 12 show idents in four cuts, room tone, the call chime, the turn tone, the connect tick, the error thud, the mark click; no reward sounds and no notification sound of our own; specs, deliverables, acceptance tests, order of work and rights | Draft; ready to send once Muath approves | `packages/languages/en/sound_design/` (PRD FR-1103) | Muath approves the brief; five volunteer listeners run the acceptance tests |

## Decisions these files follow

Taken after the first drafts and reflected in them (ADR-24, section B):

| Decision | What it means here |
|---|---|
| 24.B22 | In a call the **host** gives the word when the learner holds the word button and says it in their own language. Salma is silent in calls. |
| 24.B23 | No self-repair prompts ("Wait, yesterday you...?"). |
| 24.B24 | The 5-second feed tag is the host's (hosts-en.md §10.5). |
| 24.B25 | PRD copy that broke the laws is replaced with the bibles' lines; "my mistake" is on the guard's allow-list, only for a host or Salma owning a wrong memory. |
| 24.B26 | An optional **address-form chip** at A3: masculine, feminine or neutral wording, neutral by default, never inferred, stored as `learners.address_form` (salma.md §6 and §7.1). |
| 24.B27 | The trial line: "Your 7-day trial is on 2 episodes a day. No card needed. On day 7 you choose a plan." |
| 24.B29 | The one exception to Salma's silence in calls: a pre-recorded crisis clip in her voice, in the learner's own language, after the host stops (salma.md §7.10, legal/06). |
| 24.B30 | The feed item's notes carry a **"Heard it"** link; it counts toward an active day, a download never does (salma.md §7.9). |
| ADR-25 | Email one-time code is the only sign-in; no calendar dates; no hired reviewers (Muath plus an AI review pass); one public launch. |

## Order of work

These files gate, in order:

1. The writer and host prompts are tuned against the bibles. Any bible change runs the writer and host eval suites (backlog E02-S07, NF-18), and Muath approves it (ADR-25.2).
2. The on-air announcement lines (hosts-en.md §10.3) and the sound library are needed before the voice studio mixes real episodes.
3. Everything here is read by Muath and passes the AI review pass before launch.

## Rules for editing

- These are package content. A change goes through a pull request, bumps the package's `versions.yaml`, and runs the eval suites the change touches.
- A host's voice, personality or memory never changes silently (PRD FR-503). A change a learner would hear is announced on air with the lines in hosts-en.md §10.3.
- Where these drafts disagree with PRD-v3 or a later decision record, those win; the disagreement is a bug in the draft.
