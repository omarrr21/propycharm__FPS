
import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('prueba')
WINDOWS_SIZE = (1240, 700)
screen = pygame.display.set_mode(WINDOWS_SIZE)
#cargando imagenes
player_image = pygame.image.load('knight.png')
dirt_image = pygame.image.load('grass.png')
grass_image = pygame.image.load('dirt.png')
TILE_SIZE = grass_image.get_width()
x1 = 0
x2 = 0
x3 = 0
x4 = 0
#x5 = 0
y1 = 0
y2 = 0
y3 = 0
y4 = 0
#y5 = 0
bkgd1 = pygame.image.load('fondo/1.png').convert()
bkgd1.set_colorkey((0,0,0))
bkgd2 = pygame.image.load('fondo/2.png').convert()
bkgd2.set_colorkey((0,0,0))
bkgd3 = pygame.image.load('fondo/3.png').convert()
bkgd3.set_colorkey((0,0,0))
bkgd4 = pygame.image.load('fondo/4.png').convert()
bkgd4.set_colorkey((0,0,0))
bkgd5 = pygame.image.load('fondo/5.png').convert()
bkgd5.set_colorkey((0,0,0))
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


#eventos causados por las flechas
moving_right = False
moving_left = False


player_y_momentum = 0
air_timer = 0
true_scroll = [0, 0]
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

player_rect = pygame.Rect(100, 100, player_image.get_width(), player_image.get_height()-28)
test_rect = pygame.Rect(300,300,300,50)


# fondo utilizado
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
#final fondo
while True:
    screen.fill((146,244,255))

    true_scroll[0] += (player_rect.x - true_scroll[0] - 684) / 20  #684 = 1240/2  +  128/2
    true_scroll[1] += (player_rect.y - true_scroll[1] - 414) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #fondo---------------------------------------------------
    rel_x1 = x1 % bkgd5.get_rect().width
    x1 -= (player_rect.x*0.5 + x1) / 20
    screen.blit(bkgd5, (rel_x1 - bkgd5.get_rect().width, int(-scroll[1]*0.05)))
    if rel_x1 < WINDOWS_SIZE[0]:
        screen.blit(bkgd5, (rel_x1, int(-scroll[1]*0.05)))

    rel_x2 = x2 % bkgd4.get_rect().width
    x2 -= (player_rect.x*0.7 + x2)/20
    screen.blit(bkgd4, (rel_x2 - bkgd4.get_rect().width, int(-scroll[1]*0.07)))
    if rel_x2 < WINDOWS_SIZE[0]:
        screen.blit(bkgd4, (rel_x2, int(-scroll[1]*0.07)))

    rel_x3 = x3 % bkgd3.get_rect().width
    x3 -= (player_rect.x*0.8 + x3) / 20
    screen.blit(bkgd3, (rel_x3 - bkgd3.get_rect().width, int(-scroll[1]*0.08)))
    if rel_x3 < WINDOWS_SIZE[0]:
        screen.blit(bkgd3, (rel_x3, int(-scroll[1]*0.08)))

    rel_x4 = x4 % bkgd2.get_rect().width
    x4 -= (player_rect.x*0.9 + x4)/ 20
    screen.blit(bkgd2, (rel_x4 - bkgd2.get_rect().width, int(-scroll[1]*0.09)))
    if rel_x4 < WINDOWS_SIZE[0]:
        screen.blit(bkgd2, (rel_x4, int(-scroll[1]*0.09)))

    #rel_x5 = x5 % bkgd1.get_rect().width
    #x5 -= (player_rect.x + x5) / 20
    #screen.blit(bkgd1, (rel_x5 - bkgd1.get_rect().width, int(-scroll[1]*0.1)))
    #if rel_x5 < WINDOWS_SIZE[0]:
        #screen.blit(bkgd1, (rel_x5, int(-scroll[1]*0.1)))

    #fondo---------------------------------------------------
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                screen.blit(dirt_image, (x * 50 - scroll[0], y * 50 - scroll[1]))
            if tile == '2':
                screen.blit(grass_image, (x * 50 - scroll[0], y * 50 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 50, y * 50, 50, 50))
            x += 1
        y += 1
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        player_y_momentum = 0
    else:
        air_timer += 1

    screen.blit(player_image, (player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 30:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps