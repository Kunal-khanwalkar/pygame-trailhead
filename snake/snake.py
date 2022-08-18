import pygame, sys, random
from pygame.locals import *

TILE_SIZE = 40
TILE_NO = 20

class Snake:
    def __init__(self):
        self.body = [pygame.math.Vector2(5,10), pygame.math.Vector2(6,10), pygame.math.Vector2(7,10)]
        self.direction = pygame.math.Vector2(-1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Assets/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Assets/Graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Assets/Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Assets/Graphics/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Assets/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Assets/Graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Assets/Graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Assets/Graphics/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('Assets/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Assets/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Assets/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Assets/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Assets/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Assets/Graphics/body_bl.png').convert_alpha()
    
        self.crunch_sound = pygame.mixer.Sound('Assets/Sound/crunch.wav')
    
    def draw_snake(self,screen):
        # for block in self.body:
        #     snake_block_rect = pygame.Rect(int(block.x * TILE_SIZE), int(block.y * TILE_SIZE), TILE_SIZE, TILE_SIZE)
        #     pygame.draw.rect(screen,(183,111,122),snake_block_rect)

        self.update_head_graphics()
        self.update_tail_graphics()

        for idx,block in enumerate(self.body):
            x_pos = int(block.x * TILE_SIZE)
            y_pos = int(block.y * TILE_SIZE)
            snake_block_rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

            if idx == 0:
                screen.blit(self.head, snake_block_rect)
            elif idx == len(self.body) - 1:
                screen.blit(self.tail, snake_block_rect)
            else:
                previous_block = self.body[idx+1] - block
                next_block = self.body[idx-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,snake_block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,snake_block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,snake_block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,snake_block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,snake_block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,snake_block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == pygame.math.Vector2(1,0):
            self.head = self.head_left
        if head_relation == pygame.math.Vector2(-1,0):
            self.head = self.head_right
        if head_relation == pygame.math.Vector2(0,1):
            self.head = self.head_up
        if head_relation == pygame.math.Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == pygame.math.Vector2(1,0):
            self.tail = self.tail_left
        if tail_relation == pygame.math.Vector2(-1,0):
            self.tail = self.tail_right
        if tail_relation == pygame.math.Vector2(0,1):
            self.tail = self.tail_up
        if tail_relation == pygame.math.Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [pygame.math.Vector2(5,10), pygame.math.Vector2(6,10), pygame.math.Vector2(7,10)]


class Fruit:
    def __init__(self):
        self.randomize()
        self.apple_image = pygame.image.load('Assets/Graphics/apple.png').convert_alpha()

    def draw_fruit(self,screen):
        fruit_rect = pygame.Rect(int(self.pos.x * TILE_SIZE), int(self.pos.y * TILE_SIZE), TILE_SIZE, TILE_SIZE)
        screen.blit(self.apple_image,fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0, TILE_NO -1)
        self.y = random.randint(0, TILE_NO -1)
        self.pos = pygame.math.Vector2(self.x,self.y)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self,screen):
        self.draw_grass(screen)
        self.fruit.draw_fruit(screen)
        self.snake.draw_snake(screen)
        self.draw_score(screen)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < TILE_NO:
            self.game_over()
        if not 0 <= self.snake.body[0].y < TILE_NO:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self,screen):
        grass_color = (167,200,61)

        for row in range(TILE_NO):
            if row % 2 == 0:
                for col in range(TILE_NO):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,TILE_SIZE)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(TILE_NO):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,TILE_SIZE)
                        pygame.draw.rect(screen,grass_color,grass_rect)
    
    def draw_score(self,screen):
        game_font = pygame.font.Font('Assets/Font/PoetsenOne-Regular.ttf', 25)
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(TILE_SIZE * TILE_NO - 60)
        score_y = int(TILE_SIZE * TILE_NO - 60)
        score_rect = score_surface.get_rect(center = (score_x,score_y))

        apple_image = pygame.image.load('Assets/Graphics/apple.png').convert_alpha()
        apple_rect = apple_image.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple_image,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((TILE_NO * TILE_SIZE, TILE_NO * TILE_SIZE))
    clock = pygame.time.Clock()
    pygame.mixer.pre_init(44100,-16,2,512) # Magic numbers to remove Sound Buffer

    game = Game()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE,150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.snake.direction.y != 1:
                    game.snake.direction = pygame.math.Vector2(0,-1)
                if event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                    game.snake.direction = pygame.math.Vector2(0,1)
                if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                    game.snake.direction = pygame.math.Vector2(-1,0)
                if event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                    game.snake.direction = pygame.math.Vector2(1,0)
        
        screen.fill((175,215,70))
        game.draw_elements(screen)
        pygame.display.update()
        clock.tick(60)

if __name__=='__main__':
    main()
