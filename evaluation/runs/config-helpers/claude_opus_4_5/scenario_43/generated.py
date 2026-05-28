#
# CarService.py
#
# Description: Police app car service reminder process with notifications and fines
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CarServiceProcess",
    
    "lanes": ["System", "Car Owner", "Mechanic"],
    
    "elements": [
        # Start - after previous service
        ("Service Completed",       TIMER_START,        "System"),
        
        # Check registration
        ("Check Registration",      SERVICE_TASK,       "System"),
        ("Registered?",             EXCLUSIVE_GW,       "System"),
        ("End Not Registered",      END,                "System"),
        
        # Notification
        ("Notify Owner",            SEND_TASK,          "System"),
        
        # Owner decision point - service or fine
        ("Wait for Service",        EVENT_BASED_GW,     "Car Owner"),
        ("Service Timeout",         TIMER_CATCH,        "Car Owner"),
        ("Arrive at Service",       RECEIVE_TASK,       "Car Owner"),
        
        # Fine path
        ("Issue Fine",              SERVICE_TASK,       "System"),
        ("End Fined",               END,                "System"),
        
        # Service process
        ("Enter Problems",          USER_TASK,          "Mechanic"),
        ("Perform Repair",          MANUAL_TASK,        "Mechanic"),
        
        # Status updates (parallel with repair)
        ("Send Status Update",      SEND_TASK,          "System"),
        ("Receive Status",          MESSAGE_CATCH,      "Car Owner"),
        ("Repair Complete?",        EXCLUSIVE_GW,       "Mechanic"),
        
        # Payment and completion
        ("Mark Repair Done",        USER_TASK,          "Mechanic"),
        ("Pay via App",             USER_TASK,          "Car Owner"),
        ("Enter Pickerl Success",   USER_TASK,          "Mechanic"),
        ("Enter Next Service Date", USER_TASK,          "Mechanic"),
        ("End Success",             END,                "Mechanic"),
    ],
    
    "flows": [
        # Initial flow
        ("Service Completed",       "Check Registration",   ""),
        ("Check Registration",      "Registered?",          ""),
        ("Registered?",             "End Not Registered",   "No"),
        ("Registered?",             "Notify Owner",         "Yes"),
        ("Notify Owner",            "Wait for Service",     ""),
        
        # Owner decision
        ("Wait for Service",        "Service Timeout",      ""),
        ("Wait for Service",        "Arrive at Service",    ""),
        
        # Fine path
        ("Service Timeout",         "Issue Fine",           "30 days"),
        ("Issue Fine",              "End Fined",            ""),
        
        # Service path
        ("Arrive at Service",       "Enter Problems",       ""),
        ("Enter Problems",          "Perform Repair",       ""),
        ("Perform Repair",          "Send Status Update",   ""),
        ("Send Status Update",      "Receive Status",       ""),
        ("Receive Status",          "Repair Complete?",     ""),
        ("Repair Complete?",        "Perform Repair",       "No"),
        ("Repair Complete?",        "Mark Repair Done",     "Yes"),
        
        # Completion
        ("Mark Repair Done",        "Pay via App",          ""),
        ("Pay via App",             "Enter Pickerl Success",""),
        ("Enter Pickerl Success",   "Enter Next Service Date", ""),
        ("Enter Next Service Date", "End Success",          ""),
    ],
    
    "data_objects": [
        ("Problem Report",      "Mechanic",   7),
        ("Service Record",      "Mechanic",   12),
    ],
    
    "data_associations": [
        ("Enter Problems",          "Problem Report"),
        ("Problem Report",          "Perform Repair"),
        ("Enter Pickerl Success",   "Service Record"),
        ("Service Record",          "Enter Next Service Date"),
    ],
    
    "layout": {
        # Column 0 - Start
        "Service Completed":        0,
        
        # Column 1 - Registration check
        "Check Registration":       1,
        
        # Column 2 - Gateway
        "Registered?":              2,
        
        # Column 3 - Notification / End not registered
        "Notify Owner":             3,
        "End Not Registered":       3,
        
        # Column 4 - Wait for service
        "Wait for Service":         4,
        
        # Column 5 - Timer / Arrive (stacked in Car Owner lane)
        "Service Timeout":          5,
        "Arrive at Service":        5,
        
        # Column 6 - Fine / Enter problems
        "Issue Fine":               6,
        "Enter Problems":           6,
        
        # Column 7 - End fined
        "End Fined":                7,
        
        # Column 8 - Perform repair
        "Perform Repair":           8,
        
        # Column 9 - Status update
        "Send Status Update":       9,
        
        # Column 10 - Receive status
        "Receive Status":           10,
        
        # Column 11 - Repair complete check
        "Repair Complete?":         11,
        
        # Column 12 - Mark done
        "Mark Repair Done":         12,
        
        # Column 13 - Payment
        "Pay via App":              13,
        
        # Column 14 - Pickerl
        "Enter Pickerl Success":    14,
        
        # Column 15 - Next service date
        "Enter Next Service Date":  15,
        
        # Column 16 - End
        "End Success":              16,
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
