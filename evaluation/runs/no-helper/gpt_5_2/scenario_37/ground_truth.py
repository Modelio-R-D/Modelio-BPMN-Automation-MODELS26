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
        ("Query the next shop", USER_TASK, "Process 1"),
        ("Ask about quantity, price and deadline", USER_TASK, "Process 1"),
        ("Create a list of the parts", SERVICE_TASK, "Process 1"),
        ("Reorder the cheapest part", SERVICE_TASK, "Process 1"),
        ("Reorder the part as fast as possible", SERVICE_TASK, "Process 1"),
        ("Receive first batch of parts", MANUAL_TASK, "Process 1"),
        ("Receive second batch of parts", MANUAL_TASK, "Process 1"),
        ("Receive third batch of parts", MANUAL_TASK, "Process 1"),
        ("Start/Continue building", MANUAL_TASK, "Process 1"),
        ("Complain to the friends", MANUAL_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("Terms acceptable?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("More parts needed?", EXCLUSIVE_GW, "Process 1"),
        ("Any stock falls?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("How much is the stock fall?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("Contract fullfilled?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("First parts arrived", COMPLEX_GW, "Process 1"),
        ("Contract project received", START, "Process 1"),
        ("Project completed", END, "Process 1"),
    ],

    "flows": [
        ("Contract project received", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_1", "Query the next shop", ""),
        ("Create a list of the parts", "ExclusiveGateway_3", ""),
        ("Query the next shop", "Ask about quantity, price and deadline", ""),
        ("Ask about quantity, price and deadline", "Terms acceptable?", ""),
        ("Terms acceptable?", "ExclusiveGateway_3", "No"),
        ("Terms acceptable?", "Create a list of the parts", "Yes"),
        ("ExclusiveGateway_3", "More parts needed?", ""),
        ("More parts needed?", "ExclusiveGateway_1", "Yes"),
        ("More parts needed?", "ParallelGateway_1", "No"),
        ("ParallelGateway_1", "Receive first batch of parts", ""),
        ("ParallelGateway_1", "Receive second batch of parts", ""),
        ("ParallelGateway_1", "Receive third batch of parts", ""),
        ("Receive first batch of parts", "First parts arrived", ""),
        ("Receive second batch of parts", "First parts arrived", ""),
        ("Receive third batch of parts", "First parts arrived", ""),
        ("First parts arrived", "Start/Continue building", ""),
        ("Start/Continue building", "Any stock falls?", ""),
        ("Any stock falls?", "How much is the stock fall?", "Yes"),
        ("Reorder the part as fast as possible", "ExclusiveGateway_8", ""),
        ("Reorder the cheapest part", "ExclusiveGateway_8", ""),
        ("Complain to the friends", "ExclusiveGateway_8", ""),
        ("ExclusiveGateway_8", "ExclusiveGateway_6", ""),
        ("Any stock falls?", "ExclusiveGateway_6", "No"),
        ("How much is the stock fall?", "Reorder the cheapest part", "Below 5"),
        ("How much is the stock fall?", "Reorder the part as fast as possible", "Below 3"),
        ("How much is the stock fall?", "Complain to the friends", "Zero"),
        ("ExclusiveGateway_6", "Contract fullfilled?", ""),
        ("Contract fullfilled?", "Start/Continue building", "No"),
        ("Contract fullfilled?", "Project completed", "Yes"),
    ],

    "layout": {
        "Contract project received": 0,
        "Query the next shop": 2,
        "Ask about quantity, price and deadline": 3,
        "Terms acceptable?": 4,
        "Create a list of the parts": 5,
        "ExclusiveGateway_3": 6,
        "More parts needed?": 6,
        "ExclusiveGateway_1": 7,
        "ParallelGateway_1": 7,
        "Receive first batch of parts": 8,
        "Receive second batch of parts": 8,
        "Receive third batch of parts": 8,
        "First parts arrived": 9,
        "Any stock falls?": 11,
        "How much is the stock fall?": 12,
        "Reorder the cheapest part": 13,
        "Reorder the part as fast as possible": 13,
        "Complain to the friends": 13,
        "Contract fullfilled?": 13,
        "Start/Continue building": 14,
        "ExclusiveGateway_8": 14,
        "Project completed": 14,
        "ExclusiveGateway_6": 15,
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
