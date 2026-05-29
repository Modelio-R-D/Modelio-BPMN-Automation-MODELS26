# Layout rules enforced by `BPMN_Helpers.py`

These rules are enforced by the helper library at execution time and
documented in the system prompt so the LLM can avoid producing invalid
configurations. They are extracted here from
[`../system_prompt.md`](../system_prompt.md)
for reference and for users who want to inspect / extend the layout
algorithm.

## Column model

Every element has an integer **column index** under `CONFIG["layout"]`. The
helper places columns left-to-right at constant horizontal spacing
(`SPACING`, default 150 px). Elements with the same column index in the
*same lane* are auto-stacked vertically with a 90 px gap (auto-stacking,
introduced in v3.2).

**Rule A.** Two sequentially connected elements must occupy **different
columns**. Violating this packs them on top of each other in the same lane.

**Rule B.** A column index is local to a lane *for the purposes of
stacking*. Across lanes, the column index is a global horizontal coordinate.

## Element-type rules

**Rule C.** Gateways must **not** participate in data associations. Modelio's
BPMN renderer silently drops `dataInput` / `dataOutput` edges connected to a
gateway. Connect the data association to the task on either side of the
gateway instead.

**Rule D.** Events (Start, End, Intermediate Catch/Throw) **may** have data
associations, contrary to a common misconception.

**Rule E.** A single lane may contain at most one Start Event for the
process to be well-formed in Modelio's BPMN designer.

## Naming rules

**Rule F.** Element labels are used as identity keys throughout `CONFIG`
(`elements`, `flows`, `layout`, `data_associations`). Labels must be
**unique within the process** and **referenced verbatim** in every list.

**Rule G.** Labels must be ASCII; non-ASCII characters trigger
`UnicodeDecodeError` in Modelio's Jython 2.7 runtime.

## Flow rules

**Rule H.** Every element except End Events must have at least one
outgoing flow.

**Rule I.** Decision gateway outgoing flows should carry edge labels
("Yes" / "No" / etc.) so the rendered diagram is readable.

## Data object rules

**Rule J.** Data objects are positioned **below their associated task**;
the offset is controlled by `DATA_OFFSET_X` and `DATA_OFFSET_Y`
(defaults 90 and 10 px).

**Rule K.** Data association direction is **auto-detected** from the
endpoint types (task → data = "output", data → task = "input"); the
DSL therefore does not require an explicit direction marker.

## Configurable spacing (advanced)

These keys in `CONFIG` adjust the layout:

| Key             | Default | Effect                                                |
|-----------------|---------|-------------------------------------------------------|
| `SPACING`       | 150     | Horizontal gap between columns                        |
| `START_X`       | 80      | X position of the leftmost column                     |
| `TASK_WIDTH`    | 120     | Width of task elements                                |
| `TASK_HEIGHT`   | 60      | Height of task elements                               |
| `DATA_WIDTH`    | 40      | Width of data objects                                 |
| `DATA_HEIGHT`   | 50      | Height of data objects                                |
| `DATA_OFFSET_X` | 90      | Data object X offset relative to its task             |
| `DATA_OFFSET_Y` | 10      | Data object Y gap below its task                      |
| `WAIT_TIME_MS`  | 50      | Time between unmask attempts during diagram rendering |
| `MAX_ATTEMPTS`  | 3       | Maximum unmask attempts                               |

## Why these rules exist

The rules above were discovered by trial and error during the iterations
described in [`DSL_DESIGN.md`](DSL_DESIGN.md). The "auto-unmask" mechanism
in Modelio is non-deterministic — sometimes all elements appear after
diagram creation, sometimes only a subset — and the helper library
implements a retry loop with explicit position-correction to compensate.
This is the principal reason the helper exists at all: encapsulating that
complexity is what lets the LLM stay focused on the *process semantics*.
