#
# UltrasoundGuidedVenousAccess.py
#
# Description: Ultrasound-guided venous access with preparation, vein identification, puncture loop on failed blood return, guidewire verification loop, and catheter placement.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "UltrasoundGuidedVenousAccess",

    "lanes": ["Doctor"],

    "elements": [
        ("Start",                          START,        "Doctor"),

        ("Prep steps",                     PARALLEL_GW,  "Doctor"),
        ("Prepare implements",             USER_TASK,    "Doctor"),
        ("Wash hands",                     USER_TASK,    "Doctor"),
        ("Put on sterile clothes",         USER_TASK,    "Doctor"),
        ("Prep complete",                  PARALLEL_GW,  "Doctor"),

        ("Clean puncture area",            USER_TASK,    "Doctor"),
        ("Drape puncture zone",            USER_TASK,    "Doctor"),
        ("Configure ultrasound",           USER_TASK,    "Doctor"),
        ("Put gel on probe",               USER_TASK,    "Doctor"),
        ("Cover probe",                    USER_TASK,    "Doctor"),
        ("Put sterile gel",                USER_TASK,    "Doctor"),
        ("Position probe",                 USER_TASK,    "Doctor"),
        ("Position patient",               USER_TASK,    "Doctor"),

        ("Vein identification method?",    EXCLUSIVE_GW, "Doctor"),
        ("Anatomic identification",        USER_TASK,    "Doctor"),
        ("Doppler identification",         USER_TASK,    "Doctor"),
        ("Compression identification",     USER_TASK,    "Doctor"),
        ("Vein identified",                EXCLUSIVE_GW, "Doctor"),

        ("Anesthetize patient",            USER_TASK,    "Doctor"),
        ("Puncture vein",                  USER_TASK,    "Doctor"),
        ("Check blood return",             USER_TASK,    "Doctor"),
        ("Blood return correct?",          EXCLUSIVE_GW, "Doctor"),

        ("Drop probe and remove syringe",  USER_TASK,    "Doctor"),
        ("Install guidewire",              USER_TASK,    "Doctor"),
        ("Remove trocar",                  USER_TASK,    "Doctor"),

        ("Check wire axis?",               EXCLUSIVE_GW, "Doctor"),
        ("Check wire long axis",           USER_TASK,    "Doctor"),
        ("Check wire short axis",          USER_TASK,    "Doctor"),
        ("Wire checked",                   EXCLUSIVE_GW, "Doctor"),

        ("Wire in good position?",         EXCLUSIVE_GW, "Doctor"),
        ("Widen pathway",                  USER_TASK,    "Doctor"),
        ("Advance catheter",               USER_TASK,    "Doctor"),
        ("Remove guidewire",               USER_TASK,    "Doctor"),
        ("Verify flow and reflow",         USER_TASK,    "Doctor"),
        ("Check catheter position",        USER_TASK,    "Doctor"),

        ("End",                            END,          "Doctor"),
    ],

    "flows": [
        ("Start",                         "Prep steps",                    ""),

        ("Prep steps",                    "Prepare implements",            ""),
        ("Prep steps",                    "Wash hands",                    ""),
        ("Prep steps",                    "Put on sterile clothes",        ""),
        ("Prepare implements",            "Prep complete",                 ""),
        ("Wash hands",                    "Prep complete",                 ""),
        ("Put on sterile clothes",        "Prep complete",                 ""),

        ("Prep complete",                 "Clean puncture area",           ""),
        ("Clean puncture area",           "Drape puncture zone",           ""),
        ("Drape puncture zone",           "Configure ultrasound",          ""),
        ("Configure ultrasound",          "Put gel on probe",              ""),
        ("Put gel on probe",              "Cover probe",                   ""),
        ("Cover probe",                   "Put sterile gel",               ""),
        ("Put sterile gel",               "Position probe",                ""),
        ("Position probe",                "Position patient",              ""),
        ("Position patient",              "Vein identification method?",   ""),

        ("Vein identification method?",   "Anatomic identification",       "Anatomic"),
        ("Vein identification method?",   "Doppler identification",        "Doppler"),
        ("Vein identification method?",   "Compression identification",    "Compression"),
        ("Anatomic identification",       "Vein identified",               ""),
        ("Doppler identification",        "Vein identified",               ""),
        ("Compression identification",    "Vein identified",               ""),

        ("Vein identified",               "Anesthetize patient",           ""),
        ("Anesthetize patient",           "Puncture vein",                 ""),
        ("Puncture vein",                 "Check blood return",            ""),
        ("Check blood return",            "Blood return correct?",         ""),

        ("Blood return correct?",         "Puncture vein",                 "No"),
        ("Blood return correct?",         "Drop probe and remove syringe", "Yes"),

        ("Drop probe and remove syringe", "Install guidewire",             ""),
        ("Install guidewire",             "Remove trocar",                 ""),

        ("Remove trocar",                 "Check wire axis?",              ""),
        ("Check wire axis?",              "Check wire long axis",          "Long axis"),
        ("Check wire axis?",              "Check wire short axis",         "Short axis"),
        ("Check wire long axis",          "Wire checked",                  ""),
        ("Check wire short axis",         "Wire checked",                  ""),

        ("Wire checked",                  "Wire in good position?",        ""),
        ("Wire in good position?",        "Puncture vein",                 "No"),
        ("Wire in good position?",        "Widen pathway",                 "Yes"),

        ("Widen pathway",                 "Advance catheter",              ""),
        ("Advance catheter",              "Remove guidewire",              ""),
        ("Remove guidewire",              "Verify flow and reflow",         ""),
        ("Verify flow and reflow",        "Check catheter position",        ""),
        ("Check catheter position",       "End",                           ""),
    ],

    "layout": {
        "Start":                         0,

        "Prep steps":                    1,
        "Prepare implements":            2,
        "Wash hands":                    2,
        "Put on sterile clothes":        2,
        "Prep complete":                 3,

        "Clean puncture area":           4,
        "Drape puncture zone":           5,
        "Configure ultrasound":          6,
        "Put gel on probe":              7,
        "Cover probe":                   8,
        "Put sterile gel":               9,
        "Position probe":                10,
        "Position patient":              11,

        "Vein identification method?":   12,
        "Anatomic identification":       13,
        "Doppler identification":        13,
        "Compression identification":    13,
        "Vein identified":               14,

        "Anesthetize patient":           15,
        "Puncture vein":                 16,
        "Check blood return":            17,
        "Blood return correct?":         18,

        "Drop probe and remove syringe": 19,
        "Install guidewire":             20,
        "Remove trocar":                 21,

        "Check wire axis?":              22,
        "Check wire long axis":          23,
        "Check wire short axis":         23,
        "Wire checked":                  24,

        "Wire in good position?":        25,
        "Widen pathway":                 26,
        "Advance catheter":              27,
        "Remove guidewire":              28,
        "Verify flow and reflow":        29,
        "Check catheter position":       30,

        "End":                           31,
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
