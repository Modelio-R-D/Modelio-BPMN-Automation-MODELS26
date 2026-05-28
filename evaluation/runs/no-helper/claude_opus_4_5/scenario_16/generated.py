#
# AnnualAuditProcess.py
#
# Description:
#   BPMN process diagram for Multinational Company Annual Audit workflow.
#   5 lanes: Audit Coordinator, Regional Office, Compliance Team, Central Audit Team, Audit Director
#
# Features:
#   - Parallel gateway for concurrent activities (regulatory check + document prep)
#   - Parallel gateway for risk assessment activities (financial, operational, compliance)
#   - Exclusive gateways for decision points (discrepancies, high risk, approval)
#   - Revision loops for clarifications and report updates
#
# Applicable on: Package
#
# Version: 1.0 - Annual Audit Process
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
SPACING = 130
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


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon - automated task)."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon - physical task)."""
    task = modelingSession.getModel().createBpmnManualTask()
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
            laneName = elementLayout.get(name, (0, "Coordinator"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + " (" + laneName[:8] + "): OK"
                else:
                    print "  [Unmask] " + name[:20] + " -> Y=" + str(targetY) + " (" + laneName[:8] + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:20] + ": ERROR - " + str(e)
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createAnnualAuditProcess(parentPackage):
    """Create the Annual Audit BPMN process with diagram."""
    
    processName = "AnnualAudit_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN ANNUAL AUDIT PROCESS"
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
    
    # Create lanes (5 lanes for the different roles)
    coordinatorLane = createLane(laneSet, "Coordinator")
    regionalLane = createLane(laneSet, "Regional")
    complianceLane = createLane(laneSet, "Compliance")
    auditTeamLane = createLane(laneSet, "AuditTeam")
    directorLane = createLane(laneSet, "Director")
    
    lanes = {
        "Coordinator": coordinatorLane,
        "Regional": regionalLane,
        "Compliance": complianceLane,
        "AuditTeam": auditTeamLane,
        "Director": directorLane
    }
    laneOrder = ["Coordinator", "Regional", "Compliance", "AuditTeam", "Director"]
    
    print "[" + str(step()) + "] Lanes: Coordinator, Regional, Compliance, AuditTeam, Director"
    
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
    
    # --- Coordinator Lane (2 elements) ---
    addElement(createStartEvent, "Audit Initiated", coordinatorLane, "Coordinator")
    addElement(createServiceTask, "Send Notification", coordinatorLane, "Coordinator")
    print "[" + str(step()) + "] Coordinator lane: 2 elements"
    
    # --- Regional Lane (4 elements) ---
    addElement(createParallelGateway, "Split Prep", regionalLane, "Regional")
    addElement(createUserTask, "Prepare Financials", regionalLane, "Regional")
    addElement(createUserTask, "Gather Documents", regionalLane, "Regional")
    addElement(createUserTask, "Submit Documents", regionalLane, "Regional")
    addElement(createUserTask, "Provide Clarification", regionalLane, "Regional")
    print "[" + str(step()) + "] Regional lane: 5 elements"
    
    # --- Compliance Lane (2 elements) ---
    addElement(createUserTask, "Check Regulations", complianceLane, "Compliance")
    addElement(createParallelGateway, "Join Prep", complianceLane, "Compliance")
    print "[" + str(step()) + "] Compliance lane: 2 elements"
    
    # --- Audit Team Lane (18 elements) ---
    addElement(createUserTask, "Review Submission", auditTeamLane, "AuditTeam")
    addElement(createExclusiveGateway, "Discrepancies?", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Request Clarify", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Risk Assessment", auditTeamLane, "AuditTeam")
    addElement(createParallelGateway, "Split Risk", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Financial Risk", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Operational Risk", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Compliance Risk", auditTeamLane, "AuditTeam")
    addElement(createParallelGateway, "Join Risk", auditTeamLane, "AuditTeam")
    addElement(createExclusiveGateway, "High Risk?", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Data Analysis", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Interviews", auditTeamLane, "AuditTeam")
    addElement(createManualTask, "Site Visits", auditTeamLane, "AuditTeam")
    addElement(createParallelGateway, "Join Invest", auditTeamLane, "AuditTeam")
    addElement(createExclusiveGateway, "Merge Path", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Compile Report", auditTeamLane, "AuditTeam")
    addElement(createUserTask, "Update Report", auditTeamLane, "AuditTeam")
    addElement(createParallelGateway, "Split Invest", auditTeamLane, "AuditTeam")
    print "[" + str(step()) + "] AuditTeam lane: 18 elements"
    
    # --- Director Lane (4 elements) ---
    addElement(createUserTask, "Review Report", directorLane, "Director")
    addElement(createExclusiveGateway, "Approved?", directorLane, "Director")
    addElement(createServiceTask, "Distribute Report", directorLane, "Director")
    addElement(createEndEvent, "Audit Closed", directorLane, "Director")
    print "[" + str(step()) + "] Director lane: 4 elements"
    
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
    
    # Layout: (column_index, lane_name)
    elementLayout = {
        # Coordinator Lane
        "Audit Initiated": (0, "Coordinator"),
        "Send Notification": (1, "Coordinator"),
        
        # Regional Lane
        "Split Prep": (2, "Regional"),
        "Prepare Financials": (3, "Regional"),
        "Gather Documents": (4, "Regional"),
        "Submit Documents": (6, "Regional"),
        "Provide Clarification": (9, "Regional"),
        
        # Compliance Lane
        "Check Regulations": (3, "Compliance"),
        "Join Prep": (5, "Compliance"),
        
        # Audit Team Lane - Main flow
        "Review Submission": (7, "AuditTeam"),
        "Discrepancies?": (8, "AuditTeam"),
        "Request Clarify": (9, "AuditTeam"),
        "Risk Assessment": (10, "AuditTeam"),
        "Split Risk": (11, "AuditTeam"),
        "Financial Risk": (12, "AuditTeam"),
        "Operational Risk": (13, "AuditTeam"),
        "Compliance Risk": (14, "AuditTeam"),
        "Join Risk": (15, "AuditTeam"),
        "High Risk?": (16, "AuditTeam"),
        "Split Invest": (17, "AuditTeam"),
        "Data Analysis": (18, "AuditTeam"),
        "Interviews": (19, "AuditTeam"),
        "Site Visits": (20, "AuditTeam"),
        "Join Invest": (21, "AuditTeam"),
        "Merge Path": (22, "AuditTeam"),
        "Compile Report": (23, "AuditTeam"),
        "Update Report": (26, "AuditTeam"),
        
        # Director Lane
        "Review Report": (24, "Director"),
        "Approved?": (25, "Director"),
        "Distribute Report": (27, "Director"),
        "Audit Closed": (28, "Director"),
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
        # Start to notification
        ("Audit Initiated", "Send Notification", ""),
        ("Send Notification", "Split Prep", ""),
        
        # Parallel split for document prep and compliance check
        ("Split Prep", "Prepare Financials", ""),
        ("Split Prep", "Check Regulations", ""),
        ("Prepare Financials", "Gather Documents", ""),
        ("Gather Documents", "Join Prep", ""),
        ("Check Regulations", "Join Prep", ""),
        
        # Submit to audit team
        ("Join Prep", "Submit Documents", ""),
        ("Submit Documents", "Review Submission", ""),
        
        # Review and discrepancy check
        ("Review Submission", "Discrepancies?", ""),
        ("Discrepancies?", "Request Clarify", "Yes"),
        ("Request Clarify", "Provide Clarification", ""),
        ("Provide Clarification", "Review Submission", ""),
        ("Discrepancies?", "Risk Assessment", "No"),
        
        # Risk assessment parallel activities
        ("Risk Assessment", "Split Risk", ""),
        ("Split Risk", "Financial Risk", ""),
        ("Split Risk", "Operational Risk", ""),
        ("Split Risk", "Compliance Risk", ""),
        ("Financial Risk", "Join Risk", ""),
        ("Operational Risk", "Join Risk", ""),
        ("Compliance Risk", "Join Risk", ""),
        
        # High risk decision
        ("Join Risk", "High Risk?", ""),
        ("High Risk?", "Split Invest", "Yes"),
        
        # Investigation parallel activities
        ("Split Invest", "Data Analysis", ""),
        ("Split Invest", "Interviews", ""),
        ("Split Invest", "Site Visits", ""),
        ("Data Analysis", "Join Invest", ""),
        ("Interviews", "Join Invest", ""),
        ("Site Visits", "Join Invest", ""),
        ("Join Invest", "Merge Path", ""),
        
        # No high risk path
        ("High Risk?", "Merge Path", "No"),
        
        # Compile and review report
        ("Merge Path", "Compile Report", ""),
        ("Compile Report", "Review Report", ""),
        ("Review Report", "Approved?", ""),
        
        # Approval decision
        ("Approved?", "Update Report", "Revise"),
        ("Update Report", "Review Report", ""),
        ("Approved?", "Distribute Report", "Approved"),
        
        # Final distribution and close
        ("Distribute Report", "Audit Closed", ""),
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
        createAnnualAuditProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
