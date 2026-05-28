#
# EmployeeDevelopmentPromotion.py
#
# Description: Employee development and promotion process from needs identification through promotion finalization
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "EmployeeDevelopmentPromotion",
    
    "lanes": ["Employee", "Manager", "HR"],
    
    "elements": [
        # Start
        ("Start", START, "Employee"),
        
        # Initial identification
        ("Identify Development Needs", USER_TASK, "Employee"),
        
        # Planning phase
        ("Create Development Plan", USER_TASK, "Manager"),
        ("Review and Approve Plan", USER_TASK, "HR"),
        
        # Development phase
        ("Work on Skill Enhancement", USER_TASK, "Employee"),
        ("Provide Feedback", USER_TASK, "Manager"),
        
        # Milestone check
        ("Milestone Reached?", EXCLUSIVE_GW, "Manager"),
        
        # Promotion consideration
        ("Consider for Promotion", USER_TASK, "Manager"),
        ("Conduct Performance Review", USER_TASK, "HR"),
        
        # Approval decision
        ("Promotion Approved?", EXCLUSIVE_GW, "HR"),
        
        # Finalization
        ("Finalize Promotion", USER_TASK, "HR"),
        ("Adjust Compensation", SERVICE_TASK, "HR"),
        ("Transition to New Role", USER_TASK, "Employee"),
        
        # End
        ("End", END, "Employee"),
    ],
    
    "flows": [
        ("Start", "Identify Development Needs", ""),
        ("Identify Development Needs", "Create Development Plan", ""),
        ("Create Development Plan", "Review and Approve Plan", ""),
        ("Review and Approve Plan", "Work on Skill Enhancement", ""),
        ("Work on Skill Enhancement", "Provide Feedback", ""),
        ("Provide Feedback", "Milestone Reached?", ""),
        ("Milestone Reached?", "Work on Skill Enhancement", "No"),
        ("Milestone Reached?", "Consider for Promotion", "Yes"),
        ("Consider for Promotion", "Conduct Performance Review", ""),
        ("Conduct Performance Review", "Promotion Approved?", ""),
        ("Promotion Approved?", "Work on Skill Enhancement", "No"),
        ("Promotion Approved?", "Finalize Promotion", "Yes"),
        ("Finalize Promotion", "Adjust Compensation", ""),
        ("Adjust Compensation", "Transition to New Role", ""),
        ("Transition to New Role", "End", ""),
    ],
    
    "data_objects": [
        ("Development Plan", "Manager", 2),
        ("Performance Report", "HR", 7),
        ("Promotion Letter", "HR", 10),
    ],
    
    "data_associations": [
        ("Create Development Plan", "Development Plan"),
        ("Development Plan", "Review and Approve Plan"),
        ("Conduct Performance Review", "Performance Report"),
        ("Performance Report", "Promotion Approved?"),
        ("Finalize Promotion", "Promotion Letter"),
        ("Promotion Letter", "Transition to New Role"),
    ],
    
    "layout": {
        "Start": 0,
        "Identify Development Needs": 1,
        "Create Development Plan": 2,
        "Review and Approve Plan": 3,
        "Work on Skill Enhancement": 4,
        "Provide Feedback": 5,
        "Milestone Reached?": 6,
        "Consider for Promotion": 7,
        "Conduct Performance Review": 8,
        "Promotion Approved?": 9,
        "Finalize Promotion": 10,
        "Adjust Compensation": 11,
        "Transition to New Role": 12,
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
