#
# ContractProcess.py
#
# Description:
#   BPMN process diagram "Contract" for ordering parts from multiple web shops,
#   starting building when first parts arrive, and reordering based on stock thresholds.
#
# Applicable on: Package
#
# Version: 9.1 - March 2026
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
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 160
START_X = 80

# Default task dimensions
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
    gw = modelingSession.getModel().createBpmnExclusiveGateway()
    gw.setName(name)
    gw.setContainer(process)
    return gw


def createParallelGateway(process, name):
    gw = modelingSession.getModel().createBpmnParallelGateway()
    gw.setName(name)
    gw.setContainer(process)
    return gw


def createSequenceFlow(process, source, target, name="", guard=""):
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)

    # Guard condition for gateway outflows (shown on arrow in diagram)
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
            shortName = name[:12]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:12] + "=--")
    return "Elements: " + ", ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK (Modelio auto-unmasks on diagram creation)
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

    # Lane center Y positions
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Builder"))[1]
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

def createContractProcess(parentPackage):
    processName = "Contract_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - CONTRACT"
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

    builderLane = createLane(laneSet, "Builder")
    shopsLane = createLane(laneSet, "Web Shops")
    friendsLane = createLane(laneSet, "Friends")

    lanes = {
        "Builder": builderLane,
        "Web Shops": shopsLane,
        "Friends": friendsLane
    }
    laneOrder = ["Builder", "Web Shops", "Friends"]

    print "[" + str(step()) + "] Lanes: Builder, Web Shops, Friends"

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
        print "  [Create] " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    # Builder lane
    addElement(createStartEvent, "Need Parts", builderLane)
    addElement(createUserTask, "Create Parts List", builderLane)
    addElement(createServiceTask, "Query Web Shops", builderLane)
    addElement(createServiceTask, "Compare Offers (Price/Time)", builderLane)
    addElement(createUserTask, "Allocate Parts (Cheapest)", builderLane)
    addElement(createUserTask, "Create Order Lists Per Shop", builderLane)
    addElement(createServiceTask, "Place Orders", builderLane)

    addElement(createManualTask, "Receive Delivery Batch", builderLane)
    addElement(createUserTask, "Add Delivered Parts To Stock", builderLane)

    addElement(createUserTask, "Build With Available Parts", builderLane)
    addElement(createServiceTask, "Consume Parts And Update Stock", builderLane)
    addElement(createServiceTask, "Check Stock Levels", builderLane)

    addElement(createExclusiveGateway, "Stock Level?", builderLane)
    addElement(createServiceTask, "Reorder Cheapest", builderLane)
    addElement(createServiceTask, "Reorder Fastest", builderLane)

    addElement(createUserTask, "Write Complaint Email", builderLane)

    addElement(createExclusiveGateway, "Build Complete?", builderLane)
    addElement(createEndEvent, "Contract Completed", builderLane)
    addElement(createEndEvent, "Stopped (No Stock)", builderLane)

    # Web Shops lane
    addElement(createServiceTask, "Send Availability And Quotes", shopsLane)
    addElement(createServiceTask, "Ship Parts In Batches", shopsLane)

    # Friends lane
    addElement(createManualTask, "Friends Read Complaint", friendsLane)

    print ""
    print "  Total elements: " + str(len(elements))

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("Contract")
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: Contract"

    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    print "[" + str(step()) + "] DiagramHandle obtained"

    # Save triggers auto-unmask of existing elements (Modelio behavior)
    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"

    # =========================================================================
    # PHASE 4: WAIT FOR AUTO-UNMASK (+ MANUAL UNMASK FALLBACK)
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        "Need Parts": (0, "Builder"),
        "Create Parts List": (1, "Builder"),
        "Query Web Shops": (2, "Builder"),
        "Send Availability And Quotes": (3, "Web Shops"),
        "Compare Offers (Price/Time)": (4, "Builder"),
        "Allocate Parts (Cheapest)": (5, "Builder"),
        "Create Order Lists Per Shop": (6, "Builder"),
        "Place Orders": (7, "Builder"),
        "Ship Parts In Batches": (8, "Web Shops"),
        "Receive Delivery Batch": (9, "Builder"),
        "Add Delivered Parts To Stock": (10, "Builder"),
        "Build Complete?": (11, "Builder"),
        "Build With Available Parts": (12, "Builder"),
        "Consume Parts And Update Stock": (13, "Builder"),
        "Check Stock Levels": (14, "Builder"),
        "Stock Level?": (15, "Builder"),
        "Reorder Cheapest": (16, "Builder"),
        "Reorder Fastest": (17, "Builder"),
        "Write Complaint Email": (18, "Builder"),
        "Friends Read Complaint": (19, "Friends"),
        "Contract Completed": (20, "Builder"),
        "Stopped (No Stock)": (20, "Builder"),
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
        print "[" + str(step()) + "] Trying manual unmask for missing elements (inside lane Y)..."
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
        y = getLaneCenterY(diagramHandle, lanes[laneName])
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"

    print ""

    sortedLayout = []
    for name, (col, ln) in elementLayout.items():
        sortedLayout.append((col, name, ln))
    sortedLayout.sort()

    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    repositionedCount = 0

    for col, name, ln in sortedLayout:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs.get(name)
        if not elem:
            print "[" + str(step()) + "] SKIP " + name + ": elementRef missing"
            continue

        dg = elementGraphics[name]
        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(ln, 100)

        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]

        dg.setBounds(Draw2DRectangle(int(targetX), int(targetY), int(width), int(height)))
        diagramHandle.save()
        repositionedCount += 1

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + ln + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes
        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # =========================================================================
    # PHASE 6: CREATE FLOWS (use Guards on gateway outflows)
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Need Parts", "Create Parts List", ""),
        ("Create Parts List", "Query Web Shops", ""),
        ("Query Web Shops", "Send Availability And Quotes", ""),
        ("Send Availability And Quotes", "Compare Offers (Price/Time)", ""),
        ("Compare Offers (Price/Time)", "Allocate Parts (Cheapest)", ""),
        ("Allocate Parts (Cheapest)", "Create Order Lists Per Shop", ""),
        ("Create Order Lists Per Shop", "Place Orders", ""),
        ("Place Orders", "Ship Parts In Batches", ""),
        ("Ship Parts In Batches", "Receive Delivery Batch", ""),
        ("Receive Delivery Batch", "Add Delivered Parts To Stock", ""),

        # Main loop entry (first delivery triggers build cycle)
        ("Add Delivered Parts To Stock", "Build Complete?", ""),

        # If not complete, build
        ("Build Complete?", "Build With Available Parts", "No"),
        ("Build Complete?", "Contract Completed", "Yes"),

        ("Build With Available Parts", "Consume Parts And Update Stock", ""),
        ("Consume Parts And Update Stock", "Check Stock Levels", ""),
        ("Check Stock Levels", "Stock Level?", ""),

        # Stock decisions (gateway outflows MUST use guards)
        ("Stock Level?", "Write Complaint Email", "0"),
        ("Stock Level?", "Reorder Fastest", "<3"),
        ("Stock Level?", "Reorder Cheapest", "<5"),
        ("Stock Level?", "Build Complete?", ">=5"),

        # Reorder paths
        ("Reorder Cheapest", "Ship Parts In Batches", ""),
        ("Reorder Fastest", "Ship Parts In Batches", ""),

        # Complaint path
        ("Write Complaint Email", "Friends Read Complaint", ""),
        ("Friends Read Complaint", "Stopped (No Stock)", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
            print "  [Flow] " + srcName + " -> " + tgtName + (" [Guard=" + guard + "]" if guard else "")
        else:
            print "  [Flow] WARNING: Missing element for flow: " + srcName + " -> " + tgtName

    diagramHandle.save()
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
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
        createContractProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
