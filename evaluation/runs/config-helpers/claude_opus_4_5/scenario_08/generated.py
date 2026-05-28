#
# IncidentManagementProcess.py
#
# Description: Incident management process from report to closure
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "IncidentManagementProcess",
    
    "lanes": ["Reporter", "Support Team", "Investigation Team", "Management"],
    
    "elements": [
        # Reporter lane
        ("Start",                    START,        "Reporter"),
        ("Report Incident",          USER_TASK,    "Reporter"),
        
        # Support Team lane
        ("Log in Tracking System",   SERVICE_TASK, "Support Team"),
        ("Assign to Team",           USER_TASK,    "Support Team"),
        ("Notify Stakeholders",      SEND_TASK,    "Support Team"),
        ("Close Incident Report",    USER_TASK,    "Support Team"),
        ("End",                      END,          "Support Team"),
        
        # Investigation Team lane
        ("Gather Information",       USER_TASK,    "Investigation Team"),
        ("Identify Root Cause",      USER_TASK,    "Investigation Team"),
        ("Propose Corrective Actions", USER_TASK,  "Investigation Team"),
        ("Implement Solution",       USER_TASK,    "Investigation Team"),
        
        # Management lane
        ("Review Solution",          USER_TASK,    "Management"),
        ("Solution Effective?",      EXCLUSIVE_GW, "Management"),
        ("Conduct Follow-up",        USER_TASK,    "Management"),
        ("Approve Closure",          USER_TASK,    "Management"),
    ],
    
    "data_objects": [
        ("Incident Report",    "Reporter",           1),
        ("Investigation Notes", "Investigation Team", 4),
        ("Closure Report",     "Management",         9),
    ],
    
    "data_associations": [
        ("Report Incident",          "Incident Report"),
        ("Incident Report",          "Log in Tracking System"),
        ("Identify Root Cause",      "Investigation Notes"),
        ("Investigation Notes",      "Propose Corrective Actions"),
        ("Approve Closure",          "Closure Report"),
        ("Closure Report",           "Notify Stakeholders"),
    ],
    
    "flows": [
        # Initial flow
        ("Start",                      "Report Incident",          ""),
        ("Report Incident",            "Log in Tracking System",   ""),
        ("Log in Tracking System",     "Assign to Team",           ""),
        ("Assign to Team",             "Gather Information",       ""),
        
        # Investigation flow
        ("Gather Information",         "Identify Root Cause",      ""),
        ("Identify Root Cause",        "Propose Corrective Actions", ""),
        ("Propose Corrective Actions", "Implement Solution",       ""),
        ("Implement Solution",         "Review Solution",          ""),
        
        # Review and follow-up
        ("Review Solution",            "Solution Effective?",      ""),
        ("Solution Effective?",        "Conduct Follow-up",        "Yes"),
        ("Solution Effective?",        "Implement Solution",       "No"),
        ("Conduct Follow-up",          "Approve Closure",          ""),
        
        # Closure flow
        ("Approve Closure",            "Notify Stakeholders",      ""),
        ("Notify Stakeholders",        "Close Incident Report",    ""),
        ("Close Incident Report",      "End",                      ""),
    ],
    
    "layout": {
        # Reporter lane
        "Start":                     0,
        "Report Incident":           1,
        
        # Support Team lane
        "Log in Tracking System":    2,
        "Assign to Team":            3,
        "Notify Stakeholders":       10,
        "Close Incident Report":     11,
        "End":                       12,
        
        # Investigation Team lane
        "Gather Information":        4,
        "Identify Root Cause":       5,
        "Propose Corrective Actions": 6,
        "Implement Solution":        7,
        
        # Management lane
        "Review Solution":           8,
        "Solution Effective?":       9,
        "Conduct Follow-up":         10,
        "Approve Closure":           11,
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
