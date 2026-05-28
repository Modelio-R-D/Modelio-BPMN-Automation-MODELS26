#
# USICourseRegistrationProcess.py
#
# Description:
#   BPMN process diagram: "New Application for Registering for an USI course"
#
# Workflow (from requirement):
#   - Search/select course, check free slots, show courses/dates, select one
#   - Check if applicant already has an account
#     - If not: check eligible university
#       - If eligible: register account
#       - If not: request activation and wait for response
#   - Log in
#   - Link Twitter and optionally tweet friends
#   - Provide payment info, complete registration
#   - Receive course ticket
#
# Applicable on: Package
# Version: v1.0 (macro generated)
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

# Waiting configuration (auto-unmask timing)
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
    except Exception as e:
        print "  [addToLane] ERROR: " + element.getName() + " -> " + lane.getName() + " : " + str(e)
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


def createMessageEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
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

    # IMPORTANT: guard/condition text on gateway outflows
    if guard:
        try:
            flow.setConditionExpression(guard)
        except Exception as e:
            print "  [Flow Guard] WARNING: Could not set guard '" + guard + "' : " + str(e)

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
            print "  [LaneY] " + laneName + " centerY=" + str(centerY)
        else:
            print "  [LaneY] WARNING: No bounds for lane " + laneName

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Applicant"))[1]
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

def createUSICourseRegistrationProcess(parentPackage):
    title = "New Application for Registering for an USI course"
    processName = "USI_Course_Registration_" + EXECUTION_ID

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

    # Lanes
    applicantLane = createLane(laneSet, "Applicant")
    systemLane = createLane(laneSet, "Sports Institute System")
    universityLane = createLane(laneSet, "University")
    twitterLane = createLane(laneSet, "Twitter")

    lanes = {
        "Applicant": applicantLane,
        "Sports Institute System": systemLane,
        "University": universityLane,
        "Twitter": twitterLane
    }
    laneOrder = ["Applicant", "Sports Institute System", "University", "Twitter"]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

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
        print "  [Element] " + laneName + " / " + name + " | addToLane=" + str(ok)
        return elem

    # Applicant
    addElement(createStartEvent, "Start Registration", "Applicant")
    addElement(createUserTask, "Search Courses", "Applicant")
    addElement(createUserTask, "Select Course and Date", "Applicant")
    addElement(createExclusiveGateway, "Account Exists?", "Applicant")
    addElement(createExclusiveGateway, "Eligible University?", "Applicant")
    addElement(createUserTask, "Register Account", "Applicant")
    addElement(createUserTask, "Request Activation", "Applicant")
    addElement(createUserTask, "Wait for Activation Response", "Applicant")
    addElement(createExclusiveGateway, "Activation Approved?", "Applicant")
    addElement(createEndEvent, "Activation Rejected", "Applicant")
    addElement(createUserTask, "Log In", "Applicant")
    addElement(createExclusiveGateway, "Tweet to Friends?", "Applicant")
    addElement(createUserTask, "Provide Payment Information", "Applicant")
    addElement(createMessageEndEvent, "Course Ticket Received", "Applicant")

    # System
    addElement(createServiceTask, "Check Slot Availability", "Sports Institute System")
    addElement(createExclusiveGateway, "Slots Free?", "Sports Institute System")
    addElement(createServiceTask, "Show Courses and Dates", "Sports Institute System")
    addElement(createEndEvent, "No Slots Available", "Sports Institute System")
    addElement(createServiceTask, "Create Account", "Sports Institute System")
    addElement(createServiceTask, "Link Twitter Account", "Sports Institute System")
    addElement(createServiceTask, "Process Payment", "Sports Institute System")
    addElement(createServiceTask, "Complete Course Registration", "Sports Institute System")

    # University
    addElement(createServiceTask, "Review Activation Request", "University")
    addElement(createServiceTask, "Send Activation Response", "University")

    # Twitter
    addElement(createServiceTask, "Tweet Friends", "Twitter")

    print ""
    print "[" + str(step()) + "] Total elements created: " + str(len(elements))

    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Applicant
        "Start Registration": (0, "Applicant"),
        "Search Courses": (1, "Applicant"),
        "Select Course and Date": (5, "Applicant"),
        "Account Exists?": (6, "Applicant"),
        "Eligible University?": (7, "Applicant"),
        "Register Account": (8, "Applicant"),
        "Request Activation": (8, "Applicant"),
        "Wait for Activation Response": (11, "Applicant"),
        "Activation Approved?": (12, "Applicant"),
        "Activation Rejected": (13, "Applicant"),
        "Log In": (14, "Applicant"),
        "Tweet to Friends?": (16, "Applicant"),
        "Provide Payment Information": (18, "Applicant"),
        "Course Ticket Received": (21, "Applicant"),

        # System
        "Check Slot Availability": (2, "Sports Institute System"),
        "Slots Free?": (3, "Sports Institute System"),
        "Show Courses and Dates": (4, "Sports Institute System"),
        "No Slots Available": (4, "Sports Institute System"),
        "Create Account": (13, "Sports Institute System"),
        "Link Twitter Account": (15, "Sports Institute System"),
        "Process Payment": (19, "Sports Institute System"),
        "Complete Course Registration": (20, "Sports Institute System"),

        # University
        "Review Activation Request": (9, "University"),
        "Send Activation Response": (10, "University"),

        # Twitter
        "Tweet Friends": (17, "Twitter"),
    }

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (AUTO-UNMASK TRIGGER)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(title)
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: " + title

    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    print "[" + str(step()) + "] DiagramHandle obtained"

    # Save triggers Modelio auto-unmask (do NOT unmask manually here)
    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"

    # =========================================================================
    # PHASE 4: WAIT FOR AUTO-UNMASK (AND MANUAL UNMASK FALLBACK)
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

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
        print "[" + str(step()) + "] Trying manual unmask for missing elements (inside correct lane Y)..."
        print ""

        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
        print ""
        print "[" + str(step()) + "] Manual unmask attempted, newly unmasked: " + str(unmaskedCount)

        foundCount = len(elementGraphics)
        if foundCount < len(elements):
            stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
            print "[" + str(step()) + "] WARNING: Still missing after manual unmask: " + ", ".join(stillMissing)
        else:
            print "[" + str(step()) + "] All elements now available after manual unmask"

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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY)"

    print ""
    sortedLayout = []
    for name, (col, laneName) in elementLayout.items():
        sortedLayout.append((col, name, laneName))
    sortedLayout.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedLayout:
        if name not in elementRefs:
            print "[" + str(step()) + "] SKIP layout item not found in refs: " + name
            continue

        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP not in diagram: " + laneName + "/" + name
            continue

        elem = elementRefs[name]
        dg = elementGraphics[name]
        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP no bounds: " + laneName + "/" + name
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)

        elemClass = elem.getMClass().getName()

        # Size policy: tasks have fixed size; keep original for events/gateways
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]

        newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
        try:
            dg.setBounds(newBounds)
            repositionedCount += 1
            diagramHandle.save()
        except Exception as e:
            print "[" + str(step()) + "] ERROR setBounds " + laneName + "/" + name + " : " + str(e)
            continue

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
    # PHASE 6: CREATE FLOWS (GUARDS ON GATEWAY OUTFLOWS)
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Course search and selection
        ("Start Registration", "Search Courses", ""),
        ("Search Courses", "Check Slot Availability", ""),
        ("Check Slot Availability", "Slots Free?", ""),

        # Slots decision (guards MUST be on gateway outflows)
        ("Slots Free?", "Show Courses and Dates", "Yes"),
        ("Slots Free?", "No Slots Available", "No"),

        ("Show Courses and Dates", "Select Course and Date", ""),
        ("Select Course and Date", "Account Exists?", ""),

        # Account exists?
        ("Account Exists?", "Log In", "Yes"),
        ("Account Exists?", "Eligible University?", "No"),

        # Eligible university?
        ("Eligible University?", "Register Account", "Yes"),
        ("Eligible University?", "Request Activation", "No"),

        # Create account (eligible path)
        ("Register Account", "Create Account", ""),

        # Activation path
        ("Request Activation", "Review Activation Request", ""),
        ("Review Activation Request", "Send Activation Response", ""),
        ("Send Activation Response", "Wait for Activation Response", ""),
        ("Wait for Activation Response", "Activation Approved?", ""),

        # Activation approved?
        ("Activation Approved?", "Create Account", "Approved"),
        ("Activation Approved?", "Activation Rejected", "Rejected"),

        # Login and social / payment
        ("Create Account", "Log In", ""),
        ("Log In", "Link Twitter Account", ""),
        ("Link Twitter Account", "Tweet to Friends?", ""),

        # Optional tweet
        ("Tweet to Friends?", "Tweet Friends", "Yes"),
        ("Tweet to Friends?", "Provide Payment Information", "No"),
        ("Tweet Friends", "Provide Payment Information", ""),

        # Payment and completion
        ("Provide Payment Information", "Process Payment", ""),
        ("Process Payment", "Complete Course Registration", ""),
        ("Complete Course Registration", "Course Ticket Received", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if not src or not tgt:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName
            continue
        try:
            f = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(f)
            if guard:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18] + " | guard=" + guard
            else:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18]
        except Exception as e:
            print "[" + str(step()) + "] ERROR creating flow " + srcName + " -> " + tgtName + " : " + str(e)

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

    try:
        diagramHandle.close()
        print ""
        print "[" + str(step()) + "] Diagram closed"
    except Exception as e:
        print ""
        print "[" + str(step()) + "] WARNING: Could not close diagram handle: " + str(e)

    print ""
    print "=================================================================="
    print "COMPLETE"
    print "=================================================================="
    print "Title:    " + title
    print "Process:  " + processName
    print "Lanes:    " + str(len(lanes))
    print "Elements: " + str(len(elements)) + " (" + str(foundCount) + " in diagram graphics)"
    print "Flows:    " + str(len(flows))
    print "=================================================================="

    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createUSICourseRegistrationProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
