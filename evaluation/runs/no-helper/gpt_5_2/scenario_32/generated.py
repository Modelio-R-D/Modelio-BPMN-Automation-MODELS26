#
# FarmingBotProcess.py
#
# Description:
#   BPMN process diagram: "Farming Bot"
#   Players configure a custom farming bot to gather resources (up to 10 in parallel),
#   with urgency, tool dependencies, milestone notifications, random disasters,
#   and the ability to update the farming list during execution.
#   After completion: brag to friends and/or send materials.
#
# Applicable on: Package
#
# Version: v1.0 - March 2026
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
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
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 170
START_X = 80

TASK_WIDTH = 150
TASK_HEIGHT = 60

# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane

def addToLane(element, lane):
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False

def createStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createUserTask(process, name):
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createManualTask(process, name):
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createServiceTask(process, name):
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createExclusiveGateway(process, name):
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createParallelGateway(process, name):
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createSequenceFlow(process, source, target, name="", guard=""):
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(name)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)

    # IMPORTANT: use guard (ConditionExpression) for gateway outflow labels
    if guard:
        try:
            flow.setConditionExpression(guard)
        except:
            pass
    return flow

# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def parseBounds(boundsStr):
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
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None

def getBounds(diagramHandle, element):
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None

def getLaneCenterY(diagramHandle, lane):
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        # Slight offset to visually center typical BPMN shapes
        return bounds["y"] + bounds["h"] / 2 - 23
    return None

def formatLanesSummary(diagramHandle, lanes, laneOrder):
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
            parts.append(name[:12] + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:12] + "=--")
    return "Elements: " + ", ".join(parts)

# ============================================================================
# WAIT FOR AUTO-UNMASK
# ============================================================================

def waitForElements(diagramHandle, elements):
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
    unmaskedCount = 0

    # Determine lane center Y (must unmask inside lane)
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
                    print "  [Unmask] " + name + " -> Y=" + str(targetY) + " (" + laneName + "): OK"
                else:
                    print "  [Unmask] " + name + " -> Y=" + str(targetY) + " (" + laneName + "): FAILED"
            except Exception as e:
                print "  [Unmask] " + name + ": ERROR - " + str(e)

    return unmaskedCount

# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createFarmingBotProcess(parentPackage):

    processName = "FarmingBot_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Farming Bot"
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
    print "[" + str(step()) + "] Process created: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    playerLane = createLane(laneSet, "Player")
    botLane = createLane(laneSet, "Farming Bot")
    worldLane = createLane(laneSet, "Game World")
    friendsLane = createLane(laneSet, "Friends")

    lanes = {
        "Player": playerLane,
        "Farming Bot": botLane,
        "Game World": worldLane,
        "Friends": friendsLane
    }
    laneOrder = ["Player", "Farming Bot", "Game World", "Friends"]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""

    elements = []
    elementRefs = {}

    laneCounts = {"Player": 0, "Farming Bot": 0, "Game World": 0, "Friends": 0}

    def addElement(creator, name, laneName):
        lane = lanes[laneName]
        elem = creator(process, name)
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        laneCounts[laneName] = laneCounts.get(laneName, 0) + 1

        status = "OK" if ok else "FAILED"
        print "  [Elem] " + laneName + " | " + name + " | addToLane=" + status
        return elem

    # --- Player configuration ---
    addElement(createStartEvent, "Start", "Player")
    addElement(createUserTask, "Select target resources", "Player")
    addElement(createUserTask, "Set urgency and priorities", "Player")
    addElement(createUserTask, "Define tool dependencies", "Player")
    addElement(createUserTask, "Confirm farming plan", "Player")

    # Notifications / updates / post actions
    addElement(createUserTask, "View milestone notification", "Player")
    addElement(createUserTask, "Update target list", "Player")
    addElement(createUserTask, "See completion notification", "Player")
    addElement(createUserTask, "Brag to selected friends", "Player")
    addElement(createEndEvent, "Done", "Player")

    # --- Bot planning / farming ---
    addElement(createServiceTask, "Compile preferences", "Farming Bot")
    addElement(createExclusiveGateway, "Any tool dependencies?", "Farming Bot")
    addElement(createServiceTask, "Plan required tools", "Farming Bot")
    addElement(createServiceTask, "Craft starter tools", "Farming Bot")
    addElement(createServiceTask, "Start farming", "Farming Bot")

    addElement(createParallelGateway, "Collect resources (<=10)", "Farming Bot")
    addElement(createServiceTask, "Collect Wood", "Farming Bot")
    addElement(createServiceTask, "Collect Stone", "Farming Bot")
    addElement(createParallelGateway, "Base resources collected", "Farming Bot")

    addElement(createServiceTask, "Craft Pickaxe", "Farming Bot")

    addElement(createParallelGateway, "Mine resources", "Farming Bot")
    addElement(createServiceTask, "Mine Iron Ore", "Farming Bot")
    addElement(createServiceTask, "Mine Gems", "Farming Bot")
    addElement(createParallelGateway, "Resources collected", "Farming Bot")

    addElement(createServiceTask, "Evaluate progress", "Farming Bot")
    addElement(createServiceTask, "Check milestones", "Farming Bot")
    addElement(createExclusiveGateway, "Milestone reached?", "Farming Bot")
    addElement(createServiceTask, "Notify player (milestone)", "Farming Bot")
    addElement(createExclusiveGateway, "Update requested?", "Farming Bot")
    addElement(createServiceTask, "Refresh plan", "Farming Bot")

    addElement(createExclusiveGateway, "More resources needed?", "Farming Bot")
    addElement(createServiceTask, "Finalize inventory", "Farming Bot")
    addElement(createServiceTask, "Notify completion", "Farming Bot")

    addElement(createParallelGateway, "Post farm actions", "Farming Bot")
    addElement(createServiceTask, "Send materials to friends", "Farming Bot")
    addElement(createParallelGateway, "Post actions done", "Farming Bot")

    # --- Game world randomness ---
    addElement(createExclusiveGateway, "Natural disaster?", "Game World")
    addElement(createServiceTask, "Natural disaster setback", "Game World")

    # --- Friends receive actions ---
    addElement(createManualTask, "Friends see brag", "Friends")
    addElement(createManualTask, "Friends receive materials", "Friends")

    print ""
    print "[" + str(step()) + "] Lane element counts:"
    for ln in laneOrder:
        print "  - " + ln + ": " + str(laneCounts.get(ln, 0))

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
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout: name -> (column, laneName)
    elementLayout = {
        # Player
        "Start": (0, "Player"),
        "Select target resources": (1, "Player"),
        "Set urgency and priorities": (2, "Player"),
        "Define tool dependencies": (3, "Player"),
        "Confirm farming plan": (4, "Player"),

        "View milestone notification": (21, "Player"),
        "Update target list": (23, "Player"),
        "See completion notification": (30, "Player"),
        "Brag to selected friends": (32, "Player"),
        "Done": (35, "Player"),

        # Bot
        "Compile preferences": (5, "Farming Bot"),
        "Any tool dependencies?": (6, "Farming Bot"),
        "Plan required tools": (7, "Farming Bot"),
        "Craft starter tools": (8, "Farming Bot"),
        "Start farming": (9, "Farming Bot"),

        "Collect resources (<=10)": (10, "Farming Bot"),
        "Collect Wood": (11, "Farming Bot"),
        "Collect Stone": (11, "Farming Bot"),
        "Base resources collected": (12, "Farming Bot"),

        "Craft Pickaxe": (13, "Farming Bot"),

        "Mine resources": (14, "Farming Bot"),
        "Mine Iron Ore": (15, "Farming Bot"),
        "Mine Gems": (15, "Farming Bot"),
        "Resources collected": (16, "Farming Bot"),

        "Evaluate progress": (17, "Farming Bot"),
        "Check milestones": (18, "Farming Bot"),
        "Milestone reached?": (19, "Farming Bot"),
        "Notify player (milestone)": (20, "Farming Bot"),
        "Update requested?": (22, "Farming Bot"),
        "Refresh plan": (24, "Farming Bot"),

        "More resources needed?": (27, "Farming Bot"),
        "Finalize inventory": (28, "Farming Bot"),
        "Notify completion": (29, "Farming Bot"),

        "Post farm actions": (31, "Farming Bot"),
        "Send materials to friends": (32, "Farming Bot"),
        "Post actions done": (34, "Farming Bot"),

        # Game World
        "Natural disaster?": (25, "Game World"),
        "Natural disaster setback": (26, "Game World"),

        # Friends
        "Friends see brag": (33, "Friends"),
        "Friends receive materials": (33, "Friends"),
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
        y = getLaneCenterY(diagramHandle, lanes[laneName])
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"

    print ""
    sortedElements = []
    for name, (col, ln) in elementLayout.items():
        sortedElements.append((col, name, ln))
    sortedElements.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedElements:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs.get(name)
        if elem is None:
            print "[" + str(step()) + "] SKIP " + name + ": elementRefs missing"
            continue

        dg = elementGraphics[name]
        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)

        elemClass = ""
        try:
            elemClass = elem.getMClass().getName()
        except:
            elemClass = "?"

        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]

        newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
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
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Player config
        ("Start", "Select target resources", ""),
        ("Select target resources", "Set urgency and priorities", ""),
        ("Set urgency and priorities", "Define tool dependencies", ""),
        ("Define tool dependencies", "Confirm farming plan", ""),

        # Hand-off to bot
        ("Confirm farming plan", "Compile preferences", ""),

        # Tool dependency logic
        ("Compile preferences", "Any tool dependencies?", ""),
        ("Any tool dependencies?", "Plan required tools", "Yes"),
        ("Any tool dependencies?", "Start farming", "No"),
        ("Plan required tools", "Craft starter tools", ""),
        ("Craft starter tools", "Start farming", ""),

        # Start farming -> parallel collect (example; diagram label says <=10)
        ("Start farming", "Collect resources (<=10)", ""),

        # Parallel collect base materials
        ("Collect resources (<=10)", "Collect Wood", ""),
        ("Collect resources (<=10)", "Collect Stone", ""),
        ("Collect Wood", "Base resources collected", ""),
        ("Collect Stone", "Base resources collected", ""),

        # Craft pickaxe -> parallel mine
        ("Base resources collected", "Craft Pickaxe", ""),
        ("Craft Pickaxe", "Mine resources", ""),
        ("Mine resources", "Mine Iron Ore", ""),
        ("Mine resources", "Mine Gems", ""),
        ("Mine Iron Ore", "Resources collected", ""),
        ("Mine Gems", "Resources collected", ""),

        # Evaluate / milestones
        ("Resources collected", "Evaluate progress", ""),
        ("Evaluate progress", "Check milestones", ""),
        ("Check milestones", "Milestone reached?", ""),
        ("Milestone reached?", "Notify player (milestone)", "Yes"),
        ("Milestone reached?", "Update requested?", "No"),

        # Notify player milestone then player views it
        ("Notify player (milestone)", "View milestone notification", ""),
        ("View milestone notification", "Update requested?", ""),

        # Update requested path (can happen any time, modeled each cycle)
        ("Update requested?", "Update target list", "Yes"),
        ("Update requested?", "Natural disaster?", "No"),
        ("Update target list", "Refresh plan", ""),
        ("Refresh plan", "Collect resources (<=10)", ""),

        # Random disaster
        ("Natural disaster?", "Natural disaster setback", "Yes"),
        ("Natural disaster?", "More resources needed?", "No"),
        ("Natural disaster setback", "Collect resources (<=10)", ""),

        # Loop until done
        ("More resources needed?", "Collect resources (<=10)", "Yes"),
        ("More resources needed?", "Finalize inventory", "No"),
        ("Finalize inventory", "Notify completion", ""),
        ("Notify completion", "See completion notification", ""),

        # Post actions: brag and/or send materials in parallel
        ("See completion notification", "Post farm actions", ""),
        ("Post farm actions", "Brag to selected friends", ""),
        ("Post farm actions", "Send materials to friends", ""),
        ("Brag to selected friends", "Friends see brag", ""),
        ("Send materials to friends", "Friends receive materials", ""),
        ("Friends see brag", "Post actions done", ""),
        ("Friends receive materials", "Post actions done", ""),
        ("Post actions done", "Done", ""),
    ]

    flows = []
    missingFlowEndpoints = 0

    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName + " -> " + tgtName + " | guard=" + guard
            else:
                print "  [Flow] " + srcName + " -> " + tgtName
        else:
            missingFlowEndpoints += 1
            print "  [Flow] WARNING: Missing endpoint for " + srcName + " -> " + tgtName

    print ""
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    if missingFlowEndpoints > 0:
        print "[" + str(step()) + "] WARNING: " + str(missingFlowEndpoints) + " flows had missing endpoints"

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
        createFarmingBotProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
