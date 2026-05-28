#
# Ordering_in_an_Online_Shop.py
#
# Description: BPMN for ordering in an online shop (login, product selection loop, parallel payment/shipment, address entry while waiting for bank confirmation).
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Ordering in an Online Shop",

    "lanes": ["Customer", "E-Shop System", "Bank"],

    "elements": [
        ("Start",                          START,          "Customer"),
        ("Enter credentials",              USER_TASK,      "Customer"),
        ("Check credentials",              SERVICE_TASK,   "E-Shop System"),
        ("Login confirmation",             MESSAGE_CATCH,  "Customer"),
        ("Login successful?",              EXCLUSIVE_GW,   "Customer"),
        ("Stop shopping",                  END,            "Customer"),

        ("Select product",                 USER_TASK,      "Customer"),
        ("Add to cart",                    USER_TASK,      "Customer"),
        ("Save product",                   USER_TASK,      "Customer"),
        ("All products selected?",         EXCLUSIVE_GW,   "Customer"),

        ("Prepare order",                  SERVICE_TASK,   "E-Shop System"),
        ("Prepare payment and shipment",   PARALLEL_GW,    "E-Shop System"),

        ("Prepare shipment",               SERVICE_TASK,   "E-Shop System"),

        ("Enter payment data",             USER_TASK,      "Customer"),
        ("Send payment to bank",           SERVICE_TASK,   "E-Shop System"),
        ("Wait and enter address in parallel", PARALLEL_GW, "E-Shop System"),

        ("Confirm payment",                SERVICE_TASK,   "Bank"),
        ("Payment confirmation received",  MESSAGE_CATCH,  "Customer"),

        ("Enter shipping address",         USER_TASK,      "Customer"),
        ("Billing address different?",     EXCLUSIVE_GW,   "Customer"),
        ("Enter billing address",          USER_TASK,      "Customer"),
        ("Address completed",              TASK,           "Customer"),

        ("Payment and address done",       PARALLEL_GW,    "E-Shop System"),
        ("Ready to complete",              PARALLEL_GW,    "E-Shop System"),
        ("Complete order",                 SERVICE_TASK,   "E-Shop System"),
        ("End",                            END,            "E-Shop System"),
    ],

    "flows": [
        ("Start",                 "Enter credentials",           ""),
        ("Enter credentials",     "Check credentials",           ""),
        ("Check credentials",     "Login confirmation",          ""),
        ("Login confirmation",    "Login successful?",           ""),

        ("Login successful?",     "Select product",              "Yes"),
        ("Login successful?",     "Stop shopping",               "No"),

        ("Select product",        "Add to cart",                 ""),
        ("Add to cart",           "Save product",                ""),
        ("Save product",          "All products selected?",      ""),

        ("All products selected?", "Select product",             "No"),
        ("All products selected?", "Prepare order",              "Yes"),

        ("Prepare order",                 "Prepare payment and shipment", ""),
        ("Prepare payment and shipment",  "Prepare shipment",             ""),
        ("Prepare payment and shipment",  "Enter payment data",           ""),

        ("Enter payment data",      "Send payment to bank",              ""),
        ("Send payment to bank",    "Wait and enter address in parallel",""),

        ("Wait and enter address in parallel", "Confirm payment",               ""),
        ("Confirm payment",                   "Payment confirmation received",   ""),

        ("Wait and enter address in parallel", "Enter shipping address",         ""),
        ("Enter shipping address",             "Billing address different?",     ""),
        ("Billing address different?",         "Enter billing address",          "Yes"),
        ("Billing address different?",         "Address completed",              "No"),
        ("Enter billing address",              "Address completed",              ""),

        ("Payment confirmation received", "Payment and address done", ""),
        ("Address completed",             "Payment and address done", ""),

        ("Prepare shipment",          "Ready to complete", ""),
        ("Payment and address done",  "Ready to complete", ""),

        ("Ready to complete",         "Complete order", ""),
        ("Complete order",            "End",            ""),
    ],

    "layout": {
        "Start":                          0,
        "Enter credentials":              1,
        "Check credentials":              2,
        "Login confirmation":             3,
        "Login successful?":              4,
        "Stop shopping":                  5,

        "Select product":                 5,
        "Add to cart":                    6,
        "Save product":                   7,
        "All products selected?":         8,

        "Prepare order":                  9,
        "Prepare payment and shipment":   10,

        "Prepare shipment":               11,

        "Enter payment data":             11,
        "Send payment to bank":           12,
        "Wait and enter address in parallel": 13,

        "Confirm payment":                14,
        "Payment confirmation received":  15,

        "Enter shipping address":         14,
        "Billing address different?":     15,
        "Enter billing address":          16,
        "Address completed":              17,

        "Payment and address done":       18,
        "Ready to complete":              19,
        "Complete order":                 20,
        "End":                            21,
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
