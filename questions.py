import pygame

class Questions:
    def __init__(self, rect, text, correct_answer):
        self.rect = rect
        self.text = text
        self.correct_answer = correct_answer
        self.color = (166, 119, 60)
        self.font = pygame.font.Font(None, 50)

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, self.rect)
        lines = self.wrap_text(self.text, self.font, self.rect.width - 40)  # Wrap text into multiple lines
        
        y = self.rect.y + 40  # Starting y-coordinate for top alignment
        
        for line in lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midtop=(self.rect.centerx, y))  # Use centerx and midtop to align text at the top center of the rectangle
            WIN.blit(text_surface, text_rect)
            y += self.font.get_height() + 10  # Increment y-coordinate for the next line

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] < max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
