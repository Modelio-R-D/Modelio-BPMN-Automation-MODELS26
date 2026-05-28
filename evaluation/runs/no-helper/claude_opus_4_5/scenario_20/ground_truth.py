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
        ("Waiter readies cart", USER_TASK, "Process 1"),
        ("Kitchen prepares food", USER_TASK, "Process 1"),
        ("Sommelier fetches wine and prepare alcoholic beverages", USER_TASK, "Process 1"),
        ("Manager takes down the order", USER_TASK, "Process 1"),
        ("Waiter prepares nonalcoholic drinks", USER_TASK, "Process 1"),
        ("Waiter waits/delays debiting", USER_TASK, "Process 1"),
        ("Manager gives order to sommelier", USER_TASK, "Process 1"),
        ("Waiter debits guest's account", USER_TASK, "Process 1"),
        ("Manager submits order ticket to kitchen", USER_TASK, "Process 1"),
        ("Waiter returns to room-service station", USER_TASK, "Process 1"),
        ("Waiter delivers order to guest's room", USER_TASK, "Process 1"),
        ("Manager assigns order to waiter", USER_TASK, "Process 1"),
        ("Guest calls room service", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("ParallelGateway_3", "Manager submits order ticket to kitchen", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_1", ""),
        ("Manager takes down the order", "ParallelGateway_3", ""),
        ("Guest calls room service", "Manager takes down the order", ""),
        ("ExclusiveGateway_2", "Waiter waits/delays debiting", ""),
        ("ParallelGateway_3", "Manager assigns order to waiter", ""),
        ("Manager assigns order to waiter", "ParallelGateway_2", ""),
        ("ParallelGateway_3", "ExclusiveGateway_3", ""),
        ("ParallelGateway_2", "Waiter prepares nonalcoholic drinks", ""),
        ("Waiter debits guest's account", "End", ""),
        ("Waiter returns to room-service station", "ExclusiveGateway_2", ""),
        ("Waiter prepares nonalcoholic drinks", "ParallelGateway_1", ""),
        ("ParallelGateway_2", "Waiter readies cart", ""),
        ("ExclusiveGateway_1", "Waiter debits guest's account", ""),
        ("ExclusiveGateway_4", "ParallelGateway_1", ""),
        ("Kitchen prepares food", "ParallelGateway_1", ""),
        ("ExclusiveGateway_3", "Manager gives order to sommelier", ""),
        ("Start", "Guest calls room service", ""),
        ("Waiter delivers order to guest's room", "Waiter returns to room-service station", ""),
        ("Manager submits order ticket to kitchen", "Kitchen prepares food", ""),
        ("ParallelGateway_1", "Waiter delivers order to guest's room", ""),
        ("Sommelier fetches wine and prepare alcoholic beverages", "ExclusiveGateway_4", ""),
        ("Manager gives order to sommelier", "Sommelier fetches wine and prepare alcoholic beverages", ""),
        ("Waiter waits/delays debiting", "ExclusiveGateway_1", ""),
        ("Waiter readies cart", "ParallelGateway_1", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_4", ""),
    ],

    "layout": {
        "Start": 0,
        "Guest calls room service": 1,
        "Manager takes down the order": 2,
        "ParallelGateway_3": 3,
        "Manager submits order ticket to kitchen": 4,
        "Manager assigns order to waiter": 4,
        "ExclusiveGateway_3": 4,
        "Kitchen prepares food": 5,
        "ParallelGateway_2": 5,
        "Manager gives order to sommelier": 5,
        "Waiter prepares nonalcoholic drinks": 6,
        "Waiter readies cart": 6,
        "Sommelier fetches wine and prepare alcoholic beverages": 6,
        "ExclusiveGateway_4": 7,
        "ParallelGateway_1": 7,
        "Waiter delivers order to guest's room": 7,
        "Waiter returns to room-service station": 8,
        "ExclusiveGateway_2": 9,
        "Waiter waits/delays debiting": 10,
        "ExclusiveGateway_1": 11,
        "Waiter debits guest's account": 11,
        "End": 12,
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
