import pygame
import button


pygame.init()
clock = pygame.time.Clock()
FPS = 60
#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level editor')

#define game variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

TILE_TYPES = 21
current_tile = 0

# load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load('img/tile/{}.png'.format(x))
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


#define colors
GREEN = (144, 201, 120)
WHITE = (255,255,255)
RED = (200, 25, 25)


#empty tile list
world_data = []

for row in range(ROWS):
    r = [-1]*MAX_COLS
    world_data.append(r)


# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS-1][tile] = 0




#create funcion for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):

        screen.blit(sky_img, ((x*width) -scroll*0.5,0))
        screen.blit(mountain_img, ((x*width)-scroll*0.6, SCREEN_HEIGHT-mountain_img.get_height()-300))
        screen.blit(pine1_img, ((x*width)-scroll*0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x*width)-scroll*0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#draw grid
def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE- scroll, SCREEN_HEIGHT))
    #HORIZONTAL LINES
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))
# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >=0:
                screen.blit(img_list[tile],(x*TILE_SIZE - scroll,y * TILE_SIZE) )


#create buttons
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75* button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0




run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    #draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    #highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)




    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5
    if scroll_right == True:
        scroll += 5

    #add new tiiles to the screen
    #get mouse posiition
    pos = pygame.mouse.get_pos()
    x = (pos[0]+scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    #check coordinates are within the area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False



    pygame.display.update()
pygame.quit()