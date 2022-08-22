import pygame
from pygame.locals import *
from settings import *
from ui import *
from items import Item

pygame.init()
pygame.font.init()

FONT = pygame.font.Font(pygame.font.get_default_font(), 16)
FONT_20 = pygame.font.Font(pygame.font.get_default_font(), 20)

def draw_string(screen, string, position, color = BLACK):
    image = FONT.render(string, False, color)
    screen.blit(image, (position[0] - image.get_width() / 2, position[1] - image.get_height() / 2))

def draw_text(screen, text, position):
    screen.blit(text, (position[0] - text.get_width() / 2, position[1] - text.get_height() / 2))


def main():
    
    pygame.init()
    pygame.font.init()

   
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    current_screen = MAIN
    
    # Set Up the Different Groups
    items = []
    tabs = []
    tab_index = 0
    
    # Initiate The Items
    for j in range(5):
        tabs.append([])
        for i in range(5):
            reward = 10 + 5 * i + 30 * j
            time_to_complete = 2 * (i + 1) + 10 * j
            cost_to_upgrade = 100 * j + 10
            purchase_cost = 100 + i * 100 + j * 1000
            operating_cost = i * 10 + j * 100
            Item([items, tabs[j]], 100, 200 + 60 * i, reward, time_to_complete, cost_to_upgrade, purchase_cost, operating_cost)

    # Setup the buttons
    prev_button = Button(285 - 60, 130, 30, 30)
    next_button = Button(285 + 30, 130, 30, 30)
    
    # Menu Buttons
    main_screen_button = Button(SCREEN_WIDTH - 300, 90, 200, 50)
    upgrades_button = Button(SCREEN_WIDTH - 300, 150, 200, 50)
    
    
    # Progress Bars

    operating_cost_progress_bar = Progress_Bar(SCREEN_WIDTH - 300, 310, 200, 50)
    operating_cost_progress_bar.set_time(60)

    
    money = 100
    
    time_since_last_update = 0
    time_since_last_turn = 0
    current_update = pygame.time.get_ticks()
    
    total_operating_cost = 0

    run = True
    while run:
        last_update = current_update
        current_update = pygame.time.get_ticks()
        dt = current_update - last_update 
        time_since_last_update += dt
        time_since_last_turn += dt

        operating_cost_progress_bar.activate()

        if time_since_last_update >= UPDATE_TIME * 1000:
            time_since_last_update = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
            
            #update
            
            for item in items:
                money += item.update()
            


            if operating_cost_progress_bar.update():
                total_operating_cost = 0
                for item in items:
                    total_operating_cost += item.operating_cost * item.upgrade_level
                time_since_last_turn = 0
                money -= total_operating_cost

                operating_cost_progress_bar.activate()

            #draw

            screen.fill(BLACK)

            pygame.draw.rect(screen, WHITE, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

            if main_screen_button.draw(screen):
                current_screen = MAIN
            if upgrades_button.draw(screen):
                current_screen = UPGRADES

            draw_string(screen, f"Main", main_screen_button.rect.center)
            draw_string(screen, f"Upgrades", upgrades_button.rect.center)
            
            
            operating_cost_progress_bar.draw(screen)
            draw_string(screen, f"{int(operating_cost_progress_bar.time)}", operating_cost_progress_bar.rect.center)
            draw_string(screen, f"Time until Operation Cost Payment", (operating_cost_progress_bar.rect.centerx, operating_cost_progress_bar.rect.centery - operating_cost_progress_bar.rect.height - 10))
            draw_string(screen, f"{total_operating_cost}", (operating_cost_progress_bar.rect.centerx, operating_cost_progress_bar.rect.centery - operating_cost_progress_bar.rect.height + 15))
            # Draw main screen
            if current_screen == MAIN:
                pygame.draw.rect(screen, BLACK, (60, 60, 450, SCREEN_HEIGHT - 120), 20)
                
                draw_string(screen, f"${money}", (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100), BLACK)
                draw_string(screen, f"{tab_index + 1}", (285, 145), BLACK)
                if next_button.draw(screen):
                    #print("next")
                    tab_index += 1
                    if tab_index >= len(tabs):
                        tab_index = len(tabs) - 1

                if prev_button.draw(screen):
                    #print("prev")
                    tab_index -= 1
                    if tab_index < 0:
                        tab_index = 0
                

                for item in tabs[tab_index]:
                    cost = item.draw(screen)
                    if money >= cost:
                        money -= cost
                        if cost == item.upgrade_cost:
                            item.upgrade()
                        elif cost == item.purchase_cost:
                            item.upgrade_level = 1

            elif current_screen == UPGRADES:

                pygame.draw.rect(screen, BLACK, (60, 60, 450, 400), 20)

                
                
                

            pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
