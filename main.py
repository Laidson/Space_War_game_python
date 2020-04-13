import pygame
import random
import math
from pygame import  mixer

# Inicialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Music
mixer.music.load('Cake_Never_There.mp3')
mixer.music.play(-1)

# Window Title
pygame.display.set_caption("Space War")
icon_head = pygame.image.load('rocket.png')#32px
pygame.display.set_icon(icon_head)

# Player
playerImg = pygame.image.load("spaceship.png")#64px
playerX = 370
playerY = 500

playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("invaders.png"))#64px
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(15, 150))

    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")#32px
bulletX = 0
bulletY = 480

bulletX_change = 0
bulletY_change = 15
bullet_state = "ready" #you can't see the bullet on the screen/fire is currently moving

# Score
score_value = 0
font = pygame.font.Font('Inconsolata-Bold.ttf', 20)
textX = 10
textY = 10

#Game Over text

over_front = pygame.font.Font('Inconsolata-Bold.ttf', 60)



def show_score(x, y):
    score = font.render("Score " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_front.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_text, (250, 190))

def player(x, y):
    screen.blit(playerImg, (x, y))#drawing an imagi on the screen

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y + 10)) # center of spaceship

def isColision(enemyX,enemyY, bulletX, bulletY): #https://www.mathplanet.com/education/algebra-2/conic-sections/distance-between-two-points-and-the-midpoint
    distence = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distence < 27:
        return True
    else:
        return False

#Game loop
running = True
while running:
    # RGB background set
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking if a keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -7
            if event.key == pygame.K_DOWN:
                playerY_change = 7
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_sound.set_volume(0.3)
                    bulletY = playerY
                    bulletX = playerX # Save the playerX(spaceship) value when press SPACE
                    fire_bullet(bulletX, bulletY)#Attentio the Y value should be the bullet!!!

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
              playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
              playerY_change = 0

    # Spaceship movements limit
    playerX += playerX_change
    if playerX <= 0:
        playerX = 736 #if want stop on the wall playerX = 0
    elif playerX >= 736:
        playerX = 0 # if want stop on the wall playerX = 736

    playerY += playerY_change
    if playerY <= 0:
        playerY = 536
    elif playerY >= 536:
        playerY = 0

    # Enemy movements limit / The [i] specify the enemy on the list
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isColision(enemyX[i],enemyY[i], bulletX, bulletY)
        if collision:
            colision_sound = mixer.Sound("explosion.wav")
            colision_sound.play()
            colision_sound.set_volume(0.3)
            colision_sound.fadeout(900)
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(10, 150)

        enemy(enemyX[i], enemyY[i], i)


    # Bullet moviment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
