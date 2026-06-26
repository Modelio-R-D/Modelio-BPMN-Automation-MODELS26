# STATUS — Artifact Badge Claims

We apply for the following three ACM badges under the
"Artifact Review and Badging Version 1.1" policy:

1. **Artifact Evaluated — Functional**
2. **Artifact Evaluated — Reusable**
3. **Artifact Available**

## Artifact Evaluated — Functional

The README (`README.md`) clearly describes the artifact's contents, purpose, and
how to obtain it. It is extended with:

- **`INSTALL.md`** : full installation guide covering hardware/software prerequisites
  (Modelio 5.4, Python 3.10+, OpenRouter API key), OS-specific setup steps for Windows,
  Linux, and macOS, and placement of the helper library inside Modelio's macro directory.
- **`docs/QUICKSTART.md`** : a small self-contained example that walks through generating
  a BPMN model for a single scenario end-to-end that works within minutes of installation.
- **`REPRODUCE.md`** : step-by-step guide to reproduce every result in the paper:
  download the PMo dataset, run the generation pipeline with `tools/run_pipeline.py`,
  test a generated macro in Modelio, and rerun `Evaluation/results/Evals.ipynb` to
  regenerate Tables 1–5.
- **`requirements.txt`** is provided as all Python dependencies can be installed with a single
  `pip install -r requirements.txt`.

---

## Artifact Evaluated — Reusable

We believe this artifact significantly exceeds minimal functionality and is structured
for reuse.

**Well-structured layout and packaging.**
The repository follows a consistent layout separating concerns where every folder
carries its own `README.md`: prompt approaches (`approaches/`), evaluation data
(`Evaluation/`), and utility scripts (`tools/`). Dependencies are declared in
`requirements.txt`, and `INSTALL.md` covers Modelio
setup and the helper library placement for Windows, Linux, and macOS.

**Reusable prompt approaches.**
Both approaches (`config-helpers` and `no-helper`) are self-contained: each has a
`system_prompt.md`, documented examples, and a `README.md`. A researcher can drop in
any other LLM supported by OpenRouter by changing only the `--model` flag in
`run_pipeline.py`.

**Reusable helper library.**
`BPMN_Helpers.py` is documented at the API level (`approaches/config-helpers/docs/`)
and designed to absorb Modelio API surface details so that LLM-facing prompts remain
model-agnostic. It can be reused for any BPMN automation task in Modelio beyond the
scenarios in this paper.

**Open, reusable data formats.**
All experiment data is stored as JSONL (one object per scenario/model/approach),
with a stable field schema documented in `Evaluation/dataset/README.md`. The PMo
benchmark dataset is independently archived on Zenodo (doi:10.5281/zenodo.15857589).

**Extensibility.**
`tools/bpmn_to_complexity.py` can compute complexity metrics for any BPMN XML file,
independent of this paper's scenarios. `tools/run_pipeline.py` accepts arbitrary
`--input` JSONL files, enabling researchers to run the same pipeline on new scenario
sets without modifying any code.

---
## Artifact Available

We believe this artifact satisfies the Available criteria on the following grounds.

**Publicly accessible.**
The artifact is published on Zenodo at a stable, persistent URL.
**DOI:** [10.5281/zenodo.20931887](https://doi.org/10.5281/zenodo.20931887)

**Open license.**
The software components of this artifact are released under the **Apache License 2.0**
(see `LICENSE`).

---
