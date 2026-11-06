# Client app, podcast feed and delivery

*Architecture domain 6 of 9 for the For one beta. Written 2026-10-16, revised 2026-10-17, against PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the UI/UX and voice lenses, and the Milestone 0 kit. It covers everything the learner touches that is not the live call's audio pipeline: the installable web app, the player, the word sheet, the private podcast feed, web push and email, auth, bidirectional text, the client-to-backend API, realtime for the drop, state management, analytics, accessibility and the sample-episode landing page. It builds on the five sibling documents already written (01 topology, 02 pipeline, 03 live call, 04 learner model, 05 assessment) and reuses their names; where it changes one of their decisions it says so in section 9.*

---

## 1. Summary and the decisions in one table

The client is a thin, logic-free installable web app whose job is to play audio well, show text in two directions well, and send honest events. Every rule about the learner (doors, the allowance, consent, counts) lives in `api`; the client reflects it. The private podcast feed is a first-class second channel that carries the part of the product phone browsers do worst (lock-screen listening on the commute) and hands the learner back to the app for the call through one link. Three message kinds leave the product and the service worker refuses to render anything else.

| # | Decision | Why | Alternative rejected |
|---|---|---|---|
| D1 | **Next.js 15 (App Router, React 19, TypeScript) on Vercel Pro**, one project serving two hostnames: `forone.app` (public: landing, sample, share, invite, legal) and `app.forone.app` (the PWA). `web` holds no vendor key and no learner logic [DECISION, confirms topology D2; PRD-v2 1.4] | Server rendering for the Arabic landing page, mature PWA tooling (Serwist), Git-integration deploys, one engineer can ship it; two hostnames keep the PWA's cookie jar, service-worker scope and edge caching clean | Vite SPA (no SSR landing, no edge cache); Remix or SvelteKit (smaller hiring pool, no gain); Expo/React Native (PRD 1.4: native after the beta); HTMX from the Python API (a karaoke player and a WebRTC screen need a client framework) |
| D2 | **PWA through `@serwist/next`**: precached shell; today's episode (app audio, `timings.json`, `glosses.json`, `package.json`, article and recap audio) plus the last two episodes stored in Cache Storage by an explicit page-side `cache.add()`; **cached audio is played from a Blob URL read out of Cache Storage, never through the service worker's fetch handler**; offline event queue in IndexedDB replayed for 24 h [DECISION; PRD-v2 1.4, 15] | Dropped episode starts in under 2 s from local bytes; the bus has no signal; Safari's handling of media-element Range requests through a service worker has a history of bugs, and a Blob URL of a 6 MB file sidesteps it entirely while keeping seeking and Media Session; iOS evicts storage of non-installed sites after 7 days of disuse but exempts home-screen apps, which A10 asks for | Streaming only (fails on the commute); relying on `RangeRequestsPlugin` for playback (kept only as a fallback for the uncached-but-partially-fetched case); caching every episode (quota and eviction on iOS) |
| D3 | **Player: one `<audio>` element on the stitched app file (`episode.m4a`) for every ready episode; a two-element scene handoff only while an on-demand episode is still streaming** (swap, return, pilot, sample); Media Session for lock screen and headphones; speeds 0.75, 0.85, 1.0 and nothing above [DECISION; PRD-v2 5.1, 3.6, 3.8] | One element keeps the lock-screen position, scrubbing and Media Session simple on iOS; a seam gap of 100 to 300 ms on the scene handoff is acceptable only where the script already has a sting or beat, which is exactly where the pipeline's segments end (`segments[].seam`) | MSE/ManagedMediaSource (iOS support too new, no gain for a 6 MB file); per-segment elements everywhere (topology 4.6; gapless handoff is unreliable on iOS and complicates seeking) |
| D4 | **Word sheet is a local lookup** in the shipped `WordIndex`; the word's audio is a play of the cached episode audio at `[s, e]` on a second, hidden audio element sharing the same Blob URL; phrase selection resolves to a chunk gloss if the span is a known chunk, else the stacked single-word glosses [DECISION; PRD-v2 5.7] | 300 ms allows no network; the gloss cache is the pipeline's; the host's voice comes from the episode bytes already on the device | Server lookup on tap; synthesizing the word |
| D5 | **Private feed: RSS 2.0 with the iTunes namespace at `GET /f/{token}.xml`; enclosures at `GET /f/{token}/{episodeId}.mp3` served by `api` with Range passthrough (the topology's route); the enclosure is an MP3 (`episode_feed.mp3`, 96 kbps mono) rendered by the pipeline's mix step next to its AAC app file** [DECISION; PRD-v2 3.3, 5.1, 12.6] | The token in the path is the only credential podcast apps can carry; MP3 is the one format every podcast app plays and seeks; Range is what every app uses to resume; Part 18 #11 says the apps Saudi learners use are unknown, so the format with zero compatibility risk wins one extra ffmpeg encode | AAC `.m4a` enclosure (the pipeline's `episode_feed.m4a`; Apple Podcasts and most Android apps play it, but `moov`-at-end files break seeking unless fast-started and a few Android apps still refuse `audio/mp4`; kept as the fallback if the pipeline cannot add the encode: then the enclosure is `audio/mp4` with `-movflags +faststart` and the week-3 podcast-app test decides); signed expiring URLs (podcast apps cache the enclosure URL for days) |
| D6 | **Feed listening is never counted as a `play` event.** Fetches are logged server-side in `feed_fetches` (user agent, range, bytes) for operations and Part 18 #11; hours heard credits a feed episode once at full length only when the learner later uses that episode's call, chat or small door (the data domain's rule, its 4.3.9); the return episode is triggered by an app open or a feed deep-link tap, never by a feed poll or an enclosure download [DECISION; PRD-v2 12.3, 3.8] | Apple Podcasts and others auto-download new items, so an enclosure fetch is not a play; counting it would fake activity, which law 1 and the trust contract forbid | Treating a full-file Range fetch as a play (PRD-v2 3.8.3 says "plays the feed"; topology 3.6 says "feed fetch"; see section 10 item 6) |
| D7 | **Feed-to-call handoff through a feed link token**: the feed item's notes carry `https://app.forone.app/call/{episodeId}?k={feedLinkToken}`; `api` exchanges `k` for a **limited session** (scope `feed_link`: this episode's call, article, chat and Today; nothing in Controls, billing, export or deletion) in whatever browser opens it [DECISION; PRD-v2 5.1, 5.4.1, 16.2] | On iOS the podcast app opens the link in Safari, which shares no cookies with the installed PWA; without a token the learner would have to sign in before every call from the feed, which is the handoff the beta is told to watch (19.3) | Requiring sign-in (loses the handoff, the very metric 19.3 uses to decide on native); a full session from the link (a forwarded feed link would then open Controls) |
| D8 | **Web push with VAPID from `api`**; one subscription row per browser context; the service worker renders only `kind: drop` and `kind: gap_note` payloads and drops anything else; title and length only [DECISION; PRD-v2 3.3, 3.10] | Three message kinds is a hard rule; enforcing it in the sender and in the renderer means a bug in one cannot leak a fourth kind | Firebase Cloud Messaging (another processor, no gain on the web); local notifications (not available to PWAs on iOS) |
| D9 | **Auth: email one-time code, Sign in with Apple, Google, implemented in `api` (Authlib plus our own OTP) with HttpOnly cookie sessions on `.forone.app`; onboarding runs on an anonymous `pre_account` session that the sign-in at A9 claims** [DECISION, confirms topology D12; PRD-v2 1.4, 2.2 A9] | Account only after the first call means the learner has state before an identity; claiming a pre-account row is a one-row update | Clerk/Auth0 (PII in a US processor); passwords (PRD 1.4 chose codes) |
| D10 | **Install handoff on iOS through a per-learner `start_url`**: the web manifest is served dynamically with `start_url=/today?h={handoffToken}` (single use, 7 days) so the home-screen app opens signed in [DECISION; PRD-v2 2.2 A10] | Safari and a home-screen web app have separate cookie jars on iOS; without this the first thing the installed app shows is a sign-in screen, right after A10 asked for the install | Asking the learner to sign in again (one email code; the single-engineer cut) |
| D11 | **API: REST JSON under `/v1`, OpenAPI generated by FastAPI, `openapi-typescript` plus `openapi-fetch` client; every response carries `X-Forone-LM-Version` (the topology's `learnerModelVersion`, one integer); events go in batches to `POST /v1/events` with client-minted UUIDv7 ids** [DECISION, confirms topology 3.5; PRD-v2 8.2] | Python backend rules out tRPC; GraphQL buys nothing for one client and thirteen screens; OpenAPI codegen gives typed calls for free | GraphQL; tRPC; ad-hoc fetch |
| D12 | **Realtime: Server-Sent Events at `GET /v1/stream`** for the foreground app (episode ready, notes ready, chat message, streaming manifest updates, voice-note replies), with ETag polling of `GET /v1/today` every 30 s as the fallback; nothing realtime is required for correctness [DECISION; PRD-v2 3.3, 5.5, 5.6] | One-directional, works through the ALB with a 20 s heartbeat, native `EventSource` in every target browser, nothing to host | WebSockets (bidirectional not needed outside the call, where LiveKit's data channel already exists); Pusher/Ably (another processor) |
| D13 | **State: TanStack Query for server documents, one Zustand store each for the player and the call, IndexedDB (`idb`) for the event queue and per-episode memory; the URL is the navigation state; no global store of learner facts** [DECISION] | Server documents are the truth; the two things with real local state (audio, call) get explicit state machines | Redux; React context trees; a client-side copy of the learner model |
| D14 | **Bidi at the technical level**: `<html dir="rtl" lang="ar">`, logical CSS properties only, `dir="auto"` plus `unicode-bidi: plaintext` on every content block, `<bdi>` for inline English inside Arabic, LTR for the transcript, article, captions and the scrub bar; Western digits; IBM Plex Sans Arabic with IBM Plex Sans as the Latin companion, self-hosted through `next/font` [DECISION; PRD-v2 1.4, 5.6, 12.1] | Mixed-direction text is the single most common visual bug in Arabic apps; fixing it in one layout layer and one lint rule is cheaper than fixing it per screen | Per-screen direction handling; Google Fonts at runtime (a third-party request per page) |
| D15 | **Analytics is the event log.** No third-party analytics SDK, no fingerprinting, no session replay; Sentry for errors with PII scrubbing; four client-only event types (`app_open`, `pwa_install`, `client_perf`, `push_permission`) added to the log so 16.2's "unprompted return" and the latency budgets are measurable [DECISION; PRD-v2 16.2, trust promise 6] | The product's own log already records everything pedagogically meaningful; any third-party SDK would be a processor under PDPL with no benefit | GA4, Mixpanel, PostHog |
| D16 | **Sample page: text or voice answers, `POST /v1/sample` returns `202 {sample_id}`, the page polls `GET /v1/sample/{id}` each second and plays from scene 1; a share page at `forone.app/s/{sampleId}` with Open Graph tags for WhatsApp; limits by first-party device cookie and contact hash in `api`** [DECISION; PRD-v2 2.1] | The 30 s budget is the pipeline's; the page only has to start on the first scene; sharing is the learner's choice through the native share sheet | Auto-sharing; email capture before play |

Fixed team cuts (one engineer instead of two) are listed in section 7; the design degrades to them without rework.

---

## 2. Requirements this domain implements

| PRD-v2 part | Requirement | Where it lands here |
|---|---|---|
| 1.4 | Installable web app in mobile Safari and Chrome; Arabic RTL interface, English LTR content, every block sets its own direction; Screen Wake Lock on calls; 18+ checkbox and birth date; Apple, Google, email code; account after the first call; three message kinds; web checkout (Mada, Apple Pay, cards) | D1, D2, D9, D10, D14, 4.1, 4.9, 4.11, 4.16 |
| 2.1 | Landing page, three questions text or voice, sample playable in 30 s, kept and forwardable, limits per device and contact per 24 h, waitlist form, invites carrying answers | 4.13, D16 |
| 2.2 A1 to A10 | First sound under 60 s; mic permission only at Talk; fact cards with ✎ and ✕; word check; casting while the pilot renders, including the name pronunciation check; pilot with transcript; first call; first note; account, drop time, voice-storage consent; three ideas; install card and feed setup | 4.2 (screens), 4.9, 4.10 |
| 2.4, 10.9.2 | The first then-and-now recording offered after session 2 (retell, opinion, 8 repeat sentences, about 3 min, skippable) [P0] | 4.2 (`/recording`), 4.10.2 |
| 3.3, 3.4 | Drop: feed item plus one push at drop time; Today screen states; three tabs | 4.3, 4.6, 4.8 |
| 3.6 to 3.8 | Allowance reflected not enforced; swap; small door; gap note send; return trigger | 4.3, D6, 4.8 |
| 3.10 | Exactly three message kinds | D8, 4.8 |
| 4 | Doors in any order; positions persist indefinitely; one open session; the throw's three choices; planning card when Read is skipped | 4.3 (`TodayDoc`), 4.4.2, 4.12 (`EpisodeMemory`) |
| 5.1 | The player: ⟲ line, Huh?, speeds, transcript folded by estimate, tap a word, Media Session mapping, feed version with Salma's tag and links in the notes | 4.4, 4.5, 4.7 |
| 5.3 | Article: tappable words, long-press a sentence, read-aloud synced | 4.4.6 |
| 5.4.1, 5.4.8, 5.4.10 | Call entry from throw, Today and feed link; captions; voice-note fallback screen | 4.2, D7 (the audio contract itself is the live-call domain's 4.11 and 4.12) |
| 5.5, 5.6 | Notes cards with ▶ and "say it once"; chat thread per host with margin notes; `dir` per bubble | 4.2, 4.3 (`NotesDoc`, `ChatDoc`) |
| 5.7 | Word sheet under 300 ms with audio and Keep | D4, 4.5 |
| 7.9 | Crisis resources card from the package, shown by the call screen, the chat, or once on the next open | 4.2, 4.3 (`TodayDoc.crisis_resources`), 4.8 |
| 12.1 to 12.4 | Three tabs; archive; notebook sections; Controls sheet | 4.2, 4.3 |
| 12.5, 12.6 | Export link with a passphrase shown once, delete in two taps, feed token reset, no cross-learner paths from the client | 4.9, 4.7, 4.3 |
| 15 | First sound under 60 s, sample under 30 s, dropped episode start under 2 s, word sheet under 300 ms, on-demand under 30 s streamed | section 6 |
| 16.2 | Time to first sound and first sentence; unprompted return; feed-to-call handoff; calls abandoned on the move | 4.14 (`app_open`, `client_perf`) |

Laws that bind the client directly: law 1 (no component for a bar, ring, percentage, level, streak or chart exists in `apps/web`; a lint rule forbids the words in component names and the CSS classes for progress fills; the only numbers rendered are `notebook_counts` and the notes header "6:12 call · you spoke 3:40"); law 7 (no correction surface on the call screen; captions show the host only); law 8 (no "next episode" control anywhere; the `ended` state of the player has no play-next); law 11 (no autoplay of anything after the throw; the Media Session play handler is a no-op in the `thrown` state); law 12 (the client renders claims it is given and sends `claim_shown`; it computes nothing about progress). Trust promise 5 (see, export, delete from Controls) and promise 8 (data use off by default; the switch is a Controls item, not an onboarding step). Sound design (12.1): the client ships no UI sounds of its own; the sting is inside the episode file and the only non-episode sound is the live-call domain's 100 ms connect sting. Budgets: the client's share of hosting is inside the $0.03 "proof share and hosting" line (section 6).

**From Milestone 0 to code.** The kit's hand-made delivery maps onto this domain one to one, which is what lets the team move from WhatsApp to the app without changing the product:

| Milestone 0 (04-production.md) | Beta (this document) |
|---|---|
| Episode MP3 sent on WhatsApp at the slot; WhatsApp plays with the phone locked | `feed.publish` plus one push at the drop time (3.4 flow A); the feed is the lock-screen channel, the PWA the screen channel |
| Article as a WhatsApp message | `/show/[episodeId]?door=read` with tappable words and read-aloud |
| ElevenLabs Agents share link opened from the drop message | `/call/{episodeId}?k=` from the feed notes, or the throw screen in the app (D7) |
| ❤️ 👍 😐 reaction as the listening record and the rating | `play` completion is the listening record; `followed_answer` is the one-tap rating on some episodes (PRD 16.2) |
| Salma's notes as an evening WhatsApp message, three cards and the three ideas | `NotesDoc` rendered at `/notes/[sessionId]` within 90 s of the call; the ideas at the chat closer or on Today |
| "Write to the show" question answered on WhatsApp | `/chat/[host]` |
| Gap note sent by hand once | `push.gap_note` and `email.send(kind: gap_note)` (4.8) |
| Then-and-now task sent as a WhatsApp voice note | `/recording/[recordingId]` (4.10.2) |

---

## 3. Architecture

### 3.1 Components

| Component | Runs | Owns | Talks to |
|---|---|---|---|
| `web` (Next.js) | Vercel, region `dxb1` for the few server functions; static assets at the edge | Public pages (SSR); the PWA shell; the player; the call screen; the service worker; the manifest route | `api` over HTTPS JSON with cookies; LiveKit Cloud over WebRTC (call screen only, live-call domain) |
| `sw.js` (Serwist) | In the learner's browser, scope `/` on `app.forone.app` only (`forone.app` registers no service worker) | Precache of the shell; runtime cache `forone-media-v1` (episode bytes, timings, glosses, package); push rendering; `notificationclick`; background replay of the event queue where Background Sync exists | `api` (same requests the page makes) |
| `forone.api.feed` (module in `api`) | Fargate `api` | `GET /f/{token}.xml`, `GET /f/{token}/{episodeId}.mp3`, `GET /f/{token}/cover.png`, `feed.publish(lid, episode_id)` called by `day/next` and `proof/make`, `links.mint()` for `notes_html`, `feed_fetches` logging, token reset | Postgres (`feed_tokens`, `feed_items`, `feed_links`, `feed_fetches`), S3 (`episode_feed.mp3` with SSE-C) |
| `forone.api.push` | Fargate `api` | `POST /v1/push/subscribe`, `DELETE /v1/push/subscribe`, `push.drop_notification(lid, episode_id)`, `push.gap_note(lid)`; VAPID keys; subscription expiry | Push services (Apple, Google, Mozilla) over Web Push |
| `forone.api.auth` | Fargate `api` | OTP, Apple, Google; `pre_account` sessions; claim at A9; handoff tokens; feed-link limited sessions; the session cookie | Resend (code emails), Apple and Google OIDC |
| `forone.api.stream` | Fargate `api` | `GET /v1/stream` SSE per learner; fan-in from Postgres `LISTEN/NOTIFY` on `forone_learner_{lid}` | Postgres |
| `forone.api.sample` | Fargate `api` | `POST /v1/sample`, `GET /v1/sample/{id}`, `POST /v1/waitlist`, share page data, limits | Inngest (`sample.requested`), S3 (`samples/`) |

Everything else the client calls (`/v1/today`, `/v1/events`, `/v1/calls`, `/v1/episodes`, notebook, controls, billing, recordings) is routed in `api` to the owning domain's modules; this document defines the contract (4.3) and not their internals.

### 3.2 Diagram, in text

Draw five boxes left to right. Leftmost, **Learner's phone**, containing three stacked boxes: **Safari or Chrome tab** (where the invite link and feed links land), **Installed PWA** (home-screen icon; its own cookie jar on iOS), and **Podcast app** (Apple Podcasts or another). Inside both browser boxes draw a small **sw.js** box with a cylinder labelled `forone-media-v1` and a cylinder labelled `IndexedDB: event queue, episode memory`; draw a small `<audio>` box in the page with an arrow from the `forone-media-v1` cylinder labelled "Blob URL" and an arrow from `api` labelled "network URL (streaming)". Second box, **Vercel edge** (`forone.app`, `app.forone.app`): static shell, SSR for public pages, the dynamic `manifest.webmanifest` route. Third box, **api (Fargate, me-central-1)** with the six modules of 3.1 as compartments and a `LISTEN/NOTIFY` tap into the fourth box, **Postgres** (`feed_tokens`, `feed_items`, `feed_links`, `feed_fetches`, `push_subscriptions`, `auth_sessions`, `accounts`, `otp_codes`, `handoff_tokens`, `waitlist`, `invites`, `learner_stream_log` next to the topology's `learners`, `sessions`, `doors`, `episodes`, `media_objects`). Fifth box, **S3 forone-media** (SSE-C per learner). Arrows: browser → Vercel (HTTPS, the shell); browser → api (`/v1`, cookies, CORS with credentials; `/f/...` without cookies); podcast app → api `/f/{token}.xml` then `/f/{token}/{episodeId}.mp3` (Range); api → S3 (Range passthrough); push services → browser (one arrow labelled "drop, gap note; nothing else"); Resend → learner's mailbox (labelled "codes, receipts, trial ending, export, deletion, gap note"); a dotted arrow from **workflows** (`day/next`, `proof/make`, off to the side) into `api.feed.publish` and `api.push.drop_notification`. A dashed arrow from the podcast app box to the Safari box labelled "call link (`?k=`)" shows the feed-to-call handoff; a dashed arrow from Safari to the Installed PWA labelled "`start_url?h=`" shows the install handoff.

### 3.3 Interfaces

| From | To | Protocol | Contract |
|---|---|---|---|
| `web` | `api` | HTTPS JSON `/v1`, cookie `forone_s` on `.forone.app`, header `X-Forone-Client: web/{build}` on every request, `credentials: include` | OpenAPI 3.1 document at `/v1/openapi.json`, TypeScript client generated in CI; responses carry `X-Forone-LM-Version` (the data domain's `lm_version` integer, the topology's `learnerModelVersion`) and `ETag` where cacheable |
| `web` | `api` media | `GET /v1/episodes/{id}/media/{asset}` with `Range`; `crossorigin="use-credentials"` on audio elements that stream | `asset` is one of `episode.m4a`, `scene-{scene_id}.m4a`, `article.m4a`, `recap.m4a`, `timings.json`, `glosses.json`, `package.json` (the names in the pipeline's `AudioManifest`; `api` maps each to its `media_objects` row); 206 with `Accept-Ranges: bytes`, `Content-Length`, `Cache-Control: private, max-age=31536000, immutable` (an asset's bytes never change under the same episode id and manifest version; a republished manifest changes the version and the client re-adds) |
| `web` | `api` clips | `GET /v1/media/{media_object_id}` with `Range` | Notes clips, marks, proof clips, kept call recordings; same headers |
| `web` | `api` SSE | `GET /v1/stream` (`text/event-stream`) | Events in 4.8; heartbeat comment every 20 s; `Last-Event-ID` resumes from the per-learner notify sequence |
| `sw.js` | push services | Web Push, VAPID, `TTL: 7200` for drops, `Urgency: normal` | Payload in 4.8; encrypted per subscription |
| `day/next`, `proof/make` | `api.feed`, `api.push` | In-process Python calls through `forone.core` (the topology's `feed.publish`, `push.drop_notification`) | Idempotent on `(learner_id, episode_id)` |
| Podcast app | `api` | `GET /f/{token}.xml`, `GET /f/{token}/{episodeId}.mp3`, `GET /f/{token}/cover.png`, no cookies, `If-None-Match` and `HEAD` honoured | 4.7 |
| Public pages | `api` | `POST /v1/sample`, `GET /v1/sample/{id}`, `POST /v1/waitlist`, `GET /v1/share/{sampleId}`, `POST /v1/telemetry` | 4.13 |

CORS on `api`: `Access-Control-Allow-Origin` echoes exactly `https://app.forone.app` or `https://forone.app` (and the Vercel preview origin on staging), `Allow-Credentials: true`, allowed headers `Content-Type, X-Forone-Client, X-Forone-Replay, If-None-Match, Range`. Mutating requests without `X-Forone-Client` are refused (CSRF belt alongside the `SameSite=Lax` braces). Media element requests from `app.forone.app` to `api.forone.app` are same-site under `forone.app`, so the `SameSite=Lax` cookie is sent with them.

### 3.4 Data flows

**A. A normal morning (dropped episode).** 07:40 `day/next` calls `feed.publish` (sets `feed_items.published_at`, bumps the feed ETag) then `push.drop_notification` (one payload to every live subscription of the learner). The phone shows "Karim vs Mona: the interview (6 min)". Tap → `notificationclick` → `clients.openWindow('/today?entry=push')` → the PWA loads the shell from precache, reads the cached `TodayDoc` (stale-while-revalidate) and finds `episode.m4a` already in `forone-media-v1` from the previous evening's `today.changed` (the pipeline publishes to the app the moment the episode is ready; the drop time only controls feed and push). The page builds a Blob URL from the cached response and `play()` starts from local bytes in under 2 s; `play` events batch every 2 s to `POST /v1/events`; the half-episode mark makes the day active server-side.

**B. The same morning on the feed.** The podcast app polled `/f/{token}.xml` at some point after 07:40, saw the new `<item>` (its `<guid>` is the episode id), downloaded `/f/{token}/{id}.mp3`. `api` logged a `feed_fetches` row and nothing else. The learner listens on the bus with the phone locked. The episode ends with Salma's 5 s tag; the notes show two links. Tapping the call link opens Safari at `/call/{episodeId}?k=...`; `web` posts `k` to `POST /v1/links/exchange`, receives a limited session cookie, logs `app_open {entry: "feed_link"}` with `feed_to_call_ms` started at link open, shows the planning card if Read is not done, and starts the call (live-call domain). After the call the notes and chat work in this Safari context too; Controls shows "sign in to change settings".

**C. First open.** Invite link `/i/{code}` → `GET /v1/invites/{code}` returns the waitlist answers → A1 (static) → A2 Talk → `POST /v1/onboarding/start {invite_code, tz}` creates the `pre_account` learner, sets the `forone_s` cookie with `scope: pre_account`, returns `{learner_id, call: {room, token}}` → the Salma call (live-call domain) → A4 to A8 → A9 `POST /v1/auth/{otp|apple|google}` claims the learner (`learners.status = trial`, `trial_started_at`), `PUT /v1/me {birth_date}` (under 18 → 403 with the plain message and the pre-account row deleted) → A10 ideas, then the install card: the page sets `<link rel="manifest" href="/manifest.webmanifest">` whose route mints a `handoff_tokens` row and returns `start_url: "/today?h={token}"`; the "copy feed link" button calls `GET /v1/feed/url`.

**D. Offline.** The SW serves the shell; today's episode plays from Cache Storage through a Blob URL; `TodayDoc` comes from the HTTP cache (stale) with an offline banner; doors that need the network (call, chat, swap) show one plain line; events queue in IndexedDB (`forone-queue`) with their original `occurred_at`; on reconnect the page (or Background Sync on Chrome) replays them with `X-Forone-Replay: 1`; the server honours the original timestamps (data domain 4.1.4).

---

## 4. Detailed design

### 4.1 Repository layout and build

Inside the topology's monorepo (`apps/web`):

```
apps/web/
  app/                      # Next.js App Router
    (public)/               # forone.app: page.tsx (landing), s/[sampleId]/page.tsx (share), i/[code]/page.tsx (invite), legal/*
    (app)/                  # app.forone.app, client components, no SSR of learner data
      today/  show/  show/[episodeId]/  notebook/  notebook/[section]/  controls/
      onboarding/[step]/    # a1 .. a10
      call/[episodeId]/     # the call screen (live-call domain's 4.11, 4.12 implemented here)
      chat/[host]/  notes/[sessionId]/  proof/[proofId]/  recording/[recordingId]/
    manifest.webmanifest/route.ts        # dynamic manifest (D10)
    sw.ts                                # Serwist source
  public/.well-known/apple-developer-merchantid-domain-association   # Apple Pay on the web (the processor's file; 4.16)
  components/  player/  call/  text/     # text/: Bidi, Transcript, WordSheet
  lib/api/ (generated client)  lib/events/ (queue)  lib/media/ (cache, blob urls, clip player)  lib/state/ (zustand stores)
  middleware.ts                          # host routing, auth redirect for (app)
  eslint-law-rules/                      # law 1 lint rule, logical-property rule
```

Build: `next build`; CI runs `tsc`, ESLint (including the law rule), Playwright on iOS Safari and Android Chrome via BrowserStack for the player and RTL snapshots (week 3 onward), and `openapi-typescript` against the staging `api`'s `/v1/openapi.json` (a drift fails the build). Deploy: Vercel Git integration, preview per PR against staging `api`, production on tag. The installed PWA may run yesterday's build for a day, so `api` keeps one release of backward compatibility (topology 4.8); the SW uses `skipWaiting` and `clients.claim` and the page reloads on the next navigation, never mid-playback or mid-call.

`middleware.ts` routes by host: `forone.app` → `(public)`; `app.forone.app` → `(app)`; an `(app)` route without a `forone_s` cookie redirects to `/onboarding/a1` except `/call/[id]?k=` and `/today?h=`, which exchange their token first.

### 4.2 Screens and routes

The learner screens map to routes; each names its data document (4.3) and the events it emits (data domain 4.1.1).

| Route | Screen (PRD-v2) | Reads | Emits |
|---|---|---|---|
| `/onboarding/a1` .. `/a10` | 2.2 A1 to A10 | `InviteDoc`, `OnboardingDoc` (casting pools, name candidates, word-check items, ideas) | `onboarding_answer`, `word_check_answer`, `fact_card_edit`, `consent_change`, `idea_chosen`, `pwa_install`, `push_permission`, `app_open` |
| `/today` | 3.4 Today, all six states; day-7 payment card; trial-ended state; the once-only crisis resources card (7.9 rule 3) | `TodayDoc` | `app_open`, `swap`, `small_door`, `idea_chosen`, `followed_answer` |
| `/show`, `/show/[episodeId]` | 12.2 archive shelf; episode page with transcript, article, call recording or transcript, notes, chat | `ShelfDoc`, `EpisodeDoc` | `play`, `pause`, `seek`, `speed`, `replay_line`, `huh`, `transcript_toggle`, `tap`, `keep`, `mark` |
| `/today` player sheet | 5.1 player, 5.2 shadow [P1], 5.3 article | `EpisodeDoc` + `AudioManifest` + `WordIndex` | as above plus `article_scroll`, `read_aloud`, `shadow` |
| `/call/[episodeId]` | 5.4 call screen, planning card, voice-note fallback, crisis card (`ui.crisis`) | `CallBundle` summary from `POST /v1/calls` | `call_started`, `replay_line{door:call}` (the worker emits the rest) |
| `/notes/[sessionId]` | 5.5 up to three cards, header line, "say it once", first-time notes preference; the offer of the first then-and-now recording after session 2 | `NotesDoc` | `note_shown`, `say_it_once`, `claim_shown`, `consent_change{kind:notes_mode}` |
| `/recording/[recordingId]` | 10.9.2 the then-and-now recording: retell, opinion, 8 repeat sentences, skippable | `RecordingDoc` | `recording` (one per part) |
| `/chat/[host]` | 5.6 thread, date separators named after episodes, margin note chip, tomorrow's ideas after the closer, crisis resources inline when the host steps out | `ChatDoc` | `chat_message{speaker:learner}`, `margin_note{opened}`, `idea_chosen` |
| `/notebook`, `/notebook/[section]` | 12.3 sections | `NotebookDoc` per section | `fact_card_edit`, `fact_card_viewed`, `notebook_edit`, `working_on_edit`, `wrong_memory_flag`, `claim_shown` |
| `/controls` | 12.4 | `ControlsDoc` | `consent_change`, plus `POST /v1/feed/reset`, `POST /v1/me/export`, `DELETE /v1/me` |
| `/proof/[proofId]` | 11.1 proof above Today, "how we know", worth-it question | `ProofDoc` (`proofId` is the `episodes.id` of the `kind: proof` episode the assessment domain publishes) | `play{media_kind:proof}`, `claim_shown`, `worth_it_answer`, `working_on_edit` |
| `forone.app/` and `/s/[sampleId]` | 2.1 landing, sample, waitlist, share | public | none (no learner) |

Design tokens: one show colour per learner (chosen in `web` from the learner id, stored in `TodayDoc.show.color` so the feed artwork matches), typographic covers rendered as SVG components and rasterized to PNG on a canvas for Media Session artwork and for the share page's OG image (public route, 1200×630). Dark mode follows `prefers-color-scheme` with a Controls override. No images of people, no mascot.

### 4.3 The API contract

Base URL `https://api.forone.app/v1`. Cookie `forone_s` (HttpOnly, Secure, `SameSite=Lax`, `Domain=.forone.app`, `Path=/`, `Max-Age` 90 days rolling, value = opaque 32-byte id of an `auth_sessions` row). Errors are `{error: {code, message_ar, message_en}}` with the code from a fixed list; the client shows `message_ar` and nothing else.

| Method and path | Purpose | Body → Response |
|---|---|---|
| `POST /onboarding/start` | A2 Talk or Type; creates `pre_account` learner | `{invite_code?, tz, mode: "talk"|"type"}` → `{learner_id, call: {room_url, token, call_id}}` (the live-call domain's Salma call) |
| `GET /onboarding` | A4, A5, A10 data | → `OnboardingDoc {word_check: {items[]}, casting: {hosts: {karim: {voices[], hello_clips[]}, mona: ...}, accents}, name: {candidates: [{index, clip_url}], chosen, verified}, pilot: {episode_id|null, state}, ideas[]}` |
| `PUT /onboarding/casting` | A5 choice | `{karim_voice_id, mona_voice_id, accent}` → 204 |
| `PUT /onboarding/name` | A5 "say it differently" (pipeline 4.8) | `{candidate_index}` → 204; cycles the three respelling candidates the voice studio rendered |
| `POST /auth/otp/request` | email code | `{email}` → 202 (always; no account enumeration) |
| `POST /auth/otp/verify` | claim or sign in | `{email, code}` → `{learner_id, status}`; sets cookie; claims the current `pre_account` learner if the cookie scope is `pre_account` |
| `GET /auth/apple/start`, `POST /auth/apple/callback` | Sign in with Apple (`response_mode=form_post`) | state carries the pre-account session id |
| `GET /auth/google/start`, `GET /auth/google/callback` | Google OIDC | same |
| `POST /auth/signout` | | → 204; deletes the `auth_sessions` row |
| `POST /handoff/mint`, `POST /handoff/exchange` | D10 install handoff | mint → `{h}` (called by the manifest route with the forwarded cookie); exchange `{h}` → sets cookie; single use |
| `POST /links/exchange` | D7 feed link | `{k, episode_id}` → sets a cookie with `scope: feed_link, episode_id`; `{learner_id, scope}` |
| `PUT /me` | A9 | `{birth_date, drop_time_local, backup_time_local?, anchor_text, display_name?}` → 204 or `403 under_18` |
| `GET /today` | the Today screen | → `TodayDoc` (below); `ETag` |
| `GET /stream` | SSE | 4.8 |
| `POST /events` | event batches | `{events: EventIn[]}` → `{accepted, duplicates, rejected[]}`; max 50 per batch; `X-Forone-Replay: 1` for queue replays |
| `GET /episodes/{id}` | episode page | → `EpisodeDoc` |
| `GET /episodes/{id}/media/{asset}` | audio and json | Range; asset names in 3.3 |
| `GET /media/{media_object_id}` | clips (notes, marks, proof, kept recordings) | Range |
| `GET /episodes/{id}/why` | 9.9 | → the pipeline's `why` artifact |
| `POST /sessions/{id}/swap` | 3.6 one swap | → `{episode_id}` (202, then `episode.manifest` on the stream) or `409 swap_used` |
| `POST /sessions/{id}/doors/{door}` | door state and position | `{state, position}` → 204 (also implied by events; this is the explicit resume point) |
| `POST /calls` | start a call | `{session_id, kind}` → `{call_id, room_url, token, planning_words[], brief_summary}` (live-call domain) |
| `POST /calls/{id}/voicenotes`, `POST /calls/{id}/talkback` | fallback | live-call domain 5.1: `{media, duration_ms}` (at most 90 s), `{text_ar}` |
| `POST /sessions/{id}/small-door` | 3.7 | multipart `{media, duration_ms, recap_played_ms}` → `202 {media_object_id}`; the host reply arrives as `chat.message` on the stream |
| `GET /sessions/{id}/notes` | 5.5 | → `NotesDoc` |
| `POST /recordings` | then-and-now parts, say it once, shadow | multipart `{media, task: "retell"|"opinion"|"repeat"|"say_it_once"|"shadow", recording_id?, part_index?, reference_text?, kept_explicitly?}` → `202 {media_object_id}` |
| `GET /recordings/{id}` | the recording task | → `RecordingDoc {recording_id, season, parts: [{task, prompt_ar, reference_audio_url|null, reference_text|null, max_s}], offered_reason}` |
| `GET /chat/{host}?before=` | 5.6 | → `ChatDoc` page |
| `POST /chat/{host}/messages` | learner message | `{text, client_event_id}` → `{message_index}`; the host reply arrives on the stream |
| `GET /ideas`, `POST /ideas/choose` | 3.1 | `{idea_id|null, source, remix?: {topic?, format?, cast?}, salma_text?}` → `{picked: Idea}` |
| `GET /shelf` | 12.2 | → `ShelfDoc {seasons[]: {season, title_ar, episodes[]: EpisodeCard}}` |
| `GET /notebook/{section}` | 12.3 | → section documents from the data domain's views (4.3.9 there) |
| `PUT /notebook/facts/{id}`, `DELETE /notebook/facts/{id}`, `POST /notebook/working-on`, `DELETE /notebook/working-on/{id}`, `POST /notebook/out-in-world` | learner edits (synchronous in the data domain) | each also appends the matching event; the response carries the new `X-Forone-LM-Version` |
| `GET /controls`, `PUT /controls` | 12.4 | `{drop_time_local?, drop_notification?, captions?, transcript_default?, default_speed?, notes_mode?, voice_storage?, data_use?, gap_note?, text_size?}` → `ControlsDoc` |
| `GET /feed/url`, `POST /feed/reset` | 12.4 | → `{url}` |
| `POST /push/subscribe`, `DELETE /push/subscribe` | D8 | `{subscription: PushSubscriptionJSON, ua_hint}` → 204 |
| `POST /me/export`, `GET /me/exports` | 12.5 | export → `202 {export_id, passphrase}` (the data domain's zip passphrase, shown once with a copy button and the sentence that it is never emailed); `GET` → `[{export_id, state, ready_at, url_expires_at}]` |
| `DELETE /me` | 12.5 | → 202 then `410` on every later request |
| `POST /billing/checkout`, `GET /billing`, `POST /billing/portal` | 1.4 | `{plan}` → `{checkout_url}`; the processor's hosted page; OPEN processor |
| `POST /sample`, `GET /sample/{id}`, `POST /waitlist`, `GET /share/{sampleId}`, `GET /invites/{code}`, `POST /telemetry` | 2.1 | 4.13 |

`TodayDoc`, the one document the home screen renders:

```ts
type TodayDoc = {
  lm_version: number;
  learner: { display_name: string; status: "pre_account"|"trial"|"paid"|"trial_ended"; trial_day: number|null; tz: string };
  show: { color: string; hosts: { karim: {display_name: string}; mona: {display_name: string} }; season: { number: number; title_ar: string|null; day: number } };
  host_line: { who: "karim"|"mona"; text: string; canon_id: string } | null;     // always a confirmed memory (PRD 3.4)
  hero: {
    state: "ready"|"in_progress"|"notes_waiting"|"done"|"none";                   // "none" only before the pilot exists
    episode: EpisodeCard | null;                                                   // {episode_id, kind, title, length_s, cast, includes: ["call","article","chat"], cover, manifest_version}
    doors: { listen: DoorState; read: DoorState; call: DoorState; chat: DoorState; small_door: DoorState; round_two: DoorState|null; shadow: DoorState|null };
    notes: { state: "none"|"writing"|"ready"; count: number; session_id: string|null };
    swap_available: boolean;                                                       // false after the one swap or once started
    streaming: boolean;                                                            // true while an on-demand episode is still rendering
  };
  proof: { proof_id: string; title: string; length_s: number; cover: Cover } | null;   // above the hero on proof day
  tomorrow: { drop_at: string; teaser: string|null; picked: boolean } | null;            // in "done"
  ideas_due: boolean;                                                                   // show the three ideas on Today after the session is done
  round_two_offer: { call_kind: "round_two"; host: "karim"|"mona" } | null;               // [P1]
  recording_offer: { recording_id: string; text_ar: string } | null;                     // the first "then" after session 2, again once in sessions 3 to 5 (PRD 2.4, 10.9.2)
  payment: { ask_now: boolean; plans: Plan[] } | null;                                   // day 7 only, once
  crisis_resources: { show_once: boolean; resources_ref: string } | null;                // PRD 7.9 rule 3; the client renders the package's card and acknowledges with GET /v1/today?ack=crisis
};
type DoorState = { state: "not_started"|"in_progress"|"done"|"skipped"; position: { ms?: number; depth?: number; cursor?: number } | null };
```

The hero never carries a count of unplayed episodes (there is only ever one) and the doors are four words with ticks, not a bar. `payment.ask_now` is true on `trial_day == 7` until answered; the card is Salma's one plain sentence and the plans; it is not a wall and Today keeps working behind it until the trial ends.

`NotesDoc` (what the assessment domain's stage 1 produces and the client renders; the client adds nothing):

```ts
type NotesDoc = { session_id: string; header: { call_s: number; spoke_s: number }; cards: NoteCard[]; ask_notes_mode: boolean; signature_ar: string };
type NoteCard =
  | { kind: "new_for_you"; card_id: string; claim_id: string; text_ar: string; quote_en: string; clip: ClipRef|null }
  | { kind: "polish"; card_id: string; learner_sentence: string; learner_clip: ClipRef|null; natural_sentence: string; natural_clip: ClipRef; reference_text: string }
  | { kind: "reached_for"; card_id: string; paraphrase_en: string; word_en: string; gloss_ar: string; example_en: string; clip: ClipRef|null };
type ClipRef = { media_object_id: string; start_ms: number; end_ms: number };   // played through GET /v1/media/{media_object_id} with Range
```

`EventIn` (data domain 4.1): `{event_id (UUIDv7), session_id?, episode_id?, call_id?, door, type, occurred_at, payload}`; `learner_id` comes from the cookie, never the body. The client mints UUIDv7 with a 48-bit millisecond prefix from `Date.now()` plus 74 random bits; the queue stores the batch exactly as sent so a replay sends identical ids.

### 4.4 The player

**4.4.1 Inputs.** `EpisodeDoc` (title, cast, kind, state, `player_defaults: {transcript_open: boolean, speed: 0.75|0.85|1.0, speech_rate}`, `media: {app, scenes[], article, recap, timings, glosses, package}` as asset names, `targets` and `new_words` lemma lists for Huh? glossing, `ask_followed`), the pipeline's `AudioManifest` (`timings.json`: `lines[]` with `sentences[]` and `words[]`, `segments[]` with `seam` and `stream_url`, `pause_no_capture`, `timing_quality: "word"|"sentence"`, `article_words[]`, `shadow_lines[]`) and `WordIndex` (`glosses.json`). On load the client builds two flat, sorted arrays: `words: {s, e, line_id, i}[]` and `sentences: {s, e, sent_id, line_id, text}[]`, and a `Map<line_id, Map<i, gloss_ref>>` from the index. For a 900-word script this is under 5 ms.

**4.4.2 State machine** (`PlayerStore`, Zustand, one instance app-wide so Today, Show and the lock screen share it):

```
states: idle → loading → ready → playing ⇄ paused → ended → thrown
                                   playing --(huh)--> huh_replay --(sentence end)--> playing
                                   any --(switch episode)--> loading
context: { episode_id, source: "blob"|"network"|"scenes", scene_index, position_ms, speed, transcript_open,
           huh: {sent_id, restore_speed} | null, mark_pending: boolean, media_session_owner: "player"|"call" }
```

Transitions that matter for the laws: `ended` fires the `completion` event (`play` with `position_ms = duration`) and moves to `thrown` when the manifest's last line is the throw; in `thrown` the three choices (Call now, Read the article first, Later) are shown and the Media Session `play` action is a no-op (PRD 4 rule 2: pressing play on the headphones after the throw does nothing). There is no `next` state and no queue. "Later" simply closes the sheet; the Today doors show Call as `not_started`.

**4.4.3 Audio elements.** Three `HTMLAudioElement`s created once per app load and unlocked on the first user gesture (play then pause on a 100 ms silent data URI; iOS allows programmatic `play()` later only on elements that have been started by a gesture): `main` (the episode or article or recap), `clip` (word sheet, notes clips, marked moments, shadow lines) and `aux` (the second element of the scene handoff while streaming). `preservesPitch = true`. `playsinline`. `crossOrigin = "use-credentials"` when the source is a network URL.

**4.4.4 Source selection.** (1) If `forone-media-v1` holds the full `episode.m4a` for this manifest version: `main.src = URL.createObjectURL(await (await cache.match(url)).blob())` (`source: "blob"`; the Blob URL is kept for the episode's lifetime and revoked on `switch episode`; `clip` shares it). (2) Else if `manifest.timing_quality == "word"` and the app file exists on the server: `main.src` = the network URL (`source: "network"`), with `api`'s Range support for seeking, and the page starts `cache.add()` of the full file in the background so the next open is case 1. (3) Else (streaming): `main.src = scene-{s0}`, `aux.src = scene-{s1}` preloaded; on `main.ended` swap roles at the seam (the pipeline guarantees a sting or beat at every segment end); when `episode.manifest` arrives on the stream with the full file, the player switches to it at the next seam, seeking to the same absolute position (`segment.start_ms + position`). While streaming, `sentences[]` come from the manifest's sentence-level estimate and the transcript is folded regardless of the learner's default (pipeline 4.13 item 3).

**4.4.5 Sync loop.** `requestAnimationFrame` while playing (and a 250 ms `setInterval` when the tab is hidden, which iOS throttles but does not stop for playing audio): `t = main.currentTime * 1000 + scene_offset`; binary search `words` for the active word; if it changed, move the `data-active` attribute (one DOM write) and, when the active line changes, scroll the transcript so the current line sits at 40% of the viewport (`scrollIntoView({block: "center"})` only when the learner has not scrolled in the last 3 s). Word spans are rendered once; nothing re-renders per frame.

**4.4.6 Controls.**

| Control | Implementation | Event |
|---|---|---|
| Play, pause, scrub | native; scrub snaps to the nearest sentence start when within 400 ms of one | `play`, `pause`, `seek` |
| ⟲ line | target = the sentence containing `t`, or the previous one if `t` is within 400 ms of its start; `main.currentTime = target.s / 1000` | `replay_line {line_id, source: "button"|"media_session"}` |
| Huh? | target = the sentence before the one containing `t` (or the current one if more than 2 s in); seek to it, set `playbackRate = 0.85`, enter `huh_replay`, open the Huh sheet with the sentence and glosses for its hardest words; at `target.e` restore the learner's speed and close the sheet unless a word is being read | `huh {line_id, sentence_text, unit_ids[]}` |
| Hardest words for Huh? | words in the sentence that are `new_words` or `targets` first, then words whose index entry has `rank > 3000` (the pipeline ships `rank` per index entry, section 9), at most 4; if the index lacks `rank`, the 3 longest content words | (inside `huh`) |
| Speed | `main.playbackRate ∈ {0.75, 0.85, 1.0}`; the control has three positions and no other value is reachable; `aux` and `clip` follow | `speed` |
| Transcript | folded or open from `player_defaults.transcript_open`; `EpisodeMemory` remembers `opened_before` per episode and overrides to open on replays (PRD 5.1) | `transcript_toggle {open, on_first_play}` |
| Tap a word | 4.5 | `tap` |
| Read it to me (article) | `main.src = article.m4a` (Blob URL if cached); `article_words[]` from the manifest drive the same sync loop over the article's sentences | `read_aloud {on, position_ms}` |
| Long-press a sentence (article) | hear it (clip player at `[s, e]`) or keep it (`keep` with `unit_id = null, sentence_text`) | `keep` |
| Shadow [P1] | plays `shadow_lines[]` by `[line.start_ms, line.end_ms]`, records with `MediaRecorder` (20 s cap), uploads to `POST /v1/recordings {task: "shadow"}` | `shadow` |
| "How much did you follow?" | one tap on some episode ends (`EpisodeDoc.ask_followed`): most / about half / little | `followed_answer` |
| Seam stop | the scene list from `segments[]` lets the learner stop at a seam from the lock screen (`seekto` snaps to seams when the position is within 1.5 s) | `pause` |
| Small door | plays `recap.m4a` (90 s), then one `MediaRecorder` note up to 60 s uploaded as `POST /v1/sessions/{id}/small-door` multipart `{media, duration_ms, recap_played_ms}`; `api` writes the `media_objects` row and the `small_door` event and the host answers in the chat thread (PRD 3.7) | `small_door` |

**4.4.7 Media Session.** Set on `loading` when `media_session_owner == "player"`:

```ts
navigator.mediaSession.metadata = new MediaMetadata({
  title: ep.title, artist: `${hosts} · For one`, album: `Season ${season}`,
  artwork: [{ src: coverPngBlobUrl, sizes: "512x512", type: "image/png" }],
});
const h = navigator.mediaSession.setActionHandler;
h("play", () => state !== "thrown" && main.play());           // PRD 4 rule 2
h("pause", () => main.pause());
h("seekto", d => seekSnappingToSeams(d.seekTime));
h("previoustrack", () => replayLastSentence("media_session"));  // PRD 5.1
h("nexttrack", () => markMoment());                             // PRD 5.1
h("seekbackward", null); h("seekforward", null);                // not offered; no 10 s skip exists
setInterval(() => navigator.mediaSession.setPositionState({ duration, playbackRate, position }), 1000);
```

Only the standard actions are registered; the app never intercepts a system gesture (no listening for triple-click, no media key hijack). `markMoment()` appends `mark {episode_id, line_id, position_ms, sentence_text, clip_media_object_id: null}` and shows a 1 s toast; the notebook later plays a mark by Range on the episode file at the sentence's `[s, e]`, so no clip is cut or stored (section 9 records this for the data domain, whose schema allows a clip id). **Ownership handoff:** when `/call/[episodeId]` mounts it pauses `main`, sets `media_session_owner = "call"` and registers the live-call domain's handlers (its 4.11: play/pause toggles mute, previous track replays the host's last line, next track is a 5 s talkback); on unmount the player re-registers its own handlers. Two owners never hold the handlers at once.

**4.4.8 Background playback.** In the installed PWA on iOS 17 and 18 and in Chrome on Android, an `HTMLAudioElement` started by a gesture keeps playing with the screen locked and shows the Media Session controls; a Blob URL source behaves like a file. Known gaps, confirmed in the week-3 test matrix rather than assumed: iOS pauses on an incoming phone call and does not resume (the player restores position; nothing to do); iOS may suspend the page after about 30 minutes of locked-screen playback in a browser tab (not in the installed app); switching audio route (AirPods disconnect) pauses, which is correct. The feed is the commute channel of record; the PWA's background play is a convenience, and `client_perf {kind: "bg_play_stop"}` is logged when `pause` fires without a learner action so the week-3 rate is measured.

### 4.5 The word sheet

Tap on a word span → `index.script.get(line_id).get(i)` → `gloss_ref` → `index.glosses[gloss_ref]` → render `{meaning_ar, pos, register_note_ar, example_en}` plus the sentence the word came from (`sentences[]` by `sent_id`) → measure `word_sheet_open_ms` from `pointerup` to first paint (`PerformanceObserver` on the sheet's `element-timing`), logged in `client_perf` when it exceeds 300 ms. 🔊 → `clip.src = main.src` (the same Blob URL or network URL), `clip.currentTime = (w.s - 60) / 1000`, play, pause at `w.e + 60` ms (a `timeupdate` guard plus a `setTimeout` at the expected duration). Keep → `keep {unit_id, sense_key, sentence_text}` and an optimistic tick. The sheet is a bottom sheet that does not pause the main audio unless 🔊 is tapped (then `main` pauses for the clip and resumes).

Phrase selection: `pointerdown` on a word, `pointermove` across spans (with `touch-action: pan-y` so vertical scroll still works), `pointerup` → the span `[i, j]` within one line; if any index entry in the span carries a `chunk_id` whose extent equals `[i, j]`, show the chunk's gloss (`index.glosses[chunk gloss_ref]`); otherwise show the per-word glosses stacked in order and log one `tap` per word with `chunk: false`. A 350 ms long-press on a single word selects it for the drag (iOS otherwise opens the text-selection UI; the transcript has `user-select: none`).

Misses: when `index.missing[]` contains the lemma, the sheet shows the sentence at once and calls `GET /v1/gloss?lemma=&sense_key=` (the pipeline's `gloss-service.lookup`) with a 1.5 s timeout and a plain "no meaning yet" fallback; this is the only network path on tap and it is rare.

### 4.6 Service worker and caching

Serwist configuration (`sw.ts`):

```ts
const sw = new Serwist({
  precacheEntries: self.__SW_MANIFEST,              // the Next.js shell: html, js, css, fonts, icons, Salma's static Arabic clips used by onboarding UI
  skipWaiting: true, clientsClaim: true, navigationPreload: true,
  runtimeCaching: [
    { matcher: ({url}) => url.hostname === "api.forone.app" && /\/v1\/episodes\/[^/]+\/media\//.test(url.pathname),
      handler: new CacheFirst({ cacheName: "forone-media-v1",
        plugins: [ new RangeRequestsPlugin(),                                     // 206 from a cached 200, for the rare network-source case that hits the cache
                   new ExpirationPlugin({ maxEntries: 40, purgeOnQuotaError: true }),
                   new CacheableResponsePlugin({ statuses: [200] }) ] }) },      // never cache a 206 itself
    { matcher: ({url}) => url.pathname === "/v1/today" || url.pathname.startsWith("/v1/shelf"),
      handler: new StaleWhileRevalidate({ cacheName: "forone-docs-v1" }) },
    { matcher: ({request}) => request.destination === "font", handler: new CacheFirst({ cacheName: "forone-fonts-v1" }) },
  ],
  fallbacks: { entries: [{ url: "/offline", matcher: ({request}) => request.mode === "navigate" }] },
});
```

Rules the page enforces on top:

1. **Warm today's episode** when `TodayDoc.hero.state == "ready"` or on `today.changed {reason: episode_ready}`: the page (not the SW) runs `cache.add()` for `episode.m4a` (a full 200 fetch), `timings.json`, `glosses.json`, `package.json`, `article.m4a`, `recap.m4a` into `forone-media-v1`; on a metered connection (`navigator.connection.saveData`) only `timings.json`, `glosses.json` and `package.json` are warmed and the audio streams from the network. `web.sw.warm_assets` is the list; `web.sw.cache_episodes_n = 3` keeps today's and the last two; older entries are evicted by the plugin and the archive streams them on demand. Playback reads the cached entries through `caches.match()` and Blob URLs (4.4.4), so playback never depends on the SW's fetch handler being invoked for a media element, which Safari has historically done inconsistently.
2. **Never cache a partial response.** A 206 from `api` is passed through and not stored (the plugin would otherwise store a truncated body).
3. **Quota.** `navigator.storage.estimate()` on app start; under 100 MB free, `cache_episodes_n` drops to 1; `persist()` is requested once after install (granted automatically to installed PWAs on Chrome; iOS ignores it but exempts home-screen apps from the 7-day eviction).
4. **Versioning.** Cache names carry a version; a new SW deletes caches with other versions on `activate`. Media keys are immutable per `(episode_id, manifest_version)` so a cached episode survives SW upgrades within a version; a republished manifest (streaming → word timings) changes the key and the page re-adds.
5. **Push and notification click** (4.8) live in the same SW.
6. **Background Sync** (`forone-events`) on Chrome replays the event queue when the page is closed; Safari has no Background Sync, so the queue is replayed on the next open (the 24 h window matches the data domain's clock-skew rule for replays).

The event queue (`lib/events/queue.ts`): IndexedDB database `forone-queue`, store `batches` keyed by `batch_id`, each a JSON array of `EventIn`. `enqueue(event)` buffers in memory for 2 s or 50 events, writes the batch, and posts it; on success the batch is deleted; on network failure it stays; on `4xx` other than 429 the batch is marked `rejected` and reported to Sentry without payload text. Replays send `X-Forone-Replay: 1`. Batches older than `events.queue_ttl_h = 24` are dropped and counted. `occurred_at` is the device clock at the moment of the event; the server corrects skew.

`EpisodeMemory` (IndexedDB `forone-memory`, store `episodes` keyed by `episode_id`): `{position_ms, speed, transcript_opened_before, article_depth, last_opened_at}`; written on `pause`, `seek` and every 5 s while playing; mirrored to the server through `POST /v1/sessions/{id}/doors/{door}` on `pause` and `visibilitychange` so the position survives a reinstall (PRD 4 rule 4).

### 4.7 The private podcast feed

**Tokens.** `feed_tokens` is the topology's table (32 random bytes, base64url, one live row per learner). Reset inserts a new row and sets `revoked_at` on the old one; a revoked token returns `410 Gone` with a one-line Arabic XML comment so the podcast app shows an error rather than silence. The feed URL is shown in A10 and Controls as `https://api.forone.app/f/{token}.xml` with a copy button and a deep link where the app supports one (Apple Podcasts accepts `podcast://api.forone.app/f/{token}.xml`; Pocket Casts accepts `pktc://subscribe/api.forone.app/f/{token}.xml`; Overcast accepts `overcast://x-callback-url/add?url=`; the instruction card tries the deep link first and shows the copy button always).

**Rendering.** `GET /f/{token}.xml` (no cookies, no CORS needed, `Cache-Control: private, max-age=300`, `ETag` = sha256 of the last `published_at` plus token row id):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podcast="https://podcastindex.org/namespace/1.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>For one · برنامج فيصل</title>
  <link>https://app.forone.app/today</link>
  <language>en</language>
  <itunes:author>For one</itunes:author>
  <itunes:block>Yes</itunes:block>
  <podcast:locked>yes</podcast:locked>
  <itunes:image href="https://api.forone.app/f/{token}/cover.png"/>
  <itunes:type>episodic</itunes:type>
  <description>برنامجك الخاص بالإنجليزية. هذا الرابط لك وحدك؛ تقدر تغيّره من الإعدادات.</description>
  <atom:link rel="self" type="application/rss+xml" href="https://api.forone.app/f/{token}.xml"/>
  <item>
    <title>Karim vs Mona: the interview (6 min)</title>
    <guid isPermaLink="false">ep_01JD3K...</guid>
    <pubDate>Wed, 09 Dec 2026 04:40:00 GMT</pubDate>
    <itunes:duration>386</itunes:duration>
    <itunes:season>1</itunes:season><itunes:episode>12</itunes:episode>
    <enclosure url="https://api.forone.app/f/{token}/ep_01JD3K....mp3" length="4643212" type="audio/mpeg"/>
    <description><![CDATA[<p><a href="https://app.forone.app/call/ep_01JD3K...?k=fl_8Zq...">اتصل بكريم</a> · <a href="https://app.forone.app/show/ep_01JD3K...?k=fl_8Zq...&door=read">اقرأ المقال</a></p>]]></description>
  </item>
</channel></rss>
```

`<itunes:block>Yes</itunes:block>` and `<podcast:locked>yes</podcast:locked>` keep the feed out of directories (PRD 12.6). The channel title carries the learner's first name once; item descriptions carry exactly the two links (pipeline 4.12 says `notes_html` holds the call link and the article link and nothing else; `api.feed` renders them from `feed_links` rather than storing HTML, so a token reset re-mints every link). Items: the last 60 published episodes plus the weekly proofs (`episodes.kind = proof`, published by `proof/make` through the same `feed.publish`), newest first; a `trial_ended` learner's feed keeps its items and gains no new ones. The feed never contains the sample, the pilot's notes, or any text about the learner beyond the title.

**Enclosures.** `GET /f/{token}/{episodeId}.mp3`: validates the token, checks the episode belongs to the token's learner and `feed_items.published_at <= now()`, opens the S3 object the `media_objects {kind: feed_full}` row names (`forone-media/{lid}/episodes/{episodeId}/episode_feed.mp3`) with the learner's DEK (SSE-C) and the request's `Range` header, and streams it with `Accept-Ranges`, `Content-Length`, `Content-Range`, `ETag` and `Cache-Control: private, max-age=31536000`. HEAD is supported (Apple Podcasts sends it). Every request appends a `feed_fetches` row.

```sql
create table feed_links (                -- D7: the links placed in feed item notes
  token        text primary key,         -- "fl_" + 24 random bytes base64url
  learner_id   uuid not null references learners(id) on delete cascade,
  feed_token   text not null references feed_tokens(token),   -- revoked with the feed token
  episode_id   uuid not null references episodes(id),
  created_at   timestamptz not null default now(),
  expires_at   timestamptz not null,     -- feed.link_ttl_days = 30 after publish
  used_n       integer not null default 0
);
create table feed_fetches (              -- D6: operations and Part 18 #11, never learner events
  id bigserial primary key, learner_id uuid not null, feed_token text not null,
  kind text not null check (kind in ('xml','enclosure','cover')), episode_id uuid,
  ua_family text, range_start bigint, range_end bigint, bytes_sent bigint, status smallint,
  at timestamptz not null default now()
);
create index on feed_fetches (learner_id, at desc);
```

`links.mint(learner_id, episode_id)` is what the pipeline's publisher calls for `notes_html` (section 9); `api.feed` renders the item from `feed_items` plus the live `feed_links` row for that episode, so the stored `notes_html` is only a fallback.

**Counting (D6).** `feed_fetches` feeds three operational views: podcast apps in use by `ua_family` (Part 18 #11, reported weekly to Muath); enclosure fetch within 24 h of publish as a feed adoption measure; and the data domain's "feed episode credited once" rule, which it applies from `call_turn`, `chat_message` or `small_door` events and not from this table. No `play` event is ever written from a fetch; the data domain's `play.surface = "feed"` value is reserved and never emitted in the beta.

**Feed-to-call (D7).** `/call/{episodeId}?k=` → `POST /v1/links/exchange`: the link must be unexpired and its feed token live; `api` creates an `auth_sessions` row `{scope: "feed_link", episode_id, learner_id}` (14 days) and sets the cookie; `used_n` increments. The page logs `app_open {entry: "feed_link", standalone: false, feed_to_call_ms: null}` and, when the call room joins, `client_perf {kind: "feed_to_call_ms", value}`. A limited session may: `GET /today`, `GET /episodes/{id}`, media, `POST /calls` for that session, notes, chat, `POST /events`. It may not: Controls, billing, export, delete, feed reset, notebook edits (reads are fine). The screen shows a thin line "signed in through your feed link; sign in to change settings" only on the blocked surfaces. If the same browser already holds a full session, the link just opens the call.

**Return detection.** `api` sends `learner.return_detected` when a full or limited session's first request of the day finds no session event in 5 or more days; the feed XML and enclosure routes never send it (D6; a deviation from topology 3.6, section 9).

### 4.8 Web push, the stream, and the three message kinds

**Subscriptions.**

```sql
create table push_subscriptions (
  id uuid primary key default gen_random_uuid(),
  learner_id uuid not null references learners(id) on delete cascade,
  endpoint text not null unique, p256dh text not null, auth text not null,
  ua_hint text, standalone boolean not null default false,
  created_at timestamptz not null default now(), last_ok_at timestamptz, failed_n smallint not null default 0, revoked_at timestamptz
);
```

The permission prompt is requested only from a tap on "turn on the drop notification" (A10's install card, or Controls), never on load; on iOS it is offered only when `navigator.standalone === true` (iOS 16.4+ allows web push only in the installed app) and the install card is shown first. `pushsubscriptionchange` re-subscribes and re-posts. A send that returns 404 or 410 sets `revoked_at`; three consecutive other failures do the same.

**Senders.** `api` has exactly three functions that can send to a learner, and nothing else in the codebase imports the push or email adapters:

| Kind | Function | Channel | Payload |
|---|---|---|---|
| Drop notification | `push.drop_notification(lid, episode_id)` from `day/next`; skipped when `consents.drop_notification = false` or no live subscription | Web push | `{kind: "drop", title: "Karim vs Mona: the interview (6 min)", url: "/today?entry=push", episode_id}` |
| Gap note | `push.gap_note(lid)` and `email.send(kind: "gap_note")` from `gap/note`, once | Web push and email | `{kind: "gap_note", title: <the learner's own words, first 80 chars>, url: "/today?entry=gap_note"}`; the email body is the learner's text verbatim, signed by no host |
| Transactional | `email.send(kind ∈ {signin_code, receipt, trial_ending, payment_failed, export_ready, trial_deleting_soon, account_deleted})` | Email (Resend, from `show@forone.app`) | templates in the language package; no host voice, no episode content |

The SW's `push` handler parses the payload, refuses any `kind` other than `drop` or `gap_note` (logs to Sentry, shows nothing), and calls `showNotification(title, {body: "", tag: kind + episode_id, renotify: false, data: {url}})`; `notificationclick` focuses an existing client or opens `url`. There is no `body`, no icon badge count, no action buttons. The drop push is sent with `TTL: 7200` so a phone off for a morning never receives a stale drop in the evening.

**The stream (D12).** `GET /v1/stream` holds one SSE connection per foreground learner; `api` `LISTEN`s on `forone_learner_{lid}` and relays `NOTIFY` payloads written by the modules that change the learner's visible state. Each message is `id: <seq>\nevent: <name>\ndata: <json>`; a comment line `: hb` every 20 s keeps the ALB's 60 s idle timeout from closing it. The client reconnects with `Last-Event-ID`; `api` replays from `learner_stream_log` (a 24 h ring table) or sends `event: resync` if the id is too old, after which the client refetches `TodayDoc`.

| event | data | client reaction |
|---|---|---|
| `today.changed` | `{reason: "episode_ready"|"session_closed"|"drop"|"swap"|"return"|"proof_ready"|"crisis"}` | refetch `/today`; warm the cache on `episode_ready` |
| `episode.manifest` | `{episode_id, manifest_version, timing_quality, full_ready}` | the streaming player switches source at the next seam |
| `notes.ready` | `{session_id, count}` | Today shows "Salma's notes (2)" |
| `chat.message` | `{host, message_index, kind: "host"|"crisis"}` | append to the thread if open, else a dot on the Chat door; `crisis` renders the package's resources card inline |
| `call.thread` | `{call_id, turn_index}` | voice-note reply arrived (live-call domain 5.1) |
| `ideas.ready` | `{plan_id}` | the three ideas appear at the chat closer or on Today |
| `controls.changed` | `{}` | refetch `/controls` (a change made through Salma by voice) |

Nothing in the stream is required for correctness: every document is also polled with `If-None-Match` every 30 s while visible, and on `visibilitychange` to visible.

### 4.9 Auth

```sql
create table accounts (                       -- one row per external identity
  id uuid primary key default gen_random_uuid(),
  learner_id uuid not null references learners(id) on delete cascade,
  provider text not null check (provider in ('email','apple','google')),
  subject text not null,                      -- normalized email, Apple sub, Google sub
  email text, verified_at timestamptz not null default now(),
  unique (provider, subject)
);
create table otp_codes (
  id uuid primary key default gen_random_uuid(),
  email citext not null, code_hash text not null,         -- argon2 of a 6-digit code
  created_at timestamptz not null default now(), expires_at timestamptz not null,   -- auth.otp_ttl_s = 600
  attempts smallint not null default 0, consumed_at timestamptz
);
create index on otp_codes (email, created_at desc);
create table auth_sessions (
  id text primary key,                        -- 32 random bytes base64url; the cookie value
  learner_id uuid not null references learners(id) on delete cascade,
  scope text not null check (scope in ('pre_account','full','feed_link')),
  episode_id uuid,                            -- feed_link only
  ua_hint text, standalone boolean,
  created_at timestamptz not null default now(), last_seen_at timestamptz not null default now(),
  expires_at timestamptz not null, revoked_at timestamptz
);
create index on auth_sessions (learner_id) where revoked_at is null;
create table handoff_tokens (                 -- D10
  token text primary key, learner_id uuid not null references learners(id) on delete cascade,
  created_at timestamptz not null default now(), expires_at timestamptz not null, used_at timestamptz
);
```

Rules:

1. **Pre-account.** `POST /onboarding/start` creates `learners {status: pre_account}` and `auth_sessions {scope: pre_account, expires_at: now() + 24 h}`. `retention/daily` deletes `pre_account` learners older than 24 h with no claim (their pilot audio and intake with them). A pre-account session may do A1 to A10 and nothing on `/show`, `/notebook`, `/controls`.
2. **Claim at A9.** Any of the three sign-ins, when the current cookie is `pre_account`: if the identity is new, link `accounts` to this learner and set `status: trial`; if the identity already belongs to another learner (a returning learner who restarted onboarding), the response is `409 existing_show` and the client offers "open your existing show" (which signs in as that learner and abandons the pre-account one) or "keep this new show" (which is refused in the beta: one account, one show; the pre-account learner is deleted). `PUT /me {birth_date}` follows; under 18 deletes the pre-account learner and shows the plain message (PRD 1.4).
3. **Email code.** `POST /auth/otp/request` always returns 202; rate limits: 3 per email per 10 min, 10 per IP hash per hour; the email is kind `signin_code` with the 6-digit code and nothing else; `verify` allows 5 attempts per code; the code is consumed on success.
4. **Apple.** Services ID for `app.forone.app`, `response_mode=form_post` to `/v1/auth/apple/callback`, the state cookie carries the pre-account session id; Apple's private relay address is stored as `accounts.email`. Two practical requirements the week-3 checklist carries: the Apple Developer Program membership (section 10), and registering `forone.app` and `show@forone.app` under "Sign in with Apple for Email Communication" with SPF and DKIM on the sending domain, because mail to `@privaterelay.appleid.com` from an unregistered sender bounces, which would silently break sign-in codes, receipts and the export link for every Apple-relay learner.
5. **Google.** OIDC authorization code with PKCE, `prompt=select_account`; the Google Cloud OAuth consent screen must be verified for `forone.app` (section 10).
6. **Sessions.** Full sessions last `auth.session_days = 90`, rolling on use; `signout` revokes the row; account deletion revokes every row at once (data domain 4.12.2 step 1); `api` sets `forone.learner_id` for RLS from the row on every request.
7. **Install handoff (D10).** The manifest route is a Next.js route handler on `app.forone.app`: it reads `forone_s` (same-origin, so the browser sends it with the manifest fetch), forwards it to `POST /v1/handoff/mint` (one token per learner per 7 days), and returns the manifest JSON with `start_url: "/today?h=<token>"`, `scope: "/"`, `display: "standalone"`, `id: "/"`, icons, `theme_color` from the show colour. On first launch of the installed app, `/today?h=` posts to `POST /v1/handoff/exchange`, receives a full-session cookie in the PWA's jar, logs `app_open {entry: "install_handoff", standalone: true}` and `pwa_install`, and strips `h` from the URL. A used or expired token simply shows the sign-in screen (no email prefilled, no leak). Android Chrome shares the jar, so the token is unused there and expires.
8. **Feed link sessions** as in 4.7.

### 4.10 Onboarding specifics the client owns

**4.10.1 A1 to A10.** A1 is static Arabic with the 18+ checkbox gating Start (unchecked → the button is disabled with the reason in text, not a toast). A2 requests the microphone only on Talk. A3 is the live-call domain's Salma call; the client renders fact cards from `ui.fact_card` messages and sends `fact_card.edit` and `fact_card.remove` on the data channel. A4 word check: 48 items from `OnboardingDoc.word_check` shown one at a time as big yes/no, a 75 s timer in code, `word_check_answer` per item, Skip as large as Start. A5 casting plays the cached hello clips from the package (no synthesis), swap cycles the host's pool, accent picks British or American with its sample; `PUT /onboarding/casting`; the same screen plays the hosts saying the learner's name from `OnboardingDoc.name.candidates[chosen].clip_url` with a "say it differently" button that cycles the three candidates through `PUT /onboarding/name` (the pipeline's name verification, its 4.8; shown always, emphasised when `verified == false`). A6 the pilot opens the player with the transcript open and one hint overlay (Huh? and tap a word) that disappears on first interaction; the pilot streams (4.4.4 case 3). A7 is the live-call domain's `first` call. A8 shows one note card from `NotesDoc` for the onboarding session. A9 collects sign-in, birth date, drop time in life terms (four chips with an adjustable clock, stored as `drop_time_local` and `anchor_text`), the voice-storage checkbox with its one sentence and the plain sentence about deletion; `consent_change {kind: voice_storage, text_shown_version}`. A10 shows the three ideas, "Tell Salma an idea" (voice or text through the pipeline's `idea.chosen {source: tell_salma}`), then the one-time setup card: install (iOS: the share-sheet steps with one picture, since Safari fires no `beforeinstallprompt`; Android: the `beforeinstallprompt` event's `prompt()`), the drop notification button, and the feed card with the copy button and three app instructions (section 10 names the apps).

Measured on first open: `client_perf {kind: "first_sound_ms"}` (page load to Salma's first clip playing, reported by the call screen) and `client_perf {kind: "first_english_ms"}` (the worker's `english_line: production` turn, reported by the worker; this domain only displays nothing).

**4.10.2 The then-and-now recording screen (`/recording/[recordingId]`, P0 for the first "then").** Offered as `TodayDoc.recording_offer` and at the end of the session-2 notes, framed in Salma's words as "the opening tape of your season"; Skip is as large as Start and says plainly that skipping means no voice comparison this month. Three parts from `RecordingDoc.parts`, in order: (1) retell: the package's short story plays (`reference_audio_url`, single voice, slow), then record up to 90 s; (2) opinion: the prompt in Arabic with the topic in English, record up to 90 s; (3) repeat: eight sentences of increasing length, each played once and recorded (up to 8 s each). Each part is one `MediaRecorder` capture uploaded as `POST /v1/recordings {task, recording_id, part_index, reference_text}` → one `recording` event per part with `media_object_id`; a part that fails to upload is retried from IndexedDB like an event batch (the blob is held in `forone-queue` for 24 h). Nothing is scored on screen; the end is Salma's one sentence. When `consents.voice_storage == false`, the screen offers "keep this one recording" (`kept_explicitly: true`, PRD 12.5.2) before the first part. Recording container: Safari produces `audio/mp4` (AAC), Chrome `audio/webm;codecs=opus`; the client sends whatever `MediaRecorder.isTypeSupported` allows, preferring `audio/mp4`, and the server-side adapters accept both (section 9). The same capture component serves "say it once", shadow, voice notes and the small door.

### 4.11 Bidirectional text

- `<html lang="ar" dir="rtl">` once. Tailwind with only logical utilities (`ps-`, `pe-`, `ms-`, `me-`, `start-`, `end-`, `text-start`); an ESLint rule forbids `pl-`, `pr-`, `ml-`, `mr-`, `left-`, `right-`, `text-left`, `text-right` in `apps/web`.
- Every block that may contain learner or host text renders through one `<Bidi as="p" text={...}/>` component that sets `dir="auto"` and `style="unicode-bidi: plaintext"`; inline English inside an Arabic sentence (Salma's notes quote English) is wrapped in `<bdi>` by a tiny tokenizer that splits on script runs (Arabic block versus Latin) so punctuation stays with its run.
- Fixed-direction surfaces: the transcript, article, captions, host chat bubbles' English text, idea lines and the scrub bar are `dir="ltr"` with `text-align: start`; the chrome around them stays RTL. Timestamps `2:14 / 7:02` are LTR runs inside `<bdi>`.
- Digits: Western (0 to 9) everywhere, `font-variant-numeric: tabular-nums` for times and counts [DECISION; section 10 item 5 for the brand call].
- Fonts: IBM Plex Sans Arabic (Arabic UI) and IBM Plex Sans (Latin content), both through `next/font/local` with `font-display: swap`; Arabic body `line-height: 1.7`, Latin transcript `1.5`; the transcript's current line is 20 px, the rest 17 px; minimum 16 px anywhere.
- Mirroring: directional icons (back, chevrons) use `rtl:-scale-x-100`; play, pause, ⟲ and the S button are not mirrored.
- Keyboard and input: chat input `dir="auto"`; the learner's bubbles use `plaintext` so an English sentence typed in an Arabic UI aligns left and reads correctly.
- A Playwright snapshot suite renders the thirteen screens with mixed-direction fixtures (Arabic note quoting English, English bubble with an Arabic word, a word sheet) on both platforms and fails on diff.

### 4.12 State management

| Concern | Where | Notes |
|---|---|---|
| Server documents (`TodayDoc`, `EpisodeDoc`, `NotesDoc`, `ChatDoc`, `NotebookDoc`, `ControlsDoc`, `ShelfDoc`, `RecordingDoc`) | TanStack Query, keys `[doc, id, lm_version]` | `X-Forone-LM-Version` from any response invalidates stale keys; `staleTime` 30 s; persisted to IndexedDB for offline reads |
| Player | `PlayerStore` (Zustand) | 4.4.2; one instance; survives route changes so the mini-player on Today and the lock screen agree |
| Call | `CallStore` (Zustand) | phase and turn state from `forone.ui` messages (live-call domain 4.12); captions buffer; nothing persisted |
| Event queue | IndexedDB `forone-queue` | 4.6; also holds pending recording blobs |
| Episode memory | IndexedDB `forone-memory` | 4.6 |
| Per-viewer conveniences | `localStorage` | theme override, last tab, "earphones suggested" flag; wrapped in try/catch |
| Navigation | URL | every sheet (player, word sheet, notes) is a route or a search param so back closes it |

The client holds no copy of the learner model: facts, counts and claims are rendered from documents and never cached beyond the query cache's TTL.

### 4.13 The sample-episode landing page

`forone.app/` (SSR, cached at the edge for 10 min, `lang="ar"`): the promise sentence, "Hear your own show", and the three questions (name; something you could talk about for an hour; what you do), each with a text field and a hold-to-talk button (`MediaRecorder`, 20 s cap). Submit → `POST /v1/sample` multipart `{name, topic, job, topic_audio?, job_audio?, contact?}` with the first-party device cookie `forone_d` (random id set on first visit; `sample_requests.device_hash = sha256(it)`). `api` applies the two limits (one per device and per contact per 24 h) and returns `202 {sample_id}` or `429 {retry_at}` with Salma's plain sentence; voice answers are referenced as `answers_audio_ref` on `sample.requested` and transcribed inside the pipeline's sample path (section 9). The page polls `GET /v1/sample/{id}` every second: `{state: "making"|"streaming"|"ready"|"failed", segments: [{url}], duration_s}`; on `streaming` the minimal player (play, pause, scrub, no transcript, no speed) starts on scene 1 through the same two-element handoff as 4.4.4 case 3; the sample audio is public-bucket (`forone-media/samples/{sample_id}/`, service key, 30-day expiry) so no cookie is needed. `client_perf {kind: "sample_first_sound_ms"}` is posted anonymously to `POST /v1/telemetry` (no learner).

After the audio (Salma's Arabic ending is in the file): the waitlist form (`POST /v1/waitlist {name, contact: whatsapp|email, why_english, self_rating, city, sample_id}`) and "Keep it" which shows the share page URL `forone.app/s/{sampleId}` and `navigator.share({url})` where available. The share page is public, `noindex`, with Open Graph title "برنامج {name}", the OG image rendered from the typographic cover, and the same minimal player; it expires with the audio. Invites (`/i/{code}`) are minted by Muath from the waitlist in `/admin` and carry the answers into `POST /onboarding/start`; the channel that carries the invite link (email or WhatsApp) is the topology's open item 9; a used or expired code shows a plain line.

### 4.14 Analytics without surveillance and accessibility basics

**Events added to the log** (data domain registry; section 9):

| type | door | payload | why |
|---|---|---|---|
| `app_open` + | `today` | `entry: push|gap_note|feed_link|install_handoff|home_screen|browser|invite, standalone: bool, drop_delta_min: int|null` | 16.2 "unprompted return" and "within an hour of the drop"; feed-to-call funnel |
| `pwa_install` + | `onboarding`, `controls` | `platform: ios|android|desktop, method: a2hs|prompt|unknown` | adoption of the install card |
| `client_perf` + | any | `kind: first_sound_ms|play_start_ms|word_sheet_open_ms|feed_to_call_ms|bg_play_stop|sample_first_sound_ms, value: int|null, context: {}` | PRD 15 budgets measured on real devices, never shown to the learner |
| `push_permission` + | `onboarding`, `controls` | `result: granted|denied|dismissed|unsupported` | why drops do not arrive |

Nothing else is collected. No third-party script runs on `app.forone.app`; the public landing page runs none either (Vercel's edge logs are the only request logs; section 10 item 8). Sentry: `sendDefaultPii: false`, `beforeSend` strips URLs' query strings (`k`, `h`), breadcrumbs exclude fetch bodies, no session replay; the learner id is attached as a hashed tag so a crash can be matched to a support request without the id being readable in Sentry. The sample page's device cookie is not a tracking identifier: it exists only for the 24 h limit and is deleted after 48 h.

**Accessibility basics (P0).** Every control has an Arabic `aria-label`; hit targets at least 44×44 px; text scales with the system setting (rem everywhere, `-webkit-text-size-adjust: 100%`) and Controls offers a larger reading size for the article (`text_size`); contrast AA in both themes with the show colour used only on covers and accents, never as text on tinted backgrounds; `prefers-reduced-motion` disables the karaoke scroll animation and the retell ring's motion; focus is trapped in sheets and returned on close; the transcript marks the current line with `aria-current="true"` and a visually hidden live region announces the line on Huh? and ⟲ line (not per word); the hold pad and S button work with a keyboard (hold Space, hold S) for screen-reader users on desktop; captions on calls are on by default and the transcript-first mode is the Controls "transcript always open" setting; every audio element has a text equivalent on the screen (the transcript, the notes text, the gloss). Colour is never the only signal (the recast word is bold and underlined in captions).

### 4.15 Configuration keys

| Key | Default | Meaning |
|---|---|---|
| `web.sw.cache_episodes_n` | 3 | episodes kept in `forone-media-v1` |
| `web.sw.warm_assets` | `[episode.m4a, timings.json, glosses.json, package.json, article.m4a, recap.m4a]` | added to the cache on `episode_ready` |
| `web.sw.warm_assets_metered` | `[timings.json, glosses.json, package.json]` | the subset warmed under `saveData` |
| `events.flush_ms`, `events.batch_max`, `events.queue_ttl_h` | 2000, 50, 24 | event queue |
| `player.speeds` | `[0.75, 0.85, 1.0]` | the only speeds; the control reads this list |
| `player.huh_rate` | 0.85 | Huh? replay speed |
| `player.seam_snap_ms` | 1500 | lock-screen seek snapping to seams |
| `recording.max_s` | `{retell: 90, opinion: 90, repeat: 8, say_it_once: 15, shadow: 20, voice_note: 90, small_door: 60}` | capture caps |
| `feed.token_bytes`, `feed.link_ttl_days`, `feed.items_max` | 32, 30, 60 | feed |
| `feed.enclosure_format`, `feed.enclosure_bitrate_kbps` | `mp3`, 96 | the pipeline's feed encode (read there); `m4a` is the fallback value |
| `push.drop_ttl_s`, `push.max_failures` | 7200, 3 | web push |
| `sse.heartbeat_s`, `sse.resync_after_s` | 20, 86400 | stream |
| `auth.otp_ttl_s`, `auth.otp_attempts`, `auth.session_days`, `auth.pre_account_ttl_h`, `auth.feed_link_session_days` | 600, 5, 90, 24, 14 | auth |
| `handoff.ttl_days` | 7 | D10 |
| `sample.device_limit_h`, `sample.contact_limit_h`, `sample.share_ttl_days` | 24, 24, 30 | 2.1 limits |
| `poll.today_s` | 30 | ETag polling while visible |
| `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_LIVEKIT_URL`, `NEXT_PUBLIC_VAPID_PUBLIC_KEY`, `NEXT_PUBLIC_SENTRY_DSN` | | the only public env values in `web` |

### 4.16 Payments touchpoints the client owns

The processor is OPEN (Part 18 #2); the client sees only a hosted checkout. `POST /v1/billing/checkout {plan}` returns the processor's URL; the return URL is `/controls?billing=done`, where the client refetches `/billing` and `TodayDoc` (the webhook sets `learners.status`). The day-7 card on Today and the day-6 `trial_ending` email are driven by `trial_started_at`. Apple Pay on the web, which PRD 1.4 requires alongside Mada and cards, needs the processor's domain-association file served at `https://app.forone.app/.well-known/apple-developer-merchantid-domain-association` (a static file in `public/`), registered with the processor on 2026-11-16 when it is chosen; the Stripe scaffold's file is the placeholder until then. Mada and Apple Pay availability on the hosted page is the processor's; the client never renders a card form.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detected by | Behaviour | Learner sees |
|---|---|---|---|
| Offline on the bus | `navigator.onLine`, fetch errors | Shell and today's episode from cache (Blob URL); events queue; Call, Chat, Swap disabled with one line; Today from the doc cache marked stale | The episode plays; "no signal, the call waits" on the call door |
| Episode not warmed (first open after the drop with no prior visit) | cache miss | Streams from `api` with Range (`source: network`); first bytes arrive in 200 to 400 ms in-region, play starts on `canplay`; the full file is added to the cache in the background | Up to 1 s longer start; still under 2 s on 4G |
| Cache Storage read fails or throws (private mode, cleared site data) | `caches.match()` rejects or returns nothing | Fall to the network source for this play; re-warm later | Nothing |
| iOS evicts Cache Storage (site unused 7 days, browser tab not installed) | cache miss on open | Re-warm; the archive streams; nothing is lost because the server holds everything | Slower first play that day |
| Quota exceeded | `QuotaExceededError`, `purgeOnQuotaError` | Keep only today's episode; drop fonts cache last | Nothing |
| `api` down | fetch 5xx or timeout | Cached `TodayDoc` read-only; events queue 24 h; calls cannot start (voice notes also need `api`) | "The studio is unreachable; your episode still plays" |
| Vercel down | shell fails to load | Installed PWA runs from precache (shell cached); a fresh browser gets nothing; the feed and media are on `api` and unaffected | Installed learners notice nothing; the feed works |
| SSE drops (ALB, sleep, roaming) | `EventSource.onerror` | Reconnect with backoff 1 s to 30 s and `Last-Event-ID`; the 30 s ETag poll continues regardless | Nothing |
| Push subscription expired or permission revoked | 404/410 from the push service; `Notification.permission` | Row revoked; Controls shows "notifications are off on this phone" with the button; the feed's own alert remains | One line in Controls |
| Drop push arrives but the episode was swapped or replaced by a return episode before open | `episode_id` in the payload differs from `TodayDoc` | The page ignores the payload id and shows Today | The current episode |
| Feed token leaked or forwarded | learner reports, or `feed_fetches` from many `ua_family` values | Controls "reset the link" revokes the token and every `feed_links` row; a 410 with an Arabic comment to the old subscribers | New link to paste |
| Podcast app refuses private feeds or the enclosure format (Part 18 #11) | `feed_fetches` never arrive for that `ua_family`, or the week-3 test fails | A10 and Controls name only apps that work; the app player and push remain; `feed.enclosure_format` is the switch if a named app needs the other container | The instruction card |
| Feed link opened in a browser with an old full session for another learner (shared phone) | `links.exchange` sees a mismatch | The exchange replaces the session with the limited one for the link's learner and says so | "Opened Faisal's call link" |
| Cookie jar split on iOS (Safari vs installed) | sign-in screen in the PWA | D10 handoff; if the token was consumed or expired, sign in once with the email code; Android unaffected | At most one email code |
| Sign-in code to an Apple relay address bounces | Resend bounce webhook | Alert; the learner is shown "use Google or another email" on the next attempt; prevented by the domain registration in 4.9 rule 4 | One plain line |
| Mic permission denied | `NotAllowedError` | Onboarding falls to Type mode; calls fall to voice notes only if the mic later works, else the chat door; the recording screen says what to change in system settings | Plain line with the system settings path |
| Screen Wake Lock unsupported | `navigator.wakeLock` missing | Live-call domain's silent video loop | A one-line notice |
| Background play stops on iOS | `pause` without learner action | Logged `client_perf bg_play_stop`; the lock-screen control resumes it; the feed is the fallback channel | A paused episode |
| Scene handoff gap audible on a streaming episode | manifest `seam == null` for a segment (should not happen) | 150 ms crossfade on `aux` start | A tiny gap at a scene change |
| Recording upload fails mid-task | fetch error on `POST /recordings` | The blob stays in `forone-queue` and is retried for 24 h; the task continues; the next part is not blocked | Nothing, or "saved, will send when there is signal" |
| Stale shell after a deploy | SW `updatefound` | `skipWaiting` + reload at the next navigation, never during playback, a recording or a call; `api` compatible for one release | Nothing |
| Clock badly wrong on the device | server skew check | `occurred_at` corrected server-side; `client_perf` values unaffected (durations) | Nothing |
| Learner deletes the account from another device | `410` on any request | The PWA clears caches, IndexedDB and the cookie and shows the deletion sentence | One screen |
| Trial ended without paying | `TodayDoc.learner.status == trial_ended` | Today shows Salma's sentence and the plans; Show, Notebook, Controls (export, delete) keep working for 90 days; the feed publishes nothing new | A quiet Today |
| Sample abuse (many devices) | `sample_requests` rate by IP hash over 1 h | `api` returns 429 with `retry_at`; the pipeline's $0.05 ceiling bounds the damage per sample | Salma's one plain sentence |

---

## 6. Cost and performance against the budgets

**Budgets.**

| Budget (PRD-v2 15) | How this domain meets it | Measured by |
|---|---|---|
| First sound under 60 s | A1 and A2 are static and precached after the first visit; `POST /onboarding/start` is one round trip (about 200 ms in-region); Salma's first clip is a package asset the call worker plays on subscribe | `client_perf first_sound_ms`, p50 target 25 s (page load 2 s, Start and Talk taps, mic prompt, room join 1.5 s) |
| Sample playable under 30 s | The page starts on scene 1 within 300 ms of `streaming`; the rest is the pipeline's 25 to 40 s | `sample_first_sound_ms` (anonymous telemetry) |
| Pilot under 45 s after A3 | A5 casting covers the wait; the player opens on `episode.manifest` with `timing_quality: sentence` | `play_start_ms {context: pilot}` |
| Dropped episode start under 2 s | Warmed cache: `caches.match()` plus `blob()` of a 6 MB entry takes 50 to 150 ms on a 2022 Android, then `play()` on a gesture starts in under 300 ms; cold path 200 to 400 ms to first bytes from `api` in `me-central-1` plus decoder start | `play_start_ms {context: daily}`; p95 target 1.5 s |
| On-demand episode under 30 s | Scene 1 on `episode.manifest`; the player is ready before the audio is | `play_start_ms {context: swap|return}` minus pipeline time |
| Word sheet under 300 ms | Local index lookup (under 5 ms) plus sheet paint (under 100 ms on a 2022 Android); the only network is a rare miss | `word_sheet_open_ms`, p95 target 150 ms |
| Call connect under 3 s | `POST /calls` then LiveKit join (live-call domain); the planning card, when shown, is before the clock starts | the live-call domain's `connect_ms` |
| Drop at the drop time | `day/next` publishes the feed item and sends the push in the same step sequence; push delivery is the push service's (seconds to a minute); podcast apps poll on their own schedule (Apple Podcasts: hourly to daily unless the learner refreshes) | `drop.published` to `app_open{entry: push}` delta |

**Costs (this domain's share of hosting; the PRD's "proof share and hosting" line is $0.03 per session).**

| Item | Beta (about 100 learners, 20 sessions a month) | Note |
|---|---|---|
| Vercel Pro | $20 per month flat | No audio through Vercel; the shell is a few hundred KB cached at the edge |
| Media egress from `api` | 6 MB app file plus 5 MB feed file per episode; about 1.1 GB per learner-month at one app play and one feed download; 110 GB per month at 100 learners; AWS egress about $0.09 per GB → about $10 per month | $0.005 per session; at 10,000 learners this is the item the topology moves to a `media` service or a CDN (needs the security decision on produced audio) |
| Extra MP3 encode and storage for the feed | about 5 MB per episode in S3 ($0.0001) and one ffmpeg pass (under 2 s of worker CPU) | inside the pipeline's voice-studio line |
| Web push | $0 | VAPID direct to the push services |
| Email (Resend) | $20 per month tier | codes, receipts, trial ending, export, deletion, gap notes |
| Sentry | free tier during the beta | errors only, sampled |
| BrowserStack (device tests) | about $40 per month | iOS Safari and Android Chrome runs in CI, weeks 3 to 5 |
| Fonts, icons | $0 | self-hosted |

Per session: about $0.006 at beta scale, $0.004 at scale (egress dominates and falls with a CDN). It fits inside the $0.03 line with room for the proof's audio.

**Bundle budget.** The `(app)` shell under 250 KB gzipped JavaScript on the Today route (Next.js, React, TanStack Query, Zustand, `idb`; `livekit-client` loaded only on `/call`); fonts about 300 KB for both families' regular and semibold; Lighthouse PWA audit green on the staging URL in week 3.

---

## 7. Build plan for 2026-11-02 to 2026-12-06

The PRD places the client in week 3 (2026-11-16); with one to two engineers the shell must start earlier at low intensity while the pipeline engineer is busy. Everything tagged P0 works on 2026-12-07.

| Week | Dates | Ships | P0 / P1 | What the pilot (Milestone 0) data lets us test |
|---|---|---|---|---|
| 1 | 2026-11-02 to 11-08 | `apps/web` skeleton in the monorepo; Next.js, Tailwind with the logical-property lint rule, `next/font` with both families, the `Bidi` component and the mixed-direction snapshot suite; design tokens and the typographic cover; `middleware.ts` host routing; the law lint rule; Vercel project with the two hostnames on the brand domain (section 10 item 1); OpenAPI codegen wired to the `api` skeleton; the Apple Developer and Google OAuth applications filed | P0 | M0 Salma notes (Arabic quoting English) and M0 scripts are the fixtures for the bidi snapshots |
| 2 | 2026-11-09 to 11-15 | Player against hand-built `timings.json` (an M0 episode run through the pipeline's `align` step on staging, or Scribe word timestamps converted by a 50-line script): sync loop, ⟲ line, Huh?, speeds, transcript fold, Media Session; Blob-URL playback from Cache Storage and the network fallback; word sheet from a hand-built `WordIndex`; service worker with media caching; event queue and `POST /v1/events`; email-code auth and sessions; `TodayDoc` rendered from a fixture; the capture component (`MediaRecorder`, both containers) | P0 | Real M0 audio on real phones in the commute for the week-3 go/no-go on background playback; `word_sheet_open_ms` measured; the M0 then-and-now voice notes replayed through the capture path |
| 3 | 2026-11-16 to 11-22 | Onboarding A1 to A10 wired to `api` and the live-call domain's Salma call, including the A5 name check; Today in all states; Show shelf and episode page; feed route, tokens, `feed_links`, enclosure streaming, `feed_fetches`; web push end to end with the drop; install card and the D10 handoff; Apple and Google sign-in if the developer accounts are approved (else P1), with the Apple relay email domain registered; SSE stream; Controls (drop time, notification, captions, transcript, speed, feed link); payments checkout redirect against the Stripe scaffold and the Apple Pay domain file | P0 (Apple/Google P1 if blocked) | The three synthetic learners' episodes from staging drop into real podcast apps on the team's phones: Apple Podcasts, Pocket Casts and one Android app (`feed.enclosure_format` decided here); the week-3 device matrix (iOS 17, iOS 18, Android 13 and 14 Chrome) for background play, push and install |
| 4 | 2026-11-23 to 11-29 | Call screen (live-call domain's 4.11 and 4.12), Media Session ownership handoff, planning card, captions, voice-note fallback UI, crisis card; notes cards with clips and "say it once"; chat thread with margin notes and the ideas at the closer; feed-to-call handoff measured | P0; shadow door P1 | M0 call transcripts and Scribe audio produce real `NotesDoc` fixtures; M0 learners' phones for the feed-to-call path |
| 5 | 2026-11-30 to 12-06 | Notebook (all sections except the tape), fact edits, working-on veto and add, out in the world; the then-and-now recording screen and its offer; proof screen with "how we know" and the worth-it question; export (passphrase shown once) and delete flows; trial-ended and day-7 payment states; the once-only crisis card on Today; the sample landing page, share page, waitlist and invites; accessibility pass; Lighthouse and bundle budget; the end-to-end run with the Milestone 0 learners re-onboarding through A1 to A10 on prod | P0 | M0 learners' first "then" recordings (where consented) appear in the notebook; cost per session measured includes this domain's egress |
| Beta | from 2026-12-07 | Round two offer on Today, shadow door, the tape, scene-streaming polish (crossfade), Apple/Google if slipped, dial-in entry [P1] | P1 | Part 18 #11 answered from `feed_fetches` by the end of the first cohort |

**Single-engineer cuts, in order:** (1) Apple and Google sign-in to P1 (email code only); (2) no SSE, polling only; (3) no D10 handoff (the installed app asks for one email code); (4) phrase drag selection becomes tap only; (5) the share page becomes a plain download link; (6) no crossfade on scene handoff; (7) Playwright device suite replaced by a manual checklist on two phones. Never cut: the feed, the push, the Blob-URL cache path, the event queue, the recording screen, the law lint rule, the bidi component.

---

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Native app (React Native or Expo) for the beta | PRD-v2 1.4 and decision 7: native after the gates; App Store review and the 15 to 30% fee; the feed carries the commute case |
| Capacitor wrapper around the PWA | Store review and fee without native audio advantages; the beta measures the web |
| Vite SPA on Cloudflare Pages | No SSR for the Arabic landing page's edge caching and OG tags; Cloudflare Workers would be a fourth runtime; the topology chose Vercel |
| Proxying `/v1` through Next.js rewrites to make everything same-origin | Audio would pass through Vercel functions (billed bandwidth, added latency); same-site cookies already work across `app.` and `api.` |
| Playing cached audio through the service worker's fetch handler (Range from Cache Storage) | Safari's media-element requests have not reliably reached service workers across versions; a Blob URL from the same cache is deterministic and costs 6 MB of memory; the plugin stays only as a fallback |
| Per-segment `<audio>` elements for every episode (topology 4.6) | Lock-screen position, scrubbing and Media Session become per-segment bookkeeping on iOS; the full stitched file exists for every ready episode and the seams only matter while streaming |
| MSE or ManagedMediaSource for streaming kinds | iPhone support is recent and uneven; a 60 s scene handoff at a sting is simpler and the pipeline already produces segments |
| Transcoding the feed enclosure on request in `api` | ffmpeg per request on the API tier; the pipeline already runs ffmpeg once per episode |
| AAC-only feed enclosure | Zero-risk compatibility is worth one encode while the podcast apps in use are unknown (Part 18 #11); kept as the configured fallback |
| Signed, expiring enclosure URLs | Podcast apps cache enclosure URLs for days; expiry would break downloads mid-week; the feed token in the path is already the credential and is resettable |
| Counting an enclosure download as a play | Auto-download in Apple Podcasts would make every learner "active" daily; law 1 and the trust contract forbid fake activity |
| Requiring sign-in before a call from the feed link | Kills the feed-to-call handoff, which 19.3 names as the native-switch signal |
| Clerk, Auth0, Firebase Auth | PII in a US processor; per-MAU cost; our needs are 300 lines |
| Passwords | PRD-v2 1.4 chose codes |
| Firebase Cloud Messaging | A processor without benefit on the web; VAPID is a library call |
| WebSockets or a hosted realtime service for the drop | One-directional needs; SSE through the ALB with a heartbeat is enough; nothing depends on it |
| GraphQL or tRPC | Python backend; one client; OpenAPI codegen gives typed calls |
| Redux or a client-side learner model | The server documents are the truth; the client must not compute anything about the learner (law 12) |
| GA4, Mixpanel, PostHog, Hotjar | Trust promise 6 and PDPL; the event log already measures the product |
| Google Fonts at runtime | A third-party request per page; self-hosting is one config line |
| Eastern Arabic digits | Western digits are the norm in Saudi consumer apps and keep times and counts LTR-safe; brand call in section 10 |
| Generated cover images (AI art) | UI lens: typographic covers are cheap, consistent and look like a real back catalogue; no image generation cost |
| Local notifications scheduled on the device | Not available to PWAs on iOS; the drop is a server event anyway |
| A separate recording app flow or WhatsApp voice notes for the then-and-now in the beta | The recording is P0 in week 5 and feeds the rater; one capture component serves five surfaces, and the M0 WhatsApp path has no `media_objects` row, consent flag or per-learner key |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check against that domain's document.

1. **System topology (01).** `api` hosts the feed, media, push, auth, SSE and sample modules in this document under its `/v1` and `/f` routes; `day/next` calls `feed.publish` and `push.drop_notification` as its 4.3 shell shows, and `proof/make` calls `feed.publish` for the proof episode; CORS with credentials for the two web origins and the `X-Forone-Client` header rule are configured on the ALB and FastAPI; the session cookie is on `.forone.app`; `feed_tokens`, `sessions`, `doors`, `episodes`, `calls`, `media_objects`, `sample_requests` are its tables and `episodes.state` (or the pipeline's `status`) exposes `ready` and `published`; `X-Forone-LM-Version` is how its `learnerModelVersion` travels; this document adds `accounts`, `otp_codes`, `auth_sessions`, `handoff_tokens`, `feed_links`, `feed_fetches`, `push_subscriptions`, `waitlist`, `invites`, `learner_stream_log`. **Deviations:** the player uses one element on the stitched file, played from a Blob URL when cached, rather than per-segment elements (its 4.6); `learner.return_detected` is sent on app open or feed-link exchange only, never on a feed fetch (its 3.6; D6); `retention/daily` gains the pre-account 24 h deletion and the `forone_d` cookie hash expiry. The enclosure route is its `/f/{token}/{episodeId}.mp3`.
2. **Episode generation pipeline (02).** `AudioManifest` (`timings.json`) and `WordIndex` (`glosses.json`) are exactly its 4.8 and 4.10, with `timing_quality`, `segments[].seam` and `segments[].stream_url`; `api` maps the asset names `episode.m4a`, `scene-{scene_id}.m4a`, `article.m4a`, `recap.m4a` to the manifest's `app_audio.url`, `segments[].stream_url`, `article_audio.url`, `recap_audio.url`; each index entry gains `rank` (lexicon rank) so Huh? can pick the hardest words without network; **the mix step adds an MP3 render of the feed file (`episode_feed.mp3`, 96 kbps mono, written to `media_objects {kind: feed_full}`) next to its AAC `episode_feed.m4a`, or, if it will not, keeps the `.m4a` with `-movflags +faststart` and `feed.enclosure_format = m4a` (D5)**; `package.json` carries `player_defaults {transcript_open, speed}`, `targets[]`, `new_words[]`, `planning_words[]`, the chat opener, the recap text and `why`; the publisher calls `links.mint(learner_id, episode_id)` for the two links in `notes_html`; ideas are English lines (its open item 8); the sample path accepts `answers_audio_ref` and transcribes voice answers with the verbatim adapter; `episode.manifest` republishes reach the stream through a `NOTIFY` the publisher issues; the cover is `{title, cast, color}` and nothing is generated for it; the three name respelling candidates of its 4.8 are rendered as clips reachable from `OnboardingDoc.name.candidates[]` and `PUT /onboarding/name` writes `voice_casting.name` (its ask of this domain, "say it differently").
3. **Live call and voice stack (03).** The call screen implements its 4.11 (audio contract) and 4.12 (data-channel protocol) inside this document's `/call/[episodeId]` route, including its Media Session mapping while the call owns the handlers (4.4.7); `POST /v1/calls` returns `planning_words[]` from the brief; `ui.fact_card`, `ui.caption`, `ui.talkback`, `ui.crisis`, `ui.fallback_required` and `ui.ended` are rendered here; the voice-note fallback posts to its endpoints with a 90 s cap; `feed_to_call_ms` is measured here and reported as `client_perf`; the Salma onboarding call starts from `POST /onboarding/start` with the pre-account session; its verbatim and pronunciation adapters accept both `audio/mp4` (Safari) and `audio/webm;codecs=opus` (Chrome) uploads from `MediaRecorder` for voice notes, say it once, shadow and the then-and-now parts.
4. **Learner model, event log and data platform (04).** The registry accepts four new types `app_open`, `pwa_install`, `client_perf`, `push_permission` (payloads in 4.14) and the `door` value `today` (its table already uses it for `idea_chosen` and `swap`; its enum list should add it); `play.surface = "feed"` is never emitted by this domain in the beta (D6); `mark.clip_media_object_id` may be null and the notebook plays marks by Range on the episode file; `X-Forone-Replay: 1` with original timestamps on queue replays; `fact_card_viewed {dwell_ms, visit_id}` is sent from the notebook; `claim_shown` and `note_shown` are sent when rendered; `consent_change` events are how Controls writes `consents` (and `PUT /controls` is a convenience that appends them); `recording` events carry `task ∈ {retell, opinion, repeat}` with `kept_explicitly`; the notebook documents are its 4.3.9 views and `notebook_counts` are the only numbers shown; `X-Forone-LM-Version` carries its integer version; `learners.status` includes `trial_ended` for the 90-day state; the export passphrase of its 4.12.1 is returned once by `POST /v1/me/export` and shown in Controls, never emailed.
5. **Assessment engine, after-session pass and claim gate (05).** `NotesDoc` (4.3) is what stage 1 writes, with `ClipRef`s that the media route can serve by `media_object_id` and Range, and the signature line in `signature_ar`; `notes.ready` is notified to the stream; the weekly proof is an `episodes` row of `kind: proof` and `ProofDoc` carries `claims[]` with `evidence` openable as clips or sentences, `more[]`, `rhythm_line`, `next_focus`, `working_on[]` and the worth-it question; `RecordingDoc` for the then-and-now task (story audio, opinion prompt, eight sentences) comes from the package through its 4.10; the "how much did you follow?" ask flag is set on `EpisodeDoc` by its measures; a crisis detected after the session reaches Today as `TodayDoc.crisis_resources {show_once: true}` through `today.changed {reason: crisis}`.
6. **Security, privacy, consent and compliance (07).** The feed-link limited session (D7) and the install handoff token (D10) are accepted or amended; the consent copy for A9 and Controls is theirs and shown by `text_shown_version`; Vercel (edge logs with IPs, EU/US) and Resend are approved processors or replaced; Sentry scrubbing as in 4.14 is sufficient; the sample share page (public audio with the person's first name, 30 days) is acceptable; `forone_d` device cookie and IP-hash rate limiting are acceptable under PDPL; produced audio may later move under a service key for CDN caching; the crisis resources card content per country is the package's and counsel-reviewed.
7. **Cost model, vendor strategy and tracing (08).** Media egress, the feed MP3 encode and Vercel are reported under the "proof share and hosting" line; `client_perf` values are not vendor calls and stay out of `vendor_calls`.
8. **Evaluation, observability and operations (09).** Better Stack watches `app.forone.app`, `api.forone.app/v1/health` and `api.forone.app/f/health.xml` (a synthetic feed); the 16.2 measures "unprompted return", "feed-to-call handoff", "calls abandoned on the move" and "time to first sound" are computed from `app_open`, `client_perf` and the live-call domain's `end_reason`; the weekly `feed_fetches` by `ua_family` report answers Part 18 #11; the device test matrix of week 3 is in their runbook.
9. **Payments (business domain or topology 9.9).** Hosted checkout returns to `/controls?billing=done`; webhooks set `learners.status`; the day-7 ask and the day-6 email are driven by `trial_started_at`; the Stripe scaffold is replaced on 2026-11-16 without a client change beyond the Apple Pay domain file.

---

## 10. Open for Muath

1. **[OPEN for Muath] The brand domain, by 2026-11-02.** `forone.app` is a placeholder in every document. Cookies, VAPID subject, the Apple Services ID, Google OAuth verification, the Apple relay email registration and the feed URLs all bind to it in week 1; changing it later costs a day and re-subscribing every learner's feed.
2. **[OPEN for Muath] Apple Developer Program ($99 a year) and Google Cloud OAuth verification, started by 2026-11-09.** Both take days to approve, and Apple's "Sign in with Apple for Email Communication" registration for the sending domain is part of the same setup (without it, codes and receipts to Apple-relay addresses bounce). If either slips, 2026-12-07 ships with the email code only and the two buttons appear in the beta (P1). The founding cohort is invited by hand, so the cost is one extra step at A9, not lost learners.
3. **[OPEN for Muath] Which three podcast apps A10 names.** This design prepares instructions for Apple Podcasts, Pocket Casts and Podcast Addict (Android). Spotify and YouTube Music do not accept private feeds and are named as "not supported" on the card. Confirm the three, or name the apps the Milestone 0 day-14 survey shows your learners use; the week-3 test on those three decides `feed.enclosure_format`.
4. **[OPEN for Muath] The feed-link session (D7).** A forwarded feed link lets its holder start that episode's call and read the chat as the learner, until the link is reset in Controls. The alternative is sign-in before every call from the feed, which weakens the handoff 19.3 watches. Accept the limited session, or require sign-in.
5. **[OPEN for Muath] Digits and type.** Western digits (0 to 9) and IBM Plex Sans Arabic with IBM Plex Sans are this document's defaults. Both are brand calls; changing the font is a day, changing the digits is an hour, both before week 2.
6. **[OPEN for Muath] "Plays the feed" (PRD-v2 3.8.3).** This design does not treat a feed download as a play (D6), so a learner who only listens through the podcast app sees the return episode when they next open the app or tap a feed link, not when the podcast app fetches. Confirm the deviation or ask for the fragile version (a Range fetch past 50% of the file by a non-auto-downloading app counts), which this document advises against.
7. **[OPEN for Muath] The public sample share page.** The share page plays the sample (which says the person's first name) to anyone with the link for 30 days, with a WhatsApp preview. It is what "the sample is theirs to keep and forward" needs; confirm with counsel that a first name in a public audio file is fine, or make the page require the sender's device cookie (which kills forwarding).
8. **[OPEN for Muath] Vercel and Resend as processors under PDPL.** Vercel serves the shell and keeps request logs (IP addresses) outside the GCC; Resend holds email addresses. Approve, or name replacements (Cloudflare Pages or static hosting on S3 and CloudFront in `me-central-1` for the shell, about three engineer-days; Amazon SES for email, one day).
9. **[OPEN for Muath] The day-7 payment card on Today.** PRD-v2 0.1 row 8 says payment is asked once, plainly, on day 7. This design shows Salma's sentence and the plans as a card above the hero on day 7 until answered, and never blocks the episode. Confirm the placement, and what happens on day 8 to 90 (this design: the card stays, quietly, under the hero).
10. **[OPEN for Muath] One engineer or two.** Section 7 lists seven cuts in order. If the team is one engineer on 2026-11-02, cuts 1 to 3 are taken on that day.
11. **[OPEN for Muath] Device test budget.** About $40 a month for BrowserStack and two physical test phones (one iPhone on iOS 18, one Android on 14) for weeks 2 to 5. Approve or the suite becomes the manual checklist (cut 7).
