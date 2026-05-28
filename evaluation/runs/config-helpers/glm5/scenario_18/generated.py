#
# UniversityEnrollment.py
#
# Description: University Enrollment Process with application, confirmation, 
#              onboarding, semester activities, and appeals
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "UniversityEnrollment",
    
    "lanes": [
        "Student", 
        "Admissions Office", 
        "Finance Department", 
        "IT Department", 
        "International Office", 
        "Registrar"
    ],
    
    "elements": [
        # === APPLICATION PHASE ===
        ("Start", START, "Student"),
        ("Submit Application", USER_TASK, "Student"),
        ("Review Application", USER_TASK, "Admissions Office"),
        ("Documents Complete?", EXCLUSIVE_GW, "Admissions Office"),
        ("Notify Missing Documents", USER_TASK, "Admissions Office"),
        ("Resubmit Documents", USER_TASK, "Student"),
        
        # === PARALLEL EVALUATION ===
        ("Fork Evaluation", PARALLEL_GW, "Admissions Office"),
        ("Evaluate Application", USER_TASK, "Admissions Office"),
        ("Process Fees Waivers", USER_TASK, "Finance Department"),
        ("Join Evaluation", PARALLEL_GW, "Admissions Office"),
        
        # === ACCEPTANCE DECISION ===
        ("Application Accepted?", EXCLUSIVE_GW, "Admissions Office"),
        ("Send Rejection Letter", USER_TASK, "Admissions Office"),
        ("End Rejected", END, "Admissions Office"),
        ("Send Acceptance Letter", USER_TASK, "Admissions Office"),
        
        # === CONFIRMATION PHASE ===
        ("Confirm Enrollment", USER_TASK, "Student"),
        ("Confirmed by Deadline?", EXCLUSIVE_GW, "Student"),
        ("Cancel Application", USER_TASK, "Admissions Office"),
        ("End Cancelled", END, "Admissions Office"),
        
        # === PARALLEL ONBOARDING ===
        ("Fork Onboarding", PARALLEL_GW, "Admissions Office"),
        ("Send Orientation Materials", USER_TASK, "Admissions Office"),
        ("Setup Student Accounts", SERVICE_TASK, "IT Department"),
        ("Is International?", EXCLUSIVE_GW, "Student"),
        ("Process Visa", USER_TASK, "International Office"),
        ("Join Onboarding", PARALLEL_GW, "Student"),
        
        # === STUDY PLAN ===
        ("Get Student ID Card", USER_TASK, "Student"),
        ("Meet Academic Advisor", USER_TASK, "Student"),
        ("Select Courses", USER_TASK, "Student"),
        ("Schedule Conflicts?", EXCLUSIVE_GW, "Student"),
        ("Resolve Conflicts", USER_TASK, "Student"),
        
        # === SEMESTER ACTIVITIES ===
        ("Begin Classes", USER_TASK, "Student"),
        ("Add Drop Courses", USER_TASK, "Student"),
        ("Post Grades", USER_TASK, "Registrar"),
        ("Review Grades", USER_TASK, "Student"),
        
        # === APPEALS PROCESS ===
        ("Has Grievance?", EXCLUSIVE_GW, "Student"),
        ("Submit Appeal Form", USER_TASK, "Student"),
        ("Appeals Committee Review", USER_TASK, "Registrar"),
        ("Receive Appeal Decision", USER_TASK, "Student"),
        
        # === COMPLETION ===
        ("Graduated or Withdrawn?", EXCLUSIVE_GW, "Student"),
        ("End", END, "Student"),
    ],
    
    "flows": [
        # Application flow
        ("Start", "Submit Application", ""),
        ("Submit Application", "Review Application", ""),
        ("Review Application", "Documents Complete?", ""),
        ("Documents Complete?", "Notify Missing Documents", "No"),
        ("Notify Missing Documents", "Resubmit Documents", ""),
        ("Resubmit Documents", "Review Application", ""),
        ("Documents Complete?", "Fork Evaluation", "Yes"),
        
        # Parallel evaluation
        ("Fork Evaluation", "Evaluate Application", ""),
        ("Fork Evaluation", "Process Fees Waivers", ""),
        ("Evaluate Application", "Join Evaluation", ""),
        ("Process Fees Waivers", "Join Evaluation", ""),
        ("Join Evaluation", "Application Accepted?", ""),
        
        # Decision
        ("Application Accepted?", "Send Rejection Letter", "No"),
        ("Send Rejection Letter", "End Rejected", ""),
        ("Application Accepted?", "Send Acceptance Letter", "Yes"),
        
        # Confirmation
        ("Send Acceptance Letter", "Confirm Enrollment", ""),
        ("Confirm Enrollment", "Confirmed by Deadline?", ""),
        ("Confirmed by Deadline?", "Cancel Application", "No"),
        ("Cancel Application", "End Cancelled", ""),
        ("Confirmed by Deadline?", "Fork Onboarding", "Yes"),
        
        # Onboarding parallel
        ("Fork Onboarding", "Send Orientation Materials", ""),
        ("Fork Onboarding", "Setup Student Accounts", ""),
        ("Fork Onboarding", "Is International?", ""),
        ("Is International?", "Process Visa", "Yes"),
        ("Is International?", "Join Onboarding", "No"),
        ("Process Visa", "Join Onboarding", ""),
        ("Send Orientation Materials", "Join Onboarding", ""),
        ("Setup Student Accounts", "Join Onboarding", ""),
        
        # Study plan
        ("Join Onboarding", "Get Student ID Card", ""),
        ("Get Student ID Card", "Meet Academic Advisor", ""),
        ("Meet Academic Advisor", "Select Courses", ""),
        ("Select Courses", "Schedule Conflicts?", ""),
        ("Schedule Conflicts?", "Resolve Conflicts", "Yes"),
        ("Resolve Conflicts", "Select Courses", ""),
        ("Schedule Conflicts?", "Begin Classes", "No"),
        
        # Semester
        ("Begin Classes", "Add Drop Courses", ""),
        ("Add Drop Courses", "Post Grades", ""),
        ("Post Grades", "Review Grades", ""),
        ("Review Grades", "Has Grievance?", ""),
        
        # Appeals
        ("Has Grievance?", "Submit Appeal Form", "Yes"),
        ("Submit Appeal Form", "Appeals Committee Review", ""),
        ("Appeals Committee Review", "Receive Appeal Decision", ""),
        ("Receive Appeal Decision", "Graduated or Withdrawn?", ""),
        ("Has Grievance?", "Graduated or Withdrawn?", "No"),
        
        # Loop back for next semester
        ("Graduated or Withdrawn?", "Begin Classes", "No"),
        ("Graduated or Withdrawn?", "End", "Yes"),
    ],
    
    "layout": {
        # Application Phase (columns 0-5)
        "Start": 0,
        "Submit Application": 1,
        "Review Application": 2,
        "Documents Complete?": 3,
        "Notify Missing Documents": 4,
        "Resubmit Documents": 5,
        
        # Evaluation Phase (columns 6-9)
        "Fork Evaluation": 6,
        "Evaluate Application": 7,
        "Process Fees Waivers": 7,
        "Join Evaluation": 8,
        "Application Accepted?": 9,
        
        # Decision outputs (column 10-11) - auto-stacked in same lane
        "Send Rejection Letter": 10,
        "Send Acceptance Letter": 10,
        "End Rejected": 11,
        
        # Confirmation (columns 11-14)
        "Confirm Enrollment": 11,
        "Confirmed by Deadline?": 12,
        "Cancel Application": 13,
        "Fork Onboarding": 13,
        "End Cancelled": 14,
        
        # Onboarding parallel (columns 14-16)
        "Send Orientation Materials": 14,
        "Setup Student Accounts": 14,
        "Is International?": 14,
        "Process Visa": 15,
        "Join Onboarding": 16,
        
        # Study Plan (columns 17-21)
        "Get Student ID Card": 17,
        "Meet Academic Advisor": 18,
        "Select Courses": 19,
        "Schedule Conflicts?": 20,
        "Resolve Conflicts": 21,
        
        # Semester Activities (columns 22-25)
        "Begin Classes": 22,
        "Add Drop Courses": 23,
        "Post Grades": 24,
        "Review Grades": 25,
        
        # Appeals (columns 26-29)
        "Has Grievance?": 26,
        "Submit Appeal Form": 27,
        "Appeals Committee Review": 28,
        "Receive Appeal Decision": 29,
        
        # Completion (columns 30-31)
        "Graduated or Withdrawn?": 30,
        "End": 31,
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
