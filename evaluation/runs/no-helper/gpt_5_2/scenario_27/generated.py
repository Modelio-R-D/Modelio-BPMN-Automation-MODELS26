#
# WorkAccident.py
#
# Description:
#   BPMN process diagram "Work Accident" for gathering information about work accidents
#   and near-miss incidents, and triggering the main reporting obligations.
#
# Applicable on: Package
# Version: 9.1 (Modelio BPMN Macro - Jython / Python 2)
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

    # IMPORTANT: use condition expression (guard) for labels on gateway outflows
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
            laneName = elementLayout.get(name, (0, "Reporter"))[1]
            targetY = laneY.get(laneName, 100)

            try:
                # CRITICAL: unmask at Y inside the correct lane
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

def createWorkAccidentProcess(parentPackage):
    processName = "WorkAccident_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN DIAGRAM CREATION - DEBUG LOG"
    print "=================================================================="
    print "Title:         Work Accident"
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

    reporterLane = createLane(laneSet, "Reporter")
    employerLane = createLane(laneSet, "Employer or Institution")
    insuranceLane = createLane(laneSet, "Accident Insurance")
    inspectorateLane = createLane(laneSet, "Labour Inspectorate")
    otherBodiesLane = createLane(laneSet, "Other Bodies")

    lanes = {
        "Reporter": reporterLane,
        "Employer or Institution": employerLane,
        "Accident Insurance": insuranceLane,
        "Labour Inspectorate": inspectorateLane,
        "Other Bodies": otherBodiesLane
    }
    laneOrder = ["Reporter", "Employer or Institution", "Accident Insurance", "Labour Inspectorate", "Other Bodies"]

    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)

    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
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
        print "  [Add] " + laneName + " :: " + name + " (addToLane=" + str(ok) + ")"
        return elem

    # Reporter
    addElement(createStartEvent, "Incident Occurs", "Reporter")
    addElement(createManualTask, "Provide First Aid / Secure Area", "Reporter")
    addElement(createExclusiveGateway, "Emergency?", "Reporter")
    addElement(createManualTask, "Call Emergency Services", "Reporter")
    addElement(createUserTask, "Notify Employer Immediately", "Reporter")

    # Employer / Institution
    addElement(createUserTask, "Record Incident", "Employer or Institution")
    addElement(createUserTask, "Collect Facts and Evidence", "Employer or Institution")
    addElement(createExclusiveGateway, "Injury or Near Miss?", "Employer or Institution")

    # Near-miss branch
    addElement(createUserTask, "Log Near Miss / Safety Risk", "Employer or Institution")
    addElement(createUserTask, "Investigate and Corrective Actions", "Employer or Institution")
    addElement(createEndEvent, "Closed - Prevention Actions", "Employer or Institution")

    # Injury branch
    addElement(createExclusiveGateway, "Work Accident or Equivalent?", "Employer or Institution")
    addElement(createUserTask, "Handle as Non-Work Incident", "Employer or Institution")
    addElement(createEndEvent, "Closed - Not Work Accident", "Employer or Institution")

    addElement(createUserTask, "Determine Reporting Obligations", "Employer or Institution")
    addElement(createExclusiveGateway, "Fatal or Serious Injury?", "Employer or Institution")
    addElement(createServiceTask, "Report to Labour Inspectorate Immediately", "Labour Inspectorate")
    addElement(createExclusiveGateway, "Accident Insurance Report Needed?", "Employer or Institution")
    addElement(createServiceTask, "Submit Report to Accident Insurance (<=5 days)", "Accident Insurance")
    addElement(createUserTask, "Document No-Report Justification", "Employer or Institution")

    addElement(createExclusiveGateway, "Student/Schoolchild?", "Employer or Institution")
    addElement(createParallelGateway, "Student Reporting Split", "Employer or Institution")
    addElement(createServiceTask, "Report Accident to Directorate", "Other Bodies")
    addElement(createServiceTask, "School Sends Insurance Report (<=5 days)", "Employer or Institution")
    addElement(createParallelGateway, "Student Reporting Join", "Employer or Institution")

    addElement(createExclusiveGateway, "Private Insurance?", "Employer or Institution")
    addElement(createServiceTask, "Notify Private Insurer in Writing", "Other Bodies")

    addElement(createUserTask, "Confirm Reports Sent and Archive", "Employer or Institution")
    addElement(createEndEvent, "Case Closed", "Employer or Institution")

    print ""
    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # =========================================================================
    # PHASE 3: CREATE DIAGRAM (TRIGGERS AUTO-UNMASK)
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""

    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("Work Accident")
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram created: Work Accident"

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

    elementLayout = {
        # Reporter
        "Incident Occurs": (0, "Reporter"),
        "Provide First Aid / Secure Area": (1, "Reporter"),
        "Emergency?": (2, "Reporter"),
        "Call Emergency Services": (3, "Reporter"),
        "Notify Employer Immediately": (4, "Reporter"),

        # Employer / Institution (core)
        "Record Incident": (5, "Employer or Institution"),
        "Collect Facts and Evidence": (6, "Employer or Institution"),
        "Injury or Near Miss?": (7, "Employer or Institution"),

        # Near miss branch
        "Log Near Miss / Safety Risk": (8, "Employer or Institution"),
        "Investigate and Corrective Actions": (9, "Employer or Institution"),
        "Closed - Prevention Actions": (10, "Employer or Institution"),

        # Injury branch and reporting
        "Work Accident or Equivalent?": (10, "Employer or Institution"),
        "Handle as Non-Work Incident": (11, "Employer or Institution"),
        "Closed - Not Work Accident": (12, "Employer or Institution"),

        "Determine Reporting Obligations": (11, "Employer or Institution"),
        "Fatal or Serious Injury?": (12, "Employer or Institution"),
        "Report to Labour Inspectorate Immediately": (13, "Labour Inspectorate"),
        "Accident Insurance Report Needed?": (14, "Employer or Institution"),
        "Submit Report to Accident Insurance (<=5 days)": (15, "Accident Insurance"),
        "Document No-Report Justification": (15, "Employer or Institution"),

        "Student/Schoolchild?": (16, "Employer or Institution"),
        "Student Reporting Split": (17, "Employer or Institution"),
        "Report Accident to Directorate": (18, "Other Bodies"),
        "School Sends Insurance Report (<=5 days)": (18, "Employer or Institution"),
        "Student Reporting Join": (19, "Employer or Institution"),

        "Private Insurance?": (20, "Employer or Institution"),
        "Notify Private Insurer in Writing": (21, "Other Bodies"),

        "Confirm Reports Sent and Archive": (22, "Employer or Institution"),
        "Case Closed": (23, "Employer or Institution")
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

    for col, name, ln in sortedElements:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs[name]
        dg = elementGraphics[name]
        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(ln, 100)

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

        print "[" + str(step()) + "] " + ln + "/" + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ") " + str(int(width)) + "x" + str(int(height)) + laneChanged
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
        ("Incident Occurs", "Provide First Aid / Secure Area", ""),
        ("Provide First Aid / Secure Area", "Emergency?", ""),

        ("Emergency?", "Call Emergency Services", "Yes"),
        ("Emergency?", "Notify Employer Immediately", "No"),
        ("Call Emergency Services", "Notify Employer Immediately", ""),

        ("Notify Employer Immediately", "Record Incident", ""),
        ("Record Incident", "Collect Facts and Evidence", ""),
        ("Collect Facts and Evidence", "Injury or Near Miss?", ""),

        ("Injury or Near Miss?", "Log Near Miss / Safety Risk", "Near miss"),
        ("Log Near Miss / Safety Risk", "Investigate and Corrective Actions", ""),
        ("Investigate and Corrective Actions", "Closed - Prevention Actions", ""),

        ("Injury or Near Miss?", "Work Accident or Equivalent?", "Injury"),

        ("Work Accident or Equivalent?", "Handle as Non-Work Incident", "No"),
        ("Handle as Non-Work Incident", "Closed - Not Work Accident", ""),

        ("Work Accident or Equivalent?", "Determine Reporting Obligations", "Yes"),
        ("Determine Reporting Obligations", "Fatal or Serious Injury?", ""),

        ("Fatal or Serious Injury?", "Report to Labour Inspectorate Immediately", "Yes"),
        ("Fatal or Serious Injury?", "Accident Insurance Report Needed?", "No"),
        ("Report to Labour Inspectorate Immediately", "Accident Insurance Report Needed?", ""),

        ("Accident Insurance Report Needed?", "Submit Report to Accident Insurance (<=5 days)", "Yes"),
        ("Accident Insurance Report Needed?", "Document No-Report Justification", "No"),

        ("Submit Report to Accident Insurance (<=5 days)", "Student/Schoolchild?", ""),
        ("Document No-Report Justification", "Student/Schoolchild?", ""),

        ("Student/Schoolchild?", "Student Reporting Split", "Yes"),
        ("Student/Schoolchild?", "Private Insurance?", "No"),

        ("Student Reporting Split", "Report Accident to Directorate", ""),
        ("Student Reporting Split", "School Sends Insurance Report (<=5 days)", ""),

        ("Report Accident to Directorate", "Student Reporting Join", ""),
        ("School Sends Insurance Report (<=5 days)", "Student Reporting Join", ""),
        ("Student Reporting Join", "Private Insurance?", ""),

        ("Private Insurance?", "Notify Private Insurer in Writing", "Yes"),
        ("Private Insurance?", "Confirm Reports Sent and Archive", "No"),
        ("Notify Private Insurer in Writing", "Confirm Reports Sent and Archive", ""),

        ("Confirm Reports Sent and Archive", "Case Closed", "")
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
            print "  [Flow] " + srcName[:30] + " -> " + tgtName[:30] + (" [guard=" + guard + "]" if guard else "")
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
    print "Title:    Work Accident"
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
        createWorkAccidentProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
