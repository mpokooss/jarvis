from brain.llm import get_llm
from tools.general import get_time
from tools.web_search import search_internet
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from automation.windows import open_application

def start_jarvis():
    print("Φόρτωση συστημάτων...")
    llm = get_llm()
    
    tools_list = [get_time, search_internet, open_application]
    llm_with_tools = llm.bind_tools(tools_list)
    tools_map = {tool.name: tool for tool in tools_list}
    
    print("\nΟ Jarvis είναι online. (Γράψε 'exit' για έξοδο)")
    print("-" * 60)

    while True:
        user_input = input("\nΕσύ: ")
        if user_input.lower() in ['exit', 'quit', 'έξοδος', 'εξοδος']:
            print("Jarvis: Απενεργοποίηση...")
            break
        if not user_input.strip():
            continue

        # ΕΠΙΓΝΩΣΗ ΧΡΟΝΟΥ: Διαβάζει τη σημερινή ημερομηνία από το σύστημά σου
        today = datetime.now().strftime("%Y-%m-%d")
        
        messages = [
            SystemMessage(content=f"Είσαι ο Jarvis, ένας AI βοηθός. Η σημερινή ημερομηνία είναι {today}. Απάντα στα Ελληνικά."),
            HumanMessage(content=user_input)
        ]

        response = llm_with_tools.invoke(messages)
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                
                if tool_name in tools_map:
                    selected_tool = tools_map[tool_name]
                    tool_result = selected_tool.invoke(tool_call["args"])
                    
                    final_prompt = f"User asked: {user_input}\nTool {tool_name} returned data: {tool_result}\nRespond based ONLY on this data."
                    messages.append(HumanMessage(content=final_prompt))
                    
                    final_response = llm.invoke(messages)
                    print(f"\nJarvis: {final_response.content}")
        else:
            print(f"\nJarvis: {response.content}")

if __name__ == "__main__":
    start_jarvis()