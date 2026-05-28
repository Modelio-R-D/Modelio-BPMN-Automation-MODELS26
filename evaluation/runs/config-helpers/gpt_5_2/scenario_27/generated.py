#
# WorkAccident.py
#
# Description: Process for capturing work accidents, near misses, risks, and defects; determines coverage and reporting obligations.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Work Accident",

    "lanes": [
        "Reporter",
        "Organization",
        "Accident Insurer",
        "Inspectorate or Private Insurer",
    ],

    "elements": [
        ("Start",                                            START,        "Reporter"),
        ("Secure scene and provide first aid",               MANUAL_TASK,  "Reporter"),
        ("Get medical assessment (if needed)",               USER_TASK,    "Reporter"),
        ("Notify employer or responsible body immediately",  USER_TASK,    "Reporter"),
        ("Collect incident information (who/where/when/what)", USER_TASK,  "Reporter"),

        ("Incident type?",                                   EXCLUSIVE_GW, "Organization"),
        ("Log near miss / dangerous occurrence",             USER_TASK,    "Organization"),
        ("Log serious and immediate risk",                   USER_TASK,    "Organization"),
        ("Log defect in protection systems",                 USER_TASK,    "Organization"),
        ("Implement corrective actions",                     USER_TASK,    "Organization"),
        ("End - Corrective actions completed",               END,          "Organization"),

        ("Assess work-accident coverage circumstances",      USER_TASK,    "Organization"),
        ("Covered as work accident/equivalent?",             EXCLUSIVE_GW, "Organization"),
        ("Record as non-covered incident",                   USER_TASK,    "Organization"),
        ("End - Not covered",                                END,          "Organization"),

        ("Fatality or serious injury?",                      EXCLUSIVE_GW, "Organization"),
        ("Report immediately to Labour Inspectorate",        SEND_TASK,    "Organization"),
        ("Labour Inspectorate receives report",              RECEIVE_TASK, "Inspectorate or Private Insurer"),

        ("Person group?",                                    EXCLUSIVE_GW, "Organization"),

        ("Employer drafts accident report",                  USER_TASK,    "Organization"),
        ("Employer submits report to accident insurance provider", SEND_TASK, "Organization"),

        ("School/university drafts report (3 copies)",       USER_TASK,    "Organization"),
        ("School submits report to accident insurance provider", SEND_TASK, "Organization"),

        ("Responsible body drafts report",                   USER_TASK,    "Organization"),
        ("Responsible body submits report to accident insurance provider", SEND_TASK, "Organization"),

        ("Self-employed drafts accident report",             USER_TASK,    "Reporter"),
        ("Self-employed submits report to accident insurance provider", SEND_TASK, "Reporter"),

        ("Accident insurer receives report",                 RECEIVE_TASK, "Accident Insurer"),
        ("Register claim and request missing info",          SERVICE_TASK, "Accident Insurer"),

        ("Private insurance also involved?",                 EXCLUSIVE_GW, "Accident Insurer"),
        ("Insured reports to private insurer (written, immediately)", USER_TASK, "Reporter"),
        ("Private insurer opens claim",                      SERVICE_TASK, "Inspectorate or Private Insurer"),

        ("End - Report completed",                           END,          "Accident Insurer"),
    ],

    "data_objects": [
        ("Medical Certificate",              "Reporter",     2),
        ("Incident Info",                    "Reporter",     4),
        ("Accident Report (Org)",            "Organization", 12),
        ("Accident Report (Self-employed)",  "Reporter",     12),
    ],

    "data_associations": [
        ("Get medical assessment (if needed)",               "Medical Certificate"),
        ("Collect incident information (who/where/when/what)", "Incident Info"),
        ("Incident Info",                                    "Assess work-accident coverage circumstances"),
        ("Medical Certificate",                              "Assess work-accident coverage circumstances"),

        ("Employer drafts accident report",                  "Accident Report (Org)"),
        ("School/university drafts report (3 copies)",       "Accident Report (Org)"),
        ("Responsible body drafts report",                   "Accident Report (Org)"),

        ("Accident Report (Org)",                            "Employer submits report to accident insurance provider"),
        ("Accident Report (Org)",                            "School submits report to accident insurance provider"),
        ("Accident Report (Org)",                            "Responsible body submits report to accident insurance provider"),

        ("Self-employed drafts accident report",             "Accident Report (Self-employed)"),
        ("Accident Report (Self-employed)",                  "Self-employed submits report to accident insurance provider"),
    ],

    "flows": [
        ("Start",                                            "Secure scene and provide first aid", ""),
        ("Secure scene and provide first aid",               "Get medical assessment (if needed)", ""),
        ("Get medical assessment (if needed)",               "Notify employer or responsible body immediately", ""),
        ("Notify employer or responsible body immediately",  "Collect incident information (who/where/when/what)", ""),
        ("Collect incident information (who/where/when/what)", "Incident type?", ""),

        ("Incident type?",                                   "Log near miss / dangerous occurrence", "Near miss"),
        ("Incident type?",                                   "Log serious and immediate risk", "Serious risk"),
        ("Incident type?",                                   "Log defect in protection systems", "Protection defect"),
        ("Incident type?",                                   "Assess work-accident coverage circumstances", "Work accident"),

        ("Log near miss / dangerous occurrence",             "Implement corrective actions", ""),
        ("Log serious and immediate risk",                   "Implement corrective actions", ""),
        ("Log defect in protection systems",                 "Implement corrective actions", ""),
        ("Implement corrective actions",                     "End - Corrective actions completed", ""),

        ("Assess work-accident coverage circumstances",      "Covered as work accident/equivalent?", ""),
        ("Covered as work accident/equivalent?",             "Record as non-covered incident", "No"),
        ("Record as non-covered incident",                   "End - Not covered", ""),

        ("Covered as work accident/equivalent?",             "Fatality or serious injury?", "Yes"),
        ("Fatality or serious injury?",                      "Report immediately to Labour Inspectorate", "Yes"),
        ("Report immediately to Labour Inspectorate",        "Labour Inspectorate receives report", ""),
        ("Labour Inspectorate receives report",              "Person group?", ""),

        ("Fatality or serious injury?",                      "Person group?", "No"),

        ("Person group?",                                    "Employer drafts accident report", "Employee (insured employment)"),
        ("Employer drafts accident report",                  "Employer submits report to accident insurance provider", ""),

        ("Person group?",                                    "School/university drafts report (3 copies)", "Student/schoolchild"),
        ("School/university drafts report (3 copies)",       "School submits report to accident insurance provider", ""),

        ("Person group?",                                    "Responsible body drafts report", "Other covered (aid org/unemployment/etc.)"),
        ("Responsible body drafts report",                   "Responsible body submits report to accident insurance provider", ""),

        ("Person group?",                                    "Self-employed drafts accident report", "Self-employed"),
        ("Self-employed drafts accident report",             "Self-employed submits report to accident insurance provider", ""),

        ("Employer submits report to accident insurance provider", "Accident insurer receives report", ""),
        ("School submits report to accident insurance provider",   "Accident insurer receives report", ""),
        ("Responsible body submits report to accident insurance provider", "Accident insurer receives report", ""),
        ("Self-employed submits report to accident insurance provider",     "Accident insurer receives report", ""),

        ("Accident insurer receives report",                 "Register claim and request missing info", ""),
        ("Register claim and request missing info",          "Private insurance also involved?", ""),

        ("Private insurance also involved?",                 "Insured reports to private insurer (written, immediately)", "Yes"),
        ("Insured reports to private insurer (written, immediately)", "Private insurer opens claim", ""),
        ("Private insurer opens claim",                      "End - Report completed", ""),

        ("Private insurance also involved?",                 "End - Report completed", "No"),
    ],

    "layout": {
        "Start":                                            0,
        "Secure scene and provide first aid":               1,
        "Get medical assessment (if needed)":               2,
        "Notify employer or responsible body immediately":  3,
        "Collect incident information (who/where/when/what)": 4,

        "Incident type?":                                   5,

        # Same lane + same column -> auto-stacked
        "Log near miss / dangerous occurrence":             6,
        "Log serious and immediate risk":                   6,
        "Log defect in protection systems":                 6,
        "Assess work-accident coverage circumstances":      6,

        "Implement corrective actions":                     7,
        "End - Corrective actions completed":               8,

        "Covered as work accident/equivalent?":             7,
        "Record as non-covered incident":                   8,
        "End - Not covered":                                9,

        "Fatality or serious injury?":                      8,
        "Report immediately to Labour Inspectorate":        9,
        "Labour Inspectorate receives report":              10,

        "Person group?":                                    11,

        "Employer drafts accident report":                  12,
        "School/university drafts report (3 copies)":       12,
        "Responsible body drafts report":                   12,
        "Self-employed drafts accident report":             12,

        "Employer submits report to accident insurance provider": 13,
        "School submits report to accident insurance provider":   13,
        "Responsible body submits report to accident insurance provider": 13,
        "Self-employed submits report to accident insurance provider":     13,

        "Accident insurer receives report":                 14,
        "Register claim and request missing info":          15,

        "Private insurance also involved?":                 16,
        "Insured reports to private insurer (written, immediately)": 17,
        "Private insurer opens claim":                      18,

        "End - Report completed":                           19,
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
