#
# HiringProcess.py
#
# Description: Employee hiring process from need identification to full integration
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "HiringProcess",
    
    "lanes": ["Department", "HR", "Candidate"],
    
    "elements": [
        # Start - Department initiates hiring need
        ("Hiring Need", START, "Department"),
        
        # HR recruitment activities
        ("Create Job Description", USER_TASK, "HR"),
        ("Post on Job Boards", USER_TASK, "HR"),
        ("Screen Resumes", USER_TASK, "HR"),
        ("Phone Interviews", USER_TASK, "HR"),
        
        # Interview type choice (candidate decides)
        ("Choose Interview Type", EXCLUSIVE_GW, "Candidate"),
        ("In-Person Interview", USER_TASK, "HR"),
        ("Virtual Interview", USER_TASK, "HR"),
        ("Interviews Complete", EXCLUSIVE_GW, "HR"),
        
        # Selection and offer
        ("Select Candidate", USER_TASK, "HR"),
        ("Extend Offer", USER_TASK, "HR"),
        ("Negotiate Salary", USER_TASK, "HR"),
        
        # Candidate accepts
        ("Accept Offer", USER_TASK, "Candidate"),
        
        # Onboarding activities
        ("Complete Paperwork", USER_TASK, "HR"),
        ("Orientation", USER_TASK, "HR"),
        ("Training", USER_TASK, "HR"),
        
        # End
        ("New Hire Integrated", END, "HR"),
    ],
    
    "flows": [
        # Initial flow
        ("Hiring Need", "Create Job Description", ""),
        ("Create Job Description", "Post on Job Boards", ""),
        ("Post on Job Boards", "Screen Resumes", ""),
        ("Screen Resumes", "Phone Interviews", ""),
        
        # Interview type decision
        ("Phone Interviews", "Choose Interview Type", ""),
        ("Choose Interview Type", "In-Person Interview", "In-Person"),
        ("Choose Interview Type", "Virtual Interview", "Virtual"),
        
        # Merge back after interviews
        ("In-Person Interview", "Interviews Complete", ""),
        ("Virtual Interview", "Interviews Complete", ""),
        
        # Selection and offer process
        ("Interviews Complete", "Select Candidate", ""),
        ("Select Candidate", "Extend Offer", ""),
        ("Extend Offer", "Negotiate Salary", ""),
        ("Negotiate Salary", "Accept Offer", ""),
        
        # Onboarding flow
        ("Accept Offer", "Complete Paperwork", ""),
        ("Complete Paperwork", "Orientation", ""),
        ("Orientation", "Training", ""),
        ("Training", "New Hire Integrated", ""),
    ],
    
    "layout": {
        "Hiring Need": 0,
        "Create Job Description": 1,
        "Post on Job Boards": 2,
        "Screen Resumes": 3,
        "Phone Interviews": 4,
        "Choose Interview Type": 5,
        "In-Person Interview": 6,
        "Virtual Interview": 6,
        "Interviews Complete": 7,
        "Select Candidate": 8,
        "Extend Offer": 9,
        "Negotiate Salary": 10,
        "Accept Offer": 11,
        "Complete Paperwork": 12,
        "Orientation": 13,
        "Training": 14,
        "New Hire Integrated": 15,
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
