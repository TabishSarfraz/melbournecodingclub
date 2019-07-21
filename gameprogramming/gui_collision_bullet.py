import pygame
from comms import gameClient as gc
import sys

player = input("Player 1 or 2?")

pTeam = ''
pColor = (0,0,0)

x = 250
y = 250

bx = -1
by = -1

enemyBulletCreated = 0
enemyBullet = 0
playerBulletCreated = 0

if int(player) == 1:
    pTeam = 'red'
    pColor = (245, 10, 10)
    x = 240
    y = 400
else:
    pTeam = 'blue'
    pColor = (10, 10, 245)
    x = 240
    y = 0
#https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement/
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Tank Battle: Team " + pTeam)


width = 40
height = 60
vel = 5

run = True

gc.makeConnection()

lastX = x
lastY = y

all_sprites = pygame.sprite.Group()
all_sprites_enemy = pygame.sprite.Group()
all_sprites_player = pygame.sprite.Group()
all_sprites_bullet = pygame.sprite.Group()
all_sprites_bullet_enemy = pygame.sprite.Group()

bulletImage = pygame.image.load('laserRed.png').convert()
background = pygame.image.load("terrain1.jpg")

win_rect = win.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (500/2, 500/2)
    
    def update(self,x,y):
        self.rect.y = y
        self.rect.x = x


class EnemyPlayer(pygame.sprite.Sprite):
    def __init__(self, width, height, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (500/2, 500/2)
        self.enemyFound = 1
    
    def update(self,x1,y1, color, width, height):

        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1



    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bulletImage, x,y):
        super().__init__()
        self.image = pygame.transform.scale(bulletImage, (70, 70))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        global  playerBulletCreated 
        playerBulletCreated = 1

        self.rect.centerx = x
        self.rect.y = y
        if pTeam == 'red':
            self.speedy = -15
        elif pTeam =='blue':
            self.speedy = +15


        global bx
        bx = self.rect.centerx
        global by
        by = self.rect.y
    
    def update(self):
        self.rect.y += self.speedy
        global by
        by = self.rect.y

        if self.rect.y < 0 or self.rect.y > 500:
            self.kill()
            bx = -1
            by = -1
            global  playerBulletCreated 
            playerBulletCreated = 0
            
            #Tells second user via server bullet destroyed 
            message = {'id': gc.getID(),'team': pTeam, 'x':x, 'y':y , 'bulletX':bx, 'bulletY':by, 'bulletExist': enemyBulletCreated}
            gc.send(message)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, bulletImage, x,y):
        super().__init__()
        self.image = pygame.transform.scale(bulletImage, (70, 70))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.y = y


        if pTeam == 'red':
            self.speedy = +15
        elif pTeam =='blue':
            self.speedy = -15
    
    def update(self):
        self.rect.y += self.speedy

        if self.rect.y < 0 or self.rect.y > 500:
            global enemyBulletCreated
            enemyBulletCreated = 0
            self.kill()
            bx = -1
            by = -1


def shoot():
        
        nowTime = pygame.time.get_ticks()
        
        if playerBulletCreated !=1: 

            bullet  = Bullet(bulletImage, player.rect.centerx, player.rect.top)
            all_sprites_bullet.add(bullet)
            all_sprites.add(bullet)

def enemyShoot():
        nowTime = pygame.time.get_ticks()
        global enemyBulletCreated
        global enemyBullet

        if enemyBulletCreated != 0:
            print("enemyBullet created")
        else:

            enemyBullet = EnemyBullet(bulletImage, enemy.rect.centerx, enemy.rect.top)

            enemyBulletCreated = 1
            all_sprites_bullet_enemy.add(enemyBullet)
            all_sprites.add(enemyBullet)
            message = {'id': gc.getID(),'team': pTeam, 'x':x, 'y':y , 'bulletX':bx, 'bulletY':by, 'bulletExist': enemyBulletCreated}


player = Player(width, height, pColor, x, y)


enemy = EnemyPlayer(width, height, (1,43,34), 50, 50)

all_sprites.add(player)
all_sprites.add(enemy)
all_sprites_enemy.add(enemy)
all_sprites_player.add(player)

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
 

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel

    if keys[pygame.K_RIGHT]:
        x += vel

    if keys[pygame.K_UP]:
        y -= vel

    if keys[pygame.K_DOWN]:
        y += vel
    
    if keys[pygame.K_SPACE]:
        shoot()

 

    win.fill((0, 0, 0))  # Fills the screen with black
    win.blit(background, (0,0))

    player.update(x,y)
    tank = gc.getTank()
    
    col = (245,10,10)
    if tank['team']=='blue':
        col = (10,10,245)
        enemy.update(tank['x'],tank['y'],col, width, height)

    elif tank['team']=='red':
        col = (245, 10, 10)
        enemy.update(tank['x'],tank['y'],col, width, height)
        
    if tank['bulletX'] > 1 and tank['bulletX']  < 500 and tank['bulletY'] > 1 and tank['bulletY'] < 500 :
        enemyShoot()

    if bx >500 or bx < 0 or by > 500 or by < 0:
        bx = -1
        by = -1

        
    player_collided_by_enemy = pygame.sprite.groupcollide(all_sprites_player, all_sprites_enemy, True, True )

    player_collided_by_enemyFire = pygame.sprite.groupcollide(all_sprites_player, all_sprites_bullet_enemy, True, True )      

    enemy_collided_by_playerFire = pygame.sprite.groupcollide(all_sprites_enemy, all_sprites_bullet, True, True )    

    for hit in player_collided_by_enemy:
        print("Player collided with enemy")


    message = {'id': gc.getID(),'team': pTeam, 'x':x, 'y':y , 'bulletX':bx, 'bulletY':by, 'bulletExist': enemyBulletCreated}
    if lastX!=x or lastY!=y or by > 0 and by < 500:
        gc.send(message)
    lastX = x
    lastY = y

    player.rect.clamp_ip(win_rect)
   
    all_sprites_bullet.update()
    all_sprites_bullet_enemy.update()
    all_sprites.draw(win)
    pygame.display.update()

#pygame.quit()
sys.exit()