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
with f.timing("import tensorflow",1):
    import tensorflow as tf
one=False
one=True
autotune = tf.data.experimental.AUTOTUNE
def time_make_list_files_dataset_str(path,pattern): # this is a list files dataset.
    path=pathlib.Path(path)
    from_glob=f.get_flowers_files(path,pattern)
    files=len(from_glob)
    with f.timing("dataset list files str with: "+str(files),files):
        ds = tf.data.Dataset.list_files(str(path/pattern),shuffle=False) # was str(path/'*.jpg')
    return ds
def time_make_list_files_dataset_glob(path,pattern,limit=None): # this is a list files dataset.
    from_glob=f.get_flowers_files(path,pattern)
    files=len(from_glob)
    if limit is not None:
        from_glob=from_glob[:limit]
    with f.timing("dataset list files glob with: "+str(files),units=files):
        return tf.data.Dataset.list_files(from_glob,shuffle=False)
def time_make_tensor_slices_dataset_glob(path,pattern,title=""):
    path=pathlib.Path(path)
    from_glob=f.get_files(path,pattern)
    files=len(from_glob)
    with f.timing("dataset from tensor slices glob with: "+str(files),units=files,title=title):
        return tf.data.Dataset.from_tensor_slices(from_glob)
def make_tensor_slices_dataset_list(files):
    return tf.data.Dataset.from_tensor_slices(files)
def time_make_tensor_slices_dataset_list(files,title=""):
    with f.timing("dataset from tensor slices file list with: "+str(len(files)),units=len(files),title=title):
        return make_tensor_slices_dataset_list(files)
def get_list_of_files_in_different_ways(path,pattern):
    from_glob=f.get_files(path,pattern)
    dslfstr=time_make_list_files_dataset_str(path,pattern)
    dslfgl=time_make_list_files_dataset_glob(path,pattern)
    dstsgl=time_make_tensor_slices_dataset_glob(path,pattern)
    dstsli=time_make_tensor_slices_dataset_list(from_glob)
def decode_image(image,width,height,jpeg=False):
    if jpeg:
        image = tf.image.decode_jpeg(image, channels=3) # convert the compressed string to a 3D uint8 tensor
    else:
        image = tf.image.decode_png(image, channels=3) # convert the compressed string to a 3D uint8 tensor
    image = tf.image.convert_image_dtype(image, tf.float32) # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    return tf.image.resize(image,[width,height]) # resize the image to the desired size.
def read_file(filename):
    binary=tf.io.read_file(filename)
    return binary
def decode_img(img):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_png(img, channels=3) # probably will not work for flowers
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [128,128])
def process_image(file_path):
    # load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img
def parse1(filename):
    binary=read_file(filename)
    return binary
def parse3(filename,y,z):
    binary=read_file(filename)
    return binary,y,z
def parse1and(image_filename): # like ings, but with .png instead of .jpeg.
    print("enter parse1 with:",type(image_filename),str(image_filename)[:50])
    binary=process_image(image_filename)
    print("parse1and returns:",type(binary))
    return binary
def parse3and(image_filename,json_filename,label_filename):
    binary=process_image(image_filename)
    return binary, json_filename, label_filename
def train_preprocess(image,json, label):
    print("image:",type(image))
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, max_delta=32.0 / 255.0)
    image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
    #Make sure the image is still in [0, 1]
    image = tf.clip_by_value(image, 0.0, 1.0)
    return image, json, label
def map_dataset(ds,parse,num_parallel_calls=1):
    return ds.map(parse,num_parallel_calls=num_parallel_calls)
def time_dataset_map(ds,parse,units,parallel,title=""):
    with f.timing(" map "+str(units)+" units with parallel="+str(parallel),units=units,title=title): # why does this require the f.?
        mapped = map_dataset(ds,parse,num_parallel_calls=parallel)
    return mapped
def time_map_varying_parallel(ds,parse,units,title=""):
    if False:
        print("just read each file")
        for i in range(1,9):
            time_dataset_map(ds,parse1,units,i,title=title)
        time_dataset_map(ds,parse1,units,autotune,title=title)
        print("read, decode, convert, resize each file")
        for i in range(1,9):
            time_dataset_map(ds,parse1and,units,i,title=title)
        time_dataset_map(ds,parse1and,units,autotune,title=title)
def do_enumerations(ds,parse=None):
        for i,x in enumerate(ds):
            if i<1 or i%5000==0:
                #print(i,type(x),str(x)[:20])
                #print(x.shape)
                if parse is not None:
                    y=parse(x)
                #print("y",type(y),y.shape)
def time_enumerations(ds,units=1,title=""):
    with f.timing("enumerate over dataset of "+str(units)+" units and map outside of dataset.",units,title): # why does this require the f.?
        do_enumerations(ds,parse1)
    mapped=time_dataset_map(ds,parse1and,units,autotune,title=title+" time dataset.map inside dataset (no enumeration).")
    with f.timing("enumerate over mapped "+str(units)+" units outside of dataset.",units,title):
        do_enumerations(mapped)
def do_one_pass(list_of_filenames):
        ds= make_tensor_slices_dataset_list(list_of_filenames)
        mapped=map_dataset(ds,parse1and,num_parallel_calls=autotune)
        do_enumerations(mapped)
def time_one_pass(list_of_filenames,title=""):
    units=len(list_of_filenames)
    with f.timing("one full pass of enumerating mapped "+str(units)+" units outside of dataset.",units=units,title=title):
        do_one_pass(list_of_filenames)
def run():
    print("one:",one)
    if False:
        get_list_of_files_in_different_ways("in/flower_photos/tulips","*.jpg")
        pattern="*.png"
        path="L:/ss/sem/20181107_133258/camera/cam_front_center"  # 188 files
        path=pathlib.Path(path)
        get_list_of_files_in_different_ways(path,pattern)

    print("--------------------------------------------")
    try:
        title="flowers"
        from_glob=f.get_files("in/flower_photos/tulips","*.jpg")
        units=len(from_glob)
        if one:
            units=2
        from_glob=from_glob[:units]    
        ds= time_make_tensor_slices_dataset_list(from_glob,title=title+" make dataset from list of filenames")
        time_enumerations(ds,units,title=title)
        time_one_pass(from_glob,title)
    except Exception as e:
        print("caught:",e)
    print("--------------------------------------------")
    try:
        title="cars"
        x,y,z=f.get_lists_of_filenames()
        path=f.path_head(x[0])
        leaf=f.path_leaf(x[0])
        #units=1000
        ds=time_make_tensor_slices_dataset_list(x[:units],title=title)
        #time_map_varying_parallel(ds,units)
        time_enumerations(ds,units,title=title)
        time_one_pass(x[:units],title)
    except Exception as e:
        print("caught:",e)
    print("--------------------------------------------")
    if one:
        exit()
    try:
        print("all the cars")
        time_one_pass(x,title)
    except Exception as e:
        print("caught:",e)
    print("--------------------------------------------")

def main():
    np.set_printoptions(precision=4)
    run()
    pass
if __name__ == "__main__":
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



