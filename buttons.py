from settings import *

class Buttons():
    def __init__(self, app, colour, x, y, width, height, text=''):
        self.app = app
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self, outline = None):
        if outline:
            pygame.draw.rect(self.app.screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(self.app.screen, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(FONT, FONT_SIZE)
            text = font.render(self.text, 1, (0, 0, 0))
            text_x = self.x + (self.width / 2 - text.get_width() / 2)
            text_y = self.y + (self.height / 2 - text.get_height() / 2)
            self.app.screen.blit(text, (text_x, text_y))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False