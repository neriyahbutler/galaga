from _enemy import *

import pygame
import random
import math

pygame.init()

width = 500
height = 500

win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Galaga")

# Objects below create the images for the video game.
gunship = pygame.image.load('sprites/player/gunship.gif')
missile = pygame.image.load('sprites/player/missile.gif')
# Arrays display the sprites for a specific type of enemy.
# For "boss_galaga", the 3rd and 4th element is the purple sprite for "boss_galaga"
# Explosion animation for enemy deaths
explosions = [pygame.image.load("sprites/enemy/enemy_death/exp1.png"), pygame.image.load("sprites/enemy/enemy_death/exp2.png"), pygame.image.load("sprites/enemy/enemy_death/exp3.png"), pygame.image.load("sprites/enemy/enemy_death/exp4.png"), pygame.image.load("sprites/enemy/enemy_death/exp5.png")]

# Resizing the sprites for the game to the appropriate size


diving_enemies = []

explosions[0] = pygame.transform.scale(explosions[0], (30, 30))
explosions[1] = pygame.transform.scale(explosions[1], (30, 30))
explosions[2] = pygame.transform.scale(explosions[2], (30, 30))
explosions[3] = pygame.transform.scale(explosions[3], (30, 30))
explosions[4] = pygame.transform.scale(explosions[4], (30, 30))

enemy_storage = {"boss": [], "butterfly": [], "bee": [], "explosion": []}
enemy_names = ["boss", "butterfly", "bee"]

stars = []

clock = pygame.time.Clock()
score = 0

x = 250
y = 400
vel = 4.5

boss_cnt = -1
butterfly_cnt = -1
bee_cnt = -1

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
            print("Missile fire!\n")
            self.missiles.append(Missile(self))
            self.prev_missile_time = pygame.time.get_ticks()
            # print("prev_missile_time updated to", self.prev_missile_time)
        # else:
            # print("condition failed, prev_missile_time is", self.prev_missile_time)
            # print("clock is set for", pygame.time.get_ticks())
    def getPosition(self):
        return [self.x, self.y]

class Missile(object):
    def __init__(self, gunship_):
        self.x = gunship_.x
        self.y = gunship_.y
        self.speed = 10

    def draw(self, win):
        win.blit(missile, (self.x + 10, self.y))

class explosion(object):
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

enemy_test = enemy("boss")

def redrawGameWindow():
    win.fill((0))
    _1UP = font.render("1UP", 1, (202, 0, 42))
    score_text = font.render(str(score), 1, (255,255,255))

    win.blit(_1UP, (40, 2))
    win.blit(score_text, (55, 15))

    for star_it in stars:
        star_it.draw()

    player.draw(win)

    for enemy1 in enemy_storage["boss"]:
        if enemy1.status is "Dive":
            if len(butterfly) >= 2:
                enemy1.dive("boss", player, True)
            else:
                enemy1.dive("boss", player, False)
        enemy1.draw(win)

    for enemy1 in enemy_storage["butterfly"]:
        if enemy1.status is "Dive":
            enemy1.dive("butterfly", player, False)
        enemy1.draw(win)

    for enemy1 in enemy_storage["bee"]:
        if enemy1.status is "Dive":
            enemy1.dive("bee", player, False)
        enemy1.draw(win)

    for missile_it in player.missiles:
        missile_it.draw(win)

    for explosion_it in enemy_storage["explosion"]:
        explosion_it.draw(win)

    pygame.display.update()

def create_fleet(fleet, fleet_type):
    global boss_cnt
    global butterfly_cnt
    global bee_cnt

    index = 0
    if fleet_type == "boss":
        while index < 4:
            index += 1
            new_enemy = enemy("boss")
            fleet["boss"].append(new_enemy)
            boss_cnt = boss_cnt + 1
    elif fleet_type == "bee":
        while index < 20:
            index += 1
            new_enemy = enemy("bee")
            fleet["bee"].append(new_enemy)
            bee_cnt = bee_cnt + 1
    else:
        while index < 16:
            index += 1
            new_enemy = enemy("butterfly")
            fleet["butterfly"].append(new_enemy)
            butterfly_cnt = butterfly_cnt + 1

def create_stars(stars_buffer, stars_count):
    for i in range(stars_count):
        stars_buffer.append(Star(random.randint(0, 4)))

def set_initial_pos(fleet, fleet_type):
    if fleet_type == "boss":
        y_cor = 40
        x_cor = 200
        x_increment = 30

        for enemy_1 in fleet[fleet_type]:
            enemy_1.x = x_cor
            enemy_1.y = y_cor
            enemy_1.initial_position = [x_cor, y_cor]
            x_cor += x_increment
            print("location set to", enemy_1.x, enemy_1.y)

    if fleet_type == "butterfly":
        y_cor = 70
        x_cor = 140
        x_increment = 30
        counter = 0

        new_row = False

        for enemy_1 in fleet[fleet_type]:
            if counter > 7 and not new_row:
                y_cor = 100
                x_cor = 140
                print("y coordinate has been changed")
                new_row = True
            enemy_1.x = x_cor
            enemy_1.y = y_cor
            enemy_1.initial_position = [x_cor, y_cor]
            x_cor += x_increment
            counter += 1

    if fleet_type == "bee":
        y_cor = 130
        x_cor = 85
        x_increment = 35
        counter = 0

        new_row = False

        for enemy_1 in fleet[fleet_type]:
            if counter > 9 and not new_row:
                y_cor = 160
                x_cor = 85
                print("y coordinate has been changed")
                new_row = True
            enemy_1.x = x_cor
            enemy_1.y = y_cor
            enemy_1.initial_position = [x_cor, y_cor]
            x_cor += x_increment
            counter += 1

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.x - t2.x, 2) + math.pow(t1.y - t2.y, 2))
    if distance < 30:
            return True
    return False


player = Gunship(250, 450)

create_stars(stars, 80)


create_fleet(enemy_storage, "boss")
set_initial_pos(enemy_storage, "boss")

create_fleet(enemy_storage, "butterfly")
set_initial_pos(enemy_storage, "butterfly")

create_fleet(enemy_storage, "bee")
set_initial_pos(enemy_storage, "bee")

run = True

firstDive_1 = True
firstDive_2 = True

firstD2_ready = False

prevTime = 0
diveTime = 0

# Something is fucked up about the pygame.time.get_ticks() shit...
# when I click the window and drag it, that's when the flying shit starts to happen.. idk why....
while run:
    font = pygame.font.Font("font/Joystix.ttf", 15)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if firstDive_1 or firstDive_2:
        if prevTime is 0:
            prevTime = pygame.time.get_ticks()
        else:
            if firstDive_1 is False:
                if (pygame.time.get_ticks() - prevTime) > 500:
                    firstD2_ready = True
            if (pygame.time.get_ticks() - prevTime) > 2000 or (not firstDive_1 and firstD2_ready):
                print("\nstarting initial dive\n")
                if firstDive_1 is True:
                    enemy_storage["boss"][random.randint(0, boss_cnt)].setStatus("Dive")
                    firstDive_1 = False
                    prevTime = pygame.time.get_ticks()
                    print("prevTime updated to", prevTime)
                else:
                    try:
                        print("2nd enemy starts flying\n")
                        enemy_storage["bee"][random.randint(0, bee_cnt)].setStatus("Dive")
                        firstDive_2 = False
                        diveTime = pygame.time.get_ticks()
                    except:
                        print("Error with bee diving\n")
    else:
        if (pygame.time.get_ticks() - diveTime) > 3000:
            if (random.randint(0, 3)) > 0:
                try:
                    enemy_storage["bee"][random.randint(0, bee_cnt)].setStatus("Dive")
                    diveTime = pygame.time.get_ticks()
                except:
                    print("Error with bee diving\n")
            else: # Seems like if you kill the enemy at a certain time mid-flight, the game crashes...
                try:
                    bee_iter = random.randint(0, boss_cnt)
                    enemy_storage["boss"][bee_iter].setStatus("Dive")
                    diveTime = pygame.time.get_ticks()
                except:
                    print("Error with boss diving", bee_iter, "\n")


    for missile_it in player.missiles:
        if missile_it.y > 0:
            missile_it.y -= missile_it.speed

            for enemy_1 in enemy_storage["boss"]:
                if isCollision(enemy_1, missile_it) and not enemy_1.isDead:
                    if enemy_1.health == 1:
                        score += 150 # Later on, check to see the position/action of the enemy
                        boss_cnt -= 1
                        enemy_1.isDead = True
                        player.missiles.pop(player.missiles.index(missile_it))

                        x_cor = enemy_1.x
                        y_cor = enemy_1.y

                        enemy_storage["explosion"].append(explosion(enemy_1))
                        enemy_storage["boss"].pop(enemy_storage["boss"].index(enemy_1))

                        print("Collision detected")
                        break
                    else:
                        enemy_1.health -= 1
                        player.missiles.pop(player.missiles.index(missile_it))

                        enemy_1.iter += 2
                        win.blit(boss_galaga[enemy_1.iter], ((enemy_1.x, enemy_1.y)))
                        break


            for enemy_1 in enemy_storage["butterfly"]:
                if isCollision(enemy_1, missile_it) and not enemy_1.isDead:
                    score += 80 # Later on, check to see the position/action of the enemy
                    butterfly_cnt -= 1
                    print("Current butterfly count:", butterfly_cnt)
                    enemy_1.isDead = True
                    player.missiles.pop(player.missiles.index(missile_it))

                    x_cor = enemy_1.x
                    y_cor = enemy_1.y

                    enemy_storage["explosion"].append(explosion(enemy_1))
                    enemy_storage["butterfly"].pop(enemy_storage["butterfly"].index(enemy_1))

                    print("Collision detected")
                    break

            for enemy_1 in enemy_storage["bee"]:
                if isCollision(enemy_1, missile_it) and not enemy_1.isDead:
                    score += 50 # Later on, check to see the position/action of the enemy
                    bee_cnt -= 1
                    print("Current bee count:", bee_cnt)
                    enemy_1.isDead = True
                    player.missiles.pop(player.missiles.index(missile_it))

                    x_cor = enemy_1.x
                    y_cor = enemy_1.y

                    enemy_storage["explosion"].append(explosion(enemy_1))
                    enemy_storage["bee"].pop(enemy_storage["bee"].index(enemy_1))

                    print("Collision detected")
                    break
        else:
            player.missiles.pop(player.missiles.index(missile_it))

    if keys[pygame.K_LEFT] and player.x - player.speed > 0:
        player.x -= player.speed

    if keys[pygame.K_RIGHT] and player.x + player.speed < 470:
        player.x += player.speed

    if keys[pygame.K_SPACE]:
        player.fire_missile()

    redrawGameWindow()


pygame.quit()
