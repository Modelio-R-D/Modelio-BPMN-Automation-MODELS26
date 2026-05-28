# Results

The paper's quantitative tables, the reproducibility notebook, and the
authoritative raw experiment data.

| File / folder       | What it is                                                       |
|---------------------|------------------------------------------------------------------|
| `tables.md`         | Paper Tables 1–5 (PMo benchmark). Same numbers Evals.ipynb produces. |
| `Evals.ipynb`       | Jupyter notebook that loads `raw_jsonl/` and computes the tables.    |
| `raw_jsonl/`        | **Source of truth.** One JSONL file per (approach, LLM) cell; one record per scenario. Schema described below. |

The per-run unpacks under [`../runs/`](../runs/) are derived from these
JSONL files.

For MATISSE tables, see [`../matisse/partner_metrics.md`](../matisse/partner_metrics.md).

## JSONL schema

Each line is a single run for a single scenario. Fields:

| Field                         | Type    | Notes                                                   |
|-------------------------------|---------|---------------------------------------------------------|
| `input`                       | str     | Natural-language process description                    |
| `output`                      | str     | Ground-truth BPMN 2.0 XML                               |
| `modelio_config`              | str     | Ground-truth Modelio config (BPMN_Helpers format)       |
| `complexity_metrics`          | dict    | Ground-truth structural metrics                         |
| `complexity`                  | str     | Difficulty label ("Simple" / "Medium" / "Complex")      |
| `<llm>_config`                | str     | The LLM-generated script (field name varies per file)   |
| `<llm>_config_input_tokens`   | int     | Input tokens reported by the provider                   |
| `<llm>_config_output_tokens`  | int     | Output tokens                                           |
| `<llm>_config_total_tokens`   | int     | Total                                                   |
| `<llm>_config_generation_time`| float   | Wall-clock seconds                                      |
| `execution_success`           | bool    | Did `generated.py` run cleanly in Modelio?              |
| `execution_output`            | str     | stdout/stderr from Modelio                              |
| `execution_error`             | str/null| Exception text if it failed                             |
| `lanes`, `elements`, `flows`, `gateways`, `data`, `data_assoc` | int | Structural metrics extracted from the resulting Modelio model |

The `<llm>_config` field name encodes the model:
`claudeopus_config`, `claudeopus45_config`, `gpt52_config`, `glm5_config`.
