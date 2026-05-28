#
# SalesInquiryToOrder.py
#
# Description: Sales process from customer inquiry through order confirmation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SalesInquiryToOrder",
    
    "lanes": ["Customer", "Sales"],
    
    "elements": [
        # Start
        ("Customer Inquiry",       MESSAGE_START,  "Customer"),
        
        # Information gathering
        ("Collect Information",    USER_TASK,      "Sales"),
        ("Address Questions",      USER_TASK,      "Sales"),
        
        # Interest check
        ("Interested?",            EXCLUSIVE_GW,   "Sales"),
        ("End Not Interested",     END,            "Sales"),
        
        # Product selection and quote
        ("Guide Product Selection", USER_TASK,     "Sales"),
        ("Provide Quote",          USER_TASK,      "Sales"),
        
        # Customer approval
        ("Review Quote",           USER_TASK,      "Customer"),
        ("Approved?",              EXCLUSIVE_GW,   "Customer"),
        
        # Order processing
        ("Place Order",            USER_TASK,      "Customer"),
        ("Record Order",           SERVICE_TASK,   "Sales"),
        ("Send Confirmation",      SEND_TASK,      "Sales"),
        ("Receive Confirmation",   RECEIVE_TASK,   "Customer"),
        
        # End
        ("End Order Confirmed",    END,            "Customer"),
    ],
    
    "flows": [
        # Main flow
        ("Customer Inquiry",        "Collect Information",    ""),
        ("Collect Information",     "Address Questions",      ""),
        ("Address Questions",       "Interested?",            ""),
        
        # Interest gateway
        ("Interested?",             "Guide Product Selection", "Yes"),
        ("Interested?",             "End Not Interested",      "No"),
        
        # Quote flow
        ("Guide Product Selection", "Provide Quote",          ""),
        ("Provide Quote",           "Review Quote",           ""),
        ("Review Quote",            "Approved?",              ""),
        
        # Approval gateway
        ("Approved?",               "Place Order",            "Yes"),
        ("Approved?",               "Provide Quote",          "No"),
        
        # Order completion
        ("Place Order",             "Record Order",           ""),
        ("Record Order",            "Send Confirmation",      ""),
        ("Send Confirmation",       "Receive Confirmation",   ""),
        ("Receive Confirmation",    "End Order Confirmed",    ""),
    ],
    
    "data_objects": [
        ("Customer Info",    "Sales",    1),
        ("Quote Document",   "Sales",    5),
        ("Order Record",     "Sales",    8),
    ],
    
    "data_associations": [
        # Customer info captured
        ("Collect Information",  "Customer Info"),
        ("Customer Info",        "Address Questions"),
        
        # Quote document
        ("Provide Quote",        "Quote Document"),
        ("Quote Document",       "Review Quote"),
        
        # Order record
        ("Record Order",         "Order Record"),
        ("Order Record",         "Send Confirmation"),
    ],
    
    "layout": {
        "Customer Inquiry":        0,
        "Collect Information":     1,
        "Address Questions":       2,
        "Interested?":             3,
        "End Not Interested":      4,
        "Guide Product Selection": 4,
        "Provide Quote":           5,
        "Review Quote":            6,
        "Approved?":               7,
        "Place Order":             8,
        "Record Order":            9,
        "Send Confirmation":       10,
        "Receive Confirmation":    11,
        "End Order Confirmed":     12,
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
