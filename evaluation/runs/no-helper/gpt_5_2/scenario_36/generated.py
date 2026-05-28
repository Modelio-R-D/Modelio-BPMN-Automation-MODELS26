#
# LuxuryAirplane.py
#
# Description:
#   BPMN process diagram: "Luxury Airplane"
#   Customer specifies luxury interior options (bar type, seats, colors, toilet water level, extras),
#   factory sends requirements to teams, manufactures parts in parallel, assembles interior,
#   test flight and protocol distribution, delivery and customer confirmation.
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
WAIT_TIME_MS = 80
MAX_ATTEMPTS = 6

# Layout configuration
SPACING = 170
START_X = 80

# Element sizes
TASK_WIDTH = 170
TASK_HEIGHT = 60
GATEWAY_SIZE = 45
EVENT_SIZE = 30

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
    except Exception as e:
        print "  [addToLane] ERROR: " + element.getName() + " -> " + lane.getName() + " : " + str(e)
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

    # IMPORTANT: Guards (condition labels) must be set as conditionExpression
    if guard:
        flow.setConditionExpression(guard)

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
        return bounds["y"] + bounds["h"] / 2 - 23
    return None

def formatLanesSummary(diagramHandle, lanes, laneOrder):
    parts = []
    for laneName in laneOrder:
        lane = lanes.get(laneName)
        info = getBounds(diagramHandle, lane) if lane else None
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
        b = getBounds(diagramHandle, elem)
        if b:
            parts.append(name[:18] + "=Y" + str(int(b["y"])))
        else:
            parts.append(name[:18] + "=--")
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
            missing = [e.getName()[:16] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)

        time.sleep(WAIT_TIME_MS / 1000.0)

    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt

def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """
    Manual unmask fallback.
    CRITICAL: Must unmask at Y position INSIDE the correct lane.
    """
    unmaskedCount = 0

    # Lane center Y values
    laneY = {}
    for laneName, lane in lanes.items():
        b = getBounds(diagramHandle, lane)
        if b:
            centerY = int(b["y"] + b["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Customer"))[1]
            targetY = laneY.get(laneName, 120)

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

def createLuxuryAirplaneProcess(parentPackage):
    processName = "LuxuryAirplane_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:          Luxury Airplane"
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="

    # -----------------------------------------------------------------------
    # PHASE 1: CREATE PROCESS & LANES
    # -----------------------------------------------------------------------
    print ""
    print "== PHASE 1: CREATE PROCESS & LANES =============================="
    print ""

    process = modelingSession.getModel().createBpmnProcess()
    process.setName(processName)
    process.setOwner(parentPackage)
    print "[" + str(step()) + "] Process created: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    # Lane names must match exactly everywhere
    laneOrder = [
        "Customer",
        "Engineering",
        "Bar Team",
        "Seats Team",
        "Toilet Team",
        "Lighting Team",
        "Entertainment Team",
        "Assembly",
        "Test Flight",
        "Logistics"
    ]

    lanes = {}
    for ln in laneOrder:
        lanes[ln] = createLane(laneSet, ln)

    print "[" + str(step()) + "] Lanes created: " + ", ".join(laneOrder)

    # -----------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # -----------------------------------------------------------------------
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""

    elements = []
    elementRefs = {}

    def addElement(creator, name, laneName):
        lane = lanes[laneName]
        elem = creator(process, name)
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        if not ok:
            print "  [Element] WARNING: addToLane failed for: " + name + " -> " + laneName
        return elem

    # --- Customer (specification) ---
    addElement(createStartEvent, "Customer wants luxury airplane", "Customer")
    addElement(createUserTask, "Choose bar type", "Customer")
    addElement(createUserTask, "Choose seat count", "Customer")
    addElement(createUserTask, "Choose seat color", "Customer")
    addElement(createUserTask, "Choose toilet water level", "Customer")
    addElement(createUserTask, "Choose extras (lighting, IFE)", "Customer")
    addElement(createUserTask, "Send specifications", "Customer")

    # --- Engineering (intake + coordination) ---
    addElement(createUserTask, "Receive specifications", "Engineering")
    addElement(createServiceTask, "Validate specifications", "Engineering")
    addElement(createServiceTask, "Send requirements to teams", "Engineering")

    # Split to parallel manufacturing
    addElement(createParallelGateway, "Manufacture parts", "Engineering")

    # Bar selection routing (exclusive)
    addElement(createExclusiveGateway, "Which bar?", "Engineering")

    # Bar manufacturing tasks (in Bar Team lane)
    addElement(createManualTask, "Russian team - Build Vodka bar", "Bar Team")
    addElement(createManualTask, "Irish team - Build Whiskey bar", "Bar Team")
    addElement(createManualTask, "French team - Build Champagne bar", "Bar Team")
    addElement(createManualTask, "Japanese team - Build Sushi bar", "Bar Team")
    addElement(createManualTask, "Italian team - Build Espresso bar", "Bar Team")

    # Merge back after selected bar
    addElement(createExclusiveGateway, "Bar ready", "Engineering")

    # Other parts in parallel
    addElement(createManualTask, "Build seats package (count and color)", "Seats Team")
    addElement(createManualTask, "Configure toilet system (water level)", "Toilet Team")
    addElement(createManualTask, "Prepare mood lighting kit", "Lighting Team")
    addElement(createManualTask, "Prepare entertainment system (IFE)", "Entertainment Team")

    # Join parallel branches
    addElement(createParallelGateway, "All parts ready", "Engineering")

    # Assembly and testing
    addElement(createManualTask, "Assemble luxury interior", "Assembly")
    addElement(createManualTask, "Integrate interior into airplane", "Assembly")

    addElement(createManualTask, "Perform test flight", "Test Flight")
    addElement(createServiceTask, "Create test protocol", "Test Flight")

    # Distribute protocol to customer and factory
    addElement(createParallelGateway, "Distribute protocol", "Test Flight")
    addElement(createUserTask, "Receive test protocol (Customer)", "Customer")
    addElement(createUserTask, "Receive test protocol (Factory)", "Engineering")
    addElement(createParallelGateway, "Protocol distributed", "Test Flight")

    # Delivery and confirmation
    addElement(createManualTask, "Deliver airplane", "Logistics")
    addElement(createUserTask, "Confirm delivery", "Customer")
    addElement(createEndEvent, "Luxury airplane accepted", "Customer")

    print "[" + str(step()) + "] Total elements created: " + str(len(elements))

    # -----------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # -----------------------------------------------------------------------
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

    # Save triggers auto-unmask (do NOT unmask manually here)
    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"

    # -----------------------------------------------------------------------
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # -----------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Customer spec chain
        "Customer wants luxury airplane": (0, "Customer"),
        "Choose bar type": (1, "Customer"),
        "Choose seat count": (2, "Customer"),
        "Choose seat color": (3, "Customer"),
        "Choose toilet water level": (4, "Customer"),
        "Choose extras (lighting, IFE)": (5, "Customer"),
        "Send specifications": (6, "Customer"),

        # Engineering intake
        "Receive specifications": (7, "Engineering"),
        "Validate specifications": (8, "Engineering"),
        "Send requirements to teams": (9, "Engineering"),

        # Parallel manufacturing
        "Manufacture parts": (10, "Engineering"),

        # Bar routing + production
        "Which bar?": (11, "Engineering"),
        "Russian team - Build Vodka bar": (12, "Bar Team"),
        "Irish team - Build Whiskey bar": (12, "Bar Team"),
        "French team - Build Champagne bar": (12, "Bar Team"),
        "Japanese team - Build Sushi bar": (12, "Bar Team"),
        "Italian team - Build Espresso bar": (12, "Bar Team"),
        "Bar ready": (13, "Engineering"),

        # Other parallel parts
        "Build seats package (count and color)": (12, "Seats Team"),
        "Configure toilet system (water level)": (12, "Toilet Team"),
        "Prepare mood lighting kit": (12, "Lighting Team"),
        "Prepare entertainment system (IFE)": (12, "Entertainment Team"),

        # Join and assembly
        "All parts ready": (14, "Engineering"),
        "Assemble luxury interior": (15, "Assembly"),
        "Integrate interior into airplane": (16, "Assembly"),

        # Test and protocol
        "Perform test flight": (17, "Test Flight"),
        "Create test protocol": (18, "Test Flight"),
        "Distribute protocol": (19, "Test Flight"),
        "Receive test protocol (Customer)": (20, "Customer"),
        "Receive test protocol (Factory)": (20, "Engineering"),
        "Protocol distributed": (21, "Test Flight"),

        # Delivery
        "Deliver airplane": (22, "Logistics"),
        "Confirm delivery": (23, "Customer"),
        "Luxury airplane accepted": (24, "Customer")
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

    # -----------------------------------------------------------------------
    # PHASE 5: REPOSITION ELEMENTS
    # -----------------------------------------------------------------------
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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (default Y used)"

    print ""
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    # Sort by column for left-to-right placement
    sortedElements = []
    for name, (col, ln) in elementLayout.items():
        sortedElements.append((col, name, ln))
    sortedElements.sort()

    repositionedCount = 0

    for col, name, ln in sortedElements:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs.get(name)
        if not elem:
            print "[" + str(step()) + "] SKIP " + name + ": no reference"
            continue

        dg = elementGraphics[name]
        b = getBounds(diagramHandle, elem)
        if not b:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(ln, 120)

        mclass = elem.getMClass().getName()

        width = b["w"]
        height = b["h"]

        if "Gateway" in mclass:
            width = GATEWAY_SIZE
            height = GATEWAY_SIZE
        elif "Event" in mclass:
            width = EVENT_SIZE
            height = EVENT_SIZE
        elif "Task" in mclass:
            width = TASK_WIDTH
            height = TASK_HEIGHT

        newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
        dg.setBounds(newBounds)
        repositionedCount += 1

        diagramHandle.save()

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + ln + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged

        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # -----------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (WITH GUARDS FROM GATEWAYS)
    # -----------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Customer specification chain
        ("Customer wants luxury airplane", "Choose bar type", ""),
        ("Choose bar type", "Choose seat count", ""),
        ("Choose seat count", "Choose seat color", ""),
        ("Choose seat color", "Choose toilet water level", ""),
        ("Choose toilet water level", "Choose extras (lighting, IFE)", ""),
        ("Choose extras (lighting, IFE)", "Send specifications", ""),

        # To engineering
        ("Send specifications", "Receive specifications", ""),
        ("Receive specifications", "Validate specifications", ""),
        ("Validate specifications", "Send requirements to teams", ""),
        ("Send requirements to teams", "Manufacture parts", ""),

        # Parallel split to branches
        ("Manufacture parts", "Which bar?", ""),
        ("Manufacture parts", "Build seats package (count and color)", ""),
        ("Manufacture parts", "Configure toilet system (water level)", ""),
        ("Manufacture parts", "Prepare mood lighting kit", ""),
        ("Manufacture parts", "Prepare entertainment system (IFE)", ""),

        # Bar choice routing (GUARDS on outgoing flows)
        ("Which bar?", "Russian team - Build Vodka bar", "Vodka bar"),
        ("Which bar?", "Irish team - Build Whiskey bar", "Whiskey bar"),
        ("Which bar?", "French team - Build Champagne bar", "Champagne bar"),
        ("Which bar?", "Japanese team - Build Sushi bar", "Sushi bar"),
        ("Which bar?", "Italian team - Build Espresso bar", "Espresso bar"),

        # Bar merge
        ("Russian team - Build Vodka bar", "Bar ready", ""),
        ("Irish team - Build Whiskey bar", "Bar ready", ""),
        ("French team - Build Champagne bar", "Bar ready", ""),
        ("Japanese team - Build Sushi bar", "Bar ready", ""),
        ("Italian team - Build Espresso bar", "Bar ready", ""),

        # Join all parts
        ("Bar ready", "All parts ready", ""),
        ("Build seats package (count and color)", "All parts ready", ""),
        ("Configure toilet system (water level)", "All parts ready", ""),
        ("Prepare mood lighting kit", "All parts ready", ""),
        ("Prepare entertainment system (IFE)", "All parts ready", ""),

        # Assembly and testing
        ("All parts ready", "Assemble luxury interior", ""),
        ("Assemble luxury interior", "Integrate interior into airplane", ""),
        ("Integrate interior into airplane", "Perform test flight", ""),
        ("Perform test flight", "Create test protocol", ""),

        # Distribute protocol to customer and factory, then join
        ("Create test protocol", "Distribute protocol", ""),
        ("Distribute protocol", "Receive test protocol (Customer)", ""),
        ("Distribute protocol", "Receive test protocol (Factory)", ""),
        ("Receive test protocol (Customer)", "Protocol distributed", ""),
        ("Receive test protocol (Factory)", "Protocol distributed", ""),

        # Delivery and acceptance
        ("Protocol distributed", "Deliver airplane", ""),
        ("Deliver airplane", "Confirm delivery", ""),
        ("Confirm delivery", "Luxury airplane accepted", "")
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
        else:
            print "[" + str(step()) + "] WARNING: Missing element for flow: " + srcName + " -> " + tgtName

    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    diagramHandle.save()
    print "[" + str(step()) + "] Save"

    # -----------------------------------------------------------------------
    # FINAL STATE
    # -----------------------------------------------------------------------
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
    print "Title:    Luxury Airplane"
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
        createLuxuryAirplaneProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
