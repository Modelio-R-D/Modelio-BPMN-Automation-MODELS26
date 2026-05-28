#
# USICourseRegistration.py
#
# Description: New Application for Registering for a USI Course
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "USI Course Registration",
    
    "lanes": ["Applicant", "USI System"],
    
    "elements": [
        # Column 0
        ("Start", START, "Applicant"),
        
        # Column 1
        ("Select Course", USER_TASK, "Applicant"),
        
        # Column 2
        ("Check Available Slots", SERVICE_TASK, "USI System"),
        
        # Column 3
        ("Slots Free?", EXCLUSIVE_GW, "USI System"),
        
        # Column 4 - different lanes
        ("Display Courses and Dates", SERVICE_TASK, "USI System"),
        ("No Slots Available", END, "Applicant"),
        
        # Column 5
        ("Select Course Date", USER_TASK, "Applicant"),
        
        # Column 6
        ("Has Account?", EXCLUSIVE_GW, "Applicant"),
        
        # Column 7
        ("Check University Registration", SERVICE_TASK, "USI System"),
        
        # Column 8
        ("University Eligible?", EXCLUSIVE_GW, "USI System"),
        
        # Column 9 - auto-stacked (same lane, same column)
        ("Register Account", SERVICE_TASK, "USI System"),
        ("Request Activation", SERVICE_TASK, "USI System"),
        
        # Column 10
        ("Wait for Response", MESSAGE_CATCH, "Applicant"),
        
        # Column 11 - all paths merge here
        ("Log In", USER_TASK, "Applicant"),
        
        # Column 12
        ("Tweet to Friends", USER_TASK, "Applicant"),
        
        # Column 13
        ("Complete Registration", USER_TASK, "Applicant"),
        
        # Column 14
        ("Provide Payment Info", USER_TASK, "Applicant"),
        
        # Column 15
        ("Issue Course Ticket", SERVICE_TASK, "USI System"),
        
        # Column 16
        ("End", END, "Applicant"),
    ],
    
    "flows": [
        # Main flow
        ("Start", "Select Course", ""),
        ("Select Course", "Check Available Slots", ""),
        ("Check Available Slots", "Slots Free?", ""),
        
        # Slots decision
        ("Slots Free?", "Display Courses and Dates", "Yes"),
        ("Slots Free?", "No Slots Available", "No"),
        
        # Continue after slot check
        ("Display Courses and Dates", "Select Course Date", ""),
        ("Select Course Date", "Has Account?", ""),
        
        # Account decision - Yes path skips to Log In
        ("Has Account?", "Log In", "Yes"),
        
        # Account decision - No path goes through university check
        ("Has Account?", "Check University Registration", "No"),
        ("Check University Registration", "University Eligible?", ""),
        
        # University decision
        ("University Eligible?", "Register Account", "Yes"),
        ("University Eligible?", "Request Activation", "No"),
        
        # Paths merge to Log In
        ("Register Account", "Log In", ""),
        ("Request Activation", "Wait for Response", ""),
        ("Wait for Response", "Log In", ""),
        
        # Continue to completion
        ("Log In", "Tweet to Friends", ""),
        ("Tweet to Friends", "Complete Registration", ""),
        ("Complete Registration", "Provide Payment Info", ""),
        ("Provide Payment Info", "Issue Course Ticket", ""),
        ("Issue Course Ticket", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Select Course": 1,
        "Check Available Slots": 2,
        "Slots Free?": 3,
        "Display Courses and Dates": 4,
        "No Slots Available": 4,
        "Select Course Date": 5,
        "Has Account?": 6,
        "Check University Registration": 7,
        "University Eligible?": 8,
        "Register Account": 9,
        "Request Activation": 9,
        "Wait for Response": 10,
        "Log In": 11,
        "Tweet to Friends": 12,
        "Complete Registration": 13,
        "Provide Payment Info": 14,
        "Issue Course Ticket": 15,
        "End": 16,
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
