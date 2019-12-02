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
def check_other_files(images):
    for n,image in enumerate(images):
        if n==0:
            print("first image file in folder:",image)
        json=image.replace(".png", ".json")
        if n==0:
            print("first json file in folder:",json)
        if not isfile(json):
            missing_jsons.append(json)
        label=image.replace("camera", "label")
        if n==0:
            print("first label file in folder:",label)
        if not isfile(label):
            print("missing label file:",label,"\nfor image file:",image)
            missing_labels.append(label)
def get_files_from_camera_folders(camera_folders): 
    good=[]
    for i,folder in enumerate(camera_folders[0]):
        if i==0:
            print("camera folders: ",type(camera_folders),len(camera_folders))
        images=f.get_files(folder,"*.png")
        if len(missing_images)>0:
            print(len(missing_jsons),"missing images, out of:",len(images))
        if len(missing_jsons)>0:
            print(len(missing_jsons),"missing jsons, out of:",len(images))
        if len(missing_labels)>0:
            print(len(missing_labels),"missing labels, out of:",len(images))
        if False:
            check_other_files(images)
        good.extend(images)
        if fast and (len(good)>100 or i>0):
            break
    print(len(good),".png's")
    correct_total=41277
    correct_good=38481
    if len(good)!=correct_good:
        print("good should be:",correct_good)
    return good
def get_filenames_from_camera_folders(path,root=None):
    correct_length=44
    print("getting directories from:",root,path)
    camera_folders=f.get_camera_folder(path,root=root)
    print(type(camera_folders),len(camera_folders),"camera folders, first:",camera_folders[0])
    if len(camera_folders)!=correct_length:
        print("length should be:",correct_length)
    else:
        print("length is correct")
    #missing=set(['L:/a2d2/camera_lidar_semantic/20181016_095036/camera/cam_front_center','L:/a2d2/camera_lidar_semantic/20181204_191844/camera/cam_front_center'])
    missing_=['20181016_095036/camera/cam_front_center','20181204_191844/camera/cam_front_center']
    missing=[join(path,part) for part in missing_]
    print("we expect problems with:",missing)
    # L:/a2d2/camera_lidar_semantic/20181016_095036/camera/cam_front_center
    # L:/a2d2/camera_lidar_semantic/20181204_191844/camera/cam_front_center
    return get_files_from_camera_folders((camera_folders,)) # do not remove the ','
root=f.get_root()
path=f.get_path()
(filename,image_filename,json_filename,label_filename)=f.get_my_filenames()
image_filename=filename
actual=[]
if os.path.exists(image_filename):
    print(image_filename+" exists")
    print("reading:",image_filename)
    actual=f.read_filenames_from_disk(image_filename)
else:
    print(image_filename+" does not exist.")
    print("examining camera folder for files")
    good=get_filenames_from_camera_folders(path,root=root)
    print(type(good),len(good),"file names")
    print(good[0])
    images=good
    jsons=[]
    labels=[]
    if not (len(images)==len(jsons) and len(images)==len(labels)):
        print("lengths of jsons and/or labels are not equal!")
        #exit()  
    f.create_file(filename,good)
    print("reading:",filename)
    actual=f.read_filenames_from_disk(filename)
    print("check")
    if not f.is_ok(actual,good):
        print("badness")
print(len(actual),"image file names")
# make into a function
