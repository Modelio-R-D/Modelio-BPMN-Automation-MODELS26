#
# LAN_Party.py
#
# Description: Plan a LAN party: invite friends, collect games, find a date with >=8 attendees (loop),
#              check/download missing games in parallel, then plan/buy beer and enjoy the party.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LAN Party",

    "lanes": ["Host", "Friends"],

    "elements": [
        ("Start",                     START,        "Host"),
        ("Send Invitations",          SEND_TASK,    "Host"),

        ("Send Game Requests",        USER_TASK,    "Friends"),
        ("Receive Game List",         RECEIVE_TASK, "Host"),

        ("Plan In Parallel",          PARALLEL_GW,  "Host"),

        # Date finding loop (needs >= 8)
        ("Propose Date",              USER_TASK,    "Host"),
        ("Confirm Availability",      USER_TASK,    "Friends"),
        ("8 Or More Free?",           EXCLUSIVE_GW, "Host"),
        ("Date Ready",                TASK,         "Host"),

        # Game availability check (parallel)
        ("Check Games Availability",  SERVICE_TASK, "Host"),
        ("Any Games Missing?",        EXCLUSIVE_GW, "Host"),
        ("Download Missing Games",    SERVICE_TASK, "Host"),
        ("Games Ready",               TASK,         "Host"),

        ("Planning Complete",         PARALLEL_GW,  "Host"),

        # Beer planning
        ("Estimate Beer Needed",      USER_TASK,    "Host"),
        ("Check Beer Stock",          TASK,         "Host"),
        ("Enough Beer?",              EXCLUSIVE_GW, "Host"),
        ("Buy Missing Beer",          USER_TASK,    "Host"),

        ("Enjoy LAN Party",           TASK,         "Host"),
        ("End",                       END,          "Host"),
    ],

    "flows": [
        ("Start",                "Send Invitations",        ""),
        ("Send Invitations",     "Send Game Requests",      ""),
        ("Send Game Requests",   "Receive Game List",       ""),

        ("Receive Game List",    "Plan In Parallel",        ""),

        # Parallel split
        ("Plan In Parallel",     "Propose Date",            ""),
        ("Plan In Parallel",     "Check Games Availability",""),

        # Date branch with loop until >=8
        ("Propose Date",         "Confirm Availability",    ""),
        ("Confirm Availability", "8 Or More Free?",         ""),
        ("8 Or More Free?",      "Date Ready",              "Yes (>=8)"),
        ("8 Or More Free?",      "Propose Date",            "No (<8)"),

        # Games branch
        ("Check Games Availability", "Any Games Missing?",   ""),
        ("Any Games Missing?",       "Download Missing Games","Yes"),
        ("Any Games Missing?",       "Games Ready",          "No"),
        ("Download Missing Games",   "Games Ready",          ""),

        # Parallel join
        ("Date Ready",           "Planning Complete",       ""),
        ("Games Ready",          "Planning Complete",       ""),

        # Beer + party
        ("Planning Complete",    "Estimate Beer Needed",    ""),
        ("Estimate Beer Needed", "Check Beer Stock",        ""),
        ("Check Beer Stock",     "Enough Beer?",            ""),
        ("Enough Beer?",         "Enjoy LAN Party",         "Yes"),
        ("Enough Beer?",         "Buy Missing Beer",        "No"),
        ("Buy Missing Beer",     "Enjoy LAN Party",         ""),
        ("Enjoy LAN Party",      "End",                     ""),
    ],

    "layout": {
        "Start":                    0,
        "Send Invitations":         1,

        "Send Game Requests":       2,
        "Receive Game List":        3,

        "Plan In Parallel":         4,

        # Parallel work (auto-stacked where same lane+column)
        "Propose Date":             5,
        "Check Games Availability": 5,

        "Confirm Availability":     6,
        "Any Games Missing?":       6,

        "8 Or More Free?":          7,
        "Download Missing Games":   7,

        "Date Ready":               8,
        "Games Ready":              8,

        "Planning Complete":        9,

        "Estimate Beer Needed":     10,
        "Check Beer Stock":         11,
        "Enough Beer?":             12,
        "Buy Missing Beer":         13,
        "Enjoy LAN Party":          14,
        "End":                      15,
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
