#
# ComplianceAudit.py
#
# Description: Generates a Compliance Audit process diagram.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComplianceAuditProcess",
    
    "lanes": ["Company", "Auditor"],
    
    "elements": [
        # Start
        ("Audit Scheduled", START, "Company"),
        
        # Preparation Phase (Company)
        ("Prepare Documentation", USER_TASK, "Company"),
        ("Gather Evidence", USER_TASK, "Company"),
        ("Conduct Self-Assessment", USER_TASK, "Company"),
        
        # Audit Phase (Auditor)
        ("Perform Initial Audit", USER_TASK, "Auditor"),
        
        # Correction Phase (Company)
        ("Implement Corrections", USER_TASK, "Company"),
        
        # Final Audit (Auditor)
        ("Conduct Final Audit", USER_TASK, "Auditor"),
        
        # Decision
        ("Criteria Met?", EXCLUSIVE_GW, "Auditor"),
        
        # Conclusion
        ("Award Certification", USER_TASK, "Auditor"),
        ("Issue Official Documents", USER_TASK, "Company"),
        ("End", END, "Company"),
    ],
    
    "flows": [
        # Preparation Flow
        ("Audit Scheduled", "Prepare Documentation", ""),
        ("Prepare Documentation", "Gather Evidence", ""),
        ("Gather Evidence", "Conduct Self-Assessment", ""),
        
        # Transition to Auditor
        ("Conduct Self-Assessment", "Perform Initial Audit", ""),
        
        # Audit to Correction
        ("Perform Initial Audit", "Implement Corrections", ""),
        
        # Correction to Final Audit
        ("Implement Corrections", "Conduct Final Audit", ""),
        
        # Decision Point
        ("Conduct Final Audit", "Criteria Met?", ""),
        ("Criteria Met?", "Award Certification", "Yes"),
        ("Criteria Met?", "Implement Corrections", "No"),
        
        # Conclusion
        ("Award Certification", "Issue Official Documents", ""),
        ("Issue Official Documents", "End", ""),
    ],
    
    "layout": {
        # Column 0: Start
        "Audit Scheduled": 0,
        
        # Column 1-3: Preparation
        "Prepare Documentation": 1,
        "Gather Evidence": 2,
        "Conduct Self-Assessment": 3,
        
        # Column 4: Initial Audit
        "Perform Initial Audit": 4,
        
        # Column 5: Corrections
        "Implement Corrections": 5,
        
        # Column 6: Final Audit
        "Conduct Final Audit": 6,
        
        # Column 7: Decision
        "Criteria Met?": 7,
        
        # Column 8: Certification
        "Award Certification": 8,
        
        # Column 9: Documents & End
        "Issue Official Documents": 9,
        "End": 10,
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
