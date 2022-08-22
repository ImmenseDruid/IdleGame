import pygame
from settings import *

class Button():

    def __init__(self, x, y, width, height):
        self.hovered = False
        self.clicked = False
        self.prev_clicked = False
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN
        self.normal_color = GREEN
        self.hovered_color = BLUE
        self.clicked_color = RED
    
    def draw(self, screen):

        self.clicked = False
        self.hovered = False
        self.color = self.normal_color

        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            self.hovered = True
            self.color = self.hovered_color

        if self.hovered and pygame.mouse.get_pressed()[0] and not self.prev_clicked:
            self.clicked = True
            self.hovered = False
            self.prev_clicked = True
            self.color = self.clicked_color

        if not pygame.mouse.get_pressed()[0]:
            self.prev_clicked = False

        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, self.color, (self.rect.x + 5, self.rect.y + 5, self.rect.w - 10, self.rect.h - 10))
    
        return self.clicked

class Progress_Bar():
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.percent = 0
        self.time = 10
        self.time_to_complete = 10
        self.original_time = 10
        self.active = False

    def set_time(self, new_time):
        self.time = new_time
        self.time_to_complete = new_time
        self.original_time = new_time

    def activate(self):
        self.active = True

    
    def update(self):
        if self.active:
            if self.time <= 0:
                self.time = self.time_to_complete
                self.active = False
                return True
            else:
                self.time -= UPDATE_TIME
                self.percent = 1 - self.time / self.time_to_complete

        return False


    def draw(self, screen):
        
        pygame.draw.rect(self.image, PROGRESS_BAR_BACKGROUND, (0, 0, self.image.get_width(), self.image.get_height()))

        pygame.draw.rect(self.image, PROGRESS_BAR_FOREGROUND, (0, 0, self.image.get_width() * self.percent, self.image.get_height()))

        screen.blit(self.image, self.rect.topleft)


