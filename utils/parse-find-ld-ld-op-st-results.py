import sys
import os

def parse_find_ld_ld_op_st_results(lines):
    opcode_hist_heading = "OPCODE HISTOGRAM"
    operand_opcode_hist_heading = "OPERAND OPCODE HISTOGRAM"
    immediate_type_hist_heading = "IMMEDIATE TYPE HISTOGRAM"

    # {opcode_name : count, ...}
    opcode_hist = {}
    # {opcode_name : count, ...}
    operand_opcode_hist = {}
    
    one_immediate_operand = 0
    two_immediate_operands = 0

    # {type : count, ...}
    immediate_type_hist = {}

    l_it = iter(lines)
    l = next(l_it)

    while opcode_hist_heading not in l: l = next(l_it)
    l = next(l_it)
    while l != '\n':
        split_str = l.strip().split('\t')
        opcode_hist[split_str[0]] = int(split_str[1])
        l = next(l_it)
    
    while operand_opcode_hist_heading not in l: l = next(l_it)
    l = next(l_it)
    while l != '\n':
        split_str = l.strip().split('\t')
        operand_opcode_hist[split_str[0]] = int(split_str[1])
        l = next(l_it)

    while not l: l = next(l_it)
    next(l_it) # skip heading
    one_immediate_operand = int(next(l_it))
    next(l_it) # skip heading
    two_immediate_operands = int(next(l_it))

    while immediate_type_hist_heading not in l: l = next(l_it)
    try:
        l = next(l_it)
        while True:
            split_str = l.strip().split('\t')
            immediate_type_hist[split_str[0]] = int(split_str[1])
            l = next(l_it)
    except StopIteration:
        pass

    return { 'opcode_hist' : opcode_hist, 
            'operand_opcode_hist' : operand_opcode_hist, 
            'one_immediate_operand' : one_immediate_operand,
            'two_immediate_operands' : two_immediate_operands, 
            'immediate_type_hist' : immediate_type_hist }

# {filename : hist, ...}
data = {}

for filename in sys.argv[1:]:
    with open(filename) as f:
        data[filename] = parse_find_ld_ld_op_st_results(f.readlines())

top10 = sorted(data.keys(), 
                key = lambda filename:
                        sum(data[filename]['opcode_hist'].values()),
                        reverse = True)[0:10]

## print latex table format

# create column names
col_headings = set()
for name in top10:
   col_headings.update(data[name]['opcode_hist'].keys())
col_headings = sorted(list(col_headings))

print('&' + '&'.join(col_headings) + '\\\\')

for name in top10:
    entries = []
    for heading in col_headings:
        try:
            count = data[name]['opcode_hist'][heading]
        except KeyError:
            count = 0
        entries.append(count)
    print(os.path.basename(name).split('.')[0] + '&' + '&'.join(map(lambda c: str(c) if c>0 else '', entries)) + '\\\\')
