#
# TicketBookingProcess.py
#
# Description: Customer searches and books a travel ticket; system generates and sends ticket, updates inventory,
#              sends pre-travel reminders, then customer completes journey with optional post-travel follow-up.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "TicketBookingProcess",

    "lanes": ["Customer", "Booking System", "Travel Company"],

    "elements": [
        ("Start",                    START,         "Customer"),
        ("Search Tickets",           USER_TASK,     "Customer"),
        ("Select Route/Date/Time",   USER_TASK,     "Customer"),
        ("Enter Personal Info",      USER_TASK,     "Customer"),
        ("Enter Payment Details",    USER_TASK,     "Customer"),

        ("Process Payment",          SERVICE_TASK,  "Booking System"),
        ("Generate Ticket",          SERVICE_TASK,  "Booking System"),

        ("Parallel Split",           PARALLEL_GW,   "Booking System"),
        ("Update Seat Inventory",    SERVICE_TASK,  "Travel Company"),

        ("Send Channel?",            EXCLUSIVE_GW,  "Booking System"),
        ("Email Ticket",             SEND_TASK,     "Booking System"),
        ("SMS Ticket",               SEND_TASK,     "Booking System"),
        ("Ticket Received",          RECEIVE_TASK,  "Customer"),

        ("Parallel Join",            PARALLEL_GW,   "Booking System"),

        ("Reminder Timer",           TIMER_CATCH,   "Booking System"),
        ("Send Reminder/Instructions", SEND_TASK,   "Booking System"),

        ("Check In / Board",         USER_TASK,     "Customer"),
        ("Complete Journey",         USER_TASK,     "Customer"),

        ("Post-Travel Follow-up?",   EXCLUSIVE_GW,  "Customer"),
        ("Collect Feedback",         USER_TASK,     "Customer"),
        ("Provide Post-Travel Service", SERVICE_TASK, "Travel Company"),

        ("End",                      END,           "Customer"),
    ],

    "data_objects": [
        ("Ticket", "Booking System", 6),
    ],

    "data_associations": [
        ("Generate Ticket", "Ticket"),
        ("Ticket", "Email Ticket"),
        ("Ticket", "SMS Ticket"),
        ("Ticket", "Ticket Received"),
    ],

    "flows": [
        ("Start",                  "Search Tickets",             ""),
        ("Search Tickets",         "Select Route/Date/Time",     ""),
        ("Select Route/Date/Time", "Enter Personal Info",        ""),
        ("Enter Personal Info",    "Enter Payment Details",      ""),
        ("Enter Payment Details",  "Process Payment",            ""),
        ("Process Payment",        "Generate Ticket",            ""),

        ("Generate Ticket",        "Parallel Split",             ""),

        ("Parallel Split",         "Send Channel?",              ""),
        ("Parallel Split",         "Update Seat Inventory",      ""),

        ("Send Channel?",          "Email Ticket",               "Email"),
        ("Send Channel?",          "SMS Ticket",                 "SMS"),

        ("Email Ticket",           "Ticket Received",            ""),
        ("SMS Ticket",             "Ticket Received",            ""),

        ("Ticket Received",        "Parallel Join",              ""),
        ("Update Seat Inventory",  "Parallel Join",              ""),

        ("Parallel Join",          "Reminder Timer",             ""),
        ("Reminder Timer",         "Send Reminder/Instructions", ""),
        ("Send Reminder/Instructions", "Check In / Board",       ""),
        ("Check In / Board",       "Complete Journey",           ""),

        ("Complete Journey",       "Post-Travel Follow-up?",     ""),
        ("Post-Travel Follow-up?", "Collect Feedback",           "Yes"),
        ("Post-Travel Follow-up?", "End",                        "No"),

        ("Collect Feedback",       "End",                        ""),
        ("Provide Post-Travel Service", "End",                   ""),
    ],

    "layout": {
        "Start":                      0,
        "Search Tickets":             1,
        "Select Route/Date/Time":     2,
        "Enter Personal Info":        3,
        "Enter Payment Details":      4,

        "Process Payment":            5,
        "Generate Ticket":            6,

        "Parallel Split":             7,
        "Send Channel?":              8,
        "Update Seat Inventory":      8,

        "Email Ticket":               9,
        "SMS Ticket":                 9,   # auto-stacked (same lane, same column)

        "Ticket Received":            10,
        "Parallel Join":              11,

        "Reminder Timer":             12,
        "Send Reminder/Instructions": 13,

        "Check In / Board":           14,
        "Complete Journey":           15,

        "Post-Travel Follow-up?":     16,
        "Collect Feedback":           17,
        "Provide Post-Travel Service": 17,

        "End":                        18,
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
