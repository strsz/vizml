#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:13:50 2018

@author: stremler
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class LinearRegression:
    """LinearRegression"""
    def __init__(self, eta=0.01, maxit=5):
        self.eta = eta
        self.maxit = maxit
    
    def fit(self, X, y):
        self.X = np.column_stack((np.ones(X.shape[0]), X))
        self.weight = np.zeros(self.X.shape[1])
        self.weight_steps = self.weight
        self.y = y
        
        for i in range(self.maxit):
            self.weight += np.matmul(self.eta * (self.y - np.matmul(self.X, self.weight)), self.X)
            self.weight_steps = np.row_stack((self.weight_steps, self.weight))
            
        return self.weight
    
    def _predict(self, X, w):        
        return self._line_func(X, w)
    
    def predict(self, X):
        X = np.column_stack((np.ones(X.shape[0]), X))
        return self._predict(X, self.weight)
    
    def scoreCost(self):
        y = self.predict(self.X)
        return np.mean((self.y - y)**2)
        
    def _line_func(self, X, w):
        return np.matmul(X, w)
    
    def _init_animation(self):
        self.line.set_data([], [])
        return self.line,

    def _animate(self, i):
        lineX = np.array([np.min(self.X[:,1]), np.max(self.X[:,1])])
        lineX = np.column_stack((np.ones(lineX.shape[0]), lineX))
        lineY = self._predict(lineX, self.weight_steps[i,:])
        self.line.set_data(lineX[:,1:], lineY)
        self.title.set_text(u"Step: {}".format(i))
        
        return self.line, self.title
    
    def plot_animation(self, interval=400, xinch=5.5, yinch=5, notebook=True):
        xlim = (np.min(self.X[:,1]) - 0.2 * np.std(self.X[:,1]), np.max(self.X[:,1]) - 0.2 *  - np.std(self.X[:,1]))
        ylim = (np.min(self.y) - 0.2 * np.std(self.y), np.max(self.y) - 0.2 *  - np.std(self.y))
                          
        if notebook:
            plt.ioff()

        fig = plt.figure()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, 
                             xlim=xlim, ylim=ylim)
        plt.axis('on')
        ax.scatter(self.X[:,1], self.y)
        self.line, = ax.plot([], [], c='black')
        self.title = ax.text(0.10, 0.95, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5},
                transform=ax.transAxes, ha="center")

        fig.set_size_inches(xinch, yinch, True)
        print(self.weight_steps.shape[0])
        anim = animation.FuncAnimation(fig, func=self._animate, init_func=self._init_animation,
                               frames=self.weight_steps.shape[0], interval=interval, blit=True)
        
        return anim
    
    def plot_trajectory(self):
        # TODO