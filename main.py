import pygame 
from settings import Settings
from startscreen import StartScreen
from game_screen import GameScreen
import game_functions as gf

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)

    # Create the start screen and game screen
    startscreen = StartScreen(screen, settings)
    gamescreen = GameScreen(screen, settings)
    
    # Set the current Screen to the start screen
    current_screen = startscreen

    # Start the main loop for the game
    while True:

        if current_screen == startscreen:
            current_screen = gf.handle_start_screen_events(startscreen, gamescreen, settings)
        
        # Handle every keyboard and mouse event in the game
        gf.handle_events(current_screen, gamescreen, settings)
        # Update the screen
        gf.update_screen(screen, settings, current_screen, gamescreen)

run_game()