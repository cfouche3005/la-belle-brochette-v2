import pygame

class buttonClass:

    def __init__(self, screen, position: tuple, size: tuple, clr : tuple = (100,100,100), radius : int = 14, cngclr: tuple = None, func: callable = None, text: str = '', font_size: int = 16, font_clr: list = [0,0,0]):
        """
        Button class to create a button in the menu

        :param screen: Screen to draw the button on
        :param position: Position of the button (x, y)
        :param size: Size of the button (width, height)
        :param clr: Color of the button (R, G, B)
        :param radius: Radius of the button corners
        :param cngclr: Color of the button when hovered (R, G, B)
        :param func: Function to call when the button is clicked
        :param text: Text to display on the button
        :param font_size: Size of the font
        :param font_clr: Color of the font (R, G, B)

        """
        self.position = position
        self.size = size
        self.clr = clr
        self.radius = radius
        self.func = func
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.screen = screen
        self.rect = self.surf.get_rect(center = position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])
        self.font = pygame.font.SysFont("Arial", font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(text, True, font_clr)
        self.txt_rect = self.txt_surf.get_rect(center = [wh//2 for wh in size])

        print(self.txt_rect)

    def mouseover(self):
        """
        Check if the mouse is over the button and change the color accordingly
        :return:
        """
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def draw(self):
        """
        Draw the button on the screen
        :return:
        """
        self.mouseover()

        self.surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.screen, self.curclr, self.rect, border_radius=self.radius)

        self.surf.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surf, self.rect)

    def call_back(self, *args):
        """
        Call the function associated with the button when clicked
        :param args:
        :return:
        """
        if self.func:
            self.func(*args)

