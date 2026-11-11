# Legal and privacy texts (drafts for counsel)

> **Draft for counsel. Not legal advice.** Every file in this folder was drafted on 2026-11-12 from the architecture (mainly [architecture/07](../architecture/07-security-privacy-and-compliance.md) and [ADR-24](../architecture/10-decision-records.md#adr-24-the-owed-decisions-taken-on-delegation-2026-11-12)), the PRD ([PRD-v3](../PRD-v3.md)) and the Milestone 0 consent. None of it is in force. Counsel must confirm every working position marked in [00-counsel-question-pack.md](00-counsel-question-pack.md) and approve the wording before anything ships to a learner.

| | |
|---|---|
| Owner of record | Muath (owner actions A1, A8 and A9 in [10-decision-records §10](../architecture/10-decision-records.md#10-register-owner-actions-and-pending-measurements)) |
| Status | Draft 0.1, 2026-11-12. Unreviewed by counsel. |
| Counsel answers due | **2026-11-17** for the questions in pack part A (register A1). **2027-02-15** for the review of every text here (register A8). The beta does not open (plan of record 2027-03-17, ADR-24.11) without reviewed consent text. |
| Milestone 0 addendum | Two parts (ADR-24.B10). Part 1 (vendor tests) is signed before any pilot clip goes to a vendor. Part 2 (the bridge, re-onboarding, fixtures and import) is signed by **2026-12-15** (register A9, ADR-24.B28); anyone who does not sign keeps the original promise of deletion by 2026-12-31. |
| Placeholders | `[Company legal name]`, `[Address]`, `[Governing law]` and the others in square brackets are facts only Muath or counsel can supply. Nothing in these drafts invents them. |

## The files and where each one ships

Learner-facing texts are written once in English here. After counsel approves them they are copied into the English native-language package `packages/native/en/` (the universal fallback, ADR-02) and translated by a native speaker into every other native package that exists when the beta opens (2027-03-17) (`native/ar` is certain). Each shipped copy gets a version id (`YYYY-MM-DD.n`, the date counsel approved it), and every learner acceptance records that version (`consent_change.text_shown_version`, 07 D4).

| File | What it is | Audience | Ships to | Review |
|---|---|---|---|---|
| [00-counsel-question-pack.md](00-counsel-question-pack.md) | The questions counsel answers, each with our working position, the facts and what it unblocks | Counsel | Sent by Muath on 2026-11-13 | A1 (2026-11-17), A8 (2027-02-15) |
| [01-privacy-notice.md](01-privacy-notice.md) | The privacy notice (GDPR Art. 13), with the paragraphs that differ per regime marked | Learners | `packages/native/<lang>/privacy/notice.md`; rendered at A1 (link), A8/A9 (acknowledged as `privacy_notice`) and in Controls; also the public page `/privacy` | A8 |
| [02-terms-of-service.md](02-terms-of-service.md) | Terms: plans, trial, renewals, plan changes, failed payment, cancellation and refunds, acceptable use, AI disclosure, deletion | Learners | `packages/native/<lang>/legal/terms.md` (ADR-24.B17) and the public page `/terms`; accepted as consent kind `terms` with its version at A9 and on any material change (ADR-24.B18). Refunds: full refund within 14 days of the first payment (ADR-24.B16) | A8 |
| [03-consent-texts.md](03-consent-texts.md) | Every in-app consent and notice string, with string ids | Learners | Consent kinds to `packages/native/<lang>/consent/consent_texts.yaml`; the other strings to the native package's `ui_strings/` | A8 |
| [04-dpia.md](04-dpia.md) | Data protection impact assessment | Counsel, Muath, a regulator on request | The source; the code repository's `docs/` links here (ADR-24.B11) | A8 |
| [05-ropa.md](05-ropa.md) | Record of processing activities, with the retention schedule | Counsel, Muath, a regulator on request | The source; the code repository's `docs/` links here (ADR-24.B11). The machine-readable processor register that CI reads (07 §4.9, handbook 09 §9) must match it | A8 |
| [06-crisis-protocol.md](06-crisis-protocol.md) | The crisis protocol as built, the clip wording (English, Arabic draft), resources per country, SB 243 duties, reporting | Counsel, Muath; a public summary for the website | `packages/languages/<target>/crisis/` and `packages/native/<lang>/crisis/` (clips, `resources.yaml`, `keywords.yaml`); public summary at `/safety` | A8 (wording by 2027-02-15, ADR-24.15) |
| [07-milestone-0-consent-addendum.md](07-milestone-0-consent-addendum.md) | Two-part addendum for the 15 pilot learners (ADR-24.B10): Part 1 vendor tests, Part 2 the bridge, re-onboarding, import and de-identified fixtures | Pilot learners | Two Google Forms, like the pilot consent | Part 1 signed before any clip leaves; Part 2 by 2026-12-15 (A9, ADR-24.B28) |
| [08-reviewer-confidentiality.md](08-reviewer-confidentiality.md) | Confidentiality agreement for native readers and taggers | Reviewers, taggers | Signed before first login; the date is recorded in `staff_accounts.agreement_signed_at` (07 §4.13) | A8 |

## Rules for editing these texts

1. Counsel edits the wording. Engineers never change a consent or notice text (handbook 09 §5); a text change is a new version, and a changed consent is asked again at next open (07 §4.3 rule 4).
2. A fact in these texts must match the system. If the product changes a window, a processor or a retention period, the text changes in the same pull request, and the privacy notice's processor list is rendered from the register so the two cannot drift (07 §4.9).
3. The beta copy must never promise less than the Milestone 0 consent did ([milestone-0/02-consent.md](../milestone-0/02-consent.md); 07 §10 #2).
4. Learner-facing texts are short, plain and in the present tense, with no exclamation marks (design 06 §4). Salma speaks the strings marked "spoken" in [03-consent-texts.md](03-consent-texts.md).

## Contradictions found while drafting

Drafting found places where the architecture, the PRD, the design and the handbook disagreed on privacy, retention or billing facts. Each one is ruled in ADR-24's consistency rulings (24.B1 to 24.B15, [10-decision-records](../architecture/10-decision-records.md)), and these texts follow the rulings; where a text depends on one, it cites "per ADR-24.Bn".
