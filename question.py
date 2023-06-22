import pygame

class Question: # question box
    def __init__(self, rect, text, correct_answer):
        self.rect = rect
        self.text = text
        self.correct_answer = correct_answer
        self.color = (166, 119, 60)
        self.font = pygame.font.Font(None, 58)
        
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft= (250, 250))
        WIN.blit(text_surface, text_rect)