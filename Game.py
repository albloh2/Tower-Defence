import GameTools as gt
import constants as const

class Shooter(gt.Sprite):
    def __init__(self, image, x, y, mode="f"):
        super().__init__(image, x, y, mode, gt.ALPHA_SURFACE)
        self.timer = gt.Timer(0.5)

    def process(self, enemy_sprites, money):
        if self.timer.tick():
            self.timer.reset()
            enemy_sprites, money = self.shoot(enemy_sprites, money)
        return enemy_sprites, money

    def shoot(self, enemy_sprites, money):
        index = None
        shortest_distance = const.SHOOTER_MAX_DISTANCE_RANGE
        for i in range(len(enemy_sprites)):
            distance = enemy_sprites[i].distance_to_point(self.x, self.y)
            if shortest_distance > distance:
                index = i
                shortest_distance = distance
        try:
            enemy_sprites.pop(index)
            money += 1
        except TypeError:
            pass
        return enemy_sprites, money


class Enemy(gt.Sprite):
    def __init__(self, image, x, y, mode="f"):
        self.x = None
        self.y = None
        self.rotation = None
        super().__init__(image, x, y, mode, gt.ALPHA_SURFACE)
        self.index = 0
        # print(f"[INFO] Enemy spawned with ID {id(self)}")

    def process(self, health, enemy_count):
        if self.index == 0:
            self.x = const.ENEMY_PATH[self.index][0]
            self.y = const.ENEMY_PATH[self.index][1]
            self.index += 1
        elif self.index == len(const.ENEMY_PATH):
            health -= 5
            enemy_count -= 1
            return True, health, enemy_count
        else:
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
        return False, health, enemy_count
