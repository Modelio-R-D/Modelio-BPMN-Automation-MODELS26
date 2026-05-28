#
# NataleItalia_Generated.py
#
# Description:
#   Detailed BPMN process for Catholic Christmas Preparation in Italy
#   Covers the entire month of December with traditional Italian customs
#
#   Key Italian Christmas Traditions included:
#   - Corona dell'Avvento (Advent Wreath)
#   - Immacolata Concezione (Dec 8)
#   - Il Presepe (Nativity Scene)
#   - Novena di Natale (Dec 16-24)
#   - La Vigilia (Christmas Eve traditions)
#   - Messa di Mezzanotte (Midnight Mass)
#   - Pranzo di Natale (Christmas Day feast)
#   - Santo Stefano (Dec 26)
#   - Preparation for Epifania (Jan 6)
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# ============================================================================
# LOAD HELPER LIBRARY
# ============================================================================

execfile(".modelio/5.4/macros/BPMN_Helpers.py")


# ============================================================================
# PROCESS CONFIGURATION
# ============================================================================

CONFIG = {
    "name": "NataleItalia",
    
    # Layout settings - wider spacing for complex process
    "SPACING": 140,
    "TASK_WIDTH": 130,
    "TASK_HEIGHT": 55,
    
    # Lanes (top to bottom) - representing key participants
    "lanes": [
        "Famiglia",      # Family - main home activities
        "Parrocchia",    # Parish - church activities
        "Bambini",       # Children - kid-specific traditions
    ],
    
    # ========================================================================
    # ELEMENTS: (name, type, lane)
    # ========================================================================
    "elements": [
        # ====================================================================
        # PHASE 1: ADVENT BEGINS (Dec 1-7)
        # ====================================================================
        
        # Family Lane - Early December
        ("Dicembre Inizia",            START,        "Famiglia"),
        ("Prepara Corona Avvento",     MANUAL_TASK,  "Famiglia"),
        ("Accendi Prima Candela",      USER_TASK,    "Famiglia"),
        ("Acquista Regali Natale",     USER_TASK,    "Famiglia"),
        ("Prepara Dolci Tradizionali", MANUAL_TASK,  "Famiglia"),
        
        # Parish Lane - Advent
        ("Prima Messa Avvento",        USER_TASK,    "Parrocchia"),
        ("Confessione Avvento",        USER_TASK,    "Parrocchia"),
        
        # Children Lane - Early December
        ("Apri Calendario Avvento",    USER_TASK,    "Bambini"),
        ("Scrivi Letterina",           USER_TASK,    "Bambini"),
        
        # ====================================================================
        # PHASE 2: IMMACOLATA CONCEZIONE (Dec 8)
        # ====================================================================
        
        # Family Lane
        ("Prepara Casa Decorazioni",   MANUAL_TASK,  "Famiglia"),
        ("Decora Albero Natale",       MANUAL_TASK,  "Famiglia"),
        
        # Parish Lane - Dec 8 Mass
        ("Messa Immacolata",           USER_TASK,    "Parrocchia"),
        
        # Children Lane
        ("Aiuta Decorare",             USER_TASK,    "Bambini"),
        
        # ====================================================================
        # PHASE 3: IL PRESEPE (Dec 8-23)
        # ====================================================================
        
        # Family Lane - Nativity Scene
        ("Costruisci Struttura Presepe", MANUAL_TASK,  "Famiglia"),
        ("Posiziona Figure Presepe",     MANUAL_TASK,  "Famiglia"),
        ("Aggiungi Muschio e Luci",      MANUAL_TASK,  "Famiglia"),
        ("Presepe Pronto?",              EXCLUSIVE_GW, "Famiglia"),
        ("Migliora Presepe",             USER_TASK,    "Famiglia"),
        
        # Children Lane - Presepe activities
        ("Disponi Pastori",            USER_TASK,    "Bambini"),
        ("Posiziona Animali",          USER_TASK,    "Bambini"),
        ("Avvicina Re Magi",           USER_TASK,    "Bambini"),
        
        # ====================================================================
        # PHASE 4: NOVENA DI NATALE (Dec 16-24)
        # ====================================================================
        
        # Parish Lane - Nine days of prayer
        ("Inizia Novena",              USER_TASK,    "Parrocchia"),
        ("Preghiere Giornaliere",      USER_TASK,    "Parrocchia"),
        ("Canti Natalizi Chiesa",      USER_TASK,    "Parrocchia"),
        
        # Family Lane - Mid December
        ("Invia Auguri Natale",        USER_TASK,    "Famiglia"),
        ("Prepara Panettone Pandoro",  MANUAL_TASK,  "Famiglia"),
        ("Acquista Torrone Struffoli", USER_TASK,    "Famiglia"),
        
        # ====================================================================
        # PHASE 5: LA VIGILIA (Dec 24)
        # ====================================================================
        
        # Family Lane - Christmas Eve
        ("Prepara Cenone Vigilia",     MANUAL_TASK,  "Famiglia"),
        ("Cucina Baccala Capitone",    MANUAL_TASK,  "Famiglia"),
        ("Apparecchia Tavola Festa",   MANUAL_TASK,  "Famiglia"),
        ("Cenone Famiglia",            USER_TASK,    "Famiglia"),
        ("Attesa Mezzanotte",          USER_TASK,    "Famiglia"),
        
        # Children Lane - Christmas Eve
        ("Aspetta Babbo Natale",       USER_TASK,    "Bambini"),
        ("Prepara Latte Biscotti",     USER_TASK,    "Bambini"),
        
        # Parish Lane - Midnight Mass
        ("Messa Mezzanotte",           USER_TASK,    "Parrocchia"),
        ("Canto Tu Scendi Stelle",     USER_TASK,    "Parrocchia"),
        
        # Family Lane - After Mass
        ("Poni Gesu Bambino Presepe",  USER_TASK,    "Famiglia"),
        
        # ====================================================================
        # PHASE 6: NATALE (Dec 25)
        # ====================================================================
        
        # Children Lane - Christmas Morning
        ("Apri Regali",                USER_TASK,    "Bambini"),
        ("Gioca Nuovi Giocattoli",     USER_TASK,    "Bambini"),
        
        # Family Lane - Christmas Day
        ("Messa Giorno Natale",        USER_TASK,    "Parrocchia"),
        ("Prepara Pranzo Natale",      MANUAL_TASK,  "Famiglia"),
        ("Pranzo Grande Famiglia",     USER_TASK,    "Famiglia"),
        ("Mangia Panettone Spumante",  USER_TASK,    "Famiglia"),
        ("Gioca Tombola",              USER_TASK,    "Famiglia"),
        ("Riposo Pomeridiano",         USER_TASK,    "Famiglia"),
        
        # ====================================================================
        # PHASE 7: SANTO STEFANO (Dec 26)
        # ====================================================================
        
        # Family Lane
        ("Visita Parenti Amici",       USER_TASK,    "Famiglia"),
        ("Pranzo Avanzi Natale",       USER_TASK,    "Famiglia"),
        
        # Parish Lane
        ("Messa Santo Stefano",        USER_TASK,    "Parrocchia"),
        
        # ====================================================================
        # PHASE 8: VERSO EPIFANIA (Dec 27-31)
        # ====================================================================
        
        # Family Lane - Post Christmas
        ("Prepara Capodanno",          USER_TASK,    "Famiglia"),
        ("Acquista Lenticchie Cotechino", USER_TASK, "Famiglia"),
        ("Calza Befana Pronta?",       EXCLUSIVE_GW, "Famiglia"),
        ("Prepara Calza Befana",       USER_TASK,    "Famiglia"),
        
        # Children Lane
        ("Scrivi Lettera Befana",      USER_TASK,    "Bambini"),
        ("Attendi Epifania",           USER_TASK,    "Bambini"),
        
        # End Events
        ("Natale Completato",          END,          "Famiglia"),
        ("Pronto per Epifania",        MESSAGE_END,  "Bambini"),
    ],
    
    # ========================================================================
    # FLOWS: (source, target, guard)
    # ========================================================================
    "flows": [
        # === PHASE 1: Advent Begins ===
        ("Dicembre Inizia",            "Prepara Corona Avvento",     ""),
        ("Prepara Corona Avvento",     "Accendi Prima Candela",      ""),
        ("Accendi Prima Candela",      "Prima Messa Avvento",        ""),
        
        # Parallel tracks begin
        ("Prima Messa Avvento",        "Apri Calendario Avvento",    ""),
        ("Prima Messa Avvento",        "Acquista Regali Natale",     ""),
        ("Apri Calendario Avvento",    "Scrivi Letterina",           ""),
        
        # Preparation continues
        ("Acquista Regali Natale",     "Prepara Dolci Tradizionali", ""),
        ("Scrivi Letterina",           "Confessione Avvento",        ""),
        
        # === PHASE 2: Immacolata (Dec 8) ===
        ("Prepara Dolci Tradizionali", "Messa Immacolata",           "8 Dicembre"),
        ("Confessione Avvento",        "Messa Immacolata",           ""),
        ("Messa Immacolata",           "Prepara Casa Decorazioni",   ""),
        ("Prepara Casa Decorazioni",   "Decora Albero Natale",       ""),
        ("Decora Albero Natale",       "Aiuta Decorare",             ""),
        
        # === PHASE 3: Presepe ===
        ("Aiuta Decorare",             "Costruisci Struttura Presepe", ""),
        ("Costruisci Struttura Presepe", "Posiziona Figure Presepe",   ""),
        ("Posiziona Figure Presepe",   "Disponi Pastori",            ""),
        ("Disponi Pastori",            "Posiziona Animali",          ""),
        ("Posiziona Animali",          "Aggiungi Muschio e Luci",    ""),
        ("Aggiungi Muschio e Luci",    "Presepe Pronto?",            ""),
        
        # Presepe decision
        ("Presepe Pronto?",            "Migliora Presepe",           "No"),
        ("Migliora Presepe",           "Presepe Pronto?",            "Ricontrolla"),
        ("Presepe Pronto?",            "Avvicina Re Magi",           "Si"),
        
        # === PHASE 4: Novena (Dec 16-24) ===
        ("Avvicina Re Magi",           "Inizia Novena",              "16 Dicembre"),
        ("Inizia Novena",              "Preghiere Giornaliere",      ""),
        ("Preghiere Giornaliere",      "Canti Natalizi Chiesa",      ""),
        
        # Parallel preparations
        ("Canti Natalizi Chiesa",      "Invia Auguri Natale",        ""),
        ("Invia Auguri Natale",        "Prepara Panettone Pandoro",  ""),
        ("Prepara Panettone Pandoro",  "Acquista Torrone Struffoli", ""),
        
        # === PHASE 5: Vigilia (Dec 24) ===
        ("Acquista Torrone Struffoli", "Prepara Cenone Vigilia",     "24 Dicembre"),
        ("Prepara Cenone Vigilia",     "Cucina Baccala Capitone",    ""),
        ("Cucina Baccala Capitone",    "Apparecchia Tavola Festa",   ""),
        ("Apparecchia Tavola Festa",   "Cenone Famiglia",            ""),
        
        # Children evening activities
        ("Cenone Famiglia",            "Aspetta Babbo Natale",       ""),
        ("Aspetta Babbo Natale",       "Prepara Latte Biscotti",     ""),
        ("Prepara Latte Biscotti",     "Attesa Mezzanotte",          ""),
        
        # Midnight
        ("Attesa Mezzanotte",          "Messa Mezzanotte",           "23:30"),
        ("Messa Mezzanotte",           "Canto Tu Scendi Stelle",     ""),
        ("Canto Tu Scendi Stelle",     "Poni Gesu Bambino Presepe",  ""),
        
        # === PHASE 6: Natale (Dec 25) ===
        ("Poni Gesu Bambino Presepe",  "Apri Regali",                "25 Mattina"),
        ("Apri Regali",                "Gioca Nuovi Giocattoli",     ""),
        ("Gioca Nuovi Giocattoli",     "Messa Giorno Natale",        ""),
        ("Messa Giorno Natale",        "Prepara Pranzo Natale",      ""),
        ("Prepara Pranzo Natale",      "Pranzo Grande Famiglia",     ""),
        ("Pranzo Grande Famiglia",     "Mangia Panettone Spumante",  ""),
        ("Mangia Panettone Spumante",  "Gioca Tombola",              ""),
        ("Gioca Tombola",              "Riposo Pomeridiano",         ""),
        
        # === PHASE 7: Santo Stefano (Dec 26) ===
        ("Riposo Pomeridiano",         "Messa Santo Stefano",        "26 Dicembre"),
        ("Messa Santo Stefano",        "Visita Parenti Amici",       ""),
        ("Visita Parenti Amici",       "Pranzo Avanzi Natale",       ""),
        
        # === PHASE 8: Toward Epifania ===
        ("Pranzo Avanzi Natale",       "Prepara Capodanno",          ""),
        ("Prepara Capodanno",          "Acquista Lenticchie Cotechino", ""),
        ("Acquista Lenticchie Cotechino", "Calza Befana Pronta?",    ""),
        
        # Befana decision
        ("Calza Befana Pronta?",       "Prepara Calza Befana",       "No"),
        ("Prepara Calza Befana",       "Scrivi Lettera Befana",      ""),
        ("Calza Befana Pronta?",       "Scrivi Lettera Befana",      "Si"),
        
        # Final flows
        ("Scrivi Lettera Befana",      "Attendi Epifania",           ""),
        ("Attendi Epifania",           "Natale Completato",          ""),
        ("Attendi Epifania",           "Pronto per Epifania",        "6 Gennaio"),
    ],
    
    # ========================================================================
    # LAYOUT: element name -> column index
    # ========================================================================
    "layout": {
        # === PHASE 1: ADVENT (Columns 0-4) ===
        "Dicembre Inizia":              0,
        "Prepara Corona Avvento":       1,
        "Accendi Prima Candela":        2,
        "Prima Messa Avvento":          3,
        "Apri Calendario Avvento":      4,
        "Scrivi Letterina":             5,
        "Acquista Regali Natale":       4,
        "Prepara Dolci Tradizionali":   5,
        "Confessione Avvento":          6,
        
        # === PHASE 2: IMMACOLATA (Columns 7-9) ===
        "Messa Immacolata":             7,
        "Prepara Casa Decorazioni":     8,
        "Decora Albero Natale":         9,
        "Aiuta Decorare":               10,
        
        # === PHASE 3: PRESEPE (Columns 11-16) ===
        "Costruisci Struttura Presepe": 11,
        "Posiziona Figure Presepe":     12,
        "Disponi Pastori":              13,
        "Posiziona Animali":            14,
        "Aggiungi Muschio e Luci":      15,
        "Presepe Pronto?":              16,
        "Migliora Presepe":             17,
        "Avvicina Re Magi":             18,
        
        # === PHASE 4: NOVENA (Columns 19-23) ===
        "Inizia Novena":                19,
        "Preghiere Giornaliere":        20,
        "Canti Natalizi Chiesa":        21,
        "Invia Auguri Natale":          22,
        "Prepara Panettone Pandoro":    23,
        "Acquista Torrone Struffoli":   24,
        
        # === PHASE 5: VIGILIA (Columns 25-31) ===
        "Prepara Cenone Vigilia":       25,
        "Cucina Baccala Capitone":      26,
        "Apparecchia Tavola Festa":     27,
        "Cenone Famiglia":              28,
        "Aspetta Babbo Natale":         29,
        "Prepara Latte Biscotti":       30,
        "Attesa Mezzanotte":            31,
        "Messa Mezzanotte":             32,
        "Canto Tu Scendi Stelle":       33,
        "Poni Gesu Bambino Presepe":    34,
        
        # === PHASE 6: NATALE (Columns 35-41) ===
        "Apri Regali":                  35,
        "Gioca Nuovi Giocattoli":       36,
        "Messa Giorno Natale":          37,
        "Prepara Pranzo Natale":        38,
        "Pranzo Grande Famiglia":       39,
        "Mangia Panettone Spumante":    40,
        "Gioca Tombola":                41,
        "Riposo Pomeridiano":           42,
        
        # === PHASE 7: SANTO STEFANO (Columns 43-45) ===
        "Messa Santo Stefano":          43,
        "Visita Parenti Amici":         44,
        "Pranzo Avanzi Natale":         45,
        
        # === PHASE 8: VERSO EPIFANIA (Columns 46-51) ===
        "Prepara Capodanno":            46,
        "Acquista Lenticchie Cotechino": 47,
        "Calza Befana Pronta?":         48,
        "Prepara Calza Befana":         49,
        "Scrivi Lettera Befana":        50,
        "Attendi Epifania":             51,
        "Natale Completato":            52,
        "Pronto per Epifania":          52,
    },
}


# ============================================================================
# ENTRY POINT
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
