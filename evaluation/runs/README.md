# Per-run artifacts

330 folders — one per (approach, LLM, scenario) cell — making every
single run individually inspectable without parsing JSONL.

```
config-helpers/                  no-helper/
├── claude_opus_4_5/             ├── claude_opus_4_5/
│   ├── scenario_01/             │   ├── scenario_01/
│   │   ├── input_scenario.md    │   │   ├── input_scenario.md
│   │   ├── ground_truth.bpmn    │   │   ├── ground_truth.bpmn
│   │   ├── ground_truth.py      │   │   ├── ground_truth.py
│   │   ├── generated.py         │   │   ├── generated.py
│   │   ├── execution_output.txt │   │   ├── execution_output.txt
│   │   └── metrics.json         │   │   └── metrics.json
│   …                            │   …
├── gpt_5_2/                     ├── gpt_5_2/
└── glm5/                        └── glm5/
```

| File                  | Contents                                                                |
|-----------------------|-------------------------------------------------------------------------|
| `input_scenario.md`   | Natural-language process description (the PMo input for this scenario)  |
| `ground_truth.bpmn`   | Ground-truth BPMN 2.0 XML from the PMo dataset                          |
| `ground_truth.py`     | Ground-truth Modelio config in BPMN_Helpers format                      |
| `generated.py`        | The LLM-generated script for this run                                   |
| `execution_output.txt`| stdout/stderr from running `generated.py` in Modelio                    |
| `metrics.json`        | Ground-truth metrics, generated metrics, tokens, timing, success flag   |

## Regenerating

The tree is fully derived from
[`../results/raw_jsonl/`](../results/raw_jsonl/):

```bash
python tools/extract_runs_from_jsonl.py --clean
```

(Run from the repository root.)

## Adding diagram renders (PNG / BPMN export)

A planned addition is to render each `generated.py` in Modelio and place the
resulting screenshot next to the script as `diagram.png`. The driver script
is [`../../tools/render_diagrams.py`](../../tools/render_diagrams.py); it
uses Modelio's ScriptServer (socket port 9999).
