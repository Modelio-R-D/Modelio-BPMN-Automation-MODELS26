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
        ("Customer brings a defective computer", USER_TASK, "Process 1"),
        ("CRS checks the defect", USER_TASK, "Process 1"),
        ("CRS hands out a repair cost calculation", USER_TASK, "Process 1"),
        ("Client takes her computer home unrepaired", USER_TASK, "Process 1"),
        ("Check the hardware", USER_TASK, "Process 1"),
        ("Check the software", USER_TASK, "Process 1"),
        ("Proper system functionality is tested", USER_TASK, "Process 1"),
        ("Repair is finished", USER_TASK, "Process 1"),
        ("Repair the hardware", USER_TASK, "Process 1"),
        ("Configure the software", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "Customer brings a defective computer", ""),
        ("Customer brings a defective computer", "CRS checks the defect", ""),
        ("CRS checks the defect", "CRS hands out a repair cost calculation", ""),
        ("CRS hands out a repair cost calculation", "ExclusiveGateway_1", ""),
        ("ParallelGateway_1", "Check the hardware", ""),
        ("ParallelGateway_1", "Check the software", ""),
        ("Repair is finished", "ExclusiveGateway_4", ""),
        ("Check the hardware", "Repair the hardware", ""),
        ("Proper system functionality is tested", "ExclusiveGateway_2", ""),
        ("Check the software", "Configure the software", ""),
        ("ParallelGateway_2", "Proper system functionality is tested", ""),
        ("ExclusiveGateway_3", "ParallelGateway_1", ""),
        ("Repair the hardware", "ParallelGateway_2", ""),
        ("Configure the software", "ParallelGateway_2", ""),
        ("ExclusiveGateway_4", "EndEvent_1", ""),
        ("Client takes her computer home unrepaired", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_1", "Client takes her computer home unrepaired", "costs are not acceptable"),
        ("ExclusiveGateway_1", "ExclusiveGateway_3", "costs are acceptable"),
        ("ExclusiveGateway_2", "ExclusiveGateway_3", "error is detected"),
        ("ExclusiveGateway_2", "Repair is finished", "no error"),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Customer brings a defective computer": 1,
        "CRS checks the defect": 2,
        "CRS hands out a repair cost calculation": 3,
        "ExclusiveGateway_1": 4,
        "Client takes her computer home unrepaired": 5,
        "ParallelGateway_1": 6,
        "EndEvent_1": 7,
        "Check the hardware": 7,
        "Check the software": 7,
        "Repair the hardware": 8,
        "Configure the software": 8,
        "ParallelGateway_2": 9,
        "Proper system functionality is tested": 10,
        "ExclusiveGateway_2": 11,
        "ExclusiveGateway_3": 12,
        "Repair is finished": 12,
        "ExclusiveGateway_4": 13,
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
