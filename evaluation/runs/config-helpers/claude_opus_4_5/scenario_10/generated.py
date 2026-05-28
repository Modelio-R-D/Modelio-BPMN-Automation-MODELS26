#
# IT_Solution_Request_Process.py
#
# Description: IT solution request workflow from submission through deployment and support
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "IT_Solution_Request_Process",
    
    "lanes": ["Requester", "IT Department"],
    
    "elements": [
        # Requester lane
        ("Submit Request",          USER_TASK,    "Requester"),
        ("Start",                   START,        "Requester"),
        ("Receive Solution",        USER_TASK,    "Requester"),
        ("Attend Training",         USER_TASK,    "Requester"),
        ("End",                     END,          "Requester"),
        
        # IT Department lane
        ("Assess Request",          USER_TASK,    "IT Department"),
        ("Approved?",               EXCLUSIVE_GW, "IT Department"),
        ("Notify Rejection",        SEND_TASK,    "IT Department"),
        ("Procure Tools",           SERVICE_TASK, "IT Department"),
        ("Install Solution",        SERVICE_TASK, "IT Department"),
        ("Test Solution",           USER_TASK,    "IT Department"),
        ("Testing OK?",             EXCLUSIVE_GW, "IT Department"),
        ("Fix Issues",              USER_TASK,    "IT Department"),
        ("Deploy to Requester",     SERVICE_TASK, "IT Department"),
        ("Provide Training",        USER_TASK,    "IT Department"),
        ("Provide Support",         USER_TASK,    "IT Department"),
    ],
    
    "flows": [
        # Main flow
        ("Start",               "Submit Request",      ""),
        ("Submit Request",      "Assess Request",      ""),
        ("Assess Request",      "Approved?",           ""),
        
        # Approval decision
        ("Approved?",           "Procure Tools",       "Yes"),
        ("Approved?",           "Notify Rejection",    "No"),
        ("Notify Rejection",    "End",                 ""),
        
        # Procurement and installation
        ("Procure Tools",       "Install Solution",    ""),
        ("Install Solution",    "Test Solution",       ""),
        ("Test Solution",       "Testing OK?",         ""),
        
        # Testing decision
        ("Testing OK?",         "Deploy to Requester", "Yes"),
        ("Testing OK?",         "Fix Issues",          "No"),
        ("Fix Issues",          "Test Solution",       ""),
        
        # Deployment and support
        ("Deploy to Requester", "Receive Solution",    ""),
        ("Receive Solution",    "Provide Training",    ""),
        ("Provide Training",    "Attend Training",     ""),
        ("Attend Training",     "Provide Support",     ""),
        ("Provide Support",     "End",                 ""),
    ],
    
    "data_objects": [
        ("Request Form",        "Requester",      1),
        ("Assessment Report",   "IT Department",  2),
        ("Training Materials",  "IT Department",  9),
    ],
    
    "data_associations": [
        ("Submit Request",      "Request Form"),
        ("Request Form",        "Assess Request"),
        ("Assess Request",      "Assessment Report"),
        ("Provide Training",    "Training Materials"),
        ("Training Materials",  "Attend Training"),
    ],
    
    "layout": {
        # Requester lane
        "Start":               0,
        "Submit Request":      1,
        "Receive Solution":    8,
        "Attend Training":     9,
        "End":                 10,
        
        # IT Department lane
        "Assess Request":      2,
        "Approved?":           3,
        "Notify Rejection":    (4, 90),
        "Procure Tools":       4,
        "Install Solution":    5,
        "Test Solution":       6,
        "Testing OK?":         7,
        "Fix Issues":          (6, 90),
        "Deploy to Requester": 8,
        "Provide Training":    9,
        "Provide Support":     10,
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
