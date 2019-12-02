#https://stackoverflow.com/questions/47653644/multi-threading-in-dataset-api
#make a copy and try to use listfiles to make 44 datsets.
import os
from os import listdir
from os.path import isfile, join
import glob
import functions as f
#import pathlib # ntpath?
from timeit import default_timer as timer
fast=True
fast=False
missing_images=[]
missing_jsons=[]
missing_labels=[]
def p(images,jsons,labels):
    print("types:",type(images),type(jsons),type(images))
    print("lengths:",len(images),len(jsons),len(images))
    print("first:",images[0],jsons[0],images[0])
def get_files_from_camera_folders(camera_folders):
    print(type(camera_folders),len(camera_folders))
    good=[]
    for i,(image,json,label) in enumerate(camera_folders):
        if i==0:
            print("camera folders: ",type(image),len(image))
        print(image)
        images=f.get_files(image,"*.png")
        jsons=f.get_files(json,"*.json")
        labels=f.get_files(label,"*.png")
        if(len(images)==len(jsons) and len(images)==len(labels)):
            good.extend(list(zip(images,jsons,labels)))
        else:
            print(image,len(images),len(jsons),len(labels),"number of files is not equal!, files will ve ignored!")
        if len(missing_images)>0:
            print(len(missing_jsons),"missing images, out of:",len(images))
        if len(missing_jsons)>0:
            print(len(missing_jsons),"missing jsons, out of:",len(images))
        if len(missing_labels)>0:
            print(len(missing_labels),"missing labels, out of:",len(images))
        if fast:
            break
    print(len(good),".png's")
    correct_total=41277
    correct_good=38481
    if len(good)!=correct_good:
        print("good should be:",correct_good)
    return good
def get_filenames_from_camera_folders(path,root=None):
    correct_length=49
    print("getting directories from:",root,path)
    camera_folders=f.get_camera_folders(path,root=root)
    print(type(camera_folders),len(camera_folders),"camera folders, first:",camera_folders[0][0])
    if len(camera_folders)!=correct_length:
        print("length should be:",correct_length)
    else:
        print("length is correct")
    #missing=set(['L:/a2d2/camera_lidar_semantic/20181016_095036/camera/cam_front_center','L:/a2d2/camera_lidar_semantic/20181204_191844/camera/cam_front_center'])
    missing_=['20181016_095036/camera/cam_front_center','20181204_191844/camera/cam_front_center']
    missing=[join(path,part) for part in missing_]
    print("we expect problems with:",missing)
    # L:/a2d2/camera_lidar_semantic/20181016_095036/camera/cam_front_center
    # L:/a2d q2/camera_lidar_semantic/20181204_191844/camera/cam_front_center
    return get_files_from_camera_folders(list(zip(*camera_folders)))
root=f.get_root()
path=f.get_path()
(filename,image_filename,json_filename,label_filename)=f.get_my_filenames()
actual=[]
if os.path.exists(image_filename):
    print(image_filename+" exists")
    print("reading:",image_filename)
    actual=f.read_filenames_from_disk(image_filename)
else:
    print(image_filename+" does not exist.")
    print("examining camera folder for files")
    good=get_filenames_from_camera_folders(path,root=root)
    print(type(good),len(good),"good file names")
    print(good[0])
    print(type(good),len(good),"good file names")
    #print(good[0])
    ts=tuple(zip(*good))
    (images,jsons,labels)=ts
    p(images,jsons,labels)
    print(labels[0])
    if not (len(images)==len(jsons) and len(images)==len(labels)):
        print("lengths of jsons and/or labels are not equal!")
        #exit()  
    #filename=join(f.get_my_path(),"image_"+"good_file_names.txt")
    f.create_file(image_filename,images)
    f.create_file(json_filename,jsons)
    f.create_file(label_filename,labels)
    print("reading:",image_filename)
    actual=f.read_filenames_from_disk(image_filename)
    print("check")
    if not f.is_ok(actual,images):
        print("badness")
print(len(actual),"image file names")
# make into a function


