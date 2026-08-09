# Review B — Canon conformance

Reviewer B. Review set: `docs/specs/01`–`08` + `09-adrs/*`, against `00-decisions.md` (binding), `docs/For_one_Design_System_and_UI_Specification.md` (design authority, read in full, 2367 lines), and the production-doc standard.

I authored none of these documents and changed none of them.

**Totals: 18 defects — 3 High · 6 Medium · 9 Low.**

---

## Defect register

| ID | Sev | Doc + section | Verbatim quote | Why it violates canon | Which document changes |
|---|---|---|---|---|---|
| RB-01 | **High** | `05-tdd.md` §6.4 (line 1042) vs `06-data-api-spec.md` §11.6 EP-23 (line 2316) | 05: "**Decision: the client polls `GET /api/v1/sessions/{id}/state`.** … Server-sent events were rejected for v1 because they hold a serverless invocation open for the entire wait and buy nothing over a sub-10 ms Redis read". 06: "**One Server-Sent Events channel per session**, carrying generation readiness, After-show host replies, and voice-note replies. … SSE is chosen over polling" | Two documents specify contradictory, mutually exclusive client↔server progress mechanisms, each with a rejection rationale naming the other. 00 §4's one-path rule and 00 §3's "No library may introduce a second way to do something this table covers" are both breached; 06 additionally provisions the SSE path with a real rate-limit class (`RL-SSE`, 10 concurrent/user, 06 line 2043), `maxDuration = 120`, `Last-Event-ID` reconnect and a Redis pub/sub publisher, so this is not stray prose — it is a fully specified second path. Neither cites an ADR. | 05 or 06 — the lead must pick one channel and record it as an ADR; the loser deletes its section |
| RB-02 | **High** | `05-tdd.md` §6.4 (line 1042) | "the client polls `GET /api/v1/sessions/{id}/state`. The endpoint reads `session:{sessionId}:runtime` and `gen:{episodeId}:state` from Redis, falls back to Postgres on a miss, and returns an ETag" | 05 defines an endpoint, its payload sources, its caching semantics and a four-tier poll cadence (1 s / 3 s / 10 s / suspended). 00 §12 makes **06** the sole owner of "endpoints"; 00 §2 requires every endpoint to carry an `EP-##` under the `/api/v1/<kebab>` scheme. `/api/v1/sessions/{id}/state` appears **nowhere** in 06's catalog (§11.2–§11.13) — the nearest is EP-17 `GET /api/v1/sessions/{sessionId}`. 05 references no `EP-*` ID anywhere in the document. | 05 (cite EP-17 or an added EP-## rather than inventing a path); 06 if a new endpoint is genuinely wanted |
| RB-03 | **High** | `04-srs.md` FR-110 (lines 655–659) | "The waiting state MUST update at least every 5 seconds **[decided here]** … *Edges:* **offline** — the waiting state MUST state that the connection is lost and MUST resume **polling** on reconnection." | 04 makes polling and a 5-second floor **normative**, which contradicts 06's push channel (sub-second by design) and 05's 1 s/3 s/10 s cadence. Three documents give three different answers to one question, and 04's version is the one written as a MUST. 00 §12 gives 04 "FR-###/NFR-## with exact limits" but the transport is 06's lane; the interval is stamped `[decided here]` in a document that does not own it. | 04 (drop the transport verb and cite the owner); resolves with RB-01 |
| RB-04 | Medium | `08-eval-testing-plan.md` §2.3 (lines 125–133) | "`unit` \| **Vitest**, node environment, no I/O … `e2e` \| **Playwright** against `next build && next start` … `load` \| **k6** against a dedicated pre-production stack … `a11y` \| **axe-core** inside Playwright" | Four technologies are pinned that appear in **no** row of 00 §3's stack table and in **no** ADR. 00 §3 closes with "Exact patch versions freeze in the lockfile at scaffold; majors/minors above are binding," which presumes the table is the complete list. 05 owns "environments & delivery" and CI/CD per 00 §12 and names none of these tools, so 08 is unilaterally pinning stack in a lane it does not own. The likeliest correct fix is a new 00 §3 row, not a change to 08. | 00 (add a Testing row); 08 cites it |
| RB-05 | Medium | `05-tdd.md` §5.3.3 (line 698) | "**Decision: segment-manifest progressive playback, followed by a concatenated master.** No HLS packaging, no Media Source Extensions." | A genuinely contested media-delivery architecture with two named rejected alternatives, chosen inside a spec with no ADR. This is not routine engineering — it determines the player contract, the storage layout, the retry granularity and the offline/export story, and 00 §13 closes with "Authors may add ADRs". Compare ADR-0010 (pre-computed vs on-demand definitions), which is a strictly smaller decision and did get one. | 09-adrs (new ADR); 05 cites it |
| RB-06 | Medium | `06-data-api-spec.md` §11.6 EP-23 (line 2318) | "SSE is chosen over polling because the three things this channel reports are all 'arrives when it arrives' with sub-second value" | Same ADR-discipline breach as RB-05, and the counterpart to RB-01: a contested transport choice with an explicit rejected alternative, decided in a spec, no ADR. | 09-adrs; 06 cites it |
| RB-07 | Medium | `02-ux-spec.md` Appendix A copy catalog, throughout | 02 contains **0** occurrences of `’ “ ”` against the authority's 485 (65 × `’`, 210 × `“`, 210 × `”`). Authority line 1857 `That’s the show.` → COPY-165 `That's the show.` | 00 §9.2 requires "the design doc's copy adopted verbatim" and 00 §9.3 authorises exactly four deltas, none of which is typographic normalisation. Roughly 14 strings tagged `[source]` deviate: COPY-034, 070, 077, 083, 157, 165, 170, 327 and the host-boundary lines at 02:1937–1939. Em dashes, `…`, `·` and `é` were all preserved, so this is a deliberate ASCII pass, not encoding loss — which means the shipped apostrophe in the product's closing line is now straight. | 02 (restore curly punctuation in the catalog, or 00 §9.3 gains a fifth delta authorising ASCII copy) |
| RB-08 | Medium | `02-ux-spec.md` COPY-078 | Authority line 1862: `Starting this episode will end “{title}” early.` · 02 COPY-078 `[source]`: "Starting this episode will end the other one early." | The `{title}` token is dropped, so the conflict dialog no longer names the episode it will end. The authority is self-inconsistent here (its table row at 1862 disagrees with its own inline block at 1380); 02 silently adopted the inline variant under a `[source]` tag with no reconciliation note. Under 00 §9.2 a divergence between two authority passages is a decision, and an undocumented decision inside a verbatim-adoption mandate is a defect. The design authority's own destructive-action rule — "Destructive labels name the result" (line 2173) — favours the variant that was dropped. | 02 (adopt the `{title}` form or record why not) |
| RB-09 | Medium | `03-design-system.md` §5.10 (lines 422–426) | "## 5.10 Token governance — Three tiers only … **A new primitive requires an ADR.** A new component token requires a named component in §6." | An entire normative governance section with no counterpart anywhere in the design authority. 00 §9.3 states the four deltas are "the only permitted changes" and 00 §9.2 that "Neither may alter an adopted value without an ADR." The content is sound and I would keep it, but it is unauthorised as written: it also creates a *new ADR trigger* (primitive additions) that 00 §13 does not know about. | 00 §9.3 (authorise) or 09-adrs |
| RB-10 | Low | `02-ux-spec.md` Appendix B.2 (line 2284) | Authority line 1820 Avoid list: "… magic, **personalised experience**, congratulations, great job." | `personalised experience` is the one term from the authority's Avoid list absent from Appendix B. Appendix B declares itself "the single normative list cited by the design QA gates … and by every copy review", and 07 §12.4 layer 2 runs "a normalised token scan … against the banned-lexicon catalogue owned by 02" — so a term outside Appendix B is a term the automated scan cannot catch. The concept survives as prose at 02:1892, which is not the list. | 02 |
| RB-11 | Low | `02-ux-spec.md` COPY-024 | Authority table line 1833: "We sent a **link** to {email}." · Authority inline line 824: "We sent a **verification link** to name@example.com." · COPY-024 `[source]`: "verification link" | Same authority self-contradiction as RB-08, same missing reconciliation note. Lower stakes than RB-08 because no token is lost. | 02 |
| RB-12 | Low | `03-design-system.md` §6.1 rule 7 (line 438) | "7. Every component declares its environment support (Paper, Booth, Proof). A component used in Booth MUST be verified against Booth focus and contrast tokens." | The authority has exactly six component rules (lines 597–602). A seventh normative rule is added outside the four deltas. Substantively correct and worth keeping; unauthorised as written. | 00 §9.3 or 03 |
| RB-13 | Low | `03-design-system.md` §5.4.1 (line 294) | Authority line 465: "Noto Sans Mono for timecodes, **token examples**, and technical documentation only." · 03: "restricted to timecodes and technical documentation" | Silent narrowing of an adopted rule inside an otherwise verbatim typeface table. | 03 |
| RB-14 | Low | `03-design-system.md` §10.2 mirroring table (line 1353) | Authority line 1921: "**Follow media semantics documented in help;** physical Left decreases time, Right increases time" · 03 keeps only the second clause | The dropped clause is the accessibility obligation (document the semantics in help), not decoration. Row is otherwise reproduced verbatim. | 03 |
| RB-15 | Low | `03-design-system.md` §7.4 (line 1196) | Authority line 1697 forbids animation on "**Completion celebration**." · 03: "completion." | Broadens the prohibition from *celebratory* animation on completion to all animation on completion. Directionally safe, but it is an altered adopted value. | 03 |
| RB-16 | Low | `03-design-system.md` §9.3 (line 1302) | Authority line 1613: "760 px stage; extra room for status/disclosure **rail**" · 03: "760 px stage with room for status and disclosure" | The named layout element (rail) is dropped from a reproduced responsive table. | 03 |
| RB-17 | Low | `02-ux-spec.md` — authority line 1838 | "Karim watched the derby and has one terrible idea about Saturday's lineup." | The only row of the authority's "Example interface copy" table with no COPY id and no omission note in 02. Defensible as an illustrative pitch rather than a shipped string, but 00 §9.2's verbatim-adoption mandate makes a silent drop a defect; one line in Appendix A stating it is illustrative would close it. | 02 |
| RB-18 | Low | `02-ux-spec.md` §Appendix D | The authority's `## Paused and resumed sessions` section (line 1353) has no `SCR-##` | 00 §9.3 delta 2 requires an ID overlay so screens are traceable. The behaviour is correctly decomposed into SCR-06 (S6 resume band, S9 conflict, COPY-070…082) rather than invented as a screen — that is the right call — but 02 records no mapping note, so a reader diffing the authority section-by-section finds no anchor. | 02 |

---

## Per-check verdict

### 1. Stack conformance — **DEFECT** (RB-01, RB-02, RB-04)

Clean on providers: I grepped ~70 off-stack product names (Prisma, tRPC, GraphQL, Sentry, Datadog, Stripe, Firebase, Auth0, SendGrid, Deepgram, Whisper, BullMQ, Kafka, Inngest, Pinecone, Yup/Joi/Valibot/Ajv, Redux/Zustand, styled-components/MUI/shadcn/Radix, Prometheus/OTel, …) across 01–08. **Zero** hits outside 00 §3 or an ADR's rejected-alternatives list. Zod is the only validation library named. Server actions are prohibited in three places (00 §4, 05:95, ADR-0005) and asserted nowhere as permitted. No client-side Supabase access anywhere. 01 and 02 name no technology at all; 03 names Tailwind exactly once (§5.10), consistent with 00 §3's own "Tailwind CSS mapped to the design-doc tokens" — not a defect.

Model IDs cross-check against 00 §3 and 07 §2 cleanly. Every LLM identifier is OpenRouter-namespaced; `eleven_multilingual_v2`, `eleven_flash_v2_5`, `scribe_v2`, `scribe_v2_realtime`, `text-embedding-3-small`/1536 all match their pins in every document. The two off-pin identifiers in 07 (`scribe_v1` at 07:139 and 07:2743, `eleven_turbo_v2_5` at 07:139) appear **only** inside ADR-0019 resolution notes explaining that they are delisted or deprecated and unused — legal, and good practice.

The failures are structural, not vendor: two contradictory realtime-progress paths (RB-01), an endpoint invented outside 06's catalog (RB-02), and test tooling pinned outside 00 §3 (RB-04).

### 2. Product-law scan — **CLEAN**

All nine laws hold across all nine documents.

- **(a) No levels/CEFR/lesson furniture on any surface.** `level_band` / `level_step` / `level_confidence` appear only in 06's table DDL (lines 504–505, 1271–1272), the enum definition (427), the 06 §2 derivation map, 04 FR-016/017/018, and 07's assessment prompts. I read all 13 response schemas in 06 §11.2–§11.13 and **no API response contains any of the three fields**; TC-0018 asserts this mechanically and TC-1164 is a negative test that tries to add one. 05:928 explicitly excludes them from the export bundle. 07 §12.4's structural argument is the strongest form of this control: "content-authoring prompts receive `{difficulty_descriptor}` … and **never a band letter**. … A band letter cannot leak into an episode because it was never in the prompt that wrote it." 02's copy catalog and Appendix B are clean (one Low gap, RB-10). 07's `BLK-laws` item 1 enumerates the banned classes and 07 §12.4 correctly declares 02 the owner and itself the enforcer across three layers (prompt naming → deterministic token scan against 02's catalogue → semantic judge). `BLK-laws` being a subset of Appendix B is by design, not a gap.
- **(b) Recast-only correction.** Consistent in every host-behaviour description I found: 00 laws 5/7, 01 F-41/F-38 ("Unsolicited explicit correction MUST NOT occur, ever, in any stage, in any surface"), 02:316 host voice, 04 FR-444 (four clauses) and FR-448, 05:815 ("the agent adds no per-turn correction logic and never grades or praises"), 07 `BLK-laws` item 3 and `PRM-callin-brief` item 4, ADR-0015. No document describes explicit in-flow correction.
- **(c) No re-engagement.** Email scope is exactly the four transactional types in 00 §1, 01 F-53, 02:2242, 04 FR-629, 06 §13.4, 08 TC-0629. 01:936 and 04:3344 both state the closed set as a MUST NOT. `BLK-laws` item 6 bans the host-side equivalent. Appendix B.3 bans the construct. No push notifications, no notification centre, no digest anywhere.
- **(d) Session self-containment.** 00 law 3 → 01:76, 01:922 (the strongest statement: the return greeting "MUST NOT reference the length of the absence as a reproach, MUST NOT ask where they were, and MUST NOT mention anything missed"). Only memory persists; 06's entity census keeps per-session rows session-scoped.
- **(e) Trust-contract honesty.** Fabricated wins are prohibited structurally, not just textually: `INV-PROOF-1` (05:371), `INV-JOB-4` (05:1138, `proofs.assessment_id` makes the assessment a hard FK precondition), 06:1361, 04 FR-506, 02 §7.6 and COPY-170/171. Uncertainty is never asserted: `BLK-laws` item 4 ("Never infer a fact and state it"), the `speakable` generated column with a repository-level filter (08:112), confidence values never rendered.

### 3. Banned normative words — **CLEAN**

Grep counts per document (`TBD` / `for example` / `such as` / `could` / `or similar` / `etc.`):

| Doc | TBD | for example | such as | could | or similar | etc. | Verdict |
|---|---|---|---|---|---|---|---|
| 00 | 1 | 1 | 1 | 1 | 1 | 1 | all six in the §7 rule statement itself |
| 01 | 0 | 0 | 0 | 0 | 0 | 0 | clean |
| 02 | 1 | 1 | 1 | 10 | 1 | 1 | 4 in the §Normative-language declaration; 6 × "could not" inside COPY-027/108/261 and their state tables |
| 03 | 0 | 0 | 0 | 0 | 0 | 0 | clean |
| 04 | 1 | 1 | 1 | 1 | 1 | 1 | all six in the §Normative-language rule statement |
| 05 | 0 | 0 | 0 | 2 | 0 | 0 | both quoting COPY-108 in failure tables |
| 06 | 0 | 0 | 0 | 0 | 0 | 0 | clean |
| 07 | 0 | 0 | 0 | 1 | 0 | 0 | quoting COPY-108 in the F-07 failure row |
| 08 | 1 | 1 | 1 | 3 | 1 | 1 | 4 in the §Normative-language rule; 2 quoting COPY-108 |

**No violation in any requirement statement, schema, contract, or procedure step.** Every `could` is the failure-voice string "could not" inside quoted user-facing copy — legal under the stated judgment rule. 02:11 and 04:16 pre-declare the exemption and 02:11 names the three exact COPY ids, which is exactly the discipline the rule wants. 07's twenty verbatim prompt texts are content and contain none of the six in normative framing regardless.

### 4. Design-doc fidelity — **DEFECT** (RB-07, RB-08, RB-09, RB-11 through RB-18)

**Values (03): flawless.** 108 values compared, **zero mismatches** — see inventory below. Every hex, easing string, duration, z-index, shadow rgba, type-scale pair and breakpoint reproduces byte-for-byte. This is the strongest part of the review set.

**Copy (02): 52 strings compared, 2 substantive mismatches + 1 systematic punctuation regression + 1 omission** (RB-07, RB-08, RB-11, RB-17). Notably, no string was found reworded and hidden under a `[new]` tag — the provenance tagging is honest. The two full consent/revocation blocks (authority 897–901 and 1557–1561) reproduce word for word.

**Defects are rule-level, not value-level** (RB-09, RB-12 through RB-16): 03 adds three normative rules and narrows four adopted ones. None changes a number; all fall outside the four permitted deltas.

**All four deltas ARE applied, and applied well:**

1. **Export & deletion exist.** SCR-25 Account essentials (02:1598, 8 states), SCR-26 Export my data (02:1642, 11 states), SCR-27 Delete my account (02:1744, 10 states). Export covers the async job, the `export-ready` `DS-SystemBanner`, the transactional email (COPY-245/246) and the signed 7-day link with the expiry date surfaced (COPY-238). Deletion covers type-to-confirm against a localised word, the six-item consequence list (COPY-248…252), "**This cannot be undone.**", the 24 h primary purge and 30-day backup age-out both stated, immediate sign-out (COPY-260) and the confirmation email (COPY-264/265). The safe action is first.
2. **Superseded language is gone.** `not designed here`: 0 hits. `known gap`: 0 hits. The QA-gate line "Does any control claim export/deletion functionality not supported by v1?": 0 hits. The strings "Unsupported data actions" and "Unsupported deletion copy" survive in exactly two places — 02:1606 and 03:64–72 — both of which are supersession notes that name the passages in order to retire them ("MUST NOT be applied"). 03 §1.6 also retires the authority's "Source authority and one explicit v1 trust gap" paragraph explicitly. The replacement gate line is at 03 §14.4 and is routed to SCR-25/26/27 by 08:1612.
3. **SCR/DS IDs exist.** 27 screens, 273 states, full `## SCR-nn — Name` body for each, plus Appendix C (screen→component matrix) and Appendix D. Every one of the authority's 16 core-screen sections maps to at least one SCR; the single unmapped section is "Paused and resumed sessions", correctly decomposed rather than invented as a screen (RB-18 is the missing note, not a missing screen).
4. **One consolidated banned lexicon.** 02 Appendix B (line 2246), declaring itself "the single normative list", with Scope (meaning not spelling; all surfaces, all languages), Enforcement, B.1 Learning furniture (21 rows), B.2 System terms, B.3 Interface constructs, B.4 Preferred vocabulary (authority's Prefer list verbatim), B.5 Permitted-but-mistakable carve-outs. 17 of the authority's 18 Avoid terms present (RB-10 is the 18th); the entire model/agent/LLM/pipeline/CEFR list present; the "AI host" carve-out preserved.
5. **Dormancy sentence.** 02:1488 COPY-209 `[new — §9.3 delta 4]`: "To remove everything permanently, delete your account from Account essentials." — exactly one added sentence, with placement rules at 02:1494 forbidding attachment to individual statements or destructive styling. "Stop using this in the show" (COPY-207) preserved verbatim, and 02:1465 keeps the honest-wording constraint.

### 5. ADR discipline — **DEFECT** (RB-05, RB-06; RB-09 and RB-12 adjacent)

**Register complete.** All 19 ADRs in 00 §13 exist as files. Every one carries Status, Context, Decision, Alternatives and Consequences — verified mechanically, 19/19 on all five headings. No spec references an ADR number outside the register (`ADR-0001`…`ADR-0019` and nothing else). No spec contradicts an accepted ADR: I checked ADR-0005 (REST/no server actions), ADR-0012 (no client DB), ADR-0013 (PostHog sole tool), ADR-0017 (public catalog narrowing the signed-URL rule), ADR-0018 (scanner role narrowing the scoped-repository rule) and ADR-0019 (Scribe v2) against 05/06/07 — all consistent, and the two narrowing ADRs are cited at both the broad rule and the exception.

**Missing ADRs for two contested choices** (RB-05, RB-06). I applied the judgment filter and deliberately did **not** flag: 05:108 (npm package layout / no Turborepo), 05:1040 (the poll endpoint mechanics — that is RB-01/RB-02, a contradiction rather than a missing ADR), 06:2767 (`fil` over `tl`, `no` over `nb` — routine and well-argued in place), and 08's ~20 `decided here` thresholds, which are 08's own lane under 00 §12 and are collected in its Appendix A for ratification, which is the right pattern.

### 6. Ownership-map conformance — **DEFECT** (RB-02, RB-03, RB-04; RB-09 minor)

Lane discipline is otherwise strong and the one-source-of-truth rule is followed unusually well:

- 03 defines **zero** `COPY-*` strings; 02 contains **zero** hex values. The 02/03 split holds exactly.
- 01 and 02 name no technology.
- Cross-document restatements cite their owner. Every occurrence of the `$1.50` / `$2.50` envelope in 04, 05, 06, 07 and 08 carries a `00 §8` citation or is an explicitly derived measurement point. The session cap cites `00 §1` at 06:926 and 07:2562. Latency budgets cite `00 §8` at 05:589, 05:741 and 07:2453.
- 05:524 is the model case: "**Membership of the view set is owned by 06 §7.4 and is not restated here** (`00` one-source-of-truth rule) … 05 never introduces one."
- 07 §12.4 correctly splits ownership of the banned lexicon (02 owns the list, 07 owns enforcement).

The breaches are RB-02 (05 defines an endpoint), RB-03 (04 fixes a transport and interval it does not own), RB-04 (08 pins stack), and marginally RB-09 (03 creates a new ADR trigger, which is 00's lane).

---

## Sampling inventories

### 03 vs design authority — 108 values compared, 0 mismatches

- **26 colour primitives**, all: `paper-0/50/100/200/300`, `ink-950/800/650/550`, `broadcast-700/400`, `petrol-700/800`, `proof-700/100`, `booth-950/900/800/650/text/muted`, `focus-600/300`, `success-700`, `warning-800`, `error-700`.
- **15 semantic tokens** across both environments, including the raw values `#A9A39A`, `#F07A5B`, `#40302B`, `#8B867E`, `#777A7A`, `#E8E1D6`, `#252728`, `rgba(23,23,22,.55)`, `rgba(0,0,0,.70)`; plus the <10% brand-colour budget.
- **11 Booth CSS overrides** and the four component tokens `--pitch-lead-title-size: clamp(2.5rem, 4vw, 3.5rem)`, `--player-control-size: 3.25rem`, `--definition-max-width: 22rem`, `--compact-player-height: 4.5rem`.
- **6 host accents**: Ochre `#8D5D16`, Teal `#2F6662`, Plum `#744C63`, Slate blue `#3F5F7A`, Rust `#914735`, Olive `#5E6531`; 3 px rule.
- **6 contrast claims**: 16:1, 5.4:1, 5.5:1, 4.5:1/3:1/3:1, focus ring 2+2 px Paper / 3 px Booth.
- **Spacing/sizing**: base 4 px and the 10-step production scale; the 20/40 optical exception; `space-1…32`; `radius-0…5` + `round:999`; `border-hairline/strong/live` 1/2/3 px; `control-sm/md/lg/call` 36/44/52/64; touch 44 min / 48 preferred; icons 16/20/24/28; scrubber 4 px track / 20 px thumb / 24 px dragging / 44 px hit; transcript 760; article 680 default / 720 max; programme 1320.
- **7 shape radii**: buttons 8, inputs 6, sheets 16, popover 8 + 1 px border, compact player 12, host marks 4, divider 1.
- **3 shadows verbatim**: `0 8px 28px rgba(23,23,22,.16)`, `0 16px 48px rgba(23,23,22,.22)`, `0 6px 24px rgba(23,23,22,.18)`.
- **6 z-indexes**: 0 / 20 / 40 / 60 / 80 / 100.
- **5 motion tokens with exact easing strings**: 80 ms linear · 140 ms `cubic-bezier(.2,.0,.2,1)` · 220 ms `cubic-bezier(.2,.0,0,1)` · 320 ms `cubic-bezier(.16,1,.3,1)` · 420 ms max `cubic-bezier(.16,1,.3,1)`; plus the §7.3 standard/emphasis/exit easings and the 80 ms reduced-motion crossfade.
- **All 14 motion-hierarchy durations**: 80–140 · 220 · 320–420 · 220 · 280–340 · 80 · 140–220 · 320 · 320–420 · 100–160 · 320 · 160 · 220 · 260 ms.
- **All 11 type-scale roles**, desktop/mobile/weight: 56/58 & 40/43 · 48/51 & 36/40 · 36/40 & 30/35 · 28/34 & 24/30 · 20/26 & 19/25 · 19/31 & 18/29 · 18/30 & 17/28 (labels 13/18) · 16/24 · 14/20 · 12/16 · 13/18.
- **Typography rules**: `-0.02em`, 62–68 / 55–72 chars, 0.75 paragraph spacing, 3/4-line clamp, 70-char plate recompose, Arabic 1.55–1.7, CJK 1.8, 35% expansion.
- **4 grid rows + 7 breakpoint properties**: 4/8/12/12 cols; 20 (16 <360) / 32 / 48 / 64 px margins; 16/20/24/24 gaps; viewport/920/1248/1320; `--bp-*` 0/600/1024/1440; `--content-*` 1320/840/680.
- **Component numerics**: 352 px popover, 50vh, 70% sheet, 120 ms hover delay, 150 ms drift, 52/56/48 px player control, 44 px collapsed strip, 64 px call control + 28 px icon, 760 px call stage, 5 s/10 s scrubber keys, 140/28-char content caps, 30-char host names, 20 px titles + 24 px padding, 0.8×/1.0×, 10–15 s samples, 6 hosts, 3 annotations, 350-word subhead, 35% scroll, 48 h, 1–3→6 lines, 200% at 1280 px, 44×44/48, 1.75 px stroke, 56 px masthead + 12/8 px scroll thresholds, 56 px archive rows, 480–560 px trust sheet, 760/240 px intake, 600/640 px thread, buffering <500 ms / 500 ms–5 s / >5 s.

### 02 vs design authority — 52 copy strings compared

All 46 rows of the authority's "Example interface copy" table (lines 1828–1873), plus 24 inline-quoted strings: the start statement and disclosure (803, 808), under-18 line (832), verification notice (824), the full voice-consent panel (897–901), duo introduction (934), generation wait (953–954), partial readiness (956), notes handoff (1104–1105), call invitation (1200–1201), leave-the-line block (1270–1271), live-line failure (1279–1280), completion footer (1321–1322), archive empty (1464), cast-full block (1508), revocation block (1557–1561), conflict block (1379), flat week (1416), memory-correction echo (2152), intake resume (879), delayed note (1328), audio-removed (786/1721/2086), word-timing (1120), daily cap (1865).

Result: 45 MATCH · 2 substantive MISMATCH (RB-08, RB-11) · 1 omission (RB-17) · ~14 punctuation-only MISMATCH (RB-07, all the same cause).

---

## Verdict summary

| Check | Verdict |
|---|---|
| 1 · Stack conformance | **DEFECT** — RB-01, RB-02, RB-04 |
| 2 · Product-law scan (nine laws) | **CLEAN** |
| 3 · Banned normative words | **CLEAN** |
| 4 · Design-doc fidelity (02/03) | **DEFECT** — values perfect; RB-07…RB-09, RB-11…RB-18. All four deltas correctly applied |
| 5 · ADR discipline | **DEFECT** — register complete and well-formed; RB-05, RB-06 missing |
| 6 · Ownership-map conformance | **DEFECT** — RB-02, RB-03, RB-04 |

One structural observation for the lead beyond the register: RB-01/02/03 are a single fault with three faces. The client progress channel is the one place in the whole corpus where four documents (04, 05, 06, 08) failed to converge — 08 references no `EP-17` and no `EP-23` anywhere, so neither candidate path has a test, which is why the contradiction survived to review. Everything else in the review set that spans documents converges tightly.
