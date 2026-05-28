#
# ComplianceAuditCertification.py
#
# Description: Compliance audit and certification process (preparation, external audit, corrections, final audit, certification, documents).
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComplianceAuditCertification",

    "lanes": ["Company", "External Auditors", "Certification Body"],

    "elements": [
        ("Audit scheduled",          START,        "Company"),

        ("Prepare documentation",    USER_TASK,    "Company"),
        ("Gather evidence",          USER_TASK,    "Company"),
        ("Conduct self-assessment",  USER_TASK,    "Company"),

        ("Review company processes", USER_TASK,    "External Auditors"),
        ("Identify gaps or issues",  USER_TASK,    "External Auditors"),
        ("Gaps found?",              EXCLUSIVE_GW, "External Auditors"),

        ("Make corrections",         USER_TASK,    "Company"),

        ("Final audit",              USER_TASK,    "External Auditors"),
        ("Criteria met?",            EXCLUSIVE_GW, "External Auditors"),

        ("Award certification",      USER_TASK,    "Certification Body"),
        ("Issue official documents", USER_TASK,    "Certification Body"),
        ("Process complete",         END,          "Certification Body"),
    ],

    "flows": [
        ("Audit scheduled",         "Prepare documentation",    ""),
        ("Prepare documentation",   "Gather evidence",          ""),
        ("Gather evidence",         "Conduct self-assessment",  ""),
        ("Conduct self-assessment", "Review company processes", ""),

        ("Review company processes","Identify gaps or issues",  ""),
        ("Identify gaps or issues", "Gaps found?",              ""),

        ("Gaps found?",             "Make corrections",         "Yes"),
        ("Gaps found?",             "Final audit",              "No"),

        ("Make corrections",        "Final audit",              ""),

        ("Final audit",             "Criteria met?",            ""),

        ("Criteria met?",           "Award certification",      "Yes"),
        ("Criteria met?",           "Make corrections",         "No"),

        ("Award certification",     "Issue official documents", ""),
        ("Issue official documents","Process complete",         ""),
    ],

    "layout": {
        "Audit scheduled":          0,

        "Prepare documentation":    1,
        "Gather evidence":          2,
        "Conduct self-assessment":  3,

        "Review company processes": 4,
        "Identify gaps or issues":  5,
        "Gaps found?":              6,

        "Make corrections":         7,

        "Final audit":              8,
        "Criteria met?":            9,

        "Award certification":      10,
        "Issue official documents": 11,
        "Process complete":         12,
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
