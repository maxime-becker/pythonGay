import pygame, sys
from CentralCircle import CentralCircle
from MovingElement import MovingElement
from FallingBall import DirectedBall
from Score import Score
from button import Button 
import csv
import os
from csv_game_data_manager import CSVManager, GameStats
import math
from datetime import datetime

pygame.init()

# Variables de l'écran
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Chargement de l'image de fond
BG = pygame.image.load("assets/foggy.png")

# Initialisation du gestionnaire CSV
csv_manager = CSVManager(data_directory='data/')

def start_game(character_name):
    now = datetime.now()

    # Charger ou créer les statistiques du joueur
    game_stats = csv_manager.read_csv(character_name)

    # Création du cercle central
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    radius = 100  # Rayon du cercle
    central_circle = CentralCircle(center_x, center_y, radius, (255, 255, 255))

    # Création de l'élément rond
    element_radius = 10  # Rayon de l'élément
    moving_element = MovingElement(center_x, center_y, radius, element_radius, (255, 0, 0))

    # Création du score
    score = Score()

    # Liste des boules dirigées
    balls = []
    ball_radius = 10
    ball_count = 3  # Nombre initial de boules
    missed_balls = 0  # Counter for missed balls

    # Création initiale des boules
    for _ in range(ball_count):
        balls.append(DirectedBall(WIDTH, HEIGHT, ball_radius))

    # Bouton pour revenir au menu principal
    BACK_BUTTON = Button(image=None, pos=(500, 50), 
                         text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")

    # Variable pour garder le jeu en cours
    running = True
    clock = pygame.time.Clock()
    BACKGROUND_COLOR = (0, 0, 0)

    # Afficher un message de bienvenue avec le nom du personnage
    display_message(f"Bienvenue, {character_name}!", "White", (640, 50), 2000)

    frames = 0
    speedball = 0.001

    # Boucle principale du jeu
    while running:
            
        frames += 1

        if frames % 60 == 0:
            save_game_statistics(character_name, score.value, missed_balls, frames // 60)
            speedball += 0.00005

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    running = False  # Arrêter la boucle pour revenir au menu principal

        # Calcul du temps écoulé (delta time) pour la gestion de la vitesse
        dt = clock.get_time()

        # Récupère la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Met à jour la position de l'élément rond
        moving_element.update_position(mouse_x, mouse_y)

        # Met à jour la position des boules dirigées
        for ball in balls:
            ball.update_position(dt, moving_element, score)

        # Supprimer les boules invisibles et ajouter une nouvelle boule si nécessaire
        for ball in balls[:]:
            if not ball.visible:
             
                missed_balls += 1  # Incrémente seulement si la balle est manquée

                # Retirez la balle actuelle et ajoutez une nouvelle
                balls.remove(ball)
                balls.append(DirectedBall(WIDTH, HEIGHT, ball_radius))

            #Augmentez la vitesse des balles
            ball.speed += speedball ** 2
        # Condition de Game Over
        
        if missed_balls - score.value >= 10:
            display_message("Game Over!", "Red", (WIDTH // 2, HEIGHT // 2), 2000)
            main_menu()

        # Remplissage de l'arrière-plan
        SCREEN.fill(BACKGROUND_COLOR)

        # Dessin du cercle central
        central_circle.draw(SCREEN)

        # Dessin de l'élément rond
        moving_element.draw(SCREEN)

        # Dessin des boules dirigées
        for ball in balls:
            ball.draw(SCREEN)

        # Affichage du score
        score.draw(SCREEN)

        # Affichage des boules manquées
        font = pygame.font.Font(None, 36)
        actual_missed_balls = missed_balls - score.value  # Calculate actual missed balls
        missed_text = font.render(f"Missed Balls: {actual_missed_balls}", True, (255, 255, 255))
        missed_text_rect = missed_text.get_rect()
        missed_text_rect.topright = (WIDTH - 10, 10)  # Align text to the top-right corner
        SCREEN.blit(missed_text, missed_text_rect)

        # Dessin du bouton BACK
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)

        # Mise à jour de l'affichage
        pygame.display.flip()

        # Limite à 60 FPS
        clock.tick(120)

    # Retour au menu principal après la fin de la boucle
    main_menu()
    # Quitter Pygame
    pygame.quit()

def display_message(message, color, position, duration):
    font = pygame.font.Font(None, 40)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=position)
    SCREEN.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(duration)

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def save_name_to_csv(name):
    try:
        # Enregistrement du nom dans le fichier principal
        if not os.path.isfile('characters.csv'):
            with open('characters.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name"])  # En-tête du fichier

        with open('characters.csv', mode='r') as file:
            reader = csv.reader(file)
            existing_names = [row[0] for row in reader]
            if name in existing_names:
                print("Ce nom existe déjà.")
                return

        with open('characters.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name])
            print(f"Le nom '{name}' a été ajouté au fichier CSV.")

        # Création d'un fichier individuel pour les statistiques du joueur
        csv_manager.create_new_player(name)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")

def save_game_statistics(player_name, boules_touchees, boules_manquees, duree_partie):
    try:
        game_stats = csv_manager.read_csv(player_name)
        updated_stats = GameStats(
            name=game_stats.name,
            total_score=game_stats.total_score + boules_touchees,
            timeplayed=datetime.now(),
            game_played=game_stats.game_played + 1,
            score_per_game=(game_stats.total_score + boules_touchees) // (game_stats.game_played + 1),
            time_per_game=datetime.now()
        )
        with open(os.path.join(csv_manager.data_directory, f"{player_name}.csv"), mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                updated_stats.name,
                updated_stats.total_score,
                updated_stats.timeplayed.strftime('%Y-%m-%d %H:%M:%S'),
                updated_stats.game_played,
                updated_stats.score_per_game,
                updated_stats.time_per_game.strftime('%Y-%m-%d %H:%M:%S')
            ])
        print(f"Statistiques de la partie sauvegardées pour {player_name}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des statistiques : {e}")

def save_final_game_statistics(player_name, boules_touchees, boules_manquees):
    try:
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{player_name}-{current_time}.csv"
        with open(os.path.join(csv_manager.data_directory, file_name), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Total Score", "Time Played", "Games Played", "Score Per Game", "Time Per Game"])
            writer.writerow([
                player_name,
                boules_touchees,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                1,
                boules_touchees,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
        print(f"Statistiques finales de la partie enregistrées dans {file_name}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des statistiques finales : {e}")
    try:
        game_stats = csv_manager.read_csv(player_name)
        updated_stats = GameStats(
            name=game_stats.name,
            total_score=game_stats.total_score + boules_touchees,
            timeplayed=datetime.now(),
            game_played=game_stats.game_played + 1,
            score_per_game=(game_stats.total_score + boules_touchees) // (game_stats.game_played + 1),
            time_per_game=datetime.now()
        )
        with open(os.path.join(csv_manager.data_directory, f"{player_name}.csv"), mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                updated_stats.name,
                updated_stats.total_score,
                updated_stats.timeplayed.strftime('%Y-%m-%d %H:%M:%S'),
                updated_stats.game_played,
                updated_stats.score_per_game,
                updated_stats.time_per_game.strftime('%Y-%m-%d %H:%M:%S')
            ])
        print(f"Statistiques de la partie sauvegardées pour {player_name}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des statistiques : {e}")

def create_a_character_menu():
    input_text = ''
    font_input = pygame.font.Font(None, 50)
    name_input_rect = pygame.Rect(450, 300, 380, 50)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('gray')
    color = color_inactive
    active = False

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("CREATE A CHARACTER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        NAME_PROMPT = get_font(30).render("Veuillez entrer un nom:", True, "White")
        NAME_PROMPT_RECT = NAME_PROMPT.get_rect(center=(640, 250))
        SCREEN.blit(NAME_PROMPT, NAME_PROMPT_RECT)

        txt_surface = font_input.render(input_text, True, color)
        SCREEN.blit(txt_surface, (name_input_rect.x + 5, name_input_rect.y + 5))
        pygame.draw.rect(SCREEN, color, name_input_rect, 2)

        CONFIRM_BUTTON = Button(image=None, pos=(640, 450), 
                             text_input="CONFIRM", font=get_font(40), base_color="White", hovering_color="Green")
        CONFIRM_BUTTON.changeColor(MENU_MOUSE_POS)
        CONFIRM_BUTTON.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(640, 600), 
                           text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(MENU_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active = name_input_rect.collidepoint(event.pos)
                if CONFIRM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if input_text:
                        save_name_to_csv(input_text)
                    else:
                        display_message("Aucun nom entré.", (255, 0, 0), (640, 550), 3000)
                if PLAY_BACK.checkForInput(MENU_MOUSE_POS):
                    main_menu()
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    save_name_to_csv(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            color = color_active if active else color_inactive

        pygame.display.update()

def load_characters_from_csv():
    # Charger les noms des personnages depuis le fichier CSV
    if not os.path.isfile('characters.csv'):
        return []  # Si le fichier n'existe pas, retourner une liste vide
    
    try:
        with open('characters.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            characters = [row[0] for row in reader if row]  # Lire les noms des personnages
        return characters[1:]  # Ignorer la première ligne (en-tête)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return []

def character_selection_menu():
    characters = load_characters_from_csv()

    if not characters:
        display_message("Aucun personnage disponible.", "Red", (640, 360), 3000)
        return

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("SELECT A CHARACTER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Afficher la liste des personnages
        y_offset = 200
        buttons = []
        for character in characters:
            button = Button(image=None, pos=(640, y_offset), 
                            text_input=character, font=get_font(40), base_color="White", hovering_color="Green")
            buttons.append(button)
            y_offset += 60

        # Créer le bouton BACK
        PLAY_BACK = Button(image=None, pos=(640, 600), 
                           text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(MENU_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # c moche

            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, button in enumerate(buttons):
                    if button.checkForInput(MENU_MOUSE_POS):
                        selected_character = characters[index]
                        display_message(f"Character '{selected_character}' selected!", "White", (640, 500), 2000)
                        start_game(selected_character)  # Passer le nom du personnage à la fonction start_game
                        return
                if PLAY_BACK.checkForInput(MENU_MOUSE_POS):
                    main_menu()  # Retourner au menu principal

        pygame.display.update()

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT_OR = get_font(45).render("OR", True, "White")
        PLAY_RECT = PLAY_TEXT_OR.get_rect(center=(640, 300))
        SCREEN.blit(PLAY_TEXT_OR, PLAY_RECT)

        PLAY_CREATE_CHARACTER = Button(image=None, pos=(640, 200), 
                                       text_input="CREATE A CHARACTER", font=get_font(50), base_color="White", hovering_color="Green")
        PLAY_CREATE_CHARACTER.changeColor(PLAY_MOUSE_POS)
        PLAY_CREATE_CHARACTER.update(SCREEN)

        PLAY_CHOSE_CHARACTER = Button(image=None, pos=(640, 400), 
                                      text_input="CHOSE A CHARACTER", font=get_font(50), base_color="White", hovering_color="Green")
        PLAY_CHOSE_CHARACTER.changeColor(PLAY_MOUSE_POS)
        PLAY_CHOSE_CHARACTER.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(640, 600), 
                           text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif PLAY_CREATE_CHARACTER.checkForInput(PLAY_MOUSE_POS):
                    create_a_character_menu()  # Créer un menu de création
                elif PLAY_CHOSE_CHARACTER.checkForInput(PLAY_MOUSE_POS):
                    character_selection_menu()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Lancer le menu principal
main_menu()
