# how fast can we read the data?
# looks like about 10 files/second
from os import listdir
import sys
import gc
import objgraph
import os.path
import numpy as np
from matplotlib import image as im
from matplotlib import pyplot
from PIL import Image
import functions as f
from mt0 import processFile
print("code")
def process_files(folder,filenames):
    for i,filename in enumerate(filenames):
        if '.png' in filename:
            # load image
            path=folder+'/'+filename
            processFile(path)
        if i%100==0:
            print(i,filename)
def process_folder(folder):
    l=listdir(folder)
    print(folder,'folder has:',len(l),'files.')
    with f.timing("process:"+str(len(l))+" files from: "+str(folder),units=len(l)):
        print("1")
        process_files(folder,l)
def run():
    print("-----------------------------------------")
    [print("local ssd")]
    process_folder("X:/cam_front_center") # on a local ssd.
    print("-----------------------------------------")
    [print("nas")]
    with f.timing("get camera folders",units=1):
        folders,jsons,labels=f.get_camera_folders(f.get_path(),root=f.get_root())
    print(len(folders)," camera folders")
    for folder in folders:
        process_folder(folder)
        if True:
            break
def main():
    np.set_printoptions(precision=4)
    run()
if __name__ == "__main__":git 
   main()
   pass