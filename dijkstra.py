from settings import *
from app_class import *
import heapq

class Dijkstra:
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.xMax = 52
        self.xMin = 1
        self.yMax = 30
        self.yMin = 1

        # Initialize the grid with costs
        self.grid = [[float('inf') for _ in range(self.yMax + 1)] for _ in range(self.xMax + 1)]
        self.grid[start_node_x][start_node_y] = 0

    def draw_all_paths(self, current):
        i, j = current[0], current[1]

        # Draw each node the algorithm is visiting as it is searching SIMULTANEOUSLY
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)

        # Redraw start/end nodes on top of all routes
        pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        self.redrawGrid()
        pygame.display.update()

    def redrawGrid(self):
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GRID_START_X + x * 24, GRID_START_Y), (GRID_START_X + x * 24, GRID_END_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GRID_START_X, GRID_START_Y + y * 24), (GRID_END_X, GRID_START_Y + y * 24))

    def dijkstra_execute(self):
        open_list = [(0, (self.start_node_x, self.start_node_y))]

        while open_list:
            current_cost, current_node = heapq.heappop(open_list)

            if current_node == (self.end_node_x, self.end_node_y):
                return self.get_path()

            for neighbor in self.get_neighbors(current_node):
                neighbor_x, neighbor_y = neighbor
                if (neighbor_x, neighbor_y) in self.wall_pos:
                    continue

                new_cost = self.grid[current_node[0]][current_node[1]] + 1

                if new_cost < self.grid[neighbor_x][neighbor_y]:
                    self.grid[neighbor_x][neighbor_y] = new_cost
                    heapq.heappush(open_list, (new_cost, neighbor))

                # Call draw_all_paths to visualize the current node
                self.draw_all_paths(neighbor)

        return None

    def get_neighbors(self, node):
        neighbors = []

        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move in moves:
            x, y = node[0] + move[0], node[1] + move[1]

            if (x, y) in self.wall_pos:
                continue
            
            if self.xMin <= x <= self.xMax and self.yMin <= y <= self.yMax:
                neighbors.append((x, y))

        return neighbors

    def get_path(self):
        path = []

        current_node = (self.end_node_x, self.end_node_y)
        while current_node != (self.start_node_x, self.start_node_y):
            path.append(current_node)

            current_node = self.get_parent(current_node)

        path.reverse()
        return path

    def get_parent(self, node):
        for neighbor in self.get_neighbors(node):
            if self.grid[neighbor[0]][neighbor[1]] == self.grid[node[0]][node[1]] - 1:
                return neighbor

        return None
