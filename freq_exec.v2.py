#!/usr/bin/python
import sys, argparse, os, glob, csv
import multiprocessing as mp
import time
from freq import *
from os import listdir
from os.path import isfile, join
start_time = time.time()

#Arguments
parser = argparse.ArgumentParser(description='Frequency analysis')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-d','--directory',help='directory name', required=True)
parser.add_argument('-o','--outfile',help='csv outfile',required=True)
args = parser.parse_args()

freq_file=args.input
out_file=args.outfile
path=args.directory

#establish frequency map
fc = FreqCounter()
fc.ignorecase = True
fc.ignorechars = ""
fc.tally_str(open(freq_file).read())

#Create score Dictionary
score_data = {}

#Get list of files
files = [ join(path,f) for f in listdir(path) if isfile(join(path,f)) ]

def compute_probability(filename):
        with open(filename, 'r') as f:
                score = fc.probability(f.read())
        return filename, score

#multiprocess our frequency comparison
pool = mp.Pool(processes=8)
score_data = dict(pool.map(compute_probability,files))

#write our results out to a csv
with open(out_file,'wb') as f:
    w = csv.writer(f)
    w.writerows(score_data.items())

#print high and low scores
low_filescore = min(score_data, key=score_data.get)
high_filescore = max(score_data, key=score_data.get)

print "Lowest Score ",low_filescore," : ",score_data[low_filescore]
print "Highest Score ",high_filescore," : ",score_data[high_filescore]
print("--- Finished in %s seconds ---" % (time.time() - start_time))


