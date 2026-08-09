# Lucent — External Services Stack

## Backend and frontend 
### Next.js

## AI and Voice

1. **LLM and AI Models — openrouter **
   Used for content generation, learner assessment, personalization, memory extraction, dictionary definitions, and translation.

2. **Speech-to-Text — ElevenLabs**
   Used to transcribe onboarding conversations, live call-ins, and user voice recordings.

3. **Text-to-Speech — ElevenLabs**
   Used to generate podcast episodes, character voices, onboarding audio, and Weekly Proof episodes.

4. **Real-Time Voice Infrastructure — LiveKit**
   Manages live audio streaming, turn-taking, interruptions, and the real-time voice pipeline.

## Data and Storage

5. **Primary Database — Supabase PostgreSQL**
   Stores users, sessions, learner profiles, characters, assessments, memories, and application data.

6. **Vector Search and Memory Retrieval — pgvector in Supabase**
   Retrieves relevant memories, previous conversations, user interests, language patterns, and character history.

7. **Audio and File Storage — Supabase Storage**
   Stores generated episodes, transcripts, articles, user recordings, and Weekly Proof audio.

8. **Authentication — Clerk**
   Handles account creation, login, session management, and user identity.

## Application Infrastructure

9. **Frontend and Backend Hosting — Vercel**
   Hosts the web application, Next.js backend functions, APIs, and frontend assets.

10. **Background Jobs and Scheduling — Trigger.dev**
    Runs episode generation, post-session analysis, nightly planning, retries, and Weekly Proof generation.

11. **Cache and Temporary State — Upstash Redis**
    Stores temporary session state, rate limits, job locks, cached data, and real-time conversation state.

## Language and Content Services

12. **Dictionary and Lexical Definitions — Low-Cost Model openrouter**
    Generates contextual definitions, parts of speech, examples, and native-language explanations for tap-to-define.

13. **Translation — Low-Cost Model openrouter**
    Handles contextual translations, onboarding language support, and multilingual explanations.

14. **News and Web Search — Exa**
    Finds current events and relevant external information for personalized episode pitches.

## Communication and Payments

15. **Transactional Email — Resend**
    Sends authentication emails, account notifications, data exports, and deletion confirmations.

16. **Payments and Subscription Management — Stripe with Clerk**
    Handles subscriptions, checkout, billing status, and access control linked to Clerk accounts.

## Analytics and Reliability

17. **Analytics, Error Monitoring, and Feature Flags — PostHog**
    Tracks product usage, retention, session completion, errors, experiments, and gradual feature rollouts.
