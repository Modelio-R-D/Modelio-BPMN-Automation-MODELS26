#
# FindAJob.py
#
# Description:
#   BPMN process diagram for Job Search workflow.
#   4 lanes: Job Applicant, Job Platform, Company, HR System
#
# Workflow:
#   - Job applicant reports job applications regularly
#   - Platform sends potential job offers based on applications
#   - Companies confirm receipt and rate applications
#   - Job interviews can be negotiated
#   - Probation phase when hired
#   - Mutual ratings after probation
#   - Company reviews visible after 1 year
#   - Process ends when job permanent (unless rated C or less)
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
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:20] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createFindAJobProcess(parentPackage):
    """Create the Find a Job BPMN process with diagram."""
    
    processName = "FindAJob_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN FIND A JOB PROCESS"
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
    platformLane = createLane(laneSet, "Platform")
    companyLane = createLane(laneSet, "Company")
    hrSystemLane = createLane(laneSet, "HR System")
    
    lanes = {
        "Applicant": applicantLane,
        "Platform": platformLane,
        "Company": companyLane,
        "HR System": hrSystemLane
    }
    laneOrder = ["Applicant", "Platform", "Company", "HR System"]
    
    print "[" + str(step()) + "] Lanes: Applicant, Platform, Company, HR System"
    
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
    
    # --- Applicant Lane ---
    addElement(createStartEvent, "Start Job Search", applicantLane, "Applicant")
    addElement(createUserTask, "Report Applications", applicantLane, "Applicant")
    addElement(createUserTask, "Review Job Offers", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Interested?", applicantLane, "Applicant")
    addElement(createUserTask, "Negotiate Interview", applicantLane, "Applicant")
    addElement(createUserTask, "Attend Interview", applicantLane, "Applicant")
    addElement(createUserTask, "Start Probation", applicantLane, "Applicant")
    addElement(createUserTask, "Rate Company", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Job Permanent?", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Rating C or less?", applicantLane, "Applicant")
    addElement(createEndEvent, "Job Secured", applicantLane, "Applicant")
    print "[" + str(step()) + "] Applicant lane: 11 elements"
    
    # --- Platform Lane ---
    addElement(createServiceTask, "Receive Report", platformLane, "Platform")
    addElement(createServiceTask, "Match Job Offers", platformLane, "Platform")
    addElement(createServiceTask, "Send Job Offers", platformLane, "Platform")
    addElement(createServiceTask, "Store Review", platformLane, "Platform")
    addElement(createServiceTask, "Publish Review", platformLane, "Platform")
    print "[" + str(step()) + "] Platform lane: 5 elements"
    
    # --- Company Lane ---
    addElement(createServiceTask, "Receive Application", companyLane, "Company")
    addElement(createUserTask, "Confirm Receipt", companyLane, "Company")
    addElement(createUserTask, "Rate Application", companyLane, "Company")
    addElement(createExclusiveGateway, "Invite Interview?", companyLane, "Company")
    addElement(createUserTask, "Conduct Interview", companyLane, "Company")
    addElement(createExclusiveGateway, "Make Offer?", companyLane, "Company")
    addElement(createUserTask, "Send Job Offer", companyLane, "Company")
    addElement(createUserTask, "Rate Employee", companyLane, "Company")
    addElement(createEndEvent, "No Hire", companyLane, "Company")
    print "[" + str(step()) + "] Company lane: 9 elements"
    
    # --- HR System Lane ---
    addElement(createServiceTask, "Track Applications", hrSystemLane, "HR System")
    addElement(createServiceTask, "Record Interview", hrSystemLane, "HR System")
    addElement(createServiceTask, "Start Probation Period", hrSystemLane, "HR System")
    addElement(createServiceTask, "End Probation", hrSystemLane, "HR System")
    addElement(createParallelGateway, "Rating Split", hrSystemLane, "HR System")
    addElement(createParallelGateway, "Rating Join", hrSystemLane, "HR System")
    addElement(createServiceTask, "Wait 1 Year", hrSystemLane, "HR System")
    print "[" + str(step()) + "] HR System lane: 7 elements"
    
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
        # Applicant Lane
        "Start Job Search": (0, "Applicant"),
        "Report Applications": (1, "Applicant"),
        "Review Job Offers": (4, "Applicant"),
        "Interested?": (5, "Applicant"),
        "Negotiate Interview": (6, "Applicant"),
        "Attend Interview": (8, "Applicant"),
        "Start Probation": (11, "Applicant"),
        "Rate Company": (14, "Applicant"),
        "Job Permanent?": (16, "Applicant"),
        "Rating C or less?": (17, "Applicant"),
        "Job Secured": (18, "Applicant"),
        # Platform Lane
        "Receive Report": (2, "Platform"),
        "Match Job Offers": (3, "Platform"),
        "Send Job Offers": (4, "Platform"),
        "Store Review": (15, "Platform"),
        "Publish Review": (17, "Platform"),
        # Company Lane
        "Receive Application": (2, "Company"),
        "Confirm Receipt": (3, "Company"),
        "Rate Application": (4, "Company"),
        "Invite Interview?": (5, "Company"),
        "Conduct Interview": (7, "Company"),
        "Make Offer?": (9, "Company"),
        "Send Job Offer": (10, "Company"),
        "Rate Employee": (14, "Company"),
        "No Hire": (10, "Company"),
        # HR System Lane
        "Track Applications": (2, "HR System"),
        "Record Interview": (8, "HR System"),
        "Start Probation Period": (11, "HR System"),
        "End Probation": (12, "HR System"),
        "Rating Split": (13, "HR System"),
        "Rating Join": (15, "HR System"),
        "Wait 1 Year": (16, "HR System"),
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
        print "         Missing: " + ", ".join(missing[:10])
        
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
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"
    
    print ""
    
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    
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
        
        print "[" + str(step()) + "] " + laneName[:8] + "/" + name[:18] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Start and report loop
        ("Start Job Search", "Report Applications", ""),
        ("Report Applications", "Receive Report", ""),
        ("Receive Report", "Track Applications", ""),
        ("Receive Report", "Match Job Offers", ""),
        ("Match Job Offers", "Send Job Offers", ""),
        
        # Application to company
        ("Report Applications", "Receive Application", ""),
        ("Receive Application", "Confirm Receipt", ""),
        ("Confirm Receipt", "Rate Application", ""),
        ("Rate Application", "Invite Interview?", ""),
        
        # Company decision on interview
        ("Invite Interview?", "Conduct Interview", "Yes"),
        ("Invite Interview?", "No Hire", "No"),
        
        # Job offers to applicant
        ("Send Job Offers", "Review Job Offers", ""),
        ("Review Job Offers", "Interested?", ""),
        ("Interested?", "Negotiate Interview", "Yes"),
        ("Interested?", "Report Applications", "No"),
        
        # Interview negotiation
        ("Negotiate Interview", "Conduct Interview", ""),
        ("Conduct Interview", "Record Interview", ""),
        ("Record Interview", "Attend Interview", ""),
        ("Attend Interview", "Make Offer?", ""),
        
        # Company offer decision
        ("Make Offer?", "Send Job Offer", "Yes"),
        ("Make Offer?", "No Hire", "No"),
        
        # Probation
        ("Send Job Offer", "Start Probation", ""),
        ("Start Probation", "Start Probation Period", ""),
        ("Start Probation Period", "End Probation", ""),
        ("End Probation", "Rating Split", ""),
        
        # Parallel ratings
        ("Rating Split", "Rate Company", ""),
        ("Rating Split", "Rate Employee", ""),
        ("Rate Company", "Rating Join", ""),
        ("Rate Employee", "Rating Join", ""),
        
        # Store and publish review
        ("Rate Company", "Store Review", ""),
        ("Rating Join", "Wait 1 Year", ""),
        ("Wait 1 Year", "Publish Review", ""),
        
        # Job permanent decision
        ("Rating Join", "Job Permanent?", ""),
        ("Job Permanent?", "Rating C or less?", "Yes"),
        ("Job Permanent?", "Report Applications", "No"),
        
        # Rating check
        ("Rating C or less?", "Job Secured", "No"),
        ("Rating C or less?", "Review Job Offers", "Yes"),
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
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createFindAJobProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
