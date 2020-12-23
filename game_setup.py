import pygame

pygame.init()

# width = 3000
# height = 3000
width = 500
height = 500

win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Galaga")

# SFX used for game exported from Galaga
sfx_4 = pygame.mixer.Sound("galaga_sfx/wav/04 Alien Flying.wav")
sfx_5 = pygame.mixer.Sound("galaga_sfx/wav/05 Zako Stricken.wav")
sfx_6 = pygame.mixer.Sound("galaga_sfx/wav/06 Goei Stricken.wav")
sfx_7 = pygame.mixer.Sound("galaga_sfx/wav/07 Boss Stricken#1.wav")
sfx_8 = pygame.mixer.Sound("galaga_sfx/wav/08 Boss Stricken#2.wav")
sfx_13 = pygame.mixer.Sound("galaga_sfx/wav/13 Fighter Shot1.wav")
sfx_15 = pygame.mixer.Sound("galaga_sfx/wav/15 Fighter Shot2.wav")
sfx_22 = pygame.mixer.Sound("galaga_sfx/wav/22 Miss.wav")

# Objects below create the images for the video game.
gunship = pygame.image.load('sprites/player/gunship.gif')

pygame.display.set_icon(gunship)

missile = pygame.image.load('sprites/player/missile.gif')

# Arrays display the sprites for a specific type of enemy.
# For "boss_galaga", the 3rd and 4th element is the purple sprite for "boss_galaga"
# Explosion animation for enemy deaths
explosions = [pygame.image.load("sprites/enemy/enemy_death/exp1.png"),
              pygame.image.load("sprites/enemy/enemy_death/exp2.png"),
              pygame.image.load("sprites/enemy/enemy_death/exp3.png"),
              pygame.image.load("sprites/enemy/enemy_death/exp4.png"),
              pygame.image.load("sprites/enemy/enemy_death/exp5.png")]

player_explosions = [pygame.image.load("sprites/player/death/1.png"),
                     pygame.image.load("sprites/player/death/1.png"),
                     pygame.image.load("sprites/player/death/1.png"),
                     pygame.image.load("sprites/player/death/1.png"),

                     pygame.image.load("sprites/player/death/2.png"),
                     pygame.image.load("sprites/player/death/2.png"),
                     pygame.image.load("sprites/player/death/2.png"),
                     pygame.image.load("sprites/player/death/2.png"),

                     pygame.image.load("sprites/player/death/3.png"),
                     pygame.image.load("sprites/player/death/3.png"),
                     pygame.image.load("sprites/player/death/3.png"),
                     pygame.image.load("sprites/player/death/3.png"),

                     pygame.image.load("sprites/player/death/4.png"),
                     pygame.image.load("sprites/player/death/4.png"),
                     pygame.image.load("sprites/player/death/4.png"),
                     pygame.image.load("sprites/player/death/4.png")]

# Resizing the sprites for the game to the appropriate size

diving_enemies = []

# Array of the different sprites for an explosion
explosions[0] = pygame.transform.scale(explosions[0], (30, 30))
explosions[1] = pygame.transform.scale(explosions[1], (30, 30))
explosions[2] = pygame.transform.scale(explosions[2], (30, 30))
explosions[3] = pygame.transform.scale(explosions[3], (30, 30))
explosions[4] = pygame.transform.scale(explosions[4], (30, 30))

player_explosions[0] = pygame.transform.scale(player_explosions[0], (35, 35))
player_explosions[1] = pygame.transform.scale(player_explosions[1], (35, 35))
player_explosions[2] = pygame.transform.scale(player_explosions[2], (35, 35))
player_explosions[3] = pygame.transform.scale(player_explosions[3], (35, 35))

player_explosions[4] = pygame.transform.scale(player_explosions[4], (35, 35))
player_explosions[5] = pygame.transform.scale(player_explosions[5], (35, 35))
player_explosions[6] = pygame.transform.scale(player_explosions[6], (35, 35))
player_explosions[7] = pygame.transform.scale(player_explosions[7], (35, 35))

player_explosions[8] = pygame.transform.scale(player_explosions[8], (35, 35))
player_explosions[9] = pygame.transform.scale(player_explosions[9], (35, 35))
player_explosions[10] = pygame.transform.scale(player_explosions[10], (35, 35))
player_explosions[11] = pygame.transform.scale(player_explosions[11], (35, 35))

player_explosions[12] = pygame.transform.scale(player_explosions[12], (35, 35))
player_explosions[13] = pygame.transform.scale(player_explosions[13], (35, 35))
player_explosions[14] = pygame.transform.scale(player_explosions[14], (35, 35))
player_explosions[15] = pygame.transform.scale(player_explosions[15], (35, 35))


# Where all the enemies are stored
enemy_storage = {"boss": [], "butterfly": [], "bee": [], "explosion": [], "player_explosion": []}
enemy_names = ["boss", "butterfly", "bee"]

# Array storing the pixels that resemble stars
stars = []

clock = pygame.time.Clock()
score = 0

x = 250
y = 400
vel = 4.5

boss_cnt = -1
butterfly_cnt = -1
bee_cnt = -1