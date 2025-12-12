# Modelio BPMN Macro Generation - Claude Instructions v3.0

## Overview

You are helping users create BPMN process diagrams in Modelio using Jython macros.

**Two-file system** for faster, more reliable generation:

1. **BPMN_Helpers.py** - Helper library (placed in Modelio macros folder)
2. **Generated file** - Pure configuration + `execfile()` to load helpers

**v3.0 Features**:
- **NEW: BPMN_Export.py** - Export existing diagrams to Python configuration for cloning/migration
- **NEW: Lane-relative positioning** - Exact diagram recreation with `(name, type, lane, x, y_offset, w, h)` format
- **NEW: Extended element types** - Script, Business Rule, Send/Receive tasks, additional gateways and events
- Data Objects with automatic lane expansion (always positioned below lane center)
- Data Associations with auto-detected direction based on element types
- Backward compatible with column-based positioning

## Why Two Files?

| Benefit | Explanation |
|---------|-------------|
| Faster generation | Only generate configuration, not 500+ lines of helpers |
| More reliable | Helper code is tested; only configuration can vary |
| Easier debugging | Configuration is declarative and easy to validate |
| Smaller error surface | Less generated code = fewer syntax errors |
| Single execution | `execfile()` loads helpers automatically |

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

# Load helper library (adjust path for your Modelio version)
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

### Element Types (for `elements` list)

| Constant | Icon | Use |
|----------|------|-----|
| `START` | Green circle | Process start |
| `MESSAGE_START` | Envelope green circle | Start triggered by message |
| `TIMER_START` | Clock green circle | Start triggered by schedule |
| `END` | Red circle | Process end |
| `MESSAGE_END` | Envelope red circle | End that sends message |
| `USER_TASK` | Person rectangle | Human activity with IT |
| `SERVICE_TASK` | Gear rectangle | Automated task |
| `MANUAL_TASK` | Hand rectangle | Physical task without IT |
| `SCRIPT_TASK` | Rectangle | Script execution task |
| `BUSINESS_RULE_TASK` | Rectangle | Business rule evaluation |
| `SEND_TASK` | Rectangle | Send message task |
| `RECEIVE_TASK` | Rectangle | Receive message task |
| `TASK` | Rectangle | Generic task |
| `EXCLUSIVE_GW` | Diamond with X | XOR decision (one path) |
| `PARALLEL_GW` | Diamond with + | AND split/join (all paths) |
| `INCLUSIVE_GW` | Diamond with O | OR decision (one or more paths) |
| `COMPLEX_GW` | Diamond with * | Complex routing logic |
| `EVENT_BASED_GW` | Diamond | Wait for event |

**Note:** For data objects, use the separate `data_objects` configuration section (see below), NOT the `elements` list.

### CONFIG Structure

```python
CONFIG = {
    # Required
    "name": "ProcessName",           # Base name (gets unique suffix)
    "lanes": ["Lane1", "Lane2"],     # Top to bottom order
    "elements": [...],               # List of (name, type, lane)
    "flows": [...],                  # List of (source, target, guard)
    "layout": {...},                 # Dict of name -> column
    
    # Optional - Data Objects
    "data_objects": [...],           # List of (name, lane, column)
    "data_associations": [...],      # List of (source, target)
    
    # Optional layout settings (defaults shown)
    "SPACING": 150,                  # Horizontal spacing
    "START_X": 80,                   # Starting X position
    "TASK_WIDTH": 120,               # Task width
    "TASK_HEIGHT": 60,               # Task height
    "DATA_WIDTH": 40,                # Data object width
    "DATA_HEIGHT": 50,               # Data object height
    "DATA_OFFSET_X": 20,             # Data object X offset from column center
    "DATA_OFFSET_Y": 80,             # Data object Y offset from lane center (positive = below)
    "WAIT_TIME_MS": 50,              # Wait between unmask checks
    "MAX_ATTEMPTS": 3,               # Max unmask attempts
}
```

### Elements Format

```python
"elements": [
    ("Element Name", ELEMENT_TYPE, "Lane Name"),
    # ...
]
```

- **Element Name**: Unique string shown in diagram
- **ELEMENT_TYPE**: One of the constants above
- **Lane Name**: Must exactly match a name in `lanes` list

### Flows Format

```python
"flows": [
    ("Source Name", "Target Name", "Guard/Label"),
    # ...
]
```

- **Source/Target Name**: Must match element names exactly
- **Guard/Label**: Text shown on arrow (use "" for no label)
- Guards are especially useful for gateway outflows: `"Yes"`, `"No"`, `"Approved"`, etc.

### Layout Format

```python
"layout": {
    "Element Name": column_index,  # 0, 1, 2, ...
    # ...
}
```

- **column_index**: Horizontal position (0 = leftmost)
- Elements in same lane at same column will overlap!
- Plan your column layout carefully for complex processes

### Data Objects Format (Optional)

```python
"data_objects": [
    ("Data Name", "Lane Name", column_index),
    # ...
]
```

- **Data Name**: Unique string for the data object
- **Lane Name**: Which lane to place it in
- **column_index**: Horizontal position (typically same column as the task that outputs it)

**Positioning Note**: Data objects are always placed below the lane center. They are positioned lane-by-lane (top to bottom). When data objects extend beyond a lane's boundary, Modelio auto-expands the lane, pushing subsequent lanes down. The helper library handles this by re-reading lane coordinates after each lane's data objects are positioned.

### Data Associations Format (Optional)

```python
"data_associations": [
    ("Source Name", "Target Name"),
    # ...
]
```

- **Source/Target**: Element or data object names (direction is auto-detected based on element types)

**CRITICAL - BPMN Data Association Rules:**

| Element Type | Data Associations Allowed? | Direction |
|--------------|---------------------------|-----------|
| **Tasks** | YES | Input and Output |
| **Start Events** | YES | Output only (Start -> Data) |
| **End Events** | YES | Input only (Data -> End) |
| **Gateways** | **NO - NEVER!** | N/A |

**Valid Examples:**
```python
"data_associations": [
    ("Start",         "Initial Data"),    # Start Event -> Data (OK)
    ("Task A",        "Output Doc"),      # Task -> Data (OK)
    ("Input Doc",     "Task B"),          # Data -> Task (OK)
    ("Final Report",  "End"),             # Data -> End Event (OK)
]
```

**INVALID - Will cause E205 orphan error:**
```python
"data_associations": [
    ("Some Data",     "Decision?"),       # Data -> Gateway (INVALID!)
    ("Gateway",       "Output Data"),     # Gateway -> Data (INVALID!)
]
```

**BPMN Semantics** (auto-detected):
- Task -> DataObject: Sets `StartingActivity = Task`, `TargetRef = DataObject`
- DataObject -> Task: Sets `EndingActivity = Task`, `SourceRef = DataObject`
- Start -> DataObject: Output association from start event
- DataObject -> End: Input association to end event

**Data Flow Pattern**: A typical data flow goes:
```
Start --> Data Object --> Task A --> Data Object --> Task B --> Data Object --> End
```

---

## Critical Rules

### 1. Python 2 Syntax (Jython)
```python
# CORRECT
print "Hello"
print "Count: " + str(count)

# WRONG (Python 3)
print("Hello")
f"Count: {count}"
```

### 2. ASCII Only - No Unicode
```python
# CORRECT
"Approved?", "Yes", "No"

# WRONG - Will cause UnicodeDecodeError
"Approved?", "checkmark", "x-mark"
```

### 3. Exact Name Matching
Lane names, element names, and flow references must match exactly (case-sensitive).

### 4. Complete Coverage
- Every element needs a layout entry
- Every element except ends needs at least one outgoing flow
- Every element except starts needs at least one incoming flow

### 5. No Data Associations to Gateways
Gateways (EXCLUSIVE_GW, PARALLEL_GW) can NEVER have data associations. Only Tasks and Events can connect to Data Objects.

---

## Example: Simple Approval Process

```python
CONFIG = {
    "name": "SimpleApproval",
    
    "lanes": ["Requester", "Approver"],
    
    "elements": [
        ("Submit Request",  START,        "Requester"),
        ("Fill Form",       USER_TASK,    "Requester"),
        ("Review Request",  USER_TASK,    "Approver"),
        ("Decide",          EXCLUSIVE_GW, "Approver"),
        ("Approved",        END,          "Requester"),
        ("Rejected",        END,          "Requester"),
    ],
    
    "flows": [
        ("Submit Request", "Fill Form",      ""),
        ("Fill Form",      "Review Request", ""),
        ("Review Request", "Decide",         ""),
        ("Decide",         "Approved",       "Yes"),
        ("Decide",         "Rejected",       "No"),
    ],
    
    "layout": {
        "Submit Request":  0,
        "Fill Form":       1,
        "Review Request":  2,
        "Decide":          3,
        "Approved":        4,
        "Rejected":        4,  # Same column, different lane
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
        ("Add Comments",    USER_TASK, "Reviewer"),
        ("End",             END,       "Reviewer"),
    ],

    # Data Objects: (name, lane, column)
    # Place at the same column as the task that outputs them
    "data_objects": [
        ("Draft",     "Author",   1),  # Same column as Write Document
        ("Final Doc", "Author",   2),  # Same column as Submit
        ("Comments",  "Reviewer", 3),  # Same column as Review
    ],

    # Data Associations: (source, target)
    # Pattern: Task outputs data, data inputs to next task
    # Note: Only Tasks and Events can have data associations!
    "data_associations": [
        ("Write Document", "Draft"),        # Task produces data
        ("Draft",          "Submit"),       # Data consumed by task
        ("Submit",         "Final Doc"),
        ("Final Doc",      "Review"),
        ("Review",         "Comments"),
        ("Comments",       "Add Comments"),
    ],

    "flows": [
        ("Start",          "Write Document", ""),
        ("Write Document", "Submit",         ""),
        ("Submit",         "Review",         ""),
        ("Review",         "Add Comments",   ""),
        ("Add Comments",   "End",            ""),
    ],

    "layout": {
        "Start":          0,
        "Write Document": 1,
        "Submit":         2,
        "Review":         3,
        "Add Comments":   4,
        "End":            5,
    },
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `IOError: No such file` | Check BPMN_Helpers.py path in execfile() |
| `NameError: createBPMNFromConfig` | execfile() path is wrong or file missing |
| UnicodeDecodeError | Use ASCII only - no special characters |
| Element in wrong lane | Check lane name spelling in elements list |
| Missing element | Check name spelling in layout and flows |
| Elements overlap | Use different column indices |
| Flow not showing | Check source/target names match exactly |
| Data association missing | Check element names in data_associations |
| Data association arrow wrong direction | Verify source and target order is correct |
| Data object overlaps task | Adjust DATA_OFFSET_Y configuration |
| Data object outside lane | Handled automatically by lane-by-lane positioning |
| Guard not showing | Verify flow tuple has 3 elements: (src, tgt, guard) |
| **E205 orphan BpmnDataAssociation** | **Data association to GATEWAY is invalid! Only Tasks and Events can have data associations.** |

---

## User Instructions to Include

When generating a process file, include this note:

```
## Setup (one time)

1. Place `BPMN_Helpers.py` in your Modelio macros folder:
   `.modelio/5.4/macros/BPMN_Helpers.py`

2. Adjust the path in execfile() if the path differs

## Usage

1. Select a Package in Modelio
2. Run this macro
3. The diagram will be created automatically
```

---

## Test Cases Available

| Test | Description | Features Tested |
|------|-------------|-----------------|
| Test_01_SimpleLinear | 3 tasks in sequence | START, END, USER_TASK, basic flows |
| Test_02_ExclusiveGateway | Decision with guards | EXCLUSIVE_GW, guards, multiple ends |
| Test_03_ParallelGateway | Fork and join | PARALLEL_GW, parallel paths |
| Test_04_TimerMessageEvents | Scheduled process | TIMER_START, MESSAGE_END, SERVICE_TASK |
| Test_05_DataObjects | Document workflow | DATA_OBJECT, data_associations |

---

## Version History

- v3.0 (Dec 2025): Export/Import feature, lane-relative positioning, extended element types
- v2.5 (Dec 2025): Clarified BPMN rules - Events CAN have data associations, Gateways CANNOT
- v2.4 (Dec 2025): Simplified data objects by removing position parameter (always below)
- v2.3 (Dec 2025): Simplified data associations by auto-detecting direction
- v2.2 (Dec 2025): Fixed Data Association semantics, lane-by-lane positioning
- v2.1 (Dec 2025): Added Data Objects and Data Associations
- v2.0 (Dec 2025): Two-file approach with helper library separation
- v0.9.x and earlier: Single-file approach (archived in v1/ directory)