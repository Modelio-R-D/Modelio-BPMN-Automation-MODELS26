#
# ComplianceAuditProcess.py
#
# Description: Compliance audit process for ISO standards, safety protocols, or environmental guidelines
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComplianceAuditProcess",
    
    "lanes": ["Company", "Internal Teams", "External Auditors"],
    
    "elements": [
        # Company lane
        ("Start", START, "Company"),
        ("Schedule Compliance Audit", USER_TASK, "Company"),
        ("Make Corrections", USER_TASK, "Company"),
        ("Certification Awarded?", EXCLUSIVE_GW, "Company"),
        ("Receive Certification", USER_TASK, "Company"),
        ("End", END, "Company"),
        
        # Internal Teams lane
        ("Prepare Documentation", USER_TASK, "Internal Teams"),
        ("Gather Evidence", USER_TASK, "Internal Teams"),
        ("Conduct Self-Assessment", USER_TASK, "Internal Teams"),
        
        # External Auditors lane
        ("Review Processes", USER_TASK, "External Auditors"),
        ("Identify Gaps", USER_TASK, "External Auditors"),
        ("Conduct Final Audit", USER_TASK, "External Auditors"),
        ("Evaluate Compliance", USER_TASK, "External Auditors"),
        ("Issue Official Documents", USER_TASK, "External Auditors"),
    ],
    
    "data_objects": [
        ("Audit Schedule", "Company", 1),
        ("Documentation Package", "Internal Teams", 3),
        ("Gap Analysis Report", "External Auditors", 5),
        ("Certification Documents", "External Auditors", 9),
    ],
    
    "data_associations": [
        ("Schedule Compliance Audit", "Audit Schedule"),
        ("Audit Schedule", "Prepare Documentation"),
        ("Conduct Self-Assessment", "Documentation Package"),
        ("Documentation Package", "Review Processes"),
        ("Identify Gaps", "Gap Analysis Report"),
        ("Gap Analysis Report", "Make Corrections"),
        ("Issue Official Documents", "Certification Documents"),
        ("Certification Documents", "Receive Certification"),
    ],
    
    "flows": [
        ("Start", "Schedule Compliance Audit", ""),
        ("Schedule Compliance Audit", "Prepare Documentation", ""),
        ("Prepare Documentation", "Gather Evidence", ""),
        ("Gather Evidence", "Conduct Self-Assessment", ""),
        ("Conduct Self-Assessment", "Review Processes", ""),
        ("Review Processes", "Identify Gaps", ""),
        ("Identify Gaps", "Make Corrections", ""),
        ("Make Corrections", "Conduct Final Audit", ""),
        ("Conduct Final Audit", "Evaluate Compliance", ""),
        ("Evaluate Compliance", "Certification Awarded?", ""),
        ("Certification Awarded?", "Make Corrections", "No"),
        ("Certification Awarded?", "Issue Official Documents", "Yes"),
        ("Issue Official Documents", "Receive Certification", ""),
        ("Receive Certification", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Schedule Compliance Audit": 1,
        "Prepare Documentation": 2,
        "Gather Evidence": 3,
        "Conduct Self-Assessment": 4,
        "Review Processes": 5,
        "Identify Gaps": 6,
        "Make Corrections": 7,
        "Conduct Final Audit": 8,
        "Evaluate Compliance": 9,
        "Certification Awarded?": 10,
        "Issue Official Documents": 11,
        "Receive Certification": 12,
        "End": 13,
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
