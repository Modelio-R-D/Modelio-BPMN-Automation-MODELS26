#
# CentralVenousCatheterInsertion.py
#
# Description:
#   BPMN process diagram for Central Venous Catheter (CVC) insertion procedure.
#   Single lane: Doctor
#   Includes parallel preparations, alternative identification methods,
#   and verification loops for blood return and wire position.
#
# Applicable on: Package
#
# Version: 1.0 - December 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
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
MAX_ATTEMPTS = 5

# Layout configuration
SPACING_X = 140
SPACING_Y = 100
START_X = 60

# Task dimensions
TASK_WIDTH = 110
TASK_HEIGHT = 55
GATEWAY_SIZE = 40
EVENT_SIZE = 30


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
    """Create a BPMN Start Event."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createEndEvent(process, name):
    """Create a BPMN End Event."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createManualTask(process, name):
    """Create a BPMN Manual Task (physical task without IT)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createUserTask(process, name):
    """Create a BPMN User Task."""
    task = modelingSession.getModel().createBpmnUserTask()
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
    """Get the bounds of an element in the diagram."""
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None


def getLaneCenterY(diagramHandle, lane):
    """Calculate the center Y position for a lane."""
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format a compact summary of all lanes."""
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
            missing = [e.getName()[:15] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + str(len(missing))
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """Manually unmask elements that were not auto-unmasked."""
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
            laneName = elementLayout.get(name, (0, 0, "Doctor"))[2]
            targetY = laneY.get(laneName, 100)
            
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
                    print "  [Unmask] " + name[:20] + " -> OK"
            except Exception as e:
                print "  [Unmask] " + name[:20] + ": ERROR"
    
    return unmaskedCount


# ============================================================================
# MAIN PROCESS CREATION
# ============================================================================

def createCVCInsertionProcess(parentPackage):
    """Create the CVC Insertion BPMN process with diagram."""
    
    processName = "CVC_Insertion_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN CVC INSERTION PROCESS"
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
    
    # Single lane for the Doctor
    doctorLane = createLane(laneSet, "Doctor")
    
    lanes = {"Doctor": doctorLane}
    laneOrder = ["Doctor"]
    
    print "[" + str(step()) + "] Lane: Doctor"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    
    def addElement(creator, name):
        elem = creator(process, name)
        addToLane(elem, doctorLane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Start Event ---
    addElement(createStartEvent, "Start")
    
    # --- Initial Preparation (Parallel) ---
    addElement(createParallelGateway, "Prep Split")
    addElement(createManualTask, "Prepare Implements")
    addElement(createManualTask, "Wash Hands")
    addElement(createManualTask, "Get Sterile Clothes")
    addElement(createParallelGateway, "Prep Join")
    
    # --- Puncture Area Preparation ---
    addElement(createManualTask, "Clean Puncture Area")
    addElement(createManualTask, "Drape Puncture Zone")
    
    # --- Ultrasound Configuration (Parallel) ---
    addElement(createParallelGateway, "US Split")
    addElement(createManualTask, "Configure Ultrasound")
    addElement(createManualTask, "Put Gel on Probe")
    addElement(createParallelGateway, "US Join")
    
    # --- Probe Preparation ---
    addElement(createManualTask, "Cover Probe")
    addElement(createManualTask, "Put Sterile Gel")
    
    # --- Positioning (Parallel) ---
    addElement(createParallelGateway, "Pos Split")
    addElement(createManualTask, "Position Probe")
    addElement(createManualTask, "Position Patient")
    addElement(createParallelGateway, "Pos Join")
    
    # --- Vein Identification (Exclusive - one of three) ---
    addElement(createExclusiveGateway, "ID Split")
    addElement(createManualTask, "Anatomic ID")
    addElement(createManualTask, "Doppler ID")
    addElement(createManualTask, "Compression ID")
    addElement(createExclusiveGateway, "ID Join")
    
    # --- Puncture Sequence ---
    addElement(createManualTask, "Anesthetize")
    addElement(createManualTask, "Puncture")
    addElement(createManualTask, "Check Blood Return")
    
    # --- Blood Return Decision ---
    addElement(createExclusiveGateway, "Blood Return OK?")
    
    # --- Post-Puncture (if blood return OK) ---
    addElement(createManualTask, "Drop Probe")
    addElement(createManualTask, "Remove Syringe")
    addElement(createManualTask, "Install Guidewire")
    addElement(createManualTask, "Remove Trocar")
    
    # --- Wire Check (Exclusive - one of two) ---
    addElement(createExclusiveGateway, "Wire Check Split")
    addElement(createManualTask, "Check Wire Long Axis")
    addElement(createManualTask, "Check Wire Short Axis")
    addElement(createExclusiveGateway, "Wire Check Join")
    
    # --- Wire Position Decision ---
    addElement(createExclusiveGateway, "Wire Position OK?")
    
    # --- Catheter Installation ---
    addElement(createManualTask, "Widen Pathway")
    addElement(createManualTask, "Advance Catheter")
    addElement(createManualTask, "Remove Guidewire")
    
    # --- Final Verification ---
    addElement(createManualTask, "Verify Flow/Reflow")
    addElement(createManualTask, "Check Catheter Pos")
    
    # --- End Event ---
    addElement(createEndEvent, "End")
    
    print "[" + str(step()) + "] Created " + str(len(elements)) + " elements"
    
    # =========================================================================
    # ELEMENT LAYOUT DEFINITION
    # =========================================================================
    # Layout: element name -> (column, row, lane)
    # Row 0 = main flow, Row -1/-2 = above, Row 1/2 = below
    
    elementLayout = {
        # Start
        "Start": (0, 0, "Doctor"),
        
        # Initial Preparation
        "Prep Split": (1, 0, "Doctor"),
        "Prepare Implements": (2, -1, "Doctor"),
        "Wash Hands": (2, 0, "Doctor"),
        "Get Sterile Clothes": (2, 1, "Doctor"),
        "Prep Join": (3, 0, "Doctor"),
        
        # Puncture Area
        "Clean Puncture Area": (4, 0, "Doctor"),
        "Drape Puncture Zone": (5, 0, "Doctor"),
        
        # Ultrasound Config
        "US Split": (6, 0, "Doctor"),
        "Configure Ultrasound": (7, -1, "Doctor"),
        "Put Gel on Probe": (7, 1, "Doctor"),
        "US Join": (8, 0, "Doctor"),
        
        # Probe Prep
        "Cover Probe": (9, 0, "Doctor"),
        "Put Sterile Gel": (10, 0, "Doctor"),
        
        # Positioning
        "Pos Split": (11, 0, "Doctor"),
        "Position Probe": (12, -1, "Doctor"),
        "Position Patient": (12, 1, "Doctor"),
        "Pos Join": (13, 0, "Doctor"),
        
        # Vein Identification
        "ID Split": (14, 0, "Doctor"),
        "Anatomic ID": (15, -1, "Doctor"),
        "Doppler ID": (15, 0, "Doctor"),
        "Compression ID": (15, 1, "Doctor"),
        "ID Join": (16, 0, "Doctor"),
        
        # Puncture
        "Anesthetize": (17, 0, "Doctor"),
        "Puncture": (18, 0, "Doctor"),
        "Check Blood Return": (19, 0, "Doctor"),
        "Blood Return OK?": (20, 0, "Doctor"),
        
        # Post-Puncture
        "Drop Probe": (21, 0, "Doctor"),
        "Remove Syringe": (22, 0, "Doctor"),
        "Install Guidewire": (23, 0, "Doctor"),
        "Remove Trocar": (24, 0, "Doctor"),
        
        # Wire Check
        "Wire Check Split": (25, 0, "Doctor"),
        "Check Wire Long Axis": (26, -1, "Doctor"),
        "Check Wire Short Axis": (26, 1, "Doctor"),
        "Wire Check Join": (27, 0, "Doctor"),
        
        # Wire Position Decision
        "Wire Position OK?": (28, 0, "Doctor"),
        
        # Catheter Installation
        "Widen Pathway": (29, 0, "Doctor"),
        "Advance Catheter": (30, 0, "Doctor"),
        "Remove Guidewire": (31, 0, "Doctor"),
        
        # Final
        "Verify Flow/Reflow": (32, 0, "Doctor"),
        "Check Catheter Pos": (33, 0, "Doctor"),
        "End": (34, 0, "Doctor"),
    }
    
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
    
    # =========================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""
    
    # Get lane center Y
    laneBounds = getBounds(diagramHandle, doctorLane)
    if laneBounds:
        baseCenterY = laneBounds["y"] + laneBounds["h"] / 2
        print "[" + str(step()) + "] Lane centerY = " + str(int(baseCenterY))
    else:
        baseCenterY = 150
        print "[" + str(step()) + "] Using default centerY = 150"
    
    print ""
    
    repositionedCount = 0
    
    for name, (col, row, laneName) in elementLayout.items():
        if name not in elementGraphics:
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
            continue
        
        # Calculate position
        targetX = START_X + SPACING_X * col
        targetY = baseCenterY + SPACING_Y * row - 25
        
        # Determine dimensions
        elemClass = elem.getMClass().getName()
        if "Gateway" in elemClass:
            width = GATEWAY_SIZE
            height = GATEWAY_SIZE
        elif "Event" in elemClass:
            width = EVENT_SIZE
            height = EVENT_SIZE
        else:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
    
    diagramHandle.save()
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + " elements"
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = [
        # Start to Prep
        ("Start", "Prep Split", ""),
        
        # Initial Preparation (parallel)
        ("Prep Split", "Prepare Implements", ""),
        ("Prep Split", "Wash Hands", ""),
        ("Prep Split", "Get Sterile Clothes", ""),
        ("Prepare Implements", "Prep Join", ""),
        ("Wash Hands", "Prep Join", ""),
        ("Get Sterile Clothes", "Prep Join", ""),
        
        # Puncture Area
        ("Prep Join", "Clean Puncture Area", ""),
        ("Clean Puncture Area", "Drape Puncture Zone", ""),
        
        # Ultrasound (parallel)
        ("Drape Puncture Zone", "US Split", ""),
        ("US Split", "Configure Ultrasound", ""),
        ("US Split", "Put Gel on Probe", ""),
        ("Configure Ultrasound", "US Join", ""),
        ("Put Gel on Probe", "US Join", ""),
        
        # Probe Prep
        ("US Join", "Cover Probe", ""),
        ("Cover Probe", "Put Sterile Gel", ""),
        
        # Positioning (parallel)
        ("Put Sterile Gel", "Pos Split", ""),
        ("Pos Split", "Position Probe", ""),
        ("Pos Split", "Position Patient", ""),
        ("Position Probe", "Pos Join", ""),
        ("Position Patient", "Pos Join", ""),
        
        # Vein Identification (exclusive - one path)
        ("Pos Join", "ID Split", ""),
        ("ID Split", "Anatomic ID", "Anatomic"),
        ("ID Split", "Doppler ID", "Doppler"),
        ("ID Split", "Compression ID", "Compression"),
        ("Anatomic ID", "ID Join", ""),
        ("Doppler ID", "ID Join", ""),
        ("Compression ID", "ID Join", ""),
        
        # Puncture sequence
        ("ID Join", "Anesthetize", ""),
        ("Anesthetize", "Puncture", ""),
        ("Puncture", "Check Blood Return", ""),
        ("Check Blood Return", "Blood Return OK?", ""),
        
        # Blood Return decision
        ("Blood Return OK?", "Puncture", "No"),
        ("Blood Return OK?", "Drop Probe", "Yes"),
        
        # Post-Puncture sequence
        ("Drop Probe", "Remove Syringe", ""),
        ("Remove Syringe", "Install Guidewire", ""),
        ("Install Guidewire", "Remove Trocar", ""),
        
        # Wire Check (exclusive - one path)
        ("Remove Trocar", "Wire Check Split", ""),
        ("Wire Check Split", "Check Wire Long Axis", "Long Axis"),
        ("Wire Check Split", "Check Wire Short Axis", "Short Axis"),
        ("Check Wire Long Axis", "Wire Check Join", ""),
        ("Check Wire Short Axis", "Wire Check Join", ""),
        
        # Wire Position decision
        ("Wire Check Join", "Wire Position OK?", ""),
        ("Wire Position OK?", "Puncture", "No"),
        ("Wire Position OK?", "Widen Pathway", "Yes"),
        
        # Catheter Installation
        ("Widen Pathway", "Advance Catheter", ""),
        ("Advance Catheter", "Remove Guidewire", ""),
        
        # Final verification
        ("Remove Guidewire", "Verify Flow/Reflow", ""),
        ("Verify Flow/Reflow", "Check Catheter Pos", ""),
        ("Check Catheter Pos", "End", ""),
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
    # CLEANUP
    # =========================================================================
    
    diagramHandle.close()
    print "[" + str(step()) + "] Diagram closed"
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print ""
    print "=================================================================="
    print "COMPLETE"
    print "=================================================================="
    print "Process:  " + processName
    print "Lanes:    1 (Doctor)"
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
        createCVCInsertionProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
