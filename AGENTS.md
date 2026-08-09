# For one — agent instructions

Before changing any project document, read these files in order:

1. `docs/HANDOFF.md` — current work state, review status, and recovery map.
2. `docs/specs/00-decisions.md` — binding cross-document canon.
3. The owning specification for the fact being changed, using the ownership map in `00-decisions.md` §12.

The current objective is to finish the implementation-ready specification set started in Claude Code session `82e6b944-cd07-4a0a-bb6e-c05f45cb4d8c`.

Rules:

- Treat `docs/specs/00-decisions.md` as binding. A contradiction with it is a defect.
- Treat `docs/For_one_Design_System_and_UI_Specification.md` as the adopted design authority, subject only to the deltas in `00-decisions.md` §9.3.
- Preserve one source of truth per fact. Change the owning document and make other documents cite it; do not duplicate values or enumerations.
- Preserve the ID schemes and traceability chain in `00-decisions.md` §2.
- Normative text uses RFC 2119. The banned normative words listed in `00-decisions.md` must not appear outside quoted copy or a rule that names the words.
- Do not call the specification set complete until independent review reports zero defects, all six implementation traces are BUILDABLE, and the final mechanical checks pass.
- Do not create `docs/specs/README.md` until Phase 3 reaches zero defects. README creation is Phase 4.
- Do not silently resolve contradictions by choosing whichever document is convenient. Apply the precedence and ownership rules, record a significant new decision in an ADR, and update the canon when the decision is cross-cutting.
- Do not ask the user about ordinary engineering choices. Make the best production-grade decision and record it. Ask only when a genuine product decision cannot be inferred safely.
- This folder is not currently a Git repository. Preserve files carefully and verify every edit directly.
