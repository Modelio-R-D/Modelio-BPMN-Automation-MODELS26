#
# Becoming_A_Parent.py
#
# Description: Process to plan, take, and optionally extend maternity leave (info gathering, selection, notification, confirmations).
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Becoming A Parent",

    "lanes": ["Parent", "Social Security", "Company HR"],

    "elements": [
        ("Start",                          START,           "Parent"),

        ("Fetch leave models",             USER_TASK,       "Parent"),
        ("Select leave model",             USER_TASK,       "Parent"),
        ("Collect required info",          USER_TASK,       "Parent"),

        ("Notify parties in time",         PARALLEL_GW,     "Parent"),
        ("Notify Social Security",         SEND_TASK,       "Parent"),
        ("Notify Company HR",              SEND_TASK,       "Parent"),

        ("Receive leave notice",           RECEIVE_TASK,    "Social Security"),
        ("Confirm eligibility",            SERVICE_TASK,    "Social Security"),
        ("Send SS confirmation",           SEND_TASK,       "Social Security"),

        ("Receive leave notice (HR)",      RECEIVE_TASK,    "Company HR"),
        ("Check policy and coverage",      USER_TASK,       "Company HR"),
        ("Send company info",              SEND_TASK,       "Company HR"),

        ("Receive SS confirmation",        RECEIVE_TASK,    "Parent"),
        ("Receive company info",           RECEIVE_TASK,    "Parent"),
        ("All responses received",         PARALLEL_GW,     "Parent"),

        ("Finalize leave plan",            USER_TASK,       "Parent"),
        ("Start maternity leave",          USER_TASK,       "Parent"),
        ("Leave period ends",              TIMER_CATCH,     "Parent"),

        ("Extend leave?",                  EXCLUSIVE_GW,    "Parent"),

        ("Request extension",              USER_TASK,       "Parent"),
        ("Notify extension",               PARALLEL_GW,     "Parent"),
        ("Send SS extension request",      SEND_TASK,       "Parent"),
        ("Send HR extension request",      SEND_TASK,       "Parent"),

        ("Receive extension request",      RECEIVE_TASK,    "Social Security"),
        ("Process extension (SS)",         SERVICE_TASK,    "Social Security"),
        ("Send extension confirmation",    SEND_TASK,       "Social Security"),

        ("Receive extension request (HR)", RECEIVE_TASK,    "Company HR"),
        ("Update leave plan (HR)",         USER_TASK,       "Company HR"),
        ("Send updated plan",              SEND_TASK,       "Company HR"),

        ("Receive SS extension confirmation", RECEIVE_TASK, "Parent"),
        ("Receive HR updated plan",        RECEIVE_TASK,    "Parent"),
        ("Extension responses received",   PARALLEL_GW,     "Parent"),

        ("Extended leave ends",            TIMER_CATCH,     "Parent"),
        ("End",                            END,             "Parent"),
    ],

    "data_objects": [
        ("Leave Models",        "Parent", 1),
        ("Selected Model",      "Parent", 2),
        ("Application Data",    "Parent", 3),
        ("SS Confirmation",     "Parent", 9),
        ("Company Info",        "Parent", 9),
        ("Extension Request",   "Parent", 15),
    ],

    "data_associations": [
        ("Fetch leave models",              "Leave Models"),
        ("Leave Models",                    "Select leave model"),
        ("Select leave model",              "Selected Model"),
        ("Selected Model",                  "Collect required info"),
        ("Collect required info",           "Application Data"),
        ("Application Data",                "Notify Social Security"),
        ("Application Data",                "Notify Company HR"),

        ("Receive SS confirmation",         "SS Confirmation"),
        ("Receive company info",            "Company Info"),
        ("SS Confirmation",                 "Finalize leave plan"),
        ("Company Info",                    "Finalize leave plan"),

        ("Request extension",               "Extension Request"),
        ("Extension Request",               "Send SS extension request"),
        ("Extension Request",               "Send HR extension request"),
    ],

    "flows": [
        ("Start",                    "Fetch leave models",             ""),
        ("Fetch leave models",       "Select leave model",             ""),
        ("Select leave model",       "Collect required info",          ""),

        ("Collect required info",    "Notify parties in time",         ""),
        ("Notify parties in time",   "Notify Social Security",         ""),
        ("Notify parties in time",   "Notify Company HR",              ""),

        ("Notify Social Security",   "Receive leave notice",           ""),
        ("Receive leave notice",     "Confirm eligibility",            ""),
        ("Confirm eligibility",      "Send SS confirmation",           ""),
        ("Send SS confirmation",     "Receive SS confirmation",        ""),

        ("Notify Company HR",        "Receive leave notice (HR)",      ""),
        ("Receive leave notice (HR)","Check policy and coverage",      ""),
        ("Check policy and coverage","Send company info",              ""),
        ("Send company info",        "Receive company info",           ""),

        ("Receive SS confirmation",  "All responses received",         ""),
        ("Receive company info",     "All responses received",         ""),
        ("All responses received",   "Finalize leave plan",            ""),
        ("Finalize leave plan",      "Start maternity leave",          ""),
        ("Start maternity leave",    "Leave period ends",              ""),

        ("Leave period ends",        "Extend leave?",                  ""),
        ("Extend leave?",            "End",                            "No"),

        ("Extend leave?",            "Request extension",              "Yes"),
        ("Request extension",        "Notify extension",               ""),
        ("Notify extension",         "Send SS extension request",      ""),
        ("Notify extension",         "Send HR extension request",      ""),

        ("Send SS extension request","Receive extension request",      ""),
        ("Receive extension request","Process extension (SS)",         ""),
        ("Process extension (SS)",   "Send extension confirmation",    ""),
        ("Send extension confirmation","Receive SS extension confirmation",""),

        ("Send HR extension request","Receive extension request (HR)", ""),
        ("Receive extension request (HR)","Update leave plan (HR)",     ""),
        ("Update leave plan (HR)",   "Send updated plan",              ""),
        ("Send updated plan",        "Receive HR updated plan",        ""),

        ("Receive SS extension confirmation", "Extension responses received", ""),
        ("Receive HR updated plan",  "Extension responses received",   ""),
        ("Extension responses received", "Extended leave ends",        ""),
        ("Extended leave ends",      "End",                            ""),
    ],

    "layout": {
        "Start":                          0,

        "Fetch leave models":             1,
        "Select leave model":             2,
        "Collect required info":          3,

        "Notify parties in time":         4,
        "Notify Social Security":         5,
        "Notify Company HR":              5,

        "Receive leave notice":           6,
        "Receive leave notice (HR)":      6,

        "Confirm eligibility":            7,
        "Check policy and coverage":      7,

        "Send SS confirmation":           8,
        "Send company info":              8,

        "Receive SS confirmation":        9,
        "Receive company info":           9,

        "All responses received":         10,
        "Finalize leave plan":            11,
        "Start maternity leave":          12,
        "Leave period ends":              13,

        "Extend leave?":                  14,

        "Request extension":              15,
        "Notify extension":               16,
        "Send SS extension request":      17,
        "Send HR extension request":      17,

        "Receive extension request":      18,
        "Receive extension request (HR)": 18,

        "Process extension (SS)":         19,
        "Update leave plan (HR)":         19,

        "Send extension confirmation":    20,
        "Send updated plan":              20,

        "Receive SS extension confirmation": 21,
        "Receive HR updated plan":        21,

        "Extension responses received":   22,
        "Extended leave ends":            24,
        "End":                            25,
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
