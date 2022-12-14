import os
from argparse import ArgumentParser
from pathlib import Path
Operations = {
    # Arithmetic
    'moverr' : ['u8', 'u8'],
    'moveri' : ['u8', 'u16'],

    'addrr' : ['u8', 'u8'],
    'addri' : ['u8', 'u16'],

    'subrr' : ['u8', 'u8'],
    'subri' : ['u8', 'u16'],

    'ls' : ['u8', 'u8'],
    'rs' : ['u8', 'u8'],

    'andrr' : ['u8', 'u8'],
    'andri' : ['u8', 'u16'],

    'orrr' : ['u8', 'u8'],
    'orri' : ['u8', 'u16'],

    'xorrr' : ['u8', 'u8'],
    'xorri' : ['u8', 'u16'],

    'cmprr' : ['u8', 'u8' ,'u8'],
    'cmpri' : ['u8', 'u8', 'u16'],

    # Control
    'cjump' : ['u8', 'u16'],
    'jump' : ['u16'],
    'syscall' : ['u16'],
    'end' : [],

    # Mem R/W
    'ldrb' : ['u8', 'u8', 'u16'],
    'strbr' : ['u8', 'u8', 'u16'],
    'strbi' : ['u8', 'u8', 'u16'],

    'ldrh' : ['u8', 'u8', 'u16'],
    'strhr' : ['u8', 'u8', 'u16'], 
    'strhi' : ['u8', 'u16', 'u16'],

    # String
    'ldstring' : ['u8', 'string']
}

Conditions = ['LT', 'GT', 'LTEQ', 'GTEQ', 'EQ', 'NEQ']

Parser = ArgumentParser(prog = 'rasmgen', description = 'Creates the syntax file for the rasm language.')
Parser.add_argument('out')
Arguments = Parser.parse_args()
OutputPath = Path(Arguments.out)
with (OutputPath / 'rasm.inc').open('w') as Macros:
    # Write conditions.
    Macros.write('@ Condition enums\n')
    for Condition in Conditions:
        Macros.write(f'.equ {Condition}, {Conditions.index(Condition)}\n')
    Macros.write('\n')

    # Write opcodes.
    OpcodeNum = 1
    Macros.write('@ Opcodes\n')
    for Operation, Parameters in Operations.items():
        Macros.write(f'@ {Operation} ')
        for x in Parameters:
            Macros.write(f'<{x}> ')
        Macros.write('\n')
        Macros.write(f'.macro {Operation} ')
        for x in range(len(Parameters)):
            Macros.write(f'p{x}{"" if x == len(Parameters) - 1 else ", "}')
        Macros.write('\n')
        Macros.write(f'.hword {hex(OpcodeNum)}\n')
        for x in range(len(Parameters)):
            match Parameters[x]:
                case 'u8':
                    Macros.write(f'.byte \p{x}')
                case 'u16':
                    Macros.write(f'.hword \p{x}')
                case 'string':
                    Macros.write(f'.asciz "\p{x}\()"')
            Macros.write('\n')
        Macros.write('.endm\n\n')
        OpcodeNum += 1
    Macros.close()



