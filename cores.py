from multiprocessing import util,Process, Manager
#from classes import BaseClass, SubclassOne, SubclassTwo, SubclassThree
import gc
import logging
verbose=True
class BaseClass():
    def __init__(self):
        #print("ctor:",self)
        pass
    def __run__(self):
        print("run:",self,'&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        pass
    def __del__(self):
        print("dtor base class:",super(),", type:",type(super()))
        #super().__del__()
        #super(type(self), self).__del__() # gets RecursionError: maximum recursion depth exceeded while calling a Python object
class SubclassOne(BaseClass):
    def __init__(self):
        print("ctor:",self)
        pass
    def __del__(self):
        #print("dtor subclass1:",super(),", type:",type(super()))
        super(type(self), self).__del__() 
class SubclassTwo(BaseClass):
    def __init__(self):
        #print("ctor:",self)
        super(type(self), self).__del__() 
    def __del__(self):
        #print("dtor subclass2:",super(),", type:",type(super()))
        super(type(self), self).__del__() 
class SubclassThree(BaseClass):
    def __init__(self):
        #print("ctor:",self)
        pass
    def __del__(self):
        #print("dtor subclass3:",super(),", type:",type(super()))
        pass
util.log_to_stderr(level=logging.DEBUG)
class Main():
    def __init__(self):
        self.manager = Manager()
        self.first_q  = self.manager.Queue()
        self.second_q = self.manager.Queue()
        self.objs = [SubclassOne(), SubclassTwo(), SubclassThree()]
        for obj in self.objs:
            self.first_q.put(obj)
#fruit = 'Apple'
#print('<<<<<<<<<<<<<')
#print(True if fruit == 'Apple' else False)            
#print('>>>>>>>>>>>>>')
x=SubclassOne()
y=SubclassTwo()
z=SubclassThree()
del x
del y
del z
gc.collect()
if __name__ == '__main__':
    #main = Main()
    pass