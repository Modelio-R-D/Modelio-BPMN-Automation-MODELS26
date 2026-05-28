#
# ExpenseApproval_Generated.py
#
# Description:
#   BPMN Expense Approval process - configuration file.
#   Loads BPMN_Helpers.py automatically via execfile().
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# ============================================================================
# LOAD HELPER LIBRARY
# ============================================================================

# Adjust path if your Modelio version differs
execfile(".modelio/5.4/macros/BPMN_Helpers.py")


# ============================================================================
# PROCESS CONFIGURATION
# ============================================================================

CONFIG = {
    "name": "ExpenseApproval",
    
    # Layout settings (optional)
    "SPACING": 150,
    "TASK_WIDTH": 120,
    "TASK_HEIGHT": 60,
    
    # Lanes (top to bottom)
    "lanes": [
        "Employee",
        "Manager",
        "Finance",
    ],
    
    # Elements: (name, type, lane)
    "elements": [
        # Employee Lane
        ("Expense Incurred",        START,        "Employee"),
        ("Create Expense Report",   USER_TASK,    "Employee"),
        ("Attach Receipts",         USER_TASK,    "Employee"),
        ("Submit Report",           USER_TASK,    "Employee"),
        ("Revise Report",           USER_TASK,    "Employee"),
        ("Provide Additional Info", USER_TASK,    "Employee"),
        ("Expense Rejected",        END,          "Employee"),
        
        # Manager Lane
        ("Review Expense",          USER_TASK,    "Manager"),
        ("Check Policy Compliance", SERVICE_TASK, "Manager"),
        ("Approved?",               EXCLUSIVE_GW, "Manager"),
        ("Request Revision",        USER_TASK,    "Manager"),
        ("Approve Expense",         USER_TASK,    "Manager"),
        
        # Finance Lane
        ("Receive Approved Expense",   SERVICE_TASK, "Finance"),
        ("Validate Expense Details",   SERVICE_TASK, "Finance"),
        ("Details Complete?",          EXCLUSIVE_GW, "Finance"),
        ("Request More Info",          USER_TASK,    "Finance"),
        ("Process Payment",            SERVICE_TASK, "Finance"),
        ("Send Payment Notification",  SERVICE_TASK, "Finance"),
        ("Expense Paid",               MESSAGE_END,  "Finance"),
    ],
    
    # Flows: (source, target, guard)
    "flows": [
        # Employee initial flow
        ("Expense Incurred",        "Create Expense Report", ""),
        ("Create Expense Report",   "Attach Receipts",       ""),
        ("Attach Receipts",         "Submit Report",         ""),
        
        # To Manager
        ("Submit Report",           "Review Expense",        ""),
        
        # Manager review
        ("Review Expense",          "Check Policy Compliance", ""),
        ("Check Policy Compliance", "Approved?",             ""),
        
        # Manager decision
        ("Approved?",               "Request Revision",      "Needs Revision"),
        ("Approved?",               "Expense Rejected",      "Rejected"),
        ("Approved?",               "Approve Expense",       "Approved"),
        
        # Revision loop
        ("Request Revision",        "Revise Report",         ""),
        ("Revise Report",           "Submit Report",         "Resubmit"),
        
        # To Finance
        ("Approve Expense",         "Receive Approved Expense", ""),
        
        # Finance processing
        ("Receive Approved Expense",  "Validate Expense Details", ""),
        ("Validate Expense Details",  "Details Complete?",        ""),
        
        # Finance decision
        ("Details Complete?",         "Request More Info",        "No"),
        ("Details Complete?",         "Process Payment",          "Yes"),
        
        # Info loop
        ("Request More Info",         "Provide Additional Info",  ""),
        ("Provide Additional Info",   "Validate Expense Details", ""),
        
        # Payment
        ("Process Payment",           "Send Payment Notification", ""),
        ("Send Payment Notification", "Expense Paid",              ""),
    ],
    
    # Layout: element name -> column index
    "layout": {
        # Employee Lane
        "Expense Incurred":        0,
        "Create Expense Report":   1,
        "Attach Receipts":         2,
        "Submit Report":           3,
        "Expense Rejected":        5,
        "Revise Report":           6,
        "Provide Additional Info": 7,
        
        # Manager Lane
        "Review Expense":          4,
        "Check Policy Compliance": 5,
        "Approved?":               6,
        "Request Revision":        7,
        "Approve Expense":         8,
        
        # Finance Lane
        "Receive Approved Expense":   9,
        "Validate Expense Details":  10,
        "Details Complete?":         11,
        "Request More Info":         12,
        "Process Payment":           13,
        "Send Payment Notification": 14,
        "Expense Paid":              15,
    },
}


# ============================================================================
# ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
