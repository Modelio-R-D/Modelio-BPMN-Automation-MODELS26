#
# ExpenseApprovalProcess.py
#
# Description:
#   BPMN process diagram for Expense Approval workflow.
#   3 lanes: Employee, Manager, Finance
#
# Key Insight (from Modelio developers):
#   - Modelio automatically unmasks elements when a diagram is created
#   - No need to call unmask() manually
#   - BUT: There may be a delay before elements are available
#   - Solution: Wait and check until all elements are ready
#
# Workflow:
#   1. Create process, lanes, and elements
#   2. Create diagram (triggers auto-unmask)
#   3. Wait for all elements to be available in diagram
#   4. Reposition elements to their target positions
#   5. Create sequence flows
#
# Applicable on: Package
#
# Version: 9.1 - December 2025 - Guards for gateway conditions
#

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
