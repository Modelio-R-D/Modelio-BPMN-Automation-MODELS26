# CatheterPlacement.py
#
# Description:
#   BPMN process diagram for Catheter Placement procedure.
#   Single lane: Doctor
#
#   Workflow:
#   1. Preparation (implements, washing, sterile clothes)
#   2. Site preparation (clean, drape)
#   3. Ultrasound setup (configure, gel, cover)
#   4. Positioning (probe, patient)
#   5. Vein identification (3 alternative methods)
#   6. Puncture and blood return check (loop if failed)
#   7. Guidewire installation and check (2 methods)
#   8. Wire position verification (loop if failed)
#   9. Catheter placement and final verification
#
# Applicable on: Package
# Version: 1.0
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
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

SCRIPT_VERSION = "v1.0"
EXECUTION_ID = str(int(time.time() * 1000) % 100000)

# Waiting configuration for auto-unmask
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3

# Layout configuration
SPACING = 130
START_X = 80
TASK_WIDTH = 110
TASK_HEIGHT = 55

# Y offset for alternative paths (within same lane)
Y_OFFSET_ALTERNATIVE = 55

# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def createLane(laneSet, name):
    """Create a BPMN Lane (swim lane) in the given lane set."""
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


def createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon - physical task)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createUserTask(process, name):
    """Create a BPMN User Task (person icon - human activity with IT)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (X diamond - XOR decision)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def createSequenceFlow(process, source, target, name="", guard=""):
    """
    Create a BPMN Sequence Flow (arrow between elements).
    
    Parameters:
    - process: The BPMN process container
    - source: Source element
    - target: Target element
    - name: Optional name for the flow
    - guard: Condition expression for gateway outflows
    """
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
    """Calculate the center Y position for placing elements in a lane."""
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format a compact summary of all lanes with their Y ranges."""
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
    """Format a compact summary of element Y positions."""
    parts = []
    sortedElems = []
    for elem in elements:
        name = elem.getName()
        col = elementLayout.get(name, (99, "?", 0))[0]
        sortedElems.append((col, name, elem))
    sortedElems.sort()
    
    for col, name, elem in sortedElems:
        bounds = getBounds(diagramHandle, elem)
        if bounds:
            shortName = name[:10]
            parts.append(shortName + "=Y" + str(int(bounds["y"])))
        else:
            parts.append(name[:10] + "=--")
    return "Elements: " + ", ".join(parts)


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
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)
        
        time.sleep(WAIT_TIME_MS / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    """Try to manually unmask elements that were not auto-unmasked."""
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
            layoutInfo = elementLayout.get(name, (0, "Doctor", 0))
            laneName = layoutInfo[1]
            yOffset = layoutInfo[2] if len(layoutInfo) > 2 else 0
            targetY = laneY.get(laneName, 100) + yOffset
            
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

def createCatheterPlacementProcess(parentPackage):
    """Create the Catheter Placement BPMN process with diagram."""
    
    processName = "CatheterPlacement_" + EXECUTION_ID
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN CATHETER PLACEMENT PROCESS"
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
    
    doctorLane = createLane(laneSet, "Doctor")
    
    lanes = {
        "Doctor": doctorLane
    }
    laneOrder = ["Doctor"]
    
    print "[" + str(step()) + "] Lanes: Doctor"
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS & ASSIGN TO LANES
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    
    def addElement(creator, name, lane, laneName, yOffset=0):
        """Helper to create element, add to lane, and register."""
        elem = creator(process, name)
        addToLane(elem, lane)
        elements.append(elem)
        elementRefs[name] = elem
        return elem
    
    # --- Start Event ---
    addElement(createStartEvent, "Start", doctorLane, "Doctor")
    
    # --- Preparation Tasks ---
    addElement(createManualTask, "Prepare Implements", doctorLane, "Doctor")
    addElement(createManualTask, "Wash Hands", doctorLane, "Doctor")
    addElement(createManualTask, "Get Sterile Clothes", doctorLane, "Doctor")
    
    # --- Site Preparation ---
    addElement(createManualTask, "Clean Puncture Area", doctorLane, "Doctor")
    addElement(createManualTask, "Drape Puncture Zone", doctorLane, "Doctor")
    
    # --- Ultrasound Setup ---
    addElement(createUserTask, "Configure Ultrasound", doctorLane, "Doctor")
    addElement(createManualTask, "Put Gel in Probe", doctorLane, "Doctor")
    addElement(createManualTask, "Cover Probe", doctorLane, "Doctor")
    addElement(createManualTask, "Put Sterile Gel", doctorLane, "Doctor")
    
    # --- Positioning ---
    addElement(createManualTask, "Position Probe", doctorLane, "Doctor")
    addElement(createManualTask, "Position Patient", doctorLane, "Doctor")
    
    # --- Vein Identification Gateway ---
    addElement(createExclusiveGateway, "Identify Vein", doctorLane, "Doctor")
    
    # --- Identification Methods (alternative paths) ---
    addElement(createUserTask, "Anatomic ID", doctorLane, "Doctor", -Y_OFFSET_ALTERNATIVE)
    addElement(createUserTask, "Doppler ID", doctorLane, "Doctor", 0)
    addElement(createUserTask, "Compression ID", doctorLane, "Doctor", Y_OFFSET_ALTERNATIVE)
    
    # --- Merge Gateway ---
    addElement(createExclusiveGateway, "Vein Identified", doctorLane, "Doctor")
    
    # --- Puncture ---
    addElement(createManualTask, "Anesthetize Patient", doctorLane, "Doctor")
    addElement(createManualTask, "Puncture", doctorLane, "Doctor")
    
    # --- Blood Return Check Gateway ---
    addElement(createExclusiveGateway, "Blood Return OK?", doctorLane, "Doctor")
    
    # --- Post-Puncture (if blood return OK) ---
    addElement(createManualTask, "Drop Probe", doctorLane, "Doctor")
    addElement(createManualTask, "Remove Syringe", doctorLane, "Doctor")
    
    # --- Guidewire ---
    addElement(createManualTask, "Install Guidewire", doctorLane, "Doctor")
    addElement(createManualTask, "Remove Trocar", doctorLane, "Doctor")
    
    # --- Wire Check Gateway ---
    addElement(createExclusiveGateway, "Check Wire Method", doctorLane, "Doctor")
    
    # --- Wire Check Methods (alternative paths) ---
    addElement(createUserTask, "Check Long Axis", doctorLane, "Doctor", -Y_OFFSET_ALTERNATIVE)
    addElement(createUserTask, "Check Short Axis", doctorLane, "Doctor", Y_OFFSET_ALTERNATIVE)
    
    # --- Wire Check Merge Gateway ---
    addElement(createExclusiveGateway, "Wire Checked", doctorLane, "Doctor")
    
    # --- Wire Position Check Gateway ---
    addElement(createExclusiveGateway, "Wire Position OK?", doctorLane, "Doctor")
    
    # --- Catheter Placement (if wire position OK) ---
    addElement(createManualTask, "Widen Pathway", doctorLane, "Doctor")
    addElement(createManualTask, "Advance Catheter", doctorLane, "Doctor")
    addElement(createManualTask, "Remove Guidewire", doctorLane, "Doctor")
    
    # --- Final Verification ---
    addElement(createUserTask, "Verify Flow and Reflow", doctorLane, "Doctor")
    addElement(createUserTask, "Check Catheter Position", doctorLane, "Doctor")
    
    # --- End Event ---
    addElement(createEndEvent, "End", doctorLane, "Doctor")
    
    print "[" + str(step()) + "] Doctor lane: " + str(len(elements)) + " elements"
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
    # PHASE 4: WAIT FOR ELEMENTS TO BE AVAILABLE
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""
    
    # Layout: element name -> (column, lane_name, y_offset)
    elementLayout = {
        # Preparation phase
        "Start": (0, "Doctor", 0),
        "Prepare Implements": (1, "Doctor", 0),
        "Wash Hands": (2, "Doctor", 0),
        "Get Sterile Clothes": (3, "Doctor", 0),
        # Site preparation
        "Clean Puncture Area": (4, "Doctor", 0),
        "Drape Puncture Zone": (5, "Doctor", 0),
        # Ultrasound setup
        "Configure Ultrasound": (6, "Doctor", 0),
        "Put Gel in Probe": (7, "Doctor", 0),
        "Cover Probe": (8, "Doctor", 0),
        "Put Sterile Gel": (9, "Doctor", 0),
        # Positioning
        "Position Probe": (10, "Doctor", 0),
        "Position Patient": (11, "Doctor", 0),
        # Vein identification
        "Identify Vein": (12, "Doctor", 0),
        "Anatomic ID": (13, "Doctor", -Y_OFFSET_ALTERNATIVE),
        "Doppler ID": (13, "Doctor", 0),
        "Compression ID": (13, "Doctor", Y_OFFSET_ALTERNATIVE),
        "Vein Identified": (14, "Doctor", 0),
        # Puncture
        "Anesthetize Patient": (15, "Doctor", 0),
        "Puncture": (16, "Doctor", 0),
        "Blood Return OK?": (17, "Doctor", 0),
        # Post-puncture
        "Drop Probe": (18, "Doctor", 0),
        "Remove Syringe": (19, "Doctor", 0),
        # Guidewire
        "Install Guidewire": (20, "Doctor", 0),
        "Remove Trocar": (21, "Doctor", 0),
        # Wire check
        "Check Wire Method": (22, "Doctor", 0),
        "Check Long Axis": (23, "Doctor", -Y_OFFSET_ALTERNATIVE),
        "Check Short Axis": (23, "Doctor", Y_OFFSET_ALTERNATIVE),
        "Wire Checked": (24, "Doctor", 0),
        # Wire position check
        "Wire Position OK?": (25, "Doctor", 0),
        # Catheter placement
        "Widen Pathway": (26, "Doctor", 0),
        "Advance Catheter": (27, "Doctor", 0),
        "Remove Guidewire": (28, "Doctor", 0),
        # Final verification
        "Verify Flow and Reflow": (29, "Doctor", 0),
        "Check Catheter Position": (30, "Doctor", 0),
        "End": (31, "Doctor", 0),
    }
    
    print "[" + str(step()) + "] Waiting for elements (max " + str(MAX_ATTEMPTS) + " attempts, " + str(WAIT_TIME_MS) + "ms interval)..."
    print ""
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    totalWaitTime = attempts * WAIT_TIME_MS
    foundCount = len(elementGraphics)
    
    if foundCount < len(elements):
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
    else:
        print ""
        print "[" + str(step()) + "] SUCCESS: All " + str(foundCount) + " elements ready in " + str(totalWaitTime) + "ms"
    
    print ""
    print "  " + formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    # =========================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""
    
    # Get lane center Y
    laneY = {}
    for laneName in laneOrder:
        lane = lanes[laneName]
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
    
    print ""
    
    # Sort elements by column for left-to-right processing
    sortedElements = []
    for name, layoutInfo in elementLayout.items():
        col = layoutInfo[0]
        laneName = layoutInfo[1]
        yOffset = layoutInfo[2] if len(layoutInfo) > 2 else 0
        sortedElements.append((col, name, laneName, yOffset))
    sortedElements.sort()
    
    repositionedCount = 0
    previousLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    for col, name, laneName, yOffset in sortedElements:
        if name not in elementGraphics:
            print "[" + str(step()) + "] SKIP " + name + ": not in diagram"
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = getBounds(diagramHandle, elem)
        
        if not bounds:
            print "[" + str(step()) + "] SKIP " + name + ": no bounds"
            continue
        
        # Calculate target position
        targetX = START_X + SPACING * col
        targetY = laneY.get(laneName, 100) + yOffset
        
        # Determine width and height
        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = TASK_WIDTH
            height = TASK_HEIGHT
        else:
            width = bounds["w"]
            height = bounds["h"]
        
        # Set new bounds
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
        
        diagramHandle.save()
        
        # Check if lanes changed
        currentLanes = formatLanesSummary(diagramHandle, lanes, laneOrder)
        laneChanged = " *** LANE CHANGED ***" if currentLanes != previousLanes else ""
        
        yInfo = "Y" + str(int(targetY))
        if yOffset != 0:
            yInfo += " (offset=" + str(yOffset) + ")"
        
        print "[" + str(step()) + "] " + name + " -> (" + str(int(targetX)) + "," + yInfo + ")" + laneChanged
        
        previousLanes = currentLanes
    
    print ""
    print "  Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 6: CREATE SEQUENCE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    # Flow definitions: (source, target, guard)
    flowDefs = [
        # Preparation phase
        ("Start", "Prepare Implements", ""),
        ("Prepare Implements", "Wash Hands", ""),
        ("Wash Hands", "Get Sterile Clothes", ""),
        ("Get Sterile Clothes", "Clean Puncture Area", ""),
        # Site preparation
        ("Clean Puncture Area", "Drape Puncture Zone", ""),
        ("Drape Puncture Zone", "Configure Ultrasound", ""),
        # Ultrasound setup
        ("Configure Ultrasound", "Put Gel in Probe", ""),
        ("Put Gel in Probe", "Cover Probe", ""),
        ("Cover Probe", "Put Sterile Gel", ""),
        ("Put Sterile Gel", "Position Probe", ""),
        # Positioning
        ("Position Probe", "Position Patient", ""),
        ("Position Patient", "Identify Vein", ""),
        # Vein identification (XOR split)
        ("Identify Vein", "Anatomic ID", "Anatomic"),
        ("Identify Vein", "Doppler ID", "Doppler"),
        ("Identify Vein", "Compression ID", "Compression"),
        # Vein identification merge
        ("Anatomic ID", "Vein Identified", ""),
        ("Doppler ID", "Vein Identified", ""),
        ("Compression ID", "Vein Identified", ""),
        # Puncture
        ("Vein Identified", "Anesthetize Patient", ""),
        ("Anesthetize Patient", "Puncture", ""),
        ("Puncture", "Blood Return OK?", ""),
        # Blood return check (XOR with loop)
        ("Blood Return OK?", "Puncture", "No"),
        ("Blood Return OK?", "Drop Probe", "Yes"),
        # Post-puncture
        ("Drop Probe", "Remove Syringe", ""),
        ("Remove Syringe", "Install Guidewire", ""),
        # Guidewire
        ("Install Guidewire", "Remove Trocar", ""),
        ("Remove Trocar", "Check Wire Method", ""),
        # Wire check (XOR split)
        ("Check Wire Method", "Check Long Axis", "Long Axis"),
        ("Check Wire Method", "Check Short Axis", "Short Axis"),
        # Wire check merge
        ("Check Long Axis", "Wire Checked", ""),
        ("Check Short Axis", "Wire Checked", ""),
        # Wire position check
        ("Wire Checked", "Wire Position OK?", ""),
        # Wire position check (XOR with loop)
        ("Wire Position OK?", "Puncture", "No"),
        ("Wire Position OK?", "Widen Pathway", "Yes"),
        # Catheter placement
        ("Widen Pathway", "Advance Catheter", ""),
        ("Advance Catheter", "Remove Guidewire", ""),
        # Final verification
        ("Remove Guidewire", "Verify Flow and Reflow", ""),
        ("Verify Flow and Reflow", "Check Catheter Position", ""),
        ("Check Catheter Position", "End", ""),
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
    print "=================================================================="
    print ""
    print "PROCESS SUMMARY:"
    print "  1. Preparation: Implements, washing, sterile clothes"
    print "  2. Site prep: Clean and drape puncture zone"
    print "  3. Ultrasound: Configure, gel, cover, sterile gel"
    print "  4. Positioning: Probe and patient"
    print "  5. Vein ID: Anatomic / Doppler / Compression (XOR)"
    print "  6. Puncture: Anesthetize and puncture"
    print "  7. Blood check: Loop back if No, continue if Yes"
    print "  8. Guidewire: Install, remove trocar"
    print "  9. Wire check: Long axis / Short axis (XOR)"
    print "  10. Wire position: Loop back if No, continue if Yes"
    print "  11. Catheter: Widen, advance, remove guidewire"
    print "  12. Final: Verify flow/reflow, check position"
    print "=================================================================="
    
    return process


# ============================================================================
# MACRO ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createCatheterPlacementProcess(element)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
