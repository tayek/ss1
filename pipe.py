from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import join
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import glob
import ntpath
import json
from contextlib import contextmanager
from timeit import default_timer as timer
import functions as f
print("importing tensorflow")
with f.timing("import tensorflow",1):
    import tensorflow as tf
print(tf.__version__)
import tffunctions as tff
print("get filenames from text file")
x,y,z=f.get_lists_of_filenames()
units=200
print("make dataset with:",units,"units")
ds=tff.make_tensor_slices_dataset_list(x[:units])
print("map dataset")
mapped=ds.map(tff.process_image,tff.autotune) # was parse1and
print("batch dataset")
batch_size=10
batch_dataset = ds.batch(batch_size)
print("prefetch dataset")
prefetched_dataset = batch_dataset.prefetch(1)
print("enumerate")
def rollup(ds,units,parallel=1):
    # this need a local timing also.
    with f.timing("make pipline from dataset "+str(units)+" batches with parallel="+str(parallel),units=units):
        ds2 = ds.map(lambda x: x+1,num_parallel_calls=parallel)
        ds3 = ds2.shuffle(min(units,10000))
        repeat=10
        ds4 = ds3.repeat(repeat)
        batch=100
        ds5 = ds4.batch(batch)
        batches=units*repeat//batch
        # Use prefetch() to overlap the producer and consumer.
        ds6 = ds5.prefetch(1) #batches
        #print(batches,"batches")
    with f.timing("iterate"+str(batches),units=batches):
        print("iterate")
        i=0
        n=0
        for i,x in enumerate(ds6):
            if i<0 or i%5000==0:
                print(i,type(x),len(x),str(x)[:20])
            n+=1
    print("after enumerationm")
    if n!=batches:
        print(n,"!=",batches)

def parse(x):
    print("x",type(x),str(x)[:10])
    return x
with f.timing("enumerate over prefetced batch mapped dataset of "+str(units)+" units.",units):
    for i,x in enumerate(ds):
        if i<2 or i%5000==0:
            print(i,"x:",type(x),str(x)[:80])
            y=tff.parse1and(x)
            print("y",type(y),str(y.numpy())[:80])

