# No-Helper approach (baseline)

> This approach is the **baseline** used in the controlled benchmark of the
> MODELS 2026 paper. It is **not** deprecated and **not** a previous
> version of Config+Helpers — it is a peer condition. The two approaches
> differ in *what the LLM emits*, not in time or maturity.

In the No-Helper approach, the LLM produces a **complete, self-contained
Modelio Jython script** that calls the Modelio API directly. Nothing is
pre-installed in Modelio; one large generated `.py` file does everything:
process creation, element instantiation, layout, sequence flows, and the
auto-unmask retry loop.

This contrasts with the [Config+Helpers](../config-helpers/) approach,
where the LLM emits a small `CONFIG = {…}` literal and the
`BPMN_Helpers.py` library does the API plumbing.

## When to use which

| Use Config+Helpers when…                               | Use No-Helper when…                                |
|--------------------------------------------------------|----------------------------------------------------|
| You can pre-install a helper library in Modelio        | You want a single drop-in script with no setup     |
| You care about tokens / generation speed / cost        | You can pay 3–5× more tokens per generation        |
| You will iterate on many processes                     | You will generate once and forget                  |
| You want the layout maths handled for you              | You want the LLM to keep total control             |

The paper reports that Config+Helpers is **3.07× faster** for Claude,
**3.60× cheaper** in tokens, and produces **~5× fewer lines** of output —
at comparable structural accuracy on PMo scenarios that contain no data
objects. See [`evaluation/results/tables.md`](../../evaluation/results/tables.md).

## Files in this folder

| File                              | Purpose                                            |
|-----------------------------------|----------------------------------------------------|
| `system_prompt.md`                | LLM system prompt for No-Helper generation         |
| `templates/BPMN_Template.py`      | Skeleton the LLM follows when emitting the script  |
| `examples/`                       | One worked example: `ExpenseApprovalProcess.py`    |
| `lm_studio/`                      | Guide for running with Qwen via LM Studio          |

## Quick start

1. Open Claude / ChatGPT / Gemini and paste [`system_prompt.md`](system_prompt.md)
   as the system instructions.
2. Describe your process; the LLM returns a single `.py` file (~600 lines).
3. In Modelio, select a package, open **Views → Script**, paste, run.

No `BPMN_Helpers.py` install is required for this approach.

## How this is evaluated

Per-run artifacts for the 55 PMo benchmark scenarios are at
[`../../evaluation/runs/no-helper/`](../../evaluation/runs/no-helper/) —
one folder per `(LLM, scenario)` cell, with the prompt input, the
generated script, the Modelio execution log, and the metrics.
