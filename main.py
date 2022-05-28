import os
import GameTools as gt
import constants as const


def process(_delta_time):
    global Mode
    if Mode == "main_menu":
        if Mouse.get_pressed()[0]:
            print(Mouse.get_position())
            load_level(1)
            Mode = "game_1"
    elif Mode == "game_1":
        if ButtonPlay.clicked(Mouse):
            return False
        handle_ui_buy_shooter()

    return True


def update(windows):
    if Mode == "main_menu":
        windows.fill_color(gt.WHITE)
        windows.draw_text(Font48, "Tower Defense Game", gt.BLACK, 0, -50)
        windows.draw_text(Font48, "Click Anywhere To Start", gt.BLACK, 0, -100)
        windows.draw_sprite(ShooterSprite)
    elif Mode == "game_1":
        windows.draw_image(LevelBackground, 0, 0)
        windows.draw_rectangle(UIBarMain, gt.BLACK, 0, -335)
        windows.draw_text(Font24, f"Wave: {Wave}", gt.WHITE, -590, -335)
        windows.draw_text(Font24, f"Health: {Health}", gt.WHITE, -450, -335)
        windows.draw_text(Font24, f"Money: ${Money}", gt.WHITE, -300, -335)
        windows.draw_button(ButtonPlay, gt.BLACK, "Start")
        windows.draw_sprite(ShooterSprite)
        windows.draw_text(Font24, f"${const.SHOOTER_PRICE}", gt.WHITE, -150, -335)
        for i in range(len(ShooterSpriteClones)):
            windows.draw_sprite(ShooterSpriteClones[i])
        # windows.draw_button(ButtonShop, gt.BLACK, "Shop")
        windows.draw_text(Font24, "Alpha Preview. Version 1.0.0-a.1.", gt.BLACK, -495, 345)
        return
    elif Mode == "loser":
        windows.fill_color(gt.WHITE)
        windows.draw_text(Font48, "You Loser", gt.BLACK, 0, 0)
    windows.draw_text(Font24, "Alpha Preview. Version 1.0.0-a.1.", gt.BLACK, -495, -345)


def handle_ui_buy_shooter():
    global IsClicked, Money
    if ShooterSprite.clicked(Mouse) and not IsClicked and Money >= const.SHOOTER_PRICE:
        IsClicked = True
        Money -= const.SHOOTER_PRICE
        ShooterSpriteClones.append(ShooterSprite.clone())
    if IsClicked:
        ShooterSpriteClones[len(ShooterSpriteClones) - 1].x = \
            Mouse.get_position()[0] - gt.PYGAME_API.display.get_surface().get_size()[0] / 2
        ShooterSpriteClones[len(ShooterSpriteClones) - 1].y = \
            gt.PYGAME_API.display.get_surface().get_size()[1] / 2 - Mouse.get_position()[1]
    if not Mouse.get_pressed()[0] and IsClicked:
        IsClicked = False
        if ShooterSpriteClones[len(ShooterSpriteClones) - 1].y < -300:
            ShooterSpriteClones.pop()
            Money += const.SHOOTER_PRICE


def splash_screen():
    global Mode
    Mode = "splash"
    Window.fill_color(gt.WHITE)
    Window.draw_text(Font24, "Albloh2 Gaming", gt.BLACK, 0, 0)
    Window.draw_text(Font24, "Alpha Preview. Version 1.0.0-a.1.", gt.BLACK, -495, -345)
    Window.update()
    Mouse.set_cursor(gt.WAIT)
    gt.PYGAME_API.time.wait(1000)
    Mouse.set_cursor(gt.ARROW)
    Mode = "main_menu"


def load_assets():
    global Font24, Font48, ShooterSprite
    Font24 = gt.Text(os.path.join("Assets", "TD_Toon Around.otf"), 24)
    Font48 = gt.Text(os.path.join("Assets", "TD_Toon Around.otf"), 48)
    ShooterSprite = gt.Sprite(os.path.join("Assets", "TD_Shooter_1.svg"), 0, 50)


def load_level(level_id):
    global LevelBackground, UIBarMain, Wave, ButtonPlay, ButtonShop, Money, Health
    Mouse.set_cursor(gt.WAIT)
    Window.fill_color(gt.BLACK)
    Window.draw_text(Font24, "Loading...", gt.WHITE, 0, 0)
    Window.draw_text(Font24, "Alpha Preview. Version 1.0.0-a.1.", gt.WHITE, -495, -345)
    Window.update()
    gt.PYGAME_API.time.wait(1000)
    LevelBackground = gt.Image(os.path.join("Assets", f"TD_Level_{level_id}.png"))
    UIBarMain = gt.Rectangle(1280, 50)
    ButtonPlay = gt.Button(os.path.join("Assets", "TD_Button_1.svg"), Font24, 590, -335)
    ShooterSprite.resize(100)
    ShooterSprite.x = -200
    ShooterSprite.y = -335
    # ButtonShop = gt.Button(os.path.join("Assets", "TD_Button_1.svg"), Font24, 500, -335)
    Wave = 0
    Money = const.INITIAL_MONEY
    Health = const.INITIAL_HEALTH
    Mouse.set_cursor(gt.ARROW)


def main():
    global Font24, Font48, ShooterSprite, Mouse, Keyboard, Mode, LevelBackground, UIBarMain, Wave, Window, IsClicked, \
        ShooterSpriteClones
    LevelBackground = None
    UIBarMain = None
    Wave = None
    IsClicked = False
    ShooterSpriteClones = []
    Mode = "init"
    Window = gt.Window(const.WIDTH, const.HEIGHT)
    Window.set_title("Tower Defense Game Alpha Preview")
    load_assets()
    ShooterSprite.rotate(90)
    Window.set_icon(ShooterSprite.get_surface())
    ShooterSprite.resize(200)
    Mouse = gt.Mouse()
    Keyboard = gt.Keyboard()
    splash_screen()
    Window.run(process, update)


if __name__ == "__main__":
    main()
