# S1 - Document Approval - GPT-5.2 Thinking (Round 2 - With Example)
# Paste generated script here

# ---------------------------------------------------------------------------
# Modelio Jython Macro
# Creates a BPMN Process Design diagram for a simple document approval process:
#   Start -> Submit Document (User Task) -> Review Document (User Task) -> End
# Single lane: "Reviewer"
# ---------------------------------------------------------------------------

from org.modelio.api.modelio import Modelio
from org.modelio.api.modelio.diagram import IDiagramNode
from org.eclipse.draw2d.geometry import Rectangle

def _first_node(graphics):
    if graphics is None:
        return None
    for g in graphics:
        try:
            if isinstance(g, IDiagramNode):
                return g
        except:
            pass
    # Fallback: return first graphic that seems to support node operations
    for g in graphics:
        try:
            g.setBounds  # attribute check
            return g
        except:
            pass
    return None

def _unmask_and_set_bounds(diagram_handle, element, x, y, w, h):
    graphics = diagram_handle.unmask(element, int(x), int(y))
    node = _first_node(graphics)
    if node is not None and w is not None and h is not None:
        try:
            node.setBounds(Rectangle(int(x), int(y), int(w), int(h)))
        except:
            # If bounds cannot be applied (layout constraints), ignore
            pass
    return graphics

def _pick_owner():
    try:
        if selectedElements.size > 0:
            return selectedElements.get(0)
    except:
        pass

    model = modelingSession.getModel()

    # Try common root access patterns
    try:
        roots = model.getModelRoots()
        try:
            if roots is not None and roots.size() > 0:
                return roots.get(0)
        except:
            if roots is not None and len(roots) > 0:
                return roots[0]
    except:
        pass

    try:
        return model.getRoot()
    except:
        pass

    return None

def create_document_approval_bpmn(owner):
    model = modelingSession.getModel()

    # 1) Create a new BpmnProcess
    process = model.createBpmnProcess()
    process.setName("Document Approval Process")
    process.setOwner(owner)

    # 2) Create BpmnLanes for each role (single lane)
    lane_set = model.createBpmnLaneSet()
    lane_set.setName("LaneSet")
    lane_set.setProcess(process)
    process.setLaneSet(lane_set)

    lane = model.createBpmnLane()
    lane.setName("Reviewer")
    lane.setLaneSet(lane_set)

    # 3) Create BPMN elements (tasks, events)
    start_evt = model.createBpmnStartEvent()
    start_evt.setName("Start")
    start_evt.setContainer(process)

    submit_task = model.createBpmnUserTask()
    submit_task.setName("Submit Document")
    submit_task.setContainer(process)

    review_task = model.createBpmnUserTask()
    review_task.setName("Review Document")
    review_task.setContainer(process)

    end_evt = model.createBpmnEndEvent()
    end_evt.setName("End")
    end_evt.setContainer(process)

    # Assign elements to the lane (partitioning)
    try:
        lane.getFlowElementRef().add(start_evt)
        lane.getFlowElementRef().add(submit_task)
        lane.getFlowElementRef().add(review_task)
        lane.getFlowElementRef().add(end_evt)
    except:
        # Fallback: set element -> lane relation if supported
        try:
            start_evt.getLane().add(lane)
            submit_task.getLane().add(lane)
            review_task.getLane().add(lane)
            end_evt.getLane().add(lane)
        except:
            pass

    # 4) Create sequence flows connecting elements
    sf1 = model.createBpmnSequenceFlow()
    sf1.setName("")
    sf1.setContainer(process)
    sf1.setSourceRef(start_evt)
    sf1.setTargetRef(submit_task)

    sf2 = model.createBpmnSequenceFlow()
    sf2.setName("")
    sf2.setContainer(process)
    sf2.setSourceRef(submit_task)
    sf2.setTargetRef(review_task)

    sf3 = model.createBpmnSequenceFlow()
    sf3.setName("")
    sf3.setContainer(process)
    sf3.setSourceRef(review_task)
    sf3.setTargetRef(end_evt)

    # 5) Create a BpmnProcessDesignDiagram
    diagram = model.createBpmnProcessDesignDiagram()
    diagram.setName("Document Approval - BPMN")
    diagram.setOrigin(process)
    process.getProduct().add(diagram)

    # 6) Position elements in the diagram (layout)
    diagram_service = Modelio.getInstance().getDiagramService()
    handle = diagram_service.getDiagramHandle(diagram)

    try:
        handle.setBatchMode(True)
        try:
            handle.setLayoutAssistantEnabled(False)
        except:
            pass

        # Layout constants
        lane_x, lane_y, lane_w, lane_h = 20, 20, 920, 240

        start_x, start_y, start_w, start_h = 80, 120, 40, 40
        submit_x, submit_y, submit_w, submit_h = 170, 100, 160, 80
        review_x, review_y, review_w, review_h = 390, 100, 160, 80
        end_x, end_y, end_w, end_h = 610, 120, 40, 40

        # Unmask lane first, then flow nodes inside
        _unmask_and_set_bounds(handle, lane, lane_x, lane_y, lane_w, lane_h)

        _unmask_and_set_bounds(handle, start_evt, start_x, start_y, start_w, start_h)
        _unmask_and_set_bounds(handle, submit_task, submit_x, submit_y, submit_w, submit_h)
        _unmask_and_set_bounds(handle, review_task, review_x, review_y, review_w, review_h)
        _unmask_and_set_bounds(handle, end_evt, end_x, end_y, end_w, end_h)

        # Unmask sequence flows (links). Coordinates are not meaningful for links.
        handle.unmask(sf1, 0, 0)
        handle.unmask(sf2, 0, 0)
        handle.unmask(sf3, 0, 0)

        handle.setBatchMode(False)
        handle.save()
    finally:
        try:
            handle.close()
        except:
            pass

    return process

# ---------------------------------------------------------------------------
# Macro execution starts here
# ---------------------------------------------------------------------------
owner = _pick_owner()
if owner is None:
    print "ERROR: No valid owner found. Please select a Package (or another element that can own a Behavior) and run again."
else:
    try:
        if not owner.getStatus().isModifiable():
            print "ERROR: The selected owner is not modifiable."
        else:
            create_document_approval_bpmn(owner)
    except Exception as e:
        print "ERROR: " + str(e)

# Modelio output: s1_gpt5_r2.png
