import GameTools as gt
import constants as const
import math as m


class Shooter(gt.Sprite):
    def __init__(self, image, x, y, mode="f"):
        super().__init__(image, x, y, mode)

    def process(self):
        pass


class Enemy(gt.Sprite):
    def __init__(self, image, x, y, mode="f"):
        self.x = None
        self.y = None
        self.rotation = None
        super().__init__(image, x, y, mode)
        self.index = 0

    def process(self, health, enemy_count):
        if self.index == 0:
            self.x = const.ENEMY_PATH[self.index][0]
            self.y = const.ENEMY_PATH[self.index][1]
            self.index += 1
        elif self.index == len(const.ENEMY_PATH):
            health -= 1
            enemy_count -= 1
            return True, health, enemy_count
        else:
            for i in range(10):
                print(self.index)
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
