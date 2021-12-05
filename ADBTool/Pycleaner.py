import subprocess
import threading
import os
import glob
import sys

from custom import ADBcommand

def cmdfunc(c:str):
    subprocess.run(c, shell=True, text=True)

def delcmd(ext:str= None):
    tlist = ADBcommand.thrList()
    cmd:list = []

    pattern = os.path.dirname(sys.argv[0]) + ext
    for r in glob.glob(pattern):
        cmd.append('del "%s"' %r)

    for c in cmd:
        tlist.addThread(funcTarget=cmdfunc, funcArgs=(c,))

    tlist.startThread()
    tlist.join()
    tlist.clear()
    cmd.clear()

if __name__ == "__main__":        

    delcmd(r"\*.pcap")
    delcmd(r"\*.log")
    delcmd(r"\*.json")

    # tlist = ADBcommand.thrList()

    # cmd:list = []

    # pattern = os.path.dirname(sys.argv[0]) + r"\*.pcap"
    # for r in glob.glob(pattern):
    #     cmd.append('del "%s"' %r)

    # for c in cmd:
    #     tlist.addThread(funcTarget=cmdfunc, funcArgs=(c,))

    # tlist.startThread()
    # tlist.join()
    # tlist.clear()
    # cmd.clear()

    # pattern = os.path.dirname(sys.argv[0]) + r"\*.log"
    # for r in glob.glob(pattern):
    #     cmd.append('del "%s"' %r)

    # for c in cmd:
    #     tlist.addThread(funcTarget=cmdfunc, funcArgs=(c,))

    # tlist.startThread()
    # tlist.join()
    # tlist.clear()
    # cmd.clear()
        
    print('end')