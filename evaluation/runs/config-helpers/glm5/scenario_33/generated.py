#
# 3DPrintProcess.py
#
# Description: Instruct an artist to create a 3D model and print it on a 3D printer
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "3D Print Process",
    
    "lanes": ["Customer", "Artist", "Printer"],
    
    "elements": [
        # Initiation
        ("Start", START, "Customer"),
        ("Send sketches", USER_TASK, "Customer"),
        ("Create project", USER_TASK, "Artist"),
        
        # Satisfaction loop
        ("Satisfied?", EXCLUSIVE_GW, "Customer"),
        ("Tell changes", USER_TASK, "Customer"),
        
        # STL delivery
        ("Send STL", USER_TASK, "Artist"),
        
        # Color selection and stock check
        ("Choose color", USER_TASK, "Customer"),
        ("In stock?", EXCLUSIVE_GW, "Customer"),
        ("Check quantity", USER_TASK, "Customer"),
        ("Order color", USER_TASK, "Customer"),
        
        # Quantity check
        ("Under 100g?", EXCLUSIVE_GW, "Customer"),
        ("Add to shopping list", USER_TASK, "Customer"),
        
        # Merge point
        ("Have plastic", EXCLUSIVE_GW, "Customer"),
        
        # Parallel activities
        ("Fork", PARALLEL_GW, "Customer"),
        ("Heat up", SERVICE_TASK, "Printer"),
        ("Generate G-code", SERVICE_TASK, "Customer"),
        ("Join", PARALLEL_GW, "Customer"),
        
        # Printing
        ("Print model", SERVICE_TASK, "Printer"),
        ("End", END, "Printer"),
    ],
    
    "flows": [
        ("Start", "Send sketches", ""),
        ("Send sketches", "Create project", ""),
        ("Create project", "Satisfied?", ""),
        ("Satisfied?", "Tell changes", "No"),
        ("Tell changes", "Create project", ""),
        ("Satisfied?", "Send STL", "Yes"),
        ("Send STL", "Choose color", ""),
        ("Choose color", "In stock?", ""),
        ("In stock?", "Check quantity", "Yes"),
        ("In stock?", "Order color", "No"),
        ("Check quantity", "Under 100g?", ""),
        ("Under 100g?", "Add to shopping list", "Yes"),
        ("Under 100g?", "Have plastic", "No"),
        ("Add to shopping list", "Have plastic", ""),
        ("Order color", "Have plastic", ""),
        ("Have plastic", "Fork", ""),
        ("Fork", "Heat up", ""),
        ("Fork", "Generate G-code", ""),
        ("Heat up", "Join", ""),
        ("Generate G-code", "Join", ""),
        ("Join", "Print model", ""),
        ("Print model", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Send sketches": 1,
        "Create project": 2,
        "Satisfied?": 3,
        "Tell changes": 4,
        "Send STL": 4,
        "Choose color": 5,
        "In stock?": 6,
        "Check quantity": 7,
        "Order color": 7,
        "Under 100g?": 8,
        "Add to shopping list": 9,
        "Have plastic": 10,
        "Fork": 11,
        "Heat up": 12,
        "Generate G-code": 12,
        "Join": 13,
        "Print model": 14,
        "End": 15,
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
