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

    op = instr[1]

    if op == '00': # ADD or SUB
        cmd = instr[3]

        Operand2 = None

        Rn = int(instr[5], 2)
        SrcA = int(registers[f'r{Rn}'], 16)           

        i = instr[2]

        SrcB = int(registers[f'r{int(instr[-1], 2)}'], 16) if i == '0' else int(instr[-1], 2)

        Rd = f'r{int(instr[6], 2)}'
    elif op == '01': # LDR or STR
        i = instr[2]

        Operand2 = None

        cmd = '0100'

        if i == '0':
            Rn = int(instr[8], 2)

            SrcA = int(registers[f'r{Rn}'], 16)       

            Rm = int(instr[-1], 2)
            SrcB = Rm

            Rd = f'r{int(instr[9], 2)}'
        else: 
            Rn = int(instr[8], 2)
   
            SrcA = int(registers[f'r{Rn}'], 16)       

            Rm = int(instr[-1], 2)
   
            SrcB = int(registers[f'r{Rm}'], 16)       

            Rd = f'r{int(instr[9], 2)}'
    elif op == '10': # MOV
        i = instr[2]

        cmd = None
        SrcA = None
        SrcB = None

        if i == '0':
            Rd = f'r{int(instr[3], 2)}'

            Operand2 = f'{int(instr[4], 2)}'

            Operand2 = registers[f'r{Operand2}']
        else:
            Rd = f'r{int(instr[3], 2)}'

            Operand2 = int(instr[4], 2)
            Operand2 = '0x' + struct.pack('>I', Operand2).hex().zfill(8)
    else: # wrong op
        print('Error: OpCode not recognize')

    return SrcA, SrcB, cmd, Rd, Operand2

    

