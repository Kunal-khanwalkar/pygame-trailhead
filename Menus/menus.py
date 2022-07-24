import pygame, sys
from pygame.locals import *


def main():
    WINDOW_SIZE = (500,500)
    CLOCK = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Menus')
    screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
    screen_font = pygame.font.SysFont(None, 30)

    bg = pygame.Color('#A6D1E6')
    Click = False
    while True:

        screen.fill(bg)

        text = screen_font.render('Main Menu', False, pygame.Color('#3D3C42'))
        screen.blit(text,(200,50))

        mx, my = pygame.mouse.get_pos()

        Menu1 = pygame.Rect(150,150,200,50)
        pygame.draw.rect(screen,pygame.Color('#7F5283'),Menu1)
        Menu1_text = screen_font.render('Game', False, pygame.Color('#FEFBF6'))
        screen.blit(Menu1_text,(220,165))

        Menu2 = pygame.Rect(150,300,200,50)
        pygame.draw.rect(screen,pygame.Color('#7F5283'),Menu2)
        Menu2_text = screen_font.render('Options', False, pygame.Color('#FEFBF6'))
        screen.blit(Menu2_text,(210,315))

        if Menu1.collidepoint((mx,my)):
            if Click:
                game(screen)
                Click = False
        if Menu2.collidepoint((mx,my)):
            if Click:
                options(screen)
                Click = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    Click = True

        pygame.display.update()
        CLOCK.tick(60)

def game(screen):
    running = True
    bg = pygame.Color('#A6D1E6')
    screen.fill(bg)
    screen_font = pygame.font.SysFont(None, 30)
    CLOCK = pygame.time.Clock()

    while running:
        text = screen_font.render('Game', False, pygame.Color('#3D3C42'))
        screen.blit(text,(200,50))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        pygame.display.update()
        CLOCK.tick(60)

def options(screen):
    running = True
    bg = pygame.Color('#A6D1E6')
    screen.fill(bg)
    screen_font = pygame.font.SysFont(None, 30)
    CLOCK = pygame.time.Clock()

    while running:
        text = screen_font.render('Options', False, pygame.Color('#3D3C42'))
        screen.blit(text,(200,50))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        pygame.display.update()
        CLOCK.tick(60)

if __name__=='__main__':
    main()
