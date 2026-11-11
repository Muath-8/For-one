# For one: documentation

*For one is your own private teacher who makes you a daily show.* It is a personal podcast in the language you are learning, with a live call after each episode, and it never tells you that you were wrong. This repository holds every document needed to build it. There is no code here yet. The build runs from 2026-11-18 to 2027-03-12, and the paid founding beta opens on **2027-03-17** and runs to the gate review on 2027-04-20. The open follows the work: 2027-03-17 with two engineers from build start, a week later for each week the second engineer starts late, and 2027-02-17 with a third engineer from 2026-12-01 (ADR-24.11).

**Status on 2026-11-12:** every product, scope and budget decision is taken (ADR-24). What remains is listed under [What is still owed](#what-is-still-owed). Two kinds of thing are left: actions only Muath can take (counsel, hiring, accounts) and numbers only the tests can produce.

## Which document wins

When two documents disagree, the higher one in this list wins, and the lower one is a bug to fix.

1. **[architecture/10-decision-records.md](architecture/10-decision-records.md):** the ADRs (ADR-01 to ADR-24) and the register of what is still owed (§10).
2. **[decisions.md](decisions.md):** Muath's ten decisions (2026-10-23; 6 to 10 taken as recommended on 2026-11-12).
3. **[PRD-v3.md](PRD-v3.md):** the requirements. Every rule has an id (`FR-`, `NFR-`, `LAW-`, `GATE-`, `OPEN-`), and other documents cite these ids.
4. **[architecture/](architecture/) 01 to 09:** how the system works, domain by domain.
5. **[technical-design/](technical-design/):** what an engineer opens to start coding (data model, API contracts, pipelines).
6. **[design/](design/):** principles, design system, tokens, flows, screens, and the audio and voice UX.
7. **[engineering/](engineering/):** how the team works (repository, environments, CI/CD, testing, on-call, data handling, definition of done).
8. **[backlog/](backlog/):** epics, stories, the release plan, risks, and the traceability from requirements to stories.

## Background only (do not build from these)

| File | What it is |
|---|---|
| [Product_Concept.md](Product_Concept.md) | The first one-page concept |
| [concept-v2.md](concept-v2.md) | The rethought concept; PRD-v3 is built on it |
| [PRD.md](PRD.md), [PRD-v2.md](PRD-v2.md) | Earlier PRD versions (2.0; 3.0 and 3.1), kept for comparison |
| [perspectives/](perspectives/) | The eleven lens studies (learning science, voice, market and others) |
| [features/for-one-features.html](features/for-one-features.html) | The agreed feature map, as a page |
| [architecture/_review-findings.md](architecture/_review-findings.md), [architecture/_digest-constraints.md](architecture/_digest-constraints.md) | Working records from the architecture reviews; every finding has been applied |

## Content, legal texts and the pilot

| Folder | What it holds | Status |
|---|---|---|
| [content/](content/) | The host bibles (Karim, Mona, the world), Salma's bible and strings (English and Arabic), ban lists and the correction-guard corpus, the sting brief | Drafts of 2026-11-12; a native English editor reads them by 2026-12-01, and Muath reads the Arabic (ADR-24.3) |
| [legal/](legal/) | Counsel question pack, privacy notice, terms, consent texts, DPIA, ROPA (record of processing), crisis protocol, pilot consent addendum, reviewer confidentiality | Drafts for counsel, not legal advice; the review is due 2027-02-15 |
| [milestone-0/](milestone-0/) | The hand-made pilot kit (15 learners, 14 days); gate decision 2026-11-18; pre-payers continue on its process until the open (the bridge, ADR-24.11) | Running |

## Reading paths

- **New engineer:** this README, then `engineering/00-handbook-index.md`, `technical-design/00-overview.md`, `architecture/10-decision-records.md` §1, `backlog/00-release-plan.md`, then the epic you are on.
- **Designer:** `design/README.md`, then `PRD-v3.md` Parts 1 to 4 and 11.
- **Writer or editor:** `content/README.md`, `design/06-content-and-voice-guidelines.md`, then `PRD-v3.md` Part 6.
- **Counsel:** `legal/00-counsel-question-pack.md`, `legal/README.md`, then `architecture/07-security-privacy-and-compliance.md`.

## What is still owed

The full list, with dates and the fallback for each, is the register in [architecture/10-decision-records.md §10](architecture/10-decision-records.md). In short:

| By | Owner action |
|---|---|
| 2026-11-13 | Name counsel and send the question pack (A13, A1) |
| 2026-11-17 | Counsel confirms the region, transfer basis and regimes (A1) |
| 2026-11-18 | Brand domain; Apple and Google developer applications (A3); the pilot gate result (M1) |
| 2026-11-19 | Tell the pilot's pre-payers the new date, with a refund or a bridge place (A15) |
| 2026-11-18 | **A second engineer working from build start** (A2); each week later moves the open a week; a third from 2026-12-01 pulls it to 2027-02-17 |
| 2026-11-25 | The native English reader hired (A4) |
| 2026-12-01 | Bibles read by the native editor; Salma's Arabic read by Muath (A4, A5) |
| 2026-12-02 | Paddle account under the legal entity (A6) |
| 2026-12-15 | Pilot consent addendum Part 2 signed by bridge learners (A9); voice-rate request; Anthropic zero data retention (A7) |
| 2027-02-15 | Counsel reviews `legal/` (A8) |

## Pages

The Markdown files are the source of truth. The HTML pages (`architecture/pages/`, `technical-design/technical-design.html`, `design/for-one-design.html`, `engineering/handbook.html`, `backlog/release-plan.html`) are readable views that were published on 2026-11-06 and 2026-11-07, and they lag the 2026-11-12 decisions until rebuilt.
