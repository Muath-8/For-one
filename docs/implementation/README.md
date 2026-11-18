# Local v1 implementation record

Started 2026-11-12. Base commit: `1983a73`. Integration branch: `codex/v1-local-integration`. Original branch: `docs/adr-24-decisions`.

## Session authorization

Muath's execution request authorizes the complete documented v1 implementation locally, concurrent delegated work, isolated story branches, and integration of independently reviewed commits into this branch. No pushes, remote issues or PRs, merges to main, deployments, cloud applies, purchases, new processor transfers, legal acceptance, or claimed human sign-off.

Local edits to application code, tests, CI, infrastructure source, canon-specified migrations, prompts, rules, versions, vendors and prices are authorized. Disposable local database migrations are authorized. Do not invent vendors, prices, thresholds, baselines, architecture, contracts or learner copy. Preserve legal text, consent, crisis resources, bibles and ban lists. Do not edit AGENTS.md. These session exceptions replace serial work and remote PR requirements, not product laws, privacy, tests-first or independent review.

Each story gets acceptance tests committed before implementation, a local review with Story / Why / What / How tested and applicable definition-of-done items, a fresh Sol high review, and a separate security review where required. Local checks are not remote CI or external verification. Fake data cannot establish vendor quality, cost, production latency or launch readiness.

## Capability and environment evidence

- Manager: current session; requested GPT-6 Astra/high. This session exposes no tool to change or independently attest its own model configuration.
- Implementation/review route: collaboration tool explicitly offers `gpt-6.1-sol`, with `reasoning_effort: high` and fresh context.
- UI: Claude Code 2.1.322 authenticated with first-party Claude login. Successful CLI probe with `--model opus --effort high` returned `canonicalModel: claude-opus-5-5` and `READY`. UI implementation launched with explicit `--model claude-opus-5-5 --effort high`, no fallback, isolated worktree `../For-one-ui`.
- Windows host: Node 22.17.0, pnpm 10.12.4 (canon requires 9), Python 3.13 (canon requires 3.12), uv 0.7.22. WSL Ubuntu exists. Docker, make and gitleaks absent from the initial PATH checks; environment setup pending.
- Existing untracked `for-one-detailed.html` and `for-one-overview.html` belong to the user and must remain untouched.

## Status

No application stories integrated yet. Per-story status must separately track implemented, locally verified, independently reviewed, externally verified, blocked and deferred; never flatten them into done.

Assignments:
- `foundation`: GPT-6.1 Sol/high, E01-S01 backend/build/CI infrastructure, `../For-one-e01-s01`, branch `codex/e01-s01-foundation`.
- Claude Opus 5.5/high: E01-S01 renderable web shell slice and E07-S01 follow-up contract, `../For-one-ui`, branch `codex/e01-s01-web-shell`; owns JSX/CSS/components, Sol owns web package/config/lockfiles.
- `inventory`: GPT-6.1 Sol/high, reconciled story/AC ledger and canonical dependency corrections, record files only.
- `toolchain`: GPT-6.1 Sol/high, WSL development tools and secret hook setup, environment record only.

The initial manager documentation commit inherited the repository's configured local author. Subsequent local commits use an explicit agent author; no remote GitHub identity or A10 verification is claimed.

## External requirements

Cloud resources, staging/prod checks, actual vendor measurements, volunteer clips and raters, device checks, accounts, DPAs and human approvals remain external until evidence exists. Do not manufacture passing results.

## Resume

Read this record, the generated story ledger, reviews and blocker records. Check git status and agent activity before editing. Continue from the first ready incomplete story; preserve all work and tests-first history.
