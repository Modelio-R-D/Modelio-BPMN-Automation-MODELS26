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
        ("Read order", SERVICE_TASK, "Process 1"),
        ("Check if product is in stock", SERVICE_TASK, "Process 1"),
        ("Reorder from wholesaler", SERVICE_TASK, "Process 1"),
        ("Waiting until arrives (handling system)", SERVICE_TASK, "Process 1"),
        ("Demand delivery delay penalty from the wholesaler", SERVICE_TASK, "Process 1"),
        ("Withdraw the Product from warehouse", MANUAL_TASK, "Process 1"),
        ("Register in stock management system", MANUAL_TASK, "Process 1"),
        ("Check if the whole order is ready for shipment", MANUAL_TASK, "Process 1"),
        ("Packing the products", MANUAL_TASK, "Process 1"),
        ("Shipping the order", MANUAL_TASK, "Process 1"),
        ("Courier is requested", MANUAL_TASK, "Process 1"),
        ("Is in stock?", EXCLUSIVE_GW, "Process 1"),
        ("Arrived after more than ten days?", EXCLUSIVE_GW, "Process 1"),
        ("Order is ready for shipment?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Storage management", START, "Process 1"),
        ("Order was shipped", END, "Process 1"),
    ],

    "flows": [
        ("Storage management", "Read order", ""),
        ("Read order", "ExclusiveGateway_5", ""),
        ("Check if product is in stock", "Is in stock?", ""),
        ("Is in stock?", "Withdraw the Product from warehouse", "Yes"),
        ("Is in stock?", "Reorder from wholesaler", "No"),
        ("Reorder from wholesaler", "Waiting until arrives (handling system)", ""),
        ("Waiting until arrives (handling system)", "Arrived after more than ten days?", ""),
        ("Demand delivery delay penalty from the wholesaler", "ExclusiveGateway_4", ""),
        ("Arrived after more than ten days?", "Demand delivery delay penalty from the wholesaler", "Yes"),
        ("Withdraw the Product from warehouse", "Check if the whole order is ready for shipment", ""),
        ("Register in stock management system", "Check if the whole order is ready for shipment", ""),
        ("Check if the whole order is ready for shipment", "Order is ready for shipment?", ""),
        ("Shipping the order", "Order was shipped", ""),
        ("ExclusiveGateway_4", "Register in stock management system", ""),
        ("ExclusiveGateway_5", "Check if product is in stock", ""),
        ("Order is ready for shipment?", "ExclusiveGateway_5", "No"),
        ("Arrived after more than ten days?", "ExclusiveGateway_4", "No"),
        ("ParallelGateway_2", "Shipping the order", ""),
        ("ParallelGateway_1", "Courier is requested", ""),
        ("Order is ready for shipment?", "ParallelGateway_1", "Yes"),
        ("Packing the products", "ParallelGateway_2", ""),
        ("Courier is requested", "ParallelGateway_2", ""),
        ("ParallelGateway_1", "Packing the products", ""),
    ],

    "layout": {
        "Storage management": 0,
        "Read order": 1,
        "Check if product is in stock": 3,
        "Is in stock?": 4,
        "Withdraw the Product from warehouse": 5,
        "Reorder from wholesaler": 5,
        "Waiting until arrives (handling system)": 6,
        "Order is ready for shipment?": 7,
        "Arrived after more than ten days?": 7,
        "ExclusiveGateway_5": 8,
        "ParallelGateway_1": 8,
        "Demand delivery delay penalty from the wholesaler": 8,
        "ExclusiveGateway_4": 9,
        "Courier is requested": 9,
        "Packing the products": 9,
        "Register in stock management system": 10,
        "ParallelGateway_2": 10,
        "Check if the whole order is ready for shipment": 11,
        "Shipping the order": 11,
        "Order was shipped": 12,
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
