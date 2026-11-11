# Consent and notice texts (in-app strings)

> **Draft for counsel. Not legal advice.** English source strings, drafted 2026-11-12 from PRD-v3 FR-110 to FR-118 and FR-1020, design 04 (A1 to A8, Controls) and 06 (§3, §4), and 07 §4.3. Not in force. **Counsel must confirm:** that each consent string is specific and informed enough for its regime (pack A-5); the pre-account wording at A1 and A2 (A-6); the sensitive-fact card as explicit consent (A-7); whether `consent.special_category` is needed (A-5); the checkout renewal and withdrawal lines (B-3).

## How to read this file

- **Ids.** Consent kinds keep 07 §4.3's keys (`voice_storage`, `data_use`, `privacy_notice`, `age_attestation`, `gap_note`) so the strings drop into `packages/native/<lang>/consent/consent_texts.yaml`. Every other string has a dotted id for the native package's `ui_strings/`. Engineers add no consent flag without one of these ids and a version (handbook 09 §5).
- **Versions.** Each consent block carries `version`. Until counsel approves, it is `draft-2026-11-12`; on approval it becomes the approval date (`2027-02-15.1` style). Every acceptance records the version shown (07 D4).
- **Spoken.** Strings marked `spoken: true` are said by the producer ({producer}: Salma in `native/ar`; each native package names its own) in the learner's own language, and also shown as a caption. `spoken_text` is the speakable form where it differs from the screen text: shorter, no links, no brackets.
- **Placeholders.** `{producer}`, `{hosts}` (the target language's two host names), `{name}` (what the hosts call the learner), `{price}`, `{date}`, `{n}`, `{plan}`, `{class}`, `{quote}`.
- **Translation.** English is the source. Every native package translates it with a native speaker, never machine-only, keeping {producer}'s register (design 06 §5). `native/ar` already has drafts of `voice_storage` and `data_use` in 07 §4.3; they are re-translated from these strings once counsel approves the English.
- **Style.** One sentence per idea, present tense, no exclamation marks, every consent an unticked box (design 00, 01, 06).

`data_use` is asked in Controls only, off by default, never during onboarding (per ADR-24.B6).

## Where each string appears

| Moment | Screen | Strings |
|---|---|---|
| First open | A1 | `age_attestation.checkbox`, `notice.a1.privacy_link`, `notice.a1.under_18` |
| Microphone | A2 | `notice.mic.primer`, `notice.mic.voice_line` |
| Salma's first words | A3 | `ai.producer.intro` (spoken) |
| After the first call | A7 caption | `ai.disclosure.onboarding` |
| Keep your show | A8 | `account.country.*`, `account.birth_date.*`, `age.refused`, `voice_storage.*`, `terms.*` (ADR-24.B18), `privacy_notice.ack`, `trial.line` (and `consent.special_category` if counsel requires it) |
| Notebook | sensitive fact pending | `fact.sensitive.card.*` |
| Any time asked | call, chat, Salma | `ai.disclosure.asked.producer`, `ai.disclosure.asked.host` |
| Feed and audio files | every episode | `ai.disclosure.feed_item` |
| Controls | the data sheet | `voice_storage.off_confirm`, `recordings.delete_all.*`, `data_use.*`, `gap_note.*`, `export.*`, `account.delete.*` |
| Plans and billing | day 7, Controls | `billing.*` |
| A consent text changes | next open | `consent.changed.*` |

## 1. Consent kinds (`consent/consent_texts.yaml`)

```yaml
# packages/native/en/consent/consent_texts.yaml  (English source; native/en is the universal fallback, ADR-02)
language: en

age_attestation:                 # A1. Unticked. Start stays disabled until ticked (07 D8).
  version: "draft-2026-11-12"
  checkbox: "I'm 18 or older"

privacy_notice:                  # Acknowledged at A8, re-shown without a checkbox after a version bump (07 §4.3 rule 4).
  version: "draft-2026-11-12"
  file: privacy/notice.md
  ack: "The privacy notice says what we keep, why, and for how long."
  ack_link: "Read the privacy notice"

terms:                           # Own consent kind (ADR-24.B18): at account creation (A9) and again on any material change.
  version: "draft-2026-11-12"
  file: legal/terms.md
  line: "By keeping your show you agree to the terms."
  link: "Read the terms"

voice_storage:                   # A8, right after the learner has heard themselves (FR-118). Unticked. Default false.
  version: "draft-2026-11-12"
  checkbox: "Keep my recordings so I can hear my progress. Only for you, delete any time."
  sentence: "If you don't, we still listen to each call for a few minutes to understand what you said and plan your next episodes, then delete the audio within 15 minutes. Transcripts are always kept."
  spoken: true
  spoken_text: "One choice before tomorrow. I can keep your recordings, so later you can hear how you sounded at the start. They're only for you, and you can delete them any time. If you'd rather not, I still listen to each call for a few minutes to plan your next episodes, then the audio is deleted. Up to you."
  then_and_now_note: "Without recordings, your then-and-now comparison uses transcripts only. It's the part most people like best."
  off_confirm: "Stop keeping recordings? Every recording you have is deleted within 24 hours. Transcripts stay."
  off_confirm_button: "Stop and delete"
  keep_one: "Keep this one recording, even with recordings off?"
  keep_one_detail: "Only this then-and-now recording is kept. Delete it any time in your notebook."

data_use:                        # Controls only (ADR-24.B6). Unticked. Default false.
  version: "draft-2026-11-12"
  switch: "Help improve the teacher with my transcripts, with names removed."
  detail: "Text only, never your voice. We remove your name, the names of people you mention, and places and employers, but it's still your words, so we call it pseudonymized and de-identified, not anonymous. A named person at For one may read it under a confidentiality agreement, to check and improve the teacher. Never sold, never used for ads. Switch it off and we delete it within a day."
  spoken: true
  spoken_text: "If you want, my team can read your call transcripts, with names removed, to make the teacher better. Never your voice, never sold. It's off unless you switch it on."
  off_confirm: "Switched off. Your transcripts are removed from the improvement set within a day."

gap_note:                        # Week 1 (FR-211), Controls. Opt-in; one message, once.
  version: "draft-2026-11-12"
  ask: "Want to write a note to yourself? If you're away for {days} days, I'll send it to you once. Only once."
  spoken: true
  switch: "Send my note once if I'm away for {days} days"
  off: "Your note won't be sent."

special_category:                # OPTIONAL. Ship only if counsel says transcripts need explicit consent for special-category content (pack A-5).
  version: "draft-2026-11-12"
  checkbox: "I understand transcripts keep everything I choose to say, including private things like health or beliefs. They're only for me and my show."
```

## 2. Notices and disclosures (`ui_strings/`)

```yaml
# packages/native/en/ui_strings/legal.yaml

# A1: the first screen. Nothing else on it (FR-110).
notice.a1.privacy_link: "How we handle your voice and data"
notice.a1.under_18: "For one is for people 18 and older."

# A2: the microphone primer (FR-111). The pre-account notice, per ADR-24.B14 (pack A-6).
notice.mic.primer: "{producer}, your producer, will talk with you for 3 minutes. You can talk back or type."
notice.mic.voice_line: "{producer} is an AI. Your voice is used only to run this talk and build your show; nothing is kept unless you make an account."
notice.mic.privacy_link: "Privacy notice"

# A3: {producer}'s first words, spoken within 60 seconds (FR-112, FR-560).
ai.producer.intro: "Hi, I'm {producer}. I'm the AI producer of your show. I'll ask you three things, then we'll make your first episode."
ai.producer.intro.spoken: true

# A7 caption area and Controls › About (design 06 §4).
ai.disclosure.onboarding: "{hosts} and {producer} are AI. This show is made for you and nobody else."
ai.badge: "AI"                                    # the small mark on host portraits and the producer monogram

# Asked "are you real?" or similar, any time (FR-560, FR-561). Fixed lines, played or shown verbatim.
ai.disclosure.asked.producer: "No, I'm an AI. I'm the producer of your show, not a person."
ai.disclosure.asked.producer.spoken: true
ai.disclosure.asked.host: "I'm an AI host. The show is made for you; the stories in it are part of the show."   # lives in packages/languages/<target>/, said in the target language

# Every feed item description and every audio file's metadata (EU AI Act Art. 50(2), pack B-2).
ai.disclosure.feed_item: "Made with AI for {name} by For one."
ai.disclosure.audio_metadata: "AI-generated audio. For one."

# A8: account (FR-118).
account.country.question: "Which country do you live in?"
account.country.why: "It decides which privacy law protects you and which help lines we show. We never guess it."
account.birth_date.label: "Your birth date"
account.birth_date.why: "To check you're 18 or older. Never shown to anyone."
age.refused: "For one is only for people 18 and older, so we can't make your show. We've deleted what you told us."
trial.line: "Your 7-day trial is on 2 episodes a day. No card needed. On day 7 you choose a plan."   # ADR-24.B27
trial.line.spoken: true
# Arabic draft for packages/native/ar (Muath's read, register A5):
# trial.line: "تجربتك المجانية ٧ أيام، بحلقتين في اليوم. لا تحتاج بطاقة. في اليوم السابع تختار خطتك."

# Notebook: the sensitive-fact card (ADR-24.10). Shown after a session in which the learner mentioned a sensitive class.
fact.sensitive.card.title: "Something private you mentioned"
fact.sensitive.card.quote: "On {date} you said: \"{quote}\""
fact.sensitive.card.body: "This is about your {class}. Should I keep it? If I do, the show still never brings it up first. If not, it's not kept as a fact."
fact.sensitive.card.keep: "Keep it"
fact.sensitive.card.dont: "Don't keep it"
fact.sensitive.card.kept: "Kept. Only you can bring it up."
fact.sensitive.card.dropped: "Not kept."
fact.sensitive.class.health: "health"
fact.sensitive.class.money: "money"
fact.sensitive.class.relationships: "relationships"
fact.sensitive.class.religion: "religion"
fact.sensitive.class.politics: "politics"
fact.sensitive.class.sexuality: "sexuality"
fact.sensitive.lock_line: "Only if you bring it up"      # the line under a kept sensitive fact (design 04)
# Open: what happens to a card nobody taps. Proposed: the fact is not kept, and the card disappears after 7 days. Not decided anywhere.

# Controls: the data sheet (FR-1020, design 03 flow I).
recordings.delete_all.row: "Delete all recordings"
recordings.delete_all.confirm: "Delete {n} recordings? The tape will be empty. Transcripts stay."
recordings.delete_all.done: "Deleting. All recordings are gone within 24 hours."
export.row: "Export my data"
export.confirm: "We'll email you a link within 72 hours. The file is kept for 7 days."   # ADR-24.B7; "within an hour" once the export job is automated
see_all.row: "See everything you know about me"
access_log.row: "Who has looked at my data"
account.delete.row: "Delete my account and everything"
account.delete.confirm: "Delete your account? Type \"delete\" to confirm."      # no grace period, ADR-24.B1
account.delete.detail: "This can't be undone. Everything is deleted within 24 hours, and from backups within 30 days. Want a copy first? Export it before you delete."
account.delete.done: "Your account is closed and is being deleted."
account.delete.spoken_text: "If you delete your account, it closes straight away and can't be brought back. Export first if you want a copy."

# A consent or notice text changed (07 §4.3 rule 4).
consent.changed.title: "Something changed"
consent.changed.body: "We changed how {topic} works. In short: {diff}. Your choice stays as it was until you change it."
consent.changed.notice: "We updated the privacy notice. In short: {diff}."
```

## 3. Plans and billing (`ui_strings/billing.yaml`)

```yaml
# Day 7 plan picker, checkout and Controls › Plan (FR-1201 to FR-1233, ADR-24.4). Facts only (design 06 §4).
billing.picker.title: "Keep your show"
billing.picker.recommended: "Recommended"
billing.picker.per_day: "About $1 a day"                 # 2 a day only (FR-1230)
billing.picker.includes: "Every plan: listen again, the article, the chat and round two, as much as you like."
billing.checkout.renewal: "{price} a month, charged today and every month on the {day} until you cancel. Cancel in one tap in Controls."
billing.checkout.tax: "Tax is added where the law requires it."
billing.checkout.reseller: "Paddle handles the payment and your invoice for us."
billing.checkout.refund: "Not happy? Ask within 14 days of your first payment for a full refund."   # ADR-24.B16; shown on the first checkout only
billing.founding.line: "You're founding member {n} of 100. Your price stays {price} for as long as you stay subscribed."
billing.upgrade.confirm: "{plan} starts with your next episode. {charge_line}"
billing.downgrade.confirm: "{plan} starts on {date}. Until then you keep your current plan."
billing.cancel.row: "Cancel my plan"
billing.cancel.confirm: "Cancel? Your show runs until {date}. After that, your archive and notebook stay for 90 days."
billing.cancel.done: "Cancelled. Your show runs until {date}."
billing.withdraw.row: "Withdraw from contract"          # EU and UK, within 14 days of the first payment (pack B-3b)
billing.payment_failed.line: "Your payment didn't go through. Your show keeps playing for 7 days. Try again any time."
billing.trial_ended.line: "No new episodes until you pick a plan. Your archive and notebook stay for 90 days."
billing.price_change.email_subject: "Your For one price is changing on {date}"
```

`billing.payment_failed.line` uses the 7-day grace (per ADR-24.B2). Upgrades are prorated and downgrades are not (per ADR-24.B3); `{charge_line}` states the prorated amount.

## 4. What these strings deliberately do not say

- No "free" in large type, no "limited", no countdown, no pre-ticked box (FR-1231, design 04 A8).
- No consent is bundled: voice storage, data use, the gap note and the terms are separate answers.
- No consent text names a person. The notice and the access log say "owner", "engineer", "reviewer" (07 §4.12).
- Crisis strings are not here. They are fixed, counsel-reviewed wording in [06-crisis-protocol.md](06-crisis-protocol.md).
