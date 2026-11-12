# For one

*For one is your own private teacher who makes you a daily show.* It is a personal podcast in the language you are learning, with a live call after each episode, and it never tells you that you were wrong.

This repository will hold the code and already holds every document needed to build it. There is no code yet. The code is built by an AI coding agent under Muath, which starts from [`AGENTS.md`](AGENTS.md).

**How it gets built ([ADR-25](docs/architecture/10-decision-records.md)).**
- An AI coding agent builds it, story by story; Muath approves merges, migrations, prompt changes and deploys.
- It is a web application only, with a private podcast feed for listening in any podcast app.
- There is no pilot and no beta: version 1 launches once, with open signup and a 7-day free trial.
- The plan has no calendar dates. Work runs in phases, in dependency order, and the product launches when the launch checklist is green.
- There is no lawyer. Compliance is built into the design and checked against a written self-review.

## Layout

```
For-one/
├── README.md            this map
├── AGENTS.md            the coding agent's instructions (read first)
├── CLAUDE.md            points Claude Code at AGENTS.md
└── docs/
    ├── product/         PRD-v3.md (the requirements), decisions.md (Muath's decisions)
    ├── architecture/    01 to 09 by domain; 10-decision-records.md (ADR-01 to ADR-25, the register of what is owed); pages/ (HTML views)
    ├── technical-design/  data model, API contracts, pipelines, client, security, observability
    ├── design/          principles, design system and tokens, flows, screen specs, audio UX, voice
    ├── engineering/     the handbook: repository, environments, CI/CD, testing, operations, data, done; starter-files/
    ├── backlog/         release plan (phases and launch checklist), epics, stories, risks, traceability
    ├── content/         host bibles, Salma's lines (English and Arabic), ban lists, sting brief
    ├── legal/           self-review checklist, privacy notice, terms, consent texts, DPIA, RoPA, crisis protocol
    └── archive/         background only: earlier concepts and PRDs, the lens studies, the unused pilot kit, the feature map
```

When code arrives, it goes beside `docs/` at the root (`apps/`, `packages/`, `infra/`, `tools/`, `eval/`, `ops/`), as [docs/engineering/01-repository-layout.md](docs/engineering/01-repository-layout.md) describes. Paths written inside the documents are relative to `docs/` (so `architecture/10-decision-records.md` means `docs/architecture/10-decision-records.md`); code paths are relative to the repository root.

## Which document wins

When two documents disagree, the higher one in this list wins, and the lower one is a bug to fix.

1. [docs/architecture/10-decision-records.md](docs/architecture/10-decision-records.md): the decision records and the register of what is still owed (§10).
2. [docs/product/decisions.md](docs/product/decisions.md): Muath's product decisions.
3. [docs/product/PRD-v3.md](docs/product/PRD-v3.md): the requirements, with ids (`FR-`, `NFR-`, `LAW-`, `GATE-`) that every other document cites.
4. [docs/architecture/](docs/architecture/) 01 to 09: how the system works, domain by domain.
5. [docs/technical-design/](docs/technical-design/): what the agent opens to start coding.
6. [docs/design/](docs/design/): every screen, flow, state and string.
7. [docs/engineering/](docs/engineering/00-handbook-index.md): how the agent works.
8. [docs/backlog/](docs/backlog/00-release-plan.md): what to build, in what order.

[docs/content/](docs/content/README.md) and [docs/legal/](docs/legal/README.md) are text used as written. Nothing in [docs/archive/](docs/archive/README.md) is an instruction.

## Reading paths

- **The AI agent:** [AGENTS.md](AGENTS.md), then [docs/backlog/00-release-plan.md](docs/backlog/00-release-plan.md), the story it is on, and the documents the story cites.
- **Muath:** this README, the register in [docs/architecture/10-decision-records.md §10](docs/architecture/10-decision-records.md), the release plan, and [docs/legal/00-self-review-checklist.md](docs/legal/00-self-review-checklist.md).
- **Writing and voice:** [docs/content/README.md](docs/content/README.md), then [docs/design/06-content-and-voice-guidelines.md](docs/design/06-content-and-voice-guidelines.md).

## What is still owed

Things only Muath can do. None has a date; each says what it must happen before. The full list is in the register (§10 of the decision records).

| Owner action | Needed before |
|---|---|
| Give the AI agent its own GitHub identity on this repository and protect `main` so merges need Muath's approval (A10) | the agent's first pull request |
| Open the vendor accounts and API keys, and accept their standard data processing agreements (A1) | the agent's first deploy to staging |
| Record about 30 short voice clips from volunteers, and rate the voice test with a few listeners (A2) | choosing the voice and speech vendors |
| Read and approve the bibles and Salma's lines, English and Arabic (A3) | tuning the writer and host prompts |
| Approve merges, migrations, prompt changes and deploys as the agent asks (A8) | each one |
| Open the Paddle account (A5) | going live with payments (the sandbox works before) |
| Choose the domain (A6) | email sending and the first public deploy |
| Complete the self-review checklist and approve the legal texts (A4) | launch |
| Appoint an EU and UK representative, a paid service, if the company is outside the EU and UK (A7) | launch, if it applies |

## Pages

The Markdown files are the source of truth. The HTML pages are readable views of them: [docs/architecture/pages/](docs/architecture/pages/architecture-hub.html) (rebuilt with `docs/architecture/pages/_build/build.py` and `hub.py`), [technical design](docs/technical-design/technical-design.html), [design](docs/design/for-one-design.html), [engineering handbook](docs/engineering/handbook.html) and [release plan](docs/backlog/release-plan.html).
