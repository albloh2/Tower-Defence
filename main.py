import os
import GameTools as gt
import Game as game
import constants as const
import random as r


def process(_delta_time):
    global Mode, InWave, Wave, EnemySpawnTimer, EnemyStillSpawning, EnemySpawned
    if Mode == "main_menu":
        if Mouse.get_pressed()[0]:
            print(Mouse.get_position())
            load_level(1)
            Mode = "game_1"
    elif Mode == "game_1":
        if Mouse.get_pressed()[0]:
            print(Mouse.get_position())
        if InWave:
            handle_enemy_spawn()
            handle_shooter_point()
        else:
            if ButtonPlay.clicked(Mouse) and not IsClicked:
                InWave = True
                EnemyStillSpawning = True
                EnemySpawned = 0
                EnemySpawnTimer = gt.Timer(0.1)
                Wave += 1
            handle_ui_buy_shooter()
        handle_enemy()
        print(EnemyCount)

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
        for i in range(len(EnemySpriteClones)):
            windows.draw_sprite(EnemySpriteClones[i])
        for i in range(len(ShooterSpriteClones)):
            windows.draw_sprite(ShooterSpriteClones[i])
        # windows.draw_button(ButtonShop, gt.BLACK, "Shop")
        windows.draw_text(Font24, "Alpha Preview. Version 1.0.0-a.1.", gt.BLACK, -495, 345)
        return
    elif Mode == "loser":
        windows.fill_color(gt.WHITE)
        windows.draw_text(Font48, "You Loser", gt.BLACK, 0, 0)
    windows.draw_text(Font24, "Alpha Preview. Version 1.0.0-a.1.", gt.BLACK, -495, -345)


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
    global LevelBackground, UIBarMain, Wave, ButtonPlay, ButtonShop, Money, Health, InWave
    InWave = False
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


def handle_ui_buy_shooter():
    global IsClicked, Money
    if ShooterSprite.clicked(Mouse) and not IsClicked and Money >= const.SHOOTER_PRICE:
        IsClicked = True
        Money -= const.SHOOTER_PRICE
        ShooterSpriteClones.append(game.Shooter(ShooterSprite, ShooterSprite.x, ShooterSprite.y, "s"))
    if IsClicked:
        ShooterSpriteClones[len(ShooterSpriteClones) - 1].x = Mouse.get_position()[0]
        ShooterSpriteClones[len(ShooterSpriteClones) - 1].y = Mouse.get_position()[1]
    if not Mouse.get_pressed()[0] and IsClicked:
        IsClicked = False
        if ShooterSpriteClones[len(ShooterSpriteClones) - 1].y < -300:
            ShooterSpriteClones.pop()
            Money += const.SHOOTER_PRICE


def handle_shooter_point():
    for i in ShooterSpriteClones:
        i.rotate_towards_point(Mouse.get_position()[0], Mouse.get_position()[1])


def handle_enemy():
    global Health, EnemyCount
    for i in range(len(EnemySpriteClones)):
        if i > len(EnemySpriteClones) - 1:
            break
        condition, Health, EnemyCount = EnemySpriteClones[i].process(Health, EnemyCount)
        if condition:
            EnemySpriteClones.pop(i)


def handle_enemy_spawn():
    global EnemyCount, InWave, EnemyStillSpawning, EnemyToSpawn, EnemySpawned
    if EnemySpawnTimer.tick():
        EnemySpriteClones.append(game.Enemy(os.path.join("Assets", "TD_Enemy_1.svg"), 0, 0))
        EnemyCount += 1
        EnemySpawned += 1
        if EnemySpawned < EnemyToSpawn:
            EnemySpawnTimer.reset()
        else:
            EnemyStillSpawning = False
            EnemyToSpawn += r.randint(0, 10)
    elif not EnemyStillSpawning:
        if EnemyCount == 0:
            InWave = False


def main():
    global Font24, Font48, ShooterSprite, Mouse, Keyboard, Mode, LevelBackground, UIBarMain, Wave, Window, IsClicked, \
        ShooterSpriteClones, InWave, EnemySpriteClones, EnemyCount, EnemySpawnTimer, EnemyStillSpawning, EnemyToSpawn, \
        EnemySpawned
    InWave = False
    LevelBackground = None
    UIBarMain = None
    Wave = None
    IsClicked = False
    EnemyToSpawn = 1
    EnemySpriteClones = []
    EnemyCount = 0
    EnemySpawnTimer = 0
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
