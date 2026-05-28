CONFIG = {
    "name": "SalesOrderProcess",
    
    "lanes": ["Customer", "Sales"],
    
    "elements": [
        # Start
        ("Customer Inquiry", START, "Customer"),
        
        # Sales tasks
        ("Collect Information", USER_TASK, "Sales"),
        ("Address Concerns", USER_TASK, "Sales"),
        
        # First gateway
        ("Interested?", EXCLUSIVE_GW, "Sales"),
        
        # Selection and quote
        ("Guide Product Selection", USER_TASK, "Sales"),
        ("Provide Quote", USER_TASK, "Sales"),
        
        # Second gateway
        ("Quote Approved?", EXCLUSIVE_GW, "Customer"),
        
        # Order processing
        ("Place Order", USER_TASK, "Sales"),
        ("Record Order", SERVICE_TASK, "Sales"),
        ("Send Confirmation", SERVICE_TASK, "Sales"),
        
        # End events
        ("Order Confirmed", END, "Customer"),
        ("No Sale", END, "Sales"),
    ],
    
    "flows": [
        ("Customer Inquiry", "Collect Information", ""),
        ("Collect Information", "Address Concerns", ""),
        ("Address Concerns", "Interested?", ""),
        ("Interested?", "Guide Product Selection", "Yes"),
        ("Interested?", "No Sale", "No"),
        ("Guide Product Selection", "Provide Quote", ""),
        ("Provide Quote", "Quote Approved?", ""),
        ("Quote Approved?", "Place Order", "Yes"),
        ("Quote Approved?", "Guide Product Selection", "No"),  # Loop back
        ("Place Order", "Record Order", ""),
        ("Record Order", "Send Confirmation", ""),
        ("Send Confirmation", "Order Confirmed", ""),
    ],
    
    "layout": {
        "Customer Inquiry": 0,
        "Collect Information": 1,
        "Address Concerns": 2,
        "Interested?": 3,
        "Guide Product Selection": 4,
        "Provide Quote": 5,
        "Quote Approved?": 6,
        "Place Order": 7,
        "Record Order": 8,
        "Send Confirmation": 9,
        "Order Confirmed": 10,
        "No Sale": 4,  # Same column as Guide Product Selection - will auto-stack
    },
}


#
# SalesOrderProcess.py
#
# Description: Sales order process from customer inquiry to order confirmation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SalesOrderProcess",
    
    "lanes": ["Customer", "Sales"],
    
    "elements": [
        ("Customer Inquiry", START, "Customer"),
        ("Collect Information", USER_TASK, "Sales"),
        ("Address Concerns", USER_TASK, "Sales"),
        ("Interested?", EXCLUSIVE_GW, "Sales"),
        ("Guide Product Selection", USER_TASK, "Sales"),
        ("Provide Quote", USER_TASK, "Sales"),
        ("Quote Approved?", EXCLUSIVE_GW, "Customer"),
        ("Place Order", USER_TASK, "Sales"),
        ("Record Order", SERVICE_TASK, "Sales"),
        ("Send Confirmation", SERVICE_TASK, "Sales"),
        ("Order Confirmed", END, "Customer"),
        ("No Sale", END, "Sales"),
    ],
    
    "flows": [
        ("Customer Inquiry", "Collect Information", ""),
        ("Collect Information", "Address Concerns", ""),
        ("Address Concerns", "Interested?", ""),
        ("Interested?", "Guide Product Selection", "Yes"),
        ("Interested?", "No Sale", "No"),
        ("Guide Product Selection", "Provide Quote", ""),
        ("Provide Quote", "Quote Approved?", ""),
        ("Quote Approved?", "Place Order", "Yes"),
        ("Quote Approved?", "Guide Product Selection", "No"),
        ("Place Order", "Record Order", ""),
        ("Record Order", "Send Confirmation", ""),
        ("Send Confirmation", "Order Confirmed", ""),
    ],
    
    "layout": {
        "Customer Inquiry": 0,
        "Collect Information": 1,
        "Address Concerns": 2,
        "Interested?": 3,
        "Guide Product Selection": 4,
        "No Sale": 4,
        "Provide Quote": 5,
        "Quote Approved?": 6,
        "Place Order": 7,
        "Record Order": 8,
        "Send Confirmation": 9,
        "Order Confirmed": 10,
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


#
# SalesOrderProcess.py
#
# Description: Sales order process from customer inquiry to order confirmation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SalesOrderProcess",
    
    "lanes": ["Customer", "Sales"],
    
    "elements": [
        # Start event
        ("Customer Inquiry", START, "Customer"),
        
        # Information gathering
        ("Collect Information", USER_TASK, "Sales"),
        ("Address Concerns", USER_TASK, "Sales"),
        
        # First decision
        ("Interested?", EXCLUSIVE_GW, "Sales"),
        
        # Selection and quote
        ("Guide Product Selection", USER_TASK, "Sales"),
        ("Provide Quote", USER_TASK, "Sales"),
        
        # Second decision
        ("Quote Approved?", EXCLUSIVE_GW, "Customer"),
        
        # Order processing
        ("Place Order", USER_TASK, "Sales"),
        ("Record Order", SERVICE_TASK, "Sales"),
        ("Send Confirmation", SERVICE_TASK, "Sales"),
        
        # End events
        ("Order Confirmed", END, "Customer"),
        ("No Sale", END, "Sales"),
    ],
    
    "flows": [
        ("Customer Inquiry", "Collect Information", ""),
        ("Collect Information", "Address Concerns", ""),
        ("Address Concerns", "Interested?", ""),
        ("Interested?", "Guide Product Selection", "Yes"),
        ("Interested?", "No Sale", "No"),
        ("Guide Product Selection", "Provide Quote", ""),
        ("Provide Quote", "Quote Approved?", ""),
        ("Quote Approved?", "Place Order", "Yes"),
        ("Quote Approved?", "Guide Product Selection", "No"),
        ("Place Order", "Record Order", ""),
        ("Record Order", "Send Confirmation", ""),
        ("Send Confirmation", "Order Confirmed", ""),
    ],
    
    "layout": {
        "Customer Inquiry": 0,
        "Collect Information": 1,
        "Address Concerns": 2,
        "Interested?": 3,
        "Guide Product Selection": 4,
        "No Sale": 4,
        "Provide Quote": 5,
        "Quote Approved?": 6,
        "Place Order": 7,
        "Record Order": 8,
        "Send Confirmation": 9,
        "Order Confirmed": 10,
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
