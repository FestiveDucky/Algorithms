import numpy
import pygame, random, math, time

NOTHING = 0
AGENT = 1


def calculateNewCoords(coords, speed, angle_in_degrees):
    new_x = coords[1] + (speed*math.cos(math.radians(angle_in_degrees)))
    new_y = coords[0] + (speed*math.sin(math.radians(angle_in_degrees)))
    return new_y, new_x


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, coords, scale, speed):
        super().__init__(group)
        self.coords = coords
        self.trigCoords = coords
        self.speed = speed
        self.angle = None
        self.scale = scale
        self.agent = False
        self.new_agent = False
        self.removal = False

        # Plain
        self.color = (0, 0, 0)

        # Gradient
        # self.color = (coords[0] + coords[1], coords[0] + coords[1], coords[0] + coords[1])

        # Checker Board
        # if self.coords[0] % 2 == self.coords[1] % 2:
        #     self.color = (0, 0, 0)
        # else:
        #     self.color = (255, 255, 255)

        self.new_color = None
        self.image = pygame.Surface((scale, scale))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(x=self.coords[1] * scale, y=self.coords[0] * scale)

    def getColor(self):
        return self.color

    def move(self, tiles, height, length):
        next_trig_coords = calculateNewCoords(self.trigCoords, 1, self.angle)
        next_coords = tuple(map(round, next_trig_coords))

        angle_of_change = 20

        if height <= next_coords[0] or next_coords[0] <= -1 or -1 >= next_coords[1] or next_coords[1] >= length:
            if height <= next_coords[0] or next_coords[0] <= -1:
                self.angle = 360 - self.angle + random.randint(-angle_of_change, angle_of_change)
            if -1 >= next_coords[1] or next_coords[1] >= length:
                self.angle = 180 - self.angle + random.randint(-angle_of_change, angle_of_change)

            return self.move(tiles, height, length)

        tiles[next_coords].trigCoords = next_trig_coords
        tiles[next_coords].color = (255, 255, 255)
        tiles[next_coords].image.fill((255, 255, 255))
        self.agent = False
        tiles[next_coords].new_agent = True
        tiles[next_coords].angle = self.angle
        surrPoints = tiles[next_coords].getSurroundingTilesCoords(height, length) + [self.coords]
        return surrPoints

    def update(self, height, length, tiles):
        self.color = self.new_color
        self.image.fill(self.color)
        self.new_color = None
        if self.removal:
            for tile in self.getSurroundingTilesCoords(height, length):
                if tiles[tile].getColor() != (0, 0, 0):
                    self.removal = False

        if self.new_agent:
            self.new_agent = False
            self.agent = True

    def average(self, height, length, tiles, amount):
        r = self.color[0]
        g = self.color[1]
        b = self.color[2]

        divisor = 1

        for tile in self.getSurroundingTilesCoords(height, length):
            divisor += 1
            color = tiles[tile].getColor()

            r += color[0]
            g += color[1]
            b += color[2]

        new_color = (r // divisor, g // divisor, b // divisor)
        self.new_color = ((new_color[0] + 2 * self.color[0]) // 3, (new_color[1] + 2 * self.color[1]) // 3, (new_color[2] + 2 * self.color[2]) // 3)

        new_color = []
        for color_part in self.new_color:
            color_part -= amount
            if color_part < 0:
                new_color.append(0)
            else:
                new_color.append(color_part)

        if new_color == [0, 0, 0]:
            self.removal = True

        self.new_color = tuple(new_color)

    def getSurroundingTilesCoords(self, height, length):
        y = self.coords[0]
        x = self.coords[1]

        surrTiles = []

        for newy in (y - 1, y, y + 1):
            for newx in (x - 1, x, x + 1):
                if (newy, newx) != self.coords and height > newy > -1 and length > newx > -1:
                    surrTiles.append((newy, newx))

        return surrTiles


class Screen:
    def __init__(self, num_agents, length, height, scale, speed):
        self.num_agents = num_agents
        self.length = length
        self.height = height
        self.tile_length = self.length // scale
        self.tile_height = self.height // scale
        print(self.tile_height, self.tile_length)
        self.tiles_dict = {}
        self.grid = numpy.zeros((self.tile_height, self.tile_length))
        print(self.grid)
        self.tiles_to_check_coords = []
        self.tile_group = pygame.sprite.Group()

        for y in range(self.tile_height):
            for x in range(self.tile_length):
                self.tiles_dict[(y, x)] = Tile(self.tile_group, (y, x), scale, speed)

        for agent in range(self.num_agents):
            y = random.randint(0, self.tile_height-1)
            x = random.randint(0, self.tile_length-1)
            self.tiles_dict[(y, x)].angle = random.randint(0, 360)
            self.tiles_dict[(y, x)].agent = True
            self.tiles_dict[(y, x)].color = (255, 255, 255)

            self.tiles_to_check_coords += self.tiles_dict[(y, x)].getSurroundingTilesCoords(self.tile_height, self.tile_length)
            self.tiles_to_check_coords.append((y, x))
            self.tiles_to_check_coords = list(set(self.tiles_to_check_coords))

    def average(self, amount):
        start = time.time()
        print(len(self.tiles_to_check_coords))
        for coords in self.tiles_to_check_coords:
            self.tiles_dict[coords].average(self.tile_height, self.tile_length, self.tiles_dict, amount)
        print(f"Time to Average - {time.time() - start}")

        start = time.time()
        for coords in self.tiles_to_check_coords:
            self.tiles_dict[coords].update(self.tile_height, self.tile_length, self.tiles_dict)
        print(f"Time to Update - {time.time() - start}")

    def move(self):
        num_agents = 0
        added_tiles = []
        for coords in self.tiles_to_check_coords:
            if self.tiles_dict[coords].removal:
                self.tiles_to_check_coords.remove(coords)
                pass
            if self.tiles_dict[coords].agent:
                num_agents += 1
                added_tiles += self.tiles_dict[coords].move(self.tiles_dict, self.tile_height, self.tile_length)

        self.tiles_to_check_coords += added_tiles
        self.tiles_to_check_coords = list(set(self.tiles_to_check_coords))
        print(f"{num_agents} Agent(s) Left")

    def getTiles(self):
        return self.tiles_dict

    def getActiveCoords(self):
        return self.tiles_to_check_coords
