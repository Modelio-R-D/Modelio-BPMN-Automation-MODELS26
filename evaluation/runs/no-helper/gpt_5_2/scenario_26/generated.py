#
# BecomingAParentProcess.py
#
# Description:
#   BPMN process diagram: "Becoming A Parent"
#   Supports planning, taking, and extending a maternity leave:
#     - Fetch info about possible leave models (duration, split between parents)
#     - Parent selects model
#     - Collect relevant information
#     - Notify Social Security and Company in time
#     - Gather information/confirmations from Company and Social Security
#     - Near end of leave, decide on extension and notify again if needed
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
    if guard:
        # IMPORTANT: guards show as condition labels on gateway outflows
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
        # Slight offset (empirical) so elements sit well in lane
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
            laneName = elementLayout.get(name, (0, "Parent"))[1]
            targetY = laneY.get(laneName, 100)

            try:
                # CRITICAL: unmask at a Y position inside the correct lane
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

def createBecomingAParentProcess(parentPackage):
    processName = "Becoming_A_Parent_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Becoming A Parent"
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

    parentLane = createLane(laneSet, "Parent")
    companyLane = createLane(laneSet, "Company HR")
    ssLane = createLane(laneSet, "Social Security")

    lanes = {
        "Parent": parentLane,
        "Company HR": companyLane,
        "Social Security": ssLane
    }
    laneOrder = ["Parent", "Company HR", "Social Security"]

    print "[" + str(step()) + "] Lanes: Parent, Company HR, Social Security"

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
            print "  [LaneAssign] WARNING: Failed addToLane for: " + name + " -> " + lane.getName()
        return elem

    # --- Parent lane elements ---
    addElement(createStartEvent, "Expecting Child", parentLane)
    addElement(createServiceTask, "Fetch Leave Models", parentLane)
    addElement(createUserTask, "Review Leave Models", parentLane)
    addElement(createUserTask, "Select Leave Model", parentLane)
    addElement(createUserTask, "Provide Required Details", parentLane)

    addElement(createParallelGateway, "Notify Parties", parentLane)
    addElement(createUserTask, "Notify Company (Planned Leave)", parentLane)
    addElement(createServiceTask, "Notify Social Security (Planned Leave)", parentLane)

    addElement(createParallelGateway, "Confirmations Received", parentLane)
    addElement(createUserTask, "Review Confirmations", parentLane)
    addElement(createManualTask, "Start Maternity Leave", parentLane)
    addElement(createUserTask, "Decide on Extension", parentLane)
    addElement(createExclusiveGateway, "Extend Leave?", parentLane)

    addElement(createUserTask, "Request Extension", parentLane)
    addElement(createParallelGateway, "Notify Extension Parties", parentLane)
    addElement(createUserTask, "Notify Company (Extension)", parentLane)
    addElement(createServiceTask, "Notify Social Security (Extension)", parentLane)
    addElement(createParallelGateway, "Extension Confirmed", parentLane)
    addElement(createUserTask, "Review Extension Confirmations", parentLane)

    addElement(createEndEvent, "Return to Work", parentLane)
    addElement(createEndEvent, "Leave Extended", parentLane)

    print "[" + str(step()) + "] Parent lane: elements created"

    # --- Company HR lane elements ---
    addElement(createUserTask, "Provide Company Policy Info", companyLane)
    addElement(createUserTask, "Confirm Leave Dates", companyLane)
    addElement(createUserTask, "Confirm Extension Dates", companyLane)
    print "[" + str(step()) + "] Company HR lane: elements created"

    # --- Social Security lane elements ---
    addElement(createServiceTask, "Validate Eligibility", ssLane)
    addElement(createServiceTask, "Register Leave and Benefits", ssLane)
    addElement(createServiceTask, "Update Benefits for Extension", ssLane)
    print "[" + str(step()) + "] Social Security lane: elements created"

    print ""
    print "  Total elements: " + str(len(elements))

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (AUTO-UNMASK TRIGGER)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("Becoming A Parent")
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: Becoming A Parent"

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

    # Layout: element name -> (column, laneName)
    elementLayout = {
        # Parent
        "Expecting Child": (0, "Parent"),
        "Fetch Leave Models": (1, "Parent"),
        "Review Leave Models": (2, "Parent"),
        "Select Leave Model": (3, "Parent"),
        "Provide Required Details": (4, "Parent"),

        "Notify Parties": (5, "Parent"),
        "Notify Company (Planned Leave)": (6, "Parent"),
        "Notify Social Security (Planned Leave)": (6, "Parent"),

        "Provide Company Policy Info": (7, "Company HR"),
        "Confirm Leave Dates": (8, "Company HR"),

        "Validate Eligibility": (7, "Social Security"),
        "Register Leave and Benefits": (8, "Social Security"),

        "Confirmations Received": (9, "Parent"),
        "Review Confirmations": (10, "Parent"),
        "Start Maternity Leave": (11, "Parent"),
        "Decide on Extension": (12, "Parent"),
        "Extend Leave?": (13, "Parent"),

        "Request Extension": (14, "Parent"),
        "Notify Extension Parties": (15, "Parent"),
        "Notify Company (Extension)": (16, "Parent"),
        "Notify Social Security (Extension)": (16, "Parent"),

        "Confirm Extension Dates": (17, "Company HR"),
        "Update Benefits for Extension": (17, "Social Security"),

        "Extension Confirmed": (18, "Parent"),
        "Review Extension Confirmations": (19, "Parent"),
        "Leave Extended": (20, "Parent"),

        "Return to Work": (14, "Parent"),
    }

    # Wait for elements AND lanes (lanes needed for bounds computations)
    waitList = []
    for ln in laneOrder:
        waitList.append(lanes[ln])
    for e in elements:
        waitList.append(e)

    print "[" + str(step()) + "] Waiting for elements+lanes (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    elementGraphics, attempts = waitForElements(diagramHandle, waitList)
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)

    if foundCount == len(waitList):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " graphics ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in waitList if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(waitList)) + " graphics ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)

        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing BPMN elements (not lanes)..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"

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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY=None)"

    print ""

    sortedLayout = []
    for name, (col, laneName) in elementLayout.items():
        sortedLayout.append((col, name, laneName))
    sortedLayout.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedLayout:
        elem = elementRefs.get(name)
        if not elem:
            print "[" + str(step()) + "] SKIP " + name + ": element not found in elementRefs"
            continue

        dg = elementGraphics.get(name)
        if not dg:
            # graphics might be missing if auto-unmask timing issues persist
            print "[" + str(step()) + "] SKIP " + laneName + "/" + name + ": not in diagram graphics"
            continue

        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + laneName + "/" + name + ": no bounds"
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
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Expecting Child", "Fetch Leave Models", ""),
        ("Fetch Leave Models", "Review Leave Models", ""),
        ("Review Leave Models", "Select Leave Model", ""),
        ("Select Leave Model", "Provide Required Details", ""),

        # Notify in time (parallel)
        ("Provide Required Details", "Notify Parties", ""),
        ("Notify Parties", "Notify Company (Planned Leave)", ""),
        ("Notify Parties", "Notify Social Security (Planned Leave)", ""),

        # Company track
        ("Notify Company (Planned Leave)", "Provide Company Policy Info", ""),
        ("Provide Company Policy Info", "Confirm Leave Dates", ""),

        # Social security track
        ("Notify Social Security (Planned Leave)", "Validate Eligibility", ""),
        ("Validate Eligibility", "Register Leave and Benefits", ""),

        # Join
        ("Confirm Leave Dates", "Confirmations Received", ""),
        ("Register Leave and Benefits", "Confirmations Received", ""),

        ("Confirmations Received", "Review Confirmations", ""),
        ("Review Confirmations", "Start Maternity Leave", ""),
        ("Start Maternity Leave", "Decide on Extension", ""),
        ("Decide on Extension", "Extend Leave?", ""),

        # Decision (guards!)
        ("Extend Leave?", "Return to Work", "No"),
        ("Extend Leave?", "Request Extension", "Yes"),

        # Extension notify (parallel)
        ("Request Extension", "Notify Extension Parties", ""),
        ("Notify Extension Parties", "Notify Company (Extension)", ""),
        ("Notify Extension Parties", "Notify Social Security (Extension)", ""),

        # Extension confirmations
        ("Notify Company (Extension)", "Confirm Extension Dates", ""),
        ("Notify Social Security (Extension)", "Update Benefits for Extension", ""),

        ("Confirm Extension Dates", "Extension Confirmed", ""),
        ("Update Benefits for Extension", "Extension Confirmed", ""),

        ("Extension Confirmed", "Review Extension Confirmations", ""),
        ("Review Extension Confirmations", "Leave Extended", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            f = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(f)
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
    print "Process:  " + processName
    print "Title:    Becoming A Parent"
    print "Lanes:    " + str(len(lanes))
    print "Elements: " + str(len(elements))
    print "Flows:    " + str(len(flows))
    print "=================================================================="

    return process

# ============================================================================
# MACRO ENTRY POINT
# ============================================================================
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBecomingAParentProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
