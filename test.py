#!/usr/bin/env python2
import sys
from time import sleep, clock, time
from PyQt4 import QtGui, QtCore

gameField = []

for i in range(0, 20):
    gameField.append([0]*20)

print gameField

class redrawWindow(QtCore.QObject):
    rdw = QtCore.pyqtSignal()

class Worker(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        for i in range(0, 100000):
            sleep(0.02)
            sgn.rdw.emit()

class player:
    def __init__(self, pos = (80, 700)):
        self.pos = pos
        self.legsDown = True
        self.handsUp = True
        self.jump = False
        self.last = clock()*28
        self.vel = (0, -970)
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
            print y2-y1, dim[1]
            exit(0)
        return (x1, y1, x2, y2)

    def drawMe(self, qp):
        c = clock()*28
        t = c - self.last
        self.last = c
        p = self.pos
        v = self.vel
        self.pos = p[0]+v[0]*t, p[1]+v[1]*t
        self.vel = v[0]+self.grvt[0]*t, v[1]+self.grvt[1]*t
        print self.vel
        d = self.getDim()
        if self.getBox()[3] > 800:
            self.vel = self.vel[0], 0
            if self.legsDown:
                self.pos = self.pos[0], 725
            else:
                self.pos = self.pos[0], 760
        if self.getBox()[3] == 800 and self.jump == True:
            self.vel = (0, -970)




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
        self.setWindowTitle("Yes!!")
        self.mafia = player()
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.show()
        self.worker = Worker()
        sgn.rdw.connect(self.repaint)
        self.worker.start()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawLine(800, 0, 800, 800)
        self.drawGame(e, qp)
        qp.end()

    def home(self):
        for i in range(0, 1000):
            self.repaint()

    def drawCharacter(self, qp, ch):
        dim = ch.getBox()
        qp.setPen(QtGui.QColor(194,194,194))
        qp.drawRect(dim[0], dim[1], dim[2]-dim[0], dim[3]-dim[1])
        qp.setPen(QtGui.QColor(167,34,54))
        ch.drawMe(qp)

    def drawGame(self, event, qp):
        qp.setPen(QtGui.QColor(167,34,54))
        self.drawCharacter(qp, self.mafia)

        if self.left:
            qp.fillRect(800, 60, 40, 40, QtCore.Qt.SolidPattern)
        if self.down:
            qp.fillRect(850, 60, 40, 40, QtCore.Qt.SolidPattern)
        if self.right:
            qp.fillRect(900, 60, 40, 40, QtCore.Qt.SolidPattern)
        if self.up:
            qp.fillRect(850, 10, 40, 40, QtCore.Qt.SolidPattern)
        self.num += 1

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            return
        if e.key() == QtCore.Qt.Key_Escape:
            self.worker.exit()
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
    sgn = redrawWindow()
    GUI = Window()

    k = app.exec_()
    sys.exit(k)
