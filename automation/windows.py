import os
from langchain_core.tools import tool

@tool
def open_application(app_name: str) -> str:
    """
    Χρησιμοποίησε αυτό το εργαλείο ΥΠΟΧΡΕΩΤΙΚΑ όταν ο χρήστης ζητάει να ανοίξεις, 
    να εκκινήσεις ή να τρέξεις οποιοδήποτε πρόγραμμα, εφαρμογή ή εργαλείο στον υπολογιστή του 
    (π.χ. αριθμομηχανή, σημειωματάριο, τερματικό, γραμμή εντολών, cmd, calculator, notepad).
    Μην υποθέτεις ΠΟΤΕ ότι η εφαρμογή είναι ήδη ανοιχτή. Κάλεσε ΠΑΝΤΑ αυτό το εργαλείο.
    """
    print(f"[Σύστημα]: Προσπάθεια εκκίνησης της εφαρμογής '{app_name}'...")
    
    app_lower = app_name.lower()
    app_exe = None
    
    if "αριθμ" in app_lower or "calc" in app_lower:
        app_exe = "calc.exe"
    elif "σημειω" in app_lower or "note" in app_lower:
        app_exe = "notepad.exe"
    elif "cmd" in app_lower or "τερματικ" in app_lower or "terminal" in app_lower:
        app_exe = "cmd.exe"
        
    if not app_exe:
        return f"Δεν γνωρίζω τη διαδρομή για την εφαρμογή '{app_name}'."
    
    try:
        os.startfile(app_exe)
        return f"Η εφαρμογή {app_name} άνοιξε με επιτυχία."
    except Exception as e:
        return f"Αποτυχία ανοίγματος. Σφάλμα: {str(e)}"