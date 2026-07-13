import json
import os
from langchain_core.tools import tool

# Το αρχείο που θα αποθηκεύονται τα δεδομένα σου (θα δημιουργηθεί αυτόματα)
PROFILE_FILE = "profile.json"

def load_profile():
    """Φορτώνει το προφίλ του χρήστη. Αν δεν υπάρχει, δημιουργεί ένα βασικό."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Το αρχικό "κενό" προφίλ
    return {
        "Ονομα": "Άγνωστο",
        "Ενδιαφεροντα": [],
        "Γεγονοτα": []
    }

@tool
def update_memory(category: str, information: str) -> str:
    """
    Χρησιμοποίησε αυτό το εργαλείο ΠΑΝΤΑ όταν ο χρήστης σου λέει κάτι σημαντικό για τον εαυτό του 
    (π.χ. το όνομά του, τη δουλειά του, τι του αρέσει) για να το αποθηκεύσεις μόνιμα στη μνήμη σου.
    Κατηγορίες (category) που δέχεσαι: 'Ονομα', 'Ενδιαφεροντα', 'Γεγονοτα'.
    """
    print(f"[Σύστημα Μνήμης]: Νέα εγγραφή -> Κατηγορία: {category} | Πληροφορία: {information}")
    
    profile = load_profile()
    
    # Ενημέρωση των δεδομένων
    if category == "Ονομα":
        profile["Ονομα"] = information
    elif category in ["Ενδιαφεροντα", "Γεγονοτα"]:
        if information not in profile[category]:
            profile[category].append(information)
    else:
        # Αν το AI φανταστεί δική του κατηγορία, τη φτιάχνουμε
        if category not in profile:
            profile[category] = []
        profile[category].append(information)

    # Αποθήκευση πίσω στο JSON
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=4)
        
    return "Η πληροφορία αποθηκεύτηκε επιτυχώς στη μόνιμη μνήμη."