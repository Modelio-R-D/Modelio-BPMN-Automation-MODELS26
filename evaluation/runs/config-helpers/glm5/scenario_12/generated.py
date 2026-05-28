CONFIG = {
    "name": "EmployeeDevelopmentPromotion",
    
    "lanes": ["Employee", "Manager", "HR"],
    
    "elements": [
        ("Start", "START", "Manager"),
        ("Identify Development Needs", "USER_TASK", "Manager"),
        ("Create Development Plan", "USER_TASK", "Manager"),
        ("Skill Enhancement", "USER_TASK", "Employee"),
        ("Provide Feedback", "USER_TASK", "Manager"),
        ("Milestones Reached?", "EXCLUSIVE_GW", "Manager"),
        ("Consider for Promotion", "USER_TASK", "Manager"),
        ("Formal Performance Review", "USER_TASK", "HR"),
        ("Approved?", "EXCLUSIVE_GW", "HR"),
        ("Finalize Promotion", "USER_TASK", "HR"),
        ("Transition to New Role", "USER_TASK", "Employee"),
        ("End", "END", "Employee"),
    ],
    
    "flows": [
        ("Start", "Identify Development Needs", ""),
        ("Identify Development Needs", "Create Development Plan", ""),
        ("Create Development Plan", "Skill Enhancement", ""),
        ("Skill Enhancement", "Provide Feedback", ""),
        ("Provide Feedback", "Milestones Reached?", ""),
        ("Milestones Reached?", "Consider for Promotion", "Yes"),
        ("Milestones Reached?", "Skill Enhancement", "No"),
        ("Consider for Promotion", "Formal Performance Review", ""),
        ("Formal Performance Review", "Approved?", ""),
        ("Approved?", "Finalize Promotion", "Yes"),
        ("Approved?", "Create Development Plan", "No"),
        ("Finalize Promotion", "Transition to New Role", ""),
        ("Transition to New Role", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Identify Development Needs": 1,
        "Create Development Plan": 2,
        "Skill Enhancement": 3,
        "Provide Feedback": 4,
        "Milestones Reached?": 5,
        "Consider for Promotion": 6,
        "Formal Performance Review": 7,
        "Approved?": 8,
        "Finalize Promotion": 9,
        "Transition to New Role": 10,
        "End": 11,
    },
}


"data_objects": [
    ("Development Plan", "Manager", 2),
    ("Feedback Record", "Manager", 4),
    ("Review Report", "HR", 7),
    ("Promotion Record", "HR", 9),
],

"data_associations": [
    ("Create Development Plan", "Development Plan"),
    ("Development Plan", "Skill Enhancement"),
    ("Provide Feedback", "Feedback Record"),
    ("Feedback Record", "Milestones Reached?"),  # WAIT - gateway can't have data association!
    ("Formal Performance Review", "Review Report"),
    ("Review Report", "Approved?"),  # WAIT - gateway can't have data association!
    ("Finalize Promotion", "Promotion Record"),
],


"data_objects": [
    ("Development Plan", "Manager", 2),
    ("Feedback Record", "Manager", 4),
    ("Review Report", "HR", 7),
    ("Promotion Record", "HR", 9),
],

"data_associations": [
    ("Create Development Plan", "Development Plan"),
    ("Development Plan", "Skill Enhancement"),
    ("Provide Feedback", "Feedback Record"),
    # Feedback Record informs Milestones decision but can't connect to gateway
    ("Formal Performance Review", "Review Report"),
    # Review Report informs Approved decision but can't connect to gateway
    ("Finalize Promotion", "Promotion Record"),
],


"data_objects": [
    ("Development Plan", "Manager", 2),
    ("Promotion Record", "HR", 9),
],

"data_associations": [
    ("Create Development Plan", "Development Plan"),
    ("Development Plan", "Skill Enhancement"),
    ("Finalize Promotion", "Promotion Record"),
],


#
# EmployeeDevelopmentPromotion.py
#
# Description: Employee Development and Promotion Process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "EmployeeDevelopmentPromotion",
    
    "lanes": ["Employee", "Manager", "HR"],
    
    "elements": [
        ("Start", START, "Manager"),
        ("Identify Development Needs", USER_TASK, "Manager"),
        ("Create Development Plan", USER_TASK, "Manager"),
        ("Skill Enhancement", USER_TASK, "Employee"),
        ("Provide Feedback", USER_TASK, "Manager"),
        ("Milestones Reached?", EXCLUSIVE_GW, "Manager"),
        ("Consider for Promotion", USER_TASK, "Manager"),
        ("Formal Performance Review", USER_TASK, "HR"),
        ("Approved?", EXCLUSIVE_GW, "HR"),
        ("Finalize Promotion", USER_TASK, "HR"),
        ("Transition to New Role", USER_TASK, "Employee"),
        ("End", END, "Employee"),
    ],
    
    "flows": [
        ("Start", "Identify Development Needs", ""),
        ("Identify Development Needs", "Create Development Plan", ""),
        ("Create Development Plan", "Skill Enhancement", ""),
        ("Skill Enhancement", "Provide Feedback", ""),
        ("Provide Feedback", "Milestones Reached?", ""),
        ("Milestones Reached?", "Consider for Promotion", "Yes"),
        ("Milestones Reached?", "Skill Enhancement", "No"),
        ("Consider for Promotion", "Formal Performance Review", ""),
        ("Formal Performance Review", "Approved?", ""),
        ("Approved?", "Finalize Promotion", "Yes"),
        ("Approved?", "Create Development Plan", "No"),
        ("Finalize Promotion", "Transition to New Role", ""),
        ("Transition to New Role", "End", ""),
    ],
    
    "data_objects": [
        ("Development Plan", "Manager", 2),
        ("Promotion Record", "HR", 9),
    ],
    
    "data_associations": [
        ("Create Development Plan", "Development Plan"),
        ("Development Plan", "Skill Enhancement"),
        ("Finalize Promotion", "Promotion Record"),
    ],
    
    "layout": {
        "Start": 0,
        "Identify Development Needs": 1,
        "Create Development Plan": 2,
        "Skill Enhancement": 3,
        "Provide Feedback": 4,
        "Milestones Reached?": 5,
        "Consider for Promotion": 6,
        "Formal Performance Review": 7,
        "Approved?": 8,
        "Finalize Promotion": 9,
        "Transition to New Role": 10,
        "End": 11,
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


#
# EmployeeDevelopmentPromotion.py
#
# Description: Employee Development and Promotion Process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "EmployeeDevelopmentPromotion",
    
    "lanes": ["Employee", "Manager", "HR"],
    
    "elements": [
        # Start - Manager initiates development process
        ("Start", START, "Manager"),
        
        # Manager identifies needs and creates plan
        ("Identify Development Needs", USER_TASK, "Manager"),
        ("Create Development Plan", USER_TASK, "Manager"),
        
        # Employee skill building with feedback loop
        ("Skill Enhancement", USER_TASK, "Employee"),
        ("Provide Feedback", USER_TASK, "Manager"),
        ("Milestones Reached?", EXCLUSIVE_GW, "Manager"),
        
        # Promotion consideration and review
        ("Consider for Promotion", USER_TASK, "Manager"),
        ("Formal Performance Review", USER_TASK, "HR"),
        ("Approved?", EXCLUSIVE_GW, "HR"),
        
        # Finalization and transition
        ("Finalize Promotion", USER_TASK, "HR"),
        ("Transition to New Role", USER_TASK, "Employee"),
        ("End", END, "Employee"),
    ],
    
    "flows": [
        # Main flow
        ("Start", "Identify Development Needs", ""),
        ("Identify Development Needs", "Create Development Plan", ""),
        ("Create Development Plan", "Skill Enhancement", ""),
        ("Skill Enhancement", "Provide Feedback", ""),
        ("Provide Feedback", "Milestones Reached?", ""),
        
        # Milestone decision
        ("Milestones Reached?", "Consider for Promotion", "Yes"),
        ("Milestones Reached?", "Skill Enhancement", "No"),
        
        # Review flow
        ("Consider for Promotion", "Formal Performance Review", ""),
        ("Formal Performance Review", "Approved?", ""),
        
        # Approval decision
        ("Approved?", "Finalize Promotion", "Yes"),
        ("Approved?", "Create Development Plan", "No"),
        
        # Complete
        ("Finalize Promotion", "Transition to New Role", ""),
        ("Transition to New Role", "End", ""),
    ],
    
    "data_objects": [
        ("Development Plan", "Manager", 2),
        ("Promotion Record", "HR", 9),
    ],
    
    "data_associations": [
        ("Create Development Plan", "Development Plan"),
        ("Development Plan", "Skill Enhancement"),
        ("Finalize Promotion", "Promotion Record"),
    ],
    
    "layout": {
        "Start": 0,
        "Identify Development Needs": 1,
        "Create Development Plan": 2,
        "Skill Enhancement": 3,
        "Provide Feedback": 4,
        "Milestones Reached?": 5,
        "Consider for Promotion": 6,
        "Formal Performance Review": 7,
        "Approved?": 8,
        "Finalize Promotion": 9,
        "Transition to New Role": 10,
        "End": 11,
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
