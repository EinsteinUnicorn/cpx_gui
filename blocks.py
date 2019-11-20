class StartBlock(object):
    def __init__(self, isConnected):
        self.msg = """import time
import board 
import neopixel
while True:
"""
        self.isConnected = isConnected

    def __repr__(self):
        return self.msg

