#
# ViennaNightRunAppProcess.py
#
# Title: App For Participating at the Vienna Night Run
#
# Description:
#   BPMN process diagram for using an app (plus fitness gadgets) to prepare for
#   and participate in the Vienna Night Run.
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
SPACING = 160
START_X = 60

# Element sizes
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

    # IMPORTANT: guard text is shown on gateway outflows (condition label)
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

    # Get lane center Y for manual unmask placement
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Runner"))[1]
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

def createViennaNightRunAppProcess(parentPackage):
    baseTitle = "App For Participating at the Vienna Night Run"
    processName = "ViennaNightRunApp_" + EXECUTION_ID
    diagramName = baseTitle + " (" + EXECUTION_ID + ")"

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
    print "Title:          " + baseTitle
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

    runnerLane = createLane(laneSet, "Runner")
    appLane = createLane(laneSet, "App")
    gadgetLane = createLane(laneSet, "Fitness Gadget")
    supportLane = createLane(laneSet, "Event Support")

    lanes = {
        "Runner": runnerLane,
        "App": appLane,
        "Fitness Gadget": gadgetLane,
        "Event Support": supportLane
    }
    laneOrder = ["Runner", "App", "Fitness Gadget", "Event Support"]

    print "[" + str(step()) + "] Lanes: Runner, App, Fitness Gadget, Event Support"

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
        print "  + Element: " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    # Start / setup
    addElement(createStartEvent, "Decide to Participate", runnerLane)
    addElement(createUserTask, "Select Starting Block (enter in app)", runnerLane)
    addElement(createServiceTask, "Save Starting Block", appLane)

    # Qualification loop (test run until <25min)
    addElement(createManualTask, "Run 5km Test", runnerLane)
    addElement(createServiceTask, "Measure Test Time", gadgetLane)
    addElement(createServiceTask, "Check Time < 25min", appLane)
    addElement(createExclusiveGateway, "Qualified?", appLane)
    addElement(createManualTask, "Train", runnerLane)

    # After qualification
    addElement(createUserTask, "Get Starting Number", runnerLane)
    addElement(createServiceTask, "Store Starting Number", appLane)

    # Workday/time planning
    addElement(createUserTask, "Enter Workday End and Start Time (app)", runnerLane)
    addElement(createServiceTask, "Compute Time Buffer", appLane)
    addElement(createExclusiveGateway, "More than 1h?", appLane)
    addElement(createManualTask, "Go to Event from Home", runnerLane)
    addElement(createManualTask, "Go to Event from Work", runnerLane)
    addElement(createExclusiveGateway, "Travel Merge", appLane)

    # Night run execution (parallel: run and drink)
    addElement(createManualTask, "Arrive at Night Run", runnerLane)
    addElement(createParallelGateway, "Run+Drink Split", appLane)
    addElement(createManualTask, "Run Night Run 5km", runnerLane)
    addElement(createManualTask, "Drink Water", supportLane)
    addElement(createParallelGateway, "Run+Drink Join", appLane)

    # Final time
    addElement(createServiceTask, "Measure Final Time", gadgetLane)
    addElement(createServiceTask, "Display Final Time", appLane)
    addElement(createEndEvent, "Final Time Received", runnerLane)

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(diagramName)
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: " + diagramName

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
        # Runner/App/Gadget setup
        "Decide to Participate": (0, "Runner"),
        "Select Starting Block (enter in app)": (1, "Runner"),
        "Save Starting Block": (2, "App"),

        # Qualification loop
        "Run 5km Test": (3, "Runner"),
        "Measure Test Time": (4, "Fitness Gadget"),
        "Check Time < 25min": (5, "App"),
        "Qualified?": (6, "App"),
        "Train": (7, "Runner"),
        "Get Starting Number": (8, "Runner"),
        "Store Starting Number": (9, "App"),

        # Workday planning
        "Enter Workday End and Start Time (app)": (10, "Runner"),
        "Compute Time Buffer": (11, "App"),
        "More than 1h?": (12, "App"),
        "Go to Event from Home": (13, "Runner"),
        "Go to Event from Work": (14, "Runner"),
        "Travel Merge": (15, "App"),

        # Night run parallel actions
        "Arrive at Night Run": (16, "Runner"),
        "Run+Drink Split": (17, "App"),
        "Run Night Run 5km": (18, "Runner"),
        "Drink Water": (18, "Event Support"),
        "Run+Drink Join": (19, "App"),

        # Final time
        "Measure Final Time": (20, "Fitness Gadget"),
        "Display Final Time": (21, "App"),
        "Final Time Received": (22, "Runner"),
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
        lane = lanes[laneName]
        y = getLaneCenterY(diagramHandle, lane)
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

    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Setup
        ("Decide to Participate", "Select Starting Block (enter in app)", ""),
        ("Select Starting Block (enter in app)", "Save Starting Block", ""),
        ("Save Starting Block", "Run 5km Test", ""),

        # Qualification check
        ("Run 5km Test", "Measure Test Time", ""),
        ("Measure Test Time", "Check Time < 25min", ""),
        ("Check Time < 25min", "Qualified?", ""),

        # Gateway outflows need guards
        ("Qualified?", "Get Starting Number", "Yes"),
        ("Qualified?", "Train", "No"),

        # Train loop
        ("Train", "Run 5km Test", ""),

        # After qualification
        ("Get Starting Number", "Store Starting Number", ""),
        ("Store Starting Number", "Enter Workday End and Start Time (app)", ""),

        # Workday buffer decision
        ("Enter Workday End and Start Time (app)", "Compute Time Buffer", ""),
        ("Compute Time Buffer", "More than 1h?", ""),
        ("More than 1h?", "Go to Event from Home", "> 1 hour"),
        ("More than 1h?", "Go to Event from Work", "<= 1 hour"),

        # Merge travel
        ("Go to Event from Home", "Travel Merge", ""),
        ("Go to Event from Work", "Travel Merge", ""),
        ("Travel Merge", "Arrive at Night Run", ""),

        # Parallel at event: run and drink at same time
        ("Arrive at Night Run", "Run+Drink Split", ""),
        ("Run+Drink Split", "Run Night Run 5km", ""),
        ("Run+Drink Split", "Drink Water", ""),
        ("Run Night Run 5km", "Run+Drink Join", ""),
        ("Drink Water", "Run+Drink Join", ""),

        # Final time
        ("Run+Drink Join", "Measure Final Time", ""),
        ("Measure Final Time", "Display Final Time", ""),
        ("Display Final Time", "Final Time Received", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  + Flow: " + srcName[:18] + " -> " + tgtName[:18] + " | Guard=" + guard
            else:
                print "  + Flow: " + srcName[:18] + " -> " + tgtName[:18]
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName

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
    print "Diagram:  " + diagramName
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
        createViennaNightRunAppProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
