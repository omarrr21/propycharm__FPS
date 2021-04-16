import pygame
from pygame.locals import *
import sys







# superficies

WIdth = 1240
HEight = 700

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIdth, HEight))
pygame.display.set_caption('pantalla deslizante')
FPS = 60

scroll_left = False
scroll_right = False
scroll_up = False
scroll = 0
scroll_speed = 1

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



dirt = pygame.image.load('grass.png')
grass = pygame.image.load('dirt.png')
tile_index = {1:dirt, 2:grass}
x1= 0
x2=0
x3=0
x4=0
x5=0
y1 = 0
y2 = 0
y3 = 0
y4 = 0
y5 = 0
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#movimiento
player_location = [50, 50]
player_y_momentum = 0
#movimiento
# #imagen del personaje
player_image = pygame.image.load('knight.png')
map_screen = {}
#rec del jugador
player_rect = pygame.Rect(50, 50, player_image.get_width(),player_image.get_height())



def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def draw_bg():
    screen.fill(WHITE)
    for i in range(4):
        screen.blit(bkgd5, ((i * bkgd4.get_rect().width) -scroll*0.5, -100))
        screen.blit(bkgd4, ((i * bkgd4.get_rect().width) -scroll*0.7, -100))
        screen.blit(bkgd3, ((i * bkgd4.get_rect().width) -scroll*0.8, -100))
        screen.blit(bkgd2, ((i * bkgd4.get_rect().width) -scroll*0.9, -100))
        screen.blit(bkgd1, ((i * bkgd4.get_rect().width) -scroll, -100))

        #inicio funciones para generar mundo por tramos
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    datos =data.split('\n')
    game_map = []
    for row in datos:
        game_map.append(list(row))
    return game_map
# gm_map = {}
gm_map = load_map('map')

CHUNK_SIZE = 7

def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            if target_y < 0:
                tile_type = 1
            if int(gm_map[target_y][target_x]) != 0:
                tile_type = int(gm_map[target_y][target_x])
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

# para trabajar chunks en Y negativo hay q restar en target_y para obtener el tile


true_scroll = [0,0]

# final funciones para generar mundo por tramos
while True:
    #movimiento del personaje

    if player_y_momentum > 3:
        player_y_momentum = 3
    true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])




    player_movement = [0, 0]
    if scroll_right == True:
        player_movement[0] += 2
    if scroll_left == True:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2




    # inicio fondo dinamico
    rel_x1 = x1 % bkgd5.get_rect().width

    screen.blit(bkgd5, (rel_x1 - bkgd5.get_rect().width,0))
    if rel_x1 < WIdth:
        screen.blit(bkgd5, (rel_x1, 0))
    if scroll_right == True:
        x1 -= 0.5
    if scroll_left == True:
        x1 += 0.5
    if scroll_up == True:
        y1 += 0.5

    rel_x2 = x2 % bkgd4.get_rect().width

    screen.blit(bkgd4, (rel_x2 - bkgd4.get_rect().width, 0))
    if rel_x2 < WIdth:
        screen.blit(bkgd4, (rel_x2, 0))
    if scroll_right == True:
        x2 -= 0.7
    if scroll_left == True:
        x2 += 0.7
    if scroll_up == True:
        y2 += 0.7

    rel_x3 = x3 % bkgd3.get_rect().width

    screen.blit(bkgd3, (rel_x3 - bkgd3.get_rect().width, 0))
    if rel_x3 < WIdth:
        screen.blit(bkgd3, (rel_x3, 0))
    if scroll_right == True:
        x3 -= 0.8
    if scroll_left == True:
        x3 += 0.8
    if scroll_up == True:
        y3 += 0.8

    rel_x4 = x4 % bkgd2.get_rect().width

    screen.blit(bkgd2, (rel_x4 - bkgd2.get_rect().width, 0))
    if rel_x4 < WIdth:
        screen.blit(bkgd2, (rel_x4, 0))
    if scroll_right == True:
        x4 -= 0.9
    if scroll_left == True:
        x4 += 0.9
    if scroll_up == True:
        y4 += 0.9

    rel_x5 = x5 % bkgd1.get_rect().width

    screen.blit(bkgd1, (rel_x5 - bkgd1.get_rect().width, 0))
    if rel_x5 < WIdth:
        screen.blit(bkgd1, (rel_x5, 0))
    if scroll_right == True:
        x5 -= 1
    if scroll_left == True:
        x5 += 1
    if scroll_up == True:
        y5 += 1
    # final fondo dinamico
   #inicio generar mundo por tramos
    tile_rects = []
    for y in range(4):
        for x in range(5):
            target_x = x - 1 + int(round(-x5 / (CHUNK_SIZE * 50)))
            target_y = y - 1 + int(round(-y5/(CHUNK_SIZE*50)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in map_screen:
                map_screen[target_chunk] = generate_chunk(target_x, target_y)
            for tile in map_screen[target_chunk]:
                screen.blit(tile_index[tile[1]],(tile[0][0]*50+x5,tile[0][1]*50+y5))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0] * 50, tile[0][1] * 50, 50, 50))
            #final generar mundo por tramos

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom'] == True:
        #air_timer = 0
        vertical_momentum = 0
    #scrool the map

    screen.blit(player_image, (player_rect.x-x5, player_rect.y))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                scroll_right = True
            if event.key == K_LEFT:
                scroll_left = True
            if event.key == K_UP:
                scroll_up = True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                scroll_right = False
            if event.key == K_LEFT:
                scroll_left = False
            if event.key == K_UP:
                scroll_up = False


    pygame.display.update()
    clock.tick(FPS)
