#
# FindAJob.py
#
# Description: BPMN diagram for job application process - regular reporting,
#              job offers, interview negotiation, probation phase, and mutual rating.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Find a Job",
    
    "lanes": ["Applicant", "Company"],
    
    "elements": [
        # Regular reporting triggered by timer
        ("Start", TIMER_START, "Applicant"),
        ("Report Applications", USER_TASK, "Applicant"),
        ("Receive Job Offers", RECEIVE_TASK, "Applicant"),
        ("Submit Application", USER_TASK, "Applicant"),
        
        # Company processing
        ("Confirm & Rate", SERVICE_TASK, "Company"),
        
        # Interview negotiation
        ("Schedule Interview", USER_TASK, "Applicant"),
        ("Confirm Interview", USER_TASK, "Company"),
        
        # Company decision
        ("Offer Decision", EXCLUSIVE_GW, "Company"),
        ("No Offer", END, "Company"),
        ("Probation Phase", USER_TASK, "Company"),
        
        # Parallel rating after probation
        ("Rate Split", PARALLEL_GW, "Company"),
        ("Rate Company", USER_TASK, "Applicant"),
        ("Rate Employee", USER_TASK, "Company"),
        ("Rate Join", PARALLEL_GW, "Applicant"),
        
        # Final decisions
        ("Rating Acceptable?", EXCLUSIVE_GW, "Applicant"),
        ("Continue Offers", END, "Applicant"),
        ("Permanent Position?", EXCLUSIVE_GW, "Applicant"),
        ("Not Permanent", END, "Applicant"),
        ("Job Accepted", END, "Applicant"),
    ],
    
    "flows": [
        # Initial flow
        ("Start", "Report Applications", ""),
        ("Report Applications", "Receive Job Offers", ""),
        ("Receive Job Offers", "Submit Application", ""),
        
        # Application processing
        ("Submit Application", "Confirm & Rate", ""),
        ("Confirm & Rate", "Schedule Interview", ""),
        
        # Interview coordination
        ("Schedule Interview", "Confirm Interview", ""),
        ("Confirm Interview", "Offer Decision", ""),
        
        # Offer decision gateway
        ("Offer Decision", "No Offer", "No"),
        ("Offer Decision", "Probation Phase", "Yes"),
        
        # Parallel rating
        ("Probation Phase", "Rate Split", ""),
        ("Rate Split", "Rate Company", ""),
        ("Rate Split", "Rate Employee", ""),
        ("Rate Company", "Rate Join", ""),
        ("Rate Employee", "Rate Join", ""),
        
        # Rating evaluation
        ("Rate Join", "Rating Acceptable?", ""),
        ("Rating Acceptable?", "Continue Offers", "C or Less"),
        ("Rating Acceptable?", "Permanent Position?", "OK"),
        
        # Final outcome
        ("Permanent Position?", "Not Permanent", "No"),
        ("Permanent Position?", "Job Accepted", "Yes"),
    ],
    
    "layout": {
        "Start": 0,
        "Report Applications": 1,
        "Receive Job Offers": 2,
        "Submit Application": 3,
        "Confirm & Rate": 4,
        "Schedule Interview": 5,
        "Confirm Interview": 6,
        "Offer Decision": 7,
        "No Offer": 8,
        "Probation Phase": 8,
        "Rate Split": 9,
        "Rate Company": 10,
        "Rate Employee": 10,
        "Rate Join": 11,
        "Rating Acceptable?": 12,
        "Continue Offers": 13,
        "Permanent Position?": 13,
        "Not Permanent": 14,
        "Job Accepted": 14,
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
