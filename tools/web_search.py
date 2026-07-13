from ddgs import DDGS
from langchain_core.tools import tool

@tool
def search_internet(query: str) -> str:
    """
    Χρησιμοποίησε αυτό το εργαλείο μόνο για πρόσφατα γεγονότα, επίκαιρες ειδήσεις και γενικές γνώσεις.
    ΜΗΝ χρησιμοποιείς ΠΟΤΕ αυτό το εργαλείο αν ο χρήστης σου ζητάει να ανοίξεις προγράμματα, 
    εφαρμογές, το τερματικό ή αρχεία του υπολογιστή του.
    """
    print(f"[Σύστημα]: Έναρξη αναζήτησης στο ίντερνετ για '{query}'...")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=3, timelimit='w'))
        
        if not results:
            return "Δεν βρέθηκαν πρόσφατες ειδήσεις για αυτή την αναζήτηση."
        
        formatted_results = ""
        for i, res in enumerate(results, 1):
            formatted_results += f"Αποτέλεσμα {i}:\nΤίτλος: {res['title']}\nΠερίληψη: {res['body']}\nΠηγή: {res['source']}\n\n"
            
        return formatted_results
        
    except Exception as e:
        return f"Σφάλμα κατά την αναζήτηση: {str(e)}"