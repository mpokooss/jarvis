from ddgs import DDGS
from langchain_core.tools import tool

@tool
def search_internet(query: str) -> str:
    """
    Χρησιμοποίησε αυτό το εργαλείο ΠΑΝΤΑ όταν ο χρήστης ρωτάει για πρόσφατα γεγονότα, 
    ειδήσεις, ή πληροφορίες που δεν γνωρίζεις.
    Δέχεται ως είσοδο τον όρο αναζήτησης (query).
    """
    print(f"[Σύστημα]: Έναρξη αναζήτησης στο ίντερνετ για '{query}'...")
    
    try:
        with DDGS() as ddgs:
            # ΑΛΛΑΓΗ: Χρησιμοποιούμε news αντί για text και timelimit='w'
            results = list(ddgs.news(query, max_results=3, timelimit='w'))
        
        if not results:
            return "Δεν βρέθηκαν πρόσφατες ειδήσεις για αυτή την αναζήτηση."
        
        formatted_results = ""
        for i, res in enumerate(results, 1):
            formatted_results += f"Αποτέλεσμα {i}:\nΤίτλος: {res['title']}\nΠερίληψη: {res['body']}\nΠηγή: {res['source']}\n\n"
            
        return formatted_results
        
    except Exception as e:
        return f"Σφάλμα κατά την αναζήτηση: {str(e)}"