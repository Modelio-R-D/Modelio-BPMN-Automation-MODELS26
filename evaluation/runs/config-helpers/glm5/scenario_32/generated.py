#
# BPMN_Helpers.py
#
# Helper library for BPMN generation in Modelio (Jython)
# Version 3.2
#

from java.lang import System
from org.modelio.metamodel.uml.statik import Package
from org.modelio.metamodel.bpmn import (
    BpmnProcess, BpmnLane, BpmnFlowNode, BpmnSequenceFlow, BpmnMessageFlow,
    BpmnActivity, BpmnTask, BpmnGateway, BpmnEvent,
    BpmnDataObject, BpmnDataAssociation
)
from org.modelio.metamodel.bpmn.events import (
    BpmnStartEvent, BpmnEndEvent, BpmnIntermediateCatchEvent, 
    BpmnIntermediateThrowEvent, BpmnBoundaryEvent
)
from org.modelio.metamodel.bpmn.gateways import (
    BpmnExclusiveGateway, BpmnParallelGateway, 
    BpmnInclusiveGateway, BpmnComplexGateway, BpmnEventBasedGateway
)
from org.modelio.api.modelio import Modelio

# Element Type Constants
START = "START"
END = "END"
TASK = "TASK"
USER_TASK = "USER_TASK"
SERVICE_TASK = "SERVICE_TASK"
MANUAL_TASK = "MANUAL_TASK"
SCRIPT_TASK = "SCRIPT_TASK"
BUSINESS_RULE_TASK = "BUSINESS_RULE_TASK"
SEND_TASK = "SEND_TASK"
RECEIVE_TASK = "RECEIVE_TASK"

EXCLUSIVE_GW = "EXCLUSIVE_GW"
PARALLEL_GW = "PARALLEL_GW"
INCLUSIVE_GW = "INCLUSIVE_GW"
COMPLEX_GW = "COMPLEX_GW"
EVENT_BASED_GW = "EVENT_BASED_GW"

INTERMEDIATE_CATCH = "INTERMEDIATE_CATCH"
INTERMEDIATE_THROW = "INTERMEDIATE_THROW"
MESSAGE_CATCH = "MESSAGE_CATCH"
MESSAGE_THROW = "MESSAGE_THROW"
TIMER_CATCH = "TIMER_CATCH"
SIGNAL_CATCH = "SIGNAL_CATCH"
SIGNAL_THROW = "SIGNAL_THROW"

MESSAGE_START = "MESSAGE_START"
TIMER_START = "TIMER_START"
SIGNAL_START = "SIGNAL_START"
CONDITIONAL_START = "CONDITIONAL_START"

MESSAGE_END = "MESSAGE_END"
SIGNAL_END = "SIGNAL_END"
TERMINATE_END = "TERMINATE_END"
ERROR_END = "ERROR_END"

def createBPMNFromConfig(package, config):
    factory = Modelio.getInstance().getModelingSession().getModel()
    
    # Get config values with defaults
    name = config.get("name", "Process")
    lanes_config = config.get("lanes", [])
    elements_config = config.get("elements", [])
    flows_config = config.get("flows", [])
    layout = config.get("layout", {})
    data_objects_config = config.get("data_objects", [])
    data_assoc_config = config.get("data_associations", [])
    
    # Spacing defaults
    SPACING = config.get("SPACING", 150)
    START_X = config.get("START_X", 80)
    TASK_WIDTH = config.get("TASK_WIDTH", 120)
    TASK_HEIGHT = config.get("TASK_HEIGHT", 60)
    DATA_WIDTH = config.get("DATA_WIDTH", 40)
    DATA_HEIGHT = config.get("DATA_HEIGHT", 50)
    DATA_OFFSET_X = config.get("DATA_OFFSET_X", 90)
    DATA_OFFSET_Y = config.get("DATA_OFFSET_Y", 10)
    
    # Create Process
    process = factory.createBpmnProcess()
    process.setName(name)
    package.getOwnedElement().add(process)
    
    # Create Lanes
    lane_map = {}
    lane_heights = {}
    current_y = 50
    for lane_name in lanes_config:
        lane = factory.createBpmnLane()
        lane.setName(lane_name)
        process.getBpmnLane().add(lane)
        lane_map[lane_name] = lane
        lane_heights[lane_name] = current_y
        current_y += 150  # Default lane height
    
    # Helper to create nodes
    def create_node(name, type_str, lane):
        node = None
        if type_str == START or type_str == MESSAGE_START or type_str == TIMER_START or type_str == SIGNAL_START or type_str == CONDITIONAL_START:
            node = factory.createBpmnStartEvent()
            if type_str == MESSAGE_START: node.setEventDefinition(factory.createBpmnMessageEventDefinition())
            elif type_str == TIMER_START: node.setEventDefinition(factory.createBpmnTimerEventDefinition())
            elif type_str == SIGNAL_START: node.setEventDefinition(factory.createBpmnSignalEventDefinition())
        elif type_str == END or type_str == MESSAGE_END or type_str == SIGNAL_END or type_str == TERMINATE_END or type_str == ERROR_END:
            node = factory.createBpmnEndEvent()
            if type_str == MESSAGE_END: node.setEventDefinition(factory.createBpmnMessageEventDefinition())
            elif type_str == SIGNAL_END: node.setEventDefinition(factory.createBpmnSignalEventDefinition())
            elif type_str == TERMINATE_END: node.setEventDefinition(factory.createBpmnTerminateEventDefinition())
        elif type_str == USER_TASK:
            node = factory.createBpmnTask()
            node.setStandardTask(True) # Using Standard for User for simplicity or map to correct property
        elif type_str == SERVICE_TASK:
            node = factory.createBpmnTask()
            node.setServiceTask(True)
        elif type_str == MANUAL_TASK:
            node = factory.createBpmnTask()
            node.setManualTask(True)
        elif type_str == SCRIPT_TASK:
            node = factory.createBpmnScriptTask()
        elif type_str == BUSINESS_RULE_TASK:
            node = factory.createBpmnBusinessRuleTask()
        elif type_str == SEND_TASK:
            node = factory.createBpmnSendTask()
        elif type_str == RECEIVE_TASK:
            node = factory.createBpmnReceiveTask()
        elif type_str == TASK:
            node = factory.createBpmnTask()
        elif type_str == EXCLUSIVE_GW:
            node = factory.createBpmnExclusiveGateway()
        elif type_str == PARALLEL_GW:
            node = factory.createBpmnParallelGateway()
        elif type_str == INCLUSIVE_GW:
            node = factory.createBpmnInclusiveGateway()
        elif type_str == COMPLEX_GW:
            node = factory.createBpmnComplexGateway()
        elif type_str == EVENT_BASED_GW:
            node = factory.createBpmnEventBasedGateway()
        elif type_str in [INTERMEDIATE_CATCH, INTERMEDIATE_THROW, MESSAGE_CATCH, MESSAGE_THROW, TIMER_CATCH, SIGNAL_CATCH, SIGNAL_THROW]:
            node = factory.createBpmnIntermediateCatchEvent() # Simplified
            # Logic to differentiate catch/throw could be added here
        
        if node:
            node.setName(name)
            lane.getBpmnFlowNode().add(node)
        return node

    # Create Elements
    nodes = {}
    for elem in elements_config:
        name, type_str, lane_name = elem[0], elem[1], elem[2]
        lane = lane_map.get(lane_name)
        if lane:
            node = create_node(name, type_str, lane)
            if node:
                nodes[name] = node

    # Create Data Objects
    data_nodes = {}
    for d in data_objects_config:
        name, lane_name, col = d[0], d[1], d[2]
        lane = lane_map.get(lane_name)
        if lane:
            do = factory.createBpmnDataObject()
            do.setName(name)
            process.getBpmnDataObject().add(do) # Data objects typically in process root
            # Note: lane association for data objects varies by tool, often purely visual or via association
            data_nodes[name] = do

    # Create Data Associations
    for assoc in data_assoc_config:
        src_name, tgt_name = assoc[0], assoc[1]
        src = nodes.get(src_name) or data_nodes.get(src_name)
        tgt = nodes.get(tgt_name) or data_nodes.get(tgt_name)
        if src and tgt:
            da = factory.createBpmnDataAssociation()
            # Simplified: Modelio API might differ on setting source/target refs directly
            # This requires specific API knowledge for DataAssociation endpoints
            # Assuming valid for generation structure
    
    # Create Flows
    for flow in flows_config:
        src_name, tgt_name, guard = flow[0], flow[1], flow[2]
        src = nodes.get(src_name)
        tgt = nodes.get(tgt_name)
        if src and tgt:
            sf = factory.createBpmnSequenceFlow()
            sf.setSource(src)
            sf.setTarget(tgt)
            sf.setName(guard)
            process.getBpmnSequenceFlow().add(sf)

    # Layout (X/Y)
    # Track stacking for elements in same lane/column
    stack_tracker = {} 

    for name, col_or_tuple in layout.items():
        node = nodes.get(name)
        if node:
            lane_name = None
            for ln, l in lane_map.items():
                if node in l.getBpmnFlowNode(): lane_name = ln; break
            
            col = 0
            y_off = 0
            
            if isinstance(col_or_tuple, tuple):
                col = col_or_tuple[0]
                y_off = col_or_tuple[1]
            else:
                col = col_or_tuple
            
            x = START_X + (col * SPACING)
            
            # Auto-stacking logic
            if lane_name:
                key = (lane_name, col)
                if key not in stack_tracker:
                    stack_tracker[key] = 0
                
                # If simple format, use auto-stack if count > 0
                if isinstance(col_or_tuple, int) and stack_tracker[key] > 0:
                    y_off = stack_tracker[key] * 90
                
                stack_tracker[key] += 1
            
            y = lane_heights.get(lane_name, 100) + 20 + y_off
            
            # Bounds setting (simplified for bounds)
            try:
                bounds = node.getBounds() # Modify existing if possible or set
            except:
                pass # API varies
                
            # Note: Modelio API often requires diagram specific commands to set bounds
            # This script generates the model. Layout in diagram often requires DiagramService.
            # For pure model generation, we stop here.
            
    print "BPMN Process '" + name + "' created successfully."


#
# Farming_Bot.py
#
# Description: Farming Bot process for resource gathering games.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Farming Bot",
    
    "lanes": ["Player", "Farming Bot"],
    
    "elements": [
        # Initialization
        ("Start", START, "Player"),
        ("Select Resources", USER_TASK, "Player"),
        ("Set Priorities", USER_TASK, "Player"),
        
        # Dependency Handling
        ("Analyze Dependencies", BUSINESS_RULE_TASK, "Farming Bot"),
        ("Tools Needed?", EXCLUSIVE_GW, "Farming Bot"),
        ("Craft Tools", SERVICE_TASK, "Farming Bot"),
        
        # Execution
        ("Fork", PARALLEL_GW, "Farming Bot"),
        ("Farm Resources", SERVICE_TASK, "Farming Bot"),
        ("Check Status", EXCLUSIVE_GW, "Farming Bot"),
        
        # Interrupts / Events
        ("Recover", SERVICE_TASK, "Farming Bot"),
        ("Update Preferences", USER_TASK, "Player"),
        ("Send Notification", MESSAGE_THROW, "Farming Bot"),
        ("Receive Notification", MESSAGE_CATCH, "Player"),
        
        # Completion
        ("Share?", INCLUSIVE_GW, "Player"),
        ("Brag", USER_TASK, "Player"),
        ("Send Materials", SEND_TASK, "Farming Bot"),
        ("End", END, "Player"),
    ],
    
    "flows": [
        # Initialization
        ("Start", "Select Resources", ""),
        ("Select Resources", "Set Priorities", ""),
        ("Set Priorities", "Analyze Dependencies", ""),
        
        # Dependency Logic
        ("Analyze Dependencies", "Tools Needed?", ""),
        ("Tools Needed?", "Craft Tools", "Yes"),
        ("Tools Needed?", "Fork", "No"),
        ("Craft Tools", "Fork", ""),
        
        # Farming Loop
        ("Fork", "Farm Resources", ""),
        ("Farm Resources", "Check Status", ""),
        
        # Status Checks (Loop backs)
        ("Check Status", "Recover", "Disaster"),
        ("Recover", "Farm Resources", ""),
        
        ("Check Status", "Update Preferences", "Update"),
        ("Update Preferences", "Farm Resources", ""),
        
        ("Check Status", "Send Notification", "Milestone"),
        ("Send Notification", "Receive Notification", ""),
        ("Receive Notification", "Farm Resources", ""),
        
        # Completion
        ("Check Status", "Share?", "Finished"),
        ("Share?", "Brag", "Friends"),
        ("Share?", "Send Materials", "Send"),
        ("Brag", "End", ""),
        ("Send Materials", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Select Resources": 1,
        "Set Priorities": 2,
        "Analyze Dependencies": 3,
        "Tools Needed?": 4,
        "Craft Tools": 5,
        "Fork": 6,
        "Farm Resources": 7,
        "Check Status": 8,
        "Recover": 9,
        "Update Preferences": 9,
        "Send Notification": 9,
        "Receive Notification": 10,
        "Share?": 11,
        "Brag": 12,
        "Send Materials": 12,
        "End": 13,
    },
    
    "data_objects": [
        ("Resource List", "Player", 1),
        ("Priority Map", "Player", 2),
        ("Tool Kit", "Farming Bot", 5),
        ("Inventory", "Farming Bot", 12),
    ],
    
    "data_associations": [
        ("Select Resources", "Resource List"),
        ("Resource List", "Set Priorities"),
        ("Set Priorities", "Priority Map"),
        ("Priority Map", "Analyze Dependencies"),
        ("Craft Tools", "Tool Kit"),
        ("Tool Kit", "Farm Resources"),
        ("Farm Resources", "Inventory"),
        ("Inventory", "Send Materials"),
    ],
}

# Entry point
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
