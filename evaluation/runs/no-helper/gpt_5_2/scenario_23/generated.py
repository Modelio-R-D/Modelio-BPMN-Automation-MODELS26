#
# CreditScoringProcess.py
#
# Description:
#   BPMN process diagram for credit scoring request between:
#   - Sales Clerk (Frontend)
#   - Banking System
#   - Scoring Agency
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
SPACING = 155
START_X = 70

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

    # IMPORTANT: condition labels on gateway outflows must be Guards
    if guard:
        flow.setConditionExpression(guard)

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

    # Lane center Y positions (needed for correct unmask)
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Banking System"))[1]
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

def createCreditScoringProcess(parentPackage):
    processName = "CreditScoring_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN CREDIT SCORING REQUEST - DEBUG LOG"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="

    # =======================================================================
    # PHASE 1: CREATE PROCESS & LANES
    # =======================================================================
    print ""
    print "== PHASE 1: CREATE PROCESS & LANES =============================="
    print ""

    process = modelingSession.getModel().createBpmnProcess()
    process.setName(processName)
    process.setOwner(parentPackage)
    print "[" + str(step()) + "] Process: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    clerkLane = createLane(laneSet, "Sales Clerk")
    bankLane = createLane(laneSet, "Banking System")
    agencyLane = createLane(laneSet, "Scoring Agency")

    lanes = {
        "Sales Clerk": clerkLane,
        "Banking System": bankLane,
        "Scoring Agency": agencyLane
    }
    laneOrder = ["Sales Clerk", "Banking System", "Scoring Agency"]

    print "[" + str(step()) + "] Lanes: Sales Clerk, Banking System, Scoring Agency"

    # =======================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =======================================================================
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
        print "  [Add] " + laneName + ": " + name + " | addToLane=" + ("OK" if ok else "FAILED")
        return elem

    # Banking System
    addElement(createMessageStartEvent, "Scoring request received", bankLane, "Banking System")
    addElement(createServiceTask, "Send scoring request to agency", bankLane, "Banking System")
    addElement(createServiceTask, "Receive delay notification", bankLane, "Banking System")
    addElement(createExclusiveGateway, "Merge results", bankLane, "Banking System")
    addElement(createServiceTask, "Receive scoring result", bankLane, "Banking System")
    addElement(createServiceTask, "Present result to frontend", bankLane, "Banking System")

    # Scoring Agency
    addElement(createServiceTask, "Level 1 quick scoring", agencyLane, "Scoring Agency")
    addElement(createExclusiveGateway, "Immediate result?", agencyLane, "Scoring Agency")
    addElement(createServiceTask, "Send scoring result (L1)", agencyLane, "Scoring Agency")
    addElement(createServiceTask, "Inform delay", agencyLane, "Scoring Agency")
    addElement(createServiceTask, "Level 2 scoring", agencyLane, "Scoring Agency")
    addElement(createServiceTask, "Send scoring result (L2)", agencyLane, "Scoring Agency")

    # Sales Clerk
    addElement(createUserTask, "Show delay message (check later)", clerkLane, "Sales Clerk")
    addElement(createUserTask, "View scoring result in frontend", clerkLane, "Sales Clerk")
    addElement(createEndEvent, "Scoring visible", clerkLane, "Sales Clerk")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # =======================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =======================================================================
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

    # =======================================================================
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # =======================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        # Banking System
        "Scoring request received": (0, "Banking System"),
        "Send scoring request to agency": (1, "Banking System"),
        "Receive delay notification": (5, "Banking System"),
        "Merge results": (9, "Banking System"),
        "Receive scoring result": (10, "Banking System"),
        "Present result to frontend": (11, "Banking System"),

        # Scoring Agency
        "Level 1 quick scoring": (2, "Scoring Agency"),
        "Immediate result?": (3, "Scoring Agency"),
        "Send scoring result (L1)": (4, "Scoring Agency"),
        "Inform delay": (4, "Scoring Agency"),
        "Level 2 scoring": (7, "Scoring Agency"),
        "Send scoring result (L2)": (8, "Scoring Agency"),

        # Sales Clerk
        "Show delay message (check later)": (6, "Sales Clerk"),
        "View scoring result in frontend": (12, "Sales Clerk"),
        "Scoring visible": (13, "Sales Clerk")
    }

    # Wait for all nodes + lanes (lanes needed for Y positioning)
    waitList = []
    for e in elements:
        waitList.append(e)
    waitList.append(clerkLane)
    waitList.append(bankLane)
    waitList.append(agencyLane)

    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    elementGraphics, attempts = waitForElements(diagramHandle, waitList)
    totalWaitTime = attempts * WAIT_TIME_MS

    readyCount = len(elementGraphics)
    print ""
    print "[" + str(step()) + "] Ready graphics: " + str(readyCount) + "/" + str(len(waitList)) + " after " + str(totalWaitTime) + "ms"

    missingNodes = [e.getName() for e in elements if e.getName() not in elementGraphics]
    if len(missingNodes) > 0:
        print "[" + str(step()) + "] WARNING: Missing node graphics: " + ", ".join(missingNodes)
        print ""
        print "[" + str(step()) + "] Trying manual unmask fallback (inside lane Y)..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
        print ""
        print "[" + str(step()) + "] Manual unmask count: " + str(unmaskedCount)

        stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        if len(stillMissing) > 0:
            print "[" + str(step()) + "] STILL MISSING: " + ", ".join(stillMissing)
        else:
            print "[" + str(step()) + "] All elements now available"
    else:
        print "[" + str(step()) + "] All node graphics available"

    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)

    # =======================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =======================================================================
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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available, defaulting Y=100"
            laneY[laneName] = 100

    print ""
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    repositionedCount = 0

    for col, name, laneName in sortedElements:
        if name not in elementRefs:
            # layout entries may include none, but here all should exist
            continue

        elem = elementRefs[name]
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + laneName + "/" + name + ": not in diagram graphics"
            continue

        dg = elementGraphics[name]
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
        diagramHandle.save()
        repositionedCount += 1

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes
        previousLanes = currentLanes

    print ""
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # =======================================================================
    # PHASE 6: CREATE FLOWS
    # =======================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Scoring request received", "Send scoring request to agency", ""),

        ("Send scoring request to agency", "Level 1 quick scoring", ""),
        ("Level 1 quick scoring", "Immediate result?", ""),

        # Gateway outflows (MUST use guards)
        ("Immediate result?", "Send scoring result (L1)", "Yes"),
        ("Immediate result?", "Inform delay", "No"),

        # Immediate result path
        ("Send scoring result (L1)", "Merge results", ""),

        # Delayed path
        ("Inform delay", "Receive delay notification", ""),
        ("Receive delay notification", "Show delay message (check later)", ""),
        ("Show delay message (check later)", "Level 2 scoring", ""),
        ("Level 2 scoring", "Send scoring result (L2)", ""),
        ("Send scoring result (L2)", "Merge results", ""),

        # After merge
        ("Merge results", "Receive scoring result", ""),
        ("Receive scoring result", "Present result to frontend", ""),
        ("Present result to frontend", "View scoring result in frontend", ""),
        ("View scoring result in frontend", "Scoring visible", "")
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName + " -> " + tgtName + " | guard=" + guard
            else:
                print "  [Flow] " + srcName + " -> " + tgtName
        else:
            print "  [Flow] WARNING: Missing element for flow: " + srcName + " -> " + tgtName

    diagramHandle.save()
    print ""
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    print "[" + str(step()) + "] Save"

    # =======================================================================
    # FINAL STATE
    # =======================================================================
    print ""
    print "== FINAL STATE ==================================================="
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
        createCreditScoringProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
