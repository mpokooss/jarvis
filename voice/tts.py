import asyncio
import edge_tts
import pygame
import os

def speak(text: str):
    """Μετατρέπει το κείμενο σε ομιλία χρησιμοποιώντας δωρεάν Neural Voices."""
    print("[J.A.R.V.I.S. μιλάει...]")
    
    # Η βρετανική ανδρική φωνή (Ryan)
    voice = "en-GB-RyanNeural"
    output_file = "temp_response.mp3"
    
    # Ασύγχρονη δημιουργία του αρχείου ήχου
    async def generate_audio():
        communicate = edge_tts.Communicate(text, voice, rate="+5%")
        await communicate.save(output_file)
        
    asyncio.run(generate_audio())
    
    # Αναπαραγωγή του ήχου
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # Περιμένουμε να τελειώσει η ομιλία
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    # Κλείνουμε το αρχείο και το διαγράφουμε για να μην γεμίζει ο δίσκος
    pygame.mixer.quit()
    try:
        os.remove(output_file)
    except:
        pass