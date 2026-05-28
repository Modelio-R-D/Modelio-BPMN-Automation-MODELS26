#
# LuxuryAirplaneProcess.py
#
# Description:
#   BPMN process diagram for Luxury Airplane Manufacturing workflow.
#   Customers customize their airplane with various luxury options including
#   different bars, seats, colors, and amenities. Parts are manufactured by
#   specialized teams worldwide, then assembled and tested before delivery.
#
# Lanes:
#   - Sales: Customer interface and order management
#   - Engineering: Design and specifications
#   - Manufacturing Teams: Various specialized teams (Russian, Irish, etc.)
#   - Assembly: Final assembly of the airplane interior
#   - Quality: Testing and certification
#   - Delivery: Final delivery and customer confirmation
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


def createMessageStartEvent(process, name):
    """Create a BPMN Message Start Event."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
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
    """Create a BPMN Exclusive Gateway (X diamond)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (+ diamond)."""
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
    """Calculate the center Y position for placing elements in a lane."""
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
        parts.append("...")
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
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + str(len(missing))
        
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
            laneName = elementLayout.get(name, (0, "Sales"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + ": OK"
                else:
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + ": FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:20] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createLuxuryAirplaneProcess(parentPackage):
    """Create the Luxury Airplane Manufacturing BPMN process."""
    
    processName = "LuxuryAirplane_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN LUXURY AIRPLANE MANUFACTURING PROCESS"
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
    
    # Create lanes
    salesLane = createLane(laneSet, "Sales")
    engineeringLane = createLane(laneSet, "Engineering")
    manufacturingLane = createLane(laneSet, "Manufacturing")
    assemblyLane = createLane(laneSet, "Assembly")
    qualityLane = createLane(laneSet, "Quality")
    deliveryLane = createLane(laneSet, "Delivery")
    
    lanes = {
        "Sales": salesLane,
        "Engineering": engineeringLane,
        "Manufacturing": manufacturingLane,
        "Assembly": assemblyLane,
        "Quality": qualityLane,
        "Delivery": deliveryLane
    }
    laneOrder = ["Sales", "Engineering", "Manufacturing", "Assembly", "Quality", "Delivery"]
    
    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)
    
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
    
    # --- Sales Lane ---
    addElement(createMessageStartEvent, "Order Received", salesLane, "Sales")
    addElement(createUserTask, "Review Customer Specs", salesLane, "Sales")
    addElement(createUserTask, "Confirm Options", salesLane, "Sales")
    addElement(createServiceTask, "Generate Order", salesLane, "Sales")
    print "[" + str(step()) + "] Sales lane: 4 elements"
    
    # --- Engineering Lane ---
    addElement(createUserTask, "Analyze Requirements", engineeringLane, "Engineering")
    addElement(createServiceTask, "Create Design Specs", engineeringLane, "Engineering")
    addElement(createParallelGateway, "Split to Teams", engineeringLane, "Engineering")
    print "[" + str(step()) + "] Engineering lane: 3 elements"
    
    # --- Manufacturing Lane (parallel bar manufacturing) ---
    addElement(createManualTask, "Make Vodka Bar", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Whiskey Bar", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Champagne Bar", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Tequila Bar", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Sake Bar", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Seats", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Toilet System", manufacturingLane, "Manufacturing")
    addElement(createManualTask, "Make Entertainment", manufacturingLane, "Manufacturing")
    addElement(createParallelGateway, "Join Parts", manufacturingLane, "Manufacturing")
    print "[" + str(step()) + "] Manufacturing lane: 9 elements"
    
    # --- Assembly Lane ---
    addElement(createServiceTask, "Receive All Parts", assemblyLane, "Assembly")
    addElement(createManualTask, "Install Interior", assemblyLane, "Assembly")
    addElement(createManualTask, "Final Assembly", assemblyLane, "Assembly")
    addElement(createUserTask, "Quality Check", assemblyLane, "Assembly")
    print "[" + str(step()) + "] Assembly lane: 4 elements"
    
    # --- Quality Lane ---
    addElement(createManualTask, "Conduct Test Flight", qualityLane, "Quality")
    addElement(createServiceTask, "Create Test Protocol", qualityLane, "Quality")
    addElement(createServiceTask, "Send Protocol", qualityLane, "Quality")
    addElement(createExclusiveGateway, "Test Passed?", qualityLane, "Quality")
    addElement(createUserTask, "Fix Issues", qualityLane, "Quality")
    print "[" + str(step()) + "] Quality lane: 5 elements"
    
    # --- Delivery Lane ---
    addElement(createManualTask, "Deliver Airplane", deliveryLane, "Delivery")
    addElement(createUserTask, "Customer Acceptance", deliveryLane, "Delivery")
    addElement(createExclusiveGateway, "Accepted?", deliveryLane, "Delivery")
    addElement(createUserTask, "Handle Complaints", deliveryLane, "Delivery")
    addElement(createMessageEndEvent, "Order Complete", deliveryLane, "Delivery")
    print "[" + str(step()) + "] Delivery lane: 5 elements"
    
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
    
    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Sales Lane (columns 0-3)
        "Order Received": (0, "Sales"),
        "Review Customer Specs": (1, "Sales"),
        "Confirm Options": (2, "Sales"),
        "Generate Order": (3, "Sales"),
        
        # Engineering Lane (columns 4-6)
        "Analyze Requirements": (4, "Engineering"),
        "Create Design Specs": (5, "Engineering"),
        "Split to Teams": (6, "Engineering"),
        
        # Manufacturing Lane (columns 7-9 for bars, parallel)
        "Make Vodka Bar": (7, "Manufacturing"),
        "Make Whiskey Bar": (8, "Manufacturing"),
        "Make Champagne Bar": (9, "Manufacturing"),
        "Make Tequila Bar": (10, "Manufacturing"),
        "Make Sake Bar": (11, "Manufacturing"),
        "Make Seats": (12, "Manufacturing"),
        "Make Toilet System": (13, "Manufacturing"),
        "Make Entertainment": (14, "Manufacturing"),
        "Join Parts": (15, "Manufacturing"),
        
        # Assembly Lane (columns 16-19)
        "Receive All Parts": (16, "Assembly"),
        "Install Interior": (17, "Assembly"),
        "Final Assembly": (18, "Assembly"),
        "Quality Check": (19, "Assembly"),
        
        # Quality Lane (columns 20-24)
        "Conduct Test Flight": (20, "Quality"),
        "Create Test Protocol": (21, "Quality"),
        "Send Protocol": (22, "Quality"),
        "Test Passed?": (23, "Quality"),
        "Fix Issues": (24, "Quality"),
        
        # Delivery Lane (columns 25-29)
        "Deliver Airplane": (25, "Delivery"),
        "Customer Acceptance": (26, "Delivery"),
        "Accepted?": (27, "Delivery"),
        "Handle Complaints": (28, "Delivery"),
        "Order Complete": (29, "Delivery"),
    }
    
    print "[" + str(step()) + "] Waiting for elements..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    foundCount = len(elementGraphics)
    
    if foundCount == len(elements):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready"
    else:
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready"
        
        print ""
        print "[" + str(step()) + "] Trying manual unmask..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        
        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements"
        
        foundCount = len(elementGraphics)
        if foundCount == len(elements):
            print "[" + str(step()) + "] All elements now available"
    
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
        # Sales flow
        ("Order Received", "Review Customer Specs", ""),
        ("Review Customer Specs", "Confirm Options", ""),
        ("Confirm Options", "Generate Order", ""),
        
        # To Engineering
        ("Generate Order", "Analyze Requirements", ""),
        ("Analyze Requirements", "Create Design Specs", ""),
        ("Create Design Specs", "Split to Teams", ""),
        
        # Parallel split to manufacturing teams
        ("Split to Teams", "Make Vodka Bar", ""),
        ("Split to Teams", "Make Whiskey Bar", ""),
        ("Split to Teams", "Make Champagne Bar", ""),
        ("Split to Teams", "Make Tequila Bar", ""),
        ("Split to Teams", "Make Sake Bar", ""),
        ("Split to Teams", "Make Seats", ""),
        ("Split to Teams", "Make Toilet System", ""),
        ("Split to Teams", "Make Entertainment", ""),
        
        # All manufacturing to join
        ("Make Vodka Bar", "Join Parts", ""),
        ("Make Whiskey Bar", "Join Parts", ""),
        ("Make Champagne Bar", "Join Parts", ""),
        ("Make Tequila Bar", "Join Parts", ""),
        ("Make Sake Bar", "Join Parts", ""),
        ("Make Seats", "Join Parts", ""),
        ("Make Toilet System", "Join Parts", ""),
        ("Make Entertainment", "Join Parts", ""),
        
        # Assembly flow
        ("Join Parts", "Receive All Parts", ""),
        ("Receive All Parts", "Install Interior", ""),
        ("Install Interior", "Final Assembly", ""),
        ("Final Assembly", "Quality Check", ""),
        
        # Quality flow
        ("Quality Check", "Conduct Test Flight", ""),
        ("Conduct Test Flight", "Create Test Protocol", ""),
        ("Create Test Protocol", "Send Protocol", ""),
        ("Send Protocol", "Test Passed?", ""),
        ("Test Passed?", "Fix Issues", "No"),
        ("Fix Issues", "Quality Check", ""),
        ("Test Passed?", "Deliver Airplane", "Yes"),
        
        # Delivery flow
        ("Deliver Airplane", "Customer Acceptance", ""),
        ("Customer Acceptance", "Accepted?", ""),
        ("Accepted?", "Handle Complaints", "No"),
        ("Handle Complaints", "Customer Acceptance", ""),
        ("Accepted?", "Order Complete", "Yes"),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "  WARNING: Missing element for flow " + srcName + " -> " + tgtName
    
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
    print "PROCESS DESCRIPTION:"
    print "  1. Customer places order with luxury options"
    print "  2. Sales confirms: 5 bar types, seats, colors, toilet water, entertainment"
    print "  3. Engineering creates design specifications"
    print "  4. Manufacturing teams work in parallel:"
    print "     - Russian team: Vodka Bar"
    print "     - Irish team: Whiskey Bar"
    print "     - French team: Champagne Bar"
    print "     - Mexican team: Tequila Bar"
    print "     - Japanese team: Sake Bar"
    print "     - Italian team: Luxury Seats"
    print "     - German team: Toilet System"
    print "     - American team: Entertainment System"
    print "  5. Assembly installs all components"
    print "  6. Test flight with protocol sent to customer"
    print "  7. Delivery and customer acceptance"
    print "=================================================================="
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createLuxuryAirplaneProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
