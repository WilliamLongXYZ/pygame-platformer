import pygame
from pygame.locals import *
import sys


pygame.init()

pygame.display.set_caption('Pygame Window')
clock = pygame.time.Clock()
WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))



grass_image = pygame.image.load('images/tiles/grass.png').convert()
dirt_image = pygame.image.load('images/tiles/dirt.png').convert()
TILE_SIZE = grass_image.get_width()

target_fps = 60

true_scroll = [0,0]

def load_map(path):
    with open(path+'.txt','r') as f:
        data = f.read().split('\n')
    game_map = [list(row) for row in data]
    return game_map

animation_frames = {}

def load_animation(path, frame_durations):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    i = 0
    for frames in frame_durations:
        animation_frame_id = animation_name+str(i)
        image_location = path+'/'+animation_frame_id+'.png'
        animation_image = pygame.image.load(image_location)
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for j in range(frames):
            animation_frame_data.append(animation_frame_id)
        i+=1
    return animation_frame_data

def change_action(current_action,frame,new):
    if current_action != new:
        current_action = new
        frame = 0
    return current_action, frame

animation_database = {}
animation_database['run'] = load_animation('animations/run', [15, 15, 15, 15])
# animation_database['idle'] = load_animation('animations/idle', [])

player_animation = 'idle'
player_frame = 0
player_flip = False

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
        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_image,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '2':
                    display.blit(grass_image,(x*16-scroll[0],y*16-scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
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

        display.blit(player_image, (player_rect.x-scroll[0],player_rect.y-scroll[1]))

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
