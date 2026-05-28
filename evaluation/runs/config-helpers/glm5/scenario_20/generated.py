#
# RoomService.py
#
# Description: Room service process at The Evanstonian hotel
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RoomService",
    
    "lanes": ["Guest", "Manager", "Kitchen", "Sommelier", "Waiter"],
    
    "elements": [
        # Start - Guest initiates the process
        ("Guest Calls", MESSAGE_START, "Guest"),
        
        # Manager receives and processes order
        ("Take Order", USER_TASK, "Manager"),
        
        # Inclusive Gateway - forks to parallel paths (alcohol is optional)
        ("Distribute Order", INCLUSIVE_GW, "Manager"),
        
        # Parallel work in different lanes
        ("Prepare Food", USER_TASK, "Kitchen"),
        ("Prepare Alcohol", USER_TASK, "Sommelier"),
        ("Ready Cart and Drinks", USER_TASK, "Waiter"),
        
        # Synchronization - inclusive join waits for all triggered paths
        ("All Ready", INCLUSIVE_GW, "Waiter"),
        
        # Delivery and billing
        ("Deliver to Room", USER_TASK, "Waiter"),
        ("Debit Account", USER_TASK, "Waiter"),
        
        # End
        ("End", END, "Waiter"),
    ],
    
    "flows": [
        ("Guest Calls", "Take Order", ""),
        ("Take Order", "Distribute Order", ""),
        ("Distribute Order", "Prepare Food", ""),
        ("Distribute Order", "Prepare Alcohol", "Alcohol (80%)"),
        ("Distribute Order", "Ready Cart and Drinks", ""),
        ("Prepare Food", "All Ready", ""),
        ("Prepare Alcohol", "All Ready", ""),
        ("Ready Cart and Drinks", "All Ready", ""),
        ("All Ready", "Deliver to Room", ""),
        ("Deliver to Room", "Debit Account", ""),
        ("Debit Account", "End", ""),
    ],
    
    "data_objects": [
        ("Order Ticket", "Manager", 1),
    ],
    
    "data_associations": [
        ("Take Order", "Order Ticket"),
        ("Order Ticket", "Prepare Food"),
        ("Order Ticket", "Prepare Alcohol"),
        ("Order Ticket", "Ready Cart and Drinks"),
    ],
    
    "layout": {
        "Guest Calls": 0,
        "Take Order": 1,
        "Distribute Order": 2,
        "Prepare Food": 3,
        "Prepare Alcohol": 3,
        "Ready Cart and Drinks": 3,
        "All Ready": 4,
        "Deliver to Room": 5,
        "Debit Account": 6,
        "End": 7,
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
