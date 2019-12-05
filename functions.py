import platform;
print("get platform")
print("platform:",platform.python_implementation())
print("got platform")
import numpy as np
np.set_printoptions(precision=4)
import numpy.linalg as la
from os.path import join
import glob
import ntpath
import json
import pathlib
from timeit import default_timer as timer
epsilon = 1.0e-10 # norm should not be small
from contextlib import contextmanager
#from time import time
from timeit import default_timer as timer
@contextmanager
def timing(description: str,units=1,title="",before="") -> None:
    if before!="":
        print(before,flush=True)
    start = timer()
    yield
    dt = timer() - start
    frequency=0 if units is None else (units/dt)
    np.set_printoptions(precision=4)
    #print(f"{description}: {dt} seconds. {str(frequency)}") if n is None else print(f"{description}: {dt} seconds.")
    if units is None:
        print(f"{title} {description}: {dt} seconds.",flush=True)
    else:
        print(f"{title} {description}: {dt} seconds. {str(frequency)} units/second.",flush=True) 
    return dt
def fix(path):
    return path.replace("\\","/").replace("\\","")
def path_head(path):
    head, tail = ntpath.split(path)
    return head
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
def get_root():
    return "L:/ss/" # was l:
def get_path():
    return "sem"
def get_my_path():
    return "data"
def get_my_filenames():
    filename=join(get_my_path(),"good_file_names.txt")
    image_filename=join(get_my_path(),"image_"+"good_file_names.txt")
    json_filename=join(get_my_path(),"json_"+"good_file_names.txt")
    label_filename=join(get_my_path(),"label_"+"good_file_names.txt")
    return (fix(filename),fix(image_filename),fix(json_filename),(label_filename))
def get_lists_of_filenames():
    (filename,image_filename,json_filename,label_filename)=get_my_filenames()
    images=read_filenames_from_disk(image_filename)
    jsons=read_filenames_from_disk(json_filename)
    labels=read_filenames_from_disk(label_filename)
    return (images,jsons,labels)
def get_camera_pattern():
    return '*/camera/*'
def get_files(path,pattern,root=None):
    path = join(root,pattern,path) if root is not None else join(path,pattern)
    path=fix(path)
    files = sorted(glob.glob(path))
    fixed=[fix(file) for file in files]
    return fixed
def get_flowers_files(path,pattern):
    path=pathlib.Path(path)
    from_glob=get_files(path,pattern)
    return from_glob
def get_camera_folder(path,root=None):
    path = join(root,path) if root is not None else join(path)
    path=fix(path)
    images=get_files(path,'*/camera/*')
    return images
def get_camera_folders(path,root=None): # get file in camera folders
    #path=fix(path) # may have to change this back
    path = join(root,path) if root is not None else join(path)
    images=get_files(path,'*/camera/*')
    jsons=get_files(path,'*/camera/*')
    labels=get_files(path,'*/label/*')
    return (images,jsons,labels) #used to return these zipped
def get_json(filename):
    with open (join(get_root(),filename), 'r') as file:
        config = json.load(file)
    return config
# file_name_image_info = file_name_image.replace(".png", ".json")",
def read_image_info(file_name):
    with open(file_name, 'r') as file:
        image_info = json.load(file)
    return image_info
def get_label_filename(file_name_image): # maybe not used?
    parts = file_name_image.split('/')
    file_name_semantic_label = parts[-1].split('.')[0]
    words=file_name_semantic_label = file_name_semantic_label.split('_')
    file_name_semantic_label = file_name_semantic_label[0] + '_' + 'label_' +  file_name_semantic_label[2] + '_' + file_name_semantic_label[3] + '.png'
    return file_name_semantic_label
def extract_semantic_file_name_from_image_file_name(file_name_image): # not used from tutorial
    file_name_semantic_label = file_name_image.split('/')
    file_name_semantic_label = file_name_semantic_label[-1].split('.')[0]
    file_name_semantic_label = file_name_semantic_label.split('_')
    file_name_semantic_label = file_name_semantic_label[0] + '_' + 'label_' +  file_name_semantic_label[2] + '_' + file_name_semantic_label[3] + '.png'
    return file_name_semantic_label
def create_file(filename,lines):
    try:
        with open(filename,'w') as filehandle:
            for line in lines:
                filehandle.write(line+'\n')
    except Exception as e:
        print(e)
def is_ok(actual,expected):
    n=min(len(actual),len(expected))
    if(len(actual)!=len(expected)):
        print("files have different lengths:",len(actual),"!=",len(expected))
    for i in range(n):
        if actual[i]!=expected[i]:
            print("actual:",str(actual[i]))
            print("expected:",str(expected[i]))
            print(i,str(actual[i])+"!="+str(expected[i]))
            return False
    return True
def read_filenames_from_disk(filename):
    l=[]
    try:
        with open(filename, 'r') as filehandle:
            lines = filehandle.readlines()
            actual = [line.strip() for line in lines]
            for line in actual:
                #l.append(join(path_prefix,actual))
                l.append(line)
    except Exception as e:
        print(e)
    return l
