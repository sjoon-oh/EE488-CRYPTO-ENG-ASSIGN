import sys

import numpy as np
import hashlib


# Index values.
HASH_   = 0
GRAPH_  = 1
IDX_    = 2

TAIL_   = 0
CYCLE_  = 1

BITMASK = 0xffff # 16 bit
BITMASK = 0xffffffff # 32 bit
# BITMASK = 0xffffffffffffffff # 64 bit
# BITMASK = 0xffffffffffffffffffff # 80 bit
# BITMASK = 0xffffffffffffffffffffffffffffffff # 128 bit



banner = \
'''[EE488] Introduction to Cryptographic Engineering
        Homework #3 5-(a), Hash Chain
        Author: SukJoon Oh, @sjoon-oh Github.'''

if (len(sys.argv) < 1):
    print("Err: Give an argument.")

else:
    print(banner) # Start.

    x_list = [] # argmuments x's
    g_list = [] # graphs 
    r_list = [] # reports

    for arg in sys.argv[1:]:
        x_init = int(arg).to_bytes(16, 'big', signed=True)
        if x_init in x_list: continue

        x_list.append(x_init)

    print(f"Arguments ready for:")
    for x in x_list:
        print(f"  {x}")


    #
    # Initialize firsts.
    def search_graph(curr_hash, curr_graph, curr_idx):

        for g_idx, g_elem in enumerate(g_list):
            for idx, elem in enumerate(g_elem):

                if (curr_hash == elem[HASH_]):
                    return g_elem, idx
        
        return curr_graph, curr_idx + 1

    #
    # Do run
    for x in x_list:

        print(f"Running for x: {x}")

        #
        # Initializers
        graph = [] # Holds type-(int) with k-bits extracted.
        g_list.append(graph)

        init_x = x
        init_h = int(hashlib.md5(init_x).hexdigest(), 16) & BITMASK

        g_elem, g_idx = search_graph(init_h, graph, 0) # Search initial.

        if (id(g_elem) != id(graph)): # Case when first hash collides.
            
            g_list.append([]) # Register an empty graph
            r_list.append((0, -1)) # Initial hash is inside of a cycle, thus -1.

            continue

        graph.append((init_h, g_elem, g_idx))

        n_tail = 1
        n_cycle = 0
        
        #
        # Start.
        while (1):
            next_h = int(
                hashlib.md5(
                    graph[-1][HASH_].to_bytes(16, 'big', signed=True)).hexdigest(), 
                    16) & BITMASK


            next_g, next_i = search_graph(next_h, graph, graph[-1][IDX_])
            graph.append((next_h, next_g, next_i))
            
            n_tail = n_tail + 1 # Incr tail.

            if (id(next_g) != id(graph)): # Case when merged to other graph
                
                n_cycle = -1
                r_list.append((n_tail, -1))

                print(f"init_x: {x}, Points to OTHER: {id(next_g)}, exit.")
                break

            elif (next_i < graph[-2][IDX_]): # Case when cycle detected.
                
                n_cycle = len(graph) - next_i + 1
                r_list.append((n_tail, n_cycle))

                print(f"init_x: {x}, CYCLE detected: exit.")
                break

            print(f"\rHASH: {next_h}, TAIL: {n_tail}", end="")
        print("")

    #
    # Report PLZ
    t_list = [] # Tails list
    c_list = [] # Cycle list

    for tail_len, cycle_len in r_list:
        t_list.append(tail_len)
        if (cycle_len != -1): c_list.append(cycle_len)

    avg_tail_len = sum(t_list) / len(t_list)
    min_tail_len = min(t_list)
    max_tail_len = max(t_list)

    avg_cycl_len = sum(c_list) / len(c_list)
    min_cycl_len = min(c_list)
    max_cycl_len = max(c_list)

    n_comp = len(c_list)

    del t_list
    del c_list

    #
    # Debug
    with open('report-hw3-a.log', 'w') as f:
        
        for g_idx, g_elem in enumerate(g_list):
            f.write(f"Init x: {x_list[g_idx]}\n")

            for idx, elem in enumerate(g_elem):
                f.write(f"{idx: {8}} - hash: {elem[HASH_]: {8}}, next_g: {id(elem[GRAPH_])}, next_i: {elem[IDX_]: {8}}\n")

            f.write(f"REPORT - (TAIL: {r_list[g_idx][TAIL_]}, CYCLE: {r_list[g_idx][CYCLE_]})\n\n")
        
        f.write(f"----\n")
        f.write(f"Total {n_comp} components.\n\n")

        f.write(f"----\n")
        f.write(f"Average Tail Length: {avg_tail_len}\n")
        f.write(f"Maximum Tail Length: {max_tail_len}\n")
        f.write(f"Minimum Tail Length: {min_tail_len}\n\n")

        f.write(f"----\n")
        f.write(f"Average Cycle Length: {avg_cycl_len}\n")
        f.write(f"Maximum Cycle Length: {max_cycl_len}\n")
        f.write(f"Minimum Cycle Length: {min_cycl_len}\n\n")
    

            
    