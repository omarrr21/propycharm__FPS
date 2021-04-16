import pygame
import random

# main character: wall, food, player

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, bg_color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(bg_color)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


class Player(pygame.sprite.Sprite):
    # object of player
    def __init__(self, x, y, role_image_path):
        pygame.sprite.Sprite.__init__(self)
        self.role_name = role_image_path.split('/')[-1].split('.')[0]
        self.base_image = pygame.image.load(role_image_path)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.prev_x = x
        self.prev_y = y

        self.base_speed = [30, 30]
        self.speed = [0, 0]

        self.is_move = False
        self.tracks = [[],[],[],[]]
        self.tracks_loc = [0, 0]

    def changeSpeed(self, direction):
        self.speed = [direction[0]*self.base_speed[0], direction[1]*self.base_speed[1]]
        return self.speed
    def update(self):

        """move your character"""
        if not self.is_move:
            return False
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]

    def randomDirection(self):
        return random.choice([[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]])

