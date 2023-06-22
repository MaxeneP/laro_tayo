import pygame
from button import Button

def draw_game_end(score, surface):
    color = (166, 119, 60)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    
    rect_w, rect_h = 700, 500
    rect_x = (surface.get_width() - rect_w) // 2
    rect_y = (surface.get_height() - rect_h) // 2
    game_end_rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
    
    pygame.draw.rect(surface, color, game_end_rect)
    
    # game text
    game_end_text = font.render("Good Job! You're doing better!", True, text_color)
    game_end_text_rect = game_end_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
    surface.blit(game_end_text, game_end_text_rect)
    
    # score
    score_text = font.render(f"Score: {score}", True, text_color)
    score_rect = score_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 50))
    surface.blit(score_text, score_rect)

    # button creation
    
    # restart button
    restart_button_rect = pygame.Rect(rect_x + 190, rect_y + 370, 150, 50)
    restart_button = Button(restart_button_rect, "Try Again")
    
    # exit button
    exit_button_rect = pygame.Rect(rect_x + 400, rect_y + 370, 150, 50)
    exit_button = Button(exit_button_rect, "Exit Game")
    
    # Draw on screen
    restart_button.draw(surface)
    exit_button.draw(surface)

    return restart_button, exit_button
