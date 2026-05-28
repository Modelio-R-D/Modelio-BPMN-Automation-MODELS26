#
# TicketBookingProcess.py
#
# Description: Travel ticket booking process from search to journey completion
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "TicketBookingProcess",
    
    "lanes": ["Customer", "Booking System", "Travel Company"],
    
    "elements": [
        # Customer lane
        ("Search Tickets",          USER_TASK,     "Customer"),
        ("Select Route and Time",   USER_TASK,     "Customer"),
        ("Provide Details",         USER_TASK,     "Customer"),
        ("Receive Ticket",          RECEIVE_TASK,  "Customer"),
        ("Receive Reminders",       MESSAGE_CATCH, "Customer"),
        ("Complete Journey",        USER_TASK,     "Customer"),
        ("Provide Feedback",        USER_TASK,     "Customer"),
        ("End",                     END,           "Customer"),
        
        # Booking System lane
        ("Start",                   START,         "Booking System"),
        ("Process Payment",         SERVICE_TASK,  "Booking System"),
        ("Payment OK?",             EXCLUSIVE_GW,  "Booking System"),
        ("Generate Ticket",         SERVICE_TASK,  "Booking System"),
        ("Send Ticket",             SEND_TASK,     "Booking System"),
        ("Send Reminders",          SEND_TASK,     "Booking System"),
        ("Payment Failed",          END,           "Booking System"),
        
        # Travel Company lane
        ("Update Inventory",        SERVICE_TASK,  "Travel Company"),
        ("Prepare Check-in Info",   SERVICE_TASK,  "Travel Company"),
    ],
    
    "data_objects": [
        ("Search Criteria",    "Customer",        1),
        ("Booking Details",    "Customer",        3),
        ("E-Ticket",           "Booking System",  6),
        ("Travel Instructions", "Travel Company", 8),
    ],
    
    "data_associations": [
        ("Search Tickets",       "Search Criteria"),
        ("Search Criteria",      "Select Route and Time"),
        ("Provide Details",      "Booking Details"),
        ("Booking Details",      "Process Payment"),
        ("Generate Ticket",      "E-Ticket"),
        ("E-Ticket",             "Send Ticket"),
        ("Prepare Check-in Info", "Travel Instructions"),
        ("Travel Instructions",  "Send Reminders"),
    ],
    
    "flows": [
        # Main flow
        ("Start",                "Search Tickets",        ""),
        ("Search Tickets",       "Select Route and Time", ""),
        ("Select Route and Time", "Provide Details",      ""),
        ("Provide Details",      "Process Payment",       ""),
        ("Process Payment",      "Payment OK?",           ""),
        
        # Payment gateway
        ("Payment OK?",          "Generate Ticket",       "Yes"),
        ("Payment OK?",          "Payment Failed",        "No"),
        
        # Successful booking flow
        ("Generate Ticket",      "Send Ticket",           ""),
        ("Generate Ticket",      "Update Inventory",      ""),
        ("Send Ticket",          "Receive Ticket",        ""),
        ("Update Inventory",     "Prepare Check-in Info", ""),
        ("Prepare Check-in Info", "Send Reminders",       ""),
        ("Send Reminders",       "Receive Reminders",     ""),
        ("Receive Ticket",       "Receive Reminders",     ""),
        ("Receive Reminders",    "Complete Journey",      ""),
        ("Complete Journey",     "Provide Feedback",      ""),
        ("Provide Feedback",     "End",                   ""),
    ],
    
    "layout": {
        # Booking System lane
        "Start":               0,
        "Process Payment":     4,
        "Payment OK?":         5,
        "Generate Ticket":     6,
        "Send Ticket":         7,
        "Send Reminders":      9,
        "Payment Failed":      6,
        
        # Customer lane
        "Search Tickets":      1,
        "Select Route and Time": 2,
        "Provide Details":     3,
        "Receive Ticket":      8,
        "Receive Reminders":   10,
        "Complete Journey":    11,
        "Provide Feedback":    12,
        "End":                 13,
        
        # Travel Company lane
        "Update Inventory":    7,
        "Prepare Check-in Info": 8,
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
