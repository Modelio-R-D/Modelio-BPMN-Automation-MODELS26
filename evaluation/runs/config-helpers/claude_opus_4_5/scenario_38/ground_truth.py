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

    "lanes": ["Lane_1"],

    "elements": [
        ("Send requirements", USER_TASK, "Lane_1"),
        ("Collect requirements", USER_TASK, "Lane_1"),
        ("Refine requirements", USER_TASK, "Lane_1"),
        ("Create order list", USER_TASK, "Lane_1"),
        ("Place order", USER_TASK, "Lane_1"),
        ("Report for builing permit", SERVICE_TASK, "Lane_1"),
        ("Calculate effort", SERVICE_TASK, "Lane_1"),
        ("Check feasibility", SERVICE_TASK, "Lane_1"),
        ("Call friends", MANUAL_TASK, "Lane_1"),
        ("Build house", MANUAL_TASK, "Lane_1"),
        ("Hire building company", MANUAL_TASK, "Lane_1"),
        ("Draft sufficient?", EXCLUSIVE_GW, "Lane_1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Lane_1"),
        ("Subject to approval?", EXCLUSIVE_GW, "Lane_1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Lane_1"),
        ("Affordable?", EXCLUSIVE_GW, "Lane_1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Lane_1"),
        ("ParallelGateway_1", PARALLEL_GW, "Lane_1"),
        ("ParallelGateway_2", PARALLEL_GW, "Lane_1"),
        ("wish to build a house", START, "Lane_1"),
        ("finished house", END, "Lane_1"),
        ("draft received", MESSAGE_CATCH, "Lane_1"),
        ("Get order", MESSAGE_CATCH, "Lane_1"),
    ],

    "flows": [
        ("wish to build a house", "Collect requirements", ""),
        ("Send requirements", "draft received", ""),
        ("Create order list", "Place order", ""),
        ("draft received", "Check feasibility", ""),
        ("Refine requirements", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "Send requirements", ""),
        ("Collect requirements", "ExclusiveGateway_2", ""),
        ("Subject to approval?", "Report for builing permit", "Yes"),
        ("Draft sufficient?", "Subject to approval?", "Yes"),
        ("Draft sufficient?", "Refine requirements", "No"),
        ("Report for builing permit", "ExclusiveGateway_4", ""),
        ("Subject to approval?", "ExclusiveGateway_4", "No"),
        ("ExclusiveGateway_4", "Create order list", ""),
        ("Place order", "Calculate effort", ""),
        ("Calculate effort", "ParallelGateway_1", ""),
        ("Check feasibility", "Draft sufficient?", ""),
        ("ParallelGateway_1", "Get order", ""),
        ("ParallelGateway_1", "Affordable?", ""),
        ("Affordable?", "Call friends", "No"),
        ("Affordable?", "Hire building company", "Yes"),
        ("Call friends", "ExclusiveGateway_6", ""),
        ("Get order", "ParallelGateway_2", ""),
        ("ExclusiveGateway_6", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Build house", ""),
        ("Build house", "finished house", ""),
        ("Hire building company", "ExclusiveGateway_6", ""),
    ],

    "layout": {
        "wish to build a house": 0,
        "Collect requirements": 1,
        "Send requirements": 3,
        "draft received": 4,
        "Check feasibility": 5,
        "Draft sufficient?": 6,
        "Subject to approval?": 7,
        "Refine requirements": 7,
        "ExclusiveGateway_2": 8,
        "Report for builing permit": 8,
        "ExclusiveGateway_4": 9,
        "Create order list": 10,
        "Place order": 11,
        "Calculate effort": 12,
        "ParallelGateway_1": 13,
        "Get order": 14,
        "Affordable?": 14,
        "Call friends": 15,
        "Hire building company": 15,
        "Build house": 16,
        "ExclusiveGateway_6": 16,
        "ParallelGateway_2": 17,
        "finished house": 17,
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
