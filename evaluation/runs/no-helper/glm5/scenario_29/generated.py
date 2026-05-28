#
# WorkAndLiveInAustria.py
#
# Description:
#   BPMN process diagram for working and living in Austria.
#   Covers: Visa application, Rot-Weiss-Rot Card, accommodation,
#   and bank account setup based on official requirements.
#
# Lanes: Applicant, Employer, Austrian Authorities, Service Providers
#
# Applicable on: Package
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
from org.modelio.metamodel.bpmn.events import BpmnTimerStartEvent
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


def createTimerStartEvent(process, name):
    """Create a BPMN Timer Start Event (clock green circle)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        pass
    return event


def createEndEvent(process, name):
    """Create a BPMN End Event (red circle)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createMessageEndEvent(process, name):
    """Create a BPMN Message End Event (envelope icon - sends message)."""
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
            laneName = elementLayout.get(name, (0, "Applicant"))[1]
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

def createWorkAndLiveInAustriaProcess(parentPackage):
    """Create the Work and Live in Austria BPMN process with diagram."""
    
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
    
    # Create 4 lanes for different actors
    applicantLane = createLane(laneSet, "Applicant")
    employerLane = createLane(laneSet, "Employer")
    authoritiesLane = createLane(laneSet, "Austrian Authorities")
    servicesLane = createLane(laneSet, "Service Providers")
    
    lanes = {
        "Applicant": applicantLane,
        "Employer": employerLane,
        "Austrian Authorities": authoritiesLane,
        "Service Providers": servicesLane
    }
    laneOrder = ["Applicant", "Employer", "Austrian Authorities", "Service Providers"]
    
    print "[" + str(step()) + "] Lanes: Applicant, Employer, Austrian Authorities, Service Providers"
    
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
    
    # --- Applicant Lane (18 elements) ---
    addElement(createStartEvent, "Plan to Work in Austria", applicantLane, "Applicant")
    addElement(createParallelGateway, "Parallel Split 1", applicantLane, "Applicant")
    addElement(createManualTask, "Get Valid Passport", applicantLane, "Applicant")
    addElement(createManualTask, "Obtain Passport Photos", applicantLane, "Applicant")
    addElement(createManualTask, "Purchase Health Insurance", applicantLane, "Applicant")
    addElement(createManualTask, "Prepare Financial Proof", applicantLane, "Applicant")
    addElement(createParallelGateway, "Parallel Join 1", applicantLane, "Applicant")
    addElement(createUserTask, "Search for Job", applicantLane, "Applicant")
    addElement(createUserTask, "Apply for Positions", applicantLane, "Applicant")
    addElement(createUserTask, "Attend Interview", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Job Decision", applicantLane, "Applicant")
    addElement(createUserTask, "Sign Employment Contract", applicantLane, "Applicant")
    addElement(createParallelGateway, "Parallel Split 2", applicantLane, "Applicant")
    addElement(createUserTask, "Search Accommodation", applicantLane, "Applicant")
    addElement(createUserTask, "Open Bank Account", applicantLane, "Applicant")
    addElement(createParallelGateway, "Parallel Join 2", applicantLane, "Applicant")
    addElement(createUserTask, "Complete Visa Application", applicantLane, "Applicant")
    addElement(createManualTask, "Submit to Embassy", applicantLane, "Applicant")
    addElement(createUserTask, "Provide Additional Docs", applicantLane, "Applicant")
    addElement(createManualTask, "Travel to Austria", applicantLane, "Applicant")
    addElement(createUserTask, "Register Residence", applicantLane, "Applicant")
    addElement(createUserTask, "Renew RWR Card", applicantLane, "Applicant")
    addElement(createEndEvent, "Living and Working", applicantLane, "Applicant")
    addElement(createEndEvent, "Application Rejected", applicantLane, "Applicant")
    print "[" + str(step()) + "] Applicant lane: 24 elements"
    
    # --- Employer Lane (6 elements) ---
    addElement(createUserTask, "Review Application", employerLane, "Employer")
    addElement(createUserTask, "Conduct Interview", employerLane, "Employer")
    addElement(createExclusiveGateway, "Candidate Suitable?", employerLane, "Employer")
    addElement(createUserTask, "Issue Job Offer", employerLane, "Employer")
    addElement(createServiceTask, "Provide Work Confirmation", employerLane, "Employer")
    addElement(createEndEvent, "Hiring Complete", employerLane, "Employer")
    print "[" + str(step()) + "] Employer lane: 6 elements"
    
    # --- Austrian Authorities Lane (9 elements) ---
    addElement(createServiceTask, "Receive Application", authoritiesLane, "Austrian Authorities")
    addElement(createExclusiveGateway, "Documents Complete?", authoritiesLane, "Austrian Authorities")
    addElement(createServiceTask, "Request Additional Docs", authoritiesLane, "Austrian Authorities")
    addElement(createServiceTask, "Process Application", authoritiesLane, "Austrian Authorities")
    addElement(createExclusiveGateway, "Visa Approved?", authoritiesLane, "Austrian Authorities")
    addElement(createServiceTask, "Reject Application", authoritiesLane, "Austrian Authorities")
    addElement(createServiceTask, "Issue Visa/Permit", authoritiesLane, "Austrian Authorities")
    addElement(createServiceTask, "Issue RWR Card", authoritiesLane, "Austrian Authorities")
    addElement(createTimerStartEvent, "Renewal Reminder", authoritiesLane, "Austrian Authorities")
    print "[" + str(step()) + "] Austrian Authorities lane: 9 elements"
    
    # --- Service Providers Lane (3 elements) ---
    addElement(createUserTask, "Process Rental Agreement", servicesLane, "Service Providers")
    addElement(createServiceTask, "Setup Bank Account", servicesLane, "Service Providers")
    addElement(createServiceTask, "Confirm Services", servicesLane, "Service Providers")
    print "[" + str(step()) + "] Service Providers lane: 3 elements"
    
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
        # Applicant Lane
        "Plan to Work in Austria": (0, "Applicant"),
        "Parallel Split 1": (1, "Applicant"),
        "Get Valid Passport": (2, "Applicant"),
        "Obtain Passport Photos": (3, "Applicant"),
        "Purchase Health Insurance": (4, "Applicant"),
        "Prepare Financial Proof": (5, "Applicant"),
        "Parallel Join 1": (6, "Applicant"),
        "Search for Job": (7, "Applicant"),
        "Apply for Positions": (8, "Applicant"),
        "Attend Interview": (9, "Applicant"),
        "Job Decision": (10, "Applicant"),
        "Sign Employment Contract": (11, "Applicant"),
        "Parallel Split 2": (12, "Applicant"),
        "Search Accommodation": (13, "Applicant"),
        "Open Bank Account": (14, "Applicant"),
        "Parallel Join 2": (15, "Applicant"),
        "Complete Visa Application": (16, "Applicant"),
        "Submit to Embassy": (17, "Applicant"),
        "Provide Additional Docs": (18, "Applicant"),
        "Travel to Austria": (22, "Applicant"),
        "Register Residence": (23, "Applicant"),
        "Renew RWR Card": (25, "Applicant"),
        "Living and Working": (26, "Applicant"),
        "Application Rejected": (21, "Applicant"),
        # Employer Lane
        "Review Application": (8, "Employer"),
        "Conduct Interview": (9, "Employer"),
        "Candidate Suitable?": (10, "Employer"),
        "Issue Job Offer": (11, "Employer"),
        "Provide Work Confirmation": (16, "Employer"),
        "Hiring Complete": (26, "Employer"),
        # Austrian Authorities Lane
        "Receive Application": (17, "Austrian Authorities"),
        "Documents Complete?": (18, "Austrian Authorities"),
        "Request Additional Docs": (19, "Austrian Authorities"),
        "Process Application": (20, "Austrian Authorities"),
        "Visa Approved?": (21, "Austrian Authorities"),
        "Reject Application": (22, "Austrian Authorities"),
        "Issue Visa/Permit": (22, "Austrian Authorities"),
        "Issue RWR Card": (24, "Austrian Authorities"),
        "Renewal Reminder": (25, "Austrian Authorities"),
        # Service Providers Lane
        "Process Rental Agreement": (13, "Service Providers"),
        "Setup Bank Account": (14, "Service Providers"),
        "Confirm Services": (15, "Service Providers"),
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
        
        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""
        
        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
        
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
        # Start and document preparation (parallel split)
        ("Plan to Work in Austria", "Parallel Split 1", ""),
        ("Parallel Split 1", "Get Valid Passport", ""),
        ("Parallel Split 1", "Obtain Passport Photos", ""),
        ("Parallel Split 1", "Purchase Health Insurance", ""),
        ("Parallel Split 1", "Prepare Financial Proof", ""),
        
        # Parallel join for documents
        ("Get Valid Passport", "Parallel Join 1", ""),
        ("Obtain Passport Photos", "Parallel Join 1", ""),
        ("Purchase Health Insurance", "Parallel Join 1", ""),
        ("Prepare Financial Proof", "Parallel Join 1", ""),
        
        # Job search flow
        ("Parallel Join 1", "Search for Job", ""),
        ("Search for Job", "Apply for Positions", ""),
        ("Apply for Positions", "Review Application", ""),
        
        # Employer review process
        ("Review Application", "Conduct Interview", ""),
        ("Conduct Interview", "Attend Interview", ""),
        ("Attend Interview", "Candidate Suitable?", ""),
        
        # Employer decision gateway
        ("Candidate Suitable?", "Issue Job Offer", "Yes"),
        ("Candidate Suitable?", "Search for Job", "No"),
        
        # Job offer acceptance
        ("Issue Job Offer", "Job Decision", ""),
        ("Job Decision", "Sign Employment Contract", "Accepted"),
        ("Job Decision", "Search for Job", "Rejected"),
        
        # Employment contract and parallel setup
        ("Sign Employment Contract", "Provide Work Confirmation", ""),
        ("Provide Work Confirmation", "Parallel Split 2", ""),
        
        # Parallel split for accommodation and bank
        ("Parallel Split 2", "Search Accommodation", ""),
        ("Parallel Split 2", "Open Bank Account", ""),
        
        # Service providers tasks
        ("Search Accommodation", "Process Rental Agreement", ""),
        ("Open Bank Account", "Setup Bank Account", ""),
        ("Process Rental Agreement", "Confirm Services", ""),
        ("Setup Bank Account", "Confirm Services", ""),
        
        # Continue to visa application
        ("Confirm Services", "Parallel Join 2", ""),
        ("Parallel Join 2", "Complete Visa Application", ""),
        
        # Visa application submission
        ("Complete Visa Application", "Submit to Embassy", ""),
        ("Submit to Embassy", "Receive Application", ""),
        
        # Authorities document check
        ("Receive Application", "Documents Complete?", ""),
        ("Documents Complete?", "Request Additional Docs", "No"),
        ("Request Additional Docs", "Provide Additional Docs", ""),
        ("Provide Additional Docs", "Documents Complete?", ""),
        ("Documents Complete?", "Process Application", "Yes"),
        
        # Visa decision
        ("Process Application", "Visa Approved?", ""),
        ("Visa Approved?", "Reject Application", "No"),
        ("Reject Application", "Application Rejected", ""),
        ("Visa Approved?", "Issue Visa/Permit", "Yes"),
        
        # Travel and registration
        ("Issue Visa/Permit", "Travel to Austria", ""),
        ("Travel to Austria", "Register Residence", ""),
        ("Register Residence", "Issue RWR Card", ""),
        
        # RWR Card and renewal loop
        ("Issue RWR Card", "Living and Working", ""),
        ("Renewal Reminder", "Renew RWR Card", ""),
        ("Renew RWR Card", "Issue RWR Card", ""),
        
        # End events
        ("Living and Working", "Hiring Complete", ""),
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
    print "PROCESS OVERVIEW:"
    print "------------------------------------------------------------------"
    print "1. DOCUMENT PREPARATION (Parallel)"
    print "   - Valid passport (3+ months validity, 2 empty pages)"
    print "   - Passport photos (35x45mm, portrait format)"
    print "   - Travel health insurance (30,000 Euro coverage, Schengen)"
    print "   - Proof of financial means"
    print ""
    print "2. JOB SEARCH & EMPLOYMENT"
    print "   - Apply for positions in Austria"
    print "   - Interview process with employer"
    print "   - Sign employment contract"
    print ""
    print "3. ACCOMMODATION & BANK (Parallel)"
    print "   - Search and negotiate accommodation"
    print "   - Open bank account"
    print ""
    print "4. VISA APPLICATION"
    print "   - Complete visa application form"
    print "   - Submit to Austrian representation"
    print "   - Document verification"
    print ""
    print "5. ROT-WEISS-ROT CARD"
    print "   - Receive RWR Card after registration"
    print "   - Renewal every X months (timer-triggered)"
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
