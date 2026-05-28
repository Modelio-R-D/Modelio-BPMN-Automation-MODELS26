#
# InternshipProcess.py
#
# Description: Internship application, offer management, status updates, and recommendation process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "InternshipProcess",
    
    "lanes": ["Applicant", "Company", "Twitter"],
    
    "elements": [
        # Applicant starts the process
        ("Start", START, "Applicant"),
        ("Enter Topic and Budget", USER_TASK, "Applicant"),
        ("Enter Experience and Hobbies", USER_TASK, "Applicant"),
        
        # Offer handling
        ("Wait for Offer", MESSAGE_CATCH, "Applicant"),
        ("Review Offer", USER_TASK, "Applicant"),
        ("Accept or Deny?", EXCLUSIVE_GW, "Applicant"),
        ("Deny Offer", USER_TASK, "Applicant"),
        ("More Offers?", EXCLUSIVE_GW, "Applicant"),
        ("Accept Offer", USER_TASK, "Applicant"),
        ("Invalidate Other Offers", SERVICE_TASK, "Applicant"),
        
        # Internship execution - parallel status updates
        ("Start Internship", PARALLEL_GW, "Applicant"),
        
        # Applicant status updates (at least 3 weekly)
        ("Write Status Update 1", USER_TASK, "Applicant"),
        ("Wait 1 Week A1", TIMER_CATCH, "Applicant"),
        ("Write Status Update 2", USER_TASK, "Applicant"),
        ("Wait 1 Week A2", TIMER_CATCH, "Applicant"),
        ("Write Status Update 3", USER_TASK, "Applicant"),
        
        # Company status updates (3 updates)
        ("Write Company Update 1", USER_TASK, "Company"),
        ("Wait 1 Week C1", TIMER_CATCH, "Company"),
        ("Write Company Update 2", USER_TASK, "Company"),
        ("Wait 1 Week C2", TIMER_CATCH, "Company"),
        ("Write Company Update 3", USER_TASK, "Company"),
        
        # Synchronize completion
        ("Complete Internship", PARALLEL_GW, "Applicant"),
        
        # Recommendation process
        ("Recommend Company?", EXCLUSIVE_GW, "Applicant"),
        ("Select Friends to Notify", USER_TASK, "Applicant"),
        ("Split for Parallel Tweets", PARALLEL_GW, "Twitter"),
        ("Send Tweet to Friend 1", SEND_TASK, "Twitter"),
        ("Send Tweet to Friend 2", SEND_TASK, "Twitter"),
        ("Send Tweet to Friend 3", SEND_TASK, "Twitter"),
        ("Join Tweets", PARALLEL_GW, "Twitter"),
        
        ("End", END, "Applicant"),
    ],
    
    "flows": [
        # Initial application
        ("Start", "Enter Topic and Budget", ""),
        ("Enter Topic and Budget", "Enter Experience and Hobbies", ""),
        ("Enter Experience and Hobbies", "Wait for Offer", ""),
        
        # Offer loop
        ("Wait for Offer", "Review Offer", ""),
        ("Review Offer", "Accept or Deny?", ""),
        ("Accept or Deny?", "Deny Offer", "No"),
        ("Accept or Deny?", "Accept Offer", "Yes"),
        ("Deny Offer", "More Offers?", ""),
        ("More Offers?", "Wait for Offer", "Yes"),
        ("More Offers?", "End", "No"),
        
        # Accept and invalidate
        ("Accept Offer", "Invalidate Other Offers", ""),
        ("Invalidate Other Offers", "Start Internship", ""),
        
        # Parallel split for internship activities
        ("Start Internship", "Write Status Update 1", ""),
        ("Start Internship", "Write Company Update 1", ""),
        
        # Applicant status chain
        ("Write Status Update 1", "Wait 1 Week A1", ""),
        ("Wait 1 Week A1", "Write Status Update 2", ""),
        ("Write Status Update 2", "Wait 1 Week A2", ""),
        ("Wait 1 Week A2", "Write Status Update 3", ""),
        ("Write Status Update 3", "Complete Internship", ""),
        
        # Company status chain
        ("Write Company Update 1", "Wait 1 Week C1", ""),
        ("Wait 1 Week C1", "Write Company Update 2", ""),
        ("Write Company Update 2", "Wait 1 Week C2", ""),
        ("Wait 1 Week C2", "Write Company Update 3", ""),
        ("Write Company Update 3", "Complete Internship", ""),
        
        # Post-internship recommendation
        ("Complete Internship", "Recommend Company?", ""),
        ("Recommend Company?", "Select Friends to Notify", "Yes"),
        ("Recommend Company?", "End", "No"),
        ("Select Friends to Notify", "Split for Parallel Tweets", ""),
        
        # Parallel tweets
        ("Split for Parallel Tweets", "Send Tweet to Friend 1", ""),
        ("Split for Parallel Tweets", "Send Tweet to Friend 2", ""),
        ("Split for Parallel Tweets", "Send Tweet to Friend 3", ""),
        ("Send Tweet to Friend 1", "Join Tweets", ""),
        ("Send Tweet to Friend 2", "Join Tweets", ""),
        ("Send Tweet to Friend 3", "Join Tweets", ""),
        ("Join Tweets", "End", ""),
    ],
    
    "layout": {
        # Application phase
        "Start": 0,
        "Enter Topic and Budget": 1,
        "Enter Experience and Hobbies": 2,
        
        # Offer handling loop
        "Wait for Offer": 3,
        "Review Offer": 4,
        "Accept or Deny?": 5,
        "Deny Offer": 6,
        "Accept Offer": 6,
        "More Offers?": 7,
        "Invalidate Other Offers": 7,
        
        # Internship start
        "Start Internship": 8,
        
        # Applicant updates (columns 9-13)
        "Write Status Update 1": 9,
        "Wait 1 Week A1": 10,
        "Write Status Update 2": 11,
        "Wait 1 Week A2": 12,
        "Write Status Update 3": 13,
        
        # Company updates (columns 9-13, same timing)
        "Write Company Update 1": 9,
        "Wait 1 Week C1": 10,
        "Write Company Update 2": 11,
        "Wait 1 Week C2": 12,
        "Write Company Update 3": 13,
        
        # Completion and recommendation
        "Complete Internship": 14,
        "Recommend Company?": 15,
        "Select Friends to Notify": 16,
        "Split for Parallel Tweets": 17,
        "Send Tweet to Friend 1": 18,
        "Send Tweet to Friend 2": 18,
        "Send Tweet to Friend 3": 18,
        "Join Tweets": 19,
        "End": 20,
    },
    
    "data_objects": [
        ("Application Data", "Applicant", 2),
        ("Offer", "Applicant", 4),
        ("Status Reports", "Applicant", 13),
        ("Company Evaluation", "Company", 13),
    ],
    
    "data_associations": [
        ("Enter Experience and Hobbies", "Application Data"),
        ("Review Offer", "Offer"),
        ("Write Status Update 3", "Status Reports"),
        ("Write Company Update 3", "Company Evaluation"),
    ],
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
