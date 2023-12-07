import pygame
class Tile():

    def __init__(self, number, color):
        self.number = number
        self.color = color
        self.image = pygame.image.load(f'assets/card/{color}-{number}.png')
        self.image = pygame.transform.scale(self.image, (60, 75))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)