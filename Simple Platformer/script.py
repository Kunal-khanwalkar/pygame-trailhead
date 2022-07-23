import pygame,sys
from pygame.locals import *

WINDOW_SIZE = (600,400)
DISPLAY_SIZE = (300,200)
BG_COLOR = (146,244,255)


class Player:
    def __init__(self):
        self.player_image = pygame.image.load('images/player.png')
        self.player_image.set_colorkey((255,255,255))

        self.moving_left = False
        self.moving_right = False
        self.player_y_momentum = 0
        self.air_timer = 0
        self.player_rect = pygame.Rect(50,50,self.player_image.get_width(),self.player_image.get_height())
    
    def display(self,disp):
        disp.blit(self.player_image,(self.player_rect.x,self.player_rect.y))

    def getCollisionTiles(self, tileMap):
        hit_list = []
        for tile in tileMap:
            if self.player_rect.colliderect(tile):
                hit_list.append(tile)

        return hit_list
    
    def move(self, tileMap):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.player_y_momentum += 0.2
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3
        self.player_rect.y += self.player_y_momentum

        hit_list = self.getCollisionTiles(tileMap)
        for tile in hit_list:
            if self.player_y_momentum > 0:
                self.player_rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.player_y_momentum < 0:
                self.player_rect.top = tile.bottom
                collision_types['top'] = True

        if self.moving_right == True:
            self.player_rect.x += 2
        if self.moving_left == True:
            self.player_rect.x -= 2
        
        hit_list = self.getCollisionTiles(tileMap)
        for tile in hit_list:
            if self.moving_right == True:
                self.player_rect.right = tile.left
                collision_types['right'] = True
            elif self.moving_left == True:
                self.player_rect.left = tile.right
                collision_types['left'] = True

        if collision_types['bottom']:
            self.player_y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

        if collision_types['top']:
            self.player_y_momentum = 0

def get_keyboard_input(player):
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_LEFT:
                player.moving_left = True    
            if event.key == K_UP:
                if player.air_timer < 6:
                    player.player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False


def generate_tileMap(display):
    grass_image = pygame.image.load('images/grass.png')
    dirt_image = pygame.image.load('images/dirt.png')
    TILE_SIZE = grass_image.get_width()

    game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
                ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

    tileMap = []
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if game_map[i][j] == '1':
                display.blit(dirt_image,(j*TILE_SIZE,i*TILE_SIZE))
            if game_map[i][j] == '2':
                display.blit(grass_image,(j*TILE_SIZE,i*TILE_SIZE))
            if game_map[i][j] != '0':
                tileMap.append(pygame.Rect(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE))
    return tileMap


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('My first game')
    screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
    display = pygame.Surface(DISPLAY_SIZE)

    player = Player()

    while True:
        display.fill(BG_COLOR)

        tileMap = generate_tileMap(display)
        player.display(display)

        get_keyboard_input(player)
        player.move(tileMap)
        #check_collisions(player,player_movement,tileMap)
        
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

if __name__=='__main__':
    main()
