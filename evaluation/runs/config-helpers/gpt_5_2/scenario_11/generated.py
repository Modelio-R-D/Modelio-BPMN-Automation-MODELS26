#
# SubscriptionLifecycle.py
#
# Description: Customer signs up, system activates subscription and runs recurring billing/notifications until cancellation; support processes cancellation, applies refund/charges, deactivates subscription, and final balance is settled.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SubscriptionLifecycle",

    "lanes": ["Customer", "System", "Support"],

    "elements": [
        ("Sign Up Start",                 START,           "Customer"),
        ("Enter Personal Info",           USER_TASK,       "Customer"),
        ("Enter Payment Info",            USER_TASK,       "Customer"),

        ("Create Account",                SERVICE_TASK,    "System"),
        ("Assign Access",                 SERVICE_TASK,    "System"),
        ("Activate Subscription",         SERVICE_TASK,    "System"),

        ("Cancel Requested?",             EXCLUSIVE_GW,    "System"),

        ("Billing Cycle Due",             TIMER_CATCH,     "System"),
        ("Run Automated Billing",         SERVICE_TASK,    "System"),
        ("Send Update or Renewal Notice", SEND_TASK,       "System"),

        ("Submit Cancellation Request",   USER_TASK,       "Customer"),
        ("Process Cancellation",          USER_TASK,       "Support"),
        ("Refund or Charge?",             EXCLUSIVE_GW,    "Support"),

        ("Apply Refund",                  SERVICE_TASK,    "System"),
        ("Apply Final Charge",            SERVICE_TASK,    "System"),

        ("Deactivate Subscription",       USER_TASK,       "Support"),
        ("Settle Final Balance",          SERVICE_TASK,    "System"),
        ("Subscription Closed",           END,             "Support"),
    ],

    "data_objects": [
        ("Personal Info",         "Customer",  1),
        ("Payment Details",       "Customer",  2),
        ("Subscription Account",  "System",    3),
        ("Cancellation Request",  "Customer",  7),
        ("Final Statement",       "System",   12),
    ],

    "data_associations": [
        ("Enter Personal Info",         "Personal Info"),
        ("Enter Payment Info",          "Payment Details"),
        ("Payment Details",             "Create Account"),
        ("Create Account",              "Subscription Account"),

        ("Submit Cancellation Request", "Cancellation Request"),
        ("Cancellation Request",        "Process Cancellation"),

        ("Settle Final Balance",        "Final Statement"),
        ("Final Statement",             "Subscription Closed"),
    ],

    "flows": [
        ("Sign Up Start",               "Enter Personal Info",           ""),
        ("Enter Personal Info",         "Enter Payment Info",            ""),
        ("Enter Payment Info",          "Create Account",                ""),
        ("Create Account",              "Assign Access",                 ""),
        ("Assign Access",               "Activate Subscription",         ""),
        ("Activate Subscription",       "Cancel Requested?",             ""),

        # Ongoing subscription loop (billing + notifications)
        ("Cancel Requested?",           "Billing Cycle Due",             "No"),
        ("Billing Cycle Due",           "Run Automated Billing",         ""),
        ("Run Automated Billing",       "Send Update or Renewal Notice", ""),
        ("Send Update or Renewal Notice","Cancel Requested?",            ""),

        # Cancellation path
        ("Cancel Requested?",           "Submit Cancellation Request",   "Yes"),
        ("Submit Cancellation Request", "Process Cancellation",          ""),
        ("Process Cancellation",        "Refund or Charge?",             ""),

        ("Refund or Charge?",           "Apply Refund",                  "Refund"),
        ("Refund or Charge?",           "Apply Final Charge",            "Charge"),
        ("Apply Refund",                "Deactivate Subscription",       ""),
        ("Apply Final Charge",          "Deactivate Subscription",       ""),

        ("Deactivate Subscription",     "Settle Final Balance",          ""),
        ("Settle Final Balance",        "Subscription Closed",           ""),
    ],

    "layout": {
        "Sign Up Start":                  0,
        "Enter Personal Info":            1,
        "Enter Payment Info":             2,

        "Create Account":                 3,
        "Assign Access":                  4,
        "Activate Subscription":          5,

        "Cancel Requested?":              6,

        "Billing Cycle Due":              7,
        "Run Automated Billing":          8,
        "Send Update or Renewal Notice":  9,

        "Submit Cancellation Request":    7,
        "Process Cancellation":           8,
        "Refund or Charge?":              9,

        # Same lane + same column => auto-stacked
        "Apply Refund":                  10,
        "Apply Final Charge":            10,

        "Deactivate Subscription":       11,
        "Settle Final Balance":          12,
        "Subscription Closed":           13,
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
