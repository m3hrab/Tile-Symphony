import pygame 


class Settings():

    def __init__(self) -> None:
        # Screen settings
        pygame.mixer.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (0, 165, 207)
        self.caption = "Rummikub"
        self.time_left = 30

        # Player Racks settings
        self.player_rack_width = 1280
        self.player_rack_height = 190
        self.border_radius = 10
        self.border_color = (255, 255, 255)
        self.player_rack_color = (174, 209, 206)#(157, 207, 162) 
        self.player_rack = pygame.Surface((self.player_rack_width, self.player_rack_height))
        self.player_rack.fill(self.player_rack_color)
        self.player_rack.set_alpha(150)
        # Sounds 
        self.click_sound = pygame.mixer.Sound("assets/sounds/tiles.wav")
        self.tiles_sound = pygame.mixer.Sound("assets/sounds/tiles.wav")
        self.game_trun_sound = pygame.mixer.Sound("assets/sounds/game_turn.wav")


        # Draw Tiles on the Rack
        self.x = 30
        self.y = self.screen_height - 220

        # Background image
        self.bg_image = pygame.image.load("assets/images/start_screen.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        self.bg_image1 = pygame.image.load("assets/images/screen_1.png")
        self.bg_image1 = pygame.transform.scale(self.bg_image1, (self.screen_width, self.screen_height))
        self.bg_image2 = pygame.image.load("assets/images/background2.png")
        self.bg_image2 = pygame.transform.scale(self.bg_image2, (self.screen_width, self.screen_height))
        self.bg_rect = self.bg_image.get_rect()

    def draw_bg(self, screen, flag=0):
        if flag==1:
            screen.blit(self.bg_image, self.bg_rect)

        elif flag==2:
            screen.blit(self.bg_image1, self.bg_rect)
        else:
            screen.blit(self.bg_image2, self.bg_rect)

    def draw_racks(self, screen):
        # inner_rect = pygame.Rect(0, self.screen_height - (self.player_rack_height+30), self.screen_width, self.player_rack_height+30)
        # pygame.draw.rect(screen, self.player_rack_color, inner_rect)
        screen.blit(self.player_rack, (0, self.screen_height - (self.player_rack_height+30)))


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = (61, 118, 126)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        # Draw the button with outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 24)
            text = font.render(self.text, 1, (255, 255, 255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Check if the mouse position is over the button
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
    
class Label():
    def __init__(self, x, y, text, font_size=32, color=(255, 0, 0), Flag=False):
        self.font = pygame.font.Font("assets/font/Anton/Anton-Regular.ttf", font_size)
        self.text = self.font.render(text, True, color)
        self.position = (x, y)

    def update_text(self, text, color=(255, 0, 0)):
        self.text = self.font.render(text, True, color)

    def draw(self, screen):
        screen.blit(self.text, self.position)


class TextBox():

    def __init__(self, x, y, width, height, text = ''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)
        self.text = text
        self.text_surface = pygame.font.Font("assets/font/Anton/Anton-Regular.ttf", 26).render(text, True, (61, 118, 126))
        self.active = False
        self.indicator = pygame.Rect(x + width - 25, y + 60 , 20, 20)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
                self.indicator.y = self.rect.y+ 20
            else:
                self.active = False
                self.indicator.y = self.rect.y+ 20


        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # # Re-render the text
                self.text_surface = pygame.font.Font("assets/font/Anton/Anton-Regular.ttf", 26).render(self.text, True, (61, 118, 126))
    

    def draw(self, screen, flag=False):
        # pygame.draw.rect(screen, self.color, self.rect)
        if self.active:
            # pygame.draw.rect(screen, (0, 0, 0), self.indicator)
            pygame.draw.circle(screen, (61, 118, 126), (self.indicator.x+10, self.indicator.y+10), 10)
        # Blit the text.
        if flag:
            screen.blit(self.text_surface, (self.rect.x+50, self.rect.y+12))
        else:
            screen.blit(self.text_surface, (self.rect.x+65, self.rect.y+12))

        