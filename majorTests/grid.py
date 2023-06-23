import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.points = pygame.sprite.Group()


class Grid:
    def __init__(self, width, height):
        self.cell_group = pygame.sprite.LayeredUpdates()
