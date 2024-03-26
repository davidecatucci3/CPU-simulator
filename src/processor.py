import configparser
import struct
import time

from data_memory import load_instr, write_data, write_back, clear_memory
from instruction_memory import instruction_memory
from register_file import register_file
from control_unit import control_unit
from building_blocks import ALU

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
register_lenght = int(config['CPU settings']['register_lenght'])
num_low_register = int(config['CPU settings']['num_low_register'])

# reset processor
def reset():
    # set registers to 0
    for i in range(num_low_register + 1):
        config.set('Registers', f'r{i}', '0x00000000')
    
    for i in ['sp', 'lr', 'pc']:
        config.set('Registers', i, '0x00000000')

    with open('src/config.ini', 'w') as configfile:
        config.write(configfile)

    # clear data memory
    clear_memory()

# load instruction in memory
load_instr()

def processor():
    # execute instructions
    for i in range(0, 50):
        # fetch
        pc = config['Registers']['PC']

        instr = instruction_memory(pc)
     
        if instr == bin(0)[2:].zfill(word_lenght): # check if there is another instruction in memory 
            break

        print(f'Cycle {i + 1}')

        new_pc = '0x' + struct.pack('>I', i + 1).hex().zfill(register_lenght)

        config.set('Registers', 'PC', new_pc)

        with open('src/config.ini', 'w') as config_file:
            config.write(config_file)

        # decode
        SrcA, SrcB, cmd, Rd, Operand2, use_alu = register_file(instr)

        # execute
        if use_alu:
            alu_res = ALU(SrcA, SrcB, cmd)
        else:
            alu_res = Operand2

        # memory
        write_data(alu_res)
    
        # write back
        write_back(alu_res, Rd)
        
        time.sleep(2)

processor()