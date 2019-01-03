import pygame
import gameConfig as config
import random


class Ball:

    def __init__(self, startPoint, radius, speed):
        self.box = pygame.Rect(startPoint[0], startPoint[1], radius, radius)
        self.startPoint = startPoint
        self.radius = radius
        self.ballSpeed = speed
        self.ballDirection = (bool(random.getrandbits(1)), True)
        self.isRunning = False

    def DrawBall(self, surface, color):
        pygame.draw.circle(
            surface, color, (self.box.x, self.box.y), self.radius)

    def MoveBallLeft(self):
        if self.box.x >= config.PLAYER_SIZE[0]/2:
            self.box.x -= config.DEFAULT_PLAYER_SPEED

    def MoveBallRight(self):
        if self.box.x <= config.DEFAULT_SCREEN_SIZE[0] - config.PLAYER_SIZE[0]/2:
            self.box.x += config.DEFAULT_PLAYER_SPEED

    def MoveBall(self):

        if self.isRunning == True:
            if self.ballDirection[0] == True:
                self.box.x += self.ballSpeed
                # print(self.ballSpeed)
            else:
                self.box.x -= self.ballSpeed
                # print(self.ballSpeed)

            if self.ballDirection[1] == True:
                self.box.y -= self.ballSpeed
                # print(self.ballSpeed)
            else:
                self.box.y += self.ballSpeed
                # print(self.ballSpeed)

    def IsCollidedWithPlayer(self, player):
        if self.box.colliderect(player.box):
            if ((self.box.bottomright[0] >= player.box.topleft[0]
                 and self.box.bottomleft[0] <= player.box.topright[0]) and self.box.bottomleft[1] >= player.box.topleft[1] and self.box.bottomright[1] >= player.box.topright[1] and (self.box.bottomleft[1] <= player.box.topleft[1] + config.PLAYER_SIZE[1] and self.box.bottomright[1] <= player.box.topright[1] + config.PLAYER_SIZE[1])):

                # check what part of paddle has been hit
                if self.box.midbottom[0] <= player.box.midtop[0]:
                    self.ballDirection = (
                        False, not self.ballDirection[1])
                else:
                    self.ballDirection = (
                        True, not self.ballDirection[1])

    def IsCollidedWithEdge(self):
        if (self.box.x <= 0 or self.box.x >= config.DEFAULT_SCREEN_SIZE[0]):
            self.ballDirection = (
                not self.ballDirection[0], self.ballDirection[1])

        if self.box.y <= 0:
            self.ballDirection = (
                self.ballDirection[0], not self.ballDirection[1])

    def IsCollidedWithObject(self, object):
        if self.box.colliderect(object.rect):
            # check if ball touched bottom side of target
            if (((self.box.topleft[0] >= object.rect.bottomleft[0] and self.box.topright[0] <= object.rect.bottomright[0]) and (self.box.topleft[1] <= object.rect.bottomleft[1] and self.box.topright[1] <= object.rect.bottomright[1])) and
                    (self.box.topleft[1] > object.rect.topleft[1] and self.box.topright[1] > object.rect.topright[1])):
                print("bottom")
                self.ballDirection = (
                    self.ballDirection[0], not self.ballDirection[1])
                object.DecrementHp()

            # check if ball touched top side of target
            elif (((self.box.bottomleft[0] >= object.rect.topleft[0] and self.box.bottomright[0] <= object.rect.topright[0]) and (self.box.bottomleft[1] >= object.rect.topleft[1] and self.box.bottomright[1] >= object.rect.topright[1])) and
                    (self.box.bottomleft[1] < object.rect.bottomleft[1] and self.box.bottomright[1] < object.rect.bottomright[1])):
                print("top")
                self.ballDirection = (
                    self.ballDirection[0], not self.ballDirection[1])
                object.DecrementHp()

            # check if ball touched left side of target
            elif ((self.box.topright[0] >= object.rect.topleft[0] and self.box.bottomright[0] >= object.rect.bottomleft[0]) and (self.box.bottomright[1] >= object.rect.topleft[1] and self.box.topright[1] <= object.rect.bottomleft[1]) and (self.box.bottomright[0] < object.rect.bottomright[0] and self.box.topright[0] < object.rect.topright[0])):
                print("left")
                self.ballDirection = (
                    not self.ballDirection[0],  self.ballDirection[1])
                object.DecrementHp()

            # check if ball touched right side of target
            elif ((self.box.topleft[0] <= object.rect.topright[0] and self.box.bottomleft[0] <= object.rect.bottomright[0]) and (self.box.bottomleft[1] >= object.rect.topright[1] and self.box.topleft[1] <= object.rect.bottomright[1]) and (self.box.bottomleft[0] > object.rect.bottomleft[0] and self.box.topleft[0] > object.rect.topleft[0])):
                print("right")
                self.ballDirection = (
                    not self.ballDirection[0],  self.ballDirection[1])
                object.DecrementHp()
            else:
                # collistion not classified
                print("collision not classified")
                pass
