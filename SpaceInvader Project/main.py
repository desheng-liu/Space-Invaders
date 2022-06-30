import pygame
import random
import math
from pygame import mixer #sound from pygame


#initalize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#create the background
background = pygame.image.load(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\background.png')
#sound of the background
mixer.music.load(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\background.wav')
pygame.mixer.music.set_volume(.2)
mixer.music.play(-1) #make sure music is playing forever


# Title and Icon
pygame.display.set_caption("Space Invaders >:)")
icon = pygame.image.load(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\spaceship.png')
pygame.display.set_icon(icon)



# player
playerimage = pygame.image.load(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\player.png')
playerX = 350
playerY = 480
playerX_change = 0

# enemies
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimage.append(pygame.image.load(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\monster.png'))
    enemyX.append(random.randint(0,760))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# ready - not visible
# fire - moving/visible

#bullet
bulletimage = pygame.image.load(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\bullet.png')
bulletX = 0
bulletY= 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 22)
#text position of score
textX = 10
textY = 10

#shoot the enemies text
shoot_font = pygame.font.Font('freesansbold.ttf', 22)

#game over text
gameover_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x , y ):
    score = font.render("Score :" + " " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def funshoot_text():
    shoottext = shoot_font.render("Shoot the enemies!", True, (255, 255, 255))
    screen.blit(shoottext,(300,50))

def game_over_text():
    overtext = gameover_font.render("GAME OVER!", True, (255,255,255))
    screen.blit(overtext,(200, 250))

def player(x,y):
    screen.blit(playerimage, (x, y))

def enemy(x,y,i):
    screen.blit(enemyimage[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage, (x + 16,y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY): #uses distance formula
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:

    #RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    #background needs to be after
    screen.blit(background, (0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # keyboard movements (left and right)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\laser.wav')
                    bullet_Sound.set_volume(.2)
                    bullet_Sound.play()
                #makes sure the bullet stays in same position in velocity
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key  == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    #boundaries for player
    if playerX <=0:
        playerX = 0
    elif playerX>=768:
        playerX = 768

#enemy repeat

    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000

            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        #boundaries for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

    # collision bool statements
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            explosion_Sound = mixer.Sound(r'C:\Users\Desheng Liu\Desktop\SpaceInvader Project\explosion.wav')
            explosion_Sound.set_volume(.3)
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            #respawn
            enemyX[i] = random.randint(0,760)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)


    #bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    funshoot_text()
    pygame.display.update()
