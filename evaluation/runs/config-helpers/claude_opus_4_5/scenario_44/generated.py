#
# RoboticBurgerSeller.py
#
# Description: Robot burger seller process near University of Vienna
#              Handles orders for burgers with optional menu (drink + fries/wedges)
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RoboticBurgerSeller",
    
    "lanes": ["Customer", "Robot"],
    
    "elements": [
        # Customer lane
        ("Order Received",          MESSAGE_START,   "Customer"),
        
        # Robot lane - Menu decision
        ("Ask Menu or Burger",      USER_TASK,       "Robot"),
        ("Menu?",                   EXCLUSIVE_GW,    "Robot"),
        
        # Menu path - parallel preparation
        ("Start Menu Prep",         PARALLEL_GW,     "Robot"),
        ("Prepare Drink",           SERVICE_TASK,    "Robot"),
        ("Ask Fries or Wedges",     USER_TASK,       "Robot"),
        ("Fries or Wedges?",        EXCLUSIVE_GW,    "Robot"),
        ("Prepare Fries",           SERVICE_TASK,    "Robot"),
        ("Prepare Wedges",          SERVICE_TASK,    "Robot"),
        ("Side Done",               EXCLUSIVE_GW,    "Robot"),
        ("Menu Prep Complete",      PARALLEL_GW,     "Robot"),
        
        # Burger preparation (common path)
        ("Prepare Burger",          SERVICE_TASK,    "Robot"),
        ("Status Update Timer",     TIMER_CATCH,     "Robot"),
        ("Give Status Update",      USER_TASK,       "Robot"),
        ("Burger Ready?",           EXCLUSIVE_GW,    "Robot"),
        
        # Delivery
        ("Deliver via Conveyor",    SERVICE_TASK,    "Robot"),
        ("Order Complete",          END,             "Robot"),
    ],
    
    "flows": [
        # Start
        ("Order Received",       "Ask Menu or Burger",   ""),
        
        # Menu decision
        ("Ask Menu or Burger",   "Menu?",                ""),
        ("Menu?",                "Start Menu Prep",      "Yes"),
        ("Menu?",                "Prepare Burger",       "No - Just Burger"),
        
        # Parallel menu preparation
        ("Start Menu Prep",      "Prepare Drink",        ""),
        ("Start Menu Prep",      "Ask Fries or Wedges",  ""),
        
        # Side dish choice
        ("Ask Fries or Wedges",  "Fries or Wedges?",     ""),
        ("Fries or Wedges?",     "Prepare Fries",        "Fries"),
        ("Fries or Wedges?",     "Prepare Wedges",       "Wedges"),
        ("Prepare Fries",        "Side Done",            ""),
        ("Prepare Wedges",       "Side Done",            ""),
        
        # Sync after parallel
        ("Prepare Drink",        "Menu Prep Complete",   ""),
        ("Side Done",            "Menu Prep Complete",   ""),
        ("Menu Prep Complete",   "Prepare Burger",       ""),
        
        # Burger with status updates loop
        ("Prepare Burger",       "Status Update Timer",  ""),
        ("Status Update Timer",  "Give Status Update",   "30 sec"),
        ("Give Status Update",   "Burger Ready?",        ""),
        ("Burger Ready?",        "Status Update Timer",  "No - Continue"),
        ("Burger Ready?",        "Deliver via Conveyor", "Yes"),
        
        # Delivery
        ("Deliver via Conveyor", "Order Complete",       ""),
    ],
    
    "layout": {
        # Customer lane
        "Order Received":        0,
        
        # Robot lane - main flow
        "Ask Menu or Burger":    1,
        "Menu?":                 2,
        
        # Parallel split
        "Start Menu Prep":       3,
        "Prepare Drink":         4,
        "Ask Fries or Wedges":   4,      # Auto-stacked with Prepare Drink
        "Fries or Wedges?":      5,
        "Prepare Fries":         6,
        "Prepare Wedges":        6,      # Auto-stacked with Prepare Fries
        "Side Done":             7,
        "Menu Prep Complete":    8,
        
        # Burger preparation with loop
        "Prepare Burger":        9,
        "Status Update Timer":   10,
        "Give Status Update":    11,
        "Burger Ready?":         12,
        
        # Delivery
        "Deliver via Conveyor":  13,
        "Order Complete":        14,
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
