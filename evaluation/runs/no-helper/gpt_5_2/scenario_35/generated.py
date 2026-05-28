#
# ChainsawProcess.py
#
# Description:
#   BPMN process diagram: "Chainsaw"
#   Custom chainsaws produced on demand.
#   Customer provides at least 5 properties (e.g., guide bar length (Schwertlaenge),
#   chain width, electric vs motor, handle type, safety features).
#   Parts are ordered in parallel, then inspected and assembled.
#   Customer receives updates during production.
#   First saw is shipped for approval; if accepted, remaining quantity is produced.
#
# Applicable on: Package
#
# Version: v9.2 - March 2026
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
SPACING = 165
START_X = 80

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
            laneName = elementLayout.get(name, (0, "Customer"))[1]
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

def createChainsawProcess(parentPackage):
    processName = "Chainsaw_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:         Chainsaw"
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="

    # ------------------------------------------------------------------------
    # PHASE 1: PROCESS & LANES
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

    customerLane = createLane(laneSet, "Customer")
    salesLane = createLane(laneSet, "Sales")
    procurementLane = createLane(laneSet, "Procurement")
    productionLane = createLane(laneSet, "Production")
    shippingLane = createLane(laneSet, "Shipping")

    lanes = {
        "Customer": customerLane,
        "Sales": salesLane,
        "Procurement": procurementLane,
        "Production": productionLane,
        "Shipping": shippingLane
    }
    laneOrder = ["Customer", "Sales", "Procurement", "Production", "Shipping"]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

    # ------------------------------------------------------------------------
    # PHASE 2: ELEMENTS
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
        print "  [Elem] " + laneName + " / " + name + " | addToLane=" + str(ok)
        return elem

    # Customer -> Sales -> Procurement (parallel) -> Production -> Shipping -> Customer approval -> remaining
    addElement(createStartEvent, "Need Custom Chainsaw", "Customer")
    addElement(createUserTask, "Provide Requirements", "Customer")

    addElement(createUserTask, "Capture Properties (5+)", "Sales")
    addElement(createUserTask, "Confirm Specs and Price", "Sales")

    addElement(createParallelGateway, "Order Parts in Parallel", "Procurement")

    addElement(createServiceTask, "Order Guide Bar (Schwertlaenge)", "Procurement")
    addElement(createServiceTask, "Order Chain (Width/Pitch)", "Procurement")
    addElement(createServiceTask, "Order Power Unit (Electric/Motor)", "Procurement")
    addElement(createServiceTask, "Order Handle and Controls", "Procurement")
    addElement(createServiceTask, "Order Safety and Fasteners", "Procurement")

    addElement(createParallelGateway, "All Parts Arrived", "Procurement")

    addElement(createManualTask, "Inspect All Parts", "Production")
    addElement(createManualTask, "Assemble First Saw", "Production")

    addElement(createServiceTask, "Send Update: First Saw Built", "Sales")
    addElement(createUserTask, "Ship First Saw", "Shipping")

    addElement(createUserTask, "Test First Saw", "Customer")
    addElement(createExclusiveGateway, "Customer Likes It?", "Customer")

    # No branch (change request -> adjust -> back to ordering)
    addElement(createUserTask, "Collect Change Request", "Sales")
    addElement(createManualTask, "Adjust Design/Build", "Production")

    # Yes branch (produce remaining -> updates -> ship remaining -> end)
    addElement(createManualTask, "Produce Remaining Saws", "Production")
    addElement(createServiceTask, "Send Production Updates (Periodic)", "Sales")
    addElement(createUserTask, "Ship Remaining Saws", "Shipping")
    addElement(createEndEvent, "Order Completed", "Customer")

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

    # Layout: element name -> (column, laneName)
    elementLayout = {
        "Need Custom Chainsaw": (0, "Customer"),
        "Provide Requirements": (1, "Customer"),

        "Capture Properties (5+)": (2, "Sales"),
        "Confirm Specs and Price": (3, "Sales"),

        "Order Parts in Parallel": (4, "Procurement"),

        "Order Guide Bar (Schwertlaenge)": (5, "Procurement"),
        "Order Chain (Width/Pitch)": (6, "Procurement"),
        "Order Power Unit (Electric/Motor)": (7, "Procurement"),
        "Order Handle and Controls": (8, "Procurement"),
        "Order Safety and Fasteners": (9, "Procurement"),

        "All Parts Arrived": (10, "Procurement"),

        "Inspect All Parts": (11, "Production"),
        "Assemble First Saw": (12, "Production"),

        "Send Update: First Saw Built": (13, "Sales"),
        "Ship First Saw": (14, "Shipping"),

        "Test First Saw": (15, "Customer"),
        "Customer Likes It?": (16, "Customer"),

        "Collect Change Request": (17, "Sales"),
        "Adjust Design/Build": (18, "Production"),

        "Produce Remaining Saws": (17, "Production"),
        "Send Production Updates (Periodic)": (18, "Sales"),
        "Ship Remaining Saws": (19, "Shipping"),
        "Order Completed": (20, "Customer"),
    }

    # ------------------------------------------------------------------------
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # ------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (GUARDS ON GATEWAY OUTFLOWS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Need Custom Chainsaw", "Provide Requirements", ""),
        ("Provide Requirements", "Capture Properties (5+)", ""),
        ("Capture Properties (5+)", "Confirm Specs and Price", ""),
        ("Confirm Specs and Price", "Order Parts in Parallel", ""),

        # Parallel ordering
        ("Order Parts in Parallel", "Order Guide Bar (Schwertlaenge)", ""),
        ("Order Parts in Parallel", "Order Chain (Width/Pitch)", ""),
        ("Order Parts in Parallel", "Order Power Unit (Electric/Motor)", ""),
        ("Order Parts in Parallel", "Order Handle and Controls", ""),
        ("Order Parts in Parallel", "Order Safety and Fasteners", ""),

        ("Order Guide Bar (Schwertlaenge)", "All Parts Arrived", ""),
        ("Order Chain (Width/Pitch)", "All Parts Arrived", ""),
        ("Order Power Unit (Electric/Motor)", "All Parts Arrived", ""),
        ("Order Handle and Controls", "All Parts Arrived", ""),
        ("Order Safety and Fasteners", "All Parts Arrived", ""),

        ("All Parts Arrived", "Inspect All Parts", ""),
        ("Inspect All Parts", "Assemble First Saw", ""),

        ("Assemble First Saw", "Send Update: First Saw Built", ""),
        ("Send Update: First Saw Built", "Ship First Saw", ""),
        ("Ship First Saw", "Test First Saw", ""),
        ("Test First Saw", "Customer Likes It?", ""),

        # Exclusive decision with guards (CRITICAL: use guard)
        ("Customer Likes It?", "Produce Remaining Saws", "Yes"),
        ("Customer Likes It?", "Collect Change Request", "No"),

        # No path loop-back
        ("Collect Change Request", "Adjust Design/Build", ""),
        ("Adjust Design/Build", "Order Parts in Parallel", ""),

        # Yes path completion
        ("Produce Remaining Saws", "Send Production Updates (Periodic)", ""),
        ("Send Production Updates (Periodic)", "Ship Remaining Saws", ""),
        ("Ship Remaining Saws", "Order Completed", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
            if guard:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18] + " | guard=" + guard
            else:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18]
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName

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
        createChainsawProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
