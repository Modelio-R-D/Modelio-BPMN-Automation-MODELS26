# Modelio BPMN Macro Generation - Claude Instructions

## Overview

You are helping users create BPMN process diagrams in Modelio using Jython macros. Use the BPMN_Template.py as the base for all scripts.

**IMPORTANT**: Always include complete debug logging in every script to facilitate issue discovery and learning of Modelio API behavior.

## Key Discovery: Auto-Unmask Behavior

**From Modelio Developers (December 2025):**

> Modelio automatically unmasks all existing elements when a diagram is created. 
> There is no need to call `unmask()` manually. However, this may take time, 
> so before repositioning, we need to check if elements are already available 
> and wait if necessary.

### Implications:

1. **DO NOT** call `diagramHandle.unmask()` manually for initial display
2. **DO** wait for elements to be available before repositioning
3. **DO** check `getDiagramGraphics(element)` to verify element is ready
4. **IF** elements are still missing after waiting â†’ manual unmask **inside the correct lane**

### Wait Pattern:

```python
WAIT_TIME_MS = 50         # Time between attempts (ms)
MAX_ATTEMPTS = 3           # Maximum attempts

def waitForElements(diagramHandle, elements):
    """Wait until all elements are available in the diagram."""
    elementGraphics = {}
    attempt = 0
    totalElements = len(elements)
    
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        
        for elem in elements:
            name = elem.getName()
            if name not in elementGraphics:
                dg = getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
        
        foundCount = len(elementGraphics)
        
        if foundCount == totalElements:
            print "  [Attempt " + str(attempt) + "] All " + str(foundCount) + " elements ready"
            return elementGraphics, attempt
        else:
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT"
    return elementGraphics, attempt
```

### Manual Unmask Fallback (CRITICAL):

If some elements are not auto-unmasked, you must unmask them **at a Y position inside their lane**. Unmasking at (0,0) will fail!

```python
def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """
    Manually unmask elements that were not auto-unmasked.
    CRITICAL: Must unmask at Y position INSIDE the correct lane!
    """
    unmaskedCount = 0
    
    # First, get each lane's center Y position
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
    
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            # Get the lane for this element
            laneName = elementLayout.get(name, (0, "Employee"))[1]
            targetY = laneY.get(laneName, 100)
            
            # Unmask at position INSIDE the lane
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name + ": ERROR - " + str(e)
    
    return unmaskedCount
```

---

## When User Asks for a BPMN Diagram

1. **Understand the process**: Ask clarifying questions if needed about lanes, tasks, decisions, etc.
2. **Use the template structure**: Copy helper functions and createBPMNDiagram() function
3. **Always include debug logging** - never skip this
4. **Apply the key rules below**

---

## Available Element Types

| Function | Icon | Use |
|----------|------|-----|
| `createStartEvent` | Green circle | Process start |
| `createMessageStartEvent` | Envelope green circle | Start triggered by message |
| `createTimerStartEvent` | Clock green circle | Start triggered by schedule |
| `createEndEvent` | Red circle | Process end |
| `createMessageEndEvent` | Envelope red circle | End that sends message |
| `createUserTask` | Person rectangle | Human activity with IT |
| `createManualTask` | Hand rectangle | Physical task without IT |
| `createServiceTask` | Gear rectangle | Automated task |
| `createExclusiveGateway` | Diamond with X | XOR decision (one path) |
| `createParallelGateway` | Diamond with + | AND split/join (all paths) |

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

### 2. ASCII Only - No Unicode Characters
```python
# CORRECT
print "=================================================================="
print "+-- STATE: BEFORE ------------------------------------------"

# WRONG - Will cause UnicodeDecodeError
print "======="
print "| PHASE 1 |"
```

### 3. Always Use addToLane()
Every element MUST be assigned to a lane:
```python
task = createUserTask(process, "Review Document")
addToLane(task, managerLane)  # REQUIRED!
```

### 4. Lane Names Must Match Exactly
Case-sensitive matching between createLane(), addToLane(), and elementLayout:
```python
managerLane = createLane(laneSet, "Manager")  # Creates "Manager"
addToLane(task, managerLane)                   # Assigns to Manager
elementLayout = {
    "Review": (1, "Manager"),  # Must match exactly!
}
```

### 5. Element Layout Dictionary
```python
elementLayout = {
    "Element Name": (column_index, "Lane Name"),
    # column_index: 0, 1, 2, ... (horizontal position)
}
```

### 6. Sequence Flows with Guards (Condition Labels)

**IMPORTANT**: Labels on flows from gateways must be set as **Guards**, not names!

```python
# Regular flow (no condition needed)
flows.append(createSequenceFlow(process, task1, task2))

# Flow FROM GATEWAY - use guard parameter for condition labels
# The guard text will appear on the arrow in the diagram
flows.append(createSequenceFlow(process, gateway, task, guard="Yes"))
flows.append(createSequenceFlow(process, gateway, otherTask, guard="No"))

# Alternative using convenience function
flows.append(createSequenceFlowWithGuard(process, gateway, task, "Yes"))
```

**Why Guards?**
- In Modelio BPMN, the "Guard" property on a sequence flow displays the condition text
- Setting just the "name" property does NOT show the label on gateway outflows
- Use `flow.setConditionExpression(guard)` internally

**Common Guard Values**:
- `"Yes"` / `"No"`
- `"Approved"` / `"Rejected"`
- `"Complete"` / `"Incomplete"`
- `"Success"` / `"Failure"`
- Any condition text you need

---

## Recommended Workflow

```
1. Create Process & Lanes
   - createBpmnProcess()
   - createBpmnLaneSet()
   - createLane() for each lane

2. Create Elements & Assign to Lanes
   - createXXX() for each element
   - addToLane() for each element

3. Create Diagram (triggers auto-unmask)
   - createBpmnProcessDesignDiagram()
   - getDiagramHandle()
   - save()

4. Wait for Elements
   - waitForElements() - poll until all graphics available
   - Log wait time and found/missing counts

5. Manual Unmask Fallback (if needed)
   - If some elements missing after wait timeout
   - Call unmaskMissingElements() with lane Y positions
   - CRITICAL: Unmask at Y position INSIDE the correct lane

6. Reposition Elements
   - Read lane Y positions
   - Calculate target X,Y for each element
   - setBounds() + save() for each

7. Create Flows
   - createSequenceFlow() for each connection
   - Final save()
```

---

## Complete Template Structure

```python
#
# MyProcess.py
#
# Description: [Your description]
# Applicable on: Package
# Version: X.X
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.gateways import BpmnParallelGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package
from org.eclipse.draw2d.geometry import Rectangle as Draw2DRectangle
import re
import time

# ============================================================================
# CONFIGURATION
# ============================================================================
SCRIPT_VERSION = "vX.X"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration
WAIT_TIME_MS = 50         # Time between attempts (ms)
MAX_ATTEMPTS = 3           # Maximum attempts

# Layout configuration  
SPACING = 120
START_X = 80

# ============================================================================
# HELPER FUNCTIONS (copy from template)
# ============================================================================
# ... createLane, addToLane, createXXX, etc. ...

# ============================================================================
# DIAGRAM UTILITIES (copy from template)
# ============================================================================
# ... parseBounds, getGraphics, getBounds, etc. ...

# ============================================================================
# WAIT FOR AUTO-UNMASK
# ============================================================================
def waitForElements(diagramHandle, elements):
    # ... implementation ...

# ============================================================================
# MAIN PROCESS
# ============================================================================
def createMyProcess(parentPackage):
    # Phase 1: Create process & lanes
    # Phase 2: Create elements & add to lanes
    # Phase 3: Create diagram (triggers auto-unmask)
    # Phase 4: Wait for elements
    # Phase 5: Reposition elements
    # Phase 6: Create flows
    pass

# ============================================================================
# ENTRY POINT
# ============================================================================
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createMyProcess(element)
    else:
        print "ERROR: Select a Package."
else:
    print "ERROR: Select a Package first."
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| UnicodeDecodeError | Use ASCII only - no special characters |
| Element in wrong lane | Check addToLane() call and lane name spelling |
| Element not visible | Wait for auto-unmask, then manual unmask fallback |
| Manual unmask fails | Must unmask at Y position INSIDE the correct lane |
| Layout mismatch | Check elementLayout lane names match exactly |
| Elements overlap | Increase spacing or adjust column indices |
| Lane expansion | Known Modelio behavior - check debug log |
| Elements not ready | Increase MAX_ATTEMPTS or WAIT_TIME_MS |
| Only first lane unmasked | Use unmaskMissingElements() with lane Y positions |

---

## Debug Log Format

A well-structured debug log should show:

```
==================================================================
BPMN DIAGRAM CREATION - DEBUG LOG
==================================================================
Script Version: v8.3
Execution ID:   12345
Process Name:   MyProcess_12345
==================================================================

== PHASE 1: CREATE PROCESS & LANES ==============================

[1] Process: MyProcess_12345
[2] Lanes: Lane1, Lane2, Lane3

== PHASE 2: CREATE ELEMENTS =====================================

[3] Lane1: 3 elements
[4] Lane2: 2 elements
[5] Lane3: 4 elements

  Total elements: 9

== PHASE 3: CREATE DIAGRAM ======================================

[6] Diagram created: MyProcess_12345
[7] DiagramHandle obtained
[8] Save (triggers auto-unmask)

== PHASE 4: WAIT FOR AUTO-UNMASK ================================

[9] Waiting for elements (max 10 attempts, 1000ms interval)...

  [Attempt 1] Found: 3/9 | Missing: Task2, Task3, ...
  [Attempt 2] Found: 3/9 | Missing: Task2, Task3, ...
  [Attempt 10] TIMEOUT - 3/9 elements

[10] WARNING: 3/9 elements ready after 10000ms
         Missing: Task2, Task3, Task4, Task5, Task6, End

[11] Trying manual unmask for missing elements...

  [Unmask] Task2 -> Y=161 (Lane2): OK
  [Unmask] Task3 -> Y=161 (Lane2): OK
  [Unmask] Task4 -> Y=261 (Lane3): OK
  [Unmask] Task5 -> Y=261 (Lane3): OK
  [Unmask] Task6 -> Y=261 (Lane3): OK
  [Unmask] End -> Y=261 (Lane3): OK

[12] Manual unmask: 6 elements unmasked
[13] All elements now available

  Lanes: Lane1(5-111); Lane2(111-211); Lane3(211-311)
  Elements: Start=Y35, Task1=Y35, Task2=Y161, ...

== PHASE 5: REPOSITION ELEMENTS =================================

[14] Lane1 centerY = 35
[15] Lane2 centerY = 149
[16] Lane3 centerY = 261

[17] Lane1/Start -> (80,35)
[18] Lane1/Task1 -> (200,35)
[19] Lane2/Task2 -> (320,149)
...

  Repositioned: 9/9

== PHASE 6: CREATE FLOWS ========================================

[20] Created 8 sequence flows
[21] Save

== FINAL STATE ==================================================

  Lanes: Lane1(5-111); Lane2(111-211); Lane3(211-311)
  Elements: Start=Y35, Task1=Y35, Task2=Y149, ...

[22] Diagram closed

==================================================================
COMPLETE
==================================================================
Process:  MyProcess_12345
Lanes:    3
Elements: 9 (9 in diagram)
Flows:    8
==================================================================
```

---

## Known Modelio Behaviors

### Lane Auto-Expansion

**Symptom**: After repositioning elements, the first lane may expand unexpectedly.

**Example**:
```
BEFORE: Lane1(5-166); Lane2(166-266)
AFTER:  Lane1(5-350); Lane2(350-450)
```

**Behavior**: This is non-deterministic - same script may produce different results.

**Mitigation**: 
- Read lane Y positions ONCE before repositioning
- Use fixed Y values for all elements in same lane
- Log changes with `*** LANE CHANGED ***` markers

### Auto-Unmask Timing

**Symptom**: Elements not available immediately after diagram creation.

**Cause**: Modelio needs time to process and unmask elements.

**Solution**: Use `waitForElements()` with polling.

### Partial Auto-Unmask

**Symptom**: Only some elements are auto-unmasked (e.g., first lane only).

**Cause**: Unknown - may be related to lane visibility or timing.

**Solution**: Use `unmaskMissingElements()` as fallback. **CRITICAL**: Must unmask at Y position inside the correct lane!

```python
# WRONG - will fail
result = diagramHandle.unmask(elem, 0, 0)

# CORRECT - unmask inside the lane
targetY = laneY[laneName]  # e.g., 161 for Manager lane
result = diagramHandle.unmask(elem, 100, targetY)
```

---

## Version History

- v9 (Dec 2025): Manual unmask inside correct lane Y position
- v8.2 (Dec 2025): Manual unmask fallback (failed - wrong Y)
- v8.1 (Dec 2025): Detailed attempt logging
- v8.0 (Dec 2025): Auto-unmask discovery, waiting mechanism
- v7.0 (Dec 2025): Detailed reposition logging
- v6.0 (Dec 2025): Lane change detection
- v5.0 (Dec 2025): Fixed lane Y values
- Earlier versions: Various experiments
