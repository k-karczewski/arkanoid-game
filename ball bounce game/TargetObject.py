import pygame
import gameConfig as config


class TargetObject(pygame.sprite.Sprite):

    def __init__(self, startPosition):
        super().__init__()
        self.image = pygame.image.load('./assets/sprites/target.png')
        self.rect = self.image.get_rect()
        self.rect.x = startPosition[0]
        self.rect.y = startPosition[1]
        self.hp = config.DEFAULT_OBJECT_HP_COUNT

    def DecrementHp(self):
        if self.hp > 0:
            self.hp -= 1

        if self.hp == 1:
            self.image = pygame.image.load('./assets/sprites/targethit.png')
