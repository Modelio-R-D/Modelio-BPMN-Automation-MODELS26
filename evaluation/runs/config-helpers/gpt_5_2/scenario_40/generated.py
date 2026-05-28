#
# OEE.py
#
# Description: Collect machine metrics, calculate OEE, stop machine and notify engineer if OEE is below threshold; continue monitoring after restart; end when disconnected.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OEE",

    "lanes": ["Monitoring System", "Machine", "Engineer"],

    "elements": [
        ("Start",                 TIMER_START,     "Monitoring System"),
        ("Collect Metrics",       SERVICE_TASK,    "Monitoring System"),
        ("Machine Connected?",    EXCLUSIVE_GW,    "Monitoring System"),
        ("Calculate OEE",         SERVICE_TASK,    "Monitoring System"),
        ("OEE Below Threshold?",  EXCLUSIVE_GW,    "Monitoring System"),

        ("Wait Sample Interval",  TIMER_CATCH,     "Monitoring System"),

        ("Stop Machine",          SERVICE_TASK,    "Machine"),
        ("Send Email to Engineer",SEND_TASK,       "Monitoring System"),
        ("Wait for Restart",      MESSAGE_CATCH,   "Monitoring System"),

        ("Process End",           END,             "Monitoring System"),
    ],

    "flows": [
        ("Start",                "Collect Metrics",        ""),
        ("Collect Metrics",      "Machine Connected?",     ""),

        ("Machine Connected?",   "Calculate OEE",          "Yes"),
        ("Machine Connected?",   "Process End",            "No"),

        ("Calculate OEE",        "OEE Below Threshold?",   ""),

        ("OEE Below Threshold?", "Wait Sample Interval",   "No"),
        ("Wait Sample Interval", "Collect Metrics",        ""),

        ("OEE Below Threshold?", "Stop Machine",           "Yes"),
        ("Stop Machine",         "Send Email to Engineer", ""),
        ("Send Email to Engineer","Wait for Restart",      ""),
        ("Wait for Restart",     "Collect Metrics",        ""),
    ],

    "layout": {
        "Start":                  0,
        "Collect Metrics":        1,
        "Machine Connected?":     2,
        "Calculate OEE":          3,
        "OEE Below Threshold?":   4,

        # Branches from the gateway (same column is fine; different lanes)
        "Wait Sample Interval":   5,
        "Stop Machine":           5,

        "Send Email to Engineer": 6,
        "Wait for Restart":       7,

        "Process End":            8,
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
