# chip8.py
#
#  This is an attempt to create a CHIP8 interpreter in circuitpython
#  for the RP2040 on the Adafruit Macropad
#
#  It is a project to learn circuitpython and the RP2040 
#
#  Started - 7/18/2024
#

# Imports
#
import time
#import board

# Initializations

# Memory - The CHIP8 has 4K (4096) bytes of RAM
#          Implement this as a list with 4096 elements initialized to zeros
#
memory = [0] * 4096

# Font - Use typical font and load starting at memory location 0x50
memory[0x50] = 0xF0
memory[0x51] = 0x90
memory[0x52] = 0x90
memory[0x53] = 0x90
memory[0x54] = 0xF0

memory[0x55] = 0x20
memory[0x56] = 0x60
memory[0x57] = 0x20
memory[0x58] = 0x20
memory[0x59] = 0x70

memory[0x5A] = 0xF0
memory[0x5B] = 0x10
memory[0x5C] = 0xF0
memory[0x5D] = 0x80
memory[0x5E] = 0xF0

memory[0x5F] = 0xF0
memory[0x60] = 0x10
memory[0x61] = 0xF0
memory[0x62] = 0x10
memory[0x63] = 0xF0

memory[0x64] = 0x90
memory[0x65] = 0x90
memory[0x66] = 0xF0
memory[0x67] = 0x10
memory[0x68] = 0x10

memory[0x69] = 0xF0
memory[0x6A] = 0x80
memory[0x6B] = 0xF0
memory[0x6C] = 0x10
memory[0x6D] = 0xF0

memory[0x6E] = 0xF0
memory[0x6F] = 0x80
memory[0x70] = 0xF0
memory[0x71] = 0x90
memory[0x72] = 0xF0

memory[0x73] = 0xF0
memory[0x74] = 0x10
memory[0x75] = 0x20
memory[0x76] = 0x40
memory[0x77] = 0x40

memory[0x78] = 0xF0
memory[0x79] = 0x90
memory[0x7A] = 0xF0
memory[0x7B] = 0x90
memory[0x7C] = 0xF0

memory[0x7D] = 0xF0
memory[0x7E] = 0x90
memory[0x7F] = 0xF0
memory[0x80] = 0x10
memory[0x81] = 0xF0

memory[0x82] = 0xF0
memory[0x83] = 0x90
memory[0x84] = 0xF0
memory[0x85] = 0x90
memory[0x86] = 0x90

memory[0x87] = 0xE0
memory[0x88] = 0x90
memory[0x89] = 0xE0
memory[0x8A] = 0x90
memory[0x8B] = 0xE0

memory[0x8C] = 0xF0
memory[0x8D] = 0x80
memory[0x8E] = 0x80
memory[0x8F] = 0x80
memory[0x90] = 0xF0

memory[0x91] = 0xE0
memory[0x92] = 0x90
memory[0x93] = 0x90
memory[0x94] = 0x90
memory[0x95] = 0xE0

memory[0x96] = 0xF0
memory[0x97] = 0x80
memory[0x98] = 0xF0
memory[0x99] = 0x80
memory[0x9A] = 0xF0

memory[0x9B] = 0xF0
memory[0x9C] = 0x80
memory[0x9D] = 0xF0
memory[0x9E] = 0x80
memory[0x9F] = 0x80

# Stack - Make it unlimited for now
stack = []

# Timers
delay_timer = 60
sound_timer = 60

# Registers
#    sixteen 8 bit registers V0-VF
#    sixteen bit index register
#    Stack Pointer
regs = [0] * 16
index_reg = 0

# Program counter - initialize to 0x200
pc = 0x200

# Function definitions
#
def read_rom(romname = "IBM Logo.ch8", startaddr=0x200):
    # Function to read a rom into memory starting at address 0x200
    #
    with open(romname, "rb") as f:
        while (byte := f.read(1)):
            memory[startaddr] = list(byte)[0]
            startaddr += 1

# Main loop
#   Fetch/decode/execute
#

# Read in ROM file
read_rom("IBM Logo.ch8", 0x200)

# Simply cycle through memory and echo 
while pc < 4096:

# Fetch instruction at PC

    inst = memory[pc]

    # echo instruction to screen
    print("byte = ", hex(pc))
    print("value = ", hex(inst))

    pc = pc + 1
    time.sleep(.01)


