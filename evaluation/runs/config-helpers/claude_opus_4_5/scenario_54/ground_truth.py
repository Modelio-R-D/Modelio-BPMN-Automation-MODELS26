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
        ("INQ transmits the transaction data request", USER_TASK, "Process 1"),
        ("IP checks the request of the INQ", USER_TASK, "Process 1"),
        ("IP answers the question of the INQ", USER_TASK, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "INQ transmits the transaction data request", ""),
        ("INQ transmits the transaction data request", "IP checks the request of the INQ", ""),
        ("IP checks the request of the INQ", "IP answers the question of the INQ", ""),
        ("IP answers the question of the INQ", "EndEvent_1", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "INQ transmits the transaction data request": 1,
        "IP checks the request of the INQ": 2,
        "IP answers the question of the INQ": 3,
        "EndEvent_1": 4,
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
