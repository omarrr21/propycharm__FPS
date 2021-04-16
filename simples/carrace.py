import pygame
import random
import time

pygame.init()
display_width = 600
display_height = 800
gameDisplay = pygame.display.set_mode((display_width,display_height))

clock = pygame.time.Clock()

carImg = pygame.image.load('badguy2.png')
# main characters of game


def enemy(x, y, w, h, color):
    pygame.draw.ellipse(gameDisplay, color, [x, y, w, h])


def renderCar(x, y):
    gameDisplay.blit(carImg, (x, 410))


green = (0, 128, 0)



def game_loop():
    x = (display_width * 0.45)
    y = (display_height*0.8)
    x_change = 0
    enemy_x = random.randrange(0, display_width)
    enemy_y = 0
    enemy_speed = 4
    enemy_width = 50
    enemy_height = 50
    score = 0

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5

                if event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0

        x += x_change
        gameDisplay.fill((255, 255, 255))
        enemy(enemy_x, enemy_y, enemy_width, enemy_height, green)
        enemy_y += enemy_speed
        renderCar(x, y)

        if x > display_width - 20 or x < 0:
            print('crashed')
            time.sleep(3)
            game_loop()

        if enemy_y > display_height:
            enemy_y = 0 - enemy_height
            enemy_x = random.randrange(0, display_width)
            score += 1
            enemy_speed += 0.1


        if y < enemy_y + enemy_height:
          #  print('crossover')
            if x > enemy_x and x < enemy_x + enemy_width or x + 20 > enemy_x and x + 20 < enemy_x + enemy_width:
             #   print('collision')
                time.sleep(3)
                game_loop()



        pygame.display.flip()
        clock.tick(60)


game_loop()
pygame.quit()
quit()