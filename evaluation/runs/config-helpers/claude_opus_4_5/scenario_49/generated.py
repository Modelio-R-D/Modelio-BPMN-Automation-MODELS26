#
# ComputerRepairProcess.py
#
# Description: Customer brings defective computer, CRS evaluates repair costs,
#              customer decides to proceed or not. Repair involves parallel
#              hardware and software activities with testing loops.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComputerRepairProcess",
    
    "lanes": ["Customer", "CRS"],
    
    "elements": [
        # Customer lane
        ("Bring Computer",          START,        "Customer"),
        ("Receive Calculation",     USER_TASK,    "Customer"),
        ("Costs Acceptable?",       EXCLUSIVE_GW, "Customer"),
        ("Take Computer Home",      USER_TASK,    "Customer"),
        ("End Unrepaired",          END,          "Customer"),
        ("Receive Repaired PC",     USER_TASK,    "Customer"),
        ("End Repaired",            END,          "Customer"),
        
        # CRS lane
        ("Check Defect",            USER_TASK,    "CRS"),
        ("Calculate Repair Cost",   USER_TASK,    "CRS"),
        ("Start Parallel Repair",   PARALLEL_GW,  "CRS"),
        ("Check Repair Hardware",   USER_TASK,    "CRS"),
        ("Check Configure Software",USER_TASK,    "CRS"),
        ("Test Hardware",           USER_TASK,    "CRS"),
        ("Test Software",           USER_TASK,    "CRS"),
        ("Hardware OK?",            EXCLUSIVE_GW, "CRS"),
        ("Software OK?",            EXCLUSIVE_GW, "CRS"),
        ("Join Parallel",           PARALLEL_GW,  "CRS"),
        ("Hand Over Computer",      USER_TASK,    "CRS"),
    ],
    
    "flows": [
        # Initial flow
        ("Bring Computer",          "Check Defect",            ""),
        ("Check Defect",            "Calculate Repair Cost",   ""),
        ("Calculate Repair Cost",   "Receive Calculation",     ""),
        ("Receive Calculation",     "Costs Acceptable?",       ""),
        
        # Customer decision
        ("Costs Acceptable?",       "Take Computer Home",      "No"),
        ("Take Computer Home",      "End Unrepaired",          ""),
        ("Costs Acceptable?",       "Start Parallel Repair",   "Yes"),
        
        # Parallel split - hardware and software paths
        ("Start Parallel Repair",   "Check Repair Hardware",   ""),
        ("Start Parallel Repair",   "Check Configure Software",""),
        
        # Hardware path with loop
        ("Check Repair Hardware",   "Test Hardware",           ""),
        ("Test Hardware",           "Hardware OK?",            ""),
        ("Hardware OK?",            "Check Repair Hardware",   "Error"),
        ("Hardware OK?",            "Join Parallel",           "OK"),
        
        # Software path with loop
        ("Check Configure Software","Test Software",           ""),
        ("Test Software",           "Software OK?",            ""),
        ("Software OK?",            "Check Configure Software","Error"),
        ("Software OK?",            "Join Parallel",           "OK"),
        
        # Final handover
        ("Join Parallel",           "Hand Over Computer",      ""),
        ("Hand Over Computer",      "Receive Repaired PC",     ""),
        ("Receive Repaired PC",     "End Repaired",            ""),
    ],
    
    "layout": {
        # Customer lane
        "Bring Computer":           0,
        "Receive Calculation":      3,
        "Costs Acceptable?":        4,
        "Take Computer Home":       5,
        "End Unrepaired":           6,
        "Receive Repaired PC":      10,
        "End Repaired":             11,
        
        # CRS lane
        "Check Defect":             1,
        "Calculate Repair Cost":    2,
        "Start Parallel Repair":    5,
        "Check Repair Hardware":    6,
        "Check Configure Software": 6,      # Auto-stacked below hardware
        "Test Hardware":            7,
        "Test Software":            7,      # Auto-stacked below Test Hardware
        "Hardware OK?":             8,
        "Software OK?":             8,      # Auto-stacked below Hardware OK?
        "Join Parallel":            9,
        "Hand Over Computer":       10,
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
