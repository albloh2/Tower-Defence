import pygame as pg

# PYGAME COLORS #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# PYGAME TOOLS #
class Window:
    def __init__(self, width, height):
        self.window = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = 60
        self.centered = False

    def set_fps(self, fps):
        self.fps = fps

    @staticmethod
    def set_title(title):
        pg.display.set_caption(title)

    def fill_color(self, colour):
        self.window.fill(colour)

    def draw_text(self, text_object, text, colour, x, y, centered=False):
        text_object.draw(self, text, colour, x, y, centered)

    def update(self):
        pg.display.update()
        self.clock.tick(self.fps)


class Text:
    def __init__(self, font, font_size):
        width, height = pg.display.get_surface().get_size()
        self.Font = pg.font.Font(font, font_size)
        self.HALF_WIDTH = round(width / 2)
        self.HALF_HEIGHT = round(height / 2)

    def draw(self, window, text, colour, x, y, centred=False):
        text_to_render = self.Font.render(text, True, colour)
        if window.centered and centred:
            window.window.blit(text_to_render, (x + self.HALF_WIDTH - (text_to_render.get_width() / 2),
                                                self.HALF_HEIGHT - y - (text_to_render.get_height() / 2)))
        elif window.centered:
            window.window.blit(text_to_render, (x + self.HALF_WIDTH, self.HALF_HEIGHT - y))
        elif centred:
            window.window.blit(text_to_render, (x + (text_to_render.get_width() / 2),
                                                y - (text_to_render.get_height() / 2)))
        else:
            window.window.blit(text_to_render, (x, y))


pg.init()
