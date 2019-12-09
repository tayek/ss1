#!/usr/bin/python
#https://www.tutorialspoint.com/python/python_multithreading.htm
# uses mutithreading to see if it is of any use.
import multiprocessing as mp
import threading
import time
import os
import gc
import functions as f
import slow
from matplotlib import image as im
def process_file(filename):
    image = im.imread(filename)
    gc.collect() # not sure where this should go
    return image
class myThread (threading.Thread):
    def __init__(self, threadID, name, q,f=None,g=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.f = f
        self.g = g
def process_data(threadName, q,f=None,g=None):
    global queueLock,workQueue,files_processed
    while not exitFlag:
        print(threadName,"acquiring lock")
        queueLock.acquire()
        print(threadName,"acquired lock")
        if not workQueue.empty():
            print(threadName,"wait for get")
            data = q.get()
            print(threadName,"got",data)
            queueLock.release()
            name=os.path.basename(data)
            if True:
                if True or files_processed%10==0:
                    print("%s is processing %s" % (threadName, name))
            if f is not None:
                y=f(data)
            if g is not None:
                f(y)
            files_processed+=1
        else:
            print(threadName, "release lock, queue is empty")
            queueLock.release()
        time.sleep(1)
    def run(self):
        print("enter run() " + self.name)
        process_data(self.name, self.q,self.f,self.g)
        print("exit run() " + self.name)
queueLock=None
workQueue=None
exitFlag = 0
files_processed=0
def run():
    n_threads=10
    units=20
    names=['Thread-'+str(e+1) for e in list(range(n_threads))]
    global queueLock,workQueue
    queueLock = threading.Lock()
    workQueue = mp.Queue(2000)
    threads = []
    threadID = 1
    # Create new threads
    for tName in names:
        thread = myThread(threadID, tName, workQueue,process_file)
        thread.start()
        print("starting thread:",tName)
        threads.append(thread)
        threadID += 1
    images,jsons,labels=f.get_camera_folders(f.get_path(),root=f.get_root())
    print(len(images),' camera folders for images')
    l=None  # global?
    for folder in images:
        l=os.listdir(folder) # global?
        break # just do one now.
    folder=images[0]
    l=[folder+'/'+e for e in l if '.json' not in e]
    l=l[:units]
    print("process",len(l),"files using",len(names),"threads.")
    # Fill the queue
    queueLock.acquire()
    for e in l:
        name=os.path.basename(e)
        print('enqueue:',name)
        workQueue.put(e)
    queueLock.release()
    # Wait for queue to empty
    print("wair for queue to empty")
    with f.timing("Wait for queue to empty: "+str(folder),units=units):
        while not workQueue.empty():
            pass
    # Notify threads it's time to exit
    global exitFlag
    exitFlag = 1
    # Wait for all threads to complete
    for t in threads:
        t.join()
    #print("Exiting Main Thread")
def main():
    run()
if __name__ == "__main__":
    main()
#http://www.cs.bsu.edu/homepages/dmz/cs335/ppt/pascal/pascal.ppt
#http://web.cse.ohio-state.edu/~soundarajan.1/courses/788/madsenPaper.pdf
#http://www.allisons.org/ll/ProgLang/PL-Block/
#https://www.quora.com/What-is-block-structured-language
