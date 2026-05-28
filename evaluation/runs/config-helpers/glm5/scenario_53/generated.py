#
# DismissalProcess.py
#
# Description: BPMN diagram for MSPN dismissal process reviewed by MSPO
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DismissalProcess",
    
    "lanes": ["MSPN", "MSPO"],
    
    "elements": [
        # Start event
        ("Start", START, "MSPN"),
        
        # MSPN activities
        ("Send Dismissal", USER_TASK, "MSPN"),
        
        # MSPO activities
        ("Review Dismissal", USER_TASK, "MSPO"),
        ("Dismissal Valid?", EXCLUSIVE_GW, "MSPO"),
        ("Reject Dismissal", USER_TASK, "MSPO"),
        ("Confirm Dismissal", USER_TASK, "MSPO"),
        
        # End events
        ("End Rejected", END, "MSPO"),
        ("End Confirmed", END, "MSPO"),
    ],
    
    "flows": [
        ("Start", "Send Dismissal", ""),
        ("Send Dismissal", "Review Dismissal", ""),
        ("Review Dismissal", "Dismissal Valid?", ""),
        ("Dismissal Valid?", "Reject Dismissal", "Reject"),
        ("Dismissal Valid?", "Confirm Dismissal", "Confirm"),
        ("Reject Dismissal", "End Rejected", ""),
        ("Confirm Dismissal", "End Confirmed", ""),
    ],
    
    "layout": {
        # Column 0: Start
        "Start": 0,
        
        # Column 1: MSPN sends
        "Send Dismissal": 1,
        
        # Column 2: MSPO reviews
        "Review Dismissal": 2,
        
        # Column 3: Decision point
        "Dismissal Valid?": 3,
        
        # Column 4: Parallel outcomes (auto-stacked)
        "Reject Dismissal": 4,
        "Confirm Dismissal": 4,
        
        # Column 5: End events (auto-stacked)
        "End Rejected": 5,
        "End Confirmed": 5,
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
