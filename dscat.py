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
    #with f.timing("folder: "+folder+" ["+str(i)+"] has: "+str(len(files))+" files.",units,title):
    #    ds=tff.make_tensor_slices_dataset_list(files) 
filesets=f.getFilesets(x,"*.png")
print(len(filesets),"filesets.")
with f.timing("make datasets from filename sets.",len(x),title):
    datasets=tff.makeDatasets(filesets)
print(len(datasets),"datasets, type:",type(datasets))
tff.time_enumeration(datasets,units=len(datasets)) # was 1892?
# this will make the 44 datasets, one for each camera folder
# naybe this is enough for this file.
exit()
print("---------------------------------------")
def concat_datasets(datasets):
    ds0 = tf.data.Dataset.from_tensors(datasets[0])
    for ds1 in datasets[1:]:
        ds0 = ds0.concatenate(tf.data.Dataset.from_tensors(ds1))
    return ds0
with f.timing("zip flat map cat.",len(x),title):
    ds = tf.data.Dataset.zip(tuple(datasets)).flat_map(
        lambda *args: concat_datasets(args)
    )
tff.time_enumeration(ds,units=1892)