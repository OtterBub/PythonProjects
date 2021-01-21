import subprocess
import threading
import os
import glob
import sys

from custom import ADBcommand

def cmdfunc(c:str):
    subprocess.run(c, shell=True, text=True)

tlist = ADBcommand.thrList()

cmd:list = []

pattern = os.path.dirname(sys.argv[0]) + r"\*.py"
for r in glob.glob(pattern):
    cmd.append('pyinstaller -F "%s"' %r)

# subprocess.run(c, shell=True, check=True)

for c in cmd:
    tlist.addThread(funcTarget=cmdfunc, funcArgs=(c,))

tlist.startThread()
tlist.join()

tlist.clear()
cmd.clear()

pattern = os.path.dirname(sys.argv[0]) + r"\*.spec"
for r in glob.glob(pattern):
    cmd.append('del "%s"' %r)
cmd.append('rmdir /s /q build')
cmd.append('rmdir /s /q __pycache__')
cmd.append('pip freeze > "%s\\requirements.txt"' %(os.path.dirname(sys.argv[0])))

for c in cmd:
    tlist.addThread(funcTarget=cmdfunc, funcArgs=(c,))

tlist.startThread()
tlist.join()

cmdfunc('pip freeze > "%s\\requirements.txt"' %(os.path.dirname(sys.argv[0])))

flist = list()
f = open('%s\\requirements.txt' %(os.path.dirname(sys.argv[0])), mode='r')
for r in f.readlines():
    flist.append(r.replace("==", ">="))
f.close()

f2 = open('%s\\requirements.txt' %(os.path.dirname(sys.argv[0])), mode='w')
for r in flist:
    f2.write(r)
f2.close()
    
print('\n\n\n----- Result List -----')

pattern = os.path.dirname(sys.argv[0]) + r"\dist\*.exe"
for r in glob.glob(pattern):
    f = os.path.basename(r).split('.')
    print('%s.%s' %(f[0], f[1]))

input('\nPyInstall Complete Press Enter')