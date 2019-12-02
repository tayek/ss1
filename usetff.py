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
def run():
    print("--------------------------------------------")
    x,y,z=f.get_camera_folders(f.get_path(),root=f.get_root())
    title="cars by folder:"
    for i,folder in enumerate(x): 
        files=f.get_files(folder,"*.png")
        units=len(files)
        print(i,"folder: "+folder,"has:",len(files),"files.")
        with f.timing("folder: "+folder+" has:"+str(len(files))+"files.",units,title):
            ds=tff.make_tensor_slices_dataset_list(files)   
            mapped=ds.map(tff.parse1and,tff.autotune)
            tff.do_enumerations(mapped)
    print("--------------------------------------------")
def main():
    run()
    pass
if __name__ == "__main__":
    print("start")
    main()
# http://cs230.stanford.edu/blog/datapipeline/

#dataset = tf.data.Dataset.from_tensor_slices((images, jsons,labels))
#dataset = dataset.shuffle(len(images))
#dataset = dataset.map(parse_function, num_parallel_calls=4)
#dataset = dataset.map(train_preprocess, num_parallel_calls=4)
#dataset = dataset.batch(batch_size)
#dataset = dataset.prefetch(1)
#print("start iterating")
#i=iter(dataset)
#file = next(i)
#print("type:",type(file))
#image, json,label = parse_function(file,None,None)
#print("type:",type(image))
#show(image)