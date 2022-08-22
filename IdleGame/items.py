import pygame
from pygame.locals import *
from settings import *
from ui import *

pygame.init()
pygame.font.init()

FONT = pygame.font.Font(pygame.font.get_default_font(), 16)
FONT_20 = pygame.font.Font(pygame.font.get_default_font(), 20)

def draw_string(screen, string, position, color = BLACK):
    image = FONT.render(string, False, color)
    screen.blit(image, (position[0] - image.get_width() / 2, position[1] - image.get_height() / 2))

def draw_text(screen, text, position):
    screen.blit(text, (position[0] - text.get_width() / 2, position[1] - text.get_height() / 2))

class Item():

    def __init__(self, groups, x, y, reward = 10, time_to_complete = 1, cost_to_upgrade = 10, purchase_cost = 100, operating_cost = 0):
        # Add self to all the groups required
        for group in groups:
            group.append(self)
        
        #All Local Variables
        self.reward = reward
        self.original_reward = reward
        self.upgrade_cost = cost_to_upgrade
        self.upgrade_level = 0
        self.purchase_cost = purchase_cost
        self.operating_cost = operating_cost
        
        # UI Elements
        self.activation_button = Button(x, y, 50, 50)
       
        self.pb = Progress_Bar(x + 60, y, 200, 50)
        self.pb.original_time = time_to_complete
        self.pb.time_to_complete = time_to_complete
        self.pb.time = time_to_complete
        
        self.upgrade_button = Button(x + 270, y, 100, 50)
        self.purchase_button = Button(x, y, 370, 50)

    def update(self):
        if self.pb.update():
            return self.reward
        else:
            return 0

    def upgrade(self):
        self.upgrade_level += 1
        self.reward = self.original_reward * self.upgrade_level
        self.upgrade_cost += self.upgrade_level * self.upgrade_level

    def draw(self, screen):
        return_value = 0

        if self.upgrade_level > 0:

            if self.activation_button.draw(screen):
                self.pb.activate()

            self.pb.draw(screen)
            draw_string(screen, f"{int(self.pb.time)}", self.pb.rect.center, WHITE)

            if self.upgrade_button.draw(screen):
                return_value = self.upgrade_cost
                

            draw_string(screen, f"${self.upgrade_cost}", self.upgrade_button.rect.center, WHITE)
        else:

            if self.purchase_button.draw(screen):
                return_value = self.purchase_cost

            draw_string(screen, f"${self.purchase_cost}", self.purchase_button.rect.center, WHITE)

        return return_value


