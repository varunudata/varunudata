#!/usr/bin/env python3
"""
Builds the complete SVG architectural drawing set for Varun Udata's GitHub portfolio.
Generates both Light (warm archival paper) and Dark (deep drafting slate) variants
with embedded subsetted WOFF2 fonts (Instrument Serif, IBM Plex Sans, IBM Plex Mono).
"""

import base64
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_DIR = ROOT / "design"
FONTS_DIR = DESIGN_DIR / "fonts"
ASSETS_DIR = ROOT / "assets"
CONTRIB_PATH = DESIGN_DIR / "contributions.json"

THEMES = {
    "light": {
        "bg": "#F3F0E9",
        "bg_elev": "#EBE6DC",
        "bg_card": "#F8F6F1",
        "ink": "#1A1A18",
        "ink_soft": "#3D3B36",
        "muted": "#6E6B63",
        "faint": "#9A958B",
        "line": "#CBC6BA",
        "line_strong": "#8C867A",
        "accent": "#2B47A8",
        "accent_soft": "#E3E8F7",
        "accent_border": "#7A90D6",
    },
    "dark": {
        "bg": "#13161C",
        "bg_elev": "#1A1E26",
        "bg_card": "#171B22",
        "ink": "#E8E4DB",
        "ink_soft": "#C5C0B5",
        "muted": "#8F8C85",
        "faint": "#5F5D58",
        "line": "#2D333E",
        "line_strong": "#4A5262",
        "accent": "#8FA5EE",
        "accent_soft": "#1D2640",
        "accent_border": "#4D64AC",
    },
}


def load_font_b64(filename: str) -> str:
    data = (FONTS_DIR / filename).read_bytes()
    return base64.b64encode(data).decode("ascii")


FONT_B64 = {
    "serif_reg": load_font_b64("InstrumentSerif-Regular.woff2"),
    "serif_ita": load_font_b64("InstrumentSerif-Italic.woff2"),
    "mono_reg": load_font_b64("IBMPlexMono-Regular.woff2"),
    "mono_med": load_font_b64("IBMPlexMono-Medium.woff2"),
    "sans_reg": load_font_b64("IBMPlexSans-Regular.woff2"),
    "sans_med": load_font_b64("IBMPlexSans-Medium.woff2"),
}


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def build_style(t: dict) -> str:
    return f"""
    @font-face {{
      font-family: 'Instrument Serif';
      font-style: normal;
      font-weight: 400;
      src: url("data:font/woff2;base64,{FONT_B64['serif_reg']}") format("woff2");
    }}
    @font-face {{
      font-family: 'Instrument Serif';
      font-style: italic;
      font-weight: 400;
      src: url("data:font/woff2;base64,{FONT_B64['serif_ita']}") format("woff2");
    }}
    @font-face {{
      font-family: 'IBM Plex Mono';
      font-style: normal;
      font-weight: 400;
      src: url("data:font/woff2;base64,{FONT_B64['mono_reg']}") format("woff2");
    }}
    @font-face {{
      font-family: 'IBM Plex Mono';
      font-style: normal;
      font-weight: 500;
      src: url("data:font/woff2;base64,{FONT_B64['mono_med']}") format("woff2");
    }}
    @font-face {{
      font-family: 'IBM Plex Sans';
      font-style: normal;
      font-weight: 400;
      src: url("data:font/woff2;base64,{FONT_B64['sans_reg']}") format("woff2");
    }}
    @font-face {{
      font-family: 'IBM Plex Sans';
      font-style: normal;
      font-weight: 500;
      src: url("data:font/woff2;base64,{FONT_B64['sans_med']}") format("woff2");
    }}
    .serif {{ font-family: 'Instrument Serif', Georgia, 'Times New Roman', serif; fill: {t['ink']}; }}
    .serif-i {{ font-family: 'Instrument Serif', Georgia, 'Times New Roman', serif; font-style: italic; fill: {t['ink']}; }}
    .mono {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; fill: {t['muted']}; }}
    .mono-ink {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; fill: {t['ink']}; }}
    .mono-med {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 500; fill: {t['ink']}; }}
    .mono-acc {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 500; fill: {t['accent']}; }}
    .sans {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; fill: {t['ink_soft']}; }}
    .sans-ink {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; fill: {t['ink']}; }}
    .sans-med {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 500; fill: {t['ink']}; }}
    .sans-muted {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; fill: {t['muted']}; }}
    .rule {{ stroke: {t['line']}; stroke-width: 1; fill: none; }}
    .rule-strong {{ stroke: {t['line_strong']}; stroke-width: 1.15; fill: none; }}
    .rule-dash {{ stroke: {t['line_strong']}; stroke-width: 1; stroke-dasharray: 4 3; fill: none; }}
    .acc-stroke {{ stroke: {t['accent']}; stroke-width: 1.35; fill: none; }}
    .acc-box {{ fill: {t['accent_soft']}; stroke: {t['accent']}; stroke-width: 1.25; }}
    .card-box {{ fill: {t['bg_card']}; stroke: {t['line']}; stroke-width: 1; }}
    .elev-box {{ fill: {t['bg_elev']}; stroke: {t['line']}; stroke-width: 1; }}
    """


def sheet_frame(
    w: int,
    h: int,
    t: dict,
    sheet_code: str,
    sheet_title: str,
    right_meta: str,
    rev: str = "REV A · NOV 2026",
) -> str:
    """Draws the architectural sheet background, crop marks, outer frame, and top title strip."""
    m = 16
    inner_w = w - 2 * m
    inner_h = h - 2 * m
    left_sep = m + 232
    right_sep = w - m - 156
    parts = [
        f'<rect width="{w}" height="{h}" rx="4" fill="{t["bg"]}"/>',
        # Outer frame
        f'<rect x="{m}" y="{m}" width="{inner_w}" height="{inner_h}" class="rule-strong"/>',
        # Corner crop ticks outside the frame
        f'<path d="M 6 {m} H 13 M {m} 6 V 13" class="rule-strong"/>',
        f'<path d="M {w-13} {m} H {w-6} M {w-m} 6 V 13" class="rule-strong"/>',
        f'<path d="M 6 {h-m} H 13 M {m} {h-13} V {h-6}" class="rule-strong"/>',
        f'<path d="M {w-13} {h-m} H {w-6} M {w-m} {h-13} V {h-6}" class="rule-strong"/>',
        # Top header bar background & line
        f'<rect x="{m+0.5}" y="{m+0.5}" width="{inner_w-1}" height="28" fill="{t["bg_elev"]}"/>',
        f'<line x1="{m}" y1="{m+28}" x2="{w-m}" y2="{m+28}" class="rule-strong"/>',
        # Small cobalt square marker in top bar
        f'<rect x="{m+12}" y="{m+10}" width="8" height="8" fill="{t["accent"]}"/>',
        f'<text x="{m+28}" y="{m+18}" class="mono-med" font-size="9.5" letter-spacing="1">{esc(sheet_code)}</text>',
        f'<line x1="{left_sep}" y1="{m}" x2="{left_sep}" y2="{m+28}" class="rule"/>',
        f'<text x="{left_sep+12}" y="{m+18}" class="mono" font-size="9.5" letter-spacing="0.6">{esc(sheet_title)}</text>',
        f'<text x="{right_sep-12}" y="{m+18}" class="mono" font-size="9.5" letter-spacing="0.6" text-anchor="end">{esc(right_meta)}</text>',
        f'<line x1="{right_sep}" y1="{m}" x2="{right_sep}" y2="{m+28}" class="rule"/>',
        f'<text x="{w-m-12}" y="{m+18}" class="mono-ink" font-size="9.5" letter-spacing="0.6" text-anchor="end">{esc(rev)}</text>',
    ]
    return "\n  ".join(parts)


def wrap_svg(w: int, h: int, t: dict, body: str, aria_label: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(aria_label)}">
  <defs>
    <style>{build_style(t)}</style>
    <pattern id="hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="{t['line']}" stroke-width="1"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.2 L 7 4 L 0 6.8 z" fill="{t['line_strong']}"/>
    </marker>
    <marker id="arrow-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.2 L 7 4 L 0 6.8 z" fill="{t['accent']}"/>
    </marker>
  </defs>
  {body}
</svg>
"""


def build_sheet_00_cover(t: dict) -> str:
    w, h = 960, 412
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 00 // COVER",
        "PORTFOLIO SPECIFICATION & IDENTITY",
        "DWG NO. VU-2026-00",
    )
    split_x = 592
    body = f"""{frame}
  <!-- Vertical divider between editorial hero and specification ledger -->
  <line x1="{split_x}" y1="44" x2="{split_x}" y2="{h-16}" class="rule-strong"/>

  <!-- Left Editorial Hero -->
  <text x="40" y="76" class="mono-acc" font-size="10.5" letter-spacing="1.4">00 / IDENTITY &amp; ENGINEERING PRACTICE</text>

  <text x="40" y="142" class="serif" font-size="68" letter-spacing="-0.5">Varun Udata<tspan fill="{t['accent']}">.</tspan></text>

  <text x="42" y="170" class="mono-med" font-size="12" letter-spacing="1.6">FULL-STACK DEVELOPER  /  SOFTWARE ENGINEER</text>

  <line x1="40" y1="188" x2="{split_x-28}" y2="188" class="rule"/>
  <rect x="40" y="186.5" width="28" height="3" fill="{t['accent']}"/>

  <!-- Architectural statement -->
  <text x="40" y="224" class="serif" font-size="23.5">
    <tspan x="40" dy="0">I build full-stack web software from relational schema to</tspan>
    <tspan x="40" dy="31">browser interface—focusing on how data is modeled, how</tspan>
    <tspan x="40" dy="31">services behave under failure, and how complex systems</tspan>
    <tspan x="40" dy="31">become legible to the people using them.</tspan>
  </text>

  <!-- Bottom strip inside left column -->
  <line x1="16" y1="350" x2="{split_x}" y2="350" class="rule"/>
  <text x="40" y="370" class="mono" font-size="9.5" letter-spacing="1.1">PRIMARY MEDIUM</text>
  <text x="40" y="385" class="mono-ink" font-size="10.5">JavaScript (ES2024+)  ·  React &amp; Next.js  ·  Node.js &amp; Express  ·  PostgreSQL &amp; Prisma</text>

  <!-- Right Technical Identity Panel -->
  <rect x="{split_x+0.6}" y="44.6" width="{w-16-split_x-1.2}" height="28" fill="{t['bg_card']}"/>
  <line x1="{split_x}" y1="72.5" x2="{w-16}" y2="72.5" class="rule"/>
  <text x="{split_x+18}" y="62.5" class="mono-med" font-size="10" letter-spacing="1.2">SPECIFICATION LEDGER // PROFILE INDEX</text>

  <!-- Row 01: Education -->
  <text x="{split_x+18}" y="95" class="mono" font-size="9.5" letter-spacing="1">01 · EDUCATION</text>
  <text x="{split_x+18}" y="113" class="sans-med" font-size="12.5">B.Tech in Computer Science (AI &amp; ML)</text>
  <text x="{split_x+18}" y="130" class="sans-muted" font-size="11.5">3rd-Year Undergraduate · Rishihood University</text>
  <line x1="{split_x}" y1="143" x2="{w-16}" y2="143" class="rule"/>

  <!-- Row 02: Core Discipline -->
  <text x="{split_x+18}" y="164" class="mono" font-size="9.5" letter-spacing="1">02 · PRIMARY DISCIPLINE</text>
  <text x="{split_x+18}" y="182" class="sans-med" font-size="12.5">Full-Stack Web Application Engineering</text>
  <text x="{split_x+18}" y="199" class="sans-muted" font-size="11.5">REST APIs, Real-Time Systems, Relational Data</text>
  <line x1="{split_x}" y1="212" x2="{w-16}" y2="212" class="rule"/>

  <!-- Row 03: Active Main Project -->
  <text x="{split_x+18}" y="233" class="mono" font-size="9.5" letter-spacing="1">03 · CURRENT MAIN WORK</text>
  <text x="{split_x+18}" y="251" class="sans-med" font-size="12.5">Codebase Intelligence Platform (hello)</text>
  <text x="{split_x+18}" y="268" class="sans-muted" font-size="11.5">Babel AST Call Graphs, Blast Radius &amp; 4-Stage RAG</text>
  <line x1="{split_x}" y1="281" x2="{w-16}" y2="281" class="rule"/>

  <!-- Row 04: Engineering Interests -->
  <text x="{split_x+18}" y="302" class="mono" font-size="9.5" letter-spacing="1">04 · SYSTEMS &amp; EXPLORATION</text>
  <text x="{split_x+18}" y="320" class="sans-med" font-size="12.5">System Design, DevOps &amp; Applied GenAI</text>
  <text x="{split_x+18}" y="337" class="sans-muted" font-size="11.5">Docker, CI/CD, Linux, NL-to-SQL, Graph Retrieval</text>
  <line x1="{split_x}" y1="350" x2="{w-16}" y2="350" class="rule"/>

  <!-- Row 05: Availability -->
  <rect x="{split_x+18}" y="365" width="9" height="9" fill="{t['accent']}"/>
  <text x="{split_x+34}" y="373" class="mono-acc" font-size="10" letter-spacing="1">STATUS // OPEN FOR OPPORTUNITIES</text>
  <text x="{split_x+34}" y="388" class="sans-ink" font-size="11.5">Preparing for SWE Internships &amp; Placements</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Varun Udata — Full-Stack Developer and Software Engineer. Cover sheet and technical identity specification.",
    )


def build_sheet_01_about(t: dict) -> str:
    w, h = 960, 316
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 01 // ABOUT",
        "ENGINEERING PHILOSOPHY & ARCHITECTURAL APPROACH",
        "SECTION 01 OF 06",
    )
    c1, c2 = 330, 645
    body = f"""{frame}
  <!-- Top Headline Banner -->
  <text x="36" y="72" class="mono-acc" font-size="10" letter-spacing="1.3">01 / ENGINEERING PHILOSOPHY</text>
  <text x="36" y="106" class="serif" font-size="34">Building software as a complete system, not isolated layers<tspan fill="{t['accent']}">.</tspan></text>
  <line x1="16" y1="124" x2="{w-16}" y2="124" class="rule-strong"/>

  <!-- Column Dividers -->
  <line x1="{c1}" y1="124" x2="{c1}" y2="{h-16}" class="rule"/>
  <line x1="{c2}" y1="124" x2="{c2}" y2="{h-16}" class="rule"/>

  <!-- Column I -->
  <text x="36" y="148" class="mono-acc" font-size="10" letter-spacing="1.1">I · APPLICATION LIFECYCLE</text>
  <text x="36" y="174" class="serif" font-size="20.5">End-to-end ownership in JavaScript.</text>
  <text x="36" y="198" class="sans" font-size="11.8">
    <tspan x="36" dy="0">I treat client state, HTTP/WebSocket boundaries,</tspan>
    <tspan x="36" dy="18">and relational schemas as one continuous surface.</tspan>
    <tspan x="36" dy="18">Working primarily in JavaScript across Next.js,</tspan>
    <tspan x="36" dy="18">React, Node.js, and Express keeps data contracts</tspan>
    <tspan x="36" dy="18">explicit from database row to rendered view.</tspan>
  </text>
  <line x1="36" y1="278" x2="{c1-20}" y2="278" class="rule"/>
  <text x="36" y="292" class="mono" font-size="9.5">SCOPE: UI  →  API  →  ORM  →  STORAGE</text>

  <!-- Column II -->
  <text x="{c1+20}" y="148" class="mono-acc" font-size="10" letter-spacing="1.1">II · BACKEND &amp; DATA DESIGN</text>
  <text x="{c1+20}" y="174" class="serif" font-size="20.5">Schemas and guardrails first.</text>
  <text x="{c1+20}" y="198" class="sans" font-size="11.8">
    <tspan x="{c1+20}" dy="0">Reliable software starts in the data and service</tspan>
    <tspan x="{c1+20}" dy="18">layer: normalized PostgreSQL schemas via Prisma,</tspan>
    <tspan x="{c1+20}" dy="18">connection-pool tuning for serverless Neon cold</tspan>
    <tspan x="{c1+20}" dy="18">starts, role-scoped JWT middleware, and automated</tspan>
    <tspan x="{c1+20}" dy="18">deployments over Tailscale and Linux/PM2.</tspan>
  </text>
  <line x1="{c1+20}" y1="278" x2="{c2-20}" y2="278" class="rule"/>
  <text x="{c1+20}" y="292" class="mono" font-size="9.5">SCOPE: POSTGRESQL  ·  PRISMA  ·  CI/CD</text>

  <!-- Column III -->
  <text x="{c2+20}" y="148" class="mono-acc" font-size="10" letter-spacing="1.1">III · APPLIED AI &amp; CODE SYSTEMS</text>
  <text x="{c2+20}" y="174" class="serif" font-size="20.5">Grounded structure over prompts.</text>
  <text x="{c2+20}" y="198" class="sans" font-size="11.8">
    <tspan x="{c2+20}" dy="0">Rather than treating LLMs as magic, I pair them</tspan>
    <tspan x="{c2+20}" dy="18">with deterministic program structure: Babel AST</tspan>
    <tspan x="{c2+20}" dy="18">call graphs and transitive blast-radius traversal</tspan>
    <tspan x="{c2+20}" dy="18">for codebase Q&amp;A, or MySQL schema introspection</tspan>
    <tspan x="{c2+20}" dy="18">with strict read-only SELECT execution gates.</tspan>
  </text>
  <line x1="{c2+20}" y1="278" x2="{w-36}" y2="278" class="rule"/>
  <text x="{c2+20}" y="292" class="mono" font-size="9.5">SCOPE: AST  ·  CALL-GRAPH RAG  ·  NL-TO-SQL</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Sheet 01 — Engineering Philosophy: Application Lifecycle, Backend & Data Design, Applied AI & Code Systems.",
    )


def build_sheet_02_header(t: dict) -> str:
    w, h = 960, 114
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 02 // SELECTED WORK",
        "ARCHITECTURAL CASE STUDIES & SYSTEM SCHEMATICS",
        "SECTION 02 OF 06",
    )
    body = f"""{frame}
  <text x="36" y="84" class="serif" font-size="38">Selected Engineering Work<tspan fill="{t['accent']}">.</tspan></text>
  <text x="{w-36}" y="71" class="mono-acc" font-size="10" letter-spacing="1.1" text-anchor="end">PLATES 01 — 04  ·  DRAWN FROM REPOSITORY SOURCE</text>
  <text x="{w-36}" y="88" class="mono" font-size="9.5" text-anchor="end">Primary focus: Codebase Intelligence Platform (hello) + 3 Full-Stack Systems</text>
"""
    return wrap_svg(w, h, t, body, "Sheet 02 — Selected Engineering Work")


def build_work_01_hello(t: dict) -> str:
    w, h = 960, 360
    frame = sheet_frame(
        w,
        h,
        t,
        "PLATE 02.1 // MAIN PROJECT",
        "HELLO (ARCHON) — CODEBASE INTELLIGENCE PLATFORM",
        "REPO: varunudata/hello",
        "ACTIVE · 12.9K LOC",
    )
    sx = 456
    body = f"""{frame}
  <line x1="{sx}" y1="44" x2="{sx}" y2="{h-16}" class="rule-strong"/>

  <!-- Left Case Study Metadata -->
  <rect x="34" y="58" width="9" height="9" fill="{t['accent']}"/>
  <text x="50" y="66" class="mono-acc" font-size="10" letter-spacing="1.2">01 · MAIN PROJECT (IN ACTIVE DEVELOPMENT)</text>

  <text x="34" y="102" class="serif" font-size="34">Codebase Intelligence Platform<tspan fill="{t['accent']}">.</tspan></text>
  <text x="34" y="122" class="mono-ink" font-size="10">Repository: varunudata/hello  ·  Engine: Archon AST Core v2.4</text>

  <line x1="34" y1="134" x2="{sx-20}" y2="134" class="rule"/>

  <text x="34" y="153" class="mono" font-size="9.5" letter-spacing="1">ARCHITECTURAL SUMMARY</text>
  <text x="34" y="171" class="sans" font-size="11.5">
    <tspan x="34" dy="0">Full-stack platform that ingests GitHub repositories via tarball</tspan>
    <tspan x="34" dy="17">streams, parses source files into Abstract Syntax Trees, computes</tspan>
    <tspan x="34" dy="17">cross-file call graphs and transitive change blast radius, and</tspan>
    <tspan x="34" dy="17">answers architectural questions through a 4-stage graph-aware RAG.</tspan>
  </text>

  <line x1="34" y1="236" x2="{sx-20}" y2="236" class="rule"/>

  <!-- Key Specs Grid -->
  <text x="34" y="254" class="mono" font-size="9">AST &amp; GRAPH ENGINE</text>
  <text x="34" y="269" class="mono-ink" font-size="9.8">@babel/parser + traverse · Complexity · BFS Blast Radius</text>

  <text x="34" y="293" class="mono" font-size="9">4-STAGE GRAPH RAG</text>
  <text x="34" y="308" class="mono-ink" font-size="9.8">Report Guard → AST Call Matcher → 20B SLM → 120B LLM</text>

  <text x="34" y="331" class="mono" font-size="9">STACK</text>
  <text x="78" y="331" class="mono-acc" font-size="9.5">Next.js 16 · React 19 · Express 5 · Prisma v6 · Neon DB</text>

  <!-- Right Technical Schematic: AST + 4-Stage RAG -->
  <rect x="{sx+0.6}" y="44.6" width="{w-16-sx-1.2}" height="24" fill="{t['bg_card']}"/>
  <line x1="{sx}" y1="68.5" x2="{w-16}" y2="68.5" class="rule"/>
  <text x="{sx+16}" y="60" class="mono-med" font-size="9.5" letter-spacing="1">FIG 2.1 — AST CALL-GRAPH INDEXER &amp; 4-STAGE RAG PIPELINE</text>

  <!-- Tier 1: Ingestion & AST Parsing -->
  <rect x="{sx+18}" y="82" width="132" height="52" class="card-box"/>
  <text x="{sx+28}" y="99" class="mono-acc" font-size="8.5">01 · INGESTION</text>
  <text x="{sx+28}" y="114" class="mono-ink" font-size="9.5">codeload.github</text>
  <text x="{sx+28}" y="127" class="mono" font-size="8.5">Tarball + ls-remote</text>

  <line x1="{sx+150}" y1="108" x2="{sx+168}" y2="108" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+170}" y="82" width="142" height="52" class="card-box"/>
  <text x="{sx+180}" y="99" class="mono-acc" font-size="8.5">02 · AST PARSER</text>
  <text x="{sx+180}" y="114" class="mono-ink" font-size="9.5">astEngine.js</text>
  <text x="{sx+180}" y="127" class="mono" font-size="8.5">Babel AST + Polyglot</text>

  <line x1="{sx+312}" y1="108" x2="{sx+330}" y2="108" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+332}" y="82" width="138" height="52" class="card-box"/>
  <text x="{sx+342}" y="99" class="mono-acc" font-size="8.5">03 · CALL GRAPH</text>
  <text x="{sx+342}" y="114" class="mono-ink" font-size="9.5">Upstream BFS</text>
  <text x="{sx+342}" y="127" class="mono" font-size="8.5">Blast % &amp; Criticality</text>

  <!-- Connector down to Stage 2 RAG box -->
  <line x1="{sx+241}" y1="134" x2="{sx+241}" y2="152" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <!-- Tier 2: Cobalt Highlighted 4-Stage RAG Pipeline -->
  <rect x="{sx+18}" y="154" width="452" height="106" class="acc-box"/>
  <text x="{sx+28}" y="172" class="mono-acc" font-size="9.2" letter-spacing="0.8">GRAPH-AWARE AST RAG ENGINE (server/lib/codebaseRag.js)</text>

  <!-- 4 stages inside the Cobalt box -->
  <rect x="{sx+28}" y="182" width="98" height="64" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+35}" y="198" class="mono-acc" font-size="8">STAGE 01</text>
  <text x="{sx+35}" y="212" class="mono-ink" font-size="9">Report Guard</text>
  <text x="{sx+35}" y="226" class="mono" font-size="8">Routes repo-wide</text>
  <text x="{sx+35}" y="237" class="mono" font-size="8">queries to Sec 04</text>

  <line x1="{sx+126}" y1="214" x2="{sx+136}" y2="214" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <rect x="{sx+138}" y="182" width="104" height="64" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+145}" y="198" class="mono-acc" font-size="8">STAGE 02</text>
  <text x="{sx+145}" y="212" class="mono-ink" font-size="9">AST Matcher</text>
  <text x="{sx+145}" y="226" class="mono" font-size="8">Stem tokens +</text>
  <text x="{sx+145}" y="237" class="mono" font-size="8">1-hop call graph</text>

  <line x1="{sx+242}" y1="214" x2="{sx+252}" y2="214" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <rect x="{sx+254}" y="182" width="98" height="64" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+261}" y="198" class="mono-acc" font-size="8">STAGE 03</text>
  <text x="{sx+261}" y="212" class="mono-ink" font-size="9">20B SLM Router</text>
  <text x="{sx+261}" y="226" class="mono" font-size="8">Fallback symbol</text>
  <text x="{sx+261}" y="237" class="mono" font-size="8">locator on miss</text>

  <line x1="{sx+352}" y1="214" x2="{sx+362}" y2="214" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <rect x="{sx+364}" y="182" width="96" height="64" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+371}" y="198" class="mono-acc" font-size="8">STAGE 04</text>
  <text x="{sx+371}" y="212" class="mono-ink" font-size="9">120B Synthesis</text>
  <text x="{sx+371}" y="226" class="mono" font-size="8">Scope-aware</text>
  <text x="{sx+371}" y="237" class="mono" font-size="8">code answer</text>

  <!-- Tier 3: Storage & Client Workspace -->
  <line x1="{sx+126}" y1="260" x2="{sx+126}" y2="278" class="rule-strong" marker-end="url(#arrow)"/>
  <line x1="{sx+354}" y1="260" x2="{sx+354}" y2="278" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+18}" y="280" width="218" height="50" class="card-box"/>
  <text x="{sx+26}" y="298" class="mono-ink" font-size="9.2">Prisma v6 + Neon PostgreSQL</text>
  <text x="{sx+26}" y="314" class="mono" font-size="8.2">PgBouncer timeout guard + JSON mirror</text>

  <rect x="{sx+246}" y="280" width="224" height="50" class="card-box"/>
  <text x="{sx+254}" y="298" class="mono-ink" font-size="9.2">Next.js 16 Workspace (4 Views)</text>
  <text x="{sx+254}" y="314" class="mono" font-size="8.2">Overview · Graph · Ask · Reports</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Case Study 01: Codebase Intelligence Platform (varunudata/hello) — AST Call-Graph Indexer and 4-Stage Graph RAG schematic.",
    )


def build_work_02_datapulse(t: dict) -> str:
    w, h = 960, 344
    frame = sheet_frame(
        w,
        h,
        t,
        "PLATE 02.2 // CASE STUDY 02",
        "DATAPULSE — NATURAL-LANGUAGE SQL & ANALYTICS ENGINE",
        "REPO: varunudata/DataPulse",
        "FULL-STACK · AI + SQL",
    )
    sx = 456
    body = f"""{frame}
  <line x1="{sx}" y1="44" x2="{sx}" y2="{h-16}" class="rule-strong"/>

  <!-- Left Metadata -->
  <text x="34" y="66" class="mono-acc" font-size="10" letter-spacing="1.2">02 · NATURAL-LANGUAGE DATABASE INTERFACE</text>
  <text x="34" y="102" class="serif" font-size="36">DataPulse<tspan fill="{t['accent']}">.</tspan></text>
  <text x="34" y="122" class="mono-ink" font-size="10">Repository: varunudata/DataPulse  ·  Schema-Scoped NL-to-SQL</text>

  <line x1="34" y1="134" x2="{sx-20}" y2="134" class="rule"/>

  <text x="34" y="153" class="mono" font-size="9.5" letter-spacing="1">ARCHITECTURAL SUMMARY</text>
  <text x="34" y="171" class="sans" font-size="11.5">
    <tspan x="34" dy="0">Analytics platform where users connect external MySQL databases</tspan>
    <tspan x="34" dy="17">and query them in plain English. Extracts table/column schemas</tspan>
    <tspan x="34" dy="17">without exposing row data to the LLM, enforces read-only SQL</tspan>
    <tspan x="34" dy="17">validation, and renders live Recharts visualizations.</tspan>
  </text>

  <line x1="34" y1="234" x2="{sx-20}" y2="234" class="rule"/>

  <text x="34" y="252" class="mono" font-size="9">PRIVACY &amp; SAFETY BOUNDARY</text>
  <text x="34" y="268" class="mono-ink" font-size="9.8">INFORMATION_SCHEMA only · SELECT-only gate · LIMIT 200 cap</text>

  <text x="34" y="292" class="mono" font-size="9">DUAL-DATABASE TOPOLOGY</text>
  <text x="34" y="308" class="mono-ink" font-size="9.8">PostgreSQL (Prisma) app state + mysql2 pool for user DBs</text>

  <!-- Right Schematic -->
  <rect x="{sx+0.6}" y="44.6" width="{w-16-sx-1.2}" height="24" fill="{t['bg_card']}"/>
  <line x1="{sx}" y1="68.5" x2="{w-16}" y2="68.5" class="rule"/>
  <text x="{sx+16}" y="60" class="mono-med" font-size="9.5" letter-spacing="1">FIG 2.2 — SCHEMA INTROSPECTION &amp; READ-ONLY SQL EXECUTION LOOP</text>

  <!-- Top Row: User MySQL -> Schema Extractor -> Gemini -->
  <rect x="{sx+18}" y="84" width="136" height="58" class="card-box"/>
  <text x="{sx+28}" y="102" class="mono-acc" font-size="8.5">USER MYSQL DB</text>
  <text x="{sx+28}" y="117" class="mono-ink" font-size="9.5">mysql2/promise</text>
  <text x="{sx+28}" y="131" class="mono" font-size="8.2">Connection Pool</text>

  <line x1="{sx+154}" y1="113" x2="{sx+174}" y2="113" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+176}" y="84" width="144" height="58" class="card-box"/>
  <text x="{sx+186}" y="102" class="mono-acc" font-size="8.5">SCHEMA SERVICE</text>
  <text x="{sx+186}" y="117" class="mono-ink" font-size="9.5">INFORMATION_SCHEMA</text>
  <text x="{sx+186}" y="131" class="mono" font-size="8.2">0 row values exposed</text>

  <line x1="{sx+320}" y1="113" x2="{sx+340}" y2="113" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+342}" y="84" width="128" height="58" class="card-box"/>
  <text x="{sx+352}" y="102" class="mono-acc" font-size="8.5">SQL SYNTHESIS</text>
  <text x="{sx+352}" y="117" class="mono-ink" font-size="9.5">Gemini 2.5 Flash</text>
  <text x="{sx+352}" y="131" class="mono" font-size="8.2">Schema + NL Prompt</text>

  <!-- Arrow down from Gemini to Safety Gate -->
  <line x1="{sx+406}" y1="142" x2="{sx+406}" y2="164" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <!-- Middle Row: Cobalt SQL Safety Gate -->
  <rect x="{sx+18}" y="166" width="452" height="66" class="acc-box"/>
  <text x="{sx+28}" y="185" class="mono-acc" font-size="9.2" letter-spacing="0.8">EXECUTION GUARDRAIL // server/utils/sqlSafety.js</text>
  <text x="{sx+28}" y="203" class="mono-ink" font-size="9.5">1. isSafeSelectQuery(q) → requires /^select/i &amp; blocks DDL/DML</text>
  <text x="{sx+28}" y="220" class="mono-ink" font-size="9.5">2. ensureLimit(q, 200)  → caps rows before hitting MySQL pool</text>

  <!-- Arrow from Safety Gate back to MySQL & down to Client -->
  <line x1="{sx+86}" y1="166" x2="{sx+86}" y2="144" class="acc-stroke" marker-end="url(#arrow-acc)"/>
  <line x1="{sx+244}" y1="232" x2="{sx+244}" y2="254" class="rule-strong" marker-end="url(#arrow)"/>

  <!-- Bottom Row: Visualization & Persistence -->
  <rect x="{sx+18}" y="256" width="222" height="56" class="card-box"/>
  <text x="{sx+28}" y="274" class="mono-acc" font-size="8.5">CLIENT VISUALIZATION (NEXT.JS 15)</text>
  <text x="{sx+28}" y="290" class="mono-ink" font-size="9.5">Recharts X/Y &amp; Data Tables</text>
  <text x="{sx+28}" y="304" class="mono" font-size="8.2">Sortable rows + PNG chart export</text>

  <rect x="{sx+252}" y="256" width="218" height="56" class="card-box"/>
  <text x="{sx+262}" y="274" class="mono-acc" font-size="8.5">APP STATE (PRISMA + POSTGRESQL)</text>
  <text x="{sx+262}" y="290" class="mono-ink" font-size="9.5">User · QueryHistory · PinnedChart</text>
  <text x="{sx+262}" y="304" class="mono" font-size="8.2">Live re-execution of pinned queries</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Case Study 02: DataPulse — Natural-Language-to-SQL Analytics Platform schematic.",
    )


def build_work_03_nookambika(t: dict) -> str:
    w, h = 960, 344
    frame = sheet_frame(
        w,
        h,
        t,
        "PLATE 02.3 // CASE STUDY 03",
        "NOOKAMBIKA DHABA — REAL-TIME HOTEL MANAGEMENT",
        "DOMAIN: HOSPITALITY OPS",
        "NEXT.JS · SOCKET.IO",
    )
    sx = 456
    body = f"""{frame}
  <line x1="{sx}" y1="44" x2="{sx}" y2="{h-16}" class="rule-strong"/>

  <!-- Left Metadata -->
  <text x="34" y="66" class="mono-acc" font-size="10" letter-spacing="1.2">03 · EVENT-DRIVEN HOSPITALITY &amp; ORDER PLATFORM</text>
  <text x="34" y="102" class="serif" font-size="36">Nookambika Dhaba<tspan fill="{t['accent']}">.</tspan></text>
  <text x="34" y="122" class="mono-ink" font-size="10">Full-Stack Hotel &amp; Restaurant Order Management Application</text>

  <line x1="34" y1="134" x2="{sx-20}" y2="134" class="rule"/>

  <text x="34" y="153" class="mono" font-size="9.5" letter-spacing="1">ARCHITECTURAL SUMMARY</text>
  <text x="34" y="171" class="sans" font-size="11.5">
    <tspan x="34" dy="0">Multi-role restaurant operations platform coordinating table</tspan>
    <tspan x="34" dy="17">customers, floor captains, and administrators. Physical tables map</tspan>
    <tspan x="34" dy="17">to QR-encoded sessions while Socket.IO synchronizes live order</tspan>
    <tspan x="34" dy="17">tickets and status transitions across every active terminal.</tspan>
  </text>

  <line x1="34" y1="234" x2="{sx-20}" y2="234" class="rule"/>

  <text x="34" y="252" class="mono" font-size="9">ROLE-BASED ACCESS &amp; TABLE CONTEXT</text>
  <text x="34" y="268" class="mono-ink" font-size="9.8">Customer (Table QR) · Captain (Floor Dispatch) · Admin (Control)</text>

  <text x="34" y="292" class="mono" font-size="9">STACK &amp; TRANSPORT</text>
  <text x="34" y="308" class="mono-ink" font-size="9.8">Next.js Frontend · Express.js REST API · Socket.IO Event Bus</text>

  <!-- Right Schematic -->
  <rect x="{sx+0.6}" y="44.6" width="{w-16-sx-1.2}" height="24" fill="{t['bg_card']}"/>
  <line x1="{sx}" y1="68.5" x2="{w-16}" y2="68.5" class="rule"/>
  <text x="{sx+16}" y="60" class="mono-med" font-size="9.5" letter-spacing="1">FIG 2.3 — QR TABLE CONTEXT &amp; SOCKET.IO MULTI-ROLE EVENT BUS</text>

  <!-- Left column of 3 Role Terminals -->
  <rect x="{sx+18}" y="84" width="148" height="66" class="card-box"/>
  <text x="{sx+28}" y="102" class="mono-acc" font-size="8.5">ROLE 01 // CUSTOMER</text>
  <text x="{sx+28}" y="117" class="mono-ink" font-size="9.5">Table QR Session</text>
  <text x="{sx+28}" y="131" class="mono" font-size="8.2">Scans table QR → menu</text>
  <text x="{sx+28}" y="143" class="mono" font-size="8.2">&amp; live order tracker</text>

  <rect x="{sx+18}" y="162" width="148" height="66" class="card-box"/>
  <text x="{sx+28}" y="180" class="mono-acc" font-size="8.5">ROLE 02 // CAPTAIN</text>
  <text x="{sx+28}" y="195" class="mono-ink" font-size="9.5">Floor &amp; Table Terminal</text>
  <text x="{sx+28}" y="209" class="mono" font-size="8.2">Instant table alerts,</text>
  <text x="{sx+28}" y="221" class="mono" font-size="8.2">order edits &amp; fulfillment</text>

  <rect x="{sx+18}" y="240" width="148" height="68" class="card-box"/>
  <text x="{sx+28}" y="258" class="mono-acc" font-size="8.5">ROLE 03 // ADMIN</text>
  <text x="{sx+28}" y="273" class="mono-ink" font-size="9.5">Operations Console</text>
  <text x="{sx+28}" y="287" class="mono" font-size="8.2">Menu catalog, QR table</text>
  <text x="{sx+28}" y="299" class="mono" font-size="8.2">registry &amp; settlement</text>

  <!-- Bidirectional arrows to Central Socket.IO Hub -->
  <line x1="{sx+166}" y1="117" x2="{sx+194}" y2="155" class="acc-stroke" marker-end="url(#arrow-acc)"/>
  <line x1="{sx+166}" y1="195" x2="{sx+194}" y2="195" class="acc-stroke" marker-end="url(#arrow-acc)"/>
  <line x1="{sx+166}" y1="274" x2="{sx+194}" y2="235" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <!-- Center Cobalt Hub: Express + Socket.IO -->
  <rect x="{sx+196}" y="114" width="136" height="162" class="acc-box"/>
  <text x="{sx+208}" y="135" class="mono-acc" font-size="8.8" letter-spacing="0.6">EXPRESS + SOCKET.IO</text>
  <text x="{sx+208}" y="151" class="mono-ink" font-size="9.5">Real-Time Event Bus</text>
  <line x1="{sx+208}" y1="160" x2="{sx+320}" y2="160" class="rule"/>
  <text x="{sx+208}" y="177" class="mono" font-size="8.2">Rooms by tableId &amp;</text>
  <text x="{sx+208}" y="190" class="mono" font-size="8.2">staff role channels:</text>
  <text x="{sx+208}" y="208" class="mono-ink" font-size="8.5">• order:created</text>
  <text x="{sx+208}" y="222" class="mono-ink" font-size="8.5">• order:status_sync</text>
  <text x="{sx+208}" y="236" class="mono-ink" font-size="8.5">• captain:notify</text>
  <text x="{sx+208}" y="250" class="mono-ink" font-size="8.5">• table:state_change</text>

  <line x1="{sx+332}" y1="195" x2="{sx+352}" y2="195" class="rule-strong" marker-end="url(#arrow)"/>

  <!-- Right Column: Order Lifecycle State Machine -->
  <rect x="{sx+354}" y="84" width="116" height="224" class="card-box"/>
  <text x="{sx+364}" y="103" class="mono-acc" font-size="8.5">ORDER LIFECYCLE</text>

  <rect x="{sx+366}" y="116" width="92" height="28" class="elev-box"/>
  <text x="{sx+412}" y="134" class="mono-ink" font-size="9" text-anchor="middle">01 · PLACED</text>
  <line x1="{sx+412}" y1="144" x2="{sx+412}" y2="158" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+366}" y="160" width="92" height="28" class="elev-box"/>
  <text x="{sx+412}" y="178" class="mono-ink" font-size="9" text-anchor="middle">02 · ACCEPTED</text>
  <line x1="{sx+412}" y1="188" x2="{sx+412}" y2="202" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+366}" y="204" width="92" height="28" class="elev-box"/>
  <text x="{sx+412}" y="222" class="mono-ink" font-size="9" text-anchor="middle">03 · SERVED</text>
  <line x1="{sx+412}" y1="232" x2="{sx+412}" y2="246" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+366}" y="248" width="92" height="28" class="acc-box"/>
  <text x="{sx+412}" y="266" class="mono-acc" font-size="9" text-anchor="middle">04 · SETTLED</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Case Study 03: Nookambika Dhaba — Real-Time Hotel and Order Management System schematic.",
    )


def build_work_04_a6news(t: dict) -> str:
    w, h = 960, 344
    frame = sheet_frame(
        w,
        h,
        t,
        "PLATE 02.4 // CASE STUDY 04",
        "A6NEWS INFRA — PRODUCTION CMS & TAILSCALE-EC2 PIPELINE",
        "LIVE: a6newsinfra.com",
        "PRODUCTION · 2 REPOS",
    )
    sx = 456
    body = f"""{frame}
  <line x1="{sx}" y1="44" x2="{sx}" y2="{h-16}" class="rule-strong"/>

  <!-- Left Metadata -->
  <text x="34" y="66" class="mono-acc" font-size="10" letter-spacing="1.2">04 · PRODUCTION NEWS PLATFORM, CMS &amp; CI/CD</text>
  <text x="34" y="102" class="serif" font-size="36">A6News Infra<tspan fill="{t['accent']}">.</tspan></text>
  <text x="34" y="122" class="mono-ink" font-size="10">Repos: a6news_frontend &amp; a6news_backend  ·  Live: a6newsinfra.com</text>

  <line x1="34" y1="134" x2="{sx-20}" y2="134" class="rule"/>

  <text x="34" y="153" class="mono" font-size="9.5" letter-spacing="1">ARCHITECTURAL SUMMARY</text>
  <text x="34" y="171" class="sans" font-size="11.5">
    <tspan x="34" dy="0">Production infrastructure news publication and editorial Content</tspan>
    <tspan x="34" dy="17">Management System. Pairs a Next.js 15 App Router public portal and</tspan>
    <tspan x="34" dy="17">role-guarded admin dashboard with an Express + Prisma + PostgreSQL</tspan>
    <tspan x="34" dy="17">backend deployed to AWS EC2 over a private Tailscale mesh network.</tspan>
  </text>

  <line x1="34" y1="234" x2="{sx-20}" y2="234" class="rule"/>

  <text x="34" y="252" class="mono" font-size="9">CMS DATA MODEL (PRISMA + POSTGRESQL)</text>
  <text x="34" y="268" class="mono-ink" font-size="9.8">User (RBAC) · Category · Post (DRAFT / PUBLISHED) · Ticker</text>

  <text x="34" y="292" class="mono" font-size="9">ZERO-TRUST DEPLOYMENT</text>
  <text x="34" y="308" class="mono-ink" font-size="9.8">GitHub Actions → Tailscale VPN → SSH EC2 → Lockfile Diff → PM2</text>

  <!-- Right Schematic -->
  <rect x="{sx+0.6}" y="44.6" width="{w-16-sx-1.2}" height="24" fill="{t['bg_card']}"/>
  <line x1="{sx}" y1="68.5" x2="{w-16}" y2="68.5" class="rule"/>
  <text x="{sx+16}" y="60" class="mono-med" font-size="9.5" letter-spacing="1">FIG 2.4 — SPLIT-REPO CMS &amp; TAILSCALE MESH EC2 DEPLOY PIPELINE</text>

  <!-- Top Row: Frontend & Backend -->
  <rect x="{sx+18}" y="84" width="212" height="64" class="card-box"/>
  <text x="{sx+28}" y="101" class="mono-acc" font-size="8.5">FRONTEND (a6news_frontend)</text>
  <text x="{sx+28}" y="116" class="mono-ink" font-size="9.5">Next.js 15 App Router + React 19</text>
  <text x="{sx+28}" y="130" class="mono" font-size="8.2">Public SSR (site) + /admin CMS</text>
  <text x="{sx+28}" y="142" class="mono" font-size="8.2">Category feeds, slugs &amp; live ticker</text>

  <line x1="{sx+230}" y1="116" x2="{sx+250}" y2="116" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+252}" y="84" width="218" height="64" class="card-box"/>
  <text x="{sx+262}" y="101" class="mono-acc" font-size="8.5">BACKEND API (a6news_backend)</text>
  <text x="{sx+262}" y="116" class="mono-ink" font-size="9.5">Express.js + Prisma + PostgreSQL</text>
  <text x="{sx+262}" y="130" class="mono" font-size="8.2">JWT + Bcrypt authMiddleware</text>
  <text x="{sx+262}" y="142" class="mono" font-size="8.2">Multer multipart media + Slugify</text>

  <!-- Middle Row: Database Schema Strip -->
  <line x1="{sx+361}" y1="148" x2="{sx+361}" y2="164" class="rule-strong" marker-end="url(#arrow)"/>

  <rect x="{sx+18}" y="166" width="452" height="44" class="elev-box"/>
  <text x="{sx+28}" y="184" class="mono-med" font-size="8.8">POSTGRESQL SCHEMA // prisma/schema.prisma</text>
  <text x="{sx+28}" y="200" class="mono" font-size="8.1">Post {{ slug @unique, status: DRAFT|PUBLISHED, gallery[], views }} · Category · Ticker</text>

  <!-- Bottom Row: Cobalt CI/CD Pipeline -->
  <rect x="{sx+18}" y="222" width="452" height="90" class="acc-box"/>
  <text x="{sx+28}" y="240" class="mono-acc" font-size="9.2" letter-spacing="0.8">CI/CD PIPELINE // .github/workflows/deploy.yml</text>

  <rect x="{sx+28}" y="250" width="96" height="48" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+36}" y="266" class="mono-acc" font-size="8">01 · TRIGGER</text>
  <text x="{sx+36}" y="280" class="mono-ink" font-size="8.8">Push to main</text>
  <text x="{sx+36}" y="292" class="mono" font-size="8">GitHub Actions</text>

  <line x1="{sx+124}" y1="274" x2="{sx+136}" y2="274" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <rect x="{sx+138}" y="250" width="102" height="48" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+146}" y="266" class="mono-acc" font-size="8">02 · MESH VPN</text>
  <text x="{sx+146}" y="280" class="mono-ink" font-size="8.8">Tailscale Action</text>
  <text x="{sx+146}" y="292" class="mono" font-size="8">Private SSH tunnel</text>

  <line x1="{sx+240}" y1="274" x2="{sx+252}" y2="274" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <rect x="{sx+254}" y="250" width="102" height="48" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+262}" y="266" class="mono-acc" font-size="8">03 · SMART BUILD</text>
  <text x="{sx+262}" y="280" class="mono-ink" font-size="8.8">git diff lockfile</text>
  <text x="{sx+262}" y="292" class="mono" font-size="8">npm ci + prisma</text>

  <line x1="{sx+356}" y1="274" x2="{sx+368}" y2="274" class="acc-stroke" marker-end="url(#arrow-acc)"/>

  <rect x="{sx+370}" y="250" width="88" height="48" fill="{t['bg']}" stroke="{t['accent_border']}" stroke-width="1"/>
  <text x="{sx+378}" y="266" class="mono-acc" font-size="8">04 · RUNTIME</text>
  <text x="{sx+378}" y="280" class="mono-ink" font-size="8.8">AWS EC2 + PM2</text>
  <text x="{sx+378}" y="292" class="mono" font-size="8">Zero-downtime</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Case Study 04: A6News Infra — Production News Portal, CMS, and Tailscale-to-EC2 CI/CD Pipeline schematic.",
    )


def build_sheet_03_engineering(t: dict) -> str:
    w, h = 960, 340
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 03 // ENGINEERING NOTES",
        "CONCRETE ARCHITECTURAL DECISIONS FROM REPOSITORY SOURCE",
        "SECTION 03 OF 06",
    )
    mid_x = 480
    mid_y = 224
    body = f"""{frame}
  <text x="36" y="72" class="mono-acc" font-size="10" letter-spacing="1.3">03 / ARCHITECTURAL &amp; IMPLEMENTATION NOTES</text>
  <text x="{w-36}" y="72" class="mono" font-size="9.5" text-anchor="end">VERIFIED IMPLEMENTATIONS IN REPOSITORY SOURCE</text>
  <text x="36" y="104" class="serif" font-size="33">Selected engineering decisions from the codebase<tspan fill="{t['accent']}">.</tspan></text>
  <line x1="16" y1="118" x2="{w-16}" y2="118" class="rule-strong"/>

  <!-- 2x2 Grid Dividers -->
  <line x1="{mid_x}" y1="118" x2="{mid_x}" y2="{h-16}" class="rule"/>
  <line x1="16" y1="{mid_y}" x2="{w-16}" y2="{mid_y}" class="rule"/>

  <!-- Note 01 (Top-Left) -->
  <text x="36" y="140" class="mono-acc" font-size="9.5" letter-spacing="1">NOTE 01 // GITHUB ARCHIVE STREAMING VS. REST QUOTAS</text>
  <text x="36" y="158" class="mono-ink" font-size="10.2">hello · server/routes/projects.js (fetchGithubRepositoryFiles)</text>
  <text x="36" y="177" class="sans" font-size="11.5">
    <tspan x="36" dy="0">Unauthenticated GitHub REST calls cap at 60 req/hr—fatal when indexing</tspan>
    <tspan x="36" dy="16">multi-file repositories. Instead, the indexer resolves HEAD via</tspan>
    <tspan x="36" dy="16">git ls-remote --symref and streams the tarball from codeload.github.com.</tspan>
  </text>

  <!-- Note 02 (Top-Right) -->
  <text x="{mid_x+20}" y="140" class="mono-acc" font-size="9.5" letter-spacing="1">NOTE 02 // TRANSITIVE BLAST-RADIUS &amp; CRITICALITY SCORING</text>
  <text x="{mid_x+20}" y="158" class="mono-ink" font-size="10.2">hello · server/lib/astEngine.js (buildRepositoryAnalysis)</text>
  <text x="{mid_x+20}" y="177" class="sans" font-size="11.5">
    <tspan x="{mid_x+20}" dy="0">After extracting AST CallExpressions and module imports, an upstream</tspan>
    <tspan x="{mid_x+20}" dy="16">BFS walks every caller chain and importing file to compute each</tspan>
    <tspan x="{mid_x+20}" dy="16">function's blastRadiusPercent and weighted criticalityScore (0–99).</tspan>
  </text>

  <!-- Note 03 (Bottom-Left) -->
  <text x="36" y="246" class="mono-acc" font-size="9.5" letter-spacing="1">NOTE 03 // SERVERLESS POSTGRES COLD-START RESILIENCE</text>
  <text x="36" y="264" class="mono-ink" font-size="10.2">hello · server/lib/prisma.js (buildResilientDatabaseUrl)</text>
  <text x="36" y="283" class="sans" font-size="11.5">
    <tspan x="36" dy="0">Neon serverless Postgres instances take 6–12s to wake from suspend,</tspan>
    <tspan x="36" dy="16">tripping Prisma's 5s default timeout. Normalizes pooler URLs at boot</tspan>
    <tspan x="36" dy="16">(connect_timeout=30, pgbouncer=true) with a local JSON fallback store.</tspan>
  </text>

  <!-- Note 04 (Bottom-Right) -->
  <text x="{mid_x+20}" y="246" class="mono-acc" font-size="9.5" letter-spacing="1">NOTE 04 // READ-ONLY SQL EXECUTION GUARDRAILS</text>
  <text x="{mid_x+20}" y="264" class="mono-ink" font-size="10.2">DataPulse · server/utils/sqlSafety.js &amp; schemaService.js</text>
  <text x="{mid_x+20}" y="283" class="sans" font-size="11.5">
    <tspan x="{mid_x+20}" dy="0">LLM-generated queries never run unchecked: only INFORMATION_SCHEMA</tspan>
    <tspan x="{mid_x+20}" dy="16">metadata leaves the DB, while sqlSafety.js rejects any non-SELECT or</tspan>
    <tspan x="{mid_x+20}" dy="16">DDL/DML token and injects a hard LIMIT 200 cap before execution.</tspan>
  </text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Sheet 03 — Engineering & Architecture Notes from Varun Udata's repositories.",
    )


def build_sheet_04_technologies(t: dict) -> str:
    w, h = 960, 416
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 04 // SECTION A–A",
        "TECHNICAL CAPABILITIES & ARCHITECTURAL STACK ELEVATION",
        "SECTION 04 OF 06",
    )
    annex_x = 656
    body = f"""{frame}
  <text x="36" y="72" class="mono-acc" font-size="10" letter-spacing="1.3">04 / TECHNOLOGIES &amp; CAPABILITIES (ARCHITECTURAL CROSS-SECTION A–A)</text>
  <text x="36" y="104" class="serif" font-size="33">Full-stack depth across interface, service, data, and infrastructure<tspan fill="{t['accent']}">.</tspan></text>
  <line x1="16" y1="118" x2="{w-16}" y2="118" class="rule-strong"/>

  <!-- Left Building Cross-Section (Levels 04 down to Foundation) -->
  <!-- Elevation axis column x=16..88 -->
  <line x1="88" y1="118" x2="88" y2="372" class="rule"/>
  <line x1="{annex_x}" y1="118" x2="{annex_x}" y2="{h-16}" class="rule-strong"/>

  <!-- Level 04: Frontend Engineering -->
  <text x="28" y="142" class="mono-acc" font-size="9.5">+12.0m</text>
  <text x="28" y="156" class="mono" font-size="8.5">LVL 04</text>
  <text x="104" y="141" class="mono-acc" font-size="9.5" letter-spacing="1">FRONTEND ENGINEERING</text>
  <text x="104" y="159" class="mono-ink" font-size="10.8">JavaScript (ES2024+) · React.js · Next.js (App Router) · Tailwind CSS</text>
  <text x="104" y="174" class="sans-muted" font-size="11">HTML5 &amp; CSS3 · Responsive UI Systems · Recharts · Framer Motion · WordPress</text>
  <line x1="16" y1="184" x2="{annex_x}" y2="184" class="rule"/>

  <!-- Level 03: Backend & Real-Time -->
  <text x="28" y="206" class="mono-acc" font-size="9.5">+09.0m</text>
  <text x="28" y="220" class="mono" font-size="8.5">LVL 03</text>
  <text x="104" y="205" class="mono-acc" font-size="9.5" letter-spacing="1">BACKEND &amp; REAL-TIME SERVICES</text>
  <text x="104" y="223" class="mono-ink" font-size="10.8">Node.js · Express.js · REST APIs · Socket.IO · Authentication &amp; RBAC</text>
  <text x="104" y="238" class="sans-muted" font-size="11">JWT &amp; Bcrypt Session Flows · Multipart Media (Multer) · Razorpay Webhooks · Electron IPC</text>
  <line x1="16" y1="248" x2="{annex_x}" y2="248" class="rule"/>

  <!-- Level 02: Databases & ORM -->
  <text x="28" y="270" class="mono-acc" font-size="9.5">+06.0m</text>
  <text x="28" y="284" class="mono" font-size="8.5">LVL 02</text>
  <text x="104" y="269" class="mono-acc" font-size="9.5" letter-spacing="1">DATABASES &amp; PERSISTENCE</text>
  <text x="104" y="287" class="mono-ink" font-size="10.8">PostgreSQL · Prisma ORM · Neon Serverless Database · MySQL (mysql2)</text>
  <text x="104" y="302" class="sans-muted" font-size="11">Relational Schema Design · Migrations · Connection Pooling · MongoDB &amp; Mongoose</text>
  <line x1="16" y1="312" x2="{annex_x}" y2="312" class="rule"/>

  <!-- Level 01: DevOps & Infrastructure -->
  <text x="28" y="334" class="mono-acc" font-size="9.5">+03.0m</text>
  <text x="28" y="348" class="mono" font-size="8.5">LVL 01</text>
  <text x="104" y="333" class="mono-acc" font-size="9.5" letter-spacing="1">INFRASTRUCTURE, DEVOPS &amp; TOOLING</text>
  <text x="104" y="351" class="mono-ink" font-size="10.8">Git &amp; GitHub Actions CI/CD · Linux · Docker Fundamentals · Cloud Hosting</text>
  <text x="104" y="366" class="sans-muted" font-size="11">AWS EC2 · PM2 Process Management · Tailscale Mesh VPN · Nginx TLS Proxy · Vercel</text>
  <line x1="16" y1="374" x2="{annex_x}" y2="374" class="rule-strong"/>

  <!-- Hatched Ground Bed: Foundations -->
  <rect x="16.5" y="374.5" width="{annex_x-17}" height="25" fill="url(#hatch)"/>
  <rect x="98" y="378" width="540" height="18" fill="{t['bg']}"/>
  <text x="104" y="390" class="mono-ink" font-size="9.5">CS FOUNDATIONS // Data Structures &amp; Algorithms · System Design · Computer Networks · C</text>

  <!-- Right Column: Dashed Annex (Exploration & Applied AI) -->
  <rect x="{annex_x+16}" y="132" width="{w-annex_x-48}" height="252" class="rule-dash"/>
  <rect x="{annex_x+28}" y="125" width="218" height="14" fill="{t['bg']}"/>
  <text x="{annex_x+32}" y="135" class="mono-acc" font-size="9.5" letter-spacing="1">ANNEX // APPLIED AI &amp; EXPLORATION</text>

  <text x="{annex_x+30}" y="158" class="mono-ink" font-size="10.5">01 · Codebase Intelligence</text>
  <text x="{annex_x+30}" y="173" class="sans-muted" font-size="11">Babel AST parsing, function call graphs,</text>
  <text x="{annex_x+30}" y="187" class="sans-muted" font-size="11">and transitive blast-radius analysis.</text>

  <line x1="{annex_x+30}" y1="198" x2="{w-46}" y2="198" class="rule"/>

  <text x="{annex_x+30}" y="216" class="mono-ink" font-size="10.5">02 · Generative AI &amp; RAG</text>
  <text x="{annex_x+30}" y="231" class="sans-muted" font-size="11">Graph-aware retrieval, multi-stage SLM/LLM</text>
  <text x="{annex_x+30}" y="245" class="sans-muted" font-size="11">routing, and schema-scoped NL-to-SQL.</text>

  <line x1="{annex_x+30}" y1="256" x2="{w-46}" y2="256" class="rule"/>

  <text x="{annex_x+30}" y="274" class="mono-ink" font-size="10.5">03 · System Architecture &amp; DevOps</text>
  <text x="{annex_x+30}" y="289" class="sans-muted" font-size="11">Service boundaries, containerization, automated</text>
  <text x="{annex_x+30}" y="303" class="sans-muted" font-size="11">CI/CD pipelines, and reverse-proxy topologies.</text>

  <line x1="{annex_x+30}" y1="314" x2="{w-46}" y2="314" class="rule"/>

  <text x="{annex_x+30}" y="332" class="mono-ink" font-size="10.5">04 · Academic &amp; Hardware Work</text>
  <text x="{annex_x+30}" y="347" class="sans-muted" font-size="11">Arduino UNO Q embedded C &amp; LED matrix,</text>
  <text x="{annex_x+30}" y="361" class="sans-muted" font-size="11">Post-Quantum Cryptography exploration.</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Sheet 04 — Section A-A Technical Capabilities across Frontend, Backend, Databases, Infrastructure, and Applied AI.",
    )


def build_sheet_05_activity(t: dict, contrib: dict) -> str:
    w, h = 960, 264
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 05 // ACTIVITY LEDGER",
        "VERIFIED GITHUB CONTRIBUTION CADENCE (12 MONTHS)",
        "SOURCE: github.com/varunudata",
    )
    days = contrib["days"]
    total = contrib["total"]
    active_days = sum(1 for d in days if d["count"] > 0)

    # Group into 53 weekly buckets (7 days each)
    weeks = []
    for i in range(0, len(days), 7):
        chunk = days[i : i + 7]
        weeks.append(
            {
                "start": chunk[0]["date"],
                "sum": sum(x["count"] for x in chunk),
            }
        )
    max_wk = max((wk["sum"] for wk in weeks), default=1) or 1

    # Draw weekly bar chart on left (x=36..620)
    chart_x0 = 40
    chart_y_base = 212
    chart_h_max = 76
    bar_step = 10.6
    bar_w = 7.2

    bars_svg = []
    month_labels_svg = []
    seen_months = set()
    month_names = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC",
    }

    for idx, wk in enumerate(weeks):
        bx = chart_x0 + idx * bar_step
        val = wk["sum"]
        if val == 0:
            bh = 3
            fill = t["line"]
        else:
            bh = max(7, round((val / max_wk) * chart_h_max))
            fill = t["accent"] if val >= 9 else t["ink_soft"]
        by = chart_y_base - bh
        bars_svg.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh}" fill="{fill}"/>'
        )
        ym = wk["start"][:7]
        mm = wk["start"][5:7]
        if ym not in seen_months and idx < len(weeks) - 1:
            seen_months.add(ym)
            if len(seen_months) == 1 or wk["start"][8:10] <= "07":
                month_labels_svg.append(
                    f'<text x="{bx:.1f}" y="{chart_y_base+16}" class="mono" font-size="8.5">{month_names.get(mm, mm)}</text>'
                )

    split_x = 636
    body = f"""{frame}
  <line x1="{split_x}" y1="44" x2="{split_x}" y2="{h-16}" class="rule-strong"/>

  <!-- Left Column: Weekly Bar Ledger -->
  <text x="40" y="72" class="mono-acc" font-size="10" letter-spacing="1.2">05 / WEEKLY COMMIT &amp; CONTRIBUTION CADENCE</text>

  <!-- Legend aligned on the top kicker line y=72 (clear of the serif headline at y=104) -->
  <rect x="{split_x-202}" y="64" width="8" height="8" fill="{t['accent']}"/>
  <text x="{split_x-190}" y="72" class="mono" font-size="8.5">PEAK SPRINT WEEK</text>
  <rect x="{split_x-90}" y="64" width="8" height="8" fill="{t['ink_soft']}"/>
  <text x="{split_x-78}" y="72" class="mono" font-size="8.5">ACTIVE WEEK</text>

  <text x="40" y="104" class="serif" font-size="30">{total} verified contributions across the last 12 months<tspan fill="{t['accent']}">.</tspan></text>

  <!-- Reference baseline and guide lines -->
  <line x1="40" y1="{chart_y_base - chart_h_max}" x2="{split_x-24}" y2="{chart_y_base - chart_h_max}" class="rule-dash"/>
  <line x1="40" y1="{chart_y_base - chart_h_max//2}" x2="{split_x-24}" y2="{chart_y_base - chart_h_max//2}" class="rule"/>
  <line x1="40" y1="{chart_y_base}" x2="{split_x-24}" y2="{chart_y_base}" class="rule-strong"/>

  {"".join(bars_svg)}
  {"".join(month_labels_svg)}

  <!-- Right Column: Verified Repository Telemetry -->
  <rect x="{split_x+0.6}" y="44.6" width="{w-16-split_x-1.2}" height="24" fill="{t['bg_card']}"/>
  <line x1="{split_x}" y1="68.5" x2="{w-16}" y2="68.5" class="rule"/>
  <text x="{split_x+16}" y="60" class="mono-med" font-size="9.5" letter-spacing="1">REPOSITORY TELEMETRY (PUBLIC)</text>

  <text x="{split_x+18}" y="92" class="mono" font-size="9.5">PUBLIC REPOSITORIES</text>
  <text x="{w-32}" y="92" class="mono-ink" font-size="11" text-anchor="end">26 Total (25 Original)</text>
  <line x1="{split_x+18}" y1="102" x2="{w-32}" y2="102" class="rule"/>

  <text x="{split_x+18}" y="122" class="mono" font-size="9.5">PRIMARY LANGUAGE SHARE</text>
  <text x="{w-32}" y="122" class="mono-ink" font-size="11" text-anchor="end">JavaScript (15 Repos)</text>
  <line x1="{split_x+18}" y1="132" x2="{w-32}" y2="132" class="rule"/>

  <text x="{split_x+18}" y="152" class="mono" font-size="9.5">ACTIVE CONTRIBUTION DAYS</text>
  <text x="{w-32}" y="152" class="mono-ink" font-size="11" text-anchor="end">{active_days} Days / 53 Weeks</text>
  <line x1="{split_x+18}" y1="162" x2="{w-32}" y2="162" class="rule"/>

  <text x="{split_x+18}" y="182" class="mono" font-size="9.5">RECENT ACTIVE TARGETS (Q4 2026)</text>
  <text x="{split_x+18}" y="200" class="mono-acc" font-size="10">• varunudata/hello (Archon AST + RAG)</text>
  <text x="{split_x+18}" y="216" class="mono-ink" font-size="10">• varunudata/a6news_frontend &amp; backend</text>
  <text x="{split_x+18}" y="232" class="mono-ink" font-size="10">• varunudata/AD_Desktop (ClassFlow)</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        f"Sheet 05 — GitHub Activity Ledger showing {total} verified contributions in the last year across 26 public repositories.",
    )


def build_sheet_06_contact(t: dict) -> str:
    w, h = 960, 216
    frame = sheet_frame(
        w,
        h,
        t,
        "SHEET 06 // CONTACT",
        "DIRECT CHANNELS & PORTFOLIO SPECIFICATION SIGN-OFF",
        "SECTION 06 OF 06",
    )
    c1, c2, c3 = 252, 488, 724
    body = f"""{frame}
  <text x="36" y="72" class="mono-acc" font-size="10" letter-spacing="1.3">06 / DIRECT CHANNELS &amp; AVAILABILITY</text>
  <text x="36" y="106" class="serif" font-size="34">Open to software engineering internships and full-stack roles<tspan fill="{t['accent']}">.</tspan></text>
  <line x1="16" y1="124" x2="{w-16}" y2="124" class="rule-strong"/>

  <!-- 4-Column Directory Block -->
  <line x1="{c1}" y1="124" x2="{c1}" y2="{h-16}" class="rule"/>
  <line x1="{c2}" y1="124" x2="{c2}" y2="{h-16}" class="rule"/>
  <line x1="{c3}" y1="124" x2="{c3}" y2="{h-16}" class="rule"/>

  <text x="36" y="148" class="mono-acc" font-size="9.5" letter-spacing="1">01 · ELECTRONIC MAIL</text>
  <text x="36" y="169" class="mono-ink" font-size="11.5">varunudata@gmail.com</text>
  <text x="36" y="186" class="sans-muted" font-size="10.5">Primary channel for roles &amp; inquiries</text>

  <text x="{c1+20}" y="148" class="mono-acc" font-size="9.5" letter-spacing="1">02 · LINKEDIN</text>
  <text x="{c1+20}" y="169" class="mono-ink" font-size="11.5">in/varunudata</text>
  <text x="{c1+20}" y="186" class="sans-muted" font-size="10.5">Professional network &amp; background</text>

  <text x="{c2+20}" y="148" class="mono-acc" font-size="9.5" letter-spacing="1">03 · GITHUB</text>
  <text x="{c2+20}" y="169" class="mono-ink" font-size="11.5">github.com/varunudata</text>
  <text x="{c2+20}" y="186" class="sans-muted" font-size="10.5">26 public repositories &amp; source code</text>

  <text x="{c3+20}" y="148" class="mono-acc" font-size="9.5" letter-spacing="1">04 · X / TWITTER</text>
  <text x="{c3+20}" y="169" class="mono-ink" font-size="11.5">@udatavarun</text>
  <text x="{c3+20}" y="186" class="sans-muted" font-size="10.5">Engineering notes &amp; updates</text>
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Sheet 06 — Contact and Colophon: varunudata@gmail.com, linkedin.com/in/varunudata, github.com/varunudata, x.com/udatavarun.",
    )


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    contrib = json.loads(CONTRIB_PATH.read_text(encoding="utf-8"))

    builders = {
        "sheet-00-cover": lambda t: build_sheet_00_cover(t),
        "sheet-01-about": lambda t: build_sheet_01_about(t),
        "sheet-02-header": lambda t: build_sheet_02_header(t),
        "work-01-hello": lambda t: build_work_01_hello(t),
        "work-02-datapulse": lambda t: build_work_02_datapulse(t),
        "work-03-nookambika": lambda t: build_work_03_nookambika(t),
        "work-04-a6news": lambda t: build_work_04_a6news(t),
        "sheet-03-engineering": lambda t: build_sheet_03_engineering(t),
        "sheet-04-technologies": lambda t: build_sheet_04_technologies(t),
        "sheet-05-activity": lambda t: build_sheet_05_activity(t, contrib),
        "sheet-06-contact": lambda t: build_sheet_06_contact(t),
    }

    for name, fn in builders.items():
        for mode, palette in THEMES.items():
            out_path = ASSETS_DIR / f"{name}-{mode}.svg"
            svg_text = fn(palette)
            out_path.write_text(svg_text, encoding="utf-8")
            print(f"Wrote {out_path.name} ({len(svg_text):,} bytes)")


if __name__ == "__main__":
    main()
