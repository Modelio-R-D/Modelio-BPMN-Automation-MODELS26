# Tools

Utilities used during artifact preparation and reproduction.

| Path                              | Purpose                                                                 |
|-----------------------------------|-------------------------------------------------------------------------|
| `extract_runs_from_jsonl.py`      | Regenerates [`evaluation/runs/`](../evaluation/runs/) from [`evaluation/results/raw_jsonl/`](../evaluation/results/raw_jsonl/). |
| `build_comparisons.py`            | Regenerates [`evaluation/comparisons/`](../evaluation/comparisons/) (55 per-scenario side-by-side docs) and the 330 thin `comparison.md` stubs inside each per-run folder. Reads from `metrics.json` and the PNGs; idempotent. |
| `macros/render_all.py`            | **Modelio macro for reproducibility.** Re-renders every `generated.py` inside a stock Modelio and saves `diagram_generated.png` next to each script. |
| `render_diagrams.py`              | Internal automation driver the authors used to produce the committed PNGs. Documented for transparency, but **not the public reproduction path** — see the note below. |

The paper's analysis notebook lives with the data, not here:
[`evaluation/results/Evals.ipynb`](../evaluation/results/Evals.ipynb).

## Refreshing the per-run folder tree

```bash
python tools/extract_runs_from_jsonl.py --clean
```

Run from the repository root. The tree under
[`evaluation/runs/`](../evaluation/runs/) is fully derived from the JSONL
in `evaluation/results/raw_jsonl/`.

## Re-rendering the PNGs (reviewer path)

Reviewers should use the Modelio macro
[`macros/render_all.py`](macros/render_all.py). It runs entirely inside a
stock Modelio installation and uses only standard Modelio APIs
(`saveInFile("PNG", …)`).

1. Open the macro file, set `REPO_ROOT` at the top to your local clone of
   this repository.
2. Copy the file to your Modelio macros folder
   (`~/.modelio/5.4/macros/render_all.py` on Linux/macOS; the Windows
   equivalent is `C:\<Modelio install>\.modelio\5.4\macros\render_all.py`).
3. Open a Modelio project that contains a top-level UML package named
   `MODELS26` (create it if missing).
4. Right-click that package → **Macros → render_all**.

The macro prints progress as it works and writes `diagram_generated.png` next to
each `evaluation/runs/.../generated.py`. To restrict the run, edit
`ONLY_APPROACH`, `ONLY_LLM`, or `ONLY_SCENARIO` at the top of the macro.

## Rendering the ground-truth side (`ground_truth.png`)

The authors' driver also supports rendering the reference side:

```bash
# Render ground_truth.py for one cell (54/55 unique scenarios produce PNGs;
# scenario_23 has no ground_truth.py in the source JSONL).
python tools/render_diagrams.py --ground-truth \
       --approach config-helpers --llm claude_opus_4_5

# Copy the 54 PNGs to the same scenario folders in the other 5 cells
# (the underlying ground_truth.py is identical across cells modulo a
# single execfile() path line, which the wrapper rewrites anyway).
python -c "
import shutil
from pathlib import Path
src = Path('evaluation/runs/config-helpers/claude_opus_4_5')
for png in sorted(src.glob('scenario_*/ground_truth.png')):
    for cell in ['config-helpers/gpt_5_2', 'config-helpers/glm5',
                 'no-helper/claude_opus_4_5', 'no-helper/gpt_5_2', 'no-helper/glm5']:
        dst = Path('evaluation/runs') / cell / png.parent.name / 'ground_truth.png'
        shutil.copyfile(png, dst)
"
```

The render-once-and-copy shortcut saves 270 redundant Modelio renders.

## A note on the two scripts

`render_diagrams.py` is the same logic as `macros/render_all.py`,
adapted to run from outside Modelio over a project-internal remote
execution channel. We commit it for transparency about how the PNGs in
the artifact were originally produced — but its execution channel is
**not part of the public reproduction path**, and reviewers should not
need to set it up. Use the macro.

Both scripts produce identical output (same per-run sub-package
convention, same diagram-export call, same failure handling).
