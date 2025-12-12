#
# BPMN_Export.py
#
# Description:
#   Export a BPMN Process Diagram to a Python configuration file.
#   Captures all elements with their exact positions and sizes.
#   The exported file can be used with BPMN_Import.py to recreate the diagram.
#
# Applicable on: BpmnProcessDesignDiagram, BpmnProcess
#
# Usage:
#   1. Select a BPMN Process Design Diagram (or BpmnProcess) in Modelio
#   2. Run this macro
#   3. A Python file will be printed to the console (copy/paste to save)
#
# Author: Generated for Modelio BPMN workflows
# Version: 1.0 - December 2025
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnTask
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.gateways import BpmnParallelGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
import re

# Try optional imports
try:
    from org.modelio.metamodel.bpmn.activities import BpmnScriptTask
except ImportError:
    BpmnScriptTask = None

try:
    from org.modelio.metamodel.bpmn.activities import BpmnBusinessRuleTask
except ImportError:
    BpmnBusinessRuleTask = None

try:
    from org.modelio.metamodel.bpmn.activities import BpmnSendTask
    from org.modelio.metamodel.bpmn.activities import BpmnReceiveTask
except ImportError:
    BpmnSendTask = None
    BpmnReceiveTask = None

try:
    from org.modelio.metamodel.bpmn.events import BpmnIntermediateCatchEvent
    from org.modelio.metamodel.bpmn.events import BpmnIntermediateThrowEvent
except ImportError:
    BpmnIntermediateCatchEvent = None
    BpmnIntermediateThrowEvent = None

try:
    from org.modelio.metamodel.bpmn.gateways import BpmnInclusiveGateway
    from org.modelio.metamodel.bpmn.gateways import BpmnComplexGateway
    from org.modelio.metamodel.bpmn.gateways import BpmnEventBasedGateway
except ImportError:
    BpmnInclusiveGateway = None
    BpmnComplexGateway = None
    BpmnEventBasedGateway = None

# Try to import Data Object classes
try:
    from org.modelio.metamodel.bpmn.objects import BpmnDataObject
    from org.modelio.metamodel.bpmn.objects import BpmnDataAssociation
    _DATA_OBJECTS_AVAILABLE = True
except ImportError:
    _DATA_OBJECTS_AVAILABLE = False


# ============================================================================
# TYPE DETECTION
# ============================================================================

def getElementType(element):
    """Determine the element type constant string."""
    className = element.getMClass().getName()
    
    # Start Events
    if isinstance(element, BpmnStartEvent):
        # Check for event definitions
        try:
            eventDefs = element.getEventDefinitions()
            if eventDefs and eventDefs.size() > 0:
                defClass = eventDefs.get(0).getMClass().getName()
                if "Message" in defClass:
                    return "MESSAGE_START"
                elif "Timer" in defClass:
                    return "TIMER_START"
                elif "Signal" in defClass:
                    return "SIGNAL_START"
                elif "Conditional" in defClass:
                    return "CONDITIONAL_START"
        except:
            pass
        return "START"
    
    # End Events
    if isinstance(element, BpmnEndEvent):
        try:
            eventDefs = element.getEventDefinitions()
            if eventDefs and eventDefs.size() > 0:
                defClass = eventDefs.get(0).getMClass().getName()
                if "Message" in defClass:
                    return "MESSAGE_END"
                elif "Signal" in defClass:
                    return "SIGNAL_END"
                elif "Terminate" in defClass:
                    return "TERMINATE_END"
                elif "Error" in defClass:
                    return "ERROR_END"
        except:
            pass
        return "END"
    
    # Intermediate Events (if available)
    if BpmnIntermediateCatchEvent and isinstance(element, BpmnIntermediateCatchEvent):
        try:
            eventDefs = element.getEventDefinitions()
            if eventDefs and eventDefs.size() > 0:
                defClass = eventDefs.get(0).getMClass().getName()
                if "Message" in defClass:
                    return "MESSAGE_CATCH"
                elif "Timer" in defClass:
                    return "TIMER_CATCH"
                elif "Signal" in defClass:
                    return "SIGNAL_CATCH"
        except:
            pass
        return "INTERMEDIATE_CATCH"
    
    if BpmnIntermediateThrowEvent and isinstance(element, BpmnIntermediateThrowEvent):
        try:
            eventDefs = element.getEventDefinitions()
            if eventDefs and eventDefs.size() > 0:
                defClass = eventDefs.get(0).getMClass().getName()
                if "Message" in defClass:
                    return "MESSAGE_THROW"
                elif "Signal" in defClass:
                    return "SIGNAL_THROW"
        except:
            pass
        return "INTERMEDIATE_THROW"
    
    # Tasks - check specific types first
    if isinstance(element, BpmnUserTask):
        return "USER_TASK"
    if isinstance(element, BpmnServiceTask):
        return "SERVICE_TASK"
    if isinstance(element, BpmnManualTask):
        return "MANUAL_TASK"
    if BpmnScriptTask and isinstance(element, BpmnScriptTask):
        return "SCRIPT_TASK"
    if BpmnBusinessRuleTask and isinstance(element, BpmnBusinessRuleTask):
        return "BUSINESS_RULE_TASK"
    if BpmnSendTask and isinstance(element, BpmnSendTask):
        return "SEND_TASK"
    if BpmnReceiveTask and isinstance(element, BpmnReceiveTask):
        return "RECEIVE_TASK"
    if isinstance(element, BpmnTask):
        return "TASK"  # Generic task
    
    # Gateways
    if isinstance(element, BpmnExclusiveGateway):
        return "EXCLUSIVE_GW"
    if isinstance(element, BpmnParallelGateway):
        return "PARALLEL_GW"
    if BpmnInclusiveGateway and isinstance(element, BpmnInclusiveGateway):
        return "INCLUSIVE_GW"
    if BpmnComplexGateway and isinstance(element, BpmnComplexGateway):
        return "COMPLEX_GW"
    if BpmnEventBasedGateway and isinstance(element, BpmnEventBasedGateway):
        return "EVENT_BASED_GW"
    
    # Data Objects
    if _DATA_OBJECTS_AVAILABLE and isinstance(element, BpmnDataObject):
        return "DATA_OBJECT"
    
    return "UNKNOWN"


def findLaneForElement(element, lanes):
    """Find which lane contains the element."""
    for laneName, lane in lanes.items():
        flowElements = lane.getFlowElementRef()
        if flowElements:
            for flowElem in flowElements:
                if flowElem.getUuid() == element.getUuid():
                    return laneName
    return None


# ============================================================================
# BOUNDS PARSING
# ============================================================================

def parseBounds(boundsStr):
    """Parse a Rectangle bounds string into a dictionary."""
    match = re.search(
        r'Rectangle\((-?[0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+)\)',
        str(boundsStr)
    )
    if match:
        return {
            "x": int(float(match.group(1))),
            "y": int(float(match.group(2))),
            "w": int(float(match.group(3))),
            "h": int(float(match.group(4)))
        }
    return None


def getGraphicBounds(diagramHandle, element):
    """Get bounds of an element in the diagram."""
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics and graphics.size() > 0:
            dg = graphics.get(0)
            bounds = dg.getBounds()
            return parseBounds(bounds)
    except Exception as e:
        pass
    return None


# ============================================================================
# EXPORT FUNCTION
# ============================================================================

def exportBPMNProcess(process, diagram):
    """
    Export a BPMN process to a configuration dictionary format.
    """
    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    
    # Collect lanes
    lanes = {}
    laneOrder = []
    
    # getLaneSet() may return a single LaneSet or a collection
    try:
        laneSets = process.getLaneSet()
        if laneSets:
            # Try to iterate (if it's a collection)
            try:
                for laneSet in laneSets:
                    for lane in laneSet.getLane():
                        laneName = lane.getName()
                        lanes[laneName] = lane
                        laneOrder.append(laneName)
            except TypeError:
                # It's a single LaneSet, not a collection
                laneSet = laneSets
                for lane in laneSet.getLane():
                    laneName = lane.getName()
                    lanes[laneName] = lane
                    laneOrder.append(laneName)
    except Exception as e:
        print "Warning: Could not get lanes: " + str(e)
    
    # Get lane bounds and sort by Y position
    laneBounds = {}
    for laneName, lane in lanes.items():
        bounds = getGraphicBounds(diagramHandle, lane)
        if bounds:
            laneBounds[laneName] = bounds
    
    # Sort by Y coordinate
    laneOrder = sorted(laneOrder, key=lambda ln: laneBounds.get(ln, {}).get("y", 9999))
    
    print "Lanes found: " + str(len(laneOrder))
    for laneName in laneOrder:
        lb = laneBounds.get(laneName, {})
        print "  " + laneName + ": y=" + str(lb.get("y", "?")) + ", h=" + str(lb.get("h", "?"))
    
    # Collect elements
    elements = []
    elementBounds = {}
    elementNameMap = {}  # UUID -> name (handles renames for duplicates)
    flowElements = process.getFlowElement()
    
    for elem in flowElements:
        elemType = getElementType(elem)
        if elemType == "UNKNOWN":
            continue
        
        # Skip sequence flows (handled separately)
        if isinstance(elem, BpmnSequenceFlow):
            continue
        
        # Skip data associations
        if _DATA_OBJECTS_AVAILABLE:
            try:
                if isinstance(elem, BpmnDataAssociation):
                    continue
            except:
                pass
        
        name = elem.getName()
        laneName = findLaneForElement(elem, lanes)
        bounds = getGraphicBounds(diagramHandle, elem)
        
        # Handle duplicate names by adding suffix
        originalName = name
        counter = 2
        while name in elementBounds:
            name = originalName + "_" + str(counter)
            counter += 1
        
        # Track the mapping from element UUID to final name
        try:
            elementNameMap[elem.getUuid()] = name
        except:
            elementNameMap[id(elem)] = name
        
        if bounds:
            elementBounds[name] = bounds
            
            # Calculate Y offset from lane top
            yOffset = bounds["y"]
            if laneName and laneName in laneBounds:
                laneTop = laneBounds[laneName]["y"]
                yOffset = bounds["y"] - laneTop
            
            if elemType == "DATA_OBJECT":
                elements.append({
                    "name": name,
                    "type": elemType,
                    "lane": laneName,
                    "x": bounds["x"],
                    "y_offset": yOffset,  # Y offset from lane top
                    "w": bounds["w"],
                    "h": bounds["h"],
                    "is_data": True
                })
            else:
                elements.append({
                    "name": name,
                    "type": elemType,
                    "lane": laneName,
                    "x": bounds["x"],
                    "y_offset": yOffset,  # Y offset from lane top
                    "w": bounds["w"],
                    "h": bounds["h"],
                    "is_data": False
                })
    
    # Sort elements by X then Y_offset for consistent ordering
    elements.sort(key=lambda e: (e["x"], e["y_offset"]))
    
    # Collect sequence flows
    flows = []
    for elem in flowElements:
        if isinstance(elem, BpmnSequenceFlow):
            srcElem = elem.getSourceRef()
            tgtElem = elem.getTargetRef()
            
            # Get the (possibly renamed) element names
            srcName = ""
            tgtName = ""
            if srcElem:
                try:
                    srcName = elementNameMap.get(srcElem.getUuid(), srcElem.getName())
                except:
                    srcName = elementNameMap.get(id(srcElem), srcElem.getName())
            if tgtElem:
                try:
                    tgtName = elementNameMap.get(tgtElem.getUuid(), tgtElem.getName())
                except:
                    tgtName = elementNameMap.get(id(tgtElem), tgtElem.getName())
            
            guard = elem.getName() if elem.getName() else ""
            if not guard:
                try:
                    guard = elem.getConditionExpression() if elem.getConditionExpression() else ""
                except:
                    pass
            flows.append((srcName, tgtName, guard))
    
    # Collect data associations
    dataAssociations = []
    if _DATA_OBJECTS_AVAILABLE:
        for elem in flowElements:
            try:
                if isinstance(elem, BpmnDataAssociation):
                    srcRef = elem.getSourceRef()
                    tgtRef = elem.getTargetRef()
                    startingAct = elem.getStartingActivity()
                    endingAct = elem.getEndingActivity()
                    
                    # Determine source and target names
                    if startingAct:
                        # Output: Task -> DataObject
                        srcName = startingAct.getName()
                        tgtName = tgtRef.getName() if tgtRef else ""
                    elif endingAct:
                        # Input: DataObject -> Task
                        srcName = srcRef.get(0).getName() if srcRef and srcRef.size() > 0 else ""
                        tgtName = endingAct.getName()
                    else:
                        continue
                    
                    if srcName and tgtName:
                        dataAssociations.append((srcName, tgtName))
            except Exception as e:
                pass
    
    # Collect lane bounds
    laneBoundsList = []
    for laneName in laneOrder:
        bounds = laneBounds.get(laneName)
        if bounds:
            laneBoundsList.append({
                "name": laneName,
                "y": bounds["y"],
                "h": bounds["h"]
            })
    
    diagramHandle.close()
    
    return {
        "name": process.getName(),
        "lanes": laneOrder,
        "lane_bounds": laneBoundsList,
        "elements": elements,
        "flows": flows,
        "data_associations": dataAssociations
    }


def formatPythonOutput(config):
    """Format the configuration as a Python file."""
    
    elements = config["elements"]
    lane_bounds = config["lane_bounds"]
    
    # Normalize X coordinates only (Y is now relative to lane)
    if elements:
        minX = min(e["x"] for e in elements)
        offsetX = 50 - minX
        
        for e in elements:
            e["x"] = e["x"] + offsetX
    
    output = []
    output.append("#")
    output.append("# " + config["name"] + "_Exported.py")
    output.append("#")
    output.append("# Description: Exported BPMN process configuration")
    output.append("#              Generated by BPMN_Export.py")
    output.append("#")
    output.append("# Applicable on: Package")
    output.append("#")
    output.append("")
    output.append("from org.modelio.metamodel.uml.statik import Package")
    output.append("")
    output.append("# Load helper library")
    output.append('execfile(".modelio/5.4/macros/BPMN_Helpers_v2.py")')
    output.append("")
    output.append("CONFIG = {")
    output.append('    "name": "' + config["name"] + '",')
    output.append("")
    
    # Lanes
    output.append("    # Lanes (top to bottom)")
    output.append("    \"lanes\": [")
    for laneName in config["lanes"]:
        output.append('        "' + laneName + '",')
    output.append("    ],")
    output.append("")
    
    # Lane bounds (for reference only)
    output.append("    # Lane bounds - reference only (y, height from original)")
    output.append("    \"lane_bounds\": [")
    for lb in config["lane_bounds"]:
        output.append('        {"name": "' + lb["name"] + '", "h": ' + str(lb["h"]) + '},')
    output.append("    ],")
    output.append("")
    
    # Elements
    output.append("    # Elements: (name, type, lane, x, y_offset, width, height)")
    output.append("    # y_offset is relative to lane top")
    output.append("    \"elements\": [")
    
    # Separate data objects
    regularElements = [e for e in config["elements"] if not e.get("is_data", False)]
    dataElements = [e for e in config["elements"] if e.get("is_data", False)]
    
    for elem in regularElements:
        lanePart = '"' + elem["lane"] + '"' if elem["lane"] else "None"
        line = '        ("' + elem["name"] + '", ' + elem["type"] + ', ' + lanePart + ', '
        line += str(elem["x"]) + ', ' + str(elem["y_offset"]) + ', ' + str(elem["w"]) + ', ' + str(elem["h"]) + '),'
        output.append(line)
    output.append("    ],")
    output.append("")
    
    # Data objects (if any)
    if dataElements:
        output.append("    # Data Objects: (name, lane, x, y_offset, width, height)")
        output.append("    \"data_objects\": [")
        for elem in dataElements:
            lanePart = '"' + elem["lane"] + '"' if elem["lane"] else "None"
            line = '        ("' + elem["name"] + '", ' + lanePart + ', '
            line += str(elem["x"]) + ', ' + str(elem["y_offset"]) + ', ' + str(elem["w"]) + ', ' + str(elem["h"]) + '),'
            output.append(line)
        output.append("    ],")
        output.append("")
    
    # Flows
    output.append("    # Sequence Flows: (source, target, guard)")
    output.append("    \"flows\": [")
    for src, tgt, guard in config["flows"]:
        output.append('        ("' + src + '", "' + tgt + '", "' + guard + '"),')
    output.append("    ],")
    output.append("")
    
    # Data associations (if any)
    if config["data_associations"]:
        output.append("    # Data Associations: (source, target)")
        output.append("    \"data_associations\": [")
        for src, tgt in config["data_associations"]:
            output.append('        ("' + src + '", "' + tgt + '"),')
        output.append("    ],")
    
    output.append("}")
    output.append("")
    output.append("# ============================================================================")
    output.append("# Entry Point")
    output.append("# ============================================================================")
    output.append("if (selectedElements.size > 0):")
    output.append("    element = selectedElements.get(0)")
    output.append("    if (isinstance(element, Package)):")
    output.append("        createBPMNFromConfig(element, CONFIG)")
    output.append("    else:")
    output.append('        print "ERROR: Please select a Package."')
    output.append("else:")
    output.append('    print "ERROR: Please select a Package first."')
    
    return "\n".join(output)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def isDiagram(element):
    """Check if element is a BPMN diagram by metaclass name."""
    try:
        mcName = element.getMClass().getName()
        return "Diagram" in mcName and "Bpmn" in mcName
    except:
        return False

if (selectedElements.size > 0):
    selected = selectedElements.get(0)
    
    process = None
    diagram = None
    
    # Check what was selected using metaclass name
    mcName = selected.getMClass().getName()
    
    if isDiagram(selected):
        diagram = selected
        # Get process from diagram origin
        try:
            process = diagram.getOrigin()
        except:
            pass
    elif isinstance(selected, BpmnProcess):
        process = selected
        # Find associated diagram
        try:
            for d in process.getProduct():
                if isDiagram(d):
                    diagram = d
                    break
        except:
            pass
    
    if process and diagram:
        print "=================================================================="
        print "BPMN EXPORT"
        print "=================================================================="
        print "Process: " + process.getName()
        print "Diagram: " + diagram.getName()
        print "=================================================================="
        print ""
        
        config = exportBPMNProcess(process, diagram)
        pythonCode = formatPythonOutput(config)
        
        print "=== EXPORTED CONFIGURATION (copy below) ==="
        print ""
        print pythonCode
        print ""
        print "=== END OF EXPORT ==="
        
        # Summary
        print ""
        print "Summary:"
        print "  Lanes: " + str(len(config["lanes"]))
        print "  Elements: " + str(len(config["elements"]))
        print "  Flows: " + str(len(config["flows"]))
        if config["data_associations"]:
            print "  Data Associations: " + str(len(config["data_associations"]))
    elif process and not diagram:
        print "ERROR: Found process but no diagram."
        print "Please select a BPMN diagram directly."
    else:
        print "ERROR: Could not find both process and diagram."
        print "Please select a BpmnProcessDesignDiagram or BpmnProcess."
        print "Selected element type: " + mcName
else:
    print "ERROR: Please select a BPMN diagram or process first."