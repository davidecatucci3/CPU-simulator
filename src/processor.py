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

# execute instructions
for i in range(0, 50):
    # fetch
    pc = config['Registers']['PC']

    instr = instruction_memory(pc)

    if instr == '000000000000000000000000000000': # check if there is another instruction in memory 
        break

    print(f'Cycle {i + 1}')

    new_pc = '0x' + struct.pack('>I', i + 1).hex().zfill(register_lenght)

    config.set('Registers', 'PC', new_pc)

    with open('src/config.ini', 'w') as config_file:
        config.write(config_file)

    # decode
    SrcA, SrcB, cmd, Rd, Operand2 = register_file(instr)
  
    # send data to control unit
    #cond = instr[0]
    #op = instr[1]
    #funct = instr[2:5] if instr[1] == '00' else instr[2:8]
    #Rd = instr[6] if instr[1] == '00' else instr[9]

    #control_unit(cond, op, funct, Rd)

    # execute
    if SrcA != None and SrcB != None:
        alu_res = ALU(SrcA, SrcB, cmd)
    else:
        alu_res = Operand2

    # memory
    write_data(alu_res)
    print(alu_res, Rd)
    # write back
    write_back(alu_res, Rd)
    
    time.sleep(2)
