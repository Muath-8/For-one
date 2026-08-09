# ADR-0002 — One package-generation pipeline for all provider-supported languages

**Status:** Accepted (user-ratified 2026-08-08)

## Context

The architecture is language-agnostic by law (source PRD v2.0 Part 13): prompts, taxonomies, band descriptors, duo personas, dialect lists, and voice inventories are per-language content packages, not code. The open question was launch scope. The product owner's standing answer: every language supported by the TTS/STT provider. That collides with the concept document's discipline ("one show, one language, one person who loves it") only if packages require hand-authoring — ~30 languages of hand-authored duos is months of editorial work.

## Decision

Build **one package-generation pipeline** and launch with packages for **every language supported by both `eleven_flash_v2_5` (TTS) and `scribe_v2` (STT, ADR-0019)** — the intersection catalog enumerated as seed data in 06-data-api-spec. The pipeline (`MDL-package` / `PRM-package-generation` in 07-ai-spec) drafts each package's duo personas, localized error taxonomy, band descriptors, and dialect list as structured, human-reviewable artifacts. The first language is built through the exact same pipeline — the enforcement rule from PRD Part 13.4 — so adding a language is running the pipeline plus review, never re-architecture.

## Alternatives considered

1. **Hand-author 3–5 flagship languages, defer the rest.** Rejected by the product owner; also creates a two-tier codebase risk where the flagship path stops exercising the package mechanism.
2. **Hand-author everything.** Rejected: editorial cost scales linearly with languages and would dominate the schedule for content the learner mostly experiences through generated episodes anyway.
3. **Ship packages with zero review.** Rejected: duo personas and taxonomy localizations are trust- and quality-critical; the pipeline outputs are reviewable artifacts, and the quality gate still checks every generated episode at runtime.

## Consequences

- Voice inventory per language is whatever ElevenLabs offers at launch (target 12 per PRD Part 7.8; fewer never blocks character creation).
- 06 seeds the language catalog with one default dialect per language; dialect variants exist only where distinct voices exist. **Dialect rule (amended after 06 §15.2):** every language ships exactly one dialect unless ElevenLabs' voice inventory supports a distinct authored duo for a second variant, in which case at most two ship at launch (the 26+6 seed in 06 §15.2); the intake dialect step is skipped when only one exists. Additional variants are seed changes gated on voice availability, never code changes.
- Package quality becomes an eval target in 08 (multilingual spot-checks, native-speaker review sampling) rather than a launch blocker per language.
- If a language's real-world quality proves inadequate, it is removed from the catalog by seed change — no code change.
