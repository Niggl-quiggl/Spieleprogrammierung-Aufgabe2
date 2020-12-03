import pygame                                           # Stellt Objekte und Konstanten zur Spielprogrammierung zur Verfügung
from pygame.constants import (                          # Verhindert verteilte Warnungen des Editors
    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN
)
import os
import random


class Settings(object):


    def __init__(self):

        self.width = 800
        self.height = 600
        self.fps = 60       
        self.title = "ITA Invader" 
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")
        self.astedist = 15


    def get_dim(self):

        return (self.width, self.height)

class Defender(pygame.sprite.Sprite):

    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "Asteroid-Man.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 42))
        self.rect = self.image.get_rect()
        self.rect.left = (settings.width - self.rect.width) // 2
        self.rect.top = settings.height - self.rect.height - 10
        self.direction = 0
        self.speed = 5

    def update(self):

        newleft = self.rect.left + (self.direction * self.speed)
        newright = newleft + self.rect.width
        newtop = self.rect.top + (self.direction * self.speed) 
        newbottom = newtop + self.rect.height
        if newleft > 0 and newright < settings.width:
            self.rect.left = newleft
        if newtop > 0 and newbottom < settings.height:
            self.rect.top = newtop


class Enemy(pygame.sprite.Sprite):

    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "Asteroid1.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, 300) 
        self.rect.top = random.randint(0, 300) 
        self.direction = 1
        self.speed = 2

    def update(self):

        newleft = self.rect.left + (self.direction * self.speed)
        newright = newleft + self.rect.width
        if newleft <= 0:
            self.direction = 300
        if newright >= settings.width:
            self.direction = -1
        self.rect.left += (self.direction * self.speed) 

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "background.png")).convert()
        self.background_rect = self.background.get_rect()
        self.defender = Defender(settings)
        self.clock = pygame.time.Clock()
        self.done = False

        self.all_defenders = pygame.sprite.Group()
        self.all_defenders.add(self.defender)

        self.all_enemies = pygame.sprite.Group()
        for n in range (0, 4):
            self.all_enemies.add(Enemy(settings))


    def run(self):
        while not self.done:                            # Hauptprogrammschleife mit Abbruchkriterium   
            self.clock.tick(self.settings.fps)          # Setzt die Taktrate auf max 60fps   
            for event in self.pygame.event.get():       # Durchwandere alle aufgetretenen  Ereignisse
                if event.type == QUIT:                  # Wenn das rechts obere X im Fenster geklickt
                    self.done = True                    # Flag wird auf Ende gesetzt
                elif event.type == KEYDOWN:             # Reagiere auf Taste drücken
                    if event.key == K_ESCAPE:
                        self.done = True
                    if event.key == K_LEFT:
                        self.defender.direction = -1
                    elif event.key == K_RIGHT:
                        self.defender.direction = 1
                    elif event.key == K_UP:
                        self.defender.direction = -1
                    elif event.key == K_DOWN:
                            self.defender.direction = 1  
                elif event.type == KEYUP:               # Reagiere auf Taste loslassen
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        self.defender.direction = 0
            self.update()
            self.draw()
 
    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.all_defenders.draw(self.screen)
        self.all_enemies.draw(self.screen)
        self.pygame.display.flip()   # Aktualisiert das Fenster

    def update(self):
        self.all_defenders.update()
        self.all_enemies.update()


if __name__ == '__main__':      # 
                                    
    settings = Settings()
# pylint: disable=no-member
    pygame.init()               # Bereitet die Module zur Verwendung vor  
# pylint: enable=no-member
    game = Game(pygame, settings)
    game.run()
  
# pylint: disable=no-member
    pygame.quit()               # beendet pygame
# pylint: enable=no-member

