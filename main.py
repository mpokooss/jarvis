from brain.llm import get_llm
from tools.general import get_time

def start_jarvis():
    print("Φόρτωση συστημάτων...")
    llm = get_llm()
    
    # Συνδέουμε το εργαλείο απευθείας με τις "ικανότητες" του Llama 3
    llm_with_tools = llm.bind_tools([get_time])
    
    print("\nΟ Jarvis είναι online. (Γράψε 'exit' για έξοδο)")
    print("-" * 50)

    while True:
        user_input = input("\nΕσύ: ")
        if user_input.lower() in ['exit', 'quit', 'έξοδος']:
            print("Jarvis: Απενεργοποίηση. Αντίο!")
            break
        if not user_input.strip():
            continue

        # Το μοντέλο επεξεργάζεται την πρόταση και αποφασίζει αν χρειάζεται εργαλείο
        response = llm_with_tools.invoke(user_input)
        
        # Έλεγχος αν το μοντέλο ζήτησε να εκτελεστεί κάποιο εργαλείο στην Python
        if response.tool_calls:
            print("[Jarvis]: Εκτέλεση εργαλείου συστήματος...")
            for tool_call in response.tool_calls:
                if tool_call["name"] == "get_time":
                    # Τρέχουμε τη συνάρτηση Python
                    time_result = get_time.invoke(tool_call["args"])
                    
                    # Δίνουμε το αποτέλεσμα πίσω στο LLM για να συντάξει την τελική απάντηση
                    final_prompt = f"User asked: {user_input}\nTool get_time returned: {time_result}\nRespond to the user in Greek."
                    final_response = llm.invoke(final_prompt)
                    print(f"\nJarvis: {final_response.content}")
        else:
            # Αν η ερώτηση ήταν απλή (π.χ. "Γεια σου"), απαντάει απευθείας
            print(f"\nJarvis: {response.content}")

if __name__ == "__main__":
    start_jarvis()