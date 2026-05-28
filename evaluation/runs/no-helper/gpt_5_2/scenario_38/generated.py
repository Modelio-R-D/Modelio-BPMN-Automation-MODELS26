#
# BuildingATreeHouse.py
#
# Description:
#   BPMN process diagram: "Building a House" (Tree House)
#   Scenario:
#     - Collect requirements and send to architect
#     - Iterate draft refinement until approved
#     - Create materials list and order materials by categories from online stores
#     - While orders are processed, message friends to build the house
#     - Build the house
#     - Send party invitations
#     - Create attendee list for buying snacks
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

# Waiting configuration (auto-unmask)
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 150
START_X = 80

TASK_WIDTH = 160
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

    # IMPORTANT: In Modelio BPMN, guard text is displayed on gateway outflows
    if guard:
        flow.setConditionExpression(guard)

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

    # Compute lane center Y values for correct unmask positions
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
def createBuildingAHouseProcess(parentPackage):
    processName = "Building_a_House_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Building a House (Tree House)"
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

    builderLane = createLane(laneSet, "Builder")
    architectLane = createLane(laneSet, "Architect")
    storeLane = createLane(laneSet, "Online Store")
    friendsLane = createLane(laneSet, "Friends")

    lanes = {
        "Builder": builderLane,
        "Architect": architectLane,
        "Online Store": storeLane,
        "Friends": friendsLane
    }
    laneOrder = ["Builder", "Architect", "Online Store", "Friends"]

    print "[" + str(step()) + "] Lanes: Builder, Architect, Online Store, Friends"

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
        if not ok:
            print "  WARNING: addToLane failed for " + name
        return elem

    # Builder
    addElement(createStartEvent, "Start", builderLane)
    addElement(createUserTask, "Collect Requirements", builderLane)
    addElement(createUserTask, "Send Requirements to Architect", builderLane)
    addElement(createUserTask, "Review Draft", builderLane)
    addElement(createExclusiveGateway, "Draft Approved?", builderLane)
    addElement(createUserTask, "Refine Requirements", builderLane)
    addElement(createUserTask, "Create Materials List", builderLane)

    addElement(createParallelGateway, "Order and Invite (Split)", builderLane)
    addElement(createParallelGateway, "Order Categories (Split)", builderLane)
    addElement(createParallelGateway, "Materials Ordered (Join)", storeLane)
    addElement(createParallelGateway, "Ready to Build (Join)", builderLane)

    addElement(createUserTask, "Message Friends to Build", builderLane)
    addElement(createUserTask, "Send Party Invitations", builderLane)
    addElement(createUserTask, "Create Attendee List", builderLane)
    addElement(createEndEvent, "End", builderLane)
    print "[" + str(step()) + "] Builder lane: elements created"

    # Architect
    addElement(createUserTask, "Create Draft Plan", architectLane)
    addElement(createUserTask, "Update Draft Plan", architectLane)
    print "[" + str(step()) + "] Architect lane: elements created"

    # Online Store
    addElement(createServiceTask, "Order Lumber", storeLane)
    addElement(createServiceTask, "Order Hardware", storeLane)
    addElement(createServiceTask, "Order Tools", storeLane)
    addElement(createServiceTask, "Ship Materials", storeLane)
    print "[" + str(step()) + "] Online Store lane: elements created"

    # Friends
    addElement(createUserTask, "Confirm Build Participation", friendsLane)
    addElement(createManualTask, "Build Tree House", friendsLane)
    addElement(createUserTask, "RSVP to Party", friendsLane)
    print "[" + str(step()) + "] Friends lane: elements created"

    print ""
    print "  Total elements: " + str(len(elements))

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (AUTO-UNMASK TRIGGER)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("Building a House")
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: Building a House"

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
        # Builder - requirements + draft loop
        "Start": (0, "Builder"),
        "Collect Requirements": (1, "Builder"),
        "Send Requirements to Architect": (2, "Builder"),
        "Create Draft Plan": (3, "Architect"),
        "Review Draft": (4, "Builder"),
        "Draft Approved?": (5, "Builder"),
        "Refine Requirements": (6, "Builder"),
        "Update Draft Plan": (7, "Architect"),

        # Builder - materials + parallel work
        "Create Materials List": (8, "Builder"),
        "Order and Invite (Split)": (9, "Builder"),

        # Order categories split and store tasks
        "Order Categories (Split)": (10, "Builder"),
        "Order Lumber": (11, "Online Store"),
        "Order Hardware": (11, "Online Store"),
        "Order Tools": (11, "Online Store"),
        "Materials Ordered (Join)": (12, "Online Store"),
        "Ship Materials": (13, "Online Store"),

        # Friends branch
        "Message Friends to Build": (10, "Builder"),
        "Confirm Build Participation": (11, "Friends"),

        # Join and build
        "Ready to Build (Join)": (14, "Builder"),
        "Build Tree House": (15, "Friends"),

        # Party + attendee list
        "Send Party Invitations": (16, "Builder"),
        "RSVP to Party": (17, "Friends"),
        "Create Attendee List": (18, "Builder"),
        "End": (19, "Builder"),
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
        y = getLaneCenterY(diagramHandle, lanes[laneName])
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
        dg = elementGraphics.get(name)

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
        # Requirements to architect
        ("Start", "Collect Requirements", ""),
        ("Collect Requirements", "Send Requirements to Architect", ""),
        ("Send Requirements to Architect", "Create Draft Plan", ""),

        # Draft review loop
        ("Create Draft Plan", "Review Draft", ""),
        ("Review Draft", "Draft Approved?", ""),

        # From XOR gateway -> GUARDS REQUIRED
        ("Draft Approved?", "Refine Requirements", "Needs Changes"),
        ("Draft Approved?", "Create Materials List", "Approved"),

        ("Refine Requirements", "Update Draft Plan", ""),
        ("Update Draft Plan", "Review Draft", ""),

        # Parallel work: ordering and inviting
        ("Create Materials List", "Order and Invite (Split)", ""),

        # Branch A: order materials
        ("Order and Invite (Split)", "Order Categories (Split)", ""),
        ("Order Categories (Split)", "Order Lumber", ""),
        ("Order Categories (Split)", "Order Hardware", ""),
        ("Order Categories (Split)", "Order Tools", ""),
        ("Order Lumber", "Materials Ordered (Join)", ""),
        ("Order Hardware", "Materials Ordered (Join)", ""),
        ("Order Tools", "Materials Ordered (Join)", ""),
        ("Materials Ordered (Join)", "Ship Materials", ""),
        ("Ship Materials", "Ready to Build (Join)", ""),

        # Branch B: invite friends to help build
        ("Order and Invite (Split)", "Message Friends to Build", ""),
        ("Message Friends to Build", "Confirm Build Participation", ""),
        ("Confirm Build Participation", "Ready to Build (Join)", ""),

        # Build, then party, then attendee list
        ("Ready to Build (Join)", "Build Tree House", ""),
        ("Build Tree House", "Send Party Invitations", ""),
        ("Send Party Invitations", "RSVP to Party", ""),
        ("RSVP to Party", "Create Attendee List", ""),
        ("Create Attendee List", "End", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
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

    print ""
    print "=================================================================="
    print "COMPLETE"
    print "=================================================================="
    print "Title:    Building a House (Tree House)"
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
        createBuildingAHouseProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
