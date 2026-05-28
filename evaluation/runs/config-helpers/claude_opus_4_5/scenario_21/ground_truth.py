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

    "lanes": ["Logistics", "Secretary", "Warehouse"],

    "elements": [
        ("Insure parcel", USER_TASK, "Logistics"),
        ("Write package label", USER_TASK, "Secretary"),
        ("Clarify shipment method", USER_TASK, "Secretary"),
        ("Get 3 offers from logistic companies", USER_TASK, "Secretary"),
        ("Select logistic company and place order", USER_TASK, "Secretary"),
        ("Package goods", USER_TASK, "Warehouse"),
        ("Prepare for picking up goods", USER_TASK, "Warehouse"),
        ("Special sandling?", EXCLUSIVE_GW, "Secretary"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Secretary"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Warehouse"),
        ("ParallelGateway_1", PARALLEL_GW, "Secretary"),
        ("InclusiveGateway_1", INCLUSIVE_GW, "Secretary"),
        ("InclusiveGateway_2", INCLUSIVE_GW, "Secretary"),
        ("Ship goods", START, "Secretary"),
        ("Shipment prepared", END, "Warehouse"),
    ],

    "flows": [
        ("Special sandling?", "InclusiveGateway_1", "no"),
        ("InclusiveGateway_1", "Insure parcel", "If insurance necessary"),
        ("InclusiveGateway_1", "Write package label", "always"),
        ("Write package label", "InclusiveGateway_2", ""),
        ("Insure parcel", "InclusiveGateway_2", ""),
        ("Ship goods", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Clarify shipment method", ""),
        ("Clarify shipment method", "Special sandling?", ""),
        ("Special sandling?", "Get 3 offers from logistic companies", "yes"),
        ("Get 3 offers from logistic companies", "Select logistic company and place order", ""),
        ("Select logistic company and place order", "ExclusiveGateway_2", ""),
        ("InclusiveGateway_2", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_3", ""),
        ("Package goods", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_3", "Prepare for picking up goods", ""),
        ("Prepare for picking up goods", "Shipment prepared", ""),
        ("ParallelGateway_1", "Package goods", ""),
    ],

    "layout": {
        "Ship goods": 0,
        "ParallelGateway_1": 1,
        "Clarify shipment method": 2,
        "Package goods": 2,
        "Special sandling?": 3,
        "InclusiveGateway_1": 4,
        "Get 3 offers from logistic companies": 4,
        "Prepare for picking up goods": 4,
        "Insure parcel": 5,
        "Write package label": 5,
        "Select logistic company and place order": 5,
        "Shipment prepared": 5,
        "InclusiveGateway_2": 6,
        "ExclusiveGateway_2": 7,
        "ExclusiveGateway_3": 8,
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
