import os
import pygame

ON_RPI = True
print("ON_RPI: %s", ON_RPI)
if ON_RPI:
    os.putenv('SDL_FBDEV', '/dev/fb0')
    os.putenv("SDL_VIDEODRIVER", "fbcon")

pygame.init()

BLACK = (0, 0, 0)
background_image = pygame.image.load('images/start_screen.png')
screen = pygame.display.set_mode((480, 480))  

while True:
    # Dessiner l'image de fond
    screen.blit(background_image, (0, 0))
    pygame.display.update()