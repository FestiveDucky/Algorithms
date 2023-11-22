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
        self.colorFood = 0
        self.colorHome = 0
        self.rect = pygame.Rect(self.coords[1] * scale, self.coords[0] * scale, scale, scale)

    def update(self, screen, fullRefresh):
        newColorFood = screen.boardFood[self.coords[0]][self.coords[1]]
        newColorHome = screen.boardHome[self.coords[0]][self.coords[1]]

        # If the new color is not significantly different than we don't update
        if not fullRefresh and abs(self.colorFood - newColorFood) < 0.02 and abs(self.colorHome - newColorHome) < 0.02:
            return

        # Set the pixels to black if they have too little color
        if newColorFood < 0.01:
            screen.boardFood[self.coords[0]][self.coords[1]] = 0
            newColorFood = 0
        if newColorHome < 0.01:
            screen.boardHome[self.coords[0]][self.coords[1]] = 0
            newColorHome = 0

        self.colorHome = newColorHome
        self.colorFood = newColorFood
        pygame.draw.rect(screen.canvas, (self.colorHome * 255, self.colorFood * 255, self.colorFood * 255), self.rect)


class Nest(pygame.sprite.Sprite):
    def __init__(self, group, coords, scale):
        super().__init__(group)
        self.coords = coords
        self.scale = scale
        self.storedFood = 0
        self.rect = pygame.Rect(self.coords[1] * scale, self.coords[0] * scale, scale, scale)

    def update(self, screen):
        # Creating new agents with food
        foodRequired = 1
        for i in range(self.storedFood//foodRequired):
            self.storedFood -= foodRequired
            screen.agents.append(Agent(screen.agent_group, self.coords, screen.speed))

        pygame.draw.rect(screen.canvas, (99, 49, 0), self.rect)


class Food(pygame.sprite.Sprite):
    def __init__(self, group, coords, scale, quantity):
        super().__init__(group)
        self.coords = coords
        self.scale = scale
        self.quantity = quantity
        self.rect = pygame.Rect(self.coords[1] * scale, self.coords[0] * scale, scale, scale)

    def update(self, screen):
        if self.quantity <= 0:
            screen.food.remove(self)
            self.kill()
        pygame.draw.rect(screen.canvas, (239, 155, 15), self.rect)


class Screen:
    def __init__(self, num_agents, length, height, scale, speed, display):
        self.num_agents = num_agents
        self.length = length
        self.height = height
        self.speed = speed
        self.tile_length = self.length // scale
        self.tile_height = self.height // scale
        self.canvas = pygame.Surface((length, height))
        self.boardFood = numpy.zeros((self.tile_height, self.tile_length))
        self.boardHome = numpy.zeros((self.tile_height, self.tile_length))
        self.agents = []
        self.display = display
        self.agent_group = pygame.sprite.Group()
        self.food_group = pygame.sprite.Group()
        self.food = []
        self.nest_group = pygame.sprite.Group()
        self.nests = []
        self.tiles_dict = {}
        self.tile_group = pygame.sprite.LayeredUpdates()
        self.scale = scale
        self.count = 0

        # Create tiles
        for y in range(self.tile_height):
            for x in range(self.tile_length):
                self.tiles_dict[(y, x)] = Tile(self.tile_group, (y, x), scale)

        # Create food
        for y in range(10):
            for x in range(10):
                self.food.append(Food(self.food_group, (1+y, 1+x), scale, 100))

        for y in range(10):
            for x in range(10):
                self.food.append(Food(self.food_group, (y + 1, self.tile_length + x - 11), scale, 100))

        # Create nest
        for y in range(10):
            for x in range(10):
                self.nests.append(Nest(self.nest_group, (self.tile_height - 12 + y, self.tile_length - 120 + x), scale))

        # Create agents
        for agent in range(self.num_agents):
            self.agents.append(Agent(self.agent_group, random.choice(self.nests).coords, self.speed))

        # self.agents[1].angle = 45
        # self.agents[1].coords = (1, 1)
        # self.agents[1].trigCoords = (1, 1)
        # self.agents[1].carryingFood = True
        # Random position: (random.randint(0, self.tile_height), random.randint(0, self.tile_length))

    def average(self, warp):
        self.count += 1
        # kernel = numpy.asarray([[0.00, 0.11, 0.00],
        #                         [0.11, 0.5, 0.11],
        #                         [0.00, 0.11, 0.00]])
        kernel = numpy.asarray([[0.00, 0.047, 0.00],
                                [0.047, 0.8, 0.047],
                                [0.00, 0.047, 0.00]])
        kernel = numpy.asarray([[0.00, 0.01, 0.00],
                                [0.01, 0.92, 0.01],
                                [0.00, 0.01, 0.00]])
        # kernel = numpy.asarray([[0.11, 0.11, 0.11],
        #                         [0.11, 0.11, 0.11],
        #                         [0.11, 0.11, 0.11]])
        # kernel = numpy.asarray([[0.992]])
        # start = time.time()
        if self.count % 2 == 0:
            self.boardFood = scipy.signal.fftconvolve(self.boardFood, kernel, 'same')
            self.boardHome = scipy.signal.fftconvolve(self.boardHome, kernel, 'same')
        # print(f"FFT Convolve: {time.time() - start}")

        start = time.time()
        # Draw all of the tiles to the screen
        if not warp:
            self.tile_group.update(self, self.count % 300 == 0)
        print(f"Draw Pixels: {time.time()-start}")
        # #2 TODO subdivide screen and decide on which pixels to update
        # #1.5 Try just predicting which cells will become blended and just add those to the update list

        self.food_group.update(self)
        self.nest_group.update(self)

        self.display.blit(self.canvas, (0, 0))
        print(len(self.agents))

    def move(self):
        self.agent_group.update(self)
