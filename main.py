import pygame 
from settings import Settings
from main_menu import MainMenu
from startscreen import GameMenu
from game import Game
import game_functions as gf

def play():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)

    mainmenu = MainMenu(screen, settings)
    gamemenu = GameMenu(screen, settings)
    game = Game(screen, settings)
    
    current_screen = mainmenu

    while True:

        if current_screen == mainmenu:
            current_screen = gf.handle_start_screen_events(1,mainmenu, gamemenu, game, settings)

        elif current_screen == gamemenu:
            current_screen = gf.handle_start_screen_events(2, mainmenu, gamemenu, game, settings)

        elif current_screen == game:
            gf.handle_events(current_screen, game, settings)
            gf.update_screen(screen, settings, current_screen, game)
            
        elif current_screen == 'q':
            pygame.quit()
            break

if __name__ == '__main__':
    play()