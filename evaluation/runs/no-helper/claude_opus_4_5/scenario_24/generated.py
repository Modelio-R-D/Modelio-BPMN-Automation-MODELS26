#
# RestaurantOrderProcess.py
#
# Description:
#   BPMN process diagram for Restaurant Order workflow.
#   3 lanes: Guest, Employee, Chef
#   Models the flow from guest entering hungry to receiving their meal.
#
# Applicable on: Package
#
# Version: 1.0 - Restaurant Order Process
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
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
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 130
START_X = 80

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


def createIntermediateCatchEvent(process, name, eventType="timer"):
    """Create a BPMN Intermediate Catch Event."""
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    if eventType == "timer":
        try:
            timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
            timerDef.setDefined(event)
        except:
            pass
    elif eventType == "signal":
        try:
            signalDef = modelingSession.getModel().createBpmnSignalEventDefinition()
            signalDef.setDefined(event)
        except:
            pass
    return event


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
    
    for col, name, elem in sortedElems[:8]:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:10]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:10] + "=--")
    if len(sortedElems) > 8:
        parts.append("...")
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
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing[:5])
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """Try to manually unmask elements that were not auto-unmasked."""
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
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:20] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createRestaurantOrderProcess(parentPackage):
    """Create the Restaurant Order BPMN process with diagram."""
    
    processName = "RestaurantOrder_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN RESTAURANT ORDER PROCESS"
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
    
    guestLane = createLane(laneSet, "Guest")
    employeeLane = createLane(laneSet, "Employee")
    chefLane = createLane(laneSet, "Chef")
    
    lanes = {
        "Guest": guestLane,
        "Employee": employeeLane,
        "Chef": chefLane
    }
    laneOrder = ["Guest", "Employee", "Chef"]
    
    print "[" + str(step()) + "] Lanes: Guest, Employee, Chef"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
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
    
    def addTimerEvent(name, lane, laneName):
        elem = createIntermediateCatchEvent(process, name, "timer")
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    def addSignalEvent(name, lane, laneName):
        elem = createIntermediateCatchEvent(process, name, "signal")
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Guest Lane (8 elements) ---
    addElement(createStartEvent, "Feeling Hungry", guestLane, "Guest")
    addElement(createManualTask, "Enter Restaurant", guestLane, "Guest")
    addElement(createManualTask, "Choose Dish", guestLane, "Guest")
    addElement(createManualTask, "Wait for Turn", guestLane, "Guest")
    addElement(createManualTask, "Place Order", guestLane, "Guest")
    addElement(createManualTask, "Receive Buzzer", guestLane, "Guest")
    addElement(createManualTask, "Wait for Buzzer", guestLane, "Guest")
    addElement(createManualTask, "Pick Up Meal", guestLane, "Guest")
    addElement(createManualTask, "Eat Meal", guestLane, "Guest")
    addElement(createEndEvent, "Meal Finished", guestLane, "Guest")
    print "[" + str(step()) + "] Guest lane: 10 elements"
    
    # --- Employee Lane (12 elements) ---
    addElement(createUserTask, "Take Order", employeeLane, "Employee")
    addElement(createServiceTask, "Enter Order POS", employeeLane, "Employee")
    addElement(createUserTask, "Collect Payment", employeeLane, "Employee")
    addElement(createManualTask, "Setup Buzzer", employeeLane, "Employee")
    addElement(createManualTask, "Give Buzzer", employeeLane, "Employee")
    addElement(createManualTask, "Inform Chef", employeeLane, "Employee")
    addElement(createManualTask, "Wait Meal Ready", employeeLane, "Employee")
    addElement(createServiceTask, "Trigger Buzzer", employeeLane, "Employee")
    addElement(createExclusiveGateway, "Guest Responds?", employeeLane, "Employee")
    addTimerEvent("Wait 5 min", employeeLane, "Employee")
    addElement(createManualTask, "Call Guest", employeeLane, "Employee")
    addElement(createManualTask, "Hand Over Meal", employeeLane, "Employee")
    print "[" + str(step()) + "] Employee lane: 12 elements"
    
    # --- Chef Lane (4 elements) ---
    addElement(createManualTask, "Receive Order", chefLane, "Chef")
    addElement(createManualTask, "Prepare Meal", chefLane, "Chef")
    addElement(createManualTask, "Place in Hatch", chefLane, "Chef")
    addElement(createManualTask, "Notify Employee", chefLane, "Chef")
    print "[" + str(step()) + "] Chef lane: 4 elements"
    
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
    
    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Guest Lane - main flow
        "Feeling Hungry": (0, "Guest"),
        "Enter Restaurant": (1, "Guest"),
        "Choose Dish": (2, "Guest"),
        "Wait for Turn": (3, "Guest"),
        "Place Order": (4, "Guest"),
        "Receive Buzzer": (7, "Guest"),
        "Wait for Buzzer": (8, "Guest"),
        "Pick Up Meal": (12, "Guest"),
        "Eat Meal": (13, "Guest"),
        "Meal Finished": (14, "Guest"),
        
        # Employee Lane
        "Take Order": (4, "Employee"),
        "Enter Order POS": (5, "Employee"),
        "Collect Payment": (6, "Employee"),
        "Setup Buzzer": (7, "Employee"),
        "Give Buzzer": (7, "Employee"),
        "Inform Chef": (8, "Employee"),
        "Wait Meal Ready": (9, "Employee"),
        "Trigger Buzzer": (10, "Employee"),
        "Guest Responds?": (11, "Employee"),
        "Wait 5 min": (12, "Employee"),
        "Call Guest": (13, "Employee"),
        "Hand Over Meal": (12, "Employee"),
        
        # Chef Lane
        "Receive Order": (8, "Chef"),
        "Prepare Meal": (9, "Chef"),
        "Place in Hatch": (10, "Chef"),
        "Notify Employee": (11, "Chef"),
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
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready"
        
        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing elements..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"
        
        foundCount = len(elementGraphics)
        if foundCount == len(elements):
            print "[" + str(step()) + "] All elements now available"
        else:
            stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
            print "[" + str(step()) + "] Still missing: " + ", ".join(stillMissing)
    
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)
    
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
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"
    
    print ""
    
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    
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
        
        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""
        
        print "[" + str(step()) + "] " + laneName + "/" + name[:18] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")" + laneChanged
        
        previousLanes = currentLanes
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Guest initial flow
        ("Feeling Hungry", "Enter Restaurant", ""),
        ("Enter Restaurant", "Choose Dish", ""),
        ("Choose Dish", "Wait for Turn", ""),
        ("Wait for Turn", "Place Order", ""),
        
        # Guest to Employee (order)
        ("Place Order", "Take Order", ""),
        
        # Employee order processing
        ("Take Order", "Enter Order POS", ""),
        ("Enter Order POS", "Collect Payment", ""),
        ("Collect Payment", "Setup Buzzer", ""),
        ("Setup Buzzer", "Give Buzzer", ""),
        
        # Buzzer to Guest
        ("Give Buzzer", "Receive Buzzer", ""),
        ("Receive Buzzer", "Wait for Buzzer", ""),
        
        # Employee informs Chef
        ("Give Buzzer", "Inform Chef", ""),
        ("Inform Chef", "Receive Order", ""),
        
        # Chef prepares meal
        ("Receive Order", "Prepare Meal", ""),
        ("Prepare Meal", "Place in Hatch", ""),
        ("Place in Hatch", "Notify Employee", ""),
        
        # Chef notifies Employee
        ("Notify Employee", "Wait Meal Ready", ""),
        ("Wait Meal Ready", "Trigger Buzzer", ""),
        
        # Buzzer triggers
        ("Trigger Buzzer", "Guest Responds?", ""),
        
        # Gateway decision - with guards
        ("Guest Responds?", "Hand Over Meal", "Yes"),
        ("Guest Responds?", "Wait 5 min", "No"),
        
        # Timer loop for calling guest
        ("Wait 5 min", "Call Guest", ""),
        ("Call Guest", "Guest Responds?", ""),
        
        # Guest picks up meal
        ("Wait for Buzzer", "Pick Up Meal", ""),
        ("Hand Over Meal", "Pick Up Meal", ""),
        ("Pick Up Meal", "Eat Meal", ""),
        ("Eat Meal", "Meal Finished", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName
    
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
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)
    
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
        createRestaurantOrderProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
