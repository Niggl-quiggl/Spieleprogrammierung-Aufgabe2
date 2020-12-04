import pygame                                           
from pygame.constants import (                          
    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
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
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "Monster.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.left = (settings.width - self.rect.width) // 2
        self.rect.top = settings.height - self.rect.height - 10
        self.directionx = 0
        self.directiony = 0
        self.speed = 5

    def update(self):

        newleft = self.rect.left + (self.directionx * self.speed)
        newright = newleft + self.rect.width
        newtop = self.rect.top + (self.directiony * self.speed) 
        newbottom = newtop + self.rect.height
        if newleft > 0 and newright < settings.width:
            self.rect.left = newleft
        if newtop > 0 and newbottom < settings.height:
            self.rect.top = newtop

    def respawn(self):

        self.rect.left = random.randint(0, self.settings.width-self.rect.width)
        self.rect.top = random.randint(0, self.settings.height-self.rect.height)


class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "Oma.png")).convert()
        self.background_rect = self.background.get_rect()
        self.defender = Defender(settings)
        self.clock = pygame.time.Clock()
        self.done = False

        self.all_defenders = pygame.sprite.Group()
        self.all_defenders.add(self.defender)

        

    def run(self):
        while not self.done:                            
            self.clock.tick(self.settings.fps)          
            for event in self.pygame.event.get():       
                if event.type == QUIT:                 
                    self.done = True 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True                        
                    if event.key == K_ESCAPE:
                        self.done = True
                    if event.key == K_LEFT:
                        self.defender.directionx = -1
                    elif event.key == K_RIGHT:
                        self.defender.directionx = 1
                    elif event.key == K_UP:
                        self.defender.directiony = -1
                    elif event.key == K_DOWN:
                            self.defender.directiony = 1  
                elif event.type == KEYUP:               
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        self.defender.directionx = 0
                    if event.key == K_UP or event.key == K_DOWN:
                        self.defender.directiony = 0
                    if event.key == K_SPACE: 
                        self.defender.respawn()
                        
            self.update()
            self.draw()
 
    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.all_defenders.draw(self.screen)
        self.pygame.display.flip()  

    def update(self):
        self.all_defenders.update()


if __name__ == '__main__':     
    settings = Settings()

    pygame.init()              
    game = Game(pygame, settings)
    game.run()
  

    pygame.quit()              

