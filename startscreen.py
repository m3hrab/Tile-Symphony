import pygame
import sys
from settings import Label, TextBox

class GameMenu():

    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        x = settings.screen_width // 2 - 240
        y = settings.screen_height // 2 - 144
        self.player_name = TextBox(x, y, 540, 80)
        self.num_players = TextBox(x+215, y + 160, 115, 60)
        self.start_btn = pygame.Rect(x+190, y+352, 155, 60)
        self.running = True

        self.error_label = Label(x+190, y+280,'Invalid input!', 26)
        self.error = False


    def run_screen(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                self.player_name.handle_event(event)
                self.num_players.handle_event(event)

                mouse_pos = pygame.mouse.get_pos()  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_btn.collidepoint(mouse_pos):
                        self.settings.click_sound.play()
                        if self.player_name.text != '' and self.num_players.text.isdigit() and int(self.num_players.text) in [1, 2, 3]:
                            return [self.player_name.text, int(self.num_players.text)]
                        else:
                            self.error_label.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(1000)

            self.settings.draw_bg(self.screen, 1)
            self.player_name.draw(self.screen)
            self.num_players.draw(self.screen, True)
            pygame.display.flip()