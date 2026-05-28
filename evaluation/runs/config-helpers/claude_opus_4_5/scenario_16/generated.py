#
# AnnualAuditProcess.py
#
# Description: Multinational company annual audit process with parallel compliance checks,
#              risk assessment, investigation, and report approval workflow.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

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
        # Start
        ("Start Audit", START, "Audit Coordinator"),
        ("Send Notification", SEND_TASK, "Audit Coordinator"),
        
        # Parallel preparation
        ("Fork Preparation", PARALLEL_GW, "Regional Office"),
        ("Prepare Financial Statements", USER_TASK, "Regional Office"),
        ("Gather Documents", USER_TASK, "Regional Office"),
        ("Check Regulatory Updates", SERVICE_TASK, "Compliance Team"),
        ("Join Preparation", PARALLEL_GW, "Regional Office"),
        
        # Document submission and review
        ("Submit Documents", SEND_TASK, "Regional Office"),
        ("Review Submission", USER_TASK, "Central Audit Team"),
        ("Discrepancies Found?", EXCLUSIVE_GW, "Central Audit Team"),
        ("Request Clarifications", SEND_TASK, "Central Audit Team"),
        ("Provide Clarifications", USER_TASK, "Regional Office"),
        
        # Risk assessment (inclusive - all must complete)
        ("Fork Risk Assessment", PARALLEL_GW, "Central Audit Team"),
        ("Evaluate Financial Risks", USER_TASK, "Central Audit Team"),
        ("Evaluate Operational Risks", USER_TASK, "Central Audit Team"),
        ("Evaluate Compliance Risks", USER_TASK, "Central Audit Team"),
        ("Join Risk Assessment", PARALLEL_GW, "Central Audit Team"),
        
        # High risk check
        ("High Risk?", EXCLUSIVE_GW, "Central Audit Team"),
        
        # Investigation (parallel activities)
        ("Fork Investigation", PARALLEL_GW, "Central Audit Team"),
        ("Data Analysis", SERVICE_TASK, "Central Audit Team"),
        ("Conduct Interviews", USER_TASK, "Central Audit Team"),
        ("Site Visits", USER_TASK, "Central Audit Team"),
        ("Join Investigation", PARALLEL_GW, "Central Audit Team"),
        
        # Report compilation and approval
        ("Compile Audit Report", USER_TASK, "Central Audit Team"),
        ("Review Report", USER_TASK, "Audit Director"),
        ("Report Approved?", EXCLUSIVE_GW, "Audit Director"),
        ("Update Report", USER_TASK, "Central Audit Team"),
        
        # Final distribution
        ("Fork Distribution", PARALLEL_GW, "Audit Director"),
        ("Distribute to Board", SEND_TASK, "Executive Board"),
        ("Archive Report", SERVICE_TASK, "Audit Director"),
        ("Join Distribution", PARALLEL_GW, "Audit Director"),
        
        # End
        ("Close Audit", END, "Audit Coordinator"),
    ],
    
    "flows": [
        # Initial flow
        ("Start Audit", "Send Notification", ""),
        ("Send Notification", "Fork Preparation", ""),
        
        # Parallel preparation
        ("Fork Preparation", "Prepare Financial Statements", ""),
        ("Fork Preparation", "Check Regulatory Updates", ""),
        ("Prepare Financial Statements", "Gather Documents", ""),
        ("Gather Documents", "Join Preparation", ""),
        ("Check Regulatory Updates", "Join Preparation", ""),
        
        # Submit and review
        ("Join Preparation", "Submit Documents", ""),
        ("Submit Documents", "Review Submission", ""),
        ("Review Submission", "Discrepancies Found?", ""),
        
        # Clarification loop
        ("Discrepancies Found?", "Request Clarifications", "Yes"),
        ("Request Clarifications", "Provide Clarifications", ""),
        ("Provide Clarifications", "Review Submission", ""),
        
        # Risk assessment
        ("Discrepancies Found?", "Fork Risk Assessment", "No"),
        ("Fork Risk Assessment", "Evaluate Financial Risks", ""),
        ("Fork Risk Assessment", "Evaluate Operational Risks", ""),
        ("Fork Risk Assessment", "Evaluate Compliance Risks", ""),
        ("Evaluate Financial Risks", "Join Risk Assessment", ""),
        ("Evaluate Operational Risks", "Join Risk Assessment", ""),
        ("Evaluate Compliance Risks", "Join Risk Assessment", ""),
        
        # High risk decision
        ("Join Risk Assessment", "High Risk?", ""),
        ("High Risk?", "Fork Investigation", "Yes"),
        
        # Investigation
        ("Fork Investigation", "Data Analysis", ""),
        ("Fork Investigation", "Conduct Interviews", ""),
        ("Fork Investigation", "Site Visits", ""),
        ("Data Analysis", "Join Investigation", ""),
        ("Conduct Interviews", "Join Investigation", ""),
        ("Site Visits", "Join Investigation", ""),
        ("Join Investigation", "Compile Audit Report", ""),
        
        # No high risk - straight to compile
        ("High Risk?", "Compile Audit Report", "No"),
        
        # Report approval loop
        ("Compile Audit Report", "Review Report", ""),
        ("Review Report", "Report Approved?", ""),
        ("Report Approved?", "Update Report", "No"),
        ("Update Report", "Review Report", ""),
        
        # Final distribution
        ("Report Approved?", "Fork Distribution", "Yes"),
        ("Fork Distribution", "Distribute to Board", ""),
        ("Fork Distribution", "Archive Report", ""),
        ("Distribute to Board", "Join Distribution", ""),
        ("Archive Report", "Join Distribution", ""),
        ("Join Distribution", "Close Audit", ""),
    ],
    
    "data_objects": [
        ("Financial Statements", "Regional Office", 3),
        ("Supporting Documents", "Regional Office", 4),
        ("Clarification Request", "Central Audit Team", 8),
        ("Risk Assessment Report", "Central Audit Team", 13),
        ("Investigation Findings", "Central Audit Team", 17),
        ("Audit Report", "Central Audit Team", 18),
        ("Final Report", "Audit Director", 21),
    ],
    
    "data_associations": [
        # Document preparation
        ("Prepare Financial Statements", "Financial Statements"),
        ("Gather Documents", "Supporting Documents"),
        ("Financial Statements", "Submit Documents"),
        ("Supporting Documents", "Submit Documents"),
        
        # Clarification
        ("Request Clarifications", "Clarification Request"),
        ("Clarification Request", "Provide Clarifications"),
        
        # Risk assessment output
        ("Join Risk Assessment", "Risk Assessment Report"),
        ("Risk Assessment Report", "High Risk?"),
        
        # Investigation output
        ("Join Investigation", "Investigation Findings"),
        ("Investigation Findings", "Compile Audit Report"),
        
        # Report
        ("Compile Audit Report", "Audit Report"),
        ("Audit Report", "Review Report"),
        ("Review Report", "Final Report"),
        ("Final Report", "Distribute to Board"),
        ("Final Report", "Archive Report"),
    ],
    
    "layout": {
        # Column 0: Start
        "Start Audit": 0,
        
        # Column 1: Send notification
        "Send Notification": 1,
        
        # Column 2: Fork preparation
        "Fork Preparation": 2,
        
        # Column 3: Parallel preparation tasks
        "Prepare Financial Statements": 3,
        "Check Regulatory Updates": 3,
        
        # Column 4: Gather documents
        "Gather Documents": 4,
        
        # Column 5: Join preparation
        "Join Preparation": 5,
        
        # Column 6: Submit documents
        "Submit Documents": 6,
        
        # Column 7: Review submission
        "Review Submission": 7,
        
        # Column 8: Discrepancies check
        "Discrepancies Found?": 8,
        
        # Column 9: Clarification activities (stacked)
        "Request Clarifications": 9,
        "Provide Clarifications": 9,
        
        # Column 10: Fork risk assessment
        "Fork Risk Assessment": 10,
        
        # Column 11: Risk evaluation tasks (auto-stacked)
        "Evaluate Financial Risks": 11,
        "Evaluate Operational Risks": 11,
        "Evaluate Compliance Risks": 11,
        
        # Column 12: Join risk assessment
        "Join Risk Assessment": 12,
        
        # Column 13: High risk decision
        "High Risk?": 13,
        
        # Column 14: Fork investigation
        "Fork Investigation": 14,
        
        # Column 15: Investigation tasks (auto-stacked)
        "Data Analysis": 15,
        "Conduct Interviews": 15,
        "Site Visits": 15,
        
        # Column 16: Join investigation
        "Join Investigation": 16,
        
        # Column 17: Compile report
        "Compile Audit Report": 17,
        
        # Column 18: Review report
        "Review Report": 18,
        
        # Column 19: Approval decision and revision (stacked)
        "Report Approved?": 19,
        "Update Report": 19,
        
        # Column 20: Fork distribution
        "Fork Distribution": 20,
        
        # Column 21: Distribution tasks (auto-stacked)
        "Distribute to Board": 21,
        "Archive Report": 21,
        
        # Column 22: Join distribution
        "Join Distribution": 22,
        
        # Column 23: End
        "Close Audit": 23,
    },
    
    # Adjusted spacing for wide diagram
    "SPACING": 140,
    "START_X": 60,
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
