#
# CustomerComplaintProcess.py
#
# Description: Customer complaint handling process with investigation, refund decision, and feedback collection
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CustomerComplaintProcess",
    
    "lanes": ["Customer", "Customer Service", "Investigation Team", "Finance"],
    
    "elements": [
        # Customer lane
        ("File Complaint",      USER_TASK,     "Customer"),
        ("Receive Decision",    USER_TASK,     "Customer"),
        ("Receive Refund",      USER_TASK,     "Customer"),
        ("Provide Feedback",    USER_TASK,     "Customer"),
        ("End",                 END,           "Customer"),
        
        # Customer Service lane
        ("Start",               START,         "Customer Service"),
        ("Log Complaint",       USER_TASK,     "Customer Service"),
        ("Assign to Dept",      USER_TASK,     "Customer Service"),
        ("Mark Resolved",       USER_TASK,     "Customer Service"),
        
        # Investigation Team lane
        ("Review Details",      USER_TASK,     "Investigation Team"),
        ("Refund Justified?",   EXCLUSIVE_GW,  "Investigation Team"),
        ("Notify Approved",     SEND_TASK,     "Investigation Team"),
        ("Notify Rejected",     SEND_TASK,     "Investigation Team"),
        
        # Finance lane
        ("Process Refund",      SERVICE_TASK,  "Finance"),
    ],
    
    "flows": [
        # Initial flow
        ("Start",             "Log Complaint",     ""),
        ("Log Complaint",     "Assign to Dept",    ""),
        ("Assign to Dept",    "Review Details",    ""),
        
        # Investigation
        ("Review Details",    "Refund Justified?", ""),
        
        # Approved path
        ("Refund Justified?", "Notify Approved",   "Yes"),
        ("Notify Approved",   "Receive Decision",  ""),
        ("Receive Decision",  "Process Refund",    ""),
        ("Process Refund",    "Receive Refund",    ""),
        ("Receive Refund",    "Mark Resolved",     ""),
        
        # Rejected path
        ("Refund Justified?", "Notify Rejected",   "No"),
        ("Notify Rejected",   "Mark Resolved",     ""),
        
        # Final steps
        ("Mark Resolved",     "Provide Feedback",  ""),
        ("Provide Feedback",  "End",               ""),
    ],
    
    "layout": {
        # Customer Service
        "Start":              0,
        "Log Complaint":      1,
        "Assign to Dept":     2,
        "Mark Resolved":      8,
        
        # Investigation Team
        "Review Details":     3,
        "Refund Justified?":  4,
        "Notify Approved":    5,
        "Notify Rejected":    5,
        
        # Customer
        "File Complaint":     0,
        "Receive Decision":   6,
        "Receive Refund":     7,
        "Provide Feedback":   9,
        "End":                10,
        
        # Finance
        "Process Refund":     6,
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
