#
# Process_1.py
#
# Auto-generated from BPMN XML: Process_1
# Compatible with BPMN_Helpers.py v3.2
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Develop basic design", USER_TASK, "Process 1"),
        ("Order Lego brick sets", USER_TASK, "Process 1"),
        ("Test subcomponent 1", SERVICE_TASK, "Process 1"),
        ("Test subcomponent 2", SERVICE_TASK, "Process 1"),
        ("Test subcomponent 3", SERVICE_TASK, "Process 1"),
        ("Test subcomponent 4", SERVICE_TASK, "Process 1"),
        ("Give the lego sets to the children", MANUAL_TASK, "Process 1"),
        ("Sort the parts into containers", MANUAL_TASK, "Process 1"),
        ("Build the next subcomponent", MANUAL_TASK, "Process 1"),
        ("Reorder parts", MANUAL_TASK, "Process 1"),
        ("Assemble subcomponents", MANUAL_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("Parts remained?", EXCLUSIVE_GW, "Process 1"),
        ("Container empty?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("All tests successfull?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("Brick sets already ordered?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("New order received", START, "Process 1"),
        ("Machine assembled", END, "Process 1"),
    ],

    "flows": [
        ("New order received", "ExclusiveGateway_6", ""),
        ("Order Lego brick sets", "Give the lego sets to the children", ""),
        ("Give the lego sets to the children", "Sort the parts into containers", ""),
        ("Parts remained?", "ExclusiveGateway_1", "Yes"),
        ("ExclusiveGateway_1", "Container empty?", ""),
        ("ExclusiveGateway_4", "Build the next subcomponent", ""),
        ("Build the next subcomponent", "Parts remained?", ""),
        ("Container empty?", "Reorder parts", "Yes"),
        ("Reorder parts", "ExclusiveGateway_4", ""),
        ("Container empty?", "ExclusiveGateway_4", "No"),
        ("ParallelGateway_1", "Test subcomponent 1", ""),
        ("ParallelGateway_1", "Test subcomponent 4", ""),
        ("Test subcomponent 4", "ParallelGateway_2", ""),
        ("Test subcomponent 3", "ParallelGateway_2", ""),
        ("Test subcomponent 1", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "All tests successfull?", ""),
        ("Assemble subcomponents", "Machine assembled", ""),
        ("Test subcomponent 2", "ParallelGateway_2", ""),
        ("ExclusiveGateway_6", "Develop basic design", ""),
        ("All tests successfull?", "ExclusiveGateway_6", "No"),
        ("All tests successfull?", "Assemble subcomponents", "Yes"),
        ("Parts remained?", "ParallelGateway_1", "No"),
        ("Develop basic design", "Brick sets already ordered?", ""),
        ("Brick sets already ordered?", "Order Lego brick sets", "No"),
        ("Sort the parts into containers", "ExclusiveGateway_8", ""),
        ("ExclusiveGateway_8", "ExclusiveGateway_1", ""),
        ("Brick sets already ordered?", "ExclusiveGateway_8", "Yes"),
        ("ParallelGateway_1", "Test subcomponent 2", ""),
        ("ParallelGateway_1", "Test subcomponent 3", ""),
    ],

    "layout": {
        "New order received": 0,
        "Develop basic design": 2,
        "Brick sets already ordered?": 3,
        "Order Lego brick sets": 4,
        "Give the lego sets to the children": 5,
        "Sort the parts into containers": 6,
        "Container empty?": 6,
        "ExclusiveGateway_8": 7,
        "Reorder parts": 7,
        "ExclusiveGateway_4": 8,
        "Build the next subcomponent": 9,
        "Parts remained?": 10,
        "ExclusiveGateway_1": 11,
        "ParallelGateway_1": 11,
        "Test subcomponent 1": 12,
        "Test subcomponent 4": 12,
        "Test subcomponent 2": 12,
        "Test subcomponent 3": 12,
        "ParallelGateway_2": 13,
        "All tests successfull?": 14,
        "ExclusiveGateway_6": 15,
        "Assemble subcomponents": 15,
        "Machine assembled": 16,
    },
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
