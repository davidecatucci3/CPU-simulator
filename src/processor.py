from instruction_memory import instruction_memory
from register_file import register_file
from data_memory import load_instr
from building_blocks import ALU

# global variables
PC = hex(0)

# load instruction in memory
load_instr()

for i in range(1, 4):
    # fetch
    instr = instruction_memory(PC)

    PC = hex(i)

    # decode
    SrcA, SrcB, cmd = register_file(instr)

    # execute
    res = ALU(SrcA, SrcB, cmd)

    print(int(res, 2))

    # memory

    # write back