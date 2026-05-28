#
# UniversityEnrollmentProcess.py
#
# Description:
#   BPMN process diagram for a University Enrollment System.
#   Covers: application, document completion loop, parallel evaluation+fee,
#   accept/reject, enrollment confirmation deadline, onboarding (incl. international),
#   semester loop (add/drop, grades, grievance appeal), repeat until graduate/withdraw.
#
# Applicable on: Package
#
# Version: v9.1 - March 2026
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

# Waiting configuration (bigger diagram => allow a bit more time)
WAIT_TIME_MS = 100
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

    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Student"))[1]
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
def createUniversityEnrollmentProcess(parentPackage):

    processName = "UniversityEnrollment_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN UNIVERSITY ENROLLMENT PROCESS - DEBUG LOG"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
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
    print "[" + str(step()) + "] Process: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    # Lane order matters for vertical position
    studentLane = createLane(laneSet, "Student")
    admissionsOfficeLane = createLane(laneSet, "Admissions Office")
    admissionsCommitteeLane = createLane(laneSet, "Admissions Committee")
    financeLane = createLane(laneSet, "Finance")
    itLane = createLane(laneSet, "IT")
    intlLane = createLane(laneSet, "International Office")
    registrarLane = createLane(laneSet, "Registrar")
    advisorLane = createLane(laneSet, "Academic Advisor")
    appealsLane = createLane(laneSet, "Appeals Committee")

    lanes = {
        "Student": studentLane,
        "Admissions Office": admissionsOfficeLane,
        "Admissions Committee": admissionsCommitteeLane,
        "Finance": financeLane,
        "IT": itLane,
        "International Office": intlLane,
        "Registrar": registrarLane,
        "Academic Advisor": advisorLane,
        "Appeals Committee": appealsLane
    }
    laneOrder = [
        "Student",
        "Admissions Office",
        "Admissions Committee",
        "Finance",
        "IT",
        "International Office",
        "Registrar",
        "Academic Advisor",
        "Appeals Committee"
    ]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

    # ------------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""

    elements = []
    elementRefs = {}
    laneCounts = {}
    for ln in laneOrder:
        laneCounts[ln] = 0

    def addElement(creator, name, laneName):
        lane = lanes[laneName]
        elem = creator(process, name)
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        laneCounts[laneName] = laneCounts.get(laneName, 0) + 1
        if not ok:
            print "  WARNING: addToLane failed for " + name + " -> " + laneName
        return elem

    # Application and document completion loop
    addElement(createStartEvent, "Application Submitted", "Student")
    addElement(createUserTask, "Review Application", "Admissions Office")
    addElement(createExclusiveGateway, "Documents Complete?", "Admissions Office")
    addElement(createServiceTask, "Notify Missing Documents", "Admissions Office")
    addElement(createUserTask, "Provide Missing Documents", "Student")

    # Parallel: evaluation and fee processing
    addElement(createParallelGateway, "Eval+Fee Split", "Admissions Office")
    addElement(createUserTask, "Evaluate Application", "Admissions Committee")
    addElement(createServiceTask, "Process Application Fee/Waiver", "Finance")
    addElement(createParallelGateway, "Eval+Fee Join", "Admissions Office")

    # Decision: accepted?
    addElement(createExclusiveGateway, "Accepted?", "Admissions Committee")
    addElement(createServiceTask, "Send Acceptance Letter", "Admissions Office")
    addElement(createMessageEndEvent, "Rejection Letter Sent", "Admissions Office")

    # Confirmation deadline
    addElement(createUserTask, "Confirm Enrollment", "Student")
    addElement(createExclusiveGateway, "Confirmed By Deadline?", "Student")
    addElement(createEndEvent, "Application Canceled", "Student")

    # Onboarding parallel work + conditional international branch
    addElement(createParallelGateway, "Onboarding Split", "Student")
    addElement(createUserTask, "Receive Orientation Materials", "Student")
    addElement(createServiceTask, "Set Up Student Accounts", "IT")
    addElement(createExclusiveGateway, "International Student?", "International Office")
    addElement(createUserTask, "Assist with Visa Processing", "International Office")
    addElement(createParallelGateway, "Onboarding Join", "Student")

    # Start of studies
    addElement(createUserTask, "Issue Student ID Card", "Registrar")
    addElement(createUserTask, "Meet Academic Advisor", "Academic Advisor")
    addElement(createUserTask, "Select Courses", "Student")
    addElement(createUserTask, "Resolve Schedule Conflicts", "Student")
    addElement(createManualTask, "Attend Classes", "Student")

    # Semester cycle
    addElement(createUserTask, "Add/Drop Courses", "Student")
    addElement(createServiceTask, "Post Grades", "Registrar")
    addElement(createUserTask, "Review Grades Online", "Student")
    addElement(createExclusiveGateway, "Grievance?", "Student")
    addElement(createUserTask, "Submit Appeal Form", "Student")
    addElement(createUserTask, "Meet Appeals Committee", "Appeals Committee")
    addElement(createUserTask, "Await Appeal Decision", "Student")
    addElement(createExclusiveGateway, "Continue Studies?", "Student")
    addElement(createEndEvent, "Graduated", "Student")
    addElement(createEndEvent, "Withdrawn", "Student")

    for ln in laneOrder:
        print "[" + str(step()) + "] " + ln + " lane: " + str(laneCounts[ln]) + " elements"

    print ""
    print "  Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # ------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        # Application intake
        "Application Submitted": (0, "Student"),
        "Review Application": (1, "Admissions Office"),
        "Documents Complete?": (2, "Admissions Office"),
        "Notify Missing Documents": (3, "Admissions Office"),
        "Provide Missing Documents": (4, "Student"),

        # Parallel evaluation + fee
        "Eval+Fee Split": (5, "Admissions Office"),
        "Evaluate Application": (6, "Admissions Committee"),
        "Process Application Fee/Waiver": (6, "Finance"),
        "Eval+Fee Join": (7, "Admissions Office"),

        # Accept/reject
        "Accepted?": (8, "Admissions Committee"),
        "Send Acceptance Letter": (9, "Admissions Office"),
        "Rejection Letter Sent": (9, "Admissions Office"),

        # Confirmation
        "Confirm Enrollment": (10, "Student"),
        "Confirmed By Deadline?": (11, "Student"),
        "Application Canceled": (12, "Student"),

        # Onboarding
        "Onboarding Split": (12, "Student"),
        "Receive Orientation Materials": (13, "Student"),
        "Set Up Student Accounts": (13, "IT"),
        "International Student?": (13, "International Office"),
        "Assist with Visa Processing": (14, "International Office"),
        "Onboarding Join": (15, "Student"),

        # Start studies
        "Issue Student ID Card": (16, "Registrar"),
        "Meet Academic Advisor": (17, "Academic Advisor"),
        "Select Courses": (18, "Student"),
        "Resolve Schedule Conflicts": (19, "Student"),
        "Attend Classes": (20, "Student"),

        # Semester loop
        "Add/Drop Courses": (21, "Student"),
        "Post Grades": (22, "Registrar"),
        "Review Grades Online": (23, "Student"),
        "Grievance?": (24, "Student"),
        "Submit Appeal Form": (25, "Student"),
        "Meet Appeals Committee": (26, "Appeals Committee"),
        "Await Appeal Decision": (27, "Student"),
        "Continue Studies?": (28, "Student"),
        "Graduated": (29, "Student"),
        "Withdrawn": (29, "Student")
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

    # ------------------------------------------------------------------------
    # PHASE 5: REPOSITION ELEMENTS
    # ------------------------------------------------------------------------
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
    for name, (col, ln) in elementLayout.items():
        sortedElements.append((col, name, ln))
    sortedElements.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, ln in sortedElements:
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
        targetY = laneY.get(ln, 100)

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

        print "[" + str(step()) + "] " + ln + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (USE GUARDS FOR GATEWAY OUTFLOWS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Application intake
        ("Application Submitted", "Review Application", ""),
        ("Review Application", "Documents Complete?", ""),

        # Documents complete?
        ("Documents Complete?", "Notify Missing Documents", "No"),
        ("Notify Missing Documents", "Provide Missing Documents", ""),
        ("Provide Missing Documents", "Review Application", ""),
        ("Documents Complete?", "Eval+Fee Split", "Yes"),

        # Parallel evaluation and fee
        ("Eval+Fee Split", "Evaluate Application", ""),
        ("Eval+Fee Split", "Process Application Fee/Waiver", ""),
        ("Evaluate Application", "Eval+Fee Join", ""),
        ("Process Application Fee/Waiver", "Eval+Fee Join", ""),

        # Accepted?
        ("Eval+Fee Join", "Accepted?", ""),
        ("Accepted?", "Send Acceptance Letter", "Accepted"),
        ("Accepted?", "Rejection Letter Sent", "Rejected"),

        # Confirmation deadline
        ("Send Acceptance Letter", "Confirm Enrollment", ""),
        ("Confirm Enrollment", "Confirmed By Deadline?", ""),
        ("Confirmed By Deadline?", "Application Canceled", "No"),
        ("Confirmed By Deadline?", "Onboarding Split", "Yes"),

        # Onboarding parallel
        ("Onboarding Split", "Receive Orientation Materials", ""),
        ("Onboarding Split", "Set Up Student Accounts", ""),
        ("Onboarding Split", "International Student?", ""),

        # International branch (conditional path to join)
        ("International Student?", "Assist with Visa Processing", "Yes"),
        ("International Student?", "Onboarding Join", "No"),
        ("Assist with Visa Processing", "Onboarding Join", ""),

        # Join onboarding
        ("Receive Orientation Materials", "Onboarding Join", ""),
        ("Set Up Student Accounts", "Onboarding Join", ""),

        # Start studies
        ("Onboarding Join", "Issue Student ID Card", ""),
        ("Issue Student ID Card", "Meet Academic Advisor", ""),
        ("Meet Academic Advisor", "Select Courses", ""),
        ("Select Courses", "Resolve Schedule Conflicts", ""),
        ("Resolve Schedule Conflicts", "Attend Classes", ""),

        # Semester loop core
        ("Attend Classes", "Add/Drop Courses", ""),
        ("Add/Drop Courses", "Post Grades", ""),
        ("Post Grades", "Review Grades Online", ""),
        ("Review Grades Online", "Grievance?", ""),

        # Grievance?
        ("Grievance?", "Submit Appeal Form", "Yes"),
        ("Grievance?", "Continue Studies?", "No"),

        # Appeal
        ("Submit Appeal Form", "Meet Appeals Committee", ""),
        ("Meet Appeals Committee", "Await Appeal Decision", ""),
        ("Await Appeal Decision", "Continue Studies?", ""),

        # Repeat until graduate or withdraw
        ("Continue Studies?", "Add/Drop Courses", "Next Semester"),
        ("Continue Studies?", "Graduated", "Graduate"),
        ("Continue Studies?", "Withdrawn", "Withdraw")
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
        createUniversityEnrollmentProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
