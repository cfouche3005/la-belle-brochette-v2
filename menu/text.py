import pygame

class text:
    def __init__(self, screen, text: str, position: tuple, clr: tuple = (100,100,100), font_size: int = 16, mid : bool = False):
        """
        :param screen: Screen to draw the text on
        :param text: Text to display
        :param position: Position of the text (x, y)
        :param clr: Color of the text (R, G, B)
        :param font_size: Size of the font
        """
        self.screen = screen
        self.position = position
        self.font = pygame.font.SysFont("Bauhaus 93", font_size)
        self.txt_surf = self.font.render(text, True, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])
        if mid :
            self.txt_rect = self.txt_surf.get_rect(center = position)

    def draw(self):
        """
        Draw the text on the screen
        :param screen: Screen to draw the text on
        """
        self.screen.blit(self.txt_surf, self.position)