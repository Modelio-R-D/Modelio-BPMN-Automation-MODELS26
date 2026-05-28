#
# UniversityEnrollmentProcess.py
#
# Description:
#   BPMN process diagram for University Enrollment workflow.
#   Covers application, admission, enrollment, and semester cycle.
#
# Lanes:
#   - Prospective Student / Student
#   - Admissions Office
#   - Admissions Committee
#   - Finance Department
#   - IT Department
#   - International Office
#   - Academic Advisor
#   - Appeals Committee
#
# Applicable on: Package
# Version: 1.0 - University Enrollment Process
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
    """Create a BPMN Start Event."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createEndEvent(process, name):
    """Create a BPMN End Event."""
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
    """Create a BPMN User Task."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway."""
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
            parts.append(laneName[:8] + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
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
    
    for col, name, elem in sortedElems[:10]:  # First 10 only
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
            missingStr = ", ".join(missing[:5])
            if len(missing) > 5:
                missingStr += "..."
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + missingStr
        
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
            laneName = elementLayout.get(name, (0, "Student"))[1]
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

def createUniversityEnrollmentProcess(parentPackage):
    """Create the University Enrollment BPMN process with diagram."""
    
    processName = "UniversityEnrollment_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN UNIVERSITY ENROLLMENT PROCESS"
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
    studentLane = createLane(laneSet, "Student")
    admissionsLane = createLane(laneSet, "Admissions")
    committeeLane = createLane(laneSet, "Committee")
    financeLane = createLane(laneSet, "Finance")
    itLane = createLane(laneSet, "IT Dept")
    intlLane = createLane(laneSet, "Intl Office")
    advisorLane = createLane(laneSet, "Advisor")
    appealsLane = createLane(laneSet, "Appeals")
    
    lanes = {
        "Student": studentLane,
        "Admissions": admissionsLane,
        "Committee": committeeLane,
        "Finance": financeLane,
        "IT Dept": itLane,
        "Intl Office": intlLane,
        "Advisor": advisorLane,
        "Appeals": appealsLane
    }
    laneOrder = ["Student", "Admissions", "Committee", "Finance", "IT Dept", "Intl Office", "Advisor", "Appeals"]
    
    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)
    
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
    
    # --- Student Lane Elements ---
    addElement(createStartEvent, "Start Application", studentLane)
    addElement(createUserTask, "Submit Application", studentLane)
    addElement(createUserTask, "Provide Missing Docs", studentLane)
    addElement(createUserTask, "Confirm Enrollment", studentLane)
    addElement(createExclusiveGateway, "Confirmed?", studentLane)
    addElement(createUserTask, "Receive Orientation", studentLane)
    addElement(createExclusiveGateway, "International?", studentLane)
    addElement(createManualTask, "Get Student ID", studentLane)
    addElement(createUserTask, "Meet Advisor", studentLane)
    addElement(createUserTask, "Select Courses", studentLane)
    addElement(createExclusiveGateway, "Conflicts?", studentLane)
    addElement(createUserTask, "Resolve Conflicts", studentLane)
    addElement(createUserTask, "Attend Classes", studentLane)
    addElement(createExclusiveGateway, "Add/Drop?", studentLane)
    addElement(createUserTask, "Modify Courses", studentLane)
    addElement(createUserTask, "Review Grades", studentLane)
    addElement(createExclusiveGateway, "Grievance?", studentLane)
    addElement(createUserTask, "Submit Appeal", studentLane)
    addElement(createExclusiveGateway, "Continue?", studentLane)
    addElement(createEndEvent, "Graduated", studentLane)
    addElement(createEndEvent, "Withdrawn", studentLane)
    addElement(createEndEvent, "App Canceled", studentLane)
    print "[" + str(step()) + "] Student lane: 22 elements"
    
    # --- Admissions Lane Elements ---
    addElement(createUserTask, "Review Application", admissionsLane)
    addElement(createExclusiveGateway, "Docs Complete?", admissionsLane)
    addElement(createServiceTask, "Notify Missing Docs", admissionsLane)
    addElement(createServiceTask, "Send Acceptance", admissionsLane)
    addElement(createServiceTask, "Send Rejection", admissionsLane)
    addElement(createEndEvent, "Rejected End", admissionsLane)
    print "[" + str(step()) + "] Admissions lane: 6 elements"
    
    # --- Committee Lane Elements ---
    addElement(createUserTask, "Evaluate Application", committeeLane)
    addElement(createExclusiveGateway, "Accepted?", committeeLane)
    print "[" + str(step()) + "] Committee lane: 2 elements"
    
    # --- Finance Lane Elements ---
    addElement(createParallelGateway, "Split Eval", financeLane)
    addElement(createServiceTask, "Process Fees", financeLane)
    addElement(createParallelGateway, "Join Eval", financeLane)
    print "[" + str(step()) + "] Finance lane: 3 elements"
    
    # --- IT Department Lane Elements ---
    addElement(createServiceTask, "Setup Accounts", itLane)
    print "[" + str(step()) + "] IT Dept lane: 1 element"
    
    # --- International Office Lane Elements ---
    addElement(createUserTask, "Assist Visa", intlLane)
    addElement(createParallelGateway, "Join Setup", intlLane)
    print "[" + str(step()) + "] Intl Office lane: 2 elements"
    
    # --- Advisor Lane Elements ---
    addElement(createUserTask, "Advising Session", advisorLane)
    print "[" + str(step()) + "] Advisor lane: 1 element"
    
    # --- Appeals Lane Elements ---
    addElement(createUserTask, "Meet Appeals Comm", appealsLane)
    addElement(createUserTask, "Await Decision", appealsLane)
    print "[" + str(step()) + "] Appeals lane: 2 elements"
    
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
    
    # Layout: element name -> (column, lane_name)
    elementLayout = {
        # Application Phase (columns 0-5)
        "Start Application": (0, "Student"),
        "Submit Application": (1, "Student"),
        "Review Application": (2, "Admissions"),
        "Docs Complete?": (3, "Admissions"),
        "Notify Missing Docs": (4, "Admissions"),
        "Provide Missing Docs": (4, "Student"),
        
        # Evaluation Phase (columns 5-9)
        "Split Eval": (5, "Finance"),
        "Evaluate Application": (6, "Committee"),
        "Process Fees": (6, "Finance"),
        "Join Eval": (7, "Finance"),
        "Accepted?": (8, "Committee"),
        
        # Decision Phase (columns 9-11)
        "Send Acceptance": (9, "Admissions"),
        "Send Rejection": (9, "Admissions"),
        "Rejected End": (10, "Admissions"),
        "Confirm Enrollment": (10, "Student"),
        "Confirmed?": (11, "Student"),
        "App Canceled": (12, "Student"),
        
        # Setup Phase (columns 12-15)
        "Receive Orientation": (13, "Student"),
        "Setup Accounts": (13, "IT Dept"),
        "International?": (14, "Student"),
        "Assist Visa": (14, "Intl Office"),
        "Join Setup": (15, "Intl Office"),
        "Get Student ID": (16, "Student"),
        
        # Course Planning Phase (columns 16-20)
        "Meet Advisor": (17, "Student"),
        "Advising Session": (17, "Advisor"),
        "Select Courses": (18, "Student"),
        "Conflicts?": (19, "Student"),
        "Resolve Conflicts": (20, "Student"),
        
        # Semester Phase (columns 20-26)
        "Attend Classes": (21, "Student"),
        "Add/Drop?": (22, "Student"),
        "Modify Courses": (23, "Student"),
        "Review Grades": (24, "Student"),
        "Grievance?": (25, "Student"),
        "Submit Appeal": (26, "Student"),
        "Meet Appeals Comm": (26, "Appeals"),
        "Await Decision": (27, "Appeals"),
        
        # End Phase (columns 27-29)
        "Continue?": (28, "Student"),
        "Graduated": (29, "Student"),
        "Withdrawn": (30, "Student"),
    }
    
    print "[" + str(step()) + "] Waiting for elements..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    foundCount = len(elementGraphics)
    
    if foundCount == len(elements):
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready"
    else:
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
        # Application submission
        ("Start Application", "Submit Application", ""),
        ("Submit Application", "Review Application", ""),
        
        # Document check
        ("Review Application", "Docs Complete?", ""),
        ("Docs Complete?", "Notify Missing Docs", "No"),
        ("Notify Missing Docs", "Provide Missing Docs", ""),
        ("Provide Missing Docs", "Review Application", ""),
        ("Docs Complete?", "Split Eval", "Yes"),
        
        # Parallel evaluation
        ("Split Eval", "Evaluate Application", ""),
        ("Split Eval", "Process Fees", ""),
        ("Evaluate Application", "Join Eval", ""),
        ("Process Fees", "Join Eval", ""),
        ("Join Eval", "Accepted?", ""),
        
        # Acceptance decision
        ("Accepted?", "Send Acceptance", "Accepted"),
        ("Accepted?", "Send Rejection", "Rejected"),
        ("Send Rejection", "Rejected End", ""),
        ("Send Acceptance", "Confirm Enrollment", ""),
        
        # Enrollment confirmation
        ("Confirm Enrollment", "Confirmed?", ""),
        ("Confirmed?", "App Canceled", "No"),
        ("Confirmed?", "Receive Orientation", "Yes"),
        
        # Setup phase
        ("Receive Orientation", "Setup Accounts", ""),
        ("Setup Accounts", "International?", ""),
        ("International?", "Assist Visa", "Yes"),
        ("International?", "Join Setup", "No"),
        ("Assist Visa", "Join Setup", ""),
        ("Join Setup", "Get Student ID", ""),
        
        # Course planning
        ("Get Student ID", "Meet Advisor", ""),
        ("Meet Advisor", "Advising Session", ""),
        ("Advising Session", "Select Courses", ""),
        ("Select Courses", "Conflicts?", ""),
        ("Conflicts?", "Resolve Conflicts", "Yes"),
        ("Resolve Conflicts", "Select Courses", ""),
        ("Conflicts?", "Attend Classes", "No"),
        
        # Semester cycle
        ("Attend Classes", "Add/Drop?", ""),
        ("Add/Drop?", "Modify Courses", "Yes"),
        ("Modify Courses", "Attend Classes", ""),
        ("Add/Drop?", "Review Grades", "No"),
        
        # Grievance handling
        ("Review Grades", "Grievance?", ""),
        ("Grievance?", "Submit Appeal", "Yes"),
        ("Submit Appeal", "Meet Appeals Comm", ""),
        ("Meet Appeals Comm", "Await Decision", ""),
        ("Await Decision", "Continue?", ""),
        ("Grievance?", "Continue?", "No"),
        
        # Continuation decision
        ("Continue?", "Meet Advisor", "Next Semester"),
        ("Continue?", "Graduated", "Graduate"),
        ("Continue?", "Withdrawn", "Withdraw"),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            missingElem = srcName if not src else tgtName
            print "  WARNING: Missing " + missingElem
    
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
        createUniversityEnrollmentProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
