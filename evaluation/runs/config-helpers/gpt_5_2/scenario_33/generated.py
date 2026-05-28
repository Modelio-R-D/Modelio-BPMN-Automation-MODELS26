#
# InstructArtist_Create3DModel_3DPrint.py
#
# Description: Instruct an artist to create a 3D model, procure filament, prepare the printer, generate G-code, and print.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "InstructArtist_Create3DModel_3DPrint",

    "lanes": ["Customer", "Artist", "3D Printer"],

    "elements": [
        ("Start",                      START,             "Customer"),
        ("Send sketches",              SEND_TASK,         "Customer"),
        ("Create 3D model",            USER_TASK,         "Artist"),
        ("Send STL",                   SEND_TASK,         "Artist"),
        ("Review STL",                 USER_TASK,         "Customer"),
        ("Satisfied?",                 EXCLUSIVE_GW,      "Customer"),

        ("Send change requests",       SEND_TASK,         "Customer"),
        ("Revise model",               USER_TASK,         "Artist"),
        ("Send revised STL",           SEND_TASK,         "Artist"),

        ("Select plastic color",       USER_TASK,         "Customer"),
        ("Color in stock?",            EXCLUSIVE_GW,      "Customer"),
        ("Check filament amount",      USER_TASK,         "Customer"),
        ("Under 100g?",                EXCLUSIVE_GW,      "Customer"),
        ("Add filament to shopping list", USER_TASK,      "Customer"),
        ("Order filament",             USER_TASK,         "Customer"),
        ("Filament available",         TASK,              "Customer"),

        ("Turn on printer",            MANUAL_TASK,       "3D Printer"),
        ("Prep in parallel",           PARALLEL_GW,       "3D Printer"),
        ("Heat bed and extruder",      SERVICE_TASK,      "3D Printer"),
        ("Generate G-code",            SCRIPT_TASK,       "Customer"),
        ("Ready to print",             PARALLEL_GW,       "3D Printer"),
        ("Print model",                SERVICE_TASK,      "3D Printer"),
        ("End",                        END,               "3D Printer"),
    ],

    "flows": [
        ("Start",                 "Send sketches",               ""),
        ("Send sketches",         "Create 3D model",             ""),
        ("Create 3D model",       "Send STL",                    ""),
        ("Send STL",              "Review STL",                  ""),
        ("Review STL",            "Satisfied?",                  ""),

        ("Satisfied?",            "Select plastic color",        "Yes"),
        ("Satisfied?",            "Send change requests",        "No"),

        ("Send change requests",  "Revise model",                ""),
        ("Revise model",          "Send revised STL",            ""),
        ("Send revised STL",      "Review STL",                  ""),

        ("Select plastic color",  "Color in stock?",             ""),
        ("Color in stock?",       "Check filament amount",       "Yes"),
        ("Color in stock?",       "Order filament",              "No"),

        ("Check filament amount", "Under 100g?",                 ""),
        ("Under 100g?",           "Add filament to shopping list","Yes"),
        ("Under 100g?",           "Filament available",          "No"),
        ("Add filament to shopping list", "Filament available",  ""),
        ("Order filament",        "Filament available",          ""),

        ("Filament available",    "Turn on printer",             ""),
        ("Turn on printer",       "Prep in parallel",            ""),
        ("Prep in parallel",      "Heat bed and extruder",       ""),
        ("Prep in parallel",      "Generate G-code",             ""),
        ("Heat bed and extruder", "Ready to print",              ""),
        ("Generate G-code",       "Ready to print",              ""),
        ("Ready to print",        "Print model",                 ""),
        ("Print model",           "End",                         ""),
    ],

    "layout": {
        "Start":                        0,
        "Send sketches":                1,
        "Create 3D model":              2,
        "Send STL":                     3,
        "Review STL":                   4,
        "Satisfied?":                   5,

        # Same lane + same column => auto-stacked alternatives
        "Select plastic color":         6,
        "Send change requests":         6,

        "Revise model":                 7,
        "Color in stock?":              7,
        "Send revised STL":             8,

        # Same lane + same column => auto-stacked alternatives
        "Check filament amount":        8,
        "Order filament":               8,

        "Under 100g?":                  9,
        "Add filament to shopping list": 10,
        "Filament available":           11,

        "Turn on printer":              12,
        "Prep in parallel":             13,
        "Heat bed and extruder":        14,
        "Generate G-code":              14,
        "Ready to print":               15,
        "Print model":                  16,
        "End":                          17,
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
