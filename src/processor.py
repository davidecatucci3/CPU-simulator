from data_memory import load_instr, write_data, write_back
from instruction_memory import instruction_memory
from register_file import register_file, registers
from building_blocks import ALU

# global variables
pc = hex(0)

# load instruction in memory
load_instr()

for i in range(1, 4):
    # fetch
    instr = instruction_memory(pc)

    pc = hex(i)

    # decode
    SrcA, SrcB, cmd, Rd = register_file(instr)

    # execute
    res = ALU(SrcA, SrcB, cmd)
  
    # memory
    write_data(res)

    # write back
    write_back(res, Rd)

    print(registers)