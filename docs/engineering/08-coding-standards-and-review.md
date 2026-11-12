# 08. Coding standards and review

Part of the For one engineering handbook. Written 2026-11-06; revised 2026-11-12 for ADR-25.2 (the code is written by an AI coding agent, read by an independent AI review pass and approved by Muath). Most of this is ordinary; the parts that are not are sections 4 (prompts) and 5 (what the review pass checks in this product).

## 1. Python

- Python 3.12, `uv` workspace, `pyproject.toml` at the root with shared tool config.
- **Ruff** for lint and format (line length 110, the default rule set plus `B`, `UP`, `S`, `PTH`, `RUF`, and the project's `banned-api` list). **Pyright** strict on `core`, `adapters`, `learner`, `assess`; standard elsewhere until the call phase, then strict everywhere.
- Pydantic v2 for every boundary: settings, events, API bodies, adapter inputs and outputs, prompt slots. A dict crossing a boundary is a bug.
- SQLAlchemy 2 with typed models; raw SQL is allowed in `forone.measures` and `ops/alerts.yaml` because those are the product, and nowhere else.
- `async` for `api`, `workflows` and the worker; CPU-bound work (alignment, spaCy) goes through a thread pool, never blocks the loop.
- Logging only through `forone.ops.log`. No `print` outside `tools/`.
- No `os.environ` outside `forone.core.settings`; no `boto3` outside `forone.core.media` and `keys`; no `resend` or `pywebpush` outside `forone.core.messaging`; no vendor SDK outside `forone.adapters`; no `hume` anywhere. Ruff enforces all of these.
- Errors: raise typed exceptions from `forone.core.errors`; adapters classify retryable versus not in `is_retryable()`; nothing catches `Exception` to continue except the outermost handler of a function, which logs and re-raises.
- Tests next to the code in `tests/` per package; fixtures in `conftest.py`; no test touches the network without the `integration` or `vendor_live` marker.

## 2. TypeScript and `web`

- Next.js 15 App Router, TypeScript strict, ESLint with `next/core-web-vitals`, `@typescript-eslint` strict, and the project's **law-furniture rule** (no streaks, points, levels, badges, autoplay or "next episode" controls in the player, or progress bars that are not the player's; the one "Next one" button on Today, shown only while the day's portion remains, is allowed (ADR-05, 24.B32); the banned names list lives in `apps/web/eslint/law-furniture.js` and Muath approves any extension).
- No business logic in `web`. The app renders what `api` returns and sends what the learner did. If a rule is needed on both sides (an allowance, a window), `api` is the truth and `web` asks.
- Generated API client from the committed OpenAPI document; hand-written fetches fail lint.
- Arabic is the first UI language: every layout is tested right-to-left first; strings come from `packages/native/ar/` through one `t()` helper; no string literal in JSX that a learner can read.
- Audio and the service worker are the two hard parts; a change there is tried on a real phone through the Vercel preview before Muath approves it, and the PR says on which phone and browser.

## 3. Pull requests

- One story per PR; under 400 lines of diff where possible; a prompt change and the code that depends on it ship together; a migration and the code that uses it ship together, expand before contract.
- Title in imperative mood, under 70 characters, starting with the story id (`E05-S03 Add the governor's recast budget`). Body with four headings: **Story** (the id, and the PRD or architecture sections it cites), **Why** (the problem), **What** (the change in words), **How tested** (the acceptance-criteria tests by name, the commands run, the eval run id if any, the staging check if any). The template is in `.github/pull_request_template.md`.
- The tests for the acceptance criteria are written and committed before the code that makes them pass; the PR's first commit is the failing tests (page 05 §1).
- Draft until CI and the review pass are green. Muath is asked to approve only then.
- The agent answers every blocking finding of the review pass with a commit or a reply that says why the finding does not apply; it never resolves a finding silently.
- Muath approves and merges. The agent has no merge permission.
- Squash merge; the squash message is the title plus the Why section.

Commit messages inside a PR do not matter (squash), but a commit that touches a prompt file says which version it bumps.

## 4. Rules for prompt changes

A prompt is code that no reader can check for correctness by reading alone, which is why these rules exist.

1. **A prompt lives in a file** under `packages/languages/<target>/prompts/` with frontmatter; the version in `versions.yaml` is bumped in the same PR (patch for wording that should not change behaviour, minor for a behaviour change, major for a new slot or a removed one). CI refuses a file change without a bump and a bump without a file change.
2. **The eval gate runs** the suites mapped to that prompt (handbook 04 §3) and the PR shows the metrics table. A regression beyond the threshold cannot merge. A pass is necessary, not sufficient: the review pass reads the diff and three sample outputs from the run (the run attaches them for synthetic learners), and so does Muath before approving.
3. **The PR says what should change and what should not.** "The host should stop apologising twice in a row; nothing else should move" is a reviewable claim; "improved the host prompt" is not. The suite's metrics table is read against that claim.
4. **No per-learner text in a prompt file.** Learner text enters through declared slots wrapped by `listener_said()`. The review pass greps the diff for anything that looks like a name, a place, or a quote.
5. **The cached prefix is sacred.** Anything above `cache_prefix_ends_at` is shared across learners and calls; moving a line across that marker changes the cache hit rate and therefore cost and latency. The PR says whether the prefix changed; the `cache_hit_low` alarm catches what the PR missed.
6. **Pinned roles** (the rater, per four-week window) cannot be bumped inside the window; CI refuses.
7. **A prompt version rolls back by reverting the PR** and cutting a release. There is no admin prompt editor and there will not be one.
8. **Bibles are Muath's** (CODEOWNERS, ADR-25.7): host and Salma bibles change only with Muath's approval, because they are the characters. The AI review pass checks every bible change against the laws and the ban lists first.
9. **Model changes are prompt changes.** Changing a role's model in `vendors.yaml` runs the same suites; a new model version from a vendor (same name, new weights) is caught by the nightly, and the agent opens a PR that re-baselines or rolls the model pin back.
10. **Consent texts, the privacy notice and crisis resources** are not prompts, but the same discipline applies: they are built from `legal/`, versioned in `packages/native/<lang>/`, checked against the self-review checklist (`legal/00-self-review-checklist.md`, ADR-25.3) by the review pass, changed only with Muath's approval, and never edited for style by the agent.

## 5. What the review pass checks in this product

The review pass is a fresh model session that reads the PR, the story and this list; it has not seen the authoring session. Beyond "does it work", in this order:

1. **Laws.** Does anything on screen or on air break one of the twelve laws (no points, streaks, levels; no autoplay or "next episode" control in the player, only the "Next one" button on Today while the portion remains; no "you are wrong"; claims only through the gate)? The law-furniture lint and the law-word scan catch words; the review pass catches intent.
2. **Learner isolation.** Every new query has `learner_id` and runs under RLS; no new table without a policy; no cross-learner read anywhere, including in admin pages (one learner per page).
3. **Learner text.** Does the change log, trace, email, push or send to a vendor anything the data-handling page forbids? Does a new Inngest event carry text? Does a new log field have a name the scrubber refuses?
4. **Cost.** Does it add a vendor call? If so, is it in the middleware, priced, and on the cost page? Does it move a line across the cache prefix? Does it add a retry?
5. **Deletion.** Does it create a new kind of learner object? Then `audio/expire`, `learner/purge-audio`, `learner/delete` and `privacy/verify` need to know about it in the same PR.
6. **Kill switch.** Can Muath turn it off without a deploy?
7. **Fakes and fixtures.** Does the fake adapter still agree with the real one? Did a golden set change, and if so is the reason a real-world case, not a test that was in the way?
8. **Migrations.** Additive; downgrade works; the previous image still runs against the new schema.
9. **Security paths.** Does the change touch auth, keys, media URLs, the feed or deletion? Then the separate security review pass must also be green (handbook 04 §3, ADR-25.11), and the review pass checks that the PR says so.
10. **The story.** Does every acceptance criterion have a named test that fails without the change? Does the change stay inside the story, or did it invent something the canon does not say (then it is blocking, and the question goes to Muath)?
11. **The boring parts.** Types, names, tests that test the thing, no dead code, no TODO without a story.

## 6. Dependencies

- `uv.lock` and `pnpm-lock.yaml` are the truth; Dependabot opens weekly PRs for patch and minor; majors are a deliberate PR with a reason.
- A new dependency needs one sentence in the PR on why the standard library or an existing dependency does not do it. Vendor SDKs are allowed only inside `forone.adapters`.
- `pip-audit` and `pnpm audit` on every PR and in the nightly; a critical finding is a P2 and fails CI when a fix exists (ADR-25.11).
- No agent framework inside the product (PRD 14.3 forbids it); the pipeline is explicit functions and the roles are pipeline steps. That the code is written by a coding agent changes nothing here.

## 7. Documentation in the repo

- Architecture decision records in `docs/adr/NNNN-<slug>.md`, one page, same headings (context, decision, consequences). ADR-0001 is the language package layout (handbook 01 §4). The agent never writes an ADR on its own: a decision that would change an architecture document goes to Muath first, and only after Muath decides does it get an ADR and a one-line note at the top of that document.
- Every package has a `README.md` of under a page: what it owns, what it must not import, how to test it.
- The handbook (`engineering/`) is edited by PR like everything else; a rule that nobody follows is deleted, not left to rot.
