from _bezierCurve import bezierCurve

import pygame
import random

boss_galaga = [pygame.image.load("sprites/enemy/boss/b1.png"), pygame.image.load("sprites/enemy/boss/b2.png"), pygame.image.load("sprites/enemy/boss/b2_1.png"), pygame.image.load("sprites/enemy/boss/b2_2.png")]
bee = [pygame.image.load("sprites/enemy/bee/bee1.png"), pygame.image.load("sprites/enemy/bee/bee2.png")]
butterfly = [pygame.image.load("sprites/enemy/butterfly/b1.png"), pygame.image.load("sprites/enemy/butterfly/b2.png")]

boss_galaga[0] = pygame.transform.scale(boss_galaga[0], (30, 30))
boss_galaga[1] = pygame.transform.scale(boss_galaga[1], (30, 30))
boss_galaga[2] = pygame.transform.scale(boss_galaga[2], (30, 30))
boss_galaga[3] = pygame.transform.scale(boss_galaga[3], (30, 30))

bee[0] = pygame.transform.scale(bee[0], (30, 30))
bee[1] = pygame.transform.scale(bee[1], (30, 30))

butterfly[0] = pygame.transform.scale(butterfly[0], (30, 30))
butterfly[1] = pygame.transform.scale(butterfly[1], (30, 30))

class enemy(object):
    prev_draw_time = 0
    iter = 0
    drift_count = 0
    drift_end = False
    isDead = False
    status = 0

    curve_queue = 0
    initial_dive = False

    # new_curve = bezierCurve([250, 0], [175, 138], [444, 93], [249, 253])
    # new_curve2 = bezierCurve([249, 253], [136, 328], [149, 362], [233, 390])
    # new_curve3 = bezierCurve([233, 390], [332, 429], [353, 470], [207, 502])

    # curve_queue = [new_curve3, new_curve2, new_curve]

    def __init__(self, enemy_type):
        if enemy_type == "boss":
            self.enemy_type = "boss"
            self.health = 2
            self.isIdle = True
            self.x = 250
            self.y = -50
        if enemy_type == "butterfly":
            self.enemy_type = "butterfly"
            self.health = 1
            self.isIdle = True
            self.x = 250
            self.y = -50
        if enemy_type == "bee":
            self.enemy_type = "bee"
            self.health = 1
            self.isIdle = True
            self.x = 250
            self.y = -50
        print(enemy_type, "created")

    def draw(self, win):
        if self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 500:
            if (self.enemy_type == "boss" and self.health == 2)\
                    or (self.enemy_type == "butterfly" or self.enemy_type == "bee"):

                if self.iter < 1:
                    self.iter += 1
                else:
                    self.iter = 0
            else:
                # print("Boss color changed")
                if self.iter < 3:
                    self.iter += 1
                else:
                    self.iter = 2
            self.prev_draw_time = pygame.time.get_ticks()

        if self.enemy_type == "boss":
            win.blit(boss_galaga[self.iter], (self.x, self.y))
        elif self.enemy_type == "butterfly":
            win.blit(butterfly[self.iter], (self.x, self.y))
        else:
            win.blit(bee[self.iter], (self.x, self.y))

    def dive(self, type, gunship):
        self.status = "Dive"
        random_int = random.randint(1, 11)
        choice = random_int % 2

        if type == "butterfly":
            if self.initial_dive is False:
                if choice == 0:
                    self.curve_queue = [bezierCurve([self.x - 1, self.y + 253], [self.x - 29, self.y + 283], [self.x - 15, self.y + 259], [(gunship.x - random.randint(20,100)), self.y + 500]),\
                         bezierCurve([self.x, self.y], [self.x - 75, self.y + 138], [self.x + 194, self.y + 93], [self.x - 1, self.y + 253])]
                else:
                    self.curve_queue = [bezierCurve([self.x + 1, self.y + 253], [self.x + 29, self.y + 283], [self.x + 15, self.y + 259], [(gunship.x + random.randint(20,100)), self.y + 500]),\
                         bezierCurve([self.x, self.y], [self.x + 75, self.y + 138], [self.x - 194, self.y + 93], [self.x + 1, self.y + 253])]
                self.initial_dive = True

            if len(self.curve_queue) != 0:
                if len(self.curve_queue) == 1:
                    self.curve_queue[len(self.curve_queue) - 1].increaseVelocity()
                self.x = self.curve_queue[len(self.curve_queue) - 1].calculatePoint()[0]
                self.y = self.curve_queue[len(self.curve_queue) - 1].calculatePoint()[1]
                if self.curve_queue[len(self.curve_queue) - 1].t >= 1:
                    self.curve_queue.pop()
