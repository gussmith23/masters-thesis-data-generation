import sys
import os

def parse_find_ld_ld_op_st_results(lines):
    opcode_hist_heading = "OPCODE HISTOGRAM"
    operand_opcode_hist_heading = "OPERAND OPCODE HISTOGRAM"
    immediate_type_hist_heading = "IMMEDIATE TYPE HISTOGRAM"
    total_op_st_heading = "TOTAL OP-ST"

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

    while total_op_st_heading not in l: l = next(l_it)
    l = next(l_it)
    total_op_st = int(l)
    
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
            'immediate_type_hist' : immediate_type_hist,
            'total_op_st' : total_op_st}

# histogram: either 'opcode_hist', 'operand_opcode_hist', or
# 'immediate_type_hist'
# ignore_columns: a set of columns to ignore, if seen.
def print_histogram_latex(data, histogram, benchmarks, ignore_columns=set()):
    # create column names
    col_headings = set()
    for name in benchmarks:
       col_headings.update(data[name][histogram].keys())
    col_headings = sorted(list(col_headings.difference(ignore_columns)))

    print('&' + '&'.join(col_headings) + '\\\\')

    for name in benchmarks:
        entries = []
        for heading in col_headings:
            try:
                count = data[name][histogram][heading]
            except KeyError:
                count = 0
            entries.append(count)
        print(os.path.basename(name).split('.')[0] + '&' + '&'.join(map(lambda c: str(c) if c>0 else '', entries)) + '\\\\')

# {filename : hist, ...}
data = {}

for filename in sys.argv[1:]:
    with open(filename) as f:
        data[filename] = parse_find_ld_ld_op_st_results(f.readlines())

# Pick the 10 benchmarks we'll use by finding the benchmarks with the greatest
# number of PIM patterns (calculated in a roundabout way, unfortunately.
# probably should have included that number in the summary results...)
top10 = sorted(data.keys(), 
                key = lambda filename:
                        sum(data[filename]['opcode_hist'].values()),
                        reverse = True)[0:10]

print("Opcode histogram:")
print_histogram_latex(data, 'opcode_hist', top10)
print("\nOperand opcode histogram:")
print_histogram_latex(data, 'operand_opcode_hist', top10)
#set(["invoke","select","phi","call","fptosi","fptoui","ptrtoint","shl","srem","urem"]))
print("\nImmediate type histogram:")
print_histogram_latex(data, 'immediate_type_hist', top10)

def getname(name): return os.path.basename(name).split('.')[0]

# name : total
totals = {}
for filename, _data in data.iteritems():
    totals[getname(filename)] = sum([v for _,v in _data['opcode_hist'].iteritems()])

# Add a new basic histogram for just the total number of patterns
for _, _data in data.iteritems():
    _data['total_pat_hist'] = {'num patterns': sum([v for k,v in _data['opcode_hist'].iteritems()])}
print("\nTotal patterns histogram:")
print_histogram_latex(data,'total_pat_hist',top10)

# opcode hist v2
# {instruction : { program_name : number}}
opcode_hist_new = {}
for filename, _data in data.iteritems():
    name = getname(filename)
    for instr, num in _data['opcode_hist'].iteritems():
        if instr not in opcode_hist_new: opcode_hist_new[instr] = {}
        opcode_hist_new[instr][name] = float(num)/totals[name]

instructions_in_order = [
        "add", "sub", "mul", "udiv", "sdiv", "urem", "srem", "fadd", "fsub",
        "fmul", "fdiv", "frem", "shl", "lshr", "ashr", "and", "or", "xor",
        "trunc", "fptrunc", "zext", "sext", "fptoui", "fptosi", "uitofp",
        "sitofp", "ptrtoint", "inttoptr", "bitcast"
        ]

print("")

columns = sorted(totals.keys(), key=lambda name: name.lower())
print("&" + "&".join(columns) + "\\\\")
for instr in instructions_in_order:
    if instr not in opcode_hist_new: continue
    _data = opcode_hist_new[instr]
    print(instr + "&" + "&".join(["{0:.1f}".format(100*_data[column]) if column in _data else "" for column in columns]) + "\\\\")

print("")

# operand opcode hist v2
operand_totals = {}
for filename, _data in data.iteritems():
    operand_totals[getname(filename)] = sum([v if k!="load" else 0 for k,v in _data['operand_opcode_hist'].iteritems()])
operand_opcode_hist_new = {}
for filename, _data in data.iteritems():
    name = getname(filename)
    for instr, num in _data['operand_opcode_hist'].iteritems():
        if instr == "load": continue
        if instr not in operand_opcode_hist_new: operand_opcode_hist_new[instr] = {}
        operand_opcode_hist_new[instr][name] = float(num)/operand_totals[name]
print("&" + "&".join(columns) + "\\\\")
for instr in sorted(operand_opcode_hist_new.keys()):
    _data = operand_opcode_hist_new[instr]
    print(instr + "&" + "&".join(["{0:.1f}".format(100*_data[column]) if column in _data else "" for column in columns]) + "\\\\")

print("\nTotal op-st:\n")
for filename, _data in data.iteritems():
    print(getname(filename) + "&" + str(_data['total_op_st']) + "\\\\")
