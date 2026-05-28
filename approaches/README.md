# Approaches

The paper evaluates two LLM-based BPMN generation strategies, both
implemented and benchmarked in this repository.

| Folder                                | Approach        | What the LLM emits                              |
|---------------------------------------|-----------------|-------------------------------------------------|
| [`config-helpers/`](config-helpers/)  | Config+Helpers  | A compact `CONFIG = {…}` IR; helper executes it |
| [`no-helper/`](no-helper/)            | No-Helper       | A complete Modelio Jython script directly       |

Both are first-class paper contributions and both are exercised on all
55 PMo benchmark scenarios. See
[`docs/APPROACHES.md`](../docs/APPROACHES.md) for the side-by-side
architectural comparison and
[`docs/DSL_DESIGN.md`](../docs/DSL_DESIGN.md) for why the Config+Helpers
DSL took the form it did.
