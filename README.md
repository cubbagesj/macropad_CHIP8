# CHIP8 for Adafruit macropad

This is an implementation of the CHIP8 for the Adafruit macropad.  It is
a personal development project to learn how to program and emulator/interpreter
and also learn the ins and outs of the RP2040 and the macropad

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
