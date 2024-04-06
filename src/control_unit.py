def control_unit(instr):
    # instr datas
    cond = instr[0]
    op = instr[1]
    funct = instr[2]
    Rd = instr[4] if op in ['00', '01'] else instr[3]

    # controller variables
    RegWrite = False
    MemWrite = False
    ALUControl = None

    # RegWrite
    if op == '01' and funct[5] == '1':
        RegWrite = True
    
    # ALUControl
    if op == '00':
        ALUControl = funct[1]
    elif op == '01':
        ALUControl = '0100'
    elif op == '10':
        ALUControl = None

    # MemWrite
    if op == '01' and funct[5] == '0':
        MemWrite = True

    return RegWrite, ALUControl, MemWrite
