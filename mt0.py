#!/usr/bin/python
#https://www.tutorialspoint.com/python/python_multithreading.htm
import multiprocessing as mp
import threading
import time
import os
import sys
import functions as f
import typing as ty
import slow as sl
import gc
from matplotlib import image as im
testMode=False
def readFile(path):
    image = im.imread(path)
    if verbose: print("read file:",os.path.basename(path))
    gc.collect() # not sure where this should go
    return image
def slow4040(unused):
   sl.slow(40,40)
def enqueue(l:ty.Iterable[str]):
   if verbose: print("length:",len)
   for word in l:
      #if verbose: print("enqueue:",word)
      gl['queue'].put(word)
def processFile(path,f=None,g=None):
   name=os.path.basename(path)
   if verbose: print("path:",name)
   if f is None: return path
   y=f(path)
   if g is None: return y
   z=g(y)
   return z
def processData(threadName,q:mp.Queue,f=None,g=None):
   while not gl['done']:
      if verbose: print("not done, acquire lock")
      gl['lock'].acquire()
      if verbose: print("got lock")
      if not gl['queue'].empty():
         data = q.get()
         gl['lock'].release()
         if verbose: print("%s processing %s" % (threadName, data))
         if os.path.isfile(data): processFile(data,f=f,g=g)
      else:
         if verbose: print("release lock")
         gl['lock'].release()
         if verbose: print(threadName,"says queue is empty")
      time.sleep(1)
class myThread (threading.Thread):
   def __init__(self, id, name, q:mp.Queue,f,g):
      threading.Thread.__init__(self)
      self.threadID = id
      self.name = name
      self.q = q
      self.f = f
      self.g = g
   def run(self):
      if verbose: print("Starting " + self.name)
      processData(self.name, self.q,f=self.f,g=self.g)
      if verbose: print("Exiting " + self.name)
def get_pngs(folder):
   l=os.listdir(folder) # global?
   l=[folder+'/'+e for e in l if '.png' in e]
   return l
def get_files(units=None):
    images,jsons,labels=f.get_camera_folders(f.get_path(),root=f.get_root())
    print(len(images),' folders for images')
    l=[]
    for folder in images:
        l=get_pngs(folder)
        break # just do one now.
    folder=images[0]
    l=l if units is None else l[:units]
    return l
def getList(units=None):
   if testMode: dataList = ["One", "Two", "Three", "Four", "Five"]
   else: dataList=get_files(units=units)
   return dataList
#global dataList
verbose=True
gl={'done':False,'queue':None,'lock':None} # global dictionary
nThreads=5
threadNames = ['Thread-'+str(i) for i in range(nThreads)]
def run(units=None):
   dataList=getList(units=units)
   print("process",len(dataList),"units using",len(threadNames),"threads.")
   gl['lock']=threading.Lock()
   gl['queue']=mp.Queue()
   f1=g=None
   if True:
      f=readFile
      g=slow4040
   print("f:",f,", g:",g)
   threads = [myThread(i+1, name, gl['queue'],f=f1,g=g) for i,name in enumerate(threadNames)]
   for thread in threads: thread.start()
   gl['lock'].acquire()
   enqueue(dataList)
   gl['lock'].release()
   with f.timing("queue is empty",units=units,title="",before="wait for queue to empty"):
      while not gl['queue'].empty():
         pass
   if verbose: print("run() says queue is empty.")
   if verbose: print("set done true.")
   gl['done']=True
   if verbose: print("wai for join.")
   for t in threads:
      t.join()
   if verbose: print("exit run()")
def main():
   units=40
   run(units=units)
if __name__ == "__main__":
    main()
