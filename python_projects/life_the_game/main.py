import pygame
import os
import random
import classes as cls

WAY = os.path.abspath(__file__)[:-7]
FPS = 50

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("The Life")
clock = pygame.time.Clock()

print(WAY)
menu_bg = pygame.image.load(WAY + 'images\\backgrounds\\menu_bg.png')

running = True
menu = True
game = False

time = 0

while running:
    while menu:
        screen.blit(menu_bg, (0, 0))
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = event.pos
                    if 150 <= position[0] <= 650:
                        if 180 <= position[1] <= 260:
                            menu = False
                            game = True
                        if 280 <= position[1] <= 360:
                            running = False
                            menu = False
            if event.type == pygame.MOUSEMOTION:
                pass
        cls.menu_buttons.draw(screen)
        cls.menu_buttons.update()

        pygame.display.flip()

    while game:
        screen.fill((255, 255, 255))
        clock.tick(FPS)
        time += 0.02
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = event.pos
                    cls.bacteria = cls.Bacteria(position[0], position[1], 5, 5)
                    cls.bacterias.add(cls.bacteria)
        if time >= random.randint(1, 20):
            time = 0
            cls.plnc = cls.Plancton()
            cls.planctons.add(cls.plnc)

        cls.bacterias.draw(screen)
        cls.bacterias.update()
        cls.planctons.draw(screen)
        cls.planctons.update()

        pygame.display.flip()
pygame.quit()
