import pygame

#Creation du cercle central 
class CentralCircle:
    def __init__(self, center_x, center_y, radius, color=(255, 255, 255)):
        """Initialise le cercle central avec un centre, un rayon, et une couleur."""
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        """Dessine le cercle central sur l'écran Pygame."""
        pygame.draw.circle(screen, self.color, (self.center_x, self.center_y), self.radius, 2)
