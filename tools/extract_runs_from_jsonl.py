"""
extract_runs_from_jsonl.py
==========================

Regenerates evaluation/runs/ from evaluation/results/raw_jsonl/.

Layout produced:
    evaluation/runs/<approach>/<llm>/scenario_<NN>/
        input_scenario.md     natural-language process description (the PMo input)
        ground_truth.bpmn     ground-truth BPMN XML
        ground_truth.py       ground-truth Modelio config (BPMN_Helpers.py format)
        generated.py          the LLM-generated config or full script
        execution_output.txt  Modelio execution stdout/stderr
        metrics.json          ground-truth and generated structural metrics, tokens, timing

Each JSONL record holds a single run for a single scenario; the LLM-generated
artifact is stored in a per-file field whose name encodes the model
('claudeopus_config', 'claudeopus45_config', 'gpt52_config', 'glm5_config').

Usage:
    python tools/extract_runs_from_jsonl.py
    python tools/extract_runs_from_jsonl.py --clean   # wipe runs/ before extracting
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "evaluation" / "results" / "raw_jsonl"
RUNS_DIR = REPO_ROOT / "evaluation" / "runs"


@dataclass(frozen=True)
class SourceFile:
    approach: str
    llm: str
    path: Path


# JSONL field name carrying the LLM-generated artifact, per file.
SOURCES: list[SourceFile] = [
    SourceFile("config-helpers", "claude_opus_4_5",
               RAW_DIR / "exp_config_helper" / "generated_configs_modelio_claude_opus_4_5.jsonl"),
    SourceFile("config-helpers", "gpt_5_2",
               RAW_DIR / "exp_config_helper" / "generated_configs_helper_GPT_5_2_modelio.jsonl"),
    SourceFile("config-helpers", "glm5",
               RAW_DIR / "exp_config_helper" / "generated_configs_helper_GLM5_modelio.jsonl"),
    SourceFile("no-helper", "claude_opus_4_5",
               RAW_DIR / "exp_no_helper" / "generated_configs_no_helper_claude_opus_4_5_modelio.jsonl"),
    SourceFile("no-helper", "gpt_5_2",
               RAW_DIR / "exp_no_helper" / "generated_configs_no_helper_gpt_5_2_modelio.jsonl"),
    SourceFile("no-helper", "glm5",
               RAW_DIR / "exp_no_helper" / "generated_configs_no_helper_GLM5_modelio.jsonl"),
]


def find_generated_field(record: dict) -> str:
    candidates = [
        k for k in record
        if k.endswith("_config")
        and k not in {"modelio_config"}
        and not k.endswith("_tokens")
        and not k.endswith("_time")
    ]
    if len(candidates) != 1:
        raise ValueError(f"Could not uniquely identify generated-config field; candidates={candidates}")
    return candidates[0]


def write_scenario(out_dir: Path, record: dict, gen_field: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    def write(fname: str, value: str | None) -> None:
        (out_dir / fname).write_text(value if value is not None else "", encoding="utf-8")

    write("input_scenario.md", f"# Input scenario\n\n{(record.get('input') or '').strip()}\n")
    write("ground_truth.bpmn", record.get("output"))
    write("ground_truth.py", record.get("modelio_config"))
    write("generated.py", record.get(gen_field))
    write("execution_output.txt", record.get("execution_output"))

    prefix = gen_field.removesuffix("_config")
    metrics = {
        "complexity": record.get("complexity"),
        "ground_truth_metrics": record.get("complexity_metrics"),
        "generated_metrics": {
            "lanes": record.get("lanes"),
            "elements": record.get("elements"),
            "flows": record.get("flows"),
            "gateways": record.get("gateways"),
            "data_objects": record.get("data"),
            "data_assoc": record.get("data_assoc"),
        },
        "execution_success": record.get("execution_success"),
        "execution_error": record.get("execution_error"),
        "tokens": {
            "input": record.get(f"{prefix}_config_input_tokens"),
            "output": record.get(f"{prefix}_config_output_tokens"),
            "total": record.get(f"{prefix}_config_total_tokens"),
        },
        "generation_time_seconds": record.get(f"{prefix}_config_generation_time"),
    }
    (out_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def process_source(src: SourceFile) -> int:
    base = RUNS_DIR / src.approach / src.llm
    records = [json.loads(line) for line in src.path.read_text(encoding="utf-8").splitlines() if line.strip()]
    gen_field = find_generated_field(records[0])
    for idx, record in enumerate(records, start=1):
        scenario_dir = base / f"scenario_{idx:02d}"
        write_scenario(scenario_dir, record, gen_field)
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--clean", action="store_true",
                        help="Wipe evaluation/runs/ before extracting")
    args = parser.parse_args()

    if args.clean and RUNS_DIR.exists():
        shutil.rmtree(RUNS_DIR)

    total = 0
    for src in SOURCES:
        n = process_source(src)
        total += n
        print(f"[OK] {src.approach}/{src.llm}: {n} scenarios")
    print(f"\nWrote {total} run folders under {RUNS_DIR.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
