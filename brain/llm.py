from langchain_ollama import ChatOllama

def get_llm():
    # Αναβάθμιση σε 3.1 που υποστηρίζει Tools!
    return ChatOllama(model="llama3.1", temperature=0)