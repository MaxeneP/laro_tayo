import pygame

def draw_instructions(surface, rect):
    pygame.draw.rect(surface, (255, 255, 255), rect)
    
    # Draw instruction text
    instruction_font = pygame.font.Font(None, 30)
    instruction_text = "Game Instructions:\n\nThe goal of the Tumbang Preso is to knock down as many cans as you can by pressing on the correct answer for each question within the given time. Players have 3 slippers which are their number of chances to get the correct answer. If the timer runs out or the players lose all their slippers then it's game over! Try your best to answer all the questions correctly and get a perfect score!"
    instruction_surface = instruction_font.render(instruction_text, True, (0, 0, 0))
    instruction_rect = instruction_surface.get_rect(center=(rect.centerx, rect.centery - 50))
    surface.blit(instruction_surface, instruction_rect)
