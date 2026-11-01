#!/usr/bin/env python3
"""
Typography build for the profile README.

GitHub's Markdown renderer ignores custom fonts, so selected text is rendered
once, here, into SVG *outlines* (no font files needed at view time) using:

    Ithaca            - greeting
    Orbitron          - section headings
  Oxanium           - project / research-note / group titles
  Share Tech Mono   - labels, tags, PR titles, badges

Usage (from the repo root):  python tools/build_type.py
Needs:                       pip install fonttools uharfbuzz

Reads   tools/README.template.md   (placeholders look like @@key@@)
Writes  assets/type/{light,dark}/*.svg, assets/type/badges/*.svg, README.md
Fonts are SIL OFL 1.1 (see tools/fonts/LICENSE-*.txt); icons are simple-icons (CC0).

NOTE: this regenerates README.md from the template. If you edit README.md by
hand, or let a workflow rewrite the LIVE-STATS block, port the change into the
template too, or just don't re-run this script.
"""
import html
import math
import os
import re
import sys

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ASSETS = os.path.join(REPO, "assets", "type")
REL = "assets/type"
PAD = 1.0  # horizontal breathing room inside text SVGs (px)

# Same colours GitHub itself uses for body text / links, so only the font changes.
COLORS = {
    "fg": ("#1f2328", "#e6edf3"),  # (light theme, dark theme)
    "lk": ("#0969da", "#4493f8"),
}


def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# --------------------------------------------------------------------------- fonts
class Face:
    def __init__(self, name, filename):
        path = os.path.join(HERE, "fonts", filename)
        self.name = name
        self.tt = TTFont(path)
        self.upem = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        cap = getattr(self.tt["OS/2"], "sCapHeight", 0)
        if not cap:
            bp = BoundsPen(self.gs)
            self.gs[self.cmap[ord("H")]].draw(bp)
            cap = bp.bounds[3]
        self.cap = cap
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(path)))

    def check(self, text):
        miss = sorted({c for c in text if ord(c) not in self.cmap})
        if miss:
            raise SystemExit(f"{self.name}: missing glyphs {miss} in {text!r}")

    def layout(self, text, size, tracking=0.0, x0=0.0):
        self.check(text)
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": False, "calt": False})
        k = size / self.upem
        x, out = x0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.tt.getGlyphName(info.codepoint), x + pos.x_offset * k, pos.y_offset * k))
            x += pos.x_advance * k + tracking
        return out, (x - x0)

    def path(self, glyphs, baseline, size):
        k = size / self.upem
        pen = SVGPathPen(self.gs, ntos=num)
        for name, gx, gy in glyphs:
            self.gs[name].draw(TransformPen(pen, (k, 0, 0, -k, gx, baseline - gy)))
        return pen.getCommands()


FACES = {}


def load_faces():
    for key, (label, fn) in {
        "ith": ("Ithaca", "Ithaca-LVB75.ttf"),
        "orb": ("Orbitron", "Orbitron-Bold.ttf"),
        "oxb": ("Oxanium Bold", "Oxanium-Bold.ttf"),
        "oxs": ("Oxanium SemiBold", "Oxanium-SemiBold.ttf"),
        "stm": ("Share Tech Mono", "ShareTechMono-Regular.ttf"),
    }.items():
        FACES[key] = Face(label, fn)


# --------------------------------------------------------------------------- registry
REG = []


def T(key, text, font, size, h, color="fg", align=None):
    REG.append(dict(key=key, text=text, alt=text, font=font, size=size, h=h,
                    color=color, align=align, kind="themed"))


def B(key, alt, parts, size, h, tracking, pad, upper, icon=None, icon_color=None):
    REG.append(dict(key=key, text=alt, alt=alt, parts=parts, size=size, h=h, tracking=tracking,
                    pad=pad, upper=upper, icon=icon, icon_color=icon_color, kind="badge"))


# Ithaca: identity
T("greeting", "Hi, I am Himanshu Pathak", "ith", 22, 30)

# Orbitron: section headings
for k, t in [("h_stats", "Live GitHub Stats"), ("h_work", "Selected Work"),
             ("h_research", "Research & Writing"), ("h_skills", "Technical Skills"),
             ("h_oss", "Open Source Contributions"), ("h_interests", "Current Interests")]:
    T(k, t, "orb", 21, 30)

# Oxanium: project titles, research-note titles, group (summary) titles
T("c_exec", "Let Execution Do the Teaching", "oxb", 14, 22, "lk")
T("c_vapor", "VaporWall", "oxb", 14, 22, "lk")
T("c_fraud", "Fraud Radar", "oxb", 14, 22, "lk")
for k, t in [("r_policy", "Policy Gradients and the Meaning of Credit"),
             ("r_reward", "Reward Shaping Without Changing the Task"),
             ("r_uncert", "What Uncertainty Can Tell a Planner"),
             ("r_world", "The World Models Today")]:
    T(k, t, "oxb", 14.5, 22, "lk", "absmiddle")
T("sum_research", "Selected research notes and interactive experiments", "oxs", 15, 24, "fg", "absmiddle")
for k, t in [("sum_gg", "ECSoC'26 — Go Gatekeeper: Concurrency, WebSocket Security & Runtime Reliability"),
             ("sum_mf", "ECSoC'26 — MediFlow: AI Security, Authorization & Backend Reliability"),
             ("sum_yh", "ECSoC'26 — YuvaHub: Database Security, Messaging & Cache Management"),
             ("sum_dt", "ECSoC'26 — Developer Tooling: Code Retrieval, Tracing & Project Detection"),
             ("sum_sr", "ECSoC'26 — Security & Resource Management")]:
    T(k, t, "oxs", 15, 24, "fg", "absmiddle")

# Share Tech Mono: labels, tags, PR titles
for k, t in [("lbl_ml", "Machine Learning"), ("lbl_lang", "Languages"),
             ("lbl_be", "Backend & Systems"), ("lbl_web", "Web & Data")]:
    T(k, t, "stm", 15, 24)
T("s_exec", "GRPO · SFT · Execution-based verification", "stm", 11.5, 18)
T("s_vapor", "eBPF/XDP · ONNX", "stm", 11.5, 18)
T("s_ml", "+ Hugging Face · ONNX", "stm", 11.5, 18)
T("s_be", "+ eBPF/XDP · WebSockets", "stm", 11.5, 18)
for k, t in [
    ("gg8", "Prevent a goroutine leak during room teardown — #8"),
    ("gg9", "Add per-IP WebSocket rate limiting — #9"),
    ("gg17", "Validate WebSocket Origin headers — #17"),
    ("gg20", "Stop exposing session codes through /stats — #20"),
    ("gg30", "Enforce WebSocket message limits and keepalives — #30"),
    ("gg18", "Implement graceful shutdown — #18"),
    ("gg19", "Verify downloaded CLI binaries with SHA-256 — #19"),
    ("mf443", "Harden AI prompt construction against untrusted input — #443"),
    ("mf394", "Validate facility ownership during registration — #394"),
    ("mf445", "Handle transient Firestore approval failures correctly — #445"),
    ("mf96", "Add rate limiting to callable Cloud Functions — #96"),
    ("yh619", "Prevent Firestore privilege escalation — #619"),
    ("yh565", "Add RabbitMQ publisher confirms and dead-letter queues — #565"),
    ("yh562", "Add LRU eviction to the persistent API cache — #562"),
    ("dw173", "Add AST-based symbol-level indexing — DevWhisper #173"),
    ("dg19", "Add scoped symbol tracing — DiffGuardian #19"),
    ("dg16", "Add JSON output to the trace CLI — DiffGuardian #16"),
    ("rs37", "Improve Python project detection fallbacks — RepoStart #37"),
    ("sp1695", "Prevent DNS rebinding in webhook requests — Semantic Plagiarism Detector #1695"),
    ("sp1697", "Add concurrent SQLite thread-safety stress tests — Semantic Plagiarism Detector #1697"),
    ("ws2138", "Fix WebAssembly memory leaks in PDF signature verification — WorkSphere #2138"),
    ("pp306", "Prevent open redirects in download URLs — PrepPilot #306"),
]:
    T(k, t, "stm", 14, 22, "lk", "absmiddle")

# Badges (Share Tech Mono). Replaces the shields.io images with identical wording.
DARK, WHITE = "#0d1117", "#ffffff"
B("bd_portfolio", "Portfolio", [("Portfolio", DARK, WHITE)], 11.5, 28, 1.2, 14, True, "googlechrome", "#4285F4")
B("bd_github", "GitHub", [("GitHub", DARK, WHITE)], 11.5, 28, 1.2, 14, True, "github", "#ffffff")
B("bd_linkedin", "LinkedIn", [("LinkedIn", DARK, WHITE)], 11.5, 28, 1.2, 14, True, "linkedin", "#2dd4bf")
B("bd_hf", "Hugging Face", [("Hugging Face", DARK, WHITE)], 11.5, 28, 1.2, 14, True, "huggingface", "#FFD21E")
B("bd_ecsoc", "ECSoC'26: 50+ merged PRs across 9 repositories",
  [("ECSoC'26", DARK, WHITE), ("50+ merged PRs across 9 repos", "#ffd21e", "#333333")],
  11.5, 28, 1.2, 14, True)
for k, t in [("bd_i_rl", "Reinforcement Learning"), ("bd_i_post", "LLM Post-Training"),
             ("bd_i_eval", "Coding-Agent Evaluation"), ("bd_i_reward", "Reward Design"),
             ("bd_i_unc", "Model Uncertainty"), ("bd_i_wm", "World Models"),
             ("bd_i_sys", "Systems Engineering")]:
    B(k, t, [(t, "#0f2027", WHITE)], 12, 20, 0.3, 9, False)

ICON, GAP = 14, 7


# --------------------------------------------------------------------------- rendering
def attr(s):
    return html.escape(s, quote=True)


def render_themed(e, theme):
    face = FACES[e["font"]]
    glyphs, adv = face.layout(e["text"], e["size"], 0.0, PAD)
    w = math.ceil(adv + 2 * PAD)
    base = e["h"] / 2 + face.cap * e["size"] / face.upem / 2
    d = face.path(glyphs, base, e["size"])
    fill = COLORS[e["color"]][0 if theme == "light" else 1]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{e["h"]}" '
           f'viewBox="0 0 {w} {e["h"]}" role="img" aria-label="{attr(e["text"])}">'
           f'<title>{html.escape(e["text"], quote=False)}</title><path fill="{fill}" d="{d}"/></svg>\n')
    return svg, w


def icon_path(name):
    with open(os.path.join(HERE, "icons", name + ".svg"), encoding="utf-8") as f:
        return re.search(r'<path d="([^"]+)"', f.read()).group(1)


def render_badge(e):
    face = FACES["stm"]
    size, h, tr, pad = e["size"], e["h"], e["tracking"], e["pad"]
    base = h / 2 + face.cap * size / face.upem / 2
    x, rects, items = 0.0, [], []
    for i, (text, bg, fg) in enumerate(e["parts"]):
        t = text.upper() if e["upper"] else text
        has_icon = i == 0 and e["icon"]
        tx = x + pad + ((ICON + GAP) if has_icon else 0)
        glyphs, adv = face.layout(t, size, tr, tx)
        tw = adv - (tr if tr else 0)
        seg_w = (tx - x) + tw + pad
        rects.append(f'<rect x="{num(x)}" width="{num(seg_w)}" height="{h}" fill="{bg}"/>')
        if has_icon:
            items.append(f'<path transform="translate({num(x + pad)} {num((h - ICON) / 2)}) scale({num(ICON / 24)})" '
                         f'fill="{e["icon_color"]}" d="{icon_path(e["icon"])}"/>')
        items.append(f'<path fill="{fg}" d="{face.path(glyphs, base, size)}"/>')
        x += seg_w
    w = math.ceil(x)
    rx = 3 if h >= 28 else 0
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{attr(e["alt"])}"><title>{html.escape(e["alt"], quote=False)}</title>'
           f'<clipPath id="c"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
           f'<g clip-path="url(#c)">{"".join(rects)}{"".join(items)}</g></svg>\n')
    return svg, w


def markup(e):
    alt = attr(e["alt"]).replace("&#x27;", "'")
    al = f' align="{e["align"]}"' if e.get("align") else ""
    if e["kind"] == "badge":
        return f'<img src="{REL}/badges/{e["key"]}.svg" alt="{alt}" />'
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{REL}/dark/{e["key"]}.svg">'
            f'<img src="{REL}/light/{e["key"]}.svg" alt="{alt}"{al} /></picture>')


def build():
    load_faces()
    for sub in ("light", "dark", "badges"):
        os.makedirs(os.path.join(ASSETS, sub), exist_ok=True)
    widths = {}
    for e in REG:
        if e["kind"] == "badge":
            svg, w = render_badge(e)
            with open(os.path.join(ASSETS, "badges", e["key"] + ".svg"), "w", encoding="utf-8") as f:
                f.write(svg)
        else:
            for theme in ("light", "dark"):
                svg, w = render_themed(e, theme)
                with open(os.path.join(ASSETS, theme, e["key"] + ".svg"), "w", encoding="utf-8") as f:
                    f.write(svg)
        widths[e["key"]] = w

    by_key = {e["key"]: e for e in REG}
    with open(os.path.join(HERE, "README.template.md"), encoding="utf-8") as f:
        tpl = f.read()
    used = set()

    def sub_(m):
        used.add(m.group(1))
        return markup(by_key[m.group(1)])

    out = re.sub(r"@@([A-Za-z0-9_]+)@@", sub_, tpl)
    assert "@@" not in out, "unreplaced placeholder"
    unused = set(by_key) - used
    assert not unused, f"registry entries never used in template: {sorted(unused)}"
    with open(os.path.join(REPO, "README.md"), "w", encoding="utf-8") as f:
        f.write(out)
    return widths


if __name__ == "__main__":
    wd = build()
    if "--widths" in sys.argv:
        for k, v in wd.items():
            print(f"{k:14s} {v:5d}px")
    print(f"built {len(REG)} assets")
