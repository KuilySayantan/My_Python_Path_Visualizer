import pygame
from settings import *
from app_class import *
import heapq

class BidirectionalSearch:
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

        # Initialize the grids with costs from both directions
        self.grid_forward = [[float('inf') for _ in range(self.yMax + 1)] for _ in range(self.xMax + 1)]
        self.grid_backward = [[float('inf') for _ in range(self.yMax + 1)] for _ in range(self.xMax + 1)]
        self.grid_forward[start_node_x][start_node_y] = 0
        self.grid_backward[end_node_x][end_node_y] = 0

        # Initialize the open lists for both directions
        self.open_list_forward = [(0, (start_node_x, start_node_y))]
        self.open_list_backward = [(0, (end_node_x, end_node_y))]

        # Store the meeting point if found
        self.meeting_point = None

    def draw_all_paths(self, current, color):
        i, j = current[0], current[1]

        # Draw each node the algorithm is visiting as it is searching SIMULTANEOUSLY
        pygame.draw.rect(self.app.screen, color, (i * 24 + 240, j * 24, 24, 24), 0)

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

    def bidirectional_search_execute(self):
        while self.open_list_forward and self.open_list_backward:
            # Forward search
            current_cost_forward, current_node_forward = heapq.heappop(self.open_list_forward)

            # Check if the node is in the backward search space
            if self.grid_backward[current_node_forward[0]][current_node_forward[1]] < float('inf'):
                self.meeting_point = current_node_forward
                break

            for neighbor in self.get_neighbors(current_node_forward, self.grid_forward):
                neighbor_x, neighbor_y = neighbor
                if (neighbor_x, neighbor_y) in self.wall_pos:
                    continue

                new_cost = self.grid_forward[current_node_forward[0]][current_node_forward[1]] + 1

                if new_cost < self.grid_forward[neighbor_x][neighbor_y]:
                    self.grid_forward[neighbor_x][neighbor_y] = new_cost
                    heapq.heappush(self.open_list_forward, (new_cost, neighbor))

                # Call draw_all_paths to visualize the current node
                self.draw_all_paths(neighbor,TAN)

            # Backward search
            current_cost_backward, current_node_backward = heapq.heappop(self.open_list_backward)

            # Check if the node is in the forward search space
            if self.grid_forward[current_node_backward[0]][current_node_backward[1]] < float('inf'):
                self.meeting_point = current_node_backward
                break

            for neighbor in self.get_neighbors(current_node_backward, self.grid_backward):
                neighbor_x, neighbor_y = neighbor
                if (neighbor_x, neighbor_y) in self.wall_pos:
                    continue

                new_cost = self.grid_backward[current_node_backward[0]][current_node_backward[1]] + 1

                if new_cost < self.grid_backward[neighbor_x][neighbor_y]:
                    self.grid_backward[neighbor_x][neighbor_y] = new_cost
                    heapq.heappush(self.open_list_backward, (new_cost, neighbor))

                # Call draw_all_paths to visualize the current node
                self.draw_all_paths(neighbor, GOLD)
        else:
            # If the loop completes without finding a path, return None
            return None

        return self.get_path()

    def get_neighbors(self, node, grid):
        neighbors = []

        if node is None:
            return neighbors

        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move in moves:
            x, y = node[0] + move[0], node[1] + move[1]

            if (x, y) in self.wall_pos:
                continue

            if self.xMin <= x <= self.xMax and self.yMin <= y <= self.yMax:
                neighbors.append((x,y))

        return neighbors


    def get_path(self):
        path_forward = []
        path_backward = []

        current_node = self.meeting_point
        while current_node != (self.start_node_x, self.start_node_y):
            path_forward.append(current_node)
            current_node = self.get_parent(current_node, self.grid_forward)

        current_node = self.meeting_point
        while current_node != (self.end_node_x, self.end_node_y):
            path_backward.append(current_node)
            current_node = self.get_parent(current_node, self.grid_backward)

        # Reverse the backward path to align with the forward path
        path_backward.reverse()

        return path_forward + path_backward

    def get_parent(self, node, grid):
        for neighbor in self.get_neighbors(node, grid):
            if grid[neighbor[0]][neighbor[1]] == grid[node[0]][node[1]] - 1:
                return neighbor

        return None
