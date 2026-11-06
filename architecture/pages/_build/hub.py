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
  ("2026-11-01", "Counsel: may Saudi voice and transcripts rest on AWS in the UAE or EU?", "01 #1", "A no means moving to GCP Dammam: 5 to 8 engineer-days, and it must be known before week 1 builds the infrastructure."),
  ("2026-11-02", "One engineer or two", "01 #5", "The build plan assumes two and still lists P0 items likely to slip into the first beta week."),
  ("2026-11-02", "Consent addendum for the vendor tests", "01 #11", "The week-1 recognizer and voice tests send pilot clips to vendors the Milestone 0 consent does not name."),
  ("2026-11-02", "Brand domain", "06 #1", "forone.app is a placeholder; DNS, cookies and push identity are set in week 1."),
  ("2026-11-09", "Apple Developer and Google OAuth started", "01 #6, 06 #2", "Both take days to approve; otherwise week 3 ships with email codes only."),
  ("2026-11-09", "English Grammar Profile permission", "04 #1, 05 #3", "The structure inventory is seeded from it in week 1; a refusal means rewriting it."),
  ("2026-11-13", "Voice vendor after the blind test", "08", "The largest single cost decision: $0.57 to $0.67 a session on the viable stacks, $1.17 on ElevenLabs list."),
  ("2026-11-16", "Legal entity and payment processor", "01 #3", "Mada needs a Saudi-capable processor; three extra engineering days if it is not Stripe."),
  ("ongoing", "Fixed infrastructure budget, about $800 to $1,100 a month", "01 #4", "Approve, or set a cap and choose between Multi-AZ and a restore drill."),
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
  O09["09 Evaluation and operations<br/>measures, alerts, eval gate"] -.- T01"""

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
  <p class="eyebrow">For one · Technical architecture · 2026-10-16 to 2026-10-23</p>
  <h1>For one architecture</h1>
  <p class="lede">How the beta gets built between 2026-11-02 and 2026-12-06: nine domain documents, each answering one question, written against PRD-v2 and concept v2.</p>
</header>

<div class="figs">
  <div class="fig"><b>9</b><span>domain documents</span></div>
  <div class="fig"><b>{total_dec}</b><span>decisions made</span></div>
  <div class="fig"><b>{total_open}</b><span>items open for you</span></div>
  <div class="fig"><b>{total_words//1000}k</b><span>words in total</span></div>
  <div class="fig"><b>11 of 18</b><span>planned reviews done</span></div>
</div>

<section class="block">
  <h2>How the nine fit together</h2>
  <p class="muted">Solid arrows are the daily loop: an episode is made, heard, talked about, assessed, and feeds tomorrow's episode. Dotted lines are the domains that cut across all of it.</p>
  <div class="diagram"><pre class="mermaid">
{esc(MAP)}
</pre></div>
</section>

<section class="block">
  <h2>The documents</h2>
  <div class="legend">
    <div><span class="pill st-ok"><i></i>{STATUS['ok'][0]}</span><p>01 and 02. Rewritten after both reviews. Rely on these first.</p></div>
    <div><span class="pill st-warn"><i></i>{STATUS['warn'][0]}</span><p>03, 04, 05. Each page lists the open findings. Read them before relying on a section.</p></div>
    <div><span class="pill st-one"><i></i>{STATUS['one'][0]}</span><p>06. The skeptic review never ran.</p></div>
    <div><span class="pill st-none"><i></i>{STATUS['none'][0]}</span><p>07, 08, 09. Complete drafts that nobody has checked.</p></div>
  </div>
  <ol class="dlist">{cards}</ol>
</section>

<section class="block">
  <h2>Decisions that are due soon</h2>
  <p class="muted">Pulled from the "Open for Muath" sections. The build starts on 2026-11-02, so the first few block week 1. Each domain page has its full list.</p>
  <ol class="dues">{due_html}</ol>
</section>

<section class="block">
  <h2>What was cut</h2>
  <p class="muted">The original plan was an architecture phase, then a design phase. The run stopped on the usage limit and you asked to finish up, so this set is what exists.</p>
  <ul class="cut">
    <li><strong>The whole design phase.</strong> Eleven designers, their reviews and the clickable prototype never ran. <code>design/</code> is empty.</li>
    <li><strong>Seven of eighteen reviews.</strong> 07, 08 and 09 have no review; 06 has the conformance review but no skeptic review.</li>
    <li><strong>Revisions for 03 to 06.</strong> Their review findings are listed on each page but not applied to the text.</li>
    <li><strong>The integration pass.</strong> No one has reconciled the nine documents against each other after the reviews. Event names and a few interfaces disagree between documents; the reviews flag several.</li>
  </ul>
</section>

<section class="block">
  <h2>Source files</h2>
  <p class="muted">Everything is in the project folder under <code>architecture/</code>: the nine Markdown documents, <code>_review-findings.md</code> (all eleven completed reviews), <code>_digest-constraints.md</code> (every budget and rule extracted from PRD-v2), and these pages under <code>architecture/pages/</code>.</p>
</section>

<footer class="foot"><span class="muted">For one · architecture set, published 2026-10-23</span></footer>
</div>
"""

(OUT / "architecture-hub.html").write_text(page("For one architecture", "", body))
print("hub", len(body))
