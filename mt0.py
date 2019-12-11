#!/usr/bin/python
#https://www.tutorialspoint.com/python/python_multithreading.htm
import multiprocessing as mp
import threading
import time
import os
import sys
import functions as f
import typing as ty
def enqueue(l:ty.Iterable[str]):
   for word in l:
      print("enqueue:",word)
      workQueue.put(word)
exitFlag = 0
class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.threadID = threadID
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print("Starting " + self.name)
      processData(self.name, self.q)
      print("Exiting " + self.name)
def processFile(path,f=None,g=None):
   if f is not None:
      y=f(path)
      if g is not None:
         z=g(y)
         return z
      else:
         return y
   else:
      return path

   
def processData(threadName, q):
   while not exitFlag:
      print("no exit, acquire lock")
      queueLock.acquire()
      print("got lock")
      if not workQueue.empty():
         data = q.get()
         queueLock.release()
         print("%s processing %s" % (threadName, data))
         if os.path.isfile(data):
            processFile(data)
      else:
         queueLock.release()
      time.sleep(1)
def get_pngs(folder):
   l=os.listdir(folder) # global?
   l=[folder+'/'+e for e in l if '.png' in e]
   return l
def get_files(units):
    images,jsons,labels=f.get_camera_folders(f.get_path(),root=f.get_root())
    print(len(images),' camera folders for images')
    global l
    l=[]
    for folder in images:
        l=get_pngs(folder)
        break # just do one now.
    folder=images[0]
    l=l[:units]
    return l

nThreads=3
threadNames = ['Thread-'+str(i) for i in range(nThreads)]
global dataList
dataList=[]
units=20
if True:
   dataList=get_files(units)
else:
   dataList = ["One", "Two", "Three", "Four", "Five"]
print("process",len(dataList),"units using",len(threadNames),"threads.")
queueLock = threading.Lock()
workQueue = mp.Queue()
threads = [myThread(i+1, name, workQueue) for i,name in enumerate(threadNames)]
for thread in threads:
   thread.start()
queueLock.acquire()
enqueue(dataList)
queueLock.release()
while not workQueue.empty():
   pass
exitFlag = 1
for t in threads:
   t.join()
print("Exiting Main Thread")
