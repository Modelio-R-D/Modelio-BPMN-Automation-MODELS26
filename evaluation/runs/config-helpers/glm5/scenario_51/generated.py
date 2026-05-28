#
# VacationRequestProcess.py
#
# Description: Vacation Request Process - Employee submits request, Supervisor approves/rejects, HR manages approved requests
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "VacationRequest",
    
    "lanes": ["Employee", "Supervisor", "Human Resources"],
    
    "elements": [
        # Employee Lane
        ("Start", START, "Employee"),
        ("Submit Vacation Request", USER_TASK, "Employee"),
        ("Register Request", SERVICE_TASK, "Employee"),
        ("Review Rejection", USER_TASK, "Employee"),
        ("End Rejected", END, "Employee"),
        
        # Supervisor Lane
        ("Review Request", USER_TASK, "Supervisor"),
        ("Approved?", EXCLUSIVE_GW, "Supervisor"),
        ("Notify HR", SEND_TASK, "Supervisor"),
        
        # Human Resources Lane
        ("Complete Procedures", USER_TASK, "Human Resources"),
        ("End Approved", END, "Human Resources"),
    ],
    
    "flows": [
        # Main flow
        ("Start", "Submit Vacation Request", ""),
        ("Submit Vacation Request", "Register Request", ""),
        ("Register Request", "Review Request", ""),
        ("Review Request", "Approved?", ""),
        
        # Rejected path (back to Employee)
        ("Approved?", "Review Rejection", "No"),
        ("Review Rejection", "End Rejected", ""),
        
        # Approved path (to HR)
        ("Approved?", "Notify HR", "Yes"),
        ("Notify HR", "Complete Procedures", ""),
        ("Complete Procedures", "End Approved", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Submit Vacation Request": 1,
        "Register Request": 2,
        "Review Request": 3,
        "Approved?": 4,
        "Review Rejection": 5,
        "Notify HR": 5,
        "Complete Procedures": 6,
        "End Rejected": 6,
        "End Approved": 7,
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
