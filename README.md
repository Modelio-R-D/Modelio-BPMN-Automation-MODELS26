# Modelio BPMN Automation — MODELS 2026 artifact

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20931887.svg)](https://doi.org/10.5281/zenodo.20931887)

LLM-assisted BPMN modeling in [Modelio](https://www.modelio.org/). Describe
a process in plain language and Claude, ChatGPT, Gemini, GLM5, or any
**local open-source model via [Ollama](https://ollama.com)** generates a runnable Modelio macro.

![BPMN Example](docs/images/expense-approval-example.png)

This repository is the companion artifact for the MODELS 2026 paper
**"Towards LLM-Assisted Business Process Modeling in an Industrial Modeling
Tool: An Experience Report"**.

The paper reports two complementary solutions and compares them across
three LLMs on 55 BPMN scenarios — both solutions, the prompts, the
generated scripts, and the resulting metrics are all in this repository.

---

## Repository layout

```
.
├── README.md                       — this file (navigation hub)
├── REPRODUCE.md                    — step-by-step replication guide
├── INSTALL.md                      — Modelio + Python setup
├── CHANGELOG.md                    — version history
├── LICENSE                         — Apache 2.0
├── requirements.txt                — Python dependencies
│
├── approaches/                     — the two solutions evaluated in the paper
│   ├── config-helpers/             —   intermediate representation + helper library
│   │   ├── BPMN_Helpers.py         —     the helper library (install to Modelio)
│   │   ├── system_prompt.md        —     LLM system prompt
│   │   ├── examples/               —     4 worked examples (complete business processes)
│   │   ├── tests/                  —     5 feature smoke tests (one BPMN feature each)
│   │   └── docs/                   —     Config+Helpers deep documentation
│   │       ├── API_REFERENCE.md    —       Config schema, element types
│   │       ├── DSL_DESIGN.md       —       design rationale + alternatives explored
│   │       ├── EXECUTION_FLOW.md   —       internal execution phases
│   │       └── LAYOUT_RULES.md     —       layout rules the helper enforces
│   └── no-helper/                  —   baseline: LLM emits Modelio API calls directly
│       ├── system_prompt.md
│       ├── templates/
│       └── examples/
│
├── docs/                           — cross-cutting user documentation
│   ├── QUICKSTART.md               —   10-minute "first BPMN diagram" walkthrough
│   ├── APPROACHES.md               —   guide to rerunning the Config+Helpers vs. No-Helper evaluation
│   └── images/                     —   figures shared by the root README
│
├── evaluation/                     — everything supporting the paper's quantitative claims
│   ├── README.md                   — Evaluation folder navigation and structure guide
│   ├── dataset/                    —   PMo benchmark input + ground-truth complexity metrics
│   │   ├── PMo_input.jsonl         —     raw extract: natural-language input + BPMN XML (55 scenarios)
│   │   └── PMo_input_processed.jsonl —   enriched with complexity label and structural metrics
│   ├── comparisons/                —   55 per-scenario docs: reference vs. all 6 LLM outputs
│   ├── preliminary_tests/          —   pilot study (3 LLMs × 3 scenarios) that motivated Config+Helpers
│   ├── prompts/                    —   system prompts used during the benchmark
│   ├── scenarios/                  —   the 55 PMo scenarios in human-readable Markdown
│   ├── runs/                       —   per-(approach × LLM × scenario) artifacts
│   │   └── config-helpers/claude_opus_4_5/scenario_07/
│   │       ├── input_scenario.md
│   │       ├── ground_truth.bpmn          (XML) / .py (Modelio script) / .png
│   │       ├── generated.py / diagram_generated.png
│   │       ├── execution_output.txt / metrics.json
│   │       └── comparison.md              — short stub linking to ../comparisons/scenario_07.md
│   ├── results/                    —   paper tables + reproducibility notebook
│   │   ├── tables.md
│   │   ├── Evals.ipynb
│   │   └── raw_jsonl/              —     source-of-truth experiment data
│   └── matisse/                    —   industrial validation (metrics only; materials confidential)
│
└── tools/                          — pipeline and utility scripts
    ├── run_pipeline.py             —   LLM generation pipeline (calls OpenRouter, writes JSONL)
    ├── run_pipeline_ollama.py      —    extended run_pipeline.py to support local models via Ollama
    ├── bpmn_to_complexity.py       —   parser: BPMN XML → structural complexity metrics
    ├── get_bpmn_metrics.py         —   Modelio macro: inspect metrics of a diagram interactively
    └── extract_runs_from_jsonl.py  —   regenerates Evaluation/runs/ from raw JSONL
```

## For paper readers

- **The paper's tables** are at
  [`evaluation/results/tables.md`](evaluation/results/tables.md) (Tables 1–5
  in the artifact map to Tables 6–10 in the paper).
  [`evaluation/matisse/partner_metrics.md`](evaluation/matisse/partner_metrics.md)
  has Tables M1–M4.
- **The prompts** are at
  [`approaches/config-helpers/system_prompt.md`](approaches/config-helpers/system_prompt.md)
  and
  [`approaches/no-helper/system_prompt.md`](approaches/no-helper/system_prompt.md).
- **The generated BPMN scripts** for every run are at
  [`evaluation/runs/`](evaluation/runs/) — 330 folders, one per
  (approach × LLM × scenario) cell.
- **DSL design alternatives** explored before settling on the published IR
  are at [`approaches/config-helpers/docs/DSL_DESIGN.md`](approaches/config-helpers/docs/DSL_DESIGN.md).
- **Preliminary baseline experiments** that motivated the move from direct
  generation to Config+Helpers are at
  [`evaluation/preliminary_tests/`](evaluation/preliminary_tests/).
- **Reproducing the tables** from the raw data: see
  [`REPRODUCE.md`](REPRODUCE.md).

## For users

Quick path:

1. Install Modelio and copy
   [`approaches/config-helpers/BPMN_Helpers.py`](approaches/config-helpers/BPMN_Helpers.py)
   into your Modelio macros folder. See [`INSTALL.md`](INSTALL.md).
2. Open Claude / ChatGPT / Gemini, paste the contents of
   [`approaches/config-helpers/system_prompt.md`](approaches/config-helpers/system_prompt.md)
   as the system instructions.
3. Describe your process in natural language. The LLM responds with a
   `CONFIG = {…}` Python script.
4. In Modelio, select a package, open **Views → Script**, paste and run.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for a 10-minute "first BPMN diagram" walkthrough example using our Config+Helpers approach, and [`REPRODUCE.md`](REPRODUCE.md) to rerun our experiments comparing Config+Helpers against the No-Helper baseline.

> **Running locally?** Use [`tools/run_pipeline_ollama.py`](tools/run_pipeline_ollama.py) instead of `run_pipeline.py` to run any Ollama-served model.

## License

Apache 2.0 — see [`LICENSE`](LICENSE).

## Acknowledgments

- [Modelio](https://www.modelio.org/) — open-source modeling environment.
- [MATISSE](https://matisse-kdt.eu/) — Project co-funded by the European
  Union under the Key Digital Technologies Joint Undertaking and
  participating national authorities (Grant Agreement ID 101140216).
- **PMo Dataset** (55 process models with textual descriptions in nine
  representations) — used as the controlled benchmark in
  [`evaluation/`](evaluation/).
  Brissard, A., Cuppens, F., & Zouaq, A. (2025).
  *PMo Dataset* (v1.0.0) [Data set]. Zenodo.
  [doi:10.5281/zenodo.15857589](https://doi.org/10.5281/zenodo.15857589).
  Companion paper: *"What is the Best Process Model Representation?
  A Comparative Analysis for Process Modeling with Large Language
  Models."* In *Proceedings of the AI4BPM Workshop at BPM 2025*.
