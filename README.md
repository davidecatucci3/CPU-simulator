# CPU Simulation

Simulation of a single-cycle CPU, able to execute only 5 instructions (ADD, SUB, STR, LDR and MOV)

## CPU Configuration
- word lenght: 32bit
- num low registers: 12 (r0-r12)
- value register lenght: 32bit

The config.ini file contains all the other data

## Files
- src/asm_code.txt: instructions written in assembly
- src/building_blocks.py: the most important logic circuits (ALU, mux, ...)
- src/config.ini: CPU configuration (with all the important data)
- control_unit.py: controller that according to the instruction decide if some global variable are True or False
- src/CPU.py: file that connect all the different main files (data_memory.py, processor.py, instruction_memory.py and control_unit.py)
- src/data_memory.py: contain the function that load the instruction in memory and the variable that represents the memory
- src/instruction_memory.py: pc -> instruction_memory -> instruction 
- src/processor.py: execute the 5 stages (fetch-decode-execute-memory-write back)
