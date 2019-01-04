import pygame
import gameConfig as config
from Player import Player
from Ball import Ball
from TargetObject import TargetObject
import sys

pygame.init()
all_sprites = pygame.sprite.Group()
deltaTime = 0.0
ballDelta = 0.0
screen = pygame.display.set_mode(config.DEFAULT_SCREEN_SIZE)
p1 = Player(config.PLAYER_START_POSITION,
            config.PLAYER_SIZE, config.DEFAULT_PLAYER_SPEED)
ball = Ball((config.PLAYER_START_POSITION[0] + config.PLAYER_SIZE[0]/2,
             config.PLAYER_START_POSITION[1] - config.BALL_RADIUS), config.BALL_RADIUS, config.DEFAULT_BALL_SPEED, False)
allBalls = [ball]
allBallsDeltas = [ballDelta]
ballSpawnedOnPoints = 0
numberOfBalls = 1
targets = []
numberOfTargets = config.TARGETS_IN_ROW * config.NUMBER_OF_ROWS
clock = pygame.time.Clock()


def CreateTargets():
    top = 15
    left = 200
    numberOfElements = 0
    for i in range(config.NUMBER_OF_ROWS):
        for j in range(config.TARGETS_IN_ROW):
            targets.append(TargetObject((left, top)))
            all_sprites.add(targets[numberOfElements])
            numberOfElements += 1
            left += 110
        top += 50
        left = 200


def RefreshScreen(screen, player):
    screen.fill(config.COLOR_BLACK)
    player.DrawPlayer(screen, config.PLAYER_COLOR)
    for i in range(len(allBalls)):
        allBalls[i].DrawBall(screen, config.BALL_COLOR)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()


def StartGame():
    allBalls[0].SetRunningMode(True)


CreateTargets()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    deltaTime += clock.tick() / 1000.0

    for i in range(len(allBallsDeltas)):
        if allBalls[i].GetRunningMode() == True:
            allBallsDeltas[i] += deltaTime
        #ballDelta += deltaTime
    # print(deltaTime)
    while deltaTime > 1 / config.MAX_GAME_FPS:
        deltaTime -= 1 / config.MAX_GAME_FPS

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            StartGame()

        if keys[pygame.K_LEFT]:
            if ball.isRunning == False:
                ball.MoveBallLeft()
            p1.MovePlayerLeft()

        if keys[pygame.K_RIGHT]:
            if ball.isRunning == False:
                ball.MoveBallRight()
            p1.MovePlayerRight()

        if numberOfTargets != 0:
            for i in range(len(targets)):
                if targets[i-1].GetHp() <= 0:
                    # to jest na bank dobrze
                    all_sprites.remove(targets[i-1])
                    targets.remove(targets[i-1])
                    numberOfTargets -= 1
                    p1.AddPoints(config.POINTS_FOR_BLOCK)

                    # tu juz nie wiem - do testow
                    if p1.GetScore() % config.NEW_BALL_SPAWN_ON_POINTS == 0 and ballSpawnedOnPoints != p1.GetScore():
                        print(p1.score)
                        newBall = Ball(config.NEW_BALL_START_POINT,
                                       config.BALL_RADIUS, config.DEFAULT_BALL_SPEED, True)
                        allBalls.append(newBall)
                        numberOfBalls += 1
                        ballSpawnedOnPoints = p1.GetScore()
                        newBallDelta = 0.0
                        allBallsDeltas.append(newBallDelta)

    for i in range(len(allBalls)):
        while allBallsDeltas[i] > 1 / allBalls[i].GetSpeed():
            for i in range(len(allBalls)):
                if allBalls[i].GetRunningMode() == True:
                    allBallsDeltas[i] -= 1 / allBalls[i].GetSpeed()
                    allBalls[i].MoveBall()
                    allBalls[i].IsCollidedWithPlayer(p1)
                    allBalls[i].IsCollidedWithEdge()

                    if numberOfTargets != 0:
                        for j in range(numberOfTargets):
                            allBalls[i].IsCollidedWithObject(targets[j])

    RefreshScreen(screen, p1)
