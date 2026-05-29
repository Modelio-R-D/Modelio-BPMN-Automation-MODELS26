# Methodology (preliminary evaluation)

This document is the trimmed methodology for the **one-shot generation
baseline** — the only preliminary experiment that was actually run. The
source author had planned four further experiments (V1 minor validation,
Config+Helpers comprehensive, MATISSE statistics, partner survey); those
were either never executed or were superseded by the published
benchmark documented in [`../PROCEDURE.md`](../PROCEDURE.md). They are
deliberately omitted here to avoid pointing reviewers at empty folders.

---

## Purpose

Establish a baseline for direct LLM generation of Modelio Jython
scripts. Specifically: do current LLMs know enough of the Modelio
metamodel API to produce a working BPMN-creation script unaided, and
how does that change when working example scripts are placed in their
context?

## Models tested

- Claude Opus 4.5
- GPT-5.2 Thinking
- Gemini Pro (Dec 2025 / Pro 3.1)

These are the same LLMs the paper references in §2.2. The published
benchmark in [`../runs/`](../runs/) substituted GLM5 for Gemini to make
the LLM set fully open-weight-hostable; the preliminary tests pre-date
that decision.

## Test scenarios

A single scenario at three complexity levels:

| ID | Complexity | Lanes | Elements | Description                                |
|----|------------|------:|---------:|--------------------------------------------|
| S1 | Simple     |     1 |        4 | Document Approval — linear, one reviewer   |
| M1 | Medium     |     2 |      ~10 | Leave Request — one gateway, two branches  |
| C1 | Complex    |     4 |      ~17 | Hiring Process — three gateways, four lanes|

Only **S1** was exercised round-by-round across all three LLMs. M1 and
C1 have one generated Claude script each but no per-round outcome —
treated as exploratory.

The rationale was *if models fail on the simplest case, they fail on
complex ones* — so most of the budget went into S1.

## Two conditions (the independent variable)

| Condition         | What's in the LLM context                                                                                       |
|-------------------|-----------------------------------------------------------------------------------------------------------------|
| Zero-shot         | System prompt + scenario prompt only.                                                                           |
| With API examples | System prompt + scenario prompt + `MakeSingleton.py` + `Sort.py` (both at [`modelio_api_examples/`](modelio_api_examples/)). |

The two attached files are Modelio's own sample macros (authored by
Modeliosoft); see
[`modelio_api_examples/README.md`](modelio_api_examples/README.md) for
their provenance and what each one teaches the LLM about the API.

For LLMs that failed in their first with-examples round, **iterative
debugging rounds** were added: the Modelio execution error was fed back
to the LLM and a new attempt requested. Each LLM was given a fixed
attempt budget; per-LLM convergence behaviour is the headline finding.

## Metrics collected

| Metric              | Definition                                                                          | How collected           |
|---------------------|-------------------------------------------------------------------------------------|-------------------------|
| Success             | "Model OK" / "Layout OK" / "Failure"                                                | Manual classification   |
| Script lines        | Lines in the generated Jython                                                       | `wc -l`                 |
| Error type          | Syntax / API / Layout                                                               | Manual classification   |
| Error message       | Verbatim error from Modelio's console                                               | Copy-paste              |
| Debugging rounds    | Iterations until success or budget exhaustion                                       | Count                   |

The labels were applied manually by the experiment author after each
Modelio execution attempt. There was no inter-rater reliability check.

## Success criteria

- **Model OK** — the script runs to completion and creates a
  well-formed BPMN process in the Modelio model tree.
- **Layout OK** — the diagram, when opened, has every element placed
  legibly. (Note that "Model OK" without "Layout OK" is a common
  outcome — see [`../../docs/LAYOUT_RULES.md`](../../docs/LAYOUT_RULES.md)
  for why Modelio's auto-unmask makes layout the harder half.)
- **Failure** — script raises an exception before the BPMN process
  appears in Modelio.

## How this relates to the published benchmark

The preliminary tests inform but do **not** feed into any number in the
paper's evaluation tables. The published benchmark in
[`../runs/`](../runs/) is the artifact-of-record for the paper's
quantitative claims; this folder exists to substantiate the *qualitative
motivation* described in paper §2.2 and §6.

| Aspect              | Preliminary (here)                       | Published benchmark (`../runs/`)        |
|---------------------|------------------------------------------|-----------------------------------------|
| Scenarios           | 3 (only S1 with full round-by-round)     | 55 (PMo dataset)                        |
| LLMs                | Claude Opus 4.5, GPT-5.2, Gemini Pro 3.1 | Claude Opus 4.5, GPT-5.2, GLM5          |
| Approaches compared | One-shot only                            | Config+Helpers vs. No-Helper            |
| Runs per cell       | 1 + retries until budget                 | 1 (with retries only for GLM5 syntax)   |
| Used for paper §    | §2.2 motivation, §6 lessons learned      | §5 evaluation tables (Tables 1–5)       |
