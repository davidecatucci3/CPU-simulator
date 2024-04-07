import configparser
import struct

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
registers = config['Registers']

# register file
def register_file(instr):
    SrcA = None
    SrcB = None
    Operand2 = None

    op = instr[1]

    if op == '00': # ADD or SUB
        Rn = int(instr[5], 2)
        SrcA = int(registers[f'r{Rn}'], 16)           

        i = instr[2][0]

        Rm = int(instr[-1], 2)
        SrcB = int(registers[f'r{Rm}'], 16) if i == '0' else Rm

        Rd = f'r{int(instr[6], 2)}'
    elif op == '01': # LDR or STR
        i = instr[2][0]

        if i == '0':
            Rn = int(instr[3], 2)

            SrcA = int(registers[f'r{Rn}'], 16)       

            Rm = int(instr[-1], 2)

            SrcB = Rm

            Rd = f'r{int(instr[4], 2)}'
        else: 
            Rn = int(instr[3], 2)
   
            SrcA = int(registers[f'r{Rn}'], 16)       

            Rm = int(instr[-1], 2)
   
            SrcB = int(registers[f'r{Rm}'], 16)       

            Rd = f'r{int(instr[4], 2)}'
    elif op == '10': # MOV
        i = instr[2][0]

        if i == '0':
            Rd = f'r{int(instr[3], 2)}'

            Operand2 = f'{int(instr[4], 2)}'
            Operand2 = registers[f'r{Operand2}']
        else:
            Rd = f'r{int(instr[3], 2)}'

            Operand2 = int(instr[4], 2)
            Operand2 = '0x' + struct.pack('>I', Operand2).hex().zfill(8)
    else: # wrong op
        print('Error: op not recognized')

    return SrcA, SrcB, Rd, Operand2

    

