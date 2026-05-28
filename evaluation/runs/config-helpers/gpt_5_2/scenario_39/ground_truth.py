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
        ("Select type of hardware Issue", USER_TASK, "Process 1"),
        ("Select device model", USER_TASK, "Process 1"),
        ("Write review", USER_TASK, "Process 1"),
        ("Upload video of reparation steps", USER_TASK, "Process 1"),
        ("Get second-hand tools and materials from friends", USER_TASK, "Process 1"),
        ("purchase online", USER_TASK, "Process 1"),
        ("Log into account", USER_TASK, "Process 1"),
        ("Create account", USER_TASK, "Process 1"),
        ("Contact friends", USER_TASK, "Process 1"),
        ("List required materials", SERVICE_TASK, "Process 1"),
        ("List required tools", SERVICE_TASK, "Process 1"),
        ("Offer ordering choices", SERVICE_TASK, "Process 1"),
        ("Display repair instructions", SERVICE_TASK, "Process 1"),
        ("Repair device", MANUAL_TASK, "Process 1"),
        ("Send device to an expert", MANUAL_TASK, "Process 1"),
        ("Is issue fixed?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("Have all required items?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("Have intention to write a review?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("Have intention to upload a video of repair steps?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("Have an account?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_10", EXCLUSIVE_GW, "Process 1"),
        ("Is login Successful?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_12", EXCLUSIVE_GW, "Process 1"),
        ("Have intention to get second-hand items?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_14", EXCLUSIVE_GW, "Process 1"),
        ("Have intention to purchase new items?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_16", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Hardware issue detected", START, "Process 1"),
        ("Hardware issue fixed", END, "Process 1"),
    ],

    "flows": [
        ("ParallelGateway_1", "List required materials", ""),
        ("ParallelGateway_1", "List required tools", ""),
        ("ParallelGateway_1", "Offer ordering choices", ""),
        ("List required materials", "ParallelGateway_2", ""),
        ("List required tools", "ParallelGateway_2", ""),
        ("Offer ordering choices", "ParallelGateway_2", ""),
        ("Select device model", "Select type of hardware Issue", ""),
        ("Select type of hardware Issue", "ParallelGateway_1", ""),
        ("Display repair instructions", "Repair device", ""),
        ("Repair device", "Is issue fixed?", ""),
        ("Send device to an expert", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "Hardware issue fixed", ""),
        ("ExclusiveGateway_4", "Display repair instructions", ""),
        ("Write review", "ExclusiveGateway_6", ""),
        ("ExclusiveGateway_6", "Have intention to upload a video of repair steps?", ""),
        ("Upload video of reparation steps", "ExclusiveGateway_8", ""),
        ("Have intention to upload a video of repair steps?", "ExclusiveGateway_8", "No"),
        ("Have intention to upload a video of repair steps?", "Upload video of reparation steps", "Yes"),
        ("Have intention to write a review?", "Write review", "Yes"),
        ("Have intention to write a review?", "ExclusiveGateway_6", "No"),
        ("ExclusiveGateway_8", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_10", "Log into account", ""),
        ("Log into account", "Is login Successful?", ""),
        ("Is login Successful?", "Select device model", "Yes"),
        ("Is login Successful?", "ExclusiveGateway_10", "No"),
        ("ExclusiveGateway_12", "ExclusiveGateway_10", ""),
        ("Get second-hand tools and materials from friends", "ExclusiveGateway_14", ""),
        ("Have intention to purchase new items?", "purchase online", "Yes"),
        ("purchase online", "ExclusiveGateway_16", ""),
        ("Have intention to get second-hand items?", "ExclusiveGateway_14", "No"),
        ("Have intention to purchase new items?", "ExclusiveGateway_16", "No"),
        ("Create account", "ExclusiveGateway_12", ""),
        ("Hardware issue detected", "Have an account?", ""),
        ("Have an account?", "Create account", "No"),
        ("Have an account?", "ExclusiveGateway_12", "Yes"),
        ("Have all required items?", "Have intention to get second-hand items?", "No"),
        ("ExclusiveGateway_16", "ExclusiveGateway_4", ""),
        ("Is issue fixed?", "Send device to an expert", "No"),
        ("Is issue fixed?", "Have intention to write a review?", "Yes"),
        ("Have intention to get second-hand items?", "Contact friends", "Yes"),
        ("Have all required items?", "ExclusiveGateway_4", "Yes"),
        ("Contact friends", "Get second-hand tools and materials from friends", ""),
        ("ExclusiveGateway_14", "Have intention to purchase new items?", ""),
        ("ParallelGateway_2", "Have all required items?", ""),
    ],

    "layout": {
        "Hardware issue detected": 0,
        "Have an account?": 1,
        "Create account": 2,
        "ExclusiveGateway_12": 3,
        "Log into account": 5,
        "Is login Successful?": 6,
        "ExclusiveGateway_10": 7,
        "Select device model": 7,
        "Select type of hardware Issue": 8,
        "ParallelGateway_1": 9,
        "List required materials": 10,
        "List required tools": 10,
        "Offer ordering choices": 10,
        "ParallelGateway_2": 11,
        "Have all required items?": 12,
        "Have intention to get second-hand items?": 13,
        "Contact friends": 14,
        "Display repair instructions": 14,
        "Have intention to purchase new items?": 15,
        "Get second-hand tools and materials from friends": 15,
        "Repair device": 15,
        "ExclusiveGateway_14": 16,
        "purchase online": 16,
        "Is issue fixed?": 16,
        "ExclusiveGateway_16": 17,
        "Send device to an expert": 17,
        "Have intention to write a review?": 17,
        "ExclusiveGateway_4": 18,
        "Write review": 18,
        "ExclusiveGateway_6": 19,
        "Hardware issue fixed": 19,
        "Have intention to upload a video of repair steps?": 20,
        "Upload video of reparation steps": 21,
        "ExclusiveGateway_2": 22,
        "ExclusiveGateway_8": 22,
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
