#
# WorkAccident.py
#
# Description: Process for gathering information about work accidents and near-misses
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "WorkAccident",
    
    "lanes": ["Employee/Insured", "Employer/School", "Authority/Insurance"],
    
    "elements": [
        # Start Event
        ("Accident Occurs", START, "Employee/Insured"),
        
        # Employee reporting - immediate notification requirement
        ("Report Incident", USER_TASK, "Employee/Insured"),
        ("Incident Type?", EXCLUSIVE_GW, "Employee/Insured"),
        ("Log Near-Miss/Risk", SERVICE_TASK, "Employee/Insured"),
        
        # Employer processing - receives and assesses report
        ("Receive Report", USER_TASK, "Employer/School"),
        ("Assess Severity", USER_TASK, "Employer/School"),
        ("Fatal or Serious?", EXCLUSIVE_GW, "Employer/School"),
        ("Report to Labour Inspectorate", SERVICE_TASK, "Employer/School"),
        
        # Authority/Insurance processing - verification and reporting
        ("Verify Insurance Status", SERVICE_TASK, "Authority/Insurance"),
        ("Person Insured?", EXCLUSIVE_GW, "Authority/Insurance"),
        ("Death or 3+ Days?", EXCLUSIVE_GW, "Authority/Insurance"),
        ("Report to Insurance (5 Days)", SERVICE_TASK, "Authority/Insurance"),
        ("Fatality?", EXCLUSIVE_GW, "Authority/Insurance"),
        ("Fatality Report (3 Days)", SERVICE_TASK, "Authority/Insurance"),
        
        # End Events
        ("Near-Miss Logged", END, "Employee/Insured"),
        ("No Insurance Coverage", END, "Authority/Insurance"),
        ("Minor Injury Logged", END, "Authority/Insurance"),
        ("Process Complete", END, "Authority/Insurance"),
    ],
    
    "flows": [
        # Initial incident reporting
        ("Accident Occurs", "Report Incident", ""),
        ("Report Incident", "Incident Type?", ""),
        
        # Branch: Near-miss vs Work Accident
        ("Incident Type?", "Log Near-Miss/Risk", "Near-Miss/Risk/Defect"),
        ("Incident Type?", "Receive Report", "Work Accident"),
        ("Log Near-Miss/Risk", "Near-Miss Logged", ""),
        
        # Employer assessment
        ("Receive Report", "Assess Severity", ""),
        ("Assess Severity", "Fatal or Serious?", ""),
        
        # Branch: Fatal/Serious requires immediate Labour Inspectorate report
        ("Fatal or Serious?", "Report to Labour Inspectorate", "Yes"),
        ("Fatal or Serious?", "Verify Insurance Status", "No"),
        ("Report to Labour Inspectorate", "Verify Insurance Status", ""),
        
        # Insurance verification
        ("Verify Insurance Status", "Person Insured?", ""),
        ("Person Insured?", "No Insurance Coverage", "No"),
        ("Person Insured?", "Death or 3+ Days?", "Yes"),
        
        # Branch: Impact duration determines reporting requirement
        ("Death or 3+ Days?", "Minor Injury Logged", "No"),
        ("Death or 3+ Days?", "Report to Insurance (5 Days)", "Yes"),
        
        # Final fatality check - additional 3-day report if fatality
        ("Report to Insurance (5 Days)", "Fatality?", ""),
        ("Fatality?", "Fatality Report (3 Days)", "Yes"),
        ("Fatality?", "Process Complete", "No"),
        ("Fatality Report (3 Days)", "Process Complete", ""),
    ],
    
    "layout": {
        "Accident Occurs": 0,
        "Report Incident": 1,
        "Incident Type?": 2,
        "Log Near-Miss/Risk": 3,
        "Near-Miss Logged": 4,
        "Receive Report": 3,
        "Assess Severity": 4,
        "Fatal or Serious?": 5,
        "Report to Labour Inspectorate": 6,
        "Verify Insurance Status": 7,
        "Person Insured?": 8,
        "No Insurance Coverage": 9,
        "Death or 3+ Days?": 9,
        "Minor Injury Logged": 10,
        "Report to Insurance (5 Days)": 10,
        "Fatality?": 11,
        "Fatality Report (3 Days)": 12,
        "Process Complete": 13,
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
