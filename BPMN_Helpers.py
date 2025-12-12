#
# BPMN_Helpers.py
#
# Description:
#   Reusable helper library for creating BPMN process diagrams in Modelio.
#   Place this file in: .modelio/5.4/macros/BPMN_Helpers.py
#   Load from generated scripts with: execfile(".modelio/5.4/macros/BPMN_Helpers.py")
#
# Key Insight (from Modelio developers, Dec 2025):
#   - Modelio automatically unmasks elements when a diagram is created
#   - No need to call unmask() manually for initial display
#   - BUT: There may be a delay before elements are available
#   - IF elements still missing: manual unmask INSIDE the correct lane
#
# Version: 2.5 - December 2025
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

# Try to import Data Object classes (may not be available in all Modelio versions)
try:
    from org.modelio.metamodel.bpmn.objects import BpmnDataObject
    from org.modelio.metamodel.bpmn.objects import BpmnDataAssociation
    _DATA_OBJECTS_AVAILABLE = True
except ImportError:
    _DATA_OBJECTS_AVAILABLE = False
    print "WARNING: BpmnDataObject/BpmnDataAssociation not available in this Modelio version"

print "BPMN_Helpers.py loaded (Data Objects: " + str(_DATA_OBJECTS_AVAILABLE) + ")"


# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

BPMN_DEFAULT_CONFIG = {
    # Waiting configuration for auto-unmask
    "WAIT_TIME_MS": 50,           # Time between attempts (milliseconds)
    "MAX_ATTEMPTS": 3,            # Maximum number of attempts
    
    # Layout configuration
    "SPACING": 150,               # Horizontal spacing between columns
    "START_X": 80,                # Starting X position
    
    # Task dimensions
    "TASK_WIDTH": 120,            # Width for all tasks
    "TASK_HEIGHT": 60,            # Height for all tasks
    
    # Data object dimensions
    "DATA_WIDTH": 40,             # Width for data objects
    "DATA_HEIGHT": 50,            # Height for data objects
    "DATA_OFFSET_X": 20,          # Horizontal offset from column position
    "DATA_OFFSET_Y": 80,          # Vertical offset from lane center (positive = below)
}


# ============================================================================
# ELEMENT TYPE CONSTANTS
# ============================================================================

# Events
START = "START"
MESSAGE_START = "MESSAGE_START"
TIMER_START = "TIMER_START"
END = "END"
MESSAGE_END = "MESSAGE_END"

# Tasks
USER_TASK = "USER_TASK"
SERVICE_TASK = "SERVICE_TASK"
MANUAL_TASK = "MANUAL_TASK"

# Gateways
EXCLUSIVE_GW = "EXCLUSIVE_GW"
PARALLEL_GW = "PARALLEL_GW"

# Data
DATA_OBJECT = "DATA_OBJECT"


# ============================================================================
# BPMN ELEMENT CREATION HELPERS
# ============================================================================

def _createLane(laneSet, name):
    """Create a BPMN Lane (swim lane) in the given lane set."""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def _addToLane(element, lane):
    """Assign an element to a lane (REQUIRED for proper positioning)."""
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False


def _createStartEvent(process, name):
    """Create a BPMN Start Event (green circle)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def _createMessageStartEvent(process, name):
    """Create a BPMN Message Start Event (envelope icon)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


def _createTimerStartEvent(process, name):
    """Create a BPMN Timer Start Event (clock icon)."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        pass
    return event


def _createEndEvent(process, name):
    """Create a BPMN End Event (red circle)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def _createMessageEndEvent(process, name):
    """Create a BPMN Message End Event (envelope icon)."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event


def _createUserTask(process, name):
    """Create a BPMN User Task (person icon)."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createServiceTask(process, name):
    """Create a BPMN Service Task (gear icon)."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createManualTask(process, name):
    """Create a BPMN Manual Task (hand icon)."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway (X diamond)."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def _createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway (+ diamond)."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def _createDataObject(process, name):
    """Create a BPMN Data Object (document icon)."""
    if not _DATA_OBJECTS_AVAILABLE:
        print "ERROR: BpmnDataObject not available in this Modelio version"
        return None
    try:
        dataObj = modelingSession.getModel().createBpmnDataObject()
        dataObj.setName(name)
        dataObj.setContainer(process)
        return dataObj
    except Exception as e:
        print "ERROR creating data object '" + name + "': " + str(e)
        return None


def _createSequenceFlow(process, source, target, guard=""):
    """Create a BPMN Sequence Flow (arrow between elements)."""
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    
    # Set guard as both name (for display) and condition expression
    if guard:
        flow.setName(guard)
        try:
            flow.setConditionExpression(guard)
        except:
            pass  # Some Modelio versions may not have this method
    
    return flow


def _createDataAssociation(process, source, target):
    """
    Create a BPMN Data Association (dotted arrow for data flow).
    Direction is auto-detected based on element types.

    Args:
        process: The BPMN process
        source: Source element (task or data object)
        target: Target element (task or data object)

    Returns:
        The created BpmnDataAssociation or None

    BPMN Data Association Semantics:
        - OUTPUT (Task -> DataObject): StartingActivity = Task, TargetRef = DataObject
        - INPUT (DataObject -> Task): EndingActivity = Task, SourceRef = DataObject
    """
    if not _DATA_OBJECTS_AVAILABLE:
        print "ERROR: BpmnDataAssociation not available in this Modelio version"
        return None

    # Auto-detect direction based on element types
    sourceIsData = isinstance(source, BpmnDataObject)
    targetIsData = isinstance(target, BpmnDataObject)

    if sourceIsData and targetIsData:
        print "ERROR: Both source and target are DataObjects"
        return None
    if not sourceIsData and not targetIsData:
        print "ERROR: Neither source nor target is a DataObject"
        return None

    try:
        assoc = modelingSession.getModel().createBpmnDataAssociation()

        if sourceIsData:
            # Data flows INTO the activity (DataObject -> Task)
            assoc.getSourceRef().add(source)   # SourceRef = DataObject
            assoc.setEndingActivity(target)    # EndingActivity = Task (receives data)
        else:
            # Data flows OUT OF the activity (Task -> DataObject)
            assoc.setTargetRef(target)         # TargetRef = DataObject
            assoc.setStartingActivity(source)  # StartingActivity = Task (produces data)

        return assoc
    except Exception as e:
        print "ERROR creating data association: " + str(e)
        return None


# Element type to creator function mapping
_ELEMENT_CREATORS = {
    START: _createStartEvent,
    MESSAGE_START: _createMessageStartEvent,
    TIMER_START: _createTimerStartEvent,
    END: _createEndEvent,
    MESSAGE_END: _createMessageEndEvent,
    USER_TASK: _createUserTask,
    SERVICE_TASK: _createServiceTask,
    MANUAL_TASK: _createManualTask,
    EXCLUSIVE_GW: _createExclusiveGateway,
    PARALLEL_GW: _createParallelGateway,
}

# Add DATA_OBJECT only if available
if _DATA_OBJECTS_AVAILABLE:
    _ELEMENT_CREATORS[DATA_OBJECT] = _createDataObject


def _createElement(process, name, elementType):
    """Create a BPMN element by type."""
    creator = _ELEMENT_CREATORS.get(elementType)
    if creator:
        return creator(process, name)
    else:
        print "ERROR: Unknown element type: " + str(elementType)
        return None


# ============================================================================
# DIAGRAM UTILITIES
# ============================================================================

def _parseBounds(boundsStr):
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


def _getGraphics(diagramHandle, element):
    """Get the diagram graphics for an element. Returns first graphic or None."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def _getBounds(diagramHandle, element):
    """Get the bounds of an element in the diagram. Returns dict or None."""
    dg = _getGraphics(diagramHandle, element)
    if dg:
        return _parseBounds(str(dg.getBounds()))
    return None


def _getLaneCenterY(diagramHandle, lane):
    """Calculate the center Y position for placing elements in a lane."""
    bounds = _getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


def _formatLanesSummary(diagramHandle, lanes, laneOrder):
    """Format a compact summary of all lanes with their Y ranges."""
    parts = []
    for laneName in laneOrder:
        lane = lanes[laneName]
        info = _getBounds(diagramHandle, lane)
        if info:
            yEnd = int(info["y"] + info["h"])
            parts.append(laneName + "(" + str(int(info["y"])) + "-" + str(yEnd) + ")")
        else:
            parts.append(laneName + "(--)")
    return "Lanes: " + "; ".join(parts)


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def _waitForElements(diagramHandle, elements, config):
    """Wait until all elements are available in the diagram."""
    elementGraphics = {}
    attempt = 0
    totalElements = len(elements)
    maxAttempts = config.get("MAX_ATTEMPTS", BPMN_DEFAULT_CONFIG["MAX_ATTEMPTS"])
    waitTimeMs = config.get("WAIT_TIME_MS", BPMN_DEFAULT_CONFIG["WAIT_TIME_MS"])
    
    while attempt < maxAttempts:
        attempt += 1
        
        for elem in elements:
            name = elem.getName()
            if name not in elementGraphics:
                dg = _getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
        
        foundCount = len(elementGraphics)
        
        if foundCount == totalElements:
            print "  [Attempt " + str(attempt) + "] All " + str(foundCount) + " elements ready"
            return elementGraphics, attempt
        else:
            missing = [e.getName()[:12] for e in elements if e.getName() not in elementGraphics]
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing)
        
        time.sleep(waitTimeMs / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt


def _unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLanes):
    """Manually unmask elements that were not auto-unmasked."""
    unmaskedCount = 0
    
    # Get each lane's center Y position
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = _getBounds(diagramHandle, lane)
        if bounds:
            centerY = int(bounds["y"] + bounds["h"] / 2)
            laneY[laneName] = centerY
    
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLanes.get(name, "")
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
# MAIN ORCHESTRATION FUNCTION
# ============================================================================

def createBPMNFromConfig(parentPackage, config):
    """
    Create a BPMN process diagram from a configuration dictionary.
    
    Config structure:
    {
        "name": "ProcessName",
        "lanes": ["Lane1", "Lane2", ...],
        "elements": [("Name", TYPE, "LaneName"), ...],
        "flows": [("Source", "Target", "Guard"), ...],
        "layout": {"Name": column_index, ...},
        
        # Optional - Data Objects and Associations
        "data_objects": [("DataName", "LaneName", column_index), ...],
        "data_associations": [("SourceName", "TargetName"), ...],
        
        # Optional overrides:
        "SPACING": 150, "START_X": 80, "TASK_WIDTH": 120, "TASK_HEIGHT": 60,
        "DATA_WIDTH": 40, "DATA_HEIGHT": 50, "DATA_OFFSET_X": 20, "DATA_OFFSET_Y": 80,
    }
    """
    
    executionId = str(int(time.time() * 1000) % 100000)
    processName = config.get("name", "Process") + "_" + executionId
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # Merge config with defaults
    cfg = dict(BPMN_DEFAULT_CONFIG)
    for key in ["SPACING", "START_X", "TASK_WIDTH", "TASK_HEIGHT", "WAIT_TIME_MS", "MAX_ATTEMPTS",
                "DATA_WIDTH", "DATA_HEIGHT", "DATA_OFFSET_X", "DATA_OFFSET_Y"]:
        if key in config:
            cfg[key] = config[key]
    
    # =========================================================================
    # HEADER
    # =========================================================================
    print ""
    print "=================================================================="
    print "BPMN PROCESS CREATION"
    print "=================================================================="
    print "Process Name: " + processName
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
    
    laneOrder = config.get("lanes", [])
    lanes = {}
    for laneName in laneOrder:
        lanes[laneName] = _createLane(laneSet, laneName)
    
    print "[" + str(step()) + "] Lanes: " + ", ".join(laneOrder)
    
    # =========================================================================
    # PHASE 2: CREATE ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    elementLanes = {}
    
    elementDefs = config.get("elements", [])
    
    # Group by lane for logging
    laneElements = {}
    for laneName in laneOrder:
        laneElements[laneName] = []
    
    for elemDef in elementDefs:
        name, elemType, laneName = elemDef
        elem = _createElement(process, name, elemType)
        if elem:
            if laneName in lanes:
                _addToLane(elem, lanes[laneName])
            elements.append(elem)
            elementRefs[name] = elem
            elementLanes[name] = laneName
            if laneName in laneElements:
                laneElements[laneName].append(name)
    
    for laneName in laneOrder:
        count = len(laneElements[laneName])
        print "[" + str(step()) + "] " + laneName + ": " + str(count) + " elements"
    
    print ""
    print "  Total: " + str(len(elements)) + " elements"
    
    # =========================================================================
    # PHASE 2B: CREATE DATA OBJECTS
    # =========================================================================
    dataObjectDefs = config.get("data_objects", [])
    dataObjects = []
    dataObjectRefs = {}
    dataObjectLanes = {}
    dataObjectLayout = {}  # name -> column
    
    if dataObjectDefs:
        print ""
        print "== PHASE 2B: CREATE DATA OBJECTS ================================"
        print ""
        
        for dataDef in dataObjectDefs:
            name, laneName, column = dataDef

            try:
                dataObj = _createDataObject(process, name)
                if dataObj:
                    if laneName in lanes:
                        _addToLane(dataObj, lanes[laneName])
                    dataObjects.append(dataObj)
                    dataObjectRefs[name] = dataObj
                    dataObjectLanes[name] = laneName
                    dataObjectLayout[name] = column
                    # Also add to elementRefs for association lookups
                    elementRefs[name] = dataObj
                    elementLanes[name] = laneName
                else:
                    print "[" + str(step()) + "] FAILED: " + name
            except Exception as e:
                print "[" + str(step()) + "] ERROR creating " + name + ": " + str(e)
        
        print "[" + str(step()) + "] Data Objects: " + str(len(dataObjects))
    
    # =========================================================================
    # PHASE 3: CREATE DIAGRAM
    # =========================================================================
    print ""
    print "== PHASE 3: CREATE DIAGRAM ======================================"
    print ""
    
    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName(processName)
    diagram.setOrigin(process)
    print "[" + str(step()) + "] Diagram: " + processName
    
    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    diagramHandle.save()
    print "[" + str(step()) + "] Save (triggers auto-unmask)"
    
    # =========================================================================
    # PHASE 4: WAIT FOR ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 4: WAIT FOR AUTO-UNMASK ================================"
    print ""
    
    layoutConfig = config.get("layout", {})
    
    # Combine elements and data objects for waiting
    allElements = elements + dataObjects
    
    elementGraphics, attempts = _waitForElements(diagramHandle, allElements, cfg)
    foundCount = len(elementGraphics)
    
    if foundCount < len(allElements):
        print ""
        print "[" + str(step()) + "] Manual unmask for missing elements..."
        print ""
        unmaskedCount = _unmaskMissingElements(diagramHandle, allElements, elementGraphics, lanes, elementLanes)
        
        if unmaskedCount > 0:
            diagramHandle.save()
    
    foundCount = len(elementGraphics)
    print ""
    print "[" + str(step()) + "] Elements ready: " + str(foundCount) + "/" + str(len(allElements))
    print "  " + _formatLanesSummary(diagramHandle, lanes, laneOrder)
    
    # =========================================================================
    # PHASE 5: REPOSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 5: REPOSITION ELEMENTS ================================="
    print ""
    
    # Get lane Y values
    laneY = {}
    for laneName in laneOrder:
        lane = lanes[laneName]
        y = _getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
            print "[" + str(step()) + "] " + laneName + " centerY = " + str(int(y))
    
    print ""
    
    # Sort elements by column
    sortedElements = []
    for name, col in layoutConfig.items():
        laneName = elementLanes.get(name, "")
        sortedElements.append((col, name, laneName))
    sortedElements.sort()
    
    repositionedCount = 0
    spacing = cfg["SPACING"]
    startX = cfg["START_X"]
    taskWidth = cfg["TASK_WIDTH"]
    taskHeight = cfg["TASK_HEIGHT"]
    
    for col, name, laneName in sortedElements:
        if name not in elementGraphics:
            continue
        
        dg = elementGraphics[name]
        elem = elementRefs[name]
        bounds = _getBounds(diagramHandle, elem)
        
        if not bounds:
            continue
        
        targetX = startX + spacing * col
        targetY = laneY.get(laneName, 100)
        
        # Use task dimensions for tasks, original for events/gateways
        elemClass = elem.getMClass().getName()
        if "Task" in elemClass:
            width = taskWidth
            height = taskHeight
        else:
            width = bounds["w"]
            height = bounds["h"]
        
        newBounds = Draw2DRectangle(
            int(targetX), int(targetY),
            int(width), int(height)
        )
        dg.setBounds(newBounds)
        repositionedCount += 1
        diagramHandle.save()
    
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(elements))
    
    # =========================================================================
    # PHASE 5B: REPOSITION DATA OBJECTS (lane by lane)
    # =========================================================================
    if dataObjects:
        print ""
        print "== PHASE 5B: REPOSITION DATA OBJECTS ============================"
        print ""
        
        dataWidth = cfg["DATA_WIDTH"]
        dataHeight = cfg["DATA_HEIGHT"]
        dataOffsetX = cfg["DATA_OFFSET_X"]
        dataOffsetY = cfg["DATA_OFFSET_Y"]
        
        dataRepositioned = 0
        
        # Process each lane in order
        for laneName in laneOrder:
            # Check if this lane has any data objects
            laneHasData = any(dataObjectLanes.get(name) == laneName for name in dataObjectLayout.keys())
            if not laneHasData:
                continue
            
            # Get CURRENT lane center (may have shifted due to previous lane expansion)
            currentLaneCenterY = _getLaneCenterY(diagramHandle, lanes[laneName])
            if not currentLaneCenterY:
                continue
            
            # Get current lane bounds for logging
            lb = _getBounds(diagramHandle, lanes[laneName])
            lbInfo = ""
            if lb:
                lbInfo = str(int(lb["y"])) + "-" + str(int(lb["y"] + lb["h"]))
            
            print "[" + laneName + "] center=" + str(int(currentLaneCenterY)) + " bounds=" + lbInfo
            
            # Find data objects belonging to this lane
            laneDataCount = 0
            for name, column in dataObjectLayout.items():
                if dataObjectLanes.get(name) != laneName:
                    continue

                if name not in elementGraphics:
                    print "  " + name + ": SKIP (not in graphics)"
                    continue

                dg = elementGraphics[name]

                # X position: column position + horizontal offset
                targetX = startX + spacing * column + dataOffsetX

                # Y position: CURRENT lane center + vertical offset (always below)
                targetY = currentLaneCenterY + dataOffsetY

                print "  " + name + " -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"

                newBounds = Draw2DRectangle(
                    int(targetX), int(targetY),
                    int(dataWidth), int(dataHeight)
                )
                dg.setBounds(newBounds)
                dataRepositioned += 1
                laneDataCount += 1
            
            # Save after each lane to trigger Modelio's auto-expansion
            if laneDataCount > 0:
                diagramHandle.save()
                print ""
        
        print "[" + str(step()) + "] Data objects repositioned: " + str(dataRepositioned) + "/" + str(len(dataObjects))
    
    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = config.get("flows", [])
    flows = []
    
    for flowDef in flowDefs:
        srcName, tgtName, guard = flowDef
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            flow = _createSequenceFlow(process, src, tgt, guard)
            flows.append(flow)
    
    print "[" + str(step()) + "] Created " + str(len(flows)) + " sequence flows"
    
    # =========================================================================
    # PHASE 6B: CREATE DATA ASSOCIATIONS
    # =========================================================================
    dataAssocDefs = config.get("data_associations", [])
    dataAssocs = []
    
    if dataAssocDefs:
        print ""
        print "== PHASE 6B: CREATE DATA ASSOCIATIONS ==========================="
        print ""
        
        for assocDef in dataAssocDefs:
            srcName, tgtName = assocDef[0], assocDef[1]

            src = elementRefs.get(srcName)
            tgt = elementRefs.get(tgtName)

            if not src:
                print "  ERROR: Source not found: " + srcName
                continue
            if not tgt:
                print "  ERROR: Target not found: " + tgtName
                continue

            assoc = _createDataAssociation(process, src, tgt)
            if assoc:
                dataAssocs.append(assoc)
        
        print "[" + str(step()) + "] Data associations: " + str(len(dataAssocs))
    
    diagramHandle.save()
    diagramHandle.close()
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print ""
    print "=================================================================="
    print "COMPLETE: " + processName
    print "=================================================================="
    summary = "Lanes: " + str(len(lanes)) + " | Elements: " + str(len(elements))
    if dataObjects:
        summary += " | Data: " + str(len(dataObjects))
    summary += " | Flows: " + str(len(flows))
    if dataAssocs:
        summary += " | DataAssoc: " + str(len(dataAssocs))
    print summary
    print "=================================================================="
    
    return process