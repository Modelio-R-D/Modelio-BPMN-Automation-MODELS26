#
# TravelTicketBookingProcess.py
#
# Description:
#   BPMN process diagram for travel ticket booking (flight/train/bus).
#   Lanes: Customer, Booking System, Travel Company
#
# Applicable on: Package
#
# Version: v9.1 - March 2026
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
SPACING = 160
START_X = 80

# Task dimensions
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
        try:
            flow.setConditionExpression(guard)
        except Exception as e:
            print "  [Flow Guard] WARNING: Could not set guard '" + guard + "': " + str(e)
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
    except Exception as e:
        # Keep verbose logging: Modelio API can throw in early timing windows
        print "  [getGraphics] ERROR for element '" + element.getName() + "': " + str(e)
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
            shortName = name[:12]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
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

    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
            print "  [LaneY] " + laneName + " centerY=" + str(centerY)
        else:
            print "  [LaneY] WARNING: No bounds for lane " + laneName

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Customer"))[1]
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

def createTravelTicketBookingProcess(parentPackage):
    processName = "TravelTicketBooking_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN TRAVEL TICKET BOOKING - DEBUG LOG"
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

    customerLane = createLane(laneSet, "Customer")
    bookingLane = createLane(laneSet, "Booking System")
    travelLane = createLane(laneSet, "Travel Company")

    lanes = {
        "Customer": customerLane,
        "Booking System": bookingLane,
        "Travel Company": travelLane
    }
    laneOrder = ["Customer", "Booking System", "Travel Company"]

    print "[" + str(step()) + "] Lanes: Customer, Booking System, Travel Company"

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
        print "  [Element] " + name + " | Lane=" + lane.getName() + " | addToLane=" + str(ok)
        return elem

    print "[" + str(step()) + "] Creating elements..."

    # Customer
    addElement(createStartEvent, "Search Ticket", customerLane)
    addElement(createUserTask, "Select Route Date Time", customerLane)
    addElement(createUserTask, "Provide Personal Info", customerLane)
    addElement(createUserTask, "Provide Payment Details", customerLane)
    addElement(createManualTask, "Check In Or Board", customerLane)
    addElement(createUserTask, "Confirm Journey Completed", customerLane)
    addElement(createUserTask, "Provide Feedback", customerLane)
    addElement(createEndEvent, "Process Complete", customerLane)

    # Booking System
    addElement(createServiceTask, "Retrieve Options", bookingLane)
    addElement(createServiceTask, "Process Payment", bookingLane)
    addElement(createServiceTask, "Generate Ticket", bookingLane)
    addElement(createExclusiveGateway, "Send Ticket Via?", bookingLane)
    addElement(createServiceTask, "Send Ticket Email", bookingLane)
    addElement(createServiceTask, "Send Ticket SMS", bookingLane)
    addElement(createExclusiveGateway, "Ticket Sent Merge", bookingLane)
    addElement(createParallelGateway, "Post Ticket Split", bookingLane)
    addElement(createParallelGateway, "Post Ticket Join", bookingLane)
    addElement(createServiceTask, "Send Pre Travel Reminder", bookingLane)
    addElement(createExclusiveGateway, "Request Post Travel Service?", bookingLane)
    addElement(createServiceTask, "Send Thank You Or Offer", bookingLane)
    addElement(createExclusiveGateway, "Post Travel Merge", bookingLane)

    # Travel Company
    addElement(createServiceTask, "Update Seat Inventory", travelLane)
    addElement(createManualTask, "Deliver Journey Service", travelLane)
    addElement(createUserTask, "Handle Feedback Or Support", travelLane)

    print "[" + str(step()) + "] Total elements: " + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 3: CREATE DIAGRAM (AUTO-UNMASK TRIGGER)
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
    # PHASE 4: WAIT FOR AUTO-UNMASK (+ MANUAL UNMASK FALLBACK)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    # element name -> (column, laneName)
    elementLayout = {
        # Customer
        "Search Ticket": (0, "Customer"),
        "Select Route Date Time": (2, "Customer"),
        "Provide Personal Info": (3, "Customer"),
        "Provide Payment Details": (4, "Customer"),
        "Check In Or Board": (10, "Customer"),
        "Confirm Journey Completed": (12, "Customer"),
        "Provide Feedback": (14, "Customer"),
        "Process Complete": (16, "Customer"),

        # Booking System
        "Retrieve Options": (1, "Booking System"),
        "Process Payment": (5, "Booking System"),
        "Generate Ticket": (6, "Booking System"),
        "Post Ticket Split": (7, "Booking System"),
        "Send Ticket Via?": (8, "Booking System"),
        "Send Ticket Email": (9, "Booking System"),
        "Send Ticket SMS": (9, "Booking System"),
        "Ticket Sent Merge": (10, "Booking System"),
        "Update Seat Inventory": (9, "Travel Company"),
        "Post Ticket Join": (11, "Booking System"),
        "Send Pre Travel Reminder": (12, "Booking System"),
        "Request Post Travel Service?": (13, "Booking System"),
        "Send Thank You Or Offer": (15, "Booking System"),
        "Post Travel Merge": (16, "Booking System"),

        # Travel Company
        "Deliver Journey Service": (11, "Travel Company"),
        "Handle Feedback Or Support": (15, "Travel Company"),
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

    # ------------------------------------------------------------------------
    # PHASE 5: REPOSITION ELEMENTS
    # ------------------------------------------------------------------------
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
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available"

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
        if not elem:
            print "[" + str(step()) + "] SKIP " + name + ": element ref missing"
            continue

        dg = elementGraphics[name]
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

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (GUARDS FOR GATEWAYS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        # Search and selection
        ("Search Ticket", "Retrieve Options", ""),
        ("Retrieve Options", "Select Route Date Time", ""),
        ("Select Route Date Time", "Provide Personal Info", ""),
        ("Provide Personal Info", "Provide Payment Details", ""),
        ("Provide Payment Details", "Process Payment", ""),
        ("Process Payment", "Generate Ticket", ""),

        # After ticket generation: split parallel - send ticket and update inventory
        ("Generate Ticket", "Post Ticket Split", ""),
        ("Post Ticket Split", "Send Ticket Via?", ""),
        ("Post Ticket Split", "Update Seat Inventory", ""),

        # Channel decision (guards)
        ("Send Ticket Via?", "Send Ticket Email", "Email"),
        ("Send Ticket Via?", "Send Ticket SMS", "SMS"),

        # Merge of channel
        ("Send Ticket Email", "Ticket Sent Merge", ""),
        ("Send Ticket SMS", "Ticket Sent Merge", ""),

        # Join after parallel work finished
        ("Ticket Sent Merge", "Post Ticket Join", ""),
        ("Update Seat Inventory", "Post Ticket Join", ""),

        # Reminders and boarding
        ("Post Ticket Join", "Send Pre Travel Reminder", ""),
        ("Send Pre Travel Reminder", "Check In Or Board", ""),
        ("Check In Or Board", "Deliver Journey Service", ""),
        ("Deliver Journey Service", "Confirm Journey Completed", ""),

        # Post travel optional services
        ("Confirm Journey Completed", "Request Post Travel Service?", ""),
        ("Request Post Travel Service?", "Send Thank You Or Offer", "Yes"),
        ("Request Post Travel Service?", "Post Travel Merge", "No"),
        ("Send Thank You Or Offer", "Post Travel Merge", ""),

        # Optional feedback
        ("Post Travel Merge", "Provide Feedback", "If Requested"),
        ("Provide Feedback", "Handle Feedback Or Support", ""),
        ("Handle Feedback Or Support", "Process Complete", ""),
    ]

    flows = []
    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = createSequenceFlow(process, src, tgt, guard=guard)
            flows.append(flow)
            if guard:
                print "  [Flow] " + srcName + " -> " + tgtName + " | Guard=" + guard
            else:
                print "  [Flow] " + srcName + " -> " + tgtName
        else:
            print "  [Flow] WARNING: Missing element for flow " + srcName + " -> " + tgtName

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
        createTravelTicketBookingProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
