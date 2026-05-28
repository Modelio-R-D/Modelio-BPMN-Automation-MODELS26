#
# RoboticBurgerSeller_UniVienna.py
#
# Description:
#   BPMN process diagram: "Robotic Burger Seller near the University of Vienna"
#
# Applicable on: Package
#
# Version: v9.1
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

# Waiting configuration (auto-unmask)
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 160
START_X = 80

TASK_WIDTH = 200
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
    except Exception as e:
        print "  [addToLane] ERROR: " + str(element.getName()) + " -> " + str(lane.getName()) + " : " + str(e)
        return False

def createStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createMessageStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except Exception as e:
        print "  [createMessageStartEvent] WARNING: cannot create message definition: " + str(e)
    return event

def createEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createMessageEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except Exception as e:
        print "  [createMessageEndEvent] WARNING: cannot create message definition: " + str(e)
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
        try:
            flow.setConditionExpression(guard)
        except Exception as e:
            print "  [createSequenceFlow] WARNING: cannot set guard '" + str(guard) + "': " + str(e)
    return flow

def createSequenceFlowWithGuard(process, source, target, guard):
    return createSequenceFlow(process, source, target, guard=guard)

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
    except Exception as e:
        # Keep noise low here; wait loop logs found/missing anyway.
        pass
    return None

def getBounds(diagramHandle, element):
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None

def getLaneCenterY(diagramHandle, lane, elementHeight):
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2.0 - elementHeight / 2.0
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
    tmp = []
    for elem in elements:
        name = elem.getName()
        col = elementLayout.get(name, (99, "?"))[0]
        tmp.append((col, name, elem))
    tmp.sort()

    for col, name, elem in tmp:
        b = getBounds(diagramHandle, elem)
        if b:
            parts.append(name[:14] + "=Y" + str(int(b["y"])))
        else:
            parts.append(name[:14] + "=--")
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

    # lane center Y (needed for correct unmask position)
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
            print "  [UnmaskPrep] Lane " + laneName + " centerY=" + str(centerY)
        else:
            print "  [UnmaskPrep] WARNING: Lane bounds missing: " + laneName

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
                    print "  [Unmask] " + name + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name + ": ERROR - " + str(e)

    return unmaskedCount

# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createRoboticBurgerSellerProcess(parentPackage):
    title = "Robotic Burger Seller near the University of Vienna"
    processName = "RoboticBurgerSeller_" + EXECUTION_ID
    diagramName = title + " " + EXECUTION_ID

    stepCounter = [0]
    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Title:          " + title
    print "Process Name:   " + processName
    print "Diagram Name:   " + diagramName
    print "=================================================================="

    # ------------------------------------------------------------------------
    # PHASE 1: CREATE PROCESS & LANES
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 1: CREATE PROCESS & LANES =============================="
    print ""

    process = modelingSession.getModel().createBpmnProcess()
    process.setName(processName)
    process.setOwner(parentPackage)
    print "[" + str(step()) + "] Process created: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    print "[" + str(step()) + "] LaneSet created"

    customerLane = createLane(laneSet, "Customer")
    robotLane = createLane(laneSet, "Robot")
    conveyorLane = createLane(laneSet, "Conveyor Belt")

    lanes = {
        "Customer": customerLane,
        "Robot": robotLane,
        "Conveyor Belt": conveyorLane
    }
    laneOrder = ["Customer", "Robot", "Conveyor Belt"]
    print "[" + str(step()) + "] Lanes: Customer, Robot, Conveyor Belt"

    # ------------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # ------------------------------------------------------------------------
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
        print "  [Elem] " + laneName + " / " + name + " | addToLane=" + str(ok)
        return elem

    # Customer
    addElement(createMessageStartEvent, "Order placed", "Customer")
    addElement(createUserTask, "Choose menu or burger", "Customer")
    addElement(createExclusiveGateway, "Menu choice", "Customer")

    addElement(createUserTask, "Choose fries or wedges", "Customer")
    addElement(createExclusiveGateway, "Side choice", "Customer")

    addElement(createEndEvent, "Order received", "Customer")

    # Robot
    addElement(createServiceTask, "Receive order", "Robot")

    addElement(createParallelGateway, "Start drink and side", "Robot")
    addElement(createServiceTask, "Prepare drink (size dependent)", "Robot")
    addElement(createUserTask, "Ask: fries or wedges", "Robot")

    addElement(createServiceTask, "Prepare fries (size dependent)", "Robot")
    addElement(createServiceTask, "Prepare wedges (size dependent)", "Robot")
    addElement(createExclusiveGateway, "Side prepared", "Robot")

    addElement(createParallelGateway, "Menu tasks done", "Robot")
    addElement(createExclusiveGateway, "Menu merge", "Robot")

    addElement(createParallelGateway, "Burger work start", "Robot")
    addElement(createServiceTask, "Prepare burger (ingredients dependent)", "Robot")
    addElement(createServiceTask, "Status updates (every 30s)", "Robot")
    addElement(createParallelGateway, "Burger done", "Robot")

    # Conveyor
    addElement(createServiceTask, "Deliver via conveyor belt", "Conveyor Belt")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(diagramName)
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: " + diagramName

    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    print "[" + str(step()) + "] DiagramHandle obtained"

    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"

    # ------------------------------------------------------------------------
    # PHASE 4: WAIT FOR AUTO-UNMASK (LANES + ELEMENTS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout definition: name -> (column, laneName)
    elementLayout = {
        # Customer
        "Order placed": (0, "Customer"),
        "Choose menu or burger": (2, "Customer"),
        "Menu choice": (3, "Customer"),

        "Choose fries or wedges": (6, "Customer"),
        "Side choice": (7, "Customer"),

        "Order received": (16, "Customer"),

        # Robot
        "Receive order": (1, "Robot"),

        "Start drink and side": (4, "Robot"),
        "Prepare drink (size dependent)": (5, "Robot"),
        "Ask: fries or wedges": (5, "Robot"),

        "Prepare fries (size dependent)": (8, "Robot"),
        "Prepare wedges (size dependent)": (8, "Robot"),
        "Side prepared": (9, "Robot"),

        "Menu tasks done": (10, "Robot"),
        "Menu merge": (11, "Robot"),

        "Burger work start": (12, "Robot"),
        "Prepare burger (ingredients dependent)": (13, "Robot"),
        "Status updates (every 30s)": (13, "Robot"),
        "Burger done": (14, "Robot"),

        # Conveyor
        "Deliver via conveyor belt": (15, "Conveyor Belt"),
    }

    print "[" + str(step()) + "] Waiting for lanes first..."
    laneList = [customerLane, robotLane, conveyorLane]
    laneGraphics, laneAttempts = waitForElements(diagramHandle, laneList)
    print "[" + str(step()) + "] Lane wait attempts: " + str(laneAttempts) + " | Ready: " + str(len(laneGraphics)) + "/" + str(len(laneList))

    print ""
    print "[" + str(step()) + "] Waiting for flow elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
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

    # ------------------------------------------------------------------------
    # PHASE 5: REPOSITION ELEMENTS
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""

    laneY = {}
    for laneName in laneOrder:
        y = getLaneCenterY(diagramHandle, lanes[laneName], TASK_HEIGHT)
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY unknown)"

    print ""
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    sortedElements = []
    for name, (col, ln) in elementLayout.items():
        sortedElements.append((col, name, ln))
    sortedElements.sort()

    repositionedCount = 0

    for col, name, ln in sortedElements:
        if name not in elementRefs:
            print "[" + str(step()) + "] SKIP " + name + ": no elementRef"
            continue

        elem = elementRefs[name]
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        dg = elementGraphics[name]
        currentBounds = getBounds(diagramHandle, elem)
        if not currentBounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(ln, 100)

        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = currentBounds["w"]
            height = currentBounds["h"]

        newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
        dg.setBounds(newBounds)
        repositionedCount += 1

        diagramHandle.save()

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + ln + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (GUARDS ON GATEWAY OUTFLOWS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Order placed", "Receive order", ""),
        ("Receive order", "Choose menu or burger", ""),
        ("Choose menu or burger", "Menu choice", ""),

        # Menu decision (guards!)
        ("Menu choice", "Start drink and side", "Menu"),
        ("Menu choice", "Menu merge", "Burger only"),

        # Menu parallel tasks
        ("Start drink and side", "Prepare drink (size dependent)", ""),
        ("Start drink and side", "Ask: fries or wedges", ""),

        ("Ask: fries or wedges", "Choose fries or wedges", ""),
        ("Choose fries or wedges", "Side choice", ""),

        # Side decision (guards!)
        ("Side choice", "Prepare fries (size dependent)", "Fries"),
        ("Side choice", "Prepare wedges (size dependent)", "Wedges"),

        # Merge side
        ("Prepare fries (size dependent)", "Side prepared", ""),
        ("Prepare wedges (size dependent)", "Side prepared", ""),

        # Join drink + side
        ("Prepare drink (size dependent)", "Menu tasks done", ""),
        ("Side prepared", "Menu tasks done", ""),

        # Continue after menu
        ("Menu tasks done", "Menu merge", ""),

        # Burger phase parallel: burger + status updates
        ("Menu merge", "Burger work start", ""),
        ("Burger work start", "Prepare burger (ingredients dependent)", ""),
        ("Burger work start", "Status updates (every 30s)", ""),
        ("Prepare burger (ingredients dependent)", "Burger done", ""),
        ("Status updates (every 30s)", "Burger done", ""),

        # Delivery
        ("Burger done", "Deliver via conveyor belt", ""),
        ("Deliver via conveyor belt", "Order received", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName + " -> " + tgtName + " | guard=" + guard
            else:
                print "  [Flow] " + srcName + " -> " + tgtName
        else:
            print "  [Flow] WARNING: Missing element for flow: " + str(srcName) + " -> " + str(tgtName)

    print ""
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    diagramHandle.save()
    print "[" + str(step()) + "] Save"

    # ------------------------------------------------------------------------
    # FINAL STATE
    # ------------------------------------------------------------------------
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
    print "Title:    " + title
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
        createRoboticBurgerSellerProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
