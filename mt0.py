#!/usr/bin/python
#https://www.tutorialspoint.com/python/python_multithreading.htm
import multiprocessing as mp
import threading
import time
import os
import sys
#import functions as f
import typing as ty
def enqueue(l:ty.Iterable[str]):
   for word in l:
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
def processData(threadName, q):
   while not exitFlag:
      queueLock.acquire()
      if not workQueue.empty():
         data = q.get()
         queueLock.release()
         print("%s processing %s" % (threadName, data))
      else:
         queueLock.release()
      time.sleep(1)
nThreads=3
threadNames = ['Thread-'+str(i) for i in range(nThreads)]
dataList = ["One", "Two", "Three", "Four", "Five"]
if True:
   # get thread couny and names
   pass
queueLock = threading.Lock()
workQueue = mp.Queue(10)
threads = []
if True:
   threads = [myThread(i+1, name, workQueue) for i,name in enumerate(threadNames)]
   for thread in threads:
      thread.start()
else:
   for id,name in enumerate(threadNames):
      thread = myThread(id+1, name, workQueue)
      thread.start()
      threads.append(thread)
queueLock.acquire()
enqueue(dataList)
queueLock.release()
while not workQueue.empty():
   pass
exitFlag = 1
for t in threads:
   t.join()
print("Exiting Main Thread")
