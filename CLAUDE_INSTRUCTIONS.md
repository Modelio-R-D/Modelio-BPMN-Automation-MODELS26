# Modelio BPMN Macro Generation - Claude Instructions v3.2

## Overview

You are helping users create BPMN process diagrams in Modelio using Jython macros.

**Two-file system** for faster, more reliable generation:

1. **BPMN_Helpers.py** - Helper library (placed in Modelio macros folder)
2. **Generated file** - Pure configuration + `execfile()` to load helpers

**v3.2 Updates**:
- **Auto-stacking**: Elements in same lane + same column are automatically stacked (90px apart)
- No more manual y_offset needed for gateway branches - just use same column number
- Manual `(column, y_offset)` format still supported for precise control

---

## Quick Start for Claude

When a user asks for a BPMN diagram:

1. **Ask clarifying questions** about lanes, tasks, decisions if needed
2. **Generate ONLY the configuration file** (with execfile to load helpers)
3. **Remind user** to place BPMN_Helpers.py in their macros folder

### Minimal Generated File Template

```python
#
# ProcessName.py
#
# Description: [Brief description]
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ProcessName",
    
    "lanes": ["Lane1", "Lane2"],
    
    "elements": [
        ("Start", START, "Lane1"),
        ("Task 1", USER_TASK, "Lane1"),
        ("End", END, "Lane2"),
    ],
    
    "flows": [
        ("Start", "Task 1", ""),
        ("Task 1", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Task 1": 1,
        "End": 2,
    },
}

# Entry point
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
```

---

## Configuration Reference

### Element Types (Complete Reference)

#### Start Events
| Constant | Description |
|----------|-------------|
| `START` | Standard start (green circle) |
| `MESSAGE_START` | Triggered by message |
| `TIMER_START` | Triggered by schedule |
| `SIGNAL_START` | Triggered by signal |
| `CONDITIONAL_START` | Triggered by condition |

#### End Events
| Constant | Description |
|----------|-------------|
| `END` | Standard end (red circle) |
| `MESSAGE_END` | Sends message on completion |
| `SIGNAL_END` | Sends signal on completion |
| `TERMINATE_END` | Terminates all process instances |
| `ERROR_END` | Throws error |

#### Intermediate Events
| Constant | Description |
|----------|-------------|
| `INTERMEDIATE_CATCH` | Generic catch event |
| `INTERMEDIATE_THROW` | Generic throw event |
| `MESSAGE_CATCH` | Wait for message |
| `MESSAGE_THROW` | Send message |
| `TIMER_CATCH` | Wait for timer |
| `SIGNAL_CATCH` | Wait for signal |
| `SIGNAL_THROW` | Send signal |

#### Tasks
| Constant | Description |
|----------|-------------|
| `TASK` | Generic task |
| `USER_TASK` | Human activity with IT (person icon) |
| `SERVICE_TASK` | Automated task (gear icon) |
| `MANUAL_TASK` | Physical task without IT (hand icon) |
| `SCRIPT_TASK` | Script execution |
| `BUSINESS_RULE_TASK` | Business rule evaluation |
| `SEND_TASK` | Send message |
| `RECEIVE_TASK` | Receive message |

#### Gateways
| Constant | Description |
|----------|-------------|
| `EXCLUSIVE_GW` | XOR - one path (X diamond) |
| `PARALLEL_GW` | AND - all paths (+ diamond) |
| `INCLUSIVE_GW` | OR - one or more paths (O diamond) |
| `COMPLEX_GW` | Complex routing (* diamond) |
| `EVENT_BASED_GW` | Wait for event |

**Note:** For data objects, use the `data_objects` configuration section, NOT the `elements` list.

### CONFIG Structure

```python
CONFIG = {
    # Required
    "name": "ProcessName",           # Base name (gets unique suffix)
    "lanes": ["Lane1", "Lane2"],     # Top to bottom order
    "elements": [...],               # List of (name, type, lane)
    "flows": [...],                  # List of (source, target, guard)
    "layout": {...},                 # Dict of name -> column or (column, y_offset)
    
    # Optional - Data Objects
    "data_objects": [...],           # List of (name, lane, column)
    "data_associations": [...],      # List of (source, target)
    
    # Optional layout settings (defaults shown)
    "SPACING": 150,                  # Horizontal spacing between columns
    "START_X": 80,                   # Starting X position
    "TASK_WIDTH": 120,               # Task width
    "TASK_HEIGHT": 60,               # Task height
    "DATA_WIDTH": 40,                # Data object width
    "DATA_HEIGHT": 50,               # Data object height
    "DATA_OFFSET_X": 90,             # Data object X offset (near right side of task)
    "DATA_OFFSET_Y": 10,             # Data object Y gap below task bottom
}
```

### Layout Format (with Auto-Stacking)

```python
"layout": {
    # Simple format: column index only
    "Element Name": column_index,

    # Extended format: (column, y_offset) for manual vertical positioning
    "Element Name": (column_index, y_offset),
}
```

**Auto-Stacking (v3.2):**
When multiple elements in the **same lane** share the **same column**, they are automatically stacked vertically with 90px spacing. No manual y_offset needed!

```python
# Auto-stacking example - just use the same column number
"layout": {
    "Decision?":     5,
    "Success Path":  6,    # Same lane, same column = auto-stacked
    "Error Path":    6,    # Automatically placed 90px below Success Path
}
```

**Manual Y-Offset (optional):**
You can still use `(column, y_offset)` tuple for precise control:
- `y_offset = 0` → default position (laneTop + 20)
- **Positive y_offset** → moves element **DOWN** within lane

**Example - Manual Override:**
```python
"layout": {
    "Success Path": (6, 0),      # Explicit: default position
    "Error Path":   (6, 120),    # Explicit: 120px below default
}
```

### Elements Format

```python
"elements": [
    ("Element Name", ELEMENT_TYPE, "Lane Name"),
    # ...
]
```

### Flows Format

```python
"flows": [
    ("Source Name", "Target Name", "Guard/Label"),
    # ...
]
```

- Guards are useful for gateway outflows: `"Yes"`, `"No"`, `"Approved"`, etc.

### Data Objects Format

```python
"data_objects": [
    ("Data Name", "Lane Name", column_index),
    # ...
]
```

**Positioning:** Data objects are positioned **below their source task**. The source task is determined from data associations (Task -> DataObject pattern).

### Data Associations Format

```python
"data_associations": [
    ("Source Name", "Target Name"),
    # ...
]
```

**CRITICAL - BPMN Rules:**

| Element Type | Data Associations? |
|--------------|-------------------|
| **Tasks** | YES |
| **Start Events** | YES (output only) |
| **End Events** | YES (input only) |
| **Gateways** | **NO - NEVER!** |

**Valid:**
```python
"data_associations": [
    ("Task A",       "Output Doc"),    # Task -> Data (OK)
    ("Input Doc",    "Task B"),        # Data -> Task (OK)
]
```

**INVALID - Will cause E205 error:**
```python
"data_associations": [
    ("Some Data",    "Decision?"),     # Data -> Gateway (INVALID!)
]
```

---

## Critical Rules

### 1. Python 2 Syntax (Jython)
```python
# CORRECT
print "Hello"

# WRONG (Python 3)
print("Hello")
```

### 2. ASCII Only - No Unicode
```python
# CORRECT
"Approved?", "Yes", "No"

# WRONG
"Approved?", "✓", "✗"
```

### 3. Exact Name Matching
Lane names, element names, and flow references must match exactly (case-sensitive).

### 4. Sequential Tasks Need Different Columns
Tasks connected by a flow (Task A → Task B) **MUST** be in different columns:

```python
# BAD - Sequential tasks overlap
"flows": [("Task A", "Task B", "")],
"layout": {
    "Task A": 5,
    "Task B": 5,   # WRONG! Same column as predecessor
}

# GOOD - Sequential tasks in consecutive columns
"layout": {
    "Task A": 5,
    "Task B": 6,   # CORRECT! Next column
}
```

### 5. Same Column = Auto-Stacked (v3.2)
Elements in the same lane and same column are automatically stacked:

```python
# SIMPLE - Just use same column number for gateway branches
"layout": {
    "Decision?":     5,
    "Success Path":  6,    # Auto-stacked with Error Path
    "Error Path":    6,    # Automatically 90px below Success Path
}

# WRONG - Don't put sequential tasks in same column
"layout": {
    "Task A": 5,
    "Task B": 5,   # WRONG if Task A -> Task B (sequential)!
}
```

### 6. No Data Associations to Gateways
Gateways can NEVER have data associations.

---

## Example: Gateway with Stacked Outputs

```python
CONFIG = {
    "name": "ValidationProcess",

    "lanes": ["Validator"],

    "elements": [
        ("Start",            START,        "Validator"),
        ("Validate",         SERVICE_TASK, "Validator"),
        ("Valid?",           EXCLUSIVE_GW, "Validator"),
        ("Process Valid",    SERVICE_TASK, "Validator"),
        ("Handle Invalid",   SERVICE_TASK, "Validator"),
        ("End",              END,          "Validator"),
    ],

    "flows": [
        ("Start",          "Validate",       ""),
        ("Validate",       "Valid?",         ""),
        ("Valid?",         "Process Valid",  "Yes"),
        ("Valid?",         "Handle Invalid", "No"),
        ("Process Valid",  "End",            ""),
        ("Handle Invalid", "End",            ""),
    ],

    "layout": {
        "Start":          0,
        "Validate":       1,
        "Valid?":         2,
        "Process Valid":  3,    # Same column = auto-stacked
        "Handle Invalid": 3,    # Automatically 90px below Process Valid
        "End":            4,
    },
}
```

---

## Example: Process with Data Objects

```python
CONFIG = {
    "name": "DocumentReview",

    "lanes": ["Author", "Reviewer"],

    "elements": [
        ("Start",           START,     "Author"),
        ("Write Document",  USER_TASK, "Author"),
        ("Submit",          USER_TASK, "Author"),
        ("Review",          USER_TASK, "Reviewer"),
        ("End",             END,       "Reviewer"),
    ],

    "data_objects": [
        ("Draft",     "Author",   1),
        ("Final Doc", "Author",   2),
    ],

    "data_associations": [
        ("Write Document", "Draft"),
        ("Draft",          "Submit"),
        ("Submit",         "Final Doc"),
        ("Final Doc",      "Review"),
    ],

    "flows": [
        ("Start",          "Write Document", ""),
        ("Write Document", "Submit",         ""),
        ("Submit",         "Review",         ""),
        ("Review",         "End",            ""),
    ],

    "layout": {
        "Start":          0,
        "Write Document": 1,
        "Submit":         2,
        "Review":         3,
        "End":            4,
    },
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `IOError: No such file` | Check BPMN_Helpers.py path |
| `NameError: createBPMNFromConfig` | execfile() path is wrong |
| UnicodeDecodeError | Use ASCII only |
| Element in wrong lane | Check lane name spelling |
| Elements overlap | Use different columns or y_offsets |
| Data object overlaps task | Automatic - positioned below source task |
| **E205 orphan BpmnDataAssociation** | Data association to GATEWAY is invalid! |

---

## Version History

- v3.2 (Dec 2025): Auto-stacking for same-lane/same-column elements
- v3.1 (Dec 2025): Fixed data association export, Y-offset layout, complete element types
- v3.0 (Dec 2025): Export/Import, lane-relative positioning, extended elements
- v2.x (Dec 2025): Data objects, two-file approach