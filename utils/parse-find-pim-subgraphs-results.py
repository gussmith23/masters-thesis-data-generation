import sys
import os
import subprocess

def parse_find_pim_subgraphs(graph_dir_name, lines):
    if not os.path.exists(graph_dir_name):
        os.makedirs(graph_dir_name)

    total_num_subgraphs_heading = "TOTAL NUMBER OF SUBGRAPHS"
    subgraph_classes_heading = "SUBGRAPH CLASSES"
    num_unique_sg_classes_heading = "Total unique subgraph classes:"
    sg_classes_by_num_instances_heading = "BY NUMBER OF INSTANCES:"
    sg_classes_by_sg_size_heading = "BY SUBGRAPH SIZE:"
    subgraph_size_hist_heading = "SUBGRAPH SIZE HISTOGRAM"
    rear_frontier_operand_hist_heading = "REAR FRONTIER OPERAND HISTOGRAM"
    rear_frontier_immediate_type_hist_heading = "REAR FRONTIER IMMEDIATE TYPE HISTOGRAM"
    subgraph_operand_hist_heading = "SUBGRAPH OPERAND HISTOGRAM"
    subgraph_immediate_type_hist_heading = "SUBGRAPH IMMEDIATE TYPE HISTOGRAM"
    frontier_operand_hist_heading = "FRONTIER OPERAND HISTOGRAM"
    frontier_immediate_type_hist_heading = "FRONTIER IMMEDIATE TYPE HISTOGRAM"

    total_num_subgraphs = 0
    num_unique_sg_classes = 0

    # {opcode_name : count, ...}
    opcode_hist = {}
    # {opcode_name : count, ...}
    operand_opcode_hist = {}
    
    # {type : count, ...}
    immediate_type_hist = {}

    l_it = iter(lines)
    l = next(l_it)


    while total_num_subgraphs_heading not in l: l = next(l_it)
    l = next(l_it)
    total_num_subgraphs = int(l)


    while subgraph_classes_heading not in l: l = next(l_it)
    while num_unique_sg_classes_heading not in l: l = next(l_it)
    l = next(l_it)
    num_unique_sg_classes = int(l)

    def parse_dot_graph(l, l_it,filename_prefix):
        while "Count:" not in l: l = next(l_it)
        while "Count:" in l: l = next(l_it)
        count = int(l)
        while "Subgraph:" not in l: l = next(l_it)
        l = next(l_it) # We assume there's at least one line of the graph
        subgraph = ""
        while l != "}\n": # We assume that the graph ends with a brace on a single line
            subgraph += l
            l = next(l_it)
        subgraph += l # add the brace
        l = next(l_it)
        print(subgraph)

        echo_subproc = subprocess.Popen(('echo',subgraph), stdout=subprocess.PIPE)
        with open(os.path.join(graph_dir_name,filename_prefix + "_ct_" + str(count) + ".png"), "wb") as f:
            subprocess.call(('dot','-Tpng'), stdin = echo_subproc.stdout, stdout=f)
            

    
    num = 1
    while sg_classes_by_num_instances_heading not in l: l = next(l_it)
    l = next(l_it)
    while True:
        l = next(l_it) # skip Count
        count = int(l)
        while "Subgraph:" not in l: l = next(l_it)
        l = next(l_it) # We assume there's at least one line of the graph
        subgraph = ""
        while l != "}\n": # We assume that the graph ends with a brace on a single line
            subgraph += l
            l = next(l_it)
        subgraph += l # add the brace

        echo_subproc = subprocess.Popen(('echo',subgraph), stdout=subprocess.PIPE)
        with open(os.path.join(graph_dir_name,"subgraph_class_by_num_isntances_" + str(num) + "_ct_" + str(count) + ".png"), "wb") as f:
            subprocess.call(('dot','-Tpng'), stdin = echo_subproc.stdout, stdout=f)

        num +=1

        l = next(l_it); l = next(l_it)
        if "Count:" not in l: break

    num = 1
    while sg_classes_by_sg_size_heading not in l: l = next(l_it)
    l = next(l_it)
    while True:
        l = next(l_it) # skip Count
        count = int(l)
        while "Subgraph:" not in l: l = next(l_it)
        l = next(l_it) # We assume there's at least one line of the graph
        subgraph = ""
        while l != "}\n": # We assume that the graph ends with a brace on a single line
            subgraph += l
            l = next(l_it)
        subgraph += l # add the brace

        echo_subproc = subprocess.Popen(('echo',subgraph), stdout=subprocess.PIPE)
        with open(os.path.join(graph_dir_name,"subgraph_class_by_sg_size_" + str(num) + "_ct_" + str(count) + ".png"), "wb") as f:
            subprocess.call(('dot','-Tpng'), stdin = echo_subproc.stdout, stdout=f)

        num += 1

        l = next(l_it); l = next(l_it)
        if "Count:" not in l: break
    #while sg_classes_by_sg_size_heading not in l: l = next(l_it)
    #while "Count:" not in l: l = next(l_it)
    #while "Count:" in l:
    #    parse_dot_graph(l,l_it,"subgraph_class_by_sg_size")
    #    while l == "\n": l = next(l_it)

    def parse_hist(l, l_it, hist_name):
        hist = {}
        while hist_name not in l: l = next(l_it)
        l = next(l_it)
        while l != '\n':
            split_str = l.strip().split('\t')
            hist[split_str[0]] = int(split_str[1])
            l = next(l_it)
        return hist

    subgraph_size_hist = parse_hist(l, l_it, subgraph_size_hist_heading)
    rear_frontier_operand_hist = parse_hist(l, l_it, rear_frontier_operand_hist_heading)
    rear_frontier_immediate_type_hist = parse_hist(l, l_it, rear_frontier_immediate_type_hist_heading)
    subgraph_operand_hist = parse_hist(l, l_it, subgraph_operand_hist_heading)
    subgraph_immediate_type_hist = parse_hist(l, l_it, subgraph_immediate_type_hist_heading)
    frontier_operand_hist = parse_hist(l, l_it, frontier_operand_hist_heading)
    frontier_immediate_type_hist = parse_hist(l, l_it, frontier_immediate_type_hist_heading)

    return (total_num_subgraphs,
            num_unique_sg_classes,
            subgraph_size_hist,
            rear_frontier_operand_hist,
            rear_frontier_immediate_type_hist,
            subgraph_operand_hist,
            subgraph_immediate_type_hist,
            frontier_operand_hist,
            frontier_immediate_type_hist)
            
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
        data[filename] = parse_find_pim_subgraphs(os.path.basename(filename)+ "_graphs", f.readlines())

# TODO haven't updated this stuff yet.
## Pick the 10 benchmarks we'll use by finding the benchmarks with the greatest
## number of PIM patterns (calculated in a roundabout way, unfortunately.
## probably should have included that number in the summary results...)
#top10 = sorted(data.keys(), 
#                key = lambda filename:
#                        sum(data[filename]['opcode_hist'].values()),
#                        reverse = True)[0:10]
#
#print("Opcode histogram:")
#print_histogram_latex(data, 'opcode_hist', top10)
#print("\nOperand opcode histogram:")
#print_histogram_latex(data, 'operand_opcode_hist', top10)
##set(["invoke","select","phi","call","fptosi","fptoui","ptrtoint","shl","srem","urem"]))
#print("\nImmediate type histogram:")
#print_histogram_latex(data, 'immediate_type_hist', top10)
