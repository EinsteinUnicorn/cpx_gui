from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
from blocks import *
from compiler import * 
import random

class CircuitPlaygroundGUI(ModalApp):

    def appStarted(app):
        app.splash =  SplashMode()
        app.program = ProgramMode()
        app.help =  HelpMode()
        app.setActiveMode(app.splash)

class SplashMode(Mode):

    def appStarted(mode):
        pass

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.program)

    def redrawAll(mode, canvas):
        #TODO this is where the splash screen graphic will go
        pass 

class HelpMode(Mode):

    def appStarted(mode):
        #TODO put help message here
        pass

    def keyPressed(mode):
        mode.app.setActiveMode(mode.app.program)

    def redrawAll(mode, canvas):
        #TODO put the help screen graphic here
        pass

class ProgramMode(Mode):

    def appStarted(mode):
        #this is where the list of "commands" will go
        mode.programComponents =  []
        mode.blocks = [StartBlock()]

    def keyPressed(mode, event):
        if event.key == 'l':
            mode.blocks.append(\
                NeopixelBlock(mode.width/2, mode.height/2))

        elif event.key == 's':

            mode.blocks.append(\
                SpeakerBlock( mode.width/2, mode.height/2))

        elif event.key == 'h':
            print('\nh')
            mode.app.setActiveMode(mode.app.help)

        elif event.key == 'd':
            print('\nddd')
            mode.blocks.append(\
                DelayBlock( mode.width/2, mode.height/2))

        elif event.key == 'r':
            #removes the last item
            mode.blocks.pop()
        
        elif event.key == 'c':
            #change the color
            mode.blocks[1].changeColor(random.randint(0,9))

        
    def mousePressed(mode, event):
        #this is where the code that will handle the 'compiling will go'
        #if compilebutton.touches(event.x, event.y):
        Compiler(mode.blocks).fileWrite()
    def redrawAll(mode, canvas ):
        #draw the background
        pass

def runCircuitPlaygroundGUI():
    CircuitPlaygroundGUI(width = 1320, height = 800)

runCircuitPlaygroundGUI()