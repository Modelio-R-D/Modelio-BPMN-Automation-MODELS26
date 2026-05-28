#
# OrderFulfillmentProcess.py
#
# Description:
#   BPMN process diagram for E-Commerce Order Fulfillment workflow.
#   5 lanes: Customer Service, Payment, Warehouse, Shipping, Quality/Returns
#
# Workflow covers:
#   - Order placement and payment processing
#   - Inventory check with back-order handling
#   - Warehouse picking and quality control
#   - Packaging (including gift wrap option)
#   - Shipping document preparation (with customs for international)
#   - Dispatch and delivery confirmation
#   - Returns process for customer issues
#
# Applicable on: Package
#
# Version: 1.0 - January 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
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
MAX_ATTEMPTS = 5

# Layout configuration
SPACING = 140
START_X = 60

# Task dimensions
TASK_WIDTH = 110
TASK_HEIGHT = 55


# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    """Create a BPMN Lane in the given lane set."""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def addToLane(element, lane):
    """Assign an element to a lane."""
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False


def createStartEvent(process, name):
    """Create a BPMN Start Event (green circle)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createEndEvent(process, name):
    """Create a BPMN End Event (red circle)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createMessageEndEvent(process, name):
    """Create a BPMN Message End Event."""
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
    """Create a BPMN User Task (person icon)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon)."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (XOR diamond)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (AND diamond)."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createSequenceFlow(process, source, target, name="", guard=""):
    """Create a BPMN Sequence Flow with optional guard condition."""
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
    """Parse a Rectangle bounds string into a dictionary."""
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
    """Get the diagram graphics for an element."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def getBounds(diagramHandle, element):
    """Get the bounds of an element in the diagram."""
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None


def getLaneCenterY(diagramHandle, lane):
    """Calculate the center Y position for placing elements in a lane."""
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format a compact summary of all lanes with their Y ranges."""
    parts = []
    for laneName in laneOrder:
        lane = lanes[laneName]
        info = getBounds(diagramHandle, lane)
        if info:
            yEnd = int(info["y"] + info["h"])
            parts.append(laneName[:8] + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
        else:
            parts.append(laneName[:8] + "(--)")
    return "Lanes: " + "; ".join(parts)


def formatElementsSummary(diagramHandle, elements, elementLayout):
    """Format a compact summary of element Y positions."""
    parts = []
    sortedElems = []
    for elem in elements:
        name = elem.getName()
        col = elementLayout.get(name, (99, "?"))[0]
        sortedElems.append((col, name, elem))
    sortedElems.sort()
    
    for col, name, elem in sortedElems[:10]:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:8]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:8] + "=--")
    if len(sortedElems) > 10:
        parts.append("..." + str(len(sortedElems) - 10) + " more")
    return "Elements: " + ", ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
    """Wait until all elements are available in the diagram."""
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
            missing = [e.getName()[:10] for e in elements if e.getName() not in elementGraphics]
            missingStr = ", ".join(missing[:5])
            if len(missing) > 5:
                missingStr += "... +" + str(len(missing) - 5)
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + missingStr
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """Manually unmask elements that were not auto-unmasked."""
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
            laneName = elementLayout.get(name, (0, "CustomerSvc"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + " (" + laneName[:8] + "): OK"
                else:
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + " (" + laneName[:8] + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:15] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createOrderFulfillmentProcess(parentPackage):
    """Create the Order Fulfillment BPMN process with diagram."""
    
    processName = "OrderFulfillment_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN ORDER FULFILLMENT PROCESS"
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
    print "[" + str(step()) + "] Process: " + processName
    
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    
    # Create 5 lanes for the process
    customerSvcLane = createLane(laneSet, "CustomerSvc")
    paymentLane = createLane(laneSet, "Payment")
    warehouseLane = createLane(laneSet, "Warehouse")
    shippingLane = createLane(laneSet, "Shipping")
    qualityLane = createLane(laneSet, "Quality")
    
    lanes = {
        "CustomerSvc": customerSvcLane,
        "Payment": paymentLane,
        "Warehouse": warehouseLane,
        "Shipping": shippingLane,
        "Quality": qualityLane
    }
    laneOrder = ["CustomerSvc", "Payment", "Warehouse", "Shipping", "Quality"]
    
    print "[" + str(step()) + "] Lanes: CustomerSvc, Payment, Warehouse, Shipping, Quality"
    
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
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- CustomerSvc Lane ---
    addElement(createStartEvent, "Order Placed", customerSvcLane)
    addElement(createServiceTask, "Record Order", customerSvcLane)
    addElement(createServiceTask, "Notify Payment Fail", customerSvcLane)
    addElement(createEndEvent, "Order Cancelled", customerSvcLane)
    addElement(createServiceTask, "Notify Backorder", customerSvcLane)
    addElement(createServiceTask, "Send Ship Confirm", customerSvcLane)
    addElement(createServiceTask, "Send Feedback Req", customerSvcLane)
    addElement(createExclusiveGateway, "Issue Reported?", customerSvcLane)
    addElement(createMessageEndEvent, "Order Complete", customerSvcLane)
    print "[" + str(step()) + "] CustomerSvc lane: 9 elements"
    
    # --- Payment Lane ---
    addElement(createServiceTask, "Process Payment", paymentLane)
    addElement(createExclusiveGateway, "Payment OK?", paymentLane)
    print "[" + str(step()) + "] Payment lane: 2 elements"
    
    # --- Warehouse Lane ---
    addElement(createServiceTask, "Check Inventory", warehouseLane)
    addElement(createExclusiveGateway, "In Stock?", warehouseLane)
    addElement(createServiceTask, "Init Backorder", warehouseLane)
    addElement(createUserTask, "Receive Backorder", warehouseLane)
    addElement(createManualTask, "Pick Items", warehouseLane)
    addElement(createParallelGateway, "Split Packaging", warehouseLane)
    addElement(createManualTask, "Package Items", warehouseLane)
    addElement(createExclusiveGateway, "Gift Wrap?", warehouseLane)
    addElement(createManualTask, "Add Gift Wrap", warehouseLane)
    addElement(createExclusiveGateway, "Merge Gift", warehouseLane)
    addElement(createParallelGateway, "Join Ship Ready", warehouseLane)
    addElement(createManualTask, "Dispatch Order", warehouseLane)
    addElement(createServiceTask, "Update Inventory", warehouseLane)
    print "[" + str(step()) + "] Warehouse lane: 13 elements"
    
    # --- Shipping Lane ---
    addElement(createServiceTask, "Prep Ship Docs", shippingLane)
    addElement(createExclusiveGateway, "International?", shippingLane)
    addElement(createUserTask, "Prep Customs Docs", shippingLane)
    addElement(createExclusiveGateway, "Merge Customs", shippingLane)
    addElement(createServiceTask, "Confirm Delivery", shippingLane)
    print "[" + str(step()) + "] Shipping lane: 5 elements"
    
    # --- Quality/Returns Lane ---
    addElement(createUserTask, "QC Check Items", qualityLane)
    addElement(createServiceTask, "Send Return Label", qualityLane)
    addElement(createManualTask, "Receive Returns", qualityLane)
    addElement(createUserTask, "Inspect Returns", qualityLane)
    addElement(createServiceTask, "Process Refund", qualityLane)
    addElement(createMessageEndEvent, "Return Complete", qualityLane)
    print "[" + str(step()) + "] Quality lane: 6 elements"
    
    totalElements = len(elements)
    print ""
    print "  Total elements: " + str(totalElements)
    
    # =========================================================================
    # PHASE 3: CREATE DIAGRAM
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
    # PHASE 4: WAIT FOR ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""
    
    # Layout: element name -> (column, lane)
    elementLayout = {
        # CustomerSvc Lane (top row flow)
        "Order Placed": (0, "CustomerSvc"),
        "Record Order": (1, "CustomerSvc"),
        "Notify Payment Fail": (3, "CustomerSvc"),
        "Order Cancelled": (4, "CustomerSvc"),
        "Notify Backorder": (6, "CustomerSvc"),
        "Send Ship Confirm": (15, "CustomerSvc"),
        "Send Feedback Req": (17, "CustomerSvc"),
        "Issue Reported?": (18, "CustomerSvc"),
        "Order Complete": (19, "CustomerSvc"),
        
        # Payment Lane
        "Process Payment": (2, "Payment"),
        "Payment OK?": (3, "Payment"),
        
        # Warehouse Lane
        "Check Inventory": (4, "Warehouse"),
        "In Stock?": (5, "Warehouse"),
        "Init Backorder": (6, "Warehouse"),
        "Receive Backorder": (7, "Warehouse"),
        "Pick Items": (8, "Warehouse"),
        "Split Packaging": (9, "Warehouse"),
        "Package Items": (10, "Warehouse"),
        "Gift Wrap?": (11, "Warehouse"),
        "Add Gift Wrap": (12, "Warehouse"),
        "Merge Gift": (13, "Warehouse"),
        "Join Ship Ready": (14, "Warehouse"),
        "Dispatch Order": (15, "Warehouse"),
        "Update Inventory": (16, "Warehouse"),
        
        # Shipping Lane
        "Prep Ship Docs": (10, "Shipping"),
        "International?": (11, "Shipping"),
        "Prep Customs Docs": (12, "Shipping"),
        "Merge Customs": (13, "Shipping"),
        "Confirm Delivery": (17, "Shipping"),
        
        # Quality Lane
        "QC Check Items": (9, "Quality"),
        "Send Return Label": (19, "Quality"),
        "Receive Returns": (20, "Quality"),
        "Inspect Returns": (21, "Quality"),
        "Process Refund": (22, "Quality"),
        "Return Complete": (23, "Quality"),
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    
    if foundCount == totalElements:
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(totalElements) + " elements ready"
        
        print ""
        print "[" + str(step()) + "] Trying manual unmask..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements"
        
        foundCount = len(elementGraphics)
        if foundCount == totalElements:
            print "[" + str(step()) + "] All elements now available"
        else:
            stillMissing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "[" + str(step()) + "] Still missing: " + ", ".join(stillMissing[:5])
    
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    
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
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
    
    print ""
    
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    
    for col, name, laneName in sortedElements:
        if name not in elementGraphics:
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
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
        
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
        diagramHandle.save()
    
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(totalElements)
    
    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Initial order flow
        ("Order Placed", "Record Order", ""),
        ("Record Order", "Process Payment", ""),
        
        # Payment decision
        ("Process Payment", "Payment OK?", ""),
        ("Payment OK?", "Notify Payment Fail", "Failed"),
        ("Notify Payment Fail", "Order Cancelled", ""),
        ("Payment OK?", "Check Inventory", "Success"),
        
        # Inventory decision
        ("Check Inventory", "In Stock?", ""),
        ("In Stock?", "Init Backorder", "No"),
        ("Init Backorder", "Notify Backorder", ""),
        ("Notify Backorder", "Receive Backorder", ""),
        ("Receive Backorder", "Pick Items", ""),
        ("In Stock?", "Pick Items", "Yes"),
        
        # Warehouse picking to QC
        ("Pick Items", "QC Check Items", ""),
        ("QC Check Items", "Split Packaging", ""),
        
        # Parallel split for packaging and shipping docs
        ("Split Packaging", "Package Items", ""),
        ("Split Packaging", "Prep Ship Docs", ""),
        
        # Packaging with gift wrap option
        ("Package Items", "Gift Wrap?", ""),
        ("Gift Wrap?", "Add Gift Wrap", "Yes"),
        ("Add Gift Wrap", "Merge Gift", ""),
        ("Gift Wrap?", "Merge Gift", "No"),
        ("Merge Gift", "Join Ship Ready", ""),
        
        # Shipping docs with international option
        ("Prep Ship Docs", "International?", ""),
        ("International?", "Prep Customs Docs", "Yes"),
        ("Prep Customs Docs", "Merge Customs", ""),
        ("International?", "Merge Customs", "No"),
        ("Merge Customs", "Join Ship Ready", ""),
        
        # Dispatch and delivery
        ("Join Ship Ready", "Dispatch Order", ""),
        ("Dispatch Order", "Send Ship Confirm", ""),
        ("Dispatch Order", "Update Inventory", ""),
        ("Send Ship Confirm", "Confirm Delivery", ""),
        ("Confirm Delivery", "Send Feedback Req", ""),
        
        # Issue check
        ("Send Feedback Req", "Issue Reported?", ""),
        ("Issue Reported?", "Order Complete", "No"),
        
        # Returns process
        ("Issue Reported?", "Send Return Label", "Yes"),
        ("Send Return Label", "Receive Returns", ""),
        ("Receive Returns", "Inspect Returns", ""),
        ("Inspect Returns", "Process Refund", ""),
        ("Process Refund", "Return Complete", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            if not src:
                print "  WARNING: Missing source: " + srcName
            if not tgt:
                print "  WARNING: Missing target: " + tgtName
    
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
    
    diagramHandle.close()
    print ""
    print "[" + str(step()) + "] Diagram closed"
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print ""
    print "=================================================================="
    print "COMPLETE"
    print "=================================================================="
    print "Process:  " + processName
    print "Lanes:    " + str(len(lanes))
    print "Elements: " + str(totalElements) + " (" + str(foundCount) + " in diagram)"
    print "Flows:    " + str(len(flows))
    print "=================================================================="
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createOrderFulfillmentProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
