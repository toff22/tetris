# 1.5inch RGB OLED Display Module 128x128 16-bit High Color SPI
# Interface SSD1351 Driver

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import subprocess as sp

os.environ['DISPLAY'] = ':0.0'
pygame.init()
pygame.font.init()

#### Get the size of the frame buffer (x, y, bits per pixels). ####
geom = sp.getoutput("fbset -fb /dev/fb0 | grep geometry").split()
xres, yres, bpp = int(geom[1]), int(geom[2]), int(geom[5])
print(xres, yres, bpp)  # bpp bits per pixel

#### Create surfaces with the same size as the display. ####  
oled = pygame.Surface((xres, yres), 0, bpp)
screen = pygame.display.set_mode((xres, yres))

#### Get some fonts and set font size ####
icfont = pygame.font.SysFont('inconsolata', 22)
djfont = pygame.font.SysFont('dejavusans', 20)
pbfont = pygame.font.SysFont('pibotolt', 16)
nsfont = pygame.font.SysFont('notoserif', 20)
llfont = pygame.font.SysFont('linuxlibertinedisplayo', 20)
bsfont = pygame.font.SysFont('bitstreamverasansmono', 18)
#print(pygame.font.get_fonts())

#### Define refresh SPI frame buffer ####
def refresh():
    fd = open("/dev/fb0","wb")
    fd.write(oled.get_buffer())
    fd.close()

#### Populate the surface with objects to be displayed ####
pygame.draw.rect(oled,(255,255,0),(4,22,38,42))
oled.blit(icfont.render('Hello!', True, (255,255,255)), (2, 1))
oled.blit(djfont.render('Hello!', True, (255,64,64)), (56, 2))
oled.blit(pbfont.render('Hello!', True, (128,255,128)), (56, 26))
oled.blit(nsfont.render('Hello!', True, (128,128,255)), (56, 46))
oled.blit(llfont.render('Hello!', True, (255,128,255)), (56, 74))
oled.blit(bsfont.render('Hello!', True, (255,255,255)), (56, 96))

#### Blit the surface to the screen ####
screen.blit(oled,(0,0))

#### Update the the displays ####
pygame.display.flip()
refresh()

pygame.event.clear()
#x = 1
#while x:
#    event = pygame.event.wait()
#    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
#        oled.fill((0, 0, 0))
#        refresh()
#        x = 0
#        pygame.quit()
