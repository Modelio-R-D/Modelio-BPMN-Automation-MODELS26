#
# BlizzardOnlineCharacterGenerator.py
#
# Description: Blizzard online tool to create a WoW character with parallel account setup and name brainstorming,
#              including subscription/payment handling, name availability loop, and post-creation notifications.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Blizzard Online Character Generator",

    "lanes": ["Player", "Blizzard"],

    "elements": [
        ("Start",                             START,         "Player"),

        ("Setup and naming in parallel",       PARALLEL_GW,   "Player"),

        # Parallel branch A - naming
        ("Brainstorm character names",         USER_TASK,     "Player"),
        ("Names ready",                        TASK,          "Player"),

        # Parallel branch B - account and subscription setup
        ("Check battle.net account",           SERVICE_TASK,  "Blizzard"),
        ("Battle.net account?",                EXCLUSIVE_GW,  "Blizzard"),
        ("Enter battle.net account information", USER_TASK,   "Player"),
        ("Send confirmation email",            SERVICE_TASK,  "Blizzard"),
        ("Click confirmation link",            USER_TASK,     "Player"),

        ("Check WoW subscription",             SERVICE_TASK,  "Blizzard"),
        ("Active subscription?",               EXCLUSIVE_GW,  "Blizzard"),

        ("Select payment method",              USER_TASK,     "Player"),
        ("Payment method?",                    EXCLUSIVE_GW,  "Player"),
        ("Enter credit card information",      USER_TASK,     "Player"),
        ("Enter IBAN and BIC",                 USER_TASK,     "Player"),
        ("Payment complete",                   EXCLUSIVE_GW,  "Player"),
        ("Activate subscription",              SERVICE_TASK,  "Blizzard"),

        ("Log into game",                      USER_TASK,     "Player"),
        ("Select realm, race and class",       USER_TASK,     "Player"),

        ("Ready to create character",          PARALLEL_GW,   "Player"),

        # Name availability loop
        ("Enter character name",               USER_TASK,     "Player"),
        ("Check name availability",            SERVICE_TASK,  "Blizzard"),
        ("Name available?",                    EXCLUSIVE_GW,  "Blizzard"),

        # Completion and notifications
        ("Create character",                   SERVICE_TASK,  "Blizzard"),
        ("Send confirmation",                  SERVICE_TASK,  "Blizzard"),
        ("Generate character selfies",         SERVICE_TASK,  "Blizzard"),
        ("Wait for expansion release",         SIGNAL_CATCH,  "Blizzard"),
        ("Send expansion release message",     SERVICE_TASK,  "Blizzard"),

        ("End",                                END,           "Player"),
    ],

    "flows": [
        ("Start", "Setup and naming in parallel", ""),

        # Parallel split
        ("Setup and naming in parallel", "Brainstorm character names", ""),
        ("Setup and naming in parallel", "Check battle.net account", ""),

        # Naming branch
        ("Brainstorm character names", "Names ready", ""),
        ("Names ready", "Ready to create character", ""),

        # Account branch - battle.net account
        ("Check battle.net account", "Battle.net account?", ""),
        ("Battle.net account?", "Check WoW subscription", "Yes"),
        ("Battle.net account?", "Enter battle.net account information", "No"),
        ("Enter battle.net account information", "Send confirmation email", ""),
        ("Send confirmation email", "Click confirmation link", ""),
        ("Click confirmation link", "Check WoW subscription", ""),

        # Subscription check
        ("Check WoW subscription", "Active subscription?", ""),
        ("Active subscription?", "Log into game", "Yes"),
        ("Active subscription?", "Select payment method", "No"),

        # Payment handling
        ("Select payment method", "Payment method?", ""),
        ("Payment method?", "Enter credit card information", "Credit card"),
        ("Payment method?", "Enter IBAN and BIC", "Bank account"),
        ("Enter credit card information", "Payment complete", ""),
        ("Enter IBAN and BIC", "Payment complete", ""),
        ("Payment complete", "Activate subscription", ""),
        ("Activate subscription", "Log into game", ""),

        # Character setup and parallel join
        ("Log into game", "Select realm, race and class", ""),
        ("Select realm, race and class", "Ready to create character", ""),

        # Name loop
        ("Ready to create character", "Enter character name", ""),
        ("Enter character name", "Check name availability", ""),
        ("Check name availability", "Name available?", ""),
        ("Name available?", "Enter character name", "No"),
        ("Name available?", "Create character", "Yes"),

        # Finish and later notification
        ("Create character", "Send confirmation", ""),
        ("Send confirmation", "Generate character selfies", ""),
        ("Generate character selfies", "Wait for expansion release", ""),
        ("Wait for expansion release", "Send expansion release message", ""),
        ("Send expansion release message", "End", ""),
    ],

    "layout": {
        "Start":                               0,
        "Setup and naming in parallel":         1,

        "Brainstorm character names":           2,
        "Names ready":                          3,

        "Check battle.net account":             2,
        "Battle.net account?":                  3,
        "Enter battle.net account information": 4,
        "Send confirmation email":              5,
        "Click confirmation link":              6,

        "Check WoW subscription":               7,
        "Active subscription?":                 8,
        "Select payment method":                9,
        "Payment method?":                      10,
        "Enter credit card information":        11,
        "Enter IBAN and BIC":                   11,  # auto-stacked (same lane, same column)
        "Payment complete":                     12,
        "Activate subscription":                13,

        "Log into game":                        14,
        "Select realm, race and class":         15,

        "Ready to create character":            16,

        "Enter character name":                 17,
        "Check name availability":              18,
        "Name available?":                      19,

        "Create character":                     20,
        "Send confirmation":                    21,
        "Generate character selfies":           22,
        "Wait for expansion release":           23,
        "Send expansion release message":       24,

        "End":                                  25,
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
