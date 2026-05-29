# S1 - Document Approval - Gemini Pro (Dec 2025) (Round 2 - With Example)
# Paste generated script here

#
# CreateBPMNProcess.py
#
# Description:
#   Creates a BPMN Process with a "Reviewer" lane and a linear approval flow:
#   Start -> Submit Document -> Review Document -> End.
#   It also generates the BpmnProcessDesignDiagram and positions the elements.
#
# Applicable on: Package
#

from org.modelio.metamodel.bpmn.process import BpmnProcess, BpmnLane, BpmnUserTask, BpmnSequenceFlow
from org.modelio.metamodel.bpmn.events import BpmnStartEvent, BpmnEndEvent
from org.modelio.metamodel.uml.statik import Package

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
PROCESS_NAME = "Document Approval Process"
LANE_NAME = "Reviewer"
DIAGRAM_NAME = "Approval Flow Diagram"

# Layout Constants
START_X = 100
START_Y = 100
TASK_WIDTH = 140
TASK_HEIGHT = 70
SPACING = 80

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def get_factory():
    """Returns the generic MObject factory for creating BPMN elements."""
    return Model.getMetamodel().getMObjectFactory()

def create_sequence_flow(process, source, target):
    """Creates a sequence flow between two nodes and adds it to the process."""
    factory = get_factory()
    flow = factory.createBpmnSequenceFlow()
    flow.setName("")
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    process.getFlowElement().add(flow)
    return flow

def layout_diagram(process, lane, start_node, task1, task2, end_node):
    """Creates and arranges the diagram elements."""
    diagram_service = modelingSession.getDiagramService()
    diagram = diagram_service.createDiagram("BpmnProcessDesignDiagram", DIAGRAM_NAME, process)
    
    if diagram:
        print "Diagram created. Calculating layout..."
        diagram_handle = diagram_service.getDiagramHandle(diagram)
        
        try:
            # 1. Calculate dimensions
            # Lane needs to fit: Start(40) + Spacing + Task1(W) + Spacing + Task2(W) + Spacing + End(40) + Padding
            content_width = 40 + TASK_WIDTH + TASK_WIDTH + 40 + (SPACING * 3)
            lane_width = START_X + content_width + 100
            lane_height = 250
            
            # 2. Draw Lane
            # Lane acts as a container visually. 
            lane_view = diagram_handle.unmask(lane, 50, 50)
            lane_view.setBounds(50, 50, lane_width, lane_height)
            
            # Center Y for elements (relative to the diagram, inside the lane)
            # Lane starts at Y=50, Height=250 -> Middle is 175
            center_y = 50 + (lane_height / 2)
            current_x = START_X + 50 # Offset from lane start
            
            # 3. Draw Elements
            # Start Event (approx 30x30 or 40x40 standard)
            diagram_handle.unmask(start_node, current_x, center_y - 15)
            current_x += 40 + SPACING
            
            # Task 1: Submit
            t1_view = diagram_handle.unmask(task1, current_x, center_y - (TASK_HEIGHT / 2))
            t1_view.setBounds(current_x, int(center_y - (TASK_HEIGHT / 2)), TASK_WIDTH, TASK_HEIGHT)
            current_x += TASK_WIDTH + SPACING
            
            # Task 2: Review
            t2_view = diagram_handle.unmask(task2, current_x, center_y - (TASK_HEIGHT / 2))
            t2_view.setBounds(current_x, int(center_y - (TASK_HEIGHT / 2)), TASK_WIDTH, TASK_HEIGHT)
            current_x += TASK_WIDTH + SPACING
            
            # End Event
            diagram_handle.unmask(end_node, current_x, center_y - 15)
            
            diagram_handle.save()
            print "Layout applied successfully."
            
        finally:
            diagram_handle.close()
    else:
        print "Error: Failed to create diagram."

def create_approval_process(package):
    """Main function to build the model elements."""
    print "Creating process in: " + package.getName()
    factory = get_factory()

    # 1. Create BpmnProcess
    process = factory.createBpmnProcess()
    process.setName(PROCESS_NAME)
    package.getCompositionChildren().add(process)

    # 2. Create Lane Structure
    # Structure: Process -> LaneSet -> Lane
    lane_set = factory.createBpmnLaneSet()
    process.getLaneSet().add(lane_set)
    
    lane = factory.createBpmnLane()
    lane.setName(LANE_NAME)
    lane_set.getLane().add(lane)

    # 3. Create Flow Nodes (Tasks & Events)
    # We add them to the Process (ownership) AND the Lane (logical partition)
    
    # Start Event
    start_evt = factory.createBpmnStartEvent()
    start_evt.setName("Start")
    process.getFlowElement().add(start_evt)
    lane.getFlowNode().add(start_evt)

    # Task 1: Submit
    task_submit = factory.createBpmnUserTask()
    task_submit.setName("Submit Document")
    process.getFlowElement().add(task_submit)
    lane.getFlowNode().add(task_submit)

    # Task 2: Review
    task_review = factory.createBpmnUserTask()
    task_review.setName("Review Document")
    process.getFlowElement().add(task_review)
    lane.getFlowNode().add(task_review)

    # End Event
    end_evt = factory.createBpmnEndEvent()
    end_evt.setName("End")
    process.getFlowElement().add(end_evt)
    lane.getFlowNode().add(end_evt)

    # 4. Create Flows
    create_sequence_flow(process, start_evt, task_submit)
    create_sequence_flow(process, task_submit, task_review)
    create_sequence_flow(process, task_review, end_evt)

    # 5. Create Diagram
    layout_diagram(process, lane, start_evt, task_submit, task_review, end_evt)


# -----------------------------------------------------------------------------
# Main Execution Block
# -----------------------------------------------------------------------------
if selectedElements.size() > 0:
    element = selectedElements.get(0)
    if isinstance(element, Package):
        create_approval_process(element)
    else:
        print "Selection Error: Please select a Package (not a Class or Diagram)."
else:
    print "Selection Error: No element selected. Please select a Package."



# Modelio output:

ImportError: No module named process in <script> at line number 12
Traceback (most recent call last):
  File "<script>", line 12, in <module>
ImportError: No module named process