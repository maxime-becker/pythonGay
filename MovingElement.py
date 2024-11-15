import pygame
import math

"""
La fonction math.atan2(dy, dx) permet de calculer l'angle en radians entre l'axe horizontal (l'axe x) 
et le segment de ligne qui relie le centre du cercle à la position de la souris. L'angle ainsi obtenu est 
utilisé pour positionner l'élément rond correctement sur la circonférence du cercle.
"""

class MovingElement:
    def __init__(self, center_x, center_y, radius, element_radius, color=(255, 0, 0)):
        """Initialise l'élément rond qui se déplace autour du cercle."""
        self.center_x = center_x
        self.center_y = center_y
        self.circle_radius = radius  # Rayon du cercle central
        self.element_radius = element_radius  # Rayon de l'élément rond
        self.color = color
        self.angle = 0  # Angle initial de l'élément rond
        self.speed = 0.05  # Vitesse de déplacement (ajustable)

    def update_position(self, mouse_x, mouse_y):
        """Met à jour la position de l'élément en fonction de la souris."""
        # Calcul de l'angle entre le centre du cercle et la souris
        dx = mouse_x - self.center_x
        dy = mouse_y - self.center_y
        angle = math.atan2(dy, dx)  # L'angle entre la souris et le centre

        # Déplacement de l'élément sur la circonférence du cercle
        self.angle = angle
        self.x = self.center_x + self.circle_radius * math.cos(self.angle)
        self.y = self.center_y + self.circle_radius * math.sin(self.angle)

    def draw(self, screen):
        """Dessine l'élément rond sur l'écran."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.element_radius)
