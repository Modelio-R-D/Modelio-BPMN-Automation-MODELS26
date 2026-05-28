#
# ComplianceAuditCertificationProcess.py
#
# Description:
#   BPMN process diagram for Compliance Audit and Certification workflow.
#
# Process Summary:
#   - Starts when a company schedules a compliance audit (timer start)
#   - Internal teams prepare documentation, gather evidence, self-assess
#   - Auditors review processes and identify gaps
#   - If gaps: company corrects issues
#   - Final audit is conducted
#   - If criteria met: certification awarded and official documents issued (message end)
#   - If not met: company improves processes and repeats final audit
#
# Applicable on: Package
#
# Version: 9.2 - March 2026
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
SCRIPT_VERSION = "v9.2"
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
    """
    Assign an element to a lane.
    IMPORTANT: required for proper placement/visibility in lanes.
    """
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
    Timer Start Event (clock icon).
    Implementation uses a StartEvent + TimerEventDefinition when available.
    """
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        # If definition type not available in this Modelio version, keep plain start event.
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


def createSequenceFlow(process, source, target, name="", guard=""):
    """
    IMPORTANT: For flows from gateways, use guard (ConditionExpression) so the
    label appears on the arrow in Modelio.
    """
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    if guard:
        flow.setConditionExpression(guard)
    return flow


def createSequenceFlowWithGuard(process, source, target, guardText):
    return createSequenceFlow(process, source, target, guard=guardText)

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
    """
    Manual unmask fallback.
    CRITICAL: unmask at a Y position inside the correct lane.
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
            laneName = elementLayout.get(name, (0, "Company"))[1]
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

def createComplianceAuditCertificationProcess(parentPackage):
    processName = "ComplianceAuditCertification_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN COMPLIANCE AUDIT AND CERTIFICATION - DEBUG LOG"
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

    companyLane = createLane(laneSet, "Company")
    auditorLane = createLane(laneSet, "Auditor")
    certBodyLane = createLane(laneSet, "Certification Body")

    lanes = {
        "Company": companyLane,
        "Auditor": auditorLane,
        "Certification Body": certBodyLane
    }
    laneOrder = ["Company", "Auditor", "Certification Body"]

    print "[" + str(step()) + "] Lanes: Company, Auditor, Certification Body"

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
        print "  [Element] " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    # Company
    addElement(createTimerStartEvent, "Audit Scheduled", companyLane)
    addElement(createUserTask, "Prepare Documentation", companyLane)
    addElement(createUserTask, "Gather Evidence", companyLane)
    addElement(createUserTask, "Conduct Self-Assessment", companyLane)
    addElement(createUserTask, "Implement Corrections", companyLane)
    addElement(createUserTask, "Improve Processes", companyLane)

    # Auditor
    addElement(createUserTask, "Review Company Processes", auditorLane)
    addElement(createUserTask, "Identify Gaps and Issues", auditorLane)
    addElement(createExclusiveGateway, "Gaps Found?", auditorLane)
    addElement(createUserTask, "Conduct Final Audit", auditorLane)
    addElement(createExclusiveGateway, "Criteria Met?", auditorLane)

    # Certification Body
    addElement(createServiceTask, "Award Certification", certBodyLane)
    addElement(createServiceTask, "Issue Official Documents", certBodyLane)
    addElement(createMessageEndEvent, "Certification Issued", certBodyLane)

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
    # PHASE 4: WAIT FOR AUTO-UNMASK (NO INITIAL UNMASK CALL)
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        "Audit Scheduled": (0, "Company"),
        "Prepare Documentation": (1, "Company"),
        "Gather Evidence": (2, "Company"),
        "Conduct Self-Assessment": (3, "Company"),

        "Review Company Processes": (4, "Auditor"),
        "Identify Gaps and Issues": (5, "Auditor"),
        "Gaps Found?": (6, "Auditor"),

        "Implement Corrections": (7, "Company"),
        "Conduct Final Audit": (8, "Auditor"),
        "Criteria Met?": (9, "Auditor"),

        "Improve Processes": (10, "Company"),

        "Award Certification": (11, "Certification Body"),
        "Issue Official Documents": (12, "Certification Body"),
        "Certification Issued": (13, "Certification Body")
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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY)"

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
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # =========================================================================
    # PHASE 6: CREATE FLOWS (GUARDS ON GATEWAY OUTFLOWS)
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Audit Scheduled", "Prepare Documentation", ""),
        ("Prepare Documentation", "Gather Evidence", ""),
        ("Gather Evidence", "Conduct Self-Assessment", ""),

        ("Conduct Self-Assessment", "Review Company Processes", ""),
        ("Review Company Processes", "Identify Gaps and Issues", ""),
        ("Identify Gaps and Issues", "Gaps Found?", ""),

        # From gateway: guards must be condition expression
        ("Gaps Found?", "Implement Corrections", "Yes"),
        ("Gaps Found?", "Conduct Final Audit", "No"),

        ("Implement Corrections", "Conduct Final Audit", ""),

        ("Conduct Final Audit", "Criteria Met?", ""),

        # From gateway: guards must be condition expression
        ("Criteria Met?", "Award Certification", "Yes"),
        ("Criteria Met?", "Improve Processes", "No"),

        ("Improve Processes", "Conduct Final Audit", ""),

        ("Award Certification", "Issue Official Documents", ""),
        ("Issue Official Documents", "Certification Issued", "")
    ]

    flows = []
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
            print "  [Flow] WARNING: missing element for " + srcName + " -> " + tgtName

    print ""
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
        createComplianceAuditCertificationProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
