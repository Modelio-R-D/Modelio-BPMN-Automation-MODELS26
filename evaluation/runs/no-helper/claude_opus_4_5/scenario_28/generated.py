#
# InternshipProcess.py
#
# Description:
#   BPMN process diagram for Internship Application and Management workflow.
#   4 lanes: Applicant, Platform, Company, Social Media
#
# Workflow:
#   - Applicant enters topic, budget, experience, hobbies
#   - Multiple offers arrive at arbitrary times
#   - Applicant can accept/deny offers
#   - Accepting one offer invalidates others
#   - Weekly status updates from both sides (3 each)
#   - Post-internship recommendation via parallel tweets
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
from org.modelio.metamodel.bpmn.events import BpmnIntermediateCatchEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.gateways import BpmnParallelGateway
from org.modelio.metamodel.bpmn.gateways import BpmnEventBasedGateway
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
    """Create a BPMN Exclusive Gateway (XOR)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (AND)."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createEventBasedGateway(process, name):
    """Create a BPMN Event-Based Gateway."""
    gateway = modelingSession.getModel().createBpmnEventBasedGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createIntermediateCatchEvent(process, name):
    """Create a BPMN Intermediate Catch Event."""
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createMessageIntermediateCatchEvent(process, name):
    """Create a BPMN Message Intermediate Catch Event."""
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


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
    """Create the Internship BPMN process with diagram."""
    
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
    
    applicantLane = createLane(laneSet, "Applicant")
    platformLane = createLane(laneSet, "Platform")
    companyLane = createLane(laneSet, "Company")
    socialLane = createLane(laneSet, "Social Media")
    
    lanes = {
        "Applicant": applicantLane,
        "Platform": platformLane,
        "Company": companyLane,
        "Social Media": socialLane
    }
    laneOrder = ["Applicant", "Platform", "Company", "Social Media"]
    
    print "[" + str(step()) + "] Lanes: Applicant, Platform, Company, Social Media"
    
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
    addElement(createStartEvent, "Start", applicantLane, "Applicant")
    addElement(createUserTask, "Enter Topic", applicantLane, "Applicant")
    addElement(createUserTask, "Enter Budget", applicantLane, "Applicant")
    addElement(createUserTask, "Enter Experience", applicantLane, "Applicant")
    addElement(createUserTask, "Enter Hobbies", applicantLane, "Applicant")
    addElement(createUserTask, "Review Offer", applicantLane, "Applicant")
    addElement(createExclusiveGateway, "Accept?", applicantLane, "Applicant")
    addElement(createUserTask, "Write Update 1", applicantLane, "Applicant")
    addElement(createUserTask, "Write Update 2", applicantLane, "Applicant")
    addElement(createUserTask, "Write Update 3", applicantLane, "Applicant")
    addElement(createUserTask, "Select Friends", applicantLane, "Applicant")
    print "[" + str(step()) + "] Applicant lane: 11 elements"
    
    # --- Platform Lane ---
    addElement(createServiceTask, "Submit Profile", platformLane, "Platform")
    addElement(createEventBasedGateway, "Wait Events", platformLane, "Platform")
    addElement(createMessageIntermediateCatchEvent, "Offer Arrived", platformLane, "Platform")
    addElement(createServiceTask, "Invalidate Offers", platformLane, "Platform")
    addElement(createServiceTask, "Start Internship", platformLane, "Platform")
    addElement(createParallelGateway, "Status Split", platformLane, "Platform")
    addElement(createParallelGateway, "Status Join", platformLane, "Platform")
    addElement(createServiceTask, "Complete Internship", platformLane, "Platform")
    print "[" + str(step()) + "] Platform lane: 8 elements"
    
    # --- Company Lane ---
    addElement(createUserTask, "Send Offer", companyLane, "Company")
    addElement(createUserTask, "Company Update 1", companyLane, "Company")
    addElement(createUserTask, "Company Update 2", companyLane, "Company")
    addElement(createUserTask, "Company Update 3", companyLane, "Company")
    print "[" + str(step()) + "] Company lane: 4 elements"
    
    # --- Social Media Lane ---
    addElement(createParallelGateway, "Tweet Split", socialLane, "Social Media")
    addElement(createServiceTask, "Tweet Friend 1", socialLane, "Social Media")
    addElement(createServiceTask, "Tweet Friend 2", socialLane, "Social Media")
    addElement(createServiceTask, "Tweet Friend 3", socialLane, "Social Media")
    addElement(createParallelGateway, "Tweet Join", socialLane, "Social Media")
    addElement(createEndEvent, "End", socialLane, "Social Media")
    print "[" + str(step()) + "] Social Media lane: 6 elements"
    
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
    
    elementLayout = {
        # Applicant Lane
        "Start": (0, "Applicant"),
        "Enter Topic": (1, "Applicant"),
        "Enter Budget": (2, "Applicant"),
        "Enter Experience": (3, "Applicant"),
        "Enter Hobbies": (4, "Applicant"),
        "Review Offer": (7, "Applicant"),
        "Accept?": (8, "Applicant"),
        "Write Update 1": (11, "Applicant"),
        "Write Update 2": (12, "Applicant"),
        "Write Update 3": (13, "Applicant"),
        "Select Friends": (15, "Applicant"),
        # Platform Lane
        "Submit Profile": (5, "Platform"),
        "Wait Events": (6, "Platform"),
        "Offer Arrived": (7, "Platform"),
        "Invalidate Offers": (9, "Platform"),
        "Start Internship": (10, "Platform"),
        "Status Split": (11, "Platform"),
        "Status Join": (14, "Platform"),
        "Complete Internship": (15, "Platform"),
        # Company Lane
        "Send Offer": (6, "Company"),
        "Company Update 1": (11, "Company"),
        "Company Update 2": (12, "Company"),
        "Company Update 3": (13, "Company"),
        # Social Media Lane
        "Tweet Split": (16, "Social Media"),
        "Tweet Friend 1": (17, "Social Media"),
        "Tweet Friend 2": (17, "Social Media"),
        "Tweet Friend 3": (17, "Social Media"),
        "Tweet Join": (18, "Social Media"),
        "End": (19, "Social Media"),
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
    
    # Special Y offsets for parallel tweets (they stack vertically)
    tweetOffsets = {
        "Tweet Friend 1": -40,
        "Tweet Friend 2": 0,
        "Tweet Friend 3": 40,
    }
    
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
        
        # Apply special offset for parallel tweets
        if name in tweetOffsets:
            targetY += tweetOffsets[name]
        
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
        
        print "[" + str(step()) + "] " + laneName[:8] + "/" + name[:15] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Application phase
        ("Start", "Enter Topic", ""),
        ("Enter Topic", "Enter Budget", ""),
        ("Enter Budget", "Enter Experience", ""),
        ("Enter Experience", "Enter Hobbies", ""),
        ("Enter Hobbies", "Submit Profile", ""),
        
        # Waiting for offers
        ("Submit Profile", "Wait Events", ""),
        ("Wait Events", "Offer Arrived", ""),
        ("Send Offer", "Offer Arrived", ""),
        ("Offer Arrived", "Review Offer", ""),
        
        # Decision on offer
        ("Review Offer", "Accept?", ""),
        ("Accept?", "Wait Events", "Deny"),
        ("Accept?", "Invalidate Offers", "Accept"),
        
        # Start internship
        ("Invalidate Offers", "Start Internship", ""),
        ("Start Internship", "Status Split", ""),
        
        # Parallel status updates
        ("Status Split", "Write Update 1", ""),
        ("Status Split", "Company Update 1", ""),
        ("Write Update 1", "Write Update 2", ""),
        ("Write Update 2", "Write Update 3", ""),
        ("Company Update 1", "Company Update 2", ""),
        ("Company Update 2", "Company Update 3", ""),
        ("Write Update 3", "Status Join", ""),
        ("Company Update 3", "Status Join", ""),
        
        # Complete internship
        ("Status Join", "Complete Internship", ""),
        ("Complete Internship", "Select Friends", ""),
        
        # Social media recommendation
        ("Select Friends", "Tweet Split", ""),
        ("Tweet Split", "Tweet Friend 1", ""),
        ("Tweet Split", "Tweet Friend 2", ""),
        ("Tweet Split", "Tweet Friend 3", ""),
        ("Tweet Friend 1", "Tweet Join", ""),
        ("Tweet Friend 2", "Tweet Join", ""),
        ("Tweet Friend 3", "Tweet Join", ""),
        ("Tweet Join", "End", ""),
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
        createInternshipProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
