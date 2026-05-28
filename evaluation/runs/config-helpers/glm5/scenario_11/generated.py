#
# SubscriptionService.py
#
# Description: Customer subscription service process from signup to cancellation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SubscriptionService",
    
    "lanes": ["Customer", "System", "Support Team"],
    
    "elements": [
        # --- Customer Lane ---
        ("Subscription Signup",   START,         "Customer"),
        ("Enter Personal Info",   USER_TASK,     "Customer"),
        ("Enter Payment Info",    USER_TASK,     "Customer"),
        ("Cancel Request?",       EXCLUSIVE_GW,  "Customer"),
        ("Submit Cancellation",   USER_TASK,     "Customer"),
        
        # --- System Lane ---
        ("Generate Account",      SERVICE_TASK,  "System"),
        ("Assign Access",         SERVICE_TASK,  "System"),
        ("Trigger Billing",       SERVICE_TASK,  "System"),
        ("Send Updates",          SEND_TASK,     "System"),
        ("Refund or Charge?",     EXCLUSIVE_GW,  "System"),
        ("Apply Refund",          SERVICE_TASK,  "System"),
        ("Apply Charges",         SERVICE_TASK,  "System"),
        ("Settle Balance",        SERVICE_TASK,  "System"),
        
        # --- Support Team Lane ---
        ("Process Cancellation",  USER_TASK,     "Support Team"),
        ("Deactivate Subscription", USER_TASK,   "Support Team"),
        ("Subscription Ended",    END,           "Support Team"),
    ],
    
    "flows": [
        # Signup flow
        ("Subscription Signup", "Enter Personal Info",   ""),
        ("Enter Personal Info", "Enter Payment Info",    ""),
        ("Enter Payment Info", "Generate Account",       ""),
        
        # Account setup flow
        ("Generate Account",    "Assign Access",         ""),
        ("Assign Access",       "Trigger Billing",       ""),
        ("Trigger Billing",     "Send Updates",          ""),
        
        # Subscription loop / cancellation decision
        ("Send Updates",        "Cancel Request?",       ""),
        ("Cancel Request?",     "Submit Cancellation",   "Yes"),
        ("Cancel Request?",     "Send Updates",          "No"),
        
        # Cancellation processing
        ("Submit Cancellation", "Process Cancellation",  ""),
        ("Process Cancellation", "Refund or Charge?",    ""),
        
        # Refund/Charge paths
        ("Refund or Charge?",   "Apply Refund",          "Refund"),
        ("Refund or Charge?",   "Apply Charges",         "Charge"),
        
        # Converge and end
        ("Apply Refund",        "Deactivate Subscription", ""),
        ("Apply Charges",       "Deactivate Subscription", ""),
        ("Deactivate Subscription", "Settle Balance",    ""),
        ("Settle Balance",      "Subscription Ended",    ""),
    ],
    
    "layout": {
        # Column 0-2: Signup phase
        "Subscription Signup":    0,
        "Enter Personal Info":    1,
        "Enter Payment Info":     2,
        
        # Column 3-5: Account setup
        "Generate Account":       3,
        "Assign Access":          4,
        "Trigger Billing":        5,
        
        # Column 6-7: Active subscription loop
        "Send Updates":           6,
        "Cancel Request?":        7,
        
        # Column 8-10: Cancellation initiation
        "Submit Cancellation":    8,
        "Process Cancellation":   9,
        "Refund or Charge?":      10,
        
        # Column 11: Parallel refund/charge (auto-stacked in System lane)
        "Apply Refund":           11,
        "Apply Charges":          11,
        
        # Column 12-14: Closure
        "Deactivate Subscription": 12,
        "Settle Balance":          13,
        "Subscription Ended":      14,
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
