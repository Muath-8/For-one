# ADR-0011 — LiveKit Agents on Node, not Python

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §3, `05-tdd.md` §5.4

## Context

The call-in loop is the only latency-critical server path in the system, with a 1,500 ms end-to-end budget allocated across five hops. LiveKit Agents ships in two flavours: a Python SDK, which is the more mature of the two and the default in most reference material, and a Node SDK.

The agent is not a thin audio pipe. It needs the host personality document and host brief, a retrieved slice of the learner file, the recast policy, the session state machine's view of the call, consent state checked at write time, silence and close rules, and per-turn writes to `call_turns`. Every one of those is domain logic that already exists in `src/modules/*` and that must not exist twice — the standard names duplicated logic as a failure mode, and a divergence between the agent's recast policy and the pipeline's would be a product-law violation nobody would notice until a user heard it.

The rest of the stack is TypeScript with `strict: true` (`00` §3), and ADR-0004 puts all three runtimes in one repository sharing `src/modules`.

## Decision

**The voice agent is built on `@livekit/agents` 1.x in Node, deployed to LiveKit Cloud US East as `src/agent`, and imports the same domain modules as the web app and the task set.**

Composition: Silero VAD for endpointing, ElevenLabs Scribe streaming for STT, `MDL-realtime` through OpenRouter for the completion, and `eleven_flash_v2_5` for TTS — a component pipeline, not a single end-to-end speech model.

**Live recovery is single-path.** A verified user departure retains the same LiveKit room only for FR-204's durable reconnect grace; an in-grace return rejoins that room without a new opening, and expiry finalizes the Call-in into After-show. A persisted `speaking` pause is reserved for a failed, already-authorized degraded voice-note exchange and resumes that exchange rather than creating a fresh live room. Voice-note degradation is never user-selectable and is authorized only by FR-230's closed typed unavailable or recovery-exhausted causes; latency alone is not a cause.

## Alternatives considered

**Python LiveKit Agents.** The stronger SDK in isolation, and it lost on system-level cost. Choosing it means either reimplementing the host brief assembly, retrieval, recast policy, consent checks, and turn persistence in Python — two implementations of rules that must be identical — or having the agent call our own HTTP API per turn, which adds a network round trip inside a budget where 200 ms is already allocated to transport. It would also add a second language toolchain, a second dependency and security-scanning surface, and a second CI path to a team whose scarcest resource is operational surface area. Python's ML ecosystem advantage is irrelevant here, because every model call is a hosted provider API.

**Python agent calling our REST API for domain decisions.** Lost on latency and on the one-path rule. Each turn would add an authenticated HTTP hop to `/api/v1/*`, and the agent would become a client of an API designed for browsers, with its own auth mode and its own failure modes inside the real-time loop.

**A single end-to-end speech-to-speech model.** Lost on control and on the product's requirements. The recast policy, silence rules, the 5:30 close and 7:00 hard cut, mid-formulation protection, and per-turn transcript persistence all require inspecting and shaping each hop. An end-to-end model collapses those hops into an opaque one, makes per-hop latency attribution impossible, and removes the fallback points that `05-tdd.md` §5.4 depends on. It also breaks the "transcript always, audio only under consent" split, because the transcript would be a by-product rather than a first-class artifact.

**Building the loop directly on WebRTC without LiveKit Agents.** Lost because it means writing turn detection, barge-in, jitter handling, and worker dispatch ourselves — infrastructure the chosen stack already provides, against the standard's instruction to maximise native platform capability.

## Consequences

- One definition of every conversational rule. The agent imports `src/modules/realtime` and `src/modules/cast`; it holds no domain rules of its own, which `05-tdd.md` §2 states as a placement rule.
- The Node SDK trails the Python SDK in features and examples. Accepted, and mitigated by keeping the agent thin: the pipeline wiring, turn policy, and call clock are ours, and each provider sits behind a `src/platform/*` port, so a provider swap is local.
- Per-hop latency is measurable and attributable because the pipeline is composed of discrete hops. That is what makes the latency allocation owned by 05 §5.4 enforceable. Repeated latency breach may select the realtime fallback model, but latency alone MUST NOT enter voice notes. Voice-note degradation occurs only after one of FR-230's typed unavailable or exhausted/unrecoverable recovery causes is durably stored.
- A verified `participant_left` begins the durable reconnect grace owned by 05/06. Re-entry inside that grace rejoins the same room and preserves its transcript; expiry finalizes the Call-in and advances to After-show. The persisted provider event and reconciliation path make tab closure safe even when `room_finished` never arrives.
- The agent is a separate deployable with its own image and rollback path. Live calls on the old version complete; new rooms land on the new one.
- Node's single-threaded model means one slow synchronous operation blocks the event loop for every session on that worker. The agent MUST keep per-turn work asynchronous and off-thread, and worker sizing (8 concurrent sessions per 2 vCPU) leaves headroom for this.
- If the Node SDK later blocks a required capability, the fallback is not a rewrite in Python but a narrower agent plus a domain call — and the cost of that is already understood, because it was the alternative evaluated here.
