import pygame
from time import sleep
import pygame._sdl2.audio as sdl2_audio

def get_devices(capture_devices):
    init_by_me = not pygame.mixer.get_init()
    if init_by_me:
        pygame.mixer.init()
    devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
    if init_by_me:
        pygame.mixer.quit()
    return devices

devices = get_devices(False)
for device in devices:
    print("Device: {}".format(device))

pygame.mixer.init(devicename="Plantronics Blackwire 5220 Seri, USB Audio")
#pygame.mixer.music.load("sounds/A-Type.ogg")
#pygame.mixer.music.play()

rotate_sound = pygame.mixer.Sound("sounds/rotate.ogg")

while True:
    rotate_sound.play()
    sleep(1)
