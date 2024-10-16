# CPU Simulator
Simulation of a single-cycle CPU, able to understand only four ARM instructions: ADD, SUB, LDR, STR and MOV

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
- src/data_memory.py: contain the function that load the instruction in memory and the variable that represents the memory
- src/instruction_memory.py: pc -> instruction_memory -> instruction 
- src/processor.py: execute the 5 stages (fetch-decode-execute-memory-write back)
- src/register_file.py: decode the instruction to be executed

## How to use it
First you have to write your asm instructions in the src/asm\code.txt, after you can go in the config.ini file
to configure the settings of the processor and at the end run the src/processor.py file
