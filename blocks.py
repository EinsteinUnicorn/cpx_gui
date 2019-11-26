from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
from mainapp import *
import copy
import random
import math

class StartBlock(object):
    def __init__(self, mode):
        self.mode =  mode
        self.x =  100
        self.y = 200
        self.image = self.mode.loadImage('start_block.png')
        self.msg = """import time
import board 
import neopixel
from adafruit_circuitplayground.express import cpx
while True:
"""

    def toString(self):
        return self.msg
    
    def inBounds(self, x, y):
        if x >= self.x - 100 and x <= self.x + 100 and \
            y >= self.y - 50 and y  <= self.y + 50:
                return True
        return False
    
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.image))

class NeopixelBlock(object):
    def __init__(self, x, y, mode):
        self.mode = mode
        self.x, self.y = x, y
        self.numTabs = 0
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        #these correspond with an index of the colors list
        self.ledColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        #these are images to be drawn
        self.block = self.mode.loadImage('led_block.png')
        self.base = self.mode.loadImage('cpx base.png')
        self.ledImages = [self.mode.loadImage('red_led.png'),\
            self.mode.loadImage('green_led.png'), \
               self.mode.loadImage('blue_led.png')]
    
    #returns a list of RGB values that correspond to the color of each led
    def getLedColors(self):
        result = []
        for led in self.ledColors:
            result.append(self.colors[led])
        return result

    #added to ensure that this works with if blocks
    def addTab(self, numTabs):
        self.numTabs  = numTabs

    #for converting to python
    def toString(self):
        s = ""
        ledColors = self.getLedColors()
        tabs = "\t" 
        tabs *= self.numTabs + 1
        for i in range(10):
            s+= f'\n{tabs}cpx.pixels[{i}]= {ledColors[i]}'
        return s

    #use getLed as the LED arguement
    def changeColor(self, led):
        self.ledColors[led] += 1
        self.ledColors[led] %= 3
    
    #returns  the distance between two points
    def getDistance(self, x0, y0, x1, y1):
        return math.sqrt((x0-x1)**2 + (y0-y1)**2)

    #takes mouse coordinates and returns which led the mouse 
    #is hovering over
    def getLed(self, x, y):
        #the radius of each LED is 10
        for led in range(len(self.getLedCoordinates())):
            ledx, ledy = self.getLedCoordinates()[led]
            if self.getDistance(ledx, ledy, x, y) <= 10:
                return led

    #determines whether coordinates are over an led or not
    def inLed (self, x, y):
        for led in range(len(self.getLedCoordinates())):
            ledx, ledy = self.getLedCoordinates()[led]
            if self.getDistance(ledx, ledy, x, y) <= 10:
                return True
        return False
        
    #determines whether the coordinates are inside the block or not
    def inBounds(self, x, y):
        if x >= self.x - 100 and x <= self.x + 100 and \
            y >= self.y - 100 and y  <= self.y + 100 and \
                self.inLed(x, y) == False:
                    return True
        return False

    #used for drawing and changing the colors of LED
    def getLedCoordinates(self):
        ledCoordinates = []
        for led in range(10):
            ledAngle =  math.pi/2 - (2*math.pi)*(led/10)
            ledX = self.x + 60 * math.cos(ledAngle)
            ledY = self.y - 60 * math.sin(ledAngle)
            ledCoordinates.append((ledX, ledY))
        return ledCoordinates

    def draw(self, canvas):
        
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.block))
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.base))

        #draws the leds circularly
        for led in range(10):
            ledX, ledY = self.getLedCoordinates()[led]
            
            self.ledImage = self.ledImages[self.ledColors[led]]
            canvas.create_image(ledX, ledY,\
                image=ImageTk.PhotoImage(self.ledImage))

class SpeakerBlock(object):
    def __init__(self, x, y, mode):
        self.mode = mode
        self.x, self.y = x, y
        self.numTabs = 0
        #these are the frequencies in c  major scale
        #Notes: CDEFGABC^
        self.frequencies = [262, 294.8, 327.5, 349.3, \
            393.0, 436.7, 491.2, 524]
        self.currentToneIndex = 0
        self.currentFreq = self.frequencies[self.currentToneIndex]
        self.base = self.mode.loadImage('speaker_block.png')

        #a list the images that correspond with the frequencies
        self.freqImages = [self.mode.loadImage('speaker_block_C.png'), \
            self.mode.loadImage('speaker_block_D.png'),\
                self.mode.loadImage('speaker_block_E.png'), \
                    self.mode.loadImage('speaker_block_F.png'), 
                        self.mode.loadImage('speaker_block_G.png'), \
                            self.mode.loadImage('speaker_block_A.png'),\
                                self.mode.loadImage('speaker_block_B.png'),
                                    self.mode.loadImage('speaker_block_C.png')]
   
    #added to ensure that this works with if blocks
    def addTab(self, numTabs):
        self.numTabs  = numTabs

    def changeTone(self):
        self.currentToneIndex +=  1
        self.currentToneIndex %= 8
        self.currentFreq = self.frequencies[self.currentToneIndex]

    #returns  the distance between two points
    def getDistance(self, x0, y0, x1, y1):
        return math.sqrt((x0-x1)**2 + (y0-y1)**2)
    
    #checks if coordinates are inside of the note block
    def inNote(self, x, y):
        if x >= self.x - 40 and x <= self.x + 40:
            if y >= self.y - 10 and y <= self.y + 50:
                return True
        return False

    def toString(self):
        tabs = "\t" 
        tabs *= self.numTabs + 1
        return f'\n{tabs}cpx.play_tone({self.currentFreq}, .5)'

    def inBounds(self, x, y):
        if x >= self.x - 100 and x <= self.x + 100 and \
            y >= self.y - 100 and y  <= self.y + 100 and\
                self.inNote(x, y)  == False:
                return True
        return False

    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.base))
        canvas.create_image(self.x, self.y, \
            image=ImageTk.PhotoImage(self.freqImages[self.currentToneIndex]))
        
class IfButtonBlock(object):
    def __init__(self, x, y, mode):
        self.mode = mode
        self.x, self.y = x, y
        self.hasBlock = False
        self.block = None
        self.base = self.mode.loadImage('if_block.png')
    
    def inBounds(self, x, y):
        if x >= self.x - 100 and x <= self.x + 100 and \
            y >= self.y - 150 and y  <= self.y + 150:
                return True
        return False

    def inBlockBounds(self, x, y):
        if x >= self.x - 50 and x <= self.x + 50 and \
            y >= self.y  and y  <= self.y + 150:
                return True
        return False
    
    def addBlock(self, block):
        if self.hasBlock != True:
            if self.inBlockBounds(block.x, block.y):
               self.addBlockSelf(block)
    
    def addBlockToSelf(self, block):
        self.block = block
        self.hasBlock

    def move(self, x, y):
        self.x = x
        self.y = y 
        if self.hasBlock == True:
            self.block.x = x #+ some coefficient
            self.block.y = y + 30#+ some coefficient
    
    def toString(self):
        msg  = '\n\tif cpx.button_a:'
        if self.hasBlock == True:
            self.block.addTab(1)
            msg += self.block.toString()
        return msg

    def draw(self, canvas):
        canvas.create_image(self.x, self.y, \
            image=ImageTk.PhotoImage(self.base))
        if self.hasBlock == True:
            self.block.draw(canvas)

class DelayBlock(object):
    def __init__(self, x, y, mode):
        self.mode = mode
        self.x, self.y = x, y
        self.numTabs = 0
        self.image = self.mode.loadImage('delay_block.png')

    def addTab(self, numTabs):
        self.numTabs  = numTabs

    def inBounds(self, x, y):
        if x >= self.x - 100 and x <= self.x + 100 and \
            y >= self.y - 100 and y  <= self.y + 100:
                return True
        return False

    def toString(self):
        tabs = "\t" 
        tabs *= self.numTabs + 1
        return f'\n{tabs}time.sleep(0.5)'
    
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.image))
