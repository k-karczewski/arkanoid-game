import pygame
import gameConfig as config
import random


class Ball:
    def __init__(self, startPoint, radius, speed, isRunning):
        self.box = pygame.Rect(startPoint[0], startPoint[1], radius, radius)
        self.startPoint = startPoint
        self.radius = radius
        self.ballSpeed = speed
        self.ballDirection = (bool(random.getrandbits(1)), True)
        self.isRunning = isRunning

    def GetRunningMode(self):
        return self.isRunning

    def GetSpeed(self):
        return self.ballSpeed

    def SetRunningMode(self, mode):
        self.isRunning = mode

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
                self.box.x += 1
            else:
                self.box.x -= 1

            if self.ballDirection[1] == True:
                self.box.y -= 1
            else:
                self.box.y += 1

    def IsCollidedWithPlayer(self, player):
        if self.box.colliderect(player.GetHitbox()):
            if ((self.box.bottomright[0] >= player.GetHitbox().topleft[0]
                 and self.box.bottomleft[0] <= player.GetHitbox().topright[0]) and self.box.bottomleft[1] >= player.GetHitbox().topleft[1] and self.box.bottomright[1] >= player.GetHitbox().topright[1] and (self.box.bottomleft[1] <= player.GetHitbox().topleft[1] + config.PLAYER_SIZE[1] and self.box.bottomright[1] <= player.GetHitbox().topright[1] + config.PLAYER_SIZE[1])):

                # check what part of paddle has been hit
                if self.box.midbottom[0] <= player.GetHitbox().midtop[0]:
                    self.ballDirection = (
                        False, not self.ballDirection[1])
                else:
                    self.ballDirection = (
                        True, not self.ballDirection[1])

    def IsCollidedWithEdge(self):
        if (self.box.x <= 0 or self.box.x >= config.DEFAULT_SCREEN_SIZE[0]):
            self.ballDirection = (
                not self.ballDirection[0], self.ballDirection[1])

            if self.ballSpeed <= config.DEFAULT_MAX_BALL_SPEED:
                self.ballSpeed += config.DEFAULT_BALL_ACCELERATION

        if self.box.y <= 0:
            self.ballDirection = (
                self.ballDirection[0], not self.ballDirection[1])

            if self.ballSpeed <= config.DEFAULT_MAX_BALL_SPEED:
                self.ballSpeed += config.DEFAULT_BALL_ACCELERATION

    def IsCollidedWithObject(self, object):
        if self.box.colliderect(object.GetHitbox()):

            # check if ball touched bottom side of target
            if (((self.box.topleft[0] >= object.GetHitbox().bottomleft[0] and self.box.topright[0] <= object.GetHitbox().bottomright[0]) and (self.box.topleft[1] <= object.GetHitbox().bottomleft[1] and self.box.topright[1] <= object.GetHitbox().bottomright[1])) and
                    (self.box.topleft[1] > object.GetHitbox().topleft[1] and self.box.topright[1] > object.GetHitbox().topright[1])):
                self.ballDirection = (
                    self.ballDirection[0], not self.ballDirection[1])
                object.DecrementHp()
                self.box.y += config.MOVEMENT_AFTER_HIT

                if self.ballSpeed <= config.DEFAULT_MAX_BALL_SPEED:
                    self.ballSpeed += config.DEFAULT_BALL_ACCELERATION

            # check if ball touched top side of target
            elif (((self.box.bottomleft[0] >= object.GetHitbox().topleft[0] and self.box.bottomright[0] <= object.GetHitbox().topright[0]) and (self.box.bottomleft[1] >= object.GetHitbox().topleft[1] and self.box.bottomright[1] >= object.GetHitbox().topright[1])) and
                    (self.box.bottomleft[1] < object.GetHitbox().bottomleft[1] and self.box.bottomright[1] < object.GetHitbox().bottomright[1])):
                self.ballDirection = (
                    self.ballDirection[0], not self.ballDirection[1])
                self.box.y -= config.MOVEMENT_AFTER_HIT
                object.DecrementHp()
                if self.ballSpeed <= config.DEFAULT_MAX_BALL_SPEED:
                    self.ballSpeed += config.DEFAULT_BALL_ACCELERATION

            # check if ball touched left side of target
            elif ((self.box.topright[0] >= object.GetHitbox().topleft[0] and self.box.bottomright[0] >= object.GetHitbox().bottomleft[0]) and (self.box.bottomright[1] >= object.GetHitbox().topleft[1] and self.box.topright[1] <= object.GetHitbox().bottomleft[1]) and (self.box.bottomright[0] < object.GetHitbox().bottomright[0] and self.box.topright[0] < object.GetHitbox().topright[0])):
                self.ballDirection = (
                    not self.ballDirection[0],  self.ballDirection[1])
                self.box.x -= config.MOVEMENT_AFTER_HIT
                object.DecrementHp()
                if self.ballSpeed <= config.DEFAULT_MAX_BALL_SPEED:
                    self.ballSpeed += config.DEFAULT_BALL_ACCELERATION

            # check if ball touched right side of target
            elif ((self.box.topleft[0] <= object.GetHitbox().topright[0] and self.box.bottomleft[0] <= object.GetHitbox().bottomright[0]) and (self.box.bottomleft[1] >= object.GetHitbox().topright[1] and self.box.topleft[1] <= object.GetHitbox().bottomright[1]) and (self.box.bottomleft[0] > object.GetHitbox().bottomleft[0] and self.box.topleft[0] > object.GetHitbox().topleft[0])):
                self.ballDirection = (
                    not self.ballDirection[0],  self.ballDirection[1])
                self.box.x += config.MOVEMENT_AFTER_HIT
                object.DecrementHp()
                if self.ballSpeed <= config.DEFAULT_MAX_BALL_SPEED:
                    self.ballSpeed += config.DEFAULT_BALL_ACCELERATION
            else:
                # collistion not classified
                pass

    def IsOnScreen(self):
        if self.box.y <= config.DEFAULT_SCREEN_SIZE[1]:
            return True
        else:
            return False
