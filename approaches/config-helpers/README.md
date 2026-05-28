# Config+Helpers approach

In the Config+Helpers approach, the LLM emits a compact intermediate
representation — a `CONFIG = {…}` Python literal — and a pre-installed
helper library [`BPMN_Helpers.py`](BPMN_Helpers.py) interprets it,
calling the Modelio Jython API to create the diagram.

This is the approach validated industrially in the MATISSE project and is
the recommended default. See the [No-Helper baseline](../no-helper/) for
the alternative (and [`docs/APPROACHES.md`](../../docs/APPROACHES.md) for
the side-by-side comparison).

## Files

| File                       | Purpose                                                       |
|----------------------------|---------------------------------------------------------------|
| `BPMN_Helpers.py`          | Helper library (install once to Modelio macros folder)        |
| `BPMN_Export.py`           | Reverse direction: export an existing diagram back to CONFIG  |
| `system_prompt.md`         | LLM system prompt                                             |
| `examples/`                | 4 worked examples (ExpenseApproval, Procurement, Complex, NataleItalia) |

## Quick start

See top-level [`README.md`](../../README.md) and [`INSTALL.md`](../../INSTALL.md).

## Generated CONFIG format

```python
CONFIG = {
    "name": "ExpenseApproval",
    "lanes": ["Employee", "Manager", "Finance"],
    "elements": [
        ("Submit Expense",  START,         "Employee"),
        ("Review",          USER_TASK,     "Manager"),
        ("Approved?",       EXCLUSIVE_GW,  "Manager"),
        ("Process Payment", SERVICE_TASK,  "Finance"),
        ("Rejected",        END,           "Manager"),
    ],
    "flows": [
        ("Submit Expense", "Review",          ""),
        ("Approved?",      "Process Payment", "Yes"),
        ("Approved?",      "Rejected",        "No"),
    ],
    "layout": {
        "Submit Expense":  0,
        "Review":          1,
        "Approved?":       2,
        "Process Payment": 3,
        "Rejected":        3,   # same column = auto-stacked
    },
}
```

See [`docs/API_REFERENCE.md`](../../docs/API_REFERENCE.md) for the full
schema and [`docs/LAYOUT_RULES.md`](../../docs/LAYOUT_RULES.md) for the
layout rules `BPMN_Helpers.py` enforces.
