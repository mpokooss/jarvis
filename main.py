from brain.llm import get_llm
# ΝΕΟ: Εισαγωγή της μνήμης
from brain.memory import load_profile, update_memory
from tools.general import get_time
from tools.web_search import search_internet
from automation.windows import open_application
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def start_jarvis():
    print("Φόρτωση συστημάτων...")
    llm = get_llm()
    
    # ΝΕΟ: Προσθήκη του update_memory στα εργαλεία
    tools_list = [get_time, search_internet, open_application, update_memory]
    llm_with_tools = llm.bind_tools(tools_list)
    tools_map = {tool.name: tool for tool in tools_list}
    
    # ΝΕΟ: Διαβάζει το προφίλ σου
    user_profile = load_profile()
    
    print("\nΟ Jarvis είναι online. (Γράψε 'exit' για έξοδο)")
    print("-" * 60)

    today = datetime.now().strftime("%Y-%m-%d")
    
    # ΝΕΟ: Δίνουμε στο LLM τα δεδομένα σου από το JSON
    system_prompt = (
        f"Είσαι ο Jarvis, ένας AI βοηθός. Η σημερινή ημερομηνία είναι {today}. Απάντα στα Ελληνικά.\n"
        f"Γνωρίζεις τα εξής για τον χρήστη:\n"
        f"Όνομα: {user_profile.get('Ονομα', 'Άγνωστο')}\n"
        f"Ενδιαφέροντα: {', '.join(user_profile.get('Ενδιαφεροντα', []))}\n"
        f"Άλλες Πληροφορίες: {', '.join(user_profile.get('Γεγονοτα', []))}"
    )
    
    chat_history = [SystemMessage(content=system_prompt)]

    while True:
        user_input = input("\nΕσύ: ")
        if user_input.lower() in ['exit', 'quit', 'έξοδος']:
            print("Jarvis: Απενεργοποίηση. Αντίο!")
            break
        if not user_input.strip():
            continue

        chat_history.append(HumanMessage(content=user_input))
        response = llm_with_tools.invoke(chat_history)
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                
                if tool_name in tools_map:
                    selected_tool = tools_map[tool_name]
                    tool_result = selected_tool.invoke(tool_call["args"])
                    
                    final_prompt = f"Tool {tool_name} returned data: {tool_result}\nRespond based ONLY on this data."
                    chat_history.append(HumanMessage(content=final_prompt))
                    
                    final_response = llm.invoke(chat_history)
                    print(f"\nJarvis: {final_response.content}")
                    chat_history.append(AIMessage(content=final_response.content))
        else:
            print(f"\nJarvis: {response.content}")
            chat_history.append(AIMessage(content=response.content))

if __name__ == "__main__":
    start_jarvis()