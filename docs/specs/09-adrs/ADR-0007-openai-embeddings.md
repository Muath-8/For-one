# ADR-0007 — OpenAI embeddings alongside OpenRouter

**Status:** Accepted · 2026-08-08 · Owner: 07-ai-spec

## Context

00 §3 pins OpenRouter as the gateway for **every LLM call**, and the reason is sound: one client, one auth surface, one cost stream, one fallback mechanism, and no vendor SDK sprawl. Embeddings sit outside that rule in the same table, pinned to OpenAI `text-embedding-3-small` at 1536 dimensions. This ADR records why a second AI vendor is worth the exception.

Embeddings serve one job in this product: retrieval inside a single user's learner file (07 §6.2) — canonical fact sentences, session summaries, character-memory notes, interest labels. The workload has four properties that decide the choice:

- **Multilingual by requirement.** ADR-0002 commits to every language supported by both the TTS and STT providers. Fact sentences are stored in the user's native language, which means the embedding model must behave across roughly a hundred languages, not across English plus a long tail.
- **Tiny.** Roughly 920 tokens per session (07 §10.2, line 18) — $0.00002 per cycle, 0.002% of the envelope. Cost is not a selection criterion here; correctness and availability are.
- **Written once, read often.** Vectors are produced in the post-session pass and read on every generation. Latency at write time is irrelevant; the read is a local pgvector query.
- **Dimension-coupled to storage.** The column width is fixed at migration time. Switching models later is a schema change plus a backfill, not a config change.

## Decision

**Embeddings are called directly against the OpenAI API using `text-embedding-3-small` at the full 1536 dimensions. Every other AI call goes through OpenRouter.**

The one-gateway rule is scoped to *completions*, which is where it earns its value — fallback chains, model routing, and per-call cost accounting are completion concerns. Embeddings have none of those needs: there is no fallback chain to express (07 §11 row AIF-14 defers instead), no routing decision, and one flat rate.

Dimensions are **not** truncated. `text-embedding-3-small` supports Matryoshka shortening, and 768 dimensions would halve the index size. At the corpus size this product produces — a few thousand vectors per user — halving the index buys nothing measurable and costs retrieval quality that shows up as a worse callback in an episode.

## Alternatives considered

**Route embeddings through OpenRouter.** The appealing option, because it preserves the one-gateway rule exactly. Rejected: OpenRouter's surface is built around chat completions, its embeddings support is not a first-class or consistently available path across providers, and routing through it adds a hop and a dependency without removing either. The rule would be preserved in letter while the system got less reliable.

**Google `gemini-embedding`.** Strong multilingual quality, and Google is already a vendor through OpenRouter. Rejected because that last point is illusory — reaching Google's embedding endpoint means a direct Google API relationship, which is the same "second vendor" cost this ADR is weighing, with a less stable dimension and pricing history.

**Cohere `embed-multilingual-v3`.** Genuinely excellent at cross-lingual retrieval, which is close to this workload. Rejected on the same second-vendor logic plus a materially higher rate, buying quality this corpus size does not convert into better output.

**Self-hosted `bge-m3` or `multilingual-e5-large`.** Zero marginal cost and no vendor. Rejected decisively: 00 §3 contains no GPU runtime and 00 §4 commits to a modular monolith with exactly two satellites. Introducing an inference deployment to save $0.00002 per cycle is the exact failure mode the engineering standard names — complexity added where no requirement demands it.

**No embeddings; Postgres full-text search over facts.** Rejected: retrieval here is semantic and cross-lingual — a fact stored as "his sister is getting married in March" must surface for an episode about weddings without sharing a token with it. Lexical search cannot do that, and 07 §6.3 depends on it in five places.

## Consequences

- A second AI vendor relationship, a second API key, and a second provider to monitor. AIF-14 in 07 §11 governs the outage path: facts are written with `embedding_pending`, retrieval degrades to recency plus salience for that user, and a backfill job clears the queue. Degraded relevance for one session is the entire blast radius.
- The 1536-dimension choice is load-bearing on the schema (06). Changing embedding models later requires an `ALTER` plus a full re-embed. That migration is cheap by construction: a 200-session user holds roughly 3,000 tokens of embeddable text, so re-embedding the entire corpus of ten thousand such users costs about $0.60. Lock-in is nominal.
- Deletion is unaffected. Vectors live in our own `embeddings` table (00 §5); the provider retains nothing. Account deletion purges them in the same ≤24 h job as everything else (ADR-0001).
- The privacy inventory in 07 §12.2 gains one row. OpenAI receives canonical fact sentences, session summaries, character-memory notes, and interest labels — never raw transcripts, chat messages, scripts, or identifiers. No completion traffic is ever routed to this vendor.
- The one-gateway rule is now explicitly a **completions** rule. Any future non-completion AI capability (reranking, classification endpoints) must argue its own case in an ADR rather than inheriting this exception.
