#
# ComplaintHandling.py
#
# Description: Customer Complaint Handling Process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CustomerComplaintHandling",
    
    "lanes": ["Customer", "Customer Service", "Investigation Team", "Financial Team"],
    
    "elements": [
        # Start
        ("Complaint Filed", START, "Customer"),
        
        # Customer Service Tasks
        ("Log & Assign Complaint", USER_TASK, "Customer Service"),
        ("Notify Customer", USER_TASK, "Customer Service"),
        ("Mark Resolved", USER_TASK, "Customer Service"),
        
        # Investigation Team Tasks
        ("Investigate Complaint", USER_TASK, "Investigation Team"),
        ("Valid & Refund?", EXCLUSIVE_GW, "Investigation Team"),
        
        # Financial Team Tasks
        ("Process Refund", SERVICE_TASK, "Financial Team"),
        
        # Customer Tasks
        ("Provide Feedback", USER_TASK, "Customer"),
        
        # End
        ("End", END, "Customer"),
    ],
    
    "flows": [
        ("Complaint Filed", "Log & Assign Complaint", ""),
        ("Log & Assign Complaint", "Investigate Complaint", ""),
        ("Investigate Complaint", "Valid & Refund?", ""),
        
        # Decision Paths
        ("Valid & Refund?", "Process Refund", "Approved"),
        ("Valid & Refund?", "Notify Customer", "Rejected"),
        
        # Convergence
        ("Process Refund", "Notify Customer", ""),
        ("Notify Customer", "Mark Resolved", ""),
        
        # Resolution & Feedback
        ("Mark Resolved", "Provide Feedback", ""),
        ("Provide Feedback", "End", ""),
    ],
    
    "layout": {
        "Complaint Filed":      0,
        "Log & Assign Complaint": 1,
        "Investigate Complaint": 2,
        "Valid & Refund?":      3,
        "Process Refund":       4,
        "Notify Customer":      5,
        "Mark Resolved":        6,
        "Provide Feedback":     7,
        "End":                  8,
    },
    
    "data_objects": [
        ("Complaint Record", "Customer Service", 1),
        ("Investigation Report", "Investigation Team", 2),
        ("Refund Receipt", "Financial Team", 4),
    ],
    
    "data_associations": [
        ("Log & Assign Complaint", "Complaint Record"),
        ("Complaint Record", "Investigate Complaint"),
        ("Investigate Complaint", "Investigation Report"),
        ("Process Refund", "Refund Receipt"),
    ],
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
