import pygame

# Playing assistant sound function
def playAssistantSound():
    pygame.mixer.init()
    music_dir = "www/assets/start_sound.mp3"
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()
    # Wait until the sound has finished playing
    while pygame.mixer.music.get_busy():
        continue