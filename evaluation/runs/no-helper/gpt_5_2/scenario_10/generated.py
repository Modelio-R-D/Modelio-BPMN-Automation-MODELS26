#
# ITSolutionRequestProcess.py
#
# Description:
#   BPMN process diagram for IT solution request workflow:
#     - Request submitted by Employee/Department
#     - IT assesses compatibility, cost, and resources
#     - Approval decision
#     - Procurement, installation, controlled testing
#     - Rollout, optional training, ongoing support
#
# Applicable on: Package
#
# Version: v9.1
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

# Dimensions
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

def createMessageStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event

def createTimerStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
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
        try:
            flow.setConditionExpression(guard)
        except:
            pass
    return flow

def createSequenceFlowWithGuard(process, source, target, guard):
    return createSequenceFlow(process, source, target, guard=guard)

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
        shortName = name[:12]
        if bounds:
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(shortName + "=--")
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
            laneName = elementLayout.get(name, (0, "Requester"))[1]
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

def createITSolutionRequestProcess(parentPackage):
    processName = "ITSolutionRequest_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN IT SOLUTION REQUEST PROCESS - DEBUG LOG"
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

    requesterLane = createLane(laneSet, "Requester")
    itLane = createLane(laneSet, "IT")
    procurementLane = createLane(laneSet, "Procurement")

    lanes = {
        "Requester": requesterLane,
        "IT": itLane,
        "Procurement": procurementLane
    }
    laneOrder = ["Requester", "IT", "Procurement"]
    print "[" + str(step()) + "] Lanes: Requester, IT, Procurement"

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
        print "  [Element] " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    # Requester
    addElement(createStartEvent, "Need IT Solution", requesterLane)
    addElement(createUserTask, "Submit IT Solution Request", requesterLane)

    # IT assessment and approval
    addElement(createUserTask, "Assess Compatibility and Needs", itLane)
    addElement(createServiceTask, "Estimate Cost and Resources", itLane)
    addElement(createExclusiveGateway, "Request Approved?", itLane)
    addElement(createEndEvent, "Request Rejected", itLane)

    # Procurement + implementation
    addElement(createServiceTask, "Procure Tools or Licenses", procurementLane)
    addElement(createServiceTask, "Install Solution", itLane)
    addElement(createServiceTask, "Test in Controlled Environment", itLane)
    addElement(createExclusiveGateway, "Testing Successful?", itLane)
    addElement(createUserTask, "Fix Issues and Retest", itLane)

    # Rollout and support
    addElement(createUserTask, "Roll Out to Requesting Department", itLane)
    addElement(createExclusiveGateway, "Training Needed?", itLane)
    addElement(createUserTask, "Provide Training", itLane)
    addElement(createServiceTask, "Provide Ongoing IT Support", itLane)
    addElement(createEndEvent, "Solution Operational", itLane)

    print ""
    print "[" + str(step()) + "] Total elements (excluding lanes): " + str(len(elements))

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

    # Layout: name -> (column, laneName)
    elementLayout = {
        # Requester
        "Need IT Solution": (0, "Requester"),
        "Submit IT Solution Request": (1, "Requester"),

        # IT assessment
        "Assess Compatibility and Needs": (2, "IT"),
        "Estimate Cost and Resources": (3, "IT"),
        "Request Approved?": (4, "IT"),
        "Request Rejected": (5, "IT"),

        # Procurement + implementation
        "Procure Tools or Licenses": (5, "Procurement"),
        "Install Solution": (6, "IT"),
        "Test in Controlled Environment": (7, "IT"),
        "Testing Successful?": (8, "IT"),
        "Fix Issues and Retest": (9, "IT"),

        # Rollout
        "Roll Out to Requesting Department": (10, "IT"),
        "Training Needed?": (11, "IT"),
        "Provide Training": (12, "IT"),
        "Provide Ongoing IT Support": (13, "IT"),
        "Solution Operational": (14, "IT")
    }

    # Wait for lanes + elements (so lane bounds are available too)
    waitList = []
    waitList.extend([requesterLane, itLane, procurementLane])
    waitList.extend(elements)

    print "[" + str(step()) + "] Waiting for lanes+elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    graphicsAll, attempts = waitForElements(diagramHandle, waitList)
    totalWaitTime = attempts * WAIT_TIME_MS

    # Split graphics: nodes only (elements), and lane graphics (optional)
    elementGraphics = {}
    for elem in elements:
        n = elem.getName()
        if n in graphicsAll:
            elementGraphics[n] = graphicsAll[n]

    foundCount = len(elementGraphics)
    totalNodes = len(elements)

    if foundCount == totalNodes:
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + "/" + str(totalNodes) + " nodes ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(totalNodes) + " nodes ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)

        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing nodes (inside lane Y)..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " nodes unmasked"

        foundCount = len(elementGraphics)
        if foundCount == totalNodes:
            print "[" + str(step()) + "] All nodes now available"
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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY missing)"

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
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (GUARDS ON GATEWAY OUTFLOWS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Need IT Solution", "Submit IT Solution Request", ""),
        ("Submit IT Solution Request", "Assess Compatibility and Needs", ""),

        ("Assess Compatibility and Needs", "Estimate Cost and Resources", ""),
        ("Estimate Cost and Resources", "Request Approved?", ""),

        # Approval decision (guards)
        ("Request Approved?", "Request Rejected", "Rejected"),
        ("Request Approved?", "Procure Tools or Licenses", "Approved"),

        ("Procure Tools or Licenses", "Install Solution", ""),
        ("Install Solution", "Test in Controlled Environment", ""),
        ("Test in Controlled Environment", "Testing Successful?", ""),

        # Testing decision (guards)
        ("Testing Successful?", "Roll Out to Requesting Department", "Yes"),
        ("Testing Successful?", "Fix Issues and Retest", "No"),
        ("Fix Issues and Retest", "Test in Controlled Environment", ""),

        ("Roll Out to Requesting Department", "Training Needed?", ""),

        # Training decision (guards)
        ("Training Needed?", "Provide Training", "Yes"),
        ("Training Needed?", "Provide Ongoing IT Support", "No"),
        ("Provide Training", "Provide Ongoing IT Support", ""),

        ("Provide Ongoing IT Support", "Solution Operational", "")
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18] + " | Guard=" + guard
            else:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18]
        else:
            print "  [Flow] WARNING: Missing element for flow " + srcName + " -> " + tgtName

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
        createITSolutionRequestProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
