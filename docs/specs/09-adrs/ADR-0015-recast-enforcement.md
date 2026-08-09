# ADR-0015 — Recast enforcement by design, not by instruction

**Status:** Accepted · 2026-08-08 · Owner: 07-ai-spec

## Context

Two product laws govern how the show responds to a user's language errors (00 §1, laws 5 and 7): in-flow correction is **recast-only**, and recasts **must be socially natural** — hosts never grade or praise per turn, and explicit correction happens only when the user asks for it.

A recast is the correct form embedded in a reply that carries its own conversational point. "I go to cinema yesterday" earns "You *went*? What did you see?" — the fix is delivered, the conversation moves, and nothing was marked.

This is the hardest behaviour in the product to guarantee, for three reasons. It is a **negative constraint** in an unscripted live conversation, where the failure mode is the model doing something helpful. It is **invisible in aggregate metrics** — error rates fall either way, so a dashboard cannot tell a natural recast from a clumsy one. And a single violation is **immediately obvious to the user**, who came for a show and got a correction; the concept document's framing is that if the user notices the pattern afterward that is fine, but a host that grades is never fine.

The tempting design is a well-written prompt instruction. An instruction is a hope, and law 7 is absolute.

## Decision

**Recasts are enforced by four mechanisms working together: they are authored ahead of the call, verified deterministically, capped and unmarked at delivery, and gated at release by a human rubric with an absolute floor.**

**1 — Authored ahead, not improvised.** `PRM-callin-brief@v1` receives the user's recent error forms and writes, before the call begins, one natural carrier sentence per form: a sentence that would make sense in *this specific conversation* and happens to contain the correct form. The prompt states that a sentence whose only purpose is the form is a product-law violation, and instructs the model to **omit** an item it cannot carry naturally, recording why. An omitted recast is a correct output.

**2 — Verified in code.** Every carrier sentence must contain the correct form and must not contain the error form, after the language package's normalisation. A sentence failing that check is dropped rather than regenerated. Fewer recasts is always the safe direction.

**3 — Capped and unmarked at delivery.** `PRM-realtime-host@v1` allows at most one recast per reply, often zero, and forbids pausing on it, repeating it, marking it with tone, or saying "you mean". The host reports which prepared recast it used through the `⟦meta⟧` side channel, so delivery is **measured rather than assumed** and can be correlated with whether the form later appears correctly in the user's own speech.

**4 — Gated at release.** 07 §13.3 defines a 1–5 naturalness rubric scored by a native speaker on an unmarked transcript, where 5 means the reviewer cannot identify which turn contained a recast. Release requires a mean of **≥4.0 with no single score of 1**, and separately **zero** turns containing praise or grading of language. Those are blockers, not percentages.

## Alternatives considered

**Prompt instruction alone.** Rejected. It is unverifiable, it degrades silently when a pinned model is updated behind its ID, and it puts the hardest judgment in the system — "is this sentence natural in this conversation" — inside a 450 ms live inference with no check behind it.

**Post-hoc filter on host turns.** Scan each generated turn and block ones that read as corrections. Rejected on two counts. It costs a full model pass inside a 1,500 ms end-to-end budget that has 300 ms of headroom, and a filter cannot make the distinction that matters: natural and unnatural recasts contain the same words in the same shapes. Naturalness is a judgment, not a pattern.

**A separate corrector model rewriting host turns.** Rejected as the worst option available. Two models producing one voice yields incoherent conversation; the rewriter has no access to why the turn said what it said; and it doubles both cost and latency on the most latency-critical path in the product to make a voice less consistent.

**Drop in-flow recasting entirely; correct only in the Weekly Proof.** Genuinely tempting, and it would eliminate this risk completely. Rejected because the recast is the mechanism the product's pedagogy rests on — the concept document's line is that correction never happens and recasting always does. Removing it leaves a conversation partner that never moves the user's language forward, which fails the product rather than the law.

## Consequences

- **Recast coverage is lower than a maximalist design would produce.** Some error forms get no recast in a given session because no natural carrier existed for that subject. This is accepted and is not a loss: the target lifecycle (PRD 10.10) keeps the form active and brings it back until it is produced correctly unprompted three times. A skipped recast costs one session, never a correction.
- **Recast delivery becomes measurable.** The `⟦meta⟧` channel writes which recast was used into the session record, which makes "did the fix take" a query joining delivered recasts against later `error_observations` — the evidence the Weekly Proof's named wins are built from.
- **One extra pipeline stage and $0.019 per cycle** for `PRM-callin-brief` (07 §10.2, line 6). The brief pays for itself twice over: it is also what makes the live host's system prompt fully static and therefore cacheable, which is worth roughly $0.033 per call in avoided uncached reads and roughly 200 ms of time-to-first-token.
- **Recast policy is a prompt-version change plus an eval run**, not a code change. The carrier-sentence verifier is the only code involved, and it checks a mechanical property.
- **The release gate can block a ship on one transcript.** A single naturalness score of 1 stops a release. That is intentional: 00 law 7 admits no percentage, and a threshold that bends under delivery pressure is not a threshold. 08 owns the test cases that carry this gate.
