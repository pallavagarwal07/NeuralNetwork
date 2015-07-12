#!/usr/bin/env python2

import numpy as np
from network import Network
import pygame
import sys

# Colors
black = (  0,   0,   0)
white = (255, 255, 255)

# Environment
gameField = []
for i in range(0, 20):
    gameField.append([0]*200)

speed = 0.07

gameField[18][2]  = 0
gameField[19][2]  = 1
gameField[16][15] = 1
gameField[14][12] = 1

class Player:
    #
    # Initial Parameters
    #
    def __init__(self, pos = (80, 700)):
        self.pos      = pos
        self.legsDown = True
        self.handsUp  = True
        self.jump     = False
        self.vel      = (0, 0)
        self.grv      = (0, 1170)
        self.ePos     = 500
        self.eVel     = 400

    def getDim(self):
        height = 85
        height += self.legsDown*35 + self.handsUp*30
        width = 70 if (self.legsDown and self.handsUp) else 110
        return (width, height)

    def getBox(self):
        dim = self.getDim()
        x1 = self.pos[0] - dim[0]/2
        x2 = self.pos[0] + dim[0]/2
        y1 = self.pos[1] - (75 if self.handsUp else 45)
        y2 = self.pos[1] + (75 if self.legsDown else 40)
        return (x1, y1, x2, y2)


def ins((x, y), (x1, y1, x2, y2)):
    if x>x1 and x<x2 and y>y1 and y<y2:
        return True
    return False


def chkOverlap((x1, y1, x2, y2), (p1, q1, p2, q2)):
    if ins((x1, y1), (p1, q1, p2, q2)):
        return True
    if ins((x1, y2), (p1, q1, p2, q2)):
        return True
    if ins((x2, y1), (p1, q1, p2, q2)):
        return True
    if ins((x2, y2), (p1, q1, p2, q2)):
        return True
    if ins((p1, q1), (x1, y1, x2, y2)):
        return True
    if ins((p1, q2), (x1, y1, x2, y2)):
        return True
    if ins((p2, q1), (x1, y1, x2, y2)):
        return True
    if ins((p2, q2), (x1, y1, x2, y2)):
        return True
    return False


def updateRobotInput(robot, brain, start):
    input = []
    j = start
    for i in range(0, 20):
        for k in range(0, 20):
            j = j % 200
            input.append(gameField[i][j])
            j += 1

    input = [input]
    [[robot.legsDown, robot.handsUp, robot.jump]] =  brain.Run(input)


def updatePos(robot):
    t = speed
    p = robot.pos
    v = robot.vel
    g = robot.grv

    robot.pos = p[0]+v[0]*t, p[1] + v[1]* t
    robot.vel = v[0]+g[0]*t, v[1] + g[1]* t
    robot.ePos= robot.ePos - robot.eVel * t

    box = robot.getBox()

    if box[3] > 800:
        robot.vel = robot.vel[0], 0

        if robot.legsDown:
            robot.pos = robot.pos[0], 725
        else:
            robot.pos = robot.pos[0], 760

    if robot.getBox()[3] == 800 and robot.jump == True:
        robot.vel = (0, -770)



def drawEnvrt(robot, screen, d, brain):
    eLoc = (-robot.ePos) % 8000
    b    = robot.getBox()
    j    = int(eLoc/40)
    st   = j*40 - eLoc

    for x in range(int(st), int(st + 800), 40):
        for i in range(0, 20):
            j = j % 200
            y = i*40
            if gameField[i][j]:
                d.rect(screen, black, (x, y, 40, 40))
                if chkOverlap((x, y, x+40, y+40), b) or robot.ePos < -8000:
                    return (1/(1+ np.exp(-robot.ePos/1000)))
        j += 1

    #for i in range(0, 20):
        #for j in range(0, 200):
            #x = (j*40 + eLoc) % 800
            #y = i*40

            #if y == 0 and x >= 0 and x < 40:
                #start = j

            #if gameField[i][j]:
                #d.rect(screen, black, (x, y, 40, 40))
                #if chkOverlap((x, y, x+40, y+40), b) or robot.ePos < -8000:
                    #return (1/(1+ np.exp(-robot.ePos/1000)))

    updateRobotInput(robot, brain, int(eLoc/40))


def drawCharacter(robot, screen, d, brain):
    updatePos(robot)

    k = drawEnvrt(robot, screen, d, brain)
    if k is not None:
        return k

    p = [int(a) for a in robot.pos]
    v = [int(a) for a in robot.vel]

    d.circle(screen, black, (p[0], p[1]-42), 22, 1)
    d.line(screen, black, (p[0], p[1]-20), (p[0]   , p[1]+20))
    d.line(screen, black, (p[0], p[1]+20), (p[0]-30, p[1]+40))
    d.line(screen, black, (p[0], p[1]+20), (p[0]+30, p[1]+40))
    d.line(screen, black, (p[0], p[1])   , (p[0]-35, p[1]-20))
    d.line(screen, black, (p[0], p[1])   , (p[0]+35, p[1]-20))

    if robot.legsDown:
        d.line(screen, black, (p[0]-30, p[1]+40), (p[0]-35, p[1]+75))
        d.line(screen, black, (p[0]+30, p[1]+40), (p[0]+35, p[1]+75))
    else:
        d.line(screen, black, (p[0]-30, p[1]+40), (p[0]-55, p[1]+35))
        d.line(screen, black, (p[0]+30, p[1]+40), (p[0]+55, p[1]+35))
    if robot.handsUp:
        d.line(screen, black, (p[0]-35, p[1]-20), (p[0]-25, p[1]-75))
        d.line(screen, black, (p[0]+35, p[1]-20), (p[0]+25, p[1]-75))
    else:
        d.line(screen, black, (p[0]-35, p[1]-20), (p[0]-55, p[1]-35))
        d.line(screen, black, (p[0]+35, p[1]-20), (p[0]+55, p[1]-35))


def evalRobot(obj):

    # Set the clock
    clock = pygame.time.Clock()

    # Init parameters
    pygame.init()
    screen = pygame.display.set_mode((950, 800))
    d = pygame.draw

    # FLAGS
    done = False

    # Network object
    brain = Network((400, 20, 3), obj)
    robot = Player()

    while not done:
        #
        # Handle Keyboard Events
        #
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                done = True

            # Up key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                robot.jump = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                robot.jump = False

            # Left Key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                robot.legsDown = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                robot.legsDown = True

            # Right Key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                robot.handsUp = False
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                robot.handsUp = True

            # Speedup keys
            global speed
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_z]:   speed -= 0.01
            if pressed[pygame.K_x]: speed += 0.01

        screen.fill(white)
        d.line(screen, black, (800, 0), (800, 800))

        if not robot.legsDown:
            d.rect(screen, black, (800, 60, 40, 40))
        if not robot.handsUp:
            d.rect(screen, black, (900, 60, 40, 40))
        if robot.jump:
            d.rect(screen, black, (850, 10, 40, 40))

        k = drawCharacter(robot, screen, d, brain)
        if k is not None:
            return k

        pygame.display.flip()
        clock.tick(60) #Set fps
    pygame.quit()



#if __name__ == '__main__':
    #print evalRobot([])

