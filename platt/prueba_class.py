import pygame
from pygame.locals import *


global animation_frames #averiguar si es necesario declarar esto en el archivo principal
animation_frames = {}    #averiguar si es necesario declarar esto en el archivo principal
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
    return animation_frame_data    # se necesita un animation_database = {} en el archivo principal


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


class Obj_fisica(object):
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.rect = pygame.Rect(x, y, self.x_size, self.y_size)

    def set_rect_size(self, new_x, new_y):
        self.x_size = new_x
        self.y_size = new_y

    def move(self, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += movement[0]
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += movement[1]
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return collision_types



global animation_database
animation_database={}


class Soldier(object):
    global animation_database
    def __init__(self, x, y, size_x, size_y, sol_type):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.animation_frame = 0
        self.sol_type = sol_type
        self.sol_action = ''
        self.set_action('idle')
        self.flip = False
        self.obj = Obj_fisica(x, y, size_x, size_y)

    def set_flip(self, boolean):
        self.flip = boolean

    def set_action(self, action_id):
        if self.sol_action != action_id:
            self.sol_action = action_id
            self.animation_frame = 0

    def move(self, movement, tiles):
        collisions = self.obj.move(movement, tiles)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions

    def change_frame(self, screen, scroll):
        self.animation_frame += 1
        if self.animation_frame >= len(animation_database[self.sol_action]):
            self.animation_frame= 0
        player_image_id = animation_database[self.sol_action][self.animation_frame]
        player_image = animation_frames[player_image_id]

        if self.flip:
            screen.blit(pygame.transform.flip(player_image, self.flip, False),
                        (self.obj.rect.x - scroll[0] - 60, self.obj.rect.y - scroll[1] - 60))
        else:
            screen.blit(pygame.transform.flip(player_image, self.flip, False),
                        (self.obj.rect.x - scroll[0] - 20, self.obj.rect.y - scroll[1] - 60))


