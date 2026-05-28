#
# InternshipProcess.py
#
# Description:
#   BPMN process diagram: Internship
#
#   - You enter topic, budget, experience, hobbies
#   - Several offers arrive at arbitrary times (modeled as a loop waiting for offers)
#   - You accept or deny offers
#   - Once accepted, all other offers become invalid
#   - Intern writes at least 3 weekly status updates
#   - Company writes 3 status updates about the intern
#   - After internship finished, recommend company to friends via Twitter
#   - Separate tweets are sent in parallel
#
# Applicable on: Package
#
# Version: v9.1
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

SCRIPT_VERSION = "v9.1"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 150
START_X = 80

# Task dimensions (help text fit)
TASK_WIDTH = 170
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
    gw = modelingSession.getModel().createBpmnExclusiveGateway()
    gw.setName(name)
    gw.setContainer(process)
    return gw

def createParallelGateway(process, name):
    gw = modelingSession.getModel().createBpmnParallelGateway()
    gw.setName(name)
    gw.setContainer(process)
    return gw

def createSequenceFlow(process, source, target, name="", guard=""):
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
            parts.append(name[:14] + "=Y" + str(int(bounds["y"])))
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
            laneName = elementLayout.get(name, (0, "Intern"))[1]
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
    processName = "Internship_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - INTERNSHIP"
    print "=================================================================="
    print "Script Version: " + SCRIPT_VERSION
    print "Execution ID:   " + EXECUTION_ID
    print "Process Name:   " + processName
    print "=================================================================="

    # ------------------------------------------------------------------------
    # PHASE 1: CREATE PROCESS & LANES
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 1: CREATE PROCESS & LANES =============================="
    print ""

    process = modelingSession.getModel().createBpmnProcess()
    process.setName(processName)
    process.setOwner(parentPackage)
    print "[" + str(step()) + "] Process: " + processName

    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)

    internLane = createLane(laneSet, "Intern")
    companyLane = createLane(laneSet, "Company")
    twitterLane = createLane(laneSet, "Twitter")

    lanes = {
        "Intern": internLane,
        "Company": companyLane,
        "Twitter": twitterLane
    }
    laneOrder = ["Intern", "Company", "Twitter"]
    print "[" + str(step()) + "] Lanes: Intern, Company, Twitter"

    # ------------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # ------------------------------------------------------------------------
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
        if not ok:
            print "  WARNING: addToLane failed for: " + name + " -> " + lane.getName()
        return elem

    # Intern lane
    addElement(createStartEvent, "Start", internLane)
    addElement(createUserTask, "Enter Topic, Budget, Experience, Hobbies", internLane)
    addElement(createServiceTask, "Wait For Offers", internLane)
    addElement(createUserTask, "Review Offer", internLane)
    addElement(createExclusiveGateway, "Accept Offer?", internLane)
    addElement(createUserTask, "Accept Offer", internLane)
    addElement(createUserTask, "Deny Offer", internLane)
    addElement(createServiceTask, "Invalidate Other Offers", internLane)

    addElement(createParallelGateway, "Updates Split", internLane)
    addElement(createUserTask, "Intern Status Week 1", internLane)
    addElement(createUserTask, "Intern Status Week 2", internLane)
    addElement(createUserTask, "Intern Status Week 3", internLane)
    addElement(createParallelGateway, "Updates Join", internLane)

    addElement(createManualTask, "Complete Internship", internLane)
    addElement(createUserTask, "Recommend Company", internLane)

    # Company lane
    addElement(createUserTask, "Prepare Internship", companyLane)
    addElement(createUserTask, "Company Status 1", companyLane)
    addElement(createUserTask, "Company Status 2", companyLane)
    addElement(createUserTask, "Company Status 3", companyLane)

    # Twitter lane (parallel tweets)
    addElement(createParallelGateway, "Tweets Split", twitterLane)
    addElement(createServiceTask, "Tweet Friend A", twitterLane)
    addElement(createServiceTask, "Tweet Friend B", twitterLane)
    addElement(createServiceTask, "Tweet Friend C", twitterLane)
    addElement(createParallelGateway, "Tweets Join", twitterLane)
    addElement(createMessageEndEvent, "Tweets Sent", twitterLane)

    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # ------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------
    # PHASE 4: WAIT FOR AUTO-UNMASK
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout definition: element name -> (column_index, lane_name)
    elementLayout = {
        # Intern (offer loop)
        "Start": (0, "Intern"),
        "Enter Topic, Budget, Experience, Hobbies": (1, "Intern"),
        "Wait For Offers": (2, "Intern"),
        "Review Offer": (3, "Intern"),
        "Accept Offer?": (4, "Intern"),
        "Deny Offer": (5, "Intern"),
        "Accept Offer": (5, "Intern"),
        "Invalidate Other Offers": (6, "Intern"),

        # Company setup
        "Prepare Internship": (7, "Company"),

        # Status updates split/join
        "Updates Split": (8, "Intern"),
        "Intern Status Week 1": (9, "Intern"),
        "Intern Status Week 2": (10, "Intern"),
        "Intern Status Week 3": (11, "Intern"),
        "Company Status 1": (9, "Company"),
        "Company Status 2": (10, "Company"),
        "Company Status 3": (11, "Company"),
        "Updates Join": (12, "Intern"),

        # Finish + recommend
        "Complete Internship": (13, "Intern"),
        "Recommend Company": (14, "Intern"),

        # Tweets
        "Tweets Split": (15, "Twitter"),
        "Tweet Friend A": (16, "Twitter"),
        "Tweet Friend B": (17, "Twitter"),
        "Tweet Friend C": (18, "Twitter"),
        "Tweets Join": (19, "Twitter"),
        "Tweets Sent": (20, "Twitter"),
    }

    # IMPORTANT: also wait for lanes (we need their bounds for Y placement)
    allWaitObjects = []
    for laneName in laneOrder:
        allWaitObjects.append(lanes[laneName])
    for e in elements:
        allWaitObjects.append(e)

    print "[" + str(step()) + "] Waiting for lanes + elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    graphicsMap, attempts = waitForElements(diagramHandle, allWaitObjects)
    totalWaitTime = attempts * WAIT_TIME_MS

    foundCount = len(graphicsMap)
    totalCount = len(allWaitObjects)

    if foundCount == totalCount:
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + "/" + str(totalCount) + " objects ready in " + str(totalWaitTime) + "ms"
    else:
        print ""
        print "[" + str(step()) + "] WARNING: Only " + str(foundCount) + "/" + str(totalCount) + " objects ready after " + str(totalWaitTime) + "ms"

    # Build elementGraphics (only for BPMN elements, not lanes)
    elementGraphics = {}
    for elem in elements:
        name = elem.getName()
        dg = getGraphics(diagramHandle, elem)
        if dg:
            elementGraphics[name] = dg

    if len(elementGraphics) != len(elements):
        missing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] Missing element graphics after wait: " + ", ".join(missing)
        print "[" + str(step()) + "] Trying manual unmask for missing elements (inside correct lane Y)..."
        print ""

        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
        print ""
        print "[" + str(step()) + "] Manual unmask done. Newly unmasked: " + str(unmaskedCount)

        stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        if stillMissing:
            print "[" + str(step()) + "] STILL MISSING: " + ", ".join(stillMissing)
        else:
            print "[" + str(step()) + "] All elements now available"

    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    print "  " + formatElementsSummary(diagramHandle, elements, elementLayout)

    # ------------------------------------------------------------------------
    # PHASE 5: REPOSITION ELEMENTS
    # ------------------------------------------------------------------------
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
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedElements:
        if name not in elementRefs:
            print "[" + str(step()) + "] SKIP " + name + ": not found in elementRefs"
            continue

        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram graphics"
            continue

        elem = elementRefs[name]
        dg = elementGraphics[name]

        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)

        elemClass = elem.getMClass().getName()
        width = bounds["w"]
        height = bounds["h"]
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT

        newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
        dg.setBounds(newBounds)
        diagramHandle.save()
        repositionedCount += 1

        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""

        print "[" + str(step()) + "] " + laneName + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged

        if laneChanged:
            print "         Before: " + previousLanes
            print "         After:  " + currentLanes

        previousLanes = currentLanes

    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Start", "Enter Topic, Budget, Experience, Hobbies", ""),
        ("Enter Topic, Budget, Experience, Hobbies", "Wait For Offers", ""),
        ("Wait For Offers", "Review Offer", ""),
        ("Review Offer", "Accept Offer?", ""),

        # Gateway with GUARDS (important)
        ("Accept Offer?", "Accept Offer", "Accept"),
        ("Accept Offer?", "Deny Offer", "Deny"),

        # Deny loop (offers can arrive at arbitrary times -> keep waiting)
        ("Deny Offer", "Wait For Offers", ""),

        # Accept path -> invalidate others
        ("Accept Offer", "Invalidate Other Offers", ""),

        # Continue to company preparation then run internship
        ("Invalidate Other Offers", "Prepare Internship", ""),
        ("Prepare Internship", "Updates Split", ""),

        # Parallel updates: Intern branch
        ("Updates Split", "Intern Status Week 1", ""),
        ("Intern Status Week 1", "Intern Status Week 2", ""),
        ("Intern Status Week 2", "Intern Status Week 3", ""),
        ("Intern Status Week 3", "Updates Join", ""),

        # Parallel updates: Company branch
        ("Updates Split", "Company Status 1", ""),
        ("Company Status 1", "Company Status 2", ""),
        ("Company Status 2", "Company Status 3", ""),
        ("Company Status 3", "Updates Join", ""),

        # Finish internship, then recommend
        ("Updates Join", "Complete Internship", ""),
        ("Complete Internship", "Recommend Company", ""),

        # Tweets in parallel
        ("Recommend Company", "Tweets Split", ""),
        ("Tweets Split", "Tweet Friend A", ""),
        ("Tweets Split", "Tweet Friend B", ""),
        ("Tweets Split", "Tweet Friend C", ""),
        ("Tweet Friend A", "Tweets Join", ""),
        ("Tweet Friend B", "Tweets Join", ""),
        ("Tweet Friend C", "Tweets Join", ""),
        ("Tweets Join", "Tweets Sent", ""),
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

    # ------------------------------------------------------------------------
    # FINAL STATE
    # ------------------------------------------------------------------------
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
    print "Elements: " + str(len(elements)) + " (" + str(len(elementGraphics)) + " in diagram)"
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
