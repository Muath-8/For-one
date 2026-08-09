# ADR-0016 — Adopt the existing design document as canonical, with bounded canon deltas

**Status:** Accepted

## Context

A complete design system and UI specification (`docs/For_one_Design_System_and_UI_Specification.md`, 2026-08-08) already exists: Paper/Booth/Proof environments, full token set, component system, per-screen compositions and states, copy catalog, i18n/RTL rules, WCAG 2.2 AA standard, and design QA gates. It was written against source PRD v2.0 — including that PRD's removal of export/deletion, which ADR-0001 has since reversed. The documentation program needed to decide: rewrite the design work into fresh specs (risking drift and quality loss) or adopt it.

## Decision

Adopt the design document as the canonical design authority. Specs 02-ux-spec and 03-design-system are its normative split — values, tokens, compositions, and copy preserved verbatim — plus only the bounded deltas and ratified additions enumerated by `00-decisions.md` §9.3. That live canon section, rather than a duplicated list here, owns their exact membership. Any other deviation between 02/03 and the design document is a defect.

## Alternatives considered

1. **Author 02/03 from scratch.** Rejected: the existing document is decision-complete and high quality; re-derivation invites contradictions and wastes the invested design judgment.
2. **Reference the design doc in place without splitting.** Rejected: the deliverable set requires 02/03 as the owning documents with traceable IDs, and the export/deletion delta cannot be applied to a document that must stay historical.

## Consequences

- The original file remains in `docs/` as historical source; `docs/specs/02` and `03` are the only citable design authorities.
- Phase-3 review includes a fidelity check: sampled values (hex, px, ms, copy strings) must match the source document exactly outside the deltas and ratified additions registered in 00 §9.3.
- Future design changes happen in 02/03 via ADR, never by editing the historical document.
