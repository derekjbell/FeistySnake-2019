'''
Duncan MacDonald - 2019

Implementation of floodfill for the purpose of BattleSnake.
'''

from queue import Queue
from helper import Helper

class FloodFill():

    def __init__(self, map):

        self.map = map[0]
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.used = {}
        self.area1 = 0
        self.area2 = 0

    def calculate(self, option1, option2, option3 = None):
        self.used = {}
        self.false_map()
        self.area1 = self.fill(option1, self.map)

        self.used = {}
        self.false_map()
        self.area2 = self.fill(option2, self.map)
        return (self.area1, self.area2)

    def false_map(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.used[(x, y)] = False


    def fill(self, start, map):
        count = 0
        q = Queue(maxsize=400)
        curr = start
        if len(self.get_neighbours(curr)) < 2:
            return 0
        q.put(curr)
        self.used[curr] = True
        count += 1
        while not q.empty():
            curr = q.get()
            for neighbour in self.get_neighbours(curr):
                if not self.used[neighbour]:
                    self.used[neighbour] = True
                    q.put(neighbour)
                    count += 1
        return count

    def get_neighbours(self, curr):
        up = (curr[0], curr[1] - 1)
        down = (curr[0], curr[1] + 1)
        left = (curr[0] - 1, curr[1])
        right = (curr[0] + 1, curr[1])
        return self.inbounds([up, down, left, right])

    def inbounds(self, neighbours):
        inb = []
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]

            if x < self.width and x >= 0 and y < self.height and y >= 0 and not self.used[neighbour]:
                if self.map[y][x] != 0:
                    inb.append(neighbour)
        return inb

if __name__=='__main__':
    grid = [[1,1,1,1,0,1,1,1],
            [1,0,1,1,0,1,1,1],
            [1,0,1,0,0,1,1,1],
            [1,0,1,0,1,1,0,1],
            [1,0,1,0,1,1,0,0]]
    map = [grid,[1]]
    op1 = (3, 0)
    op2 = (5, 0)
    head = (4, 0)
    results = FloodFill(map)
    move = results.calculate(op1, op2)
    if move[0] > move[1]:
        print(move)
        print("Make the first move!")
    else:
        print(move)
        print("Make the second move!")
