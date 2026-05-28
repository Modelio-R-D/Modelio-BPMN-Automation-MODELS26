#
# EmployeeDevelopmentAndPromotionProcess.py
#
# Description:
#   BPMN process diagram for Employee Development Plan and Promotion workflow.
#   3 lanes: Employee, Manager, HR
#
# Applicable on: Package
#
# Version: v9.1 - March 2026
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

SCRIPT_VERSION = "v9.1"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 170
START_X = 80

# Task dimensions (keep consistent)
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
    except Exception as e:
        print "  [addToLane] ERROR: " + str(e)
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


def createServiceTask(process, name):
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createManualTask(process, name):
    task = modelingSession.getModel().createBpmnManualTask()
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

    # Guard text is what shows on gateway outflows in Modelio
    if guard:
        try:
            flow.setConditionExpression(guard)
        except Exception as e:
            print "  [Flow Guard] WARNING: Could not set guard='" + guard + "' -> " + str(e)

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
    except Exception as e:
        # Keep silent to avoid noise during polling
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
    sortable = []
    for elem in elements:
        name = elem.getName()
        col = elementLayout.get(name, (99, "?"))[0]
        sortable.append((col, name, elem))
    sortable.sort()

    for col, name, elem in sortable:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            parts.append(name[:10] + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:10] + "=--")
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
        else:
            print "  [Unmask] WARNING: Lane bounds missing for " + laneName

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Employee"))[1]
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

def createEmployeeDevelopmentAndPromotionProcess(parentPackage):

    processName = "EmployeeDevelopmentAndPromotion_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN EMPLOYEE DEVELOPMENT AND PROMOTION - DEBUG LOG"
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

    employeeLane = createLane(laneSet, "Employee")
    managerLane = createLane(laneSet, "Manager")
    hrLane = createLane(laneSet, "HR")

    lanes = {
        "Employee": employeeLane,
        "Manager": managerLane,
        "HR": hrLane
    }
    laneOrder = ["Employee", "Manager", "HR"]

    print "[" + str(step()) + "] Lanes: Employee, Manager, HR"

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
        ok = addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        print "  [Element] " + laneName + ": " + name + " | addToLane=" + str(ok)
        return elem

    # Employee
    addElement(createStartEvent, "Identify Development Needs", employeeLane, "Employee")
    addElement(createUserTask, "Share Career Aspirations", employeeLane, "Employee")

    # Manager and HR create plan (parallel work)
    addElement(createUserTask, "Review Needs and Aspirations", managerLane, "Manager")
    addElement(createParallelGateway, "Plan Work Split", managerLane, "Manager")
    addElement(createUserTask, "Define Mentorship and Responsibilities", managerLane, "Manager")
    addElement(createUserTask, "Arrange Training Programs", hrLane, "HR")
    addElement(createParallelGateway, "Plan Consolidated", managerLane, "Manager")

    # Continuous development and feedback
    addElement(createUserTask, "Work on Skill Enhancement", employeeLane, "Employee")
    addElement(createUserTask, "Provide Feedback and Evaluation", managerLane, "Manager")
    addElement(createExclusiveGateway, "Milestones Reached?", managerLane, "Manager")
    addElement(createUserTask, "Adjust Personal Development Plan", managerLane, "Manager")

    # Promotion consideration and formal HR review
    addElement(createUserTask, "Formal Performance Review", hrLane, "HR")
    addElement(createExclusiveGateway, "Promotion Approved?", hrLane, "HR")
    addElement(createUserTask, "Finalize Promotion and Compensation", hrLane, "HR")
    addElement(createEndEvent, "Promoted and Transitioned", employeeLane, "Employee")

    print ""
    print "[" + str(step()) + "] Total elements (flow nodes): " + str(len(elements))

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
    # PHASE 4: WAIT FOR AUTO-UNMASK (AND MANUAL UNMASK FALLBACK)
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # Layout: element name -> (column, laneName)
    elementLayout = {
        "Identify Development Needs": (0, "Employee"),
        "Share Career Aspirations": (1, "Employee"),

        "Review Needs and Aspirations": (2, "Manager"),
        "Plan Work Split": (3, "Manager"),
        "Define Mentorship and Responsibilities": (4, "Manager"),
        "Arrange Training Programs": (4, "HR"),
        "Plan Consolidated": (5, "Manager"),

        "Work on Skill Enhancement": (6, "Employee"),
        "Provide Feedback and Evaluation": (7, "Manager"),
        "Milestones Reached?": (8, "Manager"),
        "Adjust Personal Development Plan": (9, "Manager"),

        "Formal Performance Review": (10, "HR"),
        "Promotion Approved?": (11, "HR"),
        "Finalize Promotion and Compensation": (12, "HR"),
        "Promoted and Transitioned": (13, "Employee"),
    }

    # Also wait for lanes (needed for lane bounds)
    allWait = elements + [employeeLane, managerLane, hrLane]

    print "[" + str(step()) + "] Waiting for elements and lanes (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""

    elementGraphics, attempts = waitForElements(diagramHandle, allWait)
    totalWaitTime = attempts * WAIT_TIME_MS

    foundCount = len(elementGraphics)
    neededCount = len(allWait)

    if foundCount == neededCount:
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " graphics ready in " + str(totalWaitTime) + "ms"
    else:
        missing = [e.getName() for e in allWait if e.getName() not in elementGraphics]
        print ""
        print "[" + str(step()) + "] WARNING: " + str(foundCount) + "/" + str(neededCount) + " graphics ready after " + str(totalWaitTime) + "ms"
        print "         Missing: " + ", ".join(missing)

        # Manual unmask only for flow nodes (not lanes)
        print ""
        print "[" + str(step()) + "] Trying manual unmask for missing flow nodes..."
        print ""
        unmaskedCount = unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)

        if unmaskedCount > 0:
            diagramHandle.save()
            print ""
            print "[" + str(step()) + "] Manual unmask: " + str(unmaskedCount) + " elements unmasked"

        # Re-check summary
        stillMissing = [e.getName() for e in elements if e.getName() not in elementGraphics]
        if len(stillMissing) == 0:
            print "[" + str(step()) + "] All flow nodes now available"
        else:
            print "[" + str(step()) + "] Still missing flow nodes: " + ", ".join(stillMissing)

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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available (centerY)"

    # Sort by column for left-to-right placement
    sortedElements = []
    for name, (col, laneName) in elementLayout.items():
        sortedElements.append((col, name, laneName))
    sortedElements.sort()

    print ""
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    repositionedCount = 0

    for col, name, laneName in sortedElements:
        if name not in elementRefs:
            print "[" + str(step()) + "] SKIP " + name + ": not found in elementRefs"
            continue
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram (no graphics)"
            continue

        elem = elementRefs[name]
        dg = elementGraphics[name]
        oldBounds = getBounds(diagramHandle, elem)
        if not oldBounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)

        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = oldBounds["w"]
            height = oldBounds["h"]

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
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elementLayout))

    # =========================================================================
    # PHASE 6: CREATE FLOWS (WITH GUARDS FROM GATEWAYS)
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Identify needs -> share aspirations -> manager review
        ("Identify Development Needs", "Share Career Aspirations", ""),
        ("Share Career Aspirations", "Review Needs and Aspirations", ""),

        # Split planning work in parallel
        ("Review Needs and Aspirations", "Plan Work Split", ""),
        ("Plan Work Split", "Define Mentorship and Responsibilities", ""),
        ("Plan Work Split", "Arrange Training Programs", ""),

        # Join
        ("Define Mentorship and Responsibilities", "Plan Consolidated", ""),
        ("Arrange Training Programs", "Plan Consolidated", ""),

        # Execute plan and feedback loop
        ("Plan Consolidated", "Work on Skill Enhancement", ""),
        ("Work on Skill Enhancement", "Provide Feedback and Evaluation", ""),
        ("Provide Feedback and Evaluation", "Milestones Reached?", ""),

        # Gateway: milestones reached?
        ("Milestones Reached?", "Formal Performance Review", "Yes"),
        ("Milestones Reached?", "Adjust Personal Development Plan", "No"),

        # Adjust plan and continue development
        ("Adjust Personal Development Plan", "Work on Skill Enhancement", ""),

        # HR review and approval decision
        ("Formal Performance Review", "Promotion Approved?", ""),
        ("Promotion Approved?", "Finalize Promotion and Compensation", "Approved"),
        ("Promotion Approved?", "Adjust Personal Development Plan", "Not Approved"),

        # End
        ("Finalize Promotion and Compensation", "Promoted and Transitioned", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18] + " | guard=" + guard
            else:
                print "  [Flow] " + srcName[:18] + " -> " + tgtName[:18]
        else:
            print "  [Flow] WARNING: Missing element for flow " + srcName + " -> " + tgtName

    print ""
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

    print ""
    print "=================================================================="
    print "COMPLETE"
    print "=================================================================="
    print "Process:  " + processName
    print "Lanes:    " + str(len(lanes))
    print "Elements: " + str(len(elements))
    print "Flows:    " + str(len(flows))
    print "=================================================================="

    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createEmployeeDevelopmentAndPromotionProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
