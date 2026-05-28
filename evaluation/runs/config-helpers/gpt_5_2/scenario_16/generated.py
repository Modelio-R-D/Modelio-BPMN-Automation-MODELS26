#
# AnnualAuditProcess.py
#
# Description: Multinational company annual audit process with parallel preparation/compliance checks,
#              discrepancy clarification loop, parallel risk assessments, optional investigation, and approval loop.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "AnnualAuditProcess",

    "lanes": [
        "Audit Coordinator",
        "Regional Office",
        "Compliance Team",
        "Central Audit Team",
        "Audit Director",
        "Executive Board"
    ],

    "elements": [
        ("Start",                           START,          "Audit Coordinator"),
        ("Send Audit Notification",         SEND_TASK,      "Audit Coordinator"),

        ("Parallel Split",                  PARALLEL_GW,    "Audit Coordinator"),

        ("Prepare Financial Statements",    USER_TASK,      "Regional Office"),
        ("Gather Supporting Documents",     USER_TASK,      "Regional Office"),
        ("Check Regulatory Updates",        USER_TASK,      "Compliance Team"),

        ("Parallel Join",                   PARALLEL_GW,    "Regional Office"),
        ("Submit Documents",                SEND_TASK,      "Regional Office"),

        ("Review Submission",               USER_TASK,      "Central Audit Team"),
        ("Discrepancies Found?",            EXCLUSIVE_GW,   "Central Audit Team"),

        ("Request Clarifications",          SEND_TASK,      "Central Audit Team"),
        ("Provide Clarifications",          USER_TASK,      "Regional Office"),
        ("Resubmit Clarifications",         SEND_TASK,      "Regional Office"),

        ("Conduct Risk Assessment",         USER_TASK,      "Central Audit Team"),
        ("Risk Split",                      PARALLEL_GW,    "Central Audit Team"),
        ("Evaluate Financial Risks",        USER_TASK,      "Central Audit Team"),
        ("Evaluate Operational Risks",      USER_TASK,      "Central Audit Team"),
        ("Evaluate Compliance Risks",       USER_TASK,      "Central Audit Team"),
        ("Risk Join",                       PARALLEL_GW,    "Central Audit Team"),

        ("High Risk?",                      EXCLUSIVE_GW,   "Central Audit Team"),
        ("Launch Detailed Investigation",   USER_TASK,      "Central Audit Team"),

        ("Investigation Split",             PARALLEL_GW,    "Central Audit Team"),
        ("Data Analysis",                   SERVICE_TASK,   "Central Audit Team"),
        ("Conduct Interviews",              USER_TASK,      "Central Audit Team"),
        ("Investigation Join",              PARALLEL_GW,    "Central Audit Team"),

        ("Need Site Visit?",                EXCLUSIVE_GW,   "Central Audit Team"),
        ("Conduct Site Visit",              MANUAL_TASK,    "Central Audit Team"),

        ("Compile Audit Report",            USER_TASK,      "Central Audit Team"),
        ("Review Report",                   USER_TASK,      "Audit Director"),
        ("Approve Report?",                 EXCLUSIVE_GW,   "Audit Director"),

        ("Request Revisions",               SEND_TASK,      "Audit Director"),
        ("Update Report",                   USER_TASK,      "Central Audit Team"),
        ("Resubmit Updated Report",         SEND_TASK,      "Central Audit Team"),

        ("Distribution Split",              PARALLEL_GW,    "Audit Director"),
        ("Send Final Report",               SEND_TASK,      "Audit Director"),
        ("Receive Final Report",            RECEIVE_TASK,   "Executive Board"),
        ("Archive Report",                  SERVICE_TASK,   "Central Audit Team"),
        ("Distribution Join",               PARALLEL_GW,    "Audit Director"),

        ("Close Audit Process",             TASK,           "Audit Coordinator"),
        ("End",                             END,            "Audit Coordinator"),
    ],

    "flows": [
        ("Start", "Send Audit Notification", ""),
        ("Send Audit Notification", "Parallel Split", ""),

        ("Parallel Split", "Prepare Financial Statements", ""),
        ("Parallel Split", "Check Regulatory Updates", ""),

        ("Prepare Financial Statements", "Gather Supporting Documents", ""),
        ("Gather Supporting Documents", "Parallel Join", ""),
        ("Check Regulatory Updates", "Parallel Join", ""),

        ("Parallel Join", "Submit Documents", ""),
        ("Submit Documents", "Review Submission", ""),
        ("Review Submission", "Discrepancies Found?", ""),

        ("Discrepancies Found?", "Request Clarifications", "Yes"),
        ("Request Clarifications", "Provide Clarifications", ""),
        ("Provide Clarifications", "Resubmit Clarifications", ""),
        ("Resubmit Clarifications", "Review Submission", ""),

        ("Discrepancies Found?", "Conduct Risk Assessment", "No"),
        ("Conduct Risk Assessment", "Risk Split", ""),

        ("Risk Split", "Evaluate Financial Risks", ""),
        ("Risk Split", "Evaluate Operational Risks", ""),
        ("Risk Split", "Evaluate Compliance Risks", ""),
        ("Evaluate Financial Risks", "Risk Join", ""),
        ("Evaluate Operational Risks", "Risk Join", ""),
        ("Evaluate Compliance Risks", "Risk Join", ""),

        ("Risk Join", "High Risk?", ""),

        ("High Risk?", "Launch Detailed Investigation", "Yes"),
        ("Launch Detailed Investigation", "Investigation Split", ""),
        ("Investigation Split", "Data Analysis", ""),
        ("Investigation Split", "Conduct Interviews", ""),
        ("Data Analysis", "Investigation Join", ""),
        ("Conduct Interviews", "Investigation Join", ""),

        ("Investigation Join", "Need Site Visit?", ""),
        ("Need Site Visit?", "Conduct Site Visit", "Yes"),
        ("Need Site Visit?", "Compile Audit Report", "No"),
        ("Conduct Site Visit", "Compile Audit Report", ""),

        ("High Risk?", "Compile Audit Report", "No"),

        ("Compile Audit Report", "Review Report", ""),
        ("Review Report", "Approve Report?", ""),

        ("Approve Report?", "Request Revisions", "Revisions"),
        ("Request Revisions", "Update Report", ""),
        ("Update Report", "Resubmit Updated Report", ""),
        ("Resubmit Updated Report", "Review Report", ""),

        ("Approve Report?", "Distribution Split", "Approved"),
        ("Distribution Split", "Send Final Report", ""),
        ("Send Final Report", "Receive Final Report", ""),
        ("Distribution Split", "Archive Report", ""),
        ("Receive Final Report", "Distribution Join", ""),
        ("Archive Report", "Distribution Join", ""),

        ("Distribution Join", "Close Audit Process", ""),
        ("Close Audit Process", "End", ""),
    ],

    "layout": {
        "Start": 0,
        "Send Audit Notification": 1,

        "Parallel Split": 2,

        "Prepare Financial Statements": 3,
        "Check Regulatory Updates": 3,
        "Gather Supporting Documents": 4,

        "Parallel Join": 5,
        "Submit Documents": 6,

        "Review Submission": 7,
        "Discrepancies Found?": 8,

        "Request Clarifications": 9,
        "Conduct Risk Assessment": 9,

        "Provide Clarifications": 10,
        "Resubmit Clarifications": 11,

        "Risk Split": 10,
        "Evaluate Financial Risks": 11,
        "Evaluate Operational Risks": 11,
        "Evaluate Compliance Risks": 11,
        "Risk Join": 12,

        "High Risk?": 13,
        "Launch Detailed Investigation": 14,

        "Investigation Split": 15,
        "Data Analysis": 16,
        "Conduct Interviews": 16,
        "Investigation Join": 17,

        "Need Site Visit?": 18,
        "Conduct Site Visit": 19,

        "Compile Audit Report": 20,
        "Review Report": 21,
        "Approve Report?": 22,

        "Request Revisions": 23,
        "Update Report": 24,
        "Resubmit Updated Report": 25,

        "Distribution Split": 26,
        "Send Final Report": 27,
        "Receive Final Report": 28,
        "Archive Report": 27,
        "Distribution Join": 29,

        "Close Audit Process": 30,
        "End": 31,
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
