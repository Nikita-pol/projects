import pygame
import os
import random
import classes as cls

WAY = os.path.abspath(__file__)[:-7]
FPS = 50

pygame.init()
screen = pygame.display.set_mode((800, 550))
pygame.display.set_caption("The Life")
clock = pygame.time.Clock()

print(WAY)
menu_bg = pygame.image.load(WAY + 'images\\backgrounds\\menu_bg.png')

running = True
menu = True
game = False

create_bacteria = True
create_plancton = False
kill = False

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
                    print(position)
                    if position[1] >= 500:
                        if 506 <= position[1] <= 543:
                            if 6 <= position[0] <= 43:
                                cls.pbx = 6
                                create_bacteria = True
                                create_plancton = False
                                kill = False
                            if 50 <= position[0] <= 87:
                                cls.pbx = 50
                                create_plancton = True
                                create_bacteria = False
                                kill = False
                            if 94 <= position[0] <= 131:
                                cls.pbx = 94
                                kill = True
                                create_bacteria = False
                                create_plancton = False
                    else:
                        if create_bacteria:
                            cls.bacteria = cls.Bacteria(position[0], position[1], 5, 5)
                            cls.bacterias.add(cls.bacteria)
                        if create_plancton:
                            cls.plnc = cls.Plancton(position[0], position[1])
                            cls.planctons.add(cls.plnc)
                        if kill:
                            cls.killer = cls.Killer(position[0], position[1])
                            cls.killerG.add(cls.killer)
        if time >= random.randint(1, 20):
            time = 0
            cls.plnc = cls.Plancton()
            cls.planctons.add(cls.plnc)

        cls.planctons.update()
        cls.bacterias.draw(screen)
        cls.bacterias.update()
        cls.zones.draw(screen)
        cls.planctons.draw(screen)
        cls.game_tools.draw(screen)
        cls.game_tools.update()

        cls.killerG.update()

        pygame.display.flip()
pygame.quit()
