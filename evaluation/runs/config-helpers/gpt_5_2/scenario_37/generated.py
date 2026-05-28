#
# Contract.py
#
# Description: Query multiple web shops, select cheapest offers, order parts (possibly split),
#              start building on first delivery batch, monitor stock and reorder by thresholds.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Contract",

    "lanes": ["Procurement", "Build", "Friends"],

    "elements": [
        ("Start",                               START,              "Procurement"),
        ("Define required parts",               USER_TASK,          "Procurement"),

        ("Query all web shops",                 PARALLEL_GW,        "Procurement"),
        ("Query Shop 1 (qty, price, lead time)", SERVICE_TASK,      "Procurement"),
        ("Query Shop 2 (qty, price, lead time)", SERVICE_TASK,      "Procurement"),
        ("Query Shop 3 (qty, price, lead time)", SERVICE_TASK,      "Procurement"),
        ("All quotes received",                 PARALLEL_GW,        "Procurement"),

        ("Select cheapest and split orders",    BUSINESS_RULE_TASK, "Procurement"),
        ("Place purchase orders per shop",      SEND_TASK,          "Procurement"),

        ("Wait for delivery batch (+/-2 days)", MESSAGE_CATCH,      "Build"),
        ("Update stock from delivered batch",   SCRIPT_TASK,        "Build"),

        ("First batch?",                        EXCLUSIVE_GW,       "Build"),
        ("Start building",                      USER_TASK,          "Build"),
        ("Continue building",                   USER_TASK,          "Build"),

        ("Build with available parts",          USER_TASK,          "Build"),
        ("Check stock levels",                  SCRIPT_TASK,        "Build"),

        ("Stock below 5?",                      EXCLUSIVE_GW,       "Build"),
        ("Stock below 3?",                      EXCLUSIVE_GW,       "Build"),
        ("Stock is zero?",                      EXCLUSIVE_GW,       "Build"),

        ("Reorder cheapest",                    SEND_TASK,          "Build"),
        ("Reorder fastest",                     SEND_TASK,          "Build"),
        ("Email friends complaining",           SEND_TASK,          "Friends"),

        ("All parts installed?",                EXCLUSIVE_GW,       "Build"),
        ("Assembly complete",                   USER_TASK,          "Build"),
        ("End",                                 END,                "Build"),
    ],

    "flows": [
        ("Start", "Define required parts", ""),
        ("Define required parts", "Query all web shops", ""),

        ("Query all web shops", "Query Shop 1 (qty, price, lead time)", ""),
        ("Query all web shops", "Query Shop 2 (qty, price, lead time)", ""),
        ("Query all web shops", "Query Shop 3 (qty, price, lead time)", ""),

        ("Query Shop 1 (qty, price, lead time)", "All quotes received", ""),
        ("Query Shop 2 (qty, price, lead time)", "All quotes received", ""),
        ("Query Shop 3 (qty, price, lead time)", "All quotes received", ""),

        ("All quotes received", "Select cheapest and split orders", ""),
        ("Select cheapest and split orders", "Place purchase orders per shop", ""),
        ("Place purchase orders per shop", "Wait for delivery batch (+/-2 days)", ""),

        ("Wait for delivery batch (+/-2 days)", "Update stock from delivered batch", ""),
        ("Update stock from delivered batch", "First batch?", ""),

        ("First batch?", "Start building", "Yes"),
        ("First batch?", "Continue building", "No"),

        ("Start building", "Build with available parts", ""),
        ("Continue building", "Build with available parts", ""),

        ("Build with available parts", "Check stock levels", ""),
        ("Check stock levels", "Stock below 5?", ""),

        ("Stock below 5?", "All parts installed?", "No (>=5)"),
        ("Stock below 5?", "Stock below 3?", "Yes (<5)"),

        ("Stock below 3?", "Reorder cheapest", "No (3-4)"),
        ("Stock below 3?", "Stock is zero?", "Yes (<3)"),

        ("Stock is zero?", "Reorder fastest", "No (1-2)"),
        ("Stock is zero?", "Email friends complaining", "Yes (=0)"),

        ("Reorder cheapest", "Wait for delivery batch (+/-2 days)", ""),
        ("Reorder fastest", "Wait for delivery batch (+/-2 days)", ""),
        ("Email friends complaining", "Wait for delivery batch (+/-2 days)", ""),

        ("All parts installed?", "Assembly complete", "Yes"),
        ("All parts installed?", "Wait for delivery batch (+/-2 days)", "No"),

        ("Assembly complete", "End", ""),
    ],

    "layout": {
        "Start":                                0,
        "Define required parts":                1,

        "Query all web shops":                  2,
        "Query Shop 1 (qty, price, lead time)": 3,
        "Query Shop 2 (qty, price, lead time)": 3,
        "Query Shop 3 (qty, price, lead time)": 3,
        "All quotes received":                  4,

        "Select cheapest and split orders":     5,
        "Place purchase orders per shop":       6,

        "Wait for delivery batch (+/-2 days)":  7,
        "Update stock from delivered batch":    8,

        "First batch?":                         9,
        "Start building":                       10,
        "Continue building":                    10,

        "Build with available parts":           11,
        "Check stock levels":                   12,

        "Stock below 5?":                       13,
        "Stock below 3?":                       14,
        "Stock is zero?":                       15,

        "Reorder cheapest":                     15,
        "Reorder fastest":                      16,
        "Email friends complaining":            16,

        "All parts installed?":                 17,
        "Assembly complete":                    18,
        "End":                                  19,
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
