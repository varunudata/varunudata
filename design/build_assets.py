#!/usr/bin/env python3
"""
Builds the minimalist editorial UI card and clickable contact buttons for Varun Udata's GitHub Profile.
- Focuses strictly on traditional GitHub profile content (Identity, About, Tech Stack, Interests, Connect)
- Zero lengthy project essays, zero clutter, single-screen scannable height
- Warm paper palette in Light mode, restrained carbon-slate in Dark mode, single muted cobalt accent
"""

import base64
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_DIR = ROOT / "design"
FONTS_DIR = DESIGN_DIR / "fonts"
ASSETS_DIR = ROOT / "assets"

THEMES = {
    "light": {
        "canvas": "#FFFFFF",
        "surface": "#F6F4EE",
        "surface_bar": "#EDE9DF",
        "pill": "#FFFFFF",
        "pill_border": "#D8D2C5",
        "border": "#DDD7CA",
        "border_strong": "#C5BEB0",
        "ink": "#181816",
        "ink_soft": "#3E3C38",
        "muted": "#6E6A61",
        "accent": "#2647B2",
        "accent_bg": "#E6ECFA",
        "accent_border": "#B2C3F0",
    },
    "dark": {
        "canvas": "#0D1117",
        "surface": "#121720",
        "surface_bar": "#171D28",
        "pill": "#19202C",
        "pill_border": "#2A3444",
        "border": "#222A36",
        "border_strong": "#333F52",
        "ink": "#F0EEE9",
        "ink_soft": "#C8C4BC",
        "muted": "#878E99",
        "accent": "#6E93F7",
        "accent_bg": "#182442",
        "accent_border": "#314C8C",
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
    .serif {{ font-family: 'Instrument Serif', Georgia, serif; fill: {t['ink']}; }}
    .serif-i {{ font-family: 'Instrument Serif', Georgia, serif; font-style: italic; fill: {t['ink_soft']}; }}
    .sans {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif; fill: {t['ink_soft']}; }}
    .sans-ink {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif; fill: {t['ink']}; }}
    .sans-med {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 500; fill: {t['ink']}; }}
    .sans-muted {{ font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif; fill: {t['muted']}; }}
    .mono {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; fill: {t['muted']}; }}
    .mono-ink {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; fill: {t['ink']}; }}
    .mono-med {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 500; fill: {t['ink']}; }}
    .mono-acc {{ font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 500; fill: {t['accent']}; }}
    .surface {{ fill: {t['surface']}; stroke: {t['border_strong']}; stroke-width: 1.25; }}
    .pill {{ fill: {t['pill']}; stroke: {t['pill_border']}; stroke-width: 1; }}
    .acc-pill {{ fill: {t['accent_bg']}; stroke: {t['accent_border']}; stroke-width: 1; }}
    .divider {{ stroke: {t['border']}; stroke-width: 1; }}
    .divider-strong {{ stroke: {t['border_strong']}; stroke-width: 1.15; }}
    """


def wrap_svg(w: int, h: int, t: dict, body: str, aria_label: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(aria_label)}">
  <defs>
    <style>{build_style(t)}</style>
    <clipPath id="card-clip">
      <rect x="2" y="2" width="{w-4}" height="{h-4}" rx="14"/>
    </clipPath>
  </defs>
  <rect width="{w}" height="{h}" fill="{t['canvas']}"/>
  {body}
</svg>
"""


def draw_pills(
    items: list[str],
    start_x: int,
    start_y: int,
    max_x: int,
    row_step: int = 34,
    accent_first: bool = False,
    char_w: float = 7.0,
    pad_w: int = 22,
    gap: int = 8,
) -> str:
    out = []
    cx = start_x
    cy = start_y
    for idx, label in enumerate(items):
        pw = int(len(label) * char_w + pad_w)
        if cx + pw > max_x and cx > start_x:
            cx = start_x
            cy += row_step
        cls = "acc-pill" if (accent_first and idx == 0) else "pill"
        tcls = "mono-acc" if (accent_first and idx == 0) else "mono-ink"
        out.append(f'<rect x="{cx}" y="{cy}" width="{pw}" height="26" rx="6" class="{cls}"/>')
        out.append(
            f'<text x="{cx + pw/2:.1f}" y="{cy + 16.5}" class="{tcls}" font-size="10.8" text-anchor="middle">{esc(label)}</text>'
        )
        cx += pw + gap
    return "\n  ".join(out)


def build_portfolio_card(t: dict) -> str:
    w, h = 960, 668

    fe_pills = draw_pills(
        ["JavaScript", "React.js", "Next.js", "Tailwind CSS", "HTML & CSS", "WordPress"],
        36,
        396,
        456,
        accent_first=True,
    )
    be_pills = draw_pills(
        ["Node.js", "Express.js", "REST APIs", "Socket.IO", "Authentication & Authorization"],
        512,
        396,
        932,
    )
    db_pills = draw_pills(
        ["PostgreSQL", "Prisma ORM", "Neon Database"],
        36,
        528,
        456,
    )
    tools_pills = draw_pills(
        ["Git & GitHub", "Linux", "Docker & DevOps", "CI/CD Concepts", "Cloud Hosting"],
        512,
        528,
        932,
    )
    interests_pills = draw_pills(
        [
            "DevOps",
            "Generative AI",
            "RAG",
            "Codebase Intelligence",
            "System Design",
            "Software Architecture",
            "DSA",
        ],
        166,
        624,
        944,
        char_w=6.2,
        pad_w=16,
        gap=6,
    )

    body = f"""
  <!-- Main Unified Card Surface -->
  <g clip-path="url(#card-clip)">
    <rect x="2" y="2" width="{w-4}" height="{h-4}" fill="{t['surface']}"/>
    <!-- Top Editorial Bar -->
    <rect x="2" y="2" width="{w-4}" height="38" fill="{t['surface_bar']}"/>
    <!-- Bottom Interests Bar -->
    <rect x="2" y="608" width="{w-4}" height="58" fill="{t['surface_bar']}"/>
  </g>
  <rect x="2" y="2" width="{w-4}" height="{h-4}" rx="14" fill="none" stroke="{t['border_strong']}" stroke-width="1.25"/>

  <!-- Top Header Strip -->
  <rect x="28" y="16" width="8" height="8" rx="1.5" fill="{t['accent']}"/>
  <text x="44" y="24.5" class="mono-med" font-size="10" letter-spacing="1.2">VARUN UDATA  //  DEVELOPER PORTFOLIO</text>
  <text x="{w-28}" y="24.5" class="mono" font-size="10" letter-spacing="0.8" text-anchor="end">B.TECH CSE (AI/ML)  ·  RISHIHOOD UNIVERSITY</text>
  <line x1="2" y1="40" x2="{w-2}" y2="40" class="divider-strong"/>

  <!-- ================= ROW 1: HERO & ABOUT (y=40..312) ================= -->
  <line x1="540" y1="40" x2="540" y2="312" class="divider-strong"/>

  <!-- Left Column: Hero -->
  <text x="36" y="76" class="mono-acc" font-size="10.5" letter-spacing="1.4">FULL-STACK DEVELOPER  ·  SOFTWARE ENGINEER</text>
  <text x="36" y="144" class="serif" font-size="68">Varun Udata<tspan fill="{t['accent']}">.</tspan></text>

  <text x="36" y="182" class="serif-i" font-size="22.5">
    <tspan x="36" dy="0">Building full-stack web applications with clean backend</tspan>
    <tspan x="36" dy="29">architecture, relational data models, and thoughtful UI.</tspan>
  </text>

  <!-- Availability Pill -->
  <rect x="36" y="256" width="388" height="28" rx="14" class="acc-pill"/>
  <circle cx="52" cy="270" r="3.5" fill="{t['accent']}"/>
  <text x="64" y="273.5" class="mono-acc" font-size="10" letter-spacing="0.6">PREPARING FOR SWE INTERNSHIPS &amp; PLACEMENTS</text>

  <!-- Right Column: About Me (Traditional Profile Points) -->
  <text x="568" y="74" class="mono-acc" font-size="10" letter-spacing="1.3">01 / ABOUT ME</text>
  <line x1="568" y1="86" x2="932" y2="86" class="divider"/>

  <text x="568" y="112" class="mono-acc" font-size="10">01</text>
  <text x="594" y="112" class="sans-med" font-size="13">B.Tech in CSE (AI/ML) Student</text>
  <text x="594" y="129" class="sans-muted" font-size="11.5">3rd-year undergraduate at Rishihood University</text>
  <line x1="568" y1="142" x2="932" y2="142" class="divider"/>

  <text x="568" y="166" class="mono-acc" font-size="10">02</text>
  <text x="594" y="166" class="sans-med" font-size="13">Full-Stack Web Development</text>
  <text x="594" y="183" class="sans-muted" font-size="11.5">JavaScript-first across React, Next.js &amp; Node.js</text>
  <line x1="568" y1="196" x2="932" y2="196" class="divider"/>

  <text x="568" y="220" class="mono-acc" font-size="10">03</text>
  <text x="594" y="220" class="sans-med" font-size="13">Backend &amp; Relational Databases</text>
  <text x="594" y="237" class="sans-muted" font-size="11.5">Express, REST APIs, Socket.IO, PostgreSQL &amp; Prisma</text>
  <line x1="568" y1="250" x2="932" y2="250" class="divider"/>

  <text x="568" y="274" class="mono-acc" font-size="10">04</text>
  <text x="594" y="274" class="sans-med" font-size="13">Exploring Systems &amp; Applied AI</text>
  <text x="594" y="291" class="sans-muted" font-size="11.5">DevOps, System Design, RAG &amp; Codebase Intelligence</text>

  <!-- ================= ROW 2: TECH STACK GRID (y=312..608) ================= -->
  <line x1="2" y1="312" x2="{w-2}" y2="312" class="divider-strong"/>
  <rect x="2.6" y="312.6" width="{w-5.2}" height="34" fill="{t['surface_bar']}"/>
  <text x="36" y="333.5" class="mono-acc" font-size="10.5" letter-spacing="1.3">02 / TECHNICAL STACK</text>
  <text x="{w-36}" y="333.5" class="mono" font-size="10" letter-spacing="0.8" text-anchor="end">PRIMARY LANGUAGE: JAVASCRIPT</text>
  <line x1="2" y1="347" x2="{w-2}" y2="347" class="divider-strong"/>

  <!-- Grid Dividers -->
  <line x1="480" y1="347" x2="480" y2="608" class="divider"/>
  <line x1="2" y1="486" x2="{w-2}" y2="486" class="divider"/>

  <!-- Cell 1: Frontend -->
  <text x="36" y="376" class="mono-med" font-size="10.5" letter-spacing="1.1">FRONTEND</text>
  {fe_pills}

  <!-- Cell 2: Backend -->
  <text x="512" y="376" class="mono-med" font-size="10.5" letter-spacing="1.1">BACKEND</text>
  {be_pills}

  <!-- Cell 3: Databases & ORM -->
  <text x="36" y="512" class="mono-med" font-size="10.5" letter-spacing="1.1">DATABASES &amp; ORM</text>
  {db_pills}
  <text x="36" y="578" class="sans-muted" font-size="11.5">Relational schema design, migrations &amp; serverless connection pooling</text>

  <!-- Cell 4: Tools & Technologies -->
  <text x="512" y="512" class="mono-med" font-size="10.5" letter-spacing="1.1">DEVELOPMENT TOOLS &amp; DEVOPS</text>
  {tools_pills}

  <!-- ================= ROW 3: OTHER INTERESTS STRIP (y=608..666) ================= -->
  <line x1="2" y1="608" x2="{w-2}" y2="608" class="divider-strong"/>
  <text x="36" y="641" class="mono-acc" font-size="10" letter-spacing="1.1">03 / INTERESTS</text>
  {interests_pills}
"""
    return wrap_svg(
        w,
        h,
        t,
        body,
        "Varun Udata — Full-Stack Developer & Software Engineer. About Me, Tech Stack, and Engineering Interests.",
    )


def build_contact_button(t: dict, label: str, handle: str, accent: bool = False) -> str:
    w, h = 230, 48
    cls = "acc-pill" if accent else "surface"
    tcls = "mono-acc" if accent else "mono-med"
    body = f"""
  <rect x="2" y="2" width="{w-4}" height="{h-4}" rx="10" class="{cls}"/>
  <text x="18" y="21" class="{tcls}" font-size="10" letter-spacing="1">{esc(label)}</text>
  <text x="18" y="36" class="mono-ink" font-size="10.5">{esc(handle)}</text>
  <text x="{w-18}" y="28" class="{tcls}" font-size="13" text-anchor="end">↗</text>
"""
    return wrap_svg(w, h, t, body, f"{label}: {handle}")


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for old_svg in ASSETS_DIR.glob("*.svg"):
        old_svg.unlink()

    builders = {
        "portfolio": lambda t: build_portfolio_card(t),
        "btn-github": lambda t: build_contact_button(t, "GITHUB", "github.com/varunudata", True),
        "btn-linkedin": lambda t: build_contact_button(t, "LINKEDIN", "in/varunudata"),
        "btn-email": lambda t: build_contact_button(t, "EMAIL", "varunudata@gmail.com"),
        "btn-x": lambda t: build_contact_button(t, "X / TWITTER", "@udatavarun"),
    }

    for name, fn in builders.items():
        for mode, palette in THEMES.items():
            out_path = ASSETS_DIR / f"{name}-{mode}.svg"
            svg_text = fn(palette)
            out_path.write_text(svg_text, encoding="utf-8")
            print(f"Wrote {out_path.name} ({len(svg_text):,} bytes)")


if __name__ == "__main__":
    main()
