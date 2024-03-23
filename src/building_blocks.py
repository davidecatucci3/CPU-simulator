def ALU(SrcA, SrcB, cmd):
    res = None
 
    if cmd == '0100':
        res = SrcA + SrcB
    elif cmd == '0010':
        res = SrcA - SrcB
   
    bin_res = bin(res).zfill(32)

    return bin_res