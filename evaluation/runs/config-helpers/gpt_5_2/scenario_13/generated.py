#
# ComplaintHandlingProcess.py
#
# Description: Complaint handling with investigation, refund decision, reimbursement, resolution, and customer feedback.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComplaintHandlingProcess",

    "lanes": ["Customer", "Customer Service", "Investigation Team", "Finance"],

    "elements": [
        ("Start",                       START,               "Customer"),
        ("File Complaint",              USER_TASK,           "Customer"),

        ("Log Complaint",               USER_TASK,           "Customer Service"),
        ("Assign to Department",        USER_TASK,           "Customer Service"),

        ("Review Complaint",            USER_TASK,           "Investigation Team"),
        ("Refund Approved?",            EXCLUSIVE_GW,        "Investigation Team"),
        ("Notify Customer - Approved",  USER_TASK,           "Investigation Team"),
        ("Notify Customer - Rejected",  USER_TASK,           "Investigation Team"),

        ("Process Reimbursement",       SERVICE_TASK,        "Finance"),
        ("Refund Received",             INTERMEDIATE_CATCH,  "Customer"),

        ("Mark Complaint Resolved",     SERVICE_TASK,        "Customer Service"),
        ("Provide Feedback",            USER_TASK,           "Customer"),
        ("End",                         END,                 "Customer"),
    ],

    "flows": [
        ("Start",                      "File Complaint",             ""),
        ("File Complaint",             "Log Complaint",              ""),
        ("Log Complaint",              "Assign to Department",       ""),
        ("Assign to Department",       "Review Complaint",           ""),
        ("Review Complaint",           "Refund Approved?",           ""),

        ("Refund Approved?",           "Notify Customer - Approved", "Yes"),
        ("Refund Approved?",           "Notify Customer - Rejected", "No"),

        ("Notify Customer - Approved", "Process Reimbursement",      ""),
        ("Process Reimbursement",      "Refund Received",            ""),
        ("Refund Received",            "Mark Complaint Resolved",    ""),

        ("Notify Customer - Rejected", "Mark Complaint Resolved",    ""),

        ("Mark Complaint Resolved",    "Provide Feedback",           ""),
        ("Provide Feedback",           "End",                        ""),
    ],

    "layout": {
        "Start":                      0,
        "File Complaint":             1,

        "Log Complaint":              2,
        "Assign to Department":       3,

        "Review Complaint":           4,
        "Refund Approved?":           5,
        "Notify Customer - Approved": 6,
        "Notify Customer - Rejected": 6,   # auto-stacked

        "Process Reimbursement":      7,
        "Refund Received":            8,

        "Mark Complaint Resolved":    9,
        "Provide Feedback":           10,
        "End":                        11,
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
