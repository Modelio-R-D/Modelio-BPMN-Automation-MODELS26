#
# ContractPartsProcurement.py
#
# Description:
#   BPMN process diagram for Contract Parts Procurement workflow.
#   Handles querying web shops, ordering parts, receiving deliveries,
#   managing stock levels, and assembly operations.
#
#   4 lanes: Procurement, Warehouse, Assembly, Communication
#
# Applicable on: Package
#
# Version: 1.0 - December 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.events import BpmnIntermediateCatchEvent
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


def createTimerEvent(process, name):
    """Create a BPMN Timer Intermediate Catch Event."""
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
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
    """Create a BPMN Exclusive Gateway (XOR decision)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (AND split/join)."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createSequenceFlow(process, source, target, name="", guard=""):
    """Create a BPMN Sequence Flow."""
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
    """Calculate the center Y position for a lane."""
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format a compact summary of all lanes."""
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
    
    for col, name, elem in sortedElems[:8]:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:8]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
    return "Elements: " + ", ".join(parts) + "..."


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
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + str(len(missing))
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT"
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
            laneName = elementLayout.get(name, (0, "Procurement"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + ": OK"
            except Exception as e:
                print "  [Unmask] " + name[:20] + ": ERROR"
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createContractProcess(parentPackage):
    """Create the Contract Parts Procurement BPMN process."""
    
    processName = "Contract_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN CONTRACT PARTS PROCUREMENT PROCESS"
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
    
    procurementLane = createLane(laneSet, "Procurement")
    warehouseLane = createLane(laneSet, "Warehouse")
    assemblyLane = createLane(laneSet, "Assembly")
    communicationLane = createLane(laneSet, "Communication")
    
    lanes = {
        "Procurement": procurementLane,
        "Warehouse": warehouseLane,
        "Assembly": assemblyLane,
        "Communication": communicationLane
    }
    laneOrder = ["Procurement", "Warehouse", "Assembly", "Communication"]
    
    print "[" + str(step()) + "] Lanes: Procurement, Warehouse, Assembly, Communication"
    
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
    
    # --- Procurement Lane ---
    addElement(createStartEvent, "Project Start", procurementLane, "Procurement")
    addElement(createUserTask, "Define Parts List", procurementLane, "Procurement")
    addElement(createServiceTask, "Query All Shops", procurementLane, "Procurement")
    addElement(createServiceTask, "Collect Responses", procurementLane, "Procurement")
    addElement(createUserTask, "Analyze Quotes", procurementLane, "Procurement")
    addElement(createUserTask, "Create Order Plan", procurementLane, "Procurement")
    addElement(createServiceTask, "Place Orders", procurementLane, "Procurement")
    addElement(createServiceTask, "Reorder Cheapest", procurementLane, "Procurement")
    addElement(createServiceTask, "Reorder Fastest", procurementLane, "Procurement")
    print "[" + str(step()) + "] Procurement lane: 9 elements"
    
    # --- Warehouse Lane ---
    addElement(createTimerEvent, "Parts Arrive", warehouseLane, "Warehouse")
    addElement(createManualTask, "Receive Batch", warehouseLane, "Warehouse")
    addElement(createServiceTask, "Update Stock", warehouseLane, "Warehouse")
    addElement(createExclusiveGateway, "Stock Level?", warehouseLane, "Warehouse")
    addElement(createParallelGateway, "Check Complete", warehouseLane, "Warehouse")
    addElement(createExclusiveGateway, "More Batches?", warehouseLane, "Warehouse")
    print "[" + str(step()) + "] Warehouse lane: 6 elements"
    
    # --- Assembly Lane ---
    addElement(createExclusiveGateway, "First Parts?", assemblyLane, "Assembly")
    addElement(createManualTask, "Start Building", assemblyLane, "Assembly")
    addElement(createManualTask, "Continue Build", assemblyLane, "Assembly")
    addElement(createExclusiveGateway, "Parts Available?", assemblyLane, "Assembly")
    addElement(createManualTask, "Wait for Parts", assemblyLane, "Assembly")
    addElement(createExclusiveGateway, "Build Complete?", assemblyLane, "Assembly")
    addElement(createEndEvent, "Project Done", assemblyLane, "Assembly")
    print "[" + str(step()) + "] Assembly lane: 7 elements"
    
    # --- Communication Lane ---
    addElement(createUserTask, "Write Complaint", communicationLane, "Communication")
    addElement(createMessageEndEvent, "Send to Friends", communicationLane, "Communication")
    print "[" + str(step()) + "] Communication lane: 2 elements"
    
    print ""
    print "  Total elements: " + str(len(elements))
    
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
    
    # Layout: element name -> (column_index, lane_name)
    elementLayout = {
        # Procurement Lane (top row)
        "Project Start": (0, "Procurement"),
        "Define Parts List": (1, "Procurement"),
        "Query All Shops": (2, "Procurement"),
        "Collect Responses": (3, "Procurement"),
        "Analyze Quotes": (4, "Procurement"),
        "Create Order Plan": (5, "Procurement"),
        "Place Orders": (6, "Procurement"),
        "Reorder Cheapest": (10, "Procurement"),
        "Reorder Fastest": (11, "Procurement"),
        
        # Warehouse Lane
        "Parts Arrive": (7, "Warehouse"),
        "Receive Batch": (8, "Warehouse"),
        "Update Stock": (9, "Warehouse"),
        "Stock Level?": (10, "Warehouse"),
        "Check Complete": (12, "Warehouse"),
        "More Batches?": (13, "Warehouse"),
        
        # Assembly Lane
        "First Parts?": (8, "Assembly"),
        "Start Building": (9, "Assembly"),
        "Continue Build": (10, "Assembly"),
        "Parts Available?": (11, "Assembly"),
        "Wait for Parts": (12, "Assembly"),
        "Build Complete?": (13, "Assembly"),
        "Project Done": (14, "Assembly"),
        
        # Communication Lane
        "Write Complaint": (12, "Communication"),
        "Send to Friends": (13, "Communication"),
    }
    
    print "[" + str(step()) + "] Waiting for elements..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    foundCount = len(elementGraphics)
    
    if foundCount < len(elements):
        print ""
        print "[" + str(step()) + "] Trying manual unmask..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        if unmaskedCount > 0:
            diagramHandle.save()
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
    
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Procurement main flow
        ("Project Start", "Define Parts List", ""),
        ("Define Parts List", "Query All Shops", ""),
        ("Query All Shops", "Collect Responses", ""),
        ("Collect Responses", "Analyze Quotes", ""),
        ("Analyze Quotes", "Create Order Plan", ""),
        ("Create Order Plan", "Place Orders", ""),
        ("Place Orders", "Parts Arrive", ""),
        
        # Warehouse receiving flow
        ("Parts Arrive", "Receive Batch", ""),
        ("Receive Batch", "Update Stock", ""),
        ("Update Stock", "Stock Level?", ""),
        
        # Stock level decisions (from gateway - need guards)
        ("Stock Level?", "Reorder Cheapest", "Below 5"),
        ("Stock Level?", "Reorder Fastest", "Below 3"),
        ("Stock Level?", "Write Complaint", "Zero"),
        ("Stock Level?", "Check Complete", "OK"),
        
        # Reorder flows back to waiting
        ("Reorder Cheapest", "Check Complete", ""),
        ("Reorder Fastest", "Check Complete", ""),
        
        # Check if more batches
        ("Check Complete", "More Batches?", ""),
        ("More Batches?", "Parts Arrive", "Yes"),
        ("More Batches?", "Build Complete?", "No"),
        
        # First parts check
        ("Receive Batch", "First Parts?", ""),
        ("First Parts?", "Start Building", "Yes"),
        ("First Parts?", "Continue Build", "No"),
        
        # Assembly flow
        ("Start Building", "Parts Available?", ""),
        ("Continue Build", "Parts Available?", ""),
        ("Parts Available?", "Wait for Parts", "No"),
        ("Parts Available?", "Build Complete?", "Yes"),
        ("Wait for Parts", "Parts Available?", ""),
        
        # Build completion
        ("Build Complete?", "Continue Build", "No"),
        ("Build Complete?", "Project Done", "Yes"),
        
        # Communication flow
        ("Write Complaint", "Send to Friends", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
    
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
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createContractProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
