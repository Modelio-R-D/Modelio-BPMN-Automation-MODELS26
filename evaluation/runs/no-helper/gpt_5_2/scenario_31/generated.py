#
# BlizzardOnlineCharacterGenerator.py
#
# Description:
#   BPMN process diagram: Blizzard Online Character Generator
#   Parallel behavior:
#     - While setting up the account/subscription, the player can brainstorm character names
#   Then:
#     - Log in, select realm/race/class
#     - Enter names until one is available
#     - Confirmation/selfies, then later expansion release notification
#
# Applicable on: Package
# Version: 1.0
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
SPACING = 160
START_X = 80

TASK_WIDTH = 140
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

def createMessageEndEvent(process, name):
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
    if guard:
        flow.setConditionExpression(guard)
    return flow

def createSequenceFlowWithGuard(process, source, target, guard):
    return createSequenceFlow(process, source, target, guard=guard)

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
            shortName = name[:14]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:14] + "=--")
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

def createBlizzardOnlineCharacterGenerator(parentPackage):

    processName = "BlizzardOnlineCharacterGenerator_" + EXECUTION_ID
    diagramTitle = "Blizzard Online Character Generator"

    stepCounter = [0]
    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          " + diagramTitle
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
    blizzardLane = createLane(laneSet, "Blizzard Systems")
    paymentLane = createLane(laneSet, "Payment Provider")

    lanes = {
        "Player": playerLane,
        "Blizzard Systems": blizzardLane,
        "Payment Provider": paymentLane
    }
    laneOrder = ["Player", "Blizzard Systems", "Payment Provider"]

    print "[" + str(step()) + "] Lanes: Player, Blizzard Systems, Payment Provider"

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
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        print "[" + str(step()) + "] Element: " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    # --- Player ---
    addElement(createStartEvent, "Start character creation", playerLane)
    addElement(createParallelGateway, "Parallel start", playerLane)

    addElement(createManualTask, "Brainstorm character names", playerLane)

    addElement(createUserTask, "Enter account information", playerLane)
    addElement(createUserTask, "Click confirmation link", playerLane)

    addElement(createUserTask, "Select payment method", playerLane)
    addElement(createExclusiveGateway, "Payment method", playerLane)
    addElement(createUserTask, "Enter credit card information", playerLane)
    addElement(createUserTask, "Enter IBAN and BIC", playerLane)

    addElement(createUserTask, "Log into game", playerLane)
    addElement(createUserTask, "Select realm race and class", playerLane)

    addElement(createParallelGateway, "Parallel join", playerLane)

    addElement(createUserTask, "Enter character name", playerLane)

    # --- Blizzard Systems ---
    addElement(createServiceTask, "Check battle.net account", blizzardLane)
    addElement(createExclusiveGateway, "Have battle.net account", blizzardLane)
    addElement(createServiceTask, "Send confirmation email", blizzardLane)

    addElement(createServiceTask, "Check active subscription", blizzardLane)
    addElement(createExclusiveGateway, "Subscription active", blizzardLane)

    addElement(createServiceTask, "Check name availability", blizzardLane)
    addElement(createExclusiveGateway, "Name available", blizzardLane)

    addElement(createServiceTask, "Create character", blizzardLane)
    addElement(createServiceTask, "Send confirmation and selfies", blizzardLane)
    addElement(createServiceTask, "Notify on expansion release", blizzardLane)
    addElement(createMessageEndEvent, "Expansion released message", blizzardLane)

    # --- Payment Provider ---
    addElement(createServiceTask, "Process credit card payment", paymentLane)
    addElement(createServiceTask, "Process bank transfer payment", paymentLane)

    print ""
    print "[" + str(step()) + "] Total elements created: " + str(len(elements))

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(diagramTitle + " " + EXECUTION_ID)
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: " + diagram.getName()

    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    print "[" + str(step()) + "] DiagramHandle obtained"

    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"

    # =========================================================================
    # PHASE 4: WAIT FOR AUTO-UNMASK (+ manual unmask fallback)
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        # Player
        "Start character creation": (0, "Player"),
        "Parallel start": (1, "Player"),
        "Brainstorm character names": (2, "Player"),

        "Enter account information": (4, "Player"),
        "Click confirmation link": (6, "Player"),

        "Select payment method": (10, "Player"),
        "Payment method": (11, "Player"),
        "Enter credit card information": (12, "Player"),
        "Enter IBAN and BIC": (12, "Player"),

        "Log into game": (14, "Player"),
        "Select realm race and class": (15, "Player"),
        "Parallel join": (16, "Player"),
        "Enter character name": (17, "Player"),

        # Blizzard Systems
        "Check battle.net account": (2, "Blizzard Systems"),
        "Have battle.net account": (3, "Blizzard Systems"),
        "Send confirmation email": (5, "Blizzard Systems"),

        "Check active subscription": (7, "Blizzard Systems"),
        "Subscription active": (8, "Blizzard Systems"),

        "Check name availability": (18, "Blizzard Systems"),
        "Name available": (19, "Blizzard Systems"),
        "Create character": (20, "Blizzard Systems"),
        "Send confirmation and selfies": (21, "Blizzard Systems"),
        "Notify on expansion release": (22, "Blizzard Systems"),
        "Expansion released message": (23, "Blizzard Systems"),

        # Payment Provider
        "Process credit card payment": (13, "Payment Provider"),
        "Process bank transfer payment": (13, "Payment Provider"),
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
        print "[" + str(step()) + "] Trying manual unmask for missing elements (inside correct lane Y)..."
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
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available; defaulting Y=100"
            laneY[laneName] = 100

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

        elem = elementRefs.get(name)
        if elem is None:
            print "[" + str(step()) + "] SKIP " + name + ": element ref not found"
            continue

        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        dg = elementGraphics[name]
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)

        elemClass = elem.getMClass().getName()
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
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # =========================================================================
    # PHASE 6: CREATE FLOWS (use guards for gateway outflows)
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Start and parallel split
        ("Start character creation", "Parallel start", ""),
        ("Parallel start", "Check battle.net account", ""),
        ("Parallel start", "Brainstorm character names", ""),

        # Account setup
        ("Check battle.net account", "Have battle.net account", ""),
        ("Have battle.net account", "Check active subscription", "Yes"),
        ("Have battle.net account", "Enter account information", "No"),

        ("Enter account information", "Send confirmation email", ""),
        ("Send confirmation email", "Click confirmation link", ""),
        ("Click confirmation link", "Check active subscription", ""),

        # Subscription check
        ("Check active subscription", "Subscription active", ""),
        ("Subscription active", "Log into game", "Yes"),
        ("Subscription active", "Select payment method", "No"),

        # Payment selection
        ("Select payment method", "Payment method", ""),
        ("Payment method", "Enter credit card information", "Credit card"),
        ("Payment method", "Enter IBAN and BIC", "Bank account"),

        ("Enter credit card information", "Process credit card payment", ""),
        ("Process credit card payment", "Log into game", ""),

        ("Enter IBAN and BIC", "Process bank transfer payment", ""),
        ("Process bank transfer payment", "Log into game", ""),

        # Character setup then join parallel with names brainstorm
        ("Log into game", "Select realm race and class", ""),
        ("Select realm race and class", "Parallel join", ""),
        ("Brainstorm character names", "Parallel join", ""),

        # Name entry loop until available
        ("Parallel join", "Enter character name", ""),
        ("Enter character name", "Check name availability", ""),
        ("Check name availability", "Name available", ""),

        ("Name available", "Enter character name", "No - try next"),
        ("Name available", "Create character", "Yes"),

        # Confirmation and later message
        ("Create character", "Send confirmation and selfies", ""),
        ("Send confirmation and selfies", "Notify on expansion release", ""),
        ("Notify on expansion release", "Expansion released message", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "[" + str(step()) + "] Flow: " + srcName + " -> " + tgtName + " | Guard=" + guard
            else:
                print "[" + str(step()) + "] Flow: " + srcName + " -> " + tgtName
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow " + srcName + " -> " + tgtName

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
    print "Title:    " + diagramTitle
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
        createBlizzardOnlineCharacterGenerator(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
