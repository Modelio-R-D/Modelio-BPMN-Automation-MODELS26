#
# WorkAndLiveInAustria.py
#
# Description:
#   BPMN process diagram: "Work and Live in Austria"
#   Covers combined steps for accommodation + bank negotiation and visa / Rot-Weiss-Rot Card,
#   including general visa requirements and a renewal cycle (every X months).
#
# Applicable on: Package
#
# Version: 1.0 - March 2026
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
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
SPACING = 155
START_X = 80

# Task dimensions
TASK_WIDTH = 170
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

def createTimerStartEvent(process, name):
    """
    Timer start event for periodic trigger (e.g., renewal every X months).
    Note: Some Modelio versions require a TimerEventDefinition object.
    This function tries to create it, but remains valid even if definition creation fails.
    """
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        # Keep event as a normal start event if timer definition is unavailable
        pass
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
    if guard:
        # IMPORTANT: Use Guard/ConditionExpression to show labels from gateways
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
            parts.append(name[:14] + "=Y" + str(int(bounds["y"])))
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
    """
    CRITICAL: Must unmask at Y position INSIDE the correct lane.
    """
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
def createWorkAndLiveInAustriaProcess(parentPackage):

    processName = "WorkAndLiveInAustria_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Work and Live in Austria"
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

    applicantLane = createLane(laneSet, "Applicant")
    employerLane = createLane(laneSet, "Employer HR")
    housingBankLane = createLane(laneSet, "Housing and Bank")
    authorityLane = createLane(laneSet, "Austrian Authorities")
    renewalLane = createLane(laneSet, "Applicant Renewal")

    lanes = {
        "Applicant": applicantLane,
        "Employer HR": employerLane,
        "Housing and Bank": housingBankLane,
        "Austrian Authorities": authorityLane,
        "Applicant Renewal": renewalLane
    }
    laneOrder = ["Applicant", "Employer HR", "Housing and Bank", "Austrian Authorities", "Applicant Renewal"]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

    # ------------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # ------------------------------------------------------------------------
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
            print "  [WARN] addToLane failed for: " + name + " -> " + lane.getName()
        return elem

    # Applicant main path
    addElement(createStartEvent, "Plan Move", applicantLane)
    addElement(createUserTask, "Check Requirements", applicantLane)

    # Employer / HR
    addElement(createUserTask, "Get Job Offer", employerLane)
    addElement(createUserTask, "Collect Employer Documents", employerLane)

    # Decide / authority competence
    addElement(createUserTask, "Determine Visa Type (D / RWR)", applicantLane)
    addElement(createServiceTask, "Identify Competent Representation", authorityLane)

    # Combined preparations (parallel)
    addElement(createParallelGateway, "Prepare Move (Parallel)", applicantLane)

    # Housing and bank
    addElement(createUserTask, "Negotiate Accommodation", housingBankLane)
    addElement(createUserTask, "Open Bank Account", housingBankLane)

    # Document gathering + core visa requirements (parallel)
    addElement(createUserTask, "Gather Documents", applicantLane)
    addElement(createParallelGateway, "Prepare Core Docs (Parallel)", applicantLane)

    addElement(createUserTask, "Travel Document Validity Check", applicantLane)
    addElement(createUserTask, "Get Passport Photo 35x45", applicantLane)
    addElement(createUserTask, "Buy Health Insurance 30k Schengen", applicantLane)
    addElement(createUserTask, "Prove Means of Subsistence", applicantLane)
    addElement(createUserTask, "Collect Other Evidence (Bookings etc.)", applicantLane)

    addElement(createParallelGateway, "Core Docs Ready (Join)", applicantLane)
    addElement(createUserTask, "Fill Visa Application Form", applicantLane)

    # Authority check (separate but in same preparation window)
    addElement(createServiceTask, "Check Refusal Grounds and Schengen Rules", authorityLane)

    addElement(createParallelGateway, "Ready to Apply (Join)", applicantLane)

    # Submit and decision loop
    addElement(createUserTask, "Submit Application at Representation", authorityLane)
    addElement(createExclusiveGateway, "Documents Complete?", authorityLane)
    addElement(createUserTask, "Request Additional Evidence", authorityLane)
    addElement(createServiceTask, "Process Visa / Rot-Weiss-Rot Card", authorityLane)
    addElement(createExclusiveGateway, "Approved?", authorityLane)

    # After approval
    addElement(createUserTask, "Book Travel and Appointment", applicantLane)
    addElement(createManualTask, "Register Residence (Meldezettel)", applicantLane)
    addElement(createEndEvent, "Working and Living in Austria", applicantLane)

    # Rejection end
    addElement(createEndEvent, "Visa Refused", authorityLane)

    # Renewal cycle (every X months)
    addElement(createTimerStartEvent, "Renewal Due (every X months)", renewalLane)
    addElement(createUserTask, "Prepare Renewal Documents", renewalLane)
    addElement(createUserTask, "Submit Renewal", authorityLane)
    addElement(createServiceTask, "Process Renewal", authorityLane)
    addElement(createExclusiveGateway, "Renewal Approved?", authorityLane)
    addElement(createMessageEndEvent, "RWR Card Renewed", renewalLane)
    addElement(createEndEvent, "Permit Ends", renewalLane)

    # Phase 2 summary
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("Work and Live in Austria")
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: Work and Live in Austria"

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

    # Layout: element name -> (column_index, lane_name)
    elementLayout = {
        # Main path
        "Plan Move": (0, "Applicant"),
        "Check Requirements": (1, "Applicant"),
        "Get Job Offer": (2, "Employer HR"),
        "Collect Employer Documents": (3, "Employer HR"),
        "Determine Visa Type (D / RWR)": (4, "Applicant"),
        "Identify Competent Representation": (5, "Austrian Authorities"),

        "Prepare Move (Parallel)": (6, "Applicant"),

        "Negotiate Accommodation": (7, "Housing and Bank"),
        "Open Bank Account": (8, "Housing and Bank"),

        "Gather Documents": (7, "Applicant"),
        "Prepare Core Docs (Parallel)": (8, "Applicant"),
        "Travel Document Validity Check": (9, "Applicant"),
        "Get Passport Photo 35x45": (9, "Applicant"),
        "Buy Health Insurance 30k Schengen": (10, "Applicant"),
        "Prove Means of Subsistence": (10, "Applicant"),
        "Collect Other Evidence (Bookings etc.)": (11, "Applicant"),
        "Core Docs Ready (Join)": (12, "Applicant"),
        "Fill Visa Application Form": (13, "Applicant"),

        "Check Refusal Grounds and Schengen Rules": (12, "Austrian Authorities"),

        "Ready to Apply (Join)": (14, "Applicant"),
        "Submit Application at Representation": (15, "Austrian Authorities"),
        "Documents Complete?": (16, "Austrian Authorities"),
        "Request Additional Evidence": (17, "Austrian Authorities"),
        "Process Visa / Rot-Weiss-Rot Card": (18, "Austrian Authorities"),
        "Approved?": (19, "Austrian Authorities"),

        "Book Travel and Appointment": (20, "Applicant"),
        "Register Residence (Meldezettel)": (21, "Applicant"),
        "Working and Living in Austria": (22, "Applicant"),

        "Visa Refused": (20, "Austrian Authorities"),

        # Renewal cycle lane
        "Renewal Due (every X months)": (16, "Applicant Renewal"),
        "Prepare Renewal Documents": (17, "Applicant Renewal"),
        "Submit Renewal": (18, "Austrian Authorities"),
        "Process Renewal": (19, "Austrian Authorities"),
        "Renewal Approved?": (20, "Austrian Authorities"),
        "RWR Card Renewed": (21, "Applicant Renewal"),
        "Permit Ends": (21, "Applicant Renewal"),
    }

    # Wait for elements AND lanes (lanes needed for bounds)
    waitItems = []
    for ln in laneOrder:
        waitItems.append(lanes[ln])
    for e in elements:
        waitItems.append(e)

    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    graphicsMap, attempts = waitForElements(diagramHandle, waitItems)
    totalWaitTime = attempts * WAIT_TIME_MS

    # Split out node graphics (keep same map, just use names)
    foundCount = 0
    for e in elements:
        if e.getName() in graphicsMap:
            foundCount += 1

    if foundCount == len(elements):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in elements if e.getName() not in graphicsMap]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)

        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing elements..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, graphicsMap, lanes, elementLayout)

        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"

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
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    repositionedCount = 0

    for col, name, laneName in sortedElements:
        elem = elementRefs.get(name)
        if not elem:
            # Not a node element (could be duplicated name mismatch); skip
            continue

        if name not in graphicsMap:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram graphics"
            continue

        dg = graphicsMap[name]
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
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Main path
        ("Plan Move", "Check Requirements", ""),
        ("Check Requirements", "Get Job Offer", ""),
        ("Get Job Offer", "Collect Employer Documents", ""),
        ("Collect Employer Documents", "Determine Visa Type (D / RWR)", ""),
        ("Determine Visa Type (D / RWR)", "Identify Competent Representation", ""),
        ("Identify Competent Representation", "Prepare Move (Parallel)", ""),

        # Parallel preparation branches
        ("Prepare Move (Parallel)", "Negotiate Accommodation", ""),
        ("Negotiate Accommodation", "Open Bank Account", ""),
        ("Open Bank Account", "Ready to Apply (Join)", ""),

        ("Prepare Move (Parallel)", "Gather Documents", ""),
        ("Gather Documents", "Prepare Core Docs (Parallel)", ""),

        # Core docs split (parallel tasks)
        ("Prepare Core Docs (Parallel)", "Travel Document Validity Check", ""),
        ("Prepare Core Docs (Parallel)", "Get Passport Photo 35x45", ""),
        ("Prepare Core Docs (Parallel)", "Buy Health Insurance 30k Schengen", ""),
        ("Prepare Core Docs (Parallel)", "Prove Means of Subsistence", ""),
        ("Prepare Core Docs (Parallel)", "Collect Other Evidence (Bookings etc.)", ""),

        # Join core docs
        ("Travel Document Validity Check", "Core Docs Ready (Join)", ""),
        ("Get Passport Photo 35x45", "Core Docs Ready (Join)", ""),
        ("Buy Health Insurance 30k Schengen", "Core Docs Ready (Join)", ""),
        ("Prove Means of Subsistence", "Core Docs Ready (Join)", ""),
        ("Collect Other Evidence (Bookings etc.)", "Core Docs Ready (Join)", ""),

        ("Core Docs Ready (Join)", "Fill Visa Application Form", ""),
        ("Fill Visa Application Form", "Ready to Apply (Join)", ""),

        # Authority check during prep
        ("Prepare Move (Parallel)", "Check Refusal Grounds and Schengen Rules", ""),
        ("Check Refusal Grounds and Schengen Rules", "Ready to Apply (Join)", ""),

        # Submit and review
        ("Ready to Apply (Join)", "Submit Application at Representation", ""),
        ("Submit Application at Representation", "Documents Complete?", ""),

        # Gateway with guards
        ("Documents Complete?", "Request Additional Evidence", "No"),
        ("Documents Complete?", "Process Visa / Rot-Weiss-Rot Card", "Yes"),

        # Evidence loop
        ("Request Additional Evidence", "Collect Other Evidence (Bookings etc.)", ""),

        # Decision
        ("Process Visa / Rot-Weiss-Rot Card", "Approved?", ""),
        ("Approved?", "Visa Refused", "No"),
        ("Approved?", "Book Travel and Appointment", "Yes"),

        # After approval
        ("Book Travel and Appointment", "Register Residence (Meldezettel)", ""),
        ("Register Residence (Meldezettel)", "Working and Living in Austria", ""),

        # Renewal cycle (separate timer-triggered start)
        ("Renewal Due (every X months)", "Prepare Renewal Documents", ""),
        ("Prepare Renewal Documents", "Submit Renewal", ""),
        ("Submit Renewal", "Process Renewal", ""),
        ("Process Renewal", "Renewal Approved?", ""),
        ("Renewal Approved?", "RWR Card Renewed", "Yes"),
        ("Renewal Approved?", "Permit Ends", "No"),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + str(srcName) + " -> " + str(tgtName)

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
        createWorkAndLiveInAustriaProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
