#
# Chainsaw.py
#
# Description: Custom chainsaw production on demand with parallel parts ordering, inspection, assembly, updates, prototype approval, and remaining production.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Chainsaw",

    "lanes": ["Customer", "Chainsaw Maker"],

    "elements": [
        ("Start",                            START,         "Customer"),
        ("Provide chainsaw specs",           USER_TASK,     "Customer"),

        ("Review specs and quote",           USER_TASK,     "Chainsaw Maker"),
        ("Confirm order",                    USER_TASK,     "Chainsaw Maker"),
        ("Send update: ordering started",    SEND_TASK,     "Chainsaw Maker"),

        ("Order parts in parallel",          PARALLEL_GW,   "Chainsaw Maker"),

        ("Order guide bar (Schwertlaenge)",  SERVICE_TASK,  "Chainsaw Maker"),
        ("Order chain (width)",              SERVICE_TASK,  "Chainsaw Maker"),
        ("Order power unit (electric/motor)",SERVICE_TASK,  "Chainsaw Maker"),
        ("Order handle and housing",         SERVICE_TASK,  "Chainsaw Maker"),
        ("Order safety parts",               SERVICE_TASK,  "Chainsaw Maker"),

        ("Receive guide bar",                RECEIVE_TASK,  "Chainsaw Maker"),
        ("Receive chain",                    RECEIVE_TASK,  "Chainsaw Maker"),
        ("Receive power unit",               RECEIVE_TASK,  "Chainsaw Maker"),
        ("Receive handle and housing",       RECEIVE_TASK,  "Chainsaw Maker"),
        ("Receive safety parts",             RECEIVE_TASK,  "Chainsaw Maker"),

        ("All parts arrived",                PARALLEL_GW,   "Chainsaw Maker"),

        ("Send update: parts arrived",       SEND_TASK,     "Chainsaw Maker"),
        ("Manual inspect parts",             MANUAL_TASK,   "Chainsaw Maker"),
        ("Send update: parts inspected",     SEND_TASK,     "Chainsaw Maker"),
        ("Assemble first chainsaw",          MANUAL_TASK,   "Chainsaw Maker"),
        ("Send update: prototype built",     SEND_TASK,     "Chainsaw Maker"),
        ("Ship first chainsaw",              SEND_TASK,     "Chainsaw Maker"),

        ("Customer test first chainsaw",     USER_TASK,     "Customer"),
        ("Customer likes it?",               EXCLUSIVE_GW,  "Customer"),

        ("Produce remaining chainsaws",      MANUAL_TASK,   "Chainsaw Maker"),
        ("Send update: remaining production",SEND_TASK,     "Chainsaw Maker"),
        ("Ship remaining chainsaws",         SEND_TASK,     "Chainsaw Maker"),

        ("Request changes",                  USER_TASK,     "Customer"),
        ("Adjust design",                    USER_TASK,     "Chainsaw Maker"),

        ("End",                              END,           "Chainsaw Maker"),
    ],

    "data_objects": [
        ("Customer specs (bar length, chain width, power type, handle, safety)", "Customer",       1),
        ("Prototype saw",                                                     "Chainsaw Maker", 12),
        ("Change request",                                                   "Customer",       17),
    ],

    "data_associations": [
        ("Provide chainsaw specs", "Customer specs (bar length, chain width, power type, handle, safety)"),
        ("Customer specs (bar length, chain width, power type, handle, safety)", "Review specs and quote"),

        ("Assemble first chainsaw", "Prototype saw"),
        ("Prototype saw",           "Ship first chainsaw"),

        ("Request changes", "Change request"),
        ("Change request",  "Adjust design"),
    ],

    "flows": [
        ("Start",                         "Provide chainsaw specs",            ""),
        ("Provide chainsaw specs",        "Review specs and quote",            ""),
        ("Review specs and quote",        "Confirm order",                     ""),
        ("Confirm order",                 "Send update: ordering started",     ""),
        ("Send update: ordering started", "Order parts in parallel",           ""),

        ("Order parts in parallel",       "Order guide bar (Schwertlaenge)",   ""),
        ("Order parts in parallel",       "Order chain (width)",               ""),
        ("Order parts in parallel",       "Order power unit (electric/motor)", ""),
        ("Order parts in parallel",       "Order handle and housing",          ""),
        ("Order parts in parallel",       "Order safety parts",                ""),

        ("Order guide bar (Schwertlaenge)","Receive guide bar",                ""),
        ("Order chain (width)",           "Receive chain",                     ""),
        ("Order power unit (electric/motor)","Receive power unit",             ""),
        ("Order handle and housing",      "Receive handle and housing",        ""),
        ("Order safety parts",            "Receive safety parts",              ""),

        ("Receive guide bar",             "All parts arrived",                 ""),
        ("Receive chain",                 "All parts arrived",                 ""),
        ("Receive power unit",            "All parts arrived",                 ""),
        ("Receive handle and housing",    "All parts arrived",                 ""),
        ("Receive safety parts",          "All parts arrived",                 ""),

        ("All parts arrived",             "Send update: parts arrived",        ""),
        ("Send update: parts arrived",    "Manual inspect parts",              ""),
        ("Manual inspect parts",          "Send update: parts inspected",      ""),
        ("Send update: parts inspected",  "Assemble first chainsaw",           ""),
        ("Assemble first chainsaw",       "Send update: prototype built",      ""),
        ("Send update: prototype built",  "Ship first chainsaw",               ""),

        ("Ship first chainsaw",           "Customer test first chainsaw",      ""),
        ("Customer test first chainsaw",  "Customer likes it?",                ""),

        ("Customer likes it?",            "Produce remaining chainsaws",       "Yes"),
        ("Produce remaining chainsaws",   "Send update: remaining production", ""),
        ("Send update: remaining production","Ship remaining chainsaws",       ""),
        ("Ship remaining chainsaws",      "End",                               ""),

        ("Customer likes it?",            "Request changes",                   "No"),
        ("Request changes",               "Adjust design",                     ""),
        ("Adjust design",                 "Assemble first chainsaw",           "Rework"),
    ],

    "layout": {
        "Start":                         0,
        "Provide chainsaw specs":        1,

        "Review specs and quote":        2,
        "Confirm order":                 3,
        "Send update: ordering started": 4,

        "Order parts in parallel":       5,

        # Parallel ordering branches (auto-stacked)
        "Order guide bar (Schwertlaenge)":   6,
        "Order chain (width)":               6,
        "Order power unit (electric/motor)": 6,
        "Order handle and housing":          6,
        "Order safety parts":                6,

        # Deliveries (auto-stacked)
        "Receive guide bar":             7,
        "Receive chain":                 7,
        "Receive power unit":            7,
        "Receive handle and housing":    7,
        "Receive safety parts":          7,

        "All parts arrived":             8,
        "Send update: parts arrived":    9,
        "Manual inspect parts":          10,
        "Send update: parts inspected":  11,
        "Assemble first chainsaw":       12,
        "Send update: prototype built":  13,
        "Ship first chainsaw":           14,

        "Customer test first chainsaw":  15,
        "Customer likes it?":            16,

        "Produce remaining chainsaws":   17,
        "Send update: remaining production": 18,
        "Ship remaining chainsaws":      19,
        "End":                           20,

        "Request changes":               17,
        "Adjust design":                 18,
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
