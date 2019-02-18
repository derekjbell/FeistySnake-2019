'''
Duncan MacDonald - 2019

Implementation of floodfill for the purpose of BattleSnake.
'''


from queue import Queue
from helper import Helper

class FloodFill():

    def __init__(self, map, head, option1, option2, option3 = None):
        self.option1 = option1
        self.option2 = option2
        self.map = map[0]
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.used = {}
        self.false_map()
        self.area1 = self.fill(self.option1, map)
        self.false_map()
        self.area2 = self.fill(self.option2, map)

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
            for block in self.get_neighbours(curr):
                if not self.used[block]:
                    self.used[block] = True
                    q.put(block)
                    count += 1
        return count

    def get_neighbours(self, curr):
        up = (curr[0], curr[1] + 1)
        down = (curr[0], curr[1] - 1)
        left = (curr[0] - 1, curr[1])
        right = (curr[0] + 1, curr[1])
        return self.inbounds([up, down, left, right])

    def inbounds(self, neighbs):
        inb = []
        for block in neighbs:
            x = block[0]
            y = block[1]
            if x < self.width and x >= 0 and y < self.height and y >= 0 and not self.used[block]:
                if self.map[y][x] != 0:
                    inb.append(block)
        return inb

if __name__=='__main__':
    grid = [[1,1,1,1,1,1,1,1],
            [1,0,1,1,1,1,1,1],
            [1,0,1,0,0,1,1,1],
            [1,0,1,0,1,1,0,1],
            [1,0,1,0,1,1,0,0]]
    map = [grid,[1]]
    op2 = (0, 5)
    op1 = (2, 5)
    head = (1, 5)
    move = FloodFill(map, head,op1, op2).move
    print(move)
