import pygame


class Agent(pygame.sprite.Sprite):
    def __init__(self, group, coords, scale, color):
        super().__init__(group)
        self.coords = coords
        self.color = color
        self.image = pygame.Surface((scale, scale))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(x=self.coords[1] * scale, y=self.coords[0] * scale)
