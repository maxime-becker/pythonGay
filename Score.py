import pygame 

class Score:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.value}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

