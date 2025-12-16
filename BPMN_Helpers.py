#
# BPMN_Helpers.py
#
# Description:
#   Comprehensive helper library for creating BPMN process diagrams in Modelio.
#   Supports two positioning modes:
#   - Column-based: Standard layout with automatic positioning (v2.7 logic)
#   - Lane-relative: Exact positioning from BPMN_Export for diagram cloning
#
#   Place this file in: .modelio/5.4/macros/BPMN_Helpers.py
#
# Version: 3.1 - December 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.activities import BpmnTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.gateways import BpmnParallelGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package
from org.eclipse.draw2d.geometry import Rectangle as Draw2DRectangle
import re
import time

# Try imports for extended types
try:
    from org.modelio.metamodel.bpmn.activities import BpmnScriptTask
    _SCRIPT_TASK_AVAILABLE = True
except ImportError:
    _SCRIPT_TASK_AVAILABLE = False

try:
    from org.modelio.metamodel.bpmn.activities import BpmnBusinessRuleTask
    _BUSINESS_RULE_TASK_AVAILABLE = True
except ImportError:
    _BUSINESS_RULE_TASK_AVAILABLE = False

try:
    from org.modelio.metamodel.bpmn.activities import BpmnSendTask
    from org.modelio.metamodel.bpmn.activities import BpmnReceiveTask
    _SEND_RECEIVE_AVAILABLE = True
except ImportError:
    _SEND_RECEIVE_AVAILABLE = False

try:
    from org.modelio.metamodel.bpmn.gateways import BpmnInclusiveGateway
    from org.modelio.metamodel.bpmn.gateways import BpmnComplexGateway
    from org.modelio.metamodel.bpmn.gateways import BpmnEventBasedGateway
    _ADDITIONAL_GATEWAYS_AVAILABLE = True
except ImportError:
    _ADDITIONAL_GATEWAYS_AVAILABLE = False

try:
    from org.modelio.metamodel.bpmn.events import BpmnIntermediateCatchEvent
    from org.modelio.metamodel.bpmn.events import BpmnIntermediateThrowEvent
    _INTERMEDIATE_EVENTS_AVAILABLE = True
except ImportError:
    _INTERMEDIATE_EVENTS_AVAILABLE = False

try:
    from org.modelio.metamodel.bpmn.objects import BpmnDataObject
    from org.modelio.metamodel.bpmn.objects import BpmnDataAssociation
    _DATA_OBJECTS_AVAILABLE = True
except ImportError:
    _DATA_OBJECTS_AVAILABLE = False

print "BPMN_Helpers.py v3.1 loaded (Data Objects: " + str(_DATA_OBJECTS_AVAILABLE) + ")"


# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

BPMN_DEFAULT_CONFIG = {
    "WAIT_TIME_MS": 50,
    "MAX_ATTEMPTS": 3,
    "SPACING": 150,
    "START_X": 80,
    "TASK_WIDTH": 120,
    "TASK_HEIGHT": 60,
    "DATA_WIDTH": 40,
    "DATA_HEIGHT": 50,
    "DATA_OFFSET_X": 90,
    "DATA_OFFSET_Y": 10,
}


# ============================================================================
# ELEMENT TYPE CONSTANTS
# ============================================================================

# Events - Start
START = "START"
MESSAGE_START = "MESSAGE_START"
TIMER_START = "TIMER_START"
SIGNAL_START = "SIGNAL_START"
CONDITIONAL_START = "CONDITIONAL_START"

# Events - End
END = "END"
MESSAGE_END = "MESSAGE_END"
SIGNAL_END = "SIGNAL_END"
TERMINATE_END = "TERMINATE_END"
ERROR_END = "ERROR_END"

# Events - Intermediate
INTERMEDIATE_CATCH = "INTERMEDIATE_CATCH"
INTERMEDIATE_THROW = "INTERMEDIATE_THROW"
MESSAGE_CATCH = "MESSAGE_CATCH"
MESSAGE_THROW = "MESSAGE_THROW"
TIMER_CATCH = "TIMER_CATCH"
SIGNAL_CATCH = "SIGNAL_CATCH"
SIGNAL_THROW = "SIGNAL_THROW"

# Tasks
TASK = "TASK"
USER_TASK = "USER_TASK"
SERVICE_TASK = "SERVICE_TASK"
MANUAL_TASK = "MANUAL_TASK"
SCRIPT_TASK = "SCRIPT_TASK"
BUSINESS_RULE_TASK = "BUSINESS_RULE_TASK"
SEND_TASK = "SEND_TASK"
RECEIVE_TASK = "RECEIVE_TASK"

# Gateways
EXCLUSIVE_GW = "EXCLUSIVE_GW"
PARALLEL_GW = "PARALLEL_GW"
INCLUSIVE_GW = "INCLUSIVE_GW"
COMPLEX_GW = "COMPLEX_GW"
EVENT_BASED_GW = "EVENT_BASED_GW"

# Data
DATA_OBJECT = "DATA_OBJECT"


# ============================================================================
# ELEMENT CREATION HELPERS
# ============================================================================

def _createLane(laneSet, name):
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane

def _addToLane(element, lane):
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False

def _createStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def _createMessageStartEvent(process, name):
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
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        pass
    return event

def _createSignalStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        signalDef = modelingSession.getModel().createBpmnSignalEventDefinition()
        signalDef.setDefined(event)
    except:
        pass
    return event

def _createConditionalStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        condDef = modelingSession.getModel().createBpmnConditionalEventDefinition()
        condDef.setDefined(event)
    except:
        pass
    return event

def _createEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def _createMessageEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event

def _createSignalEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        signalDef = modelingSession.getModel().createBpmnSignalEventDefinition()
        signalDef.setDefined(event)
    except:
        pass
    return event

def _createTerminateEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        termDef = modelingSession.getModel().createBpmnTerminateEventDefinition()
        termDef.setDefined(event)
    except:
        pass
    return event

def _createErrorEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        errDef = modelingSession.getModel().createBpmnErrorEventDefinition()
        errDef.setDefined(event)
    except:
        pass
    return event

def _createIntermediateCatchEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createStartEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def _createIntermediateThrowEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createEndEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateThrowEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def _createMessageCatchEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createIntermediateCatchEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event

def _createMessageThrowEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createIntermediateThrowEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateThrowEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        msgDef = modelingSession.getModel().createBpmnMessageEventDefinition()
        msgDef.setDefined(event)
    except:
        pass
    return event

def _createTimerCatchEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createIntermediateCatchEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        timerDef = modelingSession.getModel().createBpmnTimerEventDefinition()
        timerDef.setDefined(event)
    except:
        pass
    return event

def _createSignalCatchEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createIntermediateCatchEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        signalDef = modelingSession.getModel().createBpmnSignalEventDefinition()
        signalDef.setDefined(event)
    except:
        pass
    return event

def _createSignalThrowEvent(process, name):
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        return _createIntermediateThrowEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateThrowEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        signalDef = modelingSession.getModel().createBpmnSignalEventDefinition()
        signalDef.setDefined(event)
    except:
        pass
    return event

def _createTask(process, name):
    task = modelingSession.getModel().createBpmnTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createUserTask(process, name):
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createServiceTask(process, name):
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createManualTask(process, name):
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createScriptTask(process, name):
    if not _SCRIPT_TASK_AVAILABLE:
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnScriptTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createBusinessRuleTask(process, name):
    if not _BUSINESS_RULE_TASK_AVAILABLE:
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnBusinessRuleTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createSendTask(process, name):
    if not _SEND_RECEIVE_AVAILABLE:
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnSendTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createReceiveTask(process, name):
    if not _SEND_RECEIVE_AVAILABLE:
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnReceiveTask()
    task.setName(name)
    task.setContainer(process)
    return task

def _createExclusiveGateway(process, name):
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def _createParallelGateway(process, name):
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def _createInclusiveGateway(process, name):
    if not _ADDITIONAL_GATEWAYS_AVAILABLE:
        return _createExclusiveGateway(process, name)
    gateway = modelingSession.getModel().createBpmnInclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def _createComplexGateway(process, name):
    if not _ADDITIONAL_GATEWAYS_AVAILABLE:
        return _createExclusiveGateway(process, name)
    gateway = modelingSession.getModel().createBpmnComplexGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def _createEventBasedGateway(process, name):
    if not _ADDITIONAL_GATEWAYS_AVAILABLE:
        return _createExclusiveGateway(process, name)
    gateway = modelingSession.getModel().createBpmnEventBasedGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def _createDataObject(process, name):
    if not _DATA_OBJECTS_AVAILABLE:
        print "ERROR: BpmnDataObject not available"
        return None
    try:
        dataObj = modelingSession.getModel().createBpmnDataObject()
        dataObj.setName(name)
        dataObj.setContainer(process)
        return dataObj
    except Exception as e:
        print "ERROR creating data object: " + str(e)
        return None

def _createSequenceFlow(process, source, target, guard=""):
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    if guard:
        flow.setName(guard)
        try:
            flow.setConditionExpression(guard)
        except:
            pass
    return flow

def _createDataAssociation(process, source, target):
    if not _DATA_OBJECTS_AVAILABLE:
        print "ERROR: BpmnDataAssociation not available"
        return None
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
            assoc.getSourceRef().add(source)
            assoc.setEndingActivity(target)
        else:
            assoc.setTargetRef(target)
            assoc.setStartingActivity(source)
        return assoc
    except Exception as e:
        print "ERROR creating data association: " + str(e)
        return None

_ELEMENT_CREATORS = {
    START: _createStartEvent,
    MESSAGE_START: _createMessageStartEvent,
    TIMER_START: _createTimerStartEvent,
    SIGNAL_START: _createSignalStartEvent,
    CONDITIONAL_START: _createConditionalStartEvent,
    END: _createEndEvent,
    MESSAGE_END: _createMessageEndEvent,
    SIGNAL_END: _createSignalEndEvent,
    TERMINATE_END: _createTerminateEndEvent,
    ERROR_END: _createErrorEndEvent,
    INTERMEDIATE_CATCH: _createIntermediateCatchEvent,
    INTERMEDIATE_THROW: _createIntermediateThrowEvent,
    MESSAGE_CATCH: _createMessageCatchEvent,
    MESSAGE_THROW: _createMessageThrowEvent,
    TIMER_CATCH: _createTimerCatchEvent,
    SIGNAL_CATCH: _createSignalCatchEvent,
    SIGNAL_THROW: _createSignalThrowEvent,
    TASK: _createTask,
    USER_TASK: _createUserTask,
    SERVICE_TASK: _createServiceTask,
    MANUAL_TASK: _createManualTask,
    SCRIPT_TASK: _createScriptTask,
    BUSINESS_RULE_TASK: _createBusinessRuleTask,
    SEND_TASK: _createSendTask,
    RECEIVE_TASK: _createReceiveTask,
    EXCLUSIVE_GW: _createExclusiveGateway,
    PARALLEL_GW: _createParallelGateway,
    INCLUSIVE_GW: _createInclusiveGateway,
    COMPLEX_GW: _createComplexGateway,
    EVENT_BASED_GW: _createEventBasedGateway,
    DATA_OBJECT: _createDataObject,
}

def _createElement(process, name, elementType):
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
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None

def _getBounds(diagramHandle, element):
    dg = _getGraphics(diagramHandle, element)
    if dg:
        return _parseBounds(str(dg.getBounds()))
    return None

def _getLaneCenterY(diagramHandle, lane):
    bounds = _getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None

def _formatLanesSummary(diagramHandle, lanes, laneOrder):
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
            print "  [Attempt " + str(attempt) + "] Found: " + str(foundCount) + "/" + str(totalElements) + " | Missing: " + ", ".join(missing[:5]) + "..."
        
        time.sleep(waitTimeMs / 1000.0)
    
    print "  [Attempt " + str(attempt) + "] TIMEOUT - " + str(len(elementGraphics)) + "/" + str(totalElements) + " elements"
    return elementGraphics, attempt

def _unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLanes):
    unmaskedCount = 0
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
# MAIN ORCHESTRATION FUNCTION (from v2.7 - best results)
# ============================================================================

def createBPMNFromConfig(parentPackage, config):
    """
    Create a BPMN process diagram from a configuration dictionary.

    Supports two formats:

    1. LANE-RELATIVE POSITIONING (from BPMN_Export):
       "elements": [("Name", TYPE, "Lane", x, y_offset, width, height), ...]
       y_offset is relative to lane top

    2. COLUMN-BASED (standard):
       "elements": [("Name", TYPE, "Lane"), ...]
       "layout": {"Name": column_index, ...}
    """

    executionId = str(int(time.time() * 1000) % 100000)
    processName = config.get("name", "Process") + "_" + executionId
    stepCounter = [0]

    def step():
        stepCounter[0] += 1
        return stepCounter[0]

    cfg = dict(BPMN_DEFAULT_CONFIG)
    for key in ["SPACING", "START_X", "TASK_WIDTH", "TASK_HEIGHT", "WAIT_TIME_MS", "MAX_ATTEMPTS",
                "DATA_WIDTH", "DATA_HEIGHT", "DATA_OFFSET_X", "DATA_OFFSET_Y"]:
        if key in config:
            cfg[key] = config[key]

    # Detect format: lane-relative vs column-based
    elementDefs = config.get("elements", [])
    useLaneRelativePositioning = False
    if elementDefs and len(elementDefs) > 0:
        firstElem = elementDefs[0]
        if len(firstElem) >= 7:
            useLaneRelativePositioning = True

    print ""
    print "=================================================================="
    print "BPMN PROCESS CREATION"
    print "=================================================================="
    print "Process Name: " + processName
    print "Positioning: " + ("LANE-RELATIVE" if useLaneRelativePositioning else "COLUMN-BASED")
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

    # Group elements by lane for lane-by-lane processing
    elementsByLane = {}
    for laneName in laneOrder:
        elementsByLane[laneName] = []

    # Position data for lane-relative positioning
    elementPositions = {}  # name -> (x, y_offset, w, h)

    for elemDef in elementDefs:
        # Support both formats:
        # 3-tuple: (name, type, lane) - column-based layout
        # 7-tuple: (name, type, lane, x, y_offset, w, h) - exact positioning (from export)
        if len(elemDef) >= 7:
            name, elemType, laneName = elemDef[0], elemDef[1], elemDef[2]
            x, yOffset, w, h = elemDef[3], elemDef[4], elemDef[5], elemDef[6]
            elementPositions[name] = (x, yOffset, w, h)
        else:
            name, elemType, laneName = elemDef[0], elemDef[1], elemDef[2]

        elem = _createElement(process, name, elemType)
        if elem:
            if laneName in lanes:
                _addToLane(elem, lanes[laneName])
            elements.append(elem)
            elementRefs[name] = elem
            elementLanes[name] = laneName
            if laneName in elementsByLane:
                elementsByLane[laneName].append(name)
    
    for laneName in laneOrder:
        count = len(elementsByLane[laneName])
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
    dataObjectLayout = {}
    
    if dataObjectDefs:
        print ""
        print "== PHASE 2B: CREATE DATA OBJECTS ================================"
        print ""
        
        for dataDef in dataObjectDefs:
            # Support both formats:
            # 3-tuple: (name, lane, column) - column-based layout
            # 6-tuple: (name, lane, x, y_offset, w, h) - exact positioning (from export)
            if len(dataDef) >= 6:
                name, laneName = dataDef[0], dataDef[1]
                x, yOffset, w, h = dataDef[2], dataDef[3], dataDef[4], dataDef[5]
                elementPositions[name] = (x, yOffset, w, h)
                column = 0  # Placeholder, not used with extended positioning
            else:
                name, laneName, column = dataDef[0], dataDef[1], dataDef[2]

            try:
                dataObj = _createDataObject(process, name)
                if dataObj:
                    if laneName in lanes:
                        _addToLane(dataObj, lanes[laneName])
                    dataObjects.append(dataObj)
                    dataObjectRefs[name] = dataObj
                    dataObjectLanes[name] = laneName
                    dataObjectLayout[name] = column
                    elementRefs[name] = dataObj
                    elementLanes[name] = laneName
                    # Add to lane grouping for lane-by-lane processing
                    if laneName in elementsByLane:
                        elementsByLane[laneName].append(name)
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
    # PHASE 4 & 5: UNMASK AND POSITION ELEMENTS
    # =========================================================================
    print ""
    print "== PHASE 4 & 5: UNMASK AND POSITION ELEMENTS ====================="
    print ""

    allElements = elements + dataObjects
    elementGraphics = {}
    repositionedCount = 0
    relativeOffsets = {}

    if useLaneRelativePositioning:
        # =====================================================================
        # LANE-BY-LANE POSITIONING (for export/import - exact recreation)
        # =====================================================================
        print "Mode: LANE-BY-LANE (exact positioning from export)"
        print ""

        for laneName in laneOrder:
            # Get current lane bounds
            laneBounds = _getBounds(diagramHandle, lanes[laneName])
            if not laneBounds:
                print "[" + laneName + "] WARNING: Could not get lane bounds"
                continue

            laneTop = laneBounds["y"]
            print "[" + laneName + "] Lane top Y = " + str(int(laneTop))

            # Get elements for this lane
            laneElementNames = elementsByLane.get(laneName, [])
            if not laneElementNames:
                continue

            # Get element objects for this lane
            laneElements = [elementRefs[n] for n in laneElementNames if n in elementRefs]

            # Wait for / unmask elements in this lane
            for elem in laneElements:
                name = elem.getName()
                dg = _getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
                else:
                    # Manual unmask into this lane
                    try:
                        targetY = int(laneTop + laneBounds["h"] / 2)
                        result = diagramHandle.unmask(elem, 100, targetY)
                        if result and result.size() > 0:
                            elementGraphics[name] = result.get(0)
                    except:
                        pass

            # Position elements in this lane
            for name in laneElementNames:
                if name not in elementGraphics:
                    print "  " + name + ": SKIP (no graphics)"
                    continue

                dg = elementGraphics[name]

                # Get position data
                if name not in elementPositions:
                    print "  " + name + ": SKIP (no position data)"
                    continue

                x, yOffset, w, h = elementPositions[name]

                # Apply minimum task size from config (for tasks only)
                elem = elementRefs.get(name)
                if elem:
                    elemClass = elem.getMClass().getName()
                    if "Task" in elemClass:
                        minW = cfg.get("TASK_WIDTH", 120)
                        minH = cfg.get("TASK_HEIGHT", 60)
                        w = max(w, minW)
                        h = max(h, minH)

                # Calculate actual Y: lane top + offset
                actualY = laneTop + yOffset

                newBounds = Draw2DRectangle(int(x), int(actualY), int(w), int(h))
                dg.setBounds(newBounds)
                repositionedCount += 1
                relativeOffsets[name] = yOffset
                print "  " + name + ": (" + str(int(x)) + ", " + str(int(actualY)) + ") " + str(int(w)) + "x" + str(int(h))

            # Save after each lane to allow Modelio to adjust
            diagramHandle.save()
            print ""

    else:
        # =====================================================================
        # COLUMN-BASED POSITIONING (standard - v2.7 logic)
        # =====================================================================
        print "Mode: COLUMN-BASED (standard layout)"
        print ""

        layoutConfig = config.get("layout", {})

        # Wait for all elements
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
        print ""

        def _parseLayoutEntry(entry):
            if isinstance(entry, tuple):
                return entry[0], entry[1]
            else:
                return entry, 0

        sortedElements = []
        for name, layoutEntry in layoutConfig.items():
            col, yOffset = _parseLayoutEntry(layoutEntry)
            laneName = elementLanes.get(name, "")
            sortedElements.append((col, yOffset, name, laneName))
        sortedElements.sort()

        spacing = cfg["SPACING"]
        startX = cfg["START_X"]
        taskWidth = cfg["TASK_WIDTH"]
        taskHeight = cfg["TASK_HEIGHT"]
        taskTopOffset = 20

        for col, yOffset, name, laneName in sortedElements:
            if name not in elementGraphics:
                continue

            laneBoundsDict = {}
            for ln in laneOrder:
                lb = _getBounds(diagramHandle, lanes[ln])
                if lb:
                    laneBoundsDict[ln] = {"top": lb["y"], "bottom": lb["y"] + lb["h"], "height": lb["h"]}

            if laneName not in laneBoundsDict:
                print "  " + name + ": SKIP (lane bounds not found)"
                continue

            laneTop = laneBoundsDict[laneName]["top"]

            dg = elementGraphics[name]
            elem = elementRefs[name]
            bounds = _getBounds(diagramHandle, elem)

            if not bounds:
                continue

            targetX = startX + spacing * col
            targetY = laneTop + taskTopOffset + yOffset

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

            freshBounds = _getBounds(diagramHandle, elem)
            if freshBounds:
                freshLaneBounds = _getBounds(diagramHandle, lanes[laneName])
                if freshLaneBounds:
                    freshLaneTop = freshLaneBounds["y"]
                    relativeY = freshBounds["y"] - freshLaneTop
                    relativeOffsets[name] = relativeY
                    print "  " + name + " -> col=" + str(col) + " Y=" + str(int(freshBounds["y"])) + " (relY=" + str(int(relativeY)) + " laneTop=" + str(int(freshLaneTop)) + ")"

        print ""
        print "  Relative Y offsets (element Y - lane top):"
        for ln in laneOrder:
            laneElems = [(n, relativeOffsets.get(n, "?")) for n in relativeOffsets.keys() if elementLanes.get(n) == ln]
            if laneElems:
                offsetStrs = [n + "=" + str(int(o) if isinstance(o, (int, float)) else o) for n, o in laneElems[:5]]
                print "    " + ln + ": " + ", ".join(offsetStrs) + ("..." if len(laneElems) > 5 else "")

    print ""
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + "/" + str(len(allElements))
    
    # =========================================================================
    # PHASE 5B: REPOSITION DATA OBJECTS (column-based only)
    # =========================================================================
    # Skip for lane-relative positioning - data objects already positioned above
    if dataObjects and not useLaneRelativePositioning:
        print ""
        print "== PHASE 5B: REPOSITION DATA OBJECTS ============================"
        print "(Lane-by-lane with coordinate refresh)"
        print ""

        # Define layout variables for column-based positioning
        layoutConfig = config.get("layout", {})
        spacing = cfg["SPACING"]
        startX = cfg["START_X"]
        taskWidth = cfg["TASK_WIDTH"]
        taskHeight = cfg["TASK_HEIGHT"]
        taskTopOffset = 20
        dataWidth = cfg["DATA_WIDTH"]
        dataHeight = cfg["DATA_HEIGHT"]
        dataOffsetX = cfg["DATA_OFFSET_X"]
        dataOffsetY = cfg["DATA_OFFSET_Y"]

        def _parseLayoutEntry(entry):
            if isinstance(entry, tuple):
                return entry[0], entry[1]
            else:
                return entry, 0

        dataObjectSourceTask = {}
        dataAssocDefs = config.get("data_associations", [])
        dataObjectNames = set(dataObjectLayout.keys())
        
        for assocDef in dataAssocDefs:
            srcName, tgtName = assocDef[0], assocDef[1]
            if tgtName in dataObjectNames and srcName not in dataObjectNames:
                dataObjectSourceTask[tgtName] = srcName
        
        print "  Source task mapping:"
        for doName, taskName in dataObjectSourceTask.items():
            print "    " + doName + " <- " + taskName
        print ""
        
        dataRepositioned = 0
        
        for laneIdx, laneName in enumerate(laneOrder):
            laneHasData = any(dataObjectLanes.get(name) == laneName for name in dataObjectLayout.keys())
            if not laneHasData:
                continue
            
            diagramHandle.save()
            
            allLaneTops = {}
            for ln in laneOrder:
                lnBounds = _getBounds(diagramHandle, lanes[ln])
                if lnBounds:
                    allLaneTops[ln] = lnBounds["y"]
            
            lb = _getBounds(diagramHandle, lanes[laneName])
            if not lb:
                print "[" + laneName + "] ERROR: Could not get lane bounds"
                continue
            
            laneTop = lb["y"]
            laneBottom = lb["y"] + lb["h"]
            laneCenterY = lb["y"] + lb["h"] / 2
            
            print "[" + laneName + "] FRESH bounds: " + str(int(laneTop)) + "-" + str(int(laneBottom)) + " (center=" + str(int(laneCenterY)) + ")"
            
            laneDataCount = 0
            for name, column in dataObjectLayout.items():
                if dataObjectLanes.get(name) != laneName:
                    continue

                if name not in elementGraphics:
                    print "  " + name + ": SKIP (not in graphics)"
                    continue

                dg = elementGraphics[name]

                targetX = startX + spacing * column + dataOffsetX

                sourceTaskName = dataObjectSourceTask.get(name)
                
                if sourceTaskName and sourceTaskName in relativeOffsets:
                    sourceTaskLane = elementLanes.get(sourceTaskName)
                    freshLaneTop = allLaneTops.get(sourceTaskLane, laneTop)
                    sourceRelY = relativeOffsets[sourceTaskName]
                    
                    sourceTaskY = freshLaneTop + sourceRelY
                    sourceTaskH = taskHeight
                    
                    targetY = sourceTaskY + sourceTaskH + dataOffsetY
                    print "  " + name + " (from " + sourceTaskName + " relY=" + str(int(sourceRelY)) + " laneTop=" + str(int(freshLaneTop)) + ") -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
                else:
                    nearestTaskBottom = None
                    minDistance = 999999
                    
                    for elemName in relativeOffsets.keys():
                        if elementLanes.get(elemName) != laneName:
                            continue
                        elemLayout = layoutConfig.get(elemName)
                        if elemLayout:
                            elemCol, elemYOff = _parseLayoutEntry(elemLayout)
                            distance = abs(elemCol - column)
                            if distance < minDistance:
                                minDistance = distance
                                elemRelY = relativeOffsets[elemName]
                                nearestTaskBottom = laneTop + elemRelY + taskHeight
                    
                    if nearestTaskBottom is not None:
                        targetY = nearestTaskBottom + dataOffsetY
                    else:
                        targetY = laneTop + taskTopOffset + taskHeight + dataOffsetY
                    
                    print "  " + name + " (fallback) -> (" + str(int(targetX)) + "," + str(int(targetY)) + ")"
                
                if targetY + dataHeight > laneBottom - 5:
                    targetY = laneBottom - dataHeight - 5

                newBounds = Draw2DRectangle(
                    int(targetX), int(targetY),
                    int(dataWidth), int(dataHeight)
                )
                dg.setBounds(newBounds)
                dataRepositioned += 1
                laneDataCount += 1
            
            if laneDataCount > 0:
                diagramHandle.save()
                print "  [Saved " + str(laneDataCount) + " DOs, refreshing coordinates...]"
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