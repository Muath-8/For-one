# Legal and privacy texts

> **Self-reviewed against legal/00; not reviewed by a lawyer; see the triggers** ([00-self-review-checklist.md](00-self-review-checklist.md) §25).

For one has no lawyer (ADR-25.3). It stays lawful by conservative design: the strictest common rule applies to every learner, risk is designed out rather than argued, Paddle as merchant of record carries the payment-side consumer law, and every text here is checked against a written self-review checklist by an AI review pass and by Muath.

| | |
|---|---|
| Owner | Muath. He is the assessor for the DPIA and the RoPA and approves every text here (register A4) |
| Status | Written and self-reviewed against [00-self-review-checklist.md](00-self-review-checklist.md); not yet ticked by Muath. Public launch waits for every check to be ticked |
| Placeholders | `[Company legal name]`, `[Address]`, `[Governing law]` and the others in square brackets are facts only Muath can supply. Nothing here invents them |

## The design that replaces a lawyer

- GDPR-grade rights and controls for every learner, wherever they live; hosting in `eu-central-1`.
- Vendors under their standard data processing agreements with SCCs and a short transfer impact assessment each; the EU-US Data Privacy Framework where a vendor is certified.
- Paddle, as merchant of record, sells the subscription and carries tax, invoices, refunds and the EU withdrawal right.
- 18+ only; no voiceprints or speaker identification; voice storage off by default with deletion within 15 minutes; data use opt-in and off by default; no sensitive fact kept without the one-tap card; explicit consent at signup for what transcripts keep; AI disclosed in Salma's first line.
- Crisis help from a maintained international helpline directory, with SB 243-style duties for everyone.
- Only Muath can read learner content, every read is logged and shown to the learner, and the AI agent that builds For one never touches learner data.

## The files and where each one ships

Learner-facing texts are written once in English here. After Muath approves them they are copied into the English native-language package `packages/native/en/` (the universal fallback, ADR-02) and translated by a native speaker into every other native package that ships (`native/ar` is read by Muath, register A3). Each shipped copy gets a version id (`YYYY-MM-DD.n`, the date Muath approved it), and every learner acceptance records that version (`consent_change.text_shown_version`, 07 D4).

| File | What it is | Audience | Ships to |
|---|---|---|---|
| [00-self-review-checklist.md](00-self-review-checklist.md) | Every legal question with its final position, the official source and a check; and when a lawyer becomes necessary | Muath, the AI review pass | Stays here |
| [01-privacy-notice.md](01-privacy-notice.md) | The privacy notice (GDPR Art. 13), with the paragraphs that differ for UK and Saudi learners marked | Learners | `packages/native/<lang>/privacy/notice.md`; linked at A1 and A2, acknowledged at account creation, in Controls; the public page `/privacy` |
| [02-terms-of-service.md](02-terms-of-service.md) | Terms: plans, trial, renewals, plan changes, failed payment, cancellation and refunds, acceptable use, AI disclosure, deletion | Learners | `packages/native/<lang>/legal/terms.md` (ADR-24.B17) and `/terms`; accepted as consent kind `terms` with its version at account creation and on any material change (ADR-24.B18); refunds per ADR-24.B16 |
| [03-consent-texts.md](03-consent-texts.md) | Every in-app consent and notice string, with string ids, and the volunteer recording consent (ADR-25.6) | Learners; vendor-test volunteers | Consent kinds to `packages/native/<lang>/consent/consent_texts.yaml`; other strings to the native package's `ui_strings/` |
| [04-dpia.md](04-dpia.md) | Data protection impact assessment | Muath; a regulator on request | Stays here; the code repository's `docs/` links here (ADR-24.B11) |
| [05-ropa.md](05-ropa.md) | Record of processing activities, with the retention schedule | Muath; a regulator on request | Stays here; `docs/` links here. The machine-readable processor register that CI reads (07 §4.9, handbook 09 §9) must match it |
| [06-crisis-protocol.md](06-crisis-protocol.md) | The crisis protocol as built, the clip wording (English, Arabic), the helpline directory, SB 243-style duties, reporting | Muath; a public summary for the website | `packages/native/<lang>/crisis/` and `packages/languages/<target>/crisis/keywords.yaml`; the summary at `/safety` |

## Rules for editing these texts

1. A text change is a new version, and a changed consent is asked again at next open (07 §4.3 rule 4). The AI review pass checks every change against [00-self-review-checklist.md](00-self-review-checklist.md); a change with a failing check does not merge; Muath approves the merge.
2. A fact in these texts must match the system. If the product changes a window, a processor or a retention period, the text changes in the same pull request, and the privacy notice's processor list is rendered from the register so the two cannot drift (07 §4.9).
3. Learner-facing texts are short, plain and in the present tense, with no exclamation marks (design 06 §4). Salma speaks the strings marked "spoken" in [03-consent-texts.md](03-consent-texts.md).

## The residual risk, accepted

Muath accepts these risks by launching without a lawyer (ADR-25.3):

- **A position could be wrong.** The final positions in legal/00 rest on the official texts and regulators' guidance as read by Muath and an AI review, not on legal advice. A regulator or a court could read a rule differently: most likely on the basis for keeping special-category content in transcripts, on whether the hosts make the product a "companion chatbot" under SB 243, or on a country whose law the checklist does not cover. The design is chosen so that a different reading would most likely mean a text change or a stricter setting, not unlawful processing at scale.
- **No one reviews the texts independently.** An AI review pass and Muath check them; neither is a lawyer.
- **Laws change.** The checklist names its sources so the review can be repeated; it is re-run when a trigger fires and at least when a vendor changes, but a change in the law between reviews could go unnoticed for a while.
- **Some duties need a person outside the company.** An EU and UK representative is appointed if the company sits outside them (GDPR Art. 27; register A7). This is a paid service, not legal advice.

When a trigger in legal/00 §25 fires (a regulator or court contact, a notifiable breach, a business or employer contract, or paid traffic from a country with a law the checklist does not cover), Muath engages a lawyer before acting further on it.

## Revision log

- 2026-11-12: drafted as texts for counsel; then rewritten under ADR-25.3 as self-reviewed texts with no counsel step. The counsel question pack, the Milestone 0 consent addendum and the reviewer confidentiality agreement were removed (ADR-25.5, 25.7).
