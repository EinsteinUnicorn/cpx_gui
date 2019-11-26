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
        #TODO put help message here
        pass

    def keyPressed(mode):
        mode.app.setActiveMode(mode.app.program)

    def redrawAll(mode, canvas):
        pass

class ProgramMode(Mode):

    def connect(mode, block, currentList):
        currentList = copy.copy(currentList)
        currentList.append(block)
        return currentList

    def appStarted(mode):
        #this is where the list of "commands" will go
        mode.programComponents =  []
        mode.blocks = [StartBlock(mode)]
        mode.activeBlocks = [StartBlock(mode)]
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
            print('\nh')
            mode.app.setActiveMode(mode.app.help)

        elif event.key == 'd':
            print('\nddd')
            mode.blocks = mode.connect(
                DelayBlock( mode.width/2, mode.height/2, mode), mode.blocks)

        elif event.key == 'r':
            #removes the last item
            mode.blocks.pop()
    
        elif  event.key == 'i':
            mode.blocks =  mode.connect(IfButtonBlock(mode.width/2,\
                mode.height/2, NeopixelBlock(mode.width/2, mode.height/2)),\
                      mode.blocks)
        
        elif event.key == 'c':
            #change the color
            mode.blocks[1].changeColor(random.randint(0,9))

    def mousePressed(mode, event):
        #this is where the code that will handle the 'compiling will go'
        print(f'x: {event.x}, y: {event.y}')
        print(mode.blocks[0].x, mode.blocks[0].y)
        if mode.compileButton.touches(event.x, event.y):
            mode.compileButton.compileCode(mode.activeBlocks)

        count = 0
        for item in mode.blocks:
            if isinstance(item, NeopixelBlock):
                if item.inLed(event.x, event.y):
                    led = item.getLed(event.x, event.y)
                    item.changeColor(led)
                    if item  in mode.activeBlocks:
                        mode.activeBlocks[count].changeColor(led)
                    #print(f'{item} ledColors' + str(item.getLedColors))
            if isinstance(item, SpeakerBlock):
                if item.inNote(event.x, event.y):
                    item.changeTone()
            count += 1
        
    def mouseDragged(mode, event):
        for item in range(len(mode.blocks)):
            if mode.blocks[item].inBounds(event.x, event.y):
                mode.blocks[item].x = event.x
                mode.blocks[item].y = event.y


    def mouseReleased(mode, event):
        #print('in mouse release')
        if len(mode.activeBlocks) < len(mode.blocks):
            for item in range(len(mode.blocks)):
                if item ==  0:
                    continue
                else:
                    leftX, leftY = mode.blocks[item].getLeftPoint()
                    if mode.blocks[item-1].inRightConnector(leftX, leftY):
                        #mode.activeBlocks = mode.activeBlocks + [mode.blocks[item]]
                        mode.activeBlocks = mode.connect(mode.blocks[item], mode.activeBlocks)
        return

    def redrawAll(mode, canvas ):
        canvas.create_image(mode.width/2, mode.height/2, image = \
            ImageTk.PhotoImage(mode.background))
        mode.compileButton.draw(canvas)

        for item  in mode.blocks:
            item.draw(canvas)
        

def runCircuitPlaygroundGUI():
    CircuitPlaygroundGUI(width = 1320, height = 800)

runCircuitPlaygroundGUI()