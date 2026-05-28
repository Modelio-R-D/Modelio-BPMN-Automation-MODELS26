#
# RoboticBurgerSeller.py
#
# Description: BPMN diagram for a robotic burger seller process near the University of Vienna.
#              The robot receives orders, prepares drinks and sides in parallel while asking
#              about preferences, prepares burgers with status updates every 30 seconds,
#              and delivers orders via conveyor belt.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RoboticBurgerSeller",
    
    "lanes": ["Robot"],
    
    "elements": [
        # Order intake
        ("Start",                START,         "Robot"),
        ("Receive Order",        SERVICE_TASK,  "Robot"),
        
        # Menu decision
        ("Menu or Burger?",      EXCLUSIVE_GW,  "Robot"),
        
        # Menu path - parallel preparation of drink and sides
        ("Prepare Menu",         PARALLEL_GW,   "Robot"),  # Split
        ("Prepare Drink",        SERVICE_TASK,  "Robot"),
        ("Fries or Wedges?",     EXCLUSIVE_GW,  "Robot"),
        ("Prepare Fries",        SERVICE_TASK,  "Robot"),
        ("Prepare Wedges",       SERVICE_TASK,  "Robot"),
        ("Sides Ready",          PARALLEL_GW,   "Robot"),  # Join
        
        # Burger preparation with status updates
        ("Prepare Burger",       SERVICE_TASK,  "Robot"),
        ("Burger Done?",         EXCLUSIVE_GW,  "Robot"),
        ("Send Status Update",   SERVICE_TASK,  "Robot"),
        ("Wait 30 sec",          TIMER_CATCH,   "Robot"),
        
        # Order delivery
        ("Deliver Order",        SERVICE_TASK,  "Robot"),
        ("End",                  END,           "Robot"),
    ],
    
    "flows": [
        # Order intake
        ("Start",              "Receive Order",    ""),
        ("Receive Order",      "Menu or Burger?",  ""),
        
        # Menu decision: Menu path vs Just Burger shortcut
        ("Menu or Burger?",    "Prepare Menu",     "Menu"),
        ("Menu or Burger?",    "Prepare Burger",   "Just Burger"),
        
        # Parallel preparation: drink and sides simultaneously
        ("Prepare Menu",       "Prepare Drink",    ""),
        ("Prepare Menu",       "Fries or Wedges?", ""),
        
        # Sides decision
        ("Fries or Wedges?",   "Prepare Fries",    "Fries"),
        ("Fries or Wedges?",   "Prepare Wedges",   "Wedges"),
        
        # Join parallel branches
        ("Prepare Drink",      "Sides Ready",      ""),
        ("Prepare Fries",      "Sides Ready",      ""),
        ("Prepare Wedges",     "Sides Ready",      ""),
        
        # Burger preparation
        ("Sides Ready",        "Prepare Burger",   ""),
        ("Prepare Burger",     "Burger Done?",     ""),
        
        # Status update loop (every 30 seconds)
        ("Burger Done?",       "Deliver Order",    "Yes"),
        ("Burger Done?",       "Send Status Update", "No"),
        ("Send Status Update", "Wait 30 sec",      ""),
        ("Wait 30 sec",        "Burger Done?",     ""),
        
        # Order delivery
        ("Deliver Order",      "End",              ""),
    ],
    
    "layout": {
        "Start":              0,
        "Receive Order":      1,
        "Menu or Burger?":    2,
        "Prepare Menu":       3,
        "Prepare Drink":      4,    # Auto-stacked with Fries or Wedges?
        "Fries or Wedges?":   4,    # 90px below Prepare Drink
        "Prepare Fries":      5,    # Auto-stacked with Prepare Wedges
        "Prepare Wedges":     5,    # 90px below Prepare Fries
        "Sides Ready":        6,
        "Prepare Burger":     7,
        "Burger Done?":       8,
        "Deliver Order":      9,    # Auto-stacked with Send Status Update
        "Send Status Update": 9,    # 90px below Deliver Order
        "Wait 30 sec":        10,
        "End":                11,
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
