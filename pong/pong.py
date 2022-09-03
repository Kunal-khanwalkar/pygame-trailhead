import pygame, sys, random
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Ball:
    def __init__(self):
        self.pos_x = SCREEN_WIDTH / 2 - 10
        self.pos_y = SCREEN_HEIGHT / 2 - 10
        self.ball_speed_x = 4
        self.ball_speed_y = 4
        self.ball_rect = pygame.Rect(self.pos_x, self.pos_y, 20, 20)
    
    def draw_ball(self,screen):
        self.move_ball()
        self.ball_rect = pygame.Rect(self.pos_x, self.pos_y, 20, 20)
        pygame.draw.ellipse(screen,(161,161,161),self.ball_rect)
    
    def move_ball(self):
        if self.ball_rect.top <= 0 or self.ball_rect.bottom >= SCREEN_HEIGHT:
            self.ball_speed_y *= -1
        if self.ball_rect.left <= 0 or self.ball_rect.right >= SCREEN_WIDTH:
            self.game_restart()

        self.pos_x += self.ball_speed_x
        self.pos_y += self.ball_speed_y

    def game_restart(self):
        self.pos_x = SCREEN_WIDTH / 2 - 10
        self.pos_y = SCREEN_HEIGHT / 2 - 10
        self.ball_speed_x = random.randint(0, 5)
        self.ball_speed_y = random.randint(0, 5)

        

class Block:
    def __init__(self,position):
        self.pos_x = position
        self.pos_y = SCREEN_HEIGHT / 2 - 40
        self.block_rect = pygame.Rect(self.pos_x, self.pos_y, 5, 80)
        self.block_speed = 0

    def draw_block(self,screen):
        self.pos_y += self.block_speed
        self.block_rect = pygame.Rect(self.pos_x, self.pos_y, 5, 80)

        if self.block_rect.top <= 0:
            self.block_rect.top = 0
        if self.block_rect.bottom >= SCREEN_HEIGHT:
            self.block_rect.bottom = SCREEN_HEIGHT

        pygame.draw.rect(screen,(161,161,161),self.block_rect)


class Game:
    def __init__(self):
        self.ball = Ball()
        self.player = Block(10)
        self.opponent = Block(SCREEN_WIDTH - 15)

    def draw_elements(self,screen):
        self.get_collision()
        self.opponent_ai()
        self.ball.draw_ball(screen)
        self.player.draw_block(screen)
        self.opponent.draw_block(screen)

    def get_collision(self):
        if self.ball.ball_rect.colliderect(self.player.block_rect) or self.ball.ball_rect.colliderect(self.opponent.block_rect):
            self.ball.ball_speed_x *= -1

    def opponent_ai(self):
        if self.opponent.block_rect.top < self.ball.pos_y:
            self.opponent.block_speed = 4
        if self.opponent.block_rect.bottom > self.ball.pos_y:
            self.opponent.block_speed = -4


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    game = Game()

    while True:
        screen.fill((31,31,31))
        pygame.draw.aaline(screen,(161,161,161), (SCREEN_WIDTH/2,0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    game.player.block_speed -= 5
                if event.key == K_DOWN:
                    game.player.block_speed += 5
            if event.type == KEYUP:
                if event.key == K_UP:
                    game.player.block_speed += 5
                if event.key == K_DOWN:
                    game.player.block_speed -= 5
        
        game.draw_elements(screen)

        pygame.display.update()
        clock.tick(60)

if __name__=='__main__':
    main()