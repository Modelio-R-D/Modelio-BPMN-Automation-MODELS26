# DSL design rationale

The Config+Helpers approach hinges on a compact intermediate
representation (IR) that the LLM emits in lieu of full Modelio Jython
code. This document records the design choices that shaped the IR
shipped in [`../system_prompt.md`](../system_prompt.md), and
explicitly bounds what was *not* explored — so a reader can see the
edge of the evidence.

**Anchoring constraint.** Modelio executes Jython directly from its
Script panel. The IR was therefore designed so the LLM's output is a
*single, self-contained Jython file* — helper load + `CONFIG = {…}`
literal + the `createBPMNFromConfig(...)` call — that the user
pastes-and-runs with no separate parsing or wrapping step. This
constraint shapes every choice below, especially the syntactic-format
decision in [§Syntactic format](#syntactic-format).

It addresses Reviewer 3's main question — *"What DSL alternatives did
you try (e.g., different abstraction levels, ordering methods,
syntactic formats) during the iterations?"* — and meta-review point 2.

---

## Final form (what the paper reports)

The IR is a Python literal `CONFIG = {…}` written by the LLM and
consumed by `BPMN_Helpers.py`. It carries:

- `name`: process name
- `lanes`: ordered list of lane names
- `elements`: list of `(label, type_constant, lane)` triples
- `flows`: list of `(source_label, target_label, edge_label)` triples
- `layout`: mapping `label → column_index` for left-to-right placement
- `data_objects` *(optional)*: `(name, lane, column)`
- `data_associations` *(optional)*: `(source, target)`, direction
  auto-detected

See [`API_REFERENCE.md`](API_REFERENCE.md) for the full schema.

## What we tried and chose

### Abstraction level

| Level | What the LLM writes | Status |
|------|---------------------|--------|
| **L0** — Raw Modelio Jython API | `bpmnTask = process.getElement().create(...)` directly | Implemented and benchmarked as the **No-Helper baseline** — see [`approaches/no-helper/`](../../no-helper/). Outputs are ~5× larger; structural accuracy lower than Config+Helpers except on Claude. |
| **L2** — Compact Python literal | `CONFIG = {…}` | **Adopted.** Best efficiency/accuracy trade-off across models in the 55-scenario benchmark. |

The two levels above are the only abstraction levels that were
implemented end-to-end and benchmarked. A BPMN-2.0-XML intermediate
representation (the LLM emits XML, the helper imports it via Modelio's
BPMN-XML import) and a higher-level domain-specific natural-language
representation (e.g., *"Lane Employee: submit then review then …"*)
are theoretically interesting but were **not explored in this work**.
We anchor on the empirical L0-vs-L2 comparison; broader DSL-design
comparison is future work (see [Open design choices](#open-design-choices)).

### Ordering of elements

How is the visual left-to-right order communicated to the helper?

- **Implicit by list position** — early iterations relied on the
  element-list order alone. Brittle: LLMs occasionally produced
  topologically correct lists whose visual rendering flowed
  right-to-left or zig-zagged. **Rejected.**
- **Explicit `layout: {label: column}`** *(adopted)* — decouples
  logical ordering from list position. v3.2 added auto-stacking for
  same-lane / same-column elements, removing a class of layout bugs
  that appeared in earlier versions.
- **Topological sort from flows** — considered conceptually but not
  implemented. Cycles (loops) and parallel-gateway branches make a
  single ordering ambiguous; an explicit layout was cheaper to ship.

### Syntactic format

The decisive constraint is *Modelio's execution surface*: scripts are
pasted into the **Script panel** of the GUI and executed as Jython
directly. We wanted the LLM's output to be **a single, self-contained
Jython file** the user can paste-and-run with no intermediate
tooling. That immediately weighs against any non-Python format.

- **JSON** — strict, and LLMs commonly violated quoting around BPMN
  type constants (e.g., `"EXCLUSIVE_GW"` vs. bare `EXCLUSIVE_GW`).
  More fundamentally, JSON is *data*, not *executable Jython*: a JSON
  artifact would require either (a) two artifacts per run — a
  `config.json` plus a separate wrapper script that parses it — or
  (b) a post-processor that wraps the JSON in Jython before the user
  can run it. Both options add a step between "LLM produced output"
  and "diagram appears in Modelio". **Rejected** after early
  iteration.
- **YAML** — same paste-and-run problem as JSON, with an extra
  twist: YAML can be embedded as a Python triple-quoted string and
  then parsed, but that requires a YAML library inside Modelio's
  Jython (`PyYAML` is not part of a stock install) and re-introduces
  the data-vs-code split the Python literal avoids — the helper
  would have to call `yaml.safe_load(CONFIG_STR)` before it could
  use any of the values. **Rejected** on the same single-file
  paste-and-run grounds.
- **Python literal** *(adopted)* — the LLM's output is *already* a
  valid Jython script: the file `execfile()`s the pre-installed
  `BPMN_Helpers.py`, defines `CONFIG = {…}` as a Python literal, and
  calls `createBPMNFromConfig(selectedElements.get(0), CONFIG)`. The
  user pastes the whole file into Modelio's Script panel and clicks
  Run. Type constants can be referenced as names imported by the
  helper (no string quoting); tuple syntax handles the heterogeneous
  triples/quadruples cleanly; LLMs reliably emit valid Python
  literals.

This is also why what the LLM emits is more than "just the JSON
config": it's the **helper-load + config + call** triple as one
runnable file. Splitting them — say, asking the LLM for only the
config and concatenating a fixed wrapper at our end — would have
worked, but at the cost of teaching users that they receive partial
output. Keeping the single-file end-to-end story is what makes the
"paste it into Modelio and run" demo trivially reproducible.

### Element-type vocabulary

The helper exposes ~30 named constants (see the table in
[`../README.md`](../README.md)). Two extremes were considered:

- **Raw BPMN URIs** — too verbose, too easy to get wrong.
- **Reduced vocabulary** (Task / Gateway / Event only) — lost
  expressiveness for MATISSE scenarios that use Send/Receive tasks,
  Timer events, etc.

The middle path — ~30 mnemonic constants — keeps the LLM productive
while preserving BPMN's element-type semantics.

## Iterations that shaped the final form

- **v1.0 → v2.0** *(Dec 2025)* — split into Helpers + Config files;
  this is the move from L0 to L2.
- **v2.1 → v2.5** *(Dec 2025)* — refined Data Object semantics;
  learned that Modelio rejects gateways with data associations (now a
  hard rule in the prompt).
- **v3.0** *(Dec 2025)* — added round-trip export so LLM-generated
  diagrams can be re-extracted as `CONFIG = {…}`.
- **v3.2** *(Dec 2025)* — auto-stacking: same-lane + same-column
  elements stack 90 px vertically without manual offsets.

## Open design choices

The DSL's design space is not exhaustively covered above. Concrete
directions for future work:

- **L1 (BPMN XML intermediate).** Whether emitting BPMN 2.0 XML and
  importing it through Modelio's XML reader trades token cost against
  format strictness more favourably than the L2 Python literal —
  open.
- **L3 (Higher-level natural-language DSL).** Whether a sentence-like
  surface form is more or less LLM-natural than the structured
  literal — open.
- **Topological-sort-driven layout from flows.** Removing the explicit
  `layout` mapping in scenarios without cycles/parallel-gateway
  branches — would simplify the LLM's job for ~half the PMo scenarios.
- **Compact textual layout grammars** (e.g., `lane1: A -> B | C`) —
  likely cheaper in tokens, but unclear whether LLMs respect the
  structure.

See also [`LAYOUT_RULES.md`](LAYOUT_RULES.md) for the layout-specific
rules the helper enforces.
