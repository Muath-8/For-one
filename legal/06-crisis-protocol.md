# Crisis and self-harm protocol

> **Draft for counsel. Not legal advice.** The protocol as designed in 07 §4.8 and D9, 03 D15, PRD FR-570 to FR-572 and ADR-24.15, with the wording counsel must approve by **2027-02-15** (ADR-24.15, register A8). **Counsel must confirm:** whether SB 243 applies and whether this protocol meets its duties as we read them (pack A-8); the lawful basis and retention of the crisis log (B-4); the clip and card wording in §3; every phone number in §4 (each row is unverified until a person has called or checked the official source); the public summary in §7.

**Ships to.** Clip wording: `packages/languages/<target>/crisis/clips/` (the hosts' line, in the target language) and `packages/native/<lang>/crisis/clips/` (the producer's line, in the learner's language), rendered at package build from the approved text, one pair per (target, native) combination the beta serves. Card and chat copy and the per-country lines: `packages/native/<lang>/crisis/resources.yaml`. Keyword lists: `crisis/keywords.yaml` in both package kinds. The public summary: the website page `/safety`.

## 1. Principles

1. **The show stops being a show.** A character steps out, says plainly that it is an AI and cannot help with this, and points to people who can.
2. **Fixed words, never generated.** Every line in a crisis is pre-written, counsel-approved and pre-rendered. A model under pressure is the wrong thing to improvise a crisis line (07 §8).
3. **The right country's help.** Resources follow the country the learner told us they live in, never a guess from their IP; an international directory covers the rest (ADR-20).
4. **Dignity.** The learner decides whether to continue. Nobody from the product contacts them afterwards. The founder sees counts, never content (ADR-24.15).
5. **The show never remembers the worst moment.** The triggering turn is quarantined from facts, callbacks, evidence, claims and proofs (07 §4.8).
6. **The same protocol for everyone.** SB 243's crisis-protocol duties are applied to every learner wherever they live (ADR-24.9).

## 2. The protocol as built

### 2.1 Triggers

| # | Source | How it fires | Where |
|---|---|---|---|
| 1 | The host in a call | The host model sets `@moves.crisis` in its turn header, under the rule "declare crisis and say nothing else" | Calls, round two, the onboarding call |
| 2 | Keyword lists in a call | An exact phrase match, after normalization, on the streaming transcript of each learner turn, against two lists: the target language's (`packages/languages/<target>/crisis/keywords.yaml`) and the learner's own language's (`packages/native/<lang>/crisis/keywords.yaml`), each with its own exclusions (idioms such as "die laughing", talk about the show's fiction) | Calls |
| 3 | Producer talkback | The native-language keyword list on what the learner said to the producer; the producer's answer is replaced by the clip | Calls (talkback), onboarding |
| 4 | The chat host | The chat host's output flag, and the keyword lists run on the learner's message before the model is called | Chat |
| 5 | The after-session analyst | The analyst's crisis flag, after the session | Any session |

### 2.2 The keyword list never fires alone (ADR-24.15)

A keyword hit does not stop the show by itself. It sets a pending flag, and the host model is asked to confirm or deny in its next turn header:

- **The host confirms:** the protocol starts.
- **The host denies:** nothing visible happens; the hit is counted for tuning the list.
- **No answer from the host within 2 seconds** (the host model failed or stalled): the protocol starts. This is a fail-safe for a broken host, not a keyword firing on its own judgment.

The timeout fails safe, per ADR-24.B12: a missed crisis costs more than a false alarm (one interruption and a "continue" tap).

### 2.3 What the learner experiences

| Surface | What happens |
|---|---|
| **Call** | The host's line plays (`crisis.clip.host`), then the producer's line in the learner's own language (`crisis.clip.producer`). The screen shows the resources card for the learner's country and two buttons, **Continue** and **Stop for today**. On Continue, the call goes on in anxiety mode: no nudges, no recall gaps, no retell, no argument. On Stop, the call ends. |
| **Chat** | One fixed message (`crisis.chat_message`) in the learner's language, then the target language, with the resources card. The host sends nothing else until the learner writes again. |
| **Onboarding** (Salma's intake, the first call) | As for a call, with the producer's clip only. |
| **After the session** (the analyst's flag) | At the learner's next open, once, the producer shows the card with `crisis.after_session` above it. |
| **If the call fails mid-crisis** | The app shows the card from its bundled copy as soon as the crisis flag reaches it, even if the call drops (07 §5). |

Nothing else changes: no message is sent afterwards, no notebook entry is made, the next episode does not mention it.

### 2.4 What is recorded

- `crisis_log` (per ADR-24.B15): no content. The date, the residence country, the resource shown and whether the call ended, plus the source and surface, `host_confirmed` (the host confirmed before the 2-second timeout) and `learner_declined` (the learner chose to continue), both set by the protocol's own steps (per ADR-24.B20). There is no reviewer field: nobody reads the content to judge a case, and the false-positive rate is computed from the two booleans. The triggering text stays only in the learner's event log under row-level security. On account deletion the rows are de-identified (the learner id is dropped) and kept for 3 years for annual reporting, then deleted.
- `crisis_quarantine`: the triggering event id, excluded from the memory keeper, the analyst, the show canon, the callback index and the proof producer.
- An ops page with ids only, so the on-call engineer can check the protocol ran correctly. Nobody reads the triggering turn to review a case (ADR-24.15, 24.B20).

## 3. Wording for counsel

Rules for every line: short; says "AI" plainly; never diagnoses, advises or promises; never says "I understand how you feel"; points to people; leaves the choice with the learner.

### 3.1 English (target `en`, native `en`)

| Id | Who | Text |
|---|---|---|
| `crisis.clip.host` | Host, target language | "I'm going to stop the show here. I'm an AI, and I can't help with this. You deserve to talk to a real person." |
| `crisis.clip.producer` | Producer, learner's language | "This is {producer}. I'm an AI too, and this is bigger than a show. There are people who can help you right now. Their numbers are on your screen. If you're in danger, call your local emergency number." |
| `crisis.card.title` | Card | "Talk to someone now" |
| `crisis.card.body` | Card | "People at these services can talk with you now." |
| `crisis.card.emergency` | Card | "In danger right now? Call {emergency_number}." |
| `crisis.card.no_country` | Card, no checked lines for the learner's country | "We don't have checked numbers for {country} yet. This directory lists services near you:" |
| `crisis.card.continue` | Button | "Continue the show" |
| `crisis.card.stop` | Button | "Stop for today" |
| `crisis.chat_message` | Chat | "I need to step out of the show for a moment. I'm an AI and I can't help with this, but people can, right now. Their numbers are below. If you're in danger, call your local emergency number." |
| `crisis.after_session` | Producer, next open, once | "After our last session I wanted to leave these here, once. If things are hard, people at these services can help, any time. Nothing about your show changes." |

### 3.2 Arabic draft (native `ar`)

Draft for Muath's read (register A5) and a native reviewer; plain Modern Standard Arabic so it reads correctly in every Arabic-speaking country. The producer's spoken register (Gulf or neutral) is settled by the blind test (FR-524); if Gulf wins, these lines are re-voiced in that register with the same meaning.

| Id | Text |
|---|---|
| `crisis.clip.producer` | "معك سلمى. أنا أيضاً ذكاء اصطناعي، وهذا أكبر من برنامج. هناك أشخاص يستطيعون مساعدتك الآن، وأرقامهم على شاشتك. إذا كنت في خطر، اتصل برقم الطوارئ في بلدك." |
| `crisis.card.title` | "تحدّث مع أحد الآن" |
| `crisis.card.body` | "الأشخاص في هذه الجهات يستطيعون التحدث معك الآن." |
| `crisis.card.emergency` | "في خطر الآن؟ اتصل بـ {emergency_number}." |
| `crisis.card.no_country` | "لا توجد لدينا أرقام موثّقة لـ{country} بعد. هذا الدليل يعرض الخدمات القريبة منك:" |
| `crisis.card.continue` | "أكمل البرنامج" |
| `crisis.card.stop` | "أتوقف اليوم" |
| `crisis.chat_message` | "سأخرج من البرنامج للحظة. أنا ذكاء اصطناعي ولا أستطيع المساعدة في هذا، لكن هناك أشخاص يستطيعون، الآن. أرقامهم في الأسفل. إذا كنت في خطر، اتصل برقم الطوارئ في بلدك." |
| `crisis.after_session` | "بعد جلستنا الأخيرة أردت أن أترك لك هذه الأرقام هنا، مرة واحدة. إذا كانت الأمور صعبة، هناك أشخاص يستطيعون مساعدتك في أي وقت. لا شيء في برنامجك سيتغير." |

The host's clip for an Arabic-speaking learner of English is the English `crisis.clip.host`: hosts speak the target language only.

## 4. Resources per country

`packages/native/<lang>/crisis/resources.yaml` is keyed by ISO 3166-1 alpha-2 (`learners.residence_country`). Every native package carries the same numbers with the names and card copy in its language. **Every row below is a seed, unverified.** Before 2027-02-15, someone checks each number against the service's official site or calls it, and counsel approves the list; a row that cannot be verified is removed, and that country falls back to `INTL`. The list must cover every country the beta invites from (FR-1051); `INTL` covers the rest.

| ISO | Crisis line (seed) | Text option | Emergency | Status |
|---|---|---|---|---|
| US | 988 Suicide and Crisis Lifeline: 988 | Text 988 | 911 | Verify |
| CA | 9-8-8 Suicide Crisis Helpline: 988 | Text 988 | 911 | Verify |
| GB | Samaritans: 116 123 | Shout: text SHOUT to 85258 | 999 or 112 | Verify |
| IE | Samaritans: 116 123 | | 112 or 999 | Verify |
| DE | TelefonSeelsorge: 0800 111 0 111 or 0800 111 0 222 | | 112 | Verify |
| FR | Numéro national de prévention du suicide: 3114 | | 112 | Verify |
| ES | Línea 024 | | 112 | Verify |
| NL | 113 Zelfmoordpreventie: 113 or 0800-0113 | | 112 | Verify |
| IT | `[to find]` | | 112 | Find |
| AU | Lifeline: 13 11 14 | | 000 | Verify |
| NZ | Need to talk?: 1737 | Text 1737 | 111 | Verify |
| IN | Tele-MANAS: 14416 | | 112 | Verify |
| BR | CVV: 188 | | 192 | Verify |
| KR | `[to find]` | | 119 | Find |
| SA | Ministry of Health: 937; `[national mental-health line: to find]` | | 911 (997 in some regions) | Verify |
| AE | `[to find]` | | 999 (998 ambulance) | Find |
| EG | `[to find]` | | 123 (ambulance) | Find |
| KW, QA, BH, OM, JO, MA, TR | `[to find]` | | `[to find]` | Find |
| `INTL` | Find a Helpline directory: findahelpline.com | | "Your local emergency number" | Verify the directory's coverage |

```yaml
# packages/native/en/crisis/resources.yaml (shape; counsel approves every line; version = approval date)
version: "draft-2026-11-12"
by_country:
  GB:
    lines: [{name: "Samaritans", number: "116 123", hours: "24/7"}, {name: "Shout", text: "85258", body: "SHOUT"}]
    emergency: "999"
  US:
    lines: [{name: "988 Suicide and Crisis Lifeline", number: "988", text: "988"}]
    emergency: "911"
INTL:
  lines: [{name: "Find a Helpline", url: "https://findahelpline.com"}]
  emergency: null        # the card says "your local emergency number"
```

## 5. SB 243-style duties, applied to every learner

As we read California SB 243; counsel confirms both the reading and whether For one is in scope (pack A-8).

| Duty (our reading) | How For one meets it, for everyone |
|---|---|
| Tell the user clearly that they are talking to an AI | The producer and hosts say so in their first lines; an "AI" mark on every portrait; every character answers "are you real?" honestly every time; the line in onboarding and Controls (FR-560, [03](03-consent-texts.md) `ai.*`) |
| Keep a protocol that prevents the chatbot from producing suicidal-ideation or self-harm content | Hosts and the producer are forbidden from engaging with it; the output guard runs before every line; crisis replies are fixed clips, never generated (07 §4.10, §4.8) |
| Refer the user to crisis services when they express suicidal ideation | The resources card for their country, with the international fallback (§4) |
| Publish the protocol on the website | §7 below, at `/safety` |
| Use evidence-based methods to detect suicidal ideation | Three independent live triggers plus the after-session analyst; keyword lists tuned on the Milestone 0 transcripts. `[Counsel: is this enough to be "evidence-based"?]` |
| Report yearly the number of crisis referrals, without personal data | The count query in §6 |
| Duties for users known to be minors | Not applicable: 18+ only. A learner found to be under 18 is closed and deleted |

## 6. Reporting

**Weekly, to Muath (ADR-24.15).** One line in the Tuesday operations review: activations this week, by surface (call, chat, onboarding, after-session) and source, and how many ran without host confirmation or with the learner declining (the inputs to the false-positive rate, ADR-24.B20). No learner ids, no content, no dates finer than the week. Muath does not write to learners about it.

**Yearly (SB 243-style).** From `crisis_log`, counts only:

```sql
select date_trunc('year', created_at) as year, source, surface,
       count(*) as activations,
       count(*) filter (where not host_confirmed) as without_host_confirmation,
       count(*) filter (where learner_declined) as learner_declined
from crisis_log group by 1, 2, 3;
```

We know a learner's country, not their US state, so a California-only count is not possible. **Working position:** report the count for all learners whose `residence_country = 'US'`, stated as an upper bound for California, or the global count if counsel prefers. `[Counsel: recipient, first due date and scope, pack A-8.]`

## 7. Public summary (for the website, `/safety`)

> **How For one handles a crisis**
>
> For one is a language-learning show with AI hosts. It is not a help line. If you say something in a call, a chat or a conversation with the producer that suggests you might be in danger, the show stops. The character tells you plainly that it is an AI and can't help with this, and we show you help lines for the country you live in, or an international directory if we don't have checked numbers for your country yet. You choose whether to continue.
>
> These words are written in advance and checked by our lawyers. They are never made up by an AI in the moment.
>
> We detect this in several independent ways during calls and chats and after each session. When a keyword check finds a worrying phrase, it asks the host to confirm first; if the host can't answer within 2 seconds, the protocol starts anyway, because missing a crisis is worse than a false alarm.
>
> Nobody from For one contacts you about it. What you said in that moment is never used in your show, your notebook or your progress. We keep a record that the protocol ran, without what you said, and we publish once a year how many times it ran.
>
> If you are in danger now, call your local emergency number.

## 8. Before the beta

| What | Who | By |
|---|---|---|
| Counsel approves §3 and §7 | Counsel | 2027-02-15 |
| Arabic lines read by Muath and a native reviewer | Muath | 2026-12-01 (A5) |
| Every number in §4 verified; countries of the first cohort covered | Engineer, counsel | 2027-02-15 |
| Clips rendered per (target, native) pair from the approved text | Engineer | The crisis build (dated in `backlog/00-release-plan.md`) |
| Milestone 0 transcripts run through both keyword lists; false positives counted with the host-confirm step | Engineer | The crisis build |
| Keyword files carry `mode: confirm_first` only, with the 2-second fail-safe (ADR-24.15) | Engineer | The crisis build |
