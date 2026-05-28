#
# ShippingProcess.py
#
# Description: Shipping process with decision paths for large vs small amounts,
#              parallel packaging activities, and coordination between departments.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ShippingProcess",
    
    "lanes": ["Secretary", "Logistics Head", "Warehousemen"],
    
    "elements": [
        # Start
        ("Start",                    START,        "Secretary"),
        
        # Initial clarification
        ("Clarify Shipping",         USER_TASK,    "Secretary"),
        
        # Decision on amount
        ("Large Amount?",            EXCLUSIVE_GW, "Secretary"),
        
        # Large amount path
        ("Invite Logistic Companies", USER_TASK,   "Secretary"),
        ("Select Company",           USER_TASK,    "Secretary"),
        
        # Small amount path - parallel activities
        ("Split Small Amount",       PARALLEL_GW,  "Secretary"),
        ("Write Package Label",      USER_TASK,    "Secretary"),
        ("Insurance Needed?",        EXCLUSIVE_GW, "Logistics Head"),
        ("Take Parcel Insurance",    USER_TASK,    "Logistics Head"),
        ("Skip Insurance",           TASK,         "Logistics Head"),
        ("Merge Insurance",          EXCLUSIVE_GW, "Logistics Head"),
        ("Package Goods",            MANUAL_TASK,  "Warehousemen"),
        ("Join Activities",          PARALLEL_GW,  "Secretary"),
        
        # Merge paths and finish
        ("Merge Paths",              EXCLUSIVE_GW, "Secretary"),
        ("Prepare for Pickup",       MANUAL_TASK,  "Warehousemen"),
        ("End",                      END,          "Warehousemen"),
    ],
    
    "flows": [
        # Main flow
        ("Start",                     "Clarify Shipping",         ""),
        ("Clarify Shipping",          "Large Amount?",            ""),
        
        # Large amount path
        ("Large Amount?",             "Invite Logistic Companies", "Yes"),
        ("Invite Logistic Companies", "Select Company",            ""),
        ("Select Company",            "Merge Paths",               ""),
        
        # Small amount path
        ("Large Amount?",             "Split Small Amount",        "No"),
        
        # Parallel split for small amounts
        ("Split Small Amount",        "Write Package Label",       ""),
        ("Split Small Amount",        "Insurance Needed?",         ""),
        ("Split Small Amount",        "Package Goods",             ""),
        
        # Insurance decision
        ("Insurance Needed?",         "Take Parcel Insurance",     "Yes"),
        ("Insurance Needed?",         "Skip Insurance",            "No"),
        ("Take Parcel Insurance",     "Merge Insurance",           ""),
        ("Skip Insurance",            "Merge Insurance",           ""),
        
        # Join parallel activities
        ("Write Package Label",       "Join Activities",           ""),
        ("Merge Insurance",           "Join Activities",           ""),
        ("Package Goods",             "Join Activities",           ""),
        
        # Merge and complete
        ("Join Activities",           "Merge Paths",               ""),
        ("Merge Paths",               "Prepare for Pickup",        ""),
        ("Prepare for Pickup",        "End",                       ""),
    ],
    
    "layout": {
        "Start":                      0,
        "Clarify Shipping":           1,
        "Large Amount?":              2,
        
        # Large amount path (top)
        "Invite Logistic Companies":  3,
        "Select Company":             4,
        
        # Small amount path - parallel gateway
        "Split Small Amount":         3,
        
        # Parallel activities (column 4)
        "Write Package Label":        4,
        "Insurance Needed?":          4,
        "Package Goods":              4,
        
        # Insurance branch (column 5)
        "Take Parcel Insurance":      5,
        "Skip Insurance":             5,
        
        # Merge insurance (column 6)
        "Merge Insurance":            6,
        
        # Join parallel activities
        "Join Activities":            7,
        
        # Final merge and completion
        "Merge Paths":                8,
        "Prepare for Pickup":         9,
        "End":                        10,
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
