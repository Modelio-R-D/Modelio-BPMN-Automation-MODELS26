#
# BPMN_Helpers.py
#
# Description:
#   Enhanced helper library for creating BPMN process diagrams in Modelio.
#   Supports ABSOLUTE POSITIONING for exact diagram recreation.
#   Use with BPMN_Export.py for diagram cloning/migration.
#
#   Place this file in: .modelio/5.4/macros/BPMN_Helpers_v2.py
#   Load from scripts with: execfile(".modelio/5.4/macros/BPMN_Helpers_v2.py")
#
# Version: 3.0 - December 2025
#   - Added absolute positioning support
#   - Added more element types (Script, BusinessRule, Send, Receive tasks)
#   - Added more event types (Intermediate, Signal, etc.)
#   - Added more gateway types (Inclusive, Complex, EventBased)
#   - Backward compatible with column-based layout
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

# Try to import additional task types
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

# Try to import additional gateway types
try:
    from org.modelio.metamodel.bpmn.gateways import BpmnInclusiveGateway
    from org.modelio.metamodel.bpmn.gateways import BpmnComplexGateway
    from org.modelio.metamodel.bpmn.gateways import BpmnEventBasedGateway
    _ADDITIONAL_GATEWAYS_AVAILABLE = True
except ImportError:
    _ADDITIONAL_GATEWAYS_AVAILABLE = False

# Try to import intermediate events
try:
    from org.modelio.metamodel.bpmn.events import BpmnIntermediateCatchEvent
    from org.modelio.metamodel.bpmn.events import BpmnIntermediateThrowEvent
    _INTERMEDIATE_EVENTS_AVAILABLE = True
except ImportError:
    _INTERMEDIATE_EVENTS_AVAILABLE = False

# Try to import Data Object classes
try:
    from org.modelio.metamodel.bpmn.objects import BpmnDataObject
    from org.modelio.metamodel.bpmn.objects import BpmnDataAssociation
    _DATA_OBJECTS_AVAILABLE = True
except ImportError:
    _DATA_OBJECTS_AVAILABLE = False

print "BPMN_Helpers_v2.py loaded"
print "  Data Objects: " + str(_DATA_OBJECTS_AVAILABLE)
print "  Script Task: " + str(_SCRIPT_TASK_AVAILABLE)
print "  Additional Gateways: " + str(_ADDITIONAL_GATEWAYS_AVAILABLE)


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
    "DATA_OFFSET_X": 20,
    "DATA_OFFSET_Y": 80,
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
    """Create a BPMN Lane."""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def _addToLane(element, lane):
    """Assign an element to a lane."""
    try:
        lane.getFlowElementRef().add(element)
        return True
    except:
        return False


# --- Start Events ---

def _createStartEvent(process, name):
    """Create a BPMN Start Event."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def _createMessageStartEvent(process, name):
    """Create a BPMN Message Start Event."""
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
    """Create a BPMN Timer Start Event."""
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
    """Create a BPMN Signal Start Event."""
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
    """Create a BPMN Conditional Start Event."""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        condDef = modelingSession.getModel().createBpmnConditionalEventDefinition()
        condDef.setDefined(event)
    except:
        pass
    return event


# --- End Events ---

def _createEndEvent(process, name):
    """Create a BPMN End Event."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def _createMessageEndEvent(process, name):
    """Create a BPMN Message End Event."""
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
    """Create a BPMN Signal End Event."""
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
    """Create a BPMN Terminate End Event."""
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
    """Create a BPMN Error End Event."""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    try:
        errDef = modelingSession.getModel().createBpmnErrorEventDefinition()
        errDef.setDefined(event)
    except:
        pass
    return event


# --- Intermediate Events ---

def _createIntermediateCatchEvent(process, name):
    """Create a BPMN Intermediate Catch Event."""
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        print "WARNING: Intermediate events not available, creating generic event"
        return _createStartEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateCatchEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def _createIntermediateThrowEvent(process, name):
    """Create a BPMN Intermediate Throw Event."""
    if not _INTERMEDIATE_EVENTS_AVAILABLE:
        print "WARNING: Intermediate events not available, creating generic event"
        return _createEndEvent(process, name)
    event = modelingSession.getModel().createBpmnIntermediateThrowEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def _createMessageCatchEvent(process, name):
    """Create a BPMN Message Catch Event."""
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
    """Create a BPMN Message Throw Event."""
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
    """Create a BPMN Timer Catch Event."""
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
    """Create a BPMN Signal Catch Event."""
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
    """Create a BPMN Signal Throw Event."""
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


# --- Tasks ---

def _createTask(process, name):
    """Create a generic BPMN Task."""
    task = modelingSession.getModel().createBpmnTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createUserTask(process, name):
    """Create a BPMN User Task."""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createServiceTask(process, name):
    """Create a BPMN Service Task."""
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createManualTask(process, name):
    """Create a BPMN Manual Task."""
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createScriptTask(process, name):
    """Create a BPMN Script Task."""
    if not _SCRIPT_TASK_AVAILABLE:
        print "WARNING: Script Task not available, creating Service Task"
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnScriptTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createBusinessRuleTask(process, name):
    """Create a BPMN Business Rule Task."""
    if not _BUSINESS_RULE_TASK_AVAILABLE:
        print "WARNING: Business Rule Task not available, creating Service Task"
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnBusinessRuleTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createSendTask(process, name):
    """Create a BPMN Send Task."""
    if not _SEND_RECEIVE_AVAILABLE:
        print "WARNING: Send Task not available, creating Service Task"
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnSendTask()
    task.setName(name)
    task.setContainer(process)
    return task


def _createReceiveTask(process, name):
    """Create a BPMN Receive Task."""
    if not _SEND_RECEIVE_AVAILABLE:
        print "WARNING: Receive Task not available, creating Service Task"
        return _createServiceTask(process, name)
    task = modelingSession.getModel().createBpmnReceiveTask()
    task.setName(name)
    task.setContainer(process)
    return task


# --- Gateways ---

def _createExclusiveGateway(process, name):
    """Create a BPMN Exclusive Gateway."""
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def _createParallelGateway(process, name):
    """Create a BPMN Parallel Gateway."""
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def _createInclusiveGateway(process, name):
    """Create a BPMN Inclusive Gateway."""
    if not _ADDITIONAL_GATEWAYS_AVAILABLE:
        print "WARNING: Inclusive Gateway not available, creating Exclusive Gateway"
        return _createExclusiveGateway(process, name)
    gateway = modelingSession.getModel().createBpmnInclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def _createComplexGateway(process, name):
    """Create a BPMN Complex Gateway."""
    if not _ADDITIONAL_GATEWAYS_AVAILABLE:
        print "WARNING: Complex Gateway not available, creating Exclusive Gateway"
        return _createExclusiveGateway(process, name)
    gateway = modelingSession.getModel().createBpmnComplexGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


def _createEventBasedGateway(process, name):
    """Create a BPMN Event-Based Gateway."""
    if not _ADDITIONAL_GATEWAYS_AVAILABLE:
        print "WARNING: Event-Based Gateway not available, creating Exclusive Gateway"
        return _createExclusiveGateway(process, name)
    gateway = modelingSession.getModel().createBpmnEventBasedGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway


# --- Data Objects ---

def _createDataObject(process, name):
    """Create a BPMN Data Object."""
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


# --- Flows ---

def _createSequenceFlow(process, source, target, guard=""):
    """Create a BPMN Sequence Flow."""
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
    """Create a BPMN Data Association."""
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


# Element type to creator mapping
_ELEMENT_CREATORS = {
    # Start events
    START: _createStartEvent,
    MESSAGE_START: _createMessageStartEvent,
    TIMER_START: _createTimerStartEvent,
    SIGNAL_START: _createSignalStartEvent,
    CONDITIONAL_START: _createConditionalStartEvent,
    
    # End events
    END: _createEndEvent,
    MESSAGE_END: _createMessageEndEvent,
    SIGNAL_END: _createSignalEndEvent,
    TERMINATE_END: _createTerminateEndEvent,
    ERROR_END: _createErrorEndEvent,
    
    # Intermediate events
    INTERMEDIATE_CATCH: _createIntermediateCatchEvent,
    INTERMEDIATE_THROW: _createIntermediateThrowEvent,
    MESSAGE_CATCH: _createMessageCatchEvent,
    MESSAGE_THROW: _createMessageThrowEvent,
    TIMER_CATCH: _createTimerCatchEvent,
    SIGNAL_CATCH: _createSignalCatchEvent,
    SIGNAL_THROW: _createSignalThrowEvent,
    
    # Tasks
    TASK: _createTask,
    USER_TASK: _createUserTask,
    SERVICE_TASK: _createServiceTask,
    MANUAL_TASK: _createManualTask,
    SCRIPT_TASK: _createScriptTask,
    BUSINESS_RULE_TASK: _createBusinessRuleTask,
    SEND_TASK: _createSendTask,
    RECEIVE_TASK: _createReceiveTask,
    
    # Gateways
    EXCLUSIVE_GW: _createExclusiveGateway,
    PARALLEL_GW: _createParallelGateway,
    INCLUSIVE_GW: _createInclusiveGateway,
    COMPLEX_GW: _createComplexGateway,
    EVENT_BASED_GW: _createEventBasedGateway,
    
    # Data
    DATA_OBJECT: _createDataObject,
}


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
    """Parse a Rectangle bounds string."""
    match = re.search(
        r'Rectangle\((-?[0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+)\)',
        str(boundsStr)
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
    """Get diagram graphics for an element."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None


def _getBounds(diagramHandle, element):
    """Get bounds of an element."""
    dg = _getGraphics(diagramHandle, element)
    if dg:
        return _parseBounds(str(dg.getBounds()))
    return None


def _getLaneCenterY(diagramHandle, lane):
    """Get center Y position of a lane."""
    bounds = _getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None


# ============================================================================
# WAITING FOR AUTO-UNMASK
# ============================================================================

def _waitForElements(diagramHandle, elements, config):
    """Wait until all elements are available."""
    elementGraphics = {}
    attempt = 0
    maxAttempts = config.get("MAX_ATTEMPTS", 3)
    waitTimeMs = config.get("WAIT_TIME_MS", 50)
    
    while attempt < maxAttempts:
        attempt += 1
        for elem in elements:
            name = elem.getName()
            if name not in elementGraphics:
                dg = _getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
        
        if len(elementGraphics) == len(elements):
            print "  [Attempt " + str(attempt) + "] All " + str(len(elements)) + " elements ready"
            return elementGraphics, attempt
        
        time.sleep(waitTimeMs / 1000.0)
    
    return elementGraphics, attempt


def _unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLanes):
    """Unmask elements that weren't auto-unmasked."""
    unmaskedCount = 0
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = _getBounds(diagramHandle, lane)
        if bounds:
            laneY[laneName] = int(bounds["y"] + bounds["h"] / 2)
    
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
            except:
                pass
    
    return unmaskedCount


# ============================================================================
# MAIN CREATION FUNCTION - LANE-RELATIVE POSITIONING
# ============================================================================

def createBPMNFromConfig(parentPackage, config):
    """
    Create a BPMN process from configuration.
    
    Supports two formats:
    
    1. LANE-RELATIVE POSITIONING (from BPMN_Export v2):
       "elements": [("Name", TYPE, "Lane", x, y_offset, width, height), ...]
       y_offset is relative to lane top
       
    2. COLUMN-BASED (backward compatible):
       "elements": [("Name", TYPE, "Lane"), ...]
       "layout": {"Name": column_index, ...}
    """
    
    executionId = str(int(time.time() * 1000) % 100000)
    processName = config.get("name", "Process") + "_" + executionId
    stepCounter = [0]
    
    def step():
        stepCounter[0] += 1
        return stepCounter[0]
    
    # Merge with defaults
    cfg = dict(BPMN_DEFAULT_CONFIG)
    for key in BPMN_DEFAULT_CONFIG.keys():
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
    # PHASE 2: CREATE ALL ELEMENTS (but don't position yet)
    # =========================================================================
    print ""
    print "== PHASE 2: CREATE ELEMENTS ====================================="
    print ""
    
    elements = []
    elementRefs = {}
    elementLanes = {}
    elementPositions = {}  # name -> (x, y_offset, w, h)
    
    # Group elements by lane for lane-by-lane processing
    elementsByLane = {}
    for laneName in laneOrder:
        elementsByLane[laneName] = []
    
    for elemDef in elementDefs:
        if useLaneRelativePositioning:
            name, elemType, laneName, x, yOffset, w, h = elemDef[0], elemDef[1], elemDef[2], elemDef[3], elemDef[4], elemDef[5], elemDef[6]
            elementPositions[name] = (x, yOffset, w, h)
        else:
            name, elemType, laneName = elemDef[0], elemDef[1], elemDef[2]
        
        elem = _createElement(process, name, elemType)
        if elem:
            if laneName and laneName in lanes:
                _addToLane(elem, lanes[laneName])
            elements.append(elem)
            elementRefs[name] = elem
            elementLanes[name] = laneName
            
            # Group by lane
            if laneName in elementsByLane:
                elementsByLane[laneName].append(name)
    
    print "[" + str(step()) + "] Created " + str(len(elements)) + " elements"
    
    # Log elements per lane
    for laneName in laneOrder:
        count = len(elementsByLane.get(laneName, []))
        print "  " + laneName + ": " + str(count) + " elements"
    
    # =========================================================================
    # PHASE 2B: CREATE DATA OBJECTS
    # =========================================================================
    dataObjectDefs = config.get("data_objects", [])
    dataObjects = []
    dataObjectPositions = {}
    
    if dataObjectDefs:
        print ""
        print "== PHASE 2B: CREATE DATA OBJECTS ================================"
        print ""
        
        for dataDef in dataObjectDefs:
            if len(dataDef) >= 6:
                # Lane-relative: (name, lane, x, y_offset, w, h)
                name, laneName, x, yOffset, w, h = dataDef[0], dataDef[1], dataDef[2], dataDef[3], dataDef[4], dataDef[5]
                dataObjectPositions[name] = (x, yOffset, w, h)
            else:
                # Column-based: (name, lane, column)
                name, laneName, column = dataDef[0], dataDef[1], dataDef[2]
            
            dataObj = _createDataObject(process, name)
            if dataObj:
                if laneName and laneName in lanes:
                    _addToLane(dataObj, lanes[laneName])
                dataObjects.append(dataObj)
                elementRefs[name] = dataObj
                elementLanes[name] = laneName
                
                # Group by lane
                if laneName in elementsByLane:
                    elementsByLane[laneName].append(name)
        
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
    # PHASE 4 & 5: LANE-BY-LANE UNMASK AND POSITION
    # =========================================================================
    print ""
    print "== PHASE 4 & 5: LANE-BY-LANE POSITIONING ========================="
    print ""
    
    allElements = elements + dataObjects
    elementGraphics = {}
    repositionedCount = 0
    
    if useLaneRelativePositioning:
        # LANE-BY-LANE POSITIONING (top to bottom)
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
            
            # Wait for / unmask elements in this lane
            laneElements = [elementRefs[n] for n in laneElementNames if n in elementRefs]
            
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
                if name in elementPositions:
                    x, yOffset, w, h = elementPositions[name]
                elif name in dataObjectPositions:
                    x, yOffset, w, h = dataObjectPositions[name]
                else:
                    continue
                
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
                print "  " + name + ": (" + str(int(x)) + ", " + str(int(actualY)) + ") " + str(int(w)) + "x" + str(int(h))
            
            # Save after each lane to allow Modelio to adjust
            diagramHandle.save()
            print ""
    
    else:
        # COLUMN-BASED POSITIONING (backward compatible)
        print "Using column-based positioning..."
        
        # Wait for all elements
        elementGraphics, attempts = _waitForElements(diagramHandle, allElements, cfg)
        
        if len(elementGraphics) < len(allElements):
            _unmaskMissingElements(diagramHandle, allElements, elementGraphics, lanes, elementLanes)
            diagramHandle.save()
        
        layoutConfig = config.get("layout", {})
        spacing = cfg["SPACING"]
        startX = cfg["START_X"]
        taskWidth = cfg["TASK_WIDTH"]
        taskHeight = cfg["TASK_HEIGHT"]
        
        # Get lane Y values
        laneY = {}
        for laneName in laneOrder:
            y = _getLaneCenterY(diagramHandle, lanes[laneName])
            if y:
                laneY[laneName] = y
        
        for name, col in layoutConfig.items():
            if name not in elementGraphics:
                continue
            
            dg = elementGraphics[name]
            elem = elementRefs[name]
            laneName = elementLanes.get(name, "")
            
            targetX = startX + spacing * col
            targetY = laneY.get(laneName, 100)
            
            bounds = _getBounds(diagramHandle, elem)
            elemClass = elem.getMClass().getName()
            if "Task" in elemClass:
                width = taskWidth
                height = taskHeight
            elif bounds:
                width = bounds["w"]
                height = bounds["h"]
            else:
                width = 30
                height = 30
            
            newBounds = Draw2DRectangle(int(targetX), int(targetY), int(width), int(height))
            dg.setBounds(newBounds)
            repositionedCount += 1
        
        diagramHandle.save()
    
    print "[" + str(step()) + "] Repositioned: " + str(repositionedCount) + " elements"
    
    # =========================================================================
    # PHASE 6: CREATE FLOWS
    # =========================================================================
    print ""
    print "== PHASE 6: CREATE FLOWS ========================================"
    print ""
    
    flowDefs = config.get("flows", [])
    flows = []
    
    for flowDef in flowDefs:
        srcName, tgtName, guard = flowDef[0], flowDef[1], flowDef[2] if len(flowDef) > 2 else ""
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
            if src and tgt:
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