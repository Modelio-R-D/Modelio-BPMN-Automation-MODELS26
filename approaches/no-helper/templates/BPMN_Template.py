#
# BPMN_Template.py
#
# Description:
#   Template for creating BPMN process diagrams in Modelio.
#   Includes helper functions for all common BPMN elements.
#
# Key Insight (from Modelio developers, Dec 2025):
#   - Modelio automatically unmasks elements when a diagram is created
#   - No need to call unmask() manually for initial display
#   - BUT: There may be a delay before elements are available
#   - IF elements still missing: manual unmask INSIDE the correct lane
#
# Applicable on: Package
#
# Version: 4.0 - December 2025
#   - Added guard parameter for sequence flows from gateways
#   - Guards display condition labels (Yes/No, Approved/Rejected, etc.)
#
# Usage:
#   1. Copy this template
#   2. Modify createMyBPMN() function with your process
#   3. Define lanes, elements, flows, and layout
#   4. Run on a Package
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

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50         # Time to wait between attempts (milliseconds)
MAX_ATTEMPTS = 3           # Maximum number of attempts

# Layout configuration
SPACING = 120               # Horizontal spacing between columns
START_X = 80                # Starting X position


# ============================================================================
# HELPER FUNCTIONS - LANES
# ============================================================================

def createLane(laneSet, name):
    """Create a BPMN Lane (swim lane)"""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def addToLane(element, lane):
    """Assign an element to a lane (REQUIRED for proper positioning)"""
    try:
        lane.getFlowElementRef().add(element)
    except:
        pass


# ============================================================================
# HELPER FUNCTIONS - START EVENTS
# ============================================================================

def createStartEvent(process, name):
    """Create a BPMN Start Event (green circle)"""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createMessageStartEvent(process, name):
    """Create a BPMN Message Start Event (envelope icon - triggered by message)"""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


def createTimerStartEvent(process, name):
    """Create a BPMN Timer Start Event (clock icon - triggered by schedule)"""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        pass
    return event


# ============================================================================
# HELPER FUNCTIONS - END EVENTS
# ============================================================================

def createEndEvent(process, name):
    """Create a BPMN End Event (red circle)"""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createMessageEndEvent(process, name):
    """Create a BPMN Message End Event (envelope icon - sends message)"""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


# ============================================================================
# HELPER FUNCTIONS - TASKS
# ============================================================================

def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)"""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon - physical task without IT)"""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon - automated task)"""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


# ============================================================================
# HELPER FUNCTIONS - GATEWAYS
# ============================================================================

def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (X diamond - XOR, one path only)"""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (+ diamond - AND, all paths)"""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


# ============================================================================
# HELPER FUNCTIONS - FLOWS
# ============================================================================

def createSequenceFlow(process, source, target, name="", guard=""):
    """
    Create a BPMN Sequence Flow (arrow between elements).
    
    Parameters:
    - process: The BPMN process container
    - source: Source element (task, gateway, event)
    - target: Target element (task, gateway, event)
    - name: Optional name for the flow (rarely used)
    - guard: Condition expression displayed on flows from gateways
             (e.g., "Yes", "No", "Approved", "Rejected")
    
    Note: For flows from Exclusive Gateways, use the 'guard' parameter
    to set the condition label. This displays the text on the arrow.
    """
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    
    # Set guard condition for gateway outflows
    if guard:
        flow.setConditionExpression(guard)
    
    return flow


def createSequenceFlowWithGuard(process, source, target, guard):
    """
    Convenience function for creating flows from gateways with conditions.
    
    Parameters:
    - process: The BPMN process container
    - source: Source gateway
    - target: Target element
    - guard: Condition expression (e.g., "Yes", "No", "Approved")
    
    Example:
        createSequenceFlowWithGuard(process, approvalGateway, rejectTask, "No")
    """
    return createSequenceFlow(process, source, target, name="", guard=guard)


# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def parseBounds(boundsStr):
    """
    Parse a Rectangle bounds string into a dictionary.
    Example: "Rectangle(100.0, 50.0, 80.0, 45.0)" -> {"x": 100, "y": 50, "w": 80, "h": 45}
    """
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
    """Get the diagram graphics for an element. Returns first graphic or None."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def getBounds(diagramHandle, element):
    """Get the bounds of an element in the diagram. Returns dict or None."""
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


def formatLanesSummary(diagramHandle, lanes):
    """Format a compact summary of all lanes with their Y ranges."""
    parts = []
    for laneName, lane in lanes.items():
        info = getBounds(diagramHandle, lane)
        if info:
            yEnd = int(info["y"] + info["h"])
            parts.append(laneName + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
        else:
            parts.append(laneName + "(--)")
    return "Lanes: " + "; ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
    """
    Wait until all elements are available in the diagram.
    
    Modelio automatically unmasks elements when a diagram is created,
    but there may be a delay. This function polls until all elements
    have valid graphics objects.
    
    Returns:
        dict: {elementName: graphicsObject} for all found elements
        int: number of attempts needed
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
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """
    Manually unmask elements that were not auto-unmasked.
    
    CRITICAL: Elements must be unmasked at a Y position INSIDE their lane!
    Unmasking at (0, 0) will fail.
    
    Args:
        diagramHandle: The diagram handle
        elements: List of all elements
        elementGraphics: Dict of already found {name: graphics}
        lanes: Dict of {laneName: lane object}
        elementLayout: Dict of {elementName: (column, laneName)}
    
    Returns:
        int: Number of newly unmasked elements
    """
    unmaskedCount = 0
    
    # First, get each lane's center Y position
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
    
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            # Get the lane for this element
            laneName = elementLayout.get(name, (0, ""))[1]
            targetY = laneY.get(laneName, 100)
            
            # Unmask at position INSIDE the lane
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
# DIAGRAM CREATION FUNCTION
# ============================================================================

def createBPMNDiagram(diagramName, process, elements, flows, lanes, elementLayout, spacing=120, startX=100):
    """
    Create a BPMN diagram with automatic layout.
    
    Workflow:
    1. Create diagram (triggers auto-unmask)
    2. Wait for elements to be available
    3. If some missing, manually unmask inside correct lane
    4. Reposition all elements
    5. Save
    
    Parameters:
    - diagramName: Name for the diagram
    - process: The BpmnProcess object
    - elements: List of all BPMN elements to display
    - flows: List of all sequence flows
    - lanes: Dictionary of lane name -> lane object
    - elementLayout: Dictionary of element name -> (column_index, lane_name)
    - spacing: Horizontal spacing between columns (default 120)
    - startX: Starting X position (default 100)
    
    Returns: The created diagram, or None on error
    """
    try:
        # Create diagram
        diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
        diagram.setName(diagramName)
        diagram.setOrigin(process)
        
        diagramService = Modelio.getInstance().getDiagramService()
        diagramHandle = diagramService.getDiagramHandle(diagram)
        
        # Initial save (triggers auto-unmask)
        diagramHandle.save()
        print "Diagram created: " + diagramName
        print "  " + formatLanesSummary(diagramHandle, lanes)
        
        # =================================================================
        # PHASE 1: Wait for auto-unmask
        # =================================================================
        print ""
        print "Waiting for elements..."
        
        elementGraphics, attempts = waitForElements(diagramHandle, elements)
        foundCount = len(elementGraphics)
        
        # =================================================================
        # PHASE 2: Manual unmask fallback
        # =================================================================
        if foundCount < len(elements):
            print ""
            print "Manual unmask for missing elements..."
            unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
            
            if unmaskedCount > 0:
                diagramHandle.save()
                print "  Unmasked: " + str(unmaskedCount) + " elements"
        
        foundCount = len(elementGraphics)
        print ""
        print "Elements ready: " + str(foundCount) + "/" + str(len(elements))
        
        # =================================================================
        # PHASE 3: Get lane Y positions
        # =================================================================
        laneY = {}
        for laneName, lane in lanes.items():
            y = getLaneCenterY(diagramHandle, lane)
            if y:
                laneY[laneName] = y
        
        # =================================================================
        # PHASE 4: Reposition elements
        # =================================================================
        print ""
        print "Repositioning elements..."
        
        # Sort by column
        sortedLayout = sorted(elementLayout.items(), key=lambda x: x[1][0])
        repositionedCount = 0
        
        for elementName, (colIndex, laneName) in sortedLayout:
            if elementName in elementGraphics:
                dg = elementGraphics[elementName]
                
                # Find the element object
                elem = None
                for e in elements:
                    if e.getName() == elementName:
                        elem = e
                        break
                
                if elem:
                    bounds = getBounds(diagramHandle, elem)
                    if bounds:
                        newX = startX + spacing * colIndex
                        newY = laneY.get(laneName, 100)
                        
                        newBounds = Draw2DRectangle(int(newX), int(newY), int(bounds["w"]), int(bounds["h"]))
                        dg.setBounds(newBounds)
                        diagramHandle.save()
                        repositionedCount += 1
        
        print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
        
        # =================================================================
        # PHASE 5: Final save and close
        # =================================================================
        diagramHandle.save()
        diagramHandle.close()
        
        print ""
        print "Diagram '" + diagramName + "' created!"
        print "  " + formatLanesSummary(diagramHandle, lanes)
        
        return diagram
        
    except Exception as e:
        print "ERROR: " + str(e)
        import traceback
        traceback.print_exc()
        return None


# ============================================================================
# YOUR BPMN PROCESS - MODIFY THIS FUNCTION
# ============================================================================

def createMyBPMN(parentPackage):
    """
    Create your BPMN process here.
    
    Steps:
    1. Create Process
    2. Create Lanes
    3. Create Elements (and assign to lanes with addToLane)
    4. Create Flows
    5. Define Layout
    6. Call createBPMNDiagram()
    """
    
    print "=" * 50
    print "Creating My BPMN Process"
    print "=" * 50
    
    # =========================================================================
    # 1. CREATE PROCESS
    # =========================================================================
    
    process = modelingSession.getModel().createBpmnProcess()
    process.setName("My Process")
    process.setOwner(parentPackage)
    
    # =========================================================================
    # 2. CREATE LANES
    # =========================================================================
    
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    
    lane1 = createLane(laneSet, "Lane 1")
    lane2 = createLane(laneSet, "Lane 2")
    
    # =========================================================================
    # 3. CREATE ELEMENTS
    # =========================================================================
    
    # --- Lane 1 ---
    start = createStartEvent(process, "Start")
    addToLane(start, lane1)
    
    task1 = createUserTask(process, "Review Request")
    addToLane(task1, lane1)
    
    decision = createExclusiveGateway(process, "Approved?")
    addToLane(decision, lane1)
    
    # --- Lane 2 ---
    task2 = createServiceTask(process, "Process Approval")
    addToLane(task2, lane2)
    
    taskReject = createUserTask(process, "Send Rejection")
    addToLane(taskReject, lane2)
    
    end = createEndEvent(process, "End")
    addToLane(end, lane2)
    
    # =========================================================================
    # 4. CREATE FLOWS
    # =========================================================================
    
    flows = []
    # Normal flows (no guard needed)
    flows.append(createSequenceFlow(process, start, task1))
    flows.append(createSequenceFlow(process, task1, decision))
    
    # Flows FROM GATEWAY - use guard parameter for condition labels
    flows.append(createSequenceFlow(process, decision, task2, guard="Yes"))
    flows.append(createSequenceFlow(process, decision, taskReject, guard="No"))
    
    # Alternative: use convenience function
    # flows.append(createSequenceFlowWithGuard(process, decision, task2, "Yes"))
    # flows.append(createSequenceFlowWithGuard(process, decision, taskReject, "No"))
    
    flows.append(createSequenceFlow(process, task2, end))
    flows.append(createSequenceFlow(process, taskReject, end))
    
    # =========================================================================
    # 5. DEFINE LAYOUT
    # =========================================================================
    
    # Format: "Element Name": (column_index, "Lane Name")
    elementLayout = {
        "Start": (0, "Lane 1"),
        "Review Request": (1, "Lane 1"),
        "Approved?": (2, "Lane 1"),
        "Process Approval": (3, "Lane 2"),
        "Send Rejection": (3, "Lane 2"),  # Same column, different lane
        "End": (4, "Lane 2"),
    }
    
    # =========================================================================
    # 6. CREATE DIAGRAM
    # =========================================================================
    
    allElements = [start, task1, decision, task2, taskReject, end]
    
    lanesDict = {
        "Lane 1": lane1,
        "Lane 2": lane2,
    }
    
    createBPMNDiagram(
        diagramName="My Process Diagram",
        process=process,
        elements=allElements,
        flows=flows,
        lanes=lanesDict,
        elementLayout=elementLayout,
        spacing=120,
        startX=100
    )
    
    print ""
    print "Process created successfully!"
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createMyBPMN(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
