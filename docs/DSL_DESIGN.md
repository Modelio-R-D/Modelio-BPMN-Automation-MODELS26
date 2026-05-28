# DSL design rationale and alternatives explored

The Config+Helpers approach hinges on a compact intermediate representation
(IR) that the LLM emits in lieu of full Modelio Jython code. This document
records the design space we explored before settling on the form shipped in
[`approaches/config-helpers/system_prompt.md`](../approaches/config-helpers/system_prompt.md).

It addresses Reviewer 3's main question — *"What DSL alternatives did you try
(e.g., different abstraction levels, ordering methods, syntactic formats)
during the iterations?"* — and meta-review point 2.

> **TODO (authors):** the section is structured around the dimensions
> Reviewer 3 named; concrete iterations need to be filled in from lab notes.

---

## Final form (what the paper reports)

The IR is a Python literal `CONFIG = {…}` written by the LLM and consumed by
`BPMN_Helpers.py`. It carries:

- `name`: process name
- `lanes`: ordered list of lane names
- `elements`: list of `(label, type_constant, lane)` triples
- `flows`: list of `(source_label, target_label, edge_label)` triples
- `layout`: mapping `label → column_index` for left-to-right placement
- `data_objects` *(optional)*: `(name, lane, column)`
- `data_associations` *(optional)*: `(source, target)`, direction
  auto-detected

See [`API_REFERENCE.md`](API_REFERENCE.md) for the full schema.

## Design dimensions and choices

### Abstraction level

| Level | What the LLM writes | Outcome |
|------|---------------------|---------|
| **L0** — Raw Modelio Jython API | `bpmnTask = process.getElement().create(...)` directly | This is the **No-Helper baseline**; see [`approaches/no-helper/`](../approaches/no-helper/). Outputs are ~5× larger; success rates lower except on Claude. |
| **L1** — BPMN XML | LLM emits BPMN 2.0 XML; helper converts to Modelio | `<<TODO>>` — Tried? Did we test it? |
| **L2** — Compact Python literal (**adopted**) | `CONFIG = {…}` | Best efficiency/accuracy trade-off across models. |
| **L3** — Domain-specific natural language | "Lane Employee: submit then review then …" | `<<TODO>>` |

### Ordering of elements

How is the visual left-to-right order communicated to the helper?

- **Implicit by list position** — relied on the element list order. Brittle:
  LLMs occasionally produced topologically correct lists that *visually*
  flowed right-to-left. Rejected.
- **Explicit `layout: {label: column}`** *(adopted)* — decouples logical
  ordering from list position. v3.2 added auto-stacking for same-column,
  same-lane elements, removing a class of layout bugs.
- **Topological-sort from flows** — `<<TODO>>` — considered? rejected because
  cycles (loops) and parallel paths make it ambiguous.

### Syntactic format

- **JSON** — strict, but LLMs commonly violated quoting around BPMN type
  constants (e.g., `EXCLUSIVE_GW`). Rejected.
- **YAML** — `<<TODO>>` — tried? Rejected for `<<reason>>`.
- **Python literal** *(adopted)* — type constants can be referenced as
  names imported by the helper; tuple syntax handles the heterogeneous
  triples/quadruples cleanly.

### Element-type vocabulary

The helper exposes ~30 named constants (see the table in
[`../README.md`](../README.md)). We considered:

- Letting the LLM emit raw BPMN URIs — too verbose, too easy to get wrong.
- A reduced vocabulary (only Task / Gateway / Event) — lost expressiveness
  for the MATISSE scenarios that need Send/Receive tasks, Timer events, etc.

## Iterations that shaped the final form

- **v1.0 → v2.0** *(Dec 2025)* — split into Helpers + Config files; this is
  the move from L0 to L2.
- **v2.1 → v2.5** *(Dec 2025)* — refined Data Object semantics; learned that
  Modelio rejects gateways with data associations (now a hard rule in the
  prompt).
- **v3.0** *(Dec 2025)* — added round-trip export so LLM-generated diagrams
  can be re-extracted as `CONFIG = {…}`.
- **v3.2** *(Dec 2025)* — auto-stacking: same-lane + same-column elements
  stack 90 px vertically without manual offsets.

## Open design choices (future work)

- Embedding ordering inside the flows list (turning DSL graph-centric
  instead of element-centric) — Reviewer 3 raised "ordering methods" as a
  dimension; worth exploring whether a pure-flow DSL is more LLM-natural.
- Compact textual layout grammars (e.g., `lane1: A -> B | C`) — likely
  cheaper in tokens, but unclear whether LLMs respect the structure.

See also [`LAYOUT_RULES.md`](LAYOUT_RULES.md) for the layout-specific rules
the helper enforces.
