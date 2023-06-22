import pygame, pygame.mixer

class Can(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.x = x
        self.y = y
        self.scale = scale
        self.idle_img = pygame.image.load('assets/can.png').convert_alpha() #converts to match pizel format as the window
        self.image = self.idle_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.correct_animation = [ # sprite frames
            pygame.image.load('assets/falling/6.png').convert_alpha(),
            pygame.image.load('assets/falling/7.png').convert_alpha(),
            pygame.image.load('assets/falling/8.png').convert_alpha(),
            pygame.image.load('assets/falling/9.png').convert_alpha(),
            pygame.image.load('assets/falling/10.png').convert_alpha(),
            pygame.image.load('assets/falling/11.png').convert_alpha(),
        ]
        self.wrong_animation = [
            pygame.image.load('assets/shake/1.png').convert_alpha(),
            pygame.image.load('assets/shake/2.png').convert_alpha(),
            pygame.image.load('assets/shake/3.png').convert_alpha(),
            pygame.image.load('assets/shake/4.png').convert_alpha(),
            pygame.image.load('assets/shake/5.png').convert_alpha(),
        ]
        
        self.current_frame = None
        self.frame_index = 0
        self.animation_speed = 125
        
        self.image = pygame.transform.scale(self.idle_img, (int(self.idle_img.get_width() * self.scale), int(self.idle_img.get_height() * self.scale))) # image size
        self.rect = self.image.get_rect() # get image rectangle
        self.rect.x = x
        self.rect.y = y
        self.can_correct_sfx = pygame.mixer.Sound('assets/correct can sfx.mp3') # sfx
    
    def display(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
    def play_correct_animation(self, WIN):
        self.can_correct_sfx.play()
        self.play_animation(WIN, self.correct_animation)
    
    def play_wrong_animation(self, WIN):
        self.play_animation(WIN, self.wrong_animation)
    
    def play_animation(self, WIN, animation):
        for frame in animation:
            scaled_frame = pygame.transform.scale(frame, (int(frame.get_width() * self.scale), int(frame.get_height() * self.scale)))
            self.current_frame = frame
            WIN.blit(self.image, (self.x, self.y))
            WIN.blit(scaled_frame, (self.x, self.y))
            pygame.display.flip()
            pygame.time.delay(self.animation_speed)