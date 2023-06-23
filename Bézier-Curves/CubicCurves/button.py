import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, group, display, text, pos, val):
        super().__init__(group)
        self.display = display
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.text = self.font.render(text, True, (240, 240, 240))
        self.textRect = self.text.get_rect()
        self.textRect.topleft = (pos[0] + 40, pos[1] + 7)
        self.rect = pygame.Rect(pos[0], pos[1], 30, 30)
        self.pos = pos
        self.enabled = val

    def update(self):
        self.display.blit(self.text, self.textRect)
        pygame.draw.rect(self.display, (23, 40, 52), self.rect)

        color = (10, 10, 10)
        if self.enabled:
            color = (10, 100, 80)

        pygame.draw.rect(self.display, color, pygame.Rect(self.pos[0] + 5, self.pos[1] + 5, 20, 20))

    def pressed(self):
        self.enabled = not self.enabled

    def set(self, val):
        self.enabled = val


ORANGE = (243, 170, 78)
DARK_BLUE = (17, 24, 32)
SEMI_DARK_BLUE = (47, 54, 62)
BLUE = (77, 84, 92)
