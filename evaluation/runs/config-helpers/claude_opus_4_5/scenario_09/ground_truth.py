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
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Discard prototype", USER_TASK, "Process 1"),
        ("Identify idea for new product or improvement", USER_TASK, "Process 1"),
        ("Collect feedback from testing phase", USER_TASK, "Process 1"),
        ("Test market potential", USER_TASK, "Process 1"),
        ("Refine prototype", USER_TASK, "Process 1"),
        ("Test functionality", USER_TASK, "Process 1"),
        ("Approve prototype for further development", USER_TASK, "Process 1"),
        ("Select promising design", USER_TASK, "Process 1"),
        ("Conduct initial research", USER_TASK, "Process 1"),
        ("Draft design concepts", USER_TASK, "Process 1"),
        ("Test safety", USER_TASK, "Process 1"),
        ("Conduct feasibility studies", USER_TASK, "Process 1"),
        ("Build prototype", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Start", "Identify idea for new product or improvement", ""),
        ("ParallelGateway_1", "Conduct feasibility studies", ""),
        ("Test safety", "ParallelGateway_2", ""),
        ("Refine prototype", "ExclusiveGateway_4", ""),
        ("Approve prototype for further development", "ExclusiveGateway_2", ""),
        ("Identify idea for new product or improvement", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Conduct initial research", ""),
        ("Conduct initial research", "ParallelGateway_4", ""),
        ("ExclusiveGateway_4", "ParallelGateway_3", ""),
        ("ExclusiveGateway_3", "Discard prototype", ""),
        ("ParallelGateway_3", "Test functionality", ""),
        ("ExclusiveGateway_3", "Approve prototype for further development", ""),
        ("Conduct feasibility studies", "ParallelGateway_4", ""),
        ("ParallelGateway_3", "Test safety", ""),
        ("ExclusiveGateway_1", "Refine prototype", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_3", ""),
        ("ParallelGateway_3", "Test market potential", ""),
        ("Select promising design", "Build prototype", ""),
        ("Build prototype", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_2", "End", ""),
        ("ParallelGateway_4", "Draft design concepts", ""),
        ("Collect feedback from testing phase", "ExclusiveGateway_1", ""),
        ("ParallelGateway_2", "Collect feedback from testing phase", ""),
        ("Draft design concepts", "Select promising design", ""),
        ("Test functionality", "ParallelGateway_2", ""),
        ("Test market potential", "ParallelGateway_2", ""),
        ("Discard prototype", "ExclusiveGateway_2", ""),
    ],

    "layout": {
        "Start": 0,
        "Identify idea for new product or improvement": 1,
        "ParallelGateway_1": 2,
        "Conduct feasibility studies": 3,
        "Conduct initial research": 3,
        "ParallelGateway_4": 4,
        "Draft design concepts": 5,
        "Select promising design": 6,
        "Build prototype": 7,
        "ParallelGateway_3": 9,
        "Test functionality": 10,
        "Test safety": 10,
        "Test market potential": 10,
        "ParallelGateway_2": 11,
        "Collect feedback from testing phase": 12,
        "ExclusiveGateway_1": 13,
        "Refine prototype": 14,
        "ExclusiveGateway_3": 14,
        "ExclusiveGateway_4": 15,
        "Discard prototype": 15,
        "Approve prototype for further development": 15,
        "ExclusiveGateway_2": 16,
        "End": 17,
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
