#!/usr/bin/env python3
"""Build the architecture pages and the hub from /mnt/project-files/architecture/*.md."""
import json, re, sys, html
from pathlib import Path
import markdown

SRC = Path("/mnt/project-files/architecture")
OUT = SRC / "pages"
HERE = Path(__file__).parent
URLS = json.loads((HERE / "urls.json").read_text()) if (HERE / "urls.json").exists() else {}
HUB_URL = URLS.get("hub", "#")

STATUS = {
    "ok":   ("Reviewed twice, revised 2026-11-06", "Both reviews ran, every finding was applied, and the text was reconciled with the 2026-10-23 decisions and the decision records (document 10) on 2026-11-06."),
    "one":  ("One review, revised 2026-11-06", "Only the conformance review ran; no skeptic review exists for this document. Its findings and the decision records were applied on 2026-11-06, so the text is current, but it has had one fewer pair of eyes than the others."),
    "adr":  ("Decision records, written 2026-11-06", "The cross-domain rulings that the nine domain documents were revised to. It records why each ruling was made and what it changed; it has not itself been reviewed."),
    "warn": ("Reviewed twice, not revised", "Both reviews found real problems that are not fixed in the text yet."),
    "none": ("Unreviewed first draft", "Nobody has checked this draft yet."),
}

DOCS = [
 dict(n="01", slug="01-system-topology", short="System topology", status="ok",
      q="What runs where, so one or two engineers can ship the beta and grow it to 10,000 learners without a rewrite.",
      diagram="""flowchart LR
  L["Learner's phone<br/>web app + podcast app"]
  subgraph Vercel["Vercel, EU edge"]
    W["web<br/>Next.js PWA, no logic"]
  end
  subgraph AWS["AWS eu-central-1 by default<br/>me-central-1 is the one-day alternative"]
    A["api<br/>FastAPI on Fargate"]
    WF["workflows<br/>Inngest functions"]
    CW["call-worker<br/>LiveKit Agents"]
    PG[("Postgres RDS<br/>Multi-AZ, pgvector")]
    S3[("S3 x3<br/>per-learner keys")]
    KMS["KMS<br/>one key wraps each DEK"]
  end
  LK["LiveKit Cloud<br/>WebRTC media"]
  ING["Inngest Cloud EU<br/>ids and timestamps"]
  V["Model and voice vendors<br/>Anthropic, Gemini, voice, STT"]
  OBS["Langfuse EU + Sentry<br/>metadata by default"]
  L --> W --> A
  L -- "RSS + audio" --> A
  L <-- "call audio" --> LK <--> CW
  A --> PG
  A --> S3
  A --> KMS
  A -- "events" --> ING --> WF
  WF --> PG
  WF --> S3
  WF --> V
  CW --> V
  CW -- "/internal/events" --> A
  WF -.-> OBS
  CW -.-> OBS"""),
 dict(n="02", slug="02-generation-pipeline", short="Generation pipeline", status="ok",
      q="How every episode is planned, written, checked, voiced and published by the drop time, with a fallback that never misses a morning.",
      diagram="""flowchart LR
  T(["Trigger<br/>pick, cutoff, swap, return, sample"]) --> TE["Teacher<br/>Opus-class, batch when time allows"]
  TE --> VP{"validate_plan<br/>code"}
  VP --> WR["Writer<br/>Sonnet-class, batch"]
  WR --> FI{"Fitter<br/>code + Haiku"}
  FI -- "fail: rewrite, max 2" --> WR
  FI --> ED{"Editor<br/>11 checks, second vendor"}
  ED -- "fail: one repair" --> WR
  ED -- "second fail" --> FB["Fallback episode"]
  ED --> VS["Voice studio<br/>TTS, mix, align"]
  VS -- "too long: rewrite last scene" --> WR
  VS --> RL["Re-listen<br/>ASR diff, resynth"]
  RL --> GL["Glosses + word index"]
  GL --> PB(["Publisher<br/>one transaction, episode.ready"])
  FB --> VS"""),
 dict(n="03", slug="03-live-call-and-voice", short="Live call and voice", status="ok",
      q="How the 6 to 8 minute call with the hosts works: turn-taking, budgets enforced by code, talkback to Salma, and nothing lost when voice fails.",
      diagram="""sequenceDiagram
  participant P as Phone
  participant A as api
  participant LK as LiveKit Cloud
  participant CW as call-worker
  participant V as STT / LLM / TTS
  participant I as Inngest
  P->>A: POST /v1/calls
  A->>LK: create room + dispatch
  CW->>A: GET brief (CallBundle)
  CW->>P: opening line (pre-rendered)
  loop each turn
    P->>CW: learner speech
    CW->>V: streaming STT, end-of-turn from pause profile
    CW->>V: host LLM with @moves header
    Note over CW: governor checks moves against budgets
    CW->>P: host voice + captions
    CW->>I: turn audio ready (verbatim re-transcription)
  end
  CW->>A: call.ended
  A->>I: after-session pass (evidence in 10 min, no notes)"""),
 dict(n="04", slug="04-learner-model-and-data", short="Learner model and data", status="ok",
      q="Where everything known about a learner lives: one append-only event log, nine derived stores that can be rebuilt, and versioned briefs.",
      diagram="""flowchart LR
  subgraph Producers
    W["web<br/>player, chat with the producer"]
    CW["call-worker<br/>turns, talkback"]
    WF["workflows<br/>after-pass outputs"]
  end
  W --> AP["events.append<br/>in api"]
  CW --> AP
  WF --> AP
  AP --> E[("events<br/>append-only, RLS")]
  E --> AF["apply_after_pass<br/>validate, versions.bump"]
  subgraph Stores["Nine derived stores"]
    S1["word_bank · structure_map · error_profile"]
    S2["skills · interests · life_facts"]
    S3["goals · taste · show_canon"]
  end
  AF --> Stores
  Stores --> B["briefs.compile<br/>teacher, writer, host, Salma, chat, proof"]
  Stores -. "rebuild: drop and replay" .-> E"""),
 dict(n="05", slug="05-assessment-and-after-session", short="Assessment and after-session", status="ok",
      q="What happens in the ten minutes after a session: Salma's notes in 90 seconds, measures by code, and a five-rule gate before any progress claim is shown.",
      diagram="""flowchart LR
  T["Each learner turn<br/>verbatim re-transcription"] --> CE(["call.ended"])
  CE --> S1["After-session pass, one function, by 10 min<br/>analyst, classify recasts and word uses,<br/>measure, update the model, memory"]
  S1 --> V["learner_model_version + 1"]
  S1 --> C["Claim candidates"]
  S1 -. "nothing shown to the learner;<br/>Salma explains only when asked" .-> X["salma_explain"]
  subgraph Gate["Claim gate, five rules in order"]
    G1["like-for-like"] --> G2["beyond the noise"] --> G3["repeated"] --> G4["clean evidence"] --> G5["openable"]
  end
  C --> G1
  G5 --> O["Weekly proof, finale,<br/>return episode, teacher brief"]"""),
 dict(n="06", slug="06-client-and-delivery", short="Client and delivery", status="one",
      q="The installable web app, the private podcast feed and the three messages the product may send, with every rule kept on the server.",
      diagram="""flowchart LR
  subgraph Phone["Learner's phone"]
    TAB["Browser tab<br/>invite and feed links land here"]
    PWA["Installed PWA<br/>sw.js, media cache, event queue"]
    POD["Podcast app<br/>lock-screen listening"]
  end
  subgraph API["api modules"]
    F["feed<br/>tokenized RSS + mp3"]
    PU["push<br/>VAPID, three kinds only"]
    AU["auth<br/>OTP, Apple, Google"]
    ST["stream<br/>SSE updates"]
    SA["sample + waitlist"]
  end
  DN(["day/next at drop time"]) --> F
  DN --> PU
  PU --> PWA
  POD --> F
  PWA --> AU
  PWA --> ST
  TAB --> SA
  POD -. "call link" .-> TAB"""),
 dict(n="07", slug="07-security-privacy-and-compliance", short="Security, privacy, compliance", status="ok",
      q="How the promises about voice and life facts become verifiable: logged consent, deletion jobs with independent checks, staff access the learner can see, and a crisis path.",
      diagram="""flowchart LR
  subgraph B1["No secrets"]
    W["web"]
  end
  subgraph B2["Holds keys, writes audit_log"]
    A["api<br/>unwraps DEK via KMS"]
    WF["workflows<br/>privacy/verify, crisis/activate"]
  end
  subgraph B3["Per-call key only, no database"]
    CW["call-worker"]
  end
  subgraph B4["Named staff, roles, MFA"]
    AD["/admin<br/>every content read logged"]
  end
  subgraph B5["No learner_id column"]
    RS["Research set<br/>opt-in, anonymized"]
  end
  CO["Counsel<br/>edits consent texts, crisis files,<br/>privacy notice, processor register"]
  W --> A
  A --> CW
  AD --> A
  WF --> RS
  CO -.-> A"""),
 dict(n="08", slug="08-cost-model-and-vendors", short="Cost model and vendors", status="ok",
      q="What one session costs on each vendor stack, how every vendor call is priced and traced, and which decisions move the number.",
      diagram="""flowchart LR
  C["Callers<br/>workflows, call-worker, api"] --> AD["adapters.for_role<br/>vendors.yaml + vendor_config"]
  AD --> TR["tracing.traced<br/>time, units, price, spend guard"]
  PB[("price_book<br/>from prices.yaml")] --> TR
  TR --> VC[("vendor_calls<br/>one row per call")]
  TR -.-> LF["Langfuse observation"]
  VC --> RU["cost/rollup<br/>every 15 min"]
  RU --> SC[("session_costs<br/>learner + role roll-ups")]
  SC --> AL["cost/alarms<br/>per-plan guards, human levers only"]
  SC --> WR["Weekly report<br/>margin by plan, Monday 06:00 UTC"]
  VC --> RC["Monthly reconcile<br/>against vendor bills"]"""),
 dict(n="09", slug="09-evaluation-observability-and-operations", short="Evaluation and operations", status="ok",
      q="How the team knows the product works and keeps it working without building an observability product: rows in Postgres, alerts as SQL, an offline eval gate.",
      diagram="""flowchart LR
  subgraph Producers
    A["api"]
    WF["workflows"]
    CW["call-worker"]
    W["web<br/>client events"]
  end
  Producers --> PG[("Postgres rows<br/>events, calls.metrics, pipeline_steps")]
  Producers --> CL["CloudWatch logs + Sentry"]
  PG --> M["forone.measures<br/>hourly + weekly SQL, every timezone"]
  PG --> OP["forone.ops<br/>ops/watch every 5 min"]
  OP --> BS["Better Stack<br/>pages, P1 only when systemic"]
  OP --> SL["Slack #forone-ops<br/>P2, morning digest"]
  M0[("Milestone 0 files<br/>fixtures")] --> EV["forone.eval<br/>eval-gate in CI"]
  EV --> ER[("eval_runs")]"""),
 dict(n="10", slug="10-decision-records", short="Decision records", status="adr",
      q="The twenty-two rulings that reconcile the nine domains with the 2026-10-23 decisions: no launch country, monthly USD plans, invisible teaching, the re-dated build, and every name two documents disagreed on.",
      diagram="""flowchart LR
  D["decisions.md<br/>2026-10-23"] --> ADR["10 Decision records<br/>ADR-01 to ADR-22"]
  C["concept-v2.md"] --> ADR
  R["_review-findings.md<br/>17 reviews, second pass 2026-11-06"] --> ADR
  ADR --> N["No launch country<br/>ADR-02, 03, 20"]
  ADR --> P["Plans and episodes a day<br/>ADR-04, 05, 15, 21"]
  ADR --> I["Invisible teaching<br/>ADR-06"]
  ADR --> T["Dates and operations<br/>ADR-07, 16"]
  ADR --> K["Keys, regions, tracing<br/>ADR-08, 09, 12, 17, 18"]
  ADR --> M["Names and interfaces<br/>ADR-19"]
  N & P & I & T & K & M --> DOCS["01 to 09 revised 2026-11-06"]
  ADR --> O["§10 Open for Muath<br/>15 items"]"""),
]

MD_EXT = ["tables", "fenced_code", "sane_lists"]

def md(text):
    out = markdown.markdown(text, extensions=MD_EXT)
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return out

def md_inline(text):
    out = markdown.markdown(text, extensions=MD_EXT).strip()
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        out = out[3:-4]
    return out

def esc(s):
    return html.escape(s, quote=True)

def split_sections(text):
    """Return (h1, preamble, [(heading, body), ...]) by '## ' headings outside code fences."""
    lines = text.split("\n")
    h1, pre, secs, cur, buf, fence = "", [], [], None, [], False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if not fence and ln.startswith("# ") and not h1:
            h1 = ln[2:].strip(); continue
        if not fence and ln.startswith("## "):
            if cur is None: pre = buf
            else: secs.append((cur, "\n".join(buf)))
            cur, buf = ln[3:].strip(), []
            continue
        buf.append(ln)
    if cur is None: pre = buf
    else: secs.append((cur, "\n".join(buf)))
    return h1, "\n".join(pre).strip().strip("-").strip(), secs

def parse_table(body):
    rows = [l for l in body.split("\n") if l.startswith("|")]
    if len(rows) < 3: return None, None, None
    def cells(l):
        l = l.strip().strip("|")
        parts = re.split(r"(?<!\\)\|", l)
        return [p.strip() for p in parts]
    head = cells(rows[0])
    data = [cells(r) for r in rows[2:]]
    start = body.index(rows[0]); end = body.index(rows[-1]) + len(rows[-1])
    return head, data, (start, end)

def decisions_html(head, data):
    hl = [h.lower() for h in head]
    def col(*keys):
        for i, h in enumerate(hl):
            if any(k in h for k in keys): return i
        return None
    ci = dict(num=col("#"), dec=col("decision"), chosen=col("chosen"), why=col("reason", "why"), rej=col("rejected"))
    out = ['<ol class="decisions">']
    for r in data:
        g = lambda k: r[ci[k]] if ci[k] is not None and ci[k] < len(r) else ""
        out.append('<li class="dec">')
        out.append(f'<span class="dec-n">{esc(g("num"))}</span>')
        out.append('<div class="dec-body">')
        out.append(f'<h4>{md_inline(g("dec"))}</h4>')
        if g("chosen"): out.append(f'<p class="dec-chosen">{md_inline(g("chosen"))}</p>')
        if g("why"): out.append(f'<p class="dec-why"><span class="lbl">Why</span> {md_inline(g("why"))}</p>')
        if g("rej"): out.append(f'<p class="dec-rej"><span class="lbl">Rejected</span> {md_inline(g("rej"))}</p>')
        out.append('</div></li>')
    out.append('</ol>')
    return "\n".join(out)

def open_items(body):
    """Numbered top-level list items in section 10."""
    items, cur = [], None
    for ln in body.split("\n"):
        m = re.match(r"^(\d+)\.\s+(.*)", ln)
        if m:
            if cur: items.append(cur)
            cur = [m.group(2)]
        elif cur is not None:
            cur.append(ln)
    if cur: items.append(cur)
    res = []
    for it in items:
        t = "\n".join(it).strip()
        t = t.replace("[OPEN for Muath] ", "").replace("**[OPEN for Muath]** ", "")
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", t, re.S)
        if m: res.append((m.group(1).strip().rstrip(":.").strip(), m.group(2).strip()))
        else: res.append(("", t))
    tail = ""
    return res

def parse_reviews():
    text = (SRC / "_review-findings.md").read_text()
    reviews = {}
    for block in re.split(r"\n(?=## review:)", text):
        m = re.match(r"## review:(\w+):(\S+)", block)
        if not m: continue
        lens, slug = m.groups()
        verdict = re.search(r"^Verdict:\s*(.+)$", block, re.M)
        findings = []
        for fm in re.finditer(r"^- \*\*(blocker|major|minor)\*\* \((.*?)\): (.*?)(?=^- \*\*(?:blocker|major|minor)\*\*|\Z)", block, re.M | re.S):
            sev, loc, rest = fm.groups()
            parts = re.split(r"\n\s+- (Evidence|Fix): ", "\n" + rest)
            stmt = parts[0].strip(); extra = {}
            for i in range(1, len(parts) - 1, 2):
                extra[parts[i]] = parts[i + 1].strip()
            findings.append(dict(sev=sev, loc=loc, stmt=stmt, **{k.lower(): v for k, v in extra.items()}))
        reviews.setdefault(slug, []).append(dict(lens=lens, verdict=verdict.group(1) if verdict else "", findings=findings))
    return reviews

def first_sentence(s, limit=330):
    s = re.sub(r"\s+", " ", s)
    m = re.match(r"(.+?[.;])(\s|$)", s)
    out = m.group(1) if m else s
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0] + "…"
    return out

LENS = {"conformance": ("Conformance review", "Checked the draft against PRD-v2, concept v2 and the decisions."),
        "skeptic": ("Skeptic review", "Looked for what breaks: failure paths, cost, timing, things a small team cannot build.")}

def reviews_html(doc, revs):
    st = doc["status"]
    if not revs:
        if st == "adr":
            return ('<div class="nore"><p><strong>This document has not been reviewed.</strong> It was written on 2026-11-06 '
                    'from the seventeen reviews of the nine domains and the 2026-10-23 decisions; section 9 says how each '
                    'finding was applied, and section 11 of every domain document logs what changed.</p></div>')
        return ('<div class="nore"><p><strong>No review ran on this document.</strong></p></div>')
    out = []
    if st in ("ok", "one"):
        out.append('<p class="rv-note">These findings were raised against earlier drafts. Every one was applied on 2026-11-06 (see section 11 of the document for what changed), so they are kept here as history.</p>')
    else:
        out.append('<p class="rv-note warnnote">These findings are <strong>not fixed</strong> in the text below. Where a finding names a section, the fix it proposes is the better guide.</p>')
    for rv in revs:
        f = rv["findings"]
        cnt = {k: sum(1 for x in f if x["sev"] == k) for k in ("blocker", "major", "minor")}
        name, blurb = LENS.get(rv["lens"], (rv["lens"], ""))
        total = max(1, len(f))
        bar = "".join(f'<span class="seg {k}" style="flex:{cnt[k]}" title="{cnt[k]} {k}"></span>' for k in ("blocker", "major", "minor") if cnt[k])
        out.append(f'<section class="rv"><header class="rv-h"><div><h3>{name}</h3><p class="muted">{blurb} Verdict: {esc(rv["verdict"])}.</p></div>'
                   f'<div class="rv-counts"><span class="cnt blocker">{cnt["blocker"]} blocker</span><span class="cnt major">{cnt["major"]} major</span><span class="cnt minor">{cnt["minor"]} minor</span></div></header>'
                   f'<div class="sevbar">{bar}</div>')
        details_open = "" if st in ("ok", "one") else " open"
        serious = [x for x in f if x["sev"] in ("blocker", "major")]
        out.append(f'<details class="rv-list"{details_open}><summary>{len(serious)} blocker and major findings</summary><ol class="findings">')
        for x in serious:
            out.append(f'<li class="fd {x["sev"]}"><span class="sev">{x["sev"]}</span><div class="fd-b"><p class="fd-s">{md_inline(first_sentence(x["stmt"]))}</p>'
                       f'<details><summary>Where, evidence and fix</summary><p class="fd-loc">{md_inline(x["loc"])}</p>{md(x["stmt"])}'
                       + (f'<p><span class="lbl">Evidence</span> {md_inline(x["evidence"])}</p>' if x.get("evidence") else "")
                       + (f'<p><span class="lbl">Fix</span> {md_inline(x["fix"])}</p>' if x.get("fix") else "")
                       + '</details></div></li>')
        out.append('</ol></details>')
        minors = [x for x in f if x["sev"] == "minor"]
        if minors:
            out.append(f'<details class="rv-list"><summary>{len(minors)} minor findings</summary><ul class="minors">')
            for x in minors:
                out.append(f'<li>{md_inline(first_sentence(x["stmt"], 260))}</li>')
            out.append('</ul></details>')
        out.append('</section>')
    return "\n".join(out)

COST_CHART = """
<figure class="costfig">
  <figcaption><strong>Cost of one daily session by voice stack</strong><span class="muted">Section 6.1, list prices, standard TTS. Budget $0.60, stop line $1.00.</span></figcaption>
  <div class="cc">
    <div class="cc-scale"><span style="left:0%">$0</span><span style="left:20%">$0.25</span><span style="left:40%">$0.50</span><span style="left:60%">$0.75</span><span style="left:80%">$1.00</span><span style="left:100%">$1.25</span></div>
    <div class="cc-plot">
      <div class="refs"><div class="ref budget" style="left:48%"><span>budget $0.60</span></div><div class="ref stop" style="left:80%"><span>stop $1.00</span></div></div>
      <div class="cc-row"><span class="cc-l">Gemini voice</span><div class="cc-bars"><div class="bar now" style="width:53.76%"><b>$0.67</b></div><div class="bar later" style="width:68.32%"><b>$0.85</b></div></div></div>
      <div class="cc-row"><span class="cc-l">Inworld voice</span><div class="cc-bars"><div class="bar now" style="width:56.16%"><b>$0.70</b></div><div class="bar later" style="width:57.36%"><b>$0.72</b></div></div></div>
      <div class="cc-row"><span class="cc-l">ElevenLabs list</span><div class="cc-bars"><div class="bar now" style="width:96.4%"><b>$1.21</b></div><div class="bar later" style="width:97.6%"><b>$1.22</b></div></div></div>
    </div>
    <div class="cc-key"><span><i class="k now"></i>Beta, standard TTS</span><span><i class="k later"></i>After 2027-01-01 (Gemini prices double)</span></div>
  </div>
  <p class="muted small">Gemini with batch TTS reaches $0.61. The floor at scale is $0.45 at list prices after the doubling, $0.43 with a Sonnet teacher, against a $0.42 break-even on the 2 and 3 a day plans (section 6.5): the voice decision by 2026-11-17 and the contract in 10-decision-records §10 item 5 are the largest cost decisions in the beta.</p>
</figure>
"""

def read_css():
    return (HERE / "style.css").read_text()

def page(title, desc_meta, body):
    return f"""<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
{read_css()}
</style>
{body}
"""

def build_doc(doc, reviews):
    text = (SRC / f"{doc['slug']}.md").read_text()
    h1, pre, secs = split_sections(text)
    words = len(text.split())
    secmap = {h.split(".")[0].strip(): (h, b) for h, b in secs}
    s1h, s1 = secmap.get("1", ("", ""))
    head, data, span = parse_table(s1)
    summary = s1[:span[0]].strip() if span else s1
    after_table = s1[span[1]:].strip().strip("-").strip() if span else ""
    s7h, s7 = secmap.get("7", ("", ""))
    s10h, s10 = secmap.get("10", ("", ""))
    items = open_items(s10)
    revs = reviews.get(doc["slug"], [])
    label, explain = STATUS[doc["status"]]
    nreview = len(revs)

    toc = []
    full = []
    for i, (h, b) in enumerate(secs):
        sid = "s" + re.sub(r"[^0-9a-z]+", "-", h.lower()).strip("-")[:40]
        toc.append(f'<li><a href="#{sid}">{esc(h)}</a></li>')
        full.append(f'<details class="fs" id="{sid}"><summary><h3>{esc(h)}</h3><span class="wc">{len(b.split()):,} words</span></summary><div class="prose">{md(b)}</div></details>')

    items_html = "\n".join(
        f'<li class="oi"><div><h4>{md_inline(t) if t else "Open item"}</h4><div class="oi-b">{md(b)}</div></div></li>' for t, b in items)

    extra = COST_CHART if doc["n"] == "08" else ""

    body = f"""
<div class="page">
<nav class="crumbs"><a href="{HUB_URL}">For one architecture</a><span>/</span><span>{'Decision records' if doc['n']=='10' else f"Domain {int(doc['n'])} of 9"}</span></nav>
<header class="hero">
  <p class="eyebrow">{'Document 10 · Technical architecture · written 2026-11-06' if doc['n']=='10' else f"Domain {doc['n']} · Technical architecture · written 2026-10-16, revised 2026-10-17 and 2026-11-06"}</p>
  <h1>{esc(h1)}</h1>
  <p class="lede">{esc(doc['q'])}</p>
  <div class="meta">
    <span class="pill st-{doc['status']}"><i></i>{label}</span>
    <span class="chip">{len(data) if data else 0} decisions</span>
    <span class="chip">{len(items)} open for Muath</span>
    <span class="chip">{words:,} words, about {round(words/230/5)*5} min</span>
  </div>
</header>

<section class="statusbox st-{doc['status']}">
  <p><strong>{label}.</strong> {explain}</p>
</section>

<section class="block" id="summary">
  <h2>In one paragraph</h2>
  <div class="prose big">{md(summary)}</div>
</section>

<section class="block" id="picture">
  <h2>The picture</h2>
  <p class="muted">{'How the records were made and where they land.' if doc['n']=='10' else 'Drawn from section 3 of the document. Boxes are the canonical names the other domains use.'}</p>
  <div class="diagram"><pre class="mermaid">
{esc(doc['diagram'])}
</pre></div>
  {extra}
</section>

<section class="block" id="decisions">
  <h2>The decisions</h2>
  <p class="muted">Section 1's table, one card per decision. "Rejected" is what was considered and turned down.</p>
  {decisions_html(head, data) if data else ''}
  {('<div class="prose">' + md(after_table) + '</div>') if after_table else ''}
</section>

<section class="block" id="open">
  <h2>Open for Muath</h2>
  <p class="muted">{'Section 10: the register of everything only you can settle, across all ten documents.' if doc['n']=='10' else 'Section 10. Items shared with other domains point to the register in document 10; the rest are specific to this domain.'}</p>
  <ol class="openitems">{items_html}</ol>
</section>

<section class="block" id="build">
  <h2>Build plan, 2026-11-18 to 2026-12-22</h2>
  <div class="prose">{md(s7)}</div>
</section>

<section class="block" id="reviews">
  <h2>Review findings</h2>
  {reviews_html(doc, revs)}
</section>

<section class="block" id="full">
  <h2>The full document</h2>
  <p class="muted">Every section as written, closed by default. Source file: <code>architecture/{doc['slug']}.md</code>.</p>
  <ol class="toc">{''.join(toc)}</ol>
  <details class="fs"><summary><h3>Front matter</h3></summary><div class="prose">{md(pre)}</div></details>
  {''.join(full)}
</section>

<footer class="foot">
  <a href="{HUB_URL}">Back to the architecture hub</a>
  <span class="muted">For one · architecture set, 2026-10-23, revised 2026-11-06</span>
</footer>
</div>
<script>
document.querySelectorAll('.toc a').forEach(a => a.addEventListener('click', () => {{
  const d = document.querySelector(a.getAttribute('href')); if (d) d.open = true;
}}));
</script>
"""
    title = {"01": "System topology", "10": "Architecture decision records"}.get(doc["n"], f"{doc['short']} architecture")
    return title, page(title, "", body), dict(words=words, decisions=len(data) if data else 0, open=len(items),
                                              open_titles=[t for t, _ in items], reviews=revs)

def main():
    reviews = parse_reviews()
    OUT.mkdir(exist_ok=True)
    stats = {}
    for d in DOCS:
        title, h, st = build_doc(d, reviews)
        (OUT / f"{d['slug']}.html").write_text(h)
        stats[d["n"]] = dict(title=title, **{k: v for k, v in st.items() if k != "reviews"},
                             review_counts=[(r["lens"], {k: sum(1 for x in r["findings"] if x["sev"] == k) for k in ("blocker","major","minor")}) for r in st["reviews"]])
        print(d["n"], title, len(h), st["decisions"], st["open"])
    (HERE / "stats.json").write_text(json.dumps(stats, indent=1))

if __name__ == "__main__":
    main()
