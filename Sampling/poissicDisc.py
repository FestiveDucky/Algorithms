import pygame

from grid import *
from random import randint as ri
from random import choice as ch


one = False


class Cell(pygame.sprite.Sprite):
    def __init__(self, side_length, coords):
        super().__init__()
        self.side_length = side_length
        self.coords = coords
        self.point = None
        self.image = pygame.Surface((self.side_length - 1, self.side_length - 1))
        self.image.fill((30, 30, 30))
        self.rect = self.image.get_rect(x=self.coords[1] * self.side_length, y=self.coords[0] * self.side_length)

    def add_point(self, point):
        self.point = point

    def remove_point(self):
        self.point = None


class Sampling:
    def __init__(self, x1, y1, x2, y2, candidate_samples, inner_circle_radius, outer_circle_radius,
                 thickness, circle_size, display, display_sampling, border_points, num_start_points, start_center,
                 border_point_radius, draw_sampling, image, color_sampling):
        # x1, y1, x2, y2 are the dimensions on where to run the algorithm
        self.inner_circle_radius = inner_circle_radius
        self.outer_circle_radius = outer_circle_radius
        self.thickness = thickness
        self.color_sampling = color_sampling
        self.circle_size = circle_size
        self.points = []
        self.available_points = []
        self.start_points = num_start_points
        self.border_points = border_points
        self.display = display
        self.display_sampling = display_sampling
        self.draw_sampling = draw_sampling
        self.start_center = start_center
        self.border_point_radius = border_point_radius
        self.image = image

        if self.image is not None:
            y2, x2, a = image.shape

        self.x1 = x1
        self.y1 = y1

        self.cell_side_length = int(self.inner_circle_radius / math.sqrt(2))
        # Making the dimensions evenly divisble by the cell side length
        self.x2 = x2 // self.cell_side_length * self.cell_side_length
        self.y2 = y2 // self.cell_side_length * self.cell_side_length
        self.x1 = x1 // self.cell_side_length * self.cell_side_length
        self.y1 = y1 // self.cell_side_length * self.cell_side_length

        self.cell_borders_y = (self.y1 // self.cell_side_length, self.y2 // self.cell_side_length)
        self.cell_borders_x = (self.x1 // self.cell_side_length, self.x2 // self.cell_side_length)

        self.voronoi_polygons_map = np.zeros((self.cell_borders_y[1], self.cell_borders_x[1]))
        self.voronoi_polygons = []

        self.cells = {}
        self.available_cells = {}
        for y in range(self.cell_borders_y[0], self.cell_borders_y[1]):
            for x in range(self.cell_borders_x[0], self.cell_borders_x[1]):
                new_cell = Cell(self.cell_side_length, (y, x))
                self.cells[(y, x)] = new_cell
                self.available_cells[(y, x)] = new_cell

        self.createPoints(candidate_samples)

    def voronoiDiagram(self):
        for i in self.cells:
            if self.cells[i].point is not None:
                self.voronoi_polygons_map[i[0]][i[1]] = 1
                if self.image is not None:
                    color = tuple(reversed(self.image[self.cells[i].point[0]][self.cells[i].point[1]]))
                else:
                    color = (ri(0, 255), ri(0, 255), ri(0, 255))
                self.voronoi_polygons.append(
                    Polygon(self.cells[i], self.cell_borders_x, self.cell_borders_y, self.cell_side_length, color))

        # for i in range(10):
        #     print("==========")
        #     self.voronoi_polygons[i].find_vertices(self.display, self.voronoi_polygons_map, self.cells)
        if one:
            self.voronoi_polygons[len(self.voronoi_polygons)//2].find_vertices(self.display, self.voronoi_polygons_map, self.cells)
        else:
            for poly in self.voronoi_polygons:
                print(self.voronoi_polygons.index(poly))
                poly.find_vertices(self.display, self.voronoi_polygons_map, self.cells)

                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.QUIT:
                        pygame.quit()

    def draw(self, specific_point, all=False):
        if self.draw_sampling:
            if all:
                self.display.fill((0, 0, 0))
                # for cell in self.available_cells:
                #     self.display.blit(self.available_cells[cell].image, self.available_cells[cell].rect)

                for point in self.points:
                    if point in self.available_points:
                        color = (255, 255, 255)
                        # Draw green square
                        # pygame.draw.rect(self.gamedisplay, (0, 255, 0), pygame.Rect(point[1] - self.inner_circle_radius,
                        #                                                             point[0] - self.inner_circle_radius,
                        #                                                             self.inner_circle_radius * 2,
                        #                                                             self.inner_circle_radius * 2), 3)
                    else:
                        if self.image is not None and self.color_sampling:
                            color = tuple(reversed(self.image[point[0]][point[1]]))
                        else:
                            color = (255, 0, 0)
                    pygame.draw.circle(self.display, color, (point[1], point[0]), self.circle_size,
                                       self.thickness)
            else:
                if specific_point in self.available_points:
                    color = (255, 255, 255)
                    # Draw green square
                    # pygame.draw.rect(self.gamedisplay, (0, 255, 0),
                    #                  pygame.Rect(specific_point[1] - self.inner_circle_radius,
                    #                              specific_point[0] - self.inner_circle_radius,
                    #                              self.inner_circle_radius * 2,
                    #                              self.inner_circle_radius * 2), 3)

                else:
                    if self.image is not None and self.color_sampling:
                        color = tuple(reversed(self.image[specific_point[0]][specific_point[1]]))
                    else:
                        color = (255, 0, 0)
                pygame.draw.circle(self.display, color, (specific_point[1], specific_point[0]),
                                   self.circle_size, self.thickness)
            pygame.display.update()

    def checkEvents(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()

    def getPoints(self):
        return self.points

    def distance(self, other_point, current_point):
        vector = (current_point[0] - other_point[0], current_point[1] - other_point[1])
        dis = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        return dis

    def createPoints(self, candidate_samples):
        # Starting point
        if self.start_center:
            current_point = ((self.y2 - self.y1) // 2 + self.y1, (self.x2 - self.x1) // 2 + self.x1)
        else:
            current_point = (ri(self.y1, self.y2 - 1), ri(self.x1, self.x2 - 1))
        current_cell = (int(current_point[0] / self.cell_side_length), int(current_point[1] / self.cell_side_length))
        self.cells[current_cell].add_point(current_point)
        self.points.append(current_point)
        self.available_cells.pop(current_cell)
        self.available_points.append(current_point)

        while True:
            self.sampling(candidate_samples, current_point)
            if len(self.available_points) > 0:
                if self.start_points is None or len(self.points) < self.start_points:
                    current_point = ch(self.available_points)
                elif len(self.points) >= self.start_points:
                    break
            else:
                break

    def sampling(self, candidate_samples, current_point):
        for i in range(candidate_samples):
            self.checkEvents()

            angle = ri(1, 360)
            distance = ri(self.inner_circle_radius, self.outer_circle_radius)
            new_candidate = new_point(angle, current_point, distance)
            if self.distance(tuple(map(round, new_candidate)), current_point) > self.outer_circle_radius:
                new_candidate = tuple(map(int, new_candidate))
            else:
                new_candidate = tuple(map(round, new_candidate))

            if self.y2 <= new_candidate[0] or new_candidate[0] < self.y1 or self.x2 <= new_candidate[1] or \
                    new_candidate[1] < self.x1:
                continue

            failed = False
            if self.border_points is not None:
                percentage = 0.05
                skip_by = int(len(self.border_points) * percentage)
                list_to_check = self.border_points[:]
                while True:
                    closest = []
                    final = False
                    if skip_by <= 1:
                        final = True
                        skip_by = 1

                    for coords in list_to_check[0::skip_by]:
                        dis = self.distance((coords[1], coords[0]), new_candidate)
                        if len(closest) == 0:
                            closest = [coords, dis]
                        else:
                            if dis < closest[1]:
                                closest = [coords, dis]

                    if final:
                        if closest[1] < self.border_point_radius:
                            failed = True
                        break

                    index = list_to_check.index(closest[0])
                    if index < skip_by:
                        first = index
                        second = skip_by + 1
                    elif index >= len(self.border_points) - skip_by:
                        first = skip_by
                        second = (len(self.border_points) - index) + 1
                    else:
                        first = skip_by
                        second = skip_by + 1
                    list_to_check = list_to_check[index - first:index + second][:]
                    percentage += 0.05
                    skip_by = int(len(list_to_check) * percentage)

                if failed:
                    continue

            # Draws the acorns
            if self.display_sampling:
                pygame.draw.circle(self.display, (139, 69, 19), (new_candidate[1], new_candidate[0]), 2, 5)
                pygame.display.update()

            point_cell = (
                int(new_candidate[0] / self.cell_side_length), int(new_candidate[1] / self.cell_side_length))
            if self.cells[point_cell].point is not None:
                continue

            nearby_points = []
            for ny in range(point_cell[0] - 3, point_cell[0] + 3):
                for nx in range(point_cell[1] - 3, point_cell[1] + 3):
                    if self.y1 // self.cell_side_length <= ny < self.y2 // self.cell_side_length and self.x1 // self.cell_side_length <= nx < self.x2 // self.cell_side_length and (
                            ny, nx) not in self.available_cells:
                        nearby_points.append(self.cells[(ny, nx)].point)

            distances = list(set(list(map(self.distance, nearby_points, [new_candidate] * len(nearby_points)))))
            for dis in distances:
                if dis <= self.inner_circle_radius:
                    failed = True
                    break

            if not failed:
                self.points.append(new_candidate)
                self.available_points.append(new_candidate)
                self.cells[point_cell].add_point(new_candidate)
                self.available_cells.pop(point_cell)
                self.draw(new_candidate)
                return
        self.available_points.remove(current_point)
        self.draw(current_point)
