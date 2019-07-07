import pygame
from comms import gameClient as gc

player = input("Player 1 or 2?")

pTeam = ''
pColor = (0,0,0)

x = 250
y = 250

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





while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel

    if keys[pygame.K_RIGHT]:
        x += vel

    if keys[pygame.K_UP]:
        y -= vel

    if keys[pygame.K_DOWN]:
        y += vel

    win.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(win, pColor, (x, y, width, height))
    tank = gc.getTank()

    col = (245,10,10)
    if tank['team']=='blue':
        col = (10,10,245)
        pygame.draw.rect(win, col, (tank['x'], tank['y'], width, height))
    elif tank['team']=='red':
        col = (245, 10, 10)
        pygame.draw.rect(win, col, (tank['x'], tank['y'], width, height))

    message = {'id': gc.getID(),'team': pTeam, 'x':x, 'y':y , 'bulletX':-1, 'bulletY':-1}
    if lastX!=x or lastY!=y:
        gc.send(message)
    lastX = x
    lastY = y

    pygame.display.update()

pygame.quit()