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

    display_explosion_fx()

    pygame.display.update()

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
                    enemy_storage["boss"][random.randint(0, boss_cnt)].set_status("Dive")
                    firstDive_1 = False
                    prevTime = pygame.time.get_ticks()
                    print("prevTime updated to", prevTime)
                else:
                    try:
                        print("2nd enemy starts flying\n")
                        enemy_storage["bee"][random.randint(0, bee_cnt)].set_status("Dive")
                        firstDive_2 = False
                        diveTime = pygame.time.get_ticks()
                    except:
                        print("Error with bee diving\n")
    else:
        if (pygame.time.get_ticks() - diveTime) > 3000:
            if (random.randint(0, 3)) > 0:
                try:
                    enemy_storage["bee"][random.randint(0, bee_cnt)].set_status("Dive")
                    diveTime = pygame.time.get_ticks()
                except:
                    print("Error with bee diving\n")
            else: # Seems like if you kill the enemy at a certain time mid-flight, the game crashes...
                try:
                    bee_iter = random.randint(0, boss_cnt)
                    enemy_storage["boss"][bee_iter].set_status("Dive")
                    diveTime = pygame.time.get_ticks()
                except:
                    print("Error with boss diving", bee_iter, "\n")


    for missile_it in player.missiles:
        if missile_it.y > 0:
            missile_it.y -= missile_it.speed

            for enemy_1 in enemy_storage["boss"]:
                if is_collision(enemy_1, missile_it) and not enemy_1.isDead:
                    if enemy_1.health == 1:
                        score += 150 # Later on, check to see the position/action of the enemy
                        boss_cnt -= 1
                        enemy_1.isDead = True
                        player.missiles.pop(player.missiles.index(missile_it))

                        x_cor = enemy_1.x
                        y_cor = enemy_1.y

                        enemy_storage["explosion"].append(Explosion(enemy_1))
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
                if is_collision(enemy_1, missile_it) and not enemy_1.isDead:
                    score += 80 # Later on, check to see the position/action of the enemy
                    butterfly_cnt -= 1
                    print("Current butterfly count:", butterfly_cnt)
                    enemy_1.isDead = True
                    player.missiles.pop(player.missiles.index(missile_it))

                    x_cor = enemy_1.x
                    y_cor = enemy_1.y

                    enemy_storage["explosion"].append(Explosion(enemy_1))
                    enemy_storage["butterfly"].pop(enemy_storage["butterfly"].index(enemy_1))

                    print("Collision detected")
                    break

            for enemy_1 in enemy_storage["bee"]:
                if is_collision(enemy_1, missile_it) and not enemy_1.isDead:
                    score += 50 # Later on, check to see the position/action of the enemy
                    bee_cnt -= 1
                    print("Current bee count:", bee_cnt)
                    enemy_1.isDead = True
                    player.missiles.pop(player.missiles.index(missile_it))

                    x_cor = enemy_1.x
                    y_cor = enemy_1.y

                    enemy_storage["explosion"].append(Explosion(enemy_1))
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