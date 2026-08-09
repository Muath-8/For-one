# ADR-0003 — "Your show" sheet is a trust surface, not settings

**Status:** Accepted · 2026-08-08 · Supersedes nothing · Referenced by `00-decisions.md` §1, §9.3

## Context

Product law 1 forbids lesson furniture, and PRD Part 16 explicitly excludes "settings screens of any kind". Yet a real product still needs somewhere for the user to see their cast, correct what the show believes about them, manage voice-recording consent, understand that the hosts are AI, and — after ADR-0001 restored data rights — export or delete their account.

The tension is that these are normally called *settings*, and a settings screen drags its whole vocabulary with it: preferences, toggles, defaults, advanced options. That vocabulary would immediately reintroduce the software-tool framing the product is built to avoid, and it would invite behavioural preference controls ("difficulty", "correction level") that violate law 2 — the system owns difficulty, targets, corrections, and sequencing, invisibly.

At the same time, ADR-0001 makes two irreversible, legally meaningful actions (export, delete) part of v1. Those cannot live in conversation alone: a destructive action needs a stable, findable, confirmable surface.

## Decision

There are **no settings or preferences screens**. One sheet, "Your show", is the single non-conversational surface, and it is framed as a **trust surface**: it answers "what does this thing know about me, who is on it, and what can I do about it". It holds exactly five sections, matching the binding information architecture in `00-decisions.md` §1 and the screen contract in 02:

1. **Cast** — the roster, character creation, editing, and retiring.
2. **What the show knows** — the plain-language knowledge summary of life facts and interests, with inline correction. The language profile is never shown.
3. **Voice tape** — current recording-consent state, what is stored, and revocation.
4. **About this AI show** — AI disclosure.
5. **Account essentials** — email state, sign-out, **Export my data**, and **Delete my account**.

Every **behavioural** preference stays conversational. Changing what the show does is said to the show, never configured.

## Alternatives considered

**A settings screen with a small, curated set of options.** Lost because there is no stable boundary between "curated" and "grown". Once a settings screen exists, every future feature has an obvious place to add a toggle, and the pressure to expose difficulty or correction level becomes structural. The product law would be defended by discipline rather than by architecture.

**Everything conversational, including export and deletion.** Lost on safety and on trust. A deletion triggered by natural-language intent is ambiguous by construction, cannot carry the type-to-confirm pattern, and cannot reliably present consequence text. Destructive actions need a deterministic surface with a safe default, which is exactly what conversation is not.

**A "privacy centre" separate from cast management.** Lost because it splits one question — what does this thing know and who is on it — across two destinations, and it names a compliance concept rather than a product one. The user's mental model is "my show", not "my privacy settings".

**Per-character configuration panels.** Lost because characters are created and edited by talking to the show (PRD 7.2, 7.5). A configuration panel would turn a designed conversational moment into form-filling and would expose the chassis mapping, which is specified as invisible.

## Consequences

- 02-ux-spec owns the sheet as a screen with states, and writes the export and deletion copy in the established legal and consent voice (`00` §9.3 delta 1).
- Any future request for a user-facing preference must first be answered conversationally. Adding a control to this sheet requires an ADR, which is the intended friction.
- The design doc's "Unsupported data actions" paragraph and the matching QA-gate line are superseded; the sheet now carries two irreversible actions and needs the destructive-action design rules (safe choice first, verb names the result, one confirmation).
- Discoverability of export and deletion depends entirely on one sheet. 02 MUST place Account essentials so it is reachable in two taps from any surface, and 08 MUST cover that path as a test case.
- The knowledge summary becomes load-bearing for trust: it is the only place a user can see and correct what the system believes. Its honesty wording ("Stop using this in the show" = dormancy, distinct from deletion) is normative, not decorative.
