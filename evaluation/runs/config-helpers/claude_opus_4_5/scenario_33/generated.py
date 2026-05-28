#
# 3DModelPrintProcess.py
#
# Description: Process for instructing an artist to create a 3D model and printing it
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "3DModelPrintProcess",
    
    "lanes": ["Customer", "Artist"],
    
    "elements": [
        # Customer lane - Initial phase
        ("Start",                    START,           "Customer"),
        ("Send Sketches",            SEND_TASK,       "Customer"),
        ("Review Design",            USER_TASK,       "Customer"),
        ("Satisfied?",               EXCLUSIVE_GW,    "Customer"),
        ("Request Changes",          SEND_TASK,       "Customer"),
        
        # Customer lane - Material phase
        ("Choose Plastic Color",     USER_TASK,       "Customer"),
        ("Color In Stock?",          EXCLUSIVE_GW,    "Customer"),
        ("Check Quantity",           USER_TASK,       "Customer"),
        ("Under 100g?",              EXCLUSIVE_GW,    "Customer"),
        ("Add to Shopping List",     USER_TASK,       "Customer"),
        ("Order Color",              SEND_TASK,       "Customer"),
        ("Merge Material",           EXCLUSIVE_GW,    "Customer"),
        
        # Customer lane - Printing phase
        ("Start Parallel",           PARALLEL_GW,     "Customer"),
        ("Heat Up Printer",          SERVICE_TASK,    "Customer"),
        ("Receive Status",           MESSAGE_CATCH,   "Customer"),
        ("Generate GCode",           SERVICE_TASK,    "Customer"),
        ("End Parallel",             PARALLEL_GW,     "Customer"),
        ("Print Model",              SERVICE_TASK,    "Customer"),
        ("End",                      END,             "Customer"),
        
        # Artist lane
        ("Receive Request",          RECEIVE_TASK,    "Artist"),
        ("Create 3D Model",          USER_TASK,       "Artist"),
        ("Send STL File",            SEND_TASK,       "Artist"),
        ("Receive Change Request",   RECEIVE_TASK,    "Artist"),
        ("Update Model",             USER_TASK,       "Artist"),
    ],
    
    "flows": [
        # Initial request flow
        ("Start",                  "Send Sketches",          ""),
        ("Send Sketches",          "Receive Request",        ""),
        ("Receive Request",        "Create 3D Model",        ""),
        ("Create 3D Model",        "Send STL File",          ""),
        ("Send STL File",          "Review Design",          ""),
        
        # Review loop
        ("Review Design",          "Satisfied?",             ""),
        ("Satisfied?",             "Request Changes",        "No"),
        ("Request Changes",        "Receive Change Request", ""),
        ("Receive Change Request", "Update Model",           ""),
        ("Update Model",           "Send STL File",          ""),
        ("Satisfied?",             "Choose Plastic Color",   "Yes"),
        
        # Material management
        ("Choose Plastic Color",   "Color In Stock?",        ""),
        ("Color In Stock?",        "Check Quantity",         "Yes"),
        ("Check Quantity",         "Under 100g?",            ""),
        ("Under 100g?",            "Add to Shopping List",   "Yes"),
        ("Add to Shopping List",   "Merge Material",         ""),
        ("Under 100g?",            "Merge Material",         "No"),
        ("Color In Stock?",        "Order Color",            "No"),
        ("Order Color",            "Merge Material",         ""),
        
        # Printing phase
        ("Merge Material",         "Start Parallel",         ""),
        ("Start Parallel",         "Heat Up Printer",        ""),
        ("Start Parallel",         "Generate GCode",         ""),
        ("Heat Up Printer",        "Receive Status",         ""),
        ("Receive Status",         "Heat Up Printer",        ""),
        ("Heat Up Printer",        "End Parallel",           ""),
        ("Generate GCode",         "End Parallel",           ""),
        ("End Parallel",           "Print Model",            ""),
        ("Print Model",            "End",                    ""),
    ],
    
    "data_objects": [
        ("Sketches",      "Customer", 0),
        ("STL File",      "Artist",   3),
        ("GCode File",    "Customer", 12),
    ],
    
    "data_associations": [
        ("Send Sketches",    "Sketches"),
        ("Sketches",         "Receive Request"),
        ("Create 3D Model",  "STL File"),
        ("STL File",         "Review Design"),
        ("Generate GCode",   "GCode File"),
        ("GCode File",       "Print Model"),
    ],
    
    "layout": {
        # Customer lane
        "Start":                  0,
        "Send Sketches":          1,
        "Review Design":          4,
        "Satisfied?":             5,
        "Request Changes":        6,
        "Choose Plastic Color":   7,
        "Color In Stock?":        8,
        "Check Quantity":         9,
        "Under 100g?":            10,
        "Add to Shopping List":   11,
        "Order Color":            9,
        "Merge Material":         12,
        "Start Parallel":         13,
        "Heat Up Printer":        14,
        "Receive Status":         15,
        "Generate GCode":         14,
        "End Parallel":           16,
        "Print Model":            17,
        "End":                    18,
        
        # Artist lane
        "Receive Request":        2,
        "Create 3D Model":        3,
        "Send STL File":          4,
        "Receive Change Request": 7,
        "Update Model":           8,
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
