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
        ("customer waits until bank confirms payment", USER_TASK, "Process 1"),
        ("customer credentials being checked by system", SERVICE_TASK, "Process 1"),
        ("Payment is prepared by system", SERVICE_TASK, "Process 1"),
        ("Shipment is prepared by system", SERVICE_TASK, "Process 1"),
        ("order is being finished by system", SERVICE_TASK, "Process 1"),
        ("customer logs into E-Shop", MANUAL_TASK, "Process 1"),
        ("customer selects a product", MANUAL_TASK, "Process 1"),
        ("customer adds product to shopping cart", MANUAL_TASK, "Process 1"),
        ("customer saves product", MANUAL_TASK, "Process 1"),
        ("customer checks if product was already selected", MANUAL_TASK, "Process 1"),
        ("customer enters payment data", MANUAL_TASK, "Process 1"),
        ("customer enters shipping address", MANUAL_TASK, "Process 1"),
        ("customer enters an independent billing adress", MANUAL_TASK, "Process 1"),
        ("succesful login?", EXCLUSIVE_GW, "Process 1"),
        ("has customer selected all desired products?", EXCLUSIVE_GW, "Process 1"),
        ("if shipping adress == billing adress?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("Open E-Shop Homepage", START, "Process 1"),
        ("Close E-Shop Homepage", END, "Process 1"),
    ],

    "flows": [
        ("Open E-Shop Homepage", "customer logs into E-Shop", ""),
        ("customer logs into E-Shop", "customer credentials being checked by system", ""),
        ("customer credentials being checked by system", "succesful login?", ""),
        ("customer selects a product", "customer adds product to shopping cart", ""),
        ("customer adds product to shopping cart", "customer saves product", ""),
        ("customer saves product", "customer checks if product was already selected", ""),
        ("customer checks if product was already selected", "has customer selected all desired products?", ""),
        ("ParallelGateway_1", "Payment is prepared by system", ""),
        ("ParallelGateway_1", "Shipment is prepared by system", ""),
        ("ParallelGateway_2", "order is being finished by system", ""),
        ("customer enters payment data", "ParallelGateway_3", ""),
        ("Payment is prepared by system", "ParallelGateway_4", ""),
        ("Shipment is prepared by system", "ParallelGateway_4", ""),
        ("ParallelGateway_4", "customer enters payment data", ""),
        ("ParallelGateway_3", "customer enters shipping address", ""),
        ("customer enters shipping address", "if shipping adress == billing adress?", ""),
        ("customer enters an independent billing adress", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_4", "ParallelGateway_2", ""),
        ("if shipping adress == billing adress?", "ExclusiveGateway_4", "Yes"),
        ("if shipping adress == billing adress?", "customer enters an independent billing adress", "No"),
        ("has customer selected all desired products?", "ParallelGateway_1", "Yes"),
        ("order is being finished by system", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_5", "Close E-Shop Homepage", ""),
        ("ExclusiveGateway_6", "customer selects a product", ""),
        ("succesful login?", "ExclusiveGateway_6", "Yes"),
        ("ParallelGateway_3", "customer waits until bank confirms payment", ""),
        ("customer waits until bank confirms payment", "ParallelGateway_2", ""),
        ("has customer selected all desired products?", "ExclusiveGateway_6", "No"),
        ("succesful login?", "ExclusiveGateway_5", "No"),
    ],

    "layout": {
        "Open E-Shop Homepage": 0,
        "customer logs into E-Shop": 1,
        "customer credentials being checked by system": 2,
        "succesful login?": 3,
        "customer selects a product": 5,
        "Close E-Shop Homepage": 5,
        "customer adds product to shopping cart": 6,
        "customer saves product": 7,
        "customer checks if product was already selected": 8,
        "has customer selected all desired products?": 9,
        "ExclusiveGateway_6": 10,
        "ParallelGateway_1": 10,
        "Payment is prepared by system": 11,
        "Shipment is prepared by system": 11,
        "ParallelGateway_4": 12,
        "customer enters payment data": 13,
        "ParallelGateway_3": 14,
        "customer enters shipping address": 15,
        "customer waits until bank confirms payment": 15,
        "if shipping adress == billing adress?": 16,
        "customer enters an independent billing adress": 17,
        "order is being finished by system": 17,
        "ExclusiveGateway_5": 18,
        "ParallelGateway_2": 18,
        "ExclusiveGateway_4": 18,
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
