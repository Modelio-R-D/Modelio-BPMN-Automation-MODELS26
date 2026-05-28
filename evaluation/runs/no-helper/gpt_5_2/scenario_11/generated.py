#
# SubscriptionLifecycleProcess.py
#
# Description:
#   BPMN process diagram for Subscription Service Lifecycle:
#   - Customer signs up, enters personal + payment info
#   - System creates account, assigns access, triggers billing cycle
#   - During subscription: updates/enhancements + renewal notifications (loop)
#   - Customer may cancel -> support processes cancellation
#   - Billing applies refund/charge based on terms
#   - Support deactivates subscription, billing settles final balance, end
#
# Applicable on: Package
# Version: 1.0
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

# Waiting configuration
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 170
START_X = 80

# Task dimensions
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
            print "  [FlowGuard] WARNING: Could not set guard '" + guard + "': " + str(e)
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
        # Keep quiet here; called frequently during waiting
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
def createSubscriptionLifecycleProcess(parentPackage):
    processName = "SubscriptionLifecycle_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN SUBSCRIPTION LIFECYCLE - DEBUG LOG"
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

    customerLane = createLane(laneSet, "Customer")
    systemLane = createLane(laneSet, "System")
    supportLane = createLane(laneSet, "Support")
    billingLane = createLane(laneSet, "Billing")

    lanes = {
        "Customer": customerLane,
        "System": systemLane,
        "Support": supportLane,
        "Billing": billingLane
    }
    laneOrder = ["Customer", "System", "Support", "Billing"]

    print "[" + str(step()) + "] Lanes: Customer, System, Support, Billing"

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
        print "  [Element] " + laneName + " / " + name + " | addToLane=" + str(ok)
        return elem

    # Customer
    addElement(createStartEvent, "Sign Up", customerLane, "Customer")
    addElement(createUserTask, "Enter Personal Information", customerLane, "Customer")
    addElement(createUserTask, "Enter Payment Information", customerLane, "Customer")

    # System provisioning
    addElement(createServiceTask, "Generate Account", systemLane, "System")
    addElement(createServiceTask, "Assign Access", systemLane, "System")
    addElement(createServiceTask, "Trigger Billing Cycle", systemLane, "System")

    # Subscription lifecycle loop
    addElement(createServiceTask, "Send Updates and Enhancements", systemLane, "System")
    addElement(createServiceTask, "Send Renewal Notifications", systemLane, "System")
    addElement(createExclusiveGateway, "Cancel Subscription?", customerLane, "Customer")

    # Cancellation path
    addElement(createUserTask, "Submit Cancellation Request", customerLane, "Customer")
    addElement(createUserTask, "Process Cancellation Request", supportLane, "Support")
    addElement(createServiceTask, "Check Cancellation Terms", billingLane, "Billing")
    addElement(createExclusiveGateway, "Refund Due?", billingLane, "Billing")
    addElement(createServiceTask, "Issue Refund", billingLane, "Billing")
    addElement(createServiceTask, "Apply Final Charge", billingLane, "Billing")
    addElement(createManualTask, "Deactivate Subscription", supportLane, "Support")
    addElement(createServiceTask, "Settle Final Account Balance", billingLane, "Billing")
    addElement(createEndEvent, "Subscription Deactivated and Settled", billingLane, "Billing")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (AUTO-UNMASK TRIGGER)
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
    # PHASE 4: WAIT FOR AUTO-UNMASK (+ MANUAL UNMASK FALLBACK)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        # Customer
        "Sign Up": (0, "Customer"),
        "Enter Personal Information": (1, "Customer"),
        "Enter Payment Information": (2, "Customer"),
        "Cancel Subscription?": (7, "Customer"),
        "Submit Cancellation Request": (8, "Customer"),

        # System
        "Generate Account": (3, "System"),
        "Assign Access": (4, "System"),
        "Trigger Billing Cycle": (5, "System"),
        "Send Updates and Enhancements": (6, "System"),
        "Send Renewal Notifications": (7, "System"),

        # Support
        "Process Cancellation Request": (9, "Support"),
        "Deactivate Subscription": (13, "Support"),

        # Billing
        "Check Cancellation Terms": (10, "Billing"),
        "Refund Due?": (11, "Billing"),
        "Issue Refund": (12, "Billing"),
        "Apply Final Charge": (12, "Billing"),
        "Settle Final Account Balance": (14, "Billing"),
        "Subscription Deactivated and Settled": (15, "Billing")
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

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedElements:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs.get(name)
        if not elem:
            print "[" + str(step()) + "] SKIP " + name + ": element ref missing"
            continue

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

        dg = elementGraphics[name]
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
        # Signup
        ("Sign Up", "Enter Personal Information", ""),
        ("Enter Personal Information", "Enter Payment Information", ""),
        ("Enter Payment Information", "Generate Account", ""),
        ("Generate Account", "Assign Access", ""),
        ("Assign Access", "Trigger Billing Cycle", ""),

        # Active subscription cycle
        ("Trigger Billing Cycle", "Send Updates and Enhancements", ""),
        ("Send Updates and Enhancements", "Send Renewal Notifications", ""),
        ("Send Renewal Notifications", "Cancel Subscription?", ""),

        # Gateway loop
        ("Cancel Subscription?", "Send Updates and Enhancements", "No"),
        ("Cancel Subscription?", "Submit Cancellation Request", "Yes"),

        # Cancellation processing
        ("Submit Cancellation Request", "Process Cancellation Request", ""),
        ("Process Cancellation Request", "Check Cancellation Terms", ""),
        ("Check Cancellation Terms", "Refund Due?", ""),

        # Refund or charge based on terms
        ("Refund Due?", "Issue Refund", "Yes"),
        ("Refund Due?", "Apply Final Charge", "No"),

        # Continue to deactivation and settlement
        ("Issue Refund", "Deactivate Subscription", ""),
        ("Apply Final Charge", "Deactivate Subscription", ""),
        ("Deactivate Subscription", "Settle Final Account Balance", ""),
        ("Settle Final Account Balance", "Subscription Deactivated and Settled", "")
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
            print "  [Flow] WARNING: Missing element for flow " + srcName + " -> " + tgtName

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
        createSubscriptionLifecycleProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
