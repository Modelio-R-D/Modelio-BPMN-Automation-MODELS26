#
# BecomingAParent.py
#
# Description: BPMN process for planning, taking and extending maternity leave.
#              Supports parent in selecting leave models, notifying authorities,
#              and managing extensions.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BecomingAParent",
    
    "lanes": ["Parent", "HR System", "Social Security", "Employer"],
    
    "elements": [
        # Start
        ("Start", START, "Parent"),
        
        # Phase 1: Information gathering & selection
        ("Fetch Leave Models", SERVICE_TASK, "HR System"),
        ("Select Leave Model", USER_TASK, "Parent"),
        ("Collect Documents", USER_TASK, "Parent"),
        
        # Phase 2: Notifications
        ("Notify Social Security", SEND_TASK, "HR System"),
        ("Process Registration", SERVICE_TASK, "Social Security"),
        ("Notify Employer", SEND_TASK, "HR System"),
        
        # Phase 3: Company handover
        ("Gather Company Info", USER_TASK, "Employer"),
        ("Prepare Handover", USER_TASK, "Employer"),
        
        # Phase 4: Leave period & extension decision
        ("End of Leave Period", TIMER_CATCH, "HR System"),
        ("Extend Leave?", EXCLUSIVE_GW, "Parent"),
        ("Submit Extension Request", USER_TASK, "Parent"),
        ("Process Extension", SERVICE_TASK, "HR System"),
        
        # End
        ("End", END, "Parent"),
    ],
    
    "flows": [
        ("Start", "Fetch Leave Models", ""),
        ("Fetch Leave Models", "Select Leave Model", ""),
        ("Select Leave Model", "Collect Documents", ""),
        ("Collect Documents", "Notify Social Security", ""),
        ("Notify Social Security", "Process Registration", ""),
        ("Process Registration", "Notify Employer", ""),
        ("Notify Employer", "Gather Company Info", ""),
        ("Gather Company Info", "Prepare Handover", ""),
        ("Prepare Handover", "End of Leave Period", ""),
        ("End of Leave Period", "Extend Leave?", ""),
        ("Extend Leave?", "Submit Extension Request", "Yes"),
        ("Extend Leave?", "End", "No"),
        ("Submit Extension Request", "Process Extension", ""),
        ("Process Extension", "End of Leave Period", ""),
    ],
    
    "data_objects": [
        ("Leave Models", "HR System", 1),
        ("Selected Model", "Parent", 2),
        ("Documents", "Parent", 3),
    ],
    
    "data_associations": [
        ("Fetch Leave Models", "Leave Models"),
        ("Leave Models", "Select Leave Model"),
        ("Select Leave Model", "Selected Model"),
        ("Selected Model", "Collect Documents"),
        ("Collect Documents", "Documents"),
        ("Documents", "Notify Social Security"),
    ],
    
    "layout": {
        "Start": 0,
        "Fetch Leave Models": 1,
        "Select Leave Model": 2,
        "Collect Documents": 3,
        "Notify Social Security": 4,
        "Process Registration": 5,
        "Notify Employer": 6,
        "Gather Company Info": 7,
        "Prepare Handover": 8,
        "End of Leave Period": 9,
        "Extend Leave?": 10,
        "Submit Extension Request": 11,
        "Process Extension": 12,
        "End": 11,  # Stacked with Submit Extension Request
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
