from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import copy

class CompileButton(object):

    def __init__(self, x, y):
        self.x, self.y =  x,y
    
    def touches(self, x, y):
        #TODO  if the cursor is in the bounds of the box, compile
        pass

    def draw(self, canvas):
        #TODO draw the image i created
        pass

class Compiler(object):

    def __init__(self, programList):
        #program is a list of the STR representations of the objects
        self.programList = copy.copy(programList)
    
    def programListToString(self):
        if self.programList == []:
            return ""
        else:
            s = ""
            for item in self.programList:
                s += item.toString()
            return s

    def fileWrite(self):
        if self.programList ==  []:
            print("There's nothing to write")
        else:
            file = open('/Volumes/CIRCUITPY/code.py', 'w')
            try:
                file.write(self.programListToString())
            finally:
                file.close()