from settings import *
from app_class import *

class AStar():
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

        # Initialize the grid with G scores
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

    def astar_execute(self):
        if self.start_node_x == self.end_node_x or self.start_node_y == self.end_node_y:
            # Handle straight paths directly
            return self.get_straight_path()

        # Continue with A* for non-straight paths
        open_list = [(self.start_node_x, self.start_node_y)]

        while open_list:
            current_node = self.get_lowest_f_cost_node(open_list)

            if current_node == (self.end_node_x, self.end_node_y):
                return self.get_path()

            open_list.remove(current_node)

            for neighbor in self.get_neighbors(current_node):
                if neighbor in open_list:
                    continue

                tentative_g_cost = self.grid[current_node[0]][current_node[1]] + 1

                if tentative_g_cost < self.grid[neighbor[0]][neighbor[1]]:
                    self.grid[neighbor[0]][neighbor[1]] = tentative_g_cost
                    open_list.append(neighbor)

                # Call draw_all_paths to visualize the current node
                self.draw_all_paths(neighbor)

        return None

    def get_straight_path(self):
        # Implement a direct path calculation for straight paths
        path = []

        x, y = self.start_node_x, self.start_node_y
        while x != self.end_node_x or y != self.end_node_y:
            if x < self.end_node_x:
                x += 1
            elif x > self.end_node_x:
                x -= 1
            elif y < self.end_node_y:
                y += 1
            else:
                y -= 1

            self.draw_all_paths((x, y))
            path.append((x, y))

        return path


    def get_neighbors(self, node):
        neighbors = []

        # Define possible moves (up, down, left, right)
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Determine the relative positions of start and end points
        if self.start_node_x < self.end_node_x:
            # Start point's x-axis is lower
            # Prioritize right and then up/down
            custom_order = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            
        else:
            # End point's x-axis is lower or equal
            # Prioritize left and then up/down
            custom_order = [(1, 0), (0, -1), (0, 1), (-1, 0)]

        for move in custom_order:
            x, y = node[0] + move[0], node[1] + move[1]

            if (x, y) in self.wall_pos:
                continue
            
            if self.xMin <= x <= self.xMax and self.yMin <= y <= self.yMax:
                neighbors.append((x, y))

        return neighbors



    def get_lowest_f_cost_node(self, open_list):
        lowest_f_cost = float('inf')
        lowest_f_cost_node = None

        for node in open_list:
            f_cost = self.grid[node[0]][node[1]] + self.calculate_heuristic(node)
            if f_cost < lowest_f_cost:
                lowest_f_cost = f_cost
                lowest_f_cost_node = node

        return lowest_f_cost_node

    def calculate_heuristic(self, node):
        dx = abs(node[0] - self.end_node_x)
        dy = abs(node[1] - self.end_node_y)

        # Weight the distance in the direction of the end node.
        weight = 1.01

        return (dx + dy)*weight

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