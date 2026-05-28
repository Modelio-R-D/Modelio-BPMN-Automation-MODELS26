# Tools

Utilities used during artifact preparation and reproduction.

| Script                       | Purpose                                                          |
|------------------------------|------------------------------------------------------------------|
| `extract_runs_from_jsonl.py` | Regenerates [`evaluation/runs/`](../evaluation/runs/) from [`evaluation/results/raw_jsonl/`](../evaluation/results/raw_jsonl/). |
| `render_diagrams.py`         | Batch-renders every `evaluation/runs/.../generated.py` in Modelio via ScriptServer, saving a PNG screenshot next to the script. *(stub — see file header for status)* |

## Run from repository root

```bash
# Refresh the per-run folder tree
python tools/extract_runs_from_jsonl.py --clean

# Render PNGs (requires Modelio running with ScriptServer on :9999)
python tools/render_diagrams.py
```

Both scripts only read from [`evaluation/`](../evaluation/) and write back
to it; they do not modify [`approaches/`](../approaches/) or
[`docs/`](../docs/).
