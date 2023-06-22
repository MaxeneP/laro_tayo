import pygame, sys
import mysql.connector
import random
from pygame.locals import *
from questions import Questions
from button import Button
from timer import Timer
from score import Scoreboard
from animator import Can
from game_end import draw_game_end

pygame.init()
pygame.mixer.init()

# Game window
WIN_W, WIN_H = 1166, 668
WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Trial 3")

# colors and img
bg_color = (193, 163, 127)
header = pygame.image.load("assets/header.png")
chance_full_img = pygame.image.load("assets/slipper_full.png")
chance_empty_img = pygame.image.load("assets/slipper_empty.png")

# sfx
correct_sfx = pygame.mixer.Sound('assets/Ping sound effect.mp3')
button_clicked_sfx = pygame.mixer.Sound('assets/button click.mp3')

# Defining Can sprite
can = Can(650, 160, 1.5)

# Score definition
scoreboard = Scoreboard()
user_id = sys.argv[1] if len(sys.argv) > 1 else None
conn = sys.argv[2] if len(sys.argv) > 2 else None

# Connect to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Admin1232022',
    database='laro_tayo'
)
c = conn.cursor()

# retrieves questions from the table
c.execute('SELECT question_text, correct_answer, choice_1, choice_2, choice_3, choice_4 FROM questions_s WHERE difficulty = 1')
easy_questions_data = c.fetchall()

c.execute('SELECT question_text, correct_answer, choice_1, choice_2, choice_3, choice_4 FROM questions_s WHERE difficulty = 2')
medium_questions_data = c.fetchall()

c.execute('SELECT question_text, correct_answer, choice_1, choice_2, choice_3, choice_4 FROM questions_s WHERE difficulty = 3')
hard_questions_data = c.fetchall()

# shuffles questions based on difficulty
random.shuffle(easy_questions_data)
random.shuffle(medium_questions_data)
random.shuffle(hard_questions_data)

# Question progression during the game
questions_data = easy_questions_data + medium_questions_data + hard_questions_data


# Create question box
question_y = 200

# Choices buttons and position
buttons = []

for i, (_, _, choice_1, choice_2, choice_3, choice_4) in enumerate(questions_data):
    button_1 = Button(pygame.Rect(180, 350, 120, 90), choice_1)
    button_2 = Button(pygame.Rect(370, 350, 120, 90), choice_2)
    button_3 = Button(pygame.Rect(180, 470, 120, 90), choice_3)
    button_4 = Button(pygame.Rect(370, 470, 120, 90), choice_4)
    buttons.append([button_1, button_2, button_3, button_4])
    for button in buttons[i]:
        button.disabled = False # initialize as enabled

def display_instructions():
    instructions_rect = pygame.Rect(80, 100, 1000, 408)  # Rectangle for instructions
    start_button_text = "Start"

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and start_button_rect.collidepoint(event.pos):
                return

        # Draw the instructions rectangle
        pygame.draw.rect(WIN, (166, 119, 60), instructions_rect)

        # Display the instructions text
        font = pygame.font.Font(None, 35)
        instructions_text = [
            "Welcome to the game!",
            "",
            "Instructions:",
            "",
            "The goal of the Tumbang Preso is to knock down as many cans as you can",
            "by pressing on the correct answer for each question within the given time.",
            "Players have 3 slippers which are their number of chances to get the",
            "correct answer. If the timer runs out or the players lose all their",
            "slippers then it's game over! Try your best to answer all the",
            "questions correctly and get a perfect score!",
        ]
        for i, line in enumerate(instructions_text):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(instructions_rect.centerx, instructions_rect.top + 50 + i * 30))
            WIN.blit(text_surface, text_rect)

        # Draw the start button
        start_button_rect = pygame.Rect(490, 550, 200, 70)  # Rectangle for start button
        pygame.draw.rect(WIN, (104, 186, 49), start_button_rect)
        start_button_font = pygame.font.Font(None, 40)
        start_button_surface = start_button_font.render(start_button_text, True, (255, 255, 255))
        start_button_rect = start_button_surface.get_rect(center=start_button_rect.center)
        WIN.blit(start_button_surface, start_button_rect)

        pygame.display.flip()
        WIN.fill(bg_color)

# When the user clicks the restart button:
def reset_game_state():
    global current_question, current_chances, can_proceed, answered_all_questions, timer_paused
    current_question = 0
    scoreboard.reset_score()
    timer.reset()
    current_chances = max_chances
    can_proceed = True
    answered_all_questions = False
    restart_button = None
    exit_button = None
    timer_paused = False # starts timer automatically upon reset
    timer.start()

running = True # If the game is running
current_question = 0
prev_question = None

# lives
max_chances = 3
current_chances = max_chances
can_proceed = True # proceed to the next question

# timer
timer = Timer(duration=180 * 1000) # 180 seconds * 1000 milliseconds
font = pygame.font.Font(None, 60) # font for the timer
timer_paused = False


answered_all_questions = False
questions = [] # questions list

timer_expired = False
timer_text = ""
total_time = 0


# Pause button variables
button_rect = pygame.Rect(1080, 35, 50, 50)
pause_button_img = pygame.image.load('assets/pause_button.png')
button_img = pause_button_img
button_pressed = False

restart_button = None
exit_button = None

# Sound
pygame.mixer.music.load('assets/bg_music.mp3')
pygame.mixer.music.set_volume(0.4)  # Set volume to 0.5
pygame.mixer.music.play(-1)

game_start = False
# Main game loop
while running:
    if not game_start:
        display_instructions()
        game_start = True
        timer.start()
        
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        # When the user presses on a button:
        if event.type == MOUSEBUTTONDOWN and not button_pressed and can_proceed and not answered_all_questions:
            for button in buttons[current_question]:
                if button.rect.collidepoint(event.pos) and not timer_paused:
                    button_pressed = True
                    button_clicked_sfx.play()
                    
                    # If user chooses the correct answer:
                    if button.text == questions[current_question].correct_answer:
                        print("Correct")
                        can.play_correct_animation(WIN)
                        scoreboard.increase_score()

                        if current_question + 1 < len(questions):
                            current_question += 1 # proceeds to the next question
                            questions[current_question].rect.y = question_y

                        else: # If all questions are answered, the timer pauses
                            answered_all_questions = True
                            timer.pause()

                        current_chances = max_chances
                        correct_sfx.play() # plays the sound

                    else: # If the user chooses the wrong answer
                        can.play_wrong_animation(WIN)
                        current_chances -= 1
                        print(f"Wrong. You have {current_chances} chances left.")
                        if current_chances <= 0:
                            can_proceed = False
                            print("No more chances")
                else:
                    button.disabled = timer_paused # If the timer is paused, the choices buttons are disabled

        if event.type == MOUSEBUTTONUP: # When the user releases their finger from the mouse
            button_pressed = False

        if event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
            button_pressed = True
            button_clicked_sfx.play()
            
            if timer_paused:
                timer.resume()
                timer_paused = False
                button_img = pause_button_img
                for button in buttons[current_question]:
                    button.disabled = False
            else:
                timer.pause()
                timer_paused = True
                button_img = pause_button_img
                for button in buttons[current_question]:
                    button.disabled = True
                
        if event.type == MOUSEBUTTONUP:
            button_pressed = False


        # Restart and Exit buttons functionality
        if event.type == MOUSEBUTTONDOWN and restart_button is not None and restart_button.rect.collidepoint(event.pos):
            total_time = timer.get_remaining_time()
            scoreboard.insert_science_score(conn, scoreboard.update_score(), total_time, user_id)
            reset_game_state()

        if event.type == MOUSEBUTTONDOWN and exit_button is not None and exit_button.rect.collidepoint(event.pos):
           total_time = timer.get_remaining_time()
           scoreboard.insert_science_score(conn, scoreboard.update_score(), total_time, user_id)
           running = False
            
    # Question box 
    if not questions:
        questions = [
            Questions(pygame.Rect(80, question_y + i * 150, 500, 400), question_text, correct_answer)
            for i, (question_text, correct_answer, choice_1, choice_2, choice_3, choice_4) in enumerate(questions_data)
        ]

    # Visuals of the screen
    WIN.fill(bg_color)
    WIN.blit(header, (0, 0))

    # Draws the buttons on the screen
    questions[current_question].draw(WIN)
    for button in buttons[current_question]:
        button.draw(WIN, disabled=button.disabled)
        
    if not timer.is_expired():
        timer.update()
    if timer.is_expired():
        timer_expired = True

    remaining_time = timer.get_remaining_time()
    if not timer_paused and remaining_time >= 0:
        minutes = remaining_time // 60000
        seconds = (remaining_time // 1000) % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        timer_surface = font.render(timer_text, True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(topleft=(137, 80))
        
    WIN.blit(timer_surface, timer_rect)

        
    # Slipper lives
    for i in range(current_chances):
        WIN.blit(chance_full_img, (700 + i * 90, 40))
    for i in range(current_chances, max_chances):
        WIN.blit(chance_empty_img, (700 + i * 90, 40))

    # Draws the can on the screen
    can.display(WIN)
    

    if answered_all_questions or current_chances <= 0:
        draw_game_end(scoreboard.update_score(), WIN)
        restart_button, exit_button = draw_game_end(scoreboard.update_score(), WIN)
    
    if timer.is_expired():
        draw_game_end(scoreboard.update_score(), WIN)
        restart_button, exit_button = draw_game_end(scoreboard.update_score(), WIN)
    
    if timer_paused: 
        pause_surface = pygame.Surface((770, 380))
        pause_surface.fill((166, 119, 60))
        WIN.blit(pause_surface, (200, 200))

            # Display "Paused" text
        paused_font = pygame.font.Font(None, 60)
        paused_text = paused_font.render("Game Paused", True, (255, 255, 255))
        paused_rect = paused_text.get_rect(center=(WIN_W // 2, WIN_H // 2 - 50))
        WIN.blit(paused_text, paused_rect)
        
        resume_font = pygame.font.Font(None, 50)
        resume_text = resume_font.render("Click the button again to resume.", True, (255, 255, 255))
        resume_rect = resume_text.get_rect(center=(WIN_W // 2, WIN_H // 2 + 100))
        WIN.blit(resume_text, resume_rect)

    WIN.blit(button_img, button_rect)

    scoreboard.draw(WIN, WIN_W, WIN_H)

    pygame.display.flip() # updates the screen

conn.close()

pygame.quit()
