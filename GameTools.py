import math as m

import pygame
import pygame as pg

PYGAME_API = pg

# PYGAME COLORS #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# PYGAME CURSOR #
ARROW = pg.SYSTEM_CURSOR_ARROW
HAND = pg.SYSTEM_CURSOR_HAND
WAIT = pg.SYSTEM_CURSOR_WAIT


# PYGAME WINDOWS #
class Window:
    def __init__(self, width, height, scaled=False):
        if scaled:
            self.window = pg.display.set_mode((width, height), pg.SCALED | pg.FULLSCREEN)
        else:
            self.window = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = 60

    def set_fps(self, fps):
        self.fps = fps

    @staticmethod
    def set_icon(icon):
        pg.display.set_icon(icon)

    @staticmethod
    def set_title(title):
        pg.display.set_caption(title)

    def fill_color(self, colour):
        self.window.fill(colour)

    def draw_image(self, image_object, x, y):
        image_object.draw(self, x, y)

    def draw_text(self, text_object, text, colour, x, y):
        text_object.draw(self, text, colour, x, y)

    def draw_sprite(self, sprite):
        sprite.draw(self)

    def draw_rectangle(self, rectangle_object, colour, x, y, filled=True, outline=1):
        rectangle_object.draw(self, colour, x, y, filled, outline)

    def draw_button(self, button_object, color, text):
        button_object.draw(self, color=color, text=text)

    def update(self):
        pg.display.update()
        self.clock.tick(self.fps)

    def run(self, process, draw):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            if run:
                run = process(self.clock.get_time() / 1000 * 30)
                draw(self)
                self.update()


# PYGAME INPUT #
class Mouse:
    def __init__(self):
        self.pressed = pg.mouse.get_pressed()
        self.position = pg.mouse.get_pos()
        self.movement = pg.mouse.get_rel()
        self.visible = pg.mouse.get_visible()
        self.focused = pg.mouse.get_focused()
        self.cursor = pg.mouse.get_cursor()

    def get_pressed(self):
        self.pressed = pg.mouse.get_pressed()
        return self.pressed

    def get_position(self):
        self.position = pg.mouse.get_pos()
        return self.position

    def set_position(self, x, y):
        pg.mouse.set_pos(x, y)
        self.position = pg.mouse.get_pos()

    def get_movement(self):
        self.movement = pg.mouse.get_rel()
        return self.movement

    def get_visible(self):
        self.visible = pg.mouse.get_visible()
        return self.visible

    def set_visible(self, visible):
        pg.mouse.set_visible(visible)
        self.visible = pg.mouse.get_visible()

    def get_focused(self):
        self.focused = pg.mouse.get_focused()
        return self.focused

    def get_cursor(self):
        self.cursor = pg.mouse.get_cursor()
        return self.cursor

    def set_cursor(self, cursor):
        pg.mouse.set_cursor(cursor)
        self.cursor = pg.mouse.get_cursor()

    def tick(self):
        self.pressed = pg.mouse.get_pressed()
        self.position = pg.mouse.get_pos()
        self.movement = pg.mouse.get_rel()
        self.visible = pg.mouse.get_visible()
        self.focused = pg.mouse.get_focused()
        self.cursor = pg.mouse.get_cursor()


class Keyboard:
    def __init__(self):
        self.pressed = pg.key.get_pressed()
        self.modifiers = pg.key.get_mods()
        self.visible = pg.key.get_focused()

    def get_pressed(self):
        self.pressed = pg.key.get_pressed()
        return self.pressed

    def get_modifiers(self):
        self.modifiers = pg.key.get_mods()
        return self.modifiers

    def get_visible(self):
        self.visible = pg.key.get_focused()
        return self.visible

    def tick(self):
        self.pressed = pg.key.get_pressed()
        self.modifiers = pg.key.get_mods()
        self.visible = pg.key.get_focused()


# PYGAME IMAGE #

class Image:
    def __init__(self, args, mode="f"):
        width, height = pg.display.get_surface().get_size()
        self.HALF_WIDTH = round(width / 2)
        self.HALF_HEIGHT = round(height / 2)
        if mode == "f":
            self.image = pg.image.load(args)
        elif mode == "o":
            self.image = args
        else:
            raise ValueError(f"Invalid Option: '{mode}'")

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.image, -angle)

    def resize(self, width, height, smooth=True):
        if smooth:
            self.image = pg.transform.smoothscale(self.image, (width, height))
        else:
            self.image = pg.transform.scale(self.image, (width, height))

    def scale(self, scale, smooth=True):
        if smooth:
            self.image = pg.transform.smoothscale(self.image, (
                round(self.image.get_width() * scale), round(self.image.get_height() * scale)))
        else:
            self.image = pg.transform.scale(self.image, (
                round(self.image.get_width() * scale), round(self.image.get_height() * scale)))

    def draw(self, window, x, y):
        window.window.blit(self.image, (x + self.HALF_WIDTH - (self.image.get_width() / 2),
                                        self.HALF_HEIGHT - y - (self.image.get_height() / 2)))


class Sprite:
    def __init__(self, image, x, y, mode="f"):
        self.smooth = True
        width, height = pg.display.get_surface().get_size()
        self.HALF_WIDTH = round(width / 2)
        self.HALF_HEIGHT = round(height / 2)
        if mode == "f":
            self.image = Image(image, mode="f")
        elif mode == "o":
            self.image = image
        else:
            raise ValueError(f"Invalid Option: '{mode}'")
        self.x = x
        self.y = y
        self.size = 100
        self.rotation = 0

    def get_image(self):
        return self.image

    def get_surface(self):
        return self.image.image

    def clone(self):
        return Sprite(Image(self.get_surface().copy(), "o"), self.x, self.y, "o")

    def rotate(self, angle):
        self.rotation = angle
        self.image.rotate(angle)

    def resize(self, size):
        self.image.scale(size / self.size, self.smooth)
        self.size = size

    def move(self, steps):
        self.x += m.sin(m.radians(self.rotation)) * steps
        self.y += m.cos(m.radians(self.rotation)) * steps

    def clicked(self, mouse_object):
        if mouse_object.get_pressed()[0]:
            hit_box = pygame.Rect(self.x + self.HALF_WIDTH - (self.image.image.get_width() / 2),
                                  self.HALF_HEIGHT - self.y - (self.image.image.get_height() / 2),
                                  self.image.image.get_width(), self.image.image.get_height())
            if hit_box.collidepoint(mouse_object.get_position()):
                return True
        return False

    def draw(self, window):
        self.image.draw(window, self.x, self.y)


# PYGAME TEXT #
class Text:
    def __init__(self, font, font_size):
        width, height = pg.display.get_surface().get_size()
        self.Font = pg.font.Font(font, font_size)
        self.HALF_WIDTH = round(width / 2)
        self.HALF_HEIGHT = round(height / 2)

    def get_image(self, text, colour):
        return Image(self.Font.render(text, True, colour), "o")

    def draw(self, window, text, colour, x, y):
        text_to_render = self.Font.render(text, True, colour)
        window.window.blit(text_to_render, (x + self.HALF_WIDTH - (text_to_render.get_width() / 2),
                                            self.HALF_HEIGHT - y - (text_to_render.get_height() / 2)))


class SystemText:
    def __init__(self, font, font_size):
        width, height = pg.display.get_surface().get_size()
        self.Font = pg.font.SysFont(font, font_size)
        self.HALF_WIDTH = round(width / 2)
        self.HALF_HEIGHT = round(height / 2)

    def get_image(self, text, colour):
        return Image(self.Font.render(text, True, colour), "o")

    def draw(self, window, text, colour, x, y):
        text_to_render = self.Font.render(text, True, colour)
        window.window.blit(text_to_render, (x + self.HALF_WIDTH - (text_to_render.get_width() / 2),
                                            self.HALF_HEIGHT - y - (text_to_render.get_height() / 2)))


# PYGAME SHAPES #

class Rectangle:
    def __init__(self, width, height):
        w_width, w_height = pg.display.get_surface().get_size()
        self.width = width
        self.height = height
        self.HALF_WIDTH = round(w_width / 2)
        self.HALF_HEIGHT = round(w_height / 2)

    def get_rect(self):
        return pg.Rect(0, 0, self.width, self.height)

    def draw(self, window, colour, x, y, filled=True, outline=1):
        if filled:
            pg.draw.rect(window.window, colour,
                         pygame.Rect(x + self.HALF_WIDTH - (self.width / 2), self.HALF_HEIGHT - y - (self.height / 2),
                                     self.width, self.height))
        else:
            pg.draw.rect(window.window, colour,
                         pygame.Rect(x + self.HALF_WIDTH - (self.width / 2), self.HALF_HEIGHT - y - (self.height / 2),
                                     self.width, self.height), outline)


# PYGAME GUI #

class Button(Sprite):
    def __init__(self, image, text_object, x, y):
        super().__init__(image, x, y)
        self.text_object = text_object

    def draw(self, window, **kwargs):
        super().draw(window)
        self.text_object.draw(window, kwargs["text"], kwargs["color"], self.x, self.y)


pg.init()

if __name__ == "__main__":
    def __process(_delta_time):
        return True


    def __update(windows):
        windows.fill_color(WHITE)
        windows.draw_text(rootFont, "About PyGameTools", BLACK, 0, 20)
        windows.draw_text(rootFont, "PyGameTools V1.0 (pygame 2.1.2)", BLACK, 0, 0)
        windows.draw_text(rootFont, "The Font Should Be Comic Sans", BLACK, 0, -20)


    root = Window(800, 600)
    root.set_title("PyGameTools")
    rootFont = SystemText("Comic Sans MS", 20)
    root.run(__process, __update)
