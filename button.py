import pygame

class Button:
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text
        self.color = (218, 180, 157)
        self.font = pygame.font.Font(None, 36) # font for button
        self.disabled = False # button is not disabled
    
    def draw(self, WIN, disabled=False):
        if disabled:
            self.color = (187, 153, 132)
        else:
            self.color = (218, 180, 157)
            
        pygame.draw.rect(WIN, self.color, self.rect) # draws button rectangle
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)