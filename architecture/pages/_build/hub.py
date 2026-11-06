#!/usr/bin/env python3
"""Build the hub page linking the nine domain pages."""
import json
from pathlib import Path
from build import DOCS, STATUS, page, esc, OUT, HERE

stats = json.loads((HERE / "stats.json").read_text())
URLS = json.loads((HERE / "urls.json").read_text()) if (HERE / "urls.json").exists() else {}

total_words = sum(s["words"] for s in stats.values())
total_open = sum(s["open"] for s in stats.values())
total_dec = sum(s["decisions"] for s in stats.values())

def card(d):
    s = stats[d["n"]]
    label, _ = STATUS[d["status"]]
    url = URLS.get(d["n"], "#")
    if s["review_counts"]:
        rc = " · ".join(f'{"Conformance" if l=="conformance" else "Skeptic"}: {c["blocker"]} blocker, {c["major"]} major' for l, c in s["review_counts"])
    else:
        rc = "No review ran"
    return f"""<li class="dcard">
  <a class="dlink" href="{url}">
    <span class="dn">{d['n']}</span>
    <span class="dbody">
      <span class="dtitle">{esc(d['short'])}</span>
      <span class="dq">{esc(d['q'])}</span>
      <span class="dmeta"><span class="pill st-{d['status']}"><i></i>{label}</span></span>
      <span class="drc">{rc}</span>
      <span class="dfoot">{s['decisions']} decisions · {s['open']} open for you · {s['words']:,} words</span>
    </span>
  </a>
</li>"""

DUE = [
  ("now", "Consent addendum for the vendor tests", "10 #13", "Clips from the Milestone 0 pilot go to recognizer and voice vendors the pilot consent does not name. Nothing leaves before the addendum is signed."),
  ("2026-11-17", "Home region and the legal view on storing learner voice", "10 #1", "Counsel confirms where a worldwide cohort's voice and transcripts may rest. eu-central-1 is the default; me-central-1 is a one-day config move, but it must be known before build week 1."),
  ("2026-11-17", "Which jurisdictions the beta covers on day one", "10 #2", "Recommended: EU and UK GDPR, Saudi PDPL and a generic baseline. Sets the consent copy per native language and the DPIA."),
  ("2026-11-17", "Voice vendor after the English blind test", "10 #5", "The largest single cost decision. The floor stack lands at $0.43 to $0.45 a session after Gemini's 2027 price rise, against a $0.42 break-even on the 2 and 3 a day plans."),
  ("2026-11-18", "Second engineer, and which week-6 items may slip", "10 #10", "The build plan assumes two engineers from the first day of build week 1."),
  ("2026-11-18", "Apple Developer, Google OAuth and the brand domain started", "10 #15", "Approvals take days; DNS, cookies and push identity are set in week 1."),
  ("2026-12-02", "Payment processor and legal entity", "10 #3", "Paddle as merchant of record (about 5%, tax handled everywhere) or Stripe with Stripe Tax (about 3% plus registrations, needs an entity in a Stripe country). Checkout is built in week 3."),
  ("2026-12-15", "Crisis protocol details", "10 #12", "Per-country resources and the international fallback, clip wording, whether the keyword list may fire alone."),
  ("2026-12-22", "Tier prices against the break-even, and the last lever to $0.35", "10 #4, #5", "Keep $19.99 / $29.99 / $44.99 and accept the loss on full-use learners, raise 2 a day to $34.99, or sign a voice contract. The exit document carries the measured number."),
  ("ongoing", "Fixed infrastructure budget, about $1,000 to $1,300 a month", "10 #9", "01's $800 to $1,100 plus staging kept up through the beta, plus vendor minimums and the Anthropic prepaid balance."),
  ("ongoing", "Web or native for the beta", "10 #8", "The architecture builds the installable web app plus the private podcast feed; the switch-to-native triggers are measured from day one."),
]

due_html = "\n".join(f"""<li class="due"><span class="dd">{esc(d)}</span><div><h4>{esc(t)}</h4><p>{esc(why)}</p><span class="src">{esc(src)}</span></div></li>""" for d, t, src, why in DUE)

MAP = """flowchart LR
  L["Learner's phone"] --> C06["06 Client and delivery<br/>PWA, podcast feed, push"]
  C06 --> T01["01 System topology<br/>web, api, workflows, call-worker"]
  L <--> C03["03 Live call and voice<br/>call-worker on LiveKit"]
  T01 --> P02["02 Generation pipeline<br/>teacher, writer, editor, voice"]
  C03 --> A05["05 Assessment<br/>after-session pass, claim gate"]
  A05 --> D04["04 Learner model<br/>event log, nine stores, briefs"]
  D04 --> P02
  P02 --> C06
  S07["07 Security and privacy<br/>keys, consent, deletion, crisis"] -.- T01
  K08["08 Cost and vendors<br/>adapters, tracing, spend guard"] -.- P02
  K08 -.- C03
  O09["09 Evaluation and operations<br/>measures, alerts, eval gate"] -.- T01
  R10["10 Decision records<br/>22 rulings, the open register"] ==> T01
  R10 ==> P02
  R10 ==> C06"""

cards = "\n".join(card(d) for d in DOCS)

HUB_CSS = """
.hubhero h1 { max-width: 16ch; }
.figs { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
.fig { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 2px; }
.fig b { font-family: var(--display); font-size: 1.7rem; font-variant-numeric: tabular-nums; }
.fig span { font-size: .84rem; color: var(--muted); }
.dlist { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr)); gap: 12px; }
.dcard { display: flex; }
.dlink { flex: 1; display: flex; gap: 12px; text-decoration: none; color: var(--ink); background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px; transition: border-color .15s, transform .15s; }
.dlink:hover { border-color: var(--accent); transform: translateY(-1px); }
.dlink:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.dn { font-family: var(--display); font-weight: 700; font-size: 1.5rem; color: var(--accent); line-height: 1; min-width: 1.6ch; }
.dbody { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.dtitle { font-family: var(--display); font-weight: 700; font-size: 1.15rem; }
.dq { font-size: .88rem; line-height: 1.5; }
.drc, .dfoot { font-family: var(--mono); font-size: .72rem; color: var(--muted); }
.dfoot { margin-top: auto; padding-top: 4px; border-top: 1px solid var(--line); }
.legend { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; }
.legend div { display: flex; flex-direction: column; gap: 6px; background: var(--surface); border-radius: 10px; padding: 12px 14px; border: 1px solid var(--line); }
.legend p { font-size: .88rem; color: var(--ink); }
.dues { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; border-top: 1px solid var(--line); }
.due { display: grid; grid-template-columns: 110px 1fr; gap: 14px; padding: 12px 0; border-bottom: 1px solid var(--line); }
.due > div { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.dd { font-family: var(--mono); font-size: .82rem; color: var(--flag); font-weight: 500; font-variant-numeric: tabular-nums; padding-top: 2px; }
.due p { font-size: .9rem; max-width: 70ch; }
.src { font-family: var(--mono); font-size: .7rem; color: var(--muted); }
.cut { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: 8px; max-width: 75ch; }
@media (max-width: 520px) { .due { grid-template-columns: 1fr; gap: 4px; } }
"""

body = f"""
<style>{HUB_CSS}</style>
<div class="page">
<header class="hero hubhero">
  <p class="eyebrow">For one · Technical architecture · written 2026-10-16, revised 2026-11-06</p>
  <h1>For one architecture</h1>
  <p class="lede">How the beta gets built between 2026-11-18 and 2026-12-22: nine domain documents, each answering one question, plus the decision records that reconcile them with the 2026-10-23 decisions: no launch country, monthly USD plans, invisible teaching, evidence instead of tests.</p>
</header>

<div class="figs">
  <div class="fig"><b>9 + 1</b><span>domain documents and the decision records</span></div>
  <div class="fig"><b>{total_dec}</b><span>decisions made</span></div>
  <div class="fig"><b>{total_open}</b><span>items open for you</span></div>
  <div class="fig"><b>{total_words//1000}k</b><span>words in total</span></div>
  <div class="fig"><b>17 of 18</b><span>planned reviews done, all applied</span></div>
</div>

<section class="block">
  <h2>How the nine fit together</h2>
  <p class="muted">Solid arrows are the daily loop: an episode is made, heard, talked about, assessed, and feeds tomorrow's episode. Dotted lines are the domains that cut across all of it. The thick arrows are document 10, whose rulings every other document was revised to on 2026-11-06.</p>
  <div class="diagram"><pre class="mermaid">
{esc(MAP)}
</pre></div>
</section>

<section class="block">
  <h2>The documents</h2>
  <div class="legend">
    <div><span class="pill st-ok"><i></i>{STATUS['ok'][0]}</span><p>01 to 05 and 07 to 09. Both reviews ran, every finding was applied, and the text follows the decision records. Section 11 of each document logs what changed.</p></div>
    <div><span class="pill st-one"><i></i>{STATUS['one'][0]}</span><p>06. The skeptic review never ran; the conformance findings and the decision records were applied.</p></div>
    <div><span class="pill st-adr"><i></i>{STATUS['adr'][0]}</span><p>10. The twenty-two cross-domain rulings, the naming table for the technical design, and the register of everything open for you.</p></div>
  </div>
  <ol class="dlist">{cards}</ol>
</section>

<section class="block">
  <h2>Decisions that are due soon</h2>
  <p class="muted">From the register in document 10, section 10. The build starts on 2026-11-18, so the first few block week 1. Each domain page keeps its own items too.</p>
  <ol class="dues">{due_html}</ol>
</section>

<section class="block">
  <h2>What changed on 2026-11-06, and what is still missing</h2>
  <p class="muted">The 2026-10-23 run stopped on the usage limit with 07 to 09 unreviewed and 03 to 06 unrevised. This pass finished the set.</p>
  <ul class="cut">
    <li><strong>Six new reviews.</strong> 07, 08 and 09 were each read by the conformance and the skeptic lens: 60 findings, six blockers, all applied.</li>
    <li><strong>Every document revised.</strong> The 2026-10-23 decisions had moved under the documents: no launch country, USD monthly plans with 1, 2 or 3 episodes a day, no correction notes, a build re-dated to 2026-11-18. Document 10 records the 22 rulings and each document's section 11 says what changed.</li>
    <li><strong>The integration pass.</strong> Names that disagreed between documents (`episodes.state`, `call_turn_verbatim`, `word_uses`, `expects_drop`, package paths) have one spelling now, listed in document 10 section 4 for the technical design.</li>
    <li><strong>Still missing.</strong> The skeptic review of 06, and a review of document 10 itself. The design phase ran separately and lives in <code>design/</code>.</li>
  </ul>
</section>

<section class="block">
  <h2>Source files</h2>
  <p class="muted">Everything is in the project folder and in the GitHub repository under <code>architecture/</code>: the ten Markdown documents, <code>_review-findings.md</code> (all seventeen reviews), <code>_digest-constraints.md</code> (every budget and rule extracted from PRD-v2), and these pages under <code>architecture/pages/</code>.</p>
</section>

<footer class="foot"><span class="muted">For one · architecture set, published 2026-10-23, revised 2026-11-06</span></footer>
</div>
"""

(OUT / "architecture-hub.html").write_text(page("For one architecture", "", body))
print("hub", len(body))
