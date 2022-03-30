import json
import hashlib

import tracemalloc

# BITMASK = 0xffffffffffffffff # 64 bit
BITMASK = 0xffffffffffffffffffff # 80 bit
# BITMASK = 0xffffffffffffffffffffffffffffffff # 128 bit

INITIAL_X = 20223402

# Test.
LOOP_THRESH = 0xffffffffff # At single loop, how many files?
FILE_THRESH = 0xffffff


tracemalloc.start()

banner = \
'''[EE488] Introduction to Cryptographic Engineering
        Homework #3 5-(d)-2, Hash Chain
        Author: SukJoon Oh, @sjoon-oh Github.'''


print(banner) # Start.

def do_hash(val):
    return \
        int(hashlib.md5(val.to_bytes(16, 'big', signed=True)).hexdigest(), 16) & BITMASK



def run_first_round(next_h, file_cnt):
    #
    # First round: Generate Database
    print("Running first round...")

    hist = {}
    prev_h = next_h

    for i in range(0, FILE_THRESH):
        
        prev_h = next_h
        next_h = do_hash(prev_h)

        try:
            val = hist[next_h] # Test

            with open(f"report-hw3-d-2.log", 'w') as f:
                f.write(f"Found at first round: Counts - {i}\n")

            print(f"\nFound: Hash: {next_h}, Message: {prev_h}, Count {i}\n")
            exit()

        except KeyError:
            hist[next_h] = ''



        mem = tracemalloc.get_traced_memory()
        print(f"\rHashing: {i: {10}} - {'%4.2f' % (i / FILE_THRESH * 100)}% of threshold, Memory: {'%8.2f' % (mem[0] / 10**6)}MB, File Written ID: {file_cnt: {10}}", end="")

    #
    # Save to JSON

    with open(f"./hw3-d-json/hist-{file_cnt}.json", 'w') as outfile:
        json.dump(hist, outfile, sort_keys=False)

    del hist
    file_cnt = file_cnt + 1

    return next_h, file_cnt
        

def run_second_round(latest_file):
    #
    # Second round:
    print("\nRunning second round...")

    if (latest_file < 1): 
        print("Not enough JSON files. Jump.")
        return

    else:
        idx_base = FILE_THRESH * latest_file


        target_keys = 0
        with open(f"./hw3-d-json/hist-{i}.json", "r") as f:

            target_keys = json.load(f)
            target_keys = [int(_) for _ in target_keys.keys()]

        for j in range(latest_file): # vs files.
            
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
            print(f"\rChecking: {latest_file: {6}} vs {j: {6}} file ID, {'%8.2f' % (j / FILE_THRESH * 100)}%, Memory: {'%8.2f' % (mem[0] / 10**6)}MB", end="")

            for k, target in enumerate(target_keys):
                try:
                    val = hist[target]

                    with open(f"report-hw3-d-2.log", 'w') as f:
                        f.write(f"Found at file - {latest_file}\n")

                        f.write(f"\nFound at second round: {target},\n")
                        f.write(f"  Each file size: {FILE_THRESH}\n")
                        f.write(f"  Current position file: {latest_file}, vs file {j}, of offset {k + 1}\n")

                        f.write(f"  Total index position: {1 + k + idx_base}\n")
                    exit()

                except KeyError:
                    continue
            
            del hist

        idx_base = idx_base + len(target_keys)
        del target_keys


#
# Main script run.

hist = {}

next_h = INITIAL_X

file_cnt = -1
loop_cnt = 0

while (loop_cnt < (BITMASK // FILE_THRESH)):


    next_h, file_cnt = run_first_round(next_h, file_cnt)

    run_second_round(file_cnt)
    loop_cnt = loop_cnt + 1

    print(f"\nCheckpoint: (loop count: {loop_cnt}, {file_cnt})")

print("Something's wrong, nothing found.")

tracemalloc.stop()
