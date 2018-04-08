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

# Add a new basic histogram for just the total number of patterns
for _, _data in data.iteritems():
    _data['total_pat_hist'] = {'num patterns': sum([v for k,v in _data['opcode_hist'].iteritems()])}
print("\nTotal patterns histogram:")
print_histogram_latex(data,'total_pat_hist',top10)
