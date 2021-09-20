import CONFIG
from CONFIG import *
import text


class Ui:
    def __init__(self, display, start_x, start_y):
        self.display = display
        self.start_pos = self.start_x, self.start_y = start_x, start_y
        self.buttons = []
        self.texts = []
        self.small_font = text.Font("./images/small_font.png")
        self.large_font = text.Font("./images/large_font.png")

    class Button(object):
        def __init__(self, button_image, x, y, ui_x, ui_y):
            self.image = button_image
            self.x = x + ui_x
            self.y = y + ui_y
            self.pos = (self.x, self.y)
            self.rect = pygame.Rect((self.x, self.y), (self.image.get_width(), self.image.get_height()))
            self.clicked = False

        def click(self, mouse_x, mouse_y):
            if self.rect.collidepoint((mouse_x, mouse_y)):
                self.clicked = True
            else:
                self.clicked = False

    class Text(object):
        def __init__(self, new_text, x, y, ui_x, ui_y):
            self.text = new_text
            self.x = x + ui_x
            self.y = y + ui_y
            self.pos = (self.x, self.y)

    def add_button(self, button_image, x, y):
        self.buttons.append(self.Button(button_image, x, y, self.start_x, self.start_y))

    def add_text(self, new_text, x, y):
        self.texts.append(self.Text(new_text, x, y, self.start_x, self.start_y))

    def draw(self):
        for item in self.buttons:
            self.display.blit(item.image, item.pos)
            # pygame.draw.rect(self.display, (245, 250, 200), item.rect, 1)

        for item in self.texts:
            self.large_font.render(self.display, item.text, item.pos)
