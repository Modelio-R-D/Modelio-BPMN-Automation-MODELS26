#
# CreditScoringProcess.py
#
# Description: Credit scoring process between bank frontend, banking system, and scoring agency
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CreditScoringProcess",
    
    "lanes": [
        "Sales Clerk Frontend",
        "Banking System", 
        "Scoring Agency"
    ],
    
    "elements": [
        # Sales Clerk Frontend
        ("Request Scoring",         USER_TASK,          "Sales Clerk Frontend"),
        ("View Result",             USER_TASK,          "Sales Clerk Frontend"),
        ("Check Later Notice",      USER_TASK,          "Sales Clerk Frontend"),
        
        # Banking System
        ("Start",                   MESSAGE_START,      "Banking System"),
        ("Send Scoring Request",    SEND_TASK,          "Banking System"),
        ("Wait for Response",       EVENT_BASED_GW,     "Banking System"),
        ("Receive Result",          MESSAGE_CATCH,      "Banking System"),
        ("Receive Delay Notice",    MESSAGE_CATCH,      "Banking System"),
        ("Display Result",          SEND_TASK,          "Banking System"),
        ("Notify Clerk of Delay",   SEND_TASK,          "Banking System"),
        ("Wait for Final Result",   MESSAGE_CATCH,      "Banking System"),
        ("Display Final Result",    SEND_TASK,          "Banking System"),
        ("End",                     END,                "Banking System"),
        
        # Scoring Agency
        ("Receive Request",         MESSAGE_CATCH,      "Scoring Agency"),
        ("Level 1 Scoring",         SERVICE_TASK,       "Scoring Agency"),
        ("Immediate Result?",       EXCLUSIVE_GW,       "Scoring Agency"),
        ("Send Immediate Result",   SEND_TASK,          "Scoring Agency"),
        ("Send Delay Notice",       SEND_TASK,          "Scoring Agency"),
        ("Level 2 Scoring",         SERVICE_TASK,       "Scoring Agency"),
        ("Send Final Result",       SEND_TASK,          "Scoring Agency"),
        ("Agency End",              END,                "Scoring Agency"),
    ],
    
    "flows": [
        # Sales Clerk Frontend flows
        ("Request Scoring",         "Start",                ""),
        ("Display Result",          "View Result",          ""),
        ("Notify Clerk of Delay",   "Check Later Notice",   ""),
        ("Display Final Result",    "View Result",          ""),
        
        # Banking System internal flows
        ("Start",                   "Send Scoring Request", ""),
        ("Send Scoring Request",    "Wait for Response",    ""),
        ("Wait for Response",       "Receive Result",       ""),
        ("Wait for Response",       "Receive Delay Notice", ""),
        ("Receive Result",          "Display Result",       ""),
        ("Display Result",          "End",                  ""),
        ("Receive Delay Notice",    "Notify Clerk of Delay",""),
        ("Notify Clerk of Delay",   "Wait for Final Result",""),
        ("Wait for Final Result",   "Display Final Result", ""),
        ("Display Final Result",    "End",                  ""),
        
        # Scoring Agency internal flows
        ("Receive Request",         "Level 1 Scoring",      ""),
        ("Level 1 Scoring",         "Immediate Result?",    ""),
        ("Immediate Result?",       "Send Immediate Result","Yes"),
        ("Immediate Result?",       "Send Delay Notice",    "No"),
        ("Send Immediate Result",   "Agency End",           ""),
        ("Send Delay Notice",       "Level 2 Scoring",      ""),
        ("Level 2 Scoring",         "Send Final Result",    ""),
        ("Send Final Result",       "Agency End",           ""),
        
        # Cross-lane message flows
        ("Send Scoring Request",    "Receive Request",      ""),
        ("Send Immediate Result",   "Receive Result",       ""),
        ("Send Delay Notice",       "Receive Delay Notice", ""),
        ("Send Final Result",       "Wait for Final Result",""),
    ],
    
    "layout": {
        # Sales Clerk Frontend (row 0)
        "Request Scoring":          0,
        "Check Later Notice":       6,
        "View Result":              8,
        
        # Banking System (row 1)
        "Start":                    0,
        "Send Scoring Request":     1,
        "Wait for Response":        3,
        "Receive Result":           4,      # Auto-stacked with Receive Delay Notice
        "Receive Delay Notice":     4,      # 90px below Receive Result
        "Display Result":           5,
        "Notify Clerk of Delay":    5,      # Auto-stacked with Display Result
        "Wait for Final Result":    7,
        "Display Final Result":     8,
        "End":                      9,
        
        # Scoring Agency (row 2)
        "Receive Request":          1,
        "Level 1 Scoring":          2,
        "Immediate Result?":        3,
        "Send Immediate Result":    4,      # Auto-stacked with Send Delay Notice
        "Send Delay Notice":        4,      # 90px below Send Immediate Result
        "Level 2 Scoring":          5,
        "Send Final Result":        7,
        "Agency End":               9,
    },
    
    # Wider spacing for complex diagram
    "SPACING": 130,
    "START_X": 60,
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
