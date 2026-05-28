#
# CreditScoringProcess.py
#
# Description: Credit scoring process between Bank Clerk, Banking System, and Agency.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CreditScoringProcess",
    
    "lanes": ["Bank Clerk", "Banking System", "Agency"],
    
    "elements": [
        # Column 0-1: Initiation
        ("Start", START, "Bank Clerk"),
        ("Request Scoring", USER_TASK, "Bank Clerk"),
        
        # Column 2: Banking System sends request
        ("Send Scoring Request", SERVICE_TASK, "Banking System"),
        
        # Column 3-4: Agency Level 1 Processing
        ("Level 1 Scoring", SERVICE_TASK, "Agency"),
        ("Immediate Result?", EXCLUSIVE_GW, "Agency"),
        
        # Column 5: Agency outputs (Stacked: Immediate Top, Delay Bottom)
        ("Return Immediate Result", SERVICE_TASK, "Agency"),
        ("Notify Delay", SERVICE_TASK, "Agency"),
        
        # Column 6: Banking System receives (Stacked: Immediate Top, Delay Bottom)
        ("Receive Immediate Result", MESSAGE_CATCH, "Banking System"),
        ("Receive Delay Notice", MESSAGE_CATCH, "Banking System"),
        
        # Column 7: Delayed path processing
        ("Level 2 Scoring", SERVICE_TASK, "Agency"),
        ("Display Delay Message", SERVICE_TASK, "Banking System"),
        
        # Column 8: Delayed path completion
        ("Return Delayed Result", SERVICE_TASK, "Agency"),
        ("Receive Delayed Result", MESSAGE_CATCH, "Banking System"),
        
        # Column 9-10: Finalization
        ("Present Result", SERVICE_TASK, "Banking System"),
        ("View Result", USER_TASK, "Bank Clerk"),
        ("End", END, "Bank Clerk"),
    ],
    
    "flows": [
        # Initiation
        ("Start", "Request Scoring", ""),
        ("Request Scoring", "Send Scoring Request", ""),
        ("Send Scoring Request", "Level 1 Scoring", ""),
        
        # Level 1 Decision
        ("Level 1 Scoring", "Immediate Result?", ""),
        
        # Immediate Path (Yes)
        ("Immediate Result?", "Return Immediate Result", "Yes"),
        ("Return Immediate Result", "Receive Immediate Result", ""),
        ("Receive Immediate Result", "Present Result", ""),
        
        # Delayed Path (No)
        ("Immediate Result?", "Notify Delay", "No"),
        ("Notify Delay", "Receive Delay Notice", ""),
        ("Notify Delay", "Level 2 Scoring", ""),
        
        # Delay handling in Banking System
        ("Receive Delay Notice", "Display Delay Message", ""),
        ("Display Delay Message", "Receive Delayed Result", ""),
        
        # Delayed Result Return
        ("Level 2 Scoring", "Return Delayed Result", ""),
        ("Return Delayed Result", "Receive Delayed Result", ""),
        ("Receive Delayed Result", "Present Result", ""),
        
        # Finalization
        ("Present Result", "View Result", ""),
        ("View Result", "End", ""),
    ],
    
    "layout": {
        # Column 0-1
        "Start": 0,
        "Request Scoring": 1,
        
        # Column 2
        "Send Scoring Request": 2,
        
        # Column 3-4
        "Level 1 Scoring": 3,
        "Immediate Result?": 4,
        
        # Column 5: Auto-stacked Agency outputs
        # "Return Immediate Result" listed first -> Top position
        # "Notify Delay" listed second -> Bottom position
        "Return Immediate Result": 5,
        "Notify Delay": 5,
        
        # Column 6: Auto-stacked Banking System receives
        "Receive Immediate Result": 6,
        "Receive Delay Notice": 6,
        
        # Column 7
        "Level 2 Scoring": 7,
        "Display Delay Message": 7,
        
        # Column 8
        "Return Delayed Result": 8,
        "Receive Delayed Result": 8,
        
        # Column 9-11
        "Present Result": 9,
        "View Result": 10,
        "End": 11,
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
