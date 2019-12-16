import os
import math
import os.path as op
import functions as f
import sys
def printffo(files,folders,others):
    print("files:",files[:3])
    print("folders:",folders[:3])
    print("others:",others[:3])
def getffo(path:str): # files, folders, others
    l=os.listdir(path)
    folders=[e for e in l if op.isdir(op.join(path,e))]
    #print(f.ppl0(folders,name="folders"))
    maybies=list(set(l)-set(folders))
    files=[e for e in l if op.isfile(op.join(path,e))]
    others=list(set(maybies)-set(files))
    printffo(files,folders,others)
    return (files,folders,others)
def printijo(imageFiles,jsonFiles,otherFiles):
    print("image_files:",imageFiles[:3])
    print("json_files:",jsonFiles[:3])
    print("others:",otherFiles[:3])
def getijo(l:list): # images, jsons, others - should only be given files.
    imageFiles=[e for e in l if '.png' in e]
    maybeFiles=list(set(l)-set(imageFiles))
    jsonFiles=[e for e in maybeFiles if '.json' in e]
    otherFiles=list(set(maybeFiles)-set(jsonFiles))
    if len(maybeFiles)!=0: print("maybies:",maybeFiles[:3])
    printijo(imageFiles,jsonFiles,otherFiles)
    return imageFiles,jsonFiles,otherFiles
path=op.join(f.get_root(),f.get_path()) # these will be sorted
(folders,y,z)=f.get_camera_folders(path)
print('--------------------------')
f.ppl0(folders,name="folders from get camera folders",print_=True)
print('--------------------------')
files,folders,others=getffo(path)
print('--------------------------')
for folder in folders:
    (files2,folders2,others2)=getffo(op.join(path,folder))
    for folder2 in folders2:
        print("process folder:",folder2)
        files3,folders3,others3=getffo(op.join(path,folder,folder2)) # may need camera or lifar sun directory?
        for folder3 in folders3:
            print("process folder:",folder2)
            files4,folders4,others4=getffo(op.join(path,folder,folder2,folder3)) # may need camera or lifar sun directory?
            (imageFiles,jsonFiles,otherFiles)=getijo(files4)
            if True: 
                print("breaking out of loop after folder3:",folder3)
                break
        if True: 
            print("breaking out of loop after folder1:",folder2)
            break
        print('--------------------------')
    if True: 
        print("breaking out of loop after folder:",folder)
        break
print('--------------------------')

git sta# looks like getting them with listir will be painfull without glob :(
# maybe just use get_camera_folders()
#print(dir())
