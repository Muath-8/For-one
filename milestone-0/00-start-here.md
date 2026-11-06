# Milestone 0 pilot kit: start here

*For one, 10 October 2026. Everything Muath needs to run the hand-made pilot from concept v2 (section 9): 15 adults from anywhere at about B1, learning English, 14 days of personal episodes and calls on WhatsApp, before any product code. Re-dated on 23 October 2026: the pilot had not started, so every date now assumes day 1 on Sunday 1 November. Updated the same day for Muath's decisions: no launch country, monthly plans at $19.99 / $29.99 / $44.99 for 1 / 2 / 3 episodes a day, and invisible teaching. Nobody sends correction notes any more; the show echoes the right forms back instead, and a new gate 8 checks that this works.*

## What changed on 23 October

| Before | Now | Where |
|---|---|---|
| Saudi, Arabic-speaking learners | Anyone, anywhere, 18+, about B1, learning English. Messages in Arabic, English or a machine-translated third language. Aim for 3+ countries. | [01](01-recruiting.md), [02](02-consent.md) |
| Salma's evening notes, with one sentence to fix | No notes. The analyst picks errors to echo, the writer puts the right forms in the next episodes, Mona recasts like a friend, and the editor fails anything that reads as a correction | [04](04-production.md#what-the-learner-gets-each-day), [05](05-prompts.md) |
| Salma corrects | Salma sends the evening choice and answers questions only when asked (PRD v2 drops her entirely; the pilot tests whether she is needed) | [05](05-prompts.md#s-show-bible) |
| Founding price SAR 349 a year | First month of a plan: $19.99, $29.99 (recommended) or $44.99; the first 100 keep their price | [07](07-measures-and-gates.md#the-pre-pay-ask) |
| 7 gates | 8: "the errors the show echoed back appear less often by day 14", from a new Echoes tab | [07](07-measures-and-gates.md#the-gates) |
| PDPL, 911, Saudi names and food | Any law that applies, the learner's own emergency number, names and stories with no home country | [02](02-consent.md), [05](05-prompts.md), [06](06-then-and-now.md) |

## What only Muath can do, before the pilot

**This weekend (Saturday 24 and Sunday 25 October)**

1. **Get a second WhatsApp number** (a second SIM or eSIM) and install WhatsApp Business on it as "For one".
2. **Pay for three accounts:** Claude Max for the month (writer and analyst chats; turn "Help improve Claude" off in Settings, Privacy); a Google Cloud project with billing on, used in Google AI Studio (episode voices and the editor); ElevenLabs Pro at $99 a month (the calls). Budget about $250 to $350 for the whole pilot, plus about $100 for an English teacher to rate the recordings.
3. **Post the recruiting message** on Saturday evening and send it directly to 20 to 30 people asking them to forward it ([01-recruiting.md](01-recruiting.md)). Recruiting is the step most likely to fail. There is no target country now, so ask friends abroad to forward it too; if the mix ends up mostly one country, run anyway and say so in the gate report.
4. **Build the screening form and the consent form** in Google Forms from the text in [01-recruiting.md](01-recruiting.md) and [02-consent.md](02-consent.md).
5. **Choose the two host voices** and build the Mona call agent; test its link on your phone while signed out ([04-production.md](04-production.md#one-time-setup-saturday-24-to-thursday-29-october)).

**Monday 26 to Friday 30 October**

6. **Close recruiting on Wednesday 28 October, then choose the 15 learners and 3 reserves on Thursday 29**, send the acceptance messages, and book intake calls for Saturday 31 October and Sunday 1 November.
7. **Do a dry run on yourself** (one full evening cycle) and time it. At about 25 minutes per learner, 15 active learners is a 5 to 6 hour evening. If your dry run is much slower, start with 12 and keep 3 as reserves.
8. **Decide how pre-payments will be taken** on 15 November: one USD payment link per plan that takes foreign cards (Tap or Moyasar with a commercial registration, otherwise PayPal), or a bank transfer, with a written refund promise ([07-measures-and-gates.md](07-measures-and-gates.md#the-pre-pay-ask)).
9. **Find the English teacher** who will rate the recordings blind on 16 and 17 November (about 3 hours of work).
10. **Ask a lawyer, at least briefly, about the consent wording** if you can. It is written to be honest and complete for a 15-person pilot with learners in several countries (so the GDPR may apply as well as Saudi Arabia's PDPL), but it is not legal advice, and concept v2 requires a real review before anyone pays.

## The tool choices

| Job | Tool | From |
|---|---|---|
| Plan and write each day's episode, article and call brief | Claude, Project "M0 Writer" | Architecture lens |
| Analyse each call, pick the errors to echo, write Salma's message when there is one | Claude, Project "M0 Analyst" | Architecture and assessment lenses |
| Check each package before it ships | Gemini 3.8 in AI Studio (a second vendor) | Concept v2 |
| Episode audio | Gemini 3.8 Flash TTS, two voices | Voice lens |
| The call | ElevenLabs Agents, one per learner | **Changed** from the voice lens's Gemini Live, which needs a small web page and code to give learners a link with their daily brief. The cost: Mona's call voice differs from her episode voice. |
| Verbatim call transcripts | ElevenLabs Scribe v2 | Voice lens |
| Known-word coverage | [Coverage checker](https://claude.ai/artifact/HuHuT3rFgTPzzV311oXdsN) (also [tools/coverage-checker.html](tools/coverage-checker.html)) | Personalization lens |
| Delivery | WhatsApp Business | Business lens |
| Learner memory and measurement | One Google Doc per learner, plus [pilot-tracker.xlsx](pilot-tracker.xlsx) in Google Sheets | Concept v2 |

No private podcast feed in Milestone 0: it is 15 private shows to set up before the pilot starts, and WhatsApp plays audio with the phone locked. The day-14 check-in asks whether learners would rather have it in their podcast app.

## The kit

| File | What it is |
|---|---|
| [01-recruiting.md](01-recruiting.md) | Who to recruit (anyone, anywhere), the recruiting message (Arabic and English), the screening form with a 2-minute word check, how to choose, and the replies |
| [02-consent.md](02-consent.md) | The consent form in English and Arabic, and what it commits Muath to |
| [03-schedule.md](03-schedule.md) | Day by day from 24 October to the gate decision on 18 November |
| [04-production.md](04-production.md) | Tools, one-time setup, the intake call, the learner file rules, the daily cycle, personal versus generic days, the WhatsApp messages, what to do when things go wrong |
| [05-prompts.md](05-prompts.md) | The show bible, the generic topic pool, and every prompt: writer (with echoes), analyst and Salma, editor, Mona's call agent, intake |
| [06-then-and-now.md](06-then-and-now.md) | The week-0 and week-3 recordings (two matched forms), blind rating, transcript measures, the claim gate, and the finale message |
| [07-measures-and-gates.md](07-measures-and-gates.md) | What to record each day, the day-7 and day-14 check-ins, the side-by-side with a BBC show, the pre-pay ask, and the pass and stop numbers |
| [08-runbook.md](08-runbook.md) | The daily checklist: morning, slots, evening production |
| [learner-file-template.md](learner-file-template.md) | The learner file, copied into one Google Doc per learner |
| [pilot-tracker.xlsx](pilot-tracker.xlsx) | Screening with word-check scoring, roster, daily log, check-ins, the Echoes log, blind ratings, and a Gates tab that computes all 8 gates |
| [tools/episode_audio.py](tools/episode_audio.py) | Optional: turns a script into an MP3 with Gemini TTS in one command (tested against a mock, not yet the live API) |
| [tools/blind_pairs.py](tools/blind_pairs.py) | Shuffles week-0 and week-3 recordings into blind X/Y pairs with a key |

## The gate, in one line

Start building the beta on 18 November only if: 10 of 15 ask for the next episode unprompted, the median learner does 4+ sessions a week and speaks 4+ minutes a session, most still choose tomorrow's episode in week 2 and say it was worth it, most sound better in the blind then-and-now, the errors the show echoed back appear less often by day 14, personal episodes beat generic ones, and 5 of 15 pay for a first month. Details and stop lines: [07-measures-and-gates.md](07-measures-and-gates.md#the-gates).
