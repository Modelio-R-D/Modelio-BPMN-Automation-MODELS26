#
# ITSolutionRequest.py
#
# Description: IT Solution Request Process - Employee/Department requests new IT solutions
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ITSolutionRequest",
    
    "lanes": ["Requester", "IT Department"],
    
    "elements": [
        # Start
        ("Start", START, "Requester"),
        
        # Requester activities
        ("Submit IT Request", USER_TASK, "Requester"),
        
        # IT assessment
        ("Assess Request", SERVICE_TASK, "IT Department"),
        ("Approved?", EXCLUSIVE_GW, "IT Department"),
        
        # Rejection path
        ("Notify Rejection", SERVICE_TASK, "IT Department"),
        ("Request Rejected", END, "IT Department"),
        
        # Approval path - Procurement
        ("Procure Tools/Licenses", SERVICE_TASK, "IT Department"),
        ("Install Solution", SERVICE_TASK, "IT Department"),
        
        # Testing
        ("Test Solution", SERVICE_TASK, "IT Department"),
        ("Test Passed?", EXCLUSIVE_GW, "IT Department"),
        
        # Fix loop
        ("Fix Issues", SERVICE_TASK, "IT Department"),
        
        # Deployment
        ("Roll Out to Department", SERVICE_TASK, "IT Department"),
        ("Provide Training", USER_TASK, "IT Department"),
        ("IT Support Available", SERVICE_TASK, "IT Department"),
        ("Solution Deployed", END, "IT Department"),
    ],
    
    "flows": [
        # Request submission
        ("Start", "Submit IT Request", ""),
        ("Submit IT Request", "Assess Request", ""),
        
        # Assessment and decision
        ("Assess Request", "Approved?", ""),
        
        # Rejection path
        ("Approved?", "Notify Rejection", "No"),
        ("Notify Rejection", "Request Rejected", ""),
        
        # Approval path
        ("Approved?", "Procure Tools/Licenses", "Yes"),
        ("Procure Tools/Licenses", "Install Solution", ""),
        ("Install Solution", "Test Solution", ""),
        
        # Testing decision
        ("Test Solution", "Test Passed?", ""),
        
        # Fix loop
        ("Test Passed?", "Fix Issues", "No"),
        ("Fix Issues", "Test Solution", ""),
        
        # Success path
        ("Test Passed?", "Roll Out to Department", "Yes"),
        ("Roll Out to Department", "Provide Training", ""),
        ("Provide Training", "IT Support Available", ""),
        ("IT Support Available", "Solution Deployed", ""),
    ],
    
    "data_objects": [
        ("IT Request", "Requester", 1),
        ("Procurement Order", "IT Department", 4),
        ("Test Report", "IT Department", 6),
    ],
    
    "data_associations": [
        ("Submit IT Request", "IT Request"),
        ("IT Request", "Assess Request"),
        ("Procure Tools/Licenses", "Procurement Order"),
        ("Procurement Order", "Install Solution"),
        ("Test Solution", "Test Report"),
    ],
    
    "layout": {
        # Column 0-1: Requester lane
        "Start": 0,
        "Submit IT Request": 1,
        
        # Column 2-3: IT Assessment
        "Assess Request": 2,
        "Approved?": 3,
        
        # Column 4: Branch split (auto-stacked)
        "Procure Tools/Licenses": 4,  # Yes path (top)
        "Notify Rejection": 4,         # No path (bottom, auto-stacked)
        
        # Column 5: Continue/End
        "Install Solution": 5,         # Yes path (top)
        "Request Rejected": 5,         # No path end (bottom, auto-stacked)
        
        # Column 6-7: Testing
        "Test Solution": 6,
        "Test Passed?": 7,
        
        # Column 8: Branch split (auto-stacked)
        "Roll Out to Department": 8,   # Yes path (top)
        "Fix Issues": 8,               # No path (bottom, auto-stacked)
        
        # Column 9-11: Deployment
        "Provide Training": 9,
        "IT Support Available": 10,
        "Solution Deployed": 11,
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
