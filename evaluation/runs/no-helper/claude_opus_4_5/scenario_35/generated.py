#
# ChainsawProduction.py
#
# Description:
#   BPMN process diagram for Custom Chainsaw Production workflow.
#   4 lanes: Customer, Sales, Procurement, Production
#
# Process Flow:
#   1. Customer specifies chainsaw properties (guide bar length, chain width, 
#      electric/motor type, handle type, safety features)
#   2. Sales receives order and confirms specifications
#   3. Procurement orders parts in parallel from various sources
#   4. Production inspects parts, assembles chainsaw, sends updates
#   5. First prototype sent to customer for approval
#   6. If approved, remaining order is produced
#
# Applicable on: Package
#
# Version: 1.0 - Custom Chainsaw Production
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
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 130
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


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon - physical task without IT)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon - automated task)."""
    task = modelingSession.getModel().createBpmnServiceTask()
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
            parts.append(laneName + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
        else:
            parts.append(laneName + "(--)")
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
            shortName = name[:10]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:10] + "=--")
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
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """Try to manually unmask elements that were not auto-unmasked."""
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
    """Create the Custom Chainsaw Production BPMN process with diagram."""
    
    processName = "ChainsawProduction_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN CUSTOM CHAINSAW PRODUCTION PROCESS"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="
    print ""
    print "Chainsaw Properties:"
    print "  - Guide Bar Length (Schwertlaenge)"
    print "  - Chain Width"
    print "  - Power Type (Electric/Motor)"
    print "  - Handle Type"
    print "  - Safety Features"
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
    salesLane = createLane(laneSet, "Sales")
    procurementLane = createLane(laneSet, "Procurement")
    productionLane = createLane(laneSet, "Production")
    
    lanes = {
        "Customer": customerLane,
        "Sales": salesLane,
        "Procurement": procurementLane,
        "Production": productionLane
    }
    laneOrder = ["Customer", "Sales", "Procurement", "Production"]
    
    print "[" + str(step()) + "] Lanes: Customer, Sales, Procurement, Production"
    
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
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Customer Lane (5 elements) ---
    addElement(createStartEvent, "Order Initiated", customerLane, "Customer")
    addElement(createUserTask, "Specify Properties", customerLane, "Customer")
    addElement(createUserTask, "Receive Prototype", customerLane, "Customer")
    addElement(createExclusiveGateway, "Approved?", customerLane, "Customer")
    addElement(createEndEvent, "Order Complete", customerLane, "Customer")
    print "[" + str(step()) + "] Customer lane: 5 elements"
    
    # --- Sales Lane (3 elements) ---
    addElement(createUserTask, "Receive Order", salesLane, "Sales")
    addElement(createUserTask, "Confirm Specs", salesLane, "Sales")
    addElement(createServiceTask, "Create Work Order", salesLane, "Sales")
    print "[" + str(step()) + "] Sales lane: 3 elements"
    
    # --- Procurement Lane (7 elements) ---
    addElement(createParallelGateway, "Split Orders", procurementLane, "Procurement")
    addElement(createServiceTask, "Order Guide Bar", procurementLane, "Procurement")
    addElement(createServiceTask, "Order Chain", procurementLane, "Procurement")
    addElement(createServiceTask, "Order Motor/Elec", procurementLane, "Procurement")
    addElement(createServiceTask, "Order Handle", procurementLane, "Procurement")
    addElement(createServiceTask, "Order Safety Parts", procurementLane, "Procurement")
    addElement(createParallelGateway, "Join Parts", procurementLane, "Procurement")
    print "[" + str(step()) + "] Procurement lane: 7 elements"
    
    # --- Production Lane (8 elements) ---
    addElement(createManualTask, "Inspect Parts", productionLane, "Production")
    addElement(createManualTask, "Assemble Chainsaw", productionLane, "Production")
    addElement(createServiceTask, "Send Update", productionLane, "Production")
    addElement(createManualTask, "Quality Test", productionLane, "Production")
    addElement(createServiceTask, "Ship Prototype", productionLane, "Production")
    addElement(createUserTask, "Request Changes", productionLane, "Production")
    addElement(createManualTask, "Produce Remaining", productionLane, "Production")
    addElement(createServiceTask, "Ship Final Order", productionLane, "Production")
    print "[" + str(step()) + "] Production lane: 8 elements"
    
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
        "Order Initiated": (0, "Customer"),
        "Specify Properties": (1, "Customer"),
        "Receive Prototype": (11, "Customer"),
        "Approved?": (12, "Customer"),
        "Order Complete": (14, "Customer"),
        # Sales Lane
        "Receive Order": (2, "Sales"),
        "Confirm Specs": (3, "Sales"),
        "Create Work Order": (4, "Sales"),
        # Procurement Lane - Parallel ordering
        "Split Orders": (5, "Procurement"),
        "Order Guide Bar": (6, "Procurement"),
        "Order Chain": (6, "Procurement"),       # Same column, different Y offset
        "Order Motor/Elec": (6, "Procurement"),
        "Order Handle": (6, "Procurement"),
        "Order Safety Parts": (6, "Procurement"),
        "Join Parts": (7, "Procurement"),
        # Production Lane
        "Inspect Parts": (8, "Production"),
        "Assemble Chainsaw": (9, "Production"),
        "Send Update": (9, "Production"),        # Parallel with assembly
        "Quality Test": (10, "Production"),
        "Ship Prototype": (11, "Production"),
        "Request Changes": (13, "Production"),
        "Produce Remaining": (13, "Production"),
        "Ship Final Order": (14, "Production"),
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
    
    # Read lane Y values
    laneY = {}
    for laneName in laneOrder:
        lane = lanes[laneName]
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"
    
    print ""
    
    # Special handling for parallel procurement tasks - spread vertically
    procurementTasks = ["Order Guide Bar", "Order Chain", "Order Motor/Elec", "Order Handle", "Order Safety Parts"]
    procurementOffsets = {}
    if "Procurement" in laneY:
        baseY = laneY["Procurement"]
        # Spread tasks vertically within the lane
        for i, taskName in enumerate(procurementTasks):
            offset = (i - 2) * 25  # -50, -25, 0, 25, 50
            procurementOffsets[taskName] = offset
    
    # Sort elements by column
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
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue
        
        # Calculate target position
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)
        
        # Apply vertical offset for parallel procurement tasks
        if name in procurementOffsets:
            targetY += procurementOffsets[name]
        
        # Handle "Send Update" - offset slightly below assembly
        if name == "Send Update":
            targetY += 35
        
        # Determine dimensions
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
        
        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""
        
        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")" + laneChanged
        
        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes
        
        previousLanes = currentLanes
    
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
        # Customer -> Sales
        ("Order Initiated", "Specify Properties", ""),
        ("Specify Properties", "Receive Order", ""),
        # Sales flow
        ("Receive Order", "Confirm Specs", ""),
        ("Confirm Specs", "Create Work Order", ""),
        ("Create Work Order", "Split Orders", ""),
        # Parallel procurement split
        ("Split Orders", "Order Guide Bar", ""),
        ("Split Orders", "Order Chain", ""),
        ("Split Orders", "Order Motor/Elec", ""),
        ("Split Orders", "Order Handle", ""),
        ("Split Orders", "Order Safety Parts", ""),
        # Parallel procurement join
        ("Order Guide Bar", "Join Parts", ""),
        ("Order Chain", "Join Parts", ""),
        ("Order Motor/Elec", "Join Parts", ""),
        ("Order Handle", "Join Parts", ""),
        ("Order Safety Parts", "Join Parts", ""),
        # Production flow
        ("Join Parts", "Inspect Parts", ""),
        ("Inspect Parts", "Assemble Chainsaw", ""),
        ("Assemble Chainsaw", "Send Update", ""),
        ("Assemble Chainsaw", "Quality Test", ""),
        ("Quality Test", "Ship Prototype", ""),
        # Prototype to customer
        ("Ship Prototype", "Receive Prototype", ""),
        ("Receive Prototype", "Approved?", ""),
        # Customer decision - GUARDS
        ("Approved?", "Request Changes", "No"),
        ("Approved?", "Produce Remaining", "Yes"),
        # Rejection loop
        ("Request Changes", "Assemble Chainsaw", ""),
        # Final production
        ("Produce Remaining", "Ship Final Order", ""),
        ("Ship Final Order", "Order Complete", ""),
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
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)
    
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
    print "Chainsaw Configuration Options:"
    print "  1. Guide Bar Length (30-90 cm)"
    print "  2. Chain Width (1.1-2.0 mm)"
    print "  3. Power Type (Electric/Gasoline Motor)"
    print "  4. Handle Type (Standard/Anti-Vibration/Heated)"
    print "  5. Safety Features (Chain Brake/Kickback Guard/Hand Guard)"
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
