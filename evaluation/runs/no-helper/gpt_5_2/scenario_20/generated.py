#
# EvanstonianRoomServiceProcess.py
#
# Description:
#   BPMN process diagram for "The Evanstonian" room service workflow.
#
# Narrative:
#   - Guest calls room service
#   - Room-service manager takes order, sends ticket to kitchen
#   - 80% of orders include alcohol -> manager notifies sommelier
#   - Manager assigns order to waiter
#   - Kitchen prepares food, sommelier prepares alcohol (if any), waiter readies cart and nonalcoholic drinks
#   - Waiter delivers to room, returns, and bills (may delay billing if busy)
#
# Applicable on: Package
#
# Version: v1.0 - March 2026
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
SCRIPT_VERSION = "v1.0"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 170
START_X = 80

TASK_WIDTH = 180
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
        try:
            flow.setConditionExpression(guard)
        except:
            pass
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
            shortName = name[:14]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
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

    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Waiter"))[1]
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

def createEvanstonianRoomServiceProcess(parentPackage):
    processName = "Evanstonian_RoomService_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN EVANSTONIAN ROOM SERVICE - DEBUG LOG"
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
    managerLane = createLane(laneSet, "Room Service Manager")
    kitchenLane = createLane(laneSet, "Kitchen")
    sommelierLane = createLane(laneSet, "Sommelier")
    waiterLane = createLane(laneSet, "Waiter")

    lanes = {
        "Guest": guestLane,
        "Room Service Manager": managerLane,
        "Kitchen": kitchenLane,
        "Sommelier": sommelierLane,
        "Waiter": waiterLane
    }
    laneOrder = ["Guest", "Room Service Manager", "Kitchen", "Sommelier", "Waiter"]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

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
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        print "  [Elem] " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    # Guest
    addElement(createStartEvent, "Call Room Service", guestLane)

    # Manager
    addElement(createUserTask, "Take Down Order", managerLane)
    addElement(createUserTask, "Submit Order Ticket to Kitchen", managerLane)
    addElement(createExclusiveGateway, "Alcohol Included?", managerLane)
    addElement(createUserTask, "Give Order to Sommelier", managerLane)
    addElement(createUserTask, "Assign Order to Waiter", managerLane)

    # Split and join variants
    addElement(createParallelGateway, "Split: Food + Cart", managerLane)
    addElement(createParallelGateway, "Join: Food + Cart", managerLane)
    addElement(createParallelGateway, "Split: Food + Wine + Cart", managerLane)
    addElement(createParallelGateway, "Join: Food + Wine + Cart", managerLane)
    addElement(createExclusiveGateway, "Ready to Deliver (Merge)", managerLane)

    # Kitchen
    addElement(createManualTask, "Prepare Food", kitchenLane)

    # Sommelier
    addElement(createManualTask, "Fetch Wine and Prepare Alcohol", sommelierLane)

    # Waiter
    addElement(createManualTask, "Ready Cart", waiterLane)
    addElement(createManualTask, "Prepare Nonalcoholic Drinks", waiterLane)
    addElement(createManualTask, "Deliver Order to Room", waiterLane)
    addElement(createManualTask, "Return to Room Service Station", waiterLane)
    addElement(createExclusiveGateway, "Bill Now?", waiterLane)
    addElement(createManualTask, "Prepare or Deliver Another Order", waiterLane)
    addElement(createUserTask, "Debit Guest Account", waiterLane)
    addElement(createEndEvent, "Order Completed", waiterLane)

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

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

    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"

    # =========================================================================
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        # Guest
        "Call Room Service": (0, "Guest"),

        # Manager - intake and routing
        "Take Down Order": (1, "Room Service Manager"),
        "Submit Order Ticket to Kitchen": (2, "Room Service Manager"),
        "Alcohol Included?": (3, "Room Service Manager"),
        "Give Order to Sommelier": (4, "Room Service Manager"),
        "Assign Order to Waiter": (5, "Room Service Manager"),

        # Parallel variants and merge
        "Split: Food + Cart": (6, "Room Service Manager"),
        "Join: Food + Cart": (9, "Room Service Manager"),
        "Split: Food + Wine + Cart": (6, "Room Service Manager"),
        "Join: Food + Wine + Cart": (9, "Room Service Manager"),
        "Ready to Deliver (Merge)": (10, "Room Service Manager"),

        # Kitchen
        "Prepare Food": (7, "Kitchen"),

        # Sommelier
        "Fetch Wine and Prepare Alcohol": (7, "Sommelier"),

        # Waiter
        "Ready Cart": (7, "Waiter"),
        "Prepare Nonalcoholic Drinks": (8, "Waiter"),
        "Deliver Order to Room": (11, "Waiter"),
        "Return to Room Service Station": (12, "Waiter"),
        "Bill Now?": (13, "Waiter"),
        "Prepare or Deliver Another Order": (14, "Waiter"),
        "Debit Guest Account": (15, "Waiter"),
        "Order Completed": (16, "Waiter"),
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
        if y is not None:
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

        elem = elementRefs.get(name)
        if not elem:
            print "[" + str(step()) + "] SKIP " + name + ": no element ref"
            continue

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

    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Intake
        ("Call Room Service", "Take Down Order", ""),
        ("Take Down Order", "Submit Order Ticket to Kitchen", ""),
        ("Submit Order Ticket to Kitchen", "Alcohol Included?", ""),

        # Alcohol decision (guards must be on flows FROM gateway)
        ("Alcohol Included?", "Give Order to Sommelier", "Yes (80%)"),
        ("Alcohol Included?", "Assign Order to Waiter", "No (20%)"),

        # If alcohol yes, notify sommelier then assign waiter
        ("Give Order to Sommelier", "Assign Order to Waiter", ""),

        # Two variants of parallelization (2-way vs 3-way)
        ("Assign Order to Waiter", "Split: Food + Wine + Cart", "Alcohol order"),
        ("Assign Order to Waiter", "Split: Food + Cart", "No alcohol order"),

        # Split: Food + Cart (2 branches)
        ("Split: Food + Cart", "Prepare Food", ""),
        ("Split: Food + Cart", "Ready Cart", ""),
        ("Ready Cart", "Prepare Nonalcoholic Drinks", ""),
        ("Prepare Food", "Join: Food + Cart", ""),
        ("Prepare Nonalcoholic Drinks", "Join: Food + Cart", ""),

        # Split: Food + Wine + Cart (3 branches)
        ("Split: Food + Wine + Cart", "Prepare Food", ""),
        ("Split: Food + Wine + Cart", "Fetch Wine and Prepare Alcohol", ""),
        ("Split: Food + Wine + Cart", "Ready Cart", ""),
        ("Fetch Wine and Prepare Alcohol", "Join: Food + Wine + Cart", ""),
        ("Prepare Food", "Join: Food + Wine + Cart", ""),
        ("Prepare Nonalcoholic Drinks", "Join: Food + Wine + Cart", ""),

        # Merge to deliver (exclusive merge)
        ("Join: Food + Cart", "Ready to Deliver (Merge)", ""),
        ("Join: Food + Wine + Cart", "Ready to Deliver (Merge)", ""),

        # Delivery and billing
        ("Ready to Deliver (Merge)", "Deliver Order to Room", ""),
        ("Deliver Order to Room", "Return to Room Service Station", ""),
        ("Return to Room Service Station", "Bill Now?", ""),

        # Billing decision (guards must be on flows FROM gateway)
        ("Bill Now?", "Debit Guest Account", "Yes"),
        ("Bill Now?", "Prepare or Deliver Another Order", "No"),
        ("Prepare or Deliver Another Order", "Debit Guest Account", ""),

        ("Debit Guest Account", "Order Completed", ""),
    ]

    flows = []
    missingFlowRefs = 0
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName + " -> " + tgtName + " | Guard=" + guard
            else:
                print "  [Flow] " + srcName + " -> " + tgtName
        else:
            missingFlowRefs += 1
            print "  [Flow] WARNING: Missing ref for " + srcName + " -> " + tgtName

    print ""
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows | Missing refs: " + str(missingFlowRefs)

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
        createEvanstonianRoomServiceProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
