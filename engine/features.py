import pygame
import eel
# Initialize pygame mixer module
pygame.mixer.init()

# Playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/start_sound.mp3"
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)