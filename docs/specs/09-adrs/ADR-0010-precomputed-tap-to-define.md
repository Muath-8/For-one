# ADR-0010 — Pre-computed tap-to-define over on-demand generation

**Status:** Accepted · 2026-08-08 · Owner: 07-ai-spec

## Context

Every word of the episode transcript and every word of the article is tappable, and a tap opens a popover with the meaning in the user's native language, the part of speech, and one example sentence (PRD 5.5). 00 §8 budgets that popover at **under 300 ms**.

Three things make this harder than a dictionary lookup:

1. **Meaning is context-dependent.** A word with four senses needs the sense that is actually in play in this sentence, or the popover is worse than useless — it teaches the wrong thing at the exact moment the user trusted it.
2. **The language set is open.** ADR-0002 commits to every language supported by both providers, in every native-language pairing. There is no bounded set of dictionaries to license.
3. **Not every language has spaces.** The design document names Thai, Chinese, Japanese, and Khmer as requiring a segmentation service, and states that segmentation must align with tap-to-define pre-computation. Whatever decides what a "word" is must be the same thing that defines it, or taps land on units that have no entry.

A session produces roughly 1,250 tappable words across the transcript and the article.

## Decision

**Definitions are pre-computed at content-generation time, in two model passes, into a cache shared across all users of a language pair. Nothing is generated at tap time.**

The two passes are `PRM-lexical-index@v1` and `PRM-definitions@v1`, both on `MDL-lexicon` (`google/gemini-2.5-flash-lite`).

*Pass one* walks the transcript and article and emits, per tappable unit: surface form, character offset, lemma, part of speech, and a **sense key** — a short, stable, reusable identifier for which meaning is in play. It is verified deterministically: reassembling the surfaces by offset must reproduce the source byte-for-byte, which catches segmentation errors mechanically rather than by inspection.

*Pass two* runs only for `(lemma, pos, senseKey)` triples that are absent from the cache, keyed on `(languagePackageId, nativeLanguage, lemma, pos, senseKey)`. The prompt is given no user-specific content and is explicitly told the example sentence must not be about the passage it came from — which is what makes an entry safely reusable in another user's show on another day.

The full definition set for an episode ships with the transcript payload, so a tap is a local lookup with no network hop at all. The 300 ms budget is spent on rendering.

## Alternatives considered

**Generate on demand at tap time.** The obvious design, and it fails the budget outright. A tap would need a network round trip plus a model call: 250–800 ms at p95 even on the fastest tier, before considering mobile networks. Meeting 300 ms is not possible, and the honest version of this design puts a spinner inside a popover — friction in the one interaction that must feel like the app already knew. It is also unbounded: a user reading closely can tap fifty words, and the cost scales with curiosity, which is precisely the behaviour the product wants to encourage.

**License static bilingual dictionaries per language pair.** Rejected on two grounds. Licensing roughly a hundred target languages against roughly a hundred native languages is not a procurable artefact, and even where a dictionary exists it returns all senses of a word with no way to pick the one in this sentence — pushing disambiguation back onto the reader at their weakest moment.

**Hybrid: pre-compute frequent content words, generate rare ones on demand.** Rejected. It creates two code paths, two latency profiles, and two failure modes to save roughly $0.007 per cycle. The saving is not worth one branch, let alone the branch appearing in the user-visible latency.

**Client-side lemmatisation with a shipped model.** Rejected: multiplies bundle size across a hundred languages, still cannot disambiguate senses, and moves a correctness problem onto the least controllable runtime in the system.

## Consequences

- **Cost is 1.6% of the cycle envelope** — $0.0150 across both passes (07 §10.2, lines 7 and 8), against $0.93 total. This is only true because `MDL-lexicon` is pinned to the cheapest tier in the matrix; the lexical index alone emits ~17,500 output tokens per session, which would cost $0.26 on the authoring tier and make this decision indefensible. The model pin and this ADR stand or fall together.
- **The cache compounds.** Hit rate runs 0% on a user's first session and roughly 93% by their tenth, because the cache is global to a language pair rather than per user. A mature language package generates almost no new entries, so marginal cost falls toward the index pass alone.
- **One bad entry reaches every user of that language pair.** This is the real cost of a shared cache and it is mitigated deliberately: 07 §13.5 samples 20 entries per language per week for native-speaker review, weighted by tap count; a rejected entry is deleted, which forces regeneration on next encounter, and is added permanently to the regression eval set.
- **The lexical index pays for itself three times.** It is the definition key source, the word-segmentation service the design document requires for space-less scripts, and the token boundary source for the word-synced transcript highlighting. One pass, three problems, one place to fix a segmentation bug.
- **Payload size.** Roughly 1,250 units at ~60 bytes each is ~75 KB uncompressed, ~20 KB gzipped, shipped once with the transcript. Acceptable on mobile; it replaces up to fifty network round trips.
- **Storage grows with vocabulary, not with sessions.** Definition rows are bounded by the language pair's word-sense inventory, so the table converges rather than accumulating per user.
- **A degradation path exists and remains pre-computed.** When pass one fails its reassembly check twice, that chunk falls back to the language package’s deterministic tokenisation rule. Pass two resolves every resulting sense before the episode or article becomes definition-ready. No tap triggers EP-50, a model call, or any other network request; the feature degrades in segmentation quality, never in latency or availability. This amendment removes the contradictory on-demand fallback while preserving the decision’s one-path rule.
