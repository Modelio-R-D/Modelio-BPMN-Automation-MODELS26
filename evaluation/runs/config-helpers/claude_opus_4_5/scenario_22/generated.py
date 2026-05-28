#
# SubrogationProcess.py
#
# Description: Insurance recourse/subrogation process handling payment requests,
#              disagreements, and collection agency forwarding
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SubrogationProcess",
    
    "lanes": ["Recourse Handler"],
    
    "elements": [
        # Start
        ("Receive Subrogation Info",     MESSAGE_START,   "Recourse Handler"),
        
        # Initial check
        ("Check Recourse Possibility",   USER_TASK,       "Recourse Handler"),
        ("Recourse Possible?",           EXCLUSIVE_GW,    "Recourse Handler"),
        
        # Not possible path
        ("Close Case - No Recourse",     USER_TASK,       "Recourse Handler"),
        ("End - No Recourse",            END,             "Recourse Handler"),
        
        # Possible path - send request
        ("Send Payment Request",         SEND_TASK,       "Recourse Handler"),
        ("Set Reminder",                 USER_TASK,       "Recourse Handler"),
        
        # Waiting for response
        ("Await Response",               EVENT_BASED_GW,  "Recourse Handler"),
        
        # Payment received
        ("Payment Received",             MESSAGE_CATCH,   "Recourse Handler"),
        ("Make Booking",                 USER_TASK,       "Recourse Handler"),
        ("Close Case - Paid",            USER_TASK,       "Recourse Handler"),
        ("End - Paid",                   END,             "Recourse Handler"),
        
        # Disagreement received
        ("Disagreement Received",        MESSAGE_CATCH,   "Recourse Handler"),
        ("Check Disagreement Reasoning", USER_TASK,       "Recourse Handler"),
        ("Insurant Right?",              EXCLUSIVE_GW,    "Recourse Handler"),
        ("Close Case - Accepted",        USER_TASK,       "Recourse Handler"),
        ("End - Accepted",               END,             "Recourse Handler"),
        
        # Forward to collection
        ("Forward to Collection Agency", SEND_TASK,       "Recourse Handler"),
        ("End - Collection",             END,             "Recourse Handler"),
        
        # Deadline reached
        ("Deadline Reached",             TIMER_CATCH,     "Recourse Handler"),
    ],
    
    "flows": [
        # Initial flow
        ("Receive Subrogation Info",     "Check Recourse Possibility",   ""),
        ("Check Recourse Possibility",   "Recourse Possible?",           ""),
        
        # Not possible
        ("Recourse Possible?",           "Close Case - No Recourse",     "No"),
        ("Close Case - No Recourse",     "End - No Recourse",            ""),
        
        # Possible - send request
        ("Recourse Possible?",           "Send Payment Request",         "Yes"),
        ("Send Payment Request",         "Set Reminder",                 ""),
        ("Set Reminder",                 "Await Response",               ""),
        
        # Event-based gateway outcomes
        ("Await Response",               "Payment Received",             ""),
        ("Await Response",               "Disagreement Received",        ""),
        ("Await Response",               "Deadline Reached",             ""),
        
        # Payment received path
        ("Payment Received",             "Make Booking",                 ""),
        ("Make Booking",                 "Close Case - Paid",            ""),
        ("Close Case - Paid",            "End - Paid",                   ""),
        
        # Disagreement path
        ("Disagreement Received",        "Check Disagreement Reasoning", ""),
        ("Check Disagreement Reasoning", "Insurant Right?",              ""),
        ("Insurant Right?",              "Close Case - Accepted",        "Yes"),
        ("Close Case - Accepted",        "End - Accepted",               ""),
        ("Insurant Right?",              "Forward to Collection Agency", "No"),
        
        # Deadline path
        ("Deadline Reached",             "Forward to Collection Agency", ""),
        
        # Collection end
        ("Forward to Collection Agency", "End - Collection",             ""),
    ],
    
    "layout": {
        # Start and initial check
        "Receive Subrogation Info":      0,
        "Check Recourse Possibility":    1,
        "Recourse Possible?":            2,
        
        # No recourse path (stacked below main flow)
        "Close Case - No Recourse":      (3, 120),
        "End - No Recourse":             (4, 120),
        
        # Yes path - send request
        "Send Payment Request":          3,
        "Set Reminder":                  4,
        "Await Response":                5,
        
        # Three event catches (auto-stacked in column 6)
        "Payment Received":              6,
        "Disagreement Received":         6,
        "Deadline Reached":              6,
        
        # Payment path
        "Make Booking":                  7,
        "Close Case - Paid":             8,
        "End - Paid":                    9,
        
        # Disagreement path (stacked below)
        "Check Disagreement Reasoning":  (7, 90),
        "Insurant Right?":               (8, 90),
        "Close Case - Accepted":         (9, 90),
        "End - Accepted":                (10, 90),
        
        # Collection path (stacked below disagreement)
        "Forward to Collection Agency":  (9, 180),
        "End - Collection":              (10, 180),
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
