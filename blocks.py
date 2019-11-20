from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import copy
import random

class StartBlock(object):
    def __init__(self):
        self.msg = """import time
import board 
import neopixel
from adafruit_circuitplayground.express import cpx
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
while True:
"""
    def toString(self):
        return self.msg
    
    def draw(self, canvas):
        pass

class NeopixelBlock(object):
    def __init__(self, isConnected, x, y):
        self.isConnected = isConnected
        self.x, self.y = x, y
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        #these correspond with an index of the colors list
        self.ledColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def getLedColors(self):
        result = []
        for led in self.ledColors:
            result.append(self.colors[led])
        return result

    def toString(self):
        s = ""
        ledColors = self.getLedColors()
        for i in range(10):
            s+= f'\n\tled[{i}]= {ledColors[i]}'
        return s

    #use getLed as the LED arguement
    def changeColor(self, led):
        self.ledColors[led] += 1
        self.ledColors[led] %= 3
    
    #takes mouse coordinates and returns which led the mouse 
    #is hovering over
    def getLed(self, x, y):
        #TODO figure out how to get cell bounds of each LED 
        return 1

    def draw(self, canvas):
        pass

class SpeakerBlock(object):
    def __init__(self, isConnected, x, y):
        self.isConnected = isConnected
        self.x, self.y = x, y
        #these are the frequencies in c  major scale
        #Notes: CDEFGABC^
        self.frequencies = [262, 294.8, 327.5, 349.3, \
            393.0, 436.7, 491.2, 524]
        self.currentToneIndex = 0
        self.currentFreq = self.frequencies[self.currentToneIndex]

    def changeTone(self):
        self.currentToneIndex +=  1
        self.currentToneIndex %= 9
        self.currentFreq = self.frequencies[self.currentToneIndex]

    def toString(self):
        return f'\n\tcpx.play_tone({self.currentFreq}, .5)'

    def draw(self, canvas):
        pass

class DelayBlock(object):
    def __init__(self, isConnected, x, y):
        self.isConnected = isConnected
        self.x, self.y = x, y

    def toString(self):
        return "\n\ttime.sleep(0.5)"
    
    def draw(self, canvas):
        pass