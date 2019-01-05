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
screen = None
p1 = None
ball = None
allBalls = []
allBallsDeltas = []
ballSpawnedOnPoints = 0
numberOfBalls = 1
targets = []
numberOfTargets = 0
clock = None
font = None
gameFailed = False
gameWon = False


def InitializeGame():
    pygame.init()
    global gameFailed
    global gameWon
    global deltaTime
    global ballDelta
    global screen
    global font
    global p1
    global ball
    global numberOfBalls
    global ballSpawnedOnPoints
    global allBalls
    global allBallsDeltas
    global all_sprites
    global targets
    global numberOfTargets
    global clock

    gameFailed = False
    gameWon = False
    deltaTime = 0.0
    ballDelta = 0.0
    screen = pygame.display.set_mode(config.DEFAULT_SCREEN_SIZE)
    font = pygame.font.SysFont(None, 25)
    p1 = Player(config.PLAYER_START_POSITION,
                config.PLAYER_SIZE, config.DEFAULT_PLAYER_SPEED)
    ball = Ball((config.PLAYER_START_POSITION[0] + config.PLAYER_SIZE[0]/2,
                 config.PLAYER_START_POSITION[1] - config.BALL_RADIUS), config.BALL_RADIUS, config.DEFAULT_BALL_SPEED, False)
    numberOfBalls = 1
    ballSpawnedOnPoints = 0
    allBalls = [ball]
    allBallsDeltas = [ballDelta]
    all_sprites = pygame.sprite.Group()
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
    if gameFailed == False and gameWon == False:
        screen.fill(config.COLOR_BLACK)
    player.DrawPlayer(screen, config.PLAYER_COLOR)

    for i in range(len(allBalls)):
        allBalls[i].DrawBall(screen, config.BALL_COLOR)

    CheckScore()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()


def StartGame():
    allBalls[0].SetRunningMode(True)


def CheckGameState(balls, deltas):
    global numberOfBalls
    global gameFailed
    global gameWon
    global numberOfTargets

    for i in range(len(balls)):
        if balls[i].IsOnScreen() == False and balls[i].GetRunningMode() == True:
            numberOfBalls -= 1
            balls[i].SetRunningMode(False)
            if numberOfBalls == 0:
                ShowMessage("You lost! You have reached " +
                            str(p1.GetScore()) + " points. Press R to play again", (255, 255, 255))
                gameFailed = True

    if numberOfTargets == 0:
        ShowMessage("You won! You have reached " +
                    str(p1.GetScore()) + " points. \n Press R to play again", (255, 255, 255))
        gameWon = True


def CheckScore():
    screenText = font.render(
        "Points: " + str(p1.GetScore()), True, (255, 255, 255))
    screen.blit(screenText, [20, 20])


def ShowMessage(msg, color):
    failureText = font.render(msg, True, color)
    screen.blit(
        failureText, (config.DEFAULT_SCREEN_SIZE[0]/2 - 230, config.DEFAULT_SCREEN_SIZE[1]/2))


InitializeGame()
CreateTargets()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    deltaTime += clock.tick() / 1000.0

    for i in range(len(allBallsDeltas)):
        if allBalls[i].GetRunningMode() == True:
            allBallsDeltas[i] += deltaTime

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

        if keys[pygame.K_r]:
            if gameFailed == True or gameWon == True:
                gameFailed = False
                gameWon = False
                InitializeGame()
                CreateTargets()

        if numberOfTargets != 0:
            for i in range(len(targets)):
                if targets[i-1].GetHp() <= 0:
                    # to jest na bank dobrze
                    all_sprites.remove(targets[i-1])
                    targets.remove(targets[i-1])
                    numberOfTargets -= 1
                    p1.AddPoints(config.POINTS_FOR_BLOCK)

                    if p1.GetScore() % config.NEW_BALL_SPAWN_ON_POINTS == 0 and ballSpawnedOnPoints != p1.GetScore():
                        newBall = Ball(config.NEW_BALL_START_POINT,
                                       config.BALL_RADIUS, config.DEFAULT_BALL_SPEED, True)
                        allBalls.append(newBall)
                        numberOfBalls += 1
                        ballSpawnedOnPoints = p1.GetScore()
                        newBallDelta = 0.0
                        allBallsDeltas.append(newBallDelta)

    for i in range(len(allBalls)):
        if allBalls[i].GetRunningMode() == True:
            while allBallsDeltas[i] > 1 / allBalls[i].GetSpeed():
                allBallsDeltas[i] -= 1 / allBalls[i].GetSpeed()
                allBalls[i].MoveBall()
                allBalls[i].IsCollidedWithPlayer(p1)
                allBalls[i].IsCollidedWithEdge()

                if numberOfTargets != 0:
                    for j in range(numberOfTargets):
                        allBalls[i].IsCollidedWithObject(targets[j])

    if gameFailed == False and gameWon == False:
        CheckGameState(allBalls, allBallsDeltas)
        RefreshScreen(screen, p1)
