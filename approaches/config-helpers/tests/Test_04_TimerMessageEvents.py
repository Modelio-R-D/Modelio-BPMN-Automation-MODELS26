#
# Test_04_TimerMessageEvents.py
#
# Description:
#   Test Case 4: Process with timer start and message end events
#   Tests: TIMER_START, MESSAGE_START, MESSAGE_END, SERVICE_TASK
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Test04_TimerMessageEvents",
    
    "lanes": ["Scheduler", "Notifier"],
    
    "elements": [
        # Timer-triggered process
        ("Daily Timer",      TIMER_START,  "Scheduler"),
        ("Generate Report",  SERVICE_TASK, "Scheduler"),
        ("Check Results",    USER_TASK,    "Scheduler"),
        
        # Notification lane
        ("Send Email",       SERVICE_TASK, "Notifier"),
        ("Email Sent",       MESSAGE_END,  "Notifier"),
    ],
    
    "flows": [
        ("Daily Timer",     "Generate Report", ""),
        ("Generate Report", "Check Results",   ""),
        ("Check Results",   "Send Email",      ""),
        ("Send Email",      "Email Sent",      ""),
    ],
    
    "layout": {
        "Daily Timer":      0,
        "Generate Report":  1,
        "Check Results":    2,
        "Send Email":       3,
        "Email Sent":       4,
    },
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Select a Package."
else:
    print "ERROR: Select a Package first."
