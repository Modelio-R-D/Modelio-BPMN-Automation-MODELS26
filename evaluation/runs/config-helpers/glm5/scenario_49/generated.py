#
# ComputerRepairProcess.py
#
# Description: Computer repair process with parallel repair activities and error handling loop
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComputerRepair",
    
    "lanes": ["Customer", "CRS"],
    
    "elements": [
        # Customer lane
        ("Start", START, "Customer"),
        ("Bring Defective Computer", USER_TASK, "Customer"),
        ("Decide Acceptable?", EXCLUSIVE_GW, "Customer"),
        ("Take Computer Home", USER_TASK, "Customer"),
        ("End Rejected", END, "Customer"),
        ("End Success", END, "Customer"),
        
        # CRS lane
        ("Check Defect", SERVICE_TASK, "CRS"),
        ("Hand Out Cost Calculation", SERVICE_TASK, "CRS"),
        ("Parallel Fork", PARALLEL_GW, "CRS"),
        ("Hardware Repair", SERVICE_TASK, "CRS"),
        ("Test Hardware", SERVICE_TASK, "CRS"),
        ("Software Repair", SERVICE_TASK, "CRS"),
        ("Test Software", SERVICE_TASK, "CRS"),
        ("Parallel Join", PARALLEL_GW, "CRS"),
        ("Error Detected?", EXCLUSIVE_GW, "CRS"),
        ("Hand Back Repaired", SERVICE_TASK, "CRS"),
    ],
    
    "flows": [
        # Initial flow
        ("Start", "Bring Defective Computer", ""),
        ("Bring Defective Computer", "Check Defect", ""),
        ("Check Defect", "Hand Out Cost Calculation", ""),
        ("Hand Out Cost Calculation", "Decide Acceptable?", ""),
        
        # Rejected path
        ("Decide Acceptable?", "Take Computer Home", "No"),
        ("Take Computer Home", "End Rejected", ""),
        
        # Accepted path - parallel repair activities
        ("Decide Acceptable?", "Parallel Fork", "Yes"),
        ("Parallel Fork", "Hardware Repair", ""),
        ("Parallel Fork", "Software Repair", ""),
        ("Hardware Repair", "Test Hardware", ""),
        ("Software Repair", "Test Software", ""),
        ("Test Hardware", "Parallel Join", ""),
        ("Test Software", "Parallel Join", ""),
        
        # Error handling loop
        ("Parallel Join", "Error Detected?", ""),
        ("Error Detected?", "Parallel Fork", "Yes"),
        ("Error Detected?", "Hand Back Repaired", "No"),
        
        # Success completion
        ("Hand Back Repaired", "End Success", ""),
    ],
    
    "layout": {
        # Column 0-4: Initial process flow
        "Start": 0,
        "Bring Defective Computer": 1,
        "Check Defect": 2,
        "Hand Out Cost Calculation": 3,
        "Decide Acceptable?": 4,
        
        # Column 5-6: Decision branches (same column, different lanes)
        "Take Computer Home": 5,
        "End Rejected": 6,
        "Parallel Fork": 5,
        
        # Column 6-7: Parallel repair activities (auto-stacked in CRS lane)
        "Hardware Repair": 6,
        "Software Repair": 6,
        "Test Hardware": 7,
        "Test Software": 7,
        
        # Column 8-10: Error check and completion
        "Parallel Join": 8,
        "Error Detected?": 9,
        "Hand Back Repaired": 10,
        "End Success": 10,
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
