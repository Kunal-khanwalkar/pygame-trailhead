import pygame, sys
from pygame.locals import *
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (640,660))
        self.speed = 15
        self.lasers = pygame.sprite.Group()
        self.laser_cooldown = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.x <= 20:
                self.rect.x = 20
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.x >= 1280 - self.image.get_width() - 20:
                self.rect.x = 1280 - self.image.get_width() - 20
        if keys[pygame.K_SPACE]:
            if self.laser_cooldown == 0:
                laser_sound = pygame.mixer.Sound('assets/sounds/laser.ogg')
                laser_sound.set_volume(0.5)    
                laser_sound.play()

                self.lasers.add(Laser(self.rect.center))
                self.laser_cooldown = 10


    def lasers_update(self):
        # Update lasers
        [laser.update() for laser in self.lasers]
        # Free up lasers
        [laser.kill() for laser in self.lasers if laser.rect.y <= 0]
        # Cooldown
        self.laser_cooldown -= 1
        if self.laser_cooldown <= 0:
            self.laser_cooldown = 0

    
    def update(self):
        self.player_input()
        self.lasers_update()

        
class Laser(pygame.sprite.Sprite):
    def __init__(self,player_position):
        super().__init__()
        self.image = pygame.image.load('assets/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(center = player_position)
        self.speed = 30
    
    def update(self):
        self.rect.y -= self.speed
            

class Meteor(pygame.sprite.Sprite):
    def __init__(self,spawn_position):
        super().__init__()
        self.image = pygame.image.load('assets/graphics/meteor.png').convert_alpha()
        self.rect = self.image.get_rect(center = spawn_position)
        self.speed = randint(3,7)

    def update(self):
        self.rect.y += self.speed

def game_over(meteors):
    for meteor in meteors:
        if meteor.rect.y >= 725:
            exp_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
            exp_sound.play()
            return True

    return False

def check_collisions(player,meteors):
    is_col = pygame.sprite.groupcollide(player.sprite.lasers,meteors,True,True)
    if is_col:
        exp_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
        exp_sound.play()


def score():
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score_text = font.render(f'Score: {current_score}', False, 'Black')
    score_text_rect = score_text.get_rect(topright = (1240,40))
    screen.blit(score_text,score_text_rect)
    return current_score

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

background = pygame.image.load('assets/graphics/background.png').convert()
font = pygame.font.Font('assets/graphics/subatomic.ttf',50)
title_text = font.render('Welcome to Space Invaders',False,'Black')
title_text_rect = title_text.get_rect(center = (640,330))
game_active = False

bg_music = pygame.mixer.Sound('assets/sounds/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

player = pygame.sprite.GroupSingle()

meteors = pygame.sprite.Group()
meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer,1500)

game_score = 0
start_time = 0

while True:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == meteor_timer:
                meteors.add(Meteor((randint(100,1000),-50)))
        if not game_active:
            if event.type == KEYDOWN:
                game_score = 0
                start_time = int(pygame.time.get_ticks() / 1000)
                player.add(Player())
                game_active = True

    if game_active:
        game_score = score()

        player.draw(screen)
        player.sprite.lasers.draw(screen)
        player.update()

        meteors.draw(screen)
        meteors.update()

        check_collisions(player,meteors)

        game_active = not game_over(meteors)

    else:
        if game_score:
            score_text = font.render(f'Your score is {game_score}',False,'Black')
            score_text_rect = score_text.get_rect(center = (640,330))
            screen.blit(score_text,score_text_rect)
        else:
            screen.blit(title_text,title_text_rect)
        player.empty()
        meteors.empty()


    clock.tick(60)
    pygame.display.update()
