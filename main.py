from brain.llm import get_llm
from brain.memory import load_profile, update_memory
from tools.general import get_time
from tools.web_search import search_internet
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from voice.tts import speak
from tools.weather import get_weather
from automation.system_commands import launch_application
from automation.system_commands import launch_application, control_volume, system_power, open_settings, mute_system, control_media, press_shortcut, play_spotify, play_youtube

def start_jarvis():
    print("Φόρτωση συστημάτων...")
    llm = get_llm()
    
    # ΝΕΟ: Προσθήκη του update_memory στα εργαλεία
    tools_list = [get_time, search_internet, launch_application, update_memory, get_weather, control_volume, system_power, open_settings, launch_application, mute_system, control_media, press_shortcut, play_spotify, play_youtube]
    llm_with_tools = llm.bind_tools(tools_list)
    tools_map = {tool.name: tool for tool in tools_list}
    
    # ΝΕΟ: Διαβάζει το προφίλ σου
    user_profile = load_profile()
    
    print("\nΟ Jarvis είναι online. (Γράψε 'exit' για έξοδο)")
    print("-" * 60)

    today = datetime.now().strftime("%Y-%m-%d")
   
    system_prompt = (
        f"You are J.A.R.V.I.S., a highly advanced AI assistant. Today is {today}.\n"
        f"You must communicate with the user STRICTLY in English.\n"
        f"Tone: highly professional, slightly sarcastic. Address the user as 'Sir'.\n\n"
        f"!!! CRITICAL SYSTEM RULE FOR TOOLS !!!\n"
        f"1. When you need to use ANY tool, YOU MUST DO IT ABSOLUTELY SILENTLY. \n"
        f"2. DO NOT output ANY conversational text before calling a tool. If you write ANY text before a tool call, the system will CRASH. Just call the tool.\n"
        f"3. YOU HAVE INTERNET ACCESS. NEVER say you cannot check real-time info. Always use the 'search_internet' tool for weather, news, etc.\n\n"
        f"User Profile (Sir):\n"
        f"Name: {user_profile.get('Ονομα', 'Unknown')}\n"
        f"Interests: {', '.join(user_profile.get('Ενδιαφεροντα', []))}\n"
        f"Facts: {', '.join(user_profile.get('Γεγονοτα', []))}"
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
            all_tool_results = ""
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                
                if tool_name in tools_map:
                    selected_tool = tools_map[tool_name]
                    tool_result = selected_tool.invoke(tool_call["args"])
                    all_tool_results += f"Tool {tool_name} returned data: {tool_result}\n"
            final_prompt = f"Tool {tool_name} returned data: {tool_result}\nRespond based ONLY on this data."
            chat_history.append(HumanMessage(content=final_prompt))
                    
            final_response = llm.invoke(chat_history)
            print(f"\nJarvis: {final_response.content}")
            speak(final_response.content)
            chat_history.append(AIMessage(content=final_response.content))
        else:
            print(f"\nJarvis: {response.content}")
            speak(response.content)
            chat_history.append(AIMessage(content=response.content))

if __name__ == "__main__":
    start_jarvis()