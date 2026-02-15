#!/usr/bin/env python3
"""
Generate the English-only "How to Use" PDF for ZIP-your-Research (v1.3.2).

This document is aligned to the current v1.3.2 release zip layout:
- ZIP-only boot: migration detect -> application guide -> intake -> MODE_LOCK -> CONFIRM -> locked execution.
- Default web browsing policy: ALLOW (unless user explicitly forbids).
- Readability policy: do NOT print internal routing/debug metadata by default.
  Optional debug trace is opt-in via `DEBUG_TRACE=ON`.

Usage:
  pip install reportlab
  python3 tools/how_to_use/gen_ZIP-your-Research_HowToUse_v1_3_2.py

Output:
  ZIP-your-Research_How_to_Use_v1.3.2.pdf
"""

from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.pdfgen import canvas
import math


# -----------------------------
# Metadata (edit here if needed)
# -----------------------------
PROJECT = "ZIP-your-Research"
VERSION = "v1.3.2 (public tag)"
VERSION_TIME = "2026-02-15"
OUT_PDF = "docs/how_to_use/ZIP-your-Research_How_to_Use_v1.3.2.pdf"

# Repo URL: keep a placeholder to avoid inventing a URL.
REPO_URL_PLACEHOLDER = "<PUT_YOUR_REPO_URL_HERE>"

# If your release zip has a different name, edit here:
RELEASE_ZIP_NAME = "ZIP-your-Research_v1.3.2_release.zip"
UNZIP_PARENT = "ASR"
RELEASE_DIR_NAME = f"{UNZIP_PARENT}/ZIP-your-Research"


# -----------------------------
# Styles (smaller fonts + tighter leading)
# -----------------------------
def build_styles():
    base = getSampleStyleSheet()

    styles = {}
    styles["Title"] = ParagraphStyle(
        "Title", parent=base["Title"],
        fontName="Helvetica-Bold", fontSize=23, leading=26,
        spaceAfter=12
    )
    styles["Subtitle"] = ParagraphStyle(
        "Subtitle", parent=base["Normal"],
        fontName="Helvetica", fontSize=11.0, leading=14.8,
        textColor=colors.HexColor("#333333"),
        spaceAfter=12
    )
    styles["H1"] = ParagraphStyle(
        "H1", parent=base["Heading1"],
        fontName="Helvetica-Bold", fontSize=15.0, leading=18.0,
        spaceBefore=7, spaceAfter=6
    )
    styles["H2"] = ParagraphStyle(
        "H2", parent=base["Heading2"],
        fontName="Helvetica-Bold", fontSize=11.6, leading=14.8,
        spaceBefore=6, spaceAfter=5
    )
    styles["Body"] = ParagraphStyle(
        "Body", parent=base["BodyText"],
        fontName="Helvetica", fontSize=9.2, leading=12.8,
        spaceAfter=5
    )
    styles["Small"] = ParagraphStyle(
        "Small", parent=base["BodyText"],
        fontName="Helvetica", fontSize=8.2, leading=11.2,
        textColor=colors.HexColor("#333333"),
        spaceAfter=3
    )
    styles["Code"] = ParagraphStyle(
        "Code", parent=base["Code"],
        fontName="Courier", fontSize=8.2, leading=10.6,
        spaceAfter=7
    )
    styles["BoxTitle"] = ParagraphStyle(
        "BoxTitle", parent=base["Heading3"],
        fontName="Helvetica-Bold", fontSize=9.2, leading=11.2,
        textColor=colors.white, spaceAfter=3
    )
    return styles


# -----------------------------
# Header / Footer
# -----------------------------
def header_footer(c: canvas.Canvas, doc):
    c.saveState()
    w, h = A4

    # top rule
    c.setStrokeColor(colors.HexColor("#DDDDDD"))
    c.setLineWidth(0.6)
    c.line(2*cm, h-2.1*cm, w-2*cm, h-2.1*cm)

    c.setFont("Helvetica", 8.2)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(2*cm, h-1.65*cm, f"{PROJECT} - How to Use")

    # bottom rule
    c.setStrokeColor(colors.HexColor("#DDDDDD"))
    c.line(2*cm, 1.7*cm, w-2*cm, 1.7*cm)

    c.setFont("Helvetica", 8.2)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(2*cm, 1.1*cm, f"Version: {VERSION}")
    c.drawRightString(w-2*cm, 1.1*cm, f"Page {doc.page}")
    c.restoreState()


# -----------------------------
# Small UI helpers
# -----------------------------
def make_badge(text, fill="#1F6FEB"):
    t = Table([[text]])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(fill)),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
        ("BOX", (0, 0), (-1, -1), 0, colors.white),
    ]))
    return t


def workflow_drawing():
    d = Drawing(520, 165)

    def box(x, y, w, h, top, bottom=None):
        d.add(Rect(x, y, w, h, rx=8, ry=8,
                   fillColor=colors.HexColor("#F6F8FA"),
                   strokeColor=colors.HexColor("#D0D7DE"),
                   strokeWidth=1))
        d.add(String(x+10, y+h-20, top, fontName="Helvetica-Bold",
                     fontSize=10.0, fillColor=colors.HexColor("#111827")))
        if bottom:
            d.add(String(x+10, y+h-38, bottom, fontName="Helvetica",
                         fontSize=8.7, fillColor=colors.HexColor("#374151")))

    box(10, 92, 165, 60, "Web chat (Deep)", "Upload zip -> intake -> mode lock")
    box(190, 92, 165, 60, "Locked execution", "A/B/C/E audits, writing, checklists")
    box(370, 92, 140, 60, "Outputs", "LaTeX, tables, patch plans")
    box(10, 15, 230, 60, "WSL2 CLI (optional)", "route.py + providers + repropack init")
    box(260, 15, 250, 60, "Back to Web", "paste evidence JSON -> higher confidence")

    def arrow(x1, y1, x2, y2):
        d.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor("#6B7280"), strokeWidth=1.1))
        ang = math.atan2(y2-y1, x2-x1)
        ah = 6
        d.add(Line(x2, y2,
                   x2-ah*math.cos(ang-math.pi/6), y2-ah*math.sin(ang-math.pi/6),
                   strokeColor=colors.HexColor("#6B7280"), strokeWidth=1.1))
        d.add(Line(x2, y2,
                   x2-ah*math.cos(ang+math.pi/6), y2-ah*math.sin(ang+math.pi/6),
                   strokeColor=colors.HexColor("#6B7280"), strokeWidth=1.1))

    arrow(175, 122, 190, 122)
    arrow(355, 122, 370, 122)
    arrow(240, 45, 260, 45)
    arrow(125, 92, 125, 75)
    arrow(385, 75, 385, 92)
    d.add(String(160, 78, "feedback loop", fontName="Helvetica", fontSize=8.2,
                 fillColor=colors.HexColor("#6B7280")))
    return d


def add_bullets(story, items: Sequence[str], style: ParagraphStyle):
    for s in items:
        story.append(Paragraph("• " + s, style))


def add_code(story, code: str, style: ParagraphStyle):
    story.append(Preformatted(code.rstrip("\n"), style))


def resolve_col_widths(col_widths, total_width, min_col_width=1*cm):
    """
    Replace None in col_widths with remaining width (split evenly if multiple Nones).
    Also guarantees each None-column has at least min_col_width, scaling fixed widths down if needed.
    """
    if not col_widths:
        return None

    n_none = sum(1 for w in col_widths if w is None)
    if n_none == 0:
        return col_widths

    fixed = [w for w in col_widths if w is not None]
    fixed_sum = sum(fixed) if fixed else 0.0
    need = n_none * min_col_width

    # If fixed widths + minimal None widths exceed total, scale fixed widths down.
    if fixed_sum + need > total_width:
        if fixed_sum > 0:
            scale = max((total_width - need) / fixed_sum, 0.05)
        else:
            scale = 0.0
        out = []
        for w in col_widths:
            if w is None:
                out.append(min_col_width)
            else:
                out.append(w * scale)
        return out

    # Otherwise distribute remaining width to None columns
    remaining = total_width - fixed_sum
    per = max(remaining / n_none, min_col_width)

    out = []
    for w in col_widths:
        out.append(per if w is None else w)
    return out


def make_table(
    rows: List[List[Union[str, Paragraph]]],
    col_widths: Optional[List[float]] = None,
    header_dark: bool = False
):
    t = Table(rows, colWidths=col_widths)
    if header_dark:
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9.0),
            ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D0D7DE")),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E5E7EB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFCFE")]),
        ]))
    else:
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F6F8FA")),
            ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D0D7DE")),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E5E7EB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFCFE")]),
        ]))
    return t


# -----------------------------
# Content spec (organized)
# -----------------------------
@dataclass
class Block:
    kind: str
    payload: object


@dataclass
class Section:
    title: str
    blocks: List[Block]


def build_sections(styles):
    sections: List[Section] = []


    # 0) What’s inside + defaults (aligned with the v1.3.2 release zip)
    sections.append(Section(
        title="0. What’s inside (repo inventory) + defaults",
        blocks=[
            Block("p", "This release is a prompt-pack repository. It contains (i) a ZIP-only boot protocol, (ii) a deterministic router + skill library, and (iii) optional local tools for evidence collection and reproducibility scaffolding."),
            Block("h2", "0.1 Repository layout (high level)"),
            Block("table", {
                "header_dark": False,
                "col_widths": [4.6*cm, None],
                "rows": [
                    ["Path", "Purpose"],
                    ["AUTOBOOT_v1.3.md", "One-file entrypoint: what to paste in the first message to trigger bootstrap + intake."],
                    ["boot/", "Bootstrap, migration, intake interview, Mode Lock format + schema, locked response templates, routing decision record."],
                    ["router/", "Deterministic router, taxonomy + weights, default intake profile (including defaults)."],
                    ["skills/", "Skill library (S2xx research_core, S3xx experiments, S4xx reproducibility, S5xx paper_ops, writing_engine)."],
                    ["tools/", "Local utilities (ra_cli.py for providers + repropack init; plus build/validate scripts)."],
                    ["docs/", "Quickstart + workflows + developer API + legal/safety statements + maintainer intro + how-to-use PDF."],
                    ["templates/", "Evidence/citation policy, skill authoring template, workflow chain template."],
                    ["interfaces/", "Provider contract, free API notes, extension hooks, config.example.yaml."],
                    ["archive/", "Legacy snapshots (kept for traceability; not required for normal use)."],
                ]
            }),
            Block("p", "Where to find key policy docs (these are included in the zip)"),
            Block("bullets", [
                "Maintainer profile: docs/ABOUT_MAINTAINER.md",
                "Legal & safe-use policy: docs/LEGAL.md",
                "Prompt-injection & mode-drift defense: docs/SECURITY_PROMPT_INJECTION.md",
                "How-to-use PDF: docs/how_to_use/ZIP-your-Research_How_to_Use_v1.3.2.pdf",
            ]),
            Block("h2", "0.2 Skill library (what you can ask for)"),
            Block("bullets", [
                "A/B/C/E audits: Logic (A), Method (B), Calculation (C), Innovation correctness (E).",
                "research_core (S2xx): problem framing, novelty map, claim-evidence matrix, assumption/risk audits, proof gap finding, paper interpretation.",
                "experiments (S3xx): minimal decidable experiments, ablation planning, evaluation protocol linting, metrics sanity, error analysis, reporting templates.",
                "reproducibility (S4xx): repro checklist, environment pinning, dataset access + checksums, command/entrypoint documentation, artifact manifests.",
                "paper_ops (S5xx): rebuttal generator, reviewer simulator, submission readiness gate, camera-ready checklist, figure/table audits, limitation builders.",
                "writing_engine: structured rewriting modules for paper sections, tone alignment, claim calibration.",
            ]),
            Block("h2", "0.3 Defaults (unless you override in the intake)"),
            Block("table", {
                "header_dark": True,
                "col_widths": [5.6*cm, None],
                "rows": [
                    ["Setting", "Default value (v1.3.2)"],
                    ["Top priorities", "A_logic, B_method, C_calculation, E_innovation_correctness"],
                    ["Intake depth", "deep"],
                    ["Strictness", "high (prefer UNKNOWN to guessing)"],
                    ["Output mode", "audit_first"],
                    ["Citation mode", "conservative"],
                    ["Web browsing policy", "ALLOW (default on)"],
                    ["Debug trace", "OFF (opt-in only via DEBUG_TRACE=ON)"],
                    ["Change protocol", "Prefer: start a new chat + paste MIGRATION PROMPT; otherwise request change explicitly and wait for confirmation."],
                ]
            }),
        ]
    ))




    # 1) Quick start (aligned with boot/07 + README)
    sections.append(Section(
        title="1. 5-minute quick start (ZIP-only boot)",
        blocks=[
            Block("p", "This is the shortest safe path designed for high correctness under limited time."),
            Block("h2", "Step 1 - Start a fresh chat and upload the release zip"),
            Block("bullets", [
                "Upload the ZIP. (No other context is required.)",
                "Optional: paste a MIGRATION PROMPT (English) if resuming a previous chat.",
                "Otherwise: say “start” (or say nothing).",
            ]),
            Block("h2", "What's inside"),
            Block("bullets", [
                "boot/: bootstrap, guardrails, prompt-shield, pre-lock rollback.",
                "router/: routing taxonomy and priority rules.",
                "skills/: task playbooks (A/B/C/E audits, novelty, writing, experiments, reproducibility).",
                "tools/: local CLI (providers search, repropack scan, validators) + PDF generator.",
                "docs/: quickstart, usage, workflows, security, dev notes.",
                "templates/: copy/paste patterns (checklists, evidence formats, LaTeX patches).",
                "interfaces/: optional config for hooks (e.g., DOI de-dup).",
            ]),
            Block("h2", "Step 2 - Intake interview (deep by default)"),
            Block("p", "The assistant will ask structured questions to lock scope, strictness, and output format. Deep mode asks A/B/C/E 5 questions each, and other domains 3 questions each."),
            Block("h2", "Step 3 - Mode lock generation + activation"),
            Block("bullets", [
                "The assistant generates MODE_LOCK.md + MODE_LOCK.json.",
                "You reply: CONFIRM.",
                "Execution Gate: before CONFIRM, do not execute substantive tasks.",
                "If you ask a normal question pre-lock, you will get a clear warning; a short quick answer may be given; then you are routed back to intake.",
            ]),
            Block("h2", "Step 4 - Execute in short sprints (recommended)"),
            Block("p", "Ask for one deliverable per sprint (audit table, LaTeX patch, proof skeleton, risk register). This increases precision and lowers drift."),
            Block("h2", "Copy/paste starter lines"),
            Block("code",
                  "NO-MIGRATION. Bootstrap from the uploaded zip and start Deep intake.\n"
                  "MIGRATION-PASTED. Bootstrap + Deep intake."),
            Block("h2", "Default overrides (if you do not specify)"),
            Block("code",
                  "SESSION_OVERRIDES:\n"
                  "  top_priorities: [A_logic, B_method, C_calculation, E_innovation_correctness]\n"
                  "  intake_depth: deep              # tight | standard | deep\n"
                  "  strictness: high\n"
                  "  output_mode: audit_first        # audit_first | rewrite_first | mixed\n"
                  "  citation_mode: conservative     # conservative | normal\n"
                  "  web_browsing_policy: ALLOW      # default is ALLOW\n"
                  "  debug_trace: OFF                # default is OFF (opt-in via DEBUG_TRACE=ON)"),
        ]
    ))

    # 2) Operating model + guardrails
    sections.append(Section(
        title="2. Guardrails: no fabrication, readability-first, execution gate",
        blocks=[
            Block("p", "The two most common failure modes in long research chats are (1) fabrication of missing details and (2) prompt drift (rules silently change over time). This release mitigates both with explicit guardrails and a strict sequence."),
            Block("h2", "2.1 Hard constraints (enforced by protocol)"),
            Block("table", {
                "header_dark": False,
                "col_widths": [4.2*cm, None],
                "rows": [
                    ["Constraint", "Meaning"],
                    ["No fabrication", "If a required fact is missing: mark UNKNOWN and ask the minimal missing input."],
                    ["Readability-first", "User-visible answers must be natural and professional; no YAML/debug dumps."],
                    ["Execution Gate", "Before Mode Lock activation (CONFIRM), do not execute substantive research tasks."],
                ]
            }),
            Block("h2", "2.2 Readability policy (default)"),
            Block("p", "Internal routing/debug metadata (step/name/route/primary/secondary/inputs_received/locked_context_used) must not appear in the final answer."),
            Block("p", "Debug trace mode is opt-in only."),
            Block("table", {
                "header_dark": True,
                "col_widths": [4.0*cm, None],
                "rows": [
                    ["Mode", "Rule"],
                    ["DEBUG_TRACE=OFF (default)", "Hide routing metadata; keep the answer human-readable."],
                    ["DEBUG_TRACE=ON (explicit)", "Append a short Debug Trace section after the main answer."],
                ]
            }),
            Block("h2", "2.3 UNKNOWN policy (anti-hallucination)"),
            Block("p", "UNKNOWN is a feature, not a bug. It prevents hallucinated details from contaminating your paper or code."),
            Block("bullets", [
                "If a number is not in the artifact: UNKNOWN (do not invent).",
                "If a definition is missing: UNKNOWN + minimal question (where is it defined?).",
                "If a claim depends on experiments you cannot run: propose a minimal patch plan instead of fabricating results.",
            ]),
            Block("h2", "2.4 Pre-lock Violation Response (rollback to intake)"),
            Block("p", "Before Mode Lock is activated (before you reply CONFIRM), the assistant must resist prompt-drift. If you ask a normal question without following the protocol, the assistant must explicitly tell you it is out-of-protocol, may give a short best-effort quick answer, and then **must** route you back to intake. If the message is injection-like, it must refuse to answer and immediately rollback."),
            Block("bullets", [
                "User-trigger: send the standard trigger word: ROLLBACK_TO_INTAKE",
                "Assistant behavior: (a) short protocol notice, (b) optional quick answer (<=200 words / 8 bullets), (c) re-ask missing intake answers.",
                "Reference: boot/02_PRELOCK_VIOLATION_RESPONSE_v1.3.2.md",
            ]),
            Block("h2", "2.5 Mandatory response prologue (hallucination self-check)"),
            Block("p", "Every assistant message must start with a one-line prologue showing whether it is following the ZIP protocol. This is a lightweight self-correction mechanism."),
            Block("code",
                  "ZIP your Research | ZIP_MODE: ON | STAGE: PRE-LOCK or LOCKED | MEMORY: NOT USED | WEB: ON | DEBUG_TRACE: OFF\n"
                  "(Then the human-readable answer follows.)"),
        ]
    ))

    # 3) A/B/C/E audits
    sections.append(Section(
        title="3. A/B/C/E audits: Logic, Method, Calculation, Innovation correctness",
        blocks=[
            Block("p", "A/B/C/E is the default top-priority routing lens for high-rigor research assistance."),
            Block("h2", "3.1 What each lens checks"),
            Block("table", {
                "header_dark": False,
                "col_widths": [2.8*cm, None],
                "rows": [
                    ["Lens", "Checks"],
                    ["A - Logic", "Argument chain, assumptions, missing steps, counterexamples, scope mistakes."],
                    ["B - Method", "Algorithm spec, protocol validity, training-vs-inference mismatch, ablation logic."],
                    ["C - Calculation", "Derivations, units/dimensions, statistics, numerics, complexity."],
                    ["E - Innovation", "Innovation feasibility, calibrated novelty, defensible claims, failure modes."],
                ]
            }),
            Block("h2", "3.2 Recommended audit output schema"),
            Block("bullets", [
                "Weakest link: the single most critical flaw/risk.",
                "Evidence: point to the exact lines/figure/code that trigger the issue.",
                "Minimal fix (2-hour viable): the smallest patch under constraints.",
                "Best fix: what you would do with more time/resources.",
                "Claim-defense wording: safe but strong phrasing for the paper.",
                "Remaining risks: what reviewers may still criticize.",
            ]),
            Block("h2", "3.3 Calculation sanity checklist (C lens)"),
            Block("bullets", [
                "Dimensional analysis: do units match?",
                "Edge cases: boundary values and degenerate cases.",
                "Numerical stability: logs, exponentials, small denominators, overflow.",
                "Complexity: time/memory hotspots.",
                "Statistics: correct baselines, confidence intervals, leakage checks.",
            ]),
        ]
    ))

    # 4) Web-first prompting pattern
    sections.append(Section(
        title="4. Web-first deep reasoning: how to ask for high-precision work",
        blocks=[
            Block("p", "Use Web chat for the highest quality reasoning: audits, proofs, writing, and research planning."),
            Block("h2", "4.1 The minimal high-signal prompt"),
            Block("table", {
                "header_dark": False,
                "col_widths": [4.0*cm, None],
                "rows": [
                    ["You provide", "Assistant does"],
                    ["Artifact chunk", "Work on a bounded piece: one section, one lemma, one table, one file."],
                    ["Task", "Audit / verify / rewrite / plan experiments / novelty map."],
                    ["Constraints", "No new experiments; 2-hour max; must not change claims; etc."],
                    ["Output format", "Bullets / LaTeX / table / checklist; enforce UNKNOWN markers."],
                ]
            }),
            Block("h2", "4.2 Good vs bad scope"),
            Block("p", "Avoid"),
            Block("bullets", [
                "\"Read my whole paper and fix everything.\"",
                "\"Find novelty\" without evidence output from provider tools.",
                "\"Add many experiments\" when you cannot run them.",
            ]),
            Block("p", "Prefer"),
            Block("bullets", [
                "\"Audit Methods Section 3.2 with A/B/C/E; output a minimal patch plan.\"",
                "\"Check this derivation line-by-line; mark UNKNOWN if a definition is missing.\"",
                "\"Given retrieved papers JSON + my contributions, build a novelty map + safe claim wording.\"",
            ]),
        ]
    ))

    # 5) Local tooling in WSL2 (aligned with README + actual tools)
    sections.append(Section(
        title="5. Optional local tooling in WSL2 (Windows): route + providers + repropack",
        blocks=[
            Block("p", "Local tools are optional, but useful for (i) deterministic routing suggestions, (ii) evidence collection via public scholarly APIs, and (iii) reproducibility skeleton templates."),
            Block("h2", "5.1 Setup (WSL2 Ubuntu)"),
            Block("code",
                  "# In WSL2 Ubuntu:\n"
                  "sudo apt update\n"
                  "sudo apt install -y python3 python3-pip unzip git\n"
                  f"unzip {RELEASE_ZIP_NAME} -d {UNZIP_PARENT}\n"
                  f"cd {RELEASE_DIR_NAME}\n"
                  "python3 -m pip install -r requirements.txt"),
            Block("h2", "5.2 Build generated artifacts (optional)"),
            Block("code",
                  "python3 tools/build_all.py\n"
                  "# Deterministic routing suggestions (Top-K skills)\n"
                  "python3 router/route.py \"方法正确性核查：请帮我检查推导是否成立\" --topk 5"),
            Block("h2", "5.3 Provider tools: literature evidence JSON"),
            Block("p", "The built-in provider CLI queries public endpoints. It is meant for evidence collection (titles, years, DOIs/IDs, URLs)."),
            Block("code",
                  "# List available providers\n"
                  "python3 tools/ra_cli.py providers list\n\n"
                  "# Search a single provider (JSON output)\n"
                  "python3 tools/ra_cli.py providers search --provider openalex \\\n"
                  "  --query \"diffusion policy offline reinforcement learning\" --limit 20 > openalex.json\n\n"
                  "python3 tools/ra_cli.py providers search --provider crossref \\\n"
                  "  --query \"implicit q-learning\" --limit 20 > crossref.json\n\n"
                  "python3 tools/ra_cli.py providers search --provider arxiv \\\n"
                  "  --query \"world model mpc\" --limit 20 > arxiv.json\n\n"
                  "python3 tools/ra_cli.py providers search --provider semantic_scholar \\\n"
                  "  --query \"TD-MPC2\" --limit 20 > s2.json"),
            Block("p", "Optional: API keys"),
            Block("bullets", [
                "Semantic Scholar: set env var S2_API_KEY (optional but recommended).",
                "OpenAlex: env var OPENALEX_API_KEY (optional).",
            ]),
            Block("h2", "5.4 Optional hook: deduplicate_by_doi"),
            Block("p", "Enable the DOI de-dup hook for provider results (within a single search output)."),
            Block("code",
                  "cp interfaces/config.example.yaml interfaces/config.yaml\n"
                  "# Edit interfaces/config.yaml:\n"
                  "hooks:\n"
                  "  deduplicate_by_doi:\n"
                  "    enabled: true"),
            Block("h2", "5.5 Repropack: create a reproducibility skeleton"),
            Block("p", "v1.3.2 includes a conservative skeleton generator. It does not infer commands automatically; you fill in the missing details without fabrication."),
            Block("code",
                  "python3 tools/ra_cli.py repropack init --out-dir repropack\n"
                  "# Then edit:\n"
                  "# - repropack/README_REPRO.md\n"
                  "# - repropack/artifact_manifest.json"),
        ]
    ))

    # 6) Playbooks
    sections.append(Section(
        title="6. Copy/paste playbooks (after Mode Lock)",
        blocks=[
            Block("p", "Use these templates after the mode is locked. They are optimized for high signal, low drift."),
            Block("h2", "6.1 Paper reading (interview-oriented)"),
            Block("code",
                  "Read the attached paper/section.\n"
                  "Output:\n"
                  "1) 10-line executive summary\n"
                  "2) Contributions (bullets)\n"
                  "3) Assumptions + where they are used\n"
                  "4) Limitations / failure modes\n"
                  "5) What breaks first in practice\n"
                  "6) 8 interview questions + short answers"),
            Block("h2", "6.2 Proof audit (A + C lenses)"),
            Block("code",
                  "Audit the following proof (or lemma) with A lens (Logic) + C lens (Calculation).\n"
                  "- If a definition is missing, mark UNKNOWN and ask minimal questions.\n"
                  "Output:\n"
                  "(1) proof sketch in your own words\n"
                  "(2) the first non-trivial step that might be invalid\n"
                  "(3) counterexample attempt\n"
                  "(4) minimal fix (tighten assumptions or add lemma)"),
            Block("h2", "6.3 Innovation correctness audit (E lens)"),
            Block("code",
                  "Audit the innovation idea.\n"
                  "Output:\n"
                  "(1) one-sentence innovation claim\n"
                  "(2) required assumptions (explicit)\n"
                  "(3) failure modes / counterexamples\n"
                  "(4) what must be shown experimentally vs theoretically\n"
                  "(5) safe claim wording + what NOT to claim"),
            Block("h2", "6.4 Novelty mapping (evidence-grounded)"),
            Block("code",
                  "Given:\n"
                  "- my contribution list\n"
                  "- retrieved papers JSON (from provider search)\n"
                  "Build a novelty map. For each contribution:\n"
                  "(1) closest prior art and overlap\n"
                  "(2) what is truly new (delta)\n"
                  "(3) safe claim wording + what NOT to claim\n"
                  "(4) citations to prioritize in related work"),
        ]
    ))

    # 7) 2-hour sprint pattern
    sections.append(Section(
        title="7. The 2-hour sprint pattern (single-task constraint)",
        blocks=[
            Block("p", "If a single task must produce a usable result within 2 hours, enforce this sprint structure."),
            Block("table", {
                "header_dark": True,
                "col_widths": [2.0*cm, 6.2*cm, None],
                "rows": [
                    ["Minute", "You do", "Assistant outputs"],
                    ["0-5", "State target + constraints + acceptance criteria", "Restate goal; list assumptions; confirm output schema"],
                    ["5-20", "Provide the artifact chunk", "Initial diagnosis; UNKNOWNs; concrete plan (deliverable)"],
                    ["20-60", "Iterate on the core", "Main audit/derivation/rewrite with actionable fixes"],
                    ["60-90", "Patch plan + defense", "Minimal fix plan; safe wording; reviewer risk register"],
                    ["90-120", "Finalize deliverable", "Clean final output + checklist + next sprint suggestions"],
                ]
            }),
            Block("p", "Scope control tips"),
            Block("bullets", [
                "If large new experiments are proposed, force a minimal patch plan first.",
                "For long proofs, audit one lemma at a time.",
                "Use hard acceptance criteria: done when you have X bullets / Y table / Z LaTeX.",
            ]),
        ]
    ))

    # 8) Troubleshooting
    sections.append(Section(
        title="8. Troubleshooting and FAQ",
        blocks=[
            Block("h2", "8.1 The assistant starts executing before Mode Lock"),
            Block("p", "This violates the Execution Gate. Ask it to re-run: Intake -> generate MODE_LOCK -> wait for CONFIRM."),
            Block("h2", "8.2 The output looks like YAML logs"),
            Block("p", "This violates the readability policy. Remind it: DEBUG_TRACE must be OFF by default; routing metadata is hidden."),
            Block("h2", "8.3 Fabrication risk"),
            Block("p", "When evidence is missing, require UNKNOWN markers. Provide the exact artifact and request minimal questions only."),
            Block("h2", "8.4 Provider search returns empty"),
            Block("p", "Try another provider, reduce limit, or add an API key (Semantic Scholar). Network restrictions may also apply."),
        ]
    ))

    # Appendices
    sections.append(Section(
        title="Appendix A. Command reference",
        blocks=[
            Block("code",
                  "# Local build\n"
                  "python3 -m pip install -r requirements.txt\n"
                  "python3 tools/build_all.py\n\n"
                  "# Router\n"
                  "python3 router/route.py \"我想做方法正确性核查\" --topk 5\n\n"
                  "# Providers\n"
                  "python3 tools/ra_cli.py providers list\n"
                  "python3 tools/ra_cli.py providers search --provider openalex --query \"your query\" --limit 10\n"
                  "python3 tools/ra_cli.py providers search --provider crossref --query \"your query\" --limit 10\n"
                  "python3 tools/ra_cli.py providers search --provider arxiv --query \"your query\" --limit 10\n"
                  "python3 tools/ra_cli.py providers search --provider semantic_scholar --query \"your query\" --limit 10\n\n"
                  "# Repropack\n"
                  "python3 tools/ra_cli.py repropack init --out-dir repropack\n\n"
                  "# Web bootstrap\n"
                  "NO-MIGRATION. Bootstrap from the uploaded zip and start Deep intake.\n"
                  "MIGRATION-PASTED. Bootstrap + Deep intake.\n"
                  "# Activate lock\n"
                  "CONFIRM\n"
                  "# Optional debug trace\n"
                  "DEBUG_TRACE=ON")
        ]
    ))

    sections.append(Section(
        title="Appendix B. Config knobs (optional)",
        blocks=[
            Block("p", "A config file is optional. If present, it enables hooks and provider-specific settings."),
            Block("h2", "B.1 Enable DOI de-dup hook"),
            Block("code",
                  "cp interfaces/config.example.yaml interfaces/config.yaml\n"
                  "# interfaces/config.yaml\n"
                  "hooks:\n"
                  "  deduplicate_by_doi:\n"
                  "    enabled: true"),
            Block("h2", "B.2 API keys (recommended for Semantic Scholar)"),
            Block("code",
                  "# Bash\n"
                  "export S2_API_KEY=\"...\"\n"
                  "export OPENALEX_API_KEY=\"...\"  # optional"),
        ]
    ))

    sections.append(Section(
        title="Appendix C. External tools & links (optional)",
        blocks=[
            Block("p", f"These tools are optional. {PROJECT} does not depend on them, but they can accelerate discovery and claim verification."),
            Block("table_raw", {
                "col_widths": [3.0*cm, 3.6*cm, None],
                "rows": [
                    ["Category", "Tool", "URL"],
                    ["Scholarly APIs", "OpenAlex", "https://openalex.org/settings/api"],
                    ["Scholarly APIs", "Semantic Scholar API", "https://api.semanticscholar.org/api-docs/"],
                    ["Scholarly APIs", "Crossref REST", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/"],
                    ["Scholarly APIs", "arXiv API", "https://info.arxiv.org/help/api/index.html"],
                    ["Discovery", "Elicit", "https://elicit.com/"],
                    ["Discovery", "Connected Papers", "https://www.connectedpapers.com/"],
                    ["Discovery", "ResearchRabbit", "https://www.researchrabbit.ai/"],
                    ["Discovery", "Litmaps", "https://www.litmaps.com/"],
                    ["Claim verification", "Scite", "https://scite.ai/"],
                    ["Answer engine", "Consensus", "https://consensus.app/"],
                    ["Answer engine", "Perplexity", "https://www.perplexity.ai/"],
                    ["Writing/refs", "Overleaf", "https://www.overleaf.com/"],
                    ["Writing/refs", "Zotero", "https://www.zotero.org/"],
                    ["Venues/reviews", "OpenReview", "https://openreview.net/"],
                ]
            }),
        ]
    ))

    return sections


# -----------------------------
# Rendering
# -----------------------------
def render_cover(story, styles):
    story.append(Spacer(1, 0.9*cm))
    story.append(Paragraph(f"{PROJECT} - How to Use", styles["Small"]))
    story.append(Paragraph(f"Version: {VERSION}", styles["Small"]))
    story.append(Paragraph("How to Use", styles["Title"]))
    story.append(Paragraph(f"Repository URL: {REPO_URL_PLACEHOLDER}", styles["Small"]))

    story.append(KeepTogether([
        make_badge("ZIP-only boot + Mode Lock"),
        Spacer(1, 5),
        make_badge("A/B/C/E audits (Logic/Method/Calculation/Innovation)"),
        Spacer(1, 5),
        make_badge("Default web browsing: ALLOW"),
        Spacer(1, 5),
        make_badge("Readability-first (no YAML logs)"),
    ]))
    story.append(Spacer(1, 0.35*cm))

    story.append(Paragraph(
        "This guide targets users who prioritize correctness and a high quality ceiling: "
        "logic audits, method/calc checks, innovation feasibility audits, and defensible novelty claims. "
        "The recommended loop is Web chat for deep reasoning + optional WSL2 CLI for deterministic routing "
        "and evidence collection via public scholarly APIs.",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.25*cm))
    story.append(workflow_drawing())
    story.append(Spacer(1, 0.25*cm))

    story.append(Paragraph("What this toolkit is best at", styles["H2"]))
    add_bullets(story, [
        "Logic audit: find missing assumptions, non sequiturs, and scope mistakes.",
        "Method audit: training-vs-inference mismatches, protocol issues, invalid ablations.",
        "Calculation audit: derivations, dimensions, statistics, numerics.",
        "Innovation correctness: feasibility, calibrated claims, failure modes.",
        "Controlled rewriting: keep claims fixed; improve clarity and defensibility.",
    ], styles["Body"])

    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(f"Version Time: {VERSION_TIME}.", styles["Small"]))
    story.append(PageBreak())


def render_toc(story, styles, sections, total_width):
    story.append(Paragraph("Table of Contents", styles["H1"]))

    rows = []
    for sec in sections:
        rows.append([Paragraph(f"<b>{sec.title}</b>", styles["Body"])])

    toc_table = Table(rows, colWidths=[total_width])
    toc_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#FBFCFE")]),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D0D7DE")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E5E7EB")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(toc_table)
    story.append(PageBreak())


def render_section(story, styles, sec: Section, total_width):
    story.append(Paragraph(sec.title, styles["H1"]))

    for blk in sec.blocks:
        if blk.kind == "p":
            story.append(Paragraph(str(blk.payload), styles["Body"]))
        elif blk.kind == "h2":
            story.append(Paragraph(str(blk.payload), styles["H2"]))
        elif blk.kind == "bullets":
            add_bullets(story, list(blk.payload), styles["Body"])
        elif blk.kind == "code":
            add_code(story, str(blk.payload), styles["Code"])
        elif blk.kind == "table":
            spec = dict(blk.payload)
            rows = spec["rows"]
            header_dark = bool(spec.get("header_dark", False))
            col_widths = resolve_col_widths(spec.get("col_widths", None), total_width)
            story.append(make_table(rows, col_widths, header_dark=header_dark))
        elif blk.kind == "table_raw":
            spec = dict(blk.payload)
            rows = spec["rows"]
            col_widths = resolve_col_widths(spec.get("col_widths", None), total_width)
            t = Table(rows, colWidths=col_widths)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9.0),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D0D7DE")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E5E7EB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFCFE")]),
            ]))
            story.append(t)
        else:
            raise ValueError(f"Unknown block kind: {blk.kind}")

    story.append(PageBreak())


def build_pdf():
    styles = build_styles()

    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.6*cm, bottomMargin=2.2*cm,
        title=f"{PROJECT} - How to Use",
        author=PROJECT,
    )

    sections = build_sections(styles)
    story = []

    render_cover(story, styles)
    content_width = doc.width
    render_toc(story, styles, sections, content_width)
    for sec in sections:
        render_section(story, styles, sec, content_width)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def main():
    build_pdf()
    print("Wrote:", OUT_PDF)


if __name__ == "__main__":
    main()
