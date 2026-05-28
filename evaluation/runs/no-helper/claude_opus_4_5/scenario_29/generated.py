#
# WorkAndLiveInAustria.py
#
# Description:
#   BPMN process diagram for Work and Live in Austria workflow.
#   Covers visa application (Rot-Weiss-Rot Card), accommodation, and bank account setup.
#   4 lanes: Applicant, Austrian Representation, Accommodation/Bank, Employer
#
# Key Insight (from Modelio developers):
#   - Modelio automatically unmasks elements when a diagram is created
#   - No need to call unmask() manually
#   - BUT: There may be a delay before elements are available
#   - Solution: Wait and check until all elements are ready
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


def createTimerEvent(process, name):
    """Create a BPMN Timer Intermediate Catch Event (clock icon)."""
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
    """Create a BPMN Sequence Flow (arrow between elements)."""
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
    
    for col, name, elem in sortedElems[:8]:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:8]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:8] + "=--")
    if len(sortedElems) > 8:
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
            missing = [e.getName()[:10] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing[:5])
        
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
            laneName = elementLayout.get(name, (0, "Applicant"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + ": OK"
                else:
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + ": FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:15] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createWorkAndLiveInAustriaProcess(parentPackage):
    """
    Create the Work and Live in Austria BPMN process with diagram.
    
    Process covers:
    - Initial research and employer contact
    - Visa application (Rot-Weiss-Rot Card)
    - Accommodation and bank account setup
    - Visa renewal cycle
    """
    
    processName = "WorkLiveAustria_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN WORK AND LIVE IN AUSTRIA PROCESS"
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
    
    applicantLane = createLane(laneSet, "Applicant")
    representationLane = createLane(laneSet, "Austrian Repr.")
    accommodationLane = createLane(laneSet, "Accom./Bank")
    employerLane = createLane(laneSet, "Employer")
    
    lanes = {
        "Applicant": applicantLane,
        "Austrian Repr.": representationLane,
        "Accom./Bank": accommodationLane,
        "Employer": employerLane
    }
    laneOrder = ["Applicant", "Austrian Repr.", "Accom./Bank", "Employer"]
    
    print "[" + str(step()) + "] Lanes: Applicant, Austrian Repr., Accom./Bank, Employer"
    
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
    
    # --- Applicant Lane (Initial Phase) ---
    addElement(createStartEvent, "Decision to Move", applicantLane)
    addElement(createUserTask, "Research Requirements", applicantLane)
    addElement(createUserTask, "Identify Employer", applicantLane)
    addElement(createParallelGateway, "Start Parallel", applicantLane)
    
    # --- Applicant Lane (Visa Documents) ---
    addElement(createUserTask, "Fill Visa Form", applicantLane)
    addElement(createManualTask, "Get Passport Photo", applicantLane)
    addElement(createUserTask, "Get Travel Insurance", applicantLane)
    addElement(createUserTask, "Proof of Funds", applicantLane)
    addElement(createParallelGateway, "Join Docs", applicantLane)
    addElement(createManualTask, "Submit Application", applicantLane)
    
    # --- Applicant Lane (Post-Decision) ---
    addElement(createUserTask, "Travel to Austria", applicantLane)
    addElement(createUserTask, "Register Residence", applicantLane)
    addElement(createTimerEvent, "Renewal Timer", applicantLane)
    addElement(createUserTask, "Prepare Renewal", applicantLane)
    addElement(createEndEvent, "Living in Austria", applicantLane)
    print "[" + str(step()) + "] Applicant lane: 15 elements"
    
    # --- Austrian Representation Lane ---
    addElement(createServiceTask, "Receive Application", representationLane)
    addElement(createUserTask, "Verify Documents", representationLane)
    addElement(createExclusiveGateway, "Documents OK?", representationLane)
    addElement(createUserTask, "Request More Docs", representationLane)
    addElement(createServiceTask, "Process RWR Card", representationLane)
    addElement(createExclusiveGateway, "Visa Approved?", representationLane)
    addElement(createServiceTask, "Issue RWR Card", representationLane)
    addElement(createEndEvent, "Visa Rejected", representationLane)
    addElement(createServiceTask, "Process Renewal", representationLane)
    print "[" + str(step()) + "] Austrian Repr. lane: 9 elements"
    
    # --- Accommodation/Bank Lane ---
    addElement(createUserTask, "Search Accommodation", accommodationLane)
    addElement(createUserTask, "Negotiate Lease", accommodationLane)
    addElement(createManualTask, "Sign Lease Contract", accommodationLane)
    addElement(createUserTask, "Open Bank Account", accommodationLane)
    addElement(createServiceTask, "Bank Verification", accommodationLane)
    addElement(createParallelGateway, "Join Accom/Bank", accommodationLane)
    print "[" + str(step()) + "] Accom./Bank lane: 6 elements"
    
    # --- Employer Lane ---
    addElement(createUserTask, "Review Application", employerLane)
    addElement(createExclusiveGateway, "Hire Decision", employerLane)
    addElement(createUserTask, "Issue Job Offer", employerLane)
    addElement(createServiceTask, "Provide AMS Docs", employerLane)
    addElement(createEndEvent, "Not Hired", employerLane)
    print "[" + str(step()) + "] Employer lane: 5 elements"
    
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
        # Applicant Lane - Initial
        "Decision to Move": (0, "Applicant"),
        "Research Requirements": (1, "Applicant"),
        "Identify Employer": (2, "Applicant"),
        "Start Parallel": (4, "Applicant"),
        # Applicant Lane - Visa Docs
        "Fill Visa Form": (5, "Applicant"),
        "Get Passport Photo": (6, "Applicant"),
        "Get Travel Insurance": (7, "Applicant"),
        "Proof of Funds": (8, "Applicant"),
        "Join Docs": (9, "Applicant"),
        "Submit Application": (10, "Applicant"),
        # Applicant Lane - Post-Decision
        "Travel to Austria": (15, "Applicant"),
        "Register Residence": (16, "Applicant"),
        "Renewal Timer": (17, "Applicant"),
        "Prepare Renewal": (18, "Applicant"),
        "Living in Austria": (20, "Applicant"),
        
        # Austrian Representation Lane
        "Receive Application": (11, "Austrian Repr."),
        "Verify Documents": (12, "Austrian Repr."),
        "Documents OK?": (13, "Austrian Repr."),
        "Request More Docs": (13, "Austrian Repr."),  # Same column, different row handled by offset
        "Process RWR Card": (14, "Austrian Repr."),
        "Visa Approved?": (15, "Austrian Repr."),
        "Issue RWR Card": (16, "Austrian Repr."),
        "Visa Rejected": (17, "Austrian Repr."),
        "Process Renewal": (19, "Austrian Repr."),
        
        # Accommodation/Bank Lane
        "Search Accommodation": (5, "Accom./Bank"),
        "Negotiate Lease": (6, "Accom./Bank"),
        "Sign Lease Contract": (7, "Accom./Bank"),
        "Open Bank Account": (8, "Accom./Bank"),
        "Bank Verification": (9, "Accom./Bank"),
        "Join Accom/Bank": (14, "Accom./Bank"),
        
        # Employer Lane
        "Review Application": (3, "Employer"),
        "Hire Decision": (4, "Employer"),
        "Issue Job Offer": (5, "Employer"),
        "Provide AMS Docs": (6, "Employer"),
        "Not Hired": (5, "Employer"),  # Same column as Issue Job Offer
    }
    
    # Adjust for elements that share columns (vertical offset)
    elementOffset = {
        "Request More Docs": -40,
        "Not Hired": 40,
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
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
        
        # Apply vertical offset if specified
        if name in elementOffset:
            targetY += elementOffset[name]
        
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
        # Initial flow
        ("Decision to Move", "Research Requirements", ""),
        ("Research Requirements", "Identify Employer", ""),
        ("Identify Employer", "Review Application", ""),
        
        # Employer decision
        ("Review Application", "Hire Decision", ""),
        ("Hire Decision", "Issue Job Offer", "Yes"),
        ("Hire Decision", "Not Hired", "No"),
        ("Issue Job Offer", "Provide AMS Docs", ""),
        ("Provide AMS Docs", "Start Parallel", ""),
        
        # Parallel split for visa docs and accommodation
        ("Start Parallel", "Fill Visa Form", ""),
        ("Start Parallel", "Search Accommodation", ""),
        
        # Visa documents preparation
        ("Fill Visa Form", "Get Passport Photo", ""),
        ("Get Passport Photo", "Get Travel Insurance", ""),
        ("Get Travel Insurance", "Proof of Funds", ""),
        ("Proof of Funds", "Join Docs", ""),
        
        # Accommodation and bank
        ("Search Accommodation", "Negotiate Lease", ""),
        ("Negotiate Lease", "Sign Lease Contract", ""),
        ("Sign Lease Contract", "Open Bank Account", ""),
        ("Open Bank Account", "Bank Verification", ""),
        ("Bank Verification", "Join Accom/Bank", ""),
        
        # Join and submit
        ("Join Docs", "Submit Application", ""),
        ("Submit Application", "Receive Application", ""),
        
        # Austrian representation processing
        ("Receive Application", "Verify Documents", ""),
        ("Verify Documents", "Documents OK?", ""),
        ("Documents OK?", "Process RWR Card", "Yes"),
        ("Documents OK?", "Request More Docs", "No"),
        ("Request More Docs", "Submit Application", ""),
        
        # Visa decision
        ("Process RWR Card", "Visa Approved?", ""),
        ("Visa Approved?", "Issue RWR Card", "Yes"),
        ("Visa Approved?", "Visa Rejected", "No"),
        
        # Post-approval
        ("Issue RWR Card", "Travel to Austria", ""),
        ("Join Accom/Bank", "Travel to Austria", ""),
        ("Travel to Austria", "Register Residence", ""),
        
        # Renewal cycle
        ("Register Residence", "Renewal Timer", ""),
        ("Renewal Timer", "Prepare Renewal", ""),
        ("Prepare Renewal", "Process Renewal", ""),
        ("Process Renewal", "Living in Austria", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "  WARNING: Missing element for " + srcName + " -> " + tgtName
    
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
        createWorkAndLiveInAustriaProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
