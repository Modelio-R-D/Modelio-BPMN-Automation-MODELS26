#
# OrderFulfillmentProcess.py
#
# Description: E-commerce end-to-end order fulfillment with payment, stock/backorder, parallel packaging+shipping docs,
#              international customs, dispatch, delivery confirmation, feedback, and returns handling.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OrderFulfillmentProcess",

    "lanes": [
        "Customer",
        "Order System",
        "Payment Service",
        "Inventory System",
        "Warehouse",
        "Shipping",
        "Returns",
    ],

    "elements": [
        ("Start",                         START,          "Customer"),
        ("Place Order",                   USER_TASK,      "Customer"),

        ("Record Order Details",          SERVICE_TASK,   "Order System"),
        ("Process Payment",               SERVICE_TASK,   "Payment Service"),
        ("Payment Successful?",           EXCLUSIVE_GW,   "Payment Service"),
        ("Notify Payment Failure",        SEND_TASK,      "Order System"),
        ("Order Cancelled",               END,            "Order System"),

        ("Check Stock Availability",      SERVICE_TASK,   "Inventory System"),
        ("Items In Stock?",               EXCLUSIVE_GW,   "Inventory System"),
        ("Initiate Backorder",            SERVICE_TASK,   "Inventory System"),
        ("Inform Customer of Delay",      SEND_TASK,      "Order System"),
        ("Backorder Received",            MESSAGE_CATCH,  "Inventory System"),

        ("Pick Items",                    MANUAL_TASK,    "Warehouse"),
        ("Quality Control Check",         MANUAL_TASK,    "Warehouse"),

        ("Prepare Packaging and Docs",    PARALLEL_GW,    "Warehouse"),

        ("Package Items",                 MANUAL_TASK,    "Warehouse"),
        ("Gift Wrap Requested?",          EXCLUSIVE_GW,   "Warehouse"),
        ("Gift Wrap",                     MANUAL_TASK,    "Warehouse"),

        ("Prepare Shipping Docs/Labels",  SERVICE_TASK,   "Shipping"),
        ("International Order?",          EXCLUSIVE_GW,   "Shipping"),
        ("Prepare Customs Documentation", SERVICE_TASK,   "Shipping"),

        ("Ready to Dispatch",             PARALLEL_GW,    "Shipping"),
        ("Dispatch Order",                MANUAL_TASK,    "Shipping"),

        ("Send Shipping Confirmation",    SEND_TASK,      "Order System"),
        ("Update Inventory Levels",       SERVICE_TASK,   "Inventory System"),

        ("Delivery Confirmed",            MESSAGE_CATCH,  "Order System"),
        ("Send Feedback Request",         SEND_TASK,      "Order System"),
        ("Issue Reported?",               EXCLUSIVE_GW,   "Order System"),
        ("Order Completed",               END,            "Order System"),

        ("Report Delivery Issue",         USER_TASK,      "Customer"),

        ("Send Return Shipping Label",    SEND_TASK,      "Returns"),
        ("Receive Returned Items",        MANUAL_TASK,    "Returns"),
        ("Inspect Returned Items",        MANUAL_TASK,    "Returns"),
        ("Process Refund or Replacement", SERVICE_TASK,   "Returns"),
        ("Return Completed",              END,            "Returns"),
    ],

    "flows": [
        ("Start",                    "Place Order",                  ""),
        ("Place Order",              "Record Order Details",          ""),

        ("Record Order Details",     "Process Payment",               ""),
        ("Process Payment",          "Payment Successful?",           ""),

        ("Payment Successful?",      "Notify Payment Failure",        "No"),
        ("Notify Payment Failure",   "Order Cancelled",               ""),

        ("Payment Successful?",      "Check Stock Availability",      "Yes"),
        ("Check Stock Availability", "Items In Stock?",               ""),

        ("Items In Stock?",          "Pick Items",                    "Yes"),

        ("Items In Stock?",          "Initiate Backorder",            "No"),
        ("Initiate Backorder",       "Inform Customer of Delay",      ""),
        ("Inform Customer of Delay", "Backorder Received",            ""),
        ("Backorder Received",       "Pick Items",                    ""),

        ("Pick Items",               "Quality Control Check",         ""),
        ("Quality Control Check",    "Prepare Packaging and Docs",    ""),

        ("Prepare Packaging and Docs", "Package Items",               ""),
        ("Prepare Packaging and Docs", "Prepare Shipping Docs/Labels", ""),

        ("Package Items",            "Gift Wrap Requested?",          ""),
        ("Gift Wrap Requested?",     "Gift Wrap",                     "Yes"),
        ("Gift Wrap Requested?",     "Ready to Dispatch",             "No"),
        ("Gift Wrap",                "Ready to Dispatch",             ""),

        ("Prepare Shipping Docs/Labels", "International Order?",       ""),
        ("International Order?",        "Prepare Customs Documentation","Yes"),
        ("International Order?",        "Ready to Dispatch",           "No"),
        ("Prepare Customs Documentation","Ready to Dispatch",          ""),

        ("Ready to Dispatch",        "Dispatch Order",                ""),
        ("Dispatch Order",           "Send Shipping Confirmation",     ""),
        ("Send Shipping Confirmation","Update Inventory Levels",      ""),

        ("Update Inventory Levels",  "Delivery Confirmed",            ""),
        ("Delivery Confirmed",       "Send Feedback Request",         ""),
        ("Send Feedback Request",    "Issue Reported?",               ""),

        ("Issue Reported?",          "Order Completed",               "No"),
        ("Issue Reported?",          "Report Delivery Issue",         "Yes"),

        ("Report Delivery Issue",    "Send Return Shipping Label",    ""),
        ("Send Return Shipping Label","Receive Returned Items",       ""),
        ("Receive Returned Items",   "Inspect Returned Items",        ""),
        ("Inspect Returned Items",   "Process Refund or Replacement", ""),
        ("Process Refund or Replacement", "Return Completed",         ""),
    ],

    "layout": {
        "Start":                          0,
        "Place Order":                    1,

        "Record Order Details":           2,
        "Process Payment":                3,
        "Payment Successful?":            4,

        "Check Stock Availability":       5,
        "Items In Stock?":                6,

        "Notify Payment Failure":         7,
        "Order Cancelled":                8,

        "Initiate Backorder":             7,
        "Inform Customer of Delay":       8,
        "Backorder Received":             9,

        "Pick Items":                     10,
        "Quality Control Check":          11,

        "Prepare Packaging and Docs":     12,

        "Package Items":                  13,
        "Prepare Shipping Docs/Labels":   13,

        "Gift Wrap Requested?":           14,
        "International Order?":           14,

        "Gift Wrap":                      15,
        "Prepare Customs Documentation":  15,

        "Ready to Dispatch":              16,
        "Dispatch Order":                 17,

        "Send Shipping Confirmation":     18,
        "Update Inventory Levels":        19,

        "Delivery Confirmed":             20,
        "Send Feedback Request":          21,
        "Issue Reported?":                22,

        "Order Completed":                23,
        "Report Delivery Issue":          23,

        "Send Return Shipping Label":     24,
        "Receive Returned Items":         25,
        "Inspect Returned Items":         26,
        "Process Refund or Replacement":  27,
        "Return Completed":               28,
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
