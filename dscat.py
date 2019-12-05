from __future__ import absolute_import, division, print_function, unicode_literals
import os
from os.path import join
import pathlib
import math
import numpy as np
import glob
import ntpath
from os import listdir
import os.path
from contextlib import contextmanager
from timeit import default_timer as timer
import functions as f
import json
from contextlib import contextmanager
from timeit import default_timer as timer
import functions as f
print("importing tensorflow")
with f.timing("import tensorflow",1):
    import tensorflow as tf
print(tf.__version__)
import tffunctions as tff
x,y,z=f.get_lists_of_filenames()
print("got (",len(x),len(y),len(z),") files.",flush=True)
first=x[0]
print("first file:",first,os.path.exists(first))
path=f.path_head(first)
filename=f.path_leaf(first)
print(path,filename)
maybe='L:/ss/sem/20180807_145028/camera/cam_front_center/20180807145028_camera_frontcenter_000000091.png'
if maybe==first:
    print("maybe =")
print("maybe file:",maybe,os.path.exists(maybe))
x,y,z=f.get_camera_folders(f.get_path(),root=f.get_root())
title="cars by folder:"
filesets=[]
for i,folder in enumerate(x): 
    files=f.get_files(folder,"*.png")
    units=len(files)
    print(i,"folder: "+folder,"has:",len(files),"files.")
    filesets.append(files)
    #with f.timing("folder: "+folder+" ["+str(i)+"] has: "+str(len(files))+" files.",units,title):
    #    ds=tff.make_tensor_slices_dataset_list(files) 
with f.timing("make datasets from filename sets.",len(x),title):
    datasets=[]
    for i,files in enumerate(filesets): 
        print(i)
        ds=tf.data.Dataset.from_tensor_slices(files)
        datasets.append(ds)

def concat_datasets(datasets):
    ds0 = tf.data.Dataset.from_tensors(datasets[0])
    for ds1 in datasets[1:]:
        ds0 = ds0.concatenate(tf.data.Dataset.from_tensors(ds1))
    return ds0

ds = tf.data.Dataset.zip(tuple(datasets)).flat_map(
    lambda *args: concat_datasets(args)
)