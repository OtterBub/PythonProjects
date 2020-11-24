import threading
from multiprocessing import Process
from typing import Any, Callable, List, Mapping, Optional, Tuple

class thrList:
    def __init__(self):
        self.ThreadList = []

    def addThread(self, funcTarget:Optional[Callable[..., Any]] = ... ,funcArgs:tuple = []):
        thr = threading.Thread(target=funcTarget, args=funcArgs)
        self.ThreadList.append(thr)

    def startThread(self):
        for thr in self.ThreadList:
            thr.start()

    def join(self):
        for thr in self.ThreadList:
            thr.join()

    def clear(self):
        self.ThreadList.clear()

class test:
    def __init__(self):
        self.a = 10

def func(i:test = None):
    print("func start")
    print(i)
    i.a = 20
    print(i)

if __name__ == "__main__":
    thli = thrList()
    a = test()
    a.a = 1
    print(id(a))
    #func(a)

    thli.addThread(func, (a,))
    thli.startThread()
    thli.join()

    print(a.a)