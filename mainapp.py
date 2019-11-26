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
        mode.screen = mode.loadImage('splash_mode_background.png')

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.program)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = \
            ImageTk.PhotoImage(mode.screen))

class HelpMode(Mode):

    def appStarted(mode):
        mode.screen = mode.loadImage('help_screen.png')

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.program)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = \
            ImageTk.PhotoImage(mode.screen))

class ProgramMode(Mode):

    def connect(mode, block, currentList):
        currentList = copy.copy(currentList)
        currentList.append(block)
        return currentList

    def appStarted(mode):
        #this is where the list of "commands" will go
        mode.programComponents =  []
        mode.blocks = [StartBlock(mode)]
        mode.background  = mode.loadImage('active_mode_background.png')
        mode.compileButton = CompileButton(mode)

    def keyPressed(mode, event):
        if event.key == 'l':
            mode.blocks = mode.connect(NeopixelBlock(mode.width/2, mode.height/2, mode),\
                 mode.blocks)

        elif event.key == 's':
            mode.blocks =  mode.connect(SpeakerBlock(mode.width/2, mode.height/2, mode), \
                mode.blocks)

        elif event.key == 'h':
            mode.app.setActiveMode(mode.app.help)

        elif event.key == 'd':
            mode.blocks = mode.connect(
                DelayBlock( mode.width/2, mode.height/2, mode), mode.blocks)

        elif event.key == 'r':
            #removes the last item
            if len(mode.blocks) > 1:
                mode.blocks.pop()
    
        elif  event.key == 'i':
            mode.blocks =  mode.connect(IfButtonBlock(mode.width/2,\
                mode.height/2, mode), mode.blocks)
        

    #def mouseMoved(self, event):
        #print(f'mouseMoved at {(event.x, event.y)}')

    def mousePressed(mode, event):
        #this is where the code that will handle the 'compiling will go'
        print(f'x: {event.x}, y: {event.y}')
        if mode.compileButton.touches(event.x, event.y):
            mode.compileButton.compileCode(mode.blocks)

        for item in mode.blocks:
            if isinstance(item, NeopixelBlock):
                if item.inLed(event.x, event.y):
                    item.changeColor(item.getLed(event.x, event.y))
            if isinstance(item, SpeakerBlock):
                if item.inNote(event.x, event.y):
                    item.changeTone()
        
    def mouseDragged(mode, event):
        for item in mode.blocks:
            if item.inBounds(event.x, event.y):
                item.x = event.x
                item.y = event.y
            
            #if isinstance(item, DelayBlock):
            #    if item.inBounds(event.x, event.y):
            #        item.x = event.x 
            #        item.y = event.y

    def redrawAll(mode, canvas ):
        canvas.create_image(mode.width/2, mode.height/2, image = \
            ImageTk.PhotoImage(mode.background))
        mode.compileButton.draw(canvas)

        for item  in mode.blocks:
            item.draw(canvas)
        

def runCircuitPlaygroundGUI():
    CircuitPlaygroundGUI(width = 1320, height = 800)

runCircuitPlaygroundGUI()