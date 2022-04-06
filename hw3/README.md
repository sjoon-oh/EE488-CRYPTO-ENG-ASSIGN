# EE488 Cryptography Engineering

## Spring 2022, Homework #3

SukJoon Oh, 20223402

## Requirements

This script is written in `Python 3.10.2`. It consists of two files, `hw3-a.py` and `hw3-d-2.py`. The former is for the question 5-(a), and the latter is for the 5-(d) and 5-(e). 

```sh
$ python --version
Python 3.10.2
```

Both script depend on the `hashlib` library, which may be pre-installed to the system with `Python3`. Make sure that your system has both of the requirements.

The running environment is as follows:
- Intel Core i7-10700 @ 2.90GHz
- RAM 31.2 GiB
- Manjaro Linux Quonos 21.2


## Problem 5. Hash Chain

### (a) Properties of a Hash Chain

#### How to Run

A hash chain comprised of a feedback architecture; the output of a function is used as an input of the same function. This structure may not be easy to implement with paralell computation.

The script requires more than one argument. The starting points (or a vectors) should be listed as an argument. For instance, if you want to give the argument of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] as multiple starting point of a graph, the the command should be given as:

```sh
$ python3 hw3-a.py 1 2 3 4 5 6 7 8 9 10 11  
```
If the number of argument given is not above 1, the script will fail to execute.

#### Code Analysis

Since `hashlib` library's `md5` function receives the argument as string byte form, the arguments are preprocessed to have its value in byte form. This is stored in `x_list` and later be used as the initial value of hash computations. The byte transformation is done as below:

```python
for arg in sys.argv[1:]:
    x_init = int(arg).to_bytes(16, 'big', signed=True)
    if x_init in x_list: continue

    x_list.append(x_init)
```

Since getting LSB 16 bits is not an expensive computation, the operation itself does not exploit much resource of a machine. 

The `g_list` holds every graph, which originated from each initial value stored in `x_list`. Each element in `g_list` is graph, represented in `list` form. Each element in a graph is tuple, that contains three elements `(hash_value, next_graph, graph_index)`. `hash_value` stores the computation result of hash function, `next_graph` stores the pointer of what graph of the vertex is pointing to, and `graph_index` stores the index of the next element (vertex) in a list. in this case the graph. 

For each initial value in `x_list`, it calls `search_graph` function. 

```python

#
# Initialize firsts.
def search_graph(curr_hash, curr_graph, curr_idx):

    for g_idx, g_elem in enumerate(g_list):
        for idx, elem in enumerate(g_elem):

            if (curr_hash == elem[HASH_]):
                return g_elem, idx

    return curr_graph, curr_idx + 1
```

When all computations were taken place, the results are stored in `r_list`, in tuple form. Properties of graphs are printed out to console at the end of the execution.

### (b) Finding a Cycle in k-bits

#### How to Run

This script does not require any additional arguments. Thus, just do:

```sh
$ python3 hw3-d-2.py
```

Before running the script, the value `FILE_THRESH` and `BITMASK` may be adjusted based on your computing environment. Also, be careful to make a directory `hw3-d-json` when running this script. Files generated will be stored in that directory. When it is not found, error will be triggered. 

#### Code Analysis

This question imposes challenges in space complexity. Since the feedback structure cannot fully utilize the parallel programming, it is not ideal to use some multithread/multiprocess library, such as `multiprocessing`. Plus, setting large k-bits makes the complexity of $$2^k$$, which most of commodity hardware cannot store all the histories.

This script tackles the problem by periodically moves the hash calculation history in JSON format to designated disk.

The script contains two parts:
- Function `run_first_round`: Computes in some specific range in memory, stores the history when it is finished.
- Function `run_second_round`: Load each files, and compare the history with the history generated in the first round.i

```python
BITMASK = 0xffffffffffffffff # 64 bit
FILE_THRESH = 0x1ffffff
```

The `BITMASK` is a global variable that extracts LSB of the output of `md5`. `FILE_THRESH` is the value that limits the in-memory computation. Until the loop count exceeds `FILE_THRESH`, the hash computation will continue. This means that every file will have exactly `FILE_THRESH` elements.

```python
def do_hash(val):
    return \
        int(hashlib.md5(val.to_bytes(16, 'big', signed=True)).hexdigest(), 16) & BITMASK
```

`do_hash` is another form of computing hash value. The LSB is extracted by `&` operation.

```python
def run_first_round(next_h, file_cnt):
    #
    # First round: Generate Database
    file_cnt = file_cnt + 1

    hist = {}
    prev_h = next_h

    for i in range(0, FILE_THRESH):
        prev_h = next_h
        next_h = do_hash(prev_h)

        try:
            val = hist[next_h] # Test
            with open(f"report-hw3-d-2.log", 'w') as f:
                f.write(f"Found at first round: Counts - {i}\n")

            exit()

        except KeyError:
            hist[next_h] = ''

        mem = tracemalloc.get_traced_memory()

    #
    # Save to JSON
    with open(f"./hw3-d-json/hist-{file_cnt}.json", 'w') as outfile:
        json.dump(hist, outfile, sort_keys=False)

    del hist
    return next_h, file_cnt
```

When recording the computed hash value, this script does not use lists or any other custom data structure, but Python dictionary. Since  the dictionary stores value using  key-value, the function `run_first_round` observes whether the dict `hist` currently has identical value to the current hash. If not, `KeyError` exception is thrown, and the value is recorded with the hash as the key, and some arbitary value as the value. The value is not really important, thus empty string is used as a dummy data.

When single run is ended in `FILE_THRESH` iteration, the dictionary is stored to the disk in JSON format. the `json` library is essential in this operation.

```python
def run_second_round(latest_file):
    #
    # Second round:
    print("\nRunning second round...")

    if (latest_file < 1): 
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
```

Before the ending this round, the previously stored files are loaded to the memory by `run_second_round` in the dictionary form. This makes the checking process rather simple, since this is again triggers `KeyError` when the key is unseen in the history. If some values are found, report is written to the disk. Otherwise, it return to the loop and calls `run_first_round` again.





