#
# EnergyDrinkBottlingInspection.py
#
# Description: Inspection process for an energy drink bottling machine
#              with manual input, automatic data collection, and conditional questions
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BottlingMachineInspection",
    
    "lanes": ["Inspector", "Application", "Machine"],
    
    "elements": [
        # Start
        ("Start",                    START,        "Inspector"),
        
        # Machine identification
        ("Enter Machine Type",       USER_TASK,    "Inspector"),
        ("Enter Serial Number",      USER_TASK,    "Inspector"),
        ("Validate Machine ID",      SERVICE_TASK, "Application"),
        ("Machine Valid?",           EXCLUSIVE_GW, "Application"),
        ("Show Error",               SERVICE_TASK, "Application"),
        
        # Inspection loop
        ("Display Question",         SERVICE_TASK, "Application"),
        ("Question Type?",           EXCLUSIVE_GW, "Application"),
        
        # Manual input branch
        ("Input Value",              USER_TASK,    "Inspector"),
        ("Record Manual Value",      SERVICE_TASK, "Application"),
        
        # Automatic collection branch
        ("Request Machine Data",     SERVICE_TASK, "Application"),
        ("Collect Sensor Data",      SERVICE_TASK, "Machine"),
        ("Display Collected Value",  SERVICE_TASK, "Application"),
        
        # Merge and evaluate
        ("Merge Values",             EXCLUSIVE_GW, "Application"),
        ("Evaluate Result",          SERVICE_TASK, "Application"),
        ("Additional Questions?",    EXCLUSIVE_GW, "Application"),
        
        # More questions check
        ("More Questions?",          EXCLUSIVE_GW, "Application"),
        
        # Complete inspection
        ("Generate Report",          SERVICE_TASK, "Application"),
        ("Review Report",            USER_TASK,    "Inspector"),
        ("End",                      END,          "Inspector"),
    ],
    
    "flows": [
        # Initial flow
        ("Start",                   "Enter Machine Type",      ""),
        ("Enter Machine Type",      "Enter Serial Number",     ""),
        ("Enter Serial Number",     "Validate Machine ID",     ""),
        ("Validate Machine ID",     "Machine Valid?",          ""),
        ("Machine Valid?",          "Show Error",              "No"),
        ("Show Error",              "Enter Machine Type",      ""),
        ("Machine Valid?",          "Display Question",        "Yes"),
        
        # Question type branching
        ("Display Question",        "Question Type?",          ""),
        ("Question Type?",          "Input Value",             "Manual"),
        ("Question Type?",          "Request Machine Data",    "Auto"),
        
        # Manual input path
        ("Input Value",             "Record Manual Value",     ""),
        ("Record Manual Value",     "Merge Values",            ""),
        
        # Automatic collection path
        ("Request Machine Data",    "Collect Sensor Data",     ""),
        ("Collect Sensor Data",     "Display Collected Value", ""),
        ("Display Collected Value", "Merge Values",            ""),
        
        # Evaluation and conditional questions
        ("Merge Values",            "Evaluate Result",         ""),
        ("Evaluate Result",         "Additional Questions?",   ""),
        ("Additional Questions?",   "Display Question",        "Yes"),
        ("Additional Questions?",   "More Questions?",         "No"),
        
        # Loop or complete
        ("More Questions?",         "Display Question",        "Yes"),
        ("More Questions?",         "Generate Report",         "No"),
        
        # Completion
        ("Generate Report",         "Review Report",           ""),
        ("Review Report",           "End",                     ""),
    ],
    
    "data_objects": [
        ("Machine Info",       "Application", 3),
        ("Inspection Data",    "Application", 9),
        ("Inspection Report",  "Application", 11),
    ],
    
    "data_associations": [
        # Machine identification
        ("Validate Machine ID",     "Machine Info"),
        ("Machine Info",            "Display Question"),
        
        # Data collection
        ("Record Manual Value",     "Inspection Data"),
        ("Display Collected Value", "Inspection Data"),
        ("Inspection Data",         "Evaluate Result"),
        
        # Report generation
        ("Inspection Data",         "Generate Report"),
        ("Generate Report",         "Inspection Report"),
        ("Inspection Report",       "Review Report"),
    ],
    
    "layout": {
        # Column 0: Start
        "Start":                   0,
        
        # Columns 1-2: Machine identification
        "Enter Machine Type":      1,
        "Enter Serial Number":     2,
        
        # Column 3: Validation
        "Validate Machine ID":     3,
        
        # Column 4: Validation gateway and error
        "Machine Valid?":          4,
        "Show Error":              (4, 90),
        
        # Column 5: Display question
        "Display Question":        5,
        
        # Column 6: Question type gateway
        "Question Type?":          6,
        
        # Column 7: Input paths (stacked in different lanes)
        "Input Value":             7,
        "Request Machine Data":    7,
        
        # Column 8: Processing
        "Record Manual Value":     8,
        "Collect Sensor Data":     8,
        
        # Column 9: Display/Merge
        "Display Collected Value": 9,
        "Merge Values":            9,
        
        # Column 10: Evaluation
        "Evaluate Result":         10,
        "Additional Questions?":   (10, 90),
        
        # Column 11: More questions check
        "More Questions?":         11,
        
        # Columns 12-13: Completion
        "Generate Report":         12,
        "Review Report":           13,
        "End":                     14,
    },
    
    # Wider spacing for complex diagram
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
