import pygame
import gameConfig as config


class Player:
    def __init__(self, startPosition, size, speed):
        self.box = pygame.Rect(
            startPosition[0], startPosition[1], size[0], size[1])
        self.width = size[0]
        self.height = size[1]
        self.speed = speed
        self.score = 0

    def GetScore(self):
        return self.score

    def GetHitbox(self):
        return self.box

    def DrawPlayer(self, surface, color):
        pygame.draw.rect(surface, color, self.box, 0)

    def MovePlayerRight(self):
        if self.box.x + self.width <= config.DEFAULT_SCREEN_SIZE[0]:
            self.box.x += self.speed

    def MovePlayerLeft(self):
        if self.box.x >= 0:
            self.box.x -= self.speed

    def AddPoints(self, points):
        self.score += points
