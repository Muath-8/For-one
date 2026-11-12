# For one — design documentation

Written 2026-11-06; revised 2026-11-12 for ADR-24 (07 records the decisions) and for ADR-25 (web only, one onboarding order, no founding lock, no Milestone 0 and no beta). Entry page (designed overview): https://claude.ai/artifact/BUsCfwipUW4zSj5PtcUeW3 (source: `for-one-design.html` in this folder).

| File | What it holds |
|---|---|
| 00-design-principles.md | The thesis, ten principles with tests, who is who on screen, the laws, departures from the UI/UX lens |
| 01-design-system.md | Character, tokens, type, layout, motion, voice identity, cover art, components, themes, accessibility, platform |
| tokens.css / tokens.json | The tokens (dark default, light theme), as CSS variables and as JSON |
| 02-information-architecture.md | The map, destinations, modes, navigation rules, the podcast feed, the web app on each surface, the first-session order, object model |
| 03-user-flows.md | First session, daily episode, the call, after-session, weekly proof, finale, subscribe, cancel, data deletion, return after a gap, small door, sample page |
| 04-screen-specs.md | Every screen with layout, components, states (empty, loading, error, offline), copy and what Salma or the hosts say |
| 05-interaction-and-audio-ux.md | Listening, speaking, turn-taking, latency masking, headphones and lock screen, hard moments, measures |
| 06-content-and-voice-guidelines.md | The hosts, Salma, interface copy, localisation, the proof's content rules |
| 07-open-questions.md | The design's open questions and how each was decided (ADR-24, ADR-25) |
| prototype/ | The clickable v2 prototype (not in the GitHub repo) |

Inputs: concept-v2.md, decisions.md, perspectives/ui-ux.md, perspectives/enjoyment-pull.md, perspectives/consistency-motivation.md, features/for-one-features.html, design/prototype/for-one-prototype.html.
