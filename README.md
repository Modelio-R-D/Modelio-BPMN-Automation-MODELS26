# Modelio BPMN Automation — MODELS 2026 artifact

LLM-assisted BPMN modeling in [Modelio](https://www.modelio.org/). Describe
a process in plain language and Claude, ChatGPT, Gemini, GLM5, or a local
LLM via LM Studio generates a runnable Modelio macro.

![BPMN Example](docs/images/expense-approval-example.png)

This repository is the companion artifact for the MODELS 2026 paper
**"Towards LLM-Assisted Business Process Modeling in an Industrial Modeling
Tool: An Experience Report"** (submission #110).

The paper reports two complementary solutions and compares them across
three LLMs on 55 BPMN scenarios — both solutions, the prompts, the
generated scripts, and the resulting metrics are all in this repository.

---

## Repository layout

```
.
├── README.md                       — this file (navigation hub)
├── REPRODUCE.md                    — step-by-step replication for artifact reviewers
├── INSTALL.md                      — Modelio + Python setup
├── CHANGELOG.md                    — version history
├── LICENSE                         — Apache 2.0
│
├── approaches/                     — the two solutions evaluated in the paper
│   ├── config-helpers/             —   intermediate representation + helper library
│   │   ├── BPMN_Helpers.py         —     the helper library (install to Modelio)
│   │   ├── BPMN_Export.py          —     reverse-direction export macro
│   │   ├── system_prompt.md        —     LLM system prompt
│   │   └── examples/               —     4 worked examples
│   └── no-helper/                  —   baseline: LLM emits Modelio API calls directly
│       ├── system_prompt.md
│       ├── templates/
│       └── examples/
│
├── docs/                           — user & design documentation
│   ├── QUICKSTART.md
│   ├── APPROACHES.md               —   side-by-side comparison
│   ├── EXECUTION_FLOW.md
│   ├── API_REFERENCE.md            —   Config schema, element types
│   ├── DSL_DESIGN.md               —   design rationale + alternatives explored
│   ├── LAYOUT_RULES.md             —   layout rules the helper enforces
│   └── BPMN_EXPORT.md              —   the export feature
│
├── evaluation/                     — everything supporting the paper's quantitative claims
│   ├── PROCEDURE.md                —   who ran it, when, with what settings
│   ├── prompts/                    —   system prompts + preliminary-test prompts
│   ├── scenarios/                  —   the 55 PMo input scenarios (browsable)
│   ├── runs/                       —   per-(approach, LLM, scenario) artifacts
│   │   └── config-helpers/claude_opus_4_5/scenario_07/
│   │       ├── input_scenario.md
│   │       ├── ground_truth.bpmn
│   │       ├── generated.py
│   │       ├── execution_output.txt
│   │       └── metrics.json
│   ├── results/                    —   paper tables + reproducibility notebook
│   │   ├── tables.md
│   │   ├── Evals.ipynb
│   │   └── raw_jsonl/              —     source-of-truth experiment data
│   └── matisse/                    —   industrial validation (metrics only; materials confidential)
│
├── tools/                          — utilities
│   ├── extract_runs_from_jsonl.py  —   regenerates evaluation/runs/ from raw JSONL
│   ├── macros/render_all.py        —   Modelio macro: reproduce the PNGs inside a stock Modelio
│   └── render_diagrams.py          —   internal driver (authors only; see tools/README.md)
│
└── tests/                          — feature-level test cases for the helper library
```

## For paper reviewers

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
- **The evaluation procedure** is at
  [`evaluation/PROCEDURE.md`](evaluation/PROCEDURE.md) (controlled benchmark)
  and [`evaluation/matisse/procedure.md`](evaluation/matisse/procedure.md)
  (MATISSE).
- **DSL design alternatives** explored before settling on the published IR
  are at [`docs/DSL_DESIGN.md`](docs/DSL_DESIGN.md).
- **Preliminary baseline experiments** that motivated the move from direct
  generation to Config+Helpers are at
  [`evaluation/prompts/preliminary_tests/`](evaluation/prompts/preliminary_tests/).
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

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for a longer walkthrough and
[`docs/APPROACHES.md`](docs/APPROACHES.md) for when to use Config+Helpers vs.
the No-Helper baseline.

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
