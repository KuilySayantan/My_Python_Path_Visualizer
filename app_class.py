import sys
from settings import *
from buttons import *
from bfs import *
from dfs import *
from astar import *
from dijkstra import *
from bidirectional import *
from visualize_path import *
from maze import *

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0
        self.generatedWall_pos = []

        # Start and End Nodes Coordinate
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list that includes te coordinates of the border)
        # self.wall_pos = wall_nodes_coords_list.copy()
        self.wall_pos = []

        # Maze class instantiation
        self.maze = Maze(self)

        # Main menu buttons
        self.bfs_button = Buttons(self, WHITE, 228, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'BFS')
        self.dfs_button = Buttons(self, WHITE, 448, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'DFS')
        self.astar_button = Buttons(self, WHITE, 668, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'A* Search')
        self.dijkstra_button = Buttons(self, WHITE, 888, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Dijkstra Search')
        self.bidirectional_button = Buttons(self, WHITE, 1108, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Bidirectional Search')




        # Grif-menu buttons
        self.start_end_node_button = Buttons(self, AQUAMARINE, 20, BUTTON_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Buttons(self, AQUAMARINE, 20, BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(self, AQUAMARINE, 20, BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Reset')
        self.visualize_button = Buttons(self, AQUAMARINE, 20, BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Visualize Path')
        self.main_menu_button = Buttons(self, AQUAMARINE, 20, BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Main Menu')
        self.maze_generate_button = Buttons(self, AQUAMARINE, 20, BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 5 + BUTTON_SPACER * 5, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Generate Maze')


    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E':
                self.draw_SE_nodes()
            if self.state == 'draw walls':
                self.creating_walls()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main_menu()

        pygame.quit()
        sys.exit()

##########################    SETUP FUNCTIONS     #####################

#   Loading Images
    def load(self):
        self.main_menu_background = pygame.image.load('Pathfinding_Visualizer.png').convert_alpha()
        self.grid_background = pygame.image.load('grid_logo.png').convert()

#   draw Text
    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.Font(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

#   Setup for main-menu
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0,0))
        
        # self.draw_text('Choose an algorithm to visualize', self.screen, [768, 500], 20, AQUAMARINE, FONT, centered=True)

        # main-menu buttons
        self.bfs_button.draw_button(AQUAMARINE)
        self.dfs_button.draw_button(AQUAMARINE)
        self.astar_button.draw_button(AQUAMARINE)
        self.dijkstra_button.draw_button(AQUAMARINE)
        self.bidirectional_button.draw_button(AQUAMARINE)


#   Setup for grid
    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)
        self.screen.blit(self.grid_background, (0,0))

    def sketch_grid(self):
        # border 
        pygame.draw.rect(self.screen, ALICE, (240, 0, WIDTH, HEIGHT), 0)   
        pygame.draw.rect(self.screen, AQUAMARINE, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        # Draw Grid
        #  along X-axis there are 52 pixels [without border]
        #  along Y-axis there are 30 pixels [without border]
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (GRID_START_X + x*GRID_SIZE, GRID_START_Y),(GRID_START_X + x*GRID_SIZE, GRID_END_Y))

        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (GRID_START_X, GRID_START_Y + y*GRID_SIZE),(GRID_END_X, GRID_START_Y + y*GRID_SIZE))

    
    def sketch_grid_buttons(self):
        #   gird-buttons
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.visualize_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)
        self.maze_generate_button.draw_button(STEELBLUE)

#   Button functions and hover effers
    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
            elif self.visualize_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.back_to_menu()
            elif self.maze_generate_button.isOver(pos):
                self.generatedWall_pos = self.maze.generateSolid()
                self.wall_pos.extend(self.generatedWall_pos)
                self.state = 'draw S/E'
            

        # hover effect in grid-menu buttons
        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.colour = MINT
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.colour = MINT
            elif self.reset_button.isOver(pos):
                self.reset_button.colour = MINT
            elif self.visualize_button.isOver(pos):
                self.visualize_button.colour = MINT
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = MINT
            elif self.maze_generate_button.isOver(pos):
                self.maze_generate_button.colour = MINT
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, \
                self.visualize_button.colour, self.main_menu_button.colour, self.maze_generate_button.colour = \
                    STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE
                
    
    
    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.colour = MINT

        elif self.state == 'draw walls':
            self.wall_node_button.colour = MINT

    def reset_shared_variables(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        # self.wall_pos = wall_nodes_coords_list.copy()
        # self.generatedWall_pos = []
        self.wall_pos = []
        self.generatedWall_pos = []

    def execute_reset(self):
        self.reset_shared_variables()
        self.state = 'grid window'

    def back_to_menu(self):
        self.reset_shared_variables()
        self.state = 'main menu'

##########################  EXECUTION FUNCTIONS     #####################
#   Main-menu functions

    def main_menu_events(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()

        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'

                elif self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'

                elif self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'

                if self.dijkstra_button.isOver(pos):
                    self.algorithm_state = 'dijkstra'
                    self.state = 'grid window'

                if self.bidirectional_button.isOver(pos):
                    self.algorithm_state = 'bidirectional'
                    self.state = 'grid window'

            buttons = [self.bfs_button, self.dfs_button, self.astar_button,self.dijkstra_button, self.bidirectional_button]
            hover_color = AQUAMARINE

            for button in buttons:
                if button.isOver(pos):
                    button.colour = hover_color
                else:
                    button.colour = WHITE
            # if event.type == pygame.MOUSEMOTION:
            #     if self.bfs_button.isOver(pos):
            #         self.bfs_button.colour = AQUAMARINE
            #     else:
            #         self.bfs_button.colour = WHITE

######  PLAYING STATE FUNCTIONS   ######
    def grid_events(self):
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

##############  Drawing nodes #######################
    def creating_walls(self):
        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            left_mouse_pressed, _, right_mouse_pressed = pygame.mouse.get_pressed() #ignore the middle button of the mouse
            
            pos = pygame.mouse.get_pos()
            # Grid button function
            self.grid_window_buttons(pos, event)

            if left_mouse_pressed:  # Check if the left mouse button is pressed

                # Checking for valid position
                if pos[0] > GRID_START_X and pos[0] < GRID_END_X and pos[1] > GRID_START_Y and pos[1] < GRID_END_Y:
                    x_grid_pos = (pos[0] - GRID_START_X) // GRID_SIZE
                    y_grid_pos = (pos[1] - GRID_START_Y) // GRID_SIZE

                    if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                        pygame.draw.rect(self.screen, BLACK, (GRID_START_X + x_grid_pos * GRID_SIZE, GRID_START_Y + y_grid_pos * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                        self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))

            elif right_mouse_pressed:  # Check if the right mouse button is pressed

                # Checking for valid position
                if pos[0] > GRID_START_X and pos[0] < GRID_END_X and pos[1] > GRID_START_Y and pos[1] < GRID_END_Y:
                    x_grid_pos = (pos[0] - GRID_START_X) // GRID_SIZE
                    y_grid_pos = (pos[1] - GRID_START_Y) // GRID_SIZE

                    if (x_grid_pos + 1, y_grid_pos + 1) in self.wall_pos:
                        pygame.draw.rect(self.screen, AQUAMARINE, (GRID_START_X + x_grid_pos * GRID_SIZE, GRID_START_Y + y_grid_pos * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                        self.wall_pos.remove((x_grid_pos + 1, y_grid_pos + 1))
            
            for x in range(52):
                pygame.draw.line(self.screen, ALICE, (GRID_START_X + x * GRID_SIZE, GRID_START_Y),
                    (GRID_START_X + x * GRID_SIZE, GRID_END_Y))
            for y in range(30):
                pygame.draw.line(self.screen, ALICE, (GRID_START_X, GRID_START_Y + y * GRID_SIZE),
                    (GRID_END_X, GRID_START_Y + y * GRID_SIZE))


                    

    def draw_SE_nodes(self):
        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            pos = pygame.mouse.get_pos()

            # Grid button function
            self.grid_window_buttons(pos, event)

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Checking for valid position
                if pos[0] > GRID_START_X and pos[0] < GRID_END_X and pos[1] > GRID_START_Y and pos[1] < GRID_END_Y:
                    x_grid_pos = (pos[0] - GRID_START_X) // GRID_SIZE
                    y_grid_pos = (pos[1] - GRID_START_Y) // GRID_SIZE

                    if self.start_end_checker < 2 and (x_grid_pos+1, y_grid_pos+1) != (self.start_node_x, self.start_node_y) and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                        if(self.start_end_checker == 0):
                            node_color = TOMATO 
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            self.state = 'draw S/E'
                        else:
                            node_color = ROYALBLUE 
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                        self.start_end_checker += 1
                        pygame.draw.rect(self.screen, node_color, (GRID_START_X + x_grid_pos * GRID_SIZE, GRID_START_Y + y_grid_pos * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

                
            

#################################### VISUALIZATION FUNCTIONS #########################################
    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        ### BFS ###

        if self.algorithm_state == 'bfs':

            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            # Make Object for new path
            if self.bfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768,384], 50, RED, FONT, centered = True)


        ### DFS ###

        elif self.algorithm_state == 'dfs':
            self.dfs = DFS(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()

            # Make Object for new path
            if self.dfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
                self.dfs.redrawGrid()   # so that the ans path also have the grid part

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768,384], 50, RED, FONT, centered = True)


        ### A* Search ###

        elif self.algorithm_state == 'astar':
            self.astar = AStar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                route = self.astar.astar_execute()

            if route is not None:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, route)
                self.draw_path.draw_path()
                self.astar.redrawGrid()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)

        ### Dijkstra* Search ###

        elif self.algorithm_state == 'dijkstra':
            self.dijkstra = Dijkstra(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                route = self.dijkstra.dijkstra_execute()

            if route is not None:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, route)
                self.draw_path.draw_path()
                self.dijkstra.redrawGrid()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)

        ### BidirectionalSearch ###

        elif self.algorithm_state == 'bidirectional':
            self.bidirectional_search = BidirectionalSearch(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            route = self.bidirectional_search.bidirectional_search_execute()

            if route is not None:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.end_node_x, route)
                self.draw_path.draw_path()
                self.bidirectional_search.redrawGrid()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)

        # for going to main menu
        self.state = 'aftermath'

############################  AFTERMATH FUNCTIONS #######################

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.visualize_button.isOver(pos):
                    self.visualize_button.colour = MINT
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.visualize_button.colour, self.main_menu_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                elif self.main_menu_button.isOver(pos):
                    self.back_to_menu()

