#
# OnlinePurchaseProcess.py
#
# Description:
#   BPMN process for purchasing items from an online shop.
#
#   Flow (high level):
#     1) User logs in
#     2) Parallel: (a) Select items  (b) Set payment method
#     3) After selecting items: choose free reward (independent of payment)
#     4) After payment method: choose Pay now OR Installments
#     5) Join: reward chosen AND payment completed/agreed
#     6) Deliver items
#     7) Optional exchange loop: each return triggers a new delivery
#
# Applicable on: Package
# Version: 9.1
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
SCRIPT_VERSION = "v9.1"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 5

# Layout configuration
SPACING = 170
START_X = 80

# Task dimensions
TASK_WIDTH = 150
TASK_HEIGHT = 60

# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane

def addToLane(element, lane):
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False

def createStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createUserTask(process, name):
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createManualTask(process, name):
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createServiceTask(process, name):
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createExclusiveGateway(process, name):
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createParallelGateway(process, name):
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createSequenceFlow(process, source, target, name="", guard=""):
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    if guard:
        flow.setConditionExpression(guard)
    return flow

def createSequenceFlowWithGuard(process, source, target, guardText):
    return createSequenceFlow(process, source, target, guard=guardText)

# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def parseBounds(boundsStr):
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
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None

def getBounds(diagramHandle, element):
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None

def getLaneCenterY(diagramHandle, lane):
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None

def formatLanesSummary(diagramHandle, lanes, laneOrder):
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
            parts.append(name[:12] + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:12] + "=--")
    return "Elements: " + ", ".join(parts)

# ============================================================================
# WAIT FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
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

    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt

def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
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
            laneName = elementLayout.get(name, (0, "Customer"))[1]
            targetY = laneY.get(laneName, 100)

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

def createOnlinePurchaseProcess(parentPackage):
    processName = "OnlinePurchase_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN ONLINE PURCHASE PROCESS - DEBUG LOG"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="

    # =======================================================================
    # PHASE 1: CREATE PROCESS & LANES
    # =======================================================================
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
    shopLane = createLane(laneSet, "Shop System")
    logisticsLane = createLane(laneSet, "Logistics")

    lanes = {
        "Customer": customerLane,
        "Shop System": shopLane,
        "Logistics": logisticsLane
    }
    laneOrder = ["Customer", "Shop System", "Logistics"]
    print "[" + str(step()) + "] Lanes: Customer, Shop System, Logistics"

    # =======================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =======================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""

    elements = []
    elementRefs = {}

    def addElement(creator, name, laneName):
        lane = lanes[laneName]
        elem = creator(process, name)
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        if ok:
            print "  [Element] " + laneName + ": " + name
        else:
            print "  [Element] WARNING: addToLane FAILED for " + laneName + ": " + name
        return elem

    # Start / Login
    addElement(createStartEvent, "Start", "Customer")
    addElement(createUserTask, "Log in", "Customer")

    # Parallel split/join for (Reward branch) and (Payment branch)
    addElement(createParallelGateway, "Parallel Split", "Customer")

    # Item selection branch (reward depends on it)
    addElement(createUserTask, "Select items", "Customer")
    addElement(createExclusiveGateway, "Reward option?", "Customer")
    addElement(createUserTask, "Select Reward A", "Customer")
    addElement(createUserTask, "Select Reward B", "Customer")
    addElement(createUserTask, "Select Reward C", "Customer")
    addElement(createExclusiveGateway, "Reward chosen", "Customer")

    # Payment branch (depends on payment method task)
    addElement(createUserTask, "Set payment method", "Customer")
    addElement(createExclusiveGateway, "Payment type?", "Customer")
    addElement(createUserTask, "Pay now", "Customer")
    addElement(createUserTask, "Installment agreement", "Customer")
    addElement(createExclusiveGateway, "Payment done", "Customer")

    addElement(createParallelGateway, "Parallel Join", "Customer")

    # Delivery + exchange loop
    addElement(createServiceTask, "Deliver items", "Logistics")
    addElement(createExclusiveGateway, "Return for exchange?", "Customer")
    addElement(createManualTask, "Return items", "Customer")
    addElement(createServiceTask, "Process exchange", "Shop System")
    addElement(createServiceTask, "Deliver replacement", "Logistics")
    addElement(createEndEvent, "End", "Customer")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # =======================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =======================================================================
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

    # =======================================================================
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # =======================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout: name -> (column, laneName)
    elementLayout = {
        "Start": (0, "Customer"),
        "Log in": (1, "Customer"),

        "Parallel Split": (2, "Customer"),

        "Select items": (3, "Customer"),
        "Reward option?": (4, "Customer"),
        "Select Reward A": (5, "Customer"),
        "Select Reward B": (5, "Customer"),
        "Select Reward C": (5, "Customer"),
        "Reward chosen": (6, "Customer"),

        "Set payment method": (3, "Customer"),
        "Payment type?": (4, "Customer"),
        "Pay now": (5, "Customer"),
        "Installment agreement": (5, "Customer"),
        "Payment done": (6, "Customer"),

        "Parallel Join": (7, "Customer"),

        "Deliver items": (8, "Logistics"),
        "Return for exchange?": (9, "Customer"),
        "Return items": (10, "Customer"),
        "Process exchange": (11, "Shop System"),
        "Deliver replacement": (12, "Logistics"),
        "End": (13, "Customer")
    }

    # Wait also for lanes (helps for lane bounds and manual unmask fallback)
    waitObjects = []
    for ln in laneOrder:
        waitObjects.append(lanes[ln])
    for e in elements:
        waitObjects.append(e)

    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    graphicsByName, attempts = waitForElements(diagramHandle, waitObjects)
    totalWaitTime = attempts * WAIT_TIME_MS

    # Build elementGraphics map only for BPMN elements (not lanes)
    elementGraphics = {}
    for e in elements:
        n = e.getName()
        if n in graphicsByName:
            elementGraphics[n] = graphicsByName[n]

    foundCount = len(elementGraphics)

    if foundCount == len(elements):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)

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

    # =======================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =======================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""

    laneY = {}
    for laneName in laneOrder:
        y = getLaneCenterY(diagramHandle, lanes[laneName])
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"

    print ""
    sortedLayout = []
    for name, (col, laneName) in elementLayout.items():
        sortedLayout.append((col, name, laneName))
    sortedLayout.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedLayout:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs[name]
        dg = elementGraphics[name]
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

        newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
        dg.setBounds(newBounds)
        repositionedCount += 1

        diagramHandle.save()

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged

        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # =======================================================================
    # PHASE 6: CREATE FLOWS (WITH GUARDS FROM XOR GATEWAYS)
    # =======================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Start -> login -> parallel split
        ("Start", "Log in", ""),
        ("Log in", "Parallel Split", ""),

        # Parallel branches
        ("Parallel Split", "Select items", ""),
        ("Parallel Split", "Set payment method", ""),

        # Reward branch (after items selection)
        ("Select items", "Reward option?", ""),
        ("Reward option?", "Select Reward A", "A"),
        ("Reward option?", "Select Reward B", "B"),
        ("Reward option?", "Select Reward C", "C"),
        ("Select Reward A", "Reward chosen", ""),
        ("Select Reward B", "Reward chosen", ""),
        ("Select Reward C", "Reward chosen", ""),

        # Payment branch (after payment method)
        ("Set payment method", "Payment type?", ""),
        ("Payment type?", "Pay now", "Pay now"),
        ("Payment type?", "Installment agreement", "Installments"),
        ("Pay now", "Payment done", ""),
        ("Installment agreement", "Payment done", ""),

        # Join: must have reward chosen and payment done
        ("Reward chosen", "Parallel Join", ""),
        ("Payment done", "Parallel Join", ""),

        # Delivery
        ("Parallel Join", "Deliver items", ""),
        ("Deliver items", "Return for exchange?", ""),

        # Exchange loop
        ("Return for exchange?", "End", "No"),
        ("Return for exchange?", "Return items", "Yes"),
        ("Return items", "Process exchange", ""),
        ("Process exchange", "Deliver replacement", ""),
        ("Deliver replacement", "Return for exchange?", "")
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

    # =======================================================================
    # FINAL STATE
    # =======================================================================
    print ""
    print "== FINAL STATE =================================================="
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)

    diagramHandle.close()
    print ""
    print "[" + str(step()) + "] Diagram closed"

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
        createOnlinePurchaseProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
