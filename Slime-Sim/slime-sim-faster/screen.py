import numpy
import pygame, random, math, time
import scipy

from agent import *
NOTHING = 0
AGENT = 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, coords, scale):
        super().__init__(group)
        self.coords = coords
        self.scale = scale
        self.agent = False
        self.new_agent = False
        self.removal = False

        # Plain
        self.color = 0

        # Gradient
        # self.color = (coords[0] + coords[1], coords[0] + coords[1], coords[0] + coords[1])

        # Checker Board
        # if self.coords[0] % 2 == self.coords[1] % 2:
        #     self.color = (0, 0, 0)
        # else:
        #     self.color = (255, 255, 255)
        self.new_color = None
        # self.image = pygame.Surface((scale, scale))
        # self.image.fill(self.color)
        self.rect = pygame.Rect(self.coords[1] * scale, self.coords[0] * scale, scale, scale)

    def getColor(self):
        return self.color

    def update(self, screen):
        new_color = screen.board[self.coords[0]][self.coords[1]]
        if new_color == self.color:
            return
        self.color = new_color
        if self.color < 0.0005:
            screen.board[self.coords[0]][self.coords[1]] = 0
        pygame.draw.rect(screen.canvas, (0, self.color * 255, self.color * 255), self.rect)
        # if color == 1:
        #     self.image.fill((120, 120, 120))
        # else:
        #     self.image.fill((color * 255, color * 255, color * 255))
        # screen.display.blit(self.image, self.rect)


    # def update(self, height, length, tiles):
    #     self.color = self.new_color
    #     self.image.fill(self.color)
    #     self.new_color = None
    #     if self.removal:
    #         for tile in self.getSurroundingTilesCoords(height, length):
    #             if tiles[tile].getColor() != (0, 0, 0):
    #                 self.removal = False
    #
    #     if self.new_agent:
    #         self.new_agent = False
    #         self.agent = True

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
    def __init__(self, num_agents, length, height, scale, speed, display):
        self.num_agents = num_agents
        self.length = length
        self.height = height
        self.speed = speed
        self.tile_length = self.length // scale
        self.tile_height = self.height // scale
        print(self.tile_height, self.tile_length)
        self.tiles_dict = {}
        self.canvas = pygame.Surface((length, height))
        self.board = numpy.zeros((self.tile_height, self.tile_length))
        self.tiles_to_check_coords = []
        self.agents = []
        self.following = None
        self.display = display
        self.tile_group = pygame.sprite.LayeredUpdates()
        self.agent_group = pygame.sprite.Group()

        for y in range(self.tile_height):
            for x in range(self.tile_length):
                self.tiles_dict[(y, x)] = Tile(self.tile_group, (y, x), scale)

        for agent in range(self.num_agents):
            self.agents.append(Agent(self.agent_group, (random.randint(0, self.tile_height), random.randint(0, self.tile_length)), self.speed))

    def average(self):
        # start = time.time()
        # kernel = numpy.asarray([[0.00, 0.11, 0.00],
        #                         [0.11, 0.5, 0.11],
        #                         [0.00, 0.11, 0.00]])
        kernel = numpy.asarray([[0.00, 0.06, 0.00],
                                [0.06, 0.7, 0.06],
                                [0.00, 0.06, 0.00]])
        # kernel = numpy.asarray([[0.11, 0.11, 0.11],
        #                         [0.11, 0.11, 0.11],
        #                         [0.11, 0.11, 0.11]])
        # kernel = numpy.asarray([[0.9]])
        # kernel = numpy.asarray([[0.08, 0.08, 0.08, 0.08],
        #                         [0.08, 0.08, 0.08, 0.08],
        #                         [0.08, 0.08, 0.08, 0.08]])
        self.board = scipy.signal.fftconvolve(self.board, kernel, 'same')
        # self.board = numpy.array(list(map(lambda x: [round(i, 4) for i in x], scipy.signal.fftconvolve(self.board, kernel, 'same'))))
        # print(f"Time to Average - {time.time() - start}")


        # start = time.time()
        self.tile_group.update(self)

        # Follow singular guy
        if self.following is not None:
            pygame.draw.rect(self.canvas, (255, 0, 0), self.tiles_dict[self.agents[self.following].coords].rect)



        self.display.blit(self.canvas, (0, 0))
        # print(f"Time to Update - {time.time() - start}")

    def move(self):
        self.agent_group.update(self)

    def getTiles(self):
        return self.tiles_dict

    def getActiveCoords(self):
        return self.tiles_to_check_coords
