# chip8_dissasembler.py
#
#  This is a modified version of the CHIP8 interprter that
#  just generates an assembly code listing of a ROM file
#
#  It is a project to learn circuitpython and the RP2040 
#

import chip8_tools

# Memory - The CHIP8 has 4K (4096) bytes of RAM
#          Implement this as a list with 4096 elements initialized to zeros
#
memory = [0] * 4096

memory = chip8_tools.load_font(memory)

[memory, endaddr] = chip8_tools.read_rom(memory, romname="Trip8 Demo.ch8")

chip8_tools.dissasemble(memory, 0x50,0x9F )
