#
# ComputerRepairProcess.py
#
# Description:
#   BPMN process diagram:
#   - Customer brings defective computer
#   - CRS checks defect and provides repair cost calculation
#   - Customer decides: accept costs or take computer home unrepaired
#   - Repair consists of two activities executed in arbitrary order (modeled as parallel split/join)
#     * Check and repair hardware
#     * Check and configure software
#   - After each activity, system functionality is tested
#   - If error detected, repeat repair cycle; otherwise finish and return computer
#
# Applicable on: Package
# Version: 1.0
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
WAIT_TIME_MS = 80
MAX_ATTEMPTS = 6

# Layout configuration
SPACING = 160
START_X = 80

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
    except Exception as e:
        print "  [addToLane] ERROR: " + str(e)
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

    # IMPORTANT: For gateway outflows, guard must be set as condition expression
    if guard:
        try:
            flow.setConditionExpression(guard)
        except:
            pass
    return flow


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
        else:
            print "  [Unmask] WARNING: No bounds for lane " + laneName

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

def createComputerRepairProcess(parentPackage):

    processName = "ComputerRepair_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN COMPUTER REPAIR PROCESS - DEBUG LOG"
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
    print "[" + str(step()) + "] Process created: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    customerLane = createLane(laneSet, "Customer")
    crsLane = createLane(laneSet, "CRS")
    techLane = createLane(laneSet, "Technician")

    lanes = {
        "Customer": customerLane,
        "CRS": crsLane,
        "Technician": techLane
    }
    laneOrder = ["Customer", "CRS", "Technician"]
    print "[" + str(step()) + "] Lanes: Customer, CRS, Technician"

    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
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
        print "  [Element] " + laneName + ": " + name + " | addToLane=" + str(ok)
        return elem

    # Customer + CRS intake and decision
    addElement(createStartEvent, "Customer arrives", "Customer")
    addElement(createUserTask, "Hand in defective computer", "Customer")
    addElement(createUserTask, "Check defect", "CRS")
    addElement(createUserTask, "Calculate repair costs", "CRS")
    addElement(createUserTask, "Provide cost calculation", "CRS")
    addElement(createExclusiveGateway, "Costs acceptable?", "Customer")
    addElement(createEndEvent, "Take computer home unrepaired", "Customer")

    # Repair cycle (modeled as parallel split/join to represent arbitrary order)
    addElement(createParallelGateway, "Start repair work", "Technician")
    addElement(createManualTask, "Check and repair hardware", "Technician")
    addElement(createServiceTask, "Test after hardware repair", "Technician")
    addElement(createUserTask, "Check and configure software", "Technician")
    addElement(createServiceTask, "Test after software config", "Technician")
    addElement(createParallelGateway, "Repair activities done", "Technician")
    addElement(createExclusiveGateway, "Error detected?", "Technician")

    # Finish
    addElement(createUserTask, "Return repaired computer", "CRS")
    addElement(createEndEvent, "Computer returned repaired", "Customer")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # Layout: element name -> (column_index, lane_name)
    elementLayout = {
        "Customer arrives": (0, "Customer"),
        "Hand in defective computer": (1, "Customer"),
        "Check defect": (2, "CRS"),
        "Calculate repair costs": (3, "CRS"),
        "Provide cost calculation": (4, "CRS"),
        "Costs acceptable?": (5, "Customer"),
        "Take computer home unrepaired": (6, "Customer"),

        "Start repair work": (6, "Technician"),
        "Check and repair hardware": (7, "Technician"),
        "Check and configure software": (7, "Technician"),
        "Test after hardware repair": (8, "Technician"),
        "Test after software config": (8, "Technician"),
        "Repair activities done": (9, "Technician"),
        "Error detected?": (10, "Technician"),

        "Return repaired computer": (11, "CRS"),
        "Computer returned repaired": (12, "Customer"),
    }

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

    # Also wait for lanes to be ready (for bounds computations)
    laneList = [customerLane, crsLane, techLane]
    waitList = []
    waitList.extend(laneList)
    waitList.extend(elements)

    print "[" + str(step()) + "] Waiting for lanes+elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""
    graphicsAll, attempts = waitForElements(diagramHandle, waitList)

    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(graphicsAll)
    print ""
    print "[" + str(step()) + "] Wait done in " + str(totalWaitTime) + "ms | Ready: " + str(foundCount) + "/" + str(len(waitList))

    # Build elementGraphics only for flow nodes (elements), by name
    elementGraphics = {}
    for elem in elements:
        dg = getGraphics(diagramHandle, elem)
        if dg:
            elementGraphics[elem.getName()] = dg

    if len(elementGraphics) != len(elements):
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: Some elements missing after wait: " + str(len(elements) - len(elementGraphics))
        print "         Missing: " + ", ".join(missing)

        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing elements (inside correct lane Y)..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"
        else:
            print ""
            print "[" + str(step()) + "] Manual unmask: 0 elements unmasked"

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
        y = getLaneCenterY(diagramHandle, lanes[laneName])
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (cannot compute centerY)"

    print ""
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    # Sort layout by column for predictable placement
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    repositionedCount = 0

    for col, name, laneName in sortedElements:
        elem = elementRefs.get(name)
        if not elem:
            print "[" + str(step()) + "] SKIP (not found): " + name
            continue

        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP (not in diagram): " + name
            continue

        dg = elementGraphics[name]
        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP (no bounds): " + name
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
        diagramHandle.save()
        repositionedCount += 1

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Customer arrives", "Hand in defective computer", ""),
        ("Hand in defective computer", "Check defect", ""),
        ("Check defect", "Calculate repair costs", ""),
        ("Calculate repair costs", "Provide cost calculation", ""),
        ("Provide cost calculation", "Costs acceptable?", ""),

        # Decision
        ("Costs acceptable?", "Take computer home unrepaired", "No"),
        ("Costs acceptable?", "Start repair work", "Yes"),

        # Parallel repair activities (arbitrary order)
        ("Start repair work", "Check and repair hardware", ""),
        ("Start repair work", "Check and configure software", ""),

        # After each activity, test
        ("Check and repair hardware", "Test after hardware repair", ""),
        ("Check and configure software", "Test after software config", ""),

        # Join after tests
        ("Test after hardware repair", "Repair activities done", ""),
        ("Test after software config", "Repair activities done", ""),

        # Error check and loop
        ("Repair activities done", "Error detected?", ""),
        ("Error detected?", "Start repair work", "Yes"),
        ("Error detected?", "Return repaired computer", "No"),

        # Finish
        ("Return repaired computer", "Computer returned repaired", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            print "  [Flow] " + srcName + " -> " + tgtName + (" | guard=" + guard if guard else "")
        else:
            print "  [Flow] WARNING: Missing element for " + srcName + " -> " + tgtName

    diagramHandle.save()
    print ""
    print "[" + str(step()) + "] Created flows: " + str(len(flows))
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
    print "Elements: " + str(len(elements)) + " (" + str(len(elementGraphics)) + " in diagram graphics)"
    print "Flows:    " + str(len(flows))
    print "=================================================================="

    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createComputerRepairProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
