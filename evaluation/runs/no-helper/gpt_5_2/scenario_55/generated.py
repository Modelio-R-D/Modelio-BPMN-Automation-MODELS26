#
# UltrasoundGuidedCatheterPlacement.py
#
# Description:
#   BPMN process diagram for an ultrasound guided puncture and catheter placement workflow.
#   Single lane: Doctor
#
# Applicable on: Package
#
# Version: 9.1 - March 2026
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

# Waiting configuration (auto-unmask)
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 6

# Layout configuration
SPACING = 150
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
    gw = modelingSession.getModel().createBpmnExclusiveGateway()
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
        # IMPORTANT: use condition expression so the label appears on gateway outflows
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

    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY

    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, "Doctor"))[1]
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

def createUltrasoundGuidedCatheterProcess(parentPackage):
    processName = "US_Guided_Catheter_" + EXECUTION_ID
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    print ""
    print "=================================================================="
    print "BPMN ULTRASOUND GUIDED CATHETER PLACEMENT - DEBUG LOG"
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

    doctorLane = createLane(laneSet, "Doctor")
    lanes = {"Doctor": doctorLane}
    laneOrder = ["Doctor"]

    print "[" + str(step()) + "] Lanes: Doctor"

    # ------------------------------------------------------------------------
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""

    elements = []
    elementRefs = {}

    def addElement(creator, name, laneObj):
        elem = creator(process, name)
        ok = addToLane(elem, laneObj)
        elements.append(elem)
        elementRefs[name] = elem
        print "  [Element] " + name + " | addToLane=" + ("OK" if ok else "FAILED")
        return elem

    # Start and preparation
    addElement(createStartEvent, "Start Procedure", doctorLane)
    addElement(createManualTask, "Prepare Implements", doctorLane)
    addElement(createManualTask, "Wash Hands", doctorLane)
    addElement(createManualTask, "Don Sterile Clothes", doctorLane)

    addElement(createManualTask, "Clean Puncture Area", doctorLane)
    addElement(createManualTask, "Drape Puncture Zone", doctorLane)

    addElement(createUserTask, "Configure Ultrasound", doctorLane)
    addElement(createManualTask, "Apply Gel to Probe", doctorLane)
    addElement(createManualTask, "Cover Probe", doctorLane)
    addElement(createManualTask, "Apply Sterile Gel", doctorLane)

    addElement(createManualTask, "Position Probe", doctorLane)
    addElement(createManualTask, "Position Patient", doctorLane)

    # Vein identification alternatives
    addElement(createExclusiveGateway, "Vein Identification Method?", doctorLane)
    addElement(createUserTask, "Anatomic Identification", doctorLane)
    addElement(createUserTask, "Doppler Identification", doctorLane)
    addElement(createUserTask, "Compression Identification", doctorLane)
    addElement(createExclusiveGateway, "Vein Identified (Merge)", doctorLane)

    # Puncture and blood return loop
    addElement(createManualTask, "Anesthetize Patient", doctorLane)
    addElement(createManualTask, "Puncture", doctorLane)
    addElement(createUserTask, "Check Blood Return", doctorLane)
    addElement(createExclusiveGateway, "Blood Return Correct?", doctorLane)

    addElement(createManualTask, "Drop Probe", doctorLane)
    addElement(createManualTask, "Remove Syringe", doctorLane)
    addElement(createManualTask, "Install Guidewire", doctorLane)
    addElement(createManualTask, "Remove Trocar", doctorLane)

    # Wire check alternatives + decision
    addElement(createExclusiveGateway, "Wire Check Axis?", doctorLane)
    addElement(createUserTask, "Check Wire Long Axis", doctorLane)
    addElement(createUserTask, "Check Wire Short Axis", doctorLane)
    addElement(createExclusiveGateway, "Wire Checked (Merge)", doctorLane)

    addElement(createExclusiveGateway, "Wire in Good Position?", doctorLane)

    # Finish
    addElement(createManualTask, "Widen Pathway", doctorLane)
    addElement(createManualTask, "Advance Catheter", doctorLane)
    addElement(createManualTask, "Remove Guidewire", doctorLane)

    addElement(createUserTask, "Verify Flow and Reflow", doctorLane)
    addElement(createUserTask, "Check Catheter Position", doctorLane)

    addElement(createEndEvent, "End Procedure", doctorLane)

    print ""
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
    # PHASE 4: WAIT FOR AUTO-UNMASK (+ MANUAL UNMASK FALLBACK)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""

    elementLayout = {
        "Start Procedure": (0, "Doctor"),
        "Prepare Implements": (1, "Doctor"),
        "Wash Hands": (2, "Doctor"),
        "Don Sterile Clothes": (3, "Doctor"),
        "Clean Puncture Area": (4, "Doctor"),
        "Drape Puncture Zone": (5, "Doctor"),
        "Configure Ultrasound": (6, "Doctor"),
        "Apply Gel to Probe": (7, "Doctor"),
        "Cover Probe": (8, "Doctor"),
        "Apply Sterile Gel": (9, "Doctor"),
        "Position Probe": (10, "Doctor"),
        "Position Patient": (11, "Doctor"),
        "Vein Identification Method?": (12, "Doctor"),
        "Anatomic Identification": (13, "Doctor"),
        "Doppler Identification": (14, "Doctor"),
        "Compression Identification": (15, "Doctor"),
        "Vein Identified (Merge)": (16, "Doctor"),
        "Anesthetize Patient": (17, "Doctor"),
        "Puncture": (18, "Doctor"),
        "Check Blood Return": (19, "Doctor"),
        "Blood Return Correct?": (20, "Doctor"),
        "Drop Probe": (21, "Doctor"),
        "Remove Syringe": (22, "Doctor"),
        "Install Guidewire": (23, "Doctor"),
        "Remove Trocar": (24, "Doctor"),
        "Wire Check Axis?": (25, "Doctor"),
        "Check Wire Long Axis": (26, "Doctor"),
        "Check Wire Short Axis": (27, "Doctor"),
        "Wire Checked (Merge)": (28, "Doctor"),
        "Wire in Good Position?": (29, "Doctor"),
        "Widen Pathway": (30, "Doctor"),
        "Advance Catheter": (31, "Doctor"),
        "Remove Guidewire": (32, "Doctor"),
        "Verify Flow and Reflow": (33, "Doctor"),
        "Check Catheter Position": (34, "Doctor"),
        "End Procedure": (35, "Doctor"),
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
        else:
            print ""
            print "[" + str(step()) + "] Manual unmask: 0 elements unmasked"

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
        y = getLaneCenterY(diagramHandle, lanes[laneName])
        if y is not None:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
        else:
            print "[" + str(step()) + "] WARNING: " + laneName + " bounds not available; using default Y=100"
            laneY[laneName] = 100

    print ""

    # sort by column for clean left-to-right reposition logging
    sortedItems = []
    for name, (col, laneName) in elementLayout.items():
        sortedItems.append((col, name, laneName))
    sortedItems.sort()

    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)

    for col, name, laneName in sortedItems:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue

        elem = elementRefs.get(name)
        dg = elementGraphics.get(name)
        if elem is None or dg is None:
            print "[" + str(step()) + "] SKIP " + name + ": missing refs"
            continue

        bounds = getBounds(diagramHandle, elem)
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue

        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100)

        elemClass = elem.getMClass().getName()

        # fixed size for tasks to keep text readable
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]

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
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))

    # ------------------------------------------------------------------------
    # PHASE 6: CREATE FLOWS (GUARDS ON GATEWAY OUTFLOWS)
    # ------------------------------------------------------------------------
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""

    flowDefs = [
        ("Start Procedure", "Prepare Implements", ""),
        ("Prepare Implements", "Wash Hands", ""),
        ("Wash Hands", "Don Sterile Clothes", ""),
        ("Don Sterile Clothes", "Clean Puncture Area", ""),
        ("Clean Puncture Area", "Drape Puncture Zone", ""),
        ("Drape Puncture Zone", "Configure Ultrasound", ""),
        ("Configure Ultrasound", "Apply Gel to Probe", ""),
        ("Apply Gel to Probe", "Cover Probe", ""),
        ("Cover Probe", "Apply Sterile Gel", ""),
        ("Apply Sterile Gel", "Position Probe", ""),
        ("Position Probe", "Position Patient", ""),
        ("Position Patient", "Vein Identification Method?", ""),

        # Identification options (guards)
        ("Vein Identification Method?", "Anatomic Identification", "Anatomic"),
        ("Vein Identification Method?", "Doppler Identification", "Doppler"),
        ("Vein Identification Method?", "Compression Identification", "Compression"),

        # Merge
        ("Anatomic Identification", "Vein Identified (Merge)", ""),
        ("Doppler Identification", "Vein Identified (Merge)", ""),
        ("Compression Identification", "Vein Identified (Merge)", ""),

        ("Vein Identified (Merge)", "Anesthetize Patient", ""),
        ("Anesthetize Patient", "Puncture", ""),
        ("Puncture", "Check Blood Return", ""),
        ("Check Blood Return", "Blood Return Correct?", ""),

        # Blood return decision (guards + loop)
        ("Blood Return Correct?", "Puncture", "No"),
        ("Blood Return Correct?", "Drop Probe", "Yes"),

        ("Drop Probe", "Remove Syringe", ""),
        ("Remove Syringe", "Install Guidewire", ""),
        ("Install Guidewire", "Remove Trocar", ""),
        ("Remove Trocar", "Wire Check Axis?", ""),

        # Wire check options (guards)
        ("Wire Check Axis?", "Check Wire Long Axis", "Long axis"),
        ("Wire Check Axis?", "Check Wire Short Axis", "Short axis"),

        # Merge
        ("Check Wire Long Axis", "Wire Checked (Merge)", ""),
        ("Check Wire Short Axis", "Wire Checked (Merge)", ""),

        ("Wire Checked (Merge)", "Wire in Good Position?", ""),

        # Wire position decision (guards + loop)
        ("Wire in Good Position?", "Puncture", "No"),
        ("Wire in Good Position?", "Widen Pathway", "Yes"),

        ("Widen Pathway", "Advance Catheter", ""),
        ("Advance Catheter", "Remove Guidewire", ""),
        ("Remove Guidewire", "Verify Flow and Reflow", ""),
        ("Verify Flow and Reflow", "Check Catheter Position", ""),
        ("Check Catheter Position", "End Procedure", ""),
    ]

    flows = []
    missingFlowRefs = 0

    for srcName, tgtName, guard in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flows.append(createSequenceFlow(process, src, tgt, guard=guard))
            print "  [Flow] " + srcName[:28] + " -> " + tgtName[:28] + (" | guard=" + guard if guard else "")
        else:
            missingFlowRefs += 1
            print "  [Flow] WARNING: Missing element for flow " + srcName + " -> " + tgtName

    diagramHandle.save()
    print ""
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows (" + str(missingFlowRefs) + " missing refs)"
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
        createUltrasoundGuidedCatheterProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
