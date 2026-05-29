# BPMN Helper Library Execution Flow

This document describes the internal execution phases of `createBPMNFromConfig()` in `BPMN_Helpers.py`.

## Overview

When you call `createBPMNFromConfig(parentPackage, CONFIG)`, the library executes in **8 phases** (with 3 optional sub-phases for data objects):

```
PHASE 1:  Create Process & Lanes
PHASE 2:  Create Elements
PHASE 2B: Create Data Objects (optional)
PHASE 3:  Create Diagram
PHASE 4:  Wait for Auto-Unmask
PHASE 5:  Reposition Elements
PHASE 5B: Reposition Data Objects (optional)
PHASE 6:  Create Flows
PHASE 6B: Create Data Associations (optional)
FINAL:    Save & Close
```

---

## Phase-by-Phase Breakdown

### Phase 1: Create Process & Lanes

**Purpose:** Create the BPMN process container and all swim lanes

**Operations:**
1. Create `BpmnProcess` with unique timestamped name: `ProcessName_12345`
2. Create `BpmnLaneSet` attached to the process
3. Create each lane in order (top to bottom in diagram)
4. Store lane references in `lanes` dictionary

**Console Output:**
```
== PHASE 1: CREATE PROCESS & LANES ==============================
[1] Process: ExpenseApproval_12345
[2] Lanes: Employee, Manager, Finance
```

**Code Reference:** `BPMN_Helpers.py:496-515`

---

### Phase 2: Create Elements

**Purpose:** Create all tasks, events, and gateways

**Operations:**
1. Iterate through `config["elements"]`
2. For each `(name, type, lane)` tuple:
   - Call appropriate creator function (`_createUserTask`, `_createStartEvent`, etc.)
   - Assign element to its lane via `_addToLane()`
   - Store reference in `elementRefs` dict and `elementLanes` dict
3. Group elements by lane for logging

**Console Output:**
```
== PHASE 2: CREATE ELEMENTS =====================================
[3] Employee: 7 elements
[4] Manager: 6 elements
[5] Finance: 7 elements

  Total: 20 elements
```

**Code Reference:** `BPMN_Helpers.py:519-552`

---

### Phase 2B: Create Data Objects (Optional)

**Purpose:** Create data object elements if configured

**Conditions:** Only executes if `config["data_objects"]` exists and is non-empty

**Operations:**
1. Iterate through `config["data_objects"]`
2. For each `(name, lane, column)` tuple:
   - Create `BpmnDataObject` via `_createDataObject()`
   - Assign to lane
   - Store in `dataObjectRefs`, `dataObjectLanes`, `dataObjectLayout`
   - Also add to `elementRefs` for association lookups

**Console Output:**
```
== PHASE 2B: CREATE DATA OBJECTS ================================
[6] Data Objects: 3
```

**Code Reference:** `BPMN_Helpers.py:555-588`

---

### Phase 3: Create Diagram

**Purpose:** Create the visual diagram and trigger Modelio's auto-unmask

**Operations:**
1. Create `BpmnProcessDesignDiagram` linked to the process
2. Get diagram handle via `getDiagramService()`
3. **Save diagram** - This triggers Modelio's auto-unmask mechanism

**Console Output:**
```
== PHASE 3: CREATE DIAGRAM ======================================
[7] Diagram: ExpenseApproval_12345
[8] Save (triggers auto-unmask)
```

**Key Insight:** Saving the diagram causes Modelio to automatically unmask (display) elements. This is non-deterministic - sometimes all elements appear, sometimes only partial.

**Code Reference:** `BPMN_Helpers.py:591-605`

---

### Phase 4: Wait for Auto-Unmask

**Purpose:** Wait for Modelio to finish auto-unmasking elements, with fallback

**Operations:**
1. **Polling loop** (default: 3 attempts × 50ms):
   - Check if each element has diagram graphics via `_getGraphics()`
   - Collect successfully unmasked elements
   - Sleep between attempts
2. **Manual unmask fallback** for missing elements:
   - Calculate lane center Y position for each lane
   - Call `diagramHandle.unmask(elem, 100, laneY)` **inside correct lane**
   - Critical: Must unmask at lane Y position, not at (0,0)

**Console Output:**
```
== PHASE 4: WAIT FOR AUTO-UNMASK ================================
  [Attempt 1] Found: 15/20 | Missing: Submit Reque, Approve Expe, ...
  [Attempt 2] Found: 18/20 | Missing: Expense Rej, Expense Paid
  [Attempt 3] Found: 18/20 | Missing: Expense Rej, Expense Paid

[9] Manual unmask for missing elements...

  [Unmask] Expense Rejected -> Y=150 (Employee): OK
  [Unmask] Expense Paid -> Y=450 (Finance): OK

[10] Elements ready: 20/20
  Lanes: Employee(50-200); Manager(200-350); Finance(350-500)
```

**Key Discovery (v0.8.0):** Modelio auto-unmasks non-deterministically. Waiting longer doesn't help.

**Key Discovery (v0.8.3):** Manual unmask MUST be at the lane's Y position. `unmask(elem, 0, 0)` fails.

**Code Reference:** `BPMN_Helpers.py:608-634`

---

### Phase 5: Reposition Elements

**Purpose:** Move all tasks, events, gateways to their configured grid positions

**Operations:**
1. Read lane center Y coordinates (fixed values, read once)
2. For each element in `config["layout"]`:
   - Calculate target X: `START_X + SPACING × column`
   - Get lane center Y from lane bounds
   - Apply task dimensions if element is a task (default: 120×60)
   - Keep original dimensions for events and gateways
   - Set new bounds via `setBounds(Rectangle(x, y, w, h))`
   - Save diagram after each element

**Console Output:**
```
== PHASE 5: REPOSITION ELEMENTS =================================
[11] Employee centerY = 125
[12] Manager centerY = 275
[13] Finance centerY = 425

[14] Repositioned: 20/20
```

**Code Reference:** `BPMN_Helpers.py:637-698`

---

### Phase 5B: Reposition Data Objects (Optional)

**Purpose:** Position data objects with proper lane expansion handling

**Conditions:** Only executes if `config["data_objects"]` exists

**Operations:**
1. **Process each lane sequentially** (top to bottom):
   - **Re-read current lane center Y** (may have shifted due to previous lane expansion)
   - Find all data objects in this lane
   - For each data object:
     - Calculate X: `START_X + SPACING × column + DATA_OFFSET_X`
     - Calculate Y: `laneCenterY + DATA_OFFSET_Y` (always below)
     - Set bounds with data object dimensions (default: 40×50)
   - **Save diagram** (triggers Modelio's lane auto-expansion)
2. Re-reading lane Y after each lane handles Modelio pushing lanes down

**Console Output:**
```
== PHASE 5B: REPOSITION DATA OBJECTS ============================
[Employee] center=125 bounds=50-200
  Draft Document -> (190,205)
  Final Doc -> (340,205)

[Finance] center=500 bounds=350-650
  Payment Receipt -> (490,580)

[15] Data objects repositioned: 3/3
```

**Key Discovery (v2.2):** Modelio auto-expands lanes when data objects extend beyond boundaries. This shifts subsequent lanes down. Solution: process lane-by-lane and re-read coordinates.

**Code Reference:** `BPMN_Helpers.py:701-771`

---

### Phase 6: Create Flows

**Purpose:** Create sequence flows (arrows) between elements

**Operations:**
1. Iterate through `config["flows"]`
2. For each `(source, target, guard)` tuple:
   - Look up source and target elements in `elementRefs`
   - Create `BpmnSequenceFlow`
   - Set `SourceRef` and `TargetRef`
   - If guard provided: set as flow name and condition expression

**Console Output:**
```
== PHASE 6: CREATE FLOWS ========================================
[16] Created 25 sequence flows
```

**Code Reference:** `BPMN_Helpers.py:774-791`

---

### Phase 6B: Create Data Associations (Optional)

**Purpose:** Create data associations with correct BPMN semantics

**Conditions:** Only executes if `config["data_associations"]` exists

**Operations:**
1. Iterate through `config["data_associations"]`
2. For each `(source, target)` tuple:
   - Look up source and target in `elementRefs`
   - Create `BpmnDataAssociation`
   - Auto-detect direction based on element types:
     - **Task → DataObject**: `StartingActivity=source`, `TargetRef=target`
     - **DataObject → Task**: `SourceRef=source`, `EndingActivity=target`

**Console Output:**
```
== PHASE 6B: CREATE DATA ASSOCIATIONS ===========================
[17] Data associations: 6
```

**Key Discovery (v2.2):** BPMN data associations require specific property settings for correct semantics. Using the wrong properties results in incorrect arrows.

**Code Reference:** `BPMN_Helpers.py:794-821`

---

### Final: Save & Close

**Purpose:** Complete diagram creation and cleanup

**Operations:**
1. Final `diagramHandle.save()`
2. `diagramHandle.close()`
3. Print summary with counts

**Console Output:**
```
==================================================================
COMPLETE: ExpenseApproval_12345
==================================================================
Lanes: 3 | Elements: 20 | Data: 3 | Flows: 25 | DataAssoc: 6
==================================================================
```

**Code Reference:** `BPMN_Helpers.py:823-840`

---

## Phase Dependencies

### Sequential Dependencies

These phases MUST execute in order:

```
1 → 2 → 3 → 4 → 5 → 6
```

**Why:**
- Phase 2 needs process from Phase 1
- Phase 3 needs elements from Phase 2
- Phase 4 needs diagram from Phase 3
- Phase 5 needs graphics from Phase 4
- Phase 6 needs positioned elements from Phase 5

### Optional Sub-Phase Insertions

Data object phases insert at specific points:

```
1 → 2 → [2B] → 3 → 4 → 5 → [5B] → 6 → [6B]
```

**Why:**
- 2B after 2: Data objects are elements, need process from Phase 1
- 5B after 5: Positioning needs graphics from Phase 4
- 6B after 6: Associations need positioned elements from Phase 5/5B

---

## Key Insights from Version History

### Auto-Unmask Discovery (v0.8.0)
- Modelio automatically unmasks when diagram is created
- No need to call `unmask()` explicitly for initial display
- BUT: It's non-deterministic and may miss elements

### Lane-Aware Unmask (v0.8.3)
- Manual unmask must specify **correct Y position inside lane**
- `unmask(elem, 0, 0)` fails - Modelio places element at (0,0) which is outside lanes
- `unmask(elem, 100, laneY)` succeeds - places inside lane

### Data Object Lane Expansion (v2.2)
- Positioning data objects below tasks can extend beyond lane boundaries
- Modelio auto-expands lanes to fit, pushing subsequent lanes down
- Solution: Process lanes sequentially, re-read Y coordinates after each lane

### Data Association Semantics (v2.2)
- BPMN requires specific property combinations for correct arrow direction
- Direction is auto-detected based on element types
- Task → DataObject: set `StartingActivity` + `TargetRef`
- DataObject → Task: set `SourceRef` + `EndingActivity`

---

## Troubleshooting by Phase

| Problem | Likely Phase | Solution |
|---------|-------------|----------|
| Elements not visible | Phase 4 | Check MAX_ATTEMPTS and WAIT_TIME_MS |
| Elements in wrong positions | Phase 5 | Check layout dict column indices |
| Elements overlap | Phase 5 | Ensure unique column indices per lane |
| Data objects in wrong position | Phase 5B | Check DATA_OFFSET_X/Y values |
| Data objects overlap tasks | Phase 5B | Increase DATA_OFFSET_Y |
| Lanes pushed down unexpectedly | Phase 5B | Expected behavior - lane auto-expansion |
| Flows missing | Phase 6 | Check source/target names match exactly |
| Data association arrow wrong direction | Phase 6B | Verify source and target order |
| Guard labels not showing | Phase 6 | Ensure flow tuple has 3 elements |

---

## Performance Characteristics

| Phase | Typical Time | Notes |
|-------|--------------|-------|
| 1 | <10ms | Minimal - just object creation |
| 2 | <50ms | Scales with element count |
| 2B | <20ms | Only if data objects configured |
| 3 | <10ms | Diagram creation is fast |
| 4 | 50-150ms | Depends on auto-unmask success (3 × 50ms default) |
| 5 | 50-200ms | Scales with element count (save after each) |
| 5B | 30-100ms | Depends on data object count + lane expansions |
| 6 | <50ms | Flow creation is fast |
| 6B | <30ms | Association creation is fast |

**Total:** Typically 200-600ms for a 20-element process with data objects.

---

## Console Output Format

Each phase prints structured output:

```
==================================================================
BPMN PROCESS CREATION
==================================================================
Process Name: ProcessName_12345
==================================================================

== PHASE X: PHASE NAME ==========================================

[step] Operation description
[step] Operation result

== PHASE X+1: NEXT PHASE ========================================
...
==================================================================
COMPLETE: ProcessName_12345
==================================================================
Summary line
==================================================================
```

This format helps with:
- **Debugging:** Identify which phase failed
- **Performance:** See where time is spent
- **Validation:** Verify expected element counts
