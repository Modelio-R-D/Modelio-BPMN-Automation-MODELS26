#
# OEE_Monitoring.py
#
# Description: OEE calculation process with machine monitoring, alerts, and engineer notification
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OEE_Monitoring",
    
    "lanes": ["Machine", "OEE System", "Engineer"],
    
    "elements": [
        # Machine Lane
        ("Machine Connected",       SIGNAL_START,     "Machine"),
        ("Collect Performance",     SERVICE_TASK,     "Machine"),
        ("Collect Availability",    SERVICE_TASK,     "Machine"),
        ("Collect Quality",         SERVICE_TASK,     "Machine"),
        ("Machine Disconnected",    SIGNAL_CATCH,     "Machine"),
        ("Machine Restarted",       SIGNAL_CATCH,     "Machine"),
        ("Stop Machine",            SERVICE_TASK,     "Machine"),
        ("Process Ended",           TERMINATE_END,    "Machine"),
        
        # OEE System Lane
        ("Calculate OEE",           SERVICE_TASK,     "OEE System"),
        ("OEE Threshold?",          EXCLUSIVE_GW,     "OEE System"),
        ("Log OEE Value",           SERVICE_TASK,     "OEE System"),
        ("Wait Interval",           TIMER_CATCH,      "OEE System"),
        ("Generate Alert",          SERVICE_TASK,     "OEE System"),
        ("Send Email",              SEND_TASK,        "OEE System"),
        
        # Engineer Lane
        ("Receive Alert",           MESSAGE_CATCH,    "Engineer"),
        ("Investigate Issue",       USER_TASK,        "Engineer"),
        ("Restart Machine",         MANUAL_TASK,      "Engineer"),
    ],
    
    "data_objects": [
        ("OEE Data",        "OEE System", 4),
        ("Alert Report",    "OEE System", 6),
    ],
    
    "data_associations": [
        ("Calculate OEE",   "OEE Data"),
        ("OEE Data",        "Log OEE Value"),
        ("Generate Alert",  "Alert Report"),
        ("Alert Report",    "Send Email"),
    ],
    
    "flows": [
        # Start and data collection
        ("Machine Connected",       "Collect Performance",    ""),
        ("Collect Performance",     "Collect Availability",   ""),
        ("Collect Availability",    "Collect Quality",        ""),
        ("Collect Quality",         "Calculate OEE",          ""),
        
        # OEE evaluation
        ("Calculate OEE",           "OEE Threshold?",         ""),
        ("OEE Threshold?",          "Log OEE Value",          "OEE >= Threshold"),
        ("OEE Threshold?",          "Generate Alert",         "OEE < Threshold"),
        
        # Normal path - continue monitoring
        ("Log OEE Value",           "Wait Interval",          ""),
        ("Wait Interval",           "Collect Performance",    ""),
        
        # Alert path
        ("Generate Alert",          "Stop Machine",           ""),
        ("Stop Machine",            "Send Email",             ""),
        ("Send Email",              "Receive Alert",          ""),
        ("Receive Alert",           "Investigate Issue",      ""),
        ("Investigate Issue",       "Restart Machine",        ""),
        ("Restart Machine",         "Machine Restarted",      ""),
        ("Machine Restarted",       "Collect Performance",    ""),
        
        # Disconnection path
        ("Machine Disconnected",    "Process Ended",          ""),
    ],
    
    "layout": {
        # Machine Lane
        "Machine Connected":        0,
        "Collect Performance":      1,
        "Collect Availability":     2,
        "Collect Quality":          3,
        "Machine Disconnected":     (1, 90),
        "Stop Machine":             6,
        "Machine Restarted":        10,
        "Process Ended":            (2, 90),
        
        # OEE System Lane
        "Calculate OEE":            4,
        "OEE Threshold?":           5,
        "Log OEE Value":            6,
        "Generate Alert":           (6, 90),
        "Wait Interval":            7,
        "Send Email":               7,
        
        # Engineer Lane
        "Receive Alert":            8,
        "Investigate Issue":        9,
        "Restart Machine":          10,
    },
    
    "SPACING": 130,
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
