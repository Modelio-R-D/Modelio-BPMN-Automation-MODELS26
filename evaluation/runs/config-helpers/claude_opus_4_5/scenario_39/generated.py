#
# DIYSmartphoneRepair.py
#
# Description: Process for repairing a broken smartphone screen using an online DIY tool
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DIYSmartphoneRepair",
    
    "lanes": ["User", "DIY Tool", "Friends", "Expert"],
    
    "elements": [
        # Start
        ("Start",                    START,        "User"),
        
        # Initial input
        ("Enter Model and Issue",    USER_TASK,    "User"),
        
        # Tool analysis
        ("Analyze Device",           SERVICE_TASK, "DIY Tool"),
        ("Generate Requirements",    SERVICE_TASK, "DIY Tool"),
        
        # User reviews lists
        ("Review Materials List",    USER_TASK,    "User"),
        ("Review Tools List",        USER_TASK,    "User"),
        ("Review Ordering Options",  USER_TASK,    "User"),
        
        # Check what user has
        ("Check Inventory",          USER_TASK,    "User"),
        ("Have Everything?",         EXCLUSIVE_GW, "User"),
        
        # Acquire missing items
        ("Contact Friends",          SEND_TASK,    "User"),
        ("Check Availability",       USER_TASK,    "Friends"),
        ("Can Borrow/Buy?",          EXCLUSIVE_GW, "User"),
        ("Get from Friends",         USER_TASK,    "User"),
        ("Buy Remaining Items",      USER_TASK,    "User"),
        ("Receive Items",            USER_TASK,    "User"),
        
        # Repair process
        ("Generate Instructions",    SERVICE_TASK, "DIY Tool"),
        ("Follow Repair Steps",      MANUAL_TASK,  "User"),
        
        # Outcome check
        ("Repair Successful?",       EXCLUSIVE_GW, "User"),
        
        # Success path
        ("Send Review",              USER_TASK,    "User"),
        ("Upload Video",             USER_TASK,    "User"),
        ("End Success",              END,          "User"),
        
        # Failure path
        ("Send to Expert",           SEND_TASK,    "User"),
        ("Repair by Expert",         SERVICE_TASK, "Expert"),
        ("End Expert",               END,          "Expert"),
    ],
    
    "flows": [
        # Start flow
        ("Start",                   "Enter Model and Issue",   ""),
        ("Enter Model and Issue",   "Analyze Device",          ""),
        
        # Tool generates lists
        ("Analyze Device",          "Generate Requirements",   ""),
        ("Generate Requirements",   "Review Materials List",   ""),
        ("Review Materials List",   "Review Tools List",       ""),
        ("Review Tools List",       "Review Ordering Options", ""),
        ("Review Ordering Options", "Check Inventory",         ""),
        
        # Inventory check
        ("Check Inventory",         "Have Everything?",        ""),
        ("Have Everything?",        "Generate Instructions",   "Yes"),
        ("Have Everything?",        "Contact Friends",         "No"),
        
        # Friends flow
        ("Contact Friends",         "Check Availability",      ""),
        ("Check Availability",      "Can Borrow/Buy?",         ""),
        ("Can Borrow/Buy?",         "Get from Friends",        "Yes"),
        ("Can Borrow/Buy?",         "Buy Remaining Items",     "No"),
        ("Get from Friends",        "Buy Remaining Items",     ""),
        ("Buy Remaining Items",     "Receive Items",           ""),
        ("Receive Items",           "Generate Instructions",   ""),
        
        # Repair flow
        ("Generate Instructions",   "Follow Repair Steps",     ""),
        ("Follow Repair Steps",     "Repair Successful?",      ""),
        
        # Success path
        ("Repair Successful?",      "Send Review",             "Yes"),
        ("Send Review",             "Upload Video",            ""),
        ("Upload Video",            "End Success",             ""),
        
        # Failure path
        ("Repair Successful?",      "Send to Expert",          "No"),
        ("Send to Expert",          "Repair by Expert",        ""),
        ("Repair by Expert",        "End Expert",              ""),
    ],
    
    "layout": {
        "Start":                   0,
        "Enter Model and Issue":   1,
        "Analyze Device":          2,
        "Generate Requirements":   3,
        "Review Materials List":   4,
        "Review Tools List":       5,
        "Review Ordering Options": 6,
        "Check Inventory":         7,
        "Have Everything?":        8,
        "Contact Friends":         9,
        "Check Availability":      10,
        "Can Borrow/Buy?":         11,
        "Get from Friends":        12,
        "Buy Remaining Items":     13,
        "Receive Items":           14,
        "Generate Instructions":   15,
        "Follow Repair Steps":     16,
        "Repair Successful?":      17,
        "Send Review":             18,
        "Send to Expert":          18,
        "Upload Video":            19,
        "Repair by Expert":        19,
        "End Success":             20,
        "End Expert":              20,
    },
    
    "data_objects": [
        ("Device Info",        "User",     1),
        ("Materials List",     "DIY Tool", 3),
        ("Tools List",         "DIY Tool", 3),
        ("Ordering Options",   "DIY Tool", 3),
        ("Repair Instructions","DIY Tool", 15),
    ],
    
    "data_associations": [
        ("Enter Model and Issue",  "Device Info"),
        ("Device Info",            "Analyze Device"),
        ("Generate Requirements",  "Materials List"),
        ("Generate Requirements",  "Tools List"),
        ("Generate Requirements",  "Ordering Options"),
        ("Materials List",         "Review Materials List"),
        ("Tools List",             "Review Tools List"),
        ("Ordering Options",       "Review Ordering Options"),
        ("Generate Instructions",  "Repair Instructions"),
        ("Repair Instructions",    "Follow Repair Steps"),
    ],
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
