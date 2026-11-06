# For one: business model, unit economics and launch

*Doc version: https://claude.ai/code/artifact/b8b95e36-45e6-4bf2-8984-198d4d22ffa3. Lens: business model, unit economics and launch strategy. Written 2026-10-09 for the eleven-perspective synthesis. Builds on the [first rethink](https://claude.ai/code/artifact/21c354e1-9b24-4fcd-bb44-dca39f26d86b) and goes deeper on money and launch; it does not repeat the learning-science case.*

**The answer in one paragraph.** For one can be a good business, but not at a Duolingo price with unlimited use. Every episode is made once for one person, so cost grows with every minute a learner spends, and a better product means more cost. At October 2026 list prices one full daily session costs about $0.25 on a lean, well-engineered stack and $0.55 to $1.10 on the stacks a beta would actually start with. That fixes the model: a subscription priced like a private teacher (around SAR 89 a month or SAR 449 a year in Saudi Arabia, about $24 and $120), one new episode a day included, no free tier, sold on the web first. The launch wedge with the best evidence is Arabic-speaking "stuck intermediate" adults learning English, starting with young professionals in Saudi Arabia. The first 100 learners come from the founder's own story and a free 90-second sample episode, not from ads, and they pay from day one.

## Decisions only you can make

My recommendation is first in each row. Everything below assumes it until you say otherwise.

| # | Decision | Recommended | Alternative | Why it matters |
|---|---|---|---|---|
| 1 | Launch wedge | Arabic speakers learning English, Saudi Arabia first, working adults 22 to 35 who understand English but freeze when speaking | Wherever your own network is strongest; or US learners of Spanish | Decides language, price, channels and voices. Saudi learners pay about 2x US app prices and English is the strongest language for voice AI. |
| 2 | Price position | "Private teacher" price: SAR 89/month, SAR 449/year | "App" price: SAR 49 to 59/month, SAR 199 to 299/year | At app prices the annual plan loses money unless usage is light. See section 3. |
| 3 | Daily allowance | One new episode a day included; replays, chat and a second short call on the same episode are free | Two full new episodes a day, as the PRD says | The 2-a-day cap lets a heavy user cost $15 to $66 a month, more than they pay. |
| 4 | Charge from the beta | Yes: founding members pay a locked founding price from day one | Free beta | Free users tell you if they like it; only payers tell you if it is a business. |
| 5 | Free tier | None. A free 90-second sample episode before signup, then a 7-day trial | Freemium with limited minutes | Hard paywalls convert about 5x better (10.7% vs 2.1% of downloads) and keep 1-year retention the same. |
| 6 | Where people pay | Web checkout first (installable web app plus private podcast feed) | Native apps with App Store billing from launch | Web keeps about 96% of revenue instead of 85%; native apps come after the gates. |

If you answer only one, answer #1. It changes the voices, the price, the channels and who you recruit next week.

## 1. What it costs to serve one learner

**One full session (7-minute personal episode, article, 6-minute live call, chat, polish card, a quarter of the weekly proof) costs $0.25 to $2.00 depending on the stack.** These are my estimates from October 2026 list prices, not measurements.

| Stack | What it uses | Per session | 20 sessions/month | 60 sessions/month (PRD cap) |
|---|---|---|---|---|
| Floor | Claude Sonnet 5.5 for writing, Haiku 5.5 for analysis, overnight work on the Batch API (half price), Gemini Flash-Lite TTS, a cascade call (streaming speech-to-text, Haiku, cheap TTS) | $0.25 | $5.00 | $15.10 |
| Lean | Same writers, no batching, Gemini 3.8 Flash TTS, OpenAI realtime mini for the call | $0.55 | $11.05 | $33.14 |
| Standard | ElevenLabs Flash voices, full OpenAI realtime call | $1.11 | $22.26 | $66.77 |
| Premium | Opus-class writer, ElevenLabs v3 voices, premium realtime | $2.01 | $40.26 | $120.78 |

Where the money goes in the floor stack: episode audio 28%, writing and planning 20%, the live call 19%, checks and regeneration 7%, chat and coach 10%, everything else 16%. In the lean and standard stacks the live call alone is 38 to 49% and voices another 20 to 27%. The text models are the cheap part.

What moves the number:
- **The call is the biggest lever.** A realtime speech-to-speech model costs about $0.02 to $0.09 a minute; a cascade of streaming speech-to-text, a small model and TTS costs about $0.01. Duolingo cut its Video Call cost from about $0.30 to under $0.01 a call by moving to open-weight models, which shows how far this falls with engineering.
- **Voices are the quality bet.** ElevenLabs v3 costs about $0.52 per 7-minute episode; Gemini Flash-Lite TTS about $0.06. Whether learners can hear the difference in "would I choose this over a real podcast" is an empirical question. Test it blind in the beta.
- **Batch everything that is not live.** The planner, tomorrow's predicted episode script, the analyst and the weekly proof can all wait minutes, so they can run at half price.
- **Prices do not only fall.** Google has announced that several Gemini 3.8 prices double on 1 January 2027, which would move the floor from $0.25 to about $0.36. Keep two voice vendors wired from the start.
- **Nothing amortizes.** Unlike Duolingo, whose course is made once for millions, every For one episode is made for one person. Cost per learner rises with engagement. That is the single most important fact for the business model.

Rule for the build: **beta can afford premium; the price must be set for the floor.** 100 beta learners on the standard stack cost about $2,000 a month, which is cheap research. The price you announce must still work when you run the floor stack at 10,000 learners.

## 2. What learners already pay

**Saudi learners already pay about SAR 95 a month for an AI speaking tutor.** Speak's monthly plan in the Saudi App Store is SAR 94.99 to 99.99 (about $26), above its US price, and its unlimited Plus tier is SAR 229.99 a month.

| Product | Saudi Arabia (App Store) | US | AI voice limits |
|---|---|---|---|
| Speak | SAR 95 to 100/mo; SAR 200/yr. Plus SAR 230/mo, SAR 400/yr | $17.99/mo, $83.99/yr; Plus $39.99/mo | Premium caps daily AI lessons; Plus unlimited |
| Duolingo Super | SAR 35 to 50/mo; SAR 210 to 300/yr | $9.99 to 12.99/mo | Max (about $30/mo) has short video calls; Duolingo says it may fold Max into Super |
| Praktika | SAR 40/mo; SAR 150 to 300/yr | $9.99 to 39.99/mo | Many test prices |
| ChatGPT | Go SAR 35/mo; Plus SAR 90/mo | $8 / $20 | General purpose, no learner model |
| Human tutor | SAR 100 to 450 per hour; British Council SAR 2,350 for 4 weeks | Preply/italki $10 to 40/hour | One hour, not a daily show |

Market facts that shape the model:
- Education apps in Saudi Arabia charge about **2.0x US prices**; the UAE 1.4x; Brazil and Mexico 0.4x (Adapty 2026).
- The global median for education apps is $9.99/month and $44.99/year (RevenueCat 2026), but AI voice tutors cluster at $15 to 20/month, and unlimited voice sits at $30 to 40/month.
- **Annual plans renew poorly in education: about 24% at the first renewal, versus 56% of monthly plans.** Middle East and Africa buyers favour monthly plans (52 to 55%).
- Trial-to-paid in the Middle East and Africa runs about 20 to 23%, versus 34% in North America.
- Egypt is a far bigger pool but about 10x less able to pay (Duolingo Super is about $1.30/month there; a British Council hour is about $3). It is a later, cheaper tier, not the wedge.

## 3. The business model I recommend

**A teacher-priced subscription with a daily allowance, no ads and no free tier.**

| Option | Verdict | Reason |
|---|---|---|
| Subscription, teacher-priced, one new episode/day | **Recommended** | Matches a cost that scales with use; priced against a tutor, not against Duolingo |
| Freemium with ads | Reject | Ads conflict with the trust contract and the intimacy of voice data; free users still cost money every session |
| Pay per session or credits | Reject | A meter makes every session a "is this worth it" decision, which is the anxiety the product exists to remove |
| Lifetime deal | Reject | Unbounded cost for a one-time payment |
| B2B first (employers, universities) | Later | Real money in Saudi (only 44% of companies offer language training), but slow sales before the product is proven |

### Plans and prices

| Plan | Saudi price (incl. 15% VAT) | US equivalent | Includes |
|---|---|---|---|
| Founding member (first 100) | SAR 349 for the first year, paid on the web | $99 | Everything; price locked while subscribed |
| Daily, monthly | SAR 89 | $19.99 | One new episode a day, call, chat, polish card, weekly proof |
| Daily, annual | SAR 449 | $119 | Same |
| Intensive (later, from beta data) | about SAR 179/mo | about $39.99 | Two new episodes a day, longer calls, real-life rehearsal |

The "one new episode a day" rule replaces the PRD's two-a-day cap. It fits the habit you described (one daily hour), it is honest, and the show can say it in character ("tomorrow's episode needs the night to be made"). Replays, the article, the chat and a second short call on the same episode stay free because they cost almost nothing.

### Margin per paying learner

Saudi VAT (15%) comes out of the price before any fee. App Store small-business commission is 15%; Stripe on the web is about 4%.

| Plan | Net to For one per month | Cost at floor stack | Contribution |
|---|---|---|---|
| SAR 89 monthly, App Store | $17.54 | $4.50 (18 sessions) | $13.04 (74%) |
| SAR 89 monthly, web | $19.82 | $4.50 | $15.32 (77%) |
| SAR 449 annual, App Store | $7.38 | $3.00 (12 sessions, annual users use less) | $4.38 (59%) |
| SAR 449 annual, web | $8.33 | $3.00 | $5.33 (64%) |
| SAR 299 annual, App Store (app price) | $4.91 | $4.50 if used daily | $0.41 (8%) |
| SAR 59 monthly, App Store (app price), on the lean stack a beta starts with | $11.63 | $9.94 (18 sessions) | $1.69 (15%) |

At app prices the monthly plan works only once the floor stack is reached, and the annual plan barely works at all, so the business would depend on learners using it lightly. That is the opposite of what a product about daily practice wants. At teacher prices it works with room for better voices.

### What one payer is worth, and what you can spend to get one

- **Monthly payer:** first renewal 56% (education benchmark), then I assume 20% monthly churn, so about 3.8 paid months × $13 = **about $49** contribution.
- **Annual payer:** one year at $52.50 plus a 24% chance of a second year = **about $65**.
- **Blended:** about **$55 to $60** per payer. To keep a 3:1 ratio, a payer must cost under about $20 to acquire.
- Paid ads can reach that only with a hard paywall: Saudi installs cost roughly $2 (weak data, about 0.4x the US) and hard-paywall apps convert about 10.7% of downloads, so about $20 per payer. With freemium conversion (2.1%) it would be about $100. Ads are a scaling tool after the gates, not a launch channel.

## 4. The wedge: who first, which language

**Arabic speakers learning English, starting with Saudi working adults aged 22 to 35 at roughly B1 (they understand a lot, read fine, and freeze when they speak).** This assumes your own network is Arabic-speaking, as the PRD's examples suggest; if it is not, the founder-fit row below changes the answer.

| Factor | Saudi Arabic speakers → English | US English speakers → Spanish |
|---|---|---|
| Need | Saudi Arabia ranks 115th of 123 on EF EPI 2025 ("very low"); 93% of Saudi workers say English affects their pay; advanced speakers earn SAR 279k vs SAR 147k | Mostly hobby; Spanish is #1 on Duolingo in all 50 states |
| Willingness to pay | About 2x US app prices; Speak charges SAR 95/month | US prices, crowded |
| Voice AI quality | English is the strongest language for every realtime and TTS model. Arabic UI and explanations only need text, which LLMs do well | Spanish is good but second tier |
| Competition | Global apps translated into Arabic; nobody builds a personal show around Saudi life | Dreaming Spanish, Speak, Langua, Duolingo |
| Founder fit | You learned English this way; you can interview learners in their language | Low |
| Reach | 34M people, median age 30, 99% online; TikTok, Snapchat, YouTube reach almost all adults | Large but expensive to reach |

Why not Arabic as a target language first: dialect TTS still "falls short" of English (Habibi 2026), the largest open Arabic TTS dataset is under 100 hours, and diglossia makes "which Arabic?" a product question of its own.

Why not beginners: the show format needs about 2,000 known words (first rethink). Why not Egypt first: willingness to pay is about a tenth. Egypt and the Levant are the second step, with a cheaper listen-first plan.

The precedent: Speak started in Korea for the same reasons (intense career-driven demand for English speaking), and Korea was still 91% of its first $20M in revenue. Aleem in Kazakhstan, aimed at A2 to B1 English learners, got 40,000 users and $10,000 in pre-sales from a Telegram mini-app before its full launch.

## 5. The smallest product that proves the thesis

**The thesis has three claims (the show earns the time, the teacher makes it count, people pay), and the smallest product must test all three.** Anything that tests none is cut.

| In the first paid version | Out until after the gates |
|---|---|
| Intake conversation (text plus voice, Arabic or English) | Character creation and the six chassis |
| Default duo per launch dialect of English, one voice pair | More than one language pair |
| One daily personal episode, delivered to a private podcast feed and the web app | Native iOS and Android apps |
| Live call with the host (realtime model or cascade) | Settings screens |
| Text chat and the opt-in polish card | World-news scout (use interests and follow-ups only) |
| Weekly proof with voice then and now | Real-life rehearsal and bring-your-own-input (first paid add-ons after launch) |
| Hidden 4-weekly speaking sample | Intensive plan |
| Web checkout (Stripe or a local processor supporting Mada and Apple Pay), cost-per-session telemetry | Referral programs, community |

Two delivery choices matter for the business:
- **The private podcast feed** puts the episode inside a habit people already have and gives the self-chosen cue for free. It also avoids iOS limits on background audio in web apps.
- **WhatsApp for Milestone 0.** In the Gulf, WhatsApp is where daily habits live. For the hand-made first 15 learners, send the episode as audio, the article as a link, take the call through a web link and do the chat in WhatsApp. It needs no app and shows whether the show is wanted before anything is built.

## 6. Finding the first 100 learners

**Sell the show by giving one away: a free 90-second English episode about the person's own team, job or city, made from three questions, sent to their WhatsApp.** It costs about $0.03 to make, it demonstrates the whole idea in a minute, and people share things that are about them. (The PRD rules out proof-clip sharing; a sample episode the person chooses to forward is different and fits the trust contract.)

Funnel to 100 founding members, assuming warm, hand-invited learners convert better than store benchmarks:

| Stage | Count | Assumption |
|---|---|---|
| Sample episodes made | about 2,000 | From the channels below |
| Waitlist with intake answers | about 1,000 | Half leave details for the full show |
| Invited to a 7-day trial (weekly batches of about 50) | about 350 | Filtered for B1-ish level and career goal |
| Pay the founding price | about 100 | About 30% of a warm, hand-picked cohort (benchmark 20 to 23% for cold store trials in the region) |

Channels, in order:
1. **Your own story in Arabic.** Short videos on TikTok, Snapchat and Instagram: "I taught myself English with one hour a day; this is the hour, rebuilt with AI." Speak's best-performing content in Korea was "common mistakes" posts and a recurring teacher persona; the For one equivalent is the hosts reacting to a real learner's (consented) sentence.
2. **Your network and the first 15.** Milestone 0 learners are recruited by hand. Each one who loves it is asked for two names.
3. **University and workplace groups.** English clubs, graduating-student groups, LinkedIn posts aimed at young professionals preparing for interviews.
4. **WhatsApp and Telegram learning groups** and IELTS preparation communities, where the sample episode is the offer.
5. **Not yet: paid ads.** They work only after the hard paywall converts and the gates pass (section 3).

## 7. The first 90 days and their gates

**Three gates, each with a number that passes and a number that stops spending.** Day 0 is Monday 2026-10-12; day 90 is 2027-01-10.

| Phase | Dates | What happens | Gate to pass |
|---|---|---|---|
| Milestone 0, hand-made | Oct 12 to Nov 1 | 15 learners, 14 days, episodes made with LLM help and checked by hand, delivered by WhatsApp and private feed; sample-episode waitlist opens | 10 of 15 ask for the next episode unprompted; median 4+ sessions a week; at least 5 of 15 pre-pay the founding price |
| Build the beta | Nov 2 to Dec 6 | Web app, feed, live call, polish card, weekly proof, payments, cost telemetry; waitlist keeps growing | Cost per session measured; a costed path to $0.30 or less |
| Paid founding beta | Dec 7 to Jan 10 | Invite about 50 a week into 7-day trials; founding price | Day 60 and day 90 checks below |

What to measure, and the line where you stop and rethink:

| Metric | Why | Target | Stop-and-rethink line |
|---|---|---|---|
| Trial to paid (founding price) | Do people pay | 30%+ | Under 15% |
| Active in week 4 (paid) | Does the show earn the time | 40%+ | Under 25% |
| Sessions per active learner per week | Habit | 4+ | Under 2.5 |
| Minutes of learner speech per session | Is the teacher getting output | 4+ | Under 2 |
| 4-weekly speaking sample, rated blind | Does it actually teach | Most learners improve on accuracy, fluency or complexity | No measurable change |
| Second-month renewal | Will it last | 60%+ (benchmark 56%) | Under 40% |
| "Very disappointed" if For one disappeared | Product-market fit signal | 40%+ | Under 25% |
| Cost per session | Margin | Under $0.60 now, plan to $0.30 | Over $1.00 with no plan |
| New trials from referrals and shared samples | Can it grow without ads | 30%+ | Under 10% |

If a gate fails, find which claim failed (the show is not wanted, the teacher is not felt, the price is wrong) before writing more code.

## 8. The sequence after day 90

1. **Prove the floor cost (months 4 to 6).** Move to the floor stack piece by piece, A/B testing each voice and call change against "would choose this over a real podcast". Launch publicly in Saudi Arabia, the UAE and Kuwait at the teacher price. Add the annual plan and real-life rehearsal ("my interview is Sunday") as the first paid add-on.
2. **Native apps and paid acquisition (months 6 to 9),** only after week-4 retention and renewal pass. Native apps bring background audio, hands-free calls and store discovery; App Store billing costs 15%.
3. **Second market, same language (months 9 to 12).** Egypt, Jordan and the Levant with a cheaper, listen-first plan (more episode, shorter calls) priced for local purchasing power.
4. **Employers and universities (year 2).** Seats for companies training staff in English; the weekly proof becomes the progress report the employer pays for, with the learner's consent.
5. **Second language pair (year 2),** chosen by data, through the PRD's language-package system. Human bridges (a real tutor who receives the learner file) come after that.

## 9. Risks to the business

- **Cost squeeze from heavy users.** Mitigated by the one-new-episode-a-day allowance and the Intensive plan.
- **Vendor prices rise as well as fall.** Gemini's January 2027 doubling is the example; keep two voice vendors and move non-live work to batch.
- **Duolingo or Speak add a personal podcast.** DuoRadio already generates episodes at scale. The defence is the learner file and fifty episodes of shared history, which the first rethink calls the moat. Speed to a loved show matters more than features.
- **Payment and platform rules.** Apple's US link-out rules are still in court; plan for some fee on web links eventually. In Saudi Arabia, local cards (Mada) and wallets matter; check which processor supports them before the beta.
- **Voice data law.** Storing Saudi residents' voice recordings falls under the Personal Data Protection Law. Get local advice on consent and cross-border storage before the paid beta. This is a flag, not legal advice.

## Sources

Prices checked 2026-10-09; figures marked "about" are estimates or conversions.

- AI pricing: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing); [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing); [ElevenLabs API pricing](https://elevenlabs.io/pricing/api); [Google Cloud TTS pricing](https://cloud.google.com/text-to-speech/pricing); [Deepgram pricing](https://deepgram.com/pricing); [realtime cost in practice, forasoft](https://www.forasoft.com/blog/article/openai-realtime-api-pricing); [Cerebrium cost per minute](https://cerebrium.ai/resources/voice-ai-agent-cost-per-minute); Claude model prices from Anthropic's current price list.
- [Duolingo Video Call cost, TIKR](https://www.tikr.com/blog/duolingo-cut-its-priciest-ai-feature-to-under-a-penny-a-call-heres-what-that-does-to-margins); [Duolingo Q2 2026 shareholder letter](https://www.sec.gov/Archives/edgar/data/0001562088/000162828026053299/q2fy26duolingo6-30x26share.htm).
- App prices: [Speak, Saudi App Store](https://apps.apple.com/sa/app/id1286609883); [Duolingo, Saudi App Store](https://apps.apple.com/sa/app/id570060128); [Praktika, Saudi App Store](https://apps.apple.com/sa/app/id1624701477); [ChatGPT, Saudi App Store](https://apps.apple.com/sa/app/id6448311069); [Speak US review](https://speakshark.com/blog/speak-app-review-2026).
- Tutors: [TutorChase Saudi](https://www.tutorchase.com/english/saudi-arabia); [British Council Saudi](https://saudiarabia.britishcouncil.org/en/english/courses-adults/englishplus); [British Council Egypt](https://www.britishcouncil.org.eg/en/english/courses-adults/general-english).
- Benchmarks: [RevenueCat State of Subscription Apps 2026](https://www.revenuecat.com/state-of-subscription-apps/); [RevenueCat 2026 trends](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026); [RevenueCat renewal rates](https://www.revenuecat.com/blog/growth/average-subscription-renewal-rates-by-app-category.md); [Adapty education benchmarks](https://adapty.io/blog/education-app-subscription-benchmarks/); cost-per-install estimates, [Linkrunner](https://linkrunner.io/tools/cost-per-install-benchmark).
- Market: [EF EPI 2025 Saudi fact sheet](https://www.ef.com/assetscdn/WIBIwq6RdJvcD9bc8RMd/cefcom-epi-site/fact-sheets/2025/ef-epi-fact-sheet-saudi-arabia-english.pdf); [Pearson Saudi skills findings, Gulf Business](https://gulfbusiness.com/en/2024/industry/the-economy-of-language-saudi-arabias-young-workers-pivot-to-english); [DataReportal Saudi Arabia 2025](https://datareportal.com/reports/digital-2025-saudi-arabia); [Duolingo 2024 language report](https://blog.duolingo.com/2024-duolingo-language-report/).
- Launch precedents: [Speak in Korea, Sensor Tower](https://sensortower.com/ko/blog/Speak-top-1-by-revenue-in-the-education-category-of-the-Korean-market-for-a-year); [Accel memo on Speak's Korea choice](https://www.accel.com/news/artifact-the-investor-memo-outlining-how-speak-decided-to-launch-in-korea.md); [Aleem, Digital Business KZ](https://digitalbusiness.kz/en/2025-12-17/kazakh-entrepreneurs-launch-aipowered-englishlearning-app-thats-hit-300-000-downloads/).
- Arabic voice quality: [Habibi TTS paper](https://arxiv.org/html/2601.13802v2); [HUMAIN Arabic TTS benchmark](https://www.middleeastainews.com/p/humain-sawtarabi-arabic-tts-benchmark).
- Platform fees: [Apple EU terms, iClarified](https://www.iclarified.com/101814/apple-revises-eu-app-store-terms-replaces-core-technology-fee-with-5-commission); [Google Play fee changes, TechCrunch](https://techcrunch.com/2026/03/04/google-settles-with-epic-games-drops-its-play-store-commissions-to-20).
