import configparser
import struct
import time

from data_memory import load_instr, write_data, write_back, clear_memory
from instruction_memory import instruction_memory
from register_file import register_file
from building_blocks import ALU

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
register_lenght = int(config['CPU settings']['register_lenght'])
pc = config['Registers']['PC']

# reset processor
def reset():
    # set registers to 0
    for i in range(13):
        config.set('Registers', f'r{i}', '0x00000000')
    
    for i in ['sp', 'lr', 'pc']:
        config.set('Registers', i, '0x00000000')

    with open('src/config.ini', 'w') as configfile:
        config.write(configfile)

    # clear data memory
    clear_memory()

# load instruction in memory
load_instr()

# execute instructions
for i in range(1, 4):
    print(f'Cycle {i}')

    # fetch
    instr = instruction_memory(pc)

    pc = '0x' + struct.pack('>I', i).hex().zfill(register_lenght)

    config.set('Registers', 'PC', pc)

    with open('src/config.ini', 'w') as config_file:
        config.write(config_file)

    # decode
    SrcA, SrcB, cmd, Rd = register_file(instr)

    # execute
    alu_res = ALU(SrcA, SrcB, cmd)
  
    # memory
    write_data(alu_res)

    # write back
    write_back(alu_res, Rd)

    time.sleep(2)

