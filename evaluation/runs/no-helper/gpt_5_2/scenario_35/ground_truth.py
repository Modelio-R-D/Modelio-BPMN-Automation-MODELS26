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
        ("Determine properties", USER_TASK, "Process 1"),
        ("Check delivery of ordered parts", USER_TASK, "Process 1"),
        ("Perform Inspection", USER_TASK, "Process 1"),
        ("Send first saw", USER_TASK, "Process 1"),
        ("Cancel production of the remaining order", USER_TASK, "Process 1"),
        ("Send the remaining order", USER_TASK, "Process 1"),
        ("Order parts", SERVICE_TASK, "Process 1"),
        ("Order parts", SERVICE_TASK, "Process 1"),
        ("Order parts", SERVICE_TASK, "Process 1"),
        ("Assemble the parts", SERVICE_TASK, "Process 1"),
        ("Send updates", SERVICE_TASK, "Process 1"),
        ("Produce the remaining order", SERVICE_TASK, "Process 1"),
        ("Parts arrived ?", EXCLUSIVE_GW, "Process 1"),
        ("Customer Approval ?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Start", "Determine properties", ""),
        ("Determine properties", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Order parts", ""),
        ("ParallelGateway_1", "Order parts", ""),
        ("Order parts", "ParallelGateway_2", ""),
        ("Order parts", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Check delivery of ordered parts", ""),
        ("Check delivery of ordered parts", "Parts arrived ?", ""),
        ("Parts arrived ?", "Check delivery of ordered parts", "No"),
        ("Parts arrived ?", "Perform Inspection", "Yes"),
        ("Perform Inspection", "Assemble the parts", ""),
        ("Assemble the parts", "Send updates", ""),
        ("Send updates", "Send first saw", ""),
        ("Send first saw", "Customer Approval ?", ""),
        ("Customer Approval ?", "Cancel production of the remaining order", "No"),
        ("Cancel production of the remaining order", "End", ""),
        ("Customer Approval ?", "Produce the remaining order", "Yes"),
        ("Produce the remaining order", "Send the remaining order", ""),
        ("Send the remaining order", "End", ""),
        ("ParallelGateway_1", "Order parts", ""),
        ("Order parts", "ParallelGateway_2", ""),
    ],

    "layout": {
        "Start": 0,
        "Determine properties": 1,
        "ParallelGateway_1": 2,
        "Order parts": 3,
        "ParallelGateway_2": 4,
        "Parts arrived ?": 6,
        "Check delivery of ordered parts": 7,
        "Perform Inspection": 7,
        "Assemble the parts": 8,
        "Send updates": 9,
        "Send first saw": 10,
        "Customer Approval ?": 11,
        "Cancel production of the remaining order": 12,
        "Produce the remaining order": 12,
        "Send the remaining order": 13,
        "End": 14,
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
