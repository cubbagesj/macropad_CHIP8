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
import board
import displayio

# Initializations

# Setup Display on macropad
#
display = board.DISPLAY

# Create bitmap with 2 colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group


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

# Program counter - initialize to 0x200 since that is where most ROMS load
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
    return startaddr -1

# Read in ROM file into memory at 0x200
end_addr = read_rom("Zero Demo.ch8", 0x200)
print("end address: %#x" % end_addr)

# Main loop
#   Fetch/decode/execute
#

# Simply cycle through memory and echo 
while pc <= end_addr:

# Fetch instruction at PC

    inst_high = memory[pc]
    inst_low = memory[pc + 1]

# Increment the program counter
    pc = pc + 2

# Break out instruction values here to use later
    inst_type = (inst_high & 0xF0) >> 4        # First nibble
    inst_X = inst_high & 0x0F                  # Second nibble
    inst_Y = (inst_low & 0xF0) >> 4            # Third Nibble
    inst_N = inst_low & 0x0F                   # Fourth Nibble
    inst_NN = inst_low                         # Third & Fourth Nibbles
    inst_NNN = (inst_X << 8) + inst_low        # Second, Third Fouth nibbles

    # Decode instruction type 
    if inst_type == 0:
        if inst_Y == 0xE:
            if inst_N == 0:         # CLS
                print("%#x    CLS" % (pc-2))
                bitmap.fill(0)
            elif inst_N == 0xE:
                pc = stack.pop()
            else:
                pass
        else:
            pass
    elif inst_type == 1:        # JMP
        print("%#x    JMP    %#x" % (pc-2, inst_NNN))
        pc = inst_NNN

    elif inst_type == 2:        # CALL
        print("%#x    CALL   %#x" % (pc-2, inst_NNN))
        stack.append(pc)
        pc = inst_NNN

    elif inst_type == 3:
        print("%#x    SE    V%d, %d" % (pc-2, inst_X, inst_NN))
        if (regs[inst_X] == inst_NN):
            pc = pc + 2
        else:
            pass

    elif inst_type == 4:
        print("%#x    SNE   V%d, %d" % (pc-2, inst_X, inst_NN))
        if (regs[inst_X] != inst_NN):
            pc = pc+2
        else:
            pass

    elif inst_type == 5:
        print("%#x    SE    V%d, V%d" % (pc-2, inst_X, inst_Y))
        if regs[inst_X] == regs[inst_Y]:
            pc = pc + 2
        else:
            pass

    elif inst_type == 6:
        print("%#x    LD    V%d, %#x" % (pc-2, inst_X, inst_NN))
        regs[inst_X] = inst_NN

    elif inst_type == 7:
        print("%#x    ADD    V%d, %#x" % (pc-2, inst_X, inst_NN))
        regs[inst_X] += inst_NN

    elif inst_type == 8:
        if inst_N == 0:             # LD Vx, Vy
            regs[inst_X] = regs[inst_Y]
        elif inst_N == 1:           # OR Vx, Vy
            regs[inst_X] |= regs[inst_Y]
        elif inst_N == 2:           # AND Vx, Vy
            regs[inst_X] &= regs[inst_Y]
        elif inst_N == 3:           # XOR Vx, Vy
            regs[inst_X] ^= regs[inst_Y]
        elif inst_N == 4:           # ADD Vx, Vy
            regs[inst_X] += regs[inst_Y]
            if regs[inst_X] > 255:
                regs[0xF] = 1
                regs[inst_X] &= 0xFF
        elif inst_N == 5:           # SUB Vx, Vy
            if regs[inst_X] > regs[inst_Y]:
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] -= regs[inst_Y]
        elif inst_N == 6:           # SHR Vx
            if (regs[inst_X] & 0x1) == 1:
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] = regs[inst_X] >> 1
        elif inst_N == 7:           # SUBN Vx, Vy
            if (regs[inst_Y] > regs[inst_X]):
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] -= regs[inst_Y]
        elif inst_N == 0xE:        # SHL Vx
            if (regs[inst_X] & 0x80) == 1:
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] = regs[inst_X] << 1
            regs[inst_X] &= 0xFF
        else:
            pass

    elif inst_type == 0x9:
        if regs[inst_X] != regs[inst_Y]:
            pc = pc +2
        else:
            pass

    elif inst_type == 0xA:          # LD I, addr
        index_reg = inst_NNN

    elif inst_type == 0xB:          # JP V0, addr
        pc = regs[0] + inst_NNN

    elif inst_type == 0xd:
        print("%#x    DRW    V%d, V%d, %d" % (pc-2, inst_X, inst_Y, inst_N))
        # Set the x and y coords
        x_coord = regs[inst_X] % 64
        y_coord = regs[inst_Y] % 32

        # Clear the collision detection flag
        regs[0xF] = 0

        # Loop through bytes to display
        #  - Currently does not do collision detection
        #  - The macropad display is 128x64 so we need to scale up
        #    the image and turn each pixel into a block of 4 pixels
        for i in range(inst_N):
            value = memory[index_reg + i]
            for x in range(8):
                if (value & (0x80 >> x)) != 0:
                    bitmap[(x_coord + x)*2, (y_coord + i)*2] ^= 1
                    bitmap[(x_coord + x)*2+1, (y_coord + i)*2] ^= 1
                    bitmap[(x_coord + x)*2, (y_coord + i)*2+1] ^= 1
                    bitmap[(x_coord + x)*2+1, (y_coord + i)*2+1] ^= 1

    elif inst_type == 0xA:
        print("%#x    LD    I, %#x" % (pc-2, inst_NNN))
        index_reg = inst_NNN

    else:
       pass 

