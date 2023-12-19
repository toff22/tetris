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


# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 420, 758
GRID_ROWS, GRID_COLS = 18, 10
CELL_SIZE = SCREEN_HEIGHT // GRID_ROWS
GRID_ORIGIN = (0, 0)

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = {
    'I': (0, 255, 255),  # Cyan pour la pièce I
    'O': (255, 255, 0),  # Jaune pour la pièce O
    'T': (128, 0, 128),  # Violet pour la pièce T
    'S': (0, 255, 0),    # Vert pour la pièce S
    'Z': (255, 0, 0),    # Rouge pour la pièce Z
    'J': (0, 0, 255),    # Bleu pour la pièce J
    'L': (255, 165, 0)   # Orange pour la pièce L
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
        print("shape: ", shape)
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
    return Piece(5, 0, TETRIMINOS[shape_type], shape_type)  # Utiliser la clé pour récupérer la pièce

def draw_grid(surface, grid):
    sx = GRID_ORIGIN[0]
    sy = GRID_ORIGIN[1]

    for i in range(len(grid)):
        pygame.draw.line(surface, WHITE, (sx, sy + i * CELL_SIZE), (sx + GRID_COLS * CELL_SIZE, sy + i * CELL_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, WHITE, (sx + j * CELL_SIZE, sy), (sx + j * CELL_SIZE, sy + GRID_ROWS * CELL_SIZE))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if 0 not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        line_clear_sound.play()
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    else:
        newpiece_sound.play()

def draw_window(surface, grid):
    surface.fill(BLACK)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (GRID_ORIGIN[0] + j * CELL_SIZE, GRID_ORIGIN[1] + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

    draw_grid(surface, grid)
    pygame.display.update()

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

    fall_speed = 0.27
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                # fall_speed -= 0.01
                change_piece = True

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
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    rotate_sound.play()
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

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
            clear_rows(grid, locked_positions)

        draw_window(win, grid)
        pygame.display.update()

        if check_lost(locked_positions):
            gameover_sound.play()
            # run = False

    # pygame.display.quit()

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main()
