import configparser

config = configparser.ConfigParser()

config.read('src/config.ini')

word_lenght = int(config['CPU settings']['word_lenght'])

registers = {f'r{i}': '0'.zfill(word_lenght) for i in range(0, 16)}

def register_file(instr):
    SrcA = None
    SrcB = None

    op = instr[1]
    
    if op == '00':
        cmd = instr[3]

        if cmd == '0100' or cmd == '0010':
            idx_SrcA = instr[5].index('b')
            SrcA = int(instr[5][idx_SrcA + 1:], 2)

            if 'b' in registers[f'r{SrcA}']:
                idx_rx = registers[f'r{SrcA}'].index('b')
                SrcA = int(registers[f'r{SrcA}'][idx_rx + 1:], 2)
            else:
                SrcA = int(registers[f'r{SrcA}'], 2)

            i = instr[2]

            idx_SrcB = instr[-1].index('b')
            SrcB = int(registers[f'r{int(instr[-1][idx_SrcB + 1:], 2)}'], 2) if i == '0' else int(instr[-1][idx_SrcB + 1:], 2)

            idx_Rd = instr[6].index('b')
            Rd = f'r{int(instr[6][idx_Rd + 1:], 2)}'
        else:
            pass
    elif op == '01':
        pass
    else:
        pass

    return SrcA, SrcB, cmd, Rd