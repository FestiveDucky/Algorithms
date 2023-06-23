import pygame, time

WALL = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, startx, starty, SIZE, borderless):
        super().__init__()
        self.size = SIZE
        self.x = startx
        self.y = starty
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 0, 255))
        if not borderless:
            self.size += 1
        self.rect = self.image.get_rect(x=startx * self.size, y=starty * self.size)

    def update(self, map):
        keys = pygame.key.get_pressed()
        speedx = 0
        speedy = 0

        if keys[pygame.K_w]:
            if 0 < self.y - 1:
                if map[self.y - 1, self.x + speedx] != WALL:
                    speedy = -1

        if keys[pygame.K_s]:
            if self.y + 1 < len(map) - 1:
                if map[self.y + 1, self.x + speedx] != WALL:
                    speedy = 1

        if keys[pygame.K_a]:
            if 0 < self.x - 1:
                if map[self.y + speedy, self.x - 1] != WALL:
                    speedx = -1

        if keys[pygame.K_d]:
            if self.x + 1 < len(map[0]) - 1:
                if map[self.y + speedy, self.x + 1] != WALL:
                    speedx = 1

        if (speedy, speedx) != (0,0):
            self.rect.x += speedx * self.size
            self.x += speedx
            self.rect.y += speedy * self.size
            self.y += speedy
