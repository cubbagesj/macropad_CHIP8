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
import random
import board
import displayio
import chip8_tools
from adafruit_macropad import MacroPad

# Initializations
macropad = MacroPad()

# Read in the list of ROMs and let user select one using the encoder
with open('roms.lst','r') as file:
    roms = [line.strip() for line in file]

text_lines = macropad.display_text(title = "Select ROM")
rom_selected = False
encoder = 1

while rom_selected != True:
    text_lines[0].text = ""
    text_lines[1].text = roms[macropad.encoder % len(roms)]
    if encoder != macropad.encoder:
        text_lines[1].text = roms[macropad.encoder % len(roms)]
        encoder = macropad.encoder
        text_lines.show()
    if macropad.encoder_switch:
        rom_selected = True
        romfile = roms[macropad.encoder % len(roms)] + '.ch8'
    time.sleep(.5)

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

# Stack - Make it unlimited for now
stack = []

# Timers
delay_timer = 0
sound_timer = 0
time_now = time.monotonic()

# Registers
#    sixteen 8 bit registers V0-VF
#    sixteen bit index register
#    Stack Pointer
regs = [0] * 16
index_reg = 0

# Program counter - initialize to 0x200 since that is where most ROMS load
pc = 0x200

# Flags for the keyboard
key_pressed = False             # Flag for keypress
key_value = 0xFF                # FF indicates no key press in buffer

# Debug - If debug flag is set, can single step instructions using the 
# encoder, each click executes one instruction and then prints values 
# of some of the registers

debug = False
encoder = 0


#*********************************************
# 
# Initialization complete - Now setup the
# interpreter

# Load font into memory at 0x50
memory = chip8_tools.load_font(memory)

# Read ROM file into memory at 0x200
[memory, end_addr] = chip8_tools.read_rom(memory, 
                                          romname = romfile, 
                                          start_addr = 0x200)
print("end address: %#x" % end_addr)


# Main program loop
#
#   The main loop will control the flow of the interpreter and handle the
#   board stuff and timing as well as running the CHIP 8 interpreter 
#

# Continually loop but stop if for some reason the pc goes beyond the end of the
# loaded ROM. This shouldn't happen but check anyway
while pc <= end_addr:

    # Debug  - Single step if true
    if debug:
        # Debug flag set so print register values
        print("Addr: {0:#x} : {1:#x}".format(pc,(memory[pc]<<8) + memory[pc+1]))
        chip8_tools.dissasemble(memory, pc, pc)
        print("I: {0:#x}  DT: {1:d}  ST:{2:d}".format(index_reg, delay_timer, sound_timer))
        for x in range(4):
            for y in range(4):
                print("V{0:X}:{1} ".format(y+x*4,regs[y+x*4]),end="") 
            print("")
        print("")
        while encoder == macropad.encoder:
            time.sleep(0.2)
        encoder = macropad.encoder

    # Look for keypress
    key_event = macropad.keys.events.get()
    if key_event and key_event.pressed:
        print("Key pressed: {}".format(key_event.key_number))
        key_value_raw = key_event.key_number
        key_pressed = True
        # Keyboard remapping
        if key_value_raw <= 9:
            key_value = key_value_raw + 1
        elif key_value_raw == 10:
            key_value = 0
        elif key_value_raw == 11:
            key_value = 11
    elif key_event and key_event.released:
        if key_event.key_number == key_value_raw:
            print("Key released: {}".format(key_event.key_number))
            key_pressed = True
            key_value = 0xFF
        else:
            pass


    # execute chip8 loop

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
            if inst_N == 0:                 # CLS
                # Clear screen
                bitmap.fill(0)
            elif inst_N == 0xE:             # RET
                # Return from subroutine
                pc = stack.pop()
            else:
                pass
        else:
            pass

    elif inst_type == 1:                    # JP nnn
        # Jump to location nnn
        pc = inst_NNN

    elif inst_type == 2:                    # CALL nnn
        # Call subroutine at nnn
        stack.append(pc)
        pc = inst_NNN

    elif inst_type == 3:                    # SE Vx, nn
        # Skip next instruction if Vx == nn
        if (regs[inst_X] == inst_NN):
            pc = pc + 2
        else:
            pass

    elif inst_type == 4:                    # SNE Vx, nn
        # Skip next instruction if Vx != nn
        if (regs[inst_X] != inst_NN):
            pc = pc+2
        else:
            pass

    elif inst_type == 5:                    # SE Vx, Vy
        # Skip next instruction if Vx = Vy
        if regs[inst_X] == regs[inst_Y]:
            pc = pc + 2
        else:
            pass

    elif inst_type == 6:                    # LD nn
        # Set Vx = nn
        regs[inst_X] = inst_NN

    elif inst_type == 7:                    # ADD Vx, nn
        # Set Vx = Vx + nn
        regs[inst_X] += inst_NN
        regs[inst_X] &= 0xFF                # Memory is only 1 byte

    elif inst_type == 8:
        if inst_N == 0:                    # LD Vx, Vy
            regs[inst_X] = regs[inst_Y]
        elif inst_N == 1:                  # OR Vx, Vy
            regs[inst_X] |= regs[inst_Y]
        elif inst_N == 2:                   # AND Vx, Vy
            regs[inst_X] &= regs[inst_Y]
        elif inst_N == 3:                   # XOR Vx, Vy
            regs[inst_X] ^= regs[inst_Y]
        elif inst_N == 4:                   # ADD Vx, Vy
            regs[inst_X] += regs[inst_Y]
            if regs[inst_X] > 255:
                regs[0xF] = 1
                regs[inst_X] &= 0xFF
            else:
                regs[0xF] = 0
        elif inst_N == 5:                   # SUB Vx, Vy
            if regs[inst_X] > regs[inst_Y]:
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] -= regs[inst_Y]
        elif inst_N == 6:                   # SHR Vx
            if (regs[inst_X] & 0x1) == 1:
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] = regs[inst_X] >> 1
        elif inst_N == 7:                   # SUBN Vx, Vy
            if (regs[inst_Y] > regs[inst_X]):
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] -= regs[inst_Y]
        elif inst_N == 0xE:                 # SHL Vx
            if (regs[inst_X] & 0x80) == 1:
                regs[0xF] = 1
            else:
                regs[0xF] = 0
            regs[inst_X] = regs[inst_X] << 1
            regs[inst_X] &= 0xFF
        else:
            pass

    elif inst_type == 0x9:                  # SNE Vx, Vy
        # Skip next instruction if Vx != Vy
        if regs[inst_X] != regs[inst_Y]:
            pc = pc +2
        else:
            pass

    elif inst_type == 0xA:          # LD I, addr
        index_reg = inst_NNN

    elif inst_type == 0xB:          # JP V0, addr
        pc = regs[0] + inst_NNN

    elif inst_type == 0xC:          # RND Vx, byte
        # Set Vx = random AND nn
        regs[inst_X] = random.randrange(256) & inst_NN


    elif inst_type == 0xD:          # DRW Vx, Vy, nibble
        # Set the x and y coords
        x_coord = regs[inst_X] % 64
        y_coord = regs[inst_Y] % 32

        # Clear the collision detection flag
        regs[0xF] = 0

        # Loop through bytes to display
        #  - The macropad display is 128x64 so we need to scale up
        #    the image and turn each pixel into a block of 4 pixels
        for y in range(inst_N):
            pixel = memory[index_reg + y]
            for x in range(8):
                if (pixel & (0x80 >> x)) != 0:
                    if bitmap[((x_coord + x)*2)%display.width,
                              ((y_coord + y)*2)%display.height] == 1:
                        regs[0xF] = 1
                    bitmap[((x_coord + x)*2)%display.width,
                           ((y_coord + y)*2)%display.height] ^= 1
                    bitmap[((x_coord + x)*2+1)%display.width,
                           ((y_coord + y)*2)%display.height] ^= 1
                    bitmap[((x_coord + x)*2)%display.width,
                           ((y_coord + y)*2+1)%display.height] ^= 1
                    bitmap[((x_coord + x)*2+1)%display.width,
                           ((y_coord + y)*2+1)%display.height] ^= 1

    elif inst_type == 0xE:   
        if inst_NN == 0x9E:         # SKP Vx
            # Skip next instruction if key with value in Vx is pressed
            if key_value == regs[inst_X]:
                pc = pc +2
            else:
                pass
        elif inst_NN == 0xA1:       # SKNP Vx
            # Skip next instruction if key with value in Vx is not pressed
            if key_value != regs[inst_X]:
                pc = pc + 2
            else:
                pass

    elif inst_type == 0xF:
        if inst_NN == 0x07:         # LD Vx, DT
            # Value of delay time put in Vx
            regs[inst_X] = delay_timer
        elif inst_NN == 0x0A:       # LD Vx, k
            # Wait for a keypress and put value in Vx
            if key_pressed == False:
                pc = pc - 2
            else:
                regs[inst_X] = key_value
        elif inst_NN == 0x15:       # LD DT, Vx
            # put value in Vx into delay timer
            delay_timer = regs[inst_X]
        elif inst_NN == 0x18:       # LD ST, Vx
            # put value in Vx into sound timer
            sound_timer = regs[inst_X]
        elif inst_NN == 0x1E:        # ADD I, Vx
            index_reg = index_reg + regs[inst_X]
        elif inst_NN == 0x29:        # LD F, Vx
            # Set I to the location of the sprite for Vx
            index_reg = 0x50 + (5 * regs[inst_X])
        elif inst_NN == 0x33:        # LD B, Vx
            # Store BCD representation of Vx in locs I, I+1, I+2
            memory[index_reg + 2] = regs[inst_X] % 10
            memory[index_reg + 1] = int(regs[inst_X]/10) % 10
            memory[index_reg] = int(regs[inst_X]/100) % 10
        elif inst_NN == 0x55:       # LD [I], Vx
            # Store values of V0 to Vx in memory starting at I
            for x in range(inst_X+1):
                memory[index_reg+x] = regs[x]
        elif inst_NN == 0x65:       # LD Vx, [I]
            #Read registers V0 to Vx from memory starting at I
            for x in range(inst_X+1):
                regs[x] = memory[index_reg + x]
        else:
            pass 

    # Do timer stuff
    # Timers get decremented if greater than zero every 1/60 s
    #
    if time.monotonic() - time_now >= 0.01667:
        if delay_timer > 0:
            delay_timer -= 1
        if sound_timer > 0:
            sound_timer -= 1
     #       macropad.play_tone(292,0.01)
        time_now = time.monotonic()

    # Wait to slow down loop
    time.sleep(1/700)
