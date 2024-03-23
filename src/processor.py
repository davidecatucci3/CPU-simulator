import configparser
import struct

from data_memory import load_instr, write_data, write_back
from instruction_memory import instruction_memory
from register_file import register_file
from building_blocks import ALU

config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
pc = config['Registers']['PC']

# reset processor
def reset():
    pass

# load instruction in memory
load_instr()

for i in range(1, 3):
    # fetch
    instr = instruction_memory(pc)

    pc = '0x' + struct.pack('>I', i).hex().zfill(10)

    config.set('Registers', 'PC', pc)

    with open('src/config.ini', 'w') as configfile:
        config.write(configfile)

    # decode
    SrcA, SrcB, cmd, Rd = register_file(instr)

    # execute
    alu_res = ALU(SrcA, SrcB, cmd)
  
    # memory
    write_data(alu_res)

    # write back
    write_back(alu_res, Rd)

