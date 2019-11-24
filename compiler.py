from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
#from mainapp import  *
import copy

class CompileButton(object):

    def __init__(self, mode):
        self.mode = mode
        self.x, self.y =  1230, 60
        self.image = self.mode.loadImage('compile_button.png')
    
    def touches(self, x, y):
        if x >= 1260 and x <= 1274 and \
            y >= 10 and y <= 46:
            return  True
        return False

        
    def compileCode(self, programList):
        Compiler(programList).fileWrite()

    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.image))

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