# Installation

## 1. Modelio

[Modelio](https://www.modelio.org/) **5.0 or later** (the experiments were run
on 5.4). Download the community edition from the project website. The
"BPMN Diagram Designer" module must be installed (it ships in the default
package).

## 2. Install the Config+Helpers helper library

Copy [`approaches/config-helpers/BPMN_Helpers.py`](approaches/config-helpers/BPMN_Helpers.py)
into the Modelio macros directory:

| OS      | Path                                                           |
|---------|----------------------------------------------------------------|
| Windows | `C:\<Modelio install>\.modelio\5.4\macros\BPMN_Helpers.py`     |
| Linux   | `~/.modelio/5.4/macros/BPMN_Helpers.py`                        |
| macOS   | `~/.modelio/5.4/macros/BPMN_Helpers.py`                        |

Replace `5.4` with your Modelio version. Create the `macros/` folder if it
does not exist.

Optional (for round-trip export): copy
[`approaches/config-helpers/BPMN_Export.py`](approaches/config-helpers/BPMN_Export.py)
to the same folder.

## 3. Python tooling (for reproduction, not for using the macros)

The macros run inside Modelio's bundled Jython 2.7 and need no external
Python. Only the **reproduction / analysis** tools need a separate Python:

```bash
pip install pandas numpy jupyterlab
```

Python 3.10 or later.

## 4. LLM access (optional)

Only required to repeat the generation phase. The experiments used:

- Claude Opus 4.5 (Anthropic API)
- GPT-5.2 (OpenAI API or OpenRouter)
- GLM5 (zai-org via OpenRouter)

See [`evaluation/PROCEDURE.md`](evaluation/PROCEDURE.md) for the exact
settings.

## 5. Verify the installation

In Modelio, select a package in the model explorer, open **Views → Script**,
paste the contents of
[`approaches/config-helpers/examples/ExpenseApproval.py`](approaches/config-helpers/examples/ExpenseApproval.py),
and click **Run**. A three-lane BPMN diagram should appear.
