# S1 - Document Approval - Claude Opus 4.5 (Round 5 - After debugging)
# Working script after 5 rounds of debugging

#
# BpmnDocumentApproval  1.0
#
# Description:
#  This macro creates a simple BPMN document approval process with:
#  - One lane: "Reviewer"
#  - Start Event -> Submit Document -> Review Document -> End Event
#  - A BpmnProcessDesignDiagram with positioned elements
#
# Applicable on: Package
#
# Author:  Generated for Modelio
#
# Version history:
# 1.0   December 2024 - creation for Modelio 4.x/5.x
#

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package


def createBpmnProcess(package):
    """Create a BPMN Process under the given package"""
    process = modelingSession.getModel().createBpmnProcess()
    process.setName("Document Approval Process")
    process.setOwner(package)
    return process


def createLaneSet(process):
    """Create a LaneSet for the process"""
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setName("Lanes")
    laneSet.setProcess(process)
    return laneSet


def createLane(laneSet, name):
    """Create a Lane in the given LaneSet"""
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane


def addToLane(lane, element):
    """Add a flow element to a lane"""
    lane.getFlowElementRef().add(element)


def createStartEvent(process, name):
    """Create a Start Event"""
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createEndEvent(process, name):
    """Create an End Event"""
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event


def createUserTask(process, name):
    """Create a User Task"""
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task


def createSequenceFlow(process, source, target):
    """Create a Sequence Flow between two elements"""
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName("")
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    return flow


def unmaskElement(dh, element, x, y, width, height):
    """Unmask an element and set its size"""
    graphics = dh.unmask(element, x, y)
    if (graphics is not None and graphics.size() > 0):
        gfx = graphics.get(0)
        gfx.setSize(width, height)
        return gfx
    return None


def unmaskFlow(dh, flow):
    """Unmask a sequence flow"""
    dh.unmask(flow, 0, 0)


def createDiagramAndLayout(process, lane, elements, flows):
    """Create a BPMN Process Design Diagram and layout elements"""

    # Create the diagram using the model factory
    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("Document Approval Process Diagram")
    diagram.setOrigin(process)

    print "Created diagram: " + diagram.getName()

    # Get diagram service for layout
    diagramService = Modelio.getInstance().getDiagramService()

    # Open diagram for editing
    dh = diagramService.getDiagramHandle(diagram)

    if (dh is not None):
        # Layout constants
        LANE_X = 50
        LANE_Y = 50
        LANE_W = 550
        LANE_H = 120

        EVENT_W = 30
        EVENT_H = 30
        TASK_W = 100
        TASK_H = 50

        # Center Y position
        centerY = LANE_Y + (LANE_H / 2)
        eventY = centerY - (EVENT_H / 2)
        taskY = centerY - (TASK_H / 2)

        # X positions for elements (left to right)
        xPositions = [
            LANE_X + 30,           # Start
            LANE_X + 100,          # Submit Document
            LANE_X + 250,          # Review Document
            LANE_X + 400           # End
        ]

        # Unmask lane
        unmaskElement(dh, lane, LANE_X, LANE_Y, LANE_W, LANE_H)

        # Unmask elements
        for i in range(len(elements)):
            el = elements[i]
            x = xPositions[i]

            if (isinstance(el, BpmnStartEvent) or isinstance(el, BpmnEndEvent)):
                unmaskElement(dh, el, x, eventY, EVENT_W, EVENT_H)
            else:
                unmaskElement(dh, el, x, taskY, TASK_W, TASK_H)

        # Unmask flows
        for flow in flows:
            unmaskFlow(dh, flow)

        # Save and close diagram handle
        dh.save()
        dh.close()

        print "Diagram layout completed"
    else:
        print "WARNING: Could not get diagram handle"

    return diagram


def buildProcess(package):
    """Build the complete BPMN Document Approval Process"""

    # Create process
    process = createBpmnProcess(package)
    print "Created process: " + process.getName()

    # Create lane set and lane
    laneSet = createLaneSet(process)
    reviewerLane = createLane(laneSet, "Reviewer")
    print "Created lane: " + reviewerLane.getName()

    # Create flow elements
    startEvent = createStartEvent(process, "Start")
    submitTask = createUserTask(process, "Submit Document")
    reviewTask = createUserTask(process, "Review Document")
    endEvent = createEndEvent(process, "End")
    print "Created 4 flow elements"

    # Add elements to lane
    addToLane(reviewerLane, startEvent)
    addToLane(reviewerLane, submitTask)
    addToLane(reviewerLane, reviewTask)
    addToLane(reviewerLane, endEvent)
    print "Added elements to lane"

    # Create sequence flows
    flow1 = createSequenceFlow(process, startEvent, submitTask)
    flow2 = createSequenceFlow(process, submitTask, reviewTask)
    flow3 = createSequenceFlow(process, reviewTask, endEvent)
    print "Created 3 sequence flows"

    # Create diagram and layout
    elements = [startEvent, submitTask, reviewTask, endEvent]
    flows = [flow1, flow2, flow3]
    createDiagramAndLayout(process, reviewerLane, elements, flows)

    print ""
    print "SUCCESS: Document Approval Process created!"
    return process


#
# The macro execution starts here
#
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        if (element.getStatus().isModifiable()):
            buildProcess(element)
        else:
            print "ERROR: The selected package is not modifiable!"
    else:
        print "ERROR: Please select a Package to create the BPMN process."
else:
    print "ERROR: Please select a Package."


# Modelio output:
# Created process: Document Approval Process
# Created lane: Reviewer
# Created 4 flow elements
# Added elements to lane
# Created 3 sequence flows
# Created diagram: Document Approval Process Diagram
# Diagram layout completed
#
# SUCCESS: Document Approval Process created!
