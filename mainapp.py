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
    
    def maxItemLength(mode, a):
        maxLen = 0
        rows = len(a)
        cols = len(a[0])
        for row in range(rows):
            for col in range(cols):
                maxLen = max(maxLen, len(str(a[row][col])))
        return maxLen
    
    def print2dList(mode, a):
        if (a == []):
            # So we don't crash accessing a[0]
            print([])
            return
        rows = len(a)
        cols = len(a[0])
        fieldWidth = mode.maxItemLength(a)
        print("[ ", end="")
        for row in range(rows):
            if (row > 0): print("\n  ", end="")
            print("[ ", end="")
            for col in range(cols):
                if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
                formatSpec = "%" + str(fieldWidth) + "s"
                print(formatSpec % str(a[row][col]), end="")
            print(" ]", end="")
        print("]")
    
    def createBoard(mode):
        #the int 0 as a placeholder
        board = [([0] * mode.cols) for row in range(mode.rows)]
        for item in mode.blocks:
            row, col = mode.getCell(item.x, item.y)
            board[row][col] = item
        #mode.print2dList(board)
        return board

    #creates the program list!
    def createProgram(mode):
        board = mode.createBoard()
        iterator = 0
        prelimProgramList = []
        saveIterator  = 0
        for row in board:
            for col in row:
                #if col != 0:
                    #print(col)
                    #print(type(col))
                    #print(type(StartBlock(mode)))
                if type(col) ==  type(StartBlock(mode)):
                    print('True')
                    saveIterator  = iterator
            iterator += 1
            prelimProgramList = board[saveIterator]
        #print(prelimProgramList)
        programList = []
        for item in prelimProgramList:
            if item != 0:
                programList.append(item)
        #print(programList)
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
        elif event.key == 'f':
            #add the for block
            pass 

        elif  event.key == 'i':
            mode.blocks =  mode.connect(IfButtonBlock(mode.width/2,\
                mode.height/2, mode), mode.blocks)
        #add the up down left right keys to shift the blocks

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
        
    def mouseDragged(mode, event):
        
        for item in mode.blocks:
            if item.inBounds(event.x, event.y):
                    row, col = mode.getCell(event.x, event.y)
                    x, y = mode.getCellCenter(row,  col)
                    item.x = x
                    item.y = y

    def redrawAll(mode, canvas ):
        canvas.create_image(mode.width/2, mode.height/2, image = \
            ImageTk.PhotoImage(mode.background))
        mode.compileButton.draw(canvas)

        for item  in mode.blocks:
            item.draw(canvas)

def runCircuitPlaygroundGUI():
    CircuitPlaygroundGUI(width = 1320, height = 800)

runCircuitPlaygroundGUI()