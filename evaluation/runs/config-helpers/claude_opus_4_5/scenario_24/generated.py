#
# RestaurantOrderProcess.py
#
# Description: Guest ordering and meal pickup process at a restaurant
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RestaurantOrderProcess",
    
    "lanes": ["Guest", "Employee", "Chef"],
    
    "elements": [
        # Guest lane
        ("Feeling Hungry",           START,           "Guest"),
        ("Choose Dish",              USER_TASK,       "Guest"),
        ("Wait for Turn",            USER_TASK,       "Guest"),
        ("Place Order",              USER_TASK,       "Guest"),
        ("Pay",                      USER_TASK,       "Guest"),
        ("Receive Buzzer",           USER_TASK,       "Guest"),
        ("Wait for Buzzer",          INTERMEDIATE_CATCH, "Guest"),
        ("Pick Up Meal",             USER_TASK,       "Guest"),
        ("Eat Meal",                 USER_TASK,       "Guest"),
        ("End Guest",                END,             "Guest"),
        
        # Employee lane
        ("Receive Order",            USER_TASK,       "Employee"),
        ("Enter in POS",             USER_TASK,       "Employee"),
        ("Collect Payment",          USER_TASK,       "Employee"),
        ("Setup Buzzer",             USER_TASK,       "Employee"),
        ("Give Buzzer to Guest",     USER_TASK,       "Employee"),
        ("Inform Chef",              SEND_TASK,       "Employee"),
        ("Wait for Meal Ready",      MESSAGE_CATCH,   "Employee"),
        ("Trigger Buzzer",           MANUAL_TASK,     "Employee"),
        ("Guest Responded?",         EXCLUSIVE_GW,    "Employee"),
        ("Hand Over Meal",           USER_TASK,       "Employee"),
        ("Wait 5 Minutes",           TIMER_CATCH,     "Employee"),
        ("Call for Guest",           MANUAL_TASK,     "Employee"),
        ("End Employee",             END,             "Employee"),
        
        # Chef lane
        ("Receive Meal Order",       MESSAGE_CATCH,   "Chef"),
        ("Prepare Meal",             MANUAL_TASK,     "Chef"),
        ("Place in Service Hatch",   MANUAL_TASK,     "Chef"),
        ("Notify Meal Ready",        SEND_TASK,       "Chef"),
        ("End Chef",                 END,             "Chef"),
    ],
    
    "flows": [
        # Guest flow
        ("Feeling Hungry",       "Choose Dish",          ""),
        ("Choose Dish",          "Wait for Turn",        ""),
        ("Wait for Turn",        "Place Order",          ""),
        ("Place Order",          "Pay",                  ""),
        ("Pay",                  "Receive Buzzer",       ""),
        ("Receive Buzzer",       "Wait for Buzzer",      ""),
        ("Wait for Buzzer",      "Pick Up Meal",         ""),
        ("Pick Up Meal",         "Eat Meal",             ""),
        ("Eat Meal",             "End Guest",            ""),
        
        # Employee flow
        ("Receive Order",        "Enter in POS",         ""),
        ("Enter in POS",         "Collect Payment",      ""),
        ("Collect Payment",      "Setup Buzzer",         ""),
        ("Setup Buzzer",         "Give Buzzer to Guest", ""),
        ("Give Buzzer to Guest", "Inform Chef",          ""),
        ("Inform Chef",          "Wait for Meal Ready",  ""),
        ("Wait for Meal Ready",  "Trigger Buzzer",       ""),
        ("Trigger Buzzer",       "Guest Responded?",     ""),
        ("Guest Responded?",     "Hand Over Meal",       "Yes"),
        ("Guest Responded?",     "Wait 5 Minutes",       "No"),
        ("Wait 5 Minutes",       "Call for Guest",       ""),
        ("Call for Guest",       "Guest Responded?",     ""),
        ("Hand Over Meal",       "End Employee",         ""),
        
        # Chef flow
        ("Receive Meal Order",   "Prepare Meal",         ""),
        ("Prepare Meal",         "Place in Service Hatch", ""),
        ("Place in Service Hatch", "Notify Meal Ready",  ""),
        ("Notify Meal Ready",    "End Chef",             ""),
    ],
    
    "data_objects": [
        ("Order Info",   "Employee", 4),
        ("Buzzer",       "Employee", 5),
    ],
    
    "data_associations": [
        ("Enter in POS",         "Order Info"),
        ("Order Info",           "Inform Chef"),
        ("Setup Buzzer",         "Buzzer"),
        ("Buzzer",               "Give Buzzer to Guest"),
    ],
    
    "layout": {
        # Guest lane
        "Feeling Hungry":        0,
        "Choose Dish":           1,
        "Wait for Turn":         2,
        "Place Order":           3,
        "Pay":                   4,
        "Receive Buzzer":        5,
        "Wait for Buzzer":       6,
        "Pick Up Meal":          10,
        "Eat Meal":              11,
        "End Guest":             12,
        
        # Employee lane
        "Receive Order":         3,
        "Enter in POS":          4,
        "Collect Payment":       5,
        "Setup Buzzer":          6,
        "Give Buzzer to Guest":  7,
        "Inform Chef":           8,
        "Wait for Meal Ready":   9,
        "Trigger Buzzer":        10,
        "Guest Responded?":      11,
        "Hand Over Meal":        12,
        "Wait 5 Minutes":        12,
        "Call for Guest":        13,
        "End Employee":          14,
        
        # Chef lane
        "Receive Meal Order":    8,
        "Prepare Meal":          9,
        "Place in Service Hatch": 10,
        "Notify Meal Ready":     11,
        "End Chef":              12,
    },
    
    "SPACING": 130,
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
