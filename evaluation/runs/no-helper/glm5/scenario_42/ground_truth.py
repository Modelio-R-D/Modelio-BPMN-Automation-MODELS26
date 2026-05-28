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
        ("Send a report to the fridge service center", USER_TASK, "Process 1"),
        ("Rate Service Facility", USER_TASK, "Process 1"),
        ("Describe the symptoms", USER_TASK, "Process 1"),
        ("Schedule an appointment for fridge repair", SERVICE_TASK, "Process 1"),
        ("Select local service facility", SERVICE_TASK, "Process 1"),
        ("Confirm that fridge is okay", MANUAL_TASK, "Process 1"),
        ("Repair the fridge", MANUAL_TASK, "Process 1"),
        ("Collect fridge type data", MANUAL_TASK, "Process 1"),
        ("Submit a rating?", EXCLUSIVE_GW, "Process 1"),
        ("Additional parts needed?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Fridge makes strange noises", START, "Process 1"),
        ("Repair process over", END, "Process 1"),
        ("Wait until service facility arrives", TIMER_CATCH, "Process 1"),
    ],

    "flows": [
        ("Rate Service Facility", "Repair process over", ""),
        ("Confirm that fridge is okay", "Submit a rating?", ""),
        ("Send a report to the fridge service center", "Select local service facility", ""),
        ("Schedule an appointment for fridge repair", "Wait until service facility arrives", ""),
        ("Wait until service facility arrives", "Repair the fridge", ""),
        ("Repair the fridge", "Additional parts needed?", ""),
        ("Select local service facility", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_3", "Schedule an appointment for fridge repair", ""),
        ("ParallelGateway_1", "Describe the symptoms", ""),
        ("ParallelGateway_1", "Collect fridge type data", ""),
        ("Additional parts needed?", "Confirm that fridge is okay", "No. Fridge is repaired"),
        ("Submit a rating?", "Rate Service Facility", "Yes"),
        ("Collect fridge type data", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Send a report to the fridge service center", ""),
        ("Describe the symptoms", "ParallelGateway_2", ""),
        ("Fridge makes strange noises", "ParallelGateway_1", ""),
        ("Submit a rating?", "Repair process over", "No"),
        ("Additional parts needed?", "ExclusiveGateway_3", "Yes. Fridge is not repaired"),
    ],

    "layout": {
        "Fridge makes strange noises": 0,
        "ParallelGateway_1": 1,
        "Describe the symptoms": 2,
        "Collect fridge type data": 2,
        "ParallelGateway_2": 3,
        "Send a report to the fridge service center": 4,
        "Select local service facility": 5,
        "Schedule an appointment for fridge repair": 7,
        "Wait until service facility arrives": 8,
        "Repair the fridge": 9,
        "Additional parts needed?": 10,
        "ExclusiveGateway_3": 11,
        "Confirm that fridge is okay": 11,
        "Submit a rating?": 12,
        "Rate Service Facility": 13,
        "Repair process over": 14,
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
