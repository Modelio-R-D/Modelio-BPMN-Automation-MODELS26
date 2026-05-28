#
# AnnualAuditProcess.py
#
# Description:
#   BPMN process diagram for a multinational company's annual audit process.
#   Lanes:
#     - Audit Coordinator
#     - Regional Office
#     - Compliance Team
#     - Central Audit Team
#     - Audit Director
#     - Executive Board
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

# Waiting configuration (auto-unmask)
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 140
START_X = 70

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
        print "  [addToLane] ERROR: " + element.getName() + " -> " + lane.getName() + " | " + str(e)
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
        except Exception as e:
            print "  [FlowGuard] WARNING: Could not set guard='" + guard + "' on flow " + source.getName() + " -> " + target.getName() + " | " + str(e)
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
        # Keep quiet here; wait loop will log missing elements anyway
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
        else:
            print "  [Unmask] WARNING: No bounds for lane " + laneName

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Central Audit Team"))[1]
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
def createAnnualAuditProcess(parentPackage):

    processName = "AnnualAudit_" + EXECUTION_ID
    stepCounter = [0]
    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN ANNUAL AUDIT PROCESS - DEBUG LOG"
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

    auditCoordinatorLane = createLane(laneSet, "Audit Coordinator")
    regionalOfficeLane = createLane(laneSet, "Regional Office")
    complianceTeamLane = createLane(laneSet, "Compliance Team")
    centralAuditTeamLane = createLane(laneSet, "Central Audit Team")
    auditDirectorLane = createLane(laneSet, "Audit Director")
    executiveBoardLane = createLane(laneSet, "Executive Board")

    lanes = {
        "Audit Coordinator": auditCoordinatorLane,
        "Regional Office": regionalOfficeLane,
        "Compliance Team": complianceTeamLane,
        "Central Audit Team": centralAuditTeamLane,
        "Audit Director": auditDirectorLane,
        "Executive Board": executiveBoardLane
    }
    laneOrder = [
        "Audit Coordinator",
        "Regional Office",
        "Compliance Team",
        "Central Audit Team",
        "Audit Director",
        "Executive Board"
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

    def addElement(creator, name, laneName):
        lane = lanes[laneName]
        elem = creator(process, name)
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        print "  [Element] " + laneName + " / " + name + " | addToLane=" + str(ok)
        return elem

    # Audit Coordinator
    addElement(createStartEvent, "Annual Audit Start", "Audit Coordinator")
    addElement(createServiceTask, "Send Audit Notification", "Audit Coordinator")
    addElement(createParallelGateway, "Start Prep And Compliance (Split)", "Audit Coordinator")

    # Regional Office
    addElement(createUserTask, "Prepare Financial Statements", "Regional Office")
    addElement(createUserTask, "Gather Supporting Documents", "Regional Office")
    addElement(createUserTask, "Submit Documents To Central Audit", "Regional Office")
    addElement(createUserTask, "Provide Clarifications", "Regional Office")

    # Compliance Team
    addElement(createUserTask, "Check Regulatory Updates", "Compliance Team")
    addElement(createServiceTask, "Send Regulatory Updates To Audit Team", "Compliance Team")

    # Central Audit Team
    addElement(createParallelGateway, "Prep And Compliance (Join)", "Central Audit Team")
    addElement(createUserTask, "Review Submission", "Central Audit Team")
    addElement(createExclusiveGateway, "Discrepancies Found?", "Central Audit Team")
    addElement(createUserTask, "Request Clarifications", "Central Audit Team")

    addElement(createUserTask, "Conduct Risk Assessment", "Central Audit Team")
    addElement(createParallelGateway, "Assess Risks (Split)", "Central Audit Team")
    addElement(createServiceTask, "Evaluate Financial Risks", "Central Audit Team")
    addElement(createServiceTask, "Evaluate Operational Risks", "Central Audit Team")
    addElement(createServiceTask, "Evaluate Compliance Risks", "Central Audit Team")
    addElement(createParallelGateway, "Assess Risks (Join)", "Central Audit Team")
    addElement(createExclusiveGateway, "High Risk Identified?", "Central Audit Team")

    addElement(createUserTask, "Launch Detailed Investigation", "Central Audit Team")
    addElement(createParallelGateway, "Investigation (Split)", "Central Audit Team")
    addElement(createServiceTask, "Perform Data Analysis", "Central Audit Team")
    addElement(createUserTask, "Conduct Interviews", "Central Audit Team")
    addElement(createParallelGateway, "Investigation (Join)", "Central Audit Team")
    addElement(createExclusiveGateway, "Site Visit Needed?", "Central Audit Team")
    addElement(createManualTask, "Conduct Site Visit", "Central Audit Team")
    addElement(createExclusiveGateway, "Site Visit (Merge)", "Central Audit Team")

    addElement(createUserTask, "Address Risks", "Central Audit Team")
    addElement(createUserTask, "Compile Audit Report", "Central Audit Team")
    addElement(createUserTask, "Update Audit Report", "Central Audit Team")

    addElement(createParallelGateway, "Distribute And Archive (Split)", "Central Audit Team")
    addElement(createServiceTask, "Distribute Final Report", "Central Audit Team")
    addElement(createServiceTask, "Archive Final Report", "Central Audit Team")
    addElement(createParallelGateway, "Distribute And Archive (Join)", "Central Audit Team")
    addElement(createEndEvent, "Audit Closed", "Central Audit Team")

    # Audit Director
    addElement(createUserTask, "Review Audit Report (Director)", "Audit Director")
    addElement(createExclusiveGateway, "Report Approved?", "Audit Director")

    # Executive Board
    addElement(createManualTask, "Receive Final Report (Board)", "Executive Board")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (AUTO-UNMASK)
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
        # Coordinator
        "Annual Audit Start": (0, "Audit Coordinator"),
        "Send Audit Notification": (1, "Audit Coordinator"),
        "Start Prep And Compliance (Split)": (2, "Audit Coordinator"),

        # Parallel work
        "Prepare Financial Statements": (3, "Regional Office"),
        "Gather Supporting Documents": (4, "Regional Office"),
        "Submit Documents To Central Audit": (6, "Regional Office"),

        "Check Regulatory Updates": (3, "Compliance Team"),
        "Send Regulatory Updates To Audit Team": (5, "Compliance Team"),

        # Join and review
        "Prep And Compliance (Join)": (7, "Central Audit Team"),
        "Review Submission": (8, "Central Audit Team"),
        "Discrepancies Found?": (9, "Central Audit Team"),
        "Request Clarifications": (10, "Central Audit Team"),
        "Provide Clarifications": (11, "Regional Office"),

        # Risk assessment
        "Conduct Risk Assessment": (12, "Central Audit Team"),
        "Assess Risks (Split)": (13, "Central Audit Team"),
        "Evaluate Financial Risks": (14, "Central Audit Team"),
        "Evaluate Operational Risks": (14, "Central Audit Team"),
        "Evaluate Compliance Risks": (14, "Central Audit Team"),
        "Assess Risks (Join)": (15, "Central Audit Team"),
        "High Risk Identified?": (16, "Central Audit Team"),

        # Investigation
        "Launch Detailed Investigation": (17, "Central Audit Team"),
        "Investigation (Split)": (18, "Central Audit Team"),
        "Perform Data Analysis": (19, "Central Audit Team"),
        "Conduct Interviews": (19, "Central Audit Team"),
        "Investigation (Join)": (20, "Central Audit Team"),
        "Site Visit Needed?": (21, "Central Audit Team"),
        "Conduct Site Visit": (22, "Central Audit Team"),
        "Site Visit (Merge)": (23, "Central Audit Team"),

        # Wrap up
        "Address Risks": (24, "Central Audit Team"),
        "Compile Audit Report": (25, "Central Audit Team"),

        # Director review loop
        "Review Audit Report (Director)": (26, "Audit Director"),
        "Report Approved?": (27, "Audit Director"),
        "Update Audit Report": (28, "Central Audit Team"),

        # Distribution and archive
        "Distribute And Archive (Split)": (29, "Central Audit Team"),
        "Distribute Final Report": (30, "Central Audit Team"),
        "Receive Final Report (Board)": (31, "Executive Board"),
        "Archive Final Report": (30, "Central Audit Team"),
        "Distribute And Archive (Join)": (32, "Central Audit Team"),
        "Audit Closed": (33, "Central Audit Team"),
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

    # ------------------------------------------------------------------------
    # PHASE 5: REPOSITION ELEMENTS
    # ------------------------------------------------------------------------
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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (default Y=100)"

    print ""
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedElements:
        if name not in elementRefs:
            print "[" + str(step()) + "] SKIP " + name + ": not found in elementRefs"
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
            print "[" + str(step()) + "] ERROR reposition " + laneName + "/" + name + ": " + str(e)
            continue

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged

        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE SEQUENCE FLOWS (WITH GUARDS FROM GATEWAYS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Annual Audit Start", "Send Audit Notification", ""),
        ("Send Audit Notification", "Start Prep And Compliance (Split)", ""),

        # Parallel branch A - Regional Office
        ("Start Prep And Compliance (Split)", "Prepare Financial Statements", ""),
        ("Prepare Financial Statements", "Gather Supporting Documents", ""),
        ("Gather Supporting Documents", "Submit Documents To Central Audit", ""),

        # Parallel branch B - Compliance
        ("Start Prep And Compliance (Split)", "Check Regulatory Updates", ""),
        ("Check Regulatory Updates", "Send Regulatory Updates To Audit Team", ""),

        # Join
        ("Submit Documents To Central Audit", "Prep And Compliance (Join)", ""),
        ("Send Regulatory Updates To Audit Team", "Prep And Compliance (Join)", ""),

        # Review and discrepancies loop
        ("Prep And Compliance (Join)", "Review Submission", ""),
        ("Review Submission", "Discrepancies Found?", ""),
        ("Discrepancies Found?", "Request Clarifications", "Yes"),
        ("Request Clarifications", "Provide Clarifications", ""),
        ("Provide Clarifications", "Review Submission", ""),
        ("Discrepancies Found?", "Conduct Risk Assessment", "No"),

        # Risk assessment parallel evaluations
        ("Conduct Risk Assessment", "Assess Risks (Split)", ""),
        ("Assess Risks (Split)", "Evaluate Financial Risks", ""),
        ("Assess Risks (Split)", "Evaluate Operational Risks", ""),
        ("Assess Risks (Split)", "Evaluate Compliance Risks", ""),
        ("Evaluate Financial Risks", "Assess Risks (Join)", ""),
        ("Evaluate Operational Risks", "Assess Risks (Join)", ""),
        ("Evaluate Compliance Risks", "Assess Risks (Join)", ""),
        ("Assess Risks (Join)", "High Risk Identified?", ""),

        # High risk decision
        ("High Risk Identified?", "Launch Detailed Investigation", "Yes"),
        ("High Risk Identified?", "Address Risks", "No"),

        # Investigation details
        ("Launch Detailed Investigation", "Investigation (Split)", ""),
        ("Investigation (Split)", "Perform Data Analysis", ""),
        ("Investigation (Split)", "Conduct Interviews", ""),
        ("Perform Data Analysis", "Investigation (Join)", ""),
        ("Conduct Interviews", "Investigation (Join)", ""),
        ("Investigation (Join)", "Site Visit Needed?", ""),
        ("Site Visit Needed?", "Conduct Site Visit", "Yes"),
        ("Site Visit Needed?", "Site Visit (Merge)", "No"),
        ("Conduct Site Visit", "Site Visit (Merge)", ""),
        ("Site Visit (Merge)", "Address Risks", ""),

        # Report compilation
        ("Address Risks", "Compile Audit Report", ""),
        ("Compile Audit Report", "Review Audit Report (Director)", ""),

        # Director approval loop
        ("Review Audit Report (Director)", "Report Approved?", ""),
        ("Report Approved?", "Update Audit Report", "Revisions Required"),
        ("Update Audit Report", "Review Audit Report (Director)", ""),
        ("Report Approved?", "Distribute And Archive (Split)", "Approved"),

        # Distribute and archive in parallel
        ("Distribute And Archive (Split)", "Distribute Final Report", ""),
        ("Distribute And Archive (Split)", "Archive Final Report", ""),
        ("Distribute Final Report", "Receive Final Report (Board)", ""),
        ("Receive Final Report (Board)", "Distribute And Archive (Join)", ""),
        ("Archive Final Report", "Distribute And Archive (Join)", ""),
        ("Distribute And Archive (Join)", "Audit Closed", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            try:
                flows.append(createSequenceFlow(process, src, tgt, guard=guard))
                if guard:
                    print "  [Flow] " + srcName + " -> " + tgtName + " | guard=" + guard
                else:
                    print "  [Flow] " + srcName + " -> " + tgtName
            except Exception as e:
                print "  [Flow] ERROR creating flow " + srcName + " -> " + tgtName + " | " + str(e)
        else:
            print "  [Flow] WARNING missing element for " + srcName + " -> " + tgtName

    print ""
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
        createAnnualAuditProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
