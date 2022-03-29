import hashlib

ITER_THRESHOLD = 0xffffffffffffffff
BITMASK = 0xffffffffffffffff # 64 bit
# BITMASK = 0xffffffffffffffffffff # 80 bit
# BITMASK = 0xffffffffffffffffffffffffffffffff # 128 bit

import multiprocessing as mp
# PROC_NUM = mp.cpu_count()
PROC_NUM = 1

banner = \
'''[EE488] Introduction to Cryptographic Engineering
        Homework #3 5-(d), Hash Chain
        Author: SukJoon Oh, @sjoon-oh Github.'''


print(banner) # Start.
print(f"PROC_NUM: {PROC_NUM}")


def do_hash(val):
    return \
        int(hashlib.md5(val.to_bytes(16, 'big', signed=True)).hexdigest(), 16) & BITMASK

def do_search(proc_id, proc_num):
    
    h_list = [] # history list

    #
    # Search!
    init_x = proc_id
    
    while (init_x < BITMASK):

        cnt = 0

        history = {}
        next_h = do_hash(init_x)

        while (cnt < ITER_THRESHOLD): 
            
            try:
                val = history[next_h] # Test
                print(f"Proc {proc_id} found: ({cnt}, {init_x}), exit.")

                with open(f"report-hw3-d-proc-{proc_id}.log", 'w') as f:
                    f.write(f"Found: Initial - {init_x}, Counts - {cnt}\n")

                return (init_x, cnt)

            except KeyError:
                print(f"\rSearching... proc_id: {proc_id: {4}}, Counts: {cnt: {10}}", end="")

                history[next_h] = 1
                next_h = do_hash(next_h)

            cnt = cnt + 1

        del history

        init_x = init_x + proc_num

    return (0, 0)


import os

if __name__ == '__main__':

    with mp.Pool(processes=PROC_NUM) as p:
        # print(p.map(do_search, range(PROC_NUM)))

        res = [p.apply_async(do_search, args=(20223402, PROC_NUM)) for i in range(PROC_NUM)]
        print([_.get() for _ in res])
