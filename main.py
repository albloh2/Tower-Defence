import pygame as pg
import GameTools as gt
import constants as const
import os


def update(windows):
    windows.fill_color(gt.WHITE)
    windows.draw_text(Font, "Hello World!", gt.BLACK, 0, 0, True)
    windows.update()


def main():
    global Font
    window = gt.Window(const.WIDTH, const.HEIGHT)
    window.set_title("Pygame Game")
    Font = gt.Text(os.path.join("Assets", "Toon Around.otf"), 24)
    window.centered = True
    frame_rate = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        update(window)
        frame_rate.tick(const.FPS)
    pg.quit()

if __name__ == "__main__":
    main()
