#
# SubscriptionLifecycle.py
#
# Description: Customer subscription process from signup through cancellation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SubscriptionLifecycle",
    
    "lanes": ["Customer", "System", "Support Team"],
    
    "elements": [
        # Customer signup
        ("Start",                    START,           "Customer"),
        ("Enter Personal Info",      USER_TASK,       "Customer"),
        ("Enter Payment Info",       USER_TASK,       "Customer"),
        
        # System account setup
        ("Generate Account",         SERVICE_TASK,    "System"),
        ("Assign Access",            SERVICE_TASK,    "System"),
        ("Start Billing Cycle",      SERVICE_TASK,    "System"),
        
        # Ongoing subscription
        ("Send Updates",             SERVICE_TASK,    "System"),
        ("Wait for Event",           EVENT_BASED_GW,  "System"),
        ("Billing Timer",            TIMER_CATCH,     "System"),
        ("Cancellation Request",     MESSAGE_CATCH,   "Customer"),
        ("Process Billing",          SERVICE_TASK,    "System"),
        
        # Cancellation flow
        ("Submit Cancellation",      USER_TASK,       "Customer"),
        ("Review Cancellation",      USER_TASK,       "Support Team"),
        ("Check Terms",              EXCLUSIVE_GW,    "Support Team"),
        ("Process Refund",           SERVICE_TASK,    "Support Team"),
        ("Apply Final Charges",      SERVICE_TASK,    "Support Team"),
        
        # Closure
        ("Deactivate Subscription",  USER_TASK,       "Support Team"),
        ("Settle Account Balance",   SERVICE_TASK,    "Support Team"),
        ("End",                      END,             "Support Team"),
    ],
    
    "flows": [
        # Signup flow
        ("Start",                   "Enter Personal Info",     ""),
        ("Enter Personal Info",     "Enter Payment Info",      ""),
        ("Enter Payment Info",      "Generate Account",        ""),
        
        # Account setup
        ("Generate Account",        "Assign Access",           ""),
        ("Assign Access",           "Start Billing Cycle",     ""),
        ("Start Billing Cycle",     "Send Updates",            ""),
        
        # Subscription loop
        ("Send Updates",            "Wait for Event",          ""),
        ("Wait for Event",          "Billing Timer",           ""),
        ("Wait for Event",          "Cancellation Request",    ""),
        ("Billing Timer",           "Process Billing",         ""),
        ("Process Billing",         "Send Updates",            ""),
        
        # Cancellation path
        ("Cancellation Request",    "Submit Cancellation",     ""),
        ("Submit Cancellation",     "Review Cancellation",     ""),
        ("Review Cancellation",     "Check Terms",             ""),
        ("Check Terms",             "Process Refund",          "Refund Due"),
        ("Check Terms",             "Apply Final Charges",     "Charges Apply"),
        
        # Closure
        ("Process Refund",          "Deactivate Subscription", ""),
        ("Apply Final Charges",     "Deactivate Subscription", ""),
        ("Deactivate Subscription", "Settle Account Balance",  ""),
        ("Settle Account Balance",  "End",                     ""),
    ],
    
    "layout": {
        # Signup (columns 0-2)
        "Start":                   0,
        "Enter Personal Info":     1,
        "Enter Payment Info":      2,
        
        # Account setup (columns 3-5)
        "Generate Account":        3,
        "Assign Access":           4,
        "Start Billing Cycle":     5,
        
        # Subscription loop (columns 6-8)
        "Send Updates":            6,
        "Wait for Event":          7,
        "Billing Timer":           8,    # Auto-stacked with Cancellation Request
        "Cancellation Request":    8,
        "Process Billing":         9,
        
        # Cancellation (columns 9-12)
        "Submit Cancellation":     9,
        "Review Cancellation":     10,
        "Check Terms":             11,
        "Process Refund":          12,   # Auto-stacked with Apply Final Charges
        "Apply Final Charges":     12,
        
        # Closure (columns 13-15)
        "Deactivate Subscription": 13,
        "Settle Account Balance":  14,
        "End":                     15,
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
