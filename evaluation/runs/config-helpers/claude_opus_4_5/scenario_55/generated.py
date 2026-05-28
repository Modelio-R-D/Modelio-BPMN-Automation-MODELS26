#
# CentralVenousCatheterInsertion.py
#
# Description: BPMN diagram for ultrasound-guided central venous catheter insertion procedure
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CentralVenousCatheterInsertion",
    
    "lanes": ["Doctor"],
    
    "elements": [
        # Preparation phase
        ("Start", START, "Doctor"),
        ("Prepare Implements", MANUAL_TASK, "Doctor"),
        ("Wash Hands", MANUAL_TASK, "Doctor"),
        ("Get Sterile Clothes", MANUAL_TASK, "Doctor"),
        ("Sync Prep", PARALLEL_GW, "Doctor"),
        
        # Site preparation
        ("Clean Puncture Area", MANUAL_TASK, "Doctor"),
        ("Drape Puncture Zone", MANUAL_TASK, "Doctor"),
        
        # Ultrasound preparation
        ("Configure Ultrasound", MANUAL_TASK, "Doctor"),
        ("Put Gel on Probe", MANUAL_TASK, "Doctor"),
        ("Sync Ultrasound", PARALLEL_GW, "Doctor"),
        ("Cover Probe", MANUAL_TASK, "Doctor"),
        ("Put Sterile Gel", MANUAL_TASK, "Doctor"),
        
        # Positioning
        ("Position Probe", MANUAL_TASK, "Doctor"),
        ("Position Patient", MANUAL_TASK, "Doctor"),
        ("Sync Position", PARALLEL_GW, "Doctor"),
        
        # Vein identification
        ("Split Identification", PARALLEL_GW, "Doctor"),
        ("Anatomic Identification", MANUAL_TASK, "Doctor"),
        ("Doppler Identification", MANUAL_TASK, "Doctor"),
        ("Compression Identification", MANUAL_TASK, "Doctor"),
        ("Join Identification", PARALLEL_GW, "Doctor"),
        
        # Puncture
        ("Anesthetize Patient", MANUAL_TASK, "Doctor"),
        ("Puncture", MANUAL_TASK, "Doctor"),
        ("Check Blood Return", MANUAL_TASK, "Doctor"),
        ("Blood Return OK?", EXCLUSIVE_GW, "Doctor"),
        
        # Post-puncture
        ("Drop Probe", MANUAL_TASK, "Doctor"),
        ("Remove Syringe", MANUAL_TASK, "Doctor"),
        ("Install Guidewire", MANUAL_TASK, "Doctor"),
        ("Remove Trocar", MANUAL_TASK, "Doctor"),
        
        # Wire check
        ("Split Wire Check", PARALLEL_GW, "Doctor"),
        ("Check Wire Long Axis", MANUAL_TASK, "Doctor"),
        ("Check Wire Short Axis", MANUAL_TASK, "Doctor"),
        ("Join Wire Check", PARALLEL_GW, "Doctor"),
        ("Wire Position OK?", EXCLUSIVE_GW, "Doctor"),
        
        # Catheter insertion
        ("Widen Pathway", MANUAL_TASK, "Doctor"),
        ("Advance Catheter", MANUAL_TASK, "Doctor"),
        ("Remove Guidewire", MANUAL_TASK, "Doctor"),
        
        # Final verification
        ("Verify Flow and Reflow", MANUAL_TASK, "Doctor"),
        ("Check Catheter Position", MANUAL_TASK, "Doctor"),
        ("End", END, "Doctor"),
    ],
    
    "flows": [
        # Preparation phase
        ("Start", "Prepare Implements", ""),
        ("Prepare Implements", "Wash Hands", ""),
        ("Wash Hands", "Get Sterile Clothes", ""),
        ("Get Sterile Clothes", "Sync Prep", ""),
        
        # Site preparation (parallel)
        ("Sync Prep", "Clean Puncture Area", ""),
        ("Sync Prep", "Configure Ultrasound", ""),
        ("Clean Puncture Area", "Drape Puncture Zone", ""),
        ("Drape Puncture Zone", "Sync Ultrasound", ""),
        ("Configure Ultrasound", "Put Gel on Probe", ""),
        ("Put Gel on Probe", "Sync Ultrasound", ""),
        
        # Probe preparation
        ("Sync Ultrasound", "Cover Probe", ""),
        ("Cover Probe", "Put Sterile Gel", ""),
        
        # Positioning (parallel)
        ("Put Sterile Gel", "Position Probe", ""),
        ("Put Sterile Gel", "Position Patient", ""),
        ("Position Probe", "Sync Position", ""),
        ("Position Patient", "Sync Position", ""),
        
        # Vein identification (parallel - all three methods)
        ("Sync Position", "Split Identification", ""),
        ("Split Identification", "Anatomic Identification", ""),
        ("Split Identification", "Doppler Identification", ""),
        ("Split Identification", "Compression Identification", ""),
        ("Anatomic Identification", "Join Identification", ""),
        ("Doppler Identification", "Join Identification", ""),
        ("Compression Identification", "Join Identification", ""),
        
        # Puncture sequence
        ("Join Identification", "Anesthetize Patient", ""),
        ("Anesthetize Patient", "Puncture", ""),
        ("Puncture", "Check Blood Return", ""),
        ("Check Blood Return", "Blood Return OK?", ""),
        
        # Blood return decision
        ("Blood Return OK?", "Puncture", "No"),
        ("Blood Return OK?", "Drop Probe", "Yes"),
        
        # Post-puncture sequence
        ("Drop Probe", "Remove Syringe", ""),
        ("Remove Syringe", "Install Guidewire", ""),
        ("Install Guidewire", "Remove Trocar", ""),
        
        # Wire check (parallel)
        ("Remove Trocar", "Split Wire Check", ""),
        ("Split Wire Check", "Check Wire Long Axis", ""),
        ("Split Wire Check", "Check Wire Short Axis", ""),
        ("Check Wire Long Axis", "Join Wire Check", ""),
        ("Check Wire Short Axis", "Join Wire Check", ""),
        ("Join Wire Check", "Wire Position OK?", ""),
        
        # Wire position decision
        ("Wire Position OK?", "Puncture", "No"),
        ("Wire Position OK?", "Widen Pathway", "Yes"),
        
        # Catheter insertion sequence
        ("Widen Pathway", "Advance Catheter", ""),
        ("Advance Catheter", "Remove Guidewire", ""),
        
        # Final verification
        ("Remove Guidewire", "Verify Flow and Reflow", ""),
        ("Verify Flow and Reflow", "Check Catheter Position", ""),
        ("Check Catheter Position", "End", ""),
    ],
    
    "layout": {
        # Preparation phase
        "Start": 0,
        "Prepare Implements": 1,
        "Wash Hands": 2,
        "Get Sterile Clothes": 3,
        "Sync Prep": 4,
        
        # Parallel: site prep and ultrasound prep
        "Clean Puncture Area": (5, 0),
        "Configure Ultrasound": (5, 90),
        "Drape Puncture Zone": (6, 0),
        "Put Gel on Probe": (6, 90),
        "Sync Ultrasound": 7,
        
        # Probe preparation
        "Cover Probe": 8,
        "Put Sterile Gel": 9,
        
        # Positioning (parallel)
        "Position Probe": (10, 0),
        "Position Patient": (10, 90),
        "Sync Position": 11,
        
        # Vein identification (parallel - 3 methods)
        "Split Identification": 12,
        "Anatomic Identification": (13, 0),
        "Doppler Identification": (13, 90),
        "Compression Identification": (13, 180),
        "Join Identification": 14,
        
        # Puncture sequence
        "Anesthetize Patient": 15,
        "Puncture": 16,
        "Check Blood Return": 17,
        "Blood Return OK?": 18,
        
        # Post-puncture
        "Drop Probe": 19,
        "Remove Syringe": 20,
        "Install Guidewire": 21,
        "Remove Trocar": 22,
        
        # Wire check (parallel)
        "Split Wire Check": 23,
        "Check Wire Long Axis": (24, 0),
        "Check Wire Short Axis": (24, 90),
        "Join Wire Check": 25,
        "Wire Position OK?": 26,
        
        # Catheter insertion
        "Widen Pathway": 27,
        "Advance Catheter": 28,
        "Remove Guidewire": 29,
        
        # Final verification
        "Verify Flow and Reflow": 30,
        "Check Catheter Position": 31,
        "End": 32,
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
