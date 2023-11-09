import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
mixer.music.load('Whats up danger.mp3')
mixer.music.play(-1)

# Create the screen
screen = pygame.display.set_mode((1000, 562))
# Background
background = pygame.image.load('galaxy.jpeg')
# Title and icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 475
playerY = 394
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 900))
    enemyY.append(random.randint(10, 110))
    enemyX_change.append(0.8)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 394
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('Sacred Hertz.otf', 40)
textX = 10
textY = 10
over_font = pygame.font.Font('Sacred Hertz.otf', 100)


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 35, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_Sound = mixer.Sound('laser_sms-[AudioTrimmer.com].mp3')
                bullet_Sound.play()
                bulletX = playerX
                fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 900:
        playerX = 900

    for i in range(num_of_enemies):
        if enemyY[i] > 370:
            for j in range(num_of_enemies):
                enemyY[j] = 5000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 900:
            enemyX_change[i] = -1.1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('M4 Shots-[AudioTrimmer.com].mp3')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 900)
            enemyY[i] = random.randint(10, 110)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 394
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    clock.tick(300)
