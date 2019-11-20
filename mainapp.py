from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random

class CircuitPlaygroundGUI(ModalApp):
    def appStarted(app):
        app.splash =  SplashMode()
        app.program = ProgramMode()
        app.compile = CompileMode()
        app.help =  HelpMode()

class SpashMode(Mode):
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
    def mousePressed(mode, event):
        #this is where the code that will handle the 'compiling will go'
        #if compilebutton.touches(event.x, event.y):
        mode.app.setActiveMode(mode.app.compile)
    def redrawAll(mode, canvas ):
        #draw the background
        pass

def runCircuitPlaygroundGUI():
    CircuitPlargroundGUI()

runCircuitPlaygroundGUI()