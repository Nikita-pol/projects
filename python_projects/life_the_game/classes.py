import pygame
import os
import random

WAY = os.path.abspath(__file__)[:-10]
FPS = 50
pbx = 6

pygame.init()
screen = pygame.display.set_mode((1, 1))
pygame.display.set_caption("")
clock = pygame.time.Clock()


img_folder = os.path.join(WAY, 'images')
playBtn_img = pygame.image.load(os.path.join(img_folder, 'btns\\play_btn.png')).convert()
exitBtn_img = pygame.image.load(os.path.join(img_folder, 'btns\\exit_btn.png')).convert()
playBtnAct_img = pygame.image.load(os.path.join(img_folder, 'btns\\play_btn-act.png')).convert()
exitBtnAct_img = pygame.image.load(os.path.join(img_folder, 'btns\\exit_btn-act.png')).convert()
bacteria_img = pygame.image.load(os.path.join(img_folder, 'sprites\\bacteria.png')).convert()
plancton_img = pygame.image.load(os.path.join(img_folder, 'sprites\\plancton.png')).convert()
zone_img = pygame.image.load(os.path.join(img_folder, 'sprites\\zone.png')).convert()
panel_img = pygame.image.load(os.path.join(img_folder, 'panel.png')).convert()
panel_btn_img = pygame.image.load(os.path.join(img_folder, 'btns\\in_panel.png')).convert()


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bacteria(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = bacteria_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.rect.x = x
        self.rect.y = y
        self.hunger = 1
        self.time_to_eat = 60
        self.zone = EatZone()
        zones.add(self.zone)

    def update(self):
        if pygame.sprite.spritecollide(self, killerG, True):
            self.kill()

        if pygame.sprite.spritecollide(self, planctons, True) or\
                pygame.sprite.spritecollide(self.zone, planctons, True):
            self.hunger += 1

        self.zone.rect.x = self.rect.x - 10
        self.zone.rect.y = self.rect.y - 10
        self.time_to_eat -= 0.02
        if self.time_to_eat <= 0:
            self.hunger -= 1
        if self.hunger <= 0:
            self.zone.kill()
            self.kill()
        if self.hunger >= 3:
            bacteria2 = Bacteria(self.rect.x + 50, self.rect.y, 5, 5)
            bacterias.add(bacteria2)
            self.hunger -= 1

        if pygame.sprite.spritecollide(self.zone, planctons, True):
            if plnc.rect.x > self.rect.x:
                self.rect.x += 8
            if plnc.rect.x < self.rect.x:
                self.rect.x -= 8
            if plnc.rect.y > self.rect.y:
                self.rect.y += 8
            if plnc.rect.y < self.rect.y:
                self.rect.y -= 8

        else:
            self.rect.x += self.dx
            self.rect.y += self.dy
            if random.randint(0, 10) > 7:
                self.dx = random.randint(-5, 5)
                self.dy = random.randint(-5, 5)
        if self.rect.x <= 0 or self.rect.x >= 757:
            self.dx *= -1
        if self.rect.y <= 0 or self.rect.y >= 462:
            self.dy *= -1


class Plancton(pygame.sprite.Sprite):
    def __init__(self, x=random.randint(0, 765), y=random.randint(0, 482)):
        pygame.sprite.Sprite.__init__(self)
        self.image = plancton_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.spritecollide(self, killerG, True):
            self.kill()

        if pygame.sprite.spritecollide(self, bacterias, True):
            self.kill()
        r = random.randint(0, 3)
        r2 = random.randint(0, 3)
        if r == 0:
            self.rect.x += 5
        elif r == 1:
            self.rect.x -= 5
        elif r == 2:
            self.rect.x += 5
        if r2 == 0:
            self.rect.y += 5
        elif r2 == 1:
            self.rect.y -= 5
        elif r2 == 2:
            self.rect.y += 5

        if self.rect.x <= -1 or\
            self.rect.x >= 766 or\
            self.rect.y <= -1 or\
            self.rect.y >= 483:
            self.kill()
            plnc = Plancton()
            planctons.add(plnc)


class EatZone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = zone_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Panel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = panel_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500


class PanelButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = panel_btn_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 6
        self.rect.y = 506
    def update(self):
        self.rect.x = pbx


class Killer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.kill()


menu_buttons = pygame.sprite.Group()
start_btn = Button(150, 180, playBtn_img)
exit_btn = Button(150, 280, exitBtn_img)
menu_buttons.add(start_btn, exit_btn)

game_tools = pygame.sprite.Group()
panel = Panel()
panel_btn = PanelButton()
game_tools.add(panel, panel_btn)

bacterias = pygame.sprite.Group()
planctons = pygame.sprite.Group()
zones = pygame.sprite.Group()
killerG = pygame.sprite.Group()
plnc = Plancton()
bacteria = Bacteria(0, 0, 0, 0)
killer = Killer(0, 0)

pygame.quit()
