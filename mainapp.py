#this file contains all of the modal app related code 
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
        #blocks are 220 by 180
        mode.rows = mode.width // 110
        mode.cols = mode.height // 20
    
    #returns the row, col that the point is in.
    def getCell(mode, x, y):
        cellWidth  = mode.width / mode.cols
        cellHeight = mode.height / mode.rows
        row = int(y / cellHeight) 
        col = int(x / cellWidth)
        return (row, col)
    
    def createBoard(mode):
        #the int 0 as a placeholder
        board = [([0] * mode.cols) for row in range(mode.rows)]
        for item in mode.blocks:
            row, col = mode.getCell(item.x, item.y)
            board[row][col] = item
        return board

    #creates the program list!
    def createProgram(mode):
        board = mode.createBoard()
        iterator = 0
        prelimProgramList = []
        saveIterator  = 0
        for row in board:
            for col in row:
                if type(col) ==  type(StartBlock(mode)):
                    print('True')
                    saveIterator  = iterator
            iterator += 1
            prelimProgramList = board[saveIterator]
        programList = []
        for item in prelimProgramList:
            if item != 0:
                programList.append(item)
        return programList

    #returns a tuple of len 4 of the bounding x and y  coordinates
    def getCellBounds(mode, row, col):
        columnWidth = mode.width / mode.cols
        rowHeight = mode.height / mode.rows
        x0 =  col * columnWidth
        x1 = (col+1) * columnWidth
        y0 = row * rowHeight
        y1 = (row+1) * rowHeight
        return (x0, x1, y0, y1)

    #returns the center of the cell
    def getCellCenter(mode, row, col):
        x0, x1, y0, y1  = mode.getCellBounds(row, col) 
        centerX = (x0 + x1)/2
        centerY = (y0 + y1)/2
        return (centerX, centerY)

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
        
        elif event.key == 'b':
            mode.blocks = mode.connect(BrightnessBlock(mode.width/2, \
                mode.height/2, mode), mode.blocks)

        elif event.key == 'f':
            mode.blocks = mode.connect(ForBlock(mode.width/2, \
                mode.height/2, mode), mode.blocks)

        elif  event.key == 'i':
            mode.blocks =  mode.connect(IfBlock(mode.width/2,\
                mode.height/2, mode), mode.blocks)

    def mousePressed(mode, event):
        #this is where the code that will handle the 'compiling will go'
        print(f'x: {event.x}, y: {event.y}')
        if mode.compileButton.touches(event.x, event.y):
            mode.compileButton.compileCode(mode.createProgram())

        for item in mode.blocks:
            if isinstance(item, NeopixelBlock):
                if item.inLed(event.x, event.y):
                    item.changeColor(item.getLed(event.x, event.y))
            if isinstance(item, SpeakerBlock):
                if item.inNote(event.x, event.y):
                    item.changeTone()
            if isinstance(item, BrightnessBlock):
                if item.inNumberBounds(event.x, event.y):
                    item.changeBrightness()
            if isinstance(item, IfBlock):
                if item.inChangeColorBounds(event.x, event.y):
                    item.changeIf()
                item.doBlockSpecificStuff(event.x, event.y)
            if isinstance(item, ForBlock):
                if item.inChangeColorBounds(event.x, event.y):
                    item.increaseLoops()
                item.doBlockSpecificStuff(event.x, event.y)

    def mouseReleased(mode, event):
        for item in mode.blocks:
            if type(item) == type(IfBlock(1,1,mode)):
                for otherBlock in mode.blocks:
                     if type(otherBlock) != type(IfBlock(1,1,mode)):
                         if item.inBounds(otherBlock.x, otherBlock.y):
                            item.addBlock(otherBlock)
                            mode.blocks.remove(otherBlock)
            if type(item) == type(ForBlock(1,1,mode)):
                for otherBlock in mode.blocks:
                     if type(otherBlock) != type(ForBlock(1,1,mode)):
                         if item.inBounds(otherBlock.x, otherBlock.y):
                            item.addBlock(otherBlock)
                            mode.blocks.remove(otherBlock)
        
    def mouseDragged(mode, event):
        for item in mode.blocks:
            if item.inBounds(event.x, event.y):
                    row, col = mode.getCell(event.x, event.y)
                    x, y = mode.getCellCenter(row,  col)
                    item.move(x,y)

    def redrawAll(mode, canvas ):
        canvas.create_image(mode.width/2, mode.height/2, image = \
            ImageTk.PhotoImage(mode.background))
        mode.compileButton.draw(canvas)

        for item  in mode.blocks:
            item.draw(canvas)

def runCircuitPlaygroundGUI():
    CircuitPlaygroundGUI(width = 1320, height = 800)

runCircuitPlaygroundGUI()