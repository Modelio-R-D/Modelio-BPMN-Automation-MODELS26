#
# DIY_Repair_Broken_Smartphone_Screen.py
#
# Description: DIY smartphone screen repair assisted by an online tool, including sourcing missing items, repair instructions, and post-repair review or expert fallback.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DIY Repair of a Broken Smartphone Screen",

    "lanes": ["DIYer", "Online Tool", "Friends", "Online Shop", "Expert"],

    "elements": [
        ("Start",                        START,              "DIYer"),

        ("Enter model and damage",       USER_TASK,          "DIYer"),
        ("Generate lists and options",   SERVICE_TASK,       "Online Tool"),
        ("Check what you already have",  USER_TASK,          "DIYer"),

        ("Missing items?",               EXCLUSIVE_GW,       "DIYer"),

        ("Ask friends for items",        SEND_TASK,          "DIYer"),
        ("Friends consider request",     USER_TASK,          "Friends"),
        ("Friends send offer",           SEND_TASK,          "Friends"),
        ("Receive offers",               RECEIVE_TASK,       "DIYer"),

        ("Got everything from friends?", EXCLUSIVE_GW,       "DIYer"),

        ("Buy remaining items",          USER_TASK,          "DIYer"),
        ("Shop fulfills order",          SERVICE_TASK,       "Online Shop"),
        ("Receive deliveries",           RECEIVE_TASK,       "DIYer"),

        ("Provide repair instructions",  SERVICE_TASK,       "Online Tool"),
        ("Repair phone",                 MANUAL_TASK,        "DIYer"),

        ("Repair successful?",           EXCLUSIVE_GW,       "DIYer"),

        ("Create review/video",          USER_TASK,          "DIYer"),
        ("Submit review/video",          SEND_TASK,          "DIYer"),
        ("End - Fixed",                  END,                "DIYer"),

        ("Send phone to expert",         SEND_TASK,          "DIYer"),
        ("Expert repairs phone",         SERVICE_TASK,       "Expert"),
        ("End - Repaired by expert",     END,                "Expert"),
    ],

    "data_objects": [
        ("Model and damage info",        "DIYer",       1),
        ("Materials list",               "Online Tool", 2),
        ("Tools list",                   "Online Tool", 2),
        ("Order options",                "Online Tool", 2),
        ("Missing items list",           "DIYer",       3),
        ("Friend offers",                "DIYer",       7),
        ("Purchased items",              "DIYer",      10),
        ("Repair instructions",          "DIYer",      13),
        ("Review/video",                 "DIYer",      16),
        ("Phone shipment",               "DIYer",      16),
        ("Repaired phone",               "Expert",     17),
    ],

    "data_associations": [
        ("Enter model and damage",       "Model and damage info"),
        ("Model and damage info",        "Generate lists and options"),

        ("Generate lists and options",   "Materials list"),
        ("Generate lists and options",   "Tools list"),
        ("Generate lists and options",   "Order options"),

        ("Materials list",               "Check what you already have"),
        ("Tools list",                   "Check what you already have"),
        ("Order options",                "Check what you already have"),

        ("Check what you already have",  "Missing items list"),
        ("Missing items list",           "Ask friends for items"),

        ("Friends send offer",           "Friend offers"),
        ("Friend offers",                "Receive offers"),

        ("Buy remaining items",          "Purchased items"),
        ("Purchased items",              "Provide repair instructions"),

        ("Provide repair instructions",  "Repair instructions"),
        ("Repair instructions",          "Repair phone"),

        ("Create review/video",          "Review/video"),
        ("Review/video",                 "Submit review/video"),

        ("Send phone to expert",         "Phone shipment"),
        ("Phone shipment",               "Expert repairs phone"),
        ("Expert repairs phone",         "Repaired phone"),
    ],

    "flows": [
        ("Start",                        "Enter model and damage",       ""),
        ("Enter model and damage",       "Generate lists and options",   ""),
        ("Generate lists and options",   "Check what you already have",  ""),
        ("Check what you already have",  "Missing items?",               ""),

        ("Missing items?",               "Ask friends for items",         "Yes"),
        ("Missing items?",               "Provide repair instructions",   "No"),

        ("Ask friends for items",        "Friends consider request",      ""),
        ("Friends consider request",     "Friends send offer",            ""),
        ("Friends send offer",           "Receive offers",                ""),
        ("Receive offers",               "Got everything from friends?",  ""),

        ("Got everything from friends?", "Provide repair instructions",   "Yes"),
        ("Got everything from friends?", "Buy remaining items",           "No"),

        ("Buy remaining items",          "Shop fulfills order",           ""),
        ("Shop fulfills order",          "Receive deliveries",            ""),
        ("Receive deliveries",           "Provide repair instructions",   ""),

        ("Provide repair instructions",  "Repair phone",                  ""),
        ("Repair phone",                 "Repair successful?",            ""),

        ("Repair successful?",           "Create review/video",           "Yes"),
        ("Create review/video",          "Submit review/video",           ""),
        ("Submit review/video",          "End - Fixed",                   ""),

        ("Repair successful?",           "Send phone to expert",          "No"),
        ("Send phone to expert",         "Expert repairs phone",          ""),
        ("Expert repairs phone",         "End - Repaired by expert",      ""),
    ],

    "layout": {
        "Start":                        0,
        "Enter model and damage":       1,
        "Generate lists and options":   2,
        "Check what you already have":  3,

        "Missing items?":               4,

        "Ask friends for items":        5,
        "Friends consider request":     6,
        "Friends send offer":           7,
        "Receive offers":               8,

        "Got everything from friends?": 9,

        "Buy remaining items":          10,
        "Shop fulfills order":          11,
        "Receive deliveries":           12,

        "Provide repair instructions":  13,
        "Repair phone":                 14,

        "Repair successful?":           15,

        # Same lane + same column (16) => auto-stacked
        "Create review/video":          16,
        "Send phone to expert":         16,

        # Column 17
        "Submit review/video":          17,
        "Expert repairs phone":         17,

        # Column 18
        "End - Fixed":                  18,
        "End - Repaired by expert":     18,
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
