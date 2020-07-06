import pygame
import os
import random

WAY = os.path.abspath(__file__)[:-10]
FPS = 50

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()


img_folder = os.path.join(WAY, 'images')
playBtn_img = pygame.image.load(os.path.join(img_folder, 'btns\\play_btn.png')).convert()
exitBtn_img = pygame.image.load(os.path.join(img_folder, 'btns\\exit_btn.png')).convert()
playBtnAct_img = pygame.image.load(os.path.join(img_folder, 'btns\\play_btn-act.png')).convert()
exitBtnAct_img = pygame.image.load(os.path.join(img_folder, 'btns\\exit_btn-act.png')).convert()
bacteria_img = pygame.image.load(os.path.join(img_folder, 'bacteria.png'))
plancton_img = pygame.image.load(os.path.join(img_folder, 'plancton.png'))
zone_img = pygame.image.load(os.path.join(img_folder, 'zone-debug.png'))


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
            print(self.hunger)
            self.rect.x += self.dx
            self.rect.y += self.dy
            if random.randint(0, 10) > 7:
                self.dx = random.randint(-5, 5)
                self.dy = random.randint(-5, 5)
        if self.rect.x <= 0 or self.rect.x >= 757:
            self.dx *= -1
        if self.rect.y <= 0 or self.rect.y >= 462:
            self.dy *= -1

        if pygame.sprite.spritecollide(self, planctons, True):
            self.hunger += 1

class Plancton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = plancton_img
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.x = random.randint(0, 765)
        self.rect.y = self.rect.y = random.randint(0, 482)
    def update(self):
        #if pygame.sprite.spritecollide(self, bacterias, True):
        #    self.kill()
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
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


menu_buttons = pygame.sprite.Group()
start_btn = Button(150, 180, playBtn_img)
exit_btn = Button(150, 280, exitBtn_img)
menu_buttons.add(start_btn, exit_btn)

bacterias = pygame.sprite.Group()
planctons = pygame.sprite.Group()
zones = pygame.sprite.Group()
plnc = Plancton()

pygame.quit()
