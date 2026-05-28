#
# TravelBookingProcess.py
#
# Description: Travel booking process for flight, train, and bus tickets
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "TravelBookingProcess",
    
    "lanes": ["Customer", "Booking System", "Travel Company"],
    
    "elements": [
        # Start Event
        ("Start", START, "Customer"),
        
        # Customer Tasks
        ("Search Ticket", USER_TASK, "Customer"),
        ("Select Route", USER_TASK, "Customer"),
        ("Provide Details", USER_TASK, "Customer"),
        ("Complete Journey", USER_TASK, "Customer"),
        ("Provide Feedback", USER_TASK, "Customer"),
        
        # Gateways
        ("Fork", PARALLEL_GW, "Booking System"),
        ("Join", PARALLEL_GW, "Booking System"),
        ("Feedback?", EXCLUSIVE_GW, "Customer"),
        
        # Booking System Tasks
        ("Generate Ticket", SERVICE_TASK, "Booking System"),
        ("Send Ticket", SERVICE_TASK, "Booking System"),
        ("Send Reminders", SERVICE_TASK, "Booking System"),
        
        # Travel Company Task
        ("Update Inventory", SERVICE_TASK, "Travel Company"),
        
        # End Event
        ("End", END, "Customer"),
    ],
    
    "flows": [
        # Main flow - Search and Selection
        ("Start", "Search Ticket", ""),
        ("Search Ticket", "Select Route", ""),
        ("Select Route", "Provide Details", ""),
        
        # Booking phase
        ("Provide Details", "Generate Ticket", ""),
        ("Generate Ticket", "Fork", ""),
        
        # Parallel split - ticket delivery and inventory update
        ("Fork", "Send Ticket", ""),
        ("Fork", "Update Inventory", ""),
        
        # Parallel merge
        ("Send Ticket", "Join", ""),
        ("Update Inventory", "Join", ""),
        
        # Post-booking flow
        ("Join", "Send Reminders", ""),
        ("Send Reminders", "Complete Journey", ""),
        
        # Exclusive gateway for optional feedback
        ("Complete Journey", "Feedback?", ""),
        ("Feedback?", "Provide Feedback", "Yes"),
        ("Feedback?", "End", "No"),
        ("Provide Feedback", "End", ""),
    ],
    
    "layout": {
        "Start":           0,
        "Search Ticket":   1,
        "Select Route":    2,
        "Provide Details": 3,
        "Generate Ticket": 4,
        "Fork":            5,
        "Send Ticket":     6,
        "Update Inventory": 6,
        "Join":            7,
        "Send Reminders":  8,
        "Complete Journey": 9,
        "Feedback?":       10,
        "Provide Feedback": 11,
        "End":            12,
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
