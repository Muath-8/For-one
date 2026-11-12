# For one: documentation

*For one is your own private teacher who makes you a daily show.* It is a personal podcast in the language you are learning, with a live call after each episode, and it never tells you that you were wrong. This repository holds every document needed to build it. There is no code here yet.

**How it gets built (ADR-25).**
- An AI coding agent builds it, story by story, under Muath. Muath approves merges, migrations, prompt changes and deploys.
- It is a web application only, with a private podcast feed for listening in any podcast app.
- There is no pilot and no beta: version 1 launches once, with open signup and a 7-day free trial.
- The plan has no calendar dates. Work runs in phases, in dependency order, and the product launches when the launch checklist is green.
- There is no lawyer. Compliance is built into the design and checked against a written self-review.

## Which document wins

When two documents disagree, the higher one in this list wins, and the lower one is a bug to fix.

1. **[architecture/10-decision-records.md](architecture/10-decision-records.md):** the decision records (ADR-01 to ADR-25) and the register of what is still owed (§10).
2. **[decisions.md](decisions.md):** Muath's product decisions.
3. **[PRD-v3.md](PRD-v3.md):** the requirements. Every rule has an id (`FR-`, `NFR-`, `LAW-`, `GATE-`), and other documents cite these ids.
4. **[architecture/](architecture/) 01 to 09:** how the system works, domain by domain.
5. **[technical-design/](technical-design/):** what the agent opens to start coding (data model, API contracts, pipelines).
6. **[design/](design/):** principles, design system, tokens, flows, screens, and the audio and voice UX.
7. **[engineering/](engineering/):** how the agent works: repository, environments, CI/CD, testing, operations, data handling, definition of done, and the `AGENTS.md` instructions for the code repository.
8. **[backlog/](backlog/):** epics, stories, the release plan (phases with exit checks), risks, and the traceability from requirements to stories.

## Content and legal texts

| Folder | What it holds | Status |
|---|---|---|
| [content/](content/) | The host bibles (Karim, Mona, the world), Salma's bible and lines (English and Arabic), ban lists and the correction-guard corpus, the sting brief | Drafts; Muath reads and approves them, and an AI review pass checks them against the laws (ADR-25.7) |
| [legal/](legal/) | The self-review checklist, privacy notice, terms, consent texts, DPIA, RoPA (record of processing), crisis protocol | Self-reviewed, not reviewed by a lawyer; `legal/README.md` says when one would become necessary (ADR-25.3) |

## Background only (do not build from these)

| File | What it is |
|---|---|
| [Product_Concept.md](Product_Concept.md), [concept-v2.md](concept-v2.md) | The first concept and the rethought concept PRD-v3 is built on |
| [PRD.md](PRD.md), [PRD-v2.md](PRD-v2.md) | Earlier PRD versions, kept for comparison |
| [perspectives/](perspectives/) | The eleven lens studies (learning science, voice, market and others) |
| [features/for-one-features.html](features/for-one-features.html) | The feature map, as a page |
| [milestone-0/](milestone-0/) | A hand-made pilot kit that will not be run (ADR-25.5); its prompts and show bible were source material for `content/` |
| [architecture/_review-findings.md](architecture/_review-findings.md), [architecture/_digest-constraints.md](architecture/_digest-constraints.md) | Working records from the architecture reviews; every finding has been applied |

## Reading paths

- **The AI agent:** `engineering/starter-files/AGENTS.md`, then this README, `backlog/00-release-plan.md`, the story it is on, and the documents the story cites.
- **Muath:** this README, `architecture/10-decision-records.md` §10 (what is owed), `backlog/00-release-plan.md`, `legal/00-self-review-checklist.md`.
- **Writing and voice:** `content/README.md`, `design/06-content-and-voice-guidelines.md`, then `PRD-v3.md` Part 6.

## What is still owed

Things only Muath can do; none has a date. Each says what it must happen before. The full list is in [architecture/10-decision-records.md §10](architecture/10-decision-records.md).

| Owner action | Needed before |
|---|---|
| Create the code repository and give the AI agent its own GitHub identity, so Muath can approve its pull requests (A10) | the agent's first pull request |
| Open the vendor accounts and API keys, and accept their standard data processing agreements (A1) | the agent's first deploy to staging |
| Record about 30 short voice clips from volunteers, and rate the voice test with a few listeners (A2) | choosing the voice and speech vendors |
| Read and approve the bibles and Salma's lines, English and Arabic (A3) | tuning the writer and host prompts |
| Approve merges, migrations, prompt changes and deploys as the agent asks (A8) | each one |
| Open the Paddle account (A5) | going live with payments (the sandbox works before) |
| Choose the domain (A6) | email sending and the first public deploy |
| Complete the self-review checklist and approve the legal texts (A4) | launch |
| Appoint an EU and UK representative, a paid service, if the company is outside the EU and UK (A7) | launch, if it applies |

## Pages

The Markdown files are the source of truth. The HTML pages (`architecture/pages/`, `technical-design/technical-design.html`, `design/for-one-design.html`, `engineering/handbook.html`, `backlog/release-plan.html`) are readable views of them. The architecture pages are rebuilt with `architecture/pages/_build/build.py` and `hub.py`.
