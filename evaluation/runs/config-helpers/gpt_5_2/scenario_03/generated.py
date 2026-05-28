#
# InventoryReorderRestock.py
#
# Description: Monitor inventory, trigger reorder at threshold, procure from supplier, receive/inspect stock, record and restock, then update inventory levels.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "InventoryReorderRestock",

    "lanes": [
        "Inventory System",
        "Procurement",
        "Warehouse",
    ],

    "elements": [
        ("Start",                         START,         "Inventory System"),
        ("Monitor Inventory Levels",       SERVICE_TASK,  "Inventory System"),
        ("Stock At Reorder Threshold?",    EXCLUSIVE_GW,  "Inventory System"),

        ("Continue Monitoring",            SERVICE_TASK,  "Inventory System"),

        ("Evaluate Suppliers",             USER_TASK,     "Procurement"),
        ("Place Order",                    USER_TASK,     "Procurement"),

        ("Update Expected Delivery Dates", SERVICE_TASK,  "Inventory System"),

        ("Receive Stock",                  MANUAL_TASK,   "Warehouse"),
        ("Inspect Quality",                MANUAL_TASK,   "Warehouse"),

        ("Record Receipt",                 SERVICE_TASK,  "Inventory System"),
        ("Put Away Stock",                 MANUAL_TASK,   "Warehouse"),

        ("Update Inventory Levels",        SERVICE_TASK,  "Inventory System"),
        ("End",                           END,           "Inventory System"),
    ],

    "data_objects": [
        ("Purchase Order",            "Procurement",      4),
        ("Expected Delivery Dates",   "Inventory System", 5),
        ("Inspection Report",         "Warehouse",        7),
        ("Stock Receipt Record",      "Inventory System", 8),
    ],

    "data_associations": [
        ("Place Order",                    "Purchase Order"),
        ("Purchase Order",                 "Update Expected Delivery Dates"),
        ("Update Expected Delivery Dates",  "Expected Delivery Dates"),
        ("Expected Delivery Dates",        "Receive Stock"),

        ("Inspect Quality",                "Inspection Report"),
        ("Inspection Report",              "Record Receipt"),

        ("Record Receipt",                 "Stock Receipt Record"),
        ("Stock Receipt Record",           "Update Inventory Levels"),
    ],

    "flows": [
        ("Start",                       "Monitor Inventory Levels",        ""),
        ("Monitor Inventory Levels",     "Stock At Reorder Threshold?",     ""),

        ("Stock At Reorder Threshold?",  "Evaluate Suppliers",              "Yes"),
        ("Stock At Reorder Threshold?",  "Continue Monitoring",             "No"),
        ("Continue Monitoring",          "Monitor Inventory Levels",        ""),

        ("Evaluate Suppliers",           "Place Order",                     ""),
        ("Place Order",                  "Update Expected Delivery Dates",  ""),
        ("Update Expected Delivery Dates","Receive Stock",                  ""),

        ("Receive Stock",                "Inspect Quality",                 ""),
        ("Inspect Quality",              "Record Receipt",                  ""),
        ("Record Receipt",               "Put Away Stock",                  ""),
        ("Put Away Stock",               "Update Inventory Levels",         ""),
        ("Update Inventory Levels",      "End",                             ""),
    ],

    "layout": {
        "Start":                          0,
        "Monitor Inventory Levels":        1,
        "Stock At Reorder Threshold?":     2,

        "Continue Monitoring":             3,
        "Evaluate Suppliers":              3,

        "Place Order":                     4,
        "Update Expected Delivery Dates":  5,
        "Receive Stock":                   6,
        "Inspect Quality":                 7,
        "Record Receipt":                  8,
        "Put Away Stock":                  9,
        "Update Inventory Levels":         10,
        "End":                             11,
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
