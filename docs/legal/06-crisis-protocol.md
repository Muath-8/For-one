# Crisis and self-harm protocol

> **Self-reviewed against legal/00; not reviewed by a lawyer; see the triggers** ([00-self-review-checklist.md](00-self-review-checklist.md) §25). The protocol as designed in 07 §4.8 and D9, 03 D15, PRD FR-570 to FR-572, ADR-24.15, 24.B12, B15, B20, B29 and ADR-25.3(d). Checked against legal/00 §19. Muath approves the wording and reads the Arabic (register A3, A4).

**Ships to.** Clip wording: `packages/native/<lang>/crisis/clips/` (the producer's line, in the learner's language), rendered at package build from the approved text. Card and chat copy and the directory link: `packages/native/<lang>/crisis/resources.yaml`. Keyword lists: `crisis/keywords.yaml` in both package kinds. The public summary: the website page `/safety`.

## 1. Principles

1. **The show stops being a show.** The host stops, the show says plainly that it is an AI and cannot help with this, and points to people who can.
2. **Fixed words, never generated.** Every line in a crisis is pre-written, approved and pre-rendered. A model under pressure is the wrong thing to improvise a crisis line (07 §8).
3. **The right country's help, from a maintained source.** Resources come from a maintained international helpline directory, opened at the page for the country the learner told us they live in (never a guess from their IP). We keep no hand-made list of numbers, because a list nobody maintains goes wrong (ADR-25.3).
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

### 2.2 The keyword list waits for the host, then fails safe (ADR-24.B12)

A keyword hit sets a pending flag, and the host model is asked to confirm or deny in its next turn header:

- **The host confirms:** the protocol starts.
- **The host denies:** nothing visible happens; the hit is counted for tuning the list.
- **No answer from the host within 2 seconds:** the protocol starts anyway. A missed crisis costs more than a false alarm (one interruption and a "continue" tap).

### 2.3 What the learner experiences

| Surface | What happens |
|---|---|
| **Call** | The host stops. A pre-recorded clip in the learner's own language, in the producer's voice, plays (`crisis.clip.producer`): the one time the producer speaks in a call (ADR-24.B29). The screen shows the resources card and two buttons, **Continue** and **Stop for today**. On Continue, the call goes on in anxiety mode: no nudges, no recall gaps, no retell, no argument. On Stop, the call ends. |
| **Chat** | One fixed message (`crisis.chat_message`) in the learner's language, then the target language, with the resources card. The host sends nothing else until the learner writes again. |
| **Onboarding** (Salma's intake, the first call) | As for a call. |
| **After the session** (the analyst's flag) | At the learner's next open, once, the producer shows the card with `crisis.after_session` above it. |
| **If the call fails mid-crisis** | The app shows the card from its bundled copy as soon as the crisis flag reaches it, even if the call drops (07 §5). |

Nothing else changes: no message is sent afterwards, no notebook entry is made, the next episode does not mention it.

### 2.4 What is recorded

- `crisis_log` (ADR-24.B15, B20): no content. The date, the residence country, the resource shown, whether the call ended, the source and surface, `host_confirmed` (the host confirmed before the 2-second timeout) and `learner_declined` (the learner chose to continue), both set by the protocol's own steps. There is no reviewer field: nobody reads the content to judge a case, and the false-positive rate is computed from the two booleans. The triggering text stays only in the learner's event log under row-level security. On account deletion the rows are de-identified (the learner id is dropped) and kept for 3 years for annual reporting, then deleted.
- `crisis_quarantine`: the triggering event id, excluded from the memory keeper, the analyst, the show canon, the callback index and the proof producer.
- An alert to Muath with ids only, so the protocol can be checked to have run. Nobody reads the triggering turn to review a case.
- **Basis** (legal/00 §7): the explicit consent the learner gives at account creation (`special_category`), and vital interests when the learner cannot act.

## 3. Wording

Rules for every line: short; says "AI" plainly; never diagnoses, advises or promises; never says "I understand how you feel"; points to people; leaves the choice with the learner.

### 3.1 English (native `en`)

| Id | Who | Text |
|---|---|---|
| `crisis.clip.producer` | Producer, learner's language | "This is {producer}. I'm an AI, and this is bigger than a show. I can't help with this, but people can, right now. Look at your screen for who to contact. If you're in danger, call your local emergency number." |
| `crisis.card.title` | Card | "Talk to someone now" |
| `crisis.card.body` | Card | "These services have people who can talk with you now. The list is kept up to date by an international helpline directory." |
| `crisis.card.directory_link` | Card, the button | "Help lines in {country}" |
| `crisis.card.emergency` | Card | "In danger right now? Call your local emergency number." |
| `crisis.card.continue` | Button | "Continue the show" |
| `crisis.card.stop` | Button | "Stop for today" |
| `crisis.chat_message` | Chat | "I need to step out of the show for a moment. I'm an AI and I can't help with this, but people can, right now. Who to contact is below. If you're in danger, call your local emergency number." |
| `crisis.after_session` | Producer, next open, once | "After our last session I wanted to leave this here, once. If things are hard, people at these services can help, any time. Nothing about your show changes." |

### 3.2 Arabic (native `ar`, for Muath's read)

Plain Modern Standard Arabic so it reads correctly in every Arabic-speaking country, and gender-neutral (24.B26): no second-person verbs or pronoun endings, which change with the listener's gender when spoken; verbal nouns, first person and "يُرجى" instead. These neutral lines are used for every learner, whatever address form they chose, because a crisis line must never guess. If the producer's voice test (register M8) picks a Gulf register, these lines are re-voiced in that register with the same meaning.

| Id | Text |
|---|---|
| `crisis.clip.producer` | "هنا سلمى. أنا ذكاء اصطناعي، وهذا أكبر من برنامج. لا أستطيع المساعدة في هذا، لكن هناك أشخاص يستطيعون المساعدة الآن، وطرق التواصل معهم على الشاشة. وفي حالة الخطر، يُرجى الاتصال برقم الطوارئ المحلي." |
| `crisis.card.title` | "للحديث مع أحد الآن" |
| `crisis.card.body` | "في هذه الجهات أشخاص مستعدون للحديث الآن. القائمة يحدّثها دليل دولي لخطوط المساعدة." |
| `crisis.card.directory_link` | "خطوط المساعدة في {country}" |
| `crisis.card.emergency` | "في حالة الخطر الآن: الاتصال برقم الطوارئ المحلي." |
| `crisis.card.continue` | "متابعة البرنامج" |
| `crisis.card.stop` | "التوقف لهذا اليوم" |
| `crisis.chat_message` | "سأخرج من البرنامج للحظة. أنا ذكاء اصطناعي ولا أستطيع المساعدة في هذا، لكن هناك أشخاص يستطيعون المساعدة الآن، وطرق التواصل معهم في الأسفل. وفي حالة الخطر، يُرجى الاتصال برقم الطوارئ المحلي." |
| `crisis.after_session` | "بعد الجلسة الأخيرة، أترك هذا هنا مرة واحدة. عند صعوبة الأمور، هناك أشخاص يستطيعون المساعدة في أي وقت. لا شيء في البرنامج سيتغير." |

## 4. Resources: a maintained international directory

**Final position (ADR-25.3(d)).** The card opens the page for the learner's `residence_country` in a maintained international helpline directory, Find A Helpline (findahelpline.com, maintained by ThroughLine), and always tells the learner to call their local emergency number. We keep no per-country list of numbers. If the directory's data feed is licensed later, the card may show the lines inline from that feed, never from a list we type ourselves.

```yaml
# packages/native/en/crisis/resources.yaml (shape; version = the date Muath approves it)
version: "draft"
directory:
  name: "Find A Helpline"
  url_for_country: "https://findahelpline.com/countries/{iso_lower}"   # checked at build for every ISO code; falls back to the home page
  fallback_url: "https://findahelpline.com"
emergency_line: crisis.card.emergency     # no number is hard-coded
card: [crisis.card.title, crisis.card.body, crisis.card.directory_link, crisis.card.emergency]
```

**Checks** (legal/00 §19): ☐ a build test opens the directory URL for every country in the country picker and fails on a dead link (falling back to the home page is allowed); ☐ the card renders from the app's bundled copy with no network call except the link itself; ☐ opening the link is the learner's own tap, so nothing about the learner is sent to the directory by us.

## 5. SB 243-style duties, applied to every learner

As For one reads California SB 243 (legal/00 §19). The protocol applies to everyone whether or not the law reaches a given learner.

| Duty | How For one meets it, for everyone |
|---|---|
| Tell the user clearly that they are talking to an AI | The producer says so in her first line; an "AI" mark on every portrait; every character answers "are you real?" honestly every time; the line in onboarding and Controls (FR-560, [03](03-consent-texts.md) `ai.*`) |
| Keep a protocol that prevents the chatbot from producing suicidal-ideation or self-harm content | Hosts and the producer are forbidden from engaging with it; the output guard runs before every line; crisis replies are fixed clips, never generated (07 §4.10, §4.8) |
| Refer the user to crisis services when they express suicidal ideation | The resources card with the directory for their country (§4) |
| Publish the protocol on the website | §7 below, at `/safety` |
| Use evidence-based methods to detect suicidal ideation | Three independent live triggers plus the after-session analyst; keyword lists built from published crisis-language lists and tuned on synthetic and scripted calls and volunteer clips (ADR-25.6), then on false-start counts after launch |
| Report yearly the number of crisis referrals, without personal data | The count query in §6 |
| Duties for users known to be minors | Not applicable: 18+ only. A learner found to be under 18 is closed and deleted |

## 6. Reporting

**Weekly, to Muath (ADR-24.15).** One line in the weekly report: activations this week, by surface (call, chat, onboarding, after-session) and source, and how many ran without host confirmation or with the learner declining (the inputs to the false-positive rate, ADR-24.B20). No learner ids, no content, no dates finer than the week. Muath does not write to learners about it.

**Yearly.** From `crisis_log`, counts only:

```sql
select date_trunc('year', created_at) as year, source, surface,
       count(*) as activations,
       count(*) filter (where not host_confirmed) as without_host_confirmation,
       count(*) filter (where learner_declined) as learner_declined
from crisis_log group by 1, 2, 3;
```

**Final position.** We know a learner's country, not their US state, so a California-only count is not possible. The yearly count for all learners whose `residence_country = 'US'` is published at `/safety`, stated as an upper bound for California, and filed with the recipient the law names if it applies. The global count is published next to it.

## 7. Public summary (for the website, `/safety`)

> **How For one handles a crisis**
>
> For one is a language-learning show with AI hosts. It is not a help line. If you say something in a call, a chat or a conversation with the producer that suggests you might be in danger, the show stops. We tell you plainly that this is an AI and can't help with this, and we show you help lines for the country you live in, from an international directory that keeps them up to date. You choose whether to continue.
>
> These words are written in advance. They are never made up by an AI in the moment.
>
> We detect this in several independent ways during calls and chats and after each session. When a keyword check finds a worrying phrase, it asks the host to confirm first; if the host can't answer within 2 seconds, the protocol starts anyway, because missing a crisis is worse than a false alarm.
>
> Nobody from For one contacts you about it. What you said in that moment is never used in your show, your notebook or your progress. We keep a record that the protocol ran, without what you said, and we publish once a year how many times it ran.
>
> If you are in danger now, call your local emergency number.

## 8. Before launch

| What | Who |
|---|---|
| Muath approves §3 and §7 after the AI review pass checks them against legal/00 §19 | Muath |
| Arabic lines read by Muath (register A3) | Muath |
| Clips rendered per native language from the approved text | Agent |
| The directory link test passes for every country in the picker | Agent |
| Keyword lists run over the synthetic and scripted calls and the volunteer clips; false starts counted with the host-confirm step | Agent |
| Keyword files carry `mode: confirm_first` only, with the 2-second fail-safe | Agent |
