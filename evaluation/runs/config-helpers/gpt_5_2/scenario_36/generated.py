#
# Luxury_Airplane.py
#
# Description: Customer specifies luxury interior options; requirements go to specialist teams; parts are assembled, tested, protocol sent, and customer confirms delivery.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Luxury Airplane",

    "lanes": [
        "Customer",
        "Luxury Airplane Co.",
        "Russian Team (Vodka Bar)",
        "Irish Team (Whiskey Bar)",
        "French Team (Champagne Bar)",
        "Craft Team (Beer Bar)",
        "Wellness Team (Mocktail Bar)",
        "Seat Team",
        "Color and Trim Team",
        "Toilet Team",
        "Electronics Team",
        "Assembly Team",
        "QA Flight Crew",
    ],

    "elements": [
        ("Start",                         START,          "Customer"),
        ("Choose luxury options",          USER_TASK,      "Customer"),
        ("Send specifications",            SEND_TASK,      "Customer"),

        ("Receive specifications",         RECEIVE_TASK,   "Luxury Airplane Co."),
        ("Validate specifications",        SERVICE_TASK,   "Luxury Airplane Co."),
        ("Create requirements package",    SERVICE_TASK,   "Luxury Airplane Co."),

        ("Dispatch requirements",          PARALLEL_GW,    "Luxury Airplane Co."),

        ("Select bar type",               EXCLUSIVE_GW,   "Luxury Airplane Co."),
        ("Manufacture vodka bar",          TASK,           "Russian Team (Vodka Bar)"),
        ("Manufacture whiskey bar",        TASK,           "Irish Team (Whiskey Bar)"),
        ("Manufacture champagne bar",      TASK,           "French Team (Champagne Bar)"),
        ("Manufacture craft beer bar",     TASK,           "Craft Team (Beer Bar)"),
        ("Manufacture mocktail bar",       TASK,           "Wellness Team (Mocktail Bar)"),
        ("Bar completed",                 EXCLUSIVE_GW,   "Luxury Airplane Co."),

        ("Manufacture luxury seats",       TASK,           "Seat Team"),
        ("Produce seat covers and trim",  TASK,           "Color and Trim Team"),
        ("Configure toilets and water",   TASK,           "Toilet Team"),
        ("Build mood lighting system",    SERVICE_TASK,   "Electronics Team"),

        ("Wait for all parts",            PARALLEL_GW,     "Luxury Airplane Co."),

        ("Build base airplane (standard)", TASK,          "Assembly Team"),
        ("Assemble luxury interior",       TASK,           "Assembly Team"),

        ("Test flight",                    TASK,           "QA Flight Crew"),
        ("Create test protocol",           SERVICE_TASK,   "QA Flight Crew"),

        ("Distribute protocol",            PARALLEL_GW,    "QA Flight Crew"),
        ("Send protocol to customer",      SEND_TASK,      "QA Flight Crew"),
        ("Send protocol to manufacturer",  SEND_TASK,      "QA Flight Crew"),
        ("Protocol distributed",           PARALLEL_GW,    "QA Flight Crew"),

        ("Deliver airplane",               SEND_TASK,      "Luxury Airplane Co."),
        ("Confirm delivery",               USER_TASK,      "Customer"),
        ("Receive confirmation",           RECEIVE_TASK,   "Luxury Airplane Co."),
        ("End",                            END,            "Luxury Airplane Co."),
    ],

    "data_objects": [
        ("Customer specifications",        "Customer",            1),
        ("Requirements package",           "Luxury Airplane Co.",  5),
        ("Test protocol",                  "QA Flight Crew",      14),
        ("Acceptance confirmation",        "Customer",            19),
    ],

    "data_associations": [
        ("Choose luxury options",          "Customer specifications"),
        ("Customer specifications",        "Send specifications"),

        ("Receive specifications",         "Requirements package"),
        ("Requirements package",           "Manufacture vodka bar"),
        ("Requirements package",           "Manufacture whiskey bar"),
        ("Requirements package",           "Manufacture champagne bar"),
        ("Requirements package",           "Manufacture craft beer bar"),
        ("Requirements package",           "Manufacture mocktail bar"),
        ("Requirements package",           "Manufacture luxury seats"),
        ("Requirements package",           "Produce seat covers and trim"),
        ("Requirements package",           "Configure toilets and water"),
        ("Requirements package",           "Build mood lighting system"),

        ("Create test protocol",           "Test protocol"),
        ("Test protocol",                  "Send protocol to customer"),
        ("Test protocol",                  "Send protocol to manufacturer"),

        ("Confirm delivery",               "Acceptance confirmation"),
        ("Acceptance confirmation",        "Receive confirmation"),
    ],

    "flows": [
        ("Start",                      "Choose luxury options",       ""),
        ("Choose luxury options",       "Send specifications",         ""),
        ("Send specifications",         "Receive specifications",      ""),

        ("Receive specifications",      "Validate specifications",     ""),
        ("Validate specifications",     "Create requirements package", ""),
        ("Create requirements package", "Dispatch requirements",       ""),

        ("Dispatch requirements",       "Select bar type",             ""),
        ("Select bar type",             "Manufacture vodka bar",        "Vodka bar"),
        ("Select bar type",             "Manufacture whiskey bar",      "Whiskey bar"),
        ("Select bar type",             "Manufacture champagne bar",    "Champagne bar"),
        ("Select bar type",             "Manufacture craft beer bar",   "Craft beer bar"),
        ("Select bar type",             "Manufacture mocktail bar",     "Mocktail bar"),

        ("Manufacture vodka bar",       "Bar completed",               ""),
        ("Manufacture whiskey bar",     "Bar completed",               ""),
        ("Manufacture champagne bar",   "Bar completed",               ""),
        ("Manufacture craft beer bar",  "Bar completed",               ""),
        ("Manufacture mocktail bar",    "Bar completed",               ""),

        ("Dispatch requirements",       "Manufacture luxury seats",     ""),
        ("Dispatch requirements",       "Produce seat covers and trim", ""),
        ("Dispatch requirements",       "Configure toilets and water",  ""),
        ("Dispatch requirements",       "Build mood lighting system",   ""),

        ("Bar completed",               "Wait for all parts",           ""),
        ("Manufacture luxury seats",    "Wait for all parts",           ""),
        ("Produce seat covers and trim","Wait for all parts",           ""),
        ("Configure toilets and water", "Wait for all parts",           ""),
        ("Build mood lighting system",  "Wait for all parts",           ""),

        ("Wait for all parts",          "Build base airplane (standard)",""),
        ("Build base airplane (standard)","Assemble luxury interior",    ""),

        ("Assemble luxury interior",    "Test flight",                  ""),
        ("Test flight",                 "Create test protocol",         ""),

        ("Create test protocol",        "Distribute protocol",          ""),
        ("Distribute protocol",         "Send protocol to customer",    ""),
        ("Distribute protocol",         "Send protocol to manufacturer",""),
        ("Send protocol to customer",   "Protocol distributed",         ""),
        ("Send protocol to manufacturer","Protocol distributed",        ""),

        ("Protocol distributed",        "Deliver airplane",             ""),
        ("Deliver airplane",            "Confirm delivery",             ""),
        ("Confirm delivery",            "Receive confirmation",         ""),
        ("Receive confirmation",        "End",                          ""),
    ],

    "layout": {
        "Start":                         0,
        "Choose luxury options":          1,
        "Send specifications":            2,

        "Receive specifications":         3,
        "Validate specifications":        4,
        "Create requirements package":    5,

        "Dispatch requirements":          6,

        "Select bar type":                7,
        "Manufacture luxury seats":       7,
        "Produce seat covers and trim":   7,
        "Configure toilets and water":    7,
        "Build mood lighting system":     7,

        "Manufacture vodka bar":          8,
        "Manufacture whiskey bar":        8,
        "Manufacture champagne bar":      8,
        "Manufacture craft beer bar":     8,
        "Manufacture mocktail bar":       8,

        "Bar completed":                  9,

        "Wait for all parts":            10,

        "Build base airplane (standard)": 11,
        "Assemble luxury interior":       12,

        "Test flight":                    13,
        "Create test protocol":           14,

        "Distribute protocol":            15,
        "Send protocol to customer":      16,  # auto-stacked with next element (same lane, same column)
        "Send protocol to manufacturer":  16,
        "Protocol distributed":           17,

        "Deliver airplane":               18,
        "Confirm delivery":               19,
        "Receive confirmation":           20,
        "End":                            21,
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
