import pygame, math


def calculate_new_coords(old_xy,speed,angle_in_radians):
    new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
    return (new_x, new_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 8), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.image = pygame.transform.rotate(self.image, direction)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = (x, y)
        self.direction = direction
        self.speed = speed

    def update(self, screen):
        self.pos = calculate_new_coords(self.pos, self.speed, math.radians(self.direction))
        print(round(self.pos[0]), round(self.pos[1]))
        self.rect.center = round(self.pos[0]), round(self.pos[1])
        if not screen.get_rect().colliderect(self.rect):
            self.kill()


pygame.init()
screen = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
spr = pygame.sprite.Group()
play = True
spr.add(Bullet(*screen.get_rect().center, 30, 1))
while play:
    clock.tick(1)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            play = False

    spr.update(screen)

    screen.fill((0, 0, 0))
    spr.draw(screen)
    pygame.draw.circle(screen, (64, 128, 255), screen.get_rect().center, 10)
    pygame.display.flip()

pygame.quit()
exit()