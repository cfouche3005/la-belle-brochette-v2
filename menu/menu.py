import pygame
from menu.button import buttonClass
from menu.text import text

class Menu:
    def __init__(self, screen):
        self.buttons = []
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)
        self.texts = []
        self.music = None
        self.music_active = False

    def addButton(self, x: int, y :int, width: int, height: int, text : str, fontsize :int, radius : int, inactiveColor : tuple, hoverColor: tuple, onClick: callable):
        """

        :param x: The x position of the button
        :param y: The y position of the button
        :param width: The width of the button
        :param height: The height of the button
        :param text: The text to display on the button
        :param fontsize: The font size of the text
        :param radius: The radius of the button corners
        :param inactiveColor: The color of the button when not hovered
        :param hoverColor: The color of the button when hovered
        :param onClick: The function to call when the button is clicked
        """
        button = buttonClass(
            screen=self.screen,
            position=(x, y),
            size=(width, height),
            clr=inactiveColor,
            cngclr=hoverColor,
            func=onClick,
            text=text,
            font_size=fontsize,
            font_clr=(255, 255, 255),
            radius = radius
        )
        self.buttons.append(button)
    def addText(self, x: int, y :int, txt : str, fontsize :int, color: tuple):
        """

        :param x: The x position of the text
        :param y: The y position of the text
        :param txt: The text to display
        :param fontsize: The font size of the text
        :param color: The color of the text
        """
        new_posx = x - self.font.size(txt)[0] // 2
        new_posy = y - self.font.size(txt)[1] // 2
        tempText = text(
            screen=self.screen,
            text=txt,
            position=(new_posx, new_posy),
            clr=color,
            font_size=fontsize,
            mid=True
        )
        self.texts.append(tempText)

    def detect_click(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.call_back()
    def attatchMusic(self, music_path: str):
        """
        Attatch a music file to the menu
        :param music_path: The path to the music file
        """
        self.music = music_path
    def launchMusic(self):
        """
        Launch the music
        """
        if self.music and not self.music_active:
            print("Playing music")
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
            self.music_active = True
    def stopMusic(self):
        """
        Stop the music
        """
        if self.music and self.music_active:
            pygame.mixer.music.stop()
            self.music_active = False
    def loadBackground(self, image_path: str):
        """
        Load a background image for the menu
        :param image_path: The path to the image file
        """
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
    def draw(self):

        if hasattr(self, 'background'):
            self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()
        for text in self.texts:
            text.draw()

