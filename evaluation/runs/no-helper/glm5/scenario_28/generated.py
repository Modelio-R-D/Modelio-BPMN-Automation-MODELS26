# InternshipProcess.py
#
# Description:
#   BPMN process diagram for Internship Search and Management workflow.
#   3 lanes: Student, Company, System
#
# Workflow:
#   1. Student enters preferences (topic, salary, experience, hobbies)
#   2. Company reviews applications and sends offers
#   3. Student reviews and decides (accept/deny with loop)
#   4. Both write 3 status updates during internship
#   5. Student recommends company via parallel tweets to friends
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
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.events import BpmnMessageEndEvent
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
SPACING = 140
START_X = 80

# Task dimensions
TASK_WIDTH = 120
TASK_HEIGHT = 60


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


def createMessageEndEvent(process, name):
    """Create a BPMN Message End Event (envelope icon)."""
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
    """
    Create a BPMN Sequence Flow (arrow between elements).
    
    Parameters:
    - process: The BPMN process container
    - source: Source element
    - target: Target element
    - name: Optional name for the flow
    - guard: Condition expression for flows from gateways
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
    """Get the bounds (x, y, width, height) of an element."""
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
            laneName = elementLayout.get(name, (0, "Student"))[1]
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

def createInternshipProcess(parentPackage):
    """
    Create the Internship BPMN process with diagram.
    """
    
    processName = "Internship_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN INTERNSHIP PROCESS"
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
    
    studentLane = createLane(laneSet, "Student")
    companyLane = createLane(laneSet, "Company")
    systemLane = createLane(laneSet, "System")
    
    lanes = {
        "Student": studentLane,
        "Company": companyLane,
        "System": systemLane
    }
    laneOrder = ["Student", "Company", "System"]
    
    print "[" + str(step()) + "] Lanes: Student, Company, System"
    
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
    
    # --- Student Lane (13 elements) ---
    addElement(createStartEvent, "Start Search", studentLane, "Student")
    addElement(createUserTask, "Enter Preferences", studentLane, "Student")
    addElement(createUserTask, "Review Offer", studentLane, "Student")
    addElement(createExclusiveGateway, "Accept?", studentLane, "Student")
    addElement(createUserTask, "Accept Offer", studentLane, "Student")
    addElement(createUserTask, "Deny Offer", studentLane, "Student")
    addElement(createUserTask, "Write Update 1", studentLane, "Student")
    addElement(createUserTask, "Write Update 2", studentLane, "Student")
    addElement(createUserTask, "Write Update 3", studentLane, "Student")
    addElement(createUserTask, "Recommend Company", studentLane, "Student")
    addElement(createParallelGateway, "Tweet Split", studentLane, "Student")
    addElement(createParallelGateway, "Tweet Join", studentLane, "Student")
    addElement(createEndEvent, "Internship Done", studentLane, "Student")
    print "[" + str(step()) + "] Student lane: 13 elements"
    
    # --- Company Lane (8 elements) ---
    addElement(createUserTask, "Review Applications", companyLane, "Company")
    addElement(createUserTask, "Send Offer", companyLane, "Company")
    addElement(createServiceTask, "Cancel Other Offers", companyLane, "Company")
    addElement(createUserTask, "Write Intern Update 1", companyLane, "Company")
    addElement(createUserTask, "Write Intern Update 2", companyLane, "Company")
    addElement(createUserTask, "Write Intern Update 3", companyLane, "Company")
    addElement(createEndEvent, "Company Done", companyLane, "Company")
    print "[" + str(step()) + "] Company lane: 7 elements"
    
    # --- System Lane (5 elements) ---
    addElement(createServiceTask, "Notify Student", systemLane, "System")
    addElement(createServiceTask, "Tweet Friend 1", systemLane, "System")
    addElement(createServiceTask, "Tweet Friend 2", systemLane, "System")
    addElement(createServiceTask, "Tweet Friend 3", systemLane, "System")
    addElement(createMessageEndEvent, "Tweets Sent", systemLane, "System")
    print "[" + str(step()) + "] System lane: 5 elements"
    
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
    
    # Layout: element name -> (column_index, lane_name)
    elementLayout = {
        # Student Lane
        "Start Search": (0, "Student"),
        "Enter Preferences": (1, "Student"),
        "Review Offer": (3, "Student"),
        "Accept?": (4, "Student"),
        "Accept Offer": (5, "Student"),
        "Deny Offer": (5, "Student"),
        "Write Update 1": (7, "Student"),
        "Write Update 2": (8, "Student"),
        "Write Update 3": (9, "Student"),
        "Recommend Company": (10, "Student"),
        "Tweet Split": (11, "Student"),
        "Tweet Join": (13, "Student"),
        "Internship Done": (14, "Student"),
        # Company Lane
        "Review Applications": (1, "Company"),
        "Send Offer": (2, "Company"),
        "Cancel Other Offers": (6, "Company"),
        "Write Intern Update 1": (7, "Company"),
        "Write Intern Update 2": (8, "Company"),
        "Write Intern Update 3": (9, "Company"),
        "Company Done": (10, "Company"),
        # System Lane
        "Notify Student": (3, "System"),
        "Tweet Friend 1": (12, "System"),
        "Tweet Friend 2": (12, "System"),
        "Tweet Friend 3": (12, "System"),
        "Tweets Sent": (13, "System"),
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    
    if foundCount < len(elements):
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(len(elements)) + " elements ready"
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
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
    
    print ""
    
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    # Track Y offset for parallel elements in same column (tweets)
    columnYOffset = {}
    
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
        
        targetX = START_X + SPACING * col
        baseY = laneY.get(laneName, 100)
        
        # Handle parallel tweets - offset Y for visibility
        if "Tweet Friend" in name:
            colKey = (col, laneName)
            if colKey not in columnYOffset:
                columnYOffset[colKey] = 0
            yOffset = columnYOffset[colKey] * 70
            targetY = baseY + yOffset
            columnYOffset[colKey] += 1
        else:
            targetY = baseY
        
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
        # Student main flow
        ("Start Search", "Enter Preferences", ""),
        ("Enter Preferences", "Review Applications", ""),  # Cross-lane to Company
        ("Review Offer", "Accept?", ""),
        ("Accept?", "Accept Offer", "Yes"),
        ("Accept?", "Deny Offer", "No"),
        ("Deny Offer", "Review Offer", ""),  # Loop back
        ("Accept Offer", "Cancel Other Offers", ""),  # Cross-lane to Company
        ("Accept Offer", "Write Update 1", ""),
        ("Write Update 1", "Write Update 2", ""),
        ("Write Update 2", "Write Update 3", ""),
        ("Write Update 3", "Recommend Company", ""),
        ("Recommend Company", "Tweet Split", ""),
        ("Tweet Split", "Tweet Friend 1", ""),
        ("Tweet Split", "Tweet Friend 2", ""),
        ("Tweet Split", "Tweet Friend 3", ""),
        ("Tweet Friend 1", "Tweet Join", ""),
        ("Tweet Friend 2", "Tweet Join", ""),
        ("Tweet Friend 3", "Tweet Join", ""),
        ("Tweet Join", "Internship Done", ""),
        ("Tweet Join", "Tweets Sent", ""),  # Cross-lane to System
        
        # Company flow
        ("Review Applications", "Send Offer", ""),
        ("Send Offer", "Notify Student", ""),  # Cross-lane to System
        ("Cancel Other Offers", "Write Intern Update 1", ""),
        ("Write Intern Update 1", "Write Intern Update 2", ""),
        ("Write Intern Update 2", "Write Intern Update 3", ""),
        ("Write Intern Update 3", "Company Done", ""),
        
        # System flow
        ("Notify Student", "Review Offer", ""),  # Cross-lane to Student
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
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createInternshipProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
