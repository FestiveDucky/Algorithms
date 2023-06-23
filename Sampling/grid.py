import pygame, numpy as np, math

draw_lines = False
draw_perp_lines = False
draw_rays = False
draw_ray_intersections = False
draw_final_lines = False
draw_vertices = False
draw_polygon = True
draw_polygon_outline = False
scan_dis = 3

ray_increment = 6
ray_increment_precision_multiplier = 1


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return round(x, 5), round(y, 5)
    else:
        return None


def new_point(angle, current_point, distance):
    angle = math.radians(angle)
    return current_point[0] + (distance * math.sin(angle)), current_point[1] + (distance * math.cos(angle))


def find_line(p1, p2, perpen=False):
    b = 1
    if (p2[1] - p1[1]) == 0:
        a = 1
        b = 0
        c = p1[1]
        if perpen:
            a = 0
            b = 1
            c = (p2[0] - p1[0]) / 2 + p1[0]
    elif (p2[0] - p1[0]) == 0:
        a = 0
        b = 1
        c = p1[0]
        if perpen:
            a = 1
            b = 0
            c = (p2[1] - p1[1]) / 2 + p1[1]
    else:
        if perpen:
            a = 1 / ((p2[0] - p1[0]) / (p2[1] - p1[1]))
        else:
            a = - (p2[0] - p1[0]) / (p2[1] - p1[1])
        center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        c = center[0] - (-a * center[1])
    return a, b, c


def on_segment(a, b, c):
    # ONLY WORKS IF POINTS ARE ON SAME LINE AND IF C IS EQUAL TO EITHER OF THE POINTS IT RETURNS TRUE
    if c == a or c == b:
        return True
    coords_ab = (b[0] - a[0], b[1] - a[1])
    coords_ac = (c[0] - a[0], c[1] - a[1])
    scalar_product_ab_ab = coords_ab[0] * coords_ab[0] + coords_ab[1] * coords_ab[1]
    scalar_product_ab_ac = coords_ab[0] * coords_ac[0] + coords_ab[1] * coords_ac[1]

    if 0 < scalar_product_ab_ac < scalar_product_ab_ab:
        return True
    else:
        return False


class Polygon:
    def __init__(self, cell, cell_border_x, cell_border_y, cell_length, color):
        self.vertices = []
        self.cell = cell
        self.color = color
        self.coords = self.cell.point
        self.cell_border_x = cell_border_x
        self.cell_border_y = cell_border_y
        self.cell_length = cell_length
        self.lines = []
        self.sub_map_corner = None

    def find_vertices(self, display, grid, cells):
        sub_map = self.sub_map(scan_dis, grid)
        points = self.locate_points(sub_map)
        # print(self.sub_map(3, grid))
        # print(self.coords, self.cell.coords, "me")
        # for c in self.locate_points(self.sub_map(3, grid)):
            # print(c, cells[c].point)
        for point in points:
            inters = self.perpendicular_coords(self.coords, cells[point].point)
            self.lines.append(inters)
            if draw_lines:
                pygame.draw.aaline(display, (0, 0, 250), tuple(reversed(self.coords)),
                                   tuple(reversed(cells[point].point)))
            if draw_perp_lines:
                pygame.draw.aaline(display, (250, 0, 0), tuple(reversed(inters[0])), tuple(reversed(inters[1])))
        self.rays(display)
        pygame.display.update()

    def rays(self, display):
        lines = []
        for i in range(0, 360 * ray_increment_precision_multiplier, ray_increment):
            i /= ray_increment_precision_multiplier
            point = new_point(i + 1, self.coords, 1000)
            current_lines = []
            zero = None
            for j in self.lines + [
                [(self.cell_border_y[0] * self.cell_length, self.cell_border_x[0] * self.cell_length),
                 (self.cell_border_y[0] * self.cell_length, self.cell_border_x[1] * self.cell_length)],
                [(self.cell_border_y[0] * self.cell_length, self.cell_border_x[0] * self.cell_length),
                 (self.cell_border_y[1] * self.cell_length, self.cell_border_x[0] * self.cell_length)],
                [(self.cell_border_y[1] * self.cell_length, self.cell_border_x[0] * self.cell_length),
                 (self.cell_border_y[1] * self.cell_length, self.cell_border_x[1] * self.cell_length)],
                [(self.cell_border_y[0] * self.cell_length, self.cell_border_x[1] * self.cell_length),
                 (self.cell_border_y[1] * self.cell_length, self.cell_border_x[1] * self.cell_length)]]:
                inter_point = intersection(find_line(self.coords, point), find_line(j[0], j[1]))

                if inter_point is not None:
                    inter_point = tuple(reversed(inter_point))
                    if on_segment(self.coords, point, inter_point) and inter_point[0] >= 0 and inter_point[1] >= 0:
                        # print(find_line(self.coords, point), find_line(j[0], j[1]), (self.coords, point), j,
                        #       inter_point, math.sqrt(
                        #         (inter_point[0] - self.coords[0]) ** 2 + (inter_point[1] - self.coords[1]) ** 2),
                        #       inter_point)
                        dis = math.sqrt((inter_point[0] - self.coords[0]) ** 2 + (inter_point[1] - self.coords[1]) ** 2)
                        if dis == 0:
                            zero = [j, dis, inter_point]
                        else:
                            current_lines.append([j, dis, inter_point])
                        if draw_ray_intersections:
                            pygame.draw.circle(display, (255, 0, 255), tuple(reversed(inter_point)), 2, 2)
            if len(current_lines) == 0:
                best = zero
            else:
                best = current_lines.pop()
                for line_candidate in current_lines:
                    if line_candidate[1] < best[1]:
                        best = line_candidate[:]
            if best[0] not in lines:
                lines.append(best[0])
            if draw_rays:
                # print(best)
                pygame.draw.aaline(display, self.color, tuple(reversed(self.coords)), tuple(reversed(best[2])))

        if draw_final_lines:
            for line in lines:
                print(line)
                # (lines.index(line) + 1) * 40, (lines.index(line) + 1) * 40, (lines.index(line) + 1) * 40)
                pygame.draw.aaline(display, (255, 255, 255),
                                   tuple(reversed(line[0])), tuple(reversed(line[1])))

        for i in range(len(lines)):
            n = i + 1
            if n == len(lines):
                n = 0
            inter = intersection(find_line(lines[i][0], lines[i][1]), find_line(lines[n][0], lines[n][1]))
            self.vertices.append(inter)

        if draw_vertices:
            for vertex in self.vertices:
                pygame.draw.circle(display, (255, 255, 255), vertex, 2, 2)

        if draw_polygon:
            # print(lines, [find_line(l[0], l[1]) for l in lines])
            # print(self.vertices)
            if draw_polygon_outline:
                pygame.draw.polygon(display, self.color, self.vertices, 1)
            else:
                pygame.draw.polygon(display, self.color, self.vertices)

    def perpendicular_coords(self, p1, p2):
        line = find_line(p1, p2, perpen=True)
        intersections = [intersection(line, (0, 1, self.cell_border_y[0] * self.cell_length)),
                         intersection(line, (0, 1, self.cell_border_y[1] * self.cell_length)),
                         intersection(line, (1, 0, self.cell_border_x[0] * self.cell_length)),
                         intersection(line, (1, 0, self.cell_border_x[1] * self.cell_length))]
        final_intersections = []
        for inter in intersections:
            if not inter:
                continue
            if self.cell_border_y[1] * self.cell_length >= inter[1] >= self.cell_border_y[0] * self.cell_length and \
                    self.cell_border_x[1] * self.cell_length >= inter[0] >= self.cell_border_x[0] * self.cell_length:
                final_intersections.append(tuple(reversed(inter)))
        # print(line, p1, p2, final_intersections)
        return final_intersections

    def sub_map(self, r, grid):
        # f - first
        # s - second
        # b - border
        x = self.cell.coords[1]
        y = self.cell.coords[0]

        fxb, sxb, fyb, syb = (r, r, r, r)
        if x - r < self.cell_border_x[0]:
            fxb = x - self.cell_border_x[0]
        elif x + r > self.cell_border_x[1]:
            sxb = self.cell_border_x[1] - x
        if y - r < self.cell_border_y[0]:
            fyb = y - self.cell_border_y[0]
        elif y + r > self.cell_border_y[1]:
            syb = self.cell_border_y[1] - y

        self.sub_map_corner = (y - fyb, x - fxb)

        return grid[y - fyb:y + syb + 1, x - fxb:x + sxb + 1]

    def locate_points(self, sub_map):
        ys, xs = np.where(np.isin(sub_map, 1))
        cells = []
        for i in range(len(xs)):
            new_cell = (ys[i] + self.sub_map_corner[0], xs[i] + self.sub_map_corner[1])
            if new_cell != self.cell.coords:
                cells.append(new_cell)
        return cells
