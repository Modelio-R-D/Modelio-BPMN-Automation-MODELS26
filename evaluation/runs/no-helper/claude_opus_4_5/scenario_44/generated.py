#
# RoboticBurgerSeller.py
#
# Description:
#   BPMN process diagram for a Robotic Burger Seller near the University of Vienna.
#   The robot handles orders for burgers, menus with drinks, and sides (fries/wedges).
#   Features parallel processing, timer events, and variable durations.
#
# Lanes:
#   - Customer: Order placement and receiving
#   - Robot: All preparation activities
#   - Conveyor System: Delivery
#
# Applicable on: Package
#
# Version: 1.0 - December 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.events import BpmnIntermediateCatchEvent
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


def createMessageStartEvent(process, name):
    """Create a BPMN Message Start Event (envelope - triggered by message)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


def createEndEvent(process, name):
    """Create a BPMN End Event (red circle)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createTimerIntermediateEvent(process, name):
    """Create a BPMN Timer Intermediate Catch Event (clock icon)."""
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        pass
    return event


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity)."""
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
    """Format a compact summary of all lanes."""
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
    
    for col, name, elem in sortedElems[:8]:  # Show first 8 only
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:8]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
    return "Elements: " + ", ".join(parts) + "..."


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
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT"
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
            laneName = elementLayout.get(name, (0, "Robot"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + ": OK"
            except Exception as e:
                print "  [Unmask] " + name[:15] + ": ERROR"
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createRoboticBurgerProcess(parentPackage):
    """Create the Robotic Burger Seller BPMN process."""
    
    processName = "RoboticBurger_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "ROBOTIC BURGER SELLER - UNIVERSITY OF VIENNA"
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
    
    customerLane = createLane(laneSet, "Customer")
    robotLane = createLane(laneSet, "Robot")
    conveyorLane = createLane(laneSet, "Conveyor")
    
    lanes = {
        "Customer": customerLane,
        "Robot": robotLane,
        "Conveyor": conveyorLane
    }
    laneOrder = ["Customer", "Robot", "Conveyor"]
    
    print "[" + str(step()) + "] Lanes: Customer, Robot, Conveyor"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    
    def addElement(creator, name, lane, laneName):
        elem = creator(process, name)
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Customer Lane ---
    addElement(createMessageStartEvent, "Order Received", customerLane, "Customer")
    addElement(createUserTask, "Place Order", customerLane, "Customer")
    addElement(createEndEvent, "Order Complete", customerLane, "Customer")
    print "[" + str(step()) + "] Customer lane: 3 elements"
    
    # --- Robot Lane ---
    addElement(createExclusiveGateway, "Menu or Burger?", robotLane, "Robot")
    addElement(createParallelGateway, "Start Menu Prep", robotLane, "Robot")
    addElement(createServiceTask, "Prepare Drink", robotLane, "Robot")
    addElement(createExclusiveGateway, "Fries or Wedges?", robotLane, "Robot")
    addElement(createServiceTask, "Prepare Fries", robotLane, "Robot")
    addElement(createServiceTask, "Prepare Wedges", robotLane, "Robot")
    addElement(createParallelGateway, "Sides Ready", robotLane, "Robot")
    addElement(createParallelGateway, "Menu Items Ready", robotLane, "Robot")
    addElement(createServiceTask, "Prepare Burger", robotLane, "Robot")
    addElement(createTimerIntermediateEvent, "30s Status Update", robotLane, "Robot")
    addElement(createServiceTask, "Announce Status", robotLane, "Robot")
    addElement(createServiceTask, "Assemble Order", robotLane, "Robot")
    print "[" + str(step()) + "] Robot lane: 12 elements"
    
    # --- Conveyor Lane ---
    addElement(createServiceTask, "Load Conveyor", conveyorLane, "Conveyor")
    addElement(createServiceTask, "Deliver Order", conveyorLane, "Conveyor")
    print "[" + str(step()) + "] Conveyor lane: 2 elements"
    
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
    print "[" + str(step()) + "] Diagram created"
    
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
    
    # Layout: element name -> (column, lane)
    elementLayout = {
        # Customer Lane
        "Order Received": (0, "Customer"),
        "Place Order": (1, "Customer"),
        "Order Complete": (14, "Customer"),
        # Robot Lane - Main flow
        "Menu or Burger?": (2, "Robot"),
        "Start Menu Prep": (3, "Robot"),
        "Prepare Drink": (4, "Robot"),
        "Fries or Wedges?": (5, "Robot"),
        "Prepare Fries": (6, "Robot"),
        "Prepare Wedges": (6, "Robot"),  # Same column, will offset Y
        "Sides Ready": (7, "Robot"),
        "Menu Items Ready": (8, "Robot"),
        "Prepare Burger": (9, "Robot"),
        "30s Status Update": (10, "Robot"),
        "Announce Status": (11, "Robot"),
        "Assemble Order": (12, "Robot"),
        # Conveyor Lane
        "Load Conveyor": (13, "Conveyor"),
        "Deliver Order": (14, "Conveyor"),
    }
    
    print "[" + str(step()) + "] Waiting for elements..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    foundCount = len(elementGraphics)
    
    if foundCount < len(elements):
        print ""
        print "[" + str(step()) + "] Trying manual unmask..."
        print ""
        unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
        foundCount = len(elementGraphics)
    
    print ""
    print "[" + str(step()) + "] Elements ready: " + str(foundCount) + "/" + str(len(elements))
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
    
    # Special Y offsets for parallel elements (Fries/Wedges)
    yOffsets = {
        "Prepare Fries": -35,
        "Prepare Wedges": 35,
    }
    
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    
    for col, name, laneName in sortedElements:
        if name not in elementGraphics:
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
            continue
        
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100) + yOffsets.get(name, 0)
        
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
        
        print "[" + str(step()) + "] " + name[:18] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Customer to Robot
        ("Order Received", "Place Order", ""),
        ("Place Order", "Menu or Burger?", ""),
        
        # Menu decision
        ("Menu or Burger?", "Start Menu Prep", "Menu"),
        ("Menu or Burger?", "Prepare Burger", "Just Burger"),
        
        # Parallel menu preparation
        ("Start Menu Prep", "Prepare Drink", ""),
        ("Start Menu Prep", "Fries or Wedges?", ""),
        
        # Sides decision
        ("Fries or Wedges?", "Prepare Fries", "Fries"),
        ("Fries or Wedges?", "Prepare Wedges", "Wedges"),
        
        # Sides join
        ("Prepare Fries", "Sides Ready", ""),
        ("Prepare Wedges", "Sides Ready", ""),
        
        # Menu items join
        ("Prepare Drink", "Menu Items Ready", ""),
        ("Sides Ready", "Menu Items Ready", ""),
        
        # After menu ready, prepare burger
        ("Menu Items Ready", "Prepare Burger", ""),
        
        # Burger preparation with status updates
        ("Prepare Burger", "30s Status Update", ""),
        ("30s Status Update", "Announce Status", ""),
        ("Announce Status", "Assemble Order", ""),
        
        # Final assembly and delivery
        ("Assemble Order", "Load Conveyor", ""),
        ("Load Conveyor", "Deliver Order", ""),
        ("Deliver Order", "Order Complete", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "  WARNING: Missing " + srcName + " or " + tgtName
    
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    
    diagramHandle.save()
    print "[" + str(step()) + "] Final save"
    
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
    print "COMPLETE - ROBOTIC BURGER SELLER"
    print "=================================================================="
    print "Process:  " + processName
    print "Lanes:    " + str(len(lanes)) + " (Customer, Robot, Conveyor)"
    print "Elements: " + str(len(elements))
    print "Flows:    " + str(len(flows))
    print ""
    print "Process Flow:"
    print "  1. Customer places order"
    print "  2. Robot asks: Menu or just burger?"
    print "  3. If Menu: Parallel prep of drink + sides"
    print "  4. Sides: Fries or Wedges (variable time by size)"
    print "  5. Burger prep with 30s status updates"
    print "  6. Conveyor belt delivery"
    print "=================================================================="
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createRoboticBurgerProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
