import pygame
import time

def read_score_from_file():
    try:
        with open("score.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def draw_secondary_window(score):
    # Initialiser la surface de l'écran secondaire
    # et dessiner le score et d'autres informations
    pass  # Remplacez ceci par votre logique de dessin

# Initialiser Pygame
pygame.init()

# Créer une fenêtre pour l'affichage secondaire
secondary_screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption('Tetris Score Screen')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lire le score du fichier
    score = read_score_from_file()

    # Dessiner sur l'écran secondaire
    draw_secondary_window(score)

    # Attente pour réduire la charge CPU
    time.sleep(0.1)

pygame.quit()