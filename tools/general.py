from langchain_core.tools import tool
from datetime import datetime

@tool
def get_time(query: str = "") -> str:
    """
    Επιστρέφει την τρέχουσα ημερομηνία και ώρα. 
    Κάλεσε αυτό το εργαλείο ΠΑΝΤΑ όταν ο χρήστης ρωτάει τι ώρα είναι, τι μέρα έχουμε ή ποια είναι η ημερομηνία.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")