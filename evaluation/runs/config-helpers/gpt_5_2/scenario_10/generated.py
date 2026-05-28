#
# IT_Solution_Request_Process.py
#
# Description: Request for an IT solution from submission through assessment, approval, procurement, install, test, rollout, training, and support.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "IT_Solution_Request_Process",

    "lanes": ["Requestor", "IT"],

    "elements": [
        ("Start", START, "Requestor"),
        ("Submit IT solution request", USER_TASK, "Requestor"),

        ("Assess request (compatibility, cost, resources)", USER_TASK, "IT"),
        ("Approve request?", EXCLUSIVE_GW, "IT"),

        ("Procure tools or licenses", USER_TASK, "IT"),
        ("Notify requestor of rejection", SEND_TASK, "IT"),
        ("Review rejection", USER_TASK, "Requestor"),
        ("End (Rejected)", END, "Requestor"),

        ("Install solution", SERVICE_TASK, "IT"),
        ("Test in controlled environment", SERVICE_TASK, "IT"),
        ("Test successful?", EXCLUSIVE_GW, "IT"),
        ("Resolve issues and adjust", SERVICE_TASK, "IT"),

        ("Roll out solution to department", SERVICE_TASK, "IT"),
        ("Provide training (if needed)", USER_TASK, "IT"),
        ("Provide support / troubleshooting", SERVICE_TASK, "IT"),
        ("End (Completed)", END, "IT"),
    ],

    "flows": [
        ("Start", "Submit IT solution request", ""),
        ("Submit IT solution request", "Assess request (compatibility, cost, resources)", ""),
        ("Assess request (compatibility, cost, resources)", "Approve request?", ""),

        ("Approve request?", "Procure tools or licenses", "Approved"),
        ("Approve request?", "Notify requestor of rejection", "Rejected"),
        ("Notify requestor of rejection", "Review rejection", ""),
        ("Review rejection", "End (Rejected)", ""),

        ("Procure tools or licenses", "Install solution", ""),
        ("Install solution", "Test in controlled environment", ""),
        ("Test in controlled environment", "Test successful?", ""),

        ("Test successful?", "Roll out solution to department", "Yes"),
        ("Test successful?", "Resolve issues and adjust", "No"),
        ("Resolve issues and adjust", "Test in controlled environment", ""),

        ("Roll out solution to department", "Provide training (if needed)", ""),
        ("Provide training (if needed)", "Provide support / troubleshooting", ""),
        ("Provide support / troubleshooting", "End (Completed)", ""),
    ],

    "layout": {
        "Start": 0,
        "Submit IT solution request": 1,

        "Assess request (compatibility, cost, resources)": 2,
        "Approve request?": 3,

        # Same lane + same column from the gateway: auto-stacked
        "Procure tools or licenses": 4,
        "Notify requestor of rejection": 4,

        "Install solution": 5,
        "Test in controlled environment": 6,
        "Test successful?": 7,

        # Same lane + same column from the gateway: auto-stacked
        "Roll out solution to department": 8,
        "Resolve issues and adjust": 8,

        "Provide training (if needed)": 9,
        "Provide support / troubleshooting": 10,
        "End (Completed)": 11,

        "Review rejection": 5,
        "End (Rejected)": 6,
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
