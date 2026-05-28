#
# ComplexProcess_TestCase.py
#
# Description: Complex multi-lane process with data objects and gateway branches
#              Test case for BPMN_Helpers layout and positioning
#
# Applicable on: Package
#
# Version: 1.0 - Complex test case with 4 lanes, 30 elements, 11 data objects
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComplexProcess_TestCase",

    # Lanes from top to bottom
    "lanes": [
        "Manager",
        "Processing System",
        "Quality Control",
        "Operations"
    ],

    # All process elements: (name, type, lane)
    "elements": [
        # === Manager Lane ===
        ("Start",                    START,        "Manager"),
        ("Define Rules",             USER_TASK,    "Manager"),
        ("Review Alert",             USER_TASK,    "Manager"),
        ("Action Required?",         EXCLUSIVE_GW, "Manager"),
        ("Schedule Action",          USER_TASK,    "Manager"),
        ("Adjust Settings",          USER_TASK,    "Manager"),
        ("Review Outcomes",          USER_TASK,    "Manager"),
        ("Continue?",                EXCLUSIVE_GW, "Manager"),
        ("Process Complete",         END,          "Manager"),

        # === Processing System Lane ===
        ("Import Data",              SERVICE_TASK, "Processing System"),
        ("Run Algorithm",            SERVICE_TASK, "Processing System"),
        ("Generate Output",          SERVICE_TASK, "Processing System"),
        ("Log Output",               SERVICE_TASK, "Processing System"),
        ("Retrain Model",            SERVICE_TASK, "Processing System"),
        ("Generate Alert",           SERVICE_TASK, "Processing System"),
        ("Compare Results",          SERVICE_TASK, "Processing System"),
        ("Update Metrics",           SERVICE_TASK, "Processing System"),

        # === Quality Control Lane ===
        ("Validate Output",          SERVICE_TASK, "Quality Control"),
        ("Check Accuracy",           SERVICE_TASK, "Quality Control"),
        ("Output Valid?",            EXCLUSIVE_GW, "Quality Control"),
        ("Generate Error Report",    SERVICE_TASK, "Quality Control"),
        ("Approved",                 SERVICE_TASK, "Quality Control"),

        # === Operations Lane ===
        ("Collect Source Data",      SERVICE_TASK,  "Operations"),
        ("Monitor System",           SERVICE_TASK,  "Operations"),
        ("Detect Issue",             SERVICE_TASK,  "Operations"),
        ("Issue Found?",             EXCLUSIVE_GW,  "Operations"),
        ("Execute Action",           MANUAL_TASK,   "Operations"),
        ("Log Actual Outcome",       SERVICE_TASK,  "Operations"),
        ("No Issue",                 END,           "Operations"),
    ],

    # Data Objects: (name, lane, column)
    # Column should match or be near the source task's column
    "data_objects": [
        ("Config File",            "Manager",            1),   # Near Define Rules
        ("Raw Source Data",        "Operations",         2),   # Near Collect Source Data
        ("Input Telemetry",        "Processing System",  3),   # Near Import Data
        ("Output Prediction",      "Processing System",  5),   # Near Generate Output
        ("Output History",         "Processing System",  6),   # Near Log Output
        ("Validation Result",      "Quality Control",    8),   # Near Check Accuracy
        ("Error Report",           "Quality Control",   10),   # Near Generate Error Report
        ("System Alert",           "Processing System", 11),   # Near Generate Alert
        ("Actual System Data",     "Operations",        14),   # Near Monitor System
        ("Comparison Report",      "Processing System", 17),   # Near Compare Results
        ("KPI Metrics",            "Processing System", 18),   # Near Update Metrics
    ],

    # Data Associations
    "data_associations": [
        ("Define Rules",           "Config File"),
        ("Config File",            "Import Data"),
        ("Collect Source Data",    "Raw Source Data"),
        ("Raw Source Data",        "Import Data"),
        ("Import Data",            "Input Telemetry"),
        ("Input Telemetry",        "Run Algorithm"),
        ("Generate Output",        "Output Prediction"),
        ("Output Prediction",      "Validate Output"),
        ("Log Output",             "Output History"),
        ("Output History",         "Compare Results"),
        ("Check Accuracy",         "Validation Result"),
        ("Validation Result",      "Approved"),
        ("Generate Error Report",  "Error Report"),
        ("Error Report",           "Retrain Model"),
        ("Generate Alert",         "System Alert"),
        ("System Alert",           "Review Alert"),
        ("Monitor System",         "Actual System Data"),
        ("Actual System Data",     "Compare Results"),
        ("Compare Results",        "Comparison Report"),
        ("Comparison Report",      "Review Outcomes"),
        ("Update Metrics",         "KPI Metrics"),
    ],

    # Sequence Flows
    "flows": [
        ("Start",                  "Define Rules",           ""),
        ("Define Rules",           "Collect Source Data",    ""),
        ("Collect Source Data",    "Import Data",            ""),
        ("Import Data",            "Run Algorithm",          ""),
        ("Run Algorithm",          "Generate Output",        ""),
        ("Generate Output",        "Log Output",             ""),
        ("Log Output",             "Validate Output",        ""),
        ("Validate Output",        "Check Accuracy",         ""),
        ("Check Accuracy",         "Output Valid?",          ""),
        ("Output Valid?",          "Generate Error Report",  "Invalid"),
        ("Output Valid?",          "Approved",               "Valid"),
        ("Generate Error Report",  "Retrain Model",          ""),
        ("Retrain Model",          "Run Algorithm",          "Retry"),
        ("Approved",               "Generate Alert",         ""),
        ("Generate Alert",         "Review Alert",           ""),
        ("Review Alert",           "Action Required?",       ""),
        ("Action Required?",       "Adjust Settings",        "False Positive"),
        ("Action Required?",       "Schedule Action",        "Confirmed"),
        ("Adjust Settings",        "Define Rules",           "Update"),
        ("Schedule Action",        "Monitor System",         ""),
        ("Monitor System",         "Detect Issue",           ""),
        ("Detect Issue",           "Issue Found?",           ""),
        ("Issue Found?",           "Execute Action",         "Yes"),
        ("Issue Found?",           "No Issue",               "No"),
        ("Execute Action",         "Log Actual Outcome",     ""),
        ("Log Actual Outcome",     "Compare Results",        ""),
        ("Compare Results",        "Update Metrics",         ""),
        ("Update Metrics",         "Review Outcomes",        ""),
        ("Review Outcomes",        "Continue?",              ""),
        ("Continue?",              "Collect Source Data",    "Continue"),
        ("Continue?",              "Process Complete",       "Stop"),
    ],

    # Layout - column positions only (auto-stacking handles same-lane/same-column conflicts)
    "layout": {
        # === Manager Lane ===
        "Start":                   0,
        "Define Rules":            1,
        "Review Alert":           12,
        "Action Required?":       13,
        "Schedule Action":        14,           # Auto-stacked with Adjust Settings
        "Adjust Settings":        14,           # Auto-stacked (90px below)
        "Review Outcomes":        20,
        "Continue?":              21,
        "Process Complete":       22,

        # === Processing System Lane ===
        "Import Data":             3,
        "Run Algorithm":           4,           # Auto-stacked with Retrain Model
        "Generate Output":         5,
        "Log Output":              6,
        "Retrain Model":           4,           # Auto-stacked (90px below Run Algorithm)
        "Generate Alert":         11,
        "Compare Results":        17,
        "Update Metrics":         18,

        # === Quality Control Lane ===
        "Validate Output":         7,
        "Check Accuracy":          8,
        "Output Valid?":           9,
        "Approved":               10,           # Auto-stacked with Generate Error Report
        "Generate Error Report":  10,           # Auto-stacked (90px below)

        # === Operations Lane ===
        "Collect Source Data":     2,
        "Monitor System":         14,
        "Detect Issue":           15,
        "Issue Found?":           16,
        "Execute Action":         17,           # Auto-stacked with No Issue
        "No Issue":               17,           # Auto-stacked (90px below)
        "Log Actual Outcome":     18,
    },

    # Layout configuration
    "TASK_WIDTH": 130,
    "SPACING": 160,               # TASK_WIDTH + 30
    "START_X": 50,
    "TASK_HEIGHT": 55,
    "DATA_OFFSET_Y": 10,          # Gap below task bottom
}

# ============================================================================
# Entry Point
# ============================================================================
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
