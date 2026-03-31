# ChaseEnemy.py
from Enemy import Enemy

class ChaseEnemy(Enemy):
    def __init__(self, x, y, speed=2):
        super().__init__(x, y)
        self.speed = speed

    def update(self, player=None):
        if player is None:
            return

        if player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed