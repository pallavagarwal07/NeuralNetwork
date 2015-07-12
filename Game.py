#!/usr/bin/env python2
import sys
import numpy as np
from time import sleep, clock, time
from PyQt4 import QtGui, QtCore
GUI = []
gameField = []

for i in range(0, 20):
    gameField.append([0]*20)

gameField[18][2] = 1
gameField[19][2] = 1
gameField[16][15] = 1
gameField[14][10] = 1

ePos = 500
eVel = 400
ptr = []
robot = []
sgn = []
scores = []

class player:
    def __init__(self, pos = (80, 700)):
        self.pos = pos
        self.legsDown = True
        self.handsUp = True
        self.jump = False
        self.last = clock()*28
        self.vel = (0, 0)
        self.grvt = (0, 1170)

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
        if not float(y2 - y1) - float(dim[1]) < 10e-6:
            exit(0)
        return (x1, y1, x2, y2)


    def ins((x, y), (x1, y1, x2, y2)):
        if x>x1 and x<x2 and y<y1 and y>y2:
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


    def drawMe(self, qp):
        c = clock()*28
        t = c - self.last
        self.last = c
        p = self.pos
        v = self.vel
        self.pos = p[0]+v[0]*t, p[1]+v[1]*t
        global ePos
        ePos = ePos - t*eVel
        ePosLoc = (ePos + 80000000)%800
        d = self.getDim()
        b = self.getBox()

        # Loop over Barriers
        for i in range(0, 20):
            for j in range(0, 20):
                y = i*40
                x = (ePosLoc + j*40)%800
                if y == 0 and x >= 0 and x < 40:
                    start = j
                if gameField[i][j]:
                    qp.fillRect(x, y, 40, 40, QtCore.Qt.SolidPattern)
                    if x > b[0] and x < b[2] and y > b[1] and y < b[3] or ePos < -8000:
                        scores.append((ePos, 1/(1+ np.exp(-ePos/1000))))
                        GUI.flag = False
                        GUI.close()
                        sys.exit(0)

        input = []
        for i in range(0, 20):
            for j in range(start, 20):
                input.append(gameField[i][j])
            for j in range(0, start):
                input.append(gameField[i][j])
        input = [input]
        [[self.legsDown, self.handsUp, self.jump]] =  robot.Run(input)
        self.vel = v[0]+self.grvt[0]*t, v[1]+self.grvt[1]*t

        if self.getBox()[3] > 800:
            self.vel = self.vel[0], 0
            if self.legsDown:
                self.pos = self.pos[0], 725
            else:
                self.pos = self.pos[0], 760
        if self.getBox()[3] == 800 and self.jump == True:
            self.vel = (0, -770)




        qp.drawEllipse(p[0]-12.5, p[1]-45, 25, 25)
        qp.drawLine(p[0], p[1]-20, p[0], p[1]+20)
        qp.drawLine(p[0], p[1]+20, p[0]-30, p[1]+40)
        qp.drawLine(p[0], p[1]+20, p[0]+30, p[1]+40)
        qp.drawLine(p[0], p[1], p[0]-35, p[1]-20)
        qp.drawLine(p[0], p[1], p[0]+35, p[1]-20)
        if self.legsDown:
            qp.drawLine(p[0]-30, p[1]+40, p[0]-35, p[1]+75)
            qp.drawLine(p[0]+30, p[1]+40, p[0]+35, p[1]+75)
        else:
            qp.drawLine(p[0]-30, p[1]+40, p[0]-55, p[1]+35)
            qp.drawLine(p[0]+30, p[1]+40, p[0]+55, p[1]+35)
        if self.handsUp:
            qp.drawLine(p[0]-35, p[1]-20, p[0]-25, p[1]-75)
            qp.drawLine(p[0]+35, p[1]-20, p[0]+25, p[1]-75)
        else:
            qp.drawLine(p[0]-35, p[1]-20, p[0]-55, p[1]-35)
            qp.drawLine(p[0]+35, p[1]-20, p[0]+55, p[1]-35)


class Window(QtGui.QMainWindow):
    def __init__(self):
        self.num = 0
        super(Window, self).__init__()
        self.setGeometry(2, 50, 950, 800)
        self.setFixedSize(950, 800)
        self.setWindowTitle("Jump! Mafia Jump!")
        self.mafia = player()
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.show()
        self.flag = True
        global GUI
        GUI = self

        while self.flag:
            self.repaint()
            sleep(0.01)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawLine(800, 0, 800, 800)
        self.drawGame(e, qp)
        qp.end()

    def drawCharacter(self, qp, ch):
        dim = ch.getBox()
        qp.setPen(QtGui.QColor(194,194,194))
        qp.drawRect(dim[0], dim[1], dim[2]-dim[0], dim[3]-dim[1])
        qp.setPen(QtGui.QColor(167,34,54))
        ch.drawMe(qp)

    def drawGame(self, event, qp):
        qp.setPen(QtGui.QColor(167,34,54))
        self.drawCharacter(qp, self.mafia)

        if self.mafia.legsDown:
            qp.fillRect(800, 60, 40, 40, QtCore.Qt.SolidPattern)
        if self.down:
            qp.fillRect(850, 60, 40, 40, QtCore.Qt.SolidPattern)
        if self.mafia.handsUp:
            qp.fillRect(900, 60, 40, 40, QtCore.Qt.SolidPattern)
        if self.mafia.jump:
            qp.fillRect(850, 10, 40, 40, QtCore.Qt.SolidPattern)
        self.num += 1

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            return
        if e.key() == QtCore.Qt.Key_Escape:
            scores.append(ePos)
            print scores
            self.close()
        if e.key() == QtCore.Qt.Key_Up:
            self.up = True
            self.mafia.jump = True
        if e.key() == QtCore.Qt.Key_Down:
            self.down = True
        if e.key() == QtCore.Qt.Key_Left:
            self.left = True
            self.mafia.legsDown = False
        if e.key() == QtCore.Qt.Key_Right:
            self.right = True
            self.mafia.handsUp = False

    def keyReleaseEvent(self, e):
        if e.isAutoRepeat():
            return
        if e.key() == QtCore.Qt.Key_Escape:
            exit(0)
        if e.key() == QtCore.Qt.Key_Up:
            self.up = False
            self.mafia.jump = False
        if e.key() == QtCore.Qt.Key_Down:
            self.down = False
        if e.key() == QtCore.Qt.Key_Left:
            self.left = False
            self.mafia.legsDown = True
        if e.key() == QtCore.Qt.Key_Right:
            self.right = False
            self.mafia.handsUp = True


if __name__ == '__main__':
    app = QtGui.QApplication([])
    scores = []
    sgn = redrawWindow()
    GUI = Window()
    k = app.exec_()
    sys.exit(k)
