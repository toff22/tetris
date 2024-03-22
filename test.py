import os
import pygame
import time

os.putenv('SDL_FBDEV', '/dev/fb0')
os.environ["SDL_FBDEV"] = "/dev/fb0"
os.environ["SDL_VIDEODRIVER"] = "dummy"
# os.environ["SDL_VIDEODRIVER"] = "rpi"

pygame.init()
print(pygame.display.Info())
print(pygame.display.get_driver())

def refresh():
    fd = open("/dev/fb0","wb")
    fd.write(oled.get_buffer())
    fd.close()

oled = pygame.Surface((480, 480), 0, 16)
#lcd = pygame.display.set_mode((480, 320))
oled.fill((255, 0, 0))
#lcd.blit(oled,(0,0))
#pygame.display.update()
refresh()
time.sleep(1)
oled.fill((0, 255, 0))
#lcd.blit(oled,(0,0))
#pygame.display.update()
refresh()
time.sleep(1)
oled.fill((0, 0, 255))
#lcd.blit(oled,(0,0))
#pygame.display.update()
refresh()
time.sleep(1)
