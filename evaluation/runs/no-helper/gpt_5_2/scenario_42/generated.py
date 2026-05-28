#
# FridgeServiceProcess.py
#
# Title: Service for Your Fridge
#
# Description:
#   BPMN process diagram for a fridge repair service workflow.
#
# Lanes:
#   - Customer
#   - Fridge Service Center
#   - Service Facility
#
# Key Insight (from Modelio developers):
#   - Modelio automatically unmasks elements when a diagram is created
#   - Do NOT unmask manually at first
#   - Wait until graphics are available before repositioning
#   - If some elements are still missing, manually unmask INSIDE the correct lane
#
# Applicable on: Package
#
# Version: 9.1
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
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)

    # IMPORTANT: guard text is what appears on gateway outflows in Modelio BPMN
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

    # Get each lane center Y (must unmask INSIDE lane)
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

def createServiceForYourFridgeProcess(parentPackage):

    processName = "ServiceForYourFridge_" + EXECUTION_ID
    diagramName = "Service for Your Fridge_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Service for Your Fridge"
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "Diagram Name:   " + diagramName
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

    customerLane = createLane(laneSet, "Customer")
    centerLane = createLane(laneSet, "Fridge Service Center")
    facilityLane = createLane(laneSet, "Service Facility")

    lanes = {
        "Customer": customerLane,
        "Fridge Service Center": centerLane,
        "Service Facility": facilityLane
    }
    laneOrder = ["Customer", "Fridge Service Center", "Service Facility"]

    print "[" + str(step()) + "] Lanes: Customer, Fridge Service Center, Service Facility"

    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
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
        print "  [Add] " + laneName + ": " + name + " | addToLane=" + str(ok)
        return elem

    # Customer
    addElement(createStartEvent, "Fridge makes strange noises", customerLane, "Customer")
    addElement(createUserTask, "Describe symptoms", customerLane, "Customer")
    addElement(createUserTask, "Send symptoms and fridge type", customerLane, "Customer")
    addElement(createUserTask, "Confirm fridge is OK", customerLane, "Customer")
    addElement(createUserTask, "Rate service facility", customerLane, "Customer")

    # Service Center
    addElement(createServiceTask, "Register request", centerLane, "Fridge Service Center")
    addElement(createUserTask, "Select local service facility", centerLane, "Fridge Service Center")
    addElement(createServiceTask, "Forward request to facility", centerLane, "Fridge Service Center")

    # Service Facility
    addElement(createUserTask, "Make appointment", facilityLane, "Service Facility")
    addElement(createManualTask, "Arrive at customer (random time)", facilityLane, "Service Facility")
    addElement(createExclusiveGateway, "Have required parts?", facilityLane, "Service Facility")
    addElement(createServiceTask, "Order additional parts", facilityLane, "Service Facility")
    addElement(createUserTask, "Repair fridge", facilityLane, "Service Facility")

    # After repair confirmation
    addElement(createExclusiveGateway, "Fridge OK?", customerLane, "Customer")
    addElement(createEndEvent, "Service completed", customerLane, "Customer")

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
    # PHASE 4: WAIT FOR AUTO-UNMASK (AND MANUAL UNMASK FALLBACK)
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout: element name -> (column, lane name)
    elementLayout = {
        # Customer
        "Fridge makes strange noises": (0, "Customer"),
        "Describe symptoms": (1, "Customer"),
        "Send symptoms and fridge type": (2, "Customer"),
        "Confirm fridge is OK": (10, "Customer"),
        "Fridge OK?": (11, "Customer"),
        "Rate service facility": (12, "Customer"),
        "Service completed": (13, "Customer"),

        # Service Center
        "Register request": (3, "Fridge Service Center"),
        "Select local service facility": (4, "Fridge Service Center"),
        "Forward request to facility": (5, "Fridge Service Center"),

        # Service Facility
        "Make appointment": (6, "Service Facility"),
        "Arrive at customer (random time)": (7, "Service Facility"),
        "Have required parts?": (8, "Service Facility"),
        "Order additional parts": (9, "Service Facility"),
        "Repair fridge": (10, "Service Facility"),
    }

    # Also wait for lanes so bounds are readable
    waitList = []
    for e in elements:
        waitList.append(e)
    waitList.append(customerLane)
    waitList.append(centerLane)
    waitList.append(facilityLane)

    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    elementGraphics, attempts = waitForElements(diagramHandle, waitList)

    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    totalCount = len(waitList)

    if foundCount == totalCount:
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " graphics ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in waitList if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(totalCount) + " graphics ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)

        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing FLOW NODES..."
        print ""

        # Only try manual unmask for BPMN nodes (not lanes)
        nodeGraphics = {}
        for k, v in elementGraphics.items():
            nodeGraphics[k] = v

        unmaskedCount = unmaskMissingElements(diagramHandle, elements, nodeGraphics, lanes, elementLayout)
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"

        # Merge back
        for k, v in nodeGraphics.items():
            elementGraphics[k] = v

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
            laneY[laneName] = 100
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available, using Y=100"

    print ""
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    # Sort by column
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        if name in elementRefs:
            sortedElements.append((col, name, laneName))
    sortedElements.sort()

    repositionedCount = 0
    for col, name, laneName in sortedElements:
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
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(sortedElements))

    # =========================================================================
    # PHASE 6: CREATE FLOWS (WITH GUARDS FROM GATEWAYS)
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Customer -> Service Center
        ("Fridge makes strange noises", "Describe symptoms", ""),
        ("Describe symptoms", "Send symptoms and fridge type", ""),
        ("Send symptoms and fridge type", "Register request", ""),

        # Service Center
        ("Register request", "Select local service facility", ""),
        ("Select local service facility", "Forward request to facility", ""),
        ("Forward request to facility", "Make appointment", ""),

        # Service Facility
        ("Make appointment", "Arrive at customer (random time)", ""),
        ("Arrive at customer (random time)", "Have required parts?", ""),

        # Parts decision (guards required)
        ("Have required parts?", "Repair fridge", "Yes"),
        ("Have required parts?", "Order additional parts", "No"),

        # Parts loop
        ("Order additional parts", "Arrive at customer (random time)", ""),

        # Repair -> Customer confirmation
        ("Repair fridge", "Confirm fridge is OK", ""),
        ("Confirm fridge is OK", "Fridge OK?", ""),

        # Confirmation decision
        ("Fridge OK?", "Rate service facility", "Yes"),
        ("Fridge OK?", "Repair fridge", "No"),

        # Finish
        ("Rate service facility", "Service completed", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
            print "  [Flow] " + srcName[:25] + " -> " + tgtName[:25] + (" | guard=" + guard if guard else "")
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
        createServiceForYourFridgeProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
