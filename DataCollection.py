import subprocess
import time
import csv
import random

ALGS = [1, 2, 3, 11, 12, 13]

def timeIt(func, *args):
    start = time.time()
    res = func(*args)
    end = time.time()

    run = end - start

    return run, res

def getPartition(flag, alg):
    complete = subprocess.run(["python3", "partition.py", str(flag), str(alg), "numbers.txt"], capture_output=True)
    output = complete.stdout.decode("utf-8").rstrip("\n")

    return output

def toCSV(csv_file, arr):
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in arr:
            writer.writerow(row)

def collect():
    times, vals = [], []

    for i in range(100):
        print("Problem: " + str(i))
        time_row, val_row = [], []
        kk_t, kk_val = timeIt(getPartition, 1, 0)
        time_row.append(kk_t)
        val_row.append(kk_val)

        for alg in ALGS:
            t, val = timeIt(getPartition, 0, alg)
            time_row.append(t)
            val_row.append(val)
        
        times.append(time_row)
        vals.append(val_row)
    
    toCSV("times.csv", times)
    toCSV("vals.csv", vals)

collect()
