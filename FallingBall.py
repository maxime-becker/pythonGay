import pygame
import random
import math

class DirectedBall:
    def __init__(self, screen_width, screen_height, radius=10, color=(0, 255, 0)):
        """Initialise la balle avec une position aléatoire sur les bords de l'écran, et un mouvement vers le centre."""
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = True
        self.speed = 0.1  # Vitesse très faible (0.001 pixels par milliseconde)

        # Position initiale sur un bord aléatoire
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.x = random.randint(self.radius, screen_width - self.radius)
            self.y = -self.radius  # Position en haut de l'écran
        elif edge == 'bottom':
            self.x = random.randint(self.radius, screen_width - self.radius)
            self.y = screen_height + self.radius  # Position en bas de l'écran
        elif edge == 'left':
            self.x = -self.radius
            self.y = random.randint(self.radius, screen_height - self.radius)  # Position à gauche
        elif edge == 'right':
            self.x = screen_width + self.radius
            self.y = random.randint(self.radius, screen_height - self.radius)  # Position à droite

        # Cible : le centre de l'écran (centre du cercle principal)
        self.target_x = screen_width // 2
        self.target_y = screen_height // 2

    def update_position(self, dt, moving_element, score):
        """Déplace la balle vers le centre du cercle, incrémente le score si elle touche l'élément MovingElement."""
        if not self.visible:
            return

        # Calcul de la distance entre la balle et le centre
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.hypot(dx, dy)

        # Déplacement de la balle vers le centre en fonction de la vitesse
        if distance > self.speed * dt:
            self.x += (self.speed * dt) * dx / distance
            self.y += (self.speed * dt) * dy / distance
        else:
            # Si la balle atteint le centre, on la rend invisible
            self.x = self.target_x
            self.y = self.target_y
            self.visible = False  # La balle disparaît lorsqu'elle atteint le centre

        # Calcul de la distance entre la balle et l'élément MovingElement
        distance_to_element = math.hypot(self.x - moving_element.x, self.y - moving_element.y)

        # Vérification de la collision entre la balle et l'élément MovingElement
        if distance_to_element <= self.radius + moving_element.element_radius:
            self.visible = False  # La balle disparaît en cas de collision
            score.increment()  # Incrémente le score à chaque collision

    def draw(self, screen):
        """Dessine la balle si elle est visible."""
        if self.visible:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

