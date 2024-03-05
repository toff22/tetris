import os
import pygame
import random
import numpy as np
import random
import time

from adafruit_blinka.agnostic import detector

ON_RPI = detector.board.any_raspberry_pi
if ON_RPI:
    os.putenv('SDL_FBDEV', '/dev/fb0')

# Initialisation de Pygame
pygame.init()


# variables globales
frame_index = 0
last_update = pygame.time.get_ticks()



# Définit le mode vidéo en créant une fenêtre. Ajustez la taille selon vos besoins.
screen = pygame.display.set_mode((800, 600))  

def load_animation_images(relative_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    image_folder = os.path.join(base_path, relative_path)
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            images.append(pygame.image.load(image_path).convert_alpha())
    return images

# Chemin relatif à partir du répertoire du script courant
relative_path = 'images/animation/tetroj'
# Chemin relatif à partir du répertoire du script courant
animation_images_I = 'images/animation/tetroi'  # Pour la pièce I
animation_images_O = 'images/animation/tetroo'  # Pour la pièce O
animation_images_T = 'images/animation/tetrot'  # Pour la pièce T
animation_images_S = 'images/animation/tetros'  # Pour la pièce S
animation_images_Z = 'images/animation/tetroz'  # Pour la pièce Z
animation_images_J = 'images/animation/tetroj'  # Pour la pièce J
animation_images_L = 'images/animation/tetrol'  # Pour la pièce L

piece_animations = {
    'I': 'images/animation/tetroi',
    'O': 'images/animation/tetroo',
    'T': 'images/animation/tetrot',
    'S': 'images/animation/tetros',
    'Z': 'images/animation/tetroz',
    'J': 'images/animation/tetroj',
    'L': 'images/animation/tetrol'
}

animations_dict = {}
for piece, path in piece_animations.items():
    animations_dict[piece] = load_animation_images(path)

# Chemin vers votre fichier de police personnalisée
font_path = 'font/gameboy.ttf'

# Charger la police personnalisée à la taille désirée
custom_font = pygame.font.Font(font_path, 24)

#chargement des images
background_image = pygame.image.load('images/start_screen.png')
score_image = pygame.image.load('images/score.png')

def get_music_files(folder_path):
    """Retourne une liste des chemins complets de tous les fichiers musicaux dans le dossier spécifié."""
    music_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):  # Assurez-vous de filtrer par le bon type de fichier
            music_files.append(os.path.join(folder_path, filename))
    return music_files

line_clear_sound = pygame.mixer.Sound("sounds/line.mp3")
rotate_sound = pygame.mixer.Sound("sounds/rotate.mp3")
tetris_sound = pygame.mixer.Sound("sounds/tetris.mp3")
newpiece_sound = pygame.mixer.Sound("sounds/piece.mp3")
musicloop_sound = pygame.mixer.Sound("sounds/A-Type.mp3")
gameover_sound = pygame.mixer.Sound("sounds/GameOver.mp3")
sheep_sound = pygame.mixer.Sound("sounds/sheep.wav")

# Constantes

GRID_ROWS, GRID_COLS = 18, 10
if ON_RPI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 480, 480
    CELL_SIZE = 1516 // GRID_ROWS
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = (420 + 240 + 240), 758
    CELL_SIZE = 758 // GRID_ROWS
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

def play_next_track(music_files):
    """Charge et joue la prochaine piste musicale de manière aléatoire, sans bloquer le jeu."""
    if music_files:  # Vérifie si la liste n'est pas vide
        next_track = random.choice(music_files)  # Sélectionne une piste aléatoirement
        pygame.mixer.music.load(next_track)
        pygame.mixer.music.set_volume(0.6)  # Réglez le volume à 70%
        pygame.mixer.music.play()

# def play_playlist(music_files):
#     """Commence la lecture de la première piste de la playlist et planifie les suivantes."""
#     if not music_files:
#         print("Aucune musique trouvée dans la playlist.")
#         return
#     pygame.mixer.music.load(music_files[0])
#     pygame.mixer.music.play()
#     for i in range(1, len(music_files)):
#         pygame.mixer.music.queue(music_files[i])
    
# Définit l'action à entreprendre lorsque la musique actuelle se termine
def music_end_event():
    play_next_track(current_music_files)  # Joue la prochaine piste musicale aléatoirement

def setup_playlist(music_files):
    """Configure la playlist pour jouer les pistes musicales en aléatoire."""
    if not music_files:
        print("Aucune musique trouvée dans la playlist.")
        return
    global current_music_files
    current_music_files = music_files
    play_next_track(music_files)  # Joue une première piste musicale aléatoirement

    # Associe l'événement de fin de musique à la fonction music_end_event
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    # pygame.event.custom_type()  # Génère un nouveau type d'événement unique
    # pygame.event.set_blocked(pygame.USEREVENT + 1)  # Bloque cet événement pour éviter sa propagation

def music_selection_screen():
    running = True
    music_options = ["Original", "Megademo"]
    current_selection = 0
    music_folder_path = 'sounds/megademo/'
    playlist_files = get_music_files(music_folder_path)

     # Utiliser custom_font ici pour rendre le texte
    font_path = 'font/gameboy.ttf'  # Remplacez par le chemin correct de votre police
    custom_font = pygame.font.Font(font_path, 24)  # Charger la police personnalisée
    


    while running:

        # header_text = custom_font.render('Start with', True, (255, 255, 255))  # Blanc

        screen.fill(BLACK)

        # Dessiner l'image de fond
        screen.blit(background_image, (0, 0))

        # Utiliser custom_font ici pour rendre le texte
        header_text = custom_font.render('MUSIC TYPE', True, (255, 255, 255))  # Blanc
        screen.blit(header_text, (132, 120))  # Modifier (100, 50) pour ajuster la position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(music_options)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(music_options)
                elif event.key == pygame.K_RETURN:
                    if current_selection == 0:  # A-Track sélectionné
                        pygame.mixer.music.load("sounds/A-Type.mp3")
                        pygame.mixer.music.play(-1)
                    elif current_selection == 1:  # B-Track sélectionné
                        setup_playlist(playlist_files)
                    running = False

        custom_font = pygame.font.Font(font_path, 24)
        for i, option in enumerate(music_options):
            text = custom_font.render(option, True, WHITE if i == current_selection else (100, 100, 100))
            screen.blit(text, (150, 170 + i * 30))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def highscore_screen(score):
    running = True
    while running:
        screen.fill(BLACK)
        # Dessiner l'image de fond
        screen.blit(score_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                    running = False

        custom_font = pygame.font.Font(font_path, 24)
        text_score_label = custom_font.render("HIGHSCORE<", True, WHITE)
        text_score = custom_font.render(f"{score}", True, BLACK)
        text_restart = custom_font.render("A to Restart", True, WHITE)
        screen.blit(text_score, (120, 226))
        screen.blit(text_score_label, (120, 160))
        screen.blit(text_restart, (110, 290))

        pygame.display.flip()
        pygame.time.Clock().tick(30)       

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

if ON_RPI:
    os.environ["SDL_VIDEODRIVER"] = "dummy" #dummy display for pygame joystick usage
    import board
    import neopixel
    import subprocess
    from luma.led_matrix.device import max7219
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core.virtual import viewport
    from luma.core.legacy import text, show_message
    from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

    os.putenv('SDL_FBDEV', '/dev/fb0')

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, blocks_arranged_in_reverse_order=True)
    pixel_pin = board.D18
    # The number of NeoPixels
    num_pixels = GRID_ROWS * GRID_COLS
    ORDER = neopixel.GRB
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.6, auto_write=False,pixel_order=ORDER)
    # pixels.fill((255, 255, 255))
    # pixels.show()


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
    inc = 0  # Nombre de lignes supprimées
    indices_to_remove = []

    # Identifier les lignes complètes à supprimer
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if 0 not in row:
            inc += 1
            indices_to_remove.append(i)
            # Supprimer les positions verrouillées dans la ligne complète
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # Déplacer les lignes supérieures vers le bas
    if inc > 0:
        for i in range(len(grid) - 1, -1, -1):
            if i in indices_to_remove:
                continue

            for j in range(len(grid[i])):
                if (j, i) in locked:
                    move_down = sum(1 for x in indices_to_remove if x > i)
                    new_key = (j, i + move_down)
                    locked[new_key] = locked.pop((j, i))

        # Recréer la grille avec les positions verrouillées mises à jour
        grid = create_grid(locked)

     # Jouer les sons appropriés en fonction du nombre de lignes supprimées
    if inc > 0:
        if inc == 4:
            tetris_sound.play()
        else:
            line_clear_sound.play()
    else:
        newpiece_sound.play()

    return grid, locked, inc





def draw_window(surface, grid, score, next_piece):
    surface.fill(BLACK)
    if ON_RPI:
        pixels.fill((0, 0, 0))

    # Dessiner chaque cellule de la grille
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if not ON_RPI:
                pygame.draw.rect(surface, grid[i][j], 
                                (GRID_ORIGIN[0] + j * CELL_SIZE, 
                                GRID_ORIGIN[1] + i * CELL_SIZE, 
                                CELL_SIZE, CELL_SIZE), 0)
            else:
                # Draw on LED
                # print("led")
                if (j>=0 and i>=0):
                    if j%2==1:
                        pixels[j*GRID_ROWS+i] = grid[i][j]
                    else:
                        pixels[j*GRID_ROWS+(GRID_ROWS-1-i)] = grid[i][j]

    # Dessiner la pièce suivante
    # draw_next_shape(surface, next_piece)
    if ON_RPI:
        draw_next_piece_animation(screen, next_piece.shape_type, 0, 0, pygame.time.get_ticks())
    else:
        draw_next_piece_animation(screen, next_piece.shape_type, 420, 0, pygame.time.get_ticks())

    # Afficher le score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)

    if ON_RPI:
        surface.blit(label, (10, 10))
    else:
        surface.blit(label, (GRID_ORIGIN[0] + GRID_COLS * CELL_SIZE + 10, 10))

    # Mettre à jour l'affichage
    pygame.display.update()
    if ON_RPI:
        pixels.show()
    
def calculate_score(num_lines, level):
    score_values = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
    return score_values[num_lines] * (level + 1)

 
    
def adjust_fall_speed(level):
    base_speed = 0.1  # Vitesse de base pour le niveau 0
    speed_increase_per_level = 0.1  # Augmentation de la vitesse par niveau

    # Calculer la nouvelle vitesse en fonction du niveau
    fall_speed = max(base_speed - (level * speed_increase_per_level), 0.1)  # Vitesse minimale de 0.1
    global fast_fall_speed  # Déclarer fast_fall_speed comme une variable globale pour la mettre à jour
    fast_fall_speed = adjust_fast_fall_speed(fall_speed)  # Ajuster la vitesse de chute rapide
    return fall_speed

def adjust_fast_fall_speed(normal_fall_speed):
    # Faire la chute rapide 5 fois plus rapide que la chute normale
    return normal_fall_speed * 0.1

fast_fall_speed = adjust_fast_fall_speed(adjust_fall_speed(0))

def draw_next_shape(surface, shape):
    # Calculer la position centrale en largeur sur l'écran
    if ON_RPI:
        center_x = 240
    else:
        center_x = SCREEN_WIDTH - 120
    preview_x = center_x - (2 * CELL_SIZE)  # Centrer la pièce de 4 cellules de large
    preview_y = 2 * CELL_SIZE  # Position Y pour la 3ème rangée

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


def draw_next_piece_animation(surface, shape_type, x, y, current_time):
    global frame_index, last_update
    images = animations_dict[shape_type]  # Utilisez les images depuis le dictionnaire

    # Mise à jour de l'index de frame et de la dernière mise à jour
    if current_time - last_update > (1000 / 20):  # Ajustez la durée selon vos besoins
        frame_index += 1
        last_update = current_time
        if frame_index >= len(images):
            frame_index = 0
    
    # Ajouter une vérification pour éviter l'erreur 'list index out of range'
    if frame_index < len(images):  # S'assurer que l'index est dans la plage
        # Affichage de l'image actuelle
        surface.blit(images[frame_index], (x, y))


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

global joystick
global joystick_detected   
def detect_joystick():
    joystick_detected=False
    clock = pygame.time.Clock()
    pygame.joystick.init()
    while joystick_detected==False:
        print("Waiting for controller...")
        pygame.joystick.quit()
        try:
            joystick = pygame.joystick.Joystick(0) # create a joystick instance
            joystick.init() # init instance
            print("Initialized joystick: {}".format(joystick.get_name()))
            joystick_detected = True
        except pygame.error:
            print("no joystick found.")
            joystick_detected = False
        clock.tick(1)



def main():

    while True:  # Boucle principale pour permettre le redémarrage du jeu
        detect_joystick()
        music_selection_screen()  # Laisser l'utilisateur choisir la musique avant de démarrer

        locked_positions = {}  # Initialiser locked_positions pour la nouvelle partie
        score = 0  # Initialiser le score à 0 pour chaque nouvelle partie
        level = 0  # Réinitialiser le niveau
        game_over = False

        current_piece = get_shape()
        next_piece = get_shape()
        clock = pygame.time.Clock()
        fall_time = 0

        while not game_over:  # Boucle de jeu tant que le jeu n'est pas terminé
            # Ici, vous pouvez utiliser locked_positions sans souci puisqu'elle a été initialisée
            # Logique de jeu, gestion des événements, affichage, etc.

            if check_lost(locked_positions):
                game_over = True
                draw_game_over_animation(win, locked_positions)  # Assurez-vous de passer les arguments corrects
                highscore_screen(score)


            # animation_images = load_animation_images('images/animation/tetroj')
            #musicloop_sound.play(-1)

            locked_positions = {}
            grid = create_grid(locked_positions)

            change_piece = False
            run = True
            current_piece = get_shape()
            next_piece = get_shape()
            clock = pygame.time.Clock()
            fall_time = 0
            frame_index = 0
            last_update = pygame.time.get_ticks()
            score = 0
            level = 0
            fall_speed = adjust_fall_speed(level)

            key_down_pressed_time = None  # Pour suivre le temps depuis que la touche bas a été pressée

            game_over = False  # Ajout d'une nouvelle variable pour suivre l'état de game over

            while run:
                if joystick_detected==False:
                    print("Waiting for controller...")
                    pygame.joystick.quit()
                    try:
                        joystick = pygame.joystick.Joystick(0) # create a joystick instance
                        joystick.init() # init instance
                        print("Initialized joystick: {}".format(joystick.get_name()))
                        joystick_detected = True
                    except pygame.error:
                        print("no joystick found.")
                        joystick_detected = False

                current_time = pygame.time.get_ticks()
                # Autre logique de jeu...

                grid = create_grid(locked_positions)
                fall_time += clock.get_rawtime()
                clock.tick(60)

                for event in pygame.event.get():
                    print("event: %s (%s)", event.type, pygame.USEREVENT + 1)
                    # Ajoute un gestionnaire pour l'événement de fin de musique
                    if event.type == pygame.USEREVENT + 1:  # Vérifie si l'événement de fin de musique est détecté
                        music_end_event()

                    if event.type == pygame.JOYBUTTONDOWN:
                        print("Initialized joystick: {}".format(event.button))

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
                            # À ce point, nous ne bougeons pas la pièce vers le bas immédiatement
                            # mais ajustons la vitesse de chute à fast_fall_speed
                            fall_speed = fast_fall_speed

                        elif event.key == pygame.K_UP:
                            rotate_sound.play()
                            original_position = (current_piece.x, current_piece.y)
                            original_rotation = current_piece.rotation
                            current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)

                            # Ajustement pour la pièce "I" lors de la rotation
                            if current_piece.shape_type == 'I':
                                if current_piece.rotation % 2 == 0:  # Rotation horizontale
                                    current_piece.x -= 2
                                else:  # Rotation verticale
                                    current_piece.x += 2

                            # Vérifier si la pièce est toujours dans la grille après la rotation et l'ajustement
                            if not valid_space(current_piece, grid):
                                # Tenter de déplacer la pièce pour qu'elle reste dans les limites de la grille
                                for dx in [-1, 1, -2, 2]:  # Essayer de déplacer de deux cases dans chaque direction
                                    current_piece.x += dx
                                    if valid_space(current_piece, grid):
                                        break
                                    current_piece.x -= dx

                            # Si la pièce ne peut toujours pas être placée, annuler la rotation et l'ajustement
                            if not valid_space(current_piece, grid):
                                current_piece.x, current_piece.y = original_position
                                current_piece.rotation = original_rotation

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            # Réinitialiser la vitesse de chute à la valeur normale basée sur le niveau
                            fall_speed = adjust_fall_speed(level)

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

                # Vérification de la condition de défaite
                if check_lost(locked_positions) and not game_over:
                    game_over = True  # Marquer le jeu comme terminé
                    pygame.mixer.music.stop()  # Arrête la musique actuelle
                    sheep_sound.play()  # Jouer le son de game over une seule fois
                    pygame.time.delay(800)  # Court délai avant de démarrer l'animation
                    draw_game_over_animation(win, grid)
                    # La ligne suivante assure qu'on ne passe dans cette section qu'une seule fois
                    pygame.time.delay(1000)  # Attente après l'animation pour voir l'écran final
                    print("Game Over! Final Score:", score, "Final Level:", level)
                    # highscore_screen(score)  # Afficher l'écran des scores ici peut-être
                    # Pas besoin de répéter le dessin de l'animation ou de jouer le son à nouveau ici
                
                if game_over:
                    # draw_game_over_animation(screen, grid)  # Utilisez 'screen' et non 'win'
                    # pygame.time.delay(2000)  # Temps d'attente après l'animation de fin
                    highscore_screen(score)  # Appel à l'écran des scores
                    run = False  # Arrêter la boucle principale du jeu
            
            pygame.quit()
            # pygame.display.quit()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main()