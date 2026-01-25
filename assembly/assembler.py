import os, sys, re

# All opcodes valid for the current version of Abacus-8
opcodes = {
    "lda":[0x00, 2], "sta":[0x10, 2], "mov":[0x20, 3], "jmp":[0x30, 2], "jcb":[0x38, 2], "jal":[0x3a, 2],
    "jeq":[0x3c, 2], "jzr":[0x3e, 2], "phs":[0x40, 2], "pls":[0x50, 2], "nop":[0x60, 1], "hlt":[0x70, 1],
    "add":[0x80, 3], "sub":[0x90, 3], "mul":[0xa0, 3], "cmp":[0xb0, 3], "ana":[0xc0, 2], "ora":[0xd0, 2],
    "xra":[0xe0, 2], "not":[0xf0, 2]
}

sp = 0xf0       # Initialize stack pointer (sp) at 0xf0
pc = 0x00       # Initialize prog counter (pc) at 0x00

loops = {}


try: f = open(sys.argv[1], 'r'); f = f.read()       # Turn the sourcefile, as stated by sys.argv[1], into a string
except: len(sys.argv != 2)                          # but that's only done if the sys.argv's length is 2.

'''
Tokenization section
'''
tokens = re.split("\n", f)                                          # 1st process: split into lines
for i in range(len(tokens)):
    tokens[i] = re.split(" |\t", tokens[i]);                        # 2nd process: split by space or tabspaces '\t'
    while '' in tokens[i]:
        tokens[i].remove('')

    if tokens[i] == []: pass
    else:
        if ';' in tokens[i]:                                        # 3rd process: remove comments
            deleteindex = tokens[i].index(';')                      #   get the index where ';' comment header is located
            for j in range(len(tokens[i])-1, deleteindex-1, -1):    #   do a reverse for-loop, starting from i-th token at this line, to the very index where ';' is located
                tokens[i].pop()                                     #   in this reverse for-loop, pop the last element of i-th token
        else: pass
    #print(tokens[i])

'''
1st pass in parsing and assembling

An assembly sourcefile is made of two main segments: '.prog' that contains all instruction and loops, and '.data' which encapsulate all variable declarations. The 1st pass program below would read the tokens line-by-line, and ignore empty lines (ones that contain empty list). If, at any line, either the keyword '.prog' or '.data' is encountered, it would set the "processing context" to respectively 0 ('.prog') or 1 ('.data').

When processing instructions (context == 0), the program would examine if there are indicators for loop declarations, which would be the double-dot ':' sign.
'''
context = None
code = []
loops = {}
data = {}
loop_len = 0
loop_loc = 0
loop_id = None
data_loc = 0x80
data_id = None
for i in range(len(tokens)):
    if tokens[i] == []: pass
    else:
        if '.' in tokens[i][0]:
            if '.prog' in tokens[i][0]: context = 0
            else: context = 1
        else:
            if context == 0:
                if ':' in tokens[i][0]:
                    loop_id = tokens[i][0][:len(tokens[i][0])-1]
                    loops[loop_id] = loop_loc
                else:
                    loop_loc += opcodes.get(tokens[i][0])[1]
                    tokens[i][0] = f'{(opcodes.get(tokens[i][0])[0]):02x}'
                    if len(tokens[i]) == 2:
                        opds = re.split(',', tokens[i][1]); tokens[i].pop()
                        for j in range(len(opds)):
                            tokens[i].append(opds[j])
                    else: pass
                    code.append(tokens[i])
            else:
                if tokens[i][1] == ':=' and '$' in tokens[i][2]:
                    tokens[i][1] = tokens[i][2][1:]; tokens[i].pop()
                else:
                    raise ValueError('Declaring data must be done with ":=" operator and "$" prefix on hex value')
                data[tokens[i][0]] = [f'{int(tokens[i][1], base=16):02x}', f'{data_loc:02x}']
                data_loc += 0x01

'''
2nd pass in parsing and assembling
'''
print("v3.0 hex words addressed")
addr_inst = 0x00
for i in range(len(code)):
    print(f'{addr_inst:02x}:', end=' ')
    try:
        if code[i][0] in ['30', '38', '3a', '3c', '3e']:
            code[i][1] = f'{loops.get(code[i][1]):02x}'
        else:
            if code[i][0] == '70':
                pass
            else:
                for j in range(1, len(code[i])):
                    code[i][j] = data.get(code[i][j])[1]
    except:
        len(code[i]) == 1
    addr_inst += len(code[i])
    for j in range(len(code[i])):
        print(code[i][j], end=' ')
    print()
hexdata = list(data.values())
for i in range(len(hexdata)):
    print(f'{hexdata[i][1]}: {hexdata[i][0]}')