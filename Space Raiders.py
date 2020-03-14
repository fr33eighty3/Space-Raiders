# IMPORT AND INITIALIZE #

import pygame
import random
import math
from pygame import mixer

pygame.init()

# SET COLOURS #

WHITE = ( 255, 255, 255)
DARKBLUE = (15,44,119)
LIGHTBLUE = (65,166,227)
TEAL = (23,128,163)
TURQUOISE = (67,239,242)
PURPLE = (116,28,214)
GREY = (102,136,136)

# SET SCREEN SIZE #

screen = pygame.display.set_mode((800,600))

# BACKGROUND #

background = pygame.image.load('outer-space1.png')

mixer.music.load('vintage-elecro.wav')
mixer.music.play(-1)


# SET SCREEN CAPTION / IMAGE #

pygame.display.set_caption("Spaced Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)



# PLAYER #

playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480

playerX_change = 0

# ALIEN #

alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 15

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0,735))
    alienY.append(random.randint(50,100))

    alienX_change.append(5)
    alienY_change.append(40)

# BULLET #

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"


# SCORE #

score_value  = 0
font = pygame.font.Font('retro.ttf',25)
textX = 10
textY = 10

# GAME OVER 

over_font = pygame.font.Font('retro.ttf',50)

def game_over_text():
    over_text  = over_font.render("HA HA HA HA HA !!!", True,(LIGHTBLUE))
    screen.blit(over_text,(110,250))

def show_score(x,y):
    score = font.render("NEUTRALIZED : " + str(score_value), True, (LIGHTBLUE))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg, (x,y))

def alien(x,y,i):
    screen.blit(alienImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 34, y - 20))

def isCollission(alienX,alienY,bulletX,bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX,2)) + (math.pow(alienY - bulletY,2,) )
    if distance <30:
        return True
    else: 
        return False

# GAME LOOP #

running = True
while running:

# FILL BACKGROUND BEFORE IMAGES #

    screen.fill(TEAL)
    screen.blit(background,(0,0))

    
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            running = False

# IF KEYSTROKE IS PRESSED, CHECK IF 'LEFT' OR 'RIGHT' #

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                    playerX_change -= 10
            if event.key == pygame.K_RIGHT:
                    playerX_change += 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY) 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # OPERATOR #

    # PLAYER MOVEMENT #

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    if playerX >= 736:
        playerX = 736

    # ALIEN MOVEMENT #

    for i in range(num_of_aliens):

    # GAME OVER TEXT #

        if alienY[i] > 500:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 6
            alienY[i] += alienY_change[i] 
        elif alienX[i] >= 736:
            alienX_change[i] = -6
            alienY[i] += alienY_change[i]

        

    # Collision #

        collision = isCollission(alienX[i],alienY[i],bulletX,bulletY)
        if collision:
            blast_Sound = mixer.Sound('blast.wav')
            blast_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            alienX[i] = random.randint(0,735)
            alienY[i] = random.randint (150,250)

        alien(alienX[i],alienY[i],i)  


    # BULLET MOVEMENT #

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


     
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()