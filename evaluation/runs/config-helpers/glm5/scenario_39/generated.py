#
# DIYRepairSmartphone.py
#
# Description: DIY Repair of a Broken Smartphone Screen process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DIYRepairSmartphoneScreen",
    
    "lanes": ["User", "Online Tool", "Friend", "Expert"],
    
    "elements": [
        # User lane
        ("Start", START, "User"),
        ("Enter Model and Issue", USER_TASK, "User"),
        ("Check What You Have", USER_TASK, "User"),
        ("Contact Friends", USER_TASK, "User"),
        ("Borrow/Buy from Friends", USER_TASK, "User"),
        ("Buy Remaining Items", USER_TASK, "User"),
        ("Follow Instructions", MANUAL_TASK, "User"),
        ("Success?", EXCLUSIVE_GW, "User"),
        ("Share Success", USER_TASK, "User"),
        ("Send to Expert", USER_TASK, "User"),
        ("End Success", END, "User"),
        
        # Online Tool lane
        ("Generate Lists", SERVICE_TASK, "Online Tool"),
        ("Provide Instructions", SERVICE_TASK, "Online Tool"),
        
        # Friend lane
        ("Lend/Sell Items", USER_TASK, "Friend"),
        
        # Expert lane
        ("Repair Phone", SERVICE_TASK, "Expert"),
        ("End Expert", END, "Expert"),
    ],
    
    "flows": [
        ("Start", "Enter Model and Issue", ""),
        ("Enter Model and Issue", "Generate Lists", ""),
        ("Generate Lists", "Check What You Have", ""),
        ("Check What You Have", "Contact Friends", ""),
        ("Contact Friends", "Lend/Sell Items", ""),
        ("Lend/Sell Items", "Borrow/Buy from Friends", ""),
        ("Borrow/Buy from Friends", "Buy Remaining Items", ""),
        ("Buy Remaining Items", "Provide Instructions", ""),
        ("Provide Instructions", "Follow Instructions", ""),
        ("Follow Instructions", "Success?", ""),
        ("Success?", "Share Success", "Yes"),
        ("Success?", "Send to Expert", "No"),
        ("Share Success", "End Success", ""),
        ("Send to Expert", "Repair Phone", ""),
        ("Repair Phone", "End Expert", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Enter Model and Issue": 1,
        "Generate Lists": 2,
        "Check What You Have": 3,
        "Contact Friends": 4,
        "Lend/Sell Items": 5,
        "Borrow/Buy from Friends": 6,
        "Buy Remaining Items": 7,
        "Provide Instructions": 8,
        "Follow Instructions": 9,
        "Success?": 10,
        "Share Success": 11,
        "Send to Expert": 11,
        "End Success": 12,
        "Repair Phone": 12,
        "End Expert": 13,
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
