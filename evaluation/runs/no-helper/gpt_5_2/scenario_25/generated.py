#
# FindAJobProcess.py
#
# Description:
#   BPMN process diagram: "Find a Job"
#
# Scenario:
#   - You regularly report which companies you applied to
#   - Based on applications, new potential offers are sent to you
#   - Companies confirm receipt and rate the application
#   - Interview can be negotiated
#   - If hired: probation phase
#   - After probation: mutual ratings + company reviews visible only after 1 year
#   - If job becomes permanent, process ends UNLESS applicant rated company "C or less"
#     then applicant continues to receive job offers but no longer has to report
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

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 155
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

    # IMPORTANT: Use guard for conditions on gateway outflows (visible label)
    if guard:
        try:
            flow.setConditionExpression(guard)
        except Exception as e:
            print "  [Flow Guard] WARNING: Could not set guard '" + guard + "': " + str(e)

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
    except Exception as e:
        # Keep silent (polling can spam); return None
        return None
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

    # Lane center Y
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

def createFindAJobProcess(parentPackage):

    processName = "FindAJob_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Find a Job"
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
    print "[" + str(step()) + "] Process created: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    applicantLane = createLane(laneSet, "Applicant")
    companyLane = createLane(laneSet, "Company")
    platformLane = createLane(laneSet, "Platform")

    lanes = {
        "Applicant": applicantLane,
        "Company": companyLane,
        "Platform": platformLane
    }
    laneOrder = ["Applicant", "Company", "Platform"]

    print "[" + str(step()) + "] Lanes: Applicant, Company, Platform"

    # ------------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""

    elements = []
    elementRefs = {}

    def addElement(creator, name, lane, laneName):
        elem = creator(process, name)
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        print "  [Element] " + laneName + ": " + name + " | addToLane=" + str(ok)
        return elem

    # Applicant
    addElement(createStartEvent, "Begin Job Search", applicantLane, "Applicant")
    addElement(createUserTask, "Write Job Applications", applicantLane, "Applicant")
    addElement(createUserTask, "Report Sent Applications", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Interested in Offer?", applicantLane, "Applicant")
    addElement(createUserTask, "Respond to Offer / Request Interview", applicantLane, "Applicant")
    addElement(createUserTask, "Negotiate Interview", applicantLane, "Applicant")
    addElement(createUserTask, "Start Probation Employment", applicantLane, "Applicant")
    addElement(createManualTask, "Work During Probation", applicantLane, "Applicant")
    addElement(createUserTask, "Applicant Rate Company", applicantLane, "Applicant")
    addElement(createUserTask, "Applicant View Reviews", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Applicant Rated <= C?", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Interested in New Offer?", applicantLane, "Applicant")
    addElement(createUserTask, "Respond While Employed", applicantLane, "Applicant")

    # Company
    addElement(createUserTask, "Confirm Application Received", companyLane, "Company")
    addElement(createUserTask, "Rate Application", companyLane, "Company")
    addElement(createExclusiveGateway, "Invite to Interview?", companyLane, "Company")
    addElement(createUserTask, "Conduct Interview", companyLane, "Company")
    addElement(createExclusiveGateway, "Hire Candidate?", companyLane, "Company")
    addElement(createExclusiveGateway, "Probation Passed?", companyLane, "Company")
    addElement(createUserTask, "Become Permanent Employee", companyLane, "Company")
    addElement(createUserTask, "Company Rate Applicant", companyLane, "Company")

    # Platform
    addElement(createServiceTask, "Analyze Applications and Match Offers", platformLane, "Platform")
    addElement(createServiceTask, "Send Potential Job Offers", platformLane, "Platform")
    addElement(createServiceTask, "Store Reviews (Hidden 1 year)", platformLane, "Platform")
    addElement(createManualTask, "Wait 1 year (Reviews hidden)", platformLane, "Platform")
    addElement(createServiceTask, "Publish Reviews", platformLane, "Platform")
    addElement(createServiceTask, "Receive Offers While Employed", platformLane, "Platform")

    # End events
    addElement(createEndEvent, "Permanent Job End", applicantLane, "Applicant")
    addElement(createEndEvent, "Stay Employed End", applicantLane, "Applicant")

    print ""
    print "[" + str(step()) + "] Total elements created: " + str(len(elements))

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

    # Layout: element -> (column, lane)
    elementLayout = {
        # Applicant lane main search
        "Begin Job Search": (0, "Applicant"),
        "Write Job Applications": (1, "Applicant"),
        "Report Sent Applications": (2, "Applicant"),
        "Interested in Offer?": (5, "Applicant"),
        "Respond to Offer / Request Interview": (6, "Applicant"),
        "Negotiate Interview": (10, "Applicant"),
        "Start Probation Employment": (13, "Applicant"),
        "Work During Probation": (14, "Applicant"),
        "Applicant Rate Company": (17, "Applicant"),
        "Applicant View Reviews": (22, "Applicant"),
        "Applicant Rated <= C?": (23, "Applicant"),
        "Interested in New Offer?": (25, "Applicant"),
        "Respond While Employed": (26, "Applicant"),
        "Permanent Job End": (27, "Applicant"),
        "Stay Employed End": (27, "Applicant"),

        # Company lane
        "Confirm Application Received": (7, "Company"),
        "Rate Application": (8, "Company"),
        "Invite to Interview?": (9, "Company"),
        "Conduct Interview": (11, "Company"),
        "Hire Candidate?": (12, "Company"),
        "Probation Passed?": (15, "Company"),
        "Become Permanent Employee": (16, "Company"),
        "Company Rate Applicant": (18, "Company"),

        # Platform lane
        "Analyze Applications and Match Offers": (3, "Platform"),
        "Send Potential Job Offers": (4, "Platform"),
        "Store Reviews (Hidden 1 year)": (19, "Platform"),
        "Wait 1 year (Reviews hidden)": (20, "Platform"),
        "Publish Reviews": (21, "Platform"),
        "Receive Offers While Employed": (24, "Platform"),
    }

    # Also wait for lanes to be ready (bounds needed for centerY)
    waitTargets = []
    waitTargets.extend(elements)
    waitTargets.append(applicantLane)
    waitTargets.append(companyLane)
    waitTargets.append(platformLane)

    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    elementGraphics, attempts = waitForElements(diagramHandle, waitTargets)
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    print ""
    print "[" + str(step()) + "] Wait finished in ~" + str(totalWaitTime) + "ms | graphics found: " + str(foundCount) + "/" + str(len(waitTargets))

    # Check missing for flow elements only (not lanes)
    missingElems = [e.getName() for e in elements if e.getName() not in elementGraphics]
    if len(missingElems) > 0:
        print "[" + str(step()) + "] WARNING: Missing flow elements after wait: " + ", ".join(missingElems)
        print "[" + str(step()) + "] Trying manual unmask fallback (inside correct lane Y)..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
        print ""
        print "[" + str(step()) + "] Manual unmask done. Newly unmasked: " + str(unmaskedCount)
        stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        if len(stillMissing) > 0:
            print "[" + str(step()) + "] WARNING: Still missing: " + ", ".join(stillMissing)
        else:
            print "[" + str(step()) + "] All elements now available after fallback"
    else:
        print "[" + str(step()) + "] All flow elements available (auto-unmask OK)"

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
            print "[" + str(step()) + "] WARNING: No centerY for lane " + laneName

    print ""
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedElements:
        if name not in elementRefs:
            # Not a flow element (could be lane name etc.)
            continue

        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram graphics"
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
        try:
            dg.setBounds(newBounds)
            repositionedCount += 1
            diagramHandle.save()
        except Exception as e:
            print "[" + str(step()) + "] ERROR setting bounds for " + name + ": " + str(e)
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

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Main loop: apply + report + platform offers
        ("Begin Job Search", "Write Job Applications", ""),
        ("Write Job Applications", "Report Sent Applications", ""),
        ("Report Sent Applications", "Analyze Applications and Match Offers", ""),
        ("Analyze Applications and Match Offers", "Send Potential Job Offers", ""),
        ("Send Potential Job Offers", "Interested in Offer?", ""),

        # Interested?
        ("Interested in Offer?", "Write Job Applications", "No"),
        ("Interested in Offer?", "Respond to Offer / Request Interview", "Yes"),

        # Company confirmation + rating
        ("Respond to Offer / Request Interview", "Confirm Application Received", ""),
        ("Confirm Application Received", "Rate Application", ""),
        ("Rate Application", "Invite to Interview?", ""),

        # Invite?
        ("Invite to Interview?", "Send Potential Job Offers", "No"),
        ("Invite to Interview?", "Negotiate Interview", "Yes"),

        # Interview + hire decision
        ("Negotiate Interview", "Conduct Interview", ""),
        ("Conduct Interview", "Hire Candidate?", ""),
        ("Hire Candidate?", "Send Potential Job Offers", "No"),
        ("Hire Candidate?", "Start Probation Employment", "Yes"),

        # Probation
        ("Start Probation Employment", "Work During Probation", ""),
        ("Work During Probation", "Probation Passed?", ""),
        ("Probation Passed?", "Send Potential Job Offers", "No"),
        ("Probation Passed?", "Become Permanent Employee", "Yes"),

        # Mutual ratings + review visibility after 1 year
        ("Become Permanent Employee", "Applicant Rate Company", ""),
        ("Applicant Rate Company", "Company Rate Applicant", ""),
        ("Company Rate Applicant", "Store Reviews (Hidden 1 year)", ""),
        ("Store Reviews (Hidden 1 year)", "Wait 1 year (Reviews hidden)", ""),
        ("Wait 1 year (Reviews hidden)", "Publish Reviews", ""),
        ("Publish Reviews", "Applicant View Reviews", ""),
        ("Applicant View Reviews", "Applicant Rated <= C?", ""),

        # Permanent end unless rated <= C
        ("Applicant Rated <= C?", "Permanent Job End", "No"),
        ("Applicant Rated <= C?", "Receive Offers While Employed", "Yes"),

        # Continue receiving offers (no reporting required)
        ("Receive Offers While Employed", "Interested in New Offer?", ""),
        ("Interested in New Offer?", "Stay Employed End", "No"),
        ("Interested in New Offer?", "Respond While Employed", "Yes"),
        ("Respond While Employed", "Confirm Application Received", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            try:
                f = createSequenceFlow(process, src, tgt, guard=guard)
                flows.append(f)
                if guard:
                    print "  [Flow] " + srcName + " -> " + tgtName + " | guard=" + guard
                else:
                    print "  [Flow] " + srcName + " -> " + tgtName
            except Exception as e:
                print "  [Flow] ERROR creating flow " + srcName + " -> " + tgtName + ": " + str(e)
        else:
            print "  [Flow] WARNING missing element for flow: " + srcName + " -> " + tgtName

    diagramHandle.save()
    print ""
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    print "[" + str(step()) + "] Save"

    # ------------------------------------------------------------------------
    # FINAL STATE
    # ------------------------------------------------------------------------
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
    print "Title:    Find a Job"
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
        createFindAJobProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
