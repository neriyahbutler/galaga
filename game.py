from classes import *
from game_display import *


def redrawGameWindow():
    win.fill((0))
    _1UP = font.render("1UP", 1, (202, 0, 42))
    score_text = font.render(str(score), 1, (255,255,255))

    win.blit(_1UP, (40, 2))
    win.blit(score_text, (55, 15))

    display_stars()

    player.draw(win)

    display_enemies()

    display_missiles()

    display_lives()

    display_explosion_fx()

    pygame.display.update()


while run:
    font = pygame.font.Font("font/Joystix.ttf", 15)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # The algorithm for making the enemies fly
    if firstDive_1 or firstDive_2:
        if prevTime == 0:
            prevTime = pygame.time.get_ticks()
        else:
            if firstDive_1 is False:
                if (pygame.time.get_ticks() - prevTime) > 500:
                    firstD2_ready = True
            if (pygame.time.get_ticks() - prevTime) > 2000 or (not firstDive_1 and firstD2_ready):
                if firstDive_1 is True:
                    boss_it = random.randint(0, boss_cnt)
                    enemy_storage["boss"][boss_it][0].set_status("Dive")
                    enemy_storage["boss"][boss_it][1].sfx1.play()

                    firstDive_1 = False
                    prevTime = pygame.time.get_ticks()
                else:
                    try:
                        boss_it = random.randint(0, bee_cnt)
                        enemy_storage["bee"][boss_it][0].set_status("Dive")
                        enemy_storage["bee"][boss_it][1].sfx1.play()

                        firstDive_2 = False
                        diveTime = pygame.time.get_ticks()
                    except IndexError:
                        print("Error with bee diving\n")
    else:
        if (pygame.time.get_ticks() - diveTime) > 3000:
            x = random.randint(0, 4)

            if (x == 0 or x == 3) and bee_cnt > 0:
                try:
                    bee_it = random.randint(0, bee_cnt)
                    enemy_storage["bee"][bee_it][0].set_status("Dive")
                    enemy_storage["bee"][bee_it][1].sfx1.play()

                    diveTime = pygame.time.get_ticks()
                except IndexError:
                    print("Error with bee diving\n")

            elif (x == 1 or x == 4) and butterfly_cnt > 0:
                try:
                    butterfly_it = random.randint(0, butterfly_cnt)
                    enemy_storage["butterfly"][butterfly_it][0].set_status("Dive")
                    enemy_storage["butterfly"][butterfly_it][1].sfx1.play()

                    diveTime = pygame.time.get_ticks()
                except IndexError:
                    print("Error with butterfly diving\n")

            if x == 2 and boss_cnt > 0:
                try:
                    boss_it = random.randint(0, boss_cnt)
                    enemy_storage["boss"][boss_it][0].set_status("Dive")
                    enemy_storage["boss"][boss_it][1].sfx1.play()

                    diveTime = pygame.time.get_ticks()
                except IndexError:
                    print("Error with boss diving", boss_it, "\n")

    # The code below checks for collisions between enemies and the player's missile
    for missile_it in player.missiles:
        if missile_it.y > 0:
            missile_it.y -= missile_it.speed
            for enemy_1 in enemy_storage["boss"]:
                if is_collision(enemy_1[0], missile_it) and not enemy_1[0].isDead:
                    if enemy_1[0].health == 1:
                        score += 150
                        boss_cnt -= 1
                        enemy_1[1].sfx2.play()
                        enemy_1[1].sfx1.stop()
                        enemy_1[0].isDead = True
                        player.missiles.pop(player.missiles.index(missile_it))

                        x_cor = enemy_1[0].x
                        y_cor = enemy_1[0].y

                        enemy_storage["explosion"].append(Explosion(enemy_1[0]))
                        enemy_storage["boss"].pop(enemy_storage["boss"].index(enemy_1))
                        break
                    else:
                        enemy_1[0].health -= 1
                        enemy_1[1].sfx3.play()
                        player.missiles.pop(player.missiles.index(missile_it))

                        enemy_1[0].iter += 2
                        win.blit(boss_galaga[enemy_1[0].iter], (int(enemy_1[0].x), int(enemy_1[0].y)))
                        break

            for enemy_1 in enemy_storage["butterfly"]:
                if is_collision(enemy_1[0], missile_it) and not enemy_1[0].isDead:
                    score += 80
                    butterfly_cnt -= 1
                    enemy_1[1].sfx2.play()
                    enemy_1[1].sfx1.stop()
                    enemy_1[0].isDead = True
                    player.missiles.pop(player.missiles.index(missile_it))

                    x_cor = enemy_1[0].x
                    y_cor = enemy_1[0].y

                    enemy_storage["explosion"].append(Explosion(enemy_1[0]))
                    enemy_storage["butterfly"].pop(enemy_storage["butterfly"].index(enemy_1))
                    break

            for enemy_1 in enemy_storage["bee"]:
                if is_collision(enemy_1[0], missile_it) and not enemy_1[0].isDead:
                    score += 50
                    bee_cnt -= 1
                    enemy_1[1].sfx2.play()
                    enemy_1[1].sfx2.stop()
                    enemy_1[0].isDead = True
                    player.missiles.pop(player.missiles.index(missile_it))

                    x_cor = enemy_1[0].x
                    y_cor = enemy_1[0].y

                    enemy_storage["explosion"].append(Explosion(enemy_1[0]))
                    enemy_storage["bee"].pop(enemy_storage["bee"].index(enemy_1))
                    break
        else:
            player.missiles.pop(player.missiles.index(missile_it))

    # Allows the player to control the gunship and fire missiles
    if keys[pygame.K_LEFT] and player.x - player.speed > 0:
        player.x -= player.speed

    if keys[pygame.K_RIGHT] and player.x + player.speed < 470:
        player.x += player.speed

    if keys[pygame.K_SPACE]:
        player.fire_missile()

    redrawGameWindow()

pygame.quit()