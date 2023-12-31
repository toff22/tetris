import pygame
import random
import numpy as np

# Initialisation de Pygame
pygame.init()

line_clear_sound = pygame.mixer.Sound("sounds/line.mp3")
rotate_sound = pygame.mixer.Sound("sounds/rotate.mp3")
tetris_sound = pygame.mixer.Sound("sounds/tetris.mp3")
newpiece_sound = pygame.mixer.Sound("sounds/piece.mp3")
musicloop_sound = pygame.mixer.Sound("sounds/A-Type.mp3")
gameover_sound = pygame.mixer.Sound("sounds/GameOver.mp3")
sheep_sound = pygame.mixer.Sound("sounds/sheep.wav")

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 420, 758
GRID_ROWS, GRID_COLS = 18, 10
CELL_SIZE = SCREEN_HEIGHT // GRID_ROWS
GRID_ORIGIN = (0, 0)

# Variable globale pour suivre le total des lignes effacées
total_lines_cleared = 0

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = {
    'I': (255, 255, 255),  # Blanc pur pour la pièce I
    'O': (255, 235, 205),  # Blanched Almond pour la pièce O
    'T': (245, 222, 179),  # Wheat pour la pièce T
    'S': (222, 184, 135),  # Burlywood pour la pièce S
    'Z': (210, 180, 140),  # Tan pour la pièce Z
    'J': (188, 143, 143),  # Rosy Brown pour la pièce J
    'L': (255, 218, 185)   # Pêche pour la pièce L
}


# Pièces de Tetris
TETRIMINOS = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], 
         [1], 
         [1], 
         [1]]
    ],
    'O': [
        [[2, 2], 
         [2, 2]]
    ],
    'T': [
        [[0, 3, 0], 
         [3, 3, 3]],
        [[3, 0], 
         [3, 3], 
         [3, 0]],
        [[3, 3, 3], 
         [0, 3, 0]],
        [[0, 3], 
         [3, 3], 
         [0, 3]]
    ],
    'S': [
        [[0, 4, 4], 
         [4, 4, 0]],
        [[4, 0], 
         [4, 4], 
         [0, 4]]
    ],
    'Z': [
        [[5, 5, 0], 
         [0, 5, 5]],
        [[0, 5], 
         [5, 5], 
         [5, 0]]
    ],
    'J': [
        [[6, 0, 0], 
         [6, 6, 6]],
        [[6, 6], 
         [6, 0], 
         [6, 0]],
        [[6, 6, 6], 
         [0, 0, 6]],
        [[0, 6], 
         [0, 6], 
         [6, 6]]
    ],
    'L': [
        [[0, 0, 7], 
         [7, 7, 7]],
        [[7, 0], 
         [7, 0], 
         [7, 7]],
        [[7, 7, 7], 
         [7, 0, 0]],
        [[7, 7], 
         [0, 7], 
         [0, 7]]
    ]
}


class Piece(object):
    def __init__(self, x, y, shape, shape_type):
        self.x = x
        self.y = y
        self.shape = shape
        self.shape_type = shape_type  # Ajoutez le type de la pièce
        self.color = COLORS[shape_type]
        self.rotation = 0

    def image(self):
        """
        Retourne la matrice représentant la forme de la pièce dans son état de rotation actuel.
        """
        return self.shape[self.rotation % len(self.shape)]

def create_grid(fixed_blocks):
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    for (x, y), color in fixed_blocks.items():
        if y < GRID_ROWS:
            grid[y][x] = color
    return grid


def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(GRID_COLS) if grid[i][j] == 0] for i in range(GRID_ROWS)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def convert_shape_format(piece):
    positions = []
    format = piece.image()

    for i, row in enumerate(format):
        for j, cell in enumerate(row):
            if cell != 0:
                positions.append((piece.x + j, piece.y + i))

    return positions

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    shape_type = random.choice(list(TETRIMINOS.keys()))  # Sélectionner une clé au hasard
    shape = TETRIMINOS[shape_type]
    shape_width = max(len(row) for row in shape[0])  # Calculer la largeur de la pièce
    start_x = GRID_COLS // 2 - shape_width // 2  # Position de départ au centre de la grille
    return Piece(start_x, 0, shape, shape_type)  # Utiliser la clé pour récupérer la pièce
    
def draw_grid(surface, grid):
    sx = GRID_ORIGIN[0]
    sy = GRID_ORIGIN[1]

    for i in range(len(grid)):
        pygame.draw.line(surface, WHITE, (sx, sy + i * CELL_SIZE), (sx + GRID_COLS * CELL_SIZE, sy + i * CELL_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, WHITE, (sx + j * CELL_SIZE, sy), (sx + j * CELL_SIZE, sy + GRID_ROWS * CELL_SIZE))

def update_score_and_level(score, lines_cleared, level):
    global total_lines_cleared
    total_lines_cleared += lines_cleared
    score += calculate_score(lines_cleared, level)
    level_lines = 10  # Nombre de lignes à effacer pour monter d'un niveau

    # Vérifier si le total des lignes effacées dépasse le seuil pour le niveau actuel
    if total_lines_cleared >= level_lines:
        level += 1
        total_lines_cleared -= level_lines  # Réduire le total des lignes pour le nouveau niveau

    return score, level

def clear_rows(grid, locked):
    inc = 0
    indices_to_remove = []

    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if 0 not in row:
            inc += 1
            indices_to_remove.append(i)
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # Jouer les sons appropriés en fonction du nombre de lignes supprimées
    if inc > 0:
        if inc == 4:
            tetris_sound.play()
        else:
            line_clear_sound.play()
    else:
        newpiece_sound.play()

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < indices_to_remove[-1]:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

        for i in range(inc):
            grid.insert(0, [0 for _ in range(GRID_COLS)])

             # Affiche le nombre total de lignes effacées dans la console
            print("Total de lignes effacées:", total_lines_cleared)

    return grid, locked, inc





def draw_window(surface, grid, score, next_piece):
    surface.fill(BLACK)

    # Dessiner chaque cellule de la grille
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], 
                             (GRID_ORIGIN[0] + j * CELL_SIZE, 
                              GRID_ORIGIN[1] + i * CELL_SIZE, 
                              CELL_SIZE, CELL_SIZE), 0)

    # Dessiner les lignes de la grille
    draw_grid(surface, grid)

    # Afficher le score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(label, (GRID_ORIGIN[0] + GRID_COLS * CELL_SIZE + 10, 20))

    # Dessiner la pièce suivante
    draw_next_shape(surface, next_piece)

    # Mettre à jour l'affichage
    pygame.display.update()

    
def calculate_score(num_lines, level):
    score_values = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
    return score_values[num_lines] * (level + 1)

 
    
def adjust_fall_speed(level):
    base_speed = 0.8  # Vitesse de base pour le niveau 0
    speed_increase_per_level = 0.1  # Augmentation de la vitesse par niveau

    # Calculer la nouvelle vitesse en fonction du niveau
    fall_speed = max(base_speed - (level * speed_increase_per_level), 0.1)  # Vitesse minimale de 0.1
    return fall_speed

def draw_next_shape(surface, shape):
    # Calculer la position centrale en largeur sur l'écran
    center_x = SCREEN_WIDTH // 2
    preview_x = center_x - (2 * CELL_SIZE)  # Centrer la pièce de 4 cellules de large
    preview_y = 3 * CELL_SIZE  # Position Y pour la 3ème rangée

    dark_grey = (70, 70, 70)  # Gris foncé pour la pièce suivante

    formatted_shape = shape.image()
    shape_width = max(len(row) for row in formatted_shape)
    offset_x = (4 - shape_width) // 2  # Centrer la pièce horizontalement dans l'aperçu

    for i, row in enumerate(formatted_shape):
        for j, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(surface, dark_grey, 
                                 (preview_x + (j + offset_x) * CELL_SIZE, 
                                  preview_y + i * CELL_SIZE, 
                                  CELL_SIZE, CELL_SIZE))

def write_score_to_file(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

def draw_game_over_animation(surface, grid):
    # Arrêter la musique
    musicloop_sound.stop()
    
    gameover_sound.play()

    # Remplir progressivement chaque ligne de blanc, case par case
    for i in range(GRID_ROWS - 1, -1, -1):
        for j in range(GRID_COLS):
            grid[i][j] = WHITE
            pygame.draw.rect(surface, WHITE, 
                             (GRID_ORIGIN[0] + j * CELL_SIZE, 
                              GRID_ORIGIN[1] + i * CELL_SIZE, 
                              CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            pygame.time.delay(5)  # Ajuster le délai pour contrôler la vitesse de l'animation

    # Ajouter un délai final pour permettre de voir l'écran rempli avant de quitter
    #pygame.time.delay(2000)


def main():
    musicloop_sound.play(-1)

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    score = 0
    level = 0
    fall_speed = adjust_fall_speed(level)

    key_down_pressed_time = None  # Pour suivre le temps depuis que la touche bas a été pressée

    game_over = False  # Ajout d'une nouvelle variable pour suivre l'état de game over

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    key_down_pressed_time = pygame.time.get_ticks()  # Marquer le temps du début de l'appui
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                        change_piece = True

                elif event.key == pygame.K_UP:
                    rotate_sound.play()
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    key_down_pressed_time = None  # Réinitialiser le suivi du temps d'appui

        if key_down_pressed_time:
            if pygame.time.get_ticks() - key_down_pressed_time > 200:
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1
                change_piece = True
                key_down_pressed_time = None

        if fall_time / 1000 > fall_speed and not change_piece:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            grid, locked_positions, lines_cleared = clear_rows(grid, locked_positions)
            score, level = update_score_and_level(score, lines_cleared, level)
            with open('score.txt', 'w') as f:
                f.write(f"{score},{level}")
            print("Score:", score, "Level:", level)
            fall_speed = adjust_fall_speed(level)

        draw_window(win, grid, score, next_piece)
        pygame.display.update()

         # Vérification de la condition de défaite
        if check_lost(locked_positions) and not game_over:
            game_over = True  # Marquer le jeu comme terminé
            musicloop_sound.stop()  # Arrêter la musique
            sheep_sound.play()  # Jouer le son de game over une seule fois
            pygame.time.delay(1000)  # Court délai avant de démarrer l'animation
            draw_game_over_animation(win, grid)
            pygame.time.delay(4000)  # Attente après l'animation pour voir l'écran final
            print("Game Over! Final Score:", score, "Final Level:", level)
            break  # Sortir de la boucle de jeu

    pygame.display.quit()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main()


