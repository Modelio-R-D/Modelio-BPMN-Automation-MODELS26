# S1 - Document Approval - Claude Opus 4.5
# Paste generated script here

# Jython Script for Modelio - BPMN Document Approval Process
# This script creates a simple document approval process with one reviewer
# Compatible with Modelio 4.x and 5.x

from org.modelio.api.modelio import Modelio
from org.modelio.api.model import IModelingSession
from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess, BpmnLane, BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnTask, BpmnUserTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent, BpmnEndEvent
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.bpmn.rootElements import BpmnFlowElement
from org.modelio.metamodel.diagrams import BpmnProcessDesignDiagram
from org.modelio.api.module import IModule

# Get the Modelio instance and modeling session
modelio = Modelio.getInstance()
modeling_session = modelio.getModelingSession()
model_services = modelio.getModelService()

# Get the selected element as the parent (should be a Package)
selected_elements = modelio.getSelectedElements()
if not selected_elements or len(selected_elements) == 0:
    print("Error: Please select a package where the BPMN process will be created.")
    raise Exception("No element selected")

parent_element = selected_elements[0]
print("Parent element: " + parent_element.getName())

# Start a transaction
transaction = modeling_session.createTransaction("Create Document Approval BPMN Process")

try:
    # =========================================================================
    # STEP 1: Create the BPMN Process
    # =========================================================================
    print("Creating BPMN Process...")
    
    bpmn_process = modeling_session.getModel().createBpmnProcess()
    bpmn_process.setName("Document Approval Process")
    bpmn_process.setOwner(parent_element)
    
    print("BPMN Process created: " + bpmn_process.getName())
    
    # =========================================================================
    # STEP 2: Create Lane Set and Lane
    # =========================================================================
    print("Creating Lane Set and Lanes...")
    
    # Create LaneSet
    lane_set = modeling_session.getModel().createBpmnLaneSet()
    lane_set.setName("Document Approval Lanes")
    lane_set.setProcess(bpmn_process)
    
    # Create Reviewer Lane
    reviewer_lane = modeling_session.getModel().createBpmnLane()
    reviewer_lane.setName("Reviewer")
    reviewer_lane.setLaneSet(lane_set)
    
    print("Lane created: " + reviewer_lane.getName())
    
    # =========================================================================
    # STEP 3: Create BPMN Elements (Start, Tasks, End)
    # =========================================================================
    print("Creating BPMN Elements...")
    
    # Create Start Event
    start_event = modeling_session.getModel().createBpmnStartEvent()
    start_event.setName("Start")
    start_event.setContainer(bpmn_process)
    start_event.setLane(reviewer_lane)
    print("  Created: Start Event")
    
    # Create User Task: Submit Document
    submit_task = modeling_session.getModel().createBpmnUserTask()
    submit_task.setName("Submit Document")
    submit_task.setContainer(bpmn_process)
    submit_task.setLane(reviewer_lane)
    print("  Created: Submit Document Task")
    
    # Create User Task: Review Document
    review_task = modeling_session.getModel().createBpmnUserTask()
    review_task.setName("Review Document")
    review_task.setContainer(bpmn_process)
    review_task.setLane(reviewer_lane)
    print("  Created: Review Document Task")
    
    # Create End Event
    end_event = modeling_session.getModel().createBpmnEndEvent()
    end_event.setName("End")
    end_event.setContainer(bpmn_process)
    end_event.setLane(reviewer_lane)
    print("  Created: End Event")
    
    # =========================================================================
    # STEP 4: Create Sequence Flows
    # =========================================================================
    print("Creating Sequence Flows...")
    
    # Flow 1: Start -> Submit Document
    flow1 = modeling_session.getModel().createBpmnSequenceFlow()
    flow1.setName("Flow_Start_Submit")
    flow1.setSourceRef(start_event)
    flow1.setTargetRef(submit_task)
    flow1.setContainer(bpmn_process)
    print("  Created flow: Start -> Submit Document")
    
    # Flow 2: Submit Document -> Review Document
    flow2 = modeling_session.getModel().createBpmnSequenceFlow()
    flow2.setName("Flow_Submit_Review")
    flow2.setSourceRef(submit_task)
    flow2.setTargetRef(review_task)
    flow2.setContainer(bpmn_process)
    print("  Created flow: Submit Document -> Review Document")
    
    # Flow 3: Review Document -> End
    flow3 = modeling_session.getModel().createBpmnSequenceFlow()
    flow3.setName("Flow_Review_End")
    flow3.setSourceRef(review_task)
    flow3.setTargetRef(end_event)
    flow3.setContainer(bpmn_process)
    print("  Created flow: Review Document -> End")
    
    # =========================================================================
    # STEP 5: Create the BPMN Process Design Diagram
    # =========================================================================
    print("Creating BPMN Diagram...")
    
    diagram_factory = modelio.getDiagramService()
    
    # Create the diagram
    diagram = diagram_factory.createDiagram(
        "BpmnProcessDesignDiagram",
        bpmn_process,
        "Document Approval Process Diagram"
    )
    
    if diagram is None:
        print("Warning: Could not create diagram automatically. Trying alternative method...")
        # Alternative: Create diagram using model factory
        diagram = modeling_session.getModel().createBpmnProcessDesignDiagram()
        diagram.setName("Document Approval Process Diagram")
        diagram.setOrigin(bpmn_process)
    
    print("Diagram created: " + diagram.getName())
    
    # =========================================================================
    # STEP 6: Add Elements to Diagram and Position Them
    # =========================================================================
    print("Adding elements to diagram and positioning...")
    
    # Open the diagram for editing
    diagram_handle = diagram_factory.getDiagramHandle(diagram)
    
    if diagram_handle is not None:
        # Define layout constants
        LANE_X = 50
        LANE_Y = 50
        LANE_WIDTH = 700
        LANE_HEIGHT = 150
        
        EVENT_SIZE = 30
        TASK_WIDTH = 100
        TASK_HEIGHT = 60
        
        # Vertical center of the lane
        ELEMENT_Y = LANE_Y + (LANE_HEIGHT / 2) - (TASK_HEIGHT / 2)
        EVENT_Y = LANE_Y + (LANE_HEIGHT / 2) - (EVENT_SIZE / 2)
        
        # Horizontal positions (left to right)
        START_X = LANE_X + 50
        SUBMIT_X = START_X + 100
        REVIEW_X = SUBMIT_X + 150
        END_X = REVIEW_X + 150
        
        # Unmask and position the Lane
        lane_graphic = diagram_handle.unmask(reviewer_lane, LANE_X, LANE_Y)
        if lane_graphic is not None:
            lane_graphic.setSize(LANE_WIDTH, LANE_HEIGHT)
            print("  Positioned: Reviewer Lane")
        
        # Unmask and position Start Event
        start_graphic = diagram_handle.unmask(start_event, START_X, EVENT_Y)
        if start_graphic is not None:
            start_graphic.setSize(EVENT_SIZE, EVENT_SIZE)
            print("  Positioned: Start Event at (" + str(START_X) + ", " + str(EVENT_Y) + ")")
        
        # Unmask and position Submit Document Task
        submit_graphic = diagram_handle.unmask(submit_task, SUBMIT_X, ELEMENT_Y)
        if submit_graphic is not None:
            submit_graphic.setSize(TASK_WIDTH, TASK_HEIGHT)
            print("  Positioned: Submit Document at (" + str(SUBMIT_X) + ", " + str(ELEMENT_Y) + ")")
        
        # Unmask and position Review Document Task
        review_graphic = diagram_handle.unmask(review_task, REVIEW_X, ELEMENT_Y)
        if review_graphic is not None:
            review_graphic.setSize(TASK_WIDTH, TASK_HEIGHT)
            print("  Positioned: Review Document at (" + str(REVIEW_X) + ", " + str(ELEMENT_Y) + ")")
        
        # Unmask and position End Event
        end_graphic = diagram_handle.unmask(end_event, END_X, EVENT_Y)
        if end_graphic is not None:
            end_graphic.setSize(EVENT_SIZE, EVENT_SIZE)
            print("  Positioned: End Event at (" + str(END_X) + ", " + str(EVENT_Y) + ")")
        
        # Unmask Sequence Flows (they will auto-route between connected elements)
        flow1_graphic = diagram_handle.unmask(flow1, 0, 0)
        if flow1_graphic is not None:
            print("  Added: Flow Start -> Submit")
        
        flow2_graphic = diagram_handle.unmask(flow2, 0, 0)
        if flow2_graphic is not None:
            print("  Added: Flow Submit -> Review")
        
        flow3_graphic = diagram_handle.unmask(flow3, 0, 0)
        if flow3_graphic is not None:
            print("  Added: Flow Review -> End")
        
        # Save the diagram changes
        diagram_handle.save()
        diagram_handle.close()
        
        print("Diagram layout completed.")
    else:
        print("Warning: Could not get diagram handle for positioning elements.")
    
    # =========================================================================
    # STEP 7: Commit the Transaction
    # =========================================================================
    transaction.commit()
    print("")
    print("=" * 60)
    print("SUCCESS: Document Approval BPMN Process created successfully!")
    print("=" * 60)
    print("")
    print("Created elements:")
    print("  - Process: " + bpmn_process.getName())
    print("  - Lane: " + reviewer_lane.getName())
    print("  - Start Event: " + start_event.getName())
    print("  - User Task: " + submit_task.getName())
    print("  - User Task: " + review_task.getName())
    print("  - End Event: " + end_event.getName())
    print("  - Sequence Flows: 3")
    print("  - Diagram: " + diagram.getName())
    print("")
    print("Open the diagram '" + diagram.getName() + "' to view the process.")

except Exception as e:
    # Rollback on error
    transaction.rollback()
    print("")
    print("ERROR: Failed to create BPMN process!")
    print("Error details: " + str(e))
    import traceback
    traceback.print_exc()
    raise e

finally:
    # Ensure transaction is closed
    if transaction is not None:
        try:
            transaction.close()
        except:
            pass



# Modelio output:
ImportError: No module named model in <script> at line number 6
Traceback (most recent call last):
  File "<script>", line 6, in <module>
ImportError: No module named model