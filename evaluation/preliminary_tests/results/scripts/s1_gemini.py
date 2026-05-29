# S1 - Document Approval - Gemini Pro (Dec 2025)
# Paste generated script here

from org.modelio.model.impl import MObject
from org.modelio.metamodel.bpmn.process import BpmnProcess, BpmnLane, BpmnStartEvent, BpmnUserTask, BpmnEndEvent, BpmnSequenceFlow

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
PROCESS_NAME = "Document Approval Process"
LANE_NAME = "Reviewer"
DIAGRAM_NAME = "Approval Diagram"

# Layout Constants
START_X = 100
START_Y = 100
TASK_WIDTH = 120
TASK_HEIGHT = 60
SPACING = 100  # Space between elements

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def get_factory():
    return Model.getMetamodel().getMObjectFactory()

def create_sequence_flow(process, source, target):
    factory = get_factory()
    flow = factory.createBpmnSequenceFlow()
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    process.getFlowElement().add(flow)
    return flow

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    # 1. Validation: specific element must be selected to hold the process
    if not selectedElements or len(selectedElements) == 0:
        print "Error: Please select a Package to contain the BPMN Process."
        return

    owner = selectedElements[0]
    print "Creating BPMN Process under: " + owner.getName()

    factory = get_factory()

    # 2. Create the BPMN Process
    process = factory.createBpmnProcess()
    process.setName(PROCESS_NAME)
    owner.getCompositionChildren().add(process)

    # 3. Create LaneSet and Lane
    # Note: In Modelio, a Process contains a LaneSet, which contains Lanes
    lane_set = factory.createBpmnLaneSet()
    process.getLaneSet().add(lane_set)
    
    lane = factory.createBpmnLane()
    lane.setName(LANE_NAME)
    lane_set.getLane().add(lane)

    # 4. Create BPMN Elements
    # Start Event
    start_evt = factory.createBpmnStartEvent()
    start_evt.setName("Start")
    process.getFlowElement().add(start_evt)

    # User Task 1: Submit
    task_submit = factory.createBpmnUserTask()
    task_submit.setName("Submit Document")
    process.getFlowElement().add(task_submit)

    # User Task 2: Review
    task_review = factory.createBpmnUserTask()
    task_review.setName("Review Document")
    process.getFlowElement().add(task_review)

    # End Event
    end_evt = factory.createBpmnEndEvent()
    end_evt.setName("End")
    process.getFlowElement().add(end_evt)

    # 5. Create Sequence Flows
    create_sequence_flow(process, start_evt, task_submit)
    create_sequence_flow(process, task_submit, task_review)
    create_sequence_flow(process, task_review, end_evt)

    # 6. Create and Layout the Diagram
    diagram_service = Model.getDiagramService()
    diagram = diagram_service.createDiagram("BpmnProcessDesignDiagram", DIAGRAM_NAME, process)
    
    if diagram:
        print "Diagram created. Applying layout..."
        diagram_handle = diagram_service.getDiagramHandle(diagram)
        
        try:
            # Layout Calculation Variables
            current_x = START_X
            # Center tasks vertically relative to the lane
            lane_y = 50
            lane_height = 200
            center_y = lane_y + (lane_height / 2)
            
            # --- Draw Lane ---
            # Unmask Lane (x, y)
            lane_node = diagram_handle.unmask(lane, 50, lane_y)
            # Calculate total width required: Start + 2 Tasks + End + Spacing
            total_width = (START_X + 40) + (TASK_WIDTH * 2) + (SPACING * 3) + 100
            lane_node.setBounds(50, lane_y, total_width, lane_height)

            # --- Draw Elements ---
            # NOTE: We unmask elements. To make them visually inside the lane, 
            # we simply position them within the lane's bounds.
            
            # 1. Start Event (Standard size ~40x40)
            start_node = diagram_handle.unmask(start_evt, current_x, center_y - 20)
            current_x += 40 + SPACING

            # 2. Submit Task
            task1_node = diagram_handle.unmask(task_submit, current_x, center_y - (TASK_HEIGHT/2))
            task1_node.setBounds(current_x, int(center_y - (TASK_HEIGHT/2)), TASK_WIDTH, TASK_HEIGHT)
            current_x += TASK_WIDTH + SPACING

            # 3. Review Task
            task2_node = diagram_handle.unmask(task_review, current_x, center_y - (TASK_HEIGHT/2))
            task2_node.setBounds(current_x, int(center_y - (TASK_HEIGHT/2)), TASK_WIDTH, TASK_HEIGHT)
            current_x += TASK_WIDTH + SPACING

            # 4. End Event
            end_node = diagram_handle.unmask(end_evt, current_x, center_y - 20)
            
            diagram_handle.save()
            print "Process and Diagram successfully created."
            
        finally:
            diagram_handle.close()
    else:
        print "Error: Could not create diagram."

# Run the script
main()

# Modelio output:
ImportError: No module named model in <script> at line number 1
Traceback (most recent call last):
  File "<script>", line 1, in <module>
ImportError: No module named model