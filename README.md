# CHIP-8 for Adafruit macropad

This is an implementation of the CHIP-8 for the Adafruit macropad.  It is
a personal development project to learn how to program and emulator/interpreter
and also learn the ins and outs of the RP2040 and the macropad

I chose the macropad because it has a monochrome display and a keypad.  The
display is 128 x 64 pixels, which is exactly twice the size of the 64 x 32
typical CHIP-8 display.  The typical CHIP-8 implementation had a 16 key keypad,
the macropad only has 12 keys (13 if you count the encoder switch) so hopefully
that won't be too much of an issue.

## What is CHIP-8 and why bring it to the macropad?
CHIP-8 was created in 1977 for the COSMAC VIP microcomputer as a simpler way to
make small programs using a hexadecimal keypad to enter instructions that
resembled machine code.  It was later ported to many other platforms including
to the hP48 calculators and there are a bunch of ROM images around that can be
used.

CHIP-8 is an easy way to get into emulator design since it is very simple design and
only has a small number of opcodes. So I thought it would be a good project to
use to learn the RP2040 and circuitpython.  Also I am kind of a sucker for
retro computers and other things.  I grew up on main frames and my first PC was
a TRS-80, I have replicas of the Altair 8800, PDP 11 and Kenbak 1. 

## Current status:
This is a work in progress, here is what works and what doesn't

 - The main code.py file gets copied to the macropad along with the various .ch8
ROM files.

- Currently the ROM that is run is hard coded into the code.py file near the
  top. Future plan is to implement a selection menu

  - The interperter implements all of the CHIP8 Opcodes (hopefully correctly
    but no gaurantees)

  - It runs some but not all of the ROMS

## Main Issues
 - Keypad mapping is off, the macropad has 4 fewer keys than most CHIP8
   implementations
 - Not sure if all opcodes are working

 ## Use

 Copy the code.py, chip8-tools.py and the .ch8 ROM files to the macropad. Edit
 the code.py to pick the correct ROM.

 ## Operation

 The code.py file sets up the enviroment and loads the font into memory, then
 reads in the ROM file and then starts looping.  The sleep() command at the end
 of the loop slows things down to be reasonable.  Still trying to figure out
 the correct timimg.

 The chip8_tools.py file has various helper functions including a dissasembler
 that prints out the assembly code from a ROM file
