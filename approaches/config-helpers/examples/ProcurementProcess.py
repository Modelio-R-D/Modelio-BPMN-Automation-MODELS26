#
# ProcurementProcess.py
#
# Description: Complete procurement process from purchase request to delivery
#              Includes vendor selection, quotes comparison, approval hierarchy,
#              and goods receipt with quality inspection.
#
# Applicable on: Package
#
# Lanes:
#   - Requester: Initiates and tracks the purchase request
#   - Procurement: Handles vendor management, quotes, and PO creation
#   - Manager: First-level approval authority
#   - Finance: Budget approval for high-value purchases
#   - Warehouse: Goods receipt and quality inspection
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library (adjust path for your Modelio version)
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ProcurementProcess",
    
    # Lanes from top to bottom (organizational roles)
    "lanes": [
        "Requester",
        "Procurement",
        "Manager",
        "Finance",
        "Warehouse"
    ],
    
    # All process elements: (name, type, lane)
    "elements": [
        # === Requester Lane ===
        ("Start",                   START,        "Requester"),
        ("Submit Request",          USER_TASK,    "Requester"),
        ("Request Complete",        END,          "Requester"),
        
        # === Procurement Lane ===
        ("Review Request",          USER_TASK,    "Procurement"),
        ("Valid?",                  EXCLUSIVE_GW, "Procurement"),
        ("Request Quotes",          USER_TASK,    "Procurement"),
        ("Receive Quotes",          USER_TASK,    "Procurement"),
        ("Compare Quotes",          USER_TASK,    "Procurement"),
        ("Select Vendor",           USER_TASK,    "Procurement"),
        ("Check Value",             EXCLUSIVE_GW, "Procurement"),
        ("Create PO",               USER_TASK,    "Procurement"),
        ("Send PO to Vendor",       SERVICE_TASK, "Procurement"),
        ("Request Rejected",        END,          "Procurement"),
        
        # === Manager Lane ===
        ("Manager Review",          USER_TASK,    "Manager"),
        ("Manager Decision",        EXCLUSIVE_GW, "Manager"),
        ("Mgr Rejected",            END,          "Manager"),
        
        # === Finance Lane ===
        ("Finance Review",          USER_TASK,    "Finance"),
        ("Finance Decision",        EXCLUSIVE_GW, "Finance"),
        ("Budget Rejected",         END,          "Finance"),
        ("Approvals Join",          PARALLEL_GW,  "Finance"),
        
        # === Warehouse Lane ===
        ("Receive Goods",           MANUAL_TASK,  "Warehouse"),
        ("Inspect Quality",         MANUAL_TASK,  "Warehouse"),
        ("Quality OK?",             EXCLUSIVE_GW, "Warehouse"),
        ("Return to Vendor",        USER_TASK,    "Warehouse"),
        ("Confirm Receipt",         USER_TASK,    "Warehouse"),
        ("Returned",                END,          "Warehouse"),
    ],
    
    # Data Objects: (name, lane, column)
    "data_objects": [
        ("Purchase Request",  "Requester",   1),
        ("Vendor Quotes",     "Procurement", 4),
        ("Quote Analysis",    "Procurement", 5),
        ("Purchase Order",    "Procurement", 9),
        ("Delivery Note",     "Warehouse",  11),
        ("Inspection Report", "Warehouse",  12),
    ],
    
    # Data Associations: (source, target) - direction auto-detected
    "data_associations": [
        ("Submit Request",    "Purchase Request"),
        ("Purchase Request",  "Review Request"),
        ("Receive Quotes",    "Vendor Quotes"),
        ("Vendor Quotes",     "Compare Quotes"),
        ("Compare Quotes",    "Quote Analysis"),
        ("Quote Analysis",    "Select Vendor"),
        ("Create PO",         "Purchase Order"),
        ("Purchase Order",    "Send PO to Vendor"),
        ("Receive Goods",     "Delivery Note"),
        ("Delivery Note",     "Inspect Quality"),
        ("Inspect Quality",   "Inspection Report"),
        ("Inspection Report", "Confirm Receipt"),
    ],
    
    # Sequence Flows: (source, target, guard/label)
    "flows": [
        # Start to Submit
        ("Start",              "Submit Request",    ""),
        ("Submit Request",     "Review Request",    ""),
        
        # Procurement validates request
        ("Review Request",     "Valid?",            ""),
        ("Valid?",             "Request Rejected",  "Invalid"),
        ("Valid?",             "Request Quotes",    "Valid"),
        
        # Quotes handling
        ("Request Quotes",     "Receive Quotes",    ""),
        ("Receive Quotes",     "Compare Quotes",    ""),
        ("Compare Quotes",     "Select Vendor",     ""),
        ("Select Vendor",      "Check Value",       ""),
        
        # Value-based routing
        ("Check Value",        "Manager Review",    "Standard"),
        ("Check Value",        "Finance Review",    "High Value"),
        
        # Manager approval path
        ("Manager Review",     "Manager Decision",  ""),
        ("Manager Decision",   "Mgr Rejected",      "Rejected"),
        ("Manager Decision",   "Create PO",         "Approved"),
        
        # Finance approval path (high value items)
        ("Finance Review",     "Finance Decision",  ""),
        ("Finance Decision",   "Budget Rejected",   "Over Budget"),
        ("Finance Decision",   "Approvals Join",    "Within Budget"),
        
        # Join point for finance-approved items
        ("Approvals Join",     "Create PO",         ""),
        
        # PO creation and sending
        ("Create PO",          "Send PO to Vendor", ""),
        ("Send PO to Vendor",  "Receive Goods",     ""),
        
        # Warehouse handling
        ("Receive Goods",      "Inspect Quality",   ""),
        ("Inspect Quality",    "Quality OK?",       ""),
        ("Quality OK?",        "Return to Vendor",  "Defective"),
        ("Quality OK?",        "Confirm Receipt",   "Passed"),
        
        # End states
        ("Return to Vendor",   "Returned",          ""),
        ("Confirm Receipt",    "Request Complete",  ""),
    ],
    
    # Layout: element name -> column index (left to right)
    "layout": {
        # Column 0: Start
        "Start":              0,
        
        # Column 1: Initial request
        "Submit Request":     1,
        
        # Column 2: Review
        "Review Request":     2,
        
        # Column 3: Validation gateway
        "Valid?":             3,
        "Request Rejected":   3,
        
        # Column 4: Request quotes
        "Request Quotes":     4,
        
        # Column 5: Receive quotes
        "Receive Quotes":     5,
        
        # Column 6: Compare quotes
        "Compare Quotes":     6,
        
        # Column 7: Select vendor
        "Select Vendor":      7,
        
        # Column 8: Value check & approvals
        "Check Value":        8,
        "Manager Review":     8,
        "Finance Review":     8,
        
        # Column 9: Approval decisions
        "Manager Decision":   9,
        "Finance Decision":   9,
        "Mgr Rejected":       9,
        "Budget Rejected":    9,
        
        # Column 10: Create PO / Join
        "Approvals Join":    10,
        "Create PO":         10,
        
        # Column 11: Send PO
        "Send PO to Vendor": 11,
        
        # Column 12: Receive goods
        "Receive Goods":     12,
        
        # Column 13: Inspection
        "Inspect Quality":   13,
        
        # Column 14: Quality decision
        "Quality OK?":       14,
        
        # Column 15: Final actions
        "Return to Vendor":  15,
        "Confirm Receipt":   15,
        "Returned":          16,
        "Request Complete":  16,
    },
    
    # Layout configuration for wider diagram
    "SPACING": 130,
    "START_X": 60,
    "TASK_WIDTH": 110,
    "TASK_HEIGHT": 55,
}

# ============================================================================
# Entry Point
# ============================================================================
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
