#
# OrderFulfillment.py
#
# Description: Order fulfillment from order placement through confirmation, warehouse handling,
# shipping, delivery, and optional post-delivery feedback/returns.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OrderFulfillment",

    "lanes": [
        "Customer",
        "Order System",
        "Warehouse",
        "Logistics Provider"
    ],

    "elements": [
        ("Start",                    START,         "Customer"),
        ("Place Order",              USER_TASK,     "Customer"),

        ("Capture Order",            SERVICE_TASK,  "Order System"),
        ("Send Order Confirmation",  SEND_TASK,     "Order System"),

        ("Pick Items",               MANUAL_TASK,   "Warehouse"),
        ("Pack Items",               MANUAL_TASK,   "Warehouse"),
        ("Generate Shipping Label",  SERVICE_TASK,  "Order System"),
        ("Handover to Logistics",    MANUAL_TASK,   "Warehouse"),

        ("Send Tracking Info",       SEND_TASK,     "Order System"),
        ("Monitor Shipment",         SERVICE_TASK,  "Logistics Provider"),
        ("Deliver Shipment",         MANUAL_TASK,   "Logistics Provider"),

        ("Further Action?",          INCLUSIVE_GW,  "Customer"),
        ("Submit Feedback",          USER_TASK,     "Customer"),
        ("Initiate Return",          USER_TASK,     "Customer"),

        ("Record Feedback",          SERVICE_TASK,  "Order System"),
        ("Authorize Return",         SERVICE_TASK,  "Order System"),
        ("Receive Returned Items",   MANUAL_TASK,   "Warehouse"),
        ("Refund Customer",          SERVICE_TASK,  "Order System"),

        ("Close Out",                INCLUSIVE_GW,  "Customer"),
        ("End",                      END,           "Customer"),
    ],

    "flows": [
        ("Start",                   "Place Order",              ""),
        ("Place Order",             "Capture Order",            ""),

        ("Capture Order",           "Send Order Confirmation",  ""),
        ("Send Order Confirmation", "Pick Items",               ""),

        ("Pick Items",              "Pack Items",               ""),
        ("Pack Items",              "Generate Shipping Label",  ""),
        ("Generate Shipping Label", "Handover to Logistics",    ""),

        ("Handover to Logistics",   "Send Tracking Info",       ""),
        ("Send Tracking Info",      "Monitor Shipment",         ""),
        ("Monitor Shipment",        "Deliver Shipment",         ""),

        ("Deliver Shipment",        "Further Action?",          ""),

        # Post-delivery optional actions (may be none, feedback, return, or both)
        ("Further Action?",         "Submit Feedback",          "Feedback"),
        ("Further Action?",         "Initiate Return",          "Return"),
        ("Further Action?",         "Close Out",                "None"),

        ("Submit Feedback",         "Record Feedback",          ""),
        ("Record Feedback",         "Close Out",                ""),

        ("Initiate Return",         "Authorize Return",         ""),
        ("Authorize Return",        "Receive Returned Items",   ""),
        ("Receive Returned Items",  "Refund Customer",          ""),
        ("Refund Customer",         "Close Out",                ""),

        ("Close Out",               "End",                      ""),
    ],

    "layout": {
        "Start":                    0,
        "Place Order":              1,

        "Capture Order":            2,
        "Send Order Confirmation":  3,

        "Pick Items":               4,
        "Pack Items":               5,
        "Generate Shipping Label":  6,
        "Handover to Logistics":    7,

        "Send Tracking Info":       8,
        "Monitor Shipment":         9,
        "Deliver Shipment":         10,

        "Further Action?":          11,

        # Same lane + same column => auto-stacked
        "Submit Feedback":          12,
        "Initiate Return":          12,

        # Same lane + same column => auto-stacked
        "Record Feedback":          13,
        "Authorize Return":         13,

        "Receive Returned Items":   14,
        "Refund Customer":          15,

        "Close Out":                16,
        "End":                      17,
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
