#
# Storage_management.py
#
# Description: Storage management process from order intake through stock check/reorder, penalty handling, and shipment.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Storage management",

    "lanes": [
        "Order Management System",
        "Warehouse",
        "Wholesaler",
        "Shipping",
    ],

    "elements": [
        ("Start",                         START,          "Order Management System"),
        ("Read order from OMS",           SERVICE_TASK,   "Order Management System"),

        ("Select product from order",     SERVICE_TASK,   "Warehouse"),
        ("Check stock for product",       SERVICE_TASK,   "Warehouse"),
        ("Product in stock?",             EXCLUSIVE_GW,   "Warehouse"),

        ("Withdraw product from warehouse", MANUAL_TASK,  "Warehouse"),

        ("Reorder from wholesaler",       SEND_TASK,      "Wholesaler"),
        ("Delivery arrives",              MESSAGE_CATCH,  "Warehouse"),
        ("Waited more than 10 days?",     EXCLUSIVE_GW,   "Warehouse"),
        ("Demand delivery delay penalty", SERVICE_TASK,   "Wholesaler"),
        ("Register arrived product in stock system", SERVICE_TASK, "Warehouse"),

        ("Whole order ready for shipment?", EXCLUSIVE_GW, "Warehouse"),

        ("Prepare shipment",              PARALLEL_GW,    "Shipping"),
        ("Request courier",               SERVICE_TASK,   "Shipping"),
        ("Pack products",                 MANUAL_TASK,    "Warehouse"),
        ("Ready to ship",                 PARALLEL_GW,    "Shipping"),
        ("Ship order",                    SEND_TASK,      "Shipping"),
        ("End",                           END,            "Shipping"),
    ],

    "flows": [
        ("Start",                       "Read order from OMS", ""),
        ("Read order from OMS",         "Select product from order", ""),

        ("Select product from order",   "Check stock for product", ""),
        ("Check stock for product",     "Product in stock?", ""),

        ("Product in stock?",           "Withdraw product from warehouse", "Yes"),
        ("Product in stock?",           "Reorder from wholesaler", "No"),

        ("Withdraw product from warehouse", "Whole order ready for shipment?", ""),

        ("Reorder from wholesaler",     "Delivery arrives", ""),
        ("Delivery arrives",            "Waited more than 10 days?", ""),

        ("Waited more than 10 days?",   "Demand delivery delay penalty", "Yes"),
        ("Waited more than 10 days?",   "Register arrived product in stock system", "No"),

        ("Demand delivery delay penalty", "Register arrived product in stock system", ""),
        ("Register arrived product in stock system", "Whole order ready for shipment?", ""),

        ("Whole order ready for shipment?", "Prepare shipment", "Yes"),
        ("Whole order ready for shipment?", "Select product from order", "No"),

        ("Prepare shipment",            "Request courier", ""),
        ("Prepare shipment",            "Pack products", ""),

        ("Request courier",             "Ready to ship", ""),
        ("Pack products",               "Ready to ship", ""),

        ("Ready to ship",               "Ship order", ""),
        ("Ship order",                  "End", ""),
    ],

    "layout": {
        "Start":                               0,
        "Read order from OMS":                 1,

        "Select product from order":           2,
        "Check stock for product":             3,
        "Product in stock?":                   4,

        "Withdraw product from warehouse":     5,
        "Reorder from wholesaler":             5,

        "Delivery arrives":                    6,
        "Waited more than 10 days?":           7,
        "Demand delivery delay penalty":       8,
        "Register arrived product in stock system": 9,

        "Whole order ready for shipment?":     10,

        "Prepare shipment":                    11,
        "Request courier":                     12,
        "Pack products":                       12,
        "Ready to ship":                       13,
        "Ship order":                          14,
        "End":                                 15,
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
