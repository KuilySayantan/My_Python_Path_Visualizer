import pygame
pygame.init()

pygame.display.set_caption("Path-Visualizer")

#   Screen Settings
WIDTH = 1536
HEIGHT = 768

GRID_SIZE = 24  # The size of each grid square
GRID_OFFSET_X = 240  # The offset for the grid on the X-axis
GRID_WIDTH = WIDTH - GRID_OFFSET_X - GRID_SIZE*2
GRID_HEIGHT = HEIGHT - GRID_SIZE*2

#       Button Settings     
MAIN_BUTTON_Y_POS = 550

#       Dimention of buttons    
MAIN_BUTTON_LENGTH = 200
MAIN_BUTTON_HEIGHT = 70

#       Grid-Menu Buttons       
BUTTON_HEIGHT = 335
BUTTON_SPACER = 20
GRID_BUTTON_LENGTH = 200
GRID_BUTTON_HEIGHT = 50

#       Colors      
WHITE = (255,255,255)
AQUAMARINE = (127,255,212)
GOLD = (255, 215, 0)
BLACK = (0,0,0)
ALICE = (240,248,255)
STEELBLUE = (110,123,139)
MINT = (189,252,201)
SPRINGGREEN = (0,255,127)
TOMATO = (255,99,71)
ROYALBLUE = (72,118,255)
TAN = (255,165,79)
RED = (255,0,0)
VIOLETRED = (255,130,171)
TURQUOISE = (30,144,255)

#       Grid        
#   Grid-string position
GRID_START_X = 264
GRID_START_Y = 24
#   Grid-ending podition
GRID_END_X = 1512
GRID_END_Y = 744

#       Font
FONT_SIZE = 20
FONT = 'font/Poppins-Medium.ttf'
