import pygame

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
CHUNK_SIZE = 7
def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0

            if 0 <= target_y < 14 and 0<= target_x < 121:
                if int(game_map[target_y][target_x]) != 0:
                    tile_type = int(game_map[target_y][target_x])
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data








