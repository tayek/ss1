#!/usr/bin/python
#https://www.tutorialspoint.com/python/python_multithreading.htm
import multiprocessing as mp
import threading
import time
import gc

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, q,f=None):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
      self.f = f
   def run(self):
      print("Starting " + self.name)
      process_data(self.name, self.q,self.f)
      print("Exiting " + self.name)

def process_data(threadName, q,f=None):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
           data = q.get()
           queueLock.release()
           print("%s processing %s" % (threadName, data))
           if f is not None:
               f(data)
               pass

        else:
           queueLock.release()
        time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = mp.Queue(10)
threads = []
threadID = 1

def f0(x):
    print('x',x)
# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue,f0)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")
def main():
    #run()
    pass
if __name__ == "__main__":
   main()
   pass