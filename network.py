#!/usr/bin/env python2
from PyQt4 import QtGui, QtCore
import numpy as np
import Game

class Network(object):
    # Class methods
    def __init__(self, layerSize, weights=None):
        self.layerCount = len(layerSize)-1
        self.shape = layerSize
        self.weights = []

        # i-o from last run
        self._layerInput = []
        self._layerOutput = []

        if weights is None:
            # Create the weight arrays
            for l1, l2 in zip(layerSize[:-1], layerSize[1:]):
                self.weights.append(np.random.normal(scale=1, size=(l2, l1+1)))
        else:
            self.weights = weights

    #def __init__(self, layerSize, weights):
        #self.layerCount = len(layerSize)
        #self.shape = layerSize
        #self.weights = []

        ## i-o from last run
        #self._layerInput = []
        #self._layerOutput = []

    def Run(self, input):
        input = np.asarray(input)
        InCases = input.shape[0]

        self._layerInput = []
        self._layerOutput= []

        for index in range(self.layerCount):
            if index == 0:
                dt = np.vstack([input.T, np.ones([1, InCases])])
                layerInput = self.weights[0].dot(dt)
            else:
                layerInput = self.weights[index].dot(np.vstack([self._layerOutput[-1], np.ones([1,InCases])]))

            self._layerInput.append(layerInput)
            self._layerOutput.append(self.sgm(layerInput))

        return self.bin(self._layerOutput[-1].T)

    # Transfer Functions
    def sgm(self, x, derivitive = False):
        if not derivitive:
            return 1/(1+np.exp(-x))
        else:
            out = self.sgm(x)
            return x*(1-x)

    def bin(self, x):
        return np.floor(x+0.5)

def evalRobot(robot):
    app = QtGui.QApplication([])
    scores = []
    Game.scores = scores
    Game.robot = robot
    Game.sgn = Game.redrawWindow()
    Game.ePos = 500
    GUI = Game.Window()
    Game.GUI = GUI
    k = app.exec_()
    return scores[0]


if __name__ == '__main__':
    nets = []
    for i in range(0, 20):
        robot = Network((400, 20, 3))
        k = evalRobot(robot)
        nets.append(( robot.weights, k ))
        print k
    np.save('NeuralNets', nets)
