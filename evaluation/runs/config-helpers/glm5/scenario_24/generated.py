#
# RestaurantProcess.py
#
# Description: Restaurant guest meal ordering and preparation process.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RestaurantProcess",
    
    "lanes": ["Guest", "Employee", "Chef"],
    
    "elements": [
        # Guest Lane
        ("Hungry", START, "Guest"),
        ("Choose Dish", USER_TASK, "Guest"),
        ("Wait for Turn", USER_TASK, "Guest"),
        ("Place Order", USER_TASK, "Guest"),
        ("Buzzer Rings", SIGNAL_CATCH, "Guest"),
        ("Go to Hatch", USER_TASK, "Guest"),
        ("Eat Meal", USER_TASK, "Guest"),
        ("End", END, "Guest"),
        
        # Employee Lane
        ("Enter Order in POS", USER_TASK, "Employee"),
        ("Collect Money", USER_TASK, "Employee"),
        ("Setup Buzzer", USER_TASK, "Employee"),
        ("Pass Buzzer", USER_TASK, "Employee"),
        ("Inform Chef", USER_TASK, "Employee"),
        ("Set off Buzzer", USER_TASK, "Employee"),
        ("Wait 5 min", TIMER_CATCH, "Employee"),
        ("Guest Arrived?", EXCLUSIVE_GW, "Employee"),
        ("Call Guest", USER_TASK, "Employee"),
        ("Hand over Meal", USER_TASK, "Employee"),
        
        # Chef Lane
        ("Prepare Meal", USER_TASK, "Chef"),
        ("Place Meal in Hatch", USER_TASK, "Chef"),
        ("Inform Employee", USER_TASK, "Chef"),
    ],
    
    "flows": [
        # Guest Flow
        ("Hungry", "Choose Dish", ""),
        ("Choose Dish", "Wait for Turn", ""),
        ("Wait for Turn", "Place Order", ""),
        
        # Transition to Employee
        ("Place Order", "Enter Order in POS", ""),
        
        # Employee Processing
        ("Enter Order in POS", "Collect Money", ""),
        ("Collect Money", "Setup Buzzer", ""),
        ("Setup Buzzer", "Pass Buzzer", ""),
        ("Pass Buzzer", "Inform Chef", ""),
        
        # Transition to Chef
        ("Inform Chef", "Prepare Meal", ""),
        
        # Chef Flow
        ("Prepare Meal", "Place Meal in Hatch", ""),
        ("Place Meal in Hatch", "Inform Employee", ""),
        
        # Transition back to Employee
        ("Inform Employee", "Set off Buzzer", ""),
        
        # Signaling and Synchronization
        ("Set off Buzzer", "Buzzer Rings", ""), # Signal to Guest
        ("Set off Buzzer", "Wait 5 min", ""),   # Employee starts wait
        
        # Guest reaction
        ("Buzzer Rings", "Go to Hatch", ""),
        ("Go to Hatch", "Hand over Meal", ""),  # Guest arrives at hatch
        
        # Employee Wait Loop & Handover
        ("Wait 5 min", "Guest Arrived?", ""),
        ("Guest Arrived?", "Call Guest", "No"),
        ("Call Guest", "Wait 5 min", ""),       # Loop back
        ("Guest Arrived?", "Hand over Meal", "Yes"),
        
        # Finalize
        ("Hand over Meal", "Eat Meal", ""),
        ("Eat Meal", "End", ""),
    ],
    
    "layout": {
        # Column 0-3: Guest actions
        "Hungry": 0,
        "Choose Dish": 1,
        "Wait for Turn": 2,
        "Place Order": 3,
        
        # Column 4-7: Employee actions
        "Enter Order in POS": 4,
        "Collect Money": 5,
        "Setup Buzzer": 6,
        "Pass Buzzer": 7,
        
        # Column 8-11: Chef actions
        "Inform Chef": 8,
        "Prepare Meal": 9,
        "Place Meal in Hatch": 10,
        "Inform Employee": 11,
        
        # Column 12-15: Synchronization & Completion
        "Set off Buzzer": 12,
        
        "Buzzer Rings": 13,
        "Wait 5 min": 13,
        
        "Go to Hatch": 14,
        "Guest Arrived?": 14,
        
        "Hand over Meal": 15,
        "Call Guest": (15, 90), # Stacked below Hand over Meal
        
        "Eat Meal": 16,
        "End": 17,
    },
    
    "data_objects": [
        ("Meal Range", "Guest", 1),
        ("Order", "Guest", 3),
        ("Meal", "Chef", 10),
    ],
    
    "data_associations": [
        ("Meal Range", "Choose Dish"),
        ("Place Order", "Order"),
        ("Order", "Enter Order in POS"),
        ("Place Meal in Hatch", "Meal"),
        ("Meal", "Hand over Meal"),
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
