#
# CustomerInquiryToOrder.py
#
# Description: Handles customer inquiry through quote approval, order placement, recording, and confirmation.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CustomerInquiryToOrder",

    "lanes": ["Customer", "Sales", "System"],

    "elements": [
        ("Inquiry Received",          MESSAGE_START,   "Sales"),
        ("Collect Customer Info",     USER_TASK,       "Sales"),
        ("Answer Questions",          USER_TASK,       "Sales"),
        ("Customer Interested?",      EXCLUSIVE_GW,    "Sales"),

        ("Guide Product Selection",   USER_TASK,       "Sales"),
        ("End - Not Interested",      END,             "Sales"),

        ("Prepare Quote",             USER_TASK,       "Sales"),
        ("Review and Approve Quote",  USER_TASK,       "Customer"),
        ("Quote Approved?",           EXCLUSIVE_GW,    "Customer"),

        ("Place Order",               USER_TASK,       "Customer"),
        ("End - Quote Rejected",      END,             "Customer"),

        ("Record Order",              SERVICE_TASK,    "System"),
        ("Send Order Confirmation",   SEND_TASK,       "System"),
        ("Order Confirmed",           END,             "Customer"),
    ],

    "flows": [
        ("Inquiry Received",         "Collect Customer Info",    ""),
        ("Collect Customer Info",    "Answer Questions",         ""),
        ("Answer Questions",         "Customer Interested?",     ""),

        ("Customer Interested?",     "Guide Product Selection",  "Yes"),
        ("Customer Interested?",     "End - Not Interested",     "No"),

        ("Guide Product Selection",  "Prepare Quote",            ""),
        ("Prepare Quote",            "Review and Approve Quote",  ""),
        ("Review and Approve Quote", "Quote Approved?",           ""),

        ("Quote Approved?",          "Place Order",              "Approved"),
        ("Quote Approved?",          "End - Quote Rejected",     "Rejected"),

        ("Place Order",              "Record Order",             ""),
        ("Record Order",             "Send Order Confirmation",  ""),
        ("Send Order Confirmation",  "Order Confirmed",          ""),
    ],

    "layout": {
        "Inquiry Received":          0,
        "Collect Customer Info":     1,
        "Answer Questions":          2,
        "Customer Interested?":      3,

        # Same lane + same column => auto-stacked branch targets
        "Guide Product Selection":   4,
        "End - Not Interested":      4,

        "Prepare Quote":             5,
        "Review and Approve Quote":  6,
        "Quote Approved?":           7,

        # Same lane + same column => auto-stacked branch targets
        "Place Order":               8,
        "End - Quote Rejected":      8,

        "Record Order":              9,
        "Send Order Confirmation":   10,
        "Order Confirmed":           11,
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
