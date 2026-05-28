#
# AnnualAuditProcess.py
#
# Description: BPMN diagram for multinational company's annual audit process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "AnnualAuditProcess",
    
    "lanes": [
        "Audit Coordinator",
        "Regional Office",
        "Compliance Team",
        "Central Audit Team",
        "Audit Director",
        "Executive Board"
    ],
    
    "elements": [
        # Column 0-2: Initiation
        ("Start", START, "Audit Coordinator"),
        ("Send Notification", SEND_TASK, "Audit Coordinator"),
        ("Initiate Parallel Work", PARALLEL_GW, "Audit Coordinator"),
        
        # Column 3-4: Parallel preparation
        ("Prepare Financial Statements", USER_TASK, "Regional Office"),
        ("Check Regulatory Updates", SERVICE_TASK, "Compliance Team"),
        ("Sync Preparation", PARALLEL_GW, "Regional Office"),
        
        # Column 5-7: Submission and review
        ("Submit Documents", USER_TASK, "Regional Office"),
        ("Review Submission", USER_TASK, "Central Audit Team"),
        ("Discrepancies?", EXCLUSIVE_GW, "Central Audit Team"),
        
        # Column 8-9: Main path - Risk assessment
        ("Conduct Risk Assessment", USER_TASK, "Central Audit Team"),
        ("Evaluate Risks", PARALLEL_GW, "Central Audit Team"),
        
        # Column 8-9: Exception path - Clarifications (offset)
        ("Request Clarifications", USER_TASK, "Central Audit Team"),
        ("Provide Clarifications", USER_TASK, "Regional Office"),
        
        # Column 10-11: Parallel risk evaluation
        ("Evaluate Financial Risks", SERVICE_TASK, "Central Audit Team"),
        ("Evaluate Operational Risks", SERVICE_TASK, "Central Audit Team"),
        ("Evaluate Compliance Risks", SERVICE_TASK, "Central Audit Team"),
        ("Sync Risk Evaluation", PARALLEL_GW, "Central Audit Team"),
        
        # Column 12-13: Risk decision
        ("High Risk?", EXCLUSIVE_GW, "Central Audit Team"),
        ("Compile Audit Report", USER_TASK, "Central Audit Team"),
        
        # Column 13-15: Exception path - Investigation (offset)
        ("Start Investigation", PARALLEL_GW, "Central Audit Team"),
        ("Data Analysis", SERVICE_TASK, "Central Audit Team"),
        ("Conduct Interviews", USER_TASK, "Central Audit Team"),
        ("Perform Site Visits", USER_TASK, "Central Audit Team"),
        ("Complete Investigation", PARALLEL_GW, "Central Audit Team"),
        
        # Column 14-15: Report review
        ("Review Report", USER_TASK, "Audit Director"),
        ("Approved?", EXCLUSIVE_GW, "Audit Director"),
        
        # Column 16: Exception path - Revisions (offset)
        ("Update Report", USER_TASK, "Central Audit Team"),
        
        # Column 16-18: Final distribution
        ("Distribute Report", SEND_TASK, "Executive Board"),
        ("Archive Report", SERVICE_TASK, "Executive Board"),
        ("End", END, "Executive Board"),
    ],
    
    "flows": [
        # Initiation
        ("Start", "Send Notification", ""),
        ("Send Notification", "Initiate Parallel Work", ""),
        
        # Parallel preparation fork
        ("Initiate Parallel Work", "Prepare Financial Statements", ""),
        ("Initiate Parallel Work", "Check Regulatory Updates", ""),
        
        # Parallel preparation join
        ("Prepare Financial Statements", "Sync Preparation", ""),
        ("Check Regulatory Updates", "Sync Preparation", ""),
        ("Sync Preparation", "Submit Documents", ""),
        
        # Review and discrepancies check
        ("Submit Documents", "Review Submission", ""),
        ("Review Submission", "Discrepancies?", ""),
        
        # Discrepancies branches
        ("Discrepancies?", "Conduct Risk Assessment", "No"),
        ("Discrepancies?", "Request Clarifications", "Yes"),
        ("Request Clarifications", "Provide Clarifications", ""),
        ("Provide Clarifications", "Review Submission", ""),
        
        # Risk assessment parallel fork
        ("Conduct Risk Assessment", "Evaluate Risks", ""),
        ("Evaluate Risks", "Evaluate Financial Risks", ""),
        ("Evaluate Risks", "Evaluate Operational Risks", ""),
        ("Evaluate Risks", "Evaluate Compliance Risks", ""),
        
        # Risk evaluation parallel join
        ("Evaluate Financial Risks", "Sync Risk Evaluation", ""),
        ("Evaluate Operational Risks", "Sync Risk Evaluation", ""),
        ("Evaluate Compliance Risks", "Sync Risk Evaluation", ""),
        ("Sync Risk Evaluation", "High Risk?", ""),
        
        # High risk decision branches
        ("High Risk?", "Compile Audit Report", "No"),
        ("High Risk?", "Start Investigation", "Yes"),
        
        # Investigation parallel fork
        ("Start Investigation", "Data Analysis", ""),
        ("Start Investigation", "Conduct Interviews", ""),
        ("Start Investigation", "Perform Site Visits", ""),
        
        # Investigation parallel join
        ("Data Analysis", "Complete Investigation", ""),
        ("Conduct Interviews", "Complete Investigation", ""),
        ("Perform Site Visits", "Complete Investigation", ""),
        ("Complete Investigation", "Compile Audit Report", ""),
        
        # Report compilation and review
        ("Compile Audit Report", "Review Report", ""),
        ("Review Report", "Approved?", ""),
        
        # Approval branches
        ("Approved?", "Distribute Report", "Yes"),
        ("Approved?", "Update Report", "No"),
        ("Update Report", "Review Report", ""),
        
        # Final distribution
        ("Distribute Report", "Archive Report", ""),
        ("Archive Report", "End", ""),
    ],
    
    "layout": {
        # Main flow (top path)
        "Start": 0,
        "Send Notification": 1,
        "Initiate Parallel Work": 2,
        "Prepare Financial Statements": 3,
        "Check Regulatory Updates": 3,
        "Sync Preparation": 4,
        "Submit Documents": 5,
        "Review Submission": 6,
        "Discrepancies?": 7,
        "Conduct Risk Assessment": 8,
        "Evaluate Risks": 9,
        "Evaluate Financial Risks": 10,
        "Evaluate Operational Risks": 10,
        "Evaluate Compliance Risks": 10,
        "Sync Risk Evaluation": 11,
        "High Risk?": 12,
        "Compile Audit Report": 13,
        "Review Report": 14,
        "Approved?": 15,
        "Distribute Report": 16,
        "Archive Report": 17,
        "End": 18,
        
        # Exception branches (offset down)
        "Request Clarifications": (8, 100),
        "Provide Clarifications": (9, 100),
        "Start Investigation": (13, 100),
        "Data Analysis": (14, 100),
        "Conduct Interviews": (14, 100),
        "Perform Site Visits": (14, 100),
        "Complete Investigation": (15, 100),
        "Update Report": (16, 100),
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
