import configparser
import struct
import time

from data_memory import load_instr, write_data, write_back, clear_memory, data_memory
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

# load instructions in memory
load_instr()

# execute instructions
def processor(): 
    cycle_counter = 1
    start = True

    # execute instructions
    while start == True or instr != hex(0).zfill(word_lenght)[:word_lenght - 2]: # check if there is another instruction in memory
        start = False

        print(f'Cycle {cycle_counter}')

        # fetch
        pc = config['Registers']['PC']

        instr = instruction_memory(pc)

        # update pc
        new_pc = '0x' + struct.pack('>I', cycle_counter).hex().zfill(register_lenght) 

        config.set('Registers', 'pc', new_pc)
   
        with open('src/config.ini', 'w') as config_file:
            config.write(config_file)

        # control unit
        RegWrite, ALUControl, MemWrite = control_unit(instr)
    
        # decode
        SrcA, SrcB, Rd, Operand2 = register_file(instr)
  
        # execute
        if ALUControl != None:
            ALUResult = ALU(SrcA, SrcB, ALUControl)
        else:
            ALUResult = Operand2
       
        # memory
        if MemWrite:
            write_data(ALUResult, Rd)
    
        # write back
        if RegWrite:
            write_back(ALUResult, Rd, False)
        
        time.sleep(2)

        cycle_counter += 1 

processor()

