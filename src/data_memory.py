import configparser
import struct
import re

from register_file import registers

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
size = 50 # units (not unit of measure)

data_memory = {'0x' + struct.pack('>I', i).hex().zfill(10): hex(0).zfill(word_lenght)[:word_lenght - 2]  for i in range(size)} # memory stack

c = 0
sp = config['Registers']['SP']

# clear memory
def clear_memory():
    global data_memory
    
    data_memory = {'0x' + struct.pack('>I', i).hex().zfill(10): hex(0).zfill(word_lenght)[:word_lenght - 2]  for i in range(size)} # memory stack

# check errors (ADD and SUB) in asm code
def check_op_error(instr):
    register_pattern = r'r([0-9]|1[0-3])'

    if not re.findall(register_pattern, instr[2]):
        return False

    return True

# write res back in register
def write_back(alu_res, Rd):
    registers[Rd] = alu_res

# write res in memory
def write_data(alu_res):
    pass

# convert asm code in binary code
def asm_to_bin(instr):
    if instr[0] == 'ADD' or instr[0] == 'SUB':
        # check asm error coding
        if check_op_error(instr):
            cond = '1110'
            op = '00'

            # funct
            i = '0' if instr[3][0] == 'r' else '1'
            cmd = '0100' if instr[0] == 'ADD' else '0010'
            s = '0'

            Rn = bin(int(instr[2][1:])).zfill(4)
            Rd = bin(int(instr[1][1:])).zfill(4)

            # Src2
            if i == '0':
                shamt5 = '00000'
                sh = '00'
                Rm = bin(int(instr[3][1:])).zfill(4)

                list_instr = [cond, op, i, cmd, s, Rn, Rd, shamt5, sh, '0', Rm]
            else:
                rot = '0'.zfill(4)
                imm8 = bin(int(instr[3])).zfill(8)

                list_instr = [cond, op, i, cmd, s, Rn, Rd, rot, imm8]
        else:
            print('Error: ASM (op) code is wrong')

            return 0
    elif instr[0] == 'LDR':
        pass
    elif instr[0] == 'STR':
        pass
    else:
        print('Error: Instruction not recognized')

        return 0

    return list_instr

# convert instruction in binary format and load in memory
def load_memory(instr):
    bin_data = asm_to_bin(instr)

    if not 0:
        global c, sp

        data_memory[sp] = bin_data

        c += 1

        sp = '0x' + struct.pack('>I', c).hex().zfill(10)

        config.set('Registers', 'SP', sp)

        with open('src/config.ini', 'w') as config_file:
            config.write(config_file)
    
# read instruction and load in memory
def load_instr():
    instrs = []

    # read asm code
    with open('src/asm_code.txt') as f:
        code = f.readlines()

        for instr in code:
            instrs.append(instr.split())
    
    # load in memory
    for instr in instrs:
        load_memory(instr)

