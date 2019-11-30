import time
import board 
import neopixel
from adafruit_circuitplayground.express import cpx
while True:

	cpx.pixels[0]= (0, 255, 0)
	cpx.pixels[1]= (0, 255, 0)
	cpx.pixels[2]= (0, 255, 0)
	cpx.pixels[3]= (255, 0, 0)
	cpx.pixels[4]= (255, 0, 0)
	cpx.pixels[5]= (255, 0, 0)
	cpx.pixels[6]= (255, 0, 0)
	cpx.pixels[7]= (255, 0, 0)
	cpx.pixels[8]= (255, 0, 0)
	cpx.pixels[9]= (255, 0, 0)
	cpx.play_tone(349.3, .5)
	if cpx.button_a:
		cpx.pixels[0]= (255, 0, 0)
		cpx.pixels[1]= (255, 0, 0)
		cpx.pixels[2]= (255, 0, 0)
		cpx.pixels[3]= (255, 0, 0)
		cpx.pixels[4]= (255, 0, 0)
		cpx.pixels[5]= (255, 0, 0)
		cpx.pixels[6]= (255, 0, 0)
		cpx.pixels[7]= (255, 0, 0)
		cpx.pixels[8]= (255, 0, 0)
		cpx.pixels[9]= (255, 0, 0)