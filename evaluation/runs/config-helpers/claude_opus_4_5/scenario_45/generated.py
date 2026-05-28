#
# OrderingOnlineShop.py
#
# Description: Customer orders products in an online shop with login,
#              product selection loop, parallel payment/shipment, and address handling.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OrderingOnlineShop",
    
    "lanes": ["Customer", "E-Shop System", "Bank"],
    
    "elements": [
        # Login sequence
        ("Start",                    START,           "Customer"),
        ("Log In",                   USER_TASK,       "Customer"),
        ("Check Credentials",        SERVICE_TASK,    "E-Shop System"),
        ("Login OK?",                EXCLUSIVE_GW,    "E-Shop System"),
        ("Login Failed End",         END,             "Customer"),
        
        # Product selection loop
        ("Select Product",           USER_TASK,       "Customer"),
        ("Add to Cart",              USER_TASK,       "Customer"),
        ("Save Product",             SERVICE_TASK,    "E-Shop System"),
        ("All Selected?",            EXCLUSIVE_GW,    "Customer"),
        
        # Parallel split for payment and shipment
        ("Finish Order",             SERVICE_TASK,    "E-Shop System"),
        ("Parallel Split",           PARALLEL_GW,     "E-Shop System"),
        
        # Payment branch
        ("Enter Payment Data",       USER_TASK,       "Customer"),
        ("Confirm Payment",          SERVICE_TASK,    "Bank"),
        ("Wait Payment Confirm",     INTERMEDIATE_CATCH, "Customer"),
        
        # Address branch (runs in parallel)
        ("Enter Shipping Address",   USER_TASK,       "Customer"),
        ("Same as Billing?",         EXCLUSIVE_GW,    "Customer"),
        ("Enter Billing Address",    USER_TASK,       "Customer"),
        ("Address Done",             EXCLUSIVE_GW,    "Customer"),
        
        # Synchronization and completion
        ("Parallel Join",            PARALLEL_GW,     "E-Shop System"),
        ("Complete Order",           SERVICE_TASK,    "E-Shop System"),
        ("End",                      END,             "E-Shop System"),
    ],
    
    "flows": [
        # Login sequence
        ("Start",                  "Log In",                ""),
        ("Log In",                 "Check Credentials",     ""),
        ("Check Credentials",      "Login OK?",             ""),
        ("Login OK?",              "Login Failed End",      "No"),
        ("Login OK?",              "Select Product",        "Yes"),
        
        # Product selection loop
        ("Select Product",         "Add to Cart",           ""),
        ("Add to Cart",            "Save Product",          ""),
        ("Save Product",           "All Selected?",         ""),
        ("All Selected?",          "Select Product",        "No"),
        ("All Selected?",          "Finish Order",          "Yes"),
        
        # Parallel split
        ("Finish Order",           "Parallel Split",        ""),
        ("Parallel Split",         "Enter Payment Data",    ""),
        ("Parallel Split",         "Enter Shipping Address", ""),
        
        # Payment branch
        ("Enter Payment Data",     "Confirm Payment",       ""),
        ("Confirm Payment",        "Wait Payment Confirm",  ""),
        ("Wait Payment Confirm",   "Parallel Join",         ""),
        
        # Address branch
        ("Enter Shipping Address", "Same as Billing?",      ""),
        ("Same as Billing?",       "Enter Billing Address", "No"),
        ("Same as Billing?",       "Address Done",          "Yes"),
        ("Enter Billing Address",  "Address Done",          ""),
        ("Address Done",           "Parallel Join",         ""),
        
        # Final completion
        ("Parallel Join",          "Complete Order",        ""),
        ("Complete Order",         "End",                   ""),
    ],
    
    "layout": {
        # Login sequence (columns 0-3)
        "Start":                  0,
        "Log In":                 1,
        "Check Credentials":      2,
        "Login OK?":              3,
        "Login Failed End":       (3, 90),
        
        # Product selection loop (columns 4-7)
        "Select Product":         4,
        "Add to Cart":            5,
        "Save Product":           6,
        "All Selected?":          7,
        
        # Order finish and parallel split (columns 8-9)
        "Finish Order":           8,
        "Parallel Split":         9,
        
        # Payment branch (columns 10-12, upper path in Customer/Bank)
        "Enter Payment Data":     10,
        "Confirm Payment":        11,
        "Wait Payment Confirm":   12,
        
        # Address branch (columns 10-12, lower path - auto-stacked)
        "Enter Shipping Address": 10,
        "Same as Billing?":       11,
        "Enter Billing Address":  12,
        "Address Done":           13,
        
        # Synchronization and end (columns 13-15)
        "Parallel Join":          14,
        "Complete Order":         15,
        "End":                    16,
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
