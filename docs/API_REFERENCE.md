# BPMN Helpers API Reference

This document describes all element types, configuration options, and functions available in `BPMN_Helpers.py`.

## Element Type Constants

Use these constants in the `elements` section of your configuration.

**Important:** Data objects use a separate `data_objects` configuration section and are NOT included in the `elements` list.

### Start Events

| Constant | Visual | Description |
|----------|--------|-------------|
| `START` | ○ (green circle) | Standard process start point |
| `MESSAGE_START` | ✉○ (envelope + green circle) | Process triggered by receiving a message |
| `TIMER_START` | ⏰○ (clock + green circle) | Process triggered by timer/schedule |

### End Events

| Constant | Visual | Description |
|----------|--------|-------------|
| `END` | ● (red circle) | Standard process end point |
| `MESSAGE_END` | ✉● (envelope + red circle) | End event that sends a message |

### Tasks

| Constant | Visual | Description |
|----------|--------|-------------|
| `TASK` | ▭ (rectangle) | Generic task |
| `USER_TASK` | 👤▭ (person icon + rectangle) | Human activity requiring IT interaction |
| `SERVICE_TASK` | ⚙▭ (gear icon + rectangle) | Automated/system task |
| `MANUAL_TASK` | ✋▭ (hand icon + rectangle) | Physical task without IT involvement |
| `SCRIPT_TASK` | ▭ (rectangle) | Script execution task |
| `BUSINESS_RULE_TASK` | ▭ (rectangle) | Business rule evaluation |
| `SEND_TASK` | ▭ (rectangle) | Send message task |
| `RECEIVE_TASK` | ▭ (rectangle) | Receive message task |

### Gateways

| Constant | Visual | Description |
|----------|--------|-------------|
| `EXCLUSIVE_GW` | ◇✕ (diamond with X) | XOR - exactly one outgoing path chosen |
| `PARALLEL_GW` | ◇+ (diamond with +) | AND - all paths execute in parallel |
| `INCLUSIVE_GW` | ◇○ (diamond with O) | OR - one or more paths |
| `COMPLEX_GW` | ◇* (diamond with *) | Complex routing logic |
| `EVENT_BASED_GW` | ◇ (diamond) | Wait for event |

### Data Elements

Data objects are configured separately using the `data_objects` section of CONFIG (see [Data Objects List](#data-objects-list) below).

**Note:** `DATA_OBJECT` constant exists internally but is NOT used in the `elements` list. Configure data objects like this:

```python
"data_objects": [
    ("Document Name", "Lane Name", column_index),
]
```

---

## Configuration Object

The `CONFIG` dictionary defines your entire process. Here's the complete structure:

```python
CONFIG = {
    # REQUIRED FIELDS
    "name": "ProcessName",           # Base name (gets unique suffix added)
    "lanes": ["Lane1", "Lane2"],     # Swim lanes, top to bottom order
    "elements": [...],               # List of (name, type, lane) tuples
    "flows": [...],                  # List of (source, target, guard) tuples
    "layout": {...},                 # Dict mapping element names to columns
    
    # OPTIONAL - Data Objects
    "data_objects": [...],           # List of (name, lane, column) tuples
    "data_associations": [...],      # List of (source, target) tuples
    
    # OPTIONAL - Layout Settings (defaults shown)
    "SPACING": 150,                  # Horizontal distance between columns (pixels)
    "START_X": 80,                   # X coordinate of column 0
    "TASK_WIDTH": 120,               # Width of task rectangles
    "TASK_HEIGHT": 60,               # Height of task rectangles
    "DATA_WIDTH": 40,                # Width of data objects
    "DATA_HEIGHT": 50,               # Height of data objects
    "DATA_OFFSET_X": 20,             # Data object X offset from column center
    "DATA_OFFSET_Y": 80,             # Data object Y offset from lane center (positive = below)
    "WAIT_TIME_MS": 50,              # Milliseconds between unmask checks
    "MAX_ATTEMPTS": 3,               # Maximum unmask retry attempts
}
```

---

## Elements List

Format: `(name, type, lane)`

```python
"elements": [
    ("Submit Request", START, "Requester"),
    ("Review Request", USER_TASK, "Reviewer"),
    ("Decision", EXCLUSIVE_GW, "Reviewer"),
    ("Approved", END, "Requester"),
    ("Rejected", END, "Requester"),
]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name and unique identifier |
| `type` | constant | One of the element type constants |
| `lane` | string | Must exactly match a lane in the `lanes` list |

---

## Flows List

Format: `(source, target, guard)`

```python
"flows": [
    ("Submit Request", "Review Request", ""),
    ("Review Request", "Decision", ""),
    ("Decision", "Approved", "Yes"),
    ("Decision", "Rejected", "No"),
]
```

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Name of source element (must match exactly) |
| `target` | string | Name of target element (must match exactly) |
| `guard` | string | Condition label for the flow (empty string if none) |

**Guard usage**:
- Empty string `""` for unconditional flows
- Text label like `"Yes"`, `"No"`, `"Approved"` for conditional flows
- Commonly used on gateway outflows

---

## Layout Dictionary

Format: `{element_name: column_index}`

```python
"layout": {
    "Submit Request": 0,
    "Review Request": 1,
    "Decision": 2,
    "Approved": 3,
    "Rejected": 3,  # Same column as Approved (different lanes)
}
```

| Field | Type | Description |
|-------|------|-------------|
| `element_name` | string | Must match element name exactly |
| `column_index` | integer | Horizontal position (0 = leftmost) |

**Layout tips**:
- Column indices can have gaps (0, 1, 5, 10 is fine)
- Elements in the same lane at the same column will overlap
- Elements in different lanes can share a column (parallel positioning)
- Events and gateways are typically single columns
- Plan complex processes on paper first

---

## Data Objects List

Format: `(name, lane, column)`

```python
"data_objects": [
    ("Draft Document", "Author", 1),
    ("Final Report", "Author", 3),
    ("Comments", "Reviewer", 2),
]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier for the data object |
| `lane` | string | Which lane to place it in |
| `column` | integer | Horizontal position (typically same as related task) |

**Positioning notes**:
- Data objects are always placed below the lane center
- Data objects are positioned lane-by-lane (top to bottom)
- When data objects extend beyond lane boundaries, Modelio auto-expands the lane
- The helper library re-reads lane coordinates after each lane's positioning

---

## Data Associations List

Format: `(source, target)` - direction is auto-detected based on element types.

```python
"data_associations": [
    ("Write Document", "Draft Document"),  # Task produces data
    ("Draft Document", "Review Task"),     # Data consumed by task
]
```

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Element or data object name |
| `target` | string | Element or data object name |

**BPMN Semantics** (auto-detected):

| Flow Direction | Internal Setting |
|----------------|------------------|
| Task → DataObject | `StartingActivity = Task`, `TargetRef = DataObject` |
| DataObject → Task | `EndingActivity = Task`, `SourceRef = DataObject` |

**Data Flow Pattern**:

A typical data flow between tasks goes:
```
Task A --> Data Object --> Task B
```

This creates:
1. Arrow from Task A to Data Object (Task A produces the data)
2. Arrow from Data Object to Task B (Task B consumes the data)

---

## Main Function

### `createBPMNFromConfig(parentPackage, config)`

Creates a complete BPMN process diagram from a configuration dictionary.

**Parameters**:
- `parentPackage` - Modelio Package element where the process will be created
- `config` - Dictionary following the CONFIG structure above

**Returns**: The created BpmnProcess element

**Example**:
```python
from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = { ... }

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        process = createBPMNFromConfig(element, CONFIG)
        print "Created: " + process.getName()
```

---

## Internal Functions (Advanced)

These functions are used internally but can be called directly for custom scenarios.

### Element Creation

```python
_createStartEvent(process, name)        # Create standard start event
_createMessageStartEvent(process, name) # Create message start event
_createTimerStartEvent(process, name)   # Create timer start event
_createEndEvent(process, name)          # Create standard end event
_createMessageEndEvent(process, name)   # Create message end event
_createUserTask(process, name)          # Create user task
_createServiceTask(process, name)       # Create service task
_createManualTask(process, name)        # Create manual task
_createExclusiveGateway(process, name)  # Create exclusive gateway
_createParallelGateway(process, name)   # Create parallel gateway
_createDataObject(process, name)        # Create data object
```

### Lane Management

```python
_createLane(laneSet, name)              # Create a lane in a lane set
_addToLane(element, lane)               # Assign element to lane
```

### Flow and Association Creation

```python
_createSequenceFlow(process, source, target, guard="")
_createDataAssociation(process, source, target, direction)
```

### Diagram Utilities

```python
_getGraphics(diagramHandle, element)    # Get diagram graphics for element
_getBounds(diagramHandle, element)      # Get element bounds as dict
_getLaneCenterY(diagramHandle, lane)    # Get Y coordinate for lane center
```

---

## Configuration Examples

### Minimal Process

```python
CONFIG = {
    "name": "Minimal",
    "lanes": ["User"],
    "elements": [
        ("Start", START, "User"),
        ("End", END, "User"),
    ],
    "flows": [
        ("Start", "End", ""),
    ],
    "layout": {
        "Start": 0,
        "End": 1,
    },
}
```

### Decision Process

```python
CONFIG = {
    "name": "Decision",
    "lanes": ["User", "System"],
    "elements": [
        ("Request", START, "User"),
        ("Process", SERVICE_TASK, "System"),
        ("Check", EXCLUSIVE_GW, "System"),
        ("Success", END, "User"),
        ("Failure", END, "User"),
    ],
    "flows": [
        ("Request", "Process", ""),
        ("Process", "Check", ""),
        ("Check", "Success", "Valid"),
        ("Check", "Failure", "Invalid"),
    ],
    "layout": {
        "Request": 0,
        "Process": 1,
        "Check": 2,
        "Success": 3,
        "Failure": 3,
    },
}
```

### Parallel Execution

```python
CONFIG = {
    "name": "Parallel",
    "lanes": ["Coordinator", "Team A", "Team B"],
    "elements": [
        ("Start", START, "Coordinator"),
        ("Split", PARALLEL_GW, "Coordinator"),
        ("Task A", USER_TASK, "Team A"),
        ("Task B", USER_TASK, "Team B"),
        ("Join", PARALLEL_GW, "Coordinator"),
        ("End", END, "Coordinator"),
    ],
    "flows": [
        ("Start", "Split", ""),
        ("Split", "Task A", ""),
        ("Split", "Task B", ""),
        ("Task A", "Join", ""),
        ("Task B", "Join", ""),
        ("Join", "End", ""),
    ],
    "layout": {
        "Start": 0,
        "Split": 1,
        "Task A": 2,
        "Task B": 2,
        "Join": 3,
        "End": 4,
    },
}
```

### Process with Data Objects

```python
CONFIG = {
    "name": "DocumentReview",
    "lanes": ["Author", "Reviewer"],
    "elements": [
        ("Start", START, "Author"),
        ("Write Document", USER_TASK, "Author"),
        ("Submit", USER_TASK, "Author"),
        ("Review", USER_TASK, "Reviewer"),
        ("End", END, "Reviewer"),
    ],
    "data_objects": [
        ("Draft", "Author", 1),
        ("Final Doc", "Author", 2),
    ],
    "data_associations": [
        ("Write Document", "Draft"),
        ("Draft", "Submit"),
        ("Submit", "Final Doc"),
        ("Final Doc", "Review"),
    ],
    "flows": [
        ("Start", "Write Document", ""),
        ("Write Document", "Submit", ""),
        ("Submit", "Review", ""),
        ("Review", "End", ""),
    ],
    "layout": {
        "Start": 0,
        "Write Document": 1,
        "Submit": 2,
        "Review": 3,
        "End": 4,
    },
}
```

---

## Error Handling

The helper library prints diagnostic messages during execution:

```
==================================================================
BPMN PROCESS CREATION
==================================================================
Process Name: MyProcess_12345

== PHASE 1: CREATE PROCESS & LANES ==============================
[1] Process: MyProcess_12345
[2] Lanes: User, Admin

== PHASE 2: CREATE ELEMENTS =====================================
[3] User: 3 elements
[4] Admin: 2 elements
  Total: 5 elements

== PHASE 3: CREATE DIAGRAM ======================================
...

== PHASE 7: CREATE DATA OBJECTS =================================
[12] Created 2 data objects

== PHASE 8: CREATE DATA ASSOCIATIONS ============================
[13] Created 4 data associations

==================================================================
COMPLETE: MyProcess_12345
==================================================================
```

### Common Error Messages

| Message | Cause | Solution |
|---------|-------|----------|
| `ERROR: Unknown element type: X` | Invalid type constant | Use valid constant from list above |
| `ERROR: Please select a Package` | Wrong element selected | Select a Package in model explorer |
| `IOError: No such file` | BPMN_Helpers.py path wrong | Check execfile() path |
| `NameError: createBPMNFromConfig` | Helper file not loaded | Verify execfile() path is correct |
| `[Unmask] ... FAILED` | Element not displayed | Usually auto-resolves; check layout |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| UnicodeDecodeError | Use ASCII only - no special characters |
| Element in wrong lane | Check lane name spelling in elements list |
| Missing element | Check name spelling in layout and flows |
| Elements overlap | Use different column indices |
| Flow not showing | Check source/target names match exactly |
| Data association missing | Check element names in data_associations |
| Data association arrow wrong | Verify source and target order |
| Data object overlaps task | Adjust DATA_OFFSET_Y configuration |
| Guard not showing | Verify flow tuple has 3 elements |

---

## Version History

- **v3.0** (December 2025): Export/Import feature, lane-relative positioning, extended element types
- **v2.5** (December 2025): Clarified BPMN rules - Events CAN have data associations, Gateways CANNOT
- **v2.4** (December 2025): Simplified data objects by removing position parameter (always below)
- **v2.3** (December 2025): Simplified data associations by auto-detecting direction
- **v2.2** (December 2025): Fixed Data Association semantics, lane-by-lane data object positioning
- **v2.1** (December 2025): Added Data Objects and Data Associations support
- **v2.0** (December 2025): Configuration-based approach with two-file system
- **v1.x**: Original inline implementations
