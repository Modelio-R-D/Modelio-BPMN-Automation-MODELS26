CONFIG = {
    "name": "Internship",
    "lanes": ["Intern", "Company", "Twitter"],
    "elements": [
        # Start
        ("Start", START, "Intern"),
        
        # Profile entry
        ("Enter Profile", USER_TASK, "Intern"),  # topic, money, experience, hobbies
        
        # Offer process
        ("Wait for Offers", MESSAGE_CATCH, "Intern"),  # waiting state
        ("Send Offer", SEND_TASK, "Company"),
        ("Receive Offer", RECEIVE_TASK, "Intern"),
        ("Review Offer", USER_TASK, "Intern"),
        ("Accept?", EXCLUSIVE_GW, "Intern"),
        ("Reject Offer", USER_TASK, "Intern"),
        ("Confirm Acceptance", SERVICE_TASK, "Intern"),
        
        # Internship - parallel updates
        ("Start Internship", PARALLEL_GW, "Intern"),
        
        # Intern updates
        ("Write Status 1", USER_TASK, "Intern"),
        ("Write Status 2", USER_TASK, "Intern"),
        ("Write Status 3", USER_TASK, "Intern"),
        
        # Company updates
        ("Report on Intern 1", USER_TASK, "Company"),
        ("Report on Intern 2", USER_TASK, "Company"),
        ("Report on Intern 3", USER_TASK, "Company"),
        
        # End internship
        ("Finish Internship", PARALLEL_GW, "Intern"),  # join
        
        # Recommendation
        ("Recommend Company", USER_TASK, "Intern"),
        
        # Twitter posts (parallel)
        ("Tweet", PARALLEL_GW, "Intern"),
        ("Post Tweet 1", SERVICE_TASK, "Twitter"),
        ("Post Tweet 2", SERVICE_TASK, "Twitter"),
        ("Post Tweet 3", SERVICE_TASK, "Twitter"),
        ("Done", PARALLEL_GW, "Twitter"),
        
        # End
        ("End", END, "Intern"),
    ],
    
    "flows": [...]
}


"elements": [
    ("Start", START, "Intern"),
    ("Enter Profile", USER_TASK, "Intern"),
    ("Send Offer", SEND_TASK, "Company"),
    ("Receive Offer", RECEIVE_TASK, "Intern"),
    ("Review Offer", USER_TASK, "Intern"),
    ("Accept?", EXCLUSIVE_GW, "Intern"),
    ("Reject Offer", USER_TASK, "Intern"),
    ("Confirm Acceptance", USER_TASK, "Intern"),
    ("Start Internship", PARALLEL_GW, "Intern"),  # Split
    # Branch 1: Intern updates
    ("Write Update 1", USER_TASK, "Intern"),
    ("Write Update 2", USER_TASK, "Intern"),
    ("Write Update 3", USER_TASK, "Intern"),
    ("Intern Done", USER_TASK, "Intern"),  # Just a marker
    # Branch 2: Company updates (crossing lanes)
    ("Write Report 1", USER_TASK, "Company"),
    ("Write Report 2", USER_TASK, "Company"),
    ("Write Report 3", USER_TASK, "Company"),
    # Join
    ("Internship Complete", PARALLEL_GW, "Intern"),  # Join
    ("Recommend Company", USER_TASK, "Intern"),
    ("Send Tweets", PARALLEL_GW, "Intern"),  # Split for tweets
    ("Tweet 1", SERVICE_TASK, "Twitter"),
    ("Tweet 2", SERVICE_TASK, "Twitter"),
    ("Tweet 3", SERVICE_TASK, "Twitter"),
    ("Tweets Done", PARALLEL_GW, "Twitter"),  # Join
    ("End", END, "Intern"),
],


"flows": [
    ("Start", "Enter Profile", ""),
    ("Enter Profile", "Receive Offer", ""),  # Implicit wait
    # Company sends offer which triggers receive
    ("Send Offer", "Receive Offer", "Offer"),
    ("Receive Offer", "Review Offer", ""),
    ("Review Offer", "Accept?", ""),
    ("Accept?", "Reject Offer", "No"),
    ("Reject Offer", "Receive Offer", ""),
    ("Accept?", "Confirm Acceptance", "Yes"),
    ("Confirm Acceptance", "Start Internship", ""),
    # Parallel split
    ("Start Internship", "Write Update 1", ""),
    ("Start Internship", "Write Report 1", ""),
    # Intern branch
    ("Write Update 1", "Write Update 2", ""),
    ("Write Update 2", "Write Update 3", ""),
    ("Write Update 3", "Internship Complete", ""),
    # Company branch
    ("Write Report 1", "Write Report 2", ""),
    ("Write Report 2", "Write Report 3", ""),
    ("Write Report 3", "Internship Complete", ""),
    # After parallel join
    ("Internship Complete", "Recommend Company", ""),
    ("Recommend Company", "Send Tweets", ""),
    # Tweet parallel split
    ("Send Tweets", "Tweet 1", ""),
    ("Send Tweets", "Tweet 2", ""),
    ("Send Tweets", "Tweet 3", ""),
    # Tweet parallel join
    ("Tweet 1", "Tweets Done", ""),
    ("Tweet 2", "Tweets Done", ""),
    ("Tweet 3", "Tweets Done", ""),
    ("Tweets Done", "End", ""),
],


CONFIG = {
    "name": "InternshipProcess",
    "lanes": ["Intern", "Company", "Twitter"],
    
    "elements": [
        # Start
        ("Start", START, "Intern"),
        
        # Profile setup
        ("Enter Profile", USER_TASK, "Intern"),
        
        # Offer process
        ("Send Offer", SEND_TASK, "Company"),
        ("Receive Offer", RECEIVE_TASK, "Intern"),
        ("Review Offer", USER_TASK, "Intern"),
        ("Accept?", EXCLUSIVE_GW, "Intern"),
        ("Reject Offer", USER_TASK, "Intern"),
        ("Confirm Acceptance", USER_TASK, "Intern"),
        
        # Internship - parallel split
        ("Start Internship", PARALLEL_GW, "Intern"),
        
        # Intern updates (branch 1)
        ("Write Update 1", USER_TASK, "Intern"),
        ("Write Update 2", USER_TASK, "Intern"),
        ("Write Update 3", USER_TASK, "Intern"),
        
        # Company reports (branch 2)
        ("Write Report 1", USER_TASK, "Company"),
        ("Write Report 2", USER_TASK, "Company"),
        ("Write Report 3", USER_TASK, "Company"),
        
        # Internship end - parallel join
        ("Internship Complete", PARALLEL_GW, "Intern"),
        
        # Recommendation
        ("Recommend Company", USER_TASK, "Intern"),
        
        # Tweets - parallel split
        ("Send Tweets", PARALLEL_GW, "Intern"),
        ("Post Tweet 1", SERVICE_TASK, "Twitter"),
        ("Post Tweet 2", SERVICE_TASK, "Twitter"),
        ("Post Tweet 3", SERVICE_TASK, "Twitter"),
        ("Tweets Complete", PARALLEL_GW, "Twitter"),
        
        # End
        ("End", END, "Intern"),
    ],
    
    "flows": [
        ("Start", "Enter Profile", ""),
        ("Enter Profile", "Send Offer", ""),  # Triggers company to send offer
        ("Enter Profile", "Receive Offer", ""),  # Intern waits for offers
        ("Send Offer", "Receive Offer", "Offer"),
        ("Receive Offer", "Review Offer", ""),
        ("Review Offer", "Accept?", ""),
        ("Accept?", "Reject Offer", "No"),
        ("Reject Offer", "Receive Offer", ""),  # Loop back
        ("Accept?", "Confirm Acceptance", "Yes"),
        ("Confirm Acceptance", "Start Internship", ""),
        
        # Parallel split for internship
        ("Start Internship", "Write Update 1", ""),
        ("Start Internship", "Write Report 1", ""),
        
        # Intern branch
        ("Write Update 1", "Write Update 2", ""),
        ("Write Update 2", "Write Update 3", ""),
        ("Write Update 3", "Internship Complete", ""),
        
        # Company branch
        ("Write Report 1", "Write Report 2", ""),
        ("Write Report 2", "Write Report 3", ""),
        ("Write Report 3", "Internship Complete", ""),
        
        # After internship
        ("Internship Complete", "Recommend Company", ""),
        ("Recommend Company", "Send Tweets", ""),
        
        # Parallel tweets
        ("Send Tweets", "Post Tweet 1", ""),
        ("Send Tweets", "Post Tweet 2", ""),
        ("Send Tweets", "Post Tweet 3", ""),
        ("Post Tweet 1", "Tweets Complete", ""),
        ("Post Tweet 2", "Tweets Complete", ""),
        ("Post Tweet 3", "Tweets Complete", ""),
        ("Tweets Complete", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Enter Profile": 1,
        "Send Offer": 2,
        "Receive Offer": 2,
        "Review Offer": 3,
        "Accept?": 4,
        "Reject Offer": 5,
        "Confirm Acceptance": 5,  # Stacked with Reject (same column, same lane)
        "Start Internship": 6,
        "Write Update 1": 7,
        "Write Report 1": 7,
        "Write Update 2": 8,
        "Write Report 2": 8,
        "Write Update 3": 9,
        "Write Report 3": 9,
        "Internship Complete": 10,
        "Recommend Company": 11,
        "Send Tweets": 12,
        "Post Tweet 1": 13,
        "Post Tweet 2": 13,  # Stacked
        "Post Tweet 3": 13,  # Stacked
        "Tweets Complete": 14,
        "End": 15,
    },
    
    "data_objects": [
        ("Profile", "Intern", 1),
        ("Offer", "Company", 2),
        ("Acceptance", "Intern", 5),
        ("Updates", "Intern", 9),
        ("Reports", "Company", 9),
    ],
    
    "data_associations": [
        ("Enter Profile", "Profile"),
        ("Profile", "Send Offer"),  # Company sees profile
        ("Send Offer", "Offer"),
        ("Offer", "Receive Offer"),
        ("Confirm Acceptance", "Acceptance"),
        ("Write Update 3", "Updates"),
        ("Write Report 3", "Reports"),
    ],
}


"elements": [
    ("Start", START, "Intern"),
    ("Enter Profile", USER_TASK, "Intern"),
    ("Profile Ready", PARALLEL_GW, "Intern"),  # Split
    ("Wait for Offer", RECEIVE_TASK, "Intern"),
    ("Send Offer", SEND_TASK, "Company"),
    ("Offer Received", RECEIVE_TASK, "Intern"),  # Hmm, this is confusing
    ...
]


"elements": [
    ("Start", START, "Intern"),
    ("Enter Profile", USER_TASK, "Intern"),
    ("Send Offer", SEND_TASK, "Company"),  # Can happen after profile is available
    ("Receive Offer", RECEIVE_TASK, "Intern"),  # Receives the offer
    ("Review Offer", USER_TASK, "Intern"),
    ("Accept?", EXCLUSIVE_GW, "Intern"),
    ("Reject Offer", USER_TASK, "Intern"),
    ("Confirm Acceptance", USER_TASK, "Intern"),
    ...
],
"flows": [
    ("Start", "Enter Profile", ""),
    ("Enter Profile", "Receive Offer", ""),  # Intern waits for offer
    ("Send Offer", "Receive Offer", "Offer"),  # Message from company
    ("Receive Offer", "Review Offer", ""),
    ("Review Offer", "Accept?", ""),
    ("Accept?", "Reject Offer", "No"),
    ("Reject Offer", "Receive Offer", ""),  # Wait for another offer
    ("Accept?", "Confirm Acceptance", "Yes"),
    ...
],


"flows": [
    ("Start", "Enter Profile", ""),
    ("Enter Profile", "Send Offer", ""),  # Crosses to Company lane
    ("Send Offer", "Receive Offer", ""),  # Crosses back to Intern lane
    ...
],


#
# Internship.py
#
# Description: Internship process with offers, status updates, and Twitter recommendations
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Internship",
    
    "lanes": ["Intern", "Company", "Twitter"],
    
    "elements": [
        # Start
        ("Start", START, "Intern"),
        
        # Profile setup
        ("Enter Profile", USER_TASK, "Intern"),
        
        # Offer process
        ("Send Offer", SEND_TASK, "Company"),
        ("Receive Offer", RECEIVE_TASK, "Intern"),
        ("Review Offer", USER_TASK, "Intern"),
        ("Accept?", EXCLUSIVE_GW, "Intern"),
        ("Reject Offer", USER_TASK, "Intern"),
        ("Confirm Acceptance", USER_TASK, "Intern"),
        
        # Internship - parallel activities
        ("Start Internship", PARALLEL_GW, "Intern"),
        
        # Intern updates (branch 1)
        ("Write Update 1", USER_TASK, "Intern"),
        ("Write Update 2", USER_TASK, "Intern"),
        ("Write Update 3", USER_TASK, "Intern"),
        
        # Company reports (branch 2)
        ("Write Report 1", USER_TASK, "Company"),
        ("Write Report 2", USER_TASK, "Company"),
        ("Write Report 3", USER_TASK, "Company"),
        
        # Internship complete - join
        ("Internship Complete", PARALLEL_GW, "Intern"),
        
        # Recommendation
        ("Recommend Company", USER_TASK, "Intern"),
        
        # Twitter posts (parallel)
        ("Send Tweets", PARALLEL_GW, "Intern"),
        ("Post Tweet 1", SERVICE_TASK, "Twitter"),
        ("Post Tweet 2", SERVICE_TASK, "Twitter"),
        ("Post Tweet 3", SERVICE_TASK, "Twitter"),
        ("Tweets Complete", PARALLEL_GW, "Twitter"),
        
        # End
        ("End", END, "Intern"),
    ],
    
    "flows": [
        # Start and profile
        ("Start", "Enter Profile", ""),
        ("Enter Profile", "Send Offer", ""),
        ("Send Offer", "Receive Offer", "Offer"),
        
        # Offer review
        ("Receive Offer", "Review Offer", ""),
        ("Review Offer", "Accept?", ""),
        
        # Decision
        ("Accept?", "Reject Offer", "No"),
        ("Reject Offer", "Receive Offer", ""),
        ("Accept?", "Confirm Acceptance", "Yes"),
        
        # Start internship
        ("Confirm Acceptance", "Start Internship", ""),
        
        # Parallel internship tasks
        ("Start Internship", "Write Update 1", ""),
        ("Start Internship", "Write Report 1", ""),
        
        # Intern updates
        ("Write Update 1", "Write Update 2", ""),
        ("Write Update 2", "Write Update 3", ""),
        ("Write Update 3", "Internship Complete", ""),
        
        # Company reports
        ("Write Report 1", "Write Report 2", ""),
        ("Write Report 2", "Write Report 3", ""),
        ("Write Report 3", "Internship Complete", ""),
        
        # Recommendation and tweets
        ("Internship Complete", "Recommend Company", ""),
        ("Recommend Company", "Send Tweets", ""),
        
        # Parallel tweets
        ("Send Tweets", "Post Tweet 1", ""),
        ("Send Tweets", "Post Tweet 2", ""),
        ("Send Tweets", "Post Tweet 3", ""),
        ("Post Tweet 1", "Tweets Complete", ""),
        ("Post Tweet 2", "Tweets Complete", ""),
        ("Post Tweet 3", "Tweets Complete", ""),
        ("Tweets Complete", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Enter Profile": 1,
        "Send Offer": 2,
        "Receive Offer": 3,
        "Review Offer": 4,
        "Accept?": 5,
        "Reject Offer": 6,
        "Confirm Acceptance": 6,
        "Start Internship": 7,
        "Write Update 1": 8,
        "Write Report 1": 8,
        "Write Update 2": 9,
        "Write Report 2": 9,
        "Write Update 3": 10,
        "Write Report 3": 10,
        "Internship Complete": 11,
        "Recommend Company": 12,
        "Send Tweets": 13,
        "Post Tweet 1": 14,
        "Post Tweet 2": 14,
        "Post Tweet 3": 14,
        "Tweets Complete": 15,
        "End": 16,
    },
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."


"data_objects": [
    ("Profile", "Intern", 1),
    ("Offer", "Intern", 3),
    ("Acceptance", "Intern", 6),
    ("Recommendation", "Intern", 12),
],

"data_associations": [
    ("Enter Profile", "Profile"),
    ("Send Offer", "Offer"),
    ("Offer", "Receive Offer"),
    ("Confirm Acceptance", "Acceptance"),
    ("Recommend Company", "Recommendation"),
],


"data_objects": [
    ("Profile", "Intern", 1),
    ("Offer", "Company", 2),  # Created by Company
    ("Acceptance", "Intern", 6),
],

"data_associations": [
    ("Enter Profile", "Profile"),
    ("Profile", "Send Offer", ""),  # Company sees profile
    ("Send Offer", "Offer"),  # Company creates offer
    ("Offer", "Receive Offer"),  # Intern receives offer
    ("Confirm Acceptance", "Acceptance"),
],


"data_objects": [
    ("Profile", "Intern", 1),
    ("Offer", "Company", 2),
    ("Acceptance", "Intern", 6),
    ("Intern Updates", "Intern", 10),
    ("Company Reports", "Company", 10),
],


"data_objects": [
    ("Profile", "Intern", 1),
    ("Offer", "Company", 2),
],

"data_associations": [
    ("Enter Profile", "Profile"),
    ("Send Offer", "Offer"),
],


#
# Internship.py
#
# Description: Internship process with offers, status updates, and Twitter recommendations
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Internship",
    
    "lanes": ["Intern", "Company", "Twitter"],
    
    "elements": [
        # Start
        ("Start", START, "Intern"),
        
        # Profile setup
        ("Enter Profile", USER_TASK, "Intern"),
        
        # Offer process
        ("Send Offer", SEND_TASK, "Company"),
        ("Receive Offer", RECEIVE_TASK, "Intern"),
        ("Review Offer", USER_TASK, "Intern"),
        ("Accept?", EXCLUSIVE_GW, "Intern"),
        ("Reject Offer", USER_TASK, "Intern"),
        ("Confirm Acceptance", USER_TASK, "Intern"),
        
        # Internship - parallel activities
        ("Start Internship", PARALLEL_GW, "Intern"),
        
        # Intern updates
        ("Write Update 1", USER_TASK, "Intern"),
        ("Write Update 2", USER_TASK, "Intern"),
        ("Write Update 3", USER_TASK, "Intern"),
        
        # Company reports
        ("Write Report 1", USER_TASK, "Company"),
        ("Write Report 2", USER_TASK, "Company"),
        ("Write Report 3", USER_TASK, "Company"),
        
        # Internship complete
        ("Internship Complete", PARALLEL_GW, "Intern"),
        
        # Recommendation
        ("Recommend Company", USER_TASK, "Intern"),
        
        # Twitter posts
        ("Send Tweets", PARALLEL_GW, "Intern"),
        ("Post Tweet 1", SERVICE_TASK, "Twitter"),
        ("Post Tweet 2", SERVICE_TASK, "Twitter"),
        ("Post Tweet 3", SERVICE_TASK, "Twitter"),
        ("Tweets Complete", PARALLEL_GW, "Twitter"),
        
        # End
        ("End", END, "Intern"),
    ],
    
    "flows": [
        ("Start", "Enter Profile", ""),
        ("Enter Profile", "Send Offer", ""),
        ("Send Offer", "Receive Offer", "Offer"),
        ("Receive Offer", "Review Offer", ""),
        ("Review Offer", "Accept?", ""),
        ("Accept?", "Reject Offer", "No"),
        ("Reject Offer", "Receive Offer", ""),
        ("Accept?", "Confirm Acceptance", "Yes"),
        ("Confirm Acceptance", "Start Internship", ""),
        ("Start Internship", "Write Update 1", ""),
        ("Start Internship", "Write Report 1", ""),
        ("Write Update 1", "Write Update 2", ""),
        ("Write Update 2", "Write Update 3", ""),
        ("Write Update 3", "Internship Complete", ""),
        ("Write Report 1", "Write Report 2", ""),
        ("Write Report 2", "Write Report 3", ""),
        ("Write Report 3", "Internship Complete", ""),
        ("Internship Complete", "Recommend Company", ""),
        ("Recommend Company", "Send Tweets", ""),
        ("Send Tweets", "Post Tweet 1", ""),
        ("Send Tweets", "Post Tweet 2", ""),
        ("Send Tweets", "Post Tweet 3", ""),
        ("Post Tweet 1", "Tweets Complete", ""),
        ("Post Tweet 2", "Tweets Complete", ""),
        ("Post Tweet 3", "Tweets Complete", ""),
        ("Tweets Complete", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Enter Profile": 1,
        "Send Offer": 2,
        "Receive Offer": 3,
        "Review Offer": 4,
        "Accept?": 5,
        "Reject Offer": 6,
        "Confirm Acceptance": 6,
        "Start Internship": 7,
        "Write Update 1": 8,
        "Write Report 1": 8,
        "Write Update 2": 9,
        "Write Report 2": 9,
        "Write Update 3": 10,
        "Write Report 3": 10,
        "Internship Complete": 11,
        "Recommend Company": 12,
        "Send Tweets": 13,
        "Post Tweet 1": 14,
        "Post Tweet 2": 14,
        "Post Tweet 3": 14,
        "Tweets Complete": 15,
        "End": 16,
    },
    
    "data_objects": [
        ("Profile", "Intern", 1),
        ("Offer", "Company", 2),
    ],
    
    "data_associations": [
        ("Enter Profile", "Profile"),
        ("Send Offer", "Offer"),
    ],
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."


#
# Internship.py
#
# Description: Internship process with profile entry, offer handling, status updates, and Twitter recommendations
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Internship",
    
    "lanes": ["Intern", "Company", "Twitter"],
    
    "elements": [
        # Start
        ("Start", START, "Intern"),
        
        # Profile entry - topic, money, experience, hobbies
        ("Enter Profile", USER_TASK, "Intern"),
        
        # Offer process
        ("Send Offer", SEND_TASK, "Company"),
        ("Receive Offer", RECEIVE_TASK, "Intern"),
        ("Review Offer", USER_TASK, "Intern"),
        ("Accept?", EXCLUSIVE_GW, "Intern"),
        ("Reject Offer", USER_TASK, "Intern"),
        ("Confirm Acceptance", USER_TASK, "Intern"),
        
        # Internship - parallel activities (Intern updates || Company reports)
        ("Start Internship", PARALLEL_GW, "Intern"),
        
        # Intern weekly updates (3 weeks)
        ("Write Update 1", USER_TASK, "Intern"),
        ("Write Update 2", USER_TASK, "Intern"),
        ("Write Update 3", USER_TASK, "Intern"),
        
        # Company status reports (3 weeks)
        ("Write Report 1", USER_TASK, "Company"),
        ("Write Report 2", USER_TASK, "Company"),
        ("Write Report 3", USER_TASK, "Company"),
        
        # Internship complete
        ("Internship Complete", PARALLEL_GW, "Intern"),
        
        # Recommendation
        ("Recommend Company", USER_TASK, "Intern"),
        
        # Twitter posts - parallel tweets
        ("Send Tweets", PARALLEL_GW, "Intern"),
        ("Post Tweet 1", SERVICE_TASK, "Twitter"),
        ("Post Tweet 2", SERVICE_TASK, "Twitter"),
        ("Post Tweet 3", SERVICE_TASK, "Twitter"),
        ("Tweets Complete", PARALLEL_GW, "Twitter"),
        
        # End
        ("End", END, "Intern"),
    ],
    
    "flows": [
        # Profile entry
        ("Start", "Enter Profile", ""),
        ("Enter Profile", "Send Offer", ""),
        
        # Offer handling
        ("Send Offer", "Receive Offer", "Offer"),
        ("Receive Offer", "Review Offer", ""),
        ("Review Offer", "Accept?", ""),
        
        # Accept/Reject decision
        ("Accept?", "Reject Offer", "No"),
        ("Reject Offer", "Receive Offer", ""),      # Loop back for next offer
        ("Accept?", "Confirm Acceptance", "Yes"),
        
        # Start internship (other offers become invalid)
        ("Confirm Acceptance", "Start Internship", ""),
        
        # Parallel: Intern updates AND Company reports
        ("Start Internship", "Write Update 1", ""),
        ("Start Internship", "Write Report 1", ""),
        
        # Intern updates sequence
        ("Write Update 1", "Write Update 2", ""),
        ("Write Update 2", "Write Update 3", ""),
        ("Write Update 3", "Internship Complete", ""),
        
        # Company reports sequence
        ("Write Report 1", "Write Report 2", ""),
        ("Write Report 2", "Write Report 3", ""),
        ("Write Report 3", "Internship Complete", ""),
        
        # After internship
        ("Internship Complete", "Recommend Company", ""),
        ("Recommend Company", "Send Tweets", ""),
        
        # Parallel tweets to friends
        ("Send Tweets", "Post Tweet 1", ""),
        ("Send Tweets", "Post Tweet 2", ""),
        ("Send Tweets", "Post Tweet 3", ""),
        ("Post Tweet 1", "Tweets Complete", ""),
        ("Post Tweet 2", "Tweets Complete", ""),
        ("Post Tweet 3", "Tweets Complete", ""),
        ("Tweets Complete", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Enter Profile": 1,
        "Send Offer": 2,
        "Receive Offer": 3,
        "Review Offer": 4,
        "Accept?": 5,
        "Reject Offer": 6,
        "Confirm Acceptance": 6,      # Auto-stacked with Reject Offer
        "Start Internship": 7,
        "Write Update 1": 8,
        "Write Report 1": 8,          # Different lane - no stacking needed
        "Write Update 2": 9,
        "Write Report 2": 9,
        "Write Update 3": 10,
        "Write Report 3": 10,
        "Internship Complete": 11,
        "Recommend Company": 12,
        "Send Tweets": 13,
        "Post Tweet 1": 14,
        "Post Tweet 2": 14,           # Auto-stacked in Twitter lane
        "Post Tweet 3": 14,           # Auto-stacked in Twitter lane
        "Tweets Complete": 15,
        "End": 16,
    },
    
    "data_objects": [
        ("Profile", "Intern", 1),
        ("Offer", "Company", 2),
    ],
    
    "data_associations": [
        ("Enter Profile", "Profile"),
        ("Send Offer", "Offer"),
    ],
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
