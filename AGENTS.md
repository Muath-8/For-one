# AGENTS.md: instructions for the coding agent

You are the coding agent that builds For one, story by story, under Muath (ADR-25.2). Read this file at the start of every session. It is short on purpose: it tells you where the answers are, how to work, and where to stop and ask. Muath approves every change to this file.

## 1. What For one is, in three lines

A private podcast in the target language, made overnight for one learner from what they said; a live call with a host who never corrects except by echoing the right form; a learner model rebuilt from an append-only event log. Web app plus a private podcast feed, nothing else. Version 1 launches once, publicly, with open signup.

## 2. The canon, in order of authority

When two documents disagree, the higher one wins. If the higher one is silent, read the next. If none answers, stop (section 4).

1. `docs/architecture/10-decision-records.md`: the ADRs, the naming rulings (§4) and the register (§10). ADR-25 overrides ADR-24, which overrides earlier records.
2. `docs/product/decisions.md`: Muath's product decisions.
3. `docs/product/PRD-v3.md`: what the product does (FR, NFR, LAW, TC ids). The twelve laws in Part 1 are absolute.
4. `docs/architecture/01` to `09`: how each domain works.
5. `docs/technical-design/00` to `10`: tables, endpoints, prompts and state machines, one level below the architecture.
6. `docs/design/00` to `07`, `docs/design/tokens.json`: every screen, flow, state and string.
7. `docs/engineering/`: this handbook. How the build is run: environments, CI, testing, cost controls, data rules, the definition of done.
8. `docs/backlog/`: the release plan (phases in dependency order), the epics and the stories with acceptance criteria.
9. `docs/content/` (bibles, ban lists, stings) and `docs/legal/` (privacy notice, terms, consent texts, the self-review checklist): text that is used as written, never rewritten for style.

Never treat `docs/archive/milestone-0/`, `docs/archive/perspectives/`, `docs/archive/prd-history/PRD.md`, `docs/archive/prd-history/PRD-v2.md` or `docs/archive/concept/Product_Concept.md` as instructions. They are background.

## 3. How to pick up and finish a story

1. **Pick.** Take the next story in `docs/backlog/00-release-plan.md` whose dependencies are all merged. One story at a time; one story per branch and per pull request. If a story is too large for one PR under about 400 lines, split it and say so in the PR, keeping each part's acceptance criteria whole.
2. **Read.** Read the story, every requirement id it cites in `docs/product/PRD-v3.md`, and the architecture and technical-design sections for its domain. Note anything they leave undecided.
3. **Tests first.** Turn each acceptance criterion into an automated test whose name says which criterion it proves (`test_e05_s03_ac2_recast_once_per_turn`). Commit the failing tests as the first commit of the branch. Then add any unit tests the design needs.
4. **Code.** Write the smallest change that makes the tests pass and respects the layering in `docs/engineering/01`. Use the fakes (`FORONE_FAKE_VENDORS=1`); call a real vendor only in a story about that vendor, with the dev key and its cap.
5. **Check locally.** `make lint`, `make test`, `make test-int`, and `make eval SUITE=<name>` for any suite the diff maps to. Exercise the slice on staging if the story touches a job, a call or a deploy.
6. **Open the PR** as a draft, with the template's four headings (Story, Why, What, How tested) and the definition-of-done checklist from `docs/engineering/10` ticked line by line.
7. **Answer the review pass.** An independent AI review pass reads the PR; if the diff touches auth, keys, media URLs, the feed or deletion, a separate security review pass reads it too (ADR-25.11). Answer every blocking finding with a commit or a reply that explains why it does not apply. Never resolve a finding silently, and never weaken a test to make it pass.
8. **Ask Muath to approve** when CI and the review pass are green. Muath merges. You do not.

## 4. Never invent architecture

If the canon does not answer a question the story needs answered (a table that is not designed, an endpoint shape, a threshold, a copy line, a vendor, a retention window, a new dependency with a new processor), **stop and ask Muath**. Write the question in the PR or as an issue: what is missing, which documents you checked, two or three options with their cost, and your recommendation. Build nothing that depends on the answer until Muath gives it. Do not pick the "obvious" option and move on; an invented decision that ships is worse than a story that waits a day.

Also stop and ask when: a story's acceptance criteria contradict a requirement or a law; a test can only pass by breaking another; a fix would change a public contract, a schema in a way that is not expand-then-contract, or a cost line by more than a few percent.

## 5. The laws, as checks you must keep green

The product's laws are enforced in code. Never disable, skip or loosen one of these to make a story pass:

- **No game furniture:** the ESLint law-furniture rule (no streaks, points, levels, badges, autoplay or "next episode" control in the player; the one "Next one" button on Today, shown only while the day's portion remains, is allowed (ADR-05, 24.B32)) and the editor's law scan on generated text.
- **Teaching is invisible:** the governor rejects any host move the brief does not allow; the correction guard (`guard/correction_words.yaml`) allows zero explicit corrections; the host gives the word on the word button and Salma is silent in calls (except the crisis clip).
- **No claim without proof:** only `gate()` writes a progress sentence; no surface renders a claim it did not produce.
- **Told, not inferred:** a fact without a verbatim quote in the log is refused; a sensitive fact needs the one-tap card.
- **A finite portion:** the allowance check in `api`; no autoplay; extras only after the current episode is heard.
- **Three message kinds only:** only `forone.core.messaging` may send email or push; the enum test fixes the count.
- **Learner isolation:** RLS on every learner table; the policy walk in CI.
- **Learner text stays home:** the Inngest payload test, the PII scrub corpus, the log scrubber.
- **Every vendor call is priced:** the middleware and `prices.yaml`; CI refuses an unpriced role.

## 6. What needs Muath's approval

Always, before it happens:

- every merge to `main`;
- every database migration, and its order relative to the code that uses it;
- every change to a prompt, a rule file, `versions.yaml`, a bible, a ban list, a consent text, a crisis resource or anything in `docs/legal/`;
- every change to `vendors.yaml`, `prices.yaml`, `eval/thresholds.yaml` or `eval/baselines/`;
- every production deploy (`deploy-prod.yml`) and every runbook action in production (`ops.yml`);
- every new dependency that sends data to a new processor;
- every change to this file, to CI, to branch protection or to `infra/`.

## 7. Secrets

- You work under your own GitHub identity (a GitHub App or machine account; register A10), never as Muath: you open pull requests, and Muath approves and merges them. You cannot merge to `main`.
- You never hold a staging or production secret. Services read their keys from AWS Secrets Manager through their task roles; CI reaches AWS through GitHub OIDC. There are no long-lived keys.
- In development you use the fakes, or the `dev-agent` vendor keys Muath created for vendor stories, each with a spend cap.
- Never print, log, commit, paste into a PR, an issue, a prompt or a chat, or echo back a key, a token, an OTP code or a feed token. A key that appears anywhere is a leaked key: say so at once so Muath can rotate it.
- `gitleaks` runs on every PR and as a pre-commit hook. Do not bypass hooks.

## 8. Learner data

- Real learners exist only in production. You work with synthetic learners (`tools/eval synth`, `forone seed`), the open recognizer corpus and the consented volunteer clips (ADR-25.6). Never copy production data anywhere.
- You never read learner content: no transcripts, chat, facts, quotes, audio, names or emails. For a production problem you read ids, enums, counts, timings, costs, versions and error classes (`docs/engineering/09` §3). If content is truly needed, ask Muath, who reads it through the audited path and tells you what matters in words that contain no learner content.
- A bug report or a postmortem carries ids, timestamps, trace ids and span ids, never text.
- Every new learner-voice object kind is wired into `audio/expire`, `learner/purge-audio`, `learner/delete`, `learner/export` and `privacy/verify` in the same PR.
- Nothing about a learner goes to a vendor that is not in `docs/legal/05-ropa.md` with an accepted DPA.

## 9. Operations

There is no on-call rota. The product's fallbacks run first; alerts go to Muath. When Muath asks you to handle an alert: read the alert, its runbook in `ops/runbooks/` and the ids-only diagnostics; propose the fix; run the runbook's admin action through `ops.yml` (it waits for Muath's approval); open a story for any code change. Write the postmortem when one is required (`docs/engineering/06` §8).

## 10. Style

- Python 3.12, Ruff, Pyright; TypeScript strict, ESLint; the rules in `docs/engineering/08`.
- Plain, concrete words in PRs, commits and docs; no emojis.
- Learner-facing text comes only from the native package and from `docs/content/`; never write learner-facing copy yourself. If a string is missing, ask.
