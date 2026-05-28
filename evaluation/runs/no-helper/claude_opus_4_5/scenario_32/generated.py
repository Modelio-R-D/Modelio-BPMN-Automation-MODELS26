#
# FarmingBot.py
#
# Description:
#   BPMN process diagram for a Farming Bot game feature.
#   Players configure custom farming bots to gather resources with dependencies,
#   handle natural disasters, receive milestone notifications, and share with friends.
#
# Lanes:
#   - Player: User interactions and decisions
#   - Bot System: Automated farming and processing
#   - Notification Service: Alerts and social features
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


def createUserTask(process, name):
    """Create a BPMN User Task (human activity)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createServiceTask(process, name):
    """Create a BPMN Service Task (automated)."""
    task = modelingSession.getModel().createBpmnServiceTask()
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


def createTimerEvent(process, name):
    """Create a BPMN Intermediate Timer Event."""
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
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
    """Parse Rectangle bounds string into dictionary."""
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
    """Get diagram graphics for an element."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def getBounds(diagramHandle, element):
    """Get bounds of an element in the diagram."""
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None


def getLaneCenterY(diagramHandle, lane):
    """Calculate center Y position for a lane."""
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format compact summary of lanes."""
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
    """Format compact summary of element positions."""
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
    return "Elements: " + ", ".join(parts) + "..."


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
    """Wait until all elements are available in diagram."""
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
    """Manually unmask elements inside their correct lane."""
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
            laneName = elementLayout.get(name, (0, "Player"))[1]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:15] + " -> Y=" + str(targetY) + ": OK"
                else:
                    print "  [Unmask] " + name[:15] + ": FAILED"
            except Exception as e:
                print "  [Unmask] " + name[:15] + ": ERROR"
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createFarmingBotProcess(parentPackage):
    """Create the Farming Bot BPMN process with diagram."""
    
    processName = "FarmingBot_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN FARMING BOT PROCESS"
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
    
    playerLane = createLane(laneSet, "Player")
    botLane = createLane(laneSet, "Bot System")
    notifyLane = createLane(laneSet, "Notification")
    
    lanes = {
        "Player": playerLane,
        "Bot System": botLane,
        "Notification": notifyLane
    }
    laneOrder = ["Player", "Bot System", "Notification"]
    
    print "[" + str(step()) + "] Lanes: Player, Bot System, Notification"
    
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
    
    # --- Player Lane Elements ---
    addElement(createStartEvent, "Start Bot Setup", playerLane)
    addElement(createUserTask, "Select Resources", playerLane)
    addElement(createUserTask, "Set Priorities", playerLane)
    addElement(createUserTask, "Update Materials", playerLane)
    addElement(createUserTask, "Select Friends", playerLane)
    addElement(createUserTask, "Choose Share Type", playerLane)
    addElement(createEndEvent, "Bot Complete", playerLane)
    print "[" + str(step()) + "] Player lane: 7 elements"
    
    # --- Bot System Lane Elements ---
    addElement(createServiceTask, "Check Dependencies", botLane)
    addElement(createServiceTask, "Create Tool Queue", botLane)
    addElement(createParallelGateway, "Split Resources", botLane)
    addElement(createServiceTask, "Farm Resource 1", botLane)
    addElement(createServiceTask, "Farm Resource 2", botLane)
    addElement(createServiceTask, "Farm Resource N", botLane)
    addElement(createParallelGateway, "Join Resources", botLane)
    addElement(createExclusiveGateway, "Disaster?", botLane)
    addElement(createServiceTask, "Handle Disaster", botLane)
    addElement(createServiceTask, "Continue Farming", botLane)
    addElement(createExclusiveGateway, "All Complete?", botLane)
    addElement(createExclusiveGateway, "Update Request?", botLane)
    addElement(createServiceTask, "Finalize Results", botLane)
    print "[" + str(step()) + "] Bot System lane: 13 elements"
    
    # --- Notification Lane Elements ---
    addElement(createServiceTask, "Check Milestones", notifyLane)
    addElement(createExclusiveGateway, "Milestone Hit?", notifyLane)
    addElement(createServiceTask, "Send Milestone Alert", notifyLane)
    addElement(createServiceTask, "Send Disaster Alert", notifyLane)
    addElement(createExclusiveGateway, "Share Type?", notifyLane)
    addElement(createServiceTask, "Post to Brag Board", notifyLane)
    addElement(createServiceTask, "Send Materials", notifyLane)
    addElement(createMessageEndEvent, "Shared Success", notifyLane)
    print "[" + str(step()) + "] Notification lane: 8 elements"
    
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
    
    # Layout: element name -> (column, lane)
    elementLayout = {
        # Player Lane
        "Start Bot Setup": (0, "Player"),
        "Select Resources": (1, "Player"),
        "Set Priorities": (2, "Player"),
        "Update Materials": (9, "Player"),
        "Select Friends": (14, "Player"),
        "Choose Share Type": (15, "Player"),
        "Bot Complete": (18, "Player"),
        
        # Bot System Lane
        "Check Dependencies": (3, "Bot System"),
        "Create Tool Queue": (4, "Bot System"),
        "Split Resources": (5, "Bot System"),
        "Farm Resource 1": (6, "Bot System"),
        "Farm Resource 2": (6, "Bot System"),
        "Farm Resource N": (6, "Bot System"),
        "Join Resources": (7, "Bot System"),
        "Disaster?": (8, "Bot System"),
        "Handle Disaster": (9, "Bot System"),
        "Continue Farming": (10, "Bot System"),
        "Update Request?": (11, "Bot System"),
        "All Complete?": (12, "Bot System"),
        "Finalize Results": (13, "Bot System"),
        
        # Notification Lane
        "Check Milestones": (7, "Notification"),
        "Milestone Hit?": (8, "Notification"),
        "Send Milestone Alert": (9, "Notification"),
        "Send Disaster Alert": (10, "Notification"),
        "Share Type?": (16, "Notification"),
        "Post to Brag Board": (17, "Notification"),
        "Send Materials": (17, "Notification"),
        "Shared Success": (18, "Notification"),
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
    print "[" + str(step()) + "] Elements ready: " + str(foundCount) + "/" + str(len(elements))
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
    
    # Special Y offsets for parallel tasks
    parallelOffsets = {
        "Farm Resource 1": -45,
        "Farm Resource 2": 0,
        "Farm Resource N": 45,
        "Post to Brag Board": -25,
        "Send Materials": 25,
    }
    
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
        
        # Apply parallel offset if needed
        if name in parallelOffsets:
            targetY += parallelOffsets[name]
        
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
        
        print "[" + str(step()) + "] " + name[:18] + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Initial setup flow
        ("Start Bot Setup", "Select Resources", ""),
        ("Select Resources", "Set Priorities", ""),
        ("Set Priorities", "Check Dependencies", ""),
        
        # Dependency and tool creation
        ("Check Dependencies", "Create Tool Queue", ""),
        ("Create Tool Queue", "Split Resources", ""),
        
        # Parallel farming (up to 10, showing 3 representative)
        ("Split Resources", "Farm Resource 1", ""),
        ("Split Resources", "Farm Resource 2", ""),
        ("Split Resources", "Farm Resource N", ""),
        ("Farm Resource 1", "Join Resources", ""),
        ("Farm Resource 2", "Join Resources", ""),
        ("Farm Resource N", "Join Resources", ""),
        
        # Milestone check during farming
        ("Join Resources", "Check Milestones", ""),
        ("Check Milestones", "Milestone Hit?", ""),
        ("Milestone Hit?", "Send Milestone Alert", "Yes"),
        ("Milestone Hit?", "Disaster?", "No"),
        ("Send Milestone Alert", "Disaster?", ""),
        
        # Disaster handling
        ("Disaster?", "Handle Disaster", "Yes"),
        ("Disaster?", "Continue Farming", "No"),
        ("Handle Disaster", "Send Disaster Alert", ""),
        ("Send Disaster Alert", "Continue Farming", ""),
        
        # Update check loop
        ("Continue Farming", "Update Request?", ""),
        ("Update Request?", "Update Materials", "Yes"),
        ("Update Materials", "Check Dependencies", ""),
        ("Update Request?", "All Complete?", "No"),
        
        # Completion check
        ("All Complete?", "Split Resources", "No"),
        ("All Complete?", "Finalize Results", "Yes"),
        
        # Share with friends
        ("Finalize Results", "Select Friends", ""),
        ("Select Friends", "Choose Share Type", ""),
        ("Choose Share Type", "Share Type?", ""),
        ("Share Type?", "Post to Brag Board", "Brag"),
        ("Share Type?", "Send Materials", "Send"),
        ("Post to Brag Board", "Shared Success", ""),
        ("Send Materials", "Shared Success", ""),
        ("Shared Success", "Bot Complete", ""),
    ]
    
    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
        else:
            print "  WARNING: Missing " + srcName + " -> " + tgtName
    
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
    print ""
    print "Game Logic Notes:"
    print "  - Resources have dependencies (tools needed first)"
    print "  - Up to 10 parallel farming tasks (3 shown)"
    print "  - Random disasters can interrupt progress"
    print "  - Milestones trigger notifications"
    print "  - Players can update materials anytime during farming"
    print "  - End: Brag to friends OR send materials"
    print "=================================================================="
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createFarmingBotProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
