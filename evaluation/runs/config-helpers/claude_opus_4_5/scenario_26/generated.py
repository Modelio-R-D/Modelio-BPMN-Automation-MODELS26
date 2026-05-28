#
# BecomingAParent.py
#
# Description: Parental leave planning, notification, and extension process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BecomingAParent",
    
    "lanes": [
        "Parent",
        "HR System",
        "External Parties"
    ],
    
    "elements": [
        # Parent Lane - Planning Phase
        ("Start",                    START,        "Parent"),
        ("Request Leave Info",       USER_TASK,    "Parent"),
        ("Review Leave Models",      USER_TASK,    "Parent"),
        ("Select Leave Model",       USER_TASK,    "Parent"),
        ("Provide Personal Info",    USER_TASK,    "Parent"),
        
        # HR System - Processing
        ("Fetch Leave Models",       SERVICE_TASK, "HR System"),
        ("Validate Selection",       SERVICE_TASK, "HR System"),
        ("Prepare Notifications",    SERVICE_TASK, "HR System"),
        ("Send Notifications",       SEND_TASK,    "HR System"),
        ("Collect Responses",        RECEIVE_TASK, "HR System"),
        ("Start Leave Period",       SERVICE_TASK, "HR System"),
        ("Monitor Leave End",        TIMER_CATCH,  "HR System"),
        ("Request Extension Decision", SEND_TASK,  "HR System"),
        
        # External Parties
        ("Notify Social Security",   SERVICE_TASK, "External Parties"),
        ("Notify Employer",          SERVICE_TASK, "External Parties"),
        ("Receive Confirmations",    MESSAGE_CATCH,"External Parties"),
        
        # Parent - Extension Decision
        ("Decide on Extension",      USER_TASK,    "Parent"),
        ("Extend Leave?",            EXCLUSIVE_GW, "Parent"),
        ("Select Extension Period",  USER_TASK,    "Parent"),
        
        # HR System - Extension Processing
        ("Process Extension",        SERVICE_TASK, "HR System"),
        ("Notify Extension",         SEND_TASK,    "HR System"),
        
        # End Events
        ("End Leave",                END,          "HR System"),
    ],
    
    "data_objects": [
        ("Leave Models",          "HR System",   2),
        ("Selected Model",        "Parent",      4),
        ("Personal Details",      "Parent",      5),
        ("Notification Package",  "HR System",   7),
        ("Confirmation Records",  "HR System",   10),
    ],
    
    "data_associations": [
        # Leave models flow
        ("Fetch Leave Models",    "Leave Models"),
        ("Leave Models",          "Review Leave Models"),
        
        # Selection flow
        ("Select Leave Model",    "Selected Model"),
        ("Selected Model",        "Validate Selection"),
        
        # Personal info flow
        ("Provide Personal Info", "Personal Details"),
        ("Personal Details",      "Prepare Notifications"),
        
        # Notification package
        ("Prepare Notifications", "Notification Package"),
        ("Notification Package",  "Send Notifications"),
        
        # Confirmations
        ("Collect Responses",     "Confirmation Records"),
        ("Confirmation Records",  "Start Leave Period"),
    ],
    
    "flows": [
        # Initial request flow
        ("Start",                    "Request Leave Info",       ""),
        ("Request Leave Info",       "Fetch Leave Models",       ""),
        ("Fetch Leave Models",       "Review Leave Models",      ""),
        ("Review Leave Models",      "Select Leave Model",       ""),
        ("Select Leave Model",       "Provide Personal Info",    ""),
        ("Provide Personal Info",    "Validate Selection",       ""),
        
        # Notification preparation
        ("Validate Selection",       "Prepare Notifications",    ""),
        ("Prepare Notifications",    "Send Notifications",       ""),
        
        # External notifications (parallel)
        ("Send Notifications",       "Notify Social Security",   ""),
        ("Send Notifications",       "Notify Employer",          ""),
        ("Notify Social Security",   "Receive Confirmations",    ""),
        ("Notify Employer",          "Receive Confirmations",    ""),
        
        # Collect and start leave
        ("Receive Confirmations",    "Collect Responses",        ""),
        ("Collect Responses",        "Start Leave Period",       ""),
        ("Start Leave Period",       "Monitor Leave End",        ""),
        
        # Extension decision flow
        ("Monitor Leave End",        "Request Extension Decision", ""),
        ("Request Extension Decision", "Decide on Extension",    ""),
        ("Decide on Extension",      "Extend Leave?",            ""),
        
        # Extension paths
        ("Extend Leave?",            "Select Extension Period",  "Yes"),
        ("Extend Leave?",            "End Leave",                "No"),
        
        # Extension processing
        ("Select Extension Period",  "Process Extension",        ""),
        ("Process Extension",        "Notify Extension",         ""),
        ("Notify Extension",         "Monitor Leave End",        ""),  # Loop back
    ],
    
    "layout": {
        # Column 0 - Start
        "Start":                     0,
        
        # Column 1 - Request
        "Request Leave Info":        1,
        
        # Column 2 - Fetch
        "Fetch Leave Models":        2,
        
        # Column 3 - Review
        "Review Leave Models":       3,
        
        # Column 4 - Select
        "Select Leave Model":        4,
        
        # Column 5 - Personal Info
        "Provide Personal Info":     5,
        
        # Column 6 - Validate
        "Validate Selection":        6,
        
        # Column 7 - Prepare
        "Prepare Notifications":     7,
        
        # Column 8 - Send
        "Send Notifications":        8,
        
        # Column 9 - External notifications (auto-stacked)
        "Notify Social Security":    9,
        "Notify Employer":           9,
        
        # Column 10 - Receive confirmations
        "Receive Confirmations":     10,
        
        # Column 11 - Collect
        "Collect Responses":         11,
        
        # Column 12 - Start leave
        "Start Leave Period":        12,
        
        # Column 13 - Monitor
        "Monitor Leave End":         13,
        
        # Column 14 - Extension request
        "Request Extension Decision": 14,
        
        # Column 15 - Decide
        "Decide on Extension":       15,
        
        # Column 16 - Gateway
        "Extend Leave?":             16,
        
        # Column 17 - Extension path (auto-stacked)
        "Select Extension Period":   17,
        "End Leave":                 17,
        
        # Column 18 - Process extension
        "Process Extension":         18,
        
        # Column 19 - Notify extension
        "Notify Extension":          19,
    },
    
    # Wider spacing for readability
    "SPACING": 160,
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
