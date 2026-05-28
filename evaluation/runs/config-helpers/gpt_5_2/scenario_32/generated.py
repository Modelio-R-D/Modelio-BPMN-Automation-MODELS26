#
# Farming_Bot.py
#
# Description: Players configure a custom farming bot with priorities and dependencies, then the bot farms (with updates, milestones, and setbacks) and finally shares results with friends.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Farming Bot",

    "lanes": [
        "Player",
        "Farming Bot",
        "Game World",
        "Friends"
    ],

    "elements": [
        # Player configuration
        ("Start",                          START,        "Player"),
        ("Choose target resources",         USER_TASK,    "Player"),
        ("Set priorities (urgent first)",   USER_TASK,    "Player"),
        ("Define dependency rules",         USER_TASK,    "Player"),
        ("Confirm bot configuration",       USER_TASK,    "Player"),

        # Bot planning
        ("Analyze resource dependencies",   SERVICE_TASK, "Farming Bot"),
        ("Plan tools and route",            SERVICE_TASK, "Farming Bot"),
        ("Tools needed?",                   EXCLUSIVE_GW, "Farming Bot"),
        ("Craft required tools",            SERVICE_TASK, "Farming Bot"),
        ("Start farming",                   SERVICE_TASK, "Farming Bot"),

        # Farming loop control (events that can happen during farming)
        ("Farming event hub",               EVENT_BASED_GW,   "Farming Bot"),
        ("Update request received",         MESSAGE_CATCH,    "Farming Bot"),
        ("Disaster detected",               SIGNAL_CATCH,     "Farming Bot"),
        ("Next farming tick",               TIMER_CATCH,      "Farming Bot"),

        ("Replan farming queue",            SERVICE_TASK, "Farming Bot"),
        ("Recover from disaster",           SERVICE_TASK, "Farming Bot"),

        # Parallel collection (represents up to 10 resources; shown as 3 example batches)
        ("Split collectors (max 10)",       PARALLEL_GW,  "Farming Bot"),
        ("Collect batch A",                 SERVICE_TASK, "Farming Bot"),
        ("Collect batch B",                 SERVICE_TASK, "Farming Bot"),
        ("Collect batch C",                 SERVICE_TASK, "Farming Bot"),
        ("Join collectors",                 PARALLEL_GW,  "Farming Bot"),

        # Milestones + continuation
        ("Milestone reached?",              EXCLUSIVE_GW, "Farming Bot"),
        ("Notify milestone",                SEND_TASK,    "Farming Bot"),
        ("Receive milestone notification",  RECEIVE_TASK, "Player"),
        ("More resources needed?",          EXCLUSIVE_GW, "Farming Bot"),

        # Finish + share
        ("Finish farming",                  SERVICE_TASK, "Farming Bot"),
        ("Review results",                  USER_TASK,    "Player"),

        ("Share results?",                  EXCLUSIVE_GW, "Player"),
        ("Split share actions",             PARALLEL_GW,  "Player"),
        ("Brag to friends",                 SEND_TASK,    "Player"),
        ("Send materials to friends",       SEND_TASK,    "Player"),
        ("Join share actions",              PARALLEL_GW,  "Player"),

        ("Friends receive brag",            RECEIVE_TASK, "Friends"),
        ("Friends receive materials",       RECEIVE_TASK, "Friends"),

        ("End",                             END,         "Player"),

        # Optional explicit world trigger (for readability; used as a source for the disaster concept)
        ("Natural disaster strikes",         SIGNAL_THROW, "Game World"),

        # Optional player update action (can be performed during farming)
        ("Request update to materials list", USER_TASK,    "Player"),
    ],

    "data_objects": [
        ("Resource list",        "Player",      1),
        ("Priority list",        "Player",      2),
        ("Dependency rules doc", "Player",      3),
        ("Tool plan",            "Farming Bot",  6),
        ("Collected materials",  "Farming Bot", 14),
        ("Gift materials",       "Player",      23),
    ],

    "data_associations": [
        ("Choose target resources",       "Resource list"),
        ("Resource list",                 "Set priorities (urgent first)"),
        ("Set priorities (urgent first)", "Priority list"),
        ("Define dependency rules",       "Dependency rules doc"),

        ("Priority list",                 "Analyze resource dependencies"),
        ("Dependency rules doc",          "Analyze resource dependencies"),

        ("Plan tools and route",          "Tool plan"),
        ("Tool plan",                     "Craft required tools"),

        ("Collect batch A",               "Collected materials"),
        ("Collect batch B",               "Collected materials"),
        ("Collect batch C",               "Collected materials"),
        ("Collected materials",           "Review results"),

        ("Review results",                "Gift materials"),
        ("Gift materials",                "Send materials to friends"),
    ],

    "flows": [
        # Configuration
        ("Start",                        "Choose target resources",        ""),
        ("Choose target resources",       "Set priorities (urgent first)",  ""),
        ("Set priorities (urgent first)", "Define dependency rules",        ""),
        ("Define dependency rules",       "Confirm bot configuration",      ""),

        # Planning
        ("Confirm bot configuration",     "Analyze resource dependencies",  ""),
        ("Analyze resource dependencies", "Plan tools and route",           ""),
        ("Plan tools and route",          "Tools needed?",                  ""),

        ("Tools needed?",                "Craft required tools",           "Yes"),
        ("Tools needed?",                "Start farming",                  "No"),
        ("Craft required tools",          "Start farming",                  ""),

        # Start farming loop
        ("Start farming",                "Farming event hub",              ""),

        # Event hub branches
        ("Farming event hub",            "Update request received",        "Update"),
        ("Farming event hub",            "Disaster detected",              "Disaster"),
        ("Farming event hub",            "Next farming tick",              "Tick"),

        # Update handling (player can request updates at any time during farming)
        ("Request update to materials list", "Replan farming queue",       ""),
        ("Update request received",          "Replan farming queue",       ""),
        ("Replan farming queue",             "Farming event hub",          ""),

        # Disaster handling (world event concept)
        ("Natural disaster strikes",      "Recover from disaster",          ""),
        ("Disaster detected",             "Recover from disaster",          ""),
        ("Recover from disaster",         "Farming event hub",              ""),

        # Tick -> farm
        ("Next farming tick",             "Split collectors (max 10)",      ""),

        # Parallel collection
        ("Split collectors (max 10)",     "Collect batch A",               ""),
        ("Split collectors (max 10)",     "Collect batch B",               ""),
        ("Split collectors (max 10)",     "Collect batch C",               ""),
        ("Collect batch A",               "Join collectors",               ""),
        ("Collect batch B",               "Join collectors",               ""),
        ("Collect batch C",               "Join collectors",               ""),

        # Milestones
        ("Join collectors",               "Milestone reached?",            ""),
        ("Milestone reached?",            "Notify milestone",              "Yes"),
        ("Milestone reached?",            "More resources needed?",        "No"),
        ("Notify milestone",              "Receive milestone notification",""),
        ("Receive milestone notification","More resources needed?",        ""),

        # Continue / finish
        ("More resources needed?",        "Farming event hub",             "Yes"),
        ("More resources needed?",        "Finish farming",                "No"),

        ("Finish farming",                "Review results",                ""),

        # Share results options
        ("Review results",                "Share results?",                ""),

        ("Share results?",                "Brag to friends",               "Brag"),
        ("Share results?",                "Send materials to friends",     "Send"),
        ("Share results?",                "Split share actions",           "Both"),
        ("Share results?",                "End",                           "None"),

        ("Split share actions",           "Brag to friends",               ""),
        ("Split share actions",           "Send materials to friends",     ""),
        ("Brag to friends",               "Join share actions",            ""),
        ("Send materials to friends",     "Join share actions",            ""),
        ("Join share actions",            "End",                           ""),

        # Friend receptions (modeled as sequence for simplicity)
        ("Brag to friends",               "Friends receive brag",          ""),
        ("Send materials to friends",     "Friends receive materials",     ""),
    ],

    "layout": {
        # Player config
        "Start":                          0,
        "Choose target resources":         1,
        "Set priorities (urgent first)":   2,
        "Define dependency rules":         3,
        "Confirm bot configuration":       4,

        # Bot planning
        "Analyze resource dependencies":   5,
        "Plan tools and route":            6,
        "Tools needed?":                   7,
        "Craft required tools":            8,
        "Start farming":                   9,

        # Farming loop hub + events (auto-stacked where same column)
        "Farming event hub":               10,
        "Update request received":         11,
        "Disaster detected":               11,
        "Next farming tick":               11,

        "Replan farming queue":            12,
        "Recover from disaster":           12,

        # Parallel collection (auto-stacked batches in same column)
        "Split collectors (max 10)":       13,
        "Collect batch A":                 14,
        "Collect batch B":                 14,
        "Collect batch C":                 14,
        "Join collectors":                 15,

        # Milestones and continuation
        "Milestone reached?":              16,
        "Notify milestone":                17,
        "Receive milestone notification":  17,
        "More resources needed?":          18,

        # Finish + share
        "Finish farming":                  19,
        "Review results":                  20,
        "Share results?":                  21,
        "Split share actions":             22,
        "Brag to friends":                 23,
        "Send materials to friends":       23,
        "Join share actions":              24,
        "End":                             25,

        # Optional extras
        "Natural disaster strikes":         9,
        "Request update to materials list": 10,

        "Friends receive brag":            24,
        "Friends receive materials":       24,
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
