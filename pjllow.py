# https://machinelearningmastery.com/how-to-load-and-manipulate-images-for-deep-learning-in-python-with-pil-pillow/
from __future__ import absolute_import, division, print_function, unicode_literals
print("start")
from os import listdir
import sys
import gc
#(596, 2, 1)
import objgraph
import os.path
import numpy as np
from matplotlib import image as im
from matplotlib import pyplot
from PIL import Image
import functions as f
def load_some_from_one_camera_folder(folder,limit=None):
    loaded_images = list()
    print("cars:",camera_folder)
    l=listdir(folder)
    print('folder has:',len(l))
    for i,filename in enumerate(l):
        if '.png' in filename:
            # load image
            path=camera_folder+'/'+filename
            img_data = im.imread(path)
            if i<20: # uses all of memory
                loaded_images.append(img_data)
                gc.collect()
            if i<5 or i%10==0:
                print('> loaded %d %s %s' % (i,filename, img_data.shape))
            if limit!=None and i>=limit:
                break
    return i+1,loaded_images
def save_as_jpeg(pngfilename):
    print("save as jpeg:",pngfilename)
    image = Image.open(pngfilename) # load the image
    path=f.path_head(pngfilename)
    filename=f.path_leaf(pngfilename)
    print(path,filename)
    target='.png'
    if target in filename:
        print(len(filename),len(target))
        part=filename[:len(filename)-len(target)]
        print("part:",part)
        filename=part+'.jpeg'
    jpegfilename='data/'+filename
    print(filename)
    #print("format:",image.format,", mode:",image.mode,"size:",image.size) # summarize some details about the image
    image.save(jpegfilename, format='JPEG')
    return image
def load_and_save_some(folder,limit=None):
    print('in save some, folder:',folder)
    for i,filename in enumerate(listdir(folder)):
        print("file:",i,filename)
        if '.png' in filename:
            image=save_as_jpeg(folder+'/'+filename)
            del image; gc.collect()
            if limit!=None and i>=limit:
                break
    return i+1
def time_load_images(folder,limit=None):
    with f.timing("load from camera folder: "+folder):
        n,l=load_some_from_one_camera_folder(folder,limit=limit)
        print('read:',n,', loaded:',len(l),'images.')
def time_load_and_save_images(folder,limit=None):
    with f.timing("load and save images: "+folder):
        n,l=load_and_save_some(folder,limit=limit)
        print('read:',n,', loaded:',len(l),'images.')
print(gc.get_threshold())
print(gc.get_count())

jpegfilename='Sydney-Opera-House.jpg'
pngfilename='Sydney-Opera-House.png'

image = Image.open(jpegfilename) # load the image
print("format:",image.format,", mode:",image.mode,"size:",image.size) # summarize some details about the image
#image.show() # show the image

image.save(pngfilename, format='PNG')
image2 = Image.open(pngfilename) # load the image again and inspect the format
print("format:",image2.format,", mode:",image2.mode,"size:",image2.size) # summarize some details about the image


data = im.imread(jpegfilename) # load image as pixel array
print("data.type:",data.dtype,"data.shape:",data.shape) # summarize shape of the pixel array
pyplot.imshow(data) # display the array of pixels as an image
#pyplot.show()

# load image and convert to and from NumPy array
image = Image.open(jpegfilename) # load the image
data = np.asarray(image) # convert image to numpy array
print("data.shape",data.shape) # summarize shape
image2 = Image.fromarray(data) # create Pillow image
print("format:",image2.format,", mode:",image2.mode,"size:",image2.size) # summarize image details
data2 = np.asarray(image2) # convert second image to numpy array
print("data2.type:",data.dtype,"data2.shape:",data.shape) # summarize shape of the pixel array
print("1:",str(data)[:60])
print("2",str(data2)[:60])
print(True) if str(data)[:100]==str(data2)[:100] else print(False)
print('-----------------------------')

# load some images from a directory
camera_folder="L:/ss/sem/20181108_123750/camera/cam_front_center" # more than 2k
camera_folder="L:/ss/sem/20180807_145028/camera/cam_front_center" # 942 - first usually
afile='L:/ss/sem/20180807_145028/camera/cam_front_center/20180807145028_camera_frontcenter_000021937.png'
#afile='L:\ss\sem\20180807_145028\camera\cam_front_center.20180807145028_camera_frontcenter_000021937.png'
#afile='L:\\ss\\sem\\20180807_145028\\camera\\cam_front_center.20180807145028_camera_frontcenter_000021937.png'
if os.path.isfile(afile):
    print(afile,"exists.")
else:
    print(afile,"does not exist!")
time_load_images(camera_folder)
#objgraph.show_most_common_types()
#objgraph.show_backrefs(loaded_images)
#print("ref count:",sys.getrefcount(img_data))
#print(gc.get_threshold())
#print(gc.get_count())
gc.collect()
#print(gc.get_threshold())
print(gc.get_count())
exit()
load_and_save_some(camera_folder,limit=10)
gc.collect()
#print(gc.get_threshold())
print(gc.get_count())
