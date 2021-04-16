
import pygame
import sys
from pygame.locals import *
from funcionss import *

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
tile_index = {1:dirt_image, 2:grass_image}
mapa_screen={}   # diccionario del mapa
#CHUNK_SIZE = 7


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

#game_map = load_map('map')

global animation_frames
animation_frames = {}
def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name +  str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc)

        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

animation_database = {}
animation_database['walk'] = load_animation('animations/walk',[7,7,7,7,7,7])
animation_database['idle'] = load_animation('animations/idle', [7, 7, 7, 7, 60, 7, 7, 7, 7, 7, 7, 60])
animation_database['jump'] = load_animation('animations/jump',[30,30,30,30,30,30,30])
animation_database['attack'] = load_animation('animations/attack',[7,7,7,7,7])
animation_database['walk_attack'] = load_animation('animations/walk_attack',[7,7,7,7,7,7])
animation_database['attack_extra'] = load_animation('animations/attack_extra',[7,7,7,7,7,7,7,7])

player_action = 'idle'
player_frame = 0
player_flip = False

#eventos causados por las flechas
moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0
true_scroll = [0, 0]

#player_rect = pygame.Rect(100, 100, player_image.get_width(), player_image.get_height()-20)
player_rect = pygame.Rect(100, 100, 40, 50)




mouse_tick_left = 0
mouse_tick_right = 0
# fondo utilizado
#background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
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
    for y in range(4):
        for x in range(6):
            target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 50)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 50)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in mapa_screen:
                mapa_screen[target_chunk] = generate_chunk(target_x, target_y)
            for tile in mapa_screen[target_chunk]:
                screen.blit(tile_index[tile[1]], (tile[0][0] * 50 - scroll[0], tile[0][1] * 50 - scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0] * 50, tile[0][1] * 50, 50, 50))


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

    now = pygame.time.get_ticks()
    if now - mouse_tick_left < 584:
        if player_movement[0] != 0:
            player_action, player_frame = change_action(player_action, player_frame, 'walk_attack')
        else:
            player_action, player_frame = change_action(player_action, player_frame, 'attack')
    elif now - mouse_tick_right < 934:
        player_action, player_frame = change_action(player_action, player_frame, 'attack_extra')

    else:
        if air_timer > 5:
            player_action, player_frame = change_action(player_action, player_frame, 'jump')
            if player_movement[0] > 0:
                player_flip = False
                #player_action, player_frame = change_action(player_action, player_frame, 'walk')
            if player_movement[0] < 0:
                player_flip = True
                #player_action, player_frame = change_action(player_action, player_frame, 'walk')
        else:
            if player_movement[0] == 0:
                player_action, player_frame = change_action(player_action, player_frame, 'idle')
            if player_movement[0] > 0:
                player_flip = False
                player_action, player_frame = change_action(player_action, player_frame, 'walk')
            if player_movement[0] < 0:
                player_flip = True
                player_action, player_frame = change_action(player_action, player_frame, 'walk')





    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_image_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_image_id]

    if player_flip:
        screen.blit(pygame.transform.flip(player_image, player_flip, False),
                    (player_rect.x - scroll[0]-60, player_rect.y - scroll[1]-60))
    else:
        screen.blit(pygame.transform.flip(player_image, player_flip, False),
                    (player_rect.x - scroll[0]-20, player_rect.y - scroll[1]-60))

    #screen.blit(player_image, (player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                mouse_tick_left = pygame.time.get_ticks()
            if event.button == BUTTON_RIGHT:
                mouse_tick_right = pygame.time.get_ticks()


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
    #print(player_movement,player_y_momentum,collisions['bottom'],air_timer)
    #print(event)
    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps