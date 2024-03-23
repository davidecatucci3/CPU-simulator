import configparser

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])

registers = config['Registers']

def register_file(instr):
    SrcA = None
    SrcB = None

    op = instr[1]
    
    if op == '00':
        cmd = instr[3]

        if cmd == '0100' or cmd == '0010':
            idx_Rn = instr[5].index('b')
            Rn = int(instr[5][idx_Rn + 1:], 2)
            SrcA = int(registers[f'r{Rn}'], 16)           

            i = instr[2]

            idx_SrcB = instr[-1].index('b')
            SrcB = int(registers[f'r{int(instr[-1][idx_SrcB + 1:], 2)}'], 16) if i == '0' else int(instr[-1][idx_SrcB + 1:], 2)

            idx_Rd = instr[6].index('b')
            Rd = f'r{int(instr[6][idx_Rd + 1:], 2)}'
        else:
            pass
    elif op == '01':
        i = instr[2]

        cmd = '0100'

        if i == '0':
            idx_Rd = instr[9].index('b')

            Rd = int(instr[9][idx_Rd + 1:], 2)

            SrcA = int(registers[f'r{Rd}'], 16)       

            idx_Rm = instr[-1].index('b')
            Rm = int(instr[-1][idx_Rm + 1:], 2)

            SrcB = Rm

            Rd = f'r{int(instr[9][idx_Rd + 1:], 2)}'
        else:
            pass
    else:
        pass

    return SrcA, SrcB, cmd, Rd

    

