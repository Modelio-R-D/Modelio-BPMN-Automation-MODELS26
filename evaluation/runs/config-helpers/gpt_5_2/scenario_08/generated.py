#
# IncidentReportingAndResolution.py
#
# Description: Incident is reported, logged and assigned, investigated, corrected, followed up, closed, and stakeholders notified.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "IncidentReportingAndResolution",

    "lanes": [
        "Reporter",
        "Tracking System",
        "Investigation Team",
        "Process Owner",
    ],

    "elements": [
        ("Incident Reported",          MESSAGE_START,      "Reporter"),
        ("Report Incident",            USER_TASK,          "Reporter"),

        ("Log Report",                 SERVICE_TASK,       "Tracking System"),
        ("Assign Investigation Team",   SERVICE_TASK,       "Tracking System"),

        ("Investigate Incident",        USER_TASK,          "Investigation Team"),
        ("Gather Information",          USER_TASK,          "Investigation Team"),
        ("Identify Root Cause",         USER_TASK,          "Investigation Team"),
        ("Propose Corrective Actions",  USER_TASK,          "Investigation Team"),

        ("Implement Solution",          SERVICE_TASK,       "Process Owner"),
        ("Follow Up",                  USER_TASK,          "Process Owner"),

        ("Close Incident Report",       SERVICE_TASK,       "Tracking System"),
        ("Notify Stakeholders",         SEND_TASK,          "Tracking System"),

        ("Incident Closed",             END,                "Tracking System"),
    ],

    "data_objects": [
        ("Incident Report",        "Reporter",            1),
        ("Investigation Notes",    "Investigation Team",  5),
        ("Corrective Action Plan", "Investigation Team",  7),
        ("Closure Record",         "Tracking System",     11),
    ],

    "data_associations": [
        ("Report Incident",           "Incident Report"),
        ("Incident Report",           "Log Report"),

        ("Gather Information",        "Investigation Notes"),
        ("Investigation Notes",       "Identify Root Cause"),

        ("Propose Corrective Actions","Corrective Action Plan"),
        ("Corrective Action Plan",    "Implement Solution"),

        ("Close Incident Report",     "Closure Record"),
        ("Closure Record",            "Notify Stakeholders"),
    ],

    "flows": [
        ("Incident Reported",         "Report Incident",           ""),
        ("Report Incident",           "Log Report",                ""),
        ("Log Report",                "Assign Investigation Team",  ""),
        ("Assign Investigation Team",  "Investigate Incident",      ""),

        ("Investigate Incident",      "Gather Information",         ""),
        ("Gather Information",        "Identify Root Cause",        ""),
        ("Identify Root Cause",       "Propose Corrective Actions", ""),

        ("Propose Corrective Actions","Implement Solution",         ""),
        ("Implement Solution",        "Follow Up",                  ""),
        ("Follow Up",                 "Close Incident Report",      ""),
        ("Close Incident Report",     "Notify Stakeholders",        ""),
        ("Notify Stakeholders",       "Incident Closed",            ""),
    ],

    "layout": {
        "Incident Reported":          0,
        "Report Incident":            1,

        "Log Report":                 2,
        "Assign Investigation Team":  3,

        "Investigate Incident":       4,
        "Gather Information":         5,
        "Identify Root Cause":        6,
        "Propose Corrective Actions": 7,

        "Implement Solution":         8,
        "Follow Up":                  9,

        "Close Incident Report":      10,
        "Notify Stakeholders":        11,
        "Incident Closed":            12,
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
