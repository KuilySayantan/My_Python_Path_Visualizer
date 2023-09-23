from settings import *

class DFS():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited = [(self.start_node_x, self.start_node_y)]
        self.route = None
        self.route_found = False
        self.xMax = 52
        self.xMin = 1
        self.yMax = 30
        self.yMin = 1

    def draw_all_paths(self, i, j):
        ##### Draw each node the computer is visiting as it is searching SIMULTNEOUSLY
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)

        ##### Redraw start/end nodes on top of all routes
        pygame.draw.rect(self.app.screen, TOMATO,
                         (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE,
                         (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        self.redrawGrid()
        pygame.display.update()

    def redrawGrid(self):
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GRID_START_X + x * 24, GRID_START_Y), (GRID_START_X + x * 24, GRID_END_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GRID_START_X, GRID_START_Y + y * 24), (GRID_END_X, GRID_START_Y + y * 24))
        
        

    def checkValid(self, move):
        if move not in self.wall_pos and move not in self.visited and self.xMin <= move[0] <= self.xMax and self.yMin <= move[1] <= self.yMax:
            self.visited.append(move)
            return True
        return False

    def findEnd(self, first_in):
        if first_in == (self.end_node_x, self.end_node_y):
            return True
        return False

    def dfs_execute(self):
        stack = []
        first_in = (self.start_node_x, self.start_node_y)
        stack.append(first_in)

        moves_stack = []
        moves_first_in = ''
        moves_stack.append(moves_first_in)

        while len(stack) > 0:
            last_out = stack[-1]  # Peek the top of the stack without popping
            moves_last_out = moves_stack[-1]

            if self.findEnd(last_out):
                self.route = moves_last_out
                self.route_found = True
                break

            # Flag to track if any valid move was found from the current node
            found_valid_move = False

            for m in ['D', 'R', 'U', 'L']:
                i, j = last_out
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1

                move_update = moves_last_out + m

                if self.checkValid((i, j)):
                    found_valid_move = True
                    stack.append((i, j))
                    moves_stack.append(move_update)
                    if not self.findEnd((i, j)):
                        self.draw_all_paths(i, j)  
                    break

            if not found_valid_move:
                # If no valid move was found, backtrack by popping the current node from the stack
                stack.pop()
                moves_stack.pop()
            
        if not self.route_found:
            return False







