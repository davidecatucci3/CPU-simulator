import configparser
import struct
import re

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
register_lenght = int(config['CPU settings']['register_lenght'])
size = 50 # units (not unit of measure)

data_memory = {'0x' + struct.pack('>I', i).hex().zfill(register_lenght): hex(0).zfill(word_lenght)[:word_lenght - 2]  for i in range(size)} # memory stack
data_memory['0x' + struct.pack('>I', 1).hex().zfill(register_lenght)] = '0x' + struct.pack('>I', 12).hex().zfill(register_lenght)
c = 0
sp = config['Registers']['SP']

# clear memory
def clear_memory():
    global data_memory
    
    data_memory = {'0x' + struct.pack('>I', i).hex().zfill(register_lenght): hex(0).zfill(word_lenght)[:word_lenght - 2]  for i in range(size)} # memory stack

# check errors (ADD and SUB) in asm code
def check_op_error(instr):
    register_pattern = r'r([0-9]|1[0-3])'

    if not re.findall(register_pattern, instr[2]):
        return False

    return True

# write res back in register
def write_back(alu_res, Rd):
    val = data_memory[alu_res]
 
    config.set('Registers', Rd, val)

    with open('src/config.ini', 'w') as config_file:
        config.write(config_file)

# write res in memory
def write_data(alu_res, Rd):
    val = config['Registers'][Rd]

    data_memory[alu_res] = val

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

            funct = [i, cmd, s]

            Rn = bin(int(instr[2][1:]))[2:].zfill(4)
            Rd = bin(int(instr[1][1:]))[2:].zfill(4)
   
            # Src2
            if i == '0':
                shamt5 = '00000'
                sh = '00'
                Rm = bin(int(instr[3][1:]))[2:].zfill(4)

                list_instr = [cond, op, funct, Rn, Rd, shamt5, sh, '0', Rm]
            else:
                rot = '0'.zfill(4)
                imm8 = bin(int(instr[3]))[2:].zfill(8)

                list_instr = [cond, op, funct, Rn, Rd, rot, imm8]
        else:
            print('Error: ASM (op) code is wrong')

            return 0
    elif instr[0] == 'LDR' or instr[0] == 'STR':
        cond = '1110'
        op = '01'

        # funct
        i = '0' if 'r' not in instr[3] else '1'
        p = '1'
        u = '0'
        b = '0'
        w = '0'
        l = '0' if instr[0] == 'STR' else '1'

        funct = [i, p, u, b, w, l]
 
        Rn = bin(int(instr[2][2:]))[2:].zfill(4)
        Rd = bin(int(instr[1][1:]))[2:].zfill(4)

        # Src2
        if i == '0':
            imm12 = bin(int(instr[3][:-1]))[2:].zfill(12)

            list_instr = [cond, op, funct, Rn, Rd, imm12]
        else:
            shamt5 = '00000'
            sh = '00'
            Rm = bin(int(instr[3][1:-1]))[2:].zfill(4)

            list_instr = [cond, op, funct, Rn, Rd, shamt5, sh, '1', Rm]
    elif instr[0] == 'MOV':
        cond = '1110'
        op = '10'

        # funct
        i = '0' if instr[2][0] == 'r' else '1'

        funct = [i]

        if i == '0':
            Rd = bin(int(instr[1][1:]))[2:].zfill(4)
            Operand2 = bin(int(instr[2][1:]))[2:].zfill(4)

            imm16 = bin(0).zfill(16)

            list_instr = [cond, op, funct, Rd, Operand2, imm16]
        else:
            Rd = bin(int(instr[1][1:]))[2:].zfill(4)
            Operand2 = bin(int(instr[2]))[2:].zfill(4)

            imm16 = bin(0)[2:].zfill(16)

            list_instr = [cond, op, funct, Rd, Operand2, imm16]
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

        sp = '0x' + struct.pack('>I', c).hex().zfill(register_lenght)

        config.set('Registers', 'SP', sp)

        with open('src/config.ini', 'w') as config_file:
            config.write(config_file)
    
# read instruction and load in memory
def load_instr():
    instrs = []

    # read asm code
    with open('src/asm code.txt') as f:
        code = f.readlines()

        for instr in code:
            instrs.append(instr.split())
    
    # load in memory
    for instr in instrs:
        load_memory(instr)
