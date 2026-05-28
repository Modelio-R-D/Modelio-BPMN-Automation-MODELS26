#
# EvanstonianRoomService.py
#
# Description:
#   BPMN process diagram for The Evanstonian Hotel Room Service workflow.
#   4 lanes: Guest, Room Service Manager, Kitchen/Sommelier, Waiter
#
# Process Flow:
#   1. Guest calls room service
#   2. Manager takes order and distributes tasks
#   3. Kitchen prepares food, Sommelier fetches wine (80% of orders)
#   4. Waiter readies cart and prepares non-alcoholic drinks (parallel)
#   5. Waiter delivers to room when all ready
#   6. Waiter debits account (may defer if busy)
#
# Applicable on: Package
#
# Version: 1.0 - December 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
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

SCRIPT_VERSION = "v1.0"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 5

# Layout configuration
SPACING = 140
START_X = 60

# Task dimensions
TASK_WIDTH = 110
TASK_HEIGHT = 55


# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    """Create a BPMN Lane in the given lane set."""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def addToLane(element, lane):
    """Assign an element to a lane."""
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


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon - physical task without IT)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (X diamond - XOR decision)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (+ diamond - AND split/join)."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createSequenceFlow(process, source, target, name="", guard=""):
    """Create a BPMN Sequence Flow with optional guard condition."""
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    if guard:
        flow.setConditionExpression(guard)
    return flow


# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def parseBounds(boundsStr):
    """Parse a Rectangle bounds string into a dictionary."""
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
    """Get the diagram graphics for an element."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def getBounds(diagramHandle, element):
    """Get the bounds of an element in the diagram."""
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None


def getLaneCenterY(diagramHandle, lane):
    """Calculate the center Y position for placing elements in a lane."""
    bounds = getBounds(diagramHandle, lane)
    if bounds:
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
            parts.append(laneName[:8] + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
        else:
            parts.append(laneName[:8] + "(--)")
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
            shortName = name[:8]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:8] + "=--")
    return "Elements: " + ", ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

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
            missing = [e.getName()[:10] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing[:5])
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """Manually unmask elements that were not auto-unmasked."""
    unmaskedCount = 0
    
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
    
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Guest"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:15] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createRoomServiceProcess(parentPackage):
    """Create The Evanstonian Room Service BPMN process with diagram."""
    
    processName = "RoomService_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "THE EVANSTONIAN - ROOM SERVICE PROCESS"
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
    
    process = modelingSession.getModel().createBpmnProcess()
    process.setName(processName)
    process.setOwner(parentPackage)
    print "[" + str(step()) + "] Process: " + processName
    
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    
    # Create lanes (order = vertical position)
    guestLane = createLane(laneSet, "Guest")
    managerLane = createLane(laneSet, "RS Manager")
    kitchenLane = createLane(laneSet, "Kitchen/Sommelier")
    waiterLane = createLane(laneSet, "Waiter")
    
    lanes = {
        "Guest": guestLane,
        "RS Manager": managerLane,
        "Kitchen/Sommelier": kitchenLane,
        "Waiter": waiterLane
    }
    laneOrder = ["Guest", "RS Manager", "Kitchen/Sommelier", "Waiter"]
    
    print "[" + str(step()) + "] Lanes: Guest, RS Manager, Kitchen/Sommelier, Waiter"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    
    def addElement(creator, name, lane):
        elem = creator(process, name)
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Guest Lane (2 elements) ---
    addElement(createStartEvent, "Call Room Service", guestLane)
    addElement(createEndEvent, "Order Received", guestLane)
    print "[" + str(step()) + "] Guest lane: 2 elements"
    
    # --- RS Manager Lane (4 elements) ---
    addElement(createUserTask, "Take Order", managerLane)
    addElement(createManualTask, "Submit to Kitchen", managerLane)
    addElement(createManualTask, "Order Sommelier", managerLane)
    addElement(createManualTask, "Assign to Waiter", managerLane)
    print "[" + str(step()) + "] RS Manager lane: 4 elements"
    
    # --- Kitchen/Sommelier Lane (4 elements) ---
    addElement(createManualTask, "Prepare Food", kitchenLane)
    addElement(createExclusiveGateway, "Wine Ordered?", kitchenLane)
    addElement(createManualTask, "Fetch Wine", kitchenLane)
    addElement(createParallelGateway, "Wine Ready", kitchenLane)
    print "[" + str(step()) + "] Kitchen/Sommelier lane: 4 elements"
    
    # --- Waiter Lane (9 elements) ---
    addElement(createParallelGateway, "Start Waiter Tasks", waiterLane)
    addElement(createManualTask, "Ready Cart", waiterLane)
    addElement(createManualTask, "Prepare Non-Alc Drinks", waiterLane)
    addElement(createParallelGateway, "Cart Ready", waiterLane)
    addElement(createParallelGateway, "All Ready", waiterLane)
    addElement(createManualTask, "Deliver to Room", waiterLane)
    addElement(createExclusiveGateway, "Another Order?", waiterLane)
    addElement(createUserTask, "Debit Account", waiterLane)
    addElement(createEndEvent, "Order Complete", waiterLane)
    print "[" + str(step()) + "] Waiter lane: 9 elements"
    
    print ""
    print "  Total elements: " + str(len(elements))
    
    # =========================================================================
    # PHASE 3: CREATE DIAGRAM
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
    
    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"
    
    # =========================================================================
    # PHASE 4: WAIT FOR ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""
    
    # Layout: element name -> (column_index, lane_name)
    elementLayout = {
        # Guest Lane
        "Call Room Service": (0, "Guest"),
        "Order Received": (10, "Guest"),
        
        # RS Manager Lane
        "Take Order": (1, "RS Manager"),
        "Submit to Kitchen": (2, "RS Manager"),
        "Order Sommelier": (3, "RS Manager"),
        "Assign to Waiter": (4, "RS Manager"),
        
        # Kitchen/Sommelier Lane
        "Prepare Food": (3, "Kitchen/Sommelier"),
        "Wine Ordered?": (4, "Kitchen/Sommelier"),
        "Fetch Wine": (5, "Kitchen/Sommelier"),
        "Wine Ready": (6, "Kitchen/Sommelier"),
        
        # Waiter Lane
        "Start Waiter Tasks": (5, "Waiter"),
        "Ready Cart": (6, "Waiter"),
        "Prepare Non-Alc Drinks": (6, "Waiter"),  # Will offset vertically
        "Cart Ready": (7, "Waiter"),
        "All Ready": (8, "Waiter"),
        "Deliver to Room": (9, "Waiter"),
        "Another Order?": (10, "Waiter"),
        "Debit Account": (11, "Waiter"),
        "Order Complete": (12, "Waiter"),
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    
    if foundCount == len(elements):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready"
    else:
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " ready"
        
        print ""
        print "[" + str(step()) + "] Trying manual unmask..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements"
        
        foundCount = len(elementGraphics)
    
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    # =========================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""
    
    laneY = {}
    for laneName in laneOrder:
        lane = lanes[laneName]
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
    
    print ""
    
    # Sort elements by column
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    
    for col, name, laneName in sortedElements:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue
        
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)
        
        # Special case: offset "Prepare Non-Alc Drinks" lower to avoid overlap with "Ready Cart"
        if name == "Prepare Non-Alc Drinks":
            targetY = targetY + 60
        
        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]
        
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
        
        diagramHandle.save()
        
        print "[" + str(step()) + "] " + laneName[:8] + "/" + name[:15] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    # Flow definitions: (source, target, guard)
    flowDefs = [
        # Guest to Manager
        ("Call Room Service", "Take Order", ""),
        
        # Manager sequence
        ("Take Order", "Submit to Kitchen", ""),
        ("Submit to Kitchen", "Order Sommelier", ""),
        ("Order Sommelier", "Assign to Waiter", ""),
        
        # Kitchen: Submit to Kitchen triggers food prep
        ("Submit to Kitchen", "Prepare Food", ""),
        
        # Sommelier: Order Sommelier triggers wine check
        ("Order Sommelier", "Wine Ordered?", ""),
        ("Wine Ordered?", "Fetch Wine", "Yes (80%)"),
        ("Wine Ordered?", "Wine Ready", "No"),
        ("Fetch Wine", "Wine Ready", ""),
        
        # Waiter parallel start
        ("Assign to Waiter", "Start Waiter Tasks", ""),
        ("Start Waiter Tasks", "Ready Cart", ""),
        ("Start Waiter Tasks", "Prepare Non-Alc Drinks", ""),
        
        # Waiter cart ready (join)
        ("Ready Cart", "Cart Ready", ""),
        ("Prepare Non-Alc Drinks", "Cart Ready", ""),
        
        # All ready join (food + wine + cart)
        ("Prepare Food", "All Ready", ""),
        ("Wine Ready", "All Ready", ""),
        ("Cart Ready", "All Ready", ""),
        
        # Delivery
        ("All Ready", "Deliver to Room", ""),
        ("Deliver to Room", "Order Received", ""),
        ("Deliver to Room", "Another Order?", ""),
        
        # Billing decision
        ("Another Order?", "Start Waiter Tasks", "Yes (defer billing)"),
        ("Another Order?", "Debit Account", "No"),
        ("Debit Account", "Order Complete", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow"
    
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    
    diagramHandle.save()
    print "[" + str(step()) + "] Save"
    
    # =========================================================================
    # FINAL STATE
    # =========================================================================
    print ""
    print "== FINAL STATE =================================================="
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    
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
        createRoomServiceProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
