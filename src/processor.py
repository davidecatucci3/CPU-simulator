from instruction_memory import instruction_memory
from register_file import register_file
from data_memory import load_instr

# global variables
PC = hex(0)

# load instruction in memory
load_instr()

# fetch
instr = instruction_memory(PC)

PC += 1

# decode
SrcA, SrcB = register_file(instr)

# execute

# memory

# write back