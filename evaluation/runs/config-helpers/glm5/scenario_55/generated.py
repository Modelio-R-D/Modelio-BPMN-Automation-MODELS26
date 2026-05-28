#
# CatheterInsertionProcess.py
#
# Description: Medical catheter insertion procedure with vein identification, 
#              puncture, guidewire installation, and catheter placement
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CatheterInsertionProcess",
    
    "lanes": ["Doctor"],
    
    "elements": [
        # Preparation phase
        ("Start",                    START,        "Doctor"),
        ("Prepare implements",       USER_TASK,    "Doctor"),
        ("Wash hands",               USER_TASK,    "Doctor"),
        ("Get in sterile clothes",   USER_TASK,    "Doctor"),
        ("Clean puncture area",      USER_TASK,    "Doctor"),
        ("Drape puncture zone",      USER_TASK,    "Doctor"),
        ("Configure ultrasound",     USER_TASK,    "Doctor"),
        ("Put gel in probe",         USER_TASK,    "Doctor"),
        ("Cover probe",              USER_TASK,    "Doctor"),
        ("Put sterile gel",          USER_TASK,    "Doctor"),
        ("Position probe",           USER_TASK,    "Doctor"),
        ("Position patient",         USER_TASK,    "Doctor"),
        
        # Vein identification (XOR branch)
        ("Identify vein",            EXCLUSIVE_GW, "Doctor"),
        ("Anatomic identification",  USER_TASK,    "Doctor"),
        ("Doppler identification",   USER_TASK,    "Doctor"),
        ("Compression identification", USER_TASK,  "Doctor"),
        ("Vein identified",          EXCLUSIVE_GW, "Doctor"),
        
        # Puncture phase
        ("Anesthetize patient",      USER_TASK,    "Doctor"),
        ("Puncture",                 USER_TASK,    "Doctor"),
        ("Check blood return",       USER_TASK,    "Doctor"),
        ("Blood return correct?",    EXCLUSIVE_GW, "Doctor"),
        
        # Guidewire phase
        ("Drop probe",               USER_TASK,    "Doctor"),
        ("Remove syringe",           USER_TASK,    "Doctor"),
        ("Install guidewire",        USER_TASK,    "Doctor"),
        ("Remove trocar",            USER_TASK,    "Doctor"),
        
        # Wire check (XOR branch)
        ("Check wire",               EXCLUSIVE_GW, "Doctor"),
        ("Check wire long axis",     USER_TASK,    "Doctor"),
        ("Check wire short axis",    USER_TASK,    "Doctor"),
        ("Wire checked",             EXCLUSIVE_GW, "Doctor"),
        ("Wire position good?",      EXCLUSIVE_GW, "Doctor"),
        
        # Catheter placement
        ("Widen pathway",            USER_TASK,    "Doctor"),
        ("Advance catheter",         USER_TASK,    "Doctor"),
        ("Remove guidewire",         USER_TASK,    "Doctor"),
        ("Verify flow and reflow",   USER_TASK,    "Doctor"),
        ("Check catheter position",  USER_TASK,    "Doctor"),
        ("End",                      END,          "Doctor"),
    ],
    
    "flows": [
        # Preparation sequence
        ("Start", "Prepare implements", ""),
        ("Prepare implements", "Wash hands", ""),
        ("Wash hands", "Get in sterile clothes", ""),
        ("Get in sterile clothes", "Clean puncture area", ""),
        ("Clean puncture area", "Drape puncture zone", ""),
        ("Drape puncture zone", "Configure ultrasound", ""),
        ("Configure ultrasound", "Put gel in probe", ""),
        ("Put gel in probe", "Cover probe", ""),
        ("Cover probe", "Put sterile gel", ""),
        ("Put sterile gel", "Position probe", ""),
        ("Position probe", "Position patient", ""),
        ("Position patient", "Identify vein", ""),
        
        # Vein identification branches
        ("Identify vein", "Anatomic identification", "Anatomic"),
        ("Identify vein", "Doppler identification", "Doppler"),
        ("Identify vein", "Compression identification", "Compression"),
        ("Anatomic identification", "Vein identified", ""),
        ("Doppler identification", "Vein identified", ""),
        ("Compression identification", "Vein identified", ""),
        
        # Puncture sequence
        ("Vein identified", "Anesthetize patient", ""),
        ("Anesthetize patient", "Puncture", ""),
        ("Puncture", "Check blood return", ""),
        ("Check blood return", "Blood return correct?", ""),
        
        # Blood return decision
        ("Blood return correct?", "Drop probe", "Yes"),
        ("Blood return correct?", "Puncture", "No"),
        
        # Guidewire sequence
        ("Drop probe", "Remove syringe", ""),
        ("Remove syringe", "Install guidewire", ""),
        ("Install guidewire", "Remove trocar", ""),
        ("Remove trocar", "Check wire", ""),
        
        # Wire check branches
        ("Check wire", "Check wire long axis", "Long axis"),
        ("Check wire", "Check wire short axis", "Short axis"),
        ("Check wire long axis", "Wire checked", ""),
        ("Check wire short axis", "Wire checked", ""),
        
        # Wire position decision
        ("Wire checked", "Wire position good?", ""),
        ("Wire position good?", "Widen pathway", "Yes"),
        ("Wire position good?", "Puncture", "No"),
        
        # Catheter placement sequence
        ("Widen pathway", "Advance catheter", ""),
        ("Advance catheter", "Remove guidewire", ""),
        ("Remove guidewire", "Verify flow and reflow", ""),
        ("Verify flow and reflow", "Check catheter position", ""),
        ("Check catheter position", "End", ""),
    ],
    
    "layout": {
        # Preparation
        "Start":                    0,
        "Prepare implements":       1,
        "Wash hands":               2,
        "Get in sterile clothes":   3,
        "Clean puncture area":      4,
        "Drape puncture zone":      5,
        "Configure ultrasound":     6,
        "Put gel in probe":         7,
        "Cover probe":              8,
        "Put sterile gel":          9,
        "Position probe":           10,
        "Position patient":         11,
        
        # Vein identification
        "Identify vein":            12,
        "Anatomic identification":  13,  # Auto-stacked
        "Doppler identification":   13,  # Auto-stacked
        "Compression identification": 13,  # Auto-stacked
        "Vein identified":          14,
        
        # Puncture
        "Anesthetize patient":      15,
        "Puncture":                 16,
        "Check blood return":       17,
        "Blood return correct?":    18,
        
        # Guidewire
        "Drop probe":               19,
        "Remove syringe":           20,
        "Install guidewire":        21,
        "Remove trocar":            22,
        
        # Wire check
        "Check wire":               23,
        "Check wire long axis":     24,  # Auto-stacked
        "Check wire short axis":    24,  # Auto-stacked
        "Wire checked":             25,
        "Wire position good?":      26,
        
        # Final
        "Widen pathway":            27,
        "Advance catheter":         28,
        "Remove guidewire":         29,
        "Verify flow and reflow":   30,
        "Check catheter position":  31,
        "End":                      32,
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
