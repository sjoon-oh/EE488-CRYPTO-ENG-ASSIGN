from socket import TIPC_CRITICAL_IMPORTANCE
import sys

import numpy as np
import hashlib

debug = True

banner = \
'''[EE488] Introduction to Cryptographic Engineering
        Homework #3, Hash Chain
        Author: SukJoon Oh, @sjoon-oh Github.'''

if (len(sys.argv) != 2):
    print("Err: Give an argument.")

else:
    print(banner) # Start.

    x = int(sys.argv[1])

    # result = hashlib.md5(x) 
    bytes_x = x.to_bytes(8, 'big', signed=True) # Eight bytes

    res = hashlib.md5(bytes_x)
    res_digest = res.digest()
    hexd = res.hexdigest()

    print(bin(int(hexd, 16)))

    hash_int = int(hexd, 16) & 0xffff


    if (debug):
        print(f"bytes_x: {bytes_x}")
        print(f"digest: {res}, type: {type(res)}")
        print(f"hex_digest: {hexd}, type: {type(hexd)}")
        print(f"hash_int: {hash_int}")
    
    graph_list = []
    report_list = []

    # graph_list.append()
    graph = []
    graph.append((hash_int, graph, 1))

    report = []

    # Index values.
    HASH_ = 0
    GRAPH_ = 1
    IDX_ = 2

    TAIL_ = 0
    CYCLE_ = 1

    graph_list.append(graph)

    curr_graph = graph
    curr_len_c = 0
    curr_len_t = 0

    run = True
    while (run):

        hash_next = int(
            hashlib.md5(
                graph[-1][HASH_].to_bytes(8, 'big', signed=True)).hexdigest(), 
                16) & 0xffff
        
        graph_next = 0
        idx_next = 0

        # In every graph,
        for g_idx, g_elem in enumerate(graph_list):

            if (run == False): break

            for idx, elem in enumerate(g_elem):
                if (hash_next == elem[HASH_]):
                    run = False

                    if (id(g_elem) == id(curr_graph)):
                        print(f"Found: {hash_next}, pointing to THIS, {idx}")

                        curr_len_c = len(curr_graph) - idx + 1
                        curr_len_t = len(curr_graph) - curr_len_c

                    else:
                        print(f"Found: {hash_next}, pointing to OTHER, {idx}")
                        
                        curr_len_c = -1
                        curr_len_t = len(curr_graph) + 1

                    graph_next = g_elem
                    idx_next = idx

                    break

        if (run):
            graph_next = curr_graph
            idx_next = len(curr_graph) + 1

        curr_graph.append((hash_next, graph_next, idx_next))
        
        
    for idx, elem in enumerate(curr_graph):
        print(f"idx_curr: {idx: {6}}, hash: {elem[HASH_]: {6}}, idx_next: {elem[IDX_]: {6}}")

    print(f"Generating report for input: {x}")
    report_list.append((curr_len_t, curr_len_c))

    print([id(g) for g in graph_list])
    print(report_list)

    # Counting tail length for this input.
    

    # encode():  to convert the string into bytes
    # digest():  to returns the encoded data in byte format
    # hexdigest():  to returns the encoded data in hexadecimal format