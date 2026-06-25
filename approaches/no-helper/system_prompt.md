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
## Complete Example of what the output can look like when executing the ExpenseApprovalProcess script in Modelio.
from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package
from org.eclipse.draw2d.geometry import Rectangle as Draw2DRectangle
import re
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_VERSION = "v9.1"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50         # Time to wait between attempts (milliseconds)
MAX_ATTEMPTS = 3           # Maximum number of attempts (total max wait = 50ms * 3 = 150ms)

# Layout configuration
SPACING = 150               # Horizontal spacing between columns (increased for wider tasks)
START_X = 80                # Starting X position

# Task dimensions (to ensure text fits)
TASK_WIDTH = 120            # Width for all tasks
TASK_HEIGHT = 60            # Height for all tasks


# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    """Create a BPMN Lane (swim lane) in the given lane set."""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def addToLane(element, lane):
    """
    Assign an element to a lane.
    IMPORTANT: This is required for proper positioning in the diagram.
    """
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False


def createStartEvent(process, name):
    """Create a BPMN Start Event (green circle)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createEndEvent(process, name):
    """Create a BPMN End Event (red circle)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createMessageEndEvent(process, name):
    """Create a BPMN Message End Event (envelope icon - sends message)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon - automated task)."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (X diamond - XOR decision)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createSequenceFlow(process, source, target, name="", guard=""):
    """
    Create a BPMN Sequence Flow (arrow between elements).
    
    Parameters:
    - process: The BPMN process container
    - source: Source element (task, gateway, event)
    - target: Target element (task, gateway, event)
    - name: Optional name for the flow (rarely used)
    - guard: Condition expression displayed on flows from gateways
             (e.g., "Yes", "No", "Approved", "Rejected")
    """
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    
    # Set guard condition for gateway outflows
    if guard:
        flow.setConditionExpression(guard)
    
    return flow


# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def parseBounds(boundsStr):
    """
    Parse a Rectangle bounds string into a dictionary.
    Example input: "Rectangle(100.0, 50.0, 80.0, 45.0)"
    Returns: {"x": 100.0, "y": 50.0, "w": 80.0, "h": 45.0} or None
    """
    match = re.search(
        r'Rectangle\((-?[0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+)\)',
        boundsStr
    )
    if match:
        return {
            "x": float(match.group(1)),
            "y": float(match.group(2)),
            "w": float(match.group(3)),
            "h": float(match.group(4))
        }
    return None


def getGraphics(diagramHandle, element):
    """
    Get the diagram graphics for an element.
    Returns the first graphic object, or None if not available.
    """
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def getBounds(diagramHandle, element):
    """
    Get the bounds (x, y, width, height) of an element in the diagram.
    Returns a dictionary or None if not available.
    """
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None


def getLaneCenterY(diagramHandle, lane):
    """
    Calculate the center Y position for placing elements in a lane.
    Returns the Y coordinate where elements should be placed, or None.
    """
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        # Center vertically, with slight offset for element height
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format a compact summary of all lanes with their Y ranges."""
    parts = []
    for laneName in laneOrder:
        lane = lanes[laneName]
        info = getBounds(diagramHandle, lane)
        if info:
            yEnd = int(info["y"] + info["h"])
            parts.append(laneName + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
        else:
            parts.append(laneName + "(--)")
    return "Lanes: " + "; ".join(parts)


def formatElementsSummary(diagramHandle, elements, elementLayout):
    """Format a compact summary of element Y positions."""
    parts = []
    sortedElems = []
    for elem in elements:
        name = elem.getName()
        col = elementLayout.get(name, (99, "?"))[0]
        sortedElems.append((col, name, elem))
    sortedElems.sort()
    
    for col, name, elem in sortedElems:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            # Truncate name to 10 chars for readability
            shortName = name[:10]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:10] + "=--")
    return "Elements: " + ", ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
    """
    Wait until all elements are available in the diagram.
    
    Modelio automatically unmasks elements when a diagram is created,
    but there may be a delay. This function polls until all elements
    have valid graphics objects.
    
    Logs each attempt with found/missing counts.
    
    Returns:
        dict: {elementName: graphicsObject} for all found elements
        int: number of attempts needed
    """
    elementGraphics = {}
    attempt = 0
    totalElements = len(elements)
    
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        
        # Check each element
        for elem in elements:
            name = elem.getName()
            if name not in elementGraphics:
                dg = getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
        
        foundCount = len(elementGraphics)
        
        # Log this attempt
        if foundCount == totalElements:
            print "  [Attempt " + str(attempt) + "] All " + str(foundCount) + " elements ready"
            return elementGraphics, attempt
        else:
            # List missing elements
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)
        
        # Wait before next check
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    # Timeout - return what we have
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """
    Try to manually unmask elements that were not auto-unmasked.
    Elements must be unmasked at a Y position inside their lane.
    
    Args:
        diagramHandle: The diagram handle
        elements: List of all elements
        elementGraphics: Dict of already found {name: graphics}
        lanes: Dict of {laneName: lane object}
        elementLayout: Dict of {elementName: (column, laneName)}
    
    Returns:
        int: Number of newly unmasked elements
    """
    unmaskedCount = 0
    
    # First, get each lane's center Y position
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            # Calculate center Y of the lane
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
    
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            # Get the lane for this element
            laneName = elementLayout.get(name, (0, "Employee"))[1]
            targetY = laneY.get(laneName, 100)
            
            # Try to unmask at position inside the lane
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


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createExpenseApprovalProcess(parentPackage):
    """
    Create the Expense Approval BPMN process with diagram.
    
    This function:
    1. Creates the process, lanes, and all BPMN elements
    2. Creates the diagram (which triggers auto-unmask)
    3. Waits for elements to be available
    4. Repositions elements according to the layout
    5. Creates sequence flows between elements
    """
    
    processName = "ExpenseApproval_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        """Get next step number for logging."""
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN EXPENSE APPROVAL PROCESS"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="
    
    # =========================================================================
    # PHASE 1: CREATE PROCESS & LANES
    # =========================================================================
    print ""
    print "== PHASE 1: CREATE PROCESS & LANES =============================="
    print ""
    
    # Create process
    process = modelingSession.getModel().createBpmnProcess()
    process.setName(processName)
    process.setOwner(parentPackage)
    print "[" + str(step()) + "] Process: " + processName
    
    # Create lane set
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    
    # Create lanes (order matters for vertical positioning)
    employeeLane = createLane(laneSet, "Employee")
    managerLane = createLane(laneSet, "Manager")
    financeLane = createLane(laneSet, "Finance")
    
    lanes = {
        "Employee": employeeLane,
        "Manager": managerLane,
        "Finance": financeLane
    }
    laneOrder = ["Employee", "Manager", "Finance"]
    
    print "[" + str(step()) + "] Lanes: Employee, Manager, Finance"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    
    def addElement(creator, name, lane, laneName):
        """Helper to create element, add to lane, and register."""
        elem = creator(process, name)
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Employee Lane (7 elements) ---
    addElement(createStartEvent, "Expense Incurred", employeeLane, "Employee")
    addElement(createUserTask, "Create Expense Report", employeeLane, "Employee")
    addElement(createUserTask, "Attach Receipts", employeeLane, "Employee")
    addElement(createUserTask, "Submit Report", employeeLane, "Employee")
    addElement(createUserTask, "Revise Report", employeeLane, "Employee")
    addElement(createUserTask, "Provide Additional Info", employeeLane, "Employee")
    addElement(createEndEvent, "Expense Rejected", employeeLane, "Employee")
    print "[" + str(step()) + "] Employee lane: 7 elements"
    
    # --- Manager Lane (5 elements) ---
    addElement(createUserTask, "Review Expense", managerLane, "Manager")
    addElement(createServiceTask, "Check Policy Compliance", managerLane, "Manager")
    addElement(createExclusiveGateway, "Approved?", managerLane, "Manager")
    addElement(createUserTask, "Request Revision", managerLane, "Manager")
    addElement(createUserTask, "Approve Expense", managerLane, "Manager")
    print "[" + str(step()) + "] Manager lane: 5 elements"
    
    # --- Finance Lane (7 elements) ---
    addElement(createServiceTask, "Receive Approved Expense", financeLane, "Finance")
    addElement(createServiceTask, "Validate Expense Details", financeLane, "Finance")
    addElement(createExclusiveGateway, "Details Complete?", financeLane, "Finance")
    addElement(createUserTask, "Request More Info", financeLane, "Finance")
    addElement(createServiceTask, "Process Payment", financeLane, "Finance")
    addElement(createServiceTask, "Send Payment Notification", financeLane, "Finance")
    addElement(createMessageEndEvent, "Expense Paid", financeLane, "Finance")
    print "[" + str(step()) + "] Finance lane: 7 elements"
    
    print ""
    print "  Total elements: " + str(len(elements))
    
    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""
    
    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(processName)
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: " + processName
    
    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    print "[" + str(step()) + "] DiagramHandle obtained"
    
    # Initial save to trigger auto-unmask
    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"
    
    # =========================================================================
    # PHASE 4: WAIT FOR ELEMENTS TO BE AVAILABLE
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""
    
    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Employee Lane
        "Expense Incurred": (0, "Employee"),
        "Create Expense Report": (1, "Employee"),
        "Attach Receipts": (2, "Employee"),
        "Submit Report": (3, "Employee"),
        "Expense Rejected": (5, "Employee"),
        "Revise Report": (6, "Employee"),
        "Provide Additional Info": (7, "Employee"),
        # Manager Lane
        "Review Expense": (4, "Manager"),
        "Check Policy Compliance": (5, "Manager"),
        "Approved?": (6, "Manager"),
        "Request Revision": (7, "Manager"),
        "Approve Expense": (8, "Manager"),
        # Finance Lane
        "Receive Approved Expense": (9, "Finance"),
        "Validate Expense Details": (10, "Finance"),
        "Details Complete?": (11, "Finance"),
        "Request More Info": (12, "Finance"),
        "Process Payment": (13, "Finance"),
        "Send Payment Notification": (14, "Finance"),
        "Expense Paid": (15, "Finance"),
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    
    if foundCount == len(elements):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)
        
        # Try manual unmask for missing elements
        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing elements..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"
        
        # Update count
        foundCount = len(elementGraphics)
        if foundCount == len(elements):
            print "[" + str(step()) + "] All elements now available"
        else:
            stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
            print "[" + str(step()) + "] Still missing: " + ", ".join(stillMissing)
    
    # Show initial state
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)
    
    # =========================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""
    
    # Read lane Y values (use fixed values to avoid drift)
    laneY = {}
    for laneName in laneOrder:
        lane = lanes[laneName]
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"
    
    print ""
    
    # Sort elements by column for left-to-right processing
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    for col, name, laneName in sortedElements:
        # Skip if element not available
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue
        
        # Calculate target position
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)
        
        # Determine width and height
        # Use TASK_WIDTH/TASK_HEIGHT for tasks, keep original for events/gateways
        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]
        
        # Set new bounds
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
        
        # Save after each reposition
        diagramHandle.save()
        
        # Check if lanes changed (Modelio behavior debugging)
        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""
        
        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes
        
        previousLanes = currentLanes
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    # Flow definitions: (source, target, guard)
    # Guard is the condition label shown on flows from gateways (e.g., "Yes", "No")
    # Leave guard empty ("") for regular flows
    flowDefs = [
        # Employee initial flow
        ("Expense Incurred", "Create Expense Report", ""),
        ("Create Expense Report", "Attach Receipts", ""),
        ("Attach Receipts", "Submit Report", ""),
        # To Manager
        ("Submit Report", "Review Expense", ""),
        # Manager review
        ("Review Expense", "Check Policy Compliance", ""),
        ("Check Policy Compliance", "Approved?", ""),
        # Manager decision - THESE NEED GUARDS (from gateway)
        ("Approved?", "Request Revision", "Needs Revision"),
        ("Approved?", "Expense Rejected", "Rejected"),
        ("Approved?", "Approve Expense", "Approved"),
        # Revision loop
        ("Request Revision", "Revise Report", ""),
        ("Revise Report", "Submit Report", ""),
        # To Finance
        ("Approve Expense", "Receive Approved Expense", ""),
        # Finance processing
        ("Receive Approved Expense", "Validate Expense Details", ""),
        ("Validate Expense Details", "Details Complete?", ""),
        # Finance decision - THESE NEED GUARDS (from gateway)
        ("Details Complete?", "Request More Info", "No"),
        ("Details Complete?", "Process Payment", "Yes"),
        # Info loop
        ("Request More Info", "Provide Additional Info", ""),
        ("Provide Additional Info", "Validate Expense Details", ""),
        # Payment
        ("Process Payment", "Send Payment Notification", ""),
        ("Send Payment Notification", "Expense Paid", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            # Pass guard as keyword argument
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName
    
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    
    # Final save
    diagramHandle.save()
    print "[" + str(step()) + "] Save"
    
    # =========================================================================
    # FINAL STATE
    # =========================================================================
    print ""
    print "== FINAL STATE =================================================="
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)
    
    # Close diagram handle
    diagramHandle.close()
    print ""
    print "[" + str(step()) + "] Diagram closed"
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print ""
    print "=================================================================="
    print "COMPLETE"
    print "=================================================================="
    print "Process:  " + processName
    print "Lanes:    " + str(len(lanes))
    print "Elements: " + str(len(elements)) + " (" + str(foundCount) + " in diagram)"
    print "Flows:    " + str(len(flows))
    print "=================================================================="
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createExpenseApprovalProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."

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
