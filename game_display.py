from classes import *


def display_stars():
    for star_it in stars:
        star_it.draw()


def display_lives():
    for live in PlayerClass.lives_queue:
        live.draw(win)


def display_enemies():
    for enemy1 in enemy_storage["boss"]:
        if enemy1.status is "Dive":
            if len(butterfly) >= 2:
                enemy1.dive("boss", player)
            else:
                enemy1.dive("boss", player)
        enemy1.draw(win)

    for enemy1 in enemy_storage["butterfly"]:
        if enemy1.status is "Dive":
            enemy1.dive("butterfly", player)
        enemy1.draw(win)

    for enemy1 in enemy_storage["bee"]:
        if enemy1.status is "Dive":
            enemy1.dive("bee", player)
        enemy1.draw(win)


def display_missiles():
    for missile_it in player.missiles:
        missile_it.draw(win)

    # Draws the missiles the enemies have fired
    for enemy_missile_it in enemy_missile_buffer:
        enemy_missile_it.draw(win)


def display_explosion_fx():
    for explosion_it in enemy_storage["explosion"]:
        explosion_it.draw(win)

    # Draws the explosions for the player
    for explosion_it in enemy_storage["player_explosion"]:
        explosion_it.draw(win)