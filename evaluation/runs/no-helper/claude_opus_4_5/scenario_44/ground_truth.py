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
        ("Select type of order", USER_TASK, "Process 1"),
        ("Select burger", USER_TASK, "Process 1"),
        ("Select type of beverage", USER_TASK, "Process 1"),
        ("Select side", USER_TASK, "Process 1"),
        ("Select menu", USER_TASK, "Process 1"),
        ("Make payment", USER_TASK, "Process 1"),
        ("Enter customer's name", USER_TASK, "Process 1"),
        ("Prepare beverage", SERVICE_TASK, "Process 1"),
        ("Prepare potato wedges", SERVICE_TASK, "Process 1"),
        ("Prepare French fries", SERVICE_TASK, "Process 1"),
        ("Prepare burger", SERVICE_TASK, "Process 1"),
        ("Check status", SERVICE_TASK, "Process 1"),
        ("Update status", SERVICE_TASK, "Process 1"),
        ("Deliver via conveyor belt", SERVICE_TASK, "Process 1"),
        ("Notify customer", SERVICE_TASK, "Process 1"),
        ("Menu or just the burger ?", EXCLUSIVE_GW, "Process 1"),
        ("Fries or wedges ?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("Is burger ready ?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("Food order decided", START, "Process 1"),
        ("Food delivered", END, "Process 1"),
        ("30 seconds", TIMER_CATCH, "Process 1"),
    ],

    "flows": [
        ("Food order decided", "Select type of order", ""),
        ("Select type of order", "Menu or just the burger ?", ""),
        ("Select type of beverage", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Prepare beverage", ""),
        ("ParallelGateway_1", "Select side", ""),
        ("Prepare beverage", "ParallelGateway_2", ""),
        ("Select side", "ParallelGateway_2", ""),
        ("Prepare potato wedges", "ExclusiveGateway_3", ""),
        ("Prepare French fries", "ExclusiveGateway_3", ""),
        ("Fries or wedges ?", "Prepare potato wedges", "Potato wedges"),
        ("Fries or wedges ?", "Prepare French fries", "French fries"),
        ("ParallelGateway_2", "Fries or wedges ?", ""),
        ("Select menu", "Select type of beverage", ""),
        ("Select burger", "ExclusiveGateway_4", ""),
        ("Menu or just the burger ?", "Select menu", "With menu"),
        ("ExclusiveGateway_3", "ExclusiveGateway_4", ""),
        ("ParallelGateway_3", "ExclusiveGateway_5", ""),
        ("30 seconds", "Check status", ""),
        ("Check status", "Is burger ready ?", ""),
        ("Prepare burger", "ParallelGateway_4", ""),
        ("Deliver via conveyor belt", "Food delivered", ""),
        ("ExclusiveGateway_5", "Update status", ""),
        ("Update status", "30 seconds", ""),
        ("ParallelGateway_4", "Notify customer", ""),
        ("Notify customer", "Deliver via conveyor belt", ""),
        ("Menu or just the burger ?", "Select burger", "Burger only"),
        ("Is burger ready ?", "ExclusiveGateway_5", "No"),
        ("Is burger ready ?", "ParallelGateway_4", "Yes"),
        ("ParallelGateway_3", "Prepare burger", ""),
        ("Make payment", "Enter customer's name", ""),
        ("Enter customer's name", "ParallelGateway_3", ""),
        ("ExclusiveGateway_4", "Make payment", ""),
    ],

    "layout": {
        "Food order decided": 0,
        "Select type of order": 1,
        "Menu or just the burger ?": 2,
        "Select menu": 3,
        "Select burger": 3,
        "Select type of beverage": 4,
        "ParallelGateway_1": 5,
        "Make payment": 5,
        "Prepare beverage": 6,
        "Select side": 6,
        "Enter customer's name": 6,
        "ParallelGateway_2": 7,
        "ParallelGateway_3": 7,
        "Fries or wedges ?": 8,
        "Prepare burger": 8,
        "Prepare potato wedges": 9,
        "Prepare French fries": 9,
        "Update status": 9,
        "ExclusiveGateway_3": 10,
        "30 seconds": 10,
        "Notify customer": 10,
        "ExclusiveGateway_4": 11,
        "Check status": 11,
        "Deliver via conveyor belt": 11,
        "Is burger ready ?": 12,
        "Food delivered": 12,
        "ExclusiveGateway_5": 13,
        "ParallelGateway_4": 13,
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
