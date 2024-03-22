import re

word_lenght = 32
size = 50 # units (not unit of measure)

data_memory = {hex(i): bin(0).zfill(word_lenght)[:word_lenght - 2]  for i in range(size)} # memory stack

c = 0
SP = hex(c)

# check errors in asm code
def check_code_error(instr):
    register_pattern = r'r([0-9]|1[0-3])'

    if not re.findall(register_pattern, instr[2]):
        return False

    return True

# convert asm code in binary code
def asm_to_bin(instr):
    if instr[0] == 'ADD' or instr[0] == 'SUB':
        # check asm error coding
        if check_code_error(instr):
            cond = '1110'
            op = '00'

            # funct
            i = '0' if instr[3][0] == 'r' else '1'
            cmd = '0100' if instr[0] == 'ADD' else '0010'
            s = '0'
            funct = i + cmd + s

            Rn = bin(int(instr[2][1:])).zfill(4)
            Rd = bin(int(instr[1][1:])).zfill(4)

            # Src2
            if i == '0':
                shamt5 = '00000'
                sh = '000'
                Rm = bin(int(instr[3][1:])).zfill(4)

                Src2 = shamt5 + sh + Rm
            else:
                rot = '0'.zfill(4)
                imm8 = bin(int(instr[3])).zfill(8)

                Src2 = rot + imm8
        
            res = cond + op + funct + Rn + Rd + Src2
    elif instr[0] == 'LDR':
        pass
    elif instr[0] == 'STR':
        pass
    else:
        print('Error: Instruction not recognized')

        return 0

    return res

# convert instruction in binary format and load in memory
def load_memory(instr):
    bin_data = asm_to_bin(instr)

    if not 0:
        global c, SP

        data_memory[SP] = bin_data

        c += 1

        SP = hex(c)

# read instruction and load in memory
def read_instr():
    instrs = []

    # read asm code
    with open('src/asm_code.txt') as f:
        code = f.readlines()

        for instr in code:
            instrs.append(instr.split())
    
    # load in memory
    for instr in instrs:
        load_memory(instr)


read_instr()