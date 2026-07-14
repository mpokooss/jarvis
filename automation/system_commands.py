from langchain_core.tools import tool
import time
import pywhatkit
from AppOpener import open as open_app
import os
import pyautogui
import subprocess

@tool
def launch_application(app_name: str) -> str:
    """
    Use this tool to open ANY application on the computer by its name 
    (e.g., Spotify, Calculator, Word, Chrome).
    """
    try:
        # Η match_closest=True βοηθάει αν το AI κάνει κάποιο μικρό ορθογραφικό!
        open_app(app_name, match_closest=True)
        return f"Sir, I have launched {app_name}."
    except Exception as e:
        return f"I encountered an error trying to open {app_name}: {str(e)}"

@tool
def control_volume(action: str, amount: int = 5) -> str:
    """
    Use this tool to change the system volume.
    Action can be ONLY 'up' or 'down'. Do not use this tool to mute.
    """
    try:
        # Κάθε πάτημα αλλάζει τον ήχο κατά 2% στα Windows
        key = 'volumeup' if action == 'up' else 'volumedown'
        for _ in range(amount):
            pyautogui.press(key)
            
        return f"Sir, the volume has been turned {action}."
    except Exception as e:
        return f"Error adjusting volume: {str(e)}"

@tool
def mute_system() -> str:
    """
    Use this tool to instantly mute or unmute the system volume.
    """
    try:
        pyautogui.press('volumemute')
        return "Sir, the system volume has been toggled (muted/unmuted)."
    except Exception as e:
        return f"Error toggling mute: {str(e)}"

@tool
def control_media(action: str) -> str:
    """
    Use this tool to control media playback in apps like Spotify, Chrome, or Media Players.
    Action must be strictly one of: 'playpause', 'nexttrack', or 'prevtrack'.
    """
    try:
        if action == 'playpause':
            pyautogui.press('playpause')
            return "Sir, I have toggled the playback."
        elif action == 'nexttrack':
            pyautogui.press('nexttrack')
            return "Sir, skipping to the next track."
        elif action == 'prevtrack':
            pyautogui.press('prevtrack')
            return "Sir, returning to the previous track."
        return "Unknown media command, Sir."
    except Exception as e:
        return f"Error controlling media: {str(e)}"

@tool
def press_shortcut(keys: str) -> str:
    """
    Use this tool to execute keyboard shortcuts in the currently active foreground application.
    Provide the keys separated by a plus sign (+). 
    Examples: 'ctrl+t' (new tab), 'ctrl+w' (close tab), 'space' (play/pause video), 'enter'.
    """
    try:
        # Split the string (e.g., "ctrl+t") into a list (["ctrl", "t"])
        key_list = [k.strip().lower() for k in keys.split('+')]
        
        # Unpack the list into the hotkey function
        pyautogui.hotkey(*key_list)
        return f"Sir, I have executed the shortcut: {keys}."
    except Exception as e:
        return f"Error pressing shortcut: {str(e)}"
    
@tool    
def play_spotify(search_query: str) -> str:
    """
    Use this tool to search and automatically play a specific song, artist, or playlist on Spotify.
    Provide the name of the song, artist, or playlist as the search_query.
    """
    try:
        # Αντικαθιστούμε τα κενά με %20 για να είναι έγκυρο το URL/URI
        formatted_query = search_query.replace(" ", "%20")
        
        # Ανοίγει το Spotify απευθείας στη σελίδα της αναζήτησης για αυτό που ζητήσαμε
        os.startfile(f"spotify:search:{formatted_query}")
        
        # Περιμένουμε 2.5 δευτερόλεπτα να φορτώσει η εφαρμογή και τα αποτελέσματα
        time.sleep(2.5)
        
        # Στο Spotify Desktop, όταν κάνεις search μέσω URI, το πρώτο αποτέλεσμα είναι ήδη επιλεγμένο.
        # Πατώντας Enter δύο φορές, ξεκινάει η αναπαραγωγή!
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        return f"Sir, I have searched for '{search_query}' on Spotify and initiated playback."
    except Exception as e:
        return f"I encountered an error trying to play '{search_query}' on Spotify: {str(e)}"

@tool
def play_youtube(search_query: str) -> str:
    """
    Use this tool to play any song, video, or playlist on YouTube.
    Provide the video name or artist as the search_query (e.g., 'drake hotline bling', 'lofi beats').
    """
    try:
        # Η pywhatkit αναλαμβάνει να βρει το πιο σχετικό βίντεο και να το παίξει αυτόματα στον browser σου!
        pywhatkit.playonyt(search_query)
        return f"Sir, I have searched for '{search_query}' on YouTube. It should be playing now."
    except Exception as e:
        return f"I encountered an error trying to play '{search_query}' on YouTube: {str(e)}"

@tool
def system_power(action: str) -> str:
    """
    Use this tool for system power commands.
    Action can be 'lock', 'sleep', or 'shutdown'.
    """
    try:
        if action == 'lock':
            # subprocess.run is the modern, secure replacement for os.system
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
            return "The workstation has been locked, Sir."
        elif action == 'sleep':
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
            return "Entering sleep mode, Sir."
        elif action == 'shutdown':
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
            return "Shutting down the system. Goodbye, Sir."
        return "Unknown power command, Sir."
    except subprocess.CalledProcessError as e:
        return f"Failed to execute power command securely: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def open_settings(setting_name: str) -> str:
    """
    Use this tool to instantly open specific Windows settings like 'bluetooth', 'wifi', or 'display'.
    """
    try:
        if setting_name == 'bluetooth':
            # os.startfile is the safest native way to open Windows URIs
            os.startfile("ms-settings:bluetooth")
            return "Sir, the Bluetooth settings panel is now open on your screen."
        elif setting_name == 'wifi':
            os.startfile("ms-settings:network-wifi")
            return "Sir, I have opened the Wi-Fi settings."
        elif setting_name == 'display':
            os.startfile("ms-settings:display")
            return "Sir, the display settings are open."
        return "I cannot find that setting panel, Sir."
    except Exception as e:
        return f"Error opening settings: {str(e)}"