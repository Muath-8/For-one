# Self-review checklist

> **Self-reviewed against legal/00; not reviewed by a lawyer; see the triggers.** This file is that review. It replaces the counsel question pack (ADR-25.3).

**What this is.** For one has no lawyer (ADR-25.3). It stays lawful through conservative design: the strictest common rule applies to every learner, and risk is designed out rather than argued. Each topic below gives the **final position** (the conservative choice), the **official source** it rests on, and a **check** that can be ticked. The texts in `legal/` and the product must match every final position.

**How it runs.**
1. On every change to a file in `legal/`, or to a consent, retention or vendor fact in the product, the agent's independent AI review pass reads the change against this checklist and lists any check that no longer holds. A change with a failing check does not merge.
2. Before launch, Muath ticks every check and records the tick in the revision log at the end (register A4). After launch, the checks are ticked again when a trigger in §25 fires or a vendor changes.
3. A check that cannot be ticked is a launch blocker, unless it is marked "after launch".

The sources are official texts and regulator guidance. They are named so the review can be repeated; where a source may have changed, the check says to read its current version.

---

## A. Where data lives and who processes it

### 1. Home region
- **Final position.** All data at rest is in AWS `eu-central-1` (Frankfurt) for every learner (ADR-24.8). No second region.
- **Source.** GDPR Chapter V (Art. 44 to 50): data held in the EU needs no transfer basis for EU learners. UK adequacy regulations for the EEA cover UK learners.
- **Check.** ☐ Terraform's `HOME_REGION` is `eu-central-1`; RDS, S3, KMS and Fargate all sit there; Vercel's region is `fra1`.

### 2. Transfers to US vendors
- **Final position.** Standard contractual clauses (Commission Decision (EU) 2021/914) in each vendor's standard DPA, with a short transfer impact assessment per vendor; the EU-US Data Privacy Framework where a vendor is certified; the UK Addendum to the SCCs for UK learners. Consent is never the transfer basis (ADR-24.B13).
- **Source.** GDPR Art. 46(2)(c) and 49; EDPB Recommendations 01/2020 on supplementary measures; the EU-US DPF adequacy decision (2023) and the DPF list at dataprivacyframework.gov; ICO guidance on the International Data Transfer Addendum.
- **Check.** ☐ For every vendor in [05-ropa.md](05-ropa.md) §3: the DPA is accepted, its SCC module is recorded, DPF status is looked up on the official list, and a one-paragraph transfer impact assessment (what data, why it is needed, the vendor's retention, encryption) is filed next to the register row.

### 3. Processors under written terms
- **Final position.** Every vendor is used under its standard (self-serve) data processing agreement. No vendor is called from code until its DPA is recorded (07 §4.9). Training on our data is switched off wherever possible; zero data retention is requested from Anthropic (register A1).
- **Source.** GDPR Art. 28(3); EDPB Guidelines 07/2020 on controller and processor.
- **Check.** ☐ Each register row says "DPA accepted" with the date it was accepted; ☐ each vendor's training switch is off, with a screenshot filed; ☐ the zero-retention request to Anthropic is sent.

### 4. EU and UK representative
- **Final position.** If the company is established outside the EU, appoint an EU representative; if outside the UK, a UK representative. This is a paid service, not a lawyer (register A7).
- **Source.** GDPR Art. 27; UK GDPR Art. 27; EDPB Guidelines 3/2018 on territorial scope.
- **Check.** ☐ The company's country of establishment is known; ☐ if needed, both representatives are appointed and named in the privacy notice §2.

### 5. Data protection officer
- **Final position.** No DPO at launch. Muath is the privacy contact. The need is reassessed when the product has 1,000 learners, because regular monitoring of speech could then count as large scale.
- **Source.** GDPR Art. 37(1)(b); Article 29 Working Party Guidelines on DPOs (WP243 rev.01).
- **Check.** ☐ The privacy notice names a privacy contact address. ☐ (After launch) Reassess at 1,000 learners.

### 6. Saudi Arabia (PDPL)
- **Final position.** Saudi residents get the same GDPR-grade handling as everyone. Their data rests in Frankfurt under SCC-style safeguards. The company follows SDAIA's registration and transfer rules where they apply to a foreign controller.
- **Source.** Saudi Personal Data Protection Law, its Implementing Regulation and its Regulation on Personal Data Transfer outside the Kingdom (SDAIA, current versions at sdaia.gov.sa).
- **Check.** ☐ Read SDAIA's current pages on registration and transfers; record in the revision log whether registration applies and, if so, complete it before Saudi learners are charged.

## B. Lawful basis, notice and consent

### 7. Lawful basis per purpose
- **Final position.**

| Purpose | Basis |
|---|---|
| Making the show (episodes, calls, transcripts, learner model, notebook) and processing voice to transcribe it | Contract, Art. 6(1)(b) |
| The first minutes before the account exists | Steps at the learner's request before a contract, Art. 6(1)(b) |
| Special-category content the learner chooses to say, which transcripts keep | Explicit consent at account creation, Art. 9(2)(a) (`special_category`, required) |
| Keeping recordings | Consent, Art. 6(1)(a); off by default |
| Keeping a sensitive fact beyond the session | Explicit consent by the one-tap card, Art. 9(2)(a) |
| Pseudonymized transcripts to improve the teacher | Consent; off by default; Controls only |
| The safety protocol and its content-free log | The explicit consent at account creation (Art. 9(2)(a)), and vital interests (Art. 6(1)(d), 9(2)(c)) when the learner cannot act |
| Security, audit, abuse and trial limits | Legitimate interests, Art. 6(1)(f) |
| Billing | Contract; Paddle is a separate controller |

- **Source.** GDPR Art. 6, 7 and 9; EDPB Guidelines 2/2019 on Art. 6(1)(b) for online services; EDPB Guidelines 05/2020 on consent.
- **Check.** ☐ The privacy notice §3 matches this table row for row; ☐ `special_category` is a required, unticked, separate checkbox at account creation.

### 8. Notice before the first word
- **Final position.** The first screen links the privacy notice. The microphone screen says, before any voice is processed: "Salma is an AI. Your voice is used only to run this talk and build your show; nothing is kept unless you make an account." It links the notice. The full notice is acknowledged at account creation (ADR-24.B14).
- **Source.** GDPR Art. 12 and 13; Article 29 Working Party Guidelines on transparency (WP260 rev.01), on layered and just-in-time notices.
- **Check.** ☐ `notice.a1.privacy_link` and `notice.mic.voice_line` ship; ☐ pre-account voice follows the 15-minute rule; ☐ abandoned pre-accounts are deleted after 24 hours.

### 9. Consent quality
- **Final position.** Every consent is separate, unticked, in plain words, and as easy to withdraw as to give. Voice storage and data use are off by default; data use is asked only in Controls, never during onboarding (ADR-24.B6). Terms acceptance is its own versioned consent kind (ADR-24.B18). Every acceptance records the text version shown.
- **Source.** GDPR Art. 4(11) and 7; EDPB Guidelines 05/2020 on consent.
- **Check.** ☐ No pre-ticked box anywhere; ☐ every consent string in [03-consent-texts.md](03-consent-texts.md) has a version; ☐ withdrawing each consent is one control in Controls.

### 10. Voice is not biometric data
- **Final position.** Voice is never used to identify or verify a person. There are no voiceprints, no speaker embeddings kept, no speaker identification or diarization features switched on at any vendor, and no voice cloning. Voice is still handled at the biometric standard: a per-learner key, deletion within 15 minutes when storage is off, consent to keep it (ADR-24.8, 25.3).
- **Source.** GDPR Art. 4(14) and 9(1) (biometric data counts as special category only when processed to identify someone uniquely); EDPB Guidelines 02/2021 on virtual voice assistants; Illinois BIPA (740 ILCS 14) defines "voiceprint" as a biometric identifier, so making none keeps the product outside it.
- **Check.** ☐ For each recognizer and voice vendor, speaker identification, diarization and voice cloning are off or unused; ☐ no table or object stores a speaker embedding.

### 11. Sensitive facts
- **Final position.** Six classes: health, money, relationships, religion, politics, sexuality (ADR-24.B5). The show never infers them and never brings them up first. A sensitive fact is used only in the session where the learner raised it, and kept beyond it only after a one-tap card (ADR-24.10). An untapped card keeps nothing.
- **Source.** GDPR Art. 9(1) and 9(2)(a); EDPB Guidelines 05/2020 on explicit consent.
- **Check.** ☐ `fact.sensitive.card.*` ships; ☐ code never passes an unconfirmed sensitive fact beyond its session (04 §4.7.3).

### 12. Age
- **Final position.** 18 or older only. The first screen asks for an attestation before anything else; the birth date is asked and checked on the server at account creation; an under-18 date deletes everything at once (07 D8).
- **Source.** GDPR Art. 8 (children's thresholds of 13 to 16, all below 18); ICO Age appropriate design code (a service for adults that keeps children out stays outside it).
- **Check.** ☐ A1 cannot start without the attestation; ☐ the under-18 path deletes the pre-account learner.

## C. Rights, retention and security

### 13. Rights in the product
- **Final position.** Every learner, wherever they live, gets GDPR rights. Access, export, correction and deletion are self-serve in Controls. Export: a link within 72 hours (within 1 hour when the export job is automated); the download link is valid 15 minutes from the click; the file is kept 7 days (ADR-24.B7). Deletion: a typed "delete", no grace period; access ends at once, live data is purged within 24 hours and backups expire within 30 days (ADR-24.B1). Written requests are answered within one month.
- **Source.** GDPR Art. 12(3) and 15 to 22; EDPB Guidelines 01/2022 on the right of access.
- **Check.** ☐ Every window in the privacy notice §8 matches the system configuration; ☐ `privacy/verify` checks each window hourly.

### 14. Retention
- **Final position.** The schedule in [05-ropa.md](05-ropa.md) §4 is the only source; the privacy notice copies it.
- **Source.** GDPR Art. 5(1)(e).
- **Check.** ☐ No retention period in the RoPA is blank; ☐ the notice and the RoPA agree.

### 15. Who can see learner data
- **Final position.** Only Muath (`owner`), for a reason, with every read logged and listed in the learner's export. The AI coding agent that builds and runs For one never has access to production learner data: it works with synthetic learners only. There are no hired reviewers or taggers at launch (ADR-25.7).
- **Source.** GDPR Art. 5(1)(f), 25 and 32.
- **Check.** ☐ No production credential or database role is available to the agent; ☐ the audit log records every content read and the export includes it.

### 16. Security and breaches
- **Final position.** The controls in 07 (encryption, per-learner keys, row-level isolation, audit log, verified deletion). A personal-data breach is assessed at once; if it must be notified, it goes to the supervisory authority within 72 hours and to learners in plain words where the risk is high, **and a lawyer is engaged** (§25).
- **Source.** GDPR Art. 32 to 34; EDPB Guidelines 9/2022 on personal data breach notification.
- **Check.** ☐ The incident runbook exists and names the supervisory authority (the lead authority of the EU representative's country, the ICO for UK learners, SDAIA for Saudi learners).

### 17. DPIA and RoPA
- **Final position.** Muath completes both from the official templates: [04-dpia.md](04-dpia.md) and [05-ropa.md](05-ropa.md).
- **Source.** GDPR Art. 30 and 35; Article 29 Working Party Guidelines on DPIA (WP248 rev.01); the ICO DPIA template; the CNIL PIA guides and tool; the ICO and CNIL record-of-processing templates.
- **Check.** ☐ The DPIA covers each Art. 35(7) element; ☐ the RoPA covers each Art. 30(1) element; ☐ both are signed off by Muath in their own sign-off tables.

## D. AI and safety

### 18. EU AI Act transparency
- **Final position.** (a) People are told they are talking to an AI: Salma says so in her first line, every host portrait has an "AI" mark, and every character answers "are you real?" honestly every time. (b) AI-generated audio and text are marked in machine-readable form: a metadata tag on every audio file, including feed enclosures, and one line in every feed item. (c) Anxiety mode uses turn length and silence, not biometric data, so it is not emotion recognition. (d) The product is a consumer service, not an educational institution's system, so Annex III point 3 does not apply; level estimates are never shown unasked and never gate access. (e) Muath keeps a one-page AI-literacy note for anyone who operates the product.
- **Source.** Regulation (EU) 2024/1689, Art. 4, Art. 50 and Annex III; the Commission's guidelines and code of practice on Art. 50 (read the current version).
- **Check.** ☐ `ai.*` strings ship; ☐ audio metadata and the feed line are present; ☐ the current Commission guidance on Art. 50 has been read and nothing in it contradicts (a) to (e).

### 19. Crisis protocol (SB 243-style duties for everyone)
- **Final position.** The protocol in [06-crisis-protocol.md](06-crisis-protocol.md): fixed words, never generated; the keyword waits up to 2 seconds for the host and fires anyway (ADR-24.B12); in a call the host stops and Salma's pre-recorded clip speaks in the learner's language (ADR-24.B29); resources come from a maintained international helpline directory (ADR-25.3); the content-free log is de-identified on deletion and kept 3 years (ADR-24.B15, B20); Muath sees weekly counts only; the protocol is published at `/safety`; activation counts are reported yearly where a law requires it.
- **Source.** California SB 243 (2025), on companion chatbots; GDPR Art. 9(2)(c).
- **Check.** ☐ The clips are rendered from the text in 06 §3; ☐ the resources card links the directory for the learner's country; ☐ `/safety` is live; ☐ the yearly count query runs.

## E. Selling the subscription

### 20. Merchant of record and consumer law
- **Final position.** Paddle is the merchant of record: it sells the subscription and carries tax, invoices, refunds and the payment-side consumer law (ADR-25.3). Our terms use Paddle's required reseller wording and never contradict Paddle's buyer terms.
- **Source.** Paddle's buyer terms and seller requirements (paddle.com/legal, current version).
- **Check.** ☐ Terms §6 carries Paddle's current reseller wording; ☐ the refund policy is at least as generous as Paddle's buyer terms.

### 21. Trial, renewal, cancellation and refunds
- **Final position.** A 7-day trial with no card: nothing renews from it, and the learner chooses a plan on day 7. Monthly renewal is stated next to the pay button with the price and renewal date. Cancellation is one tap in Controls and keeps access to the end of the paid period. A full refund on request within 14 days of the first payment (ADR-24.B16), which covers the EU and UK withdrawal right. An EU/UK "Withdraw from contract" control sits in Controls › Plan. Prices change only with 30 days' notice by email.
- **Source.** Consumer Rights Directive 2011/83/EU, Art. 9 to 16 and Art. 11a (the withdrawal function added by Directive (EU) 2023/2673); Germany's §312k BGB (cancellation button); California's automatic renewal law (Bus. & Prof. Code §17600 and following); the UK Consumer Contracts Regulations 2013 and the subscription-contract rules of the DMCC Act 2024 (once in force); the US FTC's ROSCA.
- **Check.** ☐ `billing.*` strings say price, renewal date and cancel in one tap; ☐ the withdraw control works in the EU and UK; ☐ the current status of the DMCC Act subscription rules has been read.

### 22. Fair terms
- **Final position.** Plain language; no clause excludes liability for death, injury, fraud or consumer rights; the liability cap applies only where the law allows; a consumer may always sue at home under their own mandatory law.
- **Source.** Unfair Contract Terms Directive 93/13/EEC; UK Consumer Rights Act 2015 Part 2; Rome I Regulation Art. 6.
- **Check.** ☐ Terms §12 and §14 keep these carve-outs.

### 23. Claims about learning
- **Final position.** No promise of results; progress claims only through the claim gate; plan copy states facts only (FR-1230, FR-1231).
- **Source.** Unfair Commercial Practices Directive 2005/29/EC.
- **Check.** ☐ The plans screen has no "best value", fake scarcity or countdown.

## F. Smaller items

### 24. Other positions
- **Podcast apps.** A learner who adds the private feed lets that app's company fetch their episodes; the notice says so (§7). ☐ The notice line ships.
- **Public use of learner material.** Never without a new, separate yes for that use. ☐ The terms §11 say so.
- **Volunteer recordings (ADR-25.6).** About 30 volunteers record clips for the vendor tests under the one-line consent `volunteer.recording` in [03-consent-texts.md](03-consent-texts.md); the clips are deleted on request and once the tests no longer need them (at most 12 months). Open corpora are used only under a commercial-use licence (speechocean762, Apache-2.0). ☐ Every volunteer clip has a recorded consent; ☐ the corpus licence is filed.

---

## 25. When a lawyer becomes necessary

None is needed until one of these happens (ADR-25.3). When one does, Muath engages a lawyer before acting further on it:

1. **A regulator or a court contacts the company**, or a learner makes a formal legal claim.
2. **A personal-data breach must be notified** to a supervisory authority (GDPR Art. 33).
3. **A business-to-business or employer contract**: anyone who wants to buy seats, sign a DPA as a controller, or negotiate terms.
4. **Paid traffic from a country with a specific law this checklist does not cover**: before advertising in that country, or when it becomes a material share of paying learners.

## Revision log

- 2026-11-12: written under ADR-25.3; replaces the counsel question pack. No check is ticked yet.
