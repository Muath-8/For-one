# Privacy notice

> **Draft for counsel. Not legal advice.** Drafted 2026-11-12 for GDPR Art. 13, UK GDPR, Saudi PDPL and a generic baseline. Not in force. **Counsel must confirm:** the lawful bases in §3 (pack A-5), the transfer basis in §7 (A-2), the biometric reading in §4 (A-3), the sensitive-fact handling in §5 (A-7), the representatives and regulators in §12 (A-4), and every retention period in §8 (B-5).

**Notes for whoever ships this (delete before publishing).**
- Ships to `packages/native/<lang>/privacy/notice.md`, English source in `native/en`. Version id = the date counsel approves it.
- Text in `[[EU]]`, `[[UK]]`, `[[SA]]` or `[[BASELINE]]` blocks is shown only to learners whose `residence_country` selects that regime (07 §4.9). Everything else is shown to everyone.
- `{producer}` is Salma in the Arabic package; each native package names its own producer (FR-520). `{hosts}` are the target language's host names (for English in the pilot, Karim and Mona).
- The vendor list in §7 is rendered from the processor register at build time, so it cannot drift from the system (07 §4.9). Vendors in `[brackets]` are decided by the blind test by 2026-11-17.
- §8 has no deletion grace (per ADR-24.B1); exports are promised within 72 hours during the beta (per ADR-24.B7). When the export job is automated, change "72 hours" to "an hour" in §8 and §11 and bump the version.

---

## For one: how we handle your voice and your data

Last updated `[date counsel approves]`. Version `[version]`.

### 1. The short version

- **Your show is made from what you tell it.** We use what you say and type to make your episodes and calls. We never look you up anywhere else, and we never guess things about your health, money, relationships, religion, politics or sexuality.
- **Your voice.** We listen to each call to understand you. If you don't ask us to keep your recordings, we delete the audio within 15 minutes of the call ending. Transcripts are kept.
- **The hosts and {producer} are AI.** Real companies' AI models write and voice the show. They don't train on your data.
- **Nobody reads your data for fun.** A small number of named people can, for specific reasons. Every time they do, it's logged, and you can see it in your export.
- **Helping improve the teacher is your choice.** It's off unless you switch it on.
- **It's yours.** See it, export it, correct it or delete it, any time, in Controls.
- **We don't sell your data and there are no ads.**

### 2. Who we are

For one is run by `[Company legal name]`, `[Address]` ("we"). We decide how your data is used, so we are the **controller**. Contact us at `[privacy email]`.

`[[EU]]` Our representative in the EU is `[EU representative name and address]`. `[[/EU]]`
`[[UK]]` Our representative in the UK is `[UK representative name and address]`. `[[/UK]]`
`[[SA]]` `[Saudi representative or registration details, if counsel says they are required]`. `[[/SA]]`
`[Data protection officer: name and contact, if counsel says one is required]`

Paddle sells you the subscription as our reseller. For payments, Paddle is a separate controller with its own privacy notice (§9).

### 3. What we collect, why, and on what basis

| What | Why | Legal basis (see the note below the table) |
|---|---|---|
| Your account: name the hosts call you, email or Apple or Google sign-in, birth date, the country you live in, your languages, time zone | To run your account, check you're 18 or older, follow the right privacy law and show the right help lines | Contract |
| What you say in calls and to {producer}, and what you type in chat (transcripts) | To make your next episodes and calls, and to show your progress in your own words | Contract |
| Your voice (calls, voice notes, "say it once", shadowing, the then-and-now recording, the recording of your name) | To understand what you said, plan your episodes and help the hosts say your name | Contract to process it; **your consent** to keep it (§4) |
| Facts about your life you tell the show (job, interests, plans, people you mention) | So the show is about you | Contract. Sensitive facts: **your explicit consent** (§5) |
| What you do in the app: plays, replays, words you tap, what you skip | To pitch the show at the right difficulty and length | Contract |
| Estimates of how much you understand and can say, and what you're working on | To plan your show. Never shown as a score; you can ask {producer} "where do I stand?" | Contract |
| Pseudonymized, de-identified transcripts (only if you switch it on): names of people, places and employers removed | To check and improve the teacher | **Your consent**, off by default |
| Billing: plan, subscription state, amounts, invoice link (no card details) | To bill you and keep accounts | Contract; legal obligation |
| Security records: sign-in, who looked at your data and why, device and network checks (hashed) | To keep your data safe, stop abuse and limit free trials to one per person | Our legitimate interest in security |
| Safety: a record that the crisis protocol started, without the content (§10) | To make sure the protocol worked and to report how often it is used | `[Counsel: basis, pack B-4]` |

`[[EU]]` `[[UK]]` "Contract" means the processing is needed to provide the service you asked for (Art. 6(1)(b)). "Consent" means Art. 6(1)(a) and, for sensitive facts, Art. 9(2)(a). "Legitimate interest" means Art. 6(1)(f); you can object to it (§11). `[[/UK]]` `[[/EU]]`
`[[SA]]` `[Counsel: the PDPL basis for each row, pack A-5.]` `[[/SA]]`

**Before you have an account.** In your first minutes, {producer} talks with you, makes a short pilot episode and puts you on a first call, before you create an account. Before you speak, the microphone screen tells you: "Salma is an AI. Your voice is used only to run this talk and build your show; nothing is kept unless you make an account." Your voice from that time is deleted within 15 minutes. If you leave without creating an account, we delete everything within 24 hours.

**We don't make decisions about you that have legal or similar effects.** The teacher plans your episodes automatically from what you say and do. That is the service; it decides what you hear next, nothing else.

### 4. Your voice

- **If you don't ask us to keep recordings (the default):** each call's audio is turned into a text transcript, then deleted within 15 minutes of the call ending. This also applies to voice notes and other short recordings. Your then-and-now comparison then uses transcripts only. You can still keep one then-and-now recording on its own.
- **If you switch "Keep my recordings" on:** we keep your recordings, encrypted with a key that belongs only to your account, until you delete them or your account. Deleting your account destroys the key, which makes any copy unreadable.
- **Switching it off later** deletes all your stored recordings within 24 hours.
- **"Delete all recordings"** in Controls deletes them within 24 hours and leaves the switch as it is.
- **We never use your voice to identify you,** never make a copy of your voice, and never use it to train anyone's AI.

### 5. Sensitive things you tell the show

Health, money, relationships, religion, politics and sexuality are sensitive. The show never guesses them and never brings them up first.

If you mention one, the show may respond to it in that conversation. It keeps it after that only if you say yes on a card in your notebook. If you don't, it isn't kept as a fact (it stays only in that day's transcript). You can delete any fact at any time.

`[Counsel: pack A-5 asks whether transcripts that contain sensitive things need a separate explicit consent. If yes, add: "Transcripts keep everything you say, including sensitive things you choose to mention. By creating an account you agree to that."]`

### 6. AI, and the people who can see your data

**The AI.** The hosts and {producer} are AI. The companies whose AI models we use (§7) process your data only to produce the show for you. They are not allowed to train their models on it, and we switch off any option that would allow it.

**People.**

| Who | What they can see | When |
|---|---|---|
| The founder | Anything, if needed | Rarely, for a reason. Every look is logged and shows in your export as "owner". |
| An engineer on call | Ids and states; your transcript or a recording only to investigate a specific problem | With a written reason, logged, and shown in your export |
| A paid reviewer who signed a confidentiality agreement | A sample of your episode scripts each month, with your name and the names you mentioned removed | To check quality. Never your transcripts, notebook or recordings |
| A tagger who signed a confidentiality agreement | Pseudonymized, de-identified transcripts, one at a time | Only if you switched on "help improve the teacher" |

Your export includes the list of every staff look at your data (the role, date and reason), grouped per minute.

### 7. Companies that help us, and where your data goes

We store your data in the European Union (Amazon Web Services, Frankfurt, Germany). Some of the companies below process it in the United States while they work on it.

| Company | What it does | What it sees | Where |
|---|---|---|---|
| Amazon Web Services | Hosting, storage, encryption keys | Everything, encrypted | EU (Frankfurt) |
| Anthropic | AI that plans and writes the show, runs the hosts and {producer}, and analyses what you said | Your transcripts and the facts the show uses | US |
| Google | AI that checks scripts; text-to-speech `[if chosen]` | Scripts and checked facts; not your voice | US |
| `[Voice vendor(s), from the blind test]` | The hosts' and {producer}'s voices | Script text, including your first name | `[US/EU]` |
| `[Live speech recognizer]` | Turns your speech into text during the call | Your voice, while you speak | `[US/EU]` |
| `[Verbatim recognizer]` | A careful transcript after the call | Your voice, deleted after transcription | `[US/EU]` |
| `[Pronunciation scorer]` | Scores short repeated sentences, internally | Short clips of your voice | `[US/EU]` |
| LiveKit | Carries the call's audio | Your voice, in transit only; nothing recorded | Nearest server to you |
| Inngest | Runs background jobs | Ids and dates, no content | EU |
| Langfuse | Technical traces | Ids, timings, costs. De-identified text only if you switched on "help improve the teacher"; kept 30 days | EU |
| Sentry | Error reports | Technical errors with personal details removed | EU |
| Resend | Sends our emails | Your email address and the email | `[US/EU]` |
| Vercel | Serves the web app | Network requests, including your IP address | Global; logs in the US |
| Paddle | Takes payment and handles tax | Name, email, country, payment details | `[Paddle region]`; Paddle's own notice applies |
| Apple, Google | Sign-in, if you choose it | Your sign-in identity | Their own terms |

**Transfers outside your country.** `[[EU]]` `[[UK]]` For transfers to the US we use the European Commission's standard contractual clauses (with the UK Addendum for UK learners), with an assessment of the risks of each transfer, and the EU-US Data Privacy Framework where the company is certified. We never rely on your consent for these transfers. Ask us for a copy. `[Counsel confirms, pack A-2.]` `[[/UK]]` `[[/EU]]` `[[SA]]` `[Counsel: the PDPL transfer basis.]` `[[/SA]]` `[[BASELINE]]` We apply the same safeguards we use for learners in the EU. `[[/BASELINE]]`

**Podcast apps.** If you add your private feed to a podcast app, that app's company may fetch and keep your episodes under its own privacy policy. Your episodes use your first name and talk about things you told the show. You can reset the feed link in Controls at any time.

### 8. How long we keep it

| What | How long |
|---|---|
| Your account, transcripts, notebook and learner model | While your account exists |
| Recordings, if you keep them | Until you delete them, switch "Keep my recordings" off, or delete your account |
| Audio, if you don't keep recordings | Deleted within 15 minutes of the call ending |
| AI prompts and replies stored with us for fixing problems | 90 days |
| Technical traces (Langfuse) | 30 days |
| Pseudonymized, de-identified transcripts for improving the teacher | Until you switch it off (deleted within 24 hours) or delete your account |
| Exports you request | Ready within 72 hours during the beta; the file is kept 7 days |
| The record that the safety protocol ran (no content) | While your account exists; after you delete it, kept 3 years without anything linking it to you, then deleted |
| If your trial ends and you don't subscribe | 90 days, then your account is deleted; we email you a week before |
| If you start but don't create an account | 24 hours |
| Security and access records | 24 months; the link to your account is removed 12 months after you delete it |
| Billing records we hold | Until you delete your account. Paddle keeps its own records as the seller, as tax law requires. |
| Waitlist details, if you were never invited | 12 months |

**When you delete your account.** You confirm by typing "delete". Your account closes at once and can't be restored. We delete everything from our live systems within 24 hours, and from our backups within 30 days. We ask the companies in §7 to delete what they hold. We keep only the safety record above, if there is one, with nothing that links it to you (§10), and a scrambled code of your email so we can prove the deletion happened.

### 9. Payments

Paddle (`[Paddle entity named at checkout]`) is the seller of your subscription and handles payment, invoices and tax. We never see your card number. We receive your plan, subscription state, amounts and an invoice link. Paddle's privacy notice explains what it does: `[link]`.

### 10. Your safety

The show is for learning a language. It is not a help line. If you say something that suggests you might be in danger, the show stops, says plainly that it is an AI and can't help with this, and shows help lines for the country you live in. You choose whether to continue. Nobody contacts you about it. We keep a record that this happened, without what you said: the date, your country, which help lines we showed, and whether the call ended. It lets us check the protocol works and report how often it is used. What you said in that moment is never used in your show, your notebook or your progress. Our full safety protocol: `[link to /safety]`.

### 11. Your choices and your rights

**In Controls, any time, with no reason needed:** keep or stop keeping recordings; delete all recordings; switch "help improve the teacher" on or off; see everything we hold about you; export it (a link by email within 72 hours during the beta); correct or delete any fact in your notebook (at once); delete your account.

**Your rights.** You can ask us to give you a copy of your data, correct it, delete it, limit how we use it, give it to you in a portable form, or stop using it where we rely on legitimate interest. You can withdraw a consent at any time; that doesn't affect what we did before. Most of this you can do yourself in Controls. Otherwise, write to `[privacy email]`. We answer within one month.

`[[EU]]` You can complain to the data protection authority in the EU country where you live or work: `[link to the EDPB list]`. `[[/EU]]`
`[[UK]]` You can complain to the Information Commissioner's Office: ico.org.uk. `[Counsel: add the DUA Act 2025 complaint step if required.]` `[[/UK]]`
`[[SA]]` You can complain to the Saudi Data and Artificial Intelligence Authority (SDAIA). `[Counsel: the PDPL rights wording and response period.]` `[[/SA]]`
`[[BASELINE]]` We haven't yet had a lawyer review the privacy law of the country you live in. We give you the same protections and rights as learners in the European Union, and you also keep any rights your own country's law gives you. `[[/BASELINE]]`

**If something goes wrong.** If a breach puts your data at risk, we tell the regulators that the law requires within 72 hours, and we tell you in plain words by email.

### 12. Age

For one is only for people aged 18 or older. If we learn that someone under 18 has an account, we delete it.

### 13. Changes

If we change this notice, we show you the new version the next time you open the app and say what changed in plain words. If a change affects something you consented to, we ask you again.
