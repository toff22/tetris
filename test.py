import os
import pygame
import sys

def load_animation_images(relative_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    image_folder = os.path.join(base_path, relative_path)
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            images.append(pygame.image.load(image_path).convert_alpha())
    return images

def main():
    pygame.init()
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Test d'Animation")
    
    relative_path = 'images/animation/tetroi'
    animation_images = load_animation_images(relative_path)
    
    clock = pygame.time.Clock()
    FPS = 60  # Le taux de rafraîchissement du jeu
    
    # Paramètres de l'animation
    animation_speed = 20  # Combien d'images par seconde pour l'animation
    animation_time = 1000 / animation_speed  # Temps en ms avant de changer d'image
    last_update = 0  # Quand la dernière image a été mise à jour
    
    current_frame = 0  # L'index de l'image actuelle de l'animation

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        now = pygame.time.get_ticks()
        if now - last_update > animation_time:
            last_update = now
            current_frame = (current_frame + 1) % len(animation_images)
        
        screen.fill((0, 0, 0))  # Efface l'écran avec du noir
        if animation_images:
            screen.blit(animation_images[current_frame], (0, 0))
        
        pygame.display.flip()
        
        clock.tick(FPS)  # Maintient le jeu à 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
