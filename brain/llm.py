import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Φορτώνει αυτόματα τις μεταβλητές από το αρχείο .env
load_dotenv()

def get_llm():
    """Φορτώνει το Mixtral μέσω του υπερ-γρήγορου δικτύου της Groq."""
    
    # Διαβάζει το κλειδί με ασφάλεια από το σύστημα
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("Δεν βρέθηκε το GROQ_API_KEY. Σιγουρέψου ότι υπάρχει στο αρχείο .env")
    
    llm = ChatGroq(
        api_key=api_key,
        # Η ΑΛΛΑΓΗ ΕΓΙΝΕ ΕΔΩ: Περνάμε στο Mixtral που είναι αλάνθαστο στα εργαλεία
        model="meta-llama/llama-4-scout-17b-16e-instruct",  
        temperature=0.1,
        max_retries=2
    )
    
    return llm