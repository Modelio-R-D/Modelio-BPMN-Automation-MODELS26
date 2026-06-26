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
pip install -r requirements.txt
```

Python 3.10 or later.

## 4. LLM access

Required to repeat the generation phase. All three models used in the
experiments are accessible via [OpenRouter](https://openrouter.ai):

| Model | OpenRouter identifier |
|---|---|
| Claude Opus 4.5 | `anthropic/claude-opus-4-5` |
| GPT-5.2 | `openai/gpt-5-2` |
| GLM5 | `z-ai/glm-5` |

Create a `.env` file at the repository root with your key:

```
OPENROUTER_API_KEY=your-key-here
```

LLM versions and sampling settings are described in the paper. See
[`REPRODUCE.md`](REPRODUCE.md) for the full generation pipeline.

## 5. Verify the installation

In Modelio, select a package in the model explorer, open **Views → Script**,
paste the contents of
[`approaches/config-helpers/examples/ExpenseApproval.py`](approaches/config-helpers/examples/ExpenseApproval.py),
and click **Run**. A three-lane BPMN diagram should appear.
