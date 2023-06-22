import pygame

import pygame

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None
        self.paused_time = None
        self.is_paused = False
        self.total_elapsed_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.paused_time = pygame.time.get_ticks()

    def resume(self): # resumes time
        if self.is_paused:
            self.is_paused = False
            elapsed_pause_time = pygame.time.get_ticks() - self.paused_time
            self.total_elapsed_time += elapsed_pause_time

    def toggle_pause(self):
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def reset(self):
        self.start_time = None
        self.paused_time = None
        self.is_paused = False
        self.total_elapsed_time = 0

    def update(self):
        if self.start_time is not None and not self.is_paused:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time - self.total_elapsed_time
            if elapsed_time >= self.duration:
                self.total_elapsed_time += elapsed_time - self.duration
                self.start_time = current_time - self.total_elapsed_time

    def is_expired(self):
        if self.start_time is not None and not self.is_paused:
            return pygame.time.get_ticks() - self.start_time - self.total_elapsed_time >= self.duration
        return False

    def get_remaining_time(self):
        if self.start_time is not None and not self.is_paused:
            remaining_time = self.duration - (pygame.time.get_ticks() - self.start_time - self.total_elapsed_time)
            return max(remaining_time, 0)
        return self.duration


