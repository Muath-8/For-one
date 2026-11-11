# Counsel question pack

> **Draft for counsel. Not legal advice.** This pack states our working positions so counsel can confirm or correct them. Counsel must answer **part A by 2026-11-17** (register A1, before build week 1) and **part B by 2027-02-15** (register A8, the review of every text in `legal/`). Where counsel does not answer in time, the "if no answer" line says what the build does.

**Product in one paragraph.** For one is a paid, personal AI podcast for adults learning a language. Each learner gets a daily audio episode written for them by AI hosts, a live voice call with an AI host, an article and a chat. The product keeps a long-term model of the learner (what they understand and say, their mistakes, their interests and the life facts they told the show) and uses their voice to transcribe and plan. Learners can live in any country. Subscriptions are monthly in USD ($19.99, $29.99 and $44.99), sold through Paddle as merchant of record after a 7-day trial that needs no card. The beta opens to waitlist learners from 2027-03-17 (ADR-24.11), about 50 a week. All learners must be 18 or older. Controller: `[Company legal name]`, `[Address]`, `[Country of incorporation]` (counsel: we need the entity's country to answer several questions below).

**The facts that recur below.** Home region AWS `eu-central-1` (Frankfurt) for the database, storage, keys and servers (ADR-24.8). Model, voice and recognition vendors process in the US or the EU (list in [05-ropa.md](05-ropa.md)). Voice is encrypted with a key per learner; with voice storage off (the default) audio is deleted within 15 minutes of the call ending; transcripts are always kept for the life of the account (PRD FR-343, FR-1041, FR-1043). Use of transcripts to improve the product is opt-in and off by default (TC-8). Account deletion has no grace period: access ends at once, live data is purged within 24 hours and backups expire within 30 days (ADR-24.B1, FR-1047). Age is attested at the first screen, with a birth date at account creation (FR-003, FR-110).

---

## Part A: answers needed by 2026-11-17 (register A1)

### A-1. Home region and where data rests

**Question.** May a worldwide cohort's data (including Saudi residents' voice and transcripts) rest in Frankfurt?

**Working position (ADR-24.8).** `eu-central-1` is final for the beta. `me-central-1` (UAE) is a one-variable move that only counsel can trigger.

**Facts.** EU and UK learners need no transfer for data at rest in Frankfurt. Saudi residents' data leaves the Kingdom either way (no Saudi region is planned). The call server (`call-worker`) holds a call's audio in memory only for the call and runs wherever the voice vendors answer fastest, which may be the US (01 §3.6). No database sits on that path.

**Unblocks.** The production Terraform apply in build week 1 (story E01-S05). **If no answer:** production is built in `eu-central-1` anyway and moved later only if counsel requires it.

### A-2. Transfer basis for the US vendors

**Question.** What is the transfer basis, per regime, for the vendors that process in the US?

**Working position (per ADR-24.B13, which corrects 24.8).** Standard contractual clauses (Art. 46; 2021/914, with the UK Addendum or IDTA for UK learners) with a transfer impact assessment per vendor, using the EU-US Data Privacy Framework where a vendor is certified. Consent is never the transfer basis for these routine transfers; the notice informs learners about them. Counsel confirms the basis per vendor and per regime.

**Facts.** The vendors, what each sees and its region are in [05-ropa.md](05-ropa.md) §3. The ones that see learner voice: the streaming recognizer, the verbatim recognizer, the pronunciation scorer and LiveKit (in transit). The ones that see learner text: Anthropic (briefs with life facts and quotes, transcripts) and, for `data_use` learners only, Langfuse (EU). The winning voice and recognition vendors are chosen by the blind test by 2026-11-17 (register M2), so the final list lands the same day as this answer.

**Also asked.** Saudi PDPL: which transfer route applies under the Transfer Regulation (adequacy, appropriate safeguards or an exception) and whether a transfer risk assessment is required.

**Unblocks.** The processor register's "transfer basis" column; the privacy notice §7; the DPIA §4. **If no answer:** we sign SCCs and write a transfer impact assessment for every US vendor, as ruled.

### A-3. Is learner voice biometric data?

**Question.** Under GDPR Art. 9, UK GDPR, PDPL and the US state biometric laws (Illinois BIPA, Texas, Washington), is the voice we process biometric data?

**Working position (ADR-24.8).** Not biometric identification: we never use voice to identify or verify a person. We handle it at the biometric standard anyway (per-learner keys, 15-minute deletion when storage is off, consent to keep it).

**Facts.** What we do with voice: speech-to-text (streaming and verbatim); pronunciation scoring of a known sentence, kept internally and never shown; timing (pause length, speech rate) for turn-taking and fluency estimates; the learner's own recording of their name so hosts pronounce it. We do not do speaker identification, voiceprints, voice cloning (a cloned voice is a later, opt-in idea, FR-1045) or emotion recognition. The pilot consent told learners to check with counsel before accepting anyone from Illinois ([milestone-0/02-consent.md](../milestone-0/02-consent.md)). We do not ask for a US state: `residence_country` is the only location fact.

**Also asked.** Should we ask US learners for their state, or refuse residents of states with voiceprint laws, or is the consent-to-keep plus no-identification position enough?

**Unblocks.** The voice-storage consent text ([03-consent-texts.md](03-consent-texts.md) `voice_storage`), the notice §4, DPIA risk R2. **If no answer:** the texts ship as drafted (no biometric consent form) and US learners are accepted.

### A-4. Which regimes the beta covers, and the representatives

**Question.** Confirm the day-one regimes and what each needs before the beta opens on 2027-03-17.

**Working position (ADR-24.9).** EU GDPR, UK GDPR, Saudi PDPL, and a generic baseline for every other country, under which the notice says the country has not been reviewed and the EU GDPR controls apply anyway. Invites go to waitlist learners in any country; countries Paddle cannot sell into are refused at checkout.

**Facts.** `[Company legal name]` is established in `[Country]`. If that is outside the EU and the UK, we understand we need an Art. 27 representative in the EU and in the UK, and there is no lead supervisory authority (no one-stop shop). We have no DPO; the product's core activity is large-scale, regular monitoring of learners' speech for teaching, which may require one at scale.

**Also asked.** (a) EU and UK Art. 27 representatives: required, and by when? (b) DPO: required now, or at what scale? (c) Saudi PDPL: registration on SDAIA's national register, a representative in the Kingdom, or a DPO? (d) UK GDPR as amended by the Data (Use and Access) Act 2025: anything that changes these texts, such as the complaints-handling duty? (e) Is the generic baseline defensible for countries with their own strict laws that we have not reviewed (for example Brazil's LGPD, India's DPDP Act, China's PIPL, South Korea's PIPA)? Should any be refused at invite until reviewed?

**Unblocks.** The regime paragraphs in the notice, the invite filter (FR-106). **If no answer:** invites open on 2027-03-17 to every country under the baseline, as ADR-24.9 decided.

### A-5. Lawful basis per purpose, including special-category data in transcripts

**Question.** Confirm the basis for each purpose in the table, and tell us how to handle special-category data that learners say in free conversation.

**Working position (drafted here from 07 §4.3 and §4.9; the architecture names consent for voice and for research use and is silent on the rest).**

| Purpose | Working basis (EU/UK) | PDPL | Notes |
|---|---|---|---|
| Making the show: episodes, calls, transcripts, the learner model, the notebook | Contract (Art. 6(1)(b)) | Consent or contract, as counsel reads PDPL | Transcripts are core and always kept (FR-1043) |
| Processing voice to transcribe and plan (storage off: deleted within 15 min) | Contract | Consent | |
| Keeping recordings (voice storage on) | Consent (Art. 6(1)(a)) | Consent | Off by default |
| Pre-account processing (A2 to A8: Salma's intake, the pilot, the first call) | Steps before a contract at the learner's request (Art. 6(1)(b)) | Consent | See A-6 |
| Sensitive life facts kept beyond the session | Explicit consent (Art. 9(2)(a)) by a one-tap card | Explicit consent | See A-7 |
| Pseudonymized transcripts to improve the teacher | Consent | Consent | Off by default; the research set writes nothing until P1 (04 §4.12.4) |
| Billing records | Contract; Paddle is a separate controller for payment and tax | | |
| Security, audit log, abuse and trial limits (hashed identity, 180 days) | Legitimate interests (Art. 6(1)(f)) | | |
| Crisis protocol and its log | **Ask counsel** | **Ask counsel** | See B-4 |

**The hard part.** Learners talk freely. A transcript kept for the life of the account will contain health, religion, politics, sex life and other special-category data even when no "fact" is stored. Our understanding is that Art. 9 applies to that text. Options we see: explicit consent at account creation that covers what the learner chooses to say (with the plain warning that transcripts keep everything said); or a shorter retention for transcripts. **Ask counsel which.**

**Unblocks.** The notice §3, the consent texts at A8. **If no answer:** we ship the table as drafted and add the explicit-consent sentence `consent.special_category` at A8, which is drafted in [03-consent-texts.md](03-consent-texts.md) and marked optional.

### A-6. Processing before the account exists (order A)

**Question.** Is the A2 notice line, with the A1 age attestation, sufficient notice for the processing that happens before the account exists?

**Working position (per ADR-24.B14, ADR-24.2).** The first session runs in order A: Salma's talk, the optional word check, the pilot episode, the first call, and only then the account, birth date, country, notice acknowledgement and voice-storage choice (FR-110 to FR-118). Age is attested at A1 (FR-110). The A2 microphone screen carries the notice line, with a link to the full notice: "Salma is an AI. Your voice is used only to run this talk and build your show; nothing is kept unless you make an account. Privacy notice." (FR-111). Pre-account voice follows the 15-minute rule; an abandoned pre-account learner is deleted after 24 hours; an under-18 birth date deletes everything at once (07 D8).

**Facts.** About 8 minutes of processing happens before A8, including the learner's name clip and life facts from the intake, sent to Anthropic and the recognizers.

**Unblocks.** The A1 and A2 strings (`notice.a1.*`, `notice.mic.*`), story E06. **If no answer:** ship as ruled.

### A-7. Sensitive facts (ADR-24.10)

**Question.** Is a one-tap confirmation card in the notebook valid explicit consent for keeping a sensitive fact, and is our list of classes complete?

**Working position (ADR-24.10).** A spoken "yes" is not enough. A sensitive fact (health, money, relationships, religion, politics, sexuality) is used in the session where the learner raised it, and kept beyond it only after a one-tap card; even then the show never brings it up first (FR-622). ADR-24.10 says this needs no counsel answer; register A1 asks counsel to confirm it anyway.

**Facts.** The card text is `fact.sensitive.card` in [03-consent-texts.md](03-consent-texts.md). An unconfirmed sensitive fact stays in the transcript but never becomes a fact. The six classes are ruled in ADR-24.B5.

**Also asked.** Should the list include ethnic origin, trade-union membership, criminal records and immigration status (GDPR Art. 9 and 10; PDPL sensitive data)? "Money" is not an Art. 9 class; PDPL treats credit data separately. Is "money" right as a product class anyway (we think yes; it is about dignity, not law)?

**Unblocks.** The notebook card (E10), the notice §5. **If no answer:** ship the six classes and the card.

### A-8. SB 243 applied to everyone

**Question.** Does California SB 243 (companion chatbots) apply to For one, and is applying its duties to every learner sound?

**Working position (ADR-24.9, ADR-24.15).** Apply its crisis-protocol duties to every learner wherever they live, so applicability stops mattering: AI disclosure at the start and whenever asked; a protocol that stops the show, says plainly it is an AI, and shows crisis resources for the learner's country; the protocol published on our website; the yearly count of crisis referrals reported without content.

**Facts.** The hosts hold a running relationship with the learner across episodes (callbacks, a series bible), which may meet the statute's definition of a companion chatbot even though the purpose is language learning. We do not know a learner's US state, so a "California only" count is impossible; the working position is to report the count for all US learners, or for everyone, as an upper bound. Users are 18+, so the minors duties should not arise; if we learn a learner is a minor, the account is closed (A-9). The protocol and its wording are in [06-crisis-protocol.md](06-crisis-protocol.md).

**Also asked.** (a) Are we in scope? (b) The reporting recipient, first date and what to count. (c) Private right of action exposure, and whether "may not be suitable for some minors" must be shown even with an 18+ gate. (d) Any equivalent duties elsewhere (for example New York's companion-model law) that the global protocol should also meet.

**Unblocks.** The crisis build (dated in `backlog/00-release-plan.md`). Wording can wait for part B; applicability cannot. **If no answer:** build as drafted; it already meets the duties as we read them.

### A-9. Under-18s

**Question.** Is the A1 age attestation, followed by the birth date at A8, sufficient for a paid adult product in every covered regime?

**Working position (per ADR-24.B14; 07 D8, FR-003, FR-110).** An 18+ attestation at A1 before anything else happens, a birth date at A8 checked on the server, refusal with one plain sentence, and deletion of everything the pre-account learner produced. No identity check in the beta. 18+ exceeds every covered regime's children's threshold.

**Facts.** Because of order A (A-6), a minor who attests falsely is processed for about 8 minutes before the birth date is asked, under the 15-minute voice rule.

**Unblocks.** A1 and A8 (E06). **If no answer:** ship as ruled.

### A-10. Milestone 0 data (ADR-24.16)

**Question.** What do we need from the 15 pilot learners, and is there anything to remedy?

**Working position (per ADR-24.B10, 24.B28 and 24.16).** A two-part addendum ([07-milestone-0-consent-addendum.md](07-milestone-0-consent-addendum.md)). **Part 1, vendor tests:** signed before any pilot clip goes to a vendor. **Part 2, signed by 2026-12-15 (register A9):** the bridge (pilot pre-payers keep receiving hand-made episodes on the pilot's process until the 2027-03-17 open, which means keeping their pilot data past the 2026-12-31 deletion promise), re-onboarding in the end-to-end run in the last build week, importing the pilot file, and de-identified fixtures. Anyone who does not sign keeps the original promise: deletion by 2026-12-31. No clip, fixture or pilot file is used beyond what a signature covers.

**Facts counsel should weigh.**
1. **The risk that remains: clips may already have left.** The vendor tests run 2026-11-01 to 11-17 (ADR-07): 30 learner clips go to candidate recognizers and a pronunciation scorer. The pilot consent named Anthropic, Google, ElevenLabs, Google Drive and WhatsApp; it did not name Soniox, Deepgram, AssemblyAI or Speechace/Microsoft. If any clip reached an unnamed vendor before Part 1 was signed, what do we tell the learners, what do we ask the vendors to delete, and is any notification owed? Part 1 carries draft wording for both cases.
2. The pilot consent promised deletion of everything by **2026-12-31** unless the learner chose to keep recordings, and deletion within 7 days of a request. Part 2 asks for a separate yes, by 2026-12-15, to keep each kind of material past that date (the bridge, the import, text fixtures, voice fixtures). Is a fresh opt-in before the original deadline enough to extend retention, and does the bridge (the pilot's services: Anthropic, Google, ElevenLabs, Google Drive, WhatsApp, run by hand) need anything beyond the pilot consent's own terms?
3. The handbook says the repository is public today and that fixtures other than the 30 clips stay out of it ([engineering/09 §6](../engineering/09-data-handling.md)), which implies the 30 clips may be in it. Our position: no learner voice or text, de-identified or not, in a public repository.
4. Pilot pre-payments were taken outside Paddle (a payment link or bank transfer, with a written 7-day refund promise; [milestone-0/07](../milestone-0/07-measures-and-gates.md#the-pre-pay-ask)). Pre-payers were told the beta opens on 23 December; under ADR-24.B28 each is told the new date (2027-03-17) by 2026-11-19 (register A15) and offered a full refund at once or a place in the bridge. How do those payers become Paddle subscribers, and does the refund promise carry into the terms?

**Unblocks.** The vendor tests (now), the bridge (from 2026-12-15), the end-to-end run, eval fixtures. **If no answer:** no further clip leaves to a vendor not named in the pilot consent, and non-signers are excluded.

---

## Part B: answers needed by 2027-02-15 (register A8)

### B-1. Review of the texts

Review and approve, with tracked changes: [01-privacy-notice.md](01-privacy-notice.md), [02-terms-of-service.md](02-terms-of-service.md), [03-consent-texts.md](03-consent-texts.md), [04-dpia.md](04-dpia.md), [05-ropa.md](05-ropa.md), [06-crisis-protocol.md](06-crisis-protocol.md), [08-reviewer-confidentiality.md](08-reviewer-confidentiality.md). **Unblocks:** E13-S03, E13-S08 and the beta opening. **If no answer:** the beta does not open (register A8).

### B-2. EU AI Act transparency

**Working position.** (a) Art. 50(1), people told they are talking to an AI: Salma and the hosts say so in their first lines; the hosts carry an "AI" mark; every character answers "are you real?" honestly every time (FR-560); the line "Karim, Mona and Salma are AI" appears in onboarding and in Controls. (b) Art. 50(2), machine-readable marking of AI-generated audio and text: every episode file, including the private feed's enclosures, carries a metadata tag saying it is AI-generated, and every feed item's description ends with one line saying so. (c) Art. 50(3): anxiety mode reads turn length and silences, not biometric data, so we treat it as outside "emotion recognition"; confirm. (d) Annex III point 3 (education): we read it as covering educational institutions, not a consumer subscription, so the product is not high-risk; the level estimates are never shown unasked and never decide access to anything. (e) Art. 4 AI literacy: a one-page brief for staff and reviewers.

**Also asked.** The dates that apply after any changes to the Act's timetable, and which marking standard counts (metadata, watermark, C2PA). **Unblocks:** the feed and audio metadata (E08), the disclosure strings.

### B-3. Consumer subscription rules

**Working position (drafted here; the architecture leaves the refund text open, 07 §4.14 rule 6).**
- **Trial without a card** (FR-1201). Nothing renews automatically from the trial: the learner must choose a plan and pay on day 7. One plain email on day 6.
- **Renewal.** Monthly until cancelled, stated at checkout next to the button, with the price and the renewal date.
- **Cancel in one tap** in Controls, keeping access to the end of the paid period (FR-1233). No win-back offers.
- **Refunds (decided, ADR-24.B16).** A full refund of the first payment on request within 14 days of it, no questions asked. This meets the EU and UK 14-day withdrawal right without a pro-rata calculation and keeps the pilot's promise. After that, no refunds for part-months unless the law requires one.
- **Price changes.** Founding learners (the first 100 payers) keep their price for as long as they stay subscribed (FR-1203). For others, at least 30 days' notice by email before a new price applies to their next renewal, with one tap to cancel. ADR-24.5 may raise `two_a_day` to $34.99 for signups after the founding 100.
- **Failed payment.** One email and a 7-day grace in which the show continues; the processor's retries run inside it (per ADR-24.B2, FR-1232).
- **Plan changes.** An upgrade takes effect at the next drop and Paddle prorates the charge; a downgrade takes effect at the next billing date with no proration; unused allowance is never refunded (per ADR-24.B3, FR-1205).
- **Payment methods.** Cards, Apple Pay, Google Pay and PayPal; Mada and other local methods later (per ADR-24.B4, FR-1204).

**Also asked.** (a) With Paddle as reseller, who owes the withdrawal right, and do Paddle's buyer terms and refund policy override or sit beside ours? (b) The EU withdrawal function (the "withdraw from contract here" button that we understand the Consumer Rights Directive requires for online contracts from 19 June 2026), Germany's cancellation button (§312k BGB), California's automatic renewal law and the UK's subscription-contract rules under the DMCC Act 2024 (commencement date): is the one-tap cancel enough, and what must the button say? (c) Saudi e-commerce rules on cancellation. (d) The "about $1 a day" and tutor-comparison claims on the plans screen (FR-1230). **Unblocks:** E12 checkout and the terms.

### B-4. The crisis protocol: basis, records and wording

**Working position (per ADR-24.B15).** The `crisis_log` holds no content: the date, the residence country, the resource shown, and whether the call ended. On account deletion its rows are de-identified (the learner id is dropped) and kept for 3 years for annual reporting, then deleted.

**Questions.** (a) The lawful basis for detecting a crisis and keeping that log (a row still records that the protocol ran for a person, which may be health data until it is de-identified). (b) Whether the 3-year de-identified retention is sound. (c) The clip wording, the per-country resources and the international fallback in [06-crisis-protocol.md](06-crisis-protocol.md). (d) Whether any regime requires more than showing resources (we never contact the learner, and the founder sees counts only, ADR-24.15). **Unblocks:** the crisis build (`backlog/00-release-plan.md`); the clips are rendered from the approved wording.

### B-5. Retention and deletion

**Confirm.** (a) Deletion: no grace period; after a typed "delete", access ends at once, live data is purged within 24 hours and backups expire within 30 days (per ADR-24.B1, FR-1047). Export: a zip without a passphrase, prepared within 72 hours during the beta while it may be done by hand and within 1 hour once automated; the emailed link opens the notebook and the download is a 15-minute link made on click; the file is kept 7 days (per ADR-24.B7, FR-1046). Both are within the one-month response period. (b) Backups expire at 30 days, not scrubbed (04 §10 #8). (c) The audit log keeps rows 24 months and keeps a deleted learner's id for 12 months (07 §4.12). (d) The deletion ledger keeps an HMAC of the email after deletion; its retention is not set. (e) Waitlist rows not invited within 12 months are deleted (07 §10 #11). (f) Transcripts kept for the life of the account (see A-5).

### B-6. Smaller items

1. **Podcast apps.** A learner who adds the private feed to a podcast app lets that app's company fetch episodes that use the learner's first name and personal topics. We disclose it in the notice §7; is that enough?
2. **Staff access.** The founder can read learner content; each read is logged and listed in the learner's export (07 §4.12). Engineers can read a learner's prompt text by trace id with a reason (handbook 09 §3). Are the notice's words adequate?
3. **The reviewer agreement** ([08-reviewer-confidentiality.md](08-reviewer-confidentiality.md)) for paid readers who may live in any country: enforceable as drafted?
4. **Breach notice contacts** per regime (07 §4.15): counsel's name and the channel to each regulator.
5. **Governing law and disputes** for consumers in many countries: `[Governing law]`, `[Courts]`, and mandatory consumer law carve-outs.
6. **Marketing use** of any learner clip, quote or story needs a new, separate yes (as in the pilot). Confirm no general clause is needed in the terms.
