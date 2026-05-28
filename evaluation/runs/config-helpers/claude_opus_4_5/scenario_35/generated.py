#
# ChainsawProduction.py
#
# Description: Custom chainsaw manufacturing process with parallel parts ordering,
#              quality inspection, assembly, and customer approval workflow.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ChainsawProduction",
    
    "lanes": ["Customer", "Sales", "Procurement", "Production", "Quality"],
    
    "elements": [
        # Customer lane
        ("Start",                    START,        "Customer"),
        ("Specify Requirements",     USER_TASK,    "Customer"),
        ("Receive Updates",          RECEIVE_TASK, "Customer"),
        ("Evaluate Prototype",       USER_TASK,    "Customer"),
        ("Approved?",                EXCLUSIVE_GW, "Customer"),
        ("Receive Final Order",      RECEIVE_TASK, "Customer"),
        ("End",                      END,          "Customer"),
        
        # Sales lane
        ("Capture Order",            USER_TASK,    "Sales"),
        ("Send Update",              SEND_TASK,    "Sales"),
        ("Send Prototype",           SEND_TASK,    "Sales"),
        ("Deliver Remaining",        SEND_TASK,    "Sales"),
        
        # Procurement lane
        ("Split Orders",             PARALLEL_GW,  "Procurement"),
        ("Order Guide Bar",          SERVICE_TASK, "Procurement"),
        ("Order Chain",              SERVICE_TASK, "Procurement"),
        ("Order Power Unit",         SERVICE_TASK, "Procurement"),
        ("Order Handle Assembly",    SERVICE_TASK, "Procurement"),
        ("Order Safety Guard",       SERVICE_TASK, "Procurement"),
        ("Await All Parts",          PARALLEL_GW,  "Procurement"),
        
        # Production lane
        ("Assemble Chainsaw",        MANUAL_TASK,  "Production"),
        ("Produce Remaining",        MANUAL_TASK,  "Production"),
        
        # Quality lane
        ("Inspect Parts",            MANUAL_TASK,  "Quality"),
        ("Final Inspection",         MANUAL_TASK,  "Quality"),
    ],
    
    "data_objects": [
        ("Order Specification", "Sales",       1),
        ("Parts Inventory",    "Procurement",  7),
        ("Prototype",          "Production",   9),
    ],
    
    "data_associations": [
        ("Capture Order",       "Order Specification"),
        ("Order Specification", "Order Guide Bar"),
        ("Order Specification", "Order Chain"),
        ("Order Specification", "Order Power Unit"),
        ("Order Specification", "Order Handle Assembly"),
        ("Order Specification", "Order Safety Guard"),
        ("Inspect Parts",       "Parts Inventory"),
        ("Parts Inventory",     "Assemble Chainsaw"),
        ("Assemble Chainsaw",   "Prototype"),
        ("Prototype",           "Final Inspection"),
    ],
    
    "flows": [
        # Customer initiates
        ("Start",                  "Specify Requirements",  ""),
        ("Specify Requirements",   "Capture Order",         ""),
        
        # Sales captures and triggers procurement
        ("Capture Order",          "Split Orders",          ""),
        
        # Parallel ordering (5 properties)
        ("Split Orders",           "Order Guide Bar",       ""),
        ("Split Orders",           "Order Chain",           ""),
        ("Split Orders",           "Order Power Unit",      ""),
        ("Split Orders",           "Order Handle Assembly", ""),
        ("Split Orders",           "Order Safety Guard",    ""),
        
        # Synchronize parts arrival
        ("Order Guide Bar",        "Await All Parts",       ""),
        ("Order Chain",            "Await All Parts",       ""),
        ("Order Power Unit",       "Await All Parts",       ""),
        ("Order Handle Assembly",  "Await All Parts",       ""),
        ("Order Safety Guard",     "Await All Parts",       ""),
        
        # Quality inspection
        ("Await All Parts",        "Inspect Parts",         ""),
        
        # Production with updates
        ("Inspect Parts",          "Assemble Chainsaw",     ""),
        ("Assemble Chainsaw",      "Send Update",           ""),
        ("Send Update",            "Receive Updates",       ""),
        ("Receive Updates",        "Final Inspection",      ""),
        
        # Send prototype for approval
        ("Final Inspection",       "Send Prototype",        ""),
        ("Send Prototype",         "Evaluate Prototype",    ""),
        
        # Customer decision
        ("Evaluate Prototype",     "Approved?",             ""),
        ("Approved?",              "Produce Remaining",     "Yes"),
        ("Approved?",              "Capture Order",         "No - Revise"),
        
        # Complete remaining order
        ("Produce Remaining",      "Deliver Remaining",     ""),
        ("Deliver Remaining",      "Receive Final Order",   ""),
        ("Receive Final Order",    "End",                   ""),
    ],
    
    "layout": {
        # Customer lane
        "Start":                  0,
        "Specify Requirements":   1,
        "Receive Updates":        10,
        "Evaluate Prototype":     12,
        "Approved?":              13,
        "Receive Final Order":    16,
        "End":                    17,
        
        # Sales lane
        "Capture Order":          2,
        "Send Update":            10,
        "Send Prototype":         12,
        "Deliver Remaining":      16,
        
        # Procurement lane
        "Split Orders":           3,
        "Order Guide Bar":        4,
        "Order Chain":            5,
        "Order Power Unit":       4,      # Auto-stacked with Guide Bar
        "Order Handle Assembly":  5,      # Auto-stacked with Chain
        "Order Safety Guard":     4,      # Auto-stacked below Power Unit
        "Await All Parts":        6,
        
        # Production lane
        "Assemble Chainsaw":      9,
        "Produce Remaining":      15,
        
        # Quality lane
        "Inspect Parts":          7,
        "Final Inspection":       11,
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
