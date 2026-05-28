#
# SubrogationProcess.py
#
# Description: Insurance subrogation process - handling recourse against insurants
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SubrogationProcess",
    
    "lanes": ["Insurance Clerk"],
    
    "elements": [
        # Start event - triggered by information about possible subrogation
        ("Start", MESSAGE_START, "Insurance Clerk"),
        
        # Initial check and decision
        ("Check Case", USER_TASK, "Insurance Clerk"),
        ("Recourse Possible?", EXCLUSIVE_GW, "Insurance Clerk"),
        
        # Payment request flow
        ("Send Payment Request", USER_TASK, "Insurance Clerk"),
        ("Create Reminder", USER_TASK, "Insurance Clerk"),
        
        # Event-based gateway for waiting
        ("Wait for Response", EVENT_BASED_GW, "Insurance Clerk"),
        
        # Three possible events after payment request
        ("Money Received", MESSAGE_CATCH, "Insurance Clerk"),
        ("Disagreement Received", MESSAGE_CATCH, "Insurance Clerk"),
        ("Deadline Reached", TIMER_CATCH, "Insurance Clerk"),
        
        # Tasks after events
        ("Make Booking", USER_TASK, "Insurance Clerk"),
        ("Check Reasoning", USER_TASK, "Insurance Clerk"),
        ("Insurant Right?", EXCLUSIVE_GW, "Insurance Clerk"),
        ("Forward to Collection", USER_TASK, "Insurance Clerk"),
        
        # End events
        ("End - Case Closed", END, "Insurance Clerk"),
        ("End - No Recourse", END, "Insurance Clerk"),
        ("End - Collected", END, "Insurance Clerk"),
    ],
    
    "flows": [
        # Start and initial check
        ("Start", "Check Case", ""),
        ("Check Case", "Recourse Possible?", ""),
        
        # Decision: Recourse possible?
        ("Recourse Possible?", "Send Payment Request", "Yes"),
        ("Recourse Possible?", "End - No Recourse", "No"),
        
        # Send request and create reminder
        ("Send Payment Request", "Create Reminder", ""),
        ("Create Reminder", "Wait for Response", ""),
        
        # Event-based gateway - three mutually exclusive events
        ("Wait for Response", "Money Received", ""),
        ("Wait for Response", "Disagreement Received", ""),
        ("Wait for Response", "Deadline Reached", ""),
        
        # Path 1: Money received - happy path
        ("Money Received", "Make Booking", ""),
        ("Make Booking", "End - Case Closed", ""),
        
        # Path 2: Disagreement received - check reasoning
        ("Disagreement Received", "Check Reasoning", ""),
        ("Check Reasoning", "Insurant Right?", ""),
        ("Insurant Right?", "End - Case Closed", "Yes"),
        ("Insurant Right?", "Forward to Collection", "No"),
        
        # Path 3: Deadline reached without payment
        ("Deadline Reached", "Forward to Collection", ""),
        ("Forward to Collection", "End - Collected", ""),
    ],
    
    "layout": {
        # Column 0-2: Start and initial check
        "Start": 0,
        "Check Case": 1,
        "Recourse Possible?": 2,
        
        # Column 3: Send request (Yes path) / End (No path stacked below)
        "Send Payment Request": 3,
        "End - No Recourse": (3, 100),
        
        # Column 4-5: Reminder and event-based gateway
        "Create Reminder": 4,
        "Wait for Response": 5,
        
        # Column 6: Three catch events (auto-stacked)
        "Money Received": 6,
        "Disagreement Received": 6,
        "Deadline Reached": 6,
        
        # Column 7: Follow-up tasks (stacked by event row)
        "Make Booking": 7,
        "Check Reasoning": (7, 100),
        
        # Column 8: Decision and collection (stacked)
        "End - Case Closed": (8, 0),
        "Insurant Right?": (8, 100),
        "Forward to Collection": (8, 200),
        
        # Column 9: Final end
        "End - Collected": (9, 200),
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
