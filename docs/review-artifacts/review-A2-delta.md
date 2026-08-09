# Review A2 — Delta re-review of Reviewer A's scope (traceability & ID integrity)

Adversarial delta review. I authored none of these documents and edited none of them. Every verdict below is backed by an extracted ID set or a verbatim quote with `file:line`. Verified against current intent as ruled since the original report (EP-23 retired, EP-52/EP-53 added, AIF-01…18, 05 §8 = 47 rows, FR-711 → F-29, canonical job names, FR-101 owns both pitch caps, 05 §9.4 target-free, zero v1 flags, `master.mp3`, US-x.y narrative).

---

## Part 0 — Re-extracted inventories (post-fix evidence base)

| Inventory | Count | Result |
|---|---|---|
| `FR-###` defined in 04 | 248 | no dupes; **zero** FRs with an empty `*Traces:*` feature list |
| `NFR-##` defined in 04 | 33 | NFR-34–40 now labelled Reserved |
| `F-##` in 04 §6.1 | 55 | matches 01's F-01…F-55 |
| **04 §6.1 vs FR trace lines** | — | **exact inverse in both directions: 0 over-reported, 0 under-reported pairs** |
| `TC-####` in 08 | 570 defined + 4 range labels (`TC-0712`, `TC-0799`, `TC-0840`, `TC-1240`) | §14.9 bands expand to **exactly** the 570 defined; empty diff both ways |
| §14.9 band sum | 248+33+6+14+15+11+12+6+3+11+47+18+21+31+20+17+16+31+10 = **570** | matches stated total |
| `EP-##` in 06 | 52 (EP-01…EP-53, EP-23 absent) | every `EP-##` cited in 00/04/05/07/08 resolves |
| `PRM-*` in 07 | 20 | all 12 cited by 04 and all 20 cited by 08 resolve |
| `JOB-*` in 05 §7 | 31 | all 04/06/08 citations verbatim-canonical; **ADR-0001 is the sole offender** |
| `AIF-##` in 07 §11 | 18 | 08 cites AIF-01…AIF-18; zero bare `F-##` failure-row citations |
| `INV-*` in 05 §13 | 30 index rows covering 34 identifiers (`INV-JOB-1/2/3`, `INV-RUNTIME-1/2/3` grouped) | every `INV-*` cited in 00/05/08/ADR-0009 resolves |
| `SCR-##` in 02 | 27 · 273 states | all 66 `SCR-##(/S#)` citations in 04 resolve; Appendix D sums to 273 |
| `DS-*` | 51 | closed both directions against 02 |
| `COPY-###` | 277 | no dangling from any document |
| `ADR-####` | **21 files** (0020, 0021 added) | 21 register entries in 00 §13; zero dangling |
| `MDL-*` | 6 | no strays in 00/04/05/06/08 |
| `RL-*` in 06 §11.1 | 18 | one dangling reference (RA2-07) |
| `Q-*` in 06 §14 | 72 | all 4 external citations resolve |
| Cross-doc `NN §x.y` citations | **735** | 734 resolve; 1 does not (RA2-06). The 03 §8/§10/§12/§14 citations resolve to numbered subsection groups — 03 has no bare parent headings by design, not a defect. |
| Forbidden normative words | — | `TBD`, `for example`, `such as`, `or similar`, `etc.` appear **only** inside the rules that forbid them |
| Leftover strings | — | `SCR mapping` 0 · `JOB-intake-finalize` 0 · `full.mp3` 0 · `PRD Part` in 05/06 = 0 |
| `EP-23` | 6 sites in 06 + 3 in ADR-0020 | **all sanctioned**: 06 §11 opener (L2013), EP-53 note (L2318), EP-52 note (L2371), §11.14 retirement table (L2703, L2705), §17.1 (L3039), and ADR-0020's own history |

---

## Part 1 — Verification of RA-01 … RA-29

### RESOLVED (27)

| ID | Verdict | Evidence on disk |
|---|---|---|
| **RA-01** | RESOLVED | `06:1766` now reads "`SELECT` on the views enumerated in §7.4 and nothing else — membership is the enumeration, never a count (ADR-0018)". `06:3031` (§17.1) same wording. `ADR-0018:11,22,23` all say "enumerated in 06 §7.4", no count. The string "nine views" appears nowhere in the corpus. §7.4's own body still says "Eleven views" — that is the owner enumerating, which is exactly what D-04 permits. |
| **RA-02** | RESOLVED | `06` §5.5: `CHECK (kind <> 'created' OR cardinality(traits) BETWEEN 1 AND 4)` with the inline note "FR-304 collects 2–4 traits and caps at 4, but its failure rule completes a creation on **1** trait after a single conversational re-prompt; only zero traits blocks completion". Schema now matches FR-304 and `TC-0304`. |
| **RA-03** | RESOLVED | `01` §6: "Call-in participation \| ≥ 70% \| completed-or-abandoned sessions where `speaking` is absent from `skipped_stages` (every completed session passes through `speaking` under the adjacent-only state machine, so state arrival would always read 100%)". |
| **RA-04** | RESOLVED | `05` §9.4: "sessions where `speaking` is absent from `skipped_stages` ÷ sessions reaching a terminal state — `call_entered` arrival counting is dead per the D-01 adjacent-only ruling". `08:2107` records D-16 as **Resolved**. 01, 05, and `TC-1090` now agree. |
| **RA-05** | RESOLVED | 04's 12 prompt IDs are `PRM-article`, `-callin-brief`, `-chat-opener`, `-chat-turns`, `-episode-script`, `-error-extraction`, `-intake-producer`, `-level-estimate`, `-proof-script`, `-qa-gate`, `-realtime-host`, `-uptake`. All 12 ⊂ 07's 20. `PRM-producer-intake`, `-level-probe`, `-callin-host`, `-aftershow`, `-error-rater`, `-uptake-rater` appear nowhere. |
| **RA-06** | RESOLVED | 05 §8 subsection row counts are now **13 / 9 / 8 / 5 / 4 / 5 / 3 = 47**. §8.1 gained the publish row (`05:1147`: "Publish fails after synthesis: audio is uploaded but the `episodes` and `sessions` flip to playable does not commit"), which is what `TC-1012` tests. `08` §14.6 declares 13 for §8.1 and `TC-1136` (`08:1970`) expects "47 rows in 05 §8 and 18 in 07 §11". |
| **RA-07** | RESOLVED | Zero hits for "SCR mapping". `04` §1.3 rewritten: "Screen and state identifiers are owned by 02-ux-spec and are cited here, never coined here." 63 FR blocks carry a `*Screen:*` field; all 66 `SCR-##(/S#)` tokens resolve against 02's 27 screens and per-screen state counts. §6.4 no longer lists SCR assignment as an obligation to 02. |
| **RA-08** | RESOLVED | `08:1947` — "\| INV-JOB-4 \| TC-1156, TC-1171 \|" in §14.4. `TC-1156` is defined at `08:1360`. `TC-1188` (`08:1389`) now names INV-JOB-4 explicitly: "including `INV-JOB-4`, which is a distinct row from `INV-JOB-1/2/3`". |
| **RA-10** | RESOLVED | `06` §5.5: `quirk` and `backstory` are `text[]` with `cardinality <= 3`, plus `CHECK (cardinality(quirk) <= 3)` / `CHECK (cardinality(backstory) <= 3)` and the note "Both are arrays rather than scalars because the requirement counts elements; a single `text` column cannot express a counted cap." |
| **RA-11** | RESOLVED | Mechanical inverse check: **0** pairs in §6.1 that no FR trace line claims. |
| **RA-12** | RESOLVED | Mechanical inverse check: **0** pairs claimed by an FR trace line and missing from §6.1. Spot-verified F-04 (9 FRs), F-29 (7), F-30 (14), F-42 (15), F-51 (6), F-55 (4) — all exactly match the inverted trace-line set. |
| **RA-13** | RESOLVED | `04:3818` — FR-711 `*Traces:* F-29 · … *Feature home decided here:* … its home is F-29`. §6.1's F-29 row lists FR-711. §6.2 row: "FR-711 Ownership semantics \| F-29 (home decided in this document…)". Zero FRs now have an empty feature list. |
| **RA-14** | RESOLVED | 07 §11 rows are `AIF-01`…`AIF-18`. `08` §14.6 row reads "07 §11 AIF-01 – AIF-18". `TC-1050`–`TC-1067` each open with their `AIF-##`. No bare `F-##` failure-row citation survives in 08. |
| **RA-15** | RESOLVED | `01` F-30: "The salience scale, the fade mechanism, and the dormancy threshold are owned by 07-ai-spec §7.3–7.4… Confidence is three-valued — high, medium, low — stored per 06-data-api-spec §5.7 and gated per 07-ai-spec §7.2." Governing-laws line retargeted to 07 §7.3–7.4 / 06 §5.7. The weekly-decay-cadence sentence and the numeric confidence register are gone. |
| **RA-16** | RESOLVED (residual → RA2-05) | "PRD Part" now appears **zero** times in 05 and 06. The five named sites are retargeted: `06:848` "the 140-character cap from FR-101"; `06:916` "The 48-hour abandonment window, measured from creation (FR-206)"; `06:958` "the 3:00 floor and 8:00 ceiling (FR-210)"; `06:966` "the ≤2 law from FR-216, enforced at the column"; `06:996` "the outer envelope of FR-217's three level bands". 07 retains two `PRD Part` strings; one is rationale prose, one is a live cadence citation → RA2-05. |
| **RA-18** | RESOLVED | `08:1387` `TC-1186` now reads "for every job in the 05 §7 catalog. The job list is read from 05 §7 rather than restated here, so a job added to the catalog enters this test without a count to update." No count. |
| **RA-19** | RESOLVED | `03:615` "title (hard cap 140 characters, owned by FR-101)"; `03:626` "Title 140 characters (FR-101); format label 28 characters (FR-101)". `04` FR-101 statement 5 claims both: "This requirement owns both pitch-card text caps; no other document sets either value." Appendix A row 9 records the ruling. |
| **RA-20** | RESOLVED | `05` §9.4: "The target values are owned by 01 §6; the rows below give only the measurement expression over this taxonomy." Every one of the five rows now reads "(target owned by 01 §6)" and carries no number. |
| **RA-21** | RESOLVED | All four sites cite FR-206: `02:104`, `02:244`, `02:1171`, `03:582`, `03:603`. |
| **RA-22** | RESOLVED | `04` FR-611 statement 2: "The download MUST be a signed URL with the 7-day expiry owned by 00 §9.3 delta 1." |
| **RA-23** | RESOLVED | `00` §2 now registers `EP-##` (06), `COPY-###` (02 Appendix A), `INV-<AREA>-<n>` (05 §13), `Q-<KEBAB>` (06 §14), and `RL-<KEBAB>` (06 §11.1). |
| **RA-24** | RESOLVED | `07` §4.6 now injects `Length: {word_band} words`. The three bands `150–300 / 250–450 / 350–600` survive in exactly one normative place: `04:1253` FR-217. `06:996` cites FR-217 for the outer envelope. |
| **RA-25** | RESOLVED | `07:2643` — "The banned lexicon is owned by 02 as one catalogue (00 §9.3, delta 3)." `00` §9.3 item 3 is "Banned-lexicon consolidation". |
| **RA-26** | RESOLVED (as scoped) | `00:22` declares the rule: "Engineering documents (01–06, 08, 09) say **'user'**. **'Listener'** is reserved for 07's prompt texts and any content-facing register where the show's own voice speaks. Mixed usage within one document is a defect." 04 now contains **zero** occurrences of "listener" (was 8). The new rule creates fresh violations elsewhere → RA2-04. |
| **RA-27** | RESOLVED | `00:11` — "Internal stage names `listening` / `reading` / `speaking` / `chatting` appear only in engineering documents." The imperative forms Listen/Read/Speak/Chat are gone. |
| **RA-28** | RESOLVED | `04` §1.2 now has two rows: "NFR-01 – NFR-33 \| Non-functional requirements" and "NFR-34 – NFR-40 \| Reserved. Not allocated in v1. A new non-functional requirement MUST take the next unused number in this range." |
| **RA-29** | RESOLVED | `00` §2 closing line: "`US-x.y` user-story IDs are narrative aids inside 01; the binding chain is F → FR → TC, and no downstream document is required to cite a US ID." |

### NOT RESOLVED (2)

**RA-09 — NOT RESOLVED (1 of 4 owners outstanding).**
04 (11 job citations), 06 (`JOB-purge-voice-audio`), and 08 (10 citations) are now all verbatim-canonical against 05 §7's 31 names. `JOB-intake-finalize` is gone corpus-wide and `04` FR-014 was rewritten around the route-handler mechanism ("No intake-finalization job exists, and this document MUST NOT be read as requiring one"). `04` §6.4 now records the rule: "**From 05-tdd:** the `JOB-*` catalog in §7, whose names every job citation in this document uses verbatim." ADR-0018 is clean.

Still wrong: **`09-adrs/ADR-0001-data-rights-restored.md:26`** — "05-tdd designs **JOB-export** and **JOB-delete-user** including third-party propagation (Clerk, PostHog, Supabase Storage)." Neither name exists in 05 §7; the canonical names are `JOB-export-user-data` and `JOB-delete-account`. ADR-0001 was named as an owner in the original defect.

**RA-17 — NOT RESOLVED (2 of 3 owners outstanding).**
06 is fixed: `06:966` "`BETWEEN 0 AND 2` — the ≤2 law from FR-216, enforced at the column". 07's two sites are functional prompt text and the §13.2 threshold table, which the original report exempted.

Still uncited restatements of FR-216's value:
- `02:1898` — "**Permitted.** Using facts the user directly volunteered; **limiting an episode to two personal references**; …" No FR-216 citation. 02 contains zero occurrences of the string "FR-216".
- `05:675` — "**Gate A** … banned-lexicon law scan against the 02 catalog, **personal-reference count ≤ 2**, canon check against high-confidence facts only, target-language check." No FR-216 citation. 05 contains zero occurrences of "FR-216".

**Score: 27 resolved / 2 not resolved.**

---

## Part 2 — New defects found in the regression sweep

| ID | Sev | Where | What is wrong | Who changes |
|---|---|---|---|---|
| **RA2-01** | **High** | `05-tdd.md:1032–1055` (§6.5) vs `06-data-api-spec.md:1928–1940` (§9.1) | **The fix-round disclaimer was added but the restated material was left behind, and it contradicts its declared owner.** `05:1036` now states "Object paths and signed-URL TTLs are owned by 06 §9.1; **05 restates neither**." The same section then restates four object paths and one TTL: `05:1051` `catalog/{packageId}/{dialectId}/duo-intro.mp3`, `05:1052` `catalog/{packageId}/{dialectId}/samples/{voiceId}.mp3`, `05:1053` `catalog/{packageId}/{hostId}/signoff-{n}.mp3`, `05:1055` "**`exports` (private)** — `exports/{userId}/{exportJobId}.zip`, **7-day signed URL**". Worse, all of them **disagree with 06 §9.1**: 06's `catalog` key pattern is `dialects/{dialectCode}.mp3`, `voices/{voiceId}.mp3` — no `{packageId}` segment, no `duo-intro`/`signoff` objects at all — and 06's exports key is `u/{userId}/exports/{exportJobId}.zip`, not `exports/{userId}/…`. The bucket taxonomy also conflicts: `05:1032` says "**Three buckets**" and `05:1034` names a bucket **`media`**, while 06 §9.1 enumerates **eight** buckets (`episode-audio`, `proof-audio`, `call-audio`, `voice-notes`, `intake-audio`, `character-intros`, `exports`, `catalog`) and defines no bucket named `media`. An implementer following 05 provisions a bucket 06 does not have and writes objects at paths 06 does not recognise. Note the neighbouring fix landed correctly — `05:704` cites "the path 06 §9.1 fixes" for `master.mp3` — so this is the same edit applied unevenly. | **05** (delete the path/TTL tables and the three-bucket framing; cite 06 §9.1) |
| **RA2-02** | **High** | `08-eval-testing-plan.md:1323` (`TC-1064`) vs `05-tdd.md` §7 job table, `05-tdd.md` §8.4, `07-ai-spec.md` §11 AIF-15 | **Three documents give three different retry policies for one failure, and the test encodes a fourth reading.** 07's AIF-15 was correctly fixed to defer: "The pass **re-enqueues under the retry bound for that job in 05 §7**." 05 §7's `JOB-post-session` row declares "**3, exponential from 10 s**". 05 §8.4's matching row declares "Post-session and planner exceed the 10-minute window \| Elapsed measurement on the run \| **None**" (no retry) — and a *separate* §8.4 row says "Task fails after 3 attempts \| **3 attempts**". `TC-1064` asserts "**The pass is retried once.** On second failure, `error_observations` and the session summary are written…". No source says "once". The test that 08 §14.6 binds to AIF-15 therefore asserts a retry count that contradicts every candidate owner, and `TC-1136`'s row-diff will not catch it because the row exists — only its expected value is wrong. | **08** (defer to 05 §7 as AIF-15 does) and **05** (reconcile §8.4's "None" against §7's 3) |
| **RA2-03** | Medium | `09-adrs/ADR-0013-posthog-sole-analytics-errors-flags.md:11` vs `05-tdd.md:1443` (§10.6) | The ADR names the two feature flags the ruling explicitly killed. ADR-0013: "3. **Feature flags** — **staged rollout of character creation and the Weekly Proof** (`00` §11)." 05 §10.6: "**v1 launches with zero flags defined**. Rollout flags for `character-creation` and `weekly-proof` were **considered and rejected**: FR-303 requires character creation to be available from day one, and FR-500 makes Proof generation an unconditional MUST for every qualifying user — a default-off flag would put the implementation in direct violation of both." The ADR is the standing rationale for adopting PostHog and still advertises the forbidden use as its third justification. | **ADR-0013** |
| **RA2-04** | Medium | `08` (26 sites), `05:1006`, `01:1014`, `01:18` | 00 §1's new person-vocabulary rule is violated by three of the documents it binds. The rule (`00:22`) is "Engineering documents (01–06, 08, 09) say **'user'**… Mixed usage within one document is a defect." 08 uses "user" 198 times and "listener" 26 times in its own engineering prose, not in quoted copy — e.g. `08:1318` "The listener sees no change in the call", `08:1326` "The listener hears the flat week stated plainly", `08:1483` "Requests for **another listener's** facts", `08:363` "The host absorbs the five **listener** moves", `08:1535` "Each of the five **listener** moves absorbed genuinely". `05:1006` "…and the listener is never…". `01:1014` (US-3.2) "As a **listener** pulled into the argument…". The rule as written makes each of these a defect, and it is mechanically checkable — so it will fail the moment anyone runs it. Either the documents change or the rule needs a carve-out for narrative/user-story register. | **08**, 05, 01 (or **00** to scope the rule) |
| **RA2-05** | Medium | `07-ai-spec.md:1676` | Residual of RA-16's class: a live cadence value credited to the superseded PRD. `PRM-proof-script`'s header reads "Role `MDL-author` · temperature 0.8 · output cap 900 · structured. Blocks: `[LAW] [SAFE]`. **Weekly (PRD Part 11)**." Job cadence is owned by 05 §7, where `JOB-weekly-proof` runs on "the user's `proof_weekday`, qualified users only". 00 §5 puts `docs/*` below `docs/specs/*`, so this citation points at a document that cannot bind. (07's other surviving "PRD Part" strings — `07:23` "what makes PRD Part 13 true" and the ADR/01 §6/08 §16.2 occurrences — are provenance or historical prose and are fine.) | **07** (cite 05 §7) |
| **RA2-06** | Low | `09-adrs/ADR-0002-all-languages-package-pipeline.md:21` | The one unresolved cross-document section citation of 735. "**Dialect rule (amended after 06 §17.5):** every language ships exactly one dialect unless…" 06 §17 has only §17.1, §17.2, and §17.3. The same sentence cites "the 26+6 seed in 06 §15.2", which does resolve — §15.2 "Dialect seed and the skipped-choice rule" is almost certainly the intended target for both. | **ADR-0002** |
| **RA2-07** | Low | `00-decisions.md:51` and `00-decisions.md:67` | 00 §2 is now the registered owner of every ID scheme (RA-23's fix), and two of its own worked examples do not resolve. Row "Functional requirement \| `FR-###` \| 04-srs \| **FR-042**" — 04 defines no FR-042 (the 0xx band runs FR-001…FR-029). Row "Rate-limit class \| `RL-<KEBAB>` \| 06-data-api-spec §11.1 \| **RL-GENERATION**" — 06 defines 18 RL classes and `RL-GENERATION` is not among them; `RL-SESSION-CREATE` is the closest real class. Every other example in the table resolves (F-07, US-3.2, NFR-04, SCR-05, SCR-05/S3, DS-ProgrammePitch, EP-17, COPY-165, INV-COST-1, Q-DEFINE-BATCH, TC-0117, ADR-0004, JOB-post-session, PRM-episode-script@v1, MDL-realtime, SESSION_CAP_REACHED), which is what makes these two stand out to a script. | **00** |
| **RA2-08** | Low | `06-data-api-spec.md:895, 956, 994, 1337` | FR-101 statement 5 now claims exclusive ownership — "This requirement owns both pitch-card text caps; **no other document sets either value**" — and `06:848` correctly cites it for `pitches.text`. Four further 140-character caps in 06 remain uncited: `sessions.title` (`char_length BETWEEN 1 AND 140`), `episodes.title`, `articles.title`, `proofs.title` (`char_length <= 140`). At least `sessions.title` and `episodes.title` carry the accepted pitch line forward, so they are FR-101's value under another column name; `articles.title` and `proofs.title` may be 06's own, but nothing on the page says which. Under 00 §3 this is a value with no stated owner in four places. | **06** (cite FR-101 where the value is inherited; state ownership where it is not) |

### Severity counts

| Severity | Count |
|---|---|
| High | 2 (RA2-01, RA2-02) |
| Medium | 3 (RA2-03, RA2-04, RA2-05) |
| Low | 3 (RA2-06, RA2-07, RA2-08) |
| **Total** | **8** |

---

## Part 3 — Regression checks that came back CLEAN

1. **04 §6.1 is now an exact inverse of the 248 FR trace lines** — 0 over-reported, 0 under-reported pairs, all 55 features present. This was the largest defect pair in the original report (RA-11/RA-12, 69 wrong pairs) and it is now mechanically perfect in both directions.
2. **TC inventory survived the additions cleanly.** 570 defined `TC-####`, zero duplicates, zero referenced-but-undefined. The 19 declared bands in §14.9 expand to exactly the defined set with an empty diff both ways, and the band counts sum to the stated 570. The four out-of-band tokens (`TC-0712`, `TC-0799`, `TC-0840`, `TC-1240`) are all reservation labels in Rules N3/R1 and §1.2, not test definitions.
3. **The seven new test cases exist where claimed.** `TC-0841`–`TC-0846` are defined at `08:949–1013` and appear in §14.7's transport matrix and §14.9's new "Transport" band; `TC-0988` at `08:1228` appears in §14.9's Load band (now 11), §14.3 under NFR-31, and §14.7; `TC-1156` at `08:1360` appears in §14.4 under INV-JOB-4, §14.2 under FR-500–508, and §14.9's Invariant band (now 31).
4. **EP-23's retirement is airtight.** The only 6 sites in 06 are the §11 opener count, the EP-52 and EP-53 out-of-sequence notes, the §11.14 retirement table and its follow-on sentence, and §17.1's ruling record; ADR-0020's three are its own decision history. `RL-SSE` appears only alongside them. Zero live references, and the opener's arithmetic is right: "52 endpoints … numbered `EP-01` through `EP-53` with `EP-23` retired and never reused".
5. **Job-name canonicalisation is complete inside the specs.** All 11 names cited by 04, the 1 by 06, and the 10 by 08 match 05 §7 verbatim. Only ADR-0001 lags (RA-09).
6. **AIF renumbering is complete and collision-free.** 18 rows in 07 §11, 18 tests, 18 matrix entries, and no residual `F-##` usage for failure rows anywhere in 08.
7. **`INV-*` closure holds across the grouped index rows.** All 34 identifiers cited in 00, 05, 08, and ADR-0009 resolve against 05 §13, including the grouped `INV-JOB-1/2/3` and `INV-RUNTIME-1/2/3` rows.
8. **02, 03, and their ID sets are unchanged and still closed.** 27 screens / 273 states (Appendix D sums exactly), 51 `DS-*` closed in both directions, 277 `COPY-###` with no dangling reference from any document.
9. **ADR set grew to 21 and stayed consistent.** 21 files, 21 register entries in 00 §13, zero dangling `ADR-####` references anywhere.
10. **Forbidden normative vocabulary is clean.** `TBD`, `for example`, `such as`, `or similar`, and `etc.` appear in specs 00–08 only inside the sentences that forbid them.
11. **Ownership spot-checks pass** on all five targets named for this review: 05 §9.4 carries no metric targets; 05 §6.4 restates no cadence tier (and discloses the one sizing figure it does carry); 07 §4.6 injects `{word_band}` rather than the three bands; 01 F-30 carries no decay mechanics or numeric confidence. Only 05 §6.5 fails (RA2-01).
12. **The 04 §6.2 and §6.3 tables are legitimately partial by design** — §6.2 covers the 12 least-obvious FRs and states the general rule; §6.3 maps NFRs by range to source. Neither is a broken chain: 08 §14.1 has a primary for all 248 FRs and §14.3 for all 33 NFRs, with no gaps.
13. **`master.mp3` is canonical.** Zero `full.mp3`. 05 §5.3 cites "the `master.mp3` object at the path 06 §9.1 fixes"; 06 §9.1 owns the key.
