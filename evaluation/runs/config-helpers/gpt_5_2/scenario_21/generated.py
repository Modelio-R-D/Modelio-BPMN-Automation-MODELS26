#
# GoodsShipping.py
#
# Description: Shipping process with large/small amount decision, offers for special shipping,
#              label + optional insurance for normal shipment, and parallel packaging.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "GoodsShipping",

    "lanes": [
        "Secretary",
        "Logistics Dept Head",
        "Warehouseman",
        "Logistics Companies",
    ],

    "elements": [
        ("Start",                         START,        "Secretary"),
        ("Clarify who ships",             USER_TASK,    "Secretary"),

        ("Parallel work",                 PARALLEL_GW,  "Secretary"),

        ("Large amount?",                 EXCLUSIVE_GW, "Secretary"),

        ("Invite 3 logistic companies",   SEND_TASK,    "Secretary"),
        ("Receive offers",                RECEIVE_TASK, "Secretary"),
        ("Select logistic company",       USER_TASK,    "Secretary"),

        ("Write package label",           USER_TASK,    "Secretary"),
        ("Insurance needed?",             EXCLUSIVE_GW, "Secretary"),
        ("Take parcel insurance",         USER_TASK,    "Logistics Dept Head"),
        ("Insurance done",                EXCLUSIVE_GW, "Secretary"),

        ("Shipping arranged",             EXCLUSIVE_GW, "Secretary"),

        ("Package goods",                 MANUAL_TASK,  "Warehouseman"),

        ("All ready?",                    PARALLEL_GW,  "Warehouseman"),
        ("Prepare goods for pickup",      MANUAL_TASK,  "Warehouseman"),

        ("Pickup by logistic company",    SERVICE_TASK, "Logistics Companies"),

        ("End",                           END,          "Secretary"),
    ],

    "flows": [
        ("Start",               "Clarify who ships",            ""),
        ("Clarify who ships",   "Parallel work",                ""),

        # Parallel split: (1) shipping arrangement, (2) packaging
        ("Parallel work",       "Large amount?",                ""),
        ("Parallel work",       "Package goods",                ""),

        # Large amount -> special shipping offers
        ("Large amount?",       "Invite 3 logistic companies",  "Large"),
        ("Invite 3 logistic companies", "Receive offers",        ""),
        ("Receive offers",      "Select logistic company",       ""),
        ("Select logistic company", "Shipping arranged",         ""),

        # Small amount -> normal post shipment
        ("Large amount?",       "Write package label",           "Small"),
        ("Write package label", "Insurance needed?",             ""),
        ("Insurance needed?",   "Take parcel insurance",         "Yes"),
        ("Insurance needed?",   "Insurance done",                "No"),
        ("Take parcel insurance", "Insurance done",              ""),
        ("Insurance done",      "Shipping arranged",             ""),

        # Join: shipping arranged + packaged goods
        ("Shipping arranged",   "All ready?",                    ""),
        ("Package goods",       "All ready?",                    ""),

        ("All ready?",          "Prepare goods for pickup",      ""),
        ("Prepare goods for pickup", "Pickup by logistic company",""),
        ("Pickup by logistic company", "End",                     ""),
    ],

    "layout": {
        "Start":                        0,
        "Clarify who ships":            1,
        "Parallel work":                2,

        "Large amount?":                3,
        "Package goods":                3,

        # Special shipping path
        "Invite 3 logistic companies":  4,
        "Receive offers":               5,
        "Select logistic company":      6,

        # Normal shipment path (auto-stacked where same lane+column)
        "Write package label":          4,
        "Insurance needed?":            5,
        "Take parcel insurance":        6,
        "Insurance done":               7,

        "Shipping arranged":            8,

        "All ready?":                   9,
        "Prepare goods for pickup":     10,
        "Pickup by logistic company":   11,
        "End":                          12,
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
