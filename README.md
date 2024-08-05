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

  - ROM selector with encoder works
  - ROMS run - but with some issues (see below)

## Main Issues
  - Seems to be some issues with collision detection on screen especially on
    games like Breakout and Tetris, but also a bunch of others.  Some work
    fine. Turns out this might be issues with the actual ROMS.  I single
    stepped through Tetris and the end behaviour seems to be what is programmed
  - Have too reboot to select new game
  - Some games seem to not get keyboard input correctly or possibly might use
    keys that I do not have
  - Not sure of timing loop

 ## Use

 Copy the code.py, chip8-tools.py and the .ch8 ROM files directory to the
 macropad. Then use the encoder to select a ROM and press the encoder to start
 it

 ## Operation

 The code.py file sets up the enviroment and loads the font into memory, then
 reads in the ROM file and then starts looping.  The sleep() command at the end
 of the loop slows things down to be reasonable.  Still trying to figure out
 the correct timimg.

 The chip8_tools.py file has various helper functions including a dissasembler
 that prints out the assembly code from a ROM file

 ## Thoughts
It appears that some of the ROMS are not as polished as others.  I also have no
way to judge the speed of the emulation.  Somes games seem fine while others
seem to run fast.  One idea would be to use the encoder wheel to adjust the
loop speed during a game.

I want to implement a way to break out of the loop and return to the ROM
selection screen.  Maybe by pressing the encoder button

 ## References
 I used the following sites to learn about how CHIP-8 works and how to
 implement it:

http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#Dxyn
https://multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
https://tobiasvl.github.io/blog/write-a-chip-8-emulator/

And ROMS are from:
https://github.com/loktar00/chip8/tree/master
