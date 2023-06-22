import pygame

pygame.font.init()

class Scoreboard:
    def __init__(self): # initializes score variables
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        self.score_surface = self.font.render("", True, (255, 255, 255))
        self.score_rect = self.score_surface.get_rect()
        self.update_score()

    def increase_score(self):
        self.score += 1
        self.update_score()
        
    def reset_score(self):
        self.score = 0
        self.update_score()

    def update_score(self):
        score_text = f"Score: {self.score}" 
        self.score_surface = self.font.render(score_text, True, (255, 255, 255))
        self.score_rect = self.score_surface.get_rect()
        return self.score

        
    def draw(self, surface, WIN_W, WIN_H):
        self.score_rect.bottomright = (WIN_W - 20, WIN_H - 20)
        surface.blit(self.score_surface, self.score_rect)
    
    def format_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

    def insert_math_score(self, conn, math_score, total_time, user_id):
        formatted_time = self.format_time(total_time)
        if user_id is not None and math_score is not None:
            print("user_id:", user_id)
            print("math_score:", math_score)
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO score (user_id, math_score, total_time) VALUES (%s, %s, %s)", (user_id, math_score, formatted_time))
                conn.commit()
                cur.close()
                print('Math score inserted')
            except Exception as e:
                print('Failed to insert math score:', str(e))
        else:
            print('Failed to insert math score:', user_id, math_score, formatted_time)

    
    def insert_science_score(self, conn, science_score, total_time, user_id):
        formatted_time = self.format_time(total_time)
        if user_id is not None and science_score is not None:
            print("user_id:", user_id)
            print("science_score:", science_score)
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO score (user_id, science_score, total_time) VALUES (%s, %s, %s)", (user_id, science_score, total_time))
                conn.commit()
                cur.close()
                print('Science score inserted')
            except Exception as e:
                print('Failed to insert science score:', str(e))
        else:
            print('Failed to insert science score:', user_id, science_score, formatted_time)







