#
# ECommerceOrderFulfillmentProcess.py
#
# Description:
#   BPMN process diagram for an e-commerce order fulfillment process including:
#   - Payment success/failure
#   - Stock check with backorder loop
#   - Pick, QC
#   - Packaging with optional gift wrap
#   - Shipping documents with optional customs (international)
#   - Dispatch, shipping confirmation, inventory update
#   - Delivery confirmation, feedback request
#   - Returns flow (label, receive, inspect, refund or replacement)
#
# Applicable on: Package
#
# Version: 9.2 - March 2026
#
# IMPORTANT (Modelio dev insight):
#   - Diagram creation triggers auto-unmask of existing elements
#   - Do NOT unmask() initially
#   - Wait for graphics to be available before repositioning
#   - If some elements are still missing, do a manual unmask INSIDE the correct lane Y
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
MAX_ATTEMPTS = 5

# Layout configuration
SPACING = 170
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
    if guard:
        # Guard text is what displays on gateway outflows
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
        # Center vertically with slight adjustment (matches prior experiments)
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

    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Order System"))[1]
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

def createECommerceOrderFulfillmentProcess(parentPackage):
    processName = "ECommerceOrderFulfillment_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN E-COMMERCE ORDER FULFILLMENT - DEBUG LOG"
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

    # Lane order defines vertical order (top to bottom)
    customerLane   = createLane(laneSet, "Customer")
    orderSysLane   = createLane(laneSet, "Order System")
    paymentLane    = createLane(laneSet, "Payment")
    inventoryLane  = createLane(laneSet, "Inventory")
    warehouseLane  = createLane(laneSet, "Warehouse")
    qcLane         = createLane(laneSet, "Quality Control")
    packagingLane  = createLane(laneSet, "Packaging")
    shippingLane   = createLane(laneSet, "Shipping")
    customsLane    = createLane(laneSet, "Customs")
    returnsLane    = createLane(laneSet, "Returns")

    lanes = {
        "Customer": customerLane,
        "Order System": orderSysLane,
        "Payment": paymentLane,
        "Inventory": inventoryLane,
        "Warehouse": warehouseLane,
        "Quality Control": qcLane,
        "Packaging": packagingLane,
        "Shipping": shippingLane,
        "Customs": customsLane,
        "Returns": returnsLane
    }
    laneOrder = ["Customer", "Order System", "Payment", "Inventory", "Warehouse", "Quality Control", "Packaging", "Shipping", "Customs", "Returns"]
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
        print "  - Create: " + name + " | Lane=" + laneName + " | addToLane=" + str(ok)
        return elem

    # Start and payment
    addElement(createMessageStartEvent, "Order Placed", "Customer")
    addElement(createServiceTask, "Record Order Details", "Order System")
    addElement(createServiceTask, "Process Payment", "Payment")
    addElement(createExclusiveGateway, "Payment Successful?", "Payment")
    addElement(createServiceTask, "Notify Payment Failure", "Order System")
    addElement(createEndEvent, "Order End (Payment Failed)", "Customer")

    # Stock check + backorder loop
    addElement(createServiceTask, "Check Stock Availability", "Inventory")
    addElement(createExclusiveGateway, "All Items In Stock?", "Inventory")
    addElement(createServiceTask, "Initiate Backorder", "Inventory")
    addElement(createServiceTask, "Inform Backorder Delay", "Order System")
    addElement(createServiceTask, "Backorder Received", "Inventory")

    # Warehouse fulfillment
    addElement(createManualTask, "Pick Items", "Warehouse")
    addElement(createUserTask, "Quality Control Check", "Quality Control")

    # Parallel split/join for packaging + shipping docs
    addElement(createParallelGateway, "Fulfillment Split", "Order System")

    # Packaging with optional gift wrap
    addElement(createManualTask, "Package Items", "Packaging")
    addElement(createExclusiveGateway, "Gift Wrap Requested?", "Packaging")
    addElement(createManualTask, "Gift Wrap Items", "Packaging")
    addElement(createExclusiveGateway, "Packaging Merge", "Packaging")

    # Shipping docs with optional customs
    addElement(createUserTask, "Prepare Shipping Docs and Labels", "Shipping")
    addElement(createExclusiveGateway, "International Order?", "Shipping")
    addElement(createUserTask, "Prepare Customs Documentation", "Customs")
    addElement(createExclusiveGateway, "Docs Merge", "Shipping")

    # Join and dispatch
    addElement(createParallelGateway, "Ready to Dispatch", "Order System")
    addElement(createManualTask, "Dispatch Order", "Shipping")
    addElement(createServiceTask, "Send Shipping Confirmation", "Order System")
    addElement(createServiceTask, "Update Inventory Levels", "Inventory")

    # Delivery + feedback or returns
    addElement(createServiceTask, "Confirm Successful Delivery", "Order System")
    addElement(createExclusiveGateway, "Issues Reported Upon Delivery?", "Order System")

    addElement(createServiceTask, "Send Feedback Request Email", "Order System")
    addElement(createEndEvent, "Order Complete", "Customer")

    # Returns process
    addElement(createServiceTask, "Send Return Shipping Label", "Returns")
    addElement(createManualTask, "Receive Returned Items", "Returns")
    addElement(createUserTask, "Inspect Returned Items", "Returns")
    addElement(createExclusiveGateway, "Refund or Replacement?", "Returns")
    addElement(createServiceTask, "Process Refund", "Returns")
    addElement(createManualTask, "Send Replacement", "Shipping")
    addElement(createExclusiveGateway, "Return Merge", "Returns")
    addElement(createEndEvent, "Return Completed", "Customer")

    print ""
    print "[" + str(step()) + "] Total flow elements: " + str(len(elements))

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

    # Layout: element name -> (column_index, lane_name)
    elementLayout = {
        "Order Placed": (0, "Customer"),
        "Record Order Details": (1, "Order System"),
        "Process Payment": (2, "Payment"),
        "Payment Successful?": (3, "Payment"),
        "Notify Payment Failure": (4, "Order System"),
        "Order End (Payment Failed)": (5, "Customer"),

        "Check Stock Availability": (4, "Inventory"),
        "All Items In Stock?": (5, "Inventory"),
        "Initiate Backorder": (6, "Inventory"),
        "Inform Backorder Delay": (7, "Order System"),
        "Backorder Received": (8, "Inventory"),

        "Pick Items": (9, "Warehouse"),
        "Quality Control Check": (10, "Quality Control"),
        "Fulfillment Split": (11, "Order System"),

        "Package Items": (12, "Packaging"),
        "Gift Wrap Requested?": (13, "Packaging"),
        "Gift Wrap Items": (14, "Packaging"),
        "Packaging Merge": (15, "Packaging"),

        "Prepare Shipping Docs and Labels": (12, "Shipping"),
        "International Order?": (13, "Shipping"),
        "Prepare Customs Documentation": (14, "Customs"),
        "Docs Merge": (15, "Shipping"),

        "Ready to Dispatch": (16, "Order System"),
        "Dispatch Order": (17, "Shipping"),
        "Send Shipping Confirmation": (18, "Order System"),
        "Update Inventory Levels": (19, "Inventory"),

        "Confirm Successful Delivery": (20, "Order System"),
        "Issues Reported Upon Delivery?": (21, "Order System"),

        "Send Feedback Request Email": (22, "Order System"),
        "Order Complete": (23, "Customer"),

        "Send Return Shipping Label": (22, "Returns"),
        "Receive Returned Items": (23, "Returns"),
        "Inspect Returned Items": (24, "Returns"),
        "Refund or Replacement?": (25, "Returns"),
        "Process Refund": (26, "Returns"),
        "Send Replacement": (26, "Shipping"),
        "Return Merge": (27, "Returns"),
        "Return Completed": (28, "Customer")
    }

    # Wait for flow elements + lanes (helps lane bounds availability)
    waitList = []
    for ln in laneOrder:
        waitList.append(lanes[ln])
    for e in elements:
        waitList.append(e)

    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    elementGraphics, attempts = waitForElements(diagramHandle, waitList)
    totalWaitTime = attempts * WAIT_TIME_MS
    print ""
    print "[" + str(step()) + "] Wait complete in ~" + str(totalWaitTime) + "ms (found " + str(len(elementGraphics)) + "/" + str(len(waitList)) + ")"

    # Manual unmask fallback for missing FLOW elements only
    missingFlow = [e for e in elements if e.getName() not in elementGraphics]
    if len(missingFlow) > 0:
        print ""
        print "[" + str(step()) + "] WARNING: Missing flow elements after wait: " + str(len(missingFlow))
        print "         Missing: " + ", ".join([e.getName() for e in missingFlow])
        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing flow elements (inside lane Y)..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
        print ""
        print "[" + str(step()) + "] Manual unmask done: " + str(unmaskedCount) + " newly unmasked"

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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY unknown)"

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
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (WITH GUARDS ON GATEWAY OUTFLOWS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Order Placed", "Record Order Details", ""),
        ("Record Order Details", "Process Payment", ""),
        ("Process Payment", "Payment Successful?", ""),

        # Payment gateway (guards)
        ("Payment Successful?", "Notify Payment Failure", "Failure"),
        ("Notify Payment Failure", "Order End (Payment Failed)", ""),
        ("Payment Successful?", "Check Stock Availability", "Success"),

        # Stock check
        ("Check Stock Availability", "All Items In Stock?", ""),
        ("All Items In Stock?", "Pick Items", "In Stock"),
        ("All Items In Stock?", "Initiate Backorder", "Out of Stock"),
        ("Initiate Backorder", "Inform Backorder Delay", ""),
        ("Inform Backorder Delay", "Backorder Received", ""),
        # Loop until stock is available
        ("Backorder Received", "Check Stock Availability", ""),

        # Fulfillment
        ("Pick Items", "Quality Control Check", ""),
        ("Quality Control Check", "Fulfillment Split", ""),

        # Parallel split
        ("Fulfillment Split", "Package Items", ""),
        ("Fulfillment Split", "Prepare Shipping Docs and Labels", ""),

        # Packaging branch
        ("Package Items", "Gift Wrap Requested?", ""),
        ("Gift Wrap Requested?", "Gift Wrap Items", "Yes"),
        ("Gift Wrap Requested?", "Packaging Merge", "No"),
        ("Gift Wrap Items", "Packaging Merge", ""),
        ("Packaging Merge", "Ready to Dispatch", ""),

        # Shipping docs branch
        ("Prepare Shipping Docs and Labels", "International Order?", ""),
        ("International Order?", "Prepare Customs Documentation", "International"),
        ("International Order?", "Docs Merge", "Domestic"),
        ("Prepare Customs Documentation", "Docs Merge", ""),
        ("Docs Merge", "Ready to Dispatch", ""),

        # Join -> dispatch -> post-dispatch
        ("Ready to Dispatch", "Dispatch Order", ""),
        ("Dispatch Order", "Send Shipping Confirmation", ""),
        ("Send Shipping Confirmation", "Update Inventory Levels", ""),
        ("Update Inventory Levels", "Confirm Successful Delivery", ""),
        ("Confirm Successful Delivery", "Issues Reported Upon Delivery?", ""),

        # Delivery decision
        ("Issues Reported Upon Delivery?", "Send Feedback Request Email", "No Issues"),
        ("Send Feedback Request Email", "Order Complete", ""),
        ("Issues Reported Upon Delivery?", "Send Return Shipping Label", "Issues"),

        # Returns process
        ("Send Return Shipping Label", "Receive Returned Items", ""),
        ("Receive Returned Items", "Inspect Returned Items", ""),
        ("Inspect Returned Items", "Refund or Replacement?", ""),
        ("Refund or Replacement?", "Process Refund", "Refund"),
        ("Refund or Replacement?", "Send Replacement", "Replacement"),
        ("Process Refund", "Return Merge", ""),
        ("Send Replacement", "Return Merge", ""),
        ("Return Merge", "Return Completed", "")
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow: " + srcName + " -> " + tgtName

    diagramHandle.save()
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
        createECommerceOrderFulfillmentProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
