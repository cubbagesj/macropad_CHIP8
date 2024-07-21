# chip8_tools.py
#
# This is a collection of helper functions for the CHIP8 interpreter
#

# Imports
#
import time

def load_font(memory = []):
    """ This routine loads the font into memory starting at address 0x50 as 
    is typical for CHIP8 programs
    """

    # Initializations


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

    # Return memory with font loaded
    return memory

def read_rom(memory, romname = "IBM Logo.ch8", start_addr=0x200):
    # Function to read a rom into memory starting at address 0x200
    #
    print("ROM: %s, loading at address: %#x" %(romname, start_addr))
    with open(romname, "rb") as f:
        while (byte := f.read(1)):
            memory[start_addr] = list(byte)[0]
            start_addr += 1

    print("End address: %#x" % (start_addr-1))
    return [memory, start_addr-1] 

def dissasemble(memory, start_addr, end_addr):
    # Function to create an assembly code listing of a block of memory
    # defined by the start and end addresses

    for pc in range(start_addr, end_addr+2, 2):
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
                elif inst_N == 0xE:     # RET
                    print("%#x    RET" % (pc-2)) 
                else:
                    print("%#x    NOP    %#x" %(pc-2, (inst_high << 8) + inst_low))
            else:
                pass
        elif inst_type == 1:        # JMP
            print("%#x    JMP    %#x" % (pc-2, inst_NNN))

        elif inst_type == 2:        # CALL
            print("%#x    CALL   %#x" % (pc-2, inst_NNN))

        elif inst_type == 3:
            print("%#x    SE    V%d, %d" % (pc-2, inst_X, inst_NN))

        elif inst_type == 4:
            print("%#x    SNE   V%d, %d" % (pc-2, inst_X, inst_NN))

        elif inst_type == 5:
            print("%#x    SE    V%d, V%d" % (pc-2, inst_X, inst_Y))

        elif inst_type == 6:
            print("%#x    LD    V%d, %#x" % (pc-2, inst_X, inst_NN))

        elif inst_type == 7:
            print("%#x    ADD    V%d, %#x" % (pc-2, inst_X, inst_NN))

        elif inst_type == 8:
            if inst_N == 0:             # LD Vx, Vy
                print("%#x    LD    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 1:           # OR Vx, Vy
                print("%#x    OR    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 2:           # AND Vx, Vy
                print("%#x    AND    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 3:           # XOR Vx, Vy
                print("%#x    XOR    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 4:           # ADD Vx, Vy
                print("%#x    ADD    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 5:           # SUB Vx, Vy
                print("%#x    SUB    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 6:           # SHR Vx
                print("%#x    SHR    V%d" % (pc-2, inst_X))
            elif inst_N == 7:           # SUBN Vx, Vy
                print("%#x    SUBN    V%d, V%d" % (pc-2, inst_X, inst_Y))
            elif inst_N == 0xE:        # SHL Vx
                print("%#x    SHL    V%d" % (pc-2, inst_X))

        elif inst_type == 0x9:          # SNE Vx, Vy
            print("%#x    SNE    V%d, V%d" % (pc-2, inst_X, inst_Y))

        elif inst_type == 0xA:          # LD I, addr
            print("%#x    LD    I, %#x" % (pc-2, inst_NNN))

        elif inst_type == 0xB:          # JP V0, addr
            print("%#x    JP    I, %#x" % (pc-2, inst_NNN))

        elif inst_type == 0xd:
            print("%#x    DRW    V%d, V%d, %d" % (pc-2, inst_X, inst_Y, inst_N))

        elif inst_type == 0xA:
            print("%#x    LD    I, %#x" % (pc-2, inst_NNN))

        else:
           print("%#x    NOP    %#x" %(pc-2, (inst_high << 8) + inst_low))
           pass 

