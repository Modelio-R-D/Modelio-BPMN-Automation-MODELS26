"""
build_comparisons.py
====================

Generate side-by-side comparison docs from the per-run artifacts.

Produces:
  - evaluation/comparisons/scenario_NN.md       (55 files; reference vs. all 6 cells)
  - evaluation/runs/<approach>/<llm>/scenario_NN/comparison.md
                                                 (330 thin per-cell stubs)
  - evaluation/comparisons/README.md            (index over the 55)

Inputs (read-only):
  - evaluation/scenarios/scenario_NN.md         (input description, complexity)
  - evaluation/runs/.../metrics.json            (ground-truth + generated metrics)
  - evaluation/runs/.../*.png                   (rendered diagrams)
  - evaluation/runs/.../diagram_render_error.txt (on failure)

Usage:
  python tools/build_comparisons.py             (idempotent — overwrites)
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "evaluation" / "runs"
COMP_DIR = REPO_ROOT / "evaluation" / "comparisons"
SCEN_DIR = REPO_ROOT / "evaluation" / "scenarios"

# (approach_slug, llm_slug, human-readable LLM label)
CELLS = [
    ("config-helpers", "claude_opus_4_5", "Claude Opus 4.5"),
    ("config-helpers", "gpt_5_2",         "GPT-5.2"),
    ("config-helpers", "glm5",            "GLM5"),
    ("no-helper",      "claude_opus_4_5", "Claude Opus 4.5"),
    ("no-helper",      "gpt_5_2",         "GPT-5.2"),
    ("no-helper",      "glm5",            "GLM5"),
]

# $ per 1M tokens; from paper Table 3.
PRICING = {
    "claude_opus_4_5": (5.0,  25.0),
    "gpt_5_2":         (1.75, 14.0),
    "glm5":            (0.72, 2.30),
}

METRIC_KEYS = ["lanes", "elements", "gateways", "flows", "data_objects", "data_assoc"]
METRIC_LABELS = {
    "lanes":        "Lanes",
    "elements":     "Elements",
    "gateways":     "Gateways",
    "flows":        "Flows",
    "data_objects": "Data obj.",
    "data_assoc":   "Data assoc.",
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _cost_usd(llm: str, in_tok: int | None, out_tok: int | None) -> float | None:
    if in_tok is None or out_tok is None:
        return None
    p_in, p_out = PRICING[llm]
    return (in_tok * p_in + out_tok * p_out) / 1_000_000


def _fmt_delta(generated: int | None, truth: int | None) -> str:
    if generated is None or truth is None:
        return ""
    diff = generated - truth
    if diff == 0:
        return " (=0)"
    return f" ({diff:+d})"


def _scenario_input(scenario_id: int) -> tuple[str, str]:
    """Return (complexity, prose) by parsing scenarios/scenario_NN.md."""
    path = SCEN_DIR / f"scenario_{scenario_id:02d}.md"
    text = path.read_text(encoding="utf-8")
    complexity = "?"
    for line in text.splitlines():
        if line.startswith("**Complexity:**"):
            complexity = line.split("**Complexity:**", 1)[1].strip().strip("*")
            break
    # The natural-language paragraph sits between
    # "## Natural-language description" and the next "##" heading.
    prose = ""
    in_block = False
    for line in text.splitlines():
        if line.strip().startswith("## Natural-language description"):
            in_block = True
            continue
        if in_block:
            if line.startswith("## "):
                break
            prose += line + "\n"
    return complexity, prose.strip()


def _status_badge(metrics: dict, png_exists: bool) -> str:
    if not metrics.get("execution_success"):
        return "❌ execution failed"
    if not png_exists:
        return "⚠️ executed at experiment time, render failed today"
    return "✅ executed"


# ---------------------------------------------------------------------------
# Per-scenario doc generator
# ---------------------------------------------------------------------------

def _metrics_table_row(label: str, m: dict | None, gt: dict, extras: dict | None = None) -> str:
    """Render one row of the unified metrics table."""
    cells = [label]
    for k in METRIC_KEYS:
        if m is None:
            cells.append("—")
            continue
        v = m.get(k)
        if v is None:
            cells.append("—")
        else:
            cells.append(f"{v}{_fmt_delta(v, gt.get(k))}" if extras else f"{v}")
    if extras:
        for v in extras.values():
            cells.append(v if v is not None else "—")
    return "| " + " | ".join(str(c) for c in cells) + " |"


def _build_scenario_doc(scenario_id: int) -> tuple[Path, int]:
    """Write evaluation/comparisons/scenario_NN.md. Returns (path, n_success)."""
    sc = f"scenario_{scenario_id:02d}"
    complexity, prose = _scenario_input(scenario_id)

    # Reference: read ground_truth_metrics from any cell that has the script.
    # config-helpers/claude_opus_4_5 always has it (except scenario_23).
    ref_run_dir = RUNS_DIR / "config-helpers" / "claude_opus_4_5" / sc
    ref_metrics_path = ref_run_dir / "metrics.json"
    ref_metrics = json.loads(ref_metrics_path.read_text(encoding="utf-8"))
    gt = ref_metrics.get("ground_truth_metrics") or {}

    has_gt_png = (ref_run_dir / "ground_truth.png").exists()
    gt_png_rel = f"../runs/config-helpers/claude_opus_4_5/{sc}/ground_truth.png"

    lines: list[str] = []
    lines.append(f"# Scenario {scenario_id:02d}")
    lines.append("")
    lines.append(f"**Complexity:** {complexity}")
    lines.append("")
    lines.append("[← back to comparisons index](README.md)")
    lines.append("")
    lines.append("## Input scenario")
    lines.append("")
    for ln in prose.splitlines():
        lines.append(f"> {ln}" if ln else ">")
    lines.append("")
    lines.append("## Reference BPMN (ground truth)")
    lines.append("")
    if has_gt_png:
        lines.append(f"![ground truth diagram]({gt_png_rel})")
    else:
        lines.append(
            "_No reference diagram available — `ground_truth.py` is empty in "
            "the source JSONL (`modelio_config: None`)._"
        )
    lines.append("")
    lines.append("| " + " | ".join(METRIC_LABELS[k] for k in METRIC_KEYS) + " |")
    lines.append("|" + "|".join(["--:"] * len(METRIC_KEYS)) + "|")
    lines.append("| " + " | ".join(str(gt.get(k, "—")) for k in METRIC_KEYS) + " |")
    lines.append("")
    lines.append("## Generated BPMN — 6 (approach × LLM) cells")
    lines.append("")
    lines.append("Δ values in parentheses are `(generated − ground_truth)`.")
    lines.append("")

    n_success = 0
    for approach, llm_slug, llm_name in CELLS:
        run_dir = RUNS_DIR / approach / llm_slug / sc
        metrics_path = run_dir / "metrics.json"
        if not metrics_path.exists():
            continue
        m = json.loads(metrics_path.read_text(encoding="utf-8"))
        gen = m.get("generated_metrics") or {}
        png = run_dir / "diagram_generated.png"
        err_path = run_dir / "diagram_render_error.txt"
        status = _status_badge(m, png.exists())
        if png.exists():
            n_success += 1

        tok = m.get("tokens") or {}
        in_tok = tok.get("input")
        out_tok = tok.get("output")
        total_tok = tok.get("total")
        gen_time = m.get("generation_time_seconds")
        cost = _cost_usd(llm_slug, in_tok, out_tok)

        png_rel = f"../runs/{approach}/{llm_slug}/{sc}/diagram_generated.png"
        err_rel = f"../runs/{approach}/{llm_slug}/{sc}/diagram_render_error.txt"

        lines.append(f"### {approach} / {llm_name}  {status}")
        lines.append("")
        if png.exists():
            lines.append(f"![]({png_rel})")
        elif err_path.exists():
            err_text = err_path.read_text(encoding="utf-8")
            short = next(
                (l for l in err_text.splitlines()
                 if l.startswith("ERROR") or "Error" in l or "Traceback" in l),
                "(no error line matched)",
            )
            lines.append(f"_Render failed: `{short[:140]}`_  ([log]({err_rel}))")
        else:
            lines.append("_No render available._")
        lines.append("")

        # Metrics table with deltas
        header = ["metric", "ground truth", "generated", "Δ"]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join(["---", "---:", "---:", "---:"]) + "|")
        for k in METRIC_KEYS:
            gv = gen.get(k)
            tv = gt.get(k)
            d = ""
            if gv is not None and tv is not None:
                d = f"{gv - tv:+d}"
                if gv == tv:
                    d = "0"
            lines.append(f"| {METRIC_LABELS[k]} | {tv if tv is not None else '—'} "
                         f"| {gv if gv is not None else '—'} | {d} |")
        lines.append("")
        lines.append(
            f"**Generation:** "
            + (f"{total_tok:,} tokens" if total_tok is not None else "tokens —")
            + " · "
            + (f"{gen_time:.1f}s" if gen_time is not None else "time —")
            + " · "
            + (f"${cost:.3f}" if cost is not None else "cost —")
        )
        if m.get("execution_error"):
            lines.append("")
            lines.append(f"> Original experiment-time error: `{m['execution_error']}`")
        lines.append("")

    COMP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = COMP_DIR / f"{sc}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path, n_success


# ---------------------------------------------------------------------------
# Per-cell stub generator (thin)
# ---------------------------------------------------------------------------

def _build_cell_stub(approach: str, llm_slug: str, llm_name: str, scenario_id: int) -> None:
    sc = f"scenario_{scenario_id:02d}"
    run_dir = RUNS_DIR / approach / llm_slug / sc
    metrics_path = run_dir / "metrics.json"
    if not metrics_path.exists():
        return
    m = json.loads(metrics_path.read_text(encoding="utf-8"))
    gen = m.get("generated_metrics") or {}
    gt = m.get("ground_truth_metrics") or {}

    png = run_dir / "diagram_generated.png"
    status = _status_badge(m, png.exists())

    tok = m.get("tokens") or {}
    in_tok, out_tok, total_tok = tok.get("input"), tok.get("output"), tok.get("total")
    gen_time = m.get("generation_time_seconds")
    cost = _cost_usd(llm_slug, in_tok, out_tok)

    err_path = run_dir / "diagram_render_error.txt"
    gt_png = run_dir / "ground_truth.png"

    lines: list[str] = []
    lines.append(f"# Scenario {scenario_id:02d} — {approach} / {llm_name}")
    lines.append("")
    lines.append(f"**Status:** {status}")
    lines.append("")
    lines.append("Side-by-side comparison with the reference BPMN and the other 5 "
                 f"(approach × LLM) cells: [scenario_{scenario_id:02d}.md]"
                 f"(../../../../comparisons/scenario_{scenario_id:02d}.md)")
    lines.append("")
    lines.append("## Reference (ground truth) vs. this run")
    lines.append("")
    lines.append("**Reference BPMN**")
    if gt_png.exists():
        lines.append("")
        lines.append("![ground truth](ground_truth.png)")
    else:
        lines.append("")
        lines.append("_No reference diagram available (scenario_23: `modelio_config` is `None` in source JSONL)._")
    lines.append("")
    lines.append("**Generated BPMN**")
    if png.exists():
        lines.append("")
        lines.append("![generated](diagram_generated.png)")
    elif err_path.exists():
        err_text = err_path.read_text(encoding="utf-8")
        short = next(
            (l for l in err_text.splitlines()
             if l.startswith("ERROR") or "Error" in l or "Traceback" in l),
            "(no error line matched)",
        )
        lines.append("")
        lines.append(f"_Render failed: `{short[:140]}`_  ([log](diagram_render_error.txt))")
    else:
        lines.append("")
        lines.append("_No render available._")
    lines.append("")
    lines.append("## This run at a glance")
    lines.append("")
    lines.append("| metric | ground truth | generated | Δ |")
    lines.append("|---|---:|---:|---:|")
    for k in METRIC_KEYS:
        gv, tv = gen.get(k), gt.get(k)
        d = "" if (gv is None or tv is None) else (f"{gv - tv:+d}" if gv != tv else "0")
        lines.append(f"| {METRIC_LABELS[k]} | {tv if tv is not None else '—'} "
                     f"| {gv if gv is not None else '—'} | {d} |")
    lines.append("")
    lines.append(
        "**Generation:** "
        + (f"{total_tok:,} tokens" if total_tok is not None else "tokens —")
        + " · "
        + (f"{gen_time:.1f}s" if gen_time is not None else "time —")
        + " · "
        + (f"${cost:.3f}" if cost is not None else "cost —")
    )
    lines.append("")
    lines.append("## Files in this folder")
    lines.append("")
    lines.append("- [`input_scenario.md`](input_scenario.md) — natural-language prompt")
    lines.append("- [`ground_truth.bpmn`](ground_truth.bpmn) — reference BPMN XML")
    lines.append("- [`ground_truth.py`](ground_truth.py) — reference Modelio script")
    lines.append("- [`ground_truth.png`](ground_truth.png) — rendered reference diagram")
    lines.append("- [`generated.py`](generated.py) — LLM output")
    if png.exists():
        lines.append("- [`diagram_generated.png`](diagram_generated.png) — rendered LLM diagram")
    lines.append("- [`metrics.json`](metrics.json) — full metric record")
    lines.append("- [`execution_output.txt`](execution_output.txt) — Modelio execution log "
                 "(from the original experiment)")
    if (run_dir / "diagram_render_error.txt").exists():
        lines.append("- [`diagram_render_error.txt`](diagram_render_error.txt) — render failure detail")
    lines.append("")

    (run_dir / "comparison.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Index generator
# ---------------------------------------------------------------------------

def _build_index(success_counts: dict[int, int]) -> None:
    lines: list[str] = []
    lines.append("# Per-scenario comparison docs")
    lines.append("")
    lines.append("55 scenarios × 6 (approach × LLM) cells = 330 LLM runs. Each "
                 "scenario doc shows the reference BPMN alongside all 6 generated "
                 "outputs with structural metrics and per-element deltas.")
    lines.append("")
    lines.append("| # | Complexity | Lanes (gt) | Elements (gt) | Gateways (gt) "
                 "| Data obj. (gt) | Renders ok |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")

    for sid in range(1, 56):
        sc = f"scenario_{sid:02d}"
        complexity, _ = _scenario_input(sid)
        ref_metrics_path = RUNS_DIR / "config-helpers" / "claude_opus_4_5" / sc / "metrics.json"
        gt = {}
        if ref_metrics_path.exists():
            gt = json.loads(ref_metrics_path.read_text(encoding="utf-8")).get(
                "ground_truth_metrics", {}
            ) or {}
        n_ok = success_counts.get(sid, 0)
        lines.append(
            f"| [scenario_{sid:02d}]({sc}.md) | {complexity} "
            f"| {gt.get('lanes', '—')} | {gt.get('elements', '—')} "
            f"| {gt.get('gateways', '—')} | {gt.get('data_objects', '—')} "
            f"| {n_ok}/6 |"
        )
    lines.append("")
    lines.append("## How these docs were produced")
    lines.append("")
    lines.append("Generated deterministically from the per-run artifacts by "
                 "[`tools/build_comparisons.py`](../../tools/build_comparisons.py). "
                 "Run it again to refresh (overwrites in place).")
    lines.append("")
    (COMP_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    success_counts: dict[int, int] = {}
    COMP_DIR.mkdir(parents=True, exist_ok=True)

    for sid in range(1, 56):
        _, n_ok = _build_scenario_doc(sid)
        success_counts[sid] = n_ok
        for approach, llm_slug, llm_name in CELLS:
            _build_cell_stub(approach, llm_slug, llm_name, sid)

    _build_index(success_counts)

    n_scenario = sum(1 for _ in COMP_DIR.glob("scenario_*.md"))
    n_cell = sum(1 for _ in RUNS_DIR.glob("*/*/scenario_*/comparison.md"))
    print(f"Wrote {n_scenario} scenario docs in {COMP_DIR.relative_to(REPO_ROOT)}/")
    print(f"Wrote {n_cell} per-cell stubs under evaluation/runs/")
    print(f"Wrote index at {(COMP_DIR / 'README.md').relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
