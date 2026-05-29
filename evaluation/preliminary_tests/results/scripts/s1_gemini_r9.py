# S1 - Document Approval - Gemini Pro (Dec 2025) (Round 9 - Final, NOT WORKING)
# After 9 rounds of debugging, still not working

#
# CreateBPMNProcess_Final_Fixed.py
#
# Description:
#   Creates a BPMN Process, Lane, Tasks, and Diagram.
#   Uses string-based reflection to avoid Jython namespace collisions.
#
# Applicable on: Package
#

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
def create_element(metamodel, metaclass_name, name=None):
    """
    Creates an element using the Metamodel and string name.
    We use strings (e.g. "BpmnProcess") to avoid importing the classes,
    which can confuse Jython's resolution of the Metamodel elements.
    """
    try:
        # Get the MClass object (The definition of the type)
        mclass = metamodel.getMClass(metaclass_name)

        # Create the instance
        if hasattr(mclass, "createInstance"):
            instance = mclass.createInstance()
        else:
            print "Error: MClass for " + metaclass_name + " found, but has no createInstance method."
            return None

        # Set Name if provided
        if name and instance:
            instance.setName(name)
        return instance

    except Exception, e:
        print "Exception creating " + metaclass_name + ": " + str(e)
        return None

def create_sequence_flow(metamodel, process, source, target):
    """Creates a sequence flow between two nodes."""
    flow = create_element(metamodel, "BpmnSequenceFlow")
    if flow:
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
            content_width = 40 + TASK_WIDTH + TASK_WIDTH + 40 + (SPACING * 3)
            lane_width = START_X + content_width + 100
            lane_height = 250

            # 2. Draw Lane
            lane_view = diagram_handle.unmask(lane, 50, 50)
            lane_view.setBounds(50, 50, lane_width, lane_height)

            center_y = 50 + (lane_height / 2)
            current_x = START_X + 50

            # 3. Draw Elements
            # Start
            diagram_handle.unmask(start_node, current_x, center_y - 15)
            current_x += 40 + SPACING

            # Task 1
            t1_view = diagram_handle.unmask(task1, current_x, center_y - (TASK_HEIGHT / 2))
            t1_view.setBounds(current_x, int(center_y - (TASK_HEIGHT / 2)), TASK_WIDTH, TASK_HEIGHT)
            current_x += TASK_WIDTH + SPACING

            # Task 2
            t2_view = diagram_handle.unmask(task2, current_x, center_y - (TASK_HEIGHT / 2))
            t2_view.setBounds(current_x, int(center_y - (TASK_HEIGHT / 2)), TASK_WIDTH, TASK_HEIGHT)
            current_x += TASK_WIDTH + SPACING

            # End
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

    # 1. Get the Metamodel Service safely from the package
    # This 'metamodel' object can create any element if we give it the string name.
    metamodel = package.getMClass().getMetamodel()

    # 2. Create Process
    process = create_element(metamodel, "BpmnProcess", PROCESS_NAME)
    if not process: return # Stop if creation failed
    package.getCompositionChildren().add(process)

    # 3. Create Lane Structure
    # Structure: Process -> LaneSet -> Lane
    lane_set = create_element(metamodel, "BpmnLaneSet")
    process.getLaneSet().add(lane_set)

    lane = create_element(metamodel, "BpmnLane", LANE_NAME)
    lane_set.getLane().add(lane)

    # 4. Create Flow Nodes
    # Note: Added to BOTH Process (ownership) and Lane (association)

    # Start Event
    start_evt = create_element(metamodel, "BpmnStartEvent", "Start")
    process.getFlowElement().add(start_evt)
    lane.getFlowNode().add(start_evt)

    # Task 1
    task_submit = create_element(metamodel, "BpmnUserTask", "Submit Document")
    process.getFlowElement().add(task_submit)
    lane.getFlowNode().add(task_submit)

    # Task 2
    task_review = create_element(metamodel, "BpmnUserTask", "Review Document")
    process.getFlowElement().add(task_review)
    lane.getFlowNode().add(task_review)

    # End Event
    end_evt = create_element(metamodel, "BpmnEndEvent", "End")
    process.getFlowElement().add(end_evt)
    lane.getFlowNode().add(end_evt)

    # 5. Create Flows
    create_sequence_flow(metamodel, process, start_evt, task_submit)
    create_sequence_flow(metamodel, process, task_submit, task_review)
    create_sequence_flow(metamodel, process, task_review, end_evt)

    # 6. Create Diagram
    layout_diagram(process, lane, start_evt, task_submit, task_review, end_evt)

# -----------------------------------------------------------------------------
# Main Execution Block
# -----------------------------------------------------------------------------
if len(selectedElements) > 0:
    element = selectedElements.get(0)
    if isinstance(element, Package):
        create_approval_process(element)
    else:
        print "Selection Error: Please select a Package."
else:
    print "Selection Error: No element selected."


# =============================================================================
# DEBUGGING HISTORY (9 ROUNDS - ALL FAILED)
# =============================================================================
#
# Round 3: ImportError: No module named process
# - Wrong import path for BpmnProcess
#
# Round 4: NameError: global name 'Model' is not defined
# - Tried to use non-existent global 'Model' object
#
# Round 5: AttributeError: 'SharedModelingSession' has no attribute 'getMetamodel'
# - Wrong API path to get metamodel
#
# Round 6: TypeError: No visible constructors for class (BpmnProcess)
# - Tried to instantiate interface directly with constructor
#
# Round 7: AttributeError: 'SmMetamodel' has no attribute 'getMObjectFactory'
# - Wrong factory access method
#
# Round 8: 'object has no attribute 'createInstance'
# - MClass reflection doesn't work as expected
#
# Round 9: Same error - still trying reflection approach
# - Final attempt still fails
#
# OBSERVATION: Gemini went in completely wrong direction after Round 3.
# Instead of using modelingSession.getModel().createBpmnProcess() (shown in examples),
# it tried increasingly complex reflection approaches that don't work.
