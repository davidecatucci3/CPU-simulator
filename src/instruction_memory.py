from data_memory import data_memory

def instruction_memory(PC):
    instr = data_memory[PC]

    return instr
