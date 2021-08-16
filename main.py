import pygame
from pygame.locals import *
import sys


pygame.init()

pygame.display.set_caption('Pygame Window')
clock = pygame.time.Clock()
WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))


player_image = pygame.image.load('images/sprites/player.png').convert()
player_image.set_colorkey((255, 255, 255))

grass_image = pygame.image.load('images/tiles/grass.png').convert()
dirt_image = pygame.image.load('images/tiles/dirt.png').convert()
TILE_SIZE = grass_image.get_width()

target_fps = 60

scroll = [0,0]

def load_map(path):
    with open(path+'.txt','r') as f:
        data = f.read().split('\n')
    game_map = [list(row) for row in data]
    return game_map

def collision_test(rect, tiles):
    return [tile for tile in tiles if rect.colliderect(tile)]

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



def main():

    moving_right = False
    moving_left = False

    player_y_momentum = 0
    air_timer = 0

    player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
    test_rect = pygame.Rect(100,100,100,50)

    game_map = load_map('map')
    while True:
        display.fill((146,244,255))
        scroll[0] += (player_rect.x-scroll[0]-152)/20
        scroll[1] += (player_rect.y+scroll[1]-106)/20

        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(dirt_image, (x*16+scroll[0], y*16+scroll[1]))
                if tile == '2':
                    display.blit(grass_image, (x*16+scroll[0], y*16+scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
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

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        elif collisions["top"]:
            player_y_momentum = 0
        else:
            air_timer += 1

        display.blit(player_image, (player_rect.x+scroll[0], player_rect.y+scroll[1]))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key in [K_RIGHT, K_d]:
                    moving_right = True
                if event.key in [K_LEFT, K_a]:
                    moving_left = True
                if event.key in [K_UP, K_w]:
                    if air_timer < 6:
                        player_y_momentum = -5
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == KEYUP:
                if event.key in [K_RIGHT, K_d]:
                    moving_right = False
                if event.key in [K_LEFT, K_a]:
                    moving_left = False
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(target_fps)

def main_menu():
    quit = False
    while True:
        display.fill((146,244,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit = True
            if event.type == KEYUP:
                pass
        if quit: break
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(target_fps)

if __name__ == "__main__":
    main()
