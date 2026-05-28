#
# OnlineShopPurchaseProcess.py
#
# Description: BPMN process for purchasing items from an online shop, including parallel item/payment setup,
#              reward selection, delivery, and exchange loop with re-delivery.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OnlineShopPurchase",

    "lanes": ["Customer", "Shop"],

    "elements": [
        ("Start",                     START,        "Customer"),
        ("Log In",                    USER_TASK,    "Customer"),

        ("Start Order (Parallel)",     PARALLEL_GW,  "Customer"),
        ("Select Items",              USER_TASK,    "Customer"),
        ("Set Payment Method",        USER_TASK,    "Customer"),

        ("Choose Reward",             EXCLUSIVE_GW, "Customer"),
        ("Reward Option A",           USER_TASK,    "Customer"),
        ("Reward Option B",           USER_TASK,    "Customer"),
        ("Reward Option C",           USER_TASK,    "Customer"),
        ("Reward Selected (Merge)",   EXCLUSIVE_GW, "Customer"),

        ("Payment Choice?",           EXCLUSIVE_GW, "Customer"),
        ("Pay Now",                   USER_TASK,    "Customer"),
        ("Installment Agreement",     USER_TASK,    "Customer"),
        ("Payment Completed (Merge)", EXCLUSIVE_GW, "Customer"),

        ("Continue (Parallel Join)",  PARALLEL_GW,  "Customer"),

        ("Deliver Items",             SERVICE_TASK, "Shop"),
        ("Return for Exchange?",      EXCLUSIVE_GW, "Shop"),
        ("Return Items",              USER_TASK,    "Customer"),
        ("Process Exchange",          SERVICE_TASK, "Shop"),
        ("End",                       END,          "Shop"),
    ],

    "flows": [
        ("Start",                 "Log In",                    ""),
        ("Log In",                "Start Order (Parallel)",     ""),

        # Parallel: item selection and payment setup
        ("Start Order (Parallel)", "Select Items",             ""),
        ("Start Order (Parallel)", "Set Payment Method",       ""),

        # Reward selection depends on selected items, independent of payment
        ("Select Items",          "Choose Reward",             ""),
        ("Choose Reward",         "Reward Option A",           "Option A"),
        ("Choose Reward",         "Reward Option B",           "Option B"),
        ("Choose Reward",         "Reward Option C",           "Option C"),
        ("Reward Option A",       "Reward Selected (Merge)",   ""),
        ("Reward Option B",       "Reward Selected (Merge)",   ""),
        ("Reward Option C",       "Reward Selected (Merge)",   ""),
        ("Reward Selected (Merge)","Continue (Parallel Join)", ""),

        # Payment: pay now or installment agreement
        ("Set Payment Method",    "Payment Choice?",           ""),
        ("Payment Choice?",       "Pay Now",                   "Pay now"),
        ("Payment Choice?",       "Installment Agreement",     "Installments"),
        ("Pay Now",               "Payment Completed (Merge)", ""),
        ("Installment Agreement", "Payment Completed (Merge)", ""),
        ("Payment Completed (Merge)","Continue (Parallel Join)",""),

        # After both reward selection and payment completion
        ("Continue (Parallel Join)","Deliver Items",            ""),

        # Return/exchange loop: each return triggers a new delivery
        ("Deliver Items",         "Return for Exchange?",      ""),
        ("Return for Exchange?",  "End",                       "No"),
        ("Return for Exchange?",  "Return Items",              "Yes"),
        ("Return Items",          "Process Exchange",          ""),
        ("Process Exchange",      "Deliver Items",             ""),
    ],

    "layout": {
        "Start":                      0,
        "Log In":                     1,

        "Start Order (Parallel)":      2,

        # Parallel branch starts
        "Select Items":               3,
        "Set Payment Method":         3,

        # Reward branch
        "Choose Reward":              4,
        "Reward Option A":            5,
        "Reward Option B":            5,   # auto-stacked
        "Reward Option C":            5,   # auto-stacked
        "Reward Selected (Merge)":    6,

        # Payment branch
        "Payment Choice?":            4,
        "Pay Now":                    5,   # auto-stacked (same lane/column as Installment Agreement)
        "Installment Agreement":      5,
        "Payment Completed (Merge)":  6,

        # Join + delivery + return loop
        "Continue (Parallel Join)":   7,
        "Deliver Items":              8,
        "Return for Exchange?":       9,
        "Return Items":               10,
        "Process Exchange":           11,
        "End":                        10,
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
