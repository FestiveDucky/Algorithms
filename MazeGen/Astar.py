from random import randint as ri
import time

class Node:
    def __init__(self, x, y, val):
        self.coords = (x, y)
        self.wall = False
        self.path = []
        self.startNode = False
        self.endNode = False
        self.selected = False

        if val == 1:
            self.wall = True
        elif val == 5:
            self.startNode = True
        elif val == 6:
            self.endNode = True

        self.gCost = 0
        self.hCost = 0
        self.fCost = 0


class Astar:
    def __init__(self, map, timeAlgorithm, display):
        self.width = len(map[0])
        self.height = len(map)

        self.selectedNode = None
        self.finished = 0

        self.startNode = None
        self.endNode = None

        self.display = False
        self.startTime = None
        # self.speed = 10
        # self.speedVar = IntVar()
        self.openNodes = []
        self.closedNodes = []

        self.nodes = {}
        for y in range(self.height):
            for x in range(self.width):
                self.nodes[(x, y)] = Node(x, y, map[y][x])
                if map[y][x] == 5:
                    self.startNode = (x, y)
                elif map[y][x] == 6:
                    self.endNode = (x, y)
                self.closedNodes.append((x, y))
        if timeAlgorithm:
            self.startTime = time.time()
        self.finalPath = None
        self.tick()
        print(self.finalPath)

    def getFinalPath(self):
        return self.finalPath

    def distance(self, coords1, coords2):
        x1, y1 = coords1
        x2, y2 = coords2
        disx = abs(x1 - x2)
        disy = abs(y1 - y2)
        cost = 0

        if disx > disy:
            cost += disy * 14
            disx -= disy
            cost += disx * 10
            return cost

        cost += disx * 14
        disy -= disx
        cost += disy * 10

        return cost

    def nodeCosts(self, selfCoords, otherCoords):
        gcost = self.distance(otherCoords, selfCoords) + self.nodes[otherCoords].gCost
        hcost = self.distance(self.endNode, selfCoords)
        fcost = gcost + hcost
        return hcost, gcost, fcost

    def bestNode(self):
        lowestCost = []
        for nodeCoords in self.openNodes:
            if lowestCost != []:
                fcost1 = self.nodes[nodeCoords].fCost
                hcost1 = self.nodes[nodeCoords].hCost
                fcost2 = self.nodes[lowestCost[0]].fCost
                hcost2 = self.nodes[lowestCost[0]].hCost
                if fcost1 < fcost2:
                    lowestCost = [nodeCoords]
                elif fcost1 == fcost2:
                    if hcost1 < hcost2:
                        lowestCost = [nodeCoords]
                    elif hcost1 == hcost2:
                        lowestCost.append(nodeCoords)
            else:
                lowestCost.append(nodeCoords)
        return lowestCost[ri(0, len(lowestCost) - 1)]

    def setCosts(self, coords, gcost, hcost, fcost):
        self.nodes[coords].gCost = gcost
        self.nodes[coords].hCost = hcost
        self.nodes[coords].fCost = fcost

    def revealNeighbors(self, nodeCoords):
        x, y = nodeCoords
        for newy in (y - 1, y, y + 1):
            for newx in (x - 1, x, x + 1):
                if self.width > newx > -1 and self.height > newy > -1 and (x, y) != (newx, newy):
                    if not self.nodes[(newx, newy)].wall and (newx, newy) not in self.openNodes and not self.nodes[(newx, newy)].selected and not self.nodes[(newx, newy)].startNode:
                        hcost, gcost, fcost = self.nodeCosts((newx, newy), nodeCoords)
                        self.setCosts((newx, newy), gcost, hcost, fcost)
                        self.nodes[(newx, newy)].path = self.nodes[nodeCoords].path + [self.nodes[(newx, newy)].coords]
                        self.openNodes.append((newx, newy))
                        self.closedNodes.remove((newx, newy))
                        # if not self.nodes[(newx, newy)].startNode and not self.nodes[(newx, newy)].endNode:
                        #     self.nodes[(newx, newy)]['bg'] = 'chartreuse3'
                        if hcost == 0 and self.finished == 0:
                            self.finished = 1
                    elif not self.nodes[(newx, newy)].wall and not self.nodes[(newx, newy)].selected and not self.nodes[(newx, newy)].startNode and (newx, newy) in self.openNodes:
                        hcost1, gcost1, fcost1 = self.nodeCosts((newx, newy), nodeCoords)
                        fcost2 = self.nodes[(newx, newy)].fCost
                        hcost2 = self.nodes[(newx, newy)].hCost
                        if fcost1 < fcost2:
                            self.setCosts((newx, newy), gcost1, hcost1, fcost1)
                            self.nodes[(newx, newy)].path = self.nodes[nodeCoords].path + [self.nodes[(newx, newy)].coords]
                        elif fcost1 == fcost2:
                            if hcost1 < hcost2:
                                self.setCosts((newx, newy), gcost1, hcost1, fcost1)
                                self.nodes[(newx, newy)].path = self.nodes[nodeCoords].path + [self.nodes[(newx, newy)].coords]

    def tick(self):
        if self.finished >= 0:
            if self.finished == 1:
                self.finished = -1
                if self.startTime != None:
                    stop = time.time()
                    print(stop - self.startTime)
                self.finalPath = self.reverseVals(self.nodes[self.endNode].path)
                # for coords in self.nodes[self.endNode].path:
                #     self.nodes[coords]['bg'] = 'dodgerblue'

            if len(self.openNodes) == 0:
                hcost, gcost, fcost = self.nodeCosts(self.startNode, self.startNode)
                self.openNodes.append(self.startNode)
                self.nodes[self.startNode].path.append(self.startNode)
                self.setCosts(self.startNode, gcost, hcost, fcost)
            lowestCost = self.bestNode()
            # if lowestCost != self.startNode and lowestCost != self.endNode:
            #     self.nodes[lowestCost]['bg'] = 'red2'
            self.nodes[lowestCost].selected = True
            self.openNodes.remove(lowestCost)
            self.closedNodes.append(lowestCost)
            self.selectedNode = lowestCost
            self.revealNeighbors(self.selectedNode)
            self.tick()

    def reverseVals(self, path):
        newPath = []
        for coords in path:
            newPath.append((coords[1], coords[0]))
        return newPath

if __name__ == '__main__':
    Astar([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 6, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 5, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], True)