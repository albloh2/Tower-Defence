import GameTools as gt
import constants as const
import math as m
import os


class Shooter(gt.Sprite):
    def __init__(self, image, x, y, mode="f"):
        super().__init__(image, x, y, mode, gt.ALPHA_SURFACE)
        self.timer = gt.Timer(0.5)

    def process(self, bullet_sprites):
        if self.timer.tick():
            self.timer.reset()
            self.shoot(bullet_sprites)

    def shoot(self, bullet_sprites):
        bullet_sprites.append(Bullet(os.path.join("Assets", "TD_Bullet.svg"), self.x, self.y, self.rotation+90))


class Enemy(gt.Sprite):
    def __init__(self, image, x, y, mode="f"):
        self.x = None
        self.y = None
        self.rotation = None
        super().__init__(image, x, y, mode, gt.ALPHA_SURFACE)
        self.index = 0
        # print(f"[INFO] Enemy spawned with ID {id(self)}")

    def process(self, health, enemy_count, delta_time):
        if self.index == 0:
            self.x = const.ENEMY_PATH[self.index][0]
            self.y = const.ENEMY_PATH[self.index][1]
            self.index += 1
        elif self.index == len(const.ENEMY_PATH):
            health -= 5
            enemy_count -= 1
            return True, health, enemy_count
        else:
            for i in range(int(5 * delta_time)):
                if self.x < const.ENEMY_PATH[self.index][0]:
                    self.x += 1
                elif self.x > const.ENEMY_PATH[self.index][0]:
                    self.x -= 1
                if self.y < const.ENEMY_PATH[self.index][1]:
                    self.y += 1
                elif self.y > const.ENEMY_PATH[self.index][1]:
                    self.y -= 1
                if self.x == const.ENEMY_PATH[self.index][0] and self.y == const.ENEMY_PATH[self.index][1]:
                    self.index += 1
                if self.index == len(const.ENEMY_PATH):
                    break
        return False, health, enemy_count


class Bullet(gt.Sprite):
    def __init__(self, image, x, y, rotation, mode="f"):
        super().__init__(image, x, y, mode, gt.ALPHA_SURFACE)
        self.rotate(rotation)

    def process(self, delta_time):
        for i in range(int(10 * delta_time)):
            self.move(1)
            if self.is_touching_edge():
                return True
        return False
