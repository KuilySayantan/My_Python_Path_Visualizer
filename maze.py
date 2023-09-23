from settings import *
import random


class Maze:
    def __init__(self, app):
        self.app = app
        # self.visited = []
        self.walls = []
        self.xMax = 53
        self.yMax = 31

    def generateSolid(self):
        self.walls = []
        self.generateMaze()
        return self.walls

    
    def generateMaze(self):
        start_vertex = (random.randint(1, self.xMax), random.randint(1, self.yMax))
        self.visited = set()
        self.randomizedDFS(start_vertex)

    def randomizedDFS(self, vertex):
        i, j = vertex
        self.visited.add(vertex)

        moves = [(i, j - 2), (i, j + 2), (i - 2, j), (i + 2, j)]
        random.shuffle(moves)

        for move in moves:
            x, y = move
            if 1 <= x < self.xMax and 1 <= y < self.yMax and (x, y) not in self.visited:
                midx = (i + x) // 2
                midy = (j + y) // 2
                self.drawMaze(midx, midy, BLACK)
                self.drawMaze(x, y, BLACK)
                self.randomizedDFS((x, y))
                self.walls.append((x,y))
                self.walls.append((midx, midy))
        


    def draw(self, pos, colour):
        i, j = pos
        pygame.draw.rect(self.app.screen, colour, (i * 24 + 240, j * 24, 24, 24), 0)

    def redrawGrid(self):
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GRID_START_X + x * 24, GRID_START_Y), (GRID_START_X + x * 24, GRID_END_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GRID_START_X, GRID_START_Y + y * 24), (GRID_END_X, GRID_START_Y + y * 24))

    def drawMaze(self, x, y, colour):
        self.draw((x, y), colour)
        self.redrawGrid()
        pygame.display.update()



