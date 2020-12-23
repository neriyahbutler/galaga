from bezier_curve import BezierCurve
from game_setup import *

import pygame
import math
import random

boss_galaga = [pygame.image.load("sprites/enemy/boss/b1.png"),
               pygame.image.load("sprites/enemy/boss/b2.png"),
               pygame.image.load("sprites/enemy/boss/b2_1.png"),
               pygame.image.load("sprites/enemy/boss/b2_2.png")]

bee = [pygame.image.load("sprites/enemy/bee/bee1.png"),
       pygame.image.load("sprites/enemy/bee/bee2.png")]

butterfly = [pygame.image.load("sprites/enemy/butterfly/b1.png"),
             pygame.image.load("sprites/enemy/butterfly/b2.png")]

boss_galaga[0] = pygame.transform.scale(boss_galaga[0], (30, 30))
boss_galaga[1] = pygame.transform.scale(boss_galaga[1], (30, 30))
boss_galaga[2] = pygame.transform.scale(boss_galaga[2], (30, 30))
boss_galaga[3] = pygame.transform.scale(boss_galaga[3], (30, 30))

bee[0] = pygame.transform.scale(bee[0], (30, 30))
bee[1] = pygame.transform.scale(bee[1], (30, 30))

butterfly[0] = pygame.transform.scale(butterfly[0], (30, 30))
butterfly[1] = pygame.transform.scale(butterfly[1], (30, 30))

enemy_missile = pygame.image.load("sprites/enemy/enemy_missile/enemy_missile.png")
enemy_missile_buffer = []


class EnemyMissile(object):
    def __init__(self, enemy, slope):
        self.x = enemy[0]
        self.y = enemy[1]

        self.speed = 1
        self.slope = slope
        self.b = enemy[1] * 1/slope * (1/enemy[0])
        print("Missile slope:", self.slope)
        print("Missile x and y:", self.x, self.y)

    def draw(self, win):
        win.blit(enemy_missile, (self.x, self.y))
        pygame.draw.line(win, (255,0,255), (self.x, self.y), (self.x + 2, self.x * self.slope + self.b), 2)
        self.x += 2
        self.y = self.x * self.slope + self.b

class Enemy(object):
    global player

    image = 0
    initial_position = []

    prev_draw_time = 0
    iter = 0

    drift_count = 0
    drift_end = False

    isDead = False
    status = None

    curve_queue = 0
    initial_dive = False
    enemyMissileFired = False

    missile_fired = False

    angle = 0.0

    prev_x = 0
    prev_y = 0

    waypoint = []

    def __init__(self, enemy_type):
        if enemy_type == "boss":
            self.enemy_type = "boss"
            self.health = 2
            self.isIdle = True
            self.x = self.prev_x = 250
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

    def draw(self, win):
        if self.prev_draw_time == 0 or pygame.time.get_ticks() - self.prev_draw_time > 500:
            if (self.enemy_type == "boss" and self.health == 2) \
                    or (self.enemy_type == "butterfly" or self.enemy_type == "bee"):
                if self.iter < 1:
                    self.iter += 1
                else:
                    self.iter = 0
            else:
                if self.iter < 3:
                    self.iter += 1
                else:
                    self.iter = 2
            self.prev_draw_time = pygame.time.get_ticks()

        if self.enemy_type == "boss":
            self.image = pygame.transform.rotate(boss_galaga[self.iter], self.angle)
            win.blit(self.image, (self.x, self.y))
        elif self.enemy_type == "butterfly":
            win.blit(butterfly[self.iter], (self.x, self.y))
        else:
            win.blit(bee[self.iter], (self.x, self.y))

        # Resets the enemy's diving status once the diving sequence is completed
        if math.ceil(self.x) == self.initial_position[0] and math.ceil(self.y) == self.initial_position[1]:
            self.initial_dive = False
            self.set_status('None')

    def dive(self, type, gunship):
        random_int = random.randint(1, 11)
        choice = random_int % 2

        # Curves for the enemy's are generated if the initial dive is False
        if type == "butterfly":
            if self.initial_dive is False:
                self.generate_butterfly_curves(choice, gunship)
            self.adjust_position()

        if type == "bee":
            if self.initial_dive is False:
                self.generate_bee_curves(choice, gunship)
            self.adjust_position()

        if type == "boss":
            if self.initial_dive is False:
                self.generate_boss_curves(choice, gunship)
            self.adjust_position()

    def generate_butterfly_curves(self, choice, gunship):
        if choice == 0:
            end_pos = [(gunship.x - random.randint(20, 50)), self.y + 480]
            self.curve_queue = [BezierCurve([self.x - 1, self.y + 253],
                                            [self.x - 50, self.y + 330],
                                            [self.x - 15, self.y + 259],
                                            end_pos),
                                BezierCurve([self.x, self.y],
                                            [self.x - 75, self.y + 138],
                                            [self.x + 194, self.y + 93],
                                            [self.x - 1, self.y + 253])]
        else:
            end_pos = [(gunship.x + random.randint(20, 50)), self.y + 480]
            self.curve_queue = [BezierCurve([self.x + 1, self.y + 253],
                                            [self.x + 50, self.y + 330],
                                            [self.x + 15, self.y + 259],
                                            end_pos),
                                BezierCurve([self.x, self.y],
                                            [self.x + 75, self.y + 138],
                                            [self.x - 194, self.y + 93],
                                            [self.x + 1, self.y + 253])]
            self.initial_dive = True

    def generate_bee_curves(self, choice, gunship):
        if choice == 0:
            self.curve_queue = [BezierCurve([self.x - 1, self.y + 253],
                                            [self.x - 50, self.y + 330], [self.x - 15, self.y + 259],
                                            [(gunship.x - random.randint(20, 50)), self.y + 480]),
                                BezierCurve([self.x, self.y],
                                            [self.x - 75, self.y + 138],
                                            [self.x + 194, self.y + 93],
                                            [self.x - 1, self.y + 253])]
        else:
            self.curve_queue = [BezierCurve([self.x + 1, self.y + 253],
                                            [self.x + 50, self.y + 330],
                                            [self.x + 15, self.y + 259],
                                            [(gunship.x + random.randint(20, 50)), self.y + 480]),
                                BezierCurve([self.x, self.y],
                                            [self.x + 75, self.y + 138],
                                            [self.x - 194, self.y + 93],
                                            [self.x + 1, self.y + 253])]
        self.initial_dive = True

    def generate_boss_curves(self, choice, gunship):
        if choice == 0:
            self.curve_queue = [BezierCurve([self.x + 150.7, self.y + 264], [self.x + 134.2, self.y + 321.6],
                                            [self.x + 0.2, self.y + 433],
                                            [(gunship.x - random.randint(20, 60)), self.y + 464]),
                                BezierCurve([self.x + 0.5, self.y + 95], [self.x + 17, self.y + 152.6],
                                            [self.x + 155, self.y + 182], [self.x + 150.7, self.y + 264]),
                                BezierCurve([self.x + 98, self.y + 96], [self.x + 106, self.y + 25],
                                            [self.x + -1, self.y + 10.5], [self.x + 0.5, self.y + 95]),
                                BezierCurve([self.x, self.y], [self.x - 48, self.y + 177],
                                            [self.x + 102, self.y + 172], [self.x + 98, self.y + 96])]
        else:
            self.curve_queue = [BezierCurve([self.x - 150.7, self.y + 264], [self.x - 134.2, self.y + 321.6],
                                            [self.x - 0.2, self.y + 433],
                                            [(gunship.x + random.randint(20, 60)), self.y + 464]),
                                BezierCurve([self.x - 0.5, self.y + 95], [self.x - 17, self.y + 152.6],
                                            [self.x - 155, self.y + 182], [self.x - 150.7, self.y + 264]),
                                BezierCurve([self.x - 98, self.y + 96], [self.x - 106, self.y + 25],
                                            [self.x - -1, self.y + 10.5], [self.x - 0.5, self.y + 95]),
                                BezierCurve([self.x, self.y], [self.x + 48, self.y + 177],
                                            [self.x - 102, self.y + 172], [self.x - 98, self.y + 96])]
        self.initial_dive = True

    # Adjusts the position of the enemy based on the next position in the "curve queue"
    def adjust_position(self):
        self.prev_x = self.x
        if len(self.curve_queue) > 1 and self.missile_fired is False:
            slope = (player.y - self.y)/(player.x - self.x)
            print("Enemy location:", self.x, self.y)
            print("PLayer location:", player.x, player.y)
            self.fire_enemy_missile(slope)
            self.missile_fired = True

        if len(self.curve_queue) != 0:
            self.waypoint = self.curve_queue[len(self.curve_queue) - 1].end_pnt
            if len(self.curve_queue) == 1:
                self.curve_queue[len(self.curve_queue) - 1].increase_velocity()

            self.x = self.curve_queue[len(self.curve_queue) - 1].calculate_point()[0]
            self.y = self.curve_queue[len(self.curve_queue) - 1].calculate_point()[1]

            if self.curve_queue[len(self.curve_queue) - 1].t >= 1:
                self.curve_queue.pop()
                if len(self.curve_queue) == 0 and self.y > self.initial_position[1]:
                    self.x = self.initial_position[0]
                    self.y = -1
                    self.curve_queue = [
                        BezierCurve([self.x, self.y], [self.x, self.y], [self.x, self.initial_position[1]],
                                    [self.x, self.initial_position[1]])]

    def fire_enemy_missile(self, slope):
        enemy_missile_buffer.append(EnemyMissile([self.x, self.y], slope))

    def set_status(self, state):
        self.status = state

    def set_prev_pos(self, x, y):
        self.prev_x = x
        self.prev_y = y


class Star(object):
    colors = ["red", "green", "blue", "white"]

    def __init__(self, layer):
        self.timer = 0
        self.visible = False
        self.scroll = True
        self.prevFlickerTime = 0
        self.flickerCooldown = 300
        self.flickerSpeed = 0.15 * (random.randint(0, 1000) / 10000) * 0.45

        self.color = (0, 0, 0)

        self.scrollSpeed = 2

        if layer == 0:
            self.color = (255, 255, 255)
        if layer == 1:
            self.color = (255, 0, 0)
        if layer == 2:
            self.color = (0, 0, 255)
        if layer == 3:
            self.color = (0, 255, 0)

        self.x = random.randint(1, 100000) % width
        self.y = random.randint(1, 100000) % height

        self.y_max = 200

    def draw(self):
        if random.randint(1, 10) % 2:
            self.visible = True
        else:
            self.visible = False
            self.prevFlickerTime = pygame.time.get_ticks()

        if self.y > height:
            self.y = 0
            self.x = random.randint(1, 100000) % width

        if self.visible:
            win.set_at((self.x, self.y), self.color)

        if self.scroll:
            self.y += self.scrollSpeed


class Gunship(object):
    missiles = []
    prev_missile_time = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.missile_ready = True

    def draw(self, win):
        win.blit(gunship, (self.x, self.y))

    def fire_missile(self):
        if len(self.missiles) < 2 and (self.prev_missile_time == 0 or pygame.time.get_ticks() - self.prev_missile_time > 70):
            sfx_13.play()
            self.missiles.append(Missile(self))
            self.prev_missile_time = pygame.time.get_ticks()

    def get_position(self):
        return [self.x, self.y]

    def set_position(self, x, y):
        self.x = x
        self.y = y


class Missile(object):
    def __init__(self, gunship_):
        self.x = gunship_.x
        self.y = gunship_.y
        self.speed = 10

    def draw(self, win):
        win.blit(missile, (self.x + 10, self.y))


class Explosion(object):
    index = 0

    def __init__(self, enemy):
        self.x = enemy.x
        self.y = enemy.y

    def draw(self, win):
        if self.index < 5:
            win.blit(explosions[self.index], (self.x, self.y))
            self.index += 1
        else:
            enemy_storage["explosion"].pop(enemy_storage["explosion"].index(self))


class PlayerExplosion(object):
    index = 0

    def __init__(self, gunship):
        self.x = gunship.x
        self.y = gunship.y

    def draw(self, win):
        if self.index < 16:
            win.blit(player_explosions[self.index], (self.x, self.y))
            self.index += 1
        else:
            enemy_storage["player_explosion"].pop(enemy_storage["player_explosion"].index(self))


class Object_SFX(object):
    type = ''

    def __init__(self, type):
        self.type = type
        self.sfx1 = pygame.mixer.Sound("galaga_sfx/wav/04 Alien Flying.wav")
        if type == 'boss':
            self.sfx2 = pygame.mixer.Sound("galaga_sfx/wav/08 Boss Stricken#2.wav")
            self.sfx3 = pygame.mixer.Sound("galaga_sfx/wav/07 Boss Stricken#1.wav")
        elif type == 'bee':
            self.sfx2 = pygame.mixer.Sound("galaga_sfx/wav/05 Zako Stricken.wav")
        else:
            self.sfx2 = pygame.mixer.Sound("galaga_sfx/wav/06 Goei Stricken.wav")


class PlayerClass(object):
    lives = 0
    score = 0.0
    lives_queue = []
    x = 5
    y = 465
    death_timer = 0.0

    def __init__(self):
        self.lives = 3
        self.generate_lives()
        print("Player class has been created")

    def generate_lives(self):
        for i in range(3):
            self.lives_queue.append(Gunship(self.x, self.y))
            self.x += 35
            print("Generating lives", self.lives_queue[i].x, self.lives_queue[i].y)

    def adjust_score(self, score):
        self.score = score

    def increase_lives(self):
        self.lives = self.lives + 1
        self.lives_queue.append(Gunship(self.x, self.y))

    def decrease_lives(self):
        self.lives = self.lives - 1
        curr_gunship = self.lives_queue.pop()
        curr_gunship.set_position(-100, 450)
        self.x -= 35
        return curr_gunship

    def get_lives_count(self):
        return self.lives

    def get_score(self):
        return self.score

    def set_death_timer(self, timer):
        self.death_timer = timer

    def get_death_timer(self):
        return self.death_timer


def create_fleet(fleet, fleet_type):
    global boss_cnt
    global butterfly_cnt
    global bee_cnt

    index = 0
    if fleet_type == "boss":
        while index < 4:
            index += 1
            new_enemy = Enemy("boss")
            fleet["boss"].append([new_enemy, Object_SFX("boss")])
            boss_cnt = boss_cnt + 1
    elif fleet_type == "bee":
        while index < 20:
            index += 1
            new_enemy = Enemy("bee")
            fleet["bee"].append([new_enemy, Object_SFX("bee")])
            bee_cnt = bee_cnt + 1
    else:
        while index < 16:
            index += 1
            new_enemy = Enemy("butterfly")
            fleet["butterfly"].append([new_enemy, Object_SFX("butterfly")])
            butterfly_cnt = butterfly_cnt + 1


def create_stars(stars_buffer, stars_count):
    for i in range(stars_count):
        stars_buffer.append(Star(random.randint(0, 4)))


def set_init_pos(fleet, fleet_type):
    if fleet_type == "boss":
        set_init_pos_boss(fleet)
    if fleet_type == "butterfly":
        set_init_pos_butterfly(fleet)
    if fleet_type == "bee":
        set_init_pos_bee(fleet)


def set_init_pos_boss(fleet):
    y_cor = 40
    x_cor = 200
    x_increment = 30

    for enemy_1 in fleet["boss"]:
        enemy_1[0].x = x_cor
        enemy_1[0].y = y_cor
        enemy_1[0].initial_position = [x_cor, y_cor]
        enemy_1[0].set_prev_pos(x_cor, y_cor)
        x_cor += x_increment


def set_init_pos_butterfly(fleet):
    y_cor = 70
    x_cor = 140
    x_increment = 30
    counter = 0

    new_row = False

    for enemy_1 in fleet["butterfly"]:
        if counter > 7 and not new_row:
            y_cor = 100
            x_cor = 140
            new_row = True
        enemy_1[0].x = x_cor
        enemy_1[0].y = y_cor
        enemy_1[0].initial_position = [x_cor, y_cor]
        enemy_1[0].set_prev_pos(x_cor, y_cor)
        x_cor += x_increment
        counter += 1


def set_init_pos_bee(fleet):
    y_cor = 130
    x_cor = 85
    x_increment = 35
    counter = 0

    new_row = False

    for enemy_1 in fleet['bee']:
        if counter > 9 and not new_row:
            y_cor = 160
            x_cor = 85
            new_row = True
        enemy_1[0].x = x_cor
        enemy_1[0].y = y_cor
        enemy_1[0].initial_position = [x_cor, y_cor]
        enemy_1[0].set_prev_pos(x_cor, y_cor)
        x_cor += x_increment
        counter += 1


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.x - t2.x, 2) + math.pow(t1.y - t2.y, 2))
    if distance < 30:
            return True
    return False


player = Gunship(250, 450)

create_stars(stars, 80)

create_fleet(enemy_storage, "boss")
set_init_pos(enemy_storage, "boss")

create_fleet(enemy_storage, "butterfly")
set_init_pos(enemy_storage, "butterfly")

create_fleet(enemy_storage, "bee")
set_init_pos(enemy_storage, "bee")

PlayerObject = PlayerClass()

run = True

firstDive_1 = True
firstDive_2 = True

firstD2_ready = False

deathBoolean = False

prevTime = 0
diveTime = 0
deathTime = 0

player_temp = ""