# OrderFulfillmentProcess.py
#
# Description:
#   BPMN process diagram for E-commerce Order Fulfillment.
#   5 lanes: Customer, System, Warehouse, Shipping, Customer Service
#   Features: Parallel gateways, exclusive gateways, loops, multiple end events
#
# Workflow:
#   1. Order placed and recorded
#   2. Payment processing with failure handling
#   3. Stock check with back-order loop
#   4. Parallel fulfillment (Warehouse + Shipping)
#   5. Dispatch and delivery confirmation
#   6. Returns process for issues
#
# Applicable on: Package
#
# Version: 1.0
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
WAIT_TIME_MS = 100
MAX_ATTEMPTS = 5

# Layout configuration
SPACING = 140
START_X = 80

# Task dimensions
TASK_WIDTH = 110
TASK_HEIGHT = 55


# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    """Create a BPMN Lane (swim lane) in the given lane set."""
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


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon - automated task)."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon - physical task without IT)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (X diamond - XOR decision)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (+ diamond - AND split/join)."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createSequenceFlow(process, source, target, name="", guard=""):
    """
    Create a BPMN Sequence Flow (arrow between elements).
    
    Parameters:
    - process: The BPMN process container
    - source: Source element (task, gateway, event)
    - target: Target element (task, gateway, event)
    - name: Optional name for the flow (rarely used)
    - guard: Condition expression displayed on flows from gateways
    """
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
    """Get the bounds (x, y, width, height) of an element in the diagram."""
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
    
    for col, name, elem in sortedElems:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:8]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:8] + "=--")
    return "Elements: " + ", ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
    """
    Wait until all elements are available in the diagram.
    Returns: (dict of elementGraphics, number of attempts)
    """
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
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing[:5]) + ("..." if len(missing) > 5 else "")
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """
    Try to manually unmask elements that were not auto-unmasked.
    Elements must be unmasked at a Y position inside their lane.
    """
    unmaskedCount = 0
    
    # Get each lane's center Y position
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
    
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "System"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:15] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createOrderFulfillmentProcess(parentPackage):
    """
    Create the Order Fulfillment BPMN process with diagram.
    """
    
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
    
    # Create 5 lanes (top to bottom)
    customerLane = createLane(laneSet, "Customer")
    systemLane = createLane(laneSet, "System")
    warehouseLane = createLane(laneSet, "Warehouse")
    shippingLane = createLane(laneSet, "Shipping")
    csLane = createLane(laneSet, "Cust Service")
    
    lanes = {
        "Customer": customerLane,
        "System": systemLane,
        "Warehouse": warehouseLane,
        "Shipping": shippingLane,
        "Cust Service": csLane
    }
    laneOrder = ["Customer", "System", "Warehouse", "Shipping", "Cust Service"]
    
    print "[" + str(step()) + "] Lanes: Customer, System, Warehouse, Shipping, Cust Service"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    
    def addElement(creator, name, lane, laneName):
        """Helper to create element, add to lane, and register."""
        elem = creator(process, name)
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Customer Lane (3 elements) ---
    addElement(createStartEvent, "Order Placed", customerLane, "Customer")
    addElement(createEndEvent, "Order Cancelled", customerLane, "Customer")
    addElement(createEndEvent, "Order Complete", customerLane, "Customer")
    print "[" + str(step()) + "] Customer lane: 3 elements"
    
    # --- System Lane (14 elements) ---
    addElement(createServiceTask, "Record Order", systemLane, "System")
    addElement(createServiceTask, "Process Payment", systemLane, "System")
    addElement(createExclusiveGateway, "Payment OK?", systemLane, "System")
    addElement(createServiceTask, "Notify Pay Failed", systemLane, "System")
    addElement(createServiceTask, "Check Stock", systemLane, "System")
    addElement(createExclusiveGateway, "In Stock?", systemLane, "System")
    addElement(createServiceTask, "Back-Order", systemLane, "System")
    addElement(createServiceTask, "Inform Delay", systemLane, "System")
    addElement(createParallelGateway, "Fork", systemLane, "System")
    addElement(createParallelGateway, "Join", systemLane, "System")
    addElement(createServiceTask, "Ship Confirm", systemLane, "System")
    addElement(createServiceTask, "Update Inventory", systemLane, "System")
    addElement(createServiceTask, "Feedback Request", systemLane, "System")
    addElement(createExclusiveGateway, "Issues?", systemLane, "System")
    print "[" + str(step()) + "] System lane: 14 elements"
    
    # --- Warehouse Lane (5 elements) ---
    addElement(createManualTask, "Pick Items", warehouseLane, "Warehouse")
    addElement(createUserTask, "Quality Check", warehouseLane, "Warehouse")
    addElement(createUserTask, "Package Items", warehouseLane, "Warehouse")
    addElement(createExclusiveGateway, "Gift Wrap?", warehouseLane, "Warehouse")
    addElement(createUserTask, "Gift Wrap", warehouseLane, "Warehouse")
    print "[" + str(step()) + "] Warehouse lane: 5 elements"
    
    # --- Shipping Lane (4 elements) ---
    addElement(createUserTask, "Prep Documents", shippingLane, "Shipping")
    addElement(createExclusiveGateway, "International?", shippingLane, "Shipping")
    addElement(createUserTask, "Customs Docs", shippingLane, "Shipping")
    addElement(createUserTask, "Dispatch Order", shippingLane, "Shipping")
    print "[" + str(step()) + "] Shipping lane: 4 elements"
    
    # --- Customer Service Lane (7 elements) ---
    addElement(createUserTask, "Send Return Label", csLane, "Cust Service")
    addElement(createUserTask, "Receive Return", csLane, "Cust Service")
    addElement(createUserTask, "Inspect Items", csLane, "Cust Service")
    addElement(createExclusiveGateway, "Resolution?", csLane, "Cust Service")
    addElement(createServiceTask, "Process Refund", csLane, "Cust Service")
    addElement(createServiceTask, "Process Replace", csLane, "Cust Service")
    addElement(createEndEvent, "Return Done", csLane, "Cust Service")
    print "[" + str(step()) + "] Cust Service lane: 7 elements"
    
    print ""
    print "  Total elements: " + str(len(elements))
    
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
    # PHASE 4: WAIT FOR ELEMENTS TO BE AVAILABLE
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""
    
    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Customer Lane
        "Order Placed": (0, "Customer"),
        "Order Cancelled": (5, "Customer"),
        "Order Complete": (20, "Customer"),
        # System Lane
        "Record Order": (1, "System"),
        "Process Payment": (2, "System"),
        "Payment OK?": (3, "System"),
        "Notify Pay Failed": (4, "System"),
        "Check Stock": (5, "System"),
        "In Stock?": (6, "System"),
        "Back-Order": (7, "System"),
        "Inform Delay": (8, "System"),
        "Fork": (9, "System"),
        "Join": (15, "System"),
        "Ship Confirm": (17, "System"),
        "Update Inventory": (18, "System"),
        "Feedback Request": (19, "System"),
        "Issues?": (20, "System"),
        # Warehouse Lane
        "Pick Items": (10, "Warehouse"),
        "Quality Check": (11, "Warehouse"),
        "Package Items": (12, "Warehouse"),
        "Gift Wrap?": (13, "Warehouse"),
        "Gift Wrap": (14, "Warehouse"),
        # Shipping Lane
        "Prep Documents": (10, "Shipping"),
        "International?": (11, "Shipping"),
        "Customs Docs": (12, "Shipping"),
        "Dispatch Order": (16, "Shipping"),
        # Customer Service Lane
        "Send Return Label": (21, "Cust Service"),
        "Receive Return": (22, "Cust Service"),
        "Inspect Items": (23, "Cust Service"),
        "Resolution?": (24, "Cust Service"),
        "Process Refund": (25, "Cust Service"),
        "Process Replace": (26, "Cust Service"),
        "Return Done": (27, "Cust Service"),
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    
    if foundCount < len(elements):
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready"
        print "         Missing: " + ", ".join(missing[:8])
        
        print ""
        print "[" + str(step()) + "] Trying manual unmask..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements"
        
        foundCount = len(elementGraphics)
    
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    # =========================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""
    
    # Read lane Y values
    laneY = {}
    for laneName in laneOrder:
        lane = lanes[laneName]
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
    
    print ""
    
    # Sort elements by column
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
        
        # Calculate target position
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)
        
        # Determine width and height
        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]
        
        # Set new bounds
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
        
        diagramHandle.save()
        
        print "[" + str(step()) + "] " + laneName[:6] + "/" + name[:12] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    # Flow definitions: (source, target, guard)
    flowDefs = [
        # Order initiation
        ("Order Placed", "Record Order", ""),
        ("Record Order", "Process Payment", ""),
        ("Process Payment", "Payment OK?", ""),
        
        # Payment decision
        ("Payment OK?", "Notify Pay Failed", "No"),
        ("Notify Pay Failed", "Order Cancelled", ""),
        ("Payment OK?", "Check Stock", "Yes"),
        
        # Stock check
        ("Check Stock", "In Stock?", ""),
        ("In Stock?", "Back-Order", "No"),
        ("Back-Order", "Inform Delay", ""),
        ("Inform Delay", "Check Stock", ""),  # Loop back after delay
        ("In Stock?", "Fork", "Yes"),
        
        # Parallel split - Warehouse path
        ("Fork", "Pick Items", ""),
        ("Pick Items", "Quality Check", ""),
        ("Quality Check", "Package Items", ""),
        ("Package Items", "Gift Wrap?", ""),
        ("Gift Wrap?", "Gift Wrap", "Yes"),
        ("Gift Wrap?", "Join", "No"),
        ("Gift Wrap", "Join", ""),
        
        # Parallel split - Shipping path
        ("Fork", "Prep Documents", ""),
        ("Prep Documents", "International?", ""),
        ("International?", "Customs Docs", "Yes"),
        ("International?", "Join", "No"),
        ("Customs Docs", "Join", ""),
        
        # After parallel join
        ("Join", "Dispatch Order", ""),
        ("Dispatch Order", "Ship Confirm", ""),
        ("Ship Confirm", "Update Inventory", ""),
        ("Update Inventory", "Feedback Request", ""),
        ("Feedback Request", "Issues?", ""),
        
        # Delivery outcome
        ("Issues?", "Order Complete", "No"),
        ("Issues?", "Send Return Label", "Yes"),
        
        # Returns process
        ("Send Return Label", "Receive Return", ""),
        ("Receive Return", "Inspect Items", ""),
        ("Inspect Items", "Resolution?", ""),
        ("Resolution?", "Process Refund", "Refund"),
        ("Resolution?", "Process Replace", "Replace"),
        ("Process Refund", "Return Done", ""),
        ("Process Replace", "Return Done", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName
    
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
    print "Elements: " + str(len(elements)) + " (" + str(foundCount) + " in diagram)"
    print "Flows:    " + str(len(flows))
    print "=================================================================="
    print ""
    print "PROCESS SUMMARY:"
    print "  1. Order placed -> Payment processing"
    print "  2. Payment fails -> Notify & Cancel"
    print "  3. Payment OK -> Check stock"
    print "  4. Out of stock -> Back-order loop"
    print "  5. In stock -> Parallel fulfillment:"
    print "     - Warehouse: Pick -> QC -> Package -> [Gift Wrap]"
    print "     - Shipping: Docs -> [Customs]"
    print "  6. Join -> Dispatch -> Confirmation -> Update"
    print "  7. Feedback request -> Issues?"
    print "  8. No issues -> Complete"
    print "  9. Issues -> Returns: Label -> Receive -> Inspect -> Refund/Replace"
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
