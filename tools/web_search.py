from ddgs import DDGS
from langchain_core.tools import tool

@tool
def search_internet(query: str) -> str:
    """
    Use this tool ALWAYS when you need real-time information, 
    such as the weather forecast, news, current events, or web searches.
    """
    # (Ο υπόλοιπος κώδικάς σου παραμένει ακριβώς ο ίδιος από κάτω)
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