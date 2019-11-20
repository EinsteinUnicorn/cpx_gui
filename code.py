import time
import board
 
# For Trinket M0, Gemma M0, ItsyBitsy M0 Express and ItsyBitsy M4 Express
#import adafruit_dotstar
#led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
# For Feather M0 Express, Metro M0 Express, Metro M4 Express and Circuit Playground Express
import neopixel

while True:
    #i = (i + 1) % 256  # run from 0 to 255
    neopixel.NeoPixel(board.NEOPIXEL, 10).fill(255)
    #time.sleep(0.1)