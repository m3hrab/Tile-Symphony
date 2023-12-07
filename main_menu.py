import pygame

class MainMenu():

    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        x = settings.screen_width // 2 - 240
        y = settings.screen_height // 2 - 144
        self.play_btn = pygame.Rect(x+166, y+302, 155, 60)
        self.running = True


    def run_screen(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

                mouse_pos = pygame.mouse.get_pos()  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn.collidepoint(mouse_pos):
                        self.settings.click_sound.play()
                        return 1

            self.settings.draw_bg(self.screen, 2)
            pygame.display.flip()