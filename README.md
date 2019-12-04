# Fake Make Code - A Lite Circuit Playground Express GUI
 
# Description: 
This project compiles visual representations of code into actual python 	that is uploaded to the Adafruit Circuit Playground Express. Users can program the	lights, speaker, and even utilize various sensors on the board. 
# Running the project:
Run the mainapp.py file. The project assumes a Mac OS File system. If this is run	on a windows machine, the path to the micro controller board will need to be modified in the compiler class.
# Libraries:	
All of the libraries needed to actually run the code are built into the 		microcontroller. It is very important to upload the latest firmware onto the microcontroller. Documentation about this can be found here(with a link to the firmware and how to install it ): https://learn.adafruit.com/adafruit-circuit-playground-express/updating-the-bootloader

# Commands:
There are no shortcut commands, however here is a list of general commands for 
use in programming mode
	
	'b' - adds a brightness block
	'r' - removes the block that was last added (note if it was added to an if/for, 	it will remove the if/for too.
	'i' - adds an if block
	'f' - adds a for block
	'd' - adds a delay block
	's' - adds a speaker block
	'l' - adds a light block

