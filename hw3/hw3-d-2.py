import json
import hashlib

import tracemalloc

BITMASK = 0xffffffffffffffff # 64 bit
# BITMASK = 0xffffffffffffffffffff # 80 bit
# BITMASK = 0xffffffffffffffffffffffffffffffff # 128 bit

INITIAL_X = 20223402
ELEM_THRESH = 0xffffffffffff

tracemalloc.start()

banner = \
'''[EE488] Introduction to Cryptographic Engineering
        Homework #3 5-(d)-2, Hash Chain
        Author: SukJoon Oh, @sjoon-oh Github.'''


print(banner) # Start.

def do_hash(val):
    return \
        int(hashlib.md5(val.to_bytes(16, 'big', signed=True)).hexdigest(), 16) & BITMASK

hist = {}
file_cnt = 0
next_h = INITIAL_X

#
# First round: Generate Database
print("\nRunning first round...")
for i in range(1, BITMASK + 1):
    
    next_h = do_hash(next_h)

    try:
        val = hist[next_h] # Test

        with open(f"report-hw3-d-2.log", 'w') as f:
            f.write(f"Found: Counts - {i}\n")

        print(f"\nFound: Hash: {next_h}, Count {i}\n")
        exit()

    except KeyError:
        hist[next_h] = ''

    #
    # Save to JSON
    if (i % ELEM_THRESH == 0):
        with open(f"./hw3-d-json/hist-{file_cnt}.json", 'w') as outfile:
            json.dump(hist, outfile, sort_keys=False)

        del hist

        hist = {}
        file_cnt = file_cnt + 1

    mem = tracemalloc.get_traced_memory()
    print(f"\rHashing: {i: {10}} - {'%4.2f' % (i / BITMASK * 100)}%, Memory: {'%6.3f' % (mem[0] / 10**6)}MB, File Written ID: {file_cnt - 1: {10}}", end="")
        


#
# Second round:
print("\nRunning second round...")

if (file_cnt < 1): 
    print("Not enough JSON files. ERROR.")
    exit()

else:
    idx_base = ELEM_THRESH

    for i in range(1, file_cnt):

        target_keys = 0
        with open(f"./hw3-d-json/hist-{i}.json", "r") as f:

            target_keys = json.load(f)
            target_keys = [int(_) for _ in target_keys.keys()]

        for j in range(i): # vs files.
            
            #
            # Recover vs files  
            hist = {}
            with open(f"./hw3-d-json/hist-{j}.json", "r") as f:

                hist = json.load(f)
                int_keys = [int(_) for _ in hist.keys()]


                del hist
                hist = {}

                for _ in int_keys: hist[_] = ''
            
            mem = tracemalloc.get_traced_memory()
            print(f"\rChecking: {i: {6}} vs {j: {6}} file ID, {'%4.2f' % (i / BITMASK * 100)}%, Memory: {'%6.3f' % (mem[0] / 10**6)}MB", end="")

            for k, target in enumerate(target_keys):
                try:
                    val = hist[target]
                    print(f"\nFound: {target},")
                    print(f"  Each file size: {ELEM_THRESH}")
                    print(f"  Current position file: {i}, vs file {j}, of offset {k + 1}")
                    print(f"  Total index position: {1 + k + idx_base}")
                    exit()

                except KeyError:
                    continue

        idx_base = idx_base + len(target_keys)

    tracemalloc.stop()