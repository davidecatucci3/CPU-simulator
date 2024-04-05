import configparser
import struct

# read config.ini
config = configparser.ConfigParser()

config.read('src/config.ini')

# global variables
word_lenght = int(config['CPU settings']['word_lenght'])
register_lenght = int(config['CPU settings']['register_lenght'])

# ALU
def ALU(SrcA, SrcB, cmd):
    res = None
 
    if cmd == '0100':
        res = SrcA + SrcB

        bin_res = '0x' + struct.pack('>I', res).hex().zfill(register_lenght)
    elif cmd == '0010':
        res = SrcA - SrcB

        unsigned_res = res + (1 << register_lenght)

        bin_res = '0x' + struct.pack('>I', unsigned_res).hex().zfill(register_lenght)

    return bin_res