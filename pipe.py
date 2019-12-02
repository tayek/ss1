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
print("importing tensorflow",flush=True)
with f.timing("import tensorflow",1):
    import tensorflow as tf
print(tf.__version__,flush=True)
import tffunctions as tff
x,y,z=f.get_lists_of_filenames()
print("got (",len(x),len(y),len(z),") files.",flush=True)
units=len(x)
units=100
with f.timing("make dataset with "+str(units)+" units.",units):
    ds=tff.make_tensor_slices_dataset_list(x[:units])
print("enumerate original.",flush=True)
tff.time_enumeration(ds,units)
print("---------------------------------")
with f.timing("map filename to image: "+str(units)+" units.",units):
    mapped=ds.map(tff.parse1and,tff.autotune) # was parse1and
print("enumerate mapped.",flush=True)
tff.time_enumeration(mapped,units)
print("---------------------------------")
with f.timing("batch dataset: "+str(units)+" units.",units):
    batch_size=10
    batch_dataset = mapped.batch(batch_size)
print("enumerate batch.",flush=True)
tff.time_enumeration(ds,units)
print("---------------------------------")
with f.timing("prfetch dataset: "+str(units)+" units.",units):
    prefetched_dataset = batch_dataset.prefetch(1)
print("enumerate prefetch.",flush=True)
tff.time_enumeration(prefetched_dataset,units)

