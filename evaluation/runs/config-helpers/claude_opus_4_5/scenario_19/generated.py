#
# OnlineShopPurchase.py
#
# Description: Online shop purchase process with parallel item selection/payment,
#              reward selection, delivery, and return loop
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OnlineShopPurchase",
    
    "lanes": ["Customer", "Shop"],
    
    "elements": [
        # Start
        ("Start",                  START,        "Customer"),
        ("Log In",                 USER_TASK,    "Customer"),
        
        # Parallel split - do items and payment setup simultaneously
        ("Split Activities",       PARALLEL_GW,  "Customer"),
        
        # Upper branch - item selection and reward
        ("Select Items",           USER_TASK,    "Customer"),
        ("Choose Reward",          USER_TASK,    "Customer"),
        
        # Lower branch - payment method
        ("Set Payment Method",     USER_TASK,    "Customer"),
        
        # Payment choice
        ("Payment Type?",          EXCLUSIVE_GW, "Customer"),
        ("Pay Now",                USER_TASK,    "Customer"),
        ("Installment Agreement",  USER_TASK,    "Customer"),
        ("Payment Done",           EXCLUSIVE_GW, "Customer"),
        
        # Synchronize before delivery
        ("Sync for Delivery",      PARALLEL_GW,  "Customer"),
        
        # Delivery and return loop
        ("Deliver Items",          SERVICE_TASK, "Shop"),
        ("Return Items?",          EXCLUSIVE_GW, "Customer"),
        ("Return Items",           USER_TASK,    "Customer"),
        
        # End
        ("End",                    END,          "Customer"),
    ],
    
    "flows": [
        # Initial flow
        ("Start",                 "Log In",                ""),
        ("Log In",                "Split Activities",      ""),
        
        # Parallel split
        ("Split Activities",      "Select Items",          ""),
        ("Split Activities",      "Set Payment Method",    ""),
        
        # Upper branch - items then reward
        ("Select Items",          "Choose Reward",         ""),
        ("Choose Reward",         "Sync for Delivery",     ""),
        
        # Lower branch - payment method then choice
        ("Set Payment Method",    "Payment Type?",         ""),
        ("Payment Type?",         "Pay Now",               "Full Payment"),
        ("Payment Type?",         "Installment Agreement", "Installment"),
        ("Pay Now",               "Payment Done",          ""),
        ("Installment Agreement", "Payment Done",          ""),
        ("Payment Done",          "Sync for Delivery",     ""),
        
        # Synchronize and deliver
        ("Sync for Delivery",     "Deliver Items",         ""),
        
        # Return decision
        ("Deliver Items",         "Return Items?",         ""),
        ("Return Items?",         "End",                   "Keep"),
        ("Return Items?",         "Return Items",          "Exchange"),
        ("Return Items",          "Deliver Items",         ""),
    ],
    
    "layout": {
        "Start":                  0,
        "Log In":                 1,
        "Split Activities":       2,
        
        # Upper branch (items + reward)
        "Select Items":           3,
        "Choose Reward":          4,
        
        # Lower branch (payment) - auto-stacked in same columns
        "Set Payment Method":     3,
        "Payment Type?":          4,
        "Pay Now":                5,
        "Installment Agreement":  5,
        "Payment Done":           6,
        
        # Sync and delivery
        "Sync for Delivery":      7,
        "Deliver Items":          8,
        
        # Return loop
        "Return Items?":          9,
        "Return Items":           (10, 0),
        "End":                    (10, 90),
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
