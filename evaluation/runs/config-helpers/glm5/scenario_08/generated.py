#
# IncidentManagement.py
#
# Description: Incident reporting and resolution process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "IncidentManagement",
    
    "lanes": ["Reporter", "Support Team", "Investigation Team"],
    
    "elements": [
        # Start - Reporter initiates
        ("Incident Reported", START, "Reporter"),
        
        # Support Team handles logging and assignment
        ("Log Incident", USER_TASK, "Support Team"),
        ("Assign to Team", SERVICE_TASK, "Support Team"),
        
        # Investigation Team handles root cause analysis
        ("Gather Information", USER_TASK, "Investigation Team"),
        ("Identify Cause", USER_TASK, "Investigation Team"),
        ("Propose Corrective Actions", USER_TASK, "Investigation Team"),
        ("Implement Solution", USER_TASK, "Investigation Team"),
        
        # Support Team handles follow-up and closure
        ("Follow-up", USER_TASK, "Support Team"),
        ("Resolved?", EXCLUSIVE_GW, "Support Team"),
        ("Close Report", SERVICE_TASK, "Support Team"),
        ("Notify Stakeholders", SERVICE_TASK, "Support Team"),
        
        # End
        ("Incident Closed", END, "Support Team"),
    ],
    
    "flows": [
        ("Incident Reported", "Log Incident", ""),
        ("Log Incident", "Assign to Team", ""),
        ("Assign to Team", "Gather Information", ""),
        ("Gather Information", "Identify Cause", ""),
        ("Identify Cause", "Propose Corrective Actions", ""),
        ("Propose Corrective Actions", "Implement Solution", ""),
        ("Implement Solution", "Follow-up", ""),
        ("Follow-up", "Resolved?", ""),
        ("Resolved?", "Close Report", "Yes"),
        ("Resolved?", "Gather Information", "No"),
        ("Close Report", "Notify Stakeholders", ""),
        ("Notify Stakeholders", "Incident Closed", ""),
    ],
    
    "layout": {
        "Incident Reported": 0,
        "Log Incident": 1,
        "Assign to Team": 2,
        "Gather Information": 3,
        "Identify Cause": 4,
        "Propose Corrective Actions": 5,
        "Implement Solution": 6,
        "Follow-up": 7,
        "Resolved?": 8,
        "Close Report": 9,
        "Notify Stakeholders": 10,
        "Incident Closed": 11,
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
