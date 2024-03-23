import configparser

config = configparser.ConfigParser()

config.read('src/config.ini')

word_lenght = int(config['CPU settings']['word_lenght'])

def ALU(SrcA, SrcB, cmd):
    res = None
 
    if cmd == '0100':
        res = SrcA + SrcB
    elif cmd == '0010':
        res = SrcA - SrcB
   
    bin_res = bin(res).zfill(word_lenght)

    return bin_res